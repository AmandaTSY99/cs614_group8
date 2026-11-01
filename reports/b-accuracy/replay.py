"""Replay saved retrieval results. Gold labels are used only after an answer is returned."""
import sys,json,time,hashlib,os,statistics,re,subprocess
from collections import defaultdict
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq,RateLimitError
sys.path.insert(0,str(Path.cwd()))
from src.system_b.pipeline import run
from src.system_b.retrieval import diversify_tail
from src.system_a.pipeline import RAG_SYSTEM
from src.system_a.evaluate import keypoint_recall
from scripts.rq2.metrics_custom import numeric_accuracy
load_dotenv()
model="openai/gpt-oss-120b"
client=Groq(max_retries=0)
out=Path("reports/b-accuracy")
def read(p):
    return [json.loads(x) for x in Path(p).read_text(encoding="utf8").splitlines() if x.strip()]
def score(r,a):
    if r["type"]=="numeric": return numeric_accuracy(a,r["ground_truth_numbers"])
    return keypoint_recall(qs[r["question_id"]]["key_points"],a)
qs={q["id"]:q for q in json.loads(Path("data/benchmark_qa_pool_2015.json").read_text(encoding="utf8"))}
records={(r["system"],r["question_id"]):r for r in read("reports/rq2/full_v3/records.jsonl")}
def call(msgs):
    attempt=0
    while True:
        try:
            response=client.chat.completions.create(model=model,messages=msgs,temperature=0,max_completion_tokens=1024,reasoning_effort="low")
            ans=response.choices[0].message.content
            if not ans: raise RuntimeError("Empty response")
            return {"answer":ans,"usage":response.usage.model_dump()}
        except RateLimitError as exc:
            message=str(exc).lower()
            if "tokens per day" in message:
                delay=re.search(r"try again in ([0-9.hms]+)",message)
                seconds=sum(float(n)*{"h":3600,"m":60,"s":1}[unit] for n,unit in re.findall(r"([0-9.]+)([hms])",delay.group(1))) if delay else 900
                seconds=max(60,int(seconds)+5)
                print(f"Daily quota reached. Retrying the pending answer in {seconds}s.",flush=True)
                time.sleep(seconds)
                continue
            attempt+=1
            if attempt>=12: raise
            time.sleep(max(8,float(exc.response.headers.get("retry-after",20)))+2)
class Saved:
    def __init__(self,hits): self.hits=hits
    def retrieve(self,query,scope): return {"hits":self.hits,"timings":{}}
rows=read(out/"answers.jsonl") if (out/"answers.jsonl").exists() else []
done={(r["arm"],r["id"]) for r in rows}
ids=sorted(qs,key=lambda k:hashlib.sha256(("system-b-v2-evaluation:"+k).encode()).digest())
for i,k in enumerate(ids):
    if all((arm,k) in done for arm in ("A","B")): continue
    for arm in ("B","A"):
        if (arm,k) in done: continue
        r=records["system_"+arm.lower(),k]
        hits=[{"id":m["chunk_id"],"text":t,"meta":m} for t,m in zip(r["retrieved_contexts"],r["contexts_meta"],strict=True)]
        if arm=="B":
            dense=records["system_a",k]
            extra=[{"id":m["chunk_id"],"text":t,"meta":m} for t,m in zip(dense["retrieved_contexts"],dense["contexts_meta"],strict=True)]
            result=run(Saved(diversify_tail(hits,extra,10)),r["question"],generator=call)
        else:
            context="\n\n".join(f"[{j}] ({h['meta']['ticker']} FY{h['meta']['fiscal_year']} 10-K) {h['text']}" for j,h in enumerate(hits,1))
            result=call([{"role":"system","content":RAG_SYSTEM},{"role":"user","content":f"Context:\n{context}\n\nQuestion: {r['question']}"}])
        entry={"id":k,"arm":arm,"answer":result["answer"],"score":score(r,result["answer"]),"tokens":result["usage"]["total_tokens"],"model":model}
        with (out/"answers.jsonl").open("a",encoding="utf8") as f: print(json.dumps(entry),file=f)
        rows.append(entry)
    subprocess.run([sys.executable,str(out/"summarize.py")],check=True,stdout=subprocess.DEVNULL)
    print(f"{i+1}/97",flush=True)
