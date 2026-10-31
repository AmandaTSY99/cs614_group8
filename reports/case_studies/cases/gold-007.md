# gold-007: Single-hop table

[← all cases](../README.md) · company: Walmart Inc. (WMT) · fiscal year: 2025 · recipe `table` · hop `single` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> By how many millions of dollars did Walmart Inc.'s net property and equipment increase from fiscal year 2024 to fiscal year 2025?

**Gold answer**

> $9,183 million

**Program**: `subtract(119993, 110810)` → `9183.0`

**Gold numbers** (RQ2 numeric_accuracy targets): $9,183 million

**Gold evidence**

1. `WMT_FY2025_2025-01-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Property and Equipment · table

   > Property and equipment, net | | $119,993 | $110,810

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 9 | 7 |
| recall@5 | 1.00 | 0.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 0.00 | 1.00 | 1.00 |
| complete@all | 1 | 0 | 1 | 1 |
| average precision (lexical) | 0.83 | 0.00 | 1.00 | 0.73 |
| gold evidence first rank | #1: 1 | #1: – | #1: 1 | #1: 2 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✗ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 0.00 | 1.00 | 1.00 |
| citation precision | 1.00 | – | 1.00 | 1.00 |
| citation recall | 1.00 | – | 1.00 | 1.00 |
| citation F1 | 1.00 | – | 1.00 | 1.00 |
| has a citation | 1 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 2 | 1 |
| tokens | 2692 | 1095 | 8753 | 5062 |
| cost (USD) | 0.0004 | 0.0002 | 0.0314 | 0.0181 |
| latency (s) | 1.9 | 5.9 | 15.4 | 7.4 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> Walmart’s net property and equipment increased by **$9,183 million** from fiscal 2024 to fiscal 2025, calculated as **$119,993 million minus $110,810 million** [1].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `WMT_FY2025_2025-01-31:317` | Item 8 › Property and Equipment | ✓ | #1 | \| \| Estimated Useful Lives \| As of January 31, \| \| \|---\|---\|---\|---\| \| (Dollars in millions) \| (in Years) \| 2025 \| 2024 \| \| Land \| N/A \| $19,342 \| $19,562 \| \| Buildings and improvements \| 3 - 40 \| 117,973 \| 111,767 \| \| F… |
| 2 | `WMT_FY2025_2025-01-31:222` | Item 7 › Consolidated Results of Operations |  |  | Our total revenues increased $32.9 billion or 5.1% and $36.8 billion or 6.0% for fiscal 2025 and 2024, respectively, when compared to the previous fiscal year. These increases in revenues were primarily due to increases … |
| 3 | `WMT_FY2025_2025-01-31:246` | Item 7 › Net Cash Used in Investing Activities |  | #1 | Net cash used in investing activities was $21.4 billion, $21.3 billion and $17.7 billion for fiscal 2025, 2024 and 2023, respectively, and generally consisted of capital expenditures. Net cash used in investing activitie… |
| 4 | `WMT_FY2025_2025-01-31:223` | Item 7 › Consolidated Results of Operations |  |  | Our gross profit rate increased 40 and 27 basis points for fiscal 2025 and 2024, respectively, when compared to the previous fiscal year. The increases were primarily driven by the Walmart U.S. segment, due to managing p… |
| 5 | `WMT_FY2025_2025-01-31:228` | Item 7 › Walmart U.S. Segment |  |  | Net sales for the Walmart U.S. segment increased $20.6 billion or 4.7% and $21.3 billion or 5.1% for fiscal 2025 and 2024, respectively, when compared to the previous fiscal year. The increases in net sales were primaril… |
| 6 | `WMT_FY2025_2025-01-31:232` | Item 7 › Walmart International Segment |  |  | Net sales for the Walmart International segment increased $7.2 billion or 6.3% and $13.7 billion or 13.5% for fiscal 2025 and 2024, respectively, when compared to the previous fiscal year. For fiscal 2025, the increase w… |
| 7 | `WMT_FY2025_2025-01-31:16` | Cautionary Statement Regarding Forward-Looking Statements |  |  | •the amount, number, growth, increase, reduction or decrease in or over certain periods, of or in certain financial items or measures or operating measures, including our earnings per share, net sales, growth rates, comp… |
| 8 | `WMT_FY2025_2025-01-31:229` | Item 7 › Walmart U.S. Segment |  |  | Gross profit rate increased 47 and 20 basis points for fiscal 2025 and 2024, respectively, when compared to the previous fiscal year. The increase in fiscal 2025 gross profit rate was primarily driven by managing prices … |
| 9 | `WMT_FY2025_2025-01-31:238` | Item 7 › Sam's Club U.S. Segment |  |  | Membership and other income increased 13.3% and 7.5% for fiscal 2025 and 2024, respectively, when compared to the previous fiscal year. For fiscal 2025 and 2024, the increases were primarily due to growth in membership b… |
| 10 | `WMT_FY2025_2025-01-31:226` | Item 7 › Consolidated Results of Operations |  |  | As a result of the factors discussed above, we reported $20.2 billion and $16.3 billion of consolidated net income for fiscal 2025 and 2024, respectively, which represents an increase of $3.9 billion and $5.0 billion for… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `WMT_FY2025_2025-01-31:317`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Property and Equipment (table)
|  | Estimated Useful Lives | As of January 31, |  |
|---|---|---|---|
| (Dollars in millions) | (in Years) | 2025 | 2024 |
| Land | N/A | $19,342 | $19,562 |
| Buildings and improvements | 3 - 40 | 117,973 | 111,767 |
| Fixtures and equipment | 2 - 30 | 76,226 | 72,161 |
| Transportation equipment | 3 - 15 | 2,673 | 2,979 |
| Construction in progress | N/A | 15,403 | 13,390 |
| Property and equipment |  | 231,617 | 219,859 |
| Accumulated depreciation |  | (111,624) | (109,049) |
| Property and equipment, net |  | $119,993 | $110,810 |
````

**#3 `WMT_FY2025_2025-01-31:246`** (gold #1)

````text
ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Net Cash Used in Investing Activities
Net cash used in investing activities was $21.4 billion, $21.3 billion and $17.7 billion for fiscal 2025, 2024 and 2023, respectively, and generally consisted of capital expenditures. Net cash used in investing activities increased $0.1 billion for fiscal 2025 when compared to the previous fiscal year. The increase is primarily due to increased purchases of property and equipment as well as the acquisition of VIZIO for net consideration of $1.9 billion, partially offset by net proceeds received from sales of certain strategic investments, including $3.6 billion related to the sale of our JD.com investment. Net cash used in investing activities increased $3.6 billion for fiscal 2024 when compared to the previous fiscal year, primarily due to increased payments for property and equipment. Capital expenditures Refer to the "Strategic Capital Allocation" section in our Company Performance Metrics for capital expenditure detail for fiscal 2025 and 2024. For the fiscal year ending January 31, 2026 ("fiscal 2026"), we project capital expenditures will be approximately $21 billion to $25 billion, with a focus on technology, supply chain and customer-facing initiatives.
````

</details>

RQ2 citation match (section level): `cited=[('WMT', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `WMT_FY2025_2025-01-31:226` | Item 7 › Consolidated Results of Operations |  |  | As a result of the factors discussed above, we reported $20.2 billion and $16.3 billion of consolidated net income for fiscal 2025 and 2024, respectively, which represents an increase of $3.9 billion and $5.0 billion for… |
| 2 | `WMT_FY2025_2025-01-31:232` | Item 7 › Walmart International Segment |  |  | Net sales for the Walmart International segment increased $7.2 billion or 6.3% and $13.7 billion or 13.5% for fiscal 2025 and 2024, respectively, when compared to the previous fiscal year. For fiscal 2025, the increase w… |
| 3 | `WMT_FY2025_2025-01-31:230` | Item 7 › Walmart U.S. Segment |  |  | As a result of the factors discussed above, segment operating income increased $1.7 billion and $1.5 billion for fiscal 2025 and 2024, respectively, when compared to the previous fiscal year. |
| 4 | `WMT_FY2025_2025-01-31:228` | Item 7 › Walmart U.S. Segment |  |  | Net sales for the Walmart U.S. segment increased $20.6 billion or 4.7% and $21.3 billion or 5.1% for fiscal 2025 and 2024, respectively, when compared to the previous fiscal year. The increases in net sales were primaril… |
| 5 | `WMT_FY2025_2025-01-31:233` | Item 7 › Walmart International Segment |  |  | Operating expenses as a percentage of segment net sales decreased 5 and 152 basis points for fiscal 2025 and 2024, respectively, when compared to the previous fiscal year. The decrease in operating expenses as a percenta… |

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 9, cited: 1.

**Generated answer**

> Walmart Inc.'s net property and equipment increased by $9,183 million from fiscal 2024 to fiscal 2025, rising from $110,810 million to $119,993 million [WMT FY2025, Item 8, WMT_FY2025_2025-01-31:317].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `WMT_FY2025_2025-01-31:317` | Item 8 › Property and Equipment | ✓ | #1 | \| \| Estimated Useful Lives \| As of January 31, \| \| \|---\|---\|---\|---\| \| (Dollars in millions) \| (in Years) \| 2025 \| 2024 \| \| Land \| N/A \| $19,342 \| $19,562 \| \| Buildings and improvements \| 3 - 40 \| 117,973 \| 111,767 \| \| F… |
| 2 | `WMT_FY2025_2025-01-31:443` | Item 8 › Note 12. Segments and Disaggregated Revenue |  | #1 | Total revenues and long-lived assets, consisting primarily of net property and equipment and lease right-of-use assets, aggregated by the Company's U.S. and non-U.S. operations, are as follows: |
| 3 | `WMT_FY2025_2025-01-31:304` | Item 8 › Consolidated Statements of Cash Flows |  | #1 | \| \| Fiscal Years Ended January 31, \| \| \| \|---\|---\|---\|---\| \| Payments for property and equipment \| (23,783) \| (20,606) \| (16,857) \| \| Proceeds from the disposal of property and equipment \| 432 \| 250 \| 170 \| \| Proceeds fr… |
| 4 | `WMT_FY2025_2025-01-31:217` | Item 7 › Strategic Capital Allocation |  | #1 | \| \| Fiscal Years Ended January 31, \| \| \| \|---\|---\|---\|---\| \| (Amounts in millions) \| 2025 \| 2024 \| 2023 \| \| Net cash provided by operating activities \| $36,443 \| $35,726 \| $28,841 \| \| Payments for property and equipment … |
| 5 | `WMT_FY2025_2025-01-31:404` | Item 8 › Note 9. Taxes |  | #1 | \| \| January 31, \| \| \|---\|---\|---\| \| (Amounts in millions) \| 2025 \| 2024 \| \| Deferred tax assets: \| \| \| \| Loss and tax credit carryforwards \| $7,539 \| $7,136 \| \| Accrued liabilities \| 3,009 \| 3,066 \| \| Share-based compens… |
| 6 | `WMT_FY2025_2025-01-31:246` | Item 7 › Net Cash Used in Investing Activities |  | #1 | Net cash used in investing activities was $21.4 billion, $21.3 billion and $17.7 billion for fiscal 2025, 2024 and 2023, respectively, and generally consisted of capital expenditures. Net cash used in investing activitie… |
| 7 | `WMT_FY2025_2025-01-31:294` | Item 8 › Consolidated Balance Sheets |  | #1 | \| \| As of January 31, \| \| \|---\|---\|---\| \| (Amounts in millions) \| 2025 \| 2024 \| \| ASSETS \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $9,037 \| $9,867 \| \| Receivables, net \| 9,975 \| 8,796 \| \| Inventories \| … |
| 8 | `WMT_FY2025_2025-01-31:210` | Item 7 › Returns |  |  | \| \| As of January 31, \| \| \| \|---\|---\|---\|---\| \| \| 2025 \| 2024 \| 2023 \| \| Certain Balance Sheet Data \| \| \| \| \| Total assets \| $260,823 \| $252,399 \| $243,197 \| \| Accumulated depreciation and amortization \| 123,646 \| 119,60… |
| 9 | `WMT_FY2025_2025-01-31:318` | Item 8 › Property and Equipment |  |  | Leasehold improvements are depreciated or amortized over the shorter of the estimated useful life of the asset or the remaining expected lease term. Total depreciation and amortization expense for property and equipment,… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `WMT_FY2025_2025-01-31:317`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Property and Equipment (table)
|  | Estimated Useful Lives | As of January 31, |  |
|---|---|---|---|
| (Dollars in millions) | (in Years) | 2025 | 2024 |
| Land | N/A | $19,342 | $19,562 |
| Buildings and improvements | 3 - 40 | 117,973 | 111,767 |
| Fixtures and equipment | 2 - 30 | 76,226 | 72,161 |
| Transportation equipment | 3 - 15 | 2,673 | 2,979 |
| Construction in progress | N/A | 15,403 | 13,390 |
| Property and equipment |  | 231,617 | 219,859 |
| Accumulated depreciation |  | (111,624) | (109,049) |
| Property and equipment, net |  | $119,993 | $110,810 |
````

**#2 `WMT_FY2025_2025-01-31:443`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 12. Segments and Disaggregated Revenue
Total revenues and long-lived assets, consisting primarily of net property and equipment and lease right-of-use assets, aggregated by the Company's U.S. and non-U.S. operations, are as follows:
````

**#3 `WMT_FY2025_2025-01-31:304`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Consolidated Statements of Cash Flows (table)
|  | Fiscal Years Ended January 31, |  |  |
|---|---|---|---|
| Payments for property and equipment | (23,783) | (20,606) | (16,857) |
| Proceeds from the disposal of property and equipment | 432 | 250 | 170 |
| Proceeds from disposal of certain strategic investments | 4,080 | — | — |
| Payments for business acquisitions, net of cash acquired | (1,896) | (9) | (740) |
| Other investing activities | (212) | (922) | (295) |
| Net cash used in investing activities | (21,379) | (21,287) | (17,722) |
| Cash flows from financing activities: |  |  |  |
| Net change in short-term borrowings | 2,212 | 512 | (34) |
| Proceeds from issuance of long-term debt | — | 4,967 | 5,041 |
| Repayments of long-term debt | (3,468) | (4,217) | (2,689) |
| Dividends paid | (6,688) | (6,140) | (6,114) |
| Purchase of Company stock | (4,494) | (2,779) | (9,920) |
| Dividends paid to noncontrolling interest | (576) | (763) | (444) |
| Purchase of noncontrolling interest | — | (3,462) | (827) |
````

**#4 `WMT_FY2025_2025-01-31:217`** (gold #1)

````text
ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Strategic Capital Allocation (table)
|  | Fiscal Years Ended January 31, |  |  |
|---|---|---|---|
| (Amounts in millions) | 2025 | 2024 | 2023 |
| Net cash provided by operating activities | $36,443 | $35,726 | $28,841 |
| Payments for property and equipment | (23,783) | (20,606) | (16,857) |
| Free cash flow | $12,660 | $15,120 | $11,984 |
| Net cash used in investing activities(1) | $(21,379) | $(21,287) | $(17,722) |
| Net cash used in financing activities | (14,822) | (13,414) | (17,039) |
````

**#5 `WMT_FY2025_2025-01-31:404`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 9. Taxes (table)
|  | January 31, |  |
|---|---|---|
| (Amounts in millions) | 2025 | 2024 |
| Deferred tax assets: |  |  |
| Loss and tax credit carryforwards | $7,539 | $7,136 |
| Accrued liabilities | 3,009 | 3,066 |
| Share-based compensation | 263 | 238 |
| Lease obligations | 4,611 | 4,831 |
| Other | 1,076 | 1,124 |
| Total deferred tax assets | 16,498 | 16,395 |
| Valuation allowances | (7,405) | (7,485) |
| Deferred tax assets, net of valuation allowances | 9,093 | 8,910 |
| Deferred tax liabilities: |  |  |
| Property and equipment | 4,303 | 4,813 |
| Acquired intangibles | 1,096 | 898 |
| Inventory | 3,336 | 3,035 |
| Lease right of use assets | 4,816 | 4,941 |
| Mark-to-market investments | 353 | 322 |
| Other | 460 | 486 |
| Total deferred tax liabilities | 14,364 | 14,495 |
| Net deferred tax liabilities | $5,271 | $5,585 |
````

**#6 `WMT_FY2025_2025-01-31:246`** (gold #1)

````text
ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Net Cash Used in Investing Activities
Net cash used in investing activities was $21.4 billion, $21.3 billion and $17.7 billion for fiscal 2025, 2024 and 2023, respectively, and generally consisted of capital expenditures. Net cash used in investing activities increased $0.1 billion for fiscal 2025 when compared to the previous fiscal year. The increase is primarily due to increased purchases of property and equipment as well as the acquisition of VIZIO for net consideration of $1.9 billion, partially offset by net proceeds received from sales of certain strategic investments, including $3.6 billion related to the sale of our JD.com investment. Net cash used in investing activities increased $3.6 billion for fiscal 2024 when compared to the previous fiscal year, primarily due to increased payments for property and equipment. Capital expenditures Refer to the "Strategic Capital Allocation" section in our Company Performance Metrics for capital expenditure detail for fiscal 2025 and 2024. For the fiscal year ending January 31, 2026 ("fiscal 2026"), we project capital expenditures will be approximately $21 billion to $25 billion, with a focus on technology, supply chain and customer-facing initiatives.
````

**#7 `WMT_FY2025_2025-01-31:294`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Consolidated Balance Sheets (table)
|  | As of January 31, |  |
|---|---|---|
| (Amounts in millions) | 2025 | 2024 |
| ASSETS |  |  |
| Current assets: |  |  |
| Cash and cash equivalents | $9,037 | $9,867 |
| Receivables, net | 9,975 | 8,796 |
| Inventories | 56,435 | 54,892 |
| Prepaid expenses and other | 4,011 | 3,322 |
| Total current assets | 79,458 | 76,877 |
| Property and equipment, net | 119,993 | 110,810 |
| Operating lease right-of-use assets | 13,599 | 13,673 |
| Finance lease right-of-use assets, net | 6,112 | 5,855 |
| Goodwill | 28,792 | 28,113 |
| Other long-term assets | 12,869 | 17,071 |
| Total assets | $260,823 | $252,399 |
| LIABILITIES, REDEEMABLE NONCONTROLLING INTEREST, AND SHAREHOLDERS' EQUITY |  |  |
| Current liabilities: |  |  |
| Short-term borrowings | $3,068 | $878 |
| Accounts payable | 58,666 | 56,812 |
| Accrued liabilities | 29,345 | 28,759 |
| Accrued income taxes | 608 | 307 |
| Long-term debt due within one year | 2,598 | 3,447 |
````

</details>

RQ2 citation match (section level): `cited=[('WMT', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Walmart Inc.'s net property and equipment increased by $9,183 million from fiscal 2024 to fiscal 2025, rising from $110,810 million to $119,993 million [WMT FY2025, Item 8, WMT_FY2025_2025-01-31:317]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 1.

**Generated answer**

> Walmart Inc.'s net property and equipment increased by $9,183 million from fiscal 2024 to fiscal 2025, rising from $110,810 million to $119,993 million [WMT FY2025, Item 8, WMT_FY2025_2025-01-31:317].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-WMT-2025` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2025,2025-01-31,680985000000,19436000000,29348000000,260823000… |
| 2 | `WMT_FY2025_2025-01-31:317` | Item 8 › Property and Equipment | ✓ | #1 | \| \| Estimated Useful Lives \| As of January 31, \| \| \|---\|---\|---\|---\| \| (Dollars in millions) \| (in Years) \| 2025 \| 2024 \| \| Land \| N/A \| $19,342 \| $19,562 \| \| Buildings and improvements \| 3 - 40 \| 117,973 \| 111,767 \| \| F… |
| 3 | `WMT_FY2025_2025-01-31:443` | Item 8 › Note 12. Segments and Disaggregated Revenue |  | #1 | Total revenues and long-lived assets, consisting primarily of net property and equipment and lease right-of-use assets, aggregated by the Company's U.S. and non-U.S. operations, are as follows: |
| 4 | `WMT_FY2025_2025-01-31:304` | Item 8 › Consolidated Statements of Cash Flows |  | #1 | \| \| Fiscal Years Ended January 31, \| \| \| \|---\|---\|---\|---\| \| Payments for property and equipment \| (23,783) \| (20,606) \| (16,857) \| \| Proceeds from the disposal of property and equipment \| 432 \| 250 \| 170 \| \| Proceeds fr… |
| 5 | `WMT_FY2025_2025-01-31:217` | Item 7 › Strategic Capital Allocation |  | #1 | \| \| Fiscal Years Ended January 31, \| \| \| \|---\|---\|---\|---\| \| (Amounts in millions) \| 2025 \| 2024 \| 2023 \| \| Net cash provided by operating activities \| $36,443 \| $35,726 \| $28,841 \| \| Payments for property and equipment … |
| 6 | `WMT_FY2025_2025-01-31:404` | Item 8 › Note 9. Taxes |  | #1 | \| \| January 31, \| \| \|---\|---\|---\| \| (Amounts in millions) \| 2025 \| 2024 \| \| Deferred tax assets: \| \| \| \| Loss and tax credit carryforwards \| $7,539 \| $7,136 \| \| Accrued liabilities \| 3,009 \| 3,066 \| \| Share-based compens… |
| 7 | `WMT_FY2025_2025-01-31:246` | Item 7 › Net Cash Used in Investing Activities |  | #1 | Net cash used in investing activities was $21.4 billion, $21.3 billion and $17.7 billion for fiscal 2025, 2024 and 2023, respectively, and generally consisted of capital expenditures. Net cash used in investing activitie… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `WMT_FY2025_2025-01-31:317`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Property and Equipment (table)
|  | Estimated Useful Lives | As of January 31, |  |
|---|---|---|---|
| (Dollars in millions) | (in Years) | 2025 | 2024 |
| Land | N/A | $19,342 | $19,562 |
| Buildings and improvements | 3 - 40 | 117,973 | 111,767 |
| Fixtures and equipment | 2 - 30 | 76,226 | 72,161 |
| Transportation equipment | 3 - 15 | 2,673 | 2,979 |
| Construction in progress | N/A | 15,403 | 13,390 |
| Property and equipment |  | 231,617 | 219,859 |
| Accumulated depreciation |  | (111,624) | (109,049) |
| Property and equipment, net |  | $119,993 | $110,810 |
````

**#3 `WMT_FY2025_2025-01-31:443`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 12. Segments and Disaggregated Revenue
Total revenues and long-lived assets, consisting primarily of net property and equipment and lease right-of-use assets, aggregated by the Company's U.S. and non-U.S. operations, are as follows:
````

**#4 `WMT_FY2025_2025-01-31:304`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Consolidated Statements of Cash Flows (table)
|  | Fiscal Years Ended January 31, |  |  |
|---|---|---|---|
| Payments for property and equipment | (23,783) | (20,606) | (16,857) |
| Proceeds from the disposal of property and equipment | 432 | 250 | 170 |
| Proceeds from disposal of certain strategic investments | 4,080 | — | — |
| Payments for business acquisitions, net of cash acquired | (1,896) | (9) | (740) |
| Other investing activities | (212) | (922) | (295) |
| Net cash used in investing activities | (21,379) | (21,287) | (17,722) |
| Cash flows from financing activities: |  |  |  |
| Net change in short-term borrowings | 2,212 | 512 | (34) |
| Proceeds from issuance of long-term debt | — | 4,967 | 5,041 |
| Repayments of long-term debt | (3,468) | (4,217) | (2,689) |
| Dividends paid | (6,688) | (6,140) | (6,114) |
| Purchase of Company stock | (4,494) | (2,779) | (9,920) |
| Dividends paid to noncontrolling interest | (576) | (763) | (444) |
| Purchase of noncontrolling interest | — | (3,462) | (827) |
````

**#5 `WMT_FY2025_2025-01-31:217`** (gold #1)

````text
ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Strategic Capital Allocation (table)
|  | Fiscal Years Ended January 31, |  |  |
|---|---|---|---|
| (Amounts in millions) | 2025 | 2024 | 2023 |
| Net cash provided by operating activities | $36,443 | $35,726 | $28,841 |
| Payments for property and equipment | (23,783) | (20,606) | (16,857) |
| Free cash flow | $12,660 | $15,120 | $11,984 |
| Net cash used in investing activities(1) | $(21,379) | $(21,287) | $(17,722) |
| Net cash used in financing activities | (14,822) | (13,414) | (17,039) |
````

**#6 `WMT_FY2025_2025-01-31:404`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 9. Taxes (table)
|  | January 31, |  |
|---|---|---|
| (Amounts in millions) | 2025 | 2024 |
| Deferred tax assets: |  |  |
| Loss and tax credit carryforwards | $7,539 | $7,136 |
| Accrued liabilities | 3,009 | 3,066 |
| Share-based compensation | 263 | 238 |
| Lease obligations | 4,611 | 4,831 |
| Other | 1,076 | 1,124 |
| Total deferred tax assets | 16,498 | 16,395 |
| Valuation allowances | (7,405) | (7,485) |
| Deferred tax assets, net of valuation allowances | 9,093 | 8,910 |
| Deferred tax liabilities: |  |  |
| Property and equipment | 4,303 | 4,813 |
| Acquired intangibles | 1,096 | 898 |
| Inventory | 3,336 | 3,035 |
| Lease right of use assets | 4,816 | 4,941 |
| Mark-to-market investments | 353 | 322 |
| Other | 460 | 486 |
| Total deferred tax liabilities | 14,364 | 14,495 |
| Net deferred tax liabilities | $5,271 | $5,585 |
````

**#7 `WMT_FY2025_2025-01-31:246`** (gold #1)

````text
ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Net Cash Used in Investing Activities
Net cash used in investing activities was $21.4 billion, $21.3 billion and $17.7 billion for fiscal 2025, 2024 and 2023, respectively, and generally consisted of capital expenditures. Net cash used in investing activities increased $0.1 billion for fiscal 2025 when compared to the previous fiscal year. The increase is primarily due to increased purchases of property and equipment as well as the acquisition of VIZIO for net consideration of $1.9 billion, partially offset by net proceeds received from sales of certain strategic investments, including $3.6 billion related to the sale of our JD.com investment. Net cash used in investing activities increased $3.6 billion for fiscal 2024 when compared to the previous fiscal year, primarily due to increased payments for property and equipment. Capital expenditures Refer to the "Strategic Capital Allocation" section in our Company Performance Metrics for capital expenditure detail for fiscal 2025 and 2024. For the fiscal year ending January 31, 2026 ("fiscal 2026"), we project capital expenditures will be approximately $21 billion to $25 billion, with a focus on technology, supply chain and customer-facing initiatives.
````

</details>

RQ2 citation match (section level): `cited=[('WMT', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Walmart Inc.'s net property and equipment increased by $9,183 million from fiscal 2024 to fiscal 2025, rising from $110,810 million to $119,993 million [WMT FY2025, Item 8, WMT_FY2025_2025-01-31:317]. | None |  |

</details>
