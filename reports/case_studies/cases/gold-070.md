# gold-070: Cross-year table

[← all cases](../README.md) · company: Meta Platforms, Inc. (META) · fiscal year: 2023 · recipe `cross_year_table` · hop `multi` · answer type `numeric` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> By how many percentage points did the effect of non-U.S. operations on Meta Platforms' effective tax rate change from fiscal year 2017 to fiscal year 2023?

**Gold answer**

> 19.5 percentage points (from -18.6 in 2017 to 0.9 in 2023)

**Program**: `subtract(0.9, -18.6)` → `19.5`

**Gold numbers** (RQ2 numeric_accuracy targets): 19.5 percentage points

**Gold evidence**

1. `META_FY2023_2023-12-31` · Item 8.Financial Statements and Supplementary Data › Note 15. Income Taxes · table

   > Effect of non-U.S. operations | 0.9 | 3.0 | 0.9 |

2. `META_FY2017_2017-12-31` · Item 8. Financial Statements and Supplementary Data › Share-based Compensation Plans · table

   > Effect of non-U.S. operations | (18.6) | (12.8) | (0.9) |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 9 | 5 | 12 | 11 |
| recall@5 | 1.00 | 1.00 | 0.00 | 0.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.25 | 1.00 | 0.14 | 0.11 |
| gold evidence first rank | #1: 4, #2: 4 | #1: 1, #2: 1 | #1: 7, #2: 7 | #1: 9, #2: 9 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✓ | ✗ | ✗ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 1.00 | 0.00 | 0.00 |
| citation precision | – | 1.00 | 1.00 | 0.50 |
| citation recall | – | 1.00 | 1.00 | 1.00 |
| citation F1 | – | 1.00 | 1.00 | 0.67 |
| has a citation | 0 | 1 | 1 | 1 |
| grounding error rate | – | – | 1.00 | 1.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 1858 | 1328 | 22449 | 21151 |
| cost (USD) | 0.0003 | 0.0002 | 0.0774 | 0.0744 |
| latency (s) | 1.4 | 5.5 | 33.7 | 28.8 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 9, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2017_2017-12-31:231` | Item 7 › Provision for income taxes |  |  | Absent unanticipated events and unexpected effects of the Tax Act, we anticipate our effective tax rate in 2018 will be lower than it was in 2017. Our 2017 effective tax rate was significantly affected by the Tax Act. In… |
| 2 | `META_FY2023_2023-12-31:379` | Item 7 › Provision for income taxes |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| 2023 vs 2022 % change \| 2022 vs 2021 % change \| \| \| (in millions, except percentages) \| \| \| \| \| \| Provision for income taxes \| $8,3… |
| 3 | `META_FY2023_2023-12-31:380` | Item 7 › Provision for income taxes |  |  | Our provision for income taxes in 2023 increased $2.71 billion, or 48%, compared to 2022, due to an increase in income before provision for income taxes. Our effective tax rate in 2023 decreased compared to 2022, primari… |
| 4 | `META_FY2023_2023-12-31:593` | Item 8 › Note 15. Income Taxes |  | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| \| U.S. federal statutory income tax rate \| 21.0% \| 21.0% \| 21.0% \| \| State income taxes, net of federal benefit \| 1.1 \| 1.0 \| 1.0 \| \| Share-bas… |
| 5 | `META_FY2023_2023-12-31:592` | Item 8 › Note 15. Income Taxes |  |  | A reconciliation of the U.S. federal statutory income tax rates to our effective tax rate is as follows (in percentages): |
| 6 | `META_FY2017_2017-12-31:226` | Item 7 › Provision for income taxes |  |  | 2017 Compared to 2016. Our provision for income taxes in 2017 increased $2.36 billion, or 103%, compared to 2016, mostly due to the effects of the Tax Act that was enacted on December 22, 2017 and an increase in income b… |
| 7 | `META_FY2017_2017-12-31:227` | Item 7 › Provision for income taxes |  |  | Our effective tax rate in 2017 increased compared to 2016, mostly due to the Tax Act and a decrease in the tax rate benefit from share-based compensation compared to 2016. These effects were partially offset by an increa… |
| 8 | `META_FY2023_2023-12-31:180` | Item 1A › Changes in tax laws or tax rulings could materially affect our financial position, results of operations, and cash flows. |  |  | Over the last several years, the Organization for Economic Cooperation and Development has been working on a Base Erosion and Profit Shifting Project that, if implemented, would change various aspects of the existing fra… |
| 9 | `META_FY2017_2017-12-31:225` | Item 7 › Provision for income taxes |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2017 \| 2016 \| 2015 \| 2017 vs 2016 % Change \| 2016 vs 2015 % Change \| \| \| (dollars in millions) \| \| \| \| \| \| Provision for income taxes \| $4,660 \| $2,301 … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#4 `META_FY2023_2023-12-31:593`** (gold #1, gold #2)

````text
Item 8.Financial Statements and Supplementary Data > Note 15. Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2023 | 2022 | 2021 |
| U.S. federal statutory income tax rate | 21.0% | 21.0% | 21.0% |
| State income taxes, net of federal benefit | 1.1 | 1.0 | 1.0 |
| Share-based compensation | (0.6) | 2.6 | (1.7) |
| Research and development tax credits | (1.5) | (2.4) | (1.3) |
| Foreign-derived intangible income deduction | (4.3) | (7.0) | (3.5) |
| Effect of non-U.S. operations | 0.9 | 3.0 | 0.9 |
| Other | 1.0 | 1.3 | 0.3 |
| Effective tax rate | 17.6% | 19.5% | 16.7% |
````

</details>

RQ2 citation match (section level): `no citations`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> The effect of non-U.S. operations was **(18.6)%** in 2017 and **0.9%** in 2023, so it changed by **19.5 percentage points** ([2], [1]).

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2023_2023-12-31:593` | Item 8 › Note 15. Income Taxes | ✓ | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| \| U.S. federal statutory income tax rate \| 21.0% \| 21.0% \| 21.0% \| \| State income taxes, net of federal benefit \| 1.1 \| 1.0 \| 1.0 \| \| Share-bas… |
| 2 | `META_FY2017_2017-12-31:402` | Item 8 › Share-based Compensation Plans | ✓ | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2017 \| 2016 \| 2015 \| \| U.S. federal statutory income tax rate \| 35.0% \| 35.0% \| 35.0% \| \| State income taxes, net of federal benefit \| 0.6 \| 1.0 \| 2.0 \| \| Research … |
| 3 | `META_FY2017_2017-12-31:227` | Item 7 › Provision for income taxes |  |  | Our effective tax rate in 2017 increased compared to 2016, mostly due to the Tax Act and a decrease in the tax rate benefit from share-based compensation compared to 2016. These effects were partially offset by an increa… |
| 4 | `META_FY2023_2023-12-31:379` | Item 7 › Provision for income taxes |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| 2023 vs 2022 % change \| 2022 vs 2021 % change \| \| \| (in millions, except percentages) \| \| \| \| \| \| Provision for income taxes \| $8,3… |
| 5 | `META_FY2023_2023-12-31:380` | Item 7 › Provision for income taxes |  |  | Our provision for income taxes in 2023 increased $2.71 billion, or 48%, compared to 2022, due to an increase in income before provision for income taxes. Our effective tax rate in 2023 decreased compared to 2022, primari… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2023_2023-12-31:593`** (cited, gold #1, gold #2)

````text
Item 8.Financial Statements and Supplementary Data > Note 15. Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2023 | 2022 | 2021 |
| U.S. federal statutory income tax rate | 21.0% | 21.0% | 21.0% |
| State income taxes, net of federal benefit | 1.1 | 1.0 | 1.0 |
| Share-based compensation | (0.6) | 2.6 | (1.7) |
| Research and development tax credits | (1.5) | (2.4) | (1.3) |
| Foreign-derived intangible income deduction | (4.3) | (7.0) | (3.5) |
| Effect of non-U.S. operations | 0.9 | 3.0 | 0.9 |
| Other | 1.0 | 1.3 | 0.3 |
| Effective tax rate | 17.6% | 19.5% | 16.7% |
````

**#2 `META_FY2017_2017-12-31:402`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Share-based Compensation Plans (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2017 | 2016 | 2015 |
| U.S. federal statutory income tax rate | 35.0% | 35.0% | 35.0% |
| State income taxes, net of federal benefit | 0.6 | 1.0 | 2.0 |
| Research tax credits | (0.9) | (0.7) | (1.4) |
| Share-based compensation | 0.4 | 1.0 | 2.2 |
| Excess tax benefits related to share-based compensation(1) | (5.8) | (7.0) | — |
| Effect of non-U.S. operations | (18.6) | (12.8) | (0.9) |
| Effect of U.S. tax law change (2) | 11.0 | — | — |
| Other | 0.9 | 1.9 | 3.5 |
| Effective tax rate | 22.6% | 18.4% | 40.4% |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 12, cited: 1.

**Generated answer**

> The filing evidence provided does not disclose the 2017 percentage effect of non-U.S. operations on Meta Platforms' effective tax rate. It does disclose that the effect of non-U.S. operations was 0.9 percentage points in 2023. Therefore, the change from 2017 to 2023 cannot be determined from the provided evidence. [META FY2023, Item 8, META_FY2023_2023-12-31:593]
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 0.9; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2017_2017-12-31:231` | Item 7 › Provision for income taxes |  |  | Absent unanticipated events and unexpected effects of the Tax Act, we anticipate our effective tax rate in 2018 will be lower than it was in 2017. Our 2017 effective tax rate was significantly affected by the Tax Act. In… |
| 2 | `META_FY2023_2023-12-31:380` | Item 7 › Provision for income taxes |  |  | Our provision for income taxes in 2023 increased $2.71 billion, or 48%, compared to 2022, due to an increase in income before provision for income taxes. Our effective tax rate in 2023 decreased compared to 2022, primari… |
| 3 | `META_FY2017_2017-12-31:229` | Item 7 › Provision for income taxes |  |  | Effective Tax Rate Items. Our effective tax rate in the future will depend upon the proportion of our income before provision for income taxes earned in the United States and in jurisdictions with a tax rate lower than t… |
| 4 | `META_FY2017_2017-12-31:227` | Item 7 › Provision for income taxes |  |  | Our effective tax rate in 2017 increased compared to 2016, mostly due to the Tax Act and a decrease in the tax rate benefit from share-based compensation compared to 2016. These effects were partially offset by an increa… |
| 5 | `META_FY2017_2017-12-31:226` | Item 7 › Provision for income taxes |  |  | 2017 Compared to 2016. Our provision for income taxes in 2017 increased $2.36 billion, or 103%, compared to 2016, mostly due to the effects of the Tax Act that was enacted on December 22, 2017 and an increase in income b… |
| 6 | `META_FY2023_2023-12-31:379` | Item 7 › Provision for income taxes |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| 2023 vs 2022 % change \| 2022 vs 2021 % change \| \| \| (in millions, except percentages) \| \| \| \| \| \| Provision for income taxes \| $8,3… |
| 7 | `META_FY2023_2023-12-31:593` | Item 8 › Note 15. Income Taxes | ✓ | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| \| U.S. federal statutory income tax rate \| 21.0% \| 21.0% \| 21.0% \| \| State income taxes, net of federal benefit \| 1.1 \| 1.0 \| 1.0 \| \| Share-bas… |
| 8 | `META_FY2023_2023-12-31:592` | Item 8 › Note 15. Income Taxes |  |  | A reconciliation of the U.S. federal statutory income tax rates to our effective tax rate is as follows (in percentages): |
| 9 | `META_FY2023_2023-12-31:543` | Item 8 › Note 10. Long-term Debt |  |  | \| \| Maturity \| Stated Interest Rate \| Effective Interest Rate \| December 31, 2023 \| December 31, 2022 \| \|---\|---\|---\|---\|---\|---\| \| August 2022 debt: \| \| \| \| \| \| \| 2027 Notes \| 2027 \| 3.50% \| 3.63% \| $2,750 \| $2,750 \| \| … |
| 10 | `META_FY2023_2023-12-31:377` | Item 7 › Interest and other income (expense), net |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| 2023 vs 2022 % change \| 2022 vs 2021 % change \| \| \| (in millions, except percentages) \| \| \| \| \| \| Interest income \| $1,639 \| $461 \|… |
| 11 | `META_FY2023_2023-12-31:589` | Item 8 › Note 15. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| \| Domestic \| $43,499 \| $25,025 \| $43,669 \| \| Foreign \| 3,929 \| 3,794 \| 3,615 \| \| Income before provision for income taxes \| $47,428 \| $28,819 \|… |
| 12 | `META_FY2017_2017-12-31:401` | Item 8 › Share-based Compensation Plans |  |  | A reconciliation of the U.S. federal statutory income tax rate of 35.0% to our effective tax rate is as follows (in percentages): |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#7 `META_FY2023_2023-12-31:593`** (cited, gold #1, gold #2)

````text
Item 8.Financial Statements and Supplementary Data > Note 15. Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2023 | 2022 | 2021 |
| U.S. federal statutory income tax rate | 21.0% | 21.0% | 21.0% |
| State income taxes, net of federal benefit | 1.1 | 1.0 | 1.0 |
| Share-based compensation | (0.6) | 2.6 | (1.7) |
| Research and development tax credits | (1.5) | (2.4) | (1.3) |
| Foreign-derived intangible income deduction | (4.3) | (7.0) | (3.5) |
| Effect of non-U.S. operations | 0.9 | 3.0 | 0.9 |
| Other | 1.0 | 1.3 | 0.3 |
| Effective tax rate | 17.6% | 19.5% | 16.7% |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 1, verified 0, ungrounded 1, uncited 1, derived 0; sentence verdicts: supported 4, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 0.9
- uncited numbers: 0.9

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| The filing evidence provided does not disclose the 2017 percentage effect of non-U.S. | supported | The retrieved evidence does not provide a 2017 percentage labeled as the effect of non-U.S. operations. |
| operations on Meta Platforms' effective tax rate. | supported | No retrieved evidence states the 2017 percentage effect of non-U.S. operations on the effective tax rate. |
| It does disclose that the effect of non-U.S. | supported | The evidence does disclose the effect of non-U.S. operations for later years, including 2023, 2022, and 2021. |
| operations was 0.9 percentage points in 2023. | None |  |
| Therefore, the change from 2017 to 2023 cannot be determined from the provided evidence. [META FY2023, Item 8, META_FY2023_2023-12-31:593] | supported | The cited table only shows 2021-2023, so it cannot determine a change from 2017 to 2023 from the provided evidence. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 11, cited: 2.

**Generated answer**

> Meta disclosed that the effect of non-U.S. operations was 0.9 percentage points in 2023. For 2017, the filing states that the effective tax rate was partially offset by an increase in income earned in jurisdictions with tax rates lower than the U.S. statutory tax rate, but it does not quantify that effect in percentage points. Therefore, the change from 2017 to 2023 in percentage points is not disclosed in the provided evidence. [META FY2023, Item 8, META_FY2023_2023-12-31:593] [META FY2017, Item 7, META_FY2017_2017-12-31:227]
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 0.9; 2 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2017_2017-12-31:231` | Item 7 › Provision for income taxes |  |  | Absent unanticipated events and unexpected effects of the Tax Act, we anticipate our effective tax rate in 2018 will be lower than it was in 2017. Our 2017 effective tax rate was significantly affected by the Tax Act. In… |
| 2 | `META_FY2023_2023-12-31:380` | Item 7 › Provision for income taxes |  |  | Our provision for income taxes in 2023 increased $2.71 billion, or 48%, compared to 2022, due to an increase in income before provision for income taxes. Our effective tax rate in 2023 decreased compared to 2022, primari… |
| 3 | `META_FY2017_2017-12-31:229` | Item 7 › Provision for income taxes |  |  | Effective Tax Rate Items. Our effective tax rate in the future will depend upon the proportion of our income before provision for income taxes earned in the United States and in jurisdictions with a tax rate lower than t… |
| 4 | `META_FY2017_2017-12-31:227` | Item 7 › Provision for income taxes | ✓ |  | Our effective tax rate in 2017 increased compared to 2016, mostly due to the Tax Act and a decrease in the tax rate benefit from share-based compensation compared to 2016. These effects were partially offset by an increa… |
| 5 | `META_FY2017_2017-12-31:226` | Item 7 › Provision for income taxes |  |  | 2017 Compared to 2016. Our provision for income taxes in 2017 increased $2.36 billion, or 103%, compared to 2016, mostly due to the effects of the Tax Act that was enacted on December 22, 2017 and an increase in income b… |
| 6 | `META_FY2023_2023-12-31:379` | Item 7 › Provision for income taxes |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| 2023 vs 2022 % change \| 2022 vs 2021 % change \| \| \| (in millions, except percentages) \| \| \| \| \| \| Provision for income taxes \| $8,3… |
| 7 | `META_FY2023_2023-12-31:592` | Item 8 › Note 15. Income Taxes |  |  | A reconciliation of the U.S. federal statutory income tax rates to our effective tax rate is as follows (in percentages): |
| 8 | `META_FY2017_2017-12-31:401` | Item 8 › Share-based Compensation Plans |  |  | A reconciliation of the U.S. federal statutory income tax rate of 35.0% to our effective tax rate is as follows (in percentages): |
| 9 | `META_FY2023_2023-12-31:593` | Item 8 › Note 15. Income Taxes | ✓ | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| \| U.S. federal statutory income tax rate \| 21.0% \| 21.0% \| 21.0% \| \| State income taxes, net of federal benefit \| 1.1 \| 1.0 \| 1.0 \| \| Share-bas… |
| 10 | `META_FY2023_2023-12-31:598` | Item 8 › Note 15. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| \| Gross unrecognized tax benefits ‑ beginning of period \| $10,757 \| $9,807 \| $8,692 \| \| Increases related to prior year tax positions \| 168 \| 2… |
| 11 | `META_FY2017_2017-12-31:225` | Item 7 › Provision for income taxes |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2017 \| 2016 \| 2015 \| 2017 vs 2016 % Change \| 2016 vs 2015 % Change \| \| \| (dollars in millions) \| \| \| \| \| \| Provision for income taxes \| $4,660 \| $2,301 … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#4 `META_FY2017_2017-12-31:227`** (cited)

````text
Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations > Provision for income taxes
Our effective tax rate in 2017 increased compared to 2016, mostly due to the Tax Act and a decrease in the tax rate benefit from share-based compensation compared to 2016. These effects were partially offset by an increase in income before provision for income taxes being earned in jurisdictions with tax rates lower than the U.S. statutory tax rate. In 2017, excess tax benefits recognized from share-based compensation decreased our provision for income taxes by $1.25 billion and our effective tax rate by six percentage points as compared to the tax rate without such benefits. For comparison, in 2016, excess tax benefits recognized from share-based compensation decreased our provision for income taxes by $934 million and our effective tax rate by seven percentage points, as compared to the tax rate without such benefits.
````

**#9 `META_FY2023_2023-12-31:593`** (cited, gold #1, gold #2)

````text
Item 8.Financial Statements and Supplementary Data > Note 15. Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2023 | 2022 | 2021 |
| U.S. federal statutory income tax rate | 21.0% | 21.0% | 21.0% |
| State income taxes, net of federal benefit | 1.1 | 1.0 | 1.0 |
| Share-based compensation | (0.6) | 2.6 | (1.7) |
| Research and development tax credits | (1.5) | (2.4) | (1.3) |
| Foreign-derived intangible income deduction | (4.3) | (7.0) | (3.5) |
| Effect of non-U.S. operations | 0.9 | 3.0 | 0.9 |
| Other | 1.0 | 1.3 | 0.3 |
| Effective tax rate | 17.6% | 19.5% | 16.7% |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8'), ('META', 'Item 7')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 1, verified 0, ungrounded 1, uncited 1, derived 0; sentence verdicts: supported 2, partial 0, unsupported 1, unchecked 0.

- ungrounded numbers: 0.9
- uncited numbers: 0.9

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta disclosed that the effect of non-U.S. | unsupported | The evidence does not contain a complete disclosed statement about the effect of non-U.S. operations for 2017. |
| operations was 0.9 percentage points in 2023. | None |  |
| For 2017, the filing states that the effective tax rate was partially offset by an increase in income earned in jurisdictions with tax rates lower than the U.S. statutory tax rate, but it does not quantify that effect in percentage points. | supported | The 2017 evidence says the lower-tax-jurisdiction income partially offset the rate increase but gives no percentage-point quantification for that effect. |
| Therefore, the change from 2017 to 2023 in percentage points is not disclosed in the provided evidence. [META FY2023, Item 8, META_FY2023_2023-12-31:593] [META FY2017, Item 7, META_FY2017_2017-12-31:227] | supported | The cited 2023 table quantifies non-U.S. operations at 0.9 points, while the 2017 cited text does not quantify that effect, so the change is not disclosed. |

</details>
