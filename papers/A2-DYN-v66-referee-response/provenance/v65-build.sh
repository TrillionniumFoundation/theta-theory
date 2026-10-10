#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build evidence
python3 ../A2-DYN-v63-referee-response/tools/verify_v63.py > evidence/v63-baseline-recheck.json
python3 tools/verify_v65.py > evidence/v65-source-and-finite-checks.json
python3 -O tools/verify_v65.py > evidence/v65-source-and-finite-checks-optimized.json
cmp evidence/v65-source-and-finite-checks.json evidence/v65-source-and-finite-checks-optimized.json
for script in certify_winding certify_excursion verify verify_v2 check_v5 check_v6; do
  python3 "tools/${script}.py" > "evidence/${script}.py.json"
done
last=''
for pass in 1 2 3 4 5 6; do
  if ! pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -recorder -output-directory=build main.tex </dev/null > "build/pass${pass}.txt" 2>&1; then
    tail -80 "build/pass${pass}.txt"
    exit 1
  fi
  now=$(sha256sum build/main.aux | cut -d' ' -f1)
  if [ "$now" = "$last" ] && ! grep -Eq 'Rerun to|Please rerun' build/main.log; then break; fi
  last="$now"
done
if grep -Eq 'LaTeX Warning|Package .* Warning|Overfull|undefined|Missing character' build/main.log; then
  grep -En 'LaTeX Warning|Package .* Warning|Overfull|undefined|Missing character' build/main.log
  exit 1
fi
python3 tools/receipt_v65.py > evidence/build-receipt.json
