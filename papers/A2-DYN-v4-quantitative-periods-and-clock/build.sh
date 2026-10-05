#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p build
python3 tools/certify_winding.py > build/winding.json
python3 tools/certify_excursion.py > build/excursion.json
python3 tools/verify.py > build/v1-finite.json
python3 tools/verify_v2.py build/excursion.json > build/v2-finite.json
python3 tools/audit_v4.py > build/v4-audit.json
python3 -O tools/audit_v4.py > build/v4-audit-optimized.json
cmp build/v4-audit.json build/v4-audit-optimized.json
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -no-shell-escape -recorder -output-directory=build main.tex > build/latex-pass-1.txt
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -no-shell-escape -recorder -output-directory=build main.tex > build/latex-pass-2.txt
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -no-shell-escape -recorder -output-directory=build main.tex > build/latex-pass-3.txt
