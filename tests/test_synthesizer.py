"""
Unit tests for Answer Synthesizer & Citation Mapper (RQ2 Citation Attribution), run in mock mode.

Covers: `[E<n>]` label expansion to handoff-format tags, the shared strict resolver, one CitationRecord
per (sentence, chunk), and final `citations` matching the final answer through the
synthesizer -> guardrail -> repair -> guardrail loop.
"""

import pytest

from src.system_c.guardrails.citations import (
    MAX_TAG_CHARS,
    build_citation_records,
    expand_labels,
    format_tag,
    short_section,
)
from src.system_c.guardrails.verifier import guardrail_node, verify_numerical_grounding
from src.system_c.nodes.synthesizer import extract_citations_from_answer, synthesizer_node
from src.system_c.state import create_initial_state

MDA_205 = {
    "chunk_id": "NVDA_FY2026_2026-01-25:205",
    "metadata": {
        "ticker": "NVDA",
        "fiscal_year": 2026,
        "section": "Item 7. Management's Discussion and Analysis of Financial Condition and Results of "
        "Operations > Fiscal Year 2026 Summary",
    },
    "content": "Revenue for fiscal year 2026 was $215.9 billion, up 65% from a year ago. "
    "Data Center revenue for fiscal year 2026 was up 68% from a year ago.",
}
MDA_213 = {
    "chunk_id": "NVDA_FY2025_2025-01-26:213",
    "metadata": {"ticker": "NVDA", "fiscal_year": 2025, "section": "Item 7. Management's Discussion > Summary"},
    "content": "Revenue for fiscal year 2025 was $130.5 billion, up 114% from a year ago. "
    "Data Center revenue for fiscal year 2025 was up 142% from a year ago.",
}
RISK_57 = {
    "chunk_id": "NVDA_FY2026_2026-01-25:57",
    "metadata": {"ticker": "NVDA", "fiscal_year": 2026, "section": "Item 1A. Risk Factors > China"},
    "content": "Increased oversight of digital platform companies may adversely affect our Data Center revenue.",
}
XBRL = {
    "chunk_id": "F-NVDA-2026",
    "metadata": {"ticker": "NVDA", "fiscal_year": 2026, "section": "SEC XBRL Reported Financials (financials.csv)"},
    "content": "fiscal_year,Revenue,NetIncome\n2026,215938000000,120067000000",
}
EVIDENCE = [MDA_205, MDA_213, RISK_57, XBRL]
LABELS = {"E1": MDA_205, "E2": MDA_213, "E3": RISK_57, "E4": XBRL}
TAG_205 = "[NVDA FY2026, Item 7, NVDA_FY2026_2026-01-25:205]"
TAG_213 = "[NVDA FY2025, Item 7, NVDA_FY2025_2025-01-26:213]"
TAG_57 = "[NVDA FY2026, Item 1A, NVDA_FY2026_2026-01-25:57]"


@pytest.fixture(autouse=True)
def force_mock_llm(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    for var in ("GUARDRAIL_SEMANTIC_CHECK", "GUARDRAIL_JUDGE_MODEL", "GUARDRAIL_JUDGE_PROVIDER"):
        monkeypatch.delenv(var, raising=False)


def _state(answer=None, evidence=EVIDENCE):
    state = create_initial_state(query="How did NVDA Data Center revenue change?", target_ticker="NVDA", fiscal_years=[2026])
    state["accumulated_evidence"] = list(evidence)
    if answer is not None:
        state["draft_answer"] = answer
    return state


def test_label_expands_to_handoff_format_with_short_section():
    text, unknown = expand_labels("Data Center revenue was up 68% [E1].", LABELS)
    assert text == f"Data Center revenue was up 68% {TAG_205}."
    assert unknown == []


def test_xbrl_label_expands_to_f_tag():
    text, _ = expand_labels("Revenue was $215,938 million [E4].", LABELS)
    assert text == "Revenue was $215,938 million [F-NVDA-2026]."


@pytest.mark.parametrize("labels", ["[E1, E2]", "[E1][E2]", "[E1] [E2]", "[ E1 ,E2 ]"])
def test_grouped_and_adjacent_labels_expand_to_two_tags(labels):
    text, _ = expand_labels(f"Data Center grew 68% after 142% {labels}.", LABELS)
    assert text == f"Data Center grew 68% after 142% {TAG_205} {TAG_213}."


def test_backticks_are_stripped_around_labels_and_tags():
    text, _ = expand_labels(f"Growth was 68% `[E1]`. Risks remain ``{TAG_57}``.", LABELS)
    assert "`" not in text
    assert text == f"Growth was 68% {TAG_205}. Risks remain {TAG_57}."


def test_expanded_tags_stay_within_80_chars_even_with_long_sections():
    long_section = {
        "chunk_id": "NVDA_FY2026_2026-01-25:441",
        "metadata": {"ticker": "NVDA", "fiscal_year": 2026, "section": "Exhibits " * 30},
    }
    long_id = {"chunk_id": "NVDA_FY2026_" + "X" * 80 + ":1", "metadata": {"ticker": "NVDA", "fiscal_year": 2026}}
    assert format_tag(long_section) == "[NVDA FY2026, 10-K, NVDA_FY2026_2026-01-25:441]"
    assert format_tag(long_id) == f"[{long_id['chunk_id']}]"  # chunk-id-only fallback
    for ch in (MDA_205, MDA_213, RISK_57, XBRL, long_section):
        assert len(format_tag(ch)) <= MAX_TAG_CHARS


def test_short_section_variants():
    assert short_section("Item 1A. Risk Factors > China") == "Item 1A"
    assert short_section("Item 15. Exhibits and Financial Statement Schedules > Notes") == "Item 15"
    assert short_section("Cover page") == "10-K"
    assert short_section(None) == "10-K"


def test_unknown_label_stays_and_guardrail_reports_it_invalid():
    text, unknown = expand_labels("Data Center demand stayed strong for accelerated computing [E1, E99].", LABELS)
    assert unknown == ["E99"]
    assert text == f"Data Center demand stayed strong for accelerated computing {TAG_205} [E99]."
    out = guardrail_node(_state(text))
    assert out["guardrail_report"]["invalid_citations"] == ["[E99]"]
    assert out["guardrail_passed"] is False


def test_one_record_per_sentence_chunk_pair_with_sentence_as_claim():
    answer = f"Data Center revenue was up 68% in FY2026 after 142% in FY2025 {TAG_205} {TAG_213}."
    records = build_citation_records(answer, EVIDENCE)
    assert [r["chunk_id"] for r in records] == [MDA_205["chunk_id"], MDA_213["chunk_id"]]
    assert [r["tag"] for r in records] == [TAG_205, TAG_213]
    claim = "Data Center revenue was up 68% in FY2026 after 142% in FY2025."
    assert all(r["supported_claim"] == claim for r in records)
    assert records[0]["section"] == MDA_205["metadata"]["section"]  # full section kept in the record
    assert records[1]["fiscal_year"] == 2025


def test_two_sentences_citing_same_chunk_give_two_records():
    answer = f"Revenue was $215.9 billion {TAG_205}. Data Center revenue was up 68% {TAG_205}."
    records = build_citation_records(answer, EVIDENCE)
    assert [r["chunk_id"] for r in records] == [MDA_205["chunk_id"]] * 2
    assert [r["supported_claim"] for r in records] == ["Revenue was $215.9 billion.", "Data Center revenue was up 68%."]


def test_section_only_tag_is_invalid_no_fallback():
    answer = "Data Center demand stayed strong for accelerated computing [NVDA FY2026, Item 7]."
    assert build_citation_records(answer, EVIDENCE) == []
    report = verify_numerical_grounding(answer, EVIDENCE)
    assert report["invalid_citations"] == ["[NVDA FY2026, Item 7]"]


def test_raw_chunk_id_tag_resolves():
    answer = "Data Center revenue was up 68% [NVDA_FY2026_2026-01-25:205]."
    report = verify_numerical_grounding(answer, EVIDENCE)
    assert report["invalid_citations"] == []
    assert report["sentences"][0]["chunk_ids"] == [MDA_205["chunk_id"]]
    assert [n["status"] for s in report["sentences"] for n in s["numbers"]] == ["verified"]
    assert [r["chunk_id"] for r in build_citation_records(answer, EVIDENCE)] == [MDA_205["chunk_id"]]


def test_extract_citations_from_answer_keeps_old_signature():
    records = extract_citations_from_answer(f"Data Center revenue was up 68% {TAG_205}.", EVIDENCE)
    assert len(records) == 1
    assert set(records[0]) == {"tag", "chunk_id", "ticker", "fiscal_year", "section", "supported_claim"}


def _run_answer_loop(state, monkeypatch, synthesized, repaired):
    """synthesizer -> guardrail -> [repair -> guardrail]*, routed by the graph's own `route_after_guardrail`."""
    from src.system_c.graph import route_after_guardrail
    from src.system_c.nodes.repair import repair_node

    monkeypatch.setattr(
        "src.system_c.nodes.synthesizer.call_llm", lambda state, node_name, messages, **kw: (synthesized, state.get("telemetry", {}))
    )
    monkeypatch.setattr(
        "src.system_c.nodes.repair.call_llm", lambda state, node_name, messages, **kw: (repaired, state.get("telemetry", {}))
    )
    state.update(synthesizer_node(state))
    state.update(guardrail_node(state))
    while route_after_guardrail(state) == "repair":
        state.update(repair_node(state))
        state.update(guardrail_node(state))
    return state


@pytest.mark.parametrize(
    "synthesized, repaired, repairs",
    [
        ("Data Center revenue was up 68% [E1].", None, 0),  # passes first time; repair never runs
        ("Data Center revenue was up 68% [E3].", "Data Center revenue was up 68% [NVDA FY2026, Item 7, NVDA_FY2026_2026-01-25:205].", 1),
    ],
    ids=["no-repair", "repaired"],
)
def test_final_citations_match_final_answer_through_full_loop(monkeypatch, synthesized, repaired, repairs):
    final = _run_answer_loop(_state(), monkeypatch, synthesized, repaired)

    assert final["repair_count"] == repairs
    assert final["guardrail_passed"] is True
    assert final["final_answer"] == f"Data Center revenue was up 68% {TAG_205}."
    assert final["citations"] == build_citation_records(final["final_answer"], EVIDENCE)
    assert [(c["tag"], c["chunk_id"]) for c in final["citations"]] == [(TAG_205, MDA_205["chunk_id"])]
    # The wrong chunk cited before repair (68% isn't in the risk chunk) is gone, and no warning text leaks in
    assert all(c["chunk_id"] != RISK_57["chunk_id"] for c in final["citations"])
    assert all("Guardrail" not in c["supported_claim"] for c in final["citations"])


def test_synthesizer_node_expands_labels_end_to_end(monkeypatch):
    seen = {}

    def fake_call_llm(state, node_name, messages, **kw):
        seen["system"], seen["user"] = messages[0]["content"], messages[-1]["content"]
        return (
            "Data Center revenue was up 68% in FY2026 after rising 142% in FY2025 `[E1, E2]`. "
            "Total FY2026 revenue was $215,938 million [E4]. "
            "Revenue from Antarctica is not disclosed in the filing.",
            state.get("telemetry", {}),
        )

    monkeypatch.setattr("src.system_c.nodes.synthesizer.call_llm", fake_call_llm)
    out = synthesizer_node(_state())

    assert set(out) == {"draft_answer", "final_answer", "citations", "telemetry"}
    assert "[E1] NVDA FY2026 | Item 7. Management's" in seen["user"]
    assert "[E4] NVDA FY2026 | SEC XBRL reported financials | F-NVDA-2026" in seen["user"]
    assert "not a nearby block on the same topic" in seen["system"]
    assert out["draft_answer"] == out["final_answer"]
    assert "[E" not in out["draft_answer"] and "`" not in out["draft_answer"]
    assert f"FY2025 {TAG_205} {TAG_213}." in out["draft_answer"]
    assert "[F-NVDA-2026]" in out["draft_answer"]
    assert [c["chunk_id"] for c in out["citations"]] == [MDA_205["chunk_id"], MDA_213["chunk_id"], "F-NVDA-2026"]

    # And the expanded answer passes the guardrail as-is (no repair needed)
    state = _state(out["draft_answer"])
    audit = guardrail_node(state)
    assert audit["guardrail_report"]["invalid_citations"] == []
    assert audit["guardrail_report"]["ungrounded_numbers"] == []
    assert audit["guardrail_passed"] is True
