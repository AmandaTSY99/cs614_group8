# gold-092: Cross-company table

[← all cases](../README.md) · company: Tesla, Inc.; Meta Platforms, Inc. (TSLA, META) · fiscal year: 2025 · recipe `cross_company_table` · hop `multi` · answer type `numeric` · scope `cross_company` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> As of the end of fiscal year 2025, by what percentage was Meta Platforms' weighted-average remaining lease term for operating leases longer than Tesla's?

**Gold answer**

> 59.74%

**Program**: `subtract(12.3, 7.7), divide(#0, 7.7), multiply(#1, 100)` → `59.74025974025975`

**Gold numbers** (RQ2 numeric_accuracy targets): 59.74%

**Gold evidence**

1. `TSLA_FY2025_2025-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA › Note 10 – Leases · table

   > Operating leases | 7.7 years | 7.9 years

2. `META_FY2025_2025-12-31` · Item 8.Financial Statements and Supplementary Data › Note 7. Leases · table

   > Operating leases | 12.3 years | 11.5 years

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 12 | 12 |
| recall@5 | 0.50 | 1.00 | 0.50 | 0.50 |
| recall@all | 0.50 | 1.00 | 1.00 | 1.00 |
| complete@all | 0 | 1 | 1 | 1 |
| average precision (lexical) | 1.00 | 1.00 | 0.64 | 0.64 |
| gold evidence first rank | #1: 1, #2: – | #1: 2, #2: 1 | #1: 7, #2: 1 | #1: 7, #2: 1 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✓ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 1.00 | 1.00 | 1.00 |
| citation precision | – | 1.00 | 1.00 | 1.00 |
| citation recall | – | 1.00 | 1.00 | 1.00 |
| citation F1 | – | 1.00 | 1.00 | 1.00 |
| has a citation | 0 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 2 | 2 |
| tokens | 1455 | 1071 | 9024 | 9090 |
| cost (USD) | 0.0002 | 0.0002 | 0.0308 | 0.0317 |
| latency (s) | 1.1 | 6.8 | 12.5 | 13.6 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `TSLA_FY2025_2025-12-31:404` | Item 8 › Note 10 – Leases |  | #1 | \| \| December 31, 2025 \| December 31, 2024 \| \|---\|---\|---\| \| Weighted-average remaining lease term: \| \| \| \| Operating leases \| 7.7 years \| 7.9 years \| \| Finance leases \| 4.3 years \| 4.4 years \| \| Weighted-average discount… |
| 2 | `TSLA_FY2025_2025-12-31:409` | Item 8 › Note 10 – Leases |  |  | As of December 31, 2025, we have excluded from the table above additional operating leases that have not yet commenced with aggregate rent payments of $849 million. These operating leases will commence between fiscal yea… |
| 3 | `TSLA_FY2025_2025-12-31:402` | Item 8 › Note 10 – Leases |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2025 \| 2024 \| 2023 \| \| Operating lease expense: \| \| \| \| \| Operating lease expense (1) \| $1,766 \| $1,500 \| $1,153 \| \| Finance lease expense: \| \| \| \| \| Amortization o… |
| 4 | `TSLA_FY2025_2025-12-31:407` | Item 8 › Note 10 – Leases |  |  | As of December 31, 2025, the maturities of our operating and finance lease liabilities (excluding short-term leases) are as follows (in millions): |
| 5 | `TSLA_FY2025_2025-12-31:400` | Item 8 › Note 10 – Leases |  |  | \| \| December 31, 2025 \| December 31, 2024 \| \|---\|---\|---\| \| Operating leases: \| \| \| \| Operating lease right-of-use assets \| $6,027 \| $5,160 \| \| Accrued liabilities and other \| $954 \| $807 \| \| Other long-term liabilities … |
| 6 | `TSLA_FY2025_2025-12-31:405` | Item 8 › Note 10 – Leases |  |  | Supplemental cash flow information related to leases where we are the lessee is as follows (in millions): |
| 7 | `TSLA_FY2025_2025-12-31:408` | Item 8 › Note 10 – Leases |  |  | \| \| Operating Leases \| Finance Leases \| \|---\|---\|---\| \| 2026 \| $1,241 \| $80 \| \| 2027 \| 1,127 \| 72 \| \| 2028 \| 1,012 \| 27 \| \| 2029 \| 879 \| 22 \| \| 2030 \| 787 \| 22 \| \| Thereafter \| 2,668 \| 23 \| \| Total minimum lease payments… |
| 8 | `TSLA_FY2025_2025-12-31:381` | Item 8 › Note 9 – Debt |  |  | The following is a summary of our debt and finance leases as of December 31, 2025 (in millions): |
| 9 | `TSLA_FY2025_2025-12-31:411` | Item 8 › Operating Lease and Sales-type Lease Receivables |  |  | \| \| Operating Leases \| Sales-type Leases \| \|---\|---\|---\| \| 2026 \| $1,045 \| $144 \| \| 2027 \| 709 \| 83 \| \| 2028 \| 363 \| 27 \| \| 2029 \| 210 \| 5 \| \| 2030 \| 203 \| — \| \| Thereafter \| 1,077 \| — \| \| Gross lease receivables \| $3,60… |
| 10 | `TSLA_FY2025_2025-12-31:384` | Item 8 › Note 9 – Debt |  |  | The following is a summary of our debt and finance leases as of December 31, 2024 (in millions): |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `TSLA_FY2025_2025-12-31:404`** (gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 10 – Leases (table)
|  | December 31, 2025 | December 31, 2024 |
|---|---|---|
| Weighted-average remaining lease term: |  |  |
| Operating leases | 7.7 years | 7.9 years |
| Finance leases | 4.3 years | 4.4 years |
| Weighted-average discount rate: |  |  |
| Operating leases | 5.0% | 5.3% |
| Finance leases | 4.7% | 4.7% |
````

</details>

RQ2 citation match (section level): `no citations`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Meta’s weighted-average remaining lease term for operating leases was 12.3 years, versus Tesla’s 7.7 years [1][2].
>
> Percentage longer = \(\frac{12.3 - 7.7}{7.7} \times 100 \approx 59.7\%\) [1][2].
>
> So, Meta’s operating lease term was approximately **59.7% longer** than Tesla’s [1][2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2025_2025-12-31:516` | Item 8 › Note 7. Leases | ✓ | #2 | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2025 \| 2024 \| \| Weighted-average remaining lease term: \| \| \| \| Finance leases \| 15.1 years \| 13.7 years \| \| Operating leases \| 12.3 years \| 11.5 years \| \| Weighted-average discount … |
| 2 | `TSLA_FY2025_2025-12-31:404` | Item 8 › Note 10 – Leases | ✓ | #1 | \| \| December 31, 2025 \| December 31, 2024 \| \|---\|---\|---\| \| Weighted-average remaining lease term: \| \| \| \| Operating leases \| 7.7 years \| 7.9 years \| \| Finance leases \| 4.3 years \| 4.4 years \| \| Weighted-average discount… |
| 3 | `TSLA_FY2025_2025-12-31:296` | Item 8 › Note 2 – Summary of Significant Accounting Policies |  |  | We have outstanding leases under our direct vehicle operating leasing programs in the U.S., Canada and in certain countries in Europe. Qualifying customers are permitted to lease a vehicle directly from Tesla for up to 4… |
| 4 | `TSLA_FY2025_2025-12-31:409` | Item 8 › Note 10 – Leases |  |  | As of December 31, 2025, we have excluded from the table above additional operating leases that have not yet commenced with aggregate rent payments of $849 million. These operating leases will commence between fiscal yea… |
| 5 | `META_FY2025_2025-12-31:519` | Item 8 › Note 7. Leases |  |  | The table above does not include lease payments that were not fixed at commencement or lease modification. As of December 31, 2025, we have additional operating and finance leases, that have not yet commenced, with total… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2025_2025-12-31:516`** (cited, gold #2)

````text
Item 8.Financial Statements and Supplementary Data > Note 7. Leases (table)
|  | December 31, |  |
|---|---|---|
|  | 2025 | 2024 |
| Weighted-average remaining lease term: |  |  |
| Finance leases | 15.1 years | 13.7 years |
| Operating leases | 12.3 years | 11.5 years |
| Weighted-average discount rate: |  |  |
| Finance leases | 4.1% | 3.6% |
| Operating leases | 4.3% | 3.9% |
````

**#2 `TSLA_FY2025_2025-12-31:404`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 10 – Leases (table)
|  | December 31, 2025 | December 31, 2024 |
|---|---|---|
| Weighted-average remaining lease term: |  |  |
| Operating leases | 7.7 years | 7.9 years |
| Finance leases | 4.3 years | 4.4 years |
| Weighted-average discount rate: |  |  |
| Operating leases | 5.0% | 5.3% |
| Finance leases | 4.7% | 4.7% |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8'), ('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 12, cited: 2.

**Generated answer**

> Meta Platforms' weighted-average remaining lease term for operating leases was 12.3 years as of December 31, 2025, while Tesla's was 7.7 years as of December 31, 2025 [META FY2025, Item 8, META_FY2025_2025-12-31:516] [TSLA FY2025, Item 8, TSLA_FY2025_2025-12-31:404].  
> The percentage by which Meta Platforms' operating lease term was longer than Tesla's was 59.7%, calculated as (12.3 - 7.7) / 7.7 × 100 [META FY2025, Item 8, META_FY2025_2025-12-31:516] [TSLA FY2025, Item 8, TSLA_FY2025_2025-12-31:404].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2025_2025-12-31:516` | Item 8 › Note 7. Leases | ✓ | #2 | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2025 \| 2024 \| \| Weighted-average remaining lease term: \| \| \| \| Finance leases \| 15.1 years \| 13.7 years \| \| Operating leases \| 12.3 years \| 11.5 years \| \| Weighted-average discount … |
| 2 | `META_FY2025_2025-12-31:519` | Item 8 › Note 7. Leases |  |  | The table above does not include lease payments that were not fixed at commencement or lease modification. As of December 31, 2025, we have additional operating and finance leases, that have not yet commenced, with total… |
| 3 | `META_FY2025_2025-12-31:383` | Item 7 › Leases and Contractual Commitments |  |  | Our operating and finance leases include data centers, offices, and certain network infrastructure. In addition to lease liabilities included in our consolidated balance sheets, we have leases that have not yet commenced… |
| 4 | `META_FY2025_2025-12-31:513` | Item 8 › Note 7. Leases |  |  | We have entered into various non-cancelable operating and finance lease agreements mostly for our data centers, offices, and certain network infrastructure. Our leases have original lease periods expiring between 2026 an… |
| 5 | `META_FY2025_2025-12-31:518` | Item 8 › Note 7. Leases |  |  | \| \| Operating Leases \| Finance Leases \| \|---\|---\|---\| \| 2026 \| $3,211 \| $344 \| \| 2027 \| 3,237 \| 97 \| \| 2028 \| 3,057 \| 97 \| \| 2029 \| 2,985 \| 88 \| \| 2030 \| 2,621 \| 86 \| \| Thereafter \| 18,397 \| 792 \| \| Total undiscounted ca… |
| 6 | `META_FY2025_2025-12-31:514` | Item 8 › Note 7. Leases |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2025 \| 2024 \| 2023 \| \| Finance lease cost: \| \| \| \| \| Amortization of right-of-use assets \| $549 \| $387 \| $349 \| \| Interest \| 31 \| 23 \| 20 \| \| Operating lease cost \|… |
| 7 | `TSLA_FY2025_2025-12-31:404` | Item 8 › Note 10 – Leases | ✓ | #1 | \| \| December 31, 2025 \| December 31, 2024 \| \|---\|---\|---\| \| Weighted-average remaining lease term: \| \| \| \| Operating leases \| 7.7 years \| 7.9 years \| \| Finance leases \| 4.3 years \| 4.4 years \| \| Weighted-average discount… |
| 8 | `TSLA_FY2025_2025-12-31:408` | Item 8 › Note 10 – Leases |  |  | \| \| Operating Leases \| Finance Leases \| \|---\|---\|---\| \| 2026 \| $1,241 \| $80 \| \| 2027 \| 1,127 \| 72 \| \| 2028 \| 1,012 \| 27 \| \| 2029 \| 879 \| 22 \| \| 2030 \| 787 \| 22 \| \| Thereafter \| 2,668 \| 23 \| \| Total minimum lease payments… |
| 9 | `TSLA_FY2025_2025-12-31:411` | Item 8 › Operating Lease and Sales-type Lease Receivables |  |  | \| \| Operating Leases \| Sales-type Leases \| \|---\|---\|---\| \| 2026 \| $1,045 \| $144 \| \| 2027 \| 709 \| 83 \| \| 2028 \| 363 \| 27 \| \| 2029 \| 210 \| 5 \| \| 2030 \| 203 \| — \| \| Thereafter \| 1,077 \| — \| \| Gross lease receivables \| $3,60… |
| 10 | `TSLA_FY2025_2025-12-31:400` | Item 8 › Note 10 – Leases |  |  | \| \| December 31, 2025 \| December 31, 2024 \| \|---\|---\|---\| \| Operating leases: \| \| \| \| Operating lease right-of-use assets \| $6,027 \| $5,160 \| \| Accrued liabilities and other \| $954 \| $807 \| \| Other long-term liabilities … |
| 11 | `TSLA_FY2025_2025-12-31:406` | Item 8 › Note 10 – Leases |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2025 \| 2024 \| 2023 \| \| Cash paid for amounts included in the measurement of lease liabilities: \| \| \| \| \| Operating cash outflows from operating leases \| $1,743 \| $1… |
| 12 | `TSLA_FY2025_2025-12-31:409` | Item 8 › Note 10 – Leases |  |  | As of December 31, 2025, we have excluded from the table above additional operating leases that have not yet commenced with aggregate rent payments of $849 million. These operating leases will commence between fiscal yea… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2025_2025-12-31:516`** (cited, gold #2)

````text
Item 8.Financial Statements and Supplementary Data > Note 7. Leases (table)
|  | December 31, |  |
|---|---|---|
|  | 2025 | 2024 |
| Weighted-average remaining lease term: |  |  |
| Finance leases | 15.1 years | 13.7 years |
| Operating leases | 12.3 years | 11.5 years |
| Weighted-average discount rate: |  |  |
| Finance leases | 4.1% | 3.6% |
| Operating leases | 4.3% | 3.9% |
````

**#7 `TSLA_FY2025_2025-12-31:404`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 10 – Leases (table)
|  | December 31, 2025 | December 31, 2024 |
|---|---|---|
| Weighted-average remaining lease term: |  |  |
| Operating leases | 7.7 years | 7.9 years |
| Finance leases | 4.3 years | 4.4 years |
| Weighted-average discount rate: |  |  |
| Operating leases | 5.0% | 5.3% |
| Finance leases | 4.7% | 4.7% |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8'), ('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta Platforms' weighted-average remaining lease term for operating leases was 12.3 years as of December 31, 2025, while Tesla's was 7.7 years as of December 31, 2025 [META FY2025, Item 8, META_FY2025_2025-12-31:516] [TSLA FY2025, Item 8, TSLA_FY2025_2025-12-31:404]. | None |  |
| The percentage by which Meta Platforms' operating lease term was longer than Tesla's was 59.7%, calculated as (12.3 - 7.7) / 7.7 × 100 [META FY2025, Item 8, META_FY2025_2025-12-31:516] [TSLA FY2025, Item 8, TSLA_FY2025_2025-12-31:404]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 12, cited: 2.

**Generated answer**

> Meta Platforms' weighted-average remaining lease term for operating leases was 12.3 years, compared with Tesla's 7.7 years as of December 31, 2025. [META FY2025, Item 8, META_FY2025_2025-12-31:516] [TSLA FY2025, Item 8, TSLA_FY2025_2025-12-31:404]
>
> The percentage by which Meta's term was longer than Tesla's was approximately 59.7%, calculated as (12.3 - 7.7) / 7.7 × 100. [META FY2025, Item 8, META_FY2025_2025-12-31:516] [TSLA FY2025, Item 8, TSLA_FY2025_2025-12-31:404]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2025_2025-12-31:516` | Item 8 › Note 7. Leases | ✓ | #2 | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2025 \| 2024 \| \| Weighted-average remaining lease term: \| \| \| \| Finance leases \| 15.1 years \| 13.7 years \| \| Operating leases \| 12.3 years \| 11.5 years \| \| Weighted-average discount … |
| 2 | `META_FY2025_2025-12-31:519` | Item 8 › Note 7. Leases |  |  | The table above does not include lease payments that were not fixed at commencement or lease modification. As of December 31, 2025, we have additional operating and finance leases, that have not yet commenced, with total… |
| 3 | `META_FY2025_2025-12-31:383` | Item 7 › Leases and Contractual Commitments |  |  | Our operating and finance leases include data centers, offices, and certain network infrastructure. In addition to lease liabilities included in our consolidated balance sheets, we have leases that have not yet commenced… |
| 4 | `META_FY2025_2025-12-31:513` | Item 8 › Note 7. Leases |  |  | We have entered into various non-cancelable operating and finance lease agreements mostly for our data centers, offices, and certain network infrastructure. Our leases have original lease periods expiring between 2026 an… |
| 5 | `META_FY2025_2025-12-31:518` | Item 8 › Note 7. Leases |  |  | \| \| Operating Leases \| Finance Leases \| \|---\|---\|---\| \| 2026 \| $3,211 \| $344 \| \| 2027 \| 3,237 \| 97 \| \| 2028 \| 3,057 \| 97 \| \| 2029 \| 2,985 \| 88 \| \| 2030 \| 2,621 \| 86 \| \| Thereafter \| 18,397 \| 792 \| \| Total undiscounted ca… |
| 6 | `META_FY2025_2025-12-31:514` | Item 8 › Note 7. Leases |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2025 \| 2024 \| 2023 \| \| Finance lease cost: \| \| \| \| \| Amortization of right-of-use assets \| $549 \| $387 \| $349 \| \| Interest \| 31 \| 23 \| 20 \| \| Operating lease cost \|… |
| 7 | `TSLA_FY2025_2025-12-31:404` | Item 8 › Note 10 – Leases | ✓ | #1 | \| \| December 31, 2025 \| December 31, 2024 \| \|---\|---\|---\| \| Weighted-average remaining lease term: \| \| \| \| Operating leases \| 7.7 years \| 7.9 years \| \| Finance leases \| 4.3 years \| 4.4 years \| \| Weighted-average discount… |
| 8 | `TSLA_FY2025_2025-12-31:408` | Item 8 › Note 10 – Leases |  |  | \| \| Operating Leases \| Finance Leases \| \|---\|---\|---\| \| 2026 \| $1,241 \| $80 \| \| 2027 \| 1,127 \| 72 \| \| 2028 \| 1,012 \| 27 \| \| 2029 \| 879 \| 22 \| \| 2030 \| 787 \| 22 \| \| Thereafter \| 2,668 \| 23 \| \| Total minimum lease payments… |
| 9 | `TSLA_FY2025_2025-12-31:411` | Item 8 › Operating Lease and Sales-type Lease Receivables |  |  | \| \| Operating Leases \| Sales-type Leases \| \|---\|---\|---\| \| 2026 \| $1,045 \| $144 \| \| 2027 \| 709 \| 83 \| \| 2028 \| 363 \| 27 \| \| 2029 \| 210 \| 5 \| \| 2030 \| 203 \| — \| \| Thereafter \| 1,077 \| — \| \| Gross lease receivables \| $3,60… |
| 10 | `TSLA_FY2025_2025-12-31:400` | Item 8 › Note 10 – Leases |  |  | \| \| December 31, 2025 \| December 31, 2024 \| \|---\|---\|---\| \| Operating leases: \| \| \| \| Operating lease right-of-use assets \| $6,027 \| $5,160 \| \| Accrued liabilities and other \| $954 \| $807 \| \| Other long-term liabilities … |
| 11 | `TSLA_FY2025_2025-12-31:406` | Item 8 › Note 10 – Leases |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2025 \| 2024 \| 2023 \| \| Cash paid for amounts included in the measurement of lease liabilities: \| \| \| \| \| Operating cash outflows from operating leases \| $1,743 \| $1… |
| 12 | `TSLA_FY2025_2025-12-31:409` | Item 8 › Note 10 – Leases |  |  | As of December 31, 2025, we have excluded from the table above additional operating leases that have not yet commenced with aggregate rent payments of $849 million. These operating leases will commence between fiscal yea… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2025_2025-12-31:516`** (cited, gold #2)

````text
Item 8.Financial Statements and Supplementary Data > Note 7. Leases (table)
|  | December 31, |  |
|---|---|---|
|  | 2025 | 2024 |
| Weighted-average remaining lease term: |  |  |
| Finance leases | 15.1 years | 13.7 years |
| Operating leases | 12.3 years | 11.5 years |
| Weighted-average discount rate: |  |  |
| Finance leases | 4.1% | 3.6% |
| Operating leases | 4.3% | 3.9% |
````

**#7 `TSLA_FY2025_2025-12-31:404`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 10 – Leases (table)
|  | December 31, 2025 | December 31, 2024 |
|---|---|---|
| Weighted-average remaining lease term: |  |  |
| Operating leases | 7.7 years | 7.9 years |
| Finance leases | 4.3 years | 4.4 years |
| Weighted-average discount rate: |  |  |
| Operating leases | 5.0% | 5.3% |
| Finance leases | 4.7% | 4.7% |
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8'), ('TSLA', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta Platforms' weighted-average remaining lease term for operating leases was 12.3 years, compared with Tesla's 7.7 years as of December 31, 2025. [META FY2025, Item 8, META_FY2025_2025-12-31:516] [TSLA FY2025, Item 8, TSLA_FY2025_2025-12-31:404] | None |  |
| The percentage by which Meta's term was longer than Tesla's was approximately 59.7%, calculated as (12.3 - 7.7) / 7.7 × 100. [META FY2025, Item 8, META_FY2025_2025-12-31:516] [TSLA FY2025, Item 8, TSLA_FY2025_2025-12-31:404] | None |  |

</details>
