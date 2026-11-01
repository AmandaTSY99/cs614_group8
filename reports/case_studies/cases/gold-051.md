# gold-051: Single-hop text

[← all cases](../README.md) · company: Alphabet Inc. (GOOGL) · fiscal year: 2020 · recipe `text` · hop `single` · answer type `qualitative` · scope `single_doc` · RQ2 category `single_hop_factual`

## Gold QA

**Question**

> According to Alphabet's 2020 10-K, what specific types of contracts are excluded from the calculation of remaining performance obligations?

**Gold answer**

> Alphabet excludes contracts with an original expected term of one year or less, cancellable contracts, and contracts for which revenue is recognized at the amount to which the company has the right to invoice for services performed.

**Key points** (RQ3 keypoint_recall targets)

1. Contracts with an original expected term of one year or less
2. Cancellable contracts
3. Contracts for which revenue is recognized at the amount to which the company has the right to invoice for services performed

**Gold evidence**

1. `GOOGL_FY2020_2020-12-31` · ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Deferred Revenues and Remaining Performance Obligations · text

   > Remaining performance obligations include related deferred revenue currently recorded as well as amounts that will be invoiced in future periods, and excludes (i) contracts with an original expected term of one year or less, (ii) cancellable contracts, and (iii) contracts for which we recognize revenue at the amount to which we have the right to invoice for services performed.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 10 | 10 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.33 | 1.00 | 0.50 | 0.50 |
| gold evidence first rank | #1: 3 | #1: 1 | #1: 2 | #1: 2 |
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
| tokens | 2249 | 1194 | 12462 | 12478 |
| cost (USD) | 0.0004 | 0.0002 | 0.0429 | 0.0430 |
| latency (s) | 1.6 | 6.0 | 20.4 | 20.5 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> Alphabet’s 2020 10-K says remaining performance obligations exclude:
> 1. contracts with an original expected term of one year or less,
> 2. cancellable contracts, and
> 3. contracts for which revenue is recognized at the amount Alphabet has the right to invoice for services performed. [3]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2020_2020-12-31:237` | Item 7 › Contractual Obligations as of December 31, 2020 |  |  | (1) For further information, refer to Note 4 of the Notes to Consolidated Financial Statements included in Part II, Item 8 of this Annual Report on Form 10-K. (2) Represents non-cancelable contractual obligations primari… |
| 2 | `GOOGL_FY2020_2020-12-31:236` | Item 7 › Contractual Obligations as of December 31, 2020 |  |  | \| \| Payments Due By Period \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| Total \| Less than 1 year \| 1-3 years \| 3-5 years \| More than 5 years \| \| Operating lease obligations(1) \| $15,091 \| $2,198 \| $4,165 \| $3,127 \| $5,601 \| \|… |
| 3 | `GOOGL_FY2020_2020-12-31:344` | Item 8 › Deferred Revenues and Remaining Performance Obligations | ✓ | #1 | Additionally, we have performance obligations associated with commitments in customer contracts, primarily related to Google Cloud, for future services that have not yet been recognized as revenues, also referred to as r… |
| 4 | `GOOGL_FY2020_2020-12-31:235` | Item 7 › Contractual Obligations as of December 31, 2020 |  |  | The following summarizes our contractual obligations as of December 31, 2020 (in millions): |
| 5 | `GOOGL_FY2020_2020-12-31:305` | Item 8 › Arrangements with Multiple Performance Obligations |  |  | Our contracts with customers may include multiple performance obligations. For such arrangements, we allocate revenues to each performance obligation based on its relative standalone selling price. We generally determine… |
| 6 | `GOOGL_FY2020_2020-12-31:434` | Item 8 › Purchase Obligations |  |  | As of December 31, 2020, we had $10.7 billion of other non-cancelable contractual obligations, primarily related to data center operations and build-outs, digital media content licensing, information technology assets an… |
| 7 | `GOOGL_FY2020_2020-12-31:239` | Item 7 › Off-Balance Sheet Arrangements |  |  | As of December 31, 2020, we did not have any off-balance sheet arrangements, as defined in Item 303(a)(4)(ii) of Regulation S-K, that have or are reasonably likely to have a current or future effect on our financial cond… |
| 8 | `GOOGL_FY2020_2020-12-31:387` | Item 8 › Other Derivatives |  |  | \| \| Gains (Losses) Recognized in Income \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Year Ended December 31, \| \| \| \| \| \| \| \| 2018 \| \| 2019 \| \| 2020 \| \| \| \| Revenues \| Other income (expense), net \| Revenues \| Other incom… |
| 9 | `GOOGL_FY2020_2020-12-31:347` | Item 8 › Debt Securities |  |  | \| \| As of December 31, 2020 \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Adjusted Cost \| Gross Unrealized Gains \| Gross Unrealized Losses \| Fair Value \| Cash and Cash Equivalents \| Marketable Securities \| \| Level 2: \| \|… |
| 10 | `GOOGL_FY2020_2020-12-31:406` | Item 8 › Long-Term Debt |  |  | \| \| Maturity \| Coupon Rate \| Effective Interest Rate \| As of December 31, 2019 \| As of December 31, 2020 \| \|---\|---\|---\|---\|---\|---\| \| Debt \| \| \| \| \| \| \| 2011-2016 Notes Issuances \| 2021 - 2026 \| 2.00% - 3.63% \| 2.23% - … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `GOOGL_FY2020_2020-12-31:344`** (cited, gold #1)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Deferred Revenues and Remaining Performance Obligations
Additionally, we have performance obligations associated with commitments in customer contracts, primarily related to Google Cloud, for future services that have not yet been recognized as revenues, also referred to as remaining performance obligations. Remaining performance obligations include related deferred revenue currently recorded as well as amounts that will be invoiced in future periods, and excludes (i) contracts with an original expected term of one year or less, (ii) cancellable contracts, and (iii) contracts for which we recognize revenue at the amount to which we have the right to invoice for services performed. As of December 31, 2020, the amount not yet recognized as revenues from these commitments is $29.8 billion. We expect to recognize approximately half over the next 24 months with the remaining thereafter. However, the amount and timing of revenue recognition is largely driven by when the customer utilizes the services and our ability to deliver in accordance with relevant contract terms, which could impact our estimate of the remaining performance obligations and when we expect to recognize such as revenues. Table of Contents Alphabet Inc.
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 1.

**Generated answer**

> Alphabet’s 2020 10-K says remaining performance obligations exclude:
>
> 1. contracts with an original expected term of one year or less,  
> 2. cancellable contracts, and  
> 3. contracts for which revenue is recognized at the amount to which Alphabet has the right to invoice for services performed. [1]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2020_2020-12-31:344` | Item 8 › Deferred Revenues and Remaining Performance Obligations | ✓ | #1 | Additionally, we have performance obligations associated with commitments in customer contracts, primarily related to Google Cloud, for future services that have not yet been recognized as revenues, also referred to as r… |
| 2 | `GOOGL_FY2020_2020-12-31:237` | Item 7 › Contractual Obligations as of December 31, 2020 |  |  | (1) For further information, refer to Note 4 of the Notes to Consolidated Financial Statements included in Part II, Item 8 of this Annual Report on Form 10-K. (2) Represents non-cancelable contractual obligations primari… |
| 3 | `GOOGL_FY2020_2020-12-31:238` | Item 7 › Contractual Obligations as of December 31, 2020 |  |  | (4) Represents one-time transition tax payable incurred as a result of the Tax Act. For further information, refer to Note 14 of the Notes to Consolidated Financial Statements included in Part II, Item 8 of this Annual R… |
| 4 | `GOOGL_FY2020_2020-12-31:305` | Item 8 › Arrangements with Multiple Performance Obligations |  |  | Our contracts with customers may include multiple performance obligations. For such arrangements, we allocate revenues to each performance obligation based on its relative standalone selling price. We generally determine… |
| 5 | `GOOGL_FY2020_2020-12-31:45` | Item 1 › Culture and Workforce |  |  | Alphabet is committed to making diversity, equity, and inclusion part of everything we do and we’re committed to growing a workforce that’s representative of the users we serve. More information on Google’s approach to d… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2020_2020-12-31:344`** (cited, gold #1)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Deferred Revenues and Remaining Performance Obligations
Additionally, we have performance obligations associated with commitments in customer contracts, primarily related to Google Cloud, for future services that have not yet been recognized as revenues, also referred to as remaining performance obligations. Remaining performance obligations include related deferred revenue currently recorded as well as amounts that will be invoiced in future periods, and excludes (i) contracts with an original expected term of one year or less, (ii) cancellable contracts, and (iii) contracts for which we recognize revenue at the amount to which we have the right to invoice for services performed. As of December 31, 2020, the amount not yet recognized as revenues from these commitments is $29.8 billion. We expect to recognize approximately half over the next 24 months with the remaining thereafter. However, the amount and timing of revenue recognition is largely driven by when the customer utilizes the services and our ability to deliver in accordance with relevant contract terms, which could impact our estimate of the remaining performance obligations and when we expect to recognize such as revenues. Table of Contents Alphabet Inc.
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 10, cited: 1.

**Generated answer**

> According to Alphabet’s 2020 10-K, remaining performance obligations exclude (i) contracts with an original expected term of one year or less, (ii) cancellable contracts, and (iii) contracts for which Alphabet recognizes revenue at the amount to which it has the right to invoice for services performed [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:344].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2020_2020-12-31:305` | Item 8 › Arrangements with Multiple Performance Obligations |  |  | Our contracts with customers may include multiple performance obligations. For such arrangements, we allocate revenues to each performance obligation based on its relative standalone selling price. We generally determine… |
| 2 | `GOOGL_FY2020_2020-12-31:344` | Item 8 › Deferred Revenues and Remaining Performance Obligations | ✓ | #1 | Additionally, we have performance obligations associated with commitments in customer contracts, primarily related to Google Cloud, for future services that have not yet been recognized as revenues, also referred to as r… |
| 3 | `GOOGL_FY2020_2020-12-31:237` | Item 7 › Contractual Obligations as of December 31, 2020 |  |  | (1) For further information, refer to Note 4 of the Notes to Consolidated Financial Statements included in Part II, Item 8 of this Annual Report on Form 10-K. (2) Represents non-cancelable contractual obligations primari… |
| 4 | `GOOGL_FY2020_2020-12-31:238` | Item 7 › Contractual Obligations as of December 31, 2020 |  |  | (4) Represents one-time transition tax payable incurred as a result of the Tax Act. For further information, refer to Note 14 of the Notes to Consolidated Financial Statements included in Part II, Item 8 of this Annual R… |
| 5 | `GOOGL_FY2020_2020-12-31:236` | Item 7 › Contractual Obligations as of December 31, 2020 |  |  | \| \| Payments Due By Period \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| Total \| Less than 1 year \| 1-3 years \| 3-5 years \| More than 5 years \| \| Operating lease obligations(1) \| $15,091 \| $2,198 \| $4,165 \| $3,127 \| $5,601 \| \|… |
| 6 | `GOOGL_FY2020_2020-12-31:386` | Item 8 › Other Derivatives |  |  | \| \| Gains (Losses) Recognized in Income \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Year Ended December 31, \| \| \| \| \| \| \| \| 2018 \| \| 2019 \| \| 2020 \| \| \| \| Revenues \| Other income (expense), net \| Revenues \| Other incom… |
| 7 | `GOOGL_FY2020_2020-12-31:343` | Item 8 › Deferred Revenues and Remaining Performance Obligations |  |  | We record deferred revenues when cash payments are received or due in advance of our performance, including amounts which are refundable. Deferred revenues primarily relate to Google Cloud and Google other. Our total def… |
| 8 | `GOOGL_FY2020_2020-12-31:19` | NOTE ABOUT FORWARD-LOOKING STATEMENTS |  |  | •fluctuations in our revenue growth, as well as the change in paid clicks and cost-per-click and the change in impressions and cost-per-impression, and various factors contributing to such fluctuations; •our expectation … |
| 9 | `GOOGL_FY2020_2020-12-31:406` | Item 8 › Long-Term Debt |  |  | \| \| Maturity \| Coupon Rate \| Effective Interest Rate \| As of December 31, 2019 \| As of December 31, 2020 \| \|---\|---\|---\|---\|---\|---\| \| Debt \| \| \| \| \| \| \| 2011-2016 Notes Issuances \| 2021 - 2026 \| 2.00% - 3.63% \| 2.23% - … |
| 10 | `GOOGL_FY2020_2020-12-31:387` | Item 8 › Other Derivatives |  |  | \| \| Gains (Losses) Recognized in Income \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Year Ended December 31, \| \| \| \| \| \| \| \| 2018 \| \| 2019 \| \| 2020 \| \| \| \| Revenues \| Other income (expense), net \| Revenues \| Other incom… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `GOOGL_FY2020_2020-12-31:344`** (cited, gold #1)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Deferred Revenues and Remaining Performance Obligations
Additionally, we have performance obligations associated with commitments in customer contracts, primarily related to Google Cloud, for future services that have not yet been recognized as revenues, also referred to as remaining performance obligations. Remaining performance obligations include related deferred revenue currently recorded as well as amounts that will be invoiced in future periods, and excludes (i) contracts with an original expected term of one year or less, (ii) cancellable contracts, and (iii) contracts for which we recognize revenue at the amount to which we have the right to invoice for services performed. As of December 31, 2020, the amount not yet recognized as revenues from these commitments is $29.8 billion. We expect to recognize approximately half over the next 24 months with the remaining thereafter. However, the amount and timing of revenue recognition is largely driven by when the customer utilizes the services and our ability to deliver in accordance with relevant contract terms, which could impact our estimate of the remaining performance obligations and when we expect to recognize such as revenues. Table of Contents Alphabet Inc.
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| According to Alphabet’s 2020 10-K, remaining performance obligations exclude (i) contracts with an original expected term of one year or less, (ii) cancellable contracts, and (iii) contracts for which Alphabet recognizes revenue at the amount to which it has the right to invoice for services performed [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:344]. | supported | The cited passage explicitly lists all three exclusions from remaining performance obligations. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 10, cited: 1.

**Generated answer**

> Alphabet excluded from remaining performance obligations (i) contracts with an original expected term of one year or less, (ii) cancellable contracts, and (iii) contracts for which it recognizes revenue at the amount to which it has the right to invoice for services performed. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:344]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2020_2020-12-31:305` | Item 8 › Arrangements with Multiple Performance Obligations |  |  | Our contracts with customers may include multiple performance obligations. For such arrangements, we allocate revenues to each performance obligation based on its relative standalone selling price. We generally determine… |
| 2 | `GOOGL_FY2020_2020-12-31:344` | Item 8 › Deferred Revenues and Remaining Performance Obligations | ✓ | #1 | Additionally, we have performance obligations associated with commitments in customer contracts, primarily related to Google Cloud, for future services that have not yet been recognized as revenues, also referred to as r… |
| 3 | `GOOGL_FY2020_2020-12-31:237` | Item 7 › Contractual Obligations as of December 31, 2020 |  |  | (1) For further information, refer to Note 4 of the Notes to Consolidated Financial Statements included in Part II, Item 8 of this Annual Report on Form 10-K. (2) Represents non-cancelable contractual obligations primari… |
| 4 | `GOOGL_FY2020_2020-12-31:238` | Item 7 › Contractual Obligations as of December 31, 2020 |  |  | (4) Represents one-time transition tax payable incurred as a result of the Tax Act. For further information, refer to Note 14 of the Notes to Consolidated Financial Statements included in Part II, Item 8 of this Annual R… |
| 5 | `GOOGL_FY2020_2020-12-31:236` | Item 7 › Contractual Obligations as of December 31, 2020 |  |  | \| \| Payments Due By Period \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| Total \| Less than 1 year \| 1-3 years \| 3-5 years \| More than 5 years \| \| Operating lease obligations(1) \| $15,091 \| $2,198 \| $4,165 \| $3,127 \| $5,601 \| \|… |
| 6 | `GOOGL_FY2020_2020-12-31:386` | Item 8 › Other Derivatives |  |  | \| \| Gains (Losses) Recognized in Income \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Year Ended December 31, \| \| \| \| \| \| \| \| 2018 \| \| 2019 \| \| 2020 \| \| \| \| Revenues \| Other income (expense), net \| Revenues \| Other incom… |
| 7 | `GOOGL_FY2020_2020-12-31:351` | Item 8 › Debt Securities |  |  | \| \| As of December 31, 2019 \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Less than 12 Months \| \| 12 Months or Greater \| \| Total \| \| \| \| Fair Value \| Unrealized Loss \| Fair Value \| Unrealized Loss \| Fair Value \| Unrealiz… |
| 8 | `GOOGL_FY2020_2020-12-31:352` | Item 8 › Debt Securities |  |  | \| \| As of December 31, 2020 \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Less than 12 Months \| \| 12 Months or Greater \| \| Total \| \| \| \| Fair Value \| Unrealized Loss \| Fair Value \| Unrealized Loss \| Fair Value \| Unrealiz… |
| 9 | `GOOGL_FY2020_2020-12-31:343` | Item 8 › Deferred Revenues and Remaining Performance Obligations |  |  | We record deferred revenues when cash payments are received or due in advance of our performance, including amounts which are refundable. Deferred revenues primarily relate to Google Cloud and Google other. Our total def… |
| 10 | `GOOGL_FY2020_2020-12-31:19` | NOTE ABOUT FORWARD-LOOKING STATEMENTS |  |  | •fluctuations in our revenue growth, as well as the change in paid clicks and cost-per-click and the change in impressions and cost-per-impression, and various factors contributing to such fluctuations; •our expectation … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `GOOGL_FY2020_2020-12-31:344`** (cited, gold #1)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Deferred Revenues and Remaining Performance Obligations
Additionally, we have performance obligations associated with commitments in customer contracts, primarily related to Google Cloud, for future services that have not yet been recognized as revenues, also referred to as remaining performance obligations. Remaining performance obligations include related deferred revenue currently recorded as well as amounts that will be invoiced in future periods, and excludes (i) contracts with an original expected term of one year or less, (ii) cancellable contracts, and (iii) contracts for which we recognize revenue at the amount to which we have the right to invoice for services performed. As of December 31, 2020, the amount not yet recognized as revenues from these commitments is $29.8 billion. We expect to recognize approximately half over the next 24 months with the remaining thereafter. However, the amount and timing of revenue recognition is largely driven by when the customer utilizes the services and our ability to deliver in accordance with relevant contract terms, which could impact our estimate of the remaining performance obligations and when we expect to recognize such as revenues. Table of Contents Alphabet Inc.
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Alphabet excluded from remaining performance obligations (i) contracts with an original expected term of one year or less, (ii) cancellable contracts, and (iii) contracts for which it recognizes revenue at the amount to which it has the right to invoice for services performed. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:344] | supported | The cited filing states remaining performance obligations exclude exactly those three categories of contracts. |

</details>
