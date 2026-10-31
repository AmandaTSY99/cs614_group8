# Case studies: individual QAs across the four systems

A per-question view of the shared 97-question × 4-system run, for examples in the report and slides. It is **separate from RQ1–RQ3**: it runs nothing new and adds no new scores; every number on these pages is read from the RQ1, RQ2 and RQ3 outputs listed below, and every answer and chunk is the system's own generated output.

Built by `scripts/case_studies/build_casebook.py` from:

- gold QAs: `data/benchmark_qa_pool_2015.json`
- answers, retrieved contexts, citations, guardrail, tokens/cost/latency: `reports/rq3/records.jsonl` (identical answers to `reports/rq2/full/records.jsonl`)
- retrieval metrics: `reports/rq1/question_scores.csv`, `reports/rq1/evidence_scores.csv`
- citation / numeric / grounding metrics: `reports/rq2/full/scores.jsonl` (judge: none, custom metrics only)

Every question has a page in [`cases/`](cases/); per-(question, system) numbers are in [`case_metrics.csv`](case_metrics.csv).

## Question types

The benchmark's (recipe, hop) cells give nine question types:

| Type | recipe | hop | questions |
|---|---|---|---|
| Single-hop text | `text` | `single` | 8 |
| Multi-hop text (one filing) | `text` | `multi` | 7 |
| Single-hop table | `table` | `single` | 11 |
| Multi-hop table (one filing) | `table` | `multi` | 9 |
| Table + text (one filing) | `table_text` | `multi` | 20 |
| Cross-year text | `cross_year_text` | `multi` | 14 |
| Cross-year table | `cross_year_table` | `multi` | 19 |
| Cross-company text | `cross_company_text` | `multi` | 5 |
| Cross-company table | `cross_company_table` | `multi` | 4 |

## Selected cases

Two per type, picked by a fixed rule (not by hand):

- **contrast**: the question whose answer score differs most across the four systems (ties → larger spread in RQ1 recall@all, then question id). Shows where the architectures diverge.
- **hardest**: the question with the lowest mean answer score across systems (ties → lower mean recall@all, then id). Shows shared failures.

*Answer score* (used only for this selection): RQ3's `numeric_correct` for numeric questions, `keypoint_recall` for qualitative ones, their mean for mixed ones. Both are string-match checks, so read the answers on each page before calling an answer right or wrong.

Cells below: answer score / RQ1 recall@all.

| Type | Case | Pick | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) | Question |
|---|---|---|---|---|---|---|---|
| Single-hop text | [gold-022](cases/gold-022.md) | contrast | 0.00 / 0.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | According to Microsoft's fiscal year 2019 10-K, what valuation methodology does the company use for its Level 3 investments? |
| Single-hop text | [gold-055](cases/gold-055.md) | hardest | 0.67 / 1.00 | 0.67 / 1.00 | 0.67 / 1.00 | 0.67 / 1.00 | For Tesla's Powerwall 2 systems sold in fiscal year 2017, what specific energy retention standard is guaranteed under the standard warranty … |
| Multi-hop text (one filing) | [gold-019](cases/gold-019.md) | contrast | 1.00 / 1.00 | 0.67 / 0.50 | 1.00 / 1.00 | 1.00 / 1.00 | How did Meta Platforms' accounting policy for share-based compensation forfeitures change in Q4 2016, and how does this interact with the st… |
| Multi-hop text (one filing) | [gold-023](cases/gold-023.md) | hardest | 1.00 / 1.00 | 1.00 / 1.00 | 0.67 / 1.00 | 0.67 / 0.50 | According to Apple's 2018 10-K, how do the specific risks associated with the company's retail store operations differ from the general risk… |
| Single-hop table | [gold-003](cases/gold-003.md) | contrast | 0.00 / 0.00 | 0.00 / 0.00 | 1.00 / 1.00 | 0.00 / 0.50 | What was the percentage decrease in Microsoft's long-lived assets held in Finland from fiscal year 2014 to fiscal year 2016? |
| Single-hop table | [gold-045](cases/gold-045.md) | hardest | 0.00 / 0.00 | 0.00 / 0.00 | 1.00 / 1.00 | 1.00 / 1.00 | In Tesla, Inc.'s fiscal year 2015 10-K, what percentage of the stock options outstanding as of December 31, 2014 were exercisable? |
| Multi-hop table (one filing) | [gold-006](cases/gold-006.md) | contrast | 1.00 / 1.00 | 0.00 / 0.00 | 1.00 / 1.00 | 0.00 / 0.50 | What is the percentage of Amazon.com's total future principal payments due after 2021 relative to the total future principal payments due in… |
| Multi-hop table (one filing) | [gold-010](cases/gold-010.md) | hardest | 0.00 / 0.50 | 0.00 / 0.00 | 1.00 / 1.00 | 0.00 / 0.00 | By what percentage did Walmart's total international segment retail square footage increase from fiscal year 2011 to fiscal year 2015? |
| Table + text (one filing) | [gold-036](cases/gold-036.md) | contrast | 0.00 / 0.00 | 0.00 / 0.50 | 1.00 / 1.00 | 0.83 / 0.50 | For Johnson & Johnson's fiscal year 2025, calculate the percentage change in the valuation allowance for continuing operations from 2024 to … |
| Table + text (one filing) | [gold-061](cases/gold-061.md) | hardest | 0.25 / 0.00 | 0.00 / 0.67 | 0.38 / 0.00 | 0.25 / 0.00 | Calculate the year-over-year percentage growth in Apple's Services net sales for fiscal year 2025 compared to fiscal year 2024. Additionally… |
| Cross-year text | [gold-079](cases/gold-079.md) | contrast | 0.00 / 0.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | How did the description of the evaluation criteria for reporting units and the reassignment of goodwill change in Alphabet Inc.'s 10-K filin… |
| Cross-year text | [gold-084](cases/gold-084.md) | hardest | 0.00 / 0.00 | 0.00 / 1.00 | 1.00 / 1.00 | 0.67 / 1.00 | How did Meta Platforms' accounting policy for recognizing credit losses on available-for-sale debt securities change between its fiscal year… |
| Cross-year table | [gold-015](cases/gold-015.md) | contrast | 0.00 / 0.50 | 0.00 / 0.00 | 1.00 / 1.00 | 1.00 / 1.00 | Calculate the percentage change in Meta Platforms' foreign income before provision for income taxes from fiscal year 2016 to fiscal year 202… |
| Cross-year table | [gold-011](cases/gold-011.md) | hardest | 0.00 / 0.50 | 0.00 / 0.50 | 0.00 / 0.50 | 0.00 / 0.50 | What is the percentage decrease in Microsoft's total estimated future amortization expense for intangible assets from June 30, 2017, to June… |
| Cross-company text | [gold-096](cases/gold-096.md) | contrast | 0.50 / 0.50 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | Compare how Alphabet Inc. and Apple Inc. described their interest rate risk management strategies in their fiscal year 2023 10-K filings, sp… |
| Cross-company text | [gold-094](cases/gold-094.md) | hardest | 0.33 / 0.50 | 0.33 / 0.50 | 0.33 / 0.50 | 0.33 / 0.50 | How do the income tax discussions in Microsoft's and Alphabet's fiscal year 2019 MD&A differ in the U.S. tax law change or tax authority the… |
| Cross-company table | [gold-089](cases/gold-089.md) | contrast | 0.00 / 0.50 | 0.00 / 0.00 | 1.00 / 1.00 | 0.00 / 0.50 | As of the end of fiscal year 2020, by how many millions of dollars did Apple's total term debt exceed Amazon's total long-term debt, based o… |
| Cross-company table | [gold-091](cases/gold-091.md) | hardest | 0.00 / 0.00 | 0.00 / 0.00 | 1.00 / 0.50 | 0.00 / 0.50 | According to their fiscal year 2019 10-Ks, how many millions of dollars more debt principal was Amazon scheduled to repay in 2020 than Johns… |

## Metrics

| Metric | Source | Meaning |
|---|---|---|
| chunks retrieved | RQ1 | number of contexts the system passed to generation (max: A 10, B 5, C 17) |
| recall@5 / recall@all | RQ1 | share of gold evidence items found in the first 5 / all retrieved chunks |
| complete@all | RQ1 | 1 if every gold evidence item was found |
| average precision | RQ1 | RAGAS Context Precision formula with lexical labels (not a RAGAS score) |
| gold evidence first rank | RQ1 | rank of the first chunk holding each gold evidence item (– = not found) |
| gold column in chunk tables | RQ1 matcher | chunk holds that gold evidence item: a 6-word sub-phrase or ≥ 65% of the quote's words appear in it (`scripts/rq1/matching.py`); a lower bound |
| numeric_correct | RQ3 | any number in the answer within 1% of the **first** number in the gold answer (scale-aware, sign ignored). Recorded for every question whose gold answer has a number, including qualitative ones; RQ3's accuracy is the mean of this |
| keypoint_recall | RQ3 | share of gold key points whose content words mostly (≥ 50%) appear in the answer |
| numeric_accuracy | RQ2 | share of the gold numbers (`ground_truth_numbers`) found in the answer |
| citation precision / recall / F1 | RQ2 | section-level (10-K item) match of cited chunks against the gold sections; – when the answer has no citations |
| has a citation | RQ2 | 1 if the answer cites at least one chunk |
| grounding error rate | RQ2 | System C guardrail's share of numerical claims not grounded in the contexts (A and B have no guardrail) |
| hops, tokens, cost, latency | RQ3 | as recorded for this query in the run |
| cited (chunk tables) | records | the chunk id appears in the answer's `citations` |
| System C guardrail block | records | System C's own guardrail output for the answer, including its LLM judge's per-sentence verdicts; it is part of the system, not an evaluation judge |

## Caveats

- Answer scores are string matches. A correct answer phrased differently can score 0, and a wrong answer that contains the gold number can score 1. Treat the scorecard as a pointer to read the answer.
- Gold-evidence labels are lexical. A chunk can state the same fact in other words, or a quote can be split across chunks, and not be marked.
- System C retrieves over several hops; records keep the chunk order but not which hop retrieved each chunk, so the pages do not show per-hop retrieval. v2's XBRL blocks (`F-…` ids) come first.
- System A/B answers were generated with `gpt-5.4-2026-03-05`, System C with `gpt-5.4` (as recorded in the run).
