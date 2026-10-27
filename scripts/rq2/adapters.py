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
    "cost_usd", "latency_ms", "stage_timings_ms", "model", "provider",
)
XBRL_ID_RE = re.compile(r"^F-([A-Z]{1,6})(?:-(\d{4}))?$")


class SystemAdapter:
    name = "base"

    def answer(self, question: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError


class SystemCAdapter(SystemAdapter):
    """System C via `run_system_c` (`v1_amr` or `v2_aamr`), called exactly like `run_rq3_ablation.py`."""

    def __init__(self, mode: str, max_hops: int = 3, force_max_hops: bool = False):
        self.mode = mode
        self.max_hops = max_hops
        self.force_max_hops = force_max_hops
        if force_max_hops:
            self.name = f"system_c_{mode}_fixed_3hop"
        else:
            self.name = {"v1_amr": "system_c_v1", "v2_aamr": "system_c_v2"}.get(mode, f"system_c_{mode}")

    def answer(self, question: Dict[str, Any]) -> Dict[str, Any]:
        from src.system_c.graph import run_system_c
        from src.system_c.llm import get_llm_config

        t0 = time.perf_counter()
        query_text = question.get("query") or question.get("question") or ""
        tickers = question.get("target_tickers") or ([question["ticker"]] if question.get("ticker") else None)
        years = question.get("fiscal_years") or ([int(question["year"])] if question.get("year") else None)

        state = run_system_c(
            query=query_text,
            max_hops=self.max_hops,
            mode=self.mode,
            target_ticker=question.get("ticker") or (tickers[0] if tickers else None),
            target_tickers=tickers,
            fiscal_years=years,
            force_max_hops=self.force_max_hops,
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
            "stage_timings_ms": {
                "retrieval_ms": round(summary.get("retrieval_latency_ms", 0.0), 1),
                "agent_critic_ms": round(summary.get("critic_latency_ms", 0.0), 1),
                "synthesis_ms": round(summary.get("synthesizer_latency_ms", 0.0), 1),
            },
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
    """System A (vanilla RAG): dense retrieval over Supabase sec_chunks + single LLM call."""

    name = "system_a"

    def __init__(self, variant: str = "rag5", top_k: int = 10):
        self.variant = variant
        self.top_k = top_k
        self._index = None

    def _get_index(self):
        if self._index is not None:
            return self._index
        import os
        from src.system_a.retrieval import ChromaIndex, SupabaseIndex
        if os.getenv("LLM_PROVIDER") == "mock":
            class _MockIndex:
                name = "mock_index"
                def retrieve(self, query, k=5, pairs=None):
                    ticker = (pairs[0][0] if pairs and pairs[0] else "NVDA")
                    year = (pairs[0][1] if pairs and len(pairs[0]) > 1 and pairs[0][1] else 2026)
                    return [{
                        "id": f"{ticker}_FY{year}_MOCK:1",
                        "score": 0.95,
                        "text": f"{ticker} Form 10-K fiscal {year} sample evidence chunk for {query}.",
                        "meta": {"ticker": ticker, "fiscal_year": year, "section": "Item 7", "doc_id": f"{ticker}_FY{year}"}
                    }]
            self._index = _MockIndex()
            return self._index

        supabase_url = os.getenv("SUPABASE_DB_URL")
        if supabase_url:
            try:
                self._index = SupabaseIndex(table="sec_chunks")
                return self._index
            except Exception:
                pass
        self._index = ChromaIndex(collection="rag5_structure_header_bge")
        return self._index

    def answer(self, question: Dict[str, Any]) -> Dict[str, Any]:
        from src.system_a.pipeline import generate
        from src.system_a.llm import get_last_telemetry
        t0 = time.perf_counter()
        query_text = question.get("query") or question.get("question") or ""
        tickers = question.get("target_tickers") or ([question["ticker"]] if question.get("ticker") else ["NVDA"])
        years = question.get("fiscal_years") or ([int(question["year"])] if question.get("year") else [2026])
        pairs = [(t, y) for t in tickers for y in years] if tickers and years else []

        index = self._get_index()
        t_ret0 = time.perf_counter()
        hits = index.retrieve(query_text, k=self.top_k, pairs=pairs)
        ret_ms = (time.perf_counter() - t_ret0) * 1000.0

        t_gen0 = time.perf_counter()
        gen_out = generate(query_text, hits, variant=self.variant, pairs=pairs)
        gen_ms = (time.perf_counter() - t_gen0) * 1000.0
        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        telemetry = get_last_telemetry()
        # Parse simple [n] citations from answer text
        citations = []
        for n, h in enumerate(hits, 1):
            if f"[{n}]" in gen_out["answer"]:
                citations.append({
                    "tag": f"[{n}]",
                    "chunk_id": h["id"],
                    "ticker": h["meta"].get("ticker"),
                    "fiscal_year": h["meta"].get("fiscal_year"),
                    "section": h["meta"].get("section"),
                })

        contexts_meta = [_chunk_meta({"chunk_id": h["id"], "metadata": h["meta"]}) for h in hits]
        prompt_tok = telemetry.get("prompt_tokens", 0)
        comp_tok = telemetry.get("completion_tokens", 0)
        cost_usd = (prompt_tok * 0.15 + comp_tok * 0.60) / 1_000_000.0

        return {
            "answer": gen_out["answer"],
            "retrieved_contexts": [h["text"] for h in hits],
            "contexts_meta": contexts_meta,
            "citations": citations,
            "guardrail_report": None,
            "hops": 1,
            "tokens": {
                "prompt": prompt_tok,
                "completion": comp_tok,
                "total": telemetry.get("total_tokens", prompt_tok + comp_tok),
            },
            "cost_usd": round(cost_usd, 6),
            "latency_ms": round(elapsed_ms, 1),
            "stage_timings_ms": {
                "retrieval_ms": round(ret_ms, 1),
                "generation_ms": round(gen_ms, 1),
            },
            "model": telemetry.get("model", "mock"),
            "provider": telemetry.get("provider", "mock"),
        }


class SystemBAdapter(SystemAdapter):
    """System B (hybrid BM25 + dense + cross-encoder rerank): single pass over Supabase sec_chunks."""

    name = "system_b"

    def __init__(self, mode: str = "hybrid_rerank", top_k: int = 5):
        self.mode = mode
        self.top_k = top_k
        self._source = None

    def _get_source(self):
        if self._source is not None:
            return self._source
        import os
        from src.system_b.adapters import ChromaSource, SupabaseSource
        if os.getenv("LLM_PROVIDER") == "mock":
            class _MockSource:
                def records(self, scope=None):
                    t = (scope.tickers[0] if scope and scope.tickers else "NVDA")
                    y = (scope.years[0] if scope and scope.years else 2026)
                    return [{
                        "id": f"{t}_FY{y}_MOCK:1",
                        "text": f"{t} fiscal {y} evidence text for query.",
                        "meta": {"ticker": t, "fiscal_year": y, "section": "Item 7"}
                    }]
                def __call__(self, query, scope, k):
                    t = (scope.tickers[0] if scope and scope.tickers else "NVDA")
                    y = (scope.years[0] if scope and scope.years else 2026)
                    return [(f"{t}_FY{y}_MOCK:1", 0.95)]
            self._source = _MockSource()
            return self._source

        supabase_url = os.getenv("SUPABASE_DB_URL")
        if supabase_url:
            try:
                self._source = SupabaseSource(table="sec_chunks")
                return self._source
            except Exception:
                pass
        self._source = ChromaSource()
        return self._source

    def answer(self, question: Dict[str, Any]) -> Dict[str, Any]:
        import os
        from src.system_b.pipeline import run
        from src.system_b.retrieval import Config, Retriever, Scope
        from src.system_b.adapters import Reranker
        t0 = time.perf_counter()
        query_text = question.get("query") or question.get("question") or ""
        tickers = question.get("target_tickers") or ([question["ticker"]] if question.get("ticker") else ["NVDA"])
        years = question.get("fiscal_years") or ([int(question["year"])] if question.get("year") else [2026])
        scope = Scope(tuple(t.upper() for t in tickers), tuple(years))

        source = self._get_source()
        records = source.records(scope) if hasattr(source, "records") and callable(getattr(source, "records")) else []
        if hasattr(source, "records") and not records:
            records = getattr(source, "records")()
        config = Config(alpha=0.5, candidates=30, rerank_candidates=30, top_k=self.top_k, mode=self.mode)
        reranker = Reranker() if os.getenv("LLM_PROVIDER") != "mock" else lambda q, txts: [0.9] * len(txts)
        retriever = Retriever(records, source, reranker, config)

        if os.getenv("LLM_PROVIDER") == "mock":
            generator = lambda msgs: {
                "answer": "System B mock answer citing [1].",
                "usage": {"prompt_tokens": 80, "completion_tokens": 30, "total_tokens": 110},
                "model": "mock",
                "rate_limit_retries": 0,
                "finish_reason": "stop",
            }
        elif os.getenv("LLM_PROVIDER") == "gemini":
            from src.system_c.llm import _call_gemini_native
            def _gemini_gen(msgs):
                content, p_tok, c_tok = _call_gemini_native("gemini-3-flash-preview", msgs, temperature=0.0)
                return {
                    "answer": content,
                    "usage": {"prompt_tokens": p_tok, "completion_tokens": c_tok, "total_tokens": p_tok + c_tok},
                    "model": "gemini-3-flash-preview",
                    "rate_limit_retries": 0,
                    "finish_reason": "stop",
                }
            generator = _gemini_gen
        elif os.getenv("LLM_PROVIDER") == "groq" or os.getenv("GROQ_API_KEY"):
            from src.system_c.llm import _call_groq_or_openai
            def _groq_gen(msgs):
                content, p_tok, c_tok = _call_groq_or_openai("groq", "openai/gpt-oss-120b", msgs, temperature=0.0)
                return {
                    "answer": content,
                    "usage": {"prompt_tokens": p_tok, "completion_tokens": c_tok, "total_tokens": p_tok + c_tok},
                    "model": "openai/gpt-oss-120b",
                    "rate_limit_retries": 0,
                    "finish_reason": "stop",
                }
            generator = _groq_gen
        else:
            from src.system_b.adapters import Generator
            generator = Generator(model=os.environ.get("SYSTEM_B_MODEL") or "openai/gpt-oss-120b",
                                  base_url=os.environ.get("SYSTEM_B_BASE_URL"))

        result = run(retriever, query_text, scope, generator)
        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        hits = result.get("hits", [])
        contexts_meta = [_chunk_meta({"chunk_id": h["id"], "metadata": h["meta"]}) for h in hits]
        citations = []
        c_dict = result.get("citations", {})
        hits_by_id = {h["id"]: h.get("meta", {}) for h in hits}
        if isinstance(c_dict, dict):
            for label, cid in c_dict.items():
                if f"[{label}]" in result.get("answer", "") or f"【{label}】" in result.get("answer", ""):
                    meta = hits_by_id.get(cid, {})
                    citations.append({
                        "tag": f"[{label}]",
                        "chunk_id": cid,
                        "ticker": meta.get("ticker"),
                        "fiscal_year": meta.get("fiscal_year"),
                        "section": meta.get("section"),
                    })
        elif isinstance(c_dict, list):
            for c in c_dict:
                cid = c.get("chunk_id", "") if isinstance(c, dict) else str(c)
                meta = hits_by_id.get(cid, {})
                citations.append({
                    "tag": c.get("label", "") if isinstance(c, dict) else "",
                    "chunk_id": cid,
                    "ticker": meta.get("ticker"),
                    "fiscal_year": meta.get("fiscal_year"),
                    "section": meta.get("section"),
                })

        usage = result.get("usage") or {}
        prompt_tok = usage.get("prompt_tokens", 0)
        comp_tok = usage.get("completion_tokens", 0)
        cost_usd = (prompt_tok * 0.15 + comp_tok * 0.60) / 1_000_000.0

        timings = result.get("timings", {})
        return {
            "answer": result.get("answer", ""),
            "retrieved_contexts": [h["text"] for h in hits],
            "contexts_meta": contexts_meta,
            "citations": citations,
            "guardrail_report": None,
            "hops": 1,
            "tokens": {
                "prompt": prompt_tok,
                "completion": comp_tok,
                "total": usage.get("total_tokens", prompt_tok + comp_tok),
            },
            "cost_usd": round(cost_usd, 6),
            "latency_ms": round(elapsed_ms, 1),
            "stage_timings_ms": {
                "retrieval_ms": round(timings.get("retrieval_seconds", 0.0) * 1000.0, 1),
                "rerank_ms": round(timings.get("rerank_seconds", 0.0) * 1000.0, 1),
                "generation_ms": round(timings.get("generation_seconds", 0.0) * 1000.0, 1),
            },
            "model": result.get("model", "mock"),
            "provider": os.environ.get("LLM_PROVIDER", "groq"),
        }


REGISTRY: Dict[str, Callable[[], SystemAdapter]] = {
    "system_c_v1": lambda: SystemCAdapter("v1_amr"),
    "system_c_v2": lambda: SystemCAdapter("v2_aamr"),
    "system_c_fixed_3hop": lambda: SystemCAdapter("v1_amr", force_max_hops=True),
    "system_a": SystemAAdapter,
    "system_b": SystemBAdapter,
}


def get_adapters(names: List[str]) -> Dict[str, SystemAdapter]:
    unknown = [n for n in names if n not in REGISTRY]
    if unknown:
        raise ValueError(f"Unknown systems {unknown}; known: {sorted(REGISTRY)}")
    return {n: REGISTRY[n]() for n in names}
