"""Colours, type, system labels and the page stylesheet shared by every page.

Look: an annual report read at night. Warm ink background, an editorial serif (Newsreader) for headings and
answers, IBM Plex Sans for the interface and IBM Plex Mono for figures and filing excerpts; brass is the one accent.
"""

import streamlit as st

SYSTEMS = ["system_c_v3", "system_c_v2", "system_c_v1", "system_b", "system_a"]
SYSTEM_ORDER = ["system_a", "system_b", "system_c_v1", "system_c_v2", "system_c_v3"]

SYSTEM_INFO = {
    "system_a": {"short": "A", "name": "System A", "tagline": "Vanilla dense", "color": "#8F969E",
                 "blurb": "One dense search, one LLM answer."},
    "system_b": {"short": "B", "name": "System B", "tagline": "Hybrid + rerank", "color": "#7AA2C8",
                 "blurb": "BM25 + dense fusion, cross-encoder rerank, one pass."},
    "system_c_v1": {"short": "C v1", "name": "System C v1", "tagline": "Adaptive multi-hop", "color": "#86B79A",
                    "blurb": "Searches, checks, searches again until the critic is satisfied."},
    "system_c_v2": {"short": "C v2", "name": "System C v2", "tagline": "Agentic + XBRL", "color": "#CF8F69",
                    "blurb": "Adds a lookup of reported XBRL figures that can end the search early."},
    "system_c_v3": {"short": "C v3", "name": "System C v3", "tagline": "Schema-aware", "color": "#D9B45F",
                    "blurb": "Uses XBRL only for headline metrics and checks every line item is found."},
}

SERIF = "'Newsreader', Georgia, 'Times New Roman', serif"
SANS = "'IBM Plex Sans', -apple-system, 'Segoe UI', sans-serif"
MONO = "'IBM Plex Mono', ui-monospace, Menlo, monospace"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&display=swap');

:root {
  --bg: #111213; --surface: #17191B; --surface-2: #1D2023; --border: #2A2E32; --rule: #34393E;
  --text: #ECE7DC; --muted: #A29D92; --faint: #74706A;
  --accent: #D9B45F; --accent-ink: #1A1508;
  --ok: #8CC09B; --warn: #E0A85A; --bad: #D9806F;
  --radius: 6px;
  --serif: SERIF_; --sans: SANS_; --mono: MONO_;
}

/* Type: Plex for the interface, Newsreader for headings. Icon fonts are left alone. */
html, body, .stApp, [data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"], .stButton button,
.stTextArea textarea, .stTextInput input, [data-baseweb="select"], [data-testid="stCaptionContainer"],
[data-testid="stExpander"] summary p, button[role="tab"] p, [data-testid="stMetric"] {
  font-family: var(--sans) !important;
}
h1, h2, h3, h4, h5, .serif { font-family: var(--serif) !important; font-weight: 500 !important; letter-spacing: -0.005em; }
[data-testid="stMarkdownContainer"] h4 { font-size: 1.35rem; }
[data-testid="stMarkdownContainer"] h5 { font-size: 1.08rem; margin-top: .6rem; }
code, .mono { font-family: var(--mono) !important; }

.block-container { padding-top: 1.4rem; padding-bottom: 4rem; max-width: 1140px; }
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none; }
header[data-testid="stHeader"] { background: transparent; height: 0; }
[data-testid="stToolbar"] { display: none; }

/* Masthead */
.masthead { display: flex; align-items: baseline; gap: 14px; flex-wrap: wrap; }
.masthead .name { font-family: var(--serif); font-size: 1.45rem; color: var(--text); }
.masthead .meta { font-size: .78rem; color: var(--muted); letter-spacing: .04em; }
.top-rule { border-top: 1px solid var(--rule); margin: 6px 0 18px; }

/* Navigation: segmented control drawn as plain text tabs with an underline */
div[data-testid="stButtonGroup"] { gap: 0; }
button[data-testid^="stBaseButton-segmented_control"] {
  background: transparent !important; border: none !important; border-radius: 0 !important; box-shadow: none !important;
  color: var(--muted) !important; padding: 6px 12px !important; border-bottom: 2px solid transparent !important;
}
button[data-testid="stBaseButton-segmented_controlActive"] {
  color: var(--text) !important; border-bottom: 2px solid var(--accent) !important;
}
button[data-testid^="stBaseButton-segmented_control"]:hover { color: var(--text) !important; }
button[data-testid^="stBaseButton-segmented_control"] p { font-weight: 500 !important; }

/* Pills (examples) as quiet rectangular tags */
button[data-testid^="stBaseButton-pills"] { border-radius: 4px !important; border-color: var(--border) !important; }
button[data-testid="stBaseButton-pillsActive"] { border-color: var(--accent) !important; color: var(--text) !important;
  background: rgba(217,180,95,.10) !important; }

.stButton button[kind="primary"] { background: var(--accent) !important; color: var(--accent-ink) !important; border: none !important;
  border-radius: 4px !important; font-weight: 600 !important; padding: .45rem 1.6rem !important; }
.stButton button[kind="primary"]:disabled { background: var(--surface-2) !important; color: var(--faint) !important; }
.stButton button[kind="secondary"] { border-radius: 4px !important; }

/* Hero */
.hero { padding: 2px 0 10px; }
.eyebrow { font-size: .72rem; font-weight: 600; letter-spacing: .14em; text-transform: uppercase; color: var(--accent); margin-bottom: 8px; }
.hero h1 { font-size: 2.35rem; line-height: 1.12; margin: 0 0 10px; padding: 0; color: var(--text); }
.hero p { color: var(--muted); font-size: 1.02rem; line-height: 1.6; margin: 0; max-width: 720px; }
.sys-note { font-size: .82rem; color: var(--accent); padding-bottom: 10px; text-align: right; }

/* Figures row */
.stat-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); margin: 14px 0 6px;
  border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); }
.stat { padding: 12px 14px 11px; border-left: 1px solid var(--border); }
.stat:first-child { border-left: none; padding-left: 2px; }
.stat .v { font-family: var(--mono); font-size: 1.2rem; color: var(--text); font-variant-numeric: tabular-nums; }
.stat .l { font-size: .74rem; color: var(--muted); margin-top: 3px; letter-spacing: .02em; }

.card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 18px 20px; margin-bottom: 12px; }
.card h4 { margin: 0 0 6px; font-size: 1.05rem; }
.muted { color: var(--muted); }
.small { font-size: .84rem; }

.tag { display: inline-block; padding: 2px 8px; border-radius: 3px; font-size: .74rem; font-weight: 500;
  border: 1px solid var(--border); color: var(--muted); background: transparent; }
.tag.ok { color: var(--ok); border-color: rgba(140,192,155,.4); }
.tag.warn { color: var(--warn); border-color: rgba(224,168,90,.4); }
.tag.bad { color: var(--bad); border-color: rgba(217,128,111,.4); }
.swatch { width: 9px; height: 9px; border-radius: 2px; display: inline-block; margin-right: 6px; vertical-align: 0; }

/* Answer: reads like a report paragraph */
.answer { background: var(--surface); border: 1px solid var(--border); border-top: 2px solid var(--accent);
  border-radius: var(--radius); padding: 18px 22px 16px; }
.answer-head { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.answer-head .title { font-size: .76rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); }
.answer-body { font-family: var(--serif); font-size: 1.22rem; line-height: 1.62; color: var(--text); }
.answer-body p { margin: 0 0 10px; }
.sent.flag { box-shadow: inset 0 -2px 0 rgba(224,168,90,.5); }
.cite { display: inline-flex; align-items: center; justify-content: center; min-width: 18px; height: 18px; padding: 0 4px;
  margin: 0 1px 0 2px; border-radius: 3px; font-family: var(--mono); font-size: .68rem; font-weight: 500; vertical-align: 3px;
  text-decoration: none !important; color: var(--accent-ink) !important; background: var(--accent); }
.cite.xbrl { background: #9FB7C9; }
.num-ok { color: var(--ok); border-bottom: 1px dotted rgba(140,192,155,.7); }
.num-bad { color: var(--warn); border-bottom: 1px dotted rgba(224,168,90,.8); }

/* Source cards: filing excerpts */
.src { border-bottom: 1px solid var(--border); }
.src:first-of-type { border-top: 1px solid var(--border); }
.src summary { list-style: none; cursor: pointer; padding: 10px 2px; display: flex; gap: 12px; align-items: baseline; }
.src summary::-webkit-details-marker { display: none; }
.src summary:hover .t1 { color: var(--accent); }
.src summary .meta { flex: 1; min-width: 0; }
.src summary .t1 { font-weight: 500; font-size: .92rem; }
.src summary .t2 { color: var(--faint); font-size: .76rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.src .body { margin: 0 0 12px 30px; padding: 12px 14px; background: var(--surface); border-left: 2px solid var(--accent);
  font-family: var(--mono); font-size: .78rem; line-height: 1.6; color: #CFC9BC; white-space: pre-wrap; max-height: 320px; overflow-y: auto; }
.src mark { background: rgba(140,192,155,.2); color: var(--ok); padding: 0 2px; }
.src.uncited .body { border-left-color: var(--rule); }
.src .body.prose { font-family: var(--sans); font-size: .86rem; line-height: 1.65; color: #D6D1C6; }
.src .body table.xbrl { border-collapse: collapse; width: auto; min-width: 280px; white-space: normal; }
.src .body table.xbrl td { padding: 3px 18px 3px 0; border-bottom: 1px dotted var(--border); }

/* Hop trace */
.hop { border-left: 1px solid var(--rule); padding: 0 0 12px 16px; margin-left: 4px; position: relative; }
.hop:before { content: ""; position: absolute; left: -4px; top: 6px; width: 7px; height: 7px; background: var(--accent); }
.hop .h { font-weight: 500; font-size: .88rem; }
.hop .q { color: var(--muted); font-family: var(--serif); font-size: .95rem; font-style: italic; }

.diagram { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 12px 12px 6px; overflow-x: auto; }
.diagram svg { display: block; width: 100%; height: auto; min-width: 640px; }
.diagram .nodetip .hit { fill: transparent; pointer-events: all; cursor: help; }
.diagram .nodetip .tip { opacity: 0; pointer-events: none; transition: opacity .12s ease-in; }
.diagram .nodetip:hover .tip { opacity: 1; }

/* Live run bar: what the run is waiting on, with CSS-only second counters (no reruns needed while a step runs) */
@property --sec { syntax: '<integer>'; inherits: false; initial-value: 0; }
@keyframes tick { from { --sec: 0; } to { --sec: 3600; } }
.tick { animation: tick 3600s linear forwards; counter-reset: sec var(--sec); font-family: var(--mono); font-variant-numeric: tabular-nums; }
.tick::after { content: counter(sec) "s"; }
.runbar { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 14px; padding: 10px 14px; margin-bottom: 8px;
  background: var(--surface); border: 1px solid var(--border); border-left: 2px solid var(--accent); border-radius: var(--radius); font-size: .9rem; }
.runbar .now { color: var(--text); }
.runbar .now b { font-weight: 600; }
.runbar .wait { color: var(--muted); }
.runbar .clock { margin-left: auto; color: var(--muted); font-size: .82rem; }
.runbar .clock .tick { color: var(--accent); }
.runbar .pulse { width: 8px; height: 8px; border-radius: 50%; background: var(--accent); animation: pulse 1.2s ease-in-out infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .25; } }
.runbar.done .pulse { animation: none; background: var(--ok); }

.rq { border-top: 2px solid var(--accent); padding: 12px 2px 4px; height: 100%; }
.rq .k { font-size: .72rem; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; color: var(--accent); }
.rq .q { font-family: var(--serif); font-size: 1.25rem; margin: 6px 0 8px; }
.rq .a { color: var(--muted); font-size: .9rem; line-height: 1.55; }
.note { border-left: 2px solid var(--warn); padding: 8px 14px; color: #E2D3B0; font-size: .88rem; margin: 18px 0 14px; background: rgba(224,168,90,.05); }

.footer { color: var(--faint); font-size: .78rem; margin-top: 40px; border-top: 1px solid var(--rule); padding-top: 14px; }
</style>
""".replace("SERIF_", SERIF).replace("SANS_", SANS).replace("MONO_", MONO)


def apply_theme() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def system_pill(system: str) -> str:
    info = SYSTEM_INFO[system]
    return (f'<span class="tag"><span class="swatch" style="background:{info["color"]}"></span>'
            f'{info["name"]} · {info["tagline"]}</span>')
