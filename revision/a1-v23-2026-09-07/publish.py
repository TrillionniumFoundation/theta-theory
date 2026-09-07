#!/usr/bin/env python3
"""Rerun the pinned v22 referee diagnostics and publish this revision only."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[2]
TARGET=ROOT/'papers/A1-english-v23'
PREFIX='papers/A1-english-v23/'
BRANCH='revision/a1-english-v23-collision-spine-saturated-proof-2026-09-07'
REFEREE=ROOT/'reviews/a1-english-v22-harsh-independent-2026-09-07/independent_diagnostics.py'
BLOB='8b4fc8f5e957f9b298f9dbb54165b15e92a5f986'
def command(args):
    return subprocess.run(args,cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()
def main():
    if os.environ.get('GITHUB_REF')!='refs/heads/'+BRANCH:
        raise RuntimeError('Publication is restricted to the new v23 branch')
    out=TARGET/'validation'
    execution=json.loads((out/'EXECUTION_REPORT.json').read_text())
    if execution.get('passed') is not True or execution.get('assertions_total')!=178160:
        raise RuntimeError('Complete author validation has not passed')
    if execution.get('pdf_pages')!=125: raise RuntimeError('Unexpected article length')
    data=REFEREE.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if blob!=BLOB: raise ValueError('Referee script identity mismatch')
    for optimized in (False,True):
        suffix='OPTIMIZED' if optimized else 'RERUN'
        result=out/f'REFEREE_V22_{suffix}.json'
        args=[sys.executable]+(['-O'] if optimized else [])+[str(REFEREE),str(result)]
        with (out/f'referee-v22-{suffix.lower()}-stdout.txt').open('w') as log:
            subprocess.run(args,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=300)
    regular=out/'REFEREE_V22_RERUN.json';optimized=out/'REFEREE_V22_OPTIMIZED.json'
    if regular.read_bytes()!=optimized.read_bytes(): raise ValueError('Referee optimization mismatch')
    r=json.loads(regular.read_text())
    if (r.get('status'),r.get('checks'),r.get('models'),r.get('full_histories'),r.get('checked_prefixes'))!=('PASS',13884,50,400,1200):
        raise ValueError('Unexpected pinned referee diagnostic receipt')
    subprocess.run([sys.executable,'manifest.py'],cwd=TARGET,check=True)
    publication={'version':23,'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),
        'workflow_input_commit':os.environ.get('GITHUB_SHA'),
        'controlling_review':'325e89b9c012830cbd219fec0cff7c52b8e8d321',
        'source_manifest_sha256':hashlib.sha256((TARGET/'SOURCE_MANIFEST.json').read_bytes()).hexdigest(),
        'author_checks':178160,'pdf_pages':125,'pdf_sha256':execution['pdf_sha256'],
        'referee_v22_rerun':{'source_git_blob':blob,'status':'PASS','checks':13884,
            'models':50,'histories':400,'prefixes':1200,'optimized_identical':True,
            'scope':'Rerun of the pinned existing referee diagnostic, not a fresh independent assessment.'},
        'publication_scope':PREFIX,'inherited_manuscripts_modified':False}
    (out/'PUBLICATION_INPUT_V23.json').write_text(json.dumps(publication,indent=2)+'\n')
    outside=[p for p in command(['git','diff','--name-only']).splitlines() if not p.startswith(PREFIX)]
    if outside: raise RuntimeError('Tracked changes outside new revision: '+repr(outside))
    paths=[]
    for p in sorted(TARGET.rglob('*')):
        if not p.is_file() or '__pycache__' in p.parts: continue
        if p.suffix in ('.pyc','.aux','.out','.toc','.fls','.fdb_latexmk'): continue
        paths.append(p.relative_to(ROOT).as_posix())
    for i in range(0,len(paths),200): command(['git','add','-f','--',*paths[i:i+200]])
    staged=command(['git','diff','--cached','--name-only']).splitlines()
    if any(not p.startswith(PREFIX) for p in staged): raise RuntimeError('Staged publication scope violation')
    if not staged:
        print('Validated source already published.'); return
    command(['git','config','user.name','github-actions[bot]'])
    command(['git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com'])
    command(['git','commit','-m','A1 v23: publish complete English revision, 125-page PDF and executed validation [skip ci]'])
    command(['git','push','origin','HEAD:refs/heads/'+BRANCH])
    print('Published commit '+command(['git','rev-parse','HEAD']))
if __name__=='__main__':main()
