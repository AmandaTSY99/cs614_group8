# gold-052: Multi-hop text (one filing)

[← all cases](../README.md) · company: Meta Platforms, Inc. (META) · fiscal year: 2021 · recipe `text` · hop `multi` · answer type `qualitative` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> According to Meta Platforms' 2021 10-K, how does the company justify its methodology for calculating Family metrics, and what specific data limitations does it cite regarding WhatsApp and Messenger Kids that affect this process?

**Gold answer**

> Meta justifies its methodology by stating that it estimates the number of unique people using at least one of its products (Facebook, Instagram, Messenger, and WhatsApp) rather than counting total user accounts, as multiple accounts per person are common. The company relies on complex techniques, algorithms, and machine learning models to attribute multiple accounts to individual people. Specifically, for WhatsApp, the company cites limited visibility into encrypted products, meaning it primarily relies on phone numbers and device information for matching. For Messenger Kids, the company states that it includes their users in metrics but does not seek to match their accounts with accounts on other applications for DAP and MAP calculations.

**Key points** (RQ3 keypoint_recall targets)

1. Family metrics estimate unique people rather than total user accounts.
2. Limited visibility into encrypted products results in fewer data signals for WhatsApp.
3. WhatsApp matching relies primarily on phone numbers and device information.
4. Messenger Kids accounts are not matched with other applications for DAP/MAP calculations.

**Gold evidence**

1. `META_FY2021_2021-12-31` · Item 1A.Risk Factors › Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business. · text

   > Rather, our Family metrics represent our estimates of the number of unique people using at least one of Facebook, Instagram, Messenger, and WhatsApp.

2. `META_FY2021_2021-12-31` · Item 1A.Risk Factors › Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business. · text

   > For example, as a result of limited visibility into encrypted products, we have fewer data signals from WhatsApp user accounts and primarily rely on phone numbers and device information to match WhatsApp user accounts with accounts on our other products.

3. `META_FY2021_2021-12-31` · Item 1A.Risk Factors › Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business. · text

   > Similarly, although Messenger Kids users are included in our Family metrics, we do not seek to match their accounts with accounts on our other applications for purposes of calculating DAP and MAP.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 9 | 9 |
| recall@5 | 1.00 | 1.00 | 0.67 | 0.67 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 0.94 | 1.00 | 0.67 | 0.67 |
| gold evidence first rank | #1: 3, #2: 1, #3: 1 | #1: 2, #2: 1, #3: 1 | #1: 3, #2: 1, #3: 7 | #1: 3, #2: 1, #3: 8 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | – | – | – | – |
| keypoint_recall | 1.00 | 1.00 | 1.00 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | – | 1.00 | 1.00 | 1.00 |
| citation recall | – | 1.00 | 1.00 | 1.00 |
| citation F1 | – | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 2 | 2 |
| tokens | 2822 | 1610 | 12490 | 12589 |
| cost (USD) | 0.0005 | 0.0003 | 0.0477 | 0.0486 |
| latency (s) | 3.6 | 8.4 | 21.6 | 23.2 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 3.

**Generated answer**

> Meta says it justifies its Family metrics methodology by arguing that simply counting total user accounts across products would overstate the size of its community, because many people have more than one account and may use multiple Meta products. So instead, Family metrics are intended to estimate the number of unique people using at least one of Facebook, Instagram, Messenger, and WhatsApp. To do this, Meta uses complex techniques, algorithms, and machine learning models to match multiple accounts within and across products when it believes they belong to the same person, and then counts that group as one person [3][5].
>
> Meta cites two specific data limitations affecting this process:
>
> - **WhatsApp:** Because of limited visibility into encrypted products, Meta says it has fewer data signals from WhatsApp accounts and primarily relies on **phone numbers and device information** to match WhatsApp accounts with accounts on its other products [2].
> - **Messenger Kids:** Although Messenger Kids users are included in Family metrics, Meta says it **does not seek to match their accounts with accounts on its other applications** for purposes of calculating DAP and MAP [2].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2021_2021-12-31:135` | Item 1A › Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business. |  | #2, #3 | signals from WhatsApp user accounts and primarily rely on phone numbers and device information to match WhatsApp user accounts with accounts on our other products. Similarly, although Messenger Kids users are included in… |
| 2 | `META_FY2021_2021-12-31:22` | Family Metrics | ✓ | #2, #3 | for some products compared to others. For example, as a result of limited visibility into encrypted products, we have fewer data signals from WhatsApp user accounts and primarily rely on phone numbers and device informat… |
| 3 | `META_FY2021_2021-12-31:19` | Family Metrics | ✓ | #1 | Many people in our community have user accounts on more than one of our products, and some people have multiple user accounts within an individual product. Accordingly, for our Family metrics, we do not seek to count the… |
| 4 | `META_FY2021_2021-12-31:131` | Item 1A › Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business. |  | #1 | update previously disclosed Family metrics for any such inaccuracies or adjustments that are within the error margins disclosed below. In addition, our Family metrics and Facebook metrics estimates will differ from estim… |
| 5 | `META_FY2021_2021-12-31:17` | LIMITATIONS OF KEY METRICS AND OTHER DATA | ✓ | #1 | The numbers for our key metrics are calculated using internal company data based on the activity of user accounts. We have historically reported the numbers of our daily active users (DAUs), monthly active users (MAUs), … |
| 6 | `META_FY2021_2021-12-31:268` | Item 7 › Trends in Our Family Metrics |  |  | Note: We report the numbers of DAP and MAP as specific amounts, but these numbers are estimates of the numbers of unique people using our products and are subject to statistical variances and errors. While we expect the … |
| 7 | `META_FY2021_2021-12-31:264` | Item 7 › Trends in Our Family Metrics |  |  | Note: We report the numbers of DAP and MAP as specific amounts, but these numbers are estimates of the numbers of unique people using our products and are subject to statistical variances and errors. While we expect the … |
| 8 | `META_FY2021_2021-12-31:132` | Item 1A › Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business. |  |  | and WhatsApp. We do not require people to use a common identifier or link their accounts to use multiple products in our Family, and therefore must seek to attribute multiple user accounts within and across products to i… |
| 9 | `META_FY2021_2021-12-31:24` | Family Metrics |  | #3 | We regularly evaluate our Family metrics to estimate the percentage of our MAP consisting solely of "violating" accounts. We define "violating" accounts as accounts which we believe are intended to be used for purposes t… |
| 10 | `META_FY2021_2021-12-31:18` | LIMITATIONS OF KEY METRICS AND OTHER DATA |  |  | While these numbers are based on what we believe to be reasonable estimates of our user base for the applicable period of measurement, there are inherent challenges in measuring usage of our products across large online … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2021_2021-12-31:135`** (gold #2, gold #3)

````text
Item 1A.Risk Factors > Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business.
signals from WhatsApp user accounts and primarily rely on phone numbers and device information to match WhatsApp user accounts with accounts on our other products. Similarly, although Messenger Kids users are included in our Family metrics, we do not seek to match their accounts with accounts on our other applications for purposes of calculating DAP and MAP. Any loss of access to data signals we use in our process for calculating Family metrics, whether as a result of our own product decisions, actions by third-party browser or mobile platforms, regulatory or legislative requirements, limitations while our personnel work remotely during the COVID-19 pandemic, or other factors, also may impact the stability or accuracy of our reported Family metrics, as well as our ability to report these metrics at all. Our estimates of Family metrics also may change as our methodologies evolve, including through the application of new data signals or technologies, product changes, or other improvements in our user surveys, algorithms, or machine learning that may improve our ability to match accounts within and across our products or otherwise evaluate the broad population of our users. In addition, such evolution may allow us to identify previously undetected violating accounts (as
````

**#2 `META_FY2021_2021-12-31:22`** (cited, gold #2, gold #3)

````text
Family Metrics
for some products compared to others. For example, as a result of limited visibility into encrypted products, we have fewer data signals from WhatsApp user accounts and primarily rely on phone numbers and device information to match WhatsApp user accounts with accounts on our other products. Similarly, although Messenger Kids users are included in our Family metrics, we do not seek to match their accounts with accounts on our other applications for purposes of calculating DAP and MAP. Any loss of access to data signals we use in our process for calculating Family metrics, whether as a result of our own product decisions, actions by third-party browser or mobile platforms, regulatory or legislative requirements, limitations while our personnel work remotely during the COVID-19 pandemic, or other factors, also may impact the stability or accuracy of our reported Family metrics, as well as our ability to report these metrics at all. Our estimates of Family metrics also may change as our methodologies evolve, including through the application of new data signals or technologies, product changes, or other improvements in our user surveys, algorithms, or machine learning that may improve our ability to match accounts within and across our products or otherwise
````

**#3 `META_FY2021_2021-12-31:19`** (cited, gold #1)

````text
Family Metrics
Many people in our community have user accounts on more than one of our products, and some people have multiple user accounts within an individual product. Accordingly, for our Family metrics, we do not seek to count the total number of user accounts across our products because we believe that would not reflect the actual size of our community. Rather, our Family metrics represent our estimates of the number of unique people using at least one of Facebook, Instagram, Messenger, and WhatsApp. We do not require people to use a common identifier or link their accounts to use multiple products in our Family, and therefore must seek to attribute multiple user accounts within and across products to individual people. To calculate these metrics, we rely upon complex techniques, algorithms and machine learning models that seek to count the individual people behind user accounts, including by matching multiple user accounts within an individual product and across multiple products when we believe they are attributable to a single person, and counting such group of accounts as one person. These techniques and models require significant judgment, are subject to data and other limitations discussed below, and inherently are subject to statistical variances and
````

**#4 `META_FY2021_2021-12-31:131`** (gold #1)

````text
Item 1A.Risk Factors > Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business.
update previously disclosed Family metrics for any such inaccuracies or adjustments that are within the error margins disclosed below. In addition, our Family metrics and Facebook metrics estimates will differ from estimates published by third parties due to differences in methodology. Many people in our community have user accounts on more than one of our products, and some people have multiple user accounts within an individual product. Accordingly, for our Family metrics, we do not seek to count the total number of user accounts across our products because we believe that would not reflect the actual size of our community. Rather, our Family metrics represent our estimates of the number of unique people using at least one of Facebook, Instagram, Messenger,
````

**#5 `META_FY2021_2021-12-31:17`** (cited, gold #1)

````text
LIMITATIONS OF KEY METRICS AND OTHER DATA
The numbers for our key metrics are calculated using internal company data based on the activity of user accounts. We have historically reported the numbers of our daily active users (DAUs), monthly active users (MAUs), and average revenue per user (ARPU) (collectively, our "Facebook metrics") based on user activity only on Facebook and Messenger and not on our other products. Beginning with our Annual Report on Form 10-K for the year ended December 31, 2019, we also report our estimates of the numbers of our daily active people (DAP), monthly active people (MAP), and average revenue per person (ARPP) (collectively, our "Family metrics") based on the activity of users who visited at least one of Facebook, Instagram, Messenger, and WhatsApp (collectively, our "Family" of products) during the applicable period of measurement. We believe our Family metrics better reflect the size of our community and the fact that many people are using more than one of our products. As a result, over time we intend to report our Family metrics as key metrics in place of DAUs, MAUs, and ARPU in our periodic reports filed with the Securities and Exchange Commission.
````

**#9 `META_FY2021_2021-12-31:24`** (gold #3)

````text
Family Metrics
We regularly evaluate our Family metrics to estimate the percentage of our MAP consisting solely of "violating" accounts. We define "violating" accounts as accounts which we believe are intended to be used for purposes that violate our terms of service, including bots and spam. In the fourth quarter of 2021, we estimated that approximately 3% of our worldwide MAP consisted solely of violating accounts. Such estimation is based on an internal review of a limited sample of accounts, and we apply significant judgment in making this determination. For example, we look for account information and behaviors associated with Facebook and Instagram accounts that appear to be inauthentic to the reviewers, but we have limited visibility into WhatsApp user activity due to encryption. In addition, if we believe an individual person has one or more violating accounts, we do not include such person in our violating accounts estimation as long as we believe they have one account that does not constitute a violating account. From time to time, we disable certain user accounts, make product changes, or take other actions to reduce the number of violating accounts among our users, which may also reduce our DAP and MAP estimates in a
````

</details>

RQ2 citation match (section level): `no citations`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 5.

**Generated answer**

> Meta says it calculates Family metrics as estimates of the number of unique people using at least one of Facebook, Instagram, Messenger, and WhatsApp, rather than simply counting total user accounts, because many people have multiple accounts across or within its products and a raw account count would not reflect the actual size of its community. To do this, it uses complex techniques, algorithms, and machine learning models to match accounts it believes belong to the same person and count them as one person. Meta justifies this approach as a better reflection of its community size, even though it acknowledges the process requires significant judgment and is subject to statistical variance and uncertainty [2][4][5].
>
> For data limitations, Meta specifically says that for WhatsApp it has limited visibility into encrypted products, so it has fewer data signals from WhatsApp user accounts and primarily relies on phone numbers and device information to match WhatsApp accounts with accounts on its other products. For Messenger Kids, although those users are included in Family metrics, Meta does not seek to match their accounts with accounts on its other applications for purposes of calculating DAP and MAP [1][3].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2021_2021-12-31:22` | Family Metrics | ✓ | #2, #3 | for some products compared to others. For example, as a result of limited visibility into encrypted products, we have fewer data signals from WhatsApp user accounts and primarily rely on phone numbers and device informat… |
| 2 | `META_FY2021_2021-12-31:19` | Family Metrics | ✓ | #1 | Many people in our community have user accounts on more than one of our products, and some people have multiple user accounts within an individual product. Accordingly, for our Family metrics, we do not seek to count the… |
| 3 | `META_FY2021_2021-12-31:135` | Item 1A › Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business. | ✓ | #2, #3 | signals from WhatsApp user accounts and primarily rely on phone numbers and device information to match WhatsApp user accounts with accounts on our other products. Similarly, although Messenger Kids users are included in… |
| 4 | `META_FY2021_2021-12-31:17` | LIMITATIONS OF KEY METRICS AND OTHER DATA | ✓ | #1 | The numbers for our key metrics are calculated using internal company data based on the activity of user accounts. We have historically reported the numbers of our daily active users (DAUs), monthly active users (MAUs), … |
| 5 | `META_FY2021_2021-12-31:132` | Item 1A › Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business. | ✓ |  | and WhatsApp. We do not require people to use a common identifier or link their accounts to use multiple products in our Family, and therefore must seek to attribute multiple user accounts within and across products to i… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2021_2021-12-31:22`** (cited, gold #2, gold #3)

````text
Family Metrics
for some products compared to others. For example, as a result of limited visibility into encrypted products, we have fewer data signals from WhatsApp user accounts and primarily rely on phone numbers and device information to match WhatsApp user accounts with accounts on our other products. Similarly, although Messenger Kids users are included in our Family metrics, we do not seek to match their accounts with accounts on our other applications for purposes of calculating DAP and MAP. Any loss of access to data signals we use in our process for calculating Family metrics, whether as a result of our own product decisions, actions by third-party browser or mobile platforms, regulatory or legislative requirements, limitations while our personnel work remotely during the COVID-19 pandemic, or other factors, also may impact the stability or accuracy of our reported Family metrics, as well as our ability to report these metrics at all. Our estimates of Family metrics also may change as our methodologies evolve, including through the application of new data signals or technologies, product changes, or other improvements in our user surveys, algorithms, or machine learning that may improve our ability to match accounts within and across our products or otherwise
````

**#2 `META_FY2021_2021-12-31:19`** (cited, gold #1)

````text
Family Metrics
Many people in our community have user accounts on more than one of our products, and some people have multiple user accounts within an individual product. Accordingly, for our Family metrics, we do not seek to count the total number of user accounts across our products because we believe that would not reflect the actual size of our community. Rather, our Family metrics represent our estimates of the number of unique people using at least one of Facebook, Instagram, Messenger, and WhatsApp. We do not require people to use a common identifier or link their accounts to use multiple products in our Family, and therefore must seek to attribute multiple user accounts within and across products to individual people. To calculate these metrics, we rely upon complex techniques, algorithms and machine learning models that seek to count the individual people behind user accounts, including by matching multiple user accounts within an individual product and across multiple products when we believe they are attributable to a single person, and counting such group of accounts as one person. These techniques and models require significant judgment, are subject to data and other limitations discussed below, and inherently are subject to statistical variances and
````

**#3 `META_FY2021_2021-12-31:135`** (cited, gold #2, gold #3)

````text
Item 1A.Risk Factors > Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business.
signals from WhatsApp user accounts and primarily rely on phone numbers and device information to match WhatsApp user accounts with accounts on our other products. Similarly, although Messenger Kids users are included in our Family metrics, we do not seek to match their accounts with accounts on our other applications for purposes of calculating DAP and MAP. Any loss of access to data signals we use in our process for calculating Family metrics, whether as a result of our own product decisions, actions by third-party browser or mobile platforms, regulatory or legislative requirements, limitations while our personnel work remotely during the COVID-19 pandemic, or other factors, also may impact the stability or accuracy of our reported Family metrics, as well as our ability to report these metrics at all. Our estimates of Family metrics also may change as our methodologies evolve, including through the application of new data signals or technologies, product changes, or other improvements in our user surveys, algorithms, or machine learning that may improve our ability to match accounts within and across our products or otherwise evaluate the broad population of our users. In addition, such evolution may allow us to identify previously undetected violating accounts (as
````

**#4 `META_FY2021_2021-12-31:17`** (cited, gold #1)

````text
LIMITATIONS OF KEY METRICS AND OTHER DATA
The numbers for our key metrics are calculated using internal company data based on the activity of user accounts. We have historically reported the numbers of our daily active users (DAUs), monthly active users (MAUs), and average revenue per user (ARPU) (collectively, our "Facebook metrics") based on user activity only on Facebook and Messenger and not on our other products. Beginning with our Annual Report on Form 10-K for the year ended December 31, 2019, we also report our estimates of the numbers of our daily active people (DAP), monthly active people (MAP), and average revenue per person (ARPP) (collectively, our "Family metrics") based on the activity of users who visited at least one of Facebook, Instagram, Messenger, and WhatsApp (collectively, our "Family" of products) during the applicable period of measurement. We believe our Family metrics better reflect the size of our community and the fact that many people are using more than one of our products. As a result, over time we intend to report our Family metrics as key metrics in place of DAUs, MAUs, and ARPU in our periodic reports filed with the Securities and Exchange Commission.
````

**#5 `META_FY2021_2021-12-31:132`** (cited)

````text
Item 1A.Risk Factors > Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business.
and WhatsApp. We do not require people to use a common identifier or link their accounts to use multiple products in our Family, and therefore must seek to attribute multiple user accounts within and across products to individual people. To calculate these metrics, we rely upon complex techniques, algorithms and machine learning models that seek to count the individual people behind user accounts, including by matching multiple user accounts within an individual product and across multiple products when we believe they are attributable to a single person, and counting such group of accounts as one person. These techniques and models require significant judgment, are subject to data and other limitations discussed below, and inherently are subject to statistical variances and uncertainties. We estimate the potential error in our Family metrics primarily based on user survey data, which itself is subject to error as well. While we expect the error margin for our Family metrics to vary from period to period, we estimate that such margin generally will be approximately 3% of our worldwide MAP. At our scale, it is very difficult to attribute multiple user accounts within and across products to individual people, and it is possible that the actual
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 1A')] gold=[(None, 'Item 1A')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 9, cited: 7.

**Generated answer**

> Meta justifies its Family metrics methodology by stating that many people have user accounts on more than one of its products, and some people have multiple user accounts within an individual product, so counting total user accounts across products would not reflect the actual size of its community. [META FY2021, 10-K, META_FY2021_2021-12-31:19] [META FY2021, Item 1A, META_FY2021_2021-12-31:131]
>
> The company says its Family metrics are intended to estimate the number of unique people using at least one of Facebook, Instagram, Messenger, and WhatsApp, which it believes better reflects the size of its community and the fact that many people use more than one of its products. [META FY2021, 10-K, META_FY2021_2021-12-31:19] [META FY2021, 10-K, META_FY2021_2021-12-31:17]
>
> To do this, Meta uses complex techniques, algorithms, and machine learning models to count the individual people behind user accounts, including matching multiple accounts within a product and across products when it believes they are attributable to a single person and then counting that group of accounts as one person. [META FY2021, 10-K, META_FY2021_2021-12-31:19]
>
> Meta also says it does not require people to use a common identifier or link their accounts across products, so it must attribute multiple user accounts within and across products to individual people using these methods. [META FY2021, 10-K, META_FY2021_2021-12-31:19]
>
> The company acknowledges that these techniques require significant judgment and are subject to data limitations, statistical variances, algorithmic or technical errors, and methodology changes over time. [META FY2021, 10-K, META_FY2021_2021-12-31:21] [META FY2021, 10-K, META_FY2021_2021-12-31:19] [META FY2021, 10-K, META_FY2021_2021-12-31:18]
>
> Regarding WhatsApp, Meta cites limited visibility into encrypted products, which means it has fewer data signals from WhatsApp user accounts and primarily relies on phone numbers and device information to match WhatsApp accounts with accounts on its other products. [META FY2021, 10-K, META_FY2021_2021-12-31:22] [META FY2021, Item 1A, META_FY2021_2021-12-31:135]
>
> Regarding Messenger Kids, Meta says those users are included in Family metrics, but it does not seek to match their accounts with accounts on its other applications for purposes of calculating DAP and MAP. [META FY2021, 10-K, META_FY2021_2021-12-31:22] [META FY2021, Item 1A, META_FY2021_2021-12-31:135]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2021_2021-12-31:21` | Family Metrics | ✓ | #2 | To calculate our estimates of Family DAP and MAP, we currently use a series of machine learning models that are developed based on internal reviews of limited samples of user accounts and calibrated against user survey d… |
| 2 | `META_FY2021_2021-12-31:268` | Item 7 › Trends in Our Family Metrics |  |  | Note: We report the numbers of DAP and MAP as specific amounts, but these numbers are estimates of the numbers of unique people using our products and are subject to statistical variances and errors. While we expect the … |
| 3 | `META_FY2021_2021-12-31:19` | Family Metrics | ✓ | #1 | Many people in our community have user accounts on more than one of our products, and some people have multiple user accounts within an individual product. Accordingly, for our Family metrics, we do not seek to count the… |
| 4 | `META_FY2021_2021-12-31:264` | Item 7 › Trends in Our Family Metrics |  |  | Note: We report the numbers of DAP and MAP as specific amounts, but these numbers are estimates of the numbers of unique people using our products and are subject to statistical variances and errors. While we expect the … |
| 5 | `META_FY2021_2021-12-31:18` | LIMITATIONS OF KEY METRICS AND OTHER DATA | ✓ |  | While these numbers are based on what we believe to be reasonable estimates of our user base for the applicable period of measurement, there are inherent challenges in measuring usage of our products across large online … |
| 6 | `META_FY2021_2021-12-31:131` | Item 1A › Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business. | ✓ | #1 | update previously disclosed Family metrics for any such inaccuracies or adjustments that are within the error margins disclosed below. In addition, our Family metrics and Facebook metrics estimates will differ from estim… |
| 7 | `META_FY2021_2021-12-31:22` | Family Metrics | ✓ | #2, #3 | for some products compared to others. For example, as a result of limited visibility into encrypted products, we have fewer data signals from WhatsApp user accounts and primarily rely on phone numbers and device informat… |
| 8 | `META_FY2021_2021-12-31:135` | Item 1A › Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business. | ✓ | #2, #3 | signals from WhatsApp user accounts and primarily rely on phone numbers and device information to match WhatsApp user accounts with accounts on our other products. Similarly, although Messenger Kids users are included in… |
| 9 | `META_FY2021_2021-12-31:17` | LIMITATIONS OF KEY METRICS AND OTHER DATA | ✓ | #1 | The numbers for our key metrics are calculated using internal company data based on the activity of user accounts. We have historically reported the numbers of our daily active users (DAUs), monthly active users (MAUs), … |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2021_2021-12-31:21`** (cited, gold #2)

````text
Family Metrics
To calculate our estimates of Family DAP and MAP, we currently use a series of machine learning models that are developed based on internal reviews of limited samples of user accounts and calibrated against user survey data. We apply significant judgment in designing these models and calculating these estimates. For example, to match user accounts within individual products and across multiple products, we use data signals such as similar device information, IP addresses, and user names. We also calibrate our models against data from periodic user surveys of varying sizes and frequency across our products, which are inherently subject to error. The timing and results of such user surveys have in the past contributed, and may in the future contribute, to changes in our reported Family metrics from period to period. In addition, our data limitations may affect our understanding of certain details of our business and increase the risk of error for our Family metrics estimates. Our techniques and models rely on a variety of data signals from different products, and we rely on more limited data signals
````

**#3 `META_FY2021_2021-12-31:19`** (cited, gold #1)

````text
Family Metrics
Many people in our community have user accounts on more than one of our products, and some people have multiple user accounts within an individual product. Accordingly, for our Family metrics, we do not seek to count the total number of user accounts across our products because we believe that would not reflect the actual size of our community. Rather, our Family metrics represent our estimates of the number of unique people using at least one of Facebook, Instagram, Messenger, and WhatsApp. We do not require people to use a common identifier or link their accounts to use multiple products in our Family, and therefore must seek to attribute multiple user accounts within and across products to individual people. To calculate these metrics, we rely upon complex techniques, algorithms and machine learning models that seek to count the individual people behind user accounts, including by matching multiple user accounts within an individual product and across multiple products when we believe they are attributable to a single person, and counting such group of accounts as one person. These techniques and models require significant judgment, are subject to data and other limitations discussed below, and inherently are subject to statistical variances and
````

**#5 `META_FY2021_2021-12-31:18`** (cited)

````text
LIMITATIONS OF KEY METRICS AND OTHER DATA
While these numbers are based on what we believe to be reasonable estimates of our user base for the applicable period of measurement, there are inherent challenges in measuring usage of our products across large online and mobile populations around the world. The methodologies used to measure these metrics require significant judgment and are also susceptible to algorithm or other technical errors. In addition, we are continually seeking to improve our estimates of our user base, and such estimates may change due to improvements or changes in our methodology. We regularly review our processes for calculating these metrics, and from time to time we discover inaccuracies in our metrics or make adjustments to improve their accuracy, which can result in adjustments to our historical metrics. Our ability to recalculate our historical metrics may be impacted by data limitations or other factors that require us to apply different methodologies for such adjustments. We generally do not intend to update previously disclosed Family metrics for any such inaccuracies or adjustments that are within the error margins disclosed below. In addition, our Family metrics and Facebook metrics estimates will differ from estimates published by third parties due to differences in methodology.
````

**#6 `META_FY2021_2021-12-31:131`** (cited, gold #1)

````text
Item 1A.Risk Factors > Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business.
update previously disclosed Family metrics for any such inaccuracies or adjustments that are within the error margins disclosed below. In addition, our Family metrics and Facebook metrics estimates will differ from estimates published by third parties due to differences in methodology. Many people in our community have user accounts on more than one of our products, and some people have multiple user accounts within an individual product. Accordingly, for our Family metrics, we do not seek to count the total number of user accounts across our products because we believe that would not reflect the actual size of our community. Rather, our Family metrics represent our estimates of the number of unique people using at least one of Facebook, Instagram, Messenger,
````

**#7 `META_FY2021_2021-12-31:22`** (cited, gold #2, gold #3)

````text
Family Metrics
for some products compared to others. For example, as a result of limited visibility into encrypted products, we have fewer data signals from WhatsApp user accounts and primarily rely on phone numbers and device information to match WhatsApp user accounts with accounts on our other products. Similarly, although Messenger Kids users are included in our Family metrics, we do not seek to match their accounts with accounts on our other applications for purposes of calculating DAP and MAP. Any loss of access to data signals we use in our process for calculating Family metrics, whether as a result of our own product decisions, actions by third-party browser or mobile platforms, regulatory or legislative requirements, limitations while our personnel work remotely during the COVID-19 pandemic, or other factors, also may impact the stability or accuracy of our reported Family metrics, as well as our ability to report these metrics at all. Our estimates of Family metrics also may change as our methodologies evolve, including through the application of new data signals or technologies, product changes, or other improvements in our user surveys, algorithms, or machine learning that may improve our ability to match accounts within and across our products or otherwise
````

**#8 `META_FY2021_2021-12-31:135`** (cited, gold #2, gold #3)

````text
Item 1A.Risk Factors > Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business.
signals from WhatsApp user accounts and primarily rely on phone numbers and device information to match WhatsApp user accounts with accounts on our other products. Similarly, although Messenger Kids users are included in our Family metrics, we do not seek to match their accounts with accounts on our other applications for purposes of calculating DAP and MAP. Any loss of access to data signals we use in our process for calculating Family metrics, whether as a result of our own product decisions, actions by third-party browser or mobile platforms, regulatory or legislative requirements, limitations while our personnel work remotely during the COVID-19 pandemic, or other factors, also may impact the stability or accuracy of our reported Family metrics, as well as our ability to report these metrics at all. Our estimates of Family metrics also may change as our methodologies evolve, including through the application of new data signals or technologies, product changes, or other improvements in our user surveys, algorithms, or machine learning that may improve our ability to match accounts within and across our products or otherwise evaluate the broad population of our users. In addition, such evolution may allow us to identify previously undetected violating accounts (as
````

**#9 `META_FY2021_2021-12-31:17`** (cited, gold #1)

````text
LIMITATIONS OF KEY METRICS AND OTHER DATA
The numbers for our key metrics are calculated using internal company data based on the activity of user accounts. We have historically reported the numbers of our daily active users (DAUs), monthly active users (MAUs), and average revenue per user (ARPU) (collectively, our "Facebook metrics") based on user activity only on Facebook and Messenger and not on our other products. Beginning with our Annual Report on Form 10-K for the year ended December 31, 2019, we also report our estimates of the numbers of our daily active people (DAP), monthly active people (MAP), and average revenue per person (ARPP) (collectively, our "Family metrics") based on the activity of users who visited at least one of Facebook, Instagram, Messenger, and WhatsApp (collectively, our "Family" of products) during the applicable period of measurement. We believe our Family metrics better reflect the size of our community and the fact that many people are using more than one of our products. As a result, over time we intend to report our Family metrics as key metrics in place of DAUs, MAUs, and ARPU in our periodic reports filed with the Securities and Exchange Commission.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 1A')] gold=[(None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 7, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta justifies its Family metrics methodology by stating that many people have user accounts on more than one of its products, and some people have multiple user accounts within an individual product, so counting total user accounts across products would not reflect the actual size of its community. [META FY2021, 10-K, META_FY2021_2021-12-31:19] [META FY2021, Item 1A, META_FY2021_2021-12-31:131] | supported | The cited text explicitly gives that rationale for not counting total user accounts across products. |
| The company says its Family metrics are intended to estimate the number of unique people using at least one of Facebook, Instagram, Messenger, and WhatsApp, which it believes better reflects the size of its community and the fact that many people use more than one of its products. [META FY2021, 10-K, META_FY2021_2021-12-31:19] [META FY2021, 10-K, META_FY2021_2021-12-31:17] | supported | The evidence states Family metrics estimate unique people using at least one listed product and says this better reflects community size because many use more than one product. |
| To do this, Meta uses complex techniques, algorithms, and machine learning models to count the individual people behind user accounts, including matching multiple accounts within a product and across products when it believes they are attributable to a single person and then counting that group of accounts as one person. [META FY2021, 10-K, META_FY2021_2021-12-31:19] | supported | The cited passage directly describes using complex techniques, algorithms, and machine learning to match accounts and count them as one person. |
| Meta also says it does not require people to use a common identifier or link their accounts across products, so it must attribute multiple user accounts within and across products to individual people using these methods. [META FY2021, 10-K, META_FY2021_2021-12-31:19] | supported | The evidence expressly says Meta does not require a common identifier or linked accounts and therefore must attribute multiple accounts to individual people. |
| The company acknowledges that these techniques require significant judgment and are subject to data limitations, statistical variances, algorithmic or technical errors, and methodology changes over time. [META FY2021, 10-K, META_FY2021_2021-12-31:21] [META FY2021, 10-K, META_FY2021_2021-12-31:19] [META FY2021, 10-K, META_FY2021_2021-12-31:18] | supported | The cited evidence states the methods require significant judgment and are subject to data limitations, statistical variances, technical errors, and methodology changes. |
| Regarding WhatsApp, Meta cites limited visibility into encrypted products, which means it has fewer data signals from WhatsApp user accounts and primarily relies on phone numbers and device information to match WhatsApp accounts with accounts on its other products. [META FY2021, 10-K, META_FY2021_2021-12-31:22] [META FY2021, Item 1A, META_FY2021_2021-12-31:135] | supported | The evidence explicitly says limited visibility into encrypted products leaves fewer WhatsApp data signals and that matching primarily relies on phone numbers and device information. |
| Regarding Messenger Kids, Meta says those users are included in Family metrics, but it does not seek to match their accounts with accounts on its other applications for purposes of calculating DAP and MAP. [META FY2021, 10-K, META_FY2021_2021-12-31:22] [META FY2021, Item 1A, META_FY2021_2021-12-31:135] | supported | The cited text directly states Messenger Kids users are included in Family metrics but are not matched with other application accounts for DAP and MAP. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 2. Chunks retrieved: 9, cited: 7.

**Generated answer**

> Meta justifies its methodology for calculating Family metrics by stating that many people use more than one of its products and some people have multiple accounts within a single product, so counting total user accounts would not reflect the actual size of its community; instead, Family metrics are intended to estimate the number of unique people using at least one of Facebook, Instagram, Messenger, and WhatsApp. [META FY2021, 10-K, META_FY2021_2021-12-31:19] [META FY2021, Item 1A, META_FY2021_2021-12-31:131] [META FY2021, 10-K, META_FY2021_2021-12-31:17]
>
> The company says it does not require people to use a common identifier or link their accounts across products, so it uses complex techniques, algorithms, and machine learning models to attribute multiple accounts within and across products to individual people and count those grouped accounts as one person. [META FY2021, 10-K, META_FY2021_2021-12-31:19]
>
> Meta also says these estimates are based on internal company data from user account activity and are meant to better reflect the size of its community and the fact that many people use more than one of its products. [META FY2021, 10-K, META_FY2021_2021-12-31:17]
>
> To build these estimates, Meta says it uses machine learning models developed from internal reviews of limited samples of user accounts and calibrated against user survey data, applying significant judgment and using signals such as similar device information, IP addresses, and user names to match accounts. [META FY2021, 10-K, META_FY2021_2021-12-31:21]
>
> Meta further notes that these methodologies require significant judgment and are subject to data limitations, statistical variances, algorithm or other technical errors, and changes from methodology improvements or recalibrations over time. [META FY2021, 10-K, META_FY2021_2021-12-31:21] [META FY2021, 10-K, META_FY2021_2021-12-31:19] [META FY2021, 10-K, META_FY2021_2021-12-31:18]
>
> Regarding WhatsApp, Meta cites limited visibility into encrypted products, which means it has fewer data signals from WhatsApp user accounts and primarily relies on phone numbers and device information to match WhatsApp accounts with accounts on its other products. [META FY2021, 10-K, META_FY2021_2021-12-31:22] [META FY2021, Item 1A, META_FY2021_2021-12-31:135]
>
> Regarding Messenger Kids, Meta says those users are included in Family metrics, but it does not seek to match their accounts with accounts on its other applications for purposes of calculating DAP and MAP. [META FY2021, 10-K, META_FY2021_2021-12-31:22] [META FY2021, Item 1A, META_FY2021_2021-12-31:135]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2021_2021-12-31:21` | Family Metrics | ✓ | #2 | To calculate our estimates of Family DAP and MAP, we currently use a series of machine learning models that are developed based on internal reviews of limited samples of user accounts and calibrated against user survey d… |
| 2 | `META_FY2021_2021-12-31:268` | Item 7 › Trends in Our Family Metrics |  |  | Note: We report the numbers of DAP and MAP as specific amounts, but these numbers are estimates of the numbers of unique people using our products and are subject to statistical variances and errors. While we expect the … |
| 3 | `META_FY2021_2021-12-31:19` | Family Metrics | ✓ | #1 | Many people in our community have user accounts on more than one of our products, and some people have multiple user accounts within an individual product. Accordingly, for our Family metrics, we do not seek to count the… |
| 4 | `META_FY2021_2021-12-31:264` | Item 7 › Trends in Our Family Metrics |  |  | Note: We report the numbers of DAP and MAP as specific amounts, but these numbers are estimates of the numbers of unique people using our products and are subject to statistical variances and errors. While we expect the … |
| 5 | `META_FY2021_2021-12-31:18` | LIMITATIONS OF KEY METRICS AND OTHER DATA | ✓ |  | While these numbers are based on what we believe to be reasonable estimates of our user base for the applicable period of measurement, there are inherent challenges in measuring usage of our products across large online … |
| 6 | `META_FY2021_2021-12-31:131` | Item 1A › Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business. | ✓ | #1 | update previously disclosed Family metrics for any such inaccuracies or adjustments that are within the error margins disclosed below. In addition, our Family metrics and Facebook metrics estimates will differ from estim… |
| 7 | `META_FY2021_2021-12-31:17` | LIMITATIONS OF KEY METRICS AND OTHER DATA | ✓ | #1 | The numbers for our key metrics are calculated using internal company data based on the activity of user accounts. We have historically reported the numbers of our daily active users (DAUs), monthly active users (MAUs), … |
| 8 | `META_FY2021_2021-12-31:22` | Family Metrics | ✓ | #2, #3 | for some products compared to others. For example, as a result of limited visibility into encrypted products, we have fewer data signals from WhatsApp user accounts and primarily rely on phone numbers and device informat… |
| 9 | `META_FY2021_2021-12-31:135` | Item 1A › Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business. | ✓ | #2, #3 | signals from WhatsApp user accounts and primarily rely on phone numbers and device information to match WhatsApp user accounts with accounts on our other products. Similarly, although Messenger Kids users are included in… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2021_2021-12-31:21`** (cited, gold #2)

````text
Family Metrics
To calculate our estimates of Family DAP and MAP, we currently use a series of machine learning models that are developed based on internal reviews of limited samples of user accounts and calibrated against user survey data. We apply significant judgment in designing these models and calculating these estimates. For example, to match user accounts within individual products and across multiple products, we use data signals such as similar device information, IP addresses, and user names. We also calibrate our models against data from periodic user surveys of varying sizes and frequency across our products, which are inherently subject to error. The timing and results of such user surveys have in the past contributed, and may in the future contribute, to changes in our reported Family metrics from period to period. In addition, our data limitations may affect our understanding of certain details of our business and increase the risk of error for our Family metrics estimates. Our techniques and models rely on a variety of data signals from different products, and we rely on more limited data signals
````

**#3 `META_FY2021_2021-12-31:19`** (cited, gold #1)

````text
Family Metrics
Many people in our community have user accounts on more than one of our products, and some people have multiple user accounts within an individual product. Accordingly, for our Family metrics, we do not seek to count the total number of user accounts across our products because we believe that would not reflect the actual size of our community. Rather, our Family metrics represent our estimates of the number of unique people using at least one of Facebook, Instagram, Messenger, and WhatsApp. We do not require people to use a common identifier or link their accounts to use multiple products in our Family, and therefore must seek to attribute multiple user accounts within and across products to individual people. To calculate these metrics, we rely upon complex techniques, algorithms and machine learning models that seek to count the individual people behind user accounts, including by matching multiple user accounts within an individual product and across multiple products when we believe they are attributable to a single person, and counting such group of accounts as one person. These techniques and models require significant judgment, are subject to data and other limitations discussed below, and inherently are subject to statistical variances and
````

**#5 `META_FY2021_2021-12-31:18`** (cited)

````text
LIMITATIONS OF KEY METRICS AND OTHER DATA
While these numbers are based on what we believe to be reasonable estimates of our user base for the applicable period of measurement, there are inherent challenges in measuring usage of our products across large online and mobile populations around the world. The methodologies used to measure these metrics require significant judgment and are also susceptible to algorithm or other technical errors. In addition, we are continually seeking to improve our estimates of our user base, and such estimates may change due to improvements or changes in our methodology. We regularly review our processes for calculating these metrics, and from time to time we discover inaccuracies in our metrics or make adjustments to improve their accuracy, which can result in adjustments to our historical metrics. Our ability to recalculate our historical metrics may be impacted by data limitations or other factors that require us to apply different methodologies for such adjustments. We generally do not intend to update previously disclosed Family metrics for any such inaccuracies or adjustments that are within the error margins disclosed below. In addition, our Family metrics and Facebook metrics estimates will differ from estimates published by third parties due to differences in methodology.
````

**#6 `META_FY2021_2021-12-31:131`** (cited, gold #1)

````text
Item 1A.Risk Factors > Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business.
update previously disclosed Family metrics for any such inaccuracies or adjustments that are within the error margins disclosed below. In addition, our Family metrics and Facebook metrics estimates will differ from estimates published by third parties due to differences in methodology. Many people in our community have user accounts on more than one of our products, and some people have multiple user accounts within an individual product. Accordingly, for our Family metrics, we do not seek to count the total number of user accounts across our products because we believe that would not reflect the actual size of our community. Rather, our Family metrics represent our estimates of the number of unique people using at least one of Facebook, Instagram, Messenger,
````

**#7 `META_FY2021_2021-12-31:17`** (cited, gold #1)

````text
LIMITATIONS OF KEY METRICS AND OTHER DATA
The numbers for our key metrics are calculated using internal company data based on the activity of user accounts. We have historically reported the numbers of our daily active users (DAUs), monthly active users (MAUs), and average revenue per user (ARPU) (collectively, our "Facebook metrics") based on user activity only on Facebook and Messenger and not on our other products. Beginning with our Annual Report on Form 10-K for the year ended December 31, 2019, we also report our estimates of the numbers of our daily active people (DAP), monthly active people (MAP), and average revenue per person (ARPP) (collectively, our "Family metrics") based on the activity of users who visited at least one of Facebook, Instagram, Messenger, and WhatsApp (collectively, our "Family" of products) during the applicable period of measurement. We believe our Family metrics better reflect the size of our community and the fact that many people are using more than one of our products. As a result, over time we intend to report our Family metrics as key metrics in place of DAUs, MAUs, and ARPU in our periodic reports filed with the Securities and Exchange Commission.
````

**#8 `META_FY2021_2021-12-31:22`** (cited, gold #2, gold #3)

````text
Family Metrics
for some products compared to others. For example, as a result of limited visibility into encrypted products, we have fewer data signals from WhatsApp user accounts and primarily rely on phone numbers and device information to match WhatsApp user accounts with accounts on our other products. Similarly, although Messenger Kids users are included in our Family metrics, we do not seek to match their accounts with accounts on our other applications for purposes of calculating DAP and MAP. Any loss of access to data signals we use in our process for calculating Family metrics, whether as a result of our own product decisions, actions by third-party browser or mobile platforms, regulatory or legislative requirements, limitations while our personnel work remotely during the COVID-19 pandemic, or other factors, also may impact the stability or accuracy of our reported Family metrics, as well as our ability to report these metrics at all. Our estimates of Family metrics also may change as our methodologies evolve, including through the application of new data signals or technologies, product changes, or other improvements in our user surveys, algorithms, or machine learning that may improve our ability to match accounts within and across our products or otherwise
````

**#9 `META_FY2021_2021-12-31:135`** (cited, gold #2, gold #3)

````text
Item 1A.Risk Factors > Real or perceived inaccuracies in our community and other metrics may harm our reputation and negatively affect our business.
signals from WhatsApp user accounts and primarily rely on phone numbers and device information to match WhatsApp user accounts with accounts on our other products. Similarly, although Messenger Kids users are included in our Family metrics, we do not seek to match their accounts with accounts on our other applications for purposes of calculating DAP and MAP. Any loss of access to data signals we use in our process for calculating Family metrics, whether as a result of our own product decisions, actions by third-party browser or mobile platforms, regulatory or legislative requirements, limitations while our personnel work remotely during the COVID-19 pandemic, or other factors, also may impact the stability or accuracy of our reported Family metrics, as well as our ability to report these metrics at all. Our estimates of Family metrics also may change as our methodologies evolve, including through the application of new data signals or technologies, product changes, or other improvements in our user surveys, algorithms, or machine learning that may improve our ability to match accounts within and across our products or otherwise evaluate the broad population of our users. In addition, such evolution may allow us to identify previously undetected violating accounts (as
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 1A')] gold=[(None, 'Item 1A')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 7, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| Meta justifies its methodology for calculating Family metrics by stating that many people use more than one of its products and some people have multiple accounts within a single product, so counting total user accounts would not reflect the actual size of its community; instead, Family metrics are intended to estimate the number of unique people using at least one of Facebook, Instagram, Messenger, and WhatsApp. [META FY2021, 10-K, META_FY2021_2021-12-31:19] [META FY2021, Item 1A, META_FY2021_2021-12-31:131] [META FY2021, 10-K, META_FY2021_2021-12-31:17] | supported | The cited text states that multiple accounts across and within products would not reflect actual community size and that Family metrics estimate unique people using at least one listed product. |
| The company says it does not require people to use a common identifier or link their accounts across products, so it uses complex techniques, algorithms, and machine learning models to attribute multiple accounts within and across products to individual people and count those grouped accounts as one person. [META FY2021, 10-K, META_FY2021_2021-12-31:19] | supported | The evidence explicitly says Meta does not require common identifiers and uses complex techniques, algorithms, and machine learning to match accounts and count them as one person. |
| Meta also says these estimates are based on internal company data from user account activity and are meant to better reflect the size of its community and the fact that many people use more than one of its products. [META FY2021, 10-K, META_FY2021_2021-12-31:17] | supported | The cited passage says key metrics use internal company data based on user account activity and that Family metrics better reflect community size and multi-product usage. |
| To build these estimates, Meta says it uses machine learning models developed from internal reviews of limited samples of user accounts and calibrated against user survey data, applying significant judgment and using signals such as similar device information, IP addresses, and user names to match accounts. [META FY2021, 10-K, META_FY2021_2021-12-31:21] | supported | The evidence directly describes machine learning models based on internal reviews and survey calibration, significant judgment, and signals like device information, IP addresses, and user names. |
| Meta further notes that these methodologies require significant judgment and are subject to data limitations, statistical variances, algorithm or other technical errors, and changes from methodology improvements or recalibrations over time. [META FY2021, 10-K, META_FY2021_2021-12-31:21] [META FY2021, 10-K, META_FY2021_2021-12-31:19] [META FY2021, 10-K, META_FY2021_2021-12-31:18] | supported | The cited passages state the methodologies require significant judgment and are subject to data limitations, statistical variances, technical errors, and changes from methodology improvements. |
| Regarding WhatsApp, Meta cites limited visibility into encrypted products, which means it has fewer data signals from WhatsApp user accounts and primarily relies on phone numbers and device information to match WhatsApp accounts with accounts on its other products. [META FY2021, 10-K, META_FY2021_2021-12-31:22] [META FY2021, Item 1A, META_FY2021_2021-12-31:135] | supported | The evidence explicitly says limited visibility into encrypted products leaves fewer WhatsApp data signals and that Meta primarily relies on phone numbers and device information for matching. |
| Regarding Messenger Kids, Meta says those users are included in Family metrics, but it does not seek to match their accounts with accounts on its other applications for purposes of calculating DAP and MAP. [META FY2021, 10-K, META_FY2021_2021-12-31:22] [META FY2021, Item 1A, META_FY2021_2021-12-31:135] | supported | The cited text directly states Messenger Kids users are included in Family metrics but are not matched with accounts on other applications for DAP and MAP. |

</details>
