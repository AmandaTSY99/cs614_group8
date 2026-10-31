# gold-039: Table + text (one filing)

[← all cases](../README.md) · company: AMAZON COM INC (AMZN) · fiscal year: 2017 · recipe `table_text` · hop `multi` · answer type `mixed` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> For Amazon.com Inc. in fiscal year 2017, by what percentage did the cost or amortized cost of corporate debt securities increase from 2016 to 2017, and what did the company state was the primary driver for the increase in operating cash flow during 2017?

**Gold answer**

> 102.61%. Amazon said the increase in operating cash flow in 2017 was primarily due to the increase in net income, excluding non-cash charges such as depreciation, amortization, and stock-based compensation.

**Program**: `subtract(4265, 2105), divide(#0, 2105)` → `1.0261282660332542`

**Gold numbers** (RQ2 numeric_accuracy targets): 102.61%

**Key points** (RQ3 keypoint_recall targets)

1. The cost of corporate debt securities rose from $2,105 million (2016) to $4,265 million (2017), an increase of 102.61%.
2. The 2017 operating cash flow increase was primarily due to higher net income.
3. That net income excludes non-cash charges such as depreciation, amortization and stock-based compensation.

**Gold evidence**

1. `AMZN_FY2017_2017-12-31` · Item 8. Financial Statements and Supplementary Data › Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES · table

   > Corporate debt securities | 2,105 | 1 | (2) | 2,104

2. `AMZN_FY2017_2017-12-31` · Item 8. Financial Statements and Supplementary Data › Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES · table

   > Corporate debt securities | 4,265 | 1 | (9) | 4,257

3. `AMZN_FY2017_2017-12-31` · Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations › Liquidity and Capital Resources · text

   > The increase in operating cash flow in 2017, compared to the comparable prior year period, was primarily due to the increase in net income, excluding non-cash charges such as depreciation, amortization, and stock-based compensation.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 10 | 13 |
| recall@5 | 0.33 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.68 | 1.00 | 0.58 | 0.46 |
| gold evidence first rank | #1: 6, #2: 7, #3: 1 | #1: 2, #2: 3, #3: 1 | #1: 2, #2: 3, #3: 4 | #1: 3, #2: 4, #3: 5 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | 1.00 | 1.00 | 0.67 | 0.67 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 1.00 | 1.00 | 1.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 0.50 |
| citation F1 | 1.00 | 1.00 | 1.00 | 0.67 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 2914 | 1652 | 20403 | 17106 |
| cost (USD) | 0.0005 | 0.0003 | 0.0716 | 0.0610 |
| latency (s) | 3.3 | 6.8 | 25.8 | 26.7 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 3.

**Generated answer**

> Amazon’s **cost or amortized cost of corporate debt securities** increased from **$2,105 million in 2016** to **$4,265 million in 2017** [6][7].
>
> Percentage increase:
> \[
> \frac{4,265 - 2,105}{2,105} \times 100 \approx 102.6\%
> \]
>
> So, the cost or amortized cost of corporate debt securities increased by **about 102.6%** [6][7].
>
> Amazon stated that the **primary driver for the increase in operating cash flow in 2017** was **the increase in net income, excluding non-cash charges such as depreciation, amortization, and stock-based compensation** [3].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AMZN_FY2017_2017-12-31:150` | Item 7 › Results of Operations |  | #3 | For 2015, 2016, and 2017, we capitalized $642 million (including $114 million of stock-based compensation), $511 million (including $94 million of stock-based compensation), and $395 million (including $84 million of sto… |
| 2 | `AMZN_FY2017_2017-12-31:172` | Item 7A › Interest Rate Risk |  |  | As of December 31, 2017, we had $24.9 billion of debt, including the current portion, primarily consisting of the following fixed rate unsecured debt (in millions): |
| 3 | `AMZN_FY2017_2017-12-31:123` | Item 7 › Liquidity and Capital Resources | ✓ | #3 | Cash provided by (used in) operating activities was $12.0 billion, $17.3 billion, and $18.4 billion in 2015, 2016, and 2017. Our operating cash flows result primarily from cash received from our consumer, seller, develop… |
| 4 | `AMZN_FY2017_2017-12-31:151` | Item 7 › Results of Operations |  |  | Interest expense was $459 million, $484 million, and $848 million in 2015, 2016, and 2017. The increase is primarily due to increases in our capital and finance lease arrangements and long-term debt. Our long-term debt w… |
| 5 | `AMZN_FY2017_2017-12-31:121` | Item 7 › Liquidity and Capital Resources |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2016 \| 2017 \| \| Cash provided by (used in): \| \| \| \| \| Operating activities \| $12,039 \| $17,272 \| $18,434 \| \| Investing activities \| (6,450) \| (9,876) \| (27,8… |
| 6 | `AMZN_FY2017_2017-12-31:251` | Item 8 › Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES | ✓ | #1 | \| \| December 31, 2016 \| \| \| \| \|---\|---\|---\|---\|---\| \| \| Cost or Amortized Cost \| Gross Unrealized Gains \| Gross Unrealized Losses \| Total Estimated Fair Value \| \| Cash \| $6,883 \| $— \| $— \| $6,883 \| \| Level 1 securities: … |
| 7 | `AMZN_FY2017_2017-12-31:252` | Item 8 › Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES | ✓ | #1, #2 | \| \| December 31, 2017 \| \| \| \| \|---\|---\|---\|---\|---\| \| \| Cost or Amortized Cost \| Gross Unrealized Gains \| Gross Unrealized Losses \| Total Estimated Fair Value \| \| Cash \| $9,982 \| $— \| $— \| $9,982 \| \| Level 1 securities: … |
| 8 | `AMZN_FY2017_2017-12-31:256` | Item 8 › Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES |  |  | \| \| Amortized Cost \| Estimated Fair Value \| \|---\|---\|---\| \| Due within one year \| $17,293 \| $17,287 \| \| Due after one year through five years \| 4,149 \| 4,129 \| \| Due after five years through ten years \| 302 \| 300 \| \| Due… |
| 9 | `AMZN_FY2017_2017-12-31:127` | Item 7 › Liquidity and Capital Resources |  |  | Cash provided by (used in) financing activities was $(3.9) billion, $(3.7) billion, and $9.9 billion in 2015, 2016, and 2017. Cash outflows from financing activities result from principal repayments on obligations relate… |
| 10 | `AMZN_FY2017_2017-12-31:185` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2016 \| 2017 \| \| Principal repayments of finance lease obligations \| (121) \| (147) \| (200) \| \| Net cash provided by (used in) financing activities \| (3,882) \|… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AMZN_FY2017_2017-12-31:150`** (gold #3)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Results of Operations
For 2015, 2016, and 2017, we capitalized $642 million (including $114 million of stock-based compensation), $511 million (including $94 million of stock-based compensation), and $395 million (including $84 million of stock-based compensation) of costs associated with internal-use software and website development. Amortization of previously capitalized amounts was $635 million, $634 million, and $545 million for 2015, 2016, and 2017. General and Administrative The increase in general and administrative costs in absolute dollars in 2016 and 2017, compared to the comparable prior year periods, is primarily due to increases in payroll and related expenses and professional service fees. Other Operating Expense, Net Other operating expense, net was $171 million, $167 million, and $214 million during 2015, 2016, and 2017, and was primarily related to the amortization of intangible assets. Interest Income and Expense Our interest income was $50 million, $100 million, and $202 million during 2015, 2016, and 2017. We generally invest our excess cash in investment grade short- to intermediate-term fixed income securities and AAA-rated money market funds. Our interest income corresponds with the average balance of invested funds based on the prevailing rates, which vary depending on the geographies and currencies in which they are invested.
````

**#3 `AMZN_FY2017_2017-12-31:123`** (cited, gold #3)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Liquidity and Capital Resources
Cash provided by (used in) operating activities was $12.0 billion, $17.3 billion, and $18.4 billion in 2015, 2016, and 2017. Our operating cash flows result primarily from cash received from our consumer, seller, developer, enterprise, and content creator customers, advertising agreements, and our co-branded credit card agreements, offset by cash payments we make for products and services, employee compensation (less amounts capitalized related to internal-use software that are reflected as cash used in investing activities), payment processing and related transaction costs, operating leases, and interest payments on our long-term obligations. Cash received from our customers and other activities generally corresponds to our net sales. Because consumers primarily use credit cards to buy from us, our receivables from consumers settle quickly. The increase in operating cash flow in 2016, compared to the comparable prior year period, was primarily due to the increase in net income, excluding non-cash charges such as depreciation, amortization, and stock-based compensation. The increase in operating cash flow in 2017, compared to the comparable prior year period, was primarily due to the increase in net income, excluding non-cash charges such as depreciation, amortization, and stock-based compensation. Cash provided by (used in) operating activities is also subject to changes
````

**#6 `AMZN_FY2017_2017-12-31:251`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES (table)
|  | December 31, 2016 |  |  |  |
|---|---|---|---|---|
|  | Cost or Amortized Cost | Gross Unrealized Gains | Gross Unrealized Losses | Total Estimated Fair Value |
| Cash | $6,883 | $— | $— | $6,883 |
| Level 1 securities: |  |  |  |  |
| Money market funds | 11,940 | — | — | 11,940 |
| Equity securities | 20 | 31 | — | 51 |
| Level 2 securities: |  |  |  |  |
| Foreign government and agency securities | 337 | — | — | 337 |
| U.S. government and agency securities | 4,821 | 2 | (7) | 4,816 |
| Corporate debt securities | 2,105 | 1 | (2) | 2,104 |
| Asset-backed securities | 355 | — | (2) | 353 |
| Other fixed income securities | 97 | — | — | 97 |
|  | $26,558 | $34 | $(11) | $26,581 |
| Less: Restricted cash, cash equivalents, and marketable securities (1) |  |  |  | (600) |
| Total cash, cash equivalents, and marketable securities |  |  |  | $25,981 |
````

**#7 `AMZN_FY2017_2017-12-31:252`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES (table)
|  | December 31, 2017 |  |  |  |
|---|---|---|---|---|
|  | Cost or Amortized Cost | Gross Unrealized Gains | Gross Unrealized Losses | Total Estimated Fair Value |
| Cash | $9,982 | $— | $— | $9,982 |
| Level 1 securities: |  |  |  |  |
| Money market funds | 11,343 | — | — | 11,343 |
| Equity securities | 23 | 30 | — | 53 |
| Level 2 securities: |  |  |  |  |
| Foreign government and agency securities | 620 | — | — | 620 |
| U.S. government and agency securities | 4,841 | 1 | (19) | 4,823 |
| Corporate debt securities | 4,265 | 1 | (9) | 4,257 |
| Asset-backed securities | 910 | — | (5) | 905 |
| Other fixed income securities | 340 | — | (2) | 338 |
|  | $32,324 | $32 | $(35) | $32,321 |
| Less: Restricted cash, cash equivalents, and marketable securities (1) |  |  |  | (1,335) |
| Total cash, cash equivalents, and marketable securities |  |  |  | $30,986 |
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 7'), ('AMZN', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 3.

**Generated answer**

> The cost or amortized cost of corporate debt securities increased from $2,105 million in 2016 to $4,265 million in 2017. That is an increase of about 102.6% \[((4,265 - 2,105) / 2,105) × 100\]. [2][3]
>
> Amazon stated that the primary driver for the increase in operating cash flow in 2017 was the increase in net income, excluding non-cash charges such as depreciation, amortization, and stock-based compensation. [1]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AMZN_FY2017_2017-12-31:123` | Item 7 › Liquidity and Capital Resources | ✓ | #3 | Cash provided by (used in) operating activities was $12.0 billion, $17.3 billion, and $18.4 billion in 2015, 2016, and 2017. Our operating cash flows result primarily from cash received from our consumer, seller, develop… |
| 2 | `AMZN_FY2017_2017-12-31:251` | Item 8 › Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES | ✓ | #1 | \| \| December 31, 2016 \| \| \| \| \|---\|---\|---\|---\|---\| \| \| Cost or Amortized Cost \| Gross Unrealized Gains \| Gross Unrealized Losses \| Total Estimated Fair Value \| \| Cash \| $6,883 \| $— \| $— \| $6,883 \| \| Level 1 securities: … |
| 3 | `AMZN_FY2017_2017-12-31:252` | Item 8 › Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES | ✓ | #1, #2 | \| \| December 31, 2017 \| \| \| \| \|---\|---\|---\|---\|---\| \| \| Cost or Amortized Cost \| Gross Unrealized Gains \| Gross Unrealized Losses \| Total Estimated Fair Value \| \| Cash \| $9,982 \| $— \| $— \| $9,982 \| \| Level 1 securities: … |
| 4 | `AMZN_FY2017_2017-12-31:151` | Item 7 › Results of Operations |  |  | Interest expense was $459 million, $484 million, and $848 million in 2015, 2016, and 2017. The increase is primarily due to increases in our capital and finance lease arrangements and long-term debt. Our long-term debt w… |
| 5 | `AMZN_FY2017_2017-12-31:141` | Item 7 › Results of Operations |  |  | The increase in AWS operating income in absolute dollars in 2016 and 2017, compared to the comparable prior year periods, is primarily due to increased customer usage and cost structure productivity, partially offset by … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AMZN_FY2017_2017-12-31:123`** (cited, gold #3)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Liquidity and Capital Resources
Cash provided by (used in) operating activities was $12.0 billion, $17.3 billion, and $18.4 billion in 2015, 2016, and 2017. Our operating cash flows result primarily from cash received from our consumer, seller, developer, enterprise, and content creator customers, advertising agreements, and our co-branded credit card agreements, offset by cash payments we make for products and services, employee compensation (less amounts capitalized related to internal-use software that are reflected as cash used in investing activities), payment processing and related transaction costs, operating leases, and interest payments on our long-term obligations. Cash received from our customers and other activities generally corresponds to our net sales. Because consumers primarily use credit cards to buy from us, our receivables from consumers settle quickly. The increase in operating cash flow in 2016, compared to the comparable prior year period, was primarily due to the increase in net income, excluding non-cash charges such as depreciation, amortization, and stock-based compensation. The increase in operating cash flow in 2017, compared to the comparable prior year period, was primarily due to the increase in net income, excluding non-cash charges such as depreciation, amortization, and stock-based compensation. Cash provided by (used in) operating activities is also subject to changes
````

**#2 `AMZN_FY2017_2017-12-31:251`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES (table)
|  | December 31, 2016 |  |  |  |
|---|---|---|---|---|
|  | Cost or Amortized Cost | Gross Unrealized Gains | Gross Unrealized Losses | Total Estimated Fair Value |
| Cash | $6,883 | $— | $— | $6,883 |
| Level 1 securities: |  |  |  |  |
| Money market funds | 11,940 | — | — | 11,940 |
| Equity securities | 20 | 31 | — | 51 |
| Level 2 securities: |  |  |  |  |
| Foreign government and agency securities | 337 | — | — | 337 |
| U.S. government and agency securities | 4,821 | 2 | (7) | 4,816 |
| Corporate debt securities | 2,105 | 1 | (2) | 2,104 |
| Asset-backed securities | 355 | — | (2) | 353 |
| Other fixed income securities | 97 | — | — | 97 |
|  | $26,558 | $34 | $(11) | $26,581 |
| Less: Restricted cash, cash equivalents, and marketable securities (1) |  |  |  | (600) |
| Total cash, cash equivalents, and marketable securities |  |  |  | $25,981 |
````

**#3 `AMZN_FY2017_2017-12-31:252`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES (table)
|  | December 31, 2017 |  |  |  |
|---|---|---|---|---|
|  | Cost or Amortized Cost | Gross Unrealized Gains | Gross Unrealized Losses | Total Estimated Fair Value |
| Cash | $9,982 | $— | $— | $9,982 |
| Level 1 securities: |  |  |  |  |
| Money market funds | 11,343 | — | — | 11,343 |
| Equity securities | 23 | 30 | — | 53 |
| Level 2 securities: |  |  |  |  |
| Foreign government and agency securities | 620 | — | — | 620 |
| U.S. government and agency securities | 4,841 | 1 | (19) | 4,823 |
| Corporate debt securities | 4,265 | 1 | (9) | 4,257 |
| Asset-backed securities | 910 | — | (5) | 905 |
| Other fixed income securities | 340 | — | (2) | 338 |
|  | $32,324 | $32 | $(35) | $32,321 |
| Less: Restricted cash, cash equivalents, and marketable securities (1) |  |  |  | (1,335) |
| Total cash, cash equivalents, and marketable securities |  |  |  | $30,986 |
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 7'), ('AMZN', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 10, cited: 3.

**Generated answer**

> The cost or amortized cost of corporate debt securities increased from $2,105 million in 2016 to $4,265 million in 2017, an increase of approximately 102.6% [AMZN FY2017, Item 8, AMZN_FY2017_2017-12-31:251] [AMZN FY2017, Item 8, AMZN_FY2017_2017-12-31:252].
>
> The company stated that interest income corresponds with the average balance of invested funds based on prevailing rates, which vary depending on the geographies and currencies in which they are invested; the provided evidence does not identify a primary driver for the increase in operating cash flow during 2017. [AMZN FY2017, Item 7, AMZN_FY2017_2017-12-31:150]
>
> > [Guardrail Audit Warning]: Manual verification required; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AMZN_FY2017_2017-12-31:256` | Item 8 › Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES |  |  | \| \| Amortized Cost \| Estimated Fair Value \| \|---\|---\|---\| \| Due within one year \| $17,293 \| $17,287 \| \| Due after one year through five years \| 4,149 \| 4,129 \| \| Due after five years through ten years \| 302 \| 300 \| \| Due… |
| 2 | `AMZN_FY2017_2017-12-31:251` | Item 8 › Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES | ✓ | #1 | \| \| December 31, 2016 \| \| \| \| \|---\|---\|---\|---\|---\| \| \| Cost or Amortized Cost \| Gross Unrealized Gains \| Gross Unrealized Losses \| Total Estimated Fair Value \| \| Cash \| $6,883 \| $— \| $— \| $6,883 \| \| Level 1 securities: … |
| 3 | `AMZN_FY2017_2017-12-31:252` | Item 8 › Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES | ✓ | #1, #2 | \| \| December 31, 2017 \| \| \| \| \|---\|---\|---\|---\|---\| \| \| Cost or Amortized Cost \| Gross Unrealized Gains \| Gross Unrealized Losses \| Total Estimated Fair Value \| \| Cash \| $9,982 \| $— \| $— \| $9,982 \| \| Level 1 securities: … |
| 4 | `AMZN_FY2017_2017-12-31:150` | Item 7 › Results of Operations | ✓ | #3 | For 2015, 2016, and 2017, we capitalized $642 million (including $114 million of stock-based compensation), $511 million (including $94 million of stock-based compensation), and $395 million (including $84 million of sto… |
| 5 | `AMZN_FY2017_2017-12-31:227` | Item 8 › Internal-Use Software and Website Development |  |  | Costs incurred to develop software for internal use and our websites are capitalized and amortized over the estimated useful life of the software. Costs related to design or maintenance of internal-use software and websi… |
| 6 | `AMZN_FY2017_2017-12-31:275` | Item 8 › Intangible Assets |  |  | ___________________ (1) Excludes the original cost and accumulated amortization of fully-amortized intangibles. (2) Intangible assets have estimated useful lives of between one and twenty-five years. Amortization expense… |
| 7 | `AMZN_FY2017_2017-12-31:254` | Item 8 › Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2016 \| 2017 \| \| Realized gains \| $2 \| $3 \| $5 \| \| Realized losses \| 7 \| 11 \| 11 \| |
| 8 | `AMZN_FY2017_2017-12-31:281` | Item 8 › Note 5—LONG-TERM DEBT |  |  | Interest on the Notes issued in 2012 is payable semi-annually in arrears in May and November. Interest on the Notes issued in 2014 is payable semi-annually in arrears in June and December. Interest on the Notes issued in… |
| 9 | `AMZN_FY2017_2017-12-31:280` | Item 8 › Note 5—LONG-TERM DEBT |  |  | _____________________________ (1) Issued in November 2012, effective interest rate of the 2022 Notes were 2.66%. (2) Issued in December 2014, effective interest rates of the 2019, 2021, 2024, 2034, and 2044 Notes were 2.… |
| 10 | `AMZN_FY2017_2017-12-31:170` | Item 7A › Interest Rate Risk |  | #2 | \| \| 2018 \| 2019 \| 2020 \| 2021 \| 2022 \| Thereafter \| Total \| Estimated Fair Value as of December 31, 2017 \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Money market funds \| $11,343 \| $— \| $— \| $— \| $— \| $— \| $11,343 \| $11,343… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `AMZN_FY2017_2017-12-31:251`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES (table)
|  | December 31, 2016 |  |  |  |
|---|---|---|---|---|
|  | Cost or Amortized Cost | Gross Unrealized Gains | Gross Unrealized Losses | Total Estimated Fair Value |
| Cash | $6,883 | $— | $— | $6,883 |
| Level 1 securities: |  |  |  |  |
| Money market funds | 11,940 | — | — | 11,940 |
| Equity securities | 20 | 31 | — | 51 |
| Level 2 securities: |  |  |  |  |
| Foreign government and agency securities | 337 | — | — | 337 |
| U.S. government and agency securities | 4,821 | 2 | (7) | 4,816 |
| Corporate debt securities | 2,105 | 1 | (2) | 2,104 |
| Asset-backed securities | 355 | — | (2) | 353 |
| Other fixed income securities | 97 | — | — | 97 |
|  | $26,558 | $34 | $(11) | $26,581 |
| Less: Restricted cash, cash equivalents, and marketable securities (1) |  |  |  | (600) |
| Total cash, cash equivalents, and marketable securities |  |  |  | $25,981 |
````

**#3 `AMZN_FY2017_2017-12-31:252`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES (table)
|  | December 31, 2017 |  |  |  |
|---|---|---|---|---|
|  | Cost or Amortized Cost | Gross Unrealized Gains | Gross Unrealized Losses | Total Estimated Fair Value |
| Cash | $9,982 | $— | $— | $9,982 |
| Level 1 securities: |  |  |  |  |
| Money market funds | 11,343 | — | — | 11,343 |
| Equity securities | 23 | 30 | — | 53 |
| Level 2 securities: |  |  |  |  |
| Foreign government and agency securities | 620 | — | — | 620 |
| U.S. government and agency securities | 4,841 | 1 | (19) | 4,823 |
| Corporate debt securities | 4,265 | 1 | (9) | 4,257 |
| Asset-backed securities | 910 | — | (5) | 905 |
| Other fixed income securities | 340 | — | (2) | 338 |
|  | $32,324 | $32 | $(35) | $32,321 |
| Less: Restricted cash, cash equivalents, and marketable securities (1) |  |  |  | (1,335) |
| Total cash, cash equivalents, and marketable securities |  |  |  | $30,986 |
````

**#4 `AMZN_FY2017_2017-12-31:150`** (cited, gold #3)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Results of Operations
For 2015, 2016, and 2017, we capitalized $642 million (including $114 million of stock-based compensation), $511 million (including $94 million of stock-based compensation), and $395 million (including $84 million of stock-based compensation) of costs associated with internal-use software and website development. Amortization of previously capitalized amounts was $635 million, $634 million, and $545 million for 2015, 2016, and 2017. General and Administrative The increase in general and administrative costs in absolute dollars in 2016 and 2017, compared to the comparable prior year periods, is primarily due to increases in payroll and related expenses and professional service fees. Other Operating Expense, Net Other operating expense, net was $171 million, $167 million, and $214 million during 2015, 2016, and 2017, and was primarily related to the amortization of intangible assets. Interest Income and Expense Our interest income was $50 million, $100 million, and $202 million during 2015, 2016, and 2017. We generally invest our excess cash in investment grade short- to intermediate-term fixed income securities and AAA-rated money market funds. Our interest income corresponds with the average balance of invested funds based on the prevailing rates, which vary depending on the geographies and currencies in which they are invested.
````

**#10 `AMZN_FY2017_2017-12-31:170`** (gold #2)

````text
Item 7A. Quantitative and Qualitative Disclosures About Market Risk > Interest Rate Risk (table)
|  | 2018 | 2019 | 2020 | 2021 | 2022 | Thereafter | Total | Estimated Fair Value as of December 31, 2017 |
|---|---|---|---|---|---|---|---|---|
| Money market funds | $11,343 | $— | $— | $— | $— | $— | $11,343 | $11,343 |
| Weighted-average interest rate | 0.61% |  |  |  |  |  | 0.61% |  |
| Corporate debt securities | 2,717 | 868 | 484 | 155 | 25 | — | 4,249 | 4,257 |
| Weighted-average interest rate | 1.79% | 2.10% | 2.27% | 2.23% | 2.00% |  | 1.93% |  |
| U.S. government and agency securities | 2,995 | 1,476 | 310 | 54 | 1 | — | 4,836 | 4,823 |
| Weighted-average interest rate | 1.49% | 1.98% | 2.06% | 2.41% | 2.64% |  | 1.69% |  |
| Asset backed securities | 341 | 273 | 262 | 31 | — | — | 907 | 905 |
| Weighted-average interest rate | 1.86% | 2.29% | 2.24% | 2.05% |  |  | 2.11% |  |
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 8'), ('AMZN', 'Item 7')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 1, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| The cost or amortized cost of corporate debt securities increased from $2,105 million in 2016 to $4,265 million in 2017, an increase of approximately 102.6% [AMZN FY2017, Item 8, AMZN_FY2017_2017-12-31:251] [AMZN FY2017, Item 8, AMZN_FY2017_2017-12-31:252]. | None |  |
| The company stated that interest income corresponds with the average balance of invested funds based on prevailing rates, which vary depending on the geographies and currencies in which they are invested; the provided evidence does not identify a primary driver for the increase in operating cash flow during 2017. [AMZN FY2017, Item 7, AMZN_FY2017_2017-12-31:150] | partial | The evidence supports the interest-income statement, but it does not address operating cash flow or its drivers in 2017. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 13, cited: 2.

**Generated answer**

> The cost or amortized cost of corporate debt securities increased from $2,105 million at December 31, 2016 to $4,265 million at December 31, 2017, which is an increase of approximately 102.6% (($4,265 - $2,105) / $2,105) [AMZN FY2017, Item 8, AMZN_FY2017_2017-12-31:251] [AMZN FY2017, Item 8, AMZN_FY2017_2017-12-31:252].  
>
> The filing does not disclose in the provided evidence what the company stated was the primary driver for the increase in operating cash flow during 2017.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-AMZN-2017` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2017,2017-12-31,177866000000,3033000000,4106000000,13131000000… |
| 2 | `AMZN_FY2017_2017-12-31:256` | Item 8 › Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES |  |  | \| \| Amortized Cost \| Estimated Fair Value \| \|---\|---\|---\| \| Due within one year \| $17,293 \| $17,287 \| \| Due after one year through five years \| 4,149 \| 4,129 \| \| Due after five years through ten years \| 302 \| 300 \| \| Due… |
| 3 | `AMZN_FY2017_2017-12-31:251` | Item 8 › Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES | ✓ | #1 | \| \| December 31, 2016 \| \| \| \| \|---\|---\|---\|---\|---\| \| \| Cost or Amortized Cost \| Gross Unrealized Gains \| Gross Unrealized Losses \| Total Estimated Fair Value \| \| Cash \| $6,883 \| $— \| $— \| $6,883 \| \| Level 1 securities: … |
| 4 | `AMZN_FY2017_2017-12-31:252` | Item 8 › Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES | ✓ | #1, #2 | \| \| December 31, 2017 \| \| \| \| \|---\|---\|---\|---\|---\| \| \| Cost or Amortized Cost \| Gross Unrealized Gains \| Gross Unrealized Losses \| Total Estimated Fair Value \| \| Cash \| $9,982 \| $— \| $— \| $9,982 \| \| Level 1 securities: … |
| 5 | `AMZN_FY2017_2017-12-31:150` | Item 7 › Results of Operations |  | #3 | For 2015, 2016, and 2017, we capitalized $642 million (including $114 million of stock-based compensation), $511 million (including $94 million of stock-based compensation), and $395 million (including $84 million of sto… |
| 6 | `AMZN_FY2017_2017-12-31:227` | Item 8 › Internal-Use Software and Website Development |  |  | Costs incurred to develop software for internal use and our websites are capitalized and amortized over the estimated useful life of the software. Costs related to design or maintenance of internal-use software and websi… |
| 7 | `AMZN_FY2017_2017-12-31:275` | Item 8 › Intangible Assets |  |  | ___________________ (1) Excludes the original cost and accumulated amortization of fully-amortized intangibles. (2) Intangible assets have estimated useful lives of between one and twenty-five years. Amortization expense… |
| 8 | `AMZN_FY2017_2017-12-31:254` | Item 8 › Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2016 \| 2017 \| \| Realized gains \| $2 \| $3 \| $5 \| \| Realized losses \| 7 \| 11 \| 11 \| |
| 9 | `AMZN_FY2017_2017-12-31:255` | Item 8 › Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES |  |  | The following table summarizes the contractual maturities of our cash equivalents and marketable fixed-income securities as of December 31, 2017 (in millions): |
| 10 | `AMZN_FY2017_2017-12-31:170` | Item 7A › Interest Rate Risk |  | #2 | \| \| 2018 \| 2019 \| 2020 \| 2021 \| 2022 \| Thereafter \| Total \| Estimated Fair Value as of December 31, 2017 \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Money market funds \| $11,343 \| $— \| $— \| $— \| $— \| $— \| $11,343 \| $11,343… |
| 11 | `AMZN_FY2017_2017-12-31:121` | Item 7 › Liquidity and Capital Resources |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2016 \| 2017 \| \| Cash provided by (used in): \| \| \| \| \| Operating activities \| $12,039 \| $17,272 \| $18,434 \| \| Investing activities \| (6,450) \| (9,876) \| (27,8… |
| 12 | `AMZN_FY2017_2017-12-31:120` | Item 7 › Liquidity and Capital Resources |  |  | Cash flow information, which reflects retrospective adjustments to our consolidated statements of cash flows as described in Item 8 of Part II, “Financial Statements and Supplementary Data — Note 1 — Description of Busin… |
| 13 | `AMZN_FY2017_2017-12-31:127` | Item 7 › Liquidity and Capital Resources |  |  | Cash provided by (used in) financing activities was $(3.9) billion, $(3.7) billion, and $9.9 billion in 2015, 2016, and 2017. Cash outflows from financing activities result from principal repayments on obligations relate… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `AMZN_FY2017_2017-12-31:251`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES (table)
|  | December 31, 2016 |  |  |  |
|---|---|---|---|---|
|  | Cost or Amortized Cost | Gross Unrealized Gains | Gross Unrealized Losses | Total Estimated Fair Value |
| Cash | $6,883 | $— | $— | $6,883 |
| Level 1 securities: |  |  |  |  |
| Money market funds | 11,940 | — | — | 11,940 |
| Equity securities | 20 | 31 | — | 51 |
| Level 2 securities: |  |  |  |  |
| Foreign government and agency securities | 337 | — | — | 337 |
| U.S. government and agency securities | 4,821 | 2 | (7) | 4,816 |
| Corporate debt securities | 2,105 | 1 | (2) | 2,104 |
| Asset-backed securities | 355 | — | (2) | 353 |
| Other fixed income securities | 97 | — | — | 97 |
|  | $26,558 | $34 | $(11) | $26,581 |
| Less: Restricted cash, cash equivalents, and marketable securities (1) |  |  |  | (600) |
| Total cash, cash equivalents, and marketable securities |  |  |  | $25,981 |
````

**#4 `AMZN_FY2017_2017-12-31:252`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES (table)
|  | December 31, 2017 |  |  |  |
|---|---|---|---|---|
|  | Cost or Amortized Cost | Gross Unrealized Gains | Gross Unrealized Losses | Total Estimated Fair Value |
| Cash | $9,982 | $— | $— | $9,982 |
| Level 1 securities: |  |  |  |  |
| Money market funds | 11,343 | — | — | 11,343 |
| Equity securities | 23 | 30 | — | 53 |
| Level 2 securities: |  |  |  |  |
| Foreign government and agency securities | 620 | — | — | 620 |
| U.S. government and agency securities | 4,841 | 1 | (19) | 4,823 |
| Corporate debt securities | 4,265 | 1 | (9) | 4,257 |
| Asset-backed securities | 910 | — | (5) | 905 |
| Other fixed income securities | 340 | — | (2) | 338 |
|  | $32,324 | $32 | $(35) | $32,321 |
| Less: Restricted cash, cash equivalents, and marketable securities (1) |  |  |  | (1,335) |
| Total cash, cash equivalents, and marketable securities |  |  |  | $30,986 |
````

**#5 `AMZN_FY2017_2017-12-31:150`** (gold #3)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Results of Operations
For 2015, 2016, and 2017, we capitalized $642 million (including $114 million of stock-based compensation), $511 million (including $94 million of stock-based compensation), and $395 million (including $84 million of stock-based compensation) of costs associated with internal-use software and website development. Amortization of previously capitalized amounts was $635 million, $634 million, and $545 million for 2015, 2016, and 2017. General and Administrative The increase in general and administrative costs in absolute dollars in 2016 and 2017, compared to the comparable prior year periods, is primarily due to increases in payroll and related expenses and professional service fees. Other Operating Expense, Net Other operating expense, net was $171 million, $167 million, and $214 million during 2015, 2016, and 2017, and was primarily related to the amortization of intangible assets. Interest Income and Expense Our interest income was $50 million, $100 million, and $202 million during 2015, 2016, and 2017. We generally invest our excess cash in investment grade short- to intermediate-term fixed income securities and AAA-rated money market funds. Our interest income corresponds with the average balance of invested funds based on the prevailing rates, which vary depending on the geographies and currencies in which they are invested.
````

**#10 `AMZN_FY2017_2017-12-31:170`** (gold #2)

````text
Item 7A. Quantitative and Qualitative Disclosures About Market Risk > Interest Rate Risk (table)
|  | 2018 | 2019 | 2020 | 2021 | 2022 | Thereafter | Total | Estimated Fair Value as of December 31, 2017 |
|---|---|---|---|---|---|---|---|---|
| Money market funds | $11,343 | $— | $— | $— | $— | $— | $11,343 | $11,343 |
| Weighted-average interest rate | 0.61% |  |  |  |  |  | 0.61% |  |
| Corporate debt securities | 2,717 | 868 | 484 | 155 | 25 | — | 4,249 | 4,257 |
| Weighted-average interest rate | 1.79% | 2.10% | 2.27% | 2.23% | 2.00% |  | 1.93% |  |
| U.S. government and agency securities | 2,995 | 1,476 | 310 | 54 | 1 | — | 4,836 | 4,823 |
| Weighted-average interest rate | 1.49% | 1.98% | 2.06% | 2.41% | 2.64% |  | 1.69% |  |
| Asset backed securities | 341 | 273 | 262 | 31 | — | — | 907 | 905 |
| Weighted-average interest rate | 1.86% | 2.29% | 2.24% | 2.05% |  |  | 2.11% |  |
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| The cost or amortized cost of corporate debt securities increased from $2,105 million at December 31, 2016 to $4,265 million at December 31, 2017, which is an increase of approximately 102.6% (($4,265 - $2,105) / $2,105) [AMZN FY2017, Item 8, AMZN_FY2017_2017-12-31:251] [AMZN FY2017, Item 8, AMZN_FY2017_2017-12-31:252]. | None |  |
| The filing does not disclose in the provided evidence what the company stated was the primary driver for the increase in operating cash flow during 2017. | supported | The retrieved evidence shows operating cash flow amounts but does not state any primary driver for the 2017 increase. |

</details>
