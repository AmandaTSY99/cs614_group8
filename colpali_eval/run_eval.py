"""Before/after: text RAG 3 (structure chunks + bge) vs ColPali page retrieval + a Groq vision model.

Run from the repo root with the GPU venv:  .venv/Scripts/python colpali_eval/run_eval.py
Needs GROQ_API_KEY. PDFs come from printing data/<ticker>/10-K/<folder>/original.htm (see README.md here).
"""
import base64
import io
import json
import os
import re
import time
from pathlib import Path

import numpy as np
import pypdfium2 as pdfium
import torch
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
TOP_K_CHUNKS = 5          # same as TOP_K in build_vdb_base_RAG.ipynb
TOP_K_PAGES = 3           # pages sent to the vision model
TEXT_MODEL = "openai/gpt-oss-120b"
VISION_MODEL = os.getenv("GROQ_VISION_MODEL", "qwen/qwen3.8-27b")   # the only image-capable model on Groq right now
COLPALI_MODEL = os.getenv("COLPALI_MODEL", "vidore/colqwen2.5-v0.2")   # colpali-v1.3 ranked the MSFT page 48th
BGE_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

FOLDERS = {   # latest 10-K per company; the PDF for each is colpali_eval/pdfs/<key>.pdf
    "MSFT_FY2025": "MSFT/10-K/FY2025_2025-06-30", "NVDA_FY2026": "NVDA/10-K/FY2026_2026-01-25",
    "AAPL_FY2025": "AAPL/10-K/FY2025_2025-09-27", "AMZN_FY2025": "AMZN/10-K/FY2025_2025-12-31",
    "GOOGL_FY2025": "GOOGL/10-K/FY2025_2025-12-31", "JNJ_FY2025": "JNJ/10-K/FY2025_2025-12-28",
    "JPM_FY2025": "JPM/10-K/FY2025_2025-12-31", "META_FY2025": "META/10-K/FY2025_2025-12-31",
    "TSLA_FY2025": "TSLA/10-K/FY2025_2025-12-31", "WMT_FY2026": "WMT/10-K/FY2026_2026-01-31",
}
FILINGS = {key: {"md": REPO / "data" / folder / "10-K.md", "htm": REPO / "data" / folder / "original.htm",
                 "ticker": key.split("_")[0], "fy": int(key.split("FY")[1])}
           for key, folder in FOLDERS.items()}

# Each answer row sits in a later piece of a cash flow table that split_table cut at 200 words.
QUESTIONS = [
    ("MSFT_FY2025", "What was Microsoft's net change in cash and cash equivalents for fiscal year 2025?", "11,927"),
    ("MSFT_FY2025", "How much net cash did Microsoft use in investing activities in fiscal year 2025?", "72,599"),
    ("NVDA_FY2026", "How much net cash did NVIDIA use in financing activities in fiscal year 2026?", "48,474"),
    ("NVDA_FY2026", "What were NVIDIA's cash and cash equivalents at the end of fiscal year 2026?", "10,605"),
    ("AAPL_FY2025", "How much cash did Apple use in financing activities in fiscal year 2025?", "120,686"),
    ("AAPL_FY2025", "How much did Apple spend on repurchases of common stock in fiscal year 2025?", "90,711"),
    ("AMZN_FY2025", "What was Amazon's net cash provided by (used in) financing activities in 2025?", "9,661"),
    ("AMZN_FY2025", "What were Amazon's cash, cash equivalents, and restricted cash at the end of 2025?", "90,106"),
    ("GOOGL_FY2025", "How much net cash did Alphabet use in financing activities in 2025?", "37,388"),
    ("GOOGL_FY2025", "What were Alphabet's cash and cash equivalents at the end of 2025?", "30,708"),
    ("JNJ_FY2025", "How much net cash did Johnson & Johnson use in financing activities in 2025?", "5,539"),
    ("JNJ_FY2025", "What were Johnson & Johnson's cash and cash equivalents at the end of 2025?", "19,709"),
    ("JPM_FY2025", "What was JPMorgan Chase's net cash provided by financing activities in 2025?", "269,533"),
    ("JPM_FY2025", "What were JPMorgan Chase's cash and due from banks and deposits with banks at the end of 2025?", "343,338"),
    ("META_FY2025", "How much did Meta spend on repurchases of Class A common stock in 2025?", "26,248"),
    ("META_FY2025", "How much net cash did Meta use in financing activities in 2025?", "20,370"),
    ("TSLA_FY2025", "What was Tesla's net cash provided by financing activities in 2025?", "1,139"),
    ("TSLA_FY2025", "What were Tesla's cash and cash equivalents and restricted cash at the end of 2025?", "17,616"),
    ("WMT_FY2026", "How much net cash did Walmart use in financing activities in fiscal year 2026?", "13,553"),
    ("WMT_FY2026", "What were Walmart's cash, cash equivalents and restricted cash at the end of fiscal year 2026?", "11,321"),
]

RAG_SYSTEM = ("Answer the question using ONLY the context below. Cite the chunk ids you used, like [2]. "
              "Each chunk is labelled with its company and fiscal year. "
              "If the answer is not in the context, reply exactly: Not found in the provided context.")
VISION_SYSTEM = ("Answer the question using ONLY the attached 10-K pages. Cite the page numbers you used, like [p. 52]. "
                 "If the answer is not on the pages, reply exactly: Not found in the provided context.")


def load_chunker():
    """Run the notebook's chunking cell so the baseline uses exactly the same chunk_by_structure."""
    nb = json.loads((REPO / "build_vdb_base_RAG.ipynb").read_text(encoding="utf-8"))
    cell = next("".join(c["source"]) for c in nb["cells"]
                if c["cell_type"] == "code" and "def chunk_by_structure" in "".join(c["source"]))
    scope = {"re": re}
    exec(cell, scope)
    return scope["chunk_by_structure"]


NUMBER_RE = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*(billion|bn|million|mn)?", re.IGNORECASE)


def is_correct(answer, expected):
    """Correct if the answer states the expected figure ($M), exactly or rounded in millions or billions.
    "$19.7 billion" matches 19,709 (19.709 rounds to 19.7); "$26.26 billion" does not match 26,248."""
    target = float(expected.replace(",", ""))
    for number, unit in NUMBER_RE.findall(answer):
        value = float(number.replace(",", ""))
        decimals = len(number.split(".")[1]) if "." in number else 0
        scale = 1000 if unit.lower() in ("billion", "bn") else 1
        if round(target / scale, decimals) == value:
            return True
    return False


def ask(client, **kwargs):
    """One chat call; on Groq's rate limit, wait and retry instead of losing the run."""
    from groq import RateLimitError
    for attempt in range(30):
        try:
            return client.chat.completions.create(**kwargs).choices[0].message.content
        except RateLimitError as err:
            wait = re.search(r"try again in (?:(\d+)m)?([\d.]+)s", str(err))
            seconds = (int(wait.group(1) or 0) * 60 + float(wait.group(2))) if wait else 60
            print(f"rate limited, waiting {seconds:.0f}s")
            time.sleep(seconds + 5)
    raise RuntimeError("still rate limited after 30 retries")


def run_text_rag(client, questions, model=TEXT_MODEL):
    chunk_by_structure = load_chunker()
    bge = SentenceTransformer("BAAI/bge-small-en-v1.5")
    chunks = {name: chunk_by_structure(f["md"].read_text(encoding="utf-8"), "md") for name, f in FILINGS.items()}
    vectors = {name: bge.encode([c["text"] for c in cs], normalize_embeddings=True) for name, cs in chunks.items()}

    results = []
    for filing, question, expected in questions:
        q = bge.encode([BGE_QUERY_PREFIX + question], normalize_embeddings=True)[0]
        top = np.argsort(-(vectors[filing] @ q))[:TOP_K_CHUNKS]   # scoped to one filing, like ticker+fiscal_year filters
        meta = FILINGS[filing]
        context = "\n\n".join(f"[{n}] ({meta['ticker']} FY{meta['fy']} 10-K) {chunks[filing][i]['text']}"
                              for n, i in enumerate(top, 1))
        extra = {"reasoning_effort": "low"} if "gpt-oss" in model else {}
        answer = client.chat.completions.create(
            model=model, temperature=0.0, max_tokens=1024, **extra,
            messages=[{"role": "system", "content": RAG_SYSTEM},
                      {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}],
        ).choices[0].message.content
        answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()
        results.append({"filing": filing, "question": question, "expected": expected, "answer": answer,
                        "correct": is_correct(answer, expected),
                        "retrieved": [chunks[filing][i]["text"] for i in top]})
    return results


class Pages:
    """Pages of one PDF, rendered on demand so a 479-page filing never sits in memory all at once."""
    def __init__(self, pdf_path, scale=150 / 72):
        self.pdf, self.scale = pdfium.PdfDocument(str(pdf_path)), scale

    def __len__(self):
        return len(self.pdf)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return [self[j] for j in range(*i.indices(len(self)))]
        return self.pdf[i].render(scale=self.scale).to_pil().convert("RGB")


def render_pages(pdf_path):
    return Pages(pdf_path)


def image_url(img, max_side=1600):
    img = img.copy()
    img.thumbnail((max_side, max_side))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def run_colpali(client, questions):
    from colpali_engine.models import ColPali, ColPaliProcessor, ColQwen2_5, ColQwen2_5_Processor

    model_cls, proc_cls = ((ColQwen2_5, ColQwen2_5_Processor) if "colqwen2.5" in COLPALI_MODEL
                           else (ColPali, ColPaliProcessor))
    model = model_cls.from_pretrained(COLPALI_MODEL, torch_dtype=torch.bfloat16, device_map="cuda").eval()
    processor = proc_cls.from_pretrained(COLPALI_MODEL)
    tag = COLPALI_MODEL.split("/")[-1]
    (ROOT / "embs").mkdir(exist_ok=True)

    pages, page_embs = {}, {}
    for name in FILINGS:
        pages[name] = render_pages(ROOT / "pdfs" / f"{name}.pdf")
        cache = ROOT / "embs" / f"{name}_{tag}.pt"
        if cache.exists():                       # page embeddings are reused across runs
            page_embs[name] = torch.load(cache)
            continue
        embs = []
        for start in range(0, len(pages[name]), 4):
            batch = processor.process_images(pages[name][start:start + 4]).to(model.device)
            with torch.no_grad():
                embs.extend(torch.unbind(model(**batch).to("cpu")))
        torch.save(embs, cache)
        page_embs[name] = embs
        print(f"{name}: embedded {len(embs)} pages")

    results = []
    for filing, question, expected in questions:
        batch = processor.process_queries([question]).to(model.device)
        with torch.no_grad():
            q = torch.unbind(model(**batch).to("cpu"))
        scores = processor.score_multi_vector(q, page_embs[filing])[0]
        top = torch.argsort(scores, descending=True)[:TOP_K_PAGES].tolist()
        content = [{"type": "text", "text": f"Pages {', '.join(str(i + 1) for i in top)} of the "
                                            f"{FILINGS[filing]['ticker']} FY{FILINGS[filing]['fy']} 10-K, in that order.\n\n"
                                            f"Question: {question}"}]
        images = {i: pages[filing][i] for i in top}
        content += [{"type": "image_url", "image_url": {"url": image_url(images[i])}} for i in top]
        answer = ask(client,
            model=VISION_MODEL, temperature=0.0, max_tokens=1024,
            messages=[{"role": "system", "content": VISION_SYSTEM}, {"role": "user", "content": content}])
        answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()   # grade the answer, not the reasoning
        results.append({"filing": filing, "question": question, "expected": expected, "answer": answer,
                        "correct": is_correct(answer, expected), "retrieved_pages": [i + 1 for i in top]})
        for i in top:   # keep the retrieved pages so the report can show them
            images[i].save(ROOT / "pages" / f"{filing}_p{i + 1}.png")
    return results


def main():
    load_dotenv(REPO / ".env")
    client = Groq()
    (ROOT / "pages").mkdir(exist_ok=True)
    def stage(name, run):
        """Save each stage as it finishes, so a rate-limit stop does not lose the stages already paid for."""
        path = ROOT / f"stage_{name}.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        result = run()
        path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result

    before = stage("before", lambda: run_text_rag(client, QUESTIONS))
    after = stage("after", lambda: run_colpali(client, QUESTIONS))
    control = stage("control", lambda: run_text_rag(client, QUESTIONS, model=VISION_MODEL))   # same model as ColPali side
    (ROOT / "results.json").write_text(json.dumps({"before": before, "control": control, "after": after}, indent=2),
                                       encoding="utf-8")

    mark = lambda r: "correct" if r["correct"] else "wrong"
    total = lambda rs: f"**{sum(r['correct'] for r in rs)}/{len(rs)}**"
    lines = [f"| Question | Expected | Text RAG 3 ({TEXT_MODEL}) | Text RAG 3 ({VISION_MODEL}) | {COLPALI_MODEL.split('/')[-1]} + {VISION_MODEL} |",
             "|---|---|---|---|---|"]
    for b, c, a in zip(before, control, after):
        lines.append(f"| {b['question']} | {b['expected']} | {mark(b)} | {mark(c)} | {mark(a)} (pages {a['retrieved_pages']}) |")
    lines.append(f"| **Total** | | {total(before)} | {total(control)} | {total(after)} |")
    (ROOT / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
