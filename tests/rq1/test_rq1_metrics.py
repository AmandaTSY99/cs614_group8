"""
RQ1 Stage 1 + 2 (no network): recall@k / completeness / average-precision arithmetic, question-type facets,
loud failures on unscoreable records, and the report aggregates.
"""

import json

import pytest

from scripts.rq1.common import load_records, question_facets
from scripts.rq1.matching import evidence_in_contexts, first_rank
from scripts.rq1.report import aggregate, build_report
from scripts.rq1.score import question_metrics, score

QUOTE_A = "Total net revenue increased to 1,534 million driven by strong Tegra processor demand"
QUOTE_B = "The Company recognized an impairment charge of 120 million related to goodwill"


def _question(qid="gold-900", kinds=("table", "text"), items=("Item 8", "Item 7")):
    return {
        "id": qid, "recipe": "table_text", "scope": "single_doc",
        "gold_evidence": [
            {"kind": k, "item": f"{it}. Something", "quote": q, "ticker": "NVDA", "year": 2018}
            for k, it, q in zip(kinds, items, (QUOTE_A, QUOTE_B))
        ],
    }


def _record(qid="gold-900", system="system_a", contexts=None):
    return {"system": system, "question_id": qid,
            "retrieved_contexts": contexts if contexts is not None else ["noise", QUOTE_B, "noise", QUOTE_A]}


def test_question_metrics_recall_completeness_and_average_precision():
    # evidence 0 at rank 4, evidence 1 at rank 2; chunks 1 and 3 irrelevant
    rel = [[False, False, False, True], [False, True, False, False]]
    m = question_metrics(rel, k_values=(2, 4))
    assert m["recall@2"] == 0.5 and m["complete@2"] == 0.0
    assert m["recall@4"] == 1.0 and m["complete@4"] == 1.0
    assert m["recall@all"] == 1.0 and m["complete@all"] == 1.0 and m["zero_recall"] == 0.0
    assert m["average_precision"] == pytest.approx((1 / 2 + 2 / 4) / 2)


def test_question_metrics_nothing_found():
    m = question_metrics([[False, False]], k_values=(1,))
    assert m["recall@all"] == 0.0 and m["zero_recall"] == 1.0 and m["average_precision"] == 0.0


def test_matching_and_first_rank():
    assert evidence_in_contexts({"quote": QUOTE_A}, ["prefix " + QUOTE_A.upper() + "!"])
    assert not evidence_in_contexts({"quote": QUOTE_A}, ["unrelated text"])
    assert first_rank([False, True, True]) == 2 and first_rank([False]) is None
    with pytest.raises(ValueError, match="empty quote"):
        evidence_in_contexts({"quote": "  "}, ["anything"])


def test_question_facets():
    f = question_facets(_question())
    assert f == {"recipe": "table_text", "modality": "table+text", "scope": "single_doc",
                 "evidence_count": "2", "section_spread": "2+ items"}
    assert question_facets(_question(kinds=("text", "text"), items=("Item 7", "Item 7")))["section_spread"] == "1 item"


def _write(tmp_path, questions, records):
    bench = tmp_path / "bench.json"
    bench.write_text(json.dumps(questions), encoding="utf-8")
    recs = tmp_path / "records.jsonl"
    recs.write_text("".join(json.dumps(r) + "\n" for r in records), encoding="utf-8")
    return bench, recs


def test_load_records_fails_loudly(tmp_path):
    _, recs = _write(tmp_path, [], [_record(contexts=[])])
    with pytest.raises(ValueError, match="missing 'retrieved_contexts'"):
        load_records(recs)
    _, recs = _write(tmp_path, [], [_record(), _record()])
    with pytest.raises(ValueError, match="Duplicate record"):
        load_records(recs)


def test_unknown_question_id_fails_loudly(tmp_path):
    bench, recs = _write(tmp_path, [_question()], [_record(qid="gold-999")])
    with pytest.raises(ValueError, match="not in"):
        score(bench, recs, tmp_path / "out")


def test_score_and_report_end_to_end(tmp_path):
    bench, recs = _write(tmp_path, [_question()], [
        _record(system="system_a"),
        _record(system="system_b", contexts=[QUOTE_A, "noise"]),
    ])
    out = tmp_path / "out"
    q_rows, e_rows = score(bench, recs, out)
    assert {(r["system"], r["recall@all"]) for r in q_rows} == {("system_a", 1.0), ("system_b", 0.5)}
    assert len(e_rows) == 4
    text = build_report(out)
    assert "## By question type" in text and "## By evidence modality" in text
    assert (out / "aggregate.csv").exists() and (out / "report.md").exists()


def test_aggregate_groups_overall_and_facets():
    rows = [{"system": "system_a", "recipe": "text", "m": 1.0},
            {"system": "system_a", "recipe": "table", "m": 0.0}]
    agg = {(a["facet"], a["group"]): a for a in aggregate(rows, ["m"], ["recipe"], "question")}
    assert agg[("overall", "all")]["mean"] == 0.5 and agg[("overall", "all")]["n"] == 2
    assert agg[("recipe", "text")]["mean"] == 1.0
