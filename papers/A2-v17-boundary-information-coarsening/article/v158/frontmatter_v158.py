"""Front matter and primary-source comparisons for the complete v158 papers."""
II_TITLE='Intrinsic power geometry and singular quadratic pencils'
I_ABSTRACT=r'''An unmarked, ungraded finite multiplication-failure algebra recovers
every complex quadratic pencil at the sharp order $n^2+2n-4$, including
singular pencils. The inverse reconstructs the tensor rulings and
orients them by unequal coefficient-support ranks. Before recovering
the pencil coefficient line, its first relation already determines
the native source projective space. We construct on that space a
source-normalized determinant-apolar algebra bundle and its projective
power diagram, functorially under arbitrary ungraded algebra
isomorphisms. Scalar twists cancel in the algebra bundle, so no
splitting of an auxiliary normalization fibre is used. The relative
inverse and the detailed geometric and local forms are included.'''
I_INTRO=r'''\section{Introduction}
\label{sec:paper-i-v158}
Let $V$ be a complex vector space of dimension $n\geq3$, and let
$R\subset\Sym^2V$ be a two-dimensional subspace. Put
$N=\binom{n+1}{2}$, $p=N-2$, and $d=n+2p=n^2+2n-4$.
The universal graph matrix $T$ and the quotient map $\gamma_R$ define
\[
 A_R=\C[t_{ij}]/\bigl((\det T)I_p(\gamma_R\Sym^2T)
                                      +\mathfrak m^{d+1}\bigr).
\]
The central result is the sharp equivalence
\[
 A_R\simeq A_{R'}\text{ as ungraded, unmarked algebras}
 \quad\Longleftrightarrow\quad R'=gR\quad(g\in\PGL(V)).
\]
Every lower truncation is independent of $R$
(Theorems~\ref{thm:artin-local-inverse-v146} and
\ref{thm:sharp-finite-pencil}). No regularity hypothesis is imposed
on the pencil.

\subsection{From the first relation to the source}
Multiplication recovers the cotangent space $E$ and its first relation
$H\subset\Sym^dE$. The determinant support of $H$ recovers the two
rank-one rulings; the residual coefficient module orients them by
support ranks $(1,\binom N2)$. The remaining coefficient line is the
Pluecker line of the pencil. This is the order of the inverse, and it
has a further consequence before the last step is performed.

Theorem~\ref{thm:intrinsic-envelope-v158} constructs from the oriented
source $S_A$ a finite algebra bundle
\[
 \mathscr B_{A,h}=\bigoplus_{j=0}^{nh}
                    B_h(V)_j\otimes\OO_{\Pj(V)}(2j),
 \qquad S_A=\Pj(V).
\]
Changing a linear lift by a line twists the two factors oppositely.
The bundle and the projective multiplication diagram therefore depend
on $A$, not on the lift. This is an intrinsic envelope constructed
from multiplication, not a claim of a preferred subquotient of $A$.
In particular it is not obtained by choosing an $n$-plane in the
$n^2-1$ dimensional coefficient complement of a common divisor-boundary
fibre. Those two constructions have different inputs and different
equivariant meanings.

\subsection{Relation to the companion paper}
The sharp inverse, its finite order, the source functor, and the
cancellation of scalar twists are proved here without the power-graph
or spectral results of the companion paper. Identifying the envelope's
projective graph with complete quadrics uses the companion's universal
ideal and graph theorems. Conversely those algebraic theorems and its
classification data for a given symmetric pencil do not use the inverse
proved here. Only their interpretation as functors of an unmarked
failure algebra invokes our source and pencil extraction. Thus the
core inverse and the core power theory have independent proofs; the
intrinsic-envelope application links them and is not claimed to have
no cross-paper inputs.

The main argument consists of the first-relation principle, tensor
rulings, coefficient extraction, sharpness and the local inverse. The
relative and source-bundle results keep their full statements.
The appendices retain the detailed recognition, covering, stack and
spectral extensions, with their dependencies explicit; they are not
additional premises of the sharp inverse. Their retention does not
require a reader to use them in proving the principal theorem.
The theorem-level comparison with Ballico's failure-locus paper
\cite{Ballico93} remains documentary-limited. No claim about its
anticipation or nonanticipation is inferred from unavailable full text.
'''
II_ABSTRACT=r'''The multiplication powers in a determinant-apolar algebra have
coefficient ideals equal, over every complex base algebra, to balanced
products of symmetric minor ideals. We identify the entire power graph
on each fixed-rank locus with relative complete quadrics over the
Grassmannian of image planes. For arbitrary symmetric pencils, boundary
contacts and finitely many multiplication-syzygy maps recover both
spectral elementary divisors and Kronecker minimal indices. Their
contact degrees and image-plane degree satisfy a global conservation
law. We compute a transverse corank-two Hilbert limit in every dimension:
it is a reduced nodal curve with one exceptional tail, selected by a
single power ideal, and all multiplication maps on that tail are
determined. The normalization-fibre origin of the auxiliary algebra and
the choice-free source envelope of a failure algebra are kept distinct.'''
II_INTRO=r'''\section{Introduction}
\label{sec:paper-ii-v158}
Let $V$ have dimension $n$ and put
\[
 B_h(V)=\Sym(\Sym^2V)/\langle(v^2)^{h+1}:v\in V\rangle,
 \qquad h\geq1.
\]
For a symmetric matrix $A$, let $J_p(A)$ be the coefficient ideal of
its $p$th power in this algebra. Its universal identity is
\[
 J_{hq+s}(A)=I_q(A)^{h-s}I_{q+1}(A)^s,\qquad0\leq s<h,
\]
where $I_q$ is the ideal of $q$-minors. Equality is of ordinary ideals
over every commutative complex algebra, not merely of radicals,
integral closures, or closed-point zero sets
(Theorem~\ref{thm:universal-power-v157}). Proposition
\ref{prop:coefficient-conventions-v158} specifies its dual coefficient
map and every projective twist.

\subsection{The power graph at every rank}
On the rank-$r$ locus, keep all nonzero powers through $hr$.
The last power recovers the image $r$-plane by its degree-$2h$ Pluecker
map. The whole graph closure is consequently
\[
 \mathcal G_{r,h}=\mathrm{CQ}(\mathcal U)
                   \longrightarrow\Gr(r,V),
\]
where $\mathcal U$ is tautological
(Theorem~\ref{thm:all-rank-graph-v158}). This is an equality of graph
schemes, without a subsequent normalization, and is independent of
$h$. The underlying complete-quadric varieties and their classical
boundary geometry are not new; the assertion identifies their full
image-plane projection and scheme structure through powers in one
fixed finite algebra.

\subsection{Singular pencils and a global degree identity}
For a pencil of normal rank $r$, write
$K=\bigoplus_a\OO(-\varepsilon_a)$ for its kernel bundle on the
parameter line. The nullities $\kappa_j$ of the finite coefficient
maps $C_j$ determine the minimal indices by
\[
 \#\{a:\varepsilon_a=j\}=\kappa_j-2\kappa_{j-1}+\kappa_{j-2}.
\]
The relative complete-quadric contact divisors $D_i$ determine the
positive Smith exponents at their supported spectral points, including
the points' projective positions. Together these give the full complex
congruence data, with no regularity restriction. Moreover
\[
 \sum_{i=1}^{r-1}(r-i)\deg D_i
       +2\deg(\Lambda\longrightarrow\Gr(r,V))=r,
 \qquad \deg(\Lambda\longrightarrow\Gr(r,V))=\sum_a\varepsilon_a
\]
(Theorem~\ref{thm:singular-complete-data-v158}). The kernel maps carry
information genuinely missing from power contacts: the constant-rank
pencils $S_0\oplus S_2$ and $S_1\oplus S_1$ have identical empty
contact divisors but different first syzygy nullities. The classical
Kronecker congruence classification is an input to the interpretation,
not a new classification theorem claimed here.

\subsection{An explicit Hilbert boundary}
For the normal main-component incidence compactification, we specify
its embedded-flat-closure universal property and calculate the family
\[
 \diag(s,s+\tau t,t-a_3s,\ldots,t-a_ns).
\]
The lifted generic curve has special fibre a reduced nodal union of the
lifted special pencil and an exceptional projective line. On the total
base the power ideal $J_{h(n-2)+1}$ is exactly $(s/t,\tau)$.
Its blow-up creates the tail. The remaining power maps restrict to
complete Veronese systems of degrees $\min\{b,2h-b\}$, where
$p=h(n-2)+b$. Thus the multiplication equations determine both the
exceptional component and all its power linear systems
(Theorem~\ref{thm:hilbert-tail-v158}). This is a family calculation;
the limiting closed algebra alone does not specify the direction of
its degeneration.

\subsection{Intrinsic origin and dependencies}
The algebra $B_h(V)$ has two constructions that must not be conflated.
It occurs as a quadratic coefficient section of a reciprocal
normalization fibre after a splitting has been chosen. Independently,
the first relation of a sharp failure algebra recovers its own source
projective space. The companion's Theorem
\ref{thm:intrinsic-envelope-v158} constructs there a choice-free
source-normalized algebra bundle and the projective power diagram.
It does not select a native $n$-space inside the auxiliary complement
of dimension $n^2-1$, and it does not assert a preferred quotient of
the original finite algebra. The ideal, graph, singular-pencil and
Hilbert-tail arguments here start with $V$ and a pencil, and are
independent of the sharp inverse. Their final interpretation for an
unmarked failure algebra uses that companion theorem explicitly.

Determinant apolarity, multiplicity-free invariant ideals, determinantal
balancing, complete quadrics and symmetric congruence normal forms are
classical inputs. The exact theorem-level comparisons appear in
Section~\ref{sec:power-conventions-v158}; the multiplier formula is
recorded only as a consequence of the classical determinantal result.
The later sections retain the finite-flat binary factorization,
squarefree conductors, collision incidence charts, and reciprocal-fibre
homology. A coefficient section is not the full fibre, and an incidence
atlas is not a classification of all its analytic singularities.
The theorem-level Ballico comparison \cite{Ballico93} remains limited
by unavailable full text; there is no historical nonanticipation claim
based on that absence.
'''
MASTER_ABSTRACT=I_ABSTRACT+'\n'+r'''The companion theory identifies all fixed-rank apolar power graphs,
recovers the elementary divisors and minimal indices of arbitrary
pencils, and computes a reduced corank-two Hilbert tail with all its
power maps. This preservation master contains both papers, their
complete inherited proofs and their technical extensions with unified
numbering; it is not a third submission.'''
MASTER_INTRO=r'''\section{Introduction}
\label{sec:introduction-v153}
This paired manuscript has two logically separated cores. The first
is the sharp inverse for every unmarked quadratic-pencil failure
algebra. The second is the universal ideal and all-rank power geometry
of a determinant-apolar algebra. Their intrinsic link is the source
projective space extracted from the first relation before the pencil
coefficient line is recovered. A source-normalized algebra bundle
cancels the scalar ambiguity and supplies the native projective power
diagram (Theorem~\ref{thm:intrinsic-envelope-v158}). This link does not
use an auxiliary splitting of a reciprocal normalization fibre.

The all-rank graph theorem identifies its Grassmannian image-plane
projection and complete-quadric structure
(Theorem~\ref{thm:all-rank-graph-v158}). For arbitrary pencils the
contact divisors, syzygy nullities and their degree conservation law
recover all complex congruence data
(Theorem~\ref{thm:singular-complete-data-v158}). A transverse
corank-two family has an explicit reduced nodal Hilbert limit; one
power ideal creates the exceptional tail and the other powers give
its complete linear systems (Theorem~\ref{thm:hilbert-tail-v158}).
These statements extend the regular-pencil analysis without altering
the sharp inverse or discarding the previous divisor and fibre theory.

The two focused papers contain individual introductions and explicit
logical dependency statements. This master preserves their full
mathematical bodies. Classical complete-quadric, invariant-ideal and
canonical-form ingredients are identified at their point of use.
The Ballico comparison \cite{Ballico93} remains documentary-limited;
no nonanticipation conclusion is based on unavailable text.
'''
BIB=r'''\bibitem{CasarottiCornianiMassarenti2023}
A. Casarotti, E. Corniani and A. Massarenti,
\emph{Complete singular collineations and quadrics},
International Mathematics Research Notices \textbf{2023} (2023),
no.~18, 15370--15407. DOI: 10.1093/imrn/rnac271.
The cited construction is also in arXiv:2111.02940,
Definition~2.5, Remark~2.6 and Theorem~2.14.

\bibitem{Thompson1991}
R. C. Thompson, \emph{Pencils of complex and real symmetric and skew
matrices}, Linear Algebra and its Applications \textbf{147} (1991),
323--371. DOI: 10.1016/0024-3795(91)90238-R.
'''
DISCLOSURE=r'''\paragraph{Scope of the new intrinsic construction.}
The source-normalized envelope is an algebra bundle with an intrinsic
projective power diagram. It is not a claimed preferred subquotient
of the sharp failure algebra. Singular-pencil classification is read
through the classical complex symmetric Kronecker form. The explicit
Hilbert tail is a boundary calculation for the stated transverse
family, not a classification of every fibre of the incidence
compactification. Exact computations accompanying the source check
finite instances; they do not certify the general proofs.
'''
