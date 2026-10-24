#!/usr/bin/env python3
"""
Publication-Quality Visualization for RQ3 Inference Economics & Pareto Frontier.

Owned by: Anish (RQ3 Lead: Latency, Token Consumption, Dollar Cost & Pareto Frontier)

Generates:
1. `reports/figures/rq3_pareto_frontier.png`: Cost vs. Latency vs. Token Consumption.
2. `reports/figures/rq3_latency_breakdown.png`: p50 vs. p90 vs. Mean latency comparison.
3. `reports/figures/rq3_hop_distribution.png`: Hop termination distribution (Hop 1 vs. 2 vs. 3).
4. `reports/figures/rq3_executive_dashboard.png`: Multi-panel executive summary for slides and report.

Usage:
    python scripts/plot_rq3_pareto.py
    python scripts/plot_rq3_pareto.py --input-csv reports/rq3_ablation_metrics.csv
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict

import matplotlib.pyplot as plt
import pandas as pd

# Styling constants for academic paper quality
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
    "axes.edgecolor": "#cccccc",
    "axes.linewidth": 0.8,
    "grid.color": "#e5e7eb",
    "grid.linestyle": "--",
    "grid.linewidth": 0.6,
    "figure.autolayout": True,
})

# Brand / Palette colors
COLORS = {
    "fixed_1hop": "#64748b",   # Slate Grey
    "fixed_3hop": "#ef4444",   # Coral Red
    "adaptive_v1": "#3b82f6",  # Royal Blue
    "agentic_v2": "#10b981",   # Emerald Green
}

MARKERS = {
    "fixed_1hop": "o",
    "fixed_3hop": "s",
    "adaptive_v1": "^",
    "agentic_v2": "*",
}


def load_metrics(csv_path: Path, json_path: Path) -> pd.DataFrame:
    """Load aggregate metrics from CSV (or fallback to JSON summary)."""
    if csv_path.exists():
        return pd.read_csv(csv_path)
    elif json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        conds = data.get("conditions", {})
        rows = []
        for k, c in conds.items():
            dist = c["hop_dynamics"]["distribution"]
            rows.append({
                "condition_key": k,
                "condition_label": c["label"],
                "cost_per_1k_queries_usd": c["cost"]["cost_per_1k_queries_usd"],
                "mean_latency_ms": c["latency"]["mean_ms"],
                "latency_p50_ms": c["latency"]["p50_ms"],
                "latency_p90_ms": c["latency"]["p90_ms"],
                "mean_total_tokens": c["tokens"]["mean_total_tokens"],
                "mean_hops": c["hop_dynamics"]["mean_hops"],
                "early_stopping_rate_pct": c["hop_dynamics"]["early_stopping_rate_pct"],
                "hop_1_count": dist.get("1", 0),
                "hop_2_count": dist.get("2", 0),
                "hop_3_count": dist.get("3", 0),
                "mean_numerical_grounding_error_rate": c["grounding_quality"]["mean_numerical_grounding_error_rate"],
            })
        return pd.DataFrame(rows)
    else:
        raise FileNotFoundError(f"Neither {csv_path} nor {json_path} could be found.")


def plot_pareto_frontier(df: pd.DataFrame, out_path: Path) -> None:
    """Plot Figure 1: Cost ($/1k) vs. Latency p50 (ms) with bubble size = token volume."""
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)

    for _, row in df.iterrows():
        key = row["condition_key"]
        color = COLORS.get(key, "#3b82f6")
        marker = MARKERS.get(key, "o")
        x = row["cost_per_1k_queries_usd"]
        y = row["latency_p50_ms"]
        size = row["mean_total_tokens"] / 6.0  # Normalized bubble area

        ax.scatter(x, y, s=size, color=color, alpha=0.85, edgecolors="#1f2937", linewidth=1.2, zorder=4)

        # Label placement
        offset_y = 1.2 if key != "adaptive_v1" else -1.8
        offset_x = 0.015 if key != "fixed_3hop" else -0.09
        ax.annotate(
            f"{row['condition_label']}\n(${x:.4f} / 1k, {y:.1f} ms)",
            xy=(x, y),
            xytext=(x + offset_x, y + offset_y),
            fontsize=9,
            fontweight="bold",
            color="#1f2937",
            bbox=dict(boxstyle="round,pad=0.3", fc="#ffffff", ec="#cbd5e1", lw=0.8, alpha=0.9),
            zorder=5,
        )

    # Draw Pareto Trade-Off Curve (connecting Fixed 1-Hop -> Adaptive v1 -> Fixed 3-Hop)
    p_df = df[df["condition_key"].isin(["fixed_1hop", "adaptive_v1", "fixed_3hop"])].sort_values("cost_per_1k_queries_usd")
    ax.plot(p_df["cost_per_1k_queries_usd"], p_df["latency_p50_ms"], linestyle=":", color="#94a3b8", linewidth=1.5, zorder=2)

    ax.set_title("RQ3: Inference Economics Pareto Frontier for SEC 10-K RAG", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Operational Cost per 1,000 Queries (USD)", fontsize=10, fontweight="bold", labelpad=8)
    ax.set_ylabel("Median End-to-End Latency p50 (ms)", fontsize=10, fontweight="bold", labelpad=8)
    ax.grid(True, zorder=1)

    # Custom annotations
    ax.text(
        0.03, 0.92,
        "Optimal Direction:\nLower Cost & Lower Latency ↙",
        transform=ax.transAxes,
        fontsize=9,
        fontweight="bold",
        color="#047857",
        bbox=dict(boxstyle="square,pad=0.4", fc="#ecfdf5", ec="#a7f3d0", lw=1),
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"✓ Saved Pareto Frontier plot to: {out_path}")


def plot_latency_breakdown(df: pd.DataFrame, out_path: Path) -> None:
    """Plot Figure 2: Latency comparison (Mean vs. p50 vs. p90)."""
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)

    labels = [row["condition_label"].replace(" (AMR v1)", "\nv1").replace(" (AAMR v2)", "\nv2") for _, row in df.iterrows()]
    x = range(len(labels))
    width = 0.25

    p50 = df["latency_p50_ms"]
    p90 = df["latency_p90_ms"]
    means = df["mean_latency_ms"]

    b1 = ax.bar([i - width for i in x], p50, width=width, label="Median (p50)", color="#3b82f6", alpha=0.9)
    b2 = ax.bar(x, means, width=width, label="Mean Latency", color="#6366f1", alpha=0.9)
    b3 = ax.bar([i + width for i in x], p90, width=width, label="Tail (p90)", color="#f43f5e", alpha=0.9)

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=9, fontweight="bold")
    ax.set_ylabel("Latency (ms)", fontsize=10, fontweight="bold")
    ax.set_title("RQ3 Latency Profile Across Architectural Configurations", fontsize=12, fontweight="bold", pad=12)
    ax.legend(frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=9)
    ax.grid(True, axis="y", zorder=1)

    # Add value annotations on top of p50 bars
    for rect in b1:
        height = rect.get_height()
        ax.annotate(f"{height:.1f}ms", xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"✓ Saved Latency Breakdown plot to: {out_path}")


def plot_hop_distribution(df: pd.DataFrame, out_path: Path) -> None:
    """Plot Figure 3: Stacked Bar Chart of Hop Distribution (Early-Stopping Behavior)."""
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)

    labels = [row["condition_label"].replace(" (AMR v1)", "\nv1").replace(" (AAMR v2)", "\nv2") for _, row in df.iterrows()]
    h1 = df["hop_1_count"]
    h2 = df["hop_2_count"]
    h3 = df["hop_3_count"]
    totals = h1 + h2 + h3

    h1_pct = (h1 / totals) * 100.0
    h2_pct = (h2 / totals) * 100.0
    h3_pct = (h3 / totals) * 100.0

    ax.bar(labels, h1_pct, label="Hop 1 (Early Stop / Single-Pass)", color="#10b981", alpha=0.9)
    ax.bar(labels, h2_pct, bottom=h1_pct, label="Hop 2 (Cross-Section Multi-Hop)", color="#3b82f6", alpha=0.9)
    ax.bar(labels, h3_pct, bottom=h1_pct + h2_pct, label="Hop 3 (Hard Ceiling / Deep)", color="#f59e0b", alpha=0.9)

    ax.set_ylabel("% of Evaluation Queries", fontsize=10, fontweight="bold")
    ax.set_title("RQ3 Hop Convergence & Early-Stopping Dynamics", fontsize=12, fontweight="bold", pad=12)
    ax.legend(loc="upper right", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8)
    ax.grid(True, axis="y", zorder=1)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"✓ Saved Hop Distribution plot to: {out_path}")


def plot_executive_dashboard(df: pd.DataFrame, out_path: Path) -> None:
    """Generate a combined 1x3 panel executive dashboard for presentation slides."""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5), dpi=300)

    # Panel 1: Cost vs. Tokens
    x = range(len(df))
    cost = df["cost_per_1k_queries_usd"]
    bars1 = ax1.bar(x, cost, color=[COLORS.get(k, "#3b82f6") for k in df["condition_key"]], alpha=0.9)
    ax1.set_xticks(list(x))
    ax1.set_xticklabels([k.replace("_", "\n") for k in df["condition_key"]], fontsize=8, fontweight="bold")
    ax1.set_ylabel("Cost per 1k Queries ($)", fontsize=9, fontweight="bold")
    ax1.set_title("A. Inference Cost ($/1k)", fontsize=10, fontweight="bold")
    ax1.grid(True, axis="y")
    for b in bars1:
        ax1.annotate(f"${b.get_height():.3f}", xy=(b.get_x() + b.get_width() / 2, b.get_height()),
                     xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8)

    # Panel 2: Latency p50 & p90
    p50 = df["latency_p50_ms"]
    p90 = df["latency_p90_ms"]
    width = 0.35
    ax2.bar([i - width/2 for i in x], p50, width=width, label="p50", color="#3b82f6", alpha=0.9)
    ax2.bar([i + width/2 for i in x], p90, width=width, label="p90", color="#f43f5e", alpha=0.9)
    ax2.set_xticks(list(x))
    ax2.set_xticklabels([k.replace("_", "\n") for k in df["condition_key"]], fontsize=8, fontweight="bold")
    ax2.set_ylabel("Latency (ms)", fontsize=9, fontweight="bold")
    ax2.set_title("B. Latency Profile (p50 vs p90)", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=8)
    ax2.grid(True, axis="y")

    # Panel 3: Mean Hops & Early Stopping
    hops = df["mean_hops"]
    bars3 = ax3.bar(x, hops, color="#8b5cf6", alpha=0.9)
    ax3.set_xticks(list(x))
    ax3.set_xticklabels([k.replace("_", "\n") for k in df["condition_key"]], fontsize=8, fontweight="bold")
    ax3.set_ylabel("Mean Retrieval Hops", fontsize=9, fontweight="bold")
    ax3.set_title("C. Iterative Convergence (Hops)", fontsize=10, fontweight="bold")
    ax3.grid(True, axis="y")
    for b in bars3:
        ax3.annotate(f"{b.get_height():.2f}", xy=(b.get_x() + b.get_width() / 2, b.get_height()),
                     xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8)

    fig.suptitle("CS614 System C: RQ3 Inference Economics & Architecture Ablation Summary", fontsize=13, fontweight="bold", y=1.02)
    fig.tight_layout()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"✓ Saved Executive Dashboard plot to: {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate publication-ready plots for RQ3.")
    parser.add_argument("--input-csv", type=str, default="reports/rq3_ablation_metrics.csv")
    parser.add_argument("--input-json", type=str, default="reports/rq3_ablation_summary.json")
    parser.add_argument("--output-dir", type=str, default="reports/figures")
    args = parser.parse_args()

    csv_path = Path(args.input_csv)
    json_path = Path(args.input_json)
    out_dir = Path(args.output_dir)

    df = load_metrics(csv_path, json_path)
    print(f"Loaded {len(df)} conditions from {csv_path}")

    plot_pareto_frontier(df, out_dir / "rq3_pareto_frontier.png")
    plot_latency_breakdown(df, out_dir / "rq3_latency_breakdown.png")
    plot_hop_distribution(df, out_dir / "rq3_hop_distribution.png")
    plot_executive_dashboard(df, out_dir / "rq3_executive_dashboard.png")


if __name__ == "__main__":
    main()
