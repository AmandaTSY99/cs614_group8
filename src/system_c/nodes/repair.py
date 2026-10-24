"""
Active Hallucination Repair & Self-Correction Node for System C.

Owned by: Anish (System Architect & Orchestration Lead)

Responsibilities:
1. Triggered when `guardrail_passed == False` and `repair_count < max_repairs`.
2. Inspects `guardrail_report["ungrounded_numbers"]` alongside `accumulated_evidence`.
3. Prompts the LLM with surgical instructions to excise hallucinated numbers or replace
   them strictly with verified ground-truth figures from the retrieved 10-K evidence blocks.
4. Updates `draft_answer`, logs `repair_history`, and loops back to `guardrail_node` for re-audit.
"""

from typing import Any, Dict, List

from src.system_c.llm import call_llm
from src.system_c.state import AdaptiveRAGState

REPAIR_SYSTEM_PROMPT = """You are a Precision Financial Fact-Auditor & Hallucination Repair Specialist for SEC 10-K filings.
You are given a Draft Financial Answer that failed numerical grounding verification because it contained specific ungrounded or hallucinated numbers.

Your task is to revise the answer:
1. For each flagged ungrounded number, check the provided Evidence Blocks. If the correct figure exists in the evidence, replace the ungrounded figure with the exact verified ground-truth figure from the context.
2. If a flagged number is completely absent from the Evidence Blocks, either excise the ungrounded sentence or explicitly state that the figure is not disclosed in the filing.
3. Preserve all valid inline citation tags (e.g. `[NVDA FY2026, Item 7, NVDA_FY2026_2026-01-25:42]` or `[F-NVDA-2026]`).
4. Output ONLY the revised, fully grounded answer text."""


def repair_node(state: AdaptiveRAGState) -> Dict[str, Any]:
    """
    LangGraph Node: Surgically repair numerical hallucinations in `draft_answer`
    using the ungrounded numbers flagged by `guardrail_node`.
    """
    draft = state.get("draft_answer") or state.get("final_answer") or ""
    ungrounded = state.get("guardrail_report", {}).get("ungrounded_numbers", [])
    evidence = state.get("accumulated_evidence", [])
    repair_count = state.get("repair_count", 0)

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
            context_blocks.append(f"Block [{tkr} FY{fy}, {sec}, {cid}]:\n{ch['content']}")

    context_str = "\n\n---\n\n".join(context_blocks) if context_blocks else "No evidence available."

    user_prompt = (
        f"Original Query: {state['original_query']}\n\n"
        f"Flagged Ungrounded Numbers to Repair or Excise: {ungrounded}\n\n"
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
            "original_draft": draft,
            "repaired_draft": repaired_text,
        }
    )

    return {
        "draft_answer": repaired_text,
        "final_answer": repaired_text,
        "repair_count": repair_count + 1,
        "repair_history": history,
        "telemetry": updated_telemetry,
    }
