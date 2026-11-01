#!/usr/bin/env python3
"""
Build the compact data bundle the Streamlit demo (app.py) reads from `app_data/`.

Inputs (all committed in the repo):
    reports/rq3/records.jsonl           485 benchmark runs (97 questions x 5 systems)
    reports/rq3/summary_metrics.json    RQ3 scorecard and paired tests (scripts/rq3/evaluate_rq3.py)
    reports/rq1/aggregate.csv           RQ1 retrieval completeness with bootstrap CIs
    data/benchmark_qa_pool_2015.json    gold answers and gold evidence quotes

Outputs:
    app_data/benchmark.json.gz  every question with each system's answer, citations, source chunks and guardrail checks
    app_data/rq1.csv            RQ1 rows for the overall, modality, scope and evidence-count facets
    app_data/rq2.json           RQ2 metrics for all 5 systems, scored on the same runs as RQ3
    app_data/rq3.json           RQ3 scorecard, paired tests and break-even thresholds

Usage:
    python scripts/build_app_data.py
"""

import csv
import gzip
import json
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.rq2.metrics_custom import custom_scores, numeric_accuracy  # noqa: E402
from src.system_c.telemetry import compute_call_cost_usd  # noqa: E402

RECORDS = REPO_ROOT / "reports" / "rq3" / "records.jsonl"
RQ3_SUMMARY = REPO_ROOT / "reports" / "rq3" / "summary_metrics.json"
RQ1_AGGREGATE = REPO_ROOT / "reports" / "rq1" / "aggregate.csv"
POOL = REPO_ROOT / "data" / "benchmark_qa_pool_2015.json"
OUT_DIR = REPO_ROOT / "app_data"

SYSTEMS = ["system_a", "system_b", "system_c_v1", "system_c_v2", "system_c_v3"]
RQ1_FACETS = {"overall", "modality", "scope", "evidence_count"}
RQ2_METRICS = ["numeric_accuracy", "citation_coverage", "citation_precision", "citation_recall", "citation_f1",
               "grounding_error_rate"]
CITED_CHARS = 2400
UNCITED_CHARS = 700

# v3 before error-driven fixes (git a8db615^), see reports/CS614_Group8_System_C_and_RQ3_Final_Report.md §7.2
V3_FIRST_RUN = {"lenient_pct": 90.8, "strict_pct": 73.0, "cost_per_1k_usd": 42.71, "p50_s": 18.6, "mean_hops": 2.03}


def bootstrap_ci(values, n_boot=4000, seed=0):
    arr = np.asarray(values, dtype=float)
    if len(arr) == 0:
        return None, None
    rng = np.random.default_rng(seed)
    means = arr[rng.integers(0, len(arr), (n_boot, len(arr)))].mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def slim_run(rec):
    """One system's answer to one question, with only what the UI renders."""
    cited_ids = {c.get("chunk_id") for c in rec.get("citations") or []}
    contexts = []
    for meta, text in zip(rec.get("contexts_meta") or [], rec.get("retrieved_contexts") or []):
        cid = meta.get("chunk_id")
        limit = CITED_CHARS if cid in cited_ids else UNCITED_CHARS
        contexts.append({**meta, "text": (text or "")[:limit]})
    guard = rec.get("guardrail_report") or None
    if guard:
        guard = {
            "sentences": [
                {k: s.get(k) for k in ("text", "chunk_ids", "numbers", "semantic_verdict", "reason")}
                for s in guard.get("sentences") or []
            ],
            "verified_numbers": guard.get("verified_numbers") or [],
            "ungrounded_numbers": guard.get("ungrounded_numbers") or [],
            "derived_numbers": guard.get("derived_numbers") or [],
            "numerical_grounding_error_rate": guard.get("numerical_grounding_error_rate"),
        }
    tokens = rec.get("tokens") or {}
    strict = numeric_accuracy(rec.get("answer", ""), rec.get("ground_truth_numbers") or [])
    return {
        "answer": rec.get("answer", ""),
        "citations": [{k: c.get(k) for k in ("tag", "chunk_id", "ticker", "fiscal_year", "section")}
                      for c in rec.get("citations") or []],
        "contexts": contexts,
        "guardrail": guard,
        "hops": rec.get("hops", 1),
        "latency_ms": rec.get("latency_ms"),
        "tokens": tokens.get("total", 0),
        "cost_usd": compute_call_cost_usd(rec.get("model") or "", tokens.get("prompt", 0), tokens.get("completion", 0)),
        "lenient_correct": rec.get("numeric_correct"),
        "strict_correct": None if strict is None else strict >= 1.0,
    }


def build_benchmark(records):
    pool = {q["id"]: q for q in json.loads(POOL.read_text(encoding="utf-8"))}
    by_q = {}
    for rec in records:
        by_q.setdefault(rec["question_id"], {})[rec["system"]] = rec
    questions = []
    for qid in sorted(by_q):
        runs = by_q[qid]
        first = next(iter(runs.values()))
        gold = pool.get(qid, {})
        questions.append({
            "id": qid,
            "question": first["question"],
            "type": first.get("type"),
            "recipe": first.get("recipe"),
            "hop": first.get("hop"),
            "category": first.get("category"),
            "gold_answer": first.get("ground_truth_answer"),
            "gold_numbers": first.get("ground_truth_numbers") or [],
            "gold_evidence": [{k: ev.get(k) for k in ("ticker", "year", "item", "heading", "kind", "quote")}
                              for ev in gold.get("gold_evidence") or []],
            "runs": {s: slim_run(runs[s]) for s in SYSTEMS if s in runs},
        })
    return questions


def build_rq2(records):
    out = {}
    for s in SYSTEMS:
        per_metric = {m: [] for m in RQ2_METRICS}
        for rec in (r for r in records if r["system"] == s):
            for metric, (value, status, _) in custom_scores(rec).items():
                if metric in per_metric and status == "ok" and value is not None:
                    per_metric[metric].append(value)
        out[s] = {}
        for metric, vals in per_metric.items():
            lo, hi = bootstrap_ci(vals)
            out[s][metric] = {"n": len(vals), "mean": float(np.mean(vals)) if vals else None, "ci_low": lo, "ci_high": hi}
    return out


def build_rq3():
    summary = json.loads(RQ3_SUMMARY.read_text(encoding="utf-8"))
    systems = summary["systems"]
    cost = {s: systems[s]["economics"]["mean_cost_per_query_usd"] for s in systems}
    strict = {s: systems[s]["accuracy"]["strict_numeric_correct_pct"] / 100.0 for s in systems}
    lenient = {s: systems[s]["accuracy"]["numeric_correct_pct"] / 100.0 for s in systems}

    def threshold(cheap, accurate, acc):
        return (cost[accurate] - cost[cheap]) / (acc[accurate] - acc[cheap])

    summary["break_even_usd"] = {
        "b_to_a_strict": threshold("system_b", "system_a", strict),
        "a_to_v3_strict": threshold("system_a", "system_c_v3", strict),
        "a_to_v3_lenient": threshold("system_a", "system_c_v3", lenient),
    }
    summary["v3_first_run"] = V3_FIRST_RUN
    return summary


def main():
    records = [json.loads(line) for line in RECORDS.read_text(encoding="utf-8").splitlines() if line.strip()]
    OUT_DIR.mkdir(exist_ok=True)

    questions = build_benchmark(records)
    with gzip.open(OUT_DIR / "benchmark.json.gz", "wt", encoding="utf-8") as f:
        json.dump(questions, f, separators=(",", ":"))

    with open(RQ1_AGGREGATE, newline="", encoding="utf-8") as src, open(OUT_DIR / "rq1.csv", "w", newline="", encoding="utf-8") as dst:
        reader = csv.DictReader(src)
        writer = csv.DictWriter(dst, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(row for row in reader if row["facet"] in RQ1_FACETS)

    (OUT_DIR / "rq2.json").write_text(json.dumps(build_rq2(records), indent=1), encoding="utf-8")
    (OUT_DIR / "rq3.json").write_text(json.dumps(build_rq3(), indent=1), encoding="utf-8")
    print(f"Wrote {len(questions)} questions and RQ1/RQ2/RQ3 metrics to {OUT_DIR}")


if __name__ == "__main__":
    main()
