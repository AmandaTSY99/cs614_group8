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
**Upcoming Milestone:** Milestone 1 — Team Sync & 3-System Benchmark (25 Oct 2026)  
**Integration Branch:** `dev` (System B + System C Unified)  

---

## 1. Quick Links & Documentation

* 🐳 **[Docker Quickstart Guide](DOCKER_QUICKSTART.md)** — One-line commands to run tests, demos, and ablations inside Docker.
* 🏛️ **[System C Architecture & Mermaid State Graph](ARCHITECTURE.md)** — Complete LangGraph specification (AMR v1 & AAMR v2).
* 🔎 **[System B Setup & Evaluation Guide (Kevin)](docs/SYSTEM_B.md)** — BM25 + RAG3 dense retrieval + weighted hybrid fusion + cross-encoder reranking.
* 📈 **[System B Evaluation Report](reports/system_b/EVALUATION_REPORT.md)** — Compact benchmark summary and per-query results.
* 🎤 **[Milestone 1 Demo Guide & Speaking Script](reports/MILESTONE1_DEMO_SCRIPT.md)** — Step-by-step presentation script and query traces.
* 🤝 **[Aryan Handoff & Module Contracts](docs/handoffs/ARYAN_HANDOFF.md)** — Plug-and-play contracts for Citations, Guardrails, and RQ2.
* 📊 **[RQ3 Publication Figures](reports/figures/)** — Pareto frontier, latency distributions, and hop convergence charts.

---

## 2. Fast Docker Commands (No Local Python Setup Needed)

```bash
# 1. Run unit tests (< 1 sec)
docker compose run --rm system-c pytest tests/test_system_c.py tests/test_system_b.py tests/test_system_b_eval.py -v

# 2. Run Milestone 1 Demo Showcase (Formatted 3-query side-by-side comparison table)
docker compose run --rm system-c python scripts/demo_milestone1_system_c.py --mock

# 3. Run RQ3 Inference Economics Ablation Benchmark (Fixed 1-Hop vs Fixed 3-Hop vs Adaptive)
docker compose run --rm system-c python scripts/run_rq3_ablation.py --mock

# 4. Generate Publication-Quality Pareto Figures
docker compose run --rm system-c python scripts/plot_rq3_pareto.py

# 5. Start interactive JupyterLab
docker compose up jupyter
```

---

## 3. System B (Kevin) — Hybrid Retrieval & Benchmark Runner

BM25 + RAG3 dense retrieval + weighted hybrid fusion + cross-encoder reranking, with a single-pass answer generator and benchmark runner. See [docs/SYSTEM_B.md](docs/SYSTEM_B.md) for setup, commands, experimental controls, and limitations.

```sh
python -m src.system_b --help
python -m unittest discover -s tests -v
```

---

## 4. Local Python Execution (System C & Interactive Streamlit Terminal)

```bash
# Launch Unified Streamlit App (System C + System B)
streamlit run app.py

# Run tests
pytest tests/test_system_c.py tests/test_system_b.py tests/test_system_b_eval.py -v

# Run Milestone 1 Demo Showcase
python scripts/demo_milestone1_system_c.py --mock
```
