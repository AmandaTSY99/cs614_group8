"""Build a 100-question benchmark QA set grounded in the 10-K.md filings in data/.

The questions are written by a different LLM from the RAG pipeline's answer model (gpt-oss-120b),
to avoid self-preference bias. The prompts follow FinQA / TAT-QA: a table with its surrounding text,
and for numeric questions a FinQA-style `program`. Every QA is checked before it is kept:
  - each gold-evidence quote must appear verbatim in the source it cites
  - numeric programs are executed and must match the stated answer
  - multi-hop questions must cite at least two pieces of evidence (and every source, for cross-section/cross-year)

Each person writes their own file, benchmark/parts/<name>.jsonl, so teammates can share the work through git
without conflicts. Questions made by anyone (every file in benchmark/parts/) are never repeated: their sources
are not reused, and near-duplicate questions are rejected.

Usage (from the repo root; git pull first so teammates' parts are counted):
    python build_benchmark_qa.py --name amanda                          # all recipes; resumes where it stopped
    python build_benchmark_qa.py --name amanda --recipes table,text     # only some recipes (split work by recipe)
    python build_benchmark_qa.py --dry-run                              # print one prompt per recipe, no API calls
    python build_benchmark_qa.py --merge                                # combine all parts into benchmark_qa.jsonl
"""
import argparse
import csv
import getpass
import json
import os
import random
import re
from difflib import SequenceMatcher
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
PARTS_DIR = ROOT / "benchmark" / "parts"                  # one file per person: <name>.jsonl
FINAL_PATH = ROOT / "benchmark" / "benchmark_qa.jsonl"    # all parts merged by --merge
SEED = 614

# Question writer. Must differ from the RAG pipeline's answer model (openai/gpt-oss-120b).
QA_MODEL = os.getenv("QA_MODEL", "qwen/qwen3.8-27b")

# recipe -> (number of QAs, type, scope). Totals: 100 QAs; 45 numeric, 35 qualitative, 20 mixed.
RECIPES = {
    "table":            (25, "numeric",     "single_doc"),  # one table + the paragraph above it
    "text":             (20, "qualitative", "single_doc"),  # one section of narrative text
    "table_text":       (20, "mixed",       "single_doc"),  # a table + a related section from another Item
    "cross_year_table": (20, "numeric",     "cross_year"),  # the same table in two filings of one company
    "cross_year_text":  (15, "qualitative", "cross_year"),  # the same section in two filings of one company
}
CROSS_YEAR_GAP = (3, 6)    # years between the two filings, so the newer one does not already restate the older figures
MAX_WORDS = 900            # cap on a text source shown to the LLM (keeps a call within Groq free-tier 8K tokens/min)
CORE_ITEMS = {"1", "1A", "7", "7A", "8"}   # Business, Risk Factors, MD&A, Market Risk, Financial Statements

ITEM_RE = re.compile(r"^item\s+(\d+[a-c]?)\b[.:]?\s*(.*)$", re.IGNORECASE)
TABLE_SEP_RE = re.compile(r"^\|(\s*:?-{3,}:?\s*\|)+$")
NUMBER_RE = re.compile(r"\d[\d,]*\.?\d*")
STOPWORDS = {"million", "billion", "fiscal", "total", "years", "ended", "which", "their", "these", "other",
             "about", "under", "shares", "including", "compared", "increase", "decrease", "primarily"}


# --- 1. Load and parse filings ---

def load_filings():
    """One dict per 10-K.md filing. Older plain-text 10-K.txt filings are skipped for now."""
    filings = []
    with open(DATA_DIR / "filings_index.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            folder = ROOT / row["local_folder"]
            if (folder / "10-K.md").exists():
                filings.append({"doc_id": f"{row['ticker']}_{folder.name}", "ticker": row["ticker"],
                                "company": row["filer"], "year": int(folder.name[2:6]), "path": folder / "10-K.md"})
    return filings


def parse_blocks(text):
    """Split a 10-K.md into blocks: runs of paragraphs under one heading, and whole tables.
    Each block keeps the Item and heading it sits under, which become its gold-evidence location."""
    blocks, lines = [], []
    kind, item, item_no, heading = "text", "", "", ""

    def flush():
        if lines:
            blocks.append({"item": item, "item_no": item_no, "heading": heading, "kind": kind, "text": "\n".join(lines)})
            lines.clear()

    for raw in text.splitlines():
        line = raw.strip()
        if not line or line == "Table of Contents" or line.isdigit() or TABLE_SEP_RE.match(line):
            continue                                              # blank lines, page furniture, |---| rows
        line_kind = "table" if line.startswith("|") else "text"
        if line_kind != kind:
            flush()
            kind = line_kind
        if kind == "text":
            plain = line.strip("#* ")
            item_match = ITEM_RE.match(plain)
            if item_match and len(plain.split()) <= 20:           # "Item 7. Management's Discussion ..."
                if item_match.group(1).upper() != item_no:        # repeated page headers are ignored
                    flush()
                    item, item_no, heading = plain, item_match.group(1).upper(), ""
                continue
            if line.startswith("#") or (line.startswith("**") and line.endswith("**") and len(line) < 150):
                flush()
                heading = plain
                continue
        lines.append(line)
    flush()
    return blocks


@lru_cache(maxsize=None)
def units(path):
    """Usable sources in one filing: tables (with the paragraph just above them) and text sections."""
    blocks = parse_blocks(Path(path).read_text(encoding="utf-8"))
    tables, texts = [], []
    for i, b in enumerate(blocks):
        n_words = len(b["text"].split())
        if b["item_no"] not in CORE_ITEMS:
            continue
        if b["kind"] == "table":
            rows = b["text"].splitlines()
            n_numbers = len(NUMBER_RE.findall(b["text"]))
            if len(rows) >= 3 and 30 <= n_words <= 700 and n_numbers >= 6 and n_numbers * 6 >= n_words:   # number-dense tables only
                prev = blocks[i - 1] if i and blocks[i - 1]["kind"] == "text" and blocks[i - 1]["heading"] == b["heading"] else None
                context = " ".join(prev["text"].split()[-150:]) if prev else ""
                tables.append({**b, "table": b["text"], "text": f"{context}\n\n{b['text']}".strip()})
        elif n_words >= 120:
            texts.append({**b, "text": " ".join(b["text"].split()[:MAX_WORDS])})
    return tables, texts


# --- 2. Pick sources for each recipe ---

def content_words(text):
    return set(re.findall(r"[a-z]{5,}", text.lower())) - STOPWORDS


def row_labels(table):
    return {row.strip("|").split("|")[0].strip().lower() for row in table.splitlines()} - {""}


def jaccard(a, b):
    return len(a & b) / len(a | b) if a | b else 0.0


def pick_sources(recipe, filings_by_ticker, rng):
    """Return a list of (filing, unit) sources for one QA, or None if this draw has nothing suitable."""
    ticker = rng.choice(sorted(filings_by_ticker))               # balance across companies, not filing counts
    filing = rng.choice(filings_by_ticker[ticker])
    tables, texts = units(filing["path"])

    if recipe == "table":
        return [(filing, rng.choice(tables))] if tables else None
    if recipe == "text":
        return [(filing, rng.choice(texts))] if texts else None
    if recipe == "table_text":                                   # hop across sections: table + related text from another Item
        if not tables:
            return None
        table = rng.choice(tables)
        others = sorted((t for t in texts if t["item_no"] != table["item_no"]),
                        key=lambda t: -len(content_words(t["text"]) & content_words(table["text"])))
        return [(filing, table), (filing, rng.choice(others[:3]))] if others else None

    # Cross-year: the same table / section in an older filing of the same company.
    older = [f for f in filings_by_ticker[ticker] if CROSS_YEAR_GAP[0] <= filing["year"] - f["year"] <= CROSS_YEAR_GAP[1]]
    if not older:
        return None
    old = rng.choice(older)
    old_tables, old_texts = units(old["path"])
    if recipe == "cross_year_table":                             # match tables by their row labels
        pairs = []
        for t in tables:
            best = max(old_tables, key=lambda o: jaccard(row_labels(t["table"]), row_labels(o["table"])), default=None)
            if best and jaccard(row_labels(t["table"]), row_labels(best["table"])) >= 0.5:
                pairs.append((t, best))
    else:                                                        # match sections by Item and heading (digits ignored)
        key = lambda u: (u["item_no"], re.sub(r"\d+", "", u["heading"].lower()))
        old_by_key = {key(o): o for o in old_texts if o["heading"]}
        pairs = [(t, old_by_key[key(t)]) for t in texts if t["heading"] and key(t) in old_by_key]
    if not pairs:
        return None
    new_unit, old_unit = rng.choice(pairs)
    return [(filing, new_unit), (old, old_unit)]


# --- 3. Prompt the question writer ---

SYSTEM_PROMPT = """You write questions for a benchmark that evaluates a RAG system over SEC 10-K filings.
Rules:
- Use ONLY the sources given. Every fact in the answer must be supported by them.
- The question must stand alone: name the company and fiscal year(s), and never refer to "the table", "the passage" or "the source".
- Ask what an analyst or investor would genuinely want to know. Avoid trivia such as page numbers or exhibit lists.
- Each gold_evidence quote must be copied VERBATIM from its source: a complete table row (cells separated by |) for table facts, or one sentence for text facts.
- If the sources cannot support a good question of the requested kind, return {"skip": "<reason>"}.
Return one JSON object and nothing else."""

TYPE_TASKS = {
    "numeric": "Ask a question that needs a calculation over numbers in the sources (e.g. change, % change, ratio, share of total, average).",
    "qualitative": "Ask a non-numeric question, e.g. about strategy, products, customers, competition, risks, drivers of results or regulation. The answer is a short explanation, not a calculation.",
    "mixed": "Ask one question that needs both a figure from the table and an explanation from the text (e.g. how a metric changed and what the company says drove it).",
}
PROGRAM_SPEC = ("`program` uses FinQA syntax: steps add, subtract, multiply, divide, exp, greater, separated by ', '. "
                "A later step can use an earlier result as #0, #1, ... e.g. 'subtract(215938, 130497), divide(#0, 130497)'. "
                "Write numbers plainly (no $, %, or thousands commas). The number in `answer` must equal the program result "
                "(for a percentage, the result x 100), rounded to at most 2 decimals, with units, e.g. '65.47%' or '$85,441 million'.")
KEY_POINTS_SPEC = "`key_points` lists 2-5 short facts that a correct answer must contain."


def build_prompt(recipe, sources, hop):
    qa_type = RECIPES[recipe][1]
    blocks = [f"[S{n}] {f['company']} ({f['ticker']}) 10-K for fiscal year {f['year']} | {u['item']}"
              + (f" > {u['heading']}" if u["heading"] else "") + f"\n{u['text']}"
              for n, (f, u) in enumerate(sources, 1)]
    if len(sources) > 1:
        hop_task = f"Multi-hop: the question must need facts from EVERY source ({', '.join(f'S{n}' for n in range(1, len(sources) + 1))}); quote evidence from each."
    elif hop == "multi":
        hop_task = ("Multi-hop: the question must combine at least two separate facts from DIFFERENT table rows, "
                    "or a table row + a sentence, or different sentences. gold_evidence must have at least 2 entries, one per fact.")
    else:
        hop_task = "Single-hop: the answer should come from a single table row or a single sentence."
    specs = {"numeric": PROGRAM_SPEC, "qualitative": KEY_POINTS_SPEC, "mixed": f"{PROGRAM_SPEC}\n{KEY_POINTS_SPEC}"}[qa_type]
    fmt = {"question": "...", "answer": "...", "gold_evidence": [{"source": "S1", "quote": "..."}]}
    if qa_type != "qualitative":
        fmt["program"] = "..."
    if qa_type != "numeric":
        fmt["key_points"] = ["..."]
    return (f"SOURCES\n\n" + "\n\n".join(blocks) +
            f"\n\nTASK\n{TYPE_TASKS[qa_type]}\n{hop_task}\n{specs}\n\nReturn JSON in this format:\n{json.dumps(fmt)}")


def make_client():
    """Same provider setup as the RAG notebooks: provider from .env, API key from the environment or a prompt."""
    from dotenv import load_dotenv
    load_dotenv()
    provider = os.getenv("LLM_PROVIDER", "groq").strip().lower()
    key_name = "GROQ_API_KEY" if provider == "groq" else "OPENAI_API_KEY"
    if not os.environ.get(key_name):
        os.environ[key_name] = getpass.getpass(f"Enter your {key_name}: ")
    if provider == "groq":
        from groq import Groq
        return Groq(max_retries=5)
    from openai import OpenAI
    return OpenAI(max_retries=5)


def ask(client, prompt):
    """One call to the question writer. Reasoning models (e.g. Qwen3) may think first, so the JSON object is
    taken from the reply after any <think>...</think> block; a reply without one raises JSONDecodeError."""
    response = client.chat.completions.create(
        model=QA_MODEL, temperature=0.7, max_tokens=1000,     # Groq free tier: at most 1K output tokens per minute
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}])
    content = re.sub(r"<think>.*?</think>", "", response.choices[0].message.content or "", flags=re.DOTALL)
    match = re.search(r"\{.*\}", content, re.DOTALL)
    return json.loads(match.group() if match else content)


# --- 4. Validate ---

OPS = {"add": lambda a, b: a + b, "subtract": lambda a, b: a - b, "multiply": lambda a, b: a * b,
       "divide": lambda a, b: a / b, "exp": lambda a, b: a ** b, "greater": lambda a, b: float(a > b)}
OPS.update(sub=OPS["subtract"], mul=OPS["multiply"], div=OPS["divide"])   # common abbreviations from the LLM
SCALE_CONSTANTS = {1.0, 100.0, 1000.0, 1e6}   # program numbers allowed without appearing in the evidence


def run_program(program):
    """Execute a FinQA-style program such as 'subtract(5829, 5735), divide(#0, 5735)'."""
    results = []
    for op, args in re.findall(r"(\w+)\(([^()]*)\)", program):
        values = [results[int(a[1:])] if a.startswith("#") else float(a.replace("const_m", "-").replace("const_", ""))
                  for a in (x.strip() for x in args.split(","))]
        results.append(OPS[op](*values))
    return results[-1]


def normalize(text):
    text = text.translate(str.maketrans("’‘“”–—", "''\"\"--")).replace("|", " ").replace("**", "")
    return re.sub(r"\s+", " ", text).strip().lower()


def validate(qa, recipe, sources, hop):
    """Return the reason a generated QA is rejected, or None if it passes."""
    qa_type = RECIPES[recipe][1]
    if not qa.get("question") or not qa.get("answer"):
        return "missing question/answer"
    evidence = qa.get("gold_evidence") or []
    for ev in evidence:
        n = int(re.sub(r"\D", "", str(ev.get("source", ""))) or 0)
        if not 1 <= n <= len(sources) or normalize(ev.get("quote", "")) not in normalize(sources[n - 1][1]["text"]):
            return f"evidence not found in source: {ev.get('quote', '')[:80]!r}"
    if not evidence or (hop == "multi" and len(evidence) < 2):
        return "not enough evidence"
    if len({ev["source"] for ev in evidence}) < len(sources):
        return "does not use every source"
    if qa_type != "qualitative":
        try:
            result = run_program(qa["program"])
            stated = float(NUMBER_RE.search(str(qa["answer"])).group().replace(",", ""))
        except Exception as e:
            return f"program/answer not executable: {e!r}"
        quoted = {float(n.replace(",", "")) for ev in evidence for n in NUMBER_RE.findall(ev["quote"])}
        for arg in re.findall(r"(?<![#\w.])-?\d[\d,]*\.?\d*", qa["program"]):
            if abs(float(arg.replace(",", ""))) not in quoted | SCALE_CONSTANTS:
                return f"program uses {arg}, which is not in the quoted evidence"
        if not any(abs(abs(result) * k - stated) <= 0.0001 * stated + 0.006 for k in (1, 100)):   # rounding only
            return f"program gives {result:.4f} but answer is {qa['answer']!r}"
    if qa_type != "numeric" and len(qa.get("key_points") or []) < 2:
        return "missing key_points"
    return None


def source_key(filing, unit):
    """Readable id of one source, e.g. 'NVDA_FY2026_2026-01-25 | Item 7 | Fiscal Year 2026 Summary | table'."""
    return f"{filing['doc_id']} | Item {unit['item_no']} | {unit['heading']} | {unit['kind']}"


def is_similar(question, seen, threshold=0.85):
    """Near-duplicate check against every question made so far (by anyone)."""
    return any(SequenceMatcher(None, question.lower(), s).ratio() >= threshold for s in seen)


def read_jsonl(paths):
    return [json.loads(line) for path in paths for line in path.open(encoding="utf-8") if line.strip()]


def to_record(qa_id, qa, recipe, sources, hop, made_by):
    """Final benchmark schema; gold evidence is mapped back to filing, Item and heading."""
    _, qa_type, scope = RECIPES[recipe]
    evidence = []
    for ev in qa["gold_evidence"]:
        filing, unit = sources[int(re.sub(r"\D", "", ev["source"])) - 1]
        in_table = "table" in unit and normalize(ev["quote"]) in normalize(unit["table"])
        evidence.append({"doc_id": filing["doc_id"], "ticker": filing["ticker"], "year": filing["year"],
                         "item": unit["item"], "heading": unit["heading"],
                         "kind": "table" if in_table else "text", "quote": ev["quote"]})
    newest = max(sources, key=lambda s: s[0]["year"])[0]
    return {"id": qa_id, "type": qa_type, "question": qa["question"], "answer": str(qa["answer"]),
            "program": qa.get("program", "") if qa_type != "qualitative" else "",
            "key_points": qa.get("key_points", []) if qa_type != "numeric" else [],
            "gold_evidence": evidence, "company": newest["company"], "ticker": newest["ticker"], "year": newest["year"],
            "scope": scope, "hop": hop, "recipe": recipe,
            "sources": [source_key(f, u) for f, u in sources], "generator": QA_MODEL, "made_by": made_by}


# --- 5. Main loop ---

def merge():
    """Combine every part file into the final benchmark: drop near-duplicates, renumber ids, report counts."""
    merged, seen = [], []
    for r in read_jsonl(sorted(PARTS_DIR.glob("*.jsonl"))):
        if is_similar(r["question"], seen):
            print(f"  dropped near-duplicate from {r['made_by']}: {r['question']}")
            continue
        seen.append(r["question"].lower())
        merged.append(r)
    merged.sort(key=lambda r: list(RECIPES).index(r["recipe"]))
    for n, r in enumerate(merged, 1):
        r["id"] = f"q{n:03d}"
    FINAL_PATH.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in merged), encoding="utf-8")
    for recipe, (target, _, _) in RECIPES.items():
        print(f"{recipe:17} {sum(r['recipe'] == recipe for r in merged):3}/{target}")
    print(f"{len(merged)} QAs saved to {FINAL_PATH}")


def main(name, recipes, dry_run=False):
    rng = random.Random(SEED)
    filings_by_ticker = {}
    for f in load_filings():
        filings_by_ticker.setdefault(f["ticker"], []).append(f)
    print(f"{sum(map(len, filings_by_ticker.values()))} 10-K.md filings, {len(filings_by_ticker)} companies, writer model: {QA_MODEL}")

    if dry_run:
        for recipe in recipes:
            sources = None
            while not sources:
                sources = pick_sources(recipe, filings_by_ticker, rng)
            src, task = build_prompt(recipe, sources, "multi").split("\n\nTASK\n")   # shorten sources only, so TASK always shows
            print(f"\n{'=' * 30} {recipe} {'=' * 30}\n{src[:2500]}{' ...[sources truncated]' if len(src) > 2500 else ''}\n\nTASK\n{task}")
        return

    # Everyone's QAs so far (git pull first to see teammates' parts): counts, questions and sources already used.
    out_path = PARTS_DIR / f"{name}.jsonl"
    records = read_jsonl(sorted(PARTS_DIR.glob("*.jsonl")))
    seen = [r["question"].lower() for r in records]
    used_sources = {key for r in records for key in r["sources"]}
    rng = random.Random(f"{SEED}-{name}-{len(records)}")   # each person and each resumed run draws different sources
    client = make_client()
    PARTS_DIR.mkdir(parents=True, exist_ok=True)
    api_errors = 0                                          # consecutive failures, e.g. the Groq daily limit

    with out_path.open("a", encoding="utf-8") as out:
        for recipe in recipes:
            target = RECIPES[recipe][0]
            made = sum(r["recipe"] == recipe for r in records)
            attempts = draws = 0
            while made < target and attempts < target * 4 and draws < target * 200:
                draws += 1
                sources = pick_sources(recipe, filings_by_ticker, rng)
                if not sources or any(source_key(f, u) in used_sources for f, u in sources):
                    continue                                 # never reuse a table/section, so questions stay varied
                hop = "multi" if len(sources) > 1 or made % 2 else "single"   # single-source recipes alternate hops
                try:
                    qa = ask(client, build_prompt(recipe, sources, hop))
                    api_errors = 0
                except json.JSONDecodeError:
                    qa = {"skip": "response was not valid JSON"}
                except Exception as e:                 # the client already retried rate limits 5 times
                    api_errors += 1
                    print(f"  [{recipe}] API error: {e!r}")
                    if api_errors >= 3:
                        print(f"\nStopping after 3 API errors in a row (see above: e.g. daily limit, or QA_MODEL not available). "
                              f"Your QAs are saved in {out_path}; rerun later to continue.")
                        return
                    continue
                attempts += 1
                reason = qa.get("skip") or validate(qa, recipe, sources, hop)
                if not reason and is_similar(qa["question"], seen):
                    reason = "too similar to an existing question"
                if reason:
                    print(f"  [{recipe}] rejected: {reason}")
                    continue
                n_mine = sum(r["made_by"] == name for r in records) + 1
                record = to_record(f"{name}-{n_mine:03d}", qa, recipe, sources, hop, name)
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                out.flush()
                records.append(record)
                seen.append(qa["question"].lower())
                used_sources.update(record["sources"])
                made += 1
                print(f"{record['id']} [{recipe}/{hop}] {record['ticker']} FY{record['year']}: {record['question']}")
            print(f"{recipe}: {made}/{target} after {attempts} attempts")
    print(f"\nYour QAs are saved in {out_path}. Run with --merge to build {FINAL_PATH.name}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--name", default=getpass.getuser(), help="your name; your QAs go to benchmark/parts/<name>.jsonl")
    parser.add_argument("--recipes", default=",".join(RECIPES), help=f"comma-separated subset of: {', '.join(RECIPES)}")
    parser.add_argument("--dry-run", action="store_true", help="print one prompt per recipe without calling the LLM")
    parser.add_argument("--merge", action="store_true", help="combine benchmark/parts/*.jsonl into the final benchmark")
    args = parser.parse_args()
    if args.merge:
        merge()
    else:
        main(args.name.strip().lower(), [r.strip() for r in args.recipes.split(",")], args.dry_run)
