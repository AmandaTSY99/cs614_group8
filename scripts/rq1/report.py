"""
RQ1 Stage 2: aggregate the Stage 1 scores into `aggregate.csv` and `report.md`.

Every cell is a mean with a bootstrap 95% CI (RQ2's `bootstrap_ci`) and n, per system, overall and per
question-type facet (`common.FACETS`). Evidence-level rows (unit = one gold evidence item) give recall by
evidence modality (table vs text). RAGAS context metrics are included when `ragas_scores.jsonl` exists.

Usage:
    python scripts/rq1/report.py [--out reports/rq1]
"""

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.rq1.common import (  # noqa: E402
    AGGREGATE_FILE, EVIDENCE_SCORES_FILE, FACETS, K_VALUES, OUT_DIR, QUESTION_SCORES_FILE, RAGAS_SCORES_FILE,
    REPORT_FILE, SYSTEMS,
)
from scripts.rq1.score import question_metric_names  # noqa: E402
from scripts.rq2.common import read_jsonl  # noqa: E402
from scripts.rq2.report import bootstrap_ci, latest_scores  # noqa: E402

RAGAS_PREFIX = "ragas_"
HEADLINE_METRICS = ["context_recall", "complete@all", f"recall@{K_VALUES[0]}", "context_precision"]
OVERALL = ("overall", "all")


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def attach_ragas(question_rows: List[Dict[str, Any]], ragas_rows: List[Dict[str, Any]]) -> List[str]:
    """Add `ragas_<metric>` to each question row (None if not scored ok). Returns the metric names added."""
    by_key = {(r["system"], r["question_id"], r["metric"]): r for r in latest_scores(ragas_rows)}
    metrics = sorted({r["metric"] for r in ragas_rows})
    for row in question_rows:
        for m in metrics:
            hit = by_key.get((row["system"], row["question_id"], m))
            ok = hit and hit["status"] == "ok" and hit.get("value") is not None
            row[RAGAS_PREFIX + m] = float(hit["value"]) if ok else None
    return [RAGAS_PREFIX + m for m in metrics]


def aggregate(rows: List[Dict[str, Any]], metrics: Sequence[str], facets: Sequence[str],
              unit: str) -> List[Dict[str, Any]]:
    """One row per (system, facet, group, metric): n, mean and bootstrap 95% CI over `rows`."""
    groups: Dict[Tuple[str, str, str, str], List[float]] = defaultdict(list)
    for row in rows:
        keys = [OVERALL] + [(f, row[f]) for f in facets]
        for metric in metrics:
            value = row.get(metric)
            if value in (None, ""):
                continue
            for facet, group in keys:
                groups[(row["system"], facet, group, metric)].append(float(value))
    out = []
    for (system, facet, group, metric), vals in sorted(groups.items()):
        low, high = bootstrap_ci(vals)
        out.append({"unit": unit, "system": system, "facet": facet, "group": group, "metric": metric,
                    "n": len(vals), "mean": sum(vals) / len(vals), "ci_low": low, "ci_high": high})
    return out


def _fmt(a: Optional[Dict[str, Any]]) -> str:
    return "–" if a is None else f"{a['mean']:.2f} [{a['ci_low']:.2f}, {a['ci_high']:.2f}]"


def _table(index: Dict[Tuple[str, str, str, str], Dict[str, Any]], systems: List[str], facet: str,
           groups: Sequence[str], metrics: Sequence[str], label: str) -> List[str]:
    """Rows = metrics (single group) or groups (single metric); columns = systems."""
    lines = [f"| {label} | " + " | ".join(systems) + " |", "|---|" + "---|" * len(systems)]
    for g in groups:
        for m in metrics:
            cells = [index.get((s, facet, g, m)) for s in systems]
            if all(c is None for c in cells):
                continue
            n = max(c["n"] for c in cells if c)
            name = m if len(groups) == 1 else f"{g} (n={n})"
            lines.append(f"| {name} | " + " | ".join(_fmt(c) for c in cells) + " |")
    return lines


def render_report(agg: List[Dict[str, Any]], question_rows: List[Dict[str, Any]], metrics: List[str],
                  ragas_metrics: List[str], records_note: str) -> str:
    q_index = {(a["system"], a["facet"], a["group"], a["metric"]): a for a in agg if a["unit"] == "question"}
    e_index = {(a["system"], a["facet"], a["group"], a["metric"]): a for a in agg if a["unit"] == "evidence"}
    systems = [s for s in SYSTEMS if any(r["system"] == s for r in question_rows)]
    per_system = {s: sum(r["system"] == s for r in question_rows) for s in systems}
    headline = HEADLINE_METRICS + ragas_metrics
    max_ctx = {s: max(int(r["n_contexts"]) for r in question_rows if r["system"] == s) for s in systems}

    lines = ["# RQ1 results: retrieval completeness by question type", "",
             f"Records: {records_note}. Questions per system: "
             + ", ".join(f"{s} {n}" for s, n in per_system.items()) + ".",
             "Cells: mean [bootstrap 95% CI]. Hypothesis tests are not run yet.", "",
             "## Overall", ""]
    lines += _table(q_index, systems, OVERALL[0], [OVERALL[1]], metrics + ragas_metrics, "Metric")
    lines += ["", "## By question type", ""]
    for facet, groups in FACETS.items():
        lines += [f"### {facet}", ""]
        for metric in headline:
            lines += [f"**{metric}**", ""] + _table(q_index, systems, facet, groups, [metric], facet) + [""]
    found = ["found"] + [f"found@{k}" for k in K_VALUES]
    lines += ["## By evidence modality (unit: gold evidence item)", ""]
    for metric in found:
        lines += [f"**{metric}**", ""] + _table(e_index, systems, "kind", ["table", "text"], [metric], "kind") + [""]
    lines += [
        "## Notes", "",
        "- Relevance is lexical: a gold evidence quote counts as retrieved if a 6-word sub-phrase or >= 65% of "
        "its words appear in a chunk (`scripts/rq1/matching.py`). Scores are lower bounds.",
        "- Ranks follow each system's own `retrieved_contexts` order; System C's order is retrieval order "
        "across hops, with v2's XBRL blocks first.",
        "- Context sizes differ (max chunks: " + ", ".join(f"{s} {n}" for s, n in max_ctx.items())
        + f"). recall@{K_VALUES[0]} "
        "compares systems at an equal budget; context_recall / complete@all compare full contexts.",
        "- `context_precision` is RAGAS-style average precision with lexical labels. `ragas_*` metrics use an "
        "LLM judge against the gold answer, not the gold evidence quotes.",
        "- System C's hop counts and early stopping are reported in RQ3, not here.",
    ]
    return "\n".join(lines) + "\n"


def write_aggregate_csv(path: Path, agg: List[Dict[str, Any]]) -> None:
    fields = ["unit", "system", "facet", "group", "metric", "n", "mean", "ci_low", "ci_high"]
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(agg)


def build_report(out_dir: Path = OUT_DIR, records_note: str = "reports/rq3/records.jsonl") -> str:
    question_rows: List[Dict[str, Any]] = read_csv(out_dir / QUESTION_SCORES_FILE)
    evidence_rows: List[Dict[str, Any]] = read_csv(out_dir / EVIDENCE_SCORES_FILE)
    metrics = [m for m in question_metric_names() if m in question_rows[0]]
    ragas_metrics = attach_ragas(question_rows, read_jsonl(out_dir / RAGAS_SCORES_FILE))
    found = ["found"] + [f"found@{k}" for k in K_VALUES]
    agg = (aggregate(question_rows, metrics + ragas_metrics, list(FACETS), "question")
           + aggregate(evidence_rows, found, ["kind"], "evidence"))
    text = render_report(agg, question_rows, metrics, ragas_metrics, records_note)
    (out_dir / REPORT_FILE).write_text(text, encoding="utf-8")
    write_aggregate_csv(out_dir / AGGREGATE_FILE, agg)
    return text


def main() -> None:
    p = argparse.ArgumentParser(description="RQ1 Stage 2: aggregates with bootstrap CIs and report.md.")
    p.add_argument("--out", type=Path, default=OUT_DIR)
    args = p.parse_args()
    print(build_report(args.out))


if __name__ == "__main__":
    main()
