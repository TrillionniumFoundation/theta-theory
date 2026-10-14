#!/usr/bin/env python3
"""Exact-source preservation, resolved claim status, finite fixtures and full assembly."""
from __future__ import annotations
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
from check_v77 import require
from check_v90 import checks
from verify_v74 import physical_tree, obj_hash
from assemble_v90 import assemble
PAPER=Path(__file__).resolve().parents[1]
BASE=PAPER.parent/'A2-DYN-v89-referee-response'
BASE_TREE='85ffb2f2b372670cf5ccb3dbf3c2032d4c835a51'
ROOT_TREE='1453a92647c1fbb8e44e9b0c988f21a0109a357d'
REVIEW='reviews/a2-dyn-v89-external-top4-review-2026-10-12/REFEREE_REPORT.md'
REVIEW_BLOB='1dba5b7de5447a59483fc790e6072f9e165aa8e3'
VARIANTS={'papers/A2-DYN-v88-referee-response':'af3d5707cc0ccad7fc20a6a67887cc0dc0e58ef6',
          'papers/A2-DYN-v88-main-preserved':'1c3e7c85c15f7265f66f8ee96ce6617d2f65488d'}
NEW=['211_two_sided_end_layers_and_source_oscillation.tex',
     '212_cutoff_uniform_original_source_prefixes.tex',
     '213_microscopic_fractional_variation_and_endpoint_scope.tex']

def git(*args: str) -> str:
    return subprocess.check_output(['git',*args],cwd=PAPER,text=True).strip()

def source_check(local: bool) -> dict:
    require(physical_tree(BASE)==BASE_TREE,'v89 baseline changed')
    require(physical_tree(PAPER/'provenance/v89-root')==ROOT_TREE,'v89 complete root snapshot')
    require((PAPER/'provenance/v89-main.tex').read_bytes()==(BASE/'main.tex').read_bytes(),'full v89 article snapshot')
    m=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    require(m['revision']==90 and m['active_core_count']==213,'revision/count')
    require(m['revision_identifier']=='a2-dyn-v90-original-source-oscillation-2026-10-12','revision identity')
    require(m['inherited_status']['path']=='provenance/v89-root/PUBLICATION_STATUS.json','inherited status route')
    status_path=PAPER/m['inherited_status']['path']
    require(obj_hash('blob',status_path.read_bytes())==m['inherited_status']['blob'],'frozen inherited status')
    inherited=json.loads(status_path.read_text())
    require(inherited==json.loads((BASE/'SOURCE_MANIFEST.json').read_text())['claims'],'baseline claim identity')
    for k,v in m['claims'].items():
        if k in inherited:require(v is inherited[k],'inherited claim promoted: '+k)
    resolved={**inherited,**m['claims']}
    public=json.loads((PAPER/'PUBLICATION_STATUS.json').read_text())
    require(public=={'inherited_status':m['inherited_status'],'claims':m['claims']},'active status mismatch')
    for k in ['full_raw_return_LLT_proved','primary_referee_request_closed',
              'original_critical_residence_source_charge_zero_proved',
              'unweakened_critical_weak_error_convergence_proved',
              'mean_oscillation_promoted_to_essential_height',
              'independent_human_review','formal_proof_certificate']:
        require(resolved[k] is False,'unproved assertion promoted: '+k)
    if local:
        require(os.environ.get('GITHUB_ACTIONS')!='true','local mode forbidden in CI')
        head='local exact-baseline archive; not remote checkout qualification'
        report_check='remote Git report pins still required'
    else:
        head=git('rev-parse','HEAD')
        require(git('rev-parse','HEAD:papers/A2-DYN-v89-referee-response')==BASE_TREE,'Git v89 source tree')
        require(git('rev-parse','HEAD:'+REVIEW)==REVIEW_BLOB,'controlling review blob')
        for path,sha in VARIANTS.items():require(git('rev-parse','HEAD:'+path)==sha,'preserved v88 variant: '+path)
        if os.environ.get('GITHUB_ACTIONS')=='true':require(head==os.environ.get('GITHUB_SHA'),'wrong checkout SHA')
        report_check='controlling report and both preserved v88 variants verified in Git'
    preserved={}
    for folder,pattern in [('core','*.tex'),('appendices','*.tex'),('tools','*.py'),('provenance','*')]:
        paths=[x for x in sorted((BASE/folder).rglob(pattern)) if x.is_file()]
        for x in paths:
            dest=PAPER/x.relative_to(BASE)
            require(x.read_bytes()==dest.read_bytes(),'inherited source: '+str(x.relative_to(BASE)))
            require(bool(x.stat().st_mode & 0o111)==bool(dest.stat().st_mode & 0o111),'inherited executable mode')
        preserved[folder]=len(paths)
    require(preserved['core']==210 and len(list((PAPER/'core').glob('*.tex')))==213,'core preservation/count')
    for x in BASE.glob('*references*.tex'):require(x.read_bytes()==(PAPER/x.name).read_bytes(),'bibliography preservation')
    for name in ['journal-problem-v89.tex','journal-inputs-v89.tex']:
        require((BASE/name).read_bytes()==(PAPER/name).read_bytes(),'v89 included source changed')
    roots=[x for x in BASE.iterdir() if x.is_file()]
    for x in roots:require(x.read_bytes()==(PAPER/'provenance/v89-root'/x.name).read_bytes(),'root snapshot: '+x.name)
    main=(PAPER/'main.tex').read_text()
    for name in NEW:require(r'\input{core/'+name[:-4]+'}' in main,'missing journal core')
    assemble()
    master=(PAPER/'build/supplement-source.tex').read_text()
    require(master.count('Superseded dyadic notation.')==1,'dyadic clarification retained')
    require(r'\part{Critical distribution and the complete diffusive window}' in master,'full preceding article missing')
    hashes={str(x.relative_to(PAPER)):hashlib.sha256(x.read_bytes()).hexdigest()
            for x in sorted(PAPER.rglob('*')) if x.is_file()
            and not set(x.relative_to(PAPER).parts)&{'build','evidence','__pycache__'}}
    return {'checkout_sha':head,'baseline_paper_tree':BASE_TREE,'root_snapshot_tree':ROOT_TREE,
            'report_blob':REVIEW_BLOB,'report_verification':report_check,'preserved':preserved,
            'v89_top_level_snapshots':len(roots),'active_core_count':213,
            'resolved_claims':resolved,'source_sha256':hashes}

def main() -> None:
    args=sys.argv[1:];require(args in ([],['--local']),'unknown verifier arguments')
    (PAPER/'build').mkdir(exist_ok=True);(PAPER/'evidence').mkdir(exist_ok=True)
    result={'revision':90,'finite_checks':checks(),'source':source_check(bool(args)),
            'formal_proof_certificate':False,'independent_human_review':False}
    for v in [*range(76,82),83,84,85,86,87,88,89]:
        result[f'inherited_v{v}_finite_checks']=importlib.import_module(f'check_v{v}').checks()
    from check_v75_geometry import checks as v75
    from verify_v74 import finite_checks as v74
    result['inherited_v75_finite_checks']=v75();result['inherited_v74_finite_checks']=v74()
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
