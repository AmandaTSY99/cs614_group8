# gold-057: Single-hop text

[← all cases](../README.md) · company: AMAZON COM INC (AMZN) · fiscal year: 2019 · recipe `text` · hop `single` · answer type `qualitative` · scope `single_doc` · RQ2 category `single_hop_factual`

## Gold QA

**Question**

> In its fiscal year 2019 10-K, which foreign currencies does Amazon name as currencies in which it holds cash equivalents and/or marketable securities, and what happens to these balances if the U.S. dollar strengthens?

**Gold answer**

> Amazon holds cash equivalents and/or marketable securities in foreign currencies including the British Pound, the Euro, and the Japanese Yen. When the U.S. dollar strengthens against these currencies, the translated value of these balances may be materially less than expected.

**Key points** (RQ3 keypoint_recall targets)

1. Amazon holds cash equivalents and/or marketable securities in foreign currencies.
2. The specific currencies mentioned include British Pounds, Euros, and Japanese Yen.
3. The value of these balances may be materially less than expected when the U.S. dollar strengthens.

**Gold evidence**

1. `AMZN_FY2019_2019-12-31` · Item 1A. Risk Factors › We Have Foreign Exchange Risk · text

   > We also hold cash equivalents and/or marketable securities in foreign currencies including British Pounds, Euros, and Japanese Yen.

2. `AMZN_FY2019_2019-12-31` · Item 1A. Risk Factors › We Have Foreign Exchange Risk · text

   > When the U.S. Dollar strengthens compared to these currencies, cash equivalents, and marketable securities balances, when translated, may be materially less than expected and vice versa.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 11 | 14 |
| recall@5 | 1.00 | 1.00 | 0.00 | 0.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.67 | 1.00 | 0.10 | 0.09 |
| gold evidence first rank | #1: 1, #2: 1 | #1: 1, #2: 1 | #1: 10, #2: 10 | #1: 11, #2: 11 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | – | – | – | – |
| keypoint_recall | 1.00 | 1.00 | 1.00 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 2215 | 1230 | 13077 | 14197 |
| cost (USD) | 0.0004 | 0.0002 | 0.0493 | 0.0505 |
| latency (s) | 1.8 | 6.2 | 23.9 | 21.3 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> Amazon names **British Pounds, Euros, and Japanese Yen** as foreign currencies in which it holds cash equivalents and/or marketable securities. If the **U.S. Dollar strengthens** against these currencies, those balances, **when translated, may be materially less than expected**. [1]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AMZN_FY2019_2019-12-31:57` | Item 1A › We Have Foreign Exchange Risk | ✓ | #1, #2 | The results of operations of, and certain of our intercompany balances associated with, our international stores and product and service offerings are exposed to foreign exchange rate fluctuations. Due to these fluctuati… |
| 2 | `AMZN_FY2019_2019-12-31:249` | Item 8 › Cash, Cash Equivalents, Restricted Cash, and Marketable Securities |  |  | \| \| December 31, 2018 \| \| \| \| \|---\|---\|---\|---\|---\| \| \| Cost or Amortized Cost \| Gross Unrealized Gains \| Gross Unrealized Losses \| Total Estimated Fair Value \| \| Cash \| $10,406 \| $— \| $— \| $10,406 \| \| Level 1 securities… |
| 3 | `AMZN_FY2019_2019-12-31:252` | Item 8 › Cash, Cash Equivalents, Restricted Cash, and Marketable Securities |  |  | ___________________ (1) The related unrealized gain (loss) recorded in “Other income (expense), net” was $4 million for the year ended December 31, 2019. (2) We are required to pledge or otherwise restrict a portion of o… |
| 4 | `AMZN_FY2019_2019-12-31:108` | Item 7 › Overview |  |  | Our financial reporting currency is the U.S. Dollar and changes in foreign exchange rates significantly affect our reported results and consolidated trends. For example, if the U.S. Dollar weakens year-over-year relative… |
| 5 | `AMZN_FY2019_2019-12-31:256` | Item 8 › Cash, Cash Equivalents, Restricted Cash, and Marketable Securities |  |  | Actual maturities may differ from the contractual maturities because borrowers may have certain prepayment conditions. |
| 6 | `AMZN_FY2019_2019-12-31:118` | Item 7 › Liquidity and Capital Resources |  | #1 | Our principal sources of liquidity are cash flows generated from operations and our cash, cash equivalents, and marketable securities balances, which, at fair value, were $41.3 billion and $55.0 billion as of December 31… |
| 7 | `AMZN_FY2019_2019-12-31:250` | Item 8 › Cash, Cash Equivalents, Restricted Cash, and Marketable Securities |  |  | \| \| December 31, 2019 \| \| \| \| \|---\|---\|---\|---\|---\| \| \| Cost or Amortized Cost \| Gross Unrealized Gains \| Gross Unrealized Losses \| Total Estimated Fair Value \| \| Cash \| $9,776 \| $— \| $— \| $9,776 \| \| Level 1 securities: … |
| 8 | `AMZN_FY2019_2019-12-31:254` | Item 8 › Cash, Cash Equivalents, Restricted Cash, and Marketable Securities |  |  | The following table summarizes the remaining contractual maturities of our cash equivalents and marketable fixed income securities as of December 31, 2019 (in millions): |
| 9 | `AMZN_FY2019_2019-12-31:248` | Item 8 › Cash, Cash Equivalents, Restricted Cash, and Marketable Securities |  |  | As of December 31, 2018 and 2019, our cash, cash equivalents, restricted cash, and marketable securities primarily consisted of cash, AAA-rated money market funds, U.S. and foreign government and agency securities, and o… |
| 10 | `AMZN_FY2019_2019-12-31:241` | Item 8 › Foreign Currency |  |  | We have internationally-focused stores for which the net sales generated, as well as most of the related expenses directly incurred from those operations, are denominated in local functional currencies. The functional cu… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AMZN_FY2019_2019-12-31:57`** (cited, gold #1, gold #2)

````text
Item 1A. Risk Factors > We Have Foreign Exchange Risk
The results of operations of, and certain of our intercompany balances associated with, our international stores and product and service offerings are exposed to foreign exchange rate fluctuations. Due to these fluctuations, operating results may differ materially from expectations, and we may record significant gains or losses on the remeasurement of intercompany balances. As we have expanded our international operations, our exposure to exchange rate fluctuations has increased. We also hold cash equivalents and/or marketable securities in foreign currencies including British Pounds, Euros, and Japanese Yen. When the U.S. Dollar strengthens compared to these currencies, cash equivalents, and marketable securities balances, when translated, may be materially less than expected and vice versa. The Loss of Key Senior Management Personnel or the Failure to Hire and Retain Highly Skilled and Other Key Personnel Could Negatively Affect Our Business
````

**#6 `AMZN_FY2019_2019-12-31:118`** (gold #1)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Liquidity and Capital Resources
Our principal sources of liquidity are cash flows generated from operations and our cash, cash equivalents, and marketable securities balances, which, at fair value, were $41.3 billion and $55.0 billion as of December 31, 2018 and 2019. Amounts held in foreign currencies were $13.8 billion and $15.3 billion as of December 31, 2018 and 2019, and were primarily Euros, British Pounds, and Japanese Yen.
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 1A')] gold=[(None, 'Item 1A')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 1.

**Generated answer**

> Amazon says it holds cash equivalents and/or marketable securities in **British Pounds, Euros, and Japanese Yen**. If the **U.S. Dollar strengthens** against these currencies, those balances, **when translated, may be materially less than expected**. [1]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AMZN_FY2019_2019-12-31:57` | Item 1A › We Have Foreign Exchange Risk | ✓ | #1, #2 | The results of operations of, and certain of our intercompany balances associated with, our international stores and product and service offerings are exposed to foreign exchange rate fluctuations. Due to these fluctuati… |
| 2 | `AMZN_FY2019_2019-12-31:118` | Item 7 › Liquidity and Capital Resources |  | #1 | Our principal sources of liquidity are cash flows generated from operations and our cash, cash equivalents, and marketable securities balances, which, at fair value, were $41.3 billion and $55.0 billion as of December 31… |
| 3 | `AMZN_FY2019_2019-12-31:108` | Item 7 › Overview |  |  | Our financial reporting currency is the U.S. Dollar and changes in foreign exchange rates significantly affect our reported results and consolidated trends. For example, if the U.S. Dollar weakens year-over-year relative… |
| 4 | `AMZN_FY2019_2019-12-31:250` | Item 8 › Cash, Cash Equivalents, Restricted Cash, and Marketable Securities |  |  | \| \| December 31, 2019 \| \| \| \| \|---\|---\|---\|---\|---\| \| \| Cost or Amortized Cost \| Gross Unrealized Gains \| Gross Unrealized Losses \| Total Estimated Fair Value \| \| Cash \| $9,776 \| $— \| $— \| $9,776 \| \| Level 1 securities: … |
| 5 | `AMZN_FY2019_2019-12-31:248` | Item 8 › Cash, Cash Equivalents, Restricted Cash, and Marketable Securities |  |  | As of December 31, 2018 and 2019, our cash, cash equivalents, restricted cash, and marketable securities primarily consisted of cash, AAA-rated money market funds, U.S. and foreign government and agency securities, and o… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AMZN_FY2019_2019-12-31:57`** (cited, gold #1, gold #2)

````text
Item 1A. Risk Factors > We Have Foreign Exchange Risk
The results of operations of, and certain of our intercompany balances associated with, our international stores and product and service offerings are exposed to foreign exchange rate fluctuations. Due to these fluctuations, operating results may differ materially from expectations, and we may record significant gains or losses on the remeasurement of intercompany balances. As we have expanded our international operations, our exposure to exchange rate fluctuations has increased. We also hold cash equivalents and/or marketable securities in foreign currencies including British Pounds, Euros, and Japanese Yen. When the U.S. Dollar strengthens compared to these currencies, cash equivalents, and marketable securities balances, when translated, may be materially less than expected and vice versa. The Loss of Key Senior Management Personnel or the Failure to Hire and Retain Highly Skilled and Other Key Personnel Could Negatively Affect Our Business
````

**#2 `AMZN_FY2019_2019-12-31:118`** (gold #1)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Liquidity and Capital Resources
Our principal sources of liquidity are cash flows generated from operations and our cash, cash equivalents, and marketable securities balances, which, at fair value, were $41.3 billion and $55.0 billion as of December 31, 2018 and 2019. Amounts held in foreign currencies were $13.8 billion and $15.3 billion as of December 31, 2018 and 2019, and were primarily Euros, British Pounds, and Japanese Yen.
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 1A')] gold=[(None, 'Item 1A')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 11, cited: 1.

**Generated answer**

> Amazon states that it holds cash equivalents and/or marketable securities in foreign currencies including British Pounds, Euros, and Japanese Yen. [AMZN FY2019, Item 1A, AMZN_FY2019_2019-12-31:57]  
> Amazon says that when the U.S. Dollar strengthens compared to these currencies, those cash equivalents and marketable securities balances, when translated, may be materially less than expected. [AMZN FY2019, Item 1A, AMZN_FY2019_2019-12-31:57]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AMZN_FY2019_2019-12-31:248` | Item 8 › Cash, Cash Equivalents, Restricted Cash, and Marketable Securities |  |  | As of December 31, 2018 and 2019, our cash, cash equivalents, restricted cash, and marketable securities primarily consisted of cash, AAA-rated money market funds, U.S. and foreign government and agency securities, and o… |
| 2 | `AMZN_FY2019_2019-12-31:254` | Item 8 › Cash, Cash Equivalents, Restricted Cash, and Marketable Securities |  |  | The following table summarizes the remaining contractual maturities of our cash equivalents and marketable fixed income securities as of December 31, 2019 (in millions): |
| 3 | `AMZN_FY2019_2019-12-31:252` | Item 8 › Cash, Cash Equivalents, Restricted Cash, and Marketable Securities |  |  | ___________________ (1) The related unrealized gain (loss) recorded in “Other income (expense), net” was $4 million for the year ended December 31, 2019. (2) We are required to pledge or otherwise restrict a portion of o… |
| 4 | `AMZN_FY2019_2019-12-31:256` | Item 8 › Cash, Cash Equivalents, Restricted Cash, and Marketable Securities |  |  | Actual maturities may differ from the contractual maturities because borrowers may have certain prepayment conditions. |
| 5 | `AMZN_FY2019_2019-12-31:241` | Item 8 › Foreign Currency |  |  | We have internationally-focused stores for which the net sales generated, as well as most of the related expenses directly incurred from those operations, are denominated in local functional currencies. The functional cu… |
| 6 | `AMZN_FY2019_2019-12-31:165` | Item 7A › Foreign Exchange Risk |  |  | We have foreign exchange risk related to foreign-denominated cash, cash equivalents, and marketable securities (“foreign funds”). Based on the balance of foreign funds as of December 31, 2019, of $15.3 billion, an assume… |
| 7 | `AMZN_FY2019_2019-12-31:157` | Item 7A |  |  | We are exposed to market risk for the effect of interest rate changes, foreign currency fluctuations, and changes in the market values of our investments. Information relating to quantitative and qualitative disclosures … |
| 8 | `AMZN_FY2019_2019-12-31:160` | Item 7A › Interest Rate Risk |  |  | \| \| 2020 \| 2021 \| 2022 \| 2023 \| 2024 \| Thereafter \| Total \| Estimated Fair Value as of December 31, 2019 \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Foreign government and agency securities \| 4,630 \| 168 \| 4 \| — \| 2 \| — \| … |
| 9 | `AMZN_FY2019_2019-12-31:159` | Item 7A › Interest Rate Risk |  |  | \| \| 2020 \| 2021 \| 2022 \| 2023 \| 2024 \| Thereafter \| Total \| Estimated Fair Value as of December 31, 2019 \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Money market funds \| $18,850 \| $— \| $— \| $— \| $— \| $— \| $18,850 \| $18,850… |
| 10 | `AMZN_FY2019_2019-12-31:57` | Item 1A › We Have Foreign Exchange Risk | ✓ | #1, #2 | The results of operations of, and certain of our intercompany balances associated with, our international stores and product and service offerings are exposed to foreign exchange rate fluctuations. Due to these fluctuati… |
| 11 | `AMZN_FY2019_2019-12-31:108` | Item 7 › Overview |  |  | Our financial reporting currency is the U.S. Dollar and changes in foreign exchange rates significantly affect our reported results and consolidated trends. For example, if the U.S. Dollar weakens year-over-year relative… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#10 `AMZN_FY2019_2019-12-31:57`** (cited, gold #1, gold #2)

````text
Item 1A. Risk Factors > We Have Foreign Exchange Risk
The results of operations of, and certain of our intercompany balances associated with, our international stores and product and service offerings are exposed to foreign exchange rate fluctuations. Due to these fluctuations, operating results may differ materially from expectations, and we may record significant gains or losses on the remeasurement of intercompany balances. As we have expanded our international operations, our exposure to exchange rate fluctuations has increased. We also hold cash equivalents and/or marketable securities in foreign currencies including British Pounds, Euros, and Japanese Yen. When the U.S. Dollar strengthens compared to these currencies, cash equivalents, and marketable securities balances, when translated, may be materially less than expected and vice versa. The Loss of Key Senior Management Personnel or the Failure to Hire and Retain Highly Skilled and Other Key Personnel Could Negatively Affect Our Business
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 1A')] gold=[(None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 2, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Amazon states that it holds cash equivalents and/or marketable securities in foreign currencies including British Pounds, Euros, and Japanese Yen. [AMZN FY2019, Item 1A, AMZN_FY2019_2019-12-31:57] | supported | The evidence explicitly states Amazon holds cash equivalents and/or marketable securities in British Pounds, Euros, and Japanese Yen. |
| Amazon says that when the U.S. Dollar strengthens compared to these currencies, those cash equivalents and marketable securities balances, when translated, may be materially less than expected. [AMZN FY2019, Item 1A, AMZN_FY2019_2019-12-31:57] | supported | The evidence explicitly says that when the U.S. Dollar strengthens, those translated balances may be materially less than expected. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 14, cited: 1.

**Generated answer**

> Amazon states that it holds cash equivalents and/or marketable securities in foreign currencies including British Pounds, Euros, and Japanese Yen. [AMZN FY2019, Item 1A, AMZN_FY2019_2019-12-31:57]
>
> Amazon says that when the U.S. Dollar strengthens compared to these currencies, the cash equivalents and marketable securities balances, when translated, may be materially less than expected. [AMZN FY2019, Item 1A, AMZN_FY2019_2019-12-31:57]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AMZN_FY2019_2019-12-31:248` | Item 8 › Cash, Cash Equivalents, Restricted Cash, and Marketable Securities |  |  | As of December 31, 2018 and 2019, our cash, cash equivalents, restricted cash, and marketable securities primarily consisted of cash, AAA-rated money market funds, U.S. and foreign government and agency securities, and o… |
| 2 | `AMZN_FY2019_2019-12-31:254` | Item 8 › Cash, Cash Equivalents, Restricted Cash, and Marketable Securities |  |  | The following table summarizes the remaining contractual maturities of our cash equivalents and marketable fixed income securities as of December 31, 2019 (in millions): |
| 3 | `AMZN_FY2019_2019-12-31:252` | Item 8 › Cash, Cash Equivalents, Restricted Cash, and Marketable Securities |  |  | ___________________ (1) The related unrealized gain (loss) recorded in “Other income (expense), net” was $4 million for the year ended December 31, 2019. (2) We are required to pledge or otherwise restrict a portion of o… |
| 4 | `AMZN_FY2019_2019-12-31:256` | Item 8 › Cash, Cash Equivalents, Restricted Cash, and Marketable Securities |  |  | Actual maturities may differ from the contractual maturities because borrowers may have certain prepayment conditions. |
| 5 | `AMZN_FY2019_2019-12-31:249` | Item 8 › Cash, Cash Equivalents, Restricted Cash, and Marketable Securities |  |  | \| \| December 31, 2018 \| \| \| \| \|---\|---\|---\|---\|---\| \| \| Cost or Amortized Cost \| Gross Unrealized Gains \| Gross Unrealized Losses \| Total Estimated Fair Value \| \| Cash \| $10,406 \| $— \| $— \| $10,406 \| \| Level 1 securities… |
| 6 | `AMZN_FY2019_2019-12-31:217` | Item 8 › Fair Value of Financial Instruments |  |  | For our cash, cash equivalents, or marketable securities, we measure the fair value of money market funds and certain marketable equity securities based on quoted prices in active markets for identical assets or liabilit… |
| 7 | `AMZN_FY2019_2019-12-31:157` | Item 7A |  |  | We are exposed to market risk for the effect of interest rate changes, foreign currency fluctuations, and changes in the market values of our investments. Information relating to quantitative and qualitative disclosures … |
| 8 | `AMZN_FY2019_2019-12-31:160` | Item 7A › Interest Rate Risk |  |  | \| \| 2020 \| 2021 \| 2022 \| 2023 \| 2024 \| Thereafter \| Total \| Estimated Fair Value as of December 31, 2019 \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Foreign government and agency securities \| 4,630 \| 168 \| 4 \| — \| 2 \| — \| … |
| 9 | `AMZN_FY2019_2019-12-31:165` | Item 7A › Foreign Exchange Risk |  |  | We have foreign exchange risk related to foreign-denominated cash, cash equivalents, and marketable securities (“foreign funds”). Based on the balance of foreign funds as of December 31, 2019, of $15.3 billion, an assume… |
| 10 | `AMZN_FY2019_2019-12-31:159` | Item 7A › Interest Rate Risk |  |  | \| \| 2020 \| 2021 \| 2022 \| 2023 \| 2024 \| Thereafter \| Total \| Estimated Fair Value as of December 31, 2019 \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Money market funds \| $18,850 \| $— \| $— \| $— \| $— \| $— \| $18,850 \| $18,850… |
| 11 | `AMZN_FY2019_2019-12-31:57` | Item 1A › We Have Foreign Exchange Risk | ✓ | #1, #2 | The results of operations of, and certain of our intercompany balances associated with, our international stores and product and service offerings are exposed to foreign exchange rate fluctuations. Due to these fluctuati… |
| 12 | `AMZN_FY2019_2019-12-31:241` | Item 8 › Foreign Currency |  |  | We have internationally-focused stores for which the net sales generated, as well as most of the related expenses directly incurred from those operations, are denominated in local functional currencies. The functional cu… |
| 13 | `AMZN_FY2019_2019-12-31:108` | Item 7 › Overview |  |  | Our financial reporting currency is the U.S. Dollar and changes in foreign exchange rates significantly affect our reported results and consolidated trends. For example, if the U.S. Dollar weakens year-over-year relative… |
| 14 | `AMZN_FY2019_2019-12-31:250` | Item 8 › Cash, Cash Equivalents, Restricted Cash, and Marketable Securities |  |  | \| \| December 31, 2019 \| \| \| \| \|---\|---\|---\|---\|---\| \| \| Cost or Amortized Cost \| Gross Unrealized Gains \| Gross Unrealized Losses \| Total Estimated Fair Value \| \| Cash \| $9,776 \| $— \| $— \| $9,776 \| \| Level 1 securities: … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#11 `AMZN_FY2019_2019-12-31:57`** (cited, gold #1, gold #2)

````text
Item 1A. Risk Factors > We Have Foreign Exchange Risk
The results of operations of, and certain of our intercompany balances associated with, our international stores and product and service offerings are exposed to foreign exchange rate fluctuations. Due to these fluctuations, operating results may differ materially from expectations, and we may record significant gains or losses on the remeasurement of intercompany balances. As we have expanded our international operations, our exposure to exchange rate fluctuations has increased. We also hold cash equivalents and/or marketable securities in foreign currencies including British Pounds, Euros, and Japanese Yen. When the U.S. Dollar strengthens compared to these currencies, cash equivalents, and marketable securities balances, when translated, may be materially less than expected and vice versa. The Loss of Key Senior Management Personnel or the Failure to Hire and Retain Highly Skilled and Other Key Personnel Could Negatively Affect Our Business
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 1A')] gold=[(None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 2, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Amazon states that it holds cash equivalents and/or marketable securities in foreign currencies including British Pounds, Euros, and Japanese Yen. [AMZN FY2019, Item 1A, AMZN_FY2019_2019-12-31:57] | supported | The evidence explicitly says Amazon holds cash equivalents and/or marketable securities in British Pounds, Euros, and Japanese Yen. |
| Amazon says that when the U.S. Dollar strengthens compared to these currencies, the cash equivalents and marketable securities balances, when translated, may be materially less than expected. [AMZN FY2019, Item 1A, AMZN_FY2019_2019-12-31:57] | supported | The evidence explicitly states that when the U.S. Dollar strengthens, translated cash equivalents and marketable securities balances may be materially less than expected. |

</details>
