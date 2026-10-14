#!/usr/bin/env python3
"""Render actual new-proof pages from the final TeX labels."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
ROOT=Path(__file__).resolve().parents[1]
aux=(ROOT/'build/main.aux').read_text()
labels=['sec:v69-comparison-trace','thm:v69-comparison-collar','sec:v69-absolute-guards','thm:v69-absolute-guard-height','sec:v69-finite-scale-coverage','thm:v69-finite-scale-height','eq:v69-canonical-endpoint-budget','end:v69-new-mathematics']
pages={}
for label in labels:
    m=re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}',aux)
    if not m:
        raise RuntimeError('missing numeric proof-page label: '+label)
    pages[label]=int(m.group(1))
start=pages['sec:v69-comparison-trace']
end=pages['end:v69-new-mathematics']
for page in range(start,end+1):
    subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1600','-png','-singlefile',str(ROOT/'build/main.pdf'),str(ROOT/f'evidence/v69-proof-page-{page:03}')],check=True)
info=subprocess.check_output(['pdfinfo',str(ROOT/'build/main.pdf')]).decode()
(ROOT/'evidence/pdfinfo.txt').write_text(info)
(ROOT/'evidence/v69-proof-pages.json').write_text(json.dumps({'labels':pages,'all_new_proof_pages_rendered':list(range(start,end+1)),'pdf_sha256':hashlib.sha256((ROOT/'build/main.pdf').read_bytes()).hexdigest()},indent=2,sort_keys=True)+'\n')
