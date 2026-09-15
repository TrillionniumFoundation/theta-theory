#!/usr/bin/env python3
"""Materialize v53 with exact v52 originals and additive entry/exposition edits."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from source_provenance import require

P=Path(__file__).resolve().parents[1]
ARCHIVE=P/'history/v52-review-baseline'
SOURCE_V52='9fd0c14c7b3fd816bdb9d7c3db0fdbae2104dcd6'
REVIEW_V52='28873f43ff25b2052afcce4df8c68907517e8b14'
CHANGES=('main.tex','article/00_structural_introduction_v48.tex','v5/references_v43.tex')
NEW_INPUTS=('article/18g_realized_window_information_v53.tex',)

OVERVIEW=r'''
A quantitative example ties these distinctions to an actual geometric
family.  The small-window benchmark in~\cite{A2ReviewV52} is realized in
Theorem~\ref{thm:v53-realized-experiment} by noncircular analytic obstacles
with fixed lattice and fixed channel gaps.  Separate recording profiles,
fixed as the half-width $h$ shrinks, preserve exact identification at each
$h>0$ while the one-record squared Hellinger distance between two fixed
shape alternatives is of order $h^8$.  For that two-point experiment the
successful-record scale $n\asymp h^{-8}$ is attainable: the critical
likelihood limit and a bounded-moment test are both explicit.  This is
not an optimal uniform estimator over the unrestricted nuisance class.
Corollary~\ref{cor:v53-finite-flight} transfers the experiment to actual
finite flights under $n\tau^J\to0$.  Its normalizing integrals also show
an additional recording fraction of order $h^2$, separate from the
original bridge rarity.  Thus the relative forward theorem controls a
joint flight/window/sample limit; the exact inverse and the acquisition
cost cannot be interchanged.  The table actions in this construction are
actual nonlinear actions, not stipulated quadratic functions.
'''

BIB=r'''
\bibitem{A2ReviewV52}
\emph{Independent referee-style report on A2, revision 52},
author-requested AI-assisted memorandum, September 15, 2026.
Repository \texttt{TrillionniumFoundation/theta-theory},
\href{https://github.com/TrillionniumFoundation/theta-theory/blob/28873f43ff25b2052afcce4df8c68907517e8b14/reviews/a2-v52-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md}{frozen review memorandum}.
Cited for the quadratic functional small-window information benchmark;
not a commissioned journal report or a mathematical certificate.
'''


def once(text: str, old: str, new: str) -> str:
    require(text.count(old)==1,'Unexpected edit anchor: '+old)
    return text.replace(old,new,1)


def revised(name: str, text: str) -> str:
    if name==CHANGES[0]:
        text=text.replace('A2 revision 52','A2 revision 53')
        text=once(text,'The local experiments obtained by retaining',
            'An explicit noncircular family realizes the small-window information\nloss, with an attained two-point testing scale and a joint finite-flight\ncomparison.  The local experiments obtained by retaining')
        text=once(text,r'\input{article/01b_observation_hierarchy_v29}',
            '\\input{article/01b_observation_hierarchy_v29}\n\\input{article/18g_realized_window_information_v53}')
        return once(text,'subsequent memorandum~\\cite{A2ReviewV51}.\n',
            'subsequent memorandum~\\cite{A2ReviewV51}.\nThe quadratic functional small-window benchmark was communicated in\n\\cite{A2ReviewV52}; Section~\\ref{sec:v53-window-information} supplies\nits actual-table realization, attainable two-point scale and finite-flight\ncomparison.\n')
    if name==CHANGES[1]:
        anchor='Finamore and Leguil~\\cite{FinamoreLeguil} study enriched marked length'
        return once(text,anchor,OVERVIEW+'\n'+anchor)
    require(name==CHANGES[2],'Unexpected amended file')
    return once(text,r'\end{thebibliography}',BIB+'\n'+r'\end{thebibliography}')


def materialize() -> dict:
    for name in NEW_INPUTS:
        require((P/name).is_file(),'Missing readable module: '+name)
    ARCHIVE.mkdir(parents=True,exist_ok=True)
    manifest=ARCHIVE/'active-source-manifest.json'
    if not manifest.exists():
        old=P.parents[1]/'deliveries/a2-v52'/SOURCE_V52/'active-source-manifest.json'
        require(old.is_file(),'Missing exact v52 native manifest')
        manifest.write_bytes(old.read_bytes())
    groups=json.loads(manifest.read_text())
    old={n:v for group in groups.values() for n,v in group.items()}
    require(len(old)==110,'Unexpected v52 active input count')
    for name,info in old.items():
        archive=ARCHIVE/name
        path=archive if name in CHANGES and archive.exists() else P/name
        raw=path.read_bytes()
        require(len(raw)==info['bytes'] and hashlib.sha256(raw).hexdigest()==info['sha256'],
                'Unexpected baseline: '+name)
        if name in CHANGES:
            archive.parent.mkdir(parents=True,exist_ok=True)
            if not archive.exists(): archive.write_bytes(raw)
            new=revised(name,raw.decode())
            require((P/name).read_text() in (raw.decode(),new),'Unexpected existing amendment: '+name)
            (P/name).write_text(new)
    return {'baseline_source':SOURCE_V52,'review_head':REVIEW_V52,
            'baseline_active_inputs':len(old),'archived_exact_originals':list(CHANGES),
            'new_inputs':list(NEW_INPUTS),'mathematical_certification':False}


if __name__=='__main__':
    print(json.dumps(materialize(),sort_keys=True,indent=2))
