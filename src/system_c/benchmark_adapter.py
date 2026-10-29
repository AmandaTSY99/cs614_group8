"""
System C Benchmark Adapter & FinQA Grounding Engine.

Loads, translates, and programmatically evaluates Amanda's academic benchmark QA pool
(benchmark_qa_pool_2015.json) for System C RAG and the Streamlit frontend.
"""

import json
import re
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
DEFAULT_POOL_FILE = DATA_DIR / "benchmark_qa_pool_2015.json"

# ---------------------------------------------------------------------------
# MODULAR FEATURED BENCHMARK PRESETS (SWAP ANY ID HERE DURING TESTING)
# ---------------------------------------------------------------------------
FEATURED_BENCHMARK_IDS: List[str] = [
    "gold-002",  # 1-Hop Table Math: META Restructuring R&D share (57.76%) [legacy: amanda-002]
    "gold-013",  # 2-Hop Cross-Year Table: NVDA FY18 vs FY21 Diluted EPS (+43.15%) [legacy: amanda-032]
    "gold-037",  # Table + Footnotes Mixed: NVDA Tegra Revenue ($975M) & Robotics [legacy: amanda-091]
    "gold-032",  # Table + Footnotes: MSFT FY23 Datacenter/GPU Leases (+16.82%) [legacy: amanda-085]
]

# FinQA mathematical operations DSL
FINQA_OPS: Dict[str, Callable[[float, float], float]] = {
    "add": lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
    "divide": lambda a, b: a / b if b != 0 else float("nan"),
    "exp": lambda a, b: a ** b,
    "greater": lambda a, b: float(a > b),
}
FINQA_OPS.update(
    sub=FINQA_OPS["subtract"],
    mul=FINQA_OPS["multiply"],
    div=FINQA_OPS["divide"],
)

_CACHED_POOL: Optional[List[Dict[str, Any]]] = None


def load_benchmark_pool(path: Path = DEFAULT_POOL_FILE) -> List[Dict[str, Any]]:
    """Load and cache the 2015+ benchmark pool."""
    global _CACHED_POOL
    if _CACHED_POOL is not None:
        return _CACHED_POOL

    if not path.exists():
        # Fallback to loading and filtering benchmark_qa_0.jsonl if pool JSON isn't generated yet
        fallback_jsonl = DATA_DIR / "benchmark_qa_0.jsonl"
        if fallback_jsonl.exists():
            records = [json.loads(line) for line in fallback_jsonl.read_text(encoding="utf-8").splitlines() if line.strip()]
            pool = [
                r for r in records
                if all(
                    int(y) >= 2015
                    for y in ({r.get("year")} | {ev.get("year") for ev in r.get("gold_evidence", []) if ev.get("year")})
                    if y
                )
            ]
            _CACHED_POOL = pool
            return _CACHED_POOL
        return []

    data = json.loads(path.read_text(encoding="utf-8"))
    _CACHED_POOL = data
    return _CACHED_POOL


def get_benchmark_by_id(question_id: str) -> Optional[Dict[str, Any]]:
    """Look up a specific benchmark QA item by its unique ID (e.g. 'gold-002') or legacy ID ('amanda-002')."""
    pool = load_benchmark_pool()
    for item in pool:
        if item.get("id") == question_id or item.get("legacy_id") == question_id:
            return item
    return None


def get_featured_benchmark_questions() -> List[Dict[str, Any]]:
    """Return the curated featured questions for the Streamlit UI."""
    featured = []
    for qid in FEATURED_BENCHMARK_IDS:
        item = get_benchmark_by_id(qid)
        if item:
            featured.append(item)
    return featured


def run_finqa_program(program: str) -> Optional[float]:
    """
    Execute a FinQA-style arithmetic program string safely.
    Example: 'subtract(2.9, 3.9), divide(#0, 3.9)' -> -0.2564
    """
    if not program or not isinstance(program, str):
        return None

    results: List[float] = []
    steps = re.findall(r"(\w+)\(([^()]*)\)", program)
    if not steps:
        return None

    try:
        for op, args in steps:
            op_key = op.strip().lower()
            if op_key not in FINQA_OPS:
                return None

            values: List[float] = []
            for a in (x.strip() for x in args.split(",")):
                if a.startswith("#"):
                    idx = int(a[1:])
                    if idx >= len(results):
                        return None
                    values.append(results[idx])
                else:
                    clean_a = a.replace("const_m", "-").replace("const_", "").replace(",", "")
                    values.append(float(clean_a))

            step_res = FINQA_OPS[op_key](*values)
            results.append(step_res)

        return results[-1] if results else None
    except Exception:
        return None


def benchmark_to_system_c_query(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Translate an Amanda benchmark item into a unified System C query payload.
    Ensures seamless compatibility with System C's multi-hop state graph.
    """
    all_years = item.get("applicable_years") or []
    if not all_years and item.get("year"):
        all_years = [int(item["year"])]

    return {
        "id": item.get("id", "custom-qa"),
        "query": item.get("question", ""),
        "ticker": item.get("ticker", ""),
        "tickers": [item.get("ticker")] if item.get("ticker") else [],
        "fiscal_years": all_years,
        "recipe": item.get("recipe", "custom"),
        "type": item.get("type", "qualitative"),
        "ground_truth_answer": item.get("answer", ""),
        "program": item.get("program", ""),
        "key_points": item.get("key_points", []),
        "gold_evidence": item.get("gold_evidence", []),
        "scope": item.get("scope", "single_doc"),
        "hop": item.get("hop", "multi"),
    }
