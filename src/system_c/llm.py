"""
Unified LLM Client & Automatic RQ3 Telemetry Wrapper for System C.

Supports:
1. `LLM_PROVIDER="ollama"` (Local zero-API-key execution via `qwen2.5:7b` / `llama3.1:8b` / `gemma2:9b`)
2. `LLM_PROVIDER="groq"`   (Team notebook default: `openai/gpt-oss-120b` or `llama-3.3-70b-versatile`)
3. `LLM_PROVIDER="openai"` (Cloud OpenAI: `gpt-4o-mini` / `gpt-4o`)
4. `LLM_PROVIDER="mock"`   (Deterministic instant responses for fast pytest & CI verification)

IMPORTANT FOR ARYAN & ANISH:
Always call `call_llm(state, node_name, messages)` instead of raw SDK calls so that RQ3
token consumption, latency, and cost metrics are automatically logged into `state["telemetry"]`.
"""

import json
import os
import time
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv

from src.system_c.telemetry import record_llm_call

load_dotenv()


def get_llm_config() -> Tuple[str, str]:
    """Return `(provider, model)` based on environment variables."""
    provider = os.getenv("LLM_PROVIDER", "ollama").strip().lower()
    model = os.getenv("LLM_MODEL", "").strip()
    if not model:
        if provider == "ollama":
            model = "qwen2.5:7b"
        elif provider == "groq":
            model = "openai/gpt-oss-120b"
        elif provider == "openai":
            model = "gpt-4o-mini"
        else:
            model = "mock"
    return provider, model


def _estimate_tokens(text: str) -> int:
    """Fallback token estimator (~1.3 tokens per word) when provider omits usage stats."""
    return max(1, int(len(text.split()) * 1.3))


def _call_ollama(
    model: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.0,
    json_mode: bool = False,
) -> Tuple[str, int, int]:
    """Call local Ollama HTTP API (`http://localhost:11434/api/chat`) without needing an API key."""
    base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature},
    }
    if json_mode:
        payload["format"] = "json"

    req = urllib.request.Request(
        f"{base_url}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    content = data.get("message", {}).get("content", "")
    prompt_tokens = data.get("prompt_eval_count") or _estimate_tokens(
        " ".join(m.get("content", "") for m in messages)
    )
    completion_tokens = data.get("eval_count") or _estimate_tokens(content)
    return content, int(prompt_tokens), int(completion_tokens)


def _call_groq_or_openai(
    provider: str,
    model: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.0,
    max_tokens: int = 1024,
) -> Tuple[str, int, int]:
    """Call Groq or OpenAI chat completions API (matches `build_vdb_base_RAG.ipynb` Cell 6)."""
    if provider == "groq":
        from groq import Groq
        client = Groq()
    else:
        from openai import OpenAI
        client = OpenAI()

    kwargs: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if "gpt-oss" in model:
        kwargs["reasoning_effort"] = "low"

    resp = client.chat.completions.create(**kwargs)
    content = resp.choices[0].message.content or ""
    usage = getattr(resp, "usage", None)
    prompt_tokens = getattr(usage, "prompt_tokens", None) or _estimate_tokens(
        " ".join(m.get("content", "") for m in messages)
    )
    completion_tokens = getattr(usage, "completion_tokens", None) or _estimate_tokens(content)
    return content, int(prompt_tokens), int(completion_tokens)


def _call_mock(
    node_name: str,
    messages: List[Dict[str, str]],
    state: Dict[str, Any],
) -> Tuple[str, int, int]:
    """Deterministic mock responder for fast unit tests and CI validation."""
    user_prompt = messages[-1].get("content", "") if messages else ""
    prompt_tokens = _estimate_tokens(" ".join(m.get("content", "") for m in messages))
    hop = state.get("current_hop", 1)
    query = state.get("original_query", "")

    if node_name == "decomposer":
        # Detect ticker and fiscal years from query
        ticker = "NVDA"
        for t in ("AAPL", "AMZN", "GOOGL", "JNJ", "JPM", "META", "MSFT", "NVDA", "TSLA", "WMT"):
            if t.lower() in query.lower():
                ticker = t
                break
        years = [int(y) for y in ("2024", "2025", "2026") if y in query] or [2026]
        is_multi = any(w in query.lower() for w in ("impact", "footnote", "covenant", "compare", "how did", "supply", "across", "concentration", "risk"))
        resp_obj = {
            "target_ticker": ticker,
            "fiscal_years": years,
            "query_complexity": "multi_hop" if is_multi else "single_hop",
            "needs_tabular_tool": any(w in query.lower() for w in ("margin", "revenue", "income", "eps", "debt", "ratio", "table")),
            "sub_queries": (
                [
                    f"{ticker} FY{years[0]} primary business drivers and operational segment performance",
                    f"{ticker} FY{years[0]} financial statement footnotes, debt covenants, and quantitative breakdown",
                ]
                if is_multi
                else [query]
            ),
        }
        content = json.dumps(resp_obj)

    elif node_name == "critic":
        # If query is single_hop or we reached hop >= 2 (or force_sufficient_at_hop in state), mark sufficient
        if state.get("force_max_hops"):
            target_hop = state.get("max_hops", 3)
        else:
            target_hop = state.get("telemetry", {}).get("mock_sufficient_at_hop", 2)
            if state.get("query_complexity") == "single_hop":
                target_hop = 1
        is_suff = hop >= target_hop
        resp_obj = {
            "is_sufficient": is_suff,
            "missing_premises": [] if is_suff else [
                "Specific quantitative footnote breakdown and risk factor disclosures referenced in Item 7"
            ],
            "critic_reasoning": (
                f"Hop {hop}: All required entities and quantitative figures are present in accumulated evidence."
                if is_suff
                else f"Hop {hop}: Retrieved initial MD&A context, but missing specific quantitative footnote disclosures."
            ),
        }
        content = json.dumps(resp_obj)

    elif node_name == "generator":
        missing = state.get("missing_premises", ["quantitative footnote details"])
        ticker = state.get("target_ticker") or "NVDA"
        years = state.get("fiscal_years") or [2026]
        content = json.dumps(
            {
                "follow_up_query": f"{ticker} FY{years[0]} Item 8 footnote table details for: {missing[0]}",
                "reasoning": f"Conditioned on Hop {hop} chunks to resolve missing premise.",
            }
        )

    elif node_name == "synthesizer":
        evidence = state.get("accumulated_evidence", [])
        tabular = state.get("tabular_evidence", [])
        cites = []
        cite_tags = []
        for ch in evidence[:2]:
            cid = ch["chunk_id"]
            sec = ch["metadata"].get("section", "Item 7")
            tkr = ch["metadata"].get("ticker", "NVDA")
            fy = ch["metadata"].get("fiscal_year", 2026)
            tag = f"[{tkr} FY{fy}, {sec}, {cid}]"
            cite_tags.append(tag)
            cites.append(
                {
                    "tag": tag,
                    "chunk_id": cid,
                    "ticker": tkr,
                    "fiscal_year": fy,
                    "section": sec,
                    "supported_claim": ch["content"][:120],
                }
            )
        if tabular:
            tag = f"[F-{state.get('target_ticker', 'NVDA')}-{(state.get('fiscal_years') or [2026])[0]}]"
            cite_tags.append(tag)
        tags_str = " ".join(cite_tags) if cite_tags else "[NVDA FY2026, Item 7]"
        content = (
            f"Based on the retrieved SEC 10-K disclosures, {state.get('target_ticker', 'NVDA')} reported strong "
            f"operational results alongside disclosed risk and footnote factors {tags_str}."
        )
    else:
        content = f"Mock response for {node_name}: {user_prompt[:80]}"

    completion_tokens = _estimate_tokens(content)
    return content, prompt_tokens, completion_tokens


def call_llm(
    state: Dict[str, Any],
    node_name: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.0,
    json_mode: bool = False,
) -> Tuple[str, Dict[str, Any]]:
    """
    Execute an LLM call using the configured provider and automatically record RQ3 telemetry.

    Returns:
        `(response_text, updated_telemetry_dict)`
    """
    provider, model = get_llm_config()
    hop = state.get("current_hop", 0)
    start = time.perf_counter()

    if provider == "mock":
        content, p_tok, c_tok = _call_mock(node_name, messages, state)
    elif provider == "ollama":
        content, p_tok, c_tok = _call_ollama(model, messages, temperature=temperature, json_mode=json_mode)
    elif provider in ("groq", "openai"):
        content, p_tok, c_tok = _call_groq_or_openai(provider, model, messages, temperature=temperature)
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER='{provider}'. Use 'ollama', 'groq', 'openai', or 'mock'.")

    latency_ms = (time.perf_counter() - start) * 1000.0
    updated_telemetry = record_llm_call(
        telemetry=state.get("telemetry", {}),
        node_name=node_name,
        model=model,
        provider=provider,
        prompt_tokens=p_tok,
        completion_tokens=c_tok,
        latency_ms=latency_ms,
        hop=hop,
    )
    return content, updated_telemetry
