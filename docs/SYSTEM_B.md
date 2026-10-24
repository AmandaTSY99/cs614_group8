# System B — Kevin

Advanced single-pass RAG: RAG3 dense retrieval + Okapi BM25 + weighted score fusion + cross-encoder reranking + one optional LLM call. No query decomposition or follow-up retrieval.

## Setup

Use the baseline Docker environment (`docker compose build`), then run the commands below with `docker compose run --rm jupyter` prepended. Alternatively install the repository requirements into a Python virtual environment.

Copy Amanda's complete Chroma database directory to `chroma_db/` (or pass `--chroma-dir`). It must contain `chroma.sqlite3` and the associated index directories. The collection is `rag3_structure_bge`; query embeddings use `BAAI/bge-small-en-v1.5`, normalized vectors, and the baseline BGE query prefix. Do not substitute BGE-m3 against these vectors. The notebook is the source of truth for how the database was built. This implementation opens an existing collection; it does not rebuild or silently replace it.

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

`Retriever.retrieve(query, Scope(tickers, years))` returns hits, component scores, configuration, and timings. `pipeline.run(...)` adds answer, usage, citation-label-to-chunk-ID mapping, and status. Both retrieval paths use identical company/year filters. Multiple tickers and years select their Cartesian product; exact company/year pair scopes are not supported yet.

BM25 uses corpus-wide document frequencies, k1=1.5, b=0.75, and a postings index constructed once per process from Chroma's stored documents. Dense and sparse top-30 lists are merged by stable chunk ID. Scores are independently min-max normalized over each returned list; equal-score lists receive 1, missing candidates receive 0. Fusion is `alpha*dense + (1-alpha)*BM25`. At alpha=0/1, only that retrieval path's candidates participate. The top 30 fused candidates are reranked; the top 5 become context. Candidate counts and alpha are configurable. Ties use chunk ID for reproducibility.

Cross-encoder input is truncated by the model tokenizer at 512 tokens; complete original chunks remain available to generation. This limitation should be considered for long tables. Generation uses the baseline RAG prompt, one call, temperature 0, and a 1500-token output limit. Keep those settings and the generator fixed across comparisons. No financial CSV lookup or System C guardrails are added to B.

## Benchmark interpretation

The golden-set builder is reused unchanged from `feature/golden-dataset-eval`; its 60 supplied answers still require source review. These are SEC questions, not imported FinQA/TAT-QA examples. The runner respects `target_tickers` for multi-company cases and marks missing requested filings as errors. It never substitutes a different year. Output is incremental JSONL; existing output files cannot be overwritten. Any per-query failure yields exit status 1; setup failures yield 2.

Outputs contain raw answers/evidence and timing/usage data, not claimed faithfulness scores. If an example includes reviewed `gold_chunk_ids`, evidence recall@k is computed. Citation label checks only establish that referenced labels exist; they do not prove that evidence supports a claim. RAGAS, numerical grounding evaluation, and cross-system adapters are follow-up evaluation work.

Loading the corpus/BM25 index is recorded separately as setup time. First-use retrieval timings include lazy model initialization; later calls reuse models. Separate cold and warm runs before drawing latency conclusions. No monetary cost is inferred without provider pricing. Retrieval-only runs have null answers/usage and cannot support answer-quality claims.

Suggested experiment order: validate 10 questions manually; compare four retrieval modes; tune alpha on development questions; freeze settings; evaluate held-out questions. For context-size experiments use `--top-k` while holding candidates, reranker, generator, and prompts fixed. Missing evidence labels mean evidence recall remains unreported.

## Validation status

Unit tests use deterministic fixtures to check the BM25 formula, filtering, alpha endpoints, reranking, deduplication, error propagation, citations, and empty evidence. Live RAG3/model/provider validation requires the externally supplied database and installed dependencies. Fixture tests are not benchmark evidence.

Adapter references: [Chroma collection API](https://github.com/chroma-core/chroma/blob/main/chromadb/api/models/Collection.py), [Sentence Transformers CrossEncoder](https://www.sbert.net/docs/package_reference/cross_encoder/model.html).
