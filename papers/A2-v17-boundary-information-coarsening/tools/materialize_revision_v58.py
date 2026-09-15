#!/usr/bin/env python3
"""Integrate the admissible-block refinement without removing inherited proofs.

The readable new proof is an ordinary TeX input.  Every prescribed amendment
is checked against the source-matched v57 manifest and its original archived.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from source_provenance import blob_id, require, write_json
from materialize_revision_v57 import dependency_map as prior_dependency_map

P = Path(__file__).resolve().parents[1]
ARCHIVE = P / 'history/v57-review-baseline'
BASE = 'e39315c1fbb79ce71d1da91186a0d7e99a5ad8d6'
REVIEW = 'e14138660e716daf60471f3b98e8f1d30cb61a34'
INTRO = 'journal/00_principal_introduction_v56.tex'
SIGNED = 'article/23a_signed_endpoint_rigidity_v27.tex'
NEW = 'article/23a1_uniform_blocks_v58.tex'
ROUTES = 'journal/full_reference_routes_v56.tex'
BIBS = ('journal/references_v56.tex', 'v5/references_v43.tex')
CHANGES = ('main.tex', 'rigidity.tex', INTRO, SIGNED, ROUTES) + BIBS

BIB = r'''\bibitem{A2ReviewV57}
\emph{Independent referee-style report on A2, revision 57},
author-requested AI-assisted memorandum, September 15, 2026,
Section R57-M3. Repository
\texttt{Trillionnium\allowbreak Foundation/\allowbreak theta-theory},
\href{https://github.com/TrillionniumFoundation/theta-theory/commit/e14138660e716daf60471f3b98e8f1d30cb61a34}{frozen review memorandum}.
Cited for the admissible highest-degree block bounds; not a commissioned
journal report or an editorial decision.

'''


def once(text: str, before: str, after: str) -> str:
    require(text.count(before) == 1, 'Unexpected edit anchor: ' + before)
    return text.replace(before, after, 1)


def revised(name: str, text: str) -> str:
    if name == 'main.tex':
        require(text.count('A2 revision 57') == 2, 'Unexpected full version metadata')
        text = text.replace('A2 revision 57', 'A2 revision 58')
        return once(text,
            'actual-smooth finite-remainder argument precede the signed jet inverse.',
            'actual-smooth finite-remainder argument precede the signed jet inverse.\n'
            'The geometrically admissible highest-degree blocks and their inverses\n'
            'are bounded uniformly in order at a positive hyperbolic margin.')
    if name == 'rigidity.tex':
        text = once(once(text, 'A2 v57.', 'A2 v58.'), 'A2 revision 57', 'A2 revision 58')
        text = once(text,
            'justify the inverse for actual smooth boundaries, not only formal jets.',
            'justify the inverse for actual smooth boundaries, not only formal jets.\n'
            'The highest-degree blocks have order-uniform bounds and approach the\n'
            'identity exponentially under geometric admissibility.')
        return once(text,
            'separately from the reports\' nonbinding placement assessments.',
            'separately from the reports\' nonbinding placement assessments.\n'
            'The admissible highest-degree block estimates were communicated\n'
            'in~\\cite{A2ReviewV57}; their fixed-lower-jet and coefficient-space\n'
            'consequences are proved with them below.')
    if name == INTRO:
        text = once(text,
            '\\end{enumerate}\nThe local forward and finite-jet conclusions',
            r'''The highest-degree blocks have the additional bounds
\begin{equation}\label{eq:v58-headline-block-bounds}
 \begin{split}
 \max\{\|M_n\|_\infty,\|M_n^{-1}\|_\infty\}
       &\le \frac{3+t^6}{1-t^6},\\
 \max\{\|M_n-I\|_\infty,\|M_n^{-1}-I\|_\infty\}
       &\le \frac{4\vartheta^n}{1-t^6},
 \end{split}
 \qquad t=e^{-\gamma},\quad \vartheta=\frac{1+t^2}{2}<1.
\end{equation}
Here the norm is the maximum absolute row sum.  These bounds are uniform
in $n\ge3$, and uniformly over geometries with $\gamma\ge\gamma_*>0$.
They do not assert an order-uniform bound for the lower-jet remainders
or the complete nonlinear inverse.
\end{enumerate}
The local forward and finite-jet conclusions''')
        text = once(text,
            '\\eqref{eq:v56-local-block} and its inverse.\nAll of these supporting proofs are printed in the present article.\nThis theorem collects their conclusions and does not assert a further\ninfinite-order estimate.',
            '\\eqref{eq:v56-local-block} and its inverse.\n'
            'Proposition~\\ref{prop:v58-uniform-blocks} uses the positive-curvature\n'
            'constraint to prove \\eqref{eq:v58-headline-block-bounds}.\n'
            'All of these supporting proofs are printed in the present article.\n'
            'The block bounds are order-uniform; the nonlinear smooth estimates\n'
            'and reconstruction remain at each separately prescribed finite order.')
        text = once(text,
            'is substituted for the required nonlinear argument.',
            'is substituted for the required nonlinear argument.\n\n'
            'The geometric parameter restriction also identifies where an\n'
            'all-order conditioning issue can occur.  Positivity gives\n'
            '$\\mathfrak r_b e^{-\\gamma}<(1+e^{-2\\gamma})/2<1$.\n'
            'Thus the highest-degree response approaches the identity rather than\n'
            'becoming singular with order.  Proposition~\\ref{prop:v58-uniform-blocks}\n'
            'places this statement on coefficient spaces and for actual smooth\n'
            'pairs with common lower jets.  The remaining lower-degree couplings,\n'
            'smooth remainder bounds and analytic continuation are distinct parts\n'
            'of the full inverse; no estimate for them follows merely from the\n'
            'diagonal bounds.')
        return text
    if name == SIGNED:
        return text + '\n\\input{article/23a1_uniform_blocks_v58}\n'
    if name == ROUTES:
        return once(once(text, 'DEPENDENCY_MAP_V57.json', 'DEPENDENCY_MAP_V58.json'),
                    '{A2-v57}', '{A2-v58}')
    if name in BIBS:
        return once(text, r'\end{thebibliography}', BIB + r'\end{thebibliography}')
    raise RuntimeError('Unknown prescribed amendment: ' + name)


def dependency_map(root: Path = P) -> dict:
    data = prior_dependency_map(root)
    data.update(revision=58, baseline_source=BASE, review_head=REVIEW,
                supersedes='journal/DEPENDENCY_MAP_V57.json')
    return data


def materialize() -> dict:
    require((P/NEW).is_file(), 'Missing readable uniform-block proof')
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    manifest = ARCHIVE/'active-source-manifest.json'
    if not manifest.exists():
        source = P.parents[1]/'deliveries/a2-v57'/BASE/'active-source-manifest.json'
        require(source.is_file(), 'Missing source-matched v57 native manifest')
        manifest.write_bytes(source.read_bytes())
    old = {n: i for group in json.loads(manifest.read_text()).values() for n, i in group.items()}
    require(len(old) == 120, 'Unexpected v57 active source union')
    for name, info in old.items():
        archived = ARCHIVE/name
        source = archived if name in CHANGES and archived.exists() else P/name
        data = source.read_bytes()
        require(len(data) == info['bytes'] and hashlib.sha256(data).hexdigest() == info['sha256']
                and blob_id(data) == info['git_blob'], 'Unexpected baseline bytes: ' + name)
        if name in CHANGES:
            archived.parent.mkdir(parents=True, exist_ok=True)
            if not archived.exists():
                archived.write_bytes(data)
            expected = revised(name, data.decode())
            require((P/name).read_text() in (data.decode(), expected), 'Unexpected current edit: ' + name)
            (P/name).write_text(expected)
    write_json(P/'journal/DEPENDENCY_MAP_V58.json', dependency_map())
    return {'status': 'materialized', 'baseline_source': BASE, 'review_head': REVIEW,
            'amended_inputs': list(CHANGES), 'new_input': NEW,
            'inherited_active_inputs': len(old), 'mathematical_certification': False}


if __name__ == '__main__':
    print(json.dumps(materialize(), sort_keys=True, indent=2))
