"""RQ3 accuracy funnel (97 -> answers containing a number) and single-hop vs multi-hop split per system.

Reads reports/rq3/records.jsonl; writes reports/rq3/hop_split.json and reports/rq3/hop_split.md.

Definitions
- Scored set: questions whose gold answer contains a number (`numeric_correct` is not None). This is a
  property of the gold answer, not the benchmark `type` label, so it includes some qualitative questions
  whose gold text mentions a year or figure.
- Typed numeric set: the scored questions the benchmark labels `numeric` or `mixed` (robustness check).
- Hop: the benchmark's own `hop` field (single / multi), copied unchanged into every record.
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RQ3 = ROOT / "reports" / "rq3"
SYSTEMS = ["system_a", "system_b", "system_c_v1", "system_c_v2", "system_c_v3"]
LABELS = {"system_a": "A", "system_b": "B", "system_c_v1": "C v1", "system_c_v2": "C v2", "system_c_v3": "C v3"}


def cell(rows):
    vals = [r["numeric_correct"] for r in rows]
    n, c = len(vals), sum(bool(v) for v in vals)
    return {"correct": c, "n": n, "pct": round(100 * c / n, 1) if n else None}


def main():
    recs = [json.loads(l) for l in open(RQ3 / "records.jsonl") if l.strip()]
    ref = sorted((r for r in recs if r["system"] == "system_a"), key=lambda r: r["question_id"])
    scored = [r for r in ref if r["numeric_correct"] is not None]
    typed = [r for r in scored if r["type"] in ("numeric", "mixed")]
    funnel = {
        "benchmark": {"n": len(ref), "hop": dict(Counter(r["hop"] for r in ref))},
        "answer_contains_number": {"n": len(scored), "hop": dict(Counter(r["hop"] for r in scored)),
                                   "type": dict(Counter(r["type"] for r in scored))},
        "excluded_no_number": sorted(r["question_id"] for r in ref if r["numeric_correct"] is None),
        "typed_numeric_or_mixed": {"n": len(typed), "hop": dict(Counter(r["hop"] for r in typed))},
    }

    out = {"funnel": funnel, "systems": {}}
    for s in SYSTEMS:
        rows = [r for r in recs if r["system"] == s and r["numeric_correct"] is not None]
        if not rows:
            continue
        res = {}
        for name, subset in [("scored", rows), ("typed", [r for r in rows if r["type"] in ("numeric", "mixed")])]:
            res[name] = {"all": cell(subset),
                         "single": cell([r for r in subset if r["hop"] == "single"]),
                         "multi": cell([r for r in subset if r["hop"] == "multi"])}
        hops = {h: [r for r in rows if r["hop"] == h] for h in ("single", "multi")}
        res["mean_agent_hops"] = {h: round(sum(r["hops"] for r in v) / len(v), 2) for h, v in hops.items()}
        res["p50_latency_s"] = {h: round(sorted(r["latency_ms"] for r in v)[len(v) // 2] / 1000, 1) for h, v in hops.items()}
        out["systems"][s] = res
    (RQ3 / "hop_split.json").write_text(json.dumps(out, indent=2))

    f = funnel
    md = ["# RQ3: accuracy on answers containing a number, by hop", "",
          f"Funnel: {f['benchmark']['n']} benchmark questions -> {f['answer_contains_number']['n']} whose gold answer "
          f"contains a number ({f['answer_contains_number']['hop'].get('multi', 0)} multi-hop, "
          f"{f['answer_contains_number']['hop'].get('single', 0)} single-hop). "
          f"Of these, {f['typed_numeric_or_mixed']['n']} are labelled numeric or mixed in the benchmark.", "",
          "| System | All | Single-hop | Multi-hop | Single -> multi | Typed numeric/mixed (all / single / multi) | Mean hops (single / multi) | p50 latency s (single / multi) |",
          "|---|---|---|---|---|---|---|---|"]
    for s, res in out["systems"].items():
        a, t = res["scored"], res["typed"]
        drop = round(a["multi"]["pct"] - a["single"]["pct"], 1)
        fmt = lambda c: f"{c['pct']}% ({c['correct']}/{c['n']})"
        md.append(f"| {LABELS[s]} | {fmt(a['all'])} | {fmt(a['single'])} | {fmt(a['multi'])} | {drop:+} pp | "
                  f"{t['all']['pct']}% / {t['single']['pct']}% / {t['multi']['pct']}% | "
                  f"{res['mean_agent_hops']['single']} / {res['mean_agent_hops']['multi']} | "
                  f"{res['p50_latency_s']['single']} / {res['p50_latency_s']['multi']} |")
    (RQ3 / "hop_split.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
