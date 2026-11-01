# Demo app review and fixes (2 Nov 2026)

The Streamlit demo (`app.py`, `ui/`) was reviewed before the final presentation by four independent reviewers, each with a different scope:

1. **Code and security**: escaping of model output, API-key isolation, Streamlit state, the Hugging Face deploy.
2. **Visual design**: hierarchy, typography, spacing, charts, anything that read as a generic template.
3. **Plain language and accessibility**: wording a first-time visitor would not follow, WCAG contrast, touch and keyboard access.
4. **Functional testing**: pytest, headless runs of every page, all 97 benchmark questions × 5 systems, 352 filter combinations, citation and diagram edge cases, and live runs on the mock provider.

This file records what they found, what was fixed and what was left on purpose.

## Confirmed safe

- **No HTML or script injection:** model answers, filing text, questions and benchmark fields are all escaped. This was tested with `<script>`, `onerror`, `<svg>`, `javascript:` and HTML in tickers.
- **Numbers on the Results page match the evaluation outputs:** `app_data/rq3.json` matches `reports/rq3/summary_metrics.json`, and the break-even thresholds were recomputed independently.
- **The deploy package imports and runs on its own:** this was tested from a `git archive` built with the workflow's file list.
- **Keys and errors:** a key pasted by a visitor is never written into the environment permanently, and error messages shown to visitors do not contain key values.

## Fixed

### Bugs

| Severity | Problem | Fix |
|---|---|---|
| Critical | System A cached its API client for the whole process (`@lru_cache(maxsize=1)`), so the first visitor's pasted key was reused for everyone after them, and switching provider broke System A. | Client cached per (provider, key) and built with an explicit `api_key` (`src/system_a/llm.py`); regression test in `tests/test_ui_live.py`. |
| High | A run waiting for another visitor's run (different model settings) waited with no time limit, and model clients had no timeout. | `llm_session` waits at most 120 s, then tells the visitor to retry; 90 s timeouts on the System A/C model clients. |
| Medium | A database or code error made the app re-run the whole pipeline on every other provider. | Fallback to another provider only for provider errors (bad key, rate limit, timeout, outage): `live.is_provider_error`. |
| Medium | Overlapping System A runs could report each other's token use and cost (global `LAST_TELEMETRY`). | Per-thread telemetry. |
| Medium | A Space secret `SYSTEM_B_API_KEY` would have overridden a visitor's own OpenAI key for System B. | Included in the per-run key scoping. |
| Low | `load_dotenv(override=True)` ran on every rerun and could reset another visitor's run settings. | Loaded once, without override. |
| Low | The new "pp" (percentage points) unit also matched "PP&E". | Lower-case `pp` only, not followed by `&`; test added. |
| Low | The citation renderer crashed on a number containing a backslash, and on malformed guardrail data. | Function replacement in `re.sub`; type checks. |
| Low | The five answers on the explorer page shared the same source-link ids, so citation chips in tabs 2–5 jumped to tab 1. | Ids prefixed per answer. |
| Low | The step timer overlapped long step titles. | Timer drawn above the step. |
| Medium | The run-bar counters stayed at 0 in some browsers (Safari does not redraw a counter driven by an animated `@property`), and the "this step" counter could keep the previous step's animation. | Counters are now m:ss digit rollers (stepped `transform` animations, supported everywhere); the animation name alternates per redraw so each step restarts at 0:00. Found in the owner's review after the first deploy. |
| Low | Clicking "Compare all five answers" then the active tab sent the visitor back to Ask. | Navigation keeps its last page. |
| Low | Company and year detection for Systems A/B missed "FY21" / "FY'22", matched "chase" and "meta-analysis", and read "$2019 million" as a year. | Fixed in `ui/live.py`. |
| Low | Gold answers were cut after HTML escaping (could split an entity), and live costs were labelled "gpt-5.4 rates" for every model. | Truncate first, then escape; label is now "estimated cost". |

### Accessibility

| Problem | Fix |
|---|---|
| `--faint` text was 3.6:1 contrast (needs 4.5:1). | `#8E897F`, now about 5.2:1. |
| Inactive diagram borders and arrows were 1.5–2.1:1. | `#5A6068` and `#6A7078`, now 3:1 or better. |
| Step explanations were hover-only. | Steps are keyboard-focusable and show their tip on focus; each diagram has a "What each step does" list for touch users. |
| Restyled buttons and tabs lost their focus ring. | Visible brass `:focus-visible` outline. |
| Checked and unchecked numbers differed by colour only. | ✓ / ? marks, plus `aria-label`s. |
| ✓/✗ in the benchmark card had no text alternative. | Coloured, with `aria-label`s. |
| Diagram text was 11.5px. | Raised to 12–15px; the SVG's accessible name lists the steps. |

### Plain language

- **Passages:** "chunk" is now "passage" everywhere a visitor sees it, and How it works defines a passage once.
- **Search rounds:** "hop" is now "search round" in labels, the trace and the diagram edges. "Multi-hop" is kept in the title.
- **Hero text:** the Ask hero says what to do and what the checker is, without jargon.
- **System descriptions:** written in plain words; "XBRL" is explained as "officially reported figures".
- **Scoring terms:** lenient and strict scoring are defined once at the top of Results. "Gold answer" is now "Correct answer", and "in-sample" is explained.
- **Results labels:** the tabs and the test table use plain labels ("Is the difference real?", "Only first right / only second right").

### Design

- **Answer above the fold:** a shorter question box (now limited to 500 characters), and the Ask button sits beside the settings.
- **Run progress:** Streamlit's stock spinner is gone; the brass run bar shows the step, what it is waiting on, and ticking timers. A "Done" bar and a step-by-step log appear afterwards.
- **Charts:** quieter error bars, no repeated axis titles, direct labels on the cost lines instead of a legend, and an annotated "C v3 cheapest above $0.17" line.
- **Explorer cards:** serif question, neutral card borders with a colour swatch per system.
- **How it works:** bullets use the brass-square list style.
- **XBRL tables:** sized to their content.
- **Mobile:** the navigation scrolls instead of wrapping, and a "scroll sideways" hint sits under each diagram.

## Left as is (on purpose)

| Suggestion | Reason |
|---|---|
| Remove the ⓘ markers on diagram steps. | The project owner asked for them. They stay, with a lighter style. |
| Per-visitor rate limiting on the Space's own key. | Out of scope for a class demo. The 500-character limit and provider-only fallback reduce the cost of misuse. Revisit if the Space stays public. |
| Show non-v3 systems at reduced opacity in charts. | Would hide the comparison the charts exist to show. |
| A step list instead of the SVG on phones. | The list is already available under each diagram, and the SVG scrolls. |
| "8.8 pp" can verify against any 8.8% figure in a cited passage, even when that figure is a level rather than a change. | Rare in practice. A full fix needs the guardrail to know which figures are changes. Noted for the guardrail owner. |

## How to re-run the checks

```bash
python -m pytest -q
python scripts/build_app_data.py          # rebuild app_data/ after a new evaluation run
python -m streamlit run app.py            # local demo
```
