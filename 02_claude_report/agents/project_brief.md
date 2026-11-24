# PROJECT BRIEF — Housing Project (Preparatory Report, ~40 pages)

Issued by: ORCHESTRATOR (00_orchestrator) · 2026-11-15
Binding source: Dr. Yoram Segal, "From Problem to PDF: The Professional Preparatory Report"
Copy: `00_orchestrator/prep_guide_segal.pdf`. **Read it. Every rule there is binding; this brief extracts the key ones.**
Where this brief and the guide disagree, the guide wins.

---

## 1. Core Research Question (verbatim, must appear in ch01 and be answered in ch06/ch07)

> באיזו מידה מבצעי המימון הקבלניים (כגון 20/80 ו-20/50/30), הלוואות הבלון ומינוף היזמים בשוק הנדל"ן הישראלי (2022–2026) משחזרים את מנגנוני הכשל של משבר הסאב-פריים (2008) ומשבר הנדל"ן בספרד, ומהי עמידות המערכת הבנקאית והיזמית בישראל בפני גל חדלות פירעון בעת 'קיר המסירות' של 2026–2027?

This is a **research project** (guide Table 4.1): research question + hypotheses (H1–H3) that are confirmed/refuted, not design goals. Hypothesis wording must be identical wherever it appears (ch01 ↔ ch06).

## 2. Folder architecture (all work stays inside `"$HOME/Desktop/housing project"`)

| Folder | Owner | Purpose |
|---|---|---|
| `00_orchestrator/` | Orchestrator | logs, tracking, guide copy |
| `01_intro_history/` | Agent 1 Intro_History | drafts for ch01–ch03 |
| `02_research_core/` | Agent 2 Research_Core | drafts for ch04, ch06, ch07 |
| `03_python_viz/` | Agent 3 Python_Viz | ch05 drafts, Python scripts, data, charts |
| `04_design_layout/` | Agent 4 Design | preamble/main templates |
| `05_fixer/` | Agent 5 Fixer | repair logs |
| `06_academic_editor/` | Agent 6 Academic_Editor | editorial notes, audit |
| `07_detector/` | Agent 7 Detector | `detector_report.md` |
| `build/` | shared | `main.tex`, `preamble.tex`, `references.bib`, `chapters/`, `scripts/`, `figures/`, `main.pdf` |
| `comms/` | shared | `chat_log.md`, `inbox/to_agentX.md`, `reviews/`, `data_summary.json`, `*.flag` |

Work in your own folder; sync only finished deliverables into `build/`. Never write outside the project root.

## 3. Chapter structure (`build/chapters/`, ~40 pages total incl. ~3 pages references)

| File | Owner | Pages | Must contain (guide chapter) |
|---|---|---|---|
| `ch01_research_framework.tex` | A1 | ~5 | Quantitative problem statement (current vs. desired state, gap, cost); verbatim RQ; H1–H3; scope & assumptions; research-requirements table with ID / target / verification (`REQ-XXX-NN`) (guide ch.4); short funnel intro + "structure of the report" paragraph (guide ch.3) |
| `ch02_us_subprime_2008.tex` | A1 | ~6 | Subprime **and Spain** failure mechanisms, as a **thematic & critical literature review** (not paper-by-paper); literature matrix papers × themes (guide ch.5) |
| `ch03_israel_housing_2022_2026.tex` | A1 | ~7 | Israeli market 2022–2026: contractor financing deals (20/80, 20/50/30), balloon loans, developer leverage, delivery wall — with real data; **flagship paper** (3 criteria: refereed venue, direct relevance, replicability) + **knowledge gap in one sentence** (guide ch.5) |
| `ch04_comparative_analysis.tex` | A2 | ~6 | Multi-parameter comparison table US 2008 / Spain 2008 / Israel 2022–26; similarities, differences; two charts (e.g. radar + scatter) (guide ch.6 adapted: "market" = the housing/credit market) |
| `ch05_methodology_and_data.tex` | A3 | ~6 | Data sources & cleaning; 2–3 genuinely different methodological alternatives + **weighted decision matrix** (weights sum to 1.0, scores 1–5, `S_j = Σ w_i·c_ij`, weights set before scoring) + chosen approach architecture/data-flow diagram (guide ch.7) |
| `ch06_delivery_wall_resilience.tex` | A2 | ~6 | Resilience / stress-test analysis of banks & developers at the 2026–27 delivery wall; sensitivity analysis; results vs. H1–H3 — empirical facts (cited) strictly separated from simulation assumptions ("בהנחה כי", "תרחיש") |
| `ch07_risks_and_gantt.tex` | A2 | ~4 | WBS, RACI, Gantt with critical path & milestones (guide ch.8); risk table R = P × I (1–5 each), every R ≥ 12 gets mitigation + contingency + residual score (guide ch.9); **1-page summary**: findings, readiness, three immediate next actions (guide ch.10) |

Front matter (A4 Design builds shells, A6 fills abstract last): cover without page number; executive summary 250–350 words + 5–7 keywords; TOC (to level 3); list of figures; list of tables; acronyms list.

## 4. Technical stack (guide ch.13)

- **LuaLaTeX** (MiKTeX, installed) + **biber** + biblatex `style=ieee`. `references.bib` holds the bibliography only.
- Document class: `book`, 12pt, A4. Hebrew RTL main language (babel, `bidi=basic`), English LTR.
- Build (4 runs, from `build/`):
  ```
  lualatex -interaction=nonstopmode main.tex
  biber main
  lualatex -interaction=nonstopmode main.tex
  lualatex -interaction=nonstopmode main.tex
  ```
- Success: `Output written on main.pdf` with page count; no `!` lines in `main.log`; no undefined references; no overfull box > 5pt.
- Design Agent may start from the existing tested-shape preamble at
  `<local path>/preamble.tex` (read-only reference; copy, do not edit there).

## 5. Formatting rules (guide ch.11, ch.16)

- Hebrew font David (or Calibri/Arial) 11–12pt; English Times New Roman; line spacing 1.5; justified.
- Margins 2.5 cm + 0.5 cm binding gutter.
- Units in SI; currency as `₪` / NIS consistently.
- Figures: caption **below**, numbered by chapter, referenced in text **before** the float, text explains what we learn.
- Tables: caption **above**, first column on the right, width ≤ 12.4 cm.
- Every figure: Hebrew caption, number referenced in text, readable in print, consistent colors across the report.
- Any number that appears inside an image must also appear in a table or text. Keep source files of every figure.
- Python charts: English labels inside the image (no Hebrew rendered by matplotlib), Hebrew caption in LaTeX. Output PDF/PNG to `build/figures/`, scripts in `build/scripts/`.

## 6. Hebrew / English BiDi rules (guide ch.14, Prompt B1) — mandatory for all writers

1. Mark every English word, name and acronym as English (template command).
2. Mark a multi-word English phrase as one unit.
3. Mark every number, decimal, range, percent, date, currency amount and version as one LTR unit (e.g. `20/80`, `2022–2026`, `₪1,500`, `25%`).
4. Never put Hebrew inside an English-marked unit.
5. Hebrew inside a formula uses the template's math command.
6. Every diagram and code box is built in an English environment; Hebrew labels wrapped.
7. In tables the first column is on the right.
8. Use only the template's commands. Do not invent new ones — request them from A4 via `comms/inbox/to_agent4.md`.
- A problem that repeats across the document is fixed **in the template**, never by patching text. Never "fix" reversed Hebrew by typing it backwards.

## 7. Writing rules (guide ch.11, ch.3)

- Third person, professional, measured, fact-based. No "I/we think", no journalistic drama.
- English term in parentheses on first use: `עברית (English)`.
- Every factual claim has a `\cite{}`. Intro claims rest on a number or a source.
- Each chapter opens with a "why this matters to a manager" box and ends with a transition sentence to the next chapter.
- Pitfalls to avoid: opening too generic; "no competitors / no precedent" claims; weights fixed after knowing the winner.

## 8. Sources (guide ch.17, Prompt 3)

- IEEE style, numbered in order of appearance; two-way match: every `\cite` in the list, every list entry cited.
- **Real sources only.** Each source is verified in three steps: (1) exact title found in an academic database / Google Scholar or the official publisher site; (2) authors, year, DOI/URL checked; (3) at least the abstract read and it says what we attribute to it. If it cannot be verified — leave it out. Never invent DOIs, page numbers or statistics.
- Preferred data sources: Bank of Israel (Financial Stability Reports, Supervisor of Banks), CBS (הלמ"ס), Israel Tax Authority, Ministry of Finance Chief Economist, IMF/BIS/OECD, US FCIC report, Banco de España; peer-reviewed journals.
- Data: no confidential organizational data in public AI tools; synthetic/simulated values explicitly labelled "להמחשה" / "תרחיש".

## 9. Workflow & flags

| Stage | Agent(s) | Done flag |
|---|---|---|
| 1 | A4 Design → `build/preamble.tex`, `build/main.tex`, front-matter shells, empty chapter files that compile | `comms/agent4_done.flag` |
| 2 (parallel) | A1 → ch01–ch03 · A2 → ch04, ch06, ch07 · A3 → ch05 + all Python charts | `agent1_done.flag`, `agent2_done.flag`, `agent3_done.flag` |
| 3 | A6 Academic Editor (register, citations, structure, abstract + keywords) | `agent6_done.flag` |
| 4 | A7 Detector → `07_detector/detector_report.md` (9 check families, guide Table 19.1; page-by-page render review, Prompt 8) | `detector_done.flag` |
| 5 | A5 Fixer → repairs + clean 4-pass build of `build/main.pdf` (38–42 pages); A7 re-verifies | `detector_verified.flag` → `project_complete.flag` |

Shared-data rule: A3 publishes all numeric series used in charts to `comms/data_summary.json` (value, unit, period, source key). A1/A2 cite numbers from there or from their own verified sources — never two different values for the same quantity.

Communication: post status lines to `comms/chat_log.md` (`[time] [AgentN] message`). Requests to a specific agent go to `comms/inbox/to_agentN.md`. Reviews go to `comms/reviews/`.

## 10. Pre-submission checklist (guide §11 box + §19.5)

1. Abstract within 250–350 words, followed by keywords.
2. Every requirement/hypothesis has a target value and verification method.
3. Flagship paper analysed; knowledge gap in one sentence.
4. Decision-matrix weights sum to 1.0.
5. Every critical risk (R ≥ 12) has mitigation + contingency.
6. Every figure and table referenced in the text.
7. Every source in the list is cited; every citation is in the list; every source verified and read.
8. Zero compile errors and no unresolved references.
9. No reversed Hebrew, no text outside margins; tables aligned; all images appear.
10. Every page reviewed by eye at readable size.
