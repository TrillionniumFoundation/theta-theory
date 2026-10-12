#!/usr/bin/env python3
"""Render actual newly added proof pages from the native TeX label map."""
from pathlib import Path
import hashlib,json,re,subprocess
root=Path(__file__).resolve().parents[1]
aux=(root/'build/main.aux').read_text()
labels={k:int(p) for k,p in re.findall(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}',aux)}
start=labels['sec:v65-reversible-critical'];end=labels['end:v65-new-mathematics']
lead=labels['thm:intro-v65-caustic']
pages=sorted({1,lead,lead+1,*range(start,end+1)})
if not(1<=start<=end) or end-start>35:raise RuntimeError('unexpected new-proof page range')
evidence=root/'evidence';evidence.mkdir(exist_ok=True)
outputs={}
for page in pages:
    prefix=evidence/f'render-{page:03d}'
    subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-r','110','-png','-singlefile',
                    str(root/'build/main.pdf'),str(prefix)],check=True)
    image=prefix.with_suffix('.png');outputs[image.name]=hashlib.sha256(image.read_bytes()).hexdigest()
receipt={'revision':65,'renderer':'pdftoppm','dpi':110,'rendered_pages':pages,
         'new_proof_page_range':[start,end],'leading_theorem_page':lead,
         'png_sha256':outputs,'human_visual_review_certified':False,
         'continuum_proof_certified':False}
(evidence/'render-receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))
