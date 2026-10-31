# gold-066: Cross-year table

[← all cases](../README.md) · company: Tesla, Inc. (TSLA) · fiscal year: 2025 · recipe `cross_year_table` · hop `multi` · answer type `numeric` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> By how many million dollars did Tesla's total assets increase from fiscal year 2021 to fiscal year 2025?

**Gold answer**

> $75,675 million

**Program**: `subtract(137806, 62131)` → `75675.0`

**Gold numbers** (RQ2 numeric_accuracy targets): $75,675 million

**Gold evidence**

1. `TSLA_FY2025_2025-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › (in millions, except per share data) · table

   > | Total assets | $137,806 | $122,070 |

2. `TSLA_FY2021_2021-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › (in millions, except per share data) · table

   > | Total assets | $62,131 | $52,148 |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 11 | 8 |
| recall@5 | 1.00 | 0.50 | 0.50 | 0.50 |
| recall@all | 1.00 | 0.50 | 0.50 | 0.50 |
| complete@all | 1 | 0 | 0 | 0 |
| average precision (lexical) | 0.42 | 0.25 | 0.50 | 0.25 |
| gold evidence first rank | #1: 3, #2: 4 | #1: –, #2: 4 | #1: 2, #2: – | #1: 4, #2: – |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✗ | ✗ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 0.00 | 0.00 | 1.00 |
| citation precision | 1.00 | – | – | 0.00 |
| citation recall | 1.00 | – | – | 0.00 |
| citation F1 | 1.00 | – | – | 0.00 |
| has a citation | 1 | 0 | 0 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 1 |
| tokens | 2692 | 1514 | 16252 | 9067 |
| cost (USD) | 0.0004 | 0.0002 | 0.0545 | 0.0277 |
| latency (s) | 2.3 | 5.7 | 22.1 | 8.4 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Tesla’s total assets increased by **$75,675 million** from 2021 to 2025, calculated as:
>
> - **2025 total assets:** $137,806 million [3]
> - **2021 total assets:** $62,131 million [4]
>
> **Increase:** $137,806 million − $62,131 million = **$75,675 million** [3][4]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2025_2025-12-31:179` | Item 7 › Overview and 2025 Highlights |  |  | In 2025, we recognized total revenues of $94.83 billion, representing a decrease of $2.86 billion compared to the prior year. In 2025, our net income attributable to common stockholders was $3.79 billion, representing a … |
| 2 | `TSLA_FY2021_2021-12-31:298` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Prepaid expenses and other current assets \| (271) \| (251) \| (288) \| \| Other non-current assets \| (1,291) \| (344) \| 115 \| \| Accounts payable a… |
| 3 | `TSLA_FY2025_2025-12-31:257` | Item 8 › (in millions, except per share data) | ✓ | #1 | \| \| December 31, 2025 \| December 31, 2024 \| \|---\|---\|---\| \| Assets \| \| \| \| Current assets \| \| \| \| Cash and cash equivalents \| $16,513 \| $16,139 \| \| Short-term investments \| 27,546 \| 20,424 \| \| Accounts receivable, net \| … |
| 4 | `TSLA_FY2021_2021-12-31:277` | Item 8 › (in millions, except per share data) | ✓ | #2 | \| \| December 31, \| December 31, \| \|---\|---\|---\| \| \| 2021 \| 2020 \| \| Assets \| \| \| \| Current assets \| \| \| \| Cash and cash equivalents \| $17,576 \| $19,384 \| \| Short-term marketable securities \| 131 \| — \| \| Accounts receivab… |
| 5 | `TSLA_FY2021_2021-12-31:258` | Item 7 › Summary of Cash Flows |  |  | Net cash provided by operating activities increased by $5.55 billion to $11.50 billion during the year ended December 31, 2021 from $5.94 billion during the year ended December 31, 2020. This increase was primarily due t… |
| 6 | `TSLA_FY2021_2021-12-31:188` | Item 7 › Overview and 2021 Highlights |  |  | In 2021, our net income attributable to common stockholders was $5.52 billion, representing a favorable change of $4.80 billion, compared to the prior year. We continue to focus on improving our profitability through pro… |
| 7 | `TSLA_FY2021_2021-12-31:452` | Item 8 › Pledged Assets |  |  | As of December 31, 2021 and 2020, we had pledged or restricted $5.25 billion and $6.04 billion of our assets (consisting principally of restricted cash, receivables, inventory, SRECs, solar energy systems, operating leas… |
| 8 | `TSLA_FY2025_2025-12-31:273` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2025 \| 2024 \| 2023 \| \| Cash Flows from Operating Activities \| \| \| \| \| Net income \| $3,855 \| $7,153 \| $14,974 \| \| Adjustments to reconcile net income to net cash pro… |
| 9 | `TSLA_FY2025_2025-12-31:454` | Item 8 › Note 12 – Income Taxes |  |  | Cash paid for income taxes, net of refunds, during the years ended December 31, 2024 and 2023 was $1.33 billion and $1.12 billion, respectively. Deferred tax assets (liabilities) as of December 31, 2025 and 2024 consiste… |
| 10 | `TSLA_FY2025_2025-12-31:496` | Item 8 › Note 16 – Segment Reporting and Information about Geographic Areas |  |  | \| \| December 31, 2025 \| December 31, 2024 \| \|---\|---\|---\| \| Automotive \| $9,678 \| $9,988 \| \| Energy generation and storage \| 2,714 \| 2,029 \| \| Total \| $12,392 \| $12,017 \| |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `TSLA_FY2025_2025-12-31:257`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (in millions, except per share data) (table)
|  | December 31, 2025 | December 31, 2024 |
|---|---|---|
| Assets |  |  |
| Current assets |  |  |
| Cash and cash equivalents | $16,513 | $16,139 |
| Short-term investments | 27,546 | 20,424 |
| Accounts receivable, net | 4,576 | 4,418 |
| Inventory | 12,392 | 12,017 |
| Prepaid expenses and other current assets | 7,615 | 5,362 |
| Total current assets | 68,642 | 58,360 |
| Operating lease vehicles, net | 4,912 | 5,581 |
| Energy generation and storage systems, net | 4,604 | 4,924 |
| Property, plant and equipment, net | 40,643 | 35,836 |
| Operating lease right-of-use assets | 6,027 | 5,160 |
| Digital assets | 1,008 | 1,076 |
| Deferred tax assets | 6,925 | 6,524 |
| Other non-current assets | 5,045 | 4,609 |
| Total assets | $137,806 | $122,070 |
| Liabilities |  |  |
| Current liabilities |  |  |
| Accounts payable | $13,371 | $12,474 |
| Accrued liabilities and other | 13,279 | 10,723 |
| Deferred revenue | 3,424 | 3,168 |
````

**#4 `TSLA_FY2021_2021-12-31:277`** (cited, gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (in millions, except per share data) (table)
|  | December 31, | December 31, |
|---|---|---|
|  | 2021 | 2020 |
| Assets |  |  |
| Current assets |  |  |
| Cash and cash equivalents | $17,576 | $19,384 |
| Short-term marketable securities | 131 | — |
| Accounts receivable, net | 1,913 | 1,886 |
| Inventory | 5,757 | 4,101 |
| Prepaid expenses and other current assets | 1,723 | 1,346 |
| Total current assets | 27,100 | 26,717 |
| Operating lease vehicles, net | 4,511 | 3,091 |
| Solar energy systems, net | 5,765 | 5,979 |
| Property, plant and equipment, net | 18,884 | 12,747 |
| Operating lease right-of-use assets | 2,016 | 1,558 |
| Digital assets, net | 1,260 | — |
| Intangible assets, net | 257 | 313 |
| Goodwill | 200 | 207 |
| Other non-current assets | 2,138 | 1,536 |
| Total assets | $62,131 | $52,148 |
| Liabilities |  |  |
| Current liabilities |  |  |
| Accounts payable | $10,025 | $6,051 |
| Accrued liabilities and other | 5,719 | 3,855 |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2021_2021-12-31:229` | Item 7 › Cost of Revenues and Gross Margin |  |  | Cost of automotive leasing revenue increased $415 million, or 74%, in the year ended December 31, 2021 as compared to the year ended December 31, 2020, primarily due to an increase in cumulative vehicles under our direct… |
| 2 | `TSLA_FY2021_2021-12-31:258` | Item 7 › Summary of Cash Flows |  |  | Net cash provided by operating activities increased by $5.55 billion to $11.50 billion during the year ended December 31, 2021 from $5.94 billion during the year ended December 31, 2020. This increase was primarily due t… |
| 3 | `TSLA_FY2021_2021-12-31:235` | Item 7 › Research and Development Expense |  |  | Research and development (“R&D”) expenses consist primarily of personnel costs for our teams in engineering and research, manufacturing engineering and manufacturing test organizations, prototyping expense, contract and … |
| 4 | `TSLA_FY2021_2021-12-31:277` | Item 8 › (in millions, except per share data) |  | #2 | \| \| December 31, \| December 31, \| \|---\|---\|---\| \| \| 2021 \| 2020 \| \| Assets \| \| \| \| Current assets \| \| \| \| Cash and cash equivalents \| $17,576 \| $19,384 \| \| Short-term marketable securities \| 131 \| — \| \| Accounts receivab… |
| 5 | `TSLA_FY2025_2025-12-31:179` | Item 7 › Overview and 2025 Highlights |  |  | In 2025, we recognized total revenues of $94.83 billion, representing a decrease of $2.86 billion compared to the prior year. In 2025, our net income attributable to common stockholders was $3.79 billion, representing a … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#4 `TSLA_FY2021_2021-12-31:277`** (gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (in millions, except per share data) (table)
|  | December 31, | December 31, |
|---|---|---|
|  | 2021 | 2020 |
| Assets |  |  |
| Current assets |  |  |
| Cash and cash equivalents | $17,576 | $19,384 |
| Short-term marketable securities | 131 | — |
| Accounts receivable, net | 1,913 | 1,886 |
| Inventory | 5,757 | 4,101 |
| Prepaid expenses and other current assets | 1,723 | 1,346 |
| Total current assets | 27,100 | 26,717 |
| Operating lease vehicles, net | 4,511 | 3,091 |
| Solar energy systems, net | 5,765 | 5,979 |
| Property, plant and equipment, net | 18,884 | 12,747 |
| Operating lease right-of-use assets | 2,016 | 1,558 |
| Digital assets, net | 1,260 | — |
| Intangible assets, net | 257 | 313 |
| Goodwill | 200 | 207 |
| Other non-current assets | 2,138 | 1,536 |
| Total assets | $62,131 | $52,148 |
| Liabilities |  |  |
| Current liabilities |  |  |
| Accounts payable | $10,025 | $6,051 |
| Accrued liabilities and other | 5,719 | 3,855 |
````

</details>

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 11, cited: 0.

**Generated answer**

> The filing does not disclose Tesla’s total assets for fiscal year 2021 in the provided evidence, so the increase from fiscal year 2021 to fiscal year 2025 cannot be determined from these blocks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2025_2025-12-31:486` | Item 8 › Note 14 – Variable Interest Entity Arrangements |  |  | \| \| December 31, 2025 \| December 31, 2024 \| \|---\|---\|---\| \| Assets \| \| \| \| Current assets \| \| \| \| Cash and cash equivalents \| $109 \| $49 \| \| Accounts receivable, net \| 11 \| 18 \| \| Prepaid expenses and other current asset… |
| 2 | `TSLA_FY2025_2025-12-31:257` | Item 8 › (in millions, except per share data) |  | #1 | \| \| December 31, 2025 \| December 31, 2024 \| \|---\|---\|---\| \| Assets \| \| \| \| Current assets \| \| \| \| Cash and cash equivalents \| $16,513 \| $16,139 \| \| Short-term investments \| 27,546 \| 20,424 \| \| Accounts receivable, net \| … |
| 3 | `TSLA_FY2025_2025-12-31:455` | Item 8 › Note 12 – Income Taxes |  |  | \| \| December 31, 2025 \| December 31, 2024 \| \|---\|---\|---\| \| Deferred tax assets: \| \| \| \| Net operating loss carry-forwards \| $1,083 \| $1,295 \| \| Research and development credits \| 2,030 \| 1,735 \| \| Other tax credits and … |
| 4 | `TSLA_FY2021_2021-12-31:390` | Item 8 › Note 4 – Goodwill and Intangible Assets |  |  | \| \| December 31, 2021 \| \| \| \| December 31, 2020 \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Gross Carrying Amount \| Accumulated Amortization \| Other \| Net Carrying Amount \| Gross Carrying Amount \| Accumulated Amort… |
| 5 | `TSLA_FY2021_2021-12-31:389` | Item 8 › Note 4 – Goodwill and Intangible Assets |  |  | \| \| December 31, 2021 \| \| \| \| December 31, 2020 \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Gross Carrying Amount \| Accumulated Amortization \| Other \| Net Carrying Amount \| Gross Carrying Amount \| Accumulated Amort… |
| 6 | `TSLA_FY2021_2021-12-31:352` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | \| \| December 31, \| December 31, \| December 31, \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Cash and cash equivalents \| $17,576 \| $19,384 \| $6,268 \| \| Restricted cash included in prepaid expenses and other current asse… |
| 7 | `TSLA_FY2025_2025-12-31:326` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | \| \| December 31, 2025 \| December 31, 2024 \| December 31, 2023 \| \|---\|---\|---\|---\| \| Cash and cash equivalents \| $16,513 \| $16,139 \| $16,398 \| \| Restricted cash included in prepaid expenses and other current assets \| 389 … |
| 8 | `TSLA_FY2021_2021-12-31:385` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | \| \| Balances at December 31, 2020 \| Adjustments from Adoption of ASU 2020-06 \| Balances at January 1, 2021 \| \|---\|---\|---\|---\| \| Assets \| \| \| \| \| Property, plant and equipment, net \| $12,747 \| $(45) \| $12,702 \| \| Liabili… |
| 9 | `TSLA_FY2021_2021-12-31:400` | Item 8 › Note 5 – Fair Value of Financial Instruments |  |  | \| \| December 31, 2021 \| \| December 31, 2020 \| \| \|---\|---\|---\|---\|---\| \| \| Carrying Value \| Fair Value \| Carrying Value \| Fair Value \| \| Convertible Senior Notes (1) \| $119 \| $2,016 \| $1,971 \| $24,596 \| \| 2025 Notes (1) \|… |
| 10 | `TSLA_FY2025_2025-12-31:371` | Item 8 › Note 5 – Inventory |  |  | \| \| December 31, 2025 \| December 31, 2024 \| \|---\|---\|---\| \| Raw materials \| $4,522 \| $5,242 \| \| Work in process \| 1,725 \| 1,532 \| \| Finished goods (1) \| 4,849 \| 3,940 \| \| Service parts \| 1,296 \| 1,303 \| \| Total \| $12,392… |
| 11 | `TSLA_FY2021_2021-12-31:392` | Item 8 › Note 4 – Goodwill and Intangible Assets |  |  | \| 2022 \| $49 \| \|---\|---\| \| 2023 \| 43 \| \| 2024 \| 28 \| \| 2025 \| 28 \| \| 2026 \| 28 \| \| Thereafter \| 66 \| \| Total \| $242 \| |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `TSLA_FY2025_2025-12-31:257`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (in millions, except per share data) (table)
|  | December 31, 2025 | December 31, 2024 |
|---|---|---|
| Assets |  |  |
| Current assets |  |  |
| Cash and cash equivalents | $16,513 | $16,139 |
| Short-term investments | 27,546 | 20,424 |
| Accounts receivable, net | 4,576 | 4,418 |
| Inventory | 12,392 | 12,017 |
| Prepaid expenses and other current assets | 7,615 | 5,362 |
| Total current assets | 68,642 | 58,360 |
| Operating lease vehicles, net | 4,912 | 5,581 |
| Energy generation and storage systems, net | 4,604 | 4,924 |
| Property, plant and equipment, net | 40,643 | 35,836 |
| Operating lease right-of-use assets | 6,027 | 5,160 |
| Digital assets | 1,008 | 1,076 |
| Deferred tax assets | 6,925 | 6,524 |
| Other non-current assets | 5,045 | 4,609 |
| Total assets | $137,806 | $122,070 |
| Liabilities |  |  |
| Current liabilities |  |  |
| Accounts payable | $13,371 | $12,474 |
| Accrued liabilities and other | 13,279 | 10,723 |
| Deferred revenue | 3,424 | 3,168 |
````

</details>

RQ2 citation match (section level): `no citations`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| The filing does not disclose Tesla’s total assets for fiscal year 2021 in the provided evidence, so the increase from fiscal year 2021 to fiscal year 2025 cannot be determined from these blocks. | supported | The retrieved evidence includes 2025 total assets but no 2021 total assets, so the 2021-to-2025 increase cannot be determined from these blocks. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 2.

**Generated answer**

> Tesla's total assets increased by $75,675 million from fiscal year 2021 to fiscal year 2025, calculated as $137,806 million minus $62,131 million. [F-TSLA-2021] [F-TSLA-2025]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-TSLA-2021` | SEC XBRL Reported Financials (financials.csv) | ✓ |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2021,2021-12-31,53823000000,5519000000,6523000000,62131000000,… |
| 2 | `F-TSLA-2025` | SEC XBRL Reported Financials (financials.csv) | ✓ |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2025,2025-12-31,94827000000,3794000000,4355000000,137806000000… |
| 3 | `TSLA_FY2025_2025-12-31:486` | Item 8 › Note 14 – Variable Interest Entity Arrangements |  |  | \| \| December 31, 2025 \| December 31, 2024 \| \|---\|---\|---\| \| Assets \| \| \| \| Current assets \| \| \| \| Cash and cash equivalents \| $109 \| $49 \| \| Accounts receivable, net \| 11 \| 18 \| \| Prepaid expenses and other current asset… |
| 4 | `TSLA_FY2025_2025-12-31:257` | Item 8 › (in millions, except per share data) |  | #1 | \| \| December 31, 2025 \| December 31, 2024 \| \|---\|---\|---\| \| Assets \| \| \| \| Current assets \| \| \| \| Cash and cash equivalents \| $16,513 \| $16,139 \| \| Short-term investments \| 27,546 \| 20,424 \| \| Accounts receivable, net \| … |
| 5 | `TSLA_FY2025_2025-12-31:455` | Item 8 › Note 12 – Income Taxes |  |  | \| \| December 31, 2025 \| December 31, 2024 \| \|---\|---\|---\| \| Deferred tax assets: \| \| \| \| Net operating loss carry-forwards \| $1,083 \| $1,295 \| \| Research and development credits \| 2,030 \| 1,735 \| \| Other tax credits and … |
| 6 | `TSLA_FY2021_2021-12-31:390` | Item 8 › Note 4 – Goodwill and Intangible Assets |  |  | \| \| December 31, 2021 \| \| \| \| December 31, 2020 \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Gross Carrying Amount \| Accumulated Amortization \| Other \| Net Carrying Amount \| Gross Carrying Amount \| Accumulated Amort… |
| 7 | `TSLA_FY2021_2021-12-31:389` | Item 8 › Note 4 – Goodwill and Intangible Assets |  |  | \| \| December 31, 2021 \| \| \| \| December 31, 2020 \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Gross Carrying Amount \| Accumulated Amortization \| Other \| Net Carrying Amount \| Gross Carrying Amount \| Accumulated Amort… |
| 8 | `TSLA_FY2021_2021-12-31:352` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | \| \| December 31, \| December 31, \| December 31, \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Cash and cash equivalents \| $17,576 \| $19,384 \| $6,268 \| \| Restricted cash included in prepaid expenses and other current asse… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `F-TSLA-2021`** (cited)

````text
[F-TSLA-2021] (TSLA FY2021 reported financials; amounts in USD, EPSDiluted in USD per share)
fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted
2021,2021-12-31,53823000000,5519000000,6523000000,62131000000,30548000000,30189000000,17576000000,11497000000,4.9
````

**#2 `F-TSLA-2025`** (cited)

````text
[F-TSLA-2025] (TSLA FY2025 reported financials; amounts in USD, EPSDiluted in USD per share)
fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted
2025,2025-12-31,94827000000,3794000000,4355000000,137806000000,54941000000,82137000000,16513000000,14747000000,1.08
````

**#4 `TSLA_FY2025_2025-12-31:257`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (in millions, except per share data) (table)
|  | December 31, 2025 | December 31, 2024 |
|---|---|---|
| Assets |  |  |
| Current assets |  |  |
| Cash and cash equivalents | $16,513 | $16,139 |
| Short-term investments | 27,546 | 20,424 |
| Accounts receivable, net | 4,576 | 4,418 |
| Inventory | 12,392 | 12,017 |
| Prepaid expenses and other current assets | 7,615 | 5,362 |
| Total current assets | 68,642 | 58,360 |
| Operating lease vehicles, net | 4,912 | 5,581 |
| Energy generation and storage systems, net | 4,604 | 4,924 |
| Property, plant and equipment, net | 40,643 | 35,836 |
| Operating lease right-of-use assets | 6,027 | 5,160 |
| Digital assets | 1,008 | 1,076 |
| Deferred tax assets | 6,925 | 6,524 |
| Other non-current assets | 5,045 | 4,609 |
| Total assets | $137,806 | $122,070 |
| Liabilities |  |  |
| Current liabilities |  |  |
| Accounts payable | $13,371 | $12,474 |
| Accrued liabilities and other | 13,279 | 10,723 |
| Deferred revenue | 3,424 | 3,168 |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'XBRL')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Tesla's total assets increased by $75,675 million from fiscal year 2021 to fiscal year 2025, calculated as $137,806 million minus $62,131 million. [F-TSLA-2021] [F-TSLA-2025] | None |  |

</details>
