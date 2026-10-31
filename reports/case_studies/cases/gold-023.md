# gold-023: Multi-hop text (one filing)

[← all cases](../README.md) · company: Apple Inc. (AAPL) · fiscal year: 2018 · recipe `text` · hop `multi` · answer type `qualitative` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> According to Apple's 2018 10-K, how do the specific risks associated with the company's retail store operations differ from the general risks associated with its international operations?

**Gold answer**

> The risks associated with Apple's retail stores are primarily operational and financial, stemming from the high cost structure of equipment, leasehold improvements, and leases, which can lead to significant termination costs and write-offs if sales decline or stores underperform. In contrast, the risks associated with international operations are regulatory and geopolitical, involving compliance with complex foreign laws (such as data privacy and anti-corruption), exposure to trade disputes, tariffs, and political instability, which can affect gross margins and brand reputation.

**Key points** (RQ3 keypoint_recall targets)

1. Retail store risks involve high fixed costs (equipment, leases) leading to potential write-offs and termination costs upon underperformance.
2. International operation risks involve compliance with diverse foreign laws, regulations, and geopolitical factors like trade disputes.
3. The retail risks are focused on operational/financial liabilities, while international risks focus on legal/regulatory compliance and market environment.

**Gold evidence**

1. `AAPL_FY2018_2018-09-29` · Item 1A. Risk Factors › The Company’s business is subject to the risks of international operations. · text

   > Due to the high cost structure associated with the Company’s retail stores, a decline in sales or the closure or poor performance of individual or multiple stores could result in significant lease termination costs, write-offs of equipment and leasehold improvements and severance costs.

2. `AAPL_FY2018_2018-09-29` · Item 1A. Risk Factors › The Company’s business is subject to the risks of international operations. · text

   > Compliance with applicable U.S. and foreign laws and regulations, such as import and export requirements, anti-corruption laws, tax laws, foreign exchange controls and cash repatriation restrictions, data privacy and data localization requirements, environmental laws, labor laws and anti-competition regulations, increases the costs of doing business in foreign jurisdictions.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 8 | 9 |
| recall@5 | 1.00 | 1.00 | 0.50 | 0.50 |
| recall@all | 1.00 | 1.00 | 1.00 | 0.50 |
| complete@all | 1 | 1 | 1 | 0 |
| average precision (lexical) | 0.46 | 0.42 | 0.39 | 0.50 |
| gold evidence first rank | #1: 2, #2: 4 | #1: 3, #2: 4 | #1: 2, #2: 7 | #1: 2, #2: – |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | – | – | – | – |
| keypoint_recall | 1.00 | 1.00 | 0.67 | 0.67 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 2456 | 1460 | 13865 | 13853 |
| cost (USD) | 0.0005 | 0.0004 | 0.0579 | 0.0586 |
| latency (s) | 5.4 | 8.9 | 31.7 | 35.2 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 5.

**Generated answer**

> According to Apple’s 2018 10-K, the risks differ as follows:
>
> - **Retail store operations risks** are tied to the economics and operation of the stores themselves. Apple highlights risks such as:
>   - macro-economic factors affecting retail activity,
>   - managing costs of **store construction and operation**,
>   - managing relationships with retail partners,
>   - fluctuations in the value of retail inventory,
>   - obtaining and renewing leases in quality locations at reasonable cost,
>   - the **substantial investment** required for equipment, leasehold improvements, information systems, inventory, and personnel,
>   - large **operating lease commitments**,
>   - and the possibility that declining sales or store closures/poor performance could lead to **lease termination costs, write-offs, and severance costs** [1][2].
>
> - **General international operations risks** are broader and relate to Apple’s global business exposure. These include:
>   - dependence on international revenue and supply chain activity,
>   - compliance with U.S. and foreign laws and regulations,
>   - import/export requirements, anti-corruption laws, tax laws, foreign exchange controls, cash repatriation restrictions, data privacy/localization, environmental, labor, and anti-competition laws,
>   - economic and labor conditions,
>   - increased duties, taxes, and other costs,
>   - political instability and international trade disputes,
>   - tariffs and antidumping penalties affecting margins,
>   - and credit/collectibility risk in certain international markets [3][4][6].
>
> In short, **retail store risks are operational and investment risks specific to running physical stores**, while **international operation risks are broader regulatory, economic, political, trade, and cross-border business risks affecting Apple’s global operations overall** [1][2][3][4][6].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2018_2018-09-29:83` | Item 1A › The Company’s business is subject to the risks of international operations. | ✓ |  | The Company’s retail operations are subject to many factors that pose risks and uncertainties and could adversely impact the Company’s financial condition and operating results, including macro-economic factors that coul… |
| 2 | `AAPL_FY2018_2018-09-29:82` | Item 1A › The Company’s business is subject to the risks of international operations. | ✓ | #1 | The Company’s retail stores have required substantial investment in equipment and leasehold improvements, information systems, inventory and personnel. The Company also has entered into substantial operating lease commit… |
| 3 | `AAPL_FY2018_2018-09-29:81` | Item 1A › The Company’s business is subject to the risks of international operations. | ✓ |  | The Company also could be significantly affected by other risks associated with international activities including, but not limited to, economic and labor conditions, increased duties, taxes and other costs, political in… |
| 4 | `AAPL_FY2018_2018-09-29:80` | Item 1A › The Company’s business is subject to the risks of international operations. | ✓ | #2 | The Company derives a majority of its revenue and earnings from its international operations. Compliance with applicable U.S. and foreign laws and regulations, such as import and export requirements, anti-corruption laws… |
| 5 | `AAPL_FY2018_2018-09-29:65` | Item 1A › Future operating results depend upon the Company’s ability to obtain components in sufficient quantities on commercially reasonable terms. |  |  | The Company relies on single-sourced outsourcing partners in the U.S., Asia and Europe to supply and manufacture many components, and on outsourcing partners primarily located in Asia, for final assembly of substantially… |
| 6 | `AAPL_FY2018_2018-09-29:51` | Item 1A | ✓ |  | Because of the following factors, as well as other factors affecting the Company’s financial condition and operating results, past financial performance should not be considered to be a reliable indicator of future perfo… |
| 7 | `AAPL_FY2018_2018-09-29:93` | Item 1A › The Company’s success depends largely on the continued service and availability of key personnel. |  |  | Many of the Company’s operations and facilities as well as critical business operations of the Company’s suppliers and contract manufacturers are in locations that are prone to earthquakes and other natural disasters. In… |
| 8 | `AAPL_FY2018_2018-09-29:77` | Item 1A › The Company could be impacted by unfavorable results of legal proceedings, such as being found to have infringed on intellectual property rights. |  | #2 | The Company is subject to laws and regulations affecting its domestic and international operations in a number of areas. These U.S. and foreign laws and regulations affect the Company’s activities in areas including, but… |
| 9 | `AAPL_FY2018_2018-09-29:68` | Item 1A › Future operating results depend upon the Company’s ability to obtain components in sufficient quantities on commercially reasonable terms. |  |  | and equipment, and/or intangible assets, and significant warranty and other expenses, including litigation costs and regulatory fines. Quality problems could also adversely affect the experience for users of the Company’… |
| 10 | `AAPL_FY2018_2018-09-29:54` | Item 1A |  |  | The Company’s ability to compete successfully depends heavily on its ability to ensure a continuing and timely introduction of innovative new products, services and technologies to the marketplace. The Company believes i… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2018_2018-09-29:83`** (cited)

````text
Item 1A. Risk Factors > The Company’s business is subject to the risks of international operations.
The Company’s retail operations are subject to many factors that pose risks and uncertainties and could adversely impact the Company’s financial condition and operating results, including macro-economic factors that could have an adverse effect on general retail activity. Other factors include, but are not limited to, the Company’s ability to manage costs associated with retail store construction and operation; manage relationships with existing retail partners; manage costs associated with fluctuations in the value of retail inventory; and obtain and renew leases in quality retail locations at a reasonable cost. Apple Inc. | 2018 Form 10-K | 13 Investment in new business strategies and acquisitions could disrupt the Company’s ongoing business and present risks not originally contemplated. The Company has invested, and in the future may invest, in new business strategies or acquisitions. Such endeavors may involve significant risks and uncertainties, including distraction of management from current operations, greater than expected liabilities and expenses, inadequate return of capital and unidentified issues not discovered in the Company’s due diligence. These new ventures are inherently risky and may not be successful.
````

**#2 `AAPL_FY2018_2018-09-29:82`** (cited, gold #1)

````text
Item 1A. Risk Factors > The Company’s business is subject to the risks of international operations.
The Company’s retail stores have required substantial investment in equipment and leasehold improvements, information systems, inventory and personnel. The Company also has entered into substantial operating lease commitments for retail space. Certain stores have been designed and built to serve as high-profile venues to promote brand awareness. Because of their unique design elements, locations and size, these stores require substantially more investment than the Company’s more typical retail stores. Due to the high cost structure associated with the Company’s retail stores, a decline in sales or the closure or poor performance of individual or multiple stores could result in significant lease termination costs, write-offs of equipment and leasehold improvements and severance costs.
````

**#3 `AAPL_FY2018_2018-09-29:81`** (cited)

````text
Item 1A. Risk Factors > The Company’s business is subject to the risks of international operations.
The Company also could be significantly affected by other risks associated with international activities including, but not limited to, economic and labor conditions, increased duties, taxes and other costs, political instability and international trade disputes. Gross margins on the Company’s products in foreign countries, and on products that include components obtained from foreign suppliers, could be materially adversely affected by international trade regulations, including duties, tariffs and antidumping penalties. The Company is also exposed to credit and collectibility risk on its trade receivables with customers in certain international markets. There can be no assurance the Company can effectively limit its credit risk and avoid losses. The Company’s retail stores have required and will continue to require a substantial investment and commitment of resources and are subject to numerous risks and uncertainties.
````

**#4 `AAPL_FY2018_2018-09-29:80`** (cited, gold #2)

````text
Item 1A. Risk Factors > The Company’s business is subject to the risks of international operations.
The Company derives a majority of its revenue and earnings from its international operations. Compliance with applicable U.S. and foreign laws and regulations, such as import and export requirements, anti-corruption laws, tax laws, foreign exchange controls and cash repatriation restrictions, data privacy and data localization requirements, environmental laws, labor laws and anti-competition regulations, increases the costs of doing business in foreign jurisdictions. Although the Company has implemented policies and procedures to comply with these laws and regulations, a violation by the Company’s employees, contractors or agents could nevertheless occur. In some cases, compliance with the laws and regulations of one country could violate the laws and regulations of another country. Violations of these laws and regulations could materially adversely affect the Company’s brand, international growth efforts and business.
````

**#6 `AAPL_FY2018_2018-09-29:51`** (cited)

````text
Item 1A. Risk Factors
Because of the following factors, as well as other factors affecting the Company’s financial condition and operating results, past financial performance should not be considered to be a reliable indicator of future performance, and investors should not use historical trends to anticipate results or trends in future periods. Global and regional economic conditions could materially adversely affect the Company’s business, results of operations, financial condition and growth. The Company has international operations with sales outside the U.S. representing a majority of the Company’s total net sales. In addition, a majority of the Company’s supply chain, and its manufacturing and assembly activities, are located outside the U.S. As a result, the Company’s operations and performance depend significantly on global and regional economic conditions.
````

**#8 `AAPL_FY2018_2018-09-29:77`** (gold #2)

````text
Item 1A. Risk Factors > The Company could be impacted by unfavorable results of legal proceedings, such as being found to have infringed on intellectual property rights.
The Company is subject to laws and regulations affecting its domestic and international operations in a number of areas. These U.S. and foreign laws and regulations affect the Company’s activities in areas including, but not limited to, labor, advertising, digital content, consumer protection, real estate, billing, e-commerce, promotions, quality of services, telecommunications, mobile communications and media, television, intellectual property ownership and infringement, tax, import and export requirements, anti-corruption, foreign exchange controls and cash repatriation restrictions, data privacy and data localization requirements, anti-competition, environmental, health and safety.
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 1A')] gold=[(None, 'Item 1A')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 4.

**Generated answer**

> Apple’s **retail store operation risks** are described as risks tied to running physical stores and their cost structure. These include:
>
> - macro-economic effects on retail activity,
> - managing costs of store construction and operation,
> - managing relationships with retail partners,
> - inventory value fluctuations,
> - obtaining and renewing leases in quality locations at reasonable cost,
> - substantial investments in equipment, leasehold improvements, systems, inventory, and personnel,
> - substantial operating lease commitments,
> - and the possibility that declining sales or store closures could lead to lease termination costs, write-offs, and severance costs [1][3].
>
> By contrast, the **general risks of international operations** relate to operating across foreign markets and jurisdictions. These include:
>
> - economic and labor conditions,
> - increased duties, taxes, and other costs,
> - political instability and international trade disputes,
> - adverse effects from trade regulations such as tariffs and antidumping penalties,
> - credit and collectibility risk in certain international markets,
> - and compliance risks from U.S. and foreign laws such as import/export rules, anti-corruption laws, tax laws, foreign exchange controls, cash repatriation restrictions, data privacy/localization requirements, environmental laws, labor laws, and anti-competition regulations [2][4].
>
> So, in short, **retail store risks are mainly operational and investment/lease-related risks specific to Apple’s store footprint**, while **international operation risks are broader cross-border economic, regulatory, trade, political, and credit risks affecting Apple’s global business** [1][2][3][4].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2018_2018-09-29:83` | Item 1A › The Company’s business is subject to the risks of international operations. | ✓ |  | The Company’s retail operations are subject to many factors that pose risks and uncertainties and could adversely impact the Company’s financial condition and operating results, including macro-economic factors that coul… |
| 2 | `AAPL_FY2018_2018-09-29:81` | Item 1A › The Company’s business is subject to the risks of international operations. | ✓ |  | The Company also could be significantly affected by other risks associated with international activities including, but not limited to, economic and labor conditions, increased duties, taxes and other costs, political in… |
| 3 | `AAPL_FY2018_2018-09-29:82` | Item 1A › The Company’s business is subject to the risks of international operations. | ✓ | #1 | The Company’s retail stores have required substantial investment in equipment and leasehold improvements, information systems, inventory and personnel. The Company also has entered into substantial operating lease commit… |
| 4 | `AAPL_FY2018_2018-09-29:80` | Item 1A › The Company’s business is subject to the risks of international operations. | ✓ | #2 | The Company derives a majority of its revenue and earnings from its international operations. Compliance with applicable U.S. and foreign laws and regulations, such as import and export requirements, anti-corruption laws… |
| 5 | `AAPL_FY2018_2018-09-29:93` | Item 1A › The Company’s success depends largely on the continued service and availability of key personnel. |  |  | Many of the Company’s operations and facilities as well as critical business operations of the Company’s suppliers and contract manufacturers are in locations that are prone to earthquakes and other natural disasters. In… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2018_2018-09-29:83`** (cited)

````text
Item 1A. Risk Factors > The Company’s business is subject to the risks of international operations.
The Company’s retail operations are subject to many factors that pose risks and uncertainties and could adversely impact the Company’s financial condition and operating results, including macro-economic factors that could have an adverse effect on general retail activity. Other factors include, but are not limited to, the Company’s ability to manage costs associated with retail store construction and operation; manage relationships with existing retail partners; manage costs associated with fluctuations in the value of retail inventory; and obtain and renew leases in quality retail locations at a reasonable cost. Apple Inc. | 2018 Form 10-K | 13 Investment in new business strategies and acquisitions could disrupt the Company’s ongoing business and present risks not originally contemplated. The Company has invested, and in the future may invest, in new business strategies or acquisitions. Such endeavors may involve significant risks and uncertainties, including distraction of management from current operations, greater than expected liabilities and expenses, inadequate return of capital and unidentified issues not discovered in the Company’s due diligence. These new ventures are inherently risky and may not be successful.
````

**#2 `AAPL_FY2018_2018-09-29:81`** (cited)

````text
Item 1A. Risk Factors > The Company’s business is subject to the risks of international operations.
The Company also could be significantly affected by other risks associated with international activities including, but not limited to, economic and labor conditions, increased duties, taxes and other costs, political instability and international trade disputes. Gross margins on the Company’s products in foreign countries, and on products that include components obtained from foreign suppliers, could be materially adversely affected by international trade regulations, including duties, tariffs and antidumping penalties. The Company is also exposed to credit and collectibility risk on its trade receivables with customers in certain international markets. There can be no assurance the Company can effectively limit its credit risk and avoid losses. The Company’s retail stores have required and will continue to require a substantial investment and commitment of resources and are subject to numerous risks and uncertainties.
````

**#3 `AAPL_FY2018_2018-09-29:82`** (cited, gold #1)

````text
Item 1A. Risk Factors > The Company’s business is subject to the risks of international operations.
The Company’s retail stores have required substantial investment in equipment and leasehold improvements, information systems, inventory and personnel. The Company also has entered into substantial operating lease commitments for retail space. Certain stores have been designed and built to serve as high-profile venues to promote brand awareness. Because of their unique design elements, locations and size, these stores require substantially more investment than the Company’s more typical retail stores. Due to the high cost structure associated with the Company’s retail stores, a decline in sales or the closure or poor performance of individual or multiple stores could result in significant lease termination costs, write-offs of equipment and leasehold improvements and severance costs.
````

**#4 `AAPL_FY2018_2018-09-29:80`** (cited, gold #2)

````text
Item 1A. Risk Factors > The Company’s business is subject to the risks of international operations.
The Company derives a majority of its revenue and earnings from its international operations. Compliance with applicable U.S. and foreign laws and regulations, such as import and export requirements, anti-corruption laws, tax laws, foreign exchange controls and cash repatriation restrictions, data privacy and data localization requirements, environmental laws, labor laws and anti-competition regulations, increases the costs of doing business in foreign jurisdictions. Although the Company has implemented policies and procedures to comply with these laws and regulations, a violation by the Company’s employees, contractors or agents could nevertheless occur. In some cases, compliance with the laws and regulations of one country could violate the laws and regulations of another country. Violations of these laws and regulations could materially adversely affect the Company’s brand, international growth efforts and business.
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 1A')] gold=[(None, 'Item 1A')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 8, cited: 4.

**Generated answer**

> Apple’s retail store operations are described as requiring substantial investment in equipment and leasehold improvements, information systems, inventory and personnel, along with substantial operating lease commitments for retail space, which creates a high cost structure for those stores [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:82].  
>
> Apple states that some stores are high-profile venues with unique design elements, locations and size, and therefore require substantially more investment than more typical retail stores [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:82].  
>
> Because of this retail-specific cost structure, Apple says a decline in sales or the closure or poor performance of individual or multiple stores could result in significant lease termination costs, write-offs of equipment and leasehold improvements and severance costs [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:82].  
>
> Apple also says its retail operations are exposed to macro-economic factors that could adversely affect general retail activity, as well as risks tied to managing retail store construction and operating costs, relationships with existing retail partners, fluctuations in the value of retail inventory, and obtaining and renewing leases in quality retail locations at a reasonable cost [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:83].  
>
> By contrast, the general risks associated with Apple’s international operations relate to the fact that the Company derives a majority of its revenue and earnings from international operations and faces increased costs and compliance burdens from U.S. and foreign laws and regulations, including import and export requirements, anti-corruption laws, tax laws, foreign exchange controls, cash repatriation restrictions, data privacy and data localization requirements, environmental laws, labor laws and anti-competition regulations [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:80].  
>
> Apple further says international operations expose it to risks including economic and labor conditions, increased duties, taxes and other costs, political instability and international trade disputes [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:81].  
>
> Apple also notes that gross margins on products sold in foreign countries, and on products that include components obtained from foreign suppliers, could be materially adversely affected by international trade regulations, including duties, tariffs and antidumping penalties [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:81].  
>
> In addition, Apple says it is exposed to credit and collectibility risk on trade receivables with customers in certain international markets [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:81].  
>
> So, the retail store risks are mainly operational and asset-intensive risks tied to store investment, leases, store performance and retail cost management, while the international operation risks are broader cross-border compliance, trade, political, economic and credit risks arising from doing business globally [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:83] [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:82] [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:81] [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:80].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2018_2018-09-29:83` | Item 1A › The Company’s business is subject to the risks of international operations. | ✓ |  | The Company’s retail operations are subject to many factors that pose risks and uncertainties and could adversely impact the Company’s financial condition and operating results, including macro-economic factors that coul… |
| 2 | `AAPL_FY2018_2018-09-29:82` | Item 1A › The Company’s business is subject to the risks of international operations. | ✓ | #1 | The Company’s retail stores have required substantial investment in equipment and leasehold improvements, information systems, inventory and personnel. The Company also has entered into substantial operating lease commit… |
| 3 | `AAPL_FY2018_2018-09-29:59` | Item 1A › The Company depends on the performance of carriers, wholesalers, retailers and other resellers. |  |  | Apple Inc. \| 2018 Form 10-K \| 9 |
| 4 | `AAPL_FY2018_2018-09-29:50` | Item 1A |  |  | The following discussion of risk factors contains forward-looking statements. These risk factors may be important to understanding other statements in this Form 10-K. The following information should be read in conjuncti… |
| 5 | `AAPL_FY2018_2018-09-29:81` | Item 1A › The Company’s business is subject to the risks of international operations. | ✓ |  | The Company also could be significantly affected by other risks associated with international activities including, but not limited to, economic and labor conditions, increased duties, taxes and other costs, political in… |
| 6 | `AAPL_FY2018_2018-09-29:62` | Item 1A › Future operating results depend upon the Company’s ability to obtain components in sufficient quantities on commercially reasonable terms. |  |  | Because the Company currently obtains certain components from single or limited sources, the Company is subject to significant supply and pricing risks. Many components, including those that are available from multiple s… |
| 7 | `AAPL_FY2018_2018-09-29:80` | Item 1A › The Company’s business is subject to the risks of international operations. | ✓ | #2 | The Company derives a majority of its revenue and earnings from its international operations. Compliance with applicable U.S. and foreign laws and regulations, such as import and export requirements, anti-corruption laws… |
| 8 | `AAPL_FY2018_2018-09-29:61` | Item 1A › The Company faces substantial inventory and other asset risk in addition to purchase commitment cancellation risk. |  |  | The Company orders components for its products and builds inventory in advance of product announcements and shipments. Manufacturing purchase obligations cover the Company’s forecasted component and manufacturing require… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2018_2018-09-29:83`** (cited)

````text
Item 1A. Risk Factors > The Company’s business is subject to the risks of international operations.
The Company’s retail operations are subject to many factors that pose risks and uncertainties and could adversely impact the Company’s financial condition and operating results, including macro-economic factors that could have an adverse effect on general retail activity. Other factors include, but are not limited to, the Company’s ability to manage costs associated with retail store construction and operation; manage relationships with existing retail partners; manage costs associated with fluctuations in the value of retail inventory; and obtain and renew leases in quality retail locations at a reasonable cost. Apple Inc. | 2018 Form 10-K | 13 Investment in new business strategies and acquisitions could disrupt the Company’s ongoing business and present risks not originally contemplated. The Company has invested, and in the future may invest, in new business strategies or acquisitions. Such endeavors may involve significant risks and uncertainties, including distraction of management from current operations, greater than expected liabilities and expenses, inadequate return of capital and unidentified issues not discovered in the Company’s due diligence. These new ventures are inherently risky and may not be successful.
````

**#2 `AAPL_FY2018_2018-09-29:82`** (cited, gold #1)

````text
Item 1A. Risk Factors > The Company’s business is subject to the risks of international operations.
The Company’s retail stores have required substantial investment in equipment and leasehold improvements, information systems, inventory and personnel. The Company also has entered into substantial operating lease commitments for retail space. Certain stores have been designed and built to serve as high-profile venues to promote brand awareness. Because of their unique design elements, locations and size, these stores require substantially more investment than the Company’s more typical retail stores. Due to the high cost structure associated with the Company’s retail stores, a decline in sales or the closure or poor performance of individual or multiple stores could result in significant lease termination costs, write-offs of equipment and leasehold improvements and severance costs.
````

**#5 `AAPL_FY2018_2018-09-29:81`** (cited)

````text
Item 1A. Risk Factors > The Company’s business is subject to the risks of international operations.
The Company also could be significantly affected by other risks associated with international activities including, but not limited to, economic and labor conditions, increased duties, taxes and other costs, political instability and international trade disputes. Gross margins on the Company’s products in foreign countries, and on products that include components obtained from foreign suppliers, could be materially adversely affected by international trade regulations, including duties, tariffs and antidumping penalties. The Company is also exposed to credit and collectibility risk on its trade receivables with customers in certain international markets. There can be no assurance the Company can effectively limit its credit risk and avoid losses. The Company’s retail stores have required and will continue to require a substantial investment and commitment of resources and are subject to numerous risks and uncertainties.
````

**#7 `AAPL_FY2018_2018-09-29:80`** (cited, gold #2)

````text
Item 1A. Risk Factors > The Company’s business is subject to the risks of international operations.
The Company derives a majority of its revenue and earnings from its international operations. Compliance with applicable U.S. and foreign laws and regulations, such as import and export requirements, anti-corruption laws, tax laws, foreign exchange controls and cash repatriation restrictions, data privacy and data localization requirements, environmental laws, labor laws and anti-competition regulations, increases the costs of doing business in foreign jurisdictions. Although the Company has implemented policies and procedures to comply with these laws and regulations, a violation by the Company’s employees, contractors or agents could nevertheless occur. In some cases, compliance with the laws and regulations of one country could violate the laws and regulations of another country. Violations of these laws and regulations could materially adversely affect the Company’s brand, international growth efforts and business.
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 1A')] gold=[(None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 9, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Apple’s retail store operations are described as requiring substantial investment in equipment and leasehold improvements, information systems, inventory and personnel, along with substantial operating lease commitments for retail space, which creates a high cost structure for those stores [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:82]. | supported | The evidence states these investments and lease commitments create a high cost structure for retail stores. |
| Apple states that some stores are high-profile venues with unique design elements, locations and size, and therefore require substantially more investment than more typical retail stores [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:82]. | supported | The evidence explicitly says certain high-profile stores with unique design, location, and size require substantially more investment. |
| Because of this retail-specific cost structure, Apple says a decline in sales or the closure or poor performance of individual or multiple stores could result in significant lease termination costs, write-offs of equipment and leasehold improvements and severance costs [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:82]. | supported | The evidence directly links the retail stores’ high cost structure to potential lease termination costs, write-offs, and severance costs. |
| Apple also says its retail operations are exposed to macro-economic factors that could adversely affect general retail activity, as well as risks tied to managing retail store construction and operating costs, relationships with existing retail partners, fluctuations in the value of retail inventory, and obtaining and renewing leases in quality retail locations at a reasonable cost [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:83]. | supported | The evidence lists each of these retail-operation risk factors, including macro-economic effects, cost management, partner relationships, inventory value fluctuations, and leases. |
| By contrast, the general risks associated with Apple’s international operations relate to the fact that the Company derives a majority of its revenue and earnings from international operations and faces increased costs and compliance burdens from U.S. and foreign laws and regulations, including import and export requirements, anti-corruption laws, tax laws, foreign exchange controls, cash repatriation restrictions, data privacy and data localization requirements, environmental laws, labor laws and anti-competition regulations [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:80]. | supported | The evidence states Apple derives a majority of revenue and earnings internationally and lists the cited compliance burdens and laws. |
| Apple further says international operations expose it to risks including economic and labor conditions, increased duties, taxes and other costs, political instability and international trade disputes [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:81]. | supported | The evidence explicitly lists economic and labor conditions, increased duties and taxes, political instability, and trade disputes as international risks. |
| Apple also notes that gross margins on products sold in foreign countries, and on products that include components obtained from foreign suppliers, could be materially adversely affected by international trade regulations, including duties, tariffs and antidumping penalties [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:81]. | supported | The evidence directly states gross margins could be materially adversely affected by international trade regulations including duties, tariffs, and antidumping penalties. |
| In addition, Apple says it is exposed to credit and collectibility risk on trade receivables with customers in certain international markets [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:81]. | supported | The evidence explicitly says Apple is exposed to credit and collectibility risk on trade receivables in certain international markets. |
| So, the retail store risks are mainly operational and asset-intensive risks tied to store investment, leases, store performance and retail cost management, while the international operation risks are broader cross-border compliance, trade, political, economic and credit risks arising from doing business globally [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:83] [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:82] [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:81] [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:80]. | supported | Taken together, the cited evidence supports this contrast between retail operational/asset risks and broader international compliance, trade, political, economic, and credit risks. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 9, cited: 3.

**Generated answer**

> Apple’s general international operations risks relate to external cross-border factors such as economic and labor conditions, increased duties, taxes and other costs, political instability, international trade disputes, and trade regulations including duties, tariffs and antidumping penalties that could materially adversely affect gross margins. [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:81]
>
> Its international operations also expose Apple to credit and collectibility risk on trade receivables with customers in certain international markets, and the filing states there can be no assurance Apple can effectively limit this credit risk and avoid losses. [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:81]
>
> By contrast, the specific risks tied to retail store operations are more operational and asset-intensive, because the stores have required substantial investment in equipment, leasehold improvements, information systems, inventory and personnel, and Apple has entered into substantial operating lease commitments for retail space. [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:82]
>
> The filing further notes that certain stores are high-profile venues with unique design elements, locations and size, and therefore require substantially more investment than more typical retail stores. [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:82]
>
> Because of this high retail store cost structure, a decline in sales or the closure or poor performance of individual or multiple stores could result in significant lease termination costs, write-offs of equipment and leasehold improvements, and severance costs. [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:82]
>
> Apple also says its retail operations are subject to macro-economic factors that could adversely affect general retail activity, as well as risks around managing store construction and operating costs, relationships with existing retail partners, fluctuations in the value of retail inventory, and obtaining and renewing leases in quality retail locations at a reasonable cost. [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:83]
>
> So, in the 2018 10-K, international operations risks are described mainly as broad geopolitical, regulatory, economic and cross-border credit risks, while retail store risks are described mainly as store-specific investment, lease, cost management, inventory and operating performance risks. [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:83] [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:82] [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:81]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2018_2018-09-29:83` | Item 1A › The Company’s business is subject to the risks of international operations. | ✓ |  | The Company’s retail operations are subject to many factors that pose risks and uncertainties and could adversely impact the Company’s financial condition and operating results, including macro-economic factors that coul… |
| 2 | `AAPL_FY2018_2018-09-29:82` | Item 1A › The Company’s business is subject to the risks of international operations. | ✓ | #1 | The Company’s retail stores have required substantial investment in equipment and leasehold improvements, information systems, inventory and personnel. The Company also has entered into substantial operating lease commit… |
| 3 | `AAPL_FY2018_2018-09-29:81` | Item 1A › The Company’s business is subject to the risks of international operations. | ✓ |  | The Company also could be significantly affected by other risks associated with international activities including, but not limited to, economic and labor conditions, increased duties, taxes and other costs, political in… |
| 4 | `AAPL_FY2018_2018-09-29:59` | Item 1A › The Company depends on the performance of carriers, wholesalers, retailers and other resellers. |  |  | Apple Inc. \| 2018 Form 10-K \| 9 |
| 5 | `AAPL_FY2018_2018-09-29:94` | Item 1A › The Company’s success depends largely on the continued service and availability of key personnel. |  |  | The Company’s operations are also subject to the risks of industrial accidents at its suppliers and contract manufacturers. While the Company’s suppliers are required to maintain safe working environments and operations,… |
| 6 | `AAPL_FY2018_2018-09-29:58` | Item 1A › The Company depends on the performance of carriers, wholesalers, retailers and other resellers. |  |  | The Company distributes its products through cellular network carriers, wholesalers, retailers and resellers, many of whom distribute products from competing manufacturers. The Company also sells its products and third-p… |
| 7 | `AAPL_FY2018_2018-09-29:50` | Item 1A |  |  | The following discussion of risk factors contains forward-looking statements. These risk factors may be important to understanding other statements in this Form 10-K. The following information should be read in conjuncti… |
| 8 | `AAPL_FY2018_2018-09-29:13` | TABLE OF CONTENTS |  |  | \| \| \| Page \| \|---\|---\|---\| \| Part I \| \| \| \| Item 1. \| Business \| 1 \| \| Item 1A. \| Risk Factors \| 8 \| \| Item 1B. \| Unresolved Staff Comments \| 17 \| \| Item 2. \| Properties \| 18 \| \| Item 3. \| Legal Proceedings \| 18 \| \| Item… |
| 9 | `AAPL_FY2018_2018-09-29:61` | Item 1A › The Company faces substantial inventory and other asset risk in addition to purchase commitment cancellation risk. |  |  | The Company orders components for its products and builds inventory in advance of product announcements and shipments. Manufacturing purchase obligations cover the Company’s forecasted component and manufacturing require… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2018_2018-09-29:83`** (cited)

````text
Item 1A. Risk Factors > The Company’s business is subject to the risks of international operations.
The Company’s retail operations are subject to many factors that pose risks and uncertainties and could adversely impact the Company’s financial condition and operating results, including macro-economic factors that could have an adverse effect on general retail activity. Other factors include, but are not limited to, the Company’s ability to manage costs associated with retail store construction and operation; manage relationships with existing retail partners; manage costs associated with fluctuations in the value of retail inventory; and obtain and renew leases in quality retail locations at a reasonable cost. Apple Inc. | 2018 Form 10-K | 13 Investment in new business strategies and acquisitions could disrupt the Company’s ongoing business and present risks not originally contemplated. The Company has invested, and in the future may invest, in new business strategies or acquisitions. Such endeavors may involve significant risks and uncertainties, including distraction of management from current operations, greater than expected liabilities and expenses, inadequate return of capital and unidentified issues not discovered in the Company’s due diligence. These new ventures are inherently risky and may not be successful.
````

**#2 `AAPL_FY2018_2018-09-29:82`** (cited, gold #1)

````text
Item 1A. Risk Factors > The Company’s business is subject to the risks of international operations.
The Company’s retail stores have required substantial investment in equipment and leasehold improvements, information systems, inventory and personnel. The Company also has entered into substantial operating lease commitments for retail space. Certain stores have been designed and built to serve as high-profile venues to promote brand awareness. Because of their unique design elements, locations and size, these stores require substantially more investment than the Company’s more typical retail stores. Due to the high cost structure associated with the Company’s retail stores, a decline in sales or the closure or poor performance of individual or multiple stores could result in significant lease termination costs, write-offs of equipment and leasehold improvements and severance costs.
````

**#3 `AAPL_FY2018_2018-09-29:81`** (cited)

````text
Item 1A. Risk Factors > The Company’s business is subject to the risks of international operations.
The Company also could be significantly affected by other risks associated with international activities including, but not limited to, economic and labor conditions, increased duties, taxes and other costs, political instability and international trade disputes. Gross margins on the Company’s products in foreign countries, and on products that include components obtained from foreign suppliers, could be materially adversely affected by international trade regulations, including duties, tariffs and antidumping penalties. The Company is also exposed to credit and collectibility risk on its trade receivables with customers in certain international markets. There can be no assurance the Company can effectively limit its credit risk and avoid losses. The Company’s retail stores have required and will continue to require a substantial investment and commitment of resources and are subject to numerous risks and uncertainties.
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 1A')] gold=[(None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 7, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Apple’s general international operations risks relate to external cross-border factors such as economic and labor conditions, increased duties, taxes and other costs, political instability, international trade disputes, and trade regulations including duties, tariffs and antidumping penalties that could materially adversely affect gross margins. [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:81] | supported | The cited text expressly lists those international risks and says trade regulations could materially adversely affect gross margins. |
| Its international operations also expose Apple to credit and collectibility risk on trade receivables with customers in certain international markets, and the filing states there can be no assurance Apple can effectively limit this credit risk and avoid losses. [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:81] | supported | The evidence directly states exposure to credit and collectibility risk and that there is no assurance Apple can limit it and avoid losses. |
| By contrast, the specific risks tied to retail store operations are more operational and asset-intensive, because the stores have required substantial investment in equipment, leasehold improvements, information systems, inventory and personnel, and Apple has entered into substantial operating lease commitments for retail space. [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:82] | supported | The evidence states the stores required substantial investment in those assets and personnel and that Apple entered substantial operating lease commitments. |
| The filing further notes that certain stores are high-profile venues with unique design elements, locations and size, and therefore require substantially more investment than more typical retail stores. [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:82] | supported | The cited passage says certain stores are high-profile venues with unique design, locations, and size requiring substantially more investment. |
| Because of this high retail store cost structure, a decline in sales or the closure or poor performance of individual or multiple stores could result in significant lease termination costs, write-offs of equipment and leasehold improvements, and severance costs. [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:82] | supported | The evidence directly states that due to the high retail store cost structure, those outcomes could result from declining sales or poor store performance. |
| Apple also says its retail operations are subject to macro-economic factors that could adversely affect general retail activity, as well as risks around managing store construction and operating costs, relationships with existing retail partners, fluctuations in the value of retail inventory, and obtaining and renewing leases in quality retail locations at a reasonable cost. [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:83] | supported | The cited text explicitly lists macro-economic retail factors and the specified cost, partner, inventory, and lease risks. |
| So, in the 2018 10-K, international operations risks are described mainly as broad geopolitical, regulatory, economic and cross-border credit risks, while retail store risks are described mainly as store-specific investment, lease, cost management, inventory and operating performance risks. [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:83] [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:82] [AAPL FY2018, Item 1A, AAPL_FY2018_2018-09-29:81] | supported | Across the cited passages, international risks are described as economic, political, regulatory, and credit-related, while retail risks are store investment, lease, cost, inventory, and performance-related. |

</details>
