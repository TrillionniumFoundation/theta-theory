#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build evidence
python3 tools/verify_v70.py > evidence/v70-source-and-finite-checks.json
python3 -O tools/verify_v70.py > evidence/v70-source-and-finite-checks-optimized.json
cmp evidence/v70-source-and-finite-checks.json evidence/v70-source-and-finite-checks-optimized.json
for script in certify_winding certify_excursion verify verify_v2 check_v5 check_v6; do
  python3 "tools/${script}.py" > "evidence/${script}.py.json"
done
last=''
stable=0
for pass in 1 2 3 4 5 6; do
  if ! pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -recorder -output-directory=build main.tex </dev/null > "build/pass${pass}.txt" 2>&1; then
    tail -80 "build/pass${pass}.txt"
    exit 1
  fi
  now=$(sha256sum build/main.aux | cut -d' ' -f1)
  if [ "$now" = "$last" ] && ! grep -Eq 'Rerun to|Please rerun' build/main.log; then stable=1; break; fi
  last="$now"
done
if [ "$stable" -ne 1 ]; then echo 'TeX references did not stabilize'; exit 1; fi
if grep -Eq 'LaTeX Warning|Package .* Warning|Overfull|undefined|Missing character' build/main.log; then
  grep -En 'LaTeX Warning|Package .* Warning|Overfull|undefined|Missing character' build/main.log
  exit 1
fi
python3 tools/render_v70.py
