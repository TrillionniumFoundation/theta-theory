#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
[[ $# -eq 0 ]] || { echo 'No build bypass arguments are accepted'; exit 1; }
mkdir -p build
export SOURCE_DATE_EPOCH=1791960952
export FORCE_SOURCE_DATE=1
for name in check_manifest check_finite check_research; do
  python3 "tools/$name.py" > "build/$name.json"
  python3 -O "tools/$name.py" > "build/$name-optimized.json"
  cmp "build/$name.json" "build/$name-optimized.json"
done
previous=''
stable=0
rm -f build/main.aux build/main.out build/main.toc
for pass in 1 2 3 4 5 6; do
  pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error \
    -recorder -output-directory=build main.tex </dev/null > "build/main-pass$pass.txt" 2>&1 || {
      tail -80 "build/main-pass$pass.txt"; exit 1;
    }
  current=$(sha256sum build/main.aux | cut -d' ' -f1)
  if [[ "$current" == "$previous" ]] && ! grep -Eq 'Rerun to|Please rerun' build/main.log; then
    stable=1; break
  fi
  previous=$current
done
[[ $stable == 1 ]] || { echo 'Unstable references'; exit 1; }
python3 tools/audit_tex.py > build/typesetting.json
pdftoppm -r 80 -png build/main.pdf build/page >/dev/null 2>&1
cat build/check_manifest.json build/check_research.json build/typesetting.json
