#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

root = Path(__file__).resolve().parents[1]
papers = root/'papers'
expected = [
 'paper-I-specular-ensembles',
 'paper-II-specular-homogenization',
 'paper-III-specular-theta',
 'paper-IV-specular-control',
 'paper-V-specular-rigidity',
]
errors=[]
dirs=sorted(p.name for p in papers.iterdir() if p.is_dir())
if dirs != expected:
    errors.append(f'paper directories mismatch: {dirs}')
for name in expected:
    d=papers/name
    for req in ['main.tex','references.bib','README.md','REFEREE_GUIDE.md']:
        if not (d/req).is_file(): errors.append(f'missing {name}/{req}')
    tex=list(d.glob('*.tex'))
    if [p.name for p in tex] != ['main.tex']:
        errors.append(f'{name}: active tex files {tex}')
    bib=list(d.glob('*.bib'))
    if [p.name for p in bib] != ['references.bib']:
        errors.append(f'{name}: active bib files {bib}')
    text=(d/'main.tex').read_text(encoding='utf-8')
    if 'OB3-PE-v1' not in text and name != 'paper-V-specular-rigidity':
        errors.append(f'{name}: missing platform id')
    if '\\bibliography{references}' not in text:
        errors.append(f'{name}: bibliography binding missing')
for p in root.rglob('*'):
    if p.is_file() and re.search(r'(main-(v\d+|final|round|submission)|FINAL_STATUS|LATEST_WINS)',p.name,re.I):
        errors.append(f'forbidden historical filename: {p.relative_to(root)}')
manifest=(papers/'SERIES_MANIFEST.yaml').read_text(encoding='utf-8')
for token in ['OB3-PE-v1','gibbs_conditioning','physical_theta_generator','saddle_envelope']:
    if token not in manifest: errors.append(f'manifest missing {token}')
result={'status':'PASS' if not errors else 'FAIL','errors':errors,'paper_count':len(dirs)}
(root/'status'/'VERIFICATION_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
sys.exit(1 if errors else 0)
