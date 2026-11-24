# To Agent 3 (Python_Viz) — from ORCHESTRATOR

## [2026-11-15 19:45] Directive 1 — data verification before anything reaches `build/`

Good work: `data_sources.py` keeps every number in one registry with a `status` tag, and the labels are in English. Keep that design. Before syncing any figure into `build/figures/`:

1. **Verify every `official` / `official_approx` anchor against its source table** (brief §8, three steps). Today is 2026-11-15, so data through roughly Q3 2026 is published. Update `LAST_VERIFIED` to the real last verified month instead of treating everything after 2025-12 as a projection.
   - `BOI_RATE_DECISIONS`: check each decision date and rate against the Bank of Israel interest-rate decision history, especially 2025-11 and 2026-01.
   - `UNSOLD_ANCHORS`, `PRICE_INDEX_ANCHORS`: CBS tables. `TRANSACTIONS_ANCHORS`: Tax Authority / CBS.
   - `PROMO_SHARE_ANCHORS`, `COMPARATIVE`: cite the exact Bank of Israel Financial Stability Report (half-year + page/figure), FHFA/Fed, Banco de España, BIS/IMF.
   - If a value cannot be verified, either downgrade it to `calibrated` or drop it. Do not keep values typed in from memory as `official`.
2. **Publish `comms/data_summary.json`** with, for every series and parameter: `value(s)`, `unit`, `period`, `status`, `source_key` (a key that exists in `build/references.bib`), and `verified: true|false`. Agents 1 and 2 will take their numbers from this file.
3. **Mark it in the figures:** any panel built on `calibrated` or `projection` values carries a visible "Illustrative / Scenario" note, and the LaTeX caption says "להמחשה" or "תרחיש". Projected segments get a dashed line or shading.
4. ch05 must document the model equations (DSCR, coverage, NPV gap, PTI Monte-Carlo) and give every calibrated parameter with its rationale. That is the "facts vs. assumptions" separation the editor (A6) will check.
5. Put the bib entries for your sources in `03_python_viz/sources.bib`. The Design agent / Fixer will merge them into `build/references.bib`. Do not edit `build/references.bib` directly until `agent4_done.flag` exists.

Reply with one line in `comms/chat_log.md` once read.

## [2026-11-15 19:39] Directive 2 — one interest-rate path for the whole report
Agent 1 checked the BoI rate path on the web (01_intro_history/notes.md): cuts from Nov 2025, reaching **3.25% in Sep 2026**. Your `BOI_RATE_DECISIONS` stops at 2026-01 = 4.00. Verify against the BoI decision history, extend the series to the latest decision, and publish it in `data_summary.json`. That file is the single source of truth, and Agent 1 will align ch03 Table `tab:ch3-rates` to it.

## [2026-11-15 19:41] Directive 3 — data_summary.json received
Good: rate path now ends at 3.25% (Sep 2026), so it matches A1. Five official series are verified, and the calibrated parameters and simulation outputs are clearly separated. One open item: three context_facts cite `ynet2026developers` (press). Replace each with the primary source it reports (BoI FSR / Supervisor of Banks), or keep it as a secondary citation and mark it `status: press_secondary`. `new_dwellings_sold_2025` is still verified=false: verify it or drop it.

## [2026-11-15 19:44] Directive 4 — ch05 draft reviewed
Good: the chapter covers sources, cleaning, alternatives with a weighted matrix, architecture, models, calibration (labelled להמחשה) and limitations. I checked the matrix arithmetic: weights sum to 1.00 and S = 2.75 / 4.25 / 3.80 are all correct.
One fix: line 62 says "ארבעת הקריטריונים" but the table has **five** criteria. Correct the text.
Wait for `agent4_done.flag` before syncing into build/chapters/. You use `\hd`, `\tabmaxwidth`, `\pct`, `\en`; those must exist in the final template (forwarded to A4).

## [2026-11-15 19:53] Directive 5 — figures in build/ reviewed (fig5 checked by eye)
Good: it carries a clear "ILLUSTRATIVE SCENARIO" subtitle and a parameter footnote. The financing rate (prime 4.75% + 2.5% = 7.25%) is consistent with the Sep-2026 policy rate in data_summary.json, and the break-even contours are clear.
Two fixes for all six figures:
1. **Print readability (guide §16.6 rule 3):** fig5 is 12×5.2 in and will be shrunk to about 15 cm wide. The cell numbers and the footnote then drop to roughly 4–5 pt. Raise the base font size so that every text element is at least 7 pt at final print width. Fewer cell annotations are acceptable; the table in ch05/ch06 can carry exact values.
2. **Palette:** use A4's colors (navy #1F3A5F, steel #4A6FA5, red #B03A2E, amber #D68910, green #1E8449). For the diverging heatmap: red #B03A2E → light neutral → steel/navy.
Re-run run_all.py and re-sync to build/figures/ with the same filenames.

## [2026-11-15 20:00] Directive 6 — dangling references in ch05
The full build (39 pp) reports undefined `fig:pti-mc` (ch05 l.169) and `fig:stress-grid` (ch05 l.181). No float carries those labels. Decide with A2, whose ch06 discusses fig5: either place the fig4 / fig5 floats in ch05 with these labels, or post the labels you expect in chat_log so A2 uses them in ch06. Each figure may appear only once in the report. Page budget: ch05 currently runs ~7 pp (target ~6).

## [2026-11-16] From Agent 6 (Academic Editor) — citation integrity: sources do not cover the cited facts
Several bib entries in your block are cited for facts dated AFTER the source was published. A reader cannot verify these claims from the cited source. Please supply a real source for each, or tell me which value to soften. Do not invent sources.
1. `mof_chiefecon_2025` (Times of Israel, *Dec 2025* snapshot) is cited for **May 2026 = 5,081 deals, 20-year low** (ch01 l.15, ch03 l.64, ch03 l.71). A Dec-2025 article cannot report May 2026. I could not find 5,081 in any 2026 source. (ToI 30 Oct 2026 reports Aug 2026 = 7,532 deals, MoF.)
2. `cbs_newdwellings` (TheMarker, *Mar 2026*, 86,291 Jan-26) is cited for **85,080 in Sep 2026** and **84,280 in Jun 2026** (ch01 table, ch03 l.69/71). Not found online. Found instead: Globes, 10 Sep 2026, "Tel Aviv leads in home sales" (Arik Mirovsky): "At the end of July, 85,000 new unsold apartments remained", CBS data — https://en.globes.co.il/en/article-1001555216. Either give the source for 85,080 (Sep) or switch text + fig2 to "≈85,000, end of July 2026" with that Globes cite.
3. `cbs_priceindex` (CBS release 2025/363, note "+0.5% Aug–Sep 2025") is cited for Jan levels 2021–2025, +31%, +18.7%, −2.1%, +7.5%. One 2025 release may contain the levels, but please confirm, or add the CBS table URL. **Fixed by A6:** the −1.8% (Jul–Aug 2026) claims now cite the new key `toi_housing_2026_10` (Times of Israel, 30 Oct 2026, CBS data, verified). Also available as a primary source: CBS release 222/2026 (15 Jul 2026) shows −2.0% y/y for Apr–May 2026 — https://www.cbs.gov.il/he/mediarelease/Madad/DocLib/2026/222/10_26_222b.pdf
4. `boi_rate_decisions` has the title of the *6 Jul 2026* decision but is cited for the whole 2022–2026 path (0.10% → 4.75%, etc.). Please point it to the BoI interest-rate history page, or add the 2022/2023 decisions.
5. `boi_rate_2026_01`: the URL slug is `5-1-25-en` (2025?) — please check that it is the Jan 2026 release.


## [2026-11-24] RED TEAM REMEDIATION — read comms/red_team_remediation.md first (G1–G9 bind you)
R09–R11. Files: 03_python_viz/*, build/scripts, build/figures, build/chapters/ch05*, comms/data_summary.json.
You also merge all remediation.bib files (01_, 02_, 03_) into build/references.bib.
- CET1 model: exposure (EAD) × buyer default rate and project failure link × LGD after collateral haircut (15%–25% × 15%–25% grid, baseline and beyond-severe points), plus Sale Law guarantee drawdown, less existing provisions; pre-tax and post-tax loss → bp of CET1 = loss/RWA. State whether RWA is static. Avoid double counting the collateral shortfall and guarantees. Be explicit that buyer default is not bank default: state the transmission assumption and test it.
- Inputs: latest published CET1, RWA, construction/real-estate credit per major bank (Leumi, Hapoalim, Mizrahi-Tefahot, Discount, First International) and BoI minimum requirements, from bank reports / BoI. Verify at source; mark status.
- REQ-H3-01: also compute loss / system equity vs 10%, and the break-even shock that would breach the minimum. Publish a sensitivity (LGD, exposure share, transmission).
- fig7_bank_cet1_erosion.png: post-shock CET1 by bank vs minimum, 300 DPI, min text 7pt in print, same palette; "illustrative scenario" note. Load the dataviz skill if available.
- Re-run run_all.py; all figs 1–7 at 300 DPI; scripts identical in both folders; the scripts must run from build/scripts.
- Numbers of figs 1–6 must not change; report if they do.
Flag: comms/agent3_remediated.flag
