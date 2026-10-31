# gold-094: Cross-company text

[← all cases](../README.md) · company: MICROSOFT CORP; Alphabet Inc. (MSFT, GOOGL) · fiscal year: 2019 · recipe `cross_company_text` · hop `multi` · answer type `qualitative` · scope `cross_company` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> How do the income tax discussions in Microsoft's and Alphabet's fiscal year 2019 MD&A differ in the U.S. tax law change or tax authority they highlight?

**Gold answer**

> Microsoft's 2019 10-K explicitly identifies the Tax Cuts and Jobs Act (TCJA) as a significant change to U.S. tax law that affects its business, while Alphabet's 2019 10-K focuses on the continuous examination of its returns by the Internal Revenue Service (IRS) and other tax authorities as the primary regulatory risk factor, without citing the TCJA.

**Key points** (RQ3 keypoint_recall targets)

1. Microsoft cites the TCJA as a significant change to U.S. tax law.
2. Alphabet cites continuous examination by the IRS and other tax authorities.
3. The comparison highlights different specific regulatory risks mentioned in their respective 2019 filings.

**Gold evidence**

1. `MSFT_FY2019_2019-06-30` · Item 7 › Income Taxes · text

   > The TCJA significantly changes existing U.S. tax law and includes numerous provisions that affect our business.

2. `GOOGL_FY2019_2019-12-31` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Income Taxes · text

   > In addition, we are subject to the continuous examination of our income tax returns by the Internal Revenue Services (IRS) and other tax authorities which may assert assessments against us.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 7 | 5 | 13 | 8 |
| recall@5 | 0.50 | 0.50 | 0.00 | 0.00 |
| recall@all | 0.50 | 0.50 | 0.50 | 0.50 |
| complete@all | 0 | 0 | 0 | 0 |
| average precision (lexical) | 0.33 | 0.42 | 0.17 | 0.12 |
| gold evidence first rank | #1: 3, #2: – | #1: 3, #2: – | #1: 6, #2: – | #1: 8, #2: – |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | 0.33 | 0.33 | 0.33 | 0.33 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 1.00 | 0.50 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 0.67 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 1 |
| tokens | 877 | 1243 | 13619 | 6152 |
| cost (USD) | 0.0002 | 0.0002 | 0.0547 | 0.0237 |
| latency (s) | 2.4 | 8.5 | 30.6 | 10.7 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 7, cited: 1.

**Generated answer**

> Microsoft’s FY2019 MD&A highlights the **TCJA (Tax Cuts and Jobs Act)** as the U.S. tax law change affecting its business [3].
>
> The part about **Alphabet’s FY2019 MD&A** and which U.S. tax law change or tax authority it highlights is **not in the provided context**.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2019_2019-06-30:401` | Item 8 › PART II |  |  | NOTE 12 — INCOME TAXES |
| 2 | `MSFT_FY2019_2019-06-30:210` | Item 7 › Fiscal Year 2019 Compared with Fiscal Year 2018 |  |  | The mix of income before income taxes between the U.S. and foreign countries impacted our effective tax rate as a result of the geographic distribution of, and customer demand for, our products and services. In fiscal ye… |
| 3 | `MSFT_FY2019_2019-06-30:249` | Item 7 › Income Taxes | ✓ | #1 | The TCJA significantly changes existing U.S. tax law and includes numerous provisions that affect our business. Refer to Note 12 – Income Taxes of the Notes to Financial Statements (Part II, Item 8 of this Form 10-K) for… |
| 4 | `MSFT_FY2019_2019-06-30:407` | Item 8 › Provision for Income Taxes |  |  | \| (In millions) \| \| \| \| \|---\|---\|---\|---\| \| Year Ended June 30, \| 2019 \| 2018 \| 2017 \| \| U.S. \| $15,799 \| $11,527 \| $6,843 \| \| Foreign \| 27,889 \| 24,947 \| 23,058 \| \| Income before income taxes \| $43,688 \| $36,474 \| $29,9… |
| 5 | `MSFT_FY2019_2019-06-30:405` | Item 8 › Provision for Income Taxes |  |  | \| (In millions) \| \| \| \| \|---\|---\|---\|---\| \| Year Ended June 30, \| 2019 \| 2018 \| 2017 \| \| Current Taxes \| \| \| \| \| U.S. federal \| $4,718 \| $19,764 \| $2,739 \| \| U.S. state and local \| 662 \| 934 \| 30 \| \| Foreign \| 5,531 \| 4,… |
| 6 | `MSFT_FY2019_2019-06-30:406` | Item 8 › Provision for Income Taxes |  |  | U.S. and foreign components of income before income taxes were as follows: |
| 7 | `MSFT_FY2019_2019-06-30:219` | Item 7 › Uncertain Tax Positions |  |  | Not meaningful. |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `MSFT_FY2019_2019-06-30:249`** (cited, gold #1)

````text
Item 7 > Income Taxes
The TCJA significantly changes existing U.S. tax law and includes numerous provisions that affect our business. Refer to Note 12 – Income Taxes of the Notes to Financial Statements (Part II, Item 8 of this Form 10-K) for further discussion.
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 7')] gold=[(None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 4.

**Generated answer**

> Microsoft’s FY2019 MD&A highlights the **Tax Cuts and Jobs Act (TCJA)**, noting that it significantly changed U.S. tax law and affected Microsoft’s business, including provisional charges, an additional tax expense adjustment, and a later tax benefit tied to restructuring intangible property ownership [3][4].
>
> Alphabet’s FY2019 income tax discussion highlights the **Tax Act enacted on December 22, 2017**, emphasizing that it **reduced the U.S. statutory tax rate from 35% to 21%** and created **new taxes on certain foreign-sourced earnings and related-party payments**, along with transition tax and deferred tax effects [1][5].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2019_2019-12-31:451` | Item 8 › Note 14. Income Taxes | ✓ |  | The Tax Act required us to pay U.S. income taxes on accumulated foreign subsidiary earnings not previously subject to U.S. income tax at a rate of 15.5% to the extent of foreign cash and certain other net current assets … |
| 2 | `MSFT_FY2019_2019-06-30:158` | Item 7 |  |  | The following Management’s Discussion and Analysis of Financial Condition and Results of Operations (“MD&A”) is intended to help the reader understand the results of operations and financial condition of Microsoft Corpor… |
| 3 | `MSFT_FY2019_2019-06-30:249` | Item 7 › Income Taxes | ✓ | #1 | The TCJA significantly changes existing U.S. tax law and includes numerous provisions that affect our business. Refer to Note 12 – Income Taxes of the Notes to Financial Statements (Part II, Item 8 of this Form 10-K) for… |
| 4 | `MSFT_FY2019_2019-06-30:161` | Item 7 › PART II | ✓ | #1 | On December 22, 2017, the Tax Cuts and Jobs Act (“TCJA”) was enacted into law, which significantly changed existing U.S. tax law and included numerous provisions that affect our business. We recorded a provisional net ch… |
| 5 | `GOOGL_FY2019_2019-12-31:450` | Item 8 › Note 14. Income Taxes | ✓ |  | The Tax Act enacted on December 22, 2017 introduced significant changes to U.S. income tax law. Effective 2018, the Tax Act reduced the U.S. statutory tax rate from 35% to 21% and created new taxes on certain foreign-sou… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2019_2019-12-31:451`** (cited)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 14. Income Taxes
The Tax Act required us to pay U.S. income taxes on accumulated foreign subsidiary earnings not previously subject to U.S. income tax at a rate of 15.5% to the extent of foreign cash and certain other net current assets and 8% on the remaining earnings. We recorded a provisional amount for our transitional tax liability and income tax expense of $10.2 billion as of December 31, 2017. Subsequent adjustments in 2018 and 2019 were not material. Deferred tax effects Due to the change in the statutory tax rate from the Tax Act, we remeasured our deferred taxes as of December 31, 2017 to reflect the reduced rate that will apply in future periods when these deferred taxes are settled or realized. We recognized a deferred tax benefit of $376 million to reflect the reduced U.S. tax rate and other effects of the Tax Act as of December 31, 2017. Table of Contents Alphabet Inc. The reconciliation of federal statutory income tax rate to our effective income tax rate is as follows:
````

**#3 `MSFT_FY2019_2019-06-30:249`** (cited, gold #1)

````text
Item 7 > Income Taxes
The TCJA significantly changes existing U.S. tax law and includes numerous provisions that affect our business. Refer to Note 12 – Income Taxes of the Notes to Financial Statements (Part II, Item 8 of this Form 10-K) for further discussion.
````

**#4 `MSFT_FY2019_2019-06-30:161`** (cited, gold #1)

````text
Item 7 > PART II
On December 22, 2017, the Tax Cuts and Jobs Act (“TCJA”) was enacted into law, which significantly changed existing U.S. tax law and included numerous provisions that affect our business. We recorded a provisional net charge related to the enactment of the TCJA of $13.7 billion in fiscal year 2018, and adjusted our provisional net charge by recording additional tax expense of $157 million in the second quarter of fiscal year 2019. In the fourth quarter of fiscal year 2019, in response to the TCJA and recently issued regulations, we transferred certain intangible properties held by our foreign subsidiaries to the U.S. and Ireland, which resulted in a $2.6 billion net income tax benefit. Refer to Note 12 – Income Taxes of the Notes to Financial Statements (Part II, Item 8 of this Form 10-K) for further discussion.
````

**#5 `GOOGL_FY2019_2019-12-31:450`** (cited)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 14. Income Taxes
The Tax Act enacted on December 22, 2017 introduced significant changes to U.S. income tax law. Effective 2018, the Tax Act reduced the U.S. statutory tax rate from 35% to 21% and created new taxes on certain foreign-sourced earnings and certain related-party payments. Due to the timing of the enactment and the complexity involved in applying the provisions of the Tax Act, we made reasonable estimates of the effects and recorded provisional amounts in our consolidated financial statements as of December 31, 2017. As we collected and prepared necessary data, and interpreted the additional guidance issued by the U.S. Treasury Department, the IRS, and other standard-setting bodies, we made adjustments, over the course of 2018, to the provisional amounts including refinements to deferred taxes. The accounting for the tax effects of the Tax Act was completed as of December 31, 2018. Transition tax
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8'), ('MSFT', 'Item 7')] gold=[(None, 'Item 7')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 13, cited: 2.

**Generated answer**

> Microsoft’s fiscal year 2019 MD&A highlights the U.S. Tax Cuts and Jobs Act, stating that the TCJA significantly changes existing U.S. tax law and includes numerous provisions that affect its business. [MSFT FY2019, Item 7, MSFT_FY2019_2019-06-30:249]
>
> Alphabet’s fiscal year 2019 MD&A highlights discrete tax items tied to the U.S. Tax Cuts and Jobs Act and a tax authority/court matter, stating that in 2018 it recognized benefits of the U.S. Tax Cuts and Jobs Act, and in 2019 it recognized increased discrete benefits from the resolution of multi-year audits, partially offset by the reversal of the Altera tax benefit as a result of the U.S. Court of Appeals decision. [GOOGL FY2019, Item 7, GOOGL_FY2019_2019-12-31:194]
>
> So, Microsoft’s discussion emphasizes the broad impact of a U.S. tax law change itself, while Alphabet’s discussion emphasizes specific discrete effects from the Tax Act and from tax audit resolutions and the Altera U.S. Court of Appeals decision. [MSFT FY2019, Item 7, MSFT_FY2019_2019-06-30:249] [GOOGL FY2019, Item 7, GOOGL_FY2019_2019-12-31:194]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2019_2019-06-30:210` | Item 7 › Fiscal Year 2019 Compared with Fiscal Year 2018 |  |  | The mix of income before income taxes between the U.S. and foreign countries impacted our effective tax rate as a result of the geographic distribution of, and customer demand for, our products and services. In fiscal ye… |
| 2 | `MSFT_FY2019_2019-06-30:406` | Item 8 › Provision for Income Taxes |  |  | U.S. and foreign components of income before income taxes were as follows: |
| 3 | `MSFT_FY2019_2019-06-30:407` | Item 8 › Provision for Income Taxes |  |  | \| (In millions) \| \| \| \| \|---\|---\|---\|---\| \| Year Ended June 30, \| 2019 \| 2018 \| 2017 \| \| U.S. \| $15,799 \| $11,527 \| $6,843 \| \| Foreign \| 27,889 \| 24,947 \| 23,058 \| \| Income before income taxes \| $43,688 \| $36,474 \| $29,9… |
| 4 | `MSFT_FY2019_2019-06-30:131` | Item 1A › PART I |  |  | We earn a significant amount of our operating income outside the U.S. A change in the mix of earnings and losses in countries with differing statutory tax rates, changes in our business or structure, or the expiration of… |
| 5 | `MSFT_FY2019_2019-06-30:405` | Item 8 › Provision for Income Taxes |  |  | \| (In millions) \| \| \| \| \|---\|---\|---\|---\| \| Year Ended June 30, \| 2019 \| 2018 \| 2017 \| \| Current Taxes \| \| \| \| \| U.S. federal \| $4,718 \| $19,764 \| $2,739 \| \| U.S. state and local \| 662 \| 934 \| 30 \| \| Foreign \| 5,531 \| 4,… |
| 6 | `MSFT_FY2019_2019-06-30:249` | Item 7 › Income Taxes | ✓ | #1 | The TCJA significantly changes existing U.S. tax law and includes numerous provisions that affect our business. Refer to Note 12 – Income Taxes of the Notes to Financial Statements (Part II, Item 8 of this Form 10-K) for… |
| 7 | `GOOGL_FY2019_2019-12-31:192` | Item 7 › Provision for Income Taxes |  |  | The following table presents our provision for income taxes (in millions) and effective tax rate: |
| 8 | `GOOGL_FY2019_2019-12-31:193` | Item 7 › Provision for Income Taxes |  |  | \| \| Year Ended December 31, \| \| \|---\|---\|---\| \| \| 2018 \| 2019 \| \| Provision for income taxes \| $4,177 \| $5,282 \| \| Effective tax rate \| 12.0% \| 13.3% \| |
| 9 | `GOOGL_FY2019_2019-12-31:195` | Item 7 › Provision for Income Taxes |  |  | We expect our future effective tax rate to be affected by the geographic mix of earnings in countries with different statutory rates. Additionally, our future effective tax rate may be affected by changes in the valuatio… |
| 10 | `GOOGL_FY2019_2019-12-31:194` | Item 7 › Provision for Income Taxes | ✓ |  | Our provision for income taxes and our effective tax rate increased from 2018 to 2019, due to discrete events in 2018 and 2019. In 2018, we released our deferred tax asset valuation allowance related to gains on equity s… |
| 11 | `GOOGL_FY2019_2019-12-31:452` | Item 8 › Note 14. Income Taxes |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2017 \| 2018 \| 2019 \| \| U.S. federal statutory tax rate \| 35.0% \| 21.0% \| 21.0% \| \| Foreign income taxed at different rates \| (14.2) \| (4.9) \| (5.6) \| \| Effect of th… |
| 12 | `GOOGL_FY2019_2019-12-31:451` | Item 8 › Note 14. Income Taxes |  |  | The Tax Act required us to pay U.S. income taxes on accumulated foreign subsidiary earnings not previously subject to U.S. income tax at a rate of 15.5% to the extent of foreign cash and certain other net current assets … |
| 13 | `GOOGL_FY2019_2019-12-31:446` | Item 8 › Note 14. Income Taxes |  |  | Income from continuing operations before income taxes consists of the following (in millions): |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#6 `MSFT_FY2019_2019-06-30:249`** (cited, gold #1)

````text
Item 7 > Income Taxes
The TCJA significantly changes existing U.S. tax law and includes numerous provisions that affect our business. Refer to Note 12 – Income Taxes of the Notes to Financial Statements (Part II, Item 8 of this Form 10-K) for further discussion.
````

**#10 `GOOGL_FY2019_2019-12-31:194`** (cited)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Provision for Income Taxes
Our provision for income taxes and our effective tax rate increased from 2018 to 2019, due to discrete events in 2018 and 2019. In 2018, we released our deferred tax asset valuation allowance related to gains on equity securities and recognized the benefits of the U.S. Tax Cuts and Jobs Act ("Tax Act"). In 2019, we recognized an increase in discrete benefits related to the resolution of multi-year audits, partially offset by the reversal of Altera tax benefit as a result of the U.S. Court of Appeals decision. See Note 14 of the Notes to Consolidated Financial Statements included in Part II, Item 8 of this Annual Report on Form 10-K for further information. As of December 31, 2019, we have simplified our corporate legal entity structure and now license intellectual property from the U.S. that was previously licensed from Bermuda. This will affect our geographic mix of earnings.
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 7'), ('GOOGL', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 3, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Microsoft’s fiscal year 2019 MD&A highlights the U.S. Tax Cuts and Jobs Act, stating that the TCJA significantly changes existing U.S. tax law and includes numerous provisions that affect its business. [MSFT FY2019, Item 7, MSFT_FY2019_2019-06-30:249] | supported | The cited Microsoft MD&A text states exactly that the TCJA significantly changes U.S. tax law and includes numerous provisions affecting its business. |
| Alphabet’s fiscal year 2019 MD&A highlights discrete tax items tied to the U.S. Tax Cuts and Jobs Act and a tax authority/court matter, stating that in 2018 it recognized benefits of the U.S. Tax Cuts and Jobs Act, and in 2019 it recognized increased discrete benefits from the resolution of multi-year audits, partially offset by the reversal of the Altera tax benefit as a result of the U.S. Court of Appeals decision. [GOOGL FY2019, Item 7, GOOGL_FY2019_2019-12-31:194] | supported | The cited Alphabet MD&A text expressly says it recognized Tax Act benefits in 2018 and increased discrete benefits from multi-year audit resolutions in 2019, partially offset by reversal of the Altera tax benefit due to the U.S. Court of Appeals decision. |
| So, Microsoft’s discussion emphasizes the broad impact of a U.S. tax law change itself, while Alphabet’s discussion emphasizes specific discrete effects from the Tax Act and from tax audit resolutions and the Altera U.S. Court of Appeals decision. [MSFT FY2019, Item 7, MSFT_FY2019_2019-06-30:249] [GOOGL FY2019, Item 7, GOOGL_FY2019_2019-12-31:194] | supported | The Microsoft evidence focuses on the broad business impact of the TCJA, while the Alphabet evidence focuses on discrete tax effects from the Tax Act, audit resolutions, and the Altera court decision. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 1.

**Generated answer**

> Microsoft’s fiscal year 2019 MD&A specifically highlights the TCJA, stating that the TCJA significantly changes existing U.S. tax law and includes numerous provisions that affect its business. [MSFT FY2019, Item 7, MSFT_FY2019_2019-06-30:249]
>
> The filing does not disclose Alphabet’s fiscal year 2019 MD&A income tax discussion in the provided evidence, so a comparison of the specific U.S. tax law change or tax authority Alphabet highlighted cannot be made from these materials.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-GOOGL-2019` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2019,2019-12-31,161857000000,34343000000,34231000000,275909000… |
| 2 | `F-MSFT-2019` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2019,2019-06-30,125843000000,39240000000,42959000000,286556000… |
| 3 | `MSFT_FY2019_2019-06-30:210` | Item 7 › Fiscal Year 2019 Compared with Fiscal Year 2018 |  |  | The mix of income before income taxes between the U.S. and foreign countries impacted our effective tax rate as a result of the geographic distribution of, and customer demand for, our products and services. In fiscal ye… |
| 4 | `MSFT_FY2019_2019-06-30:406` | Item 8 › Provision for Income Taxes |  |  | U.S. and foreign components of income before income taxes were as follows: |
| 5 | `MSFT_FY2019_2019-06-30:407` | Item 8 › Provision for Income Taxes |  |  | \| (In millions) \| \| \| \| \|---\|---\|---\|---\| \| Year Ended June 30, \| 2019 \| 2018 \| 2017 \| \| U.S. \| $15,799 \| $11,527 \| $6,843 \| \| Foreign \| 27,889 \| 24,947 \| 23,058 \| \| Income before income taxes \| $43,688 \| $36,474 \| $29,9… |
| 6 | `MSFT_FY2019_2019-06-30:131` | Item 1A › PART I |  |  | We earn a significant amount of our operating income outside the U.S. A change in the mix of earnings and losses in countries with differing statutory tax rates, changes in our business or structure, or the expiration of… |
| 7 | `MSFT_FY2019_2019-06-30:405` | Item 8 › Provision for Income Taxes |  |  | \| (In millions) \| \| \| \| \|---\|---\|---\|---\| \| Year Ended June 30, \| 2019 \| 2018 \| 2017 \| \| Current Taxes \| \| \| \| \| U.S. federal \| $4,718 \| $19,764 \| $2,739 \| \| U.S. state and local \| 662 \| 934 \| 30 \| \| Foreign \| 5,531 \| 4,… |
| 8 | `MSFT_FY2019_2019-06-30:249` | Item 7 › Income Taxes | ✓ | #1 | The TCJA significantly changes existing U.S. tax law and includes numerous provisions that affect our business. Refer to Note 12 – Income Taxes of the Notes to Financial Statements (Part II, Item 8 of this Form 10-K) for… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#8 `MSFT_FY2019_2019-06-30:249`** (cited, gold #1)

````text
Item 7 > Income Taxes
The TCJA significantly changes existing U.S. tax law and includes numerous provisions that affect our business. Refer to Note 12 – Income Taxes of the Notes to Financial Statements (Part II, Item 8 of this Form 10-K) for further discussion.
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 2, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Microsoft’s fiscal year 2019 MD&A specifically highlights the TCJA, stating that the TCJA significantly changes existing U.S. tax law and includes numerous provisions that affect its business. [MSFT FY2019, Item 7, MSFT_FY2019_2019-06-30:249] | supported | The cited MD&A text states exactly that the TCJA significantly changes existing U.S. tax law and includes numerous provisions affecting Microsoft's business. |
| The filing does not disclose Alphabet’s fiscal year 2019 MD&A income tax discussion in the provided evidence, so a comparison of the specific U.S. tax law change or tax authority Alphabet highlighted cannot be made from these materials. | supported | The provided evidence contains no Alphabet/GOOGL MD&A income tax discussion, only summary financial data, so such a comparison cannot be made from these materials. |

</details>
