"""
Automated Pytest Suite for Canonical Golden Evaluation Benchmark.

Validates schema compliance, hop stratification, company balance, multi-company
comparisons, and ground-truth numerical integrity for CS614 GenAI Evaluation.
"""

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

import pytest

EVAL_FILE = Path(__file__).resolve().parent.parent / "data" / "golden_eval_set.json"
EXPECTED_TICKERS = {"AAPL", "MSFT", "AMZN", "GOOGL", "META", "NVDA", "TSLA", "JPM", "JNJ", "WMT"}
EXPECTED_CATEGORIES = {
    "single_hop_factual",
    "quantitative_tabular",
    "cross_section_multihop",
    "multi_company_comparison",
}
REQUIRED_FIELDS = {
    "id",
    "ticker",
    "fiscal_years",
    "category",
    "min_required_hops",
    "query",
    "target_sections",
    "ground_truth_answer",
    "ground_truth_numbers",
}


@pytest.fixture(scope="module")
def eval_dataset() -> List[Dict[str, Any]]:
    assert EVAL_FILE.exists(), f"Evaluation file not found: {EVAL_FILE}"
    with open(EVAL_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def test_golden_dataset_total_count(eval_dataset: List[Dict[str, Any]]) -> None:
    """Benchmark must contain 60 curated questions (50 single-company + 10 multi-company)."""
    assert len(eval_dataset) == 60, f"Expected 60 questions, found {len(eval_dataset)}"


def test_golden_dataset_schema(eval_dataset: List[Dict[str, Any]]) -> None:
    """Every record must conform to the required JSON schema."""
    for i, item in enumerate(eval_dataset):
        expected_id = f"GOLD-{i+1:02d}"
        assert item["id"] == expected_id, f"Item {i} has unexpected id: {item['id']}"
        assert REQUIRED_FIELDS.issubset(set(item.keys())), f"Item {item['id']} fields missing: {REQUIRED_FIELDS - set(item.keys())}"

        assert item["ticker"] in EXPECTED_TICKERS, f"Invalid ticker: {item['ticker']}"
        assert item["category"] in EXPECTED_CATEGORIES, f"Invalid category: {item['category']}"

        assert isinstance(item["fiscal_years"], list) and len(item["fiscal_years"]) >= 1
        assert all(isinstance(y, int) for y in item["fiscal_years"])

        assert isinstance(item["target_sections"], list) and len(item["target_sections"]) >= 1
        assert all(isinstance(s, str) for s in item["target_sections"])

        assert isinstance(item["query"], str) and len(item["query"].strip()) >= 15
        assert isinstance(item["ground_truth_answer"], str) and len(item["ground_truth_answer"].strip()) >= 20
        assert isinstance(item["ground_truth_numbers"], list)
        assert item["min_required_hops"] in {1, 2, 3}


def test_golden_dataset_tier_stratification(eval_dataset: List[Dict[str, Any]]) -> None:
    """Dataset must be stratified into 15 single-hop, 20 quantitative tabular, 15 cross-section, and 10 multi-company."""
    counts = Counter(d["category"] for d in eval_dataset)
    assert counts["single_hop_factual"] == 15, f"Expected 15 single_hop_factual, got {counts['single_hop_factual']}"
    assert counts["quantitative_tabular"] == 20, f"Expected 20 quantitative_tabular, got {counts['quantitative_tabular']}"
    assert counts["cross_section_multihop"] == 15, f"Expected 15 cross_section_multihop, got {counts['cross_section_multihop']}"
    assert counts["multi_company_comparison"] == 10, f"Expected 10 multi_company_comparison, got {counts['multi_company_comparison']}"


def test_golden_dataset_single_company_balance(eval_dataset: List[Dict[str, Any]]) -> None:
    """The first 50 questions preserve perfect 5-questions-per-company balance."""
    first_50 = eval_dataset[:50]
    counts = Counter(d["ticker"] for d in first_50)
    assert set(counts.keys()) == EXPECTED_TICKERS
    for ticker in EXPECTED_TICKERS:
        assert counts[ticker] == 5, f"Company {ticker} expected 5 questions in first 50, got {counts[ticker]}"


def test_golden_dataset_multi_company_tier(eval_dataset: List[Dict[str, Any]]) -> None:
    """Multi-company questions (GOLD-51 to GOLD-60) must specify multiple target tickers and min_hops >= 2."""
    multi_tier = eval_dataset[50:]
    assert len(multi_tier) == 10
    for item in multi_tier:
        assert item["category"] == "multi_company_comparison"
        assert item["min_required_hops"] in {2, 3}
        target_tickers = item.get("target_tickers", [])
        assert len(target_tickers) >= 2, f"Item {item['id']} must specify at least 2 target tickers"
        assert all(t in EXPECTED_TICKERS for t in target_tickers)


def test_golden_dataset_numerical_grounding(eval_dataset: List[Dict[str, Any]]) -> None:
    """Every ground truth number/key entity must appear in the ground truth answer."""
    for item in eval_dataset:
        for num in item["ground_truth_numbers"]:
            assert num in item["ground_truth_answer"], (
                f"Item {item['id']}: Ground truth token '{num}' missing from answer: {item['ground_truth_answer']}"
            )
