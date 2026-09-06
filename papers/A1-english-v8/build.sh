#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
if [[ $# -ne 0 ]]; then echo 'Usage: bash build.sh' >&2; exit 2; fi
PYTHON=$(command -v python3 || command -v python) || { echo 'Python 3 is required' >&2; exit 1; }
command -v pdflatex >/dev/null || { echo 'pdflatex is required' >&2; exit 1; }
"$PYTHON" tests/test_v7.py
"$PYTHON" tests/test_v8.py
for pass in 1 2 3; do
  pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex > "build-pass-${pass}.txt"
done
if grep -Eq 'There were undefined references|Citation .* undefined|Reference .* undefined|Overfull \\[hv]box' main.log; then
  echo 'Unresolved reference, citation, or overfull box in main.log' >&2
  grep -E 'undefined|Overfull' main.log >&2
  exit 1
fi
printf 'A1 v8 principal manuscript and finite diagnostics built successfully.\n'
