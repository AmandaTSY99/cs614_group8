"""
RQ2 report (`cs614-eval` env): per system x metric mean with bootstrap 95% CI and n, overall and per
category, generation failures per system, and (with `--smoke`) judge usage per metric per sample, the
latest Groq rate-limit headers, and an estimate of free-tier scoring time for a full run.

Usage:
    python scripts/rq2/report.py --run reports/rq2/smoke --smoke --n-samples 120
"""

import argparse
import csv
import random
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.rq2.common import CATEGORIES, GEN_ERRORS_FILE, RECORDS_FILE, SCORES_FILE, read_jsonl  # noqa: E402

METRIC_ORDER = [
    "faithfulness", "answer_relevancy", "context_recall", "context_precision", "factual_correctness",
    "numeric_accuracy", "citation_precision", "citation_recall", "citation_f1", "citation_coverage",
    "grounding_error_rate",
]
LLM_METRICS = METRIC_ORDER[:5]
N_BOOT = 1000
SEED = 0


def bootstrap_ci(values: List[float], n_boot: int = N_BOOT, seed: int = SEED) -> Tuple[float, float]:
    if not values:
        return (float("nan"), float("nan"))
    if len(values) == 1:
        return (values[0], values[0])
    rng = random.Random(seed)
    n = len(values)
    means = sorted(sum(rng.choice(values) for _ in range(n)) / n for _ in range(n_boot))
    return (means[int(0.025 * n_boot)], means[min(n_boot - 1, int(0.975 * n_boot))])


def latest_scores(scores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Last row per (system, question_id, metric): a retried error is replaced by its later result."""
    latest: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
    for row in scores:
        latest[(row["system"], row["question_id"], row["metric"])] = row
    return list(latest.values())


def aggregate(scores: List[Dict[str, Any]], n_boot: int = N_BOOT, seed: int = SEED) -> List[Dict[str, Any]]:
    """One row per (system, category | "overall", metric): n ok, n_na, n_failed, mean, 95% CI."""
    groups: Dict[Tuple[str, str, str], Dict[str, Any]] = defaultdict(lambda: {"values": [], "na": 0, "failed": 0})
    for row in latest_scores(scores):
        for cat in ("overall", row.get("category") or "unknown"):
            g = groups[(row["system"], cat, row["metric"])]
            if row["status"] == "ok" and row.get("value") is not None:
                g["values"].append(float(row["value"]))
            elif row["status"] == "na":
                g["na"] += 1
            else:
                g["failed"] += 1
    out = []
    for (system, cat, metric), g in sorted(groups.items()):
        vals = g["values"]
        low, high = bootstrap_ci(vals, n_boot, seed)
        out.append({
            "system": system, "category": cat, "metric": metric, "n": len(vals), "n_na": g["na"],
            "n_failed": g["failed"], "mean": sum(vals) / len(vals) if vals else None,
            "ci_low": low if vals else None, "ci_high": high if vals else None,
        })
    return out


def generation_failures(records: List[Dict[str, Any]], gen_errors: List[Dict[str, Any]]) -> Dict[str, int]:
    """Per system: questions with a generation error and no successful record."""
    ok = {(r["system"], r["question_id"]) for r in records}
    failed: Dict[str, set] = defaultdict(set)
    for e in gen_errors:
        if (e["system"], e["question_id"]) not in ok:
            failed[e["system"]].add(e["question_id"])
    systems = {r["system"] for r in records} | {e["system"] for e in gen_errors}
    return {s: len(failed.get(s, set())) for s in sorted(systems)}


def judge_usage(scores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Judge calls and tokens per metric per sample (LLM metrics only)."""
    rows = []
    for r in latest_scores(scores):
        if r["metric"] not in LLM_METRICS:
            continue
        rows.append({
            "system": r["system"], "question_id": r["question_id"], "metric": r["metric"], "status": r["status"],
            "calls": r.get("judge_calls", 0), "prompt_tokens": r.get("judge_prompt_tokens", 0),
            "completion_tokens": r.get("judge_completion_tokens", 0),
        })
    return sorted(rows, key=lambda x: (x["system"], x["question_id"], LLM_METRICS.index(x["metric"])))


def latest_ratelimit(scores: List[Dict[str, Any]]) -> Dict[str, str]:
    for r in reversed(sorted(scores, key=lambda x: x.get("timestamp", ""))):
        if r.get("ratelimit"):
            return r["ratelimit"]
    return {}


def _num(v: Any) -> Optional[float]:
    try:
        return float(str(v).strip())
    except (TypeError, ValueError):
        return None


def estimate_free_tier(
    usage: List[Dict[str, Any]],
    ratelimit: Dict[str, str],
    n_samples: int = 120,
    tokens_per_day: Optional[float] = None,
    requests_per_day: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Scale the smoke test's judge calls/tokens per sample to `n_samples` and divide by the daily limits.
    Groq headers give `x-ratelimit-limit-requests` (requests per day) and `x-ratelimit-limit-tokens`
    (tokens per minute); a daily token cap is not in the headers, so it can be passed as `tokens_per_day`.
    """
    samples = {(u["system"], u["question_id"]) for u in usage}
    if not samples:
        return {"samples_measured": 0}
    calls = sum(u["calls"] for u in usage)
    tokens = sum(u["prompt_tokens"] + u["completion_tokens"] for u in usage)
    per_sample_calls = calls / len(samples)
    per_sample_tokens = tokens / len(samples)
    total_calls = per_sample_calls * n_samples
    total_tokens = per_sample_tokens * n_samples
    rpd = requests_per_day or _num(ratelimit.get("x-ratelimit-limit-requests"))
    tpm = _num(ratelimit.get("x-ratelimit-limit-tokens"))
    est = {
        "samples_measured": len(samples),
        "calls_per_sample": per_sample_calls,
        "tokens_per_sample": per_sample_tokens,
        "n_samples": n_samples,
        "total_calls": total_calls,
        "total_tokens": total_tokens,
        "requests_per_day_limit": rpd,
        "tokens_per_minute_limit": tpm,
        "tokens_per_day_limit": tokens_per_day,
        "days_by_requests": total_calls / rpd if rpd else None,
        "days_by_tokens_per_day": total_tokens / tokens_per_day if tokens_per_day else None,
        "minutes_by_tokens_per_minute": total_tokens / tpm if tpm else None,
    }
    days = [d for d in (est["days_by_requests"], est["days_by_tokens_per_day"]) if d is not None]
    est["estimated_days"] = max(days) if days else None
    return est


def _fmt(row: Optional[Dict[str, Any]]) -> str:
    if not row or row["mean"] is None:
        return "N/A (n=0)" if row is None else f"N/A (n=0, na={row['n_na']})"
    extra = f", failed={row['n_failed']}" if row["n_failed"] else ""
    return f"{row['mean']:.3f} [{row['ci_low']:.3f}, {row['ci_high']:.3f}] (n={row['n']}{extra})"


def render_report(
    records: List[Dict[str, Any]],
    scores: List[Dict[str, Any]],
    gen_errors: List[Dict[str, Any]],
    agg: List[Dict[str, Any]],
    smoke: Optional[Dict[str, Any]] = None,
) -> str:
    systems = sorted({r["system"] for r in records} | {e["system"] for e in gen_errors})
    judges = sorted({r["judge"] for r in scores if r.get("metric") in LLM_METRICS and r.get("judge")})
    failures = generation_failures(records, gen_errors)
    index = {(a["system"], a["category"], a["metric"]): a for a in agg}

    lines = ["# RQ2 results", ""]
    lines.append(f"Judge: {', '.join(judges) if judges else 'none (custom metrics only)'}. "
                 "Cells: mean [bootstrap 95% CI] (n scored; na and failed rows excluded).")
    lines.append("")
    lines.append("## Generation")
    lines.append("")
    lines.append("| System | Records | Failed to generate |")
    lines.append("|---|---|---|")
    for s in systems:
        lines.append(f"| {s} | {sum(r['system'] == s for r in records)} | {failures.get(s, 0)} |")
    for cat in ["overall"] + CATEGORIES:
        lines += ["", f"## {cat}", "", "| Metric | " + " | ".join(systems) + " |",
                  "|---|" + "---|" * len(systems)]
        for metric in METRIC_ORDER:
            cells = [_fmt(index.get((s, cat, metric))) for s in systems]
            if all(c.startswith("N/A (n=0)") and "na=" not in c for c in cells):
                continue
            lines.append(f"| {metric} | " + " | ".join(cells) + " |")
    lines += [
        "", "## Notes", "",
        "- Context Precision is order-sensitive: it rewards relevant contexts ranked early. "
        "`retrieved_contexts` are kept in the order each system produced them (System C: retrieval order "
        "across hops, with v2's XBRL blocks first).",
        "- Citation precision/recall/F1 are section-level (top-level 10-K item, `financials.csv` = any "
        "`[F-…]` citation), because the golden set has no gold chunk IDs. Answers with no citations are N/A, "
        "not 0; `citation_coverage` is the share of answers with at least one citation.",
        "- RAGAS metrics see the answer with citation tags stripped.",
    ]
    if smoke:
        lines += ["", "## Smoke test: judge usage", "",
                  "| System | Question | Metric | Status | Calls | Prompt tok | Completion tok |",
                  "|---|---|---|---|---|---|---|"]
        for u in smoke["usage"]:
            lines.append(f"| {u['system']} | {u['question_id']} | {u['metric']} | {u['status']} | {u['calls']} | "
                         f"{u['prompt_tokens']} | {u['completion_tokens']} |")
        lines += ["", "Latest rate-limit headers: " + (", ".join(f"`{k}: {v}`" for k, v in
                                                                 sorted(smoke["ratelimit"].items())) or "none returned")]
        e = smoke["estimate"]
        if e.get("samples_measured"):
            lines += ["", f"Estimate for {e['n_samples']} samples: {e['calls_per_sample']:.1f} calls and "
                          f"{e['tokens_per_sample']:,.0f} tokens per sample -> {e['total_calls']:,.0f} calls, "
                          f"{e['total_tokens']:,.0f} tokens."]
            for label, key in (("Days by request/day limit", "days_by_requests"),
                               ("Days by token/day limit", "days_by_tokens_per_day"),
                               ("Minutes of token/minute budget", "minutes_by_tokens_per_minute")):
                if e.get(key) is not None:
                    lines.append(f"- {label}: {e[key]:.2f}")
            lines.append(f"- Estimated days: {e['estimated_days']:.2f}" if e.get("estimated_days") is not None
                         else "- Estimated days: unknown (no daily limit in headers; pass --tpd / --rpd)")
    return "\n".join(lines) + "\n"


def write_aggregate_csv(path: Path, agg: List[Dict[str, Any]]) -> None:
    fields = ["system", "category", "metric", "n", "n_na", "n_failed", "mean", "ci_low", "ci_high"]
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(agg)


def build_report(run_path: Path, scores_file: str = SCORES_FILE, smoke: bool = False, n_samples: int = 120,
                 tokens_per_day: Optional[float] = None, requests_per_day: Optional[float] = None) -> str:
    records = read_jsonl(run_path / RECORDS_FILE)
    scores = read_jsonl(run_path / scores_file)
    gen_errors = read_jsonl(run_path / GEN_ERRORS_FILE)
    agg = aggregate(scores)
    smoke_info = None
    if smoke:
        usage = judge_usage(scores)
        ratelimit = latest_ratelimit(scores)
        smoke_info = {"usage": usage, "ratelimit": ratelimit,
                      "estimate": estimate_free_tier(usage, ratelimit, n_samples, tokens_per_day, requests_per_day)}
    text = render_report(records, scores, gen_errors, agg, smoke_info)
    (run_path / "report.md").write_text(text, encoding="utf-8")
    write_aggregate_csv(run_path / "aggregate.csv", agg)
    return text


def main() -> None:
    p = argparse.ArgumentParser(description="RQ2 report: aggregates, CIs, generation failures, smoke usage.")
    p.add_argument("--run", required=True)
    p.add_argument("--scores-file", default=SCORES_FILE)
    p.add_argument("--smoke", action="store_true", help="Add judge usage, rate limits and a free-tier estimate.")
    p.add_argument("--n-samples", type=int, default=120, help="Samples in the full run (System C v1 + v2 = 120).")
    p.add_argument("--tpd", type=float, default=None, help="Judge tokens-per-day limit, if known.")
    p.add_argument("--rpd", type=float, default=None, help="Override requests-per-day limit.")
    args = p.parse_args()
    print(build_report(Path(args.run), args.scores_file, args.smoke, args.n_samples, args.tpd, args.rpd))


if __name__ == "__main__":
    main()
