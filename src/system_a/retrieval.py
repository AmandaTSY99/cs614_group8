"""Dense retrieval over the RAG 3 index (structure-based chunks + bge-small), from Chroma or Supabase.

Every index has the same interface: `retrieve(query, k, pairs)` returns a list of
{"id", "score", "text", "meta"} dicts, best first, with score = cosine similarity.
"""
from pathlib import Path

import chromadb
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

ROOT = Path(__file__).resolve().parents[2]
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
BGE_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "  # bge was trained with this on queries


class QueryEmbedder:
    """Must be the model that embedded the chunks, or the query and chunk vectors don't line up."""

    def __init__(self, model_name=EMBED_MODEL):
        if SentenceTransformer is None:
            raise ImportError("sentence-transformers is required for QueryEmbedder. Please install sentence-transformers.")
        self.model = SentenceTransformer(model_name)
        self.prefix = BGE_QUERY_PREFIX if "bge" in model_name.lower() else ""   # only bge expects a query prefix

    def __call__(self, query):
        return self.model.encode([self.prefix + query], normalize_embeddings=True)[0]


def make_filter(pairs):
    """Chroma `where` filter from (ticker, fiscal_year) pairs. None in a pair means any; no pairs = whole corpus."""
    filters = []
    for ticker, year in pairs or []:
        conditions = ([{"ticker": ticker}] if ticker else []) + ([{"fiscal_year": year}] if year else [])
        if conditions:
            filters.append(conditions[0] if len(conditions) == 1 else {"$and": conditions})
    if not filters:
        return None
    return filters[0] if len(filters) == 1 else {"$or": filters}


class ChromaIndex:
    """A saved Chroma collection (built in build_vdb_base_RAG.ipynb), opened without re-embedding anything."""

    def __init__(self, chroma_dir="chroma_db", collection="rag3_structure_bge", embedder=None):
        path = ROOT / chroma_dir                      # an absolute chroma_dir is used as is
        self.collection = chromadb.PersistentClient(path=str(path)).get_collection(collection, embedding_function=None)
        if self.collection.count() == 0:
            raise ValueError(f"'{collection}' in {path} is empty: build it first in build_vdb_base_RAG.ipynb")
        self.embed = embedder or QueryEmbedder()
        self.name = f"chroma:{collection}"
        print(f"{self.name}: {self.collection.count():,} vectors from {path}")

    def retrieve(self, query, k=5, pairs=None):
        res = self.collection.query(query_embeddings=[self.embed(query)], n_results=k,
                                    where=make_filter(pairs), include=["documents", "metadatas", "distances"])
        return [{"id": id_, "score": 1 - dist, "text": doc, "meta": meta}
                for id_, dist, doc, meta in zip(res["ids"][0], res["distances"][0],
                                                res["documents"][0], res["metadatas"][0])]


# --- Supabase (pgvector) --------------------------------------------------------------------
# The shared table holds the RAG 3 chunks for FY2023-2026 only (20,125 rows), so benchmark QAs on
# older filings cannot be answered from it. Needs psycopg (requirements.txt) and SUPABASE_DB_* in .env.
# To use it: uncomment this class, plus the --store / --supabase-table lines in __main__.py.
#
# import getpass
# import os
#
# import psycopg
# from dotenv import load_dotenv
# from psycopg import sql
#
#
# class SupabaseIndex:
#     """The shared Supabase table: same chunks and model as rag3_structure_bge, searched with pgvector."""
#
#     def __init__(self, table="chunks", embedder=None):
#         load_dotenv(ROOT / ".env")                    # SUPABASE_DB_* (no password stored there)
#         if not os.environ.get("SUPABASE_DB_PASSWORD"):
#             os.environ["SUPABASE_DB_PASSWORD"] = getpass.getpass("Enter your SUPABASE_DB_PASSWORD: ")
#         self.conn = psycopg.connect(
#             host=os.environ["SUPABASE_DB_HOST"],
#             port=os.environ["SUPABASE_DB_PORT"],
#             dbname=os.environ["SUPABASE_DB_NAME"],
#             user=os.environ["SUPABASE_DB_USER"],
#             password=os.environ["SUPABASE_DB_PASSWORD"],
#             sslmode="require",
#             autocommit=True,
#         )
#         self.table = sql.Identifier(table)
#         self.embed = embedder or QueryEmbedder()
#         self.name = f"supabase:{table}"
#         count = self.conn.execute(sql.SQL("select count(*) from {}").format(self.table)).fetchone()[0]
#         print(f"{self.name}: {count:,} rows")
#
#     def retrieve(self, query, k=5, pairs=None):
#         vec = self.embed(query)
#         params = {"vec": "[" + ",".join(map(str, vec.tolist())) + "]", "k": k}
#         conditions = []
#         for n, (ticker, year) in enumerate(pairs or []):
#             parts = []
#             if ticker:
#                 parts.append(sql.SQL("ticker = {}").format(sql.Placeholder(f"t{n}")))
#                 params[f"t{n}"] = ticker
#             if year:
#                 parts.append(sql.SQL("fiscal_year = {}").format(sql.Placeholder(f"y{n}")))
#                 params[f"y{n}"] = year
#             if parts:
#                 conditions.append(sql.SQL("(") + sql.SQL(" and ").join(parts) + sql.SQL(")"))
#         where = sql.SQL("where ") + sql.SQL(" or ").join(conditions) if conditions else sql.SQL("")
#         rows = self.conn.execute(sql.SQL("""
#             select chunk_id, 1 - (embedding <=> %(vec)s::vector), content, ticker, fiscal_year, section, metadata
#             from {} {}
#             order by embedding <=> %(vec)s::vector
#             limit %(k)s
#         """).format(self.table, where), params).fetchall()
#         return [{"id": id_, "score": score, "text": text,
#                  "meta": {**(meta or {}), "doc_id": id_.rsplit(":", 1)[0],
#                           "ticker": ticker, "fiscal_year": year, "section": section}}
#                 for id_, score, text, ticker, year, section, meta in rows]
