"""Live adapters. Never create/rebuild a missing RAG3 collection."""
from pathlib import Path

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
        self.client = OpenAI(api_key=key, base_url=base_url, timeout=90, max_retries=1)
        self.model = model

    def __call__(self, messages):
        response = self.client.chat.completions.create(model=self.model, messages=messages,
            temperature=0, max_tokens=1500)
        if not response.choices[0].message.content:
            raise RuntimeError('Generator returned no answer')
        return {'answer': response.choices[0].message.content,
                'usage': response.usage.model_dump() if response.usage else None,
                'model': response.model}
