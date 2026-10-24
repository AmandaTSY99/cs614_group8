"""
Answer Synthesizer & Inline Table Citation Mapper Node for System C.

Owned by: Aryan (Citations, Guardrails & RQ2 Lead)
Integration Contract:
- Reads `original_query`, `accumulated_evidence`, and `tabular_evidence` from `AdaptiveRAGState`.
- Synthesizes a comprehensive financial answer where every factual claim or number includes an inline
  citation tag (`[<TICKER> FY<YEAR>, <SECTION>, <CHUNK_ID>]` or `[F-<TICKER>-<YEAR>]`).
- Populates `draft_answer`, `final_answer`, and structured `citations` list (`List[CitationRecord]`).
- Uses `call_llm(state, "synthesizer", messages)` so RQ3 telemetry is captured automatically.
"""

import re
from typing import Any, Dict, List

from src.system_c.llm import call_llm
from src.system_c.state import AdaptiveRAGState, CitationRecord

SYNTHESIZER_SYSTEM_PROMPT = """You are a Senior SEC 10-K Financial Analyst.
Answer the user's question ONLY using the provided Evidence Blocks.
STRICT CITATION RULE:
1. Every factual assertion, percentage, or dollar figure MUST be followed by an inline citation tag referencing the exact chunk ID or XBRL block, e.g.:
   - `[NVDA FY2026, Item 7, NVDA_FY2026_2026-01-25:42]` for 10-K text/table chunks
   - `[F-NVDA-2026]` for SEC XBRL reported financials blocks
2. Never invent or extrapolate numbers not explicitly present in the context.
3. If a specific figure is unavailable in the context, state that clearly."""


def extract_citations_from_answer(
    answer_text: str,
    evidence: List[Dict[str, Any]],
) -> List[CitationRecord]:
    """
    Map inline `[...]` citation tags in `answer_text` back to exact `EvidenceChunk` records
    for RQ2 Citation Precision / Recall / F1 evaluation.
    """
    chunk_lookup = {c["chunk_id"]: c for c in evidence}
    citations: List[CitationRecord] = []
    seen_chunk_ids = set()

    # Match bracketed tags `[...]`
    for match in re.finditer(r"\[([^\[\]]+)\]", answer_text):
        tag_full = match.group(0)
        tag_inner = match.group(1)

        matched_chunk = None
        for cid, ch in chunk_lookup.items():
            if cid in tag_inner or tag_inner == cid:
                matched_chunk = ch
                break

        if matched_chunk is None and evidence:
            # Check section or ticker match
            for ch in evidence:
                sec = str(ch["metadata"].get("section", ""))
                if sec and sec[:15].lower() in tag_inner.lower():
                    matched_chunk = ch
                    break

        if matched_chunk and matched_chunk["chunk_id"] not in seen_chunk_ids:
            seen_chunk_ids.add(matched_chunk["chunk_id"])
            citations.append(
                CitationRecord(
                    tag=tag_full,
                    chunk_id=matched_chunk["chunk_id"],
                    ticker=str(matched_chunk["metadata"].get("ticker", "UNKNOWN")),
                    fiscal_year=matched_chunk["metadata"].get("fiscal_year", "N/A"),
                    section=str(matched_chunk["metadata"].get("section", "N/A")),
                    supported_claim=matched_chunk["content"][:160],
                )
            )
    return citations


def synthesizer_node(state: AdaptiveRAGState) -> Dict[str, Any]:
    """
    LangGraph Node (Aryan's Module):
    Synthesizes the final citation-grounded response from `accumulated_evidence`.
    """
    evidence = state.get("accumulated_evidence", [])
    context_blocks = []
    for ch in evidence:
        cid = ch["chunk_id"]
        meta = ch.get("metadata", {})
        tkr = meta.get("ticker", state.get("target_ticker") or "NVDA")
        fy = meta.get("fiscal_year", "N/A")
        sec = meta.get("section", "10-K")
        if str(cid).startswith("F-"):
            context_blocks.append(f"Block [{cid}]:\n{ch['content']}")
        else:
            context_blocks.append(
                f"Block [{tkr} FY{fy}, {sec}, {cid}]:\n{ch['content']}"
            )

    context_str = "\n\n---\n\n".join(context_blocks) if context_blocks else "No evidence retrieved."
    user_prompt = f"Evidence Blocks:\n{context_str}\n\nQuestion: {state['original_query']}"

    answer_text, updated_telemetry = call_llm(
        state=state,
        node_name="synthesizer",
        messages=[
            {"role": "system", "content": SYNTHESIZER_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
    )

    citations = extract_citations_from_answer(answer_text, evidence)

    return {
        "draft_answer": answer_text,
        "final_answer": answer_text,
        "citations": citations,
        "telemetry": updated_telemetry,
    }
