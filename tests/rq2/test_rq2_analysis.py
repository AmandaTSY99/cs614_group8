"""
RQ2 analysis on fixed data: primary accuracy, Holm-corrected paired comparisons and the ordering test,
rule-based error types and the citation sensitivity rows.
"""

import pytest

pytest.importorskip("scipy")

import numpy as np  # noqa: E402

from scripts.rq2 import analysis as A  # noqa: E402
from scripts.rq2 import report as R  # noqa: E402


def _row(system, qid, metric, value, status="ok", dims=None, detail="", category="quantitative_tabular"):
    return {"system": system, "question_id": qid, "category": category, "dims": dims or {"hop": "multi"},
            "metric": metric, "value": value, "status": status, "judge": "none", "detail": detail}


def test_holm_matches_hand_calculation():
    assert A.holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])
    assert A.holm([0.5]) == [0.5]
    assert A.holm([0.2, 0.9, 0.001]) == pytest.approx([0.4, 0.9, 0.003])


def test_paired_bootstrap_is_deterministic_and_brackets_the_mean():
    diffs = np.array([0.1, 0.3, -0.1, 0.2, 0.4, 0.0, 0.2, 0.1])
    first, second = A.paired_bootstrap(diffs), A.paired_bootstrap(diffs)
    assert first == second
    assert first[0] <= diffs.mean() <= first[1]


def test_paired_comparison_significant_and_not():
    scores = []
    for i in range(12):
        qid = f"q{i}"
        scores += [_row("system_a", qid, "m", 0.0), _row("system_b", qid, "m", 1.0),
                   _row("system_a", qid, "same", 0.5), _row("system_b", qid, "same", 0.5)]
    comps = {(c["metric"], c["group"]): c for c in A.paired_comparisons(scores)}
    big = comps[("m", "overall")]
    assert (big["system_a"], big["system_b"], big["n"]) == ("system_a", "system_b", 12)
    assert big["mean_diff"] == pytest.approx(1.0) and big["ci_low"] == pytest.approx(1.0)
    assert big["p_wilcoxon"] < 0.001 and big["p_holm"] < 0.05 and big["significant"]
    same = comps[("same", "overall")]
    assert same["mean_diff"] == 0.0 and same["p_wilcoxon"] == 1.0 and not same["significant"]
    assert ("m", "hop=multi") in comps and ("m", "category=quantitative_tabular") in comps


def test_paired_comparison_uses_only_questions_both_systems_have():
    scores = [_row("system_a", f"q{i}", "m", 0.0) for i in range(6)]
    scores += [_row("system_b", f"q{i}", "m", 1.0) for i in range(3, 9)]
    comps = A.paired_comparisons(scores)
    assert {c["n"] for c in comps} == {3} and "overall" in {c["group"] for c in comps}


def _four_systems(values):
    scores = []
    for i in range(12):
        for system, v in zip(A.SYSTEM_ORDER, values):
            scores.append(_row(system, f"q{i}", "primary_accuracy", v))
    return scores


def test_ordering_test_holds_and_reports_the_six_pairs():
    result = A.ordering_test(A.paired_comparisons(_four_systems([0.1, 0.3, 0.5, 0.7])))
    assert len(result["rows"]) == 6
    assert result["ordering_holds"]
    assert all(r["verdict"] == "as expected (significant)" for r in result["rows"])
    assert result["order"] == A.SYSTEM_ORDER


def test_ordering_test_flags_the_opposite_direction_and_ties():
    opposite = A.ordering_test(A.paired_comparisons(_four_systems([0.5, 0.3, 0.7, 0.9])))
    verdicts = {(r["system_a"], r["system_b"]): r["verdict"] for r in opposite["rows"]}
    assert verdicts[("system_a", "system_b")] == "OPPOSITE (significant)"
    assert not opposite["ordering_holds"]
    tied = A.ordering_test(A.paired_comparisons(_four_systems([0.5, 0.5, 0.5, 0.5])))
    assert all(r["verdict"] == "not significant" for r in tied["rows"]) and not tied["ordering_holds"]


def test_primary_accuracy_uses_numeric_accuracy_or_saved_keypoint_recall():
    scores = [_row("system_a", "n1", "numeric_accuracy", 1.0), _row("system_a", "n2", "numeric_accuracy", None, "na"),
              _row("system_a", "m1", "numeric_accuracy", 0.0), _row("system_a", "m1", "abstained", 0.0),
              _row("system_a", "q1", "abstained", 0.0), _row("system_a", "q2", "abstained", 0.0)]
    records = [
        {"system": "system_a", "question_id": "n1", "type": "numeric", "keypoint_recall": None},
        {"system": "system_a", "question_id": "n2", "type": "numeric", "keypoint_recall": None},
        {"system": "system_a", "question_id": "m1", "type": "mixed", "keypoint_recall": 0.67},
        {"system": "system_a", "question_id": "q1", "type": "qualitative", "keypoint_recall": 0.5},
        {"system": "system_a", "question_id": "q2", "type": "qualitative", "keypoint_recall": None},
    ]
    rows = {r["question_id"]: r for r in A.primary_accuracy_rows(records, scores)}
    assert rows["n1"]["value"] == 1.0 and rows["n1"]["detail"] == "numeric_accuracy"
    assert rows["n2"]["value"] is None and rows["n2"]["status"] == "na"
    assert rows["m1"]["value"] == 0.67 and rows["m1"]["detail"] == "keypoint_recall"  # mixed: key points, not the number
    assert rows["q1"]["value"] == 0.5
    assert rows["q2"]["status"] == "na"


@pytest.mark.parametrize("kwargs, expected", [
    (dict(abstained=True, numeric_accuracy=0.0, primary=0.0, is_numeric_type=True, context_recall=0.0, faithfulness=0.0), "refusal"),
    (dict(abstained=False, numeric_accuracy=0.0, primary=0.0, is_numeric_type=True, context_recall=0.2, faithfulness=0.0), "retrieval_miss"),
    (dict(abstained=False, numeric_accuracy=0.0, primary=0.0, is_numeric_type=True, context_recall=0.8, faithfulness=0.0), "wrong_number"),
    (dict(abstained=False, numeric_accuracy=None, primary=0.3, is_numeric_type=False, context_recall=0.8, faithfulness=0.4), "unsupported_claim"),
    (dict(abstained=False, numeric_accuracy=None, primary=0.3, is_numeric_type=False, context_recall=0.8, faithfulness=0.9), "incomplete"),
    (dict(abstained=False, numeric_accuracy=1.0, primary=1.0, is_numeric_type=True, context_recall=0.0, faithfulness=0.0), None),
    (dict(abstained=False, numeric_accuracy=None, primary=0.5, is_numeric_type=False, context_recall=0.0, faithfulness=0.0), None),
    (dict(abstained=False, numeric_accuracy=0.0, primary=0.6, is_numeric_type=False, context_recall=0.9, faithfulness=0.9), None),
])
def test_classify_error_priority_order(kwargs, expected):
    assert A.classify_error(**kwargs) == expected


def test_error_type_rows_and_counts_per_system_and_attribute():
    def rec(system, qid, qtype, kp=None):
        return {"system": system, "question_id": qid, "type": qtype, "keypoint_recall": kp}

    records = [rec("system_a", "n1", "numeric"), rec("system_a", "n2", "numeric"), rec("system_a", "q1", "qualitative", 0.2),
               rec("system_a", "q2", "qualitative", 1.0)]
    scores = []
    for qid, numacc, abst, cr, fa in [("n1", 0.0, 1.0, 0.0, None), ("n2", 0.0, 0.0, 0.9, 0.9), ("q1", None, 0.0, 0.9, 0.2),
                                      ("q2", None, 0.0, 0.9, 0.9)]:
        scores += [_row("system_a", qid, "abstained", abst), _row("system_a", qid, "context_recall", cr)]
        scores.append(_row("system_a", qid, "numeric_accuracy", numacc, "ok" if numacc is not None else "na"))
        scores.append(_row("system_a", qid, "faithfulness", fa, "ok" if fa is not None else "na"))
    primary = A.primary_accuracy_rows(records, scores)
    rows = A.error_type_rows(records, scores, primary)
    assert {r["question_id"]: r["error_type"] for r in rows} == {
        "n1": "refusal", "n2": "wrong_number", "q1": "unsupported_claim", "q2": None}
    overall = next(c for c in A.error_type_counts(rows) if c["group"] == "overall")
    assert (overall["answers"], overall["wrong"]) == (4, 3)
    assert overall["refusal"] == overall["wrong_number"] == overall["unsupported_claim"] == 1
    assert overall["incomplete"] == 0 and overall["refusal_share"] == pytest.approx(1 / 3)
    assert any(c["group"] == "hop=multi" for c in A.error_type_counts(rows))


def test_citation_sensitivity_counts_uncited_answers_as_zero():
    scores = [
        _row("system_a", "q1", "citation_precision", 1.0),
        _row("system_a", "q2", "citation_precision", None, "na", detail="no citations"),
        _row("system_a", "q3", "citation_precision", None, "na", detail="no gold sections"),
        _row("system_a", "q2", "citation_coverage", 0.0),
    ]
    rows = {r["question_id"]: r for r in A.citation_sensitivity_rows(scores)}
    assert set(r["metric"] for r in rows.values()) == {"citation_precision_incl_uncited"}
    assert rows["q1"]["value"] == 1.0
    assert rows["q2"]["value"] == 0.0 and rows["q2"]["status"] == "ok"
    assert rows["q3"]["status"] == "na"  # no gold section: still N/A, not 0
    assert len(rows) == 3  # coverage is not duplicated

    agg = {(a["system"], a["category"], a["metric"]): a
           for a in R.aggregate(scores + list(rows.values()))}
    assert agg[("system_a", "overall", "citation_precision")]["mean"] == 1.0  # citing answers only
    assert agg[("system_a", "overall", "citation_precision_incl_uncited")]["mean"] == 0.5
