# System B evaluation — 24 October 2026

GitHub contains this report, the compact [summary](full_eval_summary/summary.json), [per-question results](full_eval_summary/per_query.csv), and [run manifest](full_eval_manifest.json). Raw JSONL runs, intermediate files, databases, and model caches are intentionally local-only. The resume command below requires the local raw results; a fresh clone can start a new run using the commands in [System B setup](../../docs/SYSTEM_B.md).

## Completion and limits

All 60 questions ran through all four retrieval modes: **240 successful retrieval runs** after correcting two company/year scope errors. **140 answers were generated** (GOLD-01 through GOLD-35 in every mode). The remaining **100 runs are retrieval-only** because Groq rejected further generations at the organization's 200,000-token-per-day quota. The replacement API key belonged to the same organization and shared that quota.

The final consolidated file is `evaluation_60_all_modes.jsonl`. Each row records its source result file; retrieval-only rows explicitly record that generation was blocked. Raw failed/interrupted attempts are retained separately for auditing and are not counted as successful answers. No API keys were saved in repository files.

## Results on the same 35 answered questions

| Retrieval mode | Generated | Pure abstentions | Median elapsed/query | Reported tokens |
|---|---:|---:|---:|---:|
| Dense | 35 | 29 | 5.15 s | 45,368 |
| BM25 | 35 | 26 | 9.39 s | 50,441 |
| Hybrid | 35 | 24 | 10.25 s | 50,269 |
| Hybrid + reranker (System B) | 35 | 22 | 17.97 s | 54,897 |

A pure abstention means the entire answer is “Not found in the provided context.” Other answers can still be partial or incorrect. Latencies include rate-limit waiting and initial model loading, exclude corpus setup, and must not be interpreted as isolated model-compute benchmarks. Reported tokens total 200,975 across successful responses; failed-request usage may not be included.

Reranking reduced abstentions but **22/35 System B answers still abstained**. This configuration is not yet a reliable general financial-question demo. GOLD-25 illustrates a partial response: it reports several Alphabet figures but omits 2024 operating cash flow. GOLD-30's JPMorgan values match the supplied reference answer. Those spot checks are not a comprehensive correctness audit.

All recognized numeric citation labels referred to existing retrieved chunks. That does not establish that the citations support the claims. Reference word-overlap diagnostics are in `full_eval_summary/summary.json` and `per_query.csv`; they are not answer accuracy or faithfulness scores.

## Experimental setup

- RAG3: `rag3_structure_bge`, 141,833 chunks; BGE-small-en-v1.5 embeddings.
- BM25: k1=1.5, b=0.75; alpha=0.5; 30 candidates per retrieval path; 30 reranked candidates; top-5 final context.
- Reranker: `BAAI/bge-reranker-large`, 512-token query/document input limit.
- Generator: Groq `openai/gpt-oss-120b`, temperature 0, max output tokens 1,500, one generation pass.
- GOLD-52 and GOLD-55 initially failed because Cartesian company/year validation required nonexistent META FY2026 and TSLA FY2026 filings. Added explicit filing pairs from the question wording and successfully reran all eight affected retrieval checks. Reference answers and question wording were not changed.
- The first 35 questions cover factual and numerical tiers. The cross-section and multi-company tiers have retrieval results but no generated answers; do not generalize the generation comparison to all 60 questions.

## Not completed

The remaining 100 generations and model-assisted evaluation are quota-blocked. The evaluator probe was rate-limited, so no model-judged quality scores are reported. RAGAS, reviewed evidence-recall labels, a comprehensive numerical audit, alpha sweeps, and context-size sweeps are not part of these results. The reference answers still require independent source review.

## Resume without repeating successful generations

Once quota is available, set `SYSTEM_B_API_KEY` in the process environment (a new key in the same exhausted organization does not add quota), then run from the repository root:

```powershell
$env:HF_HOME = "$PWD\.cache\huggingface"
$env:SYSTEM_B_BASE_URL = 'https://api.groq.com/openai/v1'
.\.venv\Scripts\python.exe -m src.system_b --benchmark data/golden_eval_set.json --all-modes --generate --model openai/gpt-oss-120b --resume-from reports/system_b/evaluation_60_all_modes.jsonl --output reports/system_b/evaluation_resumed.jsonl
```

Use a new output filename each time. Existing successful answers are reused; retrieval-only and failed rows are retried. The runner now stops on daily-quota exhaustion with exit code 3. Improvements were validated with 17 passing software tests; those tests do not measure answer quality.
