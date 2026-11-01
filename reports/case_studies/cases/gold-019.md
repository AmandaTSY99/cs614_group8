# gold-019: Multi-hop text (one filing)

[← all cases](../README.md) · company: Meta Platforms, Inc. (META) · fiscal year: 2016 · recipe `text` · hop `multi` · answer type `qualitative` · scope `single_doc` · RQ2 category `cross_section_multihop`

## Gold QA

**Question**

> How did Meta Platforms' accounting policy for share-based compensation forfeitures change in Q4 2016, and how does this interact with the standard vesting period for its awards?

**Gold answer**

> In Q4 2016, Meta early adopted ASU 2016-09 and elected to account for forfeitures as they occur, rather than estimating them. Expense is recognized straight-line over the service period, which is four years for the majority of awards, so under the new policy expense accrues over that period and is reduced only when forfeitures actually occur.

**Key points** (RQ3 keypoint_recall targets)

1. Meta early adopted ASU 2016-09 in Q4 2016
2. The policy change involved accounting for forfeitures as they occur instead of estimating them
3. The majority of awards have a four-year service period

**Gold evidence**

1. `META_FY2016_2016-12-31` · Item 8. Financial Statements and Supplementary Data › Share-based Compensation · text

   > In the fourth quarter of 2016, we elected to early adopt Accounting Standards Update No. 2016-09, Compensation-Stock Compensation (Topic 718): Improvement to Employee Share-based Payment Accounting (ASU 2016-09) issued by the Financial Accounting Standards Board (FASB), which among other items, provides an accounting policy election to account for forfeitures as they occur, rather than to account for them based on an estimate of expected forfeitures.

2. `META_FY2016_2016-12-31` · Item 8. Financial Statements and Supplementary Data › Share-based Compensation · text

   > The majority of our awards are earned over a service period of four years.

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 12 | 13 |
| recall@5 | 0.50 | 0.50 | 0.50 | 0.50 |
| recall@all | 1.00 | 0.50 | 1.00 | 1.00 |
| complete@all | 1 | 0 | 1 | 1 |
| average precision (lexical) | 0.80 | 0.87 | 0.85 | 0.85 |
| gold evidence first rank | #1: 1, #2: 7 | #1: 1, #2: – | #1: 1, #2: 8 | #1: 1, #2: 8 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | 1.00 | 0.67 | 1.00 | 1.00 |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | – | – | – | – |
| citation precision | 0.50 | 0.50 | 0.50 | 0.50 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 0.67 | 0.67 | 0.67 | 0.67 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 3 | 3 |
| tokens | 2387 | 1391 | 23733 | 14877 |
| cost (USD) | 0.0004 | 0.0003 | 0.0890 | 0.0578 |
| latency (s) | 3.4 | 7.2 | 36.0 | 29.2 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 3.

**Generated answer**

> In Q4 2016, Meta early adopted ASU 2016-09 and changed its policy for share-based compensation forfeitures from estimating expected forfeitures to recognizing forfeitures as they occur. As a result, 2016 share-based compensation expense was calculated based on actual forfeitures, whereas 2015 and 2014 had been recorded net of estimated forfeitures [1][2].
>
> This interacts with vesting because Meta recognizes share-based compensation expense over the employee service period, generally on a straight-line basis, and the majority of its awards are earned over a four-year service period [9]. So after the policy change, expense continues to be recognized over that service/vesting period, but forfeitures are now reflected when they actually happen rather than being estimated in advance [1][2][9].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2016_2016-12-31:194` | Item 7 › Share-based Compensation | ✓ | #1 | We elected to early adopt ASU 2016-09 in the fourth quarter of 2016, which among other items, provides an accounting policy election to account for forfeitures as they occur, rather than to account for them based on an e… |
| 2 | `META_FY2016_2016-12-31:315` | Item 8 › Share-based Compensation | ✓ | #1 | In the fourth quarter of 2016, we elected to early adopt Accounting Standards Update No. 2016-09, Compensation-Stock Compensation (Topic 718): Improvement to Employee Share-based Payment Accounting (ASU 2016-09) issued b… |
| 3 | `META_FY2016_2016-12-31:409` | Item 8 › Share-based Compensation Plans |  |  | (1) Due to the adoption of ASU 2016-09, excess tax benefits from share-based award activity for the year ended December 31, 2016 are reflected as a reduction of the provision for income taxes, whereas they previously wer… |
| 4 | `META_FY2016_2016-12-31:169` | Item 6 |  | #1 | (1) In the fourth quarter of 2016, we elected to early adopt Accounting Standards Update No. 2016-09, Compensation-Stock Compensation (Topic 718): Improvement to Employee Share-based Payment Accounting (ASU 2016-09) whic… |
| 5 | `META_FY2016_2016-12-31:338` | Item 8 › Accounting Pronouncements Adopted in 2016 |  |  | In March 2016, the FASB issued ASU 2016-09 to simplify certain aspects of the accounting for share-based payment transactions to employees. The new standard requires excess tax benefits and tax deficiencies to be recorde… |
| 6 | `META_FY2016_2016-12-31:339` | Item 8 › Accounting Pronouncements Adopted in 2016 |  | #1 | We elected to early adopt the new guidance in the fourth quarter of 2016 which required us to reflect any adjustments as of January 1, 2016, the beginning of the annual period that includes the interim period of adoption… |
| 7 | `META_FY2016_2016-12-31:401` | Item 8 › Share-based Compensation Plans |  | #2 | (1) Unvested shares include inducement awards issued in connection with an acquisition in 2014 and are subject to the terms, restrictions, and conditions of separate non-plan RSU award agreements. The fair value as of th… |
| 8 | `META_FY2016_2016-12-31:400` | Item 8 › Share-based Compensation Plans |  |  | \| \| Unvested RSUs(1) \| \| \|---\|---\|---\| \| \| Number of Shares \| Weighted Average Grant Date Fair Value \| \| \| (in thousands) \| \| \| Unvested at December 31, 2015 \| 116,409 \| $65.95 \| \| Granted \| 30,414 \| 113.43 \| \| Vested \| … |
| 9 | `META_FY2016_2016-12-31:314` | Item 8 › Share-based Compensation | ✓ | #2 | We account for share-based employee compensation plans under the fair value recognition and measurement provisions of GAAP. Those provisions require all share-based payments to employees, including grants of stock option… |
| 10 | `META_FY2016_2016-12-31:340` | Item 8 › Accounting Pronouncements Adopted in 2016 |  |  | We adopted the aspects of the standard affecting the cash flow presentation retrospectively, and accordingly, to conform to the current year presentation, we reclassified $1.72 billion and $1.87 billion of excess tax ben… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2016_2016-12-31:194`** (cited, gold #1)

````text
Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations > Share-based Compensation
We elected to early adopt ASU 2016-09 in the fourth quarter of 2016, which among other items, provides an accounting policy election to account for forfeitures as they occur, rather than to account for them based on an estimate of expected forfeitures. We elected to account for forfeitures as they occur and therefore, share-based compensation expense for the year ended December 31, 2016 has been calculated based on actual forfeitures in our consolidated statements of income, rather than our previous approach which was net of estimated forfeitures. The net cumulative effect of this change was recognized as a $39 million increase to paid-in capital as of January 1, 2016. Share-based compensation expense for the years ended December 31, 2015 and 2014 were recorded net of estimated forfeitures, which were based on historical forfeitures and adjusted to reflect changes in facts and circumstances, if any.
````

**#2 `META_FY2016_2016-12-31:315`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Share-based Compensation
In the fourth quarter of 2016, we elected to early adopt Accounting Standards Update No. 2016-09, Compensation-Stock Compensation (Topic 718): Improvement to Employee Share-based Payment Accounting (ASU 2016-09) issued by the Financial Accounting Standards Board (FASB), which among other items, provides an accounting policy election to account for forfeitures as they occur, rather than to account for them based on an estimate of expected forfeitures. We elected to account for forfeitures as they occur and therefore, share-based compensation expense for the year ended December 31, 2016 has been calculated based on actual forfeitures in our consolidated statements of income, rather than our previous approach which was net of estimated forfeitures. The net cumulative effect of this change increased additional paid-in capital as of January 1, 2016 by $39 million. Share-based compensation expense for the years ended December 31, 2015 and 2014 were recorded net of estimated forfeitures, which were based on historical forfeitures and adjusted to reflect changes in facts and circumstances, if any.
````

**#4 `META_FY2016_2016-12-31:169`** (gold #1)

````text
Item 6. Selected Financial Data.
(1) In the fourth quarter of 2016, we elected to early adopt Accounting Standards Update No. 2016-09, Compensation-Stock Compensation (Topic 718): Improvement to Employee Share-based Payment Accounting (ASU 2016-09) which requires us, among other items, to record excess tax benefits as a reduction of the provision for income taxes in the income statements, whereas they were previously recognized in equity. We are required to reflect any adoption adjustments as of January 1, 2016, the beginning of the annual period that includes the interim period of adoption. As such, certain consolidated statements of income data for the year ended December 31, 2016 included the impact of the ASU 2016-09 adoption. See Note 1 of the accompanying notes to our consolidated financial statements for additional information related to this adoption. (2) Total costs and expenses include $3.22 billion, $2.97 billion, $1.84 billion, $906 million, and $1.57 billion of share-based compensation for the years ended December 31, 2016, 2015, 2014, 2013, and 2012, respectively.
````

**#6 `META_FY2016_2016-12-31:339`** (gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Accounting Pronouncements Adopted in 2016
We elected to early adopt the new guidance in the fourth quarter of 2016 which required us to reflect any adjustments as of January 1, 2016, the beginning of the annual period that includes the interim period of adoption. Upon adoption, excess tax benefits or deficiencies from share-based award activity are reflected in the consolidated statements of income as a component of the provision for income taxes, whereas they previously were recognized in equity. We also elected to account for forfeitures as they occur, rather than estimate expected forfeitures. The adoption of ASU 2016-09 resulted in net cumulative-effect adjustment of $1.67 billion increase to retained earnings as of January 1, 2016, mostly related to the recognition of the previously unrecognized excess tax benefits using the modified retrospective method. The previously unrecognized excess tax effects were recorded as a reduction to tax liability or an increase to deferred tax asset.
````

**#7 `META_FY2016_2016-12-31:401`** (gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Share-based Compensation Plans
(1) Unvested shares include inducement awards issued in connection with an acquisition in 2014 and are subject to the terms, restrictions, and conditions of separate non-plan RSU award agreements. The fair value as of the respective vesting dates of RSUs that vested during the years ended December 31, 2016, 2015, and 2014 was $4.92 billion, $4.23 billion, and $2.77 billion, respectively. As of December 31, 2016, there was $7.03 billion of unrecognized share-based compensation expense, of which (i) $6.78 billion was related to RSUs, and (ii) $255 million was related to restricted shares, shares related to our contingent consideration with performance conditions that were met in the second quarter of 2016 but are still subject to service condition, and stock options. This unrecognized compensation expense is expected to be recognized over a weighted-average period of approximately three years. Note 11. Interest and other income/(expense), net The following table presents the detail of interest and other income/(expense), net, for the periods presented (in millions):
````

**#9 `META_FY2016_2016-12-31:314`** (cited, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Share-based Compensation
We account for share-based employee compensation plans under the fair value recognition and measurement provisions of GAAP. Those provisions require all share-based payments to employees, including grants of stock options and restricted stock units (RSUs), to be measured based on the grant date fair value of the awards, with the resulting expense generally recognized on a straight-line basis in our consolidated statements of income over the period during which the employee is required to perform service in exchange for the award. The majority of our awards are earned over a service period of four years.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 7'), ('META', 'Item 8')] gold=[(None, 'Item 8')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 2.

**Generated answer**

> In Q4 2016, Meta early adopted ASU 2016-09 and changed its policy for share-based compensation forfeitures from estimating expected forfeitures in advance to recognizing forfeitures only as they actually occur. As a result, 2016 share-based compensation expense was based on actual forfeitures, while 2015 and 2014 had been recorded net of estimated forfeitures. The cumulative effect of this change increased additional paid-in capital by $39 million as of January 1, 2016 [1][2].
>
> The provided context does not state the standard vesting period for Meta’s awards, so the interaction with that vesting period is not described here. [1][2]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2016_2016-12-31:194` | Item 7 › Share-based Compensation | ✓ | #1 | We elected to early adopt ASU 2016-09 in the fourth quarter of 2016, which among other items, provides an accounting policy election to account for forfeitures as they occur, rather than to account for them based on an e… |
| 2 | `META_FY2016_2016-12-31:315` | Item 8 › Share-based Compensation | ✓ | #1 | In the fourth quarter of 2016, we elected to early adopt Accounting Standards Update No. 2016-09, Compensation-Stock Compensation (Topic 718): Improvement to Employee Share-based Payment Accounting (ASU 2016-09) issued b… |
| 3 | `META_FY2016_2016-12-31:340` | Item 8 › Accounting Pronouncements Adopted in 2016 |  |  | We adopted the aspects of the standard affecting the cash flow presentation retrospectively, and accordingly, to conform to the current year presentation, we reclassified $1.72 billion and $1.87 billion of excess tax ben… |
| 4 | `META_FY2016_2016-12-31:338` | Item 8 › Accounting Pronouncements Adopted in 2016 |  |  | In March 2016, the FASB issued ASU 2016-09 to simplify certain aspects of the accounting for share-based payment transactions to employees. The new standard requires excess tax benefits and tax deficiencies to be recorde… |
| 5 | `META_FY2016_2016-12-31:339` | Item 8 › Accounting Pronouncements Adopted in 2016 |  | #1 | We elected to early adopt the new guidance in the fourth quarter of 2016 which required us to reflect any adjustments as of January 1, 2016, the beginning of the annual period that includes the interim period of adoption… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2016_2016-12-31:194`** (cited, gold #1)

````text
Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations > Share-based Compensation
We elected to early adopt ASU 2016-09 in the fourth quarter of 2016, which among other items, provides an accounting policy election to account for forfeitures as they occur, rather than to account for them based on an estimate of expected forfeitures. We elected to account for forfeitures as they occur and therefore, share-based compensation expense for the year ended December 31, 2016 has been calculated based on actual forfeitures in our consolidated statements of income, rather than our previous approach which was net of estimated forfeitures. The net cumulative effect of this change was recognized as a $39 million increase to paid-in capital as of January 1, 2016. Share-based compensation expense for the years ended December 31, 2015 and 2014 were recorded net of estimated forfeitures, which were based on historical forfeitures and adjusted to reflect changes in facts and circumstances, if any.
````

**#2 `META_FY2016_2016-12-31:315`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Share-based Compensation
In the fourth quarter of 2016, we elected to early adopt Accounting Standards Update No. 2016-09, Compensation-Stock Compensation (Topic 718): Improvement to Employee Share-based Payment Accounting (ASU 2016-09) issued by the Financial Accounting Standards Board (FASB), which among other items, provides an accounting policy election to account for forfeitures as they occur, rather than to account for them based on an estimate of expected forfeitures. We elected to account for forfeitures as they occur and therefore, share-based compensation expense for the year ended December 31, 2016 has been calculated based on actual forfeitures in our consolidated statements of income, rather than our previous approach which was net of estimated forfeitures. The net cumulative effect of this change increased additional paid-in capital as of January 1, 2016 by $39 million. Share-based compensation expense for the years ended December 31, 2015 and 2014 were recorded net of estimated forfeitures, which were based on historical forfeitures and adjusted to reflect changes in facts and circumstances, if any.
````

**#5 `META_FY2016_2016-12-31:339`** (gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Accounting Pronouncements Adopted in 2016
We elected to early adopt the new guidance in the fourth quarter of 2016 which required us to reflect any adjustments as of January 1, 2016, the beginning of the annual period that includes the interim period of adoption. Upon adoption, excess tax benefits or deficiencies from share-based award activity are reflected in the consolidated statements of income as a component of the provision for income taxes, whereas they previously were recognized in equity. We also elected to account for forfeitures as they occur, rather than estimate expected forfeitures. The adoption of ASU 2016-09 resulted in net cumulative-effect adjustment of $1.67 billion increase to retained earnings as of January 1, 2016, mostly related to the recognition of the previously unrecognized excess tax benefits using the modified retrospective method. The previously unrecognized excess tax effects were recorded as a reduction to tax liability or an increase to deferred tax asset.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 7'), ('META', 'Item 8')] gold=[(None, 'Item 8')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 12, cited: 6.

**Generated answer**

> In the fourth quarter of 2016, Meta Platforms early adopted ASU 2016-09 and changed its accounting policy for share-based compensation forfeitures from estimating expected forfeitures to accounting for forfeitures as they occur. [META FY2016, Item 8, META_FY2016_2016-12-31:315] [META FY2016, Item 7, META_FY2016_2016-12-31:194]
>
> As a result, share-based compensation expense for the year ended December 31, 2016 was calculated based on actual forfeitures, whereas for 2015 and 2014 the expense had been recorded net of estimated forfeitures based on historical forfeitures and adjusted for changes in facts and circumstances, if any. [META FY2016, Item 8, META_FY2016_2016-12-31:315] [META FY2016, Item 7, META_FY2016_2016-12-31:194]
>
> The net cumulative effect of this change increased additional paid-in capital, or paid-in capital, by $39 million as of January 1, 2016. [META FY2016, Item 8, META_FY2016_2016-12-31:315] [META FY2016, Item 7, META_FY2016_2016-12-31:194]
>
> In terms of vesting or service periods, Meta states that it recognizes compensation expense for certain unvested restricted shares on a straight-line basis over the period during which the employee is required to perform service in exchange for the award. [META FY2016, Item 7, META_FY2016_2016-12-31:195] [META FY2016, Item 8, META_FY2016_2016-12-31:316]
>
> For outstanding unrecognized share-based compensation expense as of December 31, 2016, Meta said the expense was expected to be recognized over a weighted-average period of approximately three years. [META FY2016, Item 8, META_FY2016_2016-12-31:401]
>
> Meta also disclosed that, in connection with a 2014 acquisition, it granted inducement RSU awards covering an aggregate of 37 million RSUs earned over a service period of four years. [META FY2016, Item 8, META_FY2016_2016-12-31:395]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2016_2016-12-31:315` | Item 8 › Share-based Compensation | ✓ | #1 | In the fourth quarter of 2016, we elected to early adopt Accounting Standards Update No. 2016-09, Compensation-Stock Compensation (Topic 718): Improvement to Employee Share-based Payment Accounting (ASU 2016-09) issued b… |
| 2 | `META_FY2016_2016-12-31:194` | Item 7 › Share-based Compensation | ✓ | #1 | We elected to early adopt ASU 2016-09 in the fourth quarter of 2016, which among other items, provides an accounting policy election to account for forfeitures as they occur, rather than to account for them based on an e… |
| 3 | `META_FY2016_2016-12-31:169` | Item 6 |  | #1 | (1) In the fourth quarter of 2016, we elected to early adopt Accounting Standards Update No. 2016-09, Compensation-Stock Compensation (Topic 718): Improvement to Employee Share-based Payment Accounting (ASU 2016-09) whic… |
| 4 | `META_FY2016_2016-12-31:339` | Item 8 › Accounting Pronouncements Adopted in 2016 |  | #1 | We elected to early adopt the new guidance in the fourth quarter of 2016 which required us to reflect any adjustments as of January 1, 2016, the beginning of the annual period that includes the interim period of adoption… |
| 5 | `META_FY2016_2016-12-31:409` | Item 8 › Share-based Compensation Plans |  |  | (1) Due to the adoption of ASU 2016-09, excess tax benefits from share-based award activity for the year ended December 31, 2016 are reflected as a reduction of the provision for income taxes, whereas they previously wer… |
| 6 | `META_FY2016_2016-12-31:410` | Item 8 › Share-based Compensation Plans |  |  | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2016 \| 2015 \| \| Deferred tax assets: \| \| \| \| Net operating loss carryforward \| $1,252 \| $476 \| \| Tax credit carryforward \| 268 \| 297 \| \| Share-based compensation \| 684 \| 529 \| \| Acc… |
| 7 | `META_FY2016_2016-12-31:338` | Item 8 › Accounting Pronouncements Adopted in 2016 |  |  | In March 2016, the FASB issued ASU 2016-09 to simplify certain aspects of the accounting for share-based payment transactions to employees. The new standard requires excess tax benefits and tax deficiencies to be recorde… |
| 8 | `META_FY2016_2016-12-31:401` | Item 8 › Share-based Compensation Plans | ✓ | #2 | (1) Unvested shares include inducement awards issued in connection with an acquisition in 2014 and are subject to the terms, restrictions, and conditions of separate non-plan RSU award agreements. The fair value as of th… |
| 9 | `META_FY2016_2016-12-31:195` | Item 7 › Share-based Compensation | ✓ |  | We have historically issued unvested restricted shares to employee stockholders of certain acquired companies. As these awards are generally subject to continued post-acquisition employment, we have accounted for them as… |
| 10 | `META_FY2016_2016-12-31:316` | Item 8 › Share-based Compensation | ✓ |  | We have historically issued unvested restricted shares to employee stockholders of certain acquired companies. As these awards are generally subject to continued post-acquisition employment, we have accounted for them as… |
| 11 | `META_FY2016_2016-12-31:400` | Item 8 › Share-based Compensation Plans |  |  | \| \| Unvested RSUs(1) \| \| \|---\|---\|---\| \| \| Number of Shares \| Weighted Average Grant Date Fair Value \| \| \| (in thousands) \| \| \| Unvested at December 31, 2015 \| 116,409 \| $65.95 \| \| Granted \| 30,414 \| 113.43 \| \| Vested \| … |
| 12 | `META_FY2016_2016-12-31:395` | Item 8 › Share-based Compensation Plans | ✓ | #2 | increase the number of shares reserved for issuance in 2016 and 2015. In addition, shares available for grant under the 2005 Stock Plan, which were reserved but not issued, forfeited or repurchased at their original issu… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2016_2016-12-31:315`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Share-based Compensation
In the fourth quarter of 2016, we elected to early adopt Accounting Standards Update No. 2016-09, Compensation-Stock Compensation (Topic 718): Improvement to Employee Share-based Payment Accounting (ASU 2016-09) issued by the Financial Accounting Standards Board (FASB), which among other items, provides an accounting policy election to account for forfeitures as they occur, rather than to account for them based on an estimate of expected forfeitures. We elected to account for forfeitures as they occur and therefore, share-based compensation expense for the year ended December 31, 2016 has been calculated based on actual forfeitures in our consolidated statements of income, rather than our previous approach which was net of estimated forfeitures. The net cumulative effect of this change increased additional paid-in capital as of January 1, 2016 by $39 million. Share-based compensation expense for the years ended December 31, 2015 and 2014 were recorded net of estimated forfeitures, which were based on historical forfeitures and adjusted to reflect changes in facts and circumstances, if any.
````

**#2 `META_FY2016_2016-12-31:194`** (cited, gold #1)

````text
Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations > Share-based Compensation
We elected to early adopt ASU 2016-09 in the fourth quarter of 2016, which among other items, provides an accounting policy election to account for forfeitures as they occur, rather than to account for them based on an estimate of expected forfeitures. We elected to account for forfeitures as they occur and therefore, share-based compensation expense for the year ended December 31, 2016 has been calculated based on actual forfeitures in our consolidated statements of income, rather than our previous approach which was net of estimated forfeitures. The net cumulative effect of this change was recognized as a $39 million increase to paid-in capital as of January 1, 2016. Share-based compensation expense for the years ended December 31, 2015 and 2014 were recorded net of estimated forfeitures, which were based on historical forfeitures and adjusted to reflect changes in facts and circumstances, if any.
````

**#3 `META_FY2016_2016-12-31:169`** (gold #1)

````text
Item 6. Selected Financial Data.
(1) In the fourth quarter of 2016, we elected to early adopt Accounting Standards Update No. 2016-09, Compensation-Stock Compensation (Topic 718): Improvement to Employee Share-based Payment Accounting (ASU 2016-09) which requires us, among other items, to record excess tax benefits as a reduction of the provision for income taxes in the income statements, whereas they were previously recognized in equity. We are required to reflect any adoption adjustments as of January 1, 2016, the beginning of the annual period that includes the interim period of adoption. As such, certain consolidated statements of income data for the year ended December 31, 2016 included the impact of the ASU 2016-09 adoption. See Note 1 of the accompanying notes to our consolidated financial statements for additional information related to this adoption. (2) Total costs and expenses include $3.22 billion, $2.97 billion, $1.84 billion, $906 million, and $1.57 billion of share-based compensation for the years ended December 31, 2016, 2015, 2014, 2013, and 2012, respectively.
````

**#4 `META_FY2016_2016-12-31:339`** (gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Accounting Pronouncements Adopted in 2016
We elected to early adopt the new guidance in the fourth quarter of 2016 which required us to reflect any adjustments as of January 1, 2016, the beginning of the annual period that includes the interim period of adoption. Upon adoption, excess tax benefits or deficiencies from share-based award activity are reflected in the consolidated statements of income as a component of the provision for income taxes, whereas they previously were recognized in equity. We also elected to account for forfeitures as they occur, rather than estimate expected forfeitures. The adoption of ASU 2016-09 resulted in net cumulative-effect adjustment of $1.67 billion increase to retained earnings as of January 1, 2016, mostly related to the recognition of the previously unrecognized excess tax benefits using the modified retrospective method. The previously unrecognized excess tax effects were recorded as a reduction to tax liability or an increase to deferred tax asset.
````

**#8 `META_FY2016_2016-12-31:401`** (cited, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Share-based Compensation Plans
(1) Unvested shares include inducement awards issued in connection with an acquisition in 2014 and are subject to the terms, restrictions, and conditions of separate non-plan RSU award agreements. The fair value as of the respective vesting dates of RSUs that vested during the years ended December 31, 2016, 2015, and 2014 was $4.92 billion, $4.23 billion, and $2.77 billion, respectively. As of December 31, 2016, there was $7.03 billion of unrecognized share-based compensation expense, of which (i) $6.78 billion was related to RSUs, and (ii) $255 million was related to restricted shares, shares related to our contingent consideration with performance conditions that were met in the second quarter of 2016 but are still subject to service condition, and stock options. This unrecognized compensation expense is expected to be recognized over a weighted-average period of approximately three years. Note 11. Interest and other income/(expense), net The following table presents the detail of interest and other income/(expense), net, for the periods presented (in millions):
````

**#9 `META_FY2016_2016-12-31:195`** (cited)

````text
Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations > Share-based Compensation
We have historically issued unvested restricted shares to employee stockholders of certain acquired companies. As these awards are generally subject to continued post-acquisition employment, we have accounted for them as post-acquisition share-based compensation expense. We recognize compensation expense equal to the grant date fair value of the common stock on a straight-line basis over the period during which the employee is required to perform service in exchange for the award.
````

**#10 `META_FY2016_2016-12-31:316`** (cited)

````text
Item 8. Financial Statements and Supplementary Data > Share-based Compensation
We have historically issued unvested restricted shares to employee stockholders of certain acquired companies. As these awards are generally subject to continued post-acquisition employment, we have accounted for them as post-acquisition share-based compensation expense. We recognize compensation expense equal to the grant date fair value of the common stock on a straight-line basis over the period during which the employee is required to perform service in exchange for the award.
````

**#12 `META_FY2016_2016-12-31:395`** (cited, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Share-based Compensation Plans
increase the number of shares reserved for issuance in 2016 and 2015. In addition, shares available for grant under the 2005 Stock Plan, which were reserved but not issued, forfeited or repurchased at their original issue price, or subject to outstanding awards under the 2005 Stock Plan as of the effective date of our IPO, were added to the reserves of the Amended 2012 Plan and shares that are withheld in connection with the net settlement of RSUs are also added to the reserves of the Amended 2012 Plan. In connection with an acquisition in 2014, we granted inducement awards covering an aggregate of 37 million RSUs earned over a service period of four years. These awards are excluded from the Stock Plans and are subject to the terms, restrictions, and conditions of separate non-plan RSU award agreements. The following table summarizes the activities of stock option awards under the Stock Plans for the year ended December 31, 2016:
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8'), ('META', 'Item 7')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 2, verified 2, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 4, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In the fourth quarter of 2016, Meta Platforms early adopted ASU 2016-09 and changed its accounting policy for share-based compensation forfeitures from estimating expected forfeitures to accounting for forfeitures as they occur. [META FY2016, Item 8, META_FY2016_2016-12-31:315] [META FY2016, Item 7, META_FY2016_2016-12-31:194] | supported | The evidence states Meta early adopted ASU 2016-09 in Q4 2016 and changed from estimated forfeitures to accounting for forfeitures as they occur. |
| As a result, share-based compensation expense for the year ended December 31, 2016 was calculated based on actual forfeitures, whereas for 2015 and 2014 the expense had been recorded net of estimated forfeitures based on historical forfeitures and adjusted for changes in facts and circumstances, if any. [META FY2016, Item 8, META_FY2016_2016-12-31:315] [META FY2016, Item 7, META_FY2016_2016-12-31:194] | supported | The cited text explicitly says 2016 expense used actual forfeitures, while 2015 and 2014 were recorded net of estimated forfeitures based on historical forfeitures and adjusted as needed. |
| The net cumulative effect of this change increased additional paid-in capital, or paid-in capital, by $39 million as of January 1, 2016. [META FY2016, Item 8, META_FY2016_2016-12-31:315] [META FY2016, Item 7, META_FY2016_2016-12-31:194] | None |  |
| In terms of vesting or service periods, Meta states that it recognizes compensation expense for certain unvested restricted shares on a straight-line basis over the period during which the employee is required to perform service in exchange for the award. [META FY2016, Item 7, META_FY2016_2016-12-31:195] [META FY2016, Item 8, META_FY2016_2016-12-31:316] | supported | The evidence says Meta recognizes compensation expense for certain unvested restricted shares on a straight-line basis over the employee service period. |
| For outstanding unrecognized share-based compensation expense as of December 31, 2016, Meta said the expense was expected to be recognized over a weighted-average period of approximately three years. [META FY2016, Item 8, META_FY2016_2016-12-31:401] | supported | The evidence states unrecognized share-based compensation expense as of December 31, 2016 was expected to be recognized over a weighted-average period of approximately three years. |
| Meta also disclosed that, in connection with a 2014 acquisition, it granted inducement RSU awards covering an aggregate of 37 million RSUs earned over a service period of four years. [META FY2016, Item 8, META_FY2016_2016-12-31:395] | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 3. Chunks retrieved: 13, cited: 3.

**Generated answer**

> In the fourth quarter of 2016, Meta early adopted ASU 2016-09 and changed its accounting policy for share-based compensation forfeitures from estimating expected forfeitures in advance to accounting for forfeitures as they occur. [META FY2016, Item 8, META_FY2016_2016-12-31:315] [META FY2016, Item 7, META_FY2016_2016-12-31:194]
>
> As a result, share-based compensation expense for the year ended December 31, 2016 was calculated based on actual forfeitures in the consolidated statements of income, whereas for 2015 and 2014 the expense had been recorded net of estimated forfeitures based on historical forfeitures and adjusted for changes in facts and circumstances, if any. [META FY2016, Item 8, META_FY2016_2016-12-31:315] [META FY2016, Item 7, META_FY2016_2016-12-31:194]
>
> The net cumulative effect of this forfeiture-policy change increased additional paid-in capital, or paid-in capital, by $39 million as of January 1, 2016. [META FY2016, Item 8, META_FY2016_2016-12-31:315] [META FY2016, Item 7, META_FY2016_2016-12-31:194]
>
> This policy interacts with vesting because Meta measures share-based awards at grant-date fair value and generally recognizes the resulting expense on a straight-line basis over the period the employee is required to perform service. [META FY2016, Item 8, META_FY2016_2016-12-31:314]
>
> The majority of Meta’s awards are earned over a service period of four years. [META FY2016, Item 8, META_FY2016_2016-12-31:314]
>
> So, under the new policy adopted in Q4 2016, Meta continues to recognize compensation expense over the service/vesting period for the awards, but forfeitures are now reflected when they actually occur rather than being estimated over that period in advance. [META FY2016, Item 8, META_FY2016_2016-12-31:315] [META FY2016, Item 7, META_FY2016_2016-12-31:194] [META FY2016, Item 8, META_FY2016_2016-12-31:314]

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `META_FY2016_2016-12-31:315` | Item 8 › Share-based Compensation | ✓ | #1 | In the fourth quarter of 2016, we elected to early adopt Accounting Standards Update No. 2016-09, Compensation-Stock Compensation (Topic 718): Improvement to Employee Share-based Payment Accounting (ASU 2016-09) issued b… |
| 2 | `META_FY2016_2016-12-31:194` | Item 7 › Share-based Compensation | ✓ | #1 | We elected to early adopt ASU 2016-09 in the fourth quarter of 2016, which among other items, provides an accounting policy election to account for forfeitures as they occur, rather than to account for them based on an e… |
| 3 | `META_FY2016_2016-12-31:169` | Item 6 |  | #1 | (1) In the fourth quarter of 2016, we elected to early adopt Accounting Standards Update No. 2016-09, Compensation-Stock Compensation (Topic 718): Improvement to Employee Share-based Payment Accounting (ASU 2016-09) whic… |
| 4 | `META_FY2016_2016-12-31:339` | Item 8 › Accounting Pronouncements Adopted in 2016 |  | #1 | We elected to early adopt the new guidance in the fourth quarter of 2016 which required us to reflect any adjustments as of January 1, 2016, the beginning of the annual period that includes the interim period of adoption… |
| 5 | `META_FY2016_2016-12-31:409` | Item 8 › Share-based Compensation Plans |  |  | (1) Due to the adoption of ASU 2016-09, excess tax benefits from share-based award activity for the year ended December 31, 2016 are reflected as a reduction of the provision for income taxes, whereas they previously wer… |
| 6 | `META_FY2016_2016-12-31:410` | Item 8 › Share-based Compensation Plans |  |  | \| \| December 31, \| \| \|---\|---\|---\| \| \| 2016 \| 2015 \| \| Deferred tax assets: \| \| \| \| Net operating loss carryforward \| $1,252 \| $476 \| \| Tax credit carryforward \| 268 \| 297 \| \| Share-based compensation \| 684 \| 529 \| \| Acc… |
| 7 | `META_FY2016_2016-12-31:338` | Item 8 › Accounting Pronouncements Adopted in 2016 |  |  | In March 2016, the FASB issued ASU 2016-09 to simplify certain aspects of the accounting for share-based payment transactions to employees. The new standard requires excess tax benefits and tax deficiencies to be recorde… |
| 8 | `META_FY2016_2016-12-31:401` | Item 8 › Share-based Compensation Plans |  | #2 | (1) Unvested shares include inducement awards issued in connection with an acquisition in 2014 and are subject to the terms, restrictions, and conditions of separate non-plan RSU award agreements. The fair value as of th… |
| 9 | `META_FY2016_2016-12-31:195` | Item 7 › Share-based Compensation |  |  | We have historically issued unvested restricted shares to employee stockholders of certain acquired companies. As these awards are generally subject to continued post-acquisition employment, we have accounted for them as… |
| 10 | `META_FY2016_2016-12-31:316` | Item 8 › Share-based Compensation |  |  | We have historically issued unvested restricted shares to employee stockholders of certain acquired companies. As these awards are generally subject to continued post-acquisition employment, we have accounted for them as… |
| 11 | `META_FY2016_2016-12-31:400` | Item 8 › Share-based Compensation Plans |  |  | \| \| Unvested RSUs(1) \| \| \|---\|---\|---\| \| \| Number of Shares \| Weighted Average Grant Date Fair Value \| \| \| (in thousands) \| \| \| Unvested at December 31, 2015 \| 116,409 \| $65.95 \| \| Granted \| 30,414 \| 113.43 \| \| Vested \| … |
| 12 | `META_FY2016_2016-12-31:403` | Item 8 › Share-based Compensation Plans |  |  | Note 12. Income Taxes The components of income before provision for income taxes for the years ended December 31, 2016, 2015, and 2014 are as follows (in millions): |
| 13 | `META_FY2016_2016-12-31:314` | Item 8 › Share-based Compensation | ✓ | #2 | We account for share-based employee compensation plans under the fair value recognition and measurement provisions of GAAP. Those provisions require all share-based payments to employees, including grants of stock option… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `META_FY2016_2016-12-31:315`** (cited, gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Share-based Compensation
In the fourth quarter of 2016, we elected to early adopt Accounting Standards Update No. 2016-09, Compensation-Stock Compensation (Topic 718): Improvement to Employee Share-based Payment Accounting (ASU 2016-09) issued by the Financial Accounting Standards Board (FASB), which among other items, provides an accounting policy election to account for forfeitures as they occur, rather than to account for them based on an estimate of expected forfeitures. We elected to account for forfeitures as they occur and therefore, share-based compensation expense for the year ended December 31, 2016 has been calculated based on actual forfeitures in our consolidated statements of income, rather than our previous approach which was net of estimated forfeitures. The net cumulative effect of this change increased additional paid-in capital as of January 1, 2016 by $39 million. Share-based compensation expense for the years ended December 31, 2015 and 2014 were recorded net of estimated forfeitures, which were based on historical forfeitures and adjusted to reflect changes in facts and circumstances, if any.
````

**#2 `META_FY2016_2016-12-31:194`** (cited, gold #1)

````text
Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations > Share-based Compensation
We elected to early adopt ASU 2016-09 in the fourth quarter of 2016, which among other items, provides an accounting policy election to account for forfeitures as they occur, rather than to account for them based on an estimate of expected forfeitures. We elected to account for forfeitures as they occur and therefore, share-based compensation expense for the year ended December 31, 2016 has been calculated based on actual forfeitures in our consolidated statements of income, rather than our previous approach which was net of estimated forfeitures. The net cumulative effect of this change was recognized as a $39 million increase to paid-in capital as of January 1, 2016. Share-based compensation expense for the years ended December 31, 2015 and 2014 were recorded net of estimated forfeitures, which were based on historical forfeitures and adjusted to reflect changes in facts and circumstances, if any.
````

**#3 `META_FY2016_2016-12-31:169`** (gold #1)

````text
Item 6. Selected Financial Data.
(1) In the fourth quarter of 2016, we elected to early adopt Accounting Standards Update No. 2016-09, Compensation-Stock Compensation (Topic 718): Improvement to Employee Share-based Payment Accounting (ASU 2016-09) which requires us, among other items, to record excess tax benefits as a reduction of the provision for income taxes in the income statements, whereas they were previously recognized in equity. We are required to reflect any adoption adjustments as of January 1, 2016, the beginning of the annual period that includes the interim period of adoption. As such, certain consolidated statements of income data for the year ended December 31, 2016 included the impact of the ASU 2016-09 adoption. See Note 1 of the accompanying notes to our consolidated financial statements for additional information related to this adoption. (2) Total costs and expenses include $3.22 billion, $2.97 billion, $1.84 billion, $906 million, and $1.57 billion of share-based compensation for the years ended December 31, 2016, 2015, 2014, 2013, and 2012, respectively.
````

**#4 `META_FY2016_2016-12-31:339`** (gold #1)

````text
Item 8. Financial Statements and Supplementary Data > Accounting Pronouncements Adopted in 2016
We elected to early adopt the new guidance in the fourth quarter of 2016 which required us to reflect any adjustments as of January 1, 2016, the beginning of the annual period that includes the interim period of adoption. Upon adoption, excess tax benefits or deficiencies from share-based award activity are reflected in the consolidated statements of income as a component of the provision for income taxes, whereas they previously were recognized in equity. We also elected to account for forfeitures as they occur, rather than estimate expected forfeitures. The adoption of ASU 2016-09 resulted in net cumulative-effect adjustment of $1.67 billion increase to retained earnings as of January 1, 2016, mostly related to the recognition of the previously unrecognized excess tax benefits using the modified retrospective method. The previously unrecognized excess tax effects were recorded as a reduction to tax liability or an increase to deferred tax asset.
````

**#8 `META_FY2016_2016-12-31:401`** (gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Share-based Compensation Plans
(1) Unvested shares include inducement awards issued in connection with an acquisition in 2014 and are subject to the terms, restrictions, and conditions of separate non-plan RSU award agreements. The fair value as of the respective vesting dates of RSUs that vested during the years ended December 31, 2016, 2015, and 2014 was $4.92 billion, $4.23 billion, and $2.77 billion, respectively. As of December 31, 2016, there was $7.03 billion of unrecognized share-based compensation expense, of which (i) $6.78 billion was related to RSUs, and (ii) $255 million was related to restricted shares, shares related to our contingent consideration with performance conditions that were met in the second quarter of 2016 but are still subject to service condition, and stock options. This unrecognized compensation expense is expected to be recognized over a weighted-average period of approximately three years. Note 11. Interest and other income/(expense), net The following table presents the detail of interest and other income/(expense), net, for the periods presented (in millions):
````

**#13 `META_FY2016_2016-12-31:314`** (cited, gold #2)

````text
Item 8. Financial Statements and Supplementary Data > Share-based Compensation
We account for share-based employee compensation plans under the fair value recognition and measurement provisions of GAAP. Those provisions require all share-based payments to employees, including grants of stock options and restricted stock units (RSUs), to be measured based on the grant date fair value of the awards, with the resulting expense generally recognized on a straight-line basis in our consolidated statements of income over the period during which the employee is required to perform service in exchange for the award. The majority of our awards are earned over a service period of four years.
````

</details>

RQ2 citation match (section level): `cited=[('META', 'Item 8'), ('META', 'Item 7')] gold=[(None, 'Item 8')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 1, verified 1, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 5, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| In the fourth quarter of 2016, Meta early adopted ASU 2016-09 and changed its accounting policy for share-based compensation forfeitures from estimating expected forfeitures in advance to accounting for forfeitures as they occur. [META FY2016, Item 8, META_FY2016_2016-12-31:315] [META FY2016, Item 7, META_FY2016_2016-12-31:194] | supported | The evidence states Meta early adopted ASU 2016-09 in Q4 2016 and changed from estimated forfeitures to accounting for forfeitures as they occur. |
| As a result, share-based compensation expense for the year ended December 31, 2016 was calculated based on actual forfeitures in the consolidated statements of income, whereas for 2015 and 2014 the expense had been recorded net of estimated forfeitures based on historical forfeitures and adjusted for changes in facts and circumstances, if any. [META FY2016, Item 8, META_FY2016_2016-12-31:315] [META FY2016, Item 7, META_FY2016_2016-12-31:194] | supported | The cited text explicitly says 2016 expense was based on actual forfeitures, while 2015 and 2014 were net of estimated forfeitures based on history and adjusted as needed. |
| The net cumulative effect of this forfeiture-policy change increased additional paid-in capital, or paid-in capital, by $39 million as of January 1, 2016. [META FY2016, Item 8, META_FY2016_2016-12-31:315] [META FY2016, Item 7, META_FY2016_2016-12-31:194] | None |  |
| This policy interacts with vesting because Meta measures share-based awards at grant-date fair value and generally recognizes the resulting expense on a straight-line basis over the period the employee is required to perform service. [META FY2016, Item 8, META_FY2016_2016-12-31:314] | supported | The evidence states awards are measured at grant-date fair value and expense is generally recognized straight-line over the employee service period. |
| The majority of Meta’s awards are earned over a service period of four years. [META FY2016, Item 8, META_FY2016_2016-12-31:314] | supported | The evidence explicitly says the majority of awards are earned over a service period of four years. |
| So, under the new policy adopted in Q4 2016, Meta continues to recognize compensation expense over the service/vesting period for the awards, but forfeitures are now reflected when they actually occur rather than being estimated over that period in advance. [META FY2016, Item 8, META_FY2016_2016-12-31:315] [META FY2016, Item 7, META_FY2016_2016-12-31:194] [META FY2016, Item 8, META_FY2016_2016-12-31:314] | supported | Taken together, the evidence supports that expense continues to be recognized over the service period while forfeitures are now accounted for when they occur rather than estimated in advance. |

</details>
