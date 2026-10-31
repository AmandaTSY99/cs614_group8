# gold-027: Cross-year text

[← all cases](../README.md) · company: Alphabet Inc. (GOOGL) · fiscal year: 2019 · recipe `cross_year_text` · hop `multi` · answer type `qualitative` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> How did the composition of Alphabet's 'Other Bets' segment change between fiscal year 2015 and fiscal year 2019, specifically regarding which distinct business units were explicitly named in each year's disclosure?

**Gold answer**

> In fiscal 2015 (after the Alphabet reorganization), Other Bets was described as including Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X and other initiatives. In fiscal 2019, it was described as including Access, Calico, CapitalG, GV, Verily, Waymo and X, among others. Nest and Google Capital are no longer named in 2019, while CapitalG and Waymo are newly named.

**Key points** (RQ3 keypoint_recall targets)

1. 2015: Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital and X.
2. 2019: Access, Calico, CapitalG, GV, Verily, Waymo and X.
3. Nest and Google Capital are not named in 2019.
4. CapitalG and Waymo are newly named in 2019.

**Gold evidence**

1. `GOOGL_FY2019_2019-12-31` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Information about Segments · text

   > Other Bets includes Access, Calico, CapitalG, GV, Verily, Waymo, and X, among others.

2. `GOOGL_FY2015_2015-12-31` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS › Information about Segments · text

   > Other Bets includes businesses such as Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and other initiatives.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 9 | 10 |
| recall@5 | 0.50 | 0.50 | 1.00 | 1.00 |
| recall@all | 0.50 | 0.50 | 1.00 | 1.00 |
| complete@all | 0 | 0 | 1 | 1 |
| average precision (lexical) | 0.62 | 0.83 | 1.00 | 1.00 |
| gold evidence first rank | #1: –, #2: 1 | #1: –, #2: 1 | #1: 3, #2: 1 | #1: 3, #2: 1 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | 0.75 | 0.75 | 1.00 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 0.33 | 0.33 | 0.50 | 0.50 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 0.50 | 0.50 | 0.67 | 0.67 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 2 |
| tokens | 1940 | 1490 | 24206 | 11883 |
| cost (USD) | 0.0004 | 0.0003 | 0.0876 | 0.0436 |
| latency (s) | 4.4 | 6.5 | 35.4 | 18.2 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 4.

**Generated answer**

> In FY2015, Alphabet explicitly named these businesses in Other Bets: **Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and other initiatives** [1][8].
>
> In FY2019, the disclosure in the provided context **does not list the full set of distinct business units** in Other Bets. It only explicitly mentions that revenues were primarily generated from **internet and TV services** and **licensing and R&D services**, and specifically refers to **Access** and **Verily** in the revenue discussion [5][7].
>
> So, based on the provided context, the change that can be identified is:
> - **FY2015:** a detailed list of named units was provided [1][8].
> - **FY2019:** no comparable full list of named units was provided in the context; only **Access** and **Verily** were explicitly referenced in connection with revenue sources [5][7].
>
> What is **not in the context**: a complete FY2019 named roster of Other Bets business units, so a full unit-by-unit comparison cannot be made from the provided excerpts.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2015_2015-12-31:525` | Item 8 › Note 16. Information about Segments and Geographic Areas | ✓ | #2 | • Other Bets – Other Bets is a combination of multiple operating segments that are not individually material. Other Bets includes businesses such as Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and o… |
| 2 | `GOOGL_FY2019_2019-12-31:161` | Item 7 › Other Bets |  |  | The following table presents our Other Bets revenues (in millions): |
| 3 | `GOOGL_FY2015_2015-12-31:183` | Item 7 › Other Bets |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2013 \| 2014 \| 2015 \| \| Other Bets revenues \| $12 \| $327 \| $448 \| \| Other Bets revenues as a percentage of consolidated revenues \| 0.0% \| 0.5% \| 0.6% \| |
| 4 | `GOOGL_FY2015_2015-12-31:182` | Item 7 › Other Bets |  |  | The following table presents our Other Bets revenues (in millions), and those revenues expressed as a percentage of consolidated revenues, for the periods presented: |
| 5 | `GOOGL_FY2019_2019-12-31:35` | Item 1 › Other Bets | ✓ |  | Throughout Alphabet, we are also using technology to try and solve big problems across many industries. Alphabet’s investment in our portfolio of Other Bets include emerging businesses at various stages of development, r… |
| 6 | `GOOGL_FY2019_2019-12-31:162` | Item 7 › Other Bets |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2017 \| 2018 \| 2019 \| \| Other Bets revenues \| $477 \| $595 \| $659 \| \| Other Bets revenues as a percentage of total revenues \| 0.4% \| 0.4% \| 0.4% \| |
| 7 | `GOOGL_FY2019_2019-12-31:163` | Item 7 › Other Bets | ✓ |  | Other Bets revenues consist primarily of revenues from sales of Access internet and TV services and Verily licensing and R&D services. |
| 8 | `GOOGL_FY2015_2015-12-31:158` | Item 7 › Information about Segments | ✓ | #2 | In conjunction with the Alphabet reorganization, in the fourth quarter of 2015, we implemented legal and operational changes in how our Chief Operating Decision Maker (CODM) manages our businesses, including resource all… |
| 9 | `GOOGL_FY2015_2015-12-31:184` | Item 7 › Other Bets |  |  | Other Bets revenues consist primarily of: • Sales of Nest branded hardware; • Revenues from internet and TV services; and • Revenues from licensing and R&D services. Our Other Bets revenues increased $121 million from 20… |
| 10 | `GOOGL_FY2015_2015-12-31:531` | Item 8 › Note 16. Information about Segments and Geographic Areas |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2013 \| 2014 \| 2015 \| \| Stock-based compensation: \| \| \| \| \| Google \| $2,911 \| $3,677 \| $4,587 \| \| Other Bets \| 124 \| 347 \| 498 \| \| Reconciling items(3) \| 92 \| 151 \| … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2015_2015-12-31:525`** (cited, gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 16. Information about Segments and Geographic Areas
• Other Bets – Other Bets is a combination of multiple operating segments that are not individually material. Other Bets includes businesses such as Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and other initiatives. Revenues from the Other Bets is derived primarily through the sales of Nest hardware products, internet and TV services through Google Fiber and licensing and R&D services through Verily. Revenue, cost of revenue, and operating expenses are generally directly attributed to our segments. Inter-segment revenues are not presented separately, as these amounts are immaterial. Our CODM does not evaluate operating segments using asset information. Information about segments during the periods presented were as follows (in millions):
````

**#5 `GOOGL_FY2019_2019-12-31:35`** (cited)

````text
ITEM 1. BUSINESS > Other Bets
Throughout Alphabet, we are also using technology to try and solve big problems across many industries. Alphabet’s investment in our portfolio of Other Bets include emerging businesses at various stages of development, ranging from those in the research and development phase to those that are in the beginning stages of commercialization, and our goal is for them to become thriving, successful businesses in the medium to long term. While these early-stage businesses naturally come with considerable uncertainty, some of them are already generating revenue and making important strides in their industries. Revenues are primarily generated from internet and TV services, as well as licensing and R&D services. Other Bets operate as independent companies and some of them have their own boards with independent members and outside investors. We are investing in our portfolio of Other Bets and being very deliberate about the focus, scale, and pace of investments.
````

**#7 `GOOGL_FY2019_2019-12-31:163`** (cited)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Other Bets
Other Bets revenues consist primarily of revenues from sales of Access internet and TV services and Verily licensing and R&D services.
````

**#8 `GOOGL_FY2015_2015-12-31:158`** (cited, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Information about Segments
In conjunction with the Alphabet reorganization, in the fourth quarter of 2015, we implemented legal and operational changes in how our Chief Operating Decision Maker (CODM) manages our businesses, including resource allocation and performance assessment. Consequently, we have multiple operating segments, representing the individual businesses that are run separately under the Alphabet structure. Google is our only reportable segment. None of our other segments meet the quantitative thresholds to qualify as reportable segments; therefore, the operating segments are combined and disclosed below as Other Bets. All prior-period amounts have been adjusted retrospectively to reflect the reportable segment change. Our reported segments are described below: • Google – Google includes our main internet products such as Search, Ads, Commerce, Maps, YouTube, Apps, Cloud, Android, Chrome, Google Play as well as hardware products we sell, such as Chromecast, Chromebooks and Nexus. Our technical infrastructure and newer efforts like Virtual Reality are also included in Google. • Other Bets – Other Bets is a combination of multiple operating segments that are not individually material. Other Bets includes businesses such as Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and other initiatives.
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8'), ('GOOGL', 'Item 1'), ('GOOGL', 'Item 7')] gold=[(None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 3.

**Generated answer**

> In FY2015, Alphabet explicitly named these businesses within Other Bets: Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and other initiatives [1][3].
>
> In FY2019, the disclosure did not explicitly list distinct business units by name. It described Other Bets more generally as a portfolio of emerging businesses generating revenues primarily from internet and TV services, and licensing and R&D services [4].
>
> So, the change is that FY2015 provided a specific named list of business units, while FY2019 did not name individual units in the disclosure [1][3][4].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2015_2015-12-31:158` | Item 7 › Information about Segments | ✓ | #2 | In conjunction with the Alphabet reorganization, in the fourth quarter of 2015, we implemented legal and operational changes in how our Chief Operating Decision Maker (CODM) manages our businesses, including resource all… |
| 2 | `GOOGL_FY2015_2015-12-31:524` | Item 8 › Note 16. Information about Segments and Geographic Areas |  |  | In conjunction with the Alphabet reorganization, in the fourth quarter of 2015, we implemented legal and operational changes in how our Chief Operating Decision Maker (CODM) manages our businesses, including resource all… |
| 3 | `GOOGL_FY2015_2015-12-31:525` | Item 8 › Note 16. Information about Segments and Geographic Areas | ✓ | #2 | • Other Bets – Other Bets is a combination of multiple operating segments that are not individually material. Other Bets includes businesses such as Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and o… |
| 4 | `GOOGL_FY2019_2019-12-31:35` | Item 1 › Other Bets | ✓ |  | Throughout Alphabet, we are also using technology to try and solve big problems across many industries. Alphabet’s investment in our portfolio of Other Bets include emerging businesses at various stages of development, r… |
| 5 | `GOOGL_FY2015_2015-12-31:157` | Item 7 › Executive Overview of Results |  |  | Here are our key financial results for the fiscal year ended December 31, 2015 (consolidated unless otherwise noted): • Revenues of $75.0 billion and revenue growth of 14% year over year, constant currency revenue growth… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2015_2015-12-31:158`** (cited, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Information about Segments
In conjunction with the Alphabet reorganization, in the fourth quarter of 2015, we implemented legal and operational changes in how our Chief Operating Decision Maker (CODM) manages our businesses, including resource allocation and performance assessment. Consequently, we have multiple operating segments, representing the individual businesses that are run separately under the Alphabet structure. Google is our only reportable segment. None of our other segments meet the quantitative thresholds to qualify as reportable segments; therefore, the operating segments are combined and disclosed below as Other Bets. All prior-period amounts have been adjusted retrospectively to reflect the reportable segment change. Our reported segments are described below: • Google – Google includes our main internet products such as Search, Ads, Commerce, Maps, YouTube, Apps, Cloud, Android, Chrome, Google Play as well as hardware products we sell, such as Chromecast, Chromebooks and Nexus. Our technical infrastructure and newer efforts like Virtual Reality are also included in Google. • Other Bets – Other Bets is a combination of multiple operating segments that are not individually material. Other Bets includes businesses such as Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and other initiatives.
````

**#3 `GOOGL_FY2015_2015-12-31:525`** (cited, gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 16. Information about Segments and Geographic Areas
• Other Bets – Other Bets is a combination of multiple operating segments that are not individually material. Other Bets includes businesses such as Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and other initiatives. Revenues from the Other Bets is derived primarily through the sales of Nest hardware products, internet and TV services through Google Fiber and licensing and R&D services through Verily. Revenue, cost of revenue, and operating expenses are generally directly attributed to our segments. Inter-segment revenues are not presented separately, as these amounts are immaterial. Our CODM does not evaluate operating segments using asset information. Information about segments during the periods presented were as follows (in millions):
````

**#4 `GOOGL_FY2019_2019-12-31:35`** (cited)

````text
ITEM 1. BUSINESS > Other Bets
Throughout Alphabet, we are also using technology to try and solve big problems across many industries. Alphabet’s investment in our portfolio of Other Bets include emerging businesses at various stages of development, ranging from those in the research and development phase to those that are in the beginning stages of commercialization, and our goal is for them to become thriving, successful businesses in the medium to long term. While these early-stage businesses naturally come with considerable uncertainty, some of them are already generating revenue and making important strides in their industries. Revenues are primarily generated from internet and TV services, as well as licensing and R&D services. Other Bets operate as independent companies and some of them have their own boards with independent members and outside investors. We are investing in our portfolio of Other Bets and being very deliberate about the focus, scale, and pace of investments.
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 7'), ('GOOGL', 'Item 8'), ('GOOGL', 'Item 1')] gold=[(None, 'Item 7')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 9, cited: 4.

**Generated answer**

> In fiscal year 2015, Alphabet disclosed that Other Bets included Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and other initiatives. [GOOGL FY2015, Item 8, GOOGL_FY2015_2015-12-31:525] [GOOGL FY2015, Item 7, GOOGL_FY2015_2015-12-31:158]
>
> In fiscal year 2019, Alphabet disclosed that Other Bets included Access, Calico, CapitalG, GV, Verily, Waymo, and X, among others. [GOOGL FY2019, Item 8, GOOGL_FY2019_2019-12-31:464] [GOOGL FY2019, Item 7, GOOGL_FY2019_2019-12-31:142]
>
> Comparing the explicit names in those disclosures, Nest and Google Capital were explicitly named in 2015 but not in 2019, while CapitalG and Waymo were explicitly named in 2019 but not in 2015. Access/Google Fiber appeared in 2015, whereas Access appeared in 2019. [GOOGL FY2015, Item 8, GOOGL_FY2015_2015-12-31:525] [GOOGL FY2015, Item 7, GOOGL_FY2015_2015-12-31:158] [GOOGL FY2019, Item 8, GOOGL_FY2019_2019-12-31:464] [GOOGL FY2019, Item 7, GOOGL_FY2019_2019-12-31:142]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2015_2015-12-31:525` | Item 8 › Note 16. Information about Segments and Geographic Areas | ✓ | #2 | • Other Bets – Other Bets is a combination of multiple operating segments that are not individually material. Other Bets includes businesses such as Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and o… |
| 2 | `GOOGL_FY2015_2015-12-31:158` | Item 7 › Information about Segments | ✓ | #2 | In conjunction with the Alphabet reorganization, in the fourth quarter of 2015, we implemented legal and operational changes in how our Chief Operating Decision Maker (CODM) manages our businesses, including resource all… |
| 3 | `GOOGL_FY2019_2019-12-31:464` | Item 8 › Note 15. Information about Segments and Geographic Areas | ✓ | #1 | We operate our business in multiple operating segments. Google is our only reportable segment. None of our other segments meet the quantitative thresholds to qualify as reportable segments; therefore, the other operating… |
| 4 | `GOOGL_FY2019_2019-12-31:142` | Item 7 › Information about Segments | ✓ | #1 | We operate our business in multiple operating segments. Google is our only reportable segment. None of our other segments meet the quantitative thresholds to qualify as reportable segments; therefore, the other operating… |
| 5 | `GOOGL_FY2019_2019-12-31:35` | Item 1 › Other Bets |  |  | Throughout Alphabet, we are also using technology to try and solve big problems across many industries. Alphabet’s investment in our portfolio of Other Bets include emerging businesses at various stages of development, r… |
| 6 | `GOOGL_FY2015_2015-12-31:527` | Item 8 › Note 16. Information about Segments and Geographic Areas |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2013 \| 2014 \| 2015 \| \| Segment operating income (loss): \| \| \| \| \| Google \| $16,260 \| $19,011 \| $23,425 \| \| Other Bets \| (527) \| (1,942) \| (3,567) \| \| Reconciling it… |
| 7 | `GOOGL_FY2019_2019-12-31:163` | Item 7 › Other Bets |  |  | Other Bets revenues consist primarily of revenues from sales of Access internet and TV services and Verily licensing and R&D services. |
| 8 | `GOOGL_FY2019_2019-12-31:25` | Item 1 › Access and technology for everyone |  |  | Our Other Bets are also pursuing initiatives with similar goals. For instance, as a part of our efforts in the Metro Phoenix area, Waymo is working toward our goal of making transportation safer and easier for everyone w… |
| 9 | `GOOGL_FY2015_2015-12-31:524` | Item 8 › Note 16. Information about Segments and Geographic Areas |  |  | In conjunction with the Alphabet reorganization, in the fourth quarter of 2015, we implemented legal and operational changes in how our Chief Operating Decision Maker (CODM) manages our businesses, including resource all… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2015_2015-12-31:525`** (cited, gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 16. Information about Segments and Geographic Areas
• Other Bets – Other Bets is a combination of multiple operating segments that are not individually material. Other Bets includes businesses such as Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and other initiatives. Revenues from the Other Bets is derived primarily through the sales of Nest hardware products, internet and TV services through Google Fiber and licensing and R&D services through Verily. Revenue, cost of revenue, and operating expenses are generally directly attributed to our segments. Inter-segment revenues are not presented separately, as these amounts are immaterial. Our CODM does not evaluate operating segments using asset information. Information about segments during the periods presented were as follows (in millions):
````

**#2 `GOOGL_FY2015_2015-12-31:158`** (cited, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Information about Segments
In conjunction with the Alphabet reorganization, in the fourth quarter of 2015, we implemented legal and operational changes in how our Chief Operating Decision Maker (CODM) manages our businesses, including resource allocation and performance assessment. Consequently, we have multiple operating segments, representing the individual businesses that are run separately under the Alphabet structure. Google is our only reportable segment. None of our other segments meet the quantitative thresholds to qualify as reportable segments; therefore, the operating segments are combined and disclosed below as Other Bets. All prior-period amounts have been adjusted retrospectively to reflect the reportable segment change. Our reported segments are described below: • Google – Google includes our main internet products such as Search, Ads, Commerce, Maps, YouTube, Apps, Cloud, Android, Chrome, Google Play as well as hardware products we sell, such as Chromecast, Chromebooks and Nexus. Our technical infrastructure and newer efforts like Virtual Reality are also included in Google. • Other Bets – Other Bets is a combination of multiple operating segments that are not individually material. Other Bets includes businesses such as Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and other initiatives.
````

**#3 `GOOGL_FY2019_2019-12-31:464`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 15. Information about Segments and Geographic Areas
We operate our business in multiple operating segments. Google is our only reportable segment. None of our other segments meet the quantitative thresholds to qualify as reportable segments; therefore, the other operating segments are combined and disclosed as Other Bets. Our reported segments are: • Google – Google includes our main products such as ads, Android, Chrome, hardware, Google Cloud, Google Maps, Google Play, Search, and YouTube. Our technical infrastructure is also included in Google. Google generates revenues primarily from advertising; sales of apps, in-app purchases, digital content products, and hardware; and licensing and service fees, including fees received for Google Cloud offerings and subscription-based products. • Other Bets – Other Bets is a combination of multiple operating segments that are not individually material. Other Bets includes Access, Calico, CapitalG, GV, Verily, Waymo, and X, among others. Revenues from the Other Bets are derived primarily through the sales of internet and TV services through Access as well as licensing and R&D services through Verily. Table of Contents Alphabet Inc.
````

**#4 `GOOGL_FY2019_2019-12-31:142`** (cited, gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Information about Segments
We operate our business in multiple operating segments. Google is our only reportable segment. None of our other segments meet the quantitative thresholds to qualify as reportable segments; therefore, the other operating segments are combined and disclosed as Other Bets. Table of Contents Alphabet Inc. Our reported segments are: • Google – Google includes our main products such as ads, Android, Chrome, hardware, Google Cloud, Google Maps, Google Play, Search, and YouTube. Our technical infrastructure is also included in Google. Google generates revenues primarily from advertising; sales of apps, in-app purchases, digital content products, and hardware; and licensing and service fees, including fees received for Google Cloud offerings and subscription-based products. • Other Bets – Other Bets is a combination of multiple operating segments that are not individually material. Other Bets includes Access, Calico, CapitalG, GV, Verily, Waymo, and X, among others. Revenues from the Other Bets are derived primarily through the sales of internet and TV services through Access as well as licensing and R&D services through Verily.
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8'), ('GOOGL', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 4, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In fiscal year 2015, Alphabet disclosed that Other Bets included Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and other initiatives. [GOOGL FY2015, Item 8, GOOGL_FY2015_2015-12-31:525] [GOOGL FY2015, Item 7, GOOGL_FY2015_2015-12-31:158] | supported | Both cited passages explicitly list Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and other initiatives in Other Bets for 2015. |
| In fiscal year 2019, Alphabet disclosed that Other Bets included Access, Calico, CapitalG, GV, Verily, Waymo, and X, among others. [GOOGL FY2019, Item 8, GOOGL_FY2019_2019-12-31:464] [GOOGL FY2019, Item 7, GOOGL_FY2019_2019-12-31:142] | supported | Both cited passages explicitly state that 2019 Other Bets included Access, Calico, CapitalG, GV, Verily, Waymo, and X, among others. |
| Comparing the explicit names in those disclosures, Nest and Google Capital were explicitly named in 2015 but not in 2019, while CapitalG and Waymo were explicitly named in 2019 but not in 2015. | supported | The retrieved 2015 disclosures name Nest and Google Capital but not CapitalG or Waymo, while the 2019 disclosures name CapitalG and Waymo but not Nest or Google Capital. |
| Access/Google Fiber appeared in 2015, whereas Access appeared in 2019. [GOOGL FY2015, Item 8, GOOGL_FY2015_2015-12-31:525] [GOOGL FY2015, Item 7, GOOGL_FY2015_2015-12-31:158] [GOOGL FY2019, Item 8, GOOGL_FY2019_2019-12-31:464] [GOOGL FY2019, Item 7, GOOGL_FY2019_2019-12-31:142] | supported | The 2015 evidence uses the label Access/Google Fiber, whereas the 2019 evidence uses Access. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 10, cited: 4.

**Generated answer**

> In fiscal year 2015, Alphabet disclosed that Other Bets included Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and other initiatives. [GOOGL FY2015, Item 8, GOOGL_FY2015_2015-12-31:525] [GOOGL FY2015, Item 7, GOOGL_FY2015_2015-12-31:158]
>
> In fiscal year 2019, Alphabet disclosed that Other Bets included Access, Calico, CapitalG, GV, Verily, Waymo, and X, among others. [GOOGL FY2019, Item 8, GOOGL_FY2019_2019-12-31:464] [GOOGL FY2019, Item 7, GOOGL_FY2019_2019-12-31:142]
>
> Comparing the named businesses, Nest and Google Fiber were explicitly named in 2015 but were not explicitly named in 2019, while Waymo was explicitly named in 2019 but was not explicitly named in 2015. [GOOGL FY2015, Item 8, GOOGL_FY2015_2015-12-31:525] [GOOGL FY2015, Item 7, GOOGL_FY2015_2015-12-31:158] [GOOGL FY2019, Item 8, GOOGL_FY2019_2019-12-31:464] [GOOGL FY2019, Item 7, GOOGL_FY2019_2019-12-31:142]
>
> The naming also changed from Google Capital in 2015 to CapitalG in 2019, and from Access/Google Fiber in 2015 to Access in 2019. [GOOGL FY2015, Item 8, GOOGL_FY2015_2015-12-31:525] [GOOGL FY2015, Item 7, GOOGL_FY2015_2015-12-31:158] [GOOGL FY2019, Item 8, GOOGL_FY2019_2019-12-31:464] [GOOGL FY2019, Item 7, GOOGL_FY2019_2019-12-31:142]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `GOOGL_FY2015_2015-12-31:525` | Item 8 › Note 16. Information about Segments and Geographic Areas | ✓ | #2 | • Other Bets – Other Bets is a combination of multiple operating segments that are not individually material. Other Bets includes businesses such as Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and o… |
| 2 | `GOOGL_FY2015_2015-12-31:158` | Item 7 › Information about Segments | ✓ | #2 | In conjunction with the Alphabet reorganization, in the fourth quarter of 2015, we implemented legal and operational changes in how our Chief Operating Decision Maker (CODM) manages our businesses, including resource all… |
| 3 | `GOOGL_FY2019_2019-12-31:464` | Item 8 › Note 15. Information about Segments and Geographic Areas | ✓ | #1 | We operate our business in multiple operating segments. Google is our only reportable segment. None of our other segments meet the quantitative thresholds to qualify as reportable segments; therefore, the other operating… |
| 4 | `GOOGL_FY2019_2019-12-31:142` | Item 7 › Information about Segments | ✓ | #1 | We operate our business in multiple operating segments. Google is our only reportable segment. None of our other segments meet the quantitative thresholds to qualify as reportable segments; therefore, the other operating… |
| 5 | `GOOGL_FY2019_2019-12-31:35` | Item 1 › Other Bets |  |  | Throughout Alphabet, we are also using technology to try and solve big problems across many industries. Alphabet’s investment in our portfolio of Other Bets include emerging businesses at various stages of development, r… |
| 6 | `GOOGL_FY2015_2015-12-31:527` | Item 8 › Note 16. Information about Segments and Geographic Areas |  |  | \| \| Year Ended December 31, \| \| \| \|---\|---\|---\|---\| \| \| 2013 \| 2014 \| 2015 \| \| Segment operating income (loss): \| \| \| \| \| Google \| $16,260 \| $19,011 \| $23,425 \| \| Other Bets \| (527) \| (1,942) \| (3,567) \| \| Reconciling it… |
| 7 | `GOOGL_FY2019_2019-12-31:161` | Item 7 › Other Bets |  |  | The following table presents our Other Bets revenues (in millions): |
| 8 | `GOOGL_FY2019_2019-12-31:163` | Item 7 › Other Bets |  |  | Other Bets revenues consist primarily of revenues from sales of Access internet and TV services and Verily licensing and R&D services. |
| 9 | `GOOGL_FY2019_2019-12-31:25` | Item 1 › Access and technology for everyone |  |  | Our Other Bets are also pursuing initiatives with similar goals. For instance, as a part of our efforts in the Metro Phoenix area, Waymo is working toward our goal of making transportation safer and easier for everyone w… |
| 10 | `GOOGL_FY2015_2015-12-31:182` | Item 7 › Other Bets |  |  | The following table presents our Other Bets revenues (in millions), and those revenues expressed as a percentage of consolidated revenues, for the periods presented: |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `GOOGL_FY2015_2015-12-31:525`** (cited, gold #2)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 16. Information about Segments and Geographic Areas
• Other Bets – Other Bets is a combination of multiple operating segments that are not individually material. Other Bets includes businesses such as Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and other initiatives. Revenues from the Other Bets is derived primarily through the sales of Nest hardware products, internet and TV services through Google Fiber and licensing and R&D services through Verily. Revenue, cost of revenue, and operating expenses are generally directly attributed to our segments. Inter-segment revenues are not presented separately, as these amounts are immaterial. Our CODM does not evaluate operating segments using asset information. Information about segments during the periods presented were as follows (in millions):
````

**#2 `GOOGL_FY2015_2015-12-31:158`** (cited, gold #2)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Information about Segments
In conjunction with the Alphabet reorganization, in the fourth quarter of 2015, we implemented legal and operational changes in how our Chief Operating Decision Maker (CODM) manages our businesses, including resource allocation and performance assessment. Consequently, we have multiple operating segments, representing the individual businesses that are run separately under the Alphabet structure. Google is our only reportable segment. None of our other segments meet the quantitative thresholds to qualify as reportable segments; therefore, the operating segments are combined and disclosed below as Other Bets. All prior-period amounts have been adjusted retrospectively to reflect the reportable segment change. Our reported segments are described below: • Google – Google includes our main internet products such as Search, Ads, Commerce, Maps, YouTube, Apps, Cloud, Android, Chrome, Google Play as well as hardware products we sell, such as Chromecast, Chromebooks and Nexus. Our technical infrastructure and newer efforts like Virtual Reality are also included in Google. • Other Bets – Other Bets is a combination of multiple operating segments that are not individually material. Other Bets includes businesses such as Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and other initiatives.
````

**#3 `GOOGL_FY2019_2019-12-31:464`** (cited, gold #1)

````text
ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Note 15. Information about Segments and Geographic Areas
We operate our business in multiple operating segments. Google is our only reportable segment. None of our other segments meet the quantitative thresholds to qualify as reportable segments; therefore, the other operating segments are combined and disclosed as Other Bets. Our reported segments are: • Google – Google includes our main products such as ads, Android, Chrome, hardware, Google Cloud, Google Maps, Google Play, Search, and YouTube. Our technical infrastructure is also included in Google. Google generates revenues primarily from advertising; sales of apps, in-app purchases, digital content products, and hardware; and licensing and service fees, including fees received for Google Cloud offerings and subscription-based products. • Other Bets – Other Bets is a combination of multiple operating segments that are not individually material. Other Bets includes Access, Calico, CapitalG, GV, Verily, Waymo, and X, among others. Revenues from the Other Bets are derived primarily through the sales of internet and TV services through Access as well as licensing and R&D services through Verily. Table of Contents Alphabet Inc.
````

**#4 `GOOGL_FY2019_2019-12-31:142`** (cited, gold #1)

````text
ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS > Information about Segments
We operate our business in multiple operating segments. Google is our only reportable segment. None of our other segments meet the quantitative thresholds to qualify as reportable segments; therefore, the other operating segments are combined and disclosed as Other Bets. Table of Contents Alphabet Inc. Our reported segments are: • Google – Google includes our main products such as ads, Android, Chrome, hardware, Google Cloud, Google Maps, Google Play, Search, and YouTube. Our technical infrastructure is also included in Google. Google generates revenues primarily from advertising; sales of apps, in-app purchases, digital content products, and hardware; and licensing and service fees, including fees received for Google Cloud offerings and subscription-based products. • Other Bets – Other Bets is a combination of multiple operating segments that are not individually material. Other Bets includes Access, Calico, CapitalG, GV, Verily, Waymo, and X, among others. Revenues from the Other Bets are derived primarily through the sales of internet and TV services through Access as well as licensing and R&D services through Verily.
````

</details>

RQ2 citation match (section level): `cited=[('GOOGL', 'Item 8'), ('GOOGL', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 4, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In fiscal year 2015, Alphabet disclosed that Other Bets included Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and other initiatives. [GOOGL FY2015, Item 8, GOOGL_FY2015_2015-12-31:525] [GOOGL FY2015, Item 7, GOOGL_FY2015_2015-12-31:158] | supported | The cited 2015 disclosures explicitly list Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and other initiatives in Other Bets. |
| In fiscal year 2019, Alphabet disclosed that Other Bets included Access, Calico, CapitalG, GV, Verily, Waymo, and X, among others. [GOOGL FY2019, Item 8, GOOGL_FY2019_2019-12-31:464] [GOOGL FY2019, Item 7, GOOGL_FY2019_2019-12-31:142] | supported | The cited 2019 disclosures explicitly state Other Bets includes Access, Calico, CapitalG, GV, Verily, Waymo, and X, among others. |
| Comparing the named businesses, Nest and Google Fiber were explicitly named in 2015 but were not explicitly named in 2019, while Waymo was explicitly named in 2019 but was not explicitly named in 2015. [GOOGL FY2015, Item 8, GOOGL_FY2015_2015-12-31:525] [GOOGL FY2015, Item 7, GOOGL_FY2015_2015-12-31:158] [GOOGL FY2019, Item 8, GOOGL_FY2019_2019-12-31:464] [GOOGL FY2019, Item 7, GOOGL_FY2019_2019-12-31:142] | supported | The 2015 citations name Nest and Access/Google Fiber but not Waymo, while the 2019 citations name Waymo and Access but not Nest or Google Fiber explicitly. |
| The naming also changed from Google Capital in 2015 to CapitalG in 2019, and from Access/Google Fiber in 2015 to Access in 2019. [GOOGL FY2015, Item 8, GOOGL_FY2015_2015-12-31:525] [GOOGL FY2015, Item 7, GOOGL_FY2015_2015-12-31:158] [GOOGL FY2019, Item 8, GOOGL_FY2019_2019-12-31:464] [GOOGL FY2019, Item 7, GOOGL_FY2019_2019-12-31:142] | supported | The 2015 evidence uses Google Capital and Access/Google Fiber, while the 2019 evidence uses CapitalG and Access. |

</details>
