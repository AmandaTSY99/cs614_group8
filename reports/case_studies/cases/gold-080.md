# gold-080: Cross-year text

[← all cases](../README.md) · company: Meta Platforms, Inc. (META) · fiscal year: 2021 · recipe `cross_year_text` · hop `multi` · answer type `qualitative` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> Based on the 2016 and 2021 10-K filings for Meta Platforms, how did the company's accounting policy description regarding the measurement period for business combinations change between these two fiscal years, and what specific valuation estimates were highlighted in the 2016 filing that were omitted from the 2021 description?

**Gold answer**

> The 2016 filing described the measurement period as 'one year from the acquisition date' and explicitly listed significant valuation estimates such as future expected cash flows from acquired users, acquired technology, and trade names, along with useful lives and discount rates. In contrast, the 2021 filing updated the policy to state the measurement period is 'not to exceed one year from the acquisition date' and omitted the specific list of valuation estimate types, focusing instead on the general allocation of fair value to tangible assets, liabilities, and intangible assets.

**Key points** (RQ3 keypoint_recall targets)

1. The 2021 filing specifies the measurement period is 'not to exceed one year', whereas the 2016 filing stated it was 'one year'.
2. The 2016 filing explicitly identified future expected cash flows from acquired users, technology, and trade names as significant valuation estimates.
3. The 2021 filing omitted the specific list of valuation estimates (users, technology, trade names) present in the 2016 filing.

**Gold evidence**

1. `META_FY2021_2021-12-31` · Item 8.Financial Statements and Supplementary Data › Business Combinations · text

   > During the measurement period, which is not to exceed one year from the acquisition date, we record adjustments to the assets acquired and liabilities assumed, with the corresponding offset to goodwill.

2. `META_FY2016_2016-12-31` · Item 8. Financial Statements and Supplementary Data › Business Combinations · text

   > Significant estimates in valuing certain intangible assets include, but are not limited to, future expected cash flows from acquired users, acquired technology, and trade names from a market participant perspective, useful lives and discount rates.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 15 | 13 |
| recall@5 | 0.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 0.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 0 | 1 | 1 | 1 |
| average precision (lexical) | 0.00 | 0.58 | 0.67 | 0.76 |
| gold evidence first rank | #1: –, #2: – | #1: 2, #2: 2 | #1: 1, #2: 4 | #1: 1, #2: 3 |
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
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 1617 | 1434 | 15992 | 14617 |
| cost (USD) | 0.0002 | 0.0003 | 0.0633 | 0.0597 |
| latency (s) | 1.6 | 7.4 | 34.5 | 31.7 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2021_2021-12-31:344` | Item 7 › Recently Issued Accounting Pronouncements |  |  | For further information on recently issued accounting pronouncements, see Note 1 — Summary of Significant Accounting Policies in the accompanying notes to consolidated financial statements included in Part II, Item 8, "F… |
| 2 | `META_FY2021_2021-12-31:536` | Item 15 |  |  | We have filed the following documents as part of this Form 10-K: 1. Consolidated Financial Statements: |
| 3 | `META_FY2021_2021-12-31:524` | Item 9 |  |  | None. |
| 4 | `META_FY2021_2021-12-31:350` | Item 7A › Equity Investment Risk |  |  | 31, 2021 and December 31, 2020, respectively. For additional information about our equity investments, see Note 1 — Summary of Significant Accounting Policies, Note 5 — Equity Investments, and Note 6 — Fair Value Measure… |
| 5 | `META_FY2021_2021-12-31:297` | Item 7 › Results of Operations |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Revenue \| $117,929 \| $85,965 \| $70,697 \| \| Costs and expenses: \| \| \| \| \| Cost of revenue \| 22,649 \| 16,692 \| 12,770 \| \| Research and developm… |
| 6 | `META_FY2021_2021-12-31:324` | Item 7 › Interest and other income, net |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| 2021 vs 2020 % Change \| 2020 vs 2019 % Change \| \| \| (dollars in millions) \| \| \| \| \| \| Interest income, net \| $461 \| $672 \| $904 \| (… |
| 7 | `META_FY2021_2021-12-31:326` | Item 7 › Provision for income taxes |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| 2021 vs 2020 % Change \| 2020 vs 2019 % Change \| \| \| (dollars in millions) \| \| \| \| \| \| Provision for income taxes \| $7,914 \| $4,034 … |
| 8 | `META_FY2021_2021-12-31:546` | Item 16 |  |  | None. |
| 9 | `META_FY2021_2021-12-31:299` | Item 7 › Results of Operations |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Revenue \| 100% \| 100% \| 100% \| \| Costs and expenses: \| \| \| \| \| Cost of revenue \| 19 \| 19 \| 18 \| \| Research and development \| 21 \| 21 \| 19 \| \|… |
| 10 | `META_FY2021_2021-12-31:314` | Item 7 › Research and development |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| 2021 vs 2020 % Change \| 2020 vs 2019 % Change \| \| \| (dollars in millions) \| \| \| \| \| \| Research and development \| $24,655 \| $18,447 … |

RQ2 citation match (section level): `no citations`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 5.

**Generated answer**

> In the provided context, the 2016 filing explicitly described the measurement period for business combinations as “one year from the acquisition date,” during which Meta could record adjustments to assets acquired and liabilities assumed with a corresponding offset to goodwill; after that period, subsequent adjustments were recorded to earnings [2][3].
>
> By contrast, the 2021 context provided does not include any business combinations accounting policy description or measurement-period discussion, so no 2021 wording is available here for comparison [1][4][5].
>
> The specific valuation estimates highlighted in the 2016 filing were:
> - future expected cash flows from acquired users,
> - acquired technology,
> - trade names from a market participant perspective,
> - useful lives, and
> - discount rates [2][3].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2021_2021-12-31:392` | Item 8 › Organization and Description of Business | ✓ |  | We were incorporated in Delaware in July 2004. In October 2021, we changed our corporate name from Facebook, Inc. to Meta Platforms, Inc. Our mission is to give people the power to build community and bring the world clo… |
| 2 | `META_FY2016_2016-12-31:329` | Item 8 › Business Combinations | ✓ | #1, #2 | We allocate the fair value of purchase consideration to the tangible assets acquired, liabilities assumed and intangible assets acquired based on their estimated fair values. The excess of the fair value of purchase cons… |
| 3 | `META_FY2016_2016-12-31:197` | Item 7 › Business Combinations and Valuation of Goodwill and Other Acquired Intangible Assets | ✓ | #1, #2 | We allocate the fair value of purchase consideration to the tangible assets acquired, liabilities assumed, and intangible assets acquired based on their estimated fair values. The excess of the fair value of purchase con… |
| 4 | `META_FY2021_2021-12-31:353` | Item 8 › Opinion on the Financial Statements | ✓ |  | We have audited the accompanying consolidated balance sheets of Meta Platforms, Inc. (the Company) as of December 31, 2021 and 2020, the related consolidated statements of income, comprehensive income, stockholders' equi… |
| 5 | `META_FY2021_2021-12-31:362` | Item 8 › Opinion on Internal Control over Financial Reporting | ✓ |  | We have audited Meta Platforms, Inc.'s internal control over financial reporting as of December 31, 2021, based on criteria established in Internal Control – Integrated Framework issued by the Committee of Sponsoring Org… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2021_2021-12-31:392`** (cited)

````text
Item 8.Financial Statements and Supplementary Data > Organization and Description of Business
We were incorporated in Delaware in July 2004. In October 2021, we changed our corporate name from Facebook, Inc. to Meta Platforms, Inc. Our mission is to give people the power to build community and bring the world closer together. All of our products, including our apps, share the vision of helping to bring the metaverse to life. We report our financial results based on two reportable segments: Family of Apps (FoA) and Reality Labs (RL). The segment information aligns with how the chief operating decision maker (CODM), who is our Chief Executive Officer (CEO), reviews and manages the business. We generate substantially all of our revenue from advertising.
````

**#2 `META_FY2016_2016-12-31:329`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Business Combinations
We allocate the fair value of purchase consideration to the tangible assets acquired, liabilities assumed and intangible assets acquired based on their estimated fair values. The excess of the fair value of purchase consideration over the fair values of these identifiable assets and liabilities is recorded as goodwill. Such valuations require management to make significant estimates and assumptions, especially with respect to intangible assets. Significant estimates in valuing certain intangible assets include, but are not limited to, future expected cash flows from acquired users, acquired technology, and trade names from a market participant perspective, useful lives and discount rates. Management’s estimates of fair value are based upon assumptions believed to be reasonable, but which are inherently uncertain and unpredictable and, as a result, actual results may differ from estimates. During the measurement period, which is one year from the acquisition date, we may record adjustments to the assets acquired and liabilities assumed, with the corresponding offset to goodwill. Upon the conclusion of the measurement period, any subsequent adjustments are recorded to earnings.
````

**#3 `META_FY2016_2016-12-31:197`** (cited, gold #1, gold #2)

````text
Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations > Business Combinations and Valuation of Goodwill and Other Acquired Intangible Assets
We allocate the fair value of purchase consideration to the tangible assets acquired, liabilities assumed, and intangible assets acquired based on their estimated fair values. The excess of the fair value of purchase consideration over the fair values of these identifiable assets and liabilities is recorded as goodwill. Such valuations require management to make significant estimates and assumptions, especially with respect to intangible assets. Significant estimates in valuing certain intangible assets include, but are not limited to, future expected cash flows from acquired users, acquired technology, and trade names from a market participant perspective, useful lives, and discount rates. Management’s estimates of fair value are based upon assumptions believed to be reasonable, but which are inherently uncertain and unpredictable and, as a result, actual results may differ from estimates. During the measurement period, which is one year from the acquisition date, we may record adjustments to the assets acquired and liabilities assumed, with the corresponding offset to goodwill. Upon the conclusion of the measurement period, any subsequent adjustments are recorded to earnings.
````

**#4 `META_FY2021_2021-12-31:353`** (cited)

````text
Item 8.Financial Statements and Supplementary Data > Opinion on the Financial Statements
We have audited the accompanying consolidated balance sheets of Meta Platforms, Inc. (the Company) as of December 31, 2021 and 2020, the related consolidated statements of income, comprehensive income, stockholders' equity and cash flows for each of the three years in the period ended December 31, 2021, and the related notes (collectively referred to as the "consolidated financial statements"). In our opinion, the consolidated financial statements present fairly, in all material respects, the financial position of the Company at December 31, 2021 and 2020, and the results of its operations and its cash flows for each of the three years in the period ended December 31, 2021, in conformity with U.S. generally accepted accounting principles. We also have audited, in accordance with the standards of the Public Company Accounting Oversight Board (United States) (PCAOB), the Company's internal control over financial reporting as of December 31, 2021, based on criteria established in Internal Control – Integrated Framework issued by the Committee of Sponsoring Organizations of the Treadway Commission (2013 framework), and our report dated February 2, 2022 expressed an unqualified opinion thereon.
````

**#5 `META_FY2021_2021-12-31:362`** (cited)

````text
Item 8.Financial Statements and Supplementary Data > Opinion on Internal Control over Financial Reporting
We have audited Meta Platforms, Inc.'s internal control over financial reporting as of December 31, 2021, based on criteria established in Internal Control – Integrated Framework issued by the Committee of Sponsoring Organizations of the Treadway Commission (2013 framework) (the COSO criteria). In our opinion, Meta Platforms, Inc. (the Company) maintained, in all material respects, effective internal control over financial reporting as of December 31, 2021, based on the COSO criteria. We also have audited, in accordance with the standards of the Public Company Accounting Oversight Board (United States) (PCAOB), the consolidated balance sheets of the Company as of December 31, 2021 and 2020, the related consolidated statements of income, comprehensive income, stockholders' equity and cash flows for each of the three years in the period ended December 31, 2021, and the related notes and our report dated February 2, 2022 expressed an unqualified opinion thereon.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8'), ('META', 'Item 7')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 15, cited: 3.

**Generated answer**

> In the 2016 filing, Meta stated that during the measurement period, “which is one year from the acquisition date,” it may record adjustments to the assets acquired and liabilities assumed, with the corresponding offset to goodwill, and that subsequent adjustments after the measurement period are recorded to earnings. [META FY2016, Item 8, META_FY2016_2016-12-31:329] [META FY2016, Item 7, META_FY2016_2016-12-31:197]
>
> In the 2021 filing, Meta described the measurement period as one “which is not to exceed one year from the acquisition date,” stated that it records adjustments to the assets acquired and liabilities assumed with the corresponding offset to goodwill during that period, and that any subsequent adjustments are recorded to earnings upon the conclusion of the measurement period. [META FY2021, Item 8, META_FY2021_2021-12-31:427]
>
> The 2016 filing specifically highlighted that valuations required significant estimates and assumptions, especially for intangible assets, including future expected cash flows from acquired users, acquired technology, and trade names from a market participant perspective, as well as useful lives and discount rates. [META FY2016, Item 8, META_FY2016_2016-12-31:329] [META FY2016, Item 7, META_FY2016_2016-12-31:197]
>
> Those specific valuation estimate examples were omitted from the 2021 description, which did not list acquired users, acquired technology, trade names, useful lives, or discount rates in its business combinations policy description. [META FY2021, Item 8, META_FY2021_2021-12-31:427] [META FY2016, Item 8, META_FY2016_2016-12-31:329] [META FY2016, Item 7, META_FY2016_2016-12-31:197]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2021_2021-12-31:427` | Item 8 › Business Combinations | ✓ | #1 | We allocate the fair value of purchase consideration to the tangible assets acquired, liabilities assumed and intangible assets acquired based on their estimated fair values. The excess of the fair value of purchase cons… |
| 2 | `META_FY2021_2021-12-31:436` | Item 8 › Accounting Pronouncements Not Yet Adopted |  |  | In October 2021, the FASB issued ASU No. 2021-08, Business Combinations (Topic 805): Accounting for Contract Assets and Contract Liabilities from Contracts with Customers (ASU 2021-08), which clarifies that an acquirer o… |
| 3 | `META_FY2016_2016-12-31:189` | Item 7 › Critical Accounting Policies and Estimates |  |  | An accounting policy is deemed to be critical if it requires an accounting estimate to be made based on assumptions about matters that are highly uncertain at the time the estimate is made, if different estimates reasona… |
| 4 | `META_FY2016_2016-12-31:329` | Item 8 › Business Combinations | ✓ | #1, #2 | We allocate the fair value of purchase consideration to the tangible assets acquired, liabilities assumed and intangible assets acquired based on their estimated fair values. The excess of the fair value of purchase cons… |
| 5 | `META_FY2021_2021-12-31:277` | Item 7 › Critical Accounting Policies and Estimates |  |  | An accounting policy is deemed to be critical if the nature of the estimates or assumptions is material due to the levels of subjectivity and judgment necessary to account for highly uncertain matters or the susceptibili… |
| 6 | `META_FY2016_2016-12-31:197` | Item 7 › Business Combinations and Valuation of Goodwill and Other Acquired Intangible Assets | ✓ | #1, #2 | We allocate the fair value of purchase consideration to the tangible assets acquired, liabilities assumed, and intangible assets acquired based on their estimated fair values. The excess of the fair value of purchase con… |
| 7 | `META_FY2021_2021-12-31:388` | Item 8 › CONSOLIDATED STATEMENTS OF CASH FLOWS |  |  | See Accompanying Notes to Consolidated Financial Statements. |
| 8 | `META_FY2021_2021-12-31:391` | Item 8 › CONSOLIDATED STATEMENTS OF CASH FLOWS |  |  | See Accompanying Notes to Consolidated Financial Statements. |
| 9 | `META_FY2021_2021-12-31:466` | Item 8 › Note 8.Leases |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2021 \| 2020 \| 2019 \| \| Cash paid for amounts included in the measurement of lease liabilities: \| \| \| \| \| Operating cash flows for operating leases \| $1,406 \| $1,208… |
| 10 | `META_FY2021_2021-12-31:464` | Item 8 › Note 8.Leases |  |  | \| \| Operating Leases \| Finance Leases \| \|---\|---\|---\| \| 2022 \| $1,425 \| $90 \| \| 2023 \| 1,542 \| 65 \| \| 2024 \| 1,513 \| 45 \| \| 2025 \| 1,354 \| 45 \| \| 2026 \| 1,295 \| 45 \| \| Thereafter \| 9,995 \| 406 \| \| Total undiscounted cash… |
| 11 | `META_FY2021_2021-12-31:395` | Item 8 › Use of Estimates |  |  | In connection with our periodic reviews of the estimated useful lives of property and equipment, we extended the estimated average useful lives of selected cohorts of servers and network assets from three years to four y… |
| 12 | `META_FY2016_2016-12-31:304` | Item 8 › NOTES TO CONSOLIDATED FINANCIAL STATEMENTS |  |  | Note 1. Summary of Significant Accounting Policies |
| 13 | `META_FY2016_2016-12-31:340` | Item 8 › Accounting Pronouncements Adopted in 2016 |  |  | We adopted the aspects of the standard affecting the cash flow presentation retrospectively, and accordingly, to conform to the current year presentation, we reclassified $1.72 billion and $1.87 billion of excess tax ben… |
| 14 | `META_FY2016_2016-12-31:199` | Item 7 › Business Combinations and Valuation of Goodwill and Other Acquired Intangible Assets |  |  | In addition to the recoverability assessment, we routinely review the remaining estimated useful lives of our finite-lived intangible assets. If we reduce the estimated useful life assumption for any asset, the remaining… |
| 15 | `META_FY2016_2016-12-31:344` | Item 8 › Accounting Pronouncements Adopted in 2016 |  |  | In August 2016, the FASB issued Accounting Standards Update No. 2016-15, Statement of Cash Flows (Topic 230) (ASU 2016-15), which addresses eight specific cash flow classification issues to reduce diversity in practice. … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2021_2021-12-31:427`** (cited, gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Business Combinations
We allocate the fair value of purchase consideration to the tangible assets acquired, liabilities assumed and intangible assets acquired based on their estimated fair values. The excess of the fair value of purchase consideration over the fair values of these identifiable assets and liabilities is recorded as goodwill to reporting units based on the expected benefit from the business combination. Allocation of purchase consideration to identifiable assets and liabilities affects the amortization expense, as acquired finite-lived intangible assets are amortized over the useful life, whereas any indefinite-lived intangible assets, including goodwill, are not amortized. During the measurement period, which is not to exceed one year from the acquisition date, we record adjustments to the assets acquired and liabilities assumed, with the corresponding offset to goodwill. Upon the conclusion of the measurement period, any subsequent adjustments are recorded to earnings. Acquisition-related expenses are recognized separately from business combinations and are expensed as incurred.
````

**#4 `META_FY2016_2016-12-31:329`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Business Combinations
We allocate the fair value of purchase consideration to the tangible assets acquired, liabilities assumed and intangible assets acquired based on their estimated fair values. The excess of the fair value of purchase consideration over the fair values of these identifiable assets and liabilities is recorded as goodwill. Such valuations require management to make significant estimates and assumptions, especially with respect to intangible assets. Significant estimates in valuing certain intangible assets include, but are not limited to, future expected cash flows from acquired users, acquired technology, and trade names from a market participant perspective, useful lives and discount rates. Management’s estimates of fair value are based upon assumptions believed to be reasonable, but which are inherently uncertain and unpredictable and, as a result, actual results may differ from estimates. During the measurement period, which is one year from the acquisition date, we may record adjustments to the assets acquired and liabilities assumed, with the corresponding offset to goodwill. Upon the conclusion of the measurement period, any subsequent adjustments are recorded to earnings.
````

**#6 `META_FY2016_2016-12-31:197`** (cited, gold #1, gold #2)

````text
Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations > Business Combinations and Valuation of Goodwill and Other Acquired Intangible Assets
We allocate the fair value of purchase consideration to the tangible assets acquired, liabilities assumed, and intangible assets acquired based on their estimated fair values. The excess of the fair value of purchase consideration over the fair values of these identifiable assets and liabilities is recorded as goodwill. Such valuations require management to make significant estimates and assumptions, especially with respect to intangible assets. Significant estimates in valuing certain intangible assets include, but are not limited to, future expected cash flows from acquired users, acquired technology, and trade names from a market participant perspective, useful lives, and discount rates. Management’s estimates of fair value are based upon assumptions believed to be reasonable, but which are inherently uncertain and unpredictable and, as a result, actual results may differ from estimates. During the measurement period, which is one year from the acquisition date, we may record adjustments to the assets acquired and liabilities assumed, with the corresponding offset to goodwill. Upon the conclusion of the measurement period, any subsequent adjustments are recorded to earnings.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8'), ('META', 'Item 7')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 4, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In the 2016 filing, Meta stated that during the measurement period, “which is one year from the acquisition date,” it may record adjustments to the assets acquired and liabilities assumed, with the corresponding offset to goodwill, and that subsequent adjustments after the measurement period are recorded to earnings. [META FY2016, Item 8, META_FY2016_2016-12-31:329] [META FY2016, Item 7, META_FY2016_2016-12-31:197] | supported | The cited 2016 passages state the one-year measurement period, goodwill offset for adjustments, and earnings treatment after the period. |
| In the 2021 filing, Meta described the measurement period as one “which is not to exceed one year from the acquisition date,” stated that it records adjustments to the assets acquired and liabilities assumed with the corresponding offset to goodwill during that period, and that any subsequent adjustments are recorded to earnings upon the conclusion of the measurement period. [META FY2021, Item 8, META_FY2021_2021-12-31:427] | supported | The 2021 cited passage explicitly says the measurement period does not exceed one year, adjustments offset goodwill, and later adjustments go to earnings. |
| The 2016 filing specifically highlighted that valuations required significant estimates and assumptions, especially for intangible assets, including future expected cash flows from acquired users, acquired technology, and trade names from a market participant perspective, as well as useful lives and discount rates. [META FY2016, Item 8, META_FY2016_2016-12-31:329] [META FY2016, Item 7, META_FY2016_2016-12-31:197] | supported | The 2016 cited text specifically lists those valuation estimates and assumptions for intangible assets. |
| Those specific valuation estimate examples were omitted from the 2021 description, which did not list acquired users, acquired technology, trade names, useful lives, or discount rates in its business combinations policy description. [META FY2021, Item 8, META_FY2021_2021-12-31:427] [META FY2016, Item 8, META_FY2016_2016-12-31:329] [META FY2016, Item 7, META_FY2016_2016-12-31:197] | supported | The 2021 cited description omits those specific examples, while the 2016 cited text includes them. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 13, cited: 3.

**Generated answer**

> In 2016, Meta stated that “during the measurement period, which is one year from the acquisition date,” it may record adjustments to the assets acquired and liabilities assumed, with the corresponding offset to goodwill, and that subsequent adjustments after the measurement period are recorded to earnings [META FY2016, Item 8, META_FY2016_2016-12-31:329] [META FY2016, Item 7, META_FY2016_2016-12-31:197].  
>
> In 2021, Meta revised that description to say the measurement period “is not to exceed one year from the acquisition date,” while still stating that adjustments during the measurement period are recorded to the assets acquired and liabilities assumed with the corresponding offset to goodwill, and that subsequent adjustments are recorded to earnings [META FY2021, Item 8, META_FY2021_2021-12-31:427].  
>
> The 2016 filing also specifically highlighted significant valuation estimates for certain intangible assets, including future expected cash flows from acquired users, acquired technology, and trade names from a market participant perspective, as well as useful lives and discount rates [META FY2016, Item 8, META_FY2016_2016-12-31:329] [META FY2016, Item 7, META_FY2016_2016-12-31:197].  
>
> Those specific valuation estimate examples were omitted from the 2021 business combinations policy description [META FY2021, Item 8, META_FY2021_2021-12-31:427].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2021_2021-12-31:427` | Item 8 › Business Combinations | ✓ | #1 | We allocate the fair value of purchase consideration to the tangible assets acquired, liabilities assumed and intangible assets acquired based on their estimated fair values. The excess of the fair value of purchase cons… |
| 2 | `META_FY2021_2021-12-31:436` | Item 8 › Accounting Pronouncements Not Yet Adopted |  |  | In October 2021, the FASB issued ASU No. 2021-08, Business Combinations (Topic 805): Accounting for Contract Assets and Contract Liabilities from Contracts with Customers (ASU 2021-08), which clarifies that an acquirer o… |
| 3 | `META_FY2016_2016-12-31:329` | Item 8 › Business Combinations | ✓ | #1, #2 | We allocate the fair value of purchase consideration to the tangible assets acquired, liabilities assumed and intangible assets acquired based on their estimated fair values. The excess of the fair value of purchase cons… |
| 4 | `META_FY2016_2016-12-31:189` | Item 7 › Critical Accounting Policies and Estimates |  |  | An accounting policy is deemed to be critical if it requires an accounting estimate to be made based on assumptions about matters that are highly uncertain at the time the estimate is made, if different estimates reasona… |
| 5 | `META_FY2016_2016-12-31:197` | Item 7 › Business Combinations and Valuation of Goodwill and Other Acquired Intangible Assets | ✓ | #1, #2 | We allocate the fair value of purchase consideration to the tangible assets acquired, liabilities assumed, and intangible assets acquired based on their estimated fair values. The excess of the fair value of purchase con… |
| 6 | `META_FY2021_2021-12-31:277` | Item 7 › Critical Accounting Policies and Estimates |  |  | An accounting policy is deemed to be critical if the nature of the estimates or assumptions is material due to the levels of subjectivity and judgment necessary to account for highly uncertain matters or the susceptibili… |
| 7 | `META_FY2016_2016-12-31:304` | Item 8 › NOTES TO CONSOLIDATED FINANCIAL STATEMENTS |  |  | Note 1. Summary of Significant Accounting Policies |
| 8 | `META_FY2021_2021-12-31:350` | Item 7A › Equity Investment Risk |  |  | 31, 2021 and December 31, 2020, respectively. For additional information about our equity investments, see Note 1 — Summary of Significant Accounting Policies, Note 5 — Equity Investments, and Note 6 — Fair Value Measure… |
| 9 | `META_FY2021_2021-12-31:388` | Item 8 › CONSOLIDATED STATEMENTS OF CASH FLOWS |  |  | See Accompanying Notes to Consolidated Financial Statements. |
| 10 | `META_FY2021_2021-12-31:391` | Item 8 › CONSOLIDATED STATEMENTS OF CASH FLOWS |  |  | See Accompanying Notes to Consolidated Financial Statements. |
| 11 | `META_FY2016_2016-12-31:370` | Item 8 › Accounting Pronouncements Not Yet Adopted |  |  | \| \| \| December 31, 2016 \| \| \| December 31, 2015 \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Weighted-Average Remaining Useful Lives (in years) \| Gross Carrying Amount \| Accumulated Amortization \| Net Carrying Amount \| Gr… |
| 12 | `META_FY2016_2016-12-31:369` | Item 8 › Accounting Pronouncements Not Yet Adopted |  |  | \| \| \| December 31, 2016 \| \| \| December 31, 2015 \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Weighted-Average Remaining Useful Lives (in years) \| Gross Carrying Amount \| Accumulated Amortization \| Net Carrying Amount \| Gr… |
| 13 | `META_FY2021_2021-12-31:344` | Item 7 › Recently Issued Accounting Pronouncements |  |  | For further information on recently issued accounting pronouncements, see Note 1 — Summary of Significant Accounting Policies in the accompanying notes to consolidated financial statements included in Part II, Item 8, "F… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2021_2021-12-31:427`** (cited, gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Business Combinations
We allocate the fair value of purchase consideration to the tangible assets acquired, liabilities assumed and intangible assets acquired based on their estimated fair values. The excess of the fair value of purchase consideration over the fair values of these identifiable assets and liabilities is recorded as goodwill to reporting units based on the expected benefit from the business combination. Allocation of purchase consideration to identifiable assets and liabilities affects the amortization expense, as acquired finite-lived intangible assets are amortized over the useful life, whereas any indefinite-lived intangible assets, including goodwill, are not amortized. During the measurement period, which is not to exceed one year from the acquisition date, we record adjustments to the assets acquired and liabilities assumed, with the corresponding offset to goodwill. Upon the conclusion of the measurement period, any subsequent adjustments are recorded to earnings. Acquisition-related expenses are recognized separately from business combinations and are expensed as incurred.
````

**#3 `META_FY2016_2016-12-31:329`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Business Combinations
We allocate the fair value of purchase consideration to the tangible assets acquired, liabilities assumed and intangible assets acquired based on their estimated fair values. The excess of the fair value of purchase consideration over the fair values of these identifiable assets and liabilities is recorded as goodwill. Such valuations require management to make significant estimates and assumptions, especially with respect to intangible assets. Significant estimates in valuing certain intangible assets include, but are not limited to, future expected cash flows from acquired users, acquired technology, and trade names from a market participant perspective, useful lives and discount rates. Management’s estimates of fair value are based upon assumptions believed to be reasonable, but which are inherently uncertain and unpredictable and, as a result, actual results may differ from estimates. During the measurement period, which is one year from the acquisition date, we may record adjustments to the assets acquired and liabilities assumed, with the corresponding offset to goodwill. Upon the conclusion of the measurement period, any subsequent adjustments are recorded to earnings.
````

**#5 `META_FY2016_2016-12-31:197`** (cited, gold #1, gold #2)

````text
Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations > Business Combinations and Valuation of Goodwill and Other Acquired Intangible Assets
We allocate the fair value of purchase consideration to the tangible assets acquired, liabilities assumed, and intangible assets acquired based on their estimated fair values. The excess of the fair value of purchase consideration over the fair values of these identifiable assets and liabilities is recorded as goodwill. Such valuations require management to make significant estimates and assumptions, especially with respect to intangible assets. Significant estimates in valuing certain intangible assets include, but are not limited to, future expected cash flows from acquired users, acquired technology, and trade names from a market participant perspective, useful lives, and discount rates. Management’s estimates of fair value are based upon assumptions believed to be reasonable, but which are inherently uncertain and unpredictable and, as a result, actual results may differ from estimates. During the measurement period, which is one year from the acquisition date, we may record adjustments to the assets acquired and liabilities assumed, with the corresponding offset to goodwill. Upon the conclusion of the measurement period, any subsequent adjustments are recorded to earnings.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8'), ('META', 'Item 7')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 4, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In 2016, Meta stated that “during the measurement period, which is one year from the acquisition date,” it may record adjustments to the assets acquired and liabilities assumed, with the corresponding offset to goodwill, and that subsequent adjustments after the measurement period are recorded to earnings [META FY2016, Item 8, META_FY2016_2016-12-31:329] [META FY2016, Item 7, META_FY2016_2016-12-31:197]. | supported | The cited 2016 passages state the one-year measurement period, goodwill offset, and subsequent adjustments to earnings. |
| In 2021, Meta revised that description to say the measurement period “is not to exceed one year from the acquisition date,” while still stating that adjustments during the measurement period are recorded to the assets acquired and liabilities assumed with the corresponding offset to goodwill, and that subsequent adjustments are recorded to earnings [META FY2021, Item 8, META_FY2021_2021-12-31:427]. | supported | The 2021 cited passage explicitly says the period is not to exceed one year and describes the same goodwill and earnings treatment. |
| The 2016 filing also specifically highlighted significant valuation estimates for certain intangible assets, including future expected cash flows from acquired users, acquired technology, and trade names from a market participant perspective, as well as useful lives and discount rates [META FY2016, Item 8, META_FY2016_2016-12-31:329] [META FY2016, Item 7, META_FY2016_2016-12-31:197]. | supported | The 2016 cited passages specifically list those valuation estimate examples for intangible assets. |
| Those specific valuation estimate examples were omitted from the 2021 business combinations policy description [META FY2021, Item 8, META_FY2021_2021-12-31:427]. | supported | The 2021 cited policy description does not include those specific valuation estimate examples. |

</details>
