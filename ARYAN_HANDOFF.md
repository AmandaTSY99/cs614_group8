# Aryan Handoff: System C Integration & Deliverables

**To:** Aryan  
**From:** Anish  
**Branch:** `feature/system-c-adaptive-rag`  
**Target Milestone:** Milestone 1 (Sun, 25 Oct) & Checkpoint 2 (Thu, 29 Oct)

---

## 1. What Has Been Built & Orchestrated (Anish's Part)

I have built and tested the core LangGraph state machine skeleton for **System C (Adaptive Multi-Hop RAG)** located under `src/system_c/`:
1. **`src/system_c/state.py`**: The central `AdaptiveRAGState` TypedDict holding query context, accumulated evidence chunks, intermediate answers, hop counter, sufficiency status, and telemetry.
2. **`src/system_c/nodes/decomposer.py`**: The Query Decomposer node that splits broad financial queries into atomic sub-goals (e.g. Hop 1: Definition/Context, Hop 2: Quantitative Metrics).
3. **`src/system_c/nodes/critic.py`**: The Evidence Sufficiency Critic node (Self-RAG style) that inspects accumulated evidence and decides whether the LLM has enough information to synthesize an answer or must loop back for more evidence.
4. **`src/system_c/graph.py`**: The LangGraph state graph wiring conditional routing edges with a hard limit of `max_hops = 3` to prevent infinite loops.
5. **`src/system_c/telemetry.py`**: Telemetry hooks capturing latency, hop count, and token usage for our **RQ3 (Inference Economics)** ablation.

---

## 2. Your Module Ownership & Next Tasks (Aryan's Part)

Your primary responsibilities are **Conditioned Sub-Query Generation**, **Synthesizer & Citation Grounding**, and **Hallucination Defense (RQ2 Lead)**:

### Deliverable A: Conditioned Sub-Query Generator (`src/system_c/nodes/generator.py`)
* **Purpose:** When the Critic node flags `is_sufficient = False`, this node generates a new, targeted sub-query conditioned on what was already retrieved in earlier hops (e.g., retrieving details on a specific credit agreement or footnote discovered in Hop 1).
* **Input:** `AdaptiveRAGState` (specifically `accumulated_evidence` and `critic_reasoning`).
* **Output:** Updated `current_sub_query`.

### Deliverable B: Answer Synthesizer & Citation Mapping (`src/system_c/nodes/synthesizer.py`)
* **Purpose:** Once evidence is deemed sufficient, synthesize a clear, financial-grade response.
* **Requirement:** Every single factual claim or dollar figure must be cited with an inline markdown citation tag referencing the exact section and table row:
  * Example: `Operating margin contracted by 140 bps [Item 7, Table 4, Row 'Operating Margin'] due to FX headwinds [Item 7A, p. 45].`
* **Output:** Updates `final_answer` and populates `citations` list in the state.

### Deliverable C: Active Hallucination & Numerical Guardrail (`src/system_c/guardrails/`)
* **Purpose:** Validate that generated numbers strictly exist in the cited context (supporting **RQ2: Factual Faithfulness**).
* **Implementation:** A post-synthesis verification check or reflection prompt that compares dollar amounts, percentages, and dates in `final_answer` against `accumulated_evidence`.

### Deliverable D: Slide Deck Lead & RQ2 Benchmark Reporting
* Lead the visual slides for System C's architecture flow and RQ2 results (Faithfulness & Citation F1) using the test harness provided by Kevin.

---

## 3. How to Run & Verify

1. Activate your Python environment:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the test suite:
   ```bash
   pytest tests/test_system_c.py -v
   ```
3. Run a sample query through System C:
   ```bash
   python -m src.system_c.graph --query "How did foreign exchange headwinds in 2024 impact gross margin, and what covenants restricted debt financing?"
   ```
