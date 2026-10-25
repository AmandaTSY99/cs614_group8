"""
Conditioned Follow-Up Sub-Query Generator Node for System C.

Owned by: Aryan (Citations, Guardrails & Conditioned Sub-Query Lead)
Integration Contract with Anish's Critic & Retriever:
- Reads `original_query`, `accumulated_evidence`, `missing_entities`, `missing_years`, `missing_premises`
  and `critic_reasoning` from `AdaptiveRAGState`; sentinel values ("None", "N/A", ...) count as empty.
- Shows the LLM a compact one-line-per-chunk summary of ALL accumulated evidence (capped at 40 lines).
- The LLM still chooses the Hop N+1 search query (`current_sub_query`); a near-duplicate of an earlier
  sub-query (word overlap >= 0.8 after removing section words and stopwords), or an unparseable reply,
  is replaced by a short fallback: `<ticker> <first missing entity or premise>` (at most 15 words).
- Increments `current_hop`.
- Uses `call_llm(state, "generator", messages)` so RQ3 token & latency telemetry are recorded automatically.
"""

import json
import re
from typing import Any, Dict, List, Set, Tuple

from src.system_c.guardrails.citations import short_section
from src.system_c.llm import call_llm
from src.system_c.state import AdaptiveRAGState

GENERATOR_SYSTEM_PROMPT = """You are a Financial Multi-Hop Sub-Query Generator for SEC 10-K filings.
Given the Original Query, the Evidence Retrieved so far, and the Missing Entities, Missing Years and Missing Premises flagged by the Sufficiency Critic, formulate ONE precise, targeted follow-up search query for the next retrieval hop.
Focus on specific 10-K sections, tables, footnotes, debt covenants, or quantitative line items that are still missing.
Do not repeat an already executed sub-query.

Return ONLY valid JSON:
{
  "follow_up_query": "targeted search query string",
  "reasoning": "why this query resolves the missing premise"
}"""

SENTINELS = {"", "none", "none.", "n/a", "na", "null", "nothing", "[]", "no missing entities"}
MAX_SUMMARY_LINES = 40
DUPLICATE_OVERLAP = 0.8
MAX_FALLBACK_WORDS = 15

STOPWORDS = {
    "a", "an", "and", "the", "of", "for", "in", "on", "to", "by", "with", "from", "at", "as", "or",
    "is", "are", "was", "were", "be", "its", "their", "what", "which", "how", "did", "does", "do",
    "fiscal", "year", "fy",
}
# Section locators are removed before the repeat check, so a query that only swaps the section
# (e.g. "Item 7 MD&A" -> "Item 8 financial statements and notes") still counts as a duplicate.
SECTION_PHRASES_RE = re.compile(
    r"\bitem\s+\d+[a-z]?\b|\bitem\b|\bmd\s*&\s*a\b|\bmarket\s+risk\b|\brisk\s+factors\b"
    r"|\b(?:consolidated\s+)?financial\s+statements\b|\bnotes\b",
    re.IGNORECASE,
)


def _clean_list(values: Any) -> List[str]:
    """Drop sentinel values ("None", "N/A", "null", "[]", blanks) and exact duplicates."""
    if isinstance(values, str):
        values = [values]
    cleaned: List[str] = []
    for v in values or []:
        s = str(v).strip()
        if s.lower() not in SENTINELS and s not in cleaned:
            cleaned.append(s)
    return cleaned


def _clean_years(values: Any) -> List[int]:
    if isinstance(values, (str, int)):
        values = [values]
    years: List[int] = []
    for v in values or []:
        s = str(v).strip().upper()
        if s.lower() in SENTINELS:
            continue
        try:
            y = int(s[2:] if s.startswith("FY") else s)
        except ValueError:
            continue
        if y not in years:
            years.append(y)
    return years


def _chunk_ticker(chunk: Dict[str, Any]) -> str:
    ticker = (chunk.get("metadata") or {}).get("ticker")
    if ticker:
        return str(ticker).upper()
    cid = str(chunk.get("chunk_id", ""))
    if cid.startswith("F-"):
        return cid.split("-")[1].upper() if cid.count("-") >= 2 else ""
    return cid.split("_")[0].upper()


def _evidence_summary(state: AdaptiveRAGState) -> Tuple[str, int]:
    """`chunk_id | TICKER FYyear | short section`, one line per accumulated chunk (most recent 40 kept)."""
    evidence = state.get("accumulated_evidence", [])
    lines = []
    for c in evidence[-MAX_SUMMARY_LINES:]:
        meta = c.get("metadata") or {}
        year = meta.get("fiscal_year")
        lines.append(
            f"{c['chunk_id']} | {_chunk_ticker(c)} FY{year if year is not None else '?'} | "
            f"{short_section(meta.get('section'))}"
        )
    return "\n".join(lines) or "(none)", len(evidence)


def _word_set(text: str) -> Set[str]:
    """Lowercase content words, with section locators and stopwords removed."""
    text = SECTION_PHRASES_RE.sub(" ", text.lower())
    return {w for w in re.findall(r"[a-z0-9&]+", text) if w not in STOPWORDS}


def _jaccard(a: str, b: str) -> float:
    wa, wb = _word_set(a), _word_set(b)
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


def _is_duplicate(query: str, earlier: List[str]) -> bool:
    return any(_jaccard(query, q) >= DUPLICATE_OVERLAP for q in earlier)


def _fallback_query(state: AdaptiveRAGState, entities: List[str], premises: List[str]) -> str:
    """`<ticker> <first missing entity or premise>`, at most 15 words."""
    tickers = state.get("target_tickers") or []
    ticker = state.get("target_ticker") or (tickers[0] if tickers else "")
    item = (entities or premises or [state["original_query"]])[0]
    return " ".join(f"{ticker} {item}".split()[:MAX_FALLBACK_WORDS])


def generator_node(state: AdaptiveRAGState) -> Dict[str, Any]:
    """
    LangGraph Node (Aryan's Module):
    Generates the next conditioned sub-query when `critic_node` determines `is_sufficient == False`.
    """
    next_hop = state.get("current_hop", 1) + 1
    planned_sub_queries = list(state.get("sub_queries", []))
    earlier_queries = planned_sub_queries + [
        q for q in [state.get("current_sub_query")] if q and q not in planned_sub_queries
    ]

    entities = _clean_list(state.get("missing_entities"))
    years = _clean_years(state.get("missing_years"))
    premises = _clean_list(state.get("missing_premises"))
    evidence_summary, n_chunks = _evidence_summary(state)

    user_prompt = (
        f"Original Query: {state['original_query']}\n"
        f"Target Ticker: {state.get('target_ticker')}\n"
        f"Fiscal Years: {state.get('fiscal_years')}\n"
        f"Critic Reasoning: {state.get('critic_reasoning')}\n"
        f"Missing Entities: {entities}\n"
        f"Missing Years: {years}\n"
        f"Missing Premises: {premises}\n"
        f"Already Executed Sub-Queries: {earlier_queries}\n\n"
        f"Evidence Retrieved So Far ({n_chunks} chunks; chunk_id | company year | section):\n{evidence_summary}"
    )

    raw_resp, updated_telemetry = call_llm(
        state=state,
        node_name="generator",
        messages=[
            {"role": "system", "content": GENERATOR_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
        json_mode=True,
    )

    follow_up_query = ""
    try:
        match = re.search(r"\{.*\}", raw_resp.strip(), flags=re.DOTALL)
        parsed = json.loads(match.group(0) if match else raw_resp)
        follow_up_query = str(parsed.get("follow_up_query", "")).strip()
    except Exception:
        pass

    # A near-duplicate of an earlier sub-query, or an unparseable reply, gets the short fallback.
    if not follow_up_query or _is_duplicate(follow_up_query, earlier_queries):
        follow_up_query = _fallback_query(state, entities, premises)

    if follow_up_query not in planned_sub_queries:
        planned_sub_queries.append(follow_up_query)

    return {
        "current_hop": next_hop,
        "current_sub_query": follow_up_query,
        "sub_queries": planned_sub_queries,
        "telemetry": updated_telemetry,
    }
