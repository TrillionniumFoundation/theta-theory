#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
export OPENBLAS_NUM_THREADS=1
mkdir -p evidence

dump_failure_logs() {
  status=$?
  echo "v129 build failed with status $status" >&2
  for f in evidence/*.log; do
    if [ -f "$f" ]; then
      echo "===== tail $f =====" >&2
      tail -n 240 "$f" >&2 || true
    fi
  done
  exit "$status"
}
trap dump_failure_logs ERR

for command in python pdflatex; do
  command -v "$command" >/dev/null || { echo "Missing $command" >&2; exit 1; }
done
python -c 'import sympy, numpy, fitz'

for f in \
  parts/01-introduction.tex parts/01b-boundary-atlas.tex \
  parts/02-relations.tex parts/03-fitting.tex parts/04-depth.tex \
  parts/04-polarization.tex parts/05-moduli.tex parts/06-coranktwo.tex \
  parts/07-classical.tex parts/08-corank-boundary.tex \
  parts/09-stratified-nilpotent.tex parts/10-reye-priority.tex \
  parts/09a-rees-specialization.tex parts/09b-boundary-atlas-proofs.tex \
  parts/09c-relative-primary-specialization.tex \
  parts/08-weighted.tex parts/09-certificates.tex; do
  test -f "$f" || { echo "Missing self-contained source $f" >&2; exit 1; }
done

python -m py_compile checks/*.py verify_build.py
python checks/exact_k3.py > evidence/exact_k3.log 2>&1
python checks/exact_corank_two.py > evidence/exact_corank_two.log 2>&1
python checks/stratified_rank_two.py > evidence/stratified_rank_two.log 2>&1
python checks/boundary_atlas.py > evidence/boundary_atlas.log 2>&1
python checks/generic_boundary_atlas.py > evidence/generic_boundary_atlas.log 2>&1

for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error geometry.tex > "evidence/geometry-pass-$pass.log" 2>&1
done
cp geometry.log evidence/GEOMETRY_TEX.log
python verify_build.py
