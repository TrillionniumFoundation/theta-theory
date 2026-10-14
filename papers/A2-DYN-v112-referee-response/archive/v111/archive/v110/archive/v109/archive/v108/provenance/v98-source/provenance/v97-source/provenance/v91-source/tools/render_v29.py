#!/usr/bin/env python3
"""Record actual PDF pages and render proof pages; does not claim visual inspection."""
from pathlib import Path
import json,re,subprocess
root=Path(__file__).resolve().parents[1]
subprocess.run(['pdfinfo','build/main.pdf'],cwd=root,check=True,stdout=(root/'evidence/pdfinfo.txt').open('w'))
subprocess.run(['pdftotext','-layout','build/main.pdf','evidence/main-text.txt'],cwd=root,check=True)
info=(root/'evidence/pdfinfo.txt').read_text();pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
aux=(root/'build/main.aux').read_text()
wanted=['thm:intro-stationary-physical-windows','sec:stationary-collision-band',
 'thm:wide-collision-band','thm:projected-collision-windows','sec:stationary-physical-conditioning',
 'lem:stationary-length-bias','prop:stationary-observation-coupling',
 'thm:stationary-physical-windows','cor:stationary-weighted-selection']
found={}
for label in wanted:
    match=re.search(r'\\newlabel\{'+re.escape(label)+r'\}\{\{([^{}]*)\}\{(\d+)',aux)
    if not match:raise RuntimeError('missing rendered label '+label)
    found[label]={'number':match.group(1),'page':int(match.group(2))}
first=found['sec:stationary-collision-band']['page'];last=found['cor:stationary-weighted-selection']['page']
selected=sorted({1,found[wanted[0]]['page']}|set(range(first,min(last+2,pages)+1)))
for page in selected:
    subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-r','90','-png',
                    'build/main.pdf',f'evidence/render-{page:03d}'],cwd=root,check=True)
checks=json.loads((root/'evidence/v29-source-and-finite-checks.json').read_text())
receipt=json.loads((root/'evidence/build-receipt.json').read_text())
summary={'event_sha':receipt['event_sha'],'workflow_run_id':receipt['workflow_run_id'],
 'pdf_pages':pages,'pdf_sha256':receipt['pdf_sha256'],'ordinary_paper_tree':receipt['ordinary_paper_tree'],
 'new_labels':found,'source':{k:v for k,v in checks['source'].items() if k!='source_sha256'},
 'new_finite_checks':checks['new_finite_checks'],'rendered_pages':selected,
 'renders_generated':True,'independent_human_review':False,'continuum_proof_certified':False,
 'full_raw_LLT_certified':False}
(root/'evidence/qualification-summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print(json.dumps(summary,indent=2,sort_keys=True))
