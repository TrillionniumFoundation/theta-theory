#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mode=()
if [[ $# -eq 1 && $1 == --local ]]; then
  [[ ${GITHUB_ACTIONS:-false} != true ]] || { echo 'Local archive mode forbidden in CI'; exit 1; }
  mode=(--local)
elif [[ $# -ne 0 ]]; then
  echo 'Usage: bash build.sh [--local]'; exit 1
fi
mkdir -p build evidence
python3 tools/verify_v88.py "${mode[@]}" > evidence/v88-checks.json
python3 -O tools/verify_v88.py "${mode[@]}" > evidence/v88-checks-optimized.json
cmp evidence/v88-checks.json evidence/v88-checks-optimized.json
# The historical verifier's no-argument filename differs from the producer's.
# Keep the inherited verifier byte-identical and pass the actual artifact path.
for script in certify_winding certify_excursion verify check_v5 check_v6; do
  python3 "tools/${script}.py" > "evidence/${script}.json"
  python3 -O "tools/${script}.py" > "evidence/${script}-optimized.json"
  cmp "evidence/${script}.json" "evidence/${script}-optimized.json"
done
python3 tools/verify_v2.py evidence/certify_excursion.json > evidence/verify_v2.json
python3 -O tools/verify_v2.py evidence/certify_excursion.json > evidence/verify_v2-optimized.json
cmp evidence/verify_v2.json evidence/verify_v2-optimized.json
compile() {
  local name=$1 last='' now='' stable=0
  rm -f "build/${name}.aux" "build/${name}.out" "build/${name}.toc"
  for pass in 1 2 3 4 5 6; do
    if ! pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
       -jobname="$name" -output-directory=build "$name.tex" </dev/null > "build/${name}-pass${pass}.txt" 2>&1; then
      tail -100 "build/${name}-pass${pass}.txt"; return 1
    fi
    now=$(sha256sum "build/${name}.aux" | cut -d' ' -f1)
    if [[ "$now" == "$last" ]] && ! grep -Eq 'Rerun to|Please rerun' "build/${name}.log"; then stable=1; break; fi
    last=$now
  done
  [[ $stable == 1 ]] || { echo "Unstable references: $name"; return 1; }
  if grep -Eq 'LaTeX Warning|Package .* Warning|pdfTeX warning|Overfull|undefined|Missing character' "build/${name}.log"; then
    grep -En 'LaTeX Warning|Package .* Warning|pdfTeX warning|Overfull|undefined|Missing character' "build/${name}.log"; return 1
  fi
}
compile supplement
compile main
python3 tools/render_v88.py "${mode[@]}"
if [[ ${#mode[@]} -eq 0 ]]; then git diff --exit-code; fi
