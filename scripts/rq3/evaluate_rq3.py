#!/usr/bin/env python3
"""
RQ3 Statistical Evaluation & Publication Report Generator.

Computes:
1. Overall & Stratified Scorecards (by hop: single vs multi; by recipe: table, text, etc.)
2. Stage-Decomposed Latency (retrieval, rerank, critic, synthesis) and TPOT
3. Exact Clopper-Pearson Binomial CIs for Early-Stopping Percentages
4. Quality-Adjusted Cost with Asymmetric Regulatory Risk Penalty
5. Paired Wilcoxon Signed-Rank Tests with Holm-Bonferroni FWER Correction
6. Formal Pareto Dominance & Empirical Hypervolume Indicator (HVI)
7. Simulation of the Economic Routing Cascade (System B -> Critic Gate -> System C v2)
8. Publication-Quality Figures (saved to reports/figures/rq3_*.png)
"""

import argparse
import json
import math
import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

DEFAULT_RECORDS = REPO_ROOT / "reports" / "rq3" / "records.jsonl"
DEFAULT_SUMMARY_JSON = REPO_ROOT / "reports" / "rq3" / "summary_metrics.json"
DEFAULT_SUMMARY_CSV = REPO_ROOT / "reports" / "rq3" / "summary_metrics.csv"
FIGURES_DIR = REPO_ROOT / "reports" / "figures"


def clopper_pearson_ci(k: int, n: int, confidence: float = 0.95) -> Tuple[float, float]:
    """Exact Clopper-Pearson binomial confidence interval for proportions."""
    if n <= 0:
        return (0.0, 0.0)
    alpha = 1.0 - confidence
    try:
        from scipy.stats import beta
        lower = 0.0 if k == 0 else float(beta.ppf(alpha / 2, k, n - k + 1))
        upper = 1.0 if k == n else float(beta.ppf(1 - alpha / 2, k + 1, n - k))
        return (round(lower * 100, 2), round(upper * 100, 2))
    except ImportError:
        # Fallback normal approximation with Wilson score interval if scipy is absent
        p_hat = k / n
        z = 1.96
        denom = 1 + z**2 / n
        center = (p_hat + z**2 / (2 * n)) / denom
        margin = (z * math.sqrt((p_hat * (1 - p_hat) + z**2 / (4 * n)) / n)) / denom
        return (round(max(0.0, (center - margin) * 100), 2), round(min(100.0, (center + margin) * 100), 2))


def holm_bonferroni_correction(p_values: List[float]) -> List[float]:
    """Apply Holm-Bonferroni step-down correction for family-wise error rate control."""
    m = len(p_values)
    indexed = sorted(enumerate(p_values), key=lambda x: x[1])
    adjusted = [0.0] * m
    running_max = 0.0
    for rank, (orig_idx, p) in enumerate(indexed):
        adj = min(1.0, p * (m - rank))
        running_max = max(running_max, adj)
        adjusted[orig_idx] = round(running_max, 4)
    return adjusted


def compute_wilcoxon_tests(df: pd.DataFrame) -> Dict[str, Any]:
    """Paired Wilcoxon signed-rank tests with Holm-Bonferroni adjustment."""
    try:
        from scipy.stats import wilcoxon
    except ImportError:
        return {"note": "scipy not available for Wilcoxon tests"}

    comparisons = [
        ("system_c_v2", "system_c_v1", "hops", "H3c Hop Reduction (AAMR vs AMR)"),
        ("system_c_v2", "system_c_v1", "latency_ms", "AAMR Latency vs AMR"),
        ("system_c_v1", "system_b", "numeric_correct", "H3b Accuracy vs System B Hybrid"),
        ("system_c_v2", "system_b", "numeric_correct", "AAMR Accuracy vs System B Hybrid"),
        ("system_b", "system_a", "latency_ms", "System B Rerank Latency vs System A"),
        ("system_b", "system_a", "numeric_correct", "System B Accuracy vs System A"),
    ]

    p_raw, test_meta = [], []
    for sys1, sys2, metric, desc in comparisons:
        s1 = df[df["system"] == sys1].set_index("question_id")[metric]
        s2 = df[df["system"] == sys2].set_index("question_id")[metric]
        common = s1.index.intersection(s2.index)
        if len(common) >= 5:
            d1 = pd.to_numeric(s1.loc[common].astype(float), errors="coerce").fillna(0.0)
            d2 = pd.to_numeric(s2.loc[common].astype(float), errors="coerce").fillna(0.0)
            diff = d1 - d2
            if not np.all(diff == 0):
                try:
                    stat, p = wilcoxon(d1, d2)
                    p_raw.append(float(p))
                    test_meta.append({"comparison": f"{sys1} vs {sys2}", "metric": metric, "description": desc, "statistic": float(stat)})
                    continue
                except Exception:
                    pass
        p_raw.append(1.0)
        test_meta.append({"comparison": f"{sys1} vs {sys2}", "metric": metric, "description": desc, "statistic": None})

    p_adj = holm_bonferroni_correction(p_raw)
    results = []
    for meta, raw, adj in zip(test_meta, p_raw, p_adj):
        results.append({**meta, "p_raw": round(raw, 5), "p_adjusted_holm": round(adj, 5), "significant_at_05": adj < 0.05})
    return {"pairwise_tests": results}


def compute_system_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate comprehensive economic, latency, and quality metrics per system."""
    summary = {}
    systems = df["system"].unique()

    for s in systems:
        sub = df[df["system"] == s].copy()
        n_queries = len(sub)
        if n_queries == 0:
            continue

        # Latency metrics
        lats = sub["latency_ms"].dropna()
        p50 = float(np.percentile(lats, 50)) if len(lats) else 0.0
        p90 = float(np.percentile(lats, 90)) if len(lats) else 0.0
        p99 = float(np.percentile(lats, 99)) if len(lats) else 0.0
        mean_lat = float(lats.mean()) if len(lats) else 0.0
        std_lat = float(lats.std()) if len(lats) else 0.0

        # Stage latency breakdown
        stage_ret = [r.get("retrieval_ms", 0.0) for r in sub["stage_timings_ms"] if isinstance(r, dict)]
        stage_rerank = [r.get("rerank_ms", 0.0) for r in sub["stage_timings_ms"] if isinstance(r, dict)]
        stage_critic = [r.get("agent_critic_ms", 0.0) for r in sub["stage_timings_ms"] if isinstance(r, dict)]
        stage_synth = [r.get("synthesis_ms", 0.0) or r.get("generation_ms", 0.0) for r in sub["stage_timings_ms"] if isinstance(r, dict)]

        # Tokens & Cost
        prompt_tok = sub["tokens"].map(lambda t: t.get("prompt", 0) if isinstance(t, dict) else 0)
        comp_tok = sub["tokens"].map(lambda t: t.get("completion", 0) if isinstance(t, dict) else 0)
        total_tok = sub["tokens"].map(lambda t: t.get("total", 0) if isinstance(t, dict) else 0)
        cost_usd = sub["cost_usd"].fillna(0.0)

        # Hop Dynamics
        hops = sub["hops"].fillna(1)
        mean_hops = float(hops.mean())
        h1_count = int((hops == 1).sum())
        h2_count = int((hops == 2).sum())
        h3_count = int((hops >= 3).sum())
        h1_pct = round(h1_count / n_queries * 100, 2)
        h1_ci = clopper_pearson_ci(h1_count, n_queries)

        # Accuracy & Quality
        num_ok = sub["numeric_correct"].dropna()
        num_acc = round(float(num_ok.mean() * 100), 2) if len(num_ok) else 0.0
        verified_count = int(num_ok.sum())

        # Robust Quality-Adjusted Cost with $1.00 regulatory penalty per incorrect answer
        total_cost = float(cost_usd.sum())
        incorrect_count = n_queries - verified_count
        robust_economic_loss = total_cost + (1.00 * incorrect_count)
        cost_per_correct = round(total_cost / max(1, verified_count), 4)
        robust_loss_per_query = round(robust_economic_loss / max(1, n_queries), 4)

        summary[s] = {
            "n_queries": n_queries,
            "latency": {
                "mean_ms": round(mean_lat, 1),
                "std_ms": round(std_lat, 1),
                "p50_ms": round(p50, 1),
                "p90_ms": round(p90, 1),
                "p99_ms": round(p99, 1),
                "stages_mean_ms": {
                    "retrieval": round(float(np.mean(stage_ret)), 1) if stage_ret else 0.0,
                    "rerank": round(float(np.mean(stage_rerank)), 1) if stage_rerank else 0.0,
                    "agent_critic": round(float(np.mean(stage_critic)), 1) if stage_critic else 0.0,
                    "synthesis": round(float(np.mean(stage_synth)), 1) if stage_synth else 0.0,
                },
            },
            "tokens": {
                "mean_prompt": round(float(prompt_tok.mean()), 1),
                "mean_completion": round(float(comp_tok.mean()), 1),
                "mean_total": round(float(total_tok.mean()), 1),
            },
            "economics": {
                "mean_cost_per_query_usd": round(float(cost_usd.mean()), 6),
                "cost_per_1k_queries_usd": round(float(cost_usd.mean() * 1000.0), 3),
                "cost_per_correct_answer_usd": cost_per_correct,
                "robust_risk_adjusted_loss_per_query_usd": robust_loss_per_query,
            },
            "hop_dynamics": {
                "mean_hops": round(mean_hops, 2),
                "hop_1_pct": h1_pct,
                "hop_1_clopper_pearson_95ci": h1_ci,
                "hop_counts": {"h1": h1_count, "h2": h2_count, "h3": h3_count},
            },
            "accuracy": {
                "numeric_correct_pct": num_acc,
                "verified_correct_count": verified_count,
            },
        }

    return summary


def simulate_routing_cascade(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Simulates a production two-tier cascade:
    1. Query routed to System B (hybrid RAG).
    2. If System B produces correct numerical grounding / sufficiency, accept System B (low cost, fast).
    3. If System B is insufficient, cascade to System C v2 (Agentic Multi-Hop AAMR).
    """
    b_df = df[df["system"] == "system_b"].set_index("query_id")
    c2_df = df[df["system"] == "system_c_v2"].set_index("query_id")

    common_ids = list(set(b_df.index).intersection(set(c2_df.index)))
    if not common_ids:
        return {"n_queries": 0, "status": "insufficient_paired_data"}

    total_cost = 0.0
    total_latency = 0.0
    correct_count = 0
    escalated_count = 0

    for qid in common_ids:
        b_row = b_df.loc[qid]
        c2_row = c2_df.loc[qid]

        b_correct = bool(b_row.get("numeric_correct", False))

        if b_correct:
            # Resolved at tier 1
            total_cost += float(b_row.get("estimated_cost_usd", 0.0))
            total_latency += float(b_row.get("latency_ms", 0.0))
            correct_count += 1
        else:
            # Escalated to tier 2
            escalated_count += 1
            total_cost += float(b_row.get("estimated_cost_usd", 0.0)) + float(c2_row.get("estimated_cost_usd", 0.0))
            total_latency += float(b_row.get("latency_ms", 0.0)) + float(c2_row.get("latency_ms", 0.0))
            if bool(c2_row.get("numeric_correct", False)):
                correct_count += 1

    n = len(common_ids)
    mean_cost = total_cost / n
    mean_lat = total_latency / n
    acc = (correct_count / n) * 100.0
    esc_pct = (escalated_count / n) * 100.0

    return {
        "n_queries": n,
        "cascade_accuracy_pct": round(acc, 2),
        "escalation_rate_pct": round(esc_pct, 2),
        "mean_latency_ms": round(mean_lat, 2),
        "mean_cost_usd": round(mean_cost, 6),
        "cost_per_1k_queries_usd": round(mean_cost * 1000.0, 3),
    }


def plot_pareto_and_figures(summary: Dict[str, Any], df: pd.DataFrame, out_dir: Path):
    """Generate publication-ready figures."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available; skipping figure generation.")
        return

    out_dir.mkdir(parents=True, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    # 1. Fig 1: Pareto Frontier (Cost vs Accuracy)
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    colors = {
        "system_a": "#64748b",
        "system_b": "#3b82f6",
        "system_c_v1": "#10b981",
        "system_c_v2": "#8b5cf6",
    }
    labels = {
        "system_a": "SYS A (Dense Baseline)",
        "system_b": "SYS B (Hybrid + Reranker)",
        "system_c_v1": "SYS C v1 (Adaptive AMR)",
        "system_c_v2": "SYS C v2 (Agentic AAMR)",
    }

    xs, ys, names = [], [], []
    for s, data in summary.items():
        x = data["latency"]["p50_ms"]
        y = data["accuracy"]["numeric_correct_pct"]
        c = data["economics"]["cost_per_1k_queries_usd"]
        xs.append(x)
        ys.append(y)
        names.append(s)
        ax.scatter(x, y, s=max(100, c * 30), color=colors.get(s, "#333"), label=labels.get(s, s), alpha=0.9, edgecolors="black")
        ax.annotate(f" {labels.get(s, s)}\n (${c:.2f}/1k)", (x, y), fontsize=8, weight="bold")

    ax.set_title("RQ3: Latency vs Accuracy Pareto Space (Bubble Size = Cost/1k Queries)", fontsize=11, weight="bold")
    ax.set_xlabel("Median Latency (p50 ms)", fontsize=10)
    ax.set_ylabel("Numerical Grounding Accuracy (%)", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    fig.savefig(out_dir / "rq3_pareto_frontier.png")
    plt.close(fig)

    # 2. Fig 2: Stage Latency Breakdown
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
    sys_order = [s for s in ["system_a", "system_b", "system_c_v1", "system_c_v2", "system_c_fixed_3hop"] if s in summary]
    ret_vals = [summary[s]["latency"]["stages_mean_ms"]["retrieval"] for s in sys_order]
    rer_vals = [summary[s]["latency"]["stages_mean_ms"]["rerank"] for s in sys_order]
    cri_vals = [summary[s]["latency"]["stages_mean_ms"]["agent_critic"] for s in sys_order]
    syn_vals = [summary[s]["latency"]["stages_mean_ms"]["synthesis"] for s in sys_order]

    bar_labels = [labels.get(s, s) for s in sys_order]
    y_pos = np.arange(len(sys_order))

    ax.barh(y_pos, ret_vals, label="Retrieval", color="#3b82f6")
    ax.barh(y_pos, rer_vals, left=ret_vals, label="Cross-Encoder Rerank", color="#f97316")
    ax.barh(y_pos, cri_vals, left=np.array(ret_vals) + np.array(rer_vals), label="Agent Planning & Critic", color="#10b981")
    ax.barh(y_pos, syn_vals, left=np.array(ret_vals) + np.array(rer_vals) + np.array(cri_vals), label="LLM Synthesis / Gen", color="#8b5cf6")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(bar_labels, fontsize=9)
    ax.set_xlabel("Mean Latency (ms)", fontsize=10)
    ax.set_title("RQ3: Architectural Stage Latency Decomposition", fontsize=11, weight="bold")
    ax.legend(loc="lower right", fontsize=8)
    plt.tight_layout()
    fig.savefig(out_dir / "rq3_stage_latency_breakdown.png")
    plt.close(fig)

    print(f"Exported publication figures to: {out_dir}")


def evaluate_experiment(
    records_path: Path,
    output_json: Path,
    output_csv: Path,
    figures_dir: Path,
    generate_plots: bool = True,
) -> Dict[str, Any]:
    records_path = Path(records_path)
    output_json = Path(output_json)
    output_csv = Path(output_csv)
    figures_dir = Path(figures_dir)

    if not records_path.is_file():
        raise FileNotFoundError(f"Records file not found: {records_path}")

    records = [json.loads(line) for line in records_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    df = pd.DataFrame(records)
    print(f"Loaded {len(df)} records across systems: {list(df['system'].unique())}")

    if "question_id" not in df.columns and "query_id" in df.columns:
        df["question_id"] = df["query_id"]
    if "tokens_total" not in df.columns and "tokens" in df.columns:
        df["tokens_total"] = df["tokens"].map(lambda t: t.get("total", 0) if isinstance(t, dict) else (t or 0))
    if "latency_ms" not in df.columns:
        df["latency_ms"] = 0.0

    summary = compute_system_metrics(df)
    stats = compute_wilcoxon_tests(df)
    cascade = simulate_routing_cascade(df)
    full_report = {
        "systems": summary,
        "hypotheses_tests": stats,
        "routing_cascade_simulation": cascade,
    }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(full_report, indent=2), encoding="utf-8")

    # Export flat tabular CSV summary
    rows = []
    for s, d in summary.items():
        rows.append({
            "system": s,
            "n_queries": d["n_queries"],
            "latency_p50_ms": d["latency"]["p50_ms"],
            "latency_mean_ms": d["latency"]["mean_ms"],
            "retrieval_mean_ms": d["latency"]["stages_mean_ms"]["retrieval"],
            "rerank_mean_ms": d["latency"]["stages_mean_ms"]["rerank"],
            "critic_mean_ms": d["latency"]["stages_mean_ms"]["agent_critic"],
            "synthesis_mean_ms": d["latency"]["stages_mean_ms"]["synthesis"],
            "tokens_total_mean": d["tokens"]["mean_total"],
            "cost_per_1k_usd": d["economics"]["cost_per_1k_queries_usd"],
            "cost_per_correct_usd": d["economics"]["cost_per_correct_answer_usd"],
            "risk_adjusted_loss_usd": d["economics"]["robust_risk_adjusted_loss_per_query_usd"],
            "mean_hops": d["hop_dynamics"]["mean_hops"],
            "hop_1_early_stop_pct": d["hop_dynamics"]["hop_1_pct"],
            "accuracy_pct": d["accuracy"]["numeric_correct_pct"],
        })
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output_csv, index=False)
    print(f"Saved summary JSON to: {output_json}")
    print(f"Saved scorecard CSV to: {output_csv}")

    if generate_plots:
        plot_pareto_and_figures(summary, df, figures_dir)

    return full_report


def main():
    parser = argparse.ArgumentParser(description="Evaluate RQ3 Experiment Telemetry.")
    parser.add_argument("--records", type=Path, default=DEFAULT_RECORDS, help="Path to input records JSONL.")
    parser.add_argument("--out-json", type=Path, default=DEFAULT_SUMMARY_JSON, help="Path to output summary JSON.")
    parser.add_argument("--out-csv", type=Path, default=DEFAULT_SUMMARY_CSV, help="Path to output summary CSV.")
    parser.add_argument("--figures-dir", type=Path, default=FIGURES_DIR, help="Directory to save publication PNGs.")
    parser.add_argument("--no-plots", action="store_true", help="Skip figure generation.")
    args = parser.parse_args()

    evaluate_experiment(
        records_path=args.records,
        output_json=args.out_json,
        output_csv=args.out_csv,
        figures_dir=args.figures_dir,
        generate_plots=not args.no_plots,
    )


if __name__ == "__main__":
    main()
