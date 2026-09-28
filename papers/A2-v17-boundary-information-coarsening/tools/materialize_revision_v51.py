#!/usr/bin/env python3
"""Materialize A2 v51 without removing an inherited mathematical input.

The new TeX modules are readable committed files. Exact originals of the
three amended inputs are checked against the frozen v50 active manifest.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from source_provenance import require

P=Path(__file__).resolve().parents[1]
ARCHIVE=P/'history/v50-review-baseline'
SOURCE_V50='49f73409b0cc6cb718fbbe48598fd7f5bc9ddca4'
REVIEW_V50='4b22b793cc2c05d3f48efb9a98dfd46cab003e5c'
CHANGES=('main.tex','article/00_structural_introduction_v48.tex','v5/references_v43.tex')
NEW_INPUTS=('article/00b_interaction_overview_v51.tex',
            'article/23p_uncentered_interaction_v51.tex')
ABSTRACT=r'''\begin{abstract}
We reconstruct the signed contact jets of a dispersing billiard channel
from its gap and two same-type conditional endpoint laws at one fixed
positive excess time.  A relative long-bridge limit on a flight-independent
collar retains nonlinear half-line actions despite exponentially small
successful-preparation probabilities.  Trace-class normalization and an
actual-smooth finite-remainder argument precede the signed jet inverse.
The geometric information lies in the interaction of the endpoints:
its mixed logarithmic derivative recovers unknown transverse contact
origins, and an anchored density ratio removes arbitrary positive separate
endpoint recording factors.  For noncircular analytic obstacles, finitely
many selected marked channels determine a finite set of complete periodic
tables, including their unknown marked Euclidean lattices.  Properly
asymmetric obstacles give uniqueness.  The same inverse is infinitesimally
rigid, including against the stated origin and recording nuisances;
finite scalar coordinates are obtained on immersed finite-dimensional
ideal-law models.  A noncircular example has exactly two realizations,
distinguished by one further marked gap.  Under separately quantified
analytic and observation bounds, finite transverse histograms give
full-table stability, and a same-flight physical pilot yields a charged
finite acquisition procedure.  The local experiments obtained by retaining
residual times, waiting counts or planar positions are determined separately.
\end{abstract}'''
BIB=r'''
\bibitem{HollandWang1987}
P. W. Holland and Y. J. Wang, \emph{Dependence function for continuous
bivariate densities}, Comm. Statist. Theory Methods \textbf{16} (1987),
no. 3, 863--876. \href{https://doi.org/10.1080/03610928708829408}{doi:10.1080/03610928708829408}.

\bibitem{Osius2009}
G. Osius, \emph{Asymptotic inference for semiparametric association models},
Ann. Statist. \textbf{37} (2009), no. 1, 459--489.
\href{https://doi.org/10.1214/07-AOS572}{doi:10.1214/07-AOS572}; arXiv:0903.0702v1.
'''


def once(text: str, old: str, new: str) -> str:
    require(text.count(old)==1,'Unexpected edit anchor: '+old)
    return text.replace(old,new,1)


def revised(name: str, text: str) -> str:
    if name==CHANGES[0]:
        text=text.replace('A2 revision 50','A2 revision 51')
        start=text.index(r'\begin{abstract}');end=text.index(r'\end{abstract}')+len(r'\end{abstract}')
        text=text[:start]+ABSTRACT+text[end:]
        text=once(text,'single-offset density inversion, contact rigidity,',
                  'single-offset density inversion, unknown transverse origins, endpoint association, contact rigidity,')
        return once(text,r'\input{article/23c_analytic_continuation_v23}',
                    '\\input{article/23c_analytic_continuation_v23}\n\\input{article/23p_uncentered_interaction_v51}')
    if name==CHANGES[1]:
        text=once(text,r'\newtheorem{structuraltheorem}{Theorem}',
                  '\\theoremstyle{plain}\n\\newtheorem{structuraltheorem}{Theorem}')
        anchor=r'\subsection{Proof of the geometric inverse}'
        return once(text,anchor,'\\input{article/00b_interaction_overview_v51}\n\n'+anchor)
    require(name==CHANGES[2],'Unexpected edited input')
    return once(text,r'\end{thebibliography}',BIB+'\n'+r'\end{thebibliography}')


def materialize() -> dict:
    for name in NEW_INPUTS:
        require((P/name).is_file(),'Missing new readable TeX module: '+name)
    ARCHIVE.mkdir(parents=True,exist_ok=True)
    manifest_path=ARCHIVE/'active-source-manifest.json'
    if not manifest_path.exists():
        original=P.parents[1]/'deliveries/a2-v50'/SOURCE_V50/'active-source-manifest.json'
        require(original.is_file(),'Missing frozen v50 active manifest')
        manifest_path.write_bytes(original.read_bytes())
    groups=json.loads(manifest_path.read_text())
    old={n:v for group in groups.values() for n,v in group.items()}
    require(len(old)==107,'Unexpected reviewed input count')
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
            require((P/name).read_text() in (raw.decode(),target),'Unexpected existing amendment: '+name)
            (P/name).write_text(target)
    return {'baseline_source':SOURCE_V50,'review_head':REVIEW_V50,
            'baseline_active_inputs':len(old),'exact_archived_originals':list(CHANGES),
            'new_inputs':list(NEW_INPUTS),'mathematical_certification':False}

if __name__=='__main__':
    print(json.dumps(materialize(),sort_keys=True,indent=2))
