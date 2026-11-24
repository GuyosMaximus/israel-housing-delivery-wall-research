# Template commands — Housing Project prep report (Agent 4 / Design)

Use **only** these commands. Need something else? Ask in `comms/inbox/to_agent4.md`.
Engine: **LuaLaTeX + biber** (babel `bidi=basic`, Hebrew main, English LTR). Build from `build/` with `build.ps1` or `build.sh`
(lualatex → biber → lualatex → lualatex).

## 1. BiDi / English marking (guide ch.14, Prompt B1)
| Command | Use | Example |
|---|---|---|
| `\en{...}` | Any English word, phrase, acronym, name, number, range, date, or version, as **one LTR unit** | `\en{Bank of Israel}`, `\en{2022–2026}`, `\en{v1.2}` |
| `\textenglish{...}` | Alias of `\en` (kept for existing drafts) | `\textenglish{LTV}` |
| `\term{עברית}{English}` | First use of a professional term → "עברית (English)" | `\term{מבחן קיצון}{Stress Test}` |
| `\enp{עברית}{English}` | Hebrew with its English equivalent in brackets. Brackets stay correct everywhere: nested brackets, headings, captions, tables, inside an English block. Do not type the outer brackets yourself | `\enp{חוק המכר (דירות)}{Sale (Apartments) Law}` |
| `\pct{25}` | Percentage, LTR unit → 25% | `\pct{3.25}` |
| `\deal{20/80}` | Deal structure, LTR unit | `\deal{20/50/30}` |
| `\nis{1,500}` | Shekel amount → ₪1,500 | `\nis{2,350,000}` |
| `\he{...}` / `\texthebrew{...}` | Hebrew **inside** an English environment (TikZ, code, formula) | `\he{הבנק}` |
| `\mathhe{...}` | Hebrew text inside math | `R = P \times I \; \mathhe{(סיכון)}` |
| `\begin{english}...\end{english}` | LTR block: every TikZ picture and code listing | see `figures/tikz_*.tex` |

`\term{עברית}{English}` is the same form, for the first use of a term. For brackets around an English unit alone, keep them outside: `(\en{LTV})`; brackets that belong to the English phrase go inside: `\en{f(x)}`.

Never put Hebrew inside `\en{}`. Never type Hebrew backwards to "fix" it. Report repeated problems to A4.

## 1b. Headings
Numbering and TOC go down to `\subsubsection` (`secnumdepth=3`, `tocdepth=3`). `\paragraph` stays unnumbered and out of the TOC.

## 2. Boxes (tcolorbox; RTL-safe, never split across pages)
| Environment | Purpose | Default title |
|---|---|---|
| `managerbox` | **Opens every chapter** (brief §7) | למה זה חשוב למנהל |
| `keyfinding` | Key finding | ממצא מרכזי |
| `keybox` | Key message (guide name) | מסר מרכזי |
| `methodology` | Methodological note: assumptions, "בהנחה כי", "תרחיש" | הערה מתודולוגית |
| `researchquestion` | Research question / hypotheses (ch01, ch06) | שאלת המחקר |
| `riskalert` / `warnbox` | Risk / pitfall warning | התראת סיכון / שימו לב |
| `projectbox` | Applying a point to our project | בפרויקט שלנו |

Custom title: `\begin{keyfinding}[ממצא 2: ...] ... \end{keyfinding}`.
`\ResearchQuestion` prints the verbatim research question (single source, in `preamble.tex`).

## 3. Tables (caption ABOVE, first column on the RIGHT, width ≤ 12.4 cm)
| Command | Use |
|---|---|
| `\tabmaxwidth` | Max table width (12.4 cm): `\begin{tabularx}{\tabmaxwidth}{R C C}` |
| `R` / `C` / `L` | Flexible X columns: right / centered / left aligned (Hebrew paragraphs) |
| `E` | Flexible column whose **whole cell is English** (LTR, left aligned) |
| `\hd{...}` | Shaded bold header cell |
| `\toprule \midrule \bottomrule` | booktabs rules (no vertical lines) |

```latex
\begin{table}[htbp]\centering
\caption{...}\label{tab:xxx}
\begin{tabularx}{\tabmaxwidth}{R C C}
\toprule
\hd{פרמטר} & \hd{\en{US 2008}} & \hd{\en{Israel 2026}} \\
\midrule
שיעור מימון מרבי & \pct{100} & \pct{75} \\
\bottomrule
\end{tabularx}
\end{table}
```
Inside tables, put line breaks `\\` on their own (`... \\` then a new line with `\midrule`).

## 4. Figures (caption BELOW, referenced in the text BEFORE the float)
```latex
כפי שמוצג באיור~\ref{fig:xxx}, ...
\begin{figure}[htbp]\centering
\includegraphics[width=0.9\textwidth]{fig_name.pdf}   % graphicspath = figures/
\caption{כיתוב בעברית}\label{fig:xxx}
\end{figure}
```
Ready TikZ figures (A4):
- `figures/tikz_credit_triangle.tex`: buyer / developer / bank flows in 20/80 and 20/50/30 → `\input{figures/tikz_credit_triangle.tex}`
- `figures/tikz_gantt_chart.tex`: research Gantt (critical path in red, milestones M1–M3, today line) → `\input{figures/tikz_gantt_chart.tex}` in ch07. A2 may edit the task rows inside the `\foreach` list. Keep each label to one line (≤ 4.8 cm).

TikZ rule: no `text width` on nodes with Hebrew text. Under LuaLaTeX, automatically wrapped RTL text inside a node is mis-measured. Break lines explicitly with `\\` and wrap each line in `\he{}`.

## 5. Citations & misc
| Command | Use |
|---|---|
| `\cite{key}` | IEEE numbered citation (biblatex/biber); entries in `build/references.bib` |
| `\todo{...}` | Red placeholder **[להשלמה: ...]**. The detector searches for it; none may remain at submission |
| `\label{ch:..}`, `\label{sec:..}`, `\label{fig:..}`, `\label{tab:..}`, `\label{eq:..}` | Label prefixes |

## 6. Palette (shared with Python charts, A3)
| Name | Hex | Role |
|---|---|---|
| brandNavy | `#1F3A5F` | headings, frames, series 1 |
| brandSteel | `#4A6FA5` | sub-headings, series 2 |
| brandRed | `#B03A2E` | risk, critical path, series 3 |
| brandAmber | `#D68910` | warnings, milestones, series 4 |
| brandGreen | `#1E8449` | cash flow, safe, series 5 |
| brandOlive | `#8C8A4B` | manager box |
| brandHead | `#DCE6F2` | table header fill |
| brandPale | `#EAF1FB` | light fills |

## 7. File map (build/)
`main.tex` → `preamble.tex` · `frontmatter/{titlepage,copyright,abstract,acronyms}.tex` · `chapters/ch01_research_framework … ch07_risks_and_gantt.tex` · `figures/` · `references.bib`.
Metadata (authors, supervisor, course, date) lives only in `preamble.tex` (`\ReportTitle`, `\ReportSubtitle`, `\ReportTitleEn`, `\ReportSubtitleEn`, `\Authors`, `\Supervisor`, `\CourseLine`, `\ReportDate`).
