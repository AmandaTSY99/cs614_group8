"""
Shared Citation Utilities for System C (Synthesizer, Guardrail, and Repair).

Supports Research Question 2 (Citation Grounding, Attribution & Precision):
- Tag-aware sentence splitting and strict tag -> chunk_id resolution.
- Standardized citation tag formatting: `[<TICKER> FY<YEAR>, <SECTION>, <CHUNK_ID>]` / `[F-<TICKER>-<YEAR>]`.
- Evidence-label expansion for the synthesizer prompt.
- Structured `CitationRecord` generation per (sentence, chunk) pair.
"""

import re
from typing import Any, Dict, List, Tuple

from src.system_c.state import CitationRecord

BRACKET_RE = re.compile(r"\[([^\[\]]+)\]")
# A bracket counts as a citation tag only if it looks like one: chunk id `...:42`, `F-NVDA-2026`, `FY2026`,
# or a synthesizer evidence label such as `E3` / `E1, E3` (so a leftover unknown label is reported as invalid).
CITATION_LIKE_RE = re.compile(
    r":\d+\b|\bF-[A-Z]{1,6}-\d{4}\b|\bFY\s?\d{4}\b|^\s*E\d+(?:\s*,\s*E\d+)*\s*$"
)
ABBREVIATIONS = ("inc.", "corp.", "co.", "ltd.", "u.s.", "e.g.", "i.e.", "vs.", "no.", "approx.", "fig.")
LABEL_GROUP_RE = re.compile(r"\[\s*(E\d+(?:\s*,\s*E\d+)*)\s*\]")
BACKTICKED_BRACKETS_RE = re.compile(r"`+\s*((?:\[[^\[\]]+\]\s*)+?)\s*`+")
SECTION_ITEM_RE = re.compile(r"^\s*(Item\s+\d+[A-Z]?)\b", re.IGNORECASE)
MAX_TAG_CHARS = 80


# ---------------------------------------------------------------------------
# Sentences
# ---------------------------------------------------------------------------


def split_sentences(answer: str) -> List[str]:
    """
    Split an answer into sentences, keeping citation tags with the sentence they follow
    (e.g. `Revenue grew. [NVDA FY2026, Item 7, X:1]` stays one sentence).
    """
    # Mask `[...]` tags so periods inside section names (`Item 15. Exhibits`) never split a sentence
    tags: List[str] = []

    def _mask(m: "re.Match[str]") -> str:
        tags.append(m.group(0))
        return f"\x00{len(tags) - 1}\x00"

    masked = BRACKET_RE.sub(_mask, answer)
    sentences = [_unmask(s, tags) for s in _split_masked(masked, tags)]
    return [s for s in sentences if re.search(r"[A-Za-z0-9]", BRACKET_RE.sub(" ", s))]


def _unmask(text: str, tags: List[str]) -> str:
    return re.sub(r"\x00(\d+)\x00", lambda m: tags[int(m.group(1))], text)


def _split_masked(answer: str, tags: List[str]) -> List[str]:
    sentences: List[str] = []
    for line in answer.splitlines():
        line = re.sub(r"^\s*(?:[-*•]|\d+[.)])\s+", "", line).strip()
        if not line:
            continue
        parts = re.split(r"(?<=[.!?])\s+", line)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            if sentences and _ends_with_abbreviation(sentences[-1]):
                sentences[-1] = f"{sentences[-1]} {part}"
                continue
            # Move leading citation tags back onto the previous sentence
            lead = re.match(r"^((?:\x00\d+\x00\s*)+)(.*)$", part)
            if lead and sentences and CITATION_LIKE_RE.search(_unmask(lead.group(1), tags)):
                sentences[-1] = f"{sentences[-1]} {lead.group(1).strip()}"
                part = lead.group(2).strip()
                if not part:
                    continue
            sentences.append(part)
    return sentences


def _ends_with_abbreviation(text: str) -> bool:
    last = text.rsplit(None, 1)[-1].lower() if text.split() else ""
    return last in ABBREVIATIONS


# ---------------------------------------------------------------------------
# Tags
# ---------------------------------------------------------------------------


def find_citation_tags(text: str) -> List[str]:
    """Return citation-like `[...]` tags (ignores brackets such as `[figure not disclosed in filing]`)."""
    return [m.group(0) for m in BRACKET_RE.finditer(text) if CITATION_LIKE_RE.search(m.group(1))]


def resolve_citation_tags(sentence: str, evidence: List[Dict[str, Any]]) -> Tuple[List[str], List[str], List[str]]:
    """
    Strictly map each citation tag in `sentence` to evidence chunk_ids.
    A tag resolves only if an evidence chunk_id appears in it as a whole token
    (no section-name fallback). Returns `(tags, chunk_ids, invalid_tags)`.
    """
    tags = find_citation_tags(sentence)
    chunk_ids: List[str] = []
    invalid: List[str] = []
    for tag in tags:
        matched = _resolve_tag(tag, evidence)
        if not matched:
            invalid.append(tag)
        for cid in matched:
            if cid not in chunk_ids:
                chunk_ids.append(cid)
    return tags, chunk_ids, invalid


def _resolve_tag(tag: str, evidence: List[Dict[str, Any]]) -> List[str]:
    inner = tag[1:-1]
    return [
        str(c["chunk_id"])
        for c in evidence
        if re.search(rf"(?<![\w-]){re.escape(str(c['chunk_id']))}(?!\w)", inner)
    ]


def short_section(section: Any) -> str:
    """Top-level 10-K item from section metadata: `"Item 7. Management's ..."` -> `"Item 7"`; fallback `10-K`."""
    m = SECTION_ITEM_RE.match(str(section or ""))
    if not m:
        return "10-K"
    return re.sub(r"\s+", " ", m.group(1)).replace("item", "Item").replace("ITEM", "Item")


def format_tag(chunk: Dict[str, Any], default_ticker: str = "NVDA") -> str:
    """
    Handoff-format citation tag for an evidence chunk (at most 80 characters):
    `[F-<TICKER>-<YEAR>]` for XBRL blocks, else `[<TICKER> FY<YEAR>, <SHORT_SECTION>, <CHUNK_ID>]`,
    falling back to section `10-K` and then to `[<CHUNK_ID>]` if the tag would be too long.
    """
    cid = str(chunk["chunk_id"])
    if cid.startswith("F-"):
        return f"[{cid}]"
    meta = chunk.get("metadata", {}) or {}
    tkr = meta.get("ticker", default_ticker)
    fy = meta.get("fiscal_year", "N/A")
    for section in (short_section(meta.get("section")), "10-K"):
        tag = f"[{tkr} FY{fy}, {section}, {cid}]"
        if len(tag) <= MAX_TAG_CHARS:
            return tag
    return f"[{cid}]"


def expand_labels(
    answer: str,
    label_map: Dict[str, Dict[str, Any]],
    default_ticker: str = "NVDA",
) -> Tuple[str, List[str]]:
    """
    Expand synthesizer evidence labels into handoff-format tags.
    `[E1]`, `[E1][E3]` and `[E1, E3]` become separate adjacent tags; backticks around labels/tags are
    stripped; unknown labels (e.g. `[E99]`) are left in place so the guardrail reports them as invalid.
    Returns `(expanded_text, unknown_labels)`.
    """
    text = BACKTICKED_BRACKETS_RE.sub(lambda m: m.group(1).strip(), answer)
    unknown: List[str] = []

    def _expand(m: "re.Match[str]") -> str:
        parts = []
        for label in re.split(r"\s*,\s*", m.group(1).strip()):
            chunk = label_map.get(label)
            if chunk is None:
                unknown.append(label)
                parts.append(f"[{label}]")
            else:
                parts.append(format_tag(chunk, default_ticker))
        return " ".join(parts)

    text = LABEL_GROUP_RE.sub(_expand, text)
    # `[E1][E3]` -> two expanded tags that now touch; put a space between adjacent tags
    text = re.sub(r"\](?=\[)", "] ", text)
    return text, unknown


# ---------------------------------------------------------------------------
# Citation records
# ---------------------------------------------------------------------------


def strip_tags(sentence: str) -> str:
    """Sentence text with citation tags removed and whitespace tidied."""
    text = sentence
    for tag in find_citation_tags(sentence):
        text = text.replace(tag, " ")
    text = re.sub(r"\(\s*\)", " ", text)
    text = re.sub(r"\s+([.,;:!?)])", r"\1", re.sub(r"\s+", " ", text))
    return text.strip()


def build_citation_records(answer: str, evidence: List[Dict[str, Any]]) -> List[CitationRecord]:
    """
    One `CitationRecord` per (sentence, resolved chunk) pair, with no de-duplication across sentences.
    `supported_claim` is the sentence with its tags removed. Unresolved tags produce no record
    (the guardrail reports them in `invalid_citations`).
    """
    chunk_by_id = {str(c["chunk_id"]): c for c in evidence}
    records: List[CitationRecord] = []
    for sentence in split_sentences(answer):
        claim = strip_tags(sentence)
        seen = set()
        for tag in find_citation_tags(sentence):
            for cid in _resolve_tag(tag, evidence):
                if cid in seen:
                    continue
                seen.add(cid)
                meta = chunk_by_id[cid].get("metadata", {}) or {}
                records.append(
                    CitationRecord(
                        tag=tag,
                        chunk_id=cid,
                        ticker=str(meta.get("ticker", "UNKNOWN")),
                        fiscal_year=meta.get("fiscal_year", "N/A"),
                        section=str(meta.get("section", "N/A")),
                        supported_claim=claim,
                    )
                )
    return records
