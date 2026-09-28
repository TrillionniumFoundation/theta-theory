#!/usr/bin/env python3
"""Materialize the complete v52 revision with exact, checked v51 originals.

No inherited statement or proof is removed. The new module is readable TeX;
this script applies only the explicit entry, exposition and attribution edits.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from source_provenance import require

P=Path(__file__).resolve().parents[1]
ARCHIVE=P/'history/v51-review-baseline'
SOURCE_V51='b9201bc272bc7ecbab1ad6a91fc844216685fadd'
REVIEW_V51='d0fd9a9b0d5cdd8004f42a7f109e39de50adda75'
CHANGES=('main.tex','article/00_structural_introduction_v48.tex',
         'article/00b_interaction_overview_v51.tex',
         'article/23p_uncentered_interaction_v51.tex','v5/references_v43.tex')
NEW_INPUTS=('article/23q_support_and_interior_windows_v52.tex',)

OVERVIEW=r'''
For the complete-cap observation in this statement, the origins can also
be recovered without a density derivative: the vertical and horizontal
fiber widths of the positive support have their unique maxima at the two
origins (Lemma~\ref{lem:v52-support-centering}).  Thus centering a complete
cap is not, by itself, a new geometric rigidity mechanism.  The benefit
of the interaction construction is its dependence on a fixed positive
interior rectangle.  Theorem~\ref{thm:v52-window-extraction} makes this
locality explicit: a known rectangular recording window containing both
unknown origins, compactly inside the positive cap, suffices even when
the cap boundary and discarded mass are not observed.  Its positive
support is the same window for every admitted law.  The signed action
is nevertheless recovered from the interior density, and
Corollary~\ref{cor:v52-window-geometry} gives exactly the same analytic
table fiber and projected derivative kernel.  The visibility of the two
origins remains a hypothesis; there is no unmarked search for that window.

The separate-factor cancellation is already the calculation of
Theorem~\ref{thm:v26-density-inverse}, with no equality of the two factors
needed.  The interior extension uses this algebra rather than inventing
another association invariant.  Its regularity is the local
$C^{m+3}$-to-$C^m$ estimate of Proposition~\ref{prop:v51-stability},
now on a window not reaching the cap boundary.  A complete support can
center the law but need not determine its action; the functional
comparison in Proposition~\ref{prop:v27-support-gauge} isolates that
distinction.  None of these statements provides a total-variation
estimate or a uniform preparation bound for an unconstrained recording
class.
'''

SYNTHESIS=r'''
The common object in these three parts is the unnormalized relative
boundary measure.  For a same-type law, suppressing the channel index,
write
\begin{equation}\label{eq:v52-common-measure}
 \nu_{b,d}(\dd u\,\dd v\,\dd r)
 =B_b(u)B_b(v)\mathbf1_{\{0<r<d-S_b(u)-S_b(v)\}}
                         \dd u\,\dd v\,\dd r.
\end{equation}
Its normalization gives the endpoint--residual-time law; integration
in $r$ gives the endpoint law.  The preparation probability retains
information from the normalization and the exponentially small reference
factor that conditional normalization removes.  The relative estimates
of Theorems~\ref{thm:v4-factorization} and~\ref{thm:v4-law} justify these
operations for the actual billiard, not just for an abstract family of
cap densities.  Part I inverts the geometric interaction in this measure.
Part II studies the different likelihoods obtained by retaining or
forgetting components of the physical record.  Part III controls the
passage from finite acquired records to the ideal law and then through
the deterministic inverse.  The same forward construction is required
at all three interfaces; the inverse alone does not supply their
statistical hypotheses.

These links specify the scope of the combined treatment.  Exact
function-valued reconstruction, local interior smooth inversion,
model-local finite scalar coordinates and charged finite-sample
acquisition are not equivalent experiments.  Separate endpoint
reweighting preserves the geometric invariant, but generally changes
the likelihood and probability of recording a bridge.  Cropping to an
interior window preserves the contact-germ inverse under its visibility
conditions, but does not provide the unrecorded mass.  In particular,
multiplying both recording probabilities by $\varepsilon$ keeps the
conditional law fixed while multiplying the recorded-success probability
by $\varepsilon^2$.  The success lower bound and density margins used
in Part III are therefore additional premises, not consequences of
Theorem~\ref{thm:v51-main} or its window extension.  Likewise, the finite
scalar coordinate theorem concerns a stipulated finite-dimensional
ideal-law model, not arbitrary infinite-dimensional efficiency profiles.
The structural contribution is the nonlinear relative/smooth inverse;
the other parts establish, for their stated records, what is lost by
coarsening and what further control permits its acquisition.
'''

BIB=r'''
\bibitem{A2ReviewV51}
\emph{Independent referee-style report on A2, revision 51},
author-requested AI-assisted memorandum, September 15, 2026.
Repository \texttt{TrillionniumFoundation/theta-theory},
\href{https://github.com/TrillionniumFoundation/theta-theory/blob/d0fd9a9b0d5cdd8004f42a7f109e39de50adda75/reviews/a2-v51-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md}{frozen review memorandum}.
Cited for the support-width centering observation; not a commissioned
journal report or a mathematical certificate.
'''


def once(text: str, old: str, new: str) -> str:
    require(text.count(old)==1,'Unexpected edit anchor: '+old)
    return text.replace(old,new,1)


def revised(name: str, text: str) -> str:
    if name==CHANGES[0]:
        text=text.replace('A2 revision 51','A2 revision 52')
        old='''The geometric information lies in the interaction of the endpoints:
its mixed logarithmic derivative recovers unknown transverse contact
origins, and an anchored density ratio removes arbitrary positive separate
endpoint recording factors.'''
        new='''The geometric information lies in the interaction of the endpoints.
The complete support already locates unknown numerical origins; an interior
mixed logarithmic derivative also locates them without an observed cap
boundary.  On a positive recording window containing the origins, an
anchored density ratio removes arbitrary positive separate endpoint factors
and recovers the signed action germ.'''
        text=once(text,old,new)
        text=once(text,r'\input{article/23p_uncentered_interaction_v51}',
                  '\\input{article/23p_uncentered_interaction_v51}\n\\input{article/23q_support_and_interior_windows_v52}')
        return once(text,'certificates.\n\n\\appendix',
              'certificates.\nThe support-width centering comparison in\nLemma~\\ref{lem:v52-support-centering} was communicated in the\nsubsequent memorandum~\\cite{A2ReviewV51}.\n\n\\appendix')
    if name==CHANGES[1]:
        anchor='Finamore and Leguil~\\cite{FinamoreLeguil} study enriched marked length'
        return once(text,anchor,SYNTHESIS+'\n'+anchor)
    if name==CHANGES[2]:
        return text+OVERVIEW
    if name==CHANGES[3]:
        anchor=r'\subsection{Recovery of the action, with separate endpoint weights}'
        addition=r'''For the complete positive cap, there is also a support-only centering
method: its fiber widths attain their unique maxima at the two origins.
Lemma~\ref{lem:v52-support-centering} gives that comparison.  The
interaction proof above is useful because its simple roots, and the
finite-smooth estimate below, are confined to a positive interior rectangle.
Theorems~\ref{thm:v52-window-extraction} and
Corollary~\ref{cor:v52-window-geometry} state what survives when only
such an interior window is recorded.

'''
        addition=addition.replace('Theorems~','Theorem~')
        return once(text,anchor,addition+anchor)
    require(name==CHANGES[4],'Unexpected amended file')
    return once(text,r'\end{thebibliography}',BIB+'\n'+r'\end{thebibliography}')


def materialize() -> dict:
    for name in NEW_INPUTS:
        require((P/name).is_file(),'Missing readable new module: '+name)
    ARCHIVE.mkdir(parents=True,exist_ok=True)
    manifest_path=ARCHIVE/'active-source-manifest.json'
    if not manifest_path.exists():
        original=P.parents[1]/'deliveries/a2-v51'/SOURCE_V51/'active-source-manifest.json'
        require(original.is_file(),'Missing frozen v51 active manifest')
        manifest_path.write_bytes(original.read_bytes())
    groups=json.loads(manifest_path.read_text())
    old={n:v for group in groups.values() for n,v in group.items()}
    require(len(old)==109,'Unexpected reviewed input count')
    for name,info in old.items():
        archive=ARCHIVE/name
        path=archive if name in CHANGES and archive.exists() else P/name
        raw=path.read_bytes()
        require(len(raw)==info['bytes'] and hashlib.sha256(raw).hexdigest()==info['sha256'],
                'Unexpected baseline bytes: '+name)
        if name in CHANGES:
            archive.parent.mkdir(parents=True,exist_ok=True)
            if not archive.exists():archive.write_bytes(raw)
            target=revised(name,raw.decode())
            require((P/name).read_text() in (raw.decode(),target),'Unexpected amendment: '+name)
            (P/name).write_text(target)
    return {'baseline_source':SOURCE_V51,'review_head':REVIEW_V51,
            'baseline_active_inputs':len(old),'exact_archived_originals':list(CHANGES),
            'new_inputs':list(NEW_INPUTS),'mathematical_certification':False}

if __name__=='__main__':
    print(json.dumps(materialize(),sort_keys=True,indent=2))
