#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
[[ $# -eq 0 ]] || { echo 'Exact-checkout qualification accepts no preview or local bypass'; exit 1; }
mkdir -p build evidence
python3 tools/verify_v105.py > evidence/v105-checks.json
python3 -O tools/verify_v104.py > evidence/v104-checks-optimized.json
cmp evidence/v104-checks.json evidence/v104-checks-optimized.json
for script in certify_winding certify_excursion verify check_v5 check_v6; do
  python3 "tools/${script}.py" > "evidence/${script}.json"
  python3 -O "tools/${script}.py" > "evidence/${script}-optimized.json"
  cmp "evidence/${script}.json" "evidence/${script}-optimized.json"
done
python3 tools/verify_v2.py evidence/certify_excursion.json > evidence/verify_v2.json
python3 -O tools/verify_v2.py evidence/certify_excursion.json > evidence/verify_v2-optimized.json
cmp evidence/verify_v2.json evidence/verify_v2-optimized.json
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
python3 tools/render_v105.py
git diff --exit-code
