# gold-008: Single-hop table

[← all cases](../README.md) · company: JPMORGAN CHASE & CO (JPM) · fiscal year: 2021 · recipe `table` · hop `single` · answer type `numeric` · scope `single_doc` · RQ2 category `quantitative_tabular`

## Gold QA

**Question**

> For JPMorgan Chase & Co (JPM) in fiscal year 2021, what was the difference in percentage points between the proportion of total employees who were White and the proportion of senior level employees who were White?

**Gold answer**

> 31 percentage points

**Program**: `subtract(77, 46)` → `31.0`

**Gold numbers** (RQ2 numeric_accuracy targets): 31 percentage points

**Gold evidence**

1. `JPM_FY2021_2021-12-31` · Item 1. Business. › Human capital · table

   > | White | 46% | 77% | 84% | 90% | |

## Scorecard

| Metric | A (vanilla dense) | B (hybrid + rerank) | C v1 (adaptive multi-hop) | C v2 (agentic multi-hop + XBRL) |
|---|---|---|---|---|
| **Retrieval (RQ1)** | | | | |
| chunks retrieved | 10 | 5 | 6 | 6 |
| recall@5 | 1.00 | 1.00 | 1.00 | 1.00 |
| recall@all | 1.00 | 1.00 | 1.00 | 1.00 |
| complete@all | 1 | 1 | 1 | 1 |
| average precision (lexical) | 1.00 | 1.00 | 1.00 | 1.00 |
| gold evidence first rank | #1: 1 | #1: 1 | #1: 1 | #1: 1 |
| **Answer (RQ3 string match)** | | | | |
| numeric_correct | ✓ | ✓ | ✓ | ✓ |
| keypoint_recall | – | – | – | – |
| **Answer & citations (RQ2)** | | | | |
| numeric_accuracy | 1.00 | 1.00 | 1.00 | 1.00 |
| citation precision | 1.00 | 1.00 | 1.00 | 1.00 |
| citation recall | 1.00 | 1.00 | 1.00 | 1.00 |
| citation F1 | 1.00 | 1.00 | 1.00 | 1.00 |
| has a citation | 1 | 1 | 1 | 1 |
| grounding error rate | – | – | 0.00 | 0.00 |
| **Cost (RQ3)** | | | | |
| retrieval hops | 1 | 1 | 1 | 1 |
| tokens | 2396 | 1338 | 4539 | 4262 |
| cost (USD) | 0.0004 | 0.0002 | 0.0156 | 0.0145 |
| latency (s) | 1.9 | 6.4 | 6.8 | 7.2 |

Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, no citations, no guardrail).

## System outputs

### System A (vanilla dense)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 10, cited: 1.

**Generated answer**

> The proportion of total employees who were White was 46%, and the proportion of senior level employees who were White was 77%, so the difference was 31 percentage points [1].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JPM_FY2021_2021-12-31:17` | Item 1 › Human capital | ✓ | #1 | \| December 31, 2021 \| Total employees \| Senior level employees(e) \| Operating Committee \| Board of Directors \| \| \|---\|---\|---\|---\|---\|---\| \| Race/Ethnicity(a): \| \| \| \| \| \| \| White \| 46% \| 77% \| 84% \| 90% \| \| \| Hispanic \|… |
| 2 | `JPM_FY2021_2021-12-31:18` | Item 1 › Human capital |  |  | (a)Based on EEO metrics. Presented as a percentage of the respective populations who self-identified race/ethnicity: 96% and 95% of the Firm’s total U.S.-based employees and U.S.-based senior level employees, respectivel… |
| 3 | `JPM_FY2021_2021-12-31:15` | Item 1 › Human capital |  |  | \| Employee Breakdown by Region \| \| Employee Breakdown by LOB and Corporate \| \| \|---\|---\|---\|---\| \| Region \| Employees \| LOB \| Employees \| \| North America \| 169,090 \| CCB \| 128,863 \| \| Europe/Middle East/Africa \| 24,260 \|… |
| 4 | `JPM_FY2021_2021-12-31:14` | Item 1 › Human capital |  |  | JPMorgan Chase believes that its long-term growth and success depend on its ability to attract, develop and retain a high-performing and diverse workforce, with inclusion and accessibility as key components of the way th… |
| 5 | `JPM_FY2021_2021-12-31:1101` | Item 15 › employee benefit plans |  |  | The weighted-average discount rate used to value the benefit obligations as of December 31, 2021 and 2020, was 2.54% and 2.17%, respectively. |
| 6 | `JPM_FY2021_2021-12-31:321` | Item 15 › Segment Results – Managed Basis |  |  | \| Year ended December 31, \| Consumer & Community Banking \| \| \| Corporate & Investment Bank \| \| \| Commercial Banking \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| (in millions, except ratios) \| 2021 \| 2020 \| 2019 \| 20… |
| 7 | `JPM_FY2021_2021-12-31:200` | Item 11 |  |  | Refer to Item 10. |
| 8 | `JPM_FY2021_2021-12-31:16` | Item 1 › Human capital |  |  | Diversity, equity and inclusion In connection with its diversity initiatives, the Firm periodically requests that its employees and Board members self-identify based on specified diversity categories. The following table… |
| 9 | `JPM_FY2021_2021-12-31:346` | Item 15 › Management’s discussion and analysis |  |  | \| Selected income statement data \| \| \| \| \|---\|---\|---\|---\| \| Year ended December 31, \| \| \| \| \| (in millions, except ratios) \| 2021 \| 2020 \| 2019 \| \| Financial ratios \| \| \| \| \| Return on equity \| 25% \| 20% \| 14% \| \| Overh… |
| 10 | `JPM_FY2021_2021-12-31:1299` | Item 15 › Notes to consolidated financial statements |  |  | (a)Reflects quarterly average of forecasted U.S. unemployment rate. (b)As of December 31, 2021, the year over year growth in U.S. real GDP in the forecast horizon of the central scenario is calculated as the percent chan… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JPM_FY2021_2021-12-31:17`** (cited, gold #1)

````text
Item 1. Business. > Human capital (table)
| December 31, 2021 | Total employees | Senior level employees(e) | Operating Committee | Board of Directors |  |
|---|---|---|---|---|---|
| Race/Ethnicity(a): |  |  |  |  |  |
| White | 46% | 77% | 84% | 90% |  |
| Hispanic | 20% | 6% | 11% | — |  |
| Asian | 17% | 11% | 5% | — |  |
| Black | 14% | 5% | — | 10% |  |
| Other(b) | 3% | 1% | — | — |  |
| Gender(c): |  |  |  |  |  |
| Men | 51% | 74% | 63% | 60% |  |
| Women | 49% | 26% | 37% | 40% |  |
| LGBT+(d) | 4% | 2% | 5% | — |  |
| Military veterans(d) | 3% | 2% | — | — |  |
| People with disabilities(d) | 4% | 2% | — | — | (f) |
````

</details>

RQ2 citation match (section level): `cited=[('JPM', 'Item 1')] gold=[(None, 'Item 1')]`

### System B (hybrid + rerank)

Model: `gpt-5.4-2026-03-05`. Hops: 1. Chunks retrieved: 5, cited: 1.

**Generated answer**

> The proportion of White total employees was 46%, and the proportion of White senior level employees was 77%, so the difference was 31 percentage points [1].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JPM_FY2021_2021-12-31:17` | Item 1 › Human capital | ✓ | #1 | \| December 31, 2021 \| Total employees \| Senior level employees(e) \| Operating Committee \| Board of Directors \| \| \|---\|---\|---\|---\|---\|---\| \| Race/Ethnicity(a): \| \| \| \| \| \| \| White \| 46% \| 77% \| 84% \| 90% \| \| \| Hispanic \|… |
| 2 | `JPM_FY2021_2021-12-31:18` | Item 1 › Human capital |  |  | (a)Based on EEO metrics. Presented as a percentage of the respective populations who self-identified race/ethnicity: 96% and 95% of the Firm’s total U.S.-based employees and U.S.-based senior level employees, respectivel… |
| 3 | `JPM_FY2021_2021-12-31:20` | Item 1 › Human capital |  |  | The goal of JPMorgan Chase’s recruitment efforts is to attract and hire talented individuals in all roles and at all career levels. The Firm strives to provide both external candidates and internal employees who are seek… |
| 4 | `JPM_FY2021_2021-12-31:14` | Item 1 › Human capital |  |  | JPMorgan Chase believes that its long-term growth and success depend on its ability to attract, develop and retain a high-performing and diverse workforce, with inclusion and accessibility as key components of the way th… |
| 5 | `JPM_FY2021_2021-12-31:251` | Item 15 › Selected capital-related metrics |  |  | •The Firm’s CET1 capital was $214 billion, and the Standardized and Advanced CET1 ratios were 13.1% and 13.8%, respectively. •The Firm’s SLR was 5.4%. •The Firm grew TBVPS, ending 2021 at $71.53, up 8% versus the prior y… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JPM_FY2021_2021-12-31:17`** (cited, gold #1)

````text
Item 1. Business. > Human capital (table)
| December 31, 2021 | Total employees | Senior level employees(e) | Operating Committee | Board of Directors |  |
|---|---|---|---|---|---|
| Race/Ethnicity(a): |  |  |  |  |  |
| White | 46% | 77% | 84% | 90% |  |
| Hispanic | 20% | 6% | 11% | — |  |
| Asian | 17% | 11% | 5% | — |  |
| Black | 14% | 5% | — | 10% |  |
| Other(b) | 3% | 1% | — | — |  |
| Gender(c): |  |  |  |  |  |
| Men | 51% | 74% | 63% | 60% |  |
| Women | 49% | 26% | 37% | 40% |  |
| LGBT+(d) | 4% | 2% | 5% | — |  |
| Military veterans(d) | 3% | 2% | — | — |  |
| People with disabilities(d) | 4% | 2% | — | — | (f) |
````

</details>

RQ2 citation match (section level): `cited=[('JPM', 'Item 1')] gold=[(None, 'Item 1')]`

### System C v1 (adaptive multi-hop)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 1.

**Generated answer**

> The proportion of total employees who were White was 46%, and the proportion of senior level employees who were White was 77%, a difference of 31 percentage points [JPM FY2021, Item 1, JPM_FY2021_2021-12-31:17].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JPM_FY2021_2021-12-31:17` | Item 1 › Human capital | ✓ | #1 | \| December 31, 2021 \| Total employees \| Senior level employees(e) \| Operating Committee \| Board of Directors \| \| \|---\|---\|---\|---\|---\|---\| \| Race/Ethnicity(a): \| \| \| \| \| \| \| White \| 46% \| 77% \| 84% \| 90% \| \| \| Hispanic \|… |
| 2 | `JPM_FY2021_2021-12-31:18` | Item 1 › Human capital |  |  | (a)Based on EEO metrics. Presented as a percentage of the respective populations who self-identified race/ethnicity: 96% and 95% of the Firm’s total U.S.-based employees and U.S.-based senior level employees, respectivel… |
| 3 | `JPM_FY2021_2021-12-31:15` | Item 1 › Human capital |  |  | \| Employee Breakdown by Region \| \| Employee Breakdown by LOB and Corporate \| \| \|---\|---\|---\|---\| \| Region \| Employees \| LOB \| Employees \| \| North America \| 169,090 \| CCB \| 128,863 \| \| Europe/Middle East/Africa \| 24,260 \|… |
| 4 | `JPM_FY2021_2021-12-31:16` | Item 1 › Human capital |  |  | Diversity, equity and inclusion In connection with its diversity initiatives, the Firm periodically requests that its employees and Board members self-identify based on specified diversity categories. The following table… |
| 5 | `JPM_FY2021_2021-12-31:321` | Item 15 › Segment Results – Managed Basis |  |  | \| Year ended December 31, \| Consumer & Community Banking \| \| \| Corporate & Investment Bank \| \| \| Commercial Banking \| \| \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|---\| \| (in millions, except ratios) \| 2021 \| 2020 \| 2019 \| 20… |
| 6 | `JPM_FY2021_2021-12-31:14` | Item 1 › Human capital |  |  | JPMorgan Chase believes that its long-term growth and success depend on its ability to attract, develop and retain a high-performing and diverse workforce, with inclusion and accessibility as key components of the way th… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JPM_FY2021_2021-12-31:17`** (cited, gold #1)

````text
Item 1. Business. > Human capital (table)
| December 31, 2021 | Total employees | Senior level employees(e) | Operating Committee | Board of Directors |  |
|---|---|---|---|---|---|
| Race/Ethnicity(a): |  |  |  |  |  |
| White | 46% | 77% | 84% | 90% |  |
| Hispanic | 20% | 6% | 11% | — |  |
| Asian | 17% | 11% | 5% | — |  |
| Black | 14% | 5% | — | 10% |  |
| Other(b) | 3% | 1% | — | — |  |
| Gender(c): |  |  |  |  |  |
| Men | 51% | 74% | 63% | 60% |  |
| Women | 49% | 26% | 37% | 40% |  |
| LGBT+(d) | 4% | 2% | 5% | — |  |
| Military veterans(d) | 3% | 2% | — | — |  |
| People with disabilities(d) | 4% | 2% | — | — | (f) |
````

</details>

RQ2 citation match (section level): `cited=[('JPM', 'Item 1')] gold=[(None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 2, verified 2, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| The proportion of total employees who were White was 46%, and the proportion of senior level employees who were White was 77%, a difference of 31 percentage points [JPM FY2021, Item 1, JPM_FY2021_2021-12-31:17]. | None |  |

</details>

### System C v2 (agentic multi-hop + XBRL)

Model: `gpt-5.4`. Hops: 1. Chunks retrieved: 6, cited: 1.

**Generated answer**

> The proportion of total employees who were White was 46%, and the proportion of senior level employees who were White was 77%, so the difference was 31 percentage points [JPM FY2021, Item 1, JPM_FY2021_2021-12-31:17].

**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; gold = holds gold evidence item #, by RQ1's lexical matcher)

| # | chunk id | section | cited | gold | snippet |
|---|---|---|---|---|---|
| 1 | `JPM_FY2021_2021-12-31:17` | Item 1 › Human capital | ✓ | #1 | \| December 31, 2021 \| Total employees \| Senior level employees(e) \| Operating Committee \| Board of Directors \| \| \|---\|---\|---\|---\|---\|---\| \| Race/Ethnicity(a): \| \| \| \| \| \| \| White \| 46% \| 77% \| 84% \| 90% \| \| \| Hispanic \|… |
| 2 | `JPM_FY2021_2021-12-31:18` | Item 1 › Human capital |  |  | (a)Based on EEO metrics. Presented as a percentage of the respective populations who self-identified race/ethnicity: 96% and 95% of the Firm’s total U.S.-based employees and U.S.-based senior level employees, respectivel… |
| 3 | `JPM_FY2021_2021-12-31:15` | Item 1 › Human capital |  |  | \| Employee Breakdown by Region \| \| Employee Breakdown by LOB and Corporate \| \| \|---\|---\|---\|---\| \| Region \| Employees \| LOB \| Employees \| \| North America \| 169,090 \| CCB \| 128,863 \| \| Europe/Middle East/Africa \| 24,260 \|… |
| 4 | `JPM_FY2021_2021-12-31:16` | Item 1 › Human capital |  |  | Diversity, equity and inclusion In connection with its diversity initiatives, the Firm periodically requests that its employees and Board members self-identify based on specified diversity categories. The following table… |
| 5 | `JPM_FY2021_2021-12-31:14` | Item 1 › Human capital |  |  | JPMorgan Chase believes that its long-term growth and success depend on its ability to attract, develop and retain a high-performing and diverse workforce, with inclusion and accessibility as key components of the way th… |
| 6 | `JPM_FY2021_2021-12-31:1120` | Item 15 › Employee share-based awards |  |  | The Firm separately recognizes compensation expense for each tranche of each award, net of estimated forfeitures, as if it were a separate award with its own vesting date. Generally, for each tranche granted, compensatio… |

<details><summary>Full text of cited and gold-matching chunks</summary>

**#1 `JPM_FY2021_2021-12-31:17`** (cited, gold #1)

````text
Item 1. Business. > Human capital (table)
| December 31, 2021 | Total employees | Senior level employees(e) | Operating Committee | Board of Directors |  |
|---|---|---|---|---|---|
| Race/Ethnicity(a): |  |  |  |  |  |
| White | 46% | 77% | 84% | 90% |  |
| Hispanic | 20% | 6% | 11% | — |  |
| Asian | 17% | 11% | 5% | — |  |
| Black | 14% | 5% | — | 10% |  |
| Other(b) | 3% | 1% | — | — |  |
| Gender(c): |  |  |  |  |  |
| Men | 51% | 74% | 63% | 60% |  |
| Women | 49% | 26% | 37% | 40% |  |
| LGBT+(d) | 4% | 2% | 5% | — |  |
| Military veterans(d) | 3% | 2% | — | — |  |
| People with disabilities(d) | 4% | 2% | — | — | (f) |
````

</details>

RQ2 citation match (section level): `cited=[('JPM', 'Item 1')] gold=[(None, 'Item 1')]`

**System C guardrail** (judge `gpt-5.4`): numerical claims 2, verified 2, ungrounded 0, uncited 0, derived 0; sentence verdicts: supported 0, partial 0, unsupported 0, unchecked 0.


<details><summary>Guardrail sentence verdicts</summary>

| sentence | verdict | judge reason |
|---|---|---|
| The proportion of total employees who were White was 46%, and the proportion of senior level employees who were White was 77%, so the difference was 31 percentage points [JPM FY2021, Item 1, JPM_FY2021_2021-12-31:17]. | None |  |

</details>
