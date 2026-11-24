# Fix log (Agent 5), 2026-11-24
Input: comms/reviews/detector_remediation.md. Backups: 05_fixer/backup_pre_fix (build/), 05_fixer/backup_pre_fix_agentdirs (agent folders, json).
Build: lualatex, biber, lualatex x2 in build/: 43 pp, 0 errors, 0 undefined, 0 biber warnings, max overfull 3.4 pt. main.pdf in project root = build/main.pdf (SHA-256 d7a8bc3c...). H1-H3 identical; abstract 336 words.

| ID | Status | What |
|---|---|---|
| D01 | fixed | ch06 table 6.1: 5x5, 24 months, A / B, generated from JSON; text: all 25 cells above 10%; 12 and 0 months ranges |
| D02 | fixed | Pre-tax basis and REQ silence on tax (ch05); after tax 13.9 / 9.2 = inconclusive under the same rule (ch06 sec. 6.3, H3, key finding, ch07, abstract). Verdict and threshold unchanged |
| D03 | fixed | All severe-cell sensitivities in the JSON reported |
| D04 | fixed | Leumi vs Hapoalim definitions, 53% share (ch05 limitations, ch06, abstract). Definitions read in both reports |
| D05 | fixed | Claim limited to tested base-parameter scenarios (to 40/40/24); 41.2% break-even stated in ch06 |
| D06 | fixed | Three mechanisms named, "not replicated" (ch06, ch07) |
| D07 | fixed | ch04 text and caption |
| D08 | fixed | "Negligible securitization" removed; replaced by "securitization law not completed" (BoI survey 2025 p. 187, Hapoalim p. 243). Same uncited claim in ch02 sec. 2.3 also softened. l.38 cite checked in the box text: ok |
| D09 | fixed | preamble: date now printed for every @online entry that has one; supervision dept. author restored for 4 BoI items |
| D10 | fixed | Four titles restored to the documents (both boxes opened); bank report titles and the BdE note title restored; Directive 329 date corrected 2021 -> 27 Dec 2020 (update history) |
| D11 | fixed | Direct PDF URLs for Leumi and BoI survey 2025 (both downloaded) |
| D12-D16, D18, D20-D22, D25 | fixed | as proposed; Mizrahi pages added (printed); FIBI D, G, P, minimum located (PDF pages in note) |
| D17 | fixed | Mizrahi 7.6 vs 18.3 bn, mostly reinsured, 59% share; checked p. 67 |
| D19 | fixed | Draft temporary directive, published by BoI (MoF review p. 11) |
| D23 | not changed | Two manual \newpage kept: layout re-checked and correct |
| D24 | fixed | Radar legend spacing; fig 5.1 boxes: gaps restored (third left box nearly touches the fourth) |
| D26 | disclosed | Not an error: 86,090 is not seasonally adjusted, BoI's about 83,000 is (ch. 8 p. 1 text). Caption of fig 3.1 says so. Anchor unchanged (86,090 itself seen only in a secondary source) |
| Box titles | fixed | Right-aligned (preamble halign) |

Data: data_sources.py (both folders) got 1 comment and 3 context_facts (mizrahi_construction_split_2026q3, absorption_cdf_hapoalim_share, unsold_2025_12_seasonally_adjusted); run_all.py re-run: 7 PNGs byte-identical, no existing JSON value changed.

Trimmed (duplicated prose): ch05 methodology box "facts vs assumptions" (its rule kept as one sentence in 5.1), forward pointers and closing sentence of ch05; ch06 opening sentence merged into 6.1, repeated definitions in 6.2 and 6.3, bank minima repeated from table 5.3, sec. 6.4 intro, repeated words in H1-H3 rulings, captions of figs 6.1 and 6.3 shortened (long list entries kept).

Unfinished: 43 pages, one over the hard target. Body fits the old 31 pages; references grew from 4 to 5 pages (dates, titles, real URLs; 4 entries on the last page). Recovering it needs a change to type or spacing, or cutting sources: not done. An option for the user: \urlstyle{same} (Times instead of Courier in URLs); not tested.
Not verified: what the detector lists in its section 7, except FIBI D/G/P/minimum, which were found.

## Wrap fix, 2026-11-24
Backup: 05_fixer/backup_pre_wrapfix. Build: 43 pp, 0 errors, 0 undefined, max overfull 3.4 pt, no page start moved. main.pdf root = build (SHA-256 c93b98f5...).
- preamble: new \enb{English} = \mbox{(\en{...})}; used by \term, \enp, and 20 literal parentheses in ch01, ch02, ch04, ch06, ch07 (multi-word or hyphenated).
- Reordered to avoid overfull: ch01 Minsky sentence, ch01 "Shadow Credit" sentence, ch02 sec. 2.3 first sentence. \sloppy paragraph: ch01 Minsky, ch02 sec. 2.3, copyright AI note.
- ch01 nested brackets -> dash; ch02 stray space fixed.
- Left wrapped: (T1, T3) ch02 sec. 2.7 (two units in a Hebrew list); SAREB cell in the acronyms table (pure LTR cell); long Hebrew parentheses containing English; English bibliography.
- Scratch: 05_fixer/wrapfix (private copy with renders), safe to delete.
