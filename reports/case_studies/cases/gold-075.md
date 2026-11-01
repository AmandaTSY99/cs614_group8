# gold-075: Cross-year table

[← all cases](../README.md) · company: Tesla, Inc. (TSLA) · fiscal year: 2020 · recipe `cross_year_table` · hop `multi` · answer type `numeric` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> By how many percentage points did Tesla's Selling, General and Administrative expense as a percentage of revenues decrease from fiscal year 2017 to fiscal year 2020?

**Gold answer**

> 11 percentage points

**Program**: `subtract(21, 10)` → `11.0`

**Gold numbers** (RQ2 numeric_accuracy targets): 11 percentage points

**Gold evidence**

1. `TSLA_FY2020_2020-12-31` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Selling, General and Administrative Expense · table

   > As a percentage of revenues | 10% | 11% | 13% |  |  |  |

2. `TSLA_FY2017_2017-12-31` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Selling, General and Administrative Expense · table

   > As a percentage of revenues | 21% | 20% | 23% |  |  |  |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 15 | 8 |
| recall@5 | 1.00 | 1.00 | 1.00 | 0.50 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.53 | 0.92 | 0.42 | 0.32 |
| gold evidence first rank | #1: 2, #2: 4 | #1: 1, #2: 2 | #1: 4, #2: 3 | #1: 6, #2: 5 |
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
| tokens | 3252 | 1254 | 14851 | 5243 |
| cost (USD) | 0.0005 | 0.0002 | 0.0538 | 0.0194 |
| latency (s) | 2.0 | 6.5 | 24.6 | 9.1 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Tesla’s SG&A expense as a percentage of revenues was **21%** in fiscal year 2017 [4] and **10%** in fiscal year 2020 [2].  
>
> So, the decrease was **11 percentage points** [2][4].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2020_2020-12-31:248` | Item 7 › Cost of Revenues and Gross Margin |  |  | Cost of services and other revenue decreased $99 million, or 4%, in the year ended December 31, 2020 as compared to the year ended December 31, 2019, primarily due to a decrease in used vehicle cost of revenue driven by … |
| 2 | `TSLA_FY2020_2020-12-31:255` | Item 7 › Selling, General and Administrative Expense | ✓ | #1 | \| \| Year Ended December 31, \| \| 2020 vs. 2019 Change \| \| 2019 vs. 2018 Change \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in millions) \| 2020 \| 2019 \| 2018 \| $% \| \| $% \| \| \| Selling, general and administrative \| $… |
| 3 | `TSLA_FY2020_2020-12-31:242` | Item 7 › Cost of Revenues and Gross Margin |  |  | \| \| Year Ended December 31, \| \| 2020 vs. 2019 Change \| \| 2019 vs. 2018 Change \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in millions) \| 2020 \| 2019 \| 2018 \| $% \| \| $% \| \| \| Cost of revenues \| \| \| \| \| \| \| \| \| Auto… |
| 4 | `TSLA_FY2017_2017-12-31:285` | Item 7 › Selling, General and Administrative Expense | ✓ | #2 | \| \| Year Ended December 31, \| \| Change 2017 vs. 2016 \| \| Change 2016 vs. 2015 \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in thousands) \| 2017 \| 2016 \| 2015 \| $% \| \| $% \| \| \| Selling, general and administrative \| … |
| 5 | `TSLA_FY2020_2020-12-31:258` | Item 7 › Selling, General and Administrative Expense |  | #1 | share price. The increase in stock-based compensation was partially offset by a decrease of $90 million in customer promotional costs, facilities-related expenses and sales and marketing activities. Additionally, there w… |
| 6 | `TSLA_FY2020_2020-12-31:235` | Item 7 › Revenues |  |  | \| \| Year Ended December 31, \| \| 2020 vs. 2019 Change \| \| 2019 vs. 2018 Change \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in millions) \| 2020 \| 2019 \| 2018 \| $% \| \| $% \| \| \| Automotive sales \| $26,184 \| $19,952 \| … |
| 7 | `TSLA_FY2017_2017-12-31:273` | Item 7 › Cost of Revenues and Gross Margin |  |  | \| \| Year Ended December 31, \| \| Change 2017 vs. 2016 \| \| Change 2016 vs. 2015 \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in thousands) \| 2017 \| 2016 \| 2015 \| $% \| \| $% \| \| \| Cost of revenues \| \| \| \| \| \| \| \| \| Aut… |
| 8 | `TSLA_FY2020_2020-12-31:243` | Item 7 › Cost of Revenues and Gross Margin |  |  | \| \| Year Ended December 31, \| \| 2020 vs. 2019 Change \| \| 2019 vs. 2018 Change \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| Gross profit total automotive \| $6,977 \| $4,423 \| $4,341 \| \| \| \| \| \| Gross margin total automotive \|… |
| 9 | `TSLA_FY2017_2017-12-31:266` | Item 7 › Revenues |  |  | \| \| Year Ended December 31, \| \| Change 2017 vs. 2016 \| \| Change 2016 vs. 2015 \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in thousands) \| 2017 \| 2016 \| 2015 \| $% \| \| $% \| \| \| Automotive sales \| $8,534,752 \| $5,589… |
| 10 | `TSLA_FY2017_2017-12-31:286` | Item 7 › Selling, General and Administrative Expense |  |  | Selling, general and administrative (“SG&A”) expenses consist primarily of personnel and facilities costs related to our stores, marketing, sales, executive, finance, human resources, information technology and legal org… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `TSLA_FY2020_2020-12-31:255`** (cited, gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Selling, General and Administrative Expense (table)
|  | Year Ended December 31, |  | 2020 vs. 2019 Change |  | 2019 vs. 2018 Change |  |  |
|---|---|---|---|---|---|---|---|
| (Dollars in millions) | 2020 | 2019 | 2018 | $% |  | $% |  |
| Selling, general and administrative | $3,145 | $2,646 | $2,835 | $499 | 19% | $(189) | -7% |
| As a percentage of revenues | 10% | 11% | 13% |  |  |  |  |
````

**#4 `TSLA_FY2017_2017-12-31:285`** (cited, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Selling, General and Administrative Expense (table)
|  | Year Ended December 31, |  | Change 2017 vs. 2016 |  | Change 2016 vs. 2015 |  |  |
|---|---|---|---|---|---|---|---|
| (Dollars in thousands) | 2017 | 2016 | 2015 | $% |  | $% |  |
| Selling, general and administrative | $2,476,500 | $1,432,189 | $922,232 | $1,044,311 | 73% | $509,957 | 55% |
| As a percentage of revenues | 21% | 20% | 23% |  |  |  |  |
````

**#5 `TSLA_FY2020_2020-12-31:258`** (gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Selling, General and Administrative Expense
share price. The increase in stock-based compensation was partially offset by a decrease of $90 million in customer promotional costs, facilities-related expenses and sales and marketing activities. Additionally, there was a reduction to operating expenses for costs previously incurred in the amount of $43 million for the settlement in part of the securities litigation relating to the SolarCity acquisition (see Note 16, Commitments and Contingencies—Legal Proceedings—Securities Litigation Relating to the SolarCity Acquisition, to the consolidated financial statements included elsewhere in this Annual Report on Form 10-K). SG&A expenses as a percentage of revenue decreased from 11% to 10% in year ended December 31, 2020 as compared to the year ended December 31, 2019. The decrease is primarily from an increase in total revenues from expanding sales, partially offset by an increase in our SG&A expenses as detailed above.
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 7')] gold=[(None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Tesla’s SG&A as a percentage of revenues decreased from 21% in fiscal 2017 to 10% in fiscal 2020, a decrease of 11 percentage points [2][4].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2020_2020-12-31:258` | Item 7 › Selling, General and Administrative Expense |  | #1 | share price. The increase in stock-based compensation was partially offset by a decrease of $90 million in customer promotional costs, facilities-related expenses and sales and marketing activities. Additionally, there w… |
| 2 | `TSLA_FY2017_2017-12-31:285` | Item 7 › Selling, General and Administrative Expense | ✓ | #2 | \| \| Year Ended December 31, \| \| Change 2017 vs. 2016 \| \| Change 2016 vs. 2015 \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in thousands) \| 2017 \| 2016 \| 2015 \| $% \| \| $% \| \| \| Selling, general and administrative \| … |
| 3 | `TSLA_FY2017_2017-12-31:286` | Item 7 › Selling, General and Administrative Expense |  |  | Selling, general and administrative (“SG&A”) expenses consist primarily of personnel and facilities costs related to our stores, marketing, sales, executive, finance, human resources, information technology and legal org… |
| 4 | `TSLA_FY2020_2020-12-31:255` | Item 7 › Selling, General and Administrative Expense | ✓ | #1 | \| \| Year Ended December 31, \| \| 2020 vs. 2019 Change \| \| 2019 vs. 2018 Change \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in millions) \| 2020 \| 2019 \| 2018 \| $% \| \| $% \| \| \| Selling, general and administrative \| $… |
| 5 | `TSLA_FY2017_2017-12-31:287` | Item 7 › Selling, General and Administrative Expense |  |  | SG&A expenses increased $510.0 million, or 55%, to $1.43 billion during the year ended December 31, 2016 compared to the year ended December 31, 2015. The increase in SG&A expenses was primarily due to a $247.2 million i… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2020_2020-12-31:258`** (gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Selling, General and Administrative Expense
share price. The increase in stock-based compensation was partially offset by a decrease of $90 million in customer promotional costs, facilities-related expenses and sales and marketing activities. Additionally, there was a reduction to operating expenses for costs previously incurred in the amount of $43 million for the settlement in part of the securities litigation relating to the SolarCity acquisition (see Note 16, Commitments and Contingencies—Legal Proceedings—Securities Litigation Relating to the SolarCity Acquisition, to the consolidated financial statements included elsewhere in this Annual Report on Form 10-K). SG&A expenses as a percentage of revenue decreased from 11% to 10% in year ended December 31, 2020 as compared to the year ended December 31, 2019. The decrease is primarily from an increase in total revenues from expanding sales, partially offset by an increase in our SG&A expenses as detailed above.
````

**#2 `TSLA_FY2017_2017-12-31:285`** (cited, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Selling, General and Administrative Expense (table)
|  | Year Ended December 31, |  | Change 2017 vs. 2016 |  | Change 2016 vs. 2015 |  |  |
|---|---|---|---|---|---|---|---|
| (Dollars in thousands) | 2017 | 2016 | 2015 | $% |  | $% |  |
| Selling, general and administrative | $2,476,500 | $1,432,189 | $922,232 | $1,044,311 | 73% | $509,957 | 55% |
| As a percentage of revenues | 21% | 20% | 23% |  |  |  |  |
````

**#4 `TSLA_FY2020_2020-12-31:255`** (cited, gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Selling, General and Administrative Expense (table)
|  | Year Ended December 31, |  | 2020 vs. 2019 Change |  | 2019 vs. 2018 Change |  |  |
|---|---|---|---|---|---|---|---|
| (Dollars in millions) | 2020 | 2019 | 2018 | $% |  | $% |  |
| Selling, general and administrative | $3,145 | $2,646 | $2,835 | $499 | 19% | $(189) | -7% |
| As a percentage of revenues | 10% | 11% | 13% |  |  |  |  |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 7')] gold=[(None, 'Item 7')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 15, cited: 2.

**Generated answer**

> Tesla's Selling, General and Administrative expense as a percentage of revenues was 21% in fiscal year 2017 and 10% in fiscal year 2020, so it decreased by 11 percentage points. [TSLA FY2017, Item 7, TSLA_FY2017_2017-12-31:285] [TSLA FY2020, Item 7, TSLA_FY2020_2020-12-31:255]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2017_2017-12-31:286` | Item 7 › Selling, General and Administrative Expense |  |  | Selling, general and administrative (“SG&A”) expenses consist primarily of personnel and facilities costs related to our stores, marketing, sales, executive, finance, human resources, information technology and legal org… |
| 2 | `TSLA_FY2020_2020-12-31:256` | Item 7 › Selling, General and Administrative Expense |  |  | Selling, general and administrative (“SG&A”) expenses generally consist of personnel and facilities costs related to our stores, marketing, sales, executive, finance, human resources, information technology and legal org… |
| 3 | `TSLA_FY2017_2017-12-31:285` | Item 7 › Selling, General and Administrative Expense | ✓ | #2 | \| \| Year Ended December 31, \| \| Change 2017 vs. 2016 \| \| Change 2016 vs. 2015 \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in thousands) \| 2017 \| 2016 \| 2015 \| $% \| \| $% \| \| \| Selling, general and administrative \| … |
| 4 | `TSLA_FY2020_2020-12-31:258` | Item 7 › Selling, General and Administrative Expense |  | #1 | share price. The increase in stock-based compensation was partially offset by a decrease of $90 million in customer promotional costs, facilities-related expenses and sales and marketing activities. Additionally, there w… |
| 5 | `TSLA_FY2020_2020-12-31:255` | Item 7 › Selling, General and Administrative Expense | ✓ | #1 | \| \| Year Ended December 31, \| \| 2020 vs. 2019 Change \| \| 2019 vs. 2018 Change \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in millions) \| 2020 \| 2019 \| 2018 \| $% \| \| $% \| \| \| Selling, general and administrative \| $… |
| 6 | `TSLA_FY2017_2017-12-31:228` | Item 7 › Management Opportunities, Challenges and Risks and 2018 Outlook |  |  | We expect operating expenses to grow in 2018 as compared to 2017, although operating expenses should decrease significantly as a percentage of revenue due to the significant increase in expected revenue in 2018 and as we… |
| 7 | `TSLA_FY2020_2020-12-31:292` | Item 8 › Index to Consolidated Financial Statements |  |  | \| \| Page \| \|---\|---\| \| Report of Independent Registered Public Accounting Firm \| 51 \| \| Consolidated Balance Sheets \| 54 \| \| Consolidated Statements of Operations \| 55 \| \| Consolidated Statements of Comprehensive Income … |
| 8 | `TSLA_FY2017_2017-12-31:312` | Item 8 › Index to Consolidated Financial Statements |  |  | \| \| Page \| \|---\|---\| \| Report of Independent Registered Public Accounting Firm \| 61 \| \| Consolidated Balance Sheets \| 63 \| \| Consolidated Statements of Operations \| 64 \| \| Consolidated Statements of Comprehensive Loss \| … |
| 9 | `TSLA_FY2020_2020-12-31:235` | Item 7 › Revenues |  |  | \| \| Year Ended December 31, \| \| 2020 vs. 2019 Change \| \| 2019 vs. 2018 Change \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in millions) \| 2020 \| 2019 \| 2018 \| $% \| \| $% \| \| \| Automotive sales \| $26,184 \| $19,952 \| … |
| 10 | `TSLA_FY2020_2020-12-31:389` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | \| \| December 31, \| December 31, \| December 31, \| \|---\|---\|---\|---\| \| \| 2020 \| 2019 \| 2018 \| \| Cash and cash equivalents \| $19,384 \| $6,268 \| $3,686 \| \| Restricted cash included in prepaid expenses and other current asset… |
| 11 | `TSLA_FY2020_2020-12-31:311` | Item 8 › (in millions, except per share data) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2020 \| 2019 \| 2018 \| \| Revenues \| \| \| \| \| Automotive sales \| $26,184 \| $19,952 \| $17,632 \| \| Automotive leasing \| 1,052 \| 869 \| 883 \| \| Total automotive revenues \| … |
| 12 | `TSLA_FY2020_2020-12-31:181` | Item 6 |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2020 \| 2019 (3) \| 2018 (2) \| 2017 \| 2016 (1) \| \| Consolidated Statements of Operations Data: \| \| \| \| \| \| \| Total revenues \| $31,536 \| $24,578 \| $21,461 … |
| 13 | `TSLA_FY2020_2020-12-31:253` | Item 7 › Research and Development Expense |  | #1 | \| \| Year Ended December 31, \| \| 2020 vs. 2019 Change \| \| 2019 vs. 2018 Change \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in millions) \| 2020 \| 2019 \| 2018 \| $% \| \| $% \| \| \| Research and development \| $1,491 \| $1,… |
| 14 | `TSLA_FY2020_2020-12-31:259` | Item 7 › Restructuring and other |  | #1 | \| \| Year Ended December 31, \| \| 2020 vs. 2019 Change \| \| 2019 vs. 2018 Change \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in millions) \| 2020 \| 2019 \| 2018 \| \| $% \| \| $% \| \| Restructuring and other \| $— \| $149 \| $… |
| 15 | `TSLA_FY2020_2020-12-31:263` | Item 7 › Other Income (Expense), Net |  | #2 | \| \| Year Ended December 31, \| \| 2020 vs. 2019 Change \| \| 2019 vs. 2018 Change \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in millions) \| 2020 \| 2019 \| 2018 \| \| $% \| \| $% \| \| Other (expense) income, net \| $(122) \| … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `TSLA_FY2017_2017-12-31:285`** (cited, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Selling, General and Administrative Expense (table)
|  | Year Ended December 31, |  | Change 2017 vs. 2016 |  | Change 2016 vs. 2015 |  |  |
|---|---|---|---|---|---|---|---|
| (Dollars in thousands) | 2017 | 2016 | 2015 | $% |  | $% |  |
| Selling, general and administrative | $2,476,500 | $1,432,189 | $922,232 | $1,044,311 | 73% | $509,957 | 55% |
| As a percentage of revenues | 21% | 20% | 23% |  |  |  |  |
````

**#4 `TSLA_FY2020_2020-12-31:258`** (gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Selling, General and Administrative Expense
share price. The increase in stock-based compensation was partially offset by a decrease of $90 million in customer promotional costs, facilities-related expenses and sales and marketing activities. Additionally, there was a reduction to operating expenses for costs previously incurred in the amount of $43 million for the settlement in part of the securities litigation relating to the SolarCity acquisition (see Note 16, Commitments and Contingencies—Legal Proceedings—Securities Litigation Relating to the SolarCity Acquisition, to the consolidated financial statements included elsewhere in this Annual Report on Form 10-K). SG&A expenses as a percentage of revenue decreased from 11% to 10% in year ended December 31, 2020 as compared to the year ended December 31, 2019. The decrease is primarily from an increase in total revenues from expanding sales, partially offset by an increase in our SG&A expenses as detailed above.
````

**#5 `TSLA_FY2020_2020-12-31:255`** (cited, gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Selling, General and Administrative Expense (table)
|  | Year Ended December 31, |  | 2020 vs. 2019 Change |  | 2019 vs. 2018 Change |  |  |
|---|---|---|---|---|---|---|---|
| (Dollars in millions) | 2020 | 2019 | 2018 | $% |  | $% |  |
| Selling, general and administrative | $3,145 | $2,646 | $2,835 | $499 | 19% | $(189) | -7% |
| As a percentage of revenues | 10% | 11% | 13% |  |  |  |  |
````

**#13 `TSLA_FY2020_2020-12-31:253`** (gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Research and Development Expense (table)
|  | Year Ended December 31, |  | 2020 vs. 2019 Change |  | 2019 vs. 2018 Change |  |  |
|---|---|---|---|---|---|---|---|
| (Dollars in millions) | 2020 | 2019 | 2018 | $% |  | $% |  |
| Research and development | $1,491 | $1,343 | $1,460 | $148 | 11% | $(117) | -8% |
| As a percentage of revenues | 5% | 5% | 7% |  |  |  |  |
````

**#14 `TSLA_FY2020_2020-12-31:259`** (gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Restructuring and other (table)
|  | Year Ended December 31, |  | 2020 vs. 2019 Change |  | 2019 vs. 2018 Change |  |  |
|---|---|---|---|---|---|---|---|
| (Dollars in millions) | 2020 | 2019 | 2018 |  | $% |  | $% |
| Restructuring and other | $— | $149 | $135 | $(149) | -100% | $14 | 10% |
| As a percentage of revenues | 0% | 1% | 1% |  |  |  |  |
````

**#15 `TSLA_FY2020_2020-12-31:263`** (gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Other Income (Expense), Net (table)
|  | Year Ended December 31, |  | 2020 vs. 2019 Change |  | 2019 vs. 2018 Change |  |  |
|---|---|---|---|---|---|---|---|
| (Dollars in millions) | 2020 | 2019 | 2018 |  | $% |  | $% |
| Other (expense) income, net | $(122) | $45 | $22 | $(167) | Not meaningful | $23 | 105% |
| As a percentage of revenues | 0% | 0% | 0% |  |  |  |  |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 2, verified 2, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Tesla's Selling, General and Administrative expense as a percentage of revenues was 21% in fiscal year 2017 and 10% in fiscal year 2020, so it decreased by 11 percentage points. [TSLA FY2017, Item 7, TSLA_FY2017_2017-12-31:285] [TSLA FY2020, Item 7, TSLA_FY2020_2020-12-31:255] | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 2.

**Generated answer**

> Tesla's Selling, General and Administrative expense as a percentage of revenues decreased from 21% in fiscal year 2017 to 10% in fiscal year 2020, a decline of 11 percentage points [TSLA FY2017, Item 7, TSLA_FY2017_2017-12-31:285] [TSLA FY2020, Item 7, TSLA_FY2020_2020-12-31:255].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-TSLA-2017` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2017,2017-12-31,11758751000,-1961400000,-1632086000,2865537200… |
| 2 | `F-TSLA-2020` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2020,2020-12-31,31536000000,721000000,1994000000,52148000000,2… |
| 3 | `TSLA_FY2017_2017-12-31:286` | Item 7 › Selling, General and Administrative Expense |  |  | Selling, general and administrative (“SG&A”) expenses consist primarily of personnel and facilities costs related to our stores, marketing, sales, executive, finance, human resources, information technology and legal org… |
| 4 | `TSLA_FY2020_2020-12-31:256` | Item 7 › Selling, General and Administrative Expense |  |  | Selling, general and administrative (“SG&A”) expenses generally consist of personnel and facilities costs related to our stores, marketing, sales, executive, finance, human resources, information technology and legal org… |
| 5 | `TSLA_FY2017_2017-12-31:285` | Item 7 › Selling, General and Administrative Expense | ✓ | #2 | \| \| Year Ended December 31, \| \| Change 2017 vs. 2016 \| \| Change 2016 vs. 2015 \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in thousands) \| 2017 \| 2016 \| 2015 \| $% \| \| $% \| \| \| Selling, general and administrative \| … |
| 6 | `TSLA_FY2020_2020-12-31:258` | Item 7 › Selling, General and Administrative Expense |  | #1 | share price. The increase in stock-based compensation was partially offset by a decrease of $90 million in customer promotional costs, facilities-related expenses and sales and marketing activities. Additionally, there w… |
| 7 | `TSLA_FY2020_2020-12-31:255` | Item 7 › Selling, General and Administrative Expense | ✓ | #1 | \| \| Year Ended December 31, \| \| 2020 vs. 2019 Change \| \| 2019 vs. 2018 Change \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in millions) \| 2020 \| 2019 \| 2018 \| $% \| \| $% \| \| \| Selling, general and administrative \| $… |
| 8 | `TSLA_FY2017_2017-12-31:228` | Item 7 › Management Opportunities, Challenges and Risks and 2018 Outlook |  |  | We expect operating expenses to grow in 2018 as compared to 2017, although operating expenses should decrease significantly as a percentage of revenue due to the significant increase in expected revenue in 2018 and as we… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#5 `TSLA_FY2017_2017-12-31:285`** (cited, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Selling, General and Administrative Expense (table)
|  | Year Ended December 31, |  | Change 2017 vs. 2016 |  | Change 2016 vs. 2015 |  |  |
|---|---|---|---|---|---|---|---|
| (Dollars in thousands) | 2017 | 2016 | 2015 | $% |  | $% |  |
| Selling, general and administrative | $2,476,500 | $1,432,189 | $922,232 | $1,044,311 | 73% | $509,957 | 55% |
| As a percentage of revenues | 21% | 20% | 23% |  |  |  |  |
````

**#6 `TSLA_FY2020_2020-12-31:258`** (gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Selling, General and Administrative Expense
share price. The increase in stock-based compensation was partially offset by a decrease of $90 million in customer promotional costs, facilities-related expenses and sales and marketing activities. Additionally, there was a reduction to operating expenses for costs previously incurred in the amount of $43 million for the settlement in part of the securities litigation relating to the SolarCity acquisition (see Note 16, Commitments and Contingencies—Legal Proceedings—Securities Litigation Relating to the SolarCity Acquisition, to the consolidated financial statements included elsewhere in this Annual Report on Form 10-K). SG&A expenses as a percentage of revenue decreased from 11% to 10% in year ended December 31, 2020 as compared to the year ended December 31, 2019. The decrease is primarily from an increase in total revenues from expanding sales, partially offset by an increase in our SG&A expenses as detailed above.
````

**#7 `TSLA_FY2020_2020-12-31:255`** (cited, gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Selling, General and Administrative Expense (table)
|  | Year Ended December 31, |  | 2020 vs. 2019 Change |  | 2019 vs. 2018 Change |  |  |
|---|---|---|---|---|---|---|---|
| (Dollars in millions) | 2020 | 2019 | 2018 | $% |  | $% |  |
| Selling, general and administrative | $3,145 | $2,646 | $2,835 | $499 | 19% | $(189) | -7% |
| As a percentage of revenues | 10% | 11% | 13% |  |  |  |  |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 2, verified 2, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Tesla's Selling, General and Administrative expense as a percentage of revenues decreased from 21% in fiscal year 2017 to 10% in fiscal year 2020, a decline of 11 percentage points [TSLA FY2017, Item 7, TSLA_FY2017_2017-12-31:285] [TSLA FY2020, Item 7, TSLA_FY2020_2020-12-31:255]. | None |  |

</details>
