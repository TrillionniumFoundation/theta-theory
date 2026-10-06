#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build evidence
python3 tools/verify_v12.py > evidence/v12-source-and-finite-checks.json
python3 -O tools/verify_v12.py > evidence/v12-source-and-finite-checks-optimized.json
cmp evidence/v12-source-and-finite-checks.json evidence/v12-source-and-finite-checks-optimized.json
for script in certify_winding certify_excursion verify verify_v2 check_v5 check_v6; do
  python3 "tools/${script}.py" > "evidence/${script}.py.json"
done
last=''
for pass in 1 2 3 4 5 6; do
  pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -recorder -output-directory=build main.tex > "build/pass${pass}.txt" 2>&1
  now="$(sha256sum build/main.aux | cut -d' ' -f1)"
  if [[ "$now" == "$last" ]] && ! grep -qE 'Rerun to|Please rerun' build/main.log; then break; fi
  last="$now"
done
if grep -Eq 'LaTeX Warning|Package .* Warning|Overfull|undefined' build/main.log; then
  grep -nE 'Warning|Overfull|undefined' build/main.log >&2
  exit 1
fi
python3 tools/receipt_v12.py > evidence/build-receipt.json
printf 'Built %s\n' "$PWD/build/main.pdf"
