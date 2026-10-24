"""
FastAPI Enterprise Gateway & Streaming Microservice for System C.

Owned by: Anish (System Architect & Orchestration Lead)

Endpoints:
1. `GET /`: Health check, active LLM provider, database connection status, and API routes.
2. `POST /api/v1/query`: Synchronous / full-state execution returning verified answer, citations, guardrail audit, and RQ3 telemetry.
3. `POST /api/v1/query/stream`: Real-time Server-Sent Events (SSE) streaming node-by-node execution trace and answer chunks.
4. `GET /api/v1/financials/{ticker}`: Direct SQL access to Supabase `sec_financials` XBRL store.

Interactive Swagger documentation available at `http://localhost:8000/docs`.
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv(override=True)

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from src.system_c.graph import run_system_c
from src.system_c.llm import get_llm_config
from src.system_c.state import AdaptiveRAGState

app = FastAPI(
    title="System C: Enterprise Adaptive Multi-Hop Financial RAG",
    description="CS614 SEC 10-K Adaptive Multi-Hop State Machine (AMR v1 & Agentic AAMR v2) with Live Supabase XBRL Storage and Closed-Loop Self-Healing.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for frontend clients (React / Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Request & Response Schemas ---

class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        description="The financial question to evaluate over SEC 10-K filings.",
        examples=["Compare NVIDIA and Apple operating margin and AI supply chain risks in 2024"],
    )
    mode: str = Field(
        default="v2_aamr",
        description="Execution mode: 'v1_amr' (Adaptive Multi-Hop) or 'v2_aamr' (Agentic Tabular XBRL + Adaptive).",
        examples=["v2_aamr"],
    )
    max_hops: int = Field(default=3, ge=1, le=5, description="Maximum iterative retrieval hops.")
    target_ticker: Optional[str] = Field(default=None, description="Primary ticker override (e.g. 'NVDA').")
    fiscal_years: Optional[List[int]] = Field(default=None, description="Fiscal years override (e.g. [2024, 2026]).")
    force_max_hops: bool = Field(default=False, description="Disable early-stopping for fixed-hop ablation benchmarking.")
    sufficiency_threshold: float = Field(default=0.85, ge=0.5, le=1.0, description="Early-stopping sufficiency score threshold.")
    max_repairs: int = Field(default=1, ge=0, le=3, description="Hard ceiling on closed-loop hallucination repair passes.")
    thread_id: Optional[str] = Field(default=None, description="Optional session/thread ID for persistent state checkpointing in Supabase.")


class QueryResponse(BaseModel):
    query: str
    mode: str
    thread_id: Optional[str] = None
    target_ticker: Optional[str]
    target_tickers: List[str]
    fiscal_years: List[int]
    hops_executed: int
    max_hops: int
    early_stopped: bool
    sufficiency_score: float
    final_answer: str
    citations: List[Dict[str, Any]]
    guardrail_passed: bool
    guardrail_report: Dict[str, Any]
    repair_count: int
    repair_history: List[Dict[str, Any]]
    intermediate_answers: List[Dict[str, Any]]
    telemetry: Dict[str, Any]


# --- API Routes ---

@app.get("/", tags=["Health & Status"])
def health_check() -> Dict[str, Any]:
    """Return microservice health status, active LLM provider, and cloud database connectivity."""
    provider, model = get_llm_config()
    supabase_connected = bool(os.getenv("SUPABASE_DB_URL"))
    return {
        "status": "online",
        "system": "System C (Adaptive Multi-Hop Financial RAG)",
        "version": "2.0.0",
        "llm_engine": {
            "provider": provider,
            "model": model,
        },
        "cloud_database": {
            "type": "Supabase PostgreSQL (AWS ap-southeast-1)",
            "connected": supabase_connected,
            "table": "sec_financials (272 XBRL filing records)",
            "checkpoints_active": supabase_connected,
        },
        "docs_url": "/docs",
    }


@app.post("/api/v1/query", response_model=QueryResponse, tags=["RAG Execution"])
def execute_query(req: QueryRequest) -> QueryResponse:
    """
    Execute a financial query end-to-end through the System C LangGraph state machine.
    Returns the citation-grounded final answer, guardrail audit, and RQ3 inference economics metrics.
    Supports persistent state checkpointing in Supabase when `thread_id` is supplied.
    """
    try:
        # Sanitize Swagger UI default placeholder inputs ("string", 0, etc.)
        ticker = None if req.target_ticker in (None, "", "string") else req.target_ticker
        years = None if not req.fiscal_years or req.fiscal_years == [0] else [y for y in req.fiscal_years if y > 1900]
        thread_id = None if req.thread_id in (None, "", "string") else req.thread_id

        db_url = os.getenv("SUPABASE_DB_URL")
        if thread_id and db_url:
            from langgraph.checkpoint.postgres import PostgresSaver

            with PostgresSaver.from_conn_string(db_url) as checkpointer:
                final_state: AdaptiveRAGState = run_system_c(
                    query=req.query,
                    max_hops=req.max_hops,
                    mode=req.mode,
                    target_ticker=ticker,
                    fiscal_years=years,
                    force_max_hops=req.force_max_hops,
                    sufficiency_threshold=req.sufficiency_threshold,
                    max_repairs=req.max_repairs,
                    checkpointer=checkpointer,
                    thread_id=thread_id,
                )
        else:
            final_state: AdaptiveRAGState = run_system_c(
                query=req.query,
                max_hops=req.max_hops,
                mode=req.mode,
                target_ticker=ticker,
                fiscal_years=years,
                force_max_hops=req.force_max_hops,
                sufficiency_threshold=req.sufficiency_threshold,
                max_repairs=req.max_repairs,
            )

        telemetry = final_state.get("telemetry", {})
        rq3_summary = telemetry.get("rq3_summary", {})

        return QueryResponse(
            query=final_state["original_query"],
            mode=final_state["mode"],
            thread_id=req.thread_id,
            target_ticker=final_state.get("target_ticker"),
            target_tickers=final_state.get("target_tickers", []),
            fiscal_years=final_state.get("fiscal_years", []),
            hops_executed=final_state.get("current_hop", 1),
            max_hops=final_state.get("max_hops", 3),
            early_stopped=rq3_summary.get("early_stopped", False),
            sufficiency_score=final_state.get("sufficiency_score", 0.0),
            final_answer=final_state.get("final_answer") or final_state.get("draft_answer") or "No answer generated.",
            citations=final_state.get("citations", []),
            guardrail_passed=final_state.get("guardrail_passed", True),
            guardrail_report=final_state.get("guardrail_report", {}),
            repair_count=final_state.get("repair_count", 0),
            repair_history=final_state.get("repair_history", []),
            intermediate_answers=final_state.get("intermediate_answers", []),
            telemetry=telemetry,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System C execution failure: {str(e)}")


@app.post("/api/v1/query/stream", tags=["Streaming Execution"])
async def stream_query(req: QueryRequest):
    """
    Stream live execution trajectory and answer generation via Server-Sent Events (SSE).
    Enables interactive browser streaming for presentations and user interfaces.
    """
    async def event_generator():
        yield f"data: {json.dumps({'event': 'started', 'query': req.query, 'mode': req.mode})}\n\n"
        await asyncio.sleep(0.05)

        ticker = None if req.target_ticker in (None, "", "string") else req.target_ticker
        years = None if not req.fiscal_years or req.fiscal_years == [0] else [y for y in req.fiscal_years if y > 1900]

        # Run pipeline
        loop = asyncio.get_event_loop()
        final_state = await loop.run_in_executor(
            None,
            lambda: run_system_c(
                query=req.query,
                max_hops=req.max_hops,
                mode=req.mode,
                target_ticker=ticker,
                fiscal_years=years,
                force_max_hops=req.force_max_hops,
                sufficiency_threshold=req.sufficiency_threshold,
                max_repairs=req.max_repairs,
            )
        )

        # Stream planning trace
        yield f"data: {json.dumps({'event': 'planning', 'tickers': final_state.get('target_tickers'), 'sub_queries': final_state.get('sub_queries')})}\n\n"
        await asyncio.sleep(0.05)

        # Stream hop reflection trace
        for step in final_state.get("intermediate_answers", []):
            yield f"data: {json.dumps({'event': 'reflection', 'hop': step.get('hop'), 'score': step.get('sufficiency_score'), 'is_sufficient': step.get('is_sufficient'), 'reasoning': step.get('critic_reasoning')})}\n\n"
            await asyncio.sleep(0.05)

        # Stream answer
        answer = final_state.get("final_answer", "")
        yield f"data: {json.dumps({'event': 'answer', 'text': answer})}\n\n"
        await asyncio.sleep(0.05)

        # Stream guardrail & summary
        yield f"data: {json.dumps({
            'event': 'completed',
            'guardrail_passed': final_state.get('guardrail_passed'),
            'citations_count': len(final_state.get('citations', [])),
            'total_latency_ms': final_state.get('telemetry', {}).get('rq3_summary', {}).get('total_latency_ms'),
            'total_tokens': final_state.get('telemetry', {}).get('total_tokens'),
            'estimated_cost_usd': final_state.get('telemetry', {}).get('estimated_cost_usd'),
        })}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.get("/api/v1/financials/{ticker}", tags=["Supabase XBRL Store"])
def get_company_financials(ticker: str, year: Optional[int] = Query(None, description="Optional fiscal year filter")) -> Dict[str, Any]:
    """Query live Supabase PostgreSQL `sec_financials` table directly for reported accounting figures."""
    db_url = os.getenv("SUPABASE_DB_URL")
    if not db_url:
        raise HTTPException(status_code=503, detail="Supabase database is not configured in .env.")
    try:
        import psycopg2
        query = """
            SELECT ticker, fiscal_year, fiscal_year_end, revenue, net_income,
                   operating_income, total_assets, total_liabilities,
                   stockholders_equity, cash_and_equivalents, operating_cash_flow, eps_diluted
            FROM sec_financials
            WHERE ticker = %s
        """
        params = [ticker.upper()]
        if year:
            query += " AND fiscal_year = %s"
            params.append(year)
        query += " ORDER BY fiscal_year DESC;"

        with psycopg2.connect(db_url, sslmode="require", connect_timeout=4) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                columns = [desc[0] for desc in cur.description]
                rows = [dict(zip(columns, row)) for row in cur.fetchall()]

        if not rows:
            raise HTTPException(status_code=404, detail=f"No financial records found for ticker '{ticker.upper()}'.")

        return {
            "ticker": ticker.upper(),
            "count": len(rows),
            "records": rows,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    print("\nStarting System C FastAPI Microservice on http://localhost:8000 ...")
    print("Interactive Swagger UI at: http://localhost:8000/docs\n")
    uvicorn.run("src.system_c.api:app", host="0.0.0.0", port=8000, reload=True)
