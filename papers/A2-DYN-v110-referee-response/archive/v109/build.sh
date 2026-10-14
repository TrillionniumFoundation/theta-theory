#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
[[ $# -eq 0 ]] || { echo 'The exact-checkout build accepts no bypass arguments'; exit 1; }
mkdir -p build evidence
python3 tools/verify_source.py > evidence/source.json
python3 -O tools/verify_source.py > evidence/source-optimized.json
cmp evidence/source.json evidence/source-optimized.json
python3 tools/check_optical.py > evidence/finite.json
python3 -O tools/check_optical.py > evidence/finite-optimized.json
cmp evidence/finite.json evidence/finite-optimized.json
compile() {
  local dir=$1 name=$2 previous='' current='' stable=0
  (
    cd "$dir"
    mkdir -p build
    rm -f "build/$name.aux" "build/$name.out" "build/$name.toc"
    for pass in 1 2 3 4 5 6; do
      if ! pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
          -jobname="$name" -output-directory=build "$name.tex" </dev/null > "build/$name-pass$pass.txt" 2>&1; then
        tail -100 "build/$name-pass$pass.txt"; exit 1
      fi
      current=$(sha256sum "build/$name.aux" | cut -d' ' -f1)
      if [[ "$current" == "$previous" ]] && ! grep -Eq 'Rerun to|Please rerun' "build/$name.log"; then stable=1; break; fi
      previous=$current
    done
    [[ $stable == 1 ]] || { echo "Unstable references: $dir/$name"; exit 1; }
  )
}
compile . main
(
  cd archive/v108
  mkdir -p build evidence
  python3 tools/assemble_v105.py
)
compile archive/v108 supplement
compile archive/v108 main
for name in supplement main; do
  (cd archive/v108 && python3 tools/audit_v107_texlog.py "$name") > "evidence/history-$name-tex.json"
done
for ext in pdf log aux fls; do
  cp "archive/v108/build/main.$ext" "build/history.$ext"
  cp "archive/v108/build/supplement.$ext" "build/supplement.$ext"
done
python3 tools/audit_build.py > evidence/build-audit.json
sha256sum build/main.pdf build/history.pdf build/supplement.pdf > evidence/pdf-sha256.txt
pdftoppm -f 1 -singlefile -scale-to 1400 -png build/main.pdf evidence/current-first-page >/dev/null 2>&1
pdftoppm -f 7 -singlefile -scale-to 1400 -png build/main.pdf evidence/current-traces-page >/dev/null 2>&1
git diff --exit-code
