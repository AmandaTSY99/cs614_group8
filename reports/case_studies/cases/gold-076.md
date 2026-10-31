# gold-076: Cross-year table

[← all cases](../README.md) · company: MICROSOFT CORP (MSFT) · fiscal year: 2020 · recipe `cross_year_table` · hop `multi` · answer type `numeric` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> By what percentage did the total estimated fair value of Microsoft's debt investments increase from June 30, 2016 to June 30, 2020?

**Gold answer**

> 19.38%

**Program**: `subtract(129798, 108730), divide(#0, 108730), multiply(#1, 100)` → `19.376437045893496`

**Gold numbers** (RQ2 numeric_accuracy targets): 19.38%

**Gold evidence**

1. `MSFT_FY2020_2020-06-30` · Item 8 › Debt Investment Maturities · table

   > Total | $122,900 | $129,798

2. `MSFT_FY2016_2016-06-30` · Item 8 › Debt Investment Maturities · table

   > Total | $108,353 | $108,730

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 8 |
| recall@5 | 1.00 | 0.50 | 1.00 | 1.00 |
| recall@all | 1.00 | 0.50 | 1.00 | 1.00 |
| complete@all | 1 | 0 | 1 | 1 |
| average precision (lexical) | 0.45 | 0.50 | 0.42 | 0.33 |
| gold evidence first rank | #1: 2, #2: 5 | #1: –, #2: 2 | #1: 3, #2: 4 | #1: 5, #2: 4 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✗ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 0.00 | 1.00 | 1.00 |
| citation precision | 1.00 | – | 1.00 | 1.00 |
| citation recall | 1.00 | – | 1.00 | 1.00 |
| citation F1 | 1.00 | – | 1.00 | 1.00 |
| has a citation | 1 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 2589 | 1164 | 3903 | 4563 |
| cost (USD) | 0.0004 | 0.0002 | 0.0148 | 0.0162 |
| latency (s) | 2.7 | 6.9 | 7.3 | 7.6 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Microsoft’s total estimated fair value of debt investments increased from **$108,730 million** on June 30, 2016 to **$129,798 million** on June 30, 2020 [5][2].
>
> Percentage increase:
>
> \[
> \frac{129,798 - 108,730}{108,730} \times 100 \approx 19.4\%
> \]
>
> So, the total estimated fair value of Microsoft’s debt investments increased by **about 19.4%** from June 30, 2016 to June 30, 2020 [5][2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2020_2020-06-30:393` | Item 8 › PART II |  |  | (a) In June 2020, we exchanged a portion of our existing debt at premium for cash and new debt with longer maturities. The premium will be amortized over the term of the new debt. (b) Refer to Note 5 – Derivatives for fu… |
| 2 | `MSFT_FY2020_2020-06-30:350` | Item 8 › Debt Investment Maturities | ✓ | #1 | \| (In millions) \| Cost Basis \| Estimated Fair Value \| \|---\|---\|---\| \| June 30, 2020 \| \| \| \| Due in one year or less \| $36,169 \| $36,276 \| \| Due after one year through five years \| 51,465 \| 54,700 \| \| Due after five years… |
| 3 | `MSFT_FY2020_2020-06-30:347` | Item 8 › Unrealized Losses on Debt Investments |  |  | \| \| Less than 12 Months \| \| 12 Months or Greater \| \| Total Unrealized Losses \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (In millions) \| Fair Value \| Unrealized Losses \| Fair Value \| Unrealized Losses \| Total Fair Value \| \| \| Ju… |
| 4 | `MSFT_FY2016_2016-06-30:394` | Item 8 › Long-term Debt |  |  | As of June 30, 2016, the total carrying value and estimated fair value of our long-term debt were $40.8 billion and $44.0 billion, respectively. This is compared to a carrying value and estimated fair value of our long-t… |
| 5 | `MSFT_FY2016_2016-06-30:330` | Item 8 › Debt Investment Maturities | ✓ | #2 | \| (In millions) \| Cost Basis \| Estimated Fair Value \| \|---\|---\|---\| \| June 30, 2016 \| \| \| \| Due in one year or less \| $54,503 \| $54,544 \| \| Due after one year through five years \| 50,683 \| 50,896 \| \| Due after five years… |
| 6 | `MSFT_FY2020_2020-06-30:339` | Item 8 › Investment Components |  |  | \| (In millions) \| Fair Value Level \| Cost Basis \| Unrealized Gains \| Unrealized Losses \| Recorded Basis \| Cash and Cash Equivalents \| Short-term Investments \| Equity Investments \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| … |
| 7 | `MSFT_FY2020_2020-06-30:342` | Item 8 › PART II |  |  | \| (In millions) \| Fair Value Level \| Cost Basis \| Unrealized Gains \| Unrealized Losses \| Recorded Basis \| Cash and Cash Equivalents \| Short-term Investments \| Equity Investments \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| … |
| 8 | `MSFT_FY2020_2020-06-30:346` | Item 8 › Unrealized Losses on Debt Investments |  |  | Debt investments with continuous unrealized losses for less than 12 months and 12 months or greater and their related fair values were as follows: |
| 9 | `MSFT_FY2020_2020-06-30:348` | Item 8 › PART II |  |  | \| \| Less than 12 Months \| \| 12 Months or Greater \| \| Total Unrealized Losses \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (In millions) \| Fair Value \| Unrealized Losses \| Fair Value \| Unrealized Losses \| Total Fair Value \| \| \| Ju… |
| 10 | `MSFT_FY2020_2020-06-30:392` | Item 8 › PART II |  |  | \| (In millions, issuance by calendar year) \| Maturities (calendar year) \| \| Stated Interest Rate \| \| \| \| Effective Interest Rate \| \| June 30, 2020 \| June 30, 2019 \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| 2… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `MSFT_FY2020_2020-06-30:350`** (cited, gold #1)

````text
Item 8 > Debt Investment Maturities (table)
| (In millions) | Cost Basis | Estimated Fair Value |
|---|---|---|
| June 30, 2020 |  |  |
| Due in one year or less | $36,169 | $36,276 |
| Due after one year through five years | 51,465 | 54,700 |
| Due after five years through 10 years | 32,299 | 35,674 |
| Due after 10 years | 2,967 | 3,148 |
| Total | $122,900 | $129,798 |
````

**#5 `MSFT_FY2016_2016-06-30:330`** (cited, gold #2)

````text
Item 8 > Debt Investment Maturities (table)
| (In millions) | Cost Basis | Estimated Fair Value |
|---|---|---|
| June 30, 2016 |  |  |
| Due in one year or less | $54,503 | $54,544 |
| Due after one year through five years | 50,683 | 50,896 |
| Due after five years through 10 years | 1,914 | 1,954 |
| Due after 10 years | 1,253 | 1,336 |
| Total | $108,353 | $108,730 |
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2016_2016-06-30:394` | Item 8 › Long-term Debt |  |  | As of June 30, 2016, the total carrying value and estimated fair value of our long-term debt were $40.8 billion and $44.0 billion, respectively. This is compared to a carrying value and estimated fair value of our long-t… |
| 2 | `MSFT_FY2016_2016-06-30:330` | Item 8 › Debt Investment Maturities |  | #2 | \| (In millions) \| Cost Basis \| Estimated Fair Value \| \|---\|---\|---\| \| June 30, 2016 \| \| \| \| Due in one year or less \| $54,503 \| $54,544 \| \| Due after one year through five years \| 50,683 \| 50,896 \| \| Due after five years… |
| 3 | `MSFT_FY2020_2020-06-30:393` | Item 8 › PART II |  |  | (a) In June 2020, we exchanged a portion of our existing debt at premium for cash and new debt with longer maturities. The premium will be amortized over the term of the new debt. (b) Refer to Note 5 – Derivatives for fu… |
| 4 | `MSFT_FY2016_2016-06-30:327` | Item 8 › Unrealized Losses on Investments |  |  | \| \| Less than 12 Months \| \| 12 Months or Greater \| \| Total Unrealized Losses \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (In millions) \| Fair Value \| Unrealized Losses \| Fair Value \| Unrealized Losses \| Total Fair Value \| \| \| Ju… |
| 5 | `MSFT_FY2020_2020-06-30:347` | Item 8 › Unrealized Losses on Debt Investments |  |  | \| \| Less than 12 Months \| \| 12 Months or Greater \| \| Total Unrealized Losses \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (In millions) \| Fair Value \| Unrealized Losses \| Fair Value \| Unrealized Losses \| Total Fair Value \| \| \| Ju… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `MSFT_FY2016_2016-06-30:330`** (gold #2)

````text
Item 8 > Debt Investment Maturities (table)
| (In millions) | Cost Basis | Estimated Fair Value |
|---|---|---|
| June 30, 2016 |  |  |
| Due in one year or less | $54,503 | $54,544 |
| Due after one year through five years | 50,683 | 50,896 |
| Due after five years through 10 years | 1,914 | 1,954 |
| Due after 10 years | 1,253 | 1,336 |
| Total | $108,353 | $108,730 |
````

</details>

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 2.

**Generated answer**

> Microsoft's total estimated fair value of debt investments increased from $108,730 million on June 30, 2016 to $129,798 million on June 30, 2020, an increase of approximately 19.4% [MSFT FY2016, Item 8, MSFT_FY2016_2016-06-30:330] [MSFT FY2020, Item 8, MSFT_FY2020_2020-06-30:350].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2016_2016-06-30:394` | Item 8 › Long-term Debt |  |  | As of June 30, 2016, the total carrying value and estimated fair value of our long-term debt were $40.8 billion and $44.0 billion, respectively. This is compared to a carrying value and estimated fair value of our long-t… |
| 2 | `MSFT_FY2020_2020-06-30:393` | Item 8 › PART II |  |  | (a) In June 2020, we exchanged a portion of our existing debt at premium for cash and new debt with longer maturities. The premium will be amortized over the term of the new debt. (b) Refer to Note 5 – Derivatives for fu… |
| 3 | `MSFT_FY2020_2020-06-30:350` | Item 8 › Debt Investment Maturities | ✓ | #1 | \| (In millions) \| Cost Basis \| Estimated Fair Value \| \|---\|---\|---\| \| June 30, 2020 \| \| \| \| Due in one year or less \| $36,169 \| $36,276 \| \| Due after one year through five years \| 51,465 \| 54,700 \| \| Due after five years… |
| 4 | `MSFT_FY2016_2016-06-30:330` | Item 8 › Debt Investment Maturities | ✓ | #2 | \| (In millions) \| Cost Basis \| Estimated Fair Value \| \|---\|---\|---\| \| June 30, 2016 \| \| \| \| Due in one year or less \| $54,503 \| $54,544 \| \| Due after one year through five years \| 50,683 \| 50,896 \| \| Due after five years… |
| 5 | `MSFT_FY2020_2020-06-30:347` | Item 8 › Unrealized Losses on Debt Investments |  |  | \| \| Less than 12 Months \| \| 12 Months or Greater \| \| Total Unrealized Losses \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (In millions) \| Fair Value \| Unrealized Losses \| Fair Value \| Unrealized Losses \| Total Fair Value \| \| \| Ju… |
| 6 | `MSFT_FY2020_2020-06-30:346` | Item 8 › Unrealized Losses on Debt Investments |  |  | Debt investments with continuous unrealized losses for less than 12 months and 12 months or greater and their related fair values were as follows: |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `MSFT_FY2020_2020-06-30:350`** (cited, gold #1)

````text
Item 8 > Debt Investment Maturities (table)
| (In millions) | Cost Basis | Estimated Fair Value |
|---|---|---|
| June 30, 2020 |  |  |
| Due in one year or less | $36,169 | $36,276 |
| Due after one year through five years | 51,465 | 54,700 |
| Due after five years through 10 years | 32,299 | 35,674 |
| Due after 10 years | 2,967 | 3,148 |
| Total | $122,900 | $129,798 |
````

**#4 `MSFT_FY2016_2016-06-30:330`** (cited, gold #2)

````text
Item 8 > Debt Investment Maturities (table)
| (In millions) | Cost Basis | Estimated Fair Value |
|---|---|---|
| June 30, 2016 |  |  |
| Due in one year or less | $54,503 | $54,544 |
| Due after one year through five years | 50,683 | 50,896 |
| Due after five years through 10 years | 1,914 | 1,954 |
| Due after 10 years | 1,253 | 1,336 |
| Total | $108,353 | $108,730 |
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Microsoft's total estimated fair value of debt investments increased from $108,730 million on June 30, 2016 to $129,798 million on June 30, 2020, an increase of approximately 19.4% [MSFT FY2016, Item 8, MSFT_FY2016_2016-06-30:330] [MSFT FY2020, Item 8, MSFT_FY2020_2020-06-30:350]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 2.

**Generated answer**

> Microsoft’s total estimated fair value of debt investments increased from $108,730 million on June 30, 2016 to $129,798 million on June 30, 2020, an increase of approximately 19.4% [MSFT FY2016, Item 8, MSFT_FY2016_2016-06-30:330] [MSFT FY2020, Item 8, MSFT_FY2020_2020-06-30:350].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-MSFT-2016` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2016,2016-06-30,85320000000,16798000000,20182000000,1936940000… |
| 2 | `F-MSFT-2020` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2020,2020-06-30,143015000000,44281000000,52959000000,301311000… |
| 3 | `MSFT_FY2016_2016-06-30:394` | Item 8 › Long-term Debt |  |  | As of June 30, 2016, the total carrying value and estimated fair value of our long-term debt were $40.8 billion and $44.0 billion, respectively. This is compared to a carrying value and estimated fair value of our long-t… |
| 4 | `MSFT_FY2016_2016-06-30:330` | Item 8 › Debt Investment Maturities | ✓ | #2 | \| (In millions) \| Cost Basis \| Estimated Fair Value \| \|---\|---\|---\| \| June 30, 2016 \| \| \| \| Due in one year or less \| $54,503 \| $54,544 \| \| Due after one year through five years \| 50,683 \| 50,896 \| \| Due after five years… |
| 5 | `MSFT_FY2020_2020-06-30:350` | Item 8 › Debt Investment Maturities | ✓ | #1 | \| (In millions) \| Cost Basis \| Estimated Fair Value \| \|---\|---\|---\| \| June 30, 2020 \| \| \| \| Due in one year or less \| $36,169 \| $36,276 \| \| Due after one year through five years \| 51,465 \| 54,700 \| \| Due after five years… |
| 6 | `MSFT_FY2020_2020-06-30:393` | Item 8 › PART II |  |  | (a) In June 2020, we exchanged a portion of our existing debt at premium for cash and new debt with longer maturities. The premium will be amortized over the term of the new debt. (b) Refer to Note 5 – Derivatives for fu… |
| 7 | `MSFT_FY2020_2020-06-30:347` | Item 8 › Unrealized Losses on Debt Investments |  |  | \| \| Less than 12 Months \| \| 12 Months or Greater \| \| Total Unrealized Losses \| \| \|---\|---\|---\|---\|---\|---\|---\| \| (In millions) \| Fair Value \| Unrealized Losses \| Fair Value \| Unrealized Losses \| Total Fair Value \| \| \| Ju… |
| 8 | `MSFT_FY2016_2016-06-30:351` | Item 8 › PART II |  |  | NOTE 6 — FAIR VALUE MEASUREMENTS |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#4 `MSFT_FY2016_2016-06-30:330`** (cited, gold #2)

````text
Item 8 > Debt Investment Maturities (table)
| (In millions) | Cost Basis | Estimated Fair Value |
|---|---|---|
| June 30, 2016 |  |  |
| Due in one year or less | $54,503 | $54,544 |
| Due after one year through five years | 50,683 | 50,896 |
| Due after five years through 10 years | 1,914 | 1,954 |
| Due after 10 years | 1,253 | 1,336 |
| Total | $108,353 | $108,730 |
````

**#5 `MSFT_FY2020_2020-06-30:350`** (cited, gold #1)

````text
Item 8 > Debt Investment Maturities (table)
| (In millions) | Cost Basis | Estimated Fair Value |
|---|---|---|
| June 30, 2020 |  |  |
| Due in one year or less | $36,169 | $36,276 |
| Due after one year through five years | 51,465 | 54,700 |
| Due after five years through 10 years | 32,299 | 35,674 |
| Due after 10 years | 2,967 | 3,148 |
| Total | $122,900 | $129,798 |
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 3, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Microsoft’s total estimated fair value of debt investments increased from $108,730 million on June 30, 2016 to $129,798 million on June 30, 2020, an increase of approximately 19.4% [MSFT FY2016, Item 8, MSFT_FY2016_2016-06-30:330] [MSFT FY2020, Item 8, MSFT_FY2020_2020-06-30:350]. | None |  |

</details>
