# gold-096: Cross-company text

[← all cases](../README.md) · company: Alphabet Inc.; Apple Inc. (GOOGL, AAPL) · fiscal year: 2023 · recipe `cross_company_text` · hop `multi` · answer type `qualitative` · scope `cross_company` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> Compare how Alphabet Inc. and Apple Inc. described their interest rate risk management strategies in their fiscal year 2023 10-K filings, specifically highlighting the difference between Alphabet's use of value-at-risk analysis and Apple's specific defensive instruments.

**Gold answer**

> In its fiscal year 2023 10-K, Alphabet described its interest rate risk management using a value-at-risk (VaR) analysis with a 95% confidence interval to determine the potential effect of interest rate fluctuations on its marketable debt security portfolio. In contrast, Apple's fiscal year 2023 10-K stated that to protect against interest rate risk, the company may use derivative instruments, offset interest rate-sensitive assets and liabilities, or control the duration of its investment and term debt portfolios.

**Key points** (RQ3 keypoint_recall targets)

1. Alphabet uses value-at-risk (VaR) analysis to assess interest rate risk.
2. Apple uses derivative instruments, offsets interest rate-sensitive assets/liabilities, or controls duration to manage interest rate risk.

**Gold evidence**

1. `GOOGL_FY2023_2023-12-31` · ITEM 7A.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK › Interest Rate Risk · text

   > We use value-at-risk (VaR) analysis to determine the potential effect of fluctuations in interest rates on the value of our marketable debt security portfolio.

2. `AAPL_FY2023_2023-09-30` · Item 7A. Quantitative and Qualitative Disclosures About Market Risk › Interest Rate Risk · text

   > To protect against interest rate risk, the Company may use derivative instruments, offset interest rate–sensitive assets and liabilities, or control duration of the investment and term debt portfolios.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 7 | 5 | 14 | 14 |
| recall@5 | 0.50 | 1.00 | 0.50 | 0.50 |
| recall@all | 0.50 | 1.00 | 1.00 | 1.00 |
| complete@all | 0 | 1 | 1 | 1 |
| average precision (lexical) | 1.00 | 0.75 | 0.53 | 0.50 |
| gold evidence first rank | #1: 1, #2: – | #1: 1, #2: 4 | #1: 1, #2: 7 | #1: 1, #2: 9 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | 0.50 | 1.00 | 1.00 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 1.00 | 1.00 | 0.67 | 0.67 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 0.80 | 0.80 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 1690 | 1373 | 16993 | 27182 |
| cost (USD) | 0.0003 | 0.0003 | 0.0648 | 0.1007 |
| latency (s) | 4.4 | 8.5 | 33.9 | 39.3 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 7, cited: 2.

**Generated answer**

> The provided context includes Alphabet’s disclosure, but does not include Apple’s FY2023 10-K disclosure, so I can only answer the Alphabet portion and note what is missing.
>
> - **Alphabet Inc.** said it **uses value-at-risk (VaR) analysis** to measure the potential effect of interest rate fluctuations on the value of its marketable debt securities portfolio. Specifically, Alphabet uses a **variance/covariance VaR model with a 95% confidence interval** to estimate the expected one-day loss in fair value from adverse interest rate movements [1][2].
>
> - **Apple Inc.**: the context does **not** provide Apple’s FY2023 10-K discussion of interest rate risk management or its “specific defensive instruments,” so that comparison cannot be completed from the provided materials.
>
> So, based on the available context, the key point is that **Alphabet described interest rate risk management as a measurement approach using VaR**, while **Apple’s specific instruments are not available in the provided context** [1][2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2023_2023-12-31:260` | Item 7A › Interest Rate Risk | ✓ | #1 | Table of Contents Alphabet Inc. We use value-at-risk (VaR) analysis to determine the potential effect of fluctuations in interest rates on the value of our marketable debt security portfolio. The VaR is the expected loss… |
| 2 | `GOOGL_FY2023_2023-12-31:261` | Item 7A › Interest Rate Risk | ✓ |  | \| \| As of December 31, \| \| 12-Month Average As of December 31, \| \| \|---\|---\|---\|---\|---\| \| \| 2022 \| 2023 \| 2022 \| 2023 \| \| Risk category - interest rate \| $256 \| $296 \| $198 \| $271 \| |
| 3 | `GOOGL_FY2023_2023-12-31:360` | Item 8 › Debt Securities |  |  | \| \| As of December 31, 2023 \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Less than 12 Months \| \| 12 Months or Greater \| \| Total \| \| \| \| Fair Value \| Unrealized Loss \| Fair Value \| Unrealized Loss \| Fair Value \| Unrealiz… |
| 4 | `GOOGL_FY2023_2023-12-31:359` | Item 8 › Debt Securities |  |  | \| \| As of December 31, 2022 \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Less than 12 Months \| \| 12 Months or Greater \| \| Total \| \| \| \| Fair Value \| Unrealized Loss \| Fair Value \| Unrealized Loss \| Fair Value \| Unrealiz… |
| 5 | `GOOGL_FY2023_2023-12-31:401` | Item 8 › Long-Term Debt |  |  | \| \| \| \| Effective Interest Rate \| As of December 31, \| \| \|---\|---\|---\|---\|---\|---\| \| \| Maturity \| Coupon Rate \| 2022 \| 2023 \| \| \| Debt \| \| \| \| \| \| \| 2014-2020 Notes issuances \| 2024 - 2060 \| 0.45% - 3.38% \| 0.57% - 3.38%… |
| 6 | `GOOGL_FY2023_2023-12-31:372` | Item 8 › Equity Securities Accounted for Under the Equity Method |  |  | As of December 31, 2022 and 2023, equity securities accounted for under the equity method had a carrying value of approximately $1.5 billion and $1.7 billion, respectively. Our share of gains and losses, including impair… |
| 7 | `GOOGL_FY2023_2023-12-31:357` | Item 8 › Debt Securities |  |  | \| \| As of December 31, 2023 \| \|---\|---\| \| Due in one year or less \| $11,231 \| \| Due in one year through five years \| 41,477 \| \| Due in five years through 10 years \| 15,351 \| \| Due after 10 years \| 14,216 \| \| Total \| $82,… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2023_2023-12-31:260`** (cited, gold #1)

````text
ITEM 7A.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK > Interest Rate Risk
Table of Contents Alphabet Inc. We use value-at-risk (VaR) analysis to determine the potential effect of fluctuations in interest rates on the value of our marketable debt security portfolio. The VaR is the expected loss in fair value, for a given confidence interval, for our investment portfolio due to adverse movements in interest rates. We use a variance/covariance VaR model with 95% confidence interval. The estimated one-day loss in fair value of marketable debt securities as of December 31, 2022 and 2023 are shown below (in millions):
````

**#2 `GOOGL_FY2023_2023-12-31:261`** (cited)

````text
ITEM 7A.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK > Interest Rate Risk (table)
|  | As of December 31, |  | 12-Month Average As of December 31, |  |
|---|---|---|---|---|
|  | 2022 | 2023 | 2022 | 2023 |
| Risk category - interest rate | $256 | $296 | $198 | $271 |
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 7A')] gold=[(None, 'Item 7A')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Alphabet and Apple described interest rate risk differently in their FY2023 10-Ks:
>
> - **Alphabet Inc.** said it **uses value-at-risk (VaR) analysis** to measure the potential effect of interest rate fluctuations on the value of its **marketable debt security portfolio**. It defined VaR as the expected loss in fair value for a given confidence interval and stated it uses a **variance/covariance VaR model with a 95% confidence interval**. This is primarily a **risk measurement/assessment approach**. [1]
>
> - **Apple Inc.** said it is exposed to U.S. interest rate fluctuations affecting both its **investment portfolio and term debt**, and that to protect against this risk it may use **derivative instruments**, **offset interest rate-sensitive assets and liabilities**, or **control duration of the investment and term debt portfolios**. This is a more explicit description of **defensive risk management tools and actions**. [4]
>
> So, the key difference is that **Alphabet emphasized VaR as an analytical method for quantifying interest rate risk**, while **Apple specifically identified instruments and portfolio management techniques it may use to mitigate that risk**, such as derivatives and duration control. [1][4]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2023_2023-12-31:260` | Item 7A › Interest Rate Risk | ✓ | #1 | Table of Contents Alphabet Inc. We use value-at-risk (VaR) analysis to determine the potential effect of fluctuations in interest rates on the value of our marketable debt security portfolio. The VaR is the expected loss… |
| 2 | `GOOGL_FY2023_2023-12-31:184` | Item 7 › Other Information: |  |  | Table of Contents Alphabet Inc. •On July 21, 2023, the IRS announced a rule change allowing taxpayers to temporarily apply the regulations in effect prior to 2022 related to U.S. federal foreign tax credits. This announc… |
| 3 | `AAPL_FY2023_2023-09-30:122` | Item 7 › Fiscal Year Highlights |  |  | •Apple Watch Series 9 and Apple Watch Ultra 2. In May 2023, the Company announced a new share repurchase program of up to $90 billion and raised its quarterly dividend from $0.23 to $0.24 per share beginning in May 2023.… |
| 4 | `AAPL_FY2023_2023-09-30:147` | Item 7A › Interest Rate Risk | ✓ | #2 | The Company is primarily exposed to fluctuations in U.S. interest rates and their impact on the Company’s investment portfolio and term debt. Increases in interest rates will negatively affect the fair value of the Compa… |
| 5 | `AAPL_FY2023_2023-09-30:150` | Item 7A › Foreign Exchange Rate Risk |  |  | The Company applied a value-at-risk (“VAR”) model to its foreign currency derivative positions to assess the potential impact of fluctuations in exchange rates. The VAR model used a Monte Carlo simulation. The VAR is the… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2023_2023-12-31:260`** (cited, gold #1)

````text
ITEM 7A.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK > Interest Rate Risk
Table of Contents Alphabet Inc. We use value-at-risk (VaR) analysis to determine the potential effect of fluctuations in interest rates on the value of our marketable debt security portfolio. The VaR is the expected loss in fair value, for a given confidence interval, for our investment portfolio due to adverse movements in interest rates. We use a variance/covariance VaR model with 95% confidence interval. The estimated one-day loss in fair value of marketable debt securities as of December 31, 2022 and 2023 are shown below (in millions):
````

**#4 `AAPL_FY2023_2023-09-30:147`** (cited, gold #2)

````text
Item 7A. Quantitative and Qualitative Disclosures About Market Risk > Interest Rate Risk
The Company is primarily exposed to fluctuations in U.S. interest rates and their impact on the Company’s investment portfolio and term debt. Increases in interest rates will negatively affect the fair value of the Company’s investment portfolio and increase the interest expense on the Company’s term debt. To protect against interest rate risk, the Company may use derivative instruments, offset interest rate–sensitive assets and liabilities, or control duration of the investment and term debt portfolios. The following table sets forth potential impacts on the Company’s investment portfolio and term debt, including the effects of any associated derivatives, that would result from a hypothetical increase in relevant interest rates as of September 30, 2023 and September 24, 2022 (dollars in millions):
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 7A'), ('AAPL', 'Item 7A')] gold=[(None, 'Item 7A')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 14, cited: 4.

**Generated answer**

> Alphabet said it uses value-at-risk analysis to determine the potential effect of fluctuations in interest rates on the value of its marketable debt security portfolio, and it described VaR as the expected loss in fair value for a given confidence interval due to adverse movements in interest rates. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:260]  
> Alphabet further stated that it uses a variance/covariance VaR model with a 95% confidence interval. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:260]  
> Alphabet’s disclosure therefore emphasizes measurement of interest rate exposure through VaR on its marketable debt securities rather than identifying specific hedging instruments in the cited interest rate risk discussion. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:260]
>
> Apple described its interest rate risk management strategy as using specific defensive actions, including derivative instruments, offsetting interest rate-sensitive assets and liabilities, and controlling the duration of the investment and term debt portfolios. [AAPL FY2023, Item 7A, AAPL_FY2023_2023-09-30:147]  
> Apple also stated that, to protect its term debt or marketable securities from fluctuations in interest rates, it may use interest rate swaps, options, or other instruments, and it designates these instruments as either cash flow or fair value hedges. [AAPL FY2023, Item 8, AAPL_FY2023_2023-09-30:204]  
> In addition, Apple disclosed that to manage interest rate risk on certain of its U.S. dollar-denominated fixed-rate notes, it uses interest rate swaps to effectively convert the fixed interest rates to floating interest rates on a portion of these notes. [AAPL FY2023, Item 8, AAPL_FY2023_2023-09-30:246]
>
> So, the key difference is that Alphabet’s 2023 filing described interest rate risk management primarily through a VaR-based analytical framework for assessing potential portfolio losses, while Apple’s 2023 filing described concrete hedging tools and portfolio defenses such as interest rate swaps, options, duration control, and asset-liability offsets. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:260] [AAPL FY2023, Item 7A, AAPL_FY2023_2023-09-30:147] [AAPL FY2023, Item 8, AAPL_FY2023_2023-09-30:204] [AAPL FY2023, Item 8, AAPL_FY2023_2023-09-30:246]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2023_2023-12-31:260` | Item 7A › Interest Rate Risk | ✓ | #1 | Table of Contents Alphabet Inc. We use value-at-risk (VaR) analysis to determine the potential effect of fluctuations in interest rates on the value of our marketable debt security portfolio. The VaR is the expected loss… |
| 2 | `GOOGL_FY2023_2023-12-31:261` | Item 7A › Interest Rate Risk |  |  | \| \| As of December 31, \| \| 12-Month Average As of December 31, \| \| \|---\|---\|---\|---\|---\| \| \| 2022 \| 2023 \| 2022 \| 2023 \| \| Risk category - interest rate \| $256 \| $296 \| $198 \| $271 \| |
| 3 | `GOOGL_FY2023_2023-12-31:401` | Item 8 › Long-Term Debt |  |  | \| \| \| \| Effective Interest Rate \| As of December 31, \| \| \|---\|---\|---\|---\|---\|---\| \| \| Maturity \| Coupon Rate \| 2022 \| 2023 \| \| \| Debt \| \| \| \| \| \| \| 2014-2020 Notes issuances \| 2024 - 2060 \| 0.45% - 3.38% \| 0.57% - 3.38%… |
| 4 | `GOOGL_FY2023_2023-12-31:15` | TABLE OF CONTENTS |  |  | \| \| \| Page \| \|---\|---\|---\| \| Note About Forward-Looking Statements \| \| 3 \| \| PART I \| \| \| \| Item 1. \| Business \| 4 \| \| Item 1A. \| Risk Factors \| 11 \| \| Item 1B. \| Unresolved Staff Comments \| 24 \| \| Item 1C. \| Cybersecuri… |
| 5 | `GOOGL_FY2023_2023-12-31:221` | Item 7 › Other Income (Expense), Net |  |  | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2022 \| 2023 \| \| Interest income \| $2,174 \| $3,865 \| \| Interest expense \| (357) \| (308) \| \| Foreign currency exchange gain (loss), net \| (654) \| (1,238) \| \| Gain (loss) on… |
| 6 | `GOOGL_FY2023_2023-12-31:294` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2022 \| 2023 \| \| Repayments of debt \| (21,435) \| (54,068) \| (11,550) \| \| Proceeds from sale of interest in consolidated entities, net \| 310 \| 35 \| 8 \| \| Net c… |
| 7 | `AAPL_FY2023_2023-09-30:204` | Item 8 › Derivative Instruments and Hedging | ✓ | #2 | To protect the Company’s foreign currency–denominated term debt or marketable securities from fluctuations in foreign exchange rates, the Company may use forwards, cross-currency swaps or other instruments. The Company d… |
| 8 | `AAPL_FY2023_2023-09-30:148` | Item 7A › Interest Rate Risk |  |  | \| Interest Rate Sensitive Instrument \| Hypothetical Interest Rate Increase \| Potential Impact \| 2023 \| 2022 \| \|---\|---\|---\|---\|---\| \| Investment portfolio \| 100 basis points, all tenors \| Decline in fair value \| $3,089 \|… |
| 9 | `AAPL_FY2023_2023-09-30:146` | Item 7A |  |  | The Company is exposed to economic risk from interest rates and foreign exchange rates. The Company uses various strategies to manage these risks; however, they may still impact the Company’s consolidated financial state… |
| 10 | `AAPL_FY2023_2023-09-30:147` | Item 7A › Interest Rate Risk | ✓ | #2 | The Company is primarily exposed to fluctuations in U.S. interest rates and their impact on the Company’s investment portfolio and term debt. Increases in interest rates will negatively affect the fair value of the Compa… |
| 11 | `AAPL_FY2023_2023-09-30:207` | Item 8 › Derivative Instruments and Hedging |  |  | \| \| 2022 \| \| \| \|---\|---\|---\|---\| \| \| Fair Value of Derivatives Designated as Accounting Hedges \| Fair Value of Derivatives Not Designated as Accounting Hedges \| Total Fair Value \| \| Derivative assets (1): \| \| \| \| \| Forei… |
| 12 | `AAPL_FY2023_2023-09-30:205` | Item 8 › Derivative Instruments and Hedging |  |  | \| \| 2023 \| 2022 \| \|---\|---\|---\| \| Derivative instruments designated as accounting hedges: \| \| \| \| Foreign exchange contracts \| $74,730 \| $102,670 \| \| Interest rate contracts \| $19,375 \| $20,125 \| \| Derivative instruments… |
| 13 | `AAPL_FY2023_2023-09-30:96` | Item 1A › The Company is exposed to credit risk and fluctuations in the values of its investment portfolio. |  |  | The Company’s investments can be negatively affected by changes in liquidity, credit deterioration, financial results, market and economic conditions, political risk, sovereign risk, interest rate fluctuations or other f… |
| 14 | `AAPL_FY2023_2023-09-30:246` | Item 8 › Term Debt | ✓ |  | To manage interest rate risk on certain of its U.S. dollar–denominated fixed-rate notes, the Company uses interest rate swaps to effectively convert the fixed interest rates to floating interest rates on a portion of the… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2023_2023-12-31:260`** (cited, gold #1)

````text
ITEM 7A.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK > Interest Rate Risk
Table of Contents Alphabet Inc. We use value-at-risk (VaR) analysis to determine the potential effect of fluctuations in interest rates on the value of our marketable debt security portfolio. The VaR is the expected loss in fair value, for a given confidence interval, for our investment portfolio due to adverse movements in interest rates. We use a variance/covariance VaR model with 95% confidence interval. The estimated one-day loss in fair value of marketable debt securities as of December 31, 2022 and 2023 are shown below (in millions):
````

**#7 `AAPL_FY2023_2023-09-30:204`** (cited, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Derivative Instruments and Hedging
To protect the Company’s foreign currency–denominated term debt or marketable securities from fluctuations in foreign exchange rates, the Company may use forwards, cross-currency swaps or other instruments. The Company designates these instruments as either cash flow or fair value hedges. As of September 30, 2023, the maximum length of time over which the Company is hedging its exposure to the variability in future cash flows for term debt–related foreign currency transactions is 19 years. The Company may also use derivative instruments that are not designated as accounting hedges to protect gross margins from certain fluctuations in foreign exchange rates, as well as to offset a portion of the foreign currency gains and losses generated by the remeasurement of certain assets and liabilities denominated in non-functional currencies. Interest Rate Risk To protect the Company’s term debt or marketable securities from fluctuations in interest rates, the Company may use interest rate swaps, options or other instruments. The Company designates these instruments as either cash flow or fair value hedges. The notional amounts of the Company’s outstanding derivative instruments as of September 30, 2023 and September 24, 2022 were as follows (in millions):
````

**#10 `AAPL_FY2023_2023-09-30:147`** (cited, gold #2)

````text
Item 7A. Quantitative and Qualitative Disclosures About Market Risk > Interest Rate Risk
The Company is primarily exposed to fluctuations in U.S. interest rates and their impact on the Company’s investment portfolio and term debt. Increases in interest rates will negatively affect the fair value of the Company’s investment portfolio and increase the interest expense on the Company’s term debt. To protect against interest rate risk, the Company may use derivative instruments, offset interest rate–sensitive assets and liabilities, or control duration of the investment and term debt portfolios. The following table sets forth potential impacts on the Company’s investment portfolio and term debt, including the effects of any associated derivatives, that would result from a hypothetical increase in relevant interest rates as of September 30, 2023 and September 24, 2022 (dollars in millions):
````

**#14 `AAPL_FY2023_2023-09-30:246`** (cited)

````text
Item 8. Financial Statements and Supplementary Data > Term Debt
To manage interest rate risk on certain of its U.S. dollar–denominated fixed-rate notes, the Company uses interest rate swaps to effectively convert the fixed interest rates to floating interest rates on a portion of these notes. Additionally, to manage foreign exchange rate risk on certain of its foreign currency–denominated notes, the Company uses cross-currency swaps to effectively convert these notes to U.S. dollar–denominated notes. The effective interest rates for the Notes include the interest on the Notes, amortization of the discount or premium and, if applicable, adjustments related to hedging. The Company recognized $3.7 billion, $2.8 billion and $2.6 billion of interest expense on its term debt for 2023, 2022 and 2021, respectively. The future principal payments for the Company’s Notes as of September 30, 2023, are as follows (in millions):
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 7A'), ('AAPL', 'Item 7A'), ('AAPL', 'Item 8')] gold=[(None, 'Item 7A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 1, verified 1, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 6, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Alphabet said it uses value-at-risk analysis to determine the potential effect of fluctuations in interest rates on the value of its marketable debt security portfolio, and it described VaR as the expected loss in fair value for a given confidence interval due to adverse movements in interest rates. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:260] | supported | The cited text states Alphabet uses VaR for its marketable debt securities and defines VaR as expected fair value loss at a given confidence interval from adverse interest-rate movements. |
| Alphabet further stated that it uses a variance/covariance VaR model with a 95% confidence interval. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:260] | None |  |
| Alphabet’s disclosure therefore emphasizes measurement of interest rate exposure through VaR on its marketable debt securities rather than identifying specific hedging instruments in the cited interest rate risk discussion. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:260] | supported | The cited discussion focuses on VaR measurement of interest-rate exposure and does not identify any specific hedging instruments. |
| Apple described its interest rate risk management strategy as using specific defensive actions, including derivative instruments, offsetting interest rate-sensitive assets and liabilities, and controlling the duration of the investment and term debt portfolios. [AAPL FY2023, Item 7A, AAPL_FY2023_2023-09-30:147] | supported | The evidence says Apple may use derivative instruments, offset interest rate-sensitive assets and liabilities, and control duration to protect against interest rate risk. |
| Apple also stated that, to protect its term debt or marketable securities from fluctuations in interest rates, it may use interest rate swaps, options, or other instruments, and it designates these instruments as either cash flow or fair value hedges. [AAPL FY2023, Item 8, AAPL_FY2023_2023-09-30:204] | supported | The cited passage explicitly says Apple may use interest rate swaps, options, or other instruments for interest-rate fluctuations and designates them as cash flow or fair value hedges. |
| In addition, Apple disclosed that to manage interest rate risk on certain of its U.S. dollar-denominated fixed-rate notes, it uses interest rate swaps to effectively convert the fixed interest rates to floating interest rates on a portion of these notes. [AAPL FY2023, Item 8, AAPL_FY2023_2023-09-30:246] | supported | The evidence directly states Apple uses interest rate swaps on certain U.S. dollar fixed-rate notes to effectively convert fixed rates to floating rates. |
| So, the key difference is that Alphabet’s 2023 filing described interest rate risk management primarily through a VaR-based analytical framework for assessing potential portfolio losses, while Apple’s 2023 filing described concrete hedging tools and portfolio defenses such as interest rate swaps, options, duration control, and asset-liability offsets. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:260] [AAPL FY2023, Item 7A, AAPL_FY2023_2023-09-30:147] [AAPL FY2023, Item 8, AAPL_FY2023_2023-09-30:204] [AAPL FY2023, Item 8, AAPL_FY2023_2023-09-30:246] | supported | The cited evidence supports that Alphabet describes interest-rate risk via a VaR assessment framework, while Apple describes specific hedging tools and defensive measures including swaps, options, duration control, and asset-liability offsets. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 14, cited: 5.

**Generated answer**

> Alphabet said it uses value-at-risk (VaR) analysis to determine the potential effect of fluctuations in interest rates on the value of its marketable debt security portfolio, and it defined VaR as the expected loss in fair value, for a given confidence interval, due to adverse movements in interest rates. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:260] Alphabet also said it uses a variance/covariance VaR model with a 95% confidence interval. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:260]
>
> Apple described its interest rate risk management in terms of specific protective actions and instruments. [AAPL FY2023, Item 7A, AAPL_FY2023_2023-09-30:147] [AAPL FY2023, Item 8, AAPL_FY2023_2023-09-30:203] Apple said it is primarily exposed to fluctuations in U.S. interest rates affecting its investment portfolio and term debt, and that to protect against interest rate risk it may use derivative instruments, offset interest rate-sensitive assets and liabilities, or control duration of the investment and term debt portfolios. [AAPL FY2023, Item 7A, AAPL_FY2023_2023-09-30:147] Apple also said it may use interest rate swaps, options or other instruments to protect its term debt or marketable securities from fluctuations in interest rates, and designates these instruments as either cash flow or fair value hedges. [AAPL FY2023, Item 8, AAPL_FY2023_2023-09-30:204] In addition, Apple specifically disclosed that it uses interest rate swaps to effectively convert fixed interest rates to floating interest rates on a portion of certain U.S. dollar-denominated fixed-rate notes. [AAPL FY2023, Item 8, AAPL_FY2023_2023-09-30:246]
>
> The difference in description is that Alphabet presented interest rate risk through a VaR measurement framework, while Apple described defensive measures such as derivative instruments, interest rate swaps, options, offsetting interest rate-sensitive assets and liabilities, and duration control. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:260] [AAPL FY2023, Item 7A, AAPL_FY2023_2023-09-30:147] [AAPL FY2023, Item 8, AAPL_FY2023_2023-09-30:204] [AAPL FY2023, Item 8, AAPL_FY2023_2023-09-30:246]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2023_2023-12-31:260` | Item 7A › Interest Rate Risk | ✓ | #1 | Table of Contents Alphabet Inc. We use value-at-risk (VaR) analysis to determine the potential effect of fluctuations in interest rates on the value of our marketable debt security portfolio. The VaR is the expected loss… |
| 2 | `GOOGL_FY2023_2023-12-31:261` | Item 7A › Interest Rate Risk |  |  | \| \| As of December 31, \| \| 12-Month Average As of December 31, \| \| \|---\|---\|---\|---\|---\| \| \| 2022 \| 2023 \| 2022 \| 2023 \| \| Risk category - interest rate \| $256 \| $296 \| $198 \| $271 \| |
| 3 | `GOOGL_FY2023_2023-12-31:401` | Item 8 › Long-Term Debt |  |  | \| \| \| \| Effective Interest Rate \| As of December 31, \| \| \|---\|---\|---\|---\|---\|---\| \| \| Maturity \| Coupon Rate \| 2022 \| 2023 \| \| \| Debt \| \| \| \| \| \| \| 2014-2020 Notes issuances \| 2024 - 2060 \| 0.45% - 3.38% \| 0.57% - 3.38%… |
| 4 | `GOOGL_FY2023_2023-12-31:15` | TABLE OF CONTENTS |  |  | \| \| \| Page \| \|---\|---\|---\| \| Note About Forward-Looking Statements \| \| 3 \| \| PART I \| \| \| \| Item 1. \| Business \| 4 \| \| Item 1A. \| Risk Factors \| 11 \| \| Item 1B. \| Unresolved Staff Comments \| 24 \| \| Item 1C. \| Cybersecuri… |
| 5 | `GOOGL_FY2023_2023-12-31:221` | Item 7 › Other Income (Expense), Net |  |  | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2022 \| 2023 \| \| Interest income \| $2,174 \| $3,865 \| \| Interest expense \| (357) \| (308) \| \| Foreign currency exchange gain (loss), net \| (654) \| (1,238) \| \| Gain (loss) on… |
| 6 | `GOOGL_FY2023_2023-12-31:294` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2022 \| 2023 \| \| Repayments of debt \| (21,435) \| (54,068) \| (11,550) \| \| Proceeds from sale of interest in consolidated entities, net \| 310 \| 35 \| 8 \| \| Net c… |
| 7 | `AAPL_FY2023_2023-09-30:146` | Item 7A |  |  | The Company is exposed to economic risk from interest rates and foreign exchange rates. The Company uses various strategies to manage these risks; however, they may still impact the Company’s consolidated financial state… |
| 8 | `AAPL_FY2023_2023-09-30:148` | Item 7A › Interest Rate Risk |  |  | \| Interest Rate Sensitive Instrument \| Hypothetical Interest Rate Increase \| Potential Impact \| 2023 \| 2022 \| \|---\|---\|---\|---\|---\| \| Investment portfolio \| 100 basis points, all tenors \| Decline in fair value \| $3,089 \|… |
| 9 | `AAPL_FY2023_2023-09-30:204` | Item 8 › Derivative Instruments and Hedging | ✓ | #2 | To protect the Company’s foreign currency–denominated term debt or marketable securities from fluctuations in foreign exchange rates, the Company may use forwards, cross-currency swaps or other instruments. The Company d… |
| 10 | `AAPL_FY2023_2023-09-30:96` | Item 1A › The Company is exposed to credit risk and fluctuations in the values of its investment portfolio. |  |  | The Company’s investments can be negatively affected by changes in liquidity, credit deterioration, financial results, market and economic conditions, political risk, sovereign risk, interest rate fluctuations or other f… |
| 11 | `AAPL_FY2023_2023-09-30:147` | Item 7A › Interest Rate Risk | ✓ | #2 | The Company is primarily exposed to fluctuations in U.S. interest rates and their impact on the Company’s investment portfolio and term debt. Increases in interest rates will negatively affect the fair value of the Compa… |
| 12 | `AAPL_FY2023_2023-09-30:196` | Item 8 › Cash, Cash Equivalents and Marketable Securities |  |  | \| \| 2023 \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Adjusted Cost \| Unrealized Gains \| Unrealized Losses \| Fair Value \| Cash and Cash Equivalents \| Current Marketable Securities \| Non-Current Marketable Securiti… |
| 13 | `AAPL_FY2023_2023-09-30:203` | Item 8 › Derivative Instruments and Hedging | ✓ |  | The Company may use derivative instruments to partially offset its business exposure to foreign exchange and interest rate risk. However, the Company may choose not to hedge certain exposures for a variety of reasons inc… |
| 14 | `AAPL_FY2023_2023-09-30:246` | Item 8 › Term Debt | ✓ |  | To manage interest rate risk on certain of its U.S. dollar–denominated fixed-rate notes, the Company uses interest rate swaps to effectively convert the fixed interest rates to floating interest rates on a portion of the… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2023_2023-12-31:260`** (cited, gold #1)

````text
ITEM 7A.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK > Interest Rate Risk
Table of Contents Alphabet Inc. We use value-at-risk (VaR) analysis to determine the potential effect of fluctuations in interest rates on the value of our marketable debt security portfolio. The VaR is the expected loss in fair value, for a given confidence interval, for our investment portfolio due to adverse movements in interest rates. We use a variance/covariance VaR model with 95% confidence interval. The estimated one-day loss in fair value of marketable debt securities as of December 31, 2022 and 2023 are shown below (in millions):
````

**#9 `AAPL_FY2023_2023-09-30:204`** (cited, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Derivative Instruments and Hedging
To protect the Company’s foreign currency–denominated term debt or marketable securities from fluctuations in foreign exchange rates, the Company may use forwards, cross-currency swaps or other instruments. The Company designates these instruments as either cash flow or fair value hedges. As of September 30, 2023, the maximum length of time over which the Company is hedging its exposure to the variability in future cash flows for term debt–related foreign currency transactions is 19 years. The Company may also use derivative instruments that are not designated as accounting hedges to protect gross margins from certain fluctuations in foreign exchange rates, as well as to offset a portion of the foreign currency gains and losses generated by the remeasurement of certain assets and liabilities denominated in non-functional currencies. Interest Rate Risk To protect the Company’s term debt or marketable securities from fluctuations in interest rates, the Company may use interest rate swaps, options or other instruments. The Company designates these instruments as either cash flow or fair value hedges. The notional amounts of the Company’s outstanding derivative instruments as of September 30, 2023 and September 24, 2022 were as follows (in millions):
````

**#11 `AAPL_FY2023_2023-09-30:147`** (cited, gold #2)

````text
Item 7A. Quantitative and Qualitative Disclosures About Market Risk > Interest Rate Risk
The Company is primarily exposed to fluctuations in U.S. interest rates and their impact on the Company’s investment portfolio and term debt. Increases in interest rates will negatively affect the fair value of the Company’s investment portfolio and increase the interest expense on the Company’s term debt. To protect against interest rate risk, the Company may use derivative instruments, offset interest rate–sensitive assets and liabilities, or control duration of the investment and term debt portfolios. The following table sets forth potential impacts on the Company’s investment portfolio and term debt, including the effects of any associated derivatives, that would result from a hypothetical increase in relevant interest rates as of September 30, 2023 and September 24, 2022 (dollars in millions):
````

**#13 `AAPL_FY2023_2023-09-30:203`** (cited)

````text
Item 8. Financial Statements and Supplementary Data > Derivative Instruments and Hedging
The Company may use derivative instruments to partially offset its business exposure to foreign exchange and interest rate risk. However, the Company may choose not to hedge certain exposures for a variety of reasons including accounting considerations or the prohibitive economic cost of hedging particular exposures. There can be no assurance the hedges will offset more than a portion of the financial impact resulting from movements in foreign exchange or interest rates. The Company classifies cash flows related to derivative instruments in the same section of the Consolidated Statements of Cash Flows as the items being hedged, which are generally classified as operating activities. Foreign Exchange Rate Risk To protect gross margins from fluctuations in foreign exchange rates, the Company may use forwards, options or other instruments, and may designate these instruments as cash flow hedges. The Company generally hedges portions of its forecasted foreign currency exposure associated with revenue and inventory purchases, typically for up to 12 months.
````

**#14 `AAPL_FY2023_2023-09-30:246`** (cited)

````text
Item 8. Financial Statements and Supplementary Data > Term Debt
To manage interest rate risk on certain of its U.S. dollar–denominated fixed-rate notes, the Company uses interest rate swaps to effectively convert the fixed interest rates to floating interest rates on a portion of these notes. Additionally, to manage foreign exchange rate risk on certain of its foreign currency–denominated notes, the Company uses cross-currency swaps to effectively convert these notes to U.S. dollar–denominated notes. The effective interest rates for the Notes include the interest on the Notes, amortization of the discount or premium and, if applicable, adjustments related to hedging. The Company recognized $3.7 billion, $2.8 billion and $2.6 billion of interest expense on its term debt for 2023, 2022 and 2021, respectively. The future principal payments for the Company’s Notes as of September 30, 2023, are as follows (in millions):
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 7A'), ('AAPL', 'Item 7A'), ('AAPL', 'Item 8')] gold=[(None, 'Item 7A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 1, verified 1, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 6, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Alphabet said it uses value-at-risk (VaR) analysis to determine the potential effect of fluctuations in interest rates on the value of its marketable debt security portfolio, and it defined VaR as the expected loss in fair value, for a given confidence interval, due to adverse movements in interest rates. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:260] | supported | The cited Alphabet text states it uses VaR for interest-rate effects on its marketable debt securities and defines VaR as expected loss in fair value for a given confidence interval due to adverse interest-rate movements. |
| Alphabet also said it uses a variance/covariance VaR model with a 95% confidence interval. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:260] | None |  |
| Apple described its interest rate risk management in terms of specific protective actions and instruments. [AAPL FY2023, Item 7A, AAPL_FY2023_2023-09-30:147] [AAPL FY2023, Item 8, AAPL_FY2023_2023-09-30:203] | supported | The Apple citations describe interest rate risk management using specific protective actions and instruments, including derivatives, offsetting assets and liabilities, duration control, and hedging instruments. |
| Apple said it is primarily exposed to fluctuations in U.S. interest rates affecting its investment portfolio and term debt, and that to protect against interest rate risk it may use derivative instruments, offset interest rate-sensitive assets and liabilities, or control duration of the investment and term debt portfolios. [AAPL FY2023, Item 7A, AAPL_FY2023_2023-09-30:147] | supported | The cited Item 7A passage states both Apple’s primary exposure to U.S. interest rates affecting its investment portfolio and term debt and the listed protective measures. |
| Apple also said it may use interest rate swaps, options or other instruments to protect its term debt or marketable securities from fluctuations in interest rates, and designates these instruments as either cash flow or fair value hedges. [AAPL FY2023, Item 8, AAPL_FY2023_2023-09-30:204] | supported | The cited Item 8 passage explicitly says Apple may use interest rate swaps, options or other instruments to protect term debt or marketable securities from interest-rate fluctuations and designates them as cash flow or fair value hedges. |
| In addition, Apple specifically disclosed that it uses interest rate swaps to effectively convert fixed interest rates to floating interest rates on a portion of certain U.S. dollar-denominated fixed-rate notes. [AAPL FY2023, Item 8, AAPL_FY2023_2023-09-30:246] | supported | The cited term debt note says Apple uses interest rate swaps to convert fixed rates to floating rates on a portion of certain U.S. dollar-denominated fixed-rate notes. |
| The difference in description is that Alphabet presented interest rate risk through a VaR measurement framework, while Apple described defensive measures such as derivative instruments, interest rate swaps, options, offsetting interest rate-sensitive assets and liabilities, and duration control. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:260] [AAPL FY2023, Item 7A, AAPL_FY2023_2023-09-30:147] [AAPL FY2023, Item 8, AAPL_FY2023_2023-09-30:204] [AAPL FY2023, Item 8, AAPL_FY2023_2023-09-30:246] | supported | The cited evidence shows Alphabet framed interest rate risk with VaR, while Apple described protective measures including derivatives, swaps, options, offsetting assets/liabilities, and duration control. |

</details>
