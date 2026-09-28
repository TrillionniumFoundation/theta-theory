#!/usr/bin/env bash
# Run from the manuscript directory. No shell escape; no downloaded proof inputs.
set -euo pipefail
OUT="${1:-native-v78}"
mkdir -p "$OUT"
OUT="$(cd "$OUT" && pwd)"
export SOURCE_DATE_EPOCH=1789632000
export FORCE_SOURCE_DATE=1
python3 tools-v78/check_revision_v78.py --output "$OUT/check-v78-normal.json" > "$OUT/check-normal.txt"
python3 -O tools-v78/check_revision_v78.py --output "$OUT/check-v78-optimized.json" > "$OUT/check-optimized.txt"
cmp "$OUT/check-v78-normal.json" "$OUT/check-v78-optimized.json"
# main.tex is the unchanged full periodic/technical archive, needed only for
# the companion's six explicitly routed extension references.
for entry in two_collision main rigidity_v78 periodic_companion_v78; do
  for pass in 1 2 3; do
    pdflatex -no-shell-escape -recorder -interaction=nonstopmode \
      -halt-on-error -output-directory="$OUT" "$entry.tex" \
      > "$OUT/$entry-pass$pass.txt" 2>&1
  done
  if grep -E 'LaTeX Warning: (Reference|Citation).*undefined|There were undefined references|multiply defined' "$OUT/$entry.log"; then
    echo "Unresolved references in $entry" >&2
    exit 1
  fi
  pdfinfo "$OUT/$entry.pdf" > "$OUT/$entry-pdfinfo.txt"
done
python3 tools-v78/source_manifest.py --build-dir "$OUT" \
  --output "$OUT/local-build-provenance.json"
echo "Local native build and both diagnostic modes passed. This is not independent proof certification."
