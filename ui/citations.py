"""
Render an answer so a reader can check every claim against the 10-K text it came from.

Works on one "run" dict, the same shape for live answers and benchmark records:
    answer, citations [{tag, chunk_id, ticker, fiscal_year, section}],
    contexts [{chunk_id, ticker, fiscal_year, section, text}], guardrail (System C only) or None.

System C's guardrail (Aryan's verifier) splits the answer into sentences, resolves each sentence's citation
tags to chunk ids and marks each number verified, derived or ungrounded. A and B have no guardrail, so their
`[n]` tags are mapped to chunks by position and numbers are left unmarked.
"""

import html
import re
from typing import Any, Dict, List, Optional, Tuple

# System C tags ("[NVDA FY2016, Item 7, NVDA_FY2016_2016-01-31:160]", "[F-TSLA-2021]") and A/B tags ("[3]", "【3】")
C_TAG_RE = re.compile(r"\[(?:[A-Z]{1,6} FY\d{4}[^\[\]]*|F-[A-Z]{1,6}(?:-\d{4})?)\]")
N_TAG_RE = re.compile(r"(?:\[(\d{1,2})\]|【(\d{1,2})】)")
WARNING_RE = re.compile(r">\s*\[Guardrail Audit Warning\]:.*", re.DOTALL)
NUM_IN_TEXT_RE = r"(?<![\w.]){}(?![\w])"


def _section_label(section: Any) -> str:
    s = str(section or "")
    parts = [p.strip() for p in s.split(">")]
    head = parts[0]
    m = re.match(r"(?i)item\s+(\d+[A-Z]?)", head)
    item = f"Item {m.group(1)}" if m else (head[:40] if head else "10-K")
    tail = parts[-1] if len(parts) > 1 else ""
    return f"{item} · {tail[:70]}" if tail else item


def _is_xbrl(chunk_id: str) -> bool:
    return str(chunk_id).startswith("F-")


class SourceIndex:
    """Numbers sources in the order the answer first cites them."""

    def __init__(self, contexts: List[Dict[str, Any]], prefix: str = "src"):
        self.prefix = prefix
        self.contexts = {str(c.get("chunk_id")): c for c in contexts}
        self.order: List[str] = []

    def number(self, chunk_id: str) -> int:
        if chunk_id not in self.order:
            self.order.append(chunk_id)
        return self.order.index(chunk_id) + 1


def _chip(n: int, chunk_id: str, prefix: str = "src") -> str:
    cls = "cite xbrl" if _is_xbrl(chunk_id) else "cite"
    return (f'<a class="{cls}" href="#{prefix}-{n}" title="Source {n}: {html.escape(chunk_id)}" '
            f'aria-label="Source {n}">{n}</a>')


def _mark_numbers(text_html: str, numbers: List[Dict[str, Any]]) -> str:
    for num in numbers:
        token = html.escape(str(num.get("value", "")))
        if not token:
            continue
        status = num.get("status")
        cls = "num-ok" if status in ("verified", "derived") else "num-bad"
        tip = {"verified": "Checked: found in the cited passage",
               "derived": "Checked: calculated from figures in the cited passages"}.get(
            status, "Not checked: not found in the cited passage")
        marked = f'<span class="{cls}" title="{tip}" aria-label="{token}, {tip}">{token}</span>'
        text_html = re.sub(NUM_IN_TEXT_RE.format(re.escape(token)), lambda _m: marked, text_html, count=1)
    return text_html


def _render_c_sentences(guard: Dict[str, Any], idx: SourceIndex) -> Tuple[str, Dict[str, int]]:
    out, stats = [], {"sentences": 0, "cited": 0, "numbers": 0, "numbers_ok": 0, "flagged_sentences": 0}
    for sent in guard.get("sentences") or []:
        if not isinstance(sent, dict):
            continue
        raw = WARNING_RE.sub("", sent.get("text") or "").strip()
        if not raw:
            continue
        stats["sentences"] += 1
        chunk_ids = [c for c in sent.get("chunk_ids") or [] if c]
        if chunk_ids:
            stats["cited"] += 1
        body = html.escape(C_TAG_RE.sub("", N_TAG_RE.sub("", raw)).strip())
        body = re.sub(r"\s+([.,;:])", r"\1", body)
        numbers = sent.get("numbers") or []
        stats["numbers"] += len(numbers)
        stats["numbers_ok"] += sum(1 for n in numbers if n.get("status") in ("verified", "derived"))
        body = _mark_numbers(body, numbers)
        flagged = any(n.get("status") not in ("verified", "derived") for n in numbers) or sent.get("semantic_verdict") == "unsupported"
        stats["flagged_sentences"] += int(flagged)
        chips = "".join(_chip(idx.number(c), c, idx.prefix) for c in dict.fromkeys(chunk_ids))
        cls = "sent flag" if flagged else "sent"
        out.append(f'<span class="{cls}">{body}</span>{chips} ')
    return "".join(out), stats


def _render_tagged_text(answer: str, run: Dict[str, Any], idx: SourceIndex) -> Tuple[str, Dict[str, int]]:
    """Fallback for answers without guardrail sentences: replace tags with chips paragraph by paragraph."""
    by_tag = {c.get("tag"): str(c.get("chunk_id")) for c in run.get("citations") or []}
    ctx_ids = [str(c.get("chunk_id")) for c in run.get("contexts") or []]
    paras, cited_paras = [], 0
    for para in [p for p in re.split(r"\n\s*\n", WARNING_RE.sub("", answer)) if p.strip()]:
        chips: List[str] = []

        def _c_tag(m):
            cid = by_tag.get(m.group(0)) or m.group(0).strip("[]").split(", ")[-1]
            chips.append(_chip(idx.number(cid), cid, idx.prefix))
            return "\x00"

        def _n_tag(m):
            n = int(m.group(1) or m.group(2))
            cid = by_tag.get(f"[{n}]") or (ctx_ids[n - 1] if 0 < n <= len(ctx_ids) else None)
            if cid:
                chips.append(_chip(idx.number(cid), cid, idx.prefix))
            return "\x00"

        tmp = N_TAG_RE.sub(_n_tag, C_TAG_RE.sub(_c_tag, para.strip()))
        cited_paras += int(bool(chips))
        text = html.escape(tmp)
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text).replace("\n", "<br>")
        for chip in chips:
            text = text.replace("\x00", chip, 1)
        paras.append(f"<p>{text.replace(chr(0), '')}</p>")
    stats = {"sentences": len(paras), "cited": cited_paras, "numbers": 0, "numbers_ok": 0, "flagged_sentences": 0}
    return "".join(paras), stats


def _highlight_chunk(text: str, values: List[str]) -> str:
    out = html.escape(text)
    for v in sorted({str(v) for v in values if v}, key=len, reverse=True):
        core = re.sub(r"[^\d.,]", "", v).strip(".,")
        if len(core) < 2:
            continue
        out = re.sub(NUM_IN_TEXT_RE.format(re.escape(html.escape(core))), lambda m: f"<mark>{m.group(0)}</mark>", out)
    return out


XBRL_LABELS = {
    "Revenue": "Revenue", "NetIncome": "Net income", "OperatingIncome": "Operating income", "TotalAssets": "Total assets",
    "TotalLiabilities": "Total liabilities", "StockholdersEquity": "Shareholders' equity", "Equity": "Shareholders' equity",
    "Cash": "Cash", "CashAndEquivalents": "Cash and equivalents", "OperatingCashFlow": "Operating cash flow",
    "EPSDiluted": "Diluted EPS",
}


def _claimed_millions(values: List[str]) -> set:
    """Figures the answer states, in $ millions, so XBRL rows (stored in dollars) can be matched to them."""
    out = set()
    for v in values:
        m = re.search(r"([\d,]+(?:\.\d+)?)\s*(billion|million|thousand|bn|mn|[BMK])?", str(v), re.IGNORECASE)
        if not m:
            continue
        num = float(m.group(1).replace(",", ""))
        scale = (m.group(2) or "").lower()
        mult = {"billion": 1e3, "bn": 1e3, "b": 1e3, "million": 1.0, "mn": 1.0, "m": 1.0, "thousand": 1e-3, "k": 1e-3}.get(scale, 1.0)
        out.add(round(num * mult))
    return out


def _xbrl_table(text: str, values: List[str]) -> Optional[str]:
    """Render an [F-TICKER-YEAR] block (CSV of reported XBRL figures) as a labelled table in $ millions."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    rows = [ln.split(",") for ln in lines if "," in ln and not ln.startswith("[")]
    if len(rows) < 2:
        return None
    header, data = rows[0], rows[-1]
    claimed = _claimed_millions(values)
    out = []
    for col, raw in zip(header, data):
        if col not in XBRL_LABELS or not raw.strip():
            continue
        try:
            val = float(raw)
        except ValueError:
            continue
        if col == "EPSDiluted":
            shown, hit = f"${val:,.2f}", False
        else:
            shown, hit = f"${val / 1e6:,.0f}M", round(val / 1e6) in claimed
        cell = f"<mark>{shown}</mark>" if hit else shown
        out.append(f'<tr><td>{html.escape(XBRL_LABELS[col])}</td><td style="text-align:right">{cell}</td></tr>')
    if not out:
        return None
    return f'<table class="xbrl">{"".join(out)}</table>'


def _source_card(n: int, chunk_id: str, ctx: Optional[Dict[str, Any]], values: List[str], open_: bool,
                 prefix: str = "src") -> str:
    anchor = f' id="{prefix}-{n}"' if n else ""
    if ctx is None:
        return (f'<details class="src"{anchor}><summary>{_chip(n, chunk_id, prefix)}<div class="meta">'
                f'<div class="t1">{html.escape(chunk_id)}</div><div class="t2">Passage text was not kept for this run</div>'
                f"</div></summary></details>")
    ticker, fy = ctx.get("ticker") or "", ctx.get("fiscal_year") or ""
    kind = "Officially reported figures (XBRL)" if _is_xbrl(chunk_id) else "10-K passage"
    title = f"{ticker} FY{fy} · {_section_label(ctx.get('section'))}" if not _is_xbrl(chunk_id) else f"{ticker} FY{fy} · Reported figures"
    is_table = _is_xbrl(chunk_id) or "|" in (ctx.get("text") or "")
    body = (_xbrl_table(ctx.get("text") or "", values) if _is_xbrl(chunk_id) else None) or _highlight_chunk(ctx.get("text") or "", values)
    return (f'<details class="src"{anchor}{" open" if open_ else ""}><summary>{_chip(n, chunk_id, prefix)}'
            f'<div class="meta"><div class="t1">{html.escape(title)}</div>'
            f'<div class="t2">{kind} · <code>{html.escape(chunk_id)}</code></div></div></summary>'
            f'<div class="body{"" if is_table else " prose"}">{body}</div></details>')


def render_answer(run: Dict[str, Any], heading: str = "Answer", open_sources: int = 2, anchor: str = "src") -> Dict[str, str]:
    """Return {"answer", "sources", "uncited", "n_sources", "n_uncited"} HTML for one run.

    `anchor` prefixes the source ids so several answers on one page link to their own sources.
    """
    answer = run.get("answer") or ""
    idx = SourceIndex(run.get("contexts") or [], prefix=anchor)
    guard = run.get("guardrail")
    if guard and not isinstance(guard.get("sentences"), list):
        guard = {**guard, "sentences": []}
    if guard and guard.get("sentences"):
        body, stats = _render_c_sentences(guard, idx)
        body = f"<p>{body}</p>"
    else:
        body, stats = _render_tagged_text(answer, run, idx)

    if not answer.strip():
        body = '<p class="muted">No answer was produced.</p>'
    elif re.match(r"\s*not found in the provided context", answer, re.IGNORECASE):
        body = '<p class="muted">The system answered: <em>“Not found in the provided context.”</em></p>'

    # Head pills: how checkable is this answer?
    pills = []
    if stats["sentences"]:
        cls = "ok" if stats["cited"] == stats["sentences"] else "warn"
        pills.append(f'<span class="tag {cls}">{stats["cited"]}/{stats["sentences"]} sentences cite a passage</span>')
    if guard:
        if stats["numbers"]:
            cls = "ok" if stats["numbers_ok"] == stats["numbers"] else "warn"
            pills.append(f'<span class="tag {cls}">{stats["numbers_ok"]}/{stats["numbers"]} numbers checked ✓</span>')
        else:
            pills.append('<span class="tag">No figures to check</span>')
    else:
        pills.append('<span class="tag">Numbers not checked by this system</span>')
    head = (f'<div class="answer-head"><span class="title">{html.escape(heading)}</span>'
            f'<span style="display:flex;gap:6px;flex-wrap:wrap">{"".join(pills)}</span></div>')
    answer_html = f'<div class="answer">{head}<div class="answer-body">{body}</div></div>'

    # Sources: cited first (numbered as in the answer), then retrieved but uncited.
    values_by_chunk: Dict[str, List[str]] = {}
    if guard:
        for sent in guard.get("sentences") or []:
            if not isinstance(sent, dict):
                continue
            for cid in sent.get("chunk_ids") or []:
                values_by_chunk.setdefault(cid, []).extend(
                    n.get("value") for n in sent.get("numbers") or [] if n.get("status") in ("verified", "derived"))
    cards = [_source_card(i + 1, cid, idx.contexts.get(cid), values_by_chunk.get(cid, []), i < open_sources, anchor)
             for i, cid in enumerate(idx.order)]
    uncited = [c for cid, c in idx.contexts.items() if cid not in idx.order]
    uncited_cards = [
        _source_card(0, str(c.get("chunk_id")), c, [], False).replace('class="src"', 'class="src uncited"').replace(
            '<a class="cite', '<a style="display:none" class="cite')
        for c in uncited
    ]
    return {
        "answer": answer_html,
        "sources": "".join(cards) or '<p class="muted small">This answer cites no sources.</p>',
        "uncited": "".join(uncited_cards),
        "n_sources": str(len(cards)),
        "n_uncited": str(len(uncited_cards)),
    }
