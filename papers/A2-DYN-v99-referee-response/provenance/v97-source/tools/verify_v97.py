#!/usr/bin/env python3
"""Exact source and claim preservation; preview is never remote qualification."""
from __future__ import annotations
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
from check_v97 import require, checks
PAPER=Path(__file__).resolve().parents[1]
BASE=PAPER.parent/'A2-DYN-v96-referee-response'
BASE_TREE='4490aafb771c8ff417c55030319a02d9602564fa'
REVIEW='reviews/a2-dyn-v96-external-top4-review-2026-10-13/REFEREE_REPORT.md'
REVIEW_BLOB='ea21dc4b10a43ffa53e7a3b0b79bf48f34ac0404'
VARIANTS={'papers/A2-DYN-v88-referee-response':'af3d5707cc0ccad7fc20a6a67887cc0dc0e58ef6',
 'papers/A2-DYN-v88-main-preserved':'1c3e7c85c15f7265f66f8ee96ce6617d2f65488d'}
NEW=['232_capped_coarea_occupation.tex','233_running_compression_height.tex',
     '234_quantitative_failure_source_reduction.tex']
IGNORED={'build','evidence','__pycache__'}
REPLACED={'main.tex','supplement.tex','build.sh','SOURCE_MANIFEST.json','PUBLICATION_STATUS.json',
 'README.md','RESPONSE_TO_REFEREE.md','REFEREE_STATUS.md','PROOF_LEDGER.md','DEPENDENCY_MAP.md',
 'SPECIALIST_AUDIT.md','JOURNAL_ROUTE.md','VALIDATION.md','LOCAL_FULL_BUILD_RECORD.md','OVERLAY_SHA256.json'}

def git(*args: str) -> str:
    return subprocess.check_output(['git',*args],cwd=PAPER,text=True).strip()

def claims_at(packet: Path, seen: set[Path] | None=None) -> dict:
    packet=packet.resolve(); seen=set() if seen is None else set(seen)
    require(packet not in seen,'cyclic inherited claim authority');seen.add(packet)
    m=json.loads((packet/'SOURCE_MANIFEST.json').read_text())
    old=claims_at(packet/m['inherited_packet'],seen) if m.get('inherited_packet') else {}
    return {**old,**m['claims']}

def authored_check() -> dict:
    inventory=json.loads((PAPER/'OVERLAY_SHA256.json').read_text())
    for name,digest in inventory.items():
        require(hashlib.sha256((PAPER/name).read_bytes()).hexdigest()==digest,'authored hash: '+name)
    main=(PAPER/'main.tex').read_text()
    for name in NEW:require(r'\input{core/'+name[:-4]+'}' in main,'omitted new core: '+name)
    m=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    require(m['revision']==97 and m['active_core_count']==234,'wrong revision/count')
    require(json.loads((PAPER/'PUBLICATION_STATUS.json').read_text())==
            {k:m[k] for k in ('inherited_packet','claims','superseded_claims')},'status mismatch')
    return inventory

def source_check() -> dict:
    from verify_v74 import physical_tree
    require(physical_tree(BASE)==BASE_TREE,'frozen v96 bytes or modes changed')
    require(physical_tree(PAPER/'provenance/v96-source')==BASE_TREE,'complete v96 snapshot changed')
    require((BASE/'main.tex').read_bytes()==(PAPER/'provenance/v96-main.tex').read_bytes(),'archive article changed')
    head=git('rev-parse','HEAD')
    for path,sha in {'papers/A2-DYN-v96-referee-response':BASE_TREE,
                     'papers/A2-DYN-v97-referee-response/provenance/v96-source':BASE_TREE,
                     REVIEW:REVIEW_BLOB,**VARIANTS}.items():
        require(git('rev-parse','HEAD:'+path)==sha,'Git source pin: '+path)
    if os.environ.get('GITHUB_ACTIONS')=='true':
        require(head==os.environ.get('GITHUB_SHA'),'wrong checkout SHA')
    m=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    old=claims_at(BASE)
    require(not {k for k,v in m['claims'].items() if k in old and old[k] is not v},'inherited flag promotion')
    require(m['superseded_claims']=={},'unexpected supersession')
    resolved={**old,**m['claims']}
    for key in ['full_raw_return_LLT_proved','primary_referee_request_closed',
                'comparison_failure_source_charge_zero_proved','original_critical_residence_source_charge_zero_proved',
                'bidirectional_signed_forcing_zero_proved','full_critical_target_core_height_decay_proved',
                'independent_human_review','formal_proof_certificate']:
        require(resolved[key] is False,'unsupported claim: '+key)
    preserved={k:0 for k in ('core','tools','appendices','provenance','root')}
    for p in BASE.rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(BASE)
        if set(rel.parts)&IGNORED:continue
        if len(rel.parts)==1 and rel.name in REPLACED:continue
        dest=PAPER/rel
        require(dest.is_file() and p.read_bytes()==dest.read_bytes(),'inherited bytes: '+str(rel))
        require(bool(p.stat().st_mode&0o111)==bool(dest.stat().st_mode&0o111),'inherited mode: '+str(rel))
        key=rel.parts[0] if rel.parts[0] in preserved else 'root';preserved[key]+=1
    require(preserved['core']==231,'inherited core count')
    require(len(list((PAPER/'core').glob('*.tex')))==234,'active core count')
    from assemble_v97 import assemble
    assemble()
    hashes={str(p.relative_to(PAPER)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(PAPER.rglob('*')) if p.is_file() and not set(p.relative_to(PAPER).parts)&IGNORED}
    return {'checkout_sha':head,'baseline_tree':BASE_TREE,'review_blob':REVIEW_BLOB,
            'preserved':preserved,'resolved_claims':resolved,'source_sha256':hashes}

def main() -> None:
    args=sys.argv[1:];require(args in ([],['--preview']),'unknown arguments')
    preview=bool(args)
    require(not preview or os.environ.get('GITHUB_ACTIONS')!='true','preview forbidden in CI')
    authored=authored_check()
    result={'revision':97,'finite_checks':checks(),'authored_sha256':authored,
            'qualification_mode':'local journal preview only' if preview else 'exact checkout and full archive',
            'formal_proof_certificate':False,'independent_human_review':False}
    if not preview:
        result['source']=source_check()
        for v in [*range(76,82),*range(83,97)]:
            result[f'inherited_v{v}_finite_checks']=importlib.import_module(f'check_v{v}').checks()
        from check_v75_geometry import checks as c75
        from verify_v74 import finite_checks as c74
        result['inherited_v75_finite_checks']=c75();result['inherited_v74_finite_checks']=c74()
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
