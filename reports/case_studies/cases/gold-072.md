# gold-072: Cross-year table

[← all cases](../README.md) · company: Apple Inc. (AAPL) · fiscal year: 2021 · recipe `cross_year_table` · hop `multi` · answer type `numeric` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> By what percentage did Apple Inc.'s total property, plant and equipment, net decrease between fiscal year 2018 and fiscal year 2021?

**Gold answer**

> 4.51%

**Program**: `subtract(41304, 39440), divide(#0, 41304), multiply(#1, 100)` → `4.5128801084640715`

**Gold numbers** (RQ2 numeric_accuracy targets): 4.51%

**Gold evidence**

1. `AAPL_FY2021_2021-09-25` · Item 8. Financial Statements and Supplementary Data › Property, Plant and Equipment, Net · table

   > Total property, plant and equipment, net | $39,440 | $36,766

2. `AAPL_FY2018_2018-09-29` · Item 8. Financial Statements and Supplementary Data › Property, Plant and Equipment, Net · table

   > Total property, plant and equipment, net | $41,304 | $33,783

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 10 | 8 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 1.00 | 0.33 | 0.70 | 0.42 |
| gold evidence first rank | #1: 1, #2: 1 | #1: 4, #2: 4 | #1: 1, #2: 1 | #1: 3, #2: 3 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 1.00 | 1.00 | 1.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 1 |
| tokens | 2353 | 1758 | 12036 | 4660 |
| cost (USD) | 0.0004 | 0.0003 | 0.0460 | 0.0165 |
| latency (s) | 2.9 | 6.3 | 22.0 | 7.1 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Apple’s total property, plant and equipment, net was **$41,304 million** in fiscal **2018** and **$39,440 million** in fiscal **2021** [2][1].
>
> Percentage decrease:
>
> \[
> \frac{41{,}304 - 39{,}440}{41{,}304} \times 100 \approx 4.5\%
> \]
>
> So, Apple’s total property, plant and equipment, net **decreased by approximately 4.5%** between fiscal 2018 and fiscal 2021 [2][1].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2021_2021-09-25:218` | Item 8 › Property, Plant and Equipment, Net | ✓ | #1, #2 | \| \| 2021 \| 2020 \| \|---\|---\|---\| \| Land and buildings \| $20,041 \| $17,952 \| \| Machinery, equipment and internal-use software \| 78,659 \| 75,291 \| \| Leasehold improvements \| 11,023 \| 10,283 \| \| Gross property, plant and equ… |
| 2 | `AAPL_FY2018_2018-09-29:287` | Item 8 › Property, Plant and Equipment, Net | ✓ | #1, #2 | \| \| 2018 \| 2017 \| \|---\|---\|---\| \| Land and buildings \| $16,216 \| $13,587 \| \| Machinery, equipment and internal-use software \| 65,982 \| 54,210 \| \| Leasehold improvements \| 8,205 \| 7,279 \| \| Gross property, plant and equip… |
| 3 | `AAPL_FY2021_2021-09-25:187` | Item 8 › Property, Plant and Equipment |  |  | Depreciation on property, plant and equipment is recognized on a straight-line basis over the estimated useful lives of the assets, which for buildings is the lesser of 40 years or the remaining life of the building; bet… |
| 4 | `AAPL_FY2018_2018-09-29:256` | Item 8 › Property, Plant and Equipment |  |  | Depreciation on property, plant and equipment is recognized on a straight-line basis over the estimated useful lives of the assets, which for buildings is the lesser of 30 years or the remaining life of the underlying bu… |
| 5 | `AAPL_FY2021_2021-09-25:285` | Item 8 › Note 11 – Segment Information and Geographic Data |  |  | Apple Inc. \| 2021 Form 10-K \| 50 The U.S. and China were the only countries that accounted for more than 10% of the Company’s net sales in 2021, 2020 and 2019. There was no single customer that accounted for more than 10… |
| 6 | `AAPL_FY2018_2018-09-29:128` | Item 7 › Overview and Highlights |  |  | \| \| 2018 \| Change \| 2017 \| Change \| 2016 \| \|---\|---\|---\|---\|---\|---\| \| Total net sales \| $265,595 \| 16% \| $229,234 \| 6% \| $215,639 \| \| Unit Sales by Product: \| \| \| \| \| \| \| iPhone \| 217,722 \| —% \| 216,756 \| 2% \| 211,884 \|… |
| 7 | `AAPL_FY2021_2021-09-25:121` | Item 7 › Products and Services Performance |  |  | \| \| 2021 \| Change \| 2020 \| Change \| 2019 \| \|---\|---\|---\|---\|---\|---\| \| Net sales by category: \| \| \| \| \| \| \| iPhone (1) \| $191,973 \| 39% \| $137,781 \| (3)% \| $142,381 \| \| Mac (1) \| 35,190 \| 23% \| 28,622 \| 11% \| 25,740 \| \| … |
| 8 | `AAPL_FY2021_2021-09-25:199` | Item 8 › Disaggregated Revenue |  |  | \| \| 2021 \| 2020 \| 2019 \| \|---\|---\|---\|---\| \| iPhone (1) \| $191,973 \| $137,781 \| $142,381 \| \| Mac (1) \| 35,190 \| 28,622 \| 25,740 \| \| iPad (1) \| 31,862 \| 23,724 \| 21,280 \| \| Wearables, Home and Accessories (1)(2) \| 38,367 … |
| 9 | `AAPL_FY2021_2021-09-25:158` | Item 8 › CONSOLIDATED STATEMENTS OF OPERATIONS |  |  | \| \| Years ended \| \| \| \|---\|---\|---\|---\| \| \| September 25, 2021 \| September 26, 2020 \| September 28, 2019 \| \| Net sales: \| \| \| \| \| Products \| $297,392 \| $220,747 \| $213,883 \| \| Services \| 68,425 \| 53,768 \| 46,291 \| \| Tota… |
| 10 | `AAPL_FY2018_2018-09-29:133` | Item 7 › Product Performance |  |  | \| \| 2018 \| Change \| 2017 \| Change \| 2016 \| \|---\|---\|---\|---\|---\|---\| \| Net sales \| $18,805 \| (2)% \| $19,222 \| (7)% \| $20,628 \| \| Percentage of total net sales \| 7% \| \| 8% \| \| 10% \| \| Unit sales \| 43,535 \| —% \| 43,753 \| (… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2021_2021-09-25:218`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Property, Plant and Equipment, Net (table)
|  | 2021 | 2020 |
|---|---|---|
| Land and buildings | $20,041 | $17,952 |
| Machinery, equipment and internal-use software | 78,659 | 75,291 |
| Leasehold improvements | 11,023 | 10,283 |
| Gross property, plant and equipment | 109,723 | 103,526 |
| Accumulated depreciation and amortization | (70,283) | (66,760) |
| Total property, plant and equipment, net | $39,440 | $36,766 |
````

**#2 `AAPL_FY2018_2018-09-29:287`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Property, Plant and Equipment, Net (table)
|  | 2018 | 2017 |
|---|---|---|
| Land and buildings | $16,216 | $13,587 |
| Machinery, equipment and internal-use software | 65,982 | 54,210 |
| Leasehold improvements | 8,205 | 7,279 |
| Gross property, plant and equipment | 90,403 | 75,076 |
| Accumulated depreciation and amortization | (49,099) | (41,293) |
| Total property, plant and equipment, net | $41,304 | $33,783 |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Apple’s property, plant and equipment, net was **$41,304 million** in fiscal 2018 and **$39,440 million** in fiscal 2021 [5][4].
>
> Percentage decrease:
>
> \[
> \frac{41{,}304 - 39{,}440}{41{,}304} \times 100 \approx 4.5\%
> \]
>
> So, Apple’s total property, plant and equipment, net **decreased by approximately 4.5%** between fiscal 2018 and fiscal 2021. [5][4]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2018_2018-09-29:256` | Item 8 › Property, Plant and Equipment |  |  | Depreciation on property, plant and equipment is recognized on a straight-line basis over the estimated useful lives of the assets, which for buildings is the lesser of 30 years or the remaining life of the underlying bu… |
| 2 | `AAPL_FY2021_2021-09-25:187` | Item 8 › Property, Plant and Equipment |  |  | Depreciation on property, plant and equipment is recognized on a straight-line basis over the estimated useful lives of the assets, which for buildings is the lesser of 40 years or the remaining life of the building; bet… |
| 3 | `AAPL_FY2021_2021-09-25:119` | Item 7 › Fiscal Year Highlights |  |  | The extent of the continuing impact of the COVID-19 pandemic on the Company’s operational and financial performance is uncertain and will depend on many factors outside the Company’s control, including the timing, extent… |
| 4 | `AAPL_FY2021_2021-09-25:166` | Item 8 › CONSOLIDATED BALANCE SHEETS | ✓ | #1, #2 | \| \| September 25, 2021 \| September 26, 2020 \| \|---\|---\|---\| \| ASSETS: \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $34,940 \| $38,016 \| \| Marketable securities \| 27,699 \| 52,927 \| \| Accounts receivable, net… |
| 5 | `AAPL_FY2018_2018-09-29:224` | Item 8 › CONSOLIDATED BALANCE SHEETS | ✓ | #1, #2 | \| \| September 29, 2018 \| September 30, 2017 \| \|---\|---\|---\| \| ASSETS: \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $25,913 \| $20,289 \| \| Marketable securities \| 40,388 \| 53,892 \| \| Accounts receivable, net… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#4 `AAPL_FY2021_2021-09-25:166`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > CONSOLIDATED BALANCE SHEETS (table)
|  | September 25, 2021 | September 26, 2020 |
|---|---|---|
| ASSETS: |  |  |
| Current assets: |  |  |
| Cash and cash equivalents | $34,940 | $38,016 |
| Marketable securities | 27,699 | 52,927 |
| Accounts receivable, net | 26,278 | 16,120 |
| Inventories | 6,580 | 4,061 |
| Vendor non-trade receivables | 25,228 | 21,325 |
| Other current assets | 14,111 | 11,264 |
| Total current assets | 134,836 | 143,713 |
| Non-current assets: |  |  |
| Marketable securities | 127,877 | 100,887 |
| Property, plant and equipment, net | 39,440 | 36,766 |
| Other non-current assets | 48,849 | 42,522 |
| Total non-current assets | 216,166 | 180,175 |
| Total assets | $351,002 | $323,888 |
| LIABILITIES AND SHAREHOLDERS’ EQUITY: |  |  |
| Current liabilities: |  |  |
| Accounts payable | $54,763 | $42,296 |
| Other current liabilities | 47,493 | 42,684 |
| Deferred revenue | 7,612 | 6,643 |
| Commercial paper | 6,000 | 4,996 |
| Term debt | 9,613 | 8,773 |
| Total current liabilities | 125,481 | 105,392 |
````

**#5 `AAPL_FY2018_2018-09-29:224`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > CONSOLIDATED BALANCE SHEETS (table)
|  | September 29, 2018 | September 30, 2017 |
|---|---|---|
| ASSETS: |  |  |
| Current assets: |  |  |
| Cash and cash equivalents | $25,913 | $20,289 |
| Marketable securities | 40,388 | 53,892 |
| Accounts receivable, net | 23,186 | 17,874 |
| Inventories | 3,956 | 4,855 |
| Vendor non-trade receivables | 25,809 | 17,799 |
| Other current assets | 12,087 | 13,936 |
| Total current assets | 131,339 | 128,645 |
| Non-current assets: |  |  |
| Marketable securities | 170,799 | 194,714 |
| Property, plant and equipment, net | 41,304 | 33,783 |
| Other non-current assets | 22,283 | 18,177 |
| Total non-current assets | 234,386 | 246,674 |
| Total assets | $365,725 | $375,319 |
| LIABILITIES AND SHAREHOLDERS’ EQUITY: |  |  |
| Current liabilities: |  |  |
| Accounts payable | $55,888 | $44,242 |
| Other current liabilities | 32,687 | 30,551 |
| Deferred revenue | 7,543 | 7,548 |
| Commercial paper | 11,964 | 11,977 |
| Term debt | 8,784 | 6,496 |
| Total current liabilities | 116,866 | 100,814 |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Apple Inc.'s total property, plant and equipment, net was $41,304 in fiscal 2018 and $39,440 in fiscal 2021 [AAPL FY2018, Item 8, AAPL_FY2018_2018-09-29:287] [AAPL FY2021, Item 8, AAPL_FY2021_2021-09-25:218].  
> The decrease was $1,864, which equals approximately 4.5% of the 2018 amount (($41,304 - $39,440) / $41,304) [AAPL FY2018, Item 8, AAPL_FY2018_2018-09-29:287] [AAPL FY2021, Item 8, AAPL_FY2021_2021-09-25:218].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2018_2018-09-29:287` | Item 8 › Property, Plant and Equipment, Net | ✓ | #1, #2 | \| \| 2018 \| 2017 \| \|---\|---\|---\| \| Land and buildings \| $16,216 \| $13,587 \| \| Machinery, equipment and internal-use software \| 65,982 \| 54,210 \| \| Leasehold improvements \| 8,205 \| 7,279 \| \| Gross property, plant and equip… |
| 2 | `AAPL_FY2021_2021-09-25:218` | Item 8 › Property, Plant and Equipment, Net | ✓ | #1, #2 | \| \| 2021 \| 2020 \| \|---\|---\|---\| \| Land and buildings \| $20,041 \| $17,952 \| \| Machinery, equipment and internal-use software \| 78,659 \| 75,291 \| \| Leasehold improvements \| 11,023 \| 10,283 \| \| Gross property, plant and equ… |
| 3 | `AAPL_FY2018_2018-09-29:256` | Item 8 › Property, Plant and Equipment |  |  | Depreciation on property, plant and equipment is recognized on a straight-line basis over the estimated useful lives of the assets, which for buildings is the lesser of 30 years or the remaining life of the underlying bu… |
| 4 | `AAPL_FY2018_2018-09-29:288` | Item 8 › Property, Plant and Equipment, Net |  |  | Apple Inc. \| 2018 Form 10-K \| 51 |
| 5 | `AAPL_FY2021_2021-09-25:187` | Item 8 › Property, Plant and Equipment |  |  | Depreciation on property, plant and equipment is recognized on a straight-line basis over the estimated useful lives of the assets, which for buildings is the lesser of 40 years or the remaining life of the building; bet… |
| 6 | `AAPL_FY2018_2018-09-29:363` | Item 8 › Note 10 – Segment Information and Geographic Data |  |  | \| \| 2018 \| 2017 \| 2016 \| \|---\|---\|---\|---\| \| Net sales: \| \| \| \| \| U.S. \| $98,061 \| $84,339 \| $75,667 \| \| China (1) \| 51,942 \| 44,764 \| 48,492 \| \| Other countries \| 115,592 \| 100,131 \| 91,480 \| \| Total net sales \| $265,59… |
| 7 | `AAPL_FY2021_2021-09-25:239` | Item 8 › Note 6 – Leases |  | #1, #2 | \| Lease-Related Assets and Liabilities \| Financial Statement Line Items \| 2021 \| 2020 \| \|---\|---\|---\|---\| \| Right-of-use assets: \| \| \| \| \| Operating leases \| Other non-current assets \| $10,087 \| $8,570 \| \| Finance leases… |
| 8 | `AAPL_FY2021_2021-09-25:166` | Item 8 › CONSOLIDATED BALANCE SHEETS |  | #1, #2 | \| \| September 25, 2021 \| September 26, 2020 \| \|---\|---\|---\| \| ASSETS: \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $34,940 \| $38,016 \| \| Marketable securities \| 27,699 \| 52,927 \| \| Accounts receivable, net… |
| 9 | `AAPL_FY2018_2018-09-29:224` | Item 8 › CONSOLIDATED BALANCE SHEETS |  | #1, #2 | \| \| September 29, 2018 \| September 30, 2017 \| \|---\|---\|---\| \| ASSETS: \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $25,913 \| $20,289 \| \| Marketable securities \| 40,388 \| 53,892 \| \| Accounts receivable, net… |
| 10 | `AAPL_FY2021_2021-09-25:286` | Item 8 › Note 11 – Segment Information and Geographic Data |  |  | \| \| 2021 \| 2020 \| 2019 \| \|---\|---\|---\|---\| \| Net sales: \| \| \| \| \| U.S. \| $133,803 \| $109,197 \| $102,266 \| \| China (1) \| 68,366 \| 40,308 \| 43,678 \| \| Other countries \| 163,648 \| 125,010 \| 114,230 \| \| Total net sales \| $36… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2018_2018-09-29:287`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Property, Plant and Equipment, Net (table)
|  | 2018 | 2017 |
|---|---|---|
| Land and buildings | $16,216 | $13,587 |
| Machinery, equipment and internal-use software | 65,982 | 54,210 |
| Leasehold improvements | 8,205 | 7,279 |
| Gross property, plant and equipment | 90,403 | 75,076 |
| Accumulated depreciation and amortization | (49,099) | (41,293) |
| Total property, plant and equipment, net | $41,304 | $33,783 |
````

**#2 `AAPL_FY2021_2021-09-25:218`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Property, Plant and Equipment, Net (table)
|  | 2021 | 2020 |
|---|---|---|
| Land and buildings | $20,041 | $17,952 |
| Machinery, equipment and internal-use software | 78,659 | 75,291 |
| Leasehold improvements | 11,023 | 10,283 |
| Gross property, plant and equipment | 109,723 | 103,526 |
| Accumulated depreciation and amortization | (70,283) | (66,760) |
| Total property, plant and equipment, net | $39,440 | $36,766 |
````

**#7 `AAPL_FY2021_2021-09-25:239`** (gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Note 6 – Leases (table)
| Lease-Related Assets and Liabilities | Financial Statement Line Items | 2021 | 2020 |
|---|---|---|---|
| Right-of-use assets: |  |  |  |
| Operating leases | Other non-current assets | $10,087 | $8,570 |
| Finance leases | Property, plant and equipment, net | 861 | 629 |
| Total right-of-use assets |  | $10,948 | $9,199 |
| Lease liabilities: |  |  |  |
| Operating leases | Other current liabilities | $1,449 | $1,436 |
|  | Other non-current liabilities | 9,506 | 7,745 |
| Finance leases | Other current liabilities | 79 | 24 |
|  | Other non-current liabilities | 769 | 637 |
| Total lease liabilities |  | $11,803 | $9,842 |
````

**#8 `AAPL_FY2021_2021-09-25:166`** (gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > CONSOLIDATED BALANCE SHEETS (table)
|  | September 25, 2021 | September 26, 2020 |
|---|---|---|
| ASSETS: |  |  |
| Current assets: |  |  |
| Cash and cash equivalents | $34,940 | $38,016 |
| Marketable securities | 27,699 | 52,927 |
| Accounts receivable, net | 26,278 | 16,120 |
| Inventories | 6,580 | 4,061 |
| Vendor non-trade receivables | 25,228 | 21,325 |
| Other current assets | 14,111 | 11,264 |
| Total current assets | 134,836 | 143,713 |
| Non-current assets: |  |  |
| Marketable securities | 127,877 | 100,887 |
| Property, plant and equipment, net | 39,440 | 36,766 |
| Other non-current assets | 48,849 | 42,522 |
| Total non-current assets | 216,166 | 180,175 |
| Total assets | $351,002 | $323,888 |
| LIABILITIES AND SHAREHOLDERS’ EQUITY: |  |  |
| Current liabilities: |  |  |
| Accounts payable | $54,763 | $42,296 |
| Other current liabilities | 47,493 | 42,684 |
| Deferred revenue | 7,612 | 6,643 |
| Commercial paper | 6,000 | 4,996 |
| Term debt | 9,613 | 8,773 |
| Total current liabilities | 125,481 | 105,392 |
````

**#9 `AAPL_FY2018_2018-09-29:224`** (gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > CONSOLIDATED BALANCE SHEETS (table)
|  | September 29, 2018 | September 30, 2017 |
|---|---|---|
| ASSETS: |  |  |
| Current assets: |  |  |
| Cash and cash equivalents | $25,913 | $20,289 |
| Marketable securities | 40,388 | 53,892 |
| Accounts receivable, net | 23,186 | 17,874 |
| Inventories | 3,956 | 4,855 |
| Vendor non-trade receivables | 25,809 | 17,799 |
| Other current assets | 12,087 | 13,936 |
| Total current assets | 131,339 | 128,645 |
| Non-current assets: |  |  |
| Marketable securities | 170,799 | 194,714 |
| Property, plant and equipment, net | 41,304 | 33,783 |
| Other non-current assets | 22,283 | 18,177 |
| Total non-current assets | 234,386 | 246,674 |
| Total assets | $365,725 | $375,319 |
| LIABILITIES AND SHAREHOLDERS’ EQUITY: |  |  |
| Current liabilities: |  |  |
| Accounts payable | $55,888 | $44,242 |
| Other current liabilities | 32,687 | 30,551 |
| Deferred revenue | 7,543 | 7,548 |
| Commercial paper | 11,964 | 11,977 |
| Term debt | 8,784 | 6,496 |
| Total current liabilities | 116,866 | 100,814 |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 7, verified 7, ungrounded 0, uncited 0, derived 2; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Apple Inc.'s total property, plant and equipment, net was $41,304 in fiscal 2018 and $39,440 in fiscal 2021 [AAPL FY2018, Item 8, AAPL_FY2018_2018-09-29:287] [AAPL FY2021, Item 8, AAPL_FY2021_2021-09-25:218]. | None |  |
| The decrease was $1,864, which equals approximately 4.5% of the 2018 amount (($41,304 - $39,440) / $41,304) [AAPL FY2018, Item 8, AAPL_FY2018_2018-09-29:287] [AAPL FY2021, Item 8, AAPL_FY2021_2021-09-25:218]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 2.

**Generated answer**

> Apple Inc.'s total property, plant and equipment, net decreased from $41,304 in 2018 to $39,440 in 2021 [AAPL FY2018, Item 8, AAPL_FY2018_2018-09-29:287] [AAPL FY2021, Item 8, AAPL_FY2021_2021-09-25:218].  
> The decrease was approximately 4.5%, calculated as ($41,304 - $39,440) / $41,304 × 100 [AAPL FY2018, Item 8, AAPL_FY2018_2018-09-29:287] [AAPL FY2021, Item 8, AAPL_FY2021_2021-09-25:218].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-AAPL-2018` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2018,2018-09-29,265595000000,59531000000,70898000000,365725000… |
| 2 | `F-AAPL-2021` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2021,2021-09-25,365817000000,94680000000,108949000000,35100200… |
| 3 | `AAPL_FY2018_2018-09-29:287` | Item 8 › Property, Plant and Equipment, Net | ✓ | #1, #2 | \| \| 2018 \| 2017 \| \|---\|---\|---\| \| Land and buildings \| $16,216 \| $13,587 \| \| Machinery, equipment and internal-use software \| 65,982 \| 54,210 \| \| Leasehold improvements \| 8,205 \| 7,279 \| \| Gross property, plant and equip… |
| 4 | `AAPL_FY2021_2021-09-25:218` | Item 8 › Property, Plant and Equipment, Net | ✓ | #1, #2 | \| \| 2021 \| 2020 \| \|---\|---\|---\| \| Land and buildings \| $20,041 \| $17,952 \| \| Machinery, equipment and internal-use software \| 78,659 \| 75,291 \| \| Leasehold improvements \| 11,023 \| 10,283 \| \| Gross property, plant and equ… |
| 5 | `AAPL_FY2018_2018-09-29:256` | Item 8 › Property, Plant and Equipment |  |  | Depreciation on property, plant and equipment is recognized on a straight-line basis over the estimated useful lives of the assets, which for buildings is the lesser of 30 years or the remaining life of the underlying bu… |
| 6 | `AAPL_FY2018_2018-09-29:288` | Item 8 › Property, Plant and Equipment, Net |  |  | Apple Inc. \| 2018 Form 10-K \| 51 |
| 7 | `AAPL_FY2021_2021-09-25:187` | Item 8 › Property, Plant and Equipment |  |  | Depreciation on property, plant and equipment is recognized on a straight-line basis over the estimated useful lives of the assets, which for buildings is the lesser of 40 years or the remaining life of the building; bet… |
| 8 | `AAPL_FY2018_2018-09-29:363` | Item 8 › Note 10 – Segment Information and Geographic Data |  |  | \| \| 2018 \| 2017 \| 2016 \| \|---\|---\|---\|---\| \| Net sales: \| \| \| \| \| U.S. \| $98,061 \| $84,339 \| $75,667 \| \| China (1) \| 51,942 \| 44,764 \| 48,492 \| \| Other countries \| 115,592 \| 100,131 \| 91,480 \| \| Total net sales \| $265,59… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `AAPL_FY2018_2018-09-29:287`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Property, Plant and Equipment, Net (table)
|  | 2018 | 2017 |
|---|---|---|
| Land and buildings | $16,216 | $13,587 |
| Machinery, equipment and internal-use software | 65,982 | 54,210 |
| Leasehold improvements | 8,205 | 7,279 |
| Gross property, plant and equipment | 90,403 | 75,076 |
| Accumulated depreciation and amortization | (49,099) | (41,293) |
| Total property, plant and equipment, net | $41,304 | $33,783 |
````

**#4 `AAPL_FY2021_2021-09-25:218`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Property, Plant and Equipment, Net (table)
|  | 2021 | 2020 |
|---|---|---|
| Land and buildings | $20,041 | $17,952 |
| Machinery, equipment and internal-use software | 78,659 | 75,291 |
| Leasehold improvements | 11,023 | 10,283 |
| Gross property, plant and equipment | 109,723 | 103,526 |
| Accumulated depreciation and amortization | (70,283) | (66,760) |
| Total property, plant and equipment, net | $39,440 | $36,766 |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Apple Inc.'s total property, plant and equipment, net decreased from $41,304 in 2018 to $39,440 in 2021 [AAPL FY2018, Item 8, AAPL_FY2018_2018-09-29:287] [AAPL FY2021, Item 8, AAPL_FY2021_2021-09-25:218]. | None |  |
| The decrease was approximately 4.5%, calculated as ($41,304 - $39,440) / $41,304 × 100 [AAPL FY2018, Item 8, AAPL_FY2018_2018-09-29:287] [AAPL FY2021, Item 8, AAPL_FY2021_2021-09-25:218]. | None |  |

</details>
