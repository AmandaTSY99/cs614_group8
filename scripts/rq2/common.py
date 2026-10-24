"""
Shared helpers for both RQ2 stages: paths, golden-set loading and append-only JSONL files.

Imported in both conda envs, so it must not import ragas or System C.
"""

import ast
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_PATH = REPO_ROOT / "data" / "golden_eval_set.json"
RUNS_ROOT = REPO_ROOT / "reports" / "rq2"

RECORDS_FILE = "records.jsonl"
GEN_ERRORS_FILE = "gen_errors.jsonl"
SCORES_FILE = "scores.jsonl"

SCHEMA_VERSION = 1
CATEGORIES = ["single_hop_factual", "quantitative_tabular", "cross_section_multihop", "multi_company_comparison"]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_list_field(value: Any) -> List[Any]:
    """Golden-set list fields are sometimes stored as a Python-literal string (`"['$5 million', '20%']"`)."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    text = str(value).strip()
    if not text:
        return []
    try:
        parsed = ast.literal_eval(text)
    except (ValueError, SyntaxError):
        return [text]
    return list(parsed) if isinstance(parsed, (list, tuple)) else [parsed]


def load_golden(path: Path = GOLDEN_PATH) -> List[Dict[str, Any]]:
    questions = json.loads(Path(path).read_text(encoding="utf-8"))
    for q in questions:
        q["ground_truth_numbers"] = parse_list_field(q.get("ground_truth_numbers"))
        q["target_sections"] = parse_list_field(q.get("target_sections"))
    return questions


def run_dir(run_id: str, root: Path = RUNS_ROOT) -> Path:
    path = Path(root) / run_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    """All complete JSON lines; a truncated last line (crash mid-write) is ignored."""
    path = Path(path)
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    """Append one row and flush it to disk immediately, so an interrupted run loses nothing finished."""
    with Path(path).open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def done_keys(rows: Iterable[Dict[str, Any]], fields: Tuple[str, ...]) -> Set[Tuple[Any, ...]]:
    return {tuple(r.get(f) for f in fields) for r in rows}
