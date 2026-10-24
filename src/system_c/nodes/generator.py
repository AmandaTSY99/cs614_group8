"""
Conditioned Follow-Up Sub-Query Generator Node for System C.

Owned by: Aryan (Citations, Guardrails & Conditioned Sub-Query Lead)
Integration Contract with Anish's Critic & Retriever:
- Reads `original_query`, `accumulated_evidence`, `missing_premises`, and `critic_reasoning` from `AdaptiveRAGState`.
- Generates a targeted Hop N+1 search query (`current_sub_query`) and increments `current_hop`.
- Uses `call_llm(state, "generator", messages)` so RQ3 token & latency telemetry are recorded automatically.
"""

import json
import re
from typing import Any, Dict

from src.system_c.llm import call_llm
from src.system_c.state import AdaptiveRAGState

GENERATOR_SYSTEM_PROMPT = """You are a Financial Multi-Hop Sub-Query Generator for SEC 10-K filings.
Given the Original Query, the Evidence Retrieved so far, and the Missing Premises flagged by the Sufficiency Critic, formulate ONE precise, targeted follow-up search query for the next retrieval hop.
Focus on specific 10-K sections, tables, footnotes, debt covenants, or quantitative line items that are still missing.

Return ONLY valid JSON:
{
  "follow_up_query": "targeted search query string",
  "reasoning": "why this query resolves the missing premise"
}"""


def generator_node(state: AdaptiveRAGState) -> Dict[str, Any]:
    """
    LangGraph Node (Aryan's Module):
    Generates the next conditioned sub-query when `critic_node` determines `is_sufficient == False`.
    """
    next_hop = state.get("current_hop", 1) + 1
    planned_sub_queries = list(state.get("sub_queries", []))
    missing = state.get("missing_premises", [])

    evidence_summary = "\n".join(
        f"- [{c['chunk_id']}] ({c['metadata'].get('section', 'N/A')}): {c['content'][:200]}"
        for c in state.get("accumulated_evidence", [])[-4:]
    )

    user_prompt = (
        f"Original Query: {state['original_query']}\n"
        f"Target Ticker: {state.get('target_ticker')}\n"
        f"Fiscal Years: {state.get('fiscal_years')}\n"
        f"Critic Reasoning: {state.get('critic_reasoning')}\n"
        f"Missing Premises: {missing}\n"
        f"Already Executed Sub-Queries: {planned_sub_queries}\n\n"
        f"Recent Retrieved Evidence:\n{evidence_summary}"
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

    # Fallback to pre-planned sub-query or missing premise if JSON parsing falls back
    if not follow_up_query:
        if len(planned_sub_queries) >= next_hop:
            follow_up_query = planned_sub_queries[next_hop - 1]
        elif missing:
            follow_up_query = f"{state.get('target_ticker') or ''} {missing[0]}".strip()
        else:
            follow_up_query = f"{state['original_query']} footnote table details"

    if follow_up_query not in planned_sub_queries:
        planned_sub_queries.append(follow_up_query)

    return {
        "current_hop": next_hop,
        "current_sub_query": follow_up_query,
        "sub_queries": planned_sub_queries,
        "telemetry": updated_telemetry,
    }
