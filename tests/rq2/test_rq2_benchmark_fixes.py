"""
RQ2 scoring on the 97-question benchmark: refusals, RAGAS references from gold evidence, unsigned
percentage decreases, corrected categories and the proposal's question dimensions.
"""

import asyncio

import pytest

pytest.importorskip("ragas")

from scripts.rq2 import judge as J  # noqa: E402
from scripts.rq2 import report as R  # noqa: E402
from scripts.rq2 import score as S  # noqa: E402
from scripts.rq2.common import RECORDS_FILE, SCORES_FILE, _derive_category, append_jsonl, question_dimensions, ragas_reference, read_jsonl  # noqa: E402
from scripts.rq2.metrics_custom import is_abstention, numeric_accuracy  # noqa: E402

BENCH_Q = {
    "id": "gold-011", "question": "What is the percentage decrease in MSFT amortization from 2017 to 2020?",
    "answer": "-30.36%", "type": "numeric", "recipe": "cross_year_table", "hop": "multi", "scope": "cross_year",
    "program": "subtract(7038, 10106), divide(#0, 10106), multiply(#1, 100)", "key_points": [],
    "gold_evidence": [{"doc_id": "MSFT_FY2020", "ticker": "MSFT", "year": 2020, "item": "Item 8", "quote": "| Total | $7,038 |"},
                      {"doc_id": "MSFT_FY2017", "ticker": "MSFT", "year": 2017, "item": "Item 8", "quote": "| Total | $10,106 |"}],
}


class _Result:
    def __init__(self, value):
        self.value = value


class _FakeMetric:
    def __init__(self, value=0.8):
        self.value = value
        self.inputs = []

    async def ascore(self, **kwargs):
        self.inputs.append(kwargs)
        return _Result(self.value)


async def _no_sleep(_):
    return None


def _record(system, answer):
    return {
        "system": system, "question_id": "gold-011", "category": "multi_company_comparison",
        "question": BENCH_Q["question"], "answer": answer, "retrieved_contexts": ["| Total | $7,038 |"],
        "contexts_meta": [{"chunk_id": "c:1"}], "citations": [], "guardrail_report": None,
        "ground_truth_answer": "-30.36%", "ground_truth_numbers": ["-30.36%"], "target_sections": ["Item 8"],
    }


def test_unsigned_decrease_matches_negative_gold():
    assert numeric_accuracy("It decreased by approximately 25.6%.", ["-25.64%"]) == 1.0
    assert numeric_accuracy("a decrease of 30.36% of the 2017 amount", ["-30.36%"]) == 1.0
    assert numeric_accuracy("It decreased by 40%.", ["-25.64%"]) == 0.0


@pytest.mark.parametrize("answer, expected", [
    ("Not found in the provided context.", True),
    ("The filing excerpts provided do not disclose the expense, so the decrease cannot be determined.", True),
    ("Revenue was $10 million [1].", False),
])
def test_abstention_detection(answer, expected):
    assert is_abstention(answer) is expected


def test_cross_year_single_company_is_not_multi_company():
    assert _derive_category(BENCH_Q) == "cross_section_multihop"
    assert _derive_category({**BENCH_Q, "recipe": "cross_company_table", "scope": "cross_company"}) == "multi_company_comparison"


def test_question_dimensions_and_references():
    assert question_dimensions(BENCH_Q) == {"answer_type": "numerical", "evidence_format": "table", "hop": "multi",
                                            "task": "calculation", "evidence_scope": "cross_year"}
    ref = ragas_reference(BENCH_Q)
    assert ref["answer"] == "-30.36% (a decrease of 30.36%)"
    assert "| Total | $10,106 |" in ref["evidence"] and "Answer: -30.36%" in ref["evidence"]


def test_fc_reference_variants_keep_decrease_wording():
    q = {**BENCH_Q, "key_points": ["Amortization fell from $10,106 million to $7,038 million"]}
    ref = ragas_reference(q)
    assert ref["answer"] == "-30.36% (a decrease of 30.36%)"
    assert ref["answer_keypoints"] == "-30.36% (a decrease of 30.36%) Amortization fell from $10,106 million to $7,038 million."
    record = {"question": "Q?", "answer": "A decrease of 30.36%.", "ragas_reference": ref}
    assert S.metric_inputs("factual_correctness", record, "answer")["reference"] == ref["answer"]
    assert S.metric_inputs("factual_correctness", record, "answer_keypoints")["reference"] == ref["answer_keypoints"]
    for variant in ("answer", "answer_keypoints"):
        assert "(a decrease of 30.36%)" in S.metric_inputs("factual_correctness", record, variant)["reference"]


def test_fc_mode_passed_to_ragas_metric(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key-not-used")
    llm = J.build_judge("groq", J.DEFAULT_JUDGE_MODEL, J.JudgeMeter())
    assert S.make_metric("factual_correctness", llm).mode == "f1"
    assert S.make_metric("factual_correctness", llm, fc_mode="recall").mode == "recall"


@pytest.mark.parametrize("fc_mode, fc_reference", [("f1", "answer_keypoints"), ("recall", "answer"),
                                                   ("recall", "answer_keypoints")])
def test_fc_variant_recorded_in_detail(tmp_path, fc_mode, fc_reference):
    q = {**BENCH_Q, "key_points": ["Amortization fell"]}
    append_jsonl(tmp_path / RECORDS_FILE, _record("system_c_v3", "A decrease of 30.36%."))
    append_jsonl(tmp_path / RECORDS_FILE, _record("system_a", "Not found in the provided context."))
    fake = _FakeMetric(0.9)
    asyncio.run(S.score_run(
        tmp_path, ["factual_correctness"], metric_factory=lambda name, llm, emb: fake, llm=object(),
        embeddings=object(), meter=J.JudgeMeter(), sleep=_no_sleep, benchmark={"gold-011": q},
        fc_mode=fc_mode, fc_reference=fc_reference,
    ))
    rows = {r["system"]: r for r in read_jsonl(tmp_path / SCORES_FILE)}
    tag = f"fc_mode={fc_mode}; fc_reference={fc_reference}"
    assert rows["system_c_v3"]["detail"] == tag and rows["system_c_v3"]["value"] == 0.9
    assert rows["system_a"]["detail"].startswith(tag) and rows["system_a"]["value"] == 0.0
    expected_ref = ragas_reference(q)[fc_reference]
    assert fake.inputs[0]["reference"] == expected_ref


def test_score_run_defaults_are_current_behaviour():
    assert (S.DEFAULT_FC_MODE, S.DEFAULT_FC_REFERENCE) == ("f1", "answer_keypoints")
    with pytest.raises(ValueError):
        asyncio.run(S.score_run(None, [], fc_mode="precision"))


def test_refusals_and_references_in_scoring(tmp_path):
    append_jsonl(tmp_path / RECORDS_FILE, _record("system_a", "Not found in the provided context."))
    append_jsonl(tmp_path / RECORDS_FILE, _record("system_c_v3", "It fell from $10,106 to $7,038 million, a decrease of 30.36%."))
    fakes = {m: _FakeMetric(0.7) for m in ("faithfulness", "factual_correctness", "context_recall")}
    asyncio.run(S.score_run(
        tmp_path, ["faithfulness", "factual_correctness", "context_recall", "abstained", "numeric_accuracy"],
        metric_factory=lambda name, llm, emb: fakes[name], llm=object(), embeddings=object(),
        meter=J.JudgeMeter(), sleep=_no_sleep, benchmark={"gold-011": BENCH_Q},
    ))
    rows = {(r["system"], r["metric"]): r for r in read_jsonl(tmp_path / SCORES_FILE)}
    assert rows[("system_a", "faithfulness")]["status"] == "na"
    assert rows[("system_a", "factual_correctness")]["value"] == 0.0
    assert rows[("system_a", "abstained")]["value"] == 1.0
    assert rows[("system_c_v3", "abstained")]["value"] == 0.0
    assert rows[("system_c_v3", "numeric_accuracy")]["value"] == 1.0
    assert rows[("system_c_v3", "faithfulness")]["value"] == 0.7
    # Only the answering system reached the judge for faithfulness / factual correctness.
    assert len(fakes["faithfulness"].inputs) == 1 and len(fakes["factual_correctness"].inputs) == 1
    assert "$10,106" in fakes["context_recall"].inputs[0]["reference"]
    assert all(r["category"] == "cross_section_multihop" and r["dims"]["task"] == "calculation" for r in rows.values())

    agg = R.aggregate(read_jsonl(tmp_path / SCORES_FILE))
    groups = {a["category"] for a in agg}
    assert {"task=calculation", "evidence_scope=cross_year", "answer_type=numerical"} <= groups
