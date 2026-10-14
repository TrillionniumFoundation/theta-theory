#!/usr/bin/env python3
"""Verify actual author source, full preservation and exact claim boundaries."""
from __future__ import annotations
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
from check_v100 import require
from check_v102 import checks
from verify_v74 import physical_tree
PAPER=Path(__file__).resolve().parents[1]
BASE=PAPER.parent/'A2-DYN-v100-uniform-capacity-referee-response'
BASE_TREE='7b8524304ab2eebc935e4c25f74b30d39f80c995'
REPORTS={
'reviews/a2-dyn-v101-submission-state-external-top4-review-2026-10-13/REFEREE_REPORT.md':'d64268f21394e8edf9e5b9bd2408ed94360966b6',
'reviews/a2-dyn-v100-uniform-capacity-external-top4-review-2026-10-13/REFEREE_REPORT.md':'b44278830cf52568a010a659dc8e38d348b5d1a4'}
VARIANTS={'papers/A2-DYN-v88-referee-response':'af3d5707cc0ccad7fc20a6a67887cc0dc0e58ef6',
'papers/A2-DYN-v88-main-preserved':'1c3e7c85c15f7265f66f8ee96ce6617d2f65488d'}
NEW=['244_barycentric_positive_trace_coarea.tex','245_transverse_clock_and_pointwise_trace_height.tex','246_transverse_certificates_and_scalar_schedule.tex']
IGNORED={'build','evidence','__pycache__'}
REPLACED={'main.tex','supplement.tex','build.sh','SOURCE_MANIFEST.json','PUBLICATION_STATUS.json',
'README.md','RESPONSE_TO_REFEREE.md','REFEREE_STATUS.md','PROOF_LEDGER.md','DEPENDENCY_MAP.md',
'SPECIALIST_AUDIT.md','JOURNAL_ROUTE.md','VALIDATION.md','LOCAL_FULL_BUILD_RECORD.md','OVERLAY_SHA256.json'}

def git(*args: str) -> str:
    return subprocess.check_output(['git',*args],cwd=PAPER,text=True).strip()

def main() -> None:
    args=sys.argv[1:];require(args in ([],['--local']),'unknown verifier arguments')
    local=bool(args);require(not local or os.environ.get('GITHUB_ACTIONS')!='true','local mode forbidden in CI')
    (PAPER/'build').mkdir(exist_ok=True);(PAPER/'evidence').mkdir(exist_ok=True)
    require(physical_tree(BASE)==BASE_TREE,'frozen actual v100 source changed')
    m=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    require(m['revision']==102 and m['active_core_count']==246,'wrong revision/count')
    require(m['revision_identifier']=='a2-dyn-v102-positive-paired-transverse-clock-2026-10-13','wrong identity')
    require(m['baseline_paper_tree']==BASE_TREE and m['report_blobs']==REPORTS,'source pins differ')
    receipt=json.loads((BASE/'BASELINE_RESOLVED_CLAIMS.json').read_text())
    old={**receipt['resolved_claims'],**json.loads((BASE/'SOURCE_MANIFEST.json').read_text())['claims']}
    if local:
        head='local byte-pinned complete source; not remote checkout qualification'
        report_check='connector-pinned reports; Git blob checks required remotely'
    else:
        head=git('rev-parse','HEAD')
        for path,sha in {'papers/A2-DYN-v100-uniform-capacity-referee-response':BASE_TREE,**REPORTS,**VARIANTS}.items():
            require(git('rev-parse','HEAD:'+path)==sha,'Git pin changed: '+path)
        if os.environ.get('GITHUB_ACTIONS')=='true':require(head==os.environ.get('GITHUB_SHA'),'checkout SHA mismatch')
        from verify_v97 import claims_at
        require(old==claims_at(BASE),'receipt disagrees with inherited repository claims')
        report_check='both frozen report blobs checked in Git'
    require(not {k for k,v in m['claims'].items() if k in old and old[k] is not v},'inherited claim promotion')
    require(m['superseded_claims']=={},'unexpected supersession')
    require(json.loads((PAPER/'PUBLICATION_STATUS.json').read_text())==
            {k:m[k] for k in ('inherited_packet','claims','superseded_claims')},'status mismatch')
    resolved={**old,**m['claims']}
    for key in ['positive_paired_short_trace_height_decay_proved','full_raw_return_LLT_proved',
                'primary_referee_request_closed','uniform_admission_of_all_physical_pairing_chambers_proved',
                'positive_transverse_failure_trace_height_decay_proved','independent_human_review','formal_proof_certificate']:
        require(resolved[key] is False,'unsupported claim: '+key)
    preserved={k:0 for k in ('core','tools','appendices','provenance','root')}
    roots=[f for f in BASE.iterdir() if f.is_file()]
    for f in roots:
        dst=PAPER/'provenance'/('v100-'+f.name)
        require(dst.read_bytes()==f.read_bytes(),'root snapshot: '+f.name)
        require(bool(dst.stat().st_mode&0o111)==bool(f.stat().st_mode&0o111),'snapshot mode: '+f.name)
    for f in BASE.rglob('*'):
        if not f.is_file():continue
        rel=f.relative_to(BASE)
        if set(rel.parts)&IGNORED or (len(rel.parts)==1 and rel.name in REPLACED):continue
        dst=PAPER/rel
        require(dst.is_file() and dst.read_bytes()==f.read_bytes(),'inherited bytes: '+str(rel))
        require(bool(dst.stat().st_mode&0o111)==bool(f.stat().st_mode&0o111),'inherited mode: '+str(rel))
        preserved[rel.parts[0] if rel.parts[0] in preserved else 'root']+=1
    require(preserved['core']==243 and len(list((PAPER/'core').glob('*.tex')))==246,'core coverage')
    main_tex=(PAPER/'main.tex').read_text()
    for n in NEW:require(r'\input{core/'+n[:-4]+'}' in main_tex,'missing article core: '+n)
    inventory=json.loads((PAPER/'OVERLAY_SHA256.json').read_text())
    for name,digest in inventory.items():
        require(hashlib.sha256((PAPER/name).read_bytes()).hexdigest()==digest,'authored hash: '+name)
    from assemble_v102 import assemble
    assemble()
    master=(PAPER/'build/supplement-source.tex').read_text()
    require(master.count('Superseded dyadic notation.')==1,'historical correction notice')
    require(master.count(r'\part{Uniform geometric capacity and the positive paired trace}')==1,'missing complete actual v100 article')
    hashes={str(f.relative_to(PAPER)):hashlib.sha256(f.read_bytes()).hexdigest()
            for f in sorted(PAPER.rglob('*')) if f.is_file() and not set(f.relative_to(PAPER).parts)&IGNORED}
    out={'revision':102,'finite_checks':checks(),'source':{'checkout_sha':head,'baseline_tree':BASE_TREE,
         'report_blobs':REPORTS,'report_verification':report_check,'preserved':preserved,'v100_root_snapshots':len(roots),
         'resolved_claims':resolved,'source_sha256':hashes},'formal_proof_certificate':False,'independent_human_review':False}
    for v in [*range(76,82),*range(83,101)]:
        out[f'inherited_v{v}_finite_checks']=importlib.import_module(f'check_v{v}').checks()
    from check_v75_geometry import checks as c75
    from verify_v74 import finite_checks as c74
    out['inherited_v75_finite_checks']=c75();out['inherited_v74_finite_checks']=c74()
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
