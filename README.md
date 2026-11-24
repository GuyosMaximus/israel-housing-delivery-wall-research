# דוח מכין לפרויקט מחקר: מבצעי המימון הקבלניים, הלוואות הבלון ו"קיר המסירות" (2026–2027)

פרויקט זה מציג **דוח מכין לפרויקט מחקר (Preliminary Research & Design Report)** בפורמט ספר אקדמי מלא ב-`LuaLaTeX`, שנבנה לפי מתודולוגיית הספר *"מהבעיה אל ה-PDF: המדריך לדוח המכין המקצועי"* ושיעור **L03** מאת **ד"ר יורם סגל**.

---

## 1. שאלת המחקר המרכזית
> *"באיזו מידה מבצעי המימון הקבלניים, הלוואות הבלון ומינוף היזמים בשוק הנדל"ן הישראלי (2022–2026) משחזרים את מנגנוני הכשל של משבר הסאב-פריים (2008), ומהי עמידות המערכת הבנקאית והיזמית בישראל בפני גל חדלות פירעון בעת 'קיר המסירות' של 2026–2027?"*

### השערות המחקר הנבחנות:
* **השערה $H_1$ (רמת משק הבית – `Payment Shock` וכשל חיתום דחוי):** מבצעי הדחייה הליניאריים (`20/80`, `10/90`) והלוואות הבלון המסובסדות מגלמים הנחת `NPV` כלכלית סמויה ($\delta_{\text{NPV}} \approx 10\%\text{--}12.4\%$) שיצרה אשליית יציבות מחירים נומינלית, אך חושפים מעל `50%` מהרוכשים לחריגה מרף יחס ההחזר להכנסה ($\text{PTI} > 40\%$) בעת פקיעת הבלון ומועד המסירה.
* **השערה $H_2$ (רמת היזם – פגיעות דיפרנציאלית ואשראי מזנין חוץ-בנקאי):** בעוד שחברות בנייה גדולות (`Tier-1`) מחזיקות בכריות נזילות המספיקות לספיגת עיכובי מסירות, יזמים קטנים ובינוניים (`Tier-2 / Tier-3`) הממונפים באשראי קרקע ובאשראי השלמת הון (`Mezzanine`) חוץ-בנקאי ייקלעו ליחס כיסוי חוב שלילי ($\text{DSCR} < 1.0$) כבר בגל ביטולים או עיכובים של `10%–20%`.
* **השערה $H_3$ (רמת המערכת הבנקאית – חומת האש המוסדית בישראל):** בזכות השילוב של חוק המכר (ליווי בנקאי סגור וערבויות חוק מכר), משטר ה-`Full Recourse` בישראל, היעדר איגוח סאב-פריים (`MBS/CDO`) והוראת השעה של בנק ישראל ממרץ 2025, ליבת המערכת הבנקאית המסחרית תשמור על יחס הון עצמי רובד 1 ($\text{CET1} \ge 9.0\%$) ולא תחווה קריסה מערכתית בנוסח ארה"ב 2008.

---

## 2. עץ התיקיות והקבצים בפרויקט (`Directory Tree`)

```text
project_prep_report/
├── .gitignore                              # סינון קובצי קומפילציה זמניים של LaTeX ו-Python
├── README.md                               # תיעוד הפרויקט, שאלת המחקר, עץ התיקיות ותפקידי הסוכנים
├── main.tex                                # קובץ המאסטר של הספר (\documentclass[12pt,a4paper,oneside]{book})
├── preamble.tex                            # הגדרות חבילות, עברית RTL מלאה, גופנים, תיבות ופקודות BiDi
├── references.bib                          # מאגר הביבליוגרפיה המלא בתקן BibTeX / IEEE
├── main.pdf                                # גרסה א' של הספר המקומפל (Antigravity Build)
├── claude_version.pdf                      # גרסה ב' של הספר המקומפל (Claude Build להשוואה)
├── red_team_comparison.md                  # דוח השיפוט וההשוואה ראש-בראש של ועדת הצוות האדום
│
├── agents/                                 # תיעוד צוות הסוכנים, הרובריקות ודוחות הבקרה
│   ├── 01_expert_committee.md              # סוכן ועדת המומחים והרובריקה המחייבת (Rubric Guidelines)
│   ├── 02_latex_architect_and_writers.md   # אדריכל ה-LaTeX וצוות סוכני הכתיבה של 7 הפרקים
│   ├── 03_python_viz_and_audit.md          # מהנדס הסימולציות בפייתון ודוח סוכן הדטקטור (Detector Report)
│   └── 04_red_team_reviewer.md             # סוכן ועדת הצוות האדום ומתודולוגיית השיפוט ההשוואתי
│
├── chapters/                               # 7 פרקי הספר המודולריים ב-LaTeX
│   ├── ch01_research_framework.tex         # פרק א': הגדרת המחקר, מסגרת תיאורטית, דרישות ומאמר הדגל
│   ├── ch02_us_subprime_2008.tex           # פרק ב': אנטומיה של משבר הסאב-פריים בארה"ב (2001–2008)
│   ├── ch03_israel_housing_2022_2026.tex   # פרק ג': שוק הדיור בישראל, TAM/SAM/SOM ומודל הנחת ה-NPV
│   ├── ch04_comparative_analysis.tex       # פרק ד': ניתוח השוואתי ישראל 2026 מול ארה"ב 2008 ומפת הסיכונים
│   ├── ch05_methodology_and_data.tex       # פרק ה': מאגרי נתונים, מטריצת פיו (Pugh) והמודלים הכמותיים
│   ├── ch06_delivery_wall_resilience.tex   # פרק ו': תוצאות סימולציות העמידות ב"קיר המסירות" (2026–2027)
│   └── ch07_risks_and_gantt.tex            # פרק ז': תוכנית עבודה (WBS, RACI, Gantt), ניהול סיכונים ומוכנות
│
├── figures/                                # גרפים ברזולוציית דפוס (300 DPI) המופקים מפייתון ומוטמעים בספר
│   ├── fig01_npv_discount_curves.png       # עקומות הנחת ה-NPV הסמויה במבצעי 20/80, 10/90 ו-20/50/30
│   ├── fig02_payment_shock_distribution.png# התפלגות יחס ההחזר להכנסה (PTI) בסימולציית מונטה-קרלו
│   ├── fig03_israel_inventory_vs_rates.png # מלאי הדירות החדשות הלא-מכורות בישראל מול ריבית בנק ישראל
│   ├── fig04_developer_stress_test.png     # מבחן קיצון ליחס כיסוי החוב (DSCR) של יזמי Tiers 1–3
│   └── fig05_bank_cet1_resilience.png      # מסלול יחס הון CET1 של הבנקים בישראל מול ארה"ב 2008
│
├── resources/                              # תבניות LaTeX, רשימת תיוג מתודולוגית ופריטי ביבליוגרפיה
│   ├── bibliography_items.tex              # פריטי הביבליוגרפיה המסונכרנים בתקן IEEE מתוך references.bib
│   ├── main_template.tex                   # תבנית קובץ מאסטר גנרית לדוח מכין בפורמט ספר
│   ├── methodology_checklist.md            # רשימת התיוג המלאה לפי הספר של ד"ר יורם סגל ושיעור L03
│   └── preamble_template.tex               # תבנית קדם-מסמך גנרית לעברית RTL ב-LuaLaTeX
│
└── scripts/                                # סקריפטי Python לסימולציות, סנכרון ביבליוגרפיה ובקרת איכות
    ├── audit_latex_book.py                 # סקריפט בדיקה אוטומטי של 9 משפחות הליקויים (Detector QA)
    ├── run_simulations_and_figures.py      # מנוע הסימולציות הכמותיות וייצור הגרפים ב-300 DPI
    ├── simulation_results.json             # פלט התוצאות הכמותיות המסונכרן עם טבלאות הספר
    └── sync_bib_to_tex.py                  # סנכרון אוטומטי של references.bib עם הציטוטים בפרקים
```

---

## 3. ארכיטקטורת צוות הסוכנים (`Multi-Agent Workflow`)

הפרויקט פותח ונבדק באמצעות ארבעה סוכנים מתמחים המתועדים בתיקיית [`agents/`](./agents/):

1. **[`agents/01_expert_committee.md`](./agents/01_expert_committee.md) — סוכן ועדת המומחים (Expert Committee):**
   מתרגם את מתודולוגיית ד"ר יורם סגל (*"מהבעיה אל ה-PDF"* ושיעור `L03`) לרובריקה מחייבת, מגדיר את תקציב העמודים, מפרט הדרישות הכמותיות (`REQ-RES-01` עד `REQ-RES-08`), וכללי הברזל ל-`BiDi` ב-`LuaLaTeX`.
2. **[`agents/02_latex_architect_and_writers.md`](./agents/02_latex_architect_and_writers.md) — אדריכל ה-LaTeX וצוות סוכני הכתיבה:**
   אחראי על תשתית העימוד ב-[`preamble.tex`](./preamble.tex) וב-[`main.tex`](./main.tex), ועל הכתיבה המודולרית של שבעת פרקי הספר בתיקיית [`chapters/`](./chapters/), כולל דיאגרמות `TikZ` וגרפי `pgfplots` וקטוריים.
3. **[`agents/03_python_viz_and_audit.md`](./agents/03_python_viz_and_audit.md) — סוכן הסימולציות בפייתון וסוכן הדטקטור (Detector QA):**
   מריץ את מודלי ה-`NPV`, סימולציית המונטה-קרלו ($N=10,000$) ומבחני הקיצון ב-[`scripts/run_simulations_and_figures.py`](./scripts/run_simulations_and_figures.py), מייצר את הגרפים בתיקיית [`figures/`](./figures/), ומבצע ביקורת איכות אוטומטית על 9 משפחות הליקויים מפרק 19 בספר.
4. **[`agents/04_red_team_reviewer.md`](./agents/04_red_team_reviewer.md) — סוכן ועדת הצוות האדום (Red-Team Reviewer):**
   מבצע שיפוט השוואתי מחמיר ראש-בראש בין גרסה א' ([`main.pdf`](./main.pdf)) לבין גרסה ב' ([`claude_version.pdf`](./claude_version.pdf)), מאתר כשלי סף מתודולוגיים וטיפוגרפיים, ומגבש את דוח ההשוואה המלא ב-[`red_team_comparison.md`](./red_team_comparison.md).

---

## 4. הוראות הרצה וקומפילציה (`Reproducibility`)

1. **הרצת הסימולציות וייצור הגרפים מחדש בפייתון:**
   ```bash
   python scripts/run_simulations_and_figures.py
   ```
2. **סנכרון הביבליוגרפיה מתוך `references.bib`:**
   ```bash
   python scripts/sync_bib_to_tex.py
   ```
3. **קומפילציה של הספר ב-`LuaLaTeX` (שני סבבים לעדכון תוכן העניינים וההפניות):**
   ```bash
   lualatex --disable-installer -interaction=nonstopmode main.tex
   lualatex --disable-installer -interaction=nonstopmode main.tex
   ```
4. **הרצת בדיקת האיכות האוטומטית (Detector QA):**
   ```bash
   python scripts/audit_latex_book.py
   ```
