#!/usr/bin/env python3
"""
RQ1: how recall and completeness grow with the retrieval depth k, per system.

Keeps the first k retrieved chunks of every record (in the order the system returned them) and scores the gold
evidence against them with the default lexical matcher. Reads the shared records; never re-runs a system.
Writes `reports/rq1/k_curve.csv` and `reports/figures/rq1_k_curve.png`.

A system cannot be scored beyond the chunks it returned (A at most 10, B exactly 5), so each curve stops at its
largest returned context. System C's chunks come in hop order, not as one ranking.

Usage:
    python scripts/rq1/k_curve.py
"""

import argparse
import csv
import sys
from pathlib import Path
from typing import Dict, List

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.rq1.common import BENCHMARK_PATH, FIGURES_DIR, OUT_DIR, RECORDS_PATH, SYSTEMS, load_benchmark, load_records  # noqa: E402
from scripts.rq1.figures import (DPI, INK_2, MUTED, SURFACE, SYSTEM_COLORS, SYSTEM_LABELS, SYSTEM_MARKERS,  # noqa: E402
                                 _finish, _legend, _style)
from scripts.rq1.matching import first_rank, relevance_matrix  # noqa: E402


def k_curves(benchmark: Path = BENCHMARK_PATH, records_path: Path = RECORDS_PATH) -> List[Dict[str, float]]:
    """One row per (system, k): mean recall@k and complete@k over questions, plus the largest k returned."""
    bench, records = load_benchmark(benchmark), load_records(records_path)
    per_system: Dict[str, List[Dict[str, object]]] = {}
    for r in records:
        gold = bench[r.get("question_id") or r["query_id"]]["gold_evidence"]
        ranks = [first_rank(row) for row in relevance_matrix(gold, r["retrieved_contexts"])]
        per_system.setdefault(r["system"], []).append({"n": len(r["retrieved_contexts"]), "ranks": ranks})

    rows = []
    for system in [s for s in SYSTEMS if s in per_system]:
        recs = per_system[system]
        max_k = max(rec["n"] for rec in recs)
        mean_k = sum(rec["n"] for rec in recs) / len(recs)
        for k in range(1, max_k + 1):
            found = [[x is not None and x <= k for x in rec["ranks"]] for rec in recs]
            rows.append({"system": system, "k": k, "max_k": max_k, "mean_chunks": round(mean_k, 2),
                         "recall": sum(sum(f) / len(f) for f in found) / len(found),
                         "complete": sum(all(f) for f in found) / len(found), "n": len(recs)})
    return rows


def plot_k_curve(rows: List[Dict[str, float]], out_path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    systems = [s for s in SYSTEMS if any(r["system"] == s for r in rows)]
    panels = [("recall", "Recall@k: share of gold evidence items found"),
              ("complete", "Complete@k: share of questions with all gold evidence found")]
    with _style(plt):
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), sharey=True)
        for ax, (metric, title) in zip(axes, panels):
            for s in systems:
                pts = [r for r in rows if r["system"] == s]
                ax.plot([r["k"] for r in pts], [r[metric] for r in pts], color=SYSTEM_COLORS[s],
                        marker=SYSTEM_MARKERS[s], lw=2, markersize=6, markeredgecolor=SURFACE, markeredgewidth=1.2,
                        zorder=3)
            ax.axvline(next(r["mean_chunks"] for r in rows if r["system"].startswith("system_c")), color=MUTED, lw=1,
                       ls=(0, (4, 3)), zorder=1)
            ax.set_title(title, loc="left", fontsize=9)
            ax.set_xlabel("k: leading retrieved chunks kept")
            ax.set_xticks(range(1, max(r["k"] for r in rows) + 1, 2))
            ax.set_ylim(0, 1.0)
            ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
            ax.grid(axis="x", visible=False)
        axes[0].set_ylabel("mean score")
        axes[0].annotate("C stops itself at\n~10 chunks on average", xy=(9.9, 0.18), xytext=(-6, 0),
                         textcoords="offset points", ha="right", fontsize=7.5, color=INK_2)
        axes[0].annotate("B returns\nexactly 5", xy=(5, 0.735), xytext=(0, 12), textcoords="offset points",
                         ha="center", va="bottom", fontsize=7.5, color=INK_2)
        _legend(fig, systems, markers=True)
        n = max(r["n"] for r in rows)
        _finish(fig, "RQ1: how deep should retrieval go?",
                f"Mean over {n} questions. Each curve ends at the most chunks that system returns "
                "(A up to 10, B exactly 5); C's chunks are in hop order, not one ranking.")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=DPI)
        plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser(description="RQ1 recall / completeness as a function of retrieval depth k.")
    p.add_argument("--benchmark", type=Path, default=BENCHMARK_PATH)
    p.add_argument("--records", type=Path, default=RECORDS_PATH)
    p.add_argument("--out", type=Path, default=OUT_DIR)
    p.add_argument("--figures-dir", type=Path, default=FIGURES_DIR)
    args = p.parse_args()

    rows = k_curves(args.benchmark, args.records)
    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / "k_curve.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    plot_k_curve(rows, args.figures_dir / "rq1_k_curve.png")
    print(f"Saved: {args.out / 'k_curve.csv'}, {args.figures_dir / 'rq1_k_curve.png'}")


if __name__ == "__main__":
    main()
