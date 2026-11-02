"""
Refusals vs retrieved gold evidence, retrieval context per system, and numeric accuracy vs the saved flags,
on fixed data.
"""

import pytest

pytest.importorskip("scipy")

from scripts.rq2 import analysis as A  # noqa: E402
from scripts.rq2 import retrieval_stats as RS  # noqa: E402

QUOTE_1 = "| Total | $7,038 |"
QUOTE_2 = "| Total | $10,106 |"
BENCH = {"q1": {"gold_evidence": [
    {"doc_id": "MSFT_FY2020", "quote": QUOTE_1}, {"doc_id": "MSFT_FY2017", "quote": QUOTE_2}]}}


def _rec(system, answer, chunks, hops=1, qid="q1", **extra):
    return {"system": system, "question_id": qid, "answer": answer, "hops": hops,
            "retrieved_contexts": [c for _, c in chunks],
            "contexts_meta": [{"chunk_id": f"{doc}:{i}"} for i, (doc, _) in enumerate(chunks)], **extra}


def test_quote_must_be_in_a_chunk_of_the_gold_filing():
    rec = _rec("system_a", "x", [("MSFT_FY2020", "Intangibles\n| Total | $7,038 |"), ("OTHER_FY2020", QUOTE_2)])
    assert RS.quote_in_contexts({"doc_id": "MSFT_FY2020", "quote": QUOTE_1}, rec)
    assert not RS.quote_in_contexts({"doc_id": "MSFT_FY2017", "quote": QUOTE_2}, rec)  # right text, wrong filing
    assert RS.evidence_coverage(rec, BENCH["q1"]) == 0.5


def test_lenient_matching_accepts_a_partly_matching_short_quote_but_strict_does_not():
    ev = {"doc_id": "D", "quote": "The company recognised revenue over the service period"}
    rec = _rec("system_a", "x", [("D", "revenue is recognised by the company across the service period")])
    assert not RS.quote_in_contexts(ev, rec)
    assert RS.quote_in_contexts(ev, rec, lenient=True)


def test_refusals_are_split_by_how_much_gold_evidence_was_retrieved():
    both = [("MSFT_FY2020", QUOTE_1), ("MSFT_FY2017", QUOTE_2)]
    recs = [_rec("system_b", "Not found in the provided context.", [("MSFT_FY2020", QUOTE_1)], qid="q1"),
            _rec("system_b", "It fell 30.36%.", both, qid="q1b"),
            _rec("system_b", "Not found in the provided context.", [("X", "unrelated")], qid="q1c"),
            _rec("system_b", "Not found in the provided context.", both, qid="q1d")]
    bench = {"q1": BENCH["q1"], "q1b": BENCH["q1"], "q1c": BENCH["q1"], "q1d": BENCH["q1"]}
    (row,) = RS.refusal_retrieval(recs, bench)
    assert (row["refusals"], row["refusals_full_evidence"], row["refusals_partial_evidence"],
            row["refusals_no_evidence"]) == (3, 1, 1, 1)
    assert (row["answered"], row["answered_full_evidence"]) == (1, 1)


def test_retrieval_context_stats_chunks_and_hops():
    recs = [_rec("system_c_v3", "a", [("D", "xx"), ("D", "yyyy")], hops=1),
            _rec("system_c_v3", "b", [("D", "z")] * 4, hops=3, qid="q2")]
    (row,) = RS.retrieval_context_stats(recs)
    assert (row["mean_chunks"], row["mean_context_chars"], row["mean_hops"]) == (3.0, 5.0, 2.0)
    assert (row["hops_1"], row["hops_2"], row["hops_3"]) == (1, 0, 1)


def test_numeric_agreement_counts_and_lists_disagreements():
    def score(system, qid, value):
        return {"system": system, "question_id": qid, "metric": "numeric_accuracy", "value": value,
                "status": "ok" if value is not None else "na"}

    recs = [{"system": "system_a", "question_id": "n1", "numeric_correct": True, "ground_truth_numbers": ["1"], "answer": "1"},
            {"system": "system_a", "question_id": "n2", "numeric_correct": True, "ground_truth_numbers": ["2"], "answer": "about 3"},
            {"system": "system_a", "question_id": "n3", "numeric_correct": False, "ground_truth_numbers": ["3"], "answer": "x"},
            {"system": "system_a", "question_id": "q1", "numeric_correct": None, "ground_truth_numbers": [], "answer": "y"}]
    scores = [score("system_a", "n1", 1.0), score("system_a", "n2", 0.0), score("system_a", "n3", 0.0),
              score("system_a", "q1", None)]
    result = A.numeric_agreement(recs, scores)
    assert (result["agree"], result["total"]) == (2, 3)
    assert [d["question_id"] for d in result["disagreements"]] == ["n2"]
    assert result["per_system"] == {"system_a": (2, 3)}
