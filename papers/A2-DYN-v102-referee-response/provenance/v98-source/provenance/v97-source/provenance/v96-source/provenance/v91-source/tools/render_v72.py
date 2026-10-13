#!/usr/bin/env python3
"""Render all actual new-proof pages and bind the rendering record to the PDF."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
ROOT=Path(__file__).resolve().parents[1]
aux=(ROOT/'build/main.aux').read_text()
labels=['sec:v72-window-current','thm:v72-window-current','prop:v72-window-fourier',
        'sec:v72-complete-current','thm:v72-complete-current','prop:v72-coarea-flux',
        'thm:v72-current-primitive','sec:v72-all-source-recovery','thm:v72-global-recovery',
        'thm:v72-complete-budget','prop:v72-flux-height','end:v72-new-mathematics']
pages={}
for label in labels:
    match=re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}',aux)
    if not match:
        raise RuntimeError('missing numeric proof-page label: '+label)
    pages[label]=int(match.group(1))
start,end=pages['sec:v72-window-current'],pages['end:v72-new-mathematics']
for page in range(1,end+1):
    subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1600','-png','-singlefile',str(ROOT/'build/main.pdf'),str(ROOT/f'evidence/v72-proof-page-{page:03}')],check=True)
(ROOT/'evidence/pdfinfo.txt').write_text(subprocess.check_output(['pdfinfo',str(ROOT/'build/main.pdf')]).decode())
(ROOT/'evidence/v72-proof-pages.json').write_text(json.dumps({'labels':pages,'front_and_new_proof_pages_rendered':list(range(1,end+1)),
    'pdf_sha256':hashlib.sha256((ROOT/'build/main.pdf').read_bytes()).hexdigest()},indent=2,sort_keys=True)+'\n')
