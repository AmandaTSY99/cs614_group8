# System B: Advanced Single-Pass Hybrid Retrieval Architecture

Published evaluation artifacts are limited to the report, manifest, summary JSON, and per-question CSV. Raw JSONL runs and intermediate outputs remain local and are ignored by Git. To reproduce results on another machine, obtain RAG3 and follow the setup below; local resume files are not included in a fresh clone.

Advanced single-pass RAG: RAG3 dense retrieval + Okapi BM25 + weighted score fusion + cross-encoder reranking + one optional LLM call. No query decomposition or follow-up retrieval.

## Setup

### Local Workspace Setup

The supplied `chroma_db.zip` has been extracted to `chroma_db/`. Its RAG3 collection contains 141,833 chunks. The original archives in Downloads are unchanged; the optional RAG5 merge has not been run. A local `.venv` has been installed with the baseline versions of Chroma (1.5.9), sentence-transformers (6.1.0), and OpenAI (3.31.0).

From the repository folder in PowerShell:

```powershell
$env:HF_HOME = "$PWD\.cache\huggingface"
.\.venv\Scripts\python.exe -m src.system_b --query "Who was Apple's independent auditor in fiscal 2024?" --tickers AAPL --years 2024
```

The first local retrieval check is saved in `reports/system_b/rag3_smoke.jsonl`. It uses real RAG3 chunks and models, without generation. These runs do not establish answer faithfulness. Model weights and the database are ignored by Git.

### Reproduce on another machine

Use the baseline Docker environment (`docker compose build`), then run the commands below with `docker compose run --rm jupyter` prepended. Alternatively install the repository requirements into a Python virtual environment.

Ensure the complete baseline Chroma database directory is present at `chroma_db/` (or pass `--chroma-dir`). It must contain `chroma.sqlite3` and the associated index directories. The collection is `rag3_structure_bge`; query embeddings use `BAAI/bge-small-en-v1.5`, normalized vectors, and the baseline BGE query prefix. Do not substitute BGE-m3 against these vectors. The notebook is the source of truth for how the database was built. This implementation opens an existing collection; it does not rebuild or silently replace it.

First retrieval downloads the embedding and reranking models if not cached. Default reranker: `BAAI/bge-reranker-large`; `--reranker` allows an explicit alternative. Model loading errors fail the run. Benchmark results record the selected model.

```sh
python -m src.system_b --query "What was NVIDIA's revenue?" --tickers NVDA --years 2026
python -m src.system_b --query "What was NVIDIA's revenue?" --tickers NVDA --years 2026 --generate --model YOUR_MODEL
python scripts/build_golden_eval_set.py
python -m src.system_b --benchmark data/golden_eval_set.json --limit 10 --all-modes --output reports/system_b/demo.jsonl
python -m unittest discover -s tests -v
```

For generation, set `SYSTEM_B_API_KEY` (or `OPENAI_API_KEY`), `SYSTEM_B_MODEL`, and optionally `SYSTEM_B_BASE_URL` for an OpenAI-compatible provider. Keys are read from process environment, never included in result metadata. Docker users must forward these variables with `docker compose run --rm -e SYSTEM_B_API_KEY -e SYSTEM_B_MODEL jupyter ...`. Retrieval-only is the default and performs no LLM calls. No `.env` autoloading is assumed.

## Retrieval contract and experimental controls

`Retriever.retrieve(query, Scope(tickers, years))` returns hits, component scores, configuration, and timings. `pipeline.run(...)` adds answer, usage, citation-label-to-chunk-ID mapping, and status. Both retrieval paths use identical company/year filters. Multiple ticker/year lists select their Cartesian product. For different years per company, use `Scope(filing_pairs=(("NVDA", 2026), ("TSLA", 2024)))` or the benchmark's `filing_pairs` field. Pairs are applied identically to BM25 and Chroma.

BM25 uses corpus-wide document frequencies, k1=1.5, b=0.75, and a postings index constructed once per process from Chroma's stored documents. Dense and sparse top-30 lists are merged by stable chunk ID. Scores are independently min-max normalized over each returned list; equal-score lists receive 1, missing candidates receive 0. Fusion is `alpha*dense + (1-alpha)*BM25`. At alpha=0/1, only that retrieval path's candidates participate. The top 30 fused candidates are reranked; the top 5 become context. Candidate counts and alpha are configurable. Ties use chunk ID for reproducibility.

Cross-encoder input is truncated by the model tokenizer at 512 tokens; complete original chunks remain available to generation. This limitation should be considered for long tables. Generation uses the baseline RAG prompt, one call, temperature 0, and a 1500-token output limit. Keep those settings and the generator fixed across comparisons. No financial CSV lookup or System C guardrails are added to B.

## Benchmark interpretation

### Full evaluation commands

```powershell
$env:HF_HOME = "$PWD\.cache\huggingface"
$env:SYSTEM_B_BASE_URL = 'https://api.groq.com/openai/v1'
# Set SYSTEM_B_API_KEY in the process environment before generation.
.\.venv\Scripts\python.exe -m src.system_b --benchmark data/golden_eval_set.json --all-modes --generate --model openai/gpt-oss-120b --output reports/system_b/full.jsonl
.\.venv\Scripts\python.exe scripts/summarize_system_b_eval.py reports/system_b/full.jsonl --output-dir reports/system_b/full_summary
.\.venv\Scripts\python.exe scripts/judge_system_b_eval.py reports/system_b/full.jsonl --output reports/system_b/full_judgments.jsonl
.\.venv\Scripts\python.exe scripts/summarize_system_b_eval.py reports/system_b/full.jsonl --judgments reports/system_b/full_judgments.jsonl --output-dir reports/system_b/full_summary
```

The four-mode run makes up to 240 generation calls. The optional judge makes another call per successful answer. Its correctness, faithfulness, citation-support, and numerical-accuracy ratings are provisional model judgments, not RAGAS or human-validated scores. Using the same model for generation and evaluation introduces self-evaluation bias. Null numeric/citation scores are excluded from those metric means, with sample counts reported.

Groq token-per-minute limits can cause retries. Generation retries HTTP 429 with provider retry-after delays; a daily quota error is saved and stops the batch with exit code 3. Retry time is included in generation latency. Add `--resume-from old.jsonl --output new.jsonl` to reuse matching successful rows and retry failed/unattempted rows. Retrieval-only rows are also retried when generation is requested. The old file remains unchanged. Resume checks configuration, query, scope, and generation model; do not change the underlying database/model revision between runs. Initial model loading can occur again after a resume, so timings may contain multiple cold starts.

Summary outputs include per-query CSV, status counts, reported token usage, latency percentiles, citation-label existence, and reference word-overlap F1. Word overlap is only a diagnostic proxy. If judgments are provided, their input hash and coverage are verified before aggregation.

The golden-set builder originates from `feature/golden-dataset-eval`; explicit `filing_pairs` were added to GOLD-52 and GOLD-55 to match the combinations requested in their questions. Its 60 supplied answers still require source review. These are SEC questions, not imported FinQA/TAT-QA examples. The runner respects `target_tickers` and explicit pairs for multi-company cases and marks missing requested filings as errors. It never substitutes a different year. Output is incremental JSONL; existing output files cannot be overwritten. Per-query failures yield exit status 1, setup failures 2, and daily quota exhaustion 3.

Outputs contain raw answers/evidence and timing/usage data, not claimed faithfulness scores. If an example includes reviewed `gold_chunk_ids`, evidence recall@k is computed. Citation label checks only establish that referenced labels exist; they do not prove that evidence supports a claim. RAGAS, numerical grounding evaluation, and cross-system adapters are follow-up evaluation work.

Loading the corpus/BM25 index is recorded separately as setup time. First-use retrieval timings include lazy model initialization; later calls reuse models. Separate cold and warm runs before drawing latency conclusions. No monetary cost is inferred without provider pricing. Retrieval-only runs have null answers/usage and cannot support answer-quality claims.

Suggested experiment order: validate 10 questions manually; compare four retrieval modes; tune alpha on development questions; freeze settings; evaluate held-out questions. For context-size experiments use `--top-k` while holding candidates, reranker, generator, and prompts fixed. Missing evidence labels mean evidence recall remains unreported.

## Validation status

Full 60-question run status and resume instructions: [evaluation report](../reports/system_b/EVALUATION_REPORT.md). Retrieval completed in all 240 cases after the explicit filing-pair fix; 140 answers were generated before Groq's daily quota blocked the remaining 100. The current suite has 17 passing tests.

All 11 unit tests pass, and `pip check` reports no broken requirements. Tests use deterministic fixtures to check the BM25 formula, filtering, alpha endpoints, reranking, deduplication, error propagation, citations, empty evidence, batch failures, and adapter contracts. Fixture tests are not benchmark evidence.

Local RAG3 smoke check (24 October 2026): GOLD-01 through GOLD-03 completed in all four modes (12/12 runs without execution errors). Initial corpus/BM25 setup took 23.34 seconds. Reranked retrieval took 51.04 seconds on first use (including model initialization), then 14.46 and 12.37 seconds. These three observations are not latency percentiles or a quality benchmark.

Evidence spot checks: GOLD-02's top-five reranked chunks contain Ernst & Young and the requested date; GOLD-03 retrieves Apple's address/incorporation/tax-ID table. GOLD-01's top-five chunks contain NVIDIA's fiscal year-end date but not the requested headquarters postcode, so full evidence coverage is not established. Retrieval parameters still need calibration on a development set. No LLM calls, answer-quality measurements, or RAGAS evaluations were performed in this check.

Adapter references: [Chroma collection API](https://github.com/chroma-core/chroma/blob/main/chromadb/api/models/Collection.py), [Sentence Transformers CrossEncoder](https://www.sbert.net/docs/package_reference/cross_encoder/model.html).
