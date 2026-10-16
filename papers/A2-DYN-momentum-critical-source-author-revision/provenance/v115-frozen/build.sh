#!/usr/bin/env bash
# The no-argument route performs every gate in order.  Stages allow exactly
# the same gates to be run in separate process-limited sessions; final
# qualification always requires *every* signed-on-disk check result.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build manuscript evidence/current

first_checks=(check_manifest check_source check_finite check_research)
second_checks=(check_load check_clearance check_critical_coarea check_two_mark)

run_checks() {
  for script in "$@"; do
    python3 "tools/$script.py" > "build/$script.json"
    python3 -O "tools/$script.py" > "build/$script-optimized.json"
    cmp "build/$script.json" "build/$script-optimized.json"
  done
}

build_manuscripts() {
  mkdir -p build/baseline-rebuild/core
  cp provenance/v112-active/{main.tex,model.tex,inputs.tex,comparison-scope.tex} build/baseline-rebuild/
  cp provenance/v112-active/core/*.tex build/baseline-rebuild/core/
  for pass in 1 2 3; do
    (cd build/baseline-rebuild && pdflatex -interaction=nonstopmode -halt-on-error -recorder main.tex) > "build/baseline-pass${pass}.txt" 2>&1
  done
  python3 tools/audit_tex.py --build-dir build/baseline-rebuild > build/baseline-typesetting.json
  for pass in 1 2 3; do
    pdflatex -interaction=nonstopmode -halt-on-error -recorder -output-directory=build main.tex > "build/main-pass${pass}.txt" 2>&1
  done
  python3 tools/audit_tex.py > build/typesetting.json
  cp build/main.pdf manuscript/A2-DYN-v115-double-clearance.pdf
}

finalize() {
  for script in "${first_checks[@]}" "${second_checks[@]}"; do
    test -s "build/$script.json"
    test -s "build/$script-optimized.json"
    cmp "build/$script.json" "build/$script-optimized.json"
  done
  python3 tools/check_manifest.py > build/qualification-source-check.json
  cmp build/check_manifest.json build/qualification-source-check.json
  python3 tools/audit_tex.py --build-dir build/baseline-rebuild > build/baseline-typesetting-final.json
  cmp build/baseline-typesetting.json build/baseline-typesetting-final.json
  python3 tools/audit_tex.py > build/typesetting-final.json
  cmp build/typesetting.json build/typesetting-final.json
  cmp build/main.pdf manuscript/A2-DYN-v115-double-clearance.pdf
  python3 tools/write_validation_receipt.py
}

case "${1:-all}" in
  checks1) run_checks "${first_checks[@]}" ;;
  checks2) run_checks "${second_checks[@]}" ;;
  typeset) build_manuscripts ;;
  finalize) finalize ;;
  all) run_checks "${first_checks[@]}"; run_checks "${second_checks[@]}"; build_manuscripts; finalize ;;
  *) echo "usage: build.sh [all|checks1|checks2|typeset|finalize]" >&2; exit 2 ;;
esac
