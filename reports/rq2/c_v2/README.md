# RQ2: System C v2

RQ2 scores for System C v2 (97 questions), added so that Section 4.5 of the report covers all five systems.

- Answers: system_c_v2 rows from `reports/rq3/records.jsonl` (dev), unchanged.
- Scoring: `scripts/rq2/score.py` with the same settings as `reports/rq2/full_v3`. RAGAS judge openai/gpt-4o-mini at temperature 0; factual correctness in recall mode against the answer key points, low atomicity; rows truncated at the default judge limit re-scored at 8,192 tokens.
- Check: the judge-free metrics reproduce the values from an independent run (accuracy 0.779, refusal rate 0.062, citation coverage 0.969, citation precision 0.851).

Overall results (mean, n): primary accuracy 0.779 (97), faithfulness 0.745 (91; refusals excluded), answer relevancy 0.713 (97), context recall 0.726 (97), context precision 0.638 (97), factual correctness 0.483 (97), refusal rate 0.062 (97), citation coverage 0.969 (97), citation precision 0.851 (94).
