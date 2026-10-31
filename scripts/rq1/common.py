"""
Shared RQ1 helpers: paths, benchmark / records loading and the question-type facets used to slice results.

Pure standard library, so it imports in both the runner image and the RAGAS (`rq2-eval`) image.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_PATH = REPO_ROOT / "data" / "benchmark_qa_pool_2015.json"
RECORDS_PATH = REPO_ROOT / "reports" / "rq3" / "records.jsonl"  # the shared 97 x 4 run
OUT_DIR = REPO_ROOT / "reports" / "rq1"

QUESTION_SCORES_FILE = "question_scores.csv"
EVIDENCE_SCORES_FILE = "evidence_scores.csv"
RAGAS_SCORES_FILE = "ragas_scores.jsonl"
AGGREGATE_FILE = "aggregate.csv"
REPORT_FILE = "report.md"

SYSTEMS = ["system_a", "system_b", "system_c_v1", "system_c_v3"]
K_VALUES = (5, 10)

# Facets that describe *where the gold evidence lives*; each question falls in exactly one group per facet.
FACETS = {
    "recipe": ["text", "table", "table_text", "cross_year_text", "cross_year_table",
               "cross_company_text", "cross_company_table"],
    "modality": ["text", "table", "table+text"],
    "scope": ["single_doc", "cross_year", "cross_company"],
    "evidence_count": ["1", "2", "3+"],
    "section_spread": ["1 item", "2+ items"],
}

ITEM_RE = re.compile(r"\bItem\s*(\d+[A-Z]?)\b", re.IGNORECASE)


def gold_item(evidence: Dict[str, Any]) -> str:
    """Top-level 10-K item of one gold evidence entry: "ITEM 8.FINANCIAL STATEMENTS" -> "Item 8"."""
    m = ITEM_RE.search(str(evidence.get("item") or ""))
    if not m:
        raise ValueError(f"Gold evidence has no recognisable 10-K item: {evidence.get('item')!r}")
    return f"Item {m.group(1).upper()}"


def question_facets(q: Dict[str, Any]) -> Dict[str, str]:
    """Group of `q` in every facet of FACETS."""
    evidence = q.get("gold_evidence") or []
    if not evidence:
        raise ValueError(f"{q['id']} has no gold_evidence; RQ1 cannot score it")
    kinds = {ev["kind"] for ev in evidence}
    n_items = len({gold_item(ev) for ev in evidence})
    n_ev = len(evidence)
    return {
        "recipe": q["recipe"],
        "modality": "table+text" if kinds == {"table", "text"} else kinds.pop(),
        "scope": q["scope"],
        "evidence_count": str(n_ev) if n_ev < 3 else "3+",
        "section_spread": "1 item" if n_items == 1 else "2+ items",
    }


def load_benchmark(path: Path = BENCHMARK_PATH) -> Dict[str, Dict[str, Any]]:
    return {q["id"]: q for q in json.loads(Path(path).read_text(encoding="utf-8"))}


def load_records(path: Path = RECORDS_PATH) -> List[Dict[str, Any]]:
    """
    Generated records, one per (system, question). Fails loudly on a record without retrieved contexts or
    a duplicated (system, question_id), instead of scoring around it.
    """
    records = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    seen: set = set()
    for r in records:
        key: Tuple[str, str] = (r.get("system"), r.get("question_id") or r.get("query_id"))
        if not r.get("retrieved_contexts"):
            raise ValueError(
                f"Record for system='{key[0]}', question_id='{key[1]}' is missing 'retrieved_contexts'. "
                "Refusing to fall back to generated answer text for retrieval evaluation."
            )
        if key in seen:
            raise ValueError(f"Duplicate record for system='{key[0]}', question_id='{key[1]}'")
        seen.add(key)
    return records
