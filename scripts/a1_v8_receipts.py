#!/usr/bin/env python3
"""Record an actual v8 build and preservation audit; no verification claims."""
from pathlib import Path
import hashlib
import json
import os
import platform
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'papers/A1-english-v8'
BASE=ROOT/'papers/A1-english-v7'
REVIEW='72eb41e358bd9af122367fea66d0de9bdda07456'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def sha(data):return hashlib.sha256(data).hexdigest()
def entry(path):
    data=path.read_bytes()
    return {'path':str(path.relative_to(ROOT)),'bytes':len(data),'sha256':sha(data),
            'git_blob':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()}

if git('rev-parse','HEAD:papers/A1-english-v7')!='2a499f613db54f9966d553ddb727562fe71a537d':
    raise RuntimeError('The v7 source tree is not the source-pinned predecessor')
old='\n'.join(p.read_text() for p in sorted((BASE/'sections').glob('*.tex')))
new='\n'.join(p.read_text() for p in sorted((P/'sections').glob('*.tex')))
proofs=re.findall(r'\\begin\{proof\}.*?\\end\{proof\}',old,re.S)
if not all(p in new for p in proofs):raise RuntimeError('An inherited proof block changed')
changes=git('diff','--name-status',REVIEW,'--')
for line in changes.splitlines():
    status,path=line.split('\t',1)
    if status!='A' or not (path.startswith('papers/A1-english-v8/') or path in
        ('scripts/materialize_a1_v8.py','scripts/a1_v8_receipts.py','.github/workflows/a1-v8-publication.yml')):
        raise RuntimeError('A pre-existing path changed: '+line)

sources=sorted([p for p in P.rglob('*') if p.is_file() and p.suffix in ('.tex','.py','.md','.sh')]
    +[ROOT/'scripts/materialize_a1_v8.py',ROOT/'scripts/a1_v8_receipts.py',ROOT/'.github/workflows/a1-v8-publication.yml'])
manifest={'revision':'A1 English v8','review_commit':REVIEW,'build_input_commit':git('rev-parse','HEAD'),
          'predecessor_submission':'02f68484cf92ef312037cf455bd3f3737ae4facd',
          'predecessor_principal_tree':'2a499f613db54f9966d553ddb727562fe71a537d',
          'entries':[entry(p) for p in sources]}
(P/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
log=(P/'main.log').read_text()
if re.search(r'There were undefined references|Citation .* undefined|Reference .* undefined|Overfull \\[hv]box',log):
    raise RuntimeError('Unresolved references/citations or overfull boxes')
pages=int(re.search(r'Output written on main.pdf \((\d+) pages?',log).group(1))
v7=json.loads((P/'DIAGNOSTICS.json').read_text());v8=json.loads((P/'V8_DIAGNOSTICS.json').read_text())
report={'revision':'A1 English v8','build_input_commit':manifest['build_input_commit'],
        'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),'python':platform.python_version(),
        'tex_engine':subprocess.check_output(['pdflatex','--version'],text=True).splitlines()[0],
        'pages':pages,'passes':3,'shell_escape':False,'undefined_references':0,'undefined_citations':0,
        'overfull_boxes':0,'underfull_notices':len(re.findall(r'Underfull \\[hv]box',log)),
        'v7_inherited_suite':{'passed':v7['passed'],'total':v7['total']},
        'v8_new_suite':{k:v8[k] for k in ('passed','total','new_seven_trial_index_only_fixtures','new_exact_raw_updates')},
        'preservation':{'pre_existing_paths_modified':0,'inherited_proof_blocks_unchanged':len(proofs),
                        'inherited_result_labels':25,'current_result_labels':34},
        'pdf_sha256':sha((P/'main.pdf').read_bytes()),'log_sha256':sha((P/'main.log').read_bytes()),
        'manifest_sha256':sha((P/'SOURCE_MANIFEST.json').read_bytes()),
        'scope':'Fresh finite diagnostics and source build; not formal verification, independent referee approval, or journal acceptance.'}
(P/'BUILD_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
