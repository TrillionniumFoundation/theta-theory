#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build evidence
python3 tools/audit_source.py > evidence/source-audit.json
python3 -O tools/audit_source.py > evidence/source-audit-optimized.json
cmp evidence/source-audit.json evidence/source-audit-optimized.json
for script in certify_winding certify_excursion verify verify_v2 check_v5 check_v6; do
  python3 "tools/${script}.py" > "evidence/${script}.py.json"
  python3 -O "tools/${script}.py" > "evidence/${script}.py-optimized.json"
  cmp "evidence/${script}.py.json" "evidence/${script}.py-optimized.json"
done
last=''
for pass in 1 2 3 4 5 6; do
  pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error \
    -file-line-error -recorder -output-directory=build main.tex > "build/pass${pass}.txt" 2>&1
  now="$(sha256sum build/main.aux | cut -d' ' -f1)"
  if [[ "$now" == "$last" ]] && ! grep -qE 'Rerun to|Please rerun' build/main.log; then break; fi
  last="$now"
done
if grep -Eq 'LaTeX Warning|Package .* Warning|Overfull|Underfull|undefined' build/main.log; then
  grep -nE 'Warning|Overfull|Underfull|undefined' build/main.log >&2
  exit 1
fi
python3 tools/make_receipt.py > evidence/build-receipt.json
printf 'Built %s\n' "$PWD/build/main.pdf"
