#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
export SOURCE_DATE_EPOCH=1790048800
export FORCE_SOURCE_DATE=1
export PYTHONDONTWRITEBYTECODE=1
python3 verify_revision.py
python3 verify_v116.py
mkdir -p evidence/build
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error -recorder paper.tex >"evidence/build/paper-pass${pass}.txt"
done
python3 make_crossrefs.py
for document in geometry applications; do
  for pass in 1 2 3; do
    pdflatex -interaction=nonstopmode -halt-on-error -recorder "${document}.tex" >"evidence/build/${document}-pass${pass}.txt"
  done
done
python3 make_receipts.py
