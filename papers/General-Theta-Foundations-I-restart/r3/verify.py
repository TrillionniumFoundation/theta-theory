#!/usr/bin/env python3
"""Read-only source, label, citation, and receipt verification for restart r3."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parent

def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def source_audit() -> dict:
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    paths=[x['path'] for x in manifest['files']]
    require(len(paths)==len(set(paths)), 'Duplicate source manifest path')
    for item in manifest['files']:
        p=ROOT/item['path']
        require(p.is_file(), 'Missing source: '+item['path'])
        require(digest(p)==item['sha256'], 'Source hash mismatch: '+item['path'])
        require(p.stat().st_size==item['bytes'], 'Source size mismatch: '+item['path'])
    native=sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*.tex'))
    require(set(native)<=set(paths), 'Unmanifested TeX source')
    text='\n'.join((ROOT/x).read_text() for x in native)
    text=re.sub(r'(?<!\\)%[^\n]*','',text)
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    require(len(labels)==len(set(labels)), 'Duplicate mathematical label')
    refs=re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}',text)
    require(set(refs)<=set(labels),'Undefined labels: '+str(sorted(set(refs)-set(labels))))
    bibs=re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',text)
    require(len(bibs)==len(set(bibs)), 'Duplicate bibliography key')
    cites=[]
    for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',text):
        cites.extend(x.strip() for x in group.split(','))
    require(set(cites)<=set(bibs), 'Undefined citation')
    require(set(bibs)<=set(cites), 'Uncited bibliography item')
    for inc in re.findall(r'\\input\{([^}]+)\}',text):
        require((ROOT/(inc if inc.endswith('.tex') else inc+'.tex')).is_file(), 'Missing include '+inc)
    kinds=('theorem','lemma','proposition','corollary')
    statements=sum(len(re.findall(r'\\begin\{'+k+r'\}',text)) for k in kinds)
    proofs=len(re.findall(r'\\begin\{proof\}',text))
    require(statements==proofs,'Formal statement / proof count mismatch')
    legacy=json.loads((ROOT/'INHERITANCE.json').read_text())
    require(set(legacy['formal_labels'])<=set(labels), 'An inherited formal result was removed')
    return {'source_files':len(paths),'tex_files':len(native),'labels':len(labels),
            'citations':len(bibs),'formal_statements':statements,'proofs':proofs,
            'inherited_formal_labels':len(legacy['formal_labels']),
            'manifest_sha256':digest(ROOT/'SOURCE_MANIFEST.json')}

def regressions(optimized: bool=False) -> dict:
    import sys
    out={}
    for name in ('regression_legacy.py','regression_new.py'):
        cmd=[sys.executable]+(['-O'] if optimized else [])+[str(ROOT/name)]
        p=subprocess.run(cmd,text=True,capture_output=True,check=True)
        out[name]=json.loads(p.stdout)
    return out

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--read-only',action='store_true')
    ap.add_argument('--source-sha')
    ap.add_argument('--artifact-sha')
    args=ap.parse_args()
    result={'status':'success','source_audit':source_audit(),'continuum_proof_by_tests':False}
    normal=regressions(False);opt=regressions(True)
    require(normal==opt,'Normal and optimized regression results differ')
    result['regressions']=normal
    result['normal_optimized_identical']=True
    if args.read_only:
        receipt=json.loads((ROOT/'evidence/BUILD_RECEIPT.json').read_text())
        require(receipt['source_commit']==args.source_sha,'Source SHA receipt mismatch')
        require(receipt['paper_sha256']==digest(ROOT/'paper.pdf'),'Paper hash mismatch')
        require(receipt['source_audit']==result['source_audit'],'Source audit receipt mismatch')
        require(receipt['independent_rebuild_identical'],'Independent rebuild failed')
        head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
        require(head==args.artifact_sha,'Read-only head mismatch')
        parent=subprocess.check_output(['git','rev-parse','HEAD^'],cwd=ROOT,text=True).strip()
        require(parent==args.source_sha,'Artifact parent is not exact source')
        changed=subprocess.check_output(['git','diff','--name-only',parent,head],cwd=ROOT,text=True).splitlines()
        prefix='papers/General-Theta-Foundations-I-restart/r3/'
        require(all(x==prefix+'paper.pdf' or x.startswith(prefix+'evidence/') for x in changed),
                'Artifact commit modified mathematical source')
        require(not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip(),
                'Read-only verification found tracked modifications')
        result.update(source_commit=args.source_sha,artifact_commit=head,artifact_parent=parent,
                      paper_sha256=digest(ROOT/'paper.pdf'),read_only=True,
                      artifact_only_paths=changed)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
