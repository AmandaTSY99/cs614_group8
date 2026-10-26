# Review: 40 QAs kept from benchmark_qa_0 (FY2015 onwards)

Source file: `benchmark/parts/kept_fy2015.jsonl` (ids `v0-<old id>`, so each maps back to `benchmark_qa_0.jsonl`).
Fix a QA by editing that file directly, or tick a box and add a note here and ask Claude to apply it.
A QA marked *corrected in v0 review* was already fixed once (see `benchmark/v0/claude_code_review.md`).

Check for each QA: the question stands alone (company + year named), the answer is right and follows from the
evidence, the evidence quotes are the right rows/sentences, and the question doesn't give the answer away.

| Recipe | Kept | Target in v1 | Still to generate |
|---|---|---|---|
| table | 10 | 20 | 10 |
| text | 8 | 15 | 7 |
| table_text | 12 | 20 | 8 |
| cross_year_table | 6 | 20 | 14 |
| cross_year_text | 4 | 15 | 11 |
| cross_company_table | 0 | 5 | 5 |
| cross_company_text | 0 | 5 | 5 |
| **Total** | **40** | **100** | **60** |

---

## v0-amanda-001  ·  table  ·  numeric  ·  single-hop  ·  JNJ FY2022

**Q:** For Johnson & Johnson's fiscal year 2022, calculate the year-over-year percentage decrease in the accumulated benefit obligation for plans with accumulated benefit obligations in excess of plan assets.

**A:** -25.64%

**Program:** `subtract(2.9, 3.9), divide(#0, 3.9)` → -0.2564

**Evidence:**
- `JNJ_FY2022_2023-01-01` · Item 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > 10.Pensions and Other Benefit Plans (text)
  > Plans with accumulated benefit obligations in excess of plan assets have an accumulated benefit obligation, projected benefit obligation and plan assets of $2.9 billion, $2.9 billion and $0.3 billion, respectively, at the end of 2022, and $3.9 billion, $4.2 billion and $0.3 billion, respectively, at the end of 2021.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-002  ·  table  ·  numeric  ·  multi-hop  ·  META FY2023  ·  *corrected in v0 review*

**Q:** What percentage of Meta Platforms' total restructuring charges for 2023 was recorded under research and development?

**A:** 57.76%

**Program:** `divide(1994, 3452)` → 0.5776

**Evidence:**
- `META_FY2023_2023-12-31` · Item 7.Management's Discussion and Analysis of Financial Con > Restructuring (table)
  > | Research and development | 1,581 | 413 | — | 1,994 |
- `META_FY2023_2023-12-31` · Item 7.Management's Discussion and Analysis of Financial Con > Restructuring (table)
  > | Total | $2,506 | $1,170 | $(224) | $3,452 |

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-005  ·  table  ·  numeric  ·  single-hop  ·  MSFT FY2016  ·  *corrected in v0 review*

**Q:** What was the percentage decrease in Microsoft's long-lived assets held in Finland from fiscal year 2014 to fiscal year 2016?

**A:** -96.05%

**Program:** `subtract(389, 9840), divide(#0, 9840), multiply(#1, 100)` → -96.0467

**Evidence:**
- `MSFT_FY2016_2016-06-30` · Item 8 > PART II (table)
  > Finland | 389 | 1,757 | 9,840 |
- `MSFT_FY2016_2016-06-30` · Item 8 > PART II (table)
  > June 30, | 2016 | 2015 | 2014 |

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-006  ·  table  ·  numeric  ·  multi-hop  ·  AAPL FY2019

**Q:** What is the ratio of Apple Inc.'s interest expense to its interest and dividend income for fiscal year 2019?

**A:** 0.72

**Program:** `divide(3576, 4961)` → 0.7208

**Evidence:**
- `AAPL_FY2019_2019-09-28` · Item 7. Management’s Discussion and Analysis of Financial Co > Other Income/(Expense), Net (table)
  > | Interest and dividend income | $4,961 |  | $5,686 |  | $5,201 |
- `AAPL_FY2019_2019-09-28` · Item 7. Management’s Discussion and Analysis of Financial Co > Other Income/(Expense), Net (table)
  > | Interest expense | (3,576) |  | (3,240) |  | (2,323) |

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-009  ·  table  ·  numeric  ·  single-hop  ·  AAPL FY2024

**Q:** What was the year-over-year percentage change in the weighted-average interest rate of Apple Inc.'s commercial paper from fiscal year 2023 to fiscal year 2024?

**A:** -5.30%

**Program:** `subtract(5.00, 5.28), divide(#0, 5.28), multiply(#1, 100)` → -5.3030

**Evidence:**
- `AAPL_FY2024_2024-09-28` · Item 8. Financial Statements and Supplementary Data > Commercial Paper (text)
  > The weighted-average interest rate of the Company’s commercial paper was 5.00% and 5.28% as of September 28, 2024 and September 30, 2023, respectively.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-010  ·  table  ·  numeric  ·  multi-hop  ·  AMZN FY2016

**Q:** What is the percentage of Amazon.com's total future principal payments due after 2021 relative to the total future principal payments due in 2017, based on the data provided in the 10-K for fiscal year 2016?

**A:** 497.16%

**Program:** `divide(5250, 1056), multiply(#0, 100)` → 497.1591

**Evidence:**
- `AMZN_FY2016_2016-12-31` · Item 8. Financial Statements and Supplementary Data > Note 5—LONG-TERM DEBT (table)
  > | Thereafter | 5,250 |
- `AMZN_FY2016_2016-12-31` · Item 8. Financial Statements and Supplementary Data > Note 5—LONG-TERM DEBT (table)
  > | 2017 | $1,056 |

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-013  ·  table  ·  numeric  ·  single-hop  ·  WMT FY2025

**Q:** By how many millions of dollars did Walmart Inc.'s net property and equipment increase from fiscal year 2024 to fiscal year 2025?

**A:** $9,183 million

**Program:** `subtract(119993, 110810)` → 9,183.0000

**Evidence:**
- `WMT_FY2025_2025-01-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Property and Equipment (table)
  > Property and equipment, net | | $119,993 | $110,810

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-021  ·  table  ·  numeric  ·  single-hop  ·  JPM FY2021  ·  *corrected in v0 review*

**Q:** For JPMorgan Chase & Co (JPM) in fiscal year 2021, what was the difference in percentage points between the proportion of total employees who were White and the proportion of senior level employees who were White?

**A:** 31 percentage points

**Program:** `subtract(77, 46)` → 31.0000

**Evidence:**
- `JPM_FY2021_2021-12-31` · Item 1. Business. > Human capital (table)
  > | White | 46% | 77% | 84% | 90% | |

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-023  ·  table  ·  numeric  ·  single-hop  ·  AAPL FY2019

**Q:** By what percentage did Apple's total shareholders' equity decrease from the fiscal year 2018 ending balance to the fiscal year 2019 ending balance?

**A:** -15.55%

**Program:** `subtract(90488, 107147), divide(#0, 107147), multiply(#1, 100)` → -15.5478

**Evidence:**
- `AAPL_FY2019_2019-09-28` · Item 8. Financial Statements and Supplementary Data > CONSOLIDATED STATEMENTS OF SHAREHOLDERS’ EQUITY (table)
  > | Total shareholders’ equity, ending balances | $90,488 | $107,147 | $134,047 |

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-024  ·  table  ·  numeric  ·  multi-hop  ·  WMT FY2015  ·  *corrected in v0 review*

**Q:** By what percentage did Walmart's total international segment retail square footage increase from fiscal year 2011 to fiscal year 2015?

**A:** 29.41%

**Program:** `subtract(367630, 284071), divide(#0, 284071), multiply(#1, 100)` → 29.4148

**Evidence:**
- `WMT_FY2015_2015-01-31` · ITEM 1. BUSINESS > UNIT COUNT(1) AND RETAIL SQUARE FEET(2) (table)
  > 2011 | 328 | 56,317 | 5 | 270 | 414 | 24,513 | 1,364 | 73,620 | 385 | 31,009 | 4,191 | 284,071
- `WMT_FY2015_2015-01-31` · ITEM 1. BUSINESS > UNIT COUNT(1) AND RETAIL SQUARE FEET(2) (table)
  > 2015 | 411 | 68,269 | 20 | 1,083 | 431 | 24,429 | 2,290 | 98,419 | 592 | 36,277 | 6,290 | 367,630

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-027  ·  cross_year_table  ·  numeric  ·  multi-hop  ·  MSFT FY2020

**Q:** What is the percentage decrease in Microsoft's total estimated future amortization expense for intangible assets from June 30, 2017, to June 30, 2020?

**A:** -30.36%

**Program:** `subtract(7038, 10106), divide(#0, 10106), multiply(#1, 100)` → -30.3582

**Evidence:**
- `MSFT_FY2020_2020-06-30` · Item 8 > PART II (table)
  > | Total | $7,038 |
- `MSFT_FY2017_2017-06-30` · Item 8 > PART II (table)
  > | Total | $10,106 |

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-030  ·  cross_year_table  ·  numeric  ·  multi-hop  ·  AMZN FY2024  ·  *corrected in v0 review*

**Q:** By how many percentage points did the dilutive effect of Amazon's outstanding stock awards, measured as a percentage of the shares used to compute basic earnings per share, change from fiscal year 2018 to fiscal year 2024?

**A:** -0.30 percentage points (from about 2.67% in 2018 to about 2.37% in 2024)

**Program:** `divide(248, 10473), divide(13, 487), subtract(#0, #1)` → -0.0030

**Evidence:**
- `AMZN_FY2024_2024-12-31` · Item 8. Financial Statements and Supplementary Data > Earnings Per Share (table)
  > | Total dilutive effect of outstanding stock awards | — | 188 | 248 |
- `AMZN_FY2024_2024-12-31` · Item 8. Financial Statements and Supplementary Data > Earnings Per Share (table)
  > | Shares used in computation of basic earnings per share | 10,189 | 10,304 | 10,473 |
- `AMZN_FY2018_2018-12-31` · Item 8. Financial Statements and Supplementary Data > Earnings per Share (table)
  > | Total dilutive effect of outstanding stock awards | 10 | 13 | 13 |
- `AMZN_FY2018_2018-12-31` · Item 8. Financial Statements and Supplementary Data > Earnings per Share (table)
  > | Shares used in computation of basic earnings per share | 474 | 480 | 487 |

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-032  ·  cross_year_table  ·  numeric  ·  multi-hop  ·  NVDA FY2021

**Q:** By what percentage did NVIDIA's net income per diluted share increase from the fiscal year ended January 28, 2018, to the fiscal year ended January 31, 2021?

**A:** 43.15%

**Program:** `subtract(6.90, 4.82), divide(#0, 4.82)` → 0.4315

**Evidence:**
- `NVDA_FY2021_2021-01-31` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CO > Fiscal Year 2021 Summary (table)
  > Net income per diluted share | $6.90 | $4.52 | Up 53%
- `NVDA_FY2018_2018-01-28` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CO > Fiscal Year 2018 Summary (table)
  > Net income per diluted share | $4.82 | $2.57 | Up 88%

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-034  ·  cross_year_table  ·  numeric  ·  multi-hop  ·  JNJ FY2021  ·  *corrected in v0 review*

**Q:** By how many percentage points did Johnson & Johnson's total research and development expense as a share of total sales increase from fiscal year 2018 to fiscal year 2021?

**A:** 2.5 percentage points

**Program:** `subtract(15.7, 13.2)` → 2.5000

**Evidence:**
- `JNJ_FY2021_2022-01-02` · Item 7.MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF OP > Research and Development Expense: (table)
  > Total research and development expense | $14,714 | 15.7% | $12,159 | 14.7%
- `JNJ_FY2018_2018-12-30` · Item 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF RESULTS OF O > Analysis of Consolidated Earnings Before Provision for Taxes on Income (table)
  > Total research and development expense | $10,775 | 13.2% | 10,594 | 13.9 | 9,143 | 12.7

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-035  ·  cross_year_table  ·  numeric  ·  multi-hop  ·  META FY2021  ·  *corrected in v0 review*

**Q:** Calculate the percentage change in Meta Platforms' foreign income before provision for income taxes from fiscal year 2016 to fiscal year 2021. Use the values in millions of dollars.

**A:** -41.22%

**Program:** `subtract(3615, 6150), divide(#0, 6150), multiply(#1, 100)` → -41.2195

**Evidence:**
- `META_FY2021_2021-12-31` · Item 8.Financial Statements and Supplementary Data > Note 14. Income Taxes (table)
  > Foreign | 3,615 | 8,947 | 19,495
- `META_FY2016_2016-12-31` · Item 8. Financial Statements and Supplementary Data > Share-based Compensation Plans (table)
  > Foreign | 6,150 | 3,392 | (8)

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-044  ·  cross_year_table  ·  numeric  ·  multi-hop  ·  META FY2022  ·  *corrected in v0 review*

**Q:** By what percentage did Meta Platforms' accrued compensation and benefits grow from December 31, 2016 to December 31, 2022?

**A:** 621.86%

**Program:** `subtract(4591, 636), divide(#0, 636)` → 6.2186

**Evidence:**
- `META_FY2022_2022-12-31` · Item 8.Financial Statements and Supplementary Data > Note 12. Liabilities (table)
  > Accrued compensation and benefits | 4,591 | 3,152
- `META_FY2016_2016-12-31` · Item 8. Financial Statements and Supplementary Data > Accounting Pronouncements Not Yet Adopted (table)
  > Accrued compensation and benefits | $636 | $473

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-046  ·  text  ·  qualitative  ·  single-hop  ·  META FY2024

**Q:** According to Meta Platforms, Inc.'s 2024 10-K, under what specific conditions does the company accrue a liability for legal and regulatory contingencies?

**A:** Meta accrues a liability when it believes that it is both probable that a loss has been incurred and the amount of the loss can be reasonably estimated.

**Key points:**
- The loss must be probable
- The amount of the loss must be reasonably estimable
- This applies to both asserted and unasserted matters

**Evidence:**
- `META_FY2024_2024-12-31` · Item 7.Management's Discussion and Analysis of Financial Con > Loss Contingencies (text)
  > With respect to these matters, asserted and unasserted, we evaluate the associated developments on a regular basis and accrue a liability when we believe that it is both probable that a loss has been incurred and the amount can be reasonably estimated.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-048  ·  text  ·  qualitative  ·  single-hop  ·  AMZN FY2025

**Q:** How does Amazon's seasonal retail demand pattern affect its cash and accounts payable balances as of December 31?

**A:** As of December 31, Amazon's cash, cash equivalents, and marketable securities balances typically reach their highest level because consumers primarily use credit cards in its stores and the related receivables settle quickly. Correspondingly, there is typically an increase in accounts payable due to inventory purchases and third-party seller sales.

**Key points:**
- Cash and marketable securities balances are at their highest level due to credit card usage and quick settlement.
- Accounts payable increases due to inventory purchases and third-party seller sales.

**Evidence:**
- `AMZN_FY2025_2025-12-31` · Item 1A. Risk Factors > The Variability in Our Retail Business Places Increased Strain on Our Operations (text)
  > As a result of holiday sales, as of December 31 of each year, our cash, cash equivalents, and marketable securities balances typically reach their highest level (other than as a result of cash flows provided by or used in investing and financing activities) because consumers primarily use credit cards in our stores and the related receivables settle quickly.
- `AMZN_FY2025_2025-12-31` · Item 1A. Risk Factors > The Variability in Our Retail Business Places Increased Strain on Our Operations (text)
  > Typically, there is also a corresponding increase in accounts payable as of December 31 due to inventory purchases and third-party seller sales.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-051  ·  text  ·  qualitative  ·  multi-hop  ·  META FY2016

**Q:** How did Meta Platforms' accounting policy for share-based compensation forfeitures change in Q4 2016, and how does this interact with the standard vesting period for its awards?

**A:** In Q4 2016, Meta Platforms elected to early adopt ASU 2016-09, changing its policy to account for forfeitures as they occur rather than estimating them. This change applies to awards, the majority of which are earned over a four-year service period.

**Key points:**
- Meta early adopted ASU 2016-09 in Q4 2016
- The policy change involved accounting for forfeitures as they occur instead of estimating them
- The majority of awards have a four-year service period

**Evidence:**
- `META_FY2016_2016-12-31` · Item 8. Financial Statements and Supplementary Data > Share-based Compensation (text)
  > In the fourth quarter of 2016, we elected to early adopt Accounting Standards Update No. 2016-09, Compensation-Stock Compensation (Topic 718): Improvement to Employee Share-based Payment Accounting (ASU 2016-09) issued by the Financial Accounting Standards Board (FASB), which among other items, provides an accounting policy election to account for forfeitures as they occur, rather than to account for them based on an estimate of expected forfeitures.
- `META_FY2016_2016-12-31` · Item 8. Financial Statements and Supplementary Data > Share-based Compensation (text)
  > The majority of our awards are earned over a service period of four years.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-053  ·  text  ·  qualitative  ·  multi-hop  ·  MSFT FY2015  ·  *corrected in v0 review*

**Q:** According to Microsoft's fiscal year 2015 10-K, which executive serves as both General Counsel and Chief Compliance Officer, and on which other company's board of directors does that executive serve?

**A:** Mr. Smith. He was appointed Executive Vice President, General Counsel, and Secretary in 2011 (after serving as Senior Vice President, General Counsel, and Secretary since November 2001), was named Chief Compliance Officer in 2002, and serves on the Board of Directors of Netflix, Inc.

**Key points:**
- Mr. Smith is Executive Vice President, General Counsel, and Secretary (since 2011).
- Mr. Smith was named Chief Compliance Officer in 2002.
- Mr. Smith serves on the Board of Directors of Netflix, Inc.

**Evidence:**
- `MSFT_FY2015_2015-06-30` · Item 1 > PART I (text)
  > Mr. Smith was appointed Executive Vice President, General Counsel, and Secretary in 2011.
- `MSFT_FY2015_2015-06-30` · Item 1 > PART I (text)
  > Mr. Smith was also named Chief Compliance Officer in 2002.
- `MSFT_FY2015_2015-06-30` · Item 1 > PART I (text)
  > Mr. Smith also serves on the Board of Directors of Netflix, Inc.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-056  ·  text  ·  qualitative  ·  single-hop  ·  WMT FY2025

**Q:** What factors drove the growth in Walmart U.S. comparable sales in fiscal 2025?

**A:** The growth was driven by an increase in transactions and unit volumes, with particularly strong sales in the grocery and health and wellness categories.

**Key points:**
- Growth in transactions
- Growth in unit volumes
- Strong sales in grocery
- Strong sales in health and wellness

**Evidence:**
- `WMT_FY2025_2025-01-31` · ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS OF FINANCIAL CO > Growth (text)
  > For fiscal 2025, comparable sales growth was driven by growth in transactions and unit volumes, with strong sales in grocery and health and wellness.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-062  ·  text  ·  qualitative  ·  single-hop  ·  MSFT FY2019

**Q:** According to Microsoft's fiscal year 2019 10-K, what valuation methodology does the company use for its Level 3 investments?

**A:** Microsoft values its Level 3 investments using internally-developed models with unobservable inputs.

**Key points:**
- Level 3 investments
- internally-developed models
- unobservable inputs

**Evidence:**
- `MSFT_FY2019_2019-06-30` · Item 7 > Valuation (text)
  > Level 3 investments are valued using internally-developed models with unobservable inputs.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-063  ·  text  ·  qualitative  ·  multi-hop  ·  AAPL FY2018

**Q:** According to Apple's 2018 10-K, how do the specific risks associated with the company's retail store operations differ from the general risks associated with its international operations?

**A:** The risks associated with Apple's retail stores are primarily operational and financial, stemming from the high cost structure of equipment, leasehold improvements, and leases, which can lead to significant termination costs and write-offs if sales decline or stores underperform. In contrast, the risks associated with international operations are regulatory and geopolitical, involving compliance with complex foreign laws (such as data privacy and anti-corruption), exposure to trade disputes, tariffs, and political instability, which can affect gross margins and brand reputation.

**Key points:**
- Retail store risks involve high fixed costs (equipment, leases) leading to potential write-offs and termination costs upon underperformance.
- International operation risks involve compliance with diverse foreign laws, regulations, and geopolitical factors like trade disputes.
- The retail risks are focused on operational/financial liabilities, while international risks focus on legal/regulatory compliance and market environment.

**Evidence:**
- `AAPL_FY2018_2018-09-29` · Item 1A. Risk Factors > The Company’s business is subject to the risks of international operations. (text)
  > Due to the high cost structure associated with the Company’s retail stores, a decline in sales or the closure or poor performance of individual or multiple stores could result in significant lease termination costs, write-offs of equipment and leasehold improvements and severance costs.
- `AAPL_FY2018_2018-09-29` · Item 1A. Risk Factors > The Company’s business is subject to the risks of international operations. (text)
  > Compliance with applicable U.S. and foreign laws and regulations, such as import and export requirements, anti-corruption laws, tax laws, foreign exchange controls and cash repatriation restrictions, data privacy and data localization requirements, environmental laws, labor laws and anti-competition regulations, increases the costs of doing business in foreign jurisdictions.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-065  ·  text  ·  qualitative  ·  multi-hop  ·  NVDA FY2015

**Q:** For NVIDIA's fiscal year 2015, what were the prior employers of Colette M. Kress and Ajay K. Puri immediately before they joined the company, and what specific roles did they hold at those companies?

**A:** Colette M. Kress previously served as Senior Vice President and Chief Financial Officer of the Business Technology and Operations Finance organization at Cisco Systems, Inc., and Ajay K. Puri held positions in sales, marketing, and general management at Sun Microsystems, Inc. before joining NVIDIA.

**Key points:**
- Colette M. Kress was previously at Cisco Systems, Inc.
- Kress served as Senior Vice President and CFO of the Business Technology and Operations Finance organization at Cisco
- Ajay K. Puri was previously at Sun Microsystems, Inc.
- Puri held positions in sales, marketing, and general management at Sun Microsystems

**Evidence:**
- `NVDA_FY2015_2015-01-25` · ITEM 1. BUSINESS > Table of Contents (text)
  > Prior to NVIDIA, Ms. Kress most recently served as Senior Vice President and Chief Financial Officer of the Business Technology and Operations Finance organization at Cisco Systems, Inc., a networking equipment company, since 2010.
- `NVDA_FY2015_2015-01-25` · ITEM 1. BUSINESS > Table of Contents (text)
  > Prior to NVIDIA, he held positions in sales, marketing, and general management over a 22-year career at Sun Microsystems, Inc., a computing systems company.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-071  ·  cross_year_text  ·  qualitative  ·  multi-hop  ·  TSLA FY2022

**Q:** How did Tesla's explanation for why recognizing its unrecognized tax benefits would not affect its effective tax rate evolve between fiscal year 2016 and fiscal year 2022, and what specific tax examinations are highlighted in the 2022 filing that were not mentioned in 2016?

**A:** In both fiscal years 2016 and 2022, Tesla explained that recognizing its unrecognized tax benefits would not affect its effective tax rate because the resulting tax benefits would increase a deferred tax asset that is fully offset by a valuation allowance. However, the 2022 filing specifically notes that the company is currently under examination by the IRS for the years 2015 to 2018, whereas the 2016 filing did not mention any current IRS examinations, only that tax years 2003 to 2015 remained subject to examination.

**Key points:**
- In both years, the lack of impact on the effective tax rate is due to the deferred tax asset being fully offset by a valuation allowance.
- The 2022 filing states Tesla is currently under IRS examination for 2015-2018.
- The 2016 filing states tax years 2003-2015 remain subject to federal examination but does not mention a current IRS examination.

**Evidence:**
- `TSLA_FY2022_2022-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Uncertain Tax Positions (text)
  > Unrecognized tax benefits of $572 million, if recognized, would not affect our effective tax rate since the tax benefits would increase a deferred tax asset that is currently fully offset by a valuation allowance.
- `TSLA_FY2022_2022-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Uncertain Tax Positions (text)
  > We are currently under examination by the Internal Revenue Service (“IRS”) for the years 2015 to 2018.
- `TSLA_FY2016_2016-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Uncertain Tax Positions (text)
  > As of December 31, 2016, unrecognized tax benefits of $198.3 million, if recognized, would not affect our effective tax rate as the tax benefits would increase a deferred tax asset which is currently fully offset with a full valuation allowance.
- `TSLA_FY2016_2016-12-31` · ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Uncertain Tax Positions (text)
  > Tax years 2003 to 2015 remain subject to examination for federal purposes, and tax years 2003 to 2015 remain subject to examination for California purposes.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-073  ·  cross_year_text  ·  qualitative  ·  multi-hop  ·  JPM FY2023

**Q:** How did JPMorgan Chase's 2023 10-K disclosure regarding the impact of market conditions on its wholesale businesses change in specificity compared to its 2018 disclosure, particularly regarding the types of capital markets activities explicitly identified as vulnerable to reduced profitability?

**A:** The 2023 10-K provides a more specific enumeration of capital markets activities vulnerable to reduced profitability under adverse market conditions, explicitly listing 'loan syndication, securities underwriting and leveraged lending activities.' In contrast, the 2018 10-K referred more generally to 'capital markets businesses' and 'capital markets transactions' without explicitly listing leveraged lending in that specific context of reduced profitability, though it did mention loan syndications and securities underwritings in the context of transaction volumes and disposal losses.

**Key points:**
- The 2023 disclosure explicitly includes 'leveraged lending activities' among the capital markets businesses vulnerable to reduced profitability.
- The 2018 disclosure refers to 'capital markets businesses' generally and lists 'loan syndications or securities underwritings' in the context of disposal losses but does not list leveraged lending in the same specific profitability clause.
- Both filings identify lower transaction volumes and reduced fee revenue as consequences of adverse market conditions.

**Evidence:**
- `JPM_FY2023_2023-12-31` · Item 1A. Risk Factors. > Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. (text)
  > the profitability of JPMorgan Chase’s businesses engaged in capital markets activities, including loan syndication, securities underwriting and leveraged lending activities, could be reduced
- `JPM_FY2018_2018-12-31` · Item 1A. Risk Factors. > Unfavorable market and economic conditions can have an adverse effect on JPMorgan Chase’s wholesale businesses. (text)
  > the profitability of JPMorgan Chase’s capital markets businesses could be reduced to the extent that those businesses: • earn less fee revenue due to lower transaction volumes, including when clients are unwilling or unable to refinance their outstanding debt obligations in unfavorable market conditions • dispose of portions of credit commitments, such as loan syndications or securities underwritings, at a loss

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-077  ·  cross_year_text  ·  qualitative  ·  multi-hop  ·  GOOGL FY2019  ·  *corrected in v0 review*

**Q:** How did the composition of Alphabet's 'Other Bets' segment change between fiscal year 2015 and fiscal year 2019, specifically regarding which distinct business units were explicitly named in each year's disclosure?

**A:** In fiscal 2015 (after the Alphabet reorganization), Other Bets was described as including Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X and other initiatives. In fiscal 2019, it was described as including Access, Calico, CapitalG, GV, Verily, Waymo and X, among others. Nest and Google Capital are no longer named in 2019, while CapitalG and Waymo are newly named.

**Key points:**
- 2015: Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital and X.
- 2019: Access, Calico, CapitalG, GV, Verily, Waymo and X.
- Nest and Google Capital are not named in 2019.
- CapitalG and Waymo are newly named in 2019.

**Evidence:**
- `GOOGL_FY2019_2019-12-31` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CO > Information about Segments (text)
  > Other Bets includes Access, Calico, CapitalG, GV, Verily, Waymo, and X, among others.
- `GOOGL_FY2015_2015-12-31` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CO > Information about Segments (text)
  > Other Bets includes businesses such as Access/Google Fiber, Calico, Nest, Verily, GV, Google Capital, X, and other initiatives.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-078  ·  cross_year_text  ·  qualitative  ·  multi-hop  ·  META FY2021

**Q:** How did Meta Platforms, Inc. expand the scope of its risk disclosures regarding privacy, safety, and content review efforts between its 2018 and 2021 fiscal year 10-K filings, specifically reflecting changes in its operational practices and external oversight mechanisms?

**A:** In its 2018 10-K, Meta disclosed costs related to its "safety, security, and content review efforts" without specific mention of voluntary practice changes or external oversight bodies. By the 2021 10-K, the company expanded this disclosure to include costs related to "privacy, safety, security, and content review efforts" and explicitly cited "implementing changes to our practices, whether voluntarily, in connection with laws, regulations, regulatory actions, or decisions or recommendations from the independent Oversight Board." This indicates a shift from general operational costs to a more detailed recognition of regulatory and independent governance influences on its cost structure.

**Key points:**
- The 2018 disclosure referred generally to costs for safety, security, and content review efforts.
- The 2021 disclosure added privacy to the list of cost drivers.
- The 2021 disclosure explicitly mentions implementing changes voluntarily or in response to regulations.
- The 2021 disclosure specifically cites decisions or recommendations from the independent Oversight Board as a factor in costs.

**Evidence:**
- `META_FY2021_2021-12-31` · Item 1A.Risk Factors > Our financial results will fluctuate from quarter to quarter and are difficult to predict. (text)
  > costs related to our privacy, safety, security, and content review efforts, including as a result of implementing changes to our practices, whether voluntarily, in connection with laws, regulations, regulatory actions, or decisions or recommendations from the independent Oversight Board, or otherwise;
- `META_FY2018_2018-12-31` · Item 1A. Risk Factors > Our financial results will fluctuate from quarter to quarter and are difficult to predict. (text)
  > costs related to our safety, security, and content review efforts;

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-081  ·  table_text  ·  mixed  ·  multi-hop  ·  NVDA FY2015  ·  *corrected in v0 review*

**Q:** Calculate the year-over-year percentage increase in NVIDIA's total operating expenses for fiscal year 2015 (ended January 25, 2015) compared to fiscal year 2014, and explain the specific structural characteristic of NVIDIA's research and development expenses cited in the 10-K that makes operating expenses less correlated with current revenue.

**A:** 3.90%. NVIDIA says its research and development expenses reflect multi-year commitments to developing new products and enhancements that will not result in revenue, if any, until future periods, so its operating expenses are largely independent of revenue in any particular period.

**Program:** `subtract(1840.5, 1771.5), divide(#0, 1771.5)` → 0.0390

**Key points:**
- Total operating expenses rose from $1,771.5 million to $1,840.5 million, an increase of 3.90%.
- R&D expenses reflect multi-year commitments to product development.
- These commitments do not result in revenue until future periods, if at all.

**Evidence:**
- `NVDA_FY2015_2015-01-25` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CO > Operating Expenses (table)
  > Total operating expenses | $1,840.5 | $1,771.5 | $69.0 | 4% | $1,771.5 | $1,578.1 | $193.4 | 12% |
- `NVDA_FY2015_2015-01-25` · ITEM 1A. RISK FACTORS > Table of Contents (text)
  > In particular, our research and development expenses reflect multi-year commitments to the development of new products and enhancements that will not result in revenue, if any, until future periods.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-082  ·  table_text  ·  mixed  ·  multi-hop  ·  META FY2021  ·  *corrected in v0 review*

**Q:** What is the percentage decrease in Meta Platforms, Inc.'s total finite-lived intangible assets net carrying amount from December 31, 2020 to December 31, 2021, and how does the company describe the materiality of the estimates associated with these assets in its critical accounting policies?

**A:** 40.93% decrease (from $623 million to $368 million). Meta lists valuation of long-lived assets, including goodwill, intangible assets and property and equipment and their estimated useful lives, among the assumptions and estimates with the greatest potential impact on its consolidated financial statements, so it treats them as critical accounting policies and estimates.

**Program:** `subtract(623, 368), divide(#0, 623), multiply(#1, 100)` → 40.9310

**Key points:**
- The net carrying amount of total finite-lived intangible assets decreased from $623 million in 2020 to $368 million in 2021.
- The percentage decrease is approximately 40.93%.
- The company identifies valuation of long-lived assets, including intangible assets, as a critical accounting policy due to the material impact of associated estimates and assumptions.

**Evidence:**
- `META_FY2021_2021-12-31` · Item 8.Financial Statements and Supplementary Data > Note 9.Goodwill and Intangible Assets (table)
  > | Total finite-lived assets |  | 5,116 | (4,748) | 368 | 5,018 | (4,395) | 623 |
- `META_FY2021_2021-12-31` · Item 7.Management's Discussion and Analysis of Financial Con > Critical Accounting Policies and Estimates (text)
  > We believe that the assumptions and estimates associated with gross vs. net in revenue recognition, valuation of equity investments, income taxes, loss contingencies, and valuation of long-lived assets including goodwill, intangible assets, and property and equipment, and their associated estimated useful lives, when applicable, have the greatest potential impact on our consolidated financial statements.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-084  ·  table_text  ·  mixed  ·  multi-hop  ·  GOOGL FY2020  ·  *corrected in v0 review*

**Q:** By how much did Alphabet's gains (losses) in other income (expense), net from foreign exchange contracts not designated as hedging instruments change from 2019 to 2020, and what does Alphabet say its foreign exchange forward contracts are used for?

**A:** $1,131 million, from a $413 million loss in 2019 to a $718 million gain in 2020. Alphabet uses foreign exchange forward contracts to offset the foreign exchange risk on assets and liabilities denominated in currencies other than the subsidiary's functional currency; the foreign currency gains and losses on those assets and liabilities are recorded in other income (expense), net and are offset by the gains and losses on the forward contracts.

**Program:** `subtract(718, -413)` → 1,131.0000

**Key points:**
- 2019: a $413 million loss on foreign exchange contracts not designated as hedging instruments.
- 2020: a $718 million gain.
- The change was $1,131 million.
- Forward contracts offset foreign exchange risk on assets and liabilities in non-functional currencies.
- Gains and losses on those assets and liabilities are recorded in other income (expense), net and offset by the forward contracts.

**Evidence:**
- `GOOGL_FY2020_2020-12-31` · ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Derivatives (table)
  > | Foreign exchange contracts | 0 | 54 | 0 | (413) | 0 | 718 |
- `GOOGL_FY2020_2020-12-31` · ITEM 7A.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKE > Foreign Currency Exchange Risk (text)
  > We use foreign exchange forward contracts to offset the foreign exchange risk on our assets and liabilities denominated in currencies other than the functional currency of the subsidiary.
- `GOOGL_FY2020_2020-12-31` · ITEM 7A.QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKE > Foreign Currency Exchange Risk (text)
  > The foreign currency gains and losses on the assets and liabilities are recorded in other income (expense), net, which are offset by the gains and losses on the forward contracts.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-085  ·  table_text  ·  mixed  ·  multi-hop  ·  MSFT FY2023  ·  *corrected in v0 review*

**Q:** For Microsoft's fiscal year 2023, calculate the percentage increase in operating lease cost compared to fiscal year 2022, and identify two specific types of infrastructure components or dependencies mentioned in the 10-K that contribute to the cost and complexity of maintaining the datacenter infrastructure driving these lease expenses.

**A:** 16.82%. Microsoft says its datacenters depend on the availability of permitted and buildable land, predictable energy, networking supplies, and servers, including graphics processing units (GPUs) and other components.

**Program:** `subtract(2875, 2461), divide(#0, 2461), multiply(#1, 100)` → 16.8224

**Key points:**
- The operating lease cost increased by 16.82% from FY2022 to FY2023.
- The answer must mention GPUs (or graphics processing units) as a dependency.
- The answer must mention servers as a dependency.

**Evidence:**
- `MSFT_FY2023_2023-06-30` · Item 8 > PART II (table)
  > Operating lease cost | $2,875 | $2,461 | $2,127
- `MSFT_FY2023_2023-06-30` · Item 1A > PART I (text)
  > Our datacenters depend on the availability of permitted and buildable land, predictable energy, networking supplies, and servers, including graphics processing units (“GPUs”) and other components.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-086  ·  table_text  ·  mixed  ·  multi-hop  ·  GOOGL FY2021

**Q:** For Alphabet Inc. in fiscal year 2021, what was the year-over-year change in the net carrying amount of 'Patents and developed technology' (in millions), and what does the company's risk factor disclosure identify as a consequence of acquisitions that could impact the financial condition or operating results related to such assets?

**A:** The net carrying amount decreased by $316 million, and the company notes that acquisitions could result in amortization expenses or impairment of goodwill and/or purchased long-lived assets.

**Program:** `subtract(674, 990)` → -316.0000

**Key points:**
- The net carrying amount of Patents and developed technology was $674 million in 2021
- The net carrying amount of Patents and developed technology was $990 million in 2020
- The change represents a decrease of $316 million
- Acquisitions can lead to amortization expenses or impairment of purchased long-lived assets

**Evidence:**
- `GOOGL_FY2021_2021-12-31` · ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Intangible Assets (table)
  > Patents and developed technology | $4,786 | $4,112 | $674
- `GOOGL_FY2021_2021-12-31` · ITEM 8.FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA > Other Intangible Assets (table)
  > Patents and developed technology | $4,639 | $3,649 | $990
- `GOOGL_FY2021_2021-12-31` · ITEM 1A.RISK FACTORS > Our operating results may fluctuate, which makes our results difficult to predict and could cause our results to fall short of expectations. (text)
  > Our acquisitions and other strategic transactions could also result in dilutive issuances of our equity securities, the incurrence of debt, contingent liabilities, or amortization expenses, or impairment of goodwill and/or purchased long-lived assets, and restructuring charges, any of which could harm our financial condition or operating results.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-087  ·  table_text  ·  mixed  ·  multi-hop  ·  META FY2020  ·  *corrected in v0 review*

**Q:** What was the year-over-year percentage change in Meta Platforms, Inc.'s domestic income before provision for income taxes from fiscal year 2019 to fiscal year 2020, and how does the company characterize the volatility and drivers of its future income tax rates in its risk factors?

**A:** 355.77%. Meta says its future income tax rates could be volatile and difficult to predict due to changes in jurisdictional profit split, changes in the amount and recognition of deferred tax assets and liabilities, or changes in tax laws, regulations, or accounting principles.

**Program:** `subtract(24233, 5317), divide(#0, 5317)` → 3.5576

**Key points:**
- Domestic income before provision for income taxes rose from $5,317 million to $24,233 million, an increase of 355.77%.
- Future income tax rates could be volatile and difficult to predict.
- Drivers include changes in jurisdictional profit split, deferred tax assets and liabilities, and tax laws, regulations or accounting principles.

**Evidence:**
- `META_FY2020_2020-12-31` · Item 8.Financial Statements and Supplementary Data > Note 15. Income Taxes (table)
  > | Domestic | $24,233 | $5,317 | $8,800 |
- `META_FY2020_2020-12-31` · Item 1A.Risk Factors > We may have exposure to greater than anticipated tax liabilities. (text)
  > Our future income tax rates could be volatile and difficult to predict due to changes in jurisdictional profit split, changes in the amount and recognition of deferred tax assets and liabilities, or by changes in tax laws, regulations, or accounting principles.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-089  ·  table_text  ·  mixed  ·  multi-hop  ·  AAPL FY2015  ·  *corrected in v0 review*

**Q:** For Apple Inc. in fiscal year 2015, calculate the percentage increase in segment operating income compared to fiscal year 2014, and identify the primary drivers of the cash generated from operating activities during 2015 as described in the Management's Discussion and Analysis.

**A:** 34.79%. Apple's 2015 operating cash flow of $81.3 billion resulted from $53.4 billion of net income, $16.2 billion of non-cash adjustments to net income, and an $11.7 billion increase in the net change in operating assets and liabilities.

**Program:** `subtract(83850, 62209), divide(#0, 62209)` → 0.3479

**Key points:**
- Segment operating income rose about 34.79% (from $62,209 million to $83,850 million).
- Net income of $53.4 billion was the main driver of operating cash flow.
- Non-cash adjustments contributed $16.2 billion.
- Changes in operating assets and liabilities contributed $11.7 billion.

**Evidence:**
- `AAPL_FY2015_2015-09-26` · Item 8. Financial Statements and Supplementary Data > Note 11 – Segment Information and Geographic Data (table)
  > | Segment operating income | $83,850 | $62,209 | $56,525 |
- `AAPL_FY2015_2015-09-26` · Item 7. Management’s Discussion and Analysis of Financial Co > Liquidity and Capital Resources (text)
  > During 2015, cash generated from operating activities of $81.3 billion was a result of $53.4 billion of net income, non-cash adjustments to net income of $16.2 billion and an increase in the net change in operating assets and liabilities of $11.7 billion.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-090  ·  table_text  ·  mixed  ·  multi-hop  ·  JNJ FY2025

**Q:** For Johnson & Johnson's fiscal year 2025, calculate the percentage change in the valuation allowance for continuing operations from 2024 to 2025. Additionally, identify the specific countries the company accounted for as having highly inflationary economic conditions in 2025.

**A:** The valuation allowance increased by 12.15%. The countries accounted for as having highly inflationary economic conditions are Argentina, Venezuela, Turkey, and Egypt.

**Program:** `subtract(1837, 1638), divide(#0, 1638), multiply(#1, 100)` → 12.1490

**Key points:**
- The valuation allowance for continuing operations ended at $1,837 million in 2025 and $1,638 million in 2024.
- The percentage change in the valuation allowance is 12.15%.
- Argentina, Venezuela, Turkey, and Egypt were accounted for as highly inflationary.

**Evidence:**
- `JNJ_FY2025_2025-12-28` · Item 8. Financial statements and supplementary data > 8. Income taxes (table)
  > | End of year | $1,837 | $1,638 |
- `JNJ_FY2025_2025-12-28` · Item 7. Management’s discussion and analysis of results of o > Economic and market factors (text)
  > The Company has accounted for operations in Argentina, Venezuela, Turkey and Egypt (beginning in the fiscal fourth quarter of 2024) as highly inflationary, as the prior three-year cumulative inflation rate surpassed 100%.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-091  ·  table_text  ·  mixed  ·  multi-hop  ·  NVDA FY2018  ·  *corrected in v0 review*

**Q:** What was the absolute increase in NVIDIA's Tegra Processor revenue, in millions of dollars, from fiscal year 2016 to fiscal year 2018, and how does the company's business description explain the strategic importance of the Tegra brand within its broader hardware ecosystem?

**A:** $975 million. NVIDIA says its Tegra brand integrates an entire computer onto a single chip and incorporates GPUs and multi-core CPUs to drive supercomputing for autonomous robots, drones and cars, as well as for consoles and mobile gaming and entertainment devices.

**Program:** `subtract(1534, 559)` → 975.0000

**Key points:**
- Tegra Processor revenue rose by $975 million, from $559 million in FY2016 to $1,534 million in FY2018.
- Tegra integrates an entire computer onto a single chip.
- Tegra incorporates GPUs and multi-core CPUs.
- It targets autonomous robots, drones and cars, as well as consoles and mobile gaming devices.

**Evidence:**
- `NVDA_FY2018_2018-01-28` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CO > Revenue by Reportable Segments (table)
  > | Tegra Processor | 1,534 | 824 | 710 | 86% | 824 | 559 | 265 | 47% |
- `NVDA_FY2018_2018-01-28` · ITEM 7. MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CO > Our Company and Our Businesses (text)
  > Our Tegra brand integrates an entire computer onto a single chip, and incorporates GPUs and multi-core CPUs to drive supercomputing for autonomous robots, drones, and cars, as well as for consoles and mobile gaming and entertainment devices.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-092  ·  table_text  ·  mixed  ·  multi-hop  ·  MSFT FY2018

**Q:** By how many millions of dollars did Microsoft's sales and marketing expenses increase in fiscal year 2018 compared to fiscal year 2017, and what does the company state about the nature of its ongoing investments in products and services during this period?

**A:** $2,008 million; The company states that it makes significant investments in new products and services that may not achieve expected returns, and that investments in new technology are speculative.

**Program:** `subtract(17469, 15461)` → 2,008.0000

**Key points:**
- The increase in sales and marketing expenses was $2,008 million.
- The company makes significant investments in new products and services.
- These investments may not achieve expected returns.
- Investments in new technology are described as speculative.

**Evidence:**
- `MSFT_FY2018_2018-06-30` · Item 7 > Sales and Marketing (table)
  > | Sales and marketing | $17,469 | $15,461 | $14,635 | 13% | 6% |
- `MSFT_FY2018_2018-06-30` · Item 1A > PART I (text)
  > We make significant investments in new products and services that may not achieve expected returns.
- `MSFT_FY2018_2018-06-30` · Item 1A > PART I (text)
  > Investments in new technology are speculative.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-093  ·  table_text  ·  mixed  ·  multi-hop  ·  AMZN FY2017  ·  *corrected in v0 review*

**Q:** For Amazon.com Inc. in fiscal year 2017, by what percentage did the cost or amortized cost of corporate debt securities increase from 2016 to 2017, and what did the company state was the primary driver for the increase in operating cash flow during 2017?

**A:** 102.61%. Amazon said the increase in operating cash flow in 2017 was primarily due to the increase in net income, excluding non-cash charges such as depreciation, amortization, and stock-based compensation.

**Program:** `subtract(4265, 2105), divide(#0, 2105)` → 1.0261

**Key points:**
- The cost of corporate debt securities rose from $2,105 million (2016) to $4,265 million (2017), an increase of 102.61%.
- The 2017 operating cash flow increase was primarily due to higher net income.
- That net income excludes non-cash charges such as depreciation, amortization and stock-based compensation.

**Evidence:**
- `AMZN_FY2017_2017-12-31` · Item 8. Financial Statements and Supplementary Data > Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES (table)
  > Corporate debt securities | 2,105 | 1 | (2) | 2,104
- `AMZN_FY2017_2017-12-31` · Item 8. Financial Statements and Supplementary Data > Note 2—CASH, CASH EQUIVALENTS, AND MARKETABLE SECURITIES (table)
  > Corporate debt securities | 4,265 | 1 | (9) | 4,257
- `AMZN_FY2017_2017-12-31` · Item 7. Management’s Discussion and Analysis of Financial Co > Liquidity and Capital Resources (text)
  > The increase in operating cash flow in 2017, compared to the comparable prior year period, was primarily due to the increase in net income, excluding non-cash charges such as depreciation, amortization, and stock-based compensation.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 

---

## v0-amanda-094  ·  table_text  ·  mixed  ·  multi-hop  ·  META FY2025  ·  *corrected in v0 review*

**Q:** For Meta Platforms, Inc. in fiscal year 2025, calculate the total increase in the provision for income taxes compared to 2024, and according to the Income Taxes note, what specific legislative act drove the $15.93 billion charge recorded in the third quarter of 2025?

**A:** $17,171 million. The $15.93 billion charge in the third quarter of 2025 resulted from the One Big Beautiful Bill Act (OBBBA), enacted in July 2025; $14.03 billion of it was a valuation allowance against Meta's U.S. federal deferred tax assets.

**Program:** `subtract(25474, 8303)` → 17,171.0000

**Key points:**
- The provision for income taxes increased by $17,171 million (from $8,303 million to $25,474 million).
- The $15.93 billion charge was driven by the One Big Beautiful Bill Act (OBBBA).
- $14.03 billion of the charge was a valuation allowance against U.S. federal deferred tax assets.

**Evidence:**
- `META_FY2025_2025-12-31` · Item 7.Management's Discussion and Analysis of Financial Con > Provision for income taxes (table)
  > | Provision for income taxes | $25,474 | $8,303 | $8,330 | 207% | —% |
- `META_FY2025_2025-12-31` · Item 8.Financial Statements and Supplementary Data > Note 14. Income Taxes (text)
  > As a result of the implementation of the One Big Beautiful Bill Act (OBBBA) enacted in July 2025, we expect to incur Corporate Alternative Minimum Tax (CAMT) beginning in 2025.
- `META_FY2025_2025-12-31` · Item 7.Management's Discussion and Analysis of Financial Con > Provision for income taxes (text)
  > We recorded a $15.93 billion charge in the third quarter of 2025, of which $14.03 billion was a valuation allowance against our U.S. federal deferred tax assets as of the enactment date of OBBBA, and the remaining was mostly related to the reduction of the benefit of the foreign-derived intangible income deduction.

**Verdict:** [ ] OK  [ ] Fix  [ ] Drop

**Notes:** 
