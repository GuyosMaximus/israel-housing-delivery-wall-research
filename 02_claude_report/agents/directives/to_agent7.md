

## [2026-11-24] RED TEAM REMEDIATION — read comms/red_team_remediation.md first (G1–G9 bind you)
R15 and verification of R01–R14. Read-only on build/.
- Script in 07_detector/scripts: scan main.tex, preamble.tex, frontmatter, ch01–ch07 for Latin letters outside `\en`/`\textenglish`/`\term`/`\enp`/english env, excluding commands, labels, cites, math, TikZ/table options, comments. Scan also for parentheses next to Latin text. Report true vs false positives honestly.
- Render every page to PNG and look for inverted brackets, e.g. "(Hedge Finance (גידור", "(Financial Instability) Hypothesis"; pdftotext is unreliable for Hebrew here.
- Audit against the guide and R01–R14; recompute CET1 arithmetic from data_summary.json independently; spot-check new sources on the web; check text numbers against data_summary.json, and the H3 verdict against REQ-H3-01.
Write comms/reviews/detector_remediation.md with PASS/FAIL per ID and severity. Flag comms/detector_remediated.flag = audit complete (not "all pass").
