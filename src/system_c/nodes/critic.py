"""
Evidence Sufficiency Critic Node (Self-RAG / Adaptive Reflection) for System C.

Supports Research Question 3 (Early Stopping & Inference Economics):
1. Evaluates whether `accumulated_evidence` contains sufficient factual and numerical premises
   to completely answer `original_query`.
2. Computes quantitative evidence sufficiency score (0.0 to 1.0) and compares against
   `sufficiency_threshold` (default 0.85) to enable early stopping.
3. Detects laser-focused missing entity gaps (`missing_entities`) and year gaps (`missing_years`)
   to instruct the downstream generator for focused follow-ups.
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
from src.system_c.nodes.decomposer import is_xbrl_headline_target
from src.system_c.state import AdaptiveRAGState

CRITIC_SYSTEM_PROMPT_BASE = """You are an Evidence Sufficiency Critic for an SEC 10-K Financial RAG system.
Evaluate whether the Accumulated Evidence (including any tabular XBRL blocks) contains ALL required facts, numbers, segment breakdowns, and footnote disclosures to thoroughly answer the Original Query.

STRICT RULE 1 (ZERO-TOLERANCE MULTI-COMPANY, SEGMENT & FOOTNOTE COVERAGE):
If the Original Query asks to compare multiple companies (e.g. Microsoft, Amazon, Alphabet), specific business segments (e.g. AWS, Tegra, Intelligent Cloud), granular footnotes (e.g. debt maturity schedules, foreign exchange derivatives, geographic asset splits), or metrics not reported on the face of the financial statements (e.g. gross margin, R&D expense as a share of sales), ALL of them must be present in the evidence.
Note: High-level financial statements [F-...] do NOT contain Gross Margin, Segment Revenue, Debt Maturity Schedules, or Footnote disclosures. If the question asks for these granular items and only macro balance sheet/income statement tables are present:
- "is_sufficient" MUST be false.
- "sufficiency_score" MUST be strictly < 0.70 (e.g. 0.40 - 0.60).
- "missing_premises" MUST list the exact missing footnote, segment, or margin disclosures.

STRICT RULE 2 (CONSISTENCY REQUIREMENT):
If your "critic_reasoning" states that any data point, segment, or footnote is missing, lacking, or not provided, you CANNOT set "is_sufficient": true. You MUST set "is_sufficient": false and "sufficiency_score" < 0.70.

Return ONLY a valid JSON object with keys:
- "sufficiency_score": float between 0.0 and 1.0 representing quantitative evidence completeness:
    * 1.0: Complete, comprehensive coverage of all requested entities, line items, segments, footnotes, and fiscal years.
    * 0.85 - 0.99: High sufficiency; all essential premises, segments, and figures are present. Meets early-stopping criteria.
    * 0.40 - 0.84: Partial sufficiency; some required segments, footnotes, or comparative figures are missing. Requires another retrieval hop.
    * 0.0 - 0.39: Low sufficiency; major gaps in required facts or filers.
- "is_sufficient": boolean (true ONLY if sufficiency_score >= 0.85 AND all requested companies, segments, and footnotes are present; false otherwise)
- "missing_entities": list of strings identifying specific missing financial entities, segments, line items, or metrics (e.g. ["Amazon AWS operating income", "Customer concentration percentages"]). Empty list [] if completely sufficient.
- "missing_years": list of integer fiscal years missing data (e.g. [2022]). Empty list [] if all requested years are represented.
- "missing_premises": list of specific missing facts or targeted questions for the next retrieval hop (empty list [] if is_sufficient is true)
- "critic_reasoning": concise 1-2 sentence justification explaining what is covered and what remains missing."""

# Upgraded prompt for System C v3 ("v3_aamr_sg") with Strict Rule 3 for lead-in chunks & Rule 4 for debt principal disambiguation
CRITIC_SYSTEM_PROMPT_V3 = CRITIC_SYSTEM_PROMPT_BASE.replace(
    "STRICT RULE 2 (CONSISTENCY REQUIREMENT):\nIf your \"critic_reasoning\" states that any data point, segment, or footnote is missing, lacking, or not provided, you CANNOT set \"is_sufficient\": true. You MUST set \"is_sufficient\": false and \"sufficiency_score\" < 0.70.",
    "STRICT RULE 2 (CONSISTENCY REQUIREMENT):\nIf your \"critic_reasoning\" states that any data point, segment, or footnote is missing, lacking, or not provided, you CANNOT set \"is_sufficient\": true. You MUST set \"is_sufficient\": false and \"sufficiency_score\" < 0.70.\n\nSTRICT RULE 3 (UNRESOLVED LEAD-IN SENTENCES & MISSING TABLES):\nIf an evidence chunk contains a forward reference, lead-in sentence, or placeholder such as \"is summarized below:\", \"as follows:\", \"refer to Note X\", or introduces an upcoming table (e.g. stock option activity, contractual obligations, fair value hierarchy), but the ACTUAL NUMERICAL ROWS AND COLUMNS of that table are absent from the evidence, the evidence is INCOMPLETE. You CANNOT set \"is_sufficient\": true. You MUST set \"is_sufficient\": false, set \"sufficiency_score\" < 0.70, and explicitly list the missing table or metric in \"missing_premises\".\n\nSTRICT RULE 4 (DEBT PRINCIPAL VS CONTRACTUAL COMMITMENTS DISAMBIGUATION):\nWhen the user query asks specifically for future principal payments on debt (or principal payments on long-term debt), do NOT accept a Contractual Obligations / Commitments table that combines debt principal and interest. The evidence must include the pure principal repayment/maturity schedule from the Long-Term Debt footnote disclosures."
)

CRITIC_SYSTEM_PROMPT = CRITIC_SYSTEM_PROMPT_V3


def _parse_critic_json(raw_text: str) -> Dict[str, Any]:
    return clean_and_parse_json(raw_text)


def critic_node(state: AdaptiveRAGState) -> Dict[str, Any]:
    """
    LangGraph Node: Inspect `accumulated_evidence` at `current_hop` and decide whether
    to stop early (`is_sufficient=True`) or trigger another hop via `generator_node`.
    """
    hop = state.get("current_hop", 1)
    max_hops = state.get("max_hops", 3)
    evidence = state.get("accumulated_evidence", [])
    tabular = state.get("tabular_evidence", [])
    threshold = float(state.get("sufficiency_threshold", 0.85))

    # Digest all accumulated chunks across all hops (prevents early hop blind spot)
    char_limit = 450 if len(evidence) <= 12 else 250
    evidence_digest = "\n\n".join(
        f"[{c['chunk_id']}] (Hop {c.get('hop_retrieved', 1)}, Section: {c.get('metadata', {}).get('section', 'N/A')}):\n"
        f"{c['content'][:char_limit]}"
        for c in evidence
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

    mode = state.get("mode")
    sys_prompt = CRITIC_SYSTEM_PROMPT_V3 if mode == "v3_aamr_sg" else CRITIC_SYSTEM_PROMPT_BASE

    raw_resp, updated_telemetry = call_llm(
        state=state,
        node_name="critic",
        messages=[
            {"role": "system", "content": sys_prompt},
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
        SENTINELS = {"none", "n/a", "na", "null", "nothing", "[]", "no missing entities", "none."}
        missing_entities = [
            str(e).strip() for e in raw_entities
            if str(e).strip() and str(e).strip().lower() not in SENTINELS
        ]

        raw_years = parsed.get("missing_years") or []
        missing_years = []
        for y in raw_years:
            try:
                missing_years.append(int(y))
            except (ValueError, TypeError):
                pass

        raw_premises = parsed.get("missing_premises") or []
        missing_premises = [
            str(m).strip() for m in raw_premises
            if str(m).strip() and str(m).strip().lower() not in SENTINELS
        ]

        # Align missing_premises with missing_entities & missing_years if omitted
        if not missing_premises and (missing_entities or missing_years):
            for ent in missing_entities:
                missing_premises.append(f"Disclosures and line items for {ent}")
            for yr in missing_years:
                missing_premises.append(f"Financial disclosures for fiscal year {yr}")

        reasoning = str(parsed.get("critic_reasoning") or f"Evaluated {len(evidence)} chunks at Hop {hop}.")

        # Enforce reasoning consistency: if the LLM states that evidence is lacking or missing,
        # ensure missing_premises is populated and score does not prematurely trigger early stopping.
        reasoning_lower = reasoning.lower()
        mentions_missing = any(
            phrase in reasoning_lower
            for phrase in (
                "lack", "lacks", "lacking", "missing", "not provided", "not disclosed",
                "not included", "does not provide", "do not provide", "fails to provide",
                "incomplete", "need further", "further disclosures needed", "absent"
            )
        )
        if mentions_missing and not missing_premises:
            missing_premises.append(reasoning[:120].strip())

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
            mock_target = state.get("telemetry", {}).get("mock_sufficient_at_hop")
            if curr_hop_chunks and curr_chunk_ids.issubset(prev_chunk_ids) and (mock_target is None or hop >= mock_target):
                redundant_prevented = True
                score = max(score, threshold)
                missing_entities = []
                missing_years = []
                missing_premises = []
                reasoning += " [Redundant loop prevented: Hop retrieved duplicate chunks with zero new coverage]."

        # Detection B: Tabular XBRL complete coverage for quantitative queries
        # If query needs tabular tool and tabular_evidence exists covering all target tickers
        mode = state.get("mode")
        if state.get("needs_tabular_tool") and tabular:
            covered_tickers = {t for t in target_tickers if any(f"F-{t}" in blk for blk in tabular)}
            if target_tickers and covered_tickers == set(target_tickers):
                if mode == "v3_aamr_sg":
                    # System C v3 (AAMR-SG): Granularity-aware sufficiency reflection.
                    # Verify target metric is truly in standard continuous XBRL headline schema.
                    # If the query asks for Gross Margin, Segment Revenue, Debt Schedules, or Footnotes,
                    # DO NOT force score = 0.95. Let the LLM Critic's organic score govern early-stopping.
                    q_text = state.get("original_query", "")
                    if is_xbrl_headline_target(q_text):
                        score = max(score, 0.95)
                        missing_entities = []
                        missing_years = []
                        missing_premises = []
                        redundant_prevented = True
                        reasoning += " [Complete factual coverage: Tabular XBRL tool provided exact reported headline financials]."
                    else:
                        # Allow LLM Critic's organic sufficiency score to govern continuation to Hops 2 and 3
                        pass
                else:
                    # Legacy v2 heuristic
                    q_lower = state.get("original_query", "").lower()
                    has_narrative_need = any(
                        w in q_lower for w in (
                            "risk", "footnote", "note", "notes", "segment", "segments",
                            "cloud", "aws", "compute", "intelligent cloud", "concentration",
                            "customer", "impact", "legal", "covenant", "contingenc",
                            "why", "driver", "strategy", "cause", "item 7", "item 8", "item 1"
                        )
                    )
                    # Tabular tool satisfies simple single-hop headline financial lookup when NO narrative/footnote/segment is requested
                    if not has_narrative_need:
                        score = max(score, 0.95)
                        missing_entities = []
                        missing_years = []
                        missing_premises = []
                        redundant_prevented = True
                        reasoning += " [Complete factual coverage: Tabular XBRL tool provided exact reported financials]."

        # Detection C: Multi-company comparative query coverage check
        # For queries with multiple target tickers (e.g. GOLD-51: MSFT, AMZN, GOOGL),
        # verify that all target tickers have at least one retrieved chunk or tabular block.
        if len(target_tickers) > 1:
            covered_companies = set()
            for t in target_tickers:
                has_text = any(
                    c.get("metadata", {}).get("ticker") == t
                    or f"{t}_" in c.get("chunk_id", "")
                    or f"-{t}-" in c.get("chunk_id", "")
                    for c in evidence
                )
                if has_text:
                    covered_companies.add(t)

            missing_tickers = [t for t in target_tickers if t not in covered_companies]
            if missing_tickers and hop < max_hops:
                score = min(score, 0.60)
                is_sufficient = False
                if mode == "v3_aamr_sg":
                    for mt in missing_tickers:
                        if mt not in missing_entities:
                            missing_entities.append(mt)
                else:
                    for mt in missing_tickers:
                        lbl = f"{mt} financial disclosures"
                        if lbl not in missing_entities:
                            missing_entities.append(lbl)
                missing_premises.append(f"Disclosures, line items, and segment performance for {', '.join(missing_tickers)}")
                reasoning += f" [Multi-company coverage incomplete: missing evidence for {', '.join(missing_tickers)}]."

        # Detection D: Unresolved forward reference / lead-in chunk check (System C v3 only)
        if mode == "v3_aamr_sg" and hop < max_hops:
            q_lower = state.get("original_query", "").lower()
            unresolved_lead_in = False
            for c in evidence:
                content = c.get("content", "")
                if re.search(r"(?:summarized below|as follows|the following table)\s*:", content, re.IGNORECASE):
                    if any(term in q_lower for term in ("option", "exercisable", "maturity", "schedule", "contractual", "obligation")):
                        has_exercisable_count = any(
                            "exercisable" in oc.get("content", "").lower()
                            and any(char.isdigit() for char in oc.get("content", ""))
                            and "|" in oc.get("content", "")
                            for oc in evidence
                        )
                        if not has_exercisable_count:
                            unresolved_lead_in = True
                            break
            if unresolved_lead_in:
                score = min(score, 0.65)
                missing_premises.append("Detailed tabular rows for summarized disclosure/schedule")
                reasoning += " [Unresolved lead-in detected: Text references an upcoming disclosure table missing from current evidence]."

        # 4. Apply quantitative early-stopping threshold (>= threshold triggers early stop)
        has_gaps = bool(missing_entities or missing_years or missing_premises)
        if score >= threshold and not has_gaps:
            is_sufficient = True
            missing_premises = []
            missing_entities = []
            missing_years = []
        elif score >= threshold and bool(parsed.get("is_sufficient", False)) and not has_gaps:
            # LLM explicitly certified completeness with score >= threshold and no gaps
            is_sufficient = True
            missing_premises = []
            missing_entities = []
            missing_years = []
        else:
            is_sufficient = False
            # When gaps exist, sufficiency score MUST accurately reflect incomplete coverage
            if has_gaps and score >= threshold:
                score = min(score, 0.70)

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
