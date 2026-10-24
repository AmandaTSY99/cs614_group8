"""
Query Decomposer & Complexity Planner Node for System C.

Owned by: Anish (System Architect & Orchestration Lead)

Responsibilities:
1. Extracts `target_ticker` and `fiscal_years` (and `target_pairs`) from `original_query`.
2. Classifies `query_complexity` ("single_hop" vs "multi_hop") and `needs_tabular_tool` (for v2 AAMR).
3. Decomposes complex financial queries into ordered atomic `sub_queries` and sets Hop 1's `current_sub_query`.
"""

import json
import re
from typing import Any, Dict, List

from src.system_c.corpus import extract_tickers_and_years_from_query, to_ticker
from src.system_c.llm import call_llm
from src.system_c.state import AdaptiveRAGState

DECOMPOSER_SYSTEM_PROMPT = """You are a Senior Financial Analyst & Query Planner for SEC 10-K filings.
Given a user's financial question, return a strict JSON object with the following keys:
- "target_ticker": primary stock ticker (one of AAPL, AMZN, GOOGL, JNJ, JPM, META, MSFT, NVDA, TSLA, WMT, or null)
- "fiscal_years": list of integer fiscal years mentioned (e.g. [2024, 2025]), or empty list []
- "query_complexity": "single_hop" if it asks for one isolated fact, or "multi_hop" if it connects multiple sections, years, drivers, or footnotes
- "needs_tabular_tool": true if the question asks for reported financial metrics (revenue, net income, operating income, assets, liabilities, equity, cash flow, EPS, margins)
- "sub_queries": list of 1 to 3 atomic search queries ordered logically (Hop 1: primary entity/MD&A driver, Hop 2: specific footnote/table/risk factor)

Respond ONLY with valid JSON."""


def _parse_json_safely(raw_text: str) -> Dict[str, Any]:
    """Extract and parse JSON object from LLM output, handling markdown code fences."""
    cleaned = raw_text.strip()
    fence_match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if fence_match:
        cleaned = fence_match.group(0)
    try:
        return json.loads(cleaned)
    except Exception:
        return {}


def decomposer_node(state: AdaptiveRAGState) -> Dict[str, Any]:
    """LangGraph Node: Decompose `original_query` into sub-goals and extract metadata filters."""
    query = state["original_query"]
    regex_ticker, regex_years = extract_tickers_and_years_from_query(query)

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

    # Resolve ticker & fiscal years (combining explicit state overrides, LLM extraction, and regex fallback)
    llm_ticker = to_ticker(str(parsed.get("target_ticker") or "")) if parsed.get("target_ticker") else None
    ticker = state.get("target_ticker") or llm_ticker or regex_ticker

    llm_years: List[int] = []
    for y in parsed.get("fiscal_years") or []:
        try:
            llm_years.append(int(y))
        except (ValueError, TypeError):
            pass
    fiscal_years = state.get("fiscal_years") or llm_years or regex_years

    pairs = (
        [[ticker, y] for y in fiscal_years]
        if (ticker and fiscal_years)
        else ([[ticker, None]] if ticker else [])
    )

    sub_queries = parsed.get("sub_queries")
    if not isinstance(sub_queries, list) or not sub_queries:
        sub_queries = [query]
    sub_queries = [str(sq).strip() for sq in sub_queries if str(sq).strip()]

    complexity = str(parsed.get("query_complexity", "multi_hop"))
    if complexity not in ("single_hop", "multi_hop"):
        complexity = "multi_hop"

    needs_tabular = bool(parsed.get("needs_tabular_tool", False))
    if not needs_tabular and any(
        kw in query.lower()
        for kw in ("revenue", "margin", "income", "eps", "asset", "liability", "cash flow", "debt", "equity")
    ):
        needs_tabular = True

    return {
        "target_ticker": ticker,
        "fiscal_years": fiscal_years,
        "target_pairs": pairs,
        "query_complexity": complexity,
        "needs_tabular_tool": needs_tabular,
        "sub_queries": sub_queries,
        "current_sub_query": sub_queries[0],
        "current_hop": 1,
        "telemetry": updated_telemetry,
    }
