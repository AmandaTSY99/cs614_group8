"""
Case studies (no network): answer-score summary by question type, deterministic case selection, and the loud
cross-check of chunk-level gold labels against RQ1's evidence_scores.csv.
"""

import pytest

from scripts.case_studies.build_casebook import answer_score, chunk_labels, select_cases
from scripts.rq1.common import SYSTEMS

QUOTE = "Total net revenue increased to 1,534 million driven by strong Tegra processor demand"


def _q(qid="gold-900", qtype="mixed", recipe="table", hop="single"):
    return {"id": qid, "type": qtype, "recipe": recipe, "hop": hop,
            "gold_evidence": [{"kind": "table", "item": "Item 7. MD&A", "quote": QUOTE}]}


def test_answer_score_uses_metrics_by_question_type():
    rec = {"numeric_correct": True, "keypoint_recall": 0.5}
    assert answer_score(_q(qtype="numeric"), rec) == 1.0
    assert answer_score(_q(qtype="qualitative"), rec) == 0.5
    assert answer_score(_q(qtype="mixed"), rec) == 0.75
    assert answer_score(_q(qtype="numeric"), {"numeric_correct": None}) is None


def test_chunk_labels_match_rq1_or_fail():
    rec = {"system": "system_a", "retrieved_contexts": ["unrelated text here", QUOTE + " in fiscal 2018"]}
    assert chunk_labels(_q(), rec, {("system_a", "gold-900", 0): "2"}) == [[], [0]]
    with pytest.raises(ValueError, match="mismatch"):
        chunk_labels(_q(), rec, {("system_a", "gold-900", 0): "1"})


def test_select_cases_picks_contrast_then_hardest():
    bench = {qid: _q(qid) for qid in ("gold-901", "gold-902", "gold-903")}
    per_q = {"gold-901": [1, 1, 1, 1], "gold-902": [0, 1, 0, 1], "gold-903": [0, 0, 0, 0]}
    scores = {qid: {s: {"answer_score": float(v), "recall@all": 1.0} for s, v in zip(SYSTEMS, vals)}
              for qid, vals in per_q.items()}
    picked = select_cases(bench, scores, per_type=2)
    assert [(qid, reason) for _, qid, reason in picked] == [("gold-902", "contrast"), ("gold-903", "hardest")]
