"""
Active Hallucination Repair & Self-Correction Node for System C.

Supports Research Question 2 (Active Grounding Error Reduction & Safety):
1. Triggered when `guardrail_passed == False` and `repair_count < max_repairs`.
2. Inspects `guardrail_report["ungrounded_numbers"]`, unverified sentences, and invalid citations.
3. Prompts the LLM with surgical instructions to excise or ground unverified figures.
4. Updates `draft_answer`, rebuilds `citations`, logs `repair_history`, and loops to `guardrail_node`.
"""

from typing import Any, Dict, List

from src.system_c.guardrails.citations import build_citation_records, format_tag
from src.system_c.guardrails.verifier import _extract_numbers, _is_derived, _match_number_in_chunks
from src.system_c.llm import call_llm
from src.system_c.state import AdaptiveRAGState

REPAIR_SYSTEM_PROMPT = """You are a Precision Financial Fact-Auditor & Hallucination Repair Specialist for SEC 10-K filings.
You are given a Draft Financial Answer that failed grounding verification: it contains flagged numbers, sentences that their cited evidence does not support, and/or citation tags that map to no retrieved chunk.

Your task is to revise the answer:
1. For each flagged number, check the provided Evidence Blocks. If the correct figure exists in the evidence, replace the flagged figure with the exact verified figure from the context and cite the block it came from.
2. For each unverified sentence, compare it with the evidence it cites. Fix it so it states only what that evidence supports, or remove the sentence entirely.
3. For each sentence marked "(no valid citation)": find the Evidence Block that contains its figure or claim and append that block's EXACT tag (copied character for character from the "Block [...]" header, including the square brackets) to the end of the sentence. If no block contains it, remove the sentence.
4. If a flagged figure is completely absent from the Evidence Blocks, either remove the sentence or explicitly state that the figure is not disclosed in the filing.
5. Remove or correct any citation tag listed as invalid. Preserve all valid inline citation tags exactly (e.g. `[NVDA FY2026, Item 7, NVDA_FY2026_2026-01-25:42]` or `[F-NVDA-2026]`).
6. Every sentence that states a figure must end with at least one valid citation tag.
7. For a "Computed figure" (a difference, ratio or growth rate), cite BOTH blocks named for its inputs, using their exact tags.
8. Output ONLY the revised, fully grounded answer text."""


def _block_label(ch: Dict[str, Any], default_ticker: str) -> str:
    return format_tag(ch, default_ticker)


def _derivation_hint(num: Dict[str, Any], evidence: List[Dict[str, Any]], default_ticker: str) -> str:
    """
    If a flagged figure can be computed (difference / ratio / growth) from figures in two retrieved chunks
    (searching ALL evidence, not just cited chunks), name both blocks' exact tags so repair cites both.
    The guardrail itself stays strict: it only accepts the derivation once the sentence cites both.
    """
    for i, a in enumerate(evidence):
        for b in evidence[i + 1:]:
            derivation = _is_derived(num, [a, b])
            if derivation and not _is_derived(num, [a]) and not _is_derived(num, [b]):
                tags = f"{_block_label(a, default_ticker)} {_block_label(b, default_ticker)}"
                return (
                    f"{num['value']} = {derivation['operation']} of {derivation['derived_from'][0]} and "
                    f"{derivation['derived_from'][1]}, which come from two blocks; cite BOTH: {tags}"
                )
    return ""


def _unverified_sentence_details(report: Dict[str, Any], evidence: List[Dict[str, Any]], default_ticker: str) -> List[Dict[str, Any]]:
    """Each failed sentence with the numbers flagged in it and the text of the chunks it cites."""
    chunk_by_id = {str(c["chunk_id"]): c for c in evidence}
    unverified = set(report.get("unverified_sentences", []))
    details = []
    for s in report.get("sentences", []):
        if s["text"] not in unverified:
            continue
        # Uncited sentence: point repair at the exact block tags whose content contains its figures
        candidate_tags: List[str] = []
        if not s["chunk_ids"]:
            for num in _extract_numbers(s["text"]):
                for ch in evidence:
                    tag = _block_label(ch, default_ticker)
                    if tag not in candidate_tags and _match_number_in_chunks(num, [ch]):
                        candidate_tags.append(tag)
        derivation_hints = [
            hint
            for num in _extract_numbers(s["text"])
            if any(n["value"] == num["value"] and n["status"] in ("ungrounded", "uncited") for n in s["numbers"])
            for hint in [_derivation_hint(num, evidence, default_ticker)]
            if hint
        ]
        details.append(
            {
                "sentence": s["text"],
                "flagged_numbers": [n["value"] for n in s["numbers"] if n["status"] in ("ungrounded", "uncited")],
                "derivation_hints": derivation_hints,
                "semantic_verdict": s.get("semantic_verdict"),
                "reason": s.get("reason", ""),
                "candidate_tags": candidate_tags,
                "cited_chunks": [
                    f"{_block_label(chunk_by_id[cid], default_ticker)}:\n{chunk_by_id[cid]['content']}"
                    for cid in s["chunk_ids"]
                    if cid in chunk_by_id
                ],
            }
        )
    return details


def repair_node(state: AdaptiveRAGState) -> Dict[str, Any]:
    """
    LangGraph Node: Surgically repair flagged numbers, unverified sentences and invalid citations
    in `draft_answer` using the guardrail report.
    """
    draft = state.get("draft_answer") or state.get("final_answer") or ""
    report = state.get("guardrail_report", {})
    ungrounded = report.get("ungrounded_numbers", [])
    invalid_citations = report.get("invalid_citations", [])
    evidence = state.get("accumulated_evidence", [])
    repair_count = state.get("repair_count", 0)
    default_ticker = state.get("target_ticker") or "NVDA"

    context_blocks = [f"Block {_block_label(ch, default_ticker)}:\n{ch['content']}" for ch in evidence]
    context_str = "\n\n---\n\n".join(context_blocks) if context_blocks else "No evidence available."

    sentence_details = _unverified_sentence_details(report, evidence, default_ticker)
    if sentence_details:
        sentence_str = "\n\n".join(
            f"Sentence {i}: {d['sentence']}\n"
            f"  Flagged numbers: {d['flagged_numbers'] or 'none'}\n"
            f"  Semantic verdict: {d['semantic_verdict'] or 'n/a'} {('- ' + d['reason']) if d['reason'] else ''}\n"
            f"  Cited evidence:\n"
            + (
                "\n".join(d["cited_chunks"])
                if d["cited_chunks"]
                else "  (no valid citation) -> add the exact tag of the Evidence Block that contains it, or remove the sentence"
            )
            + (f"\n  Evidence blocks containing its figures: {' '.join(d['candidate_tags'])}" if d["candidate_tags"] else "")
            + "".join(f"\n  Computed figure: {hint}" for hint in d["derivation_hints"])
            for i, d in enumerate(sentence_details, start=1)
        )
    else:
        sentence_str = "None"

    user_prompt = (
        f"Original Query: {state['original_query']}\n\n"
        f"Flagged Ungrounded Numbers to Repair or Excise: {ungrounded}\n\n"
        f"Invalid Citation Tags to Remove or Correct: {invalid_citations or 'None'}\n\n"
        f"Unverified Sentences (fix from their cited evidence or remove):\n{sentence_str}\n\n"
        f"Draft Answer to Correct:\n{draft}\n\n"
        f"Verified Evidence Blocks:\n{context_str}"
    )

    repaired_text, updated_telemetry = call_llm(
        state=state,
        node_name="repair",
        messages=[
            {"role": "system", "content": REPAIR_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
    )

    history = list(state.get("repair_history", []))
    history.append(
        {
            "repair_iteration": repair_count + 1,
            "flagged_numbers": ungrounded,
            "unverified_sentences": [d["sentence"] for d in sentence_details],
            "invalid_citations": invalid_citations,
            "original_draft": draft,
            "repaired_draft": repaired_text,
        }
    )

    return {
        "draft_answer": repaired_text,
        "final_answer": repaired_text,
        "citations": build_citation_records(repaired_text, evidence),
        "repair_count": repair_count + 1,
        "repair_history": history,
        "telemetry": updated_telemetry,
    }
