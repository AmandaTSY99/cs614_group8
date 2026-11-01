# gold-056: Multi-hop text (one filing)

[← all cases](../README.md) · company: Alphabet Inc. (GOOGL) · fiscal year: 2020 · recipe `text` · hop `multi` · answer type `qualitative` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> Regarding Alphabet Inc.'s 2020 financial disclosures, how does the company describe the treatment of unobservable inputs in its fair value measurements for non-marketable investments and Other Bets, and what specific financial impact can performance fee compensation arrangements have on expense recognition timing?

**Gold answer**

> Alphabet states that it maximizes the use of observable inputs and minimizes the use of unobservable inputs, reflecting assumptions that market participants would use. For performance fee compensation arrangements, the company recognizes expense based on estimated payouts, which can result in expense being recognized before the corresponding investment returns are actually realized.

**Key points** (RQ3 keypoint_recall targets)

1. Alphabet minimizes the use of unobservable inputs in fair value measurements.
2. Performance fee compensation expense is recognized based on estimated payouts.
3. This accounting treatment may result in expense being recognized before investment returns are realized.

**Gold evidence**

1. `GOOGL_FY2020_2020-12-31` · ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Fair Value Measurements · text

   > We maximize the use of relevant observable inputs and minimize the use of unobservable inputs.

2. `GOOGL_FY2020_2020-12-31` · ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Fair Value Measurements · text

   > We recognize compensation expense based on the estimated payouts, which may result in expense recognized before investment returns are realized, and may require the use of unobservable inputs.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 12 | 16 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 1.00 | 1.00 | 0.83 | 0.77 |
| gold evidence first rank | #1: 2, #2: 1 | #1: 2, #2: 1 | #1: 1, #2: 2 | #1: 1, #2: 2 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | – | – | – | – |
| keypoint_recall | 1.00 | 1.00 | 1.00 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 0.50 | 0.33 | 0.50 | 0.50 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 0.67 | 0.50 | 0.67 | 0.67 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 2114 | 1296 | 16534 | 18175 |
| cost (USD) | 0.0004 | 0.0003 | 0.0655 | 0.0700 |
| latency (s) | 7.0 | 8.0 | 31.7 | 32.9 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 3.

**Generated answer**

> Alphabet says that for fair value measurements of certain non-marketable equity and debt investments, certain stock-based compensation awards settled in the stock of certain Other Bets, and some business-combination assets and liabilities, it tries to maximize observable inputs and minimize unobservable inputs. When unobservable inputs are used, they reflect assumptions market participants would use and may include Alphabet’s own data adjusted based on reasonably available information; management also applies judgment when observable market data is limited or absent [2]. Alphabet also notes that the equity values of certain Other Bets used for some stock-based compensation awards require the use of unobservable inputs [1].
>
> For performance fee compensation arrangements, Alphabet says these payouts are based on realized investment returns, but it recognizes compensation expense based on estimated payouts. As a result, expense may be recognized before the investment returns are actually realized [1][3].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2020_2020-12-31:249` | Item 7 › Fair Value Measurements | ✓ | #2 | In determining the fair values of our non-marketable equity and debt investments, as well as assets acquired (especially with respect to intangible assets) and liabilities assumed in business combinations, we make signif… |
| 2 | `GOOGL_FY2020_2020-12-31:248` | Item 7 › Fair Value Measurements | ✓ | #1 | We measure certain of our non-marketable equity and debt investments, certain other instruments including stock-based compensation awards settled in the stock of certain Other Bets, and certain assets and liabilities acq… |
| 3 | `GOOGL_FY2020_2020-12-31:312` | Item 8 › Performance Fees | ✓ | #2 | Performance fees refer to compensation arrangements with payouts based on realized investment returns. We recognize compensation expense based on the estimated payouts, which may result in expense recognized before inves… |
| 4 | `GOOGL_FY2020_2020-12-31:264` | Item 7A › Equity Investment Risk |  |  | companies are inherently more complex due to the lack of readily available market data. Volatility in the global economic climate and financial markets could result in a significant impairment charge relating to our non-… |
| 5 | `GOOGL_FY2020_2020-12-31:123` | Item 1A › If we were to lose the services of key personnel, we may not be able to execute our business strategy. |  |  | We are exposed to fluctuations in the market values of our investments and, in some instances, our financial statements incorporate valuation methodologies that are subjective in nature resulting in fluctuations over tim… |
| 6 | `GOOGL_FY2020_2020-12-31:325` | Item 8 › Impairment of Investments |  |  | For non-marketable equity securities we consider whether impairment indicators exist by evaluating the companies' financial and liquidity position, access to capital resources and the time since the last adjustment to fa… |
| 7 | `GOOGL_FY2020_2020-12-31:350` | Item 8 › Debt Securities |  |  | Table of Contents Alphabet Inc. The following tables present fair values and gross unrealized losses recorded to AOCI as of December 31, 2019 and 2020, aggregated by investment category and the length of time that indivi… |
| 8 | `GOOGL_FY2020_2020-12-31:263` | Item 7A › Equity Investment Risk |  |  | Our non-marketable equity securities not accounted for under the equity method are adjusted to fair value for observable transactions for identical or similar investments of the same issuer or impairment (referred to as … |
| 9 | `GOOGL_FY2020_2020-12-31:464` | Item 8 › Stock-Based Award Activities |  |  | \| \| Unvested Restricted Stock Units \| \| \|---\|---\|---\| \| \| Number of Shares \| Weighted- Average Grant-Date Fair Value \| \| Unvested as of December 31, 2019 \| 19,394,236 \| $1,055.22 \| \| Granted \| 12,647,562 \| 1,407.97 \| \| V… |
| 10 | `GOOGL_FY2020_2020-12-31:319` | Item 8 › Cash, Cash Equivalents, and Marketable Securities |  |  | Our investments in marketable equity securities are measured at fair value with the related gains and losses, realized and unrealized, recognized in other income (expense), net. |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2020_2020-12-31:249`** (cited, gold #2)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Fair Value Measurements
In determining the fair values of our non-marketable equity and debt investments, as well as assets acquired (especially with respect to intangible assets) and liabilities assumed in business combinations, we make significant estimates and assumptions, some of which include the use of unobservable inputs. Certain stock-based compensation awards may be settled in the stock of certain of our Other Bets or in cash. These awards are based on the equity values of the respective Other Bet, which requires use of unobservable inputs. We also have compensation arrangements with payouts based on realized investment returns, i.e. performance fees. We recognize compensation expense based on the estimated payouts, which may result in expense recognized before investment returns are realized, and may require the use of unobservable inputs.
````

**#2 `GOOGL_FY2020_2020-12-31:248`** (cited, gold #1)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Fair Value Measurements
We measure certain of our non-marketable equity and debt investments, certain other instruments including stock-based compensation awards settled in the stock of certain Other Bets, and certain assets and liabilities acquired in a business combination, at fair value on a nonrecurring basis. The determination of fair value involves the use of appropriate valuation methods and relevant inputs into valuation models. The fair value hierarchy prioritizes the inputs used to measure fair value whereby it gives the highest priority to quoted prices (unadjusted) in active markets for identical assets or liabilities and the lowest priority to unobservable inputs. We maximize the use of relevant observable inputs and minimize the use of unobservable inputs. Our use of unobservable inputs reflects the assumptions that market participants would use and may include our own data adjusted based on reasonably available information. We apply judgment in assessing the relevance of observable market data to determine the priority of inputs under the fair value hierarchy, particularly in situations where there is very little or no market activity. Table of Contents Alphabet Inc.
````

**#3 `GOOGL_FY2020_2020-12-31:312`** (cited, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Performance Fees
Performance fees refer to compensation arrangements with payouts based on realized investment returns. We recognize compensation expense based on the estimated payouts, which may result in expense recognized before investment returns are realized. Performance fees, which are primarily related to gains on equity securities, are recorded as a component of other income (expense), net.
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 7'), ('GOOGL', 'Item 8')] gold=[(None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 4.

**Generated answer**

> Alphabet says its fair value measurements for certain non-marketable equity and debt investments and certain stock-based compensation awards tied to Other Bets may require the use of unobservable inputs. It states that the fair value hierarchy gives the lowest priority to unobservable inputs, that it seeks to maximize observable inputs and minimize unobservable ones, and that its use of unobservable inputs reflects assumptions market participants would use, sometimes including Alphabet’s own adjusted data and management judgment where market activity is limited [1][2][5].
>
> For performance fee compensation arrangements, Alphabet says these payouts are based on realized investment returns, but it recognizes compensation expense based on estimated payouts. As a result, expense may be recognized before the investment returns are actually realized [1][3].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2020_2020-12-31:249` | Item 7 › Fair Value Measurements | ✓ | #2 | In determining the fair values of our non-marketable equity and debt investments, as well as assets acquired (especially with respect to intangible assets) and liabilities assumed in business combinations, we make signif… |
| 2 | `GOOGL_FY2020_2020-12-31:248` | Item 7 › Fair Value Measurements | ✓ | #1 | We measure certain of our non-marketable equity and debt investments, certain other instruments including stock-based compensation awards settled in the stock of certain Other Bets, and certain assets and liabilities acq… |
| 3 | `GOOGL_FY2020_2020-12-31:312` | Item 8 › Performance Fees | ✓ | #2 | Performance fees refer to compensation arrangements with payouts based on realized investment returns. We recognize compensation expense based on the estimated payouts, which may result in expense recognized before inves… |
| 4 | `GOOGL_FY2020_2020-12-31:344` | Item 8 › Deferred Revenues and Remaining Performance Obligations |  |  | Additionally, we have performance obligations associated with commitments in customer contracts, primarily related to Google Cloud, for future services that have not yet been recognized as revenues, also referred to as r… |
| 5 | `GOOGL_FY2020_2020-12-31:123` | Item 1A › If we were to lose the services of key personnel, we may not be able to execute our business strategy. | ✓ |  | We are exposed to fluctuations in the market values of our investments and, in some instances, our financial statements incorporate valuation methodologies that are subjective in nature resulting in fluctuations over tim… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2020_2020-12-31:249`** (cited, gold #2)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Fair Value Measurements
In determining the fair values of our non-marketable equity and debt investments, as well as assets acquired (especially with respect to intangible assets) and liabilities assumed in business combinations, we make significant estimates and assumptions, some of which include the use of unobservable inputs. Certain stock-based compensation awards may be settled in the stock of certain of our Other Bets or in cash. These awards are based on the equity values of the respective Other Bet, which requires use of unobservable inputs. We also have compensation arrangements with payouts based on realized investment returns, i.e. performance fees. We recognize compensation expense based on the estimated payouts, which may result in expense recognized before investment returns are realized, and may require the use of unobservable inputs.
````

**#2 `GOOGL_FY2020_2020-12-31:248`** (cited, gold #1)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Fair Value Measurements
We measure certain of our non-marketable equity and debt investments, certain other instruments including stock-based compensation awards settled in the stock of certain Other Bets, and certain assets and liabilities acquired in a business combination, at fair value on a nonrecurring basis. The determination of fair value involves the use of appropriate valuation methods and relevant inputs into valuation models. The fair value hierarchy prioritizes the inputs used to measure fair value whereby it gives the highest priority to quoted prices (unadjusted) in active markets for identical assets or liabilities and the lowest priority to unobservable inputs. We maximize the use of relevant observable inputs and minimize the use of unobservable inputs. Our use of unobservable inputs reflects the assumptions that market participants would use and may include our own data adjusted based on reasonably available information. We apply judgment in assessing the relevance of observable market data to determine the priority of inputs under the fair value hierarchy, particularly in situations where there is very little or no market activity. Table of Contents Alphabet Inc.
````

**#3 `GOOGL_FY2020_2020-12-31:312`** (cited, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Performance Fees
Performance fees refer to compensation arrangements with payouts based on realized investment returns. We recognize compensation expense based on the estimated payouts, which may result in expense recognized before investment returns are realized. Performance fees, which are primarily related to gains on equity securities, are recorded as a component of other income (expense), net.
````

**#5 `GOOGL_FY2020_2020-12-31:123`** (cited)

````text
ITEM 1A.RISK FACTORS > If we were to lose the services of key personnel, we may not be able to execute our business strategy.
We are exposed to fluctuations in the market values of our investments and, in some instances, our financial statements incorporate valuation methodologies that are subjective in nature resulting in fluctuations over time. The market value of our investments can be negatively affected by liquidity, credit deterioration or losses, performance and financial results of the underlying entities, foreign exchange rates, changes in interest rates, including changes that may result from the implementation of new benchmark rates, the effect of new or changing regulations, the stock market in general, or other factors. The effect of COVID-19 on our impairment assessment for non-marketable investments requires significant judgment due to the uncertainty around the duration and severity of the impact. We measure certain of our non-marketable equity and debt investments, certain other instruments including stock-based compensation awards settled in the stock of certain Other Bets, and certain assets and liabilities acquired in a business combination, at fair value on a nonrecurring basis. The determination of fair value involves use of appropriate valuation methods and certain unobservable inputs, require management judgment and estimation, and may change over time.
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 7'), ('GOOGL', 'Item 8'), ('GOOGL', 'Item 1A')] gold=[(None, 'Item 7')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 12, cited: 6.

**Generated answer**

> Alphabet states that the determination of fair value for certain non-marketable equity and debt investments, certain instruments including stock-based compensation awards settled in the stock of certain Other Bets, and certain assets and liabilities acquired in a business combination involves appropriate valuation methods and relevant inputs, and that the fair value hierarchy gives the lowest priority to unobservable inputs. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:248]
>
> Alphabet says it maximizes the use of relevant observable inputs and minimizes the use of unobservable inputs, and that its use of unobservable inputs reflects assumptions that market participants would use and may include Alphabet’s own data adjusted based on reasonably available information. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:248]
>
> The company also says that, in determining the fair values of non-marketable equity and debt investments, assets acquired and liabilities assumed in business combinations, and certain Other Bet stock-based compensation awards, it makes significant estimates and assumptions, some of which include the use of unobservable inputs. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:249]
>
> For Other Bets specifically, Alphabet discloses that certain stock-based compensation awards may be settled in the stock of certain Other Bets or in cash, and that these awards are based on the equity values of the respective Other Bet, which requires use of unobservable inputs. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:249]
>
> Alphabet further describes Level 3 fair value inputs as unobservable inputs that are supported by little or no market activities, and says the fair value hierarchy requires an entity to maximize observable inputs and minimize unobservable inputs when measuring fair value. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:316]
>
> For non-marketable investments not accounted for under the equity method, Alphabet says they are primarily accounted for under the measurement alternative, under which carrying value is adjusted to fair value for observable transactions for identical or similar investments of the same issuer or impairment. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:323]
>
> Alphabet also notes that recording upward and downward adjustments to the carrying value of non-marketable equity securities as a result of observable price changes requires quantitative assessments using various valuation methodologies and involves the use of estimates. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:250]
>
> Regarding performance fee compensation arrangements, Alphabet says these payouts are based on realized investment returns and that it recognizes compensation expense based on estimated payouts, which may result in expense being recognized before investment returns are realized. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:249] [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:312]
>
> Alphabet also states that performance fees are primarily related to gains on equity securities and are recorded as a component of other income (expense), net. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:312]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2020_2020-12-31:248` | Item 7 › Fair Value Measurements | ✓ | #1 | We measure certain of our non-marketable equity and debt investments, certain other instruments including stock-based compensation awards settled in the stock of certain Other Bets, and certain assets and liabilities acq… |
| 2 | `GOOGL_FY2020_2020-12-31:249` | Item 7 › Fair Value Measurements | ✓ | #2 | In determining the fair values of our non-marketable equity and debt investments, as well as assets acquired (especially with respect to intangible assets) and liabilities assumed in business combinations, we make signif… |
| 3 | `GOOGL_FY2020_2020-12-31:263` | Item 7A › Equity Investment Risk |  |  | Our non-marketable equity securities not accounted for under the equity method are adjusted to fair value for observable transactions for identical or similar investments of the same issuer or impairment (referred to as … |
| 4 | `GOOGL_FY2020_2020-12-31:316` | Item 8 › Fair Value of Financial Instruments | ✓ | #1 | Level 2 - Inputs that are based upon quoted prices for similar instruments in active markets, quoted prices for identical or similar instruments in markets that are not active, and model-based valuation techniques for wh… |
| 5 | `GOOGL_FY2020_2020-12-31:315` | Item 8 › Fair Value of Financial Instruments |  |  | Our financial assets and liabilities that are measured at fair value on a recurring basis include cash equivalents, marketable securities, derivative contracts, and non-marketable debt securities. Our financial assets me… |
| 6 | `GOOGL_FY2020_2020-12-31:250` | Item 7 › Non-marketable Equity Securities | ✓ |  | Our non-marketable equity securities not accounted for under the equity method are carried either at fair value or under the measurement alternative. Under the measurement alternative, the carrying value is measured at c… |
| 7 | `GOOGL_FY2020_2020-12-31:312` | Item 8 › Performance Fees | ✓ | #2 | Performance fees refer to compensation arrangements with payouts based on realized investment returns. We recognize compensation expense based on the estimated payouts, which may result in expense recognized before inves… |
| 8 | `GOOGL_FY2020_2020-12-31:462` | Item 8 › Stock-Based Compensation |  |  | For the years ended December 31, 2018, 2019 and 2020, total stock-based compensation expense was $10.0 billion, $11.7 billion and $13.4 billion, including amounts associated with awards we expect to settle in Alphabet st… |
| 9 | `GOOGL_FY2020_2020-12-31:310` | Item 8 › Stock-based Compensation |  |  | Stock-based compensation primarily consists of Alphabet restricted stock units ("RSUs"). RSUs are equity classified and measured at the fair market value of the underlying stock at the grant date. We recognize RSU expens… |
| 10 | `GOOGL_FY2020_2020-12-31:123` | Item 1A › If we were to lose the services of key personnel, we may not be able to execute our business strategy. |  |  | We are exposed to fluctuations in the market values of our investments and, in some instances, our financial statements incorporate valuation methodologies that are subjective in nature resulting in fluctuations over tim… |
| 11 | `GOOGL_FY2020_2020-12-31:323` | Item 8 › Non-Marketable Investments | ✓ |  | We account for non-marketable equity investments through which we exercise significant influence but do not have control over the investee under the equity method. Our non-marketable equity securities not accounted for u… |
| 12 | `GOOGL_FY2020_2020-12-31:464` | Item 8 › Stock-Based Award Activities |  |  | \| \| Unvested Restricted Stock Units \| \| \|---\|---\|---\| \| \| Number of Shares \| Weighted- Average Grant-Date Fair Value \| \| Unvested as of December 31, 2019 \| 19,394,236 \| $1,055.22 \| \| Granted \| 12,647,562 \| 1,407.97 \| \| V… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2020_2020-12-31:248`** (cited, gold #1)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Fair Value Measurements
We measure certain of our non-marketable equity and debt investments, certain other instruments including stock-based compensation awards settled in the stock of certain Other Bets, and certain assets and liabilities acquired in a business combination, at fair value on a nonrecurring basis. The determination of fair value involves the use of appropriate valuation methods and relevant inputs into valuation models. The fair value hierarchy prioritizes the inputs used to measure fair value whereby it gives the highest priority to quoted prices (unadjusted) in active markets for identical assets or liabilities and the lowest priority to unobservable inputs. We maximize the use of relevant observable inputs and minimize the use of unobservable inputs. Our use of unobservable inputs reflects the assumptions that market participants would use and may include our own data adjusted based on reasonably available information. We apply judgment in assessing the relevance of observable market data to determine the priority of inputs under the fair value hierarchy, particularly in situations where there is very little or no market activity. Table of Contents Alphabet Inc.
````

**#2 `GOOGL_FY2020_2020-12-31:249`** (cited, gold #2)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Fair Value Measurements
In determining the fair values of our non-marketable equity and debt investments, as well as assets acquired (especially with respect to intangible assets) and liabilities assumed in business combinations, we make significant estimates and assumptions, some of which include the use of unobservable inputs. Certain stock-based compensation awards may be settled in the stock of certain of our Other Bets or in cash. These awards are based on the equity values of the respective Other Bet, which requires use of unobservable inputs. We also have compensation arrangements with payouts based on realized investment returns, i.e. performance fees. We recognize compensation expense based on the estimated payouts, which may result in expense recognized before investment returns are realized, and may require the use of unobservable inputs.
````

**#4 `GOOGL_FY2020_2020-12-31:316`** (cited, gold #1)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Fair Value of Financial Instruments
Level 2 - Inputs that are based upon quoted prices for similar instruments in active markets, quoted prices for identical or similar instruments in markets that are not active, and model-based valuation techniques for which all significant inputs are observable in the market or can be derived from observable market data. Where applicable, these models project future cash flows and discount the future amounts to a present value using market-based observable inputs including interest rate curves, foreign exchange rates, and credit ratings. Level 3 - Unobservable inputs that are supported by little or no market activities. The fair value hierarchy requires an entity to maximize the use of observable inputs and minimize the use of unobservable inputs when measuring fair value.
````

**#6 `GOOGL_FY2020_2020-12-31:250`** (cited)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Non-marketable Equity Securities
Our non-marketable equity securities not accounted for under the equity method are carried either at fair value or under the measurement alternative. Under the measurement alternative, the carrying value is measured at cost, less any impairment, plus or minus changes resulting from observable price changes in orderly transactions for the identical or a similar investment of the same issuer. Determining whether an observed transaction is similar to a security within our portfolio requires judgment based on the rights and obligations of the securities. Recording upward and downward adjustments to the carrying value of our equity securities as a result of observable price changes requires quantitative assessments of the fair value of our securities using various valuation methodologies and involves the use of estimates.
````

**#7 `GOOGL_FY2020_2020-12-31:312`** (cited, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Performance Fees
Performance fees refer to compensation arrangements with payouts based on realized investment returns. We recognize compensation expense based on the estimated payouts, which may result in expense recognized before investment returns are realized. Performance fees, which are primarily related to gains on equity securities, are recorded as a component of other income (expense), net.
````

**#11 `GOOGL_FY2020_2020-12-31:323`** (cited)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Non-Marketable Investments
We account for non-marketable equity investments through which we exercise significant influence but do not have control over the investee under the equity method. Our non-marketable equity securities not accounted for under the equity method are primarily accounted for under the measurement alternative. Under the measurement alternative, the carrying value of our non-marketable equity investments is adjusted to fair value for observable transactions for identical or similar investments of the same issuer or impairment. Adjustments are determined primarily based on a market approach as of the transaction date and are recorded as a component of other income (expense), net. Non-marketable debt investments are classified as available-for-sale securities. Non-marketable investments that do not have stated contractual maturity dates are classified as non-current assets on the Consolidated Balance Sheets.
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 7'), ('GOOGL', 'Item 8')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 9, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Alphabet states that the determination of fair value for certain non-marketable equity and debt investments, certain instruments including stock-based compensation awards settled in the stock of certain Other Bets, and certain assets and liabilities acquired in a business combination involves appropriate valuation methods and relevant inputs, and that the fair value hierarchy gives the lowest priority to unobservable inputs. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:248] | supported | The evidence states all listed instruments, says fair value determination uses appropriate valuation methods and relevant inputs, and that the hierarchy gives lowest priority to unobservable inputs. |
| Alphabet says it maximizes the use of relevant observable inputs and minimizes the use of unobservable inputs, and that its use of unobservable inputs reflects assumptions that market participants would use and may include Alphabet’s own data adjusted based on reasonably available information. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:248] | supported | The cited passage explicitly says Alphabet maximizes observable inputs, minimizes unobservable inputs, and that unobservable inputs reflect market participant assumptions and may include adjusted company data. |
| The company also says that, in determining the fair values of non-marketable equity and debt investments, assets acquired and liabilities assumed in business combinations, and certain Other Bet stock-based compensation awards, it makes significant estimates and assumptions, some of which include the use of unobservable inputs. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:249] | supported | The evidence says these fair value determinations involve significant estimates and assumptions, including unobservable inputs, and separately says certain Other Bets stock awards require unobservable inputs. |
| For Other Bets specifically, Alphabet discloses that certain stock-based compensation awards may be settled in the stock of certain Other Bets or in cash, and that these awards are based on the equity values of the respective Other Bet, which requires use of unobservable inputs. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:249] | supported | The cited text directly states those awards may be settled in Other Bets stock or cash and are based on the Other Bet’s equity values requiring unobservable inputs. |
| Alphabet further describes Level 3 fair value inputs as unobservable inputs that are supported by little or no market activities, and says the fair value hierarchy requires an entity to maximize observable inputs and minimize unobservable inputs when measuring fair value. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:316] | supported | The evidence explicitly defines Level 3 as unobservable inputs supported by little or no market activities and states the hierarchy requires maximizing observable and minimizing unobservable inputs. |
| For non-marketable investments not accounted for under the equity method, Alphabet says they are primarily accounted for under the measurement alternative, under which carrying value is adjusted to fair value for observable transactions for identical or similar investments of the same issuer or impairment. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:323] | supported | The passage states such investments are primarily under the measurement alternative and that carrying value is adjusted to fair value for observable transactions for identical or similar investments of the same issuer or impairment. |
| Alphabet also notes that recording upward and downward adjustments to the carrying value of non-marketable equity securities as a result of observable price changes requires quantitative assessments using various valuation methodologies and involves the use of estimates. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:250] | supported | The evidence expressly says recording upward and downward adjustments from observable price changes requires quantitative fair value assessments using various valuation methodologies and estimates. |
| Regarding performance fee compensation arrangements, Alphabet says these payouts are based on realized investment returns and that it recognizes compensation expense based on estimated payouts, which may result in expense being recognized before investment returns are realized. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:249] [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:312] | supported | Both cited passages state that performance fee payouts are based on realized investment returns and that compensation expense is recognized based on estimated payouts before returns are realized. |
| Alphabet also states that performance fees are primarily related to gains on equity securities and are recorded as a component of other income (expense), net. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:312] | supported | The cited evidence explicitly says performance fees are primarily related to gains on equity securities and are recorded in other income (expense), net. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 16, cited: 6.

**Generated answer**

> Alphabet states that in determining the fair values of its non-marketable equity and debt investments, assets acquired and liabilities assumed in business combinations, and certain stock-based compensation awards settled in the stock of certain Other Bets, it makes significant estimates and assumptions, some of which include the use of unobservable inputs. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:249]
>
> The company says its use of unobservable inputs reflects assumptions that market participants would use and may include Alphabet’s own data adjusted based on reasonably available information. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:248]
>
> Alphabet also says it maximizes the use of relevant observable inputs and minimizes the use of unobservable inputs when measuring fair value, and that Level 3 inputs are unobservable inputs supported by little or no market activities. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:248] [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:316]
>
> For non-marketable equity securities under the measurement alternative, Alphabet says carrying value is measured at cost, less any impairment, plus or minus changes from observable price changes in orderly transactions for the identical or a similar investment of the same issuer, and that determining similarity of observed transactions and recording upward and downward adjustments requires judgment, quantitative assessments, various valuation methodologies, and the use of estimates. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:250]
>
> For certain Other Bets awards, Alphabet says these awards are based on the equity values of the respective Other Bet, which requires use of unobservable inputs. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:249]
>
> Regarding performance fee compensation arrangements, Alphabet says these payouts are based on realized investment returns and that it recognizes compensation expense based on estimated payouts, which may result in expense being recognized before investment returns are realized. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:249] [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:312]
>
> Alphabet further discloses that performance fees are recorded as a component of other income (expense), net. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:312]
>
> In 2020, performance fees were $(609) million. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:422]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2020_2020-12-31:248` | Item 7 › Fair Value Measurements | ✓ | #1 | We measure certain of our non-marketable equity and debt investments, certain other instruments including stock-based compensation awards settled in the stock of certain Other Bets, and certain assets and liabilities acq… |
| 2 | `GOOGL_FY2020_2020-12-31:249` | Item 7 › Fair Value Measurements | ✓ | #2 | In determining the fair values of our non-marketable equity and debt investments, as well as assets acquired (especially with respect to intangible assets) and liabilities assumed in business combinations, we make signif… |
| 3 | `GOOGL_FY2020_2020-12-31:263` | Item 7A › Equity Investment Risk |  |  | Our non-marketable equity securities not accounted for under the equity method are adjusted to fair value for observable transactions for identical or similar investments of the same issuer or impairment (referred to as … |
| 4 | `GOOGL_FY2020_2020-12-31:316` | Item 8 › Fair Value of Financial Instruments | ✓ | #1 | Level 2 - Inputs that are based upon quoted prices for similar instruments in active markets, quoted prices for identical or similar instruments in markets that are not active, and model-based valuation techniques for wh… |
| 5 | `GOOGL_FY2020_2020-12-31:315` | Item 8 › Fair Value of Financial Instruments |  |  | Our financial assets and liabilities that are measured at fair value on a recurring basis include cash equivalents, marketable securities, derivative contracts, and non-marketable debt securities. Our financial assets me… |
| 6 | `GOOGL_FY2020_2020-12-31:250` | Item 7 › Non-marketable Equity Securities | ✓ |  | Our non-marketable equity securities not accounted for under the equity method are carried either at fair value or under the measurement alternative. Under the measurement alternative, the carrying value is measured at c… |
| 7 | `GOOGL_FY2020_2020-12-31:464` | Item 8 › Stock-Based Award Activities |  |  | \| \| Unvested Restricted Stock Units \| \| \|---\|---\|---\| \| \| Number of Shares \| Weighted- Average Grant-Date Fair Value \| \| Unvested as of December 31, 2019 \| 19,394,236 \| $1,055.22 \| \| Granted \| 12,647,562 \| 1,407.97 \| \| V… |
| 8 | `GOOGL_FY2020_2020-12-31:407` | Item 8 › Long-Term Debt |  |  | (1)Net of imputed interest. (2)Total current portion of long-term debt is included within other accrued expenses and current liabilities. See Note 7. The notes in the table above are comprised of fixed-rate senior unsecu… |
| 9 | `GOOGL_FY2020_2020-12-31:350` | Item 8 › Debt Securities |  |  | Table of Contents Alphabet Inc. The following tables present fair values and gross unrealized losses recorded to AOCI as of December 31, 2019 and 2020, aggregated by investment category and the length of time that indivi… |
| 10 | `GOOGL_FY2020_2020-12-31:347` | Item 8 › Debt Securities |  |  | \| \| As of December 31, 2020 \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Adjusted Cost \| Gross Unrealized Gains \| Gross Unrealized Losses \| Fair Value \| Cash and Cash Equivalents \| Marketable Securities \| \| Level 2: \| \|… |
| 11 | `GOOGL_FY2020_2020-12-31:280` | Item 8 › (In millions, except share amounts which are reflected in thousands, and par value per share amounts) |  |  | \| \| As of December 31, 2019 \| As of December 31, 2020 \| \|---\|---\|---\| \| Accrued compensation and benefits \| 8,495 \| 11,086 \| \| Accrued expenses and other current liabilities \| 23,067 \| 28,631 \| \| Accrued revenue share \| … |
| 12 | `GOOGL_FY2020_2020-12-31:312` | Item 8 › Performance Fees | ✓ | #2 | Performance fees refer to compensation arrangements with payouts based on realized investment returns. We recognize compensation expense based on the estimated payouts, which may result in expense recognized before inves… |
| 13 | `GOOGL_FY2020_2020-12-31:462` | Item 8 › Stock-Based Compensation |  |  | For the years ended December 31, 2018, 2019 and 2020, total stock-based compensation expense was $10.0 billion, $11.7 billion and $13.4 billion, including amounts associated with awards we expect to settle in Alphabet st… |
| 14 | `GOOGL_FY2020_2020-12-31:289` | Item 8 › (In millions, except share amounts which are reflected in thousands) |  |  | \| \| Class A and Class B Common Stock, Class C Capital Stock and Additional Paid-In Capital \| \| Accumulated Other Comprehensive Income (Loss) \| Retained Earnings \| Total Stockholders’ Equity \| \|---\|---\|---\|---\|---\|---\| \| … |
| 15 | `GOOGL_FY2020_2020-12-31:288` | Item 8 › (In millions, except share amounts which are reflected in thousands) |  |  | \| \| Class A and Class B Common Stock, Class C Capital Stock and Additional Paid-In Capital \| \| Accumulated Other Comprehensive Income (Loss) \| Retained Earnings \| Total Stockholders’ Equity \| \|---\|---\|---\|---\|---\|---\| \| … |
| 16 | `GOOGL_FY2020_2020-12-31:422` | Item 8 › Other Income (Expense), Net | ✓ |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2018 \| 2019 \| 2020 \| \| Interest income \| $1,878 \| $2,427 \| $1,865 \| \| Interest expense(1) \| (114) \| (100) \| (135) \| \| Foreign currency exchange gain (loss), net (2)… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2020_2020-12-31:248`** (cited, gold #1)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Fair Value Measurements
We measure certain of our non-marketable equity and debt investments, certain other instruments including stock-based compensation awards settled in the stock of certain Other Bets, and certain assets and liabilities acquired in a business combination, at fair value on a nonrecurring basis. The determination of fair value involves the use of appropriate valuation methods and relevant inputs into valuation models. The fair value hierarchy prioritizes the inputs used to measure fair value whereby it gives the highest priority to quoted prices (unadjusted) in active markets for identical assets or liabilities and the lowest priority to unobservable inputs. We maximize the use of relevant observable inputs and minimize the use of unobservable inputs. Our use of unobservable inputs reflects the assumptions that market participants would use and may include our own data adjusted based on reasonably available information. We apply judgment in assessing the relevance of observable market data to determine the priority of inputs under the fair value hierarchy, particularly in situations where there is very little or no market activity. Table of Contents Alphabet Inc.
````

**#2 `GOOGL_FY2020_2020-12-31:249`** (cited, gold #2)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Fair Value Measurements
In determining the fair values of our non-marketable equity and debt investments, as well as assets acquired (especially with respect to intangible assets) and liabilities assumed in business combinations, we make significant estimates and assumptions, some of which include the use of unobservable inputs. Certain stock-based compensation awards may be settled in the stock of certain of our Other Bets or in cash. These awards are based on the equity values of the respective Other Bet, which requires use of unobservable inputs. We also have compensation arrangements with payouts based on realized investment returns, i.e. performance fees. We recognize compensation expense based on the estimated payouts, which may result in expense recognized before investment returns are realized, and may require the use of unobservable inputs.
````

**#4 `GOOGL_FY2020_2020-12-31:316`** (cited, gold #1)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Fair Value of Financial Instruments
Level 2 - Inputs that are based upon quoted prices for similar instruments in active markets, quoted prices for identical or similar instruments in markets that are not active, and model-based valuation techniques for which all significant inputs are observable in the market or can be derived from observable market data. Where applicable, these models project future cash flows and discount the future amounts to a present value using market-based observable inputs including interest rate curves, foreign exchange rates, and credit ratings. Level 3 - Unobservable inputs that are supported by little or no market activities. The fair value hierarchy requires an entity to maximize the use of observable inputs and minimize the use of unobservable inputs when measuring fair value.
````

**#6 `GOOGL_FY2020_2020-12-31:250`** (cited)

````text
ITEM 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Non-marketable Equity Securities
Our non-marketable equity securities not accounted for under the equity method are carried either at fair value or under the measurement alternative. Under the measurement alternative, the carrying value is measured at cost, less any impairment, plus or minus changes resulting from observable price changes in orderly transactions for the identical or a similar investment of the same issuer. Determining whether an observed transaction is similar to a security within our portfolio requires judgment based on the rights and obligations of the securities. Recording upward and downward adjustments to the carrying value of our equity securities as a result of observable price changes requires quantitative assessments of the fair value of our securities using various valuation methodologies and involves the use of estimates.
````

**#12 `GOOGL_FY2020_2020-12-31:312`** (cited, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Performance Fees
Performance fees refer to compensation arrangements with payouts based on realized investment returns. We recognize compensation expense based on the estimated payouts, which may result in expense recognized before investment returns are realized. Performance fees, which are primarily related to gains on equity securities, are recorded as a component of other income (expense), net.
````

**#16 `GOOGL_FY2020_2020-12-31:422`** (cited)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Income (Expense), Net (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2018 | 2019 | 2020 |
| Interest income | $1,878 | $2,427 | $1,865 |
| Interest expense(1) | (114) | (100) | (135) |
| Foreign currency exchange gain (loss), net (2) | (80) | 103 | (344) |
| Gain (loss) on debt securities, net(3) | 1,190 | 149 | 725 |
| Gain (loss) on equity securities, net | 5,460 | 2,649 | 5,592 |
| Performance fees | (1,203) | (326) | (609) |
| Income (loss) and impairment from equity method investments, net | (120) | 390 | 401 |
| Other(4) | 378 | 102 | (637) |
| Other income (expense), net | $7,389 | $5,394 | $6,858 |
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 7'), ('GOOGL', 'Item 8')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 8, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Alphabet states that in determining the fair values of its non-marketable equity and debt investments, assets acquired and liabilities assumed in business combinations, and certain stock-based compensation awards settled in the stock of certain Other Bets, it makes significant estimates and assumptions, some of which include the use of unobservable inputs. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:249] | supported | The cited text states all three categories and says some estimates and assumptions include unobservable inputs. |
| The company says its use of unobservable inputs reflects assumptions that market participants would use and may include Alphabet’s own data adjusted based on reasonably available information. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:248] | supported | The evidence explicitly says unobservable inputs reflect market participant assumptions and may include Alphabet’s own adjusted data. |
| Alphabet also says it maximizes the use of relevant observable inputs and minimizes the use of unobservable inputs when measuring fair value, and that Level 3 inputs are unobservable inputs supported by little or no market activities. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:248] [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:316] | supported | One citation states Alphabet maximizes observable inputs and minimizes unobservable inputs, and the other defines Level 3 as unobservable inputs with little or no market activity. |
| For non-marketable equity securities under the measurement alternative, Alphabet says carrying value is measured at cost, less any impairment, plus or minus changes from observable price changes in orderly transactions for the identical or a similar investment of the same issuer, and that determining similarity of observed transactions and recording upward and downward adjustments requires judgment, quantitative assessments, various valuation methodologies, and the use of estimates. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:250] | supported | The cited passage matches the measurement alternative description and the judgment, valuation, and estimates language. |
| For certain Other Bets awards, Alphabet says these awards are based on the equity values of the respective Other Bet, which requires use of unobservable inputs. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:249] | supported | The evidence expressly says certain Other Bets awards are based on the equity values of the respective Other Bet and require unobservable inputs. |
| Regarding performance fee compensation arrangements, Alphabet says these payouts are based on realized investment returns and that it recognizes compensation expense based on estimated payouts, which may result in expense being recognized before investment returns are realized. [GOOGL FY2020, Item 7, GOOGL_FY2020_2020-12-31:249] [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:312] | supported | The cited evidence states both that payouts are based on realized investment returns and that expense is recognized based on estimated payouts before returns are realized. |
| Alphabet further discloses that performance fees are recorded as a component of other income (expense), net. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:312] | supported | The citation explicitly says performance fees are recorded as a component of other income (expense), net. |
| In 2020, performance fees were $(609) million. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:422] | supported | The table shows Performance fees of $(609) million for 2020. |

</details>
