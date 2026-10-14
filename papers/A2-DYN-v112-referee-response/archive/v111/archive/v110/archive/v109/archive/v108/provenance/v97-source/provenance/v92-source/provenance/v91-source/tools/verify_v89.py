#!/usr/bin/env python3
"""Verify exact variant identity, byte preservation and actual full-source assembly."""
from __future__ import annotations
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
from check_v77 import require
from check_v89 import checks
from verify_v74 import physical_tree
from assemble_v89 import assemble
PAPER=Path(__file__).resolve().parents[1]
BASE=PAPER.parent/'A2-DYN-v88-referee-response'
BASE_TREE='af3d5707cc0ccad7fc20a6a67887cc0dc0e58ef6'
PARALLEL=PAPER.parent/'A2-DYN-v88-main-preserved'
PARALLEL_TREE='1c3e7c85c15f7265f66f8ee96ce6617d2f65488d'
REPORTS={
 'reviews/a2-dyn-v88-weaklp-external-top4-review-2026-10-12/REFEREE_REPORT.md':'90affffc4882c6312707aea59b0d2c51d6f4be28',
 'reviews/a2-dyn-v88-external-top4-review-2026-10-12/REFEREE_REPORT.md':'874290c1568d86c93d7e93606b05fc8439d6662f'}
NEW=['208_critical_surface_distribution.tex','209_logarithmic_endpoint_and_exceptional_source.tex','210_diffusive_window_and_exact_limit_order.tex']

def git(*args: str) -> str:
    return subprocess.check_output(['git',*args],cwd=PAPER,text=True).strip()

def source_check(local: bool) -> dict:
    require(physical_tree(BASE)==BASE_TREE,'weak-Lp v88 baseline changed')
    require(physical_tree(PARALLEL)==PARALLEL_TREE,'parallel main-v88 source changed')
    m=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    require(m['revision']==89 and m['active_core_count']==210,'active revision/count')
    require(m['revision_identifier']=='a2-dyn-v89-critical-distribution-2026-10-12','variant identity')
    require('new_estimate' not in m and 'inherited_estimate_v87' in m,'stale active estimate')
    if local:
        require(os.environ.get('GITHUB_ACTIONS')!='true','local mode forbidden in CI')
        head='local byte-pinned archive; not a remote checkout qualification'
        report_check='report blobs pinned by connected GitHub reads; full Git checks required remotely'
    else:
        head=git('rev-parse','HEAD')
        require(git('rev-parse','HEAD:papers/A2-DYN-v88-referee-response')==BASE_TREE,'Git weak-Lp tree')
        require(git('rev-parse','HEAD:papers/A2-DYN-v88-main-preserved')==PARALLEL_TREE,'Git parallel tree')
        for p,h in REPORTS.items():require(git('rev-parse','HEAD:'+p)==h,'review blob changed: '+p)
        if os.environ.get('GITHUB_ACTIONS')=='true':require(head==os.environ.get('GITHUB_SHA'),'wrong SHA')
        report_check='both exact report blobs verified in Git'
    preserved={}
    for folder,pattern in [('core','*.tex'),('appendices','*.tex'),('tools','*.py'),('provenance','*')]:
        files=[x for x in sorted((BASE/folder).rglob(pattern)) if x.is_file()]
        for x in files:require(x.read_bytes()==(PAPER/x.relative_to(BASE)).read_bytes(),'inherited bytes: '+str(x))
        preserved[folder]=len(files)
    require(preserved['core']==207 and len(list((PAPER/'core').glob('*.tex')))==210,'core preservation/count')
    for x in BASE.glob('*references*.tex'):require(x.read_bytes()==(PAPER/x.name).read_bytes(),'bibliography changed')
    roots=[x for x in BASE.iterdir() if x.is_file()]
    for x in roots:require(x.read_bytes()==(PAPER/'provenance'/('v88-'+x.name)).read_bytes(),'v88 snapshot: '+x.name)
    old=json.loads((BASE/'SOURCE_MANIFEST.json').read_text())
    for k,v in old['claims'].items():require(m['claims'].get(k) is v,'inherited flag changed: '+k)
    for k in ['full_raw_return_LLT_proved','original_critical_residence_source_charge_zero_proved',
              'unweakened_critical_weak_error_convergence_proved','unnormalized_growing_window_Lp_convergence_proved',
              'critical_distribution_bound_promoted_to_essential_height','independent_human_review','formal_proof_certificate']:
        require(m['claims'][k] is False,'unproved endpoint promoted: '+k)
    require(json.loads((PAPER/'PUBLICATION_STATUS.json').read_text())==m['claims'],'status mismatch')
    main=(PAPER/'main.tex').read_text()
    for n in NEW:require(r'\input{core/'+n[:-4]+'}' in main,'missing core in journal: '+n)
    assemble()
    master=(PAPER/'build/supplement-source.tex').read_text()
    require(master.count('Superseded dyadic notation.')==1,'historical dyadic notice')
    require(master.count('hypertexnames=false')==1,'PDF archive target names')
    require(r'\part{Untruncated residence moments and the raw local norm}' in master,'missing full v88 article')
    hashes={str(x.relative_to(PAPER)):hashlib.sha256(x.read_bytes()).hexdigest()
            for x in sorted(PAPER.rglob('*')) if x.is_file()
            and not set(x.relative_to(PAPER).parts)&{'build','evidence','__pycache__'}}
    return {'checkout_sha':head,'weaklp_baseline_tree':BASE_TREE,'parallel_tree':PARALLEL_TREE,
            'report_blobs':REPORTS,'report_verification':report_check,'preserved':preserved,
            'v88_top_level_snapshots':len(roots),'active_core_count':210,'source_sha256':hashes}

def main() -> None:
    args=sys.argv[1:];require(args in ([],['--local']),'unknown verifier arguments')
    (PAPER/'build').mkdir(exist_ok=True);(PAPER/'evidence').mkdir(exist_ok=True)
    r={'revision':89,'finite_checks':checks(),'source':source_check(bool(args)),
       'formal_proof_certificate':False,'independent_human_review':False}
    for v in [*range(76,82),83,84,85,86,87,88]:r[f'inherited_v{v}_finite_checks']=importlib.import_module(f'check_v{v}').checks()
    from check_v75_geometry import checks as v75
    from verify_v74 import finite_checks as v74
    r['inherited_v75_finite_checks']=v75();r['inherited_v74_finite_checks']=v74()
    print(json.dumps(r,indent=2,sort_keys=True))
if __name__=='__main__':main()
