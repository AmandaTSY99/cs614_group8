"""Benchmark evaluation: retrieval metrics against gold_evidence, and answer scores against the gold answer.

Retrieval (per QA, top-k hits):
  hit              at least one gold evidence quote is in a retrieved chunk
  evidence_recall  share of gold evidence quotes found in the retrieved chunks
  doc_recall       share of gold filings (doc_id) that any retrieved chunk comes from
  mrr              1 / rank of the first chunk holding gold evidence (0 if none)
Answers:
  numeric_correct  numeric/mixed QAs: a number in the answer matches the gold number (rounding and
                   million/billion scale allowed, sign ignored)
  keypoint_recall  qualitative/mixed QAs: share of key points whose content words mostly appear in the answer
Both answer scores are simple string checks, a rough guide rather than a judge; read the answers in the
results file for the final call. They avoid an LLM judge from the same family as the RAG model.
"""
import json
import re
import time
from pathlib import Path

import pandas as pd

from .pipeline import generate

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BENCHMARK = [ROOT / "benchmark" / "benchmark_qa.jsonl"]   # amanda.jsonl with the reviewed corrections applied
NUMBER_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")
SCALES = (1, 100, 0.01, 1e3, 1e-3, 1e6, 1e-6, 1e9, 1e-9)     # e.g. "$3.19 billion" vs "$3,192,049 thousand"
STOPWORDS = {"the", "and", "for", "with", "that", "this", "from", "its", "was", "were", "are", "has", "have",
             "had", "which", "their", "than", "into", "over", "also", "such", "as", "of", "to", "in", "on", "by"}
METRICS = ["hit", "evidence_recall", "doc_recall", "mrr", "numeric_correct", "keypoint_recall"]


def load_benchmark(paths=None):
    """QAs from .jsonl files (or a .json list). A QA in a later file replaces one with the same id."""
    qas = {}
    for path in map(Path, paths or DEFAULT_BENCHMARK):
        text = path.read_text(encoding="utf-8")
        records = json.loads(text) if path.suffix == ".json" else [json.loads(l) for l in text.splitlines() if l.strip()]
        qas.update((r["id"], r) for r in records)
    return list(qas.values())


def gold_pairs(qa):
    """(ticker, fiscal_year) of every gold filing: the filters a user would give for this question."""
    return list(dict.fromkeys((e["ticker"], e["year"]) for e in qa["gold_evidence"]))


# --- Retrieval ---------------------------------------------------------------------------------

def normalize(text):
    return " ".join(re.sub(r"[*_`]", "", text).lower().split())


def words(text):
    return set(re.findall(r"\w+", text.lower()))


def evidence_in_hit(evidence, hit, min_overlap=0.8):
    """Exact quote in the chunk, or (for longer quotes split across two chunks) most of its words."""
    if hit["meta"].get("doc_id") != evidence["doc_id"]:
        return False
    quote, text = normalize(evidence["quote"]), normalize(hit["text"])
    if quote in text:
        return True
    quote_words = words(quote)
    return len(quote_words) >= 15 and len(quote_words & words(text)) >= min_overlap * len(quote_words)


def score_retrieval(qa, hits):
    evidence = qa["gold_evidence"]
    ranks = [next((rank for rank, h in enumerate(hits, 1) if evidence_in_hit(e, h)), None) for e in evidence]
    first = min((r for r in ranks if r), default=None)
    gold_docs = {e["doc_id"] for e in evidence}
    return {"hit": first is not None,
            "evidence_recall": sum(r is not None for r in ranks) / len(evidence),
            "doc_recall": len(gold_docs & {h["meta"].get("doc_id") for h in hits}) / len(gold_docs),
            "mrr": 1 / first if first else 0.0}


# --- Answers -----------------------------------------------------------------------------------

def numbers(text):
    return [float(n.replace(",", "")) for n in NUMBER_RE.findall(text or "")]


def numeric_correct(gold, prediction, tol=0.01):
    """Any number in the prediction within `tol` (relative) of the gold number, at any scale in SCALES."""
    gold_numbers = numbers(gold)
    if not gold_numbers:
        return None
    target = gold_numbers[0]
    return any(abs(p * s - target) <= tol * target + 1e-9 for p in numbers(prediction) for s in SCALES)


def keypoint_recall(key_points, prediction, min_overlap=0.5):
    if not key_points:
        return None
    answer_words = words(prediction or "")
    covered = 0
    for point in key_points:
        content = {w for w in words(point) if len(w) > 2 and w not in STOPWORDS}
        covered += bool(content) and len(content & answer_words) >= min_overlap * len(content)
    return covered / len(key_points)


def score_answer(qa, prediction, tol=0.01):
    if not prediction or prediction.startswith("Not found in the provided context"):
        prediction = ""
    numeric = numeric_correct(qa["answer"], prediction, tol) if qa["type"] in ("numeric", "mixed") else None
    return {"numeric_correct": numeric,
            "keypoint_recall": keypoint_recall(qa.get("key_points"), prediction) if qa["type"] != "numeric" else None}


# --- Run ---------------------------------------------------------------------------------------

def run_benchmark(index, qas, variants=("rag3",), k=5, scope="gold", generate_answers=True,
                  model=None, out_path=None, tol=0.01, sleep=0.0, max_errors=3):
    """Run every QA through each variant, write one JSON line per (QA, variant) and return them as a DataFrame.
    scope="gold" filters retrieval to the QA's gold companies and years; "none" searches the whole corpus."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rows, errors = [], 0
    with out_path.open("w", encoding="utf-8") as f:
        for n, qa in enumerate(qas, 1):
            pairs = gold_pairs(qa) if scope == "gold" else []
            hits = index.retrieve(qa["question"], k, pairs)          # RAG 3 and 4 retrieve the same way
            retrieval = score_retrieval(qa, hits)
            for variant in variants:
                row = {"id": qa["id"], "variant": variant, "recipe": qa.get("recipe"), "hop": qa.get("hop"),
                       "type": qa["type"], "scope": scope, "question": qa["question"],
                       "gold_answer": qa["answer"], "prediction": None, **retrieval,
                       "numeric_correct": None, "keypoint_recall": None,
                       "retrieved": [h["id"] for h in hits]}
                if generate_answers:
                    try:
                        out = generate(qa["question"], hits, variant, pairs, **({"model": model} if model else {}))
                        row.update(prediction=out["answer"], **score_answer(qa, out["answer"], tol))
                        errors = 0
                    except Exception as e:                         # e.g. daily rate limit; keep what is done so far
                        row["error"] = str(e)
                        errors += 1
                        print(f"  {qa['id']} {variant}: {e}")
                    time.sleep(sleep)
                rows.append(row)
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
                f.flush()
            print(f"[{n}/{len(qas)}] {qa['id']}  hit={retrieval['hit']}  evidence_recall={retrieval['evidence_recall']:.2f}")
            if errors >= max_errors:
                print(f"Stopped after {max_errors} API errors in a row (see above: e.g. daily limit). "
                      f"Results so far are in {out_path}")
                break
    return pd.DataFrame(rows)


def summarize(df):
    """Mean of each metric per variant, overall and by recipe. Answer scores skip QAs they don't apply to."""
    df = df.copy()
    for col in METRICS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    overall = df.groupby("variant")[METRICS].mean().round(3)
    overall.insert(0, "n", df.groupby("variant").size())
    by_recipe = df.groupby(["variant", "recipe"])[METRICS].mean().round(3)
    return overall, by_recipe
