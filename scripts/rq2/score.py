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
from scripts.rq2.common import (  # noqa: E402
    RECORDS_FILE, REPO_ROOT, SCORES_FILE, _derive_category, append_jsonl, benchmark_index, now_iso,
    question_dimensions, ragas_reference, read_jsonl,
)
from scripts.rq2.metrics_custom import custom_scores, is_abstention, strip_citation_tags  # noqa: E402

LLM_METRICS = ["faithfulness", "answer_relevancy", "context_recall", "context_precision", "factual_correctness"]
CUSTOM_METRICS = ["citation_precision", "citation_recall", "citation_f1", "citation_coverage",
                  "numeric_accuracy", "grounding_error_rate", "abstained"]
ALL_METRICS = LLM_METRICS + CUSTOM_METRICS
NO_JUDGE = "none"
CIRCUIT_BREAKER_FAILURES = 5
# Factual correctness: `f1` also penalises correct extra statements (e.g. intermediate figures); `recall` only
# asks whether the answer contains the reference's claims. Reference: gold answer, gold answer + key points, or
# "Question: … Answer: …" + key points. Atomicity `high` splits the reference into one claim per fact.
FC_MODES = ("f1", "recall")
FC_REFERENCES = ("answer", "answer_keypoints", "question_answer_keypoints")
FC_ATOMICITIES = ("low", "high")
DEFAULT_FC_MODE = "f1"
DEFAULT_FC_REFERENCE = "answer_keypoints"
DEFAULT_FC_ATOMICITY = "low"


def fc_tag(fc_mode: str, fc_reference: str, fc_atomicity: str = DEFAULT_FC_ATOMICITY) -> str:
    return f"fc_mode={fc_mode}; fc_reference={fc_reference}; fc_atomicity={fc_atomicity}"


def make_metric(name: str, llm: Any, embeddings: Any = None, fc_mode: str = DEFAULT_FC_MODE,
                fc_atomicity: str = DEFAULT_FC_ATOMICITY) -> Any:
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
        return m.FactualCorrectness(llm=llm, mode=fc_mode, atomicity=fc_atomicity, coverage="low")
    raise ValueError(f"unknown RAGAS metric {name}")


def metric_inputs(name: str, record: Dict[str, Any],
                  fc_reference: str = DEFAULT_FC_REFERENCE) -> Optional[Dict[str, Any]]:
    """`ascore` kwargs for one metric, or None if the record lacks what the metric needs (-> status na)."""
    question = record.get("question") or ""
    response = strip_citation_tags(record.get("answer") or "")
    contexts = [c for c in (record.get("retrieved_contexts") or []) if c]  # order kept as produced
    ref = record.get("ragas_reference") or {}
    reference = ref.get(fc_reference) or record.get("ground_truth_answer") or ""
    evidence_reference = ref.get("evidence") or reference
    if name == "faithfulness":
        return dict(user_input=question, response=response, retrieved_contexts=contexts) if response and contexts else None
    if name == "answer_relevancy":
        return dict(user_input=question, response=response) if response else None
    if name == "context_recall":
        return (dict(user_input=question, retrieved_contexts=contexts, reference=evidence_reference)
                if contexts and evidence_reference else None)
    if name == "context_precision":
        return (dict(user_input=question, reference=evidence_reference, retrieved_contexts=contexts)
                if contexts and evidence_reference else None)
    if name == "factual_correctness":
        return dict(response=response, reference=reference) if response and reference else None
    raise ValueError(f"unknown RAGAS metric {name}")


def enrich_record(record: Dict[str, Any], benchmark: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Category, proposal dimensions and RAGAS references from the benchmark question (not stored in records)."""
    q = benchmark.get(str(record.get("question_id")))
    if not q:
        return record
    q = {k: v for k, v in q.items() if k != "category"}
    return {**record, "category": _derive_category(q), "dims": question_dimensions(q), "ragas_reference": ragas_reference(q)}


def _row(record: Dict[str, Any], metric: str, value: Optional[float], status: str, judge: str,
         detail: str = "", attempts: int = 0, usage: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    usage = usage or {}
    return {
        "system": record["system"],
        "question_id": record["question_id"],
        "category": record.get("category"),
        "dims": record.get("dims") or {},
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
    fc_mode: str = DEFAULT_FC_MODE,
    fc_reference: str = DEFAULT_FC_REFERENCE,
    fc_atomicity: str = DEFAULT_FC_ATOMICITY,
) -> Dict[str, Any]:
    # Factual-correctness rows carry their mode, reference and atomicity, so scores files stay traceable.
    tag = fc_tag(fc_mode, fc_reference, fc_atomicity) if metric == "factual_correctness" else ""

    def detail(text: str = "") -> str:
        return "; ".join(t for t in (tag, text) if t)

    # A refusal ("Not found in the provided context") has no claims, so RAGAS would score it as fully faithful
    # and fully correct. It is counted by the `abstained` metric instead: not faithful-or-unfaithful, and wrong.
    if metric in ("faithfulness", "factual_correctness") and is_abstention(record.get("answer") or ""):
        if metric == "faithfulness":
            return _row(record, metric, None, J.STATUS_NA, judge, "abstained (counted in abstained)")
        return _row(record, metric, 0.0, J.STATUS_OK, judge, detail("abstained: no answer given"))
    inputs = metric_inputs(metric, record, fc_reference)
    if inputs is None:
        return _row(record, metric, None, J.STATUS_NA, judge, detail("missing answer, contexts or reference"))
    key = (record["system"], record["question_id"], metric)
    meter.start(key)
    try:
        result, attempts = await J.call_with_retry(lambda: metric_obj.ascore(**inputs), sleep=sleep)
    except J.JudgeCallError as exc:
        status = J.STATUS_TOO_LARGE if exc.kind == J.ERROR_TOO_LARGE else J.STATUS_ERROR
        return _row(record, metric, None, status, judge, detail(str(exc)), exc.attempts, meter.snapshot(key))
    value = getattr(result, "value", result)
    try:
        value = float(value)
    except (TypeError, ValueError):
        return _row(record, metric, None, J.STATUS_ERROR, judge, detail(f"non-numeric result {value!r}"), attempts,
                    meter.snapshot(key))
    return _row(record, metric, value, J.STATUS_OK, judge, detail(), attempts, meter.snapshot(key))


async def score_run(
    run_path: Path,
    metrics: List[str],
    judge_provider: str = J.DEFAULT_JUDGE_PROVIDER,
    judge_model: str = J.DEFAULT_JUDGE_MODEL,
    concurrency: int = 1,
    scores_file: str = SCORES_FILE,
    metric_factory: Optional[Callable[..., Any]] = None,
    llm: Any = None,
    embeddings: Any = None,
    meter: Optional[J.JudgeMeter] = None,
    sleep: Callable[[float], Any] = asyncio.sleep,
    benchmark: Optional[Dict[str, Dict[str, Any]]] = None,
    fc_mode: str = DEFAULT_FC_MODE,
    fc_reference: str = DEFAULT_FC_REFERENCE,
    fc_atomicity: str = DEFAULT_FC_ATOMICITY,
) -> Dict[str, int]:
    if fc_mode not in FC_MODES or fc_reference not in FC_REFERENCES or fc_atomicity not in FC_ATOMICITIES:
        raise ValueError(f"fc_mode must be one of {FC_MODES}, fc_reference one of {FC_REFERENCES} and "
                         f"fc_atomicity one of {FC_ATOMICITIES}")
    metric_factory = metric_factory or (
        lambda name, llm_, emb: make_metric(name, llm_, emb, fc_mode=fc_mode, fc_atomicity=fc_atomicity))
    benchmark = benchmark_index() if benchmark is None else benchmark
    records = [enrich_record(r, benchmark) for r in read_jsonl(run_path / RECORDS_FILE)]
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
    breaker = {"consecutive": 0, "stopped": None}

    async def one(rec: Dict[str, Any], metric: str) -> None:
        async with semaphore:
            if breaker["stopped"]:
                return  # not written, so a later run picks it up
            row = await score_llm_metric(rec, metric, metric_objs[metric], judge, meter, sleep, fc_mode, fc_reference,
                                         fc_atomicity)
            append_jsonl(scores_path, row)
            counts["scored"] += 1
            print(f"  {rec['system']} {rec['question_id']} {metric}: {row['status']} {row['value']} "
                  f"(calls={row['judge_calls']}, tokens={row['judge_prompt_tokens'] + row['judge_completion_tokens']})",
                  flush=True)
            # Circuit breaker: consecutive calls that still failed after all retries (too_large is neutral).
            if row["status"] == J.STATUS_ERROR:
                breaker["consecutive"] += 1
                if breaker["consecutive"] >= CIRCUIT_BREAKER_FAILURES and not breaker["stopped"]:
                    breaker["stopped"] = (
                        f"{CIRCUIT_BREAKER_FAILURES} consecutive judge calls failed after all retries; "
                        f"last: {row['detail'][:300]}"
                    )
                    print(f"STOPPING: {breaker['stopped']}. Progress is saved in {scores_path}; "
                          "rerun to resume.", flush=True)
            elif row["status"] in (J.STATUS_OK, J.STATUS_NA):
                breaker["consecutive"] = 0

    await asyncio.gather(*(asyncio.create_task(one(rec, m)) for rec, m in llm_todo))
    if breaker["stopped"]:
        counts["stopped"] = breaker["stopped"]
    return counts


def main() -> None:
    p = argparse.ArgumentParser(description="RQ2 Stage 2: score generated records.")
    p.add_argument("--run", required=True, help="Run directory, e.g. reports/rq2/smoke")
    p.add_argument("--metrics", default=",".join(ALL_METRICS))
    p.add_argument("--concurrency", type=int, default=1, help="Parallel judge calls (1-2).")
    p.add_argument("--scores-file", default=SCORES_FILE)
    p.add_argument("--fc-mode", choices=FC_MODES, default=DEFAULT_FC_MODE,
                   help="Factual correctness: f1 (also penalises extra claims) or recall (answer covers the reference).")
    p.add_argument("--fc-reference", choices=FC_REFERENCES, default=DEFAULT_FC_REFERENCE,
                   help="Factual correctness reference: gold answer only, gold answer + key points, or "
                        "'Question: … Answer: …' + key points.")
    p.add_argument("--fc-atomicity", choices=FC_ATOMICITIES, default=DEFAULT_FC_ATOMICITY,
                   help="Factual correctness claim decomposition: low (few compound claims) or high (one per fact).")
    args = p.parse_args()

    from dotenv import load_dotenv

    load_dotenv(REPO_ROOT / ".env", override=False)
    provider = os.getenv("EVAL_JUDGE_PROVIDER", J.DEFAULT_JUDGE_PROVIDER).strip().lower()
    model = os.getenv("EVAL_JUDGE_MODEL", J.DEFAULT_JUDGE_MODEL).strip()
    metrics = [m.strip() for m in args.metrics.split(",") if m.strip()]
    unknown = [m for m in metrics if m not in ALL_METRICS]
    if unknown:
        raise SystemExit(f"Unknown metrics {unknown}; known: {ALL_METRICS}")
    counts = asyncio.run(score_run(Path(args.run), metrics, provider, model, args.concurrency, args.scores_file,
                                   fc_mode=args.fc_mode, fc_reference=args.fc_reference,
                                   fc_atomicity=args.fc_atomicity))
    print(f"Done: {counts} (judge {J.judge_label(provider, model)}; "
          f"{fc_tag(args.fc_mode, args.fc_reference, args.fc_atomicity)})")
    if counts.get("stopped"):
        sys.exit(2)


if __name__ == "__main__":
    main()
