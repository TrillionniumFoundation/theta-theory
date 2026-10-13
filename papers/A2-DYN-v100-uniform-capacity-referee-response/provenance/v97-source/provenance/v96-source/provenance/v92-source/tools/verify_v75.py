#!/usr/bin/env python3
"""Source pinning, finite checks and assembly; no continuum proof certificate."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import verify_v74 as inherited
from check_v75_geometry import checks

PAPER=Path(__file__).resolve().parents[1]
BASE=PAPER.parent/'A2-DYN-v74-referee-response'
BASE_TREE='02bac634205e7f776793ba330c98c11039fd71d5'
REVIEW_PATH='reviews/a2-dyn-v74-external-top4-review-2026-10-11/REFEREE_REPORT.md'
REVIEW_BLOB='83ab4fa82c4f5be6ee930865c87633ef5d94717f'
require=inherited.require


def git(*args: str) -> str:
    return subprocess.check_output(['git',*args],cwd=PAPER,text=True).strip()


def status_texts(m: dict) -> dict[str,str]:
    keys=('revision','active_directory','branches','full_raw_return_LLT_proved',
          'pointwise_roof_density_LLT_proved','lorentz_level_matched_tail_decay_proved',
          'collision_uniform_wordwise_gauss_coarea_proved',
          'collision_uniform_weighted_word_trace_decay_proved','primary_referee_request_closed',
          'independent_human_review','formal_proof_certificate')
    status={k:m[k] for k in keys}; status['authority']='SOURCE_MANIFEST.json'
    return {
      'PUBLICATION_STATUS.json':json.dumps(status,indent=2)+'\n',
      'REFEREE_STATUS.md':'# A2-DYN revision 75: referee status\n\nAuthority: `SOURCE_MANIFEST.json`.\n\nThe new physical-word convex-support, uniform curvature and Gauss coarea theorems are submitted for review. The complete collision-normalized weighted trace estimate remains unproved. The original pointwise raw theorem and its unconditional normalizations are not marked proved. No independent human specialist audit, journal acceptance or formal certificate is claimed. See `RESPONSE_TO_REFEREE.md` for every v74 request.\n',
      'VALIDATION.md':'# A2-DYN revision 75: validation contract\n\nRun `bash build.sh` in an exact Git checkout. `bash build.sh --local` is permitted only outside CI for a materialized source copy and does not certify a remote checkout. The verifier pins the v74 paper tree and controlling report, preserves 167 inherited cores, all inherited Python sources, appendices and bibliographies, and checks generated status files without mutation.\n\nThe build runs exact rational identities, deterministic physical billiard fixtures, all v74 finite fixtures and six inherited checks in addition to normal/optimized agreement. Native TeX must stabilize without warnings. Actual recorder coverage must include 3 journal and 167 supplement modules; page geometry is checked for both PDFs. Workflow: `.github/workflows/a2-dyn-v75-qualification.yml`.\n\nThese checks certify neither the continuum proofs nor the missing weighted dynamical estimate. Evidence is generated for the exact checkout, not copied from a preceding revision. Current local evidence is described in `LOCAL_FULL_BUILD_RECORD.md`.\n'
    }


def assemble() -> None:
    build=PAPER/'build'; build.mkdir(exist_ok=True)
    v72=(PAPER/'provenance/v72-main.tex').read_text()
    marker='\\part{The complete physical current and source recovery}'
    require(v72.count(marker)==1,'v72 assembly boundary')
    before,after=v72.split(marker)
    body=marker+after.split('\\input{references}',1)[0]
    abstract=before.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
    opening=before.split('\\maketitle',1)[1]
    front=('\\section{The retained opening of revision 72}\n\\label{app:v73-retained-front}\n'
      'The following opening is retained as a historical statement of the preceding route. '
      'Its finite-measure qualification is superseded by Theorem~\\ref{thm:v73-full-source-bv}; '
      'its collision-uniform qualification is not. In its source notation, $e_{70}$ means '
      'first clearance outside the selected disks, with incidence separate.\n'
      '\\paragraph{Preceding abstract.}\n'+abstract+'\n'+opening)
    (build/'v72-body.tex').write_text(body); (build/'v72-frontmatter.tex').write_text(front)
    v74=(PAPER/'provenance/v74-main.tex').read_text()
    a74=v74.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
    b74=v74.split('\\maketitle',1)[1].split('\\input{journal-references}',1)[0]
    insert=('\\part{The retained complete source and short excursions}\n'
            '\\paragraph{Retained revision-74 abstract.}\n'+a74+'\n'+b74+'\n')
    master=(PAPER/'provenance/v73-main.tex').read_text()
    marker='\\part{Finite physical currents and the pointwise error}'
    require(master.count(marker)==1,'v73 assembly boundary')
    master=master.replace(marker,insert+marker)
    old='\\title[Collision records and raw local inversion]{Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas}'
    require(master.count(old)==1,'supplement title boundary')
    master=master.replace(old,'\\title[Technical supplement]{Technical supplement to Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas}')
    master=master.replace('October 11, 2026. A2-DYN, revision 73',
              'October 11, 2026. A2-DYN, revision 75; retained revision-73 and revision-74 sources')
    master=master.replace('\\begin{document}',
      '\\theoremstyle{definition}\\newtheorem{inputstatement}[theorem]{Input statement}\n'
      '\\newcommand{\\esssup}{\\operatorname*{ess\\,sup}}\n\\begin{document}',1)
    (build/'supplement-source.tex').write_text(master)


def source_check(local: bool) -> dict:
    require(inherited.physical_tree(BASE)==BASE_TREE,'frozen v74 paper bytes or modes changed')
    if local:
        require(os.environ.get('GITHUB_ACTIONS')!='true','local mode forbidden in CI')
        head='materialized source copy; not a remote-checkout claim'
    else:
        head=git('rev-parse','HEAD')
        require(git('rev-parse','HEAD:papers/A2-DYN-v74-referee-response')==BASE_TREE,'Git v74 tree changed')
        require(git('rev-parse','HEAD:'+REVIEW_PATH)==REVIEW_BLOB,'controlling report changed')
        if os.environ.get('GITHUB_ACTIONS')=='true':
            require(head==os.environ.get('GITHUB_SHA'),'qualification SHA mismatch')
    preserved={}
    for folder,pattern in [('core','*.tex'),('appendices','*.tex'),('tools','*.py')]:
        files=list((BASE/folder).rglob(pattern))
        for src in files:
            require(src.read_bytes()==(PAPER/src.relative_to(BASE)).read_bytes(),
                    'inherited source changed: '+str(src.relative_to(BASE)))
        preserved[folder]=len(files)
    require(preserved['core']==167 and len(list((PAPER/'core').glob('*.tex')))==170,'core counts')
    for name in ('references.tex','journal-references.tex'):
        require((PAPER/name).read_bytes()==(BASE/name).read_bytes(),'bibliography changed: '+name)
    old=json.loads((BASE/'SOURCE_MANIFEST.json').read_text())
    active=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
    for key,value in old.items():
        if isinstance(value,bool): require(active.get(key) is value,'inherited claim flag changed: '+key)
    require(active['revision']==75 and active['active_core_count']==170,'active manifest')
    require(active['primary_referee_request_closed'] is False,'physical tail promoted to theorem')
    for snapshot in sorted((PAPER/'provenance').glob('v74-*')):
        original=BASE/snapshot.name[len('v74-'):]
        require(original.is_file() and snapshot.read_bytes()==original.read_bytes(),
                'v74 provenance mismatch: '+snapshot.name)
    for name,text in status_texts(active).items():
        require((PAPER/name).read_text()==text,'stale generated status: '+name)
    assemble()
    hashes={str(f.relative_to(PAPER)):hashlib.sha256(f.read_bytes()).hexdigest()
            for f in sorted(PAPER.rglob('*')) if f.is_file()
            and not set(f.relative_to(PAPER).parts)&{'build','evidence','__pycache__'}}
    return dict(checkout_sha=head,baseline_tree=BASE_TREE,controlling_review_blob=REVIEW_BLOB,
                preserved=preserved,active_core_count=170,source_sha256=hashes)


def main() -> None:
    args=sys.argv[1:]; require(args in ([],['--local'],['--write-status']),'unknown arguments')
    if args==['--write-status']:
        require(os.environ.get('GITHUB_ACTIONS')!='true','status mutation forbidden in CI')
        m=json.loads((PAPER/'SOURCE_MANIFEST.json').read_text())
        for name,text in status_texts(m).items(): (PAPER/name).write_text(text)
        return
    result=dict(revision=75,scope='source identity, finite fixtures and deterministic assembly only',
                formal_proof_certificate=False,independent_human_review=False,
                finite_checks=checks(),inherited_v74_finite_checks=inherited.finite_checks(),
                source=source_check(args==['--local']))
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__': main()
