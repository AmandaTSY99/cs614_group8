"""Text RAG 3, control, ColQwen2.5 visual RAG and System C v3 on 20 benchmark questions (filings from FY2022 onwards).

The FY2022+ cut of the 97-question pool has 21 questions: keep the 5 from results.json, then the lowest ids up to 20.
System C v3 answers are the published ones (reports/rq2/full_v3, gpt-5.4), graded by the same judge. Search is scoped
to the gold filing(s) for the other systems, as in run_benchmark.py. Resumable: finished questions in results_20.jsonl
are skipped and missing page embeddings are created.

Run from the repo root:  .venv/Scripts/python colpali_eval/benchmark/run_benchmark_20.py
"""
import json
import re

import numpy as np
import pypdfium2 as pdfium
import torch
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

from run_benchmark import (BGE_QUERY_PREFIX, COLQWEN, HERE, RAG_SYSTEM, REPO, TEXT_MODEL, TOP_K_CHUNKS, TOP_K_PAGES,
                           VISION_MODEL, VISION_SYSTEM, ColQwen2_5, ColQwen2_5_Processor, ask, evidence_in, image_url,
                           judge, load_chunker, md_path, render_pages)

EVAL_REPO = REPO.parent / "cs614_group8_eval"   # worktree of eval/colpali-v3: pool, published C v3 run, PDFs, embeddings
POOL = EVAL_REPO / "data" / "benchmark_qa_pool_2015.json"
RECORDS = EVAL_REPO / "reports" / "rq2" / "full_v3" / "records.jsonl"
PDFS = EVAL_REPO / "colpali_eval" / "v3" / "pdfs"
EMBS = EVAL_REPO / "colpali_eval" / "v3" / "embs" / "colqwen2_5"
OUT = HERE / "results_20.jsonl"
MIN_YEAR = 2022
N_QUESTIONS = 20
ORIGINAL = {"amanda-013", "amanda-048", "amanda-056", "amanda-090", "amanda-094"}


def select_questions(pool):
    rows = [q for q in pool if all(e["year"] >= MIN_YEAR for e in q["gold_evidence"])]
    original = [q for q in rows if q.get("legacy_id") in ORIGINAL]
    others = [q for q in rows if q.get("legacy_id") not in ORIGINAL]
    return original + others[:N_QUESTIONS - len(original)]


def page_embeddings(model, processor, doc_id):
    """Cached page embeddings for one filing, in the same format as index_filings.py."""
    path = EMBS / f"{doc_id}.pt"
    if path.exists():
        return torch.load(path)
    pages, embs = render_pages(PDFS / f"{doc_id}.pdf"), []
    for start in range(0, len(pages), 4):
        batch = processor.process_images(pages[start:start + 4]).to(model.device)
        with torch.no_grad():
            embs.extend(torch.unbind(model(**batch).to("cpu")))
    torch.save(embs, path)
    print(f"{doc_id}: embedded {len(embs)} pages", flush=True)
    return embs


def first_hits(evidence, ranked_texts):
    """Rank of the first text holding each gold quote, None if no text does."""
    ranks = []
    for e in evidence:
        hits = [n for n, (doc, text) in enumerate(ranked_texts, 1) if doc in (None, e["doc_id"]) and evidence_in(e, text)]
        ranks.append(hits[0] if hits else None)
    return ranks


def main():
    load_dotenv(REPO / ".env")
    client = Groq()
    questions = select_questions(json.loads(POOL.read_text(encoding="utf-8")))
    doc_ids = sorted({e["doc_id"] for q in questions for e in q["gold_evidence"]})
    missing = [d for d in doc_ids if not md_path(d).exists() or not (PDFS / f"{d}.pdf").exists()]
    if len(questions) != N_QUESTIONS or missing:
        raise SystemExit(f"{len(questions)} questions selected; filings missing a .md or PDF: {missing}")
    print(f"{len(questions)} questions over {len(doc_ids)} filings", flush=True)

    records = [json.loads(line) for line in RECORDS.read_text(encoding="utf-8").splitlines() if line.strip()]
    v3 = {r["question_id"]: r for r in records if r["system"] == "system_c_v3"}
    done = {json.loads(line)["id"] for line in OUT.read_text(encoding="utf-8").splitlines()} if OUT.exists() else set()

    chunk_by_structure = load_chunker()
    bge = SentenceTransformer("BAAI/bge-small-en-v1.5")
    model = ColQwen2_5.from_pretrained(COLQWEN, torch_dtype=torch.bfloat16, device_map="cuda").eval()
    processor = ColQwen2_5_Processor.from_pretrained(COLQWEN)

    chunks, chunk_vecs, pages, page_text, page_embs = {}, {}, {}, {}, {}
    for d in doc_ids:
        chunks[d] = [c["text"] for c in chunk_by_structure(md_path(d).read_text(encoding="utf-8"), "md")]
        chunk_vecs[d] = bge.encode(chunks[d], normalize_embeddings=True)
        pdf = pdfium.PdfDocument(str(PDFS / f"{d}.pdf"))
        page_text[d] = [pdf[i].get_textpage().get_text_range() for i in range(len(pdf))]
        pages[d] = render_pages(PDFS / f"{d}.pdf")
        page_embs[d] = page_embeddings(model, processor, d)

    strip = lambda a: re.sub(r"<think>.*?</think>", "", a or "", flags=re.DOTALL).strip()
    for row in questions:
        if row["id"] in done:
            continue
        evidence = row["gold_evidence"]
        docs = sorted({e["doc_id"] for e in evidence})

        q = bge.encode([BGE_QUERY_PREFIX + row["question"]], normalize_embeddings=True)[0]
        ranked_chunks = sorted(((float(chunk_vecs[d][i] @ q), d, i) for d in docs for i in range(len(chunks[d]))), reverse=True)
        with torch.no_grad():
            qv = torch.unbind(model(**processor.process_queries([row["question"]]).to(model.device)).to("cpu"))
        ranked_pages = []
        for d in docs:
            ranked_pages += [(float(s), d, i) for i, s in enumerate(processor.score_multi_vector(qv, page_embs[d])[0])]
        ranked_pages.sort(reverse=True)
        top_pages = ranked_pages[:TOP_K_PAGES]

        context = "\n\n".join(f"[{n}] ({d}) {chunks[d][i]}" for n, (_, d, i) in enumerate(ranked_chunks[:TOP_K_CHUNKS], 1))
        text_messages = [{"role": "system", "content": RAG_SYSTEM},
                         {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {row['question']}"}]
        content = [{"type": "text", "text": f"Pages {', '.join(f'{d} p.{i + 1}' for _, d, i in top_pages)}, in that order.\n\n"
                                            f"Question: {row['question']}"}]
        content += [{"type": "image_url", "image_url": {"url": image_url(pages[d][i])}} for _, d, i in top_pages]
        rec = v3[row["id"]]
        answers = {
            "text": ask(client, model=TEXT_MODEL, temperature=0.0, max_tokens=2048, reasoning_effort="low", messages=text_messages),
            "control": ask(client, model=VISION_MODEL, temperature=0.0, max_tokens=2048, messages=text_messages),
            "visual": ask(client, model=VISION_MODEL, temperature=0.0, max_tokens=2048,
                          messages=[{"role": "system", "content": VISION_SYSTEM}, {"role": "user", "content": content}]),
            "c_v3": rec["answer"],
        }
        result = {"id": row["id"], "legacy_id": row.get("legacy_id"), "type": row["type"], "recipe": row["recipe"],
                  "question": row["question"], "gold": row["answer"], "evidence_kinds": [e["kind"] for e in evidence],
                  "chunk_ranks": first_hits(evidence, [(d, chunks[d][i]) for _, d, i in ranked_chunks]),
                  "page_ranks": first_hits(evidence, [(d, page_text[d][i]) for _, d, i in ranked_pages]),
                  "c_v3_ranks": first_hits(evidence, [(None, t) for t in rec["retrieved_contexts"]]),
                  "c_v3_contexts": len(rec["retrieved_contexts"]),
                  "top_pages": [f"{d} p.{i + 1}" for _, d, i in top_pages]}
        for name, answer in answers.items():
            answer = strip(answer)
            result[f"{name}_answer"] = answer
            result[f"{name}_grade"] = judge(client, row, answer)
        with OUT.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(result) + "\n")
        print(row["id"], row["recipe"], {k: result[f"{k}_grade"]["grade"] for k in answers}, flush=True)


if __name__ == "__main__":
    main()
