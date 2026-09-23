#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
export OPENBLAS_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
mkdir -p evidence
trap 's=$?; for f in evidence/*.log; do echo "===== $f ====="; tail -n 100 "$f"; done; exit "$s"' ERR
python -m py_compile checks/*.py verify_build.py
python -c 'import sympy, numpy, fitz'
for check in exact_k3 exact_corank_two stratified_rank_two boundary_atlas generic_boundary_atlas revision131_exact; do
  echo "Executing $check"
  python "checks/$check.py" > "evidence/$check.log" 2>&1
done
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error geometry.tex > "evidence/geometry-pass-$pass.log" 2>&1
done
cp geometry.log evidence/GEOMETRY_TEX.log
python verify_build.py
