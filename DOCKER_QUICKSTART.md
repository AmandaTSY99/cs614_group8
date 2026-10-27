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

## 5. Guardrail, Citations & RQ2 Evaluation

**System C (`system-c` service): no changes needed.** The guardrail, synthesizer, citation and generator code use no new packages, so the existing `Dockerfile` and `docker-compose.yaml` work as they are. To run its tests: `docker compose run --rm system-c pytest tests/ -q`. For a live run you can point the guardrail judge at a different model with `GUARDRAIL_JUDGE_PROVIDER` / `GUARDRAIL_JUDGE_MODEL` (for example in `.env`; unset = same model as System C).

**RQ2 evaluation uses two images** because RAGAS needs `openai` 1.x while `requirements.txt` pins 3.x:

| Stage | Service | Image |
| :--- | :--- | :--- |
| 1. Generate answers (runs System C) | `system-c` | `Dockerfile` (no RAGAS) |
| 2. Score + report (RAGAS judge) | `rq2-eval` | `Dockerfile.eval` (`requirements.txt` + `requirements-eval.txt`) |

The stages only talk through the files in `reports/rq2/<run_id>/` (the project folder is mounted).
```bash
# Stage 1 (live, needs OPENAI_API_KEY in .env):
docker compose run --rm -e LLM_PROVIDER=openai system-c python scripts/rq2/generate.py --systems system_c_v1,system_c_v2 --run-id smoke --ids GOLD-01,GOLD-21,GOLD-56

# Stage 2 (runs score.py then report.py; judge defaults to OpenAI gpt-4o-mini):
docker compose run --rm rq2-eval
# Another run or scores file: docker compose run --rm -e RQ2_RUN=reports/rq2/full -e RQ2_SCORES_FILE=scores_gpt4omini.jsonl rq2-eval

# Offline tests (no API calls):
docker compose run --rm system-c pytest tests/ -q
docker compose run --rm rq2-eval pytest tests/ -q
```
Build the images once with `docker compose build system-c rq2-eval`. The first `rq2-eval` scoring run also downloads the local embedding model (`BAAI/bge-small-en-v1.5`, about 130 MB) into the `hf-cache` volume.

---

## 6. Summary Cheat Sheet

| Task | One-Line Command |
| :--- | :--- |
| **Build Containers** | `docker compose build` |
| **Run Unit Tests** | `docker compose run --rm system-c pytest tests/ -v` |
| **Milestone 1 Demo** | `docker compose run --rm system-c python scripts/demo_milestone1_system_c.py --mock` |
| **RQ3 Ablation** | `docker compose run --rm system-c python scripts/run_rq3_ablation.py --mock` |
| **Plot Pareto Curves** | `docker compose run --rm system-c python scripts/plot_rq3_pareto.py` |
| **JupyterLab Server** | `docker compose up jupyter` |
| **RQ2 Score + Report** | `docker compose run --rm rq2-eval` |
