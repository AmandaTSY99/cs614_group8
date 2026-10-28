"""Retrieval-only check on normal (narrative) questions: text RAG 3 chunks vs ColQwen2.5 pages.

A chunk or page is a hit if it contains the gold phrase (case and whitespace ignored).
Uses cached page embeddings from colpali_eval/embs/; no LLM calls.
"""
import re
import sys
from pathlib import Path

import numpy as np
import pypdfium2 as pdfium
import torch
from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(Path(__file__).parent))
from run_eval import BGE_QUERY_PREFIX, FILINGS, ROOT, load_chunker

from colpali_engine.models import ColQwen2_5, ColQwen2_5_Processor

MODEL_NAME = "vidore/colqwen2.5-v0.2"

QUESTIONS = [   # (filing, question, gold phrase)
    ("NVDA_FY2026", "How have U.S. export controls affected NVIDIA's ability to sell to customers?", "export control restrictions"),
    ("MSFT_FY2025", "How many people did Microsoft employ as of June 30, 2025?", "228,000"),
    ("AAPL_FY2025", "Where is Apple's manufacturing performed?", "outsourcing partners located primarily in"),
    ("AMZN_FY2025", "How many employees did Amazon have at the end of 2025?", "1,576,000"),
    ("GOOGL_FY2025", "How does the EU Digital Markets Act affect Alphabet?", "Digital Markets Act"),
    ("JNJ_FY2025", "How is Johnson & Johnson trying to resolve the talc claims?", "talc claims"),
    ("JPM_FY2025", "What stress testing framework does the Federal Reserve apply to JPMorgan Chase?", "Comprehensive Capital Analysis and Review"),
    ("META_FY2025", "What are Meta's reportable segments?", "Family of Apps (FoA) and Reality Labs (RL)"),
    ("TSLA_FY2025", "What is Tesla's Cortex AI training cluster?", "Cortex"),
    ("WMT_FY2026", "How many associates does Walmart employ?", "2.1 million associates"),
]


def norm(text):
    return re.sub(r"\s+", " ", text).lower()


def first_hit_rank(order, texts, phrase):
    hits = [rank for rank, i in enumerate(order, 1) if norm(phrase) in norm(texts[i])]
    return (hits[0] if hits else None), len(hits)


chunk_by_structure = load_chunker()
bge = SentenceTransformer("BAAI/bge-small-en-v1.5")
model = ColQwen2_5.from_pretrained(MODEL_NAME, torch_dtype=torch.bfloat16, device_map="cuda").eval()
processor = ColQwen2_5_Processor.from_pretrained(MODEL_NAME)

rows = []
for filing, question, phrase in QUESTIONS:
    chunks = [c["text"] for c in chunk_by_structure(FILINGS[filing]["md"].read_text(encoding="utf-8"), "md")]
    vecs = bge.encode(chunks, normalize_embeddings=True)
    q = bge.encode([BGE_QUERY_PREFIX + question], normalize_embeddings=True)[0]
    chunk_rank, chunk_hits = first_hit_rank(np.argsort(-(vecs @ q)), chunks, phrase)

    pdf = pdfium.PdfDocument(str(ROOT / "pdfs" / f"{filing}.pdf"))
    pages = [pdf[i].get_textpage().get_text_range() for i in range(len(pdf))]
    embs = torch.load(ROOT / "embs" / f"{filing}_colqwen2.5-v0.2.pt")
    with torch.no_grad():
        qv = torch.unbind(model(**processor.process_queries([question]).to(model.device)).to("cpu"))
    page_rank, page_hits = first_hit_rank(torch.argsort(processor.score_multi_vector(qv, embs)[0], descending=True).tolist(),
                                          pages, phrase)
    rows.append((filing, question, chunk_rank, len(chunks), chunk_hits, page_rank, len(pages), page_hits))

print("| Filing | Question | Text RAG 3: rank of first gold chunk | ColQwen2.5: rank of first gold page |")
print("|---|---|---|---|")
for f, q, cr, nc, ch, pr, np_, ph in rows:
    print(f"| {f} | {q} | {cr} of {nc} ({ch} gold) | {pr} of {np_} ({ph} gold) |")
top5 = sum(1 for r in rows if r[2] and r[2] <= 5)
top3 = sum(1 for r in rows if r[5] and r[5] <= 3)
top1c = sum(1 for r in rows if r[2] == 1)
top1p = sum(1 for r in rows if r[5] == 1)
print(f"| **Total** | | top-1: {top1c}/{len(rows)} · top-5: **{top5}/{len(rows)}** | top-1: {top1p}/{len(rows)} · top-3: **{top3}/{len(rows)}** |")
