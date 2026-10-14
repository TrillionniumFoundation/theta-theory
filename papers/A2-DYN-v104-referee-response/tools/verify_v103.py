#!/usr/bin/env python3
"""Exact Git-source preservation and inherited claim boundaries for revision 103."""
from __future__ import annotations
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
from check_v100 import require
from check_v103 import checks
from verify_v97 import claims_at
PAPER=Path(__file__).resolve().parents[1]
BASE=PAPER.parent/'A2-DYN-v102-referee-response'
BASE_TREE='2ac230d86ffc9c4907e57f0e425b80d97971a6c9'
REVIEW_COMMIT='37faf38478a5b561c3aa4a1faf63da378caf8189'
REVIEW='reviews/a2-dyn-v102-external-top4-review-2026-10-13/REFEREE_REPORT.md'
REVIEW_BLOB='6c6bbd2fc9fd5e6da575ac6db9827448e091af3d'
REPLACED={'main.tex','supplement.tex','build.sh','SOURCE_MANIFEST.json','PUBLICATION_STATUS.json',
'README.md','RESPONSE_TO_REFEREE.md','PROOF_LEDGER.md','DEPENDENCY_MAP.md','SPECIALIST_AUDIT.md',
'VALIDATION.md','REFEREE_STATUS.md','JOURNAL_ROUTE.md','LOCAL_FULL_BUILD_RECORD.md'}
NEW=['247_endpoint_distance_coarea_and_critical_traces.tex','248_gap_clock_pointwise_recovery.tex',
'249_expanding_endpoint_certificate.tex']
VARIANTS={'papers/A2-DYN-v88-referee-response':'af3d5707cc0ccad7fc20a6a67887cc0dc0e58ef6',
'papers/A2-DYN-v88-main-preserved':'1c3e7c85c15f7265f66f8ee96ce6617d2f65488d'}

def git(*args):
    return subprocess.check_output(['git',*args],cwd=PAPER,text=True).strip()

def entries(tree):
    raw=subprocess.check_output(['git','ls-tree','-rz',tree],cwd=PAPER)
    out={}
    for item in raw.split(b'\0'):
        if not item:continue
        meta,name=item.split(b'\t',1);mode,kind,sha=meta.decode().split()
        require(kind=='blob','unexpected tracked submodule')
        out[name.decode()]=(mode,sha)
    return out

def blob(path):
    data=path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def main():
    require(not sys.argv[1:],'run in an exact Git checkout without local or preview flags')
    (PAPER/'build').mkdir(exist_ok=True);(PAPER/'evidence').mkdir(exist_ok=True)
    head=git('rev-parse','HEAD')
    if os.environ.get('GITHUB_ACTIONS')=='true':require(head==os.environ.get('GITHUB_SHA'),'wrong checkout SHA')
    require(git('rev-parse','HEAD:papers/A2-DYN-v102-referee-response')==BASE_TREE,'baseline Git tree')
    require(git('rev-parse','HEAD:'+REVIEW)==REVIEW_BLOB,'controlling report blob')
    for path,sha in VARIANTS.items():require(git('rev-parse','HEAD:'+path)==sha,'variant changed: '+path)
    m=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    require(m['revision']==103 and m['active_core_count']==249,'revision or count')
    require(m['baseline_paper_tree']==BASE_TREE and m['controlling_review_blob']==REVIEW_BLOB,'manifest pins')
    require(m['inherited_packet']=='../A2-DYN-v102-referee-response','wrong inherited packet')
    old=claims_at(BASE)
    require(not {k for k,v in m['claims'].items() if k in old and old[k] is not v},'inherited claim promotion')
    require(m['superseded_claims']=={},'unexpected supersession')
    require(json.loads((PAPER/'PUBLICATION_STATUS.json').read_text())==
            {k:m[k] for k in ('inherited_packet','claims','superseded_claims')},'status mismatch')
    resolved={**old,**m['claims']}
    for key in ('full_raw_return_LLT_proved','primary_referee_request_closed',
                'positive_transverse_failure_trace_height_decay_proved',
                'positive_paired_short_trace_height_decay_proved',
                'all_three_clock_failure_height_decay_proved',
                'independent_human_review','formal_proof_certificate'):
        require(resolved[key] is False,'unsupported claim: '+key)
    base=entries(BASE_TREE); current=entries('HEAD:papers/A2-DYN-v103-referee-response')
    preserved={'core':0,'tools':0,'appendices':0,'provenance':0,'root':0}
    for name,record in base.items():
        destination='provenance/v102-'+name if name in REPLACED else name
        require(current.get(destination)==record,'inherited Git bytes or mode: '+name)
        path=PAPER/destination
        require(blob(path)==record[1],'working copy differs: '+destination)
        require(bool(path.stat().st_mode&0o111)==(record[0]=='100755'),'working mode: '+destination)
        key=name.split('/',1)[0];preserved[key if key in preserved else 'root']+=1
    require(preserved['core']==246,'inherited core count')
    require(len(list((PAPER/'core').glob('*.tex')))==249,'active core count')
    maintex=(PAPER/'main.tex').read_text()
    for name in NEW:require(r'\input{core/'+name[:-4]+'}' in maintex,'missing article module')
    changed=git('diff','--name-only',REVIEW_COMMIT,head).splitlines()
    allowed=('papers/A2-DYN-v103-referee-response/','.github/workflows/a2-dyn-v103-qualification.yml','A2_DYN_V103_REVISION_INDEX.md')
    require(all(p.startswith(allowed[0]) or p in allowed[1:] for p in changed),'unrelated repository mutation')
    authored={}
    for name,record in current.items():
        require(blob(PAPER/name)==record[1],'tracked file differs from author tree: '+name)
        if name not in base or base[name]!=record:
            authored[name]=hashlib.sha256((PAPER/name).read_bytes()).hexdigest()
    from assemble_v103 import assemble
    assemble()
    master=(PAPER/'build/supplement-source.tex').read_text()
    require(master.count(r'\part{Positive paired coarea and the relative transverse clock}')==1,'complete v102 article')
    require(master.count('Superseded dyadic notation.')==1,'historical correction notice')
    out={'revision':103,'finite_checks':checks(),'source':{'checkout_sha':head,
         'paper_tree':git('rev-parse','HEAD:papers/A2-DYN-v103-referee-response'),
         'baseline_tree':BASE_TREE,'review_blob':REVIEW_BLOB,'preserved':preserved,
         'replaced_root_snapshots':len(REPLACED),'resolved_claims':resolved,
         'authored_sha256':authored,'tracked_source_files':len(current)},
         'formal_proof_certificate':False,'independent_human_review':False}
    for v in [*range(76,82),*range(83,101),102]:
        out[f'inherited_v{v}_finite_checks']=importlib.import_module(f'check_v{v}').checks()
    from check_v75_geometry import checks as c75
    from verify_v74 import finite_checks as c74
    out['inherited_v75_finite_checks']=c75();out['inherited_v74_finite_checks']=c74()
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
