"""Text RAG 3 vs ColQwen2.5 visual RAG on benchmark_qa_0.jsonl, filings from FY2025 onwards.

For each question, search is scoped to the gold filing(s), like the ticker + fiscal year filter.
Retrieval: is each gold evidence quote in the context sent to the model?
Answers: graded against the gold answer and key points by an LLM judge (gpt-oss-120b).

Run from the repo root:  .venv/Scripts/python colpali_eval/benchmark/run_benchmark.py
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
import pypdfium2 as pdfium
import torch
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from run_eval import (BGE_QUERY_PREFIX, RAG_SYSTEM, REPO, TEXT_MODEL, VISION_MODEL, VISION_SYSTEM,
                      ask, image_url, load_chunker, render_pages)

from colpali_engine.models import ColQwen2_5, ColQwen2_5_Processor

MIN_YEAR = 2025
TOP_K_CHUNKS, TOP_K_PAGES = 5, 3
COLQWEN = "vidore/colqwen2.5-v0.2"

JUDGE_SYSTEM = (
    "You grade answers to questions about SEC 10-K filings. Compare the candidate answer with the gold answer "
    "and key points. Numbers may be rounded or in different units; small rounding differences are fine. "
    'Reply with JSON only: {"grade": "correct" | "partial" | "wrong", "reason": "<one sentence>"}. '
    "correct = the main figure or claim matches the gold answer; partial = some key points right or the figure "
    "right but key parts missing; wrong = wrong figure, wrong claim, or not answered."
)


def norm(text):
    return re.sub(r"[^a-z0-9.%$()-]+", " ", text.lower()).strip()


def numbers(text):
    return [n.replace(",", "") for n in re.findall(r"\d[\d,]*(?:\.\d+)?", text)]


def evidence_in(evidence, text):
    """Is this gold quote in a chunk or page? Tables: row label words and every number. Text: any 8-word run."""
    hay = norm(text)
    if evidence["kind"] == "table":
        cells = [c.strip() for c in evidence["quote"].strip("|").split("|")]
        label = norm(re.sub(r"\(\d+\)", "", cells[0]))
        hay_numbers = set(numbers(text))
        return label in hay and all(n in hay_numbers for n in numbers(" ".join(cells[1:])))
    words = norm(evidence["quote"]).split()
    windows = [" ".join(words[i:i + 8]) for i in range(max(len(words) - 7, 1))]
    return any(w in hay for w in windows)


def md_path(doc_id):
    ticker, folder = doc_id.split("_", 1)
    return REPO / "data" / ticker / "10-K" / folder / "10-K.md"


def judge(client, row, answer):
    gold = f"Gold answer: {row['answer']}\nKey points: {row['key_points']}"
    reply = ask(client, model=TEXT_MODEL, temperature=0.0, max_tokens=512, reasoning_effort="low",
                messages=[{"role": "system", "content": JUDGE_SYSTEM},
                          {"role": "user", "content": f"Question: {row['question']}\n{gold}\n\nCandidate answer: {answer}"}])
    match = re.search(r"\{.*\}", reply, re.DOTALL)
    return json.loads(match.group(0)) if match else {"grade": "wrong", "reason": f"unparseable judge reply: {reply[:80]}"}


def main():
    load_dotenv(REPO / ".env")
    client = Groq()
    rows = [json.loads(line) for line in (HERE / "benchmark_qa_0.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    rows = [r for r in rows if all(e["year"] >= MIN_YEAR for e in r["gold_evidence"])]
    doc_ids = sorted({e["doc_id"] for r in rows for e in r["gold_evidence"]})
    print(f"{len(rows)} questions over {len(doc_ids)} filings")

    chunk_by_structure = load_chunker()
    bge = SentenceTransformer("BAAI/bge-small-en-v1.5")
    model = ColQwen2_5.from_pretrained(COLQWEN, torch_dtype=torch.bfloat16, device_map="cuda").eval()
    processor = ColQwen2_5_Processor.from_pretrained(COLQWEN)

    chunks, chunk_vecs, pages, page_text, page_embs = {}, {}, {}, {}, {}
    for d in doc_ids:
        chunks[d] = [c["text"] for c in chunk_by_structure(md_path(d).read_text(encoding="utf-8"), "md")]
        chunk_vecs[d] = bge.encode(chunks[d], normalize_embeddings=True)
        pdf = pdfium.PdfDocument(str(HERE / "pdfs" / f"{d}.pdf"))
        page_text[d] = [pdf[i].get_textpage().get_text_range() for i in range(len(pdf))]
        pages[d] = render_pages(HERE / "pdfs" / f"{d}.pdf")
        page_embs[d] = torch.load(HERE / "embs" / f"{d}.pt")

    results = []
    for row in rows:
        docs = sorted({e["doc_id"] for e in row["gold_evidence"]})
        meta = f"{row['ticker']} FY{row['year']} 10-K"

        # Text RAG 3: rank every chunk of the scoped filings
        q = bge.encode([BGE_QUERY_PREFIX + row["question"]], normalize_embeddings=True)[0]
        ranked_chunks = sorted(((float(chunk_vecs[d][i] @ q), d, i) for d in docs for i in range(len(chunks[d]))), reverse=True)
        top_chunks = [chunks[d][i] for _, d, i in ranked_chunks[:TOP_K_CHUNKS]]

        # Visual RAG: rank every page of the scoped filings
        with torch.no_grad():
            qv = torch.unbind(model(**processor.process_queries([row["question"]]).to(model.device)).to("cpu"))
        ranked_pages = []
        for d in docs:
            scores = processor.score_multi_vector(qv, page_embs[d])[0]
            ranked_pages += [(float(s), d, i) for i, s in enumerate(scores)]
        ranked_pages.sort(reverse=True)
        top_pages = ranked_pages[:TOP_K_PAGES]

        def evidence_ranks(ranked, texts):
            out = []
            for e in row["gold_evidence"]:
                hits = [n for n, (_, d, i) in enumerate(ranked, 1) if d == e["doc_id"] and evidence_in(e, texts[d][i])]
                out.append(hits[0] if hits else None)
            return out

        chunk_ranks = evidence_ranks(ranked_chunks, chunks)
        page_ranks = evidence_ranks(ranked_pages, page_text)

        context = "\n\n".join(f"[{n}] ({meta}) {t}" for n, t in enumerate(top_chunks, 1))
        text_messages = [{"role": "system", "content": RAG_SYSTEM},
                         {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {row['question']}"}]
        text_answer = ask(client, model=TEXT_MODEL, temperature=0.0, max_tokens=2048, reasoning_effort="low",
                          messages=text_messages)
        control_answer = ask(client, model=VISION_MODEL, temperature=0.0, max_tokens=2048, messages=text_messages)

        content = [{"type": "text", "text": f"Pages {', '.join(f'{d} p.{i + 1}' for _, d, i in top_pages)}, in that order.\n\n"
                                            f"Question: {row['question']}"}]
        content += [{"type": "image_url", "image_url": {"url": image_url(pages[d][i])}} for _, d, i in top_pages]
        visual_answer = ask(client, model=VISION_MODEL, temperature=0.0, max_tokens=2048,
                            messages=[{"role": "system", "content": VISION_SYSTEM}, {"role": "user", "content": content}])
        strip = lambda a: re.sub(r"<think>.*?</think>", "", a or "", flags=re.DOTALL).strip()

        result = {"id": row["id"], "type": row["type"], "recipe": row["recipe"], "question": row["question"],
                  "gold": row["answer"], "evidence_kinds": [e["kind"] for e in row["gold_evidence"]],
                  "chunk_ranks": chunk_ranks, "page_ranks": page_ranks,
                  "top_pages": [f"{d} p.{i + 1}" for _, d, i in top_pages]}
        for name, answer in (("text", text_answer), ("control", control_answer), ("visual", visual_answer)):
            answer = strip(answer)
            result[f"{name}_answer"] = answer
            result[f"{name}_grade"] = judge(client, row, answer)
        results.append(result)
        print(row["id"], "chunks", chunk_ranks, "pages", page_ranks,
              {k: result[f"{k}_grade"]["grade"] for k in ("text", "control", "visual")}, flush=True)

    (HERE / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
