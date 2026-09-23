#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
rm -rf evidence
mkdir -p evidence
python -m py_compile checks/*.py verify_build.py
for name in exact_k3 exact_corank_two stratified_rank_two boundary_atlas generic_boundary_atlas revision131_exact revision132_exact revision133_exact revision134_exact revision135_exact revision136_exact; do
  echo "Executing $name"
  python "checks/$name.py" > "evidence/${name}.log" 2>&1
done
# AMS stores internal tocindent data with newlabel. Do not import that data,
# or bibliography keys, through xr-hyper; import only mathematical labels.
labels() {
  python - "$1" <<'PY'
from pathlib import Path
import sys
name=sys.argv[1]
lines=Path(name+'.aux').read_text().splitlines()
Path(name+'-labels.aux').write_text('\n'.join(x for x in lines if x.startswith('\\newlabel{') and not x.startswith('\\newlabel{tocindent'))+'\n')
PY
}
rm -f geometry.aux geometry.out supplement.aux supplement.out supplement.toc complete.aux complete.out geometry-labels.aux supplement-labels.aux
for pass in 1 2 3 4; do
  for name in geometry supplement; do
    pdflatex -interaction=nonstopmode -halt-on-error "$name.tex" > "evidence/${name}-pass${pass}.log"
    labels "$name"
  done
done
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error complete.tex > "evidence/complete-pass${pass}.log"
done
for name in geometry supplement complete; do cp "$name.log" "evidence/${name}-final.log"; done
python verify_build.py
