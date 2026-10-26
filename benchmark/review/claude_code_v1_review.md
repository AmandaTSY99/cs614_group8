# Review: 60 new QAs (benchmark/parts/amanda.jsonl, FY2015 onwards)

Each QA was checked against its sources: the full table (headers and columns) or the text around each quote, plus the
rest of the source section for claims the quotes don't cover. The checks were: the question stands alone and makes
sense, the answer is right and complete, the evidence supports it, and the question does not give the answer away.

- **30 QAs are fine as they are.**
- **27 QAs are corrected** in `benchmark/review/claude_code_v1.jsonl` (same ids and format as `amanda.jsonl`). Every
  corrected QA passes the generator's checks: quotes are verbatim in the source, the program matches the answer
  within rounding, and every program number is in the quoted evidence.
- **3 QAs should be dropped** (038, 046, 053) and regenerated: one cross_year_table, one cross_year_text and one
  cross_company_table.

## Problems found

| Problem | QAs | Count |
|---|---|---|
| Question gives the answer's figures away | 029, 036, 051, 055 | 4 |
| Calculation compares things that don't belong together | 001, 004, 010, 027, 052, 053 | 6 |
| Wrong or misleading answer | 030 (% change of a sign-flipping rate), 034 (says "higher" but it fell), 037 (rounding), 060 (Tesla claim not in the filing), 043 ("13 countries" not in the filing) | 5 |
| Answer incomplete, or claims not in the evidence | 018 (units), 020, 021, 022, 023, 047 | 6 |
| Question unclear or not standalone | 005, 007 ("the table"), 017 (no year, "which currency" for three), 025, 054, 057 | 6 |
| Unusable | 038 (ratio of two unrelated metrics, refers to "S1"/"S2"), 046 (only true of one Overview paragraph), 053 (ratio of unrelated metrics) | 3 |
| Formatting only | 008 (no units) | 1 |

The script's checks caught arithmetic and quoting errors well: no wrong arithmetic got through, unlike v0. What they
can't catch is whether a calculation is meaningful, which is now the main problem: 6 forced comparisons (e.g.
"Apple's total dividends in $ minus J&J's dividend per share"). Cross-company table QAs were the weakest (3 of 5 needed
a rewrite, 1 dropped), because two companies' tables rarely share a comparable line item.

## Applying

1. Replace the 27 QAs in `benchmark/parts/amanda.jsonl` with the versions in `claude_code_v1.jsonl` (matched by id),
   and delete 038, 046 and 053.
2. Rerun `python build_benchmark_qa.py --name amanda --min-year 2015` to generate the 3 replacements.
3. Review those 3, then run `--merge` for `benchmark_qa_1.jsonl`.

## Corrected and dropped QAs

| id | recipe | issue | old | new |
|---|---|---|---|---|
| 001 | table | Compared White share of *all employees* with Black share of the *Board* | 25 pp (43 − 18) | White share: Board 82% vs all employees 43% = **39 pp** (single hop) |
| 004 | table | "Sales minus net earnings" is not a meaningful figure | $66,284 million | Net earnings as % of sales: **18.75%** |
| 005 | table | Mixed "fiscal 2015" with options "as of December 31, 2014" | — | Question reworded: options outstanding at Dec 31, 2014, as reported in the FY2015 10-K (55.95%) |
| 007 | table | Referred to "the table" | — | Question reworded to stand alone (-20.00%) |
| 008 | table | Answer had no units | -6.0 | **-6.0 percentage points** |
| 010 | table | R&D as % of cost of products sold is not a standard ratio | 41.94% | R&D as % of sales: **12.65%** (evidence: sales row added) |
| 017 | text | No fiscal year; asked for one currency, answer lists three | — | Question names FY2019 and asks for the currencies |
| 018 | table_text | Square feet are in thousands | "increased by 4,571" | **4,571 thousand square feet**; key points updated |
| 020 | table_text | Table evidence (debt maturities) was not used | — | Unused evidence removed; answer written in full |
| 021 | table_text | Answer only gave the number; question also asks two explanations | 13.51% | Full answer: 13.51% + net-basis accounting + competitive pressures |
| 022 | table_text | Capex range $4.50–6.00 billion was not in the evidence | — | Capex sentence added to evidence |
| 023 | table_text | Answer had no units; 38.3% vs 37.3% not in the evidence | "1176, ..." | **$1,176 million** + full explanation; Pharmaceutical sentence added to evidence |
| 025 | table_text | Asked for the "driver of changes" in the returns reserve; the source gives its estimation basis | — | Question asks how the reserve is estimated; answer in full |
| 027 | cross_year_table | Compared FY2024 R&D with FY2018 *total* operating expenses | $6,063 million | R&D growth FY2018→FY2024: **382.75%** (FY2018 R&D row added) |
| 029 | cross_year_table | Question stated both figures | — | Figures removed (22.76%) |
| 030 | cross_year_table | % change of a rate that flips sign (−18.6 → 0.9) is meaningless | 104.84% | **19.5 percentage points** |
| 034 | cross_year_table | Asked how much *higher* 2024 was; 2024 was lower | "higher by $1,746 million" | Asks how much **lower** ($1,746 million) |
| 036 | cross_year_table | Question stated both figures | — | Figures removed (19.38%) |
| 037 | cross_year_table | Rounding error (validator's tolerance let it through); ratio as "%" is awkward | 823.02% | Revenue growth FY2017→FY2023: **722.99%** |
| 038 | cross_year_table | Ratio of 2019 PPE additions to 2016 segment assets; question refers to "S1"/"S2" | — | **Drop** |
| 043 | cross_year_text | "13 countries" not in the filing; Mexico missing from FY2021 list | — | Answer rewritten from the filings |
| 046 | cross_year_text | Says product names were dropped, but only from one Overview paragraph (the FY2024 10-K still names Megapack/Powerwall elsewhere) | — | **Drop** |
| 047 | cross_year_text | Password spray attack and supply chain claims not in the evidence; "source code repositories" not in the source | — | Answer rewritten; 2 FY2025 sentences added to evidence |
| 051 | cross_company_table | Question stated both figures | — | Figures removed ($72,904 million) |
| 052 | cross_company_table | Subtracted J&J's dividend *per share* from Apple's *total* dividends | 99.97% | J&J dividend per share vs Apple's: **38.33%** higher |
| 053 | cross_company_table | Ratio of J&J contractual obligations to Meta's amortization expense; figures in question | — | **Drop** |
| 054 | cross_company_table | Program negated a negative result; direction unclear | 207 million | Asks how much more Amazon repays in 2020: **$207 million** |
| 055 | cross_company_table | Question stated both figures | — | Figures removed (59.74%) |
| 057 | cross_company_text | Called MD&A income tax sections "risk disclosures" | — | Question reworded |
| 060 | cross_company_text | Said both companies' leases are typically ≤10 years; Tesla's filing doesn't say this | — | Answer and key points rewritten |

## Weak but kept

- 013: the answer restates the one quoted sentence. Valid, but easy.
- 006, 008: ratios that an analyst might compute, though not common.
- 016, 019, 021: combine unrelated sub-questions in one QA (allowed by the table_text recipe).
