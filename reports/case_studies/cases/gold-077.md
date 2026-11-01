# gold-077: Cross-year table

[← all cases](../README.md) · company: Tesla, Inc. (TSLA) · fiscal year: 2023 · recipe `cross_year_table` · hop `multi` · answer type `numeric` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> By what percentage did Tesla's total revenue grow from fiscal year 2017 to fiscal year 2023?

**Gold answer**

> 722.99%

**Program**: `multiply(96773, 1000), subtract(#0, 11758751), divide(#1, 11758751), multiply(#2, 100)` → `722.987067248894`

**Gold numbers** (RQ2 numeric_accuracy targets): 722.99%

**Gold evidence**

1. `TSLA_FY2023_2023-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Note 18 – Segment Reporting and Information about Geographic Areas · table

   > Total | $96,773 | $81,462 | $53,823

2. `TSLA_FY2017_2017-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Note 23 – Segment Reporting and Information about Geographic Areas · table

   > Total | $11,758,751 | $7,000,132

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 17 | 8 |
| recall@5 | 0.00 | 0.50 | 0.50 | 0.50 |
| recall@all | 0.50 | 0.50 | 1.00 | 0.50 |
| complete@all | 0 | 0 | 1 | 0 |
| average precision (lexical) | 0.17 | 0.50 | 0.64 | 0.37 |
| gold evidence first rank | #1: 7, #2: – | #1: 2, #2: – | #1: 12, #2: 1 | #1: –, #2: 3 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✗ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 1.00 | 1.00 |
| citation precision | – | – | 0.50 | 0.00 |
| citation recall | – | – | 1.00 | 0.00 |
| citation F1 | – | – | 0.67 | 0.00 |
| has a citation | 0 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.33 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 1 |
| tokens | 2589 | 1447 | 21245 | 6502 |
| cost (USD) | 0.0004 | 0.0002 | 0.0677 | 0.0202 |
| latency (s) | 1.2 | 6.0 | 21.0 | 6.6 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2023_2023-12-31:176` | Item 7 › Overview and 2023 Highlights |  |  | In 2023, we recognized total revenues of $96.77 billion, representing an increase of $15.31 billion, compared to the prior year. We continue to ramp production, build new manufacturing capacity and expand our operations … |
| 2 | `TSLA_FY2023_2023-12-31:204` | Item 7 › Revenues |  |  | Services and other revenue increased $2.23 billion, or 37%, in the year ended December 31, 2023 as compared to the year ended December 31, 2022. The increase was primarily due to higher used vehicle revenue driven by inc… |
| 3 | `TSLA_FY2023_2023-12-31:203` | Item 7 › Revenues |  |  | 2023 compared to 2022 Automotive sales revenue increased $11.30 billion, or 17%, in the year ended December 31, 2023 as compared to the year ended December 31, 2022, primarily due to an increase of 473,382 combined Model… |
| 4 | `TSLA_FY2023_2023-12-31:209` | Item 7 › Cost of Revenues and Gross Margin |  |  | Cost of services and other revenue increased $1.95 billion, or 33%, in the year ended December 31, 2023 as compared to the year ended December 31, 2022. The increase was generally in line with the changes in services and… |
| 5 | `TSLA_FY2023_2023-12-31:211` | Item 7 › Cost of Revenues and Gross Margin |  |  | Cost of energy generation and storage revenue increased $1.27 billion, or 35%, in the year ended December 31, 2023 as compared to the year ended December 31, 2022, in line with the increase in Megapack deployments year o… |
| 6 | `TSLA_FY2023_2023-12-31:469` | Item 8 › Note 18 – Segment Reporting and Information about Geographic Areas |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| \| Automotive segment \| \| \| \| \| Revenues \| $90,738 \| $77,553 \| $51,034 \| \| Gross profit \| $16,519 \| $20,565 \| $13,735 \| \| Energy generation and … |
| 7 | `TSLA_FY2023_2023-12-31:253` | Item 8 › (in millions, except per share data) |  | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| \| Revenues \| \| \| \| \| Automotive sales \| $78,509 \| $67,210 \| $44,125 \| \| Automotive regulatory credits \| 1,790 \| 1,776 \| 1,465 \| \| Automotive le… |
| 8 | `TSLA_FY2023_2023-12-31:208` | Item 7 › Cost of Revenues and Gross Margin |  |  | Cost of automotive sales revenue increased $15.52 billion, or 31%, in the year ended December 31, 2023 as compared to the year ended December 31, 2022. Cost of automotive sales revenue increased in line with the change i… |
| 9 | `TSLA_FY2017_2017-12-31:268` | Item 7 › Revenues |  |  | Automotive sales revenue increased $2.95 billion, or 53%, during the year ended December 31, 2017 compared to the year ended December 31, 2016, primarily related to a 58% increase in deliveries to 80,060 vehicles resulti… |
| 10 | `TSLA_FY2023_2023-12-31:276` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| \| Automotive sales \| $78,509 \| $67,210 \| $44,125 \| \| Automotive regulatory credits \| 1,790 \| 1,776 \| 1,465 \| \| Energy generation and storage sa… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#7 `TSLA_FY2023_2023-12-31:253`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (in millions, except per share data) (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2023 | 2022 | 2021 |
| Revenues |  |  |  |
| Automotive sales | $78,509 | $67,210 | $44,125 |
| Automotive regulatory credits | 1,790 | 1,776 | 1,465 |
| Automotive leasing | 2,120 | 2,476 | 1,642 |
| Total automotive revenues | 82,419 | 71,462 | 47,232 |
| Energy generation and storage | 6,035 | 3,909 | 2,789 |
| Services and other | 8,319 | 6,091 | 3,802 |
| Total revenues | 96,773 | 81,462 | 53,823 |
| Cost of revenues |  |  |  |
| Automotive sales | 65,121 | 49,599 | 32,415 |
| Automotive leasing | 1,268 | 1,509 | 978 |
| Total automotive cost of revenues | 66,389 | 51,108 | 33,393 |
| Energy generation and storage | 4,894 | 3,621 | 2,918 |
| Services and other | 7,830 | 5,880 | 3,906 |
| Total cost of revenues | 79,113 | 60,609 | 40,217 |
| Gross profit | 17,660 | 20,853 | 13,606 |
| Operating expenses |  |  |  |
````

**#10 `TSLA_FY2023_2023-12-31:276`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 2 – Summary of Significant Accounting Policies (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2023 | 2022 | 2021 |
| Automotive sales | $78,509 | $67,210 | $44,125 |
| Automotive regulatory credits | 1,790 | 1,776 | 1,465 |
| Energy generation and storage sales | 5,515 | 3,376 | 2,279 |
| Services and other | 8,319 | 6,091 | 3,802 |
| Total revenues from sales and services | 94,133 | 78,453 | 51,671 |
| Automotive leasing | 2,120 | 2,476 | 1,642 |
| Energy generation and storage leasing | 520 | 533 | 510 |
| Total revenues | $96,773 | $81,462 | $53,823 |
````

</details>

RQ2 citation match (section level): `no citations`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2023_2023-12-31:203` | Item 7 › Revenues |  |  | 2023 compared to 2022 Automotive sales revenue increased $11.30 billion, or 17%, in the year ended December 31, 2023 as compared to the year ended December 31, 2022, primarily due to an increase of 473,382 combined Model… |
| 2 | `TSLA_FY2023_2023-12-31:201` | Item 7 › Revenues |  | #1 | \| \| Year Ended December 31, \| \| \| 2023 vs. 2022 Change \| \| 2022 vs. 2021 Change \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in millions) \| 2023 \| 2022 \| 2021 \| \| $% \| \| $% \| \| Automotive sales \| $78,509 \| $67,210 \| … |
| 3 | `TSLA_FY2017_2017-12-31:268` | Item 7 › Revenues |  |  | Automotive sales revenue increased $2.95 billion, or 53%, during the year ended December 31, 2017 compared to the year ended December 31, 2016, primarily related to a 58% increase in deliveries to 80,060 vehicles resulti… |
| 4 | `TSLA_FY2023_2023-12-31:176` | Item 7 › Overview and 2023 Highlights |  |  | In 2023, we recognized total revenues of $96.77 billion, representing an increase of $15.31 billion, compared to the prior year. We continue to ramp production, build new manufacturing capacity and expand our operations … |
| 5 | `TSLA_FY2023_2023-12-31:204` | Item 7 › Revenues |  |  | Services and other revenue increased $2.23 billion, or 37%, in the year ended December 31, 2023 as compared to the year ended December 31, 2022. The increase was primarily due to higher used vehicle revenue driven by inc… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `TSLA_FY2023_2023-12-31:201`** (gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Revenues (table)
|  | Year Ended December 31, |  |  | 2023 vs. 2022 Change |  | 2022 vs. 2021 Change |  |
|---|---|---|---|---|---|---|---|
| (Dollars in millions) | 2023 | 2022 | 2021 |  | $% |  | $% |
| Automotive sales | $78,509 | $67,210 | $44,125 | $11,299 | 17% | $23,085 | 52% |
| Automotive regulatory credits | 1,790 | 1,776 | 1,465 | 14 | 1% | 311 | 21% |
| Automotive leasing | 2,120 | 2,476 | 1,642 | (356) | (14)% | 834 | 51% |
| Total automotive revenues | 82,419 | 71,462 | 47,232 | 10,957 | 15% | 24,230 | 51% |
| Services and other | 8,319 | 6,091 | 3,802 | 2,228 | 37% | 2,289 | 60% |
| Total automotive & services and other segment revenue | 90,738 | 77,553 | 51,034 | 13,185 | 17% | 26,519 | 52% |
| Energy generation and storage segment revenue | 6,035 | 3,909 | 2,789 | 2,126 | 54% | 1,120 | 40% |
| Total revenues | $96,773 | $81,462 | $53,823 | $15,311 | 19% | $27,639 | 51% |
````

</details>

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 17, cited: 2.

**Generated answer**

> Tesla’s total revenues were $11,758,751 thousand in fiscal year 2017 and $96,773 million in fiscal year 2023. [TSLA FY2017, Item 6, TSLA_FY2017_2017-12-31:213] [TSLA FY2023, Item 8, TSLA_FY2023_2023-12-31:471]
>
> Using those figures, Tesla’s total revenue grew by approximately 723% from fiscal year 2017 to fiscal year 2023. [TSLA FY2017, Item 6, TSLA_FY2017_2017-12-31:213] [TSLA FY2023, Item 8, TSLA_FY2023_2023-12-31:471]
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 723%; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2017_2017-12-31:266` | Item 7 › Revenues |  | #2 | \| \| Year Ended December 31, \| \| Change 2017 vs. 2016 \| \| Change 2016 vs. 2015 \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in thousands) \| 2017 \| 2016 \| 2015 \| $% \| \| $% \| \| \| Automotive sales \| $8,534,752 \| $5,589… |
| 2 | `TSLA_FY2017_2017-12-31:606` | Item 8 › Note 22 – Quarterly Results of Operations (Unaudited) |  |  | \| \| Three Months Ended \| \| \| \| \|---\|---\|---\|---\|---\| \| \| March 31 \| June 30 \| September 30 \| December 31 \| \| 2017 \| \| \| \| \| \| Total revenues \| $2,696,270 \| $2,789,557 \| $2,984,675 \| $3,288,249 \| \| Gross profit \| $667,946… |
| 3 | `TSLA_FY2017_2017-12-31:213` | Item 6 | ✓ | #2 | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2017 \| 2016 (1) \| 2015 \| 2014 \| 2013 \| \| Consolidated Statements of Operations Data: \| \| \| \| \| \| \| Total revenues \| $11,758,751 \| $7,000,132 \| $4,046,02… |
| 4 | `TSLA_FY2017_2017-12-31:273` | Item 7 › Cost of Revenues and Gross Margin |  |  | \| \| Year Ended December 31, \| \| Change 2017 vs. 2016 \| \| Change 2016 vs. 2015 \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in thousands) \| 2017 \| 2016 \| 2015 \| $% \| \| $% \| \| \| Cost of revenues \| \| \| \| \| \| \| \| \| Aut… |
| 5 | `TSLA_FY2017_2017-12-31:321` | Item 8 › (in thousands, except per share data) |  |  | \| \| December 31, \| December 31, \| \|---\|---\|---\| \| \| 2017 \| 2016 \| \| Accrued liabilities and other \| 1,731,366 \| 1,210,028 \| \| Deferred revenue \| 1,015,253 \| 763,126 \| \| Resale value guarantees \| 787,333 \| 179,504 \| \| Cus… |
| 6 | `TSLA_FY2017_2017-12-31:274` | Item 7 › Cost of Revenues and Gross Margin |  |  | \| \| Year Ended December 31, \| \| Change 2017 vs. 2016 \| \| Change 2016 vs. 2015 \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| Gross profit total automotive \| $2,208,596 \| $1,600,685 \| $917,671 \| \| \| \| \| \| Gross margin total au… |
| 7 | `TSLA_FY2023_2023-12-31:368` | Item 8 › Note 8 – Property, Plant and Equipment, Net |  |  | \| \| December 31, 2023 \| December 31, 2022 \| \|---\|---\|---\| \| Machinery, equipment, vehicles and office furniture \| $16,372 \| $13,558 \| \| Tooling \| 3,147 \| 2,579 \| \| Leasehold improvements \| 3,168 \| 2,366 \| \| Land and buil… |
| 8 | `TSLA_FY2023_2023-12-31:426` | Item 8 › Summary Stock-Based Compensation Information |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| \| Cost of revenues \| $741 \| $594 \| $421 \| \| Research and development \| 689 \| 536 \| 448 \| \| Selling, general and administrative \| 382 \| 430 \| 1,… |
| 9 | `TSLA_FY2023_2023-12-31:283` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2023 \| 2022 \| \| Deferred revenue— beginning of period \| $2,913 \| $2,382 \| \| Additions \| 1,201 \| 1,178 \| \| Net changes in liability for pre-existing contracts \| 17 \| (67) … |
| 10 | `TSLA_FY2023_2023-12-31:312` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| \| Stock-based awards \| 12 \| 4 \| 1 \| |
| 11 | `TSLA_FY2023_2023-12-31:372` | Item 8 › Note 9 – Accrued Liabilities and Other |  |  | \| \| December 31, 2023 \| December 31, 2022 \| \|---\|---\|---\| \| Accrued purchases (1) \| $2,721 \| $2,747 \| \| Accrued warranty reserve, current portion \| 1,546 \| 1,025 \| \| Payroll and related costs \| 1,325 \| 1,026 \| \| Taxes pa… |
| 12 | `TSLA_FY2023_2023-12-31:471` | Item 8 › Note 18 – Segment Reporting and Information about Geographic Areas | ✓ | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| \| United States \| $45,235 \| $40,553 \| $23,973 \| \| China \| 21,745 \| 18,145 \| 13,844 \| \| Other international \| 29,793 \| 22,764 \| 16,006 \| \| Total… |
| 13 | `TSLA_FY2017_2017-12-31:312` | Item 8 › Index to Consolidated Financial Statements |  |  | \| \| Page \| \|---\|---\| \| Report of Independent Registered Public Accounting Firm \| 61 \| \| Consolidated Balance Sheets \| 63 \| \| Consolidated Statements of Operations \| 64 \| \| Consolidated Statements of Comprehensive Loss \| … |
| 14 | `TSLA_FY2023_2023-12-31:237` | Item 8 › Index to Consolidated Financial Statements |  |  | \| \| Page \| \|---\|---\| \| Report of Independent Registered Public Accounting Firm (PCAOB ID: 238) \| 47 \| \| Consolidated Balance Sheets \| 49 \| \| Consolidated Statements of Operations \| 50 \| \| Consolidated Statements of Compr… |
| 15 | `TSLA_FY2023_2023-12-31:315` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | \| \| December 31, 2023 \| December 31, 2022 \| December 31, 2021 \| \|---\|---\|---\|---\| \| Cash and cash equivalents \| $16,398 \| $16,253 \| $17,576 \| \| Restricted cash included in prepaid expenses and other current assets \| 543 … |
| 16 | `TSLA_FY2017_2017-12-31:610` | Item 8 › Note 23 – Segment Reporting and Information about Geographic Areas |  |  | The following table presents revenues by geographic area based on where our products are delivered (in thousands): |
| 17 | `TSLA_FY2017_2017-12-31:347` | Item 8 › Basis of Presentation and Preparation |  |  | Principles of Consolidation |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2017_2017-12-31:266`** (gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Revenues (table)
|  | Year Ended December 31, |  | Change 2017 vs. 2016 |  | Change 2016 vs. 2015 |  |  |
|---|---|---|---|---|---|---|---|
| (Dollars in thousands) | 2017 | 2016 | 2015 | $% |  | $% |  |
| Automotive sales | $8,534,752 | $5,589,007 | $3,431,587 | $2,945,745 | 53% | $2,157,420 | 63% |
| Automotive leasing | 1,106,548 | 761,759 | 309,386 | 344,789 | 45% | 452,373 | 146% |
| Total automotive revenues | 9,641,300 | 6,350,766 | 3,740,973 | 3,290,534 | 52% | 2,609,793 | 70% |
| Services and other | 1,001,185 | 467,972 | 290,575 | 533,213 | 114% | 177,397 | 61% |
| Total automotive & services and other segment revenue | 10,642,485 | 6,818,738 | 4,031,548 | 3,823,747 | 56% | 2,787,190 | 69% |
| Energy generation and storage segment revenue | 1,116,266 | 181,394 | 14,477 | 934,872 | 515% | 166,917 | 1153% |
| Total revenues | $11,758,751 | $7,000,132 | $4,046,025 | $4,758,619 | 68% | $2,954,107 | 73% |
````

**#3 `TSLA_FY2017_2017-12-31:213`** (cited, gold #2)

````text
ITEM 6. SELECTED CONSOLIDATED FINANCIAL DATA (table)
|  | Year Ended December 31, |  |  |  |  |
|---|---|---|---|---|---|
|  | 2017 | 2016 (1) | 2015 | 2014 | 2013 |
| Consolidated Statements of Operations Data: |  |  |  |  |  |
| Total revenues | $11,758,751 | $7,000,132 | $4,046,025 | $3,198,356 | $2,013,496 |
| Gross profit | $2,222,487 | $1,599,257 | $923,503 | $881,671 | $456,262 |
| Loss from operations | $(1,632,086) | $(667,340) | $(716,629) | $(186,689) | $(61,283) |
| Net loss attributable to common stockholders | $(1,961,400) | $(674,914) | $(888,663) | $(294,040) | $(74,014) |
| Net loss per share of common stock attributable to common stockholders, basic and diluted | $(11.83) | $(4.68) | $(6.93) | $(2.36) | $(0.62) |
| Weighted average shares used in computing net loss per share of common stock, basic and diluted | 165,758 | 144,212 | 128,202 | 124,539 | 119,421 |
````

**#12 `TSLA_FY2023_2023-12-31:471`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 18 – Segment Reporting and Information about Geographic Areas (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2023 | 2022 | 2021 |
| United States | $45,235 | $40,553 | $23,973 |
| China | 21,745 | 18,145 | 13,844 |
| Other international | 29,793 | 22,764 | 16,006 |
| Total | $96,773 | $81,462 | $53,823 |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 6'), ('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 2, ungrounded 1, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 723%

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Tesla’s total revenues were $11,758,751 thousand in fiscal year 2017 and $96,773 million in fiscal year 2023. [TSLA FY2017, Item 6, TSLA_FY2017_2017-12-31:213] [TSLA FY2023, Item 8, TSLA_FY2023_2023-12-31:471] | None |  |
| Using those figures, Tesla’s total revenue grew by approximately 723% from fiscal year 2017 to fiscal year 2023. [TSLA FY2017, Item 6, TSLA_FY2017_2017-12-31:213] [TSLA FY2023, Item 8, TSLA_FY2023_2023-12-31:471] | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 2.

**Generated answer**

> Tesla’s total revenue grew from $11,758,751,000 in fiscal year 2017 to $96,773,000,000 in fiscal year 2023, an increase of approximately 723% [F-TSLA-2017] [F-TSLA-2023].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-TSLA-2017` | SEC XBRL Reported Financials (financials.csv) | ✓ |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2017,2017-12-31,11758751000,-1961400000,-1632086000,2865537200… |
| 2 | `F-TSLA-2023` | SEC XBRL Reported Financials (financials.csv) | ✓ |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2023,2023-12-31,96773000000,14997000000,8891000000,10661800000… |
| 3 | `TSLA_FY2017_2017-12-31:266` | Item 7 › Revenues |  | #2 | \| \| Year Ended December 31, \| \| Change 2017 vs. 2016 \| \| Change 2016 vs. 2015 \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in thousands) \| 2017 \| 2016 \| 2015 \| $% \| \| $% \| \| \| Automotive sales \| $8,534,752 \| $5,589… |
| 4 | `TSLA_FY2017_2017-12-31:606` | Item 8 › Note 22 – Quarterly Results of Operations (Unaudited) |  |  | \| \| Three Months Ended \| \| \| \| \|---\|---\|---\|---\|---\| \| \| March 31 \| June 30 \| September 30 \| December 31 \| \| 2017 \| \| \| \| \| \| Total revenues \| $2,696,270 \| $2,789,557 \| $2,984,675 \| $3,288,249 \| \| Gross profit \| $667,946… |
| 5 | `TSLA_FY2017_2017-12-31:213` | Item 6 |  | #2 | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2017 \| 2016 (1) \| 2015 \| 2014 \| 2013 \| \| Consolidated Statements of Operations Data: \| \| \| \| \| \| \| Total revenues \| $11,758,751 \| $7,000,132 \| $4,046,02… |
| 6 | `TSLA_FY2017_2017-12-31:273` | Item 7 › Cost of Revenues and Gross Margin |  |  | \| \| Year Ended December 31, \| \| Change 2017 vs. 2016 \| \| Change 2016 vs. 2015 \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| (Dollars in thousands) \| 2017 \| 2016 \| 2015 \| $% \| \| $% \| \| \| Cost of revenues \| \| \| \| \| \| \| \| \| Aut… |
| 7 | `TSLA_FY2017_2017-12-31:321` | Item 8 › (in thousands, except per share data) |  |  | \| \| December 31, \| December 31, \| \|---\|---\|---\| \| \| 2017 \| 2016 \| \| Accrued liabilities and other \| 1,731,366 \| 1,210,028 \| \| Deferred revenue \| 1,015,253 \| 763,126 \| \| Resale value guarantees \| 787,333 \| 179,504 \| \| Cus… |
| 8 | `TSLA_FY2017_2017-12-31:274` | Item 7 › Cost of Revenues and Gross Margin |  |  | \| \| Year Ended December 31, \| \| Change 2017 vs. 2016 \| \| Change 2016 vs. 2015 \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| Gross profit total automotive \| $2,208,596 \| $1,600,685 \| $917,671 \| \| \| \| \| \| Gross margin total au… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `F-TSLA-2017`** (cited)

````text
[F-TSLA-2017] (TSLA FY2017 reported financials; amounts in USD, EPSDiluted in USD per share)
fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted
2017,2017-12-31,11758751000,-1961400000,-1632086000,28655372000,23022980000,4237242000,3367914000,-60654000,-11.83
````

**#2 `F-TSLA-2023`** (cited)

````text
[F-TSLA-2023] (TSLA FY2023 reported financials; amounts in USD, EPSDiluted in USD per share)
fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted
2023,2023-12-31,96773000000,14997000000,8891000000,106618000000,43009000000,62634000000,16398000000,13256000000,4.3
````

**#3 `TSLA_FY2017_2017-12-31:266`** (gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Revenues (table)
|  | Year Ended December 31, |  | Change 2017 vs. 2016 |  | Change 2016 vs. 2015 |  |  |
|---|---|---|---|---|---|---|---|
| (Dollars in thousands) | 2017 | 2016 | 2015 | $% |  | $% |  |
| Automotive sales | $8,534,752 | $5,589,007 | $3,431,587 | $2,945,745 | 53% | $2,157,420 | 63% |
| Automotive leasing | 1,106,548 | 761,759 | 309,386 | 344,789 | 45% | 452,373 | 146% |
| Total automotive revenues | 9,641,300 | 6,350,766 | 3,740,973 | 3,290,534 | 52% | 2,609,793 | 70% |
| Services and other | 1,001,185 | 467,972 | 290,575 | 533,213 | 114% | 177,397 | 61% |
| Total automotive & services and other segment revenue | 10,642,485 | 6,818,738 | 4,031,548 | 3,823,747 | 56% | 2,787,190 | 69% |
| Energy generation and storage segment revenue | 1,116,266 | 181,394 | 14,477 | 934,872 | 515% | 166,917 | 1153% |
| Total revenues | $11,758,751 | $7,000,132 | $4,046,025 | $4,758,619 | 68% | $2,954,107 | 73% |
````

**#5 `TSLA_FY2017_2017-12-31:213`** (gold #2)

````text
ITEM 6. SELECTED CONSOLIDATED FINANCIAL DATA (table)
|  | Year Ended December 31, |  |  |  |  |
|---|---|---|---|---|---|
|  | 2017 | 2016 (1) | 2015 | 2014 | 2013 |
| Consolidated Statements of Operations Data: |  |  |  |  |  |
| Total revenues | $11,758,751 | $7,000,132 | $4,046,025 | $3,198,356 | $2,013,496 |
| Gross profit | $2,222,487 | $1,599,257 | $923,503 | $881,671 | $456,262 |
| Loss from operations | $(1,632,086) | $(667,340) | $(716,629) | $(186,689) | $(61,283) |
| Net loss attributable to common stockholders | $(1,961,400) | $(674,914) | $(888,663) | $(294,040) | $(74,014) |
| Net loss per share of common stock attributable to common stockholders, basic and diluted | $(11.83) | $(4.68) | $(6.93) | $(2.36) | $(0.62) |
| Weighted average shares used in computing net loss per share of common stock, basic and diluted | 165,758 | 144,212 | 128,202 | 124,539 | 119,421 |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'XBRL')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Tesla’s total revenue grew from $11,758,751,000 in fiscal year 2017 to $96,773,000,000 in fiscal year 2023, an increase of approximately 723% [F-TSLA-2017] [F-TSLA-2023]. | None |  |

</details>
