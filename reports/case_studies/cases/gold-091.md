# gold-091: Cross-company table

[← all cases](../README.md) · company: AMAZON COM INC; JOHNSON & JOHNSON (AMZN, JNJ) · fiscal year: 2019 · recipe `cross_company_table` · hop `multi` · answer type `numeric` · scope `cross_company` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> According to their fiscal year 2019 10-Ks, how many millions of dollars more debt principal was Amazon scheduled to repay in 2020 than Johnson & Johnson?

**Gold answer**

> $207 million

**Program**: `subtract(1307, 1100)` → `207.0`

**Gold numbers** (RQ2 numeric_accuracy targets): $207 million

**Gold evidence**

1. `AMZN_FY2019_2019-12-31` · Item 8. Financial Statements and Supplementary Data › Note 6 — DEBT · table

   > 2020 | $1,307

2. `JNJ_FY2019_2019-12-29` · Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OPERATIONS AND FINANCIAL CONDITION › Contractual Obligations and Commitments · table

   > 2020 | $528 | 1,100 | 886 | 103 | 215 | 2,832

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 6 | 5 | 17 | 8 |
| recall@5 | 0.00 | 0.00 | 0.50 | 0.00 |
| recall@all | 0.00 | 0.00 | 0.50 | 0.50 |
| complete@all | 0 | 0 | 0 | 0 |
| average precision (lexical) | 0.00 | 0.00 | 0.25 | 0.17 |
| gold evidence first rank | #1: –, #2: – | #1: –, #2: – | #1: 4, #2: – | #1: 6, #2: – |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✗ | ✓ | ✗ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 1.00 | 0.00 |
| citation precision | – | – | 1.00 | 1.00 |
| citation recall | – | – | 0.50 | 0.50 |
| citation F1 | – | – | 0.67 | 0.67 |
| has a citation | 0 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.33 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 1 |
| tokens | 1316 | 1113 | 21617 | 8293 |
| cost (USD) | 0.0002 | 0.0002 | 0.0705 | 0.0272 |
| latency (s) | 1.9 | 6.3 | 23.8 | 9.9 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 6, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2019_2019-12-29:161` | Item 7 › Financing and Market Risk |  |  | The Company has access to substantial sources of funds at numerous banks worldwide. In September 2019, the Company secured a new 364-day Credit Facility. Total credit available to the Company approximates $10 billion, wh… |
| 2 | `JNJ_FY2019_2019-12-29:214` | Item 8 › (Dollars in Millions) (Note 1) |  |  | \| \| 2019 \| 2018 \| 2017 \| \|---\|---\|---\|---\| \| Repayment of short-term debt \| (100) \| (2,479) \| (1,330) \| \| Proceeds from long-term debt, net of issuance costs \| 3 \| 5 \| 8,992 \| \| Repayment of long-term debt \| (2,823) \| (1… |
| 3 | `JNJ_FY2019_2019-12-29:75` | Item 1B |  |  | Not applicable. |
| 4 | `JNJ_FY2019_2019-12-29:297` | Item 8 › Reclassification |  |  | \| Subtotal \| 27,594 \| (4) \| 3.19% \| (1) \| 30,320 \| (4) \| 3.19 \| (1) \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Less current portion \| 1,100 \| \| \| \| 2,636 \| \| \| \| \| Total long-term debt \| $26,494 \| \| \| \| 27,684 \| \| \| \| |
| 5 | `JNJ_FY2019_2019-12-29:565` | Item 9B |  |  | Not applicable. |
| 6 | `JNJ_FY2019_2019-12-29:155` | Item 7 › Liquidity & Cash Flows |  |  | As of December 29, 2019, the Company's notes payable and long-term debt was in excess of cash, cash equivalents and marketable securities. As of December 29, 2019, the net debt position was $8.4 billion as compared to th… |

RQ2 citation match (section level): `no citations`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JNJ_FY2019_2019-12-29:510` | Item 8 › GOVERNMENT PROCEEDINGS |  |  | 2019. In January 2020, the court found in favor of the state and awarded the state civil penalties of approximately $344 million. The Company intends to appeal when further proceedings are concluded in the trial court. S… |
| 2 | `JNJ_FY2019_2019-12-29:299` | Item 8 › Reclassification |  |  | Throughout 2019, the Company continued to have access to liquidity through the commercial paper market. Short-term borrowings and the current portion of long-term debt amounted to approximately $1.2 billion at the end of… |
| 3 | `JNJ_FY2019_2019-12-29:214` | Item 8 › (Dollars in Millions) (Note 1) |  |  | \| \| 2019 \| 2018 \| 2017 \| \|---\|---\|---\|---\| \| Repayment of short-term debt \| (100) \| (2,479) \| (1,330) \| \| Proceeds from long-term debt, net of issuance costs \| 3 \| 5 \| 8,992 \| \| Repayment of long-term debt \| (2,823) \| (1… |
| 4 | `JNJ_FY2019_2019-12-29:2` | JOHNSON & JOHNSON |  |  | (Exact name of registrant as specified in its charter) |
| 5 | `JNJ_FY2019_2019-12-29:298` | Item 8 › Reclassification |  |  | (1) Weighted average effective rate. (2) Translation rate at December 29, 2019. (3) Translation rate at December 30, 2018. (4) The excess of the fair value over the carrying value of debt was $3.0 billion in 2019 and $0.… |

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 17, cited: 2.

**Generated answer**

> Amazon was scheduled to repay $1,307 million of debt principal in 2020, while Johnson & Johnson reported $1,100 million as the current portion of long-term debt at the end of 2019. [AMZN FY2019, Item 8, AMZN_FY2019_2019-12-31:288] [JNJ FY2019, Item 8, JNJ_FY2019_2019-12-29:297]
>
> Therefore, Amazon was scheduled to repay $207 million more debt principal in 2020 than Johnson & Johnson. [AMZN FY2019, Item 8, AMZN_FY2019_2019-12-31:288] [JNJ FY2019, Item 8, JNJ_FY2019_2019-12-29:297]
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 207; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AMZN_FY2019_2019-12-31:291` | Item 8 › Commitments |  |  | \| \| Year Ended December 31, \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| 2020 \| 2021 \| 2022 \| 2023 \| 2024 \| Thereafter \| Total \| \| Debt principal and interest \| $2,202 \| $2,009 \| $2,603 \| $2,273 \| $4,084 \| $26,019… |
| 2 | `AMZN_FY2019_2019-12-31:121` | Item 7 › Liquidity and Capital Resources |  |  | Cash provided by (used in) financing activities was $(7.7) billion and $(10.1) billion in 2018 and 2019. Cash outflows from financing activities result from principal repayments of finance leases and financing obligation… |
| 3 | `AMZN_FY2019_2019-12-31:151` | Item 7 › Non-GAAP Financial Measures |  |  | ___________________ (1) For the twelve months ended December 31, 2019, this amount relates to equipment included in “Property and equipment acquired under finance leases” of $13,723 million. Amounts for 2018 have not bee… |
| 4 | `AMZN_FY2019_2019-12-31:288` | Item 8 › Note 6 — DEBT | ✓ | #1 | \| Year Ended December 31, \| \| \|---\|---\| \| 2020 \| $1,307 \| \| 2021 \| 1,141 \| \| 2022 \| 1,773 \| \| 2023 \| 1,510 \| \| 2024 \| 3,339 \| \| Thereafter \| 15,750 \| \| \| $24,820 \| |
| 5 | `AMZN_FY2019_2019-12-31:148` | Item 7 › Non-GAAP Financial Measures |  |  | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2018 \| 2019 \| \| Net cash provided by (used in) operating activities \| $30,723 \| $38,514 \| \| Purchases of property and equipment, net of proceeds from sales and incentives… |
| 6 | `AMZN_FY2019_2019-12-31:282` | Item 8 › Note 6 — DEBT |  |  | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2018 \| 2019 \| \| 2.600% Notes due on December 5, 2019 \| 1,000 \| — \| \| 1.900% Notes due on August 21, 2020 (3) \| 1,000 \| 1,000 \| \| 3.300% Notes due on December 5, 2021 (2) \| 1,000 \| 1… |
| 7 | `JNJ_FY2019_2019-12-29:199` | Item 8 › (Dollars in Millions Except Share and Per Share Amounts) (Note 1) |  |  | \| \| 2019 \| 2018 \| \|---\|---\|---\| \| Accounts payable \| 8,544 \| 7,537 \| \| Accrued liabilities \| 9,715 \| 7,601 \| \| Accrued rebates, returns and promotions \| 10,883 \| 9,380 \| \| Accrued compensation and employee related obliga… |
| 8 | `JNJ_FY2019_2019-12-29:198` | Item 8 › (Dollars in Millions Except Share and Per Share Amounts) (Note 1) |  |  | \| \| 2019 \| 2018 \| \|---\|---\|---\| \| Assets \| \| \| \| Current assets \| \| \| \| Cash and cash equivalents (Notes 1 and 2) \| $17,305 \| 18,107 \| \| Marketable securities (Notes 1 and 2) \| 1,982 \| 1,580 \| \| Accounts receivable trade… |
| 9 | `JNJ_FY2019_2019-12-29:197` | Item 8 |  |  | \| Index to Audited Consolidated Financial Statements \| \| \|---\|---\| \| 35 \| Consolidated Balance Sheets \| \| 36 \| Consolidated Statements of Earnings \| \| 37 \| Consolidated Statements of Comprehensive Income \| \| 38 \| Consoli… |
| 10 | `JNJ_FY2019_2019-12-29:218` | Item 8 › NOTES TO CONSOLIDATED FINANCIAL STATEMENTS |  |  | 1. Summary of Significant Accounting Policies |
| 11 | `JNJ_FY2019_2019-12-29:293` | Item 8 › Reclassification |  |  | \| (Dollars in Millions) \| 2019 \| \| Effective Rate % \| 2018 \| \| Effective Rate % \| \|---\|---\|---\|---\|---\|---\|---\| \| 4.75% Notes due 2019 (1B Euro 1.1096)(2)/(1B Euro 1.14)(3) \| $— \| \| — \| 1,139 \| (2) \| 5.83 \| \| 1.875% Note… |
| 12 | `JNJ_FY2019_2019-12-29:164` | Item 7 › Contractual Obligations and Commitments |  |  | For tax matters, see Note 8 to the Consolidated Financial Statements. For other retirement plan and post-employment medical benefit information, see Note 10 to the Consolidated Financial Statements. The table does not in… |
| 13 | `JNJ_FY2019_2019-12-29:299` | Item 8 › Reclassification |  |  | Throughout 2019, the Company continued to have access to liquidity through the commercial paper market. Short-term borrowings and the current portion of long-term debt amounted to approximately $1.2 billion at the end of… |
| 14 | `JNJ_FY2019_2019-12-29:297` | Item 8 › Reclassification | ✓ |  | \| Subtotal \| 27,594 \| (4) \| 3.19% \| (1) \| 30,320 \| (4) \| 3.19 \| (1) \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Less current portion \| 1,100 \| \| \| \| 2,636 \| \| \| \| \| Total long-term debt \| $26,494 \| \| \| \| 27,684 \| \| \| \| |
| 15 | `JNJ_FY2019_2019-12-29:214` | Item 8 › (Dollars in Millions) (Note 1) |  |  | \| \| 2019 \| 2018 \| 2017 \| \|---\|---\|---\|---\| \| Repayment of short-term debt \| (100) \| (2,479) \| (1,330) \| \| Proceeds from long-term debt, net of issuance costs \| 3 \| 5 \| 8,992 \| \| Repayment of long-term debt \| (2,823) \| (1… |
| 16 | `JNJ_FY2019_2019-12-29:278` | Item 8 › Reclassification |  |  | \| Line item in the Consolidated Balance Sheet in which the hedged item is included \| Carrying Amount of the Hedged Liability \| \| Cumulative Amount of Fair Value Hedging Adjustment Included in the Carrying Amount of the H… |
| 17 | `JNJ_FY2019_2019-12-29:298` | Item 8 › Reclassification |  |  | (1) Weighted average effective rate. (2) Translation rate at December 29, 2019. (3) Translation rate at December 30, 2018. (4) The excess of the fair value over the carrying value of debt was $3.0 billion in 2019 and $0.… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#4 `AMZN_FY2019_2019-12-31:288`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Note 6 — DEBT (table)
| Year Ended December 31, |  |
|---|---|
| 2020 | $1,307 |
| 2021 | 1,141 |
| 2022 | 1,773 |
| 2023 | 1,510 |
| 2024 | 3,339 |
| Thereafter | 15,750 |
|  | $24,820 |
````

**#14 `JNJ_FY2019_2019-12-29:297`** (cited)

````text
Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Reclassification (table)
| Subtotal | 27,594 | (4) | 3.19% | (1) | 30,320 | (4) | 3.19 | (1) |
|---|---|---|---|---|---|---|---|---|
| Less current portion | 1,100 |  |  |  | 2,636 |  |  |  |
| Total long-term debt | $26,494 |  |  |  | 27,684 |  |  |  |
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 8'), ('JNJ', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 2, ungrounded 1, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 207

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Amazon was scheduled to repay $1,307 million of debt principal in 2020, while Johnson & Johnson reported $1,100 million as the current portion of long-term debt at the end of 2019. [AMZN FY2019, Item 8, AMZN_FY2019_2019-12-31:288] [JNJ FY2019, Item 8, JNJ_FY2019_2019-12-29:297] | None |  |
| Therefore, Amazon was scheduled to repay $207 million more debt principal in 2020 than Johnson & Johnson. [AMZN FY2019, Item 8, AMZN_FY2019_2019-12-31:288] [JNJ FY2019, Item 8, JNJ_FY2019_2019-12-29:297] | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 1.

**Generated answer**

> Amazon’s FY2019 10-K shows debt principal due in 2020 of $1,307 million [AMZN FY2019, Item 8, AMZN_FY2019_2019-12-31:288]. Johnson & Johnson’s FY2019 10-K debt principal due in 2020 is not disclosed in the provided evidence.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-AMZN-2019` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2019,2019-12-31,280522000000,11588000000,14541000000,225248000… |
| 2 | `F-JNJ-2019` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2019,2019-12-29,82059000000,15119000000,,157728000000,98257000… |
| 3 | `AMZN_FY2019_2019-12-31:291` | Item 8 › Commitments |  |  | \| \| Year Ended December 31, \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| 2020 \| 2021 \| 2022 \| 2023 \| 2024 \| Thereafter \| Total \| \| Debt principal and interest \| $2,202 \| $2,009 \| $2,603 \| $2,273 \| $4,084 \| $26,019… |
| 4 | `AMZN_FY2019_2019-12-31:178` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2017 \| 2018 \| 2019 \| \| Unearned revenue \| 738 \| 1,151 \| 1,711 \| \| Net cash provided by (used in) operating activities \| 18,365 \| 30,723 \| 38,514 \| \| INVESTING ACTIV… |
| 5 | `AMZN_FY2019_2019-12-31:121` | Item 7 › Liquidity and Capital Resources |  |  | Cash provided by (used in) financing activities was $(7.7) billion and $(10.1) billion in 2018 and 2019. Cash outflows from financing activities result from principal repayments of finance leases and financing obligation… |
| 6 | `AMZN_FY2019_2019-12-31:288` | Item 8 › Note 6 — DEBT | ✓ | #1 | \| Year Ended December 31, \| \| \|---\|---\| \| 2020 \| $1,307 \| \| 2021 \| 1,141 \| \| 2022 \| 1,773 \| \| 2023 \| 1,510 \| \| 2024 \| 3,339 \| \| Thereafter \| 15,750 \| \| \| $24,820 \| |
| 7 | `AMZN_FY2019_2019-12-31:282` | Item 8 › Note 6 — DEBT |  |  | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2018 \| 2019 \| \| 2.600% Notes due on December 5, 2019 \| 1,000 \| — \| \| 1.900% Notes due on August 21, 2020 (3) \| 1,000 \| 1,000 \| \| 3.300% Notes due on December 5, 2021 (2) \| 1,000 \| 1… |
| 8 | `AMZN_FY2019_2019-12-31:148` | Item 7 › Non-GAAP Financial Measures |  |  | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2018 \| 2019 \| \| Net cash provided by (used in) operating activities \| $30,723 \| $38,514 \| \| Purchases of property and equipment, net of proceeds from sales and incentives… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#6 `AMZN_FY2019_2019-12-31:288`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Note 6 — DEBT (table)
| Year Ended December 31, |  |
|---|---|
| 2020 | $1,307 |
| 2021 | 1,141 |
| 2022 | 1,773 |
| 2023 | 1,510 |
| 2024 | 3,339 |
| Thereafter | 15,750 |
|  | $24,820 |
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 1, verified 1, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Amazon’s FY2019 10-K shows debt principal due in 2020 of $1,307 million [AMZN FY2019, Item 8, AMZN_FY2019_2019-12-31:288]. | None |  |
| Johnson & Johnson’s FY2019 10-K debt principal due in 2020 is not disclosed in the provided evidence. | supported | The retrieved evidence includes no Johnson & Johnson debt maturity schedule or 2020 debt principal due amount, so that information is not disclosed here. |

</details>
