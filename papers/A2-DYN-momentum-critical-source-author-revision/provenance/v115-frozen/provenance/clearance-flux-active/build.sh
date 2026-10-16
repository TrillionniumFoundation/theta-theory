#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build manuscript
for script in check_manifest check_source check_finite check_research check_load check_clearance; do
  python3 "tools/$script.py" > "build/$script.json"
  python3 -O "tools/$script.py" > "build/$script-optimized.json"
  cmp "build/$script.json" "build/$script-optimized.json"
done
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error -recorder -output-directory=build main.tex > "build/main-pass${pass}.txt" 2>&1
done
python3 tools/audit_tex.py > build/typesetting.json
pdftoppm -r 90 -png build/main.pdf build/page >/dev/null 2>&1
cp build/main.pdf manuscript/A2-DYN-clearance-flux.pdf
