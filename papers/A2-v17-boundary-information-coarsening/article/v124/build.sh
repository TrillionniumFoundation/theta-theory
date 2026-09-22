#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
export OPENBLAS_NUM_THREADS=1
mkdir -p evidence
for command in python pdflatex; do
  command -v "$command" >/dev/null || { echo "Missing $command" >&2; exit 1; }
done
python -c 'import sympy, numpy, fitz'
test -f ../v123/parts/02-relations.tex || { echo 'Missing preserved v123 mathematical source' >&2; exit 1; }

python checks/exact_k3.py > evidence/exact_k3.log 2>&1
python checks/exact_corank_two.py > evidence/exact_corank_two.log 2>&1

for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error geometry.tex > "evidence/geometry-pass-${pass}.log" 2>&1
done
cp geometry.log evidence/GEOMETRY_TEX.log
python verify_build.py
