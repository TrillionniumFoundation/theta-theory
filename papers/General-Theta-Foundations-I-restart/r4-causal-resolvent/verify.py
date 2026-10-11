#!/usr/bin/env python3
"""Read-only source, label, citation, and receipt verification for restart r4 causal resolvent."""
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
    inventory=sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
                     if p.is_file() and 'evidence' not in p.relative_to(ROOT).parts
                     and '__pycache__' not in p.relative_to(ROOT).parts
                     and p.name not in ('SOURCE_MANIFEST.json','paper.pdf'))
    require(set(inventory)==set(paths), 'Complete native source inventory mismatch')
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
    seen=set()
    def visit(name):
        require(name not in seen, 'Repeated/cyclic include: '+name)
        seen.add(name)
        content=re.sub(r'(?<!\\)%[^\n]*','',(ROOT/name).read_text())
        for inc in re.findall(r'\\input\{([^}]+)\}',content):
            visit(inc if inc.endswith('.tex') else inc+'.tex')
    visit('main.tex')
    require(seen==set(native), 'Orphan or missing TeX source in main include graph')
    kinds=('theorem','lemma','proposition','corollary')
    statements=sum(len(re.findall(r'\\begin\{'+k+r'\}',text)) for k in kinds)
    proofs=len(re.findall(r'\\begin\{proof\}',text))
    require(statements==proofs,'Formal statement / proof count mismatch')
    legacy=json.loads((ROOT/'INHERITANCE.json').read_text())
    require(set(legacy['formal_labels'])<=set(labels), 'An inherited formal result was removed')
    for path,sha in legacy.get('unchanged_mathematical_files',{}).items():
        require(digest(ROOT/path)==sha, 'Unchanged inherited mathematics modified: '+path)
    return {'source_files':len(paths),'tex_files':len(native),'labels':len(labels),
            'citations':len(bibs),'formal_statements':statements,'proofs':proofs,
            'inherited_formal_labels':len(legacy['formal_labels']),
            'manifest_sha256':digest(ROOT/'SOURCE_MANIFEST.json')}

def regressions(optimized: bool=False) -> dict:
    import sys
    out={}
    for name in ('regression_legacy.py','regression_new.py','regression_transport.py'):
        cmd=[sys.executable]+(['-O'] if optimized else [])+[str(ROOT/name)]
        p=subprocess.run(cmd,text=True,capture_output=True,check=True)
        out[name]=json.loads(p.stdout)
    return out

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--read-only',action='store_true')
    ap.add_argument('--source-sha')
    ap.add_argument('--artifact-sha')
    ap.add_argument('--verification-sha')
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
        def git(*args):
            return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
        head=git('rev-parse','HEAD')
        expected=args.verification_sha or args.artifact_sha
        require(head==expected,'Read-only head mismatch')
        artifact_parent=git('rev-parse',args.artifact_sha+'^')
        require(artifact_parent==args.source_sha,'Artifact parent is not exact source')
        changed=git('diff','--name-only',args.source_sha,args.artifact_sha).splitlines()
        prefix='papers/General-Theta-Foundations-I-restart/r4-causal-resolvent/'
        allowed={prefix+'paper.pdf',prefix+'evidence/BUILD_RECEIPT.json',prefix+'evidence/REGRESSION.json'}
        require(set(changed)==allowed,'Artifact commit did not contain exactly the declared artifacts')
        result.update(source_commit=args.source_sha,artifact_commit=args.artifact_sha,
                      artifact_parent=artifact_parent,paper_sha256=digest(ROOT/'paper.pdf'),
                      read_only=True,artifact_only_paths=changed,verified_head=head)
        if args.verification_sha:
            require(git('rev-parse',head+'^')==args.artifact_sha,'Verification parent mismatch')
            vchanged=git('diff','--name-only',args.artifact_sha,head).splitlines()
            require(vchanged==[prefix+'evidence/READ_ONLY_AT_ARTIFACT.json'],
                    'Verification commit changed more than its receipt')
            stored=json.loads((ROOT/'evidence/READ_ONLY_AT_ARTIFACT.json').read_text())
            require(stored['verified_head']==args.artifact_sha,'Stored verification subject mismatch')
            require(stored['source_commit']==args.source_sha,'Stored source mismatch')
            require(stored['source_audit']==result['source_audit'],'Stored source audit mismatch')
            require(stored['regressions']==normal,'Stored regression mismatch')
            result.update(verification_commit=head,verification_only_paths=vchanged)
        require(not git('status','--porcelain','--untracked-files=no'),
                'Read-only verification found tracked modifications')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
