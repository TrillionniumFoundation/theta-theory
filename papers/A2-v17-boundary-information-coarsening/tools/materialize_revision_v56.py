#!/usr/bin/env python3
"""Create a dependency-focused journal entry while retaining the complete A2 corpus.

All inherited mathematical inputs stay byte-identical; only main.tex metadata is
amended. Generated journal navigation and bibliography are ordinary committed TeX.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
from source_provenance import graph, require, write_json
P=Path(__file__).resolve().parents[1]
ARCHIVE=P/'history/v55-review-baseline'
SOURCE_V55='3903f5b8a5ffb0d0a69065b1d303c247c06ebf69'
REVIEW_V55='5015444dc016dec38a7d0f0130b818823bbabd4e'
NEW_INTRO='journal/00_principal_introduction_v56.tex'
LOCAL_CONVERSION='journal/02_graph_support_v56.tex'

def replace_once(text,before,after):
    require(text.count(before)==1,'Unexpected anchor: '+before)
    return text.replace(before,after,1)

def amended_main(text):
    return text.replace('A2 revision 55','A2 revision 56').replace(
        r'\title[Boundary laws and periodic rigidity]{Boundary laws and rigidity of periodic dispersing billiards}',
        r'\title[Boundary laws: full technical manuscript]{Boundary laws and rigidity of periodic dispersing billiards\\Full technical manuscript}')

def materialize():
    ARCHIVE.mkdir(parents=True,exist_ok=True)
    manifest_path=ARCHIVE/'active-source-manifest.json'
    if not manifest_path.exists():
        origin=P.parents[1]/'deliveries/a2-v55'/SOURCE_V55/'active-source-manifest.json'
        require(origin.is_file(),'Missing exact v55 manifest')
        manifest_path.write_bytes(origin.read_bytes())
    manifest=json.loads(manifest_path.read_text())
    old={n:v for d in manifest.values() for n,v in d.items()}
    require(len(old)==111,'Wrong baseline graph')
    for name,info in old.items():
        f=ARCHIVE/name if name=='main.tex' and (ARCHIVE/name).exists() else P/name
        data=f.read_bytes()
        require(hashlib.sha256(data).hexdigest()==info['sha256'],'Wrong baseline '+name)
    original=ARCHIVE/'main.tex'
    if not original.exists():original.write_bytes((P/'main.tex').read_bytes())
    before=original.read_text(); after=amended_main(before)
    require((P/'main.tex').read_text() in (before,after),'Unexpected main edit')
    (P/'main.tex').write_text(after)
    # The original structural statements and their proof paragraphs are shared verbatim.
    intro=(P/'article/00_structural_introduction_v48.tex').read_text()
    a=intro.index(r'\subsection{The observation and the main theorem}')
    b=intro.index(r'\subsection{Proof of the geometric inverse}')
    (P/'journal/01_structural_statements_v56.tex').write_text(intro[a:b])
    part=before.split(r'\part{Relative laws, signed inversion, and intrinsic rigidity}',1)[1].split(r'\part{Boundary information',1)[0]
    core=re.findall(r'\\input\{([^}]+)\}',part)
    # Only three comparison sentences require a document-name qualification.
    # Keep their entire statement/proof bodies unchanged in generated journal views.
    display_edits={
      'article/15_operator_comparison.tex':('experiment comparison in Part II,',
        'experiment comparison in Part II of the complete technical manuscript,'),
      'article/23p_uncentered_interaction_v51.tex':('Part III cannot be transferred',
        'Part III of the complete technical manuscript cannot be transferred'),
      'article/23q_support_and_interior_windows_v52.tex':('budgets of Part III to',
        'budgets of Part III of the complete technical manuscript to')}
    display_views={}
    (P/'journal/shared').mkdir(exist_ok=True)
    for src,(old_sentence,new_sentence) in display_edits.items():
        dst='journal/shared/'+Path(src).name
        (P/dst).write_text(replace_once((P/src).read_text(),old_sentence,new_sentence))
        display_views[src]=dst
    core=[display_views.get(x+'.tex',x+'.tex').removesuffix('.tex') for x in core]
    extra=['article/90_marked_results','v3/30_observability',
           'v4/20_nonlinear_information']
    entry=r'''% A2 v56. Principal journal article; shared complete proofs, no excerpted proof bodies.
\input{preamble}
\externaldocument[F-]{main}[main.pdf]
\title[Boundary laws and periodic rigidity]{Boundary laws and rigidity of periodic dispersing billiards}
\author{Qian Qi}
\date{September 15, 2026}
\subjclass[2020]{37D50, 37C30, 70H09, 53A04}
\keywords{Dispersing billiards, relative boundary laws, signed contact jets,
analytic rigidity, unknown lattice, endpoint interaction}
\hypersetup{pdftitle={Boundary laws and rigidity of periodic dispersing billiards},
pdfauthor={Qian Qi},pdfsubject={A2 revision 56; principal journal article}}
\begin{document}
\input{journal/full_reference_routes_v56}
\begin{abstract}
We reconstruct the signed contact jets of a smooth dispersing billiard
channel from its gap and two conditional endpoint laws at a fixed positive
excess time. A nonlinear relative limit on a flight-independent collar
retains two half-line actions despite an exponentially small reference
twist. Trace-class normalization and a finite stationary-envelope argument
justify the inverse for actual smooth boundaries, not only formal jets.
For noncircular analytic periodic tables, selected marked channels determine
finitely many complete realizations, including the unknown marked lattice;
proper asymmetry gives uniqueness. The inverse survives unknown transverse
origins and separate positive recording factors on visible interior windows.
Its differential has precisely the common Euclidean kernel, and immersed
finite-dimensional models admit local coordinates given by finitely many
gaps and law expectations. We give explicit geometric comparisons separating
nonlinear information, discrete matching ambiguity and continuous symmetry.
\end{abstract}
\maketitle
\setcounter{tocdepth}{1}
\tableofcontents
\input{journal/00_principal_introduction_v56}
\part{The relative law and the complete geometric inverse}
'''
    entry+='\n'.join(r'\input{'+x+'}' for x in core)
    entry+=r'''

\subsection*{Acknowledgments}
The author-requested AI-assisted memoranda cited here are not commissioned
journal reports. The finite-versus-infinitesimal symmetry distinction and
the circular comparison were communicated in~\cite{A2ReviewV48}; the
noncircular two-table example was communicated in~\cite{A2ReviewV49}.
The support-width centering comparison was communicated
in~\cite{A2ReviewV51}. The proofs and their attributions are retained
separately from the reports' nonbinding placement assessments.

\appendix
\renewcommand{\thesection}{A.\arabic{section}}
\renewcommand{\theHsection}{principal.appendix.\arabic{section}}
\part{Local coordinate conversion and comparison proofs}
\input{journal/02_graph_support_v56}
'''
    entry+='\n'.join(r'\input{'+x+'}' for x in extra)
    entry+='\n\\input{journal/references_v56}\n\\end{document}\n'
    (P/'rigidity.tex').write_text(entry)
    # Temporary stubs permit recursive graph computation without TeX execution.
    routes=P/'journal/full_reference_routes_v56.tex'
    bib=P/'journal/references_v56.tex'
    if not routes.exists():routes.write_text('% generated routes\n')
    if not bib.exists():bib.write_text('% generated bibliography\n')
    principal=graph(P,'rigidity.tex')
    texts={n:(P/n).read_text() for n in principal if n not in
           ('journal/full_reference_routes_v56.tex','journal/references_v56.tex')}
    principal_labels={l for t in texts.values() for l in re.findall(r'\\label\{([^}]+)\}',t)}
    full_labels={l for n in old for l in re.findall(r'\\label\{([^}]+)\}',(P/n).read_text())}
    refs={l for t in texts.values() for l in re.findall(r'\\(?:ref|eqref|autoref|pageref)\{([^}]+)\}',t)}
    external=sorted(refs-principal_labels)
    require(set(external)<=full_labels,'Unknown principal reference: '+str(set(external)-full_labels))
    proof_external=[]
    for name,text in texts.items():
        for proof in re.findall(r'\\begin\{proof\}.*?\\end\{proof\}',text,re.S):
            bad=set(re.findall(r'\\(?:ref|eqref|autoref|pageref)\{([^}]+)\}',proof))&set(external)
            if bad:proof_external.append({'file':name,'labels':sorted(bad)})
    require(not proof_external,'A printed proof depends on a full-only label: '+str(proof_external))
    code=r'''% Explicit external labels; internal proof labels are never redirected.
\makeatletter
\def\vFSave#1#2#3#4#5\@nil#6{%
  \expandafter\gdef\csname r@#6\endcsname{{F.#1}{#2}{#3}{#4}{#5}}}
\newcommand{\vFullAlias}[1]{%
  \@ifundefined{r@F-#1}{%
    \PackageError{A2-v56}{Missing full-manuscript label #1}{Build main.tex first.}%
  }{%
    \expandafter\expandafter\expandafter\vFSave\csname r@F-#1\endcsname\@nil{#1}%
  }}
'''
    code+='\n'.join(r'\vFullAlias{'+x+'}' for x in external)
    code+='\n\\makeatother\n'
    routes.write_text(code)
    cited={k.strip() for t in texts.values() for v in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',t) for k in v.split(',')}
    original_bib=(P/'v5/references_v43.tex').read_text()
    items=re.findall(r'(\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}.*?)(?=\\bibitem|\\end\{thebibliography\})',original_bib,re.S)
    require(cited<={k for _,k in items},'Unknown cited item')
    bib.write_text('\\begin{thebibliography}{99}\n'+''.join(t for t,k in items if k in cited)+'\\end{thebibliography}\n')
    proofmap={'baseline_source':SOURCE_V55,'review_head':REVIEW_V55,
       'principal_entry':'rigidity.tex','full_entry':'main.tex',
       'principal_inputs':sorted(principal),'shared_baseline_inputs':sorted(principal&set(old)),
       'external_comparison_labels':external,'external_labels_in_proof_environments':proof_external,
       'display_views':display_views,'display_edits':display_edits,
       'headline_source_labels':['thm:v56-local-mechanism','thm:v48-main','thm:v51-main'],
       'scope':'Static reference closure of printed proof environments plus an explicit reading map; not formal proof verification.'}
    write_json(P/'journal/DEPENDENCY_MAP_V56.json',proofmap)
    return {'status':'materialized','baseline_inputs':len(old),'principal_inputs':len(principal),
       'full_inputs':len(graph(P,'main.tex')|graph(P,'two_collision.tex')),
       'external_comparison_labels':external,'mathematical_certification':False}

if __name__=='__main__':print(json.dumps(materialize(),indent=2,sort_keys=True))
