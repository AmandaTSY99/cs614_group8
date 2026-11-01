# gold-093: Cross-company text

[← all cases](../README.md) · company: AMAZON COM INC; JPMORGAN CHASE & CO (AMZN, JPM) · fiscal year: 2015 · recipe `cross_company_text` · hop `multi` · answer type `qualitative` · scope `cross_company` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> Comparing Amazon.com Inc and JPMorgan Chase & Co in their fiscal year 2015 10-K filings, how do the primary competitive factors they cite for their respective retail and financial services businesses differ?

**Gold answer**

> In fiscal year 2015, Amazon cited selection, price, and convenience (specifically fast and reliable fulfillment) as the principal competitive factors for its retail businesses, while also noting service quality and reliability for its enterprise services. In contrast, JPMorgan Chase stated that its businesses generally compete on the basis of the quality and variety of products and services, transaction execution, innovation, reputation, and price, with competition varying by client type, industry, and geography.

**Key points** (RQ3 keypoint_recall targets)

1. Amazon's retail competitive factors include selection, price, and convenience/fulfillment.
2. JPMorgan Chase's competitive factors include product/service quality, transaction execution, innovation, reputation, and price.
3. The comparison highlights the difference between e-commerce logistics/product availability and financial service quality/reputation.

**Gold evidence**

1. `AMZN_FY2015_2015-12-31` · Item 1. Business › Competition · text

   > We believe that the principal competitive factors in our retail businesses include selection, price, and convenience, including fast and reliable fulfillment.

2. `JPM_FY2015_2015-12-31` · ITEM 1: BUSINESS › Competition · text

   > The Firm’s businesses generally compete on the basis of the quality and variety of the Firm’s products and services, transaction execution, innovation, reputation and price.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 7 | 5 | 14 | 12 |
| recall@5 | 0.50 | 1.00 | 0.50 | 0.50 |
| recall@all | 0.50 | 1.00 | 0.50 | 1.00 |
| complete@all | 0 | 1 | 0 | 1 |
| average precision (lexical) | 1.00 | 0.59 | 1.00 | 0.81 |
| gold evidence first rank | #1: –, #2: 1 | #1: 3, #2: 2 | #1: 1, #2: – | #1: 1, #2: 7 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | 0.67 | 0.67 | 0.67 | 0.67 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 1.00 | 1.00 | 0.33 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 0.50 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 1655 | 1383 | 18517 | 14557 |
| cost (USD) | 0.0003 | 0.0003 | 0.0680 | 0.0549 |
| latency (s) | 4.2 | 10.2 | 38.9 | 28.4 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 7, cited: 1.

**Generated answer**

> The provided context includes JPMorgan Chase’s cited competitive factors, but it does not include Amazon.com Inc’s FY2015 10-K, so only part of the comparison can be answered.
>
> JPMorgan Chase says its financial services businesses generally compete based on:
> - quality and variety of products and services,
> - transaction execution,
> - innovation,
> - reputation, and
> - price.  
> It also says competitiveness depends on attracting and retaining personnel and on its reputation [1].
>
> What is not in the provided context:
> - Amazon.com Inc’s FY2015 10-K competitive factors for its retail business, so a direct comparison to Amazon cannot be completed from the provided materials.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JPM_FY2015_2015-12-31:14` | Item 1 › Competition | ✓ | #2 | JPMorgan Chase and its subsidiaries and affiliates operate in a highly competitive environment. Competitors include other banks, brokerage firms, investment banking companies, merchant banks, hedge funds, commodity tradi… |
| 2 | `JPM_FY2015_2015-12-31:280` | Item 15 › 2014 compared with 2013 |  |  | \| JPMorgan Chase \| \| \| \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Consumer Businesses \| \| \| \| \| \| Wholesale Businesses \| \| \| \| \| Consumer & Community Banking \| \| \| \| \| \| Corporate & Investment Bank \| \| Com… |
| 3 | `JPM_FY2015_2015-12-31:114` | Item 1A › Other Risks |  |  | The financial services industry is highly competitive, and JPMorgan Chase’s inability to compete successfully may adversely affect its results of operations. JPMorgan Chase operates in a highly competitive environment, a… |
| 4 | `JPM_FY2015_2015-12-31:15` | Item 1 › Competition |  |  | It is likely that competition in the financial services industry will become even more intense as the Firm’s businesses continue to compete with other financial institutions that may have a stronger local presence in cer… |
| 5 | `JPM_FY2015_2015-12-31:10` | Item 1 › Overview |  |  | JPMorgan Chase & Co., (“JPMorgan Chase” or the “Firm”) a financial holding company incorporated under Delaware law in 1968, is a leading global financial services firm and one of the largest banking institutions in the U… |
| 6 | `JPM_FY2015_2015-12-31:190` | Item 15 › Management’s discussion and analysis |  |  | JPMorgan Chase & Co., a financial holding company incorporated under Delaware law in 1968, is a leading global financial services firm and one of the largest banking institutions in the U.S., with operations worldwide; t… |
| 7 | `JPM_FY2015_2015-12-31:806` | Item 15 › Note 1 – Basis of presentation |  |  | JPMorgan Chase & Co. (“JPMorgan Chase” or the “Firm”), a financial holding company incorporated under Delaware law in 1968, is a leading global financial services firm and one of the largest banking institutions in the U… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JPM_FY2015_2015-12-31:14`** (cited, gold #2)

````text
ITEM 1: BUSINESS > Competition
JPMorgan Chase and its subsidiaries and affiliates operate in a highly competitive environment. Competitors include other banks, brokerage firms, investment banking companies, merchant banks, hedge funds, commodity trading companies, private equity firms, insurance companies, mutual fund companies, investment managers, credit card companies, mortgage banking companies, trust companies, securities processing companies, automobile financing companies, leasing companies, e-commerce and other Internet-based companies, financial technology companies, and other companies engaged in providing similar products and services. The Firm’s businesses generally compete on the basis of the quality and variety of the Firm’s products and services, transaction execution, innovation, reputation and price. Competition also varies based on the types of clients, customers, industries and geographies served. With respect to some of its geographies and products, JPMorgan Chase competes globally; with respect to others, the Firm competes on a national or regional basis. The Firm’s ability to compete also depends on its ability to attract and retain professional and other personnel, and on its reputation.
````

</details>

RQ2 citation match (section level): `cited=[('JPM', 'Item 1')] gold=[(None, 'Item 1')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> Amazon and JPMorgan Chase emphasize different primary competitive factors in their FY2015 10-Ks:
>
> - **Amazon (retail businesses):** cites **selection, price, and convenience**, including **fast and reliable fulfillment**, as the principal competitive factors. It also notes for seller and enterprise services the **quality, speed, and reliability of services and tools** [5].
> - **JPMorgan Chase (financial services businesses):** says it generally competes on the basis of **quality and variety of products and services, transaction execution, innovation, reputation, and price**. It also notes that competitiveness depends on its ability to **attract and retain personnel** and maintain its **reputation** [2].
>
> So, in short, **Amazon focuses more on consumer retail value drivers like selection, convenience, and fulfillment**, while **JPMorgan focuses more on service breadth, execution, innovation, reputation, and pricing in financial services** [5][2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JPM_FY2015_2015-12-31:114` | Item 1A › Other Risks |  |  | The financial services industry is highly competitive, and JPMorgan Chase’s inability to compete successfully may adversely affect its results of operations. JPMorgan Chase operates in a highly competitive environment, a… |
| 2 | `JPM_FY2015_2015-12-31:14` | Item 1 › Competition | ✓ | #2 | JPMorgan Chase and its subsidiaries and affiliates operate in a highly competitive environment. Competitors include other banks, brokerage firms, investment banking companies, merchant banks, hedge funds, commodity tradi… |
| 3 | `AMZN_FY2015_2015-12-31:24` | Item 1 › Competition |  | #1 | Our businesses encompass a large variety of product types, service offerings, and delivery channels. The international marketplace in which we compete is evolving rapidly and intensely competitive, and we face a broad ar… |
| 4 | `JPM_FY2015_2015-12-31:116` | Item 1A › Other Risks |  |  | Competitors of the Firm’s non-U.S. wholesale businesses are typically subject to different, and in some cases, less stringent, legislative and regulatory regimes. The more restrictive laws and regulations applicable to U… |
| 5 | `AMZN_FY2015_2015-12-31:25` | Item 1 › Competition | ✓ | #1 | include selection, price, and convenience, including fast and reliable fulfillment. Additional competitive factors for our seller and enterprise services include the quality, speed, and reliability of our services and to… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#2 `JPM_FY2015_2015-12-31:14`** (cited, gold #2)

````text
ITEM 1: BUSINESS > Competition
JPMorgan Chase and its subsidiaries and affiliates operate in a highly competitive environment. Competitors include other banks, brokerage firms, investment banking companies, merchant banks, hedge funds, commodity trading companies, private equity firms, insurance companies, mutual fund companies, investment managers, credit card companies, mortgage banking companies, trust companies, securities processing companies, automobile financing companies, leasing companies, e-commerce and other Internet-based companies, financial technology companies, and other companies engaged in providing similar products and services. The Firm’s businesses generally compete on the basis of the quality and variety of the Firm’s products and services, transaction execution, innovation, reputation and price. Competition also varies based on the types of clients, customers, industries and geographies served. With respect to some of its geographies and products, JPMorgan Chase competes globally; with respect to others, the Firm competes on a national or regional basis. The Firm’s ability to compete also depends on its ability to attract and retain professional and other personnel, and on its reputation.
````

**#3 `AMZN_FY2015_2015-12-31:24`** (gold #1)

````text
Item 1. Business > Competition
Our businesses encompass a large variety of product types, service offerings, and delivery channels. The international marketplace in which we compete is evolving rapidly and intensely competitive, and we face a broad array of competitors from many different industry sectors around the world. Our current and potential competitors include: (1) online, offline, and multichannel retailers, publishers, vendors, distributors, manufacturers, and producers of the products we offer and sell to consumers and businesses; (2) publishers, producers, and distributors of physical, digital, and interactive media of all types and all distribution channels; (3) web search engines, comparison shopping websites, social networks, web portals, and other online and app-based means of discovering, using, or acquiring goods and services, either directly or in collaboration with other retailers; (4) companies that provide e-commerce services, including website development, advertising, fulfillment, customer service, and payment processing; (5) companies that provide fulfillment and logistics services for themselves or for third parties, whether online or offline; (6) companies that provide information technology services or products, including on-premises or cloud-based infrastructure and other services; and (7) companies that design, manufacture, market, or sell consumer electronics, telecommunication, and electronic devices. We believe that the principal competitive factors in our retail businesses
````

**#5 `AMZN_FY2015_2015-12-31:25`** (cited, gold #1)

````text
Item 1. Business > Competition
include selection, price, and convenience, including fast and reliable fulfillment. Additional competitive factors for our seller and enterprise services include the quality, speed, and reliability of our services and tools, as well as customers’ ability and willingness to change business practices. Some of our current and potential competitors have greater resources, longer histories, more customers, greater brand recognition, and greater control over inputs critical to our various businesses. They may secure better terms from suppliers, adopt more aggressive pricing, pursue restrictive distribution agreements that restrict our access to supply, direct consumers to their own offerings instead of ours, lock-in potential customers with restrictive terms, and devote more resources to technology, infrastructure, fulfillment, and marketing. Each of our businesses is also subject to rapid change and the development of new business models and the entry of new and well-funded competitors. Other companies also may enter into business combinations or alliances that strengthen their competitive positions.
````

</details>

RQ2 citation match (section level): `cited=[('JPM', 'Item 1'), ('AMZN', 'Item 1')] gold=[(None, 'Item 1')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 14, cited: 7.

**Generated answer**

> Amazon.com states that in its retail businesses, the principal competitive factors include selection, price, and convenience, including fast and reliable fulfillment. [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:25]  
>
> Amazon also says additional competitive factors for its seller and enterprise services include the quality, speed, and reliability of its services and tools, as well as customers’ ability and willingness to change business practices. [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:25]  
>
> More broadly, Amazon describes competition as coming from a wide range of sectors including retailers, publishers, logistics providers, IT and cloud services companies, e-commerce service providers, search and discovery platforms, and consumer device companies. [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:24]  
>
> Amazon further emphasizes that competitors may have greater resources, stronger brands, better supplier terms, more aggressive pricing, restrictive distribution arrangements, and greater ability to invest in technology, infrastructure, fulfillment, and marketing. [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:25] [AMZN FY2015, Item 1A, AMZN_FY2015_2015-12-31:36]  
>
> For JPMorgan Chase, the provided evidence blocks identify its business segments and financial services lines such as Consumer & Business Banking, Commercial Banking, Corporate & Investment Bank, and Asset Management, but they do not disclose the primary competitive factors those businesses cite in the filing. [JPM FY2015, 10-K, JPM_FY2015_2015-12-31:8] [JPM FY2015, Item 15, JPM_FY2015_2015-12-31:280] [JPM FY2015, Item 15, JPM_FY2015_2015-12-31:302] [JPM FY2015, Item 15, JPM_FY2015_2015-12-31:377]  
>
> So, based on the evidence provided, Amazon explicitly frames competition around customer-facing retail factors such as selection, price, convenience, and fulfillment quality, while JPMorgan’s specific cited competitive factors for its financial services businesses are not disclosed in the provided excerpts. [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:25] [JPM FY2015, 10-K, JPM_FY2015_2015-12-31:8] [JPM FY2015, Item 15, JPM_FY2015_2015-12-31:280] [JPM FY2015, Item 15, JPM_FY2015_2015-12-31:302] [JPM FY2015, Item 15, JPM_FY2015_2015-12-31:377]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AMZN_FY2015_2015-12-31:25` | Item 1 › Competition | ✓ | #1 | include selection, price, and convenience, including fast and reliable fulfillment. Additional competitive factors for our seller and enterprise services include the quality, speed, and reliability of our services and to… |
| 2 | `AMZN_FY2015_2015-12-31:24` | Item 1 › Competition | ✓ | #1 | Our businesses encompass a large variety of product types, service offerings, and delivery channels. The international marketplace in which we compete is evolving rapidly and intensely competitive, and we face a broad ar… |
| 3 | `AMZN_FY2015_2015-12-31:36` | Item 1A › We Face Intense Competition | ✓ |  | Our businesses are rapidly evolving and intensely competitive, and we have many competitors in different industries, including retail, e-commerce services, digital content and electronic devices, and web and infrastructu… |
| 4 | `AMZN_FY2015_2015-12-31:0` |  |  |  | 10-K 1 amzn-20151231x10k.htm FORM 10-K |
| 5 | `AMZN_FY2015_2015-12-31:1` | Washington, D.C. 20549 |  |  | ____________________________________ |
| 6 | `AMZN_FY2015_2015-12-31:10` | None |  |  | Indicate by check mark if disclosure of delinquent filers pursuant to Item 405 of Regulation S-K is not contained herein, and will not be contained, to the best of registrant’s knowledge, in definitive proxy or informati… |
| 7 | `JPM_FY2015_2015-12-31:8` | Form 10-K Index | ✓ |  | \| Part I \| \| Page \| \|---\|---\|---\| \| Item 1 \| Business \| 1 \| \| \| Overview \| 1 \| \| \| Business segments \| 1 \| \| \| Competition \| 1 \| \| \| Supervision and regulation \| 1 \| \| \| Distribution of assets, liabilities and stockholde… |
| 8 | `JPM_FY2015_2015-12-31:459` | Item 15 › Management’s discussion and analysis |  |  | \| Consumer credit portfolio \| \| \| \| \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Subprime mortgage \| 3,690 \| \| 5,056 \| \| 751 \| 1,036 \| (53) \| (27) \| (1.22) \| (0.43) \| \| Auto(a) \| 60,255 \| \| 54,536 \| \| 11… |
| 9 | `JPM_FY2015_2015-12-31:280` | Item 15 › 2014 compared with 2013 | ✓ |  | \| JPMorgan Chase \| \| \| \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| Consumer Businesses \| \| \| \| \| \| Wholesale Businesses \| \| \| \| \| Consumer & Community Banking \| \| \| \| \| \| Corporate & Investment Bank \| \| Com… |
| 10 | `JPM_FY2015_2015-12-31:201` | Item 15 › Management’s discussion and analysis |  |  | 70 JPMorgan Chase & Co./2015 Annual Report |
| 11 | `JPM_FY2015_2015-12-31:302` | Item 15 › Consumer & Business Banking | ✓ |  | \| Selected income statement data \| \| \| \| \|---\|---\|---\|---\| \| As of or for the year ended December 31, \| \| \| \| \| (in millions, except ratios) \| 2015 \| 2014 \| 2013 \| \| Revenue \| \| \| \| \| Lending- and deposit-related fees \| … |
| 12 | `JPM_FY2015_2015-12-31:377` | Item 15 › Management’s discussion and analysis | ✓ |  | \| Selected metrics \| \| \| \| \|---\|---\|---\|---\| \| Year ended December 31, (in millions, except ratios) \| 2015 \| 2014 \| 2013 \| \| Revenue by product \| \| \| \| \| Lending(a) \| $3,429 \| $3,358 \| $3,730 \| \| Treasury services(a) \| 2… |
| 13 | `JPM_FY2015_2015-12-31:687` | Item 15 › Line of business equity |  |  | \| Line of business equity \| January 1, 2016 \| December 31, \| \| \|---\|---\|---\|---\| \| (in billions) \| 2015 \| 2014 \| \| \| Consumer & Community Banking \| $51.0 \| $51.0 \| $51.0 \| \| Corporate & Investment Bank \| 64.0 \| 62.0 \| 61… |
| 14 | `JPM_FY2015_2015-12-31:400` | Item 15 › 2014 compared with 2013 |  |  | \| Client assets \| \| \| \| \|---\|---\|---\|---\| \| December 31, (in billions) \| 2015 \| 2014 \| 2013 \| \| Assets by asset class \| \| \| \| \| Liquidity \| $464 \| $461 \| $451 \| \| Fixed income \| 342 \| 359 \| 330 \| \| Equity \| 353 \| 375 \| 3… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AMZN_FY2015_2015-12-31:25`** (cited, gold #1)

````text
Item 1. Business > Competition
include selection, price, and convenience, including fast and reliable fulfillment. Additional competitive factors for our seller and enterprise services include the quality, speed, and reliability of our services and tools, as well as customers’ ability and willingness to change business practices. Some of our current and potential competitors have greater resources, longer histories, more customers, greater brand recognition, and greater control over inputs critical to our various businesses. They may secure better terms from suppliers, adopt more aggressive pricing, pursue restrictive distribution agreements that restrict our access to supply, direct consumers to their own offerings instead of ours, lock-in potential customers with restrictive terms, and devote more resources to technology, infrastructure, fulfillment, and marketing. Each of our businesses is also subject to rapid change and the development of new business models and the entry of new and well-funded competitors. Other companies also may enter into business combinations or alliances that strengthen their competitive positions.
````

**#2 `AMZN_FY2015_2015-12-31:24`** (cited, gold #1)

````text
Item 1. Business > Competition
Our businesses encompass a large variety of product types, service offerings, and delivery channels. The international marketplace in which we compete is evolving rapidly and intensely competitive, and we face a broad array of competitors from many different industry sectors around the world. Our current and potential competitors include: (1) online, offline, and multichannel retailers, publishers, vendors, distributors, manufacturers, and producers of the products we offer and sell to consumers and businesses; (2) publishers, producers, and distributors of physical, digital, and interactive media of all types and all distribution channels; (3) web search engines, comparison shopping websites, social networks, web portals, and other online and app-based means of discovering, using, or acquiring goods and services, either directly or in collaboration with other retailers; (4) companies that provide e-commerce services, including website development, advertising, fulfillment, customer service, and payment processing; (5) companies that provide fulfillment and logistics services for themselves or for third parties, whether online or offline; (6) companies that provide information technology services or products, including on-premises or cloud-based infrastructure and other services; and (7) companies that design, manufacture, market, or sell consumer electronics, telecommunication, and electronic devices. We believe that the principal competitive factors in our retail businesses
````

**#3 `AMZN_FY2015_2015-12-31:36`** (cited)

````text
Item 1A. Risk Factors > We Face Intense Competition
Our businesses are rapidly evolving and intensely competitive, and we have many competitors in different industries, including retail, e-commerce services, digital content and electronic devices, and web and infrastructure computing services. Some of our current and potential competitors have greater resources, longer histories, more customers, and/or greater brand recognition. They may secure better terms from vendors, adopt more aggressive pricing, and devote more resources to technology, infrastructure, fulfillment, and marketing. Competition may intensify as our competitors enter into business combinations or alliances and established companies in other market segments expand to become competitive with our business. In addition, new and enhanced technologies, including search, web and infrastructure computing services, digital content, and electronic devices, may increase our competition. The Internet facilitates competitive entry and comparison shopping, and increased competition may reduce our sales and profits.
````

**#7 `JPM_FY2015_2015-12-31:8`** (cited)

````text
Form 10-K Index (table)
| Part I |  | Page |
|---|---|---|
| Item 1 | Business | 1 |
|  | Overview | 1 |
|  | Business segments | 1 |
|  | Competition | 1 |
|  | Supervision and regulation | 1 |
|  | Distribution of assets, liabilities and stockholders’ equity; interest rates and interest differentials | 316–320 |
|  | Return on equity and assets | 66, 309, 316 |
|  | Securities portfolio | 321 |
|  | Loan portfolio | 112–129, 242–261, 322–327 |
|  | Summary of loan and lending-related commitments loss experience | 130–132, 262–265, 328–329 |
|  | Deposits | 278,330 |
|  | Short-term and other borrowed funds | 331 |
| Item 1A | Risk factors | 8–18 |
| Item 1B | Unresolved SEC Staff comments | 18 |
| Item 2 | Properties | 19 |
| Item 3 | Legal proceedings | 19 |
| Item 4 | Mine safety disclosures | 19 |
| Part II |  |  |
| Item 5 | Market for registrant’s common equity, related stockholder matters and issuer purchases of equity securities | 20 |
````

**#9 `JPM_FY2015_2015-12-31:280`** (cited)

````text
ITEM 15: EXHIBITS, FINANCIAL STATEMENT SCHEDULES > 2014 compared with 2013 (table)
| JPMorgan Chase |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|
| Consumer Businesses |  |  |  |  |  | Wholesale Businesses |  |  |  |
| Consumer & Community Banking |  |  |  |  |  | Corporate & Investment Bank |  | Commercial Banking | Asset Management |
| Consumer & Business Banking |  | Mortgage Banking |  | Card, Commerce Solutions & Auto |  | Banking | Markets & Investor Services | • Middle Market Banking | • Global Investment Management |
| • Consumer Banking/Chase Wealth Management • Business Banking | • Mortgage Production • Mortgage Servicing • Real Estate Portfolios | • Card Services – Credit Card – Commerce Solutions • Auto & Student | • Investment Banking • Treasury Services • Lending | • Fixed Income Markets | • Corporate Client Banking | • Global Wealth Management |  |  |  |
| • Equity Markets • Securities Services • Credit Adjustments & Other | • Commercial Term Lending |  |  |  |  |  |  |  |  |
| • Real Estate Banking |  |  |  |  |  |  |  |  |  |
````

**#11 `JPM_FY2015_2015-12-31:302`** (cited)

````text
ITEM 15: EXHIBITS, FINANCIAL STATEMENT SCHEDULES > Consumer & Business Banking (table)
| Selected income statement data |  |  |  |
|---|---|---|---|
| As of or for the year ended December 31, |  |  |  |
| (in millions, except ratios) | 2015 | 2014 | 2013 |
| Revenue |  |  |  |
| Lending- and deposit-related fees | $3,112 | $3,010 | $2,942 |
| Asset management, administration and commissions | 2,097 | 2,025 | 1,815 |
| Card income | 1,721 | 1,605 | 1,495 |
| All other income | 611 | 534 | 492 |
| Noninterest revenue | 7,541 | 7,174 | 6,744 |
| Net interest income | 10,442 | 11,052 | 10,668 |
| Total net revenue | 17,983 | 18,226 | 17,412 |
| Provision for credit losses | 254 | 305 | 347 |
| Noninterest expense | 11,916 | 12,149 | 12,162 |
| Income before income tax expense | 5,813 | 5,772 | 4,903 |
| Net income | $3,581 | $3,443 | $2,943 |
| Return on common equity | 30% | 31% | 26% |
| Overhead ratio | 66 | 67 | 70 |
| Equity (period-end and average) | $11,500 | $11,000 | $11,000 |
````

**#12 `JPM_FY2015_2015-12-31:377`** (cited)

````text
ITEM 15: EXHIBITS, FINANCIAL STATEMENT SCHEDULES > Management’s discussion and analysis (table)
| Selected metrics |  |  |  |
|---|---|---|---|
| Year ended December 31, (in millions, except ratios) | 2015 | 2014 | 2013 |
| Revenue by product |  |  |  |
| Lending(a) | $3,429 | $3,358 | $3,730 |
| Treasury services(a) | 2,581 | 2,681 | 2,649 |
| Investment banking | 730 | 684 | 575 |
| Other(a) | 145 | 159 | 138 |
| Total Commercial Banking net revenue | $6,885 | $6,882 | $7,092 |
| Investment banking revenue, gross | $2,179 | $1,986 | $1,676 |
| Revenue by client segment |  |  |  |
| Middle Market Banking(b) | $2,742 | $2,791 | $3,015 |
| Corporate Client Banking(b) | 2,012 | 1,982 | 1,911 |
| Commercial Term Lending | 1,275 | 1,252 | 1,239 |
| Real Estate Banking | 494 | 495 | 561 |
| Other | 362 | 362 | 366 |
| Total Commercial Banking net revenue | $6,885 | $6,882 | $7,092 |
| Financial ratios |  |  |  |
| Return on common equity | 15% | 18% | 19% |
| Overhead ratio | 42 | 39 | 37 |
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 1'), ('AMZN', 'Item 1A'), ('JPM', 'Item 15')] gold=[(None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 6, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Amazon.com states that in its retail businesses, the principal competitive factors include selection, price, and convenience, including fast and reliable fulfillment. [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:25] | supported | The cited text states the principal competitive factors include selection, price, and convenience, including fast and reliable fulfillment. |
| Amazon also says additional competitive factors for its seller and enterprise services include the quality, speed, and reliability of its services and tools, as well as customers’ ability and willingness to change business practices. [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:25] | supported | The evidence exactly states those additional competitive factors for seller and enterprise services. |
| More broadly, Amazon describes competition as coming from a wide range of sectors including retailers, publishers, logistics providers, IT and cloud services companies, e-commerce service providers, search and discovery platforms, and consumer device companies. [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:24] | supported | The evidence lists competitors across those sectors, including retailers, publishers, logistics, IT/cloud, e-commerce services, discovery platforms, and device companies. |
| Amazon further emphasizes that competitors may have greater resources, stronger brands, better supplier terms, more aggressive pricing, restrictive distribution arrangements, and greater ability to invest in technology, infrastructure, fulfillment, and marketing. [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:25] [AMZN FY2015, Item 1A, AMZN_FY2015_2015-12-31:36] | supported | The cited passages state competitors may have greater resources and brand recognition, secure better supplier terms, use aggressive pricing, restrictive distribution, and invest more in technology, infrastructure, fulfillment, and marketing. |
| For JPMorgan Chase, the provided evidence blocks identify its business segments and financial services lines such as Consumer & Business Banking, Commercial Banking, Corporate & Investment Bank, and Asset Management, but they do not disclose the primary competitive factors those businesses cite in the filing. [JPM FY2015, 10-K, JPM_FY2015_2015-12-31:8] [JPM FY2015, Item 15, JPM_FY2015_2015-12-31:280] [JPM FY2015, Item 15, JPM_FY2015_2015-12-31:302] [JPM FY2015, Item 15, JPM_FY2015_2015-12-31:377] | supported | The JPM excerpts identify segments and business lines but do not provide the businesses’ primary competitive factors. |
| So, based on the evidence provided, Amazon explicitly frames competition around customer-facing retail factors such as selection, price, convenience, and fulfillment quality, while JPMorgan’s specific cited competitive factors for its financial services businesses are not disclosed in the provided excerpts. [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:25] [JPM FY2015, 10-K, JPM_FY2015_2015-12-31:8] [JPM FY2015, Item 15, JPM_FY2015_2015-12-31:280] [JPM FY2015, Item 15, JPM_FY2015_2015-12-31:302] [JPM FY2015, Item 15, JPM_FY2015_2015-12-31:377] | supported | Amazon’s excerpt explicitly gives retail competitive factors, while the provided JPM excerpts do not disclose specific competitive factors for those businesses. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 12, cited: 3.

**Generated answer**

> Amazon.com states that the principal competitive factors in its retail businesses include selection, price, and convenience, including fast and reliable fulfillment. [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:25] [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:24]
>
> Amazon also says that for its seller and enterprise services, additional competitive factors include the quality, speed, and reliability of its services and tools, as well as customers’ ability and willingness to change business practices. [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:25]
>
> JPMorgan Chase states that its businesses generally compete on the basis of the quality and variety of the Firm’s products and services, transaction execution, innovation, reputation and price. [JPM FY2015, Item 1, JPM_FY2015_2015-12-31:14]
>
> So, Amazon emphasizes consumer-facing retail factors such as broad selection, low price, convenience, and fulfillment speed and reliability, while JPMorgan emphasizes financial-services factors such as product and service quality and variety, transaction execution, innovation, reputation, and price. [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:25] [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:24] [JPM FY2015, Item 1, JPM_FY2015_2015-12-31:14]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AMZN_FY2015_2015-12-31:25` | Item 1 › Competition | ✓ | #1 | include selection, price, and convenience, including fast and reliable fulfillment. Additional competitive factors for our seller and enterprise services include the quality, speed, and reliability of our services and to… |
| 2 | `AMZN_FY2015_2015-12-31:24` | Item 1 › Competition | ✓ | #1 | Our businesses encompass a large variety of product types, service offerings, and delivery channels. The international marketplace in which we compete is evolving rapidly and intensely competitive, and we face a broad ar… |
| 3 | `AMZN_FY2015_2015-12-31:36` | Item 1A › We Face Intense Competition |  |  | Our businesses are rapidly evolving and intensely competitive, and we have many competitors in different industries, including retail, e-commerce services, digital content and electronic devices, and web and infrastructu… |
| 4 | `AMZN_FY2015_2015-12-31:37` | Item 1A › Our Expansion Places a Significant Strain on our Management, Operational, Financial, and Other Resources |  |  | We are rapidly and significantly expanding our global operations, including increasing our product and service offerings and scaling our infrastructure to support our retail and services businesses. This expansion increa… |
| 5 | `AMZN_FY2015_2015-12-31:206` | Item 8 › Description of Business |  |  | Amazon.com opened its virtual doors on the World Wide Web in July 1995. We seek to be Earth’s most customer-centric company. In each of our segments, we serve our primary customer sets, consisting of consumers, sellers, … |
| 6 | `AMZN_FY2015_2015-12-31:45` | Item 1A › Our International Operations Expose Us to a Number of Risks |  |  | The People’s Republic of China (“PRC”) and India regulate Amazon’s and its affiliates’ businesses and operations in country through regulations and license requirements that may restrict (i) foreign investment in and ope… |
| 7 | `JPM_FY2015_2015-12-31:14` | Item 1 › Competition | ✓ | #2 | JPMorgan Chase and its subsidiaries and affiliates operate in a highly competitive environment. Competitors include other banks, brokerage firms, investment banking companies, merchant banks, hedge funds, commodity tradi… |
| 8 | `JPM_FY2015_2015-12-31:15` | Item 1 › Competition |  |  | It is likely that competition in the financial services industry will become even more intense as the Firm’s businesses continue to compete with other financial institutions that may have a stronger local presence in cer… |
| 9 | `JPM_FY2015_2015-12-31:114` | Item 1A › Other Risks |  |  | The financial services industry is highly competitive, and JPMorgan Chase’s inability to compete successfully may adversely affect its results of operations. JPMorgan Chase operates in a highly competitive environment, a… |
| 10 | `JPM_FY2015_2015-12-31:10` | Item 1 › Overview |  |  | JPMorgan Chase & Co., (“JPMorgan Chase” or the “Firm”) a financial holding company incorporated under Delaware law in 1968, is a leading global financial services firm and one of the largest banking institutions in the U… |
| 11 | `JPM_FY2015_2015-12-31:1591` | Item 5 › Note 33 – Business segments |  |  | The Firm is managed on a line of business basis. There are four major reportable business segments – Consumer & Community Banking, Corporate & Investment Bank, Commercial Banking and Asset Management. In addition, there … |
| 12 | `JPM_FY2015_2015-12-31:13` | Item 1 › Business segments |  |  | JPMorgan Chase’s activities are organized, for management reporting purposes, into four major reportable business segments, as well as a Corporate segment. The Firm’s consumer business is the Consumer & Community Banking… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AMZN_FY2015_2015-12-31:25`** (cited, gold #1)

````text
Item 1. Business > Competition
include selection, price, and convenience, including fast and reliable fulfillment. Additional competitive factors for our seller and enterprise services include the quality, speed, and reliability of our services and tools, as well as customers’ ability and willingness to change business practices. Some of our current and potential competitors have greater resources, longer histories, more customers, greater brand recognition, and greater control over inputs critical to our various businesses. They may secure better terms from suppliers, adopt more aggressive pricing, pursue restrictive distribution agreements that restrict our access to supply, direct consumers to their own offerings instead of ours, lock-in potential customers with restrictive terms, and devote more resources to technology, infrastructure, fulfillment, and marketing. Each of our businesses is also subject to rapid change and the development of new business models and the entry of new and well-funded competitors. Other companies also may enter into business combinations or alliances that strengthen their competitive positions.
````

**#2 `AMZN_FY2015_2015-12-31:24`** (cited, gold #1)

````text
Item 1. Business > Competition
Our businesses encompass a large variety of product types, service offerings, and delivery channels. The international marketplace in which we compete is evolving rapidly and intensely competitive, and we face a broad array of competitors from many different industry sectors around the world. Our current and potential competitors include: (1) online, offline, and multichannel retailers, publishers, vendors, distributors, manufacturers, and producers of the products we offer and sell to consumers and businesses; (2) publishers, producers, and distributors of physical, digital, and interactive media of all types and all distribution channels; (3) web search engines, comparison shopping websites, social networks, web portals, and other online and app-based means of discovering, using, or acquiring goods and services, either directly or in collaboration with other retailers; (4) companies that provide e-commerce services, including website development, advertising, fulfillment, customer service, and payment processing; (5) companies that provide fulfillment and logistics services for themselves or for third parties, whether online or offline; (6) companies that provide information technology services or products, including on-premises or cloud-based infrastructure and other services; and (7) companies that design, manufacture, market, or sell consumer electronics, telecommunication, and electronic devices. We believe that the principal competitive factors in our retail businesses
````

**#7 `JPM_FY2015_2015-12-31:14`** (cited, gold #2)

````text
ITEM 1: BUSINESS > Competition
JPMorgan Chase and its subsidiaries and affiliates operate in a highly competitive environment. Competitors include other banks, brokerage firms, investment banking companies, merchant banks, hedge funds, commodity trading companies, private equity firms, insurance companies, mutual fund companies, investment managers, credit card companies, mortgage banking companies, trust companies, securities processing companies, automobile financing companies, leasing companies, e-commerce and other Internet-based companies, financial technology companies, and other companies engaged in providing similar products and services. The Firm’s businesses generally compete on the basis of the quality and variety of the Firm’s products and services, transaction execution, innovation, reputation and price. Competition also varies based on the types of clients, customers, industries and geographies served. With respect to some of its geographies and products, JPMorgan Chase competes globally; with respect to others, the Firm competes on a national or regional basis. The Firm’s ability to compete also depends on its ability to attract and retain professional and other personnel, and on its reputation.
````

</details>

RQ2 citation match (section level): `cited=[('AMZN', 'Item 1'), ('JPM', 'Item 1')] gold=[(None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 4, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Amazon.com states that the principal competitive factors in its retail businesses include selection, price, and convenience, including fast and reliable fulfillment. [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:25] [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:24] | supported | The cited Amazon evidence states the principal competitive factors include selection, price, and convenience, including fast and reliable fulfillment. |
| Amazon also says that for its seller and enterprise services, additional competitive factors include the quality, speed, and reliability of its services and tools, as well as customers’ ability and willingness to change business practices. [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:25] | supported | The cited evidence exactly states those additional competitive factors for seller and enterprise services. |
| JPMorgan Chase states that its businesses generally compete on the basis of the quality and variety of the Firm’s products and services, transaction execution, innovation, reputation and price. [JPM FY2015, Item 1, JPM_FY2015_2015-12-31:14] | supported | The JPMorgan evidence explicitly says its businesses generally compete on those bases. |
| So, Amazon emphasizes consumer-facing retail factors such as broad selection, low price, convenience, and fulfillment speed and reliability, while JPMorgan emphasizes financial-services factors such as product and service quality and variety, transaction execution, innovation, reputation, and price. [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:25] [AMZN FY2015, Item 1, AMZN_FY2015_2015-12-31:24] [JPM FY2015, Item 1, JPM_FY2015_2015-12-31:14] | supported | The cited evidence supports Amazon’s retail-focused factors and JPMorgan’s listed financial-services competitive factors as a comparative summary. |

</details>
