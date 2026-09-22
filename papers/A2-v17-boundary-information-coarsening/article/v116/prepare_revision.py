#!/usr/bin/env python3
"""Materialize v116 from the pinned v115 tree. Never modifies the old tree."""
from pathlib import Path
import hashlib, json, re, shutil, subprocess
R=Path(__file__).resolve().parent
S=R.parent/'v115'
REVIEW='1cb4e00c86699247454d21dbec2dcce01a9c6b8b'
BASE='acfd3d57e0053e1b03df53020fd8e79e14599c03'
ROOT=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=R,text=True).strip())
if not S.is_dir(): raise RuntimeError('Pinned v115 source directory is required')
for p in S.rglob('*'):
    if not p.is_file(): continue
    rel=p.relative_to(S)
    if rel.parts[0] in ('evidence','crossrefs') or '__pycache__' in rel.parts: continue
    if p.suffix in ('.pdf','.log','.fls','.aux','.out','.toc'): continue
    target=R/rel
    if not target.exists():
        target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,target)
manifest={}
for p in sorted(S.rglob('*.tex')):
    rel=p.relative_to(S)
    if 'history' in rel.parts: continue
    raw=subprocess.check_output(['git','show',BASE+':'+str(p.relative_to(ROOT))],cwd=ROOT)
    if raw!=p.read_bytes(): raise RuntimeError('v115 source differs from frozen review: '+str(rel))
    target=R/'history/v115_source'/rel; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(raw)
    manifest[str(rel)]=hashlib.sha256(raw).hexdigest()
if len(manifest)!=24: raise RuntimeError('Unexpected reviewed TeX manifest size')
for name in ('README.md','LITERATURE_AUDIT.md','PROOF_AUDIT.md','RESPONSE_TO_R114.md','PRESERVATION_AND_DEPENDENCIES.md','AI_ASSISTANCE_AND_PROVENANCE.md','verify_revision.py','make_receipts.py','build.sh'):
    shutil.copy2(S/name,R/'history'/('v115_'+name))
shutil.copy2(S/'evidence/V114_SOURCE_MANIFEST.json',R/'history/v115_V114_SOURCE_MANIFEST.json')
report='reviews/a2-v115-independent-harsh-top4-2026-09-22/REFEREE_REPORT.md'
(R/'history/R115_REFEREE_REPORT.md').write_bytes(subprocess.check_output(['git','show',REVIEW+':'+report],cwd=ROOT))
(R/'evidence').mkdir(exist_ok=True)
(R/'evidence/V115_SOURCE_MANIFEST.json').write_text(json.dumps({'review_commit':REVIEW,'reviewed_revision_commit':BASE,'mathematical_source_commit':'426d112c574f5d3289f6c7d4ecb5f0328ac040b5','tex_sha256':manifest},indent=2)+'\n')
for name in ('paper.tex','geometry.tex','applications.tex','references.tex','parts/00-introduction.tex','parts/02j-higher-hyperplane-classification.tex','parts/06-priority-and-application.tex'):
    (R/name).write_bytes((S/name).read_bytes())
p=R/'parts/00-introduction.tex'
p.write_text(p.read_text().replace('\\section{Introduction}','\\section{The quadratic family and the polar residual framework}',1))

HYPERPLANE=r'''\begin{lemma}[Explicit plane-derivative matrix and residual span]
\label{lem:hyperplane-explicit-matrix}
Use the monomials $z_j=X^jY^{n-j}$. At a split secant take
\[
 a=z_0+\lambda z_n,\quad (w_1,\ldots,w_{n-1})=(z_1,\ldots,z_{n-1}),
 \quad v=z_n,\quad\lambda\ne0,
\]
and let the annihilator be coefficient $mn$ minus $\lambda^m$
times coefficient zero. At a tangent secant take $a=z_0$,
$(w_1,\ldots,w_{n-1})=(z_2,\ldots,z_n)$, $v=z_1$, and the
coefficient-one annihilator. Set $u_0=a$, $u_i=w_i$, and vary
$u_i$ by $t_i v$. On the ordered source quotient
\[
 a^m,w_1a^{m-1},\ldots,w_{n-1}a^{m-1}
\]
the plane-derivative matrix is
\begin{equation}\label{eq:hyperplane-explicit-diagonal}
       \kappa\,\operatorname{diag}(m,1,\ldots,1),\qquad
       \kappa=\lambda^{m-1}\ \text{or}\ 1,
\end{equation}
respectively. It is zero on all monomials with at least two $w$
factors. Their product image has dimension $mn-3$ in both cases.
\end{lemma}
\begin{proof}
Let $\ell$ be the indicated annihilator. Then
$\ell(va^{m-1})=\kappa\ne0$. The variation of $a^m$ gives
$m\kappa t_0$. For $w_i a^{m-1}$ only variation of $w_i$ can
contribute to $\ell$, giving $\kappa t_i$; all terms which retain
$w_i$ vanish. For a monomial with at least two $w$ factors one
such factor remains after every single variation, and the result
is annihilated by $\ell$. This gives every entry of
\eqref{eq:hyperplane-explicit-diagonal}.

In the split case $W=XYV_{n-2}$, so
$W^2=(XY)^2V_{2n-4}$. The subseries $U=W+\C a$ is
base-point-free: $W$ has only the two endpoint base points, and
$a$ is nonzero at both. Since $2n-4\ge n-1$ for $n\ge4$,
Lemma~\ref{lem:hyperplane-propagation} can be applied successively
at degrees $2n-4,3n-4,\ldots$, proving
$W^2U^{m-2}=(XY)^2V_{mn-4}$.

In the tangent case the exponent set of $W^2$ is the entire
integer interval $[4,2n]$. If the exponent set at degree $k$ is
$[4,kn]$, adding the exponent set $\{0\}\cup[2,n]$ of $U$
gives $[4,kn]\cup[6,(k+1)n]=[4,(k+1)n]$, since $kn\ge5$.
Induction from $k=2$ proves the assertion in every degree.
There are exactly $mn-3$ exponents in $[4,mn]$.
\end{proof}

'''
ASSOCIATED=r'''\begin{lemma}[The length-two radical, including a double point]
\label{lem:hyperplane-confluent-radical}
Let $0\ne\ell\in V_{2n}^*$ and let
$H_\ell(f,g)=\ell(fg)$ on $V_n$. If $H_\ell$ has rank two,
there is a length-two divisor $Z\subset\Pj^1$ such that
\[
 \ell\in H^0(\mathcal O_Z(2n))^*\subset V_{2n}^*,\qquad
 \operatorname{rad}H_\ell=H^0(\mathcal O(n)(-Z)).
\]
The induced pairing on $H^0(\mathcal O_Z(n))$ is nondegenerate.
\end{lemma}
\begin{proof}
The rank-at-most-two Hankel variety is the secant variety of the
evaluation rational normal curve. The shape-independence of the
Hankel minor ideal and the precise secant parametrization are given
in \cite[Section 1 and Section 2, equation (2.0.1)]{CMSV}; here the
minor size is three. The projective bundle of the spaces
$H^0(\mathcal O_Z(2n))^*$ over $\operatorname{Hilb}^2\Pj^1$ is
proper. Its image contains the distinct-point secant lines and is
contained in the rank-at-most-two locus by factorization through a
two-dimensional restriction space. Its image is therefore the
entire secant variety, including tangent lines. Thus $\ell$
factors through some $Z$.

For two distinct points the pairing on the length-two algebra has
matrix $\operatorname{diag}(\alpha,\beta)$. Rank two forces
$\alpha\beta\ne0$. For $Z=2p$, choose a parameter $z$ and
trivialize the line bundle. Write
$\ell(A+Bz)=\alpha A+\beta B$ on $\C[z]/(z^2)$. The pairing
matrix in the basis $1,z$ is
$\left(\begin{smallmatrix}\alpha&\beta\\\beta&0\end{smallmatrix}\right)$,
which has rank two exactly when $\beta\ne0$. Restriction
$V_n\to H^0(\mathcal O_Z(n))$ is surjective. In either case the
kernel of the pulled-back nondegenerate pairing is exactly its
restriction kernel $H^0(\mathcal O(n)(-Z))$.
\end{proof}

\begin{lemma}[Equivariant associated points on a transitive curve]
\label{lem:equivariant-associated-curve}
Let a group act on a Noetherian variety, preserving an ideal
$\mathcal J$ with irreducible reduced support $S$. Let $C\subset S$
be a closed irreducible curve on whose closed points the group acts
transitively. Suppose $\mathcal J=\mathcal I_S$ away from $C$
and the nonzero module $\mathcal N=\mathcal I_S/\mathcal J$
has support exactly $C$. Then
\[
       \operatorname{Ass}(\mathcal O/\mathcal J)
                     =\{\eta_S,\eta_C\}.
\]
\end{lemma}
\begin{proof}
For a finite module over a Noetherian ring, associated primes are
finite, minimal points of its support are associated, and the
associated primes of a submodule are associated to the ambient
module; see \cite[Lemma 10.63.3, Lemma 10.63.5,
and Proposition 10.63.6]{StacksAssociated}. These assertions apply
on a finite affine cover and give the corresponding coherent-sheaf
statements. Associated points outside $C$ consist only of $\eta_S$,
since the quotient there is the structure sheaf of a reduced
irreducible variety. An associated point with closure inside $C$
is either $\eta_C$ or a closed point. The finite associated set is
preserved by the group action. Transitivity on the infinitely many
closed points of $C$ excludes the latter possibility. Finally
$\eta_C$ is a minimal point of the support of $\mathcal N$, hence
is associated to $\mathcal N$ and therefore to
$\mathcal O/\mathcal J$. The minimal point $\eta_S$ is associated
as well. This gives exactly the two asserted points.
\end{proof}

The coordinate assertion in
Lemma~\ref{lem:hyperplane-residual-smoothness} is supplied by
\eqref{eq:hyperplane-explicit-diagonal}. The length-two assertion
and the associated-point step of the following proof are, respectively,
Lemma~\ref{lem:hyperplane-confluent-radical} and
Lemma~\ref{lem:equivariant-associated-curve}. We retain the full
argument to specify where its nilpotence estimate is used.

'''
BIB=r'''\bibitem{StacksAssociated} The Stacks Project Authors, \emph{The Stacks Project}, Section 10.63, Tag 00L9; Lemmas 10.63.3 and 10.63.5 and Proposition 10.63.6, associated primes; consulted September 22, 2026.'''
abstract='''For binary subseries containing the sections vanishing on a finite divisor, we identify the higher-multiplication cokernel with a finite-algebra cokernel, in families and after arbitrary base change. For generating contact pencils this gives the entire failure scheme in every degree. Above the contact-length threshold the ideal stabilizes and has an explicit primary decomposition for every multiplicity partition of the divisor. We determine all coranks, exact nilpotency indices, successive nilradical quotients, and local weighted-arrangement equations. Although fixed-contact fibres can be highly nonreduced, the moving-contact failure divisor is integral. Its normalization is the smooth finite incidence marking a length-two subdivisor not separated by the pencil; an explicit differential criterion determines its singular support, including collisions. These results apply to subseries of arbitrarily large codimension. We also retain the quadratic binary component classification, polar residual equations and wall singularities, and the all-degree hyperplane theorem with its embedded evaluation curve. Complete information-recovery and statistical applications are reproduced in separate appendices.'''
lead='\n'.join(r'\input{parts/'+x+'}' for x in ('00a-conductor-introduction.tex','00c-conductor-reduction.tex','00d-contact-primary-structure.tex','00e-moving-contact-normalization.tex'))+'\n'
for name in ('paper.tex','geometry.tex'):
    p=R/name; s=p.read_text()
    lines=[r'\title[Conductor reduction and multiplication failure]{Conductor reduction and primary structures\\of multiplication failure schemes}' if x.startswith('\\title[') else x for x in s.splitlines()]
    s='\n'.join(lines)+'\n'
    s=re.sub(r'\\begin\{abstract\}[\s\S]*?\\end\{abstract\}',lambda match:'\\begin{abstract}\n'+abstract+'\n\\end{abstract}',s,count=1)
    s=s.replace(r'\input{parts/00-introduction.tex}',lead+r'\input{parts/00-introduction.tex}',1)
    s=s.replace('pdftitle={Residual geometry and singularities of multiplication failure schemes}','pdftitle={Conductor reduction and primary structures of multiplication failure schemes}')
    s=s.replace(r'\subjclass[2020]{14M12, 14B05, 14H50, 14N15, 35R30, 62B15}',r'\subjclass[2020]{14M12, 14H50, 13C40, 14B05, 14N15}')
    s=s.replace(r'\keywords{Multiplication of sections, polar residual spaces, singular schemes, Hankel forms, orthogonal Grassmannians, ordinary double crossings}',r'\keywords{Multiplication of sections, finite contact algebras, primary decomposition, normalization, nilpotent structures, polar residual spaces}')
    p.write_text(s)
p=R/'applications.tex'
p.write_text(p.read_text().replace('Residual geometry\nand singularities of multiplication failure schemes','Conductor reduction\nand primary structures of multiplication failure schemes'))
p=R/'parts/06-priority-and-application.tex'
s=p.read_text().replace("Its publisher's first page has been inspected: it\nintroduces", "The preceding source audit inspected its publisher's first page, which\nintroduces")
insert=r'''
\subsection{Contact-algebra reduction and the scope of the new classification}
Theorems~\ref{thm:conductor-reduction}--\ref{thm:moving-normalization}
concern the entire relative generating Grassmannian
$X_{d,2}^\circ$, including all multiplicity partitions of its
length-$d$ divisor. The subseries have codimension $d-2$; $d$ is
arbitrary. For this family the result is a complete scheme theorem,
not only a two-point annihilator sector: the component ideals,
primary exponents, absence of embedded points, nilpotent layers,
all coranks, and moving-divisor normalization are explicit.
The marked length-two divisor in the normalization is recovered
from the failure scheme; it is not imposed on the parameter space
as a restriction to one preselected obstruction sector.

The determinant of a power basis, the Vandermonde and confluent
Vandermonde identities, and the change-of-basis formula for
discriminants are elementary classical identities; no priority is
claimed for those identities. Their proofs are included to fix all
multiplicities, including at nonreduced contacts. The exact
multiplication-cokernel transport in
Theorem~\ref{thm:conductor-reduction} is what permits these identities
to describe the original maximal-minor scheme after arbitrary
base change. The resulting primary decomposition is not inferred
from an order-of-vanishing lower bound.

For a precise comparison, \cite[Theorem 0.2 and Proposition 2.2]{Ballico96}
are existence results for deficient finite linear sections of a
fixed completely embedded surface. Those statements do not contain
the contact-pencil primary formula or the normalization constructed
here. This observation is a comparison of the specified statements,
not a claim about all work on failure loci. The theorem pages of
\cite{Ballico93} have still not been obtained, so its comparison
remains explicitly undetermined. The accompanying source audit
records the parameter-space, degree, scheme, corank, and associated-prime
questions separately; a missing source is not treated as evidence
of novelty.

'''
s=s.replace(r'\section{An application to calibrated information recovery}',insert+r'\section{An application to calibrated information recovery}',1)
p.write_text(s)
p=R/'parts/02j-higher-hyperplane-classification.tex'; s=p.read_text()
s=s.replace('\\begin{lemma}[Scheme smoothness off the evaluation curve]',HYPERPLANE+'\n\\begin{lemma}[Scheme smoothness off the evaluation curve]',1)
s=s.replace('\\begin{proof}[Proof of Theorem~\\ref{thm:higher-hyperplane-global}]',ASSOCIATED+'\n\\begin{proof}[Proof of Theorem~\\ref{thm:higher-hyperplane-global}]',1)
p.write_text(s)
p=R/'references.tex'
p.write_text(p.read_text().replace('\\end{thebibliography}',BIB+'\n\\end{thebibliography}',1))
p=R/'parts/00d-contact-primary-structure.tex'
p.write_text(p.read_text().replace('The coordinate ring of the frame space is an open localization of\na polynomial ring.','On each affine frame chart the coordinate ring is a localization of\na polynomial ring.'))
p=R/'parts/00c-conductor-reduction.tex'
p.write_text(p.read_text().replace('condition is open in a family.\n','condition is open in a family. In relative notation, $\\pi$ denotes\nthe projection from $\\Pj^1$ times the parameter space; all bundles\nare pulled back to the indicated relative Grassmannian when needed.\n'))
print('Prepared v116; all 24 reviewed TeX files pinned and archived')
