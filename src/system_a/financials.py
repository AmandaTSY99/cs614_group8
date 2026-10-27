"""financials.csv lookup for RAG 4: reported annual figures (SEC XBRL, FY2009 onwards) as extra context blocks.

It runs in code for the chosen companies and years. The LLM never decides whether to look anything up,
so RAG 4 is still vanilla (non-agentic) RAG with one LLM call.
"""
from functools import lru_cache
import os
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
METRICS = ["Revenue", "NetIncome", "OperatingIncome", "TotalAssets", "TotalLiabilities",
           "StockholdersEquity", "CashAndEquivalents", "OperatingCashFlow", "EPSDiluted"]
FINANCIALS_NOTE = (" Blocks labelled [F-...] hold reported annual figures from SEC XBRL data; "
                   "cite them by their label, like [F-NVDA-2026], when you use a figure from them.")


def _financials_block_supabase(ticker, fiscal_year=None):
    """Query Supabase `sec_financials` table when SUPABASE_DB_URL is configured."""
    db_url = os.getenv("SUPABASE_DB_URL")
    if not db_url or os.getenv("LLM_PROVIDER", "").strip().lower() == "mock":
        return None
    import psycopg
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
    with psycopg.connect(db_url, sslmode="require", autocommit=True) as conn:
        rows = conn.execute(query, params).fetchall()
    label, scope = (f"F-{ticker}-{fiscal_year}", f"FY{fiscal_year}") if fiscal_year else (f"F-{ticker}", "all years")
    if not rows:
        return f"[{label}] ({ticker} {scope} reported financials) No figures available."
    header = "fiscal_year,fiscal_year_end," + ",".join(METRICS) + "\n"
    lines = [header]
    for r in rows:
        vals = [str(r[0]), str(r[1] or "")] + ["" if v is None else f"{float(v):.15g}" for v in r[2:]]
        lines.append(",".join(vals) + "\n")
    return f"[{label}] ({ticker} {scope} reported financials; amounts in USD, EPSDiluted in USD per share)\n{''.join(lines)}"


@lru_cache(maxsize=1)
def load_financials():
    """financials.csv only has the period-end date, so the fiscal year comes from the filing's folder name
    (FY{year}_{period-end}), matched on accession number."""
    df = pd.read_csv(DATA_DIR / "financials.csv", dtype={"accession": str}).merge(
        pd.read_csv(DATA_DIR / "filings_index.csv", dtype=str)[["accession", "local_folder"]], on="accession")
    df["fiscal_year"] = df["local_folder"].map(lambda folder: int(Path(folder).name[2:6]))
    return df


def financials_block(ticker, fiscal_year=None):
    """One company's figures as a context block: one year, or every year if `fiscal_year` is None."""
    sb = _financials_block_supabase(ticker, fiscal_year)
    if sb is not None:
        return sb
    df = load_financials()
    rows = df[df["ticker"] == ticker]
    if fiscal_year:
        rows = rows[rows["fiscal_year"] == fiscal_year]
    rows = rows.dropna(subset=METRICS, how="all").sort_values("fiscal_year")   # pre-2009 rows have no XBRL figures
    label, scope = (f"F-{ticker}-{fiscal_year}", f"FY{fiscal_year}") if fiscal_year else (f"F-{ticker}", "all years")
    if rows.empty:
        return f"[{label}] ({ticker} {scope} reported financials) No figures available."
    table = rows.set_index("fiscal_year")[["fiscal_year_end"] + METRICS].to_csv(float_format="%.15g")
    return f"[{label}] ({ticker} {scope} reported financials; amounts in USD, EPSDiluted in USD per share)\n{table}"


def lookup_financials(pairs):
    """Blocks for the same (ticker, fiscal_year) pairs retrieval is filtered on. Nothing without a company."""
    return [financials_block(ticker, year) for ticker, year in pairs or [] if ticker]
