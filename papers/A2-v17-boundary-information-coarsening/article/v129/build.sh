#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
export OPENBLAS_NUM_THREADS=1
mkdir -p evidence ../v125/evidence

dump_failure_logs() {
  status=$?
  echo "v128 build failed with status $status" >&2
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

test -f ../v127/parts/01b-boundary-atlas.tex || { echo 'Missing preserved v127 atlas' >&2; exit 1; }
test -f ../v125/parts/09-stratified-nilpotent.tex || { echo 'Missing preserved v125 source' >&2; exit 1; }
test -f ../v126/parts/04-depth.tex || { echo 'Missing preserved v126 depth source' >&2; exit 1; }
test -f parts/01-introduction.tex || { echo 'Missing v128 native introduction' >&2; exit 1; }
test -f parts/01b-boundary-atlas.tex || { echo 'Missing v128 atlas statement' >&2; exit 1; }
test -f parts/09b-boundary-atlas-proofs.tex || { echo 'Missing v128 atlas proof' >&2; exit 1; }
test -f parts/09c-relative-primary-specialization.tex || { echo 'Missing v128 relative-primary section' >&2; exit 1; }

python ../v125/checks/exact_k3.py > evidence/exact_k3.log 2>&1
python ../v125/checks/exact_corank_two.py > evidence/exact_corank_two.log 2>&1
python ../v125/checks/stratified_rank_two.py > evidence/stratified_rank_two.log 2>&1
python checks/boundary_atlas.py > evidence/boundary_atlas.log 2>&1
python checks/generic_boundary_atlas.py > evidence/generic_boundary_atlas.log 2>&1

cp -f ../v125/evidence/K3_CERTIFICATES.json evidence/ 2>/dev/null || true
cp -f ../v125/evidence/CORANK_TWO_CERTIFICATES.json evidence/ 2>/dev/null || true
cp -f ../v125/evidence/STRATIFIED_RANK_TWO_CERTIFICATES.json evidence/ 2>/dev/null || true

for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error geometry.tex > "evidence/geometry-pass-$pass.log" 2>&1
done
cp geometry.log evidence/GEOMETRY_TEX.log
python verify_build.py
