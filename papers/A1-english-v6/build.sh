#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
if [[ $# -gt 1 || ( $# -eq 1 && "$1" != "--complete" ) ]]; then
  echo "Usage: bash build.sh [--complete]" >&2
  exit 2
fi
command -v python >/dev/null || { echo 'Python is required' >&2; exit 1; }
command -v latexmk >/dev/null || { echo 'latexmk is required' >&2; exit 1; }
python tests/test_v6.py
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -pdflatex='pdflatex -no-shell-escape %O %S' main.tex
if [[ ${1:-} == '--complete' ]]; then
  [[ -f legacy/main.tex ]] || { echo 'The pinned legacy subtree is missing; use the full Git checkout.' >&2; exit 1; }
  ( cd legacy && latexmk -pdf -interaction=nonstopmode -halt-on-error \
    -pdflatex='pdflatex -no-shell-escape %O %S' main.tex )
  latexmk -pdf -interaction=nonstopmode -halt-on-error \
    -pdflatex='pdflatex -no-shell-escape %O %S' complete.tex
fi
