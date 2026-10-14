#!/usr/bin/env python3
"""Pin v76, preserve every inherited source, and assemble the 173-core supplement."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from check_v77 import checks, require

PAPER=Path(__file__).resolve().parents[1]
BASE=PAPER.parent/'A2-DYN-v76-referee-response'
BASE_TREE='a33c145a96aba6fe6005796b554f0bfa2fd607f5'
REVIEW='reviews/a2-dyn-v76-external-top4-review-2026-10-11/REFEREE_REPORT.md'
REVIEW_BLOB='6857e4851ff12b7d0828f4eb661152e131fba091'
NEW=['174_canonical_endpoint_momentum_flow.tex','175_complete_angular_recoupling.tex',
     '176_angular_current_and_ordered_endpoint.tex']


def git(*args: str) -> str:
    return subprocess.check_output(['git',*args],cwd=PAPER,text=True).strip()


def assemble() -> None:
    import verify_v76 as inherited
    inherited.assemble()
    target=PAPER/'build/supplement-source.tex'
    master=target.read_text()
    old=(PAPER/'provenance/v76-main.tex').read_text()
    abstract=old.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
    body=old.split('\\maketitle',1)[1].split('\\input{journal-references}',1)[0]
    marker='\\part{Convex support and the complete physical Gauss trace}'
    require(master.count(marker)==1,'v76 supplement insertion boundary')
    insert=('\\part{Stopped physical transport and optical persistence}\n'
            '\\paragraph{Retained revision-76 abstract.}\n'+abstract+'\n'+body+'\n')
    master=master.replace(marker,insert+marker)
    master=master.replace('A2-DYN, revision 76; complete retained source through revision 75',
                          'A2-DYN, revision 77; complete retained source through revision 76')
    master=master.replace('\\begin{document}',
                          '\\providecommand{\\diver}{\\operatorname{div}}\n\\begin{document}',1)
    target.write_text(master)


def source_check(local: bool) -> dict:
    from verify_v74 import physical_tree
    require(physical_tree(BASE)==BASE_TREE,'frozen v76 paper bytes or file modes changed')
    manifest=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    require(manifest['revision']==77 and manifest['active_core_count']==176,'active revision and core count')
    if local:
        require(os.environ.get('GITHUB_ACTIONS')!='true','local mode forbidden in CI')
        head='local materialized archive plus new sources; not a qualified remote checkout'
    else:
        head=git('rev-parse','HEAD')
        require(git('rev-parse','HEAD:papers/A2-DYN-v76-referee-response')==BASE_TREE,'Git baseline tree')
        require(git('rev-parse','HEAD:'+REVIEW)==REVIEW_BLOB,'controlling review blob')
        if os.environ.get('GITHUB_ACTIONS')=='true':
            require(head==os.environ.get('GITHUB_SHA'),'checkout/qualification SHA mismatch')
    preserved={}
    for folder,pattern in [('core','*.tex'),('appendices','*.tex'),('tools','*.py')]:
        files=sorted((BASE/folder).rglob(pattern))
        for src in files:
            require(src.read_bytes()==(PAPER/src.relative_to(BASE)).read_bytes(),
                    'inherited source changed: '+str(src.relative_to(BASE)))
        preserved[folder]=len(files)
    require(preserved['core']==173,'baseline core count')
    require(len(list((PAPER/'core').glob('*.tex')))==176,'complete active core count')
    for name in ['references.tex','journal-references.tex']:
        require((BASE/name).read_bytes()==(PAPER/name).read_bytes(),'inherited bibliography changed')
    for snap in sorted((PAPER/'provenance').glob('v76-*')):
        require(snap.read_bytes()==(BASE/snap.name[4:]).read_bytes(),'v76 provenance changed: '+snap.name)
    old=json.loads((BASE/'SOURCE_MANIFEST.json').read_text())
    for key,value in old['claims'].items():
        require(manifest['claims'].get(key) is value,'inherited claim promoted or altered: '+key)
    for key in ['primary_referee_request_closed','full_raw_return_LLT_proved',
                'collision_uniform_angular_defect_bound_proved','independent_human_review','formal_proof_certificate']:
        require(manifest['claims'][key] is False,'unsupported claim promoted: '+key)
    require(json.loads((PAPER/'PUBLICATION_STATUS.json').read_text())==manifest['claims'],'stale publication status')
    for name in NEW:
        require((PAPER/'core'/name).is_file(),'missing new core')
        require(('\\input{core/'+name[:-4]+'}') in (PAPER/'main.tex').read_text(),'new core absent from journal')
    assemble()
    hashes={str(f.relative_to(PAPER)):hashlib.sha256(f.read_bytes()).hexdigest()
            for f in sorted(PAPER.rglob('*')) if f.is_file()
            and not set(f.relative_to(PAPER).parts)&{'build','evidence','__pycache__'}}
    return {'checkout_sha':head,'baseline_tree':BASE_TREE,
            'review_blob':REVIEW_BLOB if not local else 'not present in the v76 build archive; checked only by exact Git checkout',
            'preserved':preserved,'active_core_count':176,'source_sha256':hashes}


def main() -> None:
    args=sys.argv[1:];require(args in ([],['--local']),'unknown verifier arguments')
    (PAPER/'build').mkdir(exist_ok=True);(PAPER/'evidence').mkdir(exist_ok=True)
    from check_v76 import checks as v76_checks
    from check_v75_geometry import checks as v75_checks
    from verify_v74 import finite_checks as v74_checks
    result={'revision':77,'finite_checks':checks(),'inherited_v76_finite_checks':v76_checks(),
            'inherited_v75_finite_checks':v75_checks(),'inherited_v74_finite_checks':v74_checks(),
            'source':source_check(bool(args)),'formal_proof_certificate':False,'independent_human_review':False}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
