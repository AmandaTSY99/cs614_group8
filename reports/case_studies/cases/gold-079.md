# gold-079: Cross-year text

[← all cases](../README.md) · company: Alphabet Inc. (GOOGL) · fiscal year: 2022 · recipe `cross_year_text` · hop `multi` · answer type `qualitative` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> How did the description of the evaluation criteria for reporting units and the reassignment of goodwill change in Alphabet Inc.'s 10-K filings between fiscal year 2018 and fiscal year 2022?

**Gold answer**

> In the fiscal year 2018 filing, Alphabet stated that it evaluates reporting units when changes in operating structure occur and reassigns goodwill if necessary. In the fiscal year 2022 filing, the company updated this description to state that it evaluates reporting units periodically, as well as when changes in operating segments occur, and explicitly stated that for changes in reporting units, it reassigns goodwill using a relative fair value allocation approach.

**Key points** (RQ3 keypoint_recall targets)

1. The 2022 filing states reporting units are evaluated periodically and upon changes in operating segments.
2. The 2018 filing stated reporting units are evaluated when changes in operating structure occur.
3. Both filings indicate goodwill is reassigned using a relative fair value allocation approach, but the 2022 filing links this explicitly to changes in reporting units.

**Gold evidence**

1. `GOOGL_FY2022_2022-12-31` · ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Long-Lived Assets, Goodwill and Other Acquired Intangible Assets · text

   > We evaluate our reporting units periodically, as well as when changes in our operating segments occur. For changes in reporting units, we reassign goodwill using a relative fair value allocation approach.

2. `GOOGL_FY2018_2018-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Long-Lived Assets, Goodwill and Other Acquired Intangible Assets · text

   > We evaluate our reporting units when changes in our operating structure occur, and if necessary, reassign goodwill using a relative fair value allocation approach.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 15 | 13 |
| recall@5 | 0.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 0.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 0 | 1 | 1 | 1 |
| average precision (lexical) | 0.00 | 1.00 | 0.83 | 0.83 |
| gold evidence first rank | #1: –, #2: – | #1: 1, #2: 1 | #1: 1, #2: 1 | #1: 1, #2: 1 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | 0.00 | 1.00 | 1.00 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 1550 | 1062 | 17799 | 17094 |
| cost (USD) | 0.0003 | 0.0002 | 0.0693 | 0.0690 |
| latency (s) | 3.9 | 7.8 | 33.2 | 31.3 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 3.

**Generated answer**

> The provided context only includes the goodwill section headings for FY2018 and the FY2022 goodwill table, but it does not include any narrative describing the evaluation criteria for reporting units or any discussion of reassignment of goodwill in either year. [2][3][10]
>
> What is in the context:
> - FY2018 includes only the heading for the goodwill section. [3]
> - FY2022 includes the heading and a table showing goodwill balances by Google Services, Google Cloud, and Other Bets, including acquisitions and foreign currency translation adjustments. [2][10]
>
> What is not in the context:
> - The description of the evaluation criteria for reporting units in FY2018 or FY2022.
> - Any explanation of how goodwill was reassigned between reporting units.
> - Any comparison of changes in that description between the two filings.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2022_2022-12-31:1` | FORM 10-K |  |  | ___________________________________________ |
| 2 | `GOOGL_FY2022_2022-12-31:406` | Item 8 › Goodwill | ✓ |  | Changes in the carrying amount of goodwill for the years ended December 31, 2021 and 2022 were as follows (in millions): |
| 3 | `GOOGL_FY2018_2018-12-31:399` | Item 8 › Goodwill | ✓ |  | Changes in the carrying amount of goodwill for the years ended December 31, 2017 and 2018 were as follows (in millions): |
| 4 | `GOOGL_FY2022_2022-12-31:483` | Item 15 |  |  | We have filed the following documents as part of this Annual Report on Form 10-K: |
| 5 | `GOOGL_FY2022_2022-12-31:0` | Washington, D.C. 20549 |  |  | ___________________________________________ |
| 6 | `GOOGL_FY2018_2018-12-31:2` | FORM 10-K |  |  | ___________________________________________ |
| 7 | `GOOGL_FY2022_2022-12-31:2` | (Mark One) |  |  | ☒ ANNUAL REPORT PURSUANT TO SECTION 13 OR 15(d) OF THE SECURITIES EXCHANGE ACT OF 1934 For the fiscal year ended December 31, 2022 |
| 8 | `GOOGL_FY2022_2022-12-31:275` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2020 \| 2021 \| 2022 \| \| Proceeds from issuance of debt, net of costs \| 11,761 \| 20,199 \| 52,872 \| \| Repayments of debt \| (2,100) \| (21,435) \| (54,068) \| \| Proceeds f… |
| 9 | `GOOGL_FY2022_2022-12-31:273` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2020 \| 2021 \| 2022 \| \| Operating activities \| \| \| \| \| Net income \| $40,269 \| $76,033 \| $59,972 \| \| Adjustments: \| \| \| \| \| Depreciation and impairment of property an… |
| 10 | `GOOGL_FY2022_2022-12-31:407` | Item 8 › Goodwill | ✓ |  | \| \| Google Services \| Google Cloud \| Other Bets \| Total \| \|---\|---\|---\|---\|---\| \| Balance as of December 31, 2020 \| $18,517 \| $1,957 \| $701 \| $21,175 \| \| Acquisitions \| 1,325 \| 382 \| 103 \| 1,810 \| \| Foreign currency tran… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `GOOGL_FY2022_2022-12-31:406`** (cited)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Goodwill
Changes in the carrying amount of goodwill for the years ended December 31, 2021 and 2022 were as follows (in millions):
````

**#3 `GOOGL_FY2018_2018-12-31:399`** (cited)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Goodwill
Changes in the carrying amount of goodwill for the years ended December 31, 2017 and 2018 were as follows (in millions):
````

**#10 `GOOGL_FY2022_2022-12-31:407`** (cited)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Goodwill (table)
|  | Google Services | Google Cloud | Other Bets | Total |
|---|---|---|---|---|
| Balance as of December 31, 2020 | $18,517 | $1,957 | $701 | $21,175 |
| Acquisitions | 1,325 | 382 | 103 | 1,810 |
| Foreign currency translation and other adjustments | (16) | (2) | (11) | (29) |
| Balance as of December 31, 2021 | 19,826 | 2,337 | 793 | 22,956 |
| Acquisitions | 1,176 | 4,876 | 119 | 6,171 |
| Foreign currency translation and other adjustments | (155) | (8) | (4) | (167) |
| Balance as of December 31, 2022 | $20,847 | $7,205 | $908 | $28,960 |
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> In FY2018, Alphabet said it **evaluated reporting units when changes in its operating structure occurred**, and **if necessary, reassigned goodwill using a relative fair value allocation approach** [2].
>
> In FY2022, Alphabet said it **evaluated reporting units periodically, as well as when changes in its operating segments occurred**. It also stated that **for changes in reporting units, it reassigns goodwill using a relative fair value allocation approach** [1].
>
> So, the change was that the FY2022 language:
> - added **periodic evaluation** of reporting units,
> - changed the trigger from **changes in operating structure** to **changes in operating segments**, and
> - made the goodwill reassignment wording more direct: **for changes in reporting units, goodwill is reassigned** using the relative fair value allocation approach, rather than saying **if necessary** [1][2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2022_2022-12-31:313` | Item 8 › Long-Lived Assets, Goodwill and Other Acquired Intangible Assets | ✓ | #1, #2 | We review property and equipment and intangible assets, excluding goodwill, for impairment when events or changes in circumstances indicate the carrying amount may not be recoverable. The evaluation is performed at the l… |
| 2 | `GOOGL_FY2018_2018-12-31:300` | Item 8 › Long-Lived Assets, Goodwill and Other Acquired Intangible Assets | ✓ | #1, #2 | We review property and equipment, long-term prepayments and intangible assets, excluding goodwill, for impairment when events or changes in circumstances indicate the carrying amount may not be recoverable. We measure re… |
| 3 | `GOOGL_FY2018_2018-12-31:2` | FORM 10-K |  |  | ___________________________________________ |
| 4 | `GOOGL_FY2022_2022-12-31:1` | FORM 10-K |  |  | ___________________________________________ |
| 5 | `GOOGL_FY2022_2022-12-31:256` | Item 8 › Opinion on Internal Control Over Financial Reporting |  |  | We have audited Alphabet Inc.’s internal control over financial reporting as of December 31, 2022, based on criteria established in Internal Control—Integrated Framework issued by the Committee of Sponsoring Organization… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2022_2022-12-31:313`** (cited, gold #1, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Long-Lived Assets, Goodwill and Other Acquired Intangible Assets
We review property and equipment and intangible assets, excluding goodwill, for impairment when events or changes in circumstances indicate the carrying amount may not be recoverable. The evaluation is performed at the lowest level of identifiable cash flows independent of other assets. We measure recoverability of these assets by Table of Contents Alphabet Inc. comparing the carrying amounts to the future undiscounted cash flows that the assets or the asset group are expected to generate. If the carrying value of the assets or asset group is not recoverable, the impairment recognized is measured as the amount by which the carrying value exceeds its fair value. Impairments were not material for the periods presented. We allocate goodwill to reporting units based on the expected benefit from the business combination. We evaluate our reporting units periodically, as well as when changes in our operating segments occur. For changes in reporting units, we reassign goodwill using a relative fair value allocation approach. We test our goodwill for impairment at least annually, or more frequently if events or changes in circumstances indicate that the asset may be impaired. Goodwill impairments were not material for the periods presented.
````

**#2 `GOOGL_FY2018_2018-12-31:300`** (cited, gold #1, gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Long-Lived Assets, Goodwill and Other Acquired Intangible Assets
We review property and equipment, long-term prepayments and intangible assets, excluding goodwill, for impairment when events or changes in circumstances indicate the carrying amount may not be recoverable. We measure recoverability of these assets by comparing the carrying amounts to the future undiscounted cash flows that the assets or the asset group are expected to generate. If the carrying value of the assets are not recoverable, the impairment recognized is measured as the amount by which the carrying value of the asset exceeds its fair value. Impairments were not material for the periods presented. We allocate goodwill to reporting units based on the expected benefit from the business combination. We evaluate our reporting units when changes in our operating structure occur, and if necessary, reassign goodwill using a relative fair value allocation approach. We test our goodwill for impairment at least annually, or more frequently if events or changes in circumstances indicate that the asset may be impaired. Goodwill impairments were not material for the periods presented. Intangible assets with definite lives are amortized over their estimated useful lives. We amortize intangible assets on a straight-line basis with definite lives over periods ranging from one to twelve years.
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 15, cited: 2.

**Generated answer**

> In fiscal year 2018, Alphabet stated that it evaluates its reporting units “when changes in our operating structure occur,” and “if necessary, reassign[s] goodwill using a relative fair value allocation approach.” [GOOGL FY2018, Item 8, GOOGL_FY2018_2018-12-31:300]
>
> In fiscal year 2022, Alphabet stated that it evaluates its reporting units “periodically, as well as when changes in our operating segments occur,” and that for changes in reporting units, it “reassign[s] goodwill using a relative fair value allocation approach.” [GOOGL FY2022, Item 8, GOOGL_FY2022_2022-12-31:313]
>
> So, the description changed from evaluating reporting units only when changes in the company’s operating structure occur to evaluating them periodically and also when changes in operating segments occur, and the goodwill reassignment language changed from “if necessary” to specifically applying reassignment “for changes in reporting units,” while still using a relative fair value allocation approach. [GOOGL FY2018, Item 8, GOOGL_FY2018_2018-12-31:300] [GOOGL FY2022, Item 8, GOOGL_FY2022_2022-12-31:313]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2022_2022-12-31:313` | Item 8 › Long-Lived Assets, Goodwill and Other Acquired Intangible Assets | ✓ | #1, #2 | We review property and equipment and intangible assets, excluding goodwill, for impairment when events or changes in circumstances indicate the carrying amount may not be recoverable. The evaluation is performed at the l… |
| 2 | `GOOGL_FY2018_2018-12-31:227` | Item 7 › Critical Accounting Policies and Estimates |  |  | Please see Notes to Consolidated Financial Statements included in Part II, Item 8 of this Annual Report on Form 10-K for a summary of significant accounting policies and the effect on our financial statements. |
| 3 | `GOOGL_FY2018_2018-12-31:300` | Item 8 › Long-Lived Assets, Goodwill and Other Acquired Intangible Assets | ✓ | #1, #2 | We review property and equipment, long-term prepayments and intangible assets, excluding goodwill, for impairment when events or changes in circumstances indicate the carrying amount may not be recoverable. We measure re… |
| 4 | `GOOGL_FY2018_2018-12-31:256` | Item 8 › Opinion on Internal Control over Financial Reporting |  |  | We have audited Alphabet Inc.’s internal control over financial reporting as of December 31, 2018, based on criteria established in Internal Control-Integrated Framework issued by the Committee of Sponsoring Organization… |
| 5 | `GOOGL_FY2022_2022-12-31:256` | Item 8 › Opinion on Internal Control Over Financial Reporting |  |  | We have audited Alphabet Inc.’s internal control over financial reporting as of December 31, 2022, based on criteria established in Internal Control—Integrated Framework issued by the Committee of Sponsoring Organization… |
| 6 | `GOOGL_FY2022_2022-12-31:250` | Item 8 › Opinion on the Financial Statements |  |  | We have audited the accompanying consolidated balance sheets of Alphabet Inc. (the Company) as of December 31, 2021 and 2022, the related consolidated statements of income, comprehensive income, stockholders' equity and … |
| 7 | `GOOGL_FY2022_2022-12-31:492` | Item 15 › 3. Exhibits |  |  | \| Exhibit Number \| \| Description \| Incorporated by reference herein \| \| \|---\|---\|---\|---\|---\| \| \| Form \| Date \| \| \| \| 4.12 \| \| Form of the Registrant’s 3.375% Notes due 2024 (included in Exhibit 4.11) \| \| \| \| 4.13 \| \| Fo… |
| 8 | `GOOGL_FY2022_2022-12-31:496` | Item 15 › 3. Exhibits |  |  | \| Exhibit Number \| \| \| Description \| Incorporated by reference herein \| \| \|---\|---\|---\|---\|---\|---\| \| \| Form \| \| Date \| \| \| \| 10.08 \| u \| \| Alphabet Inc. Amended and Restated 2021 Stock Plan \| Current Report on Form 8-K … |
| 9 | `GOOGL_FY2022_2022-12-31:493` | Item 15 › 3. Exhibits |  |  | \| Exhibit Number \| \| Description \| Incorporated by reference herein \| \| \|---\|---\|---\|---\|---\| \| \| Form \| Date \| \| \| \| 4.18 \| \| Form of Global Note representing the Registrant’s 2.050% notes due 2050 \| Current Report on F… |
| 10 | `GOOGL_FY2022_2022-12-31:261` | Item 8 › (in millions, except par value per share amounts) |  |  | \| \| As of December 31, \| \| \|---\|---\|---\| \| \| 2021 \| 2022 \| \| Assets \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $20,945 \| $21,879 \| \| Marketable securities \| 118,704 \| 91,883 \| \| Total cash, cash equivale… |
| 11 | `GOOGL_FY2022_2022-12-31:471` | Item 9 |  |  | None. |
| 12 | `GOOGL_FY2022_2022-12-31:163` | Item 7 › Executive Overview |  |  | \| \| Year Ended December 31, \| \| \| \| \|---\|---\|---\|---\|---\| \| \| 2021 \| 2022 \| $ Change \| % Change \| \| Consolidated revenues \| $257,637 \| $282,836 \| $25,199 \| 10% \| \| Change in consolidated constant currency revenues(1) \| \|… |
| 13 | `GOOGL_FY2022_2022-12-31:306` | Item 8 › Impairment of Investments |  |  | For non-marketable equity securities, including equity method investments, we consider whether impairment indicators exist by evaluating the companies' financial and liquidity position and access to capital resources, am… |
| 14 | `GOOGL_FY2022_2022-12-31:409` | Item 8 › Other Intangible Assets |  |  | \| \| As of December 31, 2021 \| \| \| As of December 31, 2022 \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Gross Carrying Amount \| Accumulated Amortization \| Net Carrying Amount \| Gross Carrying Amount \| Accumulated Amortiz… |
| 15 | `GOOGL_FY2018_2018-12-31:261` | Item 8 › (In millions, except share amounts which are reflected in thousands, and par value per share amounts) |  |  | \| \| As of December 31, 2017 \| As of December 31, 2018 \| \|---\|---\|---\| \| Assets \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $10,715 \| $16,701 \| \| Marketable securities \| 91,156 \| 92,439 \| \| Total cash, cas… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2022_2022-12-31:313`** (cited, gold #1, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Long-Lived Assets, Goodwill and Other Acquired Intangible Assets
We review property and equipment and intangible assets, excluding goodwill, for impairment when events or changes in circumstances indicate the carrying amount may not be recoverable. The evaluation is performed at the lowest level of identifiable cash flows independent of other assets. We measure recoverability of these assets by Table of Contents Alphabet Inc. comparing the carrying amounts to the future undiscounted cash flows that the assets or the asset group are expected to generate. If the carrying value of the assets or asset group is not recoverable, the impairment recognized is measured as the amount by which the carrying value exceeds its fair value. Impairments were not material for the periods presented. We allocate goodwill to reporting units based on the expected benefit from the business combination. We evaluate our reporting units periodically, as well as when changes in our operating segments occur. For changes in reporting units, we reassign goodwill using a relative fair value allocation approach. We test our goodwill for impairment at least annually, or more frequently if events or changes in circumstances indicate that the asset may be impaired. Goodwill impairments were not material for the periods presented.
````

**#3 `GOOGL_FY2018_2018-12-31:300`** (cited, gold #1, gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Long-Lived Assets, Goodwill and Other Acquired Intangible Assets
We review property and equipment, long-term prepayments and intangible assets, excluding goodwill, for impairment when events or changes in circumstances indicate the carrying amount may not be recoverable. We measure recoverability of these assets by comparing the carrying amounts to the future undiscounted cash flows that the assets or the asset group are expected to generate. If the carrying value of the assets are not recoverable, the impairment recognized is measured as the amount by which the carrying value of the asset exceeds its fair value. Impairments were not material for the periods presented. We allocate goodwill to reporting units based on the expected benefit from the business combination. We evaluate our reporting units when changes in our operating structure occur, and if necessary, reassign goodwill using a relative fair value allocation approach. We test our goodwill for impairment at least annually, or more frequently if events or changes in circumstances indicate that the asset may be impaired. Goodwill impairments were not material for the periods presented. Intangible assets with definite lives are amortized over their estimated useful lives. We amortize intangible assets on a straight-line basis with definite lives over periods ranging from one to twelve years.
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 3, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In fiscal year 2018, Alphabet stated that it evaluates its reporting units “when changes in our operating structure occur,” and “if necessary, reassign[s] goodwill using a relative fair value allocation approach.” [GOOGL FY2018, Item 8, GOOGL_FY2018_2018-12-31:300] | supported | The cited 2018 filing states both quoted phrases exactly. |
| In fiscal year 2022, Alphabet stated that it evaluates its reporting units “periodically, as well as when changes in our operating segments occur,” and that for changes in reporting units, it “reassign[s] goodwill using a relative fair value allocation approach.” [GOOGL FY2022, Item 8, GOOGL_FY2022_2022-12-31:313] | supported | The cited 2022 filing states both quoted phrases exactly. |
| So, the description changed from evaluating reporting units only when changes in the company’s operating structure occur to evaluating them periodically and also when changes in operating segments occur, and the goodwill reassignment language changed from “if necessary” to specifically applying reassignment “for changes in reporting units,” while still using a relative fair value allocation approach. [GOOGL FY2018, Item 8, GOOGL_FY2018_2018-12-31:300] [GOOGL FY2022, Item 8, GOOGL_FY2022_2022-12-31:313] | supported | The two cited passages show the described wording changes while retaining the relative fair value allocation approach. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 13, cited: 2.

**Generated answer**

> In fiscal year 2018, Alphabet stated that it evaluates its reporting units when changes in its operating structure occur, and if necessary, reassigns goodwill using a relative fair value allocation approach. [GOOGL FY2018, Item 8, GOOGL_FY2018_2018-12-31:300]
>
> In fiscal year 2022, Alphabet stated that it evaluates its reporting units periodically, as well as when changes in its operating segments occur. [GOOGL FY2022, Item 8, GOOGL_FY2022_2022-12-31:313]
>
> In fiscal year 2022, Alphabet also stated more specifically that for changes in reporting units, it reassigns goodwill using a relative fair value allocation approach. [GOOGL FY2022, Item 8, GOOGL_FY2022_2022-12-31:313]
>
> So, the description changed from evaluating reporting units only when changes in operating structure occur in 2018 to evaluating them periodically and also when changes in operating segments occur in 2022, while the goodwill reassignment language became more explicit by tying the relative fair value allocation approach specifically to changes in reporting units rather than saying “if necessary.” [GOOGL FY2022, Item 8, GOOGL_FY2022_2022-12-31:313] [GOOGL FY2018, Item 8, GOOGL_FY2018_2018-12-31:300]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2022_2022-12-31:313` | Item 8 › Long-Lived Assets, Goodwill and Other Acquired Intangible Assets | ✓ | #1, #2 | We review property and equipment and intangible assets, excluding goodwill, for impairment when events or changes in circumstances indicate the carrying amount may not be recoverable. The evaluation is performed at the l… |
| 2 | `GOOGL_FY2018_2018-12-31:227` | Item 7 › Critical Accounting Policies and Estimates |  |  | Please see Notes to Consolidated Financial Statements included in Part II, Item 8 of this Annual Report on Form 10-K for a summary of significant accounting policies and the effect on our financial statements. |
| 3 | `GOOGL_FY2018_2018-12-31:300` | Item 8 › Long-Lived Assets, Goodwill and Other Acquired Intangible Assets | ✓ | #1, #2 | We review property and equipment, long-term prepayments and intangible assets, excluding goodwill, for impairment when events or changes in circumstances indicate the carrying amount may not be recoverable. We measure re… |
| 4 | `GOOGL_FY2018_2018-12-31:256` | Item 8 › Opinion on Internal Control over Financial Reporting |  |  | We have audited Alphabet Inc.’s internal control over financial reporting as of December 31, 2018, based on criteria established in Internal Control-Integrated Framework issued by the Committee of Sponsoring Organization… |
| 5 | `GOOGL_FY2022_2022-12-31:256` | Item 8 › Opinion on Internal Control Over Financial Reporting |  |  | We have audited Alphabet Inc.’s internal control over financial reporting as of December 31, 2022, based on criteria established in Internal Control—Integrated Framework issued by the Committee of Sponsoring Organization… |
| 6 | `GOOGL_FY2022_2022-12-31:250` | Item 8 › Opinion on the Financial Statements |  |  | We have audited the accompanying consolidated balance sheets of Alphabet Inc. (the Company) as of December 31, 2021 and 2022, the related consolidated statements of income, comprehensive income, stockholders' equity and … |
| 7 | `GOOGL_FY2022_2022-12-31:261` | Item 8 › (in millions, except par value per share amounts) |  |  | \| \| As of December 31, \| \| \|---\|---\|---\| \| \| 2021 \| 2022 \| \| Assets \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $20,945 \| $21,879 \| \| Marketable securities \| 118,704 \| 91,883 \| \| Total cash, cash equivale… |
| 8 | `GOOGL_FY2022_2022-12-31:275` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2020 \| 2021 \| 2022 \| \| Proceeds from issuance of debt, net of costs \| 11,761 \| 20,199 \| 52,872 \| \| Repayments of debt \| (2,100) \| (21,435) \| (54,068) \| \| Proceeds f… |
| 9 | `GOOGL_FY2018_2018-12-31:248` | Item 8 › INDEX TO CONSOLIDATED FINANCIAL STATEMENTS |  |  | \| \| Page \| \|---\|---\| \| Reports of Ernst & Young LLP, Independent Registered Public Accounting Firm \| 44 \| \| Financial Statements: \| \| \| Consolidated Balance Sheets \| 46 \| \| Consolidated Statements of Income \| 47 \| \| Cons… |
| 10 | `GOOGL_FY2018_2018-12-31:261` | Item 8 › (In millions, except share amounts which are reflected in thousands, and par value per share amounts) |  |  | \| \| As of December 31, 2017 \| As of December 31, 2018 \| \|---\|---\|---\| \| Assets \| \| \| \| Current assets: \| \| \| \| Cash and cash equivalents \| $10,715 \| $16,701 \| \| Marketable securities \| 91,156 \| 92,439 \| \| Total cash, cas… |
| 11 | `GOOGL_FY2022_2022-12-31:273` | Item 8 › (in millions) |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2020 \| 2021 \| 2022 \| \| Operating activities \| \| \| \| \| Net income \| $40,269 \| $76,033 \| $59,972 \| \| Adjustments: \| \| \| \| \| Depreciation and impairment of property an… |
| 12 | `GOOGL_FY2022_2022-12-31:402` | Item 8 › Mandiant Acquisition |  |  | \| Intangible assets \| $840 \| \|---\|---\| \| Goodwill(1) \| 4,772 \| \| Net assets acquired(2) \| 489 \| \| Total purchase price \| $6,101 \| |
| 13 | `GOOGL_FY2022_2022-12-31:409` | Item 8 › Other Intangible Assets |  |  | \| \| As of December 31, 2021 \| \| \| As of December 31, 2022 \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Gross Carrying Amount \| Accumulated Amortization \| Net Carrying Amount \| Gross Carrying Amount \| Accumulated Amortiz… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2022_2022-12-31:313`** (cited, gold #1, gold #2)

````text
ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Long-Lived Assets, Goodwill and Other Acquired Intangible Assets
We review property and equipment and intangible assets, excluding goodwill, for impairment when events or changes in circumstances indicate the carrying amount may not be recoverable. The evaluation is performed at the lowest level of identifiable cash flows independent of other assets. We measure recoverability of these assets by Table of Contents Alphabet Inc. comparing the carrying amounts to the future undiscounted cash flows that the assets or the asset group are expected to generate. If the carrying value of the assets or asset group is not recoverable, the impairment recognized is measured as the amount by which the carrying value exceeds its fair value. Impairments were not material for the periods presented. We allocate goodwill to reporting units based on the expected benefit from the business combination. We evaluate our reporting units periodically, as well as when changes in our operating segments occur. For changes in reporting units, we reassign goodwill using a relative fair value allocation approach. We test our goodwill for impairment at least annually, or more frequently if events or changes in circumstances indicate that the asset may be impaired. Goodwill impairments were not material for the periods presented.
````

**#3 `GOOGL_FY2018_2018-12-31:300`** (cited, gold #1, gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Long-Lived Assets, Goodwill and Other Acquired Intangible Assets
We review property and equipment, long-term prepayments and intangible assets, excluding goodwill, for impairment when events or changes in circumstances indicate the carrying amount may not be recoverable. We measure recoverability of these assets by comparing the carrying amounts to the future undiscounted cash flows that the assets or the asset group are expected to generate. If the carrying value of the assets are not recoverable, the impairment recognized is measured as the amount by which the carrying value of the asset exceeds its fair value. Impairments were not material for the periods presented. We allocate goodwill to reporting units based on the expected benefit from the business combination. We evaluate our reporting units when changes in our operating structure occur, and if necessary, reassign goodwill using a relative fair value allocation approach. We test our goodwill for impairment at least annually, or more frequently if events or changes in circumstances indicate that the asset may be impaired. Goodwill impairments were not material for the periods presented. Intangible assets with definite lives are amortized over their estimated useful lives. We amortize intangible assets on a straight-line basis with definite lives over periods ranging from one to twelve years.
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 4, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In fiscal year 2018, Alphabet stated that it evaluates its reporting units when changes in its operating structure occur, and if necessary, reassigns goodwill using a relative fair value allocation approach. [GOOGL FY2018, Item 8, GOOGL_FY2018_2018-12-31:300] | supported | The cited 2018 text states both that reporting units are evaluated when operating structure changes occur and that goodwill is reassigned if necessary using a relative fair value allocation approach. |
| In fiscal year 2022, Alphabet stated that it evaluates its reporting units periodically, as well as when changes in its operating segments occur. [GOOGL FY2022, Item 8, GOOGL_FY2022_2022-12-31:313] | supported | The cited 2022 text explicitly says Alphabet evaluates reporting units periodically and when changes in operating segments occur. |
| In fiscal year 2022, Alphabet also stated more specifically that for changes in reporting units, it reassigns goodwill using a relative fair value allocation approach. [GOOGL FY2022, Item 8, GOOGL_FY2022_2022-12-31:313] | supported | The cited 2022 text explicitly states that for changes in reporting units, goodwill is reassigned using a relative fair value allocation approach. |
| So, the description changed from evaluating reporting units only when changes in operating structure occur in 2018 to evaluating them periodically and also when changes in operating segments occur in 2022, while the goodwill reassignment language became more explicit by tying the relative fair value allocation approach specifically to changes in reporting units rather than saying “if necessary.” [GOOGL FY2022, Item 8, GOOGL_FY2022_2022-12-31:313] [GOOGL FY2018, Item 8, GOOGL_FY2018_2018-12-31:300] | supported | The 2018 and 2022 excerpts support the described wording change from operating-structure-triggered evaluation with 'if necessary' reassignment to periodic/operating-segment evaluation and reassignment tied to changes in reporting units. |

</details>
