# gold-095: Cross-company text

[← all cases](../README.md) · company: Alphabet Inc.; Meta Platforms, Inc. (GOOGL, META) · fiscal year: 2023 · recipe `cross_company_text` · hop `multi` · answer type `qualitative` · scope `cross_company` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> How do Alphabet and Meta Platforms differ in their stated strategies for managing foreign currency exchange risk in their 2023 10-K filings, specifically regarding the use of derivative instruments?

**Gold answer**

> Alphabet actively uses derivative instruments, including foreign currency forward and option contracts (such as collars), to hedge foreign currency risk on assets, liabilities, and forecasted earnings. In contrast, Meta Platforms stated that as of its 2023 filing, it had not entered into derivatives or other financial instruments to hedge its foreign currency exchange risk, though it acknowledged it might do so in the future.

**Key points** (RQ3 keypoint_recall targets)

1. Alphabet uses derivative instruments to hedge foreign currency risk.
2. Meta Platforms had not entered into derivatives to hedge foreign currency risk as of the 2023 filing.
3. The comparison highlights a divergence in risk management strategy between the two companies.

**Gold evidence**

1. `GOOGL_FY2023_2023-12-31` · ITEM 7A.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK › Foreign Currency Exchange Risk · text

   > As discussed below, we enter into derivative instruments to hedge foreign currency risk.

2. `META_FY2023_2023-12-31` · Item 7A.Quantitative and Qualitative Disclosures About Market Risk › Foreign Currency Exchange Risk · text

   > At this time, we have not entered into, but in the future we may enter into, derivatives or other financial instruments in an attempt to hedge our foreign currency exchange risk.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 9 | 5 | 15 | 6 |
| recall@5 | 0.00 | 1.00 | 0.50 | 0.50 |
| recall@all | 0.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 0 | 1 | 1 | 1 |
| average precision (lexical) | 0.00 | 0.95 | 0.88 | 0.92 |
| gold evidence first rank | #1: –, #2: – | #1: 1, #2: 5 | #1: 1, #2: 8 | #1: 1, #2: 6 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | 1.00 | 0.67 | 0.67 | 0.67 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | – | 0.67 | 0.67 | 0.67 |
| citation recall | – | 1.00 | 1.00 | 1.00 |
| citation F1 | – | 0.80 | 0.80 | 0.80 |
| has a citation | 0 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 1 |
| tokens | 2834 | 1175 | 18300 | 7307 |
| cost (USD) | 0.0005 | 0.0002 | 0.0710 | 0.0299 |
| latency (s) | 3.7 | 6.1 | 40.4 | 13.1 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 9, cited: 0.

**Generated answer**

> The provided context includes Meta Platforms only and does not include Alphabet’s 2023 10-K, so I can answer only part of the question.
>
> For Meta Platforms, the context provided does not state any strategy for managing foreign currency exchange risk or any use of derivative instruments. Therefore, Meta’s specific stated strategy on this topic is not in the provided context.
>
> What is not in the context:
> - Alphabet’s stated strategy for managing foreign currency exchange risk in its 2023 10-K
> - Meta Platforms’ stated strategy for managing foreign currency exchange risk in its 2023 10-K
> - Any comparison between the two regarding derivative instruments
>
> The only relevant conclusion from the provided context is that the answer is not available from these excerpts.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2023_2023-12-31:8` | Securities registered pursuant to Section 12(g) of the Act: None |  |  | Indicate by check mark whether the registrant is a large accelerated filer, an accelerated filer, a non-accelerated filer, a smaller reporting company, or an emerging growth company. See the definitions of "large acceler… |
| 2 | `META_FY2023_2023-12-31:16` | NOTE ABOUT FORWARD-LOOKING STATEMENTS |  |  | those contained in any forward-looking statements we may make. In light of these risks, uncertainties and assumptions, the future events and trends discussed in this Annual Report on Form 10-K may not occur and actual re… |
| 3 | `META_FY2023_2023-12-31:10` | Securities registered pursuant to Section 12(g) of the Act: None |  |  | If an emerging growth company, indicate by check mark if the registrant has elected not to use the extended transition period for complying with any new or revised financial accounting standards provided pursuant to Sect… |
| 4 | `META_FY2023_2023-12-31:629` | Item 15 |  |  | \| Exhibit \| \| Incorporated by Reference \| \| \| Filed Herewith \| \|---\|---\|---\|---\|---\|---\| \| 10.2(L)+ \| 2012 Equity Incentive Plan forms of award agreements (Additional Forms). \| 10-Q \| 001-35551 \| 10.1 \| April 27, 2023 \| … |
| 5 | `META_FY2023_2023-12-31:630` | Item 15 |  |  | \| Exhibit \| \| Incorporated by Reference \| \| \| Filed Herewith \| \|---\|---\|---\|---\|---\|---\| \| 10.9+ \| Form of Executive Officer Offer Letter. \| 10-Q \| 001-35551 \| 10.3 \| July 25, 2019 \| \| 10.10+ \| Director Compensation Poli… |
| 6 | `META_FY2023_2023-12-31:627` | Item 15 |  |  | \| Exhibit \| \| Incorporated by Reference \| \| \| Filed Herewith \| \|---\|---\|---\|---\|---\|---\| \| 4.5 \| Second Supplemental Indenture, dated as of May 3, 2023, by and between Meta Platforms, Inc. and U.S. Bank Trust Company, Na… |
| 7 | `META_FY2023_2023-12-31:247` | Item 1A › The trading price of our Class A common stock has been and will likely continue to be volatile. |  |  | •additional shares of our stock being sold into the market by us, our existing stockholders, or in connection with acquisitions, or the anticipation of such sales; •investor sentiment with respect to our competitors, our… |
| 8 | `META_FY2023_2023-12-31:626` | Item 15 |  |  | \| Exhibit \| \| Incorporated by Reference \| \| \| Filed Herewith \| \|---\|---\|---\|---\|---\|---\| \| Number \| Exhibit Description \| Form \| File No. \| Exhibit \| Filing Date \| \| 3.1 \| Amended and Restated Certificate of Incorporatio… |
| 9 | `META_FY2023_2023-12-31:637` | Item 16 › SIGNATURES |  |  | \| \| \| META PLATFORMS, INC. \| \|---\|---\|---\| \| Date: \| February 1, 2024 \| /s/ Susan Li \| \| \| \| Susan Li \| \| \| \| Chief Financial Officer \| |

RQ2 citation match (section level): `no citations`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 4.

**Generated answer**

> Alphabet states that it actively uses derivative instruments—specifically foreign currency forward and option contracts—to hedge foreign currency exchange risk and reduce the impact of exchange-rate movements on cash flows, earnings, investments, and certain assets and liabilities [1][2][3].  
>
> Meta Platforms states that, as of its 2023 10-K, it had not entered into derivatives or other financial instruments to hedge foreign currency exchange risk, though it may do so in the future [5].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2023_2023-12-31:373` | Item 8 › Derivative Financial Instruments | ✓ | #1 | We use derivative instruments to manage risks relating to our ongoing business operations. The primary risk managed is foreign exchange risk. We use foreign currency contracts to reduce the risk that our cash flows, earn… |
| 2 | `GOOGL_FY2023_2023-12-31:255` | Item 7A › Foreign Currency Exchange Risk | ✓ | #1 | We transact business globally in multiple currencies. International revenues, as well as costs and expenses denominated in foreign currencies, expose us to the risk of fluctuations in foreign currency exchange rates agai… |
| 3 | `GOOGL_FY2023_2023-12-31:377` | Item 8 › Other Derivatives | ✓ | #1 | We enter into foreign currency forward and option contracts that are not designated as hedging instruments to hedge intercompany transactions and other monetary assets or liabilities denominated in currencies other than … |
| 4 | `GOOGL_FY2023_2023-12-31:316` | Item 8 › Credit Risks |  |  | We are subject to credit risk primarily from cash equivalents, marketable debt securities, derivative financial instruments, including foreign exchange contracts, and accounts receivable. We manage our credit risk exposu… |
| 5 | `META_FY2023_2023-12-31:402` | Item 7A › Foreign Currency Exchange Risk | ✓ | #1, #2 | We have experienced and will continue to experience fluctuations in our net income as a result of transaction gains or losses related to remeasuring monetary asset and liability balances that are denominated in currencie… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2023_2023-12-31:373`** (cited, gold #1)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Derivative Financial Instruments
We use derivative instruments to manage risks relating to our ongoing business operations. The primary risk managed is foreign exchange risk. We use foreign currency contracts to reduce the risk that our cash flows, earnings, and investment in foreign subsidiaries will be adversely affected by foreign currency exchange rate fluctuations. We also enter into derivative instruments to partially offset our exposure to other risks and enhance investment returns. We recognize derivative instruments in the Consolidated Balance Sheets at fair value and classify the derivatives primarily within Level 2 in the fair value hierarchy. We present our collar contracts (an option strategy comprised of a combination of purchased and written options) at net fair values and present all other derivatives at gross fair values. The accounting treatment for derivatives is based on the intended use and hedge designation.
````

**#2 `GOOGL_FY2023_2023-12-31:255`** (cited, gold #1)

````text
ITEM 7A.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK > Foreign Currency Exchange Risk
We transact business globally in multiple currencies. International revenues, as well as costs and expenses denominated in foreign currencies, expose us to the risk of fluctuations in foreign currency exchange rates against the U.S. dollar. As discussed below, we enter into derivative instruments to hedge foreign currency risk. Principal currencies hedged included the Australian dollar, British pound, Canadian dollar, Euro, and Japanese yen. For the purpose of analyzing foreign currency exchange risk, we considered the historical trends in foreign currency exchange rates and determined that it was reasonably possible that adverse changes in exchange rates of 10% could be experienced. We use foreign currency forward and option contracts to offset the foreign exchange risk on assets and liabilities denominated in currencies other than the functional currency of the subsidiary. These forward and option contracts reduce, but do not entirely eliminate, the effect of foreign currency exchange rate movements on our assets and liabilities. The foreign currency gains and losses on these assets and liabilities are recorded in OI&E, which are offset by the gains and losses on the forward and option contracts.
````

**#3 `GOOGL_FY2023_2023-12-31:377`** (cited, gold #1)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Derivatives
We enter into foreign currency forward and option contracts that are not designated as hedging instruments to hedge intercompany transactions and other monetary assets or liabilities denominated in currencies other than the functional currency of a subsidiary. Gains and losses on these derivatives that are not designated as accounting hedges are primarily recorded in OI&E along with the foreign currency gains and losses on monetary assets and liabilities. We also use derivatives not designated as hedging instruments to manage risks relating to interest rates, commodity prices, credit exposures, and to enhance investment returns. From time to time, we enter into derivatives to hedge the market price risk on certain of our marketable equity securities. Gains and losses arising from other derivatives are primarily reflected within the “other” component of OI&E. See Note 7 for further details. 68. Table of Contents Alphabet Inc. The gross notional amounts of outstanding derivative instruments were as follows (in millions):
````

**#5 `META_FY2023_2023-12-31:402`** (cited, gold #1, gold #2)

````text
Item 7A.Quantitative and Qualitative Disclosures About Market Risk > Foreign Currency Exchange Risk
We have experienced and will continue to experience fluctuations in our net income as a result of transaction gains or losses related to remeasuring monetary asset and liability balances that are denominated in currencies other than the functional currency of the entities in which they are recorded. At this time, we have not entered into, but in the future we may enter into, derivatives or other financial instruments in an attempt to hedge our foreign currency exchange risk. It is difficult to predict the effect hedging activities would have on our results of operations. Foreign currency exchange net losses of $366 million, $81 million, and $140 million were recognized in 2023, 2022, and 2021, respectively.
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8'), ('GOOGL', 'Item 7A'), ('META', 'Item 7A')] gold=[(None, 'Item 7A')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 15, cited: 7.

**Generated answer**

> Alphabet states that it uses derivative instruments to manage risks relating to its ongoing business operations, with foreign exchange risk identified as the primary risk managed. [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:373] Alphabet says it uses foreign currency contracts to reduce the risk that its cash flows, earnings, and investment in foreign subsidiaries will be adversely affected by foreign currency exchange rate fluctuations. [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:373] Alphabet also states that it enters into foreign currency forward and option contracts to hedge foreign currency risk, and that principal currencies hedged included the Australian dollar, British pound, Canadian dollar, Euro, and Japanese yen. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:255] Alphabet further says it uses foreign currency forward and option contracts, including collars, to protect forecasted U.S. dollar-equivalent earnings from changes in foreign currency exchange rates, designates these contracts as cash flow hedges for accounting purposes, and uses foreign exchange forward contracts designated as net investment hedges to hedge foreign currency risks related to investments in foreign subsidiaries. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:257] [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:258] Alphabet also uses foreign currency forward and option contracts that are not designated as hedging instruments to hedge intercompany transactions and other monetary assets or liabilities denominated in currencies other than the functional currency of a subsidiary. [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:377]
>
> Meta states that it is exposed to foreign currency exchange risk related to revenue and operating expenses denominated in currencies other than the U.S. dollar, primarily the Euro. [META FY2023, Item 7A, META_FY2023_2023-12-31:401] However, Meta says that, at this time, it has not entered into derivatives or other financial instruments to hedge its foreign currency exchange risk, although it may do so in the future. [META FY2023, Item 7A, META_FY2023_2023-12-31:402] Meta therefore describes foreign currency transaction gains or losses from remeasuring monetary asset and liability balances, rather than an active derivative hedging program. [META FY2023, Item 7A, META_FY2023_2023-12-31:402]
>
> In short, Alphabet describes an active and multi-faceted derivative hedging strategy for foreign currency risk, including cash flow hedges, net investment hedges, and non-designated derivatives, while Meta says it had not entered into derivatives or other financial instruments to hedge foreign currency exchange risk as of its 2023 filing. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:257] [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:258] [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:377] [META FY2023, Item 7A, META_FY2023_2023-12-31:402]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2023_2023-12-31:373` | Item 8 › Derivative Financial Instruments | ✓ | #1 | We use derivative instruments to manage risks relating to our ongoing business operations. The primary risk managed is foreign exchange risk. We use foreign currency contracts to reduce the risk that our cash flows, earn… |
| 2 | `GOOGL_FY2023_2023-12-31:255` | Item 7A › Foreign Currency Exchange Risk | ✓ | #1 | We transact business globally in multiple currencies. International revenues, as well as costs and expenses denominated in foreign currencies, expose us to the risk of fluctuations in foreign currency exchange rates agai… |
| 3 | `GOOGL_FY2023_2023-12-31:377` | Item 8 › Other Derivatives | ✓ | #1 | We enter into foreign currency forward and option contracts that are not designated as hedging instruments to hedge intercompany transactions and other monetary assets or liabilities denominated in currencies other than … |
| 4 | `GOOGL_FY2023_2023-12-31:256` | Item 7A › Foreign Currency Exchange Risk |  |  | If an adverse 10% foreign currency exchange rate change was applied to total monetary assets, liabilities, and commitments denominated in currencies other than the functional currencies at the balance sheet date, it woul… |
| 5 | `GOOGL_FY2023_2023-12-31:258` | Item 7A › Foreign Currency Exchange Risk | ✓ |  | If the U.S. dollar weakened by 10% as of December 31, 2022 and 2023, the amount recorded in AOCI related to our cash flow hedges before tax effect would have been approximately $1.3 billion and $1.5 billion lower as of D… |
| 6 | `GOOGL_FY2023_2023-12-31:257` | Item 7A › Foreign Currency Exchange Risk | ✓ |  | We use foreign currency forward and option contracts, including collars (an option strategy comprised of a combination of purchased and written options) to protect forecasted U.S. dollar-equivalent earnings from changes … |
| 7 | `META_FY2023_2023-12-31:13` | TABLE OF CONTENTS |  |  | \| \| \| Page \| \|---\|---\|---\| \| Note About Forward-Looking Statements \| \| 3 \| \| Limitations of Key Metrics and Other Data \| \| 4 \| \| PART I \| \| \| \| Item 1. \| Business \| 7 \| \| Item 1A. \| Risk Factors \| 15 \| \| Item 1B. \| Unres… |
| 8 | `META_FY2023_2023-12-31:402` | Item 7A › Foreign Currency Exchange Risk | ✓ | #1, #2 | We have experienced and will continue to experience fluctuations in our net income as a result of transaction gains or losses related to remeasuring monetary asset and liability balances that are denominated in currencie… |
| 9 | `META_FY2023_2023-12-31:377` | Item 7 › Interest and other income (expense), net |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| 2023 vs 2022 % change \| 2022 vs 2021 % change \| \| \| (in millions, except percentages) \| \| \| \| \| \| Interest income \| $1,639 \| $461 \|… |
| 10 | `META_FY2023_2023-12-31:407` | Item 7A › Equity Price Risk |  |  | For additional information, see Note 1 — Summary of Significant Accounting Policies, Note 5 — Financial Instruments, Note 6 — Non-marketable Equity Securities, and Note 10 — Long-term Debt in the notes to the consolidate… |
| 11 | `META_FY2023_2023-12-31:400` | Item 7A |  |  | We are exposed to market risks, including changes to foreign currency exchange rates, interest rates, and equity price risk. |
| 12 | `META_FY2023_2023-12-31:587` | Item 8 › Note 14. Interest and Other Income (Expense), Net |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| \| Interest income \| $1,639 \| $461 \| $484 \| \| Interest expense \| (446) \| (185) \| (23) \| \| Foreign currency exchange losses, net \| (366) \| (81) \|… |
| 13 | `META_FY2023_2023-12-31:401` | Item 7A › Foreign Currency Exchange Risk | ✓ |  | We have foreign currency risks related to our revenue and operating expenses denominated in currencies other than the U.S. dollar, primarily the Euro. Accordingly, changes in exchange rates, and in particular a strengthe… |
| 14 | `META_FY2023_2023-12-31:510` | Item 8 › Instruments Measured at Fair Value |  |  | \| \| \| Fair Value Measurement at Reporting Date Using \| \| \| \|---\|---\|---\|---\|---\| \| Description \| December 31, 2023 \| Quoted Prices in Active Markets for Identical Assets (Level 1) \| Significant Other Observable Inputs (L… |
| 15 | `META_FY2023_2023-12-31:512` | Item 8 › Instruments Measured at Fair Value |  |  | \| \| \| Fair Value Measurement at Reporting Date Using \| \| \| \|---\|---\|---\|---\|---\| \| Description \| December 31, 2022 \| Quoted Prices in Active Markets for Identical Assets (Level 1) \| Significant Other Observable Inputs (L… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2023_2023-12-31:373`** (cited, gold #1)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Derivative Financial Instruments
We use derivative instruments to manage risks relating to our ongoing business operations. The primary risk managed is foreign exchange risk. We use foreign currency contracts to reduce the risk that our cash flows, earnings, and investment in foreign subsidiaries will be adversely affected by foreign currency exchange rate fluctuations. We also enter into derivative instruments to partially offset our exposure to other risks and enhance investment returns. We recognize derivative instruments in the Consolidated Balance Sheets at fair value and classify the derivatives primarily within Level 2 in the fair value hierarchy. We present our collar contracts (an option strategy comprised of a combination of purchased and written options) at net fair values and present all other derivatives at gross fair values. The accounting treatment for derivatives is based on the intended use and hedge designation.
````

**#2 `GOOGL_FY2023_2023-12-31:255`** (cited, gold #1)

````text
ITEM 7A.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK > Foreign Currency Exchange Risk
We transact business globally in multiple currencies. International revenues, as well as costs and expenses denominated in foreign currencies, expose us to the risk of fluctuations in foreign currency exchange rates against the U.S. dollar. As discussed below, we enter into derivative instruments to hedge foreign currency risk. Principal currencies hedged included the Australian dollar, British pound, Canadian dollar, Euro, and Japanese yen. For the purpose of analyzing foreign currency exchange risk, we considered the historical trends in foreign currency exchange rates and determined that it was reasonably possible that adverse changes in exchange rates of 10% could be experienced. We use foreign currency forward and option contracts to offset the foreign exchange risk on assets and liabilities denominated in currencies other than the functional currency of the subsidiary. These forward and option contracts reduce, but do not entirely eliminate, the effect of foreign currency exchange rate movements on our assets and liabilities. The foreign currency gains and losses on these assets and liabilities are recorded in OI&E, which are offset by the gains and losses on the forward and option contracts.
````

**#3 `GOOGL_FY2023_2023-12-31:377`** (cited, gold #1)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Derivatives
We enter into foreign currency forward and option contracts that are not designated as hedging instruments to hedge intercompany transactions and other monetary assets or liabilities denominated in currencies other than the functional currency of a subsidiary. Gains and losses on these derivatives that are not designated as accounting hedges are primarily recorded in OI&E along with the foreign currency gains and losses on monetary assets and liabilities. We also use derivatives not designated as hedging instruments to manage risks relating to interest rates, commodity prices, credit exposures, and to enhance investment returns. From time to time, we enter into derivatives to hedge the market price risk on certain of our marketable equity securities. Gains and losses arising from other derivatives are primarily reflected within the “other” component of OI&E. See Note 7 for further details. 68. Table of Contents Alphabet Inc. The gross notional amounts of outstanding derivative instruments were as follows (in millions):
````

**#5 `GOOGL_FY2023_2023-12-31:258`** (cited)

````text
ITEM 7A.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK > Foreign Currency Exchange Risk
If the U.S. dollar weakened by 10% as of December 31, 2022 and 2023, the amount recorded in AOCI related to our cash flow hedges before tax effect would have been approximately $1.3 billion and $1.5 billion lower as of December 31, 2022 and 2023, respectively. The change in the value recorded in AOCI would be expected to offset a corresponding foreign currency change in forecasted hedged revenues when recognized. We use foreign exchange forward contracts designated as net investment hedges to hedge the foreign currency risks related to investment in foreign subsidiaries. These forward contracts serve to offset the foreign currency translation risk from our foreign operations. If the U.S. dollar weakened by 10%, the amount recorded in cumulative translation adjustment (CTA) within AOCI related to our net investment hedges before tax effect would have been approximately $903 million and $946 million lower as of December 31, 2022 and 2023, respectively. The change in value recorded in CTA would be expected to offset a corresponding foreign currency translation gain or loss from our investment in foreign subsidiaries.
````

**#6 `GOOGL_FY2023_2023-12-31:257`** (cited)

````text
ITEM 7A.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK > Foreign Currency Exchange Risk
We use foreign currency forward and option contracts, including collars (an option strategy comprised of a combination of purchased and written options) to protect forecasted U.S. dollar-equivalent earnings from changes in foreign currency exchange rates. When the U.S. dollar strengthens, gains from foreign currency forward and option contacts reduce the foreign currency losses related to our earnings. When the U.S. dollar weakens, losses from foreign currency forward and option contracts offset the foreign currency gains related to our earnings. These hedging contracts reduce, but do not entirely eliminate, the effect of foreign currency exchange rate movements. We designate these contracts as cash flow hedges for accounting purposes. We reflect the gains or losses of foreign currency spot rate changes as a component of accumulated other comprehensive income (AOCI) and subsequently reclassify them into revenues to offset the hedged exposures as they occur.
````

**#8 `META_FY2023_2023-12-31:402`** (cited, gold #1, gold #2)

````text
Item 7A.Quantitative and Qualitative Disclosures About Market Risk > Foreign Currency Exchange Risk
We have experienced and will continue to experience fluctuations in our net income as a result of transaction gains or losses related to remeasuring monetary asset and liability balances that are denominated in currencies other than the functional currency of the entities in which they are recorded. At this time, we have not entered into, but in the future we may enter into, derivatives or other financial instruments in an attempt to hedge our foreign currency exchange risk. It is difficult to predict the effect hedging activities would have on our results of operations. Foreign currency exchange net losses of $366 million, $81 million, and $140 million were recognized in 2023, 2022, and 2021, respectively.
````

**#13 `META_FY2023_2023-12-31:401`** (cited)

````text
Item 7A.Quantitative and Qualitative Disclosures About Market Risk > Foreign Currency Exchange Risk
We have foreign currency risks related to our revenue and operating expenses denominated in currencies other than the U.S. dollar, primarily the Euro. Accordingly, changes in exchange rates, and in particular a strengthening of the U.S. dollar, have in the past, and may in the future, negatively affect our revenue and other operating results as expressed in U.S. dollars. See Management's Discussion and Analysis of Financial Condition and Results of Operations — Foreign Exchange Impact on Revenue section included in Part II, Item 7 of this Annual Report on Form 10-K for additional information.
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8'), ('GOOGL', 'Item 7A'), ('META', 'Item 7A')] gold=[(None, 'Item 7A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 9, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Alphabet states that it uses derivative instruments to manage risks relating to its ongoing business operations, with foreign exchange risk identified as the primary risk managed. [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:373] | supported | The evidence states Alphabet uses derivatives for ongoing business risks and that foreign exchange risk is the primary risk managed. |
| Alphabet says it uses foreign currency contracts to reduce the risk that its cash flows, earnings, and investment in foreign subsidiaries will be adversely affected by foreign currency exchange rate fluctuations. [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:373] | supported | The sentence matches the quoted evidence verbatim. |
| Alphabet also states that it enters into foreign currency forward and option contracts to hedge foreign currency risk, and that principal currencies hedged included the Australian dollar, British pound, Canadian dollar, Euro, and Japanese yen. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:255] | supported | The evidence says Alphabet uses foreign currency forward and option contracts to hedge foreign currency risk and lists those principal currencies hedged. |
| Alphabet further says it uses foreign currency forward and option contracts, including collars, to protect forecasted U.S. dollar-equivalent earnings from changes in foreign currency exchange rates, designates these contracts as cash flow hedges for accounting purposes, and uses foreign exchange forward contracts designated as net investment hedges to hedge foreign currency risks related to investments in foreign subsidiaries. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:257] [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:258] | supported | The cited passages support use of forward/option contracts including collars as cash flow hedges and forward contracts as net investment hedges for foreign subsidiaries. |
| Alphabet also uses foreign currency forward and option contracts that are not designated as hedging instruments to hedge intercompany transactions and other monetary assets or liabilities denominated in currencies other than the functional currency of a subsidiary. [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:377] | supported | The evidence explicitly states this use of non-designated foreign currency forward and option contracts. |
| Meta states that it is exposed to foreign currency exchange risk related to revenue and operating expenses denominated in currencies other than the U.S. dollar, primarily the Euro. [META FY2023, Item 7A, META_FY2023_2023-12-31:401] | supported | The evidence states Meta has foreign currency risks related to revenue and operating expenses denominated in currencies other than the U.S. dollar, primarily the Euro. |
| However, Meta says that, at this time, it has not entered into derivatives or other financial instruments to hedge its foreign currency exchange risk, although it may do so in the future. [META FY2023, Item 7A, META_FY2023_2023-12-31:402] | supported | The evidence explicitly says Meta had not entered into derivatives or other financial instruments to hedge this risk, though it may in the future. |
| Meta therefore describes foreign currency transaction gains or losses from remeasuring monetary asset and liability balances, rather than an active derivative hedging program. [META FY2023, Item 7A, META_FY2023_2023-12-31:402] | supported | The evidence describes transaction gains or losses from remeasurement and says Meta had not entered into hedging derivatives. |
| In short, Alphabet describes an active and multi-faceted derivative hedging strategy for foreign currency risk, including cash flow hedges, net investment hedges, and non-designated derivatives, while Meta says it had not entered into derivatives or other financial instruments to hedge foreign currency exchange risk as of its 2023 filing. [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:257] [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:258] [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:377] [META FY2023, Item 7A, META_FY2023_2023-12-31:402] | supported | The cited evidence supports Alphabet's active use of cash flow, net investment, and non-designated derivatives, and Meta's statement that it had not entered into hedging derivatives. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 5.

**Generated answer**

> Alphabet states that it uses derivative instruments to manage foreign exchange risk, including foreign currency forward and option contracts to offset foreign exchange risk on assets and liabilities denominated in currencies other than a subsidiary’s functional currency, and it identifies principal currencies hedged as the Australian dollar, British pound, Canadian dollar, Euro, and Japanese yen [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:373] [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:255].  
>
> Alphabet also states that it uses foreign currency forward and option contracts, including collars, to protect forecasted U.S. dollar-equivalent earnings from changes in foreign currency exchange rates, designates these contracts as cash flow hedges for accounting purposes, and records spot-rate gains or losses in AOCI before reclassifying them into revenues as the hedged exposures occur [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:257].  
>
> In addition, Alphabet says it enters into foreign currency forward and option contracts that are not designated as hedging instruments to hedge intercompany transactions and other monetary assets or liabilities denominated in currencies other than the functional currency of a subsidiary, with gains and losses primarily recorded in OI&E [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:377].  
>
> By contrast, Meta states that it has not entered into derivatives or other financial instruments to hedge its foreign currency exchange risk, although it may do so in the future [META FY2023, Item 7A, META_FY2023_2023-12-31:402].  
>
> So, Alphabet’s 2023 filing describes an active derivative-based foreign currency risk management program using forwards, options, and collars, including both designated cash flow hedges and non-designated hedges, while Meta’s 2023 filing says it was not using derivatives for foreign currency hedging at that time [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:373] [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:377] [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:257] [META FY2023, Item 7A, META_FY2023_2023-12-31:402].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2023_2023-12-31:373` | Item 8 › Derivative Financial Instruments | ✓ | #1 | We use derivative instruments to manage risks relating to our ongoing business operations. The primary risk managed is foreign exchange risk. We use foreign currency contracts to reduce the risk that our cash flows, earn… |
| 2 | `GOOGL_FY2023_2023-12-31:255` | Item 7A › Foreign Currency Exchange Risk | ✓ | #1 | We transact business globally in multiple currencies. International revenues, as well as costs and expenses denominated in foreign currencies, expose us to the risk of fluctuations in foreign currency exchange rates agai… |
| 3 | `GOOGL_FY2023_2023-12-31:377` | Item 8 › Other Derivatives | ✓ | #1 | We enter into foreign currency forward and option contracts that are not designated as hedging instruments to hedge intercompany transactions and other monetary assets or liabilities denominated in currencies other than … |
| 4 | `GOOGL_FY2023_2023-12-31:257` | Item 7A › Foreign Currency Exchange Risk | ✓ |  | We use foreign currency forward and option contracts, including collars (an option strategy comprised of a combination of purchased and written options) to protect forecasted U.S. dollar-equivalent earnings from changes … |
| 5 | `GOOGL_FY2023_2023-12-31:256` | Item 7A › Foreign Currency Exchange Risk |  |  | If an adverse 10% foreign currency exchange rate change was applied to total monetary assets, liabilities, and commitments denominated in currencies other than the functional currencies at the balance sheet date, it woul… |
| 6 | `META_FY2023_2023-12-31:402` | Item 7A › Foreign Currency Exchange Risk | ✓ | #1, #2 | We have experienced and will continue to experience fluctuations in our net income as a result of transaction gains or losses related to remeasuring monetary asset and liability balances that are denominated in currencie… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2023_2023-12-31:373`** (cited, gold #1)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Derivative Financial Instruments
We use derivative instruments to manage risks relating to our ongoing business operations. The primary risk managed is foreign exchange risk. We use foreign currency contracts to reduce the risk that our cash flows, earnings, and investment in foreign subsidiaries will be adversely affected by foreign currency exchange rate fluctuations. We also enter into derivative instruments to partially offset our exposure to other risks and enhance investment returns. We recognize derivative instruments in the Consolidated Balance Sheets at fair value and classify the derivatives primarily within Level 2 in the fair value hierarchy. We present our collar contracts (an option strategy comprised of a combination of purchased and written options) at net fair values and present all other derivatives at gross fair values. The accounting treatment for derivatives is based on the intended use and hedge designation.
````

**#2 `GOOGL_FY2023_2023-12-31:255`** (cited, gold #1)

````text
ITEM 7A.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK > Foreign Currency Exchange Risk
We transact business globally in multiple currencies. International revenues, as well as costs and expenses denominated in foreign currencies, expose us to the risk of fluctuations in foreign currency exchange rates against the U.S. dollar. As discussed below, we enter into derivative instruments to hedge foreign currency risk. Principal currencies hedged included the Australian dollar, British pound, Canadian dollar, Euro, and Japanese yen. For the purpose of analyzing foreign currency exchange risk, we considered the historical trends in foreign currency exchange rates and determined that it was reasonably possible that adverse changes in exchange rates of 10% could be experienced. We use foreign currency forward and option contracts to offset the foreign exchange risk on assets and liabilities denominated in currencies other than the functional currency of the subsidiary. These forward and option contracts reduce, but do not entirely eliminate, the effect of foreign currency exchange rate movements on our assets and liabilities. The foreign currency gains and losses on these assets and liabilities are recorded in OI&E, which are offset by the gains and losses on the forward and option contracts.
````

**#3 `GOOGL_FY2023_2023-12-31:377`** (cited, gold #1)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Derivatives
We enter into foreign currency forward and option contracts that are not designated as hedging instruments to hedge intercompany transactions and other monetary assets or liabilities denominated in currencies other than the functional currency of a subsidiary. Gains and losses on these derivatives that are not designated as accounting hedges are primarily recorded in OI&E along with the foreign currency gains and losses on monetary assets and liabilities. We also use derivatives not designated as hedging instruments to manage risks relating to interest rates, commodity prices, credit exposures, and to enhance investment returns. From time to time, we enter into derivatives to hedge the market price risk on certain of our marketable equity securities. Gains and losses arising from other derivatives are primarily reflected within the “other” component of OI&E. See Note 7 for further details. 68. Table of Contents Alphabet Inc. The gross notional amounts of outstanding derivative instruments were as follows (in millions):
````

**#4 `GOOGL_FY2023_2023-12-31:257`** (cited)

````text
ITEM 7A.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK > Foreign Currency Exchange Risk
We use foreign currency forward and option contracts, including collars (an option strategy comprised of a combination of purchased and written options) to protect forecasted U.S. dollar-equivalent earnings from changes in foreign currency exchange rates. When the U.S. dollar strengthens, gains from foreign currency forward and option contacts reduce the foreign currency losses related to our earnings. When the U.S. dollar weakens, losses from foreign currency forward and option contracts offset the foreign currency gains related to our earnings. These hedging contracts reduce, but do not entirely eliminate, the effect of foreign currency exchange rate movements. We designate these contracts as cash flow hedges for accounting purposes. We reflect the gains or losses of foreign currency spot rate changes as a component of accumulated other comprehensive income (AOCI) and subsequently reclassify them into revenues to offset the hedged exposures as they occur.
````

**#6 `META_FY2023_2023-12-31:402`** (cited, gold #1, gold #2)

````text
Item 7A.Quantitative and Qualitative Disclosures About Market Risk > Foreign Currency Exchange Risk
We have experienced and will continue to experience fluctuations in our net income as a result of transaction gains or losses related to remeasuring monetary asset and liability balances that are denominated in currencies other than the functional currency of the entities in which they are recorded. At this time, we have not entered into, but in the future we may enter into, derivatives or other financial instruments in an attempt to hedge our foreign currency exchange risk. It is difficult to predict the effect hedging activities would have on our results of operations. Foreign currency exchange net losses of $366 million, $81 million, and $140 million were recognized in 2023, 2022, and 2021, respectively.
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8'), ('GOOGL', 'Item 7A'), ('META', 'Item 7A')] gold=[(None, 'Item 7A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 5, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Alphabet states that it uses derivative instruments to manage foreign exchange risk, including foreign currency forward and option contracts to offset foreign exchange risk on assets and liabilities denominated in currencies other than a subsidiary’s functional currency, and it identifies principal currencies hedged as the Australian dollar, British pound, Canadian dollar, Euro, and Japanese yen [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:373] [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:255]. | supported | The cited passages state Alphabet uses derivative instruments, specifically foreign currency forwards and options, to offset FX risk on non-functional-currency assets and liabilities and list the principal currencies hedged. |
| Alphabet also states that it uses foreign currency forward and option contracts, including collars, to protect forecasted U.S. dollar-equivalent earnings from changes in foreign currency exchange rates, designates these contracts as cash flow hedges for accounting purposes, and records spot-rate gains or losses in AOCI before reclassifying them into revenues as the hedged exposures occur [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:257]. | supported | The evidence directly states Alphabet uses forwards, options, and collars for forecasted earnings, designates them as cash flow hedges, and records spot-rate gains/losses in AOCI before reclassifying to revenues. |
| In addition, Alphabet says it enters into foreign currency forward and option contracts that are not designated as hedging instruments to hedge intercompany transactions and other monetary assets or liabilities denominated in currencies other than the functional currency of a subsidiary, with gains and losses primarily recorded in OI&E [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:377]. | supported | The cited note explicitly says Alphabet uses non-designated foreign currency forwards and options to hedge intercompany transactions and other monetary assets or liabilities, with gains and losses primarily in OI&E. |
| By contrast, Meta states that it has not entered into derivatives or other financial instruments to hedge its foreign currency exchange risk, although it may do so in the future [META FY2023, Item 7A, META_FY2023_2023-12-31:402]. | supported | The Meta evidence states it had not entered into derivatives or other financial instruments to hedge foreign currency exchange risk, though it may do so in the future. |
| So, Alphabet’s 2023 filing describes an active derivative-based foreign currency risk management program using forwards, options, and collars, including both designated cash flow hedges and non-designated hedges, while Meta’s 2023 filing says it was not using derivatives for foreign currency hedging at that time [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:373] [GOOGL FY2023, Item 8, GOOGL_FY2023_2023-12-31:377] [GOOGL FY2023, Item 7A, GOOGL_FY2023_2023-12-31:257] [META FY2023, Item 7A, META_FY2023_2023-12-31:402]. | supported | The combined evidence supports that Alphabet actively used derivative-based FX hedging with forwards, options, collars, and both designated and non-designated hedges, while Meta was not using derivatives for FX hedging at that time. |

</details>
