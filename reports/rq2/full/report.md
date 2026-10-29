# RQ2 results

Judge: none (custom metrics only). Cells: mean [bootstrap 95% CI] (n scored; na and failed rows excluded).

## Configuration

- RAGAS judge: none (`EVAL_JUDGE_PROVIDER` / `EVAL_JUDGE_MODEL`; one judge per scores file).
- Answer relevancy embeddings: local `BAAI/bge-small-en-v1.5` (sentence-transformers, CPU).
- Answer model(s): openai/gpt-5.4, openai/gpt-5.4-2026-03-05.
- System C's own guardrail judge: for the full run it is set to OpenAI `gpt-4o-mini` via env vars during generation (`GUARDRAIL_JUDGE_PROVIDER=openai`, `GUARDRAIL_JUDGE_MODEL=gpt-4o-mini`); the smoke run used the `.env` setting (Groq `openai/gpt-oss-120b`).

## Generation

| System | Records | Failed to generate |
|---|---|---|
| system_a | 97 | 0 |
| system_b | 97 | 0 |
| system_c_v1 | 97 | 0 |
| system_c_v2 | 97 | 0 |

## overall

| Metric | system_a | system_b | system_c_v1 | system_c_v2 |
|---|---|---|---|---|
| numeric_accuracy | 0.587 [0.460, 0.714] (n=63) | 0.429 [0.302, 0.556] (n=63) | 0.730 [0.619, 0.841] (n=63) | 0.635 [0.508, 0.746] (n=63) |
| citation_precision | 0.890 [0.833, 0.944] (n=80) | 0.893 [0.843, 0.943] (n=67) | 0.854 [0.795, 0.902] (n=95) | 0.851 [0.793, 0.902] (n=94) |
| citation_recall | 0.912 [0.863, 0.956] (n=80) | 0.970 [0.940, 0.993] (n=67) | 0.905 [0.847, 0.953] (n=95) | 0.872 [0.814, 0.926] (n=94) |
| citation_f1 | 0.879 [0.829, 0.927] (n=80) | 0.907 [0.868, 0.943] (n=67) | 0.855 [0.803, 0.898] (n=95) | 0.841 [0.787, 0.889] (n=94) |
| citation_coverage | 0.835 [0.753, 0.907] (n=97) | 0.691 [0.598, 0.784] (n=97) | 0.979 [0.948, 1.000] (n=97) | 0.969 [0.938, 1.000] (n=97) |
| grounding_error_rate | N/A (n=0, na=97) | N/A (n=0, na=97) | 0.089 [0.042, 0.145] (n=97) | 0.063 [0.022, 0.110] (n=97) |

## single_hop_factual

| Metric | system_a | system_b | system_c_v1 | system_c_v2 |
|---|---|---|---|---|
| numeric_accuracy | N/A (n=0, na=8) | N/A (n=0, na=8) | N/A (n=0, na=8) | N/A (n=0, na=8) |
| citation_precision | 0.714 [0.429, 0.929] (n=7) | 0.750 [0.562, 0.938] (n=8) | 0.792 [0.583, 1.000] (n=8) | 0.812 [0.625, 0.938] (n=8) |
| citation_recall | 0.857 [0.571, 1.000] (n=7) | 1.000 [1.000, 1.000] (n=8) | 1.000 [1.000, 1.000] (n=8) | 1.000 [1.000, 1.000] (n=8) |
| citation_f1 | 0.762 [0.476, 0.952] (n=7) | 0.833 [0.708, 0.958] (n=8) | 0.854 [0.708, 1.000] (n=8) | 0.875 [0.750, 0.958] (n=8) |
| citation_coverage | 0.875 [0.625, 1.000] (n=8) | 1.000 [1.000, 1.000] (n=8) | 1.000 [1.000, 1.000] (n=8) | 1.000 [1.000, 1.000] (n=8) |
| grounding_error_rate | N/A (n=0, na=8) | N/A (n=0, na=8) | 0.000 [0.000, 0.000] (n=8) | 0.000 [0.000, 0.000] (n=8) |

## quantitative_tabular

| Metric | system_a | system_b | system_c_v1 | system_c_v2 |
|---|---|---|---|---|
| numeric_accuracy | 0.600 [0.400, 0.800] (n=20) | 0.500 [0.300, 0.700] (n=20) | 0.700 [0.500, 0.900] (n=20) | 0.600 [0.400, 0.800] (n=20) |
| citation_precision | 0.895 [0.763, 1.000] (n=19) | 0.933 [0.833, 1.000] (n=15) | 0.900 [0.775, 1.000] (n=20) | 0.868 [0.711, 1.000] (n=19) |
| citation_recall | 0.947 [0.842, 1.000] (n=19) | 1.000 [1.000, 1.000] (n=15) | 0.950 [0.850, 1.000] (n=20) | 0.895 [0.737, 1.000] (n=19) |
| citation_f1 | 0.912 [0.789, 1.000] (n=19) | 0.956 [0.889, 1.000] (n=15) | 0.917 [0.800, 1.000] (n=20) | 0.877 [0.719, 1.000] (n=19) |
| citation_coverage | 0.950 [0.850, 1.000] (n=20) | 0.750 [0.550, 0.900] (n=20) | 1.000 [1.000, 1.000] (n=20) | 0.950 [0.850, 1.000] (n=20) |
| grounding_error_rate | N/A (n=0, na=20) | N/A (n=0, na=20) | 0.117 [0.000, 0.267] (n=20) | 0.117 [0.000, 0.267] (n=20) |

## cross_section_multihop

| Metric | system_a | system_b | system_c_v1 | system_c_v2 |
|---|---|---|---|---|
| numeric_accuracy | 0.667 [0.458, 0.833] (n=24) | 0.375 [0.208, 0.583] (n=24) | 0.792 [0.625, 0.958] (n=24) | 0.667 [0.458, 0.833] (n=24) |
| citation_precision | 0.898 [0.817, 0.968] (n=31) | 0.917 [0.833, 0.986] (n=24) | 0.847 [0.759, 0.931] (n=36) | 0.889 [0.819, 0.949] (n=36) |
| citation_recall | 0.855 [0.774, 0.935] (n=31) | 0.938 [0.854, 1.000] (n=24) | 0.847 [0.750, 0.931] (n=36) | 0.847 [0.778, 0.917] (n=36) |
| citation_f1 | 0.844 [0.780, 0.909] (n=31) | 0.901 [0.831, 0.958] (n=24) | 0.811 [0.735, 0.881] (n=36) | 0.835 [0.780, 0.892] (n=36) |
| citation_coverage | 0.889 [0.778, 0.972] (n=36) | 0.667 [0.500, 0.806] (n=36) | 1.000 [1.000, 1.000] (n=36) | 1.000 [1.000, 1.000] (n=36) |
| grounding_error_rate | N/A (n=0, na=36) | N/A (n=0, na=36) | 0.086 [0.009, 0.183] (n=36) | 0.028 [0.000, 0.083] (n=36) |

## multi_company_comparison

| Metric | system_a | system_b | system_c_v1 | system_c_v2 |
|---|---|---|---|---|
| numeric_accuracy | 0.474 [0.263, 0.684] (n=19) | 0.421 [0.211, 0.632] (n=19) | 0.684 [0.474, 0.895] (n=19) | 0.632 [0.421, 0.842] (n=19) |
| citation_precision | 0.928 [0.848, 1.000] (n=23) | 0.892 [0.783, 0.975] (n=20) | 0.849 [0.737, 0.952] (n=31) | 0.806 [0.677, 0.919] (n=31) |
| citation_recall | 0.978 [0.935, 1.000] (n=23) | 0.975 [0.925, 1.000] (n=20) | 0.919 [0.806, 1.000] (n=31) | 0.855 [0.726, 0.968] (n=31) |
| citation_f1 | 0.935 [0.877, 0.986] (n=23) | 0.908 [0.833, 0.967] (n=20) | 0.866 [0.758, 0.952] (n=31) | 0.817 [0.688, 0.925] (n=31) |
| citation_coverage | 0.697 [0.515, 0.848] (n=33) | 0.606 [0.424, 0.758] (n=33) | 0.939 [0.848, 1.000] (n=33) | 0.939 [0.848, 1.000] (n=33) |
| grounding_error_rate | N/A (n=0, na=33) | N/A (n=0, na=33) | 0.097 [0.035, 0.173] (n=33) | 0.085 [0.015, 0.164] (n=33) |

## Notes

- Context Precision is order-sensitive: it rewards relevant contexts ranked early. `retrieved_contexts` are kept in the order each system produced them (System C: retrieval order across hops, with v2's XBRL blocks first).
- Citation precision/recall/F1 are section-level (top-level 10-K item, `financials.csv` = any `[F-…]` citation), because the golden set has no gold chunk IDs. Answers with no citations are N/A, not 0; `citation_coverage` is the share of answers with at least one citation.
- Section aliases (a limitation of section-level matching): a cited `Item 15` chunk that is financial statements or notes counts as `Item 8`, and a cover-page chunk (no Item heading; registrant name, address, file number) counts as `Item 1`, matching how the golden set labels those facts.
- RAGAS metrics see the answer with citation tags stripped.
