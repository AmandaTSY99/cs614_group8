"""Pull every 10-K filing and XBRL financial data from SEC EDGAR for a set of companies,
and save human-readable copies alongside the originals.

Usage:
    export SEC_USER_AGENT="Your Name your.email@example.com"
    python fetch_10k.py                          # default 10 companies, every 10-K on EDGAR
    python fetch_10k.py --years 5 --tickers AAPL MSFT

Output layout (under data/):
    README.md                       overview: companies, years covered, layout
    filings_index.csv               one row per 10-K, all companies
    financials.csv                  key annual metrics, all companies
    {TICKER}/
        README.md                   company profile, financials table, list of filings
        company_info.json           name, CIK, industry, addresses, fiscal year end
        financials.csv              key annual metrics for this company
        raw/submissions.json        EDGAR filing history (pretty-printed)
        raw/companyfacts.json       all XBRL facts (pretty-printed)
        10-K/FY{year}_{period-end}/
            10-K.md                 readable Markdown version (or 10-K.txt for 1990s plain-text filings)
            original.htm|.txt       document exactly as filed
            metadata.json           accession, dates, form type, SEC URLs
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

import requests

DEFAULT_TICKERS = ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "NVDA", "TSLA", "JPM", "JNJ", "WMT"]

# Earlier registrants whose 10-Ks belong to the same business (e.g. Google Inc. before Alphabet).
PREDECESSOR_CIKS = {"GOOGL": ["0001288776"]}

FORMS = ("10-K", "10-K405")  # 10-K405 was used until 2002; amendments (10-K/A) are excluded

# Ordered fallbacks: companies tag the same concept differently.
METRICS = {
    "Revenue": ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"],
    "NetIncome": ["NetIncomeLoss"],
    "OperatingIncome": ["OperatingIncomeLoss"],
    "TotalAssets": ["Assets"],
    "TotalLiabilities": ["Liabilities"],
    "StockholdersEquity": ["StockholdersEquity"],
    "CashAndEquivalents": ["CashAndCashEquivalentsAtCarryingValue"],
    "OperatingCashFlow": ["NetCashProvidedByUsedInOperatingActivities",
                          "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"],
    "EPSDiluted": ["EarningsPerShareDiluted"],
}

DATA_DIR = Path("data")
MIN_INTERVAL = 0.12  # SEC allows max 10 requests/second
_last_request = 0.0


def get(session, url):
    global _last_request
    attempts = 5
    for attempt in range(attempts):
        wait = MIN_INTERVAL - (time.monotonic() - _last_request)
        if wait > 0:
            time.sleep(wait)
        _last_request = time.monotonic()
        try:
            resp = session.get(url, timeout=60)
        except (requests.ConnectionError, requests.Timeout):
            if attempt == attempts - 1:
                raise
        else:
            if resp.status_code not in (429, 500, 502, 503) or attempt == attempts - 1:
                resp.raise_for_status()
                return resp
        time.sleep(2 ** attempt)


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False))


def ticker_to_cik(session):
    data = get(session, "https://www.sec.gov/files/company_tickers.json").json()
    return {row["ticker"]: str(row["cik_str"]).zfill(10) for row in data.values()}


def list_10ks(session, submissions):
    """All 10-Ks for a registrant, newest first. Heavy filers spill older filings into extra pages."""
    pages = [submissions["filings"]["recent"]]
    pages += [get(session, f"https://data.sec.gov/submissions/{p['name']}").json()
              for p in submissions["filings"].get("files", [])]
    rows = []
    for page in pages:
        for i, form in enumerate(page["form"]):
            if form in FORMS:
                rows.append({
                    "form": form,
                    "accession": page["accessionNumber"][i],
                    "filing_date": page["filingDate"][i],
                    "report_date": page["reportDate"][i],
                    "primary_doc": page["primaryDocument"][i],
                })
    return sorted(rows, key=lambda r: r["filing_date"], reverse=True)


def fiscal_year(report_date):
    """52/53-week years that end in the first days of January belong to the previous fiscal year."""
    year, month, day = (int(x) for x in report_date.split("-"))
    return year - 1 if month == 1 and day <= 7 else year


def days_between(start, end):
    return (time.mktime(time.strptime(end, "%Y-%m-%d")) - time.mktime(time.strptime(start, "%Y-%m-%d"))) / 86400


def latest_period_values(facts, acc, report_date):
    """Values tagged in this 10-K whose period ends on the fiscal year end date."""
    row = {}
    gaap = facts.get("facts", {}).get("us-gaap", {})
    for metric, tags in METRICS.items():
        for tag in tags:
            for unit_vals in gaap.get(tag, {}).get("units", {}).values():
                for v in unit_vals:
                    if v.get("accn") == acc and v.get("end") == report_date:
                        # For flow metrics, use the full-year duration, not a quarter
                        if "start" in v and days_between(v["start"], v["end"]) < 300:
                            continue
                        row[metric] = v["val"]
                        break
                if metric in row:
                    break
            if metric in row:
                break
    return row


# ---------------------------------------------------------------------------
# HTML -> Markdown
# ---------------------------------------------------------------------------

BLOCK_TAGS = {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "center", "pre", "ul", "ol"}
SKIP_TAGS = {"script", "style", "head", "title", "ix:header"}
VOID_TAGS = {"br", "hr", "img", "meta", "link", "input", "col", "area", "base", "wbr"}
ITEM_RE = re.compile(r"^(PART\s+[IV]+\b|Item\s+\d+[A-C]?\.)", re.IGNORECASE)


class _Converter(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []          # finished Markdown blocks
        self.para = []         # text pieces of the current paragraph: (text, bold)
        self.stack = []        # (tag, hidden, bold) for open elements
        self.table = None      # list of rows while inside a table
        self.row = None
        self.cell = None
        self.cell_span = 1
        self.table_depth = 0

    # state helpers
    def _hidden(self):
        return any(h for _, h, _ in self.stack)

    def _bold(self):
        return any(b for _, _, b in self.stack)

    def _flush_para(self):
        text = "".join(t for t, _ in self.para)
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            bold_chars = sum(len(t.strip()) for t, b in self.para if b)
            all_bold = bold_chars >= 0.9 * len(text.replace(" ", ""))
            if ITEM_RE.match(text) and len(text) < 200:
                text = f"## {text}" if text.upper().startswith("PART") else f"### {text}"
            elif all_bold and len(text) < 150 and not re.fullmatch(r"[\d\W]+", text):
                text = f"**{text}**"
            self.out.append(text)
        self.para = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        style = (attrs.get("style") or "").replace(" ", "").lower()
        hidden = tag in SKIP_TAGS or "display:none" in style
        bold = tag in ("b", "strong", "h1", "h2", "h3", "h4") or "font-weight:bold" in style \
            or "font-weight:700" in style
        if tag not in VOID_TAGS:
            self.stack.append((tag, hidden, bold))
        if self._hidden():
            return

        if tag == "table":
            self.table_depth += 1
            if self.table_depth == 1:
                self._flush_para()
                self.table = []
        elif tag == "tr" and self.table_depth == 1:
            self.row = []
        elif tag in ("td", "th") and self.table_depth == 1:
            self.cell = []
            try:
                self.cell_span = max(1, int(attrs.get("colspan") or 1))
            except ValueError:
                self.cell_span = 1
        elif tag in BLOCK_TAGS:
            if self.cell is not None:
                self.cell.append(" ")
            elif self.table is None:
                self._flush_para()

    def handle_endtag(self, tag):
        # pop up to and including the matching tag (tolerates sloppy HTML)
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                hidden_before = self._hidden()
                del self.stack[i:]
                if hidden_before and self._hidden():
                    return
                break
        else:
            return
        if self._hidden():
            return

        if tag in ("td", "th") and self.table_depth == 1 and self.cell is not None:
            if self.row is not None:
                self.row.append("".join(self.cell))
                self.row.extend([""] * (self.cell_span - 1))
            self.cell = None
        elif tag == "tr" and self.table_depth == 1 and self.row is not None:
            self.table.append(self.row)
            self.row = None
        elif tag == "table" and self.table_depth:
            self.table_depth -= 1
            if self.table_depth == 0:
                rendered = render_table(self.table or [])
                if rendered:
                    self.out.append(rendered)
                self.table = None
        elif tag in BLOCK_TAGS and self.table is None:
            self._flush_para()

    def handle_data(self, data):
        if self._hidden():
            return
        if self.cell is not None:
            self.cell.append(data)
        elif self.table is None:
            self.para.append((data, self._bold()))

    def close(self):
        super().close()
        self._flush_para()


def _clean(text):
    return re.sub(r"\s+", " ", text.replace("​", "")).strip()


def render_table(rows):
    rows = [[_clean(c) for c in r] for r in rows]
    rows = [r for r in rows if any(r)]
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]

    # Glue "$" onto the number after it, and ")" / "%" onto the number before it
    for r in rows:
        for i, c in enumerate(r):
            if c in ("$", "€", "£") and i + 1 < width:
                nxt = next((j for j in range(i + 1, width) if r[j]), None)
                if nxt is not None:
                    r[nxt] = c + r[nxt]
                    r[i] = ""
            elif c in (")", "%", ")%", "%)") and i > 0:
                prv = next((j for j in range(i - 1, -1, -1) if r[j]), None)
                if prv is not None:
                    r[prv] += c
                    r[i] = ""

    keep = [i for i in range(width) if any(r[i] for r in rows)]
    rows = [[r[i] for i in keep] for r in rows]
    if not keep:
        return ""

    # Filings split one logical column into several ("$" | number | ")"), with colspan placing
    # values inconsistently. Merge neighbouring value columns that never collide in any row.
    j = 1
    while j + 1 < len(rows[0]):
        if all(not r[j] or not r[j + 1] for r in rows):
            for r in rows:
                r[j] = r[j] or r[j + 1]
                del r[j + 1]
        else:
            j += 1
    keep = rows[0]

    # Layout tables (one column, or a single row) read better as plain paragraphs
    if len(keep) == 1 or len(rows) == 1:
        return "\n\n".join(" ".join(c for c in r if c) for r in rows)

    esc = lambda c: c.replace("|", "\\|")
    lines = ["| " + " | ".join(esc(c) for c in rows[0]) + " |",
             "|" + "---|" * len(keep)]
    lines += ["| " + " | ".join(esc(c) for c in r) + " |" for r in rows[1:]]
    return "\n".join(lines)


def html_to_markdown(html):
    conv = _Converter()
    conv.feed(html)
    conv.close()
    md = "\n\n".join(conv.out)
    md = re.sub(r"\n{3,}", "\n\n", md)
    # Drop bare page numbers / page-break remnants left on their own line
    md = re.sub(r"(?m)^(\d{1,3}|Table of Contents|[ivx]{1,4})\n\n", "", md)
    return md.strip() + "\n"


def extract_sgml_document(text):
    """From a full EDGAR submission (.txt), return the body of the main 10-K document."""
    m = re.search(r"<DOCUMENT>.*?<TEXT>(.*?)</TEXT>", text, re.DOTALL | re.IGNORECASE)
    body = m.group(1) if m else text
    return re.sub(r"(?im)^\s*</?PAGE>\s*$", "", body)


def readable_version(raw_bytes, doc_name):
    """Return (filename, text) for the human-readable copy of a filing."""
    text = raw_bytes.decode("utf-8", errors="replace") if b"\x00" not in raw_bytes[:1000] else ""
    if doc_name.lower().endswith(".txt"):
        text = extract_sgml_document(text)
        # Old filings are preformatted text with SGML table markup (<TABLE>, <S>, <C>, <FN>), not HTML
        if not re.search(r"<(html|body|p|div|br|font)\b", text, re.IGNORECASE):
            text = re.sub(r"(?i)</?(TABLE|CAPTION|S|C|FN)>", "", text)
            return "10-K.txt", unescape(text).strip() + "\n"
    return "10-K.md", html_to_markdown(text)


def download_original(session, f, base, doc_name, filing_dir):
    """Save the filed document, falling back to the full submission .txt when EDGAR no longer
    serves the listed primary document. Updates f["url"] / f["original"] in place."""
    fallback = f"{f['accession']}.txt"
    use_fallback = (filing_dir / "original.txt").exists() and f["original"] != "original.txt"
    path = filing_dir / f["original"]
    if not use_fallback and not path.exists():
        try:
            path.write_bytes(get(session, f["url"]).content)
        except requests.HTTPError as e:
            if e.response.status_code != 404:
                raise
            use_fallback = True
            (filing_dir / "original.txt").write_bytes(get(session, f"{base}/{fallback}").content)
    if use_fallback:
        doc_name, f["original"], f["url"] = fallback, "original.txt", f"{base}/{fallback}"
        path = filing_dir / "original.txt"
    return doc_name, path


# ---------------------------------------------------------------------------
# Per-company README
# ---------------------------------------------------------------------------

def fmt_money(v, metric):
    if v in ("", None):
        return "–"
    if metric == "EPSDiluted":
        return f"{v:.2f}"
    return f"{v / 1e6:,.0f}"


def company_readme(ticker, info, fin_rows, filings):
    lines = [f"# {info['name']} ({ticker})", "",
             f"- **CIK:** {info['cik']}",
             f"- **Industry:** {info.get('sicDescription') or '–'} (SIC {info.get('sic') or '–'})",
             f"- **Exchange(s):** {', '.join(x for x in info.get('exchanges', []) if x) or '–'}",
             f"- **Fiscal year end:** {info.get('fiscalYearEnd') or '–'} (MMDD)",
             f"- **State of incorporation:** {info.get('stateOfIncorporation') or '–'}",
             f"- **10-K filings saved:** {len(filings)} "
             f"(fiscal years {fiscal_year(filings[-1]['report_date'])}–{fiscal_year(filings[0]['report_date'])})", ""]

    with_data = [r for r in fin_rows if any(r.get(m) not in ("", None) for m in METRICS)]
    if with_data:
        lines += ["## Key financials", "",
                  "USD millions, except diluted EPS. As reported in each year's 10-K (not restated). "
                  "– = not tagged by the company.", ""]
        cols = sorted(with_data, key=lambda r: r["fiscal_year_end"])
        lines.append("| Metric | " + " | ".join(f"FY{fiscal_year(r['fiscal_year_end'])}" for r in cols) + " |")
        lines.append("|---|" + "---:|" * len(cols))
        for m in METRICS:
            lines.append(f"| {m} | " + " | ".join(fmt_money(r.get(m), m) for r in cols) + " |")
        lines.append("")

    lines += ["## Filings", "",
              "| Fiscal year | Period end | Filed | Form | Readable | Original | SEC |",
              "|---|---|---|---|---|---|---|"]
    for f in filings:
        folder = f"10-K/{f['folder']}"
        lines.append(f"| FY{fiscal_year(f['report_date'])} | {f['report_date']} | {f['filing_date']} | {f['form']} "
                     f"| [{f['readable']}]({folder}/{f['readable']}) | [{f['original']}]({folder}/{f['original']}) "
                     f"| [link]({f['url']}) |")
    return "\n".join(lines) + "\n"


def top_readme(summary):
    lines = ["# 10-K dataset", "",
             "10-K annual reports and XBRL financial data from SEC EDGAR, generated by `fetch_10k.py`.", "",
             "| Ticker | Company | 10-Ks | Fiscal years | Years with XBRL financials |",
             "|---|---|---:|---|---:|"]
    for s in summary:
        lines.append(f"| [{s['ticker']}]({s['ticker']}/README.md) | {s['name']} | {s['count']} "
                     f"| {s['first']}–{s['last']} | {s['xbrl']} |")
    lines += ["", "## Layout", "", "```",
              "filings_index.csv          every 10-K, all companies",
              "financials.csv             key annual metrics, all companies",
              "{TICKER}/README.md         company profile, financials table, filing list",
              "{TICKER}/company_info.json",
              "{TICKER}/financials.csv",
              "{TICKER}/raw/              submissions.json, companyfacts.json (pretty-printed)",
              "{TICKER}/10-K/FY{year}_{period-end}/",
              "    10-K.md                readable version (10-K.txt for 1990s plain-text filings)",
              "    original.htm|.txt      as filed with the SEC",
              "    metadata.json",
              "```", "",
              "Notes:",
              "- Machine-readable (XBRL) financials only exist from ~2009 onward; older years have documents only.",
              "- Values are as originally reported in each 10-K, so per-share figures are not split-adjusted.",
              "- Amended filings (10-K/A) are not included.",
              ""]
    return "\n".join(lines)


# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tickers", nargs="+", default=DEFAULT_TICKERS)
    parser.add_argument("--years", type=int, default=None, help="only the N most recent 10-Ks (default: all)")
    parser.add_argument("--no-docs", action="store_true", help="skip downloading 10-K documents")
    args = parser.parse_args()

    user_agent = os.environ.get("SEC_USER_AGENT")
    if not user_agent:
        sys.exit('Set SEC_USER_AGENT, e.g. export SEC_USER_AGENT="Jane Doe jane@example.com" (SEC requires it)')

    session = requests.Session()
    session.headers.update({"User-Agent": user_agent, "Accept-Encoding": "gzip, deflate"})

    ciks = ticker_to_cik(session)
    index_rows, all_fin_rows, summary = [], [], []

    for ticker in [t.upper() for t in args.tickers]:
        cik = ciks.get(ticker)
        if not cik:
            print(f"[skip] {ticker}: ticker not found")
            continue
        company_dir = DATA_DIR / ticker
        (company_dir / "raw").mkdir(parents=True, exist_ok=True)

        filings, seen_periods, facts_by_cik, info = [], set(), {}, None
        for reg_cik in [cik, *PREDECESSOR_CIKS.get(ticker, [])]:
            submissions = get(session, f"https://data.sec.gov/submissions/CIK{reg_cik}.json").json()
            try:
                facts = get(session, f"https://data.sec.gov/api/xbrl/companyfacts/CIK{reg_cik}.json").json()
            except requests.HTTPError:
                facts = {}
            suffix = "" if reg_cik == cik else f"_CIK{reg_cik}"
            write_json(company_dir / "raw" / f"submissions{suffix}.json", submissions)
            write_json(company_dir / "raw" / f"companyfacts{suffix}.json", facts)
            facts_by_cik[reg_cik] = facts
            if info is None:
                info = {k: v for k, v in submissions.items() if k != "filings"}
            for f in list_10ks(session, submissions):
                # Skip a predecessor's 10-K when the current registrant already covers that period
                if f["report_date"] in seen_periods:
                    continue
                seen_periods.add(f["report_date"])
                filings.append({**f, "cik": reg_cik, "filer": submissions["name"]})

        filings.sort(key=lambda r: r["report_date"], reverse=True)
        if args.years:
            filings = filings[:args.years]
        write_json(company_dir / "company_info.json", info)
        print(f"{ticker}: {info['name']} (CIK {cik}), {len(filings)} 10-Ks")

        fin_rows = []
        for f in filings:
            acc_nodash = f["accession"].replace("-", "")
            base = f"https://www.sec.gov/Archives/edgar/data/{int(f['cik'])}/{acc_nodash}"
            doc_name = f["primary_doc"] or f"{f['accession']}.txt"  # 1990s filings: full submission text
            f["url"] = f"{base}/{doc_name}"
            f["folder"] = f"FY{fiscal_year(f['report_date'])}_{f['report_date']}"
            f["original"] = "original" + (".txt" if doc_name.lower().endswith(".txt") else ".htm")
            filing_dir = company_dir / "10-K" / f["folder"]
            filing_dir.mkdir(parents=True, exist_ok=True)

            original_path = filing_dir / f["original"]
            if not args.no_docs:
                doc_name, original_path = download_original(session, f, base, doc_name, filing_dir)
                readable_name, readable = readable_version(original_path.read_bytes(), doc_name)
                (filing_dir / readable_name).write_text(readable)
                f["readable"] = readable_name
            else:
                f["readable"] = "10-K.md"

            write_json(filing_dir / "metadata.json", {
                "ticker": ticker, "filer": f["filer"], "cik": f["cik"], "form": f["form"],
                "accession": f["accession"], "fiscal_year_end": f["report_date"],
                "filing_date": f["filing_date"], "document_url": f["url"], "filing_index_url": f"{base}/",
            })

            index_rows.append({"ticker": ticker, "filer": f["filer"], "cik": f["cik"], "form": f["form"],
                               "accession": f["accession"], "fiscal_year_end": f["report_date"],
                               "filing_date": f["filing_date"], "url": f["url"],
                               "local_folder": str(filing_dir)})
            fin_rows.append({"ticker": ticker, "fiscal_year_end": f["report_date"], "accession": f["accession"],
                             **latest_period_values(facts_by_cik[f["cik"]], f["accession"], f["report_date"])})

        fieldnames = ["ticker", "fiscal_year_end", "accession", *METRICS]
        with open(company_dir / "financials.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(fin_rows)
        all_fin_rows += fin_rows
        (company_dir / "README.md").write_text(company_readme(ticker, info, fin_rows, filings))
        summary.append({"ticker": ticker, "name": info["name"], "count": len(filings),
                        "first": fiscal_year(filings[-1]["report_date"]), "last": fiscal_year(filings[0]["report_date"]),
                        "xbrl": sum(1 for r in fin_rows if len(r) > 3)})

    DATA_DIR.mkdir(exist_ok=True)
    with open(DATA_DIR / "filings_index.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(index_rows[0].keys()))
        w.writeheader()
        w.writerows(index_rows)
    with open(DATA_DIR / "financials.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["ticker", "fiscal_year_end", "accession", *METRICS])
        w.writeheader()
        w.writerows(all_fin_rows)
    (DATA_DIR / "README.md").write_text(top_readme(summary))
    print(f"Wrote {len(index_rows)} filings to {DATA_DIR}/")


if __name__ == "__main__":
    main()
