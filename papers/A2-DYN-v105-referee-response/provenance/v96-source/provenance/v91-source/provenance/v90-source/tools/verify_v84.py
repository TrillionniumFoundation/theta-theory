#!/usr/bin/env python3
"""Pin the reviewed source; preserve and qualify the full new article and archive."""
from __future__ import annotations
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
from check_v77 import require
from check_v84 import checks
from verify_v74 import physical_tree, obj_hash
from assemble_v84 import assemble

PAPER=Path(__file__).resolve().parents[1]
BASE=PAPER.parent/'A2-DYN-v83-referee-response'
BASE_TREE='5422c924a1a26006a2cd39c5776eae56a684849c'
REVIEW='reviews/a2-dyn-v83-external-top4-review-2026-10-12/REFEREE_REPORT.md'
REVIEW_BLOB='d5cb27a2f9bd769241c32941d77a08c5b438803f'
NEW=['193_backward_residence_surface_height.tex','194_paired_boundary_optical_transfer.tex',
     '195_canonical_concentration_and_endpoint.tex']


def git(*args: str) -> str:
    return subprocess.check_output(['git',*args],cwd=PAPER,text=True).strip()


def source_check(local: bool) -> dict:
    require(physical_tree(BASE)==BASE_TREE,'frozen v83 bytes or modes changed')
    m=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    require(m['revision']==84 and m['active_core_count']==195,'revision/count')
    review_path=PAPER.parents[1]/REVIEW
    if local and not review_path.exists():
        review_status='remote report read and blob pinned; local archive lacks report bytes; exact Git mode requires them'
    else:
        require(obj_hash('blob',review_path.read_bytes())==REVIEW_BLOB,'controlling report changed')
        review_status='verified exact report bytes'
    if local:
        require(os.environ.get('GITHUB_ACTIONS')!='true','local archive mode forbidden in CI')
        head='local exact-baseline source check; not remote checkout qualification'
    else:
        head=git('rev-parse','HEAD')
        require(git('rev-parse','HEAD:papers/A2-DYN-v83-referee-response')==BASE_TREE,'Git v83 tree')
        require(git('rev-parse','HEAD:'+REVIEW)==REVIEW_BLOB,'Git controlling report')
        if os.environ.get('GITHUB_ACTIONS')=='true':
            require(head==os.environ.get('GITHUB_SHA'),'wrong checkout SHA')
    preserved={}
    for folder,pattern in [('core','*.tex'),('appendices','*.tex'),('tools','*.py'),('provenance','*')]:
        files=[f for f in sorted((BASE/folder).rglob(pattern)) if f.is_file()]
        for src in files:
            require(src.read_bytes()==(PAPER/src.relative_to(BASE)).read_bytes(),
                    'inherited source changed: '+str(src.relative_to(BASE)))
        preserved[folder]=len(files)
    require(preserved['core']==192,'inherited core count')
    require(len(list((PAPER/'core').glob('*.tex')))==195,'active core count')
    for src in sorted(BASE.glob('*references*.tex')):
        require(src.read_bytes()==(PAPER/src.name).read_bytes(),'inherited bibliography changed')
    roots=[src for src in sorted(BASE.iterdir()) if src.is_file()]
    for src in roots:
        require(src.read_bytes()==(PAPER/'provenance'/('v83-'+src.name)).read_bytes(),
                'v83 top-level snapshot changed: '+src.name)
    old=json.loads((BASE/'SOURCE_MANIFEST.json').read_text())
    for key,value in old['claims'].items():
        require(m['claims'].get(key) is value,'inherited claim changed: '+key)
    for key in ['primary_referee_request_closed','full_raw_return_LLT_proved',
                'complete_nongrazing_outgoing_flux_height_decay_proved',
                'complete_microscopic_fractional_tail_height_decay_proved',
                'complete_paired_short_nongrazing_surface_height_decay_proved',
                'complete_short_critical_surface_height_decay_proved',
                'canonical_microscopic_concentration_charge_zero_proved',
                'independent_human_review','formal_proof_certificate']:
        require(m['claims'][key] is False,'unsupported endpoint promotion: '+key)
    require(json.loads((PAPER/'PUBLICATION_STATUS.json').read_text())==m['claims'],'stale status')
    main=(PAPER/'main.tex').read_text()
    for name in NEW:
        require(r'\input{core/'+name[:-4]+'}' in main,'missing new core')
    assemble()
    master=(PAPER/'build/supplement-source.tex').read_text()
    require(master.count('Superseded dyadic notation.')==1,'unqualified historical dyadic formula')
    hashes={str(f.relative_to(PAPER)):hashlib.sha256(f.read_bytes()).hexdigest()
            for f in sorted(PAPER.rglob('*')) if f.is_file()
            and not set(f.relative_to(PAPER).parts)&{'build','evidence','__pycache__'}}
    return {'checkout_sha':head,'baseline_v83_tree':BASE_TREE,
            'controlling_report_blob':REVIEW_BLOB,'review_verification':review_status,
            'preserved':preserved,'v83_top_level_snapshots':len(roots),
            'active_core_count':195,'source_sha256':hashes}


def main() -> None:
    args=sys.argv[1:];require(args in ([],['--local']),'unknown verifier arguments')
    (PAPER/'build').mkdir(exist_ok=True);(PAPER/'evidence').mkdir(exist_ok=True)
    result={'revision':84,'finite_checks':checks(),'source':source_check(bool(args)),
            'formal_proof_certificate':False,'independent_human_review':False}
    for version in [*range(76,82),83]:
        result[f'inherited_v{version}_finite_checks']=importlib.import_module(f'check_v{version}').checks()
    from check_v75_geometry import checks as v75
    from verify_v74 import finite_checks as v74
    result['inherited_v75_finite_checks']=v75();result['inherited_v74_finite_checks']=v74()
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
