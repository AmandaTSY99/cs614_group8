"""Unit tests for System A (Baseline Vanilla RAG) components and evaluation."""
from unittest.mock import MagicMock, patch
import pytest
import pandas as pd
from pathlib import Path

from src.system_a.pipeline import VARIANTS, DEFAULT_VARIANT, TOP_K, generate, answer
from src.system_a.financials import load_financials, financials_block, lookup_financials
from src.system_a.evaluate import (
    load_benchmark,
    gold_pairs,
    evidence_in_hit,
    score_retrieval,
    numeric_correct,
    keypoint_recall,
    score_answer,
    summarize,
)
from src.system_a.retrieval import make_filter


def test_system_a_variants_definition():
    """Verify all 4 core CLI variants are properly declared."""
    assert "rag5" in VARIANTS
    assert "rag3" in VARIANTS
    assert "rag4" in VARIANTS
    assert "rag6" in VARIANTS
    assert DEFAULT_VARIANT == "rag5"
    assert TOP_K == 10
    assert VARIANTS["rag5"]["financials"] is False
    assert VARIANTS["rag6"]["financials"] is True


def test_retrieval_make_filter():
    """Verify Chroma filter construction from ticker/year pairs."""
    assert make_filter([]) is None
    assert make_filter(None) is None
    
    # Single pair
    single = make_filter([("NVDA", 2026)])
    assert single == {"$and": [{"ticker": "NVDA"}, {"fiscal_year": 2026}]}
    
    # Single ticker only
    ticker_only = make_filter([("AAPL", None)])
    assert ticker_only == {"ticker": "AAPL"}
    
    # Multiple pairs
    multi = make_filter([("NVDA", 2026), ("MSFT", 2025)])
    assert "$or" in multi
    assert len(multi["$or"]) == 2


def test_financials_loading_and_lookup():
    """Verify XBRL data lookup from data/financials.csv."""
    df = load_financials()
    assert not df.empty
    assert "ticker" in df.columns
    assert "fiscal_year" in df.columns
    assert "Revenue" in df.columns
    
    block = financials_block("NVDA", 2026)
    assert "[F-NVDA-2026]" in block
    assert "reported financials" in block

    # Multi-pair lookup
    blocks = lookup_financials([("NVDA", 2026), ("MSFT", 2025)])
    assert len(blocks) == 2


@patch("src.system_a.pipeline.chat")
def test_pipeline_generate_and_answer(mock_chat):
    """Verify answer generation and context construction with mock hits."""
    mock_chat.return_value = "NVIDIA's total revenue was $60.9B in FY2024 [1]."
    
    hits = [
        {
            "id": "NVDA_2024:001",
            "score": 0.88,
            "text": "Total revenue for fiscal 2024 was $60,922 million.",
            "meta": {"ticker": "NVDA", "fiscal_year": 2024, "doc_id": "NVDA_2024"}
        }
    ]
    
    # Test generate without financials (rag5)
    out = generate("What was revenue?", hits, variant="rag5", pairs=[("NVDA", 2024)])
    assert out["answer"] == mock_chat.return_value
    assert out["financials"] == []
    assert mock_chat.called

    # Test generate with financials (rag6)
    out_fin = generate("What was revenue?", hits, variant="rag6", pairs=[("NVDA", 2024)])
    assert len(out_fin["financials"]) >= 1
    assert "[F-NVDA-2024]" in out_fin["financials"][0]

    # Test answer() with mock index
    mock_index = MagicMock()
    mock_index.retrieve.return_value = hits
    ans = answer(mock_index, "What was revenue?", variant="rag5", k=5, pairs=[("NVDA", 2024)])
    assert ans["hits"] == hits
    assert ans["answer"] == mock_chat.return_value


def test_evaluation_metrics_and_benchmark():
    """Verify evaluation metric computation against gold evidence and numbers."""
    qa = {
        "id": "test_qa_01",
        "question": "What was NVIDIA revenue in 2024?",
        "answer": "$60,922 million",
        "type": "numeric",
        "gold_evidence": [
            {
                "ticker": "NVDA",
                "year": 2024,
                "doc_id": "NVDA_2024",
                "quote": "total revenue for fiscal 2024 was $60,922 million"
            }
        ]
    }
    
    pairs = gold_pairs(qa)
    assert pairs == [("NVDA", 2024)]
    
    hits = [
        {
            "id": "NVDA_2024:001",
            "score": 0.9,
            "text": "Total revenue for fiscal 2024 was $60,922 million, an increase of 126%.",
            "meta": {"ticker": "NVDA", "fiscal_year": 2024, "doc_id": "NVDA_2024"}
        }
    ]
    
    # Score retrieval
    scores = score_retrieval(qa, hits)
    assert scores["hit"] is True
    assert scores["evidence_recall"] == 1.0
    assert scores["doc_recall"] == 1.0
    assert scores["mrr"] == 1.0

    # Numeric matching
    assert numeric_correct("$60,922 million", "$60.92 billion") is True
    assert numeric_correct("15.2%", "15.2 percent") is True
    assert numeric_correct("100", "200") is False

    # Keypoint recall
    kps = ["Net income increased significantly", "Gross margin reached 72%"]
    pred = "The net income increased significantly due to data center demand and gross margin was 72%."
    assert keypoint_recall(kps, pred) == 1.0

    # Answer scoring helper
    ans_score = score_answer(qa, "Total revenue was $60.92B.")
    assert ans_score["numeric_correct"] is True


def test_load_benchmark_from_data():
    """Verify load_benchmark automatically resolves to data/benchmark_qa_0.jsonl."""
    qas = load_benchmark()
    assert len(qas) > 0
    assert "id" in qas[0]
    assert "gold_evidence" in qas[0]
