# RQ2 results

Judge: openai/gpt-4o-mini. Cells: mean [bootstrap 95% CI] (n scored; na and failed rows excluded).

## Configuration

- RAGAS judge: openai/gpt-4o-mini, temperature 0 (`EVAL_JUDGE_PROVIDER` / `EVAL_JUDGE_MODEL`; one judge per scores file).
- Factual correctness (SECONDARY metric): mode `recall`, reference `answer_keypoints`, atomicity `low`.
- Judge output limit: the ragas default (1024 tokens) for most rows; 8192 tokens for the 16 rows that were truncated at the default and re-scored (`judge_max_tokens` in each such row's `detail`). The output limit only caps how long the judge's structured answer may be; model, temperature and prompts are identical, so it does not affect rows that completed under the lower limit.
- Primary accuracy: numeric questions use `numeric_accuracy`; qualitative and mixed questions use the saved `keypoint_recall` (rule-based, no LLM: `keypoint_recall` in `src/system_a/evaluate.py`, stored on each record by `scripts/rq3/run_rq3_experiment.py`; the share of a question's key points of which at least half of the content words appear in the answer). The refusal rate (`abstained`) is shown beside it.
- Answer relevancy embeddings: local `BAAI/bge-small-en-v1.5` (sentence-transformers, CPU).
- Answer model(s): openai/gpt-5.4.
- System C's own guardrail judge: for the full run it is set to OpenAI `gpt-4o-mini` via env vars during generation (`GUARDRAIL_JUDGE_PROVIDER=openai`, `GUARDRAIL_JUDGE_MODEL=gpt-4o-mini`); the smoke run used the `.env` setting (Groq `openai/gpt-oss-120b`).

## Generation

| System | Records | Failed to generate |
|---|---|---|
| system_c_v2 | 97 | 0 |

## overall

| Metric | system_c_v2 |
|---|---|
| primary_accuracy (numeric_accuracy / keypoint_recall) | 0.779 [0.710, 0.842] (n=97) |
| abstained (refusal rate) | 0.062 [0.021, 0.124] (n=97) |
| faithfulness | 0.745 [0.690, 0.798] (n=91) |
| answer_relevancy | 0.713 [0.639, 0.777] (n=97) |
| context_recall | 0.726 [0.673, 0.779] (n=97) |
| context_precision | 0.638 [0.578, 0.706] (n=97) |
| factual_correctness (secondary) | 0.483 [0.408, 0.567] (n=97) |
| numeric_accuracy | 0.762 [0.651, 0.857] (n=63) |
| citation_precision | 0.851 [0.784, 0.908] (n=94) |
| citation_recall | 0.872 [0.814, 0.926] (n=94) |
| citation_f1 | 0.841 [0.779, 0.893] (n=94) |
| citation_coverage | 0.969 [0.928, 1.000] (n=97) |
| citation_precision, uncited = 0 | 0.825 [0.756, 0.881] (n=97) |
| citation_recall, uncited = 0 | 0.845 [0.784, 0.907] (n=97) |
| citation_f1, uncited = 0 | 0.815 [0.752, 0.872] (n=97) |
| grounding_error_rate | 0.063 [0.019, 0.108] (n=97) |

## single_hop_factual

| Metric | system_c_v2 |
|---|---|
| primary_accuracy (numeric_accuracy / keypoint_recall) | 0.917 [0.833, 1.000] (n=8) |
| abstained (refusal rate) | 0.000 [0.000, 0.000] (n=8) |
| faithfulness | 0.906 [0.767, 1.000] (n=8) |
| answer_relevancy | 0.777 [0.547, 0.911] (n=8) |
| context_recall | 0.938 [0.812, 1.000] (n=8) |
| context_precision | 0.833 [0.720, 0.935] (n=8) |
| factual_correctness (secondary) | 0.863 [0.713, 1.000] (n=8) |
| numeric_accuracy | N/A (n=0, na=8) |
| citation_precision | 0.812 [0.625, 0.938] (n=8) |
| citation_recall | 1.000 [1.000, 1.000] (n=8) |
| citation_f1 | 0.875 [0.750, 0.958] (n=8) |
| citation_coverage | 1.000 [1.000, 1.000] (n=8) |
| citation_precision, uncited = 0 | 0.812 [0.625, 0.938] (n=8) |
| citation_recall, uncited = 0 | 1.000 [1.000, 1.000] (n=8) |
| citation_f1, uncited = 0 | 0.875 [0.750, 0.958] (n=8) |
| grounding_error_rate | 0.000 [0.000, 0.000] (n=8) |

## quantitative_tabular

| Metric | system_c_v2 |
|---|---|
| primary_accuracy (numeric_accuracy / keypoint_recall) | 0.850 [0.650, 1.000] (n=20) |
| abstained (refusal rate) | 0.050 [0.000, 0.150] (n=20) |
| faithfulness | 0.653 [0.535, 0.779] (n=19) |
| answer_relevancy | 0.792 [0.650, 0.894] (n=20) |
| context_recall | 0.625 [0.533, 0.717] (n=20) |
| context_precision | 0.673 [0.548, 0.790] (n=20) |
| factual_correctness (secondary) | 0.350 [0.175, 0.550] (n=20) |
| numeric_accuracy | 0.850 [0.650, 1.000] (n=20) |
| citation_precision | 0.868 [0.737, 1.000] (n=19) |
| citation_recall | 0.895 [0.737, 1.000] (n=19) |
| citation_f1 | 0.877 [0.737, 1.000] (n=19) |
| citation_coverage | 0.950 [0.850, 1.000] (n=20) |
| citation_precision, uncited = 0 | 0.825 [0.625, 0.975] (n=20) |
| citation_recall, uncited = 0 | 0.850 [0.650, 1.000] (n=20) |
| citation_f1, uncited = 0 | 0.833 [0.650, 0.983] (n=20) |
| grounding_error_rate | 0.117 [0.000, 0.267] (n=20) |

## cross_section_multihop

| Metric | system_c_v2 |
|---|---|
| primary_accuracy (numeric_accuracy / keypoint_recall) | 0.760 [0.673, 0.840] (n=60) |
| abstained (refusal rate) | 0.083 [0.017, 0.150] (n=60) |
| faithfulness | 0.752 [0.677, 0.829] (n=55) |
| answer_relevancy | 0.671 [0.575, 0.764] (n=60) |
| context_recall | 0.737 [0.660, 0.808] (n=60) |
| context_precision | 0.634 [0.551, 0.712] (n=60) |
| factual_correctness (secondary) | 0.474 [0.369, 0.567] (n=60) |
| numeric_accuracy | 0.744 [0.590, 0.872] (n=39) |
| citation_precision | 0.845 [0.767, 0.914] (n=58) |
| citation_recall | 0.836 [0.750, 0.905] (n=58) |
| citation_f1 | 0.816 [0.739, 0.882] (n=58) |
| citation_coverage | 0.967 [0.917, 1.000] (n=60) |
| citation_precision, uncited = 0 | 0.817 [0.725, 0.892] (n=60) |
| citation_recall, uncited = 0 | 0.808 [0.717, 0.883] (n=60) |
| citation_f1, uncited = 0 | 0.789 [0.703, 0.861] (n=60) |
| grounding_error_rate | 0.063 [0.017, 0.123] (n=60) |

## multi_company_comparison

| Metric | system_c_v2 |
|---|---|
| primary_accuracy (numeric_accuracy / keypoint_recall) | 0.630 [0.370, 0.852] (n=9) |
| abstained (refusal rate) | 0.000 [0.000, 0.000] (n=9) |
| faithfulness | 0.758 [0.567, 0.922] (n=9) |
| answer_relevancy | 0.755 [0.561, 0.877] (n=9) |
| context_recall | 0.694 [0.556, 0.843] (n=9) |
| context_precision | 0.406 [0.149, 0.667] (n=9) |
| factual_correctness (secondary) | 0.497 [0.246, 0.724] (n=9) |
| numeric_accuracy | 0.500 [0.000, 1.000] (n=4) |
| citation_precision | 0.889 [0.778, 1.000] (n=9) |
| citation_recall | 0.944 [0.833, 1.000] (n=9) |
| citation_f1 | 0.896 [0.815, 0.978] (n=9) |
| citation_coverage | 1.000 [1.000, 1.000] (n=9) |
| citation_precision, uncited = 0 | 0.889 [0.778, 1.000] (n=9) |
| citation_recall, uncited = 0 | 0.944 [0.833, 1.000] (n=9) |
| citation_f1, uncited = 0 | 0.896 [0.815, 0.978] (n=9) |
| grounding_error_rate | 0.000 [0.000, 0.000] (n=9) |

## answer_type=mixed

| Metric | system_c_v2 |
|---|---|
| primary_accuracy (numeric_accuracy / keypoint_recall) | 0.620 [0.490, 0.751] (n=20) |
| abstained (refusal rate) | 0.100 [0.000, 0.250] (n=20) |
| faithfulness | 0.714 [0.613, 0.815] (n=18) |
| answer_relevancy | 0.502 [0.325, 0.686] (n=20) |
| context_recall | 0.824 [0.737, 0.903] (n=20) |
| context_precision | 0.789 [0.706, 0.868] (n=20) |
| factual_correctness (secondary) | 0.417 [0.283, 0.556] (n=20) |
| numeric_accuracy | 0.750 [0.550, 0.950] (n=20) |
| citation_precision | 0.925 [0.850, 1.000] (n=20) |
| citation_recall | 0.750 [0.650, 0.850] (n=20) |
| citation_f1 | 0.800 [0.717, 0.883] (n=20) |
| citation_coverage | 1.000 [1.000, 1.000] (n=20) |
| citation_precision, uncited = 0 | 0.925 [0.850, 1.000] (n=20) |
| citation_recall, uncited = 0 | 0.750 [0.650, 0.850] (n=20) |
| citation_f1, uncited = 0 | 0.800 [0.717, 0.883] (n=20) |
| grounding_error_rate | 0.050 [0.000, 0.150] (n=20) |

## answer_type=narrative

| Metric | system_c_v2 |
|---|---|
| primary_accuracy (numeric_accuracy / keypoint_recall) | 0.887 [0.828, 0.946] (n=34) |
| abstained (refusal rate) | 0.000 [0.000, 0.000] (n=34) |
| faithfulness | 0.910 [0.852, 0.960] (n=34) |
| answer_relevancy | 0.803 [0.724, 0.865] (n=34) |
| context_recall | 0.876 [0.817, 0.936] (n=34) |
| context_precision | 0.805 [0.734, 0.865] (n=34) |
| factual_correctness (secondary) | 0.811 [0.725, 0.886] (n=34) |
| numeric_accuracy | N/A (n=0, na=34) |
| citation_precision | 0.838 [0.755, 0.912] (n=34) |
| citation_recall | 1.000 [1.000, 1.000] (n=34) |
| citation_f1 | 0.894 [0.839, 0.943] (n=34) |
| citation_coverage | 1.000 [1.000, 1.000] (n=34) |
| citation_precision, uncited = 0 | 0.838 [0.755, 0.912] (n=34) |
| citation_recall, uncited = 0 | 1.000 [1.000, 1.000] (n=34) |
| citation_f1, uncited = 0 | 0.894 [0.839, 0.943] (n=34) |
| grounding_error_rate | 0.000 [0.000, 0.000] (n=34) |

## answer_type=numerical

| Metric | system_c_v2 |
|---|---|
| primary_accuracy (numeric_accuracy / keypoint_recall) | 0.767 [0.628, 0.884] (n=43) |
| abstained (refusal rate) | 0.093 [0.023, 0.186] (n=43) |
| faithfulness | 0.617 [0.524, 0.711] (n=39) |
| answer_relevancy | 0.740 [0.629, 0.841] (n=43) |
| context_recall | 0.562 [0.484, 0.636] (n=43) |
| context_precision | 0.435 [0.333, 0.529] (n=43) |
| factual_correctness (secondary) | 0.254 [0.143, 0.370] (n=43) |
| numeric_accuracy | 0.767 [0.628, 0.884] (n=43) |
| citation_precision | 0.825 [0.713, 0.938] (n=40) |
| citation_recall | 0.825 [0.700, 0.925] (n=40) |
| citation_f1 | 0.817 [0.700, 0.925] (n=40) |
| citation_coverage | 0.930 [0.837, 1.000] (n=43) |
| citation_precision, uncited = 0 | 0.767 [0.628, 0.872] (n=43) |
| citation_recall, uncited = 0 | 0.767 [0.628, 0.872] (n=43) |
| citation_f1, uncited = 0 | 0.760 [0.620, 0.868] (n=43) |
| grounding_error_rate | 0.119 [0.039, 0.209] (n=43) |

## evidence_format=table

| Metric | system_c_v2 |
|---|---|
| primary_accuracy (numeric_accuracy / keypoint_recall) | 0.767 [0.628, 0.884] (n=43) |
| abstained (refusal rate) | 0.093 [0.023, 0.186] (n=43) |
| faithfulness | 0.617 [0.524, 0.711] (n=39) |
| answer_relevancy | 0.740 [0.629, 0.841] (n=43) |
| context_recall | 0.562 [0.484, 0.636] (n=43) |
| context_precision | 0.435 [0.333, 0.529] (n=43) |
| factual_correctness (secondary) | 0.254 [0.143, 0.370] (n=43) |
| numeric_accuracy | 0.767 [0.628, 0.884] (n=43) |
| citation_precision | 0.825 [0.713, 0.938] (n=40) |
| citation_recall | 0.825 [0.700, 0.925] (n=40) |
| citation_f1 | 0.817 [0.700, 0.925] (n=40) |
| citation_coverage | 0.930 [0.837, 1.000] (n=43) |
| citation_precision, uncited = 0 | 0.767 [0.628, 0.872] (n=43) |
| citation_recall, uncited = 0 | 0.767 [0.628, 0.872] (n=43) |
| citation_f1, uncited = 0 | 0.760 [0.620, 0.868] (n=43) |
| grounding_error_rate | 0.119 [0.039, 0.209] (n=43) |

## evidence_format=table_text

| Metric | system_c_v2 |
|---|---|
| primary_accuracy (numeric_accuracy / keypoint_recall) | 0.620 [0.490, 0.751] (n=20) |
| abstained (refusal rate) | 0.100 [0.000, 0.250] (n=20) |
| faithfulness | 0.714 [0.613, 0.815] (n=18) |
| answer_relevancy | 0.502 [0.325, 0.686] (n=20) |
| context_recall | 0.824 [0.737, 0.903] (n=20) |
| context_precision | 0.789 [0.706, 0.868] (n=20) |
| factual_correctness (secondary) | 0.417 [0.283, 0.556] (n=20) |
| numeric_accuracy | 0.750 [0.550, 0.950] (n=20) |
| citation_precision | 0.925 [0.850, 1.000] (n=20) |
| citation_recall | 0.750 [0.650, 0.850] (n=20) |
| citation_f1 | 0.800 [0.717, 0.883] (n=20) |
| citation_coverage | 1.000 [1.000, 1.000] (n=20) |
| citation_precision, uncited = 0 | 0.925 [0.850, 1.000] (n=20) |
| citation_recall, uncited = 0 | 0.750 [0.650, 0.850] (n=20) |
| citation_f1, uncited = 0 | 0.800 [0.717, 0.883] (n=20) |
| grounding_error_rate | 0.050 [0.000, 0.150] (n=20) |

## evidence_format=text

| Metric | system_c_v2 |
|---|---|
| primary_accuracy (numeric_accuracy / keypoint_recall) | 0.887 [0.828, 0.946] (n=34) |
| abstained (refusal rate) | 0.000 [0.000, 0.000] (n=34) |
| faithfulness | 0.910 [0.852, 0.960] (n=34) |
| answer_relevancy | 0.803 [0.724, 0.865] (n=34) |
| context_recall | 0.876 [0.817, 0.936] (n=34) |
| context_precision | 0.805 [0.734, 0.865] (n=34) |
| factual_correctness (secondary) | 0.811 [0.725, 0.886] (n=34) |
| numeric_accuracy | N/A (n=0, na=34) |
| citation_precision | 0.838 [0.755, 0.912] (n=34) |
| citation_recall | 1.000 [1.000, 1.000] (n=34) |
| citation_f1 | 0.894 [0.839, 0.943] (n=34) |
| citation_coverage | 1.000 [1.000, 1.000] (n=34) |
| citation_precision, uncited = 0 | 0.838 [0.755, 0.912] (n=34) |
| citation_recall, uncited = 0 | 1.000 [1.000, 1.000] (n=34) |
| citation_f1, uncited = 0 | 0.894 [0.839, 0.943] (n=34) |
| grounding_error_rate | 0.000 [0.000, 0.000] (n=34) |

## hop=multi

| Metric | system_c_v2 |
|---|---|
| primary_accuracy (numeric_accuracy / keypoint_recall) | 0.747 [0.666, 0.825] (n=78) |
| abstained (refusal rate) | 0.064 [0.013, 0.128] (n=78) |
| faithfulness | 0.740 [0.679, 0.802] (n=73) |
| answer_relevancy | 0.694 [0.611, 0.777] (n=78) |
| context_recall | 0.728 [0.665, 0.786] (n=78) |
| context_precision | 0.612 [0.537, 0.677] (n=78) |
| factual_correctness (secondary) | 0.454 [0.365, 0.537] (n=78) |
| numeric_accuracy | 0.731 [0.615, 0.846] (n=52) |
| citation_precision | 0.836 [0.757, 0.895] (n=76) |
| citation_recall | 0.842 [0.770, 0.901] (n=76) |
| citation_f1 | 0.817 [0.747, 0.875] (n=76) |
| citation_coverage | 0.974 [0.936, 1.000] (n=78) |
| citation_precision, uncited = 0 | 0.814 [0.737, 0.882] (n=78) |
| citation_recall, uncited = 0 | 0.821 [0.744, 0.891] (n=78) |
| citation_f1, uncited = 0 | 0.796 [0.727, 0.861] (n=78) |
| grounding_error_rate | 0.066 [0.023, 0.117] (n=78) |

## hop=single

| Metric | system_c_v2 |
|---|---|
| primary_accuracy (numeric_accuracy / keypoint_recall) | 0.912 [0.789, 1.000] (n=19) |
| abstained (refusal rate) | 0.053 [0.000, 0.158] (n=19) |
| faithfulness | 0.767 [0.644, 0.889] (n=18) |
| answer_relevancy | 0.788 [0.650, 0.894] (n=19) |
| context_recall | 0.719 [0.588, 0.851] (n=19) |
| context_precision | 0.744 [0.615, 0.856] (n=19) |
| factual_correctness (secondary) | 0.600 [0.389, 0.811] (n=19) |
| numeric_accuracy | 0.909 [0.727, 1.000] (n=11) |
| citation_precision | 0.917 [0.833, 1.000] (n=18) |
| citation_recall | 1.000 [1.000, 1.000] (n=18) |
| citation_f1 | 0.944 [0.889, 1.000] (n=18) |
| citation_coverage | 0.947 [0.842, 1.000] (n=19) |
| citation_precision, uncited = 0 | 0.868 [0.737, 0.974] (n=19) |
| citation_recall, uncited = 0 | 0.947 [0.842, 1.000] (n=19) |
| citation_f1, uncited = 0 | 0.895 [0.754, 0.982] (n=19) |
| grounding_error_rate | 0.053 [0.000, 0.158] (n=19) |

## task=calculation

| Metric | system_c_v2 |
|---|---|
| primary_accuracy (numeric_accuracy / keypoint_recall) | 0.721 [0.625, 0.811] (n=63) |
| abstained (refusal rate) | 0.095 [0.032, 0.175] (n=63) |
| faithfulness | 0.647 [0.576, 0.723] (n=57) |
| answer_relevancy | 0.664 [0.564, 0.758] (n=63) |
| context_recall | 0.645 [0.575, 0.707] (n=63) |
| context_precision | 0.547 [0.459, 0.635] (n=63) |
| factual_correctness (secondary) | 0.306 [0.217, 0.397] (n=63) |
| numeric_accuracy | 0.762 [0.651, 0.857] (n=63) |
| citation_precision | 0.858 [0.775, 0.933] (n=60) |
| citation_recall | 0.800 [0.708, 0.883] (n=60) |
| citation_f1 | 0.811 [0.725, 0.883] (n=60) |
| citation_coverage | 0.952 [0.889, 1.000] (n=63) |
| citation_precision, uncited = 0 | 0.817 [0.722, 0.897] (n=63) |
| citation_recall, uncited = 0 | 0.762 [0.667, 0.849] (n=63) |
| citation_f1, uncited = 0 | 0.772 [0.677, 0.852] (n=63) |
| grounding_error_rate | 0.097 [0.037, 0.173] (n=63) |

## task=lookup

| Metric | system_c_v2 |
|---|---|
| primary_accuracy (numeric_accuracy / keypoint_recall) | 0.887 [0.828, 0.946] (n=34) |
| abstained (refusal rate) | 0.000 [0.000, 0.000] (n=34) |
| faithfulness | 0.910 [0.852, 0.960] (n=34) |
| answer_relevancy | 0.803 [0.724, 0.865] (n=34) |
| context_recall | 0.876 [0.817, 0.936] (n=34) |
| context_precision | 0.805 [0.734, 0.865] (n=34) |
| factual_correctness (secondary) | 0.811 [0.725, 0.886] (n=34) |
| numeric_accuracy | N/A (n=0, na=34) |
| citation_precision | 0.838 [0.755, 0.912] (n=34) |
| citation_recall | 1.000 [1.000, 1.000] (n=34) |
| citation_f1 | 0.894 [0.839, 0.943] (n=34) |
| citation_coverage | 1.000 [1.000, 1.000] (n=34) |
| citation_precision, uncited = 0 | 0.838 [0.755, 0.912] (n=34) |
| citation_recall, uncited = 0 | 1.000 [1.000, 1.000] (n=34) |
| citation_f1, uncited = 0 | 0.894 [0.839, 0.943] (n=34) |
| grounding_error_rate | 0.000 [0.000, 0.000] (n=34) |

## evidence_scope=cross_company

| Metric | system_c_v2 |
|---|---|
| primary_accuracy (numeric_accuracy / keypoint_recall) | 0.630 [0.370, 0.852] (n=9) |
| abstained (refusal rate) | 0.000 [0.000, 0.000] (n=9) |
| faithfulness | 0.758 [0.567, 0.922] (n=9) |
| answer_relevancy | 0.755 [0.561, 0.877] (n=9) |
| context_recall | 0.694 [0.556, 0.843] (n=9) |
| context_precision | 0.406 [0.149, 0.667] (n=9) |
| factual_correctness (secondary) | 0.497 [0.246, 0.724] (n=9) |
| numeric_accuracy | 0.500 [0.000, 1.000] (n=4) |
| citation_precision | 0.889 [0.778, 1.000] (n=9) |
| citation_recall | 0.944 [0.833, 1.000] (n=9) |
| citation_f1 | 0.896 [0.815, 0.978] (n=9) |
| citation_coverage | 1.000 [1.000, 1.000] (n=9) |
| citation_precision, uncited = 0 | 0.889 [0.778, 1.000] (n=9) |
| citation_recall, uncited = 0 | 0.944 [0.833, 1.000] (n=9) |
| citation_f1, uncited = 0 | 0.896 [0.815, 0.978] (n=9) |
| grounding_error_rate | 0.000 [0.000, 0.000] (n=9) |

## evidence_scope=cross_year

| Metric | system_c_v2 |
|---|---|
| primary_accuracy (numeric_accuracy / keypoint_recall) | 0.803 [0.677, 0.919] (n=33) |
| abstained (refusal rate) | 0.091 [0.000, 0.182] (n=33) |
| faithfulness | 0.734 [0.612, 0.838] (n=30) |
| answer_relevancy | 0.767 [0.654, 0.873] (n=33) |
| context_recall | 0.640 [0.535, 0.745] (n=33) |
| context_precision | 0.499 [0.387, 0.612] (n=33) |
| factual_correctness (secondary) | 0.425 [0.288, 0.567] (n=33) |
| numeric_accuracy | 0.737 [0.526, 0.895] (n=19) |
| citation_precision | 0.806 [0.677, 0.919] (n=31) |
| citation_recall | 0.855 [0.726, 0.968] (n=31) |
| citation_f1 | 0.817 [0.688, 0.925] (n=31) |
| citation_coverage | 0.939 [0.848, 1.000] (n=33) |
| citation_precision, uncited = 0 | 0.758 [0.621, 0.879] (n=33) |
| citation_recall, uncited = 0 | 0.803 [0.667, 0.909] (n=33) |
| citation_f1, uncited = 0 | 0.768 [0.636, 0.889] (n=33) |
| grounding_error_rate | 0.085 [0.015, 0.170] (n=33) |

## evidence_scope=single_doc

| Metric | system_c_v2 |
|---|---|
| primary_accuracy (numeric_accuracy / keypoint_recall) | 0.789 [0.709, 0.861] (n=55) |
| abstained (refusal rate) | 0.055 [0.000, 0.127] (n=55) |
| faithfulness | 0.750 [0.682, 0.818] (n=52) |
| answer_relevancy | 0.673 [0.569, 0.761] (n=55) |
| context_recall | 0.783 [0.718, 0.844] (n=55) |
| context_precision | 0.759 [0.694, 0.822] (n=55) |
| factual_correctness (secondary) | 0.515 [0.413, 0.623] (n=55) |
| numeric_accuracy | 0.800 [0.675, 0.925] (n=40) |
| citation_precision | 0.870 [0.787, 0.935] (n=54) |
| citation_recall | 0.870 [0.787, 0.935] (n=54) |
| citation_f1 | 0.846 [0.775, 0.904] (n=54) |
| citation_coverage | 0.982 [0.945, 1.000] (n=55) |
| citation_precision, uncited = 0 | 0.855 [0.782, 0.927] (n=55) |
| citation_recall, uncited = 0 | 0.855 [0.773, 0.918] (n=55) |
| citation_f1, uncited = 0 | 0.830 [0.755, 0.894] (n=55) |
| grounding_error_rate | 0.061 [0.006, 0.127] (n=55) |

## Failed to score

No judge rows failed: every LLM metric was scored for every answer (N/A rows excluded).

## Expected ordering on primary accuracy

Expected:  (a later system scores higher). Paired differences (second minus first) on the same questions, 95% paired bootstrap CI (2000 resamples, seed 0), Wilcoxon signed-rank p-value, Holm-corrected across the 0 pairs.

| Pair | n | Mean first | Mean second | Difference [95% CI] | p (Holm) | Significant | Verdict |
|---|---|---|---|---|---|---|---|

The full expected ordering **does not hold**: at least one adjacent pair is not significantly in the expected direction.

## Paired comparisons (overall, all metrics)

Difference = second minus first, mean [95% CI]; * = significant after Holm correction (p < 0.05). Per attribute: `paired_comparisons.csv`.

| Metric |  |
|---|

## Significant paired differences by question attribute

None.

## Error types

A wrong answer is a numeric question whose number is not in the answer (numeric_accuracy < 1), or any other question with keypoint_recall < 0.5, or a refusal. Each gets ONE primary type, first match wins: 1 `refusal` = abstained; 2 `retrieval_miss` = RAGAS context recall < 0.5 (the gold evidence was not retrieved); 3 `wrong_number` = the question has a gold number and numeric_accuracy < 1 although evidence was retrieved; 4 `unsupported_claim` = faithfulness < 0.5; 5 `incomplete` = everything else, e.g. key points missed.

### overall

| System | Answers | Wrong | refusal | retrieval_miss | wrong_number | unsupported_claim | incomplete |
|---|---|---|---|---|---|---|---|
| system_c_v2 | 97 | 17 | 6 (35%) | 3 (18%) | 4 (24%) | 1 (6%) | 3 (18%) |

### answer_type=mixed

| System | Answers | Wrong | refusal | retrieval_miss | wrong_number | unsupported_claim | incomplete |
|---|---|---|---|---|---|---|---|
| system_c_v2 | 20 | 6 | 2 (33%) | 0 (0%) | 1 (17%) | 1 (17%) | 2 (33%) |

### answer_type=narrative

| System | Answers | Wrong | refusal | retrieval_miss | wrong_number | unsupported_claim | incomplete |
|---|---|---|---|---|---|---|---|
| system_c_v2 | 34 | 1 | 0 (0%) | 0 (0%) | 0 (0%) | 0 (0%) | 1 (100%) |

### answer_type=numerical

| System | Answers | Wrong | refusal | retrieval_miss | wrong_number | unsupported_claim | incomplete |
|---|---|---|---|---|---|---|---|
| system_c_v2 | 43 | 10 | 4 (40%) | 3 (30%) | 3 (30%) | 0 (0%) | 0 (0%) |

### evidence_format=table

| System | Answers | Wrong | refusal | retrieval_miss | wrong_number | unsupported_claim | incomplete |
|---|---|---|---|---|---|---|---|
| system_c_v2 | 43 | 10 | 4 (40%) | 3 (30%) | 3 (30%) | 0 (0%) | 0 (0%) |

### evidence_format=table_text

| System | Answers | Wrong | refusal | retrieval_miss | wrong_number | unsupported_claim | incomplete |
|---|---|---|---|---|---|---|---|
| system_c_v2 | 20 | 6 | 2 (33%) | 0 (0%) | 1 (17%) | 1 (17%) | 2 (33%) |

### evidence_format=text

| System | Answers | Wrong | refusal | retrieval_miss | wrong_number | unsupported_claim | incomplete |
|---|---|---|---|---|---|---|---|
| system_c_v2 | 34 | 1 | 0 (0%) | 0 (0%) | 0 (0%) | 0 (0%) | 1 (100%) |

### hop=multi

| System | Answers | Wrong | refusal | retrieval_miss | wrong_number | unsupported_claim | incomplete |
|---|---|---|---|---|---|---|---|
| system_c_v2 | 78 | 16 | 5 (31%) | 3 (19%) | 4 (25%) | 1 (6%) | 3 (19%) |

### hop=single

| System | Answers | Wrong | refusal | retrieval_miss | wrong_number | unsupported_claim | incomplete |
|---|---|---|---|---|---|---|---|
| system_c_v2 | 19 | 1 | 1 (100%) | 0 (0%) | 0 (0%) | 0 (0%) | 0 (0%) |

### task=calculation

| System | Answers | Wrong | refusal | retrieval_miss | wrong_number | unsupported_claim | incomplete |
|---|---|---|---|---|---|---|---|
| system_c_v2 | 63 | 16 | 6 (38%) | 3 (19%) | 4 (25%) | 1 (6%) | 2 (12%) |

### task=lookup

| System | Answers | Wrong | refusal | retrieval_miss | wrong_number | unsupported_claim | incomplete |
|---|---|---|---|---|---|---|---|
| system_c_v2 | 34 | 1 | 0 (0%) | 0 (0%) | 0 (0%) | 0 (0%) | 1 (100%) |

### evidence_scope=cross_company

| System | Answers | Wrong | refusal | retrieval_miss | wrong_number | unsupported_claim | incomplete |
|---|---|---|---|---|---|---|---|
| system_c_v2 | 9 | 3 | 0 (0%) | 2 (67%) | 0 (0%) | 0 (0%) | 1 (33%) |

### evidence_scope=cross_year

| System | Answers | Wrong | refusal | retrieval_miss | wrong_number | unsupported_claim | incomplete |
|---|---|---|---|---|---|---|---|
| system_c_v2 | 33 | 5 | 3 (60%) | 1 (20%) | 1 (20%) | 0 (0%) | 0 (0%) |

### evidence_scope=single_doc

| System | Answers | Wrong | refusal | retrieval_miss | wrong_number | unsupported_claim | incomplete |
|---|---|---|---|---|---|---|---|
| system_c_v2 | 55 | 9 | 3 (33%) | 0 (0%) | 3 (33%) | 1 (11%) | 2 (22%) |

Cells: count (share of that system's wrong answers).

## Refusals and retrieval

For every answer the gold evidence quotes of its question (benchmark `gold_evidence`) are checked against the retrieved contexts of that system: *all* = every quote is in a retrieved chunk of the gold filing (normalised substring, or at least 80% of the words of a quote of 15+ words); *some* = at least one but not all; *none*. *Lenient* additionally accepts any quote of which 60% of the words are in a chunk of that filing.

| System | Refusals | Evidence all | some | none | All, lenient | Answered | Evidence all | some | none | All, lenient |
|---|---|---|---|---|---|---|---|---|---|---|
| system_c_v2 | 6 | 0 | 2 | 4 | 1 | 91 | 63 | 22 | 6 | 67 |

## Retrieval context per system

| System | Answers | Mean chunks | Mean characters | Mean hops | 1 hop | 2 hops | 3 hops |
|---|---|---|---|---|---|---|---|
| system_c_v2 | 97 | 9.4 | 7,346 | 1.77 | 53 | 13 | 31 |

## Numeric accuracy vs the saved correctness flags

`numeric_accuracy` agrees with the RQ3 harness flag `numeric_correct` on 63 of 63 answers with a gold number (system_c_v2: 63/63).

## Notes

- Context Precision is order-sensitive: it rewards relevant contexts ranked early. `retrieved_contexts` are kept in the order each system produced them (System C: retrieval order across hops).
- Citation precision/recall/F1 are section-level (top-level 10-K item, `financials.csv` = any `[F-…]` citation), because the benchmark has no gold chunk IDs. Answers with no citations are N/A, not 0, so those rows use citing answers only; `citation_coverage` (the share of answers with at least one citation) is always shown beside them, and the `uncited = 0` rows count an answer without citations as 0.
- Section aliases (a limitation of section-level matching): a cited `Item 15` chunk that is financial statements or notes counts as `Item 8`, and a cover-page chunk (no Item heading; registrant name, address, file number) counts as `Item 1`, matching how the benchmark labels those facts.
- RAGAS metrics see the answer with citation tags stripped.
- Refusals ("Not found in the provided context", "cannot be determined", ...) are counted by `abstained`. They are N/A for faithfulness (no claims to check) and score 0 for factual correctness, instead of the 1.0 RAGAS would give a claim-free answer.
- RAGAS references come from the benchmark: factual correctness uses the reference named in the configuration; context recall / precision use the gold evidence quotes plus the gold answer, because a computed answer such as "-30.36%" does not appear in any filing. A bare negative gold number is also written as a decrease.
- Numeric accuracy accepts the unsigned value of a negative gold number ("-25.64%" matches "decreased by 25.6%", 0.5% relative tolerance), so a wrong sign is not caught.
- Categories: multi_company_comparison is only questions across companies; one company across years is cross_section_multihop. `dim=value` sections use the proposal's attributes from the benchmark: answer_type (type), evidence_format (recipe), hop, task (calculation when the gold has a program), evidence_scope (scope).

## Limitations

- **Factual correctness is a secondary metric.** On a 20-answer canary it agreed only moderately with the saved correctness flags (mean absolute difference 0.28), because (1) its recall also counts the answer's extra correct claims (intermediate figures the reference does not contain), (2) the judge is confused by the sign of the gold number ("-30.36%" is marked wrong for an answer saying a 30.36% decrease, and the reverse), and (3) it splits one condition ("probable AND reasonably estimable") into separate claims that are then judged one by one.
- **Faithfulness cannot verify a number the system calculated itself** (e.g. 30.36%), since it is not in any retrieved text; correct calculations are therefore slightly penalised.
- **The judge is not fully repeatable at temperature 0**: repeated scoring of the same answer gave different values on the canary.
- **Refusal detection is a rule**: an answer is a refusal when its first sentence says the evidence is missing ("not found in the provided context", "cannot be determined", ...). Partial answers are not refusals. The rule treats some partial "I can only answer part of this" replies inconsistently (e.g. A gold-045 is flagged, A gold-071 is not), so refusal counts may be off by a few for A.
- **Numeric matching is a rule**: it accepts accounting negatives ("(6.0)", "$(316)"), a bare table figure against a gold value with a unit ("$316" for "$316 million", exact digits, at least 3 significant digits), the unsigned value of a negative gold number, and ratio / percentage equivalents ("72.08%" for "0.72") within a 0.5% relative tolerance. A wrong sign or a wrong unit is therefore not caught. The remaining disagreements with the saved `numeric_correct` flags are listed under "Numeric accuracy vs the saved correctness flags".
- **Error types are heuristic.** A wrong answer is a numeric question whose number is not in the answer (numeric_accuracy < 1), or any other question with keypoint_recall < 0.5, or a refusal. Each gets ONE primary type, first match wins: 1 `refusal` = abstained; 2 `retrieval_miss` = RAGAS context recall < 0.5 (the gold evidence was not retrieved); 3 `wrong_number` = the question has a gold number and numeric_accuracy < 1 although evidence was retrieved; 4 `unsupported_claim` = faithfulness < 0.5; 5 `incomplete` = everything else, e.g. key points missed.
- **System C v3 may have been tuned on this benchmark** (built after it existed, reports 100% numerical accuracy on it), so its numbers may be optimistic.
- **The judge (gpt-4o-mini) is weaker than the answer model (gpt-5.4)**; a stronger-judge spot-check is planned.
- **The answer model is labelled both `gpt-5.4` and `gpt-5.4-2026-03-05`** in the records; most likely the same model reported two ways.
- **Keypoint recall is word overlap**, not meaning: a paraphrase can miss a key point, and a long answer can cover one by chance.
- Paired differences use the same questions for both systems; with 97 questions, small per-attribute groups have wide intervals, and p-values are Holm-corrected only across the 6 system pairs of one metric and group, not across metrics or groups.
