# gold-078: Cross-year table

[← all cases](../README.md) · company: Tesla, Inc. (TSLA) · fiscal year: 2023 · recipe `cross_year_table` · hop `multi` · answer type `numeric` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> By how many millions of dollars did Tesla's accrued warranty liability at the end of the fiscal year 2023 exceed the accrued warranty liability at the end of the fiscal year 2018?

**Gold answer**

> $4,404.17 million

**Program**: `divide(747826, 1000), subtract(5152, #0)` → `4404.174`

**Gold numbers** (RQ2 numeric_accuracy targets): $4,404.17 million

**Gold evidence**

1. `TSLA_FY2023_2023-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Note 2 – Summary of Significant Accounting Policies · table

   > Accrued warranty—end of period | $5,152 | $3,505 | $2,101

2. `TSLA_FY2018_2018-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Note 2 – Summary of Significant Accounting Policies · table

   > Accrued warranty—end of period | $747,826 | $401,790 | $266,655

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 8 |
| recall@5 | 1.00 | 0.50 | 1.00 | 1.00 |
| recall@all | 1.00 | 0.50 | 1.00 | 1.00 |
| complete@all | 1 | 0 | 1 | 1 |
| average precision (lexical) | 1.00 | 0.50 | 1.00 | 0.42 |
| gold evidence first rank | #1: 1, #2: 2 | #1: –, #2: 2 | #1: 1, #2: 2 | #1: 3, #2: 4 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✗ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 0.00 | 1.00 | 1.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.50 | 0.50 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 2325 | 1250 | 6402 | 8183 |
| cost (USD) | 0.0004 | 0.0002 | 0.0223 | 0.0286 |
| latency (s) | 2.2 | 6.9 | 9.4 | 12.4 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Tesla’s accrued warranty liability at the end of fiscal year 2023 was **$5,152 million** [1], compared with **$747.826 million** at the end of fiscal year 2018 [2].
>
> So, the 2023 amount exceeded the 2018 amount by **$4,404.174 million** [1][2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2023_2023-12-31:336` | Item 8 › Note 2 – Summary of Significant Accounting Policies | ✓ | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| \| Accrued warranty—beginning of period \| $3,505 \| $2,101 \| $1,468 \| \| Warranty costs incurred \| (1,225) \| (803) \| (525) \| \| Net changes in liab… |
| 2 | `TSLA_FY2018_2018-12-31:464` | Item 8 › Note 2 – Summary of Significant Accounting Policies | ✓ | #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2018 \| 2017 \| 2016 \| \| Accrued warranty—beginning of period \| $401,790 \| $266,655 \| $180,754 \| \| Assumed warranty liability from acquisition \| — \| 4,737 \| 31,366 \| … |
| 3 | `TSLA_FY2023_2023-12-31:372` | Item 8 › Note 9 – Accrued Liabilities and Other |  |  | \| \| December 31, 2023 \| December 31, 2022 \| \|---\|---\|---\| \| Accrued purchases (1) \| $2,721 \| $2,747 \| \| Accrued warranty reserve, current portion \| 1,546 \| 1,025 \| \| Payroll and related costs \| 1,325 \| 1,026 \| \| Taxes pa… |
| 4 | `TSLA_FY2023_2023-12-31:371` | Item 8 › Note 9 – Accrued Liabilities and Other |  |  | Our accrued liabilities and other current liabilities consisted of the following (in millions): |
| 5 | `TSLA_FY2023_2023-12-31:283` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2023 \| 2022 \| \| Deferred revenue— beginning of period \| $2,913 \| $2,382 \| \| Additions \| 1,201 \| 1,178 \| \| Net changes in liability for pre-existing contracts \| 17 \| (67) … |
| 6 | `TSLA_FY2023_2023-12-31:375` | Item 8 › Note 10 – Other Long-Term Liabilities |  |  | \| \| December 31, 2023 \| December 31, 2022 \| \|---\|---\|---\| \| Operating lease liabilities \| $3,671 \| $2,164 \| \| Accrued warranty reserve \| 3,606 \| 2,480 \| \| Other non-current liabilities \| 876 \| 686 \| \| Total other long-te… |
| 7 | `TSLA_FY2018_2018-12-31:530` | Item 8 › Note 11 – Other Long-Term Liabilities |  |  | \| \| December 31, \| December 31, \| \|---\|---\|---\| \| \| 2018 \| 2017 \| \| Accrued warranty reserve \| $547,125 \| $276,289 \| \| Build-to-suit lease liability \| 1,662,017 \| 1,665,768 \| \| Deferred rent expense \| 59,252 \| 46,820 \| \|… |
| 8 | `TSLA_FY2023_2023-12-31:266` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| \| Accounts payable, accrued and other liabilities \| 2,605 \| 8,029 \| 5,367 \| \| Deferred revenue \| 1,532 \| 1,131 \| 793 \| \| Net cash provided by o… |
| 9 | `TSLA_FY2023_2023-12-31:265` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| \| Cash Flows from Operating Activities \| \| \| \| \| Net income \| $14,974 \| $12,587 \| $5,644 \| \| Adjustments to reconcile net income to net cash pr… |
| 10 | `TSLA_FY2018_2018-12-31:527` | Item 8 › Note 10 - Accrued Liabilities and Other |  |  | \| \| December 31, \| December 31, \| \|---\|---\|---\| \| \| 2018 \| 2017 \| \| Accrued purchases \| $394,216 \| $753,408 \| \| Payroll and related costs \| 448,836 \| 378,284 \| \| Taxes payable \| 348,663 \| 185,807 \| \| Financing obligation… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2023_2023-12-31:336`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 2 – Summary of Significant Accounting Policies (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2023 | 2022 | 2021 |
| Accrued warranty—beginning of period | $3,505 | $2,101 | $1,468 |
| Warranty costs incurred | (1,225) | (803) | (525) |
| Net changes in liability for pre-existing warranties, including expirations and foreign exchange impact | 539 | 522 | 102 |
| Provision for warranty | 2,333 | 1,685 | 1,056 |
| Accrued warranty—end of period | $5,152 | $3,505 | $2,101 |
````

**#2 `TSLA_FY2018_2018-12-31:464`** (cited, gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 2 – Summary of Significant Accounting Policies (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2018 | 2017 | 2016 |
| Accrued warranty—beginning of period | $401,790 | $266,655 | $180,754 |
| Assumed warranty liability from acquisition | — | 4,737 | 31,366 |
| Warranty costs incurred | (209,124) | (122,510) | (79,147) |
| Net changes in liability for pre-existing warranties, including expirations and foreign exchange impact | (26,294) | 4,342 | (20,084) |
| Additional warranty accrued from adoption of the new revenue standard | 37,139 | — | — |
| Provision for warranty | 544,315 | 248,566 | 153,766 |
| Accrued warranty—end of period | $747,826 | $401,790 | $266,655 |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 3.

**Generated answer**

> Tesla’s total accrued warranty was $5,152 million at the end of FY2023 [1].  
> At the end of FY2018, accrued warranty was $747.826 million current [2] plus $547.125 million noncurrent [5], totaling $1,294.951 million.
>
> Difference: $5,152 million − $1,294.951 million = $3,857.049 million.
>
> So, Tesla’s accrued warranty liability exceeded the FY2018 amount by about $3,857.0 million [1][2][5].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2023_2023-12-31:246` | Item 8 › Critical Audit Matters | ✓ |  | As described in Note 2 to the consolidated financial statements, total accrued warranty, which primarily relates to the automotive segment, was $5,152 million as of December 31, 2023. The Company provides a manufacturer’… |
| 2 | `TSLA_FY2018_2018-12-31:464` | Item 8 › Note 2 – Summary of Significant Accounting Policies | ✓ | #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2018 \| 2017 \| 2016 \| \| Accrued warranty—beginning of period \| $401,790 \| $266,655 \| $180,754 \| \| Assumed warranty liability from acquisition \| — \| 4,737 \| 31,366 \| … |
| 3 | `TSLA_FY2023_2023-12-31:372` | Item 8 › Note 9 – Accrued Liabilities and Other |  |  | \| \| December 31, 2023 \| December 31, 2022 \| \|---\|---\|---\| \| Accrued purchases (1) \| $2,721 \| $2,747 \| \| Accrued warranty reserve, current portion \| 1,546 \| 1,025 \| \| Payroll and related costs \| 1,325 \| 1,026 \| \| Taxes pa… |
| 4 | `TSLA_FY2018_2018-12-31:689` | Item 8 › Note 23 – Restructuring and Other |  |  | In October 2018, a final court order was entered approving the terms of a settlement in connection with the SEC’s legal actions relating to Elon Musk’s prior consideration during the third quarter of 2018 of a take-priva… |
| 5 | `TSLA_FY2018_2018-12-31:530` | Item 8 › Note 11 – Other Long-Term Liabilities | ✓ |  | \| \| December 31, \| December 31, \| \|---\|---\|---\| \| \| 2018 \| 2017 \| \| Accrued warranty reserve \| $547,125 \| $276,289 \| \| Build-to-suit lease liability \| 1,662,017 \| 1,665,768 \| \| Deferred rent expense \| 59,252 \| 46,820 \| \|… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2023_2023-12-31:246`** (cited)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Critical Audit Matters
As described in Note 2 to the consolidated financial statements, total accrued warranty, which primarily relates to the automotive segment, was $5,152 million as of December 31, 2023. The Company provides a manufacturer’s warranty on all new and used Tesla vehicles. A warranty reserve is accrued for these products sold, which includes management’s best estimate of the projected costs to repair or replace items under warranty and recalls if identified. These estimates are based on actual claims incurred to date and an estimate of the nature, frequency and costs of future claims. The principal considerations for our determination that performing procedures relating to the automotive warranty reserve is a critical audit matter are the significant judgment by management in determining the automotive warranty reserve for certain Tesla vehicle models; this in turn led to significant auditor judgment, subjectivity, and effort in performing procedures to evaluate management’s significant assumptions related to the nature, frequency and costs of future claims for certain Tesla vehicle models, and the audit effort involved the use of professionals with specialized skill and knowledge.
````

**#2 `TSLA_FY2018_2018-12-31:464`** (cited, gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 2 – Summary of Significant Accounting Policies (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2018 | 2017 | 2016 |
| Accrued warranty—beginning of period | $401,790 | $266,655 | $180,754 |
| Assumed warranty liability from acquisition | — | 4,737 | 31,366 |
| Warranty costs incurred | (209,124) | (122,510) | (79,147) |
| Net changes in liability for pre-existing warranties, including expirations and foreign exchange impact | (26,294) | 4,342 | (20,084) |
| Additional warranty accrued from adoption of the new revenue standard | 37,139 | — | — |
| Provision for warranty | 544,315 | 248,566 | 153,766 |
| Accrued warranty—end of period | $747,826 | $401,790 | $266,655 |
````

**#5 `TSLA_FY2018_2018-12-31:530`** (cited)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 11 – Other Long-Term Liabilities (table)
|  | December 31, | December 31, |
|---|---|---|
|  | 2018 | 2017 |
| Accrued warranty reserve | $547,125 | $276,289 |
| Build-to-suit lease liability | 1,662,017 | 1,665,768 |
| Deferred rent expense | 59,252 | 46,820 |
| Financing obligation | 50,383 | 67,929 |
| Liability for receipts from an investor | — | 29,713 |
| Sales return reserve | 84,143 | — |
| Other noncurrent liabilities | 307,483 | 356,451 |
| Total other long-term liabilities | $2,710,403 | $2,442,970 |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 2.

**Generated answer**

> Tesla’s accrued warranty liability was $5,152 million at the end of fiscal year 2023 and $747,826 thousand ($747.826 million) at the end of fiscal year 2018, so the 2023 balance exceeded the 2018 balance by $4,404.174 million. [TSLA FY2023, Item 8, TSLA_FY2023_2023-12-31:336] [TSLA FY2018, Item 8, TSLA_FY2018_2018-12-31:464]
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 747.826, 4,404.174; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2023_2023-12-31:336` | Item 8 › Note 2 – Summary of Significant Accounting Policies | ✓ | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| \| Accrued warranty—beginning of period \| $3,505 \| $2,101 \| $1,468 \| \| Warranty costs incurred \| (1,225) \| (803) \| (525) \| \| Net changes in liab… |
| 2 | `TSLA_FY2018_2018-12-31:464` | Item 8 › Note 2 – Summary of Significant Accounting Policies | ✓ | #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2018 \| 2017 \| 2016 \| \| Accrued warranty—beginning of period \| $401,790 \| $266,655 \| $180,754 \| \| Assumed warranty liability from acquisition \| — \| 4,737 \| 31,366 \| … |
| 3 | `TSLA_FY2023_2023-12-31:335` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | from our suppliers, we record receivables for the contractually obligated amounts on the consolidated balance sheets as a component of Prepaid expenses and other current assets for the current portion and as Other non-cu… |
| 4 | `TSLA_FY2023_2023-12-31:194` | Item 7 › Critical Accounting Policies and Estimates |  |  | from our suppliers, we record receivables for the contractually obligated amounts on the consolidated balance sheets as a component of Prepaid expenses and other current assets for the current portion and as Other non-cu… |
| 5 | `TSLA_FY2018_2018-12-31:463` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | included within other long-term liabilities on the consolidated balance sheet. Due to the adoption of the new revenue standard, automotive sales with resale value guarantees that were previously recorded within operating… |
| 6 | `TSLA_FY2023_2023-12-31:373` | Item 8 › Note 9 – Accrued Liabilities and Other |  |  | (1)Accrued purchases primarily reflects receipts of goods and services for which we had not yet been invoiced. As we are invoiced for these goods and services, this balance will reduce and accounts payable will increase.… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2023_2023-12-31:336`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 2 – Summary of Significant Accounting Policies (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2023 | 2022 | 2021 |
| Accrued warranty—beginning of period | $3,505 | $2,101 | $1,468 |
| Warranty costs incurred | (1,225) | (803) | (525) |
| Net changes in liability for pre-existing warranties, including expirations and foreign exchange impact | 539 | 522 | 102 |
| Provision for warranty | 2,333 | 1,685 | 1,056 |
| Accrued warranty—end of period | $5,152 | $3,505 | $2,101 |
````

**#2 `TSLA_FY2018_2018-12-31:464`** (cited, gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 2 – Summary of Significant Accounting Policies (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2018 | 2017 | 2016 |
| Accrued warranty—beginning of period | $401,790 | $266,655 | $180,754 |
| Assumed warranty liability from acquisition | — | 4,737 | 31,366 |
| Warranty costs incurred | (209,124) | (122,510) | (79,147) |
| Net changes in liability for pre-existing warranties, including expirations and foreign exchange impact | (26,294) | 4,342 | (20,084) |
| Additional warranty accrued from adoption of the new revenue standard | 37,139 | — | — |
| Provision for warranty | 544,315 | 248,566 | 153,766 |
| Accrued warranty—end of period | $747,826 | $401,790 | $266,655 |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 4, verified 2, ungrounded 2, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 747.826, 4,404.174

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Tesla’s accrued warranty liability was $5,152 million at the end of fiscal year 2023 and $747,826 thousand ($747.826 million) at the end of fiscal year 2018, so the 2023 balance exceeded the 2018 balance by $4,404.174 million. [TSLA FY2023, Item 8, TSLA_FY2023_2023-12-31:336] [TSLA FY2018, Item 8, TSLA_FY2018_2018-12-31:464] | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 3.

**Generated answer**

> Tesla’s accrued warranty liability at the end of fiscal year 2023 was $5,152 million, and at the end of fiscal year 2018 it was $747,826 thousand, or $747.826 million. [TSLA FY2023, Item 8, TSLA_FY2023_2023-12-31:336] [TSLA FY2018, Item 8, TSLA_FY2018_2018-12-31:463] [TSLA FY2018, Item 8, TSLA_FY2018_2018-12-31:464]
>
> Therefore, the 2023 accrued warranty liability exceeded the 2018 amount by $4,404.174 million. [TSLA FY2023, Item 8, TSLA_FY2023_2023-12-31:336] [TSLA FY2018, Item 8, TSLA_FY2018_2018-12-31:463] [TSLA FY2018, Item 8, TSLA_FY2018_2018-12-31:464]
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 747.826, 4,404.174; 2 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-TSLA-2018` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2018,2018-12-31,21461268000,-976091000,-388073000,29739614000,… |
| 2 | `F-TSLA-2023` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2023,2023-12-31,96773000000,14997000000,8891000000,10661800000… |
| 3 | `TSLA_FY2023_2023-12-31:336` | Item 8 › Note 2 – Summary of Significant Accounting Policies | ✓ | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| \| Accrued warranty—beginning of period \| $3,505 \| $2,101 \| $1,468 \| \| Warranty costs incurred \| (1,225) \| (803) \| (525) \| \| Net changes in liab… |
| 4 | `TSLA_FY2018_2018-12-31:464` | Item 8 › Note 2 – Summary of Significant Accounting Policies | ✓ | #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2018 \| 2017 \| 2016 \| \| Accrued warranty—beginning of period \| $401,790 \| $266,655 \| $180,754 \| \| Assumed warranty liability from acquisition \| — \| 4,737 \| 31,366 \| … |
| 5 | `TSLA_FY2023_2023-12-31:335` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | from our suppliers, we record receivables for the contractually obligated amounts on the consolidated balance sheets as a component of Prepaid expenses and other current assets for the current portion and as Other non-cu… |
| 6 | `TSLA_FY2023_2023-12-31:194` | Item 7 › Critical Accounting Policies and Estimates |  |  | from our suppliers, we record receivables for the contractually obligated amounts on the consolidated balance sheets as a component of Prepaid expenses and other current assets for the current portion and as Other non-cu… |
| 7 | `TSLA_FY2018_2018-12-31:463` | Item 8 › Note 2 – Summary of Significant Accounting Policies | ✓ |  | included within other long-term liabilities on the consolidated balance sheet. Due to the adoption of the new revenue standard, automotive sales with resale value guarantees that were previously recorded within operating… |
| 8 | `TSLA_FY2023_2023-12-31:373` | Item 8 › Note 9 – Accrued Liabilities and Other |  |  | (1)Accrued purchases primarily reflects receipts of goods and services for which we had not yet been invoiced. As we are invoiced for these goods and services, this balance will reduce and accounts payable will increase.… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `TSLA_FY2023_2023-12-31:336`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 2 – Summary of Significant Accounting Policies (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2023 | 2022 | 2021 |
| Accrued warranty—beginning of period | $3,505 | $2,101 | $1,468 |
| Warranty costs incurred | (1,225) | (803) | (525) |
| Net changes in liability for pre-existing warranties, including expirations and foreign exchange impact | 539 | 522 | 102 |
| Provision for warranty | 2,333 | 1,685 | 1,056 |
| Accrued warranty—end of period | $5,152 | $3,505 | $2,101 |
````

**#4 `TSLA_FY2018_2018-12-31:464`** (cited, gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 2 – Summary of Significant Accounting Policies (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2018 | 2017 | 2016 |
| Accrued warranty—beginning of period | $401,790 | $266,655 | $180,754 |
| Assumed warranty liability from acquisition | — | 4,737 | 31,366 |
| Warranty costs incurred | (209,124) | (122,510) | (79,147) |
| Net changes in liability for pre-existing warranties, including expirations and foreign exchange impact | (26,294) | 4,342 | (20,084) |
| Additional warranty accrued from adoption of the new revenue standard | 37,139 | — | — |
| Provision for warranty | 544,315 | 248,566 | 153,766 |
| Accrued warranty—end of period | $747,826 | $401,790 | $266,655 |
````

**#7 `TSLA_FY2018_2018-12-31:463`** (cited)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 2 – Summary of Significant Accounting Policies
included within other long-term liabilities on the consolidated balance sheet. Due to the adoption of the new revenue standard, automotive sales with resale value guarantees that were previously recorded within operating lease assets require a corresponding warranty accrual, which is included in the table below. Warranty expense is recorded as a component of cost of revenues in the consolidated statements of operations. Accrued warranty activity consisted of the following (in thousands):
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 4, verified 2, ungrounded 2, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 747.826, 4,404.174

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Tesla’s accrued warranty liability at the end of fiscal year 2023 was $5,152 million, and at the end of fiscal year 2018 it was $747,826 thousand, or $747.826 million. [TSLA FY2023, Item 8, TSLA_FY2023_2023-12-31:336] [TSLA FY2018, Item 8, TSLA_FY2018_2018-12-31:463] [TSLA FY2018, Item 8, TSLA_FY2018_2018-12-31:464] | None |  |
| Therefore, the 2023 accrued warranty liability exceeded the 2018 amount by $4,404.174 million. [TSLA FY2023, Item 8, TSLA_FY2023_2023-12-31:336] [TSLA FY2018, Item 8, TSLA_FY2018_2018-12-31:463] [TSLA FY2018, Item 8, TSLA_FY2018_2018-12-31:464] | None |  |

</details>
