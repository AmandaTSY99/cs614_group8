#!/usr/bin/env python3
"""
Supabase Enterprise Sync Tool for System C.

Owned by: Anish (System Architect & Orchestration Lead)

Syncs:
1. Structured XBRL financial line items from `data/financials.csv` into `sec_financials` table.
2. Structure-chunked 10-K sections into `sec_chunks` table for SQL-partitioned retrieval.
"""

import os
from pathlib import Path
from typing import Optional

import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from dotenv import load_dotenv

load_dotenv()

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"

SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL", "")


def get_db_connection():
    if not SUPABASE_DB_URL:
        raise ValueError("SUPABASE_DB_URL is not set in environment or .env file.")
    return psycopg2.connect(SUPABASE_DB_URL, sslmode="require")


def sync_financials():
    """Sync `data/financials.csv` into Supabase `sec_financials` table."""
    fin_path = DATA_DIR / "financials.csv"
    idx_path = DATA_DIR / "filings_index.csv"

    if not fin_path.exists() or not idx_path.exists():
        print("financials.csv or filings_index.csv not found.")
        return

    fin_df = pd.read_csv(fin_path, dtype={"accession": str})
    idx_df = pd.read_csv(idx_path, dtype=str)[["accession", "local_folder"]]

    merged = fin_df.merge(idx_df, on="accession")
    merged["fiscal_year"] = merged["local_folder"].map(lambda f: int(Path(f).name[2:6]))

    rows_to_insert = []
    for _, r in merged.iterrows():
        def val(col):
            v = r.get(col)
            return None if pd.isna(v) else float(v)

        rows_to_insert.append((
            str(r["ticker"]),
            int(r["fiscal_year"]),
            str(r.get("fiscal_year_end") or ""),
            val("Revenue"),
            val("NetIncome"),
            val("OperatingIncome"),
            val("TotalAssets"),
            val("TotalLiabilities"),
            val("StockholdersEquity"),
            val("CashAndEquivalents"),
            val("OperatingCashFlow"),
            val("EPSDiluted"),
        ))

    insert_sql = """
    INSERT INTO sec_financials (
        ticker, fiscal_year, fiscal_year_end,
        revenue, net_income, operating_income,
        total_assets, total_liabilities, stockholders_equity,
        cash_and_equivalents, operating_cash_flow, eps_diluted
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (ticker, fiscal_year) DO UPDATE SET
        fiscal_year_end = EXCLUDED.fiscal_year_end,
        revenue = EXCLUDED.revenue,
        net_income = EXCLUDED.net_income,
        operating_income = EXCLUDED.operating_income,
        total_assets = EXCLUDED.total_assets,
        total_liabilities = EXCLUDED.total_liabilities,
        stockholders_equity = EXCLUDED.stockholders_equity,
        cash_and_equivalents = EXCLUDED.cash_and_equivalents,
        operating_cash_flow = EXCLUDED.operating_cash_flow,
        eps_diluted = EXCLUDED.eps_diluted;
    """

    print(f"Connecting to Supabase to sync {len(rows_to_insert)} financial records...")
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            execute_batch(cur, insert_sql, rows_to_insert, page_size=100)
        conn.commit()

        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM sec_financials;")
            count = cur.fetchone()[0]
            print(f"SUCCESS: Supabase `sec_financials` table now contains {count} rows!")


def main():
    print("=" * 60)
    print("SYSTEM C -> SUPABASE CLUSTER SYNC")
    print("=" * 60)
    sync_financials()


if __name__ == "__main__":
    main()
