

## [2026-11-24] RED TEAM REMEDIATION — read comms/red_team_remediation.md first (G1–G9 bind you)
R16. After detector_remediated.flag. You may edit all of build/.
Fix every FAIL; wrap English (Hebrew outside, e.g. `גידור פיננסי (\en{Hedge Finance})`) ; trim to 38–42 pp under G5; build lualatex → biber → lualatex ×2 (G1); 0 errors, 0 undefined, no overfull > 5pt. Verify all ch01–07, preamble, references.bib and .py exist in build/. Copy main.pdf to the project root. Sync final chapters back to agent folders. Post a fix log in 05_fixer/fix_log.md. Do NOT raise red_team_closed.flag until the Detector re-check passes.
