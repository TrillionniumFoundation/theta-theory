#!/usr/bin/env python3
"""Generate page renders and exact PDF identities; not an assertion of human inspection."""
from pathlib import Path
import json,re,subprocess
root=Path(__file__).resolve().parents[1]
with (root/'evidence/pdfinfo.txt').open('w') as stream:
    subprocess.run(['pdfinfo','build/main.pdf'],cwd=root,check=True,stdout=stream)
subprocess.run(['pdftotext','-layout','build/main.pdf','evidence/main-text.txt'],cwd=root,check=True)
info=(root/'evidence/pdfinfo.txt').read_text();pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
aux=(root/'build/main.aux').read_text()
wanted=['thm:intro-exact-path-bridge','sec:v36-family-inputs','prop:v36-cover-mixing',
 'sec:v36-local-bridge-moments','prop:v36-local-fourth','cor:v36-conditional-tightness',
 'sec:v36-exact-path-bridge','lem:v36-local-block-probes','thm:v36-microscopic-path-bridge',
 'cor:v36-band-posterior-bridge','sec:v36-nonelliptic-family','prop:v36-support-family',
 'thm:intro-stationary-microscopic','thm:intro-action-family','sec:v35-literature-routes',
 'sec:action-norm-details','prop:v35-expanded-LY','lem:v35-faithful-strong','lem:v35-peripheral-density',
 'sec:rotation-free-arithmetic','thm:v35-rotation-free-rigidity','sec:compact-family-local-principle',
 'thm:v35-action-family-LLT','lem:v35-ellipse-geometry','cor:v35-ellipse-local-law',
 'cor:v35-family-posterior','sec:compact-collision-spectrum','sec:collision-mixing-local-limit',
 'cor:local-endpoint-measures','sec:stationary-microscopic-LLT','cor:normalized-physical-band']
found={}
for label in wanted:
    match=re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{([^{}]*)\}\{(\d+)',aux)
    if not match:raise RuntimeError('missing render label '+label)
    found[label]={'number':match.group(1),'page':int(match.group(2))}
last=found['cor:normalized-physical-band']['page']
selected=list(range(1,min(last+1,pages)+1))
subprocess.run(['pdftoppm','-f',str(selected[0]),'-l',str(selected[-1]),'-r','90','-png',
                'build/main.pdf','evidence/render'],cwd=root,check=True)
checks=json.loads((root/'evidence/v36-source-and-finite-checks.json').read_text())
receipt=json.loads((root/'evidence/build-receipt.json').read_text())
summary={'event_sha':receipt['event_sha'],'workflow_run_id':receipt['workflow_run_id'],
 'pdf_pages':pages,'pdf_sha256':receipt['pdf_sha256'],'ordinary_paper_tree':receipt['ordinary_paper_tree'],
 'direct_route_labels':found,'source':{k:v for k,v in checks['source'].items() if k!='source_sha256'},
 'new_finite_checks':checks['new_finite_checks'],'rendered_pages':selected,
 'renders_generated':True,'independent_human_review':False,'continuum_proof_certified':False,
 'full_raw_LLT_certified':False}
(root/'evidence/qualification-summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print(json.dumps(summary,indent=2,sort_keys=True))
