"""Swap one system's rows in reports/rq3/records.jsonl for a fresh run, keeping a backup of the old rows.

Usage:
    python scripts/rq3/replace_system_rows.py --system system_b \
        --new reports/rq3/records_system_b_new.jsonl

Checks that the new run has exactly one ok row for every benchmark question before touching anything.
The old rows are written to reports/rq3/records_<system>_superseded.jsonl.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RECORDS = ROOT / "reports" / "rq3" / "records.jsonl"
BENCHMARK = ROOT / "data" / "benchmark_qa_pool_2015.json"


def read(path):
    return [json.loads(line) for line in open(path) if line.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--system", required=True)
    ap.add_argument("--new", type=Path, required=True)
    args = ap.parse_args()

    expected = {q["id"] for q in json.load(open(BENCHMARK))}
    new = [r for r in read(args.new) if r.get("system") == args.system and r.get("status") == "ok"]
    ids = [r["question_id"] for r in new]
    missing, extra = expected - set(ids), set(ids) - expected
    dupes = {i for i in ids if ids.count(i) > 1}
    if missing or extra or dupes:
        raise SystemExit(f"New run incomplete: missing={sorted(missing)} extra={sorted(extra)} dupes={sorted(dupes)}")

    old = read(RECORDS)
    kept = [r for r in old if r["system"] != args.system]
    superseded = [r for r in old if r["system"] == args.system]
    backup = RECORDS.with_name(f"records_{args.system}_superseded.jsonl")
    with open(backup, "w") as f:
        for r in superseded:
            f.write(json.dumps(r) + "\n")
    with open(RECORDS, "w") as f:
        for r in kept + sorted(new, key=lambda r: r["question_id"]):
            f.write(json.dumps(r) + "\n")
    print(f"{args.system}: replaced {len(superseded)} rows with {len(new)}; total rows {len(kept) + len(new)}; backup {backup.name}")


if __name__ == "__main__":
    main()
