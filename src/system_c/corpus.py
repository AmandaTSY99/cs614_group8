"""
SEC 10-K Corpus Loader, Contextual Structure Chunker, and Tabular Financials Lookup.

Standardized against baseline RAG corpus specifications (`build_vdb_base_RAG.ipynb` RAG 1–5).
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

DATA_DIR = Path("data")

ITEM_RE = re.compile(r"^item\s+(\d+[a-c]?)\b[.:]?\s*(.*)$", re.IGNORECASE)
TABLE_SEP_RE = re.compile(r"^\|(\s*:?-{3,}:?\s*\|)+$")

METRICS = [
    "Revenue",
    "NetIncome",
    "OperatingIncome",
    "TotalAssets",
    "TotalLiabilities",
    "StockholdersEquity",
    "CashAndEquivalents",
    "OperatingCashFlow",
    "EPSDiluted",
]

COMPANY_TICKERS: Dict[str, str] = {
    "apple": "AAPL",
    "microsoft": "MSFT",
    "amazon": "AMZN",
    "alphabet": "GOOGL",
    "google": "GOOGL",
    "meta": "META",
    "facebook": "META",
    "nvidia": "NVDA",
    "tesla": "TSLA",
    "jpmorgan": "JPM",
    "jp morgan": "JPM",
    "johnson & johnson": "JNJ",
    "johnson and johnson": "JNJ",
    "j&j": "JNJ",
    "walmart": "WMT",
}

KNOWN_TICKERS = ["AAPL", "AMZN", "GOOGL", "JNJ", "JPM", "META", "MSFT", "NVDA", "TSLA", "WMT"]


def to_ticker(name: str) -> Optional[str]:
    """Resolve company name or ticker string to canonical ticker (matches `build_vdb_base_RAG.ipynb`)."""
    if not name:
        return None
    clean = name.strip()
    if clean.upper() in KNOWN_TICKERS:
        return clean.upper()
    return COMPANY_TICKERS.get(clean.lower())


def extract_all_tickers_and_years_from_query(query: str) -> Tuple[List[str], List[int]]:
    """Extract all mentioned company tickers (for comparative multi-company queries) and fiscal years."""
    q_lower = query.lower()
    detected = []
    for t in KNOWN_TICKERS:
        if re.search(rf"\b{t.lower()}\b", q_lower):
            detected.append(t)
    for name, t in COMPANY_TICKERS.items():
        if name in q_lower and t not in detected:
            detected.append(t)

    years = sorted({int(m) for m in re.findall(r"\b(199\d|20[0-2]\d)\b", query)})
    return detected, years


def extract_tickers_and_years_from_query(query: str) -> Tuple[Optional[str], List[int]]:
    """Fast regex/lexicon extractor for primary ticker and fiscal years mentioned in a query."""
    tickers, years = extract_all_tickers_and_years_from_query(query)
    primary = tickers[0] if tickers else None
    return primary, years


def load_filings(
    data_dir: Path = DATA_DIR,
    tickers: Optional[List[str]] = None,
    min_year: Optional[int] = None,
    fiscal_years: Optional[List[int]] = None,
) -> List[Dict[str, Any]]:
    """Load 10-K filings and metadata from `data/filings_index.csv` (matches `build_vdb_base_RAG.ipynb`)."""
    index_path = data_dir / "filings_index.csv"
    if not index_path.exists():
        return []
    index = pd.read_csv(index_path, dtype=str)
    filings = []
    for row in index.itertuples():
        folder = data_dir.parent / Path(row.local_folder) if not Path(row.local_folder).exists() else Path(row.local_folder)
        fiscal_year = int(folder.name[2:6])
        if tickers and row.ticker not in tickers:
            continue
        if min_year and fiscal_year < min_year:
            continue
        if fiscal_years and fiscal_year not in fiscal_years:
            continue
        path = next(
            (folder / name for name in ("10-K.md", "10-K.txt") if (folder / name).exists()),
            None,
        )
        if path is None:
            continue
        filings.append(
            {
                "text": path.read_text(encoding="utf-8"),
                "meta": {
                    "doc_id": f"{row.ticker}_{folder.name}",
                    "ticker": row.ticker,
                    "filer": row.filer,
                    "fiscal_year": fiscal_year,
                    "fiscal_year_end": row.fiscal_year_end,
                    "filing_date": row.filing_date,
                    "format": path.suffix.lstrip("."),
                    "url": row.url,
                },
            }
        )
    return filings


def _n_words(lines: List[str]) -> int:
    return sum(len(line.split()) for line in lines)


def _is_heading(line: str, fmt: str) -> bool:
    if fmt == "md":
        return line.startswith("#") or (
            line.startswith("**") and line.endswith("**") and len(line) < 150
        )
    words = line.split()
    return (
        len(words) <= 8
        and bool(line)
        and line[0].isupper()
        and not line.endswith((".", ":", ";", ","))
        and not re.fullmatch(r"[\d\W]+", line)
    )


def _split_table(rows: List[str], max_words: int) -> List[str]:
    """Split a Markdown table into pieces of whole rows, repeating the header rows in every piece."""
    sep = next((i for i, row in enumerate(rows) if TABLE_SEP_RE.match(row)), None)
    head_end = 0
    if sep is not None:
        head_end = sep + 1
        while head_end < len(rows) and len(rows[head_end].split("|")) > 1 and rows[head_end].split("|")[1].strip() == "":
            head_end += 1
    header, body = rows[:head_end], rows[head_end:]

    pieces, current = [], []
    for row in body:
        if current and _n_words(header + current + [row]) > max_words:
            pieces.append(header + current)
            current = []
        current.append(row)
    pieces.append(header + current)
    return ["\n".join(piece) for piece in pieces]


def chunk_by_structure(text: str, fmt: str = "md", max_words: int = 200) -> List[Dict[str, str]]:
    """Split at 10-K Items, headings, and tables while preserving table headers (matches RAG 3 & RAG 5)."""
    chunks: List[Dict[str, str]] = []
    paragraph: List[str] = []
    table: List[str] = []
    item, item_no, heading = "", "", ""

    def label() -> str:
        return " > ".join(part for part in (item, heading) if part)

    def add(body: str, kind: str = "") -> None:
        chunks.append({"section": label(), "text": f"{label()}{kind}\n{body}".strip()})

    def flush_paragraph() -> None:
        if paragraph:
            add(" ".join(paragraph))
            paragraph.clear()

    def flush_table() -> None:
        if table:
            for piece in _split_table(table, max_words):
                add(piece, " (table)")
            table.clear()

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("|"):
            flush_paragraph()
            table.append(line)
            continue
        flush_table()
        if not line or line == "Table of Contents" or line.isdigit():
            continue

        plain = line.strip("#* ")
        item_match = ITEM_RE.match(plain)
        if item_match and len(plain.split()) <= 20:
            if item_match.group(1).upper() != item_no:
                flush_paragraph()
                item, item_no, heading = plain, item_match.group(1).upper(), ""
        elif _is_heading(line, fmt):
            flush_paragraph()
            heading = plain
        else:
            words = plain.split()
            for start in range(0, len(words), max_words):
                piece = words[start : start + max_words]
                if paragraph and _n_words(paragraph) + len(piece) > max_words:
                    flush_paragraph()
                paragraph.append(" ".join(piece))
    flush_paragraph()
    flush_table()
    return chunks


def doc_header(meta: Dict[str, Any]) -> str:
    """Contextual RAG 5 header naming company and fiscal year."""
    end = pd.Timestamp(meta["fiscal_year_end"])
    return (
        f"{meta['filer']} ({meta['ticker']}) 10-K, fiscal year {meta['fiscal_year']}, "
        f"year ended {end:%B} {end.day}, {end.year}"
    )


def chunk_corpus(filings: List[Dict[str, Any]], header: bool = True) -> List[Dict[str, Any]]:
    """Chunk filings using `chunk_by_structure` and optionally attach RAG 5 contextual `embed_text`."""
    records = []
    for f in filings:
        for i, c in enumerate(chunk_by_structure(f["text"], f["meta"]["format"])):
            record = {
                "id": f"{f['meta']['doc_id']}:{i}",
                "text": c["text"],
                "meta": {**f["meta"], "section": c["section"][:300], "chunk": i},
            }
            if header:
                record["embed_text"] = f"{doc_header(f['meta'])}\n{c['text']}"
            records.append(record)
    return records
