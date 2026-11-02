# RQ2 results

Judge: openai/gpt-4o-mini. Cells: mean [bootstrap 95% CI] (n scored; na and failed rows excluded).

## Configuration

- RAGAS judge: openai/gpt-4o-mini (`EVAL_JUDGE_PROVIDER` / `EVAL_JUDGE_MODEL`; one judge per scores file).
- Answer relevancy embeddings: local `BAAI/bge-small-en-v1.5` (sentence-transformers, CPU).
- Answer model(s): openai/gpt-5.4, openai/gpt-5.4-2026-03-05.
- System C's own guardrail judge: for the full run it is set to OpenAI `gpt-4o-mini` via env vars during generation (`GUARDRAIL_JUDGE_PROVIDER=openai`, `GUARDRAIL_JUDGE_MODEL=gpt-4o-mini`); the smoke run used the `.env` setting (Groq `openai/gpt-oss-120b`).

## Generation

| System | Records | Failed to generate |
|---|---|---|
| system_a | 5 | 0 |
| system_b | 5 | 0 |
| system_c_v1 | 5 | 0 |
| system_c_v3 | 5 | 0 |

## overall

| Metric | system_a | system_b | system_c_v1 | system_c_v3 |
|---|---|---|---|---|
| faithfulness | 0.920 [0.760, 1.000] (n=5) | 0.867 [0.600, 1.000] (n=5) | 0.660 [0.300, 0.960] (n=5) | 0.688 [0.428, 0.916] (n=5) |
| answer_relevancy | 0.587 [0.260, 0.835] (n=5) | 0.621 [0.277, 0.856] (n=5) | 0.607 [0.275, 0.886] (n=5) | 0.785 [0.627, 0.922] (n=5) |
| context_recall | 0.600 [0.200, 1.000] (n=5) | 0.467 [0.067, 0.867] (n=5) | 0.467 [0.067, 0.867] (n=5) | 0.467 [0.067, 0.867] (n=5) |
| context_precision | 0.604 [0.283, 0.926] (n=5) | 0.750 [0.367, 0.983] (n=5) | 0.748 [0.362, 0.986] (n=5) | 0.897 [0.750, 0.996] (n=5) |
| factual_correctness | 0.508 [0.120, 0.896] (n=5) | 0.572 [0.248, 0.848] (n=5) | 0.394 [0.200, 0.562] (n=5) | 0.280 [0.080, 0.480] (n=5) |
| numeric_accuracy | 0.000 [0.000, 0.000] (n=2) | 0.000 [0.000, 0.000] (n=2) | 0.000 [0.000, 0.000] (n=2) | 0.000 [0.000, 0.000] (n=2) |
| citation_precision | 0.625 [0.250, 1.000] (n=4) | 0.750 [0.500, 1.000] (n=4) | 0.800 [0.600, 1.000] (n=5) | 0.800 [0.600, 1.000] (n=5) |
| citation_recall | 0.750 [0.250, 1.000] (n=4) | 1.000 [1.000, 1.000] (n=4) | 1.000 [1.000, 1.000] (n=5) | 1.000 [1.000, 1.000] (n=5) |
| citation_f1 | 0.667 [0.250, 1.000] (n=4) | 0.833 [0.667, 1.000] (n=4) | 0.867 [0.733, 1.000] (n=5) | 0.867 [0.733, 1.000] (n=5) |
| citation_coverage | 0.800 [0.400, 1.000] (n=5) | 0.800 [0.400, 1.000] (n=5) | 1.000 [1.000, 1.000] (n=5) | 1.000 [1.000, 1.000] (n=5) |
| grounding_error_rate | N/A (n=0, na=5) | N/A (n=0, na=5) | 0.000 [0.000, 0.000] (n=5) | 0.000 [0.000, 0.000] (n=5) |

## single_hop_factual

| Metric | system_a | system_b | system_c_v1 | system_c_v3 |
|---|---|---|---|---|
| faithfulness | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) | 0.800 [0.800, 0.800] (n=1) | 0.889 [0.889, 0.889] (n=1) |
| answer_relevancy | 0.832 [0.832, 0.832] (n=1) | 0.825 [0.825, 0.825] (n=1) | 0.923 [0.923, 0.923] (n=1) | 0.932 [0.932, 0.932] (n=1) |
| context_recall | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| context_precision | 0.174 [0.174, 0.174] (n=1) | 0.917 [0.917, 0.917] (n=1) | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| factual_correctness | 0.000 [0.000, 0.000] (n=1) | 0.570 [0.570, 0.570] (n=1) | 0.400 [0.400, 0.400] (n=1) | 0.000 [0.000, 0.000] (n=1) |
| numeric_accuracy | N/A (n=0, na=1) | N/A (n=0, na=1) | N/A (n=0, na=1) | N/A (n=0, na=1) |
| citation_precision | 0.000 [0.000, 0.000] (n=1) | 0.500 [0.500, 0.500] (n=1) | 0.500 [0.500, 0.500] (n=1) | 0.500 [0.500, 0.500] (n=1) |
| citation_recall | 0.000 [0.000, 0.000] (n=1) | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| citation_f1 | 0.000 [0.000, 0.000] (n=1) | 0.667 [0.667, 0.667] (n=1) | 0.667 [0.667, 0.667] (n=1) | 0.667 [0.667, 0.667] (n=1) |
| citation_coverage | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| grounding_error_rate | N/A (n=0, na=1) | N/A (n=0, na=1) | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) |

## quantitative_tabular

| Metric | system_a | system_b | system_c_v1 | system_c_v3 |
|---|---|---|---|---|
| faithfulness | 0.600 [0.600, 0.600] (n=1) | 0.333 [0.333, 0.333] (n=1) | 0.500 [0.500, 0.500] (n=1) | 0.500 [0.500, 0.500] (n=1) |
| answer_relevancy | 0.720 [0.720, 0.720] (n=1) | 0.806 [0.806, 0.806] (n=1) | 0.720 [0.720, 0.720] (n=1) | 0.719 [0.719, 0.719] (n=1) |
| context_recall | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) |
| context_precision | 0.734 [0.734, 0.734] (n=1) | 0.833 [0.833, 0.833] (n=1) | 0.810 [0.810, 0.810] (n=1) | 0.877 [0.877, 0.877] (n=1) |
| factual_correctness | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) | 0.400 [0.400, 0.400] (n=1) | 0.400 [0.400, 0.400] (n=1) |
| numeric_accuracy | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) |
| citation_precision | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| citation_recall | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| citation_f1 | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| citation_coverage | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| grounding_error_rate | N/A (n=0, na=1) | N/A (n=0, na=1) | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) |

## cross_section_multihop

| Metric | system_a | system_b | system_c_v1 | system_c_v3 |
|---|---|---|---|---|
| faithfulness | 1.000 [1.000, 1.000] (n=2) | 1.000 [1.000, 1.000] (n=2) | 1.000 [1.000, 1.000] (n=2) | 0.900 [0.800, 1.000] (n=2) |
| answer_relevancy | 0.690 [0.468, 0.912] (n=2) | 0.738 [0.562, 0.913] (n=2) | 0.696 [0.451, 0.942] (n=2) | 0.666 [0.468, 0.864] (n=2) |
| context_recall | 1.000 [1.000, 1.000] (n=2) | 0.667 [0.333, 1.000] (n=2) | 0.667 [0.333, 1.000] (n=2) | 0.667 [0.333, 1.000] (n=2) |
| context_precision | 0.974 [0.947, 1.000] (n=2) | 1.000 [1.000, 1.000] (n=2) | 0.965 [0.929, 1.000] (n=2) | 0.991 [0.982, 1.000] (n=2) |
| factual_correctness | 0.770 [0.600, 0.940] (n=2) | 0.645 [0.620, 0.670] (n=2) | 0.335 [0.000, 0.670] (n=2) | 0.500 [0.500, 0.500] (n=2) |
| numeric_accuracy | N/A (n=0, na=2) | N/A (n=0, na=2) | N/A (n=0, na=2) | N/A (n=0, na=2) |
| citation_precision | 0.750 [0.500, 1.000] (n=2) | 0.750 [0.500, 1.000] (n=2) | 0.750 [0.500, 1.000] (n=2) | 0.750 [0.500, 1.000] (n=2) |
| citation_recall | 1.000 [1.000, 1.000] (n=2) | 1.000 [1.000, 1.000] (n=2) | 1.000 [1.000, 1.000] (n=2) | 1.000 [1.000, 1.000] (n=2) |
| citation_f1 | 0.833 [0.667, 1.000] (n=2) | 0.833 [0.667, 1.000] (n=2) | 0.833 [0.667, 1.000] (n=2) | 0.833 [0.667, 1.000] (n=2) |
| citation_coverage | 1.000 [1.000, 1.000] (n=2) | 1.000 [1.000, 1.000] (n=2) | 1.000 [1.000, 1.000] (n=2) | 1.000 [1.000, 1.000] (n=2) |
| grounding_error_rate | N/A (n=0, na=2) | N/A (n=0, na=2) | 0.000 [0.000, 0.000] (n=2) | 0.000 [0.000, 0.000] (n=2) |

## multi_company_comparison

| Metric | system_a | system_b | system_c_v1 | system_c_v3 |
|---|---|---|---|---|
| faithfulness | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) | 0.000 [0.000, 0.000] (n=1) | 0.250 [0.250, 0.250] (n=1) |
| answer_relevancy | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) | 0.941 [0.941, 0.941] (n=1) |
| context_recall | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) |
| context_precision | 0.167 [0.167, 0.167] (n=1) | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) | 0.625 [0.625, 0.625] (n=1) |
| factual_correctness | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) | 0.500 [0.500, 0.500] (n=1) | 0.000 [0.000, 0.000] (n=1) |
| numeric_accuracy | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) |
| citation_precision | N/A (n=0, na=1) | N/A (n=0, na=1) | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| citation_recall | N/A (n=0, na=1) | N/A (n=0, na=1) | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| citation_f1 | N/A (n=0, na=1) | N/A (n=0, na=1) | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| citation_coverage | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) | 1.000 [1.000, 1.000] (n=1) | 1.000 [1.000, 1.000] (n=1) |
| grounding_error_rate | N/A (n=0, na=1) | N/A (n=0, na=1) | 0.000 [0.000, 0.000] (n=1) | 0.000 [0.000, 0.000] (n=1) |

## Notes

- Context Precision is order-sensitive: it rewards relevant contexts ranked early. `retrieved_contexts` are kept in the order each system produced them (System C: retrieval order across hops, with v2's XBRL blocks first).
- Citation precision/recall/F1 are section-level (top-level 10-K item, `financials.csv` = any `[F-…]` citation), because the golden set has no gold chunk IDs. Answers with no citations are N/A, not 0; `citation_coverage` is the share of answers with at least one citation.
- Section aliases (a limitation of section-level matching): a cited `Item 15` chunk that is financial statements or notes counts as `Item 8`, and a cover-page chunk (no Item heading; registrant name, address, file number) counts as `Item 1`, matching how the golden set labels those facts.
- RAGAS metrics see the answer with citation tags stripped.
