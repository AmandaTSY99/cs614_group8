"""
Live query execution for the demo. Every system returns the same "run" dict the citation renderer reads:
    answer, citations, contexts [{chunk_id, ticker, fiscal_year, section, text}], guardrail,
    hops, latency_ms, tokens, cost_usd, plus `trace` (System C hop-by-hop log).

System C is streamed node by node through its LangGraph so the diagram can light up as it runs.
Systems A and B reuse the RQ2 evaluation adapters, so live answers are produced exactly as in the benchmark.
"""

import hashlib
import os
import re
import threading
import time
from contextlib import contextmanager
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple

C_MODES = {"system_c_v1": "v1_amr", "system_c_v2": "v2_aamr", "system_c_v3": "v3_aamr_sg"}

# Order = preference when the visitor brings no key: the Space's own secrets are used in this order.
PROVIDERS = {
    "openai": {"label": "OpenAI", "keys": ["OPENAI_API_KEY"], "models": ["gpt-5.4", "gpt-4o-mini"]},
    "groq": {"label": "Groq", "keys": ["GROQ_API_KEY"], "models": ["openai/gpt-oss-120b", "llama-3.3-70b-versatile"]},
    "gemini": {"label": "Google Gemini", "keys": ["GEMINI_API_KEY", "GOOGLE_API_KEY"], "models": ["gemini-3-flash-preview"]},
}

# The LLM layers read provider, model and key from os.environ, which every visitor of the Space shares.
# `llm_session` sets them only for the duration of a run and restores the Space's own values afterwards, so a
# visitor's pasted key is never reused for anyone else. Runs with identical settings may overlap; a run with
# different settings waits until the others finish.
_ENV_NAMES = ("LLM_PROVIDER", "LLM_MODEL", "SYSTEM_B_MODEL", *{k for p in PROVIDERS.values() for k in p["keys"]})
_BASELINE = {k: os.environ.get(k) for k in _ENV_NAMES}
_session_cond = threading.Condition()
_session_state: Dict[str, Any] = {"signature": None, "active": 0}

COMPANY_ALIASES = {
    "AAPL": ["apple"], "AMZN": ["amazon"], "GOOGL": ["alphabet", "google"], "JNJ": ["johnson & johnson", "johnson and johnson", "j&j"],
    "JPM": ["jpmorgan", "jp morgan", "chase"], "META": ["meta", "facebook"], "MSFT": ["microsoft"], "NVDA": ["nvidia"],
    "TSLA": ["tesla"], "WMT": ["walmart", "wal-mart"],
}
YEAR_RE = re.compile(r"\b(?:FY\s?)?(20[1-2]\d)\b", re.IGNORECASE)


def space_has_key(provider: str) -> bool:
    """True when the Space (secrets or .env) holds a key for this provider."""
    return any(_BASELINE.get(k) for k in PROVIDERS[provider]["keys"])


def space_providers() -> List[str]:
    return [p for p in PROVIDERS if space_has_key(p)]


def _restore_baseline() -> None:
    for name, value in _BASELINE.items():
        if value is None:
            os.environ.pop(name, None)
        else:
            os.environ[name] = value


@contextmanager
def llm_session(provider: str, model: str, api_key: str = "") -> Iterator[None]:
    """Point the LLM layers at `provider`/`model` (and the visitor's own key, if given) for one run."""
    key = api_key.strip()
    env = {"LLM_PROVIDER": provider, "LLM_MODEL": model, "SYSTEM_B_MODEL": model}
    if key:
        env.update({name: key for name in PROVIDERS[provider]["keys"]})
    signature = (provider, model, hashlib.sha256(key.encode()).hexdigest() if key else None)
    with _session_cond:
        while _session_state["active"] and _session_state["signature"] != signature:
            _session_cond.wait()
        if not _session_state["active"]:
            _restore_baseline()
            os.environ.update(env)
            _session_state["signature"] = signature
        _session_state["active"] += 1
    try:
        yield
    finally:
        with _session_cond:
            _session_state["active"] -= 1
            if not _session_state["active"]:
                _restore_baseline()
                _session_state["signature"] = None
                _session_cond.notify_all()


def database_ready() -> bool:
    return bool(os.getenv("SUPABASE_DB_URL") or os.getenv("SUPABASE_DB_HOST"))


def detect_scope(question: str) -> Tuple[List[str], List[int]]:
    """Tickers and fiscal years named in a question (used to scope the single-pass systems)."""
    q = question.lower()
    tickers = [t for t, names in COMPANY_ALIASES.items()
               if any(re.search(rf"\b{re.escape(n)}\b", q) for n in names) or re.search(rf"\b{t.lower()}\b", q)]
    years = sorted({int(y) for y in YEAR_RE.findall(question)})
    return tickers, years


def _contexts_from_evidence(evidence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for ch in evidence:
        meta = ch.get("metadata") or {}
        cid = str(ch.get("chunk_id", ""))
        xbrl = re.match(r"^F-([A-Z]{1,6})-(\d{4})$", cid)
        out.append({
            "chunk_id": cid,
            "ticker": meta.get("ticker") or (xbrl.group(1) if xbrl else None),
            "fiscal_year": meta.get("fiscal_year") or (int(xbrl.group(2)) if xbrl else None),
            "section": meta.get("section") or ("financials.csv" if xbrl else None),
            "text": str(ch.get("content", "")),
            "hop": ch.get("hop_retrieved"),
        })
    return out


def run_system_c(
    question: str,
    system: str,
    max_hops: int = 3,
    on_step: Optional[Callable[[str, Optional[str], List[str], Dict[str, Any]], None]] = None,
    scope: Optional[Tuple[List[str], List[int]]] = None,
) -> Dict[str, Any]:
    """Stream System C's graph; `on_step(node, next_node, visited, state)` fires after every node."""
    from src.system_c.graph import build_system_c_graph
    from src.system_c.state import create_initial_state
    from src.system_c.telemetry import summarize_rq3_metrics

    tickers, years = scope or ([], [])
    state = dict(create_initial_state(
        query=question, max_hops=max_hops, mode=C_MODES[system],
        target_ticker=tickers[0] if len(tickers) == 1 else None, target_tickers=tickers or None,
        fiscal_years=years or None,
    ))
    graph = build_system_c_graph()
    visited: List[str] = []
    trace: List[Dict[str, Any]] = []
    t0 = time.perf_counter()

    for event in graph.stream(state):
        for node, update in event.items():
            if isinstance(update, dict):
                state.update(update)
            if node not in visited:
                visited.append(node)
            hop = int(state.get("current_hop", 1) or 1)
            nxt: Optional[str] = None
            if node == "decomposer":
                nxt = "tabular_tool" if state.get("mode") in ("v2_aamr", "v3_aamr_sg") and state.get("needs_tabular_tool") else "retriever"
                trace.append({"kind": "plan", "tickers": state.get("target_tickers") or [],
                              "years": state.get("fiscal_years") or state.get("target_fiscal_years") or [],
                              "xbrl": nxt == "tabular_tool"})
            elif node == "tabular_tool":
                nxt = "retriever"
                trace.append({"kind": "xbrl", "rows": len(state.get("tabular_evidence") or [])})
            elif node == "retriever":
                nxt = "critic"
                trace.append({"kind": "retrieve", "hop": hop, "query": state.get("current_sub_query") or question,
                              "total": len(state.get("accumulated_evidence") or [])})
            elif node == "critic":
                done = bool(state.get("is_sufficient")) or hop >= max_hops
                nxt = "synthesizer" if done else "generator"
                trace.append({"kind": "critic", "hop": hop, "score": float(state.get("sufficiency_score") or 0.0),
                              "sufficient": bool(state.get("is_sufficient")), "missing": list(state.get("missing_premises") or [])[:3],
                              "budget_hit": hop >= max_hops and not state.get("is_sufficient")})
            elif node == "generator":
                nxt = "retriever"
            elif node == "synthesizer":
                nxt = "guardrail"
            elif node == "guardrail":
                failed = not state.get("guardrail_passed", True)
                nxt = "repair" if failed and int(state.get("repair_count", 0) or 0) < int(state.get("max_repairs", 1) or 1) else None
                if nxt:
                    trace.append({"kind": "repair"})
            elif node == "repair":
                nxt = "guardrail"
            if on_step:
                on_step(node, nxt, visited, state)

    summary = summarize_rq3_metrics(state)
    evidence = state.get("accumulated_evidence") or []
    return {
        "answer": state.get("final_answer") or state.get("draft_answer") or "",
        "citations": [{k: c.get(k) for k in ("tag", "chunk_id", "ticker", "fiscal_year", "section")}
                      for c in state.get("citations") or []],
        "contexts": _contexts_from_evidence(evidence),
        "guardrail": state.get("guardrail_report") or None,
        "hops": int(state.get("current_hop", 1) or 1),
        "latency_ms": (time.perf_counter() - t0) * 1000.0,
        "tokens": int(summary.get("total_tokens", 0) or 0),
        "cost_usd": float(summary.get("estimated_cost_usd", 0.0) or 0.0),
        "trace": trace,
        "visited": visited,
    }


def run_single_pass(question: str, system: str, scope: Tuple[List[str], List[int]]) -> Dict[str, Any]:
    """System A or B through the same adapters used to produce the benchmark runs."""
    from scripts.rq2.adapters import SystemAAdapter, SystemBAdapter

    tickers, years = scope
    adapter = SystemAAdapter() if system == "system_a" else SystemBAdapter()
    rec = adapter.answer({"question": question, "target_tickers": tickers, "fiscal_years": years})
    return {
        "answer": rec["answer"],
        "citations": rec["citations"],
        "contexts": [{**meta, "text": text} for meta, text in zip(rec["contexts_meta"], rec["retrieved_contexts"])],
        "guardrail": None,
        "hops": 1,
        "latency_ms": rec["latency_ms"],
        "tokens": rec["tokens"].get("total", 0),
        "cost_usd": rec["cost_usd"],
        "trace": [],
        "visited": ["question", "retrieve", "rerank", "generate", "answer"] if system == "system_b"
        else ["question", "retrieve", "generate", "answer"],
    }
