"""
RQ2 custom metrics (pure Python, no LLM): section normalisation, citation P/R/F1 and coverage,
numeric answer accuracy with scale matching, grounding error rate. Runs in both `cs614` and `cs614-eval`.
"""

import pytest

from scripts.rq2.metrics_custom import (
    citation_prf, cited_sections, custom_scores, gold_sections, grounding_error, normalise_section,
    numeric_accuracy, strip_citation_tags,
)


def _cite(chunk_id, ticker, section, fy=2024):
    return {"tag": f"[{chunk_id}]", "chunk_id": chunk_id, "ticker": ticker, "fiscal_year": fy, "section": section}


def test_normalise_section_variants():
    assert normalise_section("Item 8 Financial Statements") == (None, "Item 8")
    assert normalise_section("Item 8 Note 19") == (None, "Item 8")
    assert normalise_section("Item 8 Note on Commitments and Contingencies") == (None, "Item 8")
    assert normalise_section("MSFT Item 8 Note 19") == ("MSFT", "Item 8")
    assert normalise_section("Item 7A") == (None, "Item 7A")
    assert normalise_section("Item 7. Management's Discussion and Analysis > Results") == (None, "Item 7")
    assert normalise_section("ITEM 1A. RISK FACTORS") == (None, "Item 1A")
    assert normalise_section("financials.csv") == (None, "XBRL")
    assert normalise_section("Exhibits") is None


def test_xbrl_citation_matches_financials_csv_gold():
    cites = [_cite("F-NVDA-2026", "NVDA", None, 2026)]
    assert cited_sections(cites) == [("NVDA", "XBRL")]
    prf = citation_prf(cites, ["financials.csv"])
    assert prf["status"] == "ok"
    assert prf["precision"] == prf["recall"] == prf["f1"] == 1.0


def test_citation_prf_values():
    cites = [
        _cite("NVDA_FY2026_x:1", "NVDA", "Item 7. MD&A"),
        _cite("NVDA_FY2026_x:2", "NVDA", "Item 7. MD&A > Liquidity"),  # same section counted once
        _cite("NVDA_FY2026_x:3", "NVDA", "Item 1A. Risk Factors"),
    ]
    prf = citation_prf(cites, ["Item 7", "Item 8 Financial Statements"])
    assert prf["precision"] == pytest.approx(0.5)  # Item 7 correct, Item 1A not
    assert prf["recall"] == pytest.approx(0.5)  # Item 7 cited, Item 8 not
    assert prf["f1"] == pytest.approx(0.5)


def test_ticker_prefixed_gold_requires_same_company():
    gold = ["MSFT Item 8 Note 19", "AMZN Item 8 Note 10"]
    assert gold_sections(gold) == [("MSFT", "Item 8"), ("AMZN", "Item 8")]
    cites = [_cite("MSFT_FY2024_x:1", "MSFT", "Item 8. Financial Statements"),
             _cite("GOOGL_FY2024_x:1", "GOOGL", "Item 8. Financial Statements")]
    prf = citation_prf(cites, gold)
    assert prf["precision"] == pytest.approx(0.5)  # GOOGL Item 8 is not a gold section
    assert prf["recall"] == pytest.approx(0.5)  # AMZN Item 8 not cited


def test_no_citations_is_na_and_coverage_zero():
    prf = citation_prf([], ["Item 7"])
    assert prf["status"] == "na" and prf["precision"] is None and prf["f1"] is None
    record = {"answer": "Revenue was $10 million.", "citations": [], "target_sections": ["Item 7"],
              "ground_truth_numbers": ["$10 million"], "guardrail_report": None}
    scores = custom_scores(record)
    assert scores["citation_f1"] == (None, "na", "no citations")
    assert scores["citation_coverage"][0] == 0.0
    assert scores["grounding_error_rate"][:2] == (None, "na")


def test_numeric_accuracy_scale_matching():
    answer = "Data Center revenue was $60.9 billion [NVDA FY2026, Item 7, NVDA_FY2026_x:1], up 142%."
    assert numeric_accuracy(answer, ["60,922 million", "142%"]) == 1.0
    assert numeric_accuracy(answer, ["60,922 million", "75%"]) == 0.5
    # Euro amounts and plain years
    assert numeric_accuracy("A €2.4 billion fine; commitments run through 2030.", ["€2.4 billion", "2030"]) == 1.0
    # Numbers inside citation tags never count
    assert numeric_accuracy("See filing [NVDA FY2026, Item 7, NVDA_FY2026_x:441].", ["441"]) == 0.0
    assert numeric_accuracy("anything", []) is None


def test_grounding_error_and_tag_stripping():
    assert grounding_error({"numerical_grounding_error_rate": 0.25}) == 0.25
    assert grounding_error(None) is None
    assert grounding_error({}) is None
    assert strip_citation_tags("Revenue rose [NVDA FY2026, Item 7, X:1] [F-NVDA-2026].") == "Revenue rose ."
