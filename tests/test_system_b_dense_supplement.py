import unittest

from src.system_b.retrieval import Config, Retriever, Scope


class TestDenseSupplement(unittest.TestCase):
    def test_dense_tail_recovers_a_scoped_hit_without_displacing_first_five(self):
        records = [{"id": str(i), "text": f"sales item {i}",
                    "meta": {"ticker": "TEST", "fiscal_year": 2020}} for i in range(12)]
        def dense(query, scope, count):
            return [(str(i), 1 - i / 20) for i in range(count)]
        def rank(query, texts):
            return [int(text.split()[-1]) for text in texts]
        scope = Scope(("TEST",), (2020,))
        def retrieve(limit):
            config = Config(candidates=12, rerank_candidates=12, top_k=limit)
            return [hit["id"] for hit in Retriever(records, dense, rank, config).retrieve("sales", scope)["hits"]]
        self.assertEqual(retrieve(5), ["11", "10", "9", "8", "7"])
        self.assertEqual(retrieve(10), ["11", "10", "9", "8", "7", "0", "1", "2", "3", "4"])
