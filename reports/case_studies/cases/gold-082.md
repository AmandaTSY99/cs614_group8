# gold-082: Cross-year text

[← all cases](../README.md) · company: Walmart Inc. (WMT) · fiscal year: 2021 · recipe `cross_year_text` · hop `multi` · answer type `qualitative` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> How did the geographic scope of Walmart's operations and its treatment of international segments change between fiscal 2017 and fiscal 2021, specifically regarding the countries where it operated and the status of its U.K. and Japan operations?

**Gold answer**

> In fiscal 2017, Walmart operated retail, wholesale and other units in the U.S., Africa, Argentina, Brazil, Canada, Central America, Chile, China, India, Japan, Mexico and the United Kingdom. By fiscal 2021 it had sold Walmart Argentina (November 2020) and the majority stake of Walmart Brazil (fiscal 2019), and its U.K. and Japan operations were classified as held for sale as of January 31, 2021. Its remaining operations were in the U.S., Africa, Canada, Central America, Chile, China, India and Mexico.

**Key points** (RQ3 keypoint_recall targets)

1. In fiscal 2017, Walmart operated in Argentina, Brazil, Japan, and the U.K.
2. By fiscal 2021, Walmart had sold its operations in Argentina and Brazil
3. In fiscal 2021, the U.K. and Japan operations were classified as held for sale
4. The remaining operational locations in fiscal 2021 included the U.S., Africa, Canada, Central America, Chile, China, India, and Mexico

**Gold evidence**

1. `WMT_FY2021_2021-01-31` · ITEM 1. BUSINESS › Information About Our Segments · text

   > We are engaged in global operations of retail, wholesale and other units, as well as eCommerce, located throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico.

2. `WMT_FY2021_2021-01-31` · ITEM 1. BUSINESS › Information About Our Segments · text

   > The Company also engaged in operations in the U.K. and Japan, both of which were classified as held for sale as of January 31, 2021.

3. `WMT_FY2021_2021-01-31` · ITEM 1. BUSINESS › Information About Our Segments · text

   > We also operated in Argentina and Brazil prior to the sale of Walmart Argentina in November 2020 and the majority stake of Walmart Brazil in fiscal 2019.

4. `WMT_FY2017_2017-01-31` · ITEM 1. BUSINESS › Information About Our Segments · text

   > The Company is engaged in the operation of retail, wholesale and other units located throughout the U.S., Africa, Argentina, Brazil, Canada, Central America, Chile, China, India, Japan, Mexico and the United Kingdom and retail websites in the U.S. and 10 other countries.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 10 | 9 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.92 | 1.00 | 0.81 | 0.83 |
| gold evidence first rank | #1: 1, #2: 1, #3: 1, #4: 1 | #1: 1, #2: 2, #3: 2, #4: 1 | #1: 1, #2: 1, #3: 1, #4: 1 | #1: 1, #2: 1, #3: 1, #4: 1 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | 1.00 | 1.00 | 1.00 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 0.50 | 0.50 | 0.50 | 0.50 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 0.67 | 0.67 | 0.67 | 0.67 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 2 | 2 |
| tokens | 2902 | 1685 | 14292 | 26122 |
| cost (USD) | 0.0006 | 0.0004 | 0.0550 | 0.0996 |
| latency (s) | 5.2 | 8.8 | 21.3 | 38.2 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 5.

**Generated answer**

> Between fiscal 2017 and fiscal 2021, Walmart’s geographic scope narrowed somewhat and the treatment of certain international operations changed.
>
> - In fiscal 2017, Walmart said it operated in the U.S., Africa, Argentina, Brazil, Canada, Central America, Chile, China, India, Japan, Mexico, and the United Kingdom, with Walmart International consisting of operations in 27 countries outside the U.S. [4][9]
> - By fiscal 2021, Walmart said it operated throughout the U.S., Africa, Canada, Central America, Chile, China, India, and Mexico, and noted that it had previously operated in Argentina and Brazil but had sold Walmart Argentina in November 2020 and the majority stake of Walmart Brazil in fiscal 2019. [1][2][3]
> - Walmart International in fiscal 2021 was described as operating in 25 countries outside the U.S. as of January 31, 2021. [3]
>
> Regarding the U.K. and Japan:
>
> - In fiscal 2017, the U.K. and Japan were part of Walmart International’s operating footprint through wholly owned subsidiaries. [4]
> - In fiscal 2021, Walmart said its operations in both the U.K. and Japan were classified as held for sale as of January 31, 2021. [1][2]
> - It further stated these businesses were subsequently sold in February 2021 and March 2021, respectively. [2]
>
> So, the main changes were that Walmart exited Argentina and Brazil before or during this period, reducing Walmart International from 27 to 25 countries, and its U.K. and Japan operations shifted from active wholly owned international operations in 2017 to held-for-sale assets by January 31, 2021, before being sold shortly afterward. [3][4][9][2]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `WMT_FY2021_2021-01-31:26` | Item 1 › Information About Our Segments | ✓ | #1, #2, #3, #4 | We are engaged in global operations of retail, wholesale and other units, as well as eCommerce, located throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico. The Company also engaged in op… |
| 2 | `WMT_FY2021_2021-01-31:426` | Item 8 › Note 13. Segments and Disaggregated Revenue | ✓ | #1, #2, #3, #4 | Segments The Company is engaged in the operation of retail, wholesale and other units, as well as eCommerce websites, located throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico. The Comp… |
| 3 | `WMT_FY2021_2021-01-31:35` | Item 1 › Walmart International Segment | ✓ | #2, #3 | Walmart International is our second largest segment and operated in 25 countries outside of the U.S as of January 31, 2021. Walmart International operated through our wholly-owned subsidiaries in Canada, Chile, and China… |
| 4 | `WMT_FY2017_2017-01-31:42` | Item 1 › Walmart International Segment | ✓ | #1, #4 | The Walmart International segment consists of operations in 27 countries outside of the U.S. and includes numerous formats divided into three major categories: retail, wholesale and other. These categories consist of num… |
| 5 | `WMT_FY2021_2021-01-31:136` | Item 2 › International |  |  | The Walmart International segment comprises the Company's operations outside of the U.S. Unit counts as of January 31, 2021(1) for Walmart International are summarized by major category for each geographic market as foll… |
| 6 | `WMT_FY2021_2021-01-31:41` | Item 1 › Walmart International Segment |  | #1, #2 | Distribution. We utilize a total of 221 distribution facilities located in Canada, Central America, Chile, China, India, Mexico and South Africa, as well as Japan and the United Kingdom, whose operations are classified a… |
| 7 | `WMT_FY2021_2021-01-31:39` | Item 1 › Walmart International Segment |  |  | Walmart International also offers fuel, financial services and related products in various markets. Our businesses in Mexico and Canada, for example, offer prepaid cards and money (wire) transfers, and our PhonePe busine… |
| 8 | `WMT_FY2021_2021-01-31:207` | Item 7 › Walmart International Segment |  |  | Operating expenses as a percentage of segment net sales increased 14 basis points and decreased 13 basis points for fiscal 2021 and 2020, respectively, when compared to the previous fiscal year. The increase in operating… |
| 9 | `WMT_FY2017_2017-01-31:25` | Item 1 › Information About Our Segments | ✓ | #1, #4 | The Company is engaged in the operation of retail, wholesale and other units located throughout the U.S., Africa, Argentina, Brazil, Canada, Central America, Chile, China, India, Japan, Mexico and the United Kingdom and … |
| 10 | `WMT_FY2021_2021-01-31:202` | Item 7 › Walmart U.S. Segment |  |  | Operating expenses as a percentage of segment net sales decreased 15 and 4 basis points for fiscal 2021 and 2020, respectively, when compared to the previous fiscal year. We leveraged operating expenses in fiscal 2021 pr… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `WMT_FY2021_2021-01-31:26`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
ITEM 1. BUSINESS > Information About Our Segments
We are engaged in global operations of retail, wholesale and other units, as well as eCommerce, located throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico. The Company also engaged in operations in the U.K. and Japan, both of which were classified as held for sale as of January 31, 2021. We also operated in Argentina and Brazil prior to the sale of Walmart Argentina in November 2020 and the majority stake of Walmart Brazil in fiscal 2019. Refer to Note 12 to our Consolidated Financial Statements for information on these divestitures. Our operations are conducted in three reportable segments: Walmart U.S., Walmart International and Sam's Club, which are further described below. Each segment contributes to the Company's operating results differently. However, each has generally maintained a consistent contribution rate to the Company's net sales and operating income in recent years other than minor changes to the contribution rate for the Walmart International segment due to fluctuations in currency exchange rates. Additional information on our operating segments and geographic and product information is contained in Note 13 to our Consolidated Financial Statements.
````

**#2 `WMT_FY2021_2021-01-31:426`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 13. Segments and Disaggregated Revenue
Segments The Company is engaged in the operation of retail, wholesale and other units, as well as eCommerce websites, located throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico. The Company also engaged in operations in Japan and the United Kingdom, both of which were classified as held for sale as of January 31, 2021, and subsequently sold in February 2021 and March 2021, respectively. The Company also operated in Argentina prior to the sale of Walmart Argentina in November 2020 and in Brazil prior to sale of the majority stake of Walmart Brazil in fiscal 2019. Refer to Note 12 for discussion of recent divestitures. The Company's operations are conducted in three reportable segments: Walmart U.S., Walmart International and Sam's Club. The Company defines its segments as those operations whose results the chief operating decision maker ("CODM") regularly reviews to analyze performance and allocate resources. The Company sells similar individual products and services in each of its segments. It is impracticable to segregate and identify revenues for each of these individual products and services.
````

**#3 `WMT_FY2021_2021-01-31:35`** (cited, gold #2, gold #3)

````text
ITEM 1. BUSINESS > Walmart International Segment
Walmart International is our second largest segment and operated in 25 countries outside of the U.S as of January 31, 2021. Walmart International operated through our wholly-owned subsidiaries in Canada, Chile, and China, as well as our businesses classified as held for sale in Japan and the United Kingdom as of January 31, 2021. Walmart International also operates through our majority-owned subsidiaries in Africa (which includes Botswana, Ghana, Kenya, Lesotho, Malawi, Mozambique, Namibia, Nigeria, South Africa, Swaziland, Tanzania, Uganda and Zambia), Central America (which includes Costa Rica, El Salvador, Guatemala, Honduras and Nicaragua), India and Mexico. Walmart International previously operated in Argentina and Brazil prior to the sale of Walmart Argentina in fiscal 2021 and the majority stake of Walmart Brazil in fiscal 2019. Refer to Note 12 for discussion of recent divestitures.
````

**#4 `WMT_FY2017_2017-01-31:42`** (cited, gold #1, gold #4)

````text
ITEM 1. BUSINESS > Walmart International Segment
The Walmart International segment consists of operations in 27 countries outside of the U.S. and includes numerous formats divided into three major categories: retail, wholesale and other. These categories consist of numerous formats, including supercenters, supermarkets, hypermarkets, warehouse clubs, including Sam's Clubs, cash & carry, home improvement, specialty electronics, apparel stores, drug stores and convenience stores, as well as digital retail. The segment's net sales for fiscal 2017, 2016 and 2015, were $116.1 billion, $123.4 billion and $136.2 billion, respectively, which have been impacted by unfavorable currency exchange rate fluctuations. During the most recent fiscal year, no single unit accounted for as much as 1% of total Company net sales. Physical. Our Walmart International segment is comprised of physical stores operated by: our wholly-owned subsidiaries operating in Argentina, Brazil, Canada, Chile, China, India, Japan and the United Kingdom; and our majority-owned subsidiaries operating in Africa (which includes Botswana, Ghana, Kenya, Lesotho, Malawi, Mozambique, Namibia, Nigeria, South Africa, Swaziland, Tanzania, Uganda and Zambia), Central America (which includes Costa Rica, El Salvador, Guatemala, Honduras and Nicaragua) and Mexico.
````

**#6 `WMT_FY2021_2021-01-31:41`** (gold #1, gold #2)

````text
ITEM 1. BUSINESS > Walmart International Segment
Distribution. We utilize a total of 221 distribution facilities located in Canada, Central America, Chile, China, India, Mexico and South Africa, as well as Japan and the United Kingdom, whose operations are classified as held for sale as of January 31, 2021, and subsequently divested in the first quarter of fiscal 2022. Through these facilities, we process and distribute both imported and domestic products to the operating units of the Walmart International segment. During fiscal 2021, the majority of Walmart International's purchases passed through these distribution facilities. Suppliers ship the remainder of Walmart International's purchases directly to our stores in the various markets in which we operate. Across the segment, we have efficient networks connecting physical stores and distribution and fulfillment centers which facilitate the movement of goods to where our customers live. We ship merchandise purchased by customers on our eCommerce platforms by a number of methods from multiple locations including from our 83 dedicated eCommerce fulfillment centers, more than 2,800 eCommerce sort centers and last-mile delivery facilities in India, as well as our physical retail stores.
````

**#9 `WMT_FY2017_2017-01-31:25`** (cited, gold #1, gold #4)

````text
ITEM 1. BUSINESS > Information About Our Segments
The Company is engaged in the operation of retail, wholesale and other units located throughout the U.S., Africa, Argentina, Brazil, Canada, Central America, Chile, China, India, Japan, Mexico and the United Kingdom and retail websites in the U.S. and 10 other countries. The Company's operations are conducted in three reportable segments: Walmart U.S., Walmart International and Sam's Club. The Company defines its segments as those operations whose results the chief operating decision maker ("CODM") regularly reviews to analyze performance and allocate resources. The Company sells similar individual products and services in each of its segments. It is impractical to segregate and identify revenues for each of these individual products and services. Walmart U.S. is our largest segment and operates retail stores in all 50 states in the U.S., Washington D.C. and Puerto Rico, with three primary store formats, as well as digital retail. Walmart U.S. generated approximately 64% of our net sales in fiscal 2017, and of our three segments, Walmart U.S. is the largest and has historically had the highest gross profit as a percentage of net sales ("gross profit rate"). In addition, Walmart U.S. has historically contributed the greatest amount to the Company's net sales and operating income.
````

</details>

RQ2 citation match (section level): `cited=[('WMT', 'Item 1'), ('WMT', 'Item 8')] gold=[(None, 'Item 1')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 5.

**Generated answer**

> Between fiscal 2017 and fiscal 2021, Walmart’s geographic footprint narrowed and the treatment of some international operations changed.
>
> - In fiscal 2017, Walmart said it operated throughout the U.S., Africa, Argentina, Brazil, Canada, Central America, Chile, China, India, Japan, Mexico and the United Kingdom, and Walmart International consisted of operations in 27 countries outside the U.S. [5][1]
> - In fiscal 2021, Walmart said it operated throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico, and Walmart International operated in 25 countries outside the U.S. as of January 31, 2021. Argentina and Brazil were no longer current operating markets because Walmart Argentina had been sold in November 2020 and the majority stake in Walmart Brazil had been sold in fiscal 2019. [2][3]
>
> Regarding the U.K. and Japan:
>
> - In fiscal 2017, the U.K. and Japan were part of Walmart’s operating footprint within Walmart International. [1][5]
> - By fiscal 2021, Walmart still had operations in the U.K. and Japan, but both were classified as held for sale as of January 31, 2021, rather than treated as ongoing core operations; they were subsequently sold in February 2021 and March 2021, respectively. [2][3][4]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `WMT_FY2017_2017-01-31:42` | Item 1 › Walmart International Segment | ✓ | #1, #4 | The Walmart International segment consists of operations in 27 countries outside of the U.S. and includes numerous formats divided into three major categories: retail, wholesale and other. These categories consist of num… |
| 2 | `WMT_FY2021_2021-01-31:26` | Item 1 › Information About Our Segments | ✓ | #1, #2, #3, #4 | We are engaged in global operations of retail, wholesale and other units, as well as eCommerce, located throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico. The Company also engaged in op… |
| 3 | `WMT_FY2021_2021-01-31:35` | Item 1 › Walmart International Segment | ✓ | #2, #3 | Walmart International is our second largest segment and operated in 25 countries outside of the U.S as of January 31, 2021. Walmart International operated through our wholly-owned subsidiaries in Canada, Chile, and China… |
| 4 | `WMT_FY2021_2021-01-31:426` | Item 8 › Note 13. Segments and Disaggregated Revenue | ✓ | #1, #2, #3, #4 | Segments The Company is engaged in the operation of retail, wholesale and other units, as well as eCommerce websites, located throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico. The Comp… |
| 5 | `WMT_FY2017_2017-01-31:25` | Item 1 › Information About Our Segments | ✓ | #1, #4 | The Company is engaged in the operation of retail, wholesale and other units located throughout the U.S., Africa, Argentina, Brazil, Canada, Central America, Chile, China, India, Japan, Mexico and the United Kingdom and … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `WMT_FY2017_2017-01-31:42`** (cited, gold #1, gold #4)

````text
ITEM 1. BUSINESS > Walmart International Segment
The Walmart International segment consists of operations in 27 countries outside of the U.S. and includes numerous formats divided into three major categories: retail, wholesale and other. These categories consist of numerous formats, including supercenters, supermarkets, hypermarkets, warehouse clubs, including Sam's Clubs, cash & carry, home improvement, specialty electronics, apparel stores, drug stores and convenience stores, as well as digital retail. The segment's net sales for fiscal 2017, 2016 and 2015, were $116.1 billion, $123.4 billion and $136.2 billion, respectively, which have been impacted by unfavorable currency exchange rate fluctuations. During the most recent fiscal year, no single unit accounted for as much as 1% of total Company net sales. Physical. Our Walmart International segment is comprised of physical stores operated by: our wholly-owned subsidiaries operating in Argentina, Brazil, Canada, Chile, China, India, Japan and the United Kingdom; and our majority-owned subsidiaries operating in Africa (which includes Botswana, Ghana, Kenya, Lesotho, Malawi, Mozambique, Namibia, Nigeria, South Africa, Swaziland, Tanzania, Uganda and Zambia), Central America (which includes Costa Rica, El Salvador, Guatemala, Honduras and Nicaragua) and Mexico.
````

**#2 `WMT_FY2021_2021-01-31:26`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
ITEM 1. BUSINESS > Information About Our Segments
We are engaged in global operations of retail, wholesale and other units, as well as eCommerce, located throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico. The Company also engaged in operations in the U.K. and Japan, both of which were classified as held for sale as of January 31, 2021. We also operated in Argentina and Brazil prior to the sale of Walmart Argentina in November 2020 and the majority stake of Walmart Brazil in fiscal 2019. Refer to Note 12 to our Consolidated Financial Statements for information on these divestitures. Our operations are conducted in three reportable segments: Walmart U.S., Walmart International and Sam's Club, which are further described below. Each segment contributes to the Company's operating results differently. However, each has generally maintained a consistent contribution rate to the Company's net sales and operating income in recent years other than minor changes to the contribution rate for the Walmart International segment due to fluctuations in currency exchange rates. Additional information on our operating segments and geographic and product information is contained in Note 13 to our Consolidated Financial Statements.
````

**#3 `WMT_FY2021_2021-01-31:35`** (cited, gold #2, gold #3)

````text
ITEM 1. BUSINESS > Walmart International Segment
Walmart International is our second largest segment and operated in 25 countries outside of the U.S as of January 31, 2021. Walmart International operated through our wholly-owned subsidiaries in Canada, Chile, and China, as well as our businesses classified as held for sale in Japan and the United Kingdom as of January 31, 2021. Walmart International also operates through our majority-owned subsidiaries in Africa (which includes Botswana, Ghana, Kenya, Lesotho, Malawi, Mozambique, Namibia, Nigeria, South Africa, Swaziland, Tanzania, Uganda and Zambia), Central America (which includes Costa Rica, El Salvador, Guatemala, Honduras and Nicaragua), India and Mexico. Walmart International previously operated in Argentina and Brazil prior to the sale of Walmart Argentina in fiscal 2021 and the majority stake of Walmart Brazil in fiscal 2019. Refer to Note 12 for discussion of recent divestitures.
````

**#4 `WMT_FY2021_2021-01-31:426`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 13. Segments and Disaggregated Revenue
Segments The Company is engaged in the operation of retail, wholesale and other units, as well as eCommerce websites, located throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico. The Company also engaged in operations in Japan and the United Kingdom, both of which were classified as held for sale as of January 31, 2021, and subsequently sold in February 2021 and March 2021, respectively. The Company also operated in Argentina prior to the sale of Walmart Argentina in November 2020 and in Brazil prior to sale of the majority stake of Walmart Brazil in fiscal 2019. Refer to Note 12 for discussion of recent divestitures. The Company's operations are conducted in three reportable segments: Walmart U.S., Walmart International and Sam's Club. The Company defines its segments as those operations whose results the chief operating decision maker ("CODM") regularly reviews to analyze performance and allocate resources. The Company sells similar individual products and services in each of its segments. It is impracticable to segregate and identify revenues for each of these individual products and services.
````

**#5 `WMT_FY2017_2017-01-31:25`** (cited, gold #1, gold #4)

````text
ITEM 1. BUSINESS > Information About Our Segments
The Company is engaged in the operation of retail, wholesale and other units located throughout the U.S., Africa, Argentina, Brazil, Canada, Central America, Chile, China, India, Japan, Mexico and the United Kingdom and retail websites in the U.S. and 10 other countries. The Company's operations are conducted in three reportable segments: Walmart U.S., Walmart International and Sam's Club. The Company defines its segments as those operations whose results the chief operating decision maker ("CODM") regularly reviews to analyze performance and allocate resources. The Company sells similar individual products and services in each of its segments. It is impractical to segregate and identify revenues for each of these individual products and services. Walmart U.S. is our largest segment and operates retail stores in all 50 states in the U.S., Washington D.C. and Puerto Rico, with three primary store formats, as well as digital retail. Walmart U.S. generated approximately 64% of our net sales in fiscal 2017, and of our three segments, Walmart U.S. is the largest and has historically had the highest gross profit as a percentage of net sales ("gross profit rate"). In addition, Walmart U.S. has historically contributed the greatest amount to the Company's net sales and operating income.
````

</details>

RQ2 citation match (section level): `cited=[('WMT', 'Item 1'), ('WMT', 'Item 8')] gold=[(None, 'Item 1')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 10, cited: 4.

**Generated answer**

> In fiscal 2017, Walmart International consisted of operations in 27 countries outside of the U.S. [WMT FY2017, Item 1, WMT_FY2017_2017-01-31:42]  
>
> In fiscal 2021, Walmart International operated in 25 countries outside of the U.S. as of January 31, 2021. [WMT FY2021, Item 1, WMT_FY2021_2021-01-31:35]  
>
> In fiscal 2017, Walmart International included wholly-owned subsidiaries in Argentina, Brazil, Canada, Chile, China, India, Japan and the United Kingdom, and majority-owned subsidiaries in Africa, Central America and Mexico. [WMT FY2017, Item 1, WMT_FY2017_2017-01-31:42]  
>
> By fiscal 2021, Walmart International operated through wholly-owned subsidiaries in Canada, Chile and China, while its Japan and United Kingdom businesses were classified as held for sale as of January 31, 2021, and it operated through majority-owned subsidiaries in Africa, Central America, India and Mexico. [WMT FY2021, Item 1, WMT_FY2021_2021-01-31:35]  
>
> Fiscal 2021 also states that Walmart International previously operated in Argentina and Brazil, but Walmart Argentina was sold in fiscal 2021 and the majority stake of Walmart Brazil had been sold in fiscal 2019. [WMT FY2021, Item 1, WMT_FY2021_2021-01-31:35]  
>
> The company’s broader segment disclosure in fiscal 2021 likewise says it was engaged in operations throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico, while also noting operations in Japan and the United Kingdom were classified as held for sale as of January 31, 2021. [WMT FY2021, Item 1, WMT_FY2021_2021-01-31:26] [WMT FY2021, Item 8, WMT_FY2021_2021-01-31:426]  
>
> The fiscal 2021 filing further states that the Japan and United Kingdom operations were subsequently sold in February 2021 and March 2021, respectively. [WMT FY2021, Item 8, WMT_FY2021_2021-01-31:426]  
>
> The filing does not disclose in these evidence blocks a full fiscal 2021 country-by-country list comparable to the fiscal 2017 “27 countries” statement beyond the regional and market descriptions provided.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `WMT_FY2021_2021-01-31:26` | Item 1 › Information About Our Segments | ✓ | #1, #2, #3, #4 | We are engaged in global operations of retail, wholesale and other units, as well as eCommerce, located throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico. The Company also engaged in op… |
| 2 | `WMT_FY2021_2021-01-31:41` | Item 1 › Walmart International Segment |  | #1, #2 | Distribution. We utilize a total of 221 distribution facilities located in Canada, Central America, Chile, China, India, Mexico and South Africa, as well as Japan and the United Kingdom, whose operations are classified a… |
| 3 | `WMT_FY2021_2021-01-31:136` | Item 2 › International |  |  | The Walmart International segment comprises the Company's operations outside of the U.S. Unit counts as of January 31, 2021(1) for Walmart International are summarized by major category for each geographic market as foll… |
| 4 | `WMT_FY2017_2017-01-31:42` | Item 1 › Walmart International Segment | ✓ | #1, #4 | The Walmart International segment consists of operations in 27 countries outside of the U.S. and includes numerous formats divided into three major categories: retail, wholesale and other. These categories consist of num… |
| 5 | `WMT_FY2021_2021-01-31:39` | Item 1 › Walmart International Segment |  |  | Walmart International also offers fuel, financial services and related products in various markets. Our businesses in Mexico and Canada, for example, offer prepaid cards and money (wire) transfers, and our PhonePe busine… |
| 6 | `WMT_FY2021_2021-01-31:35` | Item 1 › Walmart International Segment | ✓ | #2, #3 | Walmart International is our second largest segment and operated in 25 countries outside of the U.S as of January 31, 2021. Walmart International operated through our wholly-owned subsidiaries in Canada, Chile, and China… |
| 7 | `WMT_FY2021_2021-01-31:426` | Item 8 › Note 13. Segments and Disaggregated Revenue | ✓ | #1, #2, #3, #4 | Segments The Company is engaged in the operation of retail, wholesale and other units, as well as eCommerce websites, located throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico. The Comp… |
| 8 | `WMT_FY2021_2021-01-31:248` | Item 7 › Impairment of Assets |  | #3 | In fiscal 2021, the Company's operations in Argentina, Japan and the United Kingdom met the held for sale criteria. As a result, the individual disposal groups were measured at fair value, less costs to sell, which resul… |
| 9 | `WMT_FY2021_2021-01-31:137` | Item 2 › International |  |  | \| Geographic Market \| Retail \| Wholesale \| Other(2) \| Total \| Square feet(3) \| \|---\|---\|---\|---\|---\|---\| \| Africa(4) \| 332 \| 91 \| — \| 423 \| 24,537 \| \| Canada \| 408 \| — \| — \| 408 \| 52,976 \| \| Central America(5) \| 855 \| — … |
| 10 | `WMT_FY2021_2021-01-31:244` | Item 7 › Other Matters |  |  | We discuss our "Asda Equal Value Claims" which includes certain existing employment claims against our recently divested United Kingdom subsidiary, Asda Group Limited, including certain risks arising therefrom, under the… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `WMT_FY2021_2021-01-31:26`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
ITEM 1. BUSINESS > Information About Our Segments
We are engaged in global operations of retail, wholesale and other units, as well as eCommerce, located throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico. The Company also engaged in operations in the U.K. and Japan, both of which were classified as held for sale as of January 31, 2021. We also operated in Argentina and Brazil prior to the sale of Walmart Argentina in November 2020 and the majority stake of Walmart Brazil in fiscal 2019. Refer to Note 12 to our Consolidated Financial Statements for information on these divestitures. Our operations are conducted in three reportable segments: Walmart U.S., Walmart International and Sam's Club, which are further described below. Each segment contributes to the Company's operating results differently. However, each has generally maintained a consistent contribution rate to the Company's net sales and operating income in recent years other than minor changes to the contribution rate for the Walmart International segment due to fluctuations in currency exchange rates. Additional information on our operating segments and geographic and product information is contained in Note 13 to our Consolidated Financial Statements.
````

**#2 `WMT_FY2021_2021-01-31:41`** (gold #1, gold #2)

````text
ITEM 1. BUSINESS > Walmart International Segment
Distribution. We utilize a total of 221 distribution facilities located in Canada, Central America, Chile, China, India, Mexico and South Africa, as well as Japan and the United Kingdom, whose operations are classified as held for sale as of January 31, 2021, and subsequently divested in the first quarter of fiscal 2022. Through these facilities, we process and distribute both imported and domestic products to the operating units of the Walmart International segment. During fiscal 2021, the majority of Walmart International's purchases passed through these distribution facilities. Suppliers ship the remainder of Walmart International's purchases directly to our stores in the various markets in which we operate. Across the segment, we have efficient networks connecting physical stores and distribution and fulfillment centers which facilitate the movement of goods to where our customers live. We ship merchandise purchased by customers on our eCommerce platforms by a number of methods from multiple locations including from our 83 dedicated eCommerce fulfillment centers, more than 2,800 eCommerce sort centers and last-mile delivery facilities in India, as well as our physical retail stores.
````

**#4 `WMT_FY2017_2017-01-31:42`** (cited, gold #1, gold #4)

````text
ITEM 1. BUSINESS > Walmart International Segment
The Walmart International segment consists of operations in 27 countries outside of the U.S. and includes numerous formats divided into three major categories: retail, wholesale and other. These categories consist of numerous formats, including supercenters, supermarkets, hypermarkets, warehouse clubs, including Sam's Clubs, cash & carry, home improvement, specialty electronics, apparel stores, drug stores and convenience stores, as well as digital retail. The segment's net sales for fiscal 2017, 2016 and 2015, were $116.1 billion, $123.4 billion and $136.2 billion, respectively, which have been impacted by unfavorable currency exchange rate fluctuations. During the most recent fiscal year, no single unit accounted for as much as 1% of total Company net sales. Physical. Our Walmart International segment is comprised of physical stores operated by: our wholly-owned subsidiaries operating in Argentina, Brazil, Canada, Chile, China, India, Japan and the United Kingdom; and our majority-owned subsidiaries operating in Africa (which includes Botswana, Ghana, Kenya, Lesotho, Malawi, Mozambique, Namibia, Nigeria, South Africa, Swaziland, Tanzania, Uganda and Zambia), Central America (which includes Costa Rica, El Salvador, Guatemala, Honduras and Nicaragua) and Mexico.
````

**#6 `WMT_FY2021_2021-01-31:35`** (cited, gold #2, gold #3)

````text
ITEM 1. BUSINESS > Walmart International Segment
Walmart International is our second largest segment and operated in 25 countries outside of the U.S as of January 31, 2021. Walmart International operated through our wholly-owned subsidiaries in Canada, Chile, and China, as well as our businesses classified as held for sale in Japan and the United Kingdom as of January 31, 2021. Walmart International also operates through our majority-owned subsidiaries in Africa (which includes Botswana, Ghana, Kenya, Lesotho, Malawi, Mozambique, Namibia, Nigeria, South Africa, Swaziland, Tanzania, Uganda and Zambia), Central America (which includes Costa Rica, El Salvador, Guatemala, Honduras and Nicaragua), India and Mexico. Walmart International previously operated in Argentina and Brazil prior to the sale of Walmart Argentina in fiscal 2021 and the majority stake of Walmart Brazil in fiscal 2019. Refer to Note 12 for discussion of recent divestitures.
````

**#7 `WMT_FY2021_2021-01-31:426`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 13. Segments and Disaggregated Revenue
Segments The Company is engaged in the operation of retail, wholesale and other units, as well as eCommerce websites, located throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico. The Company also engaged in operations in Japan and the United Kingdom, both of which were classified as held for sale as of January 31, 2021, and subsequently sold in February 2021 and March 2021, respectively. The Company also operated in Argentina prior to the sale of Walmart Argentina in November 2020 and in Brazil prior to sale of the majority stake of Walmart Brazil in fiscal 2019. Refer to Note 12 for discussion of recent divestitures. The Company's operations are conducted in three reportable segments: Walmart U.S., Walmart International and Sam's Club. The Company defines its segments as those operations whose results the chief operating decision maker ("CODM") regularly reviews to analyze performance and allocate resources. The Company sells similar individual products and services in each of its segments. It is impracticable to segregate and identify revenues for each of these individual products and services.
````

**#8 `WMT_FY2021_2021-01-31:248`** (gold #3)

````text
ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Impairment of Assets
In fiscal 2021, the Company's operations in Argentina, Japan and the United Kingdom met the held for sale criteria. As a result, the individual disposal groups were measured at fair value, less costs to sell, which resulted in impairment charges that were included in the total estimated pre-tax loss of $8.3 billion recorded in fiscal 2021. Refer to Note 12. Fiscal 2019 included a pre-tax loss of $4.8 billion related to the sale of the majority stake in Walmart Brazil, which included full impairment of all related assets.
````

</details>

RQ2 citation match (section level): `cited=[('WMT', 'Item 1'), ('WMT', 'Item 8')] gold=[(None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 8, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In fiscal 2017, Walmart International consisted of operations in 27 countries outside of the U.S. [WMT FY2017, Item 1, WMT_FY2017_2017-01-31:42] | supported | The cited text states Walmart International consisted of operations in 27 countries outside the U.S. in fiscal 2017. |
| In fiscal 2021, Walmart International operated in 25 countries outside of the U.S. as of January 31, 2021. [WMT FY2021, Item 1, WMT_FY2021_2021-01-31:35] | supported | The evidence explicitly says Walmart International operated in 25 countries outside the U.S. as of January 31, 2021. |
| In fiscal 2017, Walmart International included wholly-owned subsidiaries in Argentina, Brazil, Canada, Chile, China, India, Japan and the United Kingdom, and majority-owned subsidiaries in Africa, Central America and Mexico. [WMT FY2017, Item 1, WMT_FY2017_2017-01-31:42] | supported | The cited passage lists those wholly-owned and majority-owned subsidiaries exactly as stated. |
| By fiscal 2021, Walmart International operated through wholly-owned subsidiaries in Canada, Chile and China, while its Japan and United Kingdom businesses were classified as held for sale as of January 31, 2021, and it operated through majority-owned subsidiaries in Africa, Central America, India and Mexico. [WMT FY2021, Item 1, WMT_FY2021_2021-01-31:35] | supported | The evidence directly states the wholly-owned, held-for-sale, and majority-owned operations exactly as described. |
| Fiscal 2021 also states that Walmart International previously operated in Argentina and Brazil, but Walmart Argentina was sold in fiscal 2021 and the majority stake of Walmart Brazil had been sold in fiscal 2019. [WMT FY2021, Item 1, WMT_FY2021_2021-01-31:35] | supported | The cited text explicitly says Walmart previously operated in Argentina and Brazil and gives those sale timing details. |
| The company’s broader segment disclosure in fiscal 2021 likewise says it was engaged in operations throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico, while also noting operations in Japan and the United Kingdom were classified as held for sale as of January 31, 2021. [WMT FY2021, Item 1, WMT_FY2021_2021-01-31:26] [WMT FY2021, Item 8, WMT_FY2021_2021-01-31:426] | supported | Both cited passages state operations in those regions and note Japan and the U.K. were classified as held for sale as of January 31, 2021. |
| The fiscal 2021 filing further states that the Japan and United Kingdom operations were subsequently sold in February 2021 and March 2021, respectively. [WMT FY2021, Item 8, WMT_FY2021_2021-01-31:426] | supported | The cited note says Japan and the United Kingdom were subsequently sold in February 2021 and March 2021, respectively. |
| The filing does not disclose in these evidence blocks a full fiscal 2021 country-by-country list comparable to the fiscal 2017 “27 countries” statement beyond the regional and market descriptions provided. | supported | Across the retrieved evidence, fiscal 2021 gives regional and market descriptions and a 25-country total, but not a full country-by-country list comparable to the fiscal 2017 statement. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 9, cited: 4.

**Generated answer**

> In fiscal 2017, Walmart International consisted of operations in 27 countries outside of the U.S. [WMT FY2017, Item 1, WMT_FY2017_2017-01-31:42]
>
> In fiscal 2021, Walmart International operated in 25 countries outside of the U.S. as of January 31, 2021. [WMT FY2021, Item 1, WMT_FY2021_2021-01-31:35]
>
> In fiscal 2017, Walmart International included wholly-owned subsidiaries in Argentina, Brazil, Canada, Chile, China, India, Japan and the United Kingdom, and majority-owned subsidiaries in Africa, Central America and Mexico. [WMT FY2017, Item 1, WMT_FY2017_2017-01-31:42]
>
> By fiscal 2021, Walmart International operated through wholly-owned subsidiaries in Canada, Chile and China, and through businesses classified as held for sale in Japan and the United Kingdom as of January 31, 2021, while also operating through majority-owned subsidiaries in Africa, Central America, India and Mexico. [WMT FY2021, Item 1, WMT_FY2021_2021-01-31:35]
>
> The fiscal 2021 filing also states that the company previously operated in Argentina and Brazil, but had sold Walmart Argentina in fiscal 2021 and the majority stake of Walmart Brazil in fiscal 2019. [WMT FY2021, Item 1, WMT_FY2021_2021-01-31:35]
>
> Regarding the U.K. and Japan specifically, in fiscal 2021 Walmart stated that both operations were classified as held for sale as of January 31, 2021. [WMT FY2021, Item 1, WMT_FY2021_2021-01-31:26] [WMT FY2021, Item 8, WMT_FY2021_2021-01-31:426]
>
> The fiscal 2021 filing further states that the Japan and United Kingdom businesses were subsequently sold in February 2021 and March 2021, respectively. [WMT FY2021, Item 8, WMT_FY2021_2021-01-31:426]
>
> So, between fiscal 2017 and fiscal 2021, Walmart’s international geographic scope narrowed from 27 countries to 25 countries outside the U.S., reflecting the exits from Argentina and Brazil, and its U.K. and Japan operations shifted from active international operations in 2017 to held-for-sale businesses at fiscal 2021 year-end that were then divested shortly afterward. [WMT FY2017, Item 1, WMT_FY2017_2017-01-31:42] [WMT FY2021, Item 1, WMT_FY2021_2021-01-31:35] [WMT FY2021, Item 8, WMT_FY2021_2021-01-31:426]
>
> > [Guardrail Audit Warning]: Manual verification required; 2 sentence(s) are not supported by their cited chunks.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `WMT_FY2021_2021-01-31:26` | Item 1 › Information About Our Segments | ✓ | #1, #2, #3, #4 | We are engaged in global operations of retail, wholesale and other units, as well as eCommerce, located throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico. The Company also engaged in op… |
| 2 | `WMT_FY2021_2021-01-31:41` | Item 1 › Walmart International Segment |  | #1, #2 | Distribution. We utilize a total of 221 distribution facilities located in Canada, Central America, Chile, China, India, Mexico and South Africa, as well as Japan and the United Kingdom, whose operations are classified a… |
| 3 | `WMT_FY2021_2021-01-31:136` | Item 2 › International |  |  | The Walmart International segment comprises the Company's operations outside of the U.S. Unit counts as of January 31, 2021(1) for Walmart International are summarized by major category for each geographic market as foll… |
| 4 | `WMT_FY2017_2017-01-31:42` | Item 1 › Walmart International Segment | ✓ | #1, #4 | The Walmart International segment consists of operations in 27 countries outside of the U.S. and includes numerous formats divided into three major categories: retail, wholesale and other. These categories consist of num… |
| 5 | `WMT_FY2021_2021-01-31:39` | Item 1 › Walmart International Segment |  |  | Walmart International also offers fuel, financial services and related products in various markets. Our businesses in Mexico and Canada, for example, offer prepaid cards and money (wire) transfers, and our PhonePe busine… |
| 6 | `WMT_FY2021_2021-01-31:35` | Item 1 › Walmart International Segment | ✓ | #2, #3 | Walmart International is our second largest segment and operated in 25 countries outside of the U.S as of January 31, 2021. Walmart International operated through our wholly-owned subsidiaries in Canada, Chile, and China… |
| 7 | `WMT_FY2021_2021-01-31:426` | Item 8 › Note 13. Segments and Disaggregated Revenue | ✓ | #1, #2, #3, #4 | Segments The Company is engaged in the operation of retail, wholesale and other units, as well as eCommerce websites, located throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico. The Comp… |
| 8 | `WMT_FY2021_2021-01-31:137` | Item 2 › International |  |  | \| Geographic Market \| Retail \| Wholesale \| Other(2) \| Total \| Square feet(3) \| \|---\|---\|---\|---\|---\|---\| \| Africa(4) \| 332 \| 91 \| — \| 423 \| 24,537 \| \| Canada \| 408 \| — \| — \| 408 \| 52,976 \| \| Central America(5) \| 855 \| — … |
| 9 | `WMT_FY2017_2017-01-31:137` | Item 2 |  |  | \| \| Owned and Operated \| Owned and Third Party Operated \| Leased and Operated \| Third Party Owned and Operated \| Total \| \|---\|---\|---\|---\|---\|---\| \| Canada \| 132 \| — \| 278 \| — \| 410 \| \| Central America \| 267 \| — \| 464 \| … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `WMT_FY2021_2021-01-31:26`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
ITEM 1. BUSINESS > Information About Our Segments
We are engaged in global operations of retail, wholesale and other units, as well as eCommerce, located throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico. The Company also engaged in operations in the U.K. and Japan, both of which were classified as held for sale as of January 31, 2021. We also operated in Argentina and Brazil prior to the sale of Walmart Argentina in November 2020 and the majority stake of Walmart Brazil in fiscal 2019. Refer to Note 12 to our Consolidated Financial Statements for information on these divestitures. Our operations are conducted in three reportable segments: Walmart U.S., Walmart International and Sam's Club, which are further described below. Each segment contributes to the Company's operating results differently. However, each has generally maintained a consistent contribution rate to the Company's net sales and operating income in recent years other than minor changes to the contribution rate for the Walmart International segment due to fluctuations in currency exchange rates. Additional information on our operating segments and geographic and product information is contained in Note 13 to our Consolidated Financial Statements.
````

**#2 `WMT_FY2021_2021-01-31:41`** (gold #1, gold #2)

````text
ITEM 1. BUSINESS > Walmart International Segment
Distribution. We utilize a total of 221 distribution facilities located in Canada, Central America, Chile, China, India, Mexico and South Africa, as well as Japan and the United Kingdom, whose operations are classified as held for sale as of January 31, 2021, and subsequently divested in the first quarter of fiscal 2022. Through these facilities, we process and distribute both imported and domestic products to the operating units of the Walmart International segment. During fiscal 2021, the majority of Walmart International's purchases passed through these distribution facilities. Suppliers ship the remainder of Walmart International's purchases directly to our stores in the various markets in which we operate. Across the segment, we have efficient networks connecting physical stores and distribution and fulfillment centers which facilitate the movement of goods to where our customers live. We ship merchandise purchased by customers on our eCommerce platforms by a number of methods from multiple locations including from our 83 dedicated eCommerce fulfillment centers, more than 2,800 eCommerce sort centers and last-mile delivery facilities in India, as well as our physical retail stores.
````

**#4 `WMT_FY2017_2017-01-31:42`** (cited, gold #1, gold #4)

````text
ITEM 1. BUSINESS > Walmart International Segment
The Walmart International segment consists of operations in 27 countries outside of the U.S. and includes numerous formats divided into three major categories: retail, wholesale and other. These categories consist of numerous formats, including supercenters, supermarkets, hypermarkets, warehouse clubs, including Sam's Clubs, cash & carry, home improvement, specialty electronics, apparel stores, drug stores and convenience stores, as well as digital retail. The segment's net sales for fiscal 2017, 2016 and 2015, were $116.1 billion, $123.4 billion and $136.2 billion, respectively, which have been impacted by unfavorable currency exchange rate fluctuations. During the most recent fiscal year, no single unit accounted for as much as 1% of total Company net sales. Physical. Our Walmart International segment is comprised of physical stores operated by: our wholly-owned subsidiaries operating in Argentina, Brazil, Canada, Chile, China, India, Japan and the United Kingdom; and our majority-owned subsidiaries operating in Africa (which includes Botswana, Ghana, Kenya, Lesotho, Malawi, Mozambique, Namibia, Nigeria, South Africa, Swaziland, Tanzania, Uganda and Zambia), Central America (which includes Costa Rica, El Salvador, Guatemala, Honduras and Nicaragua) and Mexico.
````

**#6 `WMT_FY2021_2021-01-31:35`** (cited, gold #2, gold #3)

````text
ITEM 1. BUSINESS > Walmart International Segment
Walmart International is our second largest segment and operated in 25 countries outside of the U.S as of January 31, 2021. Walmart International operated through our wholly-owned subsidiaries in Canada, Chile, and China, as well as our businesses classified as held for sale in Japan and the United Kingdom as of January 31, 2021. Walmart International also operates through our majority-owned subsidiaries in Africa (which includes Botswana, Ghana, Kenya, Lesotho, Malawi, Mozambique, Namibia, Nigeria, South Africa, Swaziland, Tanzania, Uganda and Zambia), Central America (which includes Costa Rica, El Salvador, Guatemala, Honduras and Nicaragua), India and Mexico. Walmart International previously operated in Argentina and Brazil prior to the sale of Walmart Argentina in fiscal 2021 and the majority stake of Walmart Brazil in fiscal 2019. Refer to Note 12 for discussion of recent divestitures.
````

**#7 `WMT_FY2021_2021-01-31:426`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 13. Segments and Disaggregated Revenue
Segments The Company is engaged in the operation of retail, wholesale and other units, as well as eCommerce websites, located throughout the U.S., Africa, Canada, Central America, Chile, China, India and Mexico. The Company also engaged in operations in Japan and the United Kingdom, both of which were classified as held for sale as of January 31, 2021, and subsequently sold in February 2021 and March 2021, respectively. The Company also operated in Argentina prior to the sale of Walmart Argentina in November 2020 and in Brazil prior to sale of the majority stake of Walmart Brazil in fiscal 2019. Refer to Note 12 for discussion of recent divestitures. The Company's operations are conducted in three reportable segments: Walmart U.S., Walmart International and Sam's Club. The Company defines its segments as those operations whose results the chief operating decision maker ("CODM") regularly reviews to analyze performance and allocate resources. The Company sells similar individual products and services in each of its segments. It is impracticable to segregate and identify revenues for each of these individual products and services.
````

</details>

RQ2 citation match (section level): `cited=[('WMT', 'Item 1'), ('WMT', 'Item 8')] gold=[(None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 7, partial 1, unsupported 1, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In fiscal 2017, Walmart International consisted of operations in 27 countries outside of the U.S. [WMT FY2017, Item 1, WMT_FY2017_2017-01-31:42] | supported | The cited text states Walmart International consisted of operations in 27 countries outside the U.S. in fiscal 2017. |
| In fiscal 2021, Walmart International operated in 25 countries outside of the U.S. as of January 31, 2021. [WMT FY2021, Item 1, WMT_FY2021_2021-01-31:35] | supported | The evidence explicitly says Walmart International operated in 25 countries outside the U.S. as of January 31, 2021. |
| In fiscal 2017, Walmart International included wholly-owned subsidiaries in Argentina, Brazil, Canada, Chile, China, India, Japan and the United Kingdom, and majority-owned subsidiaries in Africa, Central America and Mexico. [WMT FY2017, Item 1, WMT_FY2017_2017-01-31:42] | supported | The cited passage lists those wholly-owned and majority-owned subsidiaries exactly as stated. |
| By fiscal 2021, Walmart International operated through wholly-owned subsidiaries in Canada, Chile and China, and through businesses classified as held for sale in Japan and the United Kingdom as of January 31, 2021, while also operating through majority-owned subsidiaries in Africa, Central America, India and Mexico. [WMT FY2021, Item 1, WMT_FY2021_2021-01-31:35] | supported | The evidence matches the described wholly-owned, held-for-sale, and majority-owned operations as of January 31, 2021. |
| The fiscal 2021 filing also states that the company previously operated in Argentina and Brazil, but had sold Walmart Argentina in fiscal 2021 and the majority stake of Walmart Brazil in fiscal 2019. [WMT FY2021, Item 1, WMT_FY2021_2021-01-31:35] | supported | The cited text expressly says Walmart previously operated in Argentina and Brazil and sold Argentina in fiscal 2021 and Brazil's majority stake in fiscal 2019. |
| Regarding the U.K. | None |  |
| and Japan specifically, in fiscal 2021 Walmart stated that both operations were classified as held for sale as of January 31, 2021. [WMT FY2021, Item 1, WMT_FY2021_2021-01-31:26] [WMT FY2021, Item 8, WMT_FY2021_2021-01-31:426] | unsupported | The evidence says Japan and the U.K. were held for sale, but the sentence says 'both operations' while only naming Japan specifically. |
| The fiscal 2021 filing further states that the Japan and United Kingdom businesses were subsequently sold in February 2021 and March 2021, respectively. [WMT FY2021, Item 8, WMT_FY2021_2021-01-31:426] | supported | The cited note states Japan and the United Kingdom were subsequently sold in February 2021 and March 2021, respectively. |
| So, between fiscal 2017 and fiscal 2021, Walmart’s international geographic scope narrowed from 27 countries to 25 countries outside the U.S., reflecting the exits from Argentina and Brazil, and its U.K. | partial | The evidence supports the narrowing from 27 to 25 countries and exits from Argentina and Brazil, but not the incomplete claim about the U.K. |
| and Japan operations shifted from active international operations in 2017 to held-for-sale businesses at fiscal 2021 year-end that were then divested shortly afterward. [WMT FY2017, Item 1, WMT_FY2017_2017-01-31:42] [WMT FY2021, Item 1, WMT_FY2021_2021-01-31:35] [WMT FY2021, Item 8, WMT_FY2021_2021-01-31:426] | supported | The evidence shows Japan and the U.K. were active operations in 2017, held for sale at fiscal 2021 year-end, and sold shortly thereafter. |

</details>
