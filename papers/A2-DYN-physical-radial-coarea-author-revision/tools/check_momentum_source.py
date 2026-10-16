#!/usr/bin/env python3
"""Verify necessary native source identities; never certify a theorem by labels."""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def require(x,m):
    if not x:raise RuntimeError(m)
def rec(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),
            'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def main():
    manifest=P/'SOURCE_MANIFEST.json';M=json.loads(manifest.read_text())
    for name,expected in M['current_files'].items():
        p=P/name;require(p.is_file(),'missing declared source '+name)
        require(rec(p)==expected,'source identity mismatch '+name)
    for name,h in M['unchanged_predecessor_blobs'].items():
        require(rec(P/name)['git_blob']==h,'changed inherited native proof/interface '+name)
    queue=[P/'main.tex'];seen=set();labels=[];refs=[]
    while queue:
        p=queue.pop();relative=p.relative_to(P).as_posix()
        if relative in seen:continue
        require(p.is_file(),'missing native input '+relative);seen.add(relative)
        s=p.read_text()
        require(not any(ord(c)<32 and c not in '\n\t\r' for c in s),'control character in '+relative)
        s=re.sub(r'(?<!\\)%[^\n]*','',s)
        labels+=re.findall(r'\\label\{([^}]+)\}',s)
        refs+=re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',s)
        for target in re.findall(r'\\input\{([^}]+)\}',s):
            require(not target.startswith('/') and '..' not in Path(target).parts,'external native input')
            queue.append(P/(target if target.endswith('.tex') else target+'.tex'))
    require(len(set(labels))==len(labels),'duplicate native labels')
    require(set(refs)<=set(labels),'unresolved native labels '+str(sorted(set(refs)-set(labels))))
    require(len([s for s in seen if s.startswith('core/')])==26,'incomplete 260-285 native proof chain')
    require(M['full_raw_pointwise_LLT_proved'] is False,'misstated final target')
    frozen=P/'provenance/uniform-frozen';frozen_present=frozen.is_dir()
    if frozen_present:
        descriptor=M['full_predecessor_manifest']
        fm=P/descriptor['path'];require(fm.is_file(),'missing full preservation manifest')
        require(rec(fm)=={k:descriptor[k] for k in ['bytes','sha256','git_blob']},'full preservation manifest changed')
        expected=json.loads(fm.read_text())['files']
        # Full archive audit is optional in a compact remote native checkout;
        # its absence is reported explicitly, not counted as preservation proof.
        actual={x.relative_to(frozen).as_posix() for x in frozen.rglob('*') if x.is_file()}
        require(actual==set(expected),'full frozen archive path set mismatch')
        for name,h in expected.items():
            require(rec(frozen/name)['git_blob']==h,'full frozen archive changed '+name)
    print(json.dumps({'status':'passed','scope':'byte/structure identity, not mathematical certification',
         'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),
         'declared_current_files':len(M['current_files']),'native_tex_files':len(seen),
         'native_labels':len(labels),'unchanged_numbered_proofs':24,'unchanged_interfaces':7,
         'unresolved_labels':0,'full_predecessor_archive_present_here':frozen_present,
         'full_predecessor_archive_declared_files':M['full_predecessor_manifest']['file_count'],
         'all_historical_branch_bytes_audited':False,'independent_proof_certificate':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
