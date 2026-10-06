#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build evidence
args=()
if [ "${A2_DYN_ALLOW_MISSING_REPORT:-0}" = 1 ]; then
  test -z "${GITHUB_ACTIONS:-}"
  args+=(--allow-missing-report)
fi
python3 tools/verify_v26.py "${args[@]}" > evidence/v26-source-and-finite-checks.json
python3 -O tools/verify_v26.py "${args[@]}" > evidence/v26-source-and-finite-checks-optimized.json
cmp evidence/v26-source-and-finite-checks.json evidence/v26-source-and-finite-checks-optimized.json
for script in certify_winding certify_excursion verify verify_v2 check_v5 check_v6; do
  python3 "tools/${script}.py" > "evidence/${script}.py.json"
done
last=''
for pass in 1 2 3 4 5 6; do
  if ! pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -recorder -output-directory=build main.tex > "build/pass${pass}.txt" 2>&1; then
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
python3 tools/receipt_v26.py > evidence/build-receipt.json
