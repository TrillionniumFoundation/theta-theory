#!/usr/bin/env bash
# Compile the complete revision, with shell escape disabled.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v latexmk >/dev/null || { echo 'latexmk is required' >&2; exit 2; }
command -v pdflatex >/dev/null || { echo 'pdflatex is required' >&2; exit 2; }
for entry in two_collision main_v77 rigidity_v77 response_v77; do
  latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
    -pdflatex='pdflatex -no-shell-escape %O %S' "$entry.tex"
  if grep -Eq 'There were undefined references|Citation .* undefined|Reference .* undefined|multiply defined|Overfull \\[hv]box' "$entry.log"; then
    echo "Unresolved references or layout overflow in $entry.log" >&2
    exit 3
  fi
done
python tools-v77/check_revision_v77.py
