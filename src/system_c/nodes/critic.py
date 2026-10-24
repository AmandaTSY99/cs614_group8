"""
Evidence Sufficiency Critic Node (Self-RAG / Adaptive Reflection) for System C.

Owned by: Anish (System Architect & Orchestration Lead)

Responsibilities:
1. Evaluates whether `accumulated_evidence` contains sufficient factual and numerical premises
   to completely answer `original_query`.
2. Populates `is_sufficient`, `missing_premises` (explicit instructions for Aryan's `generator.py`),
   and `critic_reasoning`.
3. Records intermediate reasoning trace in `intermediate_answers` and tracks early-stopping for RQ3.
"""

import json
import re
from typing import Any, Dict

from src.system_c.llm import call_llm
from src.system_c.state import AdaptiveRAGState

CRITIC_SYSTEM_PROMPT = """You are an Evidence Sufficiency Critic for an SEC 10-K Financial RAG system.
Evaluate whether the Accumulated Evidence contains ALL required facts, numbers, and footnote context to thoroughly answer the Original Query.

Return ONLY a valid JSON object with keys:
- "is_sufficient": boolean (true if the evidence is complete; false if important premises, numbers, or footnote details are still missing)
- "missing_premises": list of specific missing facts or questions that the next retrieval hop must look up (empty list [] if is_sufficient is true)
- "critic_reasoning": concise 1-2 sentence justification of your sufficiency decision."""


def _parse_critic_json(raw_text: str) -> Dict[str, Any]:
    cleaned = raw_text.strip()
    match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if match:
        cleaned = match.group(0)
    try:
        return json.loads(cleaned)
    except Exception:
        return {}


def critic_node(state: AdaptiveRAGState) -> Dict[str, Any]:
    """
    LangGraph Node: Inspect `accumulated_evidence` at `current_hop` and decide whether
    to stop early (`is_sufficient=True`) or trigger another hop via Aryan's `generator_node`.
    """
    hop = state.get("current_hop", 1)
    max_hops = state.get("max_hops", 3)
    evidence = state.get("accumulated_evidence", [])

    evidence_digest = "\n\n".join(
        f"[{c['chunk_id']}] (Hop {c['hop_retrieved']}, Section: {c['metadata'].get('section', 'N/A')}):\n"
        f"{c['content'][:450]}"
        for c in evidence[-8:]
    )

    user_prompt = (
        f"Original Query: {state['original_query']}\n"
        f"Current Hop: {hop} of {max_hops}\n"
        f"Planned Sub-Queries: {state.get('sub_queries', [])}\n\n"
        f"Accumulated Evidence ({len(evidence)} chunks):\n{evidence_digest}"
    )

    raw_resp, updated_telemetry = call_llm(
        state=state,
        node_name="critic",
        messages=[
            {"role": "system", "content": CRITIC_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
        json_mode=True,
    )
    parsed = _parse_critic_json(raw_resp)

    is_sufficient = bool(parsed.get("is_sufficient", False))
    missing_premises = [str(m) for m in (parsed.get("missing_premises") or []) if str(m).strip()]
    reasoning = str(parsed.get("critic_reasoning") or f"Evaluated {len(evidence)} chunks at Hop {hop}.")

    # Record intermediate hop trace for RQ1 / RQ3 interpretability
    intermediate = list(state.get("intermediate_answers", []))
    intermediate.append(
        {
            "hop": hop,
            "sub_query_executed": state.get("current_sub_query", ""),
            "chunks_accumulated": len(evidence),
            "is_sufficient": is_sufficient,
            "missing_premises": missing_premises,
            "critic_reasoning": reasoning,
        }
    )

    if is_sufficient and hop < max_hops:
        updated_telemetry["early_stopped"] = True
    updated_telemetry["hop_count"] = hop

    return {
        "is_sufficient": is_sufficient,
        "missing_premises": missing_premises,
        "critic_reasoning": reasoning,
        "intermediate_answers": intermediate,
        "telemetry": updated_telemetry,
    }
