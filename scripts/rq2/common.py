"""
Shared helpers for both RQ2 stages: paths, golden-set loading and append-only JSONL files.

Imported in both conda envs, so it must not import ragas or System C.
"""

import ast
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_PATH = REPO_ROOT / "data" / "benchmark_qa_pool_2015.json"
GOLDEN_PATH = BENCHMARK_PATH  # backward-compatibility alias
RUNS_ROOT = REPO_ROOT / "reports" / "rq2"

RECORDS_FILE = "records.jsonl"
GEN_ERRORS_FILE = "gen_errors.jsonl"
SCORES_FILE = "scores.jsonl"

SCHEMA_VERSION = 1
CATEGORIES = ["single_hop_factual", "quantitative_tabular", "cross_section_multihop", "multi_company_comparison"]
_NUM_UNIT_RE = re.compile(
    r"[-+]?\$?\d[\d,]*(?:\.\d+)?(?:\s*(?:percentage points|%|percent|million|billion|thousand|trillion))?",
    re.IGNORECASE,
)


def _derive_category(q: Dict[str, Any]) -> str:
    if q.get("category") in CATEGORIES:
        return str(q["category"])
    recipe = str(q.get("recipe") or "").lower()
    hop = str(q.get("hop") or "").lower()
    # Only questions spanning several companies are multi-company; one company across years is multi-hop.
    if recipe.startswith("cross_company") or recipe == "multi_company" or q.get("scope") == "cross_company":
        return "multi_company_comparison"
    if recipe.startswith("cross_year") or recipe == "table_text" or (hop == "multi" and recipe != "table"):
        return "cross_section_multihop"
    if recipe == "table" or q.get("type") == "numeric":
        return "quantitative_tabular"
    return "single_hop_factual"


def question_dimensions(q: Dict[str, Any]) -> Dict[str, str]:
    """The RQ2 proposal's question attributes, from the benchmark's type / recipe / hop / program / scope."""
    qtype = str(q.get("type") or "").lower()
    recipe = str(q.get("recipe") or "").lower()
    evidence = "table_text" if recipe.endswith("table_text") else "table" if recipe.endswith("table") else "text"
    return {
        "answer_type": {"numeric": "numerical", "qualitative": "narrative"}.get(qtype, qtype or "unknown"),
        "evidence_format": evidence,
        "hop": str(q.get("hop") or "unknown").lower(),
        "task": "calculation" if str(q.get("program") or "").strip() else "lookup",
        "evidence_scope": str(q.get("scope") or "unknown").lower(),
    }


def ragas_reference(q: Dict[str, Any]) -> Dict[str, str]:
    """
    References for RAGAS. A bare computed answer ("-30.36%") cannot be found in any filing, so:
    - `answer`: the gold answer only; a bare negative number also states it as a decrease.
    - `answer_keypoints`: `answer` plus the question's key points.
    - `evidence`: the gold evidence quotes plus the gold answer, for context recall / precision.
    """
    answer = str(q.get("answer") or q.get("ground_truth_answer") or "").strip()
    if re.fullmatch(r"-\$?\d[\d,]*(?:\.\d+)?\s*(?:%|percent|million|billion)?", answer):
        answer = f"{answer} (a decrease of {answer[1:]})"
    key_points = [str(k).strip() for k in (q.get("key_points") or []) if str(k).strip()]
    full_answer = " ".join([answer] + [k if k.endswith(".") else k + "." for k in key_points]).strip()
    quotes = [str(e.get("quote") or "").strip() for e in (q.get("gold_evidence") or []) if e.get("quote")]
    evidence = "\n".join(quotes + ([f"Answer: {answer}"] if answer else [])).strip()
    return {"answer": answer, "answer_keypoints": full_answer, "evidence": evidence or full_answer}


def benchmark_index(path: Path = BENCHMARK_PATH) -> Dict[str, Dict[str, Any]]:
    """Raw benchmark questions by id (gold evidence, key points, attributes), for scoring."""
    path = Path(path)
    if not path.exists():
        return {}
    return {str(q["id"]): q for q in json.loads(path.read_text(encoding="utf-8"))}


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


def load_golden(path: Path = BENCHMARK_PATH) -> List[Dict[str, Any]]:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    records = json.loads(text) if path.suffix == ".json" else [json.loads(l) for l in text.splitlines() if l.strip()]
    questions = []
    for q in records:
        # Normalize benchmark question schema to adapter input conventions
        if "query" not in q and "question" in q:
            q["query"] = q["question"]
        if "ground_truth_answer" not in q and "answer" in q:
            q["ground_truth_answer"] = q["answer"]
        if not q.get("category"):
            q["category"] = _derive_category(q)

        # Build complete ticker and year lists from item + gold_evidence (strictly ticker/year metadata)
        tickers: List[str] = list(q.get("target_tickers") or [])
        if q.get("ticker") and q["ticker"] not in tickers:
            tickers.append(q["ticker"])
        for ct in q.get("comparison_tickers") or []:
            if ct not in tickers:
                tickers.append(ct)
        for ev in q.get("gold_evidence") or []:
            if ev.get("ticker") and ev["ticker"] not in tickers:
                tickers.append(ev["ticker"])
        if tickers:
            q["target_tickers"] = tickers

        years: List[int] = [int(y) for y in (q.get("fiscal_years") or q.get("applicable_years") or []) if y]
        if q.get("year") and int(q["year"]) not in years:
            years.append(int(q["year"]))
        for ev in q.get("gold_evidence") or []:
            if ev.get("year") and int(ev["year"]) not in years:
                years.append(int(ev["year"]))
        if years:
            q["fiscal_years"] = sorted(years)

        ev_pairs = list(dict.fromkeys(
            (ev["ticker"], int(ev["year"]))
            for ev in (q.get("gold_evidence") or [])
            if ev.get("ticker") and ev.get("year")
        ))
        if ev_pairs:
            q["target_pairs"] = ev_pairs
        elif tickers and years:
            q["target_pairs"] = [(t, y) for t in tickers for y in sorted(years)]

        gt_nums = parse_list_field(q.get("ground_truth_numbers"))
        if not gt_nums and q.get("type") in ("numeric", "mixed") and q.get("ground_truth_answer"):
            m = _NUM_UNIT_RE.search(str(q["ground_truth_answer"]))
            if m:
                gt_nums = [m.group(0).strip()]
        q["ground_truth_numbers"] = gt_nums

        t_secs = parse_list_field(q.get("target_sections"))
        if not t_secs and q.get("gold_evidence"):
            for ev in q["gold_evidence"]:
                sec_item = ev.get("item")
                if sec_item:
                    sec_label = f"{ev['ticker']} {sec_item}" if len(tickers) > 1 and ev.get("ticker") else sec_item
                    if sec_label not in t_secs:
                        t_secs.append(sec_label)
        q["target_sections"] = t_secs
        questions.append(q)
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
