# gold-058: Table + text (one filing)

[← all cases](../README.md) · company: Walmart Inc. (WMT) · fiscal year: 2017 · recipe `table_text` · hop `multi` · answer type `mixed` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> Based on Walmart Inc.'s fiscal year 2017 10-K, how did the total square footage of its international segment change between fiscal 2016 and fiscal 2017, and what specific geopolitical risk factor does the company cite as a potential driver of negative financial performance for its operations in the United Kingdom?

**Gold answer**

> Total international retail square footage increased by 4,571 thousand square feet, from 372,198 thousand in fiscal 2016 to 376,769 thousand in fiscal 2017. For the United Kingdom, Walmart cites the UK's anticipated exit from the European Union (Brexit), which could bring changes in trade policies or in labor, immigration, tax or other laws, alongside currency fluctuations and higher food costs.

**Program**: `subtract(376769, 372198)` → `4571.0`

**Gold numbers** (RQ2 numeric_accuracy targets): 4,571 thousand

**Key points** (RQ3 keypoint_recall targets)

1. International retail square footage was 372,198 thousand in fiscal 2016 and 376,769 thousand in fiscal 2017.
2. The increase was 4,571 thousand square feet.
3. The UK risk cited is the UK's anticipated exit from the European Union (Brexit).

**Gold evidence**

1. `WMT_FY2017_2017-01-31` · ITEM 1. BUSINESS › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) · table

   > | 2016 | 432 | 71,724 | 21 | 1,146 | 346 | 22,551 | 2,360 | 100,308 | 621 | 37,044 | 6,299 | 372,198 |

2. `WMT_FY2017_2017-01-31` · ITEM 1. BUSINESS › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) · table

   > | 2017 | 439 | 73,172 | 20 | 1,091 | 341 | 21,921 | 2,411 | 101,681 | 631 | 37,338 | 6,363 | 376,769 |

3. `WMT_FY2017_2017-01-31` · ITEM 1A. RISK FACTORS › Legal, Tax, Regulatory, Compliance, Reputational and Other Risks · text

   > Our business and results of operations in the UK may be negatively affected by fluctuations in currency exchange rates, increases in food costs, changes in trade policies, or changes in labor, immigration, tax or other laws resulting from the UK's anticipated exit from the European Union.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 12 | 12 |
| recall@5 | 0.00 | 0.00 | 0.00 | 0.00 |
| recall@all | 0.67 | 0.00 | 0.00 | 0.67 |
| complete@all | 0 | 0 | 0 | 0 |
| average precision (lexical) | 0.11 | 0.00 | 0.00 | 0.10 |
| gold evidence first rank | #1: 9, #2: 9, #3: – | #1: –, #2: –, #3: – | #1: –, #2: –, #3: – | #1: 10, #2: 10, #3: – |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✗ | ✗ | ✓ |
| keypoint_recall | 0.67 | 0.00 | 0.67 | 0.67 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 0.00 | 1.00 |
| citation precision | 1.00 | – | 1.00 | 1.00 |
| citation recall | 1.00 | – | 0.50 | 0.50 |
| citation F1 | 1.00 | – | 0.67 | 0.67 |
| has a citation | 1 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 3216 | 1273 | 18075 | 23256 |
| cost (USD) | 0.0005 | 0.0002 | 0.0621 | 0.0760 |
| latency (s) | 2.6 | 6.8 | 24.9 | 28.2 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Walmart’s international segment total square footage increased from **372,198** in fiscal **2016** to **376,769** in fiscal **2017**, a rise of **4,571** square feet [9].
>
> As for the United Kingdom risk factor, Walmart cites the potential imposition by the **U.S. of a border tax or border adjustment tax, new or higher tariffs, or other trade restrictions**, which could trigger retaliatory tariffs or taxes and harm the reputation of U.S.-based companies, potentially hurting financial performance in countries where it operates, including the U.K. [1].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `WMT_FY2017_2017-01-31:121` | Item 1A › Legal, Tax, Regulatory, Compliance, Reputational and Other Risks | ✓ |  | During fiscal 2017, our Walmart International operations generated approximately 24% of our consolidated net sales. Our operating segments also source goods and services from other countries. Our future operating results… |
| 2 | `WMT_FY2017_2017-01-31:45` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | \| \| Africa \| \| Argentina \| \| Brazil \| \| Canada \| \| Central America \| \| Chile \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 2017 \| 412 \| 22,542 \| 107 \| 8,264 \| 498 \| 30,642 \| 410 \| 53,088 \| 731 \| 11,770 \| 36… |
| 3 | `WMT_FY2017_2017-01-31:82` | Item 1A › General or macro-economic factors, both domestically and internationally, may materially adversely affect our financial performance. |  |  | It is difficult to predict consistently and successfully the products and services our customers will demand and changes in their shopping patterns. The success of our business depends in part on how accurately we predic… |
| 4 | `WMT_FY2017_2017-01-31:44` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | \| \| Africa \| \| Argentina \| \| Brazil \| \| Canada \| \| Central America \| \| Chile \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Fiscal Year \| Unit Count \| Square Feet \| Unit Count \| Square Feet \| Unit Count \| Sq… |
| 5 | `WMT_FY2017_2017-01-31:31` | Item 1 › RETAIL UNIT COUNT AND RETAIL SQUARE FEET(1) |  |  | \| \| Supercenters \| \| \| \| \| Discount Stores \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Fiscal Year \| Opened \| Closed \| Conversions(2) \| Total \| Square Feet \| Opened \| Closed \| Conversions(2) \| Total \| Squar… |
| 6 | `WMT_FY2017_2017-01-31:113` | Item 1A › Changes in the results of our retail pharmacy business could adversely affect our overall results of operations, cash flows and liquidity. |  |  | Impediments to the expansion of our Walmart International operations, and the performance of strategic alliances to support the expansion of that segment, could materially adversely affect our financial performance. Our … |
| 7 | `WMT_FY2017_2017-01-31:32` | Item 1 › RETAIL UNIT COUNT AND RETAIL SQUARE FEET(1) |  |  | \| \| Supercenters \| \| \| \| \| Discount Stores \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Fiscal Year \| Opened \| Closed \| Conversions(2) \| Total \| Square Feet \| \| Opened(3) \| Closed \| Total \| Square Feet \| \| B… |
| 8 | `WMT_FY2017_2017-01-31:15` | Cautionary Statement Regarding Forward-Looking Statements |  |  | • consumer confidence, disposable income, credit availability, spending levels, shopping patterns, debt levels, and demand for certain merchandise; • trends in consumer shopping habits around the world and in the markets… |
| 9 | `WMT_FY2017_2017-01-31:46` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) | ✓ | #1, #2 | \| \| Africa \| \| Argentina \| \| Brazil \| \| Canada \| \| Central America \| \| Chile \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 2015 \| 411 \| 68,269 \| 20 \| 1,083 \| 431 \| 24,429 \| 2,290 \| 98,419 \| 592 \| 36,277 \| 6… |
| 10 | `WMT_FY2017_2017-01-31:48` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | \| Geographic Market \| Retail \| Wholesale \| Other(2) \| Total \| \|---\|---\|---\|---\|---\| \| Africa(3) \| 326 \| 86 \| — \| 412 \| \| Argentina \| 107 \| — \| — \| 107 \| \| Brazil \| 413 \| 71 \| 14 \| 498 \| \| Canada \| 410 \| — \| — \| 410 \| \| C… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `WMT_FY2017_2017-01-31:121`** (cited)

````text
ITEM 1A. RISK FACTORS > Legal, Tax, Regulatory, Compliance, Reputational and Other Risks
During fiscal 2017, our Walmart International operations generated approximately 24% of our consolidated net sales. Our operating segments also source goods and services from other countries. Our future operating results in these countries could be negatively affected by a variety of factors, most of which are beyond our control. These factors include political conditions, including political instability, local and global economic conditions, legal and regulatory constraints, local product safety and environmental laws, tax regulations, local labor laws, anti-money laundering laws and regulations, trade policies, currency regulations, and other matters in any of the countries or regions in which we operate, now or in the future. The potential imposition by the U.S. of a border tax or border adjustment tax, new or higher tariffs or other restrictions on trade discussed above which impact a country in which we have operations could result in actions by that country to impose new, or increase existing tariffs or taxes on products imported into such country from the U.S. or elsewhere and could damage the reputations of U.S.-based companies, including us, with customers and others in that country. This could materially adversely affect the financial performance of our operations in such country or countries.
````

**#9 `WMT_FY2017_2017-01-31:46`** (cited, gold #1, gold #2)

````text
ITEM 1. BUSINESS > UNIT COUNT(1) AND RETAIL SQUARE FEET(2) (table)
|  | Africa |  | Argentina |  | Brazil |  | Canada |  | Central America |  | Chile |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2015 | 411 | 68,269 | 20 | 1,083 | 431 | 24,429 | 2,290 | 98,419 | 592 | 36,277 | 6,290 | 367,630 |
| 2016 | 432 | 71,724 | 21 | 1,146 | 346 | 22,551 | 2,360 | 100,308 | 621 | 37,044 | 6,299 | 372,198 |
| 2017 | 439 | 73,172 | 20 | 1,091 | 341 | 21,921 | 2,411 | 101,681 | 631 | 37,338 | 6,363 | 376,769 |
````

</details>

RQ2 citation match (section level): `cited=[('WMT', 'Item 1A'), ('WMT', 'Item 1')] gold=[(None, 'Item 1'), (None, 'Item 1A')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `WMT_FY2017_2017-01-31:121` | Item 1A › Legal, Tax, Regulatory, Compliance, Reputational and Other Risks |  |  | During fiscal 2017, our Walmart International operations generated approximately 24% of our consolidated net sales. Our operating segments also source goods and services from other countries. Our future operating results… |
| 2 | `WMT_FY2017_2017-01-31:43` | Item 1 › Walmart International Segment |  |  | Generally, retail units range in size from 8,900 square feet to 185,000 square feet. Our wholesale stores generally range in size from 35,000 square feet to 70,000 square feet. Other, which includes drugstores and conven… |
| 3 | `WMT_FY2017_2017-01-31:115` | Item 1A › Changes in the results of our retail pharmacy business could adversely affect our overall results of operations, cash flows and liquidity. |  |  | Our Walmart International segment may also enter into strategic alliances in the countries in which we have existing operations or in other markets to expand our digital retail operations, physical retail operations or b… |
| 4 | `WMT_FY2017_2017-01-31:84` | Item 1A › General or macro-economic factors, both domestically and internationally, may materially adversely affect our financial performance. |  |  | Our Walmart U.S. segment competes with retailers operating discount, department, retail and wholesale grocers, drug, dollar, variety and specialty stores, supermarkets, supercenter-type stores and hypermarkets, as well a… |
| 5 | `WMT_FY2017_2017-01-31:120` | Item 1A › Legal, Tax, Regulatory, Compliance, Reputational and Other Risks |  |  | In fiscal 2017, our Walmart U.S. and Sam's Club operating segments generated approximately 76% of our consolidated net sales. The Federal Government has created the potential for significant changes in trade policies, in… |

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 12, cited: 2.

**Generated answer**

> Walmart International total segment square footage increased from 689,647 in fiscal 2016 to 699,289 in fiscal 2017, an increase of 9,642, with square feet reported in thousands. [WMT FY2017, Item 1, WMT_FY2017_2017-01-31:32] [WMT FY2017, Item 1, WMT_FY2017_2017-01-31:47]
>
> The filing does not disclose in the provided evidence blocks the specific geopolitical risk factor cited as a potential driver of negative financial performance for Walmart’s operations in the United Kingdom.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `WMT_FY2017_2017-01-31:31` | Item 1 › RETAIL UNIT COUNT AND RETAIL SQUARE FEET(1) |  |  | \| \| Supercenters \| \| \| \| \| Discount Stores \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Fiscal Year \| Opened \| Closed \| Conversions(2) \| Total \| Square Feet \| Opened \| Closed \| Conversions(2) \| Total \| Squar… |
| 2 | `WMT_FY2017_2017-01-31:23` | Item 1 › General |  |  | Our operations comprise three reportable segments: Walmart U.S., Walmart International and Sam's Club. Our fiscal year ends on January 31 for our United States ("U.S.") and Canadian operations. We consolidate all other o… |
| 3 | `WMT_FY2017_2017-01-31:47` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) | ✓ |  | (1) "Unit Count" includes retail stores, wholesale clubs and other, which includes drugstores and convenience stores. Walmart International unit counts, with the exception of Canada, are stated as of December 31, to corr… |
| 4 | `WMT_FY2017_2017-01-31:53` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | Distribution. We utilize a total of 176 distribution facilities located in Argentina, Brazil, Canada, Central America, Chile, China, Japan, Mexico, South Africa and the United Kingdom. Through these facilities, we proces… |
| 5 | `WMT_FY2017_2017-01-31:42` | Item 1 › Walmart International Segment |  |  | The Walmart International segment consists of operations in 27 countries outside of the U.S. and includes numerous formats divided into three major categories: retail, wholesale and other. These categories consist of num… |
| 6 | `WMT_FY2017_2017-01-31:28` | Item 1 › Walmart U.S. Segment |  |  | The Walmart U.S. segment is a mass merchandiser of consumer products, operating under the "Walmart," "Wal-Mart" and "Walmart Neighborhood Market" brands, as well as walmart.com and other digital retail. The Walmart U.S. … |
| 7 | `WMT_FY2017_2017-01-31:29` | Item 1 › Walmart U.S. Segment |  |  | \| \| Minimum Square Feet \| Maximum Square Feet \| Average Square Feet \| \|---\|---\|---\|---\| \| Supercenters (general merchandise and grocery) \| 69,000 \| 260,000 \| 178,000 \| \| Discount stores (general merchandise and limited g… |
| 8 | `WMT_FY2017_2017-01-31:32` | Item 1 › RETAIL UNIT COUNT AND RETAIL SQUARE FEET(1) | ✓ |  | \| \| Supercenters \| \| \| \| \| Discount Stores \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Fiscal Year \| Opened \| Closed \| Conversions(2) \| Total \| Square Feet \| \| Opened(3) \| Closed \| Total \| Square Feet \| \| B… |
| 9 | `WMT_FY2017_2017-01-31:36` | Item 1 › RETAIL UNIT COUNT AND RETAIL SQUARE FEET(1) |  |  | \| \| Fiscal Years Ended January 31, \| \| \| \|---\|---\|---\|---\| \| STRATEGIC MERCHANDISE UNITS \| 2017 \| 2016 \| 2015 \| \| Grocery \| 56% \| 56% \| 56% \| \| Health and wellness \| 11% \| 11% \| 11% \| \| General merchandise \| 33% \| 33% \| … |
| 10 | `WMT_FY2017_2017-01-31:44` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | \| \| Africa \| \| Argentina \| \| Brazil \| \| Canada \| \| Central America \| \| Chile \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Fiscal Year \| Unit Count \| Square Feet \| Unit Count \| Square Feet \| Unit Count \| Sq… |
| 11 | `WMT_FY2017_2017-01-31:45` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | \| \| Africa \| \| Argentina \| \| Brazil \| \| Canada \| \| Central America \| \| Chile \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 2017 \| 412 \| 22,542 \| 107 \| 8,264 \| 498 \| 30,642 \| 410 \| 53,088 \| 731 \| 11,770 \| 36… |
| 12 | `WMT_FY2017_2017-01-31:48` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | \| Geographic Market \| Retail \| Wholesale \| Other(2) \| Total \| \|---\|---\|---\|---\|---\| \| Africa(3) \| 326 \| 86 \| — \| 412 \| \| Argentina \| 107 \| — \| — \| 107 \| \| Brazil \| 413 \| 71 \| 14 \| 498 \| \| Canada \| 410 \| — \| — \| 410 \| \| C… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `WMT_FY2017_2017-01-31:47`** (cited)

````text
ITEM 1. BUSINESS > UNIT COUNT(1) AND RETAIL SQUARE FEET(2)
(1) "Unit Count" includes retail stores, wholesale clubs and other, which includes drugstores and convenience stores. Walmart International unit counts, with the exception of Canada, are stated as of December 31, to correspond with the fiscal year end of the related geographic market. Canada unit counts and square footage are stated as of January 31. For the balance forward, all country balances are stated as of the end of fiscal year 2012. (2) "Square Feet" columns are reported in thousands. (3) All periods presented exclude units and square feet for the Vips restaurant business. The Company completed the sale of the Vips restaurant business in fiscal 2015. Unit counts(1) as of January 31, 2017 for Walmart International are summarized by major category for each geographic market as follows:
````

**#8 `WMT_FY2017_2017-01-31:32`** (cited)

````text
ITEM 1. BUSINESS > RETAIL UNIT COUNT AND RETAIL SQUARE FEET(1) (table)
|  | Supercenters |  |  |  |  | Discount Stores |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| Fiscal Year | Opened | Closed | Conversions(2) | Total | Square Feet |  | Opened(3) | Closed | Total | Square Feet |
| Balance forward |  |  |  | 210 | 8,047 |  |  |  | 3,868 | 626,686 |
| 2013 | 79 | (3) | — | 286 | 11,226 |  | 141 | (4) | 4,005 | 640,733 |
| 2014 | 122 | — | (1) | 407 | 15,778 |  | 198 | — | 4,203 | 659,132 |
| 2015 | 235 | (3) | — | 639 | 23,370 |  | 316 | (3) | 4,516 | 680,112 |
| 2016 | 161 | (133) | — | 667 | 27,228 |  | 216 | (158) | 4,574 | 689,647 |
| 2017 | 73 | (5) | — | 735 | 30,012 |  | 111 | (13) | 4,672 | 699,289 |
````

</details>

RQ2 citation match (section level): `cited=[('WMT', 'Item 1')] gold=[(None, 'Item 1'), (None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Walmart International total segment square footage increased from 689,647 in fiscal 2016 to 699,289 in fiscal 2017, an increase of 9,642, with square feet reported in thousands. [WMT FY2017, Item 1, WMT_FY2017_2017-01-31:32] [WMT FY2017, Item 1, WMT_FY2017_2017-01-31:47] | None |  |
| The filing does not disclose in the provided evidence blocks the specific geopolitical risk factor cited as a potential driver of negative financial performance for Walmart’s operations in the United Kingdom. | supported | The retrieved evidence mentions the United Kingdom only in operational tables and descriptions and does not disclose any specific geopolitical risk factor tied to negative financial performance there. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 12, cited: 1.

**Generated answer**

> Walmart International total square footage increased from 372,198 thousand square feet in fiscal 2016 to 376,769 thousand square feet in fiscal 2017, an increase of 4,571 thousand square feet. [WMT FY2017, Item 1, WMT_FY2017_2017-01-31:46][WMT FY2017, Item 1, WMT_FY2017_2017-01-31:46]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `WMT_FY2017_2017-01-31:31` | Item 1 › RETAIL UNIT COUNT AND RETAIL SQUARE FEET(1) |  |  | \| \| Supercenters \| \| \| \| \| Discount Stores \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Fiscal Year \| Opened \| Closed \| Conversions(2) \| Total \| Square Feet \| Opened \| Closed \| Conversions(2) \| Total \| Squar… |
| 2 | `WMT_FY2017_2017-01-31:23` | Item 1 › General |  |  | Our operations comprise three reportable segments: Walmart U.S., Walmart International and Sam's Club. Our fiscal year ends on January 31 for our United States ("U.S.") and Canadian operations. We consolidate all other o… |
| 3 | `WMT_FY2017_2017-01-31:47` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | (1) "Unit Count" includes retail stores, wholesale clubs and other, which includes drugstores and convenience stores. Walmart International unit counts, with the exception of Canada, are stated as of December 31, to corr… |
| 4 | `WMT_FY2017_2017-01-31:53` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | Distribution. We utilize a total of 176 distribution facilities located in Argentina, Brazil, Canada, Central America, Chile, China, Japan, Mexico, South Africa and the United Kingdom. Through these facilities, we proces… |
| 5 | `WMT_FY2017_2017-01-31:42` | Item 1 › Walmart International Segment |  |  | The Walmart International segment consists of operations in 27 countries outside of the U.S. and includes numerous formats divided into three major categories: retail, wholesale and other. These categories consist of num… |
| 6 | `WMT_FY2017_2017-01-31:28` | Item 1 › Walmart U.S. Segment |  |  | The Walmart U.S. segment is a mass merchandiser of consumer products, operating under the "Walmart," "Wal-Mart" and "Walmart Neighborhood Market" brands, as well as walmart.com and other digital retail. The Walmart U.S. … |
| 7 | `WMT_FY2017_2017-01-31:44` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | \| \| Africa \| \| Argentina \| \| Brazil \| \| Canada \| \| Central America \| \| Chile \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Fiscal Year \| Unit Count \| Square Feet \| Unit Count \| Square Feet \| Unit Count \| Sq… |
| 8 | `WMT_FY2017_2017-01-31:32` | Item 1 › RETAIL UNIT COUNT AND RETAIL SQUARE FEET(1) |  |  | \| \| Supercenters \| \| \| \| \| Discount Stores \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Fiscal Year \| Opened \| Closed \| Conversions(2) \| Total \| Square Feet \| \| Opened(3) \| Closed \| Total \| Square Feet \| \| B… |
| 9 | `WMT_FY2017_2017-01-31:45` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | \| \| Africa \| \| Argentina \| \| Brazil \| \| Canada \| \| Central America \| \| Chile \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 2017 \| 412 \| 22,542 \| 107 \| 8,264 \| 498 \| 30,642 \| 410 \| 53,088 \| 731 \| 11,770 \| 36… |
| 10 | `WMT_FY2017_2017-01-31:46` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) | ✓ | #1, #2 | \| \| Africa \| \| Argentina \| \| Brazil \| \| Canada \| \| Central America \| \| Chile \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 2015 \| 411 \| 68,269 \| 20 \| 1,083 \| 431 \| 24,429 \| 2,290 \| 98,419 \| 592 \| 36,277 \| 6… |
| 11 | `WMT_FY2017_2017-01-31:48` | Item 1 › UNIT COUNT(1) AND RETAIL SQUARE FEET(2) |  |  | \| Geographic Market \| Retail \| Wholesale \| Other(2) \| Total \| \|---\|---\|---\|---\|---\| \| Africa(3) \| 326 \| 86 \| — \| 412 \| \| Argentina \| 107 \| — \| — \| 107 \| \| Brazil \| 413 \| 71 \| 14 \| 498 \| \| Canada \| 410 \| — \| — \| 410 \| \| C… |
| 12 | `WMT_FY2017_2017-01-31:137` | Item 2 |  |  | \| \| Owned and Operated \| Owned and Third Party Operated \| Leased and Operated \| Third Party Owned and Operated \| Total \| \|---\|---\|---\|---\|---\|---\| \| Canada \| 132 \| — \| 278 \| — \| 410 \| \| Central America \| 267 \| — \| 464 \| … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#10 `WMT_FY2017_2017-01-31:46`** (cited, gold #1, gold #2)

````text
ITEM 1. BUSINESS > UNIT COUNT(1) AND RETAIL SQUARE FEET(2) (table)
|  | Africa |  | Argentina |  | Brazil |  | Canada |  | Central America |  | Chile |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2015 | 411 | 68,269 | 20 | 1,083 | 431 | 24,429 | 2,290 | 98,419 | 592 | 36,277 | 6,290 | 367,630 |
| 2016 | 432 | 71,724 | 21 | 1,146 | 346 | 22,551 | 2,360 | 100,308 | 621 | 37,044 | 6,299 | 372,198 |
| 2017 | 439 | 73,172 | 20 | 1,091 | 341 | 21,921 | 2,411 | 101,681 | 631 | 37,338 | 6,363 | 376,769 |
````

</details>

RQ2 citation match (section level): `cited=[('WMT', 'Item 1')] gold=[(None, 'Item 1'), (None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Walmart International total square footage increased from 372,198 thousand square feet in fiscal 2016 to 376,769 thousand square feet in fiscal 2017, an increase of 4,571 thousand square feet. [WMT FY2017, Item 1, WMT_FY2017_2017-01-31:46][WMT FY2017, Item 1, WMT_FY2017_2017-01-31:46] | None |  |

</details>
