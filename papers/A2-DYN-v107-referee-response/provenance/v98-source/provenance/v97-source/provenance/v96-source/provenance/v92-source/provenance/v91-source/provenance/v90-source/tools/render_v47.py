#!/usr/bin/env python3
"""Render theorem-bearing pages from actual aux labels and record file hashes."""
from pathlib import Path
import hashlib,json,re,subprocess
root=Path(__file__).resolve().parents[1];aux=(root/'build/main.aux').read_text()
labels=['thm:intro-v47-boundary-decisions', 'sec:v47-endpoint-decisions', 'lem:v47-small-endpoint-local', 'lem:v47-endpoint-envelopes', 'lem:v47-free-decision-continuation', 'prop:v47-high-gradient-boundary', 'lem:v47-free-critical-cluster', 'thm:v47-endpoint-boundary-smallness', 'cor:v47-endpoint-jumps', 'sec:v47-first-bad-margins', 'prop:v47-first-defect-masses', 'thm:v47-ordered-boundary-removal', 'cor:v47-arithmetic-residual']
info=subprocess.check_output(['pdfinfo',str(root/'build/main.pdf')],text=True)
count=int(re.search(r'Pages:\s+(\d+)',info).group(1));pages={1}
located={}
for label in labels:
    found=re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{[^}]*\}\{(\d+)\}',aux)
    if not found:raise RuntimeError('missing rendered label '+label)
    page=int(found.group(1));located[label]=page
    pages.update(range(max(1,page-1),min(count,page+2)+1))
for page in sorted(pages):
    stem=root/f'evidence/render-{page:03}'
    subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-r','90','-singlefile','-png',
                    str(root/'build/main.pdf'),str(stem)],check=True,stdout=subprocess.DEVNULL)
files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'evidence').glob('render-*.png')}
(root/'evidence/render-receipt.json').write_text(json.dumps({'pages':count,'labels':located,
    'rendered_pages':sorted(pages),'image_sha256':files,'proof_certification':False},indent=2,sort_keys=True)+'\n')
print(json.dumps({'pages':count,'rendered_pages':len(pages),'labels':located},indent=2))
