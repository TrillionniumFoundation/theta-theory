#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build manuscript evidence/current
for script in check_manifest check_source check_finite check_research check_load check_clearance check_critical_coarea; do
  python3 "tools/$script.py" > "build/$script.json"
  python3 -O "tools/$script.py" > "build/$script-optimized.json"
  cmp "build/$script.json" "build/$script-optimized.json"
done
# Rebuild the unchanged downloaded baseline source, not just the new article.
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
cp build/main.pdf manuscript/A2-DYN-clearance-roof.pdf
# Record success only after all prior commands and comparisons succeed.
python3 tools/write_validation_receipt.py
