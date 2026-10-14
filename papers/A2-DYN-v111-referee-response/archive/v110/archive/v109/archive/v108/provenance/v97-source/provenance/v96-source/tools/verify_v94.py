#!/usr/bin/env python3
"""Check exact source/claim preservation and assemble the complete archive."""
from __future__ import annotations
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
from check_v94 import checks, require
from verify_v74 import physical_tree
from assemble_v94 import assemble
PAPER=Path(__file__).resolve().parents[1]
BASE=PAPER.parent/'A2-DYN-v93-referee-response'
BASE_TREE='ef2f30899784526ad41aac95fe88c7417761e558'
ROOT_TREE='d56ce08199c9177e2a2e7048ea810af911434e83'
REVIEW='reviews/a2-dyn-v93-external-top4-review-2026-10-12/REFEREE_REPORT.md'
REVIEW_BLOB='7625de487f043ac21dc59fe7d98639284ed8736a'
VARIANTS={'papers/A2-DYN-v88-referee-response':'af3d5707cc0ccad7fc20a6a67887cc0dc0e58ef6',
          'papers/A2-DYN-v88-main-preserved':'1c3e7c85c15f7265f66f8ee96ce6617d2f65488d'}
NEW=['223_noncritical_entrance_residence.tex','224_critical_radial_transit_packets.tex',
     '225_signed_projected_forcing_and_endpoint.tex']
IGNORED={'build','evidence','__pycache__'}
REPLACED={'main.tex','supplement.tex','build.sh','SOURCE_MANIFEST.json','PUBLICATION_STATUS.json',
          'README.md','RESPONSE_TO_REFEREE.md','REFEREE_STATUS.md','PROOF_LEDGER.md','DEPENDENCY_MAP.md',
          'SPECIALIST_AUDIT.md','JOURNAL_ROUTE.md','VALIDATION.md','LOCAL_FULL_BUILD_RECORD.md'}


def git(*args: str) -> str:
    return subprocess.check_output(['git',*args],cwd=PAPER,text=True).strip()


def claims_at(packet: Path, seen: frozenset = frozenset()) -> dict:
    key=packet.resolve()
    require(key not in seen,'claim inheritance cycle')
    manifest=json.loads((packet/'SOURCE_MANIFEST.json').read_text())
    old=claims_at(packet/manifest['inherited_packet'],seen|{key}) if manifest.get('inherited_packet') else {}
    return {**old,**manifest['claims']}


def source_check(local: bool) -> dict:
    require(physical_tree(BASE)==BASE_TREE,'frozen v93 paper bytes or modes changed')
    snapshot=PAPER/'provenance/v93-root'
    require(physical_tree(snapshot)==ROOT_TREE,'complete v93 root snapshot')
    for src in BASE.iterdir():
        if src.is_file():
            dst=snapshot/src.name
            require(dst.is_file() and src.read_bytes()==dst.read_bytes(),'root snapshot: '+src.name)
            require(bool(src.stat().st_mode&0o111)==bool(dst.stat().st_mode&0o111),'root mode: '+src.name)
    require((BASE/'main.tex').read_bytes()==(PAPER/'provenance/v93-main.tex').read_bytes(),'article snapshot')
    manifest=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    require(manifest['revision']==94 and manifest['active_core_count']==225,'revision or count')
    require(manifest['inherited_packet']=='../A2-DYN-v93-referee-response','baseline claim reference')
    old=claims_at(BASE); active=manifest['claims']; resolved={**old,**active}
    require(not {k for k,v in active.items() if k in old and old[k] is not v},'inherited flag promotion')
    require(manifest['superseded_claims']=={},'unexpected supersession')
    for key in ['full_raw_return_LLT_proved','primary_referee_request_closed',
                'original_critical_residence_source_charge_zero_proved',
                'ancestral_entrance_and_critical_gain_decay_proved',
                'joint_signed_upper_forcing_zero_proved','full_critical_target_core_height_decay_proved',
                'independent_human_review','formal_proof_certificate']:
        require(resolved[key] is False,'unsupported endpoint promotion: '+key)
    require(json.loads((PAPER/'PUBLICATION_STATUS.json').read_text())=={
        'inherited_packet':manifest['inherited_packet'],'claims':active,'superseded_claims':{}},'status mismatch')
    preserved={x:0 for x in ['core','tools','appendices','provenance','root']}
    for src in BASE.rglob('*'):
        if not src.is_file():continue
        rel=src.relative_to(BASE)
        if set(rel.parts)&IGNORED:continue
        if len(rel.parts)==1 and rel.name in REPLACED:continue
        dest=PAPER/rel
        require(dest.is_file() and src.read_bytes()==dest.read_bytes(),'inherited bytes: '+str(rel))
        require(bool(src.stat().st_mode&0o111)==bool(dest.stat().st_mode&0o111),'inherited mode: '+str(rel))
        key=rel.parts[0] if rel.parts[0] in preserved else 'root';preserved[key]+=1
    require(preserved['core']==222 and len(list((PAPER/'core').glob('*.tex')))==225,'complete core coverage')
    if local:
        require(os.environ.get('GITHUB_ACTIONS')!='true','local archive mode forbidden in CI')
        head='local byte-pinned archive; not remote checkout qualification'
    else:
        head=git('rev-parse','HEAD')
        require(git('rev-parse','HEAD:papers/A2-DYN-v93-referee-response')==BASE_TREE,'Git baseline')
        require(git('rev-parse','HEAD:'+REVIEW)==REVIEW_BLOB,'controlling review')
        for path,sha in VARIANTS.items():require(git('rev-parse','HEAD:'+path)==sha,'variant: '+path)
        if os.environ.get('GITHUB_ACTIONS')=='true':require(head==os.environ.get('GITHUB_SHA'),'wrong checkout')
    main=(PAPER/'main.tex').read_text()
    for name in NEW:require(r'\input{core/'+name[:-4]+'}' in main,'missing new core')
    assemble()
    hashes={str(x.relative_to(PAPER)):hashlib.sha256(x.read_bytes()).hexdigest()
            for x in sorted(PAPER.rglob('*')) if x.is_file()
            and not set(x.relative_to(PAPER).parts)&IGNORED}
    return {'checkout_sha':head,'baseline_tree':BASE_TREE,'root_snapshot_tree':ROOT_TREE,
            'review_blob':REVIEW_BLOB,'preserved':preserved,'resolved_claims':resolved,
            'source_sha256':hashes}


def main() -> None:
    args=sys.argv[1:];require(args in ([],['--local']),'unknown verifier arguments')
    (PAPER/'build').mkdir(exist_ok=True);(PAPER/'evidence').mkdir(exist_ok=True)
    result={'revision':94,'finite_checks':checks(),'source':source_check(bool(args)),
            'formal_proof_certificate':False,'independent_human_review':False}
    for v in [*range(76,82),*range(83,94)]:
        result[f'inherited_v{v}_finite_checks']=importlib.import_module(f'check_v{v}').checks()
    from check_v75_geometry import checks as c75
    from verify_v74 import finite_checks as c74
    result['inherited_v75_finite_checks']=c75();result['inherited_v74_finite_checks']=c74()
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
