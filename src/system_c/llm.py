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
import re
import time
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv

from src.system_c.telemetry import record_llm_call

load_dotenv(override=True)


def clean_and_parse_json(raw_text: str) -> Dict[str, Any]:
    """
    Robust JSON parser for LLM responses.
    Handles markdown code fences, trailing commas, and returns an empty dict on failure.
    """
    cleaned = raw_text.strip()
    fence_match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if fence_match:
        cleaned = fence_match.group(0)
    # Strip trailing commas before closing braces/brackets (common local LLM issue)
    cleaned = re.sub(r",\s*([\]}])", r"\1", cleaned)
    try:
        return json.loads(cleaned)
    except Exception:
        try:
            import ast
            parsed = ast.literal_eval(cleaned)
            return parsed if isinstance(parsed, dict) else {}
        except Exception:
            return {}


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
        # Detect all tickers and fiscal years from query
        found_tickers = []
        for t in ("AAPL", "AMZN", "GOOGL", "JNJ", "JPM", "META", "MSFT", "NVDA", "TSLA", "WMT"):
            pattern = rf"\b{t.lower()}\b"
            if re.search(pattern, query.lower()):
                found_tickers.append(t)
        for name, t in (
            ("apple", "AAPL"),
            ("microsoft", "MSFT"),
            ("amazon", "AMZN"),
            ("alphabet", "GOOGL"),
            ("google", "GOOGL"),
            ("meta", "META"),
            ("nvidia", "NVDA"),
            ("tesla", "TSLA"),
            ("jpmorgan", "JPM"),
            ("walmart", "WMT"),
        ):
            if name in query.lower() and t not in found_tickers:
                found_tickers.append(t)

        ticker = found_tickers[0] if found_tickers else "NVDA"
        years = [int(y) for y in ("2023", "2024", "2025", "2026") if y in query] or [2026]
        is_multi = len(found_tickers) > 1 or any(
            w in query.lower()
            for w in ("impact", "footnote", "covenant", "compare", "how did", "supply", "across", "concentration", "risk")
        )

        plans: List[Dict[str, Any]] = []
        if len(found_tickers) > 1:
            for tkr in found_tickers:
                y = years[0] if years else 2024
                is_quant = any(w in query.lower() for w in ("margin", "revenue", "income", "eps", "debt", "ratio", "table", "asset", "liability"))
                plans.append({
                    "query": f"{tkr} FY{y} revenue, operating margin, and reported financials",
                    "target_tool": "tabular_tool" if is_quant else "retriever",
                    "ticker": tkr,
                    "fiscal_year": y,
                })
                if any(w in query.lower() for w in ("risk", "supply", "chain", "footnote", "contingenc")):
                    plans.append({
                        "query": f"{tkr} FY{y} supply chain, risk factors, and footnote disclosures",
                        "target_tool": "retriever",
                        "ticker": tkr,
                        "fiscal_year": y,
                    })
        elif is_multi:
            plans = [
                {
                    "query": f"{ticker} FY{years[0]} primary business drivers and operational segment performance",
                    "target_tool": "retriever",
                    "ticker": ticker,
                    "fiscal_year": years[0],
                },
                {
                    "query": f"{ticker} FY{years[0]} financial statement footnotes, debt covenants, and quantitative breakdown",
                    "target_tool": "tabular_tool" if any(w in query.lower() for w in ("margin", "revenue", "income", "eps", "debt", "ratio", "table")) else "retriever",
                    "ticker": ticker,
                    "fiscal_year": years[0],
                },
            ]
        else:
            plans = [
                {
                    "query": query,
                    "target_tool": "tabular_tool" if any(w in query.lower() for w in ("margin", "revenue", "income", "eps", "debt", "ratio", "table")) else "retriever",
                    "ticker": ticker,
                    "fiscal_year": years[0],
                }
            ]

        resp_obj = {
            "target_ticker": ticker,
            "target_tickers": found_tickers or [ticker],
            "fiscal_years": years,
            "query_complexity": "multi_hop" if is_multi else "single_hop",
            "needs_tabular_tool": any(p.get("target_tool") == "tabular_tool" for p in plans),
            "sub_query_plans": plans,
            "sub_queries": [p["query"] for p in plans],
        }
        content = json.dumps(resp_obj)

    elif node_name == "critic":
        # Check for explicit mock score override in state telemetry
        explicit_score = state.get("telemetry", {}).get("mock_sufficiency_score")
        tabular = state.get("tabular_evidence", [])
        q_lower = query.lower()
        has_qual = any(w in q_lower for w in ("risk", "footnote", "impact", "legal", "covenant", "contingenc", "why", "driver", "strategy", "cause"))

        if state.get("force_max_hops"):
            target_hop = state.get("max_hops", 3)
            is_suff = hop >= target_hop
        elif explicit_score is not None:
            threshold = float(state.get("sufficiency_threshold", 0.85))
            is_suff = float(explicit_score) >= threshold
        elif tabular and not has_qual:
            is_suff = True
        else:
            target_hop = state.get("telemetry", {}).get("mock_sufficient_at_hop", 2)
            if state.get("query_complexity") == "single_hop":
                target_hop = 1
            is_suff = hop >= target_hop

        if explicit_score is not None:
            sufficiency_score = float(explicit_score)
        else:
            sufficiency_score = 0.95 if is_suff else 0.50

        missing_ent = [] if is_suff else [
            f"FY{(state.get('fiscal_years') or [2026])[0]} specific quantitative footnote line items"
        ]
        missing_yrs = [] if is_suff else [
            y for y in state.get("fiscal_years", [])
            if not any(str(y) in c["content"] for c in state.get("accumulated_evidence", []))
        ]
        missing_prem = [] if is_suff else [
            f"Specific quantitative footnote breakdown and risk factor disclosures for {state.get('target_ticker', 'NVDA')}"
        ]

        resp_obj = {
            "sufficiency_score": sufficiency_score,
            "is_sufficient": is_suff,
            "missing_entities": missing_ent,
            "missing_years": missing_yrs,
            "missing_premises": missing_prem,
            "critic_reasoning": (
                f"Hop {hop}: Quantitative sufficiency score {sufficiency_score:.2f} satisfies completeness criteria."
                if is_suff
                else f"Hop {hop}: Quantitative sufficiency score {sufficiency_score:.2f} indicates missing footnote or entity details."
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

    elif node_name == "repair":
        # In mock mode, repair excises ungrounded numbers to produce a 100% grounded answer
        draft = state.get("draft_answer") or ""
        ungrounded = state.get("guardrail_report", {}).get("ungrounded_numbers", [])
        repaired = draft
        for bad_num in ungrounded:
            repaired = repaired.replace(bad_num, "[figure not disclosed in filing]")
        content = repaired

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
