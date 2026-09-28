#!/usr/bin/env python3
"""Integrate the conditional observation inverse, preserving exact v59 inputs."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from source_provenance import blob_id, require, write_json
from materialize_revision_v59 import dependency_map as prior_dependency_map

P=Path(__file__).resolve().parents[1]
BASE='b56282439324435668ae80be90207fe7f5eebbf2'
REVIEW='f480cf1d099128c0c84df1ed149cff9b75e6ba2d'
ARCHIVE=P/'history/v59-review-baseline'
NEW='article/23a3_conditional_observation_inverse_v60.tex'
INTRO='journal/00_principal_introduction_v56.tex'
FULL_INTRO='article/00_structural_introduction_v48.tex'
SIGNED='article/23a_signed_endpoint_rigidity_v27.tex'
ROUTES='journal/full_reference_routes_v56.tex'
BIB='v5/references_v43.tex'
PBIB='journal/references_v56.tex'
CHANGES=('main.tex','rigidity.tex',INTRO,FULL_INTRO,SIGNED,ROUTES,BIB,PBIB)
OVERVIEW=r'''There is also a conditional conclusion in the real observation topology.
Theorem~\ref{thm:v60-real-observation-stability} fixes a local bounded
analytic neighborhood and recovers the complete contact germs on a
strictly smaller complex disc from uniform real endpoint-density error
$\epsilon$, with a bound $C(\epsilon_g+\epsilon^\vartheta)$,
$0<\vartheta<1$.  Curvatures may vary and are not separately supplied.
With a uniform first-order real density bound, total variation or
histogram errors give exponent $\vartheta/3$.  The proof combines
amplitude-free extraction on a real square, a displayed interpolation
estimate, and the complete analytic inverse on the inner disc.
It does not infer same-disc analytic smallness from real data: the
outer analytic prior, radius loss, density and anchor margins, and
local choice of inverse branch are explicit.  No global registration,
unknown-origin calibration, or preparation budget is a consequence of
this local estimate.  Proposition~\ref{prop:v60-contracted-criterion}
isolates the elementary functional-analytic criterion; the protected
half-lines and stationary envelope remain its billiard-specific inputs.
'''
BIB_ENTRY=r'''
\bibitem{A2ReviewV59}
\emph{Independent referee report on A2, revision 59},
author-requested AI-assisted memorandum, September 16, 2026,
Sections R59-M3 and R59-E2. Repository
\texttt{Trillionnium\allowbreak Foundation/\allowbreak theta-theory},
\href{https://github.com/TrillionniumFoundation/theta-theory/blob/f480cf1d099128c0c84df1ed149cff9b75e6ba2d/reviews/a2-v59-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md}{frozen memorandum}.
Cited for the qualitative Fredholm check and the suggestion to isolate
the contracted-evaluation structure; not a commissioned journal report.

'''

def once(text: str,before: str,after: str)->str:
    require(text.count(before)==1,'Unexpected edit anchor: '+before)
    return text.replace(before,after,1)

def revised(name: str,text: str)->str:
    if name in ('main.tex','rigidity.tex'):
        text=text.replace('A2 revision 59','A2 revision 60').replace('A2 v59.','A2 v60.')
        text=once(text,r'\date{September 15, 2026}',r'\date{September 16, 2026}')
        anchor=('an envelope representation controls its lower-degree couplings.' if name=='main.tex'
                else 'bounded-holomorphic norm, including all lower-degree couplings.')
        return once(text,anchor,anchor+'\nUnder a local analytic prior, real density errors give conditional\nH\\"older bounds for the complete contact germs on a smaller disc.')
    if name in (INTRO,FULL_INTRO):
        anchor='rate is part of this local analytic estimate.'
        return once(text,anchor,anchor+'\n\n'+OVERVIEW)
    if name==SIGNED:
        return text+'\n\\input{article/23a3_conditional_observation_inverse_v60}\n'
    if name==ROUTES:
        return once(once(text,'DEPENDENCY_MAP_V59.json','DEPENDENCY_MAP_V60.json'),'{A2-v59}','{A2-v60}')
    if name in (BIB,PBIB):
        extra=(r'\bibitem{Trefethen2020}'+'\n'+r'L.~N.~Trefethen, Quantifying the ill-conditioning of analytic continuation,'+'\n'+r'\emph{BIT Numerical Mathematics} \textbf{60} (2020), 901--915.'+'\n\n' if name==PBIB else '')
        return once(text,r'\end{thebibliography}',extra+BIB_ENTRY+r'\end{thebibliography}')
    raise RuntimeError('Unprescribed amendment: '+name)

def dependency_map(root: Path=P)->dict:
    out=prior_dependency_map(root)
    out.update(revision=60,baseline_source=BASE,review_head=REVIEW,
               supersedes='journal/DEPENDENCY_MAP_V59.json')
    return out

def materialize()->dict:
    require((P/NEW).is_file(),'Missing complete new shared proof')
    ARCHIVE.mkdir(parents=True,exist_ok=True)
    mp=ARCHIVE/'active-source-manifest.json'
    if not mp.exists():
        origin=P.parents[1]/'deliveries/a2-v59'/BASE/'active-source-manifest.json'
        require(origin.is_file(),'Missing source-matched v59 manifest')
        mp.write_bytes(origin.read_bytes())
    old={n:i for g in json.loads(mp.read_text()).values() for n,i in g.items()}
    require(len(old)==122,'Unexpected v59 active union')
    for name,info in old.items():
        archived=ARCHIVE/name
        data=(archived if name in CHANGES and archived.exists() else P/name).read_bytes()
        require(len(data)==info['bytes'] and hashlib.sha256(data).hexdigest()==info['sha256']
                and blob_id(data)==info['git_blob'],'Baseline identity: '+name)
        if name in CHANGES:
            archived.parent.mkdir(parents=True,exist_ok=True)
            if not archived.exists():archived.write_bytes(data)
            after=revised(name,data.decode())
            require((P/name).read_text() in (data.decode(),after),'Unexpected current amendment: '+name)
            (P/name).write_text(after)
    write_json(P/'journal/DEPENDENCY_MAP_V60.json',dependency_map())
    return {'status':'materialized','baseline_source':BASE,'review_head':REVIEW,
            'inherited_active_sources':len(old),'new_input':NEW,'amended_inputs':list(CHANGES),
            'mathematical_certification':False}

if __name__=='__main__':print(json.dumps(materialize(),indent=2,sort_keys=True))
