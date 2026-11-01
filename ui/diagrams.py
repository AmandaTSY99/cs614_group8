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
            "retrieve": (single_x[1], MAIN_Y, "Dense search", ["Search by meaning,", "up to 10 passages"]),
            "generate": (single_x[2], MAIN_Y, "Generate", ["One model call,", "cites passages [n]"]),
            "answer": (single_x[3], MAIN_Y, "Answer", ["No checking step", "1 hop"]),
        }, [("question", "retrieve", "", "main"), ("retrieve", "generate", "", "main"),
            ("generate", "answer", "", "main")], 230, 1000),
        "system_b": ({
            "question": (five_x[0], MAIN_Y, "Question", ["Company and year", "filters the search"]),
            "retrieve": (five_x[1], MAIN_Y, "Hybrid search", ["Keywords + meaning,", "30 candidates"]),
            "rerank": (five_x[2], MAIN_Y, "Rerank", ["Cross-encoder", "keeps top 5"]),
            "generate": (five_x[3], MAIN_Y, "Generate", ["One model call,", "cites passages [n]"]),
            "answer": (five_x[4], MAIN_Y, "Answer", ["No checking step", "1 hop"]),
        }, [("question", "retrieve", "", "main"), ("retrieve", "rerank", "", "main"),
            ("rerank", "generate", "", "main"), ("generate", "answer", "", "main")], 230, 1000),
        "system_c_v1": ({
            "decomposer": (five_x[0], MAIN_Y, "Decomposer", ["Finds tickers, years", "and sub-queries"]),
            "retriever": (five_x[1], MAIN_Y, "Retriever", ["Searches the filings,", "keeps new passages"]),
            "critic": (five_x[2], MAIN_Y, "Critic", ["Checks: is anything", "still missing?"]),
            "synthesizer": (five_x[3], MAIN_Y, "Synthesizer", ["Writes the answer", "with citations"]),
            "guardrail": (five_x[4], MAIN_Y, "Guardrail", ["Checks every number", "against its passage"]),
            "generator": (310, LOOP_Y, "Generator", ["Writes a follow-up", "query for the gap"]),
        }, [("decomposer", "retriever", "", "main"), ("retriever", "critic", "", "main"),
            ("critic", "synthesizer", "enough", "main"), ("synthesizer", "guardrail", "", "main"),
            ("critic", "generator", "something missing, under 3 rounds", "loop"), ("generator", "retriever", "", "back")], 300, 1000),
        "system_c_v2": ({
            "decomposer": (x[0], MAIN_Y, "Decomposer", ["Flags numeric", "questions"]),
            "tabular_tool": (x[1], MAIN_Y, "XBRL lookup", ["Adds officially", "reported figures"]),
            "retriever": (x[2], MAIN_Y, "Retriever", ["Searches the filings,", "keeps new passages"]),
            "critic": (x[3], MAIN_Y, "Critic", ["Stops early once the", "table has the company"]),
            "synthesizer": (x[4], MAIN_Y, "Synthesizer", ["Writes the answer", "with citations"]),
            "guardrail": (x[5], MAIN_Y, "Guardrail", ["Checks every number", "against its passage"]),
            "generator": (x[2] + 100, LOOP_Y, "Generator", ["Writes a follow-up", "query for the gap"]),
        }, [("decomposer", "tabular_tool", "", "main"), ("tabular_tool", "retriever", "", "main"),
            ("decomposer", "retriever", "not numeric", "bypass"), ("retriever", "critic", "", "main"),
            ("critic", "synthesizer", "enough", "main"), ("synthesizer", "guardrail", "", "main"),
            ("critic", "generator", "something missing, under 3 rounds", "loop"), ("generator", "retriever", "", "back")], 300, 1176),
        "system_c_v3": ({
            "decomposer": (x[0], MAIN_Y, "Decomposer", ["Plans years, tickers", "and the route"]),
            "tabular_tool": (x[1], MAIN_Y, "XBRL lookup", ["Only for the 9", "headline metrics"]),
            "retriever": (x[2], MAIN_Y, "Hybrid search", ["BM25 + dense per hop,", "stitches split tables"]),
            "critic": (x[3], MAIN_Y, "Critic", ["Checks: is every figure", "found for every year?"]),
            "synthesizer": (x[4], MAIN_Y, "Synthesizer", ["Writes the answer,", "one citation per claim"]),
            "guardrail": (x[5], MAIN_Y, "Guardrail", ["Checks every number;", "repairs if one fails"]),
            "generator": (x[2] + 100, LOOP_Y, "Generator", ["Targets the missing", "line item"]),
        }, [("decomposer", "tabular_tool", "", "main"), ("tabular_tool", "retriever", "", "main"),
            ("decomposer", "retriever", "margins, segments, footnotes", "bypass"), ("retriever", "critic", "", "main"),
            ("critic", "synthesizer", "found", "main"), ("synthesizer", "guardrail", "", "main"),
            ("critic", "generator", "a figure missing, under 3 rounds", "loop"), ("generator", "retriever", "", "back")], 300, 1176),
    }


LAYOUTS = _layouts()

FONT = "IBM Plex Sans, -apple-system, sans-serif"

# Plain-English hover text for each step. System-specific wording wins over the shared default.
NODE_INFO: Dict[str, str] = {
    "question": "Your question, plus the company and year spotted in it. These narrow the search to the right filings.",
    "retrieve": "Searches the 10-K filings for the passages that best match your question.",
    "rerank": "A second model re-reads the top 30 passages and keeps the 5 that best answer the question.",
    "generate": "The language model writes an answer using only those passages, citing them as [1], [2] and so on.",
    "answer": "The final answer. Nothing checks it, so a wrong number goes straight through.",
    "decomposer": "Reads your question and works out which companies, which years and what exactly to look for.",
    "tabular_tool": "Looks up the company's officially reported figures (XBRL) and adds them as evidence before searching.",
    "retriever": "Searches the 10-K filings by keyword and by meaning, adding new passages each round.",
    "critic": "Checks whether the evidence so far is enough to answer. If not, it says exactly what is missing.",
    "generator": "Writes a new search aimed at what the critic said is missing, then searches again (up to 3 rounds).",
    "synthesizer": "Writes the answer and tags every sentence with the passage it came from.",
    "guardrail": "Checks every number in the answer against the passage it cites. If one does not match, it tries to fix it once.",
}
SYSTEM_NODE_INFO: Dict[Tuple[str, str], str] = {
    ("system_a", "retrieve"): "Turns your question into a vector and finds the 10 passages with the closest meaning.",
    ("system_b", "retrieve"): "Searches two ways, exact keywords (BM25) and meaning (embeddings), and merges the two result lists.",
    ("system_c_v3", "tabular_tool"): "Looks up officially reported figures (XBRL), but only for the 9 headline numbers such as revenue or total assets.",
    ("system_c_v3", "critic"): "Checks that every figure the question asks for has been found, for every year. If not, it says what is missing.",
    ("system_c_v3", "retriever"): "Searches the filings by keyword and by meaning, re-joining tables that were split across passages.",
}

# What a running step is waiting on, for the live status bar
NODE_WAIT = {
    "decomposer": "waiting for the language model", "critic": "waiting for the language model",
    "generator": "waiting for the language model", "synthesizer": "waiting for the language model",
    "guardrail": "checking numbers, then a language-model check", "repair": "waiting for the language model",
    "generate": "waiting for the language model", "retriever": "searching the filings", "retrieve": "searching the filings",
    "rerank": "re-ranking passages", "tabular_tool": "looking up reported figures", "question": "preparing the search",
}


def node_title(system: str, node: str) -> str:
    node = "guardrail" if node == "repair" else node
    return LAYOUTS[system][0].get(node, (0, 0, node.title(), []))[2]


def node_info(system: str, node: str) -> str:
    return SYSTEM_NODE_INFO.get((system, node)) or NODE_INFO.get(node, "")


def step_list_html(system: str) -> str:
    """Every step's explanation as plain text, for touch and keyboard users who cannot hover."""
    rows = "".join(f"<li><b>{html.escape(t)}</b> {html.escape(node_info(system, n))}</li>"
                   for n, (_, _, t, _) in LAYOUTS[system][0].items() if node_info(system, n))
    return f'<ul class="steps">{rows}</ul>'


def _wrap(text: str, width: int = 38) -> List[str]:
    lines, line = [], ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > width:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    return lines + ([line] if line else [])


def _fmt_secs(sec: float) -> str:
    return f"{sec:.1f}s" if sec < 60 else f"{int(sec // 60)}m{int(sec % 60):02d}s"


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
    timings: Optional[Dict[str, Tuple[float, int]]] = None,
) -> str:
    """Return the system's diagram as HTML.

    `active` glows, `visited` nodes are ticked, `static` colours everything, and `timings` ({node: (seconds, runs)})
    replaces the tick with how long the step took. Hovering a step shows what it does.
    """
    timings = timings or {}
    layout, edges, height, width = LAYOUTS[system]
    color = SYSTEM_INFO[system]["color"]
    visited = set(layout) if static else set(visited)
    if active == "repair":
        active = "guardrail"
    parts: List[str] = [
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="{html.escape(SYSTEM_INFO[system]["name"])} architecture. Steps: '
        f'{html.escape(", ".join(v[2] for v in layout.values()))}.">',
        "<defs>",
        f'<marker id="arr-{system}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#6A7078"/></marker>',
        f'<marker id="arr-on-{system}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>',
        f'<filter id="glow-{system}" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
        "</defs>",
    ]

    for src, dst, label, kind in edges:
        path, (lx, ly) = _edge_path(layout[src], layout[dst], kind)
        lit = src in visited and (dst in visited or dst == active)
        stroke = color if lit else "#6A7078"
        dash = ' stroke-dasharray="5 5"' if kind in ("bypass", "loop", "back") else ""
        marker = f"arr-on-{system}" if lit else f"arr-{system}"
        parts.append(f'<path d="{path}" fill="none" stroke="{stroke}" stroke-width="2"{dash} marker-end="url(#{marker})"/>')
        if label:
            anchor = "start" if kind == "loop" else "middle"
            parts.append(f'<text x="{lx}" y="{ly}" text-anchor="{anchor}" font-size="12" fill="#A29D92" '
                         f'font-family="IBM Plex Sans, -apple-system, sans-serif">{html.escape(label)}</text>')

    for node_id, (nx, ny, title, sub) in layout.items():
        is_active, is_done = node_id == active, node_id in visited
        fill = "#1D2023" if not (is_active or is_done) else ("#2B2719" if is_active else "#202326")
        stroke = color if (is_active or is_done) else "#5A6068"
        glow = f' filter="url(#glow-{system})"' if is_active else ""
        stroke_w = 2.4 if is_active else 1.4
        parts.append(f'<g{glow}><rect x="{nx}" y="{ny}" width="{NODE_W}" height="{NODE_H}" rx="5" '
                     f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"/>')
        if is_active:
            parts.append(f'<rect x="{nx}" y="{ny}" width="{NODE_W}" height="{NODE_H}" rx="5" fill="none" stroke="{color}" '
                         'stroke-width="2"><animate attributeName="opacity" values="1;0.25;1" dur="1.4s" repeatCount="indefinite"/></rect>')
        parts.append("</g>")
        title_color = "#F2EDE2" if (is_active or is_done) else "#D6D1C6"
        parts.append(f'<text x="{nx + 14}" y="{ny + 25}" font-size="15" font-weight="600" fill="{title_color}" '
                     f'font-family="IBM Plex Sans, -apple-system, sans-serif">{html.escape(title)}</text>')
        for i, line in enumerate(sub):
            parts.append(f'<text x="{nx + 14}" y="{ny + 45 + i * 15}" font-size="12" fill="#A29D92" '
                         f'font-family="IBM Plex Sans, -apple-system, sans-serif">{html.escape(line)}</text>')
        if node_id in timings and not is_active:
            secs, runs = timings[node_id]
            label = _fmt_secs(secs) + (f" ×{runs}" if runs > 1 else "")
            parts.append(f'<text x="{nx + NODE_W - 2}" y="{ny - 6}" text-anchor="end" font-size="11.5" fill="{color}" '
                         f'font-family="IBM Plex Mono, ui-monospace, monospace">{html.escape(label)}</text>')
        if is_done and not is_active and not static:
            parts.append(f'<circle cx="{nx + NODE_W - 16}" cy="{ny + 18}" r="7" fill="{color}"/>'
                         f'<path d="M{nx + NODE_W - 19.5},{ny + 18} l2.5,2.5 l4.5,-5" stroke="#17191B" stroke-width="2" fill="none"/>')
        # "i" marker: hovering the step shows what it does
        parts.append(f'<circle cx="{nx + NODE_W - 14}" cy="{ny + NODE_H - 14}" r="7" fill="none" stroke="#6E6A63" stroke-width="1.2"/>'
                     f'<text x="{nx + NODE_W - 14}" y="{ny + NODE_H - 10.5}" text-anchor="middle" font-size="10" font-weight="600" '
                     f'fill="#A29D92" font-family="Georgia, serif">i</text>')

    # Hover layer, drawn last so the tip sits above every node and edge
    for node_id, (nx, ny, title, _) in layout.items():
        info = node_info(system, node_id)
        if not info:
            continue
        lines = _wrap(info)
        tip_w, tip_h = 252, 26 + 15 * len(lines)
        tx = max(4, min(nx, width - tip_w - 4))
        ty = ny + NODE_H + 8 if ny + NODE_H + 8 + tip_h <= height else ny - tip_h - 8
        text = "".join(f'<tspan x="{tx + 12}" dy="{15 if i else 0}">{html.escape(l)}</tspan>' for i, l in enumerate(lines))
        parts.append(
            f'<g class="nodetip" tabindex="0" role="note" aria-label="{html.escape(title)}: {html.escape(info)}"><title>{html.escape(title)}: {html.escape(info)}</title>'
            f'<rect class="hit" x="{nx}" y="{ny}" width="{NODE_W}" height="{NODE_H}" rx="5"/>'
            f'<g class="tip"><rect x="{tx}" y="{ty}" width="{tip_w}" height="{tip_h}" rx="4" fill="#26292D" stroke="{color}" stroke-width="1"/>'
            f'<text x="{tx + 12}" y="{ty + 20}" font-size="12" fill="#ECE7DC" font-family="{FONT}">{text}</text></g></g>'
        )

    parts.append("</svg>")
    cap = f'<div class="small muted" style="padding:6px 4px 2px">{html.escape(caption)}</div>' if caption else ""
    return f'<div class="diagram">{"".join(parts)}{cap}</div>'
