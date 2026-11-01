# Showcase cases

Selected by `scripts/case_studies/select_showcase.py` from `reports/rq3/records.jsonl` using fixed pass/fail rules on numeric correctness (numeric/mixed questions only; numeric first, then shorter question, then id). Read the full page in `cases/` before using a case: the check is a string match.

## 1. Every system passes

35 eligible question(s).

**Pick: [gold-004](cases/gold-004.md)** (numeric, multi-hop, recipe `table`)

> What is the ratio of Apple Inc.'s interest expense to its interest and dividend income for fiscal year 2019?

Gold answer: 0.72

| System | Correct | Hops | Latency s | Answer (start) |
|---|---|---|---|---|
| A | yes | 1 | 2.1 | For fiscal year 2019, Apple reported interest expense of $3,576 million and interest and dividend income of $4,961 million [1]. Ratio = 3,576 / 4,961 ≈ 0.72 So, the ratio of interest expense to interest and dividend inc… |
| B | yes | 1 | 7.0 | For fiscal 2019, Apple reported interest expense of $3,576 million and interest and dividend income of $4,961 million.[2] Calculation: - Interest expense = 3,576[2] - Interest and dividend income = 4,961[2] - Ratio = 3,… |
| C v1 | yes | 1 | 7.6 | Apple Inc.'s interest expense was $(3,576) and its interest and dividend income was $4,961 in fiscal year 2019, so the ratio of interest expense to interest and dividend income was approximately 0.72:1.00 [AAPL FY2019, … |
| C v2 | yes | 1 | 7.0 | Apple Inc.'s interest expense was $(3,576) and its interest and dividend income was $4,961 in fiscal year 2019, so the ratio of interest expense to interest and dividend income was approximately 0.72:1. [AAPL FY2019, It… |
| C v3 | yes | 1 | 4.7 | Apple Inc.'s interest expense was $(3,576) and its interest and dividend income was $4,961 in fiscal year 2019, so the ratio of interest expense to interest and dividend income was 72.08% (3,576 ÷ 4,961). [AAPL FY2019, … |

Alternates: [gold-068](cases/gold-068.md), [gold-002](cases/gold-002.md)

## 2. B and C pass, A fails

5 eligible question(s).

**Pick: [gold-016](cases/gold-016.md)** (numeric, multi-hop, recipe `cross_year_table`)

> By what percentage did Meta Platforms' accrued compensation and benefits grow from December 31, 2016 to December 31, 2022?

Gold answer: 621.86%

| System | Correct | Hops | Latency s | Answer (start) |
|---|---|---|---|---|
| A | no | 1 | 1.8 | Not found in the provided context. |
| B | yes | 1 | 7.7 | Meta Platforms' accrued compensation and benefits increased from **$636 million** at December 31, 2016 to **$4,591 million** at December 31, 2022. [4][3] Calculation: - Increase = 4,591 − 636 = **3,955** million [4][3] … |
| C v1 | yes | 1 | 9.0 | Meta Platforms' accrued compensation and benefits increased from $636 million at December 31, 2016 to $4,591 million at December 31, 2022 [META FY2016, Item 8, META_FY2016_2016-12-31:374] [META FY2022, Item 8, META_FY20… |
| C v2 | yes | 1 | 10.6 | Meta Platforms' accrued compensation and benefits increased from $636 million at December 31, 2016 to $4,591 million at December 31, 2022. [META FY2016, Item 8, META_FY2016_2016-12-31:374] [META FY2022, Item 8, META_FY2… |
| C v3 | yes | 1 | 7.7 | Meta Platforms' accrued compensation and benefits increased from $636 million at December 31, 2016 to $4,591 million at December 31, 2022 [META FY2016, Item 8, META_FY2016_2016-12-31:374] [META FY2022, Item 8, META_FY20… |

Alternates: [gold-092](cases/gold-092.md), [gold-090](cases/gold-090.md)

## 3. A and B fail, C passes

10 eligible question(s).

**Pick: [gold-077](cases/gold-077.md)** (numeric, multi-hop, recipe `cross_year_table`)

> By what percentage did Tesla's total revenue grow from fiscal year 2017 to fiscal year 2023?

Gold answer: 722.99%

| System | Correct | Hops | Latency s | Answer (start) |
|---|---|---|---|---|
| A | no | 1 | 1.2 | Not found in the provided context. |
| B | no | 1 | 7.3 | The passages do not provide Tesla’s **total revenue for fiscal year 2017**, so the percentage growth from **2017 to 2023** cannot be calculated from the provided context. [2][3] - **2023 total revenue** = **$96,773 mill… |
| C v1 | yes | 3 | 21.0 | Tesla’s total revenues were $11,758,751 thousand in fiscal year 2017 and $96,773 million in fiscal year 2023. [TSLA FY2017, Item 6, TSLA_FY2017_2017-12-31:213] [TSLA FY2023, Item 8, TSLA_FY2023_2023-12-31:471] Using tho… |
| C v2 | yes | 1 | 6.6 | Tesla’s total revenue grew from $11,758,751,000 in fiscal year 2017 to $96,773,000,000 in fiscal year 2023, an increase of approximately 723% [F-TSLA-2017] [F-TSLA-2023]. |
| C v3 | yes | 1 | 6.0 | Tesla’s total revenue grew from $11,758,751,000 in fiscal year 2017 to $96,773,000,000 in fiscal year 2023, an increase of approximately 723.0% [F-TSLA-2017] [F-TSLA-2023]. |

Alternates: [gold-073](cases/gold-073.md), [gold-067](cases/gold-067.md)

## 4. A, B, C v1 and C v2 fail, only C v3 passes

3 eligible question(s).

**Pick: [gold-074](cases/gold-074.md)** (numeric, multi-hop, recipe `cross_year_table`)

> By how many millions of dollars was Alphabet Inc.'s net gain on equity securities in fiscal year 2024 lower than in fiscal year 2018?

Gold answer: $1,746 million

| System | Correct | Hops | Latency s | Answer (start) |
|---|---|---|---|---|
| A | no | 1 | 9.8 | Not found in the provided context. |
| B | no | 1 | 7.4 | The provided passages do not include Alphabet’s fiscal year 2018 net gain on equity securities, so the comparison cannot be calculated from the supplied context. [6][9] - FY 2024 total gain on equity securities in other… |
| C v1 | no | 3 | 24.6 | The filing evidence provided does not disclose Alphabet Inc.'s net gain on equity securities for fiscal year 2018, so the difference versus fiscal year 2024 cannot be determined from these evidence blocks. |
| C v2 | no | 1 | 11.0 | The filing does not disclose Alphabet Inc.'s net gain on equity securities for fiscal year 2018, so the difference versus fiscal year 2024 cannot be determined from the provided evidence. |
| C v3 | yes | 3 | 19.8 | Alphabet Inc.'s total gain (loss) on equity securities in other income (expense), net was $3,714 million in fiscal year 2024 and $5,460 million in fiscal year 2018. [GOOGL FY2024, Item 8, GOOGL_FY2024_2024-12-31:376] [G… |

Alternates: [gold-011](cases/gold-011.md), [gold-061](cases/gold-061.md)

## 5. C v1 passes, C v2 fails (C v3 recovers)

9 eligible question(s).

**Pick: [gold-073](cases/gold-073.md)** (numeric, multi-hop, recipe `cross_year_table`)

> By how many percentage points did NVIDIA's gross margin increase from fiscal year 2016 to fiscal year 2022?

Gold answer: 8.8 percentage points

| System | Correct | Hops | Latency s | Answer (start) |
|---|---|---|---|---|
| A | no | 1 | 3.4 | The provided context gives NVIDIA’s gross margin for fiscal year 2022 as **64.9%** [5], but it does **not** provide NVIDIA’s overall gross margin for fiscal year 2016. Chunk [2] discusses the **GPU business gross margin… |
| B | no | 1 | 8.0 | The question asks for NVIDIA’s gross margin increase from fiscal year 2016 to fiscal year 2022. - Fiscal year 2022 gross margin: 64.9% [5][7] - Fiscal year 2016 gross margin: not provided in the supplied passages Calcul… |
| C v1 | yes | 2 | 14.8 | NVIDIA's gross margin increased from 56.1% in fiscal year 2016 to 64.9% in fiscal year 2022, an increase of 8.8 percentage points [NVDA FY2016, Item 7, NVDA_FY2016_2016-01-31:160] [NVDA FY2022, Item 7, NVDA_FY2022_2022-… |
| C v2 | no | 1 | 15.7 | NVIDIA’s gross margin was 56.1% in fiscal year 2016. [NVDA FY2016, Item 7, NVDA_FY2016_2016-01-31:123] The provided evidence does not disclose NVIDIA’s overall gross margin percentage for fiscal year 2022; it only state… |
| C v3 | yes | 2 | 11.5 | NVIDIA's gross margin increased from 56.1% in fiscal year 2016 to 64.9% in fiscal year 2022, an increase of 8.8 percentage points [NVDA FY2016, Item 7, NVDA_FY2016_2016-01-31:160] [NVDA FY2022, Item 7, NVDA_FY2022_2022-… |

Alternates: [gold-003](cases/gold-003.md), [gold-010](cases/gold-010.md)
