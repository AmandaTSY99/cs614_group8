# Active Task: System C Core Architecture & Aryan Handoff

**Current Focus:** Build and test the LangGraph state machine skeleton for System C to ensure it is executable and ready for demo at tomorrow's Milestone 1 Team Sync, then generate the handoff package for Aryan.

---

## Task Checklist

- [x] **Phase 0: Workspace Isolation & Setup**
  - [x] Isolated repo to `~/projects/cs614_group8` (non-OneDrive, non-iCloud).
  - [x] Created & checked out branch `feature/system-c-adaptive-rag`.
  - [x] Consolidated all context docs & Gantt charts into `docs/context/`.
  - [x] Created `PROJECT_CONTEXT.md` single source of truth.

- [ ] **Phase 1: System C Package Structure (`src/system_c/`)**
  - [ ] Define `src/system_c/state.py` (TypedDict state schema).
  - [ ] Implement `src/system_c/nodes/decomposer.py` (Query decomposer & planner).
  - [ ] Implement `src/system_c/nodes/critic.py` (Evidence Sufficiency Critic).
  - [ ] Implement `src/system_c/nodes/retriever.py` (Retriever interface & mock/live connector).
  - [ ] Implement `src/system_c/graph.py` (LangGraph compile with conditional routing & `max_hops=3`).
  - [ ] Implement `src/system_c/telemetry.py` (RQ3 latency & token tracker).

- [ ] **Phase 2: Validation & Milestone 1 Demo Script**
  - [ ] Create `tests/test_system_c.py` (end-to-end dry run with a multi-hop financial query).
  - [ ] Verify conditional edge logic (stops on sufficiency, loops on missing premise, hard stops at 3 hops).

- [ ] **Phase 3: Aryan Handoff Preparation**
  - [ ] Finalize `ARYAN_HANDOFF.md` with explicit integration points, prompt contracts, and citation mapper requirements.
