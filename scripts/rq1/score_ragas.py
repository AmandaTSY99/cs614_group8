"""
RQ1 Stage 1b (optional, LLM judge, costs API credits): RAGAS 0.4.3 Context Recall and Context Precision.

These complement the lexical scores in `score.py`:
- RAGAS Context Recall: share of the *gold answer's* claims that the judge finds supported by the retrieved
  context (no gold evidence quotes involved).
- RAGAS Context Precision: average precision where the judge decides, chunk by chunk, whether each chunk
  was useful for the gold answer (one judge call per retrieved chunk).

Reuses RQ2's judge plumbing (`scripts/rq2/judge.py`, `scripts/rq2/score.py`), so it runs in the RAGAS image:
    docker compose run --rm rq2-eval python scripts/rq1/score_ragas.py --limit 2      # smoke test
    docker compose run --rm rq2-eval python scripts/rq1/score_ragas.py                # full run

Resumable: every score is appended to `reports/rq1/ragas_scores.jsonl` at once; finished
(system, question_id, metric) rows are skipped and `status: error` rows are retried. One file never mixes
judges. Judge: `EVAL_JUDGE_PROVIDER` / `EVAL_JUDGE_MODEL` (rq2-eval defaults to openai / gpt-4o-mini).
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.rq1.common import OUT_DIR, RAGAS_SCORES_FILE, RECORDS_PATH, REPO_ROOT, SYSTEMS, load_records  # noqa: E402
from scripts.rq2 import judge as J  # noqa: E402
from scripts.rq2 import score as S  # noqa: E402
from scripts.rq2.common import append_jsonl, read_jsonl  # noqa: E402

RAGAS_METRICS = ["context_recall", "context_precision"]


def select_records(records: List[Dict[str, Any]], systems: List[str], limit: Optional[int]) -> List[Dict[str, Any]]:
    """Records of `systems`, restricted to the first `limit` question ids (sorted) if given."""
    qids = sorted({r["question_id"] for r in records})
    keep = set(qids[:limit]) if limit else set(qids)
    return [r for r in records if r["system"] in systems and r["question_id"] in keep]


async def score_ragas(
    records: List[Dict[str, Any]],
    out_path: Path,
    metrics: List[str],
    provider: str,
    model: str,
    concurrency: int = 1,
) -> Dict[str, Any]:
    existing = read_jsonl(out_path)
    judge = J.judge_label(provider, model)
    done = {(r["system"], r["question_id"], r["metric"]) for r in existing if r.get("status") != J.STATUS_ERROR}
    todo = [(rec, m) for rec in records for m in metrics if (rec["system"], rec["question_id"], m) not in done]
    counts: Dict[str, Any] = {"scored": 0, "skipped": len(records) * len(metrics) - len(todo)}
    if not todo:
        return counts
    S.check_single_judge(existing, judge)
    meter = J.JudgeMeter()
    llm = J.build_judge(provider, model, meter)
    metric_objs = {m: S.make_metric(m, llm) for m in metrics}
    semaphore = asyncio.Semaphore(max(1, min(concurrency, 2)))
    breaker = {"consecutive": 0, "stopped": None}

    async def one(rec: Dict[str, Any], metric: str) -> None:
        async with semaphore:
            if breaker["stopped"]:
                return  # not written, so a later run picks it up
            row = await S.score_llm_metric(rec, metric, metric_objs[metric], judge, meter)
            append_jsonl(out_path, row)
            counts["scored"] += 1
            print(f"  {rec['system']} {rec['question_id']} {metric}: {row['status']} {row['value']} "
                  f"(calls={row['judge_calls']})", flush=True)
            if row["status"] == J.STATUS_ERROR:
                breaker["consecutive"] += 1
                if breaker["consecutive"] >= S.CIRCUIT_BREAKER_FAILURES and not breaker["stopped"]:
                    breaker["stopped"] = f"{S.CIRCUIT_BREAKER_FAILURES} consecutive judge failures; last: {row['detail'][:300]}"
                    print(f"STOPPING: {breaker['stopped']}. Progress is saved in {out_path}; rerun to resume.",
                          flush=True)
            elif row["status"] in (J.STATUS_OK, J.STATUS_NA):
                breaker["consecutive"] = 0

    await asyncio.gather(*(one(rec, m) for rec, m in todo))
    if breaker["stopped"]:
        counts["stopped"] = breaker["stopped"]
    return counts


def main() -> None:
    p = argparse.ArgumentParser(description="RQ1 Stage 1b: RAGAS context recall / precision (LLM judge).")
    p.add_argument("--records", type=Path, default=RECORDS_PATH)
    p.add_argument("--out", type=Path, default=OUT_DIR)
    p.add_argument("--scores-file", default=RAGAS_SCORES_FILE)
    p.add_argument("--metrics", default=",".join(RAGAS_METRICS))
    p.add_argument("--systems", default=",".join(SYSTEMS))
    p.add_argument("--limit", type=int, default=None, help="Score only the first N question ids (smoke test).")
    p.add_argument("--concurrency", type=int, default=1, help="Parallel judge calls (1-2).")
    args = p.parse_args()

    from dotenv import load_dotenv

    load_dotenv(REPO_ROOT / ".env", override=False)
    provider = os.getenv("EVAL_JUDGE_PROVIDER", J.DEFAULT_JUDGE_PROVIDER).strip().lower()
    model = os.getenv("EVAL_JUDGE_MODEL", J.DEFAULT_JUDGE_MODEL).strip()
    metrics = [m.strip() for m in args.metrics.split(",") if m.strip()]
    unknown = [m for m in metrics if m not in RAGAS_METRICS]
    if unknown:
        raise SystemExit(f"Unknown metrics {unknown}; known: {RAGAS_METRICS}")
    records = select_records(load_records(args.records), args.systems.split(","), args.limit)
    args.out.mkdir(parents=True, exist_ok=True)
    counts = asyncio.run(score_ragas(records, args.out / args.scores_file, metrics, provider, model, args.concurrency))
    print(f"Done: {counts} (judge {J.judge_label(provider, model)})")
    if counts.get("stopped"):
        sys.exit(2)


if __name__ == "__main__":
    main()
