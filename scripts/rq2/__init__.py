"""
RQ2 evaluation harness (workplan Section 4.4).

Stage 1 `generate.py` runs the systems (main `cs614` env, never imports ragas) and writes `records.jsonl`.
Stage 2 `score.py` / `report.py` run in the `cs614-eval` env (ragas) and read only the JSONL files.
"""
