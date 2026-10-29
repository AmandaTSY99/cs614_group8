#!/usr/bin/env python3
"""
RQ3 Controlled Batch Experiment Runner: Inference Economics across 4+1 RAG Systems.

Evaluates 5 systems head-to-head on the standardized benchmark pool:
1. `system_a`: Vanilla Dense Baseline (rag5 contextual headers, 1 LLM call)
2. `system_b`: Advanced Single-Pass Hybrid RAG (Okapi BM25 + dense + cross-encoder rerank, 1 LLM call)
3. `system_c_v1`: Adaptive Multi-Hop RAG (AMR: dynamic 1-3 hops + Sufficiency Critic + Guardrail)
4. `system_c_v2`: Agentic Adaptive Multi-Hop RAG (AAMR: XBRL tabular tool + dynamic 1-3 hops + Guardrail)
5. `system_c_fixed_3hop`: Unconditioned 3-Hop Ablation Control (force_max_hops=True)

Hardened Experimental Protocol:
- Confounder Control: 3-query burn-in warmup to eliminate PyTorch GPU & DB cold starts.
- Serialization Control: Randomized query execution order to mitigate provider KV-cache bias.
- Anti-Leakage Firewall: Strips answer, program, key_points, and gold evidence before execution.
- Resumability: Line-by-line JSONL streaming with auto-skip on completed (system, question_id) pairs.
"""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import random
import sys
import time
from typing import Any, Dict, List, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.rq2.adapters import ADAPTER_KEYS, get_adapters
from src.system_a.evaluate import numeric_correct, keypoint_recall
from src.system_c.benchmark_adapter import run_finqa_program

DEFAULT_BENCHMARK_2015 = REPO_ROOT / "data" / "benchmark_qa_pool_2015.json"
DEFAULT_RECORDS_FILE = REPO_ROOT / "reports" / "rq3" / "records.jsonl"
DEFAULT_ERRORS_FILE = REPO_ROOT / "reports" / "rq3" / "errors.jsonl"

ALL_SYSTEMS = ["system_a", "system_b", "system_c_v1", "system_c_v2"]


def load_benchmark_records(path: Path, min_year: int = 2015) -> List[Dict[str, Any]]:
    """Load benchmark records, filtering by min_year if reading raw benchmark_qa_0.jsonl."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Benchmark file not found: {path}")

    text = path.read_text(encoding="utf-8")
    raw_records = json.loads(text) if path.suffix == ".json" else [json.loads(l) for l in text.splitlines() if l.strip()]

    filtered = []
    for r in raw_records:
        years = set()
        if r.get("year"):
            years.add(int(r["year"]))
        for ev in r.get("gold_evidence", []):
            if ev.get("year"):
                years.add(int(ev["year"]))
        if all(y >= min_year for y in years):
            filtered.append(r)
    return filtered


def sanitize_input_for_system(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    STRICT ANTI-LEAKAGE FIREWALL:
    Construct clean system input with query and (ticker, year) scope only.
    Excludes ground-truth answer, program, key_points, and evidence text/sections.
    """
    years = [int(y) for y in (item.get("applicable_years") or []) if y]
    if item.get("year") and int(item["year"]) not in years:
        years.append(int(item["year"]))
    for ev in item.get("gold_evidence") or []:
        if ev.get("year") and int(ev["year"]) not in years:
            years.append(int(ev["year"]))
    years = sorted(years)

    raw_tickers = []
    if isinstance(item.get("target_tickers"), list):
        raw_tickers.extend(item["target_tickers"])
    elif item.get("ticker"):
        raw_tickers.append(item["ticker"])

    tickers = []
    for t in raw_tickers:
        if isinstance(t, str) and "," in t:
            tickers.extend([part.strip().upper() for part in t.split(",") if part.strip()])
        elif t:
            tickers.append(str(t).strip().upper())
    if item.get("comparison_tickers"):
        tickers.extend([t.upper() for t in item["comparison_tickers"] if t.upper() not in tickers])
    for ev in item.get("gold_evidence") or []:
        if ev.get("ticker") and ev["ticker"].upper() not in tickers:
            tickers.append(ev["ticker"].upper())
    tickers = sorted(list(dict.fromkeys(tickers)))

    qid = item.get("id") or item.get("query_id") or ""
    q_text = item.get("question") or item.get("query") or ""

    ev_pairs = list(dict.fromkeys(
        (ev["ticker"], int(ev["year"]))
        for ev in (item.get("gold_evidence") or [])
        if ev.get("ticker") and ev.get("year")
    ))
    pairs = ev_pairs if ev_pairs else ([(t, y) for t in tickers for y in years] if tickers and years else [])
    return {
        "id": qid,
        "query_id": qid,
        "query": q_text,
        "question": q_text,
        "ticker": tickers[0] if tickers else None,
        "target_tickers": tickers,
        "fiscal_years": years,
        "target_pairs": pairs,
        "scope": pairs,
    }


def load_done_pairs_and_cost(records_path: Path) -> Tuple[Set[Tuple[str, str]], float]:
    """Return set of completed (system, question_id) pairs and cumulative spend to support resuming."""
    done = set()
    total_cost = 0.0
    if records_path.exists():
        for line in records_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                done.add((row["system"], row["question_id"]))
                cost = row.get("cost_usd") or row.get("estimated_cost_usd") or 0.0
                total_cost += float(cost)
            except Exception:
                continue
    return done, total_cost


def load_done_pairs(records_path: Path) -> Set[Tuple[str, str]]:
    """Return set of completed (system, question_id) pairs to support resuming."""
    done, _ = load_done_pairs_and_cost(records_path)
    return done


def run_warmup_queries(adapter, system_name: str, count: int = 3):
    """Burn-in warmup phase to eliminate cold starts (PyTorch weights, CUDA context, DB pools)."""
    dummy_q = {
        "id": "WARMUP-000",
        "query": "What is the company's fiscal year end date and total revenue?",
        "question": "What is the company's fiscal year end date and total revenue?",
        "ticker": "NVDA",
        "target_tickers": ["NVDA"],
        "fiscal_years": [2026],
    }
    print(f"  [{system_name}] Running {count} warmup queries...", end="", flush=True)
    for _ in range(count):
        try:
            adapter.answer(dummy_q)
        except Exception:
            pass
    print(" complete.")


def run_experiment(
    systems: List[str],
    benchmark_path: Path,
    out_records_path: Path,
    out_errors_path: Path,
    min_year: int = 2015,
    limit: Optional[int] = None,
    seed: int = 42,
    warmup_count: int = 3,
    verbose: bool = True,
    mock: bool = False,
    clean: bool = False,
    fail_fast: bool = True,
    max_budget_usd: float = 2.0,
) -> Dict[str, int]:
    """Execute the controlled RQ3 benchmark experiment across the specified systems with a strict cost ceiling."""
    if mock:
        os.environ["LLM_PROVIDER"] = "mock"

    out_records_path = Path(out_records_path)
    out_errors_path = Path(out_errors_path)
    out_records_path.parent.mkdir(parents=True, exist_ok=True)
    out_errors_path.parent.mkdir(parents=True, exist_ok=True)

    if clean:
        if out_records_path.exists():
            out_records_path.unlink()
        if out_errors_path.exists():
            out_errors_path.unlink()

    questions = load_benchmark_records(benchmark_path, min_year=min_year)
    if limit:
        questions = questions[:limit]

    print(f"Loaded {len(questions)} benchmark questions (min_year={min_year}) for systems: {systems}")
    print(f"Financial Guardrail Active: Strict budget ceiling = ${max_budget_usd:.2f}")
    adapters = get_adapters(systems)
    done_pairs, cumulative_cost = load_done_pairs_and_cost(out_records_path)
    counts = {"generated": 0, "skipped": 0, "failed": 0}

    if cumulative_cost >= max_budget_usd:
        print("\n" + "=" * 80, file=sys.stderr)
        print("🛑 LOUD STOP: Prior experiment records have already reached the budget limit!", file=sys.stderr)
        print(f"Cumulative spend: ${cumulative_cost:.4f} >= ${max_budget_usd:.2f} max budget.", file=sys.stderr)
        print("Aborting before starting to protect your API budget.", file=sys.stderr)
        print("=" * 80 + "\n", file=sys.stderr)
        raise RuntimeError(f"Strict budget cutoff exceeded: Prior spend ${cumulative_cost:.4f} >= ${max_budget_usd:.2f}.")

    # 1. Run Warmup Phase per system
    if warmup_count > 0:
        for sys_name in systems:
            run_warmup_queries(adapters[sys_name], sys_name, count=warmup_count)

    # 2. Build Randomized Execution Queue (mitigates provider prefix-cache bias)
    execution_queue = []
    for q in questions:
        for sys_name in systems:
            if (sys_name, q["id"]) in done_pairs:
                counts["skipped"] += 1
            else:
                execution_queue.append((sys_name, q))

    random.seed(seed)
    random.shuffle(execution_queue)

    total_tasks = len(execution_queue)
    print(f"Starting execution: {total_tasks} queries remaining ({counts['skipped']} already completed) | Current spend: ${cumulative_cost:.4f}\n")

    with out_records_path.open("a", encoding="utf-8") as rf, out_errors_path.open("a", encoding="utf-8") as ef:
        for idx, (sys_name, q) in enumerate(execution_queue, 1):
            sanitized_q = sanitize_input_for_system(q)
            t_start = time.perf_counter()
            try:
                out = adapters[sys_name].answer(sanitized_q)
                elapsed_ms = (time.perf_counter() - t_start) * 1000.0

                # Track cumulative financial spend
                q_cost = float(out.get("cost_usd") or 0.0)
                cumulative_cost += q_cost

                # Compute Time-Per-Output-Token (TPOT)
                comp_tokens = out["tokens"].get("completion", 0)
                gen_ms = out.get("stage_timings_ms", {}).get("generation_ms") or (
                    out.get("stage_timings_ms", {}).get("synthesis_ms") or elapsed_ms
                )
                tpot_ms = round(gen_ms / max(1, comp_tokens), 2) if comp_tokens > 0 else 0.0

                # Post-hoc evaluation against ground-truth targets (zero leakage during generation)
                ans_text = out.get("answer", "")
                num_correct = numeric_correct(q["answer"], ans_text) if q.get("answer") else None
                kp_recall = keypoint_recall(q.get("key_points", []), ans_text) if q.get("key_points") else None
                prog_val = run_finqa_program(q.get("program", "")) if q.get("program") else None

                qid = q.get("id") or q.get("query_id")
                from scripts.rq2.common import _derive_category, _NUM_UNIT_RE
                t_secs = list(dict.fromkeys(
                    ev.get("item") for ev in (q.get("gold_evidence") or []) if ev.get("item")
                ))
                gt_nums: List[str] = []
                if q.get("type") in ("numeric", "mixed") and q.get("answer"):
                    m_num = _NUM_UNIT_RE.search(str(q["answer"]))
                    if m_num:
                        gt_nums = [m_num.group(0).strip()]

                record = {
                    "status": "ok",
                    "system": sys_name,
                    "question_id": qid,
                    "query_id": qid,
                    "category": q.get("category") or _derive_category(q),
                    "recipe": q.get("recipe"),
                    "hop": q.get("hop"),
                    "type": q.get("type"),
                    "question": q["question"],
                    "ground_truth_answer": q.get("answer"),
                    "ground_truth_numbers": gt_nums,
                    "target_sections": t_secs,
                    "gold_program_result": prog_val,
                    "answer": ans_text,
                    "prediction": ans_text,
                    "retrieved_contexts": out.get("retrieved_contexts", []),
                    "contexts_meta": out.get("contexts_meta", []),
                    "citations": out.get("citations", []),
                    "guardrail_report": out.get("guardrail_report"),
                    "numeric_correct": num_correct,
                    "keypoint_recall": kp_recall,
                    "hops": out["hops"],
                    "tokens": out["tokens"],
                    "token_metrics": out["tokens"],
                    "tokens_total": out["tokens"].get("total", 0) if isinstance(out.get("tokens"), dict) else 0,
                    "cost_usd": out["cost_usd"],
                    "estimated_cost_usd": out["cost_usd"],
                    "latency_ms": out["latency_ms"],
                    "stage_timings_ms": out.get("stage_timings_ms", {}),
                    "tpot_ms": tpot_ms,
                    "tpot_ms_per_token": tpot_ms,
                    "model": out["model"],
                    "provider": out["provider"],
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                rf.write(json.dumps(record, ensure_ascii=False) + "\n")
                rf.flush()
                counts["generated"] += 1

                if verbose:
                    status_line = (
                        f"[{idx}/{total_tasks}] {sys_name:<16} | {q['id']} | "
                        f"hops={out['hops']} | lat={out['latency_ms']:.0f}ms | "
                        f"tokens={out['tokens']['total']:<4} | cost=${q_cost:.5f} | "
                        f"total_spent=${cumulative_cost:.4f}/${max_budget_usd:.2f} | num_ok={num_correct}"
                    )
                    print(status_line)

                # Strict budget ceiling enforcement
                if cumulative_cost >= max_budget_usd:
                    budget_err = (
                        f"Strict financial stop: Cumulative spend ${cumulative_cost:.4f} "
                        f"reached or exceeded the strict cutoff threshold of ${max_budget_usd:.2f}."
                    )
                    err_record = {
                        "system": sys_name,
                        "question_id": q["id"],
                        "error": f"BudgetExceededError: {budget_err}",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                    ef.write(json.dumps(err_record, ensure_ascii=False) + "\n")
                    ef.flush()
                    print("\n" + "=" * 80, file=sys.stderr)
                    print("🛑 LOUD STOP: Strict Budget Cutoff Guardrail Triggered!", file=sys.stderr)
                    print(budget_err, file=sys.stderr)
                    print("Execution halted immediately to protect your API budget.", file=sys.stderr)
                    print("=" * 80 + "\n", file=sys.stderr)
                    raise RuntimeError(budget_err)

            except Exception as exc:
                counts["failed"] += 1
                err_record = {
                    "system": sys_name,
                    "question_id": q["id"],
                    "error": f"{type(exc).__name__}: {exc}",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                ef.write(json.dumps(err_record, ensure_ascii=False) + "\n")
                ef.flush()
                import traceback
                print("\n" + "=" * 80, file=sys.stderr)
                print(f"❌ LOUD STOP: System [{sys_name}] failed on Question [{q['id']}]!", file=sys.stderr)
                print(f"Error Type: {type(exc).__name__}", file=sys.stderr)
                print(f"Error Message: {exc}", file=sys.stderr)
                traceback.print_exc()
                print("=" * 80 + "\n", file=sys.stderr)
                if fail_fast:
                    raise exc

    return counts


def main():
    parser = argparse.ArgumentParser(description="Run RQ3 Inference Economics Batch Experiment.")
    parser.add_argument("--systems", nargs="+", default=ALL_SYSTEMS, help=f"Systems to evaluate (default: {ALL_SYSTEMS})")
    parser.add_argument("--benchmark", type=Path, default=DEFAULT_BENCHMARK_2015, help="Path to benchmark JSON/JSONL.")
    parser.add_argument("--min-year", type=int, default=2015, help="Minimum fiscal year constraint (default: 2015).")
    parser.add_argument("--limit", type=int, default=None, help="Limit to first N questions.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for query queue shuffle.")
    parser.add_argument("--warmup", type=int, default=3, help="Number of warmup queries per system (default: 3).")
    parser.add_argument("--mock", action="store_true", help="Force mock LLM provider for zero-cost rapid testing.")
    parser.add_argument("--clean", action="store_true", help="Clean prior output records before starting (disable resume).")
    parser.add_argument("--no-fail-fast", action="store_true", help="Continue running other queries if a query fails (default is loud stop).")
    parser.add_argument("--max-budget-usd", type=float, default=float(os.getenv("MAX_BUDGET_USD", "2.0")), help="Strict financial cutoff ceiling in USD (default: $2.00).")
    parser.add_argument("--records-out", type=Path, default=DEFAULT_RECORDS_FILE, help="Path to write records JSONL.")
    parser.add_argument("--errors-out", type=Path, default=DEFAULT_ERRORS_FILE, help="Path to write errors JSONL.")
    args = parser.parse_args()

    if args.mock:
        os.environ["LLM_PROVIDER"] = "mock"

    counts = run_experiment(
        systems=args.systems,
        benchmark_path=args.benchmark,
        out_records_path=args.records_out,
        out_errors_path=args.errors_out,
        min_year=args.min_year,
        limit=args.limit,
        seed=args.seed,
        warmup_count=args.warmup,
        clean=args.clean,
        fail_fast=not args.no_fail_fast,
        max_budget_usd=args.max_budget_usd,
    )
    print("\n" + "=" * 60)
    print(f"RQ3 Experiment Complete: {counts['generated']} generated, {counts['skipped']} skipped, {counts['failed']} failed")
    print(f"Records saved to: {args.records_out}")


if __name__ == "__main__":
    main()
