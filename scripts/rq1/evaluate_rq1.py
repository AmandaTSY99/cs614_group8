#!/usr/bin/env python3
"""
RQ1: Retrieval completeness of the 4 systems, by question type. One command for the free pipeline:

    Stage 1   score.py          lexical recall@k, recall@all, completeness, average precision
    Stage 1b  score_ragas.py    (optional, LLM judge) RAGAS context recall / precision; run separately
    Stage 2   report.py         bootstrap CIs per system x question-type facet -> aggregate.csv, report.md

Reads pre-generated records (default `reports/rq3/records.jsonl`, 97 questions x 4 systems); never
re-runs the systems. Outputs go to `reports/rq1/`.

Usage:
    docker compose run --rm runner python scripts/rq1/evaluate_rq1.py
"""

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.rq1.common import BENCHMARK_PATH, OUT_DIR, RECORDS_PATH, REPO_ROOT  # noqa: E402
from scripts.rq1.report import build_report  # noqa: E402
from scripts.rq1.score import evaluate_records, score  # noqa: E402,F401  (evaluate_records: public API)


def main() -> None:
    p = argparse.ArgumentParser(description="RQ1 retrieval completeness: score + report.")
    p.add_argument("--benchmark", type=Path, default=BENCHMARK_PATH)
    p.add_argument("--records", type=Path, default=RECORDS_PATH)
    p.add_argument("--out", type=Path, default=OUT_DIR)
    args = p.parse_args()

    q_rows, e_rows = score(args.benchmark, args.records, args.out)
    print(f"Stage 1: scored {len(q_rows)} records ({len(e_rows)} gold evidence items)")
    records_note = str(args.records.resolve().relative_to(REPO_ROOT)) if args.records.resolve().is_relative_to(
        REPO_ROOT) else str(args.records)
    print(build_report(args.out, records_note))
    print(f"Saved: {args.out}")


if __name__ == "__main__":
    main()
