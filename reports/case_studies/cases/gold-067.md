# gold-067: Cross-year table

[← all cases](../README.md) · company: NVIDIA CORP (NVDA) · fiscal year: 2024 · recipe `cross_year_table` · hop `multi` · answer type `numeric` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> By what percentage did NVIDIA's research and development expenses grow from fiscal year 2018 to fiscal year 2024?

**Gold answer**

> 382.75%

**Program**: `subtract(8675, 1797), divide(#0, 1797), multiply(#1, 100)` → `382.7490261547023`

**Gold numbers** (RQ2 numeric_accuracy targets): 382.75%

**Gold evidence**

1. `NVDA_FY2024_2024-01-28` · Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations › Operating Expenses · table

   > Research and development expenses | $8,675 | $7,339 | $1,336 | 18%

2. `NVDA_FY2018_2018-01-28` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Operating Expenses · table

   > | Research and development expenses | $1,797 | $1,463 | $334 | 23% | $1,463 | $1,331 | $132 | 10% |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 12 | 8 |
| recall@5 | 0.00 | 0.00 | 1.00 | 0.00 |
| recall@all | 0.00 | 0.00 | 1.00 | 1.00 |
| complete@all | 0 | 0 | 1 | 1 |
| average precision (lexical) | 0.00 | 0.00 | 0.33 | 0.23 |
| gold evidence first rank | #1: –, #2: – | #1: –, #2: – | #1: 5, #2: 4 | #1: 7, #2: 6 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✗ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 1.00 | 1.00 |
| citation precision | 0.50 | – | 1.00 | 1.00 |
| citation recall | 1.00 | – | 1.00 | 1.00 |
| citation F1 | 0.67 | – | 1.00 | 1.00 |
| has a citation | 1 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 2 | 1 |
| tokens | 1948 | 1219 | 15066 | 5103 |
| cost (USD) | 0.0004 | 0.0002 | 0.0472 | 0.0172 |
| latency (s) | 2.4 | 6.4 | 13.3 | 7.1 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 3.

**Generated answer**

> The provided context does not include NVIDIA’s fiscal year 2024 research and development expense amount, so the exact growth percentage from fiscal year 2018 to fiscal year 2024 cannot be calculated from the context.
>
> What is in the context:
> - Fiscal year 2018 R&D expense was **$1.80 billion** [2].
> - For fiscal year 2024, the context only says R&D expenses increased, but does **not** give the dollar amount [4][8].
>
> So, the percentage growth from 2018 to 2024 is **not available in the provided context**. [2][4][8]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2018_2018-01-28:172` | Item 7 › Research and Development |  |  | Research and development expenses increased by 23% in fiscal year 2018 compared to fiscal year 2017 and increased 10% in fiscal year 2017 compared to fiscal year 2016, driven primarily by employee additions and increases… |
| 2 | `NVDA_FY2018_2018-01-28:51` | Item 1 › Table of Contents | ✓ |  | As of January 28, 2018, we had 8,191 full-time employees engaged in research and development. During fiscal years 2018, 2017 and 2016, we incurred research and development expenses of $1.80 billion, $1.46 billion, and $1… |
| 3 | `NVDA_FY2024_2024-01-28:200` | Item 7 › Fiscal Year 2024 Summary |  |  | We specialize in markets where our computing platforms can provide tremendous acceleration for applications. These platforms incorporate processors, interconnects, software, algorithms, systems, and services to deliver u… |
| 4 | `NVDA_FY2024_2024-01-28:223` | Item 7 › Operating Expenses | ✓ |  | The increase in research and development expenses and sales, general and administrative expenses for fiscal year 2024 was primarily driven by compensation and benefits, including stock-based compensation, reflecting empl… |
| 5 | `NVDA_FY2018_2018-01-28:136` | Item 7 › Fiscal Year 2018 Summary |  |  | Revenue for fiscal year 2018 grew 41% to $9.71 billion, reflecting broad growth in each of our market platforms - gaming, professional visualization, datacenter, and automotive. GPU business revenue was $8.14 billion, up… |
| 6 | `NVDA_FY2024_2024-01-28:455` | Item 15 › Notes to the Consolidated Financial Statements |  |  | Revenue from sales to customers outside of the United States accounted for 56%, 69%, and 84% of total revenue for fiscal years 2024, 2023, and 2022, respectively. The increase in revenue to the United States for fiscal y… |
| 7 | `NVDA_FY2024_2024-01-28:397` | Item 15 › Notes to the Consolidated Financial Statements |  |  | (1)In fiscal years 2024 and 2023, we recorded an expense of approximately $1.4 billion and $1.1 billion, respectively, in cost of revenue for inventory purchase obligations in excess of our current demand projections, su… |
| 8 | `NVDA_FY2024_2024-01-28:201` | Item 7 › Fiscal Year 2024 Summary | ✓ |  | Gross margin increased in fiscal year 2024, primarily driven by Data Center revenue growth and lower net inventory provisions as a percentage of revenue. Operating expenses increased for fiscal year 2024, driven by growt… |
| 9 | `NVDA_FY2024_2024-01-28:219` | Item 7 › Operating Income by Reportable Segments |  |  | Compute & Networking revenue – The year-on-year increase was due to higher Data Center revenue. Compute grew 266% due to higher shipments of the NVIDIA Hopper GPU computing platform for the training and inference of LLMs… |
| 10 | `NVDA_FY2024_2024-01-28:203` | Item 7 › Market Platform Highlights |  |  | Gaming revenue for fiscal year 2024 was $10.4 billion, up 15% from fiscal year 2023. In Gaming, we launched the GeForce RTX 4060 and 4070 GPUs based on the NVIDIA Ada Lovelace architecture. We announced NVIDIA Avatar Clo… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `NVDA_FY2018_2018-01-28:51`** (cited)

````text
ITEM 1. BUSINESS > Table of Contents
As of January 28, 2018, we had 8,191 full-time employees engaged in research and development. During fiscal years 2018, 2017 and 2016, we incurred research and development expenses of $1.80 billion, $1.46 billion, and $1.33 billion, respectively.
````

**#4 `NVDA_FY2024_2024-01-28:223`** (cited)

````text
Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations > Operating Expenses
The increase in research and development expenses and sales, general and administrative expenses for fiscal year 2024 was primarily driven by compensation and benefits, including stock-based compensation, reflecting employee growth and compensation increases.
````

**#8 `NVDA_FY2024_2024-01-28:201`** (cited)

````text
Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations > Fiscal Year 2024 Summary
Gross margin increased in fiscal year 2024, primarily driven by Data Center revenue growth and lower net inventory provisions as a percentage of revenue. Operating expenses increased for fiscal year 2024, driven by growth in employees and compensation increases. Fiscal year 2023 also included a $1.4 billion acquisition termination charge related to the proposed Arm transaction.
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 1'), ('NVDA', 'Item 7')] gold=[(None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2024_2024-01-28:200` | Item 7 › Fiscal Year 2024 Summary |  |  | We specialize in markets where our computing platforms can provide tremendous acceleration for applications. These platforms incorporate processors, interconnects, software, algorithms, systems, and services to deliver u… |
| 2 | `NVDA_FY2018_2018-01-28:172` | Item 7 › Research and Development |  |  | Research and development expenses increased by 23% in fiscal year 2018 compared to fiscal year 2017 and increased 10% in fiscal year 2017 compared to fiscal year 2016, driven primarily by employee additions and increases… |
| 3 | `NVDA_FY2024_2024-01-28:202` | Item 7 › Market Platform Highlights |  |  | Data Center revenue for fiscal year 2024 was $47.5 billion, up 217% from fiscal year 2023. In Data Center, we launched AI inference platforms that combine our full-stack inference software with NVIDIA Ada, NVIDIA Hopper … |
| 4 | `NVDA_FY2018_2018-01-28:136` | Item 7 › Fiscal Year 2018 Summary |  |  | Revenue for fiscal year 2018 grew 41% to $9.71 billion, reflecting broad growth in each of our market platforms - gaming, professional visualization, datacenter, and automotive. GPU business revenue was $8.14 billion, up… |
| 5 | `NVDA_FY2024_2024-01-28:203` | Item 7 › Market Platform Highlights |  |  | Gaming revenue for fiscal year 2024 was $10.4 billion, up 15% from fiscal year 2023. In Gaming, we launched the GeForce RTX 4060 and 4070 GPUs based on the NVIDIA Ada Lovelace architecture. We announced NVIDIA Avatar Clo… |

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 12, cited: 2.

**Generated answer**

> NVIDIA’s research and development expenses increased from $1,797 million in fiscal year 2018 to $8,675 million in fiscal year 2024. [NVDA FY2018, Item 7, NVDA_FY2018_2018-01-28:170] [NVDA FY2024, Item 7, NVDA_FY2024_2024-01-28:222]
>
> That represents growth of approximately 382.7% from fiscal year 2018 to fiscal year 2024. [NVDA FY2018, Item 7, NVDA_FY2018_2018-01-28:170] [NVDA FY2024, Item 7, NVDA_FY2024_2024-01-28:222]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2018_2018-01-28:172` | Item 7 › Research and Development |  |  | Research and development expenses increased by 23% in fiscal year 2018 compared to fiscal year 2017 and increased 10% in fiscal year 2017 compared to fiscal year 2016, driven primarily by employee additions and increases… |
| 2 | `NVDA_FY2018_2018-01-28:51` | Item 1 › Table of Contents |  |  | As of January 28, 2018, we had 8,191 full-time employees engaged in research and development. During fiscal years 2018, 2017 and 2016, we incurred research and development expenses of $1.80 billion, $1.46 billion, and $1… |
| 3 | `NVDA_FY2024_2024-01-28:223` | Item 7 › Operating Expenses |  |  | The increase in research and development expenses and sales, general and administrative expenses for fiscal year 2024 was primarily driven by compensation and benefits, including stock-based compensation, reflecting empl… |
| 4 | `NVDA_FY2018_2018-01-28:170` | Item 7 › Operating Expenses | ✓ | #2 | \| \| Year Ended \| \| \| \| Year Ended \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| January 28, 2018 \| January 29, 2017 \| $ Change \| % Change \| January 29, 2017 \| January 31, 2016 \| $ Change \| % Change \| \| \| ($ in millio… |
| 5 | `NVDA_FY2024_2024-01-28:222` | Item 7 › Operating Expenses | ✓ | #1 | \| \| Year Ended \| \| \| \| \|---\|---\|---\|---\|---\| \| \| Jan 28, 2024 \| Jan 29, 2023 \| $ Change \| % Change \| \| \| ($ in millions) \| \| \| \| \| Research and development expenses \| $8,675 \| $7,339 \| $1,336 \| 18% \| \| % of net revenue \|… |
| 6 | `NVDA_FY2024_2024-01-28:432` | Item 15 › Note 14 - Income Taxes |  |  | \| \| Year Ended \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Jan 28, 2024 \| \| Jan 29, 2023 \| \| Jan 30, 2022 \| \| \| \| (In millions, except percentages) \| \| \| \| \| \| \| Tax expense computed at federal statutory rate \| $7,102 … |
| 7 | `NVDA_FY2018_2018-01-28:127` | Item 6 |  |  | \| \| Year Ended \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| January 28, 2018 \| January 29, 2017 \| January 31, 2016 (A) \| January 25, 2015 \| January 26, 2014 \| \| Consolidated Statements of Income Data: \| (In millions, except p… |
| 8 | `NVDA_FY2018_2018-01-28:224` | Item 15 |  |  | \| \| \| \| Page \| \|---\|---\|---\|---\| \| (a) \| 1. \| Consolidated Financial Statements \| \| \| \| \| Report of Independent Registered Public Accounting Firm \| 39 \| \| \| \| Consolidated Statements of Income for the years ended January… |
| 9 | `NVDA_FY2024_2024-01-28:287` | Item 15 › Consolidated Statements of Shareholders' Equity |  |  | \| \| Common Stock Outstanding \| \| Additional Paid-in \| Treasury \| Accumulated Other Comprehensive \| Retained \| Total Shareholders' \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Shares \| Amount \| Capital \| Stock \| Income (Loss) … |
| 10 | `NVDA_FY2018_2018-01-28:242` | Item 15 › CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY |  |  | \| \| Common Stock Outstanding \| \| Additional \| Treasury \| Accumulated Other Comprehensive \| Retained \| Total Shareholders' \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| Tax benefit from stock-based compensation \| — \| — \| 10 \| — \|… |
| 11 | `NVDA_FY2018_2018-01-28:241` | Item 15 › CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY |  |  | \| \| Common Stock Outstanding \| \| Additional \| Treasury \| Accumulated Other Comprehensive \| Retained \| Total Shareholders' \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (In millions, except per share data) \| Shares \| Amount \| Pai… |
| 12 | `NVDA_FY2018_2018-01-28:245` | Item 15 › CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY |  |  | \| \| Common Stock Outstanding \| \| Additional \| Treasury \| Accumulated Other Comprehensive \| Retained \| Total Shareholders' \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| Tax withholding related to vesting of restricted stock units… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#4 `NVDA_FY2018_2018-01-28:170`** (cited, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Operating Expenses (table)
|  | Year Ended |  |  |  | Year Ended |  |  |  |
|---|---|---|---|---|---|---|---|---|
|  | January 28, 2018 | January 29, 2017 | $ Change | % Change | January 29, 2017 | January 31, 2016 | $ Change | % Change |
|  | ($ in millions) |  |  |  | ($ in millions) |  |  |  |
| Research and development expenses | $1,797 | $1,463 | $334 | 23% | $1,463 | $1,331 | $132 | 10% |
| % of net revenue | 18.5% | 21.2% |  |  | 21.2% | 26.6% |  |  |
| Sales, general and administrative expenses | 815 | 663 | 152 | 23% | 663 | 602 | 61 | 10% |
| % of net revenue | 8.4% | 9.6% |  |  | 9.6% | 12.0% |  |  |
| Restructuring and other charges | — | 3 | (3) | (100)% | 3 | 131 | (128) | (98)% |
| % of net revenue | —% | —% |  |  | —% | 2.6% |  |  |
````

**#5 `NVDA_FY2024_2024-01-28:222`** (cited, gold #1)

````text
Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations > Operating Expenses (table)
|  | Year Ended |  |  |  |
|---|---|---|---|---|
|  | Jan 28, 2024 | Jan 29, 2023 | $ Change | % Change |
|  | ($ in millions) |  |  |  |
| Research and development expenses | $8,675 | $7,339 | $1,336 | 18% |
| % of net revenue | 14.2% | 27.2% |  |  |
| Sales, general and administrative expenses | 2,654 | 2,440 | 214 | 9% |
| % of net revenue | 4.4% | 9.1% |  |  |
| Acquisition termination cost | — | 1,353 | (1,353) | (100)% |
| % of net revenue | —% | 5.0% |  |  |
| Total operating expenses | $11,329 | $11,132 | $197 | 2% |
| % of net revenue | 18.6% | 41.3% |  |  |
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| NVIDIA’s research and development expenses increased from $1,797 million in fiscal year 2018 to $8,675 million in fiscal year 2024. [NVDA FY2018, Item 7, NVDA_FY2018_2018-01-28:170] [NVDA FY2024, Item 7, NVDA_FY2024_2024-01-28:222] | None |  |
| That represents growth of approximately 382.7% from fiscal year 2018 to fiscal year 2024. [NVDA FY2018, Item 7, NVDA_FY2018_2018-01-28:170] [NVDA FY2024, Item 7, NVDA_FY2024_2024-01-28:222] | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 2.

**Generated answer**

> NVIDIA's research and development expenses increased from $1,797 million in fiscal year 2018 to $8,675 million in fiscal year 2024, which represents growth of approximately 382.7% [NVDA FY2018, Item 7, NVDA_FY2018_2018-01-28:170] [NVDA FY2024, Item 7, NVDA_FY2024_2024-01-28:222].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-NVDA-2018` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2018,2018-01-28,9714000000,3047000000,3210000000,11241000000,3… |
| 2 | `F-NVDA-2024` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2024,2024-01-28,60922000000,29760000000,32972000000,6572800000… |
| 3 | `NVDA_FY2018_2018-01-28:172` | Item 7 › Research and Development |  |  | Research and development expenses increased by 23% in fiscal year 2018 compared to fiscal year 2017 and increased 10% in fiscal year 2017 compared to fiscal year 2016, driven primarily by employee additions and increases… |
| 4 | `NVDA_FY2018_2018-01-28:51` | Item 1 › Table of Contents |  |  | As of January 28, 2018, we had 8,191 full-time employees engaged in research and development. During fiscal years 2018, 2017 and 2016, we incurred research and development expenses of $1.80 billion, $1.46 billion, and $1… |
| 5 | `NVDA_FY2024_2024-01-28:223` | Item 7 › Operating Expenses |  |  | The increase in research and development expenses and sales, general and administrative expenses for fiscal year 2024 was primarily driven by compensation and benefits, including stock-based compensation, reflecting empl… |
| 6 | `NVDA_FY2018_2018-01-28:170` | Item 7 › Operating Expenses | ✓ | #2 | \| \| Year Ended \| \| \| \| Year Ended \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| January 28, 2018 \| January 29, 2017 \| $ Change \| % Change \| January 29, 2017 \| January 31, 2016 \| $ Change \| % Change \| \| \| ($ in millio… |
| 7 | `NVDA_FY2024_2024-01-28:222` | Item 7 › Operating Expenses | ✓ | #1 | \| \| Year Ended \| \| \| \| \|---\|---\|---\|---\|---\| \| \| Jan 28, 2024 \| Jan 29, 2023 \| $ Change \| % Change \| \| \| ($ in millions) \| \| \| \| \| Research and development expenses \| $8,675 \| $7,339 \| $1,336 \| 18% \| \| % of net revenue \|… |
| 8 | `NVDA_FY2024_2024-01-28:432` | Item 15 › Note 14 - Income Taxes |  |  | \| \| Year Ended \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Jan 28, 2024 \| \| Jan 29, 2023 \| \| Jan 30, 2022 \| \| \| \| (In millions, except percentages) \| \| \| \| \| \| \| Tax expense computed at federal statutory rate \| $7,102 … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#6 `NVDA_FY2018_2018-01-28:170`** (cited, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Operating Expenses (table)
|  | Year Ended |  |  |  | Year Ended |  |  |  |
|---|---|---|---|---|---|---|---|---|
|  | January 28, 2018 | January 29, 2017 | $ Change | % Change | January 29, 2017 | January 31, 2016 | $ Change | % Change |
|  | ($ in millions) |  |  |  | ($ in millions) |  |  |  |
| Research and development expenses | $1,797 | $1,463 | $334 | 23% | $1,463 | $1,331 | $132 | 10% |
| % of net revenue | 18.5% | 21.2% |  |  | 21.2% | 26.6% |  |  |
| Sales, general and administrative expenses | 815 | 663 | 152 | 23% | 663 | 602 | 61 | 10% |
| % of net revenue | 8.4% | 9.6% |  |  | 9.6% | 12.0% |  |  |
| Restructuring and other charges | — | 3 | (3) | (100)% | 3 | 131 | (128) | (98)% |
| % of net revenue | —% | —% |  |  | —% | 2.6% |  |  |
````

**#7 `NVDA_FY2024_2024-01-28:222`** (cited, gold #1)

````text
Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations > Operating Expenses (table)
|  | Year Ended |  |  |  |
|---|---|---|---|---|
|  | Jan 28, 2024 | Jan 29, 2023 | $ Change | % Change |
|  | ($ in millions) |  |  |  |
| Research and development expenses | $8,675 | $7,339 | $1,336 | 18% |
| % of net revenue | 14.2% | 27.2% |  |  |
| Sales, general and administrative expenses | 2,654 | 2,440 | 214 | 9% |
| % of net revenue | 4.4% | 9.1% |  |  |
| Acquisition termination cost | — | 1,353 | (1,353) | (100)% |
| % of net revenue | —% | 5.0% |  |  |
| Total operating expenses | $11,329 | $11,132 | $197 | 2% |
| % of net revenue | 18.6% | 41.3% |  |  |
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| NVIDIA's research and development expenses increased from $1,797 million in fiscal year 2018 to $8,675 million in fiscal year 2024, which represents growth of approximately 382.7% [NVDA FY2018, Item 7, NVDA_FY2018_2018-01-28:170] [NVDA FY2024, Item 7, NVDA_FY2024_2024-01-28:222]. | None |  |

</details>
