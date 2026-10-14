#!/usr/bin/env python3
"""Pin the complete v97 source, new proofs and conditional claim boundary."""
from __future__ import annotations
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
from check_v98 import require, checks
from verify_v74 import physical_tree
PAPER=Path(__file__).resolve().parents[1]
BASE=PAPER.parent/'A2-DYN-v97-referee-response'
BASE_TREE='dea215a65a5b3f3ff51d4448cce551abed75fd1d'
BASE_COMMIT='6dd3149985ff5f6aca9dce9e2c186589df309872'
REVIEW='reviews/a2-dyn-v97-external-top4-review-2026-10-13/REFEREE_REPORT.md'
REVIEW_BLOB='a8b4f9dc2b6079adb8b43912f5807a59c3d977b9'
VARIANTS={'papers/A2-DYN-v88-referee-response':'af3d5707cc0ccad7fc20a6a67887cc0dc0e58ef6',
 'papers/A2-DYN-v88-main-preserved':'1c3e7c85c15f7265f66f8ee96ce6617d2f65488d'}
NEW=['235_quadratic_gradient_cap_and_uncut_insertion.tex',
 '236_disjoint_residuals_and_critical_height_certificate.tex',
 '237_paired_physical_traces_and_scalar_reduction.tex']
IGNORED={'build','evidence','__pycache__'}
REPLACED={'main.tex','supplement.tex','build.sh','SOURCE_MANIFEST.json','PUBLICATION_STATUS.json',
 'README.md','RESPONSE_TO_REFEREE.md','REFEREE_STATUS.md','PROOF_LEDGER.md','DEPENDENCY_MAP.md',
 'SPECIALIST_AUDIT.md','JOURNAL_ROUTE.md','VALIDATION.md','LOCAL_FULL_BUILD_RECORD.md','OVERLAY_SHA256.json'}

def git(*args: str) -> str:
    return subprocess.check_output(['git',*args],cwd=PAPER,text=True).strip()

def authored_check() -> dict:
    inventory=json.loads((PAPER/'OVERLAY_SHA256.json').read_text())
    for name,digest in inventory.items():
        require(hashlib.sha256((PAPER/name).read_bytes()).hexdigest()==digest,'authored hash: '+name)
    main=(PAPER/'main.tex').read_text()
    for name in NEW:require(r'\input{core/'+name[:-4]+'}' in main,'omitted new core: '+name)
    m=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    require(m['revision']==98 and m['active_core_count']==237,'wrong revision/count')
    require(m['baseline_paper_tree']==BASE_TREE,'wrong baseline')
    require(json.loads((PAPER/'PUBLICATION_STATUS.json').read_text())==
            {k:m[k] for k in ('inherited_packet','claims','superseded_claims')},'status mismatch')
    return inventory

def source_check(local: bool) -> dict:
    require(physical_tree(BASE)==BASE_TREE,'frozen v97 bytes or modes changed')
    require(physical_tree(PAPER/'provenance/v97-source')==BASE_TREE,'complete v97 snapshot changed')
    require((BASE/'main.tex').read_bytes()==(PAPER/'provenance/v97-main.tex').read_bytes(),'archive article changed')
    receipt=json.loads((PAPER/'BASELINE_RESOLVED_CLAIMS.json').read_text())
    require(receipt['baseline_author_commit']==BASE_COMMIT and receipt['baseline_paper_tree']==BASE_TREE,'claim receipt identity')
    if local:
        require(os.environ.get('GITHUB_ACTIONS')!='true','local archive mode forbidden in CI')
        head='local byte-pinned archive; not exact remote checkout qualification'
        old=receipt['resolved_claims']
        claim_source='qualified v97 exact-SHA receipt; Git recomputation required remotely'
    else:
        head=git('rev-parse','HEAD')
        for path,sha in {'papers/A2-DYN-v97-referee-response':BASE_TREE,
                         'papers/A2-DYN-v98-referee-response/provenance/v97-source':BASE_TREE,
                         REVIEW:REVIEW_BLOB,**VARIANTS}.items():
            require(git('rev-parse','HEAD:'+path)==sha,'Git source pin: '+path)
        if os.environ.get('GITHUB_ACTIONS')=='true':require(head==os.environ.get('GITHUB_SHA'),'wrong checkout SHA')
        from verify_v97 import claims_at
        old=claims_at(BASE)
        require(old==receipt['resolved_claims'],'qualified receipt disagrees with inherited Git source')
        claim_source='independently recomputed inherited Git source and matched qualified receipt'
    m=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    require(not {k for k,v in m['claims'].items() if k in old and old[k] is not v},'inherited claim changed')
    require(m['superseded_claims']=={},'unexpected supersession')
    resolved={**old,**m['claims']}
    for key in ['full_raw_return_LLT_proved','primary_referee_request_closed',
                'comparison_failure_source_charge_zero_proved','original_critical_residence_source_charge_zero_proved',
                'bidirectional_signed_forcing_zero_proved','full_critical_target_core_height_decay_proved',
                'spectral_capacity_condition_verified','weighted_gradient_multiplicity_growth_bound_proved',
                'positive_paired_short_trace_height_decay_proved','independent_human_review','formal_proof_certificate']:
        require(resolved[key] is False,'unsupported claim: '+key)
    preserved={k:0 for k in ('core','tools','appendices','provenance','root')}
    for src in BASE.rglob('*'):
        if not src.is_file():continue
        rel=src.relative_to(BASE)
        if set(rel.parts)&IGNORED:continue
        if len(rel.parts)==1 and rel.name in REPLACED:continue
        dest=PAPER/rel
        require(dest.is_file() and src.read_bytes()==dest.read_bytes(),'inherited bytes: '+str(rel))
        require(bool(src.stat().st_mode&0o111)==bool(dest.stat().st_mode&0o111),'inherited mode: '+str(rel))
        key=rel.parts[0] if rel.parts[0] in preserved else 'root';preserved[key]+=1
    require(preserved['core']==234 and len(list((PAPER/'core').glob('*.tex')))==237,'core coverage')
    from assemble_v98 import assemble
    assemble()
    hashes={str(f.relative_to(PAPER)):hashlib.sha256(f.read_bytes()).hexdigest()
            for f in sorted(PAPER.rglob('*')) if f.is_file() and not set(f.relative_to(PAPER).parts)&IGNORED}
    return {'checkout_sha':head,'baseline_tree':BASE_TREE,'review_blob':REVIEW_BLOB,
            'claim_source':claim_source,'preserved':preserved,'resolved_claims':resolved,'source_sha256':hashes}

def main() -> None:
    args=sys.argv[1:];require(args in ([],['--local'],['--preview']),'unknown arguments')
    preview=args==['--preview'];local=args==['--local']
    require(not args or os.environ.get('GITHUB_ACTIONS')!='true','local modes forbidden in CI')
    result={'revision':98,'finite_checks':checks(),'authored_sha256':authored_check(),
            'qualification_mode':'journal preview' if preview else ('local full archive' if local else 'exact checkout and full archive'),
            'spectral_capacity_verified':False,'formal_proof_certificate':False,'independent_human_review':False}
    if not preview:
        result['source']=source_check(local)
        for v in [*range(76,82),*range(83,98)]:
            result[f'inherited_v{v}_finite_checks']=importlib.import_module(f'check_v{v}').checks()
        from check_v75_geometry import checks as c75
        from verify_v74 import finite_checks as c74
        result['inherited_v75_finite_checks']=c75();result['inherited_v74_finite_checks']=c74()
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
