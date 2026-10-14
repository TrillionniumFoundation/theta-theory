#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mode=()
if [[ $# -eq 1 && $1 == --local ]]; then
  [[ ${GITHUB_ACTIONS:-false} != true ]] || { echo 'Local mode forbidden in CI'; exit 1; }
  mode=(--local)
elif [[ $# -ne 0 ]]; then
  echo 'Usage: bash build.sh [--local]'; exit 1
fi
mkdir -p build evidence
python3 tools/verify_v74.py "${mode[@]}" > evidence/v74-source-and-finite-checks.json
python3 -O tools/verify_v74.py "${mode[@]}" > evidence/v74-source-and-finite-checks-optimized.json
cmp evidence/v74-source-and-finite-checks.json evidence/v74-source-and-finite-checks-optimized.json
python3 - <<'PY'
import json
x=json.load(open('evidence/v74-source-and-finite-checks.json'))
print(json.dumps({'finite_checks':x['finite_checks'],'preserved':x['source']['preserved'],
 'checkout_sha':x['source']['checkout_sha'],'active_core_count':167},indent=2))
PY
for script in certify_winding certify_excursion verify verify_v2 check_v5 check_v6; do
  python3 "tools/${script}.py" > "evidence/${script}.py.json"
done
compile() {
  local name=$1 source=$2 last='' now='' stable=0
  rm -f "build/${name}.aux" "build/${name}.out" "build/${name}.toc"
  for pass in 1 2 3 4 5 6; do
    if ! pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
       -jobname="$name" -output-directory=build "$source" </dev/null > "build/${name}-pass${pass}.txt" 2>&1; then
      tail -100 "build/${name}-pass${pass}.txt"; return 1
    fi
    now=$(sha256sum "build/${name}.aux" | cut -d' ' -f1)
    if [[ "$now" == "$last" ]] && ! grep -Eq 'Rerun to|Please rerun' "build/${name}.log"; then stable=1; break; fi
    last=$now
  done
  [[ $stable == 1 ]] || { echo "Unstable references: $name"; return 1; }
  if grep -Eq 'LaTeX Warning|Package .* Warning|Overfull|undefined|Missing character' "build/${name}.log"; then
    grep -En 'LaTeX Warning|Package .* Warning|Overfull|undefined|Missing character' "build/${name}.log"; return 1
  fi
}
compile supplement supplement.tex
python3 tools/render_v74.py --labels
compile main main.tex
python3 tools/render_v74.py
if [[ ${#mode[@]} -eq 0 ]]; then git diff --exit-code; fi
