# Updated System B slide tables

All 97 distinct expected question IDs have one A and one revised B answer (194 records). Both use Groq openai/gpt-oss-120b, temperature 0. Primary accuracy is final. RAGAS evaluation is IN PROGRESS; partial judgments are excluded from this publication snapshot.

## Primary accuracy

| Question type | A: Dense (Groq) | Revised B: Hybrid (Groq) | C v1: Historical GPT-5.4 reference | Paired significance A/B |
|---|---:|---:|---:|---|
| All questions (n=97) | 0.60 | 0.76 | 0.86 | B > A |
| Narrative (n=34) | 0.65 | 0.88 | 0.93 | B > A |
| Numerical / table (n=43) | 0.53 | 0.65 | 0.88 | B > A |
| Mixed text + table (n=20) | 0.64 | 0.79 | 0.70 | Not significant |
| Single-hop (n=19) | 0.77 | 0.88 | 0.98 | Not significant |
| Multi-hop (n=78) | 0.55 | 0.73 | 0.83 | B > A |
| Cross-year (n=33) | 0.48 | 0.68 | 0.83 | B > A |

Primary accuracy uses numerical matching for numeric questions and key-point recall for qualitative/mixed questions. The numerical/table and mixed labels follow team answer-type facets; they are not independent evidence-format filters.

## Faithfulness, relevance and citations

| Metric | What it checks | A: Dense (Groq) | Revised B (Groq) | C v1: Historical reference | Paired significance A/B |
|---|---|---:|---:|---:|---|
| Faithfulness | Claims supported by retrieved text (answered cases) | Pending (0/97 judged) | Pending (0/97 judged) | 0.74 | Pending |
| Answer relevancy | Answer addresses the question | Pending (0/97 judged) | Pending (0/97 judged) | 0.77 | Pending |
| Context recall | Gold evidence represented in retrieved text | Pending (0/97 judged) | Pending (0/97 judged) | 0.74 | Pending |
| Context precision | Retrieved passages are relevant | Pending (0/97 judged) | Pending (0/97 judged) | 0.71 | Pending |
| Factual correctness | Reference claims are correctly stated | Pending (0/97 judged) | Pending (0/97 judged) | 0.49 | Pending |
| Citation coverage | Answers containing at least one mapped citation | 15% (n=97) | 72% (n=97) | 98% | B > A |
| Citation precision | Citations point to a target section | 0.83 (n=15) | 0.90 (n=70) | 0.85 | Not significant |

## Interpretation and provenance

- C v1 is a historical reference generated with GPT-5.4 and judged with GPT-4o-mini. Comparisons/significance involving C are unavailable for this matched Groq experiment.
- A uses archived dense contexts. B retains five archived reranked passages and supplements from the archived A dense list, up to ten. This is a cached-context replay, not a new live retrieval run across all questions.
- Both B retrieval context and its answer prompt changed. This comparison cannot isolate which change caused the improvement. The benchmark was previously inspected, so it is not a held-out test.
- A/B significance uses the team Wilcoxon signed-rank test and Holm correction across system pairs within each metric/group. There is one comparable pair per group here; no correction across facets is applied, matching the team procedure. Exact p-values and coverage are in table_comparisons.json.
- Citation parsing reproduces the adapters: A uses [n]; B uses [n] or 【n】. Citation precision excludes unscorable answers; n is shown. This section-matching metric does not prove that each cited passage entails the claim.
- RAGAS configuration for A/B: ragas 0.4.3; Groq openai/gpt-oss-120b judge; temperature 0; output cap 4096; answer relevancy strictness 3 with BAAI/bge-small-en-v1.5 local embeddings; factual correctness F1, answer + keypoints reference, low atomicity and coverage. Team abstention handling is preserved. See ragas_coverage.json for successful, N/A, failed and missing judgments by arm/metric.
- Historical C values must not be treated as a common-judge comparison. No primary accuracy score is substituted for RAGAS. RAGAS means use successful judgments only; paired tests use the intersection of successful question IDs. Unequal coverage can make marginal means differ from paired-test means.
- Sources: answers.jsonl, replay.py, reconstructed records.jsonl, custom_scores.jsonl, frozen reports/rq2/full_v3/records.jsonl and aggregate_scores_gpt4omini.csv, and data/benchmark_qa_pool_2015.json.
