# gold-026: Cross-year text

[← all cases](../README.md) · company: JPMORGAN CHASE & CO (JPM) · fiscal year: 2023 · recipe `cross_year_text` · hop `multi` · answer type `qualitative` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> How did JPMorgan Chase's 2023 10-K disclosure regarding the impact of market conditions on its wholesale businesses change in specificity compared to its 2018 disclosure, particularly regarding the types of capital markets activities explicitly identified as vulnerable to reduced profitability?

**Gold answer**

> The 2023 10-K provides a more specific enumeration of capital markets activities vulnerable to reduced profitability under adverse market conditions, explicitly listing 'loan syndication, securities underwriting and leveraged lending activities.' In contrast, the 2018 10-K referred more generally to 'capital markets businesses' and 'capital markets transactions' without explicitly listing leveraged lending in that specific context of reduced profitability, though it did mention loan syndications and securities underwritings in the context of transaction volumes and disposal losses.

**Key points** (RQ3 keypoint_recall targets)

1. The 2023 disclosure explicitly includes 'leveraged lending activities' among the capital markets businesses vulnerable to reduced profitability.
2. The 2018 disclosure refers to 'capital markets businesses' generally and lists 'loan syndications or securities underwritings' in the context of disposal losses but does not list leveraged lending in the same specific profitability clause.
3. Both filings identify lower transaction volumes and reduced fee revenue as consequences of adverse market conditions.

**Gold evidence**

1. `JPM_FY2023_2023-12-31` · Item 1A. Risk Factors. › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. · text

   > the profitability of JPMorgan Chase’s businesses engaged in capital markets activities, including loan syndication, securities underwriting and leveraged lending activities, could be reduced

2. `JPM_FY2018_2018-12-31` · Item 1A. Risk Factors. › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. · text

   > the profitability of JPMorgan Chase’s capital markets businesses could be reduced to the extent that those businesses: • earn less fee revenue due to lower transaction volumes, including when clients are unwilling or unable to refinance their outstanding debt obligations in unfavorable market conditions • dispose of portions of credit commitments, such as loan syndications or securities underwritings, at a loss

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 9 | 5 | 8 | 17 |
| recall@5 | 1.00 | 1.00 | 1.00 | 0.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.75 | 0.83 | 1.00 | 0.11 |
| gold evidence first rank | #1: 1, #2: 1 | #1: 1, #2: 1 | #1: 1, #2: 1 | #1: 12, #2: 12 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | 0.67 | 0.67 | 1.00 | 0.67 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 2262 | 1166 | 19013 | 17601 |
| cost (USD) | 0.0004 | 0.0002 | 0.0772 | 0.0661 |
| latency (s) | 3.4 | 9.3 | 40.8 | 32.3 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 9, cited: 2.

**Generated answer**

> JPMorgan Chase’s 2023 disclosure became slightly more specific in naming the capital markets activities whose profitability could be hurt by deteriorating market conditions.
>
> - In the 2018 10-K, it said the profitability of its “capital markets businesses” could be reduced, and then discussed examples such as loan syndications and securities underwritings elsewhere in the paragraph, including losses on “credit commitments, such as loan syndications or securities underwritings.” [4]
> - In the 2023 10-K, it more explicitly identified the vulnerable businesses as those “engaged in capital markets activities, including loan syndication, securities underwriting and leveraged lending activities.” [1]
>
> So, compared with 2018, the 2023 disclosure was more specific because it directly listed the affected activities and added “leveraged lending activities” as an explicitly identified area vulnerable to reduced profitability. [1][4]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JPM_FY2023_2023-12-31:87` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. | ✓ | #1, #2 | In JPMorgan Chase’s wholesale businesses, market and economic factors can affect the volume of transactions that JPMorgan Chase executes for its clients or for which it advises clients, and, therefore, the revenue that J… |
| 2 | `JPM_FY2023_2023-12-31:83` | Item 1A › Economic and market events and conditions can materially affect JPMorgan Chase’s businesses and investment and market-making positions. |  |  | JPMorgan Chase’s results of operations can be negatively affected by adverse changes in any of the following: •investor, consumer and business sentiment •events that reduce confidence in the financial markets •inflation,… |
| 3 | `JPM_FY2018_2018-12-31:780` | Item 15 › Management’s discussion and analysis |  |  | All forward-looking statements are, by their nature, subject to risks and uncertainties, many of which are beyond the Firm’s control. JPMorgan Chase’s actual future results may differ materially from those set forth in i… |
| 4 | `JPM_FY2018_2018-12-31:77` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. | ✓ | #1, #2 | In JPMorgan Chase’s wholesale businesses, market and economic factors can affect the volume of transactions that JPMorgan Chase executes for its clients or for which it advises clients, and, therefore, the revenue that J… |
| 5 | `JPM_FY2018_2018-12-31:80` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. |  |  | An economic downturn that results in lower consumer and business spending could also have a negative impact on certain of JPMorgan Chase’s wholesale clients, and thereby diminish JPMorgan Chase’s earnings from its wholes… |
| 6 | `JPM_FY2018_2018-12-31:82` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. |  |  | • other market risks that may not have been appropriately taken into account in the development, structuring or pricing of a financial instrument. If JPMorgan Chase experiences significant losses in its investment securi… |
| 7 | `JPM_FY2023_2023-12-31:825` | Item 15 › Management’s discussion and analysis |  |  | All forward-looking statements are, by their nature, subject to risks and uncertainties, many of which are beyond the Firm’s control. JPMorgan Chase’s actual future results may differ materially from those set forth in i… |
| 8 | `JPM_FY2023_2023-12-31:192` | Item 7A |  |  | Refer to the Market Risk Management section of Management’s discussion and analysis on pages 135–143 for a discussion of quantitative and qualitative disclosures about market risk. |
| 9 | `JPM_FY2018_2018-12-31:81` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. |  |  | JPMorgan Chase generally maintains positions in various fixed income instruments in its investment securities portfolio, and positions in various fixed income, currency, commodity, credit and equity instruments as part o… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JPM_FY2023_2023-12-31:87`** (cited, gold #1, gold #2)

````text
Item 1A. Risk Factors. > Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses.
In JPMorgan Chase’s wholesale businesses, market and economic factors can affect the volume of transactions that JPMorgan Chase executes for its clients or for which it advises clients, and, therefore, the revenue that JPMorgan Chase receives from those transactions. These factors can also influence the willingness of other financial institutions and investors to participate in capital markets transactions that JPMorgan Chase manages, such as loan syndications or securities underwriting. Furthermore, if a significant and sustained deterioration in market conditions were to occur, the profitability of JPMorgan Chase’s businesses engaged in capital markets activities, including loan syndication, securities underwriting and leveraged lending activities, could be reduced to the extent that those businesses: •earn less fee revenue due to lower transaction volumes, including when clients are unwilling or unable to
````

**#4 `JPM_FY2018_2018-12-31:77`** (cited, gold #1, gold #2)

````text
Item 1A. Risk Factors. > Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses.
In JPMorgan Chase’s wholesale businesses, market and economic factors can affect the volume of transactions that JPMorgan Chase executes for its clients or for which it advises clients, and, therefore, the revenue that JPMorgan Chase receives from those transactions. These factors can also influence the willingness of other financial institutions and investors to participate in capital markets transactions that JPMorgan Chase manages, such as loan syndications or securities underwritings. Furthermore, if a significant and sustained deterioration in market conditions were to occur, the profitability of JPMorgan Chase’s capital markets businesses could be reduced to the extent that those businesses: • earn less fee revenue due to lower transaction volumes, including when clients are unwilling or unable to refinance their outstanding debt obligations in unfavorable market conditions • dispose of portions of credit commitments, such as loan syndications or securities underwritings, at a loss, or • hold larger residual positions in credit commitments that cannot be sold at favorable prices.
````

</details>

RQ2 citation match (section level): `cited=[('JPM', 'Item 1A')] gold=[(None, 'Item 1A')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> In 2023, JPMorgan Chase’s disclosure became more specific by explicitly naming the vulnerable capital markets activities as “loan syndication, securities underwriting and leveraged lending activities” [1].  
>
> In 2018, the disclosure was broader, referring generally to “capital markets businesses,” while describing examples such as “loan syndications or securities underwritings” in the discussion of transaction impacts, but not explicitly listing leveraged lending in the identified set of businesses whose profitability could be reduced [3].  
>
> So, compared with 2018, the 2023 disclosure added specificity by expressly identifying leveraged lending alongside loan syndication and securities underwriting as activities vulnerable to reduced profitability under deteriorating market conditions [1][3].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JPM_FY2023_2023-12-31:87` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. | ✓ | #1, #2 | In JPMorgan Chase’s wholesale businesses, market and economic factors can affect the volume of transactions that JPMorgan Chase executes for its clients or for which it advises clients, and, therefore, the revenue that J… |
| 2 | `JPM_FY2018_2018-12-31:82` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. |  |  | • other market risks that may not have been appropriately taken into account in the development, structuring or pricing of a financial instrument. If JPMorgan Chase experiences significant losses in its investment securi… |
| 3 | `JPM_FY2018_2018-12-31:77` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. | ✓ | #1, #2 | In JPMorgan Chase’s wholesale businesses, market and economic factors can affect the volume of transactions that JPMorgan Chase executes for its clients or for which it advises clients, and, therefore, the revenue that J… |
| 4 | `JPM_FY2018_2018-12-31:78` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. |  |  | An adverse change in market conditions in particular segments of the economy, such as a sudden and severe downturn in oil and gas prices or an increase in commodity prices, could have a material adverse effect on clients… |
| 5 | `JPM_FY2018_2018-12-31:79` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. |  |  | The fees that JPMorgan Chase earns from managing client assets or holding assets under custody for clients could be diminished by declining asset values or other adverse macroeconomic conditions. For example, higher inte… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JPM_FY2023_2023-12-31:87`** (cited, gold #1, gold #2)

````text
Item 1A. Risk Factors. > Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses.
In JPMorgan Chase’s wholesale businesses, market and economic factors can affect the volume of transactions that JPMorgan Chase executes for its clients or for which it advises clients, and, therefore, the revenue that JPMorgan Chase receives from those transactions. These factors can also influence the willingness of other financial institutions and investors to participate in capital markets transactions that JPMorgan Chase manages, such as loan syndications or securities underwriting. Furthermore, if a significant and sustained deterioration in market conditions were to occur, the profitability of JPMorgan Chase’s businesses engaged in capital markets activities, including loan syndication, securities underwriting and leveraged lending activities, could be reduced to the extent that those businesses: •earn less fee revenue due to lower transaction volumes, including when clients are unwilling or unable to
````

**#3 `JPM_FY2018_2018-12-31:77`** (cited, gold #1, gold #2)

````text
Item 1A. Risk Factors. > Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses.
In JPMorgan Chase’s wholesale businesses, market and economic factors can affect the volume of transactions that JPMorgan Chase executes for its clients or for which it advises clients, and, therefore, the revenue that JPMorgan Chase receives from those transactions. These factors can also influence the willingness of other financial institutions and investors to participate in capital markets transactions that JPMorgan Chase manages, such as loan syndications or securities underwritings. Furthermore, if a significant and sustained deterioration in market conditions were to occur, the profitability of JPMorgan Chase’s capital markets businesses could be reduced to the extent that those businesses: • earn less fee revenue due to lower transaction volumes, including when clients are unwilling or unable to refinance their outstanding debt obligations in unfavorable market conditions • dispose of portions of credit commitments, such as loan syndications or securities underwritings, at a loss, or • hold larger residual positions in credit commitments that cannot be sold at favorable prices.
````

</details>

RQ2 citation match (section level): `cited=[('JPM', 'Item 1A')] gold=[(None, 'Item 1A')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 8, cited: 2.

**Generated answer**

> JPMorgan Chase’s 2023 disclosure remained similar to its 2018 disclosure in stating that unfavorable market and economic conditions can reduce transaction volumes and revenue in its wholesale businesses, and that a significant and sustained deterioration in market conditions could reduce profitability and fee revenue. [JPM FY2023, Item 1A, JPM_FY2023_2023-12-31:87] [JPM FY2018, Item 1A, JPM_FY2018_2018-12-31:77]
>
> Compared with 2018, the 2023 filing was more specific in describing the affected businesses: in 2018 it referred to “JPMorgan Chase’s capital markets businesses,” while in 2023 it referred to “businesses engaged in capital markets activities, including loan syndication, securities underwriting and leveraged lending activities.” [JPM FY2023, Item 1A, JPM_FY2023_2023-12-31:87] [JPM FY2018, Item 1A, JPM_FY2018_2018-12-31:77]
>
> The 2018 filing mentioned loan syndications and securities underwritings as examples of capital markets transactions JPMorgan Chase manages and as credit commitments that might be disposed of at a loss, but it did not explicitly include leveraged lending activities in that profitability sentence. [JPM FY2018, Item 1A, JPM_FY2018_2018-12-31:77]
>
> So the added specificity in 2023 was the explicit identification of loan syndication, securities underwriting, and leveraged lending activities as capital markets activities whose profitability could be reduced by adverse market conditions. [JPM FY2023, Item 1A, JPM_FY2023_2023-12-31:87] [JPM FY2018, Item 1A, JPM_FY2018_2018-12-31:77]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JPM_FY2023_2023-12-31:87` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. | ✓ | #1, #2 | In JPMorgan Chase’s wholesale businesses, market and economic factors can affect the volume of transactions that JPMorgan Chase executes for its clients or for which it advises clients, and, therefore, the revenue that J… |
| 2 | `JPM_FY2018_2018-12-31:77` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. | ✓ | #1, #2 | In JPMorgan Chase’s wholesale businesses, market and economic factors can affect the volume of transactions that JPMorgan Chase executes for its clients or for which it advises clients, and, therefore, the revenue that J… |
| 3 | `JPM_FY2018_2018-12-31:80` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. |  |  | An economic downturn that results in lower consumer and business spending could also have a negative impact on certain of JPMorgan Chase’s wholesale clients, and thereby diminish JPMorgan Chase’s earnings from its wholes… |
| 4 | `JPM_FY2018_2018-12-31:82` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. |  |  | • other market risks that may not have been appropriately taken into account in the development, structuring or pricing of a financial instrument. If JPMorgan Chase experiences significant losses in its investment securi… |
| 5 | `JPM_FY2018_2018-12-31:81` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. |  |  | JPMorgan Chase generally maintains positions in various fixed income instruments in its investment securities portfolio, and positions in various fixed income, currency, commodity, credit and equity instruments as part o… |
| 6 | `JPM_FY2018_2018-12-31:78` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. |  |  | An adverse change in market conditions in particular segments of the economy, such as a sudden and severe downturn in oil and gas prices or an increase in commodity prices, could have a material adverse effect on clients… |
| 7 | `JPM_FY2018_2018-12-31:79` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. |  |  | The fees that JPMorgan Chase earns from managing client assets or holding assets under custody for clients could be diminished by declining asset values or other adverse macroeconomic conditions. For example, higher inte… |
| 8 | `JPM_FY2023_2023-12-31:57` | Item 1A › Summary |  |  | •Market risks, including the effects that economic and market events and conditions, governmental policies, changes in interest rates and credit spreads, and market fluctuations can have on JPMorgan Chase’s consumer and … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JPM_FY2023_2023-12-31:87`** (cited, gold #1, gold #2)

````text
Item 1A. Risk Factors. > Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses.
In JPMorgan Chase’s wholesale businesses, market and economic factors can affect the volume of transactions that JPMorgan Chase executes for its clients or for which it advises clients, and, therefore, the revenue that JPMorgan Chase receives from those transactions. These factors can also influence the willingness of other financial institutions and investors to participate in capital markets transactions that JPMorgan Chase manages, such as loan syndications or securities underwriting. Furthermore, if a significant and sustained deterioration in market conditions were to occur, the profitability of JPMorgan Chase’s businesses engaged in capital markets activities, including loan syndication, securities underwriting and leveraged lending activities, could be reduced to the extent that those businesses: •earn less fee revenue due to lower transaction volumes, including when clients are unwilling or unable to
````

**#2 `JPM_FY2018_2018-12-31:77`** (cited, gold #1, gold #2)

````text
Item 1A. Risk Factors. > Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses.
In JPMorgan Chase’s wholesale businesses, market and economic factors can affect the volume of transactions that JPMorgan Chase executes for its clients or for which it advises clients, and, therefore, the revenue that JPMorgan Chase receives from those transactions. These factors can also influence the willingness of other financial institutions and investors to participate in capital markets transactions that JPMorgan Chase manages, such as loan syndications or securities underwritings. Furthermore, if a significant and sustained deterioration in market conditions were to occur, the profitability of JPMorgan Chase’s capital markets businesses could be reduced to the extent that those businesses: • earn less fee revenue due to lower transaction volumes, including when clients are unwilling or unable to refinance their outstanding debt obligations in unfavorable market conditions • dispose of portions of credit commitments, such as loan syndications or securities underwritings, at a loss, or • hold larger residual positions in credit commitments that cannot be sold at favorable prices.
````

</details>

RQ2 citation match (section level): `cited=[('JPM', 'Item 1A')] gold=[(None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 4, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| JPMorgan Chase’s 2023 disclosure remained similar to its 2018 disclosure in stating that unfavorable market and economic conditions can reduce transaction volumes and revenue in its wholesale businesses, and that a significant and sustained deterioration in market conditions could reduce profitability and fee revenue. [JPM FY2023, Item 1A, JPM_FY2023_2023-12-31:87] [JPM FY2018, Item 1A, JPM_FY2018_2018-12-31:77] | supported | Both excerpts state reduced transaction volumes/revenue in wholesale businesses and reduced profitability/fee revenue under sustained market deterioration, supporting the similarity claim. |
| Compared with 2018, the 2023 filing was more specific in describing the affected businesses: in 2018 it referred to “JPMorgan Chase’s capital markets businesses,” while in 2023 it referred to “businesses engaged in capital markets activities, including loan syndication, securities underwriting and leveraged lending activities.” [JPM FY2023, Item 1A, JPM_FY2023_2023-12-31:87] [JPM FY2018, Item 1A, JPM_FY2018_2018-12-31:77] | supported | The 2018 excerpt uses 'capital markets businesses' while the 2023 excerpt more specifically names businesses engaged in capital markets activities including loan syndication, securities underwriting, and leveraged lending. |
| The 2018 filing mentioned loan syndications and securities underwritings as examples of capital markets transactions JPMorgan Chase manages and as credit commitments that might be disposed of at a loss, but it did not explicitly include leveraged lending activities in that profitability sentence. [JPM FY2018, Item 1A, JPM_FY2018_2018-12-31:77] | supported | The 2018 text mentions loan syndications and securities underwritings in both contexts cited and does not explicitly mention leveraged lending activities in that profitability sentence. |
| So the added specificity in 2023 was the explicit identification of loan syndication, securities underwriting, and leveraged lending activities as capital markets activities whose profitability could be reduced by adverse market conditions. [JPM FY2023, Item 1A, JPM_FY2023_2023-12-31:87] [JPM FY2018, Item 1A, JPM_FY2018_2018-12-31:77] | supported | The 2023 excerpt explicitly identifies loan syndication, securities underwriting, and leveraged lending activities in the profitability clause, whereas the 2018 excerpt does not. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 17, cited: 2.

**Generated answer**

> JPMorgan Chase’s 2018 disclosure said that, if market conditions significantly and sustainably deteriorated, “the profitability of JPMorgan Chase’s capital markets businesses could be reduced,” and it specifically tied that risk to loan syndications and securities underwritings, including the possibility of disposing of portions of credit commitments such as loan syndications or securities underwritings at a loss or holding larger residual positions that could not be sold at favorable prices [JPM FY2018, Item 1A, JPM_FY2018_2018-12-31:77].  
>
> In 2023, the disclosure became more specific by stating that “the profitability of JPMorgan Chase’s businesses engaged in capital markets activities, including loan syndication, securities underwriting and leveraged lending activities, could be reduced,” explicitly adding leveraged lending activities to the identified vulnerable activities [JPM FY2023, Item 1A, JPM_FY2023_2023-12-31:87].  
>
> So, compared with 2018, the 2023 10-K narrowed the discussion from the broader phrase “capital markets businesses” to businesses engaged in capital markets activities and expanded the explicit list of vulnerable activities from loan syndications and securities underwritings to loan syndication, securities underwriting, and leveraged lending activities [JPM FY2023, Item 1A, JPM_FY2023_2023-12-31:87] [JPM FY2018, Item 1A, JPM_FY2018_2018-12-31:77].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JPM_FY2023_2023-12-31:8` | Form 10-K Index |  |  | \| Part I \| \| Page \| \|---\|---\|---\| \| Item 7. \| Management’s Discussion and Analysis of Financial Condition and Results of Operations. \| 35 \| \| Item 7A. \| Quantitative and Qualitative Disclosures About Market Risk. \| 35 \| … |
| 2 | `JPM_FY2023_2023-12-31:826` | Item 15 › Management’s discussion and analysis |  |  | •Changes in credit ratings assigned to the Firm or its subsidiaries; •Damage to the Firm’s reputation; •Ability of the Firm to appropriately address social, environmental and sustainability concerns that may arise, inclu… |
| 3 | `JPM_FY2018_2018-12-31:179` | Item 7A |  |  | For a discussion of quantitative and qualitative disclosures about market risk, refer to the Market Risk Management section of Management’s discussion and analysis on pages 124–131. |
| 4 | `JPM_FY2023_2023-12-31:611` | Item 15 › Management’s discussion and analysis |  |  | The Firm’s wholesale credit portfolio includes exposure held in CIB, CB, AWM, and Corporate, and risk-rated exposure held in CCB, for which the wholesale methodology is applied when determining the allowance for loan los… |
| 5 | `JPM_FY2018_2018-12-31:550` | Item 15 › Risk monitoring and management |  |  | Wholesale credit risk is monitored regularly at an aggregate portfolio, industry, and individual client and counterparty level with established concentration limits that are reviewed and revised as deemed appropriate by … |
| 6 | `JPM_FY2018_2018-12-31:101` | Item 1A › Reductions in JPMorgan Chase’s credit ratings may adversely affect its liquidity and cost of funding. |  |  | JPMorgan Chase & Co. and certain of its principal subsidiaries are rated by credit rating agencies. Rating agencies evaluate both general and firm-specific and industry-specific factors when determining credit ratings fo… |
| 7 | `JPM_FY2023_2023-12-31:7` | Form 10-K Index |  |  | \| Part I \| \| Page \| \|---\|---\|---\| \| Item 1. \| Business. \| 1 \| \| \| Overview \| 1 \| \| \| Business segments \| 1 \| \| \| Competition \| 1 \| \| \| Human capital \| 2-3 \| \| \| Supervision and regulation \| 4-8 \| \| \| Distribution of asse… |
| 8 | `JPM_FY2023_2023-12-31:1027` | Item 15 › Notes to consolidated financial statements |  |  | \| \| 2023 \| \| \| \| 2022 \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Credit exposure(h)(i) \| On-balance sheet \| \| Off-balance sheet(k) \| Credit exposure(h) \| On-balance sheet \| \| Off-balance sheet(k) \| \| \| Secur… |
| 9 | `JPM_FY2023_2023-12-31:493` | Item 15 › Management’s discussion and analysis |  |  | \| \| Standardized \| \| \| Advanced \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| Year ended December 31, 2023 (in millions) \| Credit risk RWA(c) \| Market risk RWA \| Total RWA \| Credit risk RWA(c)(d) \| Market risk RWA \| Operat… |
| 10 | `JPM_FY2023_2023-12-31:626` | Item 15 › Wholesale credit exposure – industry exposures |  |  | \| Wholesale credit exposure – industries(a) \| \| \| \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| \| \| \| \| \| Selected metrics \| \| \| \| \| \| \| \| \| \| \| 30 days or more past due and accruing loans(i) \| Net charge-o… |
| 11 | `JPM_FY2023_2023-12-31:625` | Item 15 › Wholesale credit exposure – industry exposures |  |  | \| Wholesale credit exposure – industries(a) \| \| \| \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| \| \| \| \| \| Selected metrics \| \| \| \| \| \| \| \| \| \| \| 30 days or more past due and accruing loans(i) \| Net charge-o… |
| 12 | `JPM_FY2023_2023-12-31:87` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. | ✓ | #1, #2 | In JPMorgan Chase’s wholesale businesses, market and economic factors can affect the volume of transactions that JPMorgan Chase executes for its clients or for which it advises clients, and, therefore, the revenue that J… |
| 13 | `JPM_FY2018_2018-12-31:81` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. |  |  | JPMorgan Chase generally maintains positions in various fixed income instruments in its investment securities portfolio, and positions in various fixed income, currency, commodity, credit and equity instruments as part o… |
| 14 | `JPM_FY2018_2018-12-31:82` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. |  |  | • other market risks that may not have been appropriately taken into account in the development, structuring or pricing of a financial instrument. If JPMorgan Chase experiences significant losses in its investment securi… |
| 15 | `JPM_FY2018_2018-12-31:77` | Item 1A › Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. | ✓ | #1, #2 | In JPMorgan Chase’s wholesale businesses, market and economic factors can affect the volume of transactions that JPMorgan Chase executes for its clients or for which it advises clients, and, therefore, the revenue that J… |
| 16 | `JPM_FY2023_2023-12-31:84` | Item 1A › Economic and market events and conditions can materially affect JPMorgan Chase’s businesses and investment and market-making positions. |  |  | •the inability to effectively hedge risks related to market-making and investment portfolio positions, or •other market risks that may not have been appropriately taken into account in the development, structuring or pri… |
| 17 | `JPM_FY2023_2023-12-31:83` | Item 1A › Economic and market events and conditions can materially affect JPMorgan Chase’s businesses and investment and market-making positions. |  |  | JPMorgan Chase’s results of operations can be negatively affected by adverse changes in any of the following: •investor, consumer and business sentiment •events that reduce confidence in the financial markets •inflation,… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#12 `JPM_FY2023_2023-12-31:87`** (cited, gold #1, gold #2)

````text
Item 1A. Risk Factors. > Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses.
In JPMorgan Chase’s wholesale businesses, market and economic factors can affect the volume of transactions that JPMorgan Chase executes for its clients or for which it advises clients, and, therefore, the revenue that JPMorgan Chase receives from those transactions. These factors can also influence the willingness of other financial institutions and investors to participate in capital markets transactions that JPMorgan Chase manages, such as loan syndications or securities underwriting. Furthermore, if a significant and sustained deterioration in market conditions were to occur, the profitability of JPMorgan Chase’s businesses engaged in capital markets activities, including loan syndication, securities underwriting and leveraged lending activities, could be reduced to the extent that those businesses: •earn less fee revenue due to lower transaction volumes, including when clients are unwilling or unable to
````

**#15 `JPM_FY2018_2018-12-31:77`** (cited, gold #1, gold #2)

````text
Item 1A. Risk Factors. > Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses.
In JPMorgan Chase’s wholesale businesses, market and economic factors can affect the volume of transactions that JPMorgan Chase executes for its clients or for which it advises clients, and, therefore, the revenue that JPMorgan Chase receives from those transactions. These factors can also influence the willingness of other financial institutions and investors to participate in capital markets transactions that JPMorgan Chase manages, such as loan syndications or securities underwritings. Furthermore, if a significant and sustained deterioration in market conditions were to occur, the profitability of JPMorgan Chase’s capital markets businesses could be reduced to the extent that those businesses: • earn less fee revenue due to lower transaction volumes, including when clients are unwilling or unable to refinance their outstanding debt obligations in unfavorable market conditions • dispose of portions of credit commitments, such as loan syndications or securities underwritings, at a loss, or • hold larger residual positions in credit commitments that cannot be sold at favorable prices.
````

</details>

RQ2 citation match (section level): `cited=[('JPM', 'Item 1A')] gold=[(None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 3, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| JPMorgan Chase’s 2018 disclosure said that, if market conditions significantly and sustainably deteriorated, “the profitability of JPMorgan Chase’s capital markets businesses could be reduced,” and it specifically tied that risk to loan syndications and securities underwritings, including the possibility of disposing of portions of credit commitments such as loan syndications or securities underwritings at a loss or holding larger residual positions that could not be sold at favorable prices [JPM FY2018, Item 1A, JPM_FY2018_2018-12-31:77]. | supported | The cited 2018 text states the quoted risk and specifically mentions loan syndications, securities underwritings, losses on disposing portions of credit commitments, and larger residual positions. |
| In 2023, the disclosure became more specific by stating that “the profitability of JPMorgan Chase’s businesses engaged in capital markets activities, including loan syndication, securities underwriting and leveraged lending activities, could be reduced,” explicitly adding leveraged lending activities to the identified vulnerable activities [JPM FY2023, Item 1A, JPM_FY2023_2023-12-31:87]. | supported | The cited 2023 text explicitly says profitability of businesses engaged in capital markets activities, including loan syndication, securities underwriting, and leveraged lending activities, could be reduced. |
| So, compared with 2018, the 2023 10-K narrowed the discussion from the broader phrase “capital markets businesses” to businesses engaged in capital markets activities and expanded the explicit list of vulnerable activities from loan syndications and securities underwritings to loan syndication, securities underwriting, and leveraged lending activities [JPM FY2023, Item 1A, JPM_FY2023_2023-12-31:87] [JPM FY2018, Item 1A, JPM_FY2018_2018-12-31:77]. | supported | The 2018 evidence uses 'capital markets businesses' and names loan syndications and securities underwritings, while the 2023 evidence uses 'businesses engaged in capital markets activities' and adds leveraged lending activities. |

</details>
