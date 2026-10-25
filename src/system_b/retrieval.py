"""Dependency-free BM25 and hybrid orchestration; model adapters are separate."""
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from math import isfinite, log
import re
from time import perf_counter


def tokenize(text):
    # Keep decimal numbers and alphanumeric financial identifiers intact.
    return re.findall(r"[a-z0-9]+(?:[.-][a-z0-9]+)*", text.lower())


@dataclass(frozen=True)
class Scope:
    tickers: tuple = ()
    years: tuple = ()
    filing_pairs: tuple = ()

    def __post_init__(self):
        if self.filing_pairs and (self.tickers or self.years):
            raise ValueError('Use filing_pairs or ticker/year lists, not both')

    def payload(self):
        result = {'tickers': list(self.tickers), 'years': list(self.years)}
        if self.filing_pairs:
            result['filing_pairs'] = [list(p) for p in self.filing_pairs]
        return result

    def matches(self, meta):
        if self.filing_pairs:
            return (meta.get('ticker'), meta.get('fiscal_year')) in self.filing_pairs
        return (not self.tickers or meta.get('ticker') in self.tickers) and (
            not self.years or meta.get('fiscal_year') in self.years)

    def where(self):
        if self.filing_pairs:
            filters = [{'$and': [{'ticker': t}, {'fiscal_year': y}]} for t, y in self.filing_pairs]
            return filters[0] if len(filters) == 1 else {'$or': filters}
        clauses = []
        if self.tickers:
            clauses.append({'ticker': {'$in': list(self.tickers)}})
        if self.years:
            clauses.append({'fiscal_year': {'$in': list(self.years)}})
        return {'$and': clauses} if len(clauses) > 1 else (clauses[0] if clauses else None)


class BM25:
    """Okapi BM25 with positive Robertson IDF and corpus-wide statistics."""
    def __init__(self, records, k1=1.5, b=0.75):
        self.records = {r['id']: r for r in records}
        if len(self.records) != len(records):
            raise ValueError('Duplicate chunk IDs')
        self.k1, self.b = k1, b
        self.lengths, self.postings = {}, defaultdict(dict)
        for r in records:
            counts = Counter(tokenize(r['text']))
            self.lengths[r['id']] = sum(counts.values())
            for term, count in counts.items():
                self.postings[term][r['id']] = count
        self.avg = sum(self.lengths.values()) / max(1, len(records)) or 1

    def search(self, query, scope, k):
        scores = defaultdict(float)
        n = len(self.records)
        for term in set(tokenize(query)):
            postings = self.postings.get(term, {})
            idf = log(1 + (n - len(postings) + 0.5) / (len(postings) + 0.5))
            for chunk_id, tf in postings.items():
                if scope.matches(self.records[chunk_id]['meta']):
                    norm = self.k1 * (1 - self.b + self.b * self.lengths[chunk_id] / self.avg)
                    scores[chunk_id] += idf * tf * (self.k1 + 1) / (tf + norm)
        return sorted(scores.items(), key=lambda x: (-x[1], x[0]))[:k]


def normalize(scores):
    if not scores:
        return {}
    if not all(isfinite(s) for s in scores.values()):
        raise ValueError('Non-finite retrieval score')
    lo, hi = min(scores.values()), max(scores.values())
    return {i: (s - lo) / (hi - lo) if hi > lo else 1.0 for i, s in scores.items()}


@dataclass(frozen=True)
class Config:
    alpha: float = 0.5
    candidates: int = 30
    rerank_candidates: int = 30
    top_k: int = 5
    mode: str = 'hybrid_rerank'

    def __post_init__(self):
        if not 0 <= self.alpha <= 1:
            raise ValueError('alpha must be between 0 and 1')
        if not 1 <= self.top_k <= self.rerank_candidates <= self.candidates:
            raise ValueError('Require 1 <= top_k <= rerank_candidates <= candidates')
        if self.mode not in ('dense', 'bm25', 'hybrid', 'hybrid_rerank'):
            raise ValueError('Unknown retrieval mode')


class Retriever:
    def __init__(self, records, dense=None, reranker=None, config=None):
        self.bm25 = BM25(records)
        self.records = self.bm25.records
        self.dense, self.reranker = dense, reranker
        self.config = config or Config()

    def retrieve(self, query, scope=Scope()):
        if not query.strip():
            raise ValueError('Question cannot be empty')
        c = self.config
        start = perf_counter()
        timings = {}
        sparse, dense = {}, {}
        if c.mode != 'dense':
            t = perf_counter()
            sparse = dict(self.bm25.search(query, scope, c.candidates))
            timings['bm25_seconds'] = perf_counter() - t
        if c.mode != 'bm25':
            if self.dense is None:
                raise RuntimeError('Dense backend is required')
            t = perf_counter()
            dense = dict(self.dense(query, scope, c.candidates))
            timings['dense_seconds'] = perf_counter() - t
        for i in dense:
            if i not in self.records or not scope.matches(self.records[i]['meta']):
                raise ValueError('Dense backend returned unknown or out-of-scope chunk')
        dn, sn = normalize(dense), normalize(sparse)
        alpha = 1 if c.mode == 'dense' else 0 if c.mode == 'bm25' else c.alpha
        ids = (set(dense) if alpha == 1 else set(sparse) if alpha == 0 else set(dense) | set(sparse))
        hits = [{**self.records[i], 'dense_score': dense.get(i), 'bm25_score': sparse.get(i),
                 'fusion_score': alpha * dn.get(i, 0) + (1-alpha) * sn.get(i, 0)} for i in ids]
        hits.sort(key=lambda h: (-h['fusion_score'], h['id']))
        hits = hits[:c.rerank_candidates]
        if c.mode == 'hybrid_rerank' and hits:
            if self.reranker is None:
                raise RuntimeError('Cross-encoder is required; no silent fallback')
            t = perf_counter()
            scores = list(self.reranker(query, [h['text'] for h in hits]))
            if len(scores) != len(hits) or not all(isfinite(float(s)) for s in scores):
                raise ValueError('Invalid cross-encoder scores')
            for hit, score in zip(hits, scores):
                hit['rerank_score'] = float(score)
            hits.sort(key=lambda h: (-h['rerank_score'], h['id']))
            timings['rerank_seconds'] = perf_counter() - t
        timings['retrieval_seconds'] = perf_counter() - start
        return {'hits': hits[:c.top_k], 'timings': timings, 'config': asdict(c)}
