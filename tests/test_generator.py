"""
Mock tests for the Conditioned Sub-Query Generator (`src/system_c/nodes/generator.py`):
(a) separate missing_entities / missing_years / missing_premises prompt fields with sentinels treated as empty,
(b) compact one-line-per-chunk evidence summary of all chunks (capped at 40),
(c) near-duplicate guard (section words and stopwords removed, overlap >= 0.8),
(d) short fallback `<ticker> <first missing entity or premise>` (<= 15 words) on a duplicate or unparseable reply.
"""

import json

import pytest

from src.system_c.graph import run_system_c
from src.system_c.nodes import generator as gen
from src.system_c.nodes.generator import generator_node
from src.system_c.state import create_initial_state


@pytest.fixture(autouse=True)
def force_mock_llm(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")


def _chunk(chunk_id, ticker="NVDA", year=2026, section="Item 7. MD&A > Results of Operations"):
    return {
        "chunk_id": chunk_id,
        "content": "Long chunk text that must never appear in the generator prompt.",
        "metadata": {"ticker": ticker, "fiscal_year": year, "section": section},
        "relevance_score": 1.0,
        "hop_retrieved": 1,
    }


def _state(query="What was NVIDIA R&D spending in 2026 and 2022?", ticker="NVDA", years=(2026,)):
    state = create_initial_state(query=query, target_ticker=ticker, fiscal_years=list(years))
    state["current_hop"] = 1
    return state


@pytest.fixture
def fake_llm(monkeypatch):
    """Replace the generator's LLM call with a fixed reply; records every prompt sent."""
    captured = {"calls": [], "reply": json.dumps({"follow_up_query": "", "reasoning": "x"})}

    def _call(state, node_name, messages, **kwargs):
        captured["calls"].append({"node": node_name, "messages": messages})
        return captured["reply"], dict(state.get("telemetry", {}))

    monkeypatch.setattr(gen, "call_llm", _call)
    return captured


def _reply(query):
    return json.dumps({"follow_up_query": query, "reasoning": "closes the gap"})


def _prompt(fake):
    return fake["calls"][-1]["messages"][1]["content"]


# (a) separate fields, sentinels treated as empty
def test_critic_lists_are_separate_prompt_fields(fake_llm):
    fake_llm["reply"] = _reply("NVIDIA FY2022 research and development expense Item 8")
    state = _state()
    state["missing_entities"] = ["2022 R&D spending"]
    state["missing_years"] = [2022]
    state["missing_premises"] = ["Disclosures and line items for 2022 R&D spending"]
    generator_node(state)
    prompt = _prompt(fake_llm)
    assert "Missing Entities: ['2022 R&D spending']" in prompt
    assert "Missing Years: [2022]" in prompt
    assert "Missing Premises: ['Disclosures and line items for 2022 R&D spending']" in prompt


def test_sentinel_values_are_treated_as_empty(fake_llm):
    fake_llm["reply"] = _reply("NVIDIA footnote table details")
    state = _state()
    state["missing_entities"] = ["None", "N/A", "null", "", "[]"]
    state["missing_years"] = ["none", "N/A"]
    state["missing_premises"] = ["nothing", "None."]
    generator_node(state)
    prompt = _prompt(fake_llm)
    assert "Missing Entities: []" in prompt
    assert "Missing Years: []" in prompt
    assert "Missing Premises: []" in prompt


def test_fy_prefixed_and_string_years_are_cleaned():
    assert gen._clean_years(["FY2022", "2023", "N/A", 2022]) == [2022, 2023]
    assert gen._clean_list(["a", "a", "None", " b "]) == ["a", "b"]


# (b) compact evidence summary of ALL chunks, capped at 40
def test_evidence_summary_lists_all_chunks_compactly(fake_llm):
    fake_llm["reply"] = _reply("NVIDIA stock-based compensation footnote")
    state = _state()
    state["accumulated_evidence"] = [
        _chunk(f"NVDA_FY2026_x:{i}", section="Item 8. Financial Statements > Note 1") for i in range(10)
    ]
    generator_node(state)
    prompt = _prompt(fake_llm)
    lines = [ln for ln in prompt.splitlines() if " | NVDA FY2026 | Item 8" in ln]
    assert len(lines) == 10  # all chunks, not just the last 4
    assert "NVDA_FY2026_x:0 | NVDA FY2026 | Item 8" in prompt
    assert "(10 chunks" in prompt
    assert "Long chunk text" not in prompt


def test_evidence_summary_is_capped_at_40_most_recent(fake_llm):
    fake_llm["reply"] = _reply("NVIDIA footnote")
    state = _state()
    state["accumulated_evidence"] = [_chunk(f"NVDA_FY2026_x:{i}") for i in range(45)]
    generator_node(state)
    prompt = _prompt(fake_llm)
    assert len([ln for ln in prompt.splitlines() if " | NVDA FY2026 | Item 7" in ln]) == 40
    assert "NVDA_FY2026_x:44 |" in prompt and "NVDA_FY2026_x:5 |" in prompt
    assert "NVDA_FY2026_x:4 |" not in prompt
    assert "(45 chunks" in prompt


def test_evidence_summary_handles_xbrl_and_missing_metadata():
    state = _state()
    state["accumulated_evidence"] = [
        {"chunk_id": "F-NVDA-2026", "content": "x", "metadata": {}, "relevance_score": 1.0, "hop_retrieved": 1},
        {"chunk_id": "AAPL_FY2024_x:3", "content": "x", "metadata": {"fiscal_year": 2024, "section": "Cover"},
         "relevance_score": 1.0, "hop_retrieved": 1},
    ]
    summary, n = gen._evidence_summary(state)
    assert n == 2
    assert summary.splitlines() == ["F-NVDA-2026 | NVDA FY? | 10-K", "AAPL_FY2024_x:3 | AAPL FY2024 | 10-K"]


# (c) near-duplicate guard
def test_section_only_swap_is_a_duplicate():
    a = "Alphabet FY2024 European Commission antitrust fines disclosed in Item 7 MD&A"
    b = "Alphabet FY2024 European Commission antitrust fines disclosed in Item 8 financial statements and notes"
    assert gen._jaccard(a, b) == 1.0
    assert gen._is_duplicate(b, [a])
    assert not gen._is_duplicate("Alphabet FY2024 content licensing commitments Item 7 MD&A", [a])


def test_stopwords_and_case_do_not_hide_a_duplicate():
    assert gen._jaccard("The NVIDIA R&D spending", "nvidia r&d SPENDING for the") == 1.0
    assert gen._jaccard("NVIDIA R&D spending", "NVIDIA debt covenants") < 0.8


def test_duplicate_of_any_earlier_query_is_replaced(fake_llm):
    state = _state()
    state["missing_entities"] = ["2022 R&D spending"]
    state["sub_queries"] = ["NVIDIA data center revenue", "NVIDIA FY2022 research development expense"]
    state["current_sub_query"] = "NVIDIA FY2022 research development expense"
    # Same words as the SECOND earlier query, differing only in section wording
    fake_llm["reply"] = _reply("NVIDIA FY2022 research development expense Item 8 financial statements")
    out = generator_node(state)
    assert out["current_sub_query"] == "NVDA 2022 R&D spending"


def test_non_duplicate_llm_query_is_kept(fake_llm):
    state = _state()
    state["missing_entities"] = ["2022 R&D spending"]
    state["sub_queries"] = ["NVIDIA data center revenue"]
    fake_llm["reply"] = _reply("NVIDIA FY2022 research and development expense Consolidated Statements of Income")
    out = generator_node(state)
    assert out["current_sub_query"] == "NVIDIA FY2022 research and development expense Consolidated Statements of Income"
    assert out["sub_queries"][-1] == out["current_sub_query"]


# (d) short fallback
def test_fallback_uses_ticker_and_first_missing_entity(fake_llm):
    state = _state()
    state["missing_entities"] = ["2022 R&D spending", "capitalization policy"]
    state["missing_premises"] = ["Disclosures for 2022 R&D spending"]
    state["sub_queries"] = ["NVIDIA stock compensation"]
    fake_llm["reply"] = "not json at all"
    out = generator_node(state)
    assert out["current_sub_query"] == "NVDA 2022 R&D spending"


def test_fallback_uses_first_premise_when_no_entity(fake_llm):
    state = _state()
    state["missing_entities"] = ["None"]
    state["missing_premises"] = ["N/A", "Debt covenant footnote"]
    fake_llm["reply"] = "{broken"
    assert generator_node(state)["current_sub_query"] == "NVDA Debt covenant footnote"


def test_fallback_is_capped_at_15_words(fake_llm):
    state = _state()
    state["missing_entities"] = [" ".join(f"word{i}" for i in range(40))]
    fake_llm["reply"] = "not json"
    query = generator_node(state)["current_sub_query"]
    assert len(query.split()) == 15
    assert query.startswith("NVDA word0 word1")


def test_fallback_with_nothing_missing_uses_the_question(fake_llm):
    state = _state(query="What was NVIDIA total revenue in FY2026?")
    fake_llm["reply"] = "not json"
    assert generator_node(state)["current_sub_query"] == "NVDA What was NVIDIA total revenue in FY2026?"


def test_fallback_without_a_ticker(fake_llm):
    state = _state(ticker=None)
    state["target_tickers"] = []
    state["missing_entities"] = ["segment operating income"]
    fake_llm["reply"] = "not json"
    assert generator_node(state)["current_sub_query"] == "segment operating income"


# Contract: outputs unchanged, one LLM call, existing loop still works
def test_output_contract_and_single_llm_call():
    state = _state()
    state["missing_entities"] = ["2022 R&D spending"]
    state["missing_premises"] = ["Disclosures for 2022 R&D spending"]  # the mock generator reads missing_premises[0]
    before = len(state["telemetry"]["calls"])
    out = generator_node(state)
    assert set(out) == {"current_hop", "current_sub_query", "sub_queries", "telemetry"}
    assert out["current_hop"] == 2
    assert out["sub_queries"].count(out["current_sub_query"]) == 1
    assert [c["node"] for c in out["telemetry"]["calls"][before:]] == ["generator"]


@pytest.mark.parametrize("mode", ["v1_amr", "v2_aamr"])
def test_full_loop_still_runs_in_both_modes(mode, monkeypatch):
    import src.system_c.graph as graph_module

    real_create_initial_state = graph_module.create_initial_state

    def never_sufficient_state(*args, **kwargs):
        state = real_create_initial_state(*args, **kwargs)
        state["telemetry"]["mock_sufficiency_score"] = 0.0  # keep the mock critic asking for more hops
        return state

    monkeypatch.setattr(graph_module, "create_initial_state", never_sufficient_state)
    res = run_system_c(
        query="How did NVDA revenue change in 2026 and what footnote debt covenants applied?",
        max_hops=3,
        mode=mode,
    )
    assert res["current_hop"] == 3
    assert res["final_answer"]
    assert len(res["sub_queries"]) >= 2
