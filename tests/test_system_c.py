"""
Unit & Integration Test Suite for System C (Adaptive Multi-Hop RAG - AMR v1 & Agentic AAMR v2).

Verifies:
1. State initialization & schema contract (`AdaptiveRAGState`).
2. Single-hop early stopping (`current_hop == 1`, `early_stopped == True`).
3. Multi-hop conditioned loop (`Hop 1 -> Critic -> Generator -> Hop 2 -> Synthesizer`).
4. Hard ceiling enforcement (`max_hops == 3` prevents infinite loops when `is_sufficient == False`).
5. System C v2 (`v2_aamr`) autonomous tabular XBRL lookup (`[F-NVDA-2026]` from `data/financials.csv`).
6. Aryan's Citation Mapper & Active Numerical Guardrail (flagging hallucinated numbers vs grounded numbers).
7. Anish's RQ3 Inference Economics telemetry (latency, tokens, USD cost, and Hop Attribution).
"""

import os
import pytest

from src.system_c.graph import run_system_c
from src.system_c.guardrails.verifier import verify_numerical_grounding
from src.system_c.state import create_initial_state


@pytest.fixture(autouse=True)
def force_mock_llm(monkeypatch):
    """Run unit tests deterministically using `LLM_PROVIDER=mock` in <1 second."""
    monkeypatch.setenv("LLM_PROVIDER", "mock")


def test_initial_state_schema():
    state = create_initial_state(
        query="What was NVDA revenue in 2026?",
        max_hops=3,
        mode="v1_amr",
        target_ticker="NVDA",
        fiscal_years=[2026],
    )
    assert state["original_query"] == "What was NVDA revenue in 2026?"
    assert state["target_ticker"] == "NVDA"
    assert state["target_pairs"] == [["NVDA", 2026]]
    assert state["max_hops"] == 3
    assert state["current_hop"] == 0
    assert state["is_sufficient"] is False


def test_single_hop_early_stopping():
    """Simple single-hop query should stop at Hop 1 without invoking Aryan's follow-up generator."""
    res = run_system_c(
        query="What is NVDA primary business in 2026?",
        max_hops=3,
        mode="v1_amr",
        mock_sufficient_at_hop=1,
    )
    assert res["current_hop"] == 1
    assert res["is_sufficient"] is True
    assert len(res["accumulated_evidence"]) >= 1
    rq3 = res["telemetry"]["rq3_summary"]
    assert rq3["hop_count"] == 1
    assert rq3["early_stopped"] is True
    assert rq3["total_tokens"] > 0


def test_multi_hop_conditioned_loop_stops_at_hop_2():
    """Multi-hop query that lacks footnote details in Hop 1 should loop through generator and finish at Hop 2."""
    res = run_system_c(
        query="How did NVDA revenue change in 2026 and what footnote debt covenants applied?",
        max_hops=3,
        mode="v1_amr",
        mock_sufficient_at_hop=2,
    )
    assert res["current_hop"] == 2
    assert res["is_sufficient"] is True
    assert len(res["intermediate_answers"]) == 2
    assert res["intermediate_answers"][0]["is_sufficient"] is False
    assert res["intermediate_answers"][1]["is_sufficient"] is True
    # Verify both Hop 1 and Hop 2 retrieved chunks (RQ1 Hop Attribution)
    rq3 = res["telemetry"]["rq3_summary"]
    assert 1 in rq3["hop_attribution_chunk_ids"]
    assert 2 in rq3["hop_attribution_chunk_ids"]
    assert len(res["citations"]) >= 1


def test_hard_ceiling_at_max_hops_3():
    """When Critic remains unsatisfied, the graph MUST hard-stop at `max_hops=3` and still synthesize."""
    res = run_system_c(
        query="Compare NVDA 2024 and 2026 foreign exchange impact and footnote table breakdowns",
        max_hops=3,
        mode="v1_amr",
        mock_sufficient_at_hop=99,  # Never sufficient
    )
    assert res["current_hop"] == 3
    assert res["is_sufficient"] is False
    assert res["final_answer"] is not None
    assert len(res["intermediate_answers"]) == 3
    rq3 = res["telemetry"]["rq3_summary"]
    assert rq3["hop_count"] == 3
    assert rq3["early_stopped"] is False


def test_v2_aamr_tabular_tool_integration():
    """In `v2_aamr` mode, quantitative queries invoke `tabular_tool_node` to fetch `[F-NVDA-2026]` from `financials.csv`."""
    res = run_system_c(
        query="What was NVDA revenue and operating margin in 2026 and how did risk factors impact it?",
        max_hops=3,
        mode="v2_aamr",
        mock_sufficient_at_hop=2,
    )
    assert res["needs_tabular_tool"] is True
    assert len(res["tabular_evidence"]) >= 1
    assert any(c["chunk_id"].startswith("F-NVDA") for c in res["accumulated_evidence"])
    assert "[F-NVDA-2026]" in (res["final_answer"] or "")


def test_guardrail_numerical_grounding_verifier():
    """Verify Aryan's numerical guardrail accurately distinguishes grounded vs hallucinated numbers."""
    evidence = [
        {
            "chunk_id": "NVDA_FY2026:10",
            "content": "In FY2026, Data Center revenue rose 142% to $115,185 million while gross margin was 75.0%.",
        }
    ]
    grounded_ans = "Data Center revenue increased by 142% to $115,185 million with a 75.0% gross margin [NVDA_FY2026:10]."
    rep_ok = verify_numerical_grounding(grounded_ans, evidence)
    assert rep_ok["numerical_grounding_error_rate"] == 0.0
    assert rep_ok["faithfulness_score"] == 1.0
    assert rep_ok["ungrounded_numbers"] == []

    hallucinated_ans = "Data Center revenue increased by 142% to $999,999 million with a 88.5% gross margin [NVDA_FY2026:10]."
    rep_bad = verify_numerical_grounding(hallucinated_ans, evidence)
    assert "999,999" in rep_bad["ungrounded_numbers"]
    assert "88.5%" in rep_bad["ungrounded_numbers"]
    assert rep_bad["numerical_grounding_error_rate"] > 0.5


def test_rq3_ablation_force_max_hops():
    """Verify that force_max_hops=True prevents early-stopping and executes all 3 hops for RQ3 ablation."""
    res = run_system_c(
        query="What was NVDA period end date?",
        max_hops=3,
        mode="v1_amr",
        force_max_hops=True,
    )
    assert res["current_hop"] == 3
    assert res["telemetry"]["rq3_summary"]["early_stopped"] is False


def test_clean_and_parse_json_robustness():
    """Verify clean_and_parse_json handles markdown fences, commentary, and trailing commas."""
    from src.system_c.llm import clean_and_parse_json

    raw_with_trailing_comma = """
    Here is the requested output:
    ```json
    {
        "is_sufficient": true,
        "missing_premises": [],
        "critic_reasoning": "Context contains all required facts.",
    }
    ```
    """
    parsed = clean_and_parse_json(raw_with_trailing_comma)
    assert parsed.get("is_sufficient") is True
    assert parsed.get("missing_premises") == []

    malformed = "Not a json response at all"
    assert clean_and_parse_json(malformed) == {}


def test_multi_company_query_decomposition():
    """Verify decomposer extracts multiple tickers and formats multi-company target pairs."""
    from src.system_c.nodes.decomposer import decomposer_node
    from src.system_c.state import create_initial_state

    state = create_initial_state(
        query="Compare Apple and Microsoft total revenue in 2024 and 2025",
        max_hops=2,
    )
    out = decomposer_node(state)
    assert "AAPL" in out["target_tickers"]
    assert "MSFT" in out["target_tickers"]
    assert 2024 in out["fiscal_years"]
    assert 2025 in out["fiscal_years"]
    assert len(out["target_pairs"]) >= 4
