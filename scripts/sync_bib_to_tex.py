import re
from pathlib import Path

root = Path(r"C:\Users\Guy\.gemini\antigravity\scratch\project_prep_report")
bib_text = (root / "references.bib").read_text(encoding="utf-8")

# Parse bib entries
entries = {}
pattern = re.compile(r"@(\w+)\s*\{\s*([^,]+)\s*,(.*?)\n\}", re.DOTALL)
for match in pattern.finditer(bib_text):
    etype, key, body = match.group(1).lower(), match.group(2).strip(), match.group(3)
    fields = {}
    for fmatch in re.finditer(r"(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", body, re.DOTALL):
        fname = fmatch.group(1).lower().strip()
        fval = " ".join(fmatch.group(2).split())
        fields[fname] = fval
    entries[key] = (etype, fields)

# Find citation order across chapters
tex_files = [root / "main.tex"] + sorted((root / "chapters").glob("ch*.tex"))
cited_order = []
for tf in tex_files:
    txt = tf.read_text(encoding="utf-8")
    for cm in re.finditer(r"\\cite\{([^}]+)\}", txt):
        for k in cm.group(1).split(","):
            k = k.strip()
            if k and k not in cited_order:
                cited_order.append(k)

for k in entries:
    if k not in cited_order:
        cited_order.append(k)

print(f"Parsed {len(entries)} bib entries, {len(cited_order)} cited in order.")

lines = [
    "% Auto-generated IEEE bibliography items from references.bib",
    "\\begin{english}",
    "\\begin{thebibliography}{99}",
    "\\small"
]

for key in cited_order:
    if key not in entries:
        print(f"WARNING: missing key {key}")
        continue
    etype, f = entries[key]
    author = f.get("author", "").replace("{", "").replace("}", "")
    title = f.get("title", "")
    # Protect Hebrew inside title if present
    title = re.sub(r"\(([^a-zA-Z0-9()]+)\)", "", title).strip()
    title = title.replace("{", "").replace("}", "")
    year = f.get("year", "")
    journal = f.get("journal", "")
    booktitle = f.get("booktitle", "")
    publisher = f.get("publisher", "")
    institution = f.get("institution", "")
    howpublished = f.get("howpublished", "")
    vol = f.get("volume", "")
    num = f.get("number", "")
    pages = f.get("pages", "")
    doi = f.get("doi", "")

    parts = [f"\\textbf{{{author}}}, ``{title},''"]
    if journal:
        parts.append(f"\\textit{{{journal}}},")
    elif booktitle:
        parts.append(f"in \\textit{{{booktitle}}},")
    elif institution:
        parts.append(f"\\textit{{{institution}}},")
    elif publisher:
        parts.append(f"\\textit{{{publisher}}},")
    elif howpublished:
        parts.append(f"\\textit{{{howpublished}}},")

    if vol:
        parts.append(f"vol.~{vol},")
    if num:
        parts.append(f"no.~{num},")
    if pages:
        parts.append(f"pp.~{pages},")
    if year:
        parts.append(f"{year}.")
    if doi:
        parts.append(f"DOI: \\texttt{{{doi}}}.")

    lines.append(f"\\bibitem{{{key}}} " + " ".join(parts))

lines.append("\\end{thebibliography}")
lines.append("\\end{english}")

(root / "resources" / "bibliography_items.tex").write_text("\n".join(lines), encoding="utf-8")
print("Successfully wrote resources/bibliography_items.tex")
