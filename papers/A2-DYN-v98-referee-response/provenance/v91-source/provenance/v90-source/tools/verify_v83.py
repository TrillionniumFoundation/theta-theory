#!/usr/bin/env python3
"""Exact-source preservation and finite fixtures; no mathematical certification."""
from __future__ import annotations
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
from check_v77 import require
from check_v83 import checks
from verify_v74 import physical_tree, obj_hash
from assemble_v83 import assemble

PAPER=Path(__file__).resolve().parents[1]
BASE=PAPER.parent/'A2-DYN-v82-referee-response'
BASE_TREE='d1908253a6d134b5b1e4c732e84ad111ad4f836a'
V81_TREE='1d68fef5bbd1abc573d8e517e845cf889fe6431c'
REVIEW='reviews/a2-dyn-v81-external-top4-review-2026-10-11/REFEREE_REPORT.md'
REVIEW_BLOB='818e5932c895aea686da68fe37cec6018d2de759'
NEW=['190_untruncated_optical_potentials.tex','191_complete_first_exit_surface_mass.tex',
     '192_ordered_fractional_tail_and_endpoint.tex']


def git(*args: str) -> str:
    return subprocess.check_output(['git',*args],cwd=PAPER,text=True).strip()


def source_check(local: bool) -> dict:
    require(physical_tree(BASE)==BASE_TREE,'frozen v82 source bytes or modes changed')
    v81=PAPER.parent/'A2-DYN-v81-referee-response'
    require(physical_tree(v81)==V81_TREE,'frozen v81 source changed')
    m=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    require(m['revision']==83 and m['active_core_count']==192,'revision/count')
    review_path=PAPER.parents[1]/REVIEW
    if local and not review_path.exists():
        review_status='report blob verified through remote read; local archive lacks report bytes; mandatory in exact Git mode'
    else:
        require(obj_hash('blob',review_path.read_bytes())==REVIEW_BLOB,'controlling report changed')
        review_status='verified exact report bytes'
    if local:
        require(os.environ.get('GITHUB_ACTIONS')!='true','local archive mode forbidden in CI')
        head='local exact-baseline source check; not remote checkout qualification'
    else:
        head=git('rev-parse','HEAD')
        require(git('rev-parse','HEAD:papers/A2-DYN-v82-referee-response')==BASE_TREE,'Git v82 tree')
        require(git('rev-parse','HEAD:'+REVIEW)==REVIEW_BLOB,'Git controlling report')
        if os.environ.get('GITHUB_ACTIONS')=='true':require(head==os.environ.get('GITHUB_SHA'),'wrong checkout SHA')
    preserved={}
    for folder,pattern in [('core','*.tex'),('appendices','*.tex'),('tools','*.py'),('provenance','*')]:
        files=[f for f in sorted((BASE/folder).rglob(pattern)) if f.is_file()]
        for src in files:
            require(src.read_bytes()==(PAPER/src.relative_to(BASE)).read_bytes(),
                    'inherited source changed: '+str(src.relative_to(BASE)))
        preserved[folder]=len(files)
    require(preserved['core']==189,'inherited core count')
    require(len(list((PAPER/'core').glob('*.tex')))==192,'active core count')
    for src in sorted(BASE.glob('*references*.tex')):
        require(src.read_bytes()==(PAPER/src.name).read_bytes(),'inherited bibliography changed')
    snapshots={}
    for version,base in [(81,v81),(82,BASE)]:
        roots=[p for p in base.iterdir() if p.is_file()]
        for src in roots:
            require(src.read_bytes()==(PAPER/'provenance'/f'v{version}-{src.name}').read_bytes(),
                    'historical top-level snapshot changed: '+str(src))
        snapshots[str(version)]=len(roots)
    old=json.loads((BASE/'SOURCE_MANIFEST.json').read_text())
    for key,value in old['claims'].items():require(m['claims'].get(key) is value,'inherited claim changed: '+key)
    for key in ['primary_referee_request_closed','full_raw_return_LLT_proved',
                'complete_critical_initial_defect_height_decay_proved',
                'complete_nongrazing_outgoing_flux_height_decay_proved',
                'complete_microscopic_fractional_tail_height_decay_proved',
                'surface_mass_bound_promoted_to_essential_height',
                'independent_human_review','formal_proof_certificate']:
        require(m['claims'][key] is False,'unsupported endpoint promotion: '+key)
    require(json.loads((PAPER/'PUBLICATION_STATUS.json').read_text())==m['claims'],'stale active status')
    main=(PAPER/'main.tex').read_text()
    for name in NEW:require(r'\input{core/'+name[:-4]+'}' in main,'missing new core in article')
    assemble()
    hashes={str(f.relative_to(PAPER)):hashlib.sha256(f.read_bytes()).hexdigest()
            for f in sorted(PAPER.rglob('*')) if f.is_file()
            and not set(f.relative_to(PAPER).parts)&{'build','evidence','__pycache__'}}
    return {'checkout_sha':head,'baseline_v82_tree':BASE_TREE,'baseline_v81_tree':V81_TREE,
            'controlling_report_blob':REVIEW_BLOB,'review_verification':review_status,
            'preserved':preserved,'top_level_snapshots':snapshots,'active_core_count':192,
            'source_sha256':hashes}


def main() -> None:
    args=sys.argv[1:];require(args in ([],['--local']),'unknown verifier arguments')
    (PAPER/'build').mkdir(exist_ok=True);(PAPER/'evidence').mkdir(exist_ok=True)
    result={'revision':83,'finite_checks':checks(),'source':source_check(bool(args)),
            'formal_proof_certificate':False,'independent_human_review':False}
    for version in range(76,82):
        result[f'inherited_v{version}_finite_checks']=importlib.import_module(f'check_v{version}').checks()
    from check_v75_geometry import checks as v75
    from verify_v74 import finite_checks as v74
    result['inherited_v75_finite_checks']=v75();result['inherited_v74_finite_checks']=v74()
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
