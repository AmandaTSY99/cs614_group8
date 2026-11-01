"""The four pages of the demo: Ask, Benchmark explorer, Results and How it works."""

import html
from typing import Any, Dict, List, Optional

import altair as alt
import pandas as pd
import streamlit as st

from ui import live
from ui.citations import render_answer
from ui.data import COMPANIES, RECIPE_LABELS, benchmark_by_question, load_benchmark, load_rq1, load_rq2, load_rq3, question_companies
from ui.diagrams import render_diagram
from ui.theme import SYSTEM_INFO, SYSTEM_ORDER, SYSTEMS, system_pill

PAGES = ["Ask", "Benchmark explorer", "Results", "How it works"]

EXAMPLES = [
    ("NVIDIA gross margin, FY16 → FY22", "By how many percentage points did NVIDIA's gross margin increase from fiscal year 2016 to fiscal year 2022?"),
    ("Tesla total assets, FY21 → FY25", "By how many million dollars did Tesla's total assets increase from fiscal year 2021 to fiscal year 2025?"),
    ("Microsoft Level 3 valuation", "According to Microsoft's fiscal year 2019 10-K, what valuation methodology does the company use for its Level 3 investments?"),
    ("Microsoft operating income, FY16 → FY19", "By how much did Microsoft's operating income increase in fiscal year 2019 compared to fiscal year 2016 (in millions)?"),
]


def _fmt_ms(ms: Optional[float]) -> str:
    return "–" if ms is None else (f"{ms / 1000:.1f} s" if ms >= 1000 else f"{ms:.0f} ms")


def _clip(text: str, n: int = 140) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def _go_to(page: str, question_id: Optional[str] = None) -> None:
    st.session_state["nav"] = page
    if question_id:
        st.session_state["explore_qid"] = question_id


def _stats(items: List[tuple]) -> str:
    cells = "".join(f'<div class="stat"><div class="v">{html.escape(str(v))}</div><div class="l">{html.escape(l)}</div></div>'
                    for v, l in items)
    return f'<div class="stat-row">{cells}</div>'


def _show_run(run: Dict[str, Any], heading: str, key: str) -> None:
    parts = render_answer(run, heading=heading)
    st.markdown(parts["answer"], unsafe_allow_html=True)
    st.markdown(_stats([
        (run.get("hops", 1), "retrieval hops"),
        (_fmt_ms(run.get("latency_ms")), "end-to-end latency"),
        (f'{int(run.get("tokens") or 0):,}', "tokens"),
        (f'${float(run.get("cost_usd") or 0):.4f}', "cost (gpt-5.4 rates)"),
    ]), unsafe_allow_html=True)
    st.markdown(f"##### Sources cited ({parts['n_sources']})")
    st.caption("Each numbered chip in the answer links to the exact 10-K chunk below. Green figures were found in "
               "(or computed from) the cited chunk by the guardrail; amber ones were not.")
    st.markdown(parts["sources"], unsafe_allow_html=True)
    if int(parts["n_uncited"]):
        with st.expander(f"Also retrieved but not cited ({parts['n_uncited']} chunks)"):
            st.markdown(parts["uncited"], unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Ask
# ---------------------------------------------------------------------------


def page_ask() -> None:
    st.markdown(
        '<div class="hero"><div class="eyebrow">Ask a 10-K question</div>'
        "<h1>Answers you can check, line by line</h1>"
        "<p>System C searches SEC 10-K filings in several hops until a critic is satisfied, then writes an answer where "
        "every sentence cites the filing chunk it came from and every number is checked against that chunk.</p></div>",
        unsafe_allow_html=True,
    )

    system = st.segmented_control(
        "System", SYSTEMS, default="system_c_v3", key="ask_system", format_func=lambda s: SYSTEM_INFO[s]["short"],
    ) or "system_c_v3"
    recommended = ' <span style="color:var(--accent)">Recommended: the most accurate system in our benchmark.</span>'
    st.markdown(f'<div class="small muted" style="margin:-6px 0 12px">{html.escape(SYSTEM_INFO[system]["name"])} · '
                f'{html.escape(SYSTEM_INFO[system]["blurb"])}{recommended if system == "system_c_v3" else ""}</div>',
                unsafe_allow_html=True)

    st.session_state.setdefault("ask_question", EXAMPLES[0][1])
    example = st.pills("Try an example", [e[1] for e in EXAMPLES], key="ask_example",
                       format_func=lambda q: next(lbl for lbl, text in EXAMPLES if text == q))
    if example and st.session_state.get("ask_last_example") != example:
        st.session_state["ask_question"] = example
        st.session_state["ask_last_example"] = example
    question = st.text_area("Your question", key="ask_question", height=90,
                            placeholder="e.g. How much did Tesla's total assets grow between FY2021 and FY2025?")

    space = live.space_providers()
    with st.expander("Model and API key"):
        s1, s2, s3 = st.columns(3)
        names = list(live.PROVIDERS)
        provider = s1.selectbox("Provider", names, index=names.index(space[0]) if space else 0,
                                format_func=lambda p: live.PROVIDERS[p]["label"] + ("" if live.space_has_key(p) else " (bring your own key)"))
        model = s2.selectbox("Model", live.PROVIDERS[provider]["models"])
        max_hops = s3.slider("Max hops (System C)", 1, 3, 3)
        api_key = st.text_input(f"Your {live.PROVIDERS[provider]['label']} API key (optional)", type="password",
                                help="Used only for your own questions, only while they run. It is not stored or shared.")
        if live.space_has_key(provider):
            st.caption(f"Leave blank to use this demo's {live.PROVIDERS[provider]['label']} key. "
                       "Benchmark results were produced with OpenAI gpt-5.4, so other models may answer differently.")
        else:
            st.caption(f"This demo has no {live.PROVIDERS[provider]['label']} key; paste your own to use it.")

    # Attempts: the visitor's own key only; otherwise this demo's key for the chosen provider, then its other keys.
    if api_key.strip():
        attempts = [(provider, model, api_key)]
    elif live.space_has_key(provider):
        attempts = [(provider, model, "")] + [(p, live.PROVIDERS[p]["models"][0], "") for p in space if p != provider]
    else:
        attempts = []
    ready = bool(attempts) and live.database_ready()
    run_clicked = st.button("Ask", type="primary", disabled=not (ready and question.strip()))
    if not ready:
        missing = [] if attempts else [f"an API key for {live.PROVIDERS[provider]['label']}"]
        missing += [] if live.database_ready() else ["the Supabase connection (SUPABASE_DB_URL)"]
        st.info(f"Live answers need {' and '.join(missing)}. You can still browse all 485 benchmark answers, "
                "with their citations, in the Benchmark explorer.")
        st.button("Open the Benchmark explorer", on_click=_go_to, args=("Benchmark explorer",))

    diagram_slot = st.empty()
    status_slot = st.empty()
    if not run_clicked and "live_result" not in st.session_state:
        diagram_slot.markdown(render_diagram(system), unsafe_allow_html=True)

    if run_clicked:
        scope = live.detect_scope(question)
        if system not in live.C_MODES and not (scope[0] and scope[1]):
            st.warning("Single-pass systems search only the filings you name. Include a company and a fiscal year "
                       "(e.g. “Microsoft fiscal year 2019”), or use System C, which works them out itself.")
            st.stop()
        errors = []
        for attempt_provider, attempt_model, attempt_key in attempts:
            try:
                with live.llm_session(attempt_provider, attempt_model, attempt_key):
                    run = _execute(system, question, max_hops, scope, diagram_slot, status_slot,
                                   f"{live.PROVIDERS[attempt_provider]['label']} · {attempt_model}")
                run["model_used"] = f"{live.PROVIDERS[attempt_provider]['label']} · {attempt_model}"
                if errors:
                    run["fallback_note"] = f"{errors[-1][0]} failed, so this answer used {run['model_used']}."
                st.session_state["live_result"] = {"question": question.strip(), "system": system, "run": run}
                break
            except Exception as exc:  # provider limits, bad keys, database errors
                errors.append((live.PROVIDERS[attempt_provider]["label"], exc))
        else:
            status_slot.empty()
            st.error(f"The run failed: {errors[-1][1]}" if errors else "The run failed.")
            with st.expander("Technical details"):
                for label, exc in errors:
                    st.markdown(f"**{label}**")
                    st.exception(exc)

    result = st.session_state.get("live_result")
    if not result:
        return
    rsys, run = result["system"], result["run"]
    diagram_slot.empty()

    if run.get("fallback_note"):
        st.info(run["fallback_note"])
    left, right = st.columns([5, 2], gap="large")
    with left:
        _show_run(run, f"{SYSTEM_INFO[rsys]['name']} answer" + (f" · {run['model_used']}" if run.get("model_used") else ""), key="live")
    with right:
        bench = benchmark_by_question().get(result["question"].lower())
        if bench:
            _benchmark_check(bench)
        if run.get("trace"):
            st.markdown("##### How it got there")
            st.markdown(_trace_html(run["trace"]), unsafe_allow_html=True)
    st.markdown("##### Path through the system")
    st.markdown(render_diagram(rsys, visited=run.get("visited", [])), unsafe_allow_html=True)


def _execute(system, question, max_hops, scope, diagram_slot, status_slot, model_label) -> Dict[str, Any]:
    """Run one system live, updating the diagram and the status log as it goes."""
    name = SYSTEM_INFO[system]["name"]
    if system not in live.C_MODES:
        diagram_slot.markdown(render_diagram(system, active="retrieve", visited=["question"]), unsafe_allow_html=True)
        with status_slot.status(f"Running {name} on {model_label}…", expanded=False) as status:
            run = live.run_single_pass(question, system, scope)
            status.update(label=f"Done in {_fmt_ms(run['latency_ms'])} · {model_label}", state="complete")
        return run

    diagram_slot.markdown(render_diagram(system, active="decomposer"), unsafe_allow_html=True)
    with status_slot.status(f"Running {name} on {model_label}…", expanded=True) as status:
        def on_step(node, nxt, visited, state):
            diagram_slot.markdown(render_diagram(system, active=nxt, visited=visited), unsafe_allow_html=True)
            hop = state.get("current_hop", 1)
            msg = {
                "decomposer": f"Planned the search for {', '.join(state.get('target_tickers') or []) or 'the named companies'}",
                "tabular_tool": "Added reported XBRL figures to the evidence",
                "retriever": f"Hop {hop}: {len(state.get('accumulated_evidence') or [])} chunks gathered so far",
                "critic": (f"Hop {hop}: evidence judged sufficient" if state.get("is_sufficient")
                           else f"Hop {hop}: still missing {_clip((state.get('missing_premises') or ['details'])[0])}"),
                "generator": f"Follow-up query: “{_clip(state.get('current_sub_query', ''))}”",
                "synthesizer": f"Drafted the answer with {len(state.get('citations') or [])} citations",
                "guardrail": "Checked every number against its cited chunk",
                "repair": "Repaired a figure the guardrail could not verify",
            }.get(node)
            if msg:
                status.write(msg)
        run = live.run_system_c(question, system, max_hops=max_hops, on_step=on_step, scope=scope)
        status.update(label=f"Done in {_fmt_ms(run['latency_ms'])} · {run['hops']} hop(s) · {model_label}",
                      state="complete", expanded=False)
    return run


def _trace_html(trace: List[Dict[str, Any]]) -> str:
    out = []
    for step in trace:
        k = step["kind"]
        if k == "plan":
            route = "XBRL lookup, then text search" if step.get("xbrl") else "text search"
            who = ", ".join(step.get("tickers") or []) or "auto"
            yrs = ", ".join(f"FY{y}" for y in step.get("years") or []) or "auto"
            out.append(f'<div class="hop"><div class="h">Plan</div><div class="small muted">{html.escape(who)} · {html.escape(yrs)} · {route}</div></div>')
        elif k == "xbrl":
            out.append('<div class="hop"><div class="h">XBRL lookup</div><div class="small muted">Reported figures added as [F-…] evidence</div></div>')
        elif k == "retrieve":
            out.append(f'<div class="hop"><div class="h">Hop {step["hop"]} search</div><div class="q">“{html.escape(step["query"][:160])}”</div>'
                       f'<div class="small muted">{step["total"]} chunks in evidence</div></div>')
        elif k == "critic":
            verdict = "enough evidence" if step["sufficient"] else ("hop budget reached" if step["budget_hit"] else "gaps remain")
            miss = f'<div class="small muted">Missing: {html.escape(_clip("; ".join(step["missing"]), 220))}</div>' if step["missing"] and not step["sufficient"] else ""
            out.append(f'<div class="hop"><div class="h">Critic · {step["score"]:.2f} · {verdict}</div>{miss}</div>')
        elif k == "repair":
            out.append('<div class="hop"><div class="h">Guardrail repair</div><div class="small muted">Rewrote an unverified figure</div></div>')
    return "".join(out)


def _benchmark_check(bench: Dict[str, Any]) -> None:
    rows = []
    for s in SYSTEM_ORDER:
        r = bench["runs"].get(s) or {}
        ok = r.get("lenient_correct")
        mark = "✓" if ok else ("–" if ok is None else "✗")
        rows.append(f'<div style="display:flex;justify-content:space-between;padding:3px 0">'
                    f'<span><span class="swatch" style="background:{SYSTEM_INFO[s]["color"]}"></span> {SYSTEM_INFO[s]["name"]}</span>'
                    f'<span>{mark}</span></div>')
    st.markdown(
        f'<div class="card"><h4>This is benchmark question {html.escape(bench["id"])}</h4>'
        f'<div class="small muted">Gold answer</div><div style="margin:2px 0 10px;font-weight:600">{html.escape(str(bench["gold_answer"]))[:300]}</div>'
        f'<div class="small muted" style="margin-bottom:4px">Recorded benchmark runs (lenient scorer)</div>{"".join(rows)}</div>',
        unsafe_allow_html=True,
    )
    st.button("Compare all five answers", on_click=_go_to, args=("Benchmark explorer", bench["id"]), use_container_width=True)


# ---------------------------------------------------------------------------
# Benchmark explorer
# ---------------------------------------------------------------------------


def page_explore() -> None:
    st.markdown(
        '<div class="hero"><div class="eyebrow">Benchmark explorer</div>'
        "<h1>97 questions, five systems, every source</h1>"
        "<p>These are the recorded answers from our evaluation (gpt-5.4, temperature 0). Pick a question to compare what each "
        "system retrieved, what it cited, and whether it got the number right.</p></div>",
        unsafe_allow_html=True,
    )
    questions = load_benchmark()
    f1, f2, f3 = st.columns(3)
    company = f1.selectbox("Company", ["All"] + sorted(COMPANIES), format_func=lambda t: "All companies" if t == "All" else f"{COMPANIES[t]} ({t})")
    recipe = f2.selectbox("Question type", ["All"] + list(RECIPE_LABELS), format_func=lambda r: "All types" if r == "All" else RECIPE_LABELS[r])
    outcome = f3.selectbox("Outcome", ["All", "v3 right, v1 wrong", "Single-pass wrong, C v3 right", "Any system wrong"])

    def keep(q):
        runs = q["runs"]
        ok = {s: runs.get(s, {}).get("lenient_correct") for s in SYSTEM_ORDER}
        if company != "All" and company not in question_companies(q):
            return False
        if recipe != "All" and q.get("recipe") != recipe:
            return False
        if outcome == "v3 right, v1 wrong":
            return ok["system_c_v3"] is True and ok["system_c_v1"] is False
        if outcome == "Single-pass wrong, C v3 right":
            return ok["system_c_v3"] is True and ok["system_a"] is False and ok["system_b"] is False
        if outcome == "Any system wrong":
            return any(v is False for v in ok.values())
        return True

    shown = [q for q in questions if keep(q)]
    if not shown:
        st.info("No questions match these filters.")
        return
    ids = [q["id"] for q in shown]
    wanted = st.session_state.get("explore_qid", "gold-073")
    qid = st.selectbox(f"Question ({len(shown)} shown)", ids, index=ids.index(wanted) if wanted in ids else 0,
                       format_func=lambda i: f"{i} · " + next(q["question"] for q in shown if q["id"] == i)[:120])
    st.session_state["explore_qid"] = qid
    q = next(x for x in shown if x["id"] == qid)

    tags = " ".join(f'<span class="tag">{html.escape(t)}</span>' for t in
                    [RECIPE_LABELS.get(q.get("recipe"), q.get("recipe") or ""), f'{q.get("hop", "")}-hop', q.get("type") or ""] +
                    [COMPANIES.get(t, t) for t in question_companies(q)] if t)
    st.markdown(
        f'<div class="card"><div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px">{tags}</div>'
        f'<div style="font-size:1.12rem;font-weight:650;line-height:1.45">{html.escape(q["question"])}</div>'
        f'<div style="margin-top:12px" class="small muted">Gold answer</div>'
        f'<div style="font-weight:600;color:var(--ok)">{html.escape(str(q.get("gold_answer") or ""))}</div></div>',
        unsafe_allow_html=True,
    )
    if q.get("gold_evidence"):
        with st.expander(f"Where the gold answer comes from ({len(q['gold_evidence'])} passages)"):
            for ev in q["gold_evidence"]:
                st.markdown(f"**{ev.get('ticker')} FY{ev.get('year')}** · {ev.get('item') or ''} · *{ev.get('heading') or ''}*")
                st.markdown("> " + (ev.get("quote") or "").replace("$", "\\$"))

    cols = st.columns(5)
    for col, s in zip(cols, SYSTEM_ORDER):
        r = q["runs"].get(s) or {}
        ok = r.get("lenient_correct")
        verdict = ('<span class="tag ok">Correct</span>' if ok else
                   '<span class="tag">Not scored</span>' if ok is None else '<span class="tag bad">Wrong</span>')
        col.markdown(
            f'<div class="card" style="padding:12px 14px;border-top:3px solid {SYSTEM_INFO[s]["color"]}">'
            f'<div style="font-weight:700">{SYSTEM_INFO[s]["name"]}</div>'
            f'<div class="small muted" style="margin-bottom:8px">{SYSTEM_INFO[s]["tagline"]}</div>{verdict}'
            f'<div class="small muted" style="margin-top:8px">{r.get("hops", 1)} hop · {_fmt_ms(r.get("latency_ms"))} · '
            f'{len(r.get("citations") or [])} cites</div></div>',
            unsafe_allow_html=True,
        )
    st.caption("Correct = lenient scorer (a number in the answer within 1% of the gold figure). Qualitative questions are not scored. "
               "Citations and number checks are shown exactly as recorded during the evaluation.")

    tabs = st.tabs([SYSTEM_INFO[s]["name"] for s in SYSTEMS])
    for tab, s in zip(tabs, SYSTEMS):
        with tab:
            r = q["runs"].get(s)
            if r:
                _show_run(r, f"{SYSTEM_INFO[s]['name']} answer", key=f"ex_{s}")
            else:
                st.info("No recorded run for this system.")


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------

LABELS = {s: SYSTEM_INFO[s]["name"] for s in SYSTEM_ORDER}
COLOR_SCALE = alt.Scale(domain=[LABELS[s] for s in SYSTEM_ORDER], range=[SYSTEM_INFO[s]["color"] for s in SYSTEM_ORDER])


def _style(chart: alt.Chart) -> alt.Chart:
    return (chart.configure_view(strokeWidth=0).configure(background="transparent")
            .configure_axis(labelColor="#A29D92", titleColor="#A29D92", gridColor="#25292D", domainColor="#3A3F45", labelFontSize=12,
                            labelFont="IBM Plex Sans", titleFont="IBM Plex Sans", titleFontWeight=500)
            .configure_legend(labelColor="#D6D1C6", titleColor="#A29D92", labelFont="IBM Plex Sans", orient="bottom", columns=3, labelLimit=160))


def _bar_ci(df: pd.DataFrame, value_title: str, fmt: str = ".0%", domain=(0, 1)) -> alt.Chart:
    base = alt.Chart(df).encode(y=alt.Y("system:N", sort=[LABELS[s] for s in SYSTEM_ORDER], title=None))
    bars = base.mark_bar(cornerRadiusEnd=2, height=20).encode(
        x=alt.X("mean:Q", title=value_title, scale=alt.Scale(domain=domain), axis=alt.Axis(format=fmt)),
        color=alt.Color("system:N", scale=COLOR_SCALE, legend=None),
        tooltip=[alt.Tooltip("system:N", title="System"), alt.Tooltip("mean:Q", format=fmt),
                 alt.Tooltip("ci_low:Q", format=fmt, title="95% CI low"), alt.Tooltip("ci_high:Q", format=fmt, title="95% CI high")])
    rules = base.mark_rule(color="#ECE7DC", opacity=0.75).encode(x="ci_low:Q", x2="ci_high:Q")
    labels = base.mark_text(align="left", dx=6, color="#ECE7DC", fontSize=12, font="IBM Plex Mono").encode(x="ci_high:Q", text=alt.Text("mean:Q", format=fmt))
    return _style((bars + rules + labels).properties(height=190))


def page_results() -> None:
    rq3 = load_rq3()
    sysm = rq3["systems"]
    rq2 = load_rq2()
    rq1 = load_rq1()
    st.markdown(
        '<div class="hero"><div class="eyebrow">Results</div>'
        "<h1>Does searching in several steps beat searching once?</h1>"
        "<p>Same 97 questions, same answer model (gpt-5.4), five retrieval designs: 485 recorded runs. "
        "Three research questions follow the path from retrieval, to the answer, to the bill.</p></div>",
        unsafe_allow_html=True,
    )
    be = rq3["break_even_usd"]
    rq_cards = [
        ("RQ1 · Retrieval", "Does it retrieve all the evidence?",
         "Yes, multi-hop finds far more: context recall 0.91 for C v1 and v3 vs 0.73 for System B, and only 3% of questions "
         "come back with no gold evidence (16% for A and B)."),
        ("RQ2 · Grounding", "Is the answer right and traceable?",
         f"C v3 gets {sysm['system_c_v3']['accuracy']['strict_numeric_correct_pct']:.0f}% of questions fully right on the strict scorer "
         f"(vs {sysm['system_a']['accuracy']['strict_numeric_correct_pct']:.0f}% for A) and cites a source in every answer."),
        ("RQ3 · Economics", "Is the overhead worth paying?",
         f"Multi-hop costs about 6–10× more per query. C v3 becomes the cheapest system overall once a wrong answer costs "
         f"more than ${be['a_to_v3_strict']:.2f}."),
    ]
    cols = st.columns(3)
    for col, (k, q, a) in zip(cols, rq_cards):
        col.markdown(f'<div class="rq"><div class="k">{k}</div><div class="q">{q}</div><div class="a">{a}</div></div>', unsafe_allow_html=True)
    first = rq3["v3_first_run"]
    st.markdown(
        f'<div class="note"><strong>Read v3 with care.</strong> v3’s fixes were developed on this benchmark. Its first run scored '
        f'{first["lenient_pct"]:.0f}% lenient and {first["strict_pct"]:.0f}% strict; after fixing those 8 failures and re-running the same '
        f"97 questions it reached 100% lenient and 84% strict. Treat the final numbers as an upper bound until a held-out test.</div>",
        unsafe_allow_html=True,
    )

    t1, t2, t3, t4 = st.tabs(["RQ1 · Retrieval", "RQ2 · Grounding", "RQ3 · Economics", "Full scorecard"])

    with t1:
        overall = rq1[(rq1["facet"] == "overall")].copy()
        overall["system"] = overall["system"].map(LABELS)
        a, b = st.columns(2)
        with a:
            st.markdown("##### Context recall")
            st.caption("Share of gold evidence passages found anywhere in the retrieved context.")
            st.altair_chart(_bar_ci(overall[overall["metric"] == "recall@all"], "recall"), use_container_width=True)
        with b:
            st.markdown("##### All evidence found")
            st.caption("Share of questions where every gold passage was retrieved (complete@all).")
            st.altair_chart(_bar_ci(overall[overall["metric"] == "complete@all"], "questions"), use_container_width=True)
        st.markdown("##### Where it gets hard: tables, and questions that need tables and text together")
        mod = rq1[(rq1["facet"] == "modality") & (rq1["metric"] == "complete@all")].copy()
        mod["system"] = mod["system"].map(LABELS)
        chart = alt.Chart(mod).mark_bar(cornerRadiusEnd=2).encode(
            x=alt.X("mean:Q", title="all evidence found", axis=alt.Axis(format=".0%"), scale=alt.Scale(domain=(0, 1))),
            y=alt.Y("system:N", title=None, sort=[LABELS[s] for s in SYSTEM_ORDER], axis=None),
            color=alt.Color("system:N", scale=COLOR_SCALE, title=None),
            row=alt.Row("group:N", title=None, header=alt.Header(labelColor="#D6D1C6", labelFontSize=13, labelFont="IBM Plex Sans", labelAngle=0, labelAlign="left")),
            tooltip=["system", "group", alt.Tooltip("mean:Q", format=".0%"), "n"],
        ).properties(height=90)
        st.altair_chart(_style(chart), use_container_width=True)
        st.caption("Source: reports/rq1 (bootstrap 95% CIs). Relevance is lexical, so these are lower bounds. "
                   "System B drops on tables; even C v1 finds all table + text evidence only 58% of the time.")

    with t2:
        rows = []
        for s in SYSTEM_ORDER:
            for metric in ("numeric_accuracy", "citation_coverage", "citation_precision", "grounding_error_rate"):
                m = rq2[s][metric]
                if m["mean"] is not None:
                    rows.append({"system": LABELS[s], "metric": metric, "mean": m["mean"], "ci_low": m["ci_low"], "ci_high": m["ci_high"], "n": m["n"]})
        df = pd.DataFrame(rows)
        a, b = st.columns(2)
        with a:
            st.markdown("##### Numeric accuracy (strict)")
            st.caption("Every gold number appears in the answer (n = 63 numeric questions).")
            st.altair_chart(_bar_ci(df[df["metric"] == "numeric_accuracy"], "questions fully right"), use_container_width=True)
        with b:
            st.markdown("##### Answers that cite a source")
            st.caption("Share of the 97 answers with at least one citation.")
            st.altair_chart(_bar_ci(df[df["metric"] == "citation_coverage"], "answers"), use_container_width=True)
        a, b = st.columns(2)
        with a:
            st.markdown("##### Citation precision")
            st.caption("Cited sections that match the gold evidence sections (answers with citations).")
            st.altair_chart(_bar_ci(df[df["metric"] == "citation_precision"], "precision"), use_container_width=True)
        with b:
            st.markdown("##### Numbers the guardrail could not verify")
            st.caption("Share of figures in the answer not found in their cited chunk. Only System C has a guardrail.")
            st.altair_chart(_bar_ci(df[df["metric"] == "grounding_error_rate"], "unverified figures", domain=(0, 0.25)), use_container_width=True)
        st.caption("Scored with scripts/rq2/metrics_custom.py on the same 485 runs as RQ3. Citation precision is section-level.")

    with t3:
        econ = pd.DataFrame([{
            "system": LABELS[s],
            "p50": sysm[s]["latency"]["p50_ms"] / 1000,
            "strict": sysm[s]["accuracy"]["strict_numeric_correct_pct"] / 100,
            "cost": sysm[s]["economics"]["cost_per_1k_queries_usd"],
        } for s in SYSTEM_ORDER])
        a, b = st.columns(2)
        with a:
            st.markdown("##### Accuracy vs latency")
            st.caption("Bubble size = cost per 1,000 queries.")
            pts = alt.Chart(econ).mark_circle(opacity=0.9, stroke="#111213", strokeWidth=1).encode(
                x=alt.X("p50:Q", title="median latency (s)"), y=alt.Y("strict:Q", title="strict accuracy", axis=alt.Axis(format=".0%"), scale=alt.Scale(domain=(0.3, 0.95))),
                size=alt.Size("cost:Q", legend=None, scale=alt.Scale(range=[150, 1600])),
                color=alt.Color("system:N", scale=COLOR_SCALE, legend=None),
                tooltip=["system", alt.Tooltip("p50:Q", format=".1f", title="p50 (s)"), alt.Tooltip("strict:Q", format=".0%"), alt.Tooltip("cost:Q", format="$.2f", title="$ / 1k")])
            txt = alt.Chart(econ).mark_text(dy=-22, color="#ECE7DC", fontSize=12).encode(x="p50:Q", y="strict:Q", text="system:N")
            st.altair_chart(_style((pts + txt).properties(height=320)), use_container_width=True)
        with b:
            st.markdown("##### Which system is cheapest overall?")
            st.caption("Expected cost per query = compute cost + P(wrong) × penalty for a wrong answer.")
            pen = [i / 200 for i in range(0, 81)]
            lines = pd.DataFrame([{"penalty": p, "system": LABELS[s],
                                   "expected": sysm[s]["economics"]["mean_cost_per_query_usd"] + (1 - sysm[s]["accuracy"]["strict_numeric_correct_pct"] / 100) * p}
                                  for s in SYSTEM_ORDER for p in pen])
            ch = alt.Chart(lines).mark_line(strokeWidth=2.5).encode(
                x=alt.X("penalty:Q", title="penalty per wrong answer ($)", axis=alt.Axis(format="$.2f")),
                y=alt.Y("expected:Q", title="expected cost per query ($)", axis=alt.Axis(format="$.2f")),
                color=alt.Color("system:N", scale=COLOR_SCALE, title=None),
                tooltip=["system", alt.Tooltip("penalty:Q", format="$.2f"), alt.Tooltip("expected:Q", format="$.3f")])
            rule = alt.Chart(pd.DataFrame({"x": [be["a_to_v3_strict"]]})).mark_rule(strokeDash=[4, 4], color="#D9B45F").encode(x="x:Q")
            st.altair_chart(_style((ch + rule).properties(height=320)), use_container_width=True)
        st.markdown(_stats([
            (f"< ${be['b_to_a_strict']:.2f}", "System B is cheapest"),
            (f"${be['b_to_a_strict']:.2f} – ${be['a_to_v3_strict']:.2f}", "System A is cheapest"),
            (f"> ${be['a_to_v3_strict']:.2f}", "C v3 is cheapest"),
            ("never", "C v1 or v2 is cheapest"),
        ]), unsafe_allow_html=True)
        st.caption("Strict accuracy; compute at gpt-5.4 rates (\\$2.50 / \\$15 per million tokens). Under the lenient scorer the v3 "
                   f"threshold is about \\${be['a_to_v3_lenient']:.2f}.")
        tests = rq3["hypotheses_tests"]["pairwise_tests"]
        tdf = pd.DataFrame([{
            "Contrast": t["comparison"].replace("system_", "").replace("c_", "C ").replace("_", " ").upper().replace(" VS ", " vs "),
            "Metric": {"strict_correct": "strict accuracy", "numeric_correct": "lenient accuracy", "hops": "hops", "latency_ms": "latency"}[t["metric"]],
            "Test": "McNemar" if t.get("test") == "mcnemar_exact" else "Wilcoxon",
            "Discordant": f'{t["first_only_correct"]} / {t["second_only_correct"]}' if t.get("first_only_correct") is not None else "",
            "p (raw)": t["p_raw"], "p (Holm)": t["p_adjusted_holm"],
        } for t in tests])
        with st.expander("Paired significance tests (15 tests, Holm-corrected)"):
            st.dataframe(tdf, hide_index=True, use_container_width=True,
                         column_config={"p (raw)": st.column_config.NumberColumn(format="%.4f"), "p (Holm)": st.column_config.NumberColumn(format="%.4f")})

    with t4:
        rec = {r["system"]: r for r in rq1[(rq1["facet"] == "overall") & (rq1["metric"] == "recall@all")].to_dict("records")}
        table = {}
        for s in SYSTEM_ORDER:
            d = sysm[s]
            table[SYSTEM_INFO[s]["name"]] = {
                "Numeric accuracy, strict (n=63)": f'{d["accuracy"]["strict_numeric_correct_pct"]:.0f}%',
                "Numeric accuracy, lenient (n=87)": f'{d["accuracy"]["numeric_correct_pct"]:.0f}%' + ("*" if s == "system_c_v3" else ""),
                "Context recall (RQ1)": f'{rec[s]["mean"]:.2f}' if s in rec else "–",
                "Answers with citations (RQ2)": f'{rq2[s]["citation_coverage"]["mean"]:.0%}',
                "Median latency": f'{d["latency"]["p50_ms"] / 1000:.1f} s',
                "Mean hops": f'{d["hop_dynamics"]["mean_hops"]:.2f}',
                "Tokens per query": f'{d["tokens"]["mean_total"]:,.0f}',
                "Cost per 1,000 queries": f'${d["economics"]["cost_per_1k_queries_usd"]:.2f}',
            }
        st.dataframe(pd.DataFrame(table), use_container_width=True)
        st.caption("*In-sample. Source: reports/rq3/records.jsonl, reports/rq1, RQ2 scorer. Systems A and B repriced at gpt-5.4 rates.")


# ---------------------------------------------------------------------------
# How it works
# ---------------------------------------------------------------------------

ARCH_TEXT = {
    "system_a": ("One dense search, one answer",
                 ["Embeds the question with BGE-small and pulls up to 10 chunks, each prefixed with its company and year.",
                  "One gpt-5.4 call writes the answer and cites chunks as [n].",
                  "No checking: whatever the single search finds is all it has."]),
    "system_b": ("Hybrid search with a reranker, still one pass",
                 ["BM25 keyword scores and dense scores are min-max normalised and fused with equal weight (α = 0.5).",
                  "A cross-encoder (bge-reranker-base) re-scores the top 30 and keeps 5.",
                  "Great on exact terms (“Level 3”), weaker on tables, where the reranker demotes dense rows."]),
    "system_c_v1": ("Keeps searching until a critic is satisfied",
                    ["The decomposer finds tickers, years and sub-queries.",
                     "After each hop the critic names what is missing; the generator writes a query aimed at that gap, so the next "
                     "search can reach a different section or filing (up to 3 hops).",
                     "The synthesizer cites every sentence; the guardrail checks every number against the chunk that sentence cites."]),
    "system_c_v2": ("Adds a table of reported figures, and lets it end the search",
                    ["Every 10-K ships machine-readable XBRL. We extracted 9 headline metrics per filing: 272 rows, 10 companies.",
                     "Numeric questions get [F-TICKER-YEAR] rows before search, so multi-year totals become a one-hop lookup.",
                     "The catch: if the table covers the companies, the critic stops at 0.95, even for margins and footnotes the table cannot answer."]),
    "system_c_v3": ("Checks for the exact line item, not just a table",
                    ["Schema-aware routing: XBRL only when the question names one of its 9 columns; margins, segments and debt schedules go to text search.",
                     "Line-item sufficiency: the critic stops only when the specific figure is found for every year asked.",
                     "Table stitching re-joins tables split across chunks; filing years are told apart from maturity years; each company is searched separately in comparisons."]),
}


def page_architecture() -> None:
    st.markdown(
        '<div class="hero"><div class="eyebrow">How it works</div>'
        "<h1>Five ways to answer a 10-K question</h1>"
        "<p>All five systems share the same index, the same answer model and the same questions. They differ only in how they "
        "gather and check evidence, so differences in results point to the retrieval design.</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown(_stats([("10", "companies"), ("272", "10-K filings"), ("95,044", "indexed chunks"),
                        ("97", "benchmark questions"), ("82 of 97", "need 2+ pieces of evidence")]), unsafe_allow_html=True)
    for s in SYSTEMS:
        title, bullets = ARCH_TEXT[s]
        st.markdown(f'<div style="margin-top:22px">{system_pill(s)}</div>', unsafe_allow_html=True)
        st.markdown(f"#### {title}")
        st.markdown(render_diagram(s, static=True), unsafe_allow_html=True)
        st.markdown("\n".join(f"- {b}" for b in bullets))

