# gold-061: Table + text (one filing)

[← all cases](../README.md) · company: Apple Inc. (AAPL) · fiscal year: 2025 · recipe `table_text` · hop `multi` · answer type `mixed` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> Calculate the year-over-year percentage growth in Apple's Services net sales for fiscal year 2025 compared to fiscal year 2024. Additionally, explain how Apple accounts for third-party application sales within this Services category and describe the competitive pressures the company faces in its markets.

**Gold answer**

> Services net sales grew 13.51%, from $96,169 million in fiscal 2024 to $109,158 million in fiscal 2025. Apple accounts for all third-party application-related sales on a net basis, recognizing in Services net sales only the commission it retains. Its markets are highly competitive, with aggressive price competition, downward pressure on gross margins, continual improvement in product performance and price-sensitive consumers and businesses.

**Program**: `subtract(109158, 96169), divide(#0, 96169), multiply(#1, 100)` → `13.506431386413501`

**Gold numbers** (RQ2 numeric_accuracy targets): 13.51%

**Key points** (RQ3 keypoint_recall targets)

1. The percentage growth in Services net sales is 13.51%.
2. Apple recognizes third-party application sales on a net basis, recording only the commission retained.
3. The company operates in highly competitive markets with aggressive price competition.
4. There is downward pressure on gross margins and price sensitivity among consumers.

**Gold evidence**

1. `AAPL_FY2025_2025-09-27` · Item 8. Financial Statements and Supplementary Data › Note 2 – Revenue · table

   > | Services (1) | 109,158 | 96,169 | 85,200 |

2. `AAPL_FY2025_2025-09-27` · Item 8. Financial Statements and Supplementary Data › Note 2 – Revenue · text

   > Therefore, the Company accounts for all third-party application–related sales on a net basis by recognizing in Services net sales only the commission it retains.

3. `AAPL_FY2025_2025-09-27` · Item 1. Business › Competition · text

   > The markets for the Company’s products and services are highly competitive and are characterized by aggressive price competition, downward pressure on gross margins, continual improvement in product performance, and price sensitivity on the part of consumers and businesses.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 9 | 7 |
| recall@5 | 0.00 | 0.67 | 0.00 | 0.00 |
| recall@all | 0.00 | 0.67 | 0.00 | 0.00 |
| complete@all | 0 | 0 | 0 | 0 |
| average precision (lexical) | 0.00 | 1.00 | 0.00 | 0.00 |
| gold evidence first rank | #1: –, #2: –, #3: – | #1: –, #2: 2, #3: 1 | #1: –, #2: –, #3: – | #1: –, #2: –, #3: – |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✗ | ✗ | ✗ |
| keypoint_recall | 0.50 | 0.00 | 0.75 | 0.50 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 0.00 | 0.00 | 0.00 | 0.00 |
| citation precision | 0.50 | – | 0.50 | 0.50 |
| citation recall | 0.50 | – | 1.00 | 0.50 |
| citation F1 | 0.50 | – | 0.67 | 0.50 |
| has a citation | 1 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.75 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 1 |
| tokens | 1627 | 1269 | 19337 | 13613 |
| cost (USD) | 0.0004 | 0.0002 | 0.0799 | 0.0534 |
| latency (s) | 4.2 | 6.1 | 36.8 | 21.2 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 3.

**Generated answer**

> The context only provides a qualitative statement that **Services net sales increased in 2025 compared to 2024**, primarily due to higher net sales from **advertising, the App Store and cloud services**, but it does **not include the actual 2025 and 2024 Services net sales figures needed to calculate the year-over-year percentage growth**. So the percentage growth **cannot be calculated from the provided context**. [1][2]
>
> For third-party application sales within Services, the provided context mentions the **App Store** as part of Services, but it **does not explain Apple’s accounting treatment** for third-party application sales. [1]
>
> For competitive pressures, the provided context says Apple designs and markets smartphones, personal computers, tablets, wearables, accessories and related services, but it **does not describe the competitive pressures the company faces in its markets**. [7]
>
> So, from the provided context:
> - **YOY Services growth percentage:** cannot be calculated from the provided context. [1][2]
> - **Accounting for third-party application sales:** not described in the provided context. [1]
> - **Competitive pressures:** not described in the provided context. [7]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2025_2025-09-27:136` | Item 7 › Products and Services Performance | ✓ |  | (1)Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. iPhone iPhone net sales increased during 2025 compared to 2024 due to higher net sales of Pro m… |
| 2 | `AAPL_FY2025_2025-09-27:134` | Item 7 › Products and Services Performance | ✓ |  | The following table shows net sales by category for 2025, 2024 and 2023 (dollars in millions): |
| 3 | `AAPL_FY2025_2025-09-27:202` | Item 8 › Note 2 – Revenue |  |  | (1)Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. The Company’s proportion of net sales by disaggregated revenue source was generally consistent … |
| 4 | `AAPL_FY2025_2025-09-27:131` | Item 7 › Segment Operating Performance |  |  | The following table shows net sales by reportable segment for 2025, 2024 and 2023 (dollars in millions): |
| 5 | `AAPL_FY2025_2025-09-27:137` | Item 7 › Gross Margin |  |  | Products and Services gross margin and gross margin percentage for 2025, 2024 and 2023 were as follows (dollars in millions): |
| 6 | `AAPL_FY2025_2025-09-27:143` | Item 7 › Operating Expenses |  |  | Research and Development The growth in R&D expense during 2025 compared to 2024 was primarily driven by increases in headcount-related expenses and infrastructure-related costs. Selling, General and Administrative The gr… |
| 7 | `AAPL_FY2025_2025-09-27:17` | Item 1 › Company Background | ✓ |  | The Company designs, manufactures and markets smartphones, personal computers, tablets, wearables and accessories, and sells a variety of related services. The Company’s fiscal year is the 52- or 53-week period that ends… |
| 8 | `AAPL_FY2025_2025-09-27:200` | Item 8 › Note 2 – Revenue |  |  | The following table shows disaggregated net sales, as well as the portion of total net sales that was previously deferred, for 2025, 2024 and 2023 (in millions): |
| 9 | `AAPL_FY2025_2025-09-27:133` | Item 7 › Segment Operating Performance |  |  | Americas Americas net sales increased during 2025 compared to 2024 primarily due to higher net sales of iPhone and Services. The weakness in foreign currencies relative to the U.S. dollar had an unfavorable year-over-yea… |
| 10 | `AAPL_FY2025_2025-09-27:272` | Item 8 › Note 13 – Segment Information and Geographic Data |  |  | Apple Inc. \| 2025 Form 10-K \| 47 The following tables show net sales for 2025, 2024 and 2023 and long-lived assets as of September 27, 2025 and September 28, 2024 for countries that individually accounted for 10% or more… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2025_2025-09-27:136`** (cited)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Products and Services Performance
(1)Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. iPhone iPhone net sales increased during 2025 compared to 2024 due to higher net sales of Pro models. Mac Mac net sales increased during 2025 compared to 2024 primarily due to higher net sales of laptops and desktops. iPad iPad net sales increased during 2025 compared to 2024 primarily due to higher net sales of iPad Air, iPad mini and iPad, partially offset by lower net sales of iPad Pro. Wearables, Home and Accessories Wearables, Home and Accessories net sales decreased during 2025 compared to 2024 primarily due to lower net sales of Accessories and Wearables. Services Services net sales increased during 2025 compared to 2024 primarily due to higher net sales from advertising, the App Store and cloud services. Apple Inc. | 2025 Form 10-K | 23
````

**#2 `AAPL_FY2025_2025-09-27:134`** (cited)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Products and Services Performance
The following table shows net sales by category for 2025, 2024 and 2023 (dollars in millions):
````

**#7 `AAPL_FY2025_2025-09-27:17`** (cited)

````text
Item 1. Business > Company Background
The Company designs, manufactures and markets smartphones, personal computers, tablets, wearables and accessories, and sells a variety of related services. The Company’s fiscal year is the 52- or 53-week period that ends on the last Saturday of September.
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 7'), ('AAPL', 'Item 1')] gold=[(None, 'Item 8'), (None, 'Item 1')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2025_2025-09-27:24` | Item 1 › Competition |  | #3 | The markets for the Company’s products and services are highly competitive and are characterized by aggressive price competition, downward pressure on gross margins, continual improvement in product performance, and pric… |
| 2 | `AAPL_FY2025_2025-09-27:199` | Item 8 › Note 2 – Revenue |  | #2 | For certain long-term service arrangements, the Company has performance obligations for services it has not yet delivered. For these arrangements, the Company does not have a right to bill for the undelivered services. T… |
| 3 | `AAPL_FY2025_2025-09-27:26` | Item 1 › Competition |  |  | The Company is focused on expanding its market opportunities related to smartphones, personal computers, tablets, wearables and accessories, and services. The Company’s products and services face substantial competition … |
| 4 | `AAPL_FY2025_2025-09-27:49` | Item 1A › Macroeconomic and Industry Risks |  |  | The Company’s products and services face substantial competition from companies that have significant technical, marketing, distribution and other resources, as well as established hardware, software and service offering… |
| 5 | `AAPL_FY2025_2025-09-27:136` | Item 7 › Products and Services Performance |  |  | (1)Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. iPhone iPhone net sales increased during 2025 compared to 2024 due to higher net sales of Pro m… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2025_2025-09-27:24`** (gold #3)

````text
Item 1. Business > Competition
The markets for the Company’s products and services are highly competitive and are characterized by aggressive price competition, downward pressure on gross margins, continual improvement in product performance, and price sensitivity on the part of consumers and businesses. The markets in which the Company competes are further defined by frequent introduction of new products and services, short product life cycles, evolving industry standards, and rapid adoption of technological advancements by competitors. Many of the Company’s competitors seek to compete primarily through aggressive pricing and very low cost structures, and by imitating the Company’s products and infringing on its intellectual property. Apple Inc. | 2025 Form 10-K | 2
````

**#2 `AAPL_FY2025_2025-09-27:199`** (gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Note 2 – Revenue
For certain long-term service arrangements, the Company has performance obligations for services it has not yet delivered. For these arrangements, the Company does not have a right to bill for the undelivered services. The Company has determined that any unbilled consideration relates entirely to the value of the undelivered services. Accordingly, the Company has not recognized revenue, and does not disclose amounts, related to these undelivered services. For the sale of third-party products where the Company obtains control of the product before transferring it to the customer, the Company recognizes revenue based on the gross amount billed to customers. The Company considers multiple factors when determining whether it obtains control of third-party products, including evaluating if it can establish the price of the product, retains inventory risk for tangible products or has the responsibility for ensuring acceptability of the product. For third-party applications sold through the App Store, the Company does not obtain control of the product before transferring it to the customer. Therefore, the Company accounts for all third-party application–related sales on a net basis by recognizing in Services net sales only the commission it retains. Apple Inc. | 2025 Form 10-K | 35
````

</details>

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 9, cited: 6.

**Generated answer**

> Apple’s Services net sales were $107.2 billion in fiscal 2025 and $96.2 billion in fiscal 2024, and the year-over-year growth was approximately 11.4% (($107.2 billion - $96.2 billion) / $96.2 billion). [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:134] [AAPL FY2025, Item 8, AAPL_FY2025_2025-09-27:200]
>
> Apple states that Services net sales increased during 2025 compared to 2024 primarily due to higher net sales from advertising, the App Store and cloud services. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136]
>
> The provided evidence blocks do not disclose Apple’s accounting treatment specifically for third-party application sales within the Services category. [AAPL FY2025, Item 8, AAPL_FY2025_2025-09-27:200] [AAPL FY2025, Item 8, AAPL_FY2025_2025-09-27:202]
>
> Apple does disclose that it sells its services through its various service platforms and also uses indirect distribution channels, such as third-party cellular network carriers and other resellers, for certain services. [AAPL FY2025, Item 1, AAPL_FY2025_2025-09-27:23]
>
> During 2025, the Company’s net sales through its direct and indirect distribution channels accounted for 40% and 60%, respectively, of total net sales. [AAPL FY2025, Item 1, AAPL_FY2025_2025-09-27:23]
>
> As to competitive pressures in its markets, the provided evidence blocks do not describe product-market competition directly, but they do state that Apple faces credit and collectibility risk because it distributes products and certain services through third-party cellular network carriers and other resellers, and a significant portion of trade receivables can be concentrated within those carriers or resellers. [AAPL FY2025, Item 1A, AAPL_FY2025_2025-09-27:100]
>
> Apple also states that its exposure to credit and collectibility risk on trade receivables is higher in certain international markets. [AAPL FY2025, Item 1A, AAPL_FY2025_2025-09-27:100]
>
> > [Guardrail Audit Warning]: Manual verification required; these numerical figures could not be matched in their cited chunks: 107.2, 96.2, 11.4%, 107.2, 96.2, 96.2; 1 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2025_2025-09-27:136` | Item 7 › Products and Services Performance | ✓ |  | (1)Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. iPhone iPhone net sales increased during 2025 compared to 2024 due to higher net sales of Pro m… |
| 2 | `AAPL_FY2025_2025-09-27:134` | Item 7 › Products and Services Performance | ✓ |  | The following table shows net sales by category for 2025, 2024 and 2023 (dollars in millions): |
| 3 | `AAPL_FY2025_2025-09-27:133` | Item 7 › Segment Operating Performance |  |  | Americas Americas net sales increased during 2025 compared to 2024 primarily due to higher net sales of iPhone and Services. The weakness in foreign currencies relative to the U.S. dollar had an unfavorable year-over-yea… |
| 4 | `AAPL_FY2025_2025-09-27:202` | Item 8 › Note 2 – Revenue | ✓ |  | (1)Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. The Company’s proportion of net sales by disaggregated revenue source was generally consistent … |
| 5 | `AAPL_FY2025_2025-09-27:200` | Item 8 › Note 2 – Revenue | ✓ |  | The following table shows disaggregated net sales, as well as the portion of total net sales that was previously deferred, for 2025, 2024 and 2023 (in millions): |
| 6 | `AAPL_FY2025_2025-09-27:273` | Item 8 › Note 13 – Segment Information and Geographic Data |  |  | \| \| 2025 \| 2024 \| 2023 \| \|---\|---\|---\|---\| \| Net sales: \| \| \| \| \| U.S. \| $151,790 \| $142,196 \| $138,573 \| \| China (1) \| 64,377 \| 66,952 \| 72,559 \| \| Other countries \| 199,994 \| 181,887 \| 172,153 \| \| Total net sales \| $41… |
| 7 | `AAPL_FY2025_2025-09-27:131` | Item 7 › Segment Operating Performance |  |  | The following table shows net sales by reportable segment for 2025, 2024 and 2023 (dollars in millions): |
| 8 | `AAPL_FY2025_2025-09-27:23` | Item 1 › Markets and Distribution | ✓ |  | The Company’s customers are primarily in the consumer, small and mid-sized business, education, enterprise and government markets. The Company sells its products and resells third-party products in most of its major mark… |
| 9 | `AAPL_FY2025_2025-09-27:100` | Item 1A › The Company is exposed to credit risk and fluctuations in the values of its investment portfolio. | ✓ |  | The Company distributes its products and certain of its services through third-party cellular network carriers and other resellers. The Company also sells its products and services directly to small and mid-sized busines… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2025_2025-09-27:136`** (cited)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Products and Services Performance
(1)Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. iPhone iPhone net sales increased during 2025 compared to 2024 due to higher net sales of Pro models. Mac Mac net sales increased during 2025 compared to 2024 primarily due to higher net sales of laptops and desktops. iPad iPad net sales increased during 2025 compared to 2024 primarily due to higher net sales of iPad Air, iPad mini and iPad, partially offset by lower net sales of iPad Pro. Wearables, Home and Accessories Wearables, Home and Accessories net sales decreased during 2025 compared to 2024 primarily due to lower net sales of Accessories and Wearables. Services Services net sales increased during 2025 compared to 2024 primarily due to higher net sales from advertising, the App Store and cloud services. Apple Inc. | 2025 Form 10-K | 23
````

**#2 `AAPL_FY2025_2025-09-27:134`** (cited)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Products and Services Performance
The following table shows net sales by category for 2025, 2024 and 2023 (dollars in millions):
````

**#4 `AAPL_FY2025_2025-09-27:202`** (cited)

````text
Item 8. Financial Statements and Supplementary Data > Note 2 – Revenue
(1)Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. The Company’s proportion of net sales by disaggregated revenue source was generally consistent for each reportable segment in Note 13, “Segment Information and Geographic Data” for 2025, 2024 and 2023, except in Greater China, where iPhone revenue represented a moderately higher proportion of net sales. As of September 27, 2025 and September 28, 2024, the Company had total deferred revenue of $13.7 billion and $12.8 billion, respectively. As of September 27, 2025, the Company expects 66% of total deferred revenue to be realized in less than a year, 23% within one-to-two years, 9% within two-to-three years and 2% in greater than three years.
````

**#5 `AAPL_FY2025_2025-09-27:200`** (cited)

````text
Item 8. Financial Statements and Supplementary Data > Note 2 – Revenue
The following table shows disaggregated net sales, as well as the portion of total net sales that was previously deferred, for 2025, 2024 and 2023 (in millions):
````

**#8 `AAPL_FY2025_2025-09-27:23`** (cited)

````text
Item 1. Business > Markets and Distribution
The Company’s customers are primarily in the consumer, small and mid-sized business, education, enterprise and government markets. The Company sells its products and resells third-party products in most of its major markets directly to customers through its retail and online stores and its direct sales force. The Company sells its services in the same markets through its various service platforms. The Company also employs a variety of indirect distribution channels, such as third-party cellular network carriers and other resellers, for the sale of its products and certain of its services. During 2025, the Company’s net sales through its direct and indirect distribution channels accounted for 40% and 60%, respectively, of total net sales.
````

**#9 `AAPL_FY2025_2025-09-27:100`** (cited)

````text
Item 1A. Risk Factors > The Company is exposed to credit risk and fluctuations in the values of its investment portfolio.
The Company distributes its products and certain of its services through third-party cellular network carriers and other resellers. The Company also sells its products and services directly to small and mid-sized businesses and education, enterprise and government customers. A substantial majority of the Company’s outstanding trade receivables are not covered by collateral, third-party bank support or financing arrangements, or credit insurance, and a significant portion of the Company’s trade receivables can be concentrated within cellular network carriers or other resellers. The Company’s exposure to credit and collectibility risk on its trade receivables is higher in certain international markets. The Company also has unsecured vendor non-trade receivables resulting from purchases of components by outsourcing partners and other vendors that manufacture subassemblies or assemble final products for the Company. In addition, the Company has made prepayments associated with long-term supply agreements to secure supply of inventory components. As of September 27, 2025, the Company’s vendor non-trade receivables were concentrated among a few individual vendors located primarily in Asia. If the Company is unable to monitor and limit exposure to credit risk on its trade and vendor non-trade receivables, as well as long-term prepayments, the Company’s results of operations, financial condition and stock
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 7'), ('AAPL', 'Item 8'), ('AAPL', 'Item 1'), ('AAPL', 'Item 1A')] gold=[(None, 'Item 8'), (None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 8, verified 2, ungrounded 6, uncited 0, derived 0; sentence verdicts: supported 5, partial 0, unsupported 0, unchecked 0.

- ungrounded numbers: 107.2, 96.2, 11.4%, 107.2, 96.2, 96.2

<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Apple’s Services net sales were $107.2 billion in fiscal 2025 and $96.2 billion in fiscal 2024, and the year-over-year growth was approximately 11.4% (($107.2 billion - $96.2 billion) / $96.2 billion). [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:134] [AAPL FY2025, Item 8, AAPL_FY2025_2025-09-27:200] | None |  |
| Apple states that Services net sales increased during 2025 compared to 2024 primarily due to higher net sales from advertising, the App Store and cloud services. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136] | supported | The evidence states verbatim that Services net sales increased in 2025 versus 2024 primarily due to advertising, the App Store and cloud services. |
| The provided evidence blocks do not disclose Apple’s accounting treatment specifically for third-party application sales within the Services category. [AAPL FY2025, Item 8, AAPL_FY2025_2025-09-27:200] [AAPL FY2025, Item 8, AAPL_FY2025_2025-09-27:202] | supported | These evidence blocks discuss disaggregated net sales and deferred revenue but do not mention accounting treatment for third-party application sales. |
| Apple does disclose that it sells its services through its various service platforms and also uses indirect distribution channels, such as third-party cellular network carriers and other resellers, for certain services. [AAPL FY2025, Item 1, AAPL_FY2025_2025-09-27:23] | supported | The evidence says Apple sells services through its service platforms and uses indirect channels such as carriers and resellers for certain services. |
| During 2025, the Company’s net sales through its direct and indirect distribution channels accounted for 40% and 60%, respectively, of total net sales. [AAPL FY2025, Item 1, AAPL_FY2025_2025-09-27:23] | None |  |
| As to competitive pressures in its markets, the provided evidence blocks do not describe product-market competition directly, but they do state that Apple faces credit and collectibility risk because it distributes products and certain services through third-party cellular network carriers and other resellers, and a significant portion of trade receivables can be concentrated within those carriers or resellers. [AAPL FY2025, Item 1A, AAPL_FY2025_2025-09-27:100] | supported | The cited block does not discuss product-market competition and does state the described credit and collectibility risks tied to carriers and resellers. |
| Apple also states that its exposure to credit and collectibility risk on trade receivables is higher in certain international markets. [AAPL FY2025, Item 1A, AAPL_FY2025_2025-09-27:100] | supported | The evidence explicitly states that exposure to credit and collectibility risk on trade receivables is higher in certain international markets. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 7, cited: 4.

**Generated answer**

> Apple’s Form 10-K provides net sales by category for 2025, 2024 and 2023, including Services, in the table referenced in Management’s Discussion and Analysis. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:134]
>
> Apple states that Services net sales increased during 2025 compared to 2024 primarily due to higher net sales from advertising, the App Store and cloud services. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136]
>
> The provided evidence does not include the actual 2025 and 2024 Services net sales figures from that table, so the year-over-year percentage growth cannot be calculated from the evidence provided here. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:134]
>
> Apple states that Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136] [AAPL FY2025, Item 8, AAPL_FY2025_2025-09-27:202]
>
> The provided evidence does not disclose how Apple accounts for third-party application sales within the Services category beyond noting that App Store sales contributed to Services growth. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136]
>
> In the Americas, Apple says net sales increased during 2025 compared to 2024 primarily due to higher net sales of iPhone and Services, and that weakness in foreign currencies relative to the U.S. dollar had an unfavorable year-over-year impact on Americas net sales during 2025. In Greater China, Apple says net sales decreased during 2025 compared to 2024 primarily due to lower net sales of iPhone, partially offset by higher net sales of Mac. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:133]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-AAPL-2025` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2025,2025-09-27,416161000000,112010000000,133050000000,3592410… |
| 2 | `AAPL_FY2025_2025-09-27:136` | Item 7 › Products and Services Performance | ✓ |  | (1)Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. iPhone iPhone net sales increased during 2025 compared to 2024 due to higher net sales of Pro m… |
| 3 | `AAPL_FY2025_2025-09-27:134` | Item 7 › Products and Services Performance | ✓ |  | The following table shows net sales by category for 2025, 2024 and 2023 (dollars in millions): |
| 4 | `AAPL_FY2025_2025-09-27:133` | Item 7 › Segment Operating Performance | ✓ |  | Americas Americas net sales increased during 2025 compared to 2024 primarily due to higher net sales of iPhone and Services. The weakness in foreign currencies relative to the U.S. dollar had an unfavorable year-over-yea… |
| 5 | `AAPL_FY2025_2025-09-27:202` | Item 8 › Note 2 – Revenue | ✓ |  | (1)Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. The Company’s proportion of net sales by disaggregated revenue source was generally consistent … |
| 6 | `AAPL_FY2025_2025-09-27:200` | Item 8 › Note 2 – Revenue |  |  | The following table shows disaggregated net sales, as well as the portion of total net sales that was previously deferred, for 2025, 2024 and 2023 (in millions): |
| 7 | `AAPL_FY2025_2025-09-27:273` | Item 8 › Note 13 – Segment Information and Geographic Data |  |  | \| \| 2025 \| 2024 \| 2023 \| \|---\|---\|---\|---\| \| Net sales: \| \| \| \| \| U.S. \| $151,790 \| $142,196 \| $138,573 \| \| China (1) \| 64,377 \| 66,952 \| 72,559 \| \| Other countries \| 199,994 \| 181,887 \| 172,153 \| \| Total net sales \| $41… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `AAPL_FY2025_2025-09-27:136`** (cited)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Products and Services Performance
(1)Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. iPhone iPhone net sales increased during 2025 compared to 2024 due to higher net sales of Pro models. Mac Mac net sales increased during 2025 compared to 2024 primarily due to higher net sales of laptops and desktops. iPad iPad net sales increased during 2025 compared to 2024 primarily due to higher net sales of iPad Air, iPad mini and iPad, partially offset by lower net sales of iPad Pro. Wearables, Home and Accessories Wearables, Home and Accessories net sales decreased during 2025 compared to 2024 primarily due to lower net sales of Accessories and Wearables. Services Services net sales increased during 2025 compared to 2024 primarily due to higher net sales from advertising, the App Store and cloud services. Apple Inc. | 2025 Form 10-K | 23
````

**#3 `AAPL_FY2025_2025-09-27:134`** (cited)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Products and Services Performance
The following table shows net sales by category for 2025, 2024 and 2023 (dollars in millions):
````

**#4 `AAPL_FY2025_2025-09-27:133`** (cited)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Segment Operating Performance
Americas Americas net sales increased during 2025 compared to 2024 primarily due to higher net sales of iPhone and Services. The weakness in foreign currencies relative to the U.S. dollar had an unfavorable year-over-year impact on Americas net sales during 2025. Europe Europe net sales increased during 2025 compared to 2024 primarily due to higher net sales of Services, iPhone and Mac. Greater China Greater China net sales decreased during 2025 compared to 2024 primarily due to lower net sales of iPhone, partially offset by higher net sales of Mac. Japan Japan net sales increased during 2025 compared to 2024 primarily due to higher net sales of iPhone, Services and iPad. Rest of Asia Pacific Rest of Asia Pacific net sales increased during 2025 compared to 2024 primarily due to higher net sales of iPhone, Services and Mac. Apple Inc. | 2025 Form 10-K | 22
````

**#5 `AAPL_FY2025_2025-09-27:202`** (cited)

````text
Item 8. Financial Statements and Supplementary Data > Note 2 – Revenue
(1)Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. The Company’s proportion of net sales by disaggregated revenue source was generally consistent for each reportable segment in Note 13, “Segment Information and Geographic Data” for 2025, 2024 and 2023, except in Greater China, where iPhone revenue represented a moderately higher proportion of net sales. As of September 27, 2025 and September 28, 2024, the Company had total deferred revenue of $13.7 billion and $12.8 billion, respectively. As of September 27, 2025, the Company expects 66% of total deferred revenue to be realized in less than a year, 23% within one-to-two years, 9% within two-to-three years and 2% in greater than three years.
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 7'), ('AAPL', 'Item 8')] gold=[(None, 'Item 8'), (None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 7, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Apple’s Form 10-K provides net sales by category for 2025, 2024 and 2023, including Services, in the table referenced in Management’s Discussion and Analysis. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:134] | supported | The evidence explicitly says a table shows net sales by category for 2025, 2024 and 2023 in Item 7. |
| Apple states that Services net sales increased during 2025 compared to 2024 primarily due to higher net sales from advertising, the App Store and cloud services. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136] | supported | The evidence states Services net sales increased in 2025 versus 2024 primarily due to advertising, the App Store and cloud services. |
| The provided evidence does not include the actual 2025 and 2024 Services net sales figures from that table, so the year-over-year percentage growth cannot be calculated from the evidence provided here. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:134] | supported | The cited excerpt only references the table and does not include the actual Services figures needed to calculate growth. |
| Apple states that Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136] [AAPL FY2025, Item 8, AAPL_FY2025_2025-09-27:202] | supported | Both cited excerpts explicitly state that Services net sales include amortization of deferred bundled services value. |
| The provided evidence does not disclose how Apple accounts for third-party application sales within the Services category beyond noting that App Store sales contributed to Services growth. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136] | supported | The evidence mentions App Store as a contributor to Services growth but gives no accounting treatment for third-party application sales. |
| In the Americas, Apple says net sales increased during 2025 compared to 2024 primarily due to higher net sales of iPhone and Services, and that weakness in foreign currencies relative to the U.S. dollar had an unfavorable year-over-year impact on Americas net sales during 2025. | supported | The retrieved evidence explicitly states both the Americas sales drivers and the unfavorable foreign currency impact. |
| In Greater China, Apple says net sales decreased during 2025 compared to 2024 primarily due to lower net sales of iPhone, partially offset by higher net sales of Mac. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:133] | supported | The cited evidence states Greater China net sales decreased primarily due to lower iPhone sales, partially offset by higher Mac sales. |

</details>
