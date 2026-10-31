# CS614 GenAI Project: Adaptive Multi-Hop RAG for SEC 10-K Financial Disclosures

**Course:** CS614 Generative AI with LLMs (SMU)  
**System Comparison:** System A (Vanilla Dense) vs. System B (Hybrid Rerank) vs. System C v1 (Adaptive Multi-Hop) vs. System C v3 (Adaptive Agentic Multi-Hop with Schema-Aware Sufficiency & Guardrails)  

---

## 1. Quick Links & Documentation

* 📖 **[Team Engineering & Evaluation Guide](docs/guides/TEAM_RAG_EVALUATION_GUIDE.md)** — Step-by-step instructions for running RQ1, RQ2, and RQ3 evaluations across all 4 systems.
* 🐳 **[Docker Quickstart Guide](DOCKER_QUICKSTART.md)** — One-line commands to run tests, demos, benchmarks, and Jupyter inside Docker.
* 🏛️ **[System C Architecture & Mermaid State Graph](ARCHITECTURE.md)** — Complete LangGraph specification (AMR v1 & AAMR-SG v3).
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

## 3. The 4 Benchmark Architectures Under Evaluation

Our research evaluates four distinct RAG architectures on complex SEC Form 10-K financial queries:

| Architecture | Retrieval Paradigm | Chunking & Indexing | Hop Control | Financial Tools & Guardrails |
| :--- | :--- | :--- | :---: | :--- |
| **`system_a`** (Vanilla Dense Baseline) | Top-10 Dense Vector Search | Structure-Preserving + Filing Headers (`rag5`) | 1-Hop | Single-pass generation; direct citation tags |
| **`system_b`** (Advanced Hybrid Single-Pass) | Okapi BM25 + BGE-Small Dense + Cross-Encoder Reranker | Structure-Preserving (`rag3`) | 1-Hop | Min-Max weighted score fusion ($\alpha=0.50$) |
| **`system_c_v1`** (Adaptive Multi-Hop AMR) | Iterative Multi-Hop Hybrid Retrieval | Structure-Preserving + Deduplication | Dynamic (1 to 3 hops) | Evidence Sufficiency Critic reflection loop + Numerical Guardrail |
| **`system_c_v3`** (Agentic Multi-Hop AAMR-SG) | Autonomous Schema-Aware Sufficiency + Multi-Hop Hybrid | Structure-Preserving + Table Stitching + Deduplication | Dynamic (1 to 3 hops) | Pre-routes to SEC XBRL financial statements (`financials.csv`) + Structural table continuity detector + Time-series consistency + Numerical Guardrail |

<details>
<summary><b>Note on Baseline Development Variants (RAG 1 to RAG 6)</b></summary>

During early Phase 1 baseline development, six incremental chunking/embedding techniques were explored in `build_vdb_base_RAG.ipynb`:
- **RAG 1:** Fixed word windows (150 words) with `all-MiniLM-L6-v2`.
- **RAG 2:** Fixed word windows with `BAAI/bge-small-en-v1.5`.
- **RAG 3:** Document structure-preserving chunking (`rag3_structure_bge`).
- **RAG 4:** Structure chunking + inline XBRL summary injection.
- **RAG 5:** Structure chunking with contextual filing headers (`rag5_structure_header_bge`) — *Selected as the official System A baseline*.
- **RAG 6:** RAG 5 with inline XBRL summary injection.
</details>

---

## 4. Standalone System Execution (CLI)

### System A (Vanilla Dense Baseline)
```bash
python -m src.system_a --query "What was NVIDIA's total revenue?" --tickers NVDA --years 2026
```

### System B (Hybrid Sparse-Dense + Cross-Encoder Rerank)
```bash
python -m src.system_b --query "What was NVIDIA's total revenue?" --tickers NVDA --years 2026
```

### System C (Adaptive Multi-Hop State Machine)
```bash
# AMR (v1: Adaptive Multi-Hop)
python -m src.system_c.graph --mode v1_amr --query "What was NVIDIA's revenue and gross margin in FY2026?"

# AAMR-SG (v3: Agentic Multi-Hop with Schema-Aware Sufficiency & Table Continuity)
python -m src.system_c.graph --mode v3_aamr_sg --query "Compare NVIDIA and Apple total revenue in 2024."
```

---

## 5. Unified Streamlit Terminal & Local API Gateway

### Launch Interactive Streamlit UI
```bash
streamlit run app.py
```
Provides side-by-side execution trace comparisons across System A, System B, and System C with full evidence inspection, citation graph mapping, and numerical guardrail reports.

### Launch FastAPI Microservice Gateway
```bash
python run_api.py
```
Interactive Swagger documentation available at `http://localhost:8000/docs`.
