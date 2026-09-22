#!/usr/bin/env python3
"""Build v118 sources from the immutable, reviewed v117 sibling.
Only this v118 directory is written. All prior theorems are retained;
the truncation lemma is relocated, not removed. New sections live in parts/.
"""
from pathlib import Path
import hashlib, json, re, shutil
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'v117'
BRANCH='revision/a2-v118-higher-defect-nonreduced-generators-2026-09-22'
REVIEW='2c6f180fa0baf23386e0a46a64abe7503ea65b00'
BASE='fb999b3a43fe4331becb42646bc2faeadfa5492a'
TITLE=r'Conductor strata and nonreduced\\multiplication failure schemes'
ABSTRACT=r'''We study multiplication failure as a coherent-cokernel problem, including its nonreduced structure. For a finite locally free algebra, stable multiplication admits a canonical generated subalgebra; stratifying its action on the quotient gives conductor flags compatible with arbitrary base change on each stratum. In codimension two the controlling quotients have rank three or four, with a quadratic-algebra tower in the latter case. For the truncated local algebra in $e$ variables of order $h$, the entire generating $(e+1)$-plane family has stable failure ideal equal to the $\binom{e+h-1}{e+1}$th power of a determinant divisor. This determines its primary structure and every ordinary power. A triangular conductor argument transports these schemes to global multiplication on $\mathbb P^e$ in the dimension-independent range $n\ge2h-1$, sharp uniformly over generating ranks. We retain the sharp rank-dependent curve comparison, the hyperplane theorem controlled by rank-two quotients, the contact primary classifications and normalization, and the reduced three-plane realization of Haiman's diagonal ideal. The primary assertions always specify their parameter spaces; coherent cokernel comparisons, rather than primary decompositions of arbitrary specializations, are what commute universally with base change.'''

def replace_once(t,old,new):
    if t.count(old)!=1: raise ValueError('replacement not unique: '+old[:90])
    return t.replace(old,new,1)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    if not (OLD/'geometry.tex').is_file(): raise RuntimeError('Reviewed v117 sibling required')
    (HERE/'parts').mkdir(exist_ok=True)
    paths=sorted(list(OLD.glob('*.tex'))+list((OLD/'parts').glob('*.tex')))
    for p in paths:
        q=HERE/p.relative_to(OLD); q.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(p,q)
    shutil.copyfile(OLD/'make_crossrefs.py',HERE/'make_crossrefs.py')
    # Preliminary lemma moved verbatim from the reduced three-plane section.
    p=HERE/'parts/03-plane-generators.tex'; t=p.read_text()
    start=t.index(r'\begin{lemma}[Total-degree truncation]')
    end=t.index(r'\end{proof}',start)+len(r'\end{proof}')
    lemma=t[start:end]
    t=t[:start]+t[end:]
    t=replace_once(t,'We first give a finite-degree statement over a coefficient ring;\npointwise interpolation alone would not suffice for a statement\nabout ideals.',r'''This theorem realizes Haiman's diagonal ideal as the stable Fitting
ideal of an actual multiplication map. The all-powers identity is
Haiman's input, not a theorem deduced here from multiplication.
The resulting global-section failure schemes and their coherent
cokernels are obtained using the conductor comparison.''')
    t=replace_once(t,'before any localization; hence they hold on the rank-three open.',r'''before any localization; hence they hold on the rank-three open.
In that corollary Haiman's $n$ is our number $d$ of labelled points,
and Haiman's exponent $d$ is our power $q$. These two indices are
independent; no restriction on $q$ is imposed.''')
    p.write_text(t)
    prelim=r'''\section{Generating opens and finite presentations}
\label{sec:finite-preliminaries}
Here ``generating'' refers to generation as an ideal or invertible
module. It does not assert generation as a unital algebra.

\begin{lemma}[The relative generating open]\label{lem:generating-open}
Let $B/S$ be a finite locally free commutative algebra over a
$\C$-scheme, and let $A\subset B$ be a subbundle. The following
conditions are equivalent: $B\otimes A\to B$ is surjective; on every
geometric fibre $A$ has nonzero image in every residue field of $B$;
and the open $A^\times$ of sections of $A$ which are units of $B$
is smooth and surjective over $S$. These conditions define an open
in the Grassmannian. The assertions have the same form for a
subbundle of an invertible $B$-module, using generating sections in
place of units.
\end{lemma}
\begin{proof}
Surjectivity is equivalent to its geometric-fibre version by
Nakayama's lemma. On a finite algebra over an algebraically closed
field, an ideal is the unit ideal exactly when its images in all
residue fields are nonzero. These evaluations cut out finitely many
proper hyperplanes in $A$. Their complement is nonempty over an
infinite field and consists precisely of units. On the total space
of the vector bundle $A$, invertibility is the open condition
$\det(b\mapsto ab)\ne0$. This open is smooth over $S$, and the
preceding fibre calculation proves surjectivity. Conversely a unit
section after a faithfully flat cover generates the unit ideal,
which descends. The Grassmannian open is the complement of the
support of the cokernel of $B\otimes A\to B$. Local trivializations
of an invertible module prove the last assertion.
\end{proof}

'''
    (HERE/'parts/01a-finite-preliminaries.tex').write_text(prelim+lemma+'\n')
    # Explicit global line and projective bundle, with no loss of old statements.
    p=HERE/'parts/02-quotient-hilbert.tex'; t=p.read_text()
    t=replace_once(t,'The sheaf $\\mathcal C_m$ is the direct image of a line bundle on\n$Y$; in particular all positive-index Fitting ideals are the unit\nideal.',r'''If $i:Y\hookrightarrow X$ and $B_Y\twoheadrightarrow Q\supset\ell$
is the universal quotient with its generating line, the canonical formula is
\begin{equation}\label{eq:hyperplane-canonical-line}
 \mathcal C_m\simeq i_*(Q/\ell^{(m)}),\qquad
 \ell^{(m)}=\operatorname{im}(\ell^{\otimes m}\longrightarrow Q).
\end{equation}
Both $\ell^{(m)}$ and its quotient are line bundles on $Y$.
In particular all positive-index Fitting ideals are the unit ideal.''')
    t=replace_once(t,'The local cyclic presentations give the\nline-bundle assertion and the higher Fitting ideals. Trivializing\nan invertible $B$-module gives the last assertion; independence of\nthe chosen unit gives the required gluing.',r'''On $Y$, the normalized subalgebra $A'$ has conductor $J$, and
$J\subset a^m A'=(\mathcal A)^m$ since $a$ is a unit and $J$ an ideal.
Passing to $Q$ identifies $(\mathcal A)^m/J$ with $\ell^{(m)}$.
This gives the canonical map in \eqref{eq:hyperplane-canonical-line};
the local cyclic presentations identify it as an isomorphism.
Multiplication by a local unit spanning $\ell$ makes $\ell^{(m)}$
a direct-summand line, so the quotient is indeed a line bundle.
For an invertible $B$-module $P$, put $P_Q=P\otimes_B Q$; the same
formula is $i_*(P_Q^{\otimes_Q m}/\ell^{(m)})$, where now
$\ell\subset P_Q$. Trivialization of $P$ gives the local proof and
this intrinsic expression supplies its gluing.''')
    t=replace_once(t,'exactly the stated open projective bundle. It is nonempty on every',r'''exactly the following canonical open projective bundle.
On $T=\operatorname{Sym}^2 C\times\operatorname{Sym}^{d-2} C$
let $\mathcal Z\subset C\times T$ be the universal degree-two divisor
and set $F=(\pi_{\mathcal Z})_*\mathcal O_{\mathcal Z}$.
Use the projectivization $\Pj_T^{\rm lines}(F)$ parametrizing line
subbundles of $F$, and retain the open where the tautological line
$\ell$ satisfies $F\ell=F$. This is the claimed bundle, not an
unspecified local form. For a restricted line bundle replace $F$
by $(\pi_{\mathcal Z})_*(L|_{\mathcal Z})$ and use generation as an
$F$-module. The open is nonempty on every''')
    p.write_text(t)
    # Fully relative curve statement, naming all base-change objects.
    p=HERE/'parts/01-sharp-conductor.tex'; t=p.read_text()
    t=replace_once(t,'They hold relatively, and after arbitrary base change, for smooth\nprojective families of curves with these fibrewise hypotheses and\nlocally free direct images of the displayed line bundles.',r'''For the relative assertion, let $f:C\to S$ be smooth and projective
of relative dimension one, with $S$ locally Noetherian over $\C$,
let $D$ be a relative effective Cartier divisor finite flat of degree
$d$, and let $L$ be invertible. Assume the preceding hypotheses on
every geometric fibre. For each $j\ge1$ and $b=0,1,2$, put
$E_{j,b}=f_*L^j(-bD)$. These are locally free, $R^1f_*L^j(-bD)=0$,
and their formation commutes with arbitrary base change. The same
base-change property holds for the finite direct images of
$L^j|_D$ and $L^j(-D)|_D$. On the relative generating Grassmannian
form $\mathcal U$ as the inverse image of $\mathcal A$ in $E_{1,0}$.
The displayed saturation and cokernel assertions then hold as maps
of these bundles and sheaves, after every base change.''')
    t=replace_once(t,'The relative assertion follows from fibrewise\nsurjectivity of maps of vector bundles, exactly as in\nTheorem~\\ref{thm:sharp-conductor}.',r'''For the relative assertion, the assumed fibrewise $H^1$-vanishing
for $b=2$ implies the same vanishing for $b=1,0$ by restriction to
$D$. Cohomology and base change for these flat line bundles on a
proper flat relative curve gives the named direct images, with no
higher cohomology; finite flat pushforward gives the two restriction
bundles. In particular $0\to E_{1,1}\to E_{1,0}\to f_*(L|_D)\to0$
is a locally split exact sequence. The quadratic map
$\Sym^2E_{1,1}\to E_{2,2}$ and each map
$E_{1,1}\otimes\Sym^{m-1}\mathcal U\to E_{m,1}$ are surjective
on every geometric fibre by the fixed-curve proof. They are thus
surjections of vector bundles and remain so under arbitrary
pullback. The same locally split restriction square proves the
relative cokernel assertion; no base-change assumption on an
unflattened image $U^j$ is needed.''')
    p.write_text(t)
    # Orient the primary article around both new mechanisms; keep old statements.
    p=HERE/'parts/00a-conductor-introduction.tex'; t=p.read_text()
    t=t.replace('The principal structural result concerns generating hyperplanes in','The defect-one structural theorem concerns generating hyperplanes in')
    anchor='scheme without passing to its radical.\n'
    addition=r'''
Two results take this comparison beyond reduced contacts and rank-two
quotients. First, the stable generated algebra carries a representation
on the multiplication defect. Its exact-rank strata identify the
conductor quotient as a flag $C\subset Q$ with $C$ acting faithfully
on $Q/C$ (Theorem~\ref{thm:higher-defect-strata}). In codimension two
there are two mechanisms: a rank-three quotient with its scalar line,
or a rank-four quotient which is quadratic over a quadratic algebra
(Theorem~\ref{thm:codimension-two}). The transition between them can
itself be nonreduced.

Second, let $Z$ be the order-$h$ fat point of $\Pj^e$, with $e\ge2$
and $h\ge3$. For every $n\ge2h-1$, take all series containing
$H^0(\mathcal I_Z(n))$ and restricting to a generating $(e+1)$-plane
on $Z$. In symmetric degrees $m\ge h-1$ their failure ideal is
\begin{equation}\label{eq:intro-fat-main}
 \mathcal I_\Delta^{\binom{e+h-1}{e+1}},
\end{equation}
where $\Delta$ is the integral determinant divisor of the map from
the augmentation kernel of the restricted series to
$\mathfrak m/\mathfrak m^2$. This is the full primary ideal, and
all its powers remain primary (Corollary~\ref{cor:global-fat-primary}).
The proof separates a filtered substitution determinant from a
triangular global conductor argument. It gives three-plane results
on every $\C[x,y]/(x,y)^h$ and works in arbitrary embedding dimension;
no diagonal-ideal theorem is used. The global range depends on the
fat-point order, rather than its binomially growing length.

'''
    t=replace_once(t,anchor,anchor+addition)
    p.write_text(t)
    # Updated front matter and inclusion graph; full complements untouched.
    for name in ['geometry.tex','paper.tex']:
        p=HERE/name; t=p.read_text()
        t=t.replace(r'\title[Finite quotients and multiplication failure]{Finite quotients and primary structures\\of multiplication failure schemes}',r'\title[Conductor strata and multiplication failure]{'+TITLE+'}')
        t=t.replace('pdftitle={Finite quotients and primary structures of multiplication failure schemes}','pdftitle={Conductor strata and nonreduced multiplication failure schemes}')
        t=re.sub(r'\\begin\{abstract\}.*?\\end\{abstract\}',lambda _: '\\begin{abstract}\n'+ABSTRACT+'\n\\end{abstract}',t,flags=re.S)
        t=t.replace(r'\input{parts/01-sharp-conductor.tex}',r'\input{parts/01-sharp-conductor.tex}'+'\n'+r'\input{parts/01a-finite-preliminaries.tex}')
        t=t.replace(r'\input{parts/02-quotient-hilbert.tex}',r'\input{parts/02-quotient-hilbert.tex}'+'\n'+r'\input{parts/02a-higher-defect.tex}')
        t=t.replace(r'\input{parts/03-plane-generators.tex}',r'\input{parts/03-plane-generators.tex}'+'\n'+r'\input{parts/03a-nonreduced-generators.tex}')
        p.write_text(t)
    p=HERE/'applications.tex'; t=p.read_text().replace('Finite quotients\nand primary structures of multiplication failure schemes','Conductor strata\nand nonreduced multiplication failure schemes'); p.write_text(t)
    # Broader, bounded theorem-level attribution. All old references retained.
    p=HERE/'parts/06-finite-literature.tex'; t=p.read_text()
    extra=r'''
\subsection*{Subalgebra varieties, quotient flags, and the additional comparisons}
Iovanov and Sistko \cite[Theorem 0.1]{IS} classify maximal subalgebras
of finite-dimensional algebras over fields under their Schur hypothesis.
In the commutative algebraically closed case, the alternatives include
identifying two residue factors and imposing a first-order condition
at one factor. These closed-point mechanisms are classical and are
not claimed here as new.
Sistko \cite[Definition 3.1, Theorems 1.1 and 4.1]{Sistko} constructs
subalgebra varieties and computes the maximal-subalgebra vanishing
ideal for basic algebras. The distinction needed here is between
such a variety and the full relative quadratic-equation functor:
for $\C[z]/(z^r)$ the latter already has the transverse algebra
$G_r$, of length $\binom r2$. Agreement on the reduced variety does
not identify this thickening.

The Hilbert functor used in Section~\ref{sec:quotient-hilbert} is the
standard functor of locally free quotient algebras; its representability
is not a contribution of this article. Likewise, nested effective
divisors on a curve are classically expressed by a divisor and its
residual divisor. What is established here is the identification
of these functors with specified multiplication Fitting schemes,
the canonical cokernel line \eqref{eq:hyperplane-canonical-line},
and the global-section transports. These are separate assertions
from the classical classification of geometric hyperplanes.

The faithful-action viewpoint is also classical; compare
\cite[Proposition 3.4]{Sistko} for subalgebras of matrix algebras.
Our conductor flags record the \emph{specified inclusion} into $B$,
the action on $B/E$, and its exact-rank scheme structure. A conductor
rank bound alone is not the flag equivalence, nor does either imply
unrestricted base change across an action-rank jump.
The one-variable codimension-two classification is already given
in \cite[Theorem 39]{GLTU}. We use it to locate the fibres of
Example~\ref{ex:conductor-rank-jump}, not as a new classification
of polynomial subalgebras. The quotient-tower statement concerns
arbitrary finite $B$ and its relative exact-rank functors.

In \cite[Example 4.16]{ABHS}, the two-generator jet calculation has
curvilinear target $k[\varepsilon]/\varepsilon^{m+1}$.
Our target in \eqref{eq:fat-algebra} has embedding dimension $e$.
The symmetric-power determinant identity in the proof is classical
linear algebra. Its role is to determine the full primary power of
the tangent determinant, uniformly in $e,h$, and then identify that
power with global section multiplication on $\Pj^e$ using
Theorem~\ref{thm:fat-conductor}. Merely knowing the polygenerator
open would not determine this exponent or the global degree range.
These comparisons identify the inputs and additional claims; they
are not a certificate of exhaustive priority against all literature.

'''
    t=replace_once(t,"Ballico's failure-locus work",extra+"Ballico's failure-locus work")
    p.write_text(t)
    p=HERE/'references.tex'; t=p.read_text()
    refs=r'''
\bibitem{IS} M. C. Iovanov and A. Sistko,
\emph{Maximal subalgebras of finite-dimensional algebras},
arXiv:1705.00762v2 (2017), Theorem 0.1.
\bibitem{Sistko} A. Sistko,
\emph{Automorphism groups of finite-dimensional algebras acting on
subalgebra varieties}, arXiv:1809.09760v2 (2019),
Definition 3.1, Proposition 3.4, and Theorems 1.1 and 4.1.
\bibitem{GLTU} R. Gr\"onkvist, E. Leffler, A. Torstensson, and V. Ufnarovski,
\emph{Describing subalgebras of $K[x]$ using derivatives},
arXiv:2107.11916v1 (2021), Theorem 39, pp.~94--95.
'''
    p.write_text(t.replace(r'\end{thebibliography}',refs+'\n'+r'\end{thebibliography}'))
    oldlabels=set(); newlabels=set()
    for p in paths: oldlabels.update(re.findall(r'\\label\{([^}]+)\}',p.read_text()))
    for p in list(HERE.glob('*.tex'))+list((HERE/'parts').glob('*.tex')): newlabels.update(re.findall(r'\\label\{([^}]+)\}',p.read_text()))
    if oldlabels-newlabels: raise RuntimeError('Old theorem labels lost: '+repr(oldlabels-newlabels))
    manifest={'review_head':REVIEW,'reviewed_product_head':BASE,'branch':BRANCH,
      'old_source_sha256':{str(p.relative_to(OLD)):sha(p) for p in paths},
      'unchanged_active_sources':[str(p.relative_to(OLD)) for p in paths if sha(p)==sha(HERE/p.relative_to(OLD))],
      'old_labels':sorted(oldlabels),'retained_old_label_count':len(oldlabels),'missing_old_labels':sorted(oldlabels-newlabels),
      'new_label_count':len(newlabels-oldlabels),'truncation_lemma_relocated_verbatim':True,
      'historical_sources_modified':False,'priority_certification':False}
    (HERE/'evidence').mkdir(exist_ok=True)
    (HERE/'evidence/PRESERVATION.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    (HERE/'IDENTITY.json').write_text(json.dumps({'version':'A2-v118','branch':BRANCH,
      'controlling_review':REVIEW,'base_product_head':BASE,'primary':'geometry.tex',
      'complete':'paper.tex','applications':'applications.tex','open_priority_item':'E117.1 Ballico 1993 full text'},indent=2)+'\n')
    print(json.dumps({'retained_labels':len(oldlabels),'new_labels':len(newlabels-oldlabels),
                      'unchanged_sources':len(manifest['unchanged_active_sources'])}))
if __name__=='__main__': main()
