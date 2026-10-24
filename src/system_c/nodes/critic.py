"""
Evidence Sufficiency Critic Node (Self-RAG / Adaptive Reflection) for System C.

Owned by: Anish (System Architect & Orchestration Lead)

Responsibilities:
1. Evaluates whether `accumulated_evidence` contains sufficient factual and numerical premises
   to completely answer `original_query`.
2. Computes quantitative evidence sufficiency score (0.0 to 1.0) and compares against
   `sufficiency_threshold` (default 0.85) to enable early stopping.
3. Detects laser-focused missing entity gaps (`missing_entities`) and year gaps (`missing_years`)
   to instruct Aryan's `generator.py` for focused follow-ups.
4. Prevents redundant search loops when tabular XBRL or text chunks already provide complete
   factual coverage or when retrieval has saturated.
5. Populates `is_sufficient`, `sufficiency_score`, `missing_premises`, `missing_entities`,
   `missing_years`, and `critic_reasoning`.
6. Records intermediate reasoning trace in `intermediate_answers` and tracks early-stopping for RQ3.
"""

import json
import re
from typing import Any, Dict, List, Set

from src.system_c.llm import call_llm, clean_and_parse_json
from src.system_c.state import AdaptiveRAGState

CRITIC_SYSTEM_PROMPT = """You are an Evidence Sufficiency Critic for an SEC 10-K Financial RAG system.
Evaluate whether the Accumulated Evidence (including any tabular XBRL blocks) contains ALL required facts, numbers, and footnote context to thoroughly answer the Original Query.

Return ONLY a valid JSON object with keys:
- "sufficiency_score": float between 0.0 and 1.0 representing quantitative evidence completeness:
    * 1.0: Complete, comprehensive coverage of all requested entities, line items, and fiscal years.
    * 0.85 - 0.99: High sufficiency; all primary premises and core figures are present. Meets early-stopping criteria.
    * 0.50 - 0.84: Partial sufficiency; some key data points, footnotes, or comparative entities are missing.
    * 0.0 - 0.49: Low sufficiency; major gaps in required facts or numbers.
- "is_sufficient": boolean (true if sufficiency_score >= 0.85 or all essential premises are satisfied; false otherwise)
- "missing_entities": list of strings identifying specific missing financial entities, line items, or metrics (e.g. ["2022 R&D spending", "AWS operating income"]). Empty list [] if sufficient.
- "missing_years": list of integer fiscal years missing data (e.g. [2022]). Empty list [] if all requested years are represented.
- "missing_premises": list of specific missing facts or targeted questions for the next retrieval hop (empty list [] if is_sufficient is true)
- "critic_reasoning": concise 1-2 sentence justification explaining what is covered and what remains missing."""


def _parse_critic_json(raw_text: str) -> Dict[str, Any]:
    return clean_and_parse_json(raw_text)


def critic_node(state: AdaptiveRAGState) -> Dict[str, Any]:
    """
    LangGraph Node: Inspect `accumulated_evidence` at `current_hop` and decide whether
    to stop early (`is_sufficient=True`) or trigger another hop via Aryan's `generator_node`.
    """
    hop = state.get("current_hop", 1)
    max_hops = state.get("max_hops", 3)
    evidence = state.get("accumulated_evidence", [])
    tabular = state.get("tabular_evidence", [])
    threshold = float(state.get("sufficiency_threshold", 0.85))

    evidence_digest = "\n\n".join(
        f"[{c['chunk_id']}] (Hop {c['hop_retrieved']}, Section: {c['metadata'].get('section', 'N/A')}):\n"
        f"{c['content'][:450]}"
        for c in evidence[-8:]
    )

    tabular_digest = "\n".join(f"- {t[:250]}" for t in tabular) if tabular else "None"

    target_tickers = state.get("target_tickers") or ([state.get("target_ticker")] if state.get("target_ticker") else [])
    fiscal_years = state.get("fiscal_years", [])

    user_prompt = (
        f"Original Query: {state['original_query']}\n"
        f"Target Tickers: {target_tickers}\n"
        f"Fiscal Years: {fiscal_years}\n"
        f"Current Hop: {hop} of {max_hops}\n"
        f"Planned Sub-Queries: {state.get('sub_queries', [])}\n\n"
        f"Tabular XBRL Evidence Available:\n{tabular_digest}\n\n"
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

    # In RQ3 Fixed Max-Hops ablation benchmark, force the critic not to early-stop before max_hops
    if state.get("force_max_hops"):
        is_sufficient = hop >= max_hops
        score = 1.0 if is_sufficient else 0.50
        missing_premises = [] if is_sufficient else ["RQ3 ablation forced hop continuation"]
        missing_entities: List[str] = []
        missing_years: List[int] = []
        redundant_prevented = False
        reasoning = f"RQ3 Fixed {max_hops}-Hop benchmark: hop {hop}/{max_hops}."
    else:
        # 1. Parse quantitative sufficiency score
        try:
            score = float(parsed.get("sufficiency_score", 0.0))
            score = max(0.0, min(1.0, score))
        except (ValueError, TypeError):
            score = 0.95 if parsed.get("is_sufficient") else 0.40

        # 2. Parse laser-focused missing entities and years
        raw_entities = parsed.get("missing_entities") or []
        missing_entities = [str(e).strip() for e in raw_entities if str(e).strip()]

        raw_years = parsed.get("missing_years") or []
        missing_years = []
        for y in raw_years:
            try:
                missing_years.append(int(y))
            except (ValueError, TypeError):
                pass

        raw_premises = parsed.get("missing_premises") or []
        missing_premises = [str(m).strip() for m in raw_premises if str(m).strip()]

        # Align missing_premises with missing_entities & missing_years if omitted
        if not missing_premises and (missing_entities or missing_years):
            for ent in missing_entities:
                missing_premises.append(f"Disclosures and line items for {ent}")
            for yr in missing_years:
                missing_premises.append(f"Financial disclosures for fiscal year {yr}")

        reasoning = str(parsed.get("critic_reasoning") or f"Evaluated {len(evidence)} chunks at Hop {hop}.")

        # 3. Prevent redundant search loops & check complete factual coverage
        redundant_prevented = False

        # Detection A: Chunk saturation check (hop > 1 returned no new unique chunks)
        if hop > 1:
            prev_chunk_ids: Set[str] = {
                c["chunk_id"] for c in evidence if c.get("hop_retrieved", 1) < hop
            }
            curr_hop_chunks = [c for c in evidence if c.get("hop_retrieved") == hop]
            curr_chunk_ids: Set[str] = {c["chunk_id"] for c in curr_hop_chunks}

            # If current hop produced no new chunks, or all chunk IDs already existed
            if curr_hop_chunks and curr_chunk_ids.issubset(prev_chunk_ids):
                redundant_prevented = True
                score = max(score, threshold)
                reasoning += " [Redundant loop prevented: Hop retrieved duplicate chunks with zero new coverage]."

        # Detection B: Tabular XBRL complete coverage for quantitative queries
        # If query needs tabular tool and tabular_evidence exists covering all target tickers
        if state.get("needs_tabular_tool") and tabular:
            covered_tickers = {t for t in target_tickers if any(f"F-{t}" in blk for blk in tabular)}
            if target_tickers and covered_tickers == set(target_tickers):
                # Check if query actually requires qualitative text (footnotes, risks, drivers)
                q_lower = state.get("original_query", "").lower()
                has_qualitative_need = any(
                    w in q_lower for w in ("risk", "footnote", "impact", "legal", "covenant", "contingenc", "why", "driver", "strategy", "cause")
                )
                if not has_qualitative_need or (not missing_entities and not missing_years):
                    score = max(score, 0.95)
                    missing_entities = []
                    missing_years = []
                    missing_premises = []
                    redundant_prevented = True
                    reasoning += " [Complete factual coverage: Tabular XBRL tool provided exact reported financials]."

        # 4. Apply quantitative early-stopping threshold (>= threshold triggers early stop)
        if score >= threshold or bool(parsed.get("is_sufficient", False)):
            is_sufficient = True
            missing_premises = []
            missing_entities = []
            missing_years = []
        else:
            is_sufficient = False

    # Record intermediate hop trace for RQ1 / RQ3 interpretability
    intermediate = list(state.get("intermediate_answers", []))
    intermediate.append(
        {
            "hop": hop,
            "sub_query_executed": state.get("current_sub_query", ""),
            "chunks_accumulated": len(evidence),
            "is_sufficient": is_sufficient,
            "sufficiency_score": round(score, 4),
            "missing_premises": missing_premises,
            "missing_entities": missing_entities,
            "missing_years": missing_years,
            "redundant_search_prevented": redundant_prevented,
            "critic_reasoning": reasoning,
        }
    )

    if is_sufficient and hop < max_hops:
        updated_telemetry["early_stopped"] = True
    updated_telemetry["hop_count"] = hop

    return {
        "is_sufficient": is_sufficient,
        "sufficiency_score": round(score, 4),
        "missing_premises": missing_premises,
        "missing_entities": missing_entities,
        "missing_years": missing_years,
        "redundant_search_prevented": redundant_prevented,
        "critic_reasoning": reasoning,
        "intermediate_answers": intermediate,
        "telemetry": updated_telemetry,
    }
