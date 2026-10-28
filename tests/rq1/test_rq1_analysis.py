"""
RQ1 Stage 3 (no network): paired tests, multiple-comparison correction, budget recall, matcher variants and the
failure-overlap bookkeeping.
"""

import pytest

from scripts.rq1.analysis import (
    BUDGET_METRIC, failure_overlap, holm, mcnemar_exact, paired_tests, recall_at_chars, sign_flip_p,
)
from scripts.rq1.matching import evidence_in_contexts


def test_mcnemar_exact_matches_the_binomial_tail():
    assert mcnemar_exact(0, 0) == 1.0
    assert mcnemar_exact(5, 5) == 1.0  # perfectly balanced discordance
    assert mcnemar_exact(10, 0) == pytest.approx(2 / 2 ** 10)  # one side wins every discordant question
    assert mcnemar_exact(2, 8) == mcnemar_exact(8, 2)  # symmetric


def test_holm_is_monotone_capped_and_keeps_input_order():
    adj = holm([0.04, 0.01, 0.03])
    assert adj == pytest.approx([0.06, 0.03, 0.06])  # sorted 0.01*3, max(0.03*2, .03), max(0.04*1, .06)
    assert holm([0.5, 0.9]) == pytest.approx([1.0, 1.0])
    assert all(a >= p for a, p in zip(adj, [0.04, 0.01, 0.03]))


def test_sign_flip_p_separates_a_consistent_gain_from_noise():
    assert sign_flip_p([0.0] * 20) == 1.0
    assert sign_flip_p([0.3] * 20, n_perm=2000) < 0.01
    noise = [0.2, -0.2] * 10
    assert sign_flip_p(noise, n_perm=2000) > 0.5
    assert sign_flip_p(noise, n_perm=500, seed=1) == sign_flip_p(noise, n_perm=500, seed=1)  # seeded


def _rows(system, values, metric="context_recall"):
    return [{"system": system, "question_id": f"q{i}", metric: v} for i, v in enumerate(values)]


def test_paired_tests_orient_differences_and_adjust_p_values():
    rows = _rows("system_a", [0.0] * 12) + _rows("system_b", [1.0] * 12)
    tests = paired_tests(rows, systems=["system_a", "system_b"], metrics=["context_recall"])
    (t,) = tests
    assert (t["system_x"], t["system_y"]) == ("system_b", "system_a")
    assert t["mean_diff"] == 1.0 and (t["x_better"], t["y_better"]) == (12, 0)
    assert t["p_holm"] >= t["p"] and t["p_holm_metric"] >= t["p"]
    assert t["test"] == "sign_flip_permutation"


def test_paired_tests_use_mcnemar_for_the_binary_metric():
    rows = _rows("system_a", [0.0] * 10, "complete@all") + _rows("system_b", [1.0] * 10, "complete@all")
    (t,) = paired_tests(rows, systems=["system_a", "system_b"], metrics=["complete@all"])
    assert t["test"] == "mcnemar_exact" and t["p"] == pytest.approx(2 / 2 ** 10)


def test_recall_at_chars_only_counts_chunks_inside_the_budget():
    rel = [[False, True, False], [False, False, True]]  # evidence 0 at chunk 2, evidence 1 at chunk 3
    contexts = ["a" * 100, "b" * 100, "c" * 100]
    assert recall_at_chars(rel, contexts, 99) == 0.0  # not even the first chunk fits
    assert recall_at_chars(rel, contexts, 200) == 0.5
    assert recall_at_chars(rel, contexts, 300) == 1.0
    assert BUDGET_METRIC == "recall@4000chars"


def test_require_numbers_rejects_a_chunk_that_reuses_the_words_but_not_the_figures():
    quote = {"quote": "Net sales decreased during 2025 compared to 2024 primarily due to net sales"}
    chunk = "Net sales increased during 2020 compared to 2019 primarily due to higher net sales of Accessories"
    assert evidence_in_contexts(quote, [chunk])  # 65% of the words overlap
    assert not evidence_in_contexts(quote, [chunk], require_numbers=True)
    assert not evidence_in_contexts(quote, [chunk], word_overlap=None)  # no 6-word phrase in common


def test_failure_overlap_counts_lost_shared_and_sole_solves():
    rows = []
    for qid, solved_by in {"q1": {"a", "b"}, "q2": {"b"}, "q3": set()}.items():
        for s in ("a", "b"):
            rows.append({"system": s, "question_id": qid, "complete@all": float(s in solved_by)})
    out = failure_overlap(rows, ["a", "b"])
    assert out["none"] == ["q3"] and out["any"] == 2 and out["all"] == 1
    assert out["sole"] == {"a": 0, "b": 1}


def test_group_diff_p_detects_a_difference_between_groups_and_not_between_equals():
    from scripts.rq1.analysis import group_diff_p
    assert group_diff_p([0.0] * 15, [0.5] * 15, n_perm=2000) < 0.01
    assert group_diff_p([0.1, 0.3] * 8, [0.3, 0.1] * 8, n_perm=2000) == 1.0  # identical groups: the observed gap (0) is never beaten


def test_by_question_type_scoreboard_and_interaction():
    from scripts.rq1.analysis import by_question_type
    rows = []
    for i in range(8):
        facets = {"recipe": "table" if i < 4 else "text", "modality": "table" if i < 4 else "text",
                  "scope": "single_doc", "hop": "multi", "evidence_count": "1", "section_spread": "1 item"}
        for system, score in (("system_a", 0.0), ("system_b", 0.5 if i < 4 else 1.0)):
            rows.append({"system": system, "question_id": f"q{i}", "complete@all": score, "recall@4000chars": score,
                         **facets})
    out = by_question_type(rows, ["system_a", "system_b"])
    table = next(c for c in out["cells"] if c["facet"] == "modality" and c["group"] == "table"
                 and c["metric"] == "complete@all")
    assert table["n"] == 4 and table["mean_system_b"] == 0.5 and table["mean_system_a"] == 0.0
    text_vs_table = next(i for i in out["interactions"] if i["contrast"] == "text vs table"
                         and i["metric"] == "complete@all" and (i["system_x"], i["system_y"]) == ("system_b", "system_a"))
    assert text_vs_table["difference_in_differences"] == pytest.approx(0.5)
