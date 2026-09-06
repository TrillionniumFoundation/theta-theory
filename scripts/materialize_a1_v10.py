#!/usr/bin/env python3
"""Reorder the pinned v9 argument without altering its forty proof blocks.

Writes only papers/A1-english-v10. No network calls, inherited-test edits,
repository ref updates or deletions. Templates are kept separate from the
printed source, and preservation is checked on the actual main.tex inputs.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / 'papers/A1-english-v9'
NEW = ROOT / 'papers/A1-english-v10'
REVIEW = '7a499e3cb32396b18eda869342ec8e9c70d8d028'
SUBMISSION = 'e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5'
PINS = {
 'main.tex':'cab616c756c322718ba305d6f4fd3c41b943daca',
 'references.tex':'8bab36ef02df6af551c3a000213ce17114108c86',
 'sections/01_introduction.tex':'8b8881ca0fc7ffc6467b5739f4bde233d21da858',
 'sections/02_experiments.tex':'1bd4f6273d62c860f8a348dcc4f72734dbc388db',
 'sections/03_transversality.tex':'6395724ba2c4bed3ead19178a1cfe8206f9a3824',
 'sections/04_observation_algebra.tex':'c3c127d2370371d45334b9d3ff61f2e9e5e98718',
 'sections/05_confluence.tex':'73eeae176876f515676f4148961cfb09146c9547',
 'sections/06_streaming.tex':'e662f435a3a485542606b759b7a3129f298cd865',
 'sections/06a_attainable_filtration.tex':'fedb4c3421227a6c8060d32d2091a5d65ff9a9a6',
 'sections/06b_collision_geometry.tex':'e0b9ba68173fc2b50f9e9fc30038959484f2ce96',
 'sections/07_uniform_resolution.tex':'03ad17ec736f673c0ad274733fde4092d28333bc',
 'sections/08_sequential_value.tex':'cd811b4398e55953def241cf43383816225f700c',
 'sections/09_common_risk.tex':'3f41b497d5602afc7f9f5bf6aa089a6fe7bf355d',
 'sections/10_scope.tex':'2512cdb91cb83856ef7aaa63d80cc4220ed7dcc9',
}

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def read(name: str) -> str:
    data=(OLD/name).read_bytes()
    if blob(data)!=PINS[name]:
        raise RuntimeError('Pinned input mismatch: '+name)
    return data.decode('utf-8')

def write(name: str, text: str) -> None:
    p=NEW/name
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(text,encoding='utf-8')

def result_block(text: str, label: str, proof: bool=False) -> str:
    pos=text.index('\\label{'+label+'}')
    matches=list(re.finditer(r'\\begin\{(theorem|lemma|proposition|corollary)\}',text[:pos]))
    if not matches: raise RuntimeError('No result start: '+label)
    start=matches[-1].start()
    endmark=r'\end{proof}' if proof else '\\end{'+matches[-1].group(1)+'}'
    end=text.index(endmark,pos)+len(endmark)
    return text[start:end]

PROOF_RE=re.compile(r'\\begin\{proof\}(?:\[[^\]]*\])?.*?\\end\{proof\}',re.S)
LABEL_RE=re.compile(r'\\label\{((?:thm|lem|cor|prop):[^}]+)\}')

def main() -> None:
    src={name:read(name) for name in PINS}
    intro=src['sections/01_introduction.tex']
    tpl=(NEW/'templates/01_introduction.tex.in').read_text()
    tpl=tpl.replace('@@SCALAR_STATEMENT@@',result_block(intro,'thm:resolution-main'))
    tpl=tpl.replace('@@EXACT_STATEMENT@@',result_block(intro,'thm:main'))
    write('sections/01_introduction.tex',tpl)
    write('sections/02_experiments.tex',src['sections/02_experiments.tex'])
    write('sections/04_transversality.tex',src['sections/03_transversality.tex'])

    stream=src['sections/06_streaming.tex']
    cut=stream.index(r'\begin{lemma}[Uniform finite-horizon transition bounds]')
    model=stream[:cut].replace(r'\section{Finite-state filtering after every report}\label{sec:streaming}',
       r'\section{Persistent memory and the prediction task}\label{sec:resource-model}',1)
    write('sections/03_finite_state.tex',model)
    opening=stream[stream.index('\n')+1:stream.index(r'\begin{definition}')]
    write('sections/C_fixed_streaming.tex',
        r'\section{Fixed-calibration streaming and control}\label{sec:streaming}'+'\n'+opening+stream[cut:])

    affine=src['sections/05_confluence.tex']
    confluent=result_block(affine,'lem:confluent-positive',proof=True)
    classical=(NEW/'templates/05_classical_flag.tex.in').read_text().replace('@@STRICT_CONFLUENT@@',confluent)
    write('sections/05_classical_flag.tex',classical)
    affine=affine.replace(confluent,
        'The strict mixed pairing used below is Lemma~\\ref{lem:confluent-positive}; its proof precedes the intrinsic theorem.\n',1)
    write('sections/B_affine_confluence.tex',affine)

    attained=src['sections/06a_attainable_filtration.tex']
    start=attained.index(r'\subsection{A global covering estimate}')
    end=attained.index(r'\begin{lemma}[The whole attainable image has bounded format]')
    cover=attained[start:end].replace(r'\subsection{A global covering estimate}',
        r'\section{A global dimension-truncated covering estimate}\label{sec:global-cover}',1)
    write('sections/06_global_cover.tex',cover)
    attained=attained[:start]+r'''\subsection{Format and the attained flag}
The covering estimate needed for the whole image is
Lemma~\ref{lem:tame-rectangle}, proved before the intrinsic classification.

'''+attained[end:]
    write('sections/D_attainable_affine.tex',attained)

    collision=src['sections/06b_collision_geometry.tex']
    end=collision.index(r'\subsection{Calibration chamber and determinant volumes}')
    collision=r'''\section{Intrinsic resolution at arbitrary exponent collisions}\label{sec:collision-geometry}
We now prove the scalar resolution theorem. Maximal Vandermonde products
on the future exponent set determine both attained checkpoint resolution
and causal memory. They are defined at an exact collision without choosing
a path into it. The finite spectral interpretation is
Proposition~\ref{prop:ordinary-spectrum}; the argument here establishes
attainability, the global image bound, and compatibility with causal updates.

'''+collision[end:]
    write('sections/07_collision_geometry.tex',collision)
    for old,new in [('04_observation_algebra','A_observation_algebra'),
                    ('07_uniform_resolution','E_five_trial'),
                    ('08_sequential_value','F_sequential_value'),
                    ('09_common_risk','G_common_risk')]:
        write('sections/'+new+'.tex',src['sections/'+old+'.tex'])
    # The displaced introductory exposition and history are retained in full,
    # separately from the principal's mathematical dependency spine.
    write('retained/v9_introduction.tex',intro)
    write('retained/v9_scope.tex',src['sections/10_scope.tex'])

    refs=src['references.tex'].replace(r'\end{thebibliography}',r'''
\bibitem{GuoKaragodinStepanov}
T. Guo, N. Karagodin and E. Stepanov,
\emph{Optimal functional product quantization}, author preprint,
version \texttt{guokaragste22a8}, Sections 1.1--1.2 and 5.5.
\url{https://cvgmt.sns.it/media/doc/paper/6002/guokaragste22a8.pdf}.
\bibitem{A1v9note}
\emph{The classical spectral content and phase structure of A1 v9},
source-pinned technical note accompanying the owner-requested AI-assisted
repository review, September 6, 2026,
\href{https://github.com/TrillionniumFoundation/theta-theory/blob/7a499e3cb32396b18eda869342ec8e9c70d8d028/reviews/a1-english-v9-2026-09-06/TECHNICAL_NOTE.md}{commit \texttt{7a499e3cb323}}.
\end{thebibliography}''')
    write('references.tex',refs)
    preamble=src['main.tex'].split(r'\title',1)[0]
    maintex=preamble+r'''\title[Sparse observations and shared memory]{Sparse observation algebras:\\ collision geometry and shared memory}
\author{Qian Qi}
\date{September 6, 2026}
\subjclass[2020]{62B05, 62C10, 93E11, 13D40}
\keywords{attainable information state, sparse observation algebra, exponent collision,
finite-state filtering, joint quantization, shared memory}
\hypersetup{pdftitle={Sparse observation algebras: collision geometry and shared memory},pdfauthor={Qian Qi}}
\begin{document}
\begin{abstract}
We determine the persistent memory of positive sparse monomial experiments
through arbitrary additive exponent collisions, and prove a composition
law when independent experiments share a single finite-state memory.
At a scalar checkpoint, the optimal squared-prediction regret is comparable
to the maximum of partial Vandermonde-volume powers, truncated at the
attainable past dimension. The comparison is uniform on compact subsets
of the one-step exponent chamber, including exact collisions, for fixed
full-support priors and finite horizons. Under independent composition,
the future query space is a tensor product, but the attained information
dimensions and resolved bit requirements add at each checkpoint. This
holds against arbitrary joint encoders, not only product codes. One
index-only transducer attains the maximum checkpoint law through all
stages. The proof combines complete Newton--Hermite flags, a global
bounded-format cover retaining each block's past cap, a product
minorization with acquisition evidence, and nonsingular raw moment
updates. The resulting bit law quantifies the effect of observation
order: serial schedules attain the largest individual memory requirement,
whereas overlapping schedules can attain their sum. Collision-tree
formulas and the exact, affine, control and common-risk consequences are
proved under their respective operational hypotheses.
\end{abstract}
\maketitle
\input{sections/01_introduction}
\input{sections/02_experiments}
\input{sections/03_finite_state}
\input{sections/04_transversality}
\input{sections/05_classical_flag}
\input{sections/06_global_cover}
\input{sections/07_collision_geometry}
\input{sections/08_shared_memory}
\input{sections/09_scheduling}
\appendix
\input{sections/A_observation_algebra}
\input{sections/B_affine_confluence}
\input{sections/C_fixed_streaming}
\input{sections/D_attainable_affine}
\input{sections/E_five_trial}
\input{sections/F_sequential_value}
\input{sections/G_common_risk}
\input{sections/H_tree_convexity}
\input{references}
\end{document}
'''
    write('main.tex',maintex)

    printed=[]
    for name in re.findall(r'\\input\{([^}]+)\}',maintex):
        printed.append((NEW/(name+'.tex')).read_text())
    oldtext='\n'.join(v for k,v in src.items() if k.startswith('sections/'))
    newtext='\n'.join(printed)
    oldproofs=PROOF_RE.findall(oldtext)
    newproofs=PROOF_RE.findall(newtext)
    oldhash=[sha256(p.encode()) for p in oldproofs]
    newhash=[sha256(p.encode()) for p in newproofs]
    missing=Counter(oldhash)-Counter(newhash)
    oldlabels=sorted(set(LABEL_RE.findall(oldtext)))
    newlabels=LABEL_RE.findall(newtext)
    if missing or not set(oldlabels)<=set(newlabels):
        raise RuntimeError('An inherited result/proof is missing')
    if len(newlabels)!=len(set(newlabels)):
        raise RuntimeError('Duplicate named result labels in printed source')
    report={
      'review_commit':REVIEW,'reviewed_submission':SUBMISSION,
      'input_git_blobs':PINS,
      'input_sha256':{k:sha256((OLD/k).read_bytes()) for k in PINS},
      'old_result_labels':oldlabels,'old_proof_sha256':oldhash,
      'printed_result_labels':sorted(newlabels),'printed_proof_sha256':newhash,
      'inherited_labels':len(oldlabels),'inherited_proofs':len(oldproofs),
      'printed_labels':len(newlabels),'printed_proofs':len(newproofs),
      'missing_inherited_labels':[],'missing_inherited_proofs':[],
      'interpretation':'Source preservation only; not mathematical or editorial certification.'
    }
    write('validation/PRESERVATION.json',json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['inherited_labels','inherited_proofs','printed_labels','printed_proofs']}))

if __name__=='__main__':
    main()
