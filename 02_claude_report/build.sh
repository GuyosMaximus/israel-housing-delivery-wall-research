#!/usr/bin/env bash
# build.sh — 4-pass build of the prep report (run from build/)
#   lualatex -> biber -> lualatex -> lualatex   (brief §4)
cd "$(dirname "$0")" || exit 1
lualatex -interaction=nonstopmode main.tex > /dev/null 2>&1
biber main
lualatex -interaction=nonstopmode main.tex > /dev/null 2>&1
lualatex -interaction=nonstopmode main.tex > /dev/null 2>&1
echo '--- build summary ---'
grep -nE '^!|Output written|undefined|Overfull' main.log
