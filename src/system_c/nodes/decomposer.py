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

# Standard 10-column continuous SEC XBRL financial schema mapping (financials.csv)
XBRL_CORE_METRICS: Dict[str, List[str]] = {
    "revenue": ["total revenue", "revenue", "net sales", "total sales", "turnover"],
    "net_income": ["net income", "net earnings", "profit"],
    "operating_income": ["operating income", "operating profit", "ebit"],
    "total_assets": ["total assets"],
    "total_liabilities": ["total liabilities"],
    "stockholders_equity": [
        "stockholders equity", "shareholders equity", "stockholders' equity",
        "shareholders' equity", "book value",
    ],
    "cash_and_equivalents": ["cash and cash equivalents", "cash and equivalents", "cash balance"],
    "operating_cash_flow": [
        "operating cash flow", "cash from operations", "cash flow from operations",
        "cash flows from operating", "ocf",
    ],
    "eps_diluted": ["diluted eps", "diluted earnings per share", "earnings per share", "eps"],
}

# Negative exclusion indicators: granular footnotes, segments, debt schedules, or narrative explanations
# that CANNOT be satisfied by continuous macro financial statement totals (financials.csv).
FOOTNOTE_OR_SEGMENT_EXCLUSIONS: List[str] = [
    "gross margin", "operating margin", "profit margin", "margin", "margins",
    "segment", "segments", "division", "geographic", "geographical", "held in",
    "retail square footage", "square footage", "tegra", "aws", "azure", "cloud",
    "intelligent cloud", "compute & networking", "personal computing", "productivity and business",
    "debt maturity", "maturity schedule", "future principal", "principal payment",
    "principal payments", "scheduled to repay", "repay", "repayment", "term debt",
    "long-term debt", "senior notes", "commercial paper", "derivative", "hedging",
    "foreign exchange contract", "fx forward", "covenant", "contingenc", "legal",
    "customer concentration", "concentration", "footnote", "note ", "notes ", "note:",
    "item 8", "item 7", "item 1", "schedule", "research and development", "r&d",
    "share of total sales", "share of sales", "as a share of",
    "goodwill", "reserve", "reserves", "sales return", "returns reserve",
    "stock option", "stock options", "equity incentive", "restricted stock",
    "impairment", "fair value", "pension", "allowance", "valuation",
    "why", "driver", "strategy", "cause", "impact", "explain", "describe", "description",
]


def is_xbrl_headline_target(query: str) -> bool:
    """
    Returns True ONLY if the query explicitly targets standard continuous XBRL headline financial metrics
    (Revenue, Net Income, Operating Income, Total Assets, Total Liabilities, Stockholders Equity,
    Cash & Equivalents, Operating Cash Flow, Diluted EPS) with NO footnote, segment, margin,
    or debt schedule requirements.
    """
    q_lower = query.lower()

    # 1. Any footnote, segment, debt maturity, or qualitative indicator disqualifies XBRL-only pre-retrieval
    for excl in FOOTNOTE_OR_SEGMENT_EXCLUSIONS:
        if excl in q_lower:
            return False

    # 2. Check for explicit match against standard XBRL core metrics
    for metric, aliases in XBRL_CORE_METRICS.items():
        for alias in aliases:
            if alias == "eps":
                if re.search(r"\beps\b", q_lower):
                    return True
            elif alias in q_lower:
                return True

    return False

DECOMPOSER_SYSTEM_PROMPT = """You are a Senior Financial Analyst & Query Planner for SEC 10-K filings.
Given a user's financial question, return a strict JSON object with the following keys:
- "target_ticker": primary stock ticker (one of AAPL, AMZN, GOOGL, JNJ, JPM, META, MSFT, NVDA, TSLA, WMT, or null)
- "target_tickers": list of all stock tickers mentioned if comparing multiple companies, e.g. ["AAPL", "NVDA"]
- "fiscal_years": list of integer fiscal years of the SEC 10-K filings to retrieve (e.g. [2024, 2018]). If the question specifies a filing year (e.g. "According to their fiscal year 2019 10-Ks", "In the 2018 10-K"), include ONLY the filing year(s) to search, NOT future maturity, repayment, or contractual years (e.g. "scheduled to repay in 2020").
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

FUTURE_MATURITY_YEAR_RE = re.compile(
    r"(?:repay(?:ing|ment)?|due|matur(?:ing|ity|ities)|scheduled\s+for|thereafter\s+in)\s+(?:in\s+)?(199\d|20[0-2]\d)",
    re.IGNORECASE,
)


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

    mode = state.get("mode")
    if mode == "v3_aamr_sg":
        # Question Text Year Priority & Semantic Disambiguation for System C v3:
        # Distinguish SEC filing years from future contractual/maturity schedule years (e.g. "repay in 2020").
        future_years = {int(y) for y in FUTURE_MATURITY_YEAR_RE.findall(query)}
        valid_regex_years = [y for y in regex_years if y not in future_years]

        extracted_years: List[int] = []
        for y in (valid_regex_years + llm_years):
            if y not in extracted_years and y not in future_years:
                extracted_years.append(y)

        existing_years = [int(y) for y in (state.get("fiscal_years") or []) if int(y) not in future_years]
        # If question explicitly mentions filing years, those define the filing search pool;
        # otherwise fall back to existing state years.
        fiscal_years = sorted(list(dict.fromkeys(extracted_years if extracted_years else existing_years)))
    else:
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

    mode = state.get("mode")
    if mode == "v3_aamr_sg":
        # System C v3 (AAMR-SG): Schema-aware sufficiency & pre-routing.
        # Only set needs_tabular_tool = True if query explicitly targets one of the standard XBRL headline metrics.
        # Queries for Gross Margin, Segment Revenue, Debt Maturity Schedules, or Footnotes route directly to retriever.
        needs_tabular = is_xbrl_headline_target(query)
        target_metric_type = "xbrl_headline" if needs_tabular else "footnote_disclosure"
        if not needs_tabular:
            for p in sub_query_plans:
                p["target_tool"] = "retriever"
    else:
        # Legacy v1/v2 heuristic routing
        target_metric_type = "xbrl_headline" if parsed.get("needs_tabular_tool") else "hybrid"
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
        "target_metric_type": target_metric_type,
        "last_action": "tabular_tool" if (needs_tabular and mode in ("v2_aamr", "v3_aamr_sg")) else "retriever",
        "sub_queries": sub_queries,
        "sub_query_plans": sub_query_plans,
        "current_sub_query": sub_queries[0],
        "current_hop": 1,
        "telemetry": updated_telemetry,
    }
