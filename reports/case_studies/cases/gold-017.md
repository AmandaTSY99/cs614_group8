# gold-017: Single-hop text

[← all cases](../README.md) · company: Meta Platforms, Inc. (META) · fiscal year: 2024 · recipe `text` · hop `single` · answer type `qualitative` · scope `single_doc` · RQ2 category `single_hop_factual`

## Gold QA

**Question**

> According to Meta Platforms, Inc.'s 2024 10-K, under what specific conditions does the company accrue a liability for legal and regulatory contingencies?

**Gold answer**

> Meta accrues a liability when it believes that it is both probable that a loss has been incurred and the amount of the loss can be reasonably estimated.

**Key points** (RQ3 keypoint_recall targets)

1. The loss must be probable
2. The amount of the loss must be reasonably estimable
3. This applies to both asserted and unasserted matters

**Gold evidence**

1. `META_FY2024_2024-12-31` · Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations › Loss Contingencies · text

   > With respect to these matters, asserted and unasserted, we evaluate the associated developments on a regular basis and accrue a liability when we believe that it is both probable that a loss has been incurred and the amount can be reasonably estimated.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 7 |
| recall@5 | 0.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.11 | 0.92 | 0.59 | 0.44 |
| gold evidence first rank | #1: 9 | #1: 1 | #1: 2 | #1: 3 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | – | – | – | – |
| keypoint_recall | 0.67 | 0.67 | 1.00 | 0.67 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 0.00 | 0.50 | 0.50 | 0.50 |
| citation recall | 0.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 0.00 | 0.67 | 0.67 | 0.67 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 1605 | 1411 | 5155 | 5891 |
| cost (USD) | 0.0003 | 0.0002 | 0.0179 | 0.0208 |
| latency (s) | 1.6 | 9.5 | 7.9 | 9.3 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> Meta says it accrues a liability for legal and regulatory contingencies **when it believes both that a loss is probable and that the amount can be reasonably estimated**. [9]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2024_2024-12-31:268` | Item 3 |  |  | Over the last several years, the number and potential significance of the litigation and investigations involving the company have increased, and there can be no assurance that this trend will not continue. For example, … |
| 2 | `META_FY2024_2024-12-31:13` | TABLE OF CONTENTS |  |  | \| \| \| Page \| \|---\|---\|---\| \| Note About Forward-Looking Statements \| \| 3 \| \| Limitations of Key Metrics and Other Data \| \| 4 \| \| PART I \| \| \| \| Item 1. \| Business \| 6 \| \| Item 1A. \| Risk Factors \| 14 \| \| Item 1B. \| Unres… |
| 3 | `META_FY2024_2024-12-31:14` | TABLE OF CONTENTS |  |  | \| \| \| Page \| \|---\|---\|---\| \| Item 9A. \| Controls and Procedures \| 123 \| \| Item 9B. \| Other Information \| 123 \| \| Item 9C. \| Disclosure Regarding Foreign Jurisdictions that Prevent Inspections \| 124 \| \| PART III \| \| \| \| I… |
| 4 | `META_FY2024_2024-12-31:543` | Item 8 › Note 11. Accrued Expenses and Other Current Liabilities |  |  | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2024 \| 2023 \| \| Legal-related accruals (1) \| $5,523 \| $6,592 \| \| Accrued compensation and benefits \| 6,350 \| 6,659 \| \| Accrued property and equipment \| 2,582 \| 2,213 \| \| Accrued tax… |
| 5 | `META_FY2024_2024-12-31:267` | Item 3 |  |  | business, or subject us to other structural or behavioral remedies that adversely affect our business. We have experienced such outcomes to varying degrees in the past, and we expect to continue to face a challenging lit… |
| 6 | `META_FY2024_2024-12-31:248` | Item 1A › Risks Related to Data, Security, Platform Integrity, and Intellectual Property |  |  | financial condition, and results of operations could be adversely affected as a result of an unfavorable resolution of the disputes and litigation referred to above. |
| 7 | `META_FY2024_2024-12-31:3` | (Exact name of registrant as specified in its charter) |  |  | __________________________ |
| 8 | `META_FY2024_2024-12-31:544` | Item 8 › Note 11. Accrued Expenses and Other Current Liabilities |  |  | _________________________ (1)Includes accruals for estimated fines, settlements, or other losses in connection with legal and related matters, as well as other legal fees. For further information, see Legal and Related M… |
| 9 | `META_FY2024_2024-12-31:479` | Item 8 › Loss Contingencies | ✓ | #1 | We are involved in legal proceedings, claims, and regulatory, tax or government inquiries and investigations that arise in the ordinary course of business. Certain of these matters include speculative claims for substant… |
| 10 | `META_FY2024_2024-12-31:619` | Item 9C |  |  | Not Applicable. |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#9 `META_FY2024_2024-12-31:479`** (cited, gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Loss Contingencies
We are involved in legal proceedings, claims, and regulatory, tax or government inquiries and investigations that arise in the ordinary course of business. Certain of these matters include speculative claims for substantial or indeterminate amounts of damages. Additionally, we are required to comply with various legal and regulatory obligations around the world, and we regularly become subject to new laws and regulations in the jurisdictions in which we operate. The requirements for complying with these obligations may be uncertain and subject to interpretation and enforcement by regulatory and other authorities, and any failure to comply with such obligations could eventually lead to asserted legal or regulatory action. With respect to these matters, asserted and unasserted, we evaluate the associated developments on a regular basis and accrue a liability when we believe that it is both probable that a loss has been incurred and the amount can be reasonably estimated. We record such losses as general and administrative expenses on our consolidated statements of income.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Meta accrues a liability for legal and regulatory contingencies when it believes that **it is both probable that a loss has been incurred and the amount can be reasonably estimated**. [2][4]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2024_2024-12-31:412` | Item 8 › Critical Audit Matters |  | #1 | \| \| Loss Contingencies \| \|---\|---\| \| Description of the Matter \| As described in Note 12 to the consolidated financial statements, the Company is party to various legal proceedings, claims, and regulatory or government i… |
| 2 | `META_FY2024_2024-12-31:337` | Item 7 › Loss Contingencies | ✓ | #1 | We are involved in legal proceedings, claims, and regulatory, tax or government inquiries and investigations that arise in the ordinary course of business. Certain of these matters include speculative claims for substant… |
| 3 | `META_FY2024_2024-12-31:628` | Item 15 |  |  | \| Exhibit \| \| Incorporated by Reference \| \| \| Filed Herewith \| \|---\|---\|---\|---\|---\|---\| \| Number \| Exhibit Description \| Form \| File No. \| Exhibit \| Filing Date \| \| 3.1 \| Amended and Restated Certificate of Incorporatio… |
| 4 | `META_FY2024_2024-12-31:479` | Item 8 › Loss Contingencies | ✓ | #1 | We are involved in legal proceedings, claims, and regulatory, tax or government inquiries and investigations that arise in the ordinary course of business. Certain of these matters include speculative claims for substant… |
| 5 | `META_FY2024_2024-12-31:629` | Item 15 |  |  | \| Exhibit \| \| Incorporated by Reference \| \| \| Filed Herewith \| \|---\|---\|---\|---\|---\|---\| \| 4.5 \| Second Supplemental Indenture, dated as of May 3, 2023, by and between Meta Platforms, Inc. and U.S. Bank Trust Company, Na… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2024_2024-12-31:412`** (gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Critical Audit Matters (table)
|  | Loss Contingencies |
|---|---|
| Description of the Matter | As described in Note 12 to the consolidated financial statements, the Company is party to various legal proceedings, claims, and regulatory or government inquiries and investigations. The Company accrues a liability when it believes a loss is probable and the amount can be reasonably estimated. In addition, the Company believes it is reasonably possible that it will incur a loss in some of these cases, actions or inquiries described above. When applicable, the Company discloses an estimate of the amount of loss or range of possible loss that may be incurred. However, for certain other matters, the Company discloses that the amount of such losses or a range of possible losses cannot be reasonably estimated at this time. Auditing the Company's accounting for, and disclosure of these loss contingencies was especially challenging due to the significant judgment required to evaluate management's assessments of the likelihood of a loss, and their estimate of the potential amount or range of such losses. |
````

**#2 `META_FY2024_2024-12-31:337`** (cited, gold #1)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Loss Contingencies
We are involved in legal proceedings, claims, and regulatory, tax or government inquiries and investigations that arise in the ordinary course of business. Certain of these matters include speculative claims for substantial or indeterminate amounts of damages. Additionally, we are required to comply with various legal and regulatory obligations around the world, and we regularly become subject to new laws and regulations in the jurisdictions in which we operate. The requirements for complying with these obligations may be uncertain and subject to interpretation and enforcement by regulatory and other authorities, and any failure to comply with such obligations could eventually lead to asserted legal or regulatory action. With respect to these matters, asserted and unasserted, we evaluate the associated developments on a regular basis and accrue a liability when we believe that it is both probable that a loss has been incurred and the amount can be reasonably estimated.
````

**#4 `META_FY2024_2024-12-31:479`** (cited, gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Loss Contingencies
We are involved in legal proceedings, claims, and regulatory, tax or government inquiries and investigations that arise in the ordinary course of business. Certain of these matters include speculative claims for substantial or indeterminate amounts of damages. Additionally, we are required to comply with various legal and regulatory obligations around the world, and we regularly become subject to new laws and regulations in the jurisdictions in which we operate. The requirements for complying with these obligations may be uncertain and subject to interpretation and enforcement by regulatory and other authorities, and any failure to comply with such obligations could eventually lead to asserted legal or regulatory action. With respect to these matters, asserted and unasserted, we evaluate the associated developments on a regular basis and accrue a liability when we believe that it is both probable that a loss has been incurred and the amount can be reasonably estimated. We record such losses as general and administrative expenses on our consolidated statements of income.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 7'), ('META', 'Item 8')] gold=[(None, 'Item 7')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 2.

**Generated answer**

> Meta Platforms, Inc. states that it accrues a liability for legal and regulatory contingencies when it believes that it is both probable that a loss has been incurred and the amount can be reasonably estimated. [META FY2024, Item 7, META_FY2024_2024-12-31:337] [META FY2024, Item 8, META_FY2024_2024-12-31:479]
>
> The company says it evaluates asserted and unasserted matters on a regular basis in making that determination. [META FY2024, Item 7, META_FY2024_2024-12-31:337] [META FY2024, Item 8, META_FY2024_2024-12-31:479]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2024_2024-12-31:268` | Item 3 |  |  | Over the last several years, the number and potential significance of the litigation and investigations involving the company have increased, and there can be no assurance that this trend will not continue. For example, … |
| 2 | `META_FY2024_2024-12-31:337` | Item 7 › Loss Contingencies | ✓ | #1 | We are involved in legal proceedings, claims, and regulatory, tax or government inquiries and investigations that arise in the ordinary course of business. Certain of these matters include speculative claims for substant… |
| 3 | `META_FY2024_2024-12-31:479` | Item 8 › Loss Contingencies | ✓ | #1 | We are involved in legal proceedings, claims, and regulatory, tax or government inquiries and investigations that arise in the ordinary course of business. Certain of these matters include speculative claims for substant… |
| 4 | `META_FY2024_2024-12-31:544` | Item 8 › Note 11. Accrued Expenses and Other Current Liabilities |  |  | _________________________ (1)Includes accruals for estimated fines, settlements, or other losses in connection with legal and related matters, as well as other legal fees. For further information, see Legal and Related M… |
| 5 | `META_FY2024_2024-12-31:412` | Item 8 › Critical Audit Matters |  | #1 | \| \| Loss Contingencies \| \|---\|---\| \| Description of the Matter \| As described in Note 12 to the consolidated financial statements, the Company is party to various legal proceedings, claims, and regulatory or government i… |
| 6 | `META_FY2024_2024-12-31:561` | Item 8 › Legal and Related Matters |  |  | IDPC are subject to review by other European privacy regulators as part of the GDPR's cooperation and consistency mechanisms, which may lead to significant changes in the final outcome of such investigations. As a result… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `META_FY2024_2024-12-31:337`** (cited, gold #1)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Loss Contingencies
We are involved in legal proceedings, claims, and regulatory, tax or government inquiries and investigations that arise in the ordinary course of business. Certain of these matters include speculative claims for substantial or indeterminate amounts of damages. Additionally, we are required to comply with various legal and regulatory obligations around the world, and we regularly become subject to new laws and regulations in the jurisdictions in which we operate. The requirements for complying with these obligations may be uncertain and subject to interpretation and enforcement by regulatory and other authorities, and any failure to comply with such obligations could eventually lead to asserted legal or regulatory action. With respect to these matters, asserted and unasserted, we evaluate the associated developments on a regular basis and accrue a liability when we believe that it is both probable that a loss has been incurred and the amount can be reasonably estimated.
````

**#3 `META_FY2024_2024-12-31:479`** (cited, gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Loss Contingencies
We are involved in legal proceedings, claims, and regulatory, tax or government inquiries and investigations that arise in the ordinary course of business. Certain of these matters include speculative claims for substantial or indeterminate amounts of damages. Additionally, we are required to comply with various legal and regulatory obligations around the world, and we regularly become subject to new laws and regulations in the jurisdictions in which we operate. The requirements for complying with these obligations may be uncertain and subject to interpretation and enforcement by regulatory and other authorities, and any failure to comply with such obligations could eventually lead to asserted legal or regulatory action. With respect to these matters, asserted and unasserted, we evaluate the associated developments on a regular basis and accrue a liability when we believe that it is both probable that a loss has been incurred and the amount can be reasonably estimated. We record such losses as general and administrative expenses on our consolidated statements of income.
````

**#5 `META_FY2024_2024-12-31:412`** (gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Critical Audit Matters (table)
|  | Loss Contingencies |
|---|---|
| Description of the Matter | As described in Note 12 to the consolidated financial statements, the Company is party to various legal proceedings, claims, and regulatory or government inquiries and investigations. The Company accrues a liability when it believes a loss is probable and the amount can be reasonably estimated. In addition, the Company believes it is reasonably possible that it will incur a loss in some of these cases, actions or inquiries described above. When applicable, the Company discloses an estimate of the amount of loss or range of possible loss that may be incurred. However, for certain other matters, the Company discloses that the amount of such losses or a range of possible losses cannot be reasonably estimated at this time. Auditing the Company's accounting for, and disclosure of these loss contingencies was especially challenging due to the significant judgment required to evaluate management's assessments of the likelihood of a loss, and their estimate of the potential amount or range of such losses. |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 7'), ('META', 'Item 8')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 2, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta Platforms, Inc. states that it accrues a liability for legal and regulatory contingencies when it believes that it is both probable that a loss has been incurred and the amount can be reasonably estimated. [META FY2024, Item 7, META_FY2024_2024-12-31:337] [META FY2024, Item 8, META_FY2024_2024-12-31:479] | supported | The cited text states Meta accrues a liability when a loss is probable and reasonably estimable. |
| The company says it evaluates asserted and unasserted matters on a regular basis in making that determination. [META FY2024, Item 7, META_FY2024_2024-12-31:337] [META FY2024, Item 8, META_FY2024_2024-12-31:479] | supported | The cited text expressly says it evaluates asserted and unasserted matters on a regular basis. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 2.

**Generated answer**

> Meta Platforms, Inc. stated that it accrues a liability for legal and regulatory contingencies when it believes that a loss has been incurred, the loss is probable, and the amount can be reasonably estimated. [META FY2024, Item 7, META_FY2024_2024-12-31:337] [META FY2024, Item 8, META_FY2024_2024-12-31:479]
>
> The company applies this approach to legal proceedings, claims, and regulatory, tax, or government inquiries and investigations that arise in the ordinary course of business. [META FY2024, Item 7, META_FY2024_2024-12-31:337] [META FY2024, Item 8, META_FY2024_2024-12-31:479]
>
> Meta also stated that such losses are recorded as general and administrative expenses on its consolidated statements of income. [META FY2024, Item 8, META_FY2024_2024-12-31:479]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-META-2024` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2024,2024-12-31,164501000000,62360000000,69380000000,276054000… |
| 2 | `META_FY2024_2024-12-31:268` | Item 3 |  |  | Over the last several years, the number and potential significance of the litigation and investigations involving the company have increased, and there can be no assurance that this trend will not continue. For example, … |
| 3 | `META_FY2024_2024-12-31:337` | Item 7 › Loss Contingencies | ✓ | #1 | We are involved in legal proceedings, claims, and regulatory, tax or government inquiries and investigations that arise in the ordinary course of business. Certain of these matters include speculative claims for substant… |
| 4 | `META_FY2024_2024-12-31:479` | Item 8 › Loss Contingencies | ✓ | #1 | We are involved in legal proceedings, claims, and regulatory, tax or government inquiries and investigations that arise in the ordinary course of business. Certain of these matters include speculative claims for substant… |
| 5 | `META_FY2024_2024-12-31:544` | Item 8 › Note 11. Accrued Expenses and Other Current Liabilities |  |  | _________________________ (1)Includes accruals for estimated fines, settlements, or other losses in connection with legal and related matters, as well as other legal fees. For further information, see Legal and Related M… |
| 6 | `META_FY2024_2024-12-31:412` | Item 8 › Critical Audit Matters |  | #1 | \| \| Loss Contingencies \| \|---\|---\| \| Description of the Matter \| As described in Note 12 to the consolidated financial statements, the Company is party to various legal proceedings, claims, and regulatory or government i… |
| 7 | `META_FY2024_2024-12-31:561` | Item 8 › Legal and Related Matters |  |  | IDPC are subject to review by other European privacy regulators as part of the GDPR's cooperation and consistency mechanisms, which may lead to significant changes in the final outcome of such investigations. As a result… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `META_FY2024_2024-12-31:337`** (cited, gold #1)

````text
Item 7.Management's Discussion and Analysis of Financial Condition and Results of Operations > Loss Contingencies
We are involved in legal proceedings, claims, and regulatory, tax or government inquiries and investigations that arise in the ordinary course of business. Certain of these matters include speculative claims for substantial or indeterminate amounts of damages. Additionally, we are required to comply with various legal and regulatory obligations around the world, and we regularly become subject to new laws and regulations in the jurisdictions in which we operate. The requirements for complying with these obligations may be uncertain and subject to interpretation and enforcement by regulatory and other authorities, and any failure to comply with such obligations could eventually lead to asserted legal or regulatory action. With respect to these matters, asserted and unasserted, we evaluate the associated developments on a regular basis and accrue a liability when we believe that it is both probable that a loss has been incurred and the amount can be reasonably estimated.
````

**#4 `META_FY2024_2024-12-31:479`** (cited, gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Loss Contingencies
We are involved in legal proceedings, claims, and regulatory, tax or government inquiries and investigations that arise in the ordinary course of business. Certain of these matters include speculative claims for substantial or indeterminate amounts of damages. Additionally, we are required to comply with various legal and regulatory obligations around the world, and we regularly become subject to new laws and regulations in the jurisdictions in which we operate. The requirements for complying with these obligations may be uncertain and subject to interpretation and enforcement by regulatory and other authorities, and any failure to comply with such obligations could eventually lead to asserted legal or regulatory action. With respect to these matters, asserted and unasserted, we evaluate the associated developments on a regular basis and accrue a liability when we believe that it is both probable that a loss has been incurred and the amount can be reasonably estimated. We record such losses as general and administrative expenses on our consolidated statements of income.
````

**#6 `META_FY2024_2024-12-31:412`** (gold #1)

````text
Item 8.Financial Statements and Supplementary Data > Critical Audit Matters (table)
|  | Loss Contingencies |
|---|---|
| Description of the Matter | As described in Note 12 to the consolidated financial statements, the Company is party to various legal proceedings, claims, and regulatory or government inquiries and investigations. The Company accrues a liability when it believes a loss is probable and the amount can be reasonably estimated. In addition, the Company believes it is reasonably possible that it will incur a loss in some of these cases, actions or inquiries described above. When applicable, the Company discloses an estimate of the amount of loss or range of possible loss that may be incurred. However, for certain other matters, the Company discloses that the amount of such losses or a range of possible losses cannot be reasonably estimated at this time. Auditing the Company's accounting for, and disclosure of these loss contingencies was especially challenging due to the significant judgment required to evaluate management's assessments of the likelihood of a loss, and their estimate of the potential amount or range of such losses. |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 7'), ('META', 'Item 8')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 3, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta Platforms, Inc. stated that it accrues a liability for legal and regulatory contingencies when it believes that a loss has been incurred, the loss is probable, and the amount can be reasonably estimated. [META FY2024, Item 7, META_FY2024_2024-12-31:337] [META FY2024, Item 8, META_FY2024_2024-12-31:479] | supported | The cited text states Meta accrues a liability when a loss has been incurred, is probable, and can be reasonably estimated. |
| The company applies this approach to legal proceedings, claims, and regulatory, tax, or government inquiries and investigations that arise in the ordinary course of business. [META FY2024, Item 7, META_FY2024_2024-12-31:337] [META FY2024, Item 8, META_FY2024_2024-12-31:479] | supported | The evidence says this accrual approach applies to legal proceedings, claims, and regulatory, tax or government inquiries and investigations arising in the ordinary course of business. |
| Meta also stated that such losses are recorded as general and administrative expenses on its consolidated statements of income. [META FY2024, Item 8, META_FY2024_2024-12-31:479] | supported | The cited evidence explicitly says such losses are recorded as general and administrative expenses on the consolidated statements of income. |

</details>
