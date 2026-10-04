#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
command -v latexmk >/dev/null || { echo "latexmk is required" >&2; exit 1; }
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder main.tex
