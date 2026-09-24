#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
mkdir -p evidence
python -m py_compile checks/*.py check_v145.py verify_v145.py
for name in exact_k3 exact_corank_two stratified_rank_two boundary_atlas generic_boundary_atlas revision131_exact revision132_exact revision133_exact revision134_exact revision135_exact revision136_exact revision137_exact revision138_exact revision139_exact revision140_exact revision141_spectral_exact revision141_likelihood_exact revision142_exact revision143_critical_exact revision144_projective_exact; do
  echo "Executing $name"
  python "checks/$name.py" > "evidence/${name}.log" 2>&1
done
python check_v145.py > evidence/revision145_exact.log
labels() {
python - "$1" <<'PY'
from pathlib import Path
import sys
n=sys.argv[1]
Path(n+'-labels.aux').write_text('\n'.join(x for x in Path(n+'.aux').read_text().splitlines() if x.startswith('\\newlabel{') and not x.startswith('\\newlabel{tocindent'))+'\n')
PY
}
for name in geometry applications archive-v144; do
 rm -f "$name.aux" "$name.out" "$name.toc"
 for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error "$name.tex" > "evidence/${name}-pass${pass}.log"
 done
 labels "$name"
 cp "$name.log" "evidence/${name}-final.log"
done
python verify_v145.py
