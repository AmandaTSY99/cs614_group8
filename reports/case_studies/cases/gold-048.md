# gold-048: Multi-hop table (one filing)

[← all cases](../README.md) · company: Alphabet Inc. (GOOGL) · fiscal year: 2023 · recipe `table` · hop `multi` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> For Alphabet Inc. in fiscal year 2023, what was the combined impact of the 'Foreign-derived intangible income deduction' and the 'Effect of tax law change' on the effective income tax rate, expressed as a percentage point change?

**Gold answer**

> -6.0 percentage points

**Program**: `add(-4.6, -1.4)` → `-6.0`

**Gold numbers** (RQ2 numeric_accuracy targets): -6.0 percentage points

**Gold evidence**

1. `GOOGL_FY2023_2023-12-31` · ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Note 14. Income Taxes · table

   > Foreign-derived intangible income deduction | (2.5) | (5.4) | (4.6)

2. `GOOGL_FY2023_2023-12-31` · ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Note 14. Income Taxes · table

   > Effect of tax law change | 0.0 | 0.0 | (1.4)

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 7 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.58 | 0.50 | 0.42 | 0.33 |
| gold evidence first rank | #1: 3, #2: 2 | #1: 2, #2: 2 | #1: 4, #2: 3 | #1: 4, #2: 4 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 0.00 | 0.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 2293 | 1293 | 4192 | 4555 |
| cost (USD) | 0.0004 | 0.0002 | 0.0146 | 0.0153 |
| latency (s) | 1.9 | 6.4 | 6.8 | 6.8 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> For 2023, the **Foreign-derived intangible income deduction** was **(4.6)** percentage points and the **Effect of tax law change** was **(1.4)** percentage points. Combined, they reduced the effective income tax rate by **6.0 percentage points**. [3]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2023_2023-12-31:225` | Item 7 › Provision for Income Taxes |  |  | In 2023, the Internal Revenue Services (IRS) issued a rule change allowing taxpayers to temporarily apply the regulations in effect prior to 2022 related to U.S. federal foreign tax credits, as well as a separate rule ch… |
| 2 | `GOOGL_FY2023_2023-12-31:469` | Item 8 › Note 14. Income Taxes |  | #2 | In 2022, there was an increase in the U.S. Foreign Derived Intangible Income tax deduction from the effects of capitalization and amortization of R&D expenses starting in 2022 as required by the 2017 Tax Cuts and Jobs Ac… |
| 3 | `GOOGL_FY2023_2023-12-31:468` | Item 8 › Note 14. Income Taxes | ✓ | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2022 \| 2023 \| \| U.S. federal statutory tax rate \| 21.0% \| 21.0% \| 21.0% \| \| Foreign income taxed at different rates \| 0.2 \| 3.0 \| 0.3 \| \| Foreign-derived int… |
| 4 | `GOOGL_FY2023_2023-12-31:184` | Item 7 › Other Information: |  |  | Table of Contents Alphabet Inc. •On July 21, 2023, the IRS announced a rule change allowing taxpayers to temporarily apply the regulations in effect prior to 2022 related to U.S. federal foreign tax credits. This announc… |
| 5 | `GOOGL_FY2023_2023-12-31:467` | Item 8 › Note 14. Income Taxes |  |  | 83. Table of Contents Alphabet Inc. The reconciliation of federal statutory income tax rate to our effective income tax rate was as follows: |
| 6 | `GOOGL_FY2023_2023-12-31:472` | Item 8 › Deferred Income Taxes |  |  | (1)As required by the 2017 Tax Cuts and Jobs Act, effective January 1, 2022, our research and development expenditures were capitalized and amortized which resulted in substantially higher cash taxes starting in 2022 wit… |
| 7 | `GOOGL_FY2023_2023-12-31:334` | Item 8 › Income Taxes |  |  | We account for income taxes using the asset and liability method, under which we recognize the amount of taxes payable or refundable for the current year and deferred tax assets and liabilities for the future tax consequ… |
| 8 | `GOOGL_FY2023_2023-12-31:178` | Item 7 › Provision for Income Taxes |  |  | Provision for income taxes represents the estimated amount of federal, state, and foreign income taxes incurred in the U.S. and the many jurisdictions in which we operate. The provision includes the effect of reserve pro… |
| 9 | `GOOGL_FY2023_2023-12-31:471` | Item 8 › Deferred Income Taxes |  |  | \| \| As of December 31, \| \| \|---\|---\|---\| \| \| 2022 \| 2023 \| \| Deferred tax assets: \| \| \| \| Accrued employee benefits \| $955 \| $1,855 \| \| Accruals and reserves not currently deductible \| 1,956 \| 2,481 \| \| Tax credits \| 6,0… |
| 10 | `GOOGL_FY2023_2023-12-31:224` | Item 7 › Provision for Income Taxes |  |  | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2022 \| 2023 \| \| Income before provision for income taxes \| $71,328 \| $85,717 \| \| Provision for income taxes \| $11,356 \| $11,922 \| \| Effective tax rate \| 15.9% \| 13.9% \| |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `GOOGL_FY2023_2023-12-31:469`** (gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 14. Income Taxes
In 2022, there was an increase in the U.S. Foreign Derived Intangible Income tax deduction from the effects of capitalization and amortization of R&D expenses starting in 2022 as required by the 2017 Tax Cuts and Jobs Act. In 2023, the IRS issued a rule change allowing taxpayers to temporarily apply the regulations in effect prior to 2022 related to U.S. federal foreign tax credits as well as a separate rule change with interim guidance on the capitalization and amortization of R&D expenses. A cumulative one-time adjustment applicable to the prior period for these tax rule changes was recorded in 2023.
````

**#3 `GOOGL_FY2023_2023-12-31:468`** (cited, gold #1, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 14. Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2021 | 2022 | 2023 |
| U.S. federal statutory tax rate | 21.0% | 21.0% | 21.0% |
| Foreign income taxed at different rates | 0.2 | 3.0 | 0.3 |
| Foreign-derived intangible income deduction | (2.5) | (5.4) | (4.6) |
| Stock-based compensation expense | (2.5) | (1.2) | (0.8) |
| Federal research credit | (1.6) | (2.2) | (1.8) |
| Deferred tax asset valuation allowance | 0.6 | 0.9 | 0.6 |
| State and local income taxes | 1.0 | 0.8 | 1.0 |
| Effect of tax law change | 0.0 | 0.0 | (1.4) |
| Other | 0.0 | (1.0) | (0.4) |
| Effective tax rate | 16.2% | 15.9% | 13.9% |
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 1.

**Generated answer**

> For 2023, the **Foreign-derived intangible income deduction** was **(4.6)** percentage points and the **Effect of tax law change** was **(1.4)** percentage points. Combined, they impacted the effective income tax rate by **(6.0) percentage points**. [2]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2023_2023-12-31:184` | Item 7 › Other Information: |  |  | Table of Contents Alphabet Inc. •On July 21, 2023, the IRS announced a rule change allowing taxpayers to temporarily apply the regulations in effect prior to 2022 related to U.S. federal foreign tax credits. This announc… |
| 2 | `GOOGL_FY2023_2023-12-31:468` | Item 8 › Note 14. Income Taxes | ✓ | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2022 \| 2023 \| \| U.S. federal statutory tax rate \| 21.0% \| 21.0% \| 21.0% \| \| Foreign income taxed at different rates \| 0.2 \| 3.0 \| 0.3 \| \| Foreign-derived int… |
| 3 | `GOOGL_FY2023_2023-12-31:187` | Item 7 › Google Services |  |  | Google advertising revenues Google Search & other Google Search & other revenues increased $12.6 billion from 2022 to 2023. The overall growth was driven by interrelated factors including increases in search queries resu… |
| 4 | `GOOGL_FY2023_2023-12-31:200` | Item 7 › Use of Non-GAAP Constant Currency Information |  |  | (1)Total constant currency revenues of $309.1 billion for 2023 increased $28.2 billion compared to $280.9 billion in revenues, excluding hedging effect, for 2022. EMEA revenue growth was favorably affected by changes in … |
| 5 | `GOOGL_FY2023_2023-12-31:467` | Item 8 › Note 14. Income Taxes |  |  | 83. Table of Contents Alphabet Inc. The reconciliation of federal statutory income tax rate to our effective income tax rate was as follows: |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `GOOGL_FY2023_2023-12-31:468`** (cited, gold #1, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 14. Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2021 | 2022 | 2023 |
| U.S. federal statutory tax rate | 21.0% | 21.0% | 21.0% |
| Foreign income taxed at different rates | 0.2 | 3.0 | 0.3 |
| Foreign-derived intangible income deduction | (2.5) | (5.4) | (4.6) |
| Stock-based compensation expense | (2.5) | (1.2) | (0.8) |
| Federal research credit | (1.6) | (2.2) | (1.8) |
| Deferred tax asset valuation allowance | 0.6 | 0.9 | 0.6 |
| State and local income taxes | 1.0 | 0.8 | 1.0 |
| Effect of tax law change | 0.0 | 0.0 | (1.4) |
| Other | 0.0 | (1.0) | (0.4) |
| Effective tax rate | 16.2% | 15.9% | 13.9% |
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 1.

**Generated answer**

> For Alphabet Inc. in fiscal year 2023, the Foreign-derived intangible income deduction was (4.6) percentage points and the Effect of tax law change was (1.4) percentage points, for a combined impact of (6.0) percentage points on the effective income tax rate [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:468].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2023_2023-12-31:467` | Item 8 › Note 14. Income Taxes |  |  | 83. Table of Contents Alphabet Inc. The reconciliation of federal statutory income tax rate to our effective income tax rate was as follows: |
| 2 | `GOOGL_FY2023_2023-12-31:225` | Item 7 › Provision for Income Taxes |  |  | In 2023, the Internal Revenue Services (IRS) issued a rule change allowing taxpayers to temporarily apply the regulations in effect prior to 2022 related to U.S. federal foreign tax credits, as well as a separate rule ch… |
| 3 | `GOOGL_FY2023_2023-12-31:469` | Item 8 › Note 14. Income Taxes |  | #2 | In 2022, there was an increase in the U.S. Foreign Derived Intangible Income tax deduction from the effects of capitalization and amortization of R&D expenses starting in 2022 as required by the 2017 Tax Cuts and Jobs Ac… |
| 4 | `GOOGL_FY2023_2023-12-31:468` | Item 8 › Note 14. Income Taxes | ✓ | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2022 \| 2023 \| \| U.S. federal statutory tax rate \| 21.0% \| 21.0% \| 21.0% \| \| Foreign income taxed at different rates \| 0.2 \| 3.0 \| 0.3 \| \| Foreign-derived int… |
| 5 | `GOOGL_FY2023_2023-12-31:184` | Item 7 › Other Information: |  |  | Table of Contents Alphabet Inc. •On July 21, 2023, the IRS announced a rule change allowing taxpayers to temporarily apply the regulations in effect prior to 2022 related to U.S. federal foreign tax credits. This announc… |
| 6 | `GOOGL_FY2023_2023-12-31:178` | Item 7 › Provision for Income Taxes |  |  | Provision for income taxes represents the estimated amount of federal, state, and foreign income taxes incurred in the U.S. and the many jurisdictions in which we operate. The provision includes the effect of reserve pro… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `GOOGL_FY2023_2023-12-31:469`** (gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 14. Income Taxes
In 2022, there was an increase in the U.S. Foreign Derived Intangible Income tax deduction from the effects of capitalization and amortization of R&D expenses starting in 2022 as required by the 2017 Tax Cuts and Jobs Act. In 2023, the IRS issued a rule change allowing taxpayers to temporarily apply the regulations in effect prior to 2022 related to U.S. federal foreign tax credits as well as a separate rule change with interim guidance on the capitalization and amortization of R&D expenses. A cumulative one-time adjustment applicable to the prior period for these tax rule changes was recorded in 2023.
````

**#4 `GOOGL_FY2023_2023-12-31:468`** (cited, gold #1, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 14. Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2021 | 2022 | 2023 |
| U.S. federal statutory tax rate | 21.0% | 21.0% | 21.0% |
| Foreign income taxed at different rates | 0.2 | 3.0 | 0.3 |
| Foreign-derived intangible income deduction | (2.5) | (5.4) | (4.6) |
| Stock-based compensation expense | (2.5) | (1.2) | (0.8) |
| Federal research credit | (1.6) | (2.2) | (1.8) |
| Deferred tax asset valuation allowance | 0.6 | 0.9 | 0.6 |
| State and local income taxes | 1.0 | 0.8 | 1.0 |
| Effect of tax law change | 0.0 | 0.0 | (1.4) |
| Other | 0.0 | (1.0) | (0.4) |
| Effective tax rate | 16.2% | 15.9% | 13.9% |
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| For Alphabet Inc. in fiscal year 2023, the Foreign-derived intangible income deduction was (4.6) percentage points and the Effect of tax law change was (1.4) percentage points, for a combined impact of (6.0) percentage points on the effective income tax rate [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:468]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 1.

**Generated answer**

> For 2023, the Foreign-derived intangible income deduction was (4.6) percentage points and the Effect of tax law change was (1.4) percentage points, for a combined impact of (6.0) percentage points on the effective income tax rate [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:468].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-GOOGL-2023` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2023,2023-12-31,307394000000,73795000000,84293000000,402392000… |
| 2 | `GOOGL_FY2023_2023-12-31:467` | Item 8 › Note 14. Income Taxes |  |  | 83. Table of Contents Alphabet Inc. The reconciliation of federal statutory income tax rate to our effective income tax rate was as follows: |
| 3 | `GOOGL_FY2023_2023-12-31:225` | Item 7 › Provision for Income Taxes |  |  | In 2023, the Internal Revenue Services (IRS) issued a rule change allowing taxpayers to temporarily apply the regulations in effect prior to 2022 related to U.S. federal foreign tax credits, as well as a separate rule ch… |
| 4 | `GOOGL_FY2023_2023-12-31:468` | Item 8 › Note 14. Income Taxes | ✓ | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2022 \| 2023 \| \| U.S. federal statutory tax rate \| 21.0% \| 21.0% \| 21.0% \| \| Foreign income taxed at different rates \| 0.2 \| 3.0 \| 0.3 \| \| Foreign-derived int… |
| 5 | `GOOGL_FY2023_2023-12-31:469` | Item 8 › Note 14. Income Taxes |  | #2 | In 2022, there was an increase in the U.S. Foreign Derived Intangible Income tax deduction from the effects of capitalization and amortization of R&D expenses starting in 2022 as required by the 2017 Tax Cuts and Jobs Ac… |
| 6 | `GOOGL_FY2023_2023-12-31:184` | Item 7 › Other Information: |  |  | Table of Contents Alphabet Inc. •On July 21, 2023, the IRS announced a rule change allowing taxpayers to temporarily apply the regulations in effect prior to 2022 related to U.S. federal foreign tax credits. This announc… |
| 7 | `GOOGL_FY2023_2023-12-31:178` | Item 7 › Provision for Income Taxes |  |  | Provision for income taxes represents the estimated amount of federal, state, and foreign income taxes incurred in the U.S. and the many jurisdictions in which we operate. The provision includes the effect of reserve pro… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#4 `GOOGL_FY2023_2023-12-31:468`** (cited, gold #1, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 14. Income Taxes (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2021 | 2022 | 2023 |
| U.S. federal statutory tax rate | 21.0% | 21.0% | 21.0% |
| Foreign income taxed at different rates | 0.2 | 3.0 | 0.3 |
| Foreign-derived intangible income deduction | (2.5) | (5.4) | (4.6) |
| Stock-based compensation expense | (2.5) | (1.2) | (0.8) |
| Federal research credit | (1.6) | (2.2) | (1.8) |
| Deferred tax asset valuation allowance | 0.6 | 0.9 | 0.6 |
| State and local income taxes | 1.0 | 0.8 | 1.0 |
| Effect of tax law change | 0.0 | 0.0 | (1.4) |
| Other | 0.0 | (1.0) | (0.4) |
| Effective tax rate | 16.2% | 15.9% | 13.9% |
````

**#5 `GOOGL_FY2023_2023-12-31:469`** (gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 14. Income Taxes
In 2022, there was an increase in the U.S. Foreign Derived Intangible Income tax deduction from the effects of capitalization and amortization of R&D expenses starting in 2022 as required by the 2017 Tax Cuts and Jobs Act. In 2023, the IRS issued a rule change allowing taxpayers to temporarily apply the regulations in effect prior to 2022 related to U.S. federal foreign tax credits as well as a separate rule change with interim guidance on the capitalization and amortization of R&D expenses. A cumulative one-time adjustment applicable to the prior period for these tax rule changes was recorded in 2023.
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| For 2023, the Foreign-derived intangible income deduction was (4.6) percentage points and the Effect of tax law change was (1.4) percentage points, for a combined impact of (6.0) percentage points on the effective income tax rate [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:468]. | None |  |

</details>
