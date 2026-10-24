"""
Agentic Tabular Financials Lookup Tool for System C v2 (AAMR).

Adapts Amanda's `lookup_financials` (`build_vdb_base_RAG.ipynb` Section 3.5) into an
autonomous LangGraph tool node so System C v2 only fetches structured XBRL figures
when the Query Decomposer / Planner detects quantitative or ratio requirements.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from src.system_c.corpus import DATA_DIR, METRICS
from src.system_c.state import AdaptiveRAGState, EvidenceChunk
from src.system_c.telemetry import track_node_latency

_FINANCIALS_DF: Optional[pd.DataFrame] = None


def _get_financials_df(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    global _FINANCIALS_DF
    if _FINANCIALS_DF is not None:
        return _FINANCIALS_DF
    fin_path = data_dir / "financials.csv"
    idx_path = data_dir / "filings_index.csv"
    if not fin_path.exists() or not idx_path.exists():
        return pd.DataFrame()
    df = pd.read_csv(fin_path, dtype={"accession": str}).merge(
        pd.read_csv(idx_path, dtype=str)[["accession", "local_folder"]],
        on="accession",
    )
    df["fiscal_year"] = df["local_folder"].map(lambda folder: int(Path(folder).name[2:6]))
    _FINANCIALS_DF = df
    return df


def _lookup_financials_supabase(ticker: str, fiscal_year: Optional[int] = None) -> Optional[str]:
    """Query live Supabase PostgreSQL `sec_financials` table for structured XBRL figures."""
    db_url = os.getenv("SUPABASE_DB_URL")
    if not db_url:
        return None
    try:
        import psycopg2

        query = """
            SELECT fiscal_year, fiscal_year_end, revenue, net_income,
                   operating_income, total_assets, total_liabilities,
                   stockholders_equity, cash_and_equivalents,
                   operating_cash_flow, eps_diluted
            FROM sec_financials
            WHERE ticker = %s
        """
        params = [ticker]
        if fiscal_year:
            query += " AND fiscal_year = %s"
            params.append(int(fiscal_year))
        query += " ORDER BY fiscal_year ASC;"

        with psycopg2.connect(db_url, sslmode="require", connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                rows = cur.fetchall()

        if not rows:
            return None

        header = "fiscal_year,fiscal_year_end,Revenue,NetIncome,OperatingIncome,TotalAssets,TotalLiabilities,StockholdersEquity,CashAndEquivalents,OperatingCashFlow,EPSDiluted\n"
        lines = [header]
        for r in rows:
            line_vals = [str(r[0]), str(r[1] or "")] + [
                "" if v is None else f"{float(v):.15g}" for v in r[2:]
            ]
            lines.append(",".join(line_vals) + "\n")

        table = "".join(lines)
        label, scope = (
            (f"F-{ticker}-{fiscal_year}", f"FY{fiscal_year}")
            if fiscal_year
            else (f"F-{ticker}", "all years")
        )
        return f"[{label}] ({ticker} {scope} reported financials; amounts in USD, EPSDiluted in USD per share)\n{table}"
    except Exception:
        return None


def financials_block(ticker: str, fiscal_year: Optional[int] = None, data_dir: Path = DATA_DIR) -> str:
    """Format one company's XBRL figures with `[F-<ticker>-<year>]` citation label (Supabase first, CSV fallback)."""
    supabase_block = _lookup_financials_supabase(ticker, fiscal_year)
    if supabase_block:
        return supabase_block

    df = _get_financials_df(data_dir)
    if df.empty:
        return f"[F-{ticker}] No financials.csv found."
    rows = df[df["ticker"] == ticker]
    if fiscal_year:
        rows = rows[rows["fiscal_year"] == int(fiscal_year)]
    rows = rows.dropna(subset=METRICS, how="all").sort_values("fiscal_year")
    label, scope = (
        (f"F-{ticker}-{fiscal_year}", f"FY{fiscal_year}")
        if fiscal_year
        else (f"F-{ticker}", "all years")
    )
    if rows.empty:
        return f"[{label}] ({ticker} {scope} reported financials) No figures available."
    table = rows.set_index("fiscal_year")[["fiscal_year_end"] + METRICS].to_csv(float_format="%.15g")
    return f"[{label}] ({ticker} {scope} reported financials; amounts in USD, EPSDiluted in USD per share)\n{table}"


def lookup_financials(
    ticker: Optional[str] = None,
    fiscal_year: Optional[int] = None,
    pairs: Optional[List[List[Any]]] = None,
    data_dir: Path = DATA_DIR,
) -> List[str]:
    """Return formatted `[F-<ticker>-<year>]` blocks for the requested `(ticker, fiscal_year)` pairs."""
    resolved_pairs = pairs or ([[ticker, fiscal_year]] if ticker else [])
    return [financials_block(str(t), int(y) if y else None, data_dir=data_dir) for t, y in resolved_pairs if t]


def tabular_tool_node(state: AdaptiveRAGState) -> Dict[str, Any]:
    """
    LangGraph Node (System C v2 AAMR):
    Executes deterministic tabular lookup over `data/financials.csv` when `needs_tabular_tool` is True
    and appends both `tabular_evidence` and a structured `EvidenceChunk` (`[F-<ticker>-<year>]`)
    so Aryan's Citation Mapper and Guardrail can cite and verify exact XBRL numbers.
    """
    telemetry = dict(state.get("telemetry", {}))
    with track_node_latency(telemetry, "tabular_tool"):
        ticker = state.get("target_ticker")
        years = state.get("fiscal_years") or []
        pairs = state.get("target_pairs") or (
            [[ticker, y] for y in years] if (ticker and years) else ([[ticker, None]] if ticker else [])
        )
        blocks = lookup_financials(pairs=pairs)
        existing_evidence = list(state.get("accumulated_evidence", []))
        existing_ids = {ch["chunk_id"] for ch in existing_evidence}

        for idx, block in enumerate(blocks):
            t_val = pairs[idx][0] if idx < len(pairs) else (ticker or "UNKNOWN")
            y_val = pairs[idx][1] if idx < len(pairs) else (years[0] if years else None)
            chunk_id = f"F-{t_val}-{y_val}" if y_val else f"F-{t_val}"
            if chunk_id not in existing_ids:
                existing_evidence.append(
                    EvidenceChunk(
                        chunk_id=chunk_id,
                        content=block,
                        metadata={
                            "doc_id": chunk_id,
                            "ticker": t_val,
                            "fiscal_year": y_val or "ALL",
                            "section": "SEC XBRL Reported Financials (financials.csv)",
                            "chunk": 0,
                            "source_type": "tabular_xbrl",
                        },
                        relevance_score=1.0,
                        hop_retrieved=state.get("current_hop", 1),
                    )
                )
                existing_ids.add(chunk_id)

    return {
        "tabular_evidence": blocks,
        "accumulated_evidence": existing_evidence,
        "telemetry": telemetry,
    }
