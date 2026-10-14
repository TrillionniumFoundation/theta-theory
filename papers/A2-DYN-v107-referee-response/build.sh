#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
[[ $# -eq 0 ]] || { echo 'Exact-checkout qualification accepts no bypass'; exit 1; }
mkdir -p build evidence
python3 tools/verify_v107.py > evidence/v107-source-and-checks.json
python3 -O tools/verify_v107.py > evidence/v107-source-and-checks-optimized.json
cmp evidence/v107-source-and-checks.json evidence/v107-source-and-checks-optimized.json
python3 tools/check_v107.py > evidence/v107-finite.json
python3 -O tools/check_v107.py > evidence/v107-finite-optimized.json
cmp evidence/v107-finite.json evidence/v107-finite-optimized.json
compile() {
  local name=$1 previous='' current='' stable=0
  rm -f "build/$name.aux" "build/$name.out" "build/$name.toc"
  for pass in 1 2 3 4 5 6; do
    if ! pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
      -jobname="$name" -output-directory=build "$name.tex" </dev/null > "build/$name-pass$pass.txt" 2>&1; then
      tail -100 "build/$name-pass$pass.txt"; return 1
    fi
    current=$(sha256sum "build/$name.aux" | cut -d' ' -f1)
    if [[ "$current" == "$previous" ]] && ! grep -Eq 'Rerun to|Please rerun' "build/$name.log"; then stable=1; break; fi
    previous=$current
  done
  [[ $stable == 1 ]] || { echo "References did not stabilize: $name"; return 1; }
  if grep -Eq 'LaTeX Warning|Package .* Warning|Overfull|undefined|Missing character' "build/$name.log"; then
    grep -En 'LaTeX Warning|Package .* Warning|Overfull|undefined|Missing character' "build/$name.log"; return 1
  fi
}
compile supplement
compile main
python3 tools/audit_v107_build.py > evidence/v107-build-audit.json
sha256sum build/main.pdf build/supplement.pdf > evidence/pdf-sha256.txt
git diff --exit-code
