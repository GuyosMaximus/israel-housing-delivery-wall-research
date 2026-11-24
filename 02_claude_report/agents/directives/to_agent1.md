# To Agent 1 (Intro_History) — from ORCHESTRATOR

## [2026-11-15 19:39] Directive 1
1. Good start: ch01–ch03 drafts with citations, and a verification list in notes.md. Keep drafting in 01_intro_history/ until `agent4_done.flag` exists.
2. **Numbers:** Agent 3 is building `comms/data_summary.json` as the single source of truth for every series (rates, unsold inventory, transactions, price index, promo share). Before syncing, align every number in ch01–ch03 with it. If you disagree with a value, post it in `chat_log.md` and don't keep two versions. The rate path (3.25% in Sep 2026) has been forwarded to Agent 3.
3. **Sources:** the guide's three-step check applies. Secondary press (Globes, Ynet, TradingEconomics) may help you find facts, but the cited source must be the primary one (BoI decision, CBS release, BoI FSR with page/figure). Fix the bib URLs that point to a site root (your notes item 5).
4. **Your open question 6** (were the March-2025 restrictions extended or removed?) is a research fact, not a user decision. Resolve it from the BoI circular / Directive 329 history. If it can't be verified, write it neutrally and flag it in notes.md. Do not guess.
5. **Brief §3 requires** ch02 to cover Spain as well as the US, as a thematic literature review with a papers × themes matrix; ch03 to contain the **flagship paper** (3 criteria) and the **one-sentence knowledge gap**; and ch01 to hold the verbatim RQ, H1–H3, scope and a requirements/hypotheses table with target + verification method.
6. Keep writing `\textenglish{}`. The template will keep supporting it.

## [20:06] From Agent 4
ch02_us_subprime_2008.tex lines 32-33: literal "textbf" (backslash lost, probably via a shell heredoc) causes a 16.6pt overfull box. Restore it to 	extbf{...}. Write LaTeX with a file editor, not a heredoc.


## [2026-11-24] RED TEAM REMEDIATION — read comms/red_team_remediation.md first (G1–G9 bind you)
R07–R08. Files: build/chapters/ch01*, ch03*, 01_intro_history/*.
- ch01: TikZ funnel, four levels: macro credit cycles and subprime lessons → Israeli housing market 2022–2026 → contractor promotions (20/80, 20/50/30) → 2026–27 delivery wall and bank/developer solvency. Hebrew labels, caption below, referenced in text.
- ch03: subsection TAM/SAM/SOM with table. TAM = total stock/demand, SAM = active new-construction market, SOM = unsold 85,000+ units and deferred-payment deals. Define each level precisely (stock vs flow, units, date). Unsold units and 20/80 deals are different populations: never add or conflate them; note overlaps. Source every figure (G3); derived values show the arithmetic. New bib entries go in 01_intro_history/remediation.bib and are posted in chat_log; new numbers too (A3 merges into data_summary.json).
Offset length by trimming ch01/ch03 repetition. Flag: comms/agent1_remediated.flag
