#!/usr/bin/env python3
"""Exact author-tree preservation, with regression-tested full-tree enumeration."""
from __future__ import annotations
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
from check_v104 import checks,require
from verify_v97 import claims_at
PAPER=Path(__file__).resolve().parents[1]
BASE=PAPER.parent/'A2-DYN-v103-referee-response'
BASE_TREE='3657fe1eb821ec398484f0487f3a8095dd44deed'
PAPER_PATH='papers/A2-DYN-v104-referee-response'
BASE_PATH='papers/A2-DYN-v103-referee-response'
VARIANTS={'papers/A2-DYN-v88-referee-response':'af3d5707cc0ccad7fc20a6a67887cc0dc0e58ef6',
'papers/A2-DYN-v88-main-preserved':'1c3e7c85c15f7265f66f8ee96ce6617d2f65488d'}

def git(*args):
    return subprocess.check_output(['git',*args],cwd=PAPER,text=True).strip()

def entries(tree):
    # --full-tree is essential when cwd is nested under the repository root.
    raw=subprocess.check_output(['git','ls-tree','-rz','--full-tree',tree],cwd=PAPER)
    result={}
    for item in raw.split(b'\0'):
        if not item:continue
        meta,name=item.split(b'\t',1);mode,kind,sha=meta.decode().split()
        require(kind=='blob','unexpected submodule in paper source')
        result[name.decode()]=(mode,sha)
    return result

def blob(path):
    b=path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def main():
    require(not sys.argv[1:],'exact-checkout qualification has no archive or preview bypass')
    (PAPER/'build').mkdir(exist_ok=True);(PAPER/'evidence').mkdir(exist_ok=True)
    head=git('rev-parse','HEAD')
    if os.environ.get('GITHUB_ACTIONS')=='true':require(head==os.environ.get('GITHUB_SHA'),'wrong final checkout SHA')
    m=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    require(m['revision']==104 and m['active_core_count']==252,'active revision/count')
    require(m['baseline_paper_tree']==BASE_TREE,'manifest baseline pin')
    require(git('rev-parse','HEAD:'+BASE_PATH)==BASE_TREE,'frozen v103 Git tree')
    for path,sha in VARIANTS.items():require(git('rev-parse','HEAD:'+path)==sha,'historical variant changed')
    for field in ('controlling_review','mathematical_review'):
        require(git('rev-parse','HEAD:'+m[field+'_path'])==m[field+'_blob'],'frozen report changed: '+field)
    repo_root=git('rev-parse','--show-toplevel')
    changed=subprocess.check_output(['git','diff','--name-only',m['baseline_author_commit'],head],cwd=repo_root,text=True).splitlines()
    allowed=(PAPER_PATH+'/',m['controlling_review_path'],
             'A2_DYN_V104_POSITIVE_INTERVAL_REVISION_INDEX.md',
             '.github/workflows/a2-dyn-v104-positive-interval-qualification.yml')
    require(all(n.startswith(allowed[0]) or n in allowed[1:] for n in changed),'unrelated committed repository change')
    old=claims_at(BASE)
    require(m['superseded_claims']=={},'unexpected inherited claim supersession')
    for k,v in m['claims'].items():
        if k in old:require(old[k] is v,'inherited claim promoted: '+k)
    resolved={**old,**m['claims']}
    for k in ('full_raw_return_LLT_proved','primary_referee_request_closed',
              'all_three_clock_failure_height_decay_proved','full_comparison_deficit_height_decay_proved',
              'independent_human_review','formal_proof_certificate'):
        require(resolved[k] is False,'unsupported completion: '+k)
    require(json.loads((PAPER/'PUBLICATION_STATUS.json').read_text())==
            {k:m[k] for k in ('inherited_packet','claims','superseded_claims')},'publication status mismatch')
    inherited=entries(BASE_TREE);active=entries('HEAD:'+PAPER_PATH)
    require(inherited and active,'empty tree enumeration is not preservation')
    roots=set(m['replaced_root_files']); counts={'core':0,'tools':0,'appendices':0,'provenance':0,'other':0}
    for name,record in inherited.items():
        dst='provenance/v103-'+name if name in roots else name
        require(active.get(dst)==record,'inherited Git bytes/mode: '+name)
        p=PAPER/dst
        require(blob(p)==record[1],'working source bytes: '+dst)
        require(bool(p.stat().st_mode&0o111)==(record[0]=='100755'),'working executable mode: '+dst)
        key=name.split('/',1)[0];counts[key if key in counts else 'other']+=1
    ncore=sum(n.startswith('core/') and n.endswith('.tex') for n in inherited)
    acore=sum(n.startswith('core/') and n.endswith('.tex') for n in active)
    require(ncore==249 and acore==252,'complete inherited/active mathematical core count')
    authored={}
    for name,record in active.items():
        p=PAPER/name
        require(blob(p)==record[1],'tracked source differs from HEAD: '+name)
        require(bool(p.stat().st_mode&0o111)==(record[0]=='100755'),'tracked source mode: '+name)
        if inherited.get(name)!=record:authored[name]=hashlib.sha256(p.read_bytes()).hexdigest()
    maintex=(PAPER/'main.tex').read_text()
    for name in m['new_core_modules']:
        require(r'\input{'+name[:-4]+'}' in maintex,'new core missing from article: '+name)
    from assemble_v104 import assemble
    assemble()
    master=(PAPER/'build/supplement-source.tex').read_text()
    require(master.count(r'\part{Endpoint-distance coarea and positive recovery}')==1,'complete preceding v103 article')
    require(master.count('Superseded dyadic notation.')==1,'historical correction omitted/duplicated')
    out={'revision':104,'finite_checks':checks(),'source':{'checkout_sha':head,
        'paper_tree':git('rev-parse','HEAD:'+PAPER_PATH),'baseline_tree':BASE_TREE,
        'preserved_files':counts,'inherited_core_count':ncore,'active_core_count':acore,
        'replaced_root_snapshots':sum(n in inherited for n in roots),'authored_sha256':authored,
        'tracked_source_files':len(active),'resolved_claims':resolved},
        'formal_proof_certificate':False,'independent_human_review':False}
    for v in [*range(76,82),*range(83,101),102,103]:
        out[f'inherited_v{v}_finite_checks']=importlib.import_module(f'check_v{v}').checks()
    from check_v75_geometry import checks as c75
    from verify_v74 import finite_checks as c74
    out['inherited_v75_finite_checks']=c75();out['inherited_v74_finite_checks']=c74()
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
