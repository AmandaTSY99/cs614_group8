# gold-032: Table + text (one filing)

[← all cases](../README.md) · company: MICROSOFT CORP (MSFT) · fiscal year: 2023 · recipe `table_text` · hop `multi` · answer type `mixed` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> For Microsoft's fiscal year 2023, calculate the percentage increase in operating lease cost compared to fiscal year 2022, and identify two specific types of infrastructure components or dependencies mentioned in the 10-K that contribute to the cost and complexity of maintaining the datacenter infrastructure driving these lease expenses.

**Gold answer**

> 16.82%. Microsoft says its datacenters depend on the availability of permitted and buildable land, predictable energy, networking supplies, and servers, including graphics processing units (GPUs) and other components.

**Program**: `subtract(2875, 2461), divide(#0, 2461), multiply(#1, 100)` → `16.822429906542055`

**Gold numbers** (RQ2 numeric_accuracy targets): 16.82%

**Key points** (RQ3 keypoint_recall targets)

1. The operating lease cost increased by 16.82% from FY2022 to FY2023.
2. The answer must mention GPUs (or graphics processing units) as a dependency.
3. The answer must mention servers as a dependency.

**Gold evidence**

1. `MSFT_FY2023_2023-06-30` · Item 8 › PART II · table

   > Operating lease cost | $2,875 | $2,461 | $2,127

2. `MSFT_FY2023_2023-06-30` · Item 1A › PART I · text

   > Our datacenters depend on the availability of permitted and buildable land, predictable energy, networking supplies, and servers, including graphics processing units (“GPUs”) and other components.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 7 |
| recall@5 | 0.50 | 0.00 | 0.50 | 0.50 |
| recall@all | 0.50 | 0.00 | 0.50 | 0.50 |
| complete@all | 0 | 0 | 0 | 0 |
| average precision (lexical) | 0.33 | 0.00 | 1.00 | 0.50 |
| gold evidence first rank | #1: 3, #2: – | #1: –, #2: – | #1: 1, #2: – | #1: 2, #2: – |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✗ | ✓ | ✓ |
| keypoint_recall | 0.33 | 0.00 | 0.33 | 0.33 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 0.00 | 1.00 | 1.00 |
| citation precision | 0.50 | – | 1.00 | 1.00 |
| citation recall | 0.50 | – | 0.50 | 0.50 |
| citation F1 | 0.50 | – | 0.67 | 0.67 |
| has a citation | 1 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 1831 | 1286 | 6042 | 6553 |
| cost (USD) | 0.0003 | 0.0002 | 0.0210 | 0.0223 |
| latency (s) | 3.3 | 5.5 | 8.6 | 9.6 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 4.

**Generated answer**

> Microsoft’s operating lease cost increased from **$2,461 million in FY2022** to **$2,875 million in FY2023** [3].
>
> Percentage increase:
> \[
> \frac{2{,}875 - 2{,}461}{2{,}461} \times 100 \approx 16.8\%
> \]
>
> So, the **operating lease cost increased by approximately 16.8%** [3].
>
> Two specific infrastructure components/dependencies mentioned in the 10-K that contribute to the datacenter-related lease footprint are:
> 1. **Datacenters** [1][6][7]  
> 2. **Certain equipment** [6][7]
>
> The context does not provide further detail on additional datacenter infrastructure dependencies beyond those lease-related categories.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2023_2023-06-30:431` | Item 8 › PART II | ✓ |  | As of June 30, 2023, we have additional operating and finance leases, primarily for datacenters, that have not yet commenced of $7.7 billion and $34.4 billion, respectively. These operating and finance leases will commen… |
| 2 | `MSFT_FY2023_2023-06-30:188` | Item 7 › Economic Conditions, Challenges, and Risks |  |  | On January 18, 2023, we announced decisions we made to align our cost structure with our revenue and customer demand, prioritize our investments in strategic areas, and consolidate office space. As a result, we recorded … |
| 3 | `MSFT_FY2023_2023-06-30:424` | Item 8 › PART II | ✓ | #1 | \| (In millions) \| \| \| \| \|---\|---\|---\|---\| \| Year Ended June 30, \| 2023 \| 2022 \| 2021 \| \| Operating lease cost \| $2,875 \| $2,461 \| $2,127 \| \| Finance lease cost: \| \| \| \| \| Amortization of right-of-use assets \| $1,352 \| $9… |
| 4 | `MSFT_FY2023_2023-06-30:205` | Item 7 › Fiscal Year 2023 Compared with Fiscal Year 2022 |  |  | Microsoft Cloud gross margin percentage increased 2 points to 72%. Excluding the impact of the change in accounting estimate, Microsoft Cloud gross margin percentage decreased slightly driven by a decline in Azure and ot… |
| 5 | `MSFT_FY2023_2023-06-30:373` | Item 8 › PART II |  |  | During fiscal years 2023, 2022, and 2021, depreciation expense was $11.0 billion, $12.6 billion, and $9.3 billion, respectively. Depreciation expense declined in fiscal year 2023 due to the change in estimated useful liv… |
| 6 | `MSFT_FY2023_2023-06-30:423` | Item 8 › PART II | ✓ |  | Revenue allocated to remaining performance obligations, which includes unearned revenue and amounts that will be invoiced and recognized as revenue in future periods, was $229 billion as of June 30, 2023, of which $224 b… |
| 7 | `MSFT_FY2023_2023-06-30:252` | Item 7 › Other Planned Uses of Capital | ✓ |  | We will continue to invest in sales, marketing, product support infrastructure, and existing and advanced areas of technology, as well as acquisitions that align with our business strategy. Additions to property and equi… |
| 8 | `MSFT_FY2023_2023-06-30:427` | Item 8 › PART II |  |  | Supplemental balance sheet information related to leases was as follows: |
| 9 | `MSFT_FY2023_2023-06-30:425` | Item 8 › PART II |  |  | Supplemental cash flow information related to leases was as follows: |
| 10 | `MSFT_FY2023_2023-06-30:204` | Item 7 › Fiscal Year 2023 Compared with Fiscal Year 2022 |  |  | Revenue increased $13.6 billion or 7% driven by growth in Intelligent Cloud and Productivity and Business Processes, offset in part by a decline in More Personal Computing. Intelligent Cloud revenue increased driven by A… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `MSFT_FY2023_2023-06-30:431`** (cited)

````text
Item 8 > PART II
As of June 30, 2023, we have additional operating and finance leases, primarily for datacenters, that have not yet commenced of $7.7 billion and $34.4 billion, respectively. These operating and finance leases will commence between fiscal year 2024 and fiscal year 2030 with lease terms of 1 year to 18 years.
````

**#3 `MSFT_FY2023_2023-06-30:424`** (cited, gold #1)

````text
Item 8 > PART II (table)
| (In millions) |  |  |  |
|---|---|---|---|
| Year Ended June 30, | 2023 | 2022 | 2021 |
| Operating lease cost | $2,875 | $2,461 | $2,127 |
| Finance lease cost: |  |  |  |
| Amortization of right-of-use assets | $1,352 | $980 | $921 |
| Interest on lease liabilities | 501 | 429 | 386 |
| Total finance lease cost | $1,853 | $1,409 | $1,307 |
````

**#6 `MSFT_FY2023_2023-06-30:423`** (cited)

````text
Item 8 > PART II
Revenue allocated to remaining performance obligations, which includes unearned revenue and amounts that will be invoiced and recognized as revenue in future periods, was $229 billion as of June 30, 2023, of which $224 billion is related to the commercial portion of revenue. We expect to recognize approximately 45% of this revenue over the next 12 months and the remainder thereafter. NOTE 14 — LEASES We have operating and finance leases for datacenters, corporate offices, research and development facilities, Microsoft Experience Centers, and certain equipment. Our leases have remaining lease terms of less than 1 year to 18 years, some of which include options to extend the leases for up to 5 years, and some of which include options to terminate the leases within 1 year. The components of lease expense were as follows:
````

**#7 `MSFT_FY2023_2023-06-30:252`** (cited)

````text
Item 7 > Other Planned Uses of Capital
We will continue to invest in sales, marketing, product support infrastructure, and existing and advanced areas of technology, as well as acquisitions that align with our business strategy. Additions to property and equipment will continue, including new facilities, datacenters, and computer systems for research and development, sales and marketing, support, and administrative staff. We expect capital expenditures to increase in coming years to support growth in our cloud offerings and our investments in AI infrastructure. We have operating and finance leases for datacenters, corporate offices, research and development facilities, Microsoft Experience Centers, and certain equipment. We have not engaged in any related party transactions or arrangements with unconsolidated entities or other persons that are reasonably likely to materially affect liquidity or the availability of capital resources. CRITICAL ACCOUNTING ESTIMATES
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 8'), ('MSFT', 'Item 7')] gold=[(None, 'Item 8'), (None, 'Item 1A')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2023_2023-06-30:204` | Item 7 › Fiscal Year 2023 Compared with Fiscal Year 2022 |  |  | Revenue increased $13.6 billion or 7% driven by growth in Intelligent Cloud and Productivity and Business Processes, offset in part by a decline in More Personal Computing. Intelligent Cloud revenue increased driven by A… |
| 2 | `MSFT_FY2023_2023-06-30:210` | Item 7 › Fiscal Year 2023 Compared with Fiscal Year 2022 |  |  | Operating expenses increased $1.3 billion or 7% driven by investment in LinkedIn and employee severance expenses. Revenue, gross margin, and operating income included an unfavorable foreign currency impact of 5%, 5%, and… |
| 3 | `MSFT_FY2023_2023-06-30:182` | Item 7 |  |  | Microsoft is a technology company whose mission is to empower every person and every organization on the planet to achieve more. We strive to create local opportunity, growth, and impact in every country around the world… |
| 4 | `MSFT_FY2023_2023-06-30:209` | Item 7 › Fiscal Year 2023 Compared with Fiscal Year 2022 |  |  | Productivity and Business Processes Revenue increased $5.9 billion or 9%. • Office Commercial products and cloud services revenue increased $3.7 billion or 10%. Office 365 Commercial revenue grew 13% with seat growth of … |
| 5 | `MSFT_FY2023_2023-06-30:205` | Item 7 › Fiscal Year 2023 Compared with Fiscal Year 2022 |  |  | Microsoft Cloud gross margin percentage increased 2 points to 72%. Excluding the impact of the change in accounting estimate, Microsoft Cloud gross margin percentage decreased slightly driven by a decline in Azure and ot… |

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 1.

**Generated answer**

> Microsoft’s operating lease cost increased from $2,461 million in fiscal year 2022 to $2,875 million in fiscal year 2023, an increase of approximately 16.8% (($2,875 - $2,461) / $2,461) [MSFT FY2023, Item 8, MSFT_FY2023_2023-06-30:424].  
>
> The filing does not disclose in the provided evidence the specific datacenter infrastructure components or dependencies that contribute to the cost and complexity of maintaining that infrastructure.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `MSFT_FY2023_2023-06-30:424` | Item 8 › PART II | ✓ | #1 | \| (In millions) \| \| \| \| \|---\|---\|---\|---\| \| Year Ended June 30, \| 2023 \| 2022 \| 2021 \| \| Operating lease cost \| $2,875 \| $2,461 \| $2,127 \| \| Finance lease cost: \| \| \| \| \| Amortization of right-of-use assets \| $1,352 \| $9… |
| 2 | `MSFT_FY2023_2023-06-30:430` | Item 8 › PART II |  |  | \| (In millions) \| \| \| \|---\|---\|---\| \| Year Ending June 30, \| Operating Leases \| Finance Leases \| \| 2024 \| $2,784 \| $1,747 \| \| 2025 \| 2,508 \| 2,087 \| \| 2026 \| 2,142 \| 1,771 \| \| 2027 \| 1,757 \| 1,780 \| \| 2028 \| 1,582 \| 1,78… |
| 3 | `MSFT_FY2023_2023-06-30:428` | Item 8 › PART II |  |  | \| (In millions, except lease term and discount rate) \| \| \| \|---\|---\|---\| \| June 30, \| 2023 \| 2022 \| \| Operating Leases \| \| \| \| Operating lease right-of-use assets \| $14,346 \| $13,148 \| \| Other current liabilities \| $2,40… |
| 4 | `MSFT_FY2023_2023-06-30:426` | Item 8 › PART II |  |  | \| (In millions) \| \| \| \| \|---\|---\|---\|---\| \| Year Ended June 30, \| 2023 \| 2022 \| 2021 \| \| Cash paid for amounts included in the measurement of lease liabilities: \| \| \| \| \| Operating cash flows from operating leases \| $2,7… |
| 5 | `MSFT_FY2023_2023-06-30:326` | Item 8 › Leases |  |  | We determine if an arrangement is a lease at inception. Operating leases are included in operating lease right-of-use (“ROU”) assets, other current liabilities, and operating lease liabilities in our consolidated balance… |
| 6 | `MSFT_FY2023_2023-06-30:233` | Item 7 › PART II |  |  | \| (In millions, except percentages and per share amounts) \| 2023 \| 2022 \| Percentage Change \| \|---\|---\|---\|---\| \| Gross margin \| $146,052 \| $135,620 \| 8% \| \| Severance, hardware-related impairment, and lease consolidatio… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `MSFT_FY2023_2023-06-30:424`** (cited, gold #1)

````text
Item 8 > PART II (table)
| (In millions) |  |  |  |
|---|---|---|---|
| Year Ended June 30, | 2023 | 2022 | 2021 |
| Operating lease cost | $2,875 | $2,461 | $2,127 |
| Finance lease cost: |  |  |  |
| Amortization of right-of-use assets | $1,352 | $980 | $921 |
| Interest on lease liabilities | 501 | 429 | 386 |
| Total finance lease cost | $1,853 | $1,409 | $1,307 |
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Microsoft’s operating lease cost increased from $2,461 million in fiscal year 2022 to $2,875 million in fiscal year 2023, an increase of approximately 16.8% (($2,875 - $2,461) / $2,461) [MSFT FY2023, Item 8, MSFT_FY2023_2023-06-30:424]. | None |  |
| The filing does not disclose in the provided evidence the specific datacenter infrastructure components or dependencies that contribute to the cost and complexity of maintaining that infrastructure. | supported | The retrieved evidence only provides lease-related amounts and classifications, not specific datacenter infrastructure components or dependencies. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 1.

**Generated answer**

> Microsoft’s operating lease cost increased from $2,461 million in fiscal year 2022 to $2,875 million in fiscal year 2023, which is an increase of approximately 16.8% (($2,875 - $2,461) / $2,461) [MSFT FY2023, Item 8, MSFT_FY2023_2023-06-30:424].  
>
> The filing excerpts provided do not disclose the specific datacenter infrastructure components or dependencies that contribute to the cost and complexity of maintaining the datacenter infrastructure driving these lease expenses.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-MSFT-2023` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2023,2023-06-30,211915000000,72361000000,88523000000,411976000… |
| 2 | `MSFT_FY2023_2023-06-30:424` | Item 8 › PART II | ✓ | #1 | \| (In millions) \| \| \| \| \|---\|---\|---\|---\| \| Year Ended June 30, \| 2023 \| 2022 \| 2021 \| \| Operating lease cost \| $2,875 \| $2,461 \| $2,127 \| \| Finance lease cost: \| \| \| \| \| Amortization of right-of-use assets \| $1,352 \| $9… |
| 3 | `MSFT_FY2023_2023-06-30:430` | Item 8 › PART II |  |  | \| (In millions) \| \| \| \|---\|---\|---\| \| Year Ending June 30, \| Operating Leases \| Finance Leases \| \| 2024 \| $2,784 \| $1,747 \| \| 2025 \| 2,508 \| 2,087 \| \| 2026 \| 2,142 \| 1,771 \| \| 2027 \| 1,757 \| 1,780 \| \| 2028 \| 1,582 \| 1,78… |
| 4 | `MSFT_FY2023_2023-06-30:428` | Item 8 › PART II |  |  | \| (In millions, except lease term and discount rate) \| \| \| \|---\|---\|---\| \| June 30, \| 2023 \| 2022 \| \| Operating Leases \| \| \| \| Operating lease right-of-use assets \| $14,346 \| $13,148 \| \| Other current liabilities \| $2,40… |
| 5 | `MSFT_FY2023_2023-06-30:426` | Item 8 › PART II |  |  | \| (In millions) \| \| \| \| \|---\|---\|---\|---\| \| Year Ended June 30, \| 2023 \| 2022 \| 2021 \| \| Cash paid for amounts included in the measurement of lease liabilities: \| \| \| \| \| Operating cash flows from operating leases \| $2,7… |
| 6 | `MSFT_FY2023_2023-06-30:326` | Item 8 › Leases |  |  | We determine if an arrangement is a lease at inception. Operating leases are included in operating lease right-of-use (“ROU”) assets, other current liabilities, and operating lease liabilities in our consolidated balance… |
| 7 | `MSFT_FY2023_2023-06-30:233` | Item 7 › PART II |  |  | \| (In millions, except percentages and per share amounts) \| 2023 \| 2022 \| Percentage Change \| \|---\|---\|---\|---\| \| Gross margin \| $146,052 \| $135,620 \| 8% \| \| Severance, hardware-related impairment, and lease consolidatio… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `MSFT_FY2023_2023-06-30:424`** (cited, gold #1)

````text
Item 8 > PART II (table)
| (In millions) |  |  |  |
|---|---|---|---|
| Year Ended June 30, | 2023 | 2022 | 2021 |
| Operating lease cost | $2,875 | $2,461 | $2,127 |
| Finance lease cost: |  |  |  |
| Amortization of right-of-use assets | $1,352 | $980 | $921 |
| Interest on lease liabilities | 501 | 429 | 386 |
| Total finance lease cost | $1,853 | $1,409 | $1,307 |
````

</details>

RQ2 citation match (section level): `cited=[('MSFT', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 6, verified 6, ungrounded 0, uncited 0, derived 1; sentence verdicts: supported 1, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Microsoft’s operating lease cost increased from $2,461 million in fiscal year 2022 to $2,875 million in fiscal year 2023, which is an increase of approximately 16.8% (($2,875 - $2,461) / $2,461) [MSFT FY2023, Item 8, MSFT_FY2023_2023-06-30:424]. | None |  |
| The filing excerpts provided do not disclose the specific datacenter infrastructure components or dependencies that contribute to the cost and complexity of maintaining the datacenter infrastructure driving these lease expenses. | supported | The retrieved evidence provides lease amounts and accounting treatment but does not disclose specific datacenter infrastructure components or dependencies driving those lease expenses. |

</details>
