# gold-031: Table + text (one filing)

[← all cases](../README.md) · company: Alphabet Inc. (GOOGL) · fiscal year: 2020 · recipe `table_text` · hop `multi` · answer type `mixed` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> By how much did Alphabet's gains (losses) in other income (expense), net from foreign exchange contracts not designated as hedging instruments change from 2019 to 2020, and what does Alphabet say its foreign exchange forward contracts are used for?

**Gold answer**

> $1,131 million, from a $413 million loss in 2019 to a $718 million gain in 2020. Alphabet uses foreign exchange forward contracts to offset the foreign exchange risk on assets and liabilities denominated in currencies other than the subsidiary's functional currency; the foreign currency gains and losses on those assets and liabilities are recorded in other income (expense), net and are offset by the gains and losses on the forward contracts.

**Program**: `subtract(718, -413)` → `1131.0`

**Gold numbers** (RQ2 numeric_accuracy targets): $1,131 million

**Key points** (RQ3 keypoint_recall targets)

1. 2019: a $413 million loss on foreign exchange contracts not designated as hedging instruments.
2. 2020: a $718 million gain.
3. The change was $1,131 million.
4. Forward contracts offset foreign exchange risk on assets and liabilities in non-functional currencies.
5. Gains and losses on those assets and liabilities are recorded in other income (expense), net and offset by the forward contracts.

**Gold evidence**

1. `GOOGL_FY2020_2020-12-31` · ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Other Derivatives · table

   > | Foreign exchange contracts | 0 | 54 | 0 | (413) | 0 | 718 |

2. `GOOGL_FY2020_2020-12-31` · ITEM 7A.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK › Foreign Currency Exchange Risk · text

   > We use foreign exchange forward contracts to offset the foreign exchange risk on our assets and liabilities denominated in currencies other than the functional currency of the subsidiary.

3. `GOOGL_FY2020_2020-12-31` · ITEM 7A.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK › Foreign Currency Exchange Risk · text

   > The foreign currency gains and losses on the assets and liabilities are recorded in other income (expense), net, which are offset by the gains and losses on the forward contracts.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 13 | 7 |
| recall@5 | 0.67 | 0.67 | 0.67 | 0.67 |
| recall@all | 1.00 | 0.67 | 1.00 | 0.67 |
| complete@all | 1 | 0 | 1 | 0 |
| average precision (lexical) | 0.62 | 0.64 | 0.75 | 0.56 |
| gold evidence first rank | #1: 8, #2: 1, #3: 1 | #1: –, #2: 2, #3: 2 | #1: 10, #2: 1, #3: 1 | #1: –, #2: 2, #3: 2 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✗ | ✓ | ✗ |
| keypoint_recall | 1.00 | 0.00 | 1.00 | 0.60 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 0.00 | 1.00 | 0.00 |
| citation precision | 1.00 | – | 1.00 | 1.00 |
| citation recall | 0.50 | – | 0.50 | 0.50 |
| citation F1 | 0.67 | – | 0.67 | 0.67 |
| has a citation | 1 | 0 | 1 | 1 |
| grounding error rate | – | – | 1.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 1 |
| tokens | 2480 | 1252 | 18594 | 11788 |
| cost (USD) | 0.0004 | 0.0002 | 0.0664 | 0.0428 |
| latency (s) | 2.1 | 5.7 | 27.4 | 16.5 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Alphabet’s gains (losses) in **other income (expense), net** from **foreign exchange contracts not designated as hedging instruments** changed from **$(413) million in 2019** to **$718 million in 2020**, an increase of **$1,131 million** [8].
>
> Alphabet says these contracts consist primarily of **foreign currency forward contracts used to hedge intercompany transactions and other monetary assets or liabilities denominated in currencies other than the functional currency of a subsidiary** [5].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2020_2020-12-31:423` | Item 8 › Other Income (Expense), Net |  | #2, #3 | (1) Interest expense is net of interest capitalized of $92 million, $167 million, and $218 million for the years ended December 31, 2018, 2019, and 2020, respectively. (2) Our foreign currency exchange gain (loss), net, … |
| 2 | `GOOGL_FY2020_2020-12-31:382` | Item 8 › Other Derivatives |  |  | Table of Contents Alphabet Inc. The gains (losses) on derivatives in cash flow hedging and net investment hedging relationships recognized in other comprehensive income ("OCI") are summarized below (in millions): |
| 3 | `GOOGL_FY2020_2020-12-31:378` | Item 8 › Other Derivatives |  |  | \| \| As of December 31, 2019 \| As of December 31, 2020 \| \|---\|---\|---\| \| Derivatives Designated as Hedging Instruments: \| \| \| \| Foreign exchange contracts \| \| \| \| Cash flow hedges \| $13,207 \| $10,187 \| \| Fair value hedges… |
| 4 | `GOOGL_FY2020_2020-12-31:386` | Item 8 › Other Derivatives |  |  | \| \| Gains (Losses) Recognized in Income \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Year Ended December 31, \| \| \| \| \| \| \| \| 2018 \| \| 2019 \| \| 2020 \| \| \| \| Revenues \| Other income (expense), net \| Revenues \| Other incom… |
| 5 | `GOOGL_FY2020_2020-12-31:377` | Item 8 › Other Derivatives | ✓ | #2, #3 | Other derivatives not designated as hedging instruments consist primarily of foreign currency forward contracts that we use to hedge intercompany transactions and other monetary assets or liabilities denominated in curre… |
| 6 | `GOOGL_FY2020_2020-12-31:385` | Item 8 › Other Derivatives |  | #3 | \| \| Gains (Losses) Recognized in Income \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Year Ended December 31, \| \| \| \| \| \| \| \| 2018 \| \| 2019 \| \| 2020 \| \| \| \| Revenues \| Other income (expense), net \| Revenues \| Other incom… |
| 7 | `GOOGL_FY2020_2020-12-31:255` | Item 7A › Foreign Currency Exchange Risk |  | #2 | If an adverse 10% foreign currency exchange rate change was applied to total monetary assets, liabilities, and commitments denominated in currencies other than the functional currencies at the balance sheet date, it woul… |
| 8 | `GOOGL_FY2020_2020-12-31:387` | Item 8 › Other Derivatives | ✓ | #1 | \| \| Gains (Losses) Recognized in Income \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Year Ended December 31, \| \| \| \| \| \| \| \| 2018 \| \| 2019 \| \| 2020 \| \| \| \| Revenues \| Other income (expense), net \| Revenues \| Other incom… |
| 9 | `GOOGL_FY2020_2020-12-31:383` | Item 8 › Other Derivatives |  |  | \| \| Gains (Losses) Recognized in OCI on Derivatives Before Tax Effect \| \| \| \|---\|---\|---\|---\| \| \| Year Ended December 31, \| \| \| \| \| 2018 \| 2019 \| 2020 \| \| Derivatives in Cash Flow Hedging Relationship: \| \| \| \| \| Foreign … |
| 10 | `GOOGL_FY2020_2020-12-31:213` | Item 7 › Other Income (Expense), Net |  |  | Other income (expense), net, increased $1,464 million from 2019 to 2020. The change was primarily driven by an increase in net gains on equity and debt securities of $3,519 million, partially offset by a $902 million los… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2020_2020-12-31:423`** (gold #2, gold #3)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Income (Expense), Net
(1) Interest expense is net of interest capitalized of $92 million, $167 million, and $218 million for the years ended December 31, 2018, 2019, and 2020, respectively. (2) Our foreign currency exchange gain (loss), net, is primarily related to the forward points for our foreign currency hedging contracts and foreign exchange transaction gains and losses from the conversion of the transaction currency to the functional currency, offset by the foreign currency hedging contracts' losses and gains. (3) During the year ended December 31, 2018, the terms of a non-marketable debt security were modified resulting in an unrealized $1.3 billion gain. (4) During the year ended December 31, 2020, we entered into derivatives that hedged the changes in fair value of certain marketable equity securities, which resulted in a $902 million loss. The offsetting recognized gains on the marketable equity securities are reflected in Gain (loss) on equity securities, net.
````

**#5 `GOOGL_FY2020_2020-12-31:377`** (cited, gold #2, gold #3)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Derivatives
Other derivatives not designated as hedging instruments consist primarily of foreign currency forward contracts that we use to hedge intercompany transactions and other monetary assets or liabilities denominated in currencies other than the functional currency of a subsidiary. Gains and losses on these contracts, as well as the related costs, are recognized in other income (expense), net, along with the foreign currency gains and losses on monetary assets and liabilities. We also use derivatives not designated as hedging instruments to manage risks relating to interest rates, equity and commodity prices, credit exposures and to enhance investment returns. The gross notional amounts of our outstanding derivative instruments were as follows (in millions):
````

**#6 `GOOGL_FY2020_2020-12-31:385`** (gold #3)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Derivatives (table)
|  | Gains (Losses) Recognized in Income |  |  |  |  |  |
|---|---|---|---|---|---|---|
|  | Year Ended December 31, |  |  |  |  |  |
|  | 2018 |  | 2019 |  | 2020 |  |
|  | Revenues | Other income (expense), net | Revenues | Other income (expense), net | Revenues | Other income (expense), net |
| Total amounts presented in the Consolidated Statements of Income in which the effects of cash flow and fair value hedges are recorded | $136,819 | $7,389 | $161,857 | $5,394 | $182,527 | $6,858 |
| Gains (Losses) on Derivatives in Cash Flow Hedging Relationship: |  |  |  |  |  |  |
| Foreign exchange contracts |  |  |  |  |  |  |
| Amount of gains (losses) reclassified from AOCI to income | $(139) | $0 | $367 | $0 | $144 | $0 |
| Amount excluded from the assessment of effectiveness recognized in earnings based on an amortization approach | 1 | 0 | 88 | 0 | 33 | 0 |
| Gains (Losses) on Derivatives in Fair Value Hedging Relationship: |  |  |  |  |  |  |
````

**#7 `GOOGL_FY2020_2020-12-31:255`** (gold #2)

````text
ITEM 7A.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK > Foreign Currency Exchange Risk
If an adverse 10% foreign currency exchange rate change was applied to total monetary assets, liabilities, and commitments denominated in currencies other than the functional currencies at the balance sheet date, it would have resulted in an adverse effect on income before income taxes of approximately $8 million and $497 million as of Table of Contents Alphabet Inc. December 31, 2019 and 2020, respectively, after consideration of the effect of foreign exchange contracts in place for the years ended December 31, 2019 and 2020.
````

**#8 `GOOGL_FY2020_2020-12-31:387`** (cited, gold #1)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Derivatives (table)
|  | Gains (Losses) Recognized in Income |  |  |  |  |  |
|---|---|---|---|---|---|---|
|  | Year Ended December 31, |  |  |  |  |  |
|  | 2018 |  | 2019 |  | 2020 |  |
|  | Revenues | Other income (expense), net | Revenues | Other income (expense), net | Revenues | Other income (expense), net |
| Foreign exchange contracts | 0 | 54 | 0 | (413) | 0 | 718 |
| Other Contracts | 0 | 0 | 0 | 0 | 0 | (906) |
| Total gains (losses) | $(138) | $169 | $455 | $(145) | $177 | $(33) |
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7A')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2020_2020-12-31:189` | Item 7 › Use of Constant Currency Revenues and Constant Currency Revenue Percentage Change |  |  | (1) Total revenues and hedging gains (losses) for the year ended December 31, 2018 were $136,819 million and $(138) million, respectively. EMEA revenue percentage change from 2019 to 2020 was not significantly affected b… |
| 2 | `GOOGL_FY2020_2020-12-31:377` | Item 8 › Other Derivatives |  | #2, #3 | Other derivatives not designated as hedging instruments consist primarily of foreign currency forward contracts that we use to hedge intercompany transactions and other monetary assets or liabilities denominated in curre… |
| 3 | `GOOGL_FY2020_2020-12-31:257` | Item 7A › Foreign Currency Exchange Risk |  | #2 | If the U.S. dollar weakened by 10% as of December 31, 2019 and 2020, the amount recorded in AOCI related to our foreign exchange contracts before tax effect would have been approximately $1.1 billion and $912 million low… |
| 4 | `GOOGL_FY2020_2020-12-31:423` | Item 8 › Other Income (Expense), Net |  | #2, #3 | (1) Interest expense is net of interest capitalized of $92 million, $167 million, and $218 million for the years ended December 31, 2018, 2019, and 2020, respectively. (2) Our foreign currency exchange gain (loss), net, … |
| 5 | `GOOGL_FY2020_2020-12-31:256` | Item 7A › Foreign Currency Exchange Risk |  |  | We use foreign currency forwards and option contracts, including collars (an option strategy comprised of a combination of purchased and written options) to protect our forecasted U.S. dollar-equivalent earnings from cha… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `GOOGL_FY2020_2020-12-31:377`** (gold #2, gold #3)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Derivatives
Other derivatives not designated as hedging instruments consist primarily of foreign currency forward contracts that we use to hedge intercompany transactions and other monetary assets or liabilities denominated in currencies other than the functional currency of a subsidiary. Gains and losses on these contracts, as well as the related costs, are recognized in other income (expense), net, along with the foreign currency gains and losses on monetary assets and liabilities. We also use derivatives not designated as hedging instruments to manage risks relating to interest rates, equity and commodity prices, credit exposures and to enhance investment returns. The gross notional amounts of our outstanding derivative instruments were as follows (in millions):
````

**#3 `GOOGL_FY2020_2020-12-31:257`** (gold #2)

````text
ITEM 7A.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK > Foreign Currency Exchange Risk
If the U.S. dollar weakened by 10% as of December 31, 2019 and 2020, the amount recorded in AOCI related to our foreign exchange contracts before tax effect would have been approximately $1.1 billion and $912 million lower as of December 31, 2019 and 2020, respectively. The change in the value recorded in AOCI would be expected to offset a corresponding foreign currency change in forecasted hedged revenues when recognized. We use foreign exchange forward contracts designated as net investment hedges to hedge the foreign currency risks related to our investment in foreign subsidiaries. These forward contracts serve to offset the foreign currency translation risk from our foreign operations. If the U.S. dollar weakened by 10%, the amount recorded in cumulative translation adjustment ("CTA") within AOCI related to our net investment hedge would have been approximately $936 million and $1 billion lower as of December 31, 2019 and 2020, respectively. The change in value recorded in CTA would be expected to offset a corresponding foreign currency translation gain or loss from our investment in foreign subsidiaries.
````

**#4 `GOOGL_FY2020_2020-12-31:423`** (gold #2, gold #3)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Income (Expense), Net
(1) Interest expense is net of interest capitalized of $92 million, $167 million, and $218 million for the years ended December 31, 2018, 2019, and 2020, respectively. (2) Our foreign currency exchange gain (loss), net, is primarily related to the forward points for our foreign currency hedging contracts and foreign exchange transaction gains and losses from the conversion of the transaction currency to the functional currency, offset by the foreign currency hedging contracts' losses and gains. (3) During the year ended December 31, 2018, the terms of a non-marketable debt security were modified resulting in an unrealized $1.3 billion gain. (4) During the year ended December 31, 2020, we entered into derivatives that hedged the changes in fair value of certain marketable equity securities, which resulted in a $902 million loss. The offsetting recognized gains on the marketable equity securities are reflected in Gain (loss) on equity securities, net.
````

</details>

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 13, cited: 2.

**Generated answer**

> Alphabet’s gains (losses) in other income (expense), net from foreign exchange contracts not designated as hedging instruments changed from $(413) million in 2019 to $718 million in 2020, an increase of $1,131 million. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:387]
>
> Alphabet says other derivatives not designated as hedging instruments consist primarily of foreign currency forward contracts that it uses to hedge intercompany transactions and other monetary assets or liabilities denominated in currencies other than the functional currency of a subsidiary. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:377]
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 718, 1,131; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2020_2020-12-31:423` | Item 8 › Other Income (Expense), Net |  | #2, #3 | (1) Interest expense is net of interest capitalized of $92 million, $167 million, and $218 million for the years ended December 31, 2018, 2019, and 2020, respectively. (2) Our foreign currency exchange gain (loss), net, … |
| 2 | `GOOGL_FY2020_2020-12-31:377` | Item 8 › Other Derivatives | ✓ | #2, #3 | Other derivatives not designated as hedging instruments consist primarily of foreign currency forward contracts that we use to hedge intercompany transactions and other monetary assets or liabilities denominated in curre… |
| 3 | `GOOGL_FY2020_2020-12-31:386` | Item 8 › Other Derivatives |  |  | \| \| Gains (Losses) Recognized in Income \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Year Ended December 31, \| \| \| \| \| \| \| \| 2018 \| \| 2019 \| \| 2020 \| \| \| \| Revenues \| Other income (expense), net \| Revenues \| Other incom… |
| 4 | `GOOGL_FY2020_2020-12-31:378` | Item 8 › Other Derivatives |  |  | \| \| As of December 31, 2019 \| As of December 31, 2020 \| \|---\|---\|---\| \| Derivatives Designated as Hedging Instruments: \| \| \| \| Foreign exchange contracts \| \| \| \| Cash flow hedges \| $13,207 \| $10,187 \| \| Fair value hedges… |
| 5 | `GOOGL_FY2020_2020-12-31:385` | Item 8 › Other Derivatives |  | #3 | \| \| Gains (Losses) Recognized in Income \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Year Ended December 31, \| \| \| \| \| \| \| \| 2018 \| \| 2019 \| \| 2020 \| \| \| \| Revenues \| Other income (expense), net \| Revenues \| Other incom… |
| 6 | `GOOGL_FY2020_2020-12-31:383` | Item 8 › Other Derivatives |  |  | \| \| Gains (Losses) Recognized in OCI on Derivatives Before Tax Effect \| \| \| \|---\|---\|---\|---\| \| \| Year Ended December 31, \| \| \| \| \| 2018 \| 2019 \| 2020 \| \| Derivatives in Cash Flow Hedging Relationship: \| \| \| \| \| Foreign … |
| 7 | `GOOGL_FY2020_2020-12-31:381` | Item 8 › Other Derivatives |  |  | \| \| \| As of December 31, 2020 \| \| \| \|---\|---\|---\|---\|---\| \| \| Balance Sheet Location \| Fair Value of Derivatives Designated as Hedging Instruments \| Fair Value of Derivatives Not Designated as Hedging Instruments \| Total… |
| 8 | `GOOGL_FY2020_2020-12-31:382` | Item 8 › Other Derivatives |  |  | Table of Contents Alphabet Inc. The gains (losses) on derivatives in cash flow hedging and net investment hedging relationships recognized in other comprehensive income ("OCI") are summarized below (in millions): |
| 9 | `GOOGL_FY2020_2020-12-31:380` | Item 8 › Other Derivatives |  |  | \| \| \| As of December 31, 2019 \| \| \| \|---\|---\|---\|---\|---\| \| \| Balance Sheet Location \| Fair Value of Derivatives Designated as Hedging Instruments \| Fair Value of Derivatives Not Designated as Hedging Instruments \| Total… |
| 10 | `GOOGL_FY2020_2020-12-31:387` | Item 8 › Other Derivatives | ✓ | #1 | \| \| Gains (Losses) Recognized in Income \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Year Ended December 31, \| \| \| \| \| \| \| \| 2018 \| \| 2019 \| \| 2020 \| \| \| \| Revenues \| Other income (expense), net \| Revenues \| Other incom… |
| 11 | `GOOGL_FY2020_2020-12-31:212` | Item 7 › Other Income (Expense), Net |  |  | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2019 \| 2020 \| \| Other income (expense), net \| $5,394 \| $6,858 \| |
| 12 | `GOOGL_FY2020_2020-12-31:211` | Item 7 › Other Income (Expense), Net |  |  | The following table presents other income (expense), net, (in millions): |
| 13 | `GOOGL_FY2020_2020-12-31:422` | Item 8 › Other Income (Expense), Net |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2018 \| 2019 \| 2020 \| \| Interest income \| $1,878 \| $2,427 \| $1,865 \| \| Interest expense(1) \| (114) \| (100) \| (135) \| \| Foreign currency exchange gain (loss), net (2)… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2020_2020-12-31:423`** (gold #2, gold #3)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Income (Expense), Net
(1) Interest expense is net of interest capitalized of $92 million, $167 million, and $218 million for the years ended December 31, 2018, 2019, and 2020, respectively. (2) Our foreign currency exchange gain (loss), net, is primarily related to the forward points for our foreign currency hedging contracts and foreign exchange transaction gains and losses from the conversion of the transaction currency to the functional currency, offset by the foreign currency hedging contracts' losses and gains. (3) During the year ended December 31, 2018, the terms of a non-marketable debt security were modified resulting in an unrealized $1.3 billion gain. (4) During the year ended December 31, 2020, we entered into derivatives that hedged the changes in fair value of certain marketable equity securities, which resulted in a $902 million loss. The offsetting recognized gains on the marketable equity securities are reflected in Gain (loss) on equity securities, net.
````

**#2 `GOOGL_FY2020_2020-12-31:377`** (cited, gold #2, gold #3)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Derivatives
Other derivatives not designated as hedging instruments consist primarily of foreign currency forward contracts that we use to hedge intercompany transactions and other monetary assets or liabilities denominated in currencies other than the functional currency of a subsidiary. Gains and losses on these contracts, as well as the related costs, are recognized in other income (expense), net, along with the foreign currency gains and losses on monetary assets and liabilities. We also use derivatives not designated as hedging instruments to manage risks relating to interest rates, equity and commodity prices, credit exposures and to enhance investment returns. The gross notional amounts of our outstanding derivative instruments were as follows (in millions):
````

**#5 `GOOGL_FY2020_2020-12-31:385`** (gold #3)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Derivatives (table)
|  | Gains (Losses) Recognized in Income |  |  |  |  |  |
|---|---|---|---|---|---|---|
|  | Year Ended December 31, |  |  |  |  |  |
|  | 2018 |  | 2019 |  | 2020 |  |
|  | Revenues | Other income (expense), net | Revenues | Other income (expense), net | Revenues | Other income (expense), net |
| Total amounts presented in the Consolidated Statements of Income in which the effects of cash flow and fair value hedges are recorded | $136,819 | $7,389 | $161,857 | $5,394 | $182,527 | $6,858 |
| Gains (Losses) on Derivatives in Cash Flow Hedging Relationship: |  |  |  |  |  |  |
| Foreign exchange contracts |  |  |  |  |  |  |
| Amount of gains (losses) reclassified from AOCI to income | $(139) | $0 | $367 | $0 | $144 | $0 |
| Amount excluded from the assessment of effectiveness recognized in earnings based on an amortization approach | 1 | 0 | 88 | 0 | 33 | 0 |
| Gains (Losses) on Derivatives in Fair Value Hedging Relationship: |  |  |  |  |  |  |
````

**#10 `GOOGL_FY2020_2020-12-31:387`** (cited, gold #1)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Derivatives (table)
|  | Gains (Losses) Recognized in Income |  |  |  |  |  |
|---|---|---|---|---|---|---|
|  | Year Ended December 31, |  |  |  |  |  |
|  | 2018 |  | 2019 |  | 2020 |  |
|  | Revenues | Other income (expense), net | Revenues | Other income (expense), net | Revenues | Other income (expense), net |
| Foreign exchange contracts | 0 | 54 | 0 | (413) | 0 | 718 |
| Other Contracts | 0 | 0 | 0 | 0 | 0 | (906) |
| Total gains (losses) | $(138) | $169 | $455 | $(145) | $177 | $(33) |
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 2, verified 0, ungrounded 2, uncited 0, derived 0; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 718, 1,131

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Alphabet’s gains (losses) in other income (expense), net from foreign exchange contracts not designated as hedging instruments changed from $(413) million in 2019 to $718 million in 2020, an increase of $1,131 million. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:387] | None |  |
| Alphabet says other derivatives not designated as hedging instruments consist primarily of foreign currency forward contracts that it uses to hedge intercompany transactions and other monetary assets or liabilities denominated in currencies other than the functional currency of a subsidiary. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:377] | supported | The cited text states this verbatim. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 3.

**Generated answer**

> The provided evidence blocks do not disclose gains (losses) in other income (expense), net from foreign exchange contracts not designated as hedging instruments for 2019 and 2020, so the change between those years is not disclosed in the provided evidence. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:385] [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:386]
>
> Alphabet says other derivatives not designated as hedging instruments consist primarily of foreign currency forward contracts used to hedge intercompany transactions and other monetary assets or liabilities denominated in currencies other than the functional currency of a subsidiary. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:377]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-GOOGL-2020` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2020,2020-12-31,182527000000,40269000000,41224000000,319616000… |
| 2 | `GOOGL_FY2020_2020-12-31:423` | Item 8 › Other Income (Expense), Net |  | #2, #3 | (1) Interest expense is net of interest capitalized of $92 million, $167 million, and $218 million for the years ended December 31, 2018, 2019, and 2020, respectively. (2) Our foreign currency exchange gain (loss), net, … |
| 3 | `GOOGL_FY2020_2020-12-31:377` | Item 8 › Other Derivatives | ✓ | #2, #3 | Other derivatives not designated as hedging instruments consist primarily of foreign currency forward contracts that we use to hedge intercompany transactions and other monetary assets or liabilities denominated in curre… |
| 4 | `GOOGL_FY2020_2020-12-31:386` | Item 8 › Other Derivatives | ✓ |  | \| \| Gains (Losses) Recognized in Income \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Year Ended December 31, \| \| \| \| \| \| \| \| 2018 \| \| 2019 \| \| 2020 \| \| \| \| Revenues \| Other income (expense), net \| Revenues \| Other incom… |
| 5 | `GOOGL_FY2020_2020-12-31:378` | Item 8 › Other Derivatives |  |  | \| \| As of December 31, 2019 \| As of December 31, 2020 \| \|---\|---\|---\| \| Derivatives Designated as Hedging Instruments: \| \| \| \| Foreign exchange contracts \| \| \| \| Cash flow hedges \| $13,207 \| $10,187 \| \| Fair value hedges… |
| 6 | `GOOGL_FY2020_2020-12-31:385` | Item 8 › Other Derivatives | ✓ | #3 | \| \| Gains (Losses) Recognized in Income \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\| \| \| Year Ended December 31, \| \| \| \| \| \| \| \| 2018 \| \| 2019 \| \| 2020 \| \| \| \| Revenues \| Other income (expense), net \| Revenues \| Other incom… |
| 7 | `GOOGL_FY2020_2020-12-31:383` | Item 8 › Other Derivatives |  |  | \| \| Gains (Losses) Recognized in OCI on Derivatives Before Tax Effect \| \| \| \|---\|---\|---\|---\| \| \| Year Ended December 31, \| \| \| \| \| 2018 \| 2019 \| 2020 \| \| Derivatives in Cash Flow Hedging Relationship: \| \| \| \| \| Foreign … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `GOOGL_FY2020_2020-12-31:423`** (gold #2, gold #3)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Income (Expense), Net
(1) Interest expense is net of interest capitalized of $92 million, $167 million, and $218 million for the years ended December 31, 2018, 2019, and 2020, respectively. (2) Our foreign currency exchange gain (loss), net, is primarily related to the forward points for our foreign currency hedging contracts and foreign exchange transaction gains and losses from the conversion of the transaction currency to the functional currency, offset by the foreign currency hedging contracts' losses and gains. (3) During the year ended December 31, 2018, the terms of a non-marketable debt security were modified resulting in an unrealized $1.3 billion gain. (4) During the year ended December 31, 2020, we entered into derivatives that hedged the changes in fair value of certain marketable equity securities, which resulted in a $902 million loss. The offsetting recognized gains on the marketable equity securities are reflected in Gain (loss) on equity securities, net.
````

**#3 `GOOGL_FY2020_2020-12-31:377`** (cited, gold #2, gold #3)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Derivatives
Other derivatives not designated as hedging instruments consist primarily of foreign currency forward contracts that we use to hedge intercompany transactions and other monetary assets or liabilities denominated in currencies other than the functional currency of a subsidiary. Gains and losses on these contracts, as well as the related costs, are recognized in other income (expense), net, along with the foreign currency gains and losses on monetary assets and liabilities. We also use derivatives not designated as hedging instruments to manage risks relating to interest rates, equity and commodity prices, credit exposures and to enhance investment returns. The gross notional amounts of our outstanding derivative instruments were as follows (in millions):
````

**#4 `GOOGL_FY2020_2020-12-31:386`** (cited)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Derivatives (table)
|  | Gains (Losses) Recognized in Income |  |  |  |  |  |
|---|---|---|---|---|---|---|
|  | Year Ended December 31, |  |  |  |  |  |
|  | 2018 |  | 2019 |  | 2020 |  |
|  | Revenues | Other income (expense), net | Revenues | Other income (expense), net | Revenues | Other income (expense), net |
| Foreign exchange contracts |  |  |  |  |  |  |
| Hedged items | 0 | (96) | 0 | (19) | 0 | 18 |
| Derivatives designated as hedging instruments | 0 | 96 | 0 | 19 | 0 | (18) |
| Amount excluded from the assessment of effectiveness | 0 | 37 | 0 | 25 | 0 | 4 |
| Gains (Losses) on Derivatives in Net Investment Hedging Relationship: |  |  |  |  |  |  |
| Foreign exchange contracts |  |  |  |  |  |  |
| Amount excluded from the assessment of effectiveness | 0 | 78 | 0 | 243 | 0 | 151 |
| Gains (Losses) on Derivatives Not Designated as Hedging Instruments: |  |  |  |  |  |  |
````

**#6 `GOOGL_FY2020_2020-12-31:385`** (cited, gold #3)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Derivatives (table)
|  | Gains (Losses) Recognized in Income |  |  |  |  |  |
|---|---|---|---|---|---|---|
|  | Year Ended December 31, |  |  |  |  |  |
|  | 2018 |  | 2019 |  | 2020 |  |
|  | Revenues | Other income (expense), net | Revenues | Other income (expense), net | Revenues | Other income (expense), net |
| Total amounts presented in the Consolidated Statements of Income in which the effects of cash flow and fair value hedges are recorded | $136,819 | $7,389 | $161,857 | $5,394 | $182,527 | $6,858 |
| Gains (Losses) on Derivatives in Cash Flow Hedging Relationship: |  |  |  |  |  |  |
| Foreign exchange contracts |  |  |  |  |  |  |
| Amount of gains (losses) reclassified from AOCI to income | $(139) | $0 | $367 | $0 | $144 | $0 |
| Amount excluded from the assessment of effectiveness recognized in earnings based on an amortization approach | 1 | 0 | 88 | 0 | 33 | 0 |
| Gains (Losses) on Derivatives in Fair Value Hedging Relationship: |  |  |  |  |  |  |
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 7A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 2, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| The provided evidence blocks do not disclose gains (losses) in other income (expense), net from foreign exchange contracts not designated as hedging instruments for 2019 and 2020, so the change between those years is not disclosed in the provided evidence. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:385] [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:386] | supported | The cited table cuts off before any amounts for derivatives not designated as hedging instruments, so 2019 and 2020 values and their change are not disclosed in the provided evidence. |
| Alphabet says other derivatives not designated as hedging instruments consist primarily of foreign currency forward contracts used to hedge intercompany transactions and other monetary assets or liabilities denominated in currencies other than the functional currency of a subsidiary. [GOOGL FY2020, Item 8, GOOGL_FY2020_2020-12-31:377] | supported | The cited text states that other derivatives not designated as hedging instruments consist primarily of foreign currency forward contracts used to hedge intercompany transactions and other monetary assets or liabilities in non-functional currencies. |

</details>
