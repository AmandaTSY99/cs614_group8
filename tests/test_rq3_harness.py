"""
Unit tests for the RQ3 Experimental Harness & Evaluation Pipeline.

Ensures:
1. Strict Anti-Leakage input firewall strips all ground-truth answers and evidence.
2. Statistical functions (Clopper-Pearson CI, Holm-Bonferroni correction) are exact.
3. Mock execution of run_rq3_experiment runs end-to-end and outputs valid JSONL records.
4. Evaluation pipeline aggregates mock records into summary metrics JSON/CSV.
"""

import json
from pathlib import Path
import pytest

from scripts.rq3.run_rq3_experiment import (
    sanitize_input_for_system,
    load_benchmark_records,
    run_experiment,
    ALL_SYSTEMS,
    DEFAULT_BENCHMARK_2015,
)
from scripts.rq3.evaluate_rq3 import (
    clopper_pearson_ci,
    holm_bonferroni_correction,
    compute_wilcoxon_tests,
    evaluate_experiment,
)


def test_sanitize_input_firewall():
    """Verify that ground truth answers, programs, quotes, and evidence sections are stripped."""
    dirty_record = {
        "query_id": "test_q1",
        "question": "What was the revenue in 2021?",
        "ticker": "AAPL",
        "year": 2021,
        # Leakage fields that MUST be stripped:
        "answer": "365817",
        "program": "add(300, 65)",
        "key_points": ["revenue grew 33%", "iPhone sales strong"],
        "gold_evidence": [
            {
                "chunk_id": "AAPL_2021_chunk_10",
                "ticker": "AAPL",
                "year": 2021,
                "text": "Total net sales were $365,817 million in 2021.",
                "section": "Item 7. MD&A",
            }
        ],
        "gold_evidence_quotes": ["Total net sales were $365,817 million"],
        "gold_evidence_sections": ["Item 7. MD&A"],
    }

    sanitized = sanitize_input_for_system(dirty_record)

    # Allowed safe fields:
    assert sanitized["query_id"] == "test_q1"
    assert sanitized["question"] == "What was the revenue in 2021?"
    assert sanitized["ticker"] == "AAPL"
    assert sanitized["target_tickers"] == ["AAPL"]
    assert sanitized["target_pairs"] == [("AAPL", 2021)]

    # Strictly disallowed leaked fields:
    assert "answer" not in sanitized
    assert "program" not in sanitized
    assert "key_points" not in sanitized
    assert "gold_evidence_quotes" not in sanitized
    assert "gold_evidence_sections" not in sanitized

    # Allowed stripped evidence metadata (for evaluation retrieval scoring):
    # Only chunk_id, ticker, year - no text or section content
    for ev in sanitized.get("gold_evidence", []):
        assert "text" not in ev
        assert "section" not in ev
        assert "chunk_id" in ev


def test_clopper_pearson_ci():
    """Verify exact binomial Clopper-Pearson CI calculation."""
    # 0 successes out of 10
    low, high = clopper_pearson_ci(0, 10, confidence=0.95)
    assert low == 0.0
    assert 25.0 <= high <= 35.0  # Exact upper bound is ~30.85%

    # 10 successes out of 10
    low, high = clopper_pearson_ci(10, 10, confidence=0.95)
    assert 65.0 <= low <= 75.0  # Exact lower bound is ~69.15%
    assert high == 100.0

    # 5 successes out of 10
    low, high = clopper_pearson_ci(5, 10, confidence=0.95)
    assert 0.0 < low < 50.0
    assert 50.0 < high < 100.0
    assert low < high


def test_holm_bonferroni_correction():
    """Verify Holm-Bonferroni step-down multiplier."""
    raw_p = [0.01, 0.04, 0.03]
    # Sorted: 0.01 (x3), 0.03 (x2), 0.04 (x1)
    # Corrected: 0.03, 0.06, 0.06
    adj = holm_bonferroni_correction(raw_p)
    assert len(adj) == 3
    assert adj[0] == pytest.approx(0.03, abs=1e-3)
    assert adj[2] == pytest.approx(0.06, abs=1e-3)
    assert adj[1] == pytest.approx(0.06, abs=1e-3)


def test_load_benchmark_records():
    """Verify canonical benchmark is loaded and filtered to >= 2015."""
    records = load_benchmark_records(DEFAULT_BENCHMARK_2015, min_year=2015)
    assert len(records) == 40
    for r in records:
        if r.get("year"):
            assert int(r["year"]) >= 2015


def test_rq3_experiment_and_evaluate_end_to_end(tmp_path):
    """Run full mock experiment harness and evaluate statistical metrics."""
    records_file = tmp_path / "mock_records.jsonl"
    errors_file = tmp_path / "mock_errors.jsonl"
    summary_json = tmp_path / "summary.json"
    summary_csv = tmp_path / "summary.csv"
    figures_dir = tmp_path / "figures"

    # 1. Run experiment on 2 queries in mock mode
    run_experiment(
        systems=ALL_SYSTEMS,
        benchmark_path=DEFAULT_BENCHMARK_2015,
        out_records_path=records_file,
        out_errors_path=errors_file,
        limit=2,
        seed=42,
        warmup_count=0,
        mock=True,
    )

    assert records_file.exists()
    lines = records_file.read_text(encoding="utf-8").strip().splitlines()
    # 2 queries * 5 systems = 10 records
    assert len(lines) == 10

    records = [json.loads(line) for line in lines]
    systems_seen = {r["system"] for r in records}
    assert systems_seen == set(ALL_SYSTEMS)

    for r in records:
        assert "query_id" in r
        assert "latency_ms" in r
        assert "token_metrics" in r
        assert "estimated_cost_usd" in r
        assert r["status"] == "ok"
        assert r["tpot_ms_per_token"] >= 0
        assert "stage_timings_ms" in r

    # 2. Run evaluation pipeline on generated mock records
    summary = evaluate_experiment(
        records_path=records_file,
        output_json=summary_json,
        output_csv=summary_csv,
        figures_dir=figures_dir,
        generate_plots=False,  # Skip headless rendering in unit test
    )

    assert summary_json.exists()
    assert summary_csv.exists()
    assert "systems" in summary
    assert "hypotheses_tests" in summary
    assert "routing_cascade_simulation" in summary
    assert len(summary["systems"]) == 5

    for sys_name in ALL_SYSTEMS:
        s_data = summary["systems"][sys_name]
        assert s_data["n_queries"] == 2
        assert "latency" in s_data
        assert "tokens" in s_data
        assert "economics" in s_data
        assert "hop_dynamics" in s_data
        assert "accuracy" in s_data
