#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
export SOURCE_DATE_EPOCH=1790035200
export FORCE_SOURCE_DATE=1
export PYTHONDONTWRITEBYTECODE=1
mkdir -p evidence/build
python3 run_inherited.py | tee evidence/build/inherited-tests.txt
python3 verify_revision.py | tee evidence/build/revision-tests.txt
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error -recorder paper.tex >"evidence/build/paper-pass${pass}.txt"
done
python3 make_crossrefs.py | tee evidence/build/crossrefs.txt
for document in geometry applications; do
  for pass in 1 2 3; do
    pdflatex -interaction=nonstopmode -halt-on-error -recorder "${document}.tex" >"evidence/build/${document}-pass${pass}.txt"
  done
done
python3 make_receipts.py | tee evidence/build/receipt-summary.txt
