"""
Architecture diagrams for the five systems, drawn as inline SVG so they can light up live as a query runs.

Layouts follow the final deck: slide 8 (A and B), slide 9 (C v1 loop), slide 10 (C v2 XBRL lookup)
and slide 20 (C v3 schema-aware routing). Node ids for System C match the LangGraph node names.
"""

import html
from typing import Dict, Iterable, List, Optional, Tuple

from ui.theme import SYSTEM_INFO

NODE_W, NODE_H = 156, 74
MAIN_Y, LOOP_Y = 46, 196

# node id -> (x, y, title, subtitle lines)
Layout = Dict[str, Tuple[int, int, str, List[str]]]
# (from, to, label, kind) where kind is "main", "loop", "bypass" or "back"
Edges = List[Tuple[str, str, str, str]]


def _six(x0: int = 10, step: int = 200) -> List[int]:
    return [x0 + i * step for i in range(6)]


def _layouts() -> Dict[str, Tuple[Layout, Edges, int, int]]:
    """system -> (nodes, edges, viewBox height, viewBox width)."""
    x = _six()
    single_x = [40, 290, 540, 790]
    five_x = [10, 210, 410, 610, 810]
    return {
        "system_a": ({
            "question": (single_x[0], MAIN_Y, "Question", ["Company and year", "filters the search"]),
            "retrieve": (single_x[1], MAIN_Y, "Dense search", ["BGE-small embeddings", "up to 10 chunks"]),
            "generate": (single_x[2], MAIN_Y, "Generate", ["One gpt-5.4 call", "cites chunks as [n]"]),
            "answer": (single_x[3], MAIN_Y, "Answer", ["No checking step", "1 hop"]),
        }, [("question", "retrieve", "", "main"), ("retrieve", "generate", "", "main"),
            ("generate", "answer", "", "main")], 150, 1000),
        "system_b": ({
            "question": (five_x[0], MAIN_Y, "Question", ["Company and year", "filters the search"]),
            "retrieve": (five_x[1], MAIN_Y, "BM25 + dense", ["Equal-weight fusion", "30 candidates"]),
            "rerank": (five_x[2], MAIN_Y, "Rerank", ["Cross-encoder", "keeps top 5"]),
            "generate": (five_x[3], MAIN_Y, "Generate", ["One gpt-5.4 call", "cites chunks as [n]"]),
            "answer": (five_x[4], MAIN_Y, "Answer", ["No checking step", "1 hop"]),
        }, [("question", "retrieve", "", "main"), ("retrieve", "rerank", "", "main"),
            ("rerank", "generate", "", "main"), ("generate", "answer", "", "main")], 150, 1000),
        "system_c_v1": ({
            "decomposer": (five_x[0], MAIN_Y, "Decomposer", ["Finds tickers, years", "and sub-queries"]),
            "retriever": (five_x[1], MAIN_Y, "Retriever", ["Hybrid search,", "removes duplicates"]),
            "critic": (five_x[2], MAIN_Y, "Critic", ["Checks evidence,", "names what's missing"]),
            "synthesizer": (five_x[3], MAIN_Y, "Synthesizer", ["Writes the answer", "with citations"]),
            "guardrail": (five_x[4], MAIN_Y, "Guardrail", ["Checks every number", "against its source"]),
            "generator": (310, LOOP_Y, "Generator", ["Writes a follow-up", "query for the gap"]),
        }, [("decomposer", "retriever", "", "main"), ("retriever", "critic", "", "main"),
            ("critic", "synthesizer", "enough", "main"), ("synthesizer", "guardrail", "", "main"),
            ("critic", "generator", "gaps remain and hop < 3", "loop"), ("generator", "retriever", "", "back")], 300, 1000),
        "system_c_v2": ({
            "decomposer": (x[0], MAIN_Y, "Decomposer", ["Flags numeric", "questions"]),
            "tabular_tool": (x[1], MAIN_Y, "XBRL lookup", ["Adds reported figures", "from financials.csv"]),
            "retriever": (x[2], MAIN_Y, "Retriever", ["Hybrid search,", "removes duplicates"]),
            "critic": (x[3], MAIN_Y, "Critic", ["Stops at 0.95 if the", "table covers companies"]),
            "synthesizer": (x[4], MAIN_Y, "Synthesizer", ["Writes the answer", "with citations"]),
            "guardrail": (x[5], MAIN_Y, "Guardrail", ["Checks every number", "against its source"]),
            "generator": (x[2] + 100, LOOP_Y, "Generator", ["Writes a follow-up", "query for the gap"]),
        }, [("decomposer", "tabular_tool", "", "main"), ("tabular_tool", "retriever", "", "main"),
            ("decomposer", "retriever", "not numeric", "bypass"), ("retriever", "critic", "", "main"),
            ("critic", "synthesizer", "enough", "main"), ("synthesizer", "guardrail", "", "main"),
            ("critic", "generator", "gaps remain and hop < 3", "loop"), ("generator", "retriever", "", "back")], 300, 1176),
        "system_c_v3": ({
            "decomposer": (x[0], MAIN_Y, "Decomposer", ["Plans years, tickers", "and the route"]),
            "tabular_tool": (x[1], MAIN_Y, "XBRL lookup", ["Only for the 9", "headline metrics"]),
            "retriever": (x[2], MAIN_Y, "Hybrid search", ["BM25 + dense per hop,", "stitches split tables"]),
            "critic": (x[3], MAIN_Y, "Critic", ["Is each line item", "present, every year?"]),
            "synthesizer": (x[4], MAIN_Y, "Synthesizer", ["Writes the answer,", "one citation per claim"]),
            "guardrail": (x[5], MAIN_Y, "Guardrail", ["Checks every number;", "repairs if one fails"]),
            "generator": (x[2] + 100, LOOP_Y, "Generator", ["Targets the missing", "line item"]),
        }, [("decomposer", "tabular_tool", "", "main"), ("tabular_tool", "retriever", "", "main"),
            ("decomposer", "retriever", "margins, segments, footnotes", "bypass"), ("retriever", "critic", "", "main"),
            ("critic", "synthesizer", "found", "main"), ("synthesizer", "guardrail", "", "main"),
            ("critic", "generator", "line item missing and hop < 3", "loop"), ("generator", "retriever", "", "back")], 300, 1176),
    }


LAYOUTS = _layouts()


def _edge_path(a, b, kind) -> Tuple[str, Tuple[float, float]]:
    ax, ay = a[0], a[1]
    bx, by = b[0], b[1]
    if kind == "main":
        x1, y1, x2, y2 = ax + NODE_W, ay + NODE_H / 2, bx, by + NODE_H / 2
        return f"M{x1},{y1} L{x2 - 3},{y2}", ((x1 + x2) / 2, y1 - 9)
    if kind == "bypass":
        x1, y1 = ax + NODE_W / 2, ay
        x2, y2 = bx + NODE_W / 2, by
        top = ay - 34
        return f"M{x1},{y1} C{x1},{top} {x2},{top} {x2},{y2 - 3}", ((x1 + x2) / 2, top + 1)
    if kind == "loop":  # critic (top) down to generator (bottom right side)
        x1, y1 = ax + NODE_W / 2, ay + NODE_H
        x2, y2 = bx + NODE_W, by + NODE_H / 2
        return f"M{x1},{y1} C{x1},{y2} {x1},{y2} {x2 + 3},{y2}", (x1 + 8, (y1 + y2) / 2 + 4)
    # back: generator (bottom) up to retriever (top)
    x1, y1 = ax, ay + NODE_H / 2
    x2, y2 = bx + NODE_W / 2, by + NODE_H
    return f"M{x1},{y1} C{x2},{y1} {x2},{y1} {x2},{y2 + 3}", ((x1 + x2) / 2, y1)


def render_diagram(
    system: str,
    active: Optional[str] = None,
    visited: Iterable[str] = (),
    caption: Optional[str] = None,
    static: bool = False,
) -> str:
    """Return the system's diagram as HTML; `active` glows, `visited` nodes are ticked, `static` colours everything."""
    layout, edges, height, width = LAYOUTS[system]
    color = SYSTEM_INFO[system]["color"]
    visited = set(layout) if static else set(visited)
    if active == "repair":
        active = "guardrail"
    parts: List[str] = [
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="{html.escape(SYSTEM_INFO[system]["name"])} architecture">',
        "<defs>",
        f'<marker id="arr-{system}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#5F646B"/></marker>',
        f'<marker id="arr-on-{system}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>',
        f'<filter id="glow-{system}" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
        "</defs>",
    ]

    for src, dst, label, kind in edges:
        path, (lx, ly) = _edge_path(layout[src], layout[dst], kind)
        lit = src in visited and (dst in visited or dst == active)
        stroke = color if lit else "#454A50"
        dash = ' stroke-dasharray="5 5"' if kind in ("bypass", "loop", "back") else ""
        marker = f"arr-on-{system}" if lit else f"arr-{system}"
        parts.append(f'<path d="{path}" fill="none" stroke="{stroke}" stroke-width="2"{dash} marker-end="url(#{marker})"/>')
        if label:
            anchor = "start" if kind == "loop" else "middle"
            parts.append(f'<text x="{lx}" y="{ly}" text-anchor="{anchor}" font-size="11.5" fill="#A29D92" '
                         f'font-family="IBM Plex Sans, -apple-system, sans-serif">{html.escape(label)}</text>')

    for node_id, (nx, ny, title, sub) in layout.items():
        is_active, is_done = node_id == active, node_id in visited
        fill = "#1D2023" if not (is_active or is_done) else ("#2B2719" if is_active else "#202326")
        stroke = color if (is_active or is_done) else "#3A3F45"
        glow = f' filter="url(#glow-{system})"' if is_active else ""
        width = 2.4 if is_active else 1.4
        parts.append(f'<g{glow}><rect x="{nx}" y="{ny}" width="{NODE_W}" height="{NODE_H}" rx="5" '
                     f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
        if is_active:
            parts.append(f'<rect x="{nx}" y="{ny}" width="{NODE_W}" height="{NODE_H}" rx="5" fill="none" stroke="{color}" '
                         'stroke-width="2"><animate attributeName="opacity" values="1;0.25;1" dur="1.4s" repeatCount="indefinite"/></rect>')
        parts.append("</g>")
        title_color = "#F2EDE2" if (is_active or is_done) else "#D6D1C6"
        parts.append(f'<text x="{nx + 14}" y="{ny + 25}" font-size="14.5" font-weight="600" fill="{title_color}" '
                     f'font-family="IBM Plex Sans, -apple-system, sans-serif">{html.escape(title)}</text>')
        for i, line in enumerate(sub):
            parts.append(f'<text x="{nx + 14}" y="{ny + 45 + i * 15}" font-size="11.5" fill="#A29D92" '
                         f'font-family="IBM Plex Sans, -apple-system, sans-serif">{html.escape(line)}</text>')
        if is_done and not is_active and not static:
            parts.append(f'<circle cx="{nx + NODE_W - 16}" cy="{ny + 18}" r="7" fill="{color}"/>'
                         f'<path d="M{nx + NODE_W - 19.5},{ny + 18} l2.5,2.5 l4.5,-5" stroke="#17191B" stroke-width="2" fill="none"/>')

    parts.append("</svg>")
    cap = f'<div class="small muted" style="padding:6px 4px 2px">{html.escape(caption)}</div>' if caption else ""
    return f'<div class="diagram">{"".join(parts)}{cap}</div>'
