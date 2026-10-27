"""
RQ2 Stage 1 — run each system once per question and save one JSONL record per (system, question).

Runs in the main `cs614` env and never imports ragas. Resumable: (system, question_id) pairs already in
`records.jsonl` are skipped; failures go to `gen_errors.jsonl` and are retried on the next run.

Usage:
    python scripts/rq2/generate.py --systems system_c_v1,system_c_v2 --run-id smoke --limit 3
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.rq2.adapters import ADAPTER_KEYS, SystemAdapter, get_adapters  # noqa: E402
from scripts.rq2.common import (  # noqa: E402
    GEN_ERRORS_FILE, GOLDEN_PATH, RECORDS_FILE, REPO_ROOT, SCHEMA_VERSION, append_jsonl, done_keys,
    load_golden, now_iso, read_jsonl, run_dir,
)


def git_commit() -> str:
    candidates = [shutil.which("git"), str(Path(sys.executable).parent / "Library" / "cmd" / "git.exe")]
    for exe in candidates:
        if exe and Path(exe).exists():
            try:
                out = subprocess.run([exe, "-C", str(REPO_ROOT), "rev-parse", "--short", "HEAD"],
                                     capture_output=True, text=True, timeout=10)
                if out.returncode == 0:
                    return out.stdout.strip()
            except (OSError, subprocess.SubprocessError):
                continue
    return "unknown"


def build_record(system: str, q: Dict[str, Any], out: Dict[str, Any], run_id: str, commit: str) -> Dict[str, Any]:
    missing = [k for k in ADAPTER_KEYS if k not in out]
    if missing:
        raise ValueError(f"{system} adapter output is missing keys {missing}")
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "system": system,
        "question_id": q["id"],
        "category": q.get("category"),
        "question": q["query"],
        "ground_truth_answer": q.get("ground_truth_answer", ""),
        "ground_truth_numbers": q.get("ground_truth_numbers", []),
        "target_sections": q.get("target_sections", []),
        **{k: out[k] for k in ADAPTER_KEYS},
        "git_commit": commit,
        "timestamp": now_iso(),
    }


def _sanitize_for_adapter(q: Dict[str, Any]) -> Dict[str, Any]:
    """Strip ground-truth fields before passing question to any RAG system adapter."""
    forbidden = {
        "answer", "ground_truth_answer", "ground_truth_numbers",
        "program", "key_points", "gold_evidence", "target_sections", "sources",
    }
    return {k: v for k, v in q.items() if k not in forbidden}


def generate(
    adapters: Dict[str, SystemAdapter],
    questions: List[Dict[str, Any]],
    run_path: Path,
    run_id: str,
    commit: Optional[str] = None,
) -> Dict[str, int]:
    records_path = run_path / RECORDS_FILE
    errors_path = run_path / GEN_ERRORS_FILE
    done = done_keys(read_jsonl(records_path), ("system", "question_id"))
    commit = commit or git_commit()
    counts = {"generated": 0, "skipped": 0, "failed": 0}
    total = len(adapters) * len(questions)
    i = 0
    for system, adapter in adapters.items():
        for q in questions:
            i += 1
            if (system, q["id"]) in done:
                counts["skipped"] += 1
                continue
            try:
                sanitized_q = _sanitize_for_adapter(q)
                record = build_record(system, q, adapter.answer(sanitized_q), run_id, commit)
            except Exception as exc:  # recorded and retried on the next run
                counts["failed"] += 1
                append_jsonl(errors_path, {
                    "system": system, "question_id": q["id"], "category": q.get("category"),
                    "error": f"{type(exc).__name__}: {exc}"[:1000], "timestamp": now_iso(),
                })
                print(f"  [{i}/{total}] {system} {q['id']} FAILED {type(exc).__name__}", flush=True)
                continue
            append_jsonl(records_path, record)
            counts["generated"] += 1
            print(f"  [{i}/{total}] {system} {q['id']} hops={record['hops']} tokens={record['tokens']['total']}",
                  flush=True)
    return counts


def select_questions(questions: List[Dict[str, Any]], ids: Optional[List[str]], limit: Optional[int]):
    if ids:
        wanted = set(ids)
        questions = [q for q in questions if q["id"] in wanted]
    return questions[:limit] if limit else questions


def main() -> None:
    p = argparse.ArgumentParser(description="RQ2 Stage 1: generate answers per system and question.")
    p.add_argument("--systems", default="system_a,system_b,system_c_v1,system_c_v2")
    p.add_argument("--run-id", required=True)
    p.add_argument("--eval-set", default=str(GOLDEN_PATH))
    p.add_argument("--ids", default=None, help="Comma-separated question ids.")
    p.add_argument("--limit", type=int, default=None)
    args = p.parse_args()

    from dotenv import load_dotenv

    load_dotenv(REPO_ROOT / ".env", override=False)
    questions = select_questions(load_golden(Path(args.eval_set)),
                                 args.ids.split(",") if args.ids else None, args.limit)
    adapters = get_adapters([s.strip() for s in args.systems.split(",") if s.strip()])
    run_path = run_dir(args.run_id)
    counts = generate(adapters, questions, run_path, args.run_id)
    print(f"Done: {counts} -> {run_path}")


if __name__ == "__main__":
    main()
