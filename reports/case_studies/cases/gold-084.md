# gold-084: Cross-year text

[← all cases](../README.md) · company: Meta Platforms, Inc. (META) · fiscal year: 2023 · recipe `cross_year_text` · hop `multi` · answer type `qualitative` · scope `cross_year` · RQ2 category `multi_company_comparison`

## Gold QA

**Question**

> How did Meta Platforms' accounting policy for recognizing credit losses on available-for-sale debt securities change between its fiscal year 2019 and fiscal year 2023 10-K filings?

**Gold answer**

> In its fiscal year 2019 10-K, Meta indicated that unrealized losses were charged against interest and other income, net, only when a decline in fair value was determined to be other-than-temporary, and noted that no such impairment charges had been recorded. In its fiscal year 2023 10-K, the policy evolved to align with newer accounting standards, where allowance for credit losses on AFS debt securities are recognized as a charge in interest and other income (expense), net, based on an assessment of expected credit losses, with any remaining unrealized losses included in accumulated other comprehensive income.

**Key points** (RQ3 keypoint_recall targets)

1. The 2019 policy required an 'other-than-temporary' impairment determination before charging losses to income.
2. The 2023 policy recognizes allowances for expected credit losses directly in interest and other income.
3. The 2023 policy separates credit losses (P&L) from remaining unrealized losses (Equity/AOCI).

**Gold evidence**

1. `META_FY2019_2019-12-31` · Item 8. Financial Statements and Supplementary Data › Cash and Cash Equivalents, Marketable Securities, and Restricted Cash · text

   > Unrealized losses are charged against interest and other income, net when a decline in fair value is determined to be other-than-temporary.

2. `META_FY2023_2023-12-31` · Item 8.Financial Statements and Supplementary Data › Cash and Cash Equivalents, Marketable Securities, and Restricted Cash · text

   > Allowance for credit losses on AFS debt securities are recognized as a charge in interest and other income (expense), net on our consolidated statements of income, and any remaining unrealized losses, net of taxes, are included in accumulated other comprehensive income (loss) in stockholders' equity.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 12 | 8 |
| recall@5 | 0.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 0.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 0 | 1 | 1 | 1 |
| average precision (lexical) | 0.00 | 1.00 | 0.29 | 0.33 |
| gold evidence first rank | #1: –, #2: – | #1: 1, #2: 1 | #1: 3, #2: 3 | #1: 3, #2: 3 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✗ | ✗ | ✓ | ✓ |
| keypoint_recall | 0.00 | 0.00 | 1.00 | 0.67 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | – | – | 1.00 | 1.00 |
| citation recall | – | – | 1.00 | 1.00 |
| citation F1 | – | – | 1.00 | 1.00 |
| has a citation | 0 | 0 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 1 |
| tokens | 1507 | 1019 | 15837 | 7473 |
| cost (USD) | 0.0002 | 0.0002 | 0.0673 | 0.0326 |
| latency (s) | 1.5 | 7.8 | 38.9 | 17.2 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2023_2023-12-31:611` | Item 9 |  |  | None. |
| 2 | `META_FY2019_2019-12-31:474` | Item 9 |  |  | None. |
| 3 | `META_FY2023_2023-12-31:488` | Item 8 › Credit Risk and Concentration |  |  | We perform ongoing credit evaluations of our customers and generally do not require collateral. We maintain an allowance for estimated credit losses, and bad debt expense on these losses was not material during the years… |
| 4 | `META_FY2019_2019-12-31:385` | Item 8 › Credit Risk and Concentration |  |  | We perform ongoing credit evaluations of our customers and generally do not require collateral. We maintain an allowance for estimated credit losses. Bad debt expense was not material during the years ended December 31, … |
| 5 | `META_FY2023_2023-12-31:377` | Item 7 › Interest and other income (expense), net |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2023 \| 2022 \| 2021 \| 2023 vs 2022 % change \| 2022 vs 2021 % change \| \| \| (in millions, except percentages) \| \| \| \| \| \| Interest income \| $1,639 \| $461 \|… |
| 6 | `META_FY2019_2019-12-31:262` | Item 7 › Interest and other income, net |  |  | \| \| Year Ended December 31, \| \| \| \| \| \|---\|---\|---\|---\|---\|---\| \| \| 2019 \| 2018 \| 2017 \| 2019 vs 2018 % Change \| 2018 vs 2017 % Change \| \| \| (in millions) \| \| \| \| \| \| Interest income, net \| $904 \| $652 \| $392 \| 39% \| 66%… |
| 7 | `META_FY2023_2023-12-31:399` | Item 7 › Recently Issued Accounting Pronouncements |  |  | For information on recently issued accounting pronouncements, see Note 1 — Summary of Significant Accounting Policies in the accompanying notes to the consolidated financial statements included in Part II, Item 8, "Finan… |
| 8 | `META_FY2023_2023-12-31:3` | (Exact name of registrant as specified in its charter) |  |  | __________________________ |
| 9 | `META_FY2023_2023-12-31:623` | Item 15 |  |  | We have filed the following documents as part of this Form 10-K: 1. Consolidated Financial Statements: |
| 10 | `META_FY2019_2019-12-31:276` | Item 7 › Quarterly Results of Operations Data |  |  | \| \| Three Months Ended \| \| \| \| \| \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| \| Dec 31, 2019 \| Sep 30, 2019 \| Jun 30, 2019 \| Mar 31, 2019 \| Dec 31, 2018 \| Sep 30, 2018 \| Jun 30, 2018 \| Mar 31, 2018 \| \| \| (in millions, e… |

RQ2 citation match (section level): `no citations`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 0.

**Generated answer**

> Not found in the provided context.

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2023_2023-12-31:464` | Item 8 › Cash and Cash Equivalents, Marketable Securities, and Restricted Cash |  | #1, #2 | We hold investments in marketable securities, consisting of U.S. government securities, U.S. government agency securities, and investment grade corporate debt securities. We classify our marketable securities as availabl… |
| 2 | `META_FY2023_2023-12-31:627` | Item 15 |  |  | \| Exhibit \| \| Incorporated by Reference \| \| \| Filed Herewith \| \|---\|---\|---\|---\|---\|---\| \| 4.5 \| Second Supplemental Indenture, dated as of May 3, 2023, by and between Meta Platforms, Inc. and U.S. Bank Trust Company, Na… |
| 3 | `META_FY2023_2023-12-31:571` | Item 8 › Legal and Related Matters |  |  | On March 8, 2022, a putative class action was filed in the U.S. District Court for the Northern District of California against us and certain of our directors and officers alleging violations of securities laws in connec… |
| 4 | `META_FY2023_2023-12-31:1` | FORM 10-K |  |  | __________________________ (Mark One) |
| 5 | `META_FY2023_2023-12-31:514` | Item 8 › Unrealized Losses |  |  | The following tables summarize our available-for-sale marketable debt securities and cash equivalents with unrealized losses as of December 31, 2023 and 2022, aggregated by major security type and the length of time that… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2023_2023-12-31:464`** (gold #1, gold #2)

````text
Item 8.Financial Statements and Supplementary Data > Cash and Cash Equivalents, Marketable Securities, and Restricted Cash
We hold investments in marketable securities, consisting of U.S. government securities, U.S. government agency securities, and investment grade corporate debt securities. We classify our marketable securities as available-for-sale (AFS) investments in our current assets because they represent investments of cash available for current operations. Our AFS investments are carried at estimated fair value with any unrealized gains and losses, net of taxes, included in accumulated other comprehensive income (loss) in stockholders' equity. AFS debt securities with an amortized cost basis in excess of estimated fair value are assessed to determine what amount of that difference, if any, is caused by expected credit losses. Allowance for credit losses on AFS debt securities are recognized as a charge in interest and other income (expense), net on our consolidated statements of income, and any remaining unrealized losses, net of taxes, are included in accumulated other comprehensive income (loss) in stockholders' equity. The amounts of credit losses recorded for the years ended December 31, 2023, 2022, and 2021 were not material. We determine realized gains or losses on sale of marketable securities on a specific
````

</details>

RQ2 citation match (section level): `no citations`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 12, cited: 3.

**Generated answer**

> In Meta Platforms’ fiscal year 2019 10-K, unrealized losses on available-for-sale investments were charged against interest and other income, net when a decline in fair value was determined to be other-than-temporary, and the company stated it had not recorded any such impairment charge in the periods presented. [META FY2019, Item 8, META_FY2019_2019-12-31:365]
>
> The fiscal year 2019 10-K also disclosed that ASU 2016-13 would be adopted effective January 1, 2020, replacing the existing incurred loss impairment model with a forward-looking expected credit loss model that requires the measurement and recognition of expected credit losses for financial assets held at amortized cost. [META FY2019, Item 8, META_FY2019_2019-12-31:390]
>
> By Meta Platforms’ fiscal year 2023 10-K, available-for-sale debt securities with an amortized cost basis in excess of estimated fair value were assessed to determine what amount of that difference, if any, was caused by expected credit losses. [META FY2023, Item 8, META_FY2023_2023-12-31:464]
>
> In the fiscal year 2023 10-K, allowance for credit losses on available-for-sale debt securities was recognized as a charge in interest and other income (expense), net on the consolidated statements of income, and any remaining unrealized losses, net of taxes, were included in accumulated other comprehensive income (loss) in stockholders’ equity. [META FY2023, Item 8, META_FY2023_2023-12-31:464]
>
> So, the policy changed from an other-than-temporary impairment approach in 2019 to an expected credit loss approach with an allowance for credit losses on available-for-sale debt securities by 2023. [META FY2023, Item 8, META_FY2023_2023-12-31:464] [META FY2019, Item 8, META_FY2019_2019-12-31:390] [META FY2019, Item 8, META_FY2019_2019-12-31:365]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2023_2023-12-31:407` | Item 7A › Equity Price Risk |  |  | For additional information, see Note 1 — Summary of Significant Accounting Policies, Note 5 — Financial Instruments, Note 6 — Non-marketable Equity Securities, and Note 10 — Long-term Debt in the notes to the consolidate… |
| 2 | `META_FY2023_2023-12-31:488` | Item 8 › Credit Risk and Concentration |  |  | We perform ongoing credit evaluations of our customers and generally do not require collateral. We maintain an allowance for estimated credit losses, and bad debt expense on these losses was not material during the years… |
| 3 | `META_FY2023_2023-12-31:464` | Item 8 › Cash and Cash Equivalents, Marketable Securities, and Restricted Cash | ✓ | #1, #2 | We hold investments in marketable securities, consisting of U.S. government securities, U.S. government agency securities, and investment grade corporate debt securities. We classify our marketable securities as availabl… |
| 4 | `META_FY2019_2019-12-31:390` | Item 8 › Recent Accounting Pronouncements Not Yet Adopted | ✓ |  | In June 2016, the Financial Accounting Standards Board (FASB) issued Accounting Standard Update No. 2016-13, Financial Instruments-Credit Losses (Topic 326): Measurement of Credit Losses on Financial Instruments (ASU 201… |
| 5 | `META_FY2019_2019-12-31:385` | Item 8 › Credit Risk and Concentration |  |  | We perform ongoing credit evaluations of our customers and generally do not require collateral. We maintain an allowance for estimated credit losses. Bad debt expense was not material during the years ended December 31, … |
| 6 | `META_FY2023_2023-12-31:399` | Item 7 › Recently Issued Accounting Pronouncements |  |  | For information on recently issued accounting pronouncements, see Note 1 — Summary of Significant Accounting Policies in the accompanying notes to the consolidated financial statements included in Part II, Item 8, "Finan… |
| 7 | `META_FY2023_2023-12-31:514` | Item 8 › Unrealized Losses |  |  | The following tables summarize our available-for-sale marketable debt securities and cash equivalents with unrealized losses as of December 31, 2023 and 2022, aggregated by major security type and the length of time that… |
| 8 | `META_FY2019_2019-12-31:365` | Item 8 › Cash and Cash Equivalents, Marketable Securities, and Restricted Cash | ✓ | #1, #2 | Cash and cash equivalents consist of cash on deposit with banks and highly liquid investments with maturities of 90 days or less from the date of purchase. We hold investments in marketable securities, consisting of U.S.… |
| 9 | `META_FY2023_2023-12-31:487` | Item 8 › Credit Risk and Concentration |  |  | Our financial instruments that are potentially subject to concentrations of credit risk consist primarily of cash, cash equivalents, restricted cash, marketable securities, and accounts receivable. Cash equivalents consi… |
| 10 | `META_FY2023_2023-12-31:517` | Item 8 › Unrealized Losses |  |  | The decrease in the gross unrealized losses for the year ended December 31, 2023 is mostly due to a shorter average portfolio duration. The allowance for credit losses and the gross unrealized gains on our marketable deb… |
| 11 | `META_FY2023_2023-12-31:470` | Item 8 › Accounts Receivable and Allowances |  |  | Accounts receivable are recorded and carried at the original invoiced amount less an allowance for any potential uncollectible amounts. We make estimates of expected credit and collectibility trends for the allowance for… |
| 12 | `META_FY2019_2019-12-31:405` | Item 8 › Note 4.Cash and Cash Equivalents and Marketable Securities |  |  | The gross unrealized gains on our marketable securities were $205 million and $24 million as of December 31, 2019 and 2018, respectively. The gross unrealized losses on our marketable securities were $24 million and $357… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `META_FY2023_2023-12-31:464`** (cited, gold #1, gold #2)

````text
Item 8.Financial Statements and Supplementary Data > Cash and Cash Equivalents, Marketable Securities, and Restricted Cash
We hold investments in marketable securities, consisting of U.S. government securities, U.S. government agency securities, and investment grade corporate debt securities. We classify our marketable securities as available-for-sale (AFS) investments in our current assets because they represent investments of cash available for current operations. Our AFS investments are carried at estimated fair value with any unrealized gains and losses, net of taxes, included in accumulated other comprehensive income (loss) in stockholders' equity. AFS debt securities with an amortized cost basis in excess of estimated fair value are assessed to determine what amount of that difference, if any, is caused by expected credit losses. Allowance for credit losses on AFS debt securities are recognized as a charge in interest and other income (expense), net on our consolidated statements of income, and any remaining unrealized losses, net of taxes, are included in accumulated other comprehensive income (loss) in stockholders' equity. The amounts of credit losses recorded for the years ended December 31, 2023, 2022, and 2021 were not material. We determine realized gains or losses on sale of marketable securities on a specific
````

**#4 `META_FY2019_2019-12-31:390`** (cited)

````text
Item 8. Financial Statements and Supplementary Data > Recent Accounting Pronouncements Not Yet Adopted
In June 2016, the Financial Accounting Standards Board (FASB) issued Accounting Standard Update No. 2016-13, Financial Instruments-Credit Losses (Topic 326): Measurement of Credit Losses on Financial Instruments (ASU 2016-13), which requires the measurement and recognition of expected credit losses for financial assets held at amortized cost. ASU 2016-13 replaces the existing incurred loss impairment model with a forward-looking expected credit loss model which will result in earlier recognition of credit losses. We will adopt the new standard effective January 1, 2020 and do not expect the adoption of this guidance to have a material impact on our consolidated financial statements. In August 2018, the FASB issued Accounting Standard Update No. 2018-13, Changes to Disclosure Requirements for Fair Value Measurements (Topic 820) (ASU 2018-13), which improved the effectiveness of disclosure requirements for recurring and nonrecurring fair value measurements. The standard removes, modifies, and adds certain disclosure requirements. We will adopt the new standard effective January 1, 2020 and do not expect the adoption of this guidance to have a material impact on our consolidated financial statements.
````

**#8 `META_FY2019_2019-12-31:365`** (cited, gold #1, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Cash and Cash Equivalents, Marketable Securities, and Restricted Cash
Cash and cash equivalents consist of cash on deposit with banks and highly liquid investments with maturities of 90 days or less from the date of purchase. We hold investments in marketable securities, consisting of U.S. government securities, U.S. government agency securities, and investment grade corporate debt securities. We classify our marketable securities as available-for-sale investments in our current assets because they represent investments of cash available for current operations. Our available-for-sale investments are carried at estimated fair value with any unrealized gains and losses, net of taxes, included in accumulated other comprehensive income (loss) in stockholders' equity. Unrealized losses are charged against interest and other income, net when a decline in fair value is determined to be other-than-temporary. We have not recorded any such impairment charge in the periods presented. We determine realized gains or losses on sale of marketable securities on a specific identification method, and record such gains or losses as interest and other income, net.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 5, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In Meta Platforms’ fiscal year 2019 10-K, unrealized losses on available-for-sale investments were charged against interest and other income, net when a decline in fair value was determined to be other-than-temporary, and the company stated it had not recorded any such impairment charge in the periods presented. [META FY2019, Item 8, META_FY2019_2019-12-31:365] | supported | The cited 2019 note states both the other-than-temporary impairment treatment and that no such impairment charge was recorded. |
| The fiscal year 2019 10-K also disclosed that ASU 2016-13 would be adopted effective January 1, 2020, replacing the existing incurred loss impairment model with a forward-looking expected credit loss model that requires the measurement and recognition of expected credit losses for financial assets held at amortized cost. [META FY2019, Item 8, META_FY2019_2019-12-31:390] | supported | The cited 2019 pronouncements note says ASU 2016-13 would be adopted on January 1, 2020 and describes the expected credit loss model replacing the incurred loss model. |
| By Meta Platforms’ fiscal year 2023 10-K, available-for-sale debt securities with an amortized cost basis in excess of estimated fair value were assessed to determine what amount of that difference, if any, was caused by expected credit losses. [META FY2023, Item 8, META_FY2023_2023-12-31:464] | supported | The cited 2023 note explicitly says AFS debt securities with amortized cost above fair value are assessed for the portion caused by expected credit losses. |
| In the fiscal year 2023 10-K, allowance for credit losses on available-for-sale debt securities was recognized as a charge in interest and other income (expense), net on the consolidated statements of income, and any remaining unrealized losses, net of taxes, were included in accumulated other comprehensive income (loss) in stockholders’ equity. [META FY2023, Item 8, META_FY2023_2023-12-31:464] | supported | The cited 2023 note expressly states the allowance charge goes to interest and other income (expense), net and remaining unrealized losses go to AOCI. |
| So, the policy changed from an other-than-temporary impairment approach in 2019 to an expected credit loss approach with an allowance for credit losses on available-for-sale debt securities by 2023. [META FY2023, Item 8, META_FY2023_2023-12-31:464] [META FY2019, Item 8, META_FY2019_2019-12-31:390] [META FY2019, Item 8, META_FY2019_2019-12-31:365] | supported | The 2019 evidence shows an other-than-temporary impairment approach, while the 2023 evidence shows an expected credit loss allowance approach for AFS debt securities. |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 8, cited: 2.

**Generated answer**

> In the FY2019 10-K, Meta disclosed that ASU 2016-13 would be adopted effective January 1, 2020 and that it “requires the measurement and recognition of expected credit losses for financial assets held at amortized cost” and “replaces the existing incurred loss impairment model with a forward-looking expected credit loss model which will result in earlier recognition of credit losses.” [META FY2019, Item 8, META_FY2019_2019-12-31:390]
>
> In the FY2023 10-K, Meta stated that available-for-sale debt securities with an amortized cost basis in excess of estimated fair value are assessed to determine what amount of that difference, if any, is caused by expected credit losses. [META FY2023, Item 8, META_FY2023_2023-12-31:464]
>
> In the FY2023 10-K, Meta also stated that allowance for credit losses on available-for-sale debt securities are recognized as a charge in interest and other income (expense), net, and any remaining unrealized losses, net of taxes, are included in accumulated other comprehensive income (loss) in stockholders’ equity. [META FY2023, Item 8, META_FY2023_2023-12-31:464]
>
> So, between FY2019 and FY2023, the disclosure moved from a pre-adoption statement that the company would shift from an incurred loss model to a forward-looking expected credit loss model, to a post-adoption policy that specifically applies expected credit loss assessment to available-for-sale debt securities and records the credit-loss allowance through earnings while other unrealized losses remain in equity. [META FY2019, Item 8, META_FY2019_2019-12-31:390] [META FY2023, Item 8, META_FY2023_2023-12-31:464]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `F-META-2019` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2019,2019-12-31,70697000000,18485000000,23986000000,1333760000… |
| 2 | `F-META-2023` | SEC XBRL Reported Financials (financials.csv) |  |  | fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted 2023,2023-12-31,134902000000,39098000000,46751000000,229623000… |
| 3 | `META_FY2023_2023-12-31:464` | Item 8 › Cash and Cash Equivalents, Marketable Securities, and Restricted Cash | ✓ | #1, #2 | We hold investments in marketable securities, consisting of U.S. government securities, U.S. government agency securities, and investment grade corporate debt securities. We classify our marketable securities as availabl… |
| 4 | `META_FY2023_2023-12-31:488` | Item 8 › Credit Risk and Concentration |  |  | We perform ongoing credit evaluations of our customers and generally do not require collateral. We maintain an allowance for estimated credit losses, and bad debt expense on these losses was not material during the years… |
| 5 | `META_FY2019_2019-12-31:390` | Item 8 › Recent Accounting Pronouncements Not Yet Adopted | ✓ |  | In June 2016, the Financial Accounting Standards Board (FASB) issued Accounting Standard Update No. 2016-13, Financial Instruments-Credit Losses (Topic 326): Measurement of Credit Losses on Financial Instruments (ASU 201… |
| 6 | `META_FY2019_2019-12-31:385` | Item 8 › Credit Risk and Concentration |  |  | We perform ongoing credit evaluations of our customers and generally do not require collateral. We maintain an allowance for estimated credit losses. Bad debt expense was not material during the years ended December 31, … |
| 7 | `META_FY2023_2023-12-31:407` | Item 7A › Equity Price Risk |  |  | For additional information, see Note 1 — Summary of Significant Accounting Policies, Note 5 — Financial Instruments, Note 6 — Non-marketable Equity Securities, and Note 10 — Long-term Debt in the notes to the consolidate… |
| 8 | `META_FY2023_2023-12-31:514` | Item 8 › Unrealized Losses |  |  | The following tables summarize our available-for-sale marketable debt securities and cash equivalents with unrealized losses as of December 31, 2023 and 2022, aggregated by major security type and the length of time that… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#3 `META_FY2023_2023-12-31:464`** (cited, gold #1, gold #2)

````text
Item 8.Financial Statements and Supplementary Data > Cash and Cash Equivalents, Marketable Securities, and Restricted Cash
We hold investments in marketable securities, consisting of U.S. government securities, U.S. government agency securities, and investment grade corporate debt securities. We classify our marketable securities as available-for-sale (AFS) investments in our current assets because they represent investments of cash available for current operations. Our AFS investments are carried at estimated fair value with any unrealized gains and losses, net of taxes, included in accumulated other comprehensive income (loss) in stockholders' equity. AFS debt securities with an amortized cost basis in excess of estimated fair value are assessed to determine what amount of that difference, if any, is caused by expected credit losses. Allowance for credit losses on AFS debt securities are recognized as a charge in interest and other income (expense), net on our consolidated statements of income, and any remaining unrealized losses, net of taxes, are included in accumulated other comprehensive income (loss) in stockholders' equity. The amounts of credit losses recorded for the years ended December 31, 2023, 2022, and 2021 were not material. We determine realized gains or losses on sale of marketable securities on a specific
````

**#5 `META_FY2019_2019-12-31:390`** (cited)

````text
Item 8. Financial Statements and Supplementary Data > Recent Accounting Pronouncements Not Yet Adopted
In June 2016, the Financial Accounting Standards Board (FASB) issued Accounting Standard Update No. 2016-13, Financial Instruments-Credit Losses (Topic 326): Measurement of Credit Losses on Financial Instruments (ASU 2016-13), which requires the measurement and recognition of expected credit losses for financial assets held at amortized cost. ASU 2016-13 replaces the existing incurred loss impairment model with a forward-looking expected credit loss model which will result in earlier recognition of credit losses. We will adopt the new standard effective January 1, 2020 and do not expect the adoption of this guidance to have a material impact on our consolidated financial statements. In August 2018, the FASB issued Accounting Standard Update No. 2018-13, Changes to Disclosure Requirements for Fair Value Measurements (Topic 820) (ASU 2018-13), which improved the effectiveness of disclosure requirements for recurring and nonrecurring fair value measurements. The standard removes, modifies, and adds certain disclosure requirements. We will adopt the new standard effective January 1, 2020 and do not expect the adoption of this guidance to have a material impact on our consolidated financial statements.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 0, verified 0, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 4, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In the FY2019 10-K, Meta disclosed that ASU 2016-13 would be adopted effective January 1, 2020 and that it “requires the measurement and recognition of expected credit losses for financial assets held at amortized cost” and “replaces the existing incurred loss impairment model with a forward-looking expected credit loss model which will result in earlier recognition of credit losses.” [META FY2019, Item 8, META_FY2019_2019-12-31:390] | supported | The cited FY2019 text states the January 1, 2020 adoption date and quotes both described ASU 2016-13 provisions. |
| In the FY2023 10-K, Meta stated that available-for-sale debt securities with an amortized cost basis in excess of estimated fair value are assessed to determine what amount of that difference, if any, is caused by expected credit losses. [META FY2023, Item 8, META_FY2023_2023-12-31:464] | supported | The cited FY2023 text explicitly says AFS debt securities with amortized cost above fair value are assessed for expected credit losses. |
| In the FY2023 10-K, Meta also stated that allowance for credit losses on available-for-sale debt securities are recognized as a charge in interest and other income (expense), net, and any remaining unrealized losses, net of taxes, are included in accumulated other comprehensive income (loss) in stockholders’ equity. [META FY2023, Item 8, META_FY2023_2023-12-31:464] | supported | The cited FY2023 text expressly states the allowance is charged to interest and other income (expense), net, while remaining unrealized losses go to AOCI in equity. |
| So, between FY2019 and FY2023, the disclosure moved from a pre-adoption statement that the company would shift from an incurred loss model to a forward-looking expected credit loss model, to a post-adoption policy that specifically applies expected credit loss assessment to available-for-sale debt securities and records the credit-loss allowance through earnings while other unrealized losses remain in equity. [META FY2019, Item 8, META_FY2019_2019-12-31:390] [META FY2023, Item 8, META_FY2023_2023-12-31:464] | supported | The FY2019 evidence shows a pre-adoption shift to an expected credit loss model, and the FY2023 evidence shows the post-adoption AFS policy with credit-loss allowance through earnings and other unrealized losses in equity. |

</details>
