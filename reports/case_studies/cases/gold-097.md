# gold-097: Cross-company text

[← all cases](../README.md) · company: Tesla, Inc.; Apple Inc. (TSLA, AAPL) · fiscal year: 2020 · recipe `cross_company_text` · hop `multi` · answer type `qualitative` · scope `cross_company` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> How do Tesla's and Apple's fiscal year 2020 10-Ks describe the terms of their leases and the options to extend or renew them?

**Gold answer**

> Apple says its leases typically have original terms not exceeding 10 years and generally contain multi-year renewal options, some of which are reasonably certain of exercise. Tesla says its leases often include options to extend the lease term for up to 10 years; it does not state a typical original lease term.

**Key points** (RQ3 keypoint_recall targets)

1. Apple's leases typically have original terms not exceeding 10 years.
2. Apple's leases generally contain multi-year renewal options, some reasonably certain of exercise.
3. Tesla's leases often include options to extend the lease term for up to 10 years.

**Gold evidence**

1. `TSLA_FY2020_2020-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Note 13 – Leases · text

   > Our leases, where we are the lessee, often include options to extend the lease term for up to 10 years.

2. `AAPL_FY2020_2020-09-26` · Item 8. Financial Statements and Supplementary Data › Note 12 – Leases · text

   > These leases typically have original terms not exceeding 10 years and generally contain multi-year renewal options, some of which are reasonably certain of exercise.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 11 | 13 |
| recall@5 | 0.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 0.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 0 | 1 | 1 | 1 |
| average precision (lexical) | 0.00 | 0.50 | 0.62 | 0.64 |
| gold evidence first rank | #1: –, #2: – | #1: 2, #2: 2 | #1: 1, #2: 1 | #1: 1, #2: 1 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | 0.67 | 1.00 | 1.00 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 1.00 | 1.00 | 0.67 | 0.67 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 0.80 | 0.80 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 2 | 3 |
| tokens | 1490 | 1244 | 11730 | 16485 |
| cost (USD) | 0.0003 | 0.0003 | 0.0440 | 0.0633 |
| latency (s) | 3.5 | 7.2 | 20.9 | 28.7 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 2.

**Generated answer**

> Tesla’s FY2020 10-K context provided here includes lease term information, but it does **not** describe Tesla’s options to extend or renew leases. Specifically, Tesla reports weighted-average remaining lease terms of **6.2 years for operating leases** and **4.9 years for finance leases** as of December 31, 2020 [7]. It also provides the maturity schedule for lease liabilities through 2025 and thereafter [6].
>
> However:
> - **Tesla’s specific description of extension or renewal options is not in the provided context.**
> - **Apple’s FY2020 10-K is not included in the provided context at all.**
>
> So, based on the provided context, only Tesla’s lease term lengths can be identified, not the extend/renew option language [6][7].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2020_2020-12-31:355` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | Vehicle Sales to Leasing Partners with a Resale Value Guarantee and a Buyback Option |
| 2 | `TSLA_FY2020_2020-12-31:457` | Item 8 › Note 12 – Debt |  |  | The following is a summary of our debt and finance leases as of December 31, 2020 (in millions): |
| 3 | `TSLA_FY2020_2020-12-31:461` | Item 8 › Note 12 – Debt |  |  | The following is a summary of our debt and finance leases as of December 31, 2019 (in millions): |
| 4 | `TSLA_FY2020_2020-12-31:514` | Item 8 › Note 13 – Leases |  |  | \| \| December 31, 2020 \| December 31, 2019 \| \|---\|---\|---\| \| Operating leases: \| \| \| \| Operating lease right-of-use assets \| $1,558 \| $1,218 \| \| Accrued liabilities and other \| $286 \| $228 \| \| Other long-term liabilities … |
| 5 | `TSLA_FY2020_2020-12-31:521` | Item 8 › Note 13 – Leases |  |  | As of December 31, 2020, the maturities of our operating and finance lease liabilities (excluding short-term leases) are as follows (in millions): |
| 6 | `TSLA_FY2020_2020-12-31:522` | Item 8 › Note 13 – Leases | ✓ |  | \| \| Operating \| Finance \| \|---\|---\|---\| \| \| Leases \| Leases \| \| 2021 \| $366 \| $462 \| \| 2022 \| 327 \| 446 \| \| 2023 \| 279 \| 412 \| \| 2024 \| 245 \| 299 \| \| 2025 \| 204 \| 9 \| \| Thereafter \| 425 \| 7 \| \| Total minimum lease paymen… |
| 7 | `TSLA_FY2020_2020-12-31:518` | Item 8 › Note 13 – Leases | ✓ |  | \| \| December 31, 2020 \| December 31, 2019 \| \|---\|---\|---\| \| Weighted-average remaining lease term: \| \| \| \| Operating leases \| 6.2 years \| 6.2 years \| \| Finance leases \| 4.9 years \| 3.9 years \| \| Weighted-average discount… |
| 8 | `TSLA_FY2020_2020-12-31:519` | Item 8 › Note 13 – Leases |  |  | Supplemental cash flow information related to leases where we are the lessee is as follows (in millions): |
| 9 | `TSLA_FY2020_2020-12-31:516` | Item 8 › Note 13 – Leases |  |  | \| \| Year Ended \| \| \|---\|---\|---\| \| \| December 31, 2020 \| December 31, 2019 \| \| Operating lease expense: \| \| \| \| Operating lease expense (1) \| $451 \| $426 \| \| Finance lease expense: \| \| \| \| Amortization of leased assets \|… |
| 10 | `TSLA_FY2020_2020-12-31:455` | Item 8 › Note 10 – Other Long-Term Liabilities |  |  | \| \| December 31, \| December 31, \| \|---\|---\|---\| \| \| 2020 \| 2019 \| \| Operating lease liabilities \| $1,254 \| $956 \| \| Accrued warranty reserve \| 989 \| 745 \| \| Sales return reserve \| 500 \| 545 \| \| Deferred tax liability \| 1… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#6 `TSLA_FY2020_2020-12-31:522`** (cited)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 13 – Leases (table)
|  | Operating | Finance |
|---|---|---|
|  | Leases | Leases |
| 2021 | $366 | $462 |
| 2022 | 327 | 446 |
| 2023 | 279 | 412 |
| 2024 | 245 | 299 |
| 2025 | 204 | 9 |
| Thereafter | 425 | 7 |
| Total minimum lease payments | 1,846 | 1,635 |
| Less: Interest | 306 | 167 |
| Present value of lease obligations | 1,540 | 1,468 |
| Less: Current portion | 286 | 374 |
| Long-term portion of lease obligations | $1,254 | $1,094 |
````

**#7 `TSLA_FY2020_2020-12-31:518`** (cited)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 13 – Leases (table)
|  | December 31, 2020 | December 31, 2019 |
|---|---|---|
| Weighted-average remaining lease term: |  |  |
| Operating leases | 6.2 years | 6.2 years |
| Finance leases | 4.9 years | 3.9 years |
| Weighted-average discount rate: |  |  |
| Operating leases | 5.8% | 6.5% |
| Finance leases | 6.5% | 6.5% |
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Tesla states that its short-term leases are those with terms of 12 months or less at lease inception and without purchase options or renewal terms reasonably certain to be exercised. For its other leases, Tesla says lease liabilities are based on the present value of lease payments over the lease term, and that its leases often include options to extend the lease term for up to 10 years, as well as some options to terminate early. Tesla includes extension or termination options in the lease term when it is reasonably certain those options will be exercised [2].
>
> Apple’s FY2020 10-K, in the provided context, mentions fixed cash payments related to operating leases and non-cash activities involving ROU assets and lease liabilities, but it does not describe lease terms or options to extend or renew them [1].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2020_2020-09-26:316` | Item 8 › Note 12 – Leases | ✓ |  | For 2020, the Company made $1.5 billion of fixed cash payments related to operating leases. Non-cash activities involving ROU assets obtained in exchange for lease liabilities were $10.5 billion for 2020, including the i… |
| 2 | `TSLA_FY2020_2020-12-31:512` | Item 8 › Note 13 – Leases | ✓ | #1, #2 | We have elected not to present short-term leases on the consolidated balance sheet as these leases have a lease term of 12 months or less at lease inception and do not contain purchase options or renewal terms that we ar… |
| 3 | `AAPL_FY2020_2020-09-26:29` | Item 1 › Intellectual Property |  |  | In addition to Company-owned intellectual property, many of the Company’s products and services are designed to include intellectual property owned by third parties. It may be necessary in the future to seek or renew lic… |
| 4 | `AAPL_FY2020_2020-09-26:185` | Item 8 › Basis of Presentation and Preparation |  |  | The consolidated financial statements include the accounts of Apple Inc. and its wholly owned subsidiaries (collectively “Apple” or the “Company”). Intercompany accounts and transactions have been eliminated. In the opin… |
| 5 | `TSLA_FY2020_2020-12-31:285` | Item 7 › Contractual Obligations |  |  | We offer resale value guarantees or similar buyback terms to certain customers who purchase and finance their vehicles through one of our specified commercial banking partners and certain leasing partners (refer to Autom… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2020_2020-09-26:316`** (cited)

````text
Item 8. Financial Statements and Supplementary Data > Note 12 – Leases
For 2020, the Company made $1.5 billion of fixed cash payments related to operating leases. Non-cash activities involving ROU assets obtained in exchange for lease liabilities were $10.5 billion for 2020, including the impact of adopting the new leases standard in the first quarter of 2020. Apple Inc. | 2020 Form 10-K | 56 The following table shows ROU assets and lease liabilities, and the associated financial statement line items, as of September 26, 2020 (in millions):
````

**#2 `TSLA_FY2020_2020-12-31:512`** (cited, gold #1, gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 13 – Leases
We have elected not to present short-term leases on the consolidated balance sheet as these leases have a lease term of 12 months or less at lease inception and do not contain purchase options or renewal terms that we are reasonably certain to exercise. All other lease assets and lease liabilities are recognized based on the present value of lease payments over the lease term at commencement date. Because most of our leases do not provide an implicit rate of return, we used our incremental borrowing rate based on the information available at lease commencement date in determining the present value of lease payments. Our leases, where we are the lessee, often include options to extend the lease term for up to 10 years. Some of our leases also include options to terminate the lease prior to the end of the agreed upon lease term. For purposes of calculating lease liabilities, lease terms include options to extend or terminate the lease when it is reasonably certain that we will exercise such options.
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 8'), ('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 11, cited: 5.

**Generated answer**

> Tesla stated that its leases, where it is the lessee, often include options to extend the lease term for up to 10 years, and some leases also include options to terminate the lease prior to the end of the agreed upon lease term. [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:512]
>
> Tesla also stated that, for purposes of calculating lease liabilities, lease terms include options to extend or terminate the lease when it is reasonably certain that Tesla will exercise such options. [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:512]
>
> Tesla disclosed in its automotive leasing program that the end customer can extend the lease for a period of up to 6 months. [TSLA FY2020, Item 7, TSLA_FY2020_2020-12-31:210] [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:358]
>
> Tesla further disclosed that qualifying customers under certain direct leasing programs in Asia and Europe are permitted to lease a vehicle directly for up to 48 months, and related loan arrangements can have terms for up to 72 months. [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:360]
>
> Apple stated that it has lease arrangements for certain equipment and facilities, including retail, corporate, manufacturing and data center space. [AAPL FY2020, Item 8, AAPL_FY2020_2020-09-26:315]
>
> Apple said these leases typically have original terms not exceeding 10 years and generally contain multi-year renewal options, some of which are reasonably certain of exercise. [AAPL FY2020, Item 8, AAPL_FY2020_2020-09-26:315]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2020_2020-12-31:512` | Item 8 › Note 13 – Leases | ✓ | #1, #2 | We have elected not to present short-term leases on the consolidated balance sheet as these leases have a lease term of 12 months or less at lease inception and do not contain purchase options or renewal terms that we ar… |
| 2 | `TSLA_FY2020_2020-12-31:373` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | We adopted ASC 842, Leases, as of January 1, 2019 using the cumulative effect adjustment approach (“adoption of the new lease standard”). In addition, we elected the package of practical expedients permitted under the tr… |
| 3 | `TSLA_FY2020_2020-12-31:210` | Item 7 › Critical Accounting Policies and Estimates | ✓ |  | At the end of the lease term, we settle our liability in cash by either purchasing the vehicle from the leasing partner for the buyback option amount or paying a shortfall to the option amount the leasing partner may rea… |
| 4 | `TSLA_FY2020_2020-12-31:358` | Item 8 › Note 2 – Summary of Significant Accounting Policies | ✓ |  | At the end of the lease term, we settle our liability in cash by either purchasing the vehicle from the leasing partner for the buyback option amount or paying a shortfall to the option amount the leasing partner may rea… |
| 5 | `TSLA_FY2020_2020-12-31:500` | Item 8 › Warehouse Agreements |  |  | In August 2016, our subsidiaries entered into a loan and security agreement (as amended from time to time, the “2016 Warehouse Agreement”) for borrowings secured by the future cash flows arising from certain leases and t… |
| 6 | `TSLA_FY2020_2020-12-31:360` | Item 8 › Note 2 – Summary of Significant Accounting Policies | ✓ |  | We have outstanding direct leases and vehicles financed by us under loan arrangements accounted for as sales-type leases under ASC 842 in certain countries in Asia and Europe, which we introduced in volume during the thi… |
| 7 | `AAPL_FY2020_2020-09-26:317` | Item 8 › Note 12 – Leases |  |  | \| Lease-Related Assets and Liabilities \| Financial Statement Line Items \| 2020 \| \|---\|---\|---\| \| Right-of-use assets: \| \| \| \| Operating leases \| Other non-current assets \| $8,570 \| \| Finance leases \| Property, plant and … |
| 8 | `AAPL_FY2020_2020-09-26:315` | Item 8 › Note 12 – Leases | ✓ | #2 | The Company has lease arrangements for certain equipment and facilities, including retail, corporate, manufacturing and data center space. These leases typically have original terms not exceeding 10 years and generally c… |
| 9 | `AAPL_FY2020_2020-09-26:187` | Item 8 › Recently Adopted Accounting Pronouncements |  |  | Leases At the beginning of the first quarter of 2020, the Company adopted the Financial Accounting Standards Board’s (the “FASB”) Accounting Standards Update (“ASU”) No. 2016-02, Leases (Topic 842) (“ASU 2016-02”), and a… |
| 10 | `TSLA_FY2020_2020-12-31:513` | Item 8 › Note 13 – Leases |  |  | Lease expense for operating leases is recognized on a straight-line basis over the lease term as cost of revenues or operating expenses depending on the nature of the leased asset. Certain operating leases provide for an… |
| 11 | `AAPL_FY2020_2020-09-26:316` | Item 8 › Note 12 – Leases |  |  | For 2020, the Company made $1.5 billion of fixed cash payments related to operating leases. Non-cash activities involving ROU assets obtained in exchange for lease liabilities were $10.5 billion for 2020, including the i… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2020_2020-12-31:512`** (cited, gold #1, gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 13 – Leases
We have elected not to present short-term leases on the consolidated balance sheet as these leases have a lease term of 12 months or less at lease inception and do not contain purchase options or renewal terms that we are reasonably certain to exercise. All other lease assets and lease liabilities are recognized based on the present value of lease payments over the lease term at commencement date. Because most of our leases do not provide an implicit rate of return, we used our incremental borrowing rate based on the information available at lease commencement date in determining the present value of lease payments. Our leases, where we are the lessee, often include options to extend the lease term for up to 10 years. Some of our leases also include options to terminate the lease prior to the end of the agreed upon lease term. For purposes of calculating lease liabilities, lease terms include options to extend or terminate the lease when it is reasonably certain that we will exercise such options.
````

**#3 `TSLA_FY2020_2020-12-31:210`** (cited)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Critical Accounting Policies and Estimates
At the end of the lease term, we settle our liability in cash by either purchasing the vehicle from the leasing partner for the buyback option amount or paying a shortfall to the option amount the leasing partner may realize on the sale of the vehicle. Any remaining balances within deferred revenue and resale value guarantee will be settled to automotive leasing revenue. The end customer can extend the lease for a period of up to 6 months. In cases where the leasing partner retains ownership of the vehicle after the end of our option period, we expense the net value of the leased vehicle to cost of automotive leasing revenue. Direct Sales-Type Leasing Program
````

**#4 `TSLA_FY2020_2020-12-31:358`** (cited)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 2 – Summary of Significant Accounting Policies
At the end of the lease term, we settle our liability in cash by either purchasing the vehicle from the leasing partner for the buyback option amount or paying a shortfall to the option amount the leasing partner may realize on the sale of the vehicle. Any remaining balances within deferred revenue and resale value guarantee will be settled to automotive leasing revenue. The end customer can extend the lease for a period of up to 6 months. In cases where the leasing partner retains ownership of the vehicle after the end of our option period, we expense the net value of the leased vehicle to cost of automotive leasing revenue. The maximum amount we could be required to pay under this program, should we decide to repurchase all vehicles, was $42 million and $214 million as of December 31, 2020 and 2019, respectively, including $23 million within a 12-month period from December 31, 2020. As of December 31, 2020 and 2019, we had $42 million and $238 million, respectively, of such borrowings recorded in accrued liabilities and other and other long-term liabilities and $11 million and $29 million, respectively, recorded in deferred revenue liability. For the years ended December
````

**#6 `TSLA_FY2020_2020-12-31:360`** (cited)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 2 – Summary of Significant Accounting Policies
We have outstanding direct leases and vehicles financed by us under loan arrangements accounted for as sales-type leases under ASC 842 in certain countries in Asia and Europe, which we introduced in volume during the third quarter of 2020. Depending on the specific program, customers may or may not have a right to return the vehicle to us during or at the end of the lease term. If the customer does not have a right to return, the customer will take title to the vehicle at the end of the lease term after making all contractual payments. Under the programs for which there is a right to return, the purchase option is reasonably certain to be exercised by the lessee and we therefore expect the customer to take title to the vehicle at the end of the lease term after making all contractual payments. Qualifying customers are permitted to lease a vehicle directly under these programs for up to 48 months. Our loan arrangements under these programs can have terms for up to 72 months. We recognize all revenue and costs associated with the sales-type lease as automotive leasing revenue and automotive leasing cost of revenue, respectively, upon delivery of
````

**#8 `AAPL_FY2020_2020-09-26:315`** (cited, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Note 12 – Leases
The Company has lease arrangements for certain equipment and facilities, including retail, corporate, manufacturing and data center space. These leases typically have original terms not exceeding 10 years and generally contain multi-year renewal options, some of which are reasonably certain of exercise. The Company’s lease arrangements may contain both lease and non-lease components. The Company has elected to combine and account for lease and non-lease components as a single lease component for leases of retail, corporate, and data center facilities. Payments under the Company’s lease arrangements may be fixed or variable, and variable lease payments are primarily based on purchases of output of the underlying leased assets. Lease costs associated with fixed payments on the Company’s operating leases were $1.5 billion for 2020. Lease costs associated with variable payments on the Company’s leases were $9.3 billion for 2020. Rent expense for operating leases, as previously reported under former lease accounting standards, was $1.3 billion and $1.2 billion in 2019 and 2018, respectively.
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8'), ('TSLA', 'Item 7'), ('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 6, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Tesla stated that its leases, where it is the lessee, often include options to extend the lease term for up to 10 years, and some leases also include options to terminate the lease prior to the end of the agreed upon lease term. [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:512] | supported | The evidence states Tesla’s lessee leases often include extension options up to 10 years and some include early termination options. |
| Tesla also stated that, for purposes of calculating lease liabilities, lease terms include options to extend or terminate the lease when it is reasonably certain that Tesla will exercise such options. [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:512] | supported | The evidence explicitly says lease terms include extension or termination options when Tesla is reasonably certain to exercise them. |
| Tesla disclosed in its automotive leasing program that the end customer can extend the lease for a period of up to 6 months. [TSLA FY2020, Item 7, TSLA_FY2020_2020-12-31:210] [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:358] | supported | Both cited passages explicitly state the end customer can extend the lease for up to 6 months. |
| Tesla further disclosed that qualifying customers under certain direct leasing programs in Asia and Europe are permitted to lease a vehicle directly for up to 48 months, and related loan arrangements can have terms for up to 72 months. [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:360] | supported | The evidence states qualifying customers may lease directly for up to 48 months and related loan arrangements can have terms up to 72 months. |
| Apple stated that it has lease arrangements for certain equipment and facilities, including retail, corporate, manufacturing and data center space. [AAPL FY2020, Item 8, AAPL_FY2020_2020-09-26:315] | supported | The evidence explicitly says Apple has lease arrangements for certain equipment and facilities including retail, corporate, manufacturing, and data center space. |
| Apple said these leases typically have original terms not exceeding 10 years and generally contain multi-year renewal options, some of which are reasonably certain of exercise. [AAPL FY2020, Item 8, AAPL_FY2020_2020-09-26:315] | supported | The evidence exactly states these leases typically have original terms not exceeding 10 years and generally contain multi-year renewal options, some reasonably certain of exercise. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 13, cited: 6.

**Generated answer**

> Tesla states that, as lessee, its leases often include options to extend the lease term for up to 10 years, and some leases also include options to terminate the lease before the end of the agreed term. [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:512]  
>
> Tesla also states that, for purposes of calculating lease liabilities, lease terms include options to extend or terminate when it is reasonably certain that Tesla will exercise those options. [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:512]  
>
> Tesla says it elected not to present short-term leases on the consolidated balance sheet when those leases have a lease term of 12 months or less at lease inception and do not contain purchase options or renewal terms that Tesla is reasonably certain to exercise. [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:512]  
>
> For Tesla’s customer-facing leasing programs, the end customer can extend the lease for a period of up to 6 months under the resale value guarantee program. [TSLA FY2020, Item 7, TSLA_FY2020_2020-12-31:210] [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:358]  
>
> Tesla also discloses direct leasing programs in certain countries in Asia and Europe under which qualifying customers are permitted to lease a vehicle directly for up to 48 months, and related loan arrangements can have terms for up to 72 months. [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:360] [TSLA FY2020, Item 7, TSLA_FY2020_2020-12-31:211]  
>
> Apple states that it has lease arrangements for certain equipment and facilities, including retail, corporate, manufacturing and data center space, and that these leases typically have original terms not exceeding 10 years. [AAPL FY2020, Item 8, AAPL_FY2020_2020-09-26:315]  
>
> Apple further states that its leases generally contain multi-year renewal options, some of which are reasonably certain of exercise. [AAPL FY2020, Item 8, AAPL_FY2020_2020-09-26:315]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2020_2020-12-31:512` | Item 8 › Note 13 – Leases | ✓ | #1, #2 | We have elected not to present short-term leases on the consolidated balance sheet as these leases have a lease term of 12 months or less at lease inception and do not contain purchase options or renewal terms that we ar… |
| 2 | `TSLA_FY2020_2020-12-31:373` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | We adopted ASC 842, Leases, as of January 1, 2019 using the cumulative effect adjustment approach (“adoption of the new lease standard”). In addition, we elected the package of practical expedients permitted under the tr… |
| 3 | `TSLA_FY2020_2020-12-31:210` | Item 7 › Critical Accounting Policies and Estimates | ✓ |  | At the end of the lease term, we settle our liability in cash by either purchasing the vehicle from the leasing partner for the buyback option amount or paying a shortfall to the option amount the leasing partner may rea… |
| 4 | `TSLA_FY2020_2020-12-31:358` | Item 8 › Note 2 – Summary of Significant Accounting Policies | ✓ |  | At the end of the lease term, we settle our liability in cash by either purchasing the vehicle from the leasing partner for the buyback option amount or paying a shortfall to the option amount the leasing partner may rea… |
| 5 | `TSLA_FY2020_2020-12-31:500` | Item 8 › Warehouse Agreements |  |  | In August 2016, our subsidiaries entered into a loan and security agreement (as amended from time to time, the “2016 Warehouse Agreement”) for borrowings secured by the future cash flows arising from certain leases and t… |
| 6 | `TSLA_FY2020_2020-12-31:360` | Item 8 › Note 2 – Summary of Significant Accounting Policies | ✓ |  | We have outstanding direct leases and vehicles financed by us under loan arrangements accounted for as sales-type leases under ASC 842 in certain countries in Asia and Europe, which we introduced in volume during the thi… |
| 7 | `AAPL_FY2020_2020-09-26:315` | Item 8 › Note 12 – Leases | ✓ | #2 | The Company has lease arrangements for certain equipment and facilities, including retail, corporate, manufacturing and data center space. These leases typically have original terms not exceeding 10 years and generally c… |
| 8 | `AAPL_FY2020_2020-09-26:319` | Item 8 › Note 12 – Leases |  |  | \| \| Operating Leases \| Finance Leases \| Total \| \|---\|---\|---\|---\| \| 2021 \| $1,493 \| $43 \| $1,536 \| \| 2022 \| 1,461 \| 43 \| 1,504 \| \| 2023 \| 1,317 \| 54 \| 1,371 \| \| 2024 \| 1,068 \| 30 \| 1,098 \| \| 2025 \| 960 \| 25 \| 985 \| \| The… |
| 9 | `AAPL_FY2020_2020-09-26:187` | Item 8 › Recently Adopted Accounting Pronouncements |  |  | Leases At the beginning of the first quarter of 2020, the Company adopted the Financial Accounting Standards Board’s (the “FASB”) Accounting Standards Update (“ASU”) No. 2016-02, Leases (Topic 842) (“ASU 2016-02”), and a… |
| 10 | `AAPL_FY2020_2020-09-26:317` | Item 8 › Note 12 – Leases |  |  | \| Lease-Related Assets and Liabilities \| Financial Statement Line Items \| 2020 \| \|---\|---\|---\| \| Right-of-use assets: \| \| \| \| Operating leases \| Other non-current assets \| $8,570 \| \| Finance leases \| Property, plant and … |
| 11 | `AAPL_FY2020_2020-09-26:316` | Item 8 › Note 12 – Leases |  |  | For 2020, the Company made $1.5 billion of fixed cash payments related to operating leases. Non-cash activities involving ROU assets obtained in exchange for lease liabilities were $10.5 billion for 2020, including the i… |
| 12 | `TSLA_FY2020_2020-12-31:518` | Item 8 › Note 13 – Leases |  |  | \| \| December 31, 2020 \| December 31, 2019 \| \|---\|---\|---\| \| Weighted-average remaining lease term: \| \| \| \| Operating leases \| 6.2 years \| 6.2 years \| \| Finance leases \| 4.9 years \| 3.9 years \| \| Weighted-average discount… |
| 13 | `TSLA_FY2020_2020-12-31:211` | Item 7 › Critical Accounting Policies and Estimates | ✓ |  | We have outstanding direct leases and vehicles financed by us under loan arrangements accounted for as sales-type leases under ASC 842 in certain countries in Asia and Europe, which we introduced in volume during the thi… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2020_2020-12-31:512`** (cited, gold #1, gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 13 – Leases
We have elected not to present short-term leases on the consolidated balance sheet as these leases have a lease term of 12 months or less at lease inception and do not contain purchase options or renewal terms that we are reasonably certain to exercise. All other lease assets and lease liabilities are recognized based on the present value of lease payments over the lease term at commencement date. Because most of our leases do not provide an implicit rate of return, we used our incremental borrowing rate based on the information available at lease commencement date in determining the present value of lease payments. Our leases, where we are the lessee, often include options to extend the lease term for up to 10 years. Some of our leases also include options to terminate the lease prior to the end of the agreed upon lease term. For purposes of calculating lease liabilities, lease terms include options to extend or terminate the lease when it is reasonably certain that we will exercise such options.
````

**#3 `TSLA_FY2020_2020-12-31:210`** (cited)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Critical Accounting Policies and Estimates
At the end of the lease term, we settle our liability in cash by either purchasing the vehicle from the leasing partner for the buyback option amount or paying a shortfall to the option amount the leasing partner may realize on the sale of the vehicle. Any remaining balances within deferred revenue and resale value guarantee will be settled to automotive leasing revenue. The end customer can extend the lease for a period of up to 6 months. In cases where the leasing partner retains ownership of the vehicle after the end of our option period, we expense the net value of the leased vehicle to cost of automotive leasing revenue. Direct Sales-Type Leasing Program
````

**#4 `TSLA_FY2020_2020-12-31:358`** (cited)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 2 – Summary of Significant Accounting Policies
At the end of the lease term, we settle our liability in cash by either purchasing the vehicle from the leasing partner for the buyback option amount or paying a shortfall to the option amount the leasing partner may realize on the sale of the vehicle. Any remaining balances within deferred revenue and resale value guarantee will be settled to automotive leasing revenue. The end customer can extend the lease for a period of up to 6 months. In cases where the leasing partner retains ownership of the vehicle after the end of our option period, we expense the net value of the leased vehicle to cost of automotive leasing revenue. The maximum amount we could be required to pay under this program, should we decide to repurchase all vehicles, was $42 million and $214 million as of December 31, 2020 and 2019, respectively, including $23 million within a 12-month period from December 31, 2020. As of December 31, 2020 and 2019, we had $42 million and $238 million, respectively, of such borrowings recorded in accrued liabilities and other and other long-term liabilities and $11 million and $29 million, respectively, recorded in deferred revenue liability. For the years ended December
````

**#6 `TSLA_FY2020_2020-12-31:360`** (cited)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 2 – Summary of Significant Accounting Policies
We have outstanding direct leases and vehicles financed by us under loan arrangements accounted for as sales-type leases under ASC 842 in certain countries in Asia and Europe, which we introduced in volume during the third quarter of 2020. Depending on the specific program, customers may or may not have a right to return the vehicle to us during or at the end of the lease term. If the customer does not have a right to return, the customer will take title to the vehicle at the end of the lease term after making all contractual payments. Under the programs for which there is a right to return, the purchase option is reasonably certain to be exercised by the lessee and we therefore expect the customer to take title to the vehicle at the end of the lease term after making all contractual payments. Qualifying customers are permitted to lease a vehicle directly under these programs for up to 48 months. Our loan arrangements under these programs can have terms for up to 72 months. We recognize all revenue and costs associated with the sales-type lease as automotive leasing revenue and automotive leasing cost of revenue, respectively, upon delivery of
````

**#7 `AAPL_FY2020_2020-09-26:315`** (cited, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Note 12 – Leases
The Company has lease arrangements for certain equipment and facilities, including retail, corporate, manufacturing and data center space. These leases typically have original terms not exceeding 10 years and generally contain multi-year renewal options, some of which are reasonably certain of exercise. The Company’s lease arrangements may contain both lease and non-lease components. The Company has elected to combine and account for lease and non-lease components as a single lease component for leases of retail, corporate, and data center facilities. Payments under the Company’s lease arrangements may be fixed or variable, and variable lease payments are primarily based on purchases of output of the underlying leased assets. Lease costs associated with fixed payments on the Company’s operating leases were $1.5 billion for 2020. Lease costs associated with variable payments on the Company’s leases were $9.3 billion for 2020. Rent expense for operating leases, as previously reported under former lease accounting standards, was $1.3 billion and $1.2 billion in 2019 and 2018, respectively.
````

**#13 `TSLA_FY2020_2020-12-31:211`** (cited)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Critical Accounting Policies and Estimates
We have outstanding direct leases and vehicles financed by us under loan arrangements accounted for as sales-type leases under ASC 842 in certain countries in Asia and Europe, which we introduced in volume during the third quarter of 2020. Depending on the specific program, customers may or may not have a right to return the vehicle to us during or at the end of the lease term. If the customer does not have a right to return, the customer will take title to the vehicle at the end of the lease term after making all contractual payments. Under the programs for which there is a right to return, the purchase option is reasonably certain to be exercised by the lessee and we therefore expect the customer to take title to the vehicle at the end of the lease term after making all contractual payments. Qualifying customers are permitted to lease a vehicle directly under these programs for up to 48 months. Our loan arrangements under these programs can have terms for up to 72 months. We recognize all revenue and costs associated with the sales-type lease as automotive leasing revenue and automotive leasing cost of revenue, respectively, upon delivery of
````

</details>

RQ2 citation match (section level): `cited=[('TSLA', 'Item 8'), ('TSLA', 'Item 7'), ('AAPL', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 7, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Tesla states that, as lessee, its leases often include options to extend the lease term for up to 10 years, and some leases also include options to terminate the lease before the end of the agreed term. [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:512] | supported | The evidence states Tesla's lessee leases often include extension options up to 10 years and some include early termination options. |
| Tesla also states that, for purposes of calculating lease liabilities, lease terms include options to extend or terminate when it is reasonably certain that Tesla will exercise those options. [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:512] | supported | The evidence explicitly says lease terms include extension or termination options when Tesla is reasonably certain to exercise them. |
| Tesla says it elected not to present short-term leases on the consolidated balance sheet when those leases have a lease term of 12 months or less at lease inception and do not contain purchase options or renewal terms that Tesla is reasonably certain to exercise. [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:512] | supported | The evidence matches Tesla's election not to present qualifying short-term leases on the balance sheet. |
| For Tesla’s customer-facing leasing programs, the end customer can extend the lease for a period of up to 6 months under the resale value guarantee program. [TSLA FY2020, Item 7, TSLA_FY2020_2020-12-31:210] [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:358] | supported | The cited passages state the end customer can extend the lease up to 6 months in that customer-facing program. |
| Tesla also discloses direct leasing programs in certain countries in Asia and Europe under which qualifying customers are permitted to lease a vehicle directly for up to 48 months, and related loan arrangements can have terms for up to 72 months. [TSLA FY2020, Item 8, TSLA_FY2020_2020-12-31:360] [TSLA FY2020, Item 7, TSLA_FY2020_2020-12-31:211] | supported | The evidence says Tesla has direct leasing programs in certain Asian and European countries with leases up to 48 months and loans up to 72 months. |
| Apple states that it has lease arrangements for certain equipment and facilities, including retail, corporate, manufacturing and data center space, and that these leases typically have original terms not exceeding 10 years. [AAPL FY2020, Item 8, AAPL_FY2020_2020-09-26:315] | supported | Apple's note states it leases certain equipment and facilities including those spaces and that these leases typically have original terms not exceeding 10 years. |
| Apple further states that its leases generally contain multi-year renewal options, some of which are reasonably certain of exercise. [AAPL FY2020, Item 8, AAPL_FY2020_2020-09-26:315] | supported | The evidence explicitly says Apple's leases generally contain multi-year renewal options, some reasonably certain of exercise. |

</details>
