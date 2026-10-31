# gold-074: Cross-year table

[← all cases](../README.md) · company: Alphabet Inc. (GOOGL) · fiscal year: 2024 · recipe `cross_year_table` · hop `multi` · answer type `numeric` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> By how many millions of dollars was Alphabet Inc.'s net gain on equity securities in fiscal year 2024 lower than in fiscal year 2018?

**Gold answer**

> $1,746 million

**Program**: `subtract(5460, 3714)` → `1746.0`

**Gold numbers** (RQ2 numeric_accuracy targets): $1,746 million

**Gold evidence**

1. `GOOGL_FY2024_2024-12-31` · ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Other Income (Expense), Net · table

   > Gain (loss) on equity securities, net | (3,455) | 392 | 3,714

2. `GOOGL_FY2020_2020-12-31` · ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Other Income (Expense), Net · table

   > Gain (loss) on equity securities, net | 5,460 | 2,649 | 5,592

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 10 | 8 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.70 | 0.50 | 0.59 | 0.42 |
| gold evidence first rank | #1: 1, #2: 1 | #1: 2, #2: 2 | #1: 2, #2: 2 | #1: 3, #2: 3 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✗ | ✗ | ✗ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 0.00 | 0.00 |
| citation precision | – | – | – | – |
| citation recall | – | – | – | – |
| citation F1 | – | – | – | – |
| has a citation | 0 | 0 | 0 | 0 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 1 |
| tokens | 129 | 1135 | 13357 | 6690 |
| cost (USD) | 0.0003 | 0.0002 | 0.0505 | 0.0237 |
| latency (s) | 9.8 | 5.6 | 24.6 | 11.0 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2024_2024-12-31:376` | Item 8 › Gains and Losses on Marketable and Non-marketable Equity Securities |  | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2022 \| 2023 \| 2024 \| \| Realized net gain (loss) on equity securities sold during the period \| $(442) \| $690 \| $186 \| \| Unrealized net gain (loss) on marketable equi… |
| 2 | `GOOGL_FY2024_2024-12-31:371` | Item 8 › Debt Securities |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2022 \| 2023 \| 2024 \| \| Unrealized gain (loss) on fair value option debt securities \| $(557) \| $386 \| $30 \| \| Gross realized gain on debt securities \| 103 \| 182 \| 48… |
| 3 | `GOOGL_FY2024_2024-12-31:378` | Item 8 › Gains and Losses on Marketable and Non-marketable Equity Securities |  |  | \| \| 2023 \| 2024 \| \|---\|---\|---\| \| Total sale price \| $1,981 \| $2,827 \| \| Total initial cost \| 1,512 \| 2,079 \| \| Cumulative net gains (losses) \| $469 \| $748 \| |
| 4 | `GOOGL_FY2024_2024-12-31:495` | Item 8 › Note 16. Subsequent Event |  |  | In January 2025, we recognized an $8.0 billion unrealized gain on our non-marketable equity securities related to our investment in a private company. The unrealized gain reflects an increase in the fair value measuremen… |
| 5 | `GOOGL_FY2020_2020-12-31:357` | Item 8 › Gains and losses on marketable and non-marketable equity securities |  | #1, #2 | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2019 \| 2020 \| \| Net gain (loss) on equity securities sold during the period \| $(301) \| $1,339 \| \| Net unrealized gain (loss) on equity securities held as of the end of th… |
| 6 | `GOOGL_FY2024_2024-12-31:373` | Item 8 › Equity Investments |  |  | \| \| As of December 31, 2023 \| \| \| As of December 31, 2024 \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Marketable Equity Securities \| Non-Marketable Equity Securities \| Total \| Marketable Equity Securities \| Non-Marketable Eq… |
| 7 | `GOOGL_FY2024_2024-12-31:225` | Item 7 › Other Income (Expense), Net |  |  | OI&E, net increased $6.0 billion from 2023 to 2024 primarily due to an increase in net gains on equity securities and a decrease in net losses on foreign currency exchange. The net gains on equity securities were primari… |
| 8 | `GOOGL_FY2024_2024-12-31:368` | Item 8 › Debt Securities |  |  | \| \| As of December 31, 2023 \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Less than 12 Months \| \| 12 Months or Greater \| \| Total \| \| \| \| Fair Value \| Unrealized Loss \| Fair Value \| Unrealized Loss \| Fair Value \| Unrealiz… |
| 9 | `GOOGL_FY2024_2024-12-31:369` | Item 8 › Debt Securities |  |  | \| \| As of December 31, 2024 \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Less than 12 Months \| \| 12 Months or Greater \| \| Total \| \| \| \| Fair Value \| Unrealized Loss \| Fair Value \| Unrealized Loss \| Fair Value \| Unrealiz… |
| 10 | `GOOGL_FY2024_2024-12-31:291` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2022 \| 2023 \| 2024 \| \| Net income \| $59,972 \| $73,795 \| $100,118 \| \| Other comprehensive income (loss): \| \| \| \| \| Change in foreign currency translation adjustment,… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2024_2024-12-31:376`** (gold #1, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Gains and Losses on Marketable and Non-marketable Equity Securities (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2022 | 2023 | 2024 |
| Realized net gain (loss) on equity securities sold during the period | $(442) | $690 | $186 |
| Unrealized net gain (loss) on marketable equity securities | (3,242) | 790 | 156 |
| Unrealized net gain (loss) on non-marketable equity securities(1) | 229 | (1,088) | 3,372 |
| Total gain (loss) on equity securities in other income (expense), net | $(3,455) | $392 | $3,714 |
````

**#5 `GOOGL_FY2020_2020-12-31:357`** (gold #1, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Gains and losses on marketable and non-marketable equity securities (table)
|  | Year Ended December 31, |  |
|---|---|---|
|  | 2019 | 2020 |
| Net gain (loss) on equity securities sold during the period | $(301) | $1,339 |
| Net unrealized gain (loss) on equity securities held as of the end of the period | 2,950 | 4,253 |
| Total gain (loss) recognized in other income (expense), net | $2,649 | $5,592 |
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
| 1 | `GOOGL_FY2020_2020-12-31:364` | Item 8 › Carrying value of marketable and non-marketable equity securities |  |  | (1)Non-marketable equity securities cumulative net gain (loss) is comprised of $6.1 billion unrealized gains and $1.9 billion unrealized losses (including impairment). (2)The long-term portion of marketable equity securi… |
| 2 | `GOOGL_FY2024_2024-12-31:377` | Item 8 › Gains and Losses on Marketable and Non-marketable Equity Securities |  | #1, #2 | (1)Unrealized gain (loss) on non-marketable equity securities accounted for under the measurement alternative is comprised of $3.3 billion, $1.8 billion, and $5.6 billion of upward adjustments and $3.0 billion, $2.9 bill… |
| 3 | `GOOGL_FY2024_2024-12-31:495` | Item 8 › Note 16. Subsequent Event |  |  | In January 2025, we recognized an $8.0 billion unrealized gain on our non-marketable equity securities related to our investment in a private company. The unrealized gain reflects an increase in the fair value measuremen… |
| 4 | `GOOGL_FY2024_2024-12-31:298` | Item 8 › (in millions) |  | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2022 \| 2023 \| 2024 \| \| Operating activities \| \| \| \| \| Net income \| $59,972 \| $73,795 \| $100,118 \| \| Adjustments: \| \| \| \| \| Depreciation of property and equipment \| … |
| 5 | `GOOGL_FY2024_2024-12-31:374` | Item 8 › Equity Investments |  |  | (1)Non-marketable equity securities cumulative net gain (loss) is comprised of $18.1 billion and $22.7 billion of gains and $6.9 billion and $8.4 billion of losses (including impairments) as of December 31, 2023 and 2024… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `GOOGL_FY2024_2024-12-31:377`** (gold #1, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Gains and Losses on Marketable and Non-marketable Equity Securities
(1)Unrealized gain (loss) on non-marketable equity securities accounted for under the measurement alternative is comprised of $3.3 billion, $1.8 billion, and $5.6 billion of upward adjustments and $3.0 billion, $2.9 billion, and $2.2 billion of downward adjustments (including impairments) for the years ended December 31, 2022, 2023, and 2024, respectively. In the table above, realized net gain (loss) on equity securities sold during the period reflects the difference between the sale proceeds and the carrying value of the equity securities at the beginning of the period or the purchase date, if later. Cumulative net gains (losses) on equity securities sold during the period, which is summarized in the following table (in millions), represents the total net gains (losses) recognized after the initial purchase date of the equity security sold during the period. While these net gains (losses) may have been reflected in periods prior to the period of sale, we believe they are important supplemental information as they reflect the economic net gains (losses) on the securities sold during the period. Cumulative net gains (losses) are calculated as the difference between the sale price and the initial purchase price for the equity security sold during the period.
````

**#4 `GOOGL_FY2024_2024-12-31:298`** (gold #1, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > (in millions) (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2022 | 2023 | 2024 |
| Operating activities |  |  |  |
| Net income | $59,972 | $73,795 | $100,118 |
| Adjustments: |  |  |  |
| Depreciation of property and equipment | 13,475 | 11,946 | 15,311 |
| Stock-based compensation expense | 19,362 | 22,460 | 22,785 |
| Deferred income taxes | (8,081) | (7,763) | (5,257) |
| Loss (gain) on debt and equity securities, net | 5,519 | 823 | (2,671) |
| Other | 3,483 | 4,330 | 3,419 |
| Changes in assets and liabilities, net of effects of acquisitions: |  |  |  |
| Accounts receivable, net | (2,317) | (7,833) | (5,891) |
| Income taxes, net | 584 | 523 | (2,418) |
| Other assets | (5,046) | (2,143) | (1,397) |
| Accounts payable | 707 | 664 | 359 |
| Accrued expenses and other liabilities | 3,915 | 3,937 | (1,161) |
| Accrued revenue share | (445) | 482 | 1,059 |
| Deferred revenue | 367 | 525 | 1,043 |
````

</details>

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 10, cited: 0.

**Generated answer**

> The filing evidence provided does not disclose Alphabet Inc.'s net gain on equity securities for fiscal year 2018, so the difference versus fiscal year 2024 cannot be determined from these evidence blocks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2024_2024-12-31:374` | Item 8 › Equity Investments |  |  | (1)Non-marketable equity securities cumulative net gain (loss) is comprised of $18.1 billion and $22.7 billion of gains and $6.9 billion and $8.4 billion of losses (including impairments) as of December 31, 2023 and 2024… |
| 2 | `GOOGL_FY2020_2020-12-31:357` | Item 8 › Gains and losses on marketable and non-marketable equity securities |  | #1, #2 | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2019 \| 2020 \| \| Net gain (loss) on equity securities sold during the period \| $(301) \| $1,339 \| \| Net unrealized gain (loss) on equity securities held as of the end of th… |
| 3 | `GOOGL_FY2024_2024-12-31:376` | Item 8 › Gains and Losses on Marketable and Non-marketable Equity Securities |  | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2022 \| 2023 \| 2024 \| \| Realized net gain (loss) on equity securities sold during the period \| $(442) \| $690 \| $186 \| \| Unrealized net gain (loss) on marketable equi… |
| 4 | `GOOGL_FY2024_2024-12-31:225` | Item 7 › Other Income (Expense), Net |  |  | OI&E, net increased $6.0 billion from 2023 to 2024 primarily due to an increase in net gains on equity securities and a decrease in net losses on foreign currency exchange. The net gains on equity securities were primari… |
| 5 | `GOOGL_FY2024_2024-12-31:377` | Item 8 › Gains and Losses on Marketable and Non-marketable Equity Securities |  | #1, #2 | (1)Unrealized gain (loss) on non-marketable equity securities accounted for under the measurement alternative is comprised of $3.3 billion, $1.8 billion, and $5.6 billion of upward adjustments and $3.0 billion, $2.9 bill… |
| 6 | `GOOGL_FY2020_2020-12-31:362` | Item 8 › Carrying value of marketable and non-marketable equity securities |  |  | (1)Non-marketable equity securities cumulative net gain (loss) is comprised of $3.5 billion unrealized gains and $445 million unrealized losses (including impairment). |
| 7 | `GOOGL_FY2020_2020-12-31:356` | Item 8 › Gains and losses on marketable and non-marketable equity securities |  |  | Gains and losses reflected in other income (expense), net, for our marketable and non-marketable equity securities are summarized below (in millions): |
| 8 | `GOOGL_FY2020_2020-12-31:364` | Item 8 › Carrying value of marketable and non-marketable equity securities |  |  | (1)Non-marketable equity securities cumulative net gain (loss) is comprised of $6.1 billion unrealized gains and $1.9 billion unrealized losses (including impairment). (2)The long-term portion of marketable equity securi… |
| 9 | `GOOGL_FY2024_2024-12-31:375` | Item 8 › Gains and Losses on Marketable and Non-marketable Equity Securities |  |  | Gains and losses (including impairments), net, for marketable and non-marketable equity securities included in OI&E are summarized below (in millions): |
| 10 | `GOOGL_FY2020_2020-12-31:363` | Item 8 › Carrying value of marketable and non-marketable equity securities |  |  | \| \| As of December 31, 2020 \| \| \| \|---\|---\|---\|---\| \| \| Marketable Equity Securities \| Non-Marketable Equity Securities \| Total \| \| Total initial cost \| $2,227 \| $14,616 \| $16,843 \| \| Cumulative net gain (loss)(1) \| 3,63… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `GOOGL_FY2020_2020-12-31:357`** (gold #1, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Gains and losses on marketable and non-marketable equity securities (table)
|  | Year Ended December 31, |  |
|---|---|---|
|  | 2019 | 2020 |
| Net gain (loss) on equity securities sold during the period | $(301) | $1,339 |
| Net unrealized gain (loss) on equity securities held as of the end of the period | 2,950 | 4,253 |
| Total gain (loss) recognized in other income (expense), net | $2,649 | $5,592 |
````

**#3 `GOOGL_FY2024_2024-12-31:376`** (gold #1, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Gains and Losses on Marketable and Non-marketable Equity Securities (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2022 | 2023 | 2024 |
| Realized net gain (loss) on equity securities sold during the period | $(442) | $690 | $186 |
| Unrealized net gain (loss) on marketable equity securities | (3,242) | 790 | 156 |
| Unrealized net gain (loss) on non-marketable equity securities(1) | 229 | (1,088) | 3,372 |
| Total gain (loss) on equity securities in other income (expense), net | $(3,455) | $392 | $3,714 |
````

**#5 `GOOGL_FY2024_2024-12-31:377`** (gold #1, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Gains and Losses on Marketable and Non-marketable Equity Securities
(1)Unrealized gain (loss) on non-marketable equity securities accounted for under the measurement alternative is comprised of $3.3 billion, $1.8 billion, and $5.6 billion of upward adjustments and $3.0 billion, $2.9 billion, and $2.2 billion of downward adjustments (including impairments) for the years ended December 31, 2022, 2023, and 2024, respectively. In the table above, realized net gain (loss) on equity securities sold during the period reflects the difference between the sale proceeds and the carrying value of the equity securities at the beginning of the period or the purchase date, if later. Cumulative net gains (losses) on equity securities sold during the period, which is summarized in the following table (in millions), represents the total net gains (losses) recognized after the initial purchase date of the equity security sold during the period. While these net gains (losses) may have been reflected in periods prior to the period of sale, we believe they are important supplemental information as they reflect the economic net gains (losses) on the securities sold during the period. Cumulative net gains (losses) are calculated as the difference between the sale price and the initial purchase price for the equity security sold during the period.
````

</details>

RQ2 citation match (section level): `no citations`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| The filing evidence provided does not disclose Alphabet Inc.'s net gain on equity securities for fiscal year 2018, so the difference versus fiscal year 2024 cannot be determined from these evidence blocks. | supported | The retrieved evidence shows 2019, 2020, 2022, 2023, and 2024 equity-security gains/losses, but no 2018 figure, so the 2018-to-2024 difference cannot be determined from these blocks. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 0.

**Generated answer**

> The filing does not disclose Alphabet Inc.'s net gain on equity securities for fiscal year 2018, so the difference versus fiscal year 2024 cannot be determined from the provided evidence.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-GOOGL-2020` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2020,2020-12-31,182527000000,40269000000,41224000000,319616000… |
| 2 | `F-GOOGL-2024` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2024,2024-12-31,350018000000,100118000000,112390000000,4502560… |
| 3 | `GOOGL_FY2024_2024-12-31:377` | Item 8 › Gains and Losses on Marketable and Non-marketable Equity Securities |  | #1, #2 | (1)Unrealized gain (loss) on non-marketable equity securities accounted for under the measurement alternative is comprised of $3.3 billion, $1.8 billion, and $5.6 billion of upward adjustments and $3.0 billion, $2.9 bill… |
| 4 | `GOOGL_FY2024_2024-12-31:374` | Item 8 › Equity Investments |  |  | (1)Non-marketable equity securities cumulative net gain (loss) is comprised of $18.1 billion and $22.7 billion of gains and $6.9 billion and $8.4 billion of losses (including impairments) as of December 31, 2023 and 2024… |
| 5 | `GOOGL_FY2020_2020-12-31:357` | Item 8 › Gains and losses on marketable and non-marketable equity securities |  | #1, #2 | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2019 \| 2020 \| \| Net gain (loss) on equity securities sold during the period \| $(301) \| $1,339 \| \| Net unrealized gain (loss) on equity securities held as of the end of th… |
| 6 | `GOOGL_FY2020_2020-12-31:362` | Item 8 › Carrying value of marketable and non-marketable equity securities |  |  | (1)Non-marketable equity securities cumulative net gain (loss) is comprised of $3.5 billion unrealized gains and $445 million unrealized losses (including impairment). |
| 7 | `GOOGL_FY2024_2024-12-31:376` | Item 8 › Gains and Losses on Marketable and Non-marketable Equity Securities |  | #1, #2 | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2022 \| 2023 \| 2024 \| \| Realized net gain (loss) on equity securities sold during the period \| $(442) \| $690 \| $186 \| \| Unrealized net gain (loss) on marketable equi… |
| 8 | `GOOGL_FY2020_2020-12-31:358` | Item 8 › Gains and losses on marketable and non-marketable equity securities |  | #1, #2 | Table of Contents Alphabet Inc. In the table above, net gain (loss) on equity securities sold during the period reflects the difference between the sale proceeds and the carrying value of the equity securities at the beg… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `GOOGL_FY2024_2024-12-31:377`** (gold #1, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Gains and Losses on Marketable and Non-marketable Equity Securities
(1)Unrealized gain (loss) on non-marketable equity securities accounted for under the measurement alternative is comprised of $3.3 billion, $1.8 billion, and $5.6 billion of upward adjustments and $3.0 billion, $2.9 billion, and $2.2 billion of downward adjustments (including impairments) for the years ended December 31, 2022, 2023, and 2024, respectively. In the table above, realized net gain (loss) on equity securities sold during the period reflects the difference between the sale proceeds and the carrying value of the equity securities at the beginning of the period or the purchase date, if later. Cumulative net gains (losses) on equity securities sold during the period, which is summarized in the following table (in millions), represents the total net gains (losses) recognized after the initial purchase date of the equity security sold during the period. While these net gains (losses) may have been reflected in periods prior to the period of sale, we believe they are important supplemental information as they reflect the economic net gains (losses) on the securities sold during the period. Cumulative net gains (losses) are calculated as the difference between the sale price and the initial purchase price for the equity security sold during the period.
````

**#5 `GOOGL_FY2020_2020-12-31:357`** (gold #1, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Gains and losses on marketable and non-marketable equity securities (table)
|  | Year Ended December 31, |  |
|---|---|---|
|  | 2019 | 2020 |
| Net gain (loss) on equity securities sold during the period | $(301) | $1,339 |
| Net unrealized gain (loss) on equity securities held as of the end of the period | 2,950 | 4,253 |
| Total gain (loss) recognized in other income (expense), net | $2,649 | $5,592 |
````

**#7 `GOOGL_FY2024_2024-12-31:376`** (gold #1, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Gains and Losses on Marketable and Non-marketable Equity Securities (table)
|  | Year Ended December 31, |  |  |
|---|---|---|---|
|  | 2022 | 2023 | 2024 |
| Realized net gain (loss) on equity securities sold during the period | $(442) | $690 | $186 |
| Unrealized net gain (loss) on marketable equity securities | (3,242) | 790 | 156 |
| Unrealized net gain (loss) on non-marketable equity securities(1) | 229 | (1,088) | 3,372 |
| Total gain (loss) on equity securities in other income (expense), net | $(3,455) | $392 | $3,714 |
````

**#8 `GOOGL_FY2020_2020-12-31:358`** (gold #1, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Gains and losses on marketable and non-marketable equity securities
Table of Contents Alphabet Inc. In the table above, net gain (loss) on equity securities sold during the period reflects the difference between the sale proceeds and the carrying value of the equity securities at the beginning of the period or the purchase date, if later. Cumulative net gains (losses) on equity securities sold during the period, which is summarized in the following table (in millions), represents the total net gains (losses) recognized after the initial purchase date of the equity security. While these net gains may have been reflected in periods prior to the period of sale, we believe they are important supplemental information as they reflect the economic realized net gains on the securities sold during the period. Cumulative net gains are calculated as the difference between the sale price and the initial purchase price for the equity security sold during the period.
````

</details>

RQ2 citation match (section level): `no citations`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| The filing does not disclose Alphabet Inc.'s net gain on equity securities for fiscal year 2018, so the difference versus fiscal year 2024 cannot be determined from the provided evidence. | supported | The retrieved evidence shows equity-securities gain/loss data for 2019, 2020, and 2022–2024, but nothing for 2018, so a 2018 vs. 2024 difference cannot be determined from it. |

</details>
