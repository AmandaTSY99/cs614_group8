# Docker Quickstart: Running System C & Team Benchmarks

This guide provides simple, copy-paste commands to build, test, and run **System C (Adaptive Multi-Hop RAG)** and our team benchmarks inside Docker with zero local Python setup required.

---

## 1. Prerequisites (One-Time Setup)

Make sure Docker Desktop is running on your machine:
```bash
# On macOS, launch Docker Desktop:
open -a Docker

# Verify Docker is running:
docker ps
```

---

## 2. Step 1: Build the Docker Image (One-Time)

From the project root directory (`/Users/anishdobz/projects/cs614_group8`):
```bash
docker compose build
```
*(Pre-installs CPU PyTorch, LangGraph, Pandas, Sentence-Transformers, and all dependencies in a cached layer).*

---

## 3. Step 2: Common Execution Commands

All commands mount your local directory (`.:/workspace`), so any reports, tables, or figures generated inside Docker persist directly onto your local machine.

### A. Run Fast Unit Tests (< 1 second)
```bash
docker compose run --rm system-c pytest tests/test_system_c.py -v
```

### B. Run the Milestone 1 Demo Showcase
Runs the 3 curated SEC 10-K benchmark queries (Single-Hop early stopping, MD&A + Footnotes multi-hop, and Quantitative Tabular `v1_amr` vs `v2_aamr`) and prints the formatted comparison table:
```bash
# Rapid mock mode:
docker compose run --rm system-c python scripts/demo_milestone1_system_c.py --mock

# Or live with host Ollama (qwen2.5:7b):
docker compose run --rm -e LLM_PROVIDER=ollama system-c python scripts/demo_milestone1_system_c.py
```

### C. Run the RQ3 Inference Economics Ablation Benchmark
Benchmarks Fixed 1-Hop vs. Fixed 3-Hop vs. Adaptive AMR (v1) vs. Agentic AAMR (v2) and exports CSV/JSON summaries:
```bash
docker compose run --rm system-c python scripts/run_rq3_ablation.py --mock
```

### D. Generate Publication-Quality Pareto Figures
Generates high-resolution PNG charts in `reports/figures/` (`rq3_pareto_frontier.png`, `rq3_latency_breakdown.png`, `rq3_hop_distribution.png`, and `rq3_executive_dashboard.png`):
```bash
docker compose run --rm system-c python scripts/plot_rq3_pareto.py
```

### E. Run an Interactive Ad-Hoc Financial Query
```bash
docker compose run --rm system-c python -m src.system_c.graph \
  --mode v2_aamr \
  --max-hops 3 \
  --query "Compare NVIDIA total revenue and net income between FY2025 and FY2026, and calculate the operating margin."
```

---

## 4. Step 3: Launching JupyterLab (Team Notebooks)

To start the interactive JupyterLab server on port `8888`:
```bash
docker compose up jupyter
```
Then open your browser to: **`http://localhost:8888`**  
*(Press `Ctrl + C` in your terminal to stop).*

---

## 5. Summary Cheat Sheet

| Task | One-Line Command |
| :--- | :--- |
| **Build Containers** | `docker compose build` |
| **Run Unit Tests** | `docker compose run --rm system-c pytest tests/ -v` |
| **Milestone 1 Demo** | `docker compose run --rm system-c python scripts/demo_milestone1_system_c.py --mock` |
| **RQ3 Ablation** | `docker compose run --rm system-c python scripts/run_rq3_ablation.py --mock` |
| **Plot Pareto Curves** | `docker compose run --rm system-c python scripts/plot_rq3_pareto.py` |
| **JupyterLab Server** | `docker compose up jupyter` |
