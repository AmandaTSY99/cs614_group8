"""
Tests for System C Academic Benchmark Integration and 2015+ Pool.
"""

import json
from pathlib import Path
import pytest

from src.system_c.benchmark_adapter import (
    FEATURED_BENCHMARK_IDS,
    load_benchmark_pool,
    get_benchmark_by_id,
    get_featured_benchmark_questions,
    run_finqa_program,
    benchmark_to_system_c_query,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
POOL_FILE = REPO_ROOT / "data" / "benchmark_qa_pool_2015.json"


def test_pool_file_exists_and_count():
    assert POOL_FILE.exists(), f"Pool file does not exist: {POOL_FILE}"
    data = json.loads(POOL_FILE.read_text(encoding="utf-8"))
    assert len(data) == 97, f"Expected 97 questions in audited 2015+ pool, found {len(data)}"


def test_pool_strict_2015_constraint():
    pool = load_benchmark_pool()
    assert len(pool) == 97

    for item in pool:
        # Check top-level year
        assert item.get("year") is not None, f"Item {item.get('id')} missing top-level year"
        assert int(item["year"]) >= 2015, f"Item {item['id']} year {item['year']} < 2015"

        # Check all gold evidence years
        evidence = item.get("gold_evidence") or []
        assert len(evidence) >= 1, f"Item {item['id']} has no gold evidence"
        for ev in evidence:
            ev_yr = ev.get("year")
            assert ev_yr is not None, f"Item {item['id']} evidence missing year"
            assert int(ev_yr) >= 2015, f"Item {item['id']} evidence year {ev_yr} < 2015"


def test_featured_benchmark_questions():
    featured = get_featured_benchmark_questions()
    assert len(featured) == len(FEATURED_BENCHMARK_IDS)
    featured_ids = [f["id"] for f in featured]
    assert featured_ids == FEATURED_BENCHMARK_IDS


def test_finqa_program_execution():
    # amanda-002: divide(1994, 3452)
    q2 = get_benchmark_by_id("amanda-002")
    assert q2 is not None
    res = run_finqa_program(q2["program"])
    assert res is not None
    assert abs(res - 0.5776) < 0.001

    # Multi-step program: subtract(2.9, 3.9), divide(#0, 3.9)
    q1 = get_benchmark_by_id("amanda-001")
    assert q1 is not None
    res1 = run_finqa_program(q1["program"])
    assert res1 is not None
    assert abs(res1 - (-0.25641)) < 0.001


def test_benchmark_to_system_c_query():
    q2 = get_benchmark_by_id("amanda-002")
    sys_c_payload = benchmark_to_system_c_query(q2)
    assert sys_c_payload["query"] == q2["question"]
    assert sys_c_payload["ground_truth_answer"] == q2["answer"]
    assert sys_c_payload["ticker"] == "META"
    assert sys_c_payload["tickers"] == ["META"]
    assert 2023 in sys_c_payload["fiscal_years"]
