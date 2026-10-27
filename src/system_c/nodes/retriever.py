"""
Hybrid Retriever + Cross-Encoder Reranker Node for System C.

Owned by: Anish (System Architect & Orchestration Lead)

Supports:
1. Live Hybrid Retrieval (BM25 lexical + Dense embeddings + Cross-Encoder Reranking) over the 10-K filings in `data/`.
2. Plug-and-play connection to Amanda/Xavier's Chroma index (`chroma_db/`) if already built on disk.
3. Fast in-memory lexical + structure-chunked fallback on `data/<TICKER>/10-K/` so tests and demos work out-of-the-box without waiting 20 minutes to embed 130k chunks.
"""

import os
import re
from typing import Any, Callable, Dict, List, Optional

from src.system_c.corpus import chunk_corpus, load_filings
from src.system_c.state import AdaptiveRAGState, EvidenceChunk
from src.system_c.telemetry import track_node_latency

# In-memory cache of chunked filings per `(ticker, fiscal_year)` to keep multi-hop retrieval fast
_CORPUS_CACHE: Dict[str, List[Dict[str, Any]]] = {}
_CROSS_ENCODER: Any = None
_DENSE_EMBEDDER: Any = None

EMBED_MODEL = "BAAI/bge-small-en-v1.5"
BGE_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


def _get_dense_embedder():
    global _DENSE_EMBEDDER
    if _DENSE_EMBEDDER is None:
        from sentence_transformers import SentenceTransformer
        _DENSE_EMBEDDER = SentenceTransformer(EMBED_MODEL)
    return _DENSE_EMBEDDER


def _fetch_dense_candidates_from_supabase(
    query: str,
    tickers: List[str],
    fiscal_years: Optional[List[int]] = None,
    k: int = 20,
) -> Dict[str, float]:
    """Query top-k nearest neighbor chunk IDs and cosine similarities directly from Supabase pgvector."""
    supabase_url = os.getenv("SUPABASE_DB_URL")
    if not supabase_url or os.getenv("LLM_PROVIDER") == "mock":
        return {}
    try:
        import psycopg

        embedder = _get_dense_embedder()
        vec = embedder.encode([BGE_QUERY_PREFIX + query], normalize_embeddings=True)[0]
        params: Dict[str, Any] = {"vec": "[" + ",".join(map(str, vec.tolist())) + "]", "k": k}
        conditions = []
        if tickers:
            conditions.append("ticker = ANY(%(tickers)s)")
            params["tickers"] = tickers
        if fiscal_years:
            conditions.append("fiscal_year = ANY(%(years)s)")
            params["years"] = [int(y) for y in fiscal_years]
        where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
        with psycopg.connect(supabase_url, sslmode="require", autocommit=True) as conn:
            rows = conn.execute(
                f"""
                SELECT chunk_id, 1 - (embedding <=> %(vec)s::vector) AS sim
                FROM sec_chunks
                {where}
                ORDER BY embedding <=> %(vec)s::vector
                LIMIT %(k)s
                """,
                params,
            ).fetchall()
            return {r[0]: float(r[1]) for r in rows}
    except Exception:
        return {}


def _fetch_chunks_from_supabase(
    tickers: List[str], fiscal_years: Optional[List[int]] = None
) -> List[Dict[str, Any]]:
    """Fetch pre-computed 10-K structure chunks directly from Supabase Cloud `sec_chunks`."""
    supabase_url = os.getenv("SUPABASE_DB_URL")
    if not supabase_url:
        return []
    try:
        import json
        import psycopg2

        with psycopg2.connect(supabase_url, sslmode="require", connect_timeout=3) as conn:
            with conn.cursor() as cur:
                if fiscal_years:
                    cur.execute(
                        """
                        SELECT chunk_id, section, content, metadata
                        FROM sec_chunks
                        WHERE ticker = ANY(%s) AND fiscal_year = ANY(%s)
                        ORDER BY chunk_id;
                        """,
                        (tickers, fiscal_years),
                    )
                else:
                    cur.execute(
                        """
                        SELECT chunk_id, section, content, metadata
                        FROM sec_chunks
                        WHERE ticker = ANY(%s)
                        ORDER BY fiscal_year DESC, chunk_id;
                        """,
                        (tickers,),
                    )
                rows = cur.fetchall()
                if not rows:
                    return []
                records = []
                for r in rows:
                    meta = r[3] if isinstance(r[3], dict) else json.loads(r[3] or "{}")
                    doc_hdr = (
                        f"{meta.get('filer', '')} ({meta.get('ticker', '')}) 10-K, "
                        f"fiscal year {meta.get('fiscal_year', '')}, "
                        f"period ended {meta.get('fiscal_year_end', '')}"
                    )
                    records.append({
                        "id": r[0],
                        "text": r[2],
                        "meta": meta,
                        "embed_text": f"{doc_hdr}\n{r[2]}",
                    })
                return records
    except Exception:
        return []


def _get_cached_chunks(
    ticker: Optional[str] = None,
    fiscal_years: Optional[List[int]] = None,
    tickers: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Retrieve pre-computed structure chunks for target companies and fiscal years.
    1. Checks in-memory cache for ultra-fast multi-hop reuse.
    2. Queries live Supabase Cloud `sec_chunks` table (pre-computed chunks).
    3. Falls back to on-disk chunking only if database is offline/unreachable.
    """
    target_tickers = tickers or ([ticker] if ticker else ["NVDA"])
    tickers_key = ",".join(sorted(target_tickers))
    years_key = ",".join(str(y) for y in sorted(fiscal_years)) if fiscal_years else "LATEST"
    cache_key = f"{tickers_key}:{years_key}"
    if cache_key in _CORPUS_CACHE:
        return _CORPUS_CACHE[cache_key]

    # Primary: Query pre-computed chunks from Supabase Cloud
    records = _fetch_chunks_from_supabase(target_tickers, fiscal_years)
    if records:
        _CORPUS_CACHE[cache_key] = records
        return records

    # Secondary Fallback: Read from local files if offline/database unavailable
    filings = load_filings(
        tickers=target_tickers,
        fiscal_years=fiscal_years if fiscal_years else None,
        min_year=2023 if not fiscal_years else None,
    )
    if not filings and fiscal_years:
        filings = load_filings(tickers=target_tickers, min_year=2024)
    if not filings:
        filings = load_filings(tickers=target_tickers)[-4:]

    records = chunk_corpus(filings, header=True)
    _CORPUS_CACHE[cache_key] = records
    return records


STOPWORDS = {
    "what", "was", "and", "where", "its", "the", "for", "with", "from",
    "between", "how", "did", "which", "about", "under", "are", "were",
    "that", "this", "these", "those", "have", "has", "had", "been",
}


def _bm25_and_lexical_score(query: str, text: str) -> float:
    """Enhanced BM25-style TF-IDF scoring with bigram phrase matching and term coverage."""
    q_all = [t for t in re.findall(r"[a-z0-9]+", query.lower()) if len(t) > 2]
    q_terms = [t for t in q_all if t not in STOPWORDS] or q_all
    if not q_terms:
        return 0.0
    t_lower = text.lower()
    matched = [
        t for t in q_terms
        if t in t_lower or (t.endswith("s") and t[:-1] in t_lower) or (t + "s" in t_lower)
    ]
    cov = len(matched) / len(q_terms)
    phrase = 0.0
    for i in range(len(q_terms) - 1):
        bg = f"{q_terms[i]} {q_terms[i+1]}"
        if bg in t_lower or (bg + "s") in t_lower:
            phrase += 1.5
    tf = sum(min(2, t_lower.count(t)) * 0.05 for t in matched)
    table_bonus = 0.20 if "(table)" in t_lower or "|" in text else 0.0
    return round(cov * 3.0 + phrase + tf + table_bonus, 4)


def _rerank_with_cross_encoder(query: str, candidates: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    """
    Optionally rerank top candidates with cached HuggingFace CrossEncoder
    (`cross-encoder/ms-marco-MiniLM-L-6-v2`) when `USE_CROSS_ENCODER=1`.
    """
    global _CROSS_ENCODER
    if not candidates:
        return []
    if os.getenv("USE_CROSS_ENCODER", "0").strip() != "1":
        return candidates[:top_k]
    try:
        if _CROSS_ENCODER is None:
            from sentence_transformers import CrossEncoder
            model_name = os.getenv("CROSS_ENCODER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")
            _CROSS_ENCODER = CrossEncoder(model_name)
        pairs = [[query, c["text"][:1000]] for c in candidates]
        scores = _CROSS_ENCODER.predict(pairs)
        for cand, sc in zip(candidates, scores):
            cand["score"] = float(sc)
        candidates.sort(key=lambda x: x["score"], reverse=True)
    except Exception:
        pass
    return candidates[:top_k]


def retrieve_10k_chunks(
    query: str,
    ticker: Optional[str] = "NVDA",
    fiscal_years: Optional[List[int]] = None,
    top_k: int = 4,
    hop: int = 1,
    tickers: Optional[List[str]] = None,
) -> List[EvidenceChunk]:
    """
    Retrieve and rerank top-k structure-preserved 10-K chunks for `query`.
    Supports single-company or multi-company comparison queries.
    """
    records = _get_cached_chunks(ticker=ticker, fiscal_years=fiscal_years, tickers=tickers)
    if not records:
        # Synthetic fallback only if data directory is absent
        return [
            EvidenceChunk(
                chunk_id=f"{ticker or 'NVDA'}_FY2026_SYNTH:{hop}",
                content=f"Item 7. MD&A > Results of Operations\nSynthetic evidence for query: {query}",
                metadata={
                    "doc_id": f"{ticker or 'NVDA'}_FY2026",
                    "ticker": ticker or "NVDA",
                    "fiscal_year": (fiscal_years or [2026])[0],
                    "section": "Item 7. MD&A > Results of Operations",
                    "chunk": hop,
                },
                relevance_score=0.85,
                hop_retrieved=hop,
            )
        ]

    target_tickers = tickers or ([ticker] if ticker else ["NVDA"])
    dense_sims = _fetch_dense_candidates_from_supabase(query, target_tickers, fiscal_years, k=max(top_k * 6, 25))

    scored = []
    for rec in records:
        lex_sc = _bm25_and_lexical_score(query, rec.get("embed_text", rec["text"]))
        dense_sc = dense_sims.get(rec["id"], 0.0)
        if dense_sims:
            norm_lex = min(1.0, lex_sc / 3.0)
            score = 0.5 * dense_sc + 0.5 * norm_lex if (dense_sc > 0 or lex_sc > 0) else 0.0
        else:
            score = lex_sc

        if score > 0:
            scored.append({**rec, "score": score})

    if not scored:
        scored = [{**rec, "score": 0.1} for rec in records[: top_k * 2]]
    else:
        scored.sort(key=lambda x: x["score"], reverse=True)

    shortlist = scored[: max(top_k * 4, 15)]
    top_hits = _rerank_with_cross_encoder(query, shortlist, top_k=top_k)

    chunks: List[EvidenceChunk] = []
    for hit in top_hits:
        chunks.append(
            EvidenceChunk(
                chunk_id=hit["id"],
                content=hit["text"],
                metadata={
                    **hit["meta"],
                    "source_type": "10k_section_chunk",
                },
                relevance_score=round(float(hit["score"]), 4),
                hop_retrieved=hop,
            )
        )
    return chunks


def retriever_node(
    state: AdaptiveRAGState,
    custom_retriever_fn: Optional[Callable[..., List[EvidenceChunk]]] = None,
) -> Dict[str, Any]:
    """
    LangGraph Node: Execute Hybrid Retrieval + Reranking for `current_sub_query`,
    deduplicate by `chunk_id`, and append new chunks to `accumulated_evidence`.
    """
    telemetry = dict(state.get("telemetry", {}))
    hop = state.get("current_hop", 1)
    sub_query = state.get("current_sub_query") or state["original_query"]
    ticker = state.get("target_ticker") or "NVDA"
    tickers = state.get("target_tickers") or ([ticker] if ticker else ["NVDA"])
    years = state.get("fiscal_years") or []

    with track_node_latency(telemetry, "retriever"):
        fn = custom_retriever_fn or retrieve_10k_chunks
        try:
            new_chunks = fn(
                query=sub_query,
                ticker=ticker,
                fiscal_years=years,
                top_k=6,
                hop=hop,
                tickers=tickers,
            )
        except TypeError:
            # Fallback for custom_retriever_fn that only takes original args
            new_chunks = fn(
                query=sub_query,
                ticker=ticker,
                fiscal_years=years,
                top_k=6,
                hop=hop,
            )

        existing = list(state.get("accumulated_evidence", []))
        seen_ids = {c["chunk_id"] for c in existing}
        added_count = 0
        for ch in new_chunks:
            if ch["chunk_id"] not in seen_ids:
                existing.append(ch)
                seen_ids.add(ch["chunk_id"])
                added_count += 1

        # If all top-4 were already seen in Hop 1, widen search on Hop 2/3 to guarantee novel evidence
        if added_count == 0 and fn is retrieve_10k_chunks:
            wider_chunks = retrieve_10k_chunks(
                query=sub_query + " footnote table breakdown risk",
                ticker=ticker,
                fiscal_years=years,
                top_k=8,
                hop=hop,
            )
            for ch in wider_chunks:
                if ch["chunk_id"] not in seen_ids:
                    existing.append(ch)
                    seen_ids.add(ch["chunk_id"])
                    if len(existing) >= len(seen_ids):
                        break

    telemetry["hop_count"] = hop
    return {
        "accumulated_evidence": existing,
        "telemetry": telemetry,
    }
