# gold-010: Multi-hop table (one filing)

[← all cases](../README.md) · company: Walmart Inc. (WMT) · fiscal year: 2015 · recipe `table` · hop `multi` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> By what percentage did Walmart's total international segment retail square footage increase from fiscal year 2011 to fiscal year 2015?

**Gold answer**

> 29.41%

**Program**: `subtract(367630, 284071), divide(#0, 284071), multiply(#1, 100)` → `29.414829391243742`

**Gold numbers** (RQ2 numeric_accuracy targets): 29.41%

**Gold evidence**

1. `WMT_FY2015_2015-01-31` · ITEM 1. BUSINESS › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) · table

   > 2011 | 328 | 56,317 | 5 | 270 | 414 | 24,513 | 1,364 | 73,620 | 385 | 31,009 | 4,191 | 284,071

2. `WMT_FY2015_2015-01-31` · ITEM 1. BUSINESS › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) · table

   > 2015 | 411 | 68,269 | 20 | 1,083 | 431 | 24,429 | 2,290 | 98,419 | 592 | 36,277 | 6,290 | 367,630

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 11 | 10 |
| recall@5 | 0.50 | 0.00 | 0.00 | 0.00 |
| recall@all | 0.50 | 0.00 | 1.00 | 0.00 |
| complete@all | 0 | 0 | 1 | 0 |
| average precision (lexical) | 0.25 | 0.00 | 0.15 | 0.00 |
| gold evidence first rank | #1: 4, #2: – | #1: –, #2: – | #1: 9, #2: 11 | #1: –, #2: – |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✗ | ✓ | ✗ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 1.00 | 0.00 |
| citation precision | 1.00 | – | 1.00 | 1.00 |
| citation recall | 1.00 | – | 1.00 | 1.00 |
| citation F1 | 1.00 | – | 1.00 | 1.00 |
| has a citation | 1 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 1.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 2696 | 1304 | 13159 | 18845 |
| cost (USD) | 0.0005 | 0.0002 | 0.0481 | 0.0629 |
| latency (s) | 2.5 | 5.6 | 21.6 | 23.6 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> Walmart International total segment retail square footage increased from **284,071** in fiscal **2011** to **326,245** in fiscal **2015** [4].
>
> Percentage increase:
>
> \[
> \frac{326,245 - 284,071}{284,071} \times 100 \approx 14.8\%
> \]
>
> So, the total international segment retail square footage increased by **about 14.8%** from fiscal 2011 to fiscal 2015 [4].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `WMT_FY2015_2015-01-31:33` | Item 1 › Walmart U.S. Segment |  |  | The Walmart U.S. segment is a mass merchandiser of consumer products, operating under the "Walmart" or "Wal-Mart" brands, as well as walmart.com. The Walmart U.S. segment had net sales of $288.0 billion, $279.4 billion a… |
| 2 | `WMT_FY2015_2015-01-31:46` | Item 1 › Walmart International Segment |  |  | The Walmart International segment consists of operations in 26 countries outside of the U.S. and includes numerous formats divided into three major categories: retail, wholesale and other. These categories consist of num… |
| 3 | `WMT_FY2015_2015-01-31:34` | Item 1 › Walmart U.S. Segment |  |  | \| \| Minimum Square Feet \| Maximum Square Feet \| Average Square Feet \| \|---\|---\|---\|---\| \| Supercenters (general merchandise and grocery) \| 69,000 \| 260,000 \| 178,000 \| \| Discount stores (general merchandise and limited g… |
| 4 | `WMT_FY2015_2015-01-31:49` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) | ✓ | #1 | \| \| Africa \| \| Argentina \| \| Brazil \| \| Canada \| \| Central America \| \| Chile \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 2015 \| 396 \| 21,223 \| 105 \| 8,119 \| 557 \| 33,028 \| 394 \| 50,927 \| 690 \| 11,094 \| 40… |
| 5 | `WMT_FY2015_2015-01-31:30` | Item 1 › Information About Our Segments |  |  | The Company is engaged in the operation of retail, wholesale and other units located throughout the U.S., Africa, Argentina, Brazil, Canada, Central America, Chile, China, India, Japan, Mexico and the United Kingdom. The… |
| 6 | `WMT_FY2015_2015-01-31:36` | Item 1 › RETAIL UNIT COUNT AND RETAIL SQUARE FEET(1) |  |  | \| \| Supercenters \| \| \| \| \| Discount Stores \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Fiscal Year \| Opened \| Closed \| Conversions(2) \| Total \| Square Feet \| Opened \| Closed \| Conversions(2) \| Total \| Squar… |
| 7 | `WMT_FY2015_2015-01-31:31` | Item 1 › Information About Our Segments |  |  | Walmart International consists of operations in 26 countries outside of the U.S. and includes numerous formats divided into three major categories: retail, wholesale and other. These categories consist of numerous format… |
| 8 | `WMT_FY2015_2015-01-31:52` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | \| Geographic Market \| Retail \| Wholesale \| Other(2) \| Total \| \|---\|---\|---\|---\|---\| \| Africa(3) \| 302 \| 94 \| — \| 396 \| \| Argentina \| 105 \| — \| — \| 105 \| \| Brazil \| 468 \| 76 \| 13 \| 557 \| \| Canada \| 394 \| — \| — \| 394 \| \| C… |
| 9 | `WMT_FY2015_2015-01-31:57` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | Distribution. We utilize a total of 156 distribution facilities located in Argentina, Brazil, Canada, Central America, Chile, China, Japan, Mexico, South Africa and the United Kingdom. Through these facilities, we proces… |
| 10 | `WMT_FY2015_2015-01-31:47` | Item 1 › Walmart International Segment |  |  | Generally, retail units range in size from 4,000 square feet to 250,000 square feet. Our wholesale stores generally range in size from 35,000 square feet to 70,000 square feet. Other, which includes restaurants, drugstor… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#4 `WMT_FY2015_2015-01-31:49`** (cited, gold #1)

````text
ITEM 1. BUSINESS > UNIT COUNT(1) AND RETAIL SQUARE FEET(2) (table)
|  | Africa |  | Argentina |  | Brazil |  | Canada |  | Central America |  | Chile |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2015 | 396 | 21,223 | 105 | 8,119 | 557 | 33,028 | 394 | 50,927 | 690 | 11,094 | 404 | 14,762 |
|  | China |  | India |  | Japan |  | Mexico(3) |  | United Kingdom |  | Total Segment |  |
| Fiscal Year | Unit Count | Square Feet | Unit Count | Square Feet | Unit Count | Square Feet | Unit Count | Square Feet | Unit Count | Square Feet | Unit Count | Square Feet |
| Balance forward | 279 | 49,401 | 1 | 50 | 414 | 24,292 | 1,109 | 66,504 | 371 | 30,053 | 3,739 | 263,283 |
| 2011 | 328 | 56,317 | 5 | 270 | 414 | 24,513 | 1,364 | 73,620 | 385 | 31,009 | 4,191 | 284,071 |
| 2012 | 370 | 62,124 | 15 | 826 | 419 | 24,521 | 1,724 | 82,611 | 541 | 33,765 | 5,287 | 326,245 |
````

</details>

RQ2 citation match (section level): `cited=[('WMT', 'Item 1')] gold=[(None, 'Item 1')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `WMT_FY2015_2015-01-31:31` | Item 1 › Information About Our Segments |  |  | Walmart International consists of operations in 26 countries outside of the U.S. and includes numerous formats divided into three major categories: retail, wholesale and other. These categories consist of numerous format… |
| 2 | `WMT_FY2015_2015-01-31:57` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | Distribution. We utilize a total of 156 distribution facilities located in Argentina, Brazil, Canada, Central America, Chile, China, Japan, Mexico, South Africa and the United Kingdom. Through these facilities, we proces… |
| 3 | `WMT_FY2015_2015-01-31:33` | Item 1 › Walmart U.S. Segment |  |  | The Walmart U.S. segment is a mass merchandiser of consumer products, operating under the "Walmart" or "Wal-Mart" brands, as well as walmart.com. The Walmart U.S. segment had net sales of $288.0 billion, $279.4 billion a… |
| 4 | `WMT_FY2015_2015-01-31:46` | Item 1 › Walmart International Segment |  |  | The Walmart International segment consists of operations in 26 countries outside of the U.S. and includes numerous formats divided into three major categories: retail, wholesale and other. These categories consist of num… |
| 5 | `WMT_FY2015_2015-01-31:30` | Item 1 › Information About Our Segments |  |  | The Company is engaged in the operation of retail, wholesale and other units located throughout the U.S., Africa, Argentina, Brazil, Canada, Central America, Chile, China, India, Japan, Mexico and the United Kingdom. The… |

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 11, cited: 2.

**Generated answer**

> Walmart International total segment retail square footage increased from 284,071 in fiscal 2011 to 367,630 in fiscal 2015 [WMT FY2015, Item 1, WMT_FY2015_2015-01-31:49] [WMT FY2015, Item 1, WMT_FY2015_2015-01-31:50].  
> The increase was 29.4%, calculated as (367,630 - 284,071) / 284,071 × 100 [WMT FY2015, Item 1, WMT_FY2015_2015-01-31:49] [WMT FY2015, Item 1, WMT_FY2015_2015-01-31:50].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `WMT_FY2015_2015-01-31:57` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | Distribution. We utilize a total of 156 distribution facilities located in Argentina, Brazil, Canada, Central America, Chile, China, Japan, Mexico, South Africa and the United Kingdom. Through these facilities, we proces… |
| 2 | `WMT_FY2015_2015-01-31:58` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | \| \| Owned and Operated \| Owned and Third Party Operated \| Leased and Operated \| Leased and Third Party Operated \| Total \| \|---\|---\|---\|---\|---\|---\| \| International distribution facilities \| 41 \| 11 \| 70 \| 34 \| 156 \| |
| 3 | `WMT_FY2015_2015-01-31:45` | Item 1 › RETAIL UNIT COUNT AND RETAIL SQUARE FEET(1) |  |  | \| \| Owned and Operated \| Owned and Third Party Operated \| Leased and Operated \| Leased and Third Party Operated \| Total \| \|---\|---\|---\|---\|---\|---\| \| Walmart U.S. distribution facilities \| 102 \| 2 \| 6 \| 24 \| 134 \| |
| 4 | `WMT_FY2015_2015-01-31:46` | Item 1 › Walmart International Segment |  |  | The Walmart International segment consists of operations in 26 countries outside of the U.S. and includes numerous formats divided into three major categories: retail, wholesale and other. These categories consist of num… |
| 5 | `WMT_FY2015_2015-01-31:41` | Item 1 › RETAIL UNIT COUNT AND RETAIL SQUARE FEET(1) |  |  | \| \| Fiscal Years Ended January 31, \| \| \| \|---\|---\|---\|---\| \| STRATEGIC MERCHANDISE UNITS \| 2015 \| 2014 \| 2013 \| \| Grocery \| 56% \| 56% \| 55% \| \| Health and wellness \| 11% \| 10% \| 11% \| \| Entertainment \| 10% \| 11% \| 11% \| … |
| 6 | `WMT_FY2015_2015-01-31:36` | Item 1 › RETAIL UNIT COUNT AND RETAIL SQUARE FEET(1) |  |  | \| \| Supercenters \| \| \| \| \| Discount Stores \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Fiscal Year \| Opened \| Closed \| Conversions(2) \| Total \| Square Feet \| Opened \| Closed \| Conversions(2) \| Total \| Squar… |
| 7 | `WMT_FY2015_2015-01-31:48` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | \| \| Africa \| \| Argentina \| \| Brazil \| \| Canada \| \| Central America \| \| Chile \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Fiscal Year \| Unit Count \| Square Feet \| Unit Count \| Square Feet \| Unit Count \| Sq… |
| 8 | `WMT_FY2015_2015-01-31:37` | Item 1 › RETAIL UNIT COUNT AND RETAIL SQUARE FEET(1) |  |  | \| \| Supercenters \| \| \| \| \| Discount Stores \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Fiscal Year \| Opened \| Closed \| Conversions(2) \| Total \| Square Feet \| \| Opened(3) \| Closed \| Total \| Square Feet \| \| B… |
| 9 | `WMT_FY2015_2015-01-31:49` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) | ✓ | #1 | \| \| Africa \| \| Argentina \| \| Brazil \| \| Canada \| \| Central America \| \| Chile \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 2015 \| 396 \| 21,223 \| 105 \| 8,119 \| 557 \| 33,028 \| 394 \| 50,927 \| 690 \| 11,094 \| 40… |
| 10 | `WMT_FY2015_2015-01-31:52` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | \| Geographic Market \| Retail \| Wholesale \| Other(2) \| Total \| \|---\|---\|---\|---\|---\| \| Africa(3) \| 302 \| 94 \| — \| 396 \| \| Argentina \| 105 \| — \| — \| 105 \| \| Brazil \| 468 \| 76 \| 13 \| 557 \| \| Canada \| 394 \| — \| — \| 394 \| \| C… |
| 11 | `WMT_FY2015_2015-01-31:50` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) | ✓ | #2 | \| \| Africa \| \| Argentina \| \| Brazil \| \| Canada \| \| Central America \| \| Chile \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 2013 \| 393 \| 65,801 \| 20 \| 1,083 \| 438 \| 24,448 \| 1,988 \| 88,833 \| 565 \| 34,810 \| 5… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#9 `WMT_FY2015_2015-01-31:49`** (cited, gold #1)

````text
ITEM 1. BUSINESS > UNIT COUNT(1) AND RETAIL SQUARE FEET(2) (table)
|  | Africa |  | Argentina |  | Brazil |  | Canada |  | Central America |  | Chile |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2015 | 396 | 21,223 | 105 | 8,119 | 557 | 33,028 | 394 | 50,927 | 690 | 11,094 | 404 | 14,762 |
|  | China |  | India |  | Japan |  | Mexico(3) |  | United Kingdom |  | Total Segment |  |
| Fiscal Year | Unit Count | Square Feet | Unit Count | Square Feet | Unit Count | Square Feet | Unit Count | Square Feet | Unit Count | Square Feet | Unit Count | Square Feet |
| Balance forward | 279 | 49,401 | 1 | 50 | 414 | 24,292 | 1,109 | 66,504 | 371 | 30,053 | 3,739 | 263,283 |
| 2011 | 328 | 56,317 | 5 | 270 | 414 | 24,513 | 1,364 | 73,620 | 385 | 31,009 | 4,191 | 284,071 |
| 2012 | 370 | 62,124 | 15 | 826 | 419 | 24,521 | 1,724 | 82,611 | 541 | 33,765 | 5,287 | 326,245 |
````

**#11 `WMT_FY2015_2015-01-31:50`** (cited, gold #2)

````text
ITEM 1. BUSINESS > UNIT COUNT(1) AND RETAIL SQUARE FEET(2) (table)
|  | Africa |  | Argentina |  | Brazil |  | Canada |  | Central America |  | Chile |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2013 | 393 | 65,801 | 20 | 1,083 | 438 | 24,448 | 1,988 | 88,833 | 565 | 34,810 | 5,783 | 345,673 |
| 2014 | 405 | 67,205 | 20 | 1,083 | 438 | 24,489 | 2,199 | 94,900 | 576 | 35,416 | 6,107 | 358,207 |
| 2015 | 411 | 68,269 | 20 | 1,083 | 431 | 24,429 | 2,290 | 98,419 | 592 | 36,277 | 6,290 | 367,630 |
````

</details>

RQ2 citation match (section level): `cited=[('WMT', 'Item 1')] gold=[(None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Walmart International total segment retail square footage increased from 284,071 in fiscal 2011 to 367,630 in fiscal 2015 [WMT FY2015, Item 1, WMT_FY2015_2015-01-31:49] [WMT FY2015, Item 1, WMT_FY2015_2015-01-31:50]. | None |  |
| The increase was 29.4%, calculated as (367,630 - 284,071) / 284,071 × 100 [WMT FY2015, Item 1, WMT_FY2015_2015-01-31:49] [WMT FY2015, Item 1, WMT_FY2015_2015-01-31:50]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 10, cited: 1.

**Generated answer**

> Walmart’s total international segment retail square footage increased from 98,342 in fiscal 2011 to 108,557 in fiscal 2015, an increase of about 10.4%. [WMT FY2015, Item 1, WMT_FY2015_2015-01-31:48] [WMT FY2015, Item 1, WMT_FY2015_2015-01-31:49]
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 98,342, 108,557; these citation tags do not map to any retrieved chunk: [WMT FY2015, Item 1, WMT_FY2015_2015-01-31:49]; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `WMT_FY2015_2015-01-31:57` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | Distribution. We utilize a total of 156 distribution facilities located in Argentina, Brazil, Canada, Central America, Chile, China, Japan, Mexico, South Africa and the United Kingdom. Through these facilities, we proces… |
| 2 | `WMT_FY2015_2015-01-31:58` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | \| \| Owned and Operated \| Owned and Third Party Operated \| Leased and Operated \| Leased and Third Party Operated \| Total \| \|---\|---\|---\|---\|---\|---\| \| International distribution facilities \| 41 \| 11 \| 70 \| 34 \| 156 \| |
| 3 | `WMT_FY2015_2015-01-31:45` | Item 1 › RETAIL UNIT COUNT AND RETAIL SQUARE FEET(1) |  |  | \| \| Owned and Operated \| Owned and Third Party Operated \| Leased and Operated \| Leased and Third Party Operated \| Total \| \|---\|---\|---\|---\|---\|---\| \| Walmart U.S. distribution facilities \| 102 \| 2 \| 6 \| 24 \| 134 \| |
| 4 | `WMT_FY2015_2015-01-31:46` | Item 1 › Walmart International Segment |  |  | The Walmart International segment consists of operations in 26 countries outside of the U.S. and includes numerous formats divided into three major categories: retail, wholesale and other. These categories consist of num… |
| 5 | `WMT_FY2015_2015-01-31:41` | Item 1 › RETAIL UNIT COUNT AND RETAIL SQUARE FEET(1) |  |  | \| \| Fiscal Years Ended January 31, \| \| \| \|---\|---\|---\|---\| \| STRATEGIC MERCHANDISE UNITS \| 2015 \| 2014 \| 2013 \| \| Grocery \| 56% \| 56% \| 55% \| \| Health and wellness \| 11% \| 10% \| 11% \| \| Entertainment \| 10% \| 11% \| 11% \| … |
| 6 | `WMT_FY2015_2015-01-31:36` | Item 1 › RETAIL UNIT COUNT AND RETAIL SQUARE FEET(1) |  |  | \| \| Supercenters \| \| \| \| \| Discount Stores \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Fiscal Year \| Opened \| Closed \| Conversions(2) \| Total \| Square Feet \| Opened \| Closed \| Conversions(2) \| Total \| Squar… |
| 7 | `WMT_FY2015_2015-01-31:37` | Item 1 › RETAIL UNIT COUNT AND RETAIL SQUARE FEET(1) |  |  | \| \| Supercenters \| \| \| \| \| Discount Stores \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Fiscal Year \| Opened \| Closed \| Conversions(2) \| Total \| Square Feet \| \| Opened(3) \| Closed \| Total \| Square Feet \| \| B… |
| 8 | `WMT_FY2015_2015-01-31:48` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) | ✓ |  | \| \| Africa \| \| Argentina \| \| Brazil \| \| Canada \| \| Central America \| \| Chile \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Fiscal Year \| Unit Count \| Square Feet \| Unit Count \| Square Feet \| Unit Count \| Sq… |
| 9 | `WMT_FY2015_2015-01-31:130` | Item 2 |  |  | \| \| Owned and Operated \| Owned and Third Party Operated \| Leased and Operated \| Leased and Third Party Operated \| Total \| \|---\|---\|---\|---\|---\|---\| \| U.S. properties \| \| \| \| \| \| \| Walmart U.S. retail units \| 3,860 \| — \| … |
| 10 | `WMT_FY2015_2015-01-31:52` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | \| Geographic Market \| Retail \| Wholesale \| Other(2) \| Total \| \|---\|---\|---\|---\|---\| \| Africa(3) \| 302 \| 94 \| — \| 396 \| \| Argentina \| 105 \| — \| — \| 105 \| \| Brazil \| 468 \| 76 \| 13 \| 557 \| \| Canada \| 394 \| — \| — \| 394 \| \| C… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#8 `WMT_FY2015_2015-01-31:48`** (cited)

````text
ITEM 1. BUSINESS > UNIT COUNT(1) AND RETAIL SQUARE FEET(2) (table)
|  | Africa |  | Argentina |  | Brazil |  | Canada |  | Central America |  | Chile |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fiscal Year | Unit Count | Square Feet | Unit Count | Square Feet | Unit Count | Square Feet | Unit Count | Square Feet | Unit Count | Square Feet | Unit Count | Square Feet |
| Balance forward | — | — | 43 | 5,185 | 434 | 28,695 | 317 | 40,225 | 519 | 8,441 | 252 | 10,437 |
| 2011 | — | — | 63 | 6,211 | 479 | 30,272 | 325 | 42,005 | 549 | 8,739 | 279 | 11,115 |
| 2012 | 347 | 18,529 | 88 | 7,270 | 512 | 31,575 | 333 | 43,738 | 622 | 9,501 | 316 | 11,785 |
| 2013 | 377 | 19,775 | 94 | 7,531 | 558 | 32,494 | 379 | 48,354 | 642 | 9,873 | 329 | 12,671 |
| 2014 | 379 | 20,513 | 104 | 8,062 | 556 | 32,501 | 389 | 49,914 | 661 | 10,427 | 380 | 13,697 |
````

</details>

RQ2 citation match (section level): `cited=[('WMT', 'Item 1')] gold=[(None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 1, ungrounded 2, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 98,342, 108,557

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Walmart’s total international segment retail square footage increased from 98,342 in fiscal 2011 to 108,557 in fiscal 2015, an increase of about 10.4%. [WMT FY2015, Item 1, WMT_FY2015_2015-01-31:48] [WMT FY2015, Item 1, WMT_FY2015_2015-01-31:49] | None |  |

</details>
