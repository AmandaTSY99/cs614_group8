# gold-081: Cross-year text

[← all cases](../README.md) · company: Meta Platforms, Inc. (META) · fiscal year: 2018 · recipe `cross_year_text` · hop `multi` · answer type `qualitative` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> How did Meta Platforms, Inc.'s description of valuation techniques for financial instruments in its fiscal year 2018 10-K differ from its fiscal year 2015 10-K regarding the specific instruments mentioned?

**Gold answer**

> In fiscal year 2018, Meta described its valuation techniques for money market funds and marketable debt securities as being derived from quoted market prices or alternative pricing sources and models utilizing market observable inputs, but did not mention contingent consideration. In contrast, the fiscal year 2015 filing additionally described the valuation technique for contingent consideration liability as being based on the present value of probability-weighted future cash flows related to the contingent earn-out criteria and the fair value of common stock.

**Key points** (RQ3 keypoint_recall targets)

1. FY2018 filing mentions valuation techniques for money market funds and marketable debt securities.
2. FY2015 filing mentions valuation techniques for money market funds, marketable debt securities, and contingent consideration liability.
3. The FY2015 filing details a specific method for contingent consideration involving probability-weighted future cash flows.
4. The FY2018 filing omits the specific description for contingent consideration found in the FY2015 filing.

**Gold evidence**

1. `META_FY2018_2018-12-31` · Item 8. Financial Statements and Supplementary Data › Fair Value of Financial Instruments · text

   > Our valuation techniques used to measure the fair value of money market funds and marketable debt securities were derived from quoted market prices or alternative pricing sources and models utilizing market observable inputs.

2. `META_FY2015_2015-12-31` · Item 8. Financial Statements and Supplementary Data › Fair Value of Financial Instruments · text

   > Our valuation technique used to measure the fair value of our contingent consideration liability was based on the present value of probability-weighted future cash flows related to the contingent earn-out criteria and the fair value of our common stock on each reporting date.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 11 | 12 |
| recall@5 | 0.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 0.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 0 | 1 | 1 | 1 |
| average precision (lexical) | 0.00 | 0.42 | 0.59 | 0.75 |
| gold evidence first rank | #1: –, #2: – | #1: 3, #2: 4 | #1: 1, #2: 1 | #1: 1, #2: 1 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✓ | ✓ | ✓ |
| keypoint_recall | 0.00 | 0.75 | 1.00 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | – | 1.00 | 1.00 | 1.00 |
| citation recall | – | 1.00 | 1.00 | 1.00 |
| citation F1 | – | 1.00 | 1.00 | 1.00 |
| has a citation | 0 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 1628 | 770 | 13766 | 14674 |
| cost (USD) | 0.0002 | 0.0002 | 0.0538 | 0.0591 |
| latency (s) | 1.5 | 8.3 | 27.7 | 35.4 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2018_2018-12-31:170` | Item 6 |  |  | \| \| As of December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2018 \| 2017 \| 2016 \| 2015 \| 2014 \| \| \| (in millions) \| \| \| \| \| \| Consolidated Balance Sheets Data: \| \| \| \| \| \| \| Cash, cash equivalents, and marketable secur… |
| 2 | `META_FY2015_2015-12-31:0` |  |  |  | 10-K 1 fb-12312015x10k.htm 10-K |
| 3 | `META_FY2018_2018-12-31:0` |  |  |  | 10-K 1 fb-12312018x10k.htm 10-K |
| 4 | `META_FY2015_2015-12-31:160` | Item 6 |  |  | \| \| As of December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| 2012 \| 2011 \| \| \| (in millions) \| \| \| \| \| \| Consolidated Balance Sheets Data: \| \| \| \| \| \| \| Cash, cash equivalents, and marketable secur… |
| 5 | `META_FY2018_2018-12-31:2` | FORM 10-K |  |  | __________________________ (Mark One) x ANNUAL REPORT PURSUANT TO SECTION 13 OR 15(d) OF THE SECURITIES EXCHANGE ACT OF 1934 |
| 6 | `META_FY2018_2018-12-31:168` | Item 6 |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2018 \| 2017 \| 2016 \| 2015 \| 2014 \| \| \| (in millions, except per share data) \| \| \| \| \| \| Consolidated Statements of Income Data: \| \| \| \| \| \| \| Revenue \| … |
| 7 | `META_FY2015_2015-12-31:401` | Item 9 |  |  | None. |
| 8 | `META_FY2015_2015-12-31:406` | Item 9B |  |  | None. |
| 9 | `META_FY2018_2018-12-31:415` | Item 9 |  |  | None. |
| 10 | `META_FY2015_2015-12-31:216` | Item 7 › Research and development |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2015 \| 2014 \| 2013 \| 2015 vs 2014 % Change \| 2014 vs 2013 % Change \| \| \| (dollars in millions) \| \| \| \| \| \| Research and development \| $4,816 \| $2,666 \| … |

RQ2 citation match (section level): `no citations`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> In fiscal year 2018, Meta said its valuation techniques for fair value measurement applied to “money market funds and marketable debt securities” and were derived from quoted market prices or alternative pricing sources and models using observable market inputs [3].
>
> In fiscal year 2015, Meta included that same description for “money market funds and marketable debt securities,” but additionally described a separate valuation technique for its “contingent consideration liability,” based on the present value of probability-weighted future cash flows related to the contingent earn-out criteria and the fair value of its common stock on each reporting date [4].
>
> So, the 2018 10-K omitted the contingent consideration liability valuation technique that was specifically mentioned in the 2015 10-K [3][4].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2018_2018-12-31:0` |  |  |  | 10-K 1 fb-12312018x10k.htm 10-K |
| 2 | `META_FY2015_2015-12-31:0` |  |  |  | 10-K 1 fb-12312015x10k.htm 10-K |
| 3 | `META_FY2018_2018-12-31:330` | Item 8 › Fair Value of Financial Instruments | ✓ | #1 | Level 2-Observable inputs other than quoted prices in active markets for identical assets and liabilities, quoted prices for identical or similar assets or liabilities in inactive markets, or other inputs that are observ… |
| 4 | `META_FY2015_2015-12-31:313` | Item 8 › Fair Value of Financial Instruments | ✓ | #1, #2 | Level 2-Observable inputs other than quoted prices in active markets for identical assets and liabilities, quoted prices for identical or similar assets or liabilities in inactive markets, or other inputs that are observ… |
| 5 | `META_FY2015_2015-12-31:14` | DOCUMENTS INCORPORATED BY REFERENCE |  |  | Portions of the registrant's Proxy Statement for the 2016 Annual Meeting of Stockholders are incorporated herein by reference in Part III of this Annual Report on Form 10-K to the extent stated herein. Such proxy stateme… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `META_FY2018_2018-12-31:330`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Fair Value of Financial Instruments
Level 2-Observable inputs other than quoted prices in active markets for identical assets and liabilities, quoted prices for identical or similar assets or liabilities in inactive markets, or other inputs that are observable or can be corroborated by observable market data for substantially the full term of the assets or liabilities. Level 3-Inputs that are generally unobservable and typically reflect management's estimate of assumptions that market participants would use in pricing the asset or liability. Our valuation techniques used to measure the fair value of money market funds and marketable debt securities were derived from quoted market prices or alternative pricing sources and models utilizing market observable inputs.
````

**#4 `META_FY2015_2015-12-31:313`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Fair Value of Financial Instruments
Level 2-Observable inputs other than quoted prices in active markets for identical assets and liabilities, quoted prices for identical or similar assets or liabilities in inactive markets, or other inputs that are observable or can be corroborated by observable market data for substantially the full term of the assets or liabilities. Level 3-Inputs that are generally unobservable and typically reflect management's estimate of assumptions that market participants would use in pricing the asset or liability. Our valuation techniques used to measure the fair value of money market funds and marketable debt securities were derived from quoted market prices or alternative pricing sources and models utilizing market observable inputs. Our valuation technique used to measure the fair value of our contingent consideration liability was based on the present value of probability-weighted future cash flows related to the contingent earn-out criteria and the fair value of our common stock on each reporting date.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 11, cited: 2.

**Generated answer**

> In fiscal year 2018, Meta stated that its valuation techniques used to measure the fair value of money market funds and marketable debt securities were derived from quoted market prices or alternative pricing sources and models utilizing market observable inputs [META FY2018, Item 8, META_FY2018_2018-12-31:330].  
>
> In fiscal year 2015, Meta used that same description for money market funds and marketable debt securities, but it also separately disclosed that its valuation technique for its contingent consideration liability was based on the present value of probability-weighted future cash flows related to the contingent earn-out criteria and the fair value of its common stock on each reporting date [META FY2015, Item 8, META_FY2015_2015-12-31:313].  
>
> So, compared with 2015, the 2018 description omitted the contingent consideration liability valuation technique and mentioned only money market funds and marketable debt securities [META FY2015, Item 8, META_FY2015_2015-12-31:313] [META FY2018, Item 8, META_FY2018_2018-12-31:330].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2015_2015-12-31:313` | Item 8 › Fair Value of Financial Instruments | ✓ | #1, #2 | Level 2-Observable inputs other than quoted prices in active markets for identical assets and liabilities, quoted prices for identical or similar assets or liabilities in inactive markets, or other inputs that are observ… |
| 2 | `META_FY2018_2018-12-31:329` | Item 8 › Fair Value of Financial Instruments |  |  | We apply fair value accounting for all financial assets and liabilities and non-financial assets and liabilities that are recognized or disclosed at fair value in the financial statements on a recurring basis. We define … |
| 3 | `META_FY2015_2015-12-31:312` | Item 8 › Fair Value of Financial Instruments |  |  | We apply fair value accounting for all financial assets and liabilities and non-financial assets and liabilities that are recognized or disclosed at fair value in the financial statements on a recurring basis. We define … |
| 4 | `META_FY2018_2018-12-31:330` | Item 8 › Fair Value of Financial Instruments | ✓ | #1 | Level 2-Observable inputs other than quoted prices in active markets for identical assets and liabilities, quoted prices for identical or similar assets or liabilities in inactive markets, or other inputs that are observ… |
| 5 | `META_FY2018_2018-12-31:341` | Item 8 › Credit Risk and Concentration |  |  | Our financial instruments that are potentially subject to concentrations of credit risk consist primarily of cash, cash equivalents, restricted cash, marketable securities, and accounts receivable. The majority of cash e… |
| 6 | `META_FY2015_2015-12-31:327` | Item 8 › Credit Risk and Concentration |  |  | Our financial instruments that are potentially subject to concentrations of credit risk consist primarily of cash, cash equivalents, restricted cash, marketable securities, and accounts receivable. Cash equivalents consi… |
| 7 | `META_FY2018_2018-12-31:361` | Item 8 › Recent Accounting Pronouncements Not Yet Adopted |  |  | \| \| \| Fair Value Measurement at Reporting Date Using \| \| \| \|---\|---\|---\|---\|---\| \| Description \| December 31, 2017 \| Quoted Prices in Active Markets for Identical Assets (Level 1) \| Significant Other Observable Inputs (L… |
| 8 | `META_FY2018_2018-12-31:360` | Item 8 › Recent Accounting Pronouncements Not Yet Adopted |  |  | \| \| \| Fair Value Measurement at Reporting Date Using \| \| \| \|---\|---\|---\|---\|---\| \| Description \| December 31, 2018 \| Quoted Prices in Active Markets for Identical Assets (Level 1) \| Significant Other Observable Inputs (L… |
| 9 | `META_FY2015_2015-12-31:346` | Item 8 › Recently Issued and Adopted Accounting Pronouncement |  |  | \| \| \| Fair Value Measurement at Reporting Date Using \| \| \| \|---\|---\|---\|---\|---\| \| Description \| December 31, 2014 \| Quoted Prices in Active Markets for Identical Assets (Level 1) \| Significant Other Observable Inputs (L… |
| 10 | `META_FY2015_2015-12-31:345` | Item 8 › Recently Issued and Adopted Accounting Pronouncement |  |  | \| \| \| Fair Value Measurement at Reporting Date Using \| \| \| \|---\|---\|---\|---\|---\| \| Description \| December 31, 2015 \| Quoted Prices in Active Markets for Identical Assets (Level 1) \| Significant Other Observable Inputs (L… |
| 11 | `META_FY2018_2018-12-31:362` | Item 8 › Recent Accounting Pronouncements Not Yet Adopted |  | #1 | We classify our cash equivalents and marketable securities within Level 1 or Level 2 because we use quoted market prices or alternative pricing sources and models utilizing market observable inputs to determine their fai… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2015_2015-12-31:313`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Fair Value of Financial Instruments
Level 2-Observable inputs other than quoted prices in active markets for identical assets and liabilities, quoted prices for identical or similar assets or liabilities in inactive markets, or other inputs that are observable or can be corroborated by observable market data for substantially the full term of the assets or liabilities. Level 3-Inputs that are generally unobservable and typically reflect management's estimate of assumptions that market participants would use in pricing the asset or liability. Our valuation techniques used to measure the fair value of money market funds and marketable debt securities were derived from quoted market prices or alternative pricing sources and models utilizing market observable inputs. Our valuation technique used to measure the fair value of our contingent consideration liability was based on the present value of probability-weighted future cash flows related to the contingent earn-out criteria and the fair value of our common stock on each reporting date.
````

**#4 `META_FY2018_2018-12-31:330`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Fair Value of Financial Instruments
Level 2-Observable inputs other than quoted prices in active markets for identical assets and liabilities, quoted prices for identical or similar assets or liabilities in inactive markets, or other inputs that are observable or can be corroborated by observable market data for substantially the full term of the assets or liabilities. Level 3-Inputs that are generally unobservable and typically reflect management's estimate of assumptions that market participants would use in pricing the asset or liability. Our valuation techniques used to measure the fair value of money market funds and marketable debt securities were derived from quoted market prices or alternative pricing sources and models utilizing market observable inputs.
````

**#11 `META_FY2018_2018-12-31:362`** (gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Recent Accounting Pronouncements Not Yet Adopted
We classify our cash equivalents and marketable securities within Level 1 or Level 2 because we use quoted market prices or alternative pricing sources and models utilizing market observable inputs to determine their fair value. Note 5. Property and Equipment Property and equipment consists of the following (in millions):
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 3, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In fiscal year 2018, Meta stated that its valuation techniques used to measure the fair value of money market funds and marketable debt securities were derived from quoted market prices or alternative pricing sources and models utilizing market observable inputs [META FY2018, Item 8, META_FY2018_2018-12-31:330]. | supported | The cited 2018 evidence states exactly that the valuation techniques for money market funds and marketable debt securities were derived from quoted market prices or alternative pricing sources and models using observable inputs. |
| In fiscal year 2015, Meta used that same description for money market funds and marketable debt securities, but it also separately disclosed that its valuation technique for its contingent consideration liability was based on the present value of probability-weighted future cash flows related to the contingent earn-out criteria and the fair value of its common stock on each reporting date [META FY2015, Item 8, META_FY2015_2015-12-31:313]. | supported | The cited 2015 evidence includes both the same money market funds/debt securities description and the separate contingent consideration liability valuation technique described in the sentence. |
| So, compared with 2015, the 2018 description omitted the contingent consideration liability valuation technique and mentioned only money market funds and marketable debt securities [META FY2015, Item 8, META_FY2015_2015-12-31:313] [META FY2018, Item 8, META_FY2018_2018-12-31:330]. | supported | The 2015 evidence includes the contingent consideration liability technique, while the 2018 evidence mentions only money market funds and marketable debt securities. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 12, cited: 2.

**Generated answer**

> In fiscal year 2015, Meta stated that its valuation techniques used to measure the fair value of money market funds and marketable debt securities were derived from quoted market prices or alternative pricing sources and models utilizing market observable inputs, and it also stated that its valuation technique for the contingent consideration liability was based on the present value of probability-weighted future cash flows related to the contingent earn-out criteria and the fair value of its common stock on each reporting date [META FY2015, Item 8, META_FY2015_2015-12-31:313].  
>
> In fiscal year 2018, Meta stated that its valuation techniques used to measure the fair value of money market funds and marketable debt securities were derived from quoted market prices or alternative pricing sources and models utilizing market observable inputs [META FY2018, Item 8, META_FY2018_2018-12-31:330].  
>
> The difference is that the 2015 10-K specifically also described a valuation technique for the contingent consideration liability, while the 2018 10-K description mentioned only money market funds and marketable debt securities and did not include the contingent consideration liability [META FY2015, Item 8, META_FY2015_2015-12-31:313] [META FY2018, Item 8, META_FY2018_2018-12-31:330].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2015_2015-12-31:313` | Item 8 › Fair Value of Financial Instruments | ✓ | #1, #2 | Level 2-Observable inputs other than quoted prices in active markets for identical assets and liabilities, quoted prices for identical or similar assets or liabilities in inactive markets, or other inputs that are observ… |
| 2 | `META_FY2018_2018-12-31:329` | Item 8 › Fair Value of Financial Instruments |  |  | We apply fair value accounting for all financial assets and liabilities and non-financial assets and liabilities that are recognized or disclosed at fair value in the financial statements on a recurring basis. We define … |
| 3 | `META_FY2015_2015-12-31:312` | Item 8 › Fair Value of Financial Instruments |  |  | We apply fair value accounting for all financial assets and liabilities and non-financial assets and liabilities that are recognized or disclosed at fair value in the financial statements on a recurring basis. We define … |
| 4 | `META_FY2018_2018-12-31:330` | Item 8 › Fair Value of Financial Instruments | ✓ | #1 | Level 2-Observable inputs other than quoted prices in active markets for identical assets and liabilities, quoted prices for identical or similar assets or liabilities in inactive markets, or other inputs that are observ… |
| 5 | `META_FY2018_2018-12-31:341` | Item 8 › Credit Risk and Concentration |  |  | Our financial instruments that are potentially subject to concentrations of credit risk consist primarily of cash, cash equivalents, restricted cash, marketable securities, and accounts receivable. The majority of cash e… |
| 6 | `META_FY2015_2015-12-31:327` | Item 8 › Credit Risk and Concentration |  |  | Our financial instruments that are potentially subject to concentrations of credit risk consist primarily of cash, cash equivalents, restricted cash, marketable securities, and accounts receivable. Cash equivalents consi… |
| 7 | `META_FY2015_2015-12-31:344` | Item 8 › Recently Issued and Adopted Accounting Pronouncement |  |  | Note 5. Fair Value Measurement The following table summarizes, for assets or liabilities measured at fair value, the respective fair value and the classification by level of input within the fair value hierarchy (in mill… |
| 8 | `META_FY2018_2018-12-31:359` | Item 8 › Recent Accounting Pronouncements Not Yet Adopted |  |  | Note 4. Fair Value Measurement The following table summarizes, for assets or liabilities measured at fair value, the respective fair value and the classification by level of input within the fair value hierarchy (in mill… |
| 9 | `META_FY2015_2015-12-31:345` | Item 8 › Recently Issued and Adopted Accounting Pronouncement |  |  | \| \| \| Fair Value Measurement at Reporting Date Using \| \| \| \|---\|---\|---\|---\|---\| \| Description \| December 31, 2015 \| Quoted Prices in Active Markets for Identical Assets (Level 1) \| Significant Other Observable Inputs (L… |
| 10 | `META_FY2018_2018-12-31:360` | Item 8 › Recent Accounting Pronouncements Not Yet Adopted |  |  | \| \| \| Fair Value Measurement at Reporting Date Using \| \| \| \|---\|---\|---\|---\|---\| \| Description \| December 31, 2018 \| Quoted Prices in Active Markets for Identical Assets (Level 1) \| Significant Other Observable Inputs (L… |
| 11 | `META_FY2018_2018-12-31:361` | Item 8 › Recent Accounting Pronouncements Not Yet Adopted |  |  | \| \| \| Fair Value Measurement at Reporting Date Using \| \| \| \|---\|---\|---\|---\|---\| \| Description \| December 31, 2017 \| Quoted Prices in Active Markets for Identical Assets (Level 1) \| Significant Other Observable Inputs (L… |
| 12 | `META_FY2015_2015-12-31:346` | Item 8 › Recently Issued and Adopted Accounting Pronouncement |  |  | \| \| \| Fair Value Measurement at Reporting Date Using \| \| \| \|---\|---\|---\|---\|---\| \| Description \| December 31, 2014 \| Quoted Prices in Active Markets for Identical Assets (Level 1) \| Significant Other Observable Inputs (L… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2015_2015-12-31:313`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Fair Value of Financial Instruments
Level 2-Observable inputs other than quoted prices in active markets for identical assets and liabilities, quoted prices for identical or similar assets or liabilities in inactive markets, or other inputs that are observable or can be corroborated by observable market data for substantially the full term of the assets or liabilities. Level 3-Inputs that are generally unobservable and typically reflect management's estimate of assumptions that market participants would use in pricing the asset or liability. Our valuation techniques used to measure the fair value of money market funds and marketable debt securities were derived from quoted market prices or alternative pricing sources and models utilizing market observable inputs. Our valuation technique used to measure the fair value of our contingent consideration liability was based on the present value of probability-weighted future cash flows related to the contingent earn-out criteria and the fair value of our common stock on each reporting date.
````

**#4 `META_FY2018_2018-12-31:330`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Fair Value of Financial Instruments
Level 2-Observable inputs other than quoted prices in active markets for identical assets and liabilities, quoted prices for identical or similar assets or liabilities in inactive markets, or other inputs that are observable or can be corroborated by observable market data for substantially the full term of the assets or liabilities. Level 3-Inputs that are generally unobservable and typically reflect management's estimate of assumptions that market participants would use in pricing the asset or liability. Our valuation techniques used to measure the fair value of money market funds and marketable debt securities were derived from quoted market prices or alternative pricing sources and models utilizing market observable inputs.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 3, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In fiscal year 2015, Meta stated that its valuation techniques used to measure the fair value of money market funds and marketable debt securities were derived from quoted market prices or alternative pricing sources and models utilizing market observable inputs, and it also stated that its valuation technique for the contingent consideration liability was based on the present value of probability-weighted future cash flows related to the contingent earn-out criteria and the fair value of its common stock on each reporting date [META FY2015, Item 8, META_FY2015_2015-12-31:313]. | supported | The cited 2015 evidence states both the valuation approach for money market funds and marketable debt securities and the separate contingent consideration liability technique. |
| In fiscal year 2018, Meta stated that its valuation techniques used to measure the fair value of money market funds and marketable debt securities were derived from quoted market prices or alternative pricing sources and models utilizing market observable inputs [META FY2018, Item 8, META_FY2018_2018-12-31:330]. | supported | The cited 2018 evidence explicitly states that valuation techniques for money market funds and marketable debt securities were derived from quoted prices or alternative pricing sources and models using observable inputs. |
| The difference is that the 2015 10-K specifically also described a valuation technique for the contingent consideration liability, while the 2018 10-K description mentioned only money market funds and marketable debt securities and did not include the contingent consideration liability [META FY2015, Item 8, META_FY2015_2015-12-31:313] [META FY2018, Item 8, META_FY2018_2018-12-31:330]. | supported | The 2015 evidence includes contingent consideration liability language, while the 2018 evidence only mentions money market funds and marketable debt securities and does not include contingent consideration liability. |

</details>
