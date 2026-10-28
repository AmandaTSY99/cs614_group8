"""Where do the pages that hold each answer rank under ColPali? Caches page embeddings in colpali_eval/embs/."""
import re
import sys
from pathlib import Path

import pypdfium2 as pdfium
import torch

sys.path.insert(0, str(Path(__file__).parent))
from run_eval import COLPALI_MODEL, FILINGS, QUESTIONS, ROOT, render_pages

from colpali_engine.models import ColPali, ColPaliProcessor, ColQwen2_5, ColQwen2_5_Processor

MODEL_NAME = sys.argv[1] if len(sys.argv) > 1 else COLPALI_MODEL
model_cls, proc_cls = (ColQwen2_5, ColQwen2_5_Processor) if "colqwen2.5" in MODEL_NAME else (ColPali, ColPaliProcessor)
model = model_cls.from_pretrained(MODEL_NAME, torch_dtype=torch.bfloat16, device_map="cuda").eval()
processor = proc_cls.from_pretrained(MODEL_NAME)
TAG = MODEL_NAME.split("/")[-1]
(ROOT / "embs").mkdir(exist_ok=True)

for name in FILINGS:
    cache = ROOT / "embs" / f"{name}_{TAG}.pt"
    if not cache.exists():
        pages, embs = render_pages(ROOT / "pdfs" / f"{name}.pdf"), []
        for start in range(0, len(pages), 4):
            batch = processor.process_images(pages[start:start + 4]).to(model.device)
            with torch.no_grad():
                embs.extend(torch.unbind(model(**batch).to("cpu")))
        torch.save(embs, cache)

for filing, question, expected in QUESTIONS:
    pdf = pdfium.PdfDocument(str(ROOT / "pdfs" / f"{filing}.pdf"))
    gold = [i for i in range(len(pdf)) if expected in pdf[i].get_textpage().get_text_range()]
    embs = torch.load(ROOT / "embs" / f"{filing}_{TAG}.pt")
    batch = processor.process_queries([question]).to(model.device)
    with torch.no_grad():
        q = torch.unbind(model(**batch).to("cpu"))
    order = torch.argsort(processor.score_multi_vector(q, embs)[0], descending=True).tolist()
    print(f"{question}\n  pages containing {expected}: {[g + 1 for g in gold]}  ranks: {[order.index(g) + 1 for g in gold]}"
          f"  top3: {[o + 1 for o in order[:3]]}")
