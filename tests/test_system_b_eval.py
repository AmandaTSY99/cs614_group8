import unittest
from scripts.summarize_system_b_eval import reference_f1, summarize
from scripts.judge_system_b_eval import validate_judgment


class SummaryTests(unittest.TestCase):
    def test_judgment_validation(self):
        valid = {'correctness': .5, 'faithfulness': 1, 'citation_support': None,
                 'numerical_accuracy': None, 'reason': 'Partial answer'}
        self.assertEqual(validate_judgment(valid), valid)
        with self.assertRaises(ValueError):
            validate_judgment({**valid, 'faithfulness': 2})
        with self.assertRaises(ValueError):
            validate_judgment({**valid, 'correctness': True})

    def test_word_overlap_is_bounded_and_ignores_citation(self):
        self.assertEqual(reference_f1('Ernst Young 【1】', 'Ernst Young'), 1)
        self.assertEqual(reference_f1('', 'Ernst Young'), 0)
        self.assertAlmostEqual(reference_f1('debt debt', 'debt'), 2/3)

    def test_failure_denominator_and_label_validity(self):
        rows = [
            {'question_id': 'a', 'mode': 'dense', 'status': 'ok', 'answer': 'Claim [9]',
             'ground_truth_answer': 'Claim', 'citations': {'1': 'chunk'},
             'timings': {'total_seconds': 2}, 'usage': {'total_tokens': 10}},
            {'question_id': 'b', 'mode': 'dense', 'status': 'error', 'error': 'rate limit'},
            {'question_id': 'c', 'mode': 'dense', 'status': 'retrieval_only', 'answer': None},
        ]
        summary, per_query = summarize(rows)
        self.assertEqual(summary['dense']['attempts'], 3)
        self.assertEqual(summary['dense']['completed'], 1)
        self.assertEqual(summary['dense']['failures'], 1)
        self.assertEqual(summary['dense']['retrieval_only'], 1)
        self.assertEqual(summary['dense']['answers_with_invalid_citation_labels'], 1)
        self.assertEqual(summary['dense']['total_reported_tokens'], 10)
        self.assertIsNone(per_query[1]['reference_token_f1_proxy'])


if __name__ == '__main__':
    unittest.main()
