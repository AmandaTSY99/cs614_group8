"""
Case studies: a per-question casebook of the shared 97 x 4 run, separate from RQ1-3 (no new runs, no LLM).

For each benchmark question it puts side by side the gold QA (question, answer, program, key points, gold
evidence) and, for every system, the generated answer, the retrieved chunks (in the system's own order, with
which ones were cited and which ones hold gold evidence) and the per-question metrics already computed by
RQ1, RQ2 and RQ3. Nothing is re-scored except the chunk-level gold-evidence labels, which reuse RQ1's
lexical matcher and are checked against RQ1's `evidence_scores.csv` (fails loudly on any mismatch).

Inputs (all read-only):
    data/benchmark_qa_pool_2015.json      gold QAs
    reports/rq3/records.jsonl              generated answers, contexts, citations, guardrail, cost/latency
    reports/rq1/question_scores.csv        RQ1 retrieval metrics per (system, question)
    reports/rq1/evidence_scores.csv        RQ1 first rank of each gold evidence item
    reports/rq2/full/scores.jsonl          RQ2 citation / numeric / grounding metrics per (system, question)

Outputs (reports/case_studies/):
    README.md            question types, selection rule, metric glossary, outcome grid of selected cases
    case_metrics.csv     one row per (question, system) with every per-question metric used here
    cases/<qid>.md       one page per question (all 97); selected cases are linked from README.md

Usage:
    python scripts/case_studies/build_casebook.py [--per-type 2]
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List, Optional, Tuple

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.rq1.common import BENCHMARK_PATH, RECORDS_PATH, SYSTEMS, load_benchmark, load_records  # noqa: E402
from scripts.rq1.matching import first_rank, relevance_matrix  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
RQ1_DIR = REPO_ROOT / "reports" / "rq1"
RQ2_SCORES = REPO_ROOT / "reports" / "rq2" / "full" / "scores.jsonl"
OUT_DIR = REPO_ROOT / "reports" / "case_studies"

SYSTEM_LABELS = {
    "system_a": "A (vanilla dense)",
    "system_b": "B (hybrid + rerank)",
    "system_c_v1": "C v1 (adaptive multi-hop)",
    "system_c_v2": "C v2 (agentic multi-hop + XBRL)",
}

# Question types = (recipe, hop) cells of the benchmark, in reading order.
QUESTION_TYPES = [
    (("text", "single"), "Single-hop text"),
    (("text", "multi"), "Multi-hop text (one filing)"),
    (("table", "single"), "Single-hop table"),
    (("table", "multi"), "Multi-hop table (one filing)"),
    (("table_text", "multi"), "Table + text (one filing)"),
    (("cross_year_text", "multi"), "Cross-year text"),
    (("cross_year_table", "multi"), "Cross-year table"),
    (("cross_company_text", "multi"), "Cross-company text"),
    (("cross_company_table", "multi"), "Cross-company table"),
]
TYPE_LABEL = dict(QUESTION_TYPES)

RQ1_METRICS = ["n_contexts", "recall@5", "recall@all", "complete@all", "average_precision"]
RQ2_METRICS = ["numeric_accuracy", "citation_precision", "citation_recall", "citation_f1",
               "citation_coverage", "grounding_error_rate"]
RQ3_FIELDS = ["numeric_correct", "keypoint_recall", "hops", "tokens_total", "cost_usd", "latency_ms"]

SNIPPET_CHARS = 220


# --- Loading -------------------------------------------------------------------------------------

def read_csv(path: Path) -> List[Dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_rq1(rq1_dir: Path = RQ1_DIR) -> Tuple[Dict[Tuple[str, str], Dict[str, str]], Dict[Tuple[str, str, int], str]]:
    questions = {(r["system"], r["question_id"]): r for r in read_csv(rq1_dir / "question_scores.csv")}
    evidence = {(r["system"], r["question_id"], int(r["evidence_index"])): r["first_rank"]
                for r in read_csv(rq1_dir / "evidence_scores.csv")}
    return questions, evidence


def load_rq2(path: Path = RQ2_SCORES) -> Dict[Tuple[str, str], Dict[str, Dict[str, Any]]]:
    out: Dict[Tuple[str, str], Dict[str, Dict[str, Any]]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            out.setdefault((row["system"], row["question_id"]), {})[row["metric"]] = row
    return out


# --- Per-record facts ----------------------------------------------------------------------------

def chunk_labels(q: Dict[str, Any], record: Dict[str, Any],
                 rq1_first_ranks: Dict[Tuple[str, str, int], str]) -> List[List[int]]:
    """For each retrieved chunk, the indices of gold evidence items it contains (RQ1 matcher, cross-checked)."""
    contexts = record["retrieved_contexts"]
    rel = relevance_matrix(q["gold_evidence"], contexts)
    for i, row in enumerate(rel):
        mine = first_rank(row)
        theirs = rq1_first_ranks.get((record["system"], q["id"], i))
        if theirs is None:
            raise ValueError(f"RQ1 evidence_scores.csv has no row for {record['system']} {q['id']} evidence {i}")
        if (str(mine) if mine is not None else "") != theirs:
            raise ValueError(f"Gold-evidence rank mismatch with RQ1 for {record['system']} {q['id']} evidence {i}: "
                             f"{mine} here vs {theirs!r} in evidence_scores.csv. Re-run RQ1 scoring first.")
    return [[i for i, row in enumerate(rel) if row[j]] for j in range(len(contexts))]


def answer_score(q: Dict[str, Any], record: Dict[str, Any]) -> Optional[float]:
    """Selection-only summary of RQ3's string-match answer scores, by question type (see README)."""
    parts = []
    if q["type"] in ("numeric", "mixed") and record.get("numeric_correct") is not None:
        parts.append(float(record["numeric_correct"]))
    if q["type"] in ("qualitative", "mixed") and record.get("keypoint_recall") is not None:
        parts.append(float(record["keypoint_recall"]))
    return mean(parts) if parts else None


def num(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    return float(value)


# --- Selection -----------------------------------------------------------------------------------

def select_cases(bench: Dict[str, Dict[str, Any]], scores: Dict[str, Dict[str, Dict[str, Any]]],
                 per_type: int) -> List[Tuple[str, str, str]]:
    """
    (type label, question id, reason) per question type. Deterministic:
      1. "contrast": largest spread (max - min) of the answer score across the 4 systems,
         ties -> larger spread of RQ1 recall@all, then question id.
      2. "hardest": lowest mean answer score across systems, ties -> lower mean recall@all, then id.
    Further picks (per_type > 2) continue the "contrast" ranking.
    """
    picked = []
    for (recipe, hop), label in QUESTION_TYPES:
        qids = sorted(qid for qid, q in bench.items() if q["recipe"] == recipe and q["hop"] == hop)

        def stats(qid: str) -> Tuple[float, float, float, float]:
            ans = [scores[qid][s]["answer_score"] for s in SYSTEMS if scores[qid][s]["answer_score"] is not None]
            rec = [scores[qid][s]["recall@all"] for s in SYSTEMS]
            return (max(ans) - min(ans) if ans else 0.0, mean(ans) if ans else 0.0,
                    max(rec) - min(rec), mean(rec))

        contrast = sorted(qids, key=lambda qid: (-stats(qid)[0], -stats(qid)[2], qid))
        hardest = sorted(qids, key=lambda qid: (stats(qid)[1], stats(qid)[3], qid))
        chosen: List[Tuple[str, str]] = []
        if contrast and per_type >= 1:
            chosen.append((contrast[0], "contrast"))
        if per_type >= 2:
            nxt = next((qid for qid in hardest if qid not in {c for c, _ in chosen}), None)
            if nxt:
                chosen.append((nxt, "hardest"))
        for qid in contrast:
            if len(chosen) >= per_type:
                break
            if qid not in {c for c, _ in chosen}:
                chosen.append((qid, "contrast"))
        picked.extend((label, qid, reason) for qid, reason in chosen)
    return picked


# --- Markdown helpers ----------------------------------------------------------------------------

def cell(text: Any) -> str:
    return re.sub(r"\s+", " ", str(text)).replace("|", "\\|").strip()


def fmt(value: Any, digits: int = 2) -> str:
    if value is None or value == "":
        return "–"
    if isinstance(value, bool):
        return "✓" if value else "✗"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def snippet(text: str) -> str:
    body = text.split("\n", 1)[1] if "\n" in text else text
    body = re.sub(r"\s+", " ", body).strip()
    return body[:SNIPPET_CHARS] + ("…" if len(body) > SNIPPET_CHARS else "")


def short_section(section: str) -> str:
    m = re.match(r"\s*(item\s*\d+[a-z]?)", section or "", re.IGNORECASE)
    head = m.group(1).title().replace("  ", " ") if m else (section or "").split(">")[0].strip()
    tail = section.split(">", 1)[1].strip() if ">" in (section or "") else ""
    return f"{head} › {tail}" if tail else head


def blockquote(text: str) -> str:
    return "\n".join("> " + line if line.strip() else ">" for line in (text or "").strip().splitlines())


def fenced(text: str) -> str:
    return "````text\n" + (text or "").strip() + "\n````"


# --- Case page -----------------------------------------------------------------------------------

def scorecard(qid: str, scores: Dict[str, Dict[str, Any]]) -> List[str]:
    header = "| Metric | " + " | ".join(SYSTEM_LABELS[s] for s in SYSTEMS) + " |"
    lines = [header, "|---|" + "---|" * len(SYSTEMS)]
    rows = [
        ("**Retrieval (RQ1)**", None, None),
        ("chunks retrieved", "n_contexts", 0),
        ("recall@5", "recall@5", 2),
        ("recall@all", "recall@all", 2),
        ("complete@all", "complete@all", 0),
        ("average precision (lexical)", "average_precision", 2),
        ("gold evidence first rank", "evidence_ranks", None),
        ("**Answer (RQ3 string match)**", None, None),
        ("numeric_correct", "numeric_correct", None),
        ("keypoint_recall", "keypoint_recall", 2),
        ("**Answer & citations (RQ2)**", None, None),
        ("numeric_accuracy", "numeric_accuracy", 2),
        ("citation precision", "citation_precision", 2),
        ("citation recall", "citation_recall", 2),
        ("citation F1", "citation_f1", 2),
        ("has a citation", "citation_coverage", 0),
        ("grounding error rate", "grounding_error_rate", 2),
        ("**Cost (RQ3)**", None, None),
        ("retrieval hops", "hops", None),
        ("tokens", "tokens_total", None),
        ("cost (USD)", "cost_usd", 4),
        ("latency (s)", "latency_s", 1),
    ]
    for label, key, digits in rows:
        if key is None:
            lines.append(f"| {label} |" + " |" * len(SYSTEMS))
            continue
        vals = []
        for s in SYSTEMS:
            v = scores[s].get(key)
            if isinstance(v, float) and digits == 0:
                v = int(v)
            vals.append(fmt(v, digits or 2) if not isinstance(v, str) else v)
        lines.append(f"| {label} | " + " | ".join(vals) + " |")
    return lines


def system_section(q: Dict[str, Any], s: str, record: Dict[str, Any], labels: List[List[int]],
                   rq2: Dict[str, Dict[str, Any]]) -> List[str]:
    cited_ids = {str(c.get("chunk_id")) for c in record.get("citations") or []}
    out = [f"### System {SYSTEM_LABELS[s]}", ""]
    out += [f"Model: `{record.get('model')}`. Hops: {record.get('hops')}. "
            f"Chunks retrieved: {len(record['retrieved_contexts'])}, cited: "
            f"{sum(str(m.get('chunk_id')) in cited_ids for m in record['contexts_meta'])}.", ""]
    out += ["**Generated answer**", "", blockquote(record.get("answer") or "(empty)"), ""]

    out += ["**Retrieved chunks** (system's own order; ✓ cited = chunk id appears in the answer's citations; "
            "gold = holds gold evidence item #, by RQ1's lexical matcher)", "",
            "| # | chunk id | section | cited | gold | snippet |", "|---|---|---|---|---|---|"]
    for j, (meta, text) in enumerate(zip(record["contexts_meta"], record["retrieved_contexts"]), 1):
        cid = str(meta.get("chunk_id"))
        gold = ", ".join(f"#{i + 1}" for i in labels[j - 1])
        out.append(f"| {j} | `{cell(cid)}` | {cell(short_section(meta.get('section', '')))} | "
                   f"{'✓' if cid in cited_ids else ''} | {gold} | {cell(snippet(text))} |")
    uncited_retrieved = cited_ids - {str(m.get("chunk_id")) for m in record["contexts_meta"]}
    if uncited_retrieved:
        out += ["", f"Cited chunk ids not in the retrieved list: {', '.join(sorted(uncited_retrieved))}."]
    out.append("")

    shown = [(j, m, t) for j, (m, t) in enumerate(zip(record["contexts_meta"], record["retrieved_contexts"]), 1)
             if str(m.get("chunk_id")) in cited_ids or labels[j - 1]]
    if shown:
        out += ["<details><summary>Full text of cited and gold-matching chunks</summary>", ""]
        for j, meta, text in shown:
            tags = (["cited"] if str(meta.get("chunk_id")) in cited_ids else []) + \
                   [f"gold #{i + 1}" for i in labels[j - 1]]
            out += [f"**#{j} `{meta.get('chunk_id')}`** ({', '.join(tags)})", "", fenced(text), ""]
        out += ["</details>", ""]

    detail = (rq2.get("citation_precision") or {}).get("detail")
    if detail:
        out += [f"RQ2 citation match (section level): `{detail}`", ""]

    gr = record.get("guardrail_report") or {}
    if gr:
        counts = gr.get("semantic_verdict_counts") or {}
        out += [f"**System C guardrail** (judge `{gr.get('semantic_judge_model')}`): "
                f"numerical claims {gr.get('total_numerical_claims')}, "
                f"verified {len(gr.get('verified_numbers') or [])}, "
                f"ungrounded {len(gr.get('ungrounded_numbers') or [])}, "
                f"uncited {len(gr.get('uncited_numbers') or [])}, "
                f"derived {len(gr.get('derived_numbers') or [])}; "
                f"sentence verdicts: " + ", ".join(f"{k} {v}" for k, v in counts.items()) + ".", ""]
        for key in ("ungrounded_numbers", "uncited_numbers"):
            if gr.get(key):
                out += [f"- {key.replace('_', ' ')}: {', '.join(map(str, gr[key]))}"]
        sentences = gr.get("sentences") or []
        if sentences:
            out += ["", "<details><summary>Guardrail sentence verdicts</summary>", "",
                    "| sentence | verdict | judge reason |", "|---|---|---|"]
            out += [f"| {cell(x.get('text', ''))} | {cell(x.get('semantic_verdict', ''))} | "
                    f"{cell(x.get('reason', ''))} |" for x in sentences]
            out += ["", "</details>"]
        out.append("")
    return out


def case_page(q: Dict[str, Any], records: Dict[str, Dict[str, Any]], labels: Dict[str, List[List[int]]],
              scores: Dict[str, Dict[str, Any]], rq2: Dict[str, Dict[str, Dict[str, Any]]]) -> str:
    qtype = TYPE_LABEL[(q["recipe"], q["hop"])]
    ref = records[SYSTEMS[0]]
    out = [f"# {q['id']}: {qtype}", "",
           f"[← all cases](../README.md) · company: {q.get('company')} ({q.get('ticker')}) · fiscal year: "
           f"{q.get('year')} · recipe `{q['recipe']}` · hop `{q['hop']}` · answer type `{q['type']}` · "
           f"scope `{q['scope']}` · RQ2 category `{ref.get('category')}`", ""]

    out += ["## Gold QA", "", "**Question**", "", blockquote(q["question"]), "",
            "**Gold answer**", "", blockquote(q["answer"]), ""]
    if q.get("program"):
        res = ref.get("gold_program_result")
        out += [f"**Program**: `{q['program']}`" + (f" → `{res}`" if res is not None else ""), ""]
    if ref.get("ground_truth_numbers"):
        out += [f"**Gold numbers** (RQ2 numeric_accuracy targets): {', '.join(map(str, ref['ground_truth_numbers']))}", ""]
    if q.get("key_points"):
        out += ["**Key points** (RQ3 keypoint_recall targets)", ""] + [f"{i}. {kp}" for i, kp in
                                                                         enumerate(q["key_points"], 1)] + [""]
    out += ["**Gold evidence**", ""]
    for i, ev in enumerate(q["gold_evidence"], 1):
        out += [f"{i}. `{ev.get('doc_id')}` · {cell(ev.get('item'))} › {cell(ev.get('heading'))} · {ev.get('kind')}",
                "", "   " + blockquote(ev.get("quote", "")).replace("\n", "\n   "), ""]

    out += ["## Scorecard", ""] + scorecard(q["id"], scores) + [""]
    out += ["Definitions: [README › Metrics](../README.md#metrics). `–` = not applicable (e.g. no gold number, "
            "no citations, no guardrail).", ""]

    out += ["## System outputs", ""]
    for s in SYSTEMS:
        out += system_section(q, s, records[s], labels[s], rq2.get((s, q["id"]), {}))
    return "\n".join(out).rstrip() + "\n"


# --- Assembly ------------------------------------------------------------------------------------

def collect_scores(q: Dict[str, Any], records: Dict[str, Dict[str, Any]],
                   rq1_q: Dict[Tuple[str, str], Dict[str, str]],
                   rq1_ev: Dict[Tuple[str, str, int], str],
                   rq2: Dict[Tuple[str, str], Dict[str, Dict[str, Any]]]) -> Dict[str, Dict[str, Any]]:
    out = {}
    for s in SYSTEMS:
        r1 = rq1_q.get((s, q["id"]))
        if r1 is None:
            raise ValueError(f"RQ1 question_scores.csv has no row for {s} {q['id']}")
        rec = records[s]
        row: Dict[str, Any] = {m: num(r1[m]) for m in RQ1_METRICS}
        ranks = [rq1_ev[(s, q["id"], i)] or "–" for i in range(len(q["gold_evidence"]))]
        row["evidence_ranks"] = ", ".join(f"#{i + 1}: {r}" for i, r in enumerate(ranks))
        for m in RQ2_METRICS:
            sc = rq2.get((s, q["id"]), {}).get(m)
            row[m] = sc["value"] if sc and sc.get("status") == "ok" else None
        for f in RQ3_FIELDS:
            row[f] = rec.get(f)
        row["latency_s"] = rec["latency_ms"] / 1000 if rec.get("latency_ms") is not None else None
        row["answer_score"] = answer_score(q, rec)
        out[s] = row
    return out


def readme(bench: Dict[str, Dict[str, Any]], picked: List[Tuple[str, str, str]],
           scores: Dict[str, Dict[str, Dict[str, Any]]]) -> str:
    counts = {label: sum(1 for q in bench.values() if (q["recipe"], q["hop"]) == key) for key, label in QUESTION_TYPES}
    out = ["# Case studies: individual QAs across the four systems", "",
           "A per-question view of the shared 97-question × 4-system run, for examples in the report and slides. "
           "It is **separate from RQ1–RQ3**: it runs nothing new and adds no new scores; every number on these "
           "pages is read from the RQ1, RQ2 and RQ3 outputs listed below, and every answer and chunk is the "
           "system's own generated output.", "",
           "Built by `scripts/case_studies/build_casebook.py` from:", "",
           "- gold QAs: `data/benchmark_qa_pool_2015.json`",
           "- answers, retrieved contexts, citations, guardrail, tokens/cost/latency: `reports/rq3/records.jsonl` "
           "(identical answers to `reports/rq2/full/records.jsonl`)",
           "- retrieval metrics: `reports/rq1/question_scores.csv`, `reports/rq1/evidence_scores.csv`",
           "- citation / numeric / grounding metrics: `reports/rq2/full/scores.jsonl` (judge: none, custom metrics only)",
           "", "Every question has a page in [`cases/`](cases/); per-(question, system) numbers are in "
           "[`case_metrics.csv`](case_metrics.csv).", "",
           "## Question types", "",
           "The benchmark's (recipe, hop) cells give nine question types:", "",
           "| Type | recipe | hop | questions |", "|---|---|---|---|"]
    out += [f"| {label} | `{key[0]}` | `{key[1]}` | {counts[label]} |" for key, label in QUESTION_TYPES]

    out += ["", "## Selected cases", "",
            "Two per type, picked by a fixed rule (not by hand):", "",
            "- **contrast**: the question whose answer score differs most across the four systems "
            "(ties → larger spread in RQ1 recall@all, then question id). Shows where the architectures diverge.",
            "- **hardest**: the question with the lowest mean answer score across systems "
            "(ties → lower mean recall@all, then id). Shows shared failures.", "",
            "*Answer score* (used only for this selection): RQ3's `numeric_correct` for numeric questions, "
            "`keypoint_recall` for qualitative ones, their mean for mixed ones. Both are string-match checks, "
            "so read the answers on each page before calling an answer right or wrong.", "",
            "Cells below: answer score / RQ1 recall@all.", "",
            "| Type | Case | Pick | " + " | ".join(SYSTEM_LABELS[s] for s in SYSTEMS) + " | Question |",
            "|---|---|---|" + "---|" * len(SYSTEMS) + "---|"]
    for label, qid, reason in picked:
        cells = [f"{fmt(scores[qid][s]['answer_score'])} / {fmt(scores[qid][s]['recall@all'])}" for s in SYSTEMS]
        question = bench[qid]["question"]
        question = question[:140] + ("…" if len(question) > 140 else "")
        out.append(f"| {label} | [{qid}](cases/{qid}.md) | {reason} | " + " | ".join(cells) + f" | {cell(question)} |")

    out += ["", "## Metrics", "",
            "| Metric | Source | Meaning |", "|---|---|---|",
            "| chunks retrieved | RQ1 | number of contexts the system passed to generation (max: A 10, B 5, C 17) |",
            "| recall@5 / recall@all | RQ1 | share of gold evidence items found in the first 5 / all retrieved chunks |",
            "| complete@all | RQ1 | 1 if every gold evidence item was found |",
            "| average precision | RQ1 | RAGAS Context Precision formula with lexical labels (not a RAGAS score) |",
            "| gold evidence first rank | RQ1 | rank of the first chunk holding each gold evidence item (– = not found) |",
            "| gold column in chunk tables | RQ1 matcher | chunk holds that gold evidence item: a 6-word sub-phrase "
            "or ≥ 65% of the quote's words appear in it (`scripts/rq1/matching.py`); a lower bound |",
            "| numeric_correct | RQ3 | any number in the answer within 1% of the **first** number in the gold answer "
            "(scale-aware, sign ignored). Recorded for every question whose gold answer has a number, "
            "including qualitative ones; RQ3's accuracy is the mean of this |",
            "| keypoint_recall | RQ3 | share of gold key points whose content words mostly (≥ 50%) appear in the answer |",
            "| numeric_accuracy | RQ2 | share of the gold numbers (`ground_truth_numbers`) found in the answer |",
            "| citation precision / recall / F1 | RQ2 | section-level (10-K item) match of cited chunks against the "
            "gold sections; – when the answer has no citations |",
            "| has a citation | RQ2 | 1 if the answer cites at least one chunk |",
            "| grounding error rate | RQ2 | System C guardrail's share of numerical claims not grounded in the "
            "contexts (A and B have no guardrail) |",
            "| hops, tokens, cost, latency | RQ3 | as recorded for this query in the run |",
            "| cited (chunk tables) | records | the chunk id appears in the answer's `citations` |",
            "| System C guardrail block | records | System C's own guardrail output for the answer, including its "
            "LLM judge's per-sentence verdicts; it is part of the system, not an evaluation judge |",
            "", "## Caveats", "",
            "- Answer scores are string matches. A correct answer phrased differently can score 0, and a wrong "
            "answer that contains the gold number can score 1. Treat the scorecard as a pointer to read the answer.",
            "- Gold-evidence labels are lexical. A chunk can state the same fact in other words, or a quote can be "
            "split across chunks, and not be marked.",
            "- System C retrieves over several hops; records keep the chunk order but not which hop retrieved each "
            "chunk, so the pages do not show per-hop retrieval. v2's XBRL blocks (`F-…` ids) come first.",
            "- System A/B answers were generated with `gpt-5.4-2026-03-05`, System C with `gpt-5.4` "
            "(as recorded in the run).", ""]
    return "\n".join(out)


def build(per_type: int = 2, out_dir: Path = OUT_DIR, benchmark_path: Path = BENCHMARK_PATH,
          records_path: Path = RECORDS_PATH, rq1_dir: Path = RQ1_DIR, rq2_path: Path = RQ2_SCORES) -> List[Tuple[str, str, str]]:
    bench = load_benchmark(benchmark_path)
    records: Dict[str, Dict[str, Dict[str, Any]]] = {}
    for r in load_records(records_path):
        records.setdefault(r["question_id"], {})[r["system"]] = r
    rq1_q, rq1_ev = load_rq1(rq1_dir)
    rq2 = load_rq2(rq2_path)

    missing = [(qid, s) for qid in bench for s in SYSTEMS if s not in records.get(qid, {})]
    if missing:
        raise ValueError(f"Missing records for {len(missing)} (question, system) pairs, e.g. {missing[:3]}")

    scores, labels = {}, {}
    for qid, q in bench.items():
        scores[qid] = collect_scores(q, records[qid], rq1_q, rq1_ev, rq2)
        labels[qid] = {s: chunk_labels(q, records[qid][s], rq1_ev) for s in SYSTEMS}

    cases_dir = out_dir / "cases"
    cases_dir.mkdir(parents=True, exist_ok=True)
    for qid, q in bench.items():
        (cases_dir / f"{qid}.md").write_text(case_page(q, records[qid], labels[qid], scores[qid], rq2),
                                             encoding="utf-8")

    picked = select_cases(bench, scores, per_type)
    (out_dir / "README.md").write_text(readme(bench, picked, scores), encoding="utf-8")

    fields = (["question_id", "question_type", "recipe", "hop", "answer_type", "system", "selected"]
              + RQ1_METRICS + ["evidence_ranks"] + RQ3_FIELDS[:2] + RQ2_METRICS + RQ3_FIELDS[2:]
              + ["answer_score", "n_cited"])
    selected = {qid: reason for _, qid, reason in picked}
    with open(out_dir / "case_metrics.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for qid in sorted(bench):
            q = bench[qid]
            for s in SYSTEMS:
                rec = records[qid][s]
                w.writerow({"question_id": qid, "question_type": TYPE_LABEL[(q["recipe"], q["hop"])],
                            "recipe": q["recipe"], "hop": q["hop"], "answer_type": q["type"], "system": s,
                            "selected": selected.get(qid, ""),
                            "n_cited": len({str(c.get("chunk_id")) for c in rec.get("citations") or []}),
                            **{k: scores[qid][s][k] for k in fields if k in scores[qid][s]}})
    return picked


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--per-type", type=int, default=2, help="cases selected per question type (default 2)")
    ap.add_argument("--out", type=Path, default=OUT_DIR)
    args = ap.parse_args()
    picked = build(args.per_type, args.out)
    print(f"Wrote {args.out / 'README.md'} ({len(picked)} selected cases), {args.out / 'cases'}/, "
          f"{args.out / 'case_metrics.csv'}")


if __name__ == "__main__":
    main()
