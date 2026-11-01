import json,sys,statistics
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from scripts.rq1.evaluate_rq1 import evidence_in_contexts
from scripts.rq2.metrics_custom import numeric_accuracy
from src.system_b.retrieval import diversify_tail
p=Path("reports/b-accuracy")
rs={(r["system"],r["question_id"]):r for r in map(json.loads,Path("reports/rq2/full_v3/records.jsonl").read_text(encoding="utf8").splitlines())}
qs=json.loads(Path("data/benchmark_qa_pool_2015.json").read_text(encoding="utf8"))
def hits(r):
    return [dict(id=m["chunk_id"],text=t,meta=m) for m,t in zip(r["contexts_meta"],r["retrieved_contexts"],strict=True)]
counts={arm:0 for arm in ["A","original B","candidate B"]}
scores={arm:[] for arm in ["A","original B"]}
npass=[]
for q in qs:
    a,b=[rs[s,q["id"]] for s in ["system_a","system_b"]]
    mixed=diversify_tail(hits(b),hits(a),10)
    assert [x["id"] for x in mixed[:len(b["contexts_meta"])]]==[m["chunk_id"] for m in b["contexts_meta"]]
    npass.append(len(mixed))
    for arm,hh in [("A",hits(a)),("original B",hits(b)),("candidate B",mixed)]:
        counts[arm]+=all(evidence_in_contexts(e,[h["text"] for h in hh]) for e in q["gold_evidence"])
    for arm,r in [("A",a),("original B",b)]:
        scores[arm].append(numeric_accuracy(r["answer"],r["ground_truth_numbers"]) if r["type"]=="numeric" else r["keypoint_recall"])
print(counts, {k:statistics.mean(v) for k,v in scores.items()},'mean context count',statistics.mean(npass))
