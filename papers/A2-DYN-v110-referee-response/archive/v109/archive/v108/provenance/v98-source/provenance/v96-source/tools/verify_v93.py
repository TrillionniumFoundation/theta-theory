#!/usr/bin/env python3
"""Exact source and claim preservation, followed by native full-source assembly."""
from __future__ import annotations
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
from check_v93 import require, checks
from verify_v74 import physical_tree
from assemble_v93 import assemble
PAPER=Path(__file__).resolve().parents[1]
BASE=PAPER.parent/'A2-DYN-v92-referee-response'
BASE_TREE='21b939b80d61a3ebfbb7620c95fb49dbee622dd5'
REVIEW='reviews/a2-dyn-v92-external-top4-review-2026-10-12/REFEREE_REPORT.md'
REVIEW_BLOB='b13997f04b117379c844f5ce237126cb9573990d'
NEW=['220_absolute_optical_traces.tex','221_signed_prefix_birth_balance.tex',
     '222_upper_birth_and_critical_gain.tex']
VARIANTS={'papers/A2-DYN-v88-referee-response':'af3d5707cc0ccad7fc20a6a67887cc0dc0e58ef6',
          'papers/A2-DYN-v88-main-preserved':'1c3e7c85c15f7265f66f8ee96ce6617d2f65488d'}
IGNORED={'build','evidence','__pycache__'}
REPLACED={'main.tex','supplement.tex','build.sh','SOURCE_MANIFEST.json','PUBLICATION_STATUS.json',
          'README.md','RESPONSE_TO_REFEREE.md','REFEREE_STATUS.md','PROOF_LEDGER.md','DEPENDENCY_MAP.md',
          'SPECIALIST_AUDIT.md','JOURNAL_ROUTE.md','VALIDATION.md','LOCAL_FULL_BUILD_RECORD.md'}

def git(*args: str) -> str:
    return subprocess.check_output(['git',*args],cwd=PAPER,text=True).strip()

def claims_at(packet: Path) -> dict:
    manifest=json.loads((packet/'SOURCE_MANIFEST.json').read_text())
    old=claims_at(packet/manifest['inherited_packet']) if manifest.get('inherited_packet') else {}
    return {**old,**manifest['claims']}

def source_check(local: bool) -> dict:
    require(physical_tree(BASE)==BASE_TREE,'frozen v92 paper bytes/modes')
    require(physical_tree(PAPER/'provenance/v92-source')==BASE_TREE,'full v92 snapshot')
    require((BASE/'main.tex').read_bytes()==(PAPER/'provenance/v92-main.tex').read_bytes(),'v92 article snapshot')
    manifest=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    require(manifest['revision']==93 and manifest['active_core_count']==222,'active revision/count')
    old=claims_at(BASE); active=manifest['claims']
    require(not {k for k,v in active.items() if k in old and old[k] is not v},'inherited flag altered')
    require(manifest['superseded_claims']=={},'unexpected claim supersession')
    resolved={**old,**active}
    for k in ['full_raw_return_LLT_proved','primary_referee_request_closed',
              'original_critical_residence_source_charge_zero_proved',
              'unconditional_upper_spike_persistence_proved',
              'ancestral_entrance_and_critical_gain_decay_proved',
              'uniform_single_sheet_modulus_summed_by_word_count',
              'independent_human_review','formal_proof_certificate']:
        require(resolved[k] is False,'unproved claim promoted: '+k)
    require(json.loads((PAPER/'PUBLICATION_STATUS.json').read_text())=={
        'inherited_packet':'provenance/v92-source','claims':active,'superseded_claims':{}},'status mismatch')
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
    require(preserved['core']==219 and len(list((PAPER/'core').glob('*.tex')))==222,'complete core count')
    if local:
        require(os.environ.get('GITHUB_ACTIONS')!='true','local mode forbidden in CI')
        head='local byte-pinned archive, not an exact remote checkout qualification'
    else:
        head=git('rev-parse','HEAD')
        require(git('rev-parse','HEAD:papers/A2-DYN-v92-referee-response')==BASE_TREE,'Git baseline')
        require(git('rev-parse','HEAD:'+REVIEW)==REVIEW_BLOB,'controlling report')
        for path,sha in VARIANTS.items():require(git('rev-parse','HEAD:'+path)==sha,'variant: '+path)
        if os.environ.get('GITHUB_ACTIONS')=='true':require(head==os.environ.get('GITHUB_SHA'),'wrong checkout SHA')
    main=(PAPER/'main.tex').read_text()
    for name in NEW:require(r'\input{core/'+name[:-4]+'}' in main,'new theorem omitted')
    assemble()
    hashes={str(x.relative_to(PAPER)):hashlib.sha256(x.read_bytes()).hexdigest()
        for x in sorted(PAPER.rglob('*')) if x.is_file() and not set(x.relative_to(PAPER).parts)&IGNORED}
    return {'checkout_sha':head,'baseline_tree':BASE_TREE,'review_blob':REVIEW_BLOB,
            'preserved':preserved,'resolved_claims':resolved,'source_sha256':hashes}

def main() -> None:
    args=sys.argv[1:];require(args in ([],['--local']),'unknown arguments')
    (PAPER/'build').mkdir(exist_ok=True);(PAPER/'evidence').mkdir(exist_ok=True)
    result={'revision':93,'finite_checks':checks(),'source':source_check(bool(args)),
            'formal_proof_certificate':False,'independent_human_review':False}
    for v in [*range(76,82),*range(83,93)]:
        result[f'inherited_v{v}_finite_checks']=importlib.import_module(f'check_v{v}').checks()
    from check_v75_geometry import checks as c75
    from verify_v74 import finite_checks as c74
    result['inherited_v75_finite_checks']=c75();result['inherited_v74_finite_checks']=c74()
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
