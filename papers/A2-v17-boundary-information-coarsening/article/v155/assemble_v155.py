#!/usr/bin/env python3
"""Build the preservation master and two companion papers from locked sources."""
from __future__ import annotations
import argparse, collections, hashlib, json, os, re, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
PREV=HERE.parent/'v154'/'geometry.tex'
PREV_HASH='908fa5461d7978f3ee0f7bfbfec16aa5748be191e3486cfb7e73628cc5b062d1'
BASE='a3a59510072f8d012f4436807c83c66d1475573d'
REVIEW='52ebb8183433ad398f61958219b2af809f721824'
BIB=r'''\bibitem{NagaokaWachi2024}
T.~Nagaoka and A.~Wachi,
\emph{The strong Lefschetz property of Gorenstein algebras generated
by relative invariants}, arXiv:2403.05492v1 (2024),
Theorem~4, Example~5, Example~9, Proposition~10, Remark~11,
Lemma~13 and Proposition~16.
Published version: doi:10.1090/proc/16870.
'''
DISCLOSURE=r'''\paragraph{Revision 155.}
AI assistance was used to formulate and draft the exact quadratic
coefficient-section theorem and the reciprocal power-ideal description
of spectral Fitting schemes, to check their finite examples, and to
prepare the companion-paper organization.  Classical apolar and
orthogonal-orbit results are explicitly attributed.  The general
claims rely on the written proofs; finite exact tests and source
preservation are not formal proof certificates.

'''
I_ABSTRACT=r'''Every complex quadratic pencil is recovered, up to congruence,
from an unmarked and ungraded finite multiplication-failure algebra.
The first distinguishing order is $n^2+2n-4$, and every smaller
truncation is independent of the pencil.  The inverse includes singular
pencils and extends to moving pencil subbundles and source bundles.
We identify its intrinsic polarization and projective moduli
completion, determine the exact ambiguity of coefficient systems, and
establish curve, covering, rigidification and spectral specialization
forms of the inverse.  On fixed-discriminant, fixed-corank strata, the
full orthogonal specialization order is read from the recovered
spectral length profiles.'''
II_ABSTRACT=r'''We study the normalization fibres of common-divisor images in
Grassmannians of forms.  In the binary case the normalization is finite
flat over every exact-gcd stratum and its collision fibres are explicit
reciprocal complete intersections.  On the squarefree locus we determine
the conductor, every branch intersection and the complete graded Betti
table.  The entire quadratic coefficient section of every multivariate
reciprocal fibre is the apolar algebra of a power of the symmetric
determinant.  Its character and length yield uniform bounds for actual
first-relation boundary fibres.  In one such section, the power-zero
ideals of an embedded quadratic pencil equal powers of all its spectral
Fitting ideals.  Their nonreduced local structure detects Segre data and
the native fixed-spectrum degeneration order.'''
I_INTRO=r'''\section{Introduction}
\label{sec:introduction-v153}
The unmarked infinitesimal scheme of a multiplication failure contains
more information than its reduced support.  The principal result of
this paper is a sharp inverse theorem: a finite local algebra determines
every complex quadratic pencil after its grading, linear coordinates
and tensor marking have been forgotten.

Let $\dim V=n\geq3$, $N=\binom{n+1}{2}$,
$R\in\Gr(2,\Sym^2V)$, $p=N-2$ and $D=n+2p=n^2+2n-4$.
With the universal matrix $T$ and quotient $\gamma_R$ by $R$, the
invariant is
\[
 \mathfrak A_R^{[D]}=\C[t_{ij}]/
 \bigl((\det T)I_p(\gamma_R\Sym^2T)+\mathfrak m^{D+1}\bigr).
\]
Theorems~\ref{thm:artin-local-inverse-v146} and
\ref{thm:sharp-finite-pencil} assert that two such unmarked,
ungraded algebras are isomorphic precisely when their pencils are
congruent.  Every smaller truncation is independent of $R$.  The
argument does not exclude singular pencils.  It passes from the
intrinsic first relation to tensor rulings, removes the possible
factor interchange by a coefficient-support argument, and recovers
an actual local algebraic inverse.

The subsequent results concern structures preserved by that inverse,
not additional decorations placed on the finite input.  The moving
coefficient theorem recovers source bundles and pencil subbundles.
The intrinsic Pluecker line determines the polarization in
Theorem~\ref{thm:polarized-completion-v154} and the normal projective
coarse quotient of semistable pencils.  This is a compatibility with
classical GIT, not a properness claim for the full stack or a universal
ordinary algebra on a coarse space.  The recognition, curve, covering
and rigidification results describe the isomorphisms and ambiguities
of the same inverse.

The final spectral arguments use the cokernel of a regular member
pair.  On the fixed-discriminant, fixed-corank locus,
Theorem~\ref{thm:fixed-spectral-classification} gives all full
orthogonal orbits and their specialization order, with flat
realizations by the actual finite failure neighbourhoods.  The
orthogonal-orbit input is classical; its precise form and attribution
are isolated in Lemma~\ref{lem:orthogonal-orbits-v145}.

The companion paper, \emph{Divisor-incidence fibres and spectral
power-zero schemes}, treats the common-divisor images of first
relations.  In particular, its
Theorem~\ref{thm:power-Fitting-v155} realizes all spectral Fitting
schemes by power-zero ideals on a line inside one reciprocal
normalization-fibre section.  This supplies an algebraic incidence
realization of the spectral data recovered here; it is not needed
for the proof of the unmarked inverse.  References prefixed II
refer to the companion paper.  References without a prefix are
internal to this paper; the complete paired version retains the same
statements with unified numbering.

Classical comparisons and the exact scope of the finite invariant
are given in Appendix~\ref{sec:introduction-v132}.  The theorem
and proof text of \cite{Ballico93} has not been obtained.  We
therefore make no theorem-level claim about anticipation or
nonanticipation by that failure-locus paper.  The inverse theorem
stated above is unchanged by this documentary limitation.
'''
II_INTRO=r'''\section{Introduction}
\label{sec:divisor-introduction-v155}
For $E$ a complex vector space, common-factor multiplication defines
an incidence morphism
\[
 \Pj(\Sym^g E)\times\Gr(r,\Sym^{D-g}E)
   \longrightarrow\Gr(r,\Sym^D E),\qquad(f,J)\longmapsto fJ.
\]
Its image $Y_g$ has a finite normalization by this marked-factor
space.  The scheme fibre, rather than the number of its closed points,
is essential at colliding and multivariate common divisors.
We determine a global binary part of this geometry and use exact
sections of its multivariate fibres to encode spectral schemes.

Theorem~\ref{thm:binary-fibres-v153} proves that, over the exact
binary gcd-degree-$s$ stratum, normalization is finite flat of degree
$\binom{s}{g}$ and every collision fibre is a product of reciprocal
complete intersections.  On the squarefree open $\mathcal U$,
Theorem~\ref{thm:squarefree-v153} identifies the whole completed
local image and gives
\[
 \mathfrak c_{Y_g}|_{\mathcal U}
                  =\II_{Y_{g+1}/Y_g}|_{\mathcal U}.
\]
It computes all multiple branch intersections, depth, multiplicity
and seminormality.  The block model has the complete graded Betti
table of Theorem~\ref{thm:block-betti-v154}.  At arbitrary binary
collisions we give a completed incidence atlas.  That presentation
is not asserted to classify every analytic singularity or its
conductor.  The double-root singular Fitting ideals are separately
evaluated in all ranks.

For a pure-power divisor the normalization fibre is the reciprocal
algebra $F_{g,k}(W)$.  Theorem~\ref{thm:quadratic-section-v155}
identifies its entire quadratic coefficient section with the apolar
algebra $B_{d,h}$ of $(\det X)^h$ for symmetric matrices, where
$d=\dim W$ and $h=\lfloor g/2\rfloor$.  The exact equality of
coefficient ideals is the link with the determinant-power algebra.
The classical representation theory of \cite{NagaokaWachi2024}
then determines the section's whole Hilbert function and length;
its socle also bounds the Loewy depth of the original fibre.  For
the ternary first-relation boundary the section has length
$922268360$ and socle degree $24$.  These give a lower bound
and a nonvanishing maximal-ideal power for the entire fibre, not a
claim that the whole fibre is this Gorenstein section.

There is a second application which retains the pencil information.
For a pencil $R\subset\Sym^2V$, the degree-one space of the
section $B_{n,h}$ contains its line $\Lambda=\Pj(R)$.
Theorem~\ref{thm:power-Fitting-v155} proves
\[
 \mathcal J_{h(n-j)}=\Fitt_j(\mathcal T_R)^h,
                          \qquad0\leq j\leq n,
\]
where $\mathcal J_p$ is the ideal of the $p$th power on this
line and $\mathcal T_R$ is the universal symmetric cokernel.
The proof diagonalizes over a discrete valuation ring and calculates
the minimal valuation of every power coefficient.  In particular
the equality preserves nonreduced multiplicity, applies also to
singular pencils, and is not an inference from set-theoretic rank
loci.  For a regular pencil the local lengths recover the full Segre
symbol.  Their inclusions express the native fixed-spectrum full
orthogonal closure order.

The companion paper, \emph{Finite failure schemes and the
reconstruction of quadratic pencils}, proves the sharp unmarked
inverse and its relative and spectral forms.  Those results are
used here only for the intrinsic interpretation and the pencil
applications; the divisor-image and reciprocal-section proofs do
not depend on that inverse.  References prefixed I refer to the
companion paper.  Its orthogonal closure theorem is not claimed
again as a new classification here.  The full $\operatorname{GL}(E)$
common extreme limit is a different construction from the embedded
native pencil line: the extreme point by itself forgets the pencil.

Binary reciprocal, Stanley--Reisner and determinant-apolar inputs
are credited to \cite{Grinberg2019,MillerSturmfels2005,
ShafieiSymmetric,NagaokaWachi2024}.  The new uses are the
normalization-fibre identifications, their scheme structure and
the power-ideal identity on a pencil line.  The comparison with
\cite{Ballico93} remains documentary-limited: its theorem and
proof text has not been obtained and no priority conclusion is
drawn from that absence.
'''

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def once(t:str,a:str,b:str)->str:
    if t.count(a)!=1:raise ValueError(f'Nonunique anchor: {a}')
    return t.replace(a,b,1)
def labels(t:str)->list[str]:return re.findall(r'\\label\{([^}]+)\}',t)
def refs(t:str)->set[str]:return set(re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}',t))
BLOCK=re.compile(r'\\begin\{(theorem|lemma|proposition|corollary|definition|example|remark|proof)\}.*?\\end\{\1\}',re.S)
def blocks(t:str)->collections.Counter:return collections.Counter(m.group(0) for m in BLOCK.finditer(t))
def compile_one(name:str,passes:int=2)->None:
    for i in range(passes):
        with (HERE/f'{name}-build-pass-{i+1}.txt').open('w') as f:
            subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',name+'.tex'],cwd=HERE,stdout=f,stderr=subprocess.STDOUT,check=True)
def aux_labels(name:str)->dict[str,tuple[str,str]]:
    t=(HERE/(name+'.aux')).read_text()
    return {m.group(1):(m.group(2),m.group(3)) for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}',t)}
def aliases(needed:set[str],other:dict[str,tuple[str,str]],prefix:str)->str:
    out=['% Embedded companion-paper references; no external aux file is required.','\\makeatletter']
    for key in sorted(needed):
        if key not in other:raise ValueError('Absent companion reference '+key)
        number,page=other[key]
        out.append(r'\@namedef{r@'+key+'}{{'+prefix+number+'}{'+prefix+page+'}{}{}{}}')
    out.append('\\makeatother\n')
    return '\n'.join(out)
def source(preamble:str,title:str,abstract:str,intro:str,body:str,tail:str,cross:str='')->str:
    return preamble+cross+'\n\\begin{document}\n\\title{'+title+'}\n\\author{Qian Qi}\n\\date{September 25, 2026}\n\\subjclass[2020]{14M12, 14B05, 14D20, 13C40}\n\\hypersetup{pdftitle={'+title+'},pdfauthor={Qian Qi}}\n\\begin{abstract}\n'+abstract+'\n\\end{abstract}\n\\maketitle\n'+intro+'\n'+body+'\n'+tail

def main()->None:
    ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');args=ap.parse_args()
    if sha(PREV)!=PREV_HASH:raise RuntimeError('Locked v154 source hash mismatch')
    old=PREV.read_text();start=old.index('\\begin{abstract}');end=old.index('% BEGIN PRESERVED PART')
    (HERE/'PREVIOUS_FRONTMATTER_V154.tex').write_text(old[start:end])
    body=old[end:]
    body=once(body,'\\section{Descent and complete-local details}',(HERE/'reciprocal-spectral-v155.tex').read_text()+'\n\\section{Descent and complete-local details}')
    body=once(body,'\\end{thebibliography}',BIB+'\n\\end{thebibliography}')
    body=once(body,'\\begin{thebibliography}{99}',DISCLOSURE+'\\begin{thebibliography}{99}')
    master=old[:start].replace('revision 154','revision 155')+(HERE/'front-v155.tex').read_text()+'\n'+body
    missing=set(labels(old))-set(labels(master));dups=[k for k,v in collections.Counter(labels(master)).items() if v>1]
    lost=blocks(old)-blocks(master);badrefs=refs(master)-set(labels(master))
    cites={x.strip() for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',master) for x in group.split(',')}
    bib=set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',master))
    if missing or dups or lost or badrefs or cites-bib:
        raise RuntimeError(str({'missing_labels':sorted(missing),'duplicates':dups,'lost_blocks':len(lost),'undefined_refs':sorted(badrefs),'undefined_citations':sorted(cites-bib)}))
    (HERE/'geometry.tex').write_text(master)
    # Partition every mathematical body block exactly once, never reconstruct proofs from summaries.
    cut=body.index('% BEGIN PRESERVED PART 17-assistance.tex')
    mathematical=body[:cut];tail=body[cut:]
    mathematical=re.sub(r'\\part\*\{[^}]*\}\s*','',mathematical)
    mathematical=mathematical.replace('\\appendix','')
    starts=list(re.finditer(r'\\section\{([^}]+)\}',mathematical))
    paper_i=[];paper_ii=[];mapping=[]
    appendix=False
    i_main={'First relations, ungraded isomorphisms, and inverse systems','Intrinsic tensor rulings','Actual factor descent and moving coefficient spaces','An intrinsic coefficient principle','Quadratic relation spaces and intrinsic reconstruction of pencils','The exact infinitesimal order of pencil reconstruction','Coefficient-support orientation and a local algebraic inverse','The intrinsic polarization and a projective moduli completion'}
    for j,m in enumerate(starts):
        title=m.group(1);block=mathematical[m.start():starts[j+1].start() if j+1<len(starts) else len(mathematical)]
        if title=='Detailed reconstruction statements and comparisons':appendix=True
        dest='I' if title in i_main or appendix else 'II'
        if title=='Detailed reconstruction statements and comparisons':paper_i.append('\\appendix\n')
        (paper_i if dest=='I' else paper_ii).append(block)
        mapping.append({'section':title,'paper':dest,'labels':labels(block)})
    i_body='\n'.join(paper_i);ii_body='\n'.join(paper_ii)
    if blocks(mathematical)!=blocks(i_body)+blocks(ii_body):raise RuntimeError('Companion proof partition lost or duplicated a mathematical block')
    preamble=old[:old.index('\\begin{document}')]
    make_i=lambda cross='':source(preamble,'Finite failure schemes and the reconstruction of quadratic pencils',I_ABSTRACT,I_INTRO,i_body,tail,cross)
    make_ii=lambda cross='':source(preamble,'Divisor-incidence fibres and spectral power-zero schemes',II_ABSTRACT,II_INTRO,ii_body,tail,cross)
    i0,ii0=make_i(),make_ii();external_i=refs(i0)-set(labels(i0));external_ii=refs(ii0)-set(labels(ii0))
    if external_i-set(labels(ii0)) or external_ii-set(labels(i0)):raise RuntimeError('Cross-paper reference not assigned')
    (HERE/'reconstruction.tex').write_text(i0);(HERE/'divisor-geometry.tex').write_text(ii0)
    (HERE/'PAPER_MAP_V155.json').write_text(json.dumps({'papers':{'I':'reconstruction','II':'divisor-geometry'},'section_allocation':mapping,'I_external_labels':sorted(external_i),'II_external_labels':sorted(external_ii),'all_body_mathematical_blocks_partitioned_exactly_once':True},indent=2)+'\n')
    preservation={'revision':155,'base_commit':BASE,'controlling_review_commit':REVIEW,'predecessor_sha256':PREV_HASH,'predecessor_labels':len(labels(old)),'current_labels':len(labels(master)),'missing_predecessor_labels':sorted(missing),'duplicate_labels':dups,'predecessor_math_blocks':sum(blocks(old).values()),'all_predecessor_math_blocks_retained_byte_for_byte':not lost,'all_body_math_blocks_partitioned_exactly_once_in_companions':True,'predecessor_source_modified':False,'previous_frontmatter_archived':True}
    (HERE/'NONDELETION_V155.json').write_text(json.dumps(preservation,indent=2)+'\n')
    receipt=dict(preservation,source_commit=os.environ.get('GITHUB_SHA','local-build'),compiled=False,historical_28_checks_rerun=False,Ballico_1993_full_text_comparison_completed=False,general_proofs_certified_by_computation=False,journal_acceptance_asserted=False)
    if args.build:
        compile_one('geometry',3)
        compile_one('reconstruction',2);compile_one('divisor-geometry',2)
        oldmaps=None
        for attempt in range(4):
            imap=aux_labels('reconstruction');iimap=aux_labels('divisor-geometry')
            maps=(aliases(external_i,iimap,'II.'),aliases(external_ii,imap,'I.'))
            (HERE/'reconstruction.tex').write_text(make_i(maps[0]));(HERE/'divisor-geometry.tex').write_text(make_ii(maps[1]))
            compile_one('reconstruction',2);compile_one('divisor-geometry',2)
            if maps==oldmaps:break
            oldmaps=maps
        else:raise RuntimeError('Companion page/number maps did not stabilize')
        outputs={}
        for name in ('geometry','reconstruction','divisor-geometry'):
            log=(HERE/(name+'.log')).read_text(errors='replace')
            bad=[s for s in ('undefined references','There were undefined','multiply defined','Citation `') if s in log]
            overfull=re.findall(r'Overfull \\hbox \(([^)]+)\)',log)
            if bad or overfull:raise RuntimeError(str({'file':name,'bad':bad,'overfull':overfull}))
            subprocess.run(['pdftotext','-layout',name+'.pdf',name+'.txt'],cwd=HERE,check=True)
            info=subprocess.run(['pdfinfo',name+'.pdf'],cwd=HERE,check=True,text=True,capture_output=True).stdout
            outputs[name]={'pages':int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1)),'source_sha256':sha(HERE/(name+'.tex')),'pdf_sha256':sha(HERE/(name+'.pdf')),'pdf_bytes':(HERE/(name+'.pdf')).stat().st_size,'clean_references_and_no_overfull_hboxes':True}
        receipt.update(compiled=True,outputs=outputs,companion_reference_maps_embedded_and_stable=True)
    receipt['input_sha256']={p.name:sha(p) for p in sorted(HERE.glob('*')) if p.name in ('front-v155.tex','reciprocal-spectral-v155.tex','assemble_v155.py','check_v155.py')}
    for name in ('EXACT_CHECKS_V155.json','INHERITED_V154_CHECKS_RERUN.json'):
        if (HERE/name).exists():receipt[name+'_sha256']=sha(HERE/name)
    (HERE/'BUILD_RECEIPT_V155.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
