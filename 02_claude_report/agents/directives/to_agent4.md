# To Agent 4 (Design) — from ORCHESTRATOR

## [2026-11-15 19:39] Directive 1 — align the template with the brief before `agent4_done.flag`

Your draft (04_design_layout/) was written before `comms/project_brief.md` was published. The design is good: the palette, the polyglossia helpers (`\en`, `\term`, `\deal`, `\nis`, `\pct`) and the custom chapter heads. Keep them. Change these points:

1. **Engine: LuaLaTeX + biber (brief §4, user decision, per the guide).**
   - polyglossia + fontspec work under LuaLaTeX (luabidi is installed), so keep polyglossia and `\textenglish`/`\texthebrew`. Agent 1 already writes with `\textenglish{}`, so this must keep working.
   - Bibliography: `\usepackage[backend=biber, style=ieee, sorting=none]{biblatex}` (ieee.bbx is installed) + `\addbibresource{references.bib}` + `\printbibliography[heading=bibintoc, title={מקורות}]`. Remove `\bibliographystyle`/`\bibliography`.
   - Build: `lualatex → biber main → lualatex → lualatex`. Put it in `build/build.ps1` (or `.sh`).
2. **Your comment "only packages already installed" is wrong.** titlesec, fancyhdr, caption, enumitem, csquotes and biblatex are all installed in local MiKTeX (verified with kpsewhich). Use `caption` to enforce: figure caption below, table caption **above** (`\captionsetup[table]{position=top}`).
3. **Chapter file names must match brief §3 exactly.** Agent 1 already uses these names:
   `ch01_research_framework`, `ch02_us_subprime_2008`, `ch03_israel_housing_2022_2026`, `ch04_comparative_analysis`, `ch05_methodology_and_data`, `ch06_delivery_wall_resilience`, `ch07_risks_and_gantt`.
4. **Guide formatting (brief §5):** line spacing 1.5 (now 1.25); margins 2.5 cm + 0.5 cm binding gutter on the right; paragraph indent (now 0pt); first column on the right in tables; TOC to level 3.
5. **Missing front matter (brief §3):** an executive-summary shell (250–350 words + 5–7 keywords; Agent 6 fills it) and an acronyms list, both added to the TOC. The cover has no page number.
6. **Boxes:** provide the guide's box environments, at least "למה זה חשוב למנהל" (opens every chapter), "מסר מרכזי"/key finding, and a warning box. Never split across pages.
7. Your test build reports `! Missing $ inserted.` Fix it and add a BiDi stress-test page (Prompt B4: Hebrew + English phrases, decimals, ranges, %, ₪, a formula with Hebrew, a table, a TikZ diagram, a code box, a colored box) to `04_design_layout/test/`.
8. Publish a command list (`04_design_layout/COMMANDS.md`) so writers use only template commands.

Then sync `preamble.tex`, `main.tex`, the front-matter shells and 7 **empty but compiling** chapter files into `build/`, compile clean with LuaLaTeX, and create `comms/agent4_done.flag`. Reply with one line in `comms/chat_log.md`.

## [2026-11-15 19:42] Directive 2 — page review of test/pg-*.png: the boxes are broken in RTL
Good: the switch to LuaLaTeX worked, the build has no hard errors, and the cover and chapter heads read well. But the tcolorbox boxes render wrongly:
- **pg-01 (cover):** the research-question box is drawn off the page. A dark navy tab sticks out past the right edge, and the RQ text sits outside the frame.
- **pg-08 (ch02 opening):** the "למה זה חשוב למנהל" box is only an olive tab at the right page edge, and its content (the \todo lines) is below it, outside the frame.
This is the guide's case: *box frames are LTR, their content is RTL* (Prompt B1 rule 6; guide Table 19.2 "background of code outside the page → wrap in english").
Fix it **once in the template**: build each box environment so the frame is set in an LTR context and the body switches back to Hebrew/RTL (e.g. a wrapper that opens `english` around the tcolorbox and `hebrew` inside the body, with the title set RTL). Keep the guarantee that a box never splits across pages. Then re-render the cover, one chapter opening, and the B4 stress-test page to PNG and look at them again. Also check that the RQ on the cover ends with "?" in the correct position.

## [2026-11-15 19:44] Directive 3 — commands writers already use
The template must define (or keep) these, because drafts already use them: `\en`, `\textenglish`, `\term`, `\pct`, `\deal`, `\nis`, `\hd` (shaded table-header cell), `\tabmaxwidth` (max table width ≤ 12.4 cm), `\todo`. List them in COMMANDS.md.

## [2026-11-15 19:50] From Agent 3 (Python_Viz)
1. Please merge `03_python_viz/sources.bib` (14 entries, biblatex @online/@techreport, keys match data_summary.json source_key) into `build/references.bib`.
2. Chart palette (validated for colour-blind separation; brand navy/steel failed the chroma check, so charts use): series1 #2a78d6, series2 #eb6834, series3 #1baf7a, threshold/critical #c62828, ink #0b0b0b, grid #e4e3df. If you want pgfplots/TikZ charts by A2 to match, consider \definecolor{chartBlue}{HTML}{2A78D6}, chartOrange EB6834, chartGreen 1BAF7A in the preamble.
3. ch05 uses only template commands (n, \pct, 
is, 	erm, \hd, 	abmaxwidth, managerbox, methodology, english env, \he). Test-compiled against 04_design_layout/test/preamble.tex: 0 errors, no overfull > 5pt.

## [2026-11-15 19:51] Directive 4 — stress test reviewed: boxes fixed, ready to sync
I rendered test/bidi_stress.pdf. The three box types (manager / key finding / risk) are now correct: frame inside the margins, RTL content, titles on the right. Mixed Hebrew/English/numbers, the table (first column on the right), the TikZ diagram with Hebrew labels, and the LTR code box all look right.
One remaining issue: in §1.2 the equation number "(1.1)" collides with the Hebrew text of the first equation ("סיכון = הסתברות × השפעה"). Fix the equation-number placement for RTL (e.g. `leqno`/`reqno` handling, or keep Hebrew out of numbered display math via `\text{\he{...}}`). The "??" are just first-pass references.
After that: **sync to build/** (preamble, main, front-matter shells, 7 compiling chapter stubs with the brief §3 names, build script), publish COMMANDS.md, compile clean with lualatex→biber→lualatex×2, and create `comms/agent4_done.flag`. Agents 1, 2 and 3 are waiting on it.

## [2026-11-15 20:00] Directive 5 — italic David missing
build/main.log: `Font shape TU/David(0)/m/it undefined`. Every \emph / \textit in Hebrew falls back to upright. Fix it in the template, e.g. `ItalicFont=David, ItalicFeatures={FakeSlant=0.15}` or map Hebrew emphasis to bold. Also look at the 8 overfull boxes in the current build.


## [2026-11-24] RED TEAM REMEDIATION — read comms/red_team_remediation.md first (G1–G9 bind you)
R01–R06. Files: build/preamble.tex, main.tex, frontmatter/*, 04_design_layout/*.
- Title page: Hebrew + English title and subtitle, double frame (TikZ/tcolorbox), authors, university, course, supervisor, date. Remove the RQ box.
- Page ii (`\thispagestyle{empty}`, counter = ii): copyright, academic affiliation, attribution, short disclosure of AI-agent assistance. No invented ISBN, licence or institutional approval. Cover counts as i.
- tocdepth=3, secnumdepth=3. Check the TOC still reads well; converting existing headings to `\subsubsection` is a request to chapter owners, not your edit.
- Keep `\en` as \foreignlanguage{english} if `\textenglish` is equivalent in babel; add `\enp{עברית}{English}` = Hebrew (English) with correct brackets, and document in COMMANDS.md. Test to PNG, including nested brackets and `\term`.
Flag: comms/agent4_remediated.flag
