# Dr. Yoram Segal ("From Problem to PDF" & Lesson L03) Complete Methodology Checklist

This reference summarizes the mandatory structural, academic, and typographical rules from Dr. Yoram Segal's book (*"מהבעיה אל ה-PDF: המדריך לדוח המכין המקצועי"*) and Lesson **L03** (*"מסמך PDF מקצועי בלטך"*).

---

## 1. Document Architecture & Page Budget (Chapters 1, 2, 11 of the Book)
- **Document Class:** `\documentclass[12pt,a4paper,oneside]{book}` compiled with `LuaLaTeX`.
- **Page Geometry (Table 11.1):** A4 paper, `top=2.5cm`, `bottom=2.5cm`, `inner=3.0cm` (`2.5cm + 0.5cm` binding gutter), `outer=2.5cm`.
- **Fonts (Table 11.1 & Table 12.1):**
  - Hebrew Serif (body): `David` (`david.ttf` / `davidbd.ttf`).
  - Hebrew Sans-Serif (headings/tables): `Arial` (`arial.ttf` / `arialbd.ttf`).
  - English Serif: `Times New Roman` (`times.ttf`).
  - Monospace: `Courier New` (`cour.ttf`).
- **Frontmatter (Unnumbered / Roman):**
  1. **Cover Page (`\begin{titlepage}`):** Double border frame (`TikZ`), project title in Hebrew & English, team details, advisor, institution, date, and `\thispagestyle{empty}` (no page number on cover; **never** place keywords on the cover page).
  2. **Executive Summary (`תקציר מנהלים`):** On its own page, **250–350 words** summarizing Problem, Methodology, Quantitative Findings, and Recommendations, followed immediately at the bottom of the same page by **5–7 Keywords (`מילות מפתח`)**.
  3. **Lists:** `\tableofcontents`, `\listoffigures`, `\listoftables`, and an **Alphabetical Abbreviations Table (`רשימת קיצורים וראשי תיבות`)**.

---

## 2. Chapter-by-Chapter Engineering & Academic Requirements (Chapters 3–10 of the Book)

### Chapter 1: Introduction, Problem Definition, Requirements & Literature Review
- **Funnel Structure Diagram (`איור משפך`):** Visual `TikZ` funnel moving from Broad Macro/Domain Trend $\rightarrow$ Specific Anomaly $\rightarrow$ System Failure $\rightarrow$ Research Scope.
- **Quantitative Problem Definition (Chapter 3):** Explicit comparison of **Current State (`מצב מצוי`)** vs. **Desired State (`מצב רצוי`)** and the quantified **Gap (`הפער הכמותי`)**.
- **SMART Goals & Hypotheses ($H_1, H_2, H_3$):** Each hypothesis must state a specific numerical falsification threshold.
- **Formal Requirements Table (Chapter 4):** At least 6–8 requirements (`REQ-01` to `REQ-08`) with columns: ID, Category, Parameter Description, Target Numerical Value/Range, and Priority (`קריטי / גבוה / בינוני`).
- **Thematic Literature Review (Chapter 5):** Organized by **conceptual themes** (never chronological author-by-author summaries), accompanied by a **Literature Comparison Matrix Table** (at least 10 sources) and a deep-dive analysis of a **Flagship Paper (`מאמר דגל`)** including its core equation.

### Chapters 2, 3 & 4: Historical Benchmark, Market Sizing (`TAM/SAM/SOM`), and Comparative Analysis
- **3-Layer Market Segmentation (`TAM / SAM / SOM` – Section 6.1):** Visual `TikZ` concentric/layered diagram and table quantifying Total Addressable Market (`TAM`), Serviceable Available Market (`SAM`), and Serviceable Obtainable Market / Target Risk Cohort (`SOM`) in physical units and monetary value (`NIS` and `USD`).
- **Multi-Dimensional Comparative Analysis (Sections 6.2–6.3):** 8–10 parameter comparison table + visual `pgfplots` comparative profile chart + unique fault-line diagram (`TikZ`).

### Chapter 5: Methodology, Data Sources & Weighted Pugh Decision Matrix (Chapter 7)
- **3 Real Alternatives (`חלופות תכן מתודולוגיות`):** Present at least 3 distinct methodological/architectural alternatives (`Alt A`, `Alt B`, `Alt C`).
- **Weighted Pugh Decision Matrix (`מטריצת החלטה משוקללת`):**
  $$S_j = \sum_{i=1}^{m} w_i \cdot c_{ij}, \qquad \sum_{i=1}^{m} w_i = 1.00$$
  Include the full scoring table, a `pgfplots` bar chart comparing the weighted totals, and a **Weight Sensitivity Analysis (`בדיקת רגישות משקולות` of $\pm 20\%$)** proving robustness of the winning alternative.
- **System Block Diagram (`תרשים בלוקים של ארכיטקטורת המערכת`):** 4-layer data & simulation pipeline in `TikZ`.

### Chapter 6: Simulation Results & Stress-Testing Validation
- Present the quantitative outputs from `scripts/run_simulations_and_figures.py` (`simulation_results.json`), embed the 300-DPI figures, and provide a formal **Hypotheses Validation Table** comparing predicted thresholds against realized simulation metrics.

### Chapter 7: Work Plan (`WBS`, `RACI`, `Gantt`), Risk Management & Design Readiness (Chapters 8–10)
- **WBS Tree (`עץ תכולת עבודה`):** Visual `TikZ` hierarchy decomposing the project into 5 Work Packages (`WP 1.0–5.0`).
- **RACI Matrix (`מטריצת אחריות`):** Table mapping every task (`TSK-1.1` to `TSK-5.2`) across team roles. **Iron Rule:** Every row must have **exactly ONE `A` (Accountable)** and **at least one `R` (Responsible)**.
- **Gantt Chart (`תרשים גאנט`):** Visual `TikZ` schedule highlighting the **Critical Path in Red**, parallel tasks in Blue, at least **2 Milestones as Green Diamonds**, and **Safety Buffers (`מרווחי ביטחון`) in Gold**.
- **Double Risk Quantification (`כימות סיכונים כפול` – Chapter 9):**
  $$R_{\text{initial}} = P_{\text{pre}} \times I_{\text{pre}} \;\longrightarrow\; R_{\text{residual}} = P_{\text{post}} \times I_{\text{post}}$$
  Include a `5x5` visual Risk Matrix (`TikZ`) showing risk migration (`Rk -> Rk'`) and a Risk Register Table where every risk with $R_{\text{initial}} \ge 12$ has both a **Preventive Mitigation Plan (`תוכנית הפחתה מונעת`)** and a **Trigger-Based Contingency Plan (`תוכנית מגירה`)**.
- **Design Readiness (`מוכנות תכנונית` – Chapter 10):** Conclude with a `TikZ` diagram of **3 Immediate Post-Approval Actions**.

---

## 3. The 9 Defect Families Checklist (Chapter 19 of the Book)
1. **Cover & Abstract Defects:** Missing double frame, page number on cover, keywords on cover instead of bottom of Executive Summary.
2. **BiDi & Number/Acronym Reversal:** Unwrapped numbers, percentages, currencies, or English acronyms in RTL paragraphs.
3. **Box & Diagram Overflow:** `tcolorbox` or `tikzpicture` not wrapped in `\begin{english}...\end{english}`.
4. **Caption Position & Floating Objects:** Table captions must be **above** tables; Figure captions must be **below** figures; every figure and table must be referenced by number in the body text.
5. **Orphan Headings:** Section headings at the bottom of a page without following text.
6. **Vague Problem/Requirements:** Non-quantified problem statements or requirements without target metrics.
7. **Unjustified Methodology:** Missing Pugh Matrix or missing weight sensitivity check.
8. **Invalid RACI / Gantt / Risk Table:** Multiple `A`s in a RACI row, Gantt without a critical path or buffers, or high risks ($R \ge 12$) without contingency plans.
9. **Bibliography Mismatch:** Citations in text missing from `references.bib`, or uncited entries in `references.bib`.
