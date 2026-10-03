#!/usr/bin/env bash
# Read-only build of tracked mathematical source; output lives in verification/current.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p verification/current
{
  printf 'source_commit='; git rev-parse HEAD
  printf 'source_tree='; git rev-parse HEAD^{tree}
  printf 'utc='; date -u +%FT%TZ
  python3 --version
  pdflatex --version | head -n 1
} > verification/current/environment.txt
python3 tools/verify_v14.py > verification/current/v14.normal.json
python3 -O tools/verify_v14.py > verification/current/v14.optimized.json
cmp verification/current/v14.normal.json verification/current/v14.optimized.json
latexmk -pdf -interaction=nonstopmode -halt-on-error two_collision.tex > verification/current/companion.stdout 2>&1
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex > verification/current/main.stdout 2>&1
if grep -E 'undefined references|undefined citations|multiply defined' main.log; then
  echo 'Unresolved or duplicate references in full manuscript' >&2
  exit 1
fi
pdfinfo main.pdf > verification/current/pdfinfo.txt
sha256sum main.tex main.pdf main.log two_collision.pdf tools/verify_v14.py > verification/current/SHA256SUMS
git diff --exit-code
printf 'Full current-source build and finite diagnostics completed.\n'
