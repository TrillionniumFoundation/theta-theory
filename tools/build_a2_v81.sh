#!/usr/bin/env bash
# A native LaTeX build, not a source-export job. No shell escape or write token.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PAPER="$ROOT/papers/A2-v17-boundary-information-coarsening"
OUT="$ROOT/build/a2-v81"
MODE="${1:-full}"
case "$MODE" in full|--core-only) ;; *) echo 'Usage: build_a2_v81.sh [--core-only]' >&2; exit 2;; esac
mkdir -p "$OUT"
export SOURCE_DATE_EPOCH=1789689600
export FORCE_SOURCE_DATE=1
python3 "$ROOT/tools/test_a2_v81.py" --json "$OUT/algebra-tests.json" 2>&1 | tee "$OUT/algebra-tests.log"
python3 - "$PAPER" "$OUT" "$MODE" <<'PY'
import hashlib,json,re,sys
from pathlib import Path
paper,out,mode=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
pat=re.compile(r'\\(?:input|include)\{([^}]+)\}')
def closure(name):
    seen=set()
    def visit(name):
        if not name.endswith('.tex'): name += '.tex'
        if name in seen: return
        file=paper/name
        if not file.is_file(): raise SystemExit('Missing active input: '+name)
        seen.add(name)
        text=re.sub(r'(?<!\\)%[^\n]*','',file.read_text())
        for child in pat.findall(text): visit(child)
    visit(name)
    return seen
names=closure('rigidity_v81_core.tex')
if mode=='full':
    full=closure('rigidity_v81.tex')
    old=closure('rigidity_v80.tex')
    exempt={'rigidity_v80.tex','article/v80/references.tex'}
    missing=(old-exempt)-full
    if missing: raise SystemExit('Dropped inherited inputs: '+repr(sorted(missing)))
    bib=lambda p:set(re.findall(r'\\bibitem\{([^}]+)\}',(paper/p).read_text()))
    if not bib('article/v80/references.tex') <= bib('article/v81/references.tex'):
        raise SystemExit('An inherited bibliography key is missing')
    names |= full
manifest={n:hashlib.sha256((paper/n).read_bytes()).hexdigest() for n in sorted(names)}
(out/'active-input-sha256.json').write_text(json.dumps(manifest,indent=2)+'\n')
PY
if [[ "$MODE" == full ]]; then entries=(rigidity_v81 rigidity_v81_core); else entries=(rigidity_v81_core); fi
for name in "${entries[@]}"; do
  (cd "$PAPER" && latexmk -gg -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$OUT" "$name.tex") 2>&1 | tee "$OUT/$name.build.log"
  if grep -Eq 'undefined references|Citation .* undefined|Reference .* undefined|multiply defined|Label\(s\) may have changed' "$OUT/$name.log"; then
    echo "Unresolved LaTeX diagnostics in $name" >&2; exit 1
  fi
  test -s "$OUT/$name.pdf"
done
{
  pdflatex --version | head -n 2
  latexmk --version | head -n 3
  python3 --version
  python3 -c 'import numpy; print("NumPy",numpy.__version__)'
  git -C "$ROOT" rev-parse HEAD 2>/dev/null || echo 'No local Git commit: use source manifest'
} > "$OUT/environment.txt"
(cd "$OUT" && sha256sum *.pdf > PDF_SHA256SUMS)
printf 'Native build complete (%s). Products: %s\n' "$MODE" "$OUT"
