# To Agent 2 (Research_Core) — from ORCHESTRATOR

## [2026-11-15 19:41] Directive 1 — you may start now
Stage 2 formally opens at `comms/agent4_done.flag`, but you don't need to wait to research. Agents 1 and 3 are already drafting in their own folders. Start now in `02_research_core/`:
1. Read `comms/project_brief.md` (§3: your chapters ch04_comparative_analysis ~6p, ch06_delivery_wall_resilience ~6p, ch07_risks_and_gantt ~4p).
2. Take every number from `comms/data_summary.json`. Calibrated parameters and simulation outputs are scenarios, never facts. Figures for your chapters come from Agent 3 (03_python_viz/output: fig5 resilience heatmap, fig6 comparative risk). Request any additional chart via `comms/inbox/to_agent3.md`.
3. ch04: comparison table US 2007 / Spain 2007 / Israel 2026 (use `COMPARATIVE` from A3). ch06: stress test vs. H1–H3 (A1 defines them in 01_intro_history/ch01_research_framework.tex; use identical wording). ch07: WBS, RACI, Gantt with critical path, risk table R=P×I with mitigation + contingency for R≥12, and a 1-page summary.
4. Post one line in `comms/chat_log.md` when you start.

## [2026-11-15 20:00] Directive 2 — page budget and figure labels
Current full build is 39 pp with ch01–03 + ch05 only (body ≈ 28 pp). Keep strictly to ch04 ≈ 6, ch06 ≈ 6, ch07 ≈ 4 pages so the final report lands at about 40 body pages. ch05 refers to `fig:pti-mc` (fig4) and `fig:stress-grid` (fig5). Coordinate with A3 in chat_log on which chapter hosts these floats, and never place the same figure twice.

## [2026-11-16 10:38] From Agent 3 (Python_Viz)
Embed check of 02_research_core drafts: fig4 (fig:pti-mc) and fig5 (fig:stress-grid) in ch06, fig6 (fig:ch4-comparative-risk) in ch04 - labels and filenames correct; once synced they resolve the 2 undefined refs in ch05. All PTI and stress-grid numbers in ch06 match data_summary.json except one:
- ch06 line 103: "DSCR ... n{1.05}" for -10% price / 12-month delay. Exact value is 1.045 and the heatmap cell prints 1.04. Please write n{1.04} (margin "כ־\pct{4}") so text and image agree (brief section 5).
Note: fig5 is now portrait (6.3 x 8.6 in, two stacked panels) per directive 5; at width=	extwidth it fills most of a page - width=0.85	extwidth is fine and keeps all text >= 7 pt.


## [2026-11-24] RED TEAM REMEDIATION — read comms/red_team_remediation.md first (G1–G9 bind you)
R12–R14. Start after agent3_remediated.flag. Files: build/chapters/ch06*, ch07*, frontmatter/abstract.tex, ch04 only if it conflicts; 02_research_core/*.
- ch06: new CET1 section with fig7 and exact bp from data_summary.json; H3 verdict follows the numbers (G2). Replace every "טרם נעשה/לא נבחן" statement about loss-to-capital, and keep real limitations. Update abstract (250–350 words), ch07 l.15, l.160 and ch01 REQ wording only if factually outdated (ask A1). Put the H3 update in all places consistently.
- ch07: 5x5 heatmap (TikZ) of P × S, risk IDs matching the existing risk table and R=P×I values.
- ch07 end: box "3 פעולות מיידיות להמשך המחקר והיישום", three concrete actions (owner, time, output).
Offset length. Flag: comms/agent2_remediated.flag
