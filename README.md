---
title: System C Financial RAG
emoji: 🏛️
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.45.1
app_file: app.py
pinned: false
---

# CS614 GenAI Project: Adaptive Multi-Hop RAG for SEC 10-K Financial Disclosures

**Course:** CS614 Gen AI with LLMs (SMU)  
**Integration Branch:** `dev` (System A + System B + System C Unified)  

---

## 1. Quick Links & Documentation

* 📖 **[Team Engineering & Evaluation Guide](docs/guides/TEAM_RAG_EVALUATION_GUIDE.md)** — Step-by-step instructions for running RQ1, RQ2, and RQ3 evaluations across all 4 systems.
* 🐳 **[Docker Quickstart Guide](DOCKER_QUICKSTART.md)** — One-line commands to run tests, demos, benchmarks, and Jupyter inside Docker.
* 🏛️ **[System C Architecture & Mermaid State Graph](ARCHITECTURE.md)** — Complete LangGraph specification (AMR v1 & AAMR v2).
* 🔎 **[System B Architecture & Setup Guide](docs/SYSTEM_B.md)** — BM25 + dense retrieval + weighted hybrid fusion + cross-encoder reranking.
* 📈 **[System B Evaluation Report](reports/system_b/EVALUATION_REPORT.md)** — Benchmark summary and per-query results.
* 🎤 **[Milestone 1 Demo Guide](reports/MILESTONE1_DEMO_SCRIPT.md)** — Presentation walkthrough and query execution traces.
* 📊 **[RQ3 Publication Figures](reports/figures/)** — Pareto frontier, latency distributions, and hop convergence charts.

---

## 2. Docker Quickstart (Team Standard: Zero Local Python Setup)

> [!IMPORTANT]
> **Docker Standard:** Do not install packages locally on your host machine. Docker ensures identical Python, PyTorch, and dependency versions across macOS, Windows, and Linux.

### One-Time Build
```bash
docker compose build
```

### Run Your Research Question Evaluation (Offline in 2s, $0 Cost)
All 388 benchmark outputs across the 4 RAG systems are precomputed in `reports/rq3/records.jsonl`. Teammates can immediately evaluate their RQ metrics inside Docker:

```bash
# RQ1 Evaluation: Retrieval Completeness & Cross-Section Discovery
docker compose run --rm runner python scripts/rq1/evaluate_rq1.py

# RQ2 Evaluation: Grounding, Citations & Hallucination Prevention
docker compose run --rm runner python scripts/rq2/report.py --run reports/rq2/full

# RQ3 Evaluation: Inference Economics & Cost Pareto Frontier
docker compose run --rm runner python scripts/rq3/evaluate_rq3.py
```

### Additional Common Docker Commands
```bash
# 1. Run all unit tests (< 4 sec)
docker compose run --rm runner pytest tests/ -v

# 2. Run Milestone 1 Demo Showcase (Formatted 3-query side-by-side comparison table)
docker compose run --rm runner python scripts/demo_milestone1_system_c.py --mock

# 3. Generate Publication-Quality Pareto Figures
docker compose run --rm runner python scripts/plot_rq3_pareto.py

# 4. Start interactive JupyterLab server (http://localhost:8888)
docker compose up jupyter
```

---

## 3. System A — Vanilla Dense Baseline & RAG Variants

Single-pass dense retrieval over persistent Chroma collections (`chroma_db/`) using `BAAI/bge-small-en-v1.5` embeddings, top-k retrieval, and single-pass answer generation (`openai/gpt-oss-120b` on Groq).

### RAG Variants Summary

| Variant | Chunking | Embedding model | Chroma collection | `financials.csv` in context | LLM | Where |
|---|---|---|---|---|---|---|
| RAG 1 | Fixed word windows (150 words, 30 overlap) | `all-MiniLM-L6-v2` | `rag1_words_minilm` | No | `openai/gpt-oss-120b` (Groq) | notebook only |
| RAG 2 | Fixed word windows (150 words, 30 overlap) | `BAAI/bge-small-en-v1.5` + query prefix | `rag2_words_bge` | No | `openai/gpt-oss-120b` (Groq) | notebook only |
| RAG 3 | Document structure (Items, headings, tables) | `BAAI/bge-small-en-v1.5` + query prefix | `rag3_structure_bge` | No | `openai/gpt-oss-120b` (Groq) | notebook, System A (`rag3`) |
| RAG 4 | Document structure (same index as RAG 3) | `BAAI/bge-small-en-v1.5` + query prefix | `rag3_structure_bge` | Yes | `openai/gpt-oss-120b` (Groq) | notebook, System A (`rag4`) |
| RAG 5 | Document structure, with company and fiscal year embedded in every chunk | `BAAI/bge-small-en-v1.5` + query prefix | `rag5_structure_header_bge` | No | `openai/gpt-oss-120b` (Groq) | notebook, System A (`rag5`, **default**) |
| RAG 6 | Document structure (same index as RAG 5) | `BAAI/bge-small-en-v1.5` + query prefix | `rag5_structure_header_bge` | Yes | `openai/gpt-oss-120b` (Groq) | System A (`rag6`) |

- **`financials.csv`**: reported annual figures from SEC XBRL data (FY2009 onwards: revenue, net income, operating income, total assets and liabilities, equity, cash, operating cash flow, diluted EPS).
- **Defaults in System A**: top-k = 10. Answers cite chunks like `[2]` and may be partial.

### Running System A

```bash
python -m src.system_a --query "What was NVIDIA's total revenue?" --tickers NVDA --years 2026   # RAG 5
python -m src.system_a --query "..." --tickers NVDA --years 2026 --variant rag6                # another variant
python -m src.system_a --benchmark --all-variants --limit 10                                   # compare all variants
```

`--tickers` and `--years` filter retrieval (and choose the `financials.csv` rows for RAG 4 and 6). See `python -m src.system_a --help` for all options.

---

## 4. System B — Hybrid Retrieval & Benchmark Runner

BM25 + RAG3 dense retrieval + weighted hybrid fusion + cross-encoder reranking, with a single-pass answer generator and benchmark runner. See [docs/SYSTEM_B.md](docs/SYSTEM_B.md) for setup, commands, experimental controls, and limitations.

```sh
python -m src.system_b --help
python -m unittest discover -s tests -v
```

---

## 5. Local Python Execution & Unified Streamlit Terminal

```bash
# Launch Unified Streamlit App (System C + System B + System A)
streamlit run app.py

# Run unit tests across all systems
pytest tests/ -v

# Run Milestone 1 Demo Showcase
python scripts/demo_milestone1_system_c.py --mock
```
