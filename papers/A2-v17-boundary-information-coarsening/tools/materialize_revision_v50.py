#!/usr/bin/env python3
"""Add the v50 mechanism exposition and realized two-branch example.

The complete v49 active graph is retained. Three originals are archived;
all changes are prescribed and all old theorem/proof bodies stay active.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from source_provenance import require

P=Path(__file__).resolve().parents[1]
ARCHIVE=P/'history/v49-review-baseline'
ASSETS=P/'tools/revision_v50'
SOURCE_V49='a003c1c69585f09f0b8fcc9fe03eb330cd6d57b7'
REVIEW_V49='5051b7789a424656a558179922607d8b55061b28'
CHANGES=('main.tex','article/00_structural_introduction_v48.tex','v5/references_v43.tex')
NEW_INPUTS=('article/23o_two_branch_example_v50.tex',)


def once(text: str, before: str, after: str) -> str:
    require(text.count(before)==1,'Unexpected edit anchor: '+before)
    return text.replace(before,after,1)


def revised(name: str, text: str) -> str:
    if name==CHANGES[1]:
        anchor='For a same-type law, on a positive interior square,'
        text=once(text,anchor,(ASSETS/'relative_core.tex').read_text()+anchor)
        anchor='Analytic continuation now gives complete channel-frame obstacle images.'
        text=once(text,anchor,(ASSETS/'smooth_core.tex').read_text()+anchor)
        anchor='''exhibits the distinction for this selected-channel design.'''
        text=once(text,anchor,anchor+r'''
Proposition~\ref{prop:v50-two-table} exhibits a different phenomenon:
a noncircular $C_4$-symmetric obstacle with exactly two realizations of
one two-channel datum and distinct marked Gram forms.  This is finite
global ambiguity despite an injective local derivative, not a circular
exception to the theorem.  Proposition~\ref{prop:v50-extra-gap} proves
that one further marked clear-channel gap distinguishes those two
realizations.  Its clearance is proved for the actual closest segment,
not assumed from the direction of its center displacement.''')
        return text
    if name==CHANGES[2]:
        entry=r'''
\bibitem{A2ReviewV49}
Independent AI-assisted referee-style memorandum,
\emph{A2 revision 49}, September 15, 2026, Section 4,
repository \texttt{Trillionnium\allowbreak Foundation/\allowbreak theta-theory},
review commit
\href{https://github.com/TrillionniumFoundation/theta-theory/commit/5051b7789a424656a558179922607d8b55061b28}{\texttt{5051b778\allowbreak 9a424656\allowbreak a5581799\allowbreak 22607d8b\allowbreak 55061b28}}.
An author-requested memorandum, not a commissioned journal report.

'''
        return once(text,r'\end{thebibliography}',entry+r'\end{thebibliography}')
    require(name=='main.tex','Unknown amended input')
    text=text.replace('A2 revision 49','A2 revision 50')
    text=once(text,r'\date{September 14, 2026}',r'\date{September 15, 2026}')
    text=once(text,'with finite symmetries we enumerate the finite reconstruction branches.',
        'with finite symmetries we enumerate the finite reconstruction branches.\nA noncircular example has exactly two branches, distinguished by one\nadditional marked channel gap.')
    text=once(text,r'\input{article/23n_finite_symmetry_v49}',
        r'\input{article/23n_finite_symmetry_v49}'+'\n'+r'\input{article/23o_two_branch_example_v50}')
    anchor='here from that distinction and the intrinsic cochain inverse.'
    return once(text,anchor,anchor+r'''
The noncircular two-table construction in
Proposition~\ref{prop:v50-two-table} was suggested in the subsequent
memorandum~\cite{A2ReviewV49}.  The additional-channel separation in
Proposition~\ref{prop:v50-extra-gap} is proved here.  These memoranda
are cited for attribution, not as journal endorsements or proof
certificates.''')


def materialize() -> dict:
    for name in NEW_INPUTS:
        require((P/name).is_file(),'Missing readable mathematical input: '+name)
    ARCHIVE.mkdir(parents=True,exist_ok=True)
    manifest=ARCHIVE/'active-source-manifest.json'
    if not manifest.exists():
        native=P.parents[1]/'deliveries/a2-v49'/SOURCE_V49/'active-source-manifest.json'
        require(native.is_file(),'Missing source-matched v49 native manifest')
        manifest.write_bytes(native.read_bytes())
    groups=json.loads(manifest.read_text())
    old={n:v for group in groups.values() for n,v in group.items()}
    require(len(old)==106,'Wrong baseline active input count')
    for name,info in old.items():
        archived=ARCHIVE/name
        path=archived if name in CHANGES and archived.exists() else P/name
        raw=path.read_bytes()
        require(len(raw)==info['bytes'] and hashlib.sha256(raw).hexdigest()==info['sha256'],
                'Unexpected baseline source: '+name)
        if name in CHANGES:
            if not archived.exists():
                archived.parent.mkdir(parents=True,exist_ok=True)
                archived.write_bytes(raw)
            expected=revised(name,raw.decode())
            require((P/name).read_text() in (raw.decode(),expected),'Unrecognized existing edit: '+name)
            (P/name).write_text(expected)
    return {'review_head':REVIEW_V49,'reviewed_mathematical_source':SOURCE_V49,
            'baseline_inputs':len(old),'archived_exact_originals':list(CHANGES),
            'new_inputs':list(NEW_INPUTS),'mathematical_certification':False}

if __name__=='__main__':
    print(json.dumps(materialize(),sort_keys=True,indent=2))
