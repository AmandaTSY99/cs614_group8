"""
RQ2 report (`cs614-eval` env): per system x metric mean with bootstrap 95% CI and n, overall and per
category, generation failures per system, and (with `--smoke`) judge usage per metric per sample, the
latest Groq rate-limit headers, and an estimate of free-tier scoring time for a full run.

Usage:
    python scripts/rq2/report.py --run reports/rq2/smoke --smoke --n-samples 120
"""

import argparse
import csv
import itertools
import random
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.rq2 import analysis as A  # noqa: E402
from scripts.rq2 import judge as J  # noqa: E402
from scripts.rq2 import retrieval_stats as RS  # noqa: E402
from scripts.rq2.common import (  # noqa: E402
    CATEGORIES, GEN_ERRORS_FILE, RECORDS_FILE, SCORES_FILE, benchmark_index, read_jsonl,
)
from scripts.rq2.judge import EMBEDDING_MODEL  # noqa: E402

METRIC_ORDER = [
    "primary_accuracy", "abstained",
    "faithfulness", "answer_relevancy", "context_recall", "context_precision", "factual_correctness",
    "numeric_accuracy", "citation_precision", "citation_recall", "citation_f1", "citation_coverage",
    "citation_precision_incl_uncited", "citation_recall_incl_uncited", "citation_f1_incl_uncited",
    "grounding_error_rate",
]
METRIC_LABELS = {
    "primary_accuracy": "primary_accuracy (numeric_accuracy / keypoint_recall)",
    "abstained": "abstained (refusal rate)",
    "factual_correctness": "factual_correctness (secondary)",
    "citation_precision_incl_uncited": "citation_precision, uncited = 0",
    "citation_recall_incl_uncited": "citation_recall, uncited = 0",
    "citation_f1_incl_uncited": "citation_f1, uncited = 0",
}
# The RQ2 proposal's question attributes (`dims` on each score row), reported as extra groups "dim=value".
DIMENSIONS = A.DIMENSIONS
LLM_METRICS = ["faithfulness", "answer_relevancy", "context_recall", "context_precision", "factual_correctness"]
FC_TAG_RE = re.compile(r"fc_mode=(\w+); fc_reference=(\w+)(?:; fc_atomicity=(\w+))?")
N_BOOT = 1000
SEED = 0
# gpt-4o-mini list prices (USD per 1M tokens); override with --price-in / --price-out.
PRICE_IN_PER_M = 0.15
PRICE_OUT_PER_M = 0.60


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
        dims = row.get("dims") or {}
        dim_groups = [f"{d}={dims[d]}" for d in DIMENSIONS if dims.get(d)]
        for cat in ("overall", row.get("category") or "unknown", *dim_groups):
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


def per_metric_usage(usage: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
    """Mean judge calls / prompt / completion tokens per sample for each metric, over completed rows."""
    out: Dict[str, Dict[str, float]] = {}
    for metric in LLM_METRICS:
        rows = [u for u in usage if u["metric"] == metric and u["status"] == "ok"]
        if rows:
            out[metric] = {k: sum(u[k] for u in rows) / len(rows) for k in ("calls", "prompt_tokens", "completion_tokens")}
            out[metric]["n"] = len(rows)
    return out


def estimate_cost(usage: List[Dict[str, Any]], n_samples: int, price_in_per_m: float,
                  price_out_per_m: float) -> Dict[str, Any]:
    """Projected judge cost for `n_samples` from per-metric mean tokens of completed rows."""
    per_metric = per_metric_usage(usage)
    p = sum(m["prompt_tokens"] for m in per_metric.values())
    c = sum(m["completion_tokens"] for m in per_metric.values())
    per_sample = (p * price_in_per_m + c * price_out_per_m) / 1e6
    return {"prompt_tokens_per_sample": p, "completion_tokens_per_sample": c, "cost_per_sample_usd": per_sample,
            "n_samples": n_samples, "total_cost_usd": per_sample * n_samples,
            "price_in_per_m": price_in_per_m, "price_out_per_m": price_out_per_m,
            "metrics_measured": sorted(per_metric)}


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
    # Per-metric averages over rows that completed, summed over metrics: rate-limited or failed rows
    # would otherwise drag the per-sample cost down.
    ok = [u for u in usage if u["status"] == "ok"]
    samples = {(u["system"], u["question_id"]) for u in ok}
    if not samples:
        return {"samples_measured": 0}
    per_metric = per_metric_usage(usage)
    per_sample_calls = sum(m["calls"] for m in per_metric.values())
    per_sample_tokens = sum(m["prompt_tokens"] + m["completion_tokens"] for m in per_metric.values())
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


LIMITATIONS = [
    "", "## Limitations", "",
    "- **Factual correctness is a secondary metric.** On a 20-answer canary it agreed only moderately with the "
    "saved correctness flags (mean absolute difference 0.28), because (1) its recall also counts the answer's "
    "extra correct claims (intermediate figures the reference does not contain), (2) the judge is confused by "
    "the sign of the gold number (\"-30.36%\" is marked wrong for an answer saying a 30.36% decrease, and the "
    "reverse), and (3) it splits one condition (\"probable AND reasonably estimable\") into separate claims "
    "that are then judged one by one.",
    "- **Faithfulness cannot verify a number the system calculated itself** (e.g. 30.36%), since it is not in "
    "any retrieved text; correct calculations are therefore slightly penalised.",
    "- **The judge is not fully repeatable at temperature 0**: repeated scoring of the same answer gave "
    "different values on the canary.",
    "- **Refusal detection is a rule**: an answer is a refusal when its first sentence says the evidence is "
    "missing (\"not found in the provided context\", \"cannot be determined\", ...). Partial answers are not "
    "refusals. The rule treats some partial \"I can only answer part of this\" replies inconsistently (e.g. A "
    "gold-045 is flagged, A gold-071 is not), so refusal counts may be off by a few for A.",
    "- **Numeric matching is a rule**: it accepts accounting negatives (\"(6.0)\", \"$(316)\"), a bare table figure "
    "against a gold value with a unit (\"$316\" for \"$316 million\", exact digits, at least 3 significant digits), "
    "the unsigned value of a negative gold number, and ratio / percentage equivalents (\"72.08%\" for \"0.72\") "
    "within a 0.5% relative tolerance. A wrong sign or a wrong unit is therefore not caught. The remaining "
    "disagreements with the saved `numeric_correct` flags are listed under \"Numeric accuracy vs the saved "
    "correctness flags\".",
    f"- **Error types are heuristic.** {A.ERROR_TYPE_RULE}",
    "- **System C v3 may have been tuned on this benchmark** (built after it existed, reports 100% numerical "
    "accuracy on it), so its numbers may be optimistic.",
    "- **The judge (gpt-4o-mini) is weaker than the answer model (gpt-5.4)**; a stronger-judge spot-check is "
    "planned.",
    "- **The answer model is labelled both `gpt-5.4` and `gpt-5.4-2026-03-05`** in the records; most likely "
    "the same model reported two ways.",
    "- **Keypoint recall is word overlap**, not meaning: a paraphrase can miss a key point, and a long answer "
    "can cover one by chance.",
    "- Paired differences use the same questions for both systems; with 97 questions, small per-attribute "
    "groups have wide intervals, and p-values are Holm-corrected only across the 6 system pairs of one metric "
    "and group, not across metrics or groups.",
]


def _fc_config(scores: List[Dict[str, Any]]) -> str:
    for r in scores:
        m = FC_TAG_RE.search(str(r.get("detail") or "")) if r.get("metric") == "factual_correctness" else None
        if m:
            return f"mode `{m.group(1)}`, reference `{m.group(2)}`, atomicity `{m.group(3) or 'low'}`"
    return "mode `f1`, reference `answer_keypoints`, atomicity `low` (defaults; not recorded in this scores file)"


def _judge_limit_config(scores: List[Dict[str, Any]]) -> Optional[str]:
    rescored = [r for r in latest_scores(scores) if r.get("judge_max_tokens")]
    if not rescored:
        return None
    limits = sorted({int(r["judge_max_tokens"]) for r in rescored})
    return (f"Judge output limit: the ragas default ({J.RAGAS_DEFAULT_MAX_TOKENS} tokens) for most rows; "
            f"{', '.join(str(n) for n in limits)} tokens for the {len(rescored)} rows that were truncated at the "
            "default and re-scored (`judge_max_tokens` in each such row's `detail`). The output limit only caps how "
            "long the judge's structured answer may be; model, temperature and prompts are identical, so it does "
            "not affect rows that completed under the lower limit.")


def failed_to_score(scores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Rows excluded from the means: status error / truncated / too_large, per system, metric and status."""
    groups: Dict[Tuple[str, str, str], List[str]] = defaultdict(list)
    for r in latest_scores(scores):
        if r.get("status") in ("error", J.STATUS_TRUNCATED, J.STATUS_TOO_LARGE):
            groups[(r["system"], r["metric"], r["status"])].append(r["question_id"])
    return [{"system": s, "metric": m, "status": st, "count": len(q), "questions": sorted(q)}
            for (s, m, st), q in sorted(groups.items())]


def _failed_section(scores: List[Dict[str, Any]]) -> List[str]:
    failed = failed_to_score(scores)
    lines = ["", "## Failed to score", ""]
    if not failed:
        return lines + ["No judge rows failed: every LLM metric was scored for every answer (N/A rows excluded)."]
    lines += ["These rows have no value and are excluded from the means above (shown as `failed=n` there). "
              "`truncated`: the judge's answer exceeded its output limit even at the highest limit tried; "
              "`error`: the call failed after all retries; `too_large`: the request exceeded the context window.",
              "", "| System | Metric | Status | Count | Questions |", "|---|---|---|---|---|"]
    for f in failed:
        lines.append(f"| {f['system']} | {f['metric']} | {f['status']} | {f['count']} | {', '.join(f['questions'])} |")
    return lines


def _sig(row: Dict[str, Any]) -> str:
    return "yes" if row["significant"] else "no"


def _pair_label(row: Dict[str, Any]) -> str:
    return f"{row['system_a']} → {row['system_b']}"


def _diff_cell(row: Dict[str, Any]) -> str:
    return f"{row['mean_diff']:+.3f} [{row['ci_low']:+.3f}, {row['ci_high']:+.3f}]"


def _retrieval_sections(analysis: Dict[str, Any]) -> List[str]:
    lines: List[str] = []
    refusals = analysis.get("refusal_retrieval") or []
    if refusals:
        lines += ["", "## Refusals and retrieval", "",
                  "For every answer the gold evidence quotes of its question (benchmark `gold_evidence`) are checked "
                  "against the retrieved contexts of that system: *all* = every quote is in a retrieved chunk of the "
                  "gold filing (normalised substring, or at least 80% of the words of a quote of 15+ words); *some* = "
                  "at least one but not all; *none*. *Lenient* additionally accepts any quote of which 60% of the words "
                  "are in a chunk of that filing.", "",
                  "| System | Refusals | Evidence all | some | none | All, lenient | Answered | Evidence all | some | none | All, lenient |",
                  "|---|---|---|---|---|---|---|---|---|---|---|"]
        for r in refusals:
            lines.append(f"| {r['system']} | {r['refusals']} | {r['refusals_full_evidence']} | "
                         f"{r['refusals_partial_evidence']} | {r['refusals_no_evidence']} | "
                         f"{r['refusals_full_evidence_lenient']} | {r['answered']} | {r['answered_full_evidence']} | "
                         f"{r['answered_partial_evidence']} | {r['answered_no_evidence']} | "
                         f"{r['answered_full_evidence_lenient']} |")
        a, b = (next((r for r in refusals if r["system"] == s), None) for s in ("system_a", "system_b"))
        if a and b:
            lines += ["", f"Refusals mostly follow incomplete retrieval: the gold evidence was fully present for only "
                          f"{b['refusals_full_evidence']} of B's {b['refusals']} refusals and "
                          f"{a['refusals_full_evidence']} of A's {a['refusals']} (lenient matching: "
                          f"{b['refusals_full_evidence_lenient']} and {a['refusals_full_evidence_lenient']}); "
                          f"it was fully present for {b['answered_full_evidence']} of B's {b['answered']} and "
                          f"{a['answered_full_evidence']} of A's {a['answered']} answered questions."]
    context = analysis.get("retrieval_context") or []
    if context:
        lines += ["", "## Retrieval context per system", "",
                  "| System | Answers | Mean chunks | Mean characters | Mean hops | 1 hop | 2 hops | 3 hops |",
                  "|---|---|---|---|---|---|---|---|"]
        for c in context:
            lines.append(f"| {c['system']} | {c['answers']} | {c['mean_chunks']:.1f} | {c['mean_context_chars']:,.0f} | "
                         f"{c['mean_hops']:.2f} | {c['hops_1']} | {c['hops_2']} | {c['hops_3']} |")
        by = {c["system"]: c for c in context}
        comps = {(c["metric"], c["system_a"], c["system_b"]): c for c in analysis["comparisons"] if c["group"] == "overall"}
        if "system_c_v1" in by and "system_c_v3" in by:
            def cell(metric: str) -> str:
                c = comps.get((metric, "system_c_v1", "system_c_v3"))
                return "n/a" if c is None else (f"{c['mean_diff']:+.3f}, "
                                                f"{'significant' if c['significant'] else 'not significant'}")

            v1, v3 = by["system_c_v1"], by["system_c_v3"]
            lines += ["", "**C v1 vs C v3** (paired differences, C v3 minus C v1): "
                          f"answer relevancy {cell('answer_relevancy')}; faithfulness {cell('faithfulness')}; "
                          f"context recall {cell('context_recall')}; context precision {cell('context_precision')}. "
                          f"C v3 stops after one hop in {v3['hops_1']} of {v3['answers']} answers (C v1: "
                          f"{v1['hops_1']}) and passes more chunks to the answer model "
                          f"({v3['mean_chunks']:.1f} vs {v1['mean_chunks']:.1f} on average)."]
    agreement = analysis.get("numeric_agreement")
    if agreement:
        lines += ["", "## Numeric accuracy vs the saved correctness flags", "",
                  f"`numeric_accuracy` agrees with the RQ3 harness flag `numeric_correct` on {agreement['agree']} of "
                  f"{agreement['total']} answers with a gold number "
                  f"({', '.join(f'{s}: {a}/{t}' for s, (a, t) in sorted(agreement['per_system'].items()))})."]
        if agreement["disagreements"]:
            lines += ["", "| Question | System | Gold | numeric_accuracy | Saved flag | Answer excerpt |",
                      "|---|---|---|---|---|---|"]
            for d in agreement["disagreements"]:
                excerpt = d["answer"].replace("\n", " ").replace("|", "/")[:160]
                lines.append(f"| {d['question_id']} | {d['system']} | {', '.join(map(str, d['gold'] or []))} | "
                             f"{d['numeric_accuracy']:.0f} | {d['numeric_correct']} | {excerpt} |")
    return lines


def _analysis_sections(analysis: Dict[str, Any], systems: List[str]) -> List[str]:
    lines: List[str] = []
    comparisons = analysis["comparisons"]
    ordering = analysis["ordering"]
    n_pairs = len(systems) * (len(systems) - 1) // 2

    lines += ["", "## Expected ordering on primary accuracy", "",
              f"Expected: {' < '.join(ordering['order'])} (a later system scores higher). Paired differences "
              f"(second minus first) on the same questions, 95% paired bootstrap CI ({A.N_BOOT_PAIRED} "
              f"resamples, seed {A.SEED}), Wilcoxon signed-rank p-value, Holm-corrected across the "
              f"{n_pairs} pairs.", "",
              "| Pair | n | Mean first | Mean second | Difference [95% CI] | p (Holm) | Significant | Verdict |",
              "|---|---|---|---|---|---|---|---|"]
    for r in ordering["rows"]:
        lines.append(f"| {_pair_label(r)} | {r['n']} | {r['mean_a']:.3f} | {r['mean_b']:.3f} | {_diff_cell(r)} | "
                     f"{r['p_holm']:.4f} | {_sig(r)} | {r['verdict']} |")
    lines += ["", "The full expected ordering " + ("**holds**: every adjacent pair is significantly in the expected "
                                                    "direction." if ordering["ordering_holds"]
                                                    else "**does not hold**: at least one adjacent pair is not "
                                                         "significantly in the expected direction.")]

    lines += ["", "## Paired comparisons (overall, all metrics)", "",
              "Difference = second minus first, mean [95% CI]; * = significant after Holm correction "
              "(p < 0.05). Per attribute: `paired_comparisons.csv`.", "",
              "| Metric | " + " | ".join(f"{a.replace('system_', '')} → {b.replace('system_', '')}"
                                          for a, b in itertools_pairs(systems)) + " |",
              "|---|" + "---|" * n_pairs]
    overall = {(c["metric"], c["system_a"], c["system_b"]): c for c in comparisons if c["group"] == "overall"}
    for metric in METRIC_ORDER:
        cells = []
        for a, b in itertools_pairs(systems):
            c = overall.get((metric, a, b))
            cells.append("n/a" if c is None else f"{c['mean_diff']:+.3f}{'*' if c['significant'] else ''}")
        if any(cell != "n/a" for cell in cells):
            lines.append(f"| {METRIC_LABELS.get(metric, metric)} | " + " | ".join(cells) + " |")

    sig = [c for c in comparisons if c["significant"] and c["group"] != "overall"
           and not c["group"].startswith("category=") and c["metric"] in METRIC_ORDER]
    lines += ["", "## Significant paired differences by question attribute", ""]
    if sig:
        lines += ["| Group | Metric | Pair | n | Difference [95% CI] | p (Holm) |", "|---|---|---|---|---|---|"]
        for c in sorted(sig, key=lambda c: (c["group"], METRIC_ORDER.index(c["metric"]), c["system_a"], c["system_b"])):
            lines.append(f"| {c['group']} | {METRIC_LABELS.get(c['metric'], c['metric'])} | {_pair_label(c)} | "
                         f"{c['n']} | {_diff_cell(c)} | {c['p_holm']:.4f} |")
    else:
        lines.append("None.")

    counts = analysis["error_counts"]
    lines += ["", "## Error types", "", A.ERROR_TYPE_RULE, ""]
    groups = sorted({c["group"] for c in counts},
                    key=lambda g: (-1 if g == "overall" else (A.DIMENSIONS.index(g.split("=")[0])
                                                              if g.split("=")[0] in A.DIMENSIONS else 99), g))
    for group in groups:
        lines += [f"### {group}", "", "| System | Answers | Wrong | " + " | ".join(A.ERROR_TYPES) + " |",
                  "|---|---|---|" + "---|" * len(A.ERROR_TYPES)]
        for c in (c for c in counts if c["group"] == group):
            cells = [f"{c[t]} ({c[t + '_share']:.0%})" if c[t + "_share"] is not None else "–" for t in A.ERROR_TYPES]
            lines.append(f"| {c['system']} | {c['answers']} | {c['wrong']} | " + " | ".join(cells) + " |")
        lines.append("")
    lines.append("Cells: count (share of that system's wrong answers).")
    lines += _retrieval_sections(analysis)
    return lines


def itertools_pairs(systems: List[str]) -> List[Any]:
    return list(itertools.combinations(systems, 2))


def render_report(
    records: List[Dict[str, Any]],
    scores: List[Dict[str, Any]],
    gen_errors: List[Dict[str, Any]],
    agg: List[Dict[str, Any]],
    smoke: Optional[Dict[str, Any]] = None,
    analysis: Optional[Dict[str, Any]] = None,
) -> str:
    systems = A.order_systems({r["system"] for r in records} | {e["system"] for e in gen_errors})
    judges = sorted({r["judge"] for r in scores if r.get("metric") in LLM_METRICS and r.get("judge")})
    failures = generation_failures(records, gen_errors)
    index = {(a["system"], a["category"], a["metric"]): a for a in agg}

    answer_models = sorted({f"{r.get('provider')}/{r.get('model')}" for r in records})
    lines = ["# RQ2 results", ""]
    lines.append(f"Judge: {', '.join(judges) if judges else 'none (custom metrics only)'}. "
                 "Cells: mean [bootstrap 95% CI] (n scored; na and failed rows excluded).")
    lines += [
        "", "## Configuration", "",
        f"- RAGAS judge: {', '.join(judges) if judges else 'none'}, temperature 0 "
        "(`EVAL_JUDGE_PROVIDER` / `EVAL_JUDGE_MODEL`; one judge per scores file).",
        f"- Factual correctness (SECONDARY metric): {_fc_config(scores)}.",
        *([f"- {_judge_limit_config(scores)}"] if _judge_limit_config(scores) else []),
        "- Primary accuracy: numeric questions use `numeric_accuracy`; qualitative and mixed questions use the "
        "saved `keypoint_recall` (rule-based, no LLM: `keypoint_recall` in `src/system_a/evaluate.py`, stored on "
        "each record by `scripts/rq3/run_rq3_experiment.py`; the share of a question's key points of which at "
        "least half of the content words appear in the answer). The refusal rate (`abstained`) is shown beside it.",
        f"- Answer relevancy embeddings: local `{EMBEDDING_MODEL}` (sentence-transformers, CPU).",
        f"- Answer model(s): {', '.join(answer_models) if answer_models else 'n/a'}.",
        "- System C's own guardrail judge: for the full run it is set to OpenAI `gpt-4o-mini` via env vars "
        "during generation (`GUARDRAIL_JUDGE_PROVIDER=openai`, `GUARDRAIL_JUDGE_MODEL=gpt-4o-mini`); the smoke "
        "run used the `.env` setting (Groq `openai/gpt-oss-120b`).",
    ]
    lines.append("")
    lines.append("## Generation")
    lines.append("")
    lines.append("| System | Records | Failed to generate |")
    lines.append("|---|---|---|")
    for s in systems:
        lines.append(f"| {s} | {sum(r['system'] == s for r in records)} | {failures.get(s, 0)} |")
    dim_groups = sorted({a["category"] for a in agg if "=" in a["category"]},
                        key=lambda g: (DIMENSIONS.index(g.split("=")[0]) if g.split("=")[0] in DIMENSIONS else 99, g))
    for cat in ["overall"] + CATEGORIES + dim_groups:
        lines += ["", f"## {cat}", "", "| Metric | " + " | ".join(systems) + " |",
                  "|---|" + "---|" * len(systems)]
        for metric in METRIC_ORDER:
            cells = [_fmt(index.get((s, cat, metric))) for s in systems]
            if all(c.startswith("N/A (n=0)") and "na=" not in c for c in cells):
                continue
            lines.append(f"| {METRIC_LABELS.get(metric, metric)} | " + " | ".join(cells) + " |")
    lines += _failed_section(scores)
    if analysis:
        lines += _analysis_sections(analysis, systems)
    lines += [
        "", "## Notes", "",
        "- Context Precision is order-sensitive: it rewards relevant contexts ranked early. "
        "`retrieved_contexts` are kept in the order each system produced them (System C: retrieval order "
        "across hops).",
        "- Citation precision/recall/F1 are section-level (top-level 10-K item, `financials.csv` = any "
        "`[F-…]` citation), because the benchmark has no gold chunk IDs. Answers with no citations are N/A, "
        "not 0, so those rows use citing answers only; `citation_coverage` (the share of answers with at least "
        "one citation) is always shown beside them, and the `uncited = 0` rows count an answer without "
        "citations as 0.",
        "- Section aliases (a limitation of section-level matching): a cited `Item 15` chunk that is financial "
        "statements or notes counts as `Item 8`, and a cover-page chunk (no Item heading; registrant name, "
        "address, file number) counts as `Item 1`, matching how the benchmark labels those facts.",
        "- RAGAS metrics see the answer with citation tags stripped.",
        "- Refusals (\"Not found in the provided context\", \"cannot be determined\", ...) are counted by "
        "`abstained`. They are N/A for faithfulness (no claims to check) and score 0 for factual correctness, "
        "instead of the 1.0 RAGAS would give a claim-free answer.",
        "- RAGAS references come from the benchmark: factual correctness uses the reference named in the "
        "configuration; context recall / precision use the gold evidence quotes plus the gold answer, because a "
        "computed answer such as \"-30.36%\" does not appear in any filing. A bare negative gold number is "
        "also written as a decrease.",
        "- Numeric accuracy accepts the unsigned value of a negative gold number (\"-25.64%\" matches "
        "\"decreased by 25.6%\", 0.5% relative tolerance), so a wrong sign is not caught.",
        "- Categories: multi_company_comparison is only questions across companies; one company across years "
        "is cross_section_multihop. `dim=value` sections use the proposal's attributes from the benchmark: "
        "answer_type (type), evidence_format (recipe), hop, task (calculation when the gold has a program), "
        "evidence_scope (scope).",
    ]
    lines += LIMITATIONS
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
        c = smoke.get("cost")
        if c and c["metrics_measured"]:
            lines += ["", f"Projected judge cost for {c['n_samples']} samples at ${c['price_in_per_m']}/M input and "
                          f"${c['price_out_per_m']}/M output tokens: {c['prompt_tokens_per_sample']:,.0f} + "
                          f"{c['completion_tokens_per_sample']:,.0f} tokens per sample, "
                          f"${c['cost_per_sample_usd']:.4f} per sample, ${c['total_cost_usd']:.2f} total "
                          f"(metrics measured: {', '.join(c['metrics_measured'])})."]
    return "\n".join(lines) + "\n"


def write_aggregate_csv(path: Path, agg: List[Dict[str, Any]]) -> None:
    fields = ["system", "category", "metric", "n", "n_na", "n_failed", "mean", "ci_low", "ci_high"]
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(agg)


def write_dict_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def build_report(run_path: Path, scores_file: str = SCORES_FILE, smoke: bool = False, n_samples: int = 120,
                 tokens_per_day: Optional[float] = None, requests_per_day: Optional[float] = None,
                 price_in_per_m: float = PRICE_IN_PER_M, price_out_per_m: float = PRICE_OUT_PER_M) -> str:
    records = read_jsonl(run_path / RECORDS_FILE)
    scores = read_jsonl(run_path / scores_file)
    gen_errors = read_jsonl(run_path / GEN_ERRORS_FILE)
    analysis = None
    if any(r.get("dims") for r in scores):
        # Derived rows (primary accuracy, citation sensitivity) join the scores, so they are aggregated per
        # system, category and question attribute like every other metric.
        latest = latest_scores(scores)
        primary = A.primary_accuracy_rows(records, latest)
        scores = scores + primary + A.citation_sensitivity_rows(latest)
        comparisons = A.paired_comparisons(latest_scores(scores))
        benchmark = benchmark_index()
        analysis = {
            "comparisons": comparisons,
            "ordering": A.ordering_test(comparisons),
            "error_counts": A.error_type_counts(A.error_type_rows(records, latest, primary)),
            "numeric_agreement": A.numeric_agreement(records, latest),
            "refusal_retrieval": RS.refusal_retrieval(records, benchmark),
            "retrieval_context": RS.retrieval_context_stats(records),
        }
    agg = aggregate(scores)
    smoke_info = None
    if smoke:
        usage = judge_usage(scores)
        ratelimit = latest_ratelimit(scores)
        smoke_info = {"usage": usage, "ratelimit": ratelimit,
                      "estimate": estimate_free_tier(usage, ratelimit, n_samples, tokens_per_day, requests_per_day),
                      "cost": estimate_cost(usage, n_samples, price_in_per_m, price_out_per_m)}
    text = render_report(records, scores, gen_errors, agg, smoke_info, analysis)
    # One report per scores file, so a Groq and a gpt-4o-mini scoring of the same run don't overwrite each other.
    suffix = "" if scores_file == SCORES_FILE else "_" + Path(scores_file).stem
    (run_path / f"report{suffix}.md").write_text(text, encoding="utf-8")
    write_aggregate_csv(run_path / f"aggregate{suffix}.csv", agg)
    if analysis:
        write_dict_csv(run_path / f"paired_comparisons{suffix}.csv", analysis["comparisons"])
        write_dict_csv(run_path / f"error_types{suffix}.csv", analysis["error_counts"])
    return text


def main() -> None:
    p = argparse.ArgumentParser(description="RQ2 report: aggregates, CIs, generation failures, smoke usage.")
    p.add_argument("--run", required=True)
    p.add_argument("--scores-file", default=SCORES_FILE)
    p.add_argument("--smoke", action="store_true", help="Add judge usage, rate limits and a free-tier estimate.")
    p.add_argument("--n-samples", type=int, default=120, help="Samples in the full run (System C v1 + v2 = 120).")
    p.add_argument("--tpd", type=float, default=None, help="Judge tokens-per-day limit, if known.")
    p.add_argument("--rpd", type=float, default=None, help="Override requests-per-day limit.")
    p.add_argument("--price-in", type=float, default=PRICE_IN_PER_M, help="Judge USD per 1M input tokens.")
    p.add_argument("--price-out", type=float, default=PRICE_OUT_PER_M, help="Judge USD per 1M output tokens.")
    args = p.parse_args()
    print(build_report(Path(args.run), args.scores_file, args.smoke, args.n_samples, args.tpd, args.rpd,
                       args.price_in, args.price_out))


if __name__ == "__main__":
    main()
