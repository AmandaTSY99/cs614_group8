"""Pick a handful of obvious showcase cases for the report and slides from reports/rq3/records.jsonl.

Each pattern is a pass/fail rule on `numeric_correct`. To keep the examples unambiguous, only questions the
benchmark labels `numeric` or `mixed` are eligible (a qualitative question can be scored correct just by
repeating a year). Ranking within a pattern is fixed, not hand-picked: numeric before mixed, then shorter
question, then question id. The top pick and two alternates are written to reports/case_studies/showcase.md.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RECORDS = ROOT / "reports" / "rq3" / "records.jsonl"
OUT = ROOT / "reports" / "case_studies" / "showcase.md"
SYSTEMS = ["system_a", "system_b", "system_c_v1", "system_c_v2", "system_c_v3"]
LABELS = {"system_a": "A", "system_b": "B", "system_c_v1": "C v1", "system_c_v2": "C v2", "system_c_v3": "C v3"}

# pattern name -> required outcome per system (True pass, False fail, absent = either)
PATTERNS = [
    ("1. Every system passes", {s: True for s in SYSTEMS}),
    ("2. B and C pass, A fails", {"system_a": False, "system_b": True, "system_c_v1": True, "system_c_v3": True}),
    ("3. A and B fail, C passes", {"system_a": False, "system_b": False, "system_c_v1": True, "system_c_v3": True}),
    ("4. A, B, C v1 and C v2 fail, only C v3 passes",
     {"system_a": False, "system_b": False, "system_c_v1": False, "system_c_v2": False, "system_c_v3": True}),
    ("5. C v1 passes, C v2 fails (C v3 recovers)", {"system_c_v1": True, "system_c_v2": False, "system_c_v3": True}),
]


def clip(text, n=220):
    text = " ".join(str(text or "").split())
    return text if len(text) <= n else text[: n - 1] + "…"


def main():
    recs = [json.loads(l) for l in open(RECORDS) if l.strip()]
    by_q = {}
    for r in recs:
        by_q.setdefault(r["question_id"], {})[r["system"]] = r
    eligible = {q: d for q, d in by_q.items()
                if all(s in d for s in SYSTEMS)
                and d["system_a"]["type"] in ("numeric", "mixed")
                and all(d[s]["numeric_correct"] is not None for s in SYSTEMS)}

    md = ["# Showcase cases", "",
          "Selected by `scripts/case_studies/select_showcase.py` from `reports/rq3/records.jsonl` using fixed pass/fail "
          "rules on numeric correctness (numeric/mixed questions only; numeric first, then shorter question, then id). "
          "Read the full page in `cases/` before using a case: the check is a string match.", ""]
    for name, rule in PATTERNS:
        hits = [q for q, d in eligible.items() if all(bool(d[s]["numeric_correct"]) == want for s, want in rule.items())]
        hits.sort(key=lambda q: (eligible[q]["system_a"]["type"] != "numeric", len(eligible[q]["system_a"]["question"]), q))
        md += [f"## {name}", "", f"{len(hits)} eligible question(s)."]
        if not hits:
            md += ["", "No question matches this pattern.", ""]
            continue
        q = hits[0]
        d = eligible[q]
        a = d["system_a"]
        md += ["", f"**Pick: [{q}](cases/{q}.md)** ({a['type']}, {a['hop']}-hop, recipe `{a['recipe']}`)", "",
               f"> {clip(a['question'], 400)}", "", f"Gold answer: {clip(a['ground_truth_answer'], 300)}", "",
               "| System | Correct | Hops | Latency s | Answer (start) |", "|---|---|---|---|---|"]
        for s in SYSTEMS:
            r = d[s]
            md.append(f"| {LABELS[s]} | {'yes' if r['numeric_correct'] else 'no'} | {r['hops']} | "
                      f"{r['latency_ms'] / 1000:.1f} | {clip(r['answer']).replace('|', '/')} |")
        if len(hits) > 1:
            md += ["", "Alternates: " + ", ".join(f"[{x}](cases/{x}.md)" for x in hits[1:3])]
        md.append("")
    OUT.write_text("\n".join(md))
    print(OUT.relative_to(ROOT))
    for name, _ in PATTERNS:
        print(name)


if __name__ == "__main__":
    main()
