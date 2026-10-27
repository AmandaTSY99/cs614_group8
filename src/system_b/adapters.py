"""Live adapters. Never create/rebuild a missing RAG3 collection."""
from pathlib import Path
import time

BGE_MODEL = 'BAAI/bge-small-en-v1.5'
BGE_PREFIX = 'Represent this sentence for searching relevant passages: '


class ChromaSource:
    def __init__(self, path='chroma_db', collection='rag3_structure_bge'):
        if not (Path(path) / 'chroma.sqlite3').is_file():
            raise FileNotFoundError(f'RAG3 database missing at {path}. Copy Amanda\'s Chroma folder here first.')
        import chromadb
        self.client = chromadb.PersistentClient(path=str(path))
        self.collection = self.client.get_collection(collection, embedding_function=None)
        if not self.collection.count():
            raise ValueError('RAG3 collection is empty')
        if (self.collection.metadata or {}).get('hnsw:space') != 'cosine':
            raise ValueError('Expected baseline RAG3 cosine-distance collection')
        self.embedder = None

    def records(self):
        records = []
        for offset in range(0, self.collection.count(), 2000):
            page = self.collection.get(limit=2000, offset=offset, include=['documents', 'metadatas'])
            for i, text, meta in zip(page['ids'], page['documents'], page['metadatas']):
                if not text or not meta or 'ticker' not in meta or 'fiscal_year' not in meta:
                    raise ValueError(f'Missing document or filing metadata: {i}')
                records.append({'id': i, 'text': text, 'meta': meta})
        return records

    def __call__(self, query, scope, k):
        if self.embedder is None:
            from sentence_transformers import SentenceTransformer
            self.embedder = SentenceTransformer(BGE_MODEL)
        vector = self.embedder.encode([BGE_PREFIX + query], normalize_embeddings=True)
        result = self.collection.query(query_embeddings=vector,
            n_results=min(k, self.collection.count()), where=scope.where(), include=['distances'])
        return list(zip(result['ids'][0], [1 - d for d in result['distances'][0]]))


class SupabaseSource:
    """Supabase pgvector source for System B: 95,044 chunks and rag5 BGE-small embeddings."""

    def __init__(self, table='sec_chunks'):
        import os
        from dotenv import load_dotenv
        load_dotenv(Path(__file__).resolve().parents[2] / '.env')
        url = os.environ.get('SUPABASE_DB_URL')
        if not url:
            raise ValueError('SUPABASE_DB_URL is required for SupabaseSource')
        import psycopg
        self.conn = psycopg.connect(url, sslmode='require', autocommit=True)
        self.table = table
        self.embedder = None

    def records(self, scope=None):
        import json
        from psycopg import sql
        conditions = []
        params = {}
        if scope:
            pairs = scope.filing_pairs or [(t, y) for t in scope.tickers or [None] for y in scope.years or [None]]
            for n, (ticker, year) in enumerate(pairs):
                parts = []
                if ticker:
                    parts.append(sql.SQL("ticker = {}").format(sql.Placeholder(f"t{n}")))
                    params[f"t{n}"] = ticker
                if year:
                    parts.append(sql.SQL("fiscal_year = {}").format(sql.Placeholder(f"y{n}")))
                    params[f"y{n}"] = int(year)
                if parts:
                    conditions.append(sql.SQL("(") + sql.SQL(" and ").join(parts) + sql.SQL(")"))
        where = sql.SQL("where ") + sql.SQL(" or ").join(conditions) if conditions else sql.SQL("")
        query = sql.SQL("select chunk_id, content, ticker, fiscal_year, section, metadata from {} {} order by chunk_id").format(
            sql.Identifier(self.table), where
        )
        rows = self.conn.execute(query, params).fetchall()
        records = []
        for cid, text, ticker, year, sec, meta in rows:
            meta_dict = meta if isinstance(meta, dict) else (json.loads(meta) if meta else {})
            records.append({
                'id': cid,
                'text': text,
                'meta': {
                    **meta_dict,
                    'ticker': ticker,
                    'fiscal_year': year,
                    'section': sec,
                    'doc_id': cid.rsplit(':', 1)[0],
                }
            })
        return records

    def __call__(self, query, scope, k):
        if self.embedder is None:
            from sentence_transformers import SentenceTransformer
            self.embedder = SentenceTransformer(BGE_MODEL)
        from psycopg import sql
        vector = self.embedder.encode([BGE_PREFIX + query], normalize_embeddings=True)[0]
        params = {"vec": "[" + ",".join(map(str, vector.tolist())) + "]", "k": k}
        conditions = []
        pairs = scope.filing_pairs or [(t, y) for t in scope.tickers or [None] for y in scope.years or [None]] if scope else []
        for n, (ticker, year) in enumerate(pairs):
            parts = []
            if ticker:
                parts.append(sql.SQL("ticker = {}").format(sql.Placeholder(f"t{n}")))
                params[f"t{n}"] = ticker
            if year:
                parts.append(sql.SQL("fiscal_year = {}").format(sql.Placeholder(f"y{n}")))
                params[f"y{n}"] = int(year)
            if parts:
                conditions.append(sql.SQL("(") + sql.SQL(" and ").join(parts) + sql.SQL(")"))
        where = sql.SQL("where ") + sql.SQL(" or ").join(conditions) if conditions else sql.SQL("")
        rows = self.conn.execute(sql.SQL("""
            select chunk_id, 1 - (embedding <=> %(vec)s::vector)
            from {} {}
            order by embedding <=> %(vec)s::vector
            limit %(k)s
        """).format(sql.Identifier(self.table), where), params).fetchall()
        return [(r[0], float(r[1])) for r in rows]


class Reranker:
    def __init__(self, model='BAAI/bge-reranker-large'):
        self.name, self.model = model, None

    def __call__(self, query, texts):
        if self.model is None:
            from sentence_transformers import CrossEncoder
            self.model = CrossEncoder(self.name, max_length=512)
        # Model tokenization truncates at 512 tokens; full evidence is retained for generation.
        return self.model.predict([(query, text) for text in texts], show_progress_bar=False)


class Generator:
    def __init__(self, model, base_url=None):
        import os
        from openai import OpenAI
        key = os.environ.get('SYSTEM_B_API_KEY') or os.environ.get('OPENAI_API_KEY')
        if not key:
            raise ValueError('Set SYSTEM_B_API_KEY or OPENAI_API_KEY for generation')
        self.client = OpenAI(api_key=key, base_url=base_url, timeout=90, max_retries=0)
        self.model = model

    def __call__(self, messages):
        from openai import RateLimitError
        for attempt in range(9):
            try:
                call_kwargs = dict(model=self.model, messages=messages, temperature=0)
                if "gpt-5" in self.model or "o1" in self.model or "o3" in self.model:
                    call_kwargs["max_completion_tokens"] = 1500
                else:
                    call_kwargs["max_tokens"] = 1500
                response = self.client.chat.completions.create(**call_kwargs)
                break
            except RateLimitError as exc:
                if attempt == 8 or 'tokens per day' in str(exc).lower():
                    raise
                retry_after = exc.response.headers.get('retry-after', '')
                try:
                    delay = float(retry_after)
                except ValueError:
                    delay = min(30, 2 ** attempt)
                time.sleep(max(1, delay) + 1)
        if not response.choices[0].message.content:
            raise RuntimeError('Generator returned no answer')
        return {'answer': response.choices[0].message.content,
                'usage': response.usage.model_dump() if response.usage else None,
                'model': response.model, 'rate_limit_retries': attempt,
                'finish_reason': response.choices[0].finish_reason}
