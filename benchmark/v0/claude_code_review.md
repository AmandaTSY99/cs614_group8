# Claude Code review of benchmark/parts/amanda.jsonl

Reviewed all 100 QAs against their source filings. 48 were modified; the corrected versions are in `benchmark/claude_code.jsonl` (same ids and format). The other 52 were checked and left unchanged.

Every quote in the corrected QAs was found word for word in its filing, and every numeric answer was re-checked against its program. This was an LLM review, so a human spot-check of about 10 corrected QAs is still recommended.

## Problems found

| Problem | Count | Examples |
|---|---|---|
| Wrong arithmetic: the answer doesn't match its own program | 15 | 026 said 539.27%, but it's 537.97%. 087 said 353.87%, but it's 355.77% |
| Wrong value or entity | 4 | 011 counted Sam's Clubs but asked about all Walmart stores. 045 used Apple's 2015 column as 2016. 030 compared share counts across Amazon's 2022 stock split. 002 divided by a negative credit line |
| Answer messed up | 6 | 072 includes the writer model's own reasoning ("Wait, let me look closer…"). 069 is garbled. 053 asks about "the other executive" but it's the same person |
| Question gives the answer away | 3 | 031, 036 and 098 state the figures in the question itself |
| Trivial or forced question | 6 | 066 and 075 only "found" a punctuation change or a reordered list. 074 and 079 compare unrelated passages |
| Rounding, units, incomplete answers, missing evidence | 14 | "13.00%" should be "13 percentage points". Mixed answers that gave only the number |

Corrected QAs keep their id and topic, with evidence quotes updated to match. Wherever possible a QA was fixed rather than replaced.

## Script bug (fixed)

`validate()` in `build_benchmark_qa.py` accepted an answer within **1%** of the program's result. All 15 arithmetic errors got past this check. The tolerance is now tightened to allow only rounding differences (`0.0001 * stated + 0.006`). Re-checking all 100 original QAs with the tighter test, the only failures were QAs already corrected here.

## Causes worth fixing before generating more QAs (not yet fixed)

1. **The parser keeps only the last heading above a table.** When several headings are stacked, the parent heading is lost and the writer sees no context. That's how 011 lost "SAM'S CLUB SEGMENT" and was asked about all Walmart stores. Fix: keep consecutive headings together (e.g. "SAM'S CLUB SEGMENT > CLUB COUNT AND SQUARE FOOTAGE > ...").
2. **Cross-year text sections are matched on generic headings** such as "Part I", "PART II" or "Table of Contents". This paired unrelated passages and produced forced comparisons (074, 079). Fix: skip generic headings when matching sections across years.
3. **The prompt doesn't forbid putting the figures in the question** (031, 036, 098). Fix: add a rule to `SYSTEM_PROMPT` that the question must not state the numbers needed to answer it.

## Using these files

`claude_code.jsonl` is in `benchmark/`, not `benchmark/parts/`. If it were in `parts/`, `--merge` would see two versions of the same 48 questions and keep the old, wrong ones from `amanda.jsonl`. To build the final set, the 48 corrected QAs should replace the originals by id.

## Corrected QAs

| id | recipe | issue | what was wrong | old answer | new answer |
|---|---|---|---|---|---|
| amanda-002 | table | wrong/meaningless | Ratio divided total restructuring charges by the cost-of-revenue line, which is a net credit of $(47) million; the 73.45 ratio drops the sign and means nothing. Rewritten from the same table. | 73.45 | 57.76% |
| amanda-004 | table | answer format | A difference between two sales shares is in percentage points, not '13.00%'. | 13.00% | 13 percentage points |
| amanda-005 | table | rounding | Program gives -96.0467, which rounds to -96.05%, not -96.04%. | -96.04% | -96.05% |
| amanda-007 | table | question quality | Question referred to 'the table' (against the writer's rules); answer had 3 decimals. | 53.298% | 53.30% |
| amanda-011 | table | wrong entity | The table is the SAM'S CLUB SEGMENT club count (heading two lines above the table), not total Walmart stores. The writer only saw the last heading. | 12.57% | 12.57% |
| amanda-016 | table | wrong answer | Program gives 40.00; answer said 39.78% (passed the old 1% tolerance). | 39.78% | 40.00% |
| amanda-021 | table | answer format | Difference between two shares is in percentage points, not '31.00%'. | 31.00% | 31 percentage points |
| amanda-024 | table | wrong answer | (367,630 - 284,071) / 284,071 = 29.41%; answer said 29.65%. | 29.65% | 29.41% |
| amanda-026 | cross_year_table | wrong answer | (75,076 - 11,768) / 11,768 = 537.97%; answer said 539.27%. | 539.27% | 537.97% |
| amanda-028 | cross_year_table | wrong answer | (3,502 - 824.2) / 824.2 = 324.90%; answer said 325.16%. | 325.16% | 324.90% |
| amanda-029 | cross_year_table | wrong answer | (1,771.5 - 1,245.0) / 1,245.0 = 42.29%; answer said 42.35%. | 42.35% | 42.29% |
| amanda-030 | cross_year_table | misleading comparison | Compared raw share counts across Amazon's 2022 20-for-1 stock split (13 million pre-split vs 248 million post-split), so '1807.69%' is meaningless. Rewritten as a share of basic shares. | 1807.69% | -0.30 percentage points (from about 2.67% in 2018 to about 2.37% in 2024) |
| amanda-031 | cross_year_table | answer leaked | Question stated both VAR figures, so no retrieval was needed. | 81.36% | 81.36% |
| amanda-033 | cross_year_table | wrong answer | (4,115 - 1,185) / 1,185 = 247.26%; answer said 247.68%. | 247.68% | 247.26% |
| amanda-034 | cross_year_table | answer format | Answer '2.5' had no unit. | 2.5 | 2.5 percentage points |
| amanda-035 | cross_year_table | wrong answer | (3,615 - 6,150) / 6,150 = -41.22%; answer said -41.26%. | -41.26% | -41.22% |
| amanda-036 | cross_year_table | wrong answer + leak | (738,494 - 114,636) / 114,636 = 544.21%; answer said 545.18%. Question also stated the 2013 value. | 545.18% | 544.21% |
| amanda-039 | cross_year_table | wrong answer | (13,118 - 1,512) / 1,512 = 767.59%; answer said 768.52%. | 768.52% | 767.59% |
| amanda-041 | cross_year_table | question quality | Asked how much FY2014 'exceeded' FY2008, but the rate fell; answer '-5.10%' should be percentage points. | -5.10% | -5.1 percentage points (from 25.8% in fiscal 2008 to 20.7% in fiscal 2014) |
| amanda-043 | cross_year_table | wrong answer | (43,884 - 28,833) / 28,833 = 52.20%; answer said 52.40%. | 52.40% | 52.20% |
| amanda-044 | cross_year_table | wrong answer | (4,591 - 636) / 636 = 621.86%; answer said 620.28%. Question also spelled out the formula. | 620.28% | 621.86% |
| amanda-045 | cross_year_table | wrong source value | $21,120 million is the September 2015 column (prior-year table in the FY2016 10-K). The FY2016 value is $20,484 million. | $11,305 million | $10,669 million |
| amanda-049 | text | question quality | Called Microsoft Research a 'subsidiary'; the filing calls it a research organization. Answer missed the segment-level funding detail. | Microsoft funds research at the corporate level to look beyond immediate product… | Microsoft funds research at the corporate level to look beyond immediate product… |
| amanda-053 | text | wrong premise | Asked which 'other executive' sits on Netflix's board, but it is the same person (Mr. Smith). | Mr. Smith was appointed Executive Vice President, General Counsel, and Secretary… | Mr. Smith. He was appointed Executive Vice President, General Counsel, and Secre… |
| amanda-058 | text | answer quality | Answer read as if the FY2010 charges caused the FY2011 decrease; the decrease came from those charges not recurring. | The primary driver for the decrease in research and development expenses was sto… | The decrease was mainly because fiscal 2010 had included $90.5 million of stock-… |
| amanda-061 | text | answer inaccurate | Implied APB 25 was the reason for not acting on the shareholder proposal; the filing says Apple was waiting for the FASB's final standard. | Apple Inc. cited APB Opinion No. 25 as the basis for not expensing the value of … | Apple measured stock-based compensation under APB Opinion No. 25 (the intrinsic … |
| amanda-066 | cross_year_text | trivial question | Only 'change' found was a slash in a line-item label ('income/(expense)' vs 'income (expense)'). Rewritten to ask about the accounting approach itself. | In the 2014 filing, realized gains or losses were recorded as 'interest and othe… | The approach did not change. In both years Meta carried available-for-sale marke… |
| amanda-069 | cross_year_text | garbled answer | Answer said portables 'remained stable at 62% (up from 62% in 2007, though the 2003 figure was lower at 42% of Mac systems)', mixing two different measures. | In fiscal year 2003, portable systems represented 42% of all Macintosh systems s… | In fiscal 2003, portable systems were 42% of all Macintosh systems sold (up from… |
| amanda-072 | cross_year_text | garbled answer | Answer contained the writer model's own reasoning ('Wait, let me look closer...') and wrongly claimed the returns factor changed. | Between fiscal year 2009 and 2012, Amazon modified the risk factor regarding int… | Fiscal 2012 broadened the Internet item from 'changes in usage of the Internet a… |
| amanda-074 | cross_year_text | contrived comparison | Compared two unrelated passages (paired only because both sit under a generic 'Part I' heading) and misdescribed the 2004 text. Rewritten as a two-part question each answered by its own filing. | In its 2010 10-K, JPMorgan Chase notes that regulatory changes, specifically the… | The 2010 10-K says the FDIC's final rule changing the deposit insurance assessme… |
| amanda-075 | cross_year_text | trivial question | Only 'change' was the order in which four line items are listed. Rewritten to ask about the rationale itself. | In its 2011 10-K, Amazon stated that if it did not pay out compensation in the f… | Amazon says stock-based compensation is non-cash and excluded from its internal … |
| amanda-076 | cross_year_text | question quality + missing evidence | Question implied both topics come from both years; the 'increases to common stock' key point had no supporting quote. | For employee equity awards, Apple recognized net excess tax benefits as increase… | FY2013: for stock options, Apple received an income tax benefit equal to the tax… |
| amanda-077 | cross_year_text | ungrounded claim | Said Google Capital 'corresponds to' CapitalG; true in reality but not stated in either filing. | In fiscal year 2015, following the Alphabet reorganization, the 'Other Bets' seg… | In fiscal 2015 (after the Alphabet reorganization), Other Bets was described as … |
| amanda-079 | cross_year_text | contrived comparison + missing evidence | Framed two unrelated topics as an 'evolution'; the 1.6% gross-margin figure and the software-driver action had no supporting quote. | In fiscal year 2012, NVIDIA highlighted a specific product quality risk involvin… | In fiscal year 2012, NVIDIA highlighted a specific product quality risk involvin… |
| amanda-080 | cross_year_text | answer inaccurate | Said Tesla's vehicles had been observed to catch fire (the filing says lithium-ion cells in general, and says so in both years); one evidence quote was about financial guidance. | In 2011, Tesla described its business as having 'limited field experience' with … | In fiscal 2011, Tesla said it had delivered only a limited number of Roadsters a… |
| amanda-081 | table_text | rounding + terse answer | 3.895% rounds to 3.90%, not 3.89%; answer was only a fragment. | 3.89%; multi-year commitments to product development | 3.90%. NVIDIA says its research and development expenses reflect multi-year comm… |
| amanda-082 | table_text | incomplete answer | Answer gave only the number, not the qualitative part the question asks for. | 40.93% | 40.93% decrease (from $623 million to $368 million). Meta lists valuation of lon… |
| amanda-083 | table_text | wrong answer | (8,471 - 5,962) / 5,962 = 42.08%; answer said 42.27%. | 42.27%; The company states that if it fails to stock or restock popular products… | 42.08%. Amazon says that if it does not stock or restock popular products in suf… |
| amanda-084 | table_text | meaningless ratio + rounding | Divided a $33 million derivative loss by a $497 million hypothetical FX sensitivity, which isn't a meaningful measure; 0.0664 also rounds to 0.07, not 0.06. Rewritten from the same table and text. | 0.06 | $1,131 million, from a $413 million loss in 2019 to a $718 million gain in 2020.… |
| amanda-085 | table_text | terse answer | Answer was only '16.82%, GPUs, servers'. | 16.82%, GPUs, servers | 16.82%. Microsoft says its datacenters depend on the availability of permitted a… |
| amanda-087 | table_text | wrong answer + incomplete | (24,233 - 5,317) / 5,317 = 355.77%; answer said 353.87% and omitted the qualitative part. | 353.87% | 355.77%. Meta says its future income tax rates could be volatile and difficult t… |
| amanda-089 | table_text | wrong answer | (83,850 - 62,209) / 62,209 = 34.79%; answer said 34.63%. | 34.63%; Net income of $53.4 billion, non-cash adjustments of $16.2 billion, and … | 34.79%. Apple's 2015 operating cash flow of $81.3 billion resulted from $53.4 bi… |
| amanda-091 | table_text | evidence cut off | Evidence quote stopped mid-word ('multi-') at a page break; replaced with the complete sentence from the same filing. | The absolute increase was $975 million. NVIDIA describes its Tegra brand as inte… | $975 million. NVIDIA says its Tegra brand integrates an entire computer onto a s… |
| amanda-093 | table_text | wrong answer | (4,265 - 2,105) / 2,105 = 102.61%; answer said 102.66%. | 102.66%; increase in net income, excluding non-cash charges such as depreciation… | 102.61%. Amazon said the increase in operating cash flow in 2017 was primarily d… |
| amanda-094 | table_text | missing evidence | Answer was right, but no quote supported the $15.93 billion charge. | $17,171 million; One Big Beautiful Bill Act (OBBBA) | $17,171 million. The $15.93 billion charge in the third quarter of 2025 resulted… |
| amanda-097 | table_text | rounding + overclaim | 173.643% rounds to 173.64%; the answer claimed a link between Asia-Pacific growth and the store plans that the filing doesn't make. | The Asia-Pacific segment's net sales grew by approximately 173.63% from 2010 to … | 173.64% (from $8,256 million to $22,592 million). Apple expected to open about 4… |
| amanda-098 | table_text | answer leaked | Question stated both deferred tax figures. | The magnitude of the swing in the net deferred tax position is $843 million. The… | $843 million, from a net deferred tax asset of $153 million to a net deferred ta… |
| amanda-099 | table_text | incomplete answer | Answer gave only the number; question asked for 'specific text', which is awkward for a benchmark. | 247.63% | 247.63%. Apple says it designs, develops, and markets a line of portable digital… |
