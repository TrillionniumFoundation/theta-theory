#!/usr/bin/env python3
"""Exact baseline, unchanged histories, explicit supersession and full assembly."""
from __future__ import annotations
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
from check_v91 import require, checks
from verify_v74 import physical_tree
from assemble_v91 import assemble
PAPER=Path(__file__).resolve().parents[1]
BASE=PAPER.parent/'A2-DYN-v90-referee-response'
BASE_TREE='01d42f467a87817d7b756615a438f95bd8072369'
REVIEW='reviews/a2-dyn-v90-external-top4-review-2026-10-12/REFEREE_REPORT.md'
REVIEW_BLOB='6fb5c325fc24eff1934b8134a5c4432a90d04486'
NEW=['214_scale_gluing_and_unweakened_critical_limit.tex',
     '215_original_source_critical_power.tex','216_all_radius_maximal_source_control.tex']
VARIANTS={'papers/A2-DYN-v88-referee-response':'af3d5707cc0ccad7fc20a6a67887cc0dc0e58ef6',
          'papers/A2-DYN-v88-main-preserved':'1c3e7c85c15f7265f66f8ee96ce6617d2f65488d'}

def git(*args: str) -> str:
    return subprocess.check_output(['git',*args],cwd=PAPER,text=True).strip()

def old_claims() -> dict:
    status=json.loads((BASE/'PUBLICATION_STATUS.json').read_text())
    inherited=json.loads((BASE/status['inherited_status']['path']).read_text())
    require(all(isinstance(v,bool) for v in inherited.values()),'flat v89 status')
    return {**inherited,**status['claims']}

def verify(local: bool) -> dict:
    require(physical_tree(BASE)==BASE_TREE,'frozen v90 paper changed')
    require(physical_tree(PAPER/'provenance/v90-source')==BASE_TREE,'complete v90 snapshot changed')
    require((PAPER/'provenance/v90-main.tex').read_bytes()==(BASE/'main.tex').read_bytes(),'v90 main snapshot')
    manifest=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    require(manifest['revision']==91 and manifest['active_core_count']==216,'revision/count')
    inherited=old_claims(); active=manifest['claims']
    changed={k for k,v in active.items() if k in inherited and inherited[k] is not v}
    require(changed=={'unweakened_critical_weak_error_convergence_proved'},'unlisted inherited promotion')
    require(inherited[next(iter(changed))] is False and active[next(iter(changed))] is True,'critical supersession')
    require(manifest['superseded_claims']['unweakened_critical_weak_error_convergence_proved']['proof']=='thm:v91-raw','proof-backed supersession')
    resolved={**inherited,**active}
    for key in ['full_raw_return_LLT_proved','primary_referee_request_closed',
                'original_critical_residence_source_charge_zero_proved',
                'mean_oscillation_promoted_to_essential_height',
                'strong_critical_LQ_convergence_proved','independent_human_review','formal_proof_certificate']:
        require(resolved[key] is False,'unsupported endpoint promotion: '+key)
    public=json.loads((PAPER/'PUBLICATION_STATUS.json').read_text())
    require(public=={'inherited_packet':'provenance/v90-source','claims':active,
                     'superseded_claims':manifest['superseded_claims']},'publication status mismatch')
    if local:
        require(os.environ.get('GITHUB_ACTIONS')!='true','local mode forbidden in CI')
        head='local exact archive; not remote checkout qualification'
    else:
        head=git('rev-parse','HEAD')
        require(git('rev-parse','HEAD:papers/A2-DYN-v90-referee-response')==BASE_TREE,'Git v90 pin')
        require(git('rev-parse','HEAD:'+REVIEW)==REVIEW_BLOB,'controlling report pin')
        for path,sha in VARIANTS.items():require(git('rev-parse','HEAD:'+path)==sha,'variant pin: '+path)
        if os.environ.get('GITHUB_ACTIONS')=='true':require(head==os.environ.get('GITHUB_SHA'),'checkout SHA')
    preserved={}
    for folder,pattern in [('core','*.tex'),('appendices','*.tex'),('tools','*.py'),('provenance','*')]:
        paths=[p for p in sorted((BASE/folder).rglob(pattern)) if p.is_file()]
        for src in paths:
            dest=PAPER/src.relative_to(BASE)
            require(src.read_bytes()==dest.read_bytes(),'inherited bytes: '+str(src.relative_to(BASE)))
            require(bool(src.stat().st_mode&0o111)==bool(dest.stat().st_mode&0o111),'inherited mode')
        preserved[folder]=len(paths)
    require(preserved['core']==213 and len(list((PAPER/'core').glob('*.tex')))==216,'core count')
    for src in BASE.iterdir():
        if src.is_file():require(src.read_bytes()==(PAPER/'provenance/v90-source'/src.name).read_bytes(),'root snapshot: '+src.name)
    for src in BASE.glob('*references*.tex'):
        require(src.read_bytes()==(PAPER/src.name).read_bytes(),'bibliography changed')
    for name in ['journal-problem-v89.tex','journal-inputs-v89.tex','journal-inputs-v90.tex']:
        require((BASE/name).read_bytes()==(PAPER/name).read_bytes(),'inherited included source')
    main=(PAPER/'main.tex').read_text()
    for name in NEW:require(r'\input{core/'+name[:-4]+'}' in main,'new core not loaded')
    assemble()
    hashes={str(p.relative_to(PAPER)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(PAPER.rglob('*')) if p.is_file()
            and not set(p.relative_to(PAPER).parts)&{'build','evidence','__pycache__'}}
    return {'checkout_sha':head,'baseline_tree':BASE_TREE,'review_blob':REVIEW_BLOB,
            'preserved':preserved,'resolved_claims':resolved,'source_sha256':hashes}

def main() -> None:
    args=sys.argv[1:];require(args in ([],['--local']),'unknown arguments')
    (PAPER/'build').mkdir(exist_ok=True);(PAPER/'evidence').mkdir(exist_ok=True)
    result={'revision':91,'finite_checks':checks(),'source':verify(bool(args)),
            'formal_proof_certificate':False,'independent_human_review':False}
    for v in [*range(76,82),83,84,85,86,87,88,89,90]:
        result[f'inherited_v{v}_finite_checks']=importlib.import_module(f'check_v{v}').checks()
    from check_v75_geometry import checks as v75
    from verify_v74 import finite_checks as v74
    result['inherited_v75_finite_checks']=v75();result['inherited_v74_finite_checks']=v74()
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
