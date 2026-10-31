# gold-001: Single-hop table

[← all cases](../README.md) · company: JOHNSON & JOHNSON (JNJ) · fiscal year: 2022 · recipe `table` · hop `single` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> For Johnson & Johnson's fiscal year 2022, calculate the year-over-year percentage decrease in the accumulated benefit obligation for plans with accumulated benefit obligations in excess of plan assets.

**Gold answer**

> -25.64%

**Program**: `subtract(2.9, 3.9), divide(#0, 3.9)` → `-0.25641025641025644`

**Gold numbers** (RQ2 numeric_accuracy targets): -25.64%

**Gold evidence**

1. `JNJ_FY2022_2023-01-01` · Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › 10.Pensions and Other Benefit Plans · text

   > Plans with accumulated benefit obligations in excess of plan assets have an accumulated benefit obligation, projected benefit obligation and plan assets of $2.9 billion, $2.9 billion and $0.3 billion, respectively, at the end of 2022, and $3.9 billion, $4.2 billion and $0.3 billion, respectively, at the end of 2021.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 7 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 1.00 | 1.00 | 1.00 | 0.50 |
| gold evidence first rank | #1: 1 | #1: 1 | #1: 1 | #1: 2 |
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
| tokens | 2407 | 1063 | 4822 | 5172 |
| cost (USD) | 0.0004 | 0.0002 | 0.0167 | 0.0175 |
| latency (s) | 2.4 | 8.0 | 7.1 | 7.9 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> For plans with accumulated benefit obligations in excess of plan assets, the accumulated benefit obligation was **$3.9 billion in 2021** and **$2.9 billion in 2022** [1].
>
> Year-over-year percentage decrease:
>
> \[
> \frac{3.9 - 2.9}{3.9} \times 100 \approx 25.6\%
> \]
>
> So, the accumulated benefit obligation **decreased by approximately 25.6%** from 2021 to 2022 [1].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2022_2023-01-01:381` | Item 8 › 10.Pensions and Other Benefit Plans | ✓ | #1 | Plans with accumulated benefit obligations in excess of plan assets have an accumulated benefit obligation, projected benefit obligation and plan assets of $2.9 billion, $2.9 billion and $0.3 billion, respectively, at th… |
| 2 | `JNJ_FY2022_2023-01-01:399` | Item 8 › 13.Accumulated Other Comprehensive Income (Loss) |  |  | \| (Dollars in Millions) \| Foreign Currency Translation \| Gain/(Loss) On Securities \| Employee Benefit Plans \| Gain/ (Loss) On Derivatives & Hedges \| Total Accumulated Other Comprehensive Income (Loss) \| \|---\|---\|---\|---\|… |
| 3 | `JNJ_FY2022_2023-01-01:374` | Item 8 › 10.Pensions and Other Benefit Plans |  |  | The following table sets forth information related to the benefit obligation and the fair value of plan assets at fiscal year-end 2022 and 2021 for the Company’s defined benefit retirement plans and other post-retirement… |
| 4 | `JNJ_FY2022_2023-01-01:386` | Item 8 › 10.Pensions and Other Benefit Plans |  |  | \| \| Percent of Plan Assets \| \| Target Allocation \| \|---\|---\|---\|---\| \| \| 2022 \| 2021 \| 2023 \| \| Worldwide Retirement Plans \| \| \| \| \| Equity securities \| 62% \| 65% \| 61% \| \| Debt securities \| 38 \| 35 \| 39 \| \| Total plan a… |
| 5 | `JNJ_FY2022_2023-01-01:375` | Item 8 › 10.Pensions and Other Benefit Plans |  |  | \| \| Retirement Plans \| \| Other Benefit Plans \| \| \|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| 2022 \| 2021 \| 2022 \| 2021 \| \| Change in Benefit Obligation \| \| \| \| \| \| Projected benefit obligation — beginning of year \| $… |
| 6 | `JNJ_FY2022_2023-01-01:352` | Item 8 › 8.Income Taxes |  |  | The fiscal year 2021 tax rate decreased by 2.5% compared to the fiscal year 2020 tax rate, which was primarily driven by the following items. In fiscal year 2021, the Company reorganized the ownership structure of certai… |
| 7 | `JNJ_FY2022_2023-01-01:364` | Item 8 › 9.Employee Related Obligations |  |  | \| (Dollars in Millions) \| 2022 \| 2021 \| \|---\|---\|---\| \| Pension benefits \| $2,698 \| 4,088 \| \| Postretirement benefits \| 1,734 \| 2,069 \| \| Postemployment benefits \| 2,832 \| 3,117 \| \| Deferred compensation \| 100 \| 181 \| \| … |
| 8 | `JNJ_FY2022_2023-01-01:359` | Item 8 › 8.Income Taxes |  |  | (1) Certain prior year amounts have been reclassified to conform to current year presentation. (2) Amount is inclusive of the $2.3 billion deferred tax asset established as part of the reorganized ownership structure of … |
| 9 | `JNJ_FY2022_2023-01-01:301` | Item 8 › 4.Property, Plant and Equipment |  |  | The Company capitalizes interest expense as part of the cost of construction of facilities and equipment. Interest expense capitalized in fiscal years 2022, 2021 and 2020 was $49 million, $49 million and $63 million, res… |
| 10 | `JNJ_FY2022_2023-01-01:378` | Item 8 › 10.Pensions and Other Benefit Plans |  |  | \| \| Retirement Plans \| \| Other Benefit Plans \| \| \|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| 2022 \| 2021 \| 2022 \| 2021 \| \| Amounts Recognized in Net Periodic Benefit Cost and Other Comprehensive Income \| \| \| \| \| \| Ne… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2022_2023-01-01:381`** (cited, gold #1)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > 10.Pensions and Other Benefit Plans
Plans with accumulated benefit obligations in excess of plan assets have an accumulated benefit obligation, projected benefit obligation and plan assets of $2.9 billion, $2.9 billion and $0.3 billion, respectively, at the end of 2022, and $3.9 billion, $4.2 billion and $0.3 billion, respectively, at the end of 2021. The following table displays the projected future benefit payments from the Company’s retirement and other benefit plans:
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 1.

**Generated answer**

> The accumulated benefit obligation decreased from $3.9 billion in 2021 to $2.9 billion in 2022 [1].
>
> Percentage decrease = \(\frac{3.9 - 2.9}{3.9} \times 100\) = approximately **25.6%** [1]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2022_2023-01-01:381` | Item 8 › 10.Pensions and Other Benefit Plans | ✓ | #1 | Plans with accumulated benefit obligations in excess of plan assets have an accumulated benefit obligation, projected benefit obligation and plan assets of $2.9 billion, $2.9 billion and $0.3 billion, respectively, at th… |
| 2 | `JNJ_FY2022_2023-01-01:393` | Item 8 › Valuation Hierarchy |  |  | (1) The activity for the Level 3 assets is not significant for all years presented. The Company's Other Benefit Plans are unfunded except for U.S. commingled funds (Level 2) of $78 million and $102 million at December 31… |
| 3 | `JNJ_FY2022_2023-01-01:380` | Item 8 › 10.Pensions and Other Benefit Plans |  |  | \| \| U.S. Plans \| \| \| \| International Plans \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Qualified Plans \| \| Non-Qualified Plans \| \| Funded Plans \| \| Unfunded Plans \| \| \| (Dollars in Millions) \| 2022 \| 2021 \| 2022 \| … |
| 4 | `JNJ_FY2022_2023-01-01:374` | Item 8 › 10.Pensions and Other Benefit Plans |  |  | The following table sets forth information related to the benefit obligation and the fair value of plan assets at fiscal year-end 2022 and 2021 for the Company’s defined benefit retirement plans and other post-retirement… |
| 5 | `JNJ_FY2022_2023-01-01:386` | Item 8 › 10.Pensions and Other Benefit Plans |  |  | \| \| Percent of Plan Assets \| \| Target Allocation \| \|---\|---\|---\|---\| \| \| 2022 \| 2021 \| 2023 \| \| Worldwide Retirement Plans \| \| \| \| \| Equity securities \| 62% \| 65% \| 61% \| \| Debt securities \| 38 \| 35 \| 39 \| \| Total plan a… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2022_2023-01-01:381`** (cited, gold #1)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > 10.Pensions and Other Benefit Plans
Plans with accumulated benefit obligations in excess of plan assets have an accumulated benefit obligation, projected benefit obligation and plan assets of $2.9 billion, $2.9 billion and $0.3 billion, respectively, at the end of 2022, and $3.9 billion, $4.2 billion and $0.3 billion, respectively, at the end of 2021. The following table displays the projected future benefit payments from the Company’s retirement and other benefit plans:
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 1.

**Generated answer**

> For plans with accumulated benefit obligations in excess of plan assets, the accumulated benefit obligation was $2.9 billion at the end of 2022 and $3.9 billion at the end of 2021 [JNJ FY2022, Item 8, JNJ_FY2022_2023-01-01:381].  
> The year-over-year percentage decrease was approximately 25.6%, calculated as (($3.9 billion - $2.9 billion) / $3.9 billion) × 100 [JNJ FY2022, Item 8, JNJ_FY2022_2023-01-01:381].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2022_2023-01-01:381` | Item 8 › 10.Pensions and Other Benefit Plans | ✓ | #1 | Plans with accumulated benefit obligations in excess of plan assets have an accumulated benefit obligation, projected benefit obligation and plan assets of $2.9 billion, $2.9 billion and $0.3 billion, respectively, at th… |
| 2 | `JNJ_FY2022_2023-01-01:374` | Item 8 › 10.Pensions and Other Benefit Plans |  |  | The following table sets forth information related to the benefit obligation and the fair value of plan assets at fiscal year-end 2022 and 2021 for the Company’s defined benefit retirement plans and other post-retirement… |
| 3 | `JNJ_FY2022_2023-01-01:380` | Item 8 › 10.Pensions and Other Benefit Plans |  |  | \| \| U.S. Plans \| \| \| \| International Plans \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Qualified Plans \| \| Non-Qualified Plans \| \| Funded Plans \| \| Unfunded Plans \| \| \| (Dollars in Millions) \| 2022 \| 2021 \| 2022 \| … |
| 4 | `JNJ_FY2022_2023-01-01:377` | Item 8 › 10.Pensions and Other Benefit Plans |  |  | \| \| Retirement Plans \| \| Other Benefit Plans \| \| \|---\|---\|---\|---\|---\| \| Current liabilities \| (132) \| (115) \| (461) \| (438) \| \| Non-current liabilities \| (2,566) \| (3,973) \| (3,658) \| (4,338) \| \| Total recognized in the… |
| 5 | `JNJ_FY2022_2023-01-01:376` | Item 8 › 10.Pensions and Other Benefit Plans |  |  | \| \| Retirement Plans \| \| Other Benefit Plans \| \| \|---\|---\|---\|---\|---\| \| Plan assets at fair value — beginning of year \| $41,930 \| 38,195 \| 102 \| 90 \| \| Actual return (loss) on plan assets \| (8,665) \| 4,439 \| (17) \| 17 \|… |
| 6 | `JNJ_FY2022_2023-01-01:375` | Item 8 › 10.Pensions and Other Benefit Plans |  |  | \| \| Retirement Plans \| \| Other Benefit Plans \| \| \|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| 2022 \| 2021 \| 2022 \| 2021 \| \| Change in Benefit Obligation \| \| \| \| \| \| Projected benefit obligation — beginning of year \| $… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JNJ_FY2022_2023-01-01:381`** (cited, gold #1)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > 10.Pensions and Other Benefit Plans
Plans with accumulated benefit obligations in excess of plan assets have an accumulated benefit obligation, projected benefit obligation and plan assets of $2.9 billion, $2.9 billion and $0.3 billion, respectively, at the end of 2022, and $3.9 billion, $4.2 billion and $0.3 billion, respectively, at the end of 2021. The following table displays the projected future benefit payments from the Company’s retirement and other benefit plans:
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| For plans with accumulated benefit obligations in excess of plan assets, the accumulated benefit obligation was $2.9 billion at the end of 2022 and $3.9 billion at the end of 2021 [JNJ FY2022, Item 8, JNJ_FY2022_2023-01-01:381]. | None |  |
| The year-over-year percentage decrease was approximately 25.6%, calculated as (($3.9 billion - $2.9 billion) / $3.9 billion) × 100 [JNJ FY2022, Item 8, JNJ_FY2022_2023-01-01:381]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 1.

**Generated answer**

> For plans with accumulated benefit obligations in excess of plan assets, the accumulated benefit obligation decreased from $3.9 billion at the end of 2021 to $2.9 billion at the end of 2022, a year-over-year decrease of approximately 25.6% (($3.9 billion - $2.9 billion) / $3.9 billion) [JNJ FY2022, Item 8, JNJ_FY2022_2023-01-01:381].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-JNJ-2022` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2022,2023-01-01,94943000000,17941000000,,187378000000,11057400… |
| 2 | `JNJ_FY2022_2023-01-01:381` | Item 8 › 10.Pensions and Other Benefit Plans | ✓ | #1 | Plans with accumulated benefit obligations in excess of plan assets have an accumulated benefit obligation, projected benefit obligation and plan assets of $2.9 billion, $2.9 billion and $0.3 billion, respectively, at th… |
| 3 | `JNJ_FY2022_2023-01-01:374` | Item 8 › 10.Pensions and Other Benefit Plans |  |  | The following table sets forth information related to the benefit obligation and the fair value of plan assets at fiscal year-end 2022 and 2021 for the Company’s defined benefit retirement plans and other post-retirement… |
| 4 | `JNJ_FY2022_2023-01-01:380` | Item 8 › 10.Pensions and Other Benefit Plans |  |  | \| \| U.S. Plans \| \| \| \| International Plans \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Qualified Plans \| \| Non-Qualified Plans \| \| Funded Plans \| \| Unfunded Plans \| \| \| (Dollars in Millions) \| 2022 \| 2021 \| 2022 \| … |
| 5 | `JNJ_FY2022_2023-01-01:377` | Item 8 › 10.Pensions and Other Benefit Plans |  |  | \| \| Retirement Plans \| \| Other Benefit Plans \| \| \|---\|---\|---\|---\|---\| \| Current liabilities \| (132) \| (115) \| (461) \| (438) \| \| Non-current liabilities \| (2,566) \| (3,973) \| (3,658) \| (4,338) \| \| Total recognized in the… |
| 6 | `JNJ_FY2022_2023-01-01:376` | Item 8 › 10.Pensions and Other Benefit Plans |  |  | \| \| Retirement Plans \| \| Other Benefit Plans \| \| \|---\|---\|---\|---\|---\| \| Plan assets at fair value — beginning of year \| $41,930 \| 38,195 \| 102 \| 90 \| \| Actual return (loss) on plan assets \| (8,665) \| 4,439 \| (17) \| 17 \|… |
| 7 | `JNJ_FY2022_2023-01-01:375` | Item 8 › 10.Pensions and Other Benefit Plans |  |  | \| \| Retirement Plans \| \| Other Benefit Plans \| \| \|---\|---\|---\|---\|---\| \| (Dollars in Millions) \| 2022 \| 2021 \| 2022 \| 2021 \| \| Change in Benefit Obligation \| \| \| \| \| \| Projected benefit obligation — beginning of year \| $… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `JNJ_FY2022_2023-01-01:381`** (cited, gold #1)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > 10.Pensions and Other Benefit Plans
Plans with accumulated benefit obligations in excess of plan assets have an accumulated benefit obligation, projected benefit obligation and plan assets of $2.9 billion, $2.9 billion and $0.3 billion, respectively, at the end of 2022, and $3.9 billion, $4.2 billion and $0.3 billion, respectively, at the end of 2021. The following table displays the projected future benefit payments from the Company’s retirement and other benefit plans:
````

</details>

RQ2 citation match (section level): `cited=[('JNJ', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| For plans with accumulated benefit obligations in excess of plan assets, the accumulated benefit obligation decreased from $3.9 billion at the end of 2021 to $2.9 billion at the end of 2022, a year-over-year decrease of approximately 25.6% (($3.9 billion - $2.9 billion) / $3.9 billion) [JNJ FY2022, Item 8, JNJ_FY2022_2023-01-01:381]. | None |  |

</details>
