#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"
python_bin="${PYTHON_BIN:-python3}"
mkdir -p build/a2-v82
"$python_bin" scripts/check_a2_v82.py 2>&1 | tee build/a2-v82/algebra-tests.txt
"$python_bin" scripts/audit_a2_v82.py --output build/a2-v82/active-source-graph.json
cd papers/A2-v17-boundary-information-coarsening
for entry in rigidity_v82_core rigidity_v82; do
  latexmk -pdf -interaction=nonstopmode -halt-on-error "${entry}.tex" \
    > "$root/build/a2-v82/${entry}.stdout" 2>&1 || {
      tail -100 "$root/build/a2-v82/${entry}.stdout"; exit 1;
    }
  if grep -E 'There were undefined references|Citation .* undefined|Reference .* undefined|LaTeX Error|Undefined control sequence' "${entry}.log"; then
    echo "Unresolved LaTeX diagnostics in ${entry}" >&2; exit 1
  fi
  cp "${entry}.pdf" "${entry}.log" "$root/build/a2-v82/"
done
cd "$root"
git rev-parse HEAD > build/a2-v82/SOURCE_COMMIT.txt
(cd build/a2-v82 && sha256sum *.pdf > PDF_SHA256SUMS.txt)
printf 'Both entries compiled; source graph and algebra checks completed.\n'
