# Detector: Red Team remediation audit (Agent 7, 2026-11-24)

Audited: build/main.pdf (42 pp, built 16:38), all .tex, references.bib, scripts, comms/data_summary.json.
Tools: 07_detector/scripts/recompute_cet1.py, bidi_scan_r15.py; output 07_detector/bidi_r15_out.txt; page images 07_detector/render2/.
Page numbers are the printed ones. Nothing in build/ was changed.

## 1. PASS / FAIL
| ID | Result | Evidence |
|---|---|---|
| R01 | PASS | Hebrew and English title and subtitle |
| R02 | PASS | Two frames drawn; both seen |
| R03 | PASS | No RQ, abstract or keywords on the cover |
| R04 | PASS (ruled) | Page ii content complete; number not printed, as ruled |
| R05 | PASS | tocdepth and secnumdepth 3; two real subsubsections in the TOC (3.2.1.1, 3.2.1.2) |
| R06 | PASS | Macros defined; no inverted bracket found |
| R07 | PASS | Funnel p. 1, legible |
| R08 | PASS | Table 3.1; every source value I opened matches |
| R09 | PASS | 7 scripts and helpers; build/scripts run in a clean copy gave 7 byte-identical PNGs, 300 DPI; all 10 files identical in 03_python_viz and build/scripts |
| R10 | **FAIL (partial)** | Code correct and reproduced; the requested 5x5 grid is nowhere in the PDF (D01). Disclosure gaps D02-D04 |
| R11 | PASS | fig7 and JSON present; JSON equals the first-run log key by key |
| R12 | PASS with majors | "Not estimated" wording gone (searched in ch01-ch07 and front matter); verdict consistent in abstract, ch04, ch06, ch07. D02-D05 |
| R13 | PASS | 25 cells = P x I; all six risks in the right cell; colours right |
| R14 | PASS | Box closes ch07: 3 actions with owner, week, output |
| R15 | PASS | 0 true BiDi faults (section 2) |

Build: 42 pp, 0 errors, 0 undefined, max overfull 3.4 pt. 48 bib keys, none missing or uncited. Abstract 318 words (250-350). H1-H3 identical ch01/ch06. No number in the text conflicts with the JSON in the CET1, DSCR, PTI and NPV passages I checked.

## 2. R15 sweep
Regex hits (Latin or digits outside wrappers), all read one by one:
- preamble.tex 45: colour and box options, macro arguments. False positives.
- acronyms.tex 23: third column, inside the LTR E column type. False positives.
- titlepage 4 (lengths), float options `[!htb]`, `p{}` column: false positives.
- ch02 l.14, 21 ("נושא 1", "נושא 2"), ch05 l.160 ("רובד 1."): bare single digits. They render correctly; cosmetic (D20).
- Hebrew inside \en: 0. Bracket at an \en edge: 0. Nested brackets: ch01 l.73, rendered correctly.
Visual read of all 42 pages (about 110 dpi; doubtful places at 200-220 dpi): brackets, ranges, signs and percentages correct, including "(-10%, 12 חודשים)", "(DSCR < 1)", nested brackets p. 2, LTR acronym column, heatmap numbers, boxes inside the page. Box titles on the left: known.

## 3. CET1 recomputation (own code, written from the spec equations)
| Cell | Variant | System loss bn | % of equity | after tax | CET1 sys | Leumi | Hapoalim | Mizrahi | Discount | FIBI |
|---|---|---|---|---|---|---|---|---|---|---|
| centre 20/20/12 | A | 31.59 | 14.02 | 9.15 | 9.97 | 10.11 | 10.64 | 9.26 | 9.47 | 9.63 |
| centre | B | 5.34 | 2.37 | 1.55 | 10.80 | 11.17 | 11.47 | 9.93 | 10.18 | 10.18 |
| severe 25/20/24 | A | 48.04 | 21.32 | 13.91 | 9.44 | 9.44 | 10.12 | 8.84 | 9.03 | 9.29 |
| severe | B | 31.87 | 14.15 | 9.23 | 9.96 | 10.10 | 10.63 | 9.25 | 9.46 | 9.63 |
All equal to the JSON. All six 5x5 grids (m = 0, 12, 24; A, B) match. Beyond-severe matches. Every sensitivity quoted in ch06 matches.

Pre-registration: the 10% threshold and the q/m range ARE in the pre-remediation ch01 (backup), so they pre-date the run. The d = 25% choice, the two-variant rule and the pre-tax basis exist only in the spec. File times cannot prove order (spec created 16:01:24, run log 16:01:25, spec last saved 16:02:36, after the run; consistent with adding sections 7-8). The claim "נקבע לפני ההרצה" is documented by the authors, not independently verifiable.
The severe cell is justified: it is the REQ's own worst q/m corner. d = 25% hardly matters (d = 0 gives 20.3% / 12.2%).
Double counting: A uses q twice (disclosed). B does not. Guarantees enter EAD only. No hidden double count found.

## 4. Findings

### Critical
None.

### Major
- **D01 (R10)** ch06 l.61, pp. 26-27; absent elsewhere. The 5x5 grid requested (and promised in spec sec. 1) is not in the report; only its centre is. Also hidden: the m = 24 grid is above 10% in all 25 cells for both variants, which argues against "fragile" and belongs in a balanced account. FIX: add a compact 5x5 table (m = 12, cell "A / B", from grid_A_m12 / grid_B_m12) after l.61. If the 42-page cap blocks it, at least the sentence (wrap numbers in \en): "ברשת 5×5 (כשל רוכשים 15%–25%, ירידת מחירים 15%–25%) ההפסד הוא 7.5%–19.9% (A) ו־0.5%–4.8% (B) בעיכוב של 12 חודשים, ו־15.4%–27.9% ו־10.7%–17.2% בעיכוב של 24 חודשים; ללא עיכוב 0%–1.3% ו־0%." A sentence alone is the minimum and should be reported to the user as such; the table fully satisfies the request.
- **D02** ch06 l.50, l.84; abstract l.18; ch07 l.172. The pre-tax basis decides the verdict: after tax B is 9.2%, below 10%, so by the spec's own rule the result would be inconclusive. The figure is printed but its consequence is not, and REQ-H3-01 (ch01 l.124) does not say pre- or post-tax. FIX l.84, after "ו־14.2% (B)": "הסף נבחן לפני מס; אחרי מס הגרסאות חלוקות (13.9% ו־9.2%), והתוצאה תלויה בשיטה".
- **D03** ch06 l.61, ch05 l.221-222. Sensitivities are selective. delta (guarantee draw) = 0 gives 11.8% / 7.6% (splits) and is omitted, although table 5.4 says 0-0.5 was tested; projects only (s = 69/367) gives 15.0% / 10.05% and is omitted. FIX l.61: "ללא מימוש ערבויות הגרסאות חלוקות (11.8% ו־7.6%); באשראי לפרויקטים בלבד ההפסד הוא 15.0% ו־10.05%".
- **D04** ch05 l.167, l.229; ch06 l.61; abstract. The "full value" reading is presented as an alternative reading. Source check: Hapoalim Q3-2026 p. 61 note 4 defines absorption capacity on the completed value of the asset ("בשווי הנכס כגמור"); Leumi p. 80 note (c) defines it on inventory prices. Hapoalim supplies 52,634 of the 99,962 NIS m (53%) behind three CDF nodes, and under its definition the severe result drops to 9.98% / 0.6%. FIX ch05 l.229: "לאומי מגדיר את כושר הספיגה על מחירי המלאי והפועלים על שווי הנכס הגמור; המודל מחיל את הגדרת לאומי, וההגדרה השנייה הופכת את התוצאה (סעיף 6.3)".
- **D05** ch06 l.59, abstract l.18, ch07 l.172: "אף תוצאה בפרמטרי הבסיס אינה נמוכה מ־6.5%" / "אף בנק אינו יורד". Not true as stated: the JSON break-even has the first bank below 6.5% at a 41.2% price fall (A, m = 24), and s = 1 or full-T exposure was not checked against 6.5%. FIX all three: "באף אחד מהתרחישים שנבחנו בפרמטרי הבסיס (עד 40%/40%/24) אין בנק היורד אל מתחת ל־6.5%".
- **D06** ch06 l.84: "ומנגנוני המשבר האמריקאי אינם קיימים בישראל". Contradicts ch04 box and ch07 l.170 (deferred affordability test IS replicated). FIX: "ושלושה ממנגנוני המשבר האמריקאי (איגוח, מינוף משקי בית גבוה, היעדר חבות אישית) אינם קיימים בישראל".
- **D07** ch04 l.61, p. 15: "כל הערכים באיור, למעט יחס החוב לתוצר בארה״ב ובישראל, מכוילים" is false: Israel 39% is official (fig 4.1 has no star; JSON official). FIX: add "וחשיפת הבנקים בישראל"; same addition in the caption l.66.
- **D08** ch04 l.40, table 4.1 "איגוח זניח \cite{boi2026_recredit}". I read the cited press box text: a search for "securitiz" found nothing. FIX: remove the cite from "איגוח זניח", or cite a source that says it. Same check advised for l.38 "מאזן בנקאי מפוקח".
- **D09** references.bib, pp. 32-35. A2's techreport-to-online change drops the publication year from print: IEEE @online prints only "Accessed". Entries [36], [37], [42]-[48], [1] now carry no date or institution. FIX: restore @techreport/@report (as in 02_research_core/backup_remediation/references.bib) or add the year to `note`.
- **D10** references.bib titles no longer matching the source: boi2026_recredit and boi2026_resloans ("Box from the forthcoming Survey of Israel's Banking System for 2025: ..."; first one confirmed in the document), boi_fsr2024h2 ("Financial Stability Report, Second Half of 2024", confirmed), boi_fsr2024h1 ("...: 2024:H1 January-June", confirmed). FIX: restore the four titles. Corporate author "Bank of Israel" for Directive 329 and Circular 2816 is shortened, not wrong. Journal and publisher abbreviations are standard. bde2017note title shortened by dropping the publisher phrase: acceptable.
- **D11** references.bib l.383, l.431: leumi_q3_2026 and boi_survey2025 point to landing pages, so cited pages are not reachable. FIX: Leumi https://www.leumi.co.il/leumi-hebrew/s3fs-public/newsite/financialstatement/26/q3/eng/Leumi%20Q3%202026_Financial%20report.pdf ; survey https://boi.org.il/media/psgdvces/ (file "סקירת-מערכת-הבנקאות-לשנת-2025-003.pdf", percent-encode). Both opened by me.

### Minor
- **D12** ch04 l.114: "שמונה מנגנונים" vs table 4.1 (10 rows) and radar (6). FIX: "מתוך שמונה מנגנוני כשל, שנגזרו מטבלה 4.1" (a derived list, not the row count).
- **D13** ch05 l.174: rule omits the third branch. FIX: add "אינו מתקיים אם שתיהן חורגות, ואם הן חלוקות התוצאה תלויה בשיטה".
- **D14** ch05 l.200 "אף אחד מהם אינו נתון נצפה": s (150/367) and tax 34.75% come from sources. FIX: "למעט מרכיבי s ושיעור המס".
- **D15** ch05 l.229 "תוצאות הרשת הן חסם תחתון": overclaim; the grid also has conservative inputs (late penalty, 10% haircut). FIX: "עשויות להמעיט בסיכון".
- **D16** ch05 l.174 "גרסה A שמרנית": not uniformly; with q = 0, m = 24, A is 2.1% and B 3.6%. FIX: "שמרנית בירידות מחיר שנבחנו".
- **D17** Mizrahi p. 67 reports 7,613 of home-buyer guarantees inside construction credit risk against the nominal 18,293 used (mostly reinsured, note 5), and 59% of on-balance construction risk is project credit against the uniform 40.9%. Nominal use is disclosed; size is not. FIX ch06 l.61 (limitations): "במזרחי־טפחות סיכון הערבויות המדווח בענף הוא 7.6 מיליארד בלבד, רובו בביטוח משנה".
- **D18** ch03 l.119 "אין במחקר הקיים": absolute claim. FIX: "לא אותר במחקר הקיים".
- **D19** ch03 l.102 "ב־23 במרץ 2025 הודיע ... צעדים מחייבים": MoF review p. 11 says a draft temporary directive was published. FIX: "פרסם טיוטת הוראת שעה".
- **D20** bare digits ch02 l.14-ff., ch05 l.160: wrap in \en (cosmetic).
- **D21** ch06 l.50 "יחס ה־\term{הון העצמי רובד 1}" prints "ה־הון". FIX: "יחס \term{ההון העצמי רובד \en{1}}{CET1}".
- **D22** refs [2] "august", [22] "evidence", [41] broken quotes. FIX: {August}, {Evidence}; BdE title with single inner quotes. mizrahi_q3_2026 has no page numbers (D, T, G and minimum are on PDF pp. 69, 70, 167 and the capital note).
- **D23** ch07 l.162, 164: two manual \newpage. Layout is fine now but fragile; recheck after any ch07 edit.
- **D24** Fig 4.2 legend: labels touch the line samples; Fig 5.1 left boxes touch. Cosmetic.
- **D25** ch07 l.35: M-A (week 7, "models validated") precedes TSK-3.2 interviews ending week 8, which RSK-MOD-02 uses for validation. FIX: "מודלים מכוילים" instead of "מאומתים".
- **D26** data_sources UNSOLD_ANCHORS 2025-12 = 86,090 (unverified, interpolation line in fig 3.1) conflicts with BoI annual report ch. 8, which the report cites: about 83,000 at end-December 2025. FIX: use 83,000 or explain. Figure only, not in text.

## 5. Guide check after A2 dropped tables
WBS table (5 packages, tasks, deliverable), RACI, 8 coded tasks, predecessors, weeks and two milestones (in Gantt), critical path, risk table, 5x5 matrix, mitigation, contingency, residual < 12: present and consistent. Gantt dates agree with predecessors. Not exactly as in the guide: no separate task table (guide table 8.3; now a Gantt column), no WBS tree (guide fig 8.1), no risk "domain" column. Minimum met; the guide shows these as examples.

## 6. Sources opened
| Item | Result |
|---|---|
| Leumi Q3-2026 (PDF): CET1 11.38 / 70,936, RWA 623,358, min 10.23, E 71,442, D 91,223+58,094 = 149,317, T 171,691+66,727 = 238,418, P 2,208+1,160 = 3,368, G 47,972 | all match |
| Discount: CET1 10.32 / 35,821, RWA 347,080, min 9.21, E 35,098, D 56,484, T 90,415, P 1,251, G 17,480, tax 34.75% | all match |
| Mizrahi: CET1 10.10 / 37,170, RWA 368,119, min 9.60, E 36,667, D 54,442, T 98,698, P 668+41 = 709, G 18,293 | all match |
| Hapoalim: CET1 11.62 / 67,480, RWA 580,553, min 10.24, E 67,530, D 116,083, T 188,829, P 2,575, G 31,513 | found in the report; labels read only for part (Hebrew text layer is broken) |
| FIBI: CET1 10.28 / 14,730, RWA 143,282, E 14,533, T 36,206 | found; D, G, P and minimum not confirmed |
| Absorption CDF: 54,630 = 25,118+29,512; 19,593; 24,771; 968; BoI 8% and 33% (p. 154), average 58% | match; definitions differ (D04) |
| BoI stress: cumulative construction loss 3.3%, share 20.9%, NIS 84 bn (p. 140); 6.5% floor (2024 survey text) | match |
| MoF Aug-2026: 30%, five areas, 1 year+, May one fifth; 60% (p. 11, since Nov-24); 2,072 | match |
| TAM: 3.02 m (Nadlan 13733); 65,500, 34,000, 90.7 k (BoI ch. 8). SAM: 217.2 k (15410). SOM: 85,080, 86,666, 25.8, 9,190 (15819) | match; titles match |

## 7. Not verified
FIBI D, G, P and minimum; part of Hapoalim labels; TheMarker 86,290; Semerenko 5,081; Times of Israel and Trading Economics values; BIS; CBS 222/2026; BoI 1.5 pp CET1 drop (p. 134 text layer broken); land 81 and total 367 only located on pages, not read; academic papers' content not reopened (checked in the November 17 audit); order of spec and first run; claim that CBS inventory counts from permit (footnote not read); print legibility on paper; main.pdf is not yet in the project root (R16, A5).

## 8. Re-check after the fix round (Agent 7, 2026-11-24)
Object: copy of build/ (main.pdf of 17:18:54, 43 pp) in 07_detector/recheck/build; identical to the live build/ when compared. A later URL-font rebuild is NOT covered. Scripts: 07_detector/recheck/chk.py, scan.py.

| Item | Result | Evidence |
|---|---|---|
| D01 / R10 | PASS | Table 6.1 (p. 27): all 25 cells, A and B (50 values), equal the JSON m = 24 grids to one decimal; minimum 15.42 (A), 10.73 (B), so "all 25 exceed 10%" is true for both. 12-month ranges 7.5-19.9 / 0.5-4.8, centre 14.0 / 2.4, no-delay max 1.3 / 0 match |
| D02 | PASS | Pre-tax basis, REQ silence and the after-tax split stated in ch05; consequence in ch06 (6.3 figures, H3, key finding), ch07, abstract. 13.9 / 9.2 as in my own recomputation (the JSON holds no after-tax percent of equity) |
| D03 | PASS | All 9 severe-cell sensitivities plus after-tax reported, values match, grouping correct |
| D04 | PASS | ch05 limitations, ch06, abstract; 53% as computed before; 9.98 / 0.6 match |
| D05 | PASS | Limited to tested base-parameter scenarios in all 3 places; lowest CET1 at 40/40/24 is 6.62 (Leumi, A); 41.2% matches |
| D06 | PASS | Three named mechanisms; agrees with ch04 and ch07 |
| D07 | PASS | Text and caption |
| D08 | PASS | Claim replaced; the new cited pages (survey p. 187, Hapoalim p. 243) not reopened by me |
| D09 | PASS | Every entry whose bib record has a date prints it; BoI supervision author back. [28], [33], [41] have no date in the bib |
| D10 | PASS | Four titles restored. New Directive 329 date (27 Dec 2020) not independently checked |
| D11 | PASS | Direct URLs are the ones I opened in the first audit |
| Numbers ch05/06/07/abstract | PASS | As above |
| H3 verdict | PASS | "Not supported by the preset threshold, fragile, after tax inconclusive" in abstract, ch06 (H3, key finding), ch07; ch04 box compatible |
| H1-H3 ch01 = ch06 | PASS | Identical, all three |
| Abstract length | PASS | 336 words |
| Citations | PASS | 48 keys, none missing or uncited |
| BiDi scan | PASS | No new hits except one float option [!htb]; D20 hits gone; Hebrew in en 0, edge brackets 0 |
| Visual pages | PASS | Read: iii, 2, 8, 10, 11, 13, 15, 17-31, 32-36 (about 85 dpi). Table 6.1 LTR cells, bold cell, brackets and ranges right |
| Box titles | PASS | Right-aligned on all boxes seen |
| Bibliography pages | PASS | 5 pages, LTR, inside margins; last page has 4 entries |
| Regressions | PASS (none blocking) | See below |

Cosmetic, not blocking: (a) ch02 l.60 "ו אף" has a stray space (pre-existing; FIX "ואף"); (b) fig 5.1: the MoF box touches its CBS and BIS neighbours; (c) the paragraph before table 6.1 is split over pp. 25-27 by floats, readable; (d) ch06 l.61 heading "עמידות הממצא" next to "הממצא שברירי": the first concerns the grid, the second the assumptions; acceptable.
Blocking: none from these checks. Page count (43 vs 42) handled separately. If the rebuild changes the font, spot-check pp. 32-36 and the page breaks of ch07.
