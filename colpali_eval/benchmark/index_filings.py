"""Print every gold filing in benchmark_qa_0.jsonl to PDF and cache its ColQwen2.5 page embeddings.

Resumable: filings that already have a PDF or an embedding file are skipped.
"""
import json
import subprocess
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from run_eval import REPO, render_pages

from colpali_engine.models import ColQwen2_5, ColQwen2_5_Processor

HERE = Path(__file__).resolve().parent
PDFS, EMBS = HERE / "pdfs", HERE / "embs"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
MODEL_NAME = "vidore/colqwen2.5-v0.2"


def doc_folder(doc_id):
    ticker, folder = doc_id.split("_", 1)
    return REPO / "data" / ticker / "10-K" / folder


def main():
    rows = [json.loads(line) for line in (HERE / "benchmark_qa_0.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    doc_ids = sorted({e["doc_id"] for r in rows for e in r["gold_evidence"]})
    PDFS.mkdir(exist_ok=True)
    EMBS.mkdir(exist_ok=True)

    for doc_id in doc_ids:
        pdf = PDFS / f"{doc_id}.pdf"
        if not pdf.exists():
            subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                            f"--print-to-pdf={pdf}", (doc_folder(doc_id) / "original.htm").as_uri()],
                           capture_output=True, timeout=600)
    print(f"{len(doc_ids)} filings printed to PDF", flush=True)

    model = ColQwen2_5.from_pretrained(MODEL_NAME, torch_dtype=torch.bfloat16, device_map="cuda").eval()
    processor = ColQwen2_5_Processor.from_pretrained(MODEL_NAME)
    for n, doc_id in enumerate(doc_ids, 1):
        out = EMBS / f"{doc_id}.pt"
        if out.exists():
            continue
        pages, embs = render_pages(PDFS / f"{doc_id}.pdf"), []
        for start in range(0, len(pages), 4):
            batch = processor.process_images(pages[start:start + 4]).to(model.device)
            with torch.no_grad():
                embs.extend(torch.unbind(model(**batch).to("cpu")))
        torch.save(embs, out)
        print(f"[{n}/{len(doc_ids)}] {doc_id}: {len(embs)} pages", flush=True)


if __name__ == "__main__":
    main()
