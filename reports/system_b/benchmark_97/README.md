# System B · Evaluation summary

[Read all 97 questions, answers and references](system_b_97_answers.md)

All 97 questions have a fresh answer from Groq `openai/gpt-oss-120b`. System B searched the shared Supabase corpus with dense retrieval and BM25, reranked the candidates, and returned five passages per question.

## RQ1 · Did the passages contain the evidence?

| Measure | Result |
|---|---:|
| Complete reference quotes found in the cited filing | 129/204 (63.2%) |
| Mean evidence recall under the team’s partial-match rule | 73.47% |
| Questions with all evidence under that rule | 60/97 (61.86%) |
| Document recall | 96.91% |
| Context precision | 35.88% |
| Mean reciprocal rank of the first matching passage | 0.66 |
| Multi-hop evidence recall / full discovery | 70.85% / 56.41% |
| Cross-section discovery rate | 40.91% |

The strict measure counts whole quotes across the benchmark. The team measure allows partial wording matches and averages recall per question.

## Answer quality and RQ2 · Did the answers use the evidence?

| Measure | Result |
|---|---:|
| Questions with all expected numbers matched | 24/63 (38.1%) |
| Answers consisting entirely of the standard abstention | 33/97 |
| Answers with a recognized citation | 52/97 |
| Answers with out-of-range numeric citation labels | 0/97 |
| Mean section citation precision / F1 | 91.2% / 90.5% on 51 scorable answers |
| Dollar or percentage mentions without an exact evidence match | 84/132 (63.6%) across 38 answers containing explicit figures |
| Mean word-overlap F1 with the reference answer | 0.232 |

Citation precision and F1 measure agreement with the expected filing sections. The exact-number check looks for the same unit and value in any retrieved passage. A valid calculation can therefore be flagged, and a matching value alone cannot verify a claim. System B supplied no native guardrail reports.

**RAGAS faithfulness snapshot (2026-10-31 16:04 SGT).** 12 of 97 answers had a saved, successful judge score at export. The mean for those 12 was 0.583. Coverage at export limits interpretation of this figure.

## Run details

| Measure | Result |
|---|---:|
| Completed / failed | 97 / 0 |
| Median / 90th percentile latency | 33.2 s / 36.7 s |
| Total reported generation tokens | 142,518 |

Benchmark and retrieval code: [team evaluation snapshot](https://github.com/AmandaTSY99/cs614_group8/tree/ae3da3a).
