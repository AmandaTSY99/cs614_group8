"""
Answer Synthesizer & Inline Table Citation Mapper Node for System C.

Supports Research Question 2 (Factual Faithfulness & Citation Grounding):
- Reads `original_query`, `accumulated_evidence`, and `tabular_evidence` from `AdaptiveRAGState`.
- Labels each evidence block in prompt context and enforces bracketed citation tags on factual claims.
- Expands citation labels to standardized citation tags (`[<TICKER> FY<YEAR>, <SECTION>, <CHUNK_ID>]` or `[F-<TICKER>-<YEAR>]`).
- Populates `draft_answer`, `final_answer`, and structured `citations` (`List[CitationRecord]`).
- Captures generation token and latency telemetry for RQ3 economics.
"""

from typing import Any, Dict, List, Tuple

from src.system_c.guardrails.citations import build_citation_records, expand_labels
from src.system_c.llm import call_llm
from src.system_c.state import AdaptiveRAGState, CitationRecord

SYNTHESIZER_SYSTEM_PROMPT = """You are a Senior SEC 10-K Financial Analyst.
Answer the user's question using ONLY the Evidence Blocks provided. Each block starts with a label such as [E1], followed by the company ticker, fiscal year, filing section and chunk id.

CITATION RULES (strict):
1. End EVERY factual sentence with the label(s) of the block(s) that contain that fact, e.g. "Revenue was $215.9 billion [E2]."
2. If a sentence combines facts from several blocks (for example FY2025 vs FY2026 figures), cite all of them: [E1][E3] or [E1, E3].
3. Use only labels that appear in the Evidence Blocks. Never invent a label, chunk id or tag.
4. Write labels exactly as shown, in square brackets. Never put backticks or quotes around them.
5. Never invent, estimate or extrapolate a figure. Copy numbers exactly as they appear in the evidence, keeping the units the evidence uses.
6. If the evidence does not cover part of the question, write one sentence saying the filing does not disclose it. That sentence needs no label.
7. Do not add a sources list, footnotes or headings; citations go inline at the end of each sentence.
8. Cite the block where that specific fact is stated, not a nearby block on the same topic. If you can't point to the block that states it, don't make the claim.
9. A figure you compute yourself (a difference, ratio or growth rate) must cite every block its inputs come from."""


def extract_citations_from_answer(
    answer_text: str,
    evidence: List[Dict[str, Any]],
) -> List[CitationRecord]:
    """
    Map inline `[...]` citation tags in `answer_text` back to exact `EvidenceChunk` records
    for RQ2 Citation Precision / Recall / F1 evaluation: one record per (sentence, chunk) pair,
    strict resolver only (no section-name fallback).
    """
    return build_citation_records(answer_text, evidence)


def _build_evidence_blocks(
    evidence: List[Dict[str, Any]],
    default_ticker: str,
) -> Tuple[str, Dict[str, Dict[str, Any]]]:
    """Label each evidence chunk `[E<n>]` with a descriptive header; return `(context_str, label_map)`."""
    blocks = []
    label_map: Dict[str, Dict[str, Any]] = {}
    for n, ch in enumerate(evidence, start=1):
        label = f"E{n}"
        label_map[label] = ch
        cid = str(ch["chunk_id"])
        meta = ch.get("metadata", {}) or {}
        tkr = meta.get("ticker", default_ticker)
        fy = meta.get("fiscal_year", "N/A")
        if cid.startswith("F-"):
            header = f"[{label}] {tkr} FY{fy} | SEC XBRL reported financials | {cid}"
        else:
            header = f"[{label}] {tkr} FY{fy} | {meta.get('section', '10-K')} | {cid}"
        blocks.append(f"{header}\n{ch['content']}")
    context_str = "\n\n---\n\n".join(blocks) if blocks else "No evidence retrieved."
    return context_str, label_map


def synthesizer_node(state: AdaptiveRAGState) -> Dict[str, Any]:
    """
    LangGraph Node:
    Synthesizes the final citation-grounded response from `accumulated_evidence`.
    """
    evidence = state.get("accumulated_evidence", [])
    default_ticker = state.get("target_ticker") or "NVDA"
    context_str, label_map = _build_evidence_blocks(evidence, default_ticker)
    user_prompt = f"Evidence Blocks:\n{context_str}\n\nQuestion: {state['original_query']}"

    raw_answer, updated_telemetry = call_llm(
        state=state,
        node_name="synthesizer",
        messages=[
            {"role": "system", "content": SYNTHESIZER_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
    )

    # Unknown labels stay in the text so the guardrail reports them as invalid citations
    answer_text, _unknown_labels = expand_labels(raw_answer, label_map, default_ticker)
    citations = extract_citations_from_answer(answer_text, evidence)

    return {
        "draft_answer": answer_text,
        "final_answer": answer_text,
        "citations": citations,
        "telemetry": updated_telemetry,
    }
