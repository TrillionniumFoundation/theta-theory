"""Revision 161 front matter; replaced introductions remain in the archive."""
I_ABSTRACT=r'''We prove that an unmarked, ungraded finite local algebra associated
with a complex quadratic pencil determines the pencil up to congruence.
The truncation order $n^2+2n-4$ is sharp, and no regularity assumption
is imposed. Multiplication recovers the first relation, its determinant
rulings, and the orientation that identifies the pencil coefficient
line. The construction extends to families over arbitrary complex
bases. On the effectively rigidified failure stack, the recovered
source carries a scalar-normalized apolar algebra bundle. The associated
multiple-incidence boundary admits explicit multi-Rees equations and
relative lifting conditions. The sharp inverse is proved independently
of this boundary application; its relative, covering, recognition,
and spectral extensions are retained in the appendices.'''
I_INTRO=r'''\section{Introduction}
\label{sec:paper-i-v161}
Let $V$ be a complex vector space of dimension $n\geq3$, and let
$R\subset\Sym^2V$ have dimension two. Set $N=\binom{n+1}{2}$,
$p=N-2$, and $d=n+2p=n^2+2n-4$. The universal graph matrix $T$ and
the quotient map $\gamma_R$ define the finite local algebra
\[
 A_R=\C[t_{ij}]/\bigl((\det T)I_p(\gamma_R\Sym^2T)
                                  +\mathfrak m^{d+1}\bigr).
\]
Our principal assertion is
\[
 A_R\simeq A_{R'}\text{ as unmarked, ungraded algebras}
       \quad\Longleftrightarrow\quad R'=gR\quad(g\in\PGL(V)).
\]
Every smaller truncation is independent of the pencil
(Theorems~\ref{thm:artin-local-inverse-v146} and
\ref{thm:sharp-finite-pencil}). This includes singular pencils.
Neither a chosen grading nor a preferred system of generators is
part of the input.

\subsection{The inverse}
The maximal ideal filtration recovers the cotangent space and the
first nonzero relation space. The common determinant divisor of
that relation recovers the two tensor rulings. The residual
coefficient module distinguishes them by unequal support ranks;
its remaining coefficient line is the Pluecker line of $R$.
The proof must show that each of these operations survives ungraded
isomorphisms, including nonlinear generator changes. The first seven
sections give this argument and its sharpness. The scheme-level
coefficient map is a closed immersion over arbitrary complex bases
(Theorem~\ref{thm:finite-parameter-immersion}), which also gives the
family form of the inverse.

The main proof ends with the coefficient-support orientation and
local algebra inverse. The appendices contain all relative,
covering, recognition, rigidification, and spectral extensions,
together with their proofs. They are not additional hypotheses of
the sharp inverse. This separates the central reconstruction
argument from consequences that require further geometric inputs.

\subsection{An effective boundary application}
The sharp first relation already determines the source projective
space before the final pencil-coefficient step. Its first-jet
bundle and Cartan relations define a source-normalized algebra
bundle. Scalar weights cancel, so this construction descends on
projective source torsors even when a global $\OO(1)$ does not exist.
Proposition~\ref{prop:envelope-stack-v161} states the resulting
morphism of stacks. It is made on the effective pencil-failure
stack, after the two specified ineffective kernels are divided out,
and not on the stack of all Artin algebras of the same length.
The case $h=1$ requires no extra exponent. The envelope is not
asserted to be a subquotient of $A_R$.

The companion computes the full Hilbert modification over the open
of regular pencils with any number of distinct reduced corank-two
incidences and no higher corank. Its exact centre is
$\Fitt_0(q_*\OO_D)$, where $D$ is the zero scheme of $J_{n-1}$ on
the intrinsic pencil line. Etale locally the centres have independent
parameters $(u_i,v_i)$. Theorem~\ref{thm:boundary-stack-v161} gives
the multi-Rees equations $v_iU_i-u_iV_i$ and descends the computed
modification to the effective stack. Proposition
\ref{prop:relative-obstructions-v161} describes the obstruction to
lifting a \emph{fixed} small base deformation by the classes
$[v_i'-u_i'\widetilde w_i]\in J/u_i'J$. This relative question is
different from the unobstructed absolute deformation problem on a
smooth quotient stack. It is also different from the local
hypersurface deformation module of a singular universal curve.

The recovered pencil line remains an essential intermediate object
of this application. A closed algebra determines the space of
boundary directions; a family supplies its chosen direction. The
multi-Rees equations and relative lifting conditions make the
boundary calculation explicit without attributing to the closed
algebra a direction that it does not contain.

\subsection{Dependencies and historical scope}
The sharp inverse uses neither complete quadrics nor the Hilbert
boundary theorem. Conversely, the companion's power-ideal and
boundary proofs begin with a vector space and a pencil and do not
use this inverse. Their interpretation as invariants of unmarked
failure algebras uses our source and pencil reconstruction. The
applications state these cross-paper inputs rather than hiding them
in embedded numerical references.

Classical symmetric-pencil completeness is accessible in
\cite[Theorem~2.1]{DeTeranDmytryshynDopico2018v161}. A minimal-index
block has size $2\varepsilon+1$, explaining the finite range of
syzygy maps. Both spectral positions and their local partitions are
needed, modulo one common projective reparametrization.
Ballico's available quadratic-normality failure-cycle theorem
\cite[Theorem~0.2]{Ballico1996v161} concerns existence of finite
subschemes explaining a failure on a projective surface; it is not
used as a reconstruction theorem here. This comparison does not
replace the still unavailable theorem/proof-level text of
\cite{Ballico93}. The latter comparison remains documentary-limited;
no claim of anticipation or nonanticipation is inferred from it.
'''
II_TITLE='Power ideals and the Hilbert boundary of quadratic pencils'
II_ABSTRACT=r'''We identify the normalized Hilbert graph of lifted quadratic pencils
on the full reduced corank-two incidence open with a Fitting-ideal
blow-up. At a pencil with $k$ incidence points its entire fibre is
$(\mathbf P^1)^k$, and the universal curve is a reduced nodal tree.
Independence of the incidence centres follows from the radicals of
distinct pencil members, without an extra genericity hypothesis.
For symmetric Jordan slices of every contact order $m\geq2$, we
compute the normalized Hilbert modification and its nonreduced
curves: a main component meets an $m$-fold tail along a length-$m$
scheme. The total multiplication graph has transverse singularity
$A_{m-1}$. After ramified base change its normalization gives a
stable-map tail of degree $m$, distinguishing the Hilbert and stable
limits with the same cycle. The proofs use an exact power-ideal
identity over arbitrary complex algebras. All-rank power graphs,
singular-pencil data, and the complete earlier collision and
reciprocal-fibre results are included in the appendices.'''
II_INTRO=r'''\section{Introduction}
\label{sec:paper-ii-v161}
A limiting pencil does not in general determine the embedded limit
of its lift to complete quadrics. Even when the base modification
is smooth, its universal Hilbert curve may be nonreduced and its
total space singular. We determine these phenomena on the full
reduced corank-two incidence open and on explicit nonreduced-contact
slices of every order.

\subsection{The full reduced-incidence modification}
Let $G=\Gr(2,\Sym^2V)$, $n=\dim V\geq3$, and let $U_{\rm red}$
be the open of regular pencils that avoid rank at most $n-3$ and
whose intersections with rank at most $n-2$ are reduced. The number
of intersection points is unrestricted. With $q:D\to U_{\rm red}$
the finite incidence scheme, our principal identification is
\[
 \widehat G|_{U_{\rm red}}
       \simeq\operatorname{Bl}_{\Fitt_0(q_*\OO_D)}U_{\rm red}
\]
(Theorem~\ref{thm:multiple-incidence-v161}). The left side is the
normalization of the reduced graph closure of lifted pencil curves
in the specified Hilbert scheme. Its fibre at a $k$-incidence pencil
is the whole scheme $(\Pj^1)^k$. Each factor parametrizes lines
through a fixed point in an ambient exceptional $\Pj^2$; the
parameter factor and the ambient plane are different spaces.
The corresponding curve has one main component and $k$ independently
attached embedded tails. Its nodal local equations are
$x_i y_i=t_i$, with independent exceptional parameters $t_i$.

The local arrangement is not assumed to be transverse. Lemma
\ref{lem:independent-radicals-v161} proves the needed independence
for every pencil in this open: radicals at distinct spectral points
lie in a direct sum, and an arbitrary symmetric variation prescribes
the forms on those radicals independently. The general
transverse-incidence lemma is stated separately, so the classical
blow-up mechanism is not confused with this pencil calculation.
The product description gives every fibre and every local boundary
intersection, rather than a family contained in one fibre.

\subsection{Nonreduced contact and the universal singularity}
For every $m\geq2$, a two-parameter family of $2m$-dimensional
symmetric linear pencils has exact residual Schur complement
\[
 \begin{pmatrix}x^m+u&v\\v&x^m-u\end{pmatrix}.
\]
The special pencil has contact length $m$ and local Smith exponents
$m,m$. The normalized graph of this \emph{slice} is
$\operatorname{Bl}_0\A^2$. In the chart $u=t,v=tw$, its universal
curve is the blow-up of $(x^m,t)$, with exact Rees equation
$tU-x^mV=0$ (Theorem~\ref{thm:contact-hilbert-v161}). The special
curve is $C_0\cup T_m$, where
\[
 T_m=\Pj^1_{\C[x]/(x^m)},\qquad
 C_0\cap T_m=\Spec\C[x]/(x^m).
\]
It has no embedded associated points but is nonreduced. Its total
space has transverse equation $x^m=tz$ and hence singularity
$A_{m-1}$, with local cotangent deformation space of dimension
$m-1$ (Proposition~\ref{prop:contact-deformations-v161}).
These assertions include arbitrarily high contact order in genuine
linear pencils; they are not residual tangencies on an already
reduced single-contact exceptional plane.

After $t=s^m$, normalization produces an ordinary point blow-up and
a reduced stable-map tail mapping with degree $m$ onto the residual
line (Theorem~\ref{thm:stable-tail-v161}). Thus the Hilbert limit
has a thickened tail whereas the stable limit has a covered tail.
Their cycles agree but their objects do not. This is an explicit
comparison, not a claim that the Hilbert and stable-map
compactifications are generally isomorphic. Nor do we identify a
slice normalization with an unproved base change of the full
ambient Hilbert normalization.

\subsection{The multiplication input}
The finite algebra
\[
 B_h(V)=\Sym(\Sym^2V)/\langle(v^2)^{h+1}:v\in V\rangle
\]
has coefficient ideals
$J_{hq+s}(A)=I_q(A)^{h-s}I_{q+1}(A)^s$, $0\leq s<h$, over every
commutative complex algebra (Theorem~\ref{thm:universal-power-v157}).
The first four sections fix its twists and coefficient map and
prove the identity and graph description. On our rank open,
$J_{h(n-2)+1}=I_{n-1}$, with $h=1$ giving the distinguished power.
All tail power systems are complete systems of degree
\[
 \delta_j=(j-h(n-2))_+-2(j-h(n-1))_+.
\]
For a thick tail this is a statement over $\C[x]/(x^m)$, not merely
on the reduced support. The exact coefficient space and the image
Rees algebra retain information that radicals and cycles discard.

\subsection{Classical geometry, scope, and dependencies}
Li's wonderful-model Theorems~1.2--1.3 \cite{Li2009v161} already
identify arrangement modifications with product-ideal blow-ups.
The strict-transform image-algebra construction is standard
\cite[Tag~080C]{Stacks161}. Our assertions identify the particular
pencil incidence ideal, prove independence at all its reduced
contacts, and identify the resulting space with the specified
normalized Hilbert graph. The familiar equations of smooth
blow-ups are not asserted to be new general geometry.
Gathmann's tangency theorem \cite[Theorem~7.1]{Gathmann1998v161}
uses stable maps to blow-ups to express enumerative conditions. Our
covered-tail calculation distinguishes that moduli object from a
flat embedded Hilbert limit; it is not an enumerative formula.

The boundary results above start with $V$ and its pencil. Their
interpretation on the effective failure-algebra stack invokes the
companion's sharp inverse and scalar-normalized envelope. That
envelope is constructed on the recovered source, not contained in
the original finite algebra. The companion gives its precise stack
home, multi-Rees presentation, and relative lifting equations.
The two core proofs are logically independent of these applications.

The appendices retain all-rank complete quadrics, the finite
syzygy/contact recovery of arbitrary symmetric pencils, ordinary
transverse collisions of arbitrary multiplicities, the earlier
single-incidence theory, conductors, and reciprocal-fibre homology.
The word ordinary in that collision theorem retains its squarefree
residual and transverse hypotheses. The new reduced-incidence
open still excludes higher corank; the nonreduced result classifies
the displayed slices, not every ambient higher-contact fibre.
The accessible classical classification is
\cite[Theorem~2.1]{DeTeranDmytryshynDopico2018v161}. The comparison
with Ballico's 1993 failure-locus paper \cite{Ballico93} remains
limited by unavailable theorem/proof-level text; the separately
available \cite{Ballico1996v161} does not remove that limitation.
'''
MASTER_ABSTRACT=I_ABSTRACT+r''' The paired boundary theory identifies the full
multiple-reduced-incidence modification and computes arbitrary-order
Jordan contact slices, thick Hilbert tails, transverse graph
singularities and covered stable-map tails. This master preserves
both mathematical bodies and is not a third submission.'''
MASTER_INTRO=r'''\section{Introduction}
\label{sec:introduction-v153}
The first paper proves the sharp unmarked inverse for every complex
quadratic pencil. The second identifies the full normalized Hilbert
modification over the reduced corank-two incidence open and computes
nonreduced-contact slices of every order. The respective principal
results are Theorems~\ref{thm:artin-local-inverse-v146},
\ref{thm:multiple-incidence-v161}, and
\ref{thm:contact-hilbert-v161}. The singularity and stable-map
comparison are Proposition~\ref{prop:contact-deformations-v161}
and Theorem~\ref{thm:stable-tail-v161}. Their effective stack and
relative lifting interpretation is given in
Theorem~\ref{thm:boundary-stack-v161} and
Proposition~\ref{prop:relative-obstructions-v161}.

This master contains all earlier statements and proofs. The focused
papers place their core arguments before supplementary extensions;
no extension is silently used as a premise of the sharp inverse.
Classical arrangement blow-ups, complete quadrics, hypersurface
singularities and symmetric canonical forms are credited at their
points of use. The source-normalized envelope is not a subquotient
of the finite failure algebra, and a closed algebra does not choose
a normal deformation direction. The Ballico 1993 comparison remains
documentary-limited \cite{Ballico93}; no priority inference is drawn
from unavailable text.
'''
DISCLOSURE=''
BIB=r'''\bibitem[Li(2009)]{Li2009v161}
L. Li, Wonderful compactification of an arrangement of subvarieties,
\emph{Michigan Math. J.} \textbf{58} (2009), 535--563;
\url{https://arxiv.org/abs/math/0611412}.
\bibitem[De Teran--Dmytryshyn--Dopico(2018)]{DeTeranDmytryshynDopico2018v161}
F. De Ter\'an, A. Dmytryshyn and F. M. Dopico,
\emph{Generic symmetric matrix pencils with bounded rank},
arXiv:1808.03118 (2018), Theorem~2.1;
\url{https://arxiv.org/abs/1808.03118}.
\bibitem[Gathmann(1998)]{Gathmann1998v161}
A. Gathmann, \emph{Gromov--Witten invariants of blow-ups},
arXiv:math/9804043 (1998), Section~7;
\url{https://arxiv.org/abs/math/9804043}.
\bibitem[Ballico(1996)]{Ballico1996v161}
E. Ballico, On the failure cycles for the quadratic normality of a
projective variety, \emph{Pacific J. Math.} \textbf{172} (1996),
307--314.
\bibitem[Stacks Project]{Stacks161}
The Stacks Project Authors, \emph{The Stacks Project},
Section~29.55 (normalization), Tags 080C (strict transform),
0806 (universal property of blowing up), and 02LS (finite morphisms),
\url{https://stacks.math.columbia.edu}, accessed September 25, 2026.
'''
