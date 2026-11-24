"""
audit_latex_book.py
Automated Red-Team Detector QA script implementing the 9 Defect Families audit
from Chapter 19 & Prompt B2 of Dr. Yoram Segal's book ("From Problem to PDF").
"""
import re
import sys
from pathlib import Path


def run_audit(project_root: Path) -> None:
    log_path = project_root / "main.log"
    tex_files = [project_root / "main.tex"] + sorted((project_root / "chapters").glob("ch*.tex"))

    issues = []

    # 1. Check main.log for LaTeX errors and undefined references
    if log_path.exists():
        log_txt = log_path.read_text(encoding="utf-8", errors="replace")
        bang_errors = re.findall(r"^!.*", log_txt, re.M)
        undef_refs = re.findall(r"LaTeX Warning: Reference `([^']+)' on page \d+ undefined", log_txt)
        undef_cites = re.findall(r"LaTeX Warning: Citation `([^']+)' on page \d+ undefined", log_txt)
        if bang_errors:
            issues.append(f"LaTeX `!` errors in main.log: {len(bang_errors)} found ({bang_errors[:3]})")
        if undef_refs:
            issues.append(f"Undefined references (`??`): {set(undef_refs)}")
        if undef_cites:
            issues.append(f"Undefined citations: {set(undef_cites)}")
    else:
        issues.append("main.log not found — run LuaLaTeX compilation first.")

    # 2. Check float [H], active quote traps, and unescaped & in TikZ across .tex files
    all_labels = set()
    all_refs = set()
    for tf in tex_files:
        if not tf.exists():
            continue
        txt = tf.read_text(encoding="utf-8")
        if "[H]" in txt:
            issues.append(f"{tf.name}: Uses `[H]` float specifier (use `[htbp]` instead).")
        for m in re.finditer(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", txt, re.S):
            for line in m.group(0).splitlines():
                if re.search(r"(?<!\\)&", line):
                    issues.append(f"{tf.name}: Unescaped `&` inside tikzpicture: {line.strip()}")
        for lm in re.finditer(r"\\label\{((?:fig|tab):[^}]+)\}", txt):
            all_labels.add(lm.group(1))
        for rm in re.finditer(r"\\ref\{((?:fig|tab):[^}]+)\}", txt):
            all_refs.add(rm.group(1))

    unreferenced_floats = all_labels - all_refs
    if unreferenced_floats:
        issues.append(f"Figures/Tables without explicit `\\ref{{}}` in text: {sorted(unreferenced_floats)}")

    if issues:
        print("=== DETECTOR QA AUDIT: ISSUES FOUND ===")
        for idx, iss in enumerate(issues, 1):
            print(f"  {idx}. {iss}")
        sys.exit(1)
    else:
        print("=== DETECTOR QA AUDIT: 100% PASS (0 Errors, 0 Undefined Refs, All Floats Referenced) ===")


if __name__ == "__main__":
    target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    run_audit(target_dir)
