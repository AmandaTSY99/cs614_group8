# gold-045: Single-hop table

[← all cases](../README.md) · company: Tesla, Inc. (TSLA) · fiscal year: 2015 · recipe `table` · hop `single` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> In Tesla, Inc.'s fiscal year 2015 10-K, what percentage of the stock options outstanding as of December 31, 2014 were exercisable?

**Gold answer**

> 55.95%

**Program**: `divide(11957510, 21372960), multiply(#0, 100)` → `55.94690674571983`

**Gold numbers** (RQ2 numeric_accuracy targets): 55.95%

**Gold evidence**

1. `TSLA_FY2015_2015-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Note 10 - Equity Incentive Plans · table

   > | | 21,372,960 | 35.93 | 5.48 | 11,957,510 | 12.37 | 3.63 |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 9 | 9 |
| recall@5 | 0.00 | 0.00 | 0.00 | 0.00 |
| recall@all | 0.00 | 0.00 | 1.00 | 1.00 |
| complete@all | 0 | 0 | 1 | 1 |
| average precision (lexical) | 0.00 | 0.00 | 0.14 | 0.11 |
| gold evidence first rank | #1: – | #1: – | #1: 7 | #1: 9 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✗ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 1.00 | 1.00 |
| citation precision | 1.00 | – | 1.00 | 1.00 |
| citation recall | 1.00 | – | 1.00 | 1.00 |
| citation F1 | 1.00 | – | 1.00 | 1.00 |
| has a citation | 1 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 2858 | 1364 | 12674 | 12481 |
| cost (USD) | 0.0005 | 0.0002 | 0.0456 | 0.0454 |
| latency (s) | 2.9 | 5.9 | 26.6 | 18.1 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> The provided context gives the number of stock options outstanding as of December 31, 2014 as **21,372,960** [3], but it does **not** provide the number of those options that were **exercisable** as of December 31, 2014. Therefore, the percentage cannot be calculated from the provided context.
>
> What is in context:
> - Stock options outstanding at December 31, 2014: **21,372,960** [3]
>
> What is not in context:
> - Stock options exercisable at December 31, 2014, needed to compute the percentage.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2015_2015-12-31:362` | Item 8 › Note 10 - Equity Incentive Plans |  |  | Additional information regarding all stock options outstanding and exercisable as of December 31, 2014 is summarized below: |
| 2 | `TSLA_FY2015_2015-12-31:359` | Item 8 › Note 10 - Equity Incentive Plans |  |  | Additional information regarding all stock options outstanding and exercisable as of December 31, 2015 is summarized below: |
| 3 | `TSLA_FY2015_2015-12-31:358` | Item 8 › Note 10 - Equity Incentive Plans | ✓ |  | \| \| \| Outstanding Stock Options \| \| Outstanding RSUs \| \| \|---\|---\|---\|---\|---\|---\| \| \| \| \| \| \| Weighted \| \| \| \| \| Weighted \| \| Average Grant \| \| \| Shares Available \| Number of \| Average \| Number \| Date Fair \| \| \| for Gra… |
| 4 | `TSLA_FY2015_2015-12-31:367` | Item 8 › Fair Value Adoption |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Risk-free interest rate: \| \| \| \| \| Stock options \| 1.6% \| 1.9% \| 1.3% \| \| ESPP \| 0.3% \| 0.1% \| 0.1% \| \| Expected term (in years): \| \| \| \| \| S… |
| 5 | `TSLA_FY2015_2015-12-31:254` | Item 8 › (in thousands) |  |  | \| \| December 31, \| December 31, \| \|---\|---\|---\| \| \| 2015 \| 2014 \| \| Total current liabilities \| 2,816,274 \| 2,107,166 \| \| Deferred revenue \| 446,105 \| 292,271 \| \| Long-term debt and capital leases \| 2,040,375 \| 1,818,785… |
| 6 | `TSLA_FY2015_2015-12-31:357` | Item 8 › Note 10 - Equity Incentive Plans |  |  | \| \| \| Outstanding Stock Options \| \| Outstanding RSUs \| \| \|---\|---\|---\|---\|---\|---\| \| \| \| \| \| \| Weighted \| \| \| \| \| Weighted \| \| Average Grant \| \| \| Shares Available \| Number of \| Average \| Number \| Date Fair \| \| \| for Gra… |
| 7 | `TSLA_FY2015_2015-12-31:270` | Item 8 › (in thousands) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Maturities of short-term marketable securities \| — \| 189,131 \| — \| \| Business acquisition \| (12,260) \| — \| — \| \| Net cash used in investing a… |
| 8 | `TSLA_FY2015_2015-12-31:0` |  |  |  | 10-K 1 tsla-10k_20151231.htm 10-K |
| 9 | `TSLA_FY2015_2015-12-31:262` | Item 8 › (in thousands, except per share data) |  |  | \| \| \| \| \| \| Accumulated \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Common Stock \| \| Additional \| \| Other \| Total \| \| \| \| \| Paid-In \| Accumulated \| Comprehensive \| Stockholders' \| \| \| Shares \| Amount \| Capital \| Deficit \| Loss… |
| 10 | `TSLA_FY2015_2015-12-31:361` | Item 8 › Note 10 - Equity Incentive Plans |  |  | \| \| Options Outstanding \| \| \| Options Exercisable \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| \| \| Weighted \| \| \| Weighted \| \| \| \| \| Average \| \| \| Average \| \| \| \| Weighted \| Remaining \| \| Weighted \| Remaining \| \| \| \| Average … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `TSLA_FY2015_2015-12-31:358`** (cited)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 10 - Equity Incentive Plans (table)
|  |  | Outstanding Stock Options |  | Outstanding RSUs |  |
|---|---|---|---|---|---|
|  |  |  |  |  | Weighted |
|  |  |  | Weighted |  | Average Grant |
|  | Shares Available | Number of | Average | Number | Date Fair |
|  | for Grant | Options | Exercise Price | of RSUs | Value |
| Cancelled | 556,765 | (433,456) | 56.25 | (123,309) | 187.90 |
| Released | — | — | — | (167,240) | 155.70 |
| Traded for taxes | 6,786 | — | — | — | — |
| Balance, December 31, 2014 | 2,836,084 | 21,372,960 | $35.93 | 1,480,110 | $203.08 |
| Granted | (2,728,110) | 1,102,190 | $243.22 | 1,625,920 | $229.54 |
| Exercised | — | (2,012,646) | 34.32 | — | — |
| Cancelled | 708,797 | (447,324) | 96.70 | (261,473) | 211.66 |
| Released | — | — | — | (404,883) | 233.30 |
| Traded for taxes | 14 | — | — | — |  |
| Balance, December 31, 2015 | 816,785 | 20,015,180 | $46.14 | 2,439,674 | $219.90 |
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
| 1 | `TSLA_FY2015_2015-12-31:365` | Item 8 › Note 10 - Equity Incentive Plans |  |  | The aggregate intrinsic value represents the total pretax intrinsic value (i.e., the difference between our common stock price and the exercise price, multiplied by the number of in-the-money options) that would have bee… |
| 2 | `TSLA_FY2015_2015-12-31:356` | Item 8 › Note 10 - Equity Incentive Plans |  |  | In July 2003, we adopted the 2003 Equity Incentive Plan. Concurrent with the effectiveness of our registration statement on Form S-1 on June 28, 2010, we adopted the 2010 Equity Incentive Plan (the Plan) and all remainin… |
| 3 | `TSLA_FY2015_2015-12-31:358` | Item 8 › Note 10 - Equity Incentive Plans |  |  | \| \| \| Outstanding Stock Options \| \| Outstanding RSUs \| \| \|---\|---\|---\|---\|---\|---\| \| \| \| \| \| \| Weighted \| \| \| \| \| Weighted \| \| Average Grant \| \| \| Shares Available \| Number of \| Average \| Number \| Date Fair \| \| \| for Gra… |
| 4 | `TSLA_FY2015_2015-12-31:362` | Item 8 › Note 10 - Equity Incentive Plans |  |  | Additional information regarding all stock options outstanding and exercisable as of December 31, 2014 is summarized below: |
| 5 | `TSLA_FY2015_2015-12-31:310` | Item 8 › Note 2 - Summary of Significant Accounting Policies |  |  | Our warranty reserves do not include projected warranty costs associated with our vehicles accounted for as operating leases or collateralized debt arrangements. Costs to repair these vehicles are expensed as incurred. F… |

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 9, cited: 1.

**Generated answer**

> As of December 31, 2014, Tesla had 21,372,960 stock options outstanding and 11,957,510 options exercisable, so 55.9% of the stock options outstanding were exercisable [TSLA FY2015, Item 8, TSLA_FY2015_2015-12-31:364].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2015_2015-12-31:362` | Item 8 › Note 10 - Equity Incentive Plans |  |  | Additional information regarding all stock options outstanding and exercisable as of December 31, 2014 is summarized below: |
| 2 | `TSLA_FY2015_2015-12-31:359` | Item 8 › Note 10 - Equity Incentive Plans |  |  | Additional information regarding all stock options outstanding and exercisable as of December 31, 2015 is summarized below: |
| 3 | `TSLA_FY2015_2015-12-31:358` | Item 8 › Note 10 - Equity Incentive Plans |  |  | \| \| \| Outstanding Stock Options \| \| Outstanding RSUs \| \| \|---\|---\|---\|---\|---\|---\| \| \| \| \| \| \| Weighted \| \| \| \| \| Weighted \| \| Average Grant \| \| \| Shares Available \| Number of \| Average \| Number \| Date Fair \| \| \| for Gra… |
| 4 | `TSLA_FY2015_2015-12-31:357` | Item 8 › Note 10 - Equity Incentive Plans |  |  | \| \| \| Outstanding Stock Options \| \| Outstanding RSUs \| \| \|---\|---\|---\|---\|---\|---\| \| \| \| \| \| \| Weighted \| \| \| \| \| Weighted \| \| Average Grant \| \| \| Shares Available \| Number of \| Average \| Number \| Date Fair \| \| \| for Gra… |
| 5 | `TSLA_FY2015_2015-12-31:367` | Item 8 › Fair Value Adoption |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Risk-free interest rate: \| \| \| \| \| Stock options \| 1.6% \| 1.9% \| 1.3% \| \| ESPP \| 0.3% \| 0.1% \| 0.1% \| \| Expected term (in years): \| \| \| \| \| S… |
| 6 | `TSLA_FY2015_2015-12-31:361` | Item 8 › Note 10 - Equity Incentive Plans |  |  | \| \| Options Outstanding \| \| \| Options Exercisable \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| \| \| Weighted \| \| \| Weighted \| \| \| \| \| Average \| \| \| Average \| \| \| \| Weighted \| Remaining \| \| Weighted \| Remaining \| \| \| \| Average … |
| 7 | `TSLA_FY2015_2015-12-31:364` | Item 8 › Note 10 - Equity Incentive Plans | ✓ | #1 | \| \| Options Outstanding \| \| \| Options Exercisable \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| \| \| Weighted \| \| \| Weighted \| \| \| \| \| Average \| \| \| Average \| \| \| \| Weighted \| Remaining \| \| Weighted \| Remaining \| \| \| \| Average … |
| 8 | `TSLA_FY2015_2015-12-31:360` | Item 8 › Note 10 - Equity Incentive Plans |  |  | \| \| Options Outstanding \| \| \| Options Exercisable \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| \| \| Weighted \| \| \| Weighted \| \| \| \| \| Average \| \| \| Average \| \| \| \| Weighted \| Remaining \| \| Weighted \| Remaining \| \| \| \| Average … |
| 9 | `TSLA_FY2015_2015-12-31:363` | Item 8 › Note 10 - Equity Incentive Plans |  |  | \| \| Options Outstanding \| \| \| Options Exercisable \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| \| \| Weighted \| \| \| Weighted \| \| \| \| \| Average \| \| \| Average \| \| \| \| Weighted \| Remaining \| \| Weighted \| Remaining \| \| \| \| Average … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#7 `TSLA_FY2015_2015-12-31:364`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 10 - Equity Incentive Plans (table)
|  | Options Outstanding |  |  | Options Exercisable |  |  |
|---|---|---|---|---|---|---|
|  |  |  | Weighted |  |  | Weighted |
|  |  |  | Average |  |  | Average |
|  |  | Weighted | Remaining |  | Weighted | Remaining |
|  |  | Average | Contractual |  | Average | Contractual |
|  |  | Exercise | Life (in |  | Exercise | Life (in |
| $184.67 - $259.32 | 498,658 | 233.06 |  | 84 | 198.09 |  |
| $259.94 - $259.94 | 72,333 | 259.94 |  | 4,332 | 259.94 |  |
| $282.11 - $282.11 | 25,958 | 282.11 |  | — | — |  |
|  | 21,372,960 | 35.93 | 5.48 | 11,957,510 | 12.37 | 3.63 |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| As of December 31, 2014, Tesla had 21,372,960 stock options outstanding and 11,957,510 options exercisable, so 55.9% of the stock options outstanding were exercisable [TSLA FY2015, Item 8, TSLA_FY2015_2015-12-31:364]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 9, cited: 2.

**Generated answer**

> As of December 31, 2014, Tesla had 21,372,960 stock options outstanding [TSLA FY2015, Item 8, TSLA_FY2015_2015-12-31:358] [TSLA FY2015, Item 8, TSLA_FY2015_2015-12-31:364]. As of December 31, 2014, 11,957,510 of those options were exercisable [TSLA FY2015, Item 8, TSLA_FY2015_2015-12-31:364]. Therefore, 55.9% of the stock options outstanding were exercisable as of December 31, 2014 [TSLA FY2015, Item 8, TSLA_FY2015_2015-12-31:358] [TSLA FY2015, Item 8, TSLA_FY2015_2015-12-31:364].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2015_2015-12-31:362` | Item 8 › Note 10 - Equity Incentive Plans |  |  | Additional information regarding all stock options outstanding and exercisable as of December 31, 2014 is summarized below: |
| 2 | `TSLA_FY2015_2015-12-31:359` | Item 8 › Note 10 - Equity Incentive Plans |  |  | Additional information regarding all stock options outstanding and exercisable as of December 31, 2015 is summarized below: |
| 3 | `TSLA_FY2015_2015-12-31:358` | Item 8 › Note 10 - Equity Incentive Plans | ✓ |  | \| \| \| Outstanding Stock Options \| \| Outstanding RSUs \| \| \|---\|---\|---\|---\|---\|---\| \| \| \| \| \| \| Weighted \| \| \| \| \| Weighted \| \| Average Grant \| \| \| Shares Available \| Number of \| Average \| Number \| Date Fair \| \| \| for Gra… |
| 4 | `TSLA_FY2015_2015-12-31:357` | Item 8 › Note 10 - Equity Incentive Plans |  |  | \| \| \| Outstanding Stock Options \| \| Outstanding RSUs \| \| \|---\|---\|---\|---\|---\|---\| \| \| \| \| \| \| Weighted \| \| \| \| \| Weighted \| \| Average Grant \| \| \| Shares Available \| Number of \| Average \| Number \| Date Fair \| \| \| for Gra… |
| 5 | `TSLA_FY2015_2015-12-31:367` | Item 8 › Fair Value Adoption |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| \| Risk-free interest rate: \| \| \| \| \| Stock options \| 1.6% \| 1.9% \| 1.3% \| \| ESPP \| 0.3% \| 0.1% \| 0.1% \| \| Expected term (in years): \| \| \| \| \| S… |
| 6 | `TSLA_FY2015_2015-12-31:361` | Item 8 › Note 10 - Equity Incentive Plans |  |  | \| \| Options Outstanding \| \| \| Options Exercisable \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| \| \| Weighted \| \| \| Weighted \| \| \| \| \| Average \| \| \| Average \| \| \| \| Weighted \| Remaining \| \| Weighted \| Remaining \| \| \| \| Average … |
| 7 | `TSLA_FY2015_2015-12-31:360` | Item 8 › Note 10 - Equity Incentive Plans |  |  | \| \| Options Outstanding \| \| \| Options Exercisable \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| \| \| Weighted \| \| \| Weighted \| \| \| \| \| Average \| \| \| Average \| \| \| \| Weighted \| Remaining \| \| Weighted \| Remaining \| \| \| \| Average … |
| 8 | `TSLA_FY2015_2015-12-31:363` | Item 8 › Note 10 - Equity Incentive Plans |  |  | \| \| Options Outstanding \| \| \| Options Exercisable \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| \| \| Weighted \| \| \| Weighted \| \| \| \| \| Average \| \| \| Average \| \| \| \| Weighted \| Remaining \| \| Weighted \| Remaining \| \| \| \| Average … |
| 9 | `TSLA_FY2015_2015-12-31:364` | Item 8 › Note 10 - Equity Incentive Plans | ✓ | #1 | \| \| Options Outstanding \| \| \| Options Exercisable \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| \| \| Weighted \| \| \| Weighted \| \| \| \| \| Average \| \| \| Average \| \| \| \| Weighted \| Remaining \| \| Weighted \| Remaining \| \| \| \| Average … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `TSLA_FY2015_2015-12-31:358`** (cited)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 10 - Equity Incentive Plans (table)
|  |  | Outstanding Stock Options |  | Outstanding RSUs |  |
|---|---|---|---|---|---|
|  |  |  |  |  | Weighted |
|  |  |  | Weighted |  | Average Grant |
|  | Shares Available | Number of | Average | Number | Date Fair |
|  | for Grant | Options | Exercise Price | of RSUs | Value |
| Cancelled | 556,765 | (433,456) | 56.25 | (123,309) | 187.90 |
| Released | — | — | — | (167,240) | 155.70 |
| Traded for taxes | 6,786 | — | — | — | — |
| Balance, December 31, 2014 | 2,836,084 | 21,372,960 | $35.93 | 1,480,110 | $203.08 |
| Granted | (2,728,110) | 1,102,190 | $243.22 | 1,625,920 | $229.54 |
| Exercised | — | (2,012,646) | 34.32 | — | — |
| Cancelled | 708,797 | (447,324) | 96.70 | (261,473) | 211.66 |
| Released | — | — | — | (404,883) | 233.30 |
| Traded for taxes | 14 | — | — | — |  |
| Balance, December 31, 2015 | 816,785 | 20,015,180 | $46.14 | 2,439,674 | $219.90 |
````

**#9 `TSLA_FY2015_2015-12-31:364`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 10 - Equity Incentive Plans (table)
|  | Options Outstanding |  |  | Options Exercisable |  |  |
|---|---|---|---|---|---|---|
|  |  |  | Weighted |  |  | Weighted |
|  |  |  | Average |  |  | Average |
|  |  | Weighted | Remaining |  | Weighted | Remaining |
|  |  | Average | Contractual |  | Average | Contractual |
|  |  | Exercise | Life (in |  | Exercise | Life (in |
| $184.67 - $259.32 | 498,658 | 233.06 |  | 84 | 198.09 |  |
| $259.94 - $259.94 | 72,333 | 259.94 |  | 4,332 | 259.94 |  |
| $282.11 - $282.11 | 25,958 | 282.11 |  | — | — |  |
|  | 21,372,960 | 35.93 | 5.48 | 11,957,510 | 12.37 | 3.63 |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| As of December 31, 2014, Tesla had 21,372,960 stock options outstanding [TSLA FY2015, Item 8, TSLA_FY2015_2015-12-31:358] [TSLA FY2015, Item 8, TSLA_FY2015_2015-12-31:364]. | None |  |
| As of December 31, 2014, 11,957,510 of those options were exercisable [TSLA FY2015, Item 8, TSLA_FY2015_2015-12-31:364]. | None |  |
| Therefore, 55.9% of the stock options outstanding were exercisable as of December 31, 2014 [TSLA FY2015, Item 8, TSLA_FY2015_2015-12-31:358] [TSLA FY2015, Item 8, TSLA_FY2015_2015-12-31:364]. | None |  |

</details>
