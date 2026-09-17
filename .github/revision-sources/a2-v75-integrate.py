#!/usr/bin/env python3
"""Materialize the v75 manuscript from pinned v74 sources; preserve every old file."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

BASE='c52fa361108a0f716d9e89017cd97eea71b0f3da'
PREFIX='papers/A2-v17-boundary-information-coarsening'
TREE='48787e35d236d4a896abe328d78eff0ef154fdee'

def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def sha(b): return hashlib.sha256(b).hexdigest()
def run(*args): return subprocess.check_output(args)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=Path(PREFIX));ap.add_argument('--baseline',type=Path)
    a=ap.parse_args();root=a.source; archive=root/'archive/v74-before-v75'
    if a.baseline:
        old={p.relative_to(a.baseline).as_posix():p.read_bytes() for p in a.baseline.rglob('*') if p.is_file()}
    else:
        need(run('git','rev-parse',f'{BASE}:{PREFIX}').decode().strip()==TREE,'Wrong baseline tree')
        entries=run('git','ls-tree','-rz',f'{BASE}:{PREFIX}').split(b'\0')
        old={}
        for ent in entries:
            if not ent:continue
            meta,path=ent.split(b'\t',1);mode,kind,blob=meta.decode().split()
            need(kind=='blob','Unexpected tree entry')
            old[path.decode()]=run('git','cat-file','blob',blob)
    need(len(old)==992,'Expected the complete 992-file v74 source tree')
    for name,data in old.items():
        need((root/name).read_bytes()==data,'Source diverged before integration: '+name)
    changed=[]
    def write(name,text):
        data=text.encode()
        if name in old and data!=old[name]:
            p=archive/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(old[name]);changed.append(name)
        p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    def text(name):return old[name].decode()
    # Exact source slices: complete core proofs, while the unsplit originals
    # remain active in main.tex and unchanged in the repository.
    splits={
      'article/10b_periodic_contact_inverse_v65.tex':('journal/core/periodic_contact_v75.tex','\\subsection{An inverse on a space of analytic germs}'),
      'article/10c_global_curvature_inverse_v66.tex':('journal/core/positive_curvature_v75.tex','\\subsection{Exact rigidity without a local branch choice}')}
    for src,(dst,marker) in splits.items():
        need(text(src).count(marker)==1,'Nonunique split marker');write(dst,text(src).split(marker)[0])
    # Retain the prior principal-only theorem and its complete explanation in
    # the active technical manuscript, not merely in a historical archive.
    legacy=text('journal/00_principal_introduction_v61.tex')
    legacy=legacy[legacy.index('\\subsection{The local relative and smooth inverse mechanism}'):legacy.index('\\subsection{The action as a nonlinear boundary coordinate}')]
    write('journal/legacy_local_mechanism_v75.tex','\\section{Alternating-channel formulation and relative comparison}\n\\label{sec:v56-introduction}\n'+legacy)
    graph=text('journal/02_graph_support_v56.tex').replace('eq:v46-graph-support','eq:v75-retained-graph-support').replace('part of the principal\narticle','part of this technical\nmanuscript')
    write('journal/legacy_graph_support_v75.tex',graph)
    m=text('main.tex').replace('A2 revision 74','A2 revision 75')
    m=m.replace('\\input{v5/references_v43}','\\input{journal/legacy_local_mechanism_v75}\n\\input{journal/legacy_graph_support_v75}\n\\input{v5/references_v43}')
    write('main.tex',m)
    # Concrete navigation correction in the retained full introduction.
    intro=text('article/00i_main_thesis_v70.tex')
    needle='The subsequent parts contain the finite-chain foundations'
    need(intro.count(needle)==1,'Missing roadmap anchor')
    intro=intro.replace(needle,'Section~\\ref{sec:v74-moments} reconstructs the limiting law from four\nfirst-moment profiles, retains the finite-flight rank defect, and proves\nthe charged one-dimensional derivative estimate and its budget balance.\nRemark~\\ref{rem:v75-conditioning} makes the fixed-gate conditioning\nrestriction explicit.\n\n'+needle)
    write('article/00i_main_thesis_v70.tex',intro)
    overview=text('article/00p_moment_overview_v74.tex')
    overview+='\nRemark~\\ref{rem:v75-conditioning} gives the explicit affine model\n$\\det H_f=p^2R^4/(9d^2)$ on $[-R,R]^2$.  It illustrates the dependence\non the fixed gate and obliquity; it is not an actual-table realization\nor a uniform estimate in a shrinking physical collar.\n'
    write('article/00p_moment_overview_v74.tex',overview)
    moments=text('article/10i_moment_reconstruction_v74.tex')
    marker='\\begin{corollary}[Moment determination of the local invariant]'
    need(moments.count(marker)==1,'Missing moment anchor')
    write('article/10i_moment_reconstruction_v74.tex',moments.replace(marker,'\\input{article/10j_conditioning_example_v75}\n\n'+marker))
    bib=r'''\bibitem{A2ReviewV74}
\emph{Independent referee report on A2, revision 74},
author-requested AI-assisted memorandum, September 17, 2026,
Section R74-M2. Repository
\texttt{Trillionnium\allowbreak Foundation/\allowbreak theta-theory},
\href{https://github.com/TrillionniumFoundation/theta-theory/blob/1ad828fd3cec7d39881fa4bb31d14423c4fd35da/reviews/a2-v74-independent-harsh-top4-2026-09-17/REFEREE_REPORT.md}{frozen memorandum}.
Cited for the affine gate-conditioning calculation, not a commissioned
journal decision or a mathematical certificate.
'''
    write('journal/review_reference_v75.tex',bib)
    for name in ('journal/references_v56.tex','v5/references_v43.tex'):
        write(name,text(name).replace('\\end{thebibliography}','\\input{journal/review_reference_v75}\n\\end{thebibliography}'))
    principal=r'''% A2 v75: the principal smooth mechanism and its observation consequences.
\input{preamble}
\externaldocument[F-]{main}[main.pdf]
\title[Boundary laws and smooth contact rigidity]{Boundary laws and smooth contact rigidity of periodic dispersing billiards}
\author{Qian Qi}
\date{September 17, 2026}
\subjclass[2020]{37D50, 37C30, 70H09, 53A04, 62G05}
\keywords{Dispersing billiards, relative boundary laws, smooth contact rigidity,
stationary envelope, finite preparations}
\hypersetup{pdftitle={Boundary laws and smooth contact rigidity of periodic dispersing billiards},
pdfauthor={Qian Qi},pdfsubject={A2 revision 75; principal journal article}}
\begin{document}
\input{journal/full_reference_routes_v75}
\begin{abstract}
\input{article/00s_principal_abstract_v75}
\end{abstract}
\maketitle
\setcounter{tocdepth}{1}
\tableofcontents
\input{article/00r_principal_introduction_v75}
\part{The relative law and the smooth inverse}
\input{article/10a_periodic_itinerary_relative_v64}
\input{journal/core/periodic_contact_v75}
\input{journal/core/positive_curvature_v75}
\input{article/10d_smooth_contact_rigidity_v68}
\input{article/10f_local_observation_comparison_v71}
\part{Consequences for the observation record}
\input{article/10g_uncalibrated_single_law_v72}
\input{article/10h_complete_record_v73}
\input{article/10i_moment_reconstruction_v74}
\subsection*{Acknowledgments}
The Riccati comparison leading to the positive quadratic inverse and the
affine moment-conditioning example were communicated in the author-requested
AI-assisted memoranda \cite{A2ReviewV65,A2ReviewV74}.  These attributions
concern the stated mathematical inputs, not journal endorsements.
\appendix
\renewcommand{\theHsection}{principal.appendix.\arabic{section}}
\input{article/10e_sampled_smooth_recovery_v69}
\input{journal/principal_references_v75}
\end{document}
'''
    write('rigidity.tex',principal)
    alias=text('journal/full_reference_routes_v56.tex')
    alias=alias[:alias.index('\\vFullAlias{sec:g-inverse}')]
    external=['prop:v66-finite-flight','thm:v14-intrinsic-density','thm:v26-density-inverse','thm:v4-factorization','thm:v65-analytic-inverse','thm:v66-global-rigidity']
    alias+='\n'.join('\\vFullAlias{'+lab+'}' for lab in external)+'\n\\makeatother\n'
    alias=alias.replace('% Full-manuscript aliases; their semantic roles are declared in DEPENDENCY_MAP_V60.json.\n% The acquisition theorem is an explicit input to a principal corollary, not a comparison.','% All six aliases are extension or specialization references; see DEPENDENCY_MAP_V75.json.')
    write('journal/full_reference_routes_v75.tex',alias)
    def expand(name,seen=None):
        seen=set() if seen is None else seen
        if name in seen:return ''
        seen.add(name);t=(root/name).read_text()
        def sub(match):
            q=match[1];q=q if q.endswith('.tex') else q+'.tex'
            return expand(q,seen) if (root/q).is_file() else match[0]
        return re.sub(r'\\input\{([^}]+)\}',sub,t)
    # Bibliography selection retains exact entries, not paraphrased citations.
    write('journal/principal_references_v75.tex','')
    keys=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])*\{([^}]+)\}',expand('rigidity.tex')):keys.update(group.split(','))
    allbib=expand('journal/references_v56.tex')
    entries=re.findall(r'(\\bibitem\{([^}]+)\}.*?)(?=\\bibitem|\\end\{thebibliography\})',allbib,re.S)
    need(keys <= {key for _,key in entries},'Missing bibliography key')
    write('journal/principal_references_v75.tex','\\begin{thebibliography}{99}\n'+''.join(body for body,key in entries if key in keys)+'\\end{thebibliography}\n')
    preservation={name:{'sha256':sha(data),'bytes':len(data),'archive':('archive/v74-before-v75/'+name if name in changed else None)} for name,data in old.items()}
    write('verification/v75-baseline-preservation.json',json.dumps({'base_commit':BASE,'base_tree':TREE,'files':preservation},indent=2,sort_keys=True)+'\n')
    labels=lambda t:set(re.findall(r'\\label\{([^}]+)\}',t))
    # Old roots are expanded from immutable originals, not the edited copies.
    def expandold(name,seen=None):
        seen=set() if seen is None else seen
        if name in seen:return ''
        seen.add(name);t=old[name].decode()
        def sub(m):
            q=m[1];q=q if q.endswith('.tex') else q+'.tex'
            return expandold(q,seen) if q in old else m[0]
        return re.sub(r'\\input\{([^}]+)\}',sub,t)
    before=set().union(*(labels(expandold(x)) for x in ('rigidity.tex','main.tex','two_collision.tex')))
    after=set().union(*(labels(expand(x)) for x in ('rigidity.tex','main.tex','two_collision.tex')))
    need(before<=after,'Lost active labels: '+repr(sorted(before-after)))
    write('verification/v75-active-labels.json',json.dumps({'inherited_labels':sorted(before),'baseline_count':len(before),'current_count':len(after),'missing':[]},indent=2)+'\n')
    dep={'central_proofs':'All included internally in rigidity.tex; no external proof premise.',
         'external_aliases':{x:'Extension or specialization comparison only; not a premise of the smooth theorem.' for x in external},
         'shared_core_slices':{s:{'principal':d,'split_marker':m,'full_original':s} for s,(d,m) in splits.items()},
         'technical_retention':'All prior source paths remain; changed originals are archived; prior principal-only statement/proof and graph-support lemma are active in main.tex.',
         'prior_active_labels':len(before),'current_active_labels':len(after)}
    write('DEPENDENCY_MAP_V75.json',json.dumps(dep,indent=2,sort_keys=True)+'\n')
    write('tools/build_revision_v75.py',"#!/usr/bin/env python3\nimport build_revision_v56 as engine\nengine.DIAGNOSTICS=(*engine.DIAGNOSTICS,'check_inherited_v73_on_baseline.py','check_revision_v74.py','check_revision_v75.py')\nif __name__=='__main__': engine.main()\n")
    write('tools/retain_native_v75.py',text('tools/retain_native_v74.py').replace('v74','v75'))
    print(json.dumps({'status':'materialized','baseline_files':len(old),'archived_originals':changed,'old_active_labels':len(before),'new_active_labels':len(after)},indent=2))
if __name__=='__main__':main()
