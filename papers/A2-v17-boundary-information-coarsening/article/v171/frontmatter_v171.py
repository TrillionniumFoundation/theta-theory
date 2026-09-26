"""Publication front matter; repository audit metadata is kept in separate files."""
TITLE='Conductors under coefficient change and nonmonomial Hilbert boundaries'
ABSTRACT=r'''
Let $T\to S$ be a normal proper birational model of a smooth variety in
characteristic zero, let $X\to S$ be finite flat with $X$ smooth, and
let $Z$ normalize $T\times_S X$. We express the actual conductor ideal
on $Z$ as the difference between the pulled-back Jacobian divisor of
the coefficient map and the ramification divisor of $Z\to T$. The
identity is compatible with towers of covers and includes conditions
in every codimension. Applied to polynomial-contact Hilbert graphs,
it determines conductors and normalization defects for all tangent
covers $b=u^r$, $c=u+v^s$. For the square-tangency cover and every
contact order, we determine the complete normalized surface and its
scheme fibre: two rational double points are followed by an explicit
chain of smooth point blow-ups. Equal embedded Hilbert limits can
then have a regular normalization lift and a singular one. The
self-contained diagonal specialization also recovers the full
nonreduced parameter fibre and its exact nilpotence order.
'''
INTRO=r'''
\section{Introduction}\label{sec:introduction-v171}
A flat embedded limit, the normalization of its parameter space, and
the scheme fibre of that normalized space need not retain the same
information. The conductor measures a further difference: it records
precisely which functions on the normalization descend to the original
parameter space. Computing its generic order on boundary divisors is
not by itself a computation of the conductor at their intersections.
This distinction is particularly relevant when a change of coefficients
turns a smooth Hilbert graph into a nonnormal surface.

The first result of this paper gives an identity of actual conductor
ideals under finite flat changes of a smooth coefficient space. It
applies to any normal proper birational model, in any dimension. Its
proof uses classical trace duality. The geometric applications then
leave the diagonal toric setting: two coefficient divisors become
tangent, distinct divisorial valuations can agree on the two original
coordinate functions, and one Hilbert point can have normalization
lifts with different singularity types.

\subsection{The conductor identity}
Let $h:X\to S$ be a finite flat dominant map of smooth varieties over
a characteristic-zero field, and let $f:T\to S$ be proper birational
with $T$ normal. Write
\[
 Y=T\times_S X,\qquad Z=Y^\nu,\qquad
 \pi:Z\to X,\quad \psi:Z\to T.
\]
The fibre product is integral. Let $R_h$ be the Cartier divisor of
$\operatorname{Fitt}_0\Omega_{X/S}$, and let $R_\psi$ have coefficient
$e_Q-1$ at a prime divisor $Q$ of $Z$, where $e_Q$ is the ramification
index over $T$. Theorem~\ref{thm:duality-conductor-v171} gives
\[
 \mathfrak c_{Z/Y}=\OO_Z(R_\psi-\pi^*R_h).
\]
This is not just an isomorphism of rank-one modules or an equality
on an open set containing the generic points of the divisors. It
identifies the conductor as a reflexive ideal at every point. In
particular its order at $Q$ is
$v_Q(\operatorname{Fitt}_0\Omega_{X/S})-e_Q+1$.

The resulting defect cycle is twice the generic length of the
normalization quotient, weighted by residue degrees
(Corollary~\ref{cor:defect-cycle-v171}). The conductor divisors add
under towers of finite flat covers in the precise sense of
Theorem~\ref{thm:conductor-tower-v171}; this involves reflexive
products, not an unproved equality of ordinary tensor products.
No smoothness or Cohen--Macaulay assumption on $T$ beyond normality
is needed for the conductor identity. The normalization of a rational
Hilbert graph is therefore an immediate source of examples.

\subsection{Tangent polynomial contacts}
For $a\geq2$ consider the marked family of embedded graphs of
\[
 [s_0:t_0]\longmapsto[t_0^a:b s_0^a:cs_0t_0^{a-1}]
 \quad\text{in }\Pj^1\times\Pj^2.
\]
We prove directly that its retained-coefficient Hilbert graph is the
smooth chain blow-up of $\prod_{j=1}^a(b,c^j)$. This proof gives a
finite row factorization of the evaluation ideal, removes its
principal content, and derives an exhaustive affine cover. It uses
no assertion about an unmarked finite algebra and no theorem from
the reconstruction paper.

Now change coefficients by $b=u^r$, $c=u+v^s$, with $r,s\geq2$.
The conductor identity determines every divisorial conductor order
and generic defect for every $a,r,s$; the residue extensions are
computed rather than inferred from the number of roots in a closed
fibre (Theorem~\ref{thm:tangent-conductor-v171}). For $r=s=2$ we
compute the complete normal surface in every contact order
(Theorem~\ref{thm:square-tangency-v171}). At order two its middle
chart is
\[
 k[e,z,v]/(v^2-ez(z-1)),\qquad u=ez,
\]
with conductor $(e)$ and scheme fibre $k[e,z]/(ez)$. The two points
$z=0,1$ on that chart are rational double points. Each higher contact
order adds one ordinary blow-up at a smooth endpoint. The full
parameter fibre stays a reduced nodal chain, although the conductor
orders grow along it.

The first two exceptional divisors both have values $(2,1)$ on
$(u,v)$, but their values on $u+v^2$ are $4$ and $2$. Thus the result
cannot be read from a fan in the original two monomial weights.
Moreover the Hilbert coordinate is $z^2$ along the second divisor.
The points $z=1$ and $z=-1$ give the same embedded Hilbert limit,
while one normalization germ is singular and the other is regular.
Explicit projective coefficient arcs realize both points
(Corollary~\ref{cor:tangent-lost-labels-v171}).

\subsection{Relation to classical results and scope}
The trace complementary module and the equality of the K\"ahler and
Dedekind differents for finite flat complete intersections are
classical; precise formulations appear in
\cite[Sections 49.8, 49.12 and 49.15]{Stacks171}. Our proof of the
conductor identity exposes this dependence. It is not a claim to a
new duality formalism. The Newton-polyhedron criterion, normalized
Rees constructions and the complete-ideal theory used in the marked
chain belong to the established theory of integral closure
\cite[Chapters 1, 5 and 14]{HunekeSwanson171}. The same reference
states Jacobian containment results and the Lipman--Sathaye theorem
in its conductor chapter. Here the stronger geometric hypotheses
permit an equality of the actual conductor with a specified
complementary module, followed by the explicit nonmonomial
normalization and fibre calculations above. No exhaustive priority
claim for the general identity is made.

The diagonal family $b=u^\rho$, $c=v^\sigma$ is treated separately in
Section~\ref{sec:diagonal-v171}. There the full coordinate ideal on a
proper toric cone is divisorial; a proof on the character lattice
shows that the scheme fibre has no embedded points. The reduction
at a cyclic quotient crossing is computed as an ordinary node, and
ordinary powers give the exact nilpotence order. The conductor is
then recovered from the same coefficient-change identity, including
an explicit unequal-cover chart and overlap generators.

The conductor theorem is not restricted to these two surface
families. The complete surface and fibre classifications, however,
refer to the stated families. Neither the conductor formula nor the
examples assert a classification of all higher-corank or singular
quadratic-pencil Hilbert fibres. Normalizing the parameters does
not normalize the embedded universal curves. All uses of a finite
failure algebra require the separate effective reconstruction
hypotheses; none enters the proofs in this paper. The accompanying
technical supplement retains the earlier power-ideal, equivariant,
contact and reconstruction-application arguments for reference,
without making them prerequisites of the present central route.
'''
I_INTRO=r'''
\section{Introduction}
\label{sec:paper-i-v164}\label{sec:paper-i-v166}\label{sec:paper-i-v167}
Let $V$ be a complex vector space of dimension $n\geq3$, and let
$R\subset\Sym^2V$ have dimension two. Set $N=\binom{n+1}{2}$,
$p=N-2$, and $d=n+2p=n^2+2n-4$. The universal graph matrix $T$ and
the quotient map $\gamma_R$ define the finite local algebra
\[
 A_R=\C[t_{ij}]/\bigl((\det T)I_p(\gamma_R\Sym^2T)
                                      +\mathfrak m^{d+1}\bigr).
\]
The main assertion is
\[
 A_R\simeq A_{R'}\text{ as unmarked, ungraded algebras}
 \quad\Longleftrightarrow\quad R'=gR\quad(g\in\PGL(V)).
\]
Every smaller truncation is independent of the pencil
(Theorems~\ref{thm:artin-local-inverse-v146} and
\ref{thm:sharp-finite-pencil}). The assertion includes singular
pencils. Neither a chosen grading nor preferred generators are part
of the input. The boundary and conductor results in the separate
paper are not used to establish this inverse.

\subsection{The invariant recovery chain}
The proof has four operations. The maximal ideal filtration first
recovers the cotangent space and its first nonzero relation space;
this is the step that must survive nonlinear changes of generators.
The common determinant divisor of the first relation then recovers
two tensor rulings. The residual coefficient module distinguishes
them by unequal support ranks, removing the transposition ambiguity.
Finally its coefficient line is the Pl\"ucker line of $R$. The
arguments from first relations through coefficient-support
orientation establish these operations before any boundary
application is introduced. The family coefficient map is a closed
immersion over arbitrary complex bases
(Theorem~\ref{thm:finite-parameter-immersion}); the family statement is
not inferred merely from injectivity on closed points.

The central proof concerns complex algebras and complex pencils.
The initial maximal-ideal and relation-space construction is an
algebraic operation, but the determinant-preserver argument,
polarization and highest-weight coefficient recovery use the
characteristic-zero hypotheses stated in their respective lemmas.
The spectral and singular-pencil consequences use the complex
symmetric Kronecker classification. We do not infer a theorem in
positive characteristic by suppressing these inputs. For a proof
audit the essential transitions are therefore: ungraded relations,
determinant rulings, support-rank orientation, coefficient recovery,
and scheme-level family immersion, followed separately by sharpness
and the singular classification consequences.

\subsection{Logical independence and applications}
The complete proofs of the relative, covering, recognition,
rigidification, envelope and spectral consequences are retained in
the appendices. They do not become extra hypotheses of the sharp
inverse. The effective-family boundary statements at the end use
geometric results recorded in the technical supplement, and are
explicitly downstream applications. A closed algebra can determine
a space of permissible directions; it does not supply a chosen
coefficient arc. Nor is every deformation of a raw Artin algebra
asserted to remain in the effective pencil image.

The companion paper starts instead with a normal birational model
of a smooth coefficient space. Its trace-duality conductor identity
and its tangent-contact computations are independent of the inverse
proved here. Interpreting them for a specified failure family first
requires reconstruction and the stated fixed-target comparison.
This separation prevents a boundary calculation from being used as
evidence for the inverse theorem itself.

\subsection{Literature and verification status}
The classical symmetric-pencil classification is stated in
\cite[Theorem 2.1]{DeTeranDmytryshynDopico2018v161}. Spectral positions
and local partitions are retained modulo a single projective
reparametrization; a minimal-index block has size $2\varepsilon+1$.
Ballico's quadratic-normality failure-cycle result
\cite[Theorem 0.2]{Ballico1996v161} is an existence theorem for finite
subschemes on a projective surface, not an input to this inverse.
The full theorem/proof comparison with \cite{Ballico93} remains
unavailable. No historical anticipation or nonanticipation claim is
inferred from that documentary limitation.

The written proof is offered for independent specialist scrutiny.
No external independent full proof audit has been obtained. Hash
checks establish preservation of the argument, not its correctness;
finite algebra checks likewise do not certify the general inverse.
'''
ACK=r'''
\section*{Acknowledgment of assistance}
AI assistance was used in deriving and drafting arguments, checking
finite symbolic instances, and preparing the manuscript. The stated
proofs and attributed mathematical results are submitted for
independent scrutiny. No AI system is listed as an author, and no
external proof audit or formal proof certification is implied.
'''
BIB=r'''
\bibitem{Stacks171}
The Stacks Project Authors, \emph{The Stacks Project},
Sections 49.8 (Tag 0BW0), 49.12 (Tag 0BWB), and 49.15 (Tag 0DWM),
\url{https://stacks.math.columbia.edu}; accessed September 27, 2026.
\bibitem{HunekeSwanson171}
C. Huneke and I. Swanson, \emph{Integral Closure of Ideals, Rings,
and Modules}, London Mathematical Society Lecture Note Series 336,
Cambridge University Press, Cambridge, 2006.
\bibitem{Gotzmann171}
G. Gotzmann, Eine Bedingung f\"ur die Flachheit und das Hilbertpolynom
eines graduierten Ringes, \emph{Math. Z.} \textbf{158} (1978), 61--70.
'''
