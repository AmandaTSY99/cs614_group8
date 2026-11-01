# gold-022: Single-hop text

[← all cases](../README.md) · company: MICROSOFT CORP (MSFT) · fiscal year: 2019 · recipe `text` · hop `single` · answer type `qualitative` · scope `single_doc` · RQ2 category `single_hop_factual`

## Gold QA

**Question**

> According to Microsoft's fiscal year 2019 10-K, what valuation methodology does the company use for its Level 3 investments?

**Gold answer**

> Microsoft values its Level 3 investments using internally-developed models with unobservable inputs.

**Key points** (RQ3 keypoint_recall targets)

1. Level 3 investments
2. internally-developed models
3. unobservable inputs

**Gold evidence**

1. `MSFT_FY2019_2019-06-30` · Item 7 › Valuation · text

   > Level 3 investments are valued using internally-developed models with unobservable inputs.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 6 |
| recall@5 | 0.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 0.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 0 | 1 | 1 | 1 |
| average precision (lexical) | 0.00 | 1.00 | 1.00 | 1.00 |
| gold evidence first rank | #1: – | #1: 1 | #1: 1 | #1: 1 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✓ | ✓ | ✓ |
| keypoint_recall | 0.00 | 1.00 | 1.00 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | – | 0.50 | 0.50 | 0.50 |
| citation recall | – | 1.00 | 1.00 | 1.00 |
| citation F1 | – | 0.67 | 0.67 | 0.67 |
| has a citation | 0 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 2711 | 1311 | 5453 | 5895 |
| cost (USD) | 0.0004 | 0.0002 | 0.0204 | 0.0213 |
| latency (s) | 1.4 | 6.0 | 9.0 | 9.7 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2019_2019-06-30:330` | Item 8 › Investment Components |  |  | \| (In millions) \| Fair Value Level \| Cost Basis \| Unrealized Gains \| Unrealized Losses \| Recorded Basis \| Cash and Cash Equivalents \| Short-term Investments \| Equity Investments \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| … |
| 2 | `MSFT_FY2019_2019-06-30:329` | Item 8 › Investment Components |  |  | \| (In millions) \| Fair Value Level \| Cost Basis \| Unrealized Gains \| Unrealized Losses \| Recorded Basis \| Cash and Cash Equivalents \| Short-term Investments \| Equity Investments \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| … |
| 3 | `MSFT_FY2019_2019-06-30:332` | Item 8 › PART II |  |  | \| (In millions) \| Fair Value Level \| Cost Basis \| Unrealized Gains \| Unrealized Losses \| Recorded Basis \| Cash and Cash Equivalents \| Short-term Investments \| Equity Investments \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| … |
| 4 | `MSFT_FY2019_2019-06-30:333` | Item 8 › PART II |  |  | \| (In millions) \| Fair Value Level \| Cost Basis \| Unrealized Gains \| Unrealized Losses \| Recorded Basis \| Cash and Cash Equivalents \| Short-term Investments \| Equity Investments \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| … |
| 5 | `MSFT_FY2019_2019-06-30:328` | Item 8 › Investment Components |  |  | \| (In millions) \| Fair Value Level \| Cost Basis \| Unrealized Gains \| Unrealized Losses \| Recorded Basis \| Cash and Cash Equivalents \| Short-term Investments \| Equity Investments \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| … |
| 6 | `MSFT_FY2019_2019-06-30:331` | Item 8 › PART II |  |  | \| (In millions) \| Fair Value Level \| Cost Basis \| Unrealized Gains \| Unrealized Losses \| Recorded Basis \| Cash and Cash Equivalents \| Short-term Investments \| Equity Investments \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| … |
| 7 | `MSFT_FY2019_2019-06-30:264` | Item 8 › BALANCE SHEETS |  |  | \| (In millions) \| \| \| \|---\|---\|---\| \| June 30, \| 2019 \| 2018 \| \| Assets \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $11,356 \| $11,946 \| \| Short-term investments \| 122,463 \| 121,822 \| \| Total cash, cash eq… |
| 8 | `MSFT_FY2019_2019-06-30:339` | Item 8 › Debt Investment Maturities |  |  | \| (In millions) \| Cost Basis \| Estimated Fair Value \| \|---\|---\|---\| \| June 30, 2019 \| \| \| \| Due in one year or less \| $53,200 \| $53,124 \| \| Due after one year through five years \| 47,016 \| 47,783 \| \| Due after five years… |
| 9 | `MSFT_FY2019_2019-06-30:372` | Item 8 › PART II |  |  | \| (In millions) \| \| \|---\|---\| \| Cash and cash equivalents \| $1,328 \| \| Short-term investments \| 2,110 \| \| Other current assets \| 697 \| \| Property and equipment \| 1,529 \| \| Intangible assets \| 7,887 \| \| Goodwill (a) \| 16,… |
| 10 | `MSFT_FY2019_2019-06-30:351` | Item 8 › Fair Values of Derivative Instruments |  |  | \| (In millions) \| Level 1 \| Level 2 \| Level 3 \| Total \| \|---\|---\|---\|---\|---\| \| June 30, 2019 \| \| \| \| \| \| Derivative assets \| $0 \| $247 \| $3 \| $250 \| \| Derivative liabilities \| 0 \| (272) \| 0 \| (272) \| \| June 30, 2018 \| \|… |

RQ2 citation match (section level): `no citations`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Microsoft states that its Level 3 investments are valued using internally developed models with unobservable inputs. It also says these fair values are determined using model-based techniques, including option pricing models and discounted cash flow models. [1][2]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2019_2019-06-30:222` | Item 7 › Valuation | ✓ | #1 | In general, and where applicable, we use quoted prices in active markets for identical assets or liabilities to determine the fair value of our financial instruments. This pricing methodology applies to our Level 1 inves… |
| 2 | `MSFT_FY2019_2019-06-30:306` | Item 8 › PART II | ✓ | #1 | • Level 3 – inputs are generally unobservable and typically reflect management’s estimates of assumptions that market participants would use in pricing the asset or liability. The fair values are therefore determined usi… |
| 3 | `MSFT_FY2019_2019-06-30:525` | Item 16 › SIGNATURES |  |  | Pursuant to the requirements of Section 13 or 15(d) of the Securities Exchange Act of 1934, the Registrant has duly caused this report to be signed on its behalf by the undersigned; thereunto duly authorized, in the City… |
| 4 | `MSFT_FY2019_2019-06-30:518` | Item 15 › PART IV |  |  | \| \| \| Incorporated by Reference \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| Exhibit Number \| Exhibit Description \| Filed Herewith \| Form \| Period Ending \| Exhibit \| Filing Date \| \| 4.15 \| Twelfth Supplemental Indenture for… |
| 5 | `MSFT_FY2019_2019-06-30:223` | Item 7 › Valuation |  |  | A majority of our investments are priced by pricing vendors and are generally Level 1 or Level 2 investments as these vendors either provide a quoted market price in an active market or use observable inputs for their pr… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `MSFT_FY2019_2019-06-30:222`** (cited, gold #1)

````text
Item 7 > Valuation
In general, and where applicable, we use quoted prices in active markets for identical assets or liabilities to determine the fair value of our financial instruments. This pricing methodology applies to our Level 1 investments, such as U.S. government securities, common and preferred stock, and mutual funds. If quoted prices in active markets for identical assets or liabilities are not available to determine fair value, then we use quoted prices for similar assets and liabilities or inputs other than the quoted prices that are observable either directly or indirectly. This pricing methodology applies to our Level 2 investments, such as commercial paper, certificates of deposit, U.S. agency securities, foreign government bonds, mortgage- and asset-backed securities, corporate notes and bonds, and municipal securities. Level 3 investments are valued using internally-developed models with unobservable inputs. Assets and liabilities measured at fair value on a recurring basis using unobservable inputs are an immaterial portion of our portfolio.
````

**#2 `MSFT_FY2019_2019-06-30:306`** (cited, gold #1)

````text
Item 8 > PART II
• Level 3 – inputs are generally unobservable and typically reflect management’s estimates of assumptions that market participants would use in pricing the asset or liability. The fair values are therefore determined using model-based techniques, including option pricing models and discounted cash flow models. Our Level 3 assets and liabilities include investments in corporate notes and bonds, and goodwill and intangible assets, when they are recorded at fair value due to an impairment charge. Unobservable inputs used in the models are significant to the fair values of the assets and liabilities. We measure equity investments without readily determinable fair values on a nonrecurring basis. The fair values of these investments are determined based on valuation techniques using the best information available, and may include quoted market prices, market comparables, and discounted cash flow projections. Our other current financial assets and current financial liabilities have fair values that approximate their carrying values.
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 7'), ('MSFT', 'Item 8')] gold=[(None, 'Item 7')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 2.

**Generated answer**

> Microsoft stated that Level 3 investments are valued using internally-developed models with unobservable inputs. [MSFT FY2019, Item 7, MSFT_FY2019_2019-06-30:222]
>
> It also said Level 3 inputs are generally unobservable and typically reflect management’s estimates of assumptions that market participants would use in pricing the asset or liability. [MSFT FY2019, Item 8, MSFT_FY2019_2019-06-30:306]
>
> Microsoft said the fair values for Level 3 assets and liabilities are determined using model-based techniques, including option pricing models and discounted cash flow models. [MSFT FY2019, Item 8, MSFT_FY2019_2019-06-30:306]
>
> For equity investments without readily determinable fair values that are measured on a nonrecurring basis, Microsoft said fair values are determined based on valuation techniques using the best information available, which may include quoted market prices, market comparables, and discounted cash flow projections. [MSFT FY2019, Item 8, MSFT_FY2019_2019-06-30:306]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2019_2019-06-30:222` | Item 7 › Valuation | ✓ | #1 | In general, and where applicable, we use quoted prices in active markets for identical assets or liabilities to determine the fair value of our financial instruments. This pricing methodology applies to our Level 1 inves… |
| 2 | `MSFT_FY2019_2019-06-30:306` | Item 8 › PART II | ✓ | #1 | • Level 3 – inputs are generally unobservable and typically reflect management’s estimates of assumptions that market participants would use in pricing the asset or liability. The fair values are therefore determined usi… |
| 3 | `MSFT_FY2019_2019-06-30:223` | Item 7 › Valuation |  |  | A majority of our investments are priced by pricing vendors and are generally Level 1 or Level 2 investments as these vendors either provide a quoted market price in an active market or use observable inputs for their pr… |
| 4 | `MSFT_FY2019_2019-06-30:305` | Item 8 › PART II |  |  | • Level 2 – inputs are based upon quoted prices for similar instruments in active markets, quoted prices for identical or similar instruments in markets that are not active, and model-based valuation techniques (e.g. the… |
| 5 | `MSFT_FY2019_2019-06-30:304` | Item 8 › Fair Value Measurements |  |  | We account for certain assets and liabilities at fair value. The hierarchy below lists three levels of fair value based on the extent to which inputs used in measuring fair value are observable in the market. We categori… |
| 6 | `MSFT_FY2019_2019-06-30:329` | Item 8 › Investment Components |  |  | \| (In millions) \| Fair Value Level \| Cost Basis \| Unrealized Gains \| Unrealized Losses \| Recorded Basis \| Cash and Cash Equivalents \| Short-term Investments \| Equity Investments \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `MSFT_FY2019_2019-06-30:222`** (cited, gold #1)

````text
Item 7 > Valuation
In general, and where applicable, we use quoted prices in active markets for identical assets or liabilities to determine the fair value of our financial instruments. This pricing methodology applies to our Level 1 investments, such as U.S. government securities, common and preferred stock, and mutual funds. If quoted prices in active markets for identical assets or liabilities are not available to determine fair value, then we use quoted prices for similar assets and liabilities or inputs other than the quoted prices that are observable either directly or indirectly. This pricing methodology applies to our Level 2 investments, such as commercial paper, certificates of deposit, U.S. agency securities, foreign government bonds, mortgage- and asset-backed securities, corporate notes and bonds, and municipal securities. Level 3 investments are valued using internally-developed models with unobservable inputs. Assets and liabilities measured at fair value on a recurring basis using unobservable inputs are an immaterial portion of our portfolio.
````

**#2 `MSFT_FY2019_2019-06-30:306`** (cited, gold #1)

````text
Item 8 > PART II
• Level 3 – inputs are generally unobservable and typically reflect management’s estimates of assumptions that market participants would use in pricing the asset or liability. The fair values are therefore determined using model-based techniques, including option pricing models and discounted cash flow models. Our Level 3 assets and liabilities include investments in corporate notes and bonds, and goodwill and intangible assets, when they are recorded at fair value due to an impairment charge. Unobservable inputs used in the models are significant to the fair values of the assets and liabilities. We measure equity investments without readily determinable fair values on a nonrecurring basis. The fair values of these investments are determined based on valuation techniques using the best information available, and may include quoted market prices, market comparables, and discounted cash flow projections. Our other current financial assets and current financial liabilities have fair values that approximate their carrying values.
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 7'), ('MSFT', 'Item 8')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 4, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Microsoft stated that Level 3 investments are valued using internally-developed models with unobservable inputs. [MSFT FY2019, Item 7, MSFT_FY2019_2019-06-30:222] | supported | The evidence states Level 3 investments are valued using internally-developed models with unobservable inputs. |
| It also said Level 3 inputs are generally unobservable and typically reflect management’s estimates of assumptions that market participants would use in pricing the asset or liability. [MSFT FY2019, Item 8, MSFT_FY2019_2019-06-30:306] | supported | The evidence explicitly says Level 3 inputs are generally unobservable and reflect management’s estimates of market participant assumptions. |
| Microsoft said the fair values for Level 3 assets and liabilities are determined using model-based techniques, including option pricing models and discounted cash flow models. [MSFT FY2019, Item 8, MSFT_FY2019_2019-06-30:306] | supported | The evidence states fair values for Level 3 assets and liabilities are determined using model-based techniques including option pricing and discounted cash flow models. |
| For equity investments without readily determinable fair values that are measured on a nonrecurring basis, Microsoft said fair values are determined based on valuation techniques using the best information available, which may include quoted market prices, market comparables, and discounted cash flow projections. [MSFT FY2019, Item 8, MSFT_FY2019_2019-06-30:306] | supported | The evidence explicitly says such nonrecurring equity investments are valued using the best information available, including quoted prices, comparables, and discounted cash flow projections. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 2.

**Generated answer**

> Microsoft states that Level 3 investments are valued using internally-developed models with unobservable inputs. [MSFT FY2019, Item 7, MSFT_FY2019_2019-06-30:222]
>
> The company also says Level 3 inputs are generally unobservable and typically reflect management’s estimates of assumptions that market participants would use in pricing the asset or liability. [MSFT FY2019, Item 8, MSFT_FY2019_2019-06-30:306]
>
> Microsoft says the fair values for Level 3 items are therefore determined using model-based techniques, including option pricing models and discounted cash flow models. [MSFT FY2019, Item 8, MSFT_FY2019_2019-06-30:306]
>
> For equity investments without readily determinable fair values that are measured on a nonrecurring basis, Microsoft says fair values are determined based on valuation techniques using the best information available, which may include quoted market prices, market comparables, and discounted cash flow projections. [MSFT FY2019, Item 8, MSFT_FY2019_2019-06-30:306]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2019_2019-06-30:222` | Item 7 › Valuation | ✓ | #1 | In general, and where applicable, we use quoted prices in active markets for identical assets or liabilities to determine the fair value of our financial instruments. This pricing methodology applies to our Level 1 inves… |
| 2 | `MSFT_FY2019_2019-06-30:306` | Item 8 › PART II | ✓ | #1 | • Level 3 – inputs are generally unobservable and typically reflect management’s estimates of assumptions that market participants would use in pricing the asset or liability. The fair values are therefore determined usi… |
| 3 | `MSFT_FY2019_2019-06-30:305` | Item 8 › PART II |  |  | • Level 2 – inputs are based upon quoted prices for similar instruments in active markets, quoted prices for identical or similar instruments in markets that are not active, and model-based valuation techniques (e.g. the… |
| 4 | `MSFT_FY2019_2019-06-30:329` | Item 8 › Investment Components |  |  | \| (In millions) \| Fair Value Level \| Cost Basis \| Unrealized Gains \| Unrealized Losses \| Recorded Basis \| Cash and Cash Equivalents \| Short-term Investments \| Equity Investments \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| … |
| 5 | `MSFT_FY2019_2019-06-30:328` | Item 8 › Investment Components |  |  | \| (In millions) \| Fair Value Level \| Cost Basis \| Unrealized Gains \| Unrealized Losses \| Recorded Basis \| Cash and Cash Equivalents \| Short-term Investments \| Equity Investments \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| … |
| 6 | `MSFT_FY2019_2019-06-30:332` | Item 8 › PART II |  |  | \| (In millions) \| Fair Value Level \| Cost Basis \| Unrealized Gains \| Unrealized Losses \| Recorded Basis \| Cash and Cash Equivalents \| Short-term Investments \| Equity Investments \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `MSFT_FY2019_2019-06-30:222`** (cited, gold #1)

````text
Item 7 > Valuation
In general, and where applicable, we use quoted prices in active markets for identical assets or liabilities to determine the fair value of our financial instruments. This pricing methodology applies to our Level 1 investments, such as U.S. government securities, common and preferred stock, and mutual funds. If quoted prices in active markets for identical assets or liabilities are not available to determine fair value, then we use quoted prices for similar assets and liabilities or inputs other than the quoted prices that are observable either directly or indirectly. This pricing methodology applies to our Level 2 investments, such as commercial paper, certificates of deposit, U.S. agency securities, foreign government bonds, mortgage- and asset-backed securities, corporate notes and bonds, and municipal securities. Level 3 investments are valued using internally-developed models with unobservable inputs. Assets and liabilities measured at fair value on a recurring basis using unobservable inputs are an immaterial portion of our portfolio.
````

**#2 `MSFT_FY2019_2019-06-30:306`** (cited, gold #1)

````text
Item 8 > PART II
• Level 3 – inputs are generally unobservable and typically reflect management’s estimates of assumptions that market participants would use in pricing the asset or liability. The fair values are therefore determined using model-based techniques, including option pricing models and discounted cash flow models. Our Level 3 assets and liabilities include investments in corporate notes and bonds, and goodwill and intangible assets, when they are recorded at fair value due to an impairment charge. Unobservable inputs used in the models are significant to the fair values of the assets and liabilities. We measure equity investments without readily determinable fair values on a nonrecurring basis. The fair values of these investments are determined based on valuation techniques using the best information available, and may include quoted market prices, market comparables, and discounted cash flow projections. Our other current financial assets and current financial liabilities have fair values that approximate their carrying values.
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 7'), ('MSFT', 'Item 8')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 4, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Microsoft states that Level 3 investments are valued using internally-developed models with unobservable inputs. [MSFT FY2019, Item 7, MSFT_FY2019_2019-06-30:222] | supported | The evidence explicitly states Level 3 investments are valued using internally-developed models with unobservable inputs. |
| The company also says Level 3 inputs are generally unobservable and typically reflect management’s estimates of assumptions that market participants would use in pricing the asset or liability. [MSFT FY2019, Item 8, MSFT_FY2019_2019-06-30:306] | supported | The evidence states Level 3 inputs are generally unobservable and reflect management’s estimates of market participant assumptions. |
| Microsoft says the fair values for Level 3 items are therefore determined using model-based techniques, including option pricing models and discounted cash flow models. [MSFT FY2019, Item 8, MSFT_FY2019_2019-06-30:306] | supported | The evidence explicitly says fair values are determined using model-based techniques including option pricing and discounted cash flow models. |
| For equity investments without readily determinable fair values that are measured on a nonrecurring basis, Microsoft says fair values are determined based on valuation techniques using the best information available, which may include quoted market prices, market comparables, and discounted cash flow projections. [MSFT FY2019, Item 8, MSFT_FY2019_2019-06-30:306] | supported | The evidence explicitly states this for equity investments without readily determinable fair values measured on a nonrecurring basis. |

</details>
