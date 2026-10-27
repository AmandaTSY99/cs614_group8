# RQ2 results

Judge: groq/openai/gpt-oss-120b. Cells: mean [bootstrap 95% CI] (n scored; na and failed rows excluded).

## Configuration

- RAGAS judge: groq/openai/gpt-oss-120b (`EVAL_JUDGE_PROVIDER` / `EVAL_JUDGE_MODEL`; one judge per scores file).
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
| faithfulness | 1.000 [1.000, 1.000] (n=2, failed=1) | 1.000 [1.000, 1.000] (n=1, failed=2) |
| answer_relevancy | 0.904 [0.890, 0.920] (n=3) | 0.920 [0.920, 0.920] (n=1, failed=2) |
| context_recall | 0.333 [0.000, 1.000] (n=3) | 1.000 [1.000, 1.000] (n=1, failed=2) |
| context_precision | N/A (n=0, na=0) | N/A (n=0, na=0) |
| factual_correctness | 0.590 [0.323, 1.000] (n=3) | N/A (n=0, na=0) |
| numeric_accuracy | 0.722 [0.556, 1.000] (n=3) | 0.833 [0.667, 1.000] (n=3) |
| citation_precision | 0.500 [0.000, 0.833] (n=3) | 0.500 [0.000, 0.833] (n=3) |
| citation_recall | 0.333 [0.000, 0.500] (n=3) | 0.333 [0.000, 0.500] (n=3) |
| citation_f1 | 0.389 [0.000, 0.611] (n=3) | 0.389 [0.000, 0.611] (n=3) |
| citation_coverage | 1.000 [1.000, 1.000] (n=3) | 1.000 [1.000, 1.000] (n=3) |
| grounding_error_rate | 0.000 [0.000, 0.000] (n=3) | 0.000 [0.000, 0.000] (n=3) |

## single_hop_factual

| Metric | system_c_v1 | system_c_v2 |
|---|---|---|
| faithfulness | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| answer_relevancy | 0.920 [0.920, 0.920] (n=1) | 0.920 [0.920, 0.920] (n=1) |
| context_recall | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| context_precision | N/A (n=0, na=0) | N/A (n=0, na=0) |
| factual_correctness | 1.000 [1.000, 1.000] (n=1) | N/A (n=0, na=0) |
| numeric_accuracy | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| citation_precision | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) |
| citation_recall | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) |
| citation_f1 | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) |
| citation_coverage | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| grounding_error_rate | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) |

## quantitative_tabular

| Metric | system_c_v1 | system_c_v2 |
|---|---|---|
| faithfulness | N/A (n=0, na=0) | N/A (n=0, na=0) |
| answer_relevancy | 0.911 [0.911, 0.911] (n=1) | N/A (n=0, na=0) |
| context_recall | 0.000 [0.000, 0.000] (n=1) | N/A (n=0, na=0) |
| context_precision | N/A (n=0, na=0) | N/A (n=0, na=0) |
| factual_correctness | 0.570 [0.570, 0.570] (n=1) | N/A (n=0, na=0) |
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
| faithfulness | 1.000 [1.000, 1.000] (n=1) | N/A (n=0, na=0) |
| answer_relevancy | 0.880 [0.880, 0.880] (n=1) | N/A (n=0, na=0) |
| context_recall | 0.000 [0.000, 0.000] (n=1) | N/A (n=0, na=0) |
| context_precision | N/A (n=0, na=0) | N/A (n=0, na=0) |
| factual_correctness | 0.200 [0.200, 0.200] (n=1) | N/A (n=0, na=0) |
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
| system_c_v1 | GOLD-01 | faithfulness | ok | 2 | 4587 | 848 |
| system_c_v1 | GOLD-01 | answer_relevancy | ok | 3 | 2280 | 612 |
| system_c_v1 | GOLD-01 | context_recall | ok | 13 | 4496 | 617 |
| system_c_v1 | GOLD-01 | context_precision | error | 26 | 8506 | 2685 |
| system_c_v1 | GOLD-01 | factual_correctness | ok | 25 | 7346 | 3450 |
| system_c_v1 | GOLD-21 | faithfulness | error | 23 | 7865 | 2618 |
| system_c_v1 | GOLD-21 | answer_relevancy | ok | 18 | 4794 | 732 |
| system_c_v1 | GOLD-21 | context_recall | ok | 16 | 5639 | 716 |
| system_c_v1 | GOLD-21 | context_precision | error | 29 | 13540 | 3464 |
| system_c_v1 | GOLD-21 | factual_correctness | ok | 21 | 5854 | 2838 |
| system_c_v1 | GOLD-56 | faithfulness | ok | 20 | 5669 | 2744 |
| system_c_v1 | GOLD-56 | answer_relevancy | ok | 4 | 2334 | 720 |
| system_c_v1 | GOLD-56 | context_recall | ok | 13 | 3539 | 720 |
| system_c_v1 | GOLD-56 | context_precision | error | 30 | 14655 | 3394 |
| system_c_v1 | GOLD-56 | factual_correctness | ok | 27 | 10385 | 6732 |
| system_c_v2 | GOLD-01 | faithfulness | ok | 20 | 6501 | 1534 |
| system_c_v2 | GOLD-01 | answer_relevancy | ok | 3 | 2280 | 599 |
| system_c_v2 | GOLD-01 | context_recall | ok | 13 | 4451 | 537 |
| system_c_v2 | GOLD-01 | context_precision | error | 28 | 11378 | 3798 |
| system_c_v2 | GOLD-01 | factual_correctness | error | 18 | 0 | 0 |
| system_c_v2 | GOLD-21 | faithfulness | error | 18 | 0 | 0 |
| system_c_v2 | GOLD-21 | answer_relevancy | error | 18 | 0 | 0 |
| system_c_v2 | GOLD-21 | context_recall | error | 18 | 0 | 0 |
| system_c_v2 | GOLD-21 | context_precision | error | 18 | 0 | 0 |
| system_c_v2 | GOLD-21 | factual_correctness | error | 19 | 675 | 458 |
| system_c_v2 | GOLD-56 | faithfulness | error | 18 | 0 | 0 |
| system_c_v2 | GOLD-56 | answer_relevancy | error | 18 | 0 | 0 |
| system_c_v2 | GOLD-56 | context_recall | error | 18 | 0 | 0 |
| system_c_v2 | GOLD-56 | context_precision | error | 18 | 0 | 0 |
| system_c_v2 | GOLD-56 | factual_correctness | error | 18 | 0 | 0 |

Latest rate-limit headers: `retry-after: 33`, `x-ratelimit-limit-requests: 1000`, `x-ratelimit-limit-tokens: 8000`, `x-ratelimit-remaining-requests: 906`, `x-ratelimit-remaining-tokens: 8000`, `x-ratelimit-reset-requests: 2h15m21.6s`, `x-ratelimit-reset-tokens: 1ms`

Estimate for 120 samples: 59.1 calls and 28,262 tokens per sample -> 7,090 calls, 3,391,500 tokens.
- Days by request/day limit: 7.09
- Days by token/day limit: 16.96
- Minutes of token/minute budget: 423.94
- Estimated days: 16.96

Projected judge cost for 120 samples at $0.15/M input and $0.6/M output tokens: 20,901 + 7,362 tokens per sample, $0.0076 per sample, $0.91 total (metrics measured: answer_relevancy, context_recall, factual_correctness, faithfulness).
