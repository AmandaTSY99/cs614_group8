"""ColPali v1.3 visual RAG on the 5 FY2025+ benchmark questions, for comparison with results_v3.json.

Same pipeline as the visual run in run_benchmark.py: search scoped to the gold filing, top 3 pages, qwen3.8-27b reads
the images, same judge and evidence matcher. Only the retriever changes. Writes results_colpali_v13.json. Page embeddings
are cached in embs_colpali_v13/.

Run from the repo root:  .venv/Scripts/python colpali_eval/benchmark/add_colpali_v13.py
"""
import json
import re

import pypdfium2 as pdfium
import torch
from colpali_engine.models import ColPali, ColPaliProcessor
from dotenv import load_dotenv
from groq import Groq

from run_benchmark import (HERE, MIN_YEAR, REPO, TOP_K_PAGES, VISION_MODEL, VISION_SYSTEM, ask, evidence_in, image_url,
                           judge, render_pages)

COLPALI = "vidore/colpali-v1.3"
EMBS = HERE / "embs_colpali_v13"
OUT = HERE / "results_colpali_v13.json"


def page_embeddings(model, processor, doc_id, pages):
    path = EMBS / f"{doc_id}.pt"
    if path.exists():
        return torch.load(path)
    embs = []
    for start in range(0, len(pages), 4):
        batch = processor.process_images(pages[start:start + 4]).to(model.device)
        with torch.no_grad():
            embs.extend(torch.unbind(model(**batch).to("cpu")))
    torch.save(embs, path)
    print(f"{doc_id}: embedded {len(embs)} pages", flush=True)
    return embs


def main():
    load_dotenv(REPO / ".env")
    client = Groq()
    rows = [json.loads(line) for line in (HERE / "benchmark_qa_0.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    rows = [r for r in rows if all(e["year"] >= MIN_YEAR for e in r["gold_evidence"])]
    doc_ids = sorted({e["doc_id"] for r in rows for e in r["gold_evidence"]})
    print(f"{len(rows)} questions over {len(doc_ids)} filings", flush=True)

    EMBS.mkdir(exist_ok=True)
    model = ColPali.from_pretrained(COLPALI, torch_dtype=torch.bfloat16, device_map="cuda").eval()
    processor = ColPaliProcessor.from_pretrained(COLPALI)

    pages, page_text, page_embs = {}, {}, {}
    for d in doc_ids:
        pdf = pdfium.PdfDocument(str(HERE / "pdfs" / f"{d}.pdf"))
        page_text[d] = [pdf[i].get_textpage().get_text_range() for i in range(len(pdf))]
        pages[d] = render_pages(HERE / "pdfs" / f"{d}.pdf")
        page_embs[d] = page_embeddings(model, processor, d, pages[d])

    results = []
    for row in rows:
        docs = sorted({e["doc_id"] for e in row["gold_evidence"]})
        with torch.no_grad():
            qv = torch.unbind(model(**processor.process_queries([row["question"]]).to(model.device)).to("cpu"))
        ranked_pages = []
        for d in docs:
            scores = processor.score_multi_vector(qv, page_embs[d])[0]
            ranked_pages += [(float(s), d, i) for i, s in enumerate(scores)]
        ranked_pages.sort(reverse=True)
        top_pages = ranked_pages[:TOP_K_PAGES]

        page_ranks = []
        for e in row["gold_evidence"]:
            hits = [n for n, (_, d, i) in enumerate(ranked_pages, 1) if d == e["doc_id"] and evidence_in(e, page_text[d][i])]
            page_ranks.append(hits[0] if hits else None)

        content = [{"type": "text", "text": f"Pages {', '.join(f'{d} p.{i + 1}' for _, d, i in top_pages)}, in that order.\n\n"
                                            f"Question: {row['question']}"}]
        content += [{"type": "image_url", "image_url": {"url": image_url(pages[d][i])}} for _, d, i in top_pages]
        answer = ask(client, model=VISION_MODEL, temperature=0.0, max_tokens=2048,
                     messages=[{"role": "system", "content": VISION_SYSTEM}, {"role": "user", "content": content}])
        answer = re.sub(r"<think>.*?</think>", "", answer or "", flags=re.DOTALL).strip()
        grade = judge(client, row, answer)

        results.append({"id": row["id"], "type": row["type"], "recipe": row["recipe"], "question": row["question"],
                        "gold": row["answer"], "evidence_kinds": [e["kind"] for e in row["gold_evidence"]],
                        "page_ranks": page_ranks, "total_pages": sum(len(page_embs[d]) for d in docs),
                        "top_pages": [f"{d} p.{i + 1}" for _, d, i in top_pages],
                        "colpali_answer": answer, "colpali_grade": grade})
        print(row["id"], "pages", page_ranks, grade["grade"], flush=True)
        OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
