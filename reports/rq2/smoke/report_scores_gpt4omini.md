# RQ2 results

Judge: openai/gpt-4o-mini. Cells: mean [bootstrap 95% CI] (n scored; na and failed rows excluded).

## Configuration

- RAGAS judge: openai/gpt-4o-mini (`EVAL_JUDGE_PROVIDER` / `EVAL_JUDGE_MODEL`; one judge per scores file).
- Answer relevancy embeddings: local `BAAI/bge-small-en-v1.5` (sentence-transformers, CPU).
- Answer model(s): openai/gpt-4o-mini.
- System C's own guardrail judge: for the full run it is set to OpenAI `gpt-4o-mini` via env vars during generation (`GUARDRAIL_JUDGE_PROVIDER=openai`, `GUARDRAIL_JUDGE_MODEL=gpt-4o-mini`); the smoke run used the `.env` setting (Groq `openai/gpt-oss-120b`).

## Generation

| System | Records | Failed to generate |
|---|---|---|
| system_c_v1 | 3 | 0 |
| system_c_v2 | 3 | 0 |

## overall

| Metric | system_c_v1 | system_c_v2 |
|---|---|---|
| faithfulness | 0.722 [0.556, 1.000] (n=3) | 0.889 [0.778, 1.000] (n=3) |
| answer_relevancy | 0.635 [0.309, 0.978] (n=3) | 0.925 [0.892, 0.973] (n=3) |
| context_recall | 0.667 [0.444, 1.000] (n=3) | 0.722 [0.500, 1.000] (n=3) |
| context_precision | 0.245 [0.111, 0.375] (n=3) | 0.514 [0.125, 1.000] (n=3) |
| factual_correctness | 0.623 [0.357, 1.000] (n=3) | 0.573 [0.313, 1.000] (n=3) |
| numeric_accuracy | 0.722 [0.556, 1.000] (n=3) | 0.833 [0.667, 1.000] (n=3) |
| citation_precision | 0.833 [0.500, 1.000] (n=3) | 0.833 [0.500, 1.000] (n=3) |
| citation_recall | 0.667 [0.500, 1.000] (n=3) | 0.667 [0.500, 1.000] (n=3) |
| citation_f1 | 0.722 [0.500, 1.000] (n=3) | 0.722 [0.500, 1.000] (n=3) |
| citation_coverage | 1.000 [1.000, 1.000] (n=3) | 1.000 [1.000, 1.000] (n=3) |
| grounding_error_rate | 0.000 [0.000, 0.000] (n=3) | 0.000 [0.000, 0.000] (n=3) |

## single_hop_factual

| Metric | system_c_v1 | system_c_v2 |
|---|---|---|
| faithfulness | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| answer_relevancy | 0.928 [0.928, 0.928] (n=1) | 0.928 [0.928, 0.928] (n=1) |
| context_recall | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| context_precision | 0.125 [0.125, 0.125] (n=1) | 0.125 [0.125, 0.125] (n=1) |
| factual_correctness | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| numeric_accuracy | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| citation_precision | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| citation_recall | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| citation_f1 | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| citation_coverage | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| grounding_error_rate | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) |

## quantitative_tabular

| Metric | system_c_v1 | system_c_v2 |
|---|---|---|
| faithfulness | 0.667 [0.667, 0.667] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| answer_relevancy | 0.978 [0.978, 0.978] (n=1) | 0.973 [0.973, 0.973] (n=1) |
| context_recall | 0.667 [0.667, 0.667] (n=1) | 0.833 [0.833, 0.833] (n=1) |
| context_precision | 0.111 [0.111, 0.111] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| factual_correctness | 0.670 [0.670, 0.670] (n=1) | 0.500 [0.500, 0.500] (n=1) |
| numeric_accuracy | 0.667 [0.667, 0.667] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| citation_precision | 0.500 [0.500, 0.500] (n=1) | 0.500 [0.500, 0.500] (n=1) |
| citation_recall | 0.500 [0.500, 0.500] (n=1) | 0.500 [0.500, 0.500] (n=1) |
| citation_f1 | 0.500 [0.500, 0.500] (n=1) | 0.500 [0.500, 0.500] (n=1) |
| citation_coverage | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| grounding_error_rate | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) |

## cross_section_multihop

| Metric | system_c_v1 | system_c_v2 |
|---|---|---|

## multi_company_comparison

| Metric | system_c_v1 | system_c_v2 |
|---|---|---|
| faithfulness | 0.500 [0.500, 0.500] (n=1) | 0.667 [0.667, 0.667] (n=1) |
| answer_relevancy | 0.000 [0.000, 0.000] (n=1) | 0.874 [0.874, 0.874] (n=1) |
| context_recall | 0.333 [0.333, 0.333] (n=1) | 0.333 [0.333, 0.333] (n=1) |
| context_precision | 0.500 [0.500, 0.500] (n=1) | 0.417 [0.417, 0.417] (n=1) |
| factual_correctness | 0.200 [0.200, 0.200] (n=1) | 0.220 [0.220, 0.220] (n=1) |
| numeric_accuracy | 0.500 [0.500, 0.500] (n=1) | 0.500 [0.500, 0.500] (n=1) |
| citation_precision | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| citation_recall | 0.500 [0.500, 0.500] (n=1) | 0.500 [0.500, 0.500] (n=1) |
| citation_f1 | 0.667 [0.667, 0.667] (n=1) | 0.667 [0.667, 0.667] (n=1) |
| citation_coverage | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| grounding_error_rate | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) |

## Notes

- Context Precision is order-sensitive: it rewards relevant contexts ranked early. `retrieved_contexts` are kept in the order each system produced them (System C: retrieval order across hops, with v2's XBRL blocks first).
- Citation precision/recall/F1 are section-level (top-level 10-K item, `financials.csv` = any `[F-…]` citation), because the golden set has no gold chunk IDs. Answers with no citations are N/A, not 0; `citation_coverage` is the share of answers with at least one citation.
- Section aliases (a limitation of section-level matching): a cited `Item 15` chunk that is financial statements or notes counts as `Item 8`, and a cover-page chunk (no Item heading; registrant name, address, file number) counts as `Item 1`, matching how the golden set labels those facts.
- RAGAS metrics see the answer with citation tags stripped.

## Smoke test: judge usage

| System | Question | Metric | Status | Calls | Prompt tok | Completion tok |
|---|---|---|---|---|---|---|
| system_c_v1 | GOLD-01 | faithfulness | ok | 2 | 4407 | 203 |
| system_c_v1 | GOLD-01 | answer_relevancy | ok | 3 | 2010 | 93 |
| system_c_v1 | GOLD-01 | context_recall | ok | 1 | 4406 | 141 |
| system_c_v1 | GOLD-01 | context_precision | ok | 12 | 16194 | 776 |
| system_c_v1 | GOLD-01 | factual_correctness | ok | 4 | 3272 | 389 |
| system_c_v1 | GOLD-21 | faithfulness | ok | 2 | 5608 | 446 |
| system_c_v1 | GOLD-21 | answer_relevancy | ok | 3 | 2127 | 105 |
| system_c_v1 | GOLD-21 | context_recall | ok | 1 | 5549 | 317 |
| system_c_v1 | GOLD-21 | context_precision | ok | 12 | 17682 | 846 |
| system_c_v1 | GOLD-21 | factual_correctness | ok | 4 | 3533 | 970 |
| system_c_v1 | GOLD-56 | faithfulness | ok | 2 | 3438 | 351 |
| system_c_v1 | GOLD-56 | answer_relevancy | ok | 3 | 2064 | 93 |
| system_c_v1 | GOLD-56 | context_recall | ok | 1 | 3449 | 269 |
| system_c_v1 | GOLD-56 | context_precision | ok | 6 | 8886 | 468 |
| system_c_v1 | GOLD-56 | factual_correctness | ok | 4 | 3530 | 875 |
| system_c_v2 | GOLD-01 | faithfulness | ok | 2 | 4362 | 202 |
| system_c_v2 | GOLD-01 | answer_relevancy | ok | 3 | 2010 | 93 |
| system_c_v2 | GOLD-01 | context_recall | ok | 1 | 4361 | 125 |
| system_c_v2 | GOLD-01 | context_precision | ok | 12 | 16147 | 799 |
| system_c_v2 | GOLD-01 | factual_correctness | ok | 4 | 3272 | 388 |
| system_c_v2 | GOLD-21 | faithfulness | ok | 2 | 3934 | 532 |
| system_c_v2 | GOLD-21 | answer_relevancy | ok | 3 | 2133 | 102 |
| system_c_v2 | GOLD-21 | context_recall | ok | 1 | 3872 | 320 |
| system_c_v2 | GOLD-21 | context_precision | ok | 8 | 11405 | 580 |
| system_c_v2 | GOLD-21 | factual_correctness | ok | 4 | 3536 | 1085 |
| system_c_v2 | GOLD-56 | faithfulness | ok | 2 | 3661 | 271 |
| system_c_v2 | GOLD-56 | answer_relevancy | ok | 3 | 2034 | 93 |
| system_c_v2 | GOLD-56 | context_recall | ok | 1 | 3695 | 266 |
| system_c_v2 | GOLD-56 | context_precision | ok | 8 | 11514 | 618 |
| system_c_v2 | GOLD-56 | factual_correctness | ok | 4 | 3497 | 818 |

Latest rate-limit headers: `x-ratelimit-limit-requests: 30000`, `x-ratelimit-limit-tokens: 150000000`, `x-ratelimit-remaining-requests: 29999`, `x-ratelimit-remaining-tokens: 149998695`, `x-ratelimit-reset-requests: 2ms`, `x-ratelimit-reset-tokens: 0s`

Estimate for 120 samples: 19.7 calls and 29,704 tokens per sample -> 2,360 calls, 3,564,440 tokens.
- Days by request/day limit: 0.08
- Minutes of token/minute budget: 0.02
- Estimated days: 0.08

Projected judge cost for 120 samples at $0.15/M input and $0.6/M output tokens: 27,598 + 2,106 tokens per sample, $0.0054 per sample, $0.65 total (metrics measured: answer_relevancy, context_precision, context_recall, factual_correctness, faithfulness).
