"""
Unit & Integration Test Suite for System C (Adaptive Multi-Hop RAG - AMR v1 & Agentic AAMR v2).

Verifies:
1. State initialization & schema contract (`AdaptiveRAGState`).
2. Single-hop early stopping (`current_hop == 1`, `early_stopped == True`).
3. Multi-hop conditioned loop (`Hop 1 -> Critic -> Generator -> Hop 2 -> Synthesizer`).
4. Hard ceiling enforcement (`max_hops == 3` prevents infinite loops when `is_sufficient == False`).
5. System C v2 (`v2_aamr`) autonomous tabular XBRL lookup (`[F-NVDA-2026]` from `data/financials.csv`).
6. Citation Mapper & Active Numerical Guardrail (flagging hallucinated numbers vs grounded numbers).
7. RQ3 Inference Economics telemetry (latency, tokens, USD cost, and Hop Attribution).
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
    """Simple single-hop query should stop at Hop 1 without invoking follow-up generator."""
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
    """Verify numerical guardrail accurately distinguishes grounded vs hallucinated numbers."""
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


def test_critic_sufficiency_score_threshold():
    """Verify quantitative sufficiency scoring with early-stopping threshold (0.85)."""
    from src.system_c.nodes.critic import critic_node

    # Case A: Sufficiency score 0.90 >= 0.85 threshold -> Early stopping triggers at Hop 1
    state_high = create_initial_state(
        query="What was NVDA revenue in 2026?",
        max_hops=3,
        mode="v1_amr",
        target_ticker="NVDA",
        fiscal_years=[2026],
        sufficiency_threshold=0.85,
    )
    state_high["current_hop"] = 1
    state_high["telemetry"]["mock_sufficiency_score"] = 0.90
    out_high = critic_node(state_high)
    assert out_high["is_sufficient"] is True
    assert out_high["sufficiency_score"] == 0.90
    assert out_high["missing_premises"] == []
    assert out_high["missing_entities"] == []
    assert out_high["missing_years"] == []
    assert out_high["telemetry"]["early_stopped"] is True

    # Case B: Sufficiency score 0.60 < 0.85 threshold -> Loop continues
    state_low = create_initial_state(
        query="What was NVDA revenue in 2026 and what are the detailed footnote contingencies?",
        max_hops=3,
        mode="v1_amr",
        target_ticker="NVDA",
        fiscal_years=[2026],
        sufficiency_threshold=0.85,
    )
    state_low["current_hop"] = 1
    state_low["telemetry"]["mock_sufficiency_score"] = 0.60
    out_low = critic_node(state_low)
    assert out_low["is_sufficient"] is False
    assert out_low["sufficiency_score"] == 0.60
    assert len(out_low["missing_premises"]) > 0


def test_critic_explicit_entity_and_year_gap_detection(monkeypatch):
    """Verify Critic detects specific missing entity line items and missing fiscal years."""
    import json
    from src.system_c.nodes.critic import critic_node
    from src.system_c.nodes.generator import generator_node

    state = create_initial_state(
        query="Compare NVDA R&D spending in 2022 vs 2026 and footnote capitalization policies",
        max_hops=3,
        target_ticker="NVDA",
        fiscal_years=[2022, 2026],
    )
    state["current_hop"] = 1

    # Simulate LLM returning explicit missing entities & years
    def mock_critic_call_llm(*args, **kwargs):
        content = json.dumps({
            "sufficiency_score": 0.45,
            "is_sufficient": False,
            "missing_entities": ["2022 R&D spending", "capitalization accounting footnote"],
            "missing_years": [2022],
            "missing_premises": ["Disclosures and line items for 2022 R&D spending"],
            "critic_reasoning": "Retrieved 2026 data, but completely missing 2022 comparative baseline."
        })
        return content, state["telemetry"]

    monkeypatch.setattr("src.system_c.nodes.critic.call_llm", mock_critic_call_llm)
    out = critic_node(state)

    assert out["is_sufficient"] is False
    assert out["sufficiency_score"] == 0.45
    assert "2022 R&D spending" in out["missing_entities"]
    assert 2022 in out["missing_years"]
    assert len(out["missing_premises"]) >= 1

    # Verify generator receives the missing entity premise
    state.update(out)
    gen_out = generator_node(state)
    assert "2022 R&D spending" in gen_out["current_sub_query"] or "NVDA" in gen_out["current_sub_query"]


def test_critic_redundant_search_prevention_on_chunk_saturation():
    """Verify Critic halts early when subsequent hop returns duplicate/saturated chunks."""
    from src.system_c.nodes.critic import critic_node

    state = create_initial_state(
        query="What were the foreign exchange risks in 2026?",
        max_hops=3,
        mode="v1_amr",
        target_ticker="NVDA",
        fiscal_years=[2026],
    )
    # Hop 1 retrieved chunk 10
    chunk1 = {
        "chunk_id": "NVDA_FY2026:10",
        "content": "Foreign currency rate fluctuations did not have a material impact.",
        "metadata": {"section": "Item 7A", "ticker": "NVDA", "fiscal_year": 2026},
        "relevance_score": 0.9,
        "hop_retrieved": 1,
    }
    # Hop 2 retrieved the exact same chunk 10 (no new data)
    chunk2 = {
        "chunk_id": "NVDA_FY2026:10",
        "content": "Foreign currency rate fluctuations did not have a material impact.",
        "metadata": {"section": "Item 7A", "ticker": "NVDA", "fiscal_year": 2026},
        "relevance_score": 0.9,
        "hop_retrieved": 2,
    }
    state["accumulated_evidence"] = [chunk1, chunk2]
    state["current_hop"] = 2
    state["telemetry"]["mock_sufficiency_score"] = 0.50  # Even if LLM thought 0.50

    out = critic_node(state)
    assert out["redundant_search_prevented"] is True
    assert out["is_sufficient"] is True
    assert out["sufficiency_score"] >= 0.85
    assert "Redundant loop prevented" in out["critic_reasoning"]


def test_critic_redundant_search_prevention_on_tabular_coverage():
    """Verify Critic recognizes complete factual coverage when tabular tool supplies exact numbers."""
    from src.system_c.nodes.critic import critic_node

    state = create_initial_state(
        query="What was NVDA revenue and operating income in 2026?",
        max_hops=3,
        mode="v2_aamr",
        target_ticker="NVDA",
        fiscal_years=[2026],
    )
    state["needs_tabular_tool"] = True
    state["tabular_evidence"] = [
        "[F-NVDA-2026] (NVDA FY2026 reported financials)\nfiscal_year,Revenue,OperatingIncome\n2026,130497000000,80854000000"
    ]
    state["current_hop"] = 1

    out = critic_node(state)
    assert out["is_sufficient"] is True
    assert out["sufficiency_score"] >= 0.85
    assert "Tabular XBRL" in out["critic_reasoning"] or "Complete" in out["critic_reasoning"]


def test_critic_multi_company_completeness_guard():
    """Verify Critic rejects early stopping at Hop 1 if comparative query is missing one or more target tickers."""
    from src.system_c.nodes.critic import critic_node

    state = create_initial_state(
        query="Compare cloud revenue across Microsoft, Amazon, and Alphabet in 2024",
        max_hops=3,
        mode="v1_amr",
    )
    state["target_tickers"] = ["MSFT", "AMZN", "GOOGL"]
    state["current_hop"] = 1
    # Only GOOGL was retrieved in Hop 1
    state["accumulated_evidence"] = [
        {
            "chunk_id": "GOOGL_FY2024:5",
            "content": "Google Cloud revenue was $43,229 million with operating income of $6,112 million.",
            "metadata": {"section": "Item 7", "ticker": "GOOGL", "fiscal_year": 2024},
            "relevance_score": 0.95,
            "hop_retrieved": 1,
        }
    ]
    # Even if LLM attempted to claim sufficiency
    state["telemetry"]["mock_sufficiency_score"] = 0.95

    out = critic_node(state)
    # Must NOT stop early because MSFT and AMZN are missing
    assert out["is_sufficient"] is False
    assert out["sufficiency_score"] <= 0.65
    assert any("MSFT" in p for p in out["missing_premises"])
    assert any("AMZN" in p for p in out["missing_premises"])


def test_supabase_precomputed_chunks_retrieval():
    """Verify retriever fetches pre-computed structure chunks directly from Supabase Cloud `sec_chunks`."""
    from src.system_c.nodes.retriever import _fetch_chunks_from_supabase, _get_cached_chunks

    # Test direct Supabase cloud query
    chunks = _fetch_chunks_from_supabase(["NVDA"], [2026])
    assert len(chunks) > 0
    sample = chunks[0]
    assert "NVDA_FY2026" in sample["id"]
    assert "text" in sample
    assert sample["meta"]["ticker"] == "NVDA"
    assert sample["meta"]["fiscal_year"] == 2026

    # Test cached multi-hop retriever resolution
    cached = _get_cached_chunks(tickers=["NVDA"], fiscal_years=[2026])
    assert len(cached) == len(chunks)


def test_decomposer_autonomous_tool_routing_and_multi_ticker():
    """Verify decomposer splits multi-ticker comparisons into atomic sub-queries and routes tools."""
    from src.system_c.nodes.decomposer import decomposer_node

    state = create_initial_state(
        query="Compare Apple and NVIDIA gross margin and AI supply chain risks in 2024",
        max_hops=2,
    )
    out = decomposer_node(state)

    # Multi-ticker extraction
    assert "AAPL" in out["target_tickers"]
    assert "NVDA" in out["target_tickers"]
    assert 2024 in out["fiscal_years"]
    assert out["needs_tabular_tool"] is True

    # Granular sub_query_plans
    plans = out["sub_query_plans"]
    assert len(plans) >= 2

    # Check that tool routing assigned tabular_tool to financial metrics and retriever to risks
    tabular_plans = [p for p in plans if p["target_tool"] == "tabular_tool"]
    retriever_plans = [p for p in plans if p["target_tool"] == "retriever"]

    assert len(tabular_plans) >= 1
    assert len(retriever_plans) >= 1
    assert any(p["ticker"] == "AAPL" for p in plans)
    assert any(p["ticker"] == "NVDA" for p in plans)


def test_financial_scale_normalizer_unit_matching():
    """Verify Scale Normalizer matches financial figures across scale units ($M vs $B)."""
    from src.system_c.guardrails.scale_normalizer import (
        fuzzy_financial_match,
        parse_financial_value,
    )
    from src.system_c.guardrails.verifier import verify_numerical_grounding

    # Test parse_financial_value
    assert parse_financial_value("$115.18 billion") == 115180000000.0
    assert parse_financial_value("115.2B") == 115200000000.0
    assert parse_financial_value("$115,185 million") == 115185000000.0
    assert parse_financial_value("75.0%") == 75.0

    # Test fuzzy_financial_match with contextual table header
    table_context = """
    CONSOLIDATED STATEMENTS OF INCOME
    (In millions, except per share data)
    Revenue: $115,185
    Gross margin: 75.0%
    """
    assert fuzzy_financial_match("115.18 billion", table_context) is True
    assert fuzzy_financial_match("115.2B", table_context) is True
    assert fuzzy_financial_match("75.0%", table_context) is True
    assert fuzzy_financial_match("999.9 billion", table_context) is False

    # Test integration with verifier
    evidence = [{"chunk_id": "NVDA:1", "content": table_context}]
    answer_with_scaled_units = "NVIDIA generated 115.18 billion in revenue with a 75.0% gross margin [NVDA:1]."
    report = verify_numerical_grounding(answer_with_scaled_units, evidence)
    assert report["numerical_grounding_error_rate"] == 0.0
    assert report["ungrounded_numbers"] == []


def test_arithmetic_derivation_margin_and_growth_grounding():
    """Verify that calculated margins, YoY growth, and spreads are recognized as grounded derivations (AUD-01)."""
    from src.system_c.guardrails.scale_normalizer import verify_arithmetic_derivation

    # Evidence contains raw figures: Revenue = 130,497 and Operating Income = 80,854
    # (Operating margin = 80,854 / 130,497 = 61.96% -> 62.0%)
    raw_evidence = """
    NVIDIA CORP (in millions)
    FY2025 Revenue: 60,922
    FY2025 Operating Income: 32,972
    FY2026 Revenue: 130,497
    FY2026 Operating Income: 80,854
    """

    # 1. Operating margin derivations (62.0% for FY26, 54.1% for FY25)
    assert verify_arithmetic_derivation("62.0%", raw_evidence) is True
    assert verify_arithmetic_derivation("61.96%", raw_evidence) is True
    assert verify_arithmetic_derivation("54.1%", raw_evidence) is True

    # 2. Percentage point spread (|61.96% - 54.12%| = 7.84% -> 7.8% or 7.9%)
    assert verify_arithmetic_derivation("7.8%", raw_evidence) is True

    # 3. Random ungrounded percentage or number MUST be rejected
    assert verify_arithmetic_derivation("43.7%", raw_evidence) is False
    assert verify_arithmetic_derivation("999999", raw_evidence) is False

    # 4. End-to-end integration with verify_numerical_grounding
    evidence = [{"chunk_id": "NVDA_FY2026_2026-01-25:1", "content": raw_evidence}]
    answer = "NVIDIA achieved an operating margin of 62.0% in FY2026, up from 54.1% in FY2025 [NVDA FY2026, Item 8, NVDA_FY2026_2026-01-25:1]."
    report = verify_numerical_grounding(answer, evidence)
    assert report["numerical_grounding_error_rate"] == 0.0
    assert "62.0%" in report["verified_numbers"]
    assert "54.1%" in report["verified_numbers"]
    assert report["ungrounded_numbers"] == []


def test_active_self_healing_repair_loop(monkeypatch):
    """Verify that when an ungrounded number is flagged, the graph triggers repair_node and re-audits."""
    from src.system_c.graph import build_system_c_graph
    from src.system_c.state import create_initial_state

    # Construct initial state where synthesizer will return an ungrounded number on pass 1
    state = create_initial_state(
        query="What was NVDA revenue in 2026?",
        max_hops=1,
        mode="v1_amr",
        target_ticker="NVDA",
        fiscal_years=[2026],
        max_repairs=1,
    )

    # Let synthesizer introduce a hallucinated number "$999,999"
    def mock_hallucinating_synthesizer(st):
        return {
            "draft_answer": "NVDA reported revenue of $999,999 million in FY2026 [NVDA_FY2026_2026-01-25:217].",
            "final_answer": "NVDA reported revenue of $999,999 million in FY2026 [NVDA_FY2026_2026-01-25:217].",
            "citations": [],
            "telemetry": st.get("telemetry", {}),
        }

    monkeypatch.setattr("src.system_c.graph.synthesizer_node", mock_hallucinating_synthesizer)

    app = build_system_c_graph()
    final_state = app.invoke(state)

    # Verify self-healing executed
    assert final_state["repair_count"] == 1
    assert len(final_state["repair_history"]) == 1
    assert "999,999" in final_state["repair_history"][0]["flagged_numbers"]
    # In mock mode, repair_node excises the ungrounded number
    assert "[figure not disclosed in filing]" in final_state["final_answer"]
    assert final_state["guardrail_passed"] is True


def test_repair_loop_bounded_at_max_repairs():
    """Verify repair loop hard-halts at max_repairs without infinite loop even if hallucination persists."""
    from src.system_c.graph import route_after_guardrail
    from src.system_c.state import create_initial_state

    state = create_initial_state(
        query="What was NVDA revenue in 2026?",
        max_repairs=1,
    )
    state["guardrail_passed"] = False
    state["repair_count"] = 0

    # First pass: should route to repair
    assert route_after_guardrail(state) == "repair"

    # Second pass (repair_count >= max_repairs): should route to __end__
    state["repair_count"] = 1
    assert route_after_guardrail(state) == "__end__"


def test_fastapi_gateway_endpoints():
    """Verify FastAPI enterprise endpoints (health check, query execution, Supabase financials)."""
    from starlette.testclient import TestClient
    from src.system_c.api import app

    client = TestClient(app)

    # 1. Health check
    res_health = client.get("/")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "online"

    # 2. Query execution
    res_query = client.post(
        "/api/v1/query",
        json={"query": "What is NVDA business model in 2026?", "max_hops": 1, "mode": "v1_amr"},
    )
    assert res_query.status_code == 200
    data = res_query.json()
    assert "NVDA" in data["final_answer"]
    assert data["guardrail_passed"] is True
    assert "telemetry" in data


def test_v3_aamr_sg_schema_aware_decomposer():
    """Verify System C v3 (AAMR-SG) Query Decomposer distinguishes headline metrics from footnotes."""
    from src.system_c.nodes.decomposer import decomposer_node, is_xbrl_headline_target

    # 1. Headline macro metric -> needs_tabular_tool = True
    state_macro = create_initial_state(
        query="By how many million dollars did Tesla's total assets increase from fiscal year 2021 to fiscal year 2025?",
        mode="v3_aamr_sg",
    )
    out_macro = decomposer_node(state_macro)
    assert out_macro["needs_tabular_tool"] is True
    assert out_macro["target_metric_type"] == "xbrl_headline"

    # 2. Footnote / Gross margin -> needs_tabular_tool = False
    state_margin = create_initial_state(
        query="By how many percentage points did NVIDIA's gross margin increase from fiscal year 2016 to fiscal year 2022?",
        mode="v3_aamr_sg",
    )
    out_margin = decomposer_node(state_margin)
    assert out_margin["needs_tabular_tool"] is False
    assert out_margin["target_metric_type"] == "footnote_disclosure"
    assert all(p["target_tool"] == "retriever" for p in out_margin["sub_query_plans"])

    # 3. Footnote / Segment revenue -> needs_tabular_tool = False
    state_segment = create_initial_state(
        query="What was the absolute increase in NVIDIA's Tegra Processor revenue, in millions of dollars, from fiscal year 2016 to fiscal year 2018?",
        mode="v3_aamr_sg",
    )
    out_segment = decomposer_node(state_segment)
    assert out_segment["needs_tabular_tool"] is False
    assert out_segment["target_metric_type"] == "footnote_disclosure"

    # 4. Footnote / Debt maturity schedule -> needs_tabular_tool = False
    state_debt = create_initial_state(
        query="What is the percentage of Amazon.com's total future principal payments due after 2021 relative to the total future principal payments due in 2017?",
        mode="v3_aamr_sg",
    )
    out_debt = decomposer_node(state_debt)
    assert out_debt["needs_tabular_tool"] is False


def test_v3_aamr_sg_critic_allows_continuation_for_footnotes():
    """Verify Critic in mode='v3_aamr_sg' does NOT force premature Hop 1 stopping when tabular schema lacks metric."""
    from src.system_c.nodes.critic import critic_node

    state = create_initial_state(
        query="By how many percentage points did NVIDIA's gross margin increase from fiscal year 2016 to fiscal year 2022?",
        max_hops=3,
        mode="v3_aamr_sg",
        target_ticker="NVDA",
        fiscal_years=[2016, 2022],
    )
    state["needs_tabular_tool"] = True  # Even if tabular tool was invoked
    state["tabular_evidence"] = [
        "[F-NVDA-2016] (NVDA reported financials)\nRevenue: 5010000000\nNetIncome: 614000000",
        "[F-NVDA-2022] (NVDA reported financials)\nRevenue: 26914000000\nNetIncome: 9752000000",
    ]
    state["current_hop"] = 1
    # Mock LLM indicates partial sufficiency for footnote inquiry
    state["telemetry"]["mock_sufficiency_score"] = 0.50

    out = critic_node(state)
    # Critic must NOT force early stopping at Hop 1!
    assert out["is_sufficient"] is False
    assert out["sufficiency_score"] <= 0.65


def test_system_c_v3_adapter_registration():
    """Verify System C v3 adapter registers under standardized name and schema contracts."""
    from scripts.rq2.adapters import get_adapters, ADAPTER_KEYS

    adapters = get_adapters(["system_c_v3"])
    adapter = adapters["system_c_v3"]
    assert adapter.name == "system_c_v3"
    assert adapter.mode == "v3_aamr_sg"


def test_v3_aamr_sg_query_text_year_priority():
    """Verify that mode='v3_aamr_sg' prioritizes and unions question years into fiscal_years, while v1 preserves state."""
    from src.system_c.nodes.decomposer import decomposer_node

    query = "By how many millions of dollars was Alphabet Inc.'s net gain on equity securities in fiscal year 2024 lower than in fiscal year 2018?"

    # In v3_aamr_sg, 2018 parsed from question must be unioned into fiscal_years
    state_v3 = create_initial_state(
        query=query,
        mode="v3_aamr_sg",
        target_ticker="GOOGL",
        fiscal_years=[2020, 2024],
    )
    out_v3 = decomposer_node(state_v3)
    assert 2018 in out_v3["fiscal_years"]
    assert 2024 in out_v3["fiscal_years"]

    # In v1_amr, pre-existing state fiscal_years is retained untouched
    state_v1 = create_initial_state(
        query=query,
        mode="v1_amr",
        target_ticker="GOOGL",
        fiscal_years=[2020, 2024],
    )
    out_v1 = decomposer_node(state_v1)
    assert out_v1["fiscal_years"] == [2020, 2024]
    assert 2018 not in out_v1["fiscal_years"]


def test_v3_aamr_sg_dynamic_year_expansion_in_follow_up_hops():
    """Verify that mode='v3_aamr_sg' dynamically expands fiscal_years on follow-up hops when Critic flags missing_years."""
    from src.system_c.nodes.generator import generator_node
    from src.system_c.nodes.retriever import retriever_node

    # 1. Test generator_node dynamic year expansion in v3
    state_v3 = create_initial_state(
        query="Alphabet net gain on equity securities",
        mode="v3_aamr_sg",
        target_ticker="GOOGL",
        fiscal_years=[2020, 2024],
    )
    state_v3["current_hop"] = 1
    state_v3["missing_years"] = [2018]
    state_v3["missing_premises"] = ["FY2018 equity securities gain"]

    gen_out_v3 = generator_node(state_v3)
    assert "fiscal_years" in gen_out_v3
    assert 2018 in gen_out_v3["fiscal_years"]
    assert 2024 in gen_out_v3["fiscal_years"]

    # 2. Test retriever_node dynamic year expansion in v3
    calls = []
    def mock_retriever(query, ticker=None, fiscal_years=None, top_k=6, hop=1, tickers=None):
        calls.append({"query": query, "years": fiscal_years, "hop": hop})
        return []

    ret_out_v3 = retriever_node(state_v3, custom_retriever_fn=mock_retriever)
    assert "fiscal_years" in ret_out_v3
    assert 2018 in ret_out_v3["fiscal_years"]
    assert calls[0]["years"] == [2018, 2020, 2024]

    # 3. Test v1_amr leaves fiscal_years untouched
    state_v1 = create_initial_state(
        query="Alphabet net gain on equity securities",
        mode="v1_amr",
        target_ticker="GOOGL",
        fiscal_years=[2020, 2024],
    )
    state_v1["current_hop"] = 1
    state_v1["missing_years"] = [2018]
    gen_out_v1 = generator_node(state_v1)
    assert "fiscal_years" not in gen_out_v1

    calls_v1 = []
    def mock_retriever_v1(query, ticker=None, fiscal_years=None, top_k=6, hop=1, tickers=None):
        calls_v1.append({"query": query, "years": fiscal_years, "hop": hop})
        return []

    ret_out_v1 = retriever_node(state_v1, custom_retriever_fn=mock_retriever_v1)
    assert "fiscal_years" not in ret_out_v1
    assert calls_v1[0]["years"] == [2020, 2024]


def test_v3_aamr_sg_adjacent_table_chunk_stitching():
    """Verify that mode='v3_aamr_sg' stitches adjacent chunk_id + 1 when a forward table lead-in is detected."""
    from src.system_c.nodes.retriever import retriever_node

    lead_in_text = (
        "Item 8 > PART II\n"
        "The following table outlines the estimated future amortization expense related to intangible assets held as of June 30, 2017:"
    )
    mock_lead_in_chunk = {
        "chunk_id": "MSFT_FY2017_2017-06-30:379",
        "content": lead_in_text,
        "metadata": {"ticker": "MSFT", "fiscal_year": 2017, "section": "Item 8"},
        "relevance_score": 0.95,
        "hop_retrieved": 1,
    }

    # 1. In mode='v3_aamr_sg', stitching should fetch chunk 380
    state_v3 = create_initial_state(
        query="Microsoft future amortization expense",
        mode="v3_aamr_sg",
        target_ticker="MSFT",
        fiscal_years=[2017],
    )
    def mock_retriever_lead_in(query, ticker=None, fiscal_years=None, top_k=6, hop=1, tickers=None):
        return [dict(mock_lead_in_chunk)]

    out_v3 = retriever_node(state_v3, custom_retriever_fn=mock_retriever_lead_in)
    accumulated_v3 = out_v3["accumulated_evidence"]
    chunk_ids_v3 = [c["chunk_id"] for c in accumulated_v3]
    assert "MSFT_FY2017_2017-06-30:379" in chunk_ids_v3
    assert "MSFT_FY2017_2017-06-30:380" in chunk_ids_v3

    # 2. In mode='v1_amr', stitching must NOT occur
    state_v1 = create_initial_state(
        query="Microsoft future amortization expense",
        mode="v1_amr",
        target_ticker="MSFT",
        fiscal_years=[2017],
    )
    out_v1 = retriever_node(state_v1, custom_retriever_fn=mock_retriever_lead_in)
    chunk_ids_v1 = [c["chunk_id"] for c in out_v1["accumulated_evidence"]]
    assert "MSFT_FY2017_2017-06-30:379" in chunk_ids_v1
    assert "MSFT_FY2017_2017-06-30:380" not in chunk_ids_v1


def test_v3_aamr_sg_debt_principal_vs_commitments_rules():
    """Verify Rule 12 in synthesizer and Rule 4 in critic exist strictly in System C v3."""
    from src.system_c.nodes.synthesizer import SYNTHESIZER_SYSTEM_PROMPT_BASE, SYNTHESIZER_SYSTEM_PROMPT_V3
    from src.system_c.nodes.critic import CRITIC_SYSTEM_PROMPT_BASE, CRITIC_SYSTEM_PROMPT_V3

    # Synthesizer prompt rules
    assert "12. DEBT PRINCIPAL VS CONTRACTUAL COMMITMENTS" in SYNTHESIZER_SYSTEM_PROMPT_V3
    assert "12. DEBT PRINCIPAL VS CONTRACTUAL COMMITMENTS" not in SYNTHESIZER_SYSTEM_PROMPT_BASE

    # Critic prompt rules
    assert "STRICT RULE 4 (DEBT PRINCIPAL VS CONTRACTUAL COMMITMENTS DISAMBIGUATION)" in CRITIC_SYSTEM_PROMPT_V3
    assert "STRICT RULE 4" not in CRITIC_SYSTEM_PROMPT_BASE


def test_v3_aamr_sg_cross_company_critic_ticker_gap_detection():
    """Verify Critic forces is_sufficient=False and appends missing ticker to missing_entities in v3."""
    from src.system_c.nodes.critic import critic_node

    state_v3 = create_initial_state(
        query="Compare debt principal of Amazon vs Johnson & Johnson in 2019",
        mode="v3_aamr_sg",
        target_ticker="AMZN",
        target_tickers=["AMZN", "JNJ"],
        fiscal_years=[2019],
    )
    state_v3["current_hop"] = 1
    state_v3["accumulated_evidence"] = [
        {
            "chunk_id": "AMZN_FY2019_2019-12-31:100",
            "content": "Amazon debt principal schedule for 2019.",
            "metadata": {"ticker": "AMZN", "fiscal_year": 2019, "section": "Item 8"},
            "relevance_score": 0.90,
            "hop_retrieved": 1,
        }
    ]

    out_v3 = critic_node(state_v3)
    assert out_v3["is_sufficient"] is False
    assert "JNJ" in out_v3["missing_entities"]


def test_v3_aamr_sg_follow_up_hop_ticker_isolation():
    """Verify retriever_node isolates search to targeted single ticker on hop >= 2 in v3."""
    from src.system_c.nodes.retriever import retriever_node

    # 1. In v3_aamr_sg, follow-up hop with single-ticker query isolates that ticker
    state_v3 = create_initial_state(
        query="Compare debt principal of Amazon vs Johnson & Johnson in 2019",
        mode="v3_aamr_sg",
        target_ticker="AMZN",
        target_tickers=["AMZN", "JNJ"],
        fiscal_years=[2019],
    )
    state_v3["current_hop"] = 2
    state_v3["current_sub_query"] = "Johnson & Johnson FY19 debt principal scheduled to repay in 2020"

    calls_v3 = []
    def mock_retriever_v3(query, ticker=None, fiscal_years=None, top_k=6, hop=1, tickers=None):
        calls_v3.append({"query": query, "ticker": ticker, "tickers": tickers, "hop": hop})
        return []

    retriever_node(state_v3, custom_retriever_fn=mock_retriever_v3)
    assert len(calls_v3) == 1
    assert calls_v3[0]["ticker"] == "JNJ"
    assert calls_v3[0]["tickers"] == ["JNJ"]

    # 2. In v1_amr, tickers are NOT isolated on follow-up hop
    state_v1 = create_initial_state(
        query="Compare debt principal of Amazon vs Johnson & Johnson in 2019",
        mode="v1_amr",
        target_ticker="AMZN",
        target_tickers=["AMZN", "JNJ"],
        fiscal_years=[2019],
    )
    state_v1["current_hop"] = 2
    state_v1["current_sub_query"] = "Johnson & Johnson FY19 debt principal scheduled to repay in 2020"

    calls_v1 = []
    def mock_retriever_v1(query, ticker=None, fiscal_years=None, top_k=6, hop=1, tickers=None):
        calls_v1.append({"query": query, "ticker": ticker, "tickers": tickers, "hop": hop})
        return []

    retriever_node(state_v1, custom_retriever_fn=mock_retriever_v1)
    assert len(calls_v1) == 1
    assert calls_v1[0]["tickers"] == ["AMZN", "JNJ"]




