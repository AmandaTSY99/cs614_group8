# gold-088: Cross-year text

[← all cases](../README.md) · company: Apple Inc. (AAPL) · fiscal year: 2025 · recipe `cross_year_text` · hop `multi` · answer type `qualitative` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> How did the primary drivers for iPhone and Wearables, Home and Accessories net sales change for Apple Inc. between fiscal year 2020 and fiscal year 2025?

**Gold answer**

> In fiscal year 2020, iPhone net sales decreased primarily due to the absence of new iPhone models in the fourth quarter and foreign currency weakness, while Wearables, Home and Accessories net sales increased due to higher sales of AirPods and Apple Watch. By fiscal year 2025, iPhone net sales increased due to higher net sales of Pro models, whereas Wearables, Home and Accessories net sales decreased primarily due to lower net sales of Accessories and Wearables.

**Key points** (RQ3 keypoint_recall targets)

1. FY2020 iPhone sales decreased due to the absence of new models in Q4 and currency weakness.
2. FY2020 Wearables, Home and Accessories sales increased due to higher sales of AirPods and Apple Watch.
3. FY2025 iPhone sales increased due to higher net sales of Pro models.
4. FY2025 Wearables, Home and Accessories sales decreased due to lower net sales of Accessories and Wearables.

**Gold evidence**

1. `AAPL_FY2025_2025-09-27` · Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations › Products and Services Performance · text

   > iPhone net sales increased during 2025 compared to 2024 due to higher net sales of Pro models.

2. `AAPL_FY2025_2025-09-27` · Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations › Products and Services Performance · text

   > Wearables, Home and Accessories net sales decreased during 2025 compared to 2024 primarily due to lower net sales of Accessories and Wearables.

3. `AAPL_FY2020_2020-09-26` · Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations › Products and Services Performance · text

   > iPhone net sales decreased during 2020 compared to 2019 due primarily to the absence of new iPhone models in the fourth quarter of 2020 and the weakness in foreign currencies relative to the U.S. dollar, partially offset by the introduction of iPhone SE in the third quarter of 2020.

4. `AAPL_FY2020_2020-09-26` · Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations › Products and Services Performance · text

   > Wearables, Home and Accessories net sales increased during 2020 compared to 2019 due primarily to higher net sales of AirPods and Apple Watch.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 11 | 10 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.90 | 1.00 | 1.00 | 0.94 |
| gold evidence first rank | #1: 1, #2: 1, #3: 1, #4: 1 | #1: 3, #2: 1, #3: 3, #4: 1 | #1: 1, #2: 1, #3: 1, #4: 1 | #1: 1, #2: 1, #3: 1, #4: 1 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✗ | ✓ | ✓ |
| keypoint_recall | 1.00 | 0.00 | 1.00 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 1.00 | – | 1.00 | 1.00 |
| citation recall | 1.00 | – | 1.00 | 1.00 |
| citation F1 | 1.00 | – | 1.00 | 1.00 |
| has a citation | 1 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 2232 | 1298 | 15543 | 15783 |
| cost (USD) | 0.0005 | 0.0002 | 0.0624 | 0.0643 |
| latency (s) | 4.7 | 6.0 | 31.6 | 28.6 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 3.

**Generated answer**

> Between fiscal year 2020 and fiscal year 2025, the primary drivers changed as follows:
>
> - **iPhone**
>   - In **2020**, iPhone net sales **decreased** primarily due to the **absence of new iPhone models in the fourth quarter of 2020** and **weakness in foreign currencies relative to the U.S. dollar**, partially offset by the **introduction of iPhone SE in the third quarter of 2020** [1].
>   - In **2025**, iPhone net sales **increased** due to **higher net sales of Pro models** [4].
>
> - **Wearables, Home and Accessories**
>   - In **2020**, net sales **increased** primarily due to **higher net sales of AirPods and Apple Watch** [2].
>   - In **2025**, net sales **decreased** primarily due to **lower net sales of Accessories and Wearables** [4].
>
> So, overall, Apple went from:
> - **iPhone** being pressured in 2020 by timing of product launches and currency weakness to being driven upward in 2025 by strong **Pro model** sales [1][4].
> - **Wearables, Home and Accessories** being driven upward in 2020 by **AirPods and Apple Watch** to declining in 2025 because of weaker **Accessories and Wearables** sales [2][4].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2020_2020-09-26:114` | Item 7 › Products and Services Performance | ✓ | #1, #2, #3, #4 | (1)Products net sales include amortization of the deferred value of unspecified software upgrade rights, which are bundled in the sales price of the respective product. (2)Wearables, Home and Accessories net sales includ… |
| 2 | `AAPL_FY2020_2020-09-26:115` | Item 7 › Products and Services Performance | ✓ | #2, #4 | Wearables, Home and Accessories net sales increased during 2020 compared to 2019 due primarily to higher net sales of AirPods and Apple Watch. Services Services net sales increased during 2020 compared to 2019 due primar… |
| 3 | `AAPL_FY2020_2020-09-26:207` | Item 8 › Note 2 – Revenue Recognition |  | #2, #4 | (1)Products net sales include amortization of the deferred value of unspecified software upgrade rights, which are bundled in the sales price of the respective product. (2)Wearables, Home and Accessories net sales includ… |
| 4 | `AAPL_FY2025_2025-09-27:136` | Item 7 › Products and Services Performance | ✓ | #1, #2, #4 | (1)Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. iPhone iPhone net sales increased during 2025 compared to 2024 due to higher net sales of Pro m… |
| 5 | `AAPL_FY2025_2025-09-27:126` | Item 7 › Product, Service and Software Announcements |  |  | The Company announces new product, service and software offerings at various times during the year. Significant announcements during fiscal year 2025 included the following: First Quarter 2025: •MacBook Pro •Mac mini •iM… |
| 6 | `AAPL_FY2025_2025-09-27:134` | Item 7 › Products and Services Performance |  |  | The following table shows net sales by category for 2025, 2024 and 2023 (dollars in millions): |
| 7 | `AAPL_FY2020_2020-09-26:112` | Item 7 › Products and Services Performance |  |  | The following table shows net sales by category for 2020, 2019 and 2018 (dollars in millions): |
| 8 | `AAPL_FY2020_2020-09-26:113` | Item 7 › Products and Services Performance |  |  | \| \| 2020 \| Change \| 2019 \| Change \| 2018 \| \|---\|---\|---\|---\|---\|---\| \| Net sales by category: \| \| \| \| \| \| \| iPhone (1) \| $137,781 \| (3)% \| $142,381 \| (14)% \| $164,888 \| \| Mac (1) \| 28,622 \| 11% \| 25,740 \| 2% \| 25,198 \| \|… |
| 9 | `AAPL_FY2020_2020-09-26:19` | Item 1 › Products |  |  | Wearables, Home and Accessories includes AirPods®, Apple TV®, Apple Watch®, Beats® products, HomePod®, iPod touch® and other Apple-branded and third-party accessories. AirPods are the Company’s wireless headphones that i… |
| 10 | `AAPL_FY2020_2020-09-26:119` | Item 7 › Segment Operating Performance |  | #1, #2, #4 | Rest of Asia Pacific net sales increased during 2020 compared to 2019 due primarily to higher net sales of Wearables, Home and Accessories, Services and iPhone. The weakness in foreign currencies relative to the U.S. dol… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2020_2020-09-26:114`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Products and Services Performance
(1)Products net sales include amortization of the deferred value of unspecified software upgrade rights, which are bundled in the sales price of the respective product. (2)Wearables, Home and Accessories net sales include sales of AirPods, Apple TV, Apple Watch, Beats products, HomePod, iPod touch and Apple-branded and third-party accessories. (3)Services net sales include sales from the Company’s advertising, AppleCare, digital content and other services. Services net sales also include amortization of the deferred value of Maps, Siri, and free iCloud® storage and Apple TV+ services, which are bundled in the sales price of certain products. iPhone iPhone net sales decreased during 2020 compared to 2019 due primarily to the absence of new iPhone models in the fourth quarter of 2020 and the weakness in foreign currencies relative to the U.S. dollar, partially offset by the introduction of iPhone SE in the third quarter of 2020. Mac Mac net sales increased during 2020 compared to 2019 due primarily to higher net sales of MacBook Pro. iPad iPad net sales increased during 2020 compared to 2019 due primarily to higher net sales of 10-inch versions of iPad, iPad Air and iPad Pro. Wearables, Home and Accessories
````

**#2 `AAPL_FY2020_2020-09-26:115`** (cited, gold #2, gold #4)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Products and Services Performance
Wearables, Home and Accessories net sales increased during 2020 compared to 2019 due primarily to higher net sales of AirPods and Apple Watch. Services Services net sales increased during 2020 compared to 2019 due primarily to higher net sales from the App Store, advertising and cloud services. Apple Inc. | 2020 Form 10-K | 21
````

**#3 `AAPL_FY2020_2020-09-26:207`** (gold #2, gold #4)

````text
Item 8. Financial Statements and Supplementary Data > Note 2 – Revenue Recognition
(1)Products net sales include amortization of the deferred value of unspecified software upgrade rights, which are bundled in the sales price of the respective product. (2)Wearables, Home and Accessories net sales include sales of AirPods, Apple TV, Apple Watch, Beats products, HomePod, iPod touch and Apple-branded and third-party accessories. (3)Services net sales include sales from the Company’s advertising, AppleCare, digital content and other services. Services net sales also include amortization of the deferred value of Maps, Siri, and free iCloud storage and Apple TV+ services, which are bundled in the sales price of certain products. (4)Includes $5.0 billion of revenue recognized in 2020 that was included in deferred revenue as of September 28, 2019, $5.9 billion of revenue recognized in 2019 that was included in deferred revenue as of September 29, 2018, and $5.8 billion of revenue recognized in 2018 that was included in deferred revenue as of September 30, 2017. The Company’s proportion of net sales by disaggregated revenue source was generally consistent for each reportable segment in Note 11, “Segment Information and Geographic Data” for 2020, 2019 and 2018. Apple Inc. | 2020 Form 10-K | 39
````

**#4 `AAPL_FY2025_2025-09-27:136`** (cited, gold #1, gold #2, gold #4)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Products and Services Performance
(1)Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. iPhone iPhone net sales increased during 2025 compared to 2024 due to higher net sales of Pro models. Mac Mac net sales increased during 2025 compared to 2024 primarily due to higher net sales of laptops and desktops. iPad iPad net sales increased during 2025 compared to 2024 primarily due to higher net sales of iPad Air, iPad mini and iPad, partially offset by lower net sales of iPad Pro. Wearables, Home and Accessories Wearables, Home and Accessories net sales decreased during 2025 compared to 2024 primarily due to lower net sales of Accessories and Wearables. Services Services net sales increased during 2025 compared to 2024 primarily due to higher net sales from advertising, the App Store and cloud services. Apple Inc. | 2025 Form 10-K | 23
````

**#10 `AAPL_FY2020_2020-09-26:119`** (gold #1, gold #2, gold #4)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Segment Operating Performance
Rest of Asia Pacific net sales increased during 2020 compared to 2019 due primarily to higher net sales of Wearables, Home and Accessories, Services and iPhone. The weakness in foreign currencies relative to the U.S. dollar had an unfavorable impact on Rest of Asia Pacific net sales during 2020. Apple Inc. | 2020 Form 10-K | 22
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 7')] gold=[(None, 'Item 7')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2020_2020-09-26:110` | Item 7 › Fiscal Year Highlights |  | #2, #4 | The full extent of the future impact of the COVID-19 pandemic on the Company’s operational and financial performance is currently uncertain and will depend on many factors outside the Company’s control, including, withou… |
| 2 | `AAPL_FY2020_2020-09-26:115` | Item 7 › Products and Services Performance |  | #2, #4 | Wearables, Home and Accessories net sales increased during 2020 compared to 2019 due primarily to higher net sales of AirPods and Apple Watch. Services Services net sales increased during 2020 compared to 2019 due primar… |
| 3 | `AAPL_FY2020_2020-09-26:114` | Item 7 › Products and Services Performance |  | #1, #2, #3, #4 | (1)Products net sales include amortization of the deferred value of unspecified software upgrade rights, which are bundled in the sales price of the respective product. (2)Wearables, Home and Accessories net sales includ… |
| 4 | `AAPL_FY2025_2025-09-27:135` | Item 7 › Products and Services Performance |  |  | \| \| 2025 \| Change \| 2024 \| Change \| 2023 \| \|---\|---\|---\|---\|---\|---\| \| iPhone \| $209,586 \| 4% \| $201,183 \| —% \| $200,583 \| \| Mac \| 33,708 \| 12% \| 29,984 \| 2% \| 29,357 \| \| iPad \| 28,023 \| 5% \| 26,694 \| (6)% \| 28,300 \| \| W… |
| 5 | `AAPL_FY2020_2020-09-26:113` | Item 7 › Products and Services Performance |  |  | \| \| 2020 \| Change \| 2019 \| Change \| 2018 \| \|---\|---\|---\|---\|---\|---\| \| Net sales by category: \| \| \| \| \| \| \| iPhone (1) \| $137,781 \| (3)% \| $142,381 \| (14)% \| $164,888 \| \| Mac (1) \| 28,622 \| 11% \| 25,740 \| 2% \| 25,198 \| \|… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2020_2020-09-26:110`** (gold #2, gold #4)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Fiscal Year Highlights
The full extent of the future impact of the COVID-19 pandemic on the Company’s operational and financial performance is currently uncertain and will depend on many factors outside the Company’s control, including, without limitation, the timing, extent, trajectory and duration of the pandemic, the development and availability of effective treatments and vaccines, the imposition of protective public safety measures, and the impact of the pandemic on the global economy and demand for consumer products. Refer to Part I, Item 1A of this Form 10-K under the heading “Risk Factors,” for more information. The Company believes its existing balances of cash, cash equivalents and marketable securities, along with commercial paper and other short-term liquidity arrangements, will be sufficient to satisfy its working capital needs, capital asset purchases, dividends, share repurchases, debt repayments and other liquidity requirements associated with its existing operations. Fiscal 2020 Highlights Total net sales increased 6% or $14.3 billion during 2020 compared to 2019, primarily driven by higher net sales of Services and Wearables, Home and Accessories. The weakness in foreign currencies had an unfavorable impact on net sales during 2020.
````

**#2 `AAPL_FY2020_2020-09-26:115`** (gold #2, gold #4)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Products and Services Performance
Wearables, Home and Accessories net sales increased during 2020 compared to 2019 due primarily to higher net sales of AirPods and Apple Watch. Services Services net sales increased during 2020 compared to 2019 due primarily to higher net sales from the App Store, advertising and cloud services. Apple Inc. | 2020 Form 10-K | 21
````

**#3 `AAPL_FY2020_2020-09-26:114`** (gold #1, gold #2, gold #3, gold #4)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Products and Services Performance
(1)Products net sales include amortization of the deferred value of unspecified software upgrade rights, which are bundled in the sales price of the respective product. (2)Wearables, Home and Accessories net sales include sales of AirPods, Apple TV, Apple Watch, Beats products, HomePod, iPod touch and Apple-branded and third-party accessories. (3)Services net sales include sales from the Company’s advertising, AppleCare, digital content and other services. Services net sales also include amortization of the deferred value of Maps, Siri, and free iCloud® storage and Apple TV+ services, which are bundled in the sales price of certain products. iPhone iPhone net sales decreased during 2020 compared to 2019 due primarily to the absence of new iPhone models in the fourth quarter of 2020 and the weakness in foreign currencies relative to the U.S. dollar, partially offset by the introduction of iPhone SE in the third quarter of 2020. Mac Mac net sales increased during 2020 compared to 2019 due primarily to higher net sales of MacBook Pro. iPad iPad net sales increased during 2020 compared to 2019 due primarily to higher net sales of 10-inch versions of iPad, iPad Air and iPad Pro. Wearables, Home and Accessories
````

</details>

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 11, cited: 3.

**Generated answer**

> In fiscal 2020, iPhone net sales decreased compared to 2019 primarily due to the absence of new iPhone models in the fourth quarter of 2020 and the weakness in foreign currencies relative to the U.S. dollar, partially offset by the introduction of iPhone SE in the third quarter of 2020. [AAPL FY2020, Item 7, AAPL_FY2020_2020-09-26:114]
>
> In fiscal 2025, iPhone net sales increased compared to 2024 due to higher net sales of Pro models. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136]
>
> This means the primary iPhone driver changed from timing and currency-related headwinds in 2020, with some support from iPhone SE, to product-mix strength from higher Pro model sales in 2025. [AAPL FY2020, Item 7, AAPL_FY2020_2020-09-26:114] [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136]
>
> In fiscal 2020, Wearables, Home and Accessories net sales increased compared to 2019 due primarily to higher net sales of AirPods and Apple Watch. [AAPL FY2020, Item 7, AAPL_FY2020_2020-09-26:115]
>
> In fiscal 2025, Wearables, Home and Accessories net sales decreased compared to 2024 primarily due to lower net sales of Accessories and Wearables. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136]
>
> This means the primary driver for Wearables, Home and Accessories shifted from growth led by AirPods and Apple Watch in 2020 to declines driven by lower sales in Accessories and Wearables in 2025. [AAPL FY2020, Item 7, AAPL_FY2020_2020-09-26:115] [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2020_2020-09-26:114` | Item 7 › Products and Services Performance | ✓ | #1, #2, #3, #4 | (1)Products net sales include amortization of the deferred value of unspecified software upgrade rights, which are bundled in the sales price of the respective product. (2)Wearables, Home and Accessories net sales includ… |
| 2 | `AAPL_FY2020_2020-09-26:207` | Item 8 › Note 2 – Revenue Recognition |  | #2, #4 | (1)Products net sales include amortization of the deferred value of unspecified software upgrade rights, which are bundled in the sales price of the respective product. (2)Wearables, Home and Accessories net sales includ… |
| 3 | `AAPL_FY2025_2025-09-27:136` | Item 7 › Products and Services Performance | ✓ | #1, #2, #4 | (1)Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. iPhone iPhone net sales increased during 2025 compared to 2024 due to higher net sales of Pro m… |
| 4 | `AAPL_FY2020_2020-09-26:115` | Item 7 › Products and Services Performance | ✓ | #2, #4 | Wearables, Home and Accessories net sales increased during 2020 compared to 2019 due primarily to higher net sales of AirPods and Apple Watch. Services Services net sales increased during 2020 compared to 2019 due primar… |
| 5 | `AAPL_FY2020_2020-09-26:202` | Item 8 › Note 2 – Revenue Recognition |  |  | The Company has identified up to three performance obligations regularly included in arrangements involving the sale of iPhone, Mac, iPad and certain other products. The first performance obligation, which represents the… |
| 6 | `AAPL_FY2025_2025-09-27:18` | Item 1 › Products |  |  | iPhone iPhone® is the Company’s line of smartphones based on its iOS operating system. The iPhone line includes iPhone 17 Pro, iPhone Air™, iPhone 17, iPhone 16 and iPhone 16e. Mac Mac® is the Company’s line of personal … |
| 7 | `AAPL_FY2020_2020-09-26:19` | Item 1 › Products |  |  | Wearables, Home and Accessories includes AirPods®, Apple TV®, Apple Watch®, Beats® products, HomePod®, iPod touch® and other Apple-branded and third-party accessories. AirPods are the Company’s wireless headphones that i… |
| 8 | `AAPL_FY2025_2025-09-27:126` | Item 7 › Product, Service and Software Announcements |  |  | The Company announces new product, service and software offerings at various times during the year. Significant announcements during fiscal year 2025 included the following: First Quarter 2025: •MacBook Pro •Mac mini •iM… |
| 9 | `AAPL_FY2020_2020-09-26:113` | Item 7 › Products and Services Performance |  |  | \| \| 2020 \| Change \| 2019 \| Change \| 2018 \| \|---\|---\|---\|---\|---\|---\| \| Net sales by category: \| \| \| \| \| \| \| iPhone (1) \| $137,781 \| (3)% \| $142,381 \| (14)% \| $164,888 \| \| Mac (1) \| 28,622 \| 11% \| 25,740 \| 2% \| 25,198 \| \|… |
| 10 | `AAPL_FY2020_2020-09-26:112` | Item 7 › Products and Services Performance |  |  | The following table shows net sales by category for 2020, 2019 and 2018 (dollars in millions): |
| 11 | `AAPL_FY2025_2025-09-27:135` | Item 7 › Products and Services Performance |  |  | \| \| 2025 \| Change \| 2024 \| Change \| 2023 \| \|---\|---\|---\|---\|---\|---\| \| iPhone \| $209,586 \| 4% \| $201,183 \| —% \| $200,583 \| \| Mac \| 33,708 \| 12% \| 29,984 \| 2% \| 29,357 \| \| iPad \| 28,023 \| 5% \| 26,694 \| (6)% \| 28,300 \| \| W… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2020_2020-09-26:114`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Products and Services Performance
(1)Products net sales include amortization of the deferred value of unspecified software upgrade rights, which are bundled in the sales price of the respective product. (2)Wearables, Home and Accessories net sales include sales of AirPods, Apple TV, Apple Watch, Beats products, HomePod, iPod touch and Apple-branded and third-party accessories. (3)Services net sales include sales from the Company’s advertising, AppleCare, digital content and other services. Services net sales also include amortization of the deferred value of Maps, Siri, and free iCloud® storage and Apple TV+ services, which are bundled in the sales price of certain products. iPhone iPhone net sales decreased during 2020 compared to 2019 due primarily to the absence of new iPhone models in the fourth quarter of 2020 and the weakness in foreign currencies relative to the U.S. dollar, partially offset by the introduction of iPhone SE in the third quarter of 2020. Mac Mac net sales increased during 2020 compared to 2019 due primarily to higher net sales of MacBook Pro. iPad iPad net sales increased during 2020 compared to 2019 due primarily to higher net sales of 10-inch versions of iPad, iPad Air and iPad Pro. Wearables, Home and Accessories
````

**#2 `AAPL_FY2020_2020-09-26:207`** (gold #2, gold #4)

````text
Item 8. Financial Statements and Supplementary Data > Note 2 – Revenue Recognition
(1)Products net sales include amortization of the deferred value of unspecified software upgrade rights, which are bundled in the sales price of the respective product. (2)Wearables, Home and Accessories net sales include sales of AirPods, Apple TV, Apple Watch, Beats products, HomePod, iPod touch and Apple-branded and third-party accessories. (3)Services net sales include sales from the Company’s advertising, AppleCare, digital content and other services. Services net sales also include amortization of the deferred value of Maps, Siri, and free iCloud storage and Apple TV+ services, which are bundled in the sales price of certain products. (4)Includes $5.0 billion of revenue recognized in 2020 that was included in deferred revenue as of September 28, 2019, $5.9 billion of revenue recognized in 2019 that was included in deferred revenue as of September 29, 2018, and $5.8 billion of revenue recognized in 2018 that was included in deferred revenue as of September 30, 2017. The Company’s proportion of net sales by disaggregated revenue source was generally consistent for each reportable segment in Note 11, “Segment Information and Geographic Data” for 2020, 2019 and 2018. Apple Inc. | 2020 Form 10-K | 39
````

**#3 `AAPL_FY2025_2025-09-27:136`** (cited, gold #1, gold #2, gold #4)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Products and Services Performance
(1)Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. iPhone iPhone net sales increased during 2025 compared to 2024 due to higher net sales of Pro models. Mac Mac net sales increased during 2025 compared to 2024 primarily due to higher net sales of laptops and desktops. iPad iPad net sales increased during 2025 compared to 2024 primarily due to higher net sales of iPad Air, iPad mini and iPad, partially offset by lower net sales of iPad Pro. Wearables, Home and Accessories Wearables, Home and Accessories net sales decreased during 2025 compared to 2024 primarily due to lower net sales of Accessories and Wearables. Services Services net sales increased during 2025 compared to 2024 primarily due to higher net sales from advertising, the App Store and cloud services. Apple Inc. | 2025 Form 10-K | 23
````

**#4 `AAPL_FY2020_2020-09-26:115`** (cited, gold #2, gold #4)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Products and Services Performance
Wearables, Home and Accessories net sales increased during 2020 compared to 2019 due primarily to higher net sales of AirPods and Apple Watch. Services Services net sales increased during 2020 compared to 2019 due primarily to higher net sales from the App Store, advertising and cloud services. Apple Inc. | 2020 Form 10-K | 21
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 6, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In fiscal 2020, iPhone net sales decreased compared to 2019 primarily due to the absence of new iPhone models in the fourth quarter of 2020 and the weakness in foreign currencies relative to the U.S. dollar, partially offset by the introduction of iPhone SE in the third quarter of 2020. [AAPL FY2020, Item 7, AAPL_FY2020_2020-09-26:114] | supported | The evidence states exactly that iPhone net sales decreased in 2020 for those reasons and offsets. |
| In fiscal 2025, iPhone net sales increased compared to 2024 due to higher net sales of Pro models. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136] | supported | The evidence explicitly says iPhone net sales increased in 2025 due to higher net sales of Pro models. |
| This means the primary iPhone driver changed from timing and currency-related headwinds in 2020, with some support from iPhone SE, to product-mix strength from higher Pro model sales in 2025. [AAPL FY2020, Item 7, AAPL_FY2020_2020-09-26:114] [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136] | supported | The two cited passages support the comparison from 2020 timing/currency headwinds with iPhone SE offset to 2025 Pro-model-driven growth. |
| In fiscal 2020, Wearables, Home and Accessories net sales increased compared to 2019 due primarily to higher net sales of AirPods and Apple Watch. [AAPL FY2020, Item 7, AAPL_FY2020_2020-09-26:115] | supported | The evidence states Wearables, Home and Accessories net sales increased in 2020 due primarily to higher net sales of AirPods and Apple Watch. |
| In fiscal 2025, Wearables, Home and Accessories net sales decreased compared to 2024 primarily due to lower net sales of Accessories and Wearables. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136] | supported | The evidence explicitly states Wearables, Home and Accessories net sales decreased in 2025 primarily due to lower net sales of Accessories and Wearables. |
| This means the primary driver for Wearables, Home and Accessories shifted from growth led by AirPods and Apple Watch in 2020 to declines driven by lower sales in Accessories and Wearables in 2025. [AAPL FY2020, Item 7, AAPL_FY2020_2020-09-26:115] [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136] | supported | The cited evidence supports that the category's main driver shifted from AirPods/Apple Watch-led growth in 2020 to Accessories/Wearables-led declines in 2025. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 10, cited: 5.

**Generated answer**

> In fiscal year 2020, iPhone net sales decreased compared to 2019 due primarily to the absence of new iPhone models in the fourth quarter of 2020 and the weakness in foreign currencies relative to the U.S. dollar, partially offset by the introduction of iPhone SE in the third quarter of 2020. [AAPL FY2020, Item 7, AAPL_FY2020_2020-09-26:114]
>
> In fiscal year 2025, iPhone net sales increased compared to 2024 due to higher net sales of Pro models. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136]
>
> This means the primary iPhone driver changed from a decline caused by product timing and foreign currency weakness in 2020 to growth driven by stronger Pro model sales in 2025. [AAPL FY2020, Item 7, AAPL_FY2020_2020-09-26:114] [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136]
>
> In fiscal year 2020, Wearables, Home and Accessories net sales increased compared to 2019 due primarily to higher net sales of AirPods and Apple Watch. [AAPL FY2020, Item 7, AAPL_FY2020_2020-09-26:115]
>
> In fiscal year 2025, Wearables, Home and Accessories net sales decreased compared to 2024 primarily due to lower net sales of Accessories and Wearables. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136]
>
> This means the primary driver for Wearables, Home and Accessories changed from growth led by AirPods and Apple Watch in 2020 to a decline driven by weaker Accessories and Wearables sales in 2025. [AAPL FY2020, Item 7, AAPL_FY2020_2020-09-26:115] [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136]
>
> The reported category results also shifted from iPhone net sales of $137,781 and Wearables, Home and Accessories net sales of $30,620 in 2020 to iPhone net sales of $209,586 and Wearables, Home and Accessories net sales of $35,686 in 2025. [AAPL FY2020, Item 7, AAPL_FY2020_2020-09-26:113] [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:135]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `AAPL_FY2020_2020-09-26:114` | Item 7 › Products and Services Performance | ✓ | #1, #2, #3, #4 | (1)Products net sales include amortization of the deferred value of unspecified software upgrade rights, which are bundled in the sales price of the respective product. (2)Wearables, Home and Accessories net sales includ… |
| 2 | `AAPL_FY2020_2020-09-26:207` | Item 8 › Note 2 – Revenue Recognition |  | #2, #4 | (1)Products net sales include amortization of the deferred value of unspecified software upgrade rights, which are bundled in the sales price of the respective product. (2)Wearables, Home and Accessories net sales includ… |
| 3 | `AAPL_FY2025_2025-09-27:136` | Item 7 › Products and Services Performance | ✓ | #1, #2, #4 | (1)Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. iPhone iPhone net sales increased during 2025 compared to 2024 due to higher net sales of Pro m… |
| 4 | `AAPL_FY2020_2020-09-26:115` | Item 7 › Products and Services Performance | ✓ | #2, #4 | Wearables, Home and Accessories net sales increased during 2020 compared to 2019 due primarily to higher net sales of AirPods and Apple Watch. Services Services net sales increased during 2020 compared to 2019 due primar… |
| 5 | `AAPL_FY2020_2020-09-26:202` | Item 8 › Note 2 – Revenue Recognition |  |  | The Company has identified up to three performance obligations regularly included in arrangements involving the sale of iPhone, Mac, iPad and certain other products. The first performance obligation, which represents the… |
| 6 | `AAPL_FY2025_2025-09-27:18` | Item 1 › Products |  |  | iPhone iPhone® is the Company’s line of smartphones based on its iOS operating system. The iPhone line includes iPhone 17 Pro, iPhone Air™, iPhone 17, iPhone 16 and iPhone 16e. Mac Mac® is the Company’s line of personal … |
| 7 | `AAPL_FY2020_2020-09-26:119` | Item 7 › Segment Operating Performance |  | #1, #2, #4 | Rest of Asia Pacific net sales increased during 2020 compared to 2019 due primarily to higher net sales of Wearables, Home and Accessories, Services and iPhone. The weakness in foreign currencies relative to the U.S. dol… |
| 8 | `AAPL_FY2020_2020-09-26:113` | Item 7 › Products and Services Performance | ✓ |  | \| \| 2020 \| Change \| 2019 \| Change \| 2018 \| \|---\|---\|---\|---\|---\|---\| \| Net sales by category: \| \| \| \| \| \| \| iPhone (1) \| $137,781 \| (3)% \| $142,381 \| (14)% \| $164,888 \| \| Mac (1) \| 28,622 \| 11% \| 25,740 \| 2% \| 25,198 \| \|… |
| 9 | `AAPL_FY2025_2025-09-27:135` | Item 7 › Products and Services Performance | ✓ |  | \| \| 2025 \| Change \| 2024 \| Change \| 2023 \| \|---\|---\|---\|---\|---\|---\| \| iPhone \| $209,586 \| 4% \| $201,183 \| —% \| $200,583 \| \| Mac \| 33,708 \| 12% \| 29,984 \| 2% \| 29,357 \| \| iPad \| 28,023 \| 5% \| 26,694 \| (6)% \| 28,300 \| \| W… |
| 10 | `AAPL_FY2020_2020-09-26:83` | Item 1A › The Company expects its quarterly net sales and operating results to fluctuate. |  |  | The Company has historically experienced higher net sales in its first quarter compared to other quarters in its fiscal year due in part to seasonal holiday demand. Additionally, new product and service introductions can… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `AAPL_FY2020_2020-09-26:114`** (cited, gold #1, gold #2, gold #3, gold #4)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Products and Services Performance
(1)Products net sales include amortization of the deferred value of unspecified software upgrade rights, which are bundled in the sales price of the respective product. (2)Wearables, Home and Accessories net sales include sales of AirPods, Apple TV, Apple Watch, Beats products, HomePod, iPod touch and Apple-branded and third-party accessories. (3)Services net sales include sales from the Company’s advertising, AppleCare, digital content and other services. Services net sales also include amortization of the deferred value of Maps, Siri, and free iCloud® storage and Apple TV+ services, which are bundled in the sales price of certain products. iPhone iPhone net sales decreased during 2020 compared to 2019 due primarily to the absence of new iPhone models in the fourth quarter of 2020 and the weakness in foreign currencies relative to the U.S. dollar, partially offset by the introduction of iPhone SE in the third quarter of 2020. Mac Mac net sales increased during 2020 compared to 2019 due primarily to higher net sales of MacBook Pro. iPad iPad net sales increased during 2020 compared to 2019 due primarily to higher net sales of 10-inch versions of iPad, iPad Air and iPad Pro. Wearables, Home and Accessories
````

**#2 `AAPL_FY2020_2020-09-26:207`** (gold #2, gold #4)

````text
Item 8. Financial Statements and Supplementary Data > Note 2 – Revenue Recognition
(1)Products net sales include amortization of the deferred value of unspecified software upgrade rights, which are bundled in the sales price of the respective product. (2)Wearables, Home and Accessories net sales include sales of AirPods, Apple TV, Apple Watch, Beats products, HomePod, iPod touch and Apple-branded and third-party accessories. (3)Services net sales include sales from the Company’s advertising, AppleCare, digital content and other services. Services net sales also include amortization of the deferred value of Maps, Siri, and free iCloud storage and Apple TV+ services, which are bundled in the sales price of certain products. (4)Includes $5.0 billion of revenue recognized in 2020 that was included in deferred revenue as of September 28, 2019, $5.9 billion of revenue recognized in 2019 that was included in deferred revenue as of September 29, 2018, and $5.8 billion of revenue recognized in 2018 that was included in deferred revenue as of September 30, 2017. The Company’s proportion of net sales by disaggregated revenue source was generally consistent for each reportable segment in Note 11, “Segment Information and Geographic Data” for 2020, 2019 and 2018. Apple Inc. | 2020 Form 10-K | 39
````

**#3 `AAPL_FY2025_2025-09-27:136`** (cited, gold #1, gold #2, gold #4)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Products and Services Performance
(1)Services net sales include amortization of the deferred value of services bundled in the sales price of certain products. iPhone iPhone net sales increased during 2025 compared to 2024 due to higher net sales of Pro models. Mac Mac net sales increased during 2025 compared to 2024 primarily due to higher net sales of laptops and desktops. iPad iPad net sales increased during 2025 compared to 2024 primarily due to higher net sales of iPad Air, iPad mini and iPad, partially offset by lower net sales of iPad Pro. Wearables, Home and Accessories Wearables, Home and Accessories net sales decreased during 2025 compared to 2024 primarily due to lower net sales of Accessories and Wearables. Services Services net sales increased during 2025 compared to 2024 primarily due to higher net sales from advertising, the App Store and cloud services. Apple Inc. | 2025 Form 10-K | 23
````

**#4 `AAPL_FY2020_2020-09-26:115`** (cited, gold #2, gold #4)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Products and Services Performance
Wearables, Home and Accessories net sales increased during 2020 compared to 2019 due primarily to higher net sales of AirPods and Apple Watch. Services Services net sales increased during 2020 compared to 2019 due primarily to higher net sales from the App Store, advertising and cloud services. Apple Inc. | 2020 Form 10-K | 21
````

**#7 `AAPL_FY2020_2020-09-26:119`** (gold #1, gold #2, gold #4)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Segment Operating Performance
Rest of Asia Pacific net sales increased during 2020 compared to 2019 due primarily to higher net sales of Wearables, Home and Accessories, Services and iPhone. The weakness in foreign currencies relative to the U.S. dollar had an unfavorable impact on Rest of Asia Pacific net sales during 2020. Apple Inc. | 2020 Form 10-K | 22
````

**#8 `AAPL_FY2020_2020-09-26:113`** (cited)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Products and Services Performance (table)
|  | 2020 | Change | 2019 | Change | 2018 |
|---|---|---|---|---|---|
| Net sales by category: |  |  |  |  |  |
| iPhone (1) | $137,781 | (3)% | $142,381 | (14)% | $164,888 |
| Mac (1) | 28,622 | 11% | 25,740 | 2% | 25,198 |
| iPad (1) | 23,724 | 11% | 21,280 | 16% | 18,380 |
| Wearables, Home and Accessories (1)(2) | 30,620 | 25% | 24,482 | 41% | 17,381 |
| Services (3) | 53,768 | 16% | 46,291 | 16% | 39,748 |
| Total net sales | $274,515 | 6% | $260,174 | (2)% | $265,595 |
````

**#9 `AAPL_FY2025_2025-09-27:135`** (cited)

````text
Item 7. Management’s Discussion and Analysis of Financial Condition and Results of Operations > Products and Services Performance (table)
|  | 2025 | Change | 2024 | Change | 2023 |
|---|---|---|---|---|---|
| iPhone | $209,586 | 4% | $201,183 | —% | $200,583 |
| Mac | 33,708 | 12% | 29,984 | 2% | 29,357 |
| iPad | 28,023 | 5% | 26,694 | (6)% | 28,300 |
| Wearables, Home and Accessories | 35,686 | (4)% | 37,005 | (7)% | 39,845 |
| Services (1) | 109,158 | 14% | 96,169 | 13% | 85,200 |
| Total net sales | $416,161 | 6% | $391,035 | 2% | $383,285 |
````

</details>

RQ2 citation match (section level): `cited=[('AAPL', 'Item 7')] gold=[(None, 'Item 7')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 4, verified 4, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 6, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In fiscal year 2020, iPhone net sales decreased compared to 2019 due primarily to the absence of new iPhone models in the fourth quarter of 2020 and the weakness in foreign currencies relative to the U.S. dollar, partially offset by the introduction of iPhone SE in the third quarter of 2020. [AAPL FY2020, Item 7, AAPL_FY2020_2020-09-26:114] | supported | The evidence states exactly that iPhone net sales decreased in 2020 for those reasons, partially offset by iPhone SE. |
| In fiscal year 2025, iPhone net sales increased compared to 2024 due to higher net sales of Pro models. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136] | supported | The evidence explicitly says iPhone net sales increased in 2025 due to higher net sales of Pro models. |
| This means the primary iPhone driver changed from a decline caused by product timing and foreign currency weakness in 2020 to growth driven by stronger Pro model sales in 2025. [AAPL FY2020, Item 7, AAPL_FY2020_2020-09-26:114] [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136] | supported | The two cited passages support that the iPhone driver shifted from a 2020 decline tied to timing/currency to 2025 growth from Pro models. |
| In fiscal year 2020, Wearables, Home and Accessories net sales increased compared to 2019 due primarily to higher net sales of AirPods and Apple Watch. [AAPL FY2020, Item 7, AAPL_FY2020_2020-09-26:115] | supported | The evidence exactly states Wearables, Home and Accessories net sales increased in 2020 due primarily to AirPods and Apple Watch. |
| In fiscal year 2025, Wearables, Home and Accessories net sales decreased compared to 2024 primarily due to lower net sales of Accessories and Wearables. [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136] | supported | The evidence explicitly states Wearables, Home and Accessories net sales decreased in 2025 primarily due to lower Accessories and Wearables sales. |
| This means the primary driver for Wearables, Home and Accessories changed from growth led by AirPods and Apple Watch in 2020 to a decline driven by weaker Accessories and Wearables sales in 2025. [AAPL FY2020, Item 7, AAPL_FY2020_2020-09-26:115] [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:136] | supported | The cited evidence supports that the segment driver changed from 2020 growth led by AirPods and Apple Watch to 2025 decline from weaker Accessories and Wearables sales. |
| The reported category results also shifted from iPhone net sales of $137,781 and Wearables, Home and Accessories net sales of $30,620 in 2020 to iPhone net sales of $209,586 and Wearables, Home and Accessories net sales of $35,686 in 2025. [AAPL FY2020, Item 7, AAPL_FY2020_2020-09-26:113] [AAPL FY2025, Item 7, AAPL_FY2025_2025-09-27:135] | None |  |

</details>
