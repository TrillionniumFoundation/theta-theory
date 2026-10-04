#!/usr/bin/env python3
"""Verify and publish the authored v74 text delta on an immutable v73 input.

Only the new revision directory is written. The compressed payload is a
hash-pinned JSON unified diff, never a serialized Python object or command.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tempfile

BASE='ab67d30dc8ad190f1e4cea150a306c8ca3a4dc1f'
OLD='papers/GTF-I-v73-noisy-readout-crossover'
NEW='papers/GTF-I-v74-coupled-boundary-geometry'
BRANCH='revision/general-theta-foundations-i-v74-coupled-boundary-geometry-2026-10-04'
PAYLOAD='48e12bfc274b8c711bcddf7b2cb1ef5c2cd9b937fecfaaefa78a1c05d53c0035'
EXPECTED='8980fdd0692f77da51c3713c822c47f537b90a541434c65a82cab391eafb29cb'
PREDECESSOR='55cb4e7f11c886aab286f4da8fa4ae57794ba43ad16fcd84c34e803e11065ba8'
AUDITS={'README.md','PROOF_AUDIT.md','PROOF_STATUS.json','LITERATURE_AUDIT.md','HISTORY_AND_PIPELINE_AUDIT.md','RESPONSE_TO_REFEREE.md','CONTROLLING_REPORTS.json','PRESERVATION_MANIFEST.json','INDEPENDENT_REVIEW_BRIEF.md'}

def require(value, message):
    if not value: raise RuntimeError(message)

def digest(data): return hashlib.sha256(data).hexdigest()
def inventory_digest(inv): return digest(json.dumps(inv,sort_keys=True,separators=(',',':')).encode())
def git(repo,*args): return subprocess.check_output(['git',*args],cwd=repo,text=True).strip()
def safe_name(name):
    p=PurePosixPath(name)
    require(str(p)==name and not p.is_absolute() and '..' not in p.parts and '\\' not in name,'unsafe path')
    require(p.suffix in {'.py','.tex','.json','.md'},'unexpected native suffix')
    return p

def materialize(repo, here):
    compressed=b''.join((here/f'part-{i}.xz').read_bytes() for i in range(4))
    require(digest(compressed)==PAYLOAD,'authored patch digest mismatch')
    data=json.loads(lzma.decompress(compressed))
    require(set(data)=={'base_commit','base_root','destination','copies','inventory_sha256','patch'},'unexpected transfer schema')
    require((data['base_commit'],data['base_root'],data['destination'],data['inventory_sha256'])==(BASE,OLD,NEW,EXPECTED),'wrong pinned source')
    prior=repo/OLD; target=repo/NEW
    require(not target.exists(),'new revision directory already exists; refusing overwrite')
    inv=json.loads((prior/'evidence/SOURCE_HASHES.json').read_text())
    require(len(inv)==222 and inventory_digest(inv)==PREDECESSOR,'wrong predecessor inventory')
    for name,h in inv.items():
        safe_name(name); p=prior/name
        require(p.is_file() and not p.is_symlink() and digest(p.read_bytes())==h,'predecessor hash mismatch: '+name)
    spec=importlib.util.spec_from_file_location('v73_builder',prior/'build_revision.py')
    builder=importlib.util.module_from_spec(spec); spec.loader.exec_module(builder)
    require(builder.sources(prior)==inv,'predecessor native tree has unlisted files')
    expected_copies={'predecessor-v73-audit/'+n:n for n in AUDITS}
    require(data['copies']==expected_copies,'unexpected audit copies')
    for name in inv:
        dest=target/name; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(prior/name,dest)
    for name,old in data['copies'].items():
        dest=target/name; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(prior/old,dest)
    patch=data['patch']; require(isinstance(patch,str),'diff must be text')
    before=re.findall(r'^--- (.+)$',patch,re.M); after=re.findall(r'^\+\+\+ (.+)$',patch,re.M)
    require(len(before)==len(after)>0,'malformed diff headers')
    for a,b in zip(before,after):
        require(b.startswith('b/') and (a=='/dev/null' or (a.startswith('a/') and a[2:]==b[2:])),'renamed/deleted diff path')
        safe_name(b[2:]); require(b[2:]!='PRESERVATION_MANIFEST.json','preservation must be derived')
    with tempfile.TemporaryDirectory(prefix='gtf74-text-diff-') as td:
        patchfile=Path(td)/'authored.patch';patchfile.write_text(patch)
        for check in [True,False]:
            cmd=['git','apply']+(['--check'] if check else [])+['--directory='+NEW,str(patchfile)]
            subprocess.run(cmd,cwd=repo,check=True)
    manifest={'schema':'gtf74.preservation/1','base_commit':BASE,'source_root':OLD,'files':inv,
        'prior_labels':sorted(set(builder.graph(prior,'main.tex')[1])),
        'prior_proof_graphs':{e:{'files':sorted(builder.graph(prior,e)[0]),'labels':sorted(builder.graph(prior,e)[1])} for e in builder.DOCUMENTS},
        'method':'All predecessor paths remain unchanged in the Git tree; all previously typeset labels remain in each successor proof graph.'}
    (target/'PRESERVATION_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    final=builder.sources(target)
    require(len(final)==238 and inventory_digest(final)==EXPECTED,'authored native inventory mismatch')
    require(builder.sources(prior)==inv,'predecessor changed')
    return {'schema':'gtf74.native-transfer/1','base':BASE,'payload_sha256':PAYLOAD,
        'native_inventory_sha256':EXPECTED,'native_files':len(final),'predecessor_files':len(inv),
        'preserved_complete_labels':len(manifest['prior_labels'])}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check-only',action='store_true');args=ap.parse_args()
    here=Path(__file__).resolve().parent;repo=Path(git(here,'rev-parse','--show-toplevel'))
    original=git(repo,'rev-parse','HEAD')
    if not args.check_only:
        require(os.environ.get('GITHUB_SHA')==original,'wrong transfer checkout')
        require(os.environ.get('GITHUB_REF')=='refs/heads/'+BRANCH,'wrong branch')
        require(git(repo,'ls-remote','--heads','origin','refs/heads/'+BRANCH).split()[0]==original,'remote moved')
    receipt=materialize(repo,here);receipt['transfer_commit']=original
    require(not git(repo,'diff','--name-only'),'tracked input changed')
    if not args.check_only:
        git(repo,'config','user.name','github-actions[bot]')
        git(repo,'config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
        git(repo,'add',NEW)
        staged=git(repo,'diff','--cached','--name-only').splitlines()
        require(len(staged)==238 and all(n.startswith(NEW+'/') for n in staged),'unexpected staged files')
        require(git(repo,'ls-remote','--heads','origin','refs/heads/'+BRANCH).split()[0]==original,'remote moved before commit')
        git(repo,'commit','-m','feat(gtf-i): add v74 coupled boundary proofs and exact joint visibility codec')
        source=git(repo,'rev-parse','HEAD');receipt['source_commit']=source
        git(repo,'push','origin','HEAD:refs/heads/'+BRANCH)
        with open(os.environ['GITHUB_OUTPUT'],'a') as f:f.write('source='+source+'\n')
        (Path(os.environ['RUNNER_TEMP'])/'gtf74-native-transfer.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__': main()
