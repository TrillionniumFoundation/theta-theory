#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build evidence
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -recorder -output-directory=build main.tex >"build/pass${pass}.txt"
done
if grep -Eq 'undefined references|Citation .* undefined|Reference .* undefined|LaTeX Error' build/main.log; then
  echo 'Unresolved source references or TeX error' >&2; exit 1
fi
python3 - <<'PY'
import hashlib,json,os,pathlib,subprocess
p=pathlib.Path('.')
sources={str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in sorted(p.rglob('*.tex'))}
sha=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
receipt={'head_sha':sha,'event_sha':os.environ.get('GITHUB_SHA'),'native_build_passed':True,'mathematical_completion_certified':False,'independent_human_review':False,'sources':sources,'pdf_sha256':hashlib.sha256((p/'build/main.pdf').read_bytes()).hexdigest()}
(p/'evidence/build-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
PY
