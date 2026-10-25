"""
Unit tests for Aryan's Guardrail + Repair hardening (workplan §4.1), run in mock mode.

Covers: number extraction, per-sentence cited-chunk matching, scale normalisation, derived figures,
uncited numbers, invalid citations, the switchable semantic check, repair inputs, and the guardrail and
repair node output keys.
"""

import pytest

from src.system_c.guardrails.verifier import (
    _extract_candidate_numbers,
    _extract_numbers,
    _split_sentences,
    guardrail_node,
    verify_numerical_grounding,
)
from src.system_c.state import create_initial_state

TABLE_CHUNK = {
    "chunk_id": "NVDA_FY2026_2026-01-25:284",
    "metadata": {"ticker": "NVDA", "fiscal_year": 2026, "section": "Item 8"},
    "content": "CONSOLIDATED STATEMENTS OF INCOME\n(In millions, except per share data)\n"
    "Revenue $ 60,922 $ 52,977\nGross margin 75.0%",
}
TEXT_CHUNK = {
    "chunk_id": "NVDA_FY2026_2026-01-25:217",
    "metadata": {"ticker": "NVDA", "fiscal_year": 2026, "section": "Item 7"},
    "content": "Data Center demand remained strong, driven by accelerated computing platforms.",
}
OTHER_CHUNK = {
    "chunk_id": "NVDA_FY2026_2026-01-25:441",
    "metadata": {"ticker": "NVDA", "fiscal_year": 2026, "section": "Item 7"},
    "content": "Net income was $4,321 million for the year.",
}
TABLE_TAG = "[NVDA FY2026, Item 8, NVDA_FY2026_2026-01-25:284]"
TEXT_TAG = "[NVDA FY2026, Item 7, NVDA_FY2026_2026-01-25:217]"
EVIDENCE = [TABLE_CHUNK, TEXT_CHUNK, OTHER_CHUNK]


@pytest.fixture(autouse=True)
def force_mock_llm(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    monkeypatch.delenv("GUARDRAIL_SEMANTIC_CHECK", raising=False)
    monkeypatch.delenv("GUARDRAIL_JUDGE_MODEL", raising=False)
    monkeypatch.delenv("GUARDRAIL_JUDGE_PROVIDER", raising=False)


def _state(answer, evidence=EVIDENCE):
    state = create_initial_state(query="What was NVDA revenue in FY2026?", target_ticker="NVDA", fiscal_years=[2026])
    state["draft_answer"] = answer
    state["accumulated_evidence"] = list(evidence)
    return state


def _numbers(report):
    return [n for s in report["sentences"] for n in s["numbers"]]


def test_extracts_dollar_scale_percent_word_and_bps():
    values = [n["value"] for n in _extract_numbers(
        "Revenue was $500 million, up 12 percent; margin of 75% and $61 billion, a $5B buyback and 50 bps."
    )]
    assert values == ["$500 million", "12 percent", "75%", "$61 billion", "$5B", "50 bps"]
    # Legacy tokens stay plain so existing callers keep working
    assert _extract_candidate_numbers("Revenue of $999,999 million and 88.5% margin") == ["999,999", "88.5%"]


def test_skips_years_small_counts_and_citation_tags():
    text = f"In FY2026 and fiscal 2025, NVIDIA had 3 segments and 36 months of backlog {TABLE_TAG}."
    assert _extract_numbers(text) == []


def test_sentence_split_keeps_trailing_tags_and_abbreviations():
    answer = f"NVIDIA Corp. grew revenue. {TABLE_TAG} Demand stayed strong {TEXT_TAG}."
    sentences = _split_sentences(answer)
    assert len(sentences) == 2
    assert sentences[0].endswith(TABLE_TAG)
    assert sentences[0].startswith("NVIDIA Corp. grew")


def test_sentence_split_ignores_periods_inside_citation_tags():
    tag = "[NVDA FY2026, Item 15. Exhibits and Financial Statement Schedules, NVDA_FY2026_2026-01-25:284]"
    answer = f"Revenue was $60.9 billion ({tag}). Demand stayed strong {TEXT_TAG}."
    sentences = _split_sentences(answer)
    assert sentences == [f"Revenue was $60.9 billion ({tag}).", f"Demand stayed strong {TEXT_TAG}."]
    report = verify_numerical_grounding(answer, EVIDENCE)
    assert report["sentences"][0]["chunk_ids"] == ["NVDA_FY2026_2026-01-25:284"]
    assert [n["status"] for n in _numbers(report)] == ["verified"]


def test_number_only_in_uncited_chunk_is_ungrounded():
    report = verify_numerical_grounding(f"Net income was $4,321 million {TEXT_TAG}.", EVIDENCE)
    assert [n["status"] for n in _numbers(report)] == ["ungrounded"]
    assert "4,321" in report["ungrounded_numbers"]


def test_scale_match_billion_vs_millions_table_is_verified():
    report = verify_numerical_grounding(f"Revenue was $60.9 billion {TABLE_TAG}.", EVIDENCE)
    assert [n["status"] for n in _numbers(report)] == ["verified"]
    assert report["numerical_grounding_error_rate"] == 0.0


def test_stated_precision_is_enforced():
    # $61.5 billion is outside the half-unit tolerance (0.05bn) of 60,922 million
    report = verify_numerical_grounding(f"Revenue was $61.5 billion {TABLE_TAG}.", EVIDENCE)
    assert [n["status"] for n in _numbers(report)] == ["ungrounded"]


AAPL_XBRL = {
    "chunk_id": "F-AAPL-2024",
    "metadata": {"ticker": "AAPL", "fiscal_year": 2024},
    "content": "[F-AAPL-2024] (AAPL FY2024 reported financials; amounts in USD, EPSDiluted in USD per share)\n"
    "fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,"
    "StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted\r\n"
    "2024,2024-09-28,391035000000,93736000000,123216000000,364980000000,308030000000,"
    "56950000000,29943000000,118254000000,6.08",
}


def test_xbrl_csv_row_verifies_revenue_and_net_income():
    answer = "Apple's total revenue in FY2024 was $391.035 billion, and net income was $93.736 billion [F-AAPL-2024]."
    report = verify_numerical_grounding(answer, [AAPL_XBRL])
    assert [(n["value"], n["status"]) for n in _numbers(report)] == [
        ("$391.035 billion", "verified"),
        ("$93.736 billion", "verified"),
    ]


def test_comma_grouped_number_does_not_run_into_more_digits():
    # In plain text too, `28,391035000000` must not be read as 28,391
    chunk = {"chunk_id": "AAPL_FY2024:1", "metadata": {}, "content": "row: 2024-09-28,391035000000"}
    report = verify_numerical_grounding("Revenue was $391.035 billion [AAPL_FY2024:1].", [chunk])
    assert [n["status"] for n in _numbers(report)] == ["verified"]
    assert _extract_candidate_numbers("value 28,391035 here") == ["391035"]  # not "28,391"


def test_scaled_figure_matches_bare_table_number_with_exact_digits():
    googl = {
        "chunk_id": "GOOGL_FY2024_2024-12-31:191",
        "metadata": {},
        "content": "ITEM 7 > Revenues (table)\n| Total revenues | $307,394 | $350,018 |",
    }
    report = verify_numerical_grounding(
        "Alphabet's total revenue for FY2024 was $350,018 million [GOOGL_FY2024_2024-12-31:191].", [googl]
    )
    assert [n["status"] for n in _numbers(report)] == ["verified"]


def test_short_bare_number_does_not_verify_scaled_figure():
    chunk = {"chunk_id": "X_FY2024:1", "metadata": {}, "content": "The company operates 12 data centers."}
    report = verify_numerical_grounding("Capex was $12 billion [X_FY2024:1].", [chunk])
    assert [n["status"] for n in _numbers(report)] == ["ungrounded"]


def test_bare_number_only_counts_from_the_sentences_own_cited_chunk():
    googl = {"chunk_id": "GOOGL:191", "metadata": {}, "content": "| Total revenues | $350,018 |"}
    other = {"chunk_id": "GOOGL:12", "metadata": {}, "content": "Alphabet is headquartered in Mountain View."}
    report = verify_numerical_grounding("Alphabet's total revenue was $350,018 million [GOOGL:12].", [googl, other])
    assert [n["status"] for n in _numbers(report)] == ["ungrounded"]


MSFT_277 = {
    "chunk_id": "MSFT_FY2024_2024-06-30:277",
    "metadata": {"ticker": "MSFT", "fiscal_year": 2024, "section": "Item 8. Financial Statements"},
    "content": "INCOME STATEMENTS\n(In millions, except per share amounts)\n| Total revenue | 245,122 | 211,915 |",
}
GOOGL_191 = {
    "chunk_id": "GOOGL_FY2024_2024-12-31:191",
    "metadata": {"ticker": "GOOGL", "fiscal_year": 2024, "section": "Item 7. MD&A > Revenues"},
    "content": "Revenues (table)\n| Total revenues | $307,394 | $350,018 |",
}
MSFT_TAG = "[MSFT FY2024, Item 8, MSFT_FY2024_2024-06-30:277]"
GOOGL_TAG = "[GOOGL FY2024, Item 7, GOOGL_FY2024_2024-12-31:191]"
GAP = "Alphabet's total revenue exceeded Microsoft's by $104,896 million"


def test_cross_chunk_difference_needs_both_chunks_cited():
    evidence = [MSFT_277, GOOGL_191]
    one = verify_numerical_grounding(f"{GAP} {GOOGL_TAG}.", evidence)
    assert [n["status"] for n in _numbers(one)] == ["ungrounded"]  # guardrail stays strict

    both = verify_numerical_grounding(f"{GAP} {GOOGL_TAG} {MSFT_TAG}.", evidence)
    assert _numbers(both) == [
        {"value": "$104,896 million", "status": "derived", "derived_from": ["350,018", "245,122"], "operation": "difference"}
    ]


def test_repair_names_both_blocks_for_cross_chunk_computed_figure(monkeypatch):
    from src.system_c.nodes.repair import REPAIR_SYSTEM_PROMPT, repair_node

    state = _state(f"{GAP} {GOOGL_TAG}.", evidence=[MSFT_277, GOOGL_191, TEXT_CHUNK])
    state.update(guardrail_node(state))
    assert state["guardrail_passed"] is False

    captured = {}

    def fake_call_llm(state, node_name, messages, **kw):
        captured["prompt"] = messages[-1]["content"]
        return f"{GAP} {GOOGL_TAG} {MSFT_TAG}.", state.get("telemetry", {})

    monkeypatch.setattr("src.system_c.nodes.repair.call_llm", fake_call_llm)
    out = repair_node(state)

    assert f"cite BOTH: {MSFT_TAG} {GOOGL_TAG}" in captured["prompt"]
    hint = next(line for line in captured["prompt"].splitlines() if "Computed figure:" in line)
    assert "$104,896 million = difference of" in hint and "350,018" in hint and "245,122" in hint
    assert "cite BOTH blocks" in REPAIR_SYSTEM_PROMPT
    state.update(out)
    assert guardrail_node(state)["guardrail_passed"] is True


def test_computed_growth_is_derived_and_not_an_error():
    report = verify_numerical_grounding(f"Revenue grew 15% year over year {TABLE_TAG}.", EVIDENCE)
    nums = _numbers(report)
    assert nums == [
        {"value": "15%", "status": "derived", "derived_from": ["60,922", "52,977"], "operation": "growth"}
    ]
    assert report["derived_numbers"][0]["operation"] == "growth"
    assert report["numerical_grounding_error_rate"] == 0.0
    assert report["ungrounded_numbers"] == []


def test_number_without_citation_is_uncited_and_fails():
    state = _state(f"Revenue was $60.9 billion. Demand stayed strong for accelerated computing {TEXT_TAG}.")
    out = guardrail_node(state)
    report = out["guardrail_report"]
    assert report["uncited_numbers"] == ["60.9"]
    assert report["sentences"][0]["numbers"][0]["status"] == "uncited"
    assert report["numerical_grounding_error_rate"] == 1.0
    assert out["guardrail_passed"] is False
    assert report["unverified_sentences"] == ["Revenue was $60.9 billion."]


def test_tag_that_maps_to_no_chunk_is_invalid_and_fails():
    bad_tag = "[NVDA FY2026, Item 7, NVDA_FY2026_2026-01-25:999]"
    out = guardrail_node(_state(f"Demand stayed strong for accelerated computing {bad_tag}."))
    assert out["guardrail_report"]["invalid_citations"] == [bad_tag]
    assert out["guardrail_passed"] is False


def test_partial_chunk_id_prefix_does_not_resolve():
    # `...:28` must not resolve to `...:284`
    report = verify_numerical_grounding("Revenue was $60.9 billion [NVDA FY2026, Item 8, NVDA_FY2026_2026-01-25:28].", EVIDENCE)
    assert report["invalid_citations"] == ["[NVDA FY2026, Item 8, NVDA_FY2026_2026-01-25:28]"]


def test_resolver_pulls_chunk_id_out_of_handoff_format_tag():
    from src.system_c.guardrails.verifier import _resolve_citation_tags

    chunk = {"chunk_id": "NVDA_FY2026_2026-01-25:220", "metadata": {}, "content": "Revenue was $215,938 million."}
    tag = "[NVDA FY2026, Item 7, NVDA_FY2026_2026-01-25:220]"
    tags, chunk_ids, invalid = _resolve_citation_tags(f"Revenue was $215,938 million {tag}.", [chunk])
    assert tags == [tag]
    assert chunk_ids == ["NVDA_FY2026_2026-01-25:220"]
    assert invalid == []


def test_resolver_accepts_xbrl_tag():
    from src.system_c.guardrails.verifier import _resolve_citation_tags

    chunk = {"chunk_id": "F-NVDA-2026", "metadata": {}, "content": "Revenue,215938000000"}
    tags, chunk_ids, invalid = _resolve_citation_tags("Revenue was $215.9 billion [F-NVDA-2026].", [chunk])
    assert tags == ["[F-NVDA-2026]"]
    assert chunk_ids == ["F-NVDA-2026"]
    assert invalid == []
    report = verify_numerical_grounding("Revenue was $215.9 billion [F-NVDA-2026].", [chunk])
    assert [n["status"] for n in _numbers(report)] == ["verified"]


def test_semantic_switch_controls_llm_call(monkeypatch):
    answer = f"Data Center demand remained strong for accelerated computing {TEXT_TAG}."

    out_on = guardrail_node(_state(answer))
    calls_on = [c for c in out_on["telemetry"].get("calls", []) if c["node"] == "guardrail_semantic"]
    assert len(calls_on) == 1
    assert out_on["guardrail_report"]["semantic_check_enabled"] is True
    # Mock mode: unparsed judge output counts as supported
    assert out_on["guardrail_report"]["sentences"][0]["semantic_verdict"] == "supported"
    assert out_on["guardrail_passed"] is True

    monkeypatch.setenv("GUARDRAIL_SEMANTIC_CHECK", "0")
    out_off = guardrail_node(_state(answer))
    calls_off = [c for c in out_off["telemetry"].get("calls", []) if c["node"] == "guardrail_semantic"]
    assert calls_off == []
    assert out_off["guardrail_report"]["semantic_check_enabled"] is False
    assert out_off["guardrail_report"]["sentences"][0]["semantic_verdict"] is None


def test_live_mode_parse_failure_is_unchecked_not_failed(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setattr(
        "src.system_c.guardrails.verifier.call_llm",
        lambda state, node_name, messages, **kw: ("not json at all", state.get("telemetry", {})),
    )
    sentence = f"Data Center demand remained strong for accelerated computing {TEXT_TAG}."
    out = guardrail_node(_state(sentence))
    report = out["guardrail_report"]
    assert report["sentences"][0]["semantic_verdict"] == "unchecked"
    assert report["unchecked_sentences"] == [sentence]
    assert report["unverified_sentences"] == []
    assert out["guardrail_passed"] is True


def test_unsupported_semantic_verdict_fails(monkeypatch):
    monkeypatch.setattr(
        "src.system_c.guardrails.verifier.call_llm",
        lambda state, node_name, messages, **kw: (
            '```json\n{"results": [{"id": 1, "verdict": "unsupported", "reason": "not in chunk"}]}\n```',
            state.get("telemetry", {}),
        ),
    )
    out = guardrail_node(_state(f"NVIDIA exited the gaming business entirely {TEXT_TAG}."))
    report = out["guardrail_report"]
    assert report["sentences"][0]["semantic_verdict"] == "unsupported"
    assert report["sentences"][0]["reason"] == "not in chunk"
    assert out["guardrail_passed"] is False


def test_uncited_factual_sentence_judged_against_all_evidence_in_same_call(monkeypatch):
    captured = []

    def fake_call_llm(state, node_name, messages, **kw):
        captured.append(messages[-1]["content"])
        return (
            '{"results": [{"id": 1, "verdict": "supported", "reason": "ok"},'
            ' {"id": 2, "verdict": "unsupported", "reason": "not in any chunk"},'
            ' {"id": 3, "verdict": "supported", "reason": "Antarctica is not in the evidence"}]}',
            state.get("telemetry", {}),
        )

    monkeypatch.setattr("src.system_c.guardrails.verifier.call_llm", fake_call_llm)
    cited = f"Data Center demand remained strong for accelerated computing {TEXT_TAG}."
    uncited = "NVIDIA opened a new headquarters on the Moon this year."
    not_disclosed = "Revenue from Antarctica is not disclosed in the filing."
    out = guardrail_node(_state(f"{cited} {uncited} {not_disclosed}"))
    report = out["guardrail_report"]

    assert len(captured) == 1  # one batched judge call
    prompt = captured[0]
    assert f"Sentence 2 (uncited): {uncited}" in prompt
    assert "ALL RETRIEVED EVIDENCE" in prompt and OTHER_CHUNK["content"] in prompt
    assert f"Sentence 3 (uncited): {not_disclosed}" in prompt  # refusals go to the judge too
    assert report["uncited_claim_sentences"] == [uncited, not_disclosed]
    verdicts = {s["text"]: s["semantic_verdict"] for s in report["sentences"]}
    assert verdicts == {cited: "supported", uncited: "unsupported", not_disclosed: "supported"}
    assert report["unverified_sentences"] == [uncited]
    assert out["guardrail_passed"] is False


def test_partial_verdict_fails_and_is_counted_separately(monkeypatch):
    monkeypatch.setattr(
        "src.system_c.guardrails.verifier.call_llm",
        lambda state, node_name, messages, **kw: (
            '{"results": [{"id": 1, "verdict": "partial", "reason": "half supported"},'
            ' {"id": 2, "verdict": "unsupported", "reason": "absent"},'
            ' {"id": 3, "verdict": "supported", "reason": "ok"}]}',
            state.get("telemetry", {}),
        ),
    )
    s1 = f"Demand stayed strong and Blackwell was the majority of revenue {TEXT_TAG}."
    s2 = f"NVIDIA exited the gaming business entirely {TEXT_TAG}."
    s3 = f"Data Center demand remained strong for accelerated computing {TEXT_TAG}."
    out = guardrail_node(_state(f"{s1} {s2} {s3}"))
    report = out["guardrail_report"]
    assert report["semantic_verdict_counts"] == {"supported": 1, "partial": 1, "unsupported": 1, "unchecked": 0}
    assert report["unverified_sentences"] == [s1, s2]
    assert out["guardrail_passed"] is False


def test_partial_sentence_is_sent_to_repair(monkeypatch):
    from src.system_c.nodes.repair import repair_node

    monkeypatch.setattr(
        "src.system_c.guardrails.verifier.call_llm",
        lambda state, node_name, messages, **kw: (
            '{"results": [{"id": 1, "verdict": "partial", "reason": "Blackwell claim not in chunk"}]}',
            state.get("telemetry", {}),
        ),
    )
    sentence = f"Demand stayed strong and Blackwell was the majority of revenue {TEXT_TAG}."
    state = _state(sentence)
    state.update(guardrail_node(state))
    captured = {}

    def fake_repair_llm(state, node_name, messages, **kw):
        captured["prompt"] = messages[-1]["content"]
        return sentence, state.get("telemetry", {})

    monkeypatch.setattr("src.system_c.nodes.repair.call_llm", fake_repair_llm)
    out = repair_node(state)
    assert out["repair_history"][0]["unverified_sentences"] == [sentence]
    assert "Semantic verdict: partial - Blackwell claim not in chunk" in captured["prompt"]


def test_not_disclosed_claim_is_judged_not_auto_passed(monkeypatch):
    import src.system_c.guardrails.verifier as verifier

    # Evidence DOES contain net income ($4,321 million), so "not disclosed" is a false refusal
    refusal = "Net income is not disclosed in the filing."
    prompts = []
    real_call_llm = verifier.call_llm

    def spy(state, node_name, messages, **kw):
        prompts.append(messages[-1]["content"])
        return real_call_llm(state, node_name, messages, **kw)

    # Mock mode: the refusal must reach the judge instead of being auto-passed
    monkeypatch.setattr(verifier, "call_llm", spy)
    report = guardrail_node(_state(refusal))["guardrail_report"]
    assert len(prompts) == 1 and f"Sentence 1 (uncited): {refusal}" in prompts[0]
    assert OTHER_CHUNK["content"] in prompts[0]
    assert report["sentences"][0]["reason"] == "mock mode: judge output not parsed"

    # A judge that spots the figure in the evidence: the refusal is not supported and fails
    monkeypatch.setattr(
        verifier,
        "call_llm",
        lambda state, node_name, messages, **kw: (
            '{"results": [{"id": 1, "verdict": "unsupported", "reason": "net income $4,321 million is in the evidence"}]}',
            state.get("telemetry", {}),
        ),
    )
    out = guardrail_node(_state(refusal))
    assert out["guardrail_report"]["sentences"][0]["semantic_verdict"] != "supported"
    assert out["guardrail_report"]["unverified_sentences"] == [refusal]
    assert out["guardrail_passed"] is False
    assert "supported\" ONLY if the evidence" in verifier.SEMANTIC_SYSTEM_PROMPT


def test_judge_without_override_uses_main_model(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.delenv("LLM_MODEL", raising=False)
    seen = {}

    def fake_call_llm(state, node_name, messages, **kw):
        seen.update(kw)
        return '{"results": [{"id": 1, "verdict": "supported", "reason": "ok"}]}', state.get("telemetry", {})

    monkeypatch.setattr("src.system_c.guardrails.verifier.call_llm", fake_call_llm)
    out = guardrail_node(_state(f"Data Center demand remained strong for accelerated computing {TEXT_TAG}."))
    assert "provider" not in seen and "model" not in seen
    assert out["guardrail_report"]["semantic_judge_provider"] == "openai"
    assert out["guardrail_report"]["semantic_judge_model"] == "gpt-4o-mini"


def test_judge_override_is_ignored_in_mock_mode(monkeypatch):
    monkeypatch.setenv("GUARDRAIL_JUDGE_PROVIDER", "groq")
    monkeypatch.setenv("GUARDRAIL_JUDGE_MODEL", "openai/gpt-oss-120b")
    out = guardrail_node(_state(f"Data Center demand remained strong for accelerated computing {TEXT_TAG}."))
    calls = [c for c in out["telemetry"]["calls"] if c["node"] == "guardrail_semantic"]
    assert [(c["provider"], c["model"]) for c in calls] == [("mock", "mock")]
    assert out["guardrail_report"]["semantic_judge_provider"] == "mock"
    assert out["guardrail_report"]["semantic_judge_model"] == "mock"


def test_call_llm_override_is_used_and_recorded(monkeypatch):
    import src.system_c.llm as llm

    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.delenv("LLM_MODEL", raising=False)
    used = {}

    def fake_api(provider, model, messages, temperature=0.0, max_tokens=1024):
        used["provider"], used["model"] = provider, model
        return "ok", 10, 5

    monkeypatch.setattr(llm, "_call_groq_or_openai", fake_api)
    state = _state("x")
    _, tel = llm.call_llm(state, "guardrail_semantic", [{"role": "user", "content": "hi"}],
                          provider="groq", model="openai/gpt-oss-120b")
    assert used == {"provider": "groq", "model": "openai/gpt-oss-120b"}
    assert (tel["calls"][-1]["provider"], tel["calls"][-1]["model"]) == ("groq", "openai/gpt-oss-120b")

    _, tel = llm.call_llm(state, "synthesizer", [{"role": "user", "content": "hi"}])
    assert used == {"provider": "openai", "model": "gpt-4o-mini"}  # no override -> configured model


def test_report_keeps_legacy_keys_and_adds_new_ones():
    out = guardrail_node(_state(f"Revenue was $60.9 billion with a 75.0% gross margin {TABLE_TAG}."))
    report = out["guardrail_report"]
    legacy = {
        "verified_numbers", "ungrounded_numbers", "numerical_grounding_error_rate",
        "faithfulness_score", "total_numerical_claims", "has_inline_citations",
    }
    new = {
        "sentences", "unverified_sentences", "unchecked_sentences", "derived_numbers",
        "uncited_numbers", "invalid_citations", "semantic_check_enabled", "semantic_judge_model",
        "semantic_judge_provider", "uncited_claim_sentences", "semantic_verdict_counts",
    }
    assert legacy | new <= set(report)
    assert report["verified_numbers"] == ["60.9", "75.0%"]
    assert set(report["sentences"][0]) == {"text", "citations", "chunk_ids", "numbers", "semantic_verdict", "reason"}
    assert out["guardrail_passed"] is True


@pytest.mark.parametrize(
    "answer",
    [f"Revenue was $60.9 billion {TABLE_TAG}.", f"Net income was $4,321 million {TEXT_TAG}."],
    ids=["passes", "fails"],
)
def test_guardrail_output_keys_match_handoff_contract(answer):
    out = guardrail_node(_state(answer))
    assert set(out) == {"final_answer", "guardrail_passed", "guardrail_report", "telemetry"}


def test_repair_output_keys_and_citations_follow_repaired_text(monkeypatch):
    from src.system_c.nodes.repair import repair_node

    state = _state(f"Net income was $4,321 million {TEXT_TAG}.")
    state.update(guardrail_node(state))
    repaired = f"Revenue was $60.9 billion {TABLE_TAG}."
    monkeypatch.setattr(
        "src.system_c.nodes.repair.call_llm", lambda state, node_name, messages, **kw: (repaired, state.get("telemetry", {}))
    )
    out = repair_node(state)

    assert set(out) == {"draft_answer", "final_answer", "citations", "repair_count", "repair_history", "telemetry"}
    assert [(c["tag"], c["chunk_id"]) for c in out["citations"]] == [(TABLE_TAG, TABLE_CHUNK["chunk_id"])]
    assert out["citations"][0]["supported_claim"] == "Revenue was $60.9 billion."


def test_repair_asks_to_cite_uncited_sentence_with_exact_block_tag(monkeypatch):
    from src.system_c.nodes.repair import REPAIR_SYSTEM_PROMPT, repair_node

    state = _state(f"Revenue was $60.9 billion. Demand stayed strong for accelerated computing {TEXT_TAG}.")
    state.update(guardrail_node(state))
    assert state["guardrail_report"]["uncited_numbers"] == ["60.9"]

    captured = {}

    def fake_call_llm(state, node_name, messages, **kw):
        captured["system"], captured["prompt"] = messages[0]["content"], messages[-1]["content"]
        return f"Revenue was $60.9 billion {TABLE_TAG}.", state.get("telemetry", {})

    monkeypatch.setattr("src.system_c.nodes.repair.call_llm", fake_call_llm)
    out = repair_node(state)

    assert "EXACT tag" in REPAIR_SYSTEM_PROMPT and "remove the sentence" in REPAIR_SYSTEM_PROMPT
    assert "(no valid citation)" in captured["prompt"]
    # The block that actually holds 60,922 (in millions) is offered with its exact tag; others are not
    assert f"Evidence blocks containing its figures: {TABLE_TAG}" in captured["prompt"]
    # Re-audit of the repaired answer now passes
    state.update(out)
    assert guardrail_node(state)["guardrail_passed"] is True


def test_repair_receives_unverified_sentences_with_cited_chunks(monkeypatch):
    from src.system_c.nodes.repair import repair_node

    answer = f"Net income was $4,321 million {TEXT_TAG}. Revenue was $60.9 billion {TABLE_TAG}."
    state = _state(answer)
    state.update(guardrail_node(state))
    assert state["guardrail_passed"] is False

    captured = {}

    def fake_call_llm(state, node_name, messages, **kw):
        captured["prompt"] = messages[-1]["content"]
        return "Revenue was $60.9 billion " + TABLE_TAG + ".", state.get("telemetry", {})

    monkeypatch.setattr("src.system_c.nodes.repair.call_llm", fake_call_llm)
    out = repair_node(state)

    prompt = captured["prompt"]
    assert f"Net income was $4,321 million {TEXT_TAG}." in prompt
    assert TEXT_CHUNK["content"] in prompt
    assert out["repair_history"][0]["unverified_sentences"] == [f"Net income was $4,321 million {TEXT_TAG}."]
    assert "4,321" in out["repair_history"][0]["flagged_numbers"]
    # Verified sentence is not sent as unverified
    assert prompt.count("Revenue was $60.9 billion") == 1
