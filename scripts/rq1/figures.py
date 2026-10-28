"""
RQ1 figures: PNG charts of the aggregated retrieval scores, written to `reports/figures/rq1_*.png`.

Plots the rows `report.aggregate` already computed (mean, bootstrap 95% CI, n), so every plotted value matches
`aggregate.csv` and `report.md`. matplotlib is imported lazily so the scoring pipeline still runs in images
without it. Colours follow the repo's validated categorical palette, one fixed hue per system in every figure.

Usage (normally called from report.build_report):
    figures = write_figures(agg, Path("reports/figures"))
"""

from pathlib import Path
from typing import Any, Callable, Dict, List, Sequence, Tuple

from scripts.rq1.common import FACETS, K_VALUES, OVERALL, SYSTEMS

Index = Dict[Tuple[str, str, str, str, str], Dict[str, Any]]  # (unit, system, facet, group, metric) -> aggregate row

DPI = 300
SURFACE, INK, INK_2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
SYSTEM_COLORS = dict(zip(SYSTEMS, ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]))  # categorical slots 1-4, in order
SYSTEM_MARKERS = dict(zip(SYSTEMS, ["o", "s", "^", "D"]))  # second channel: yellow / aqua are < 3:1 on the surface
SYSTEM_LABELS = {
    "system_a": "SYS A (Dense Baseline)",
    "system_b": "SYS B (Hybrid + Reranker)",
    "system_c_v1": "SYS C v1 (Adaptive AMR)",
    "system_c_v2": "SYS C v2 (Agentic AAMR)",
}
SYSTEM_SHORT = {"system_a": "A", "system_b": "B", "system_c_v1": "C v1", "system_c_v2": "C v2"}
SEQUENTIAL = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]  # blue 100 -> 700


def _style(plt):
    """Light-surface chart chrome: recessive solid hairline grid, no top / right spines."""
    return plt.rc_context({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "axes.edgecolor": AXIS, "axes.labelcolor": INK_2, "axes.titlecolor": INK, "text.color": INK,
        "xtick.color": AXIS, "ytick.color": AXIS, "xtick.labelcolor": INK_2, "ytick.labelcolor": INK_2,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "grid.linestyle": "-", "axes.axisbelow": True,
        "axes.spines.top": False, "axes.spines.right": False, "font.size": 9, "axes.titlesize": 10,
    })


def _cell(idx: Index, unit: str, system: str, facet: str, group: str, metric: str):
    return idx.get((unit, system, facet, group, metric))


def _n_questions(idx: Index, systems: Sequence[str]) -> int:
    return max(_cell(idx, "question", s, *OVERALL, "context_recall")["n"] for s in systems)


def _legend(fig, systems: Sequence[str], markers: bool = False) -> None:
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    handles = [Line2D([], [], color=SYSTEM_COLORS[s], marker=SYSTEM_MARKERS[s], lw=2, markersize=7,
                      markeredgecolor=SURFACE) if markers else Patch(facecolor=SYSTEM_COLORS[s])
               for s in systems]
    fig.legend(handles, [SYSTEM_LABELS[s] for s in systems], loc="upper left", bbox_to_anchor=(0.01, 0.93),
               ncol=len(systems), frameon=False, fontsize=8.5, labelcolor=INK_2, columnspacing=1.8)


def _bars(ax, xs: Sequence[float], cells: Sequence[Any], colors: Sequence[str], width: float) -> None:
    """Bars with a thin CI whisker and the mean printed above the whisker (cells of None are skipped)."""
    for x, cell, color in zip(xs, cells, colors):
        if cell is None:
            continue
        mean, low, high = cell["mean"], cell["ci_low"], cell["ci_high"]
        ax.bar(x, mean, width=width, color=color, zorder=2)
        ax.errorbar(x, mean, yerr=[[max(0.0, mean - low)], [max(0.0, high - mean)]], color=INK_2, lw=1,
                    capsize=2.5, capthick=1, zorder=3)
        ax.text(x, high + 0.02, f"{mean:.2f}", ha="center", va="bottom", fontsize=7.5, color=INK)


def _finish(fig, title: str, subtitle: str) -> None:
    fig.suptitle(title, x=0.01, y=0.985, ha="left", fontsize=11.5, fontweight="bold", color=INK)
    fig.text(0.01, 0.945, subtitle, ha="left", va="top", fontsize=8.5, color=MUTED)
    fig.tight_layout(rect=(0, 0, 1, 0.85))
    fig.subplots_adjust(top=0.81)  # tight_layout also reserves room for the figure legend; keep the header tight


def _fig_overall(plt, idx: Index, systems: List[str]):
    """One panel per headline metric, one bar per system (overall, all questions)."""
    panels = [
        (f"recall@{K_VALUES[0]}", f"Recall@{K_VALUES[0]}: equal top-{K_VALUES[0]} budget"),
        ("context_recall", "Context recall: all retrieved chunks"),
        ("complete@all", "Complete@all: every gold item found"),
        ("context_precision", "Context precision: rank-aware"),
    ]
    fig, axes = plt.subplots(1, len(panels), figsize=(12.5, 4.1), sharey=True)
    xs = list(range(len(systems)))
    for ax, (metric, title) in zip(axes, panels):
        _bars(ax, xs, [_cell(idx, "question", s, *OVERALL, metric) for s in systems],
              [SYSTEM_COLORS[s] for s in systems], width=0.62)
        ax.set_title(title, loc="left", fontsize=9)
        ax.set_xticks(xs, [SYSTEM_SHORT[s] for s in systems])
        ax.set_ylim(0, 1.12)
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("mean score")
    _legend(fig, systems)
    _finish(fig, "RQ1: retrieval completeness, overall",
            f"Mean over {_n_questions(idx, systems)} questions per system; whiskers are bootstrap 95% CIs. "
            "Higher is better on every panel.")
    return fig


def _fig_facets(plt, idx: Index, systems: List[str]):
    """Heatmaps (rows = question-type groups, columns = systems) of context recall and complete@all."""
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap

    rows = []
    for facet, groups in FACETS.items():
        present = [g for g in groups if any(_cell(idx, "question", s, facet, g, "context_recall") for s in systems)]
        if present:  # a group with no questions (e.g. a benchmark subset) has nothing to draw
            rows.append((facet, None))  # header row: facet name, no cells
            rows += [(facet, g) for g in present]
    metrics = [("context_recall", "Context recall"), ("complete@all", "Complete@all")]
    cmap = LinearSegmentedColormap.from_list("rq1_blue", SEQUENTIAL)

    fig, axes = plt.subplots(1, 2, figsize=(9.6, 0.31 * len(rows) + 2.0), sharey=True)
    fig.subplots_adjust(left=0.22, right=0.89, top=0.86, bottom=0.06, wspace=0.07)
    for ax, (metric, title) in zip(axes, metrics):
        data = np.full((len(rows), len(systems)), np.nan)
        for r, (facet, group) in enumerate(rows):
            for c, s in enumerate(systems):
                cell = _cell(idx, "question", s, facet, group, metric) if group else None
                if cell:
                    data[r, c] = cell["mean"]
        mesh = ax.pcolormesh(np.ma.masked_invalid(data), cmap=cmap, vmin=0, vmax=1, edgecolors=SURFACE, linewidth=2)
        for r in range(len(rows)):
            for c in range(len(systems)):
                if not np.isnan(data[r, c]):
                    ax.text(c + 0.5, r + 0.5, f"{data[r, c]:.2f}", ha="center", va="center", fontsize=8,
                            color="#ffffff" if data[r, c] >= 0.5 else INK)
        ax.set_ylim(len(rows), 0)
        ax.set_xticks(np.arange(len(systems)) + 0.5, [SYSTEM_SHORT[s] for s in systems])
        ax.xaxis.tick_top()
        ax.tick_params(length=0)
        ax.set_title(title, loc="left", fontsize=9.5, pad=24)
        ax.grid(False)
        for spine in ax.spines.values():
            spine.set_visible(False)

    ticks, labels = [], []
    for r, (facet, group) in enumerate(rows):
        if group is None:
            axes[0].annotate(facet.replace("_", " ").upper(), xy=(0.012, r + 0.5), xycoords=("figure fraction", "data"),
                             ha="left", va="center", fontsize=8, fontweight="bold", color=INK)
            continue
        n = next(c["n"] for s in systems if (c := _cell(idx, "question", s, facet, group, "context_recall")))
        ticks.append(r + 0.5)
        labels.append(f"{group} (n={n})")
    axes[0].set_yticks(ticks, labels)
    axes[0].tick_params(axis="y", labelsize=8.5)

    cax = fig.add_axes([0.915, 0.42, 0.014, 0.28])
    cbar = fig.colorbar(mesh, cax=cax)
    cbar.outline.set_visible(False)
    cbar.ax.tick_params(length=0, labelsize=8)
    cbar.set_label("mean score", fontsize=8, color=INK_2)

    fig.suptitle("RQ1: where retrieval falls short, by question type", x=0.01, y=0.985, ha="left", fontsize=11.5,
                 fontweight="bold", color=INK)
    fig.text(0.01, 0.945, "Systems: A = dense, B = hybrid + reranker, C v1 / C v2 = adaptive multi-hop. "
             "95% CIs in aggregate.csv; groups with n < 10 are noisy.", ha="left", va="top", fontsize=8.5, color=MUTED)
    return fig


def _fig_modality(plt, idx: Index, systems: List[str]):
    """Share of gold evidence items found, for table vs narrative-text evidence (unit: evidence item)."""
    kinds = ["table", "text"]
    panels = [("found", "Found anywhere in the retrieved context"),
              (f"found@{K_VALUES[0]}", f"Found within the top {K_VALUES[0]} chunks")]
    width = 0.19
    fig, axes = plt.subplots(1, len(panels), figsize=(10.5, 4.2), sharey=True)
    for ax, (metric, title) in zip(axes, panels):
        for j, s in enumerate(systems):
            offset = (j - (len(systems) - 1) / 2) * (width + 0.02)
            _bars(ax, [i + offset for i in range(len(kinds))], [_cell(idx, "evidence", s, "kind", k, metric)
                                                                  for k in kinds], [SYSTEM_COLORS[s]] * len(kinds), width)
        n = [max((_cell(idx, "evidence", s, "kind", k, metric) or {"n": 0})["n"] for s in systems) for k in kinds]
        ax.set_xticks(range(len(kinds)), [f"{k} evidence (n={m})" for k, m in zip(kinds, n)])
        ax.set_xlim(-0.55, len(kinds) - 0.45)
        ax.set_title(title, loc="left", fontsize=9)
        ax.set_ylim(0, 1.12)
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("share of gold evidence items found")
    _legend(fig, systems)
    _finish(fig, "RQ1: recall by evidence modality",
            "Unit is one gold evidence item; whiskers are bootstrap 95% CIs. Tables and narrative text are matched "
            "lexically against each system's retrieved chunks.")
    return fig


def _fig_tradeoff(plt, idx: Index, systems: List[str]):
    """Recall as the context budget grows (left) and the recall / precision trade-off (right)."""
    budgets = [(f"recall@{K_VALUES[0]}", f"top {K_VALUES[0]}"), (f"recall@{K_VALUES[1]}", f"top {K_VALUES[1]}"),
               ("context_recall", "all retrieved")]
    fig, (ax_k, ax_p) = plt.subplots(1, 2, figsize=(11, 4.4))

    for s in systems:
        cells = [_cell(idx, "question", s, *OVERALL, m) for m, _ in budgets]
        ax_k.plot(range(len(budgets)), [c["mean"] for c in cells], color=SYSTEM_COLORS[s], marker=SYSTEM_MARKERS[s],
                  lw=2, markersize=7, markeredgecolor=SURFACE, markeredgewidth=1.5, zorder=3)
    ax_k.set_xticks(range(len(budgets)), [b for _, b in budgets])
    ax_k.set_xlim(-0.25, len(budgets) - 0.75)
    ax_k.set_ylim(0.4, 1.0)
    ax_k.set_title("Recall by context budget", loc="left", fontsize=9)
    ax_k.set_ylabel("mean recall")
    ax_k.grid(axis="x", visible=False)

    x_range, y_range = [], []
    for s in systems:
        p = _cell(idx, "question", s, *OVERALL, "context_precision")
        r = _cell(idx, "question", s, *OVERALL, "context_recall")
        ax_p.errorbar(p["mean"], r["mean"], xerr=[[p["mean"] - p["ci_low"]], [p["ci_high"] - p["mean"]]],
                      yerr=[[r["mean"] - r["ci_low"]], [r["ci_high"] - r["mean"]]], fmt=SYSTEM_MARKERS[s],
                      color=SYSTEM_COLORS[s], ecolor=SYSTEM_COLORS[s], elinewidth=1.3, markersize=10,
                      markeredgecolor=SURFACE, markeredgewidth=1.5, zorder=3)
        # labels sit diagonal to the marker, clear of its own whiskers; C v2 goes below to miss C v1's whisker
        offset, va = ((9, -9), "top") if s == "system_c_v2" else ((9, 9), "bottom")
        ax_p.annotate(f"System {SYSTEM_SHORT[s]}", (p["mean"], r["mean"]), xytext=offset, textcoords="offset points",
                      fontsize=8.5, color=INK, ha="left", va=va)
        x_range += [p["ci_low"], p["ci_high"]]
        y_range += [r["ci_low"], r["ci_high"]]
    ax_p.set_xlim(max(0.0, min(x_range) - 0.04), min(1.0, max(x_range) + 0.12))  # room for the labels
    ax_p.set_ylim(max(0.0, min(y_range) - 0.04), min(1.0, max(y_range) + 0.04))
    ax_p.set_xlabel("context precision (mean, 95% CI)")
    ax_p.set_ylabel("context recall (mean, 95% CI)")
    ax_p.set_title("Recall vs precision: all retrieved chunks", loc="left", fontsize=9)

    _legend(fig, systems, markers=True)
    _finish(fig, "RQ1: the completeness / precision trade-off",
            "Left: System B returns 5 chunks, so its recall does not grow with the budget. "
            "Right: up and to the right is better.")
    return fig


FIGURES: List[Tuple[str, str, Callable]] = [
    ("rq1_overall_metrics.png", "Overall retrieval scores per system (mean, bootstrap 95% CI).", _fig_overall),
    ("rq1_recall_by_question_type.png",
     "Context recall and complete@all by recipe, modality, scope, evidence count and section spread.", _fig_facets),
    ("rq1_evidence_modality.png", "Share of gold table vs text evidence items found.", _fig_modality),
    ("rq1_recall_precision_tradeoff.png", "Recall by context budget, and recall vs context precision.", _fig_tradeoff),
]


def write_figures(agg: List[Dict[str, Any]], out_dir: Path) -> List[Tuple[Path, str]]:
    """Render every RQ1 figure into `out_dir`. Returns (path, caption) per figure; [] if matplotlib is missing."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available; skipping RQ1 figures.")
        return []

    idx: Index = {(a["unit"], a["system"], a["facet"], a["group"], a["metric"]): a for a in agg}
    systems = [s for s in SYSTEMS if _cell(idx, "question", s, *OVERALL, "context_recall")]
    if not systems:
        return []
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    with _style(plt):
        for name, caption, draw in FIGURES:
            fig = draw(plt, idx, systems)
            fig.savefig(out_dir / name, dpi=DPI)
            plt.close(fig)
            written.append((out_dir / name, caption))
    return written
