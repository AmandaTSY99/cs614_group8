"""
RQ2 Stage 2 — score `records.jsonl` (`cs614-eval` env). Re-scoring never re-runs systems.

- Custom metrics (free, judge "none"): citation precision/recall/F1/coverage, numeric accuracy,
  numerical grounding error rate.
- RAGAS 0.4.3 metrics (LLM judge): faithfulness, answer_relevancy, context_recall, context_precision,
  factual_correctness.

Resumable: every finished score is appended to the scores file at once, and (system, question_id, metric)
rows already there are skipped, except `status: error` rows, which are retried. One scores file never mixes
LLM judges: scoring with a different judge needs a new `--scores-file`.

Usage:
    python scripts/rq2/score.py --run reports/rq2/smoke --concurrency 1
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.rq2 import judge as J  # noqa: E402
from scripts.rq2.common import RECORDS_FILE, REPO_ROOT, SCORES_FILE, append_jsonl, now_iso, read_jsonl  # noqa: E402
from scripts.rq2.metrics_custom import custom_scores, strip_citation_tags  # noqa: E402

LLM_METRICS = ["faithfulness", "answer_relevancy", "context_recall", "context_precision", "factual_correctness"]
CUSTOM_METRICS = ["citation_precision", "citation_recall", "citation_f1", "citation_coverage",
                  "numeric_accuracy", "grounding_error_rate"]
ALL_METRICS = LLM_METRICS + CUSTOM_METRICS
NO_JUDGE = "none"


def make_metric(name: str, llm: Any, embeddings: Any = None) -> Any:
    """ragas 0.4.3 collections metric for `name`."""
    from ragas.metrics import collections as m

    if name == "faithfulness":
        return m.Faithfulness(llm=llm)
    if name == "answer_relevancy":
        return m.AnswerRelevancy(llm=llm, embeddings=embeddings, strictness=3)
    if name == "context_recall":
        return m.ContextRecall(llm=llm)
    if name == "context_precision":
        return m.ContextPrecision(llm=llm)
    if name == "factual_correctness":
        return m.FactualCorrectness(llm=llm, mode="f1", atomicity="low", coverage="low")
    raise ValueError(f"unknown RAGAS metric {name}")


def metric_inputs(name: str, record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """`ascore` kwargs for one metric, or None if the record lacks what the metric needs (-> status na)."""
    question = record.get("question") or ""
    response = strip_citation_tags(record.get("answer") or "")
    contexts = [c for c in (record.get("retrieved_contexts") or []) if c]  # order kept as produced
    reference = record.get("ground_truth_answer") or ""
    if name == "faithfulness":
        return dict(user_input=question, response=response, retrieved_contexts=contexts) if response and contexts else None
    if name == "answer_relevancy":
        return dict(user_input=question, response=response) if response else None
    if name == "context_recall":
        return dict(user_input=question, retrieved_contexts=contexts, reference=reference) if contexts and reference else None
    if name == "context_precision":
        return dict(user_input=question, reference=reference, retrieved_contexts=contexts) if contexts and reference else None
    if name == "factual_correctness":
        return dict(response=response, reference=reference) if response and reference else None
    raise ValueError(f"unknown RAGAS metric {name}")


def _row(record: Dict[str, Any], metric: str, value: Optional[float], status: str, judge: str,
         detail: str = "", attempts: int = 0, usage: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    usage = usage or {}
    return {
        "system": record["system"],
        "question_id": record["question_id"],
        "category": record.get("category"),
        "metric": metric,
        "value": value,
        "status": status,
        "judge": judge,
        "attempts": attempts,
        "judge_calls": usage.get("calls", 0),
        "judge_prompt_tokens": usage.get("prompt_tokens", 0),
        "judge_completion_tokens": usage.get("completion_tokens", 0),
        "ratelimit": usage.get("ratelimit", {}),
        "detail": detail[:500],
        "timestamp": now_iso(),
    }


def check_single_judge(existing: List[Dict[str, Any]], judge: str) -> None:
    others = {r.get("judge") for r in existing if r.get("metric") in LLM_METRICS} - {judge, NO_JUDGE, None}
    if others:
        raise SystemExit(
            f"Scores file already has LLM scores from judge(s) {sorted(others)}; refusing to mix in '{judge}'. "
            "Use a new --scores-file to re-score everything with this judge."
        )


async def score_llm_metric(
    record: Dict[str, Any],
    metric: str,
    metric_obj: Any,
    judge: str,
    meter: J.JudgeMeter,
    sleep: Callable[[float], Any] = asyncio.sleep,
) -> Dict[str, Any]:
    inputs = metric_inputs(metric, record)
    if inputs is None:
        return _row(record, metric, None, J.STATUS_NA, judge, "missing answer, contexts or reference")
    key = (record["system"], record["question_id"], metric)
    meter.start(key)
    try:
        result, attempts = await J.call_with_retry(lambda: metric_obj.ascore(**inputs), sleep=sleep)
    except J.JudgeCallError as exc:
        status = J.STATUS_TOO_LARGE if exc.kind == J.ERROR_TOO_LARGE else J.STATUS_ERROR
        return _row(record, metric, None, status, judge, str(exc), exc.attempts, meter.snapshot(key))
    value = getattr(result, "value", result)
    try:
        value = float(value)
    except (TypeError, ValueError):
        return _row(record, metric, None, J.STATUS_ERROR, judge, f"non-numeric result {value!r}", attempts,
                    meter.snapshot(key))
    return _row(record, metric, value, J.STATUS_OK, judge, "", attempts, meter.snapshot(key))


async def score_run(
    run_path: Path,
    metrics: List[str],
    judge_provider: str = J.DEFAULT_JUDGE_PROVIDER,
    judge_model: str = J.DEFAULT_JUDGE_MODEL,
    concurrency: int = 1,
    scores_file: str = SCORES_FILE,
    metric_factory: Callable[..., Any] = make_metric,
    llm: Any = None,
    embeddings: Any = None,
    meter: Optional[J.JudgeMeter] = None,
    sleep: Callable[[float], Any] = asyncio.sleep,
) -> Dict[str, int]:
    records = read_jsonl(run_path / RECORDS_FILE)
    scores_path = run_path / scores_file
    existing = read_jsonl(scores_path)
    judge = J.judge_label(judge_provider, judge_model)
    done = {(r["system"], r["question_id"], r["metric"]) for r in existing if r.get("status") != J.STATUS_ERROR}
    counts = {"scored": 0, "skipped": 0}

    # 1. Free custom metrics
    for rec in records:
        computed = custom_scores(rec)
        for metric in metrics:
            if metric not in CUSTOM_METRICS:
                continue
            if (rec["system"], rec["question_id"], metric) in done:
                counts["skipped"] += 1
                continue
            value, status, detail = computed[metric]
            append_jsonl(scores_path, _row(rec, metric, value, status, NO_JUDGE, detail))
            counts["scored"] += 1

    # 2. RAGAS metrics with the LLM judge
    llm_todo = [(rec, m) for rec in records for m in metrics
                if m in LLM_METRICS and (rec["system"], rec["question_id"], m) not in done]
    counts["skipped"] += sum(1 for rec in records for m in metrics
                             if m in LLM_METRICS and (rec["system"], rec["question_id"], m) in done)
    if not llm_todo:
        return counts
    check_single_judge(existing, judge)
    meter = meter or J.JudgeMeter()
    if llm is None:
        llm = J.build_judge(judge_provider, judge_model, meter)
    if embeddings is None and any(m == "answer_relevancy" for _, m in llm_todo):
        embeddings = J.build_embeddings()
    metric_objs = {m: metric_factory(m, llm, embeddings) for m in {m for _, m in llm_todo}}
    semaphore = asyncio.Semaphore(max(1, min(concurrency, 2)))

    async def one(rec: Dict[str, Any], metric: str) -> None:
        async with semaphore:
            row = await score_llm_metric(rec, metric, metric_objs[metric], judge, meter, sleep)
            append_jsonl(scores_path, row)
            counts["scored"] += 1
            print(f"  {rec['system']} {rec['question_id']} {metric}: {row['status']} {row['value']} "
                  f"(calls={row['judge_calls']}, tokens={row['judge_prompt_tokens'] + row['judge_completion_tokens']})",
                  flush=True)

    await asyncio.gather(*(asyncio.create_task(one(rec, m)) for rec, m in llm_todo))
    return counts


def main() -> None:
    p = argparse.ArgumentParser(description="RQ2 Stage 2: score generated records.")
    p.add_argument("--run", required=True, help="Run directory, e.g. reports/rq2/smoke")
    p.add_argument("--metrics", default=",".join(ALL_METRICS))
    p.add_argument("--concurrency", type=int, default=1, help="Parallel judge calls (1-2).")
    p.add_argument("--scores-file", default=SCORES_FILE)
    args = p.parse_args()

    from dotenv import load_dotenv

    load_dotenv(REPO_ROOT / ".env", override=False)
    provider = os.getenv("EVAL_JUDGE_PROVIDER", J.DEFAULT_JUDGE_PROVIDER).strip().lower()
    model = os.getenv("EVAL_JUDGE_MODEL", J.DEFAULT_JUDGE_MODEL).strip()
    metrics = [m.strip() for m in args.metrics.split(",") if m.strip()]
    unknown = [m for m in metrics if m not in ALL_METRICS]
    if unknown:
        raise SystemExit(f"Unknown metrics {unknown}; known: {ALL_METRICS}")
    counts = asyncio.run(score_run(Path(args.run), metrics, provider, model, args.concurrency, args.scores_file))
    print(f"Done: {counts} (judge {J.judge_label(provider, model)})")


if __name__ == "__main__":
    main()
