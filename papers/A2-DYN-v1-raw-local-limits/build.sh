#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p build
python3 tools/certify_winding.py > build/winding-certificate.json
python3 tools/verify.py > build/finite-diagnostics.json
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -latexoption=-no-shell-escape -outdir=build main.tex
