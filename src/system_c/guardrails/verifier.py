"""
Active Hallucination & Numerical Grounding Guardrail Node for System C.

Owned by: Aryan (Citations, Guardrails & RQ2 Lead)
Integration Contract:
- Inspects `draft_answer` (or `final_answer`) against `accumulated_evidence`.
- Extracts all numerical figures (dollar values, percentages, basis points) in the answer
  and verifies whether they exist in the retrieved context (ignoring year numbers like 2024/2025/2026
  and citation chunk indices).
- Populates `guardrail_passed` and `guardrail_report` (containing `numerical_grounding_error_rate`
  and `faithfulness_score` for RQ2).
"""

import re
from typing import Any, Dict, List

from src.system_c.state import AdaptiveRAGState
from src.system_c.telemetry import track_node_latency


def _extract_candidate_numbers(text: str) -> List[str]:
    """
    Extract quantitative numbers (decimals, comma-separated numbers, percentages, dollar figures)
    while stripping out `[...]` inline citation tags and 4-digit fiscal years.
    """
    # Strip bracketed citations first so chunk IDs like `:42` or `FY2026` aren't treated as claims
    text_no_cites = re.sub(r"\[[^\[\]]+\]", " ", text)
    raw_matches = re.findall(r"\b\d{1,3}(?:,\d{3})+(?:\.\d+)?%?(?!\w)|\b\d+\.\d+%?(?!\w)|\b\d+%(?!\w)", text_no_cites)
    cleaned = []
    for m in raw_matches:
        num_str = m.rstrip("%").replace(",", "")
        if re.fullmatch(r"199\d|20[0-2]\d", num_str):
            continue
        cleaned.append(m)
    return cleaned


def verify_numerical_grounding(answer: str, evidence_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compare every quantitative figure in `answer` against `evidence_chunks` to compute
    RQ2's Numerical Grounding Error Rate.
    """
    combined_corpus = " ".join(c.get("content", "") for c in evidence_chunks)
    combined_normalized = combined_corpus.replace(",", "")

    numbers = _extract_candidate_numbers(answer)
    verified: List[str] = []
    ungrounded: List[str] = []

    for token in numbers:
        norm_tok = token.rstrip("%").replace(",", "")
        if token in combined_corpus or norm_tok in combined_normalized:
            verified.append(token)
        else:
            ungrounded.append(token)

    total = len(numbers)
    error_rate = round(len(ungrounded) / total, 4) if total > 0 else 0.0
    faithfulness_score = round(1.0 - error_rate, 4)

    return {
        "total_numerical_claims": total,
        "verified_numbers": verified,
        "ungrounded_numbers": ungrounded,
        "numerical_grounding_error_rate": error_rate,
        "faithfulness_score": faithfulness_score,
        "has_inline_citations": bool(re.search(r"\[[^\[\]]+\]", answer)),
    }


def guardrail_node(state: AdaptiveRAGState) -> Dict[str, Any]:
    """
    LangGraph Node (Aryan's Module):
    Audits `draft_answer` for numerical grounding & inline citations and produces `final_answer` + `guardrail_report`.
    """
    telemetry = dict(state.get("telemetry", {}))
    draft = state.get("draft_answer") or state.get("final_answer") or ""
    evidence = state.get("accumulated_evidence", [])

    with track_node_latency(telemetry, "guardrail"):
        report = verify_numerical_grounding(draft, evidence)
        passed = len(report["ungrounded_numbers"]) == 0

        final_ans = draft
        if not passed:
            flagged_str = ", ".join(report["ungrounded_numbers"])
            final_ans = (
                f"{draft}\n\n> [Guardrail Audit Warning]: The following numerical figures could not be "
                f"exact-matched in the retrieved chunks and require manual verification: {flagged_str}."
            )

    return {
        "final_answer": final_ans,
        "guardrail_passed": passed,
        "guardrail_report": report,
        "telemetry": telemetry,
    }
