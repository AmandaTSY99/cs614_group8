"""
System adapters for RQ2 Stage 1 (main `cs614` env).

Every adapter exposes `answer(question_record) -> dict` with exactly the keys in `ADAPTER_KEYS`:

    answer              final answer text (with the system's own citation tags, if any)
    retrieved_contexts  list of context texts, in the order the system produced them
    contexts_meta       one {chunk_id, ticker, fiscal_year, section} per context, same order
    citations           list of {tag, chunk_id, ticker, fiscal_year, section} ([] if the system has none)
    guardrail_report    dict, or None if the system has no guardrail
    hops                retrieval hops executed (1 for single-shot systems)
    tokens              {prompt, completion, total} for the whole answer
    cost_usd            estimated answer cost
    latency_ms          end-to-end latency
    model, provider     answer model and provider
"""

import re
import time
from typing import Any, Callable, Dict, List

ADAPTER_KEYS = (
    "answer", "retrieved_contexts", "contexts_meta", "citations", "guardrail_report", "hops", "tokens",
    "cost_usd", "latency_ms", "model", "provider",
)
XBRL_ID_RE = re.compile(r"^F-([A-Z]{1,6})(?:-(\d{4}))?$")


class SystemAdapter:
    name = "base"

    def answer(self, question: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError


class SystemCAdapter(SystemAdapter):
    """System C via `run_system_c` (`v1_amr` or `v2_aamr`), called exactly like `run_rq3_ablation.py`."""

    def __init__(self, mode: str, max_hops: int = 3):
        self.mode = mode
        self.max_hops = max_hops
        self.name = {"v1_amr": "system_c_v1", "v2_aamr": "system_c_v2"}.get(mode, f"system_c_{mode}")

    def answer(self, question: Dict[str, Any]) -> Dict[str, Any]:
        from src.system_c.graph import run_system_c
        from src.system_c.llm import get_llm_config

        t0 = time.perf_counter()
        state = run_system_c(
            query=question["query"],
            max_hops=self.max_hops,
            mode=self.mode,
            target_ticker=question.get("ticker"),
            fiscal_years=question.get("fiscal_years") or question.get("years"),
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        summary = state.get("telemetry", {}).get("rq3_summary", {})
        provider, model = get_llm_config()

        # `accumulated_evidence` is already in retrieval order across hops, and in v2 it also holds the
        # XBRL `F-<TICKER>-<YEAR>` blocks the tabular tool added before Hop 1.
        evidence = state.get("accumulated_evidence", [])
        return {
            "answer": state.get("final_answer") or state.get("draft_answer") or "",
            "retrieved_contexts": [str(c.get("content", "")) for c in evidence],
            "contexts_meta": [_chunk_meta(c) for c in evidence],
            "citations": [
                {k: c.get(k) for k in ("tag", "chunk_id", "ticker", "fiscal_year", "section")}
                for c in state.get("citations", [])
            ],
            "guardrail_report": state.get("guardrail_report") or None,
            "hops": state.get("current_hop", 1),
            "tokens": {
                "prompt": summary.get("total_prompt_tokens", 0),
                "completion": summary.get("total_completion_tokens", 0),
                "total": summary.get("total_tokens", 0),
            },
            "cost_usd": summary.get("estimated_cost_usd", 0.0),
            "latency_ms": round(summary.get("total_latency_ms") or elapsed_ms, 1),
            "model": model,
            "provider": provider,
        }


def _chunk_meta(chunk: Dict[str, Any]) -> Dict[str, Any]:
    meta = chunk.get("metadata") or {}
    cid = str(chunk.get("chunk_id", ""))
    xbrl = XBRL_ID_RE.match(cid)
    return {
        "chunk_id": cid,
        "ticker": meta.get("ticker") or (xbrl.group(1) if xbrl else None),
        "fiscal_year": meta.get("fiscal_year") or (int(xbrl.group(2)) if xbrl and xbrl.group(2) else None),
        "section": meta.get("section") or ("financials.csv" if xbrl else None),
    }


class SystemAAdapter(SystemAdapter):
    """
    System A (vanilla RAG) — TO BE IMPLEMENTED by its owner.

    `answer(question)` receives one golden-set record (`id`, `query`, `ticker`, `fiscal_years`, ...) and must
    return a dict with exactly `ADAPTER_KEYS` (see the module docstring). Use gpt-4o-mini as the answer model.
    `retrieved_contexts` must be the chunk texts actually given to the LLM, in retrieval order. If the system
    produces no citations, return `citations: []` (citation P/R/F1 are then reported as N/A, never 0) and
    `guardrail_report: None`.
    """

    name = "system_a"

    def answer(self, question: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("system_a adapter not implemented yet; see SystemAAdapter docstring")


class SystemBAdapter(SystemAdapter):
    """
    System B (advanced RAG) — TO BE IMPLEMENTED by its owner.

    Same contract as `SystemAAdapter`: return exactly `ADAPTER_KEYS`, contexts in the order the system
    produced them (after reranking, if that is what the LLM saw), `citations: []` if it has none, and
    `guardrail_report: None` unless it has a guardrail with `numerical_grounding_error_rate`.
    """

    name = "system_b"

    def answer(self, question: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("system_b adapter not implemented yet; see SystemBAdapter docstring")


REGISTRY: Dict[str, Callable[[], SystemAdapter]] = {
    "system_c_v1": lambda: SystemCAdapter("v1_amr"),
    "system_c_v2": lambda: SystemCAdapter("v2_aamr"),
    "system_a": SystemAAdapter,
    "system_b": SystemBAdapter,
}


def get_adapters(names: List[str]) -> Dict[str, SystemAdapter]:
    unknown = [n for n in names if n not in REGISTRY]
    if unknown:
        raise ValueError(f"Unknown systems {unknown}; known: {sorted(REGISTRY)}")
    return {n: REGISTRY[n]() for n in names}
