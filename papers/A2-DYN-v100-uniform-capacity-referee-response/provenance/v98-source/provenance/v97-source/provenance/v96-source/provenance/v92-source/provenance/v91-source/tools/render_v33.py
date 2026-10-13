#!/usr/bin/env python3
"""Record actual page identities and render proofs; generation is not visual inspection."""
from pathlib import Path
import json,re,subprocess
root=Path(__file__).resolve().parents[1]
subprocess.run(['pdfinfo','build/main.pdf'],cwd=root,check=True,stdout=(root/'evidence/pdfinfo.txt').open('w'))
subprocess.run(['pdftotext','-layout','build/main.pdf','evidence/main-text.txt'],cwd=root,check=True)
info=(root/'evidence/pdfinfo.txt').read_text();pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
aux=(root/'build/main.aux').read_text()
wanted=['thm:intro-exact-physical-endpoint','sec:exact-stationary-endpoint',
 'lem:finite-flight-cell-partition','thm:stationary-overlap-regularity',
 'thm:stationary-polynomial-band','thm:physical-time-selector-reconstruction',
 'cor:direct-physical-posterior','sec:stationary-gaussian-complement',
 'lem:two-roof-central-comparison','thm:stationary-singleton-central-term',
 'thm:physical-singleton-reduction','cor:stationary-singleton-denominator-criterion']
found={}
for label in wanted:
    match=re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{([^{}]*)\}\{(\d+)',aux)
    if not match:raise RuntimeError('missing render label '+label)
    found[label]={'number':match.group(1),'page':int(match.group(2))}
first=found['sec:exact-stationary-endpoint']['page'];last=found[wanted[-1]]['page']
selected=sorted({1,found[wanted[0]]['page']}|set(range(first,min(last+2,pages)+1)))
for page in selected:
    subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-r','100','-png',
                    'build/main.pdf',f'evidence/render-{page:03d}'],cwd=root,check=True)
checks=json.loads((root/'evidence/v33-source-and-finite-checks.json').read_text())
receipt=json.loads((root/'evidence/build-receipt.json').read_text())
summary={'event_sha':receipt['event_sha'],'workflow_run_id':receipt['workflow_run_id'],
 'pdf_pages':pages,'pdf_sha256':receipt['pdf_sha256'],'ordinary_paper_tree':receipt['ordinary_paper_tree'],
 'new_labels':found,'source':{k:v for k,v in checks['source'].items() if k!='source_sha256'},
 'new_finite_checks':checks['new_finite_checks'],'rendered_pages':selected,
 'renders_generated':True,'independent_human_review':False,'continuum_proof_certified':False,
 'full_raw_LLT_certified':False}
(root/'evidence/qualification-summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print(json.dumps(summary,indent=2,sort_keys=True))
