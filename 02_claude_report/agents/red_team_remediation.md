# RED TEAM REMEDIATION — binding directive (ORCHESTRATOR, 2026-11-24)

Source: user's Red Team audit of `claude_version.pdf` (the PDF itself is not in the project tree; we work from the user's list).
`comms/project_brief.md` still applies except where this file overrides it. Baseline: `build/main.pdf`, 42 pp, clean.

## Ground rules
- G1 **Engine: LuaLaTeX + biber.** The sprint text says xelatex + bibtex, but `babel bidi=basic` is LuaTeX-only and the user explicitly chose LuaLaTeX + biber per the guide. Switching would reintroduce BiDi faults. Reported to the user as a deviation.
- G2 **Results are not predetermined.** The sprint text says "proving H3". Run the CET1 model and report whatever it shows against the existing REQ-H3-01 threshold (bank loss < 10% of system equity; DSCR < 1). Do not tune parameters to a verdict, and do not move the threshold. Verdict may be supported, partly supported or not supported; say "supported", never "proven".
- G3 **No invented data.** Bank CET1 ratios, RWA, regulatory minima, provisions, stock, demand: each needs a real source opened and checked on the web, with a bib entry. Anything not found is a labelled assumption (`calibrated`, "להמחשה") with rationale and a sensitivity check. Never imply insider/official stress results.
- G4 Every number in text comes from `comms/data_summary.json`.
- G5 **Length: ~40 pp, hard target 38–42 total.** New content must be compact and offset by trimming duplicate prose in the same chapters. Never trim requirements, sources, limitations or hypotheses; never shrink font/margins/spacing. If 42 is not reachable, say so; do not hide it.
- G6 Keep metadata in preamble.tex: אוניברסיטת חיפה, the AI-course line, "עבודת מחקר על שוק הדיור". No seminar or Bar-Ilan wording.
- G7 H1–H3 wording identical in ch01 and ch06. Back up any file before editing (in your own folder, not in build/).
- G8 Raise your flag only when done and compiled; list anything unfinished in chat_log.md. Use real `date` timestamps.
- G9 Only edit the files you own. Compile in your own copy of build/ (parallel lualatex in build/ corrupts aux files).

## Items (verified one by one by Detector)
| ID | Owner | Item |
|---|---|---|
| R01 | A4 | Title page bilingual (Hebrew + English title and subtitle) |
| R02 | A4 | Double decorative frame |
| R03 | A4 | No RQ box, abstract or keywords on the title page (RQ stays in ch01) |
| R04 | A4 | Copyright/affiliation/attribution page numbered ii, between title and executive summary |
| R05 | A4 | tocdepth=3 and secnumdepth=3; real `\subsubsection` entries visible in TOC where the content has them |
| R06 | A4 | `\en` (LTR wrapper) and `\enp{he}{en}` defined; brackets never invert |
| R07 | A1 | TikZ funnel in ch01 |
| R08 | A1 | TAM/SAM/SOM subsection + table/visual in ch03 |
| R09 | A3 | All fig1–fig7 scripts and helpers in 03_python_viz/ AND build/scripts/, running, 300 DPI PNGs |
| R10 | A3 | CET1 model in code and ch05 |
| R11 | A3 | fig7_bank_cet1_erosion.png + data_summary.json |
| R12 | A2 | CET1 result integrated in ch06; "not yet estimated" statements removed everywhere (ch06, ch07 l.15/160, abstract, limitations) |
| R13 | A2 | 5x5 colour risk matrix in ch07 |
| R14 | A2 | Box "3 פעולות מיידיות להמשך המחקר והיישום" closing ch07 |
| R15 | A7 | Regex + visual BiDi sweep of all .tex |
| R16 | A5 | All findings fixed; build complete; main.pdf copied to project root |

Flow: A4 → (A3 then A2; A1 in parallel) → A7 → A5 → A7 re-check. Flags: agent4_remediated, agent1_remediated, agent3_remediated, agent2_remediated, detector_remediated, red_team_closed.
