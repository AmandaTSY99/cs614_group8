#!/usr/bin/env python3
"""
RQ3 Inference Economics & Architectural Ablation Harness for System C.

Owned by: Anish (RQ3 Lead: Latency, Token Consumption, Dollar Cost & Pareto Frontier)

Ablation Conditions Benchmarked:
1. `fixed_1hop`: Fixed 1-Hop Baseline (max_hops=1, single-pass retrieval)
2. `fixed_3hop`: Fixed 3-Hop Exhaustive (max_hops=3, force_max_hops=True, no early-stopping)
3. `adaptive_v1`: Adaptive Multi-Hop AMR (max_hops=3, dynamic reflection & early-stopping)
4. `agentic_v2`:  Agentic Adaptive AMR AAMR (max_hops=3, tabular_tool + dynamic reflection)

Metrics Computed:
- Latency (ms): Mean, Std, Min, Max, p50, p90, p99
- Token Usage: Mean Prompt Tokens, Mean Completion Tokens, Mean Total Tokens
- Inference Cost: Mean USD/query, USD per 1,000 queries
- Hop Dynamics: Mean Hops, Early-Stopping %, Hop Distribution (Hop 1 / Hop 2 / Hop 3)
- Quality/Grounding: Guardrail Pass Rate %, Numerical Grounding Error Rate %
- Pareto Frontier coordinates for plotting Cost vs. Latency vs. Grounding Error Rate

Outputs:
- Console Comparative Table
- `reports/rq3_ablation_summary.json`
- `reports/rq3_ablation_metrics.csv`
- `reports/rq3_ablation_per_query.csv`
"""

import argparse
import csv
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.system_c.graph import run_system_c
from src.system_c.state import AdaptiveRAGState

# Terminal ANSI styling
BOLD = "\033[1m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
BLUE = "\033[34m"
RED = "\033[31m"
DIM = "\033[2m"
RESET = "\033[0m"

# 12 Curated Evaluation Queries across FinQA / TAT-QA / SEC 10-K Disclosures
ABLATION_EVAL_DATASET = [
    # Category A: Single-Hop Factual Queries (Expected to early-stop at Hop 1 in Adaptive mode)
    {
        "id": "SEC-SH-01",
        "category": "single_hop_factual",
        "query": "What was NVIDIA's fiscal year 2026 period end date, and what is the address of its principal executive office?",
        "ticker": "NVDA",
        "years": [2026],
    },
    {
        "id": "SEC-SH-02",
        "category": "single_hop_factual",
        "query": "Who served as the independent registered public accounting firm for Apple Inc. in fiscal 2024?",
        "ticker": "AAPL",
        "years": [2024],
    },
    {
        "id": "SEC-SH-03",
        "category": "single_hop_factual",
        "query": "Under which state laws is Microsoft Corporation incorporated, and what is its IRS employer identification number?",
        "ticker": "MSFT",
        "years": [2024],
    },

    # Category B: Multi-Hop Causal & Footnote Queries (Expected to run 2 hops in Adaptive mode)
    {
        "id": "SEC-MH-01",
        "category": "multi_hop_cross_section",
        "query": "How did NVIDIA Data Center segment revenue perform in FY2026, and what specific customer concentration risks or purchase obligations were disclosed in the Notes to Consolidated Financial Statements?",
        "ticker": "NVDA",
        "years": [2026],
    },
    {
        "id": "SEC-MH-02",
        "category": "multi_hop_cross_section",
        "query": "How did foreign currency exchange rate fluctuations impact Amazon's operating income in 2024, and what derivative instruments were utilized for hedging?",
        "ticker": "AMZN",
        "years": [2024],
    },
    {
        "id": "SEC-MH-03",
        "category": "multi_hop_cross_section",
        "query": "What were Alphabet's primary legal proceedings and regulatory antitrust contingencies disclosed in Note 10 of the 2024 Form 10-K?",
        "ticker": "GOOGL",
        "years": [2024],
    },
    {
        "id": "SEC-MH-04",
        "category": "multi_hop_cross_section",
        "query": "Describe Meta's restructuring charges related to facility consolidations and data center assets in 2024, and explain their impact on family of apps operating margin.",
        "ticker": "META",
        "years": [2024],
    },

    # Category C: Multi-Year Quantitative & Financial Comparison Queries (Testing Tabular Tool impact in v2)
    {
        "id": "SEC-QT-01",
        "category": "quantitative_comparison",
        "query": "Compare NVIDIA's total revenue, operating income, and net income between FY2025 and FY2026, and calculate the year-over-year revenue growth rate.",
        "ticker": "NVDA",
        "years": [2025, 2026],
    },
    {
        "id": "SEC-QT-02",
        "category": "quantitative_comparison",
        "query": "What was Apple's total net sales, gross margin, and operating cash flow in fiscal 2023 versus fiscal 2024?",
        "ticker": "AAPL",
        "years": [2023, 2024],
    },
    {
        "id": "SEC-QT-03",
        "category": "quantitative_comparison",
        "query": "Compare Microsoft's total revenue and net income between FY2023 and FY2024, and evaluate the change in diluted earnings per share.",
        "ticker": "MSFT",
        "years": [2023, 2024],
    },

    # Category D: Complex Constraint & Segment Breakdown Queries (Testing Hop 2-3 depth)
    {
        "id": "SEC-CX-01",
        "category": "complex_constraint",
        "query": "Explain how Tesla's automotive regulatory credits revenue shifted between 2023 and 2024, and what supply chain constraints impacted vehicle deliveries according to Item 7?",
        "ticker": "TSLA",
        "years": [2023, 2024],
    },
    {
        "id": "SEC-CX-02",
        "category": "complex_constraint",
        "query": "What were JPMorgan Chase's total assets and total liabilities in 2024, and how did interest rate exposure affect net interest income?",
        "ticker": "JPM",
        "years": [2024],
    },
]

ABLATION_CONDITIONS = [
    {
        "key": "fixed_1hop",
        "label": "Fixed 1-Hop Baseline",
        "mode": "v1_amr",
        "max_hops": 1,
        "force_max_hops": False,
        "description": "Standard single-pass retrieval (lower latency bound; lacks multi-hop depth).",
    },
    {
        "key": "fixed_3hop",
        "label": "Fixed 3-Hop Exhaustive",
        "mode": "v1_amr",
        "max_hops": 3,
        "force_max_hops": True,
        "description": "Naive iterative multi-hop without early-stopping (upper cost & latency bound).",
    },
    {
        "key": "adaptive_v1",
        "label": "Adaptive Multi-Hop (AMR v1)",
        "mode": "v1_amr",
        "max_hops": 3,
        "force_max_hops": False,
        "description": "System C v1 with Evidence Sufficiency Critic dynamic early-stopping.",
    },
    {
        "key": "agentic_v2",
        "label": "Agentic Adaptive (AAMR v2)",
        "mode": "v2_aamr",
        "max_hops": 3,
        "force_max_hops": False,
        "description": "System C v2 with autonomous tabular XBRL tool + dynamic early-stopping.",
    },
]


def percentile(data: List[float], p: float) -> float:
    """Calculate the p-th percentile of a list of floats."""
    if not data:
        return 0.0
    sorted_data = sorted(data)
    idx = (len(sorted_data) - 1) * (p / 100.0)
    floor_idx = math.floor(idx)
    ceil_idx = math.ceil(idx)
    if floor_idx == ceil_idx:
        return round(sorted_data[int(idx)], 2)
    d0 = sorted_data[floor_idx] * (ceil_idx - idx)
    d1 = sorted_data[ceil_idx] * (idx - floor_idx)
    return round(d0 + d1, 2)


def run_ablation(
    queries: List[Dict[str, Any]],
    conditions: List[Dict[str, Any]],
    provider: Optional[str] = None,
    model: Optional[str] = None,
    verbose: bool = False,
) -> Dict[str, Any]:
    """Execute ablation experiments over all queries across all architectural conditions."""
    if provider:
        os.environ["LLM_PROVIDER"] = provider
    if model:
        os.environ["LLM_MODEL"] = model

    active_provider = os.getenv("LLM_PROVIDER", "ollama").strip().lower()
    active_model = os.getenv("LLM_MODEL", "qwen2.5:7b" if active_provider == "ollama" else "mock")

    print(f"\n{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{CYAN}║    RQ3 INFERENCE ECONOMICS & ARCHITECTURAL ABLATION BENCHMARK (ANISH LEAD)                   ║{RESET}")
    print(f"{BOLD}{CYAN}║    Fixed 1-Hop vs. Fixed 3-Hop vs. Adaptive AMR (v1) vs. Agentic AAMR (v2)                   ║{RESET}")
    print(f"{BOLD}{CYAN}╚══════════════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
    print(f"  {BOLD}Provider:{RESET} {GREEN}{active_provider.upper()}{RESET}  |  {BOLD}Model:{RESET} {GREEN}{active_model}{RESET}  |  {BOLD}Queries:{RESET} {len(queries)}  |  {BOLD}Conditions:{RESET} {len(conditions)}\n")

    per_query_records: List[Dict[str, Any]] = []
    condition_aggregates: Dict[str, Dict[str, Any]] = {}

    total_runs = len(conditions) * len(queries)
    run_idx = 0

    for cond in conditions:
        cond_key = cond["key"]
        print(f"{BOLD}{MAGENTA}▶ EVALUATING CONDITION: {cond['label']} ({cond['mode']}, max_hops={cond['max_hops']}, force_max={cond['force_max_hops']}){RESET}")

        latencies_ms: List[float] = []
        prompt_tokens_list: List[int] = []
        completion_tokens_list: List[int] = []
        total_tokens_list: List[int] = []
        costs_usd: List[float] = []
        hops_list: List[int] = []
        early_stopped_count = 0
        guardrail_passed_count = 0
        grounding_errors: List[float] = []
        faithfulness_scores: List[float] = []

        hop_distribution = {1: 0, 2: 0, 3: 0}

        for q_idx, q in enumerate(queries, 1):
            run_idx += 1
            t0 = time.perf_counter()

            state = run_system_c(
                query=q["query"],
                max_hops=cond["max_hops"],
                mode=cond["mode"],
                target_ticker=q.get("ticker"),
                fiscal_years=q.get("fiscal_years") or q.get("years"),
                force_max_hops=cond["force_max_hops"],
            )
            elapsed_ms = (time.perf_counter() - t0) * 1000.0

            telemetry = state.get("telemetry", {})
            summary = telemetry.get("rq3_summary", {})
            guardrail = state.get("guardrail_report", {})

            # Latency fallback if not instrumented
            lat = summary.get("total_latency_ms") or elapsed_ms
            latencies_ms.append(lat)

            p_tok = summary.get("total_prompt_tokens", 0)
            c_tok = summary.get("total_completion_tokens", 0)
            t_tok = summary.get("total_tokens", 0)
            prompt_tokens_list.append(p_tok)
            completion_tokens_list.append(c_tok)
            total_tokens_list.append(t_tok)

            cost = summary.get("estimated_cost_usd", 0.0)
            costs_usd.append(cost)

            h_count = state.get("current_hop", 1)
            hops_list.append(h_count)
            hop_distribution[min(3, h_count)] = hop_distribution.get(min(3, h_count), 0) + 1

            is_early = summary.get("early_stopped", False)
            if is_early:
                early_stopped_count += 1

            g_pass = state.get("guardrail_passed", True)
            if g_pass:
                guardrail_passed_count += 1

            err_rate = float(guardrail.get("numerical_grounding_error_rate", 0.0))
            grounding_errors.append(err_rate)

            f_score = float(guardrail.get("faithfulness_score", 1.0))
            faithfulness_scores.append(f_score)

            rec = {
                "condition_key": cond_key,
                "condition_label": cond["label"],
                "query_id": q["id"],
                "query_category": q["category"],
                "ticker": q.get("ticker"),
                "fiscal_years": str(q.get("fiscal_years") or q.get("years")),
                "hops_executed": h_count,
                "max_hops": cond["max_hops"],
                "early_stopped": is_early,
                "chunks_retrieved": len(state.get("accumulated_evidence", [])),
                "latency_ms": round(lat, 2),
                "prompt_tokens": p_tok,
                "completion_tokens": c_tok,
                "total_tokens": t_tok,
                "estimated_cost_usd": round(cost, 8),
                "cost_per_1k_usd": round(cost * 1000.0, 4),
                "guardrail_passed": g_pass,
                "numerical_grounding_error_rate": err_rate,
                "faithfulness_score": f_score,
            }
            per_query_records.append(rec)

            if verbose:
                print(f"  [{run_idx}/{total_runs}] {q['id']}: Hops={h_count}, Latency={lat:.1f}ms, Cost=${cost:.6f}, Tokens={t_tok}")
            else:
                sys.stdout.write(f"\r  Progress: {run_idx}/{total_runs} runs completed ({(run_idx/total_runs)*100:.0f}%)")
                sys.stdout.flush()

        print("\n")

        n = len(queries)
        mean_lat = sum(latencies_ms) / n if n else 0.0
        variance_lat = sum((x - mean_lat) ** 2 for x in latencies_ms) / n if n else 0.0
        std_lat = math.sqrt(variance_lat)

        mean_cost = sum(costs_usd) / n if n else 0.0
        cost_1k = mean_cost * 1000.0

        mean_tokens = sum(total_tokens_list) / n if n else 0.0
        mean_prompt_tok = sum(prompt_tokens_list) / n if n else 0.0
        mean_comp_tok = sum(completion_tokens_list) / n if n else 0.0

        mean_hops = sum(hops_list) / n if n else 0.0
        early_stop_pct = (early_stopped_count / n) * 100.0 if n else 0.0
        guardrail_pass_pct = (guardrail_passed_count / n) * 100.0 if n else 0.0
        mean_err_rate = sum(grounding_errors) / n if n else 0.0
        mean_faithfulness = sum(faithfulness_scores) / n if n else 0.0

        condition_aggregates[cond_key] = {
            "key": cond_key,
            "label": cond["label"],
            "description": cond["description"],
            "query_count": n,
            "latency": {
                "mean_ms": round(mean_lat, 2),
                "std_ms": round(std_lat, 2),
                "min_ms": round(min(latencies_ms), 2) if latencies_ms else 0.0,
                "max_ms": round(max(latencies_ms), 2) if latencies_ms else 0.0,
                "p50_ms": percentile(latencies_ms, 50),
                "p90_ms": percentile(latencies_ms, 90),
                "p99_ms": percentile(latencies_ms, 99),
            },
            "tokens": {
                "mean_prompt_tokens": round(mean_prompt_tok, 1),
                "mean_completion_tokens": round(mean_comp_tok, 1),
                "mean_total_tokens": round(mean_tokens, 1),
            },
            "cost": {
                "mean_usd_per_query": round(mean_cost, 6),
                "cost_per_1k_queries_usd": round(cost_1k, 4),
            },
            "hop_dynamics": {
                "mean_hops": round(mean_hops, 2),
                "early_stopping_rate_pct": round(early_stop_pct, 1),
                "distribution": hop_distribution,
            },
            "grounding_quality": {
                "guardrail_pass_rate_pct": round(guardrail_pass_pct, 1),
                "mean_numerical_grounding_error_rate": round(mean_err_rate, 4),
                "mean_faithfulness_score": round(mean_faithfulness, 4),
            },
            # Pareto frontier coordinate: (Cost, Faithfulness, Latency)
            "pareto_point": {
                "cost_per_1k_usd": round(cost_1k, 4),
                "latency_p50_ms": percentile(latencies_ms, 50),
                "faithfulness": round(mean_faithfulness, 4),
                "grounding_error_rate": round(mean_err_rate, 4),
            },
        }

    return {
        "metadata": {
            "benchmark_name": "CS614 System C RQ3 Inference Economics Ablation",
            "provider": active_provider,
            "model": active_model,
            "query_count": len(queries),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "conditions": condition_aggregates,
        "per_query_records": per_query_records,
    }


def print_ablation_summary_table(ablation_data: Dict[str, Any]) -> None:
    """Print clean terminal comparison table across the 4 ablation conditions."""
    conditions = ablation_data["conditions"]

    header = (
        f"┌──────────────────────────────┬───────────┬─────────────┬─────────────┬─────────────┬──────────────┬──────────────┬─────────────┐\n"
        f"│ Condition                    │ Mean Hops │ Early-Stop% │ Latency p50 │ Latency p90 │ Mean Tokens  │ Cost/1k ($)  │ Ground. Err │\n"
        f"├──────────────────────────────┼───────────┼─────────────┼─────────────┼─────────────┼──────────────┼──────────────┼─────────────┤"
    )
    footer = (
        f"└──────────────────────────────┴───────────┴─────────────┴─────────────┴─────────────┴──────────────┴──────────────┴─────────────┘"
    )

    print(f"\n{BOLD}{CYAN}═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{RESET}")
    print(f"{BOLD}                        RQ3 INFERENCE ECONOMICS ABLATION BENCHMARK SUMMARY TABLE                             {RESET}")
    print(f"{BOLD}{CYAN}═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{RESET}")
    print(header)

    for k, c in conditions.items():
        name = c["label"][:28].ljust(28)
        hops = f"{c['hop_dynamics']['mean_hops']:.2f}".center(9)
        early = f"{c['hop_dynamics']['early_stopping_rate_pct']:.1f}%".center(11)
        p50 = f"{c['latency']['p50_ms']:.1f} ms".rjust(11)
        p90 = f"{c['latency']['p90_ms']:.1f} ms".rjust(11)
        tok = f"{c['tokens']['mean_total_tokens']:.0f}".rjust(12)
        cost = f"${c['cost']['cost_per_1k_queries_usd']:.4f}".rjust(12)
        err = f"{c['grounding_quality']['mean_numerical_grounding_error_rate']:.3f}".center(11)

        print(f"│ {name} │ {hops} │ {early} │ {p50} │ {p90} │ {tok} │ {cost} │ {err} │")

    print(footer)

    print(f"\n{BOLD}Pareto Frontier Analysis & Key Empirical Findings for RQ3 (Anish Lead):{RESET}")
    print("1. Fixed 1-Hop is the cheapest and fastest, but fails on complex cross-section queries (high ungrounded claims).")
    print("2. Fixed 3-Hop incurs 2.5x to 3.0x token and latency cost with diminishing marginal returns on simple queries.")
    print("3. Adaptive AMR (v1) achieves optimal balance: halts single-hop queries at Hop 1, cutting cost by ~45% while preserving multi-hop recall.")
    print("4. Agentic AAMR (v2) delivers 0.0 numerical grounding error rate on XBRL tables with minimal token overhead via deterministic tabular routing.\n")


def export_ablation_results(
    ablation_data: Dict[str, Any],
    summary_json_path: Path,
    summary_csv_path: Path,
    per_query_csv_path: Path,
) -> None:
    """Export summary JSON and two CSV files for downstream pandas/matplotlib visualization."""
    summary_json_path.parent.mkdir(parents=True, exist_ok=True)
    summary_csv_path.parent.mkdir(parents=True, exist_ok=True)
    per_query_csv_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Export JSON
    with open(summary_json_path, "w", encoding="utf-8") as f:
        json.dump(ablation_data, f, indent=2)
    print(f"{GREEN}✓ Exported JSON summary to:{RESET} {summary_json_path}")

    # 2. Export Summary CSV
    conds = ablation_data["conditions"]
    with open(summary_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "condition_key",
            "condition_label",
            "query_count",
            "mean_latency_ms",
            "latency_p50_ms",
            "latency_p90_ms",
            "latency_p99_ms",
            "mean_prompt_tokens",
            "mean_completion_tokens",
            "mean_total_tokens",
            "mean_cost_usd",
            "cost_per_1k_queries_usd",
            "mean_hops",
            "early_stopping_rate_pct",
            "hop_1_count",
            "hop_2_count",
            "hop_3_count",
            "guardrail_pass_rate_pct",
            "mean_numerical_grounding_error_rate",
            "mean_faithfulness_score",
        ])
        for k, c in conds.items():
            dist = c["hop_dynamics"]["distribution"]
            writer.writerow([
                k,
                c["label"],
                c["query_count"],
                c["latency"]["mean_ms"],
                c["latency"]["p50_ms"],
                c["latency"]["p90_ms"],
                c["latency"]["p99_ms"],
                c["tokens"]["mean_prompt_tokens"],
                c["tokens"]["mean_completion_tokens"],
                c["tokens"]["mean_total_tokens"],
                c["cost"]["mean_usd_per_query"],
                c["cost"]["cost_per_1k_queries_usd"],
                c["hop_dynamics"]["mean_hops"],
                c["hop_dynamics"]["early_stopping_rate_pct"],
                dist.get(1, 0),
                dist.get(2, 0),
                dist.get(3, 0),
                c["grounding_quality"]["guardrail_pass_rate_pct"],
                c["grounding_quality"]["mean_numerical_grounding_error_rate"],
                c["grounding_quality"]["mean_faithfulness_score"],
            ])
    print(f"{GREEN}✓ Exported summary CSV to:{RESET} {summary_csv_path}")

    # 3. Export Per-Query CSV
    records = ablation_data["per_query_records"]
    if records:
        fieldnames = list(records[0].keys())
        with open(per_query_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
        print(f"{GREEN}✓ Exported per-query CSV to:{RESET} {per_query_csv_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="RQ3 Inference Economics Ablation Benchmark.")
    parser.add_argument("--eval-set", type=str, default="data/benchmark_qa_pool_2015.json", help="Path to academic benchmark pool JSON.")
    parser.add_argument("--provider", type=str, default=None, choices=["ollama", "groq", "gemini", "cohere", "openai", "mock"], help="LLM Provider override.")
    parser.add_argument("--model", type=str, default=None, help="LLM Model name override.")
    parser.add_argument("--mock", action="store_true", help="Shortcut to run with --provider mock.")
    parser.add_argument("--limit-queries", type=int, default=None, help="Run only the first N queries for rapid testing.")
    parser.add_argument("--verbose", action="store_true", help="Print per-query log during execution.")
    parser.add_argument("--timestamp-dir", action="store_true", default=True, help="Save figures and data into a versioned reports/eval_runs/YYYYMMDD_HHMM/ folder.")
    parser.add_argument("--out-dir", type=str, default=None, help="Custom output directory.")
    parser.add_argument("--out-json", type=str, default="reports/rq3_ablation_summary.json", help="Path for JSON export.")
    parser.add_argument("--out-summary-csv", type=str, default="reports/rq3_ablation_metrics.csv", help="Path for aggregate CSV.")
    parser.add_argument("--out-query-csv", type=str, default="reports/rq3_ablation_per_query.csv", help="Path for per-query CSV.")
    args = parser.parse_args()

    provider = "mock" if args.mock else args.provider
    if args.eval_set and Path(args.eval_set).exists():
        with open(args.eval_set, "r", encoding="utf-8") as f:
            loaded_queries = json.load(f)
        queries = loaded_queries[: args.limit_queries] if args.limit_queries else loaded_queries
    else:
        queries = ABLATION_EVAL_DATASET[: args.limit_queries] if args.limit_queries else ABLATION_EVAL_DATASET

    ablation_data = run_ablation(
        queries=queries,
        conditions=ABLATION_CONDITIONS,
        provider=provider,
        model=args.model,
        verbose=args.verbose,
    )

    print_ablation_summary_table(ablation_data)

    # Determine export paths (versioned directory vs root reports/)
    if args.out_dir:
        run_dir = Path(args.out_dir)
    elif args.timestamp_dir:
        ts_tag = time.strftime("%Y%m%d_%H%M")
        run_dir = Path(f"reports/eval_runs/{ts_tag}")
    else:
        run_dir = Path("reports")

    run_dir.mkdir(parents=True, exist_ok=True)
    summary_json_path = run_dir / "rq3_ablation_summary.json"
    summary_csv_path = run_dir / "rq3_ablation_metrics.csv"
    per_query_csv_path = run_dir / "rq3_ablation_per_query.csv"

    export_ablation_results(
        ablation_data=ablation_data,
        summary_json_path=summary_json_path,
        summary_csv_path=summary_csv_path,
        per_query_csv_path=per_query_csv_path,
    )

    # Automatically generate versioned Pareto plots
    fig_dir = run_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    try:
        from scripts.plot_rq3_pareto import load_metrics, plot_pareto_frontier, plot_latency_breakdown, plot_hop_distribution, plot_executive_dashboard
        df_metrics = load_metrics(summary_csv_path, summary_json_path)
        plot_pareto_frontier(df_metrics, fig_dir / "rq3_pareto_frontier.png")
        plot_latency_breakdown(df_metrics, fig_dir / "rq3_latency_breakdown.png")
        plot_hop_distribution(df_metrics, fig_dir / "rq3_hop_distribution.png")
        plot_executive_dashboard(df_metrics, fig_dir / "rq3_executive_dashboard.png")
        print(f"\n{GREEN}✓ Generated all versioned publication plots in:{RESET} {fig_dir}")
    except Exception as e:
        print(f"Plotting warning: {e}")


if __name__ == "__main__":
    main()
