import math
import unittest
import contextlib
import io
import json
from pathlib import Path
import tempfile
from unittest.mock import patch
from src.system_b.retrieval import BM25, Config, Retriever, Scope, normalize, tokenize
from src.system_b.pipeline import run


def record(i, text, ticker='NVDA', year=2026):
    return {'id': i, 'text': text, 'meta': {'ticker': ticker, 'fiscal_year': year}}


class SystemBTests(unittest.TestCase):
    def setUp(self):
        self.records = [record('a', 'revenue revenue growth'), record('b', 'export restrictions'),
                        record('c', 'revenue', 'AAPL', 2024)]

    def test_bm25_formula(self):
        index = BM25([record('a', 'debt debt'), record('b', 'cash')])
        score = dict(index.search('debt', Scope(), 5))['a']
        expected = math.log(2) * 2 * 2.5 / (2 + 1.5 * (.25 + .75 * 2 / 1.5))
        self.assertAlmostEqual(score, expected)

    def test_scope_and_financial_tokens(self):
        self.assertEqual(tokenize('FY2026 10-K 3.5%'), ['fy2026', '10-k', '3.5'])
        index = BM25(self.records)
        self.assertEqual([i for i, _ in index.search('revenue', Scope(('NVDA',), (2026,)), 5)], ['a'])
        self.assertEqual(index.search('absent', Scope(), 5), [])
        self.assertIn('$and', Scope(('NVDA', 'AAPL'), (2024,)).where())

    def test_reranking_dedup_and_citations(self):
        def dense(q, scope, k):
            return [('a', .9), ('b', .5)]
        r = Retriever(self.records, dense, lambda q, texts: [0, 10], Config(top_k=1))
        out = run(r, 'revenue', Scope(('NVDA',), (2026,)),
                  lambda messages: {'answer': 'Restrictions [1]', 'usage': {'total_tokens': 8}})
        self.assertEqual(out['hits'][0]['id'], 'b')
        self.assertEqual(out['citations'], {'1': 'b'})
        self.assertEqual(out['invalid_citation_labels'], [])
        self.assertEqual(out['usage']['total_tokens'], 8)

    def test_alpha_endpoints(self):
        for alpha, expected in [(0, 'a'), (1, 'b')]:
            r = Retriever(self.records, lambda *a: [('b', .9)],
                          config=Config(alpha=alpha, mode='hybrid', top_k=1))
            self.assertEqual(r.retrieve('revenue', Scope(('NVDA',), (2026,)))['hits'][0]['id'], expected)

    def test_cross_scope_dense_rejected(self):
        r = Retriever(self.records, lambda *a: [('c', .9)], config=Config(mode='dense'))
        with self.assertRaisesRegex(ValueError, 'out-of-scope'):
            r.retrieve('revenue', Scope(('NVDA',), (2026,)))

    def test_reranker_failure_is_not_hidden(self):
        def fail(*args):
            raise RuntimeError('model unavailable')
        r = Retriever(self.records, lambda *a: [('a', .9)], fail)
        with self.assertRaisesRegex(RuntimeError, 'model unavailable'):
            r.retrieve('revenue')

    def test_no_evidence_skips_generation(self):
        r = Retriever(self.records, config=Config(mode='bm25'))
        def fail(messages):
            self.fail('No evidence must not call LLM')
        self.assertEqual(run(r, 'absent', generator=fail)['status'], 'no_evidence')

    def test_invalid_citation_exposed(self):
        r = Retriever(self.records, config=Config(mode='bm25'))
        out = run(r, 'revenue', generator=lambda m: {'answer': 'Claim [99]'})
        self.assertEqual(out['invalid_citation_labels'], ['99'])

    def test_validation(self):
        with self.assertRaises(ValueError):
            Config(alpha=2)
        with self.assertRaises(ValueError):
            Config(top_k=0)
        with self.assertRaises(ValueError):
            BM25(self.records + [self.records[0]])
        with self.assertRaises(ValueError):
            normalize({'a': float('nan')})
        self.assertEqual(normalize({'a': 2, 'b': 2}), {'a': 1, 'b': 1})

    def test_batch_runner_preserves_failures_and_multi_company_scope(self):
        from src.system_b.__main__ import main
        records = self.records + [record('d', 'revenue', 'AAPL', 2026)]
        class Source:
            def __init__(self, *args):
                pass
            def records(self):
                return records
            def __call__(self, query, scope, k):
                return [(r['id'], .8) for r in records if scope.matches(r['meta'])][:k]
        with tempfile.TemporaryDirectory() as tmp:
            questions, output = Path(tmp) / 'questions.json', Path(tmp) / 'results.jsonl'
            questions.write_text(json.dumps([
                {'id': 'multi', 'query': 'revenue', 'target_tickers': ['NVDA', 'AAPL'], 'fiscal_years': [2026]},
                {'id': 'missing', 'query': 'revenue', 'ticker': 'MSFT', 'fiscal_years': [2026]},
            ]), encoding='utf-8')
            argv = ['system_b', '--benchmark', str(questions), '--all-modes', '--output', str(output)]
            with patch('sys.argv', argv), patch('src.system_b.__main__.ChromaSource', Source), \
                 patch('src.system_b.__main__.Reranker', return_value=lambda q, texts: [1] * len(texts)), \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(), 1)
            rows = [json.loads(line) for line in output.read_text(encoding='utf-8').splitlines()]
            self.assertEqual(len(rows), 8)
            self.assertEqual([r['status'] for r in rows[:4]], ['retrieval_only'] * 4)
            self.assertTrue(all(r['status'] == 'error' for r in rows[4:]))
            self.assertEqual(rows[0]['scope']['tickers'], ['NVDA', 'AAPL'])
            self.assertIsNone(rows[0]['answer'])
            self.assertEqual({h['meta']['ticker'] for h in rows[0]['hits']}, {'NVDA', 'AAPL'})
            with patch('sys.argv', argv), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as exc:
                    main()
                self.assertEqual(exc.exception.code, 2)

    def test_chroma_adapter_pagination_and_query_contract(self):
        from src.system_b.adapters import ChromaSource, BGE_PREFIX
        from unittest.mock import Mock
        source = ChromaSource.__new__(ChromaSource)
        source.collection = Mock()
        source.collection.count.return_value = 1
        source.collection.get.return_value = {
            'ids': ['a'], 'documents': ['revenue'], 'metadatas': [{'ticker': 'NVDA', 'fiscal_year': 2026}]}
        self.assertEqual(source.records()[0]['id'], 'a')
        source.embedder = Mock()
        source.embedder.encode.return_value = [[.1, .2]]
        source.collection.query.return_value = {'ids': [['a']], 'distances': [[.2]]}
        scope = Scope(('NVDA',), (2026,))
        self.assertEqual(source('revenue', scope, 30), [('a', .8)])
        source.embedder.encode.assert_called_once_with([BGE_PREFIX + 'revenue'], normalize_embeddings=True)
        self.assertEqual(source.collection.query.call_args.kwargs['n_results'], 1)
        self.assertEqual(source.collection.query.call_args.kwargs['where'], scope.where())


if __name__ == '__main__':
    unittest.main()
