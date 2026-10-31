# gold-073: Cross-year table

[← all cases](../README.md) · company: NVIDIA CORP (NVDA) · fiscal year: 2022 · recipe `cross_year_table` · hop `multi` · answer type `numeric` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> By how many percentage points did NVIDIA's gross margin increase from fiscal year 2016 to fiscal year 2022?

**Gold answer**

> 8.8 percentage points

**Program**: `subtract(64.9, 56.1)` → `8.800000000000004`

**Gold numbers** (RQ2 numeric_accuracy targets): 8.8 percentage points

**Gold evidence**

1. `NVDA_FY2022_2022-01-30` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Fiscal Year 2022 Summary · table

   > Gross margin | 64.9% | 62.3% | Up 260 bps

2. `NVDA_FY2016_2016-01-31` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Recent Developments, Future Objectives and Challenges · table

   > Gross margin | 56.1% | 55.5% | up 60 bps

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 8 | 5 | 10 | 8 |
| recall@5 | 0.50 | 0.00 | 0.50 | 0.00 |
| recall@all | 0.50 | 0.00 | 1.00 | 0.50 |
| complete@all | 0 | 0 | 1 | 0 |
| average precision (lexical) | 0.20 | 0.00 | 0.25 | 0.17 |
| gold evidence first rank | #1: 5, #2: – | #1: –, #2: – | #1: 8, #2: 4 | #1: –, #2: 6 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✗ | ✓ | ✗ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 1.00 | 0.00 |
| citation precision | 1.00 | – | 1.00 | 1.00 |
| citation recall | 1.00 | – | 1.00 | 1.00 |
| citation F1 | 1.00 | – | 1.00 | 1.00 |
| has a citation | 1 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.33 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 2 | 1 |
| tokens | 1771 | 1213 | 12388 | 10563 |
| cost (USD) | 0.0003 | 0.0002 | 0.0404 | 0.0367 |
| latency (s) | 3.4 | 6.1 | 14.8 | 15.7 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 8, cited: 2.

**Generated answer**

> The provided context gives NVIDIA’s gross margin for fiscal year 2022 as **64.9%** [5], but it does **not** provide NVIDIA’s overall gross margin for fiscal year 2016. Chunk [2] discusses the **GPU business gross margin** trend in 2016, not the company-wide gross margin percentage.
>
> So, I can only answer part of the question:
>
> - **Fiscal year 2022 gross margin:** 64.9% [5]
> - **Fiscal year 2016 gross margin:** not provided in the context
>
> Therefore, **the increase from fiscal year 2016 to fiscal year 2022 cannot be determined from the provided context**. [2][5]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2022_2022-01-30:198` | Item 7 › Gross Profit and Gross Margin |  |  | Inventory provisions totaled $354 million and $116 million for fiscal years 2022 and 2021, respectively. Sales of inventory that was previously written-off or written-down totaled $111 million and $145 million for fiscal… |
| 2 | `NVDA_FY2016_2016-01-31:162` | Item 7 › Gross Profit and Gross Margin | ✓ |  | GPU Business. The gross margin of our GPU business increased during fiscal year 2016 when compared to fiscal year 2015 primarily due to a richer product mix resulting from stronger sales of our GeForce GPU products for g… |
| 3 | `NVDA_FY2022_2022-01-30:171` | Item 7 › Fiscal Year 2022 Summary |  |  | We specialize in markets where our computing platforms can provide tremendous acceleration for applications. These platforms incorporate processors, interconnects, software, algorithms, systems, and services to deliver u… |
| 4 | `NVDA_FY2022_2022-01-30:194` | Item 7 › Revenue by Reportable Segments |  |  | Graphics - Graphics segment revenue increased by 61% in fiscal year 2022 compared to fiscal year 2021. We continue to benefit from strong demand for NVIDIA Ampere architecture products, and believe the increase in Gaming… |
| 5 | `NVDA_FY2022_2022-01-30:170` | Item 7 › Fiscal Year 2022 Summary | ✓ | #1 | \| \| Year Ended \| \| \| \|---\|---\|---\|---\| \| \| January 30, 2022 \| January 31, 2021 \| Change \| \| \| ($ in millions, except per share data) \| \| \| \| Revenue \| $26,914 \| $16,675 \| Up 61% \| \| Gross margin \| 64.9% \| 62.3% \| Up 260 … |
| 6 | `NVDA_FY2022_2022-01-30:201` | Item 7 › Sales, General and Administrative |  |  | Sales, general and administrative expenses increased by 12% in fiscal year 2022 compared to fiscal year 2021, primarily driven by stock-based compensation, compensation-related costs associated with employee growth, part… |
| 7 | `NVDA_FY2022_2022-01-30:195` | Item 7 › Revenue by Reportable Segments |  |  | Compute & Networking - Compute & Networking segment revenue increased by 61% in fiscal year 2022 compared to fiscal year 2021, driven primarily by sales of NVIDIA Ampere architecture products to hyperscale customers for … |
| 8 | `NVDA_FY2022_2022-01-30:173` | Item 7 › Table of Contents |  |  | Automotive revenue was up 6% from a year ago due to self-driving and AI cockpit solutions offset by a decline in legacy cockpit revenue. OEM and Other revenue was up 84% from a year ago primarily driven by CMP sales. CMP… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `NVDA_FY2016_2016-01-31:162`** (cited)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Gross Profit and Gross Margin
GPU Business. The gross margin of our GPU business increased during fiscal year 2016 when compared to fiscal year 2015 primarily due to a richer product mix resulting from stronger sales of our GeForce GPU products for gaming and lower sales of GeForce GPU products for mainstream PC OEMs. The gross margin of our GPU business increased during fiscal year 2015 when compared to fiscal year 2014 due to richer product mix resulting from strong sales of high-end GeForce GTX GPU products based on our Maxwell architecture and the volume increase in our Tesla accelerated computing products.
````

**#5 `NVDA_FY2022_2022-01-30:170`** (cited, gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Fiscal Year 2022 Summary (table)
|  | Year Ended |  |  |
|---|---|---|---|
|  | January 30, 2022 | January 31, 2021 | Change |
|  | ($ in millions, except per share data) |  |  |
| Revenue | $26,914 | $16,675 | Up 61% |
| Gross margin | 64.9% | 62.3% | Up 260 bps |
| Operating expenses | $7,434 | $5,864 | Up 27% |
| Income from operations | $10,041 | $4,532 | Up 122% |
| Net income | $9,752 | $4,332 | Up 125% |
| Net income per diluted share | $3.85 | $1.73 | Up 123% |
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 7')] gold=[(None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2022_2022-01-30:171` | Item 7 › Fiscal Year 2022 Summary |  |  | We specialize in markets where our computing platforms can provide tremendous acceleration for applications. These platforms incorporate processors, interconnects, software, algorithms, systems, and services to deliver u… |
| 2 | `NVDA_FY2022_2022-01-30:198` | Item 7 › Gross Profit and Gross Margin |  |  | Inventory provisions totaled $354 million and $116 million for fiscal years 2022 and 2021, respectively. Sales of inventory that was previously written-off or written-down totaled $111 million and $145 million for fiscal… |
| 3 | `NVDA_FY2022_2022-01-30:194` | Item 7 › Revenue by Reportable Segments |  |  | Graphics - Graphics segment revenue increased by 61% in fiscal year 2022 compared to fiscal year 2021. We continue to benefit from strong demand for NVIDIA Ampere architecture products, and believe the increase in Gaming… |
| 4 | `NVDA_FY2022_2022-01-30:173` | Item 7 › Table of Contents |  |  | Automotive revenue was up 6% from a year ago due to self-driving and AI cockpit solutions offset by a decline in legacy cockpit revenue. OEM and Other revenue was up 84% from a year ago primarily driven by CMP sales. CMP… |
| 5 | `NVDA_FY2022_2022-01-30:197` | Item 7 › Gross Profit and Gross Margin |  |  | Gross profit consists of total revenue, net of allowances, less cost of revenue. Cost of revenue consists primarily of the cost of semiconductors, including wafer fabrication, assembly, testing and packaging, board and d… |

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 10, cited: 2.

**Generated answer**

> NVIDIA's gross margin increased from 56.1% in fiscal year 2016 to 64.9% in fiscal year 2022, an increase of 8.8 percentage points [NVDA FY2016, Item 7, NVDA_FY2016_2016-01-31:160] [NVDA FY2022, Item 7, NVDA_FY2022_2022-01-30:197].
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 8.8; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `NVDA_FY2022_2022-01-30:198` | Item 7 › Gross Profit and Gross Margin |  |  | Inventory provisions totaled $354 million and $116 million for fiscal years 2022 and 2021, respectively. Sales of inventory that was previously written-off or written-down totaled $111 million and $145 million for fiscal… |
| 2 | `NVDA_FY2016_2016-01-31:161` | Item 7 › Gross Profit and Gross Margin |  |  | Charges to cost of sales for inventory provisions totaled $112 million, $59 million and $50 million for fiscal years 2016, 2015 and 2014, unfavorably impacting our gross margin by 2.2%, 1.3% and 1.2%, respectively. Sales… |
| 3 | `NVDA_FY2016_2016-01-31:125` | Item 7 › Recent Developments, Future Objectives and Challenges |  |  | Net income for fiscal year 2016 was $614 million and net income per diluted share was $1.08, down from $631 million and $1.12, respectively, in the previous year. These decreases were driven by our legal fees and our res… |
| 4 | `NVDA_FY2016_2016-01-31:123` | Item 7 › Recent Developments, Future Objectives and Challenges |  | #2 | \| \| Year Ended \| \| \| \|---\|---\|---\|---\| \| \| January 31, 2016 \| January 25, 2015 \| Change \| \| \| (In millions, except per share data) \| \| \| \| Revenue \| $5,010 \| $4,682 \| up 7% \| \| Gross margin \| 56.1% \| 55.5% \| up 60 bps \| … |
| 5 | `NVDA_FY2016_2016-01-31:162` | Item 7 › Gross Profit and Gross Margin |  |  | GPU Business. The gross margin of our GPU business increased during fiscal year 2016 when compared to fiscal year 2015 primarily due to a richer product mix resulting from stronger sales of our GeForce GPU products for g… |
| 6 | `NVDA_FY2016_2016-01-31:137` | Item 7 › Table of Contents |  |  | The overall net effect on our gross margin from inventory provisions and sales of items previously written down was an unfavorable impact of 1.6%, 0.6% and 0.1% in fiscal years 2016, 2015 and 2014, respectively. The char… |
| 7 | `NVDA_FY2022_2022-01-30:192` | Item 7 › Results of Operations |  |  | \| \| Year Ended \| \| \|---\|---\|---\| \| \| January 30, 2022 \| January 31, 2021 \| \| Revenue \| 100.0% \| 100.0% \| \| Cost of revenue \| 35.1 \| 37.7 \| \| Gross profit \| 64.9 \| 62.3 \| \| Operating expenses: \| \| \| \| Research and develop… |
| 8 | `NVDA_FY2022_2022-01-30:170` | Item 7 › Fiscal Year 2022 Summary |  | #1 | \| \| Year Ended \| \| \| \|---\|---\|---\|---\| \| \| January 30, 2022 \| January 31, 2021 \| Change \| \| \| ($ in millions, except per share data) \| \| \| \| Revenue \| $26,914 \| $16,675 \| Up 61% \| \| Gross margin \| 64.9% \| 62.3% \| Up 260 … |
| 9 | `NVDA_FY2022_2022-01-30:197` | Item 7 › Gross Profit and Gross Margin | ✓ |  | Gross profit consists of total revenue, net of allowances, less cost of revenue. Cost of revenue consists primarily of the cost of semiconductors, including wafer fabrication, assembly, testing and packaging, board and d… |
| 10 | `NVDA_FY2016_2016-01-31:160` | Item 7 › Gross Profit and Gross Margin | ✓ |  | Gross profit consists of total revenue, net of allowances, less cost of revenue. Cost of revenue consists primarily of the cost of semiconductors purchased from subcontractors, including wafer fabrication, assembly, test… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#4 `NVDA_FY2016_2016-01-31:123`** (gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Recent Developments, Future Objectives and Challenges (table)
|  | Year Ended |  |  |
|---|---|---|---|
|  | January 31, 2016 | January 25, 2015 | Change |
|  | (In millions, except per share data) |  |  |
| Revenue | $5,010 | $4,682 | up 7% |
| Gross margin | 56.1% | 55.5% | up 60 bps |
| Operating expenses | $2,064 | $1,840 | up 12% |
| Income from operations | $747 | $759 | down 2% |
| Net income | $614 | $631 | down 3% |
| Net income per diluted share | $1.08 | $1.12 | down 4% |
````

**#8 `NVDA_FY2022_2022-01-30:170`** (gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Fiscal Year 2022 Summary (table)
|  | Year Ended |  |  |
|---|---|---|---|
|  | January 30, 2022 | January 31, 2021 | Change |
|  | ($ in millions, except per share data) |  |  |
| Revenue | $26,914 | $16,675 | Up 61% |
| Gross margin | 64.9% | 62.3% | Up 260 bps |
| Operating expenses | $7,434 | $5,864 | Up 27% |
| Income from operations | $10,041 | $4,532 | Up 122% |
| Net income | $9,752 | $4,332 | Up 125% |
| Net income per diluted share | $3.85 | $1.73 | Up 123% |
````

**#9 `NVDA_FY2022_2022-01-30:197`** (cited)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Gross Profit and Gross Margin
Gross profit consists of total revenue, net of allowances, less cost of revenue. Cost of revenue consists primarily of the cost of semiconductors, including wafer fabrication, assembly, testing and packaging, board and device costs, manufacturing support costs, including labor and overhead associated with such purchases, final test yield fallout, inventory and warranty provisions, memory and component costs, tariffs, and shipping costs. Cost of revenue also includes acquisition-related costs, development costs for license and service arrangements, IP-related costs, and stock-based compensation related to personnel associated with manufacturing. Our overall gross margin was 64.9% and 62.3% for fiscal years 2022 and 2021, respectively. The increase in fiscal year 2022 was primarily due to lower Mellanox acquisition-related charges, including a non-recurring inventory step-up charge of $161 million in fiscal year 2021. The increase also benefited from a higher-end mix within Graphics, partially offset by a mix shift within Compute & Networking.
````

**#10 `NVDA_FY2016_2016-01-31:160`** (cited)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Gross Profit and Gross Margin
Gross profit consists of total revenue, net of allowances, less cost of revenue. Cost of revenue consists primarily of the cost of semiconductors purchased from subcontractors, including wafer fabrication, assembly, testing and packaging, board and device costs, manufacturing support costs, including labor and overhead associated with such purchases, final test yield fallout, inventory and warranty provisions and shipping costs. Cost of revenue also includes development costs for license and service arrangements and stock-based compensation related to personnel associated with manufacturing. Gross margin is the percentage of gross profit to revenue. Our overall gross margin was 56.1%, 55.5% and 54.9% for fiscal years 2016, 2015 and 2014, respectively. The increase over these fiscal years was driven primarily by a richer product mix in our GPU business, partially offset by lower Tegra business margins.
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 3, verified 2, ungrounded 1, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 8.8

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| NVIDIA's gross margin increased from 56.1% in fiscal year 2016 to 64.9% in fiscal year 2022, an increase of 8.8 percentage points [NVDA FY2016, Item 7, NVDA_FY2016_2016-01-31:160] [NVDA FY2022, Item 7, NVDA_FY2022_2022-01-30:197]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 2.

**Generated answer**

> NVIDIA’s gross margin was 56.1% in fiscal year 2016. [NVDA FY2016, Item 7, NVDA_FY2016_2016-01-31:123]
>
> The provided evidence does not disclose NVIDIA’s overall gross margin percentage for fiscal year 2022; it only states that inventory provisions had an unfavorable impact of 0.9% on gross margin in fiscal year 2022 and discusses segment gross margin trends. [NVDA FY2022, Item 7, NVDA_FY2022_2022-01-30:198]
>
> Therefore, the increase in NVIDIA’s overall gross margin from fiscal year 2016 to fiscal year 2022 cannot be determined from the provided evidence. [NVDA FY2016, Item 7, NVDA_FY2016_2016-01-31:123] [NVDA FY2022, Item 7, NVDA_FY2022_2022-01-30:198]
>
> > [Guardrail Audit Warning]: Manual verification required; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-NVDA-2016` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2016,2016-01-31,5010000000,614000000,747000000,7370000000,2814… |
| 2 | `F-NVDA-2022` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2022,2022-01-30,26914000000,9752000000,10041000000,44187000000… |
| 3 | `NVDA_FY2022_2022-01-30:198` | Item 7 › Gross Profit and Gross Margin | ✓ |  | Inventory provisions totaled $354 million and $116 million for fiscal years 2022 and 2021, respectively. Sales of inventory that was previously written-off or written-down totaled $111 million and $145 million for fiscal… |
| 4 | `NVDA_FY2016_2016-01-31:161` | Item 7 › Gross Profit and Gross Margin |  |  | Charges to cost of sales for inventory provisions totaled $112 million, $59 million and $50 million for fiscal years 2016, 2015 and 2014, unfavorably impacting our gross margin by 2.2%, 1.3% and 1.2%, respectively. Sales… |
| 5 | `NVDA_FY2016_2016-01-31:125` | Item 7 › Recent Developments, Future Objectives and Challenges |  |  | Net income for fiscal year 2016 was $614 million and net income per diluted share was $1.08, down from $631 million and $1.12, respectively, in the previous year. These decreases were driven by our legal fees and our res… |
| 6 | `NVDA_FY2016_2016-01-31:123` | Item 7 › Recent Developments, Future Objectives and Challenges | ✓ | #2 | \| \| Year Ended \| \| \| \|---\|---\|---\|---\| \| \| January 31, 2016 \| January 25, 2015 \| Change \| \| \| (In millions, except per share data) \| \| \| \| Revenue \| $5,010 \| $4,682 \| up 7% \| \| Gross margin \| 56.1% \| 55.5% \| up 60 bps \| … |
| 7 | `NVDA_FY2016_2016-01-31:162` | Item 7 › Gross Profit and Gross Margin |  |  | GPU Business. The gross margin of our GPU business increased during fiscal year 2016 when compared to fiscal year 2015 primarily due to a richer product mix resulting from stronger sales of our GeForce GPU products for g… |
| 8 | `NVDA_FY2016_2016-01-31:137` | Item 7 › Table of Contents |  |  | The overall net effect on our gross margin from inventory provisions and sales of items previously written down was an unfavorable impact of 1.6%, 0.6% and 0.1% in fiscal years 2016, 2015 and 2014, respectively. The char… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `NVDA_FY2022_2022-01-30:198`** (cited)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Gross Profit and Gross Margin
Inventory provisions totaled $354 million and $116 million for fiscal years 2022 and 2021, respectively. Sales of inventory that was previously written-off or written-down totaled $111 million and $145 million for fiscal years 2022 and 2021, respectively. As a result, the overall net effect on our gross margin was an unfavorable impact of 0.9% in fiscal year 2022 and insignificant in fiscal year 2021. The gross margin of our Graphics segment increased during fiscal year 2022 when compared to fiscal year 2021, primarily due to higher-end mix within GeForce GPUs. The gross margin of our Compute & Networking segment decreased during fiscal year 2022 when compared to fiscal year 2021, primarily due to a shift in product mix and partially offset by a reduced contribution from Automotive solutions.
````

**#6 `NVDA_FY2016_2016-01-31:123`** (cited, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Recent Developments, Future Objectives and Challenges (table)
|  | Year Ended |  |  |
|---|---|---|---|
|  | January 31, 2016 | January 25, 2015 | Change |
|  | (In millions, except per share data) |  |  |
| Revenue | $5,010 | $4,682 | up 7% |
| Gross margin | 56.1% | 55.5% | up 60 bps |
| Operating expenses | $2,064 | $1,840 | up 12% |
| Income from operations | $747 | $759 | down 2% |
| Net income | $614 | $631 | down 3% |
| Net income per diluted share | $1.08 | $1.12 | down 4% |
````

</details>

RQ2 citation match (section level): `cited=[('NVDA', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 2, verified 2, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 1, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| NVIDIA’s gross margin was 56.1% in fiscal year 2016. [NVDA FY2016, Item 7, NVDA_FY2016_2016-01-31:123] | None |  |
| The provided evidence does not disclose NVIDIA’s overall gross margin percentage for fiscal year 2022; it only states that inventory provisions had an unfavorable impact of 0.9% on gross margin in fiscal year 2022 and discusses segment gross margin trends. [NVDA FY2022, Item 7, NVDA_FY2022_2022-01-30:198] | None |  |
| Therefore, the increase in NVIDIA’s overall gross margin from fiscal year 2016 to fiscal year 2022 cannot be determined from the provided evidence. [NVDA FY2016, Item 7, NVDA_FY2016_2016-01-31:123] [NVDA FY2022, Item 7, NVDA_FY2022_2022-01-30:198] | unsupported | The 2016 evidence gives overall gross margin as 56.1%, but the 2022 cited evidence does not provide NVIDIA’s overall gross margin, so the sentence’s claim about what cannot be determined from the provided evidence is not established by the cited text alone. |

</details>
