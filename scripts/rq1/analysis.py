"""
RQ1 Stage 3: do the Stage 2 differences hold up? Significance, context-budget fairness, matcher validity.
Pure standard library, deterministic (seeded), never re-runs systems. Writes `paired_tests.csv` and `analysis.md`.

1. Paired tests. All four systems answer the same 97 questions, so every comparison is paired by question.
   Binary metric (complete@all): exact McNemar test. Continuous metrics: sign-flip permutation test on the
   per-question differences, plus a paired bootstrap 95% CI of the mean difference. Holm correction over every
   test in the table (the family is all pairs x all metrics, i.e. deliberately conservative).
2. Budget fairness. System B returns 5 chunks, System C up to 17, so context_recall rewards a bigger context.
   `recall@Nchars` keeps only the leading chunks that fit in a character budget, whatever the system.
3. Matcher validity. (a) Sensitivity: the matcher's thresholds are varied and the system ranking re-derived;
   `grounded` additionally requires the matching chunk to come from the gold ticker and fiscal year.
   (b) False positives: each gold quote is matched against the contexts the same system retrieved for a
   *different* question on other filings, where a correct match is impossible, so anything found is spurious.
4. Failure overlap: how many questions are lost by every system, and how often each system wins alone.

Usage:
    python scripts/rq1/analysis.py [--records reports/rq3/records.jsonl] [--out reports/rq1]
"""

import argparse
import csv
import math
import random
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.rq1.common import (  # noqa: E402
    BENCHMARK_PATH, FACETS, OUT_DIR, QUESTION_SCORES_FILE, RECORDS_PATH, SYSTEMS, load_benchmark, load_records,
)
from scripts.rq1.matching import evidence_in_contexts, first_rank, normalize_text, relevance_matrix  # noqa: E402
from scripts.rq1.score import question_metrics  # noqa: E402
from scripts.rq2.report import bootstrap_ci  # noqa: E402

PAIRED_FILE = "paired_tests.csv"
ANALYSIS_FILE = "analysis.md"
SEED = 614
N_PERM = 10_000
CHAR_BUDGET = 4_000  # about System B's whole context (mean 4.8k chars), so all systems are compared at its size
CHAR_BUDGETS = (2_000, 4_000, 6_000, 8_000)
BUDGET_METRIC = f"recall@{CHAR_BUDGET}chars"
BINARY_METRICS = ("complete@all",)
PAIRED_METRICS = ("complete@all", "context_recall", "recall@5", BUDGET_METRIC, "context_precision")
DEFAULT = "default (6-word phrase or 65% words)"
NUMERIC = "numeric-anchored (default + every number of the quote)"
PHRASE_ONLY = "phrase only"
# label -> (matcher kwargs, require the gold ticker + fiscal year on the matching chunk)
MATCHERS: Dict[str, Tuple[Dict[str, Any], bool]] = {
    DEFAULT: ({}, False),
    "lenient (phrase or 50% words)": ({"word_overlap": 0.50}, False),
    "strict (phrase or 80% words)": ({"word_overlap": 0.80}, False),
    NUMERIC: ({"require_numbers": True}, False),
    PHRASE_ONLY: ({"word_overlap": None}, False),
    "grounded (default + gold ticker/year)": ({}, True),
    "grounded + numeric-anchored": ({"require_numbers": True}, True),
}
DECOY_MATCHERS = (DEFAULT, NUMERIC, PHRASE_ONLY)
AUDIT_FILE = "match_audit_sample.csv"
TYPE_FILE = "by_question_type.csv"
CONTRAST_FILE = "question_type_contrasts.csv"
TYPE_FACETS = ("recipe", "modality", "scope", "hop", "evidence_count", "section_spread")
TYPE_METRICS = ("complete@all", BUDGET_METRIC)
TYPE_PAIRS = (("system_b", "system_a"), ("system_c_v1", "system_b"), ("system_c_v1", "system_a"),
              ("system_c_v2", "system_b"))
# Does a system's advantage depend on the question type? (facet, label, group set 1, group set 2)
CONTRASTS = (("modality", "text vs table", {"text"}, {"table"}),
             ("scope", "single_doc vs multi-doc (cross_year + cross_company)", {"single_doc"},
              {"cross_year", "cross_company"}),
             ("hop", "single-hop vs multi-hop (benchmark label)", {"single"}, {"multi"}),
             ("section_spread", "1 item vs 2+ items", {"1 item"}, {"2+ items"}))
AUDIT_SIZE = 40


# ---------------------------------------------------------------- statistics

def mcnemar_exact(only_x: int, only_y: int) -> float:
    """Two-sided exact McNemar p from the discordant counts (x succeeds alone, y succeeds alone)."""
    n = only_x + only_y
    if n == 0:
        return 1.0
    tail = sum(math.comb(n, i) for i in range(min(only_x, only_y) + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def sign_flip_p(diffs: Sequence[float], n_perm: int = N_PERM, seed: int = SEED) -> float:
    """Two-sided Monte-Carlo sign-flip permutation p for mean(diffs) = 0 (add-one corrected)."""
    nonzero = [d for d in diffs if d != 0]
    if not nonzero:
        return 1.0
    rng = random.Random(seed)
    observed = abs(sum(nonzero))
    hits = 0
    for _ in range(n_perm):
        bits = rng.getrandbits(len(nonzero))
        total = sum(d if (bits >> i) & 1 else -d for i, d in enumerate(nonzero))
        hits += abs(total) >= observed - 1e-12
    return (hits + 1) / (n_perm + 1)


def holm(p_values: Sequence[float]) -> List[float]:
    """Holm-Bonferroni adjusted p-values, in the input order."""
    m = len(p_values)
    order = sorted(range(m), key=lambda i: p_values[i])
    adjusted, running = [0.0] * m, 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * p_values[i]))
        adjusted[i] = running
    return adjusted


def paired_tests(question_rows: List[Dict[str, Any]], systems: Sequence[str] = SYSTEMS,
                 metrics: Sequence[str] = PAIRED_METRICS) -> List[Dict[str, Any]]:
    """One row per (metric, system_x, system_y): mean(x - y) with paired bootstrap CI, raw and Holm p."""
    by_key = {(r["system"], r["question_id"]): r for r in question_rows}
    qids = sorted({r["question_id"] for r in question_rows})
    systems = [s for s in systems if any(r["system"] == s for r in question_rows)]
    out: List[Dict[str, Any]] = []
    for metric in metrics:
        for y, x in combinations(systems, 2):  # SYSTEMS is ordered baseline-first, so x is the "newer" system
            xs = [float(by_key[(x, q)][metric]) for q in qids]
            ys = [float(by_key[(y, q)][metric]) for q in qids]
            diffs = [a - b for a, b in zip(xs, ys)]
            low, high = bootstrap_ci(diffs)
            only_x, only_y = sum(d > 0 for d in diffs), sum(d < 0 for d in diffs)
            p = mcnemar_exact(only_x, only_y) if metric in BINARY_METRICS else sign_flip_p(diffs)
            out.append({"metric": metric, "system_x": x, "system_y": y, "n": len(qids),
                        "mean_x": sum(xs) / len(xs), "mean_y": sum(ys) / len(ys),
                        "mean_diff": sum(diffs) / len(diffs), "ci_low": low, "ci_high": high,
                        "x_better": only_x, "y_better": only_y, "p": p,
                        "test": "mcnemar_exact" if metric in BINARY_METRICS else "sign_flip_permutation"})
    for row, p_adj in zip(out, holm([r["p"] for r in out])):
        row["p_holm"] = p_adj
    for metric in metrics:  # the less conservative reading: one family per metric
        family = [r for r in out if r["metric"] == metric]
        for row, p_adj in zip(family, holm([r["p"] for r in family])):
            row["p_holm_metric"] = p_adj
    return out


# ------------------------------------------------------------------ scoring

def recall_at_chars(rel: List[List[bool]], contexts: Sequence[str], budget: int) -> float:
    """Share of gold evidence found in the leading chunks whose cumulative length stays within `budget` chars."""
    keep, used = 0, 0
    for ctx in contexts:
        used += len(ctx)
        if used > budget:
            break
        keep += 1
    ranks = [first_rank(row) for row in rel]
    return sum(r is not None and r <= keep for r in ranks) / len(ranks)


def ground(rel: List[List[bool]], gold: List[Dict[str, Any]], meta: List[Dict[str, Any]]) -> List[List[bool]]:
    """Keep a match only if the chunk comes from the gold evidence's own ticker and fiscal year."""
    return [[hit and m.get("ticker") == ev.get("ticker") and int(m.get("fiscal_year") or 0) == int(ev.get("year") or -1)
             for hit, m in zip(row, meta)] for ev, row in zip(gold, rel)]


def score_records(bench: Dict[str, Dict[str, Any]], records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Per-record budget recall, per-matcher recall/completeness, plus context sizes."""
    budget_rows: List[Dict[str, Any]] = []
    matcher_rows: List[Dict[str, Any]] = []
    for r in records:
        qid, system = r.get("question_id") or r.get("query_id"), r["system"]
        gold, contexts, meta = bench[qid]["gold_evidence"], r["retrieved_contexts"], r.get("contexts_meta") or []
        base = relevance_matrix(gold, contexts)
        budget_rows.append({"system": system, "question_id": qid, "chars": sum(map(len, contexts)),
                            **{f"recall@{b}chars": recall_at_chars(base, contexts, b) for b in CHAR_BUDGETS}})
        for label, (kwargs, grounded) in MATCHERS.items():
            rel = relevance_matrix(gold, contexts, **kwargs)
            if grounded:
                if len(meta) != len(contexts):
                    raise ValueError(f"{system}/{qid}: {len(meta)} contexts_meta entries for {len(contexts)} contexts")
                rel = ground(rel, gold, meta)
            m = question_metrics(rel)
            matcher_rows.append({"system": system, "question_id": qid, "matcher": label,
                                 "context_recall": m["context_recall"], "complete@all": m["complete@all"]})
    return {"budget": budget_rows, "matchers": matcher_rows}


def decoy_false_positives(bench: Dict[str, Dict[str, Any]], records: List[Dict[str, Any]], seed: int = SEED,
                          matchers: Sequence[str] = DECOY_MATCHERS) -> List[Dict[str, Any]]:
    """
    Share of gold evidence items "found" in contexts retrieved by the same system for a decoy question whose gold
    filings (ticker, year) are all different, so that a true match is impossible. One row per (system, matcher, kind).
    """
    filings = {qid: {(ev["ticker"], int(ev["year"])) for ev in q["gold_evidence"]} for qid, q in bench.items()}
    by_system: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(dict)
    for r in records:
        by_system[r["system"]][r.get("question_id") or r.get("query_id")] = r
    rng = random.Random(seed)
    counts: Dict[Tuple[str, str, str], List[int]] = defaultdict(lambda: [0, 0])
    for system, recs in sorted(by_system.items()):
        for qid, r in sorted(recs.items()):
            candidates = sorted(d for d in recs if not filings[d] & filings[qid])
            if not candidates:
                continue
            decoy = recs[rng.choice(candidates)]
            for label in matchers:
                rel = relevance_matrix(bench[qid]["gold_evidence"], decoy["retrieved_contexts"], **MATCHERS[label][0])
                for ev, row in zip(bench[qid]["gold_evidence"], rel):
                    cell = counts[(system, label, ev["kind"])]
                    cell[0] += any(row)
                    cell[1] += 1
    return [{"system": s, "matcher": m, "kind": k, "false_positive_rate": hit / n, "items": n}
            for (s, m, k), (hit, n) in sorted(counts.items())]


def audit_sample(bench: Dict[str, Dict[str, Any]], records: List[Dict[str, Any]], size: int = AUDIT_SIZE,
                 seed: int = SEED) -> List[Dict[str, Any]]:
    """
    Random sample of matches that only the word-overlap rule accepts (the phrase rule rejects them), for manual
    labelling: they are 60% of all credited evidence and the part of the matcher that could be spurious.
    `human_label` is left empty: fill in 1 if the chunk really contains the quoted fact, 0 if not.
    """
    pool = []
    for r in records:
        qid = r.get("question_id") or r.get("query_id")
        for ev in bench[qid]["gold_evidence"]:
            for j, chunk in enumerate(r["retrieved_contexts"]):
                if evidence_in_contexts(ev, [chunk]) and not evidence_in_contexts(ev, [chunk], word_overlap=None):
                    quote_words, chunk_words = set(normalize_text(ev["quote"]).split()), set(normalize_text(chunk).split())
                    pool.append({"system": r["system"], "question_id": qid, "kind": ev["kind"], "ticker": ev["ticker"],
                                 "year": ev["year"], "chunk_rank": j + 1,
                                 "word_overlap": round(len(quote_words & chunk_words) / len(quote_words), 2),
                                 "numeric_anchored_accepts": evidence_in_contexts(ev, [chunk], require_numbers=True),
                                 "quote": ev["quote"], "chunk_excerpt": chunk[:600], "human_label": ""})
                    break  # one (the first) matching chunk per evidence item
    return random.Random(seed).sample(pool, min(size, len(pool)))


def _type_pairs(systems: Sequence[str]) -> List[Tuple[str, str]]:
    return [(x, y) for x, y in TYPE_PAIRS if x in systems and y in systems]


def group_diff_p(a: Sequence[float], b: Sequence[float], n_perm: int = N_PERM, seed: int = SEED) -> float:
    """Two-sided label-permutation p for mean(a) = mean(b) (two independent groups of per-question values)."""
    observed = abs(sum(a) / len(a) - sum(b) / len(b))
    pooled, rng, hits = list(a) + list(b), random.Random(seed), 0
    for _ in range(n_perm):
        rng.shuffle(pooled)
        hits += abs(sum(pooled[:len(a)]) / len(a) - sum(pooled[len(a):]) / len(b)) >= observed - 1e-12
    return (hits + 1) / (n_perm + 1)


def by_question_type(question_rows: List[Dict[str, Any]], systems: Sequence[str]) -> Dict[str, Any]:
    """
    Per question-type group: mean score per system (the scoreboard) and paired differences with bootstrap CIs
    (exploratory: subgroup n is small and nothing is corrected). Plus interaction tests: is a system pair's
    advantage different between two groups of questions?
    """
    by_key = {(r["system"], r["question_id"]): r for r in question_rows}
    facet_of = {r["question_id"]: r for r in question_rows if r["system"] == systems[0]}
    cells: List[Dict[str, Any]] = []
    for facet in TYPE_FACETS:
        for group in FACETS[facet]:
            qids = sorted(q for q, r in facet_of.items() if r[facet] == group)
            if not qids:
                continue
            for metric in TYPE_METRICS:
                means = {s: sum(float(by_key[(s, q)][metric]) for q in qids) / len(qids) for s in systems}
                cell: Dict[str, Any] = {"facet": facet, "group": group, "n": len(qids), "metric": metric,
                                        **{f"mean_{s}": v for s, v in means.items()}}
                for x, y in _type_pairs(systems):
                    diffs = [float(by_key[(x, q)][metric]) - float(by_key[(y, q)][metric]) for q in qids]
                    low, high = bootstrap_ci(diffs)
                    cell[f"diff_{x}_minus_{y}"] = sum(diffs) / len(diffs)
                    cell[f"ci_low_{x}_minus_{y}"], cell[f"ci_high_{x}_minus_{y}"] = low, high
                cells.append(cell)
    interactions: List[Dict[str, Any]] = []
    for facet, label, set1, set2 in CONTRASTS:
        for metric in TYPE_METRICS:
            for x, y in _type_pairs(systems):
                d1, d2 = ([float(by_key[(x, q)][metric]) - float(by_key[(y, q)][metric])
                           for q, r in sorted(facet_of.items()) if r[facet] in grp] for grp in (set1, set2))
                if not d1 or not d2:
                    continue  # one of the two groups has no question
                interactions.append({"contrast": label, "metric": metric, "system_x": x, "system_y": y,
                                     "n1": len(d1), "n2": len(d2), "diff_group1": sum(d1) / len(d1),
                                     "diff_group2": sum(d2) / len(d2),
                                     "difference_in_differences": sum(d1) / len(d1) - sum(d2) / len(d2),
                                     "p": group_diff_p(d1, d2)})
    return {"cells": cells, "interactions": interactions}


def failure_overlap(question_rows: List[Dict[str, Any]], systems: Sequence[str]) -> Dict[str, Any]:
    """Questions lost by every system, solved by at least one, and solved by exactly one (complete@all)."""
    solved: Dict[str, set] = defaultdict(set)
    for r in question_rows:
        if float(r["complete@all"]) == 1.0:
            solved[r["question_id"]].add(r["system"])
    qids = sorted({r["question_id"] for r in question_rows})
    sole = {s: sum(solved[q] == {s} for q in qids) for s in systems}
    return {"n": len(qids), "none": [q for q in qids if not solved[q]], "any": sum(bool(solved[q]) for q in qids),
            "all": sum(len(solved[q]) == len(systems) for q in qids), "sole": sole}


# ---------------------------------------------------------------- rendering

def _mean_ci(values: List[float]) -> str:
    low, high = bootstrap_ci(values)
    return f"{sum(values) / len(values):.2f} [{low:.2f}, {high:.2f}]"


def _stars(p: float) -> str:
    return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"


def render_analysis(tests: List[Dict[str, Any]], scored: Dict[str, Any], fps: List[Dict[str, Any]],
                    overlap: Dict[str, Any], systems: Sequence[str], n_questions: int) -> str:
    lines = ["# RQ1 analysis: significance, budget fairness and matcher validity", "",
             f"{n_questions} questions x {len(systems)} systems, seed {SEED}. Companion to `report.md`; "
             "regenerated by `scripts/rq1/analysis.py`.", "",
             "## 1. Paired significance tests", "",
             "Every comparison is paired by question. `diff` is mean(x - y) with a paired bootstrap 95% CI. "
             "complete@all uses an exact McNemar test (x only / y only = questions only one of the two solves); the other "
             f"metrics use a sign-flip permutation test ({N_PERM:,} flips). `p_holm` is Holm-adjusted over all "
             f"{len(tests)} tests in this section (conservative); `p_holm_m` over the 6 pairs of its own metric only. "
             "sig is judged on `p_holm`; ns = not significant at 0.05 after correction.", ""]
    for metric in PAIRED_METRICS:
        lines += [f"**{metric}**", "", "| x vs y | mean x | mean y | diff [95% CI] | x only / y only | p | p_holm | p_holm_m | sig |",
                  "|---|---|---|---|---|---|---|---|---|"]
        for t in (t for t in tests if t["metric"] == metric):
            tail = f"{t['x_better']} / {t['y_better']}"
            lines.append(f"| {t['system_x']} vs {t['system_y']} | {t['mean_x']:.2f} | {t['mean_y']:.2f} | "
                         f"{t['mean_diff']:+.2f} [{t['ci_low']:+.2f}, {t['ci_high']:+.2f}] | {tail} | "
                         f"{t['p']:.4f} | {t['p_holm']:.4f} | {t['p_holm_metric']:.4f} | {_stars(t['p_holm'])} |")
        lines.append("")
    lines += ["x only / y only: questions where x's score is higher / y's score is higher (ties not shown).", "",
              "## 2. Context-budget fairness", "",
              "Systems return different amounts of context, so full-context recall favours bigger contexts. "
              "Recall keeping only the leading chunks that fit in a character budget (mean [95% CI] over questions):", "",
              "| system | mean context chars | " + " | ".join(f"@{b:,} chars" for b in CHAR_BUDGETS) + " | full context |",
              "|---|---|" + "---|" * (len(CHAR_BUDGETS) + 1)]
    full = {(r["system"], r["question_id"]): float(r["context_recall"]) for r in scored["question_rows"]}
    for s in systems:
        rows = [r for r in scored["budget"] if r["system"] == s]
        cells = [_mean_ci([r[f"recall@{b}chars"] for r in rows]) for b in CHAR_BUDGETS]
        full_vals = [v for (sys_, _), v in full.items() if sys_ == s]
        lines.append(f"| {s} | {sum(r['chars'] for r in rows) / len(rows):,.0f} | " + " | ".join(cells)
                     + f" | {_mean_ci(full_vals)} |")
    lines += ["", f"Paired tests at the {CHAR_BUDGET:,}-character budget are in section 1 (`{BUDGET_METRIC}`).", "",
              "## 3. Is the lexical matcher trustworthy?", "",
              "### 3a. Sensitivity of the conclusions to the matcher", "",
              "context_recall / complete@all per system under each matcher; the last column is the system ranking by "
              "context_recall. If the ranking is stable, the conclusions do not depend on the threshold choice.", "",
              "| matcher | " + " | ".join(systems) + " | ranking by context_recall |", "|---|" + "---|" * (len(systems) + 1)]
    for label in MATCHERS:
        rows = [r for r in scored["matchers"] if r["matcher"] == label]
        means = {s: (sum(r["context_recall"] for r in rows if r["system"] == s) / n_questions,
                     sum(r["complete@all"] for r in rows if r["system"] == s) / n_questions) for s in systems}
        ranking = " > ".join(sorted(systems, key=lambda s: -means[s][0]))
        lines.append(f"| {label} | " + " | ".join(f"{means[s][0]:.2f} / {means[s][1]:.2f}" for s in systems)
                     + f" | {ranking} |")
    lines += ["", "### 3b. False-positive rate (decoy contexts)", "",
              "Each gold quote is matched against the contexts the same system retrieved for a different question on "
              "different filings. A correct match is impossible, so every hit is spurious. Lower is better; "
              "this is the credit the matcher hands out for free.", "",
              "| matcher | kind | " + " | ".join(systems) + " |", "|---|---|" + "---|" * len(systems)]
    for label in dict.fromkeys(f["matcher"] for f in fps):
        for kind in ("table", "text"):
            cells = {f["system"]: f for f in fps if f["matcher"] == label and f["kind"] == kind}
            lines.append(f"| {label} | {kind} | "
                         + " | ".join(f"{cells[s]['false_positive_rate']:.1%} (n={cells[s]['items']})" if s in cells else "–"
                                      for s in systems) + " |")
    lines += ["", "## 4. Failure overlap (complete@all)", "",
              f"- Solved by every system: {overlap['all']} / {overlap['n']}",
              f"- Solved by at least one system (oracle ceiling): {overlap['any']} / {overlap['n']}",
              f"- Lost by every system: {len(overlap['none'])} / {overlap['n']} ({', '.join(overlap['none']) or 'none'})",
              "- Solved by exactly one system: " + ", ".join(f"{s} {n}" for s, n in overlap["sole"].items()), ""]
    return "\n".join(lines)


def render_by_question_type(typed: Dict[str, Any], systems: Sequence[str]) -> List[str]:
    lines = ["", "## 5. Performance by question type", "",
             "**Bold** = best mean in the row (ties both bold). Differences are paired by question, mean(x - y) with a "
             "bootstrap 95% CI; `*` = CI excludes 0. Subgroups have n = 4 to 76 and nothing here is multiplicity-corrected, "
             "so read them as exploratory effect sizes, not confirmed findings. "
             f"`{BUDGET_METRIC}` is the equal-budget view (see section 2).", ""]
    labels = {"recipe": "recipe (what evidence a question needs)", "modality": "modality of the gold evidence",
              "scope": "scope (documents spanned)", "hop": "hop (benchmark label)", "evidence_count": "number of gold evidence items",
              "section_spread": "10-K items the evidence spans"}
    pair_names = [f"{x.replace('system_', '')} - {y.replace('system_', '')}" for x, y in _type_pairs(systems)]
    for metric in TYPE_METRICS:
        lines += [f"### 5a. Scoreboard and paired differences: {metric}", ""]
        for facet in TYPE_FACETS:
            rows = [c for c in typed["cells"] if c["facet"] == facet and c["metric"] == metric]
            lines += [f"**{labels[facet]}**", "",
                      "| group (n) | " + " | ".join(systems) + " | " + " | ".join(pair_names) + " |",
                      "|---|" + "---|" * (len(systems) + len(pair_names))]
            for c in rows:
                best = max(c[f"mean_{s}"] for s in systems)
                means = [f"**{c[f'mean_{s}']:.2f}**" if abs(c[f"mean_{s}"] - best) < 1e-9 else f"{c[f'mean_{s}']:.2f}"
                         for s in systems]
                diffs = []
                for x, y in _type_pairs(systems):
                    d, lo, hi = (c[f"{k}_{x}_minus_{y}"] for k in ("diff", "ci_low", "ci_high"))
                    diffs.append(f"{d:+.2f} [{lo:+.2f}, {hi:+.2f}]" + ("*" if lo > 0 or hi < 0 else ""))
                lines.append(f"| {c['group']} (n={c['n']}) | " + " | ".join(means) + " | " + " | ".join(diffs) + " |")
            lines.append("")
    lines += ["### 5b. Does a system's advantage depend on the question type?", "",
              "For each system pair, the mean paired difference in one group of questions vs another, and a "
              f"label-permutation test ({N_PERM:,} shuffles) of whether those two differences differ. "
              "A small p means the advantage is concentrated in one kind of question. Uncorrected.", "",
              "| contrast | metric | x - y | diff in group 1 (n) | diff in group 2 (n) | difference of differences | p |",
              "|---|---|---|---|---|---|---|"]
    for i in typed["interactions"]:
        lines.append(f"| {i['contrast']} | {i['metric']} | {i['system_x'].replace('system_', '')} - "
                     f"{i['system_y'].replace('system_', '')} | {i['diff_group1']:+.2f} ({i['n1']}) | "
                     f"{i['diff_group2']:+.2f} ({i['n2']}) | {i['difference_in_differences']:+.2f} | {i['p']:.4f} |")
    return lines + [""]


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def build_analysis(benchmark: Path = BENCHMARK_PATH, records_path: Path = RECORDS_PATH,
                   out_dir: Path = OUT_DIR) -> str:
    bench, records = load_benchmark(benchmark), load_records(records_path)
    with (out_dir / QUESTION_SCORES_FILE).open(encoding="utf-8") as fh:
        question_rows = list(csv.DictReader(fh))
    systems = [s for s in SYSTEMS if any(r["system"] == s for r in records)]
    scored = score_records(bench, records)
    scored["question_rows"] = question_rows
    budget = {(r["system"], r["question_id"]): r[f"recall@{CHAR_BUDGET}chars"] for r in scored["budget"]}
    for row in question_rows:
        row[BUDGET_METRIC] = budget[(row["system"], row["question_id"])]
    tests = paired_tests(question_rows, systems)
    n_questions = len({r["question_id"] for r in question_rows})
    typed = by_question_type(question_rows, systems)
    text = render_analysis(tests, scored, decoy_false_positives(bench, records), failure_overlap(question_rows, systems),
                           systems, n_questions)
    text += "\n".join(render_by_question_type(typed, systems))
    write_csv(out_dir / TYPE_FILE, typed["cells"])
    write_csv(out_dir / CONTRAST_FILE, typed["interactions"])
    write_csv(out_dir / PAIRED_FILE, tests)
    write_csv(out_dir / AUDIT_FILE, audit_sample(bench, records))
    (out_dir / ANALYSIS_FILE).write_text(text, encoding="utf-8")
    return text


def main() -> None:
    p = argparse.ArgumentParser(description="RQ1 Stage 3: paired tests, budget fairness, matcher validity.")
    p.add_argument("--benchmark", type=Path, default=BENCHMARK_PATH)
    p.add_argument("--records", type=Path, default=RECORDS_PATH)
    p.add_argument("--out", type=Path, default=OUT_DIR)
    args = p.parse_args()
    print(build_analysis(args.benchmark, args.records, args.out))


if __name__ == "__main__":
    main()
