#!/usr/bin/env python3
"""Exact source identity, inherited claim preservation and full assembly."""
from __future__ import annotations
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
from check_v96 import require, checks
from verify_v74 import physical_tree
from assemble_v96 import assemble
PAPER=Path(__file__).resolve().parents[1]
BASE=PAPER.parent/'A2-DYN-v95-referee-response'
BASE_TREE='5d15fd482383c35aac22d922c730a5d20cd69507'
ROOT_TREE='769c2bf87f6217a63755a3d03ebabf2059042865'
REVIEW='reviews/a2-dyn-v95-external-top4-review-2026-10-13/REFEREE_REPORT.md'
REVIEW_BLOB='23d0415a5c2823b67259c3697fb46d5b896c7584'
VARIANTS={'papers/A2-DYN-v88-referee-response':'af3d5707cc0ccad7fc20a6a67887cc0dc0e58ef6',
 'papers/A2-DYN-v88-main-preserved':'1c3e7c85c15f7265f66f8ee96ce6617d2f65488d'}
NEW=['229_same_label_continuation_occupation.tex',
     '230_recurrent_packets_and_untruncated_radial_core.tex',
     '231_continuation_failure_and_joint_forcing.tex']
IGNORED={'build','evidence','__pycache__'}
REPLACED={'main.tex','supplement.tex','build.sh','SOURCE_MANIFEST.json','PUBLICATION_STATUS.json',
 'README.md','RESPONSE_TO_REFEREE.md','REFEREE_STATUS.md','PROOF_LEDGER.md','DEPENDENCY_MAP.md',
 'SPECIALIST_AUDIT.md','JOURNAL_ROUTE.md','VALIDATION.md','LOCAL_FULL_BUILD_RECORD.md','OVERLAY_SHA256.json'}

def git(*args: str) -> str:
    return subprocess.check_output(['git',*args],cwd=PAPER,text=True).strip()

def claims_at(packet: Path) -> dict:
    m=json.loads((packet/'SOURCE_MANIFEST.json').read_text())
    old=claims_at(packet/m['inherited_packet']) if m.get('inherited_packet') else {}
    return {**old,**m['claims']}

def source_check(local: bool) -> dict:
    require(physical_tree(BASE)==BASE_TREE,'v95 bytes/modes changed')
    roots=[p for p in BASE.iterdir() if p.is_file()]
    for p in roots:
        q=PAPER/'provenance/v95-root'/p.name
        require(q.is_file() and p.read_bytes()==q.read_bytes(),'v95 root snapshot: '+p.name)
        require(bool(p.stat().st_mode&0o111)==bool(q.stat().st_mode&0o111),'snapshot mode: '+p.name)
    require(physical_tree(PAPER/'provenance/v95-root')==ROOT_TREE,'root snapshot tree')
    require((BASE/'main.tex').read_bytes()==(PAPER/'provenance/v95-main.tex').read_bytes(),'full prior article')
    m=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    require(m['revision']==96 and m['active_core_count']==231,'revision or active core count')
    old=claims_at(BASE);new=m['claims']
    require(not {k for k,v in new.items() if k in old and old[k] is not v},'inherited flag promotion')
    require(m['superseded_claims']=={},'unexpected supersession')
    resolved={**old,**new}
    for k in ['full_raw_return_LLT_proved','primary_referee_request_closed',
              'original_critical_residence_source_charge_zero_proved',
              'all_targets_satisfy_continuation_admission_proved',
              'comparison_failure_source_charge_zero_proved',
              'zero_gradient_annular_tail_height_decay_proved',
              'bidirectional_signed_forcing_zero_proved','independent_human_review','formal_proof_certificate']:
        require(resolved[k] is False,'unsupported endpoint promoted: '+k)
    require(json.loads((PAPER/'PUBLICATION_STATUS.json').read_text())==
       {k:m[k] for k in ('inherited_packet','claims','superseded_claims')},'status/manifest mismatch')
    preserved={k:0 for k in ('core','tools','appendices','provenance','root')}
    for p in BASE.rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(BASE)
        if set(rel.parts)&IGNORED:continue
        if len(rel.parts)==1 and rel.name in REPLACED:continue
        q=PAPER/rel
        require(q.is_file() and p.read_bytes()==q.read_bytes(),'inherited source: '+str(rel))
        require(bool(p.stat().st_mode&0o111)==bool(q.stat().st_mode&0o111),'inherited mode: '+str(rel))
        key=rel.parts[0] if rel.parts[0] in preserved else 'root';preserved[key]+=1
    require(preserved['core']==228 and len(list((PAPER/'core').glob('*.tex')))==231,'core preservation')
    if local:
        require(os.environ.get('GITHUB_ACTIONS')!='true','local mode forbidden in CI')
        head='local exact-baseline full archive; not remote SHA qualification'
    else:
        head=git('rev-parse','HEAD')
        require(git('rev-parse','HEAD:papers/A2-DYN-v95-referee-response')==BASE_TREE,'Git baseline')
        require(git('rev-parse','HEAD:'+REVIEW)==REVIEW_BLOB,'controlling report blob')
        for p,s in VARIANTS.items():require(git('rev-parse','HEAD:'+p)==s,'preserved variant: '+p)
        if os.environ.get('GITHUB_ACTIONS')=='true':require(head==os.environ.get('GITHUB_SHA'),'wrong checkout SHA')
    for n in NEW:require(r'\input{core/'+n[:-4]+'}' in (PAPER/'main.tex').read_text(),'omitted new core')
    inventory=json.loads((PAPER/'OVERLAY_SHA256.json').read_text())
    for name,digest in inventory.items():
        require(hashlib.sha256((PAPER/name).read_bytes()).hexdigest()==digest,'authored overlay hash: '+name)
    assemble()
    hashes={str(p.relative_to(PAPER)):hashlib.sha256(p.read_bytes()).hexdigest()
      for p in sorted(PAPER.rglob('*')) if p.is_file() and not set(p.relative_to(PAPER).parts)&IGNORED}
    return {'checkout_sha':head,'baseline_tree':BASE_TREE,'root_snapshot_tree':ROOT_TREE,
      'review_blob':REVIEW_BLOB,'preserved':preserved,'root_snapshots':len(roots),
      'resolved_claims':resolved,'source_sha256':hashes}

def main() -> None:
    args=sys.argv[1:];require(args in ([],['--local']),'unknown arguments')
    (PAPER/'build').mkdir(exist_ok=True);(PAPER/'evidence').mkdir(exist_ok=True)
    result={'revision':96,'finite_checks':checks(),'source':source_check(bool(args)),
      'formal_proof_certificate':False,'independent_human_review':False}
    for v in [*range(76,82),*range(83,96)]:
        result[f'inherited_v{v}_finite_checks']=importlib.import_module(f'check_v{v}').checks()
    from check_v75_geometry import checks as c75
    from verify_v74 import finite_checks as c74
    result['inherited_v75_finite_checks']=c75();result['inherited_v74_finite_checks']=c74()
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
