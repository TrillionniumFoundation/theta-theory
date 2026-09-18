#!/usr/bin/env bash
# Offline, read-only with respect to mathematical sources and historical files.
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"
for command in python3 pdflatex cmp; do
  command -v "$command" >/dev/null || { echo "Missing required command: $command" >&2; exit 2; }
done
mkdir -p build-v79
# A stable source date improves reproduction on the same TeX toolchain.
export SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH:-1789646400}
export FORCE_SOURCE_DATE=1
python3 tools-v79/check_sources_v79.py --output build-v79/source_check.json > build-v79/source_check.stdout.json
python3 tools-v79/verify_v79.py --output build-v79/diagnostics.json > build-v79/diagnostics.stdout.json
python3 -O tools-v79/verify_v79.py > build-v79/diagnostics.optimized.json
cmp build-v79/diagnostics.stdout.json build-v79/diagnostics.optimized.json
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
    -output-directory=build-v79 rigidity_v79.tex > "build-v79/latex-pass-${pass}.stdout"
done
python3 - <<'PY'
from pathlib import Path
import hashlib, json, re, subprocess
root=Path.cwd(); build=root/'build-v79'; log=(build/'rigidity_v79.log').read_text(errors='replace')
patterns={'undefined_references':r'(?:Reference .* undefined|There were undefined references)',
          'undefined_citations':r'Citation .* undefined',
          'multiply_defined_labels':r'(?:multiply defined|multiply-defined)',
          'overfull_boxes':r'Overfull \\[hv]box'}
counts={name:len(re.findall(pattern,log)) for name,pattern in patterns.items()}
if any(counts.values()):
    raise SystemExit('TeX reference/layout diagnostic failure: '+str(counts))
pdf=build/'rigidity_v79.pdf'; data=pdf.read_bytes()
if not data.startswith(b'%PDF-'):
    raise SystemExit('invalid PDF header')
report={'kind':'local_build_not_proof_certification','status':'PASS',
        'compiler':subprocess.check_output(['pdflatex','--version'],text=True).splitlines()[0],
        'latex_passes':3,'tex_diagnostic_counts':counts,
        'underfull_boxes':len(re.findall(r'Underfull \\[hv]box',log)),
        'normal_and_optimized_diagnostics_identical':True,
        'pdf_sha256':hashlib.sha256(data).hexdigest(),'pdf_bytes':len(data)}
(build/'build_result.json').write_text(json.dumps(report,indent=2)+'\n')
(root/'rigidity_v79.pdf').write_bytes(data)
print(json.dumps(report,indent=2))
PY
