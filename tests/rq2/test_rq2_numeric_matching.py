"""
Numeric accuracy: accounting negatives, a bare table figure against a gold value with a unit, and ratio / percentage
equivalents, using the cases found in an independent check of the 97-question benchmark.
"""

import pytest

from scripts.rq2.metrics_custom import numeric_accuracy


def test_gold_048_accounting_negative_matches_negative_gold():
    answer = ("For 2023, the Foreign-derived intangible income deduction was (4.6) percentage points and the Effect "
              "of tax law change was (1.4) percentage points, for a combined impact of (6.0) percentage points on "
              "Alphabet’s effective income tax rate. [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:468]")
    assert numeric_accuracy(answer, ["-6.0 percentage points"]) == 1.0
    assert numeric_accuracy("a decline of $(316) in the year", ["-316"]) == 1.0  # "$(316)" is -316
    assert numeric_accuracy("a combined impact of (7.0) percentage points", ["-6.0 percentage points"]) == 0.0


def test_gold_033_bare_table_figure_matches_gold_with_unit():
    answer = ("the net carrying amount of “Patents and developed technology” decreased from $990 as of December 31, "
              "2020 to $674 as of December 31, 2021, a decline of $316.00 [GOOGL FY2021, Item 8, GOOGL_FY2021:414]")
    assert numeric_accuracy(answer, ["$316 million"]) == 1.0
    assert numeric_accuracy("a decline of $316", ["$316 million"]) == 1.0


@pytest.mark.parametrize("answer, gold", [
    ("a decline of $316 billion", "$316 million"),     # another magnitude stated
    ("a decline of $317", "$316 million"),             # digits differ
    ("a decline of $95", "$95 million"),               # fewer than 3 significant digits
    ("a decline of 316%", "$316 million"),             # a percentage
])
def test_bare_figure_needs_exact_digits_at_least_three_significant_and_no_other_unit(answer, gold):
    assert numeric_accuracy(answer, [gold]) == 0.0


def test_gold_004_percentage_matches_ratio_gold_and_back():
    answer = ("Apple Inc.'s interest expense was $(3,576) and its interest and dividend income was $4,961 in fiscal "
              "year 2019, so the ratio of interest expense to interest and dividend income was 72.08% (3,576 ÷ 4,961). "
              "[AAPL FY2019, Item 8, AAPL_FY2019_2019-09-28:242]")
    assert numeric_accuracy(answer, ["0.72"]) == 1.0
    assert numeric_accuracy("the ratio was 0.72", ["72%"]) == 1.0
    assert numeric_accuracy("the ratio was 0.7208", ["72%"]) == 1.0


@pytest.mark.parametrize("answer, gold", [
    ("the ratio was 75%", "0.72"),
    ("the ratio was 0.75", "72%"),
    ("the ratio was 72 million", "0.72"),
])
def test_ratio_percentage_equivalence_uses_the_existing_tolerance(answer, gold):
    assert numeric_accuracy(answer, [gold]) == 0.0


def test_existing_matching_is_unchanged():
    assert numeric_accuracy("It decreased by approximately 25.6%.", ["-25.64%"]) == 1.0
    assert numeric_accuracy("revenue was $60.9 billion", ["60,922 million"]) == 1.0
    assert numeric_accuracy("It decreased by 40%.", ["-25.64%"]) == 0.0
    assert numeric_accuracy("no figures here", []) is None
