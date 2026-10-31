"""
Hybrid Retriever + Cross-Encoder Reranker Node for System C.

Supports Research Question 1 (Retrieval Recall & Non-Adjacent Section Discovery):
1. Hybrid Retrieval (BM25 lexical + Dense embeddings + Cross-Encoder Reranking) over 10-K filings.
2. Connection to Supabase pgvector `sec_chunks` and local Chroma index (`chroma_db/`).
3. Multi-hop evidence accumulation with chunk deduplication and hop attribution tags.
"""

import os
import re
from typing import Any, Callable, Dict, List, Optional

from src.system_c.corpus import chunk_corpus, extract_all_tickers_and_years_from_query, load_filings
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
    is_mock = os.getenv("LLM_PROVIDER", "").strip().lower() == "mock"
    if not supabase_url or is_mock:
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
        if not is_mock:
            raise
        return {}


def _fetch_chunks_from_supabase(
    tickers: List[str], fiscal_years: Optional[List[int]] = None
) -> List[Dict[str, Any]]:
    """Fetch pre-computed 10-K structure chunks directly from Supabase Cloud `sec_chunks`."""
    supabase_url = os.getenv("SUPABASE_DB_URL")
    is_mock = os.getenv("LLM_PROVIDER", "").strip().lower() == "mock"
    if not supabase_url:
        return []
    clean_tickers = []
    for t in (tickers or []):
        if isinstance(t, str) and "," in t:
            clean_tickers.extend([part.strip().upper() for part in t.split(",") if part.strip()])
        elif t:
            clean_tickers.append(str(t).strip().upper())
    clean_tickers = sorted(list(dict.fromkeys(clean_tickers)))
    if not clean_tickers:
        clean_tickers = ["NVDA"]

    try:
        import json
        import psycopg

        with psycopg.connect(supabase_url, sslmode="require", autocommit=True) as conn:
            if fiscal_years:
                rows = conn.execute(
                    """
                    SELECT chunk_id, section, content, metadata
                    FROM sec_chunks
                    WHERE ticker = ANY(%s) AND fiscal_year = ANY(%s)
                    ORDER BY chunk_id;
                    """,
                    (clean_tickers, [int(y) for y in fiscal_years]),
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT chunk_id, section, content, metadata
                    FROM sec_chunks
                    WHERE ticker = ANY(%s)
                    ORDER BY fiscal_year DESC, chunk_id;
                    """,
                    (clean_tickers,),
                ).fetchall()
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
        if not is_mock:
            raise
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
    is_mock = os.getenv("LLM_PROVIDER", "").strip().lower() == "mock"
    if not is_mock and not os.getenv("SUPABASE_DB_URL"):
        raise RuntimeError(
            "SUPABASE_DB_URL is not set. Live System C requires Supabase pgvector (sec_chunks) "
            "and does not fall back to local files or synthetic chunks."
        )

    raw_tickers = tickers or ([ticker] if ticker else ["NVDA"])
    target_tickers = []
    for t in raw_tickers:
        if isinstance(t, str) and "," in t:
            target_tickers.extend([part.strip().upper() for part in t.split(",") if part.strip()])
        elif t:
            target_tickers.append(str(t).strip().upper())
    target_tickers = sorted(list(dict.fromkeys(target_tickers)))
    if not target_tickers:
        target_tickers = ["NVDA"]

    tickers_key = ",".join(sorted(target_tickers))
    years_key = ",".join(str(y) for y in sorted(fiscal_years)) if fiscal_years else "LATEST"
    cache_key = f"{tickers_key}:{years_key}"
    if cache_key in _CORPUS_CACHE:
        return _CORPUS_CACHE[cache_key]

    # Primary: Query pre-computed chunks from Supabase Cloud
    records = _fetch_chunks_from_supabase(target_tickers, fiscal_years)
    if not records and fiscal_years and os.getenv("SUPABASE_DB_URL") and not is_mock:
        # If multi-company query has disjoint fiscal years (e.g. NVDA FY2026 vs MSFT FY2024), widen year filter
        records = _fetch_chunks_from_supabase(target_tickers, None)
    if records:
        _CORPUS_CACHE[cache_key] = records
        return records

    # Secondary Fallback (Mock / Offline Unit Tests Only): Read from local files if present
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
        if os.getenv("LLM_PROVIDER", "").strip().lower() != "mock":
            raise RuntimeError(
                f"No chunks retrieved from Supabase sec_chunks for tickers={tickers or [ticker]}, "
                f"fiscal_years={fiscal_years}. Refusing to return synthetic dummy chunks in live mode."
            )
        # Synthetic fallback strictly for mock mode unit tests when local data directory is absent
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


TABLE_LEAD_IN_RE = re.compile(
    r"(?:(?:following\s+table|summarized\s+below|is\s+set\s+forth\s+below|are\s+set\s+forth\s+below|as\s+follows)\s*:|"
    r"(?:following\s+table[^\n:]{0,120}:|summarized\s+below[^\n:]{0,60}:|set\s+forth\s+below[^\n:]{0,60}:|as\s+follows[^\n:]{0,60}:))",
    re.IGNORECASE,
)

STRUCTURAL_TABLE_CONTINUATION_RE = re.compile(
    r"(?:"
    r"following\s+table[^\n:]{0,120}:|"
    r"summarized\s+below[^\n:]{0,60}:|"
    r"set\s+forth\s+below[^\n:]{0,60}:|"
    r"as\s+follows[^\n:]{0,60}:|"
    r"\b(?:are|is|were|was|consists?\s+of|comprises?\s+of)\s*:\s*$|"
    r"\|[^\n]+\|\s*$"
    r")",
    re.IGNORECASE | re.MULTILINE,
)


def _get_adjacent_chunk_id(chunk_id: str) -> Optional[str]:
    """Given a chunk_id like MSFT_FY2017_2017-06-30:379, return MSFT_FY2017_2017-06-30:380."""
    if not chunk_id:
        return None
    if ":" in chunk_id:
        prefix, seq_str = chunk_id.rsplit(":", 1)
        if seq_str.isdigit():
            return f"{prefix}:{int(seq_str) + 1}"
    m = re.search(r"^(.*?)([-_])(\d+)$", chunk_id)
    if m:
        prefix, sep, seq_str = m.group(1), m.group(2), m.group(3)
        return f"{prefix}{sep}{int(seq_str) + 1}"
    return None


def _fetch_chunk_by_id(chunk_id: str, cached_records: Optional[List[Dict[str, Any]]] = None) -> Optional[Dict[str, Any]]:
    """Retrieve chunk by exact chunk_id from in-memory cache or live Supabase Cloud sec_chunks."""
    if not chunk_id:
        return None
    if cached_records:
        for r in cached_records:
            if r.get("id") == chunk_id:
                return r
    for key, records in _CORPUS_CACHE.items():
        for r in records:
            if r.get("id") == chunk_id:
                return r
    supabase_url = os.getenv("SUPABASE_DB_URL")
    is_mock = os.getenv("LLM_PROVIDER", "").strip().lower() == "mock"
    if supabase_url and not is_mock:
        try:
            import json
            import psycopg

            with psycopg.connect(supabase_url, sslmode="require", autocommit=True) as conn:
                row = conn.execute(
                    "SELECT chunk_id, section, content, metadata FROM sec_chunks WHERE chunk_id = %s",
                    (chunk_id,),
                ).fetchone()
                if row:
                    meta = row[3] if isinstance(row[3], dict) else json.loads(row[3] or "{}")
                    return {
                        "id": row[0],
                        "text": row[2],
                        "meta": meta,
                    }
        except Exception:
            pass
    elif is_mock:
        return {
            "id": chunk_id,
            "text": "Item 8 > PART II (table)\n| (In millions) |\n| Total | $10,106 |",
            "meta": {"chunk_id": chunk_id, "section": "Item 8 > PART II", "ticker": "MSFT", "fiscal_year": 2017},
        }
    return None


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
    tickers = list(state.get("target_tickers") or ([ticker] if ticker else ["NVDA"]))
    years = list(state.get("fiscal_years") or [])

    mode = state.get("mode")
    if mode == "v3_aamr_sg":
        # Atomic sub-query single ticker isolation for cross-company comparative queries
        if len(tickers) > 1:
            sub_tickers, _ = extract_all_tickers_and_years_from_query(sub_query)
            matching_tickers = [t for t in sub_tickers if t in tickers]
            if len(matching_tickers) == 1:
                isolated_ticker = matching_tickers[0]
                tickers = [isolated_ticker]
                ticker = isolated_ticker

        # Dynamic Year Expansion in Follow-Up Hops:
        # If the Critic flagged missing_years, dynamically expand fiscal_years
        critic_missing_years = []
        for y in state.get("missing_years") or []:
            try:
                s = str(y).strip().upper()
                val = int(s[2:] if s.startswith("FY") else s)
                critic_missing_years.append(val)
            except (ValueError, TypeError):
                pass
        if critic_missing_years:
            for y in critic_missing_years:
                if y not in years:
                    years.append(y)
            years = sorted(years)

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
                tickers=tickers,
            )
            for ch in wider_chunks:
                if ch["chunk_id"] not in seen_ids:
                    existing.append(ch)
                    seen_ids.add(ch["chunk_id"])
                    if len(existing) >= len(seen_ids):
                        break

        # Adjacent Table Chunk Stitching for Orphaned & Severed Table Chunking (mode == "v3_aamr_sg")
        if mode == "v3_aamr_sg":
            stitched_chunks: List[EvidenceChunk] = []
            for ch in list(existing):
                content = ch.get("content", "").strip()
                if STRUCTURAL_TABLE_CONTINUATION_RE.search(content) or TABLE_LEAD_IN_RE.search(content):
                    adj_cid = _get_adjacent_chunk_id(ch.get("chunk_id", ""))
                    if adj_cid and adj_cid not in seen_ids:
                        adj_rec = _fetch_chunk_by_id(adj_cid)
                        if adj_rec:
                            adj_text = adj_rec.get("text", "")
                            is_table_row_end = bool(re.search(r"\|[^\n]+\|\s*$", content))
                            if not is_table_row_end or ("|" in adj_text or "(table)" in adj_text.lower()):
                                stitched = EvidenceChunk(
                                    chunk_id=adj_rec["id"],
                                    content=adj_text,
                                    metadata={
                                        **(adj_rec.get("meta") or {}),
                                        "source_type": "10k_section_chunk",
                                        "stitched_from": ch.get("chunk_id"),
                                    },
                                    relevance_score=round(float(ch.get("relevance_score", 0.90)), 4),
                                    hop_retrieved=hop,
                                )
                                stitched_chunks.append(stitched)
                                seen_ids.add(adj_cid)

                                # If the stitched chunk itself ends mid-table, stitch one more contiguous chunk
                                if re.search(r"\|[^\n]+\|\s*$", adj_text.strip()):
                                    next_adj_cid = _get_adjacent_chunk_id(adj_cid)
                                    if next_adj_cid and next_adj_cid not in seen_ids:
                                        next_adj_rec = _fetch_chunk_by_id(next_adj_cid)
                                        if next_adj_rec and ("|" in next_adj_rec.get("text", "") or "(table)" in next_adj_rec.get("text", "").lower()):
                                            stitched_2 = EvidenceChunk(
                                                chunk_id=next_adj_rec["id"],
                                                content=next_adj_rec["text"],
                                                metadata={
                                                    **(next_adj_rec.get("meta") or {}),
                                                    "source_type": "10k_section_chunk",
                                                    "stitched_from": adj_cid,
                                                },
                                                relevance_score=round(float(ch.get("relevance_score", 0.90)), 4),
                                                hop_retrieved=hop,
                                            )
                                            stitched_chunks.append(stitched_2)
                                            seen_ids.add(next_adj_cid)
            if stitched_chunks:
                existing.extend(stitched_chunks)

    telemetry["hop_count"] = hop
    ret = {
        "accumulated_evidence": existing,
        "telemetry": telemetry,
    }
    if mode == "v3_aamr_sg" and years != (state.get("fiscal_years") or []):
        ret["fiscal_years"] = years
        if tickers and years:
            ret["target_pairs"] = [[t, y] for t in tickers for y in years]
    return ret
