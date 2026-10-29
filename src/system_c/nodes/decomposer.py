"""
Query Decomposer & Complexity Planner Node for System C.

Supports Research Question 3 (Inference Economics & Early Stopping):
1. Extracts `target_ticker`, `target_tickers`, and `fiscal_years` from `original_query`.
2. Classifies `query_complexity` ("single_hop" vs "multi_hop") and routes between
   deterministic XBRL (`tabular_tool`) and unstructured 10-K text chunks (`retriever`).
3. Decomposes multi-entity or cross-year comparative queries into ordered sub-queries.
4. Initializes Hop 1 state and sets `current_sub_query`.
"""

import json
import re
from typing import Any, Dict, List

from src.system_c.corpus import (
    extract_all_tickers_and_years_from_query,
    extract_tickers_and_years_from_query,
    to_ticker,
)
from src.system_c.llm import call_llm, clean_and_parse_json
from src.system_c.state import AdaptiveRAGState

DECOMPOSER_SYSTEM_PROMPT = """You are a Senior Financial Analyst & Query Planner for SEC 10-K filings.
Given a user's financial question, return a strict JSON object with the following keys:
- "target_ticker": primary stock ticker (one of AAPL, AMZN, GOOGL, JNJ, JPM, META, MSFT, NVDA, TSLA, WMT, or null)
- "target_tickers": list of all stock tickers mentioned if comparing multiple companies, e.g. ["AAPL", "NVDA"]
- "fiscal_years": list of integer fiscal years mentioned (e.g. [2024, 2025]), or empty list []
- "query_complexity": "single_hop" if it asks for one isolated fact, or "multi_hop" if it connects multiple sections, years, drivers, or footnotes
- "needs_tabular_tool": true if the question asks for reported financial metrics (revenue, net income, operating income, assets, liabilities, equity, cash flow, EPS, margins)
- "sub_query_plans": list of 1 to 4 structured sub-query objects with tool routing:
    [
      {
        "query": "AAPL FY2024 total revenue and operating margin",
        "target_tool": "tabular_tool", // "tabular_tool" if quantitative financial line items; "retriever" if narrative/MD&A/risk/footnotes
        "ticker": "AAPL",
        "fiscal_year": 2024
      }
    ]
    NOTE for multi-ticker comparative queries: Decompose into separate atomic sub-queries for EACH company ticker rather than a single combined query.
- "sub_queries": list of 1 to 4 atomic search query strings corresponding to "sub_query_plans"

Respond ONLY with valid JSON."""


def _parse_json_safely(raw_text: str) -> Dict[str, Any]:
    """Extract and parse JSON object from LLM output with syntax repair."""
    return clean_and_parse_json(raw_text)


def decomposer_node(state: AdaptiveRAGState) -> Dict[str, Any]:
    """LangGraph Node: Decompose `original_query` into sub-goals and extract metadata filters."""
    query = state["original_query"]
    regex_tickers, regex_years = extract_all_tickers_and_years_from_query(query)
    regex_ticker = regex_tickers[0] if regex_tickers else None

    messages = [
        {"role": "system", "content": DECOMPOSER_SYSTEM_PROMPT},
        {"role": "user", "content": f"User Query: {query}"},
    ]
    raw_resp, updated_telemetry = call_llm(
        state=state,
        node_name="decomposer",
        messages=messages,
        temperature=0.0,
        json_mode=True,
    )
    parsed = _parse_json_safely(raw_resp)

    # Resolve primary ticker & all tickers (combining explicit state overrides, LLM extraction, and regex fallback)
    llm_ticker = to_ticker(str(parsed.get("target_ticker") or "")) if parsed.get("target_ticker") else None
    primary_ticker = state.get("target_ticker") or llm_ticker or regex_ticker

    all_tickers: List[str] = list(state.get("target_tickers") or [])
    if not all_tickers:
        for t in parsed.get("target_tickers") or []:
            res_t = to_ticker(str(t))
            if res_t and res_t not in all_tickers:
                all_tickers.append(res_t)
        for t in regex_tickers:
            if t not in all_tickers:
                all_tickers.append(t)
    if primary_ticker and primary_ticker not in all_tickers:
        all_tickers.insert(0, primary_ticker)

    llm_years: List[int] = []
    for y in parsed.get("fiscal_years") or []:
        try:
            llm_years.append(int(y))
        except (ValueError, TypeError):
            pass
    fiscal_years = state.get("fiscal_years") or llm_years or regex_years

    pairs = (
        [[t, y] for t in all_tickers for y in fiscal_years]
        if (all_tickers and fiscal_years)
        else ([[t, None] for t in all_tickers] if all_tickers else ([[primary_ticker, None]] if primary_ticker else []))
    )

    # Parse and validate sub_query_plans with tool routing
    raw_plans = parsed.get("sub_query_plans")
    sub_query_plans: List[Dict[str, Any]] = []
    if isinstance(raw_plans, list) and raw_plans:
        for p in raw_plans:
            if isinstance(p, dict) and p.get("query"):
                q_str = str(p["query"]).strip()
                t_tool = str(p.get("target_tool", "retriever")).lower()
                if t_tool not in ("tabular_tool", "retriever"):
                    is_quant = any(
                        kw in q_str.lower()
                        for kw in ("revenue", "margin", "income", "eps", "asset", "liability", "cash flow", "debt", "equity")
                    )
                    t_tool = "tabular_tool" if is_quant else "retriever"
                sub_query_plans.append(
                    {
                        "query": q_str,
                        "target_tool": t_tool,
                        "ticker": to_ticker(str(p.get("ticker", ""))) or primary_ticker,
                        "fiscal_year": int(p["fiscal_year"]) if p.get("fiscal_year") else (fiscal_years[0] if fiscal_years else None),
                    }
                )

    sub_queries = parsed.get("sub_queries")
    if not isinstance(sub_queries, list) or not sub_queries:
        sub_queries = [query]
    sub_queries = [str(sq).strip() for sq in sub_queries if str(sq).strip()]

    # If sub_query_plans is empty or multi-ticker needs per-ticker atomic splitting
    if not sub_query_plans:
        if len(all_tickers) > 1 and len(sub_queries) <= 1:
            sub_query_plans = []
            for tkr in all_tickers:
                yr_val = fiscal_years[0] if fiscal_years else None
                yr_str = f"FY{yr_val} " if yr_val else ""
                is_quant = any(
                    kw in query.lower()
                    for kw in ("revenue", "margin", "income", "eps", "asset", "liability", "cash flow", "debt", "equity")
                )
                sub_query_plans.append(
                    {
                        "query": f"{tkr} {yr_str}{query}".strip(),
                        "target_tool": "tabular_tool" if is_quant else "retriever",
                        "ticker": tkr,
                        "fiscal_year": yr_val,
                    }
                )
        else:
            for sq in sub_queries:
                sq_lower = sq.lower()
                sq_tickers, sq_years = extract_all_tickers_and_years_from_query(sq)
                sq_ticker = sq_tickers[0] if sq_tickers else primary_ticker
                sq_year = sq_years[0] if sq_years else (fiscal_years[0] if fiscal_years else None)
                is_quant = any(
                    kw in sq_lower
                    for kw in ("revenue", "margin", "income", "eps", "asset", "liability", "cash flow", "debt", "equity", "table", "ratio")
                )
                sub_query_plans.append(
                    {
                        "query": sq,
                        "target_tool": "tabular_tool" if is_quant else "retriever",
                        "ticker": sq_ticker,
                        "fiscal_year": sq_year,
                    }
                )

    # Synchronize sub_queries strings from sub_query_plans
    if sub_query_plans:
        sub_queries = [p["query"] for p in sub_query_plans if p.get("query")]
    if not sub_queries:
        sub_queries = [query]

    complexity = str(parsed.get("query_complexity", "multi_hop"))
    if complexity not in ("single_hop", "multi_hop"):
        complexity = "multi_hop"

    needs_tabular = (
        bool(parsed.get("needs_tabular_tool", False))
        or any(p.get("target_tool") == "tabular_tool" for p in sub_query_plans)
        or any(
            kw in query.lower()
            for kw in ("revenue", "margin", "income", "eps", "asset", "liability", "cash flow", "debt", "equity")
        )
    )

    return {
        "target_ticker": primary_ticker,
        "target_tickers": all_tickers,
        "fiscal_years": fiscal_years,
        "target_pairs": pairs,
        "query_complexity": complexity,
        "needs_tabular_tool": needs_tabular,
        "sub_queries": sub_queries,
        "sub_query_plans": sub_query_plans,
        "current_sub_query": sub_queries[0],
        "current_hop": 1,
        "telemetry": updated_telemetry,
    }
