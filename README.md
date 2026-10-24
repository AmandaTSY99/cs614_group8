# CS614 GenAI Project: Adaptive Multi-Hop RAG for SEC 10-K Financial Disclosures

**Course:** CS614 Gen AI with LLMs (SMU)  
**Upcoming Milestone:** Milestone 1 — Team Sync & 3-System Benchmark (25 Oct 2026)  
**Integration Branch:** `feature/system-c-adaptive-rag`  

---

## 1. Quick Links & Documentation

* 🐳 **[Docker Quickstart Guide](DOCKER_QUICKSTART.md)** — One-line commands to run tests, demos, and ablations inside Docker.
* 🏛️ **[System Architecture & Mermaid State Graph](ARCHITECTURE.md)** — Complete LangGraph specification (AMR v1 & AAMR v2).
* 🎤 **[Milestone 1 Demo Guide & Speaking Script](reports/MILESTONE1_DEMO_SCRIPT.md)** — Step-by-step presentation script and query traces.
* 🤝 **[Aryan Handoff & Module Contracts](ARYAN_HANDOFF.md)** — Plug-and-play contracts for Citations, Guardrails, and RQ2.
* 📊 **[RQ3 Publication Figures](reports/figures/)** — Pareto frontier, latency distributions, and hop convergence charts.

---

## 2. Fast Docker Commands (No Local Python Setup Needed)

```bash
# 1. Run unit tests (< 1 sec)
docker compose run --rm system-c pytest tests/test_system_c.py -v

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

## 3. Local Python Execution (Alternative)

If running outside Docker using local Python (`/opt/anaconda3/bin/python`):

```bash
# Run tests
pytest tests/test_system_c.py -v

# Run Milestone 1 Demo Showcase
python scripts/demo_milestone1_system_c.py --mock

# Run live with local Ollama (qwen2.5:7b)
python scripts/demo_milestone1_system_c.py
```
