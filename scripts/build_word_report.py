"""
Generates the Word Document (.docx) version of the System C & RQ3 final report.

The Markdown report (reports/CS614_Group8_System_C_and_RQ3_Final_Report.md) is the
single source of truth; this script renders it with the report's house style so the
two documents cannot drift apart. Aryan's placeholder blockquotes render as red boxes.

Usage:
    python scripts/build_word_report.py
"""

import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_MD = REPO_ROOT / "reports" / "CS614_Group8_System_C_and_RQ3_Final_Report.md"
OUT_DOCX = REPO_ROOT / "reports" / "CS614_Group8_System_C_and_RQ3_Final_Report.docx"

NAVY = RGBColor(0x1B, 0x36, 0x5D)
BLUE = RGBColor(0x00, 0x5A, 0x9C)
DARK_RED = RGBColor(0xC0, 0x00, 0x00)
GREY = RGBColor(0x55, 0x55, 0x55)

INLINE_RE = re.compile(r"(\*\*.+?\*\*|`[^`]+`|\*[^*\s][^*]*?\*)")
LATEX_SUBS = {r"$\ge 0.8$": "≥ 0.8", r"$\ge$": "≥", r"$\rightarrow$": "→"}


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def clean_text(text):
    """Strip HTML spans and Markdown escapes, and replace the few LaTeX fragments used."""
    text = re.sub(r"</?span[^>]*>", "", text)
    for k, v in LATEX_SUBS.items():
        text = text.replace(k, v)
    return text.replace("\\$", "$").replace("\\*", "*").rstrip()


def add_inline(paragraph, text, size=None, color=None, italic=False):
    """Add text to a paragraph, honouring **bold**, *italic* and `code` spans."""
    for part in INLINE_RE.split(clean_text(text)):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        elif part.startswith("`") and part.endswith("`"):
            run = paragraph.add_run(part[1:-1])
            run.font.name = "Consolas"
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            run = paragraph.add_run(part[1:-1])
            run.italic = True
        else:
            run = paragraph.add_run(part)
        if italic:
            run.italic = True
        if size:
            run.font.size = Pt(size)
        if color is not None:
            run.font.color.rgb = color


class ReportRenderer:
    def __init__(self):
        self.doc = Document()
        for section in self.doc.sections:
            section.top_margin = section.bottom_margin = Inches(1.0)
            section.left_margin = section.right_margin = Inches(1.0)
        normal = self.doc.styles['Normal']
        normal.font.name = 'Calibri'
        normal.font.size = Pt(11)
        normal.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
        normal.paragraph_format.line_spacing = 1.15
        normal.paragraph_format.space_after = Pt(6)

    def title(self, text):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(clean_text(text))
        run.font.size = Pt(20)
        run.bold = True
        run.font.color.rgb = NAVY

    def meta(self, text):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        add_inline(p, text, size=10, color=GREY)

    def heading(self, text, level):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16 if level == 2 else 12)
        p.paragraph_format.space_after = Pt(6 if level == 2 else 4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(clean_text(text))
        run.bold = True
        run.font.size = Pt(14 if level == 2 else 12)
        run.font.color.rgb = NAVY if level == 2 else BLUE

    def paragraph(self, text):
        add_inline(self.doc.add_paragraph(), text)

    def list_item(self, text, numbered, depth):
        style = "List Number" if numbered else "List Bullet"
        if depth and not numbered:
            style += " 2"
        add_inline(self.doc.add_paragraph(style=style), text)

    def table(self, rows):
        header, body = rows[0], rows[1:]
        tbl = self.doc.add_table(rows=len(rows), cols=len(header))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.style = 'Table Grid'
        for j, h in enumerate(header):
            c = tbl.cell(0, j)
            set_cell_background(c, "1B365D")
            set_cell_margins(c)
            add_inline(c.paragraphs[0], h.replace("**", ""), size=9.5, color=RGBColor(0xFF, 0xFF, 0xFF))
            for run in c.paragraphs[0].runs:
                run.bold = True
        for i, row in enumerate(body, start=1):
            for j, val in enumerate(row):
                c = tbl.cell(i, j)
                set_cell_background(c, "F9FBFD" if i % 2 == 1 else "FFFFFF")
                set_cell_margins(c)
                add_inline(c.paragraphs[0], val, size=9.5)
        self.doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def red_box(self, lines):
        tbl = self.doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "FFF0F0")
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
        header, body = lines[0], " ".join(lines[1:])
        add_inline(cell.paragraphs[0], header.replace("**", ""), color=DARK_RED)
        for run in cell.paragraphs[0].runs:
            run.bold = True
        if body:
            add_inline(cell.add_paragraph(), body, color=DARK_RED, italic=True)
        self.doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def code_block(self, lines, lang):
        caption = "Figure: System C LangGraph control flow (Mermaid source)" if lang == "mermaid" else None
        tbl = self.doc.add_table(rows=1, cols=1)
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F4F6F8")
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        run = p.add_run("\n".join(lines))
        run.font.name = "Consolas"
        run.font.size = Pt(8)
        if caption:
            self.caption(caption)
        else:
            self.doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def image(self, alt, rel_path):
        path = (SOURCE_MD.parent / rel_path).resolve()
        if not path.exists():
            self.paragraph(f"[Missing figure: {rel_path}]")
            return
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(path), width=Inches(6.0))
        self.caption(f"Figure: {alt}")

    def caption(self, text):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_inline(p, text, size=9, color=GREY, italic=True)

    def save(self, path):
        self.doc.save(path)


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def render(md_text, renderer):
    lines = md_text.splitlines()
    i, in_header = 0, True
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            block = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            renderer.code_block(block, lang)
        elif stripped.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                if not re.fullmatch(r"\|[\s:\-|]+\|", lines[i].strip()):
                    rows.append(split_row(lines[i]))
                i += 1
            renderer.table(rows)
            continue
        elif stripped.startswith(">"):
            block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(lines[i].strip().lstrip(">").strip())
                i += 1
            renderer.red_box([b for b in block if b])
            continue
        elif stripped.startswith("# "):
            renderer.title(stripped[2:])
        elif stripped.startswith("## "):
            in_header = False
            renderer.heading(stripped[3:], level=2)
        elif stripped.startswith("### "):
            renderer.heading(stripped[4:], level=3)
        elif stripped == "---" or not stripped:
            pass
        elif in_header:
            renderer.meta(stripped)
        elif m := re.fullmatch(r"!\[(.*)\]\((.+)\)", stripped):
            renderer.image(m.group(1), m.group(2))
        elif m := re.match(r"(\s*)([*-]|\d+\.)\s+(.*)", line):
            renderer.list_item(m.group(3), numbered=m.group(2)[0].isdigit(), depth=len(m.group(1)) // 2)
        else:
            renderer.paragraph(stripped)
        i += 1


def create_report(source=SOURCE_MD, out=OUT_DOCX):
    renderer = ReportRenderer()
    render(Path(source).read_text(encoding="utf-8"), renderer)
    renderer.save(out)
    print(f"Successfully generated Word document: {out}")


if __name__ == "__main__":
    create_report()
