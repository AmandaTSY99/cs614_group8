"""Add System C v3 to the FY2025+ benchmark, using its published answers (reports/rq2/full_v3, answer model gpt-5.4).

Answers are not regenerated. They are graded by the same judge as results.json, and evidence ranks use the same
matcher over C v3's retrieved contexts. Writes results_v3.json; results.json is left as is.

Run from the repo root:  .venv/Scripts/python colpali_eval/benchmark/add_system_c_v3.py
"""
import json

from dotenv import load_dotenv
from groq import Groq

from run_benchmark import HERE, REPO, evidence_in, judge

EVAL_REPO = REPO.parent / "cs614_group8_eval"   # worktree of eval/colpali-v3, which holds the published C v3 run
POOL = EVAL_REPO / "data" / "benchmark_qa_pool_2015.json"
RECORDS = EVAL_REPO / "reports" / "rq2" / "full_v3" / "records.jsonl"


def main():
    load_dotenv(REPO / ".env")
    client = Groq()
    rows = {r["id"]: r for r in map(json.loads, (HERE / "benchmark_qa_0.jsonl").read_text(encoding="utf-8").splitlines()) if r}
    gold_ids = {p["legacy_id"]: p["id"] for p in json.loads(POOL.read_text(encoding="utf-8"))}
    records = [json.loads(line) for line in RECORDS.read_text(encoding="utf-8").splitlines() if line.strip()]
    v3 = {r["question_id"]: r for r in records if r["system"] == "system_c_v3"}

    results = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    for result in results:
        row, rec = rows[result["id"]], v3[gold_ids[result["id"]]]
        ranks = []
        for e in row["gold_evidence"]:
            hits = [n for n, text in enumerate(rec["retrieved_contexts"], 1) if evidence_in(e, text)]
            ranks.append(hits[0] if hits else None)
        result["c_v3_ranks"] = ranks
        result["c_v3_contexts"] = len(rec["retrieved_contexts"])
        result["c_v3_answer"] = rec["answer"]
        result["c_v3_grade"] = judge(client, row, rec["answer"])
        print(result["id"], "evidence ranks", ranks, "of", result["c_v3_contexts"], "contexts |",
              "c_v3", result["c_v3_grade"]["grade"], "| visual", result["visual_grade"]["grade"],
              "| text", result["text_grade"]["grade"], flush=True)

    (HERE / "results_v3.json").write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
