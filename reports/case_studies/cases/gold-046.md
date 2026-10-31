# gold-046: Multi-hop table (one filing)

[← all cases](../README.md) · company: Tesla, Inc. (TSLA) · fiscal year: 2015 · recipe `table` · hop `multi` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> For Tesla, Inc. in fiscal year 2015, calculate the ratio of the net cash used in investing activities to the net cash provided by financing activities, expressed as a percentage.

**Gold answer**

> 109.85%

**Program**: `divide(1673551, 1523523), multiply(#0, 100)` → `109.84743912628821`

**Gold numbers** (RQ2 numeric_accuracy targets): 109.85%

**Gold evidence**

1. `TSLA_FY2015_2015-12-31` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Summary of Cash Flows · table

   > | Net cash used in investing activities | (1,673,551) | (990,444) | (249,417) |

2. `TSLA_FY2015_2015-12-31` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Summary of Cash Flows · table

   > | Net cash provided by financing activities | 1,523,523 | 2,143,130 | 635,422 |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 7 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.92 | 0.68 | 0.89 | 0.61 |
| gold evidence first rank | #1: 1, #2: 1 | #1: 2, #2: 2 | #1: 2, #2: 1 | #1: 3, #2: 2 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 1.00 | 1.00 | 1.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 1.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 3397 | 1703 | 8149 | 5379 |
| cost (USD) | 0.0006 | 0.0003 | 0.0260 | 0.0177 |
| latency (s) | 2.2 | 7.5 | 12.6 | 6.9 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> For Tesla in fiscal year 2015:
>
> - Net cash used in investing activities = **$1,673,551** thousand [1]
> - Net cash provided by financing activities = **$1,523,523** thousand [1]
>
> Ratio as a percentage:
>
> \[
> \frac{1,673,551}{1,523,523} \times 100 \approx 109.8\%
> \]
>
> So, the net cash used in investing activities was **about 109.8%** of the net cash provided by financing activities in 2015 [1].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2015_2015-12-31:227` | Item 7 › Summary of Cash Flows | ✓ | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Net cash provided by (used in) operating activities \| $(524,499) \| $(57,337) \| $264,804 \| \| Net cash used in investing activities \| (1,673,55… |
| 2 | `TSLA_FY2015_2015-12-31:231` | Item 7 › Cash Flows from Financing Activities |  | #2 | Net cash provided by financing activities was $1.52 billion, $2.14 billion and $635.4 million in 2015, 2014 and 2013. Cash flows from financing activities during the twelve months ended December 31, 2015 consisted primar… |
| 3 | `TSLA_FY2015_2015-12-31:230` | Item 7 › Cash Flows from Investing Activities |  |  | Cash flows from investing activities primarily relate to capital expenditures to support our growth in operations, including investments in Model S manufacturing equipment and tooling and our stores, service centers and … |
| 4 | `TSLA_FY2015_2015-12-31:270` | Item 8 › (in thousands) |  | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Maturities of short-term marketable securities \| — \| 189,131 \| — \| \| Business acquisition \| (12,260) \| — \| — \| \| Net cash used in investing a… |
| 5 | `TSLA_FY2015_2015-12-31:246` | Item 7A › Interest Rate Risk |  |  | We had cash and cash equivalents totaling $1.20 billion as of December 31, 2015. A significant portion of our cash and cash equivalents were invested in money market funds. Cash and cash equivalents are held for working … |
| 6 | `TSLA_FY2015_2015-12-31:170` | Item 6 |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| 2012 \| 2011 \| \| \| (in thousands, except per share data) \| \| \| \| \| \| Consolidated Statements of Operations Data: \| \| \| \| \| \| \| Total… |
| 7 | `TSLA_FY2015_2015-12-31:253` | Item 8 › (in thousands) |  |  | \| \| December 31, \| December 31, \| \|---\|---\|---\| \| \| 2015 \| 2014 \| \| Assets \| \| \| \| Current assets \| \| \| \| Cash and cash equivalents \| $1,196,908 \| $1,905,713 \| \| Restricted cash and marketable securities \| 22,628 \| 17,94… |
| 8 | `TSLA_FY2015_2015-12-31:264` | Item 8 › (in thousands, except per share data) |  |  | \| \| \| \| \| \| Accumulated \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Common Stock \| \| Additional \| \| Other \| Total \| \| \| \| \| Paid-In \| Accumulated \| Comprehensive \| Stockholders' \| \| \| Shares \| Amount \| Capital \| Deficit \| Loss… |
| 9 | `TSLA_FY2015_2015-12-31:261` | Item 8 › (in thousands, except per share data) |  |  | \| \| \| \| \| \| Accumulated \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Common Stock \| \| Additional \| \| Other \| Total \| \| \| \| \| Paid-In \| Accumulated \| Comprehensive \| Stockholders' \| \| \| Shares \| Amount \| Capital \| Deficit \| Loss… |
| 10 | `TSLA_FY2015_2015-12-31:268` | Item 8 › (in thousands) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Cash Flows From Operating Activities \| \| \| \| \| Net loss \| $(888,663) \| $(294,040) \| $(74,014) \| \| Adjustments to reconcile net loss to net ca… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2015_2015-12-31:227`** (cited, gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Summary of Cash Flows (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2015 | 2014 | 2013 |
| Net cash provided by (used in) operating activities | $(524,499) | $(57,337) | $264,804 |
| Net cash used in investing activities | (1,673,551) | (990,444) | (249,417) |
| Net cash provided by financing activities | 1,523,523 | 2,143,130 | 635,422 |
````

**#2 `TSLA_FY2015_2015-12-31:231`** (gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Cash Flows from Financing Activities
Net cash provided by financing activities was $1.52 billion, $2.14 billion and $635.4 million in 2015, 2014 and 2013. Cash flows from financing activities during the twelve months ended December 31, 2015 consisted primarily of $738.3 million net proceeds from August 2015 public offering of 3,099,173 shares of common stock and $568.7 received from vehicle sales to our bank leasing partners. The decrease in cash provided from financing in 2015 as compared to 2014 was primarily due to $2.1 billion net proceeds received in 2014 from issuance of our 2019 and 2021 Notes. The increase in cash provided from financing in 2014 as compared to 2013 was primarily due to $2.1 billion net proceeds from the issuance of our 2019 and 2021 Notes, including the associated hedge and warrant transactions, representing a $1.5 billion increase in debt financing as compared to 2013. Cash flows from financing in 2013 that did not recur in 2014 included proceeds of $415.0 million from the issuance of common stock in public and private offerings and $452.3 million used to repay our DOE loans. 0.25% and 1.25% Convertible Senior Notes and Bond Hedge and Warrant Transactions
````

**#4 `TSLA_FY2015_2015-12-31:270`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (in thousands) (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2015 | 2014 | 2013 |
| Maturities of short-term marketable securities | — | 189,131 | — |
| Business acquisition | (12,260) | — | — |
| Net cash used in investing activities | (1,673,551) | (990,444) | (249,417) |
| Cash Flows From Financing Activities |  |  |  |
| Proceeds from issuance of convertible and other debt | 318,972 | 2,300,000 | 660,000 |
| Proceeds from issuance of common stock in public offering | 730,000 | — | 360,000 |
| Proceeds from issuance of warrants | — | 389,160 | 120,318 |
| Proceeds from exercise of stock options and other stock issuances | 106,611 | 100,455 | 95,307 |
| Proceeds from issuance of common stock in private placement | 20,000 | — | 55,000 |
| Principal payments on DOE loans | — | — | (452,337) |
| Purchase of convertible note hedges | — | (603,428) | (177,540) |
| Common stock and convertible debt issuance costs | (17,025) | (35,149) | (16,901) |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 7')] gold=[(None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 1.

**Generated answer**

> For Tesla in FY2015:
>
> - Net cash used in investing activities = **$1,673,551** [2]
> - Net cash provided by financing activities = **$1,523,523** [2]
>
> Ratio = \( \frac{1,673,551}{1,523,523} \times 100 \approx 109.8\% \) [2]
>
> So, the net cash used in investing activities was **about 109.8%** of the net cash provided by financing activities in 2015 [2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2015_2015-12-31:230` | Item 7 › Cash Flows from Investing Activities |  |  | Cash flows from investing activities primarily relate to capital expenditures to support our growth in operations, including investments in Model S manufacturing equipment and tooling and our stores, service centers and … |
| 2 | `TSLA_FY2015_2015-12-31:227` | Item 7 › Summary of Cash Flows | ✓ | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Net cash provided by (used in) operating activities \| $(524,499) \| $(57,337) \| $264,804 \| \| Net cash used in investing activities \| (1,673,55… |
| 3 | `TSLA_FY2015_2015-12-31:231` | Item 7 › Cash Flows from Financing Activities |  | #2 | Net cash provided by financing activities was $1.52 billion, $2.14 billion and $635.4 million in 2015, 2014 and 2013. Cash flows from financing activities during the twelve months ended December 31, 2015 consisted primar… |
| 4 | `TSLA_FY2015_2015-12-31:270` | Item 8 › (in thousands) |  | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Maturities of short-term marketable securities \| — \| 189,131 \| — \| \| Business acquisition \| (12,260) \| — \| — \| \| Net cash used in investing a… |
| 5 | `TSLA_FY2015_2015-12-31:271` | Item 8 › (in thousands) |  | #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Principal payments on capital leases and other debt \| (203,780) \| (11,179) \| (8,425) \| \| Collateralized lease borrowing \| 568,745 \| 3,271 \| —… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `TSLA_FY2015_2015-12-31:227`** (cited, gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Summary of Cash Flows (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2015 | 2014 | 2013 |
| Net cash provided by (used in) operating activities | $(524,499) | $(57,337) | $264,804 |
| Net cash used in investing activities | (1,673,551) | (990,444) | (249,417) |
| Net cash provided by financing activities | 1,523,523 | 2,143,130 | 635,422 |
````

**#3 `TSLA_FY2015_2015-12-31:231`** (gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Cash Flows from Financing Activities
Net cash provided by financing activities was $1.52 billion, $2.14 billion and $635.4 million in 2015, 2014 and 2013. Cash flows from financing activities during the twelve months ended December 31, 2015 consisted primarily of $738.3 million net proceeds from August 2015 public offering of 3,099,173 shares of common stock and $568.7 received from vehicle sales to our bank leasing partners. The decrease in cash provided from financing in 2015 as compared to 2014 was primarily due to $2.1 billion net proceeds received in 2014 from issuance of our 2019 and 2021 Notes. The increase in cash provided from financing in 2014 as compared to 2013 was primarily due to $2.1 billion net proceeds from the issuance of our 2019 and 2021 Notes, including the associated hedge and warrant transactions, representing a $1.5 billion increase in debt financing as compared to 2013. Cash flows from financing in 2013 that did not recur in 2014 included proceeds of $415.0 million from the issuance of common stock in public and private offerings and $452.3 million used to repay our DOE loans. 0.25% and 1.25% Convertible Senior Notes and Bond Hedge and Warrant Transactions
````

**#4 `TSLA_FY2015_2015-12-31:270`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (in thousands) (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2015 | 2014 | 2013 |
| Maturities of short-term marketable securities | — | 189,131 | — |
| Business acquisition | (12,260) | — | — |
| Net cash used in investing activities | (1,673,551) | (990,444) | (249,417) |
| Cash Flows From Financing Activities |  |  |  |
| Proceeds from issuance of convertible and other debt | 318,972 | 2,300,000 | 660,000 |
| Proceeds from issuance of common stock in public offering | 730,000 | — | 360,000 |
| Proceeds from issuance of warrants | — | 389,160 | 120,318 |
| Proceeds from exercise of stock options and other stock issuances | 106,611 | 100,455 | 95,307 |
| Proceeds from issuance of common stock in private placement | 20,000 | — | 55,000 |
| Principal payments on DOE loans | — | — | (452,337) |
| Purchase of convertible note hedges | — | (603,428) | (177,540) |
| Common stock and convertible debt issuance costs | (17,025) | (35,149) | (16,901) |
````

**#5 `TSLA_FY2015_2015-12-31:271`** (gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (in thousands) (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2015 | 2014 | 2013 |
| Principal payments on capital leases and other debt | (203,780) | (11,179) | (8,425) |
| Collateralized lease borrowing | 568,745 | 3,271 | — |
| Net cash provided by financing activities | 1,523,523 | 2,143,130 | 635,422 |
| Effect of exchange rate changes on cash and cash equivalents | (34,278) | (35,525) | (6,810) |
| Net increase (decrease) in cash and cash equivalents | (708,805) | 1,059,824 | 643,999 |
| Cash and cash equivalents at beginning of period | 1,905,713 | 845,889 | 201,890 |
| Cash and cash equivalents at end of period | $1,196,908 | $1,905,713 | $845,889 |
| Supplemental Disclosures |  |  |  |
| Interest paid | $32,060 | $20,539 | $9,041 |
| Income taxes paid | 9,461 | 3,120 | 257 |
| Supplemental noncash investing activities |  |  |  |
| Acquisition of property and equipment included in accounts payable and accrued liabilities | 267,334 | 254,393 | 38,789 |
| Estimated fair market value of facilities under build-to-suit lease | 174,749 | 50,076 | — |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 7')] gold=[(None, 'Item 7')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 2.

**Generated answer**

> For fiscal year 2015, net cash used in investing activities was $(1,673,551) and net cash provided by financing activities was $1,523,523. Dividing $(1,673,551) by $1,523,523 gives a ratio of approximately -109.8%, or 109.8% in magnitude. [TSLA FY2015, Item 7, TSLA_FY2015_2015-12-31:230] [TSLA FY2015, Item 7, TSLA_FY2015_2015-12-31:231]
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 1,673,551, 1,523,523, 109.8%, 109.8%, 1,673,551, 1,523,523; 2 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2015_2015-12-31:231` | Item 7 › Cash Flows from Financing Activities | ✓ | #2 | Net cash provided by financing activities was $1.52 billion, $2.14 billion and $635.4 million in 2015, 2014 and 2013. Cash flows from financing activities during the twelve months ended December 31, 2015 consisted primar… |
| 2 | `TSLA_FY2015_2015-12-31:227` | Item 7 › Summary of Cash Flows |  | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Net cash provided by (used in) operating activities \| $(524,499) \| $(57,337) \| $264,804 \| \| Net cash used in investing activities \| (1,673,55… |
| 3 | `TSLA_FY2015_2015-12-31:230` | Item 7 › Cash Flows from Investing Activities | ✓ |  | Cash flows from investing activities primarily relate to capital expenditures to support our growth in operations, including investments in Model S manufacturing equipment and tooling and our stores, service centers and … |
| 4 | `TSLA_FY2015_2015-12-31:270` | Item 8 › (in thousands) |  | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Maturities of short-term marketable securities \| — \| 189,131 \| — \| \| Business acquisition \| (12,260) \| — \| — \| \| Net cash used in investing a… |
| 5 | `TSLA_FY2015_2015-12-31:271` | Item 8 › (in thousands) |  | #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Principal payments on capital leases and other debt \| (203,780) \| (11,179) \| (8,425) \| \| Collateralized lease borrowing \| 568,745 \| 3,271 \| —… |
| 6 | `TSLA_FY2015_2015-12-31:268` | Item 8 › (in thousands) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Cash Flows From Operating Activities \| \| \| \| \| Net loss \| $(888,663) \| $(294,040) \| $(74,014) \| \| Adjustments to reconcile net loss to net ca… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2015_2015-12-31:231`** (cited, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Cash Flows from Financing Activities
Net cash provided by financing activities was $1.52 billion, $2.14 billion and $635.4 million in 2015, 2014 and 2013. Cash flows from financing activities during the twelve months ended December 31, 2015 consisted primarily of $738.3 million net proceeds from August 2015 public offering of 3,099,173 shares of common stock and $568.7 received from vehicle sales to our bank leasing partners. The decrease in cash provided from financing in 2015 as compared to 2014 was primarily due to $2.1 billion net proceeds received in 2014 from issuance of our 2019 and 2021 Notes. The increase in cash provided from financing in 2014 as compared to 2013 was primarily due to $2.1 billion net proceeds from the issuance of our 2019 and 2021 Notes, including the associated hedge and warrant transactions, representing a $1.5 billion increase in debt financing as compared to 2013. Cash flows from financing in 2013 that did not recur in 2014 included proceeds of $415.0 million from the issuance of common stock in public and private offerings and $452.3 million used to repay our DOE loans. 0.25% and 1.25% Convertible Senior Notes and Bond Hedge and Warrant Transactions
````

**#2 `TSLA_FY2015_2015-12-31:227`** (gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Summary of Cash Flows (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2015 | 2014 | 2013 |
| Net cash provided by (used in) operating activities | $(524,499) | $(57,337) | $264,804 |
| Net cash used in investing activities | (1,673,551) | (990,444) | (249,417) |
| Net cash provided by financing activities | 1,523,523 | 2,143,130 | 635,422 |
````

**#3 `TSLA_FY2015_2015-12-31:230`** (cited)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Cash Flows from Investing Activities
Cash flows from investing activities primarily relate to capital expenditures to support our growth in operations, including investments in Model S manufacturing equipment and tooling and our stores, service centers and Supercharger network infrastructure. Cash used in investing activities was $1.67 billion, $990.4 million and $249.4 million in 2015, 2014 and 2013. Cash flows from investing activities and variability between each year related primarily to capital expenditures, which were $1.63 billion, $969.9 million, and $264.2 million in 2015, 2014, and 2013. Expenditures in all years consisted primarily of purchases of capital equipment, tooling, and facilities to support our Model S and Model X manufacturing. In 2014, we began construction of our Gigafactory facility in Nevada. Tesla’s contribution to total capital expenditures are expected to be about $2.0 billion over the next 5 years. In 2015, we used cash of $220.0 million towards the construction of the first stage of this project and expect to spend up to $250 million over the next 12 months.
````

**#4 `TSLA_FY2015_2015-12-31:270`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (in thousands) (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2015 | 2014 | 2013 |
| Maturities of short-term marketable securities | — | 189,131 | — |
| Business acquisition | (12,260) | — | — |
| Net cash used in investing activities | (1,673,551) | (990,444) | (249,417) |
| Cash Flows From Financing Activities |  |  |  |
| Proceeds from issuance of convertible and other debt | 318,972 | 2,300,000 | 660,000 |
| Proceeds from issuance of common stock in public offering | 730,000 | — | 360,000 |
| Proceeds from issuance of warrants | — | 389,160 | 120,318 |
| Proceeds from exercise of stock options and other stock issuances | 106,611 | 100,455 | 95,307 |
| Proceeds from issuance of common stock in private placement | 20,000 | — | 55,000 |
| Principal payments on DOE loans | — | — | (452,337) |
| Purchase of convertible note hedges | — | (603,428) | (177,540) |
| Common stock and convertible debt issuance costs | (17,025) | (35,149) | (16,901) |
````

**#5 `TSLA_FY2015_2015-12-31:271`** (gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (in thousands) (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2015 | 2014 | 2013 |
| Principal payments on capital leases and other debt | (203,780) | (11,179) | (8,425) |
| Collateralized lease borrowing | 568,745 | 3,271 | — |
| Net cash provided by financing activities | 1,523,523 | 2,143,130 | 635,422 |
| Effect of exchange rate changes on cash and cash equivalents | (34,278) | (35,525) | (6,810) |
| Net increase (decrease) in cash and cash equivalents | (708,805) | 1,059,824 | 643,999 |
| Cash and cash equivalents at beginning of period | 1,905,713 | 845,889 | 201,890 |
| Cash and cash equivalents at end of period | $1,196,908 | $1,905,713 | $845,889 |
| Supplemental Disclosures |  |  |  |
| Interest paid | $32,060 | $20,539 | $9,041 |
| Income taxes paid | 9,461 | 3,120 | 257 |
| Supplemental noncash investing activities |  |  |  |
| Acquisition of property and equipment included in accounts payable and accrued liabilities | 267,334 | 254,393 | 38,789 |
| Estimated fair market value of facilities under build-to-suit lease | 174,749 | 50,076 | — |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 0, ungrounded 6, uncited 2, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 1,673,551, 1,523,523, 109.8%, 109.8%, 1,673,551, 1,523,523
- uncited numbers: 1,673,551, 1,523,523

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| For fiscal year 2015, net cash used in investing activities was $(1,673,551) and net cash provided by financing activities was $1,523,523. | None |  |
| Dividing $(1,673,551) by $1,523,523 gives a ratio of approximately -109.8%, or 109.8% in magnitude. [TSLA FY2015, Item 7, TSLA_FY2015_2015-12-31:230] [TSLA FY2015, Item 7, TSLA_FY2015_2015-12-31:231] | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 1.

**Generated answer**

> For fiscal year 2015, net cash used in investing activities was $(1,673,551) and net cash provided by financing activities was $1,523,523, both stated in thousands. [TSLA FY2015, Item 7, TSLA_FY2015_2015-12-31:227]
>
> Using those figures, the ratio of net cash used in investing activities to net cash provided by financing activities was approximately 109.8%. [TSLA FY2015, Item 7, TSLA_FY2015_2015-12-31:227]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-TSLA-2015` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2015,2015-12-31,4046025000,-888663000,-716629000,8092460000,69… |
| 2 | `TSLA_FY2015_2015-12-31:231` | Item 7 › Cash Flows from Financing Activities |  | #2 | Net cash provided by financing activities was $1.52 billion, $2.14 billion and $635.4 million in 2015, 2014 and 2013. Cash flows from financing activities during the twelve months ended December 31, 2015 consisted primar… |
| 3 | `TSLA_FY2015_2015-12-31:227` | Item 7 › Summary of Cash Flows | ✓ | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Net cash provided by (used in) operating activities \| $(524,499) \| $(57,337) \| $264,804 \| \| Net cash used in investing activities \| (1,673,55… |
| 4 | `TSLA_FY2015_2015-12-31:230` | Item 7 › Cash Flows from Investing Activities |  |  | Cash flows from investing activities primarily relate to capital expenditures to support our growth in operations, including investments in Model S manufacturing equipment and tooling and our stores, service centers and … |
| 5 | `TSLA_FY2015_2015-12-31:270` | Item 8 › (in thousands) |  | #1 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Maturities of short-term marketable securities \| — \| 189,131 \| — \| \| Business acquisition \| (12,260) \| — \| — \| \| Net cash used in investing a… |
| 6 | `TSLA_FY2015_2015-12-31:271` | Item 8 › (in thousands) |  | #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Principal payments on capital leases and other debt \| (203,780) \| (11,179) \| (8,425) \| \| Collateralized lease borrowing \| 568,745 \| 3,271 \| —… |
| 7 | `TSLA_FY2015_2015-12-31:268` | Item 8 › (in thousands) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Cash Flows From Operating Activities \| \| \| \| \| Net loss \| $(888,663) \| $(294,040) \| $(74,014) \| \| Adjustments to reconcile net loss to net ca… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `TSLA_FY2015_2015-12-31:231`** (gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Cash Flows from Financing Activities
Net cash provided by financing activities was $1.52 billion, $2.14 billion and $635.4 million in 2015, 2014 and 2013. Cash flows from financing activities during the twelve months ended December 31, 2015 consisted primarily of $738.3 million net proceeds from August 2015 public offering of 3,099,173 shares of common stock and $568.7 received from vehicle sales to our bank leasing partners. The decrease in cash provided from financing in 2015 as compared to 2014 was primarily due to $2.1 billion net proceeds received in 2014 from issuance of our 2019 and 2021 Notes. The increase in cash provided from financing in 2014 as compared to 2013 was primarily due to $2.1 billion net proceeds from the issuance of our 2019 and 2021 Notes, including the associated hedge and warrant transactions, representing a $1.5 billion increase in debt financing as compared to 2013. Cash flows from financing in 2013 that did not recur in 2014 included proceeds of $415.0 million from the issuance of common stock in public and private offerings and $452.3 million used to repay our DOE loans. 0.25% and 1.25% Convertible Senior Notes and Bond Hedge and Warrant Transactions
````

**#3 `TSLA_FY2015_2015-12-31:227`** (cited, gold #1, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Summary of Cash Flows (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2015 | 2014 | 2013 |
| Net cash provided by (used in) operating activities | $(524,499) | $(57,337) | $264,804 |
| Net cash used in investing activities | (1,673,551) | (990,444) | (249,417) |
| Net cash provided by financing activities | 1,523,523 | 2,143,130 | 635,422 |
````

**#5 `TSLA_FY2015_2015-12-31:270`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (in thousands) (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2015 | 2014 | 2013 |
| Maturities of short-term marketable securities | — | 189,131 | — |
| Business acquisition | (12,260) | — | — |
| Net cash used in investing activities | (1,673,551) | (990,444) | (249,417) |
| Cash Flows From Financing Activities |  |  |  |
| Proceeds from issuance of convertible and other debt | 318,972 | 2,300,000 | 660,000 |
| Proceeds from issuance of common stock in public offering | 730,000 | — | 360,000 |
| Proceeds from issuance of warrants | — | 389,160 | 120,318 |
| Proceeds from exercise of stock options and other stock issuances | 106,611 | 100,455 | 95,307 |
| Proceeds from issuance of common stock in private placement | 20,000 | — | 55,000 |
| Principal payments on DOE loans | — | — | (452,337) |
| Purchase of convertible note hedges | — | (603,428) | (177,540) |
| Common stock and convertible debt issuance costs | (17,025) | (35,149) | (16,901) |
````

**#6 `TSLA_FY2015_2015-12-31:271`** (gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (in thousands) (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2015 | 2014 | 2013 |
| Principal payments on capital leases and other debt | (203,780) | (11,179) | (8,425) |
| Collateralized lease borrowing | 568,745 | 3,271 | — |
| Net cash provided by financing activities | 1,523,523 | 2,143,130 | 635,422 |
| Effect of exchange rate changes on cash and cash equivalents | (34,278) | (35,525) | (6,810) |
| Net increase (decrease) in cash and cash equivalents | (708,805) | 1,059,824 | 643,999 |
| Cash and cash equivalents at beginning of period | 1,905,713 | 845,889 | 201,890 |
| Cash and cash equivalents at end of period | $1,196,908 | $1,905,713 | $845,889 |
| Supplemental Disclosures |  |  |  |
| Interest paid | $32,060 | $20,539 | $9,041 |
| Income taxes paid | 9,461 | 3,120 | 257 |
| Supplemental noncash investing activities |  |  |  |
| Acquisition of property and equipment included in accounts payable and accrued liabilities | 267,334 | 254,393 | 38,789 |
| Estimated fair market value of facilities under build-to-suit lease | 174,749 | 50,076 | — |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| For fiscal year 2015, net cash used in investing activities was $(1,673,551) and net cash provided by financing activities was $1,523,523, both stated in thousands. [TSLA FY2015, Item 7, TSLA_FY2015_2015-12-31:227] | None |  |
| Using those figures, the ratio of net cash used in investing activities to net cash provided by financing activities was approximately 109.8%. [TSLA FY2015, Item 7, TSLA_FY2015_2015-12-31:227] | None |  |

</details>
