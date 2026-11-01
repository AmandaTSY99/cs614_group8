import json,random,statistics
from pathlib import Path
from collections import Counter
p=Path(__file__).parent
def read(path): return [json.loads(s) for s in path.read_text(encoding="utf8").splitlines() if s]
rows=read(p/"answers.jsonl")
arms={a:{r["id"]:r for r in rows if r["arm"]==a} for a in ("A","B")}
assert sum(map(len,arms.values()))==len(rows)
ids=sorted(arms["A"].keys() & arms["B"].keys())
assert ids and all(arms[a][k]["score"] is not None for k in ids for a in arms)
scores={a:statistics.mean(arms[a][k]["score"] for k in ids) for a in arms}
diff=[arms["B"][k]["score"]-arms["A"][k]["score"] for k in ids]
rng=random.Random(614)
boot=sorted(statistics.mean(rng.choices(diff,k=len(diff))) for _ in range(5000))
q=read(Path("reports/rq2/full_v3/records.jsonl"))
types={r["question_id"]:r["type"] for r in q}
matrix=Counter((a,types[k]) for a in arms for k in ids)
s={"paired_questions":len(ids),"expected":97,"model":rows[0]["model"],"primary_accuracy":scores,"paired_difference":statistics.mean(diff),"paired_bootstrap95":[boot[124],boot[4874]],"wins_ties_losses":[sum(d>0 for d in diff),sum(d==0 for d in diff),sum(d<0 for d in diff)],"mean_tokens":{a:statistics.mean(arms[a][k]["tokens"] for k in ids) for a in arms},"question_types":dict(Counter(types[k] for k in ids)),"ids":ids}
def save(name,text):
    temp=p/(name+".tmp")
    temp.write_text(text,encoding="utf8")
    temp.replace(p/name)
save("paired_summary.json",json.dumps(s,indent=2))
save("README.md",f"""# System B accuracy comparison

**{len(ids)}/97 paired questions scored** with Groq GPT-OSS-120B at temperature zero. The question order was fixed by hashing IDs before the run. The team score uses numerical matching for numeric questions and key-point recall for qualitative and mixed questions. Both arms receive the same question and generation settings. Reference answers, expected figures and key points are used only in scoring.

| Measure | Original A | Revised B |
|---|---:|---:|
| Mean primary accuracy | {scores["A"]:.1%} | {scores["B"]:.1%} |
| Mean reported tokens per answer | {s["mean_tokens"]["A"]:.0f} | {s["mean_tokens"]["B"]:.0f} |

B scored higher on {s["wins_ties_losses"][0]} questions, tied on {s["wins_ties_losses"][1]} and scored lower on {s["wins_ties_losses"][2]}. The observed difference is {s["paired_difference"]*100:.1f} percentage points. This is a matched replay of a previously inspected benchmark.

## Method

A uses its original prompt and stored dense passages. B keeps its five stored cross-encoder selections and fills remaining slots from the stored dense list, up to ten distinct passages. Its prompt requests supported partial answers and calculations with units and cited inputs. This replay uses the archived A dense list as a proxy for B’s live dense ordering. One independent live adapter smoke test verified retrieval of ten distinct passages. The comparison tests the combination of retrieval and prompt changes.

Across all 97 questions, the offline evidence test found all required evidence for 55 with A, 60 with original B and 70 with the candidate. The original shared GPT-5.4 run remains separate from this Groq experiment. See [paired scores](paired_summary.json) for the included question IDs.
""")
print(json.dumps({k:v for k,v in s.items() if k!="ids"}))
