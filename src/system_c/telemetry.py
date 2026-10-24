"""
RQ3 Inference Economics & Telemetry Module for System C.

Owned by: Anish (RQ3 Lead - Latency, Token Consumption, Monetary Cost & Pareto Frontier)
"""

import time
from contextlib import contextmanager
from typing import Any, Dict, List


# Standard pricing per 1M tokens (USD) for RQ3 cost estimation across providers
MODEL_PRICING_PER_1M: Dict[str, Dict[str, float]] = {
    # Cloud providers (used in team benchmarks)
    "openai/gpt-oss-120b": {"prompt": 0.15, "completion": 0.60},
    "llama-3.3-70b-versatile": {"prompt": 0.59, "completion": 0.79},
    "llama-3.1-8b-instant": {"prompt": 0.05, "completion": 0.08},
    "gpt-4o-mini": {"prompt": 0.15, "completion": 0.60},
    "gpt-4o": {"prompt": 2.50, "completion": 10.00},
    "gemini-1.5-flash": {"prompt": 0.075, "completion": 0.30},
    "gemini-2.0-flash": {"prompt": 0.10, "completion": 0.40},
    "command-r": {"prompt": 0.15, "completion": 0.60},
    "command-r-plus": {"prompt": 2.50, "completion": 10.00},
    # Local Ollama models (imputed cloud-equivalent 7B/8B cost for RQ3 Pareto comparison)
    "qwen2.5:7b": {"prompt": 0.10, "completion": 0.30},
    "llama3.1:8b": {"prompt": 0.10, "completion": 0.30},
    "gemma2:9b": {"prompt": 0.10, "completion": 0.30},
    "mock": {"prompt": 0.10, "completion": 0.30},
}


def compute_call_cost_usd(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Calculate USD cost for a single LLM invocation."""
    rates = MODEL_PRICING_PER_1M.get(model, {"prompt": 0.15, "completion": 0.60})
    cost = (prompt_tokens / 1_000_000.0) * rates["prompt"] + (
        completion_tokens / 1_000_000.0
    ) * rates["completion"]
    return round(cost, 8)


def record_llm_call(
    telemetry: Dict[str, Any],
    node_name: str,
    model: str,
    provider: str,
    prompt_tokens: int,
    completion_tokens: int,
    latency_ms: float,
    hop: int = 0,
) -> Dict[str, Any]:
    """
    Append an LLM call record to `state['telemetry']` and update running totals.
    Returns the mutated/updated telemetry dictionary.
    """
    t = dict(telemetry) if telemetry else {
        "calls": [],
        "node_latencies_ms": {},
        "total_prompt_tokens": 0,
        "total_completion_tokens": 0,
        "total_tokens": 0,
        "estimated_cost_usd": 0.0,
        "hop_count": 0,
        "early_stopped": False,
    }
    calls = list(t.get("calls", []))
    cost_usd = compute_call_cost_usd(model, prompt_tokens, completion_tokens)

    calls.append(
        {
            "node": node_name,
            "hop": hop,
            "provider": provider,
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "latency_ms": round(latency_ms, 2),
            "cost_usd": cost_usd,
        }
    )

    node_latencies = dict(t.get("node_latencies_ms", {}))
    node_latencies[node_name] = round(node_latencies.get(node_name, 0.0) + latency_ms, 2)

    t["calls"] = calls
    t["node_latencies_ms"] = node_latencies
    t["total_prompt_tokens"] = t.get("total_prompt_tokens", 0) + prompt_tokens
    t["total_completion_tokens"] = t.get("total_completion_tokens", 0) + completion_tokens
    t["total_tokens"] = t["total_prompt_tokens"] + t["total_completion_tokens"]
    t["estimated_cost_usd"] = round(t.get("estimated_cost_usd", 0.0) + cost_usd, 8)
    t["cost_per_1k_queries_usd"] = round(t["estimated_cost_usd"] * 1000.0, 4)
    return t


@contextmanager
def track_node_latency(telemetry: Dict[str, Any], node_name: str):
    """Context manager to record non-LLM node execution wall-clock time (e.g. retrieval/reranking)."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        node_latencies = dict(telemetry.get("node_latencies_ms", {}))
        node_latencies[node_name] = round(node_latencies.get(node_name, 0.0) + elapsed_ms, 2)
        telemetry["node_latencies_ms"] = node_latencies


def summarize_rq3_metrics(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate an executive RQ3 Inference Economics summary from a completed `AdaptiveRAGState`.
    Includes Hop Attribution (RQ1 bridge) and Cost/Latency breakdown.
    """
    telemetry = state.get("telemetry", {})
    evidence = state.get("accumulated_evidence", [])
    hop_chunks: Dict[int, List[str]] = {}
    for ch in evidence:
        h = ch.get("hop_retrieved", 1)
        hop_chunks.setdefault(h, []).append(ch.get("chunk_id", ""))

    total_latency_ms = sum(telemetry.get("node_latencies_ms", {}).values())
    current_hop = state.get("current_hop", 1)
    max_hops = state.get("max_hops", 3)

    return {
        "mode": state.get("mode", "v1_amr"),
        "hop_count": current_hop,
        "max_hops": max_hops,
        "early_stopped": current_hop < max_hops and bool(state.get("is_sufficient")),
        "total_latency_ms": round(total_latency_ms, 2),
        "total_prompt_tokens": telemetry.get("total_prompt_tokens", 0),
        "total_completion_tokens": telemetry.get("total_completion_tokens", 0),
        "total_tokens": telemetry.get("total_tokens", 0),
        "estimated_cost_usd": telemetry.get("estimated_cost_usd", 0.0),
        "cost_per_1k_queries_usd": round(telemetry.get("estimated_cost_usd", 0.0) * 1000.0, 4),
        "node_latencies_ms": telemetry.get("node_latencies_ms", {}),
        "hop_attribution_chunk_ids": hop_chunks,
    }
