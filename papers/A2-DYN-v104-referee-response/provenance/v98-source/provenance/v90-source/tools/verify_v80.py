#!/usr/bin/env python3
"""Pin v79 and the controlling v79 review; preserve and assemble the full source."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from check_v77 import require
from check_v80 import checks
from verify_v74 import physical_tree, obj_hash

PAPER=Path(__file__).resolve().parents[1]
BASE=PAPER.parent/'A2-DYN-v79-referee-response'
BASE_TREE='6d41a1dbb1b0ed702e7445aaac476c87258b7ab8'
REVIEW='reviews/a2-dyn-v79-external-top4-review-2026-10-11/REFEREE_REPORT.md'
REVIEW_BLOB='dd7a2e7ee91757cdb253eaf8e605cd330ca11e3f'
NEW=['183_homogeneous_incidence_localization.tex', '184_singular_optical_transport.tex', '185_common_coarea_and_remaining_boundary.tex']


def git(*args: str) -> str:
    return subprocess.check_output(['git',*args],cwd=PAPER,text=True).strip()


def assemble() -> None:
    import re
    import verify_v79 as inherited
    inherited.assemble()
    target=PAPER/'build/supplement-source.tex'
    master=target.read_text()
    old=(PAPER/'provenance/v79-main.tex').read_text()
    abstract=old.split(r'\begin{abstract}',1)[1].split(r'\end{abstract}',1)[0]
    body=old.split(r'\maketitle',1)[1].split(r'\input{journal-references}',1)[0]
    # External supplement references become ordinary references in this
    # assembled copy only. The historical source snapshot is byte-identical.
    body=re.sub(r'\\eqref\{supp-([^}]+)\}',
                lambda m:r'\textup{(\ArchiveRef{'+m.group(1)+'})}',body)
    body=re.sub(r'\\ref\{supp-([^}]+)\}',
                lambda m:r'\ArchiveRef{'+m.group(1)+'}',body)
    marker=r'\part{Complete guard distortion and exact occupation currents}'
    require(master.count(marker)==1,'v79 supplement insertion boundary')
    prefix=r"""\part{Uniform cubic geometry and separated optical transport}
\begingroup
\let\ArchiveLabel\label
\let\ArchiveRef\ref
\renewcommand{\label}[1]{\ArchiveLabel{v79archive:#1}}
\renewcommand{\ref}[1]{\ArchiveRef{v79archive:#1}}
\makeatletter
\let\ltx@label\label
\makeatother
\paragraph{Retained revision-79 abstract.}
"""
    master=master.replace(marker,prefix+abstract+'\n'+body+'\n\\endgroup\n'+marker)
    master=master.replace('A2-DYN, revision 79; complete retained source through revision 78',
                          'A2-DYN, revision 80; complete retained source through revision 79')
    target.write_text(master)


def source_check(local: bool) -> dict:
    require(physical_tree(BASE)==BASE_TREE,'frozen v79 paper bytes or modes changed')
    manifest=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    require(manifest['revision']==80 and manifest['active_core_count']==185,'active revision/count')
    review_path=PAPER.parents[1]/REVIEW
    if local and not review_path.exists():
        review_status='not verified in local author archive; mandatory in exact Git mode'
    else:
        require(obj_hash('blob',review_path.read_bytes())==REVIEW_BLOB,'controlling review bytes')
        review_status='verified exact report bytes'
    if local:
        require(os.environ.get('GITHUB_ACTIONS')!='true','local mode forbidden in CI')
        head='local exact-baseline archive plus new sources; not remote checkout qualification'
    else:
        head=git('rev-parse','HEAD')
        require(git('rev-parse','HEAD:papers/A2-DYN-v79-referee-response')==BASE_TREE,'Git baseline tree')
        require(git('rev-parse','HEAD:'+REVIEW)==REVIEW_BLOB,'Git controlling review blob')
        if os.environ.get('GITHUB_ACTIONS')=='true':
            require(head==os.environ.get('GITHUB_SHA'),'checkout/qualification SHA mismatch')
    preserved={}
    for folder,pattern in [('core','*.tex'),('appendices','*.tex'),('tools','*.py'),('provenance','*')]:
        files=[f for f in sorted((BASE/folder).rglob(pattern)) if f.is_file()]
        for src in files:
            require(src.read_bytes()==(PAPER/src.relative_to(BASE)).read_bytes(),
                    'inherited source changed: '+str(src.relative_to(BASE)))
        preserved[folder]=len(files)
    require(preserved['core']==182,'baseline core count')
    require(len(list((PAPER/'core').glob('*.tex')))==185,'active core count')
    for name in ['references.tex','journal-references.tex']:
        require((BASE/name).read_bytes()==(PAPER/name).read_bytes(),'inherited bibliography changed')
    snapshots=[f for f in sorted(BASE.iterdir()) if f.is_file()]
    for src in snapshots:
        require(src.read_bytes()==(PAPER/'provenance'/('v79-'+src.name)).read_bytes(),
                'v79 top-level provenance changed: '+src.name)
    old=json.loads((BASE/'SOURCE_MANIFEST.json').read_text())
    for key,value in old['claims'].items():
        require(manifest['claims'].get(key) is value,'inherited claim altered: '+key)
    for key in ['primary_referee_request_closed','full_raw_return_LLT_proved',
                'complete_geometric_exit_volume_bound_proved',
                'complete_true_exit_roof_height_decay_proved',
                'complete_inverse_twist_roof_height_decay_proved',
                'uniform_surface_current_spectral_insertion_bound_proved',
                'independent_human_review','formal_proof_certificate']:
        require(manifest['claims'][key] is False,'unsupported claim promoted: '+key)
    require(json.loads((PAPER/'PUBLICATION_STATUS.json').read_text())==manifest['claims'],'stale status')
    for name in NEW:
        require((PAPER/'core'/name).is_file(),'missing new core')
        require((r'\input{core/'+name[:-4]+'}') in (PAPER/'main.tex').read_text(),'new core absent from journal')
    assemble()
    hashes={str(f.relative_to(PAPER)):hashlib.sha256(f.read_bytes()).hexdigest()
            for f in sorted(PAPER.rglob('*')) if f.is_file()
            and not set(f.relative_to(PAPER).parts)&{'build','evidence','__pycache__'}}
    return {'checkout_sha':head,'baseline_tree':BASE_TREE,'review_blob':REVIEW_BLOB,
            'preserved':preserved,'v79_top_level_snapshots':len(snapshots),
            'active_core_count':185,'review_verification':review_status,'source_sha256':hashes}


def main() -> None:
    args=sys.argv[1:];require(args in ([],['--local']),'unknown verifier arguments')
    (PAPER/'build').mkdir(exist_ok=True);(PAPER/'evidence').mkdir(exist_ok=True)
    from check_v79 import checks as v79_checks
    from check_v78 import checks as v78_checks
    from check_v77 import checks as v77_checks
    from check_v76 import checks as v76_checks
    from check_v75_geometry import checks as v75_checks
    from verify_v74 import finite_checks as v74_checks
    result={'revision':80,'finite_checks':checks(),'inherited_v79_finite_checks':v79_checks(),
            'inherited_v78_finite_checks':v78_checks(),
            'inherited_v77_finite_checks':v77_checks(),
            'inherited_v76_finite_checks':v76_checks(),'inherited_v75_finite_checks':v75_checks(),
            'inherited_v74_finite_checks':v74_checks(),'source':source_check(bool(args)),
            'formal_proof_certificate':False,'independent_human_review':False}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
