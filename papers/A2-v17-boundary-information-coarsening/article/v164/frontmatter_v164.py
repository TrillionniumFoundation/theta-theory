"""Front matter for the paired papers; all preceding front matter is archived."""
from pathlib import Path
import importlib.util
p=Path(__file__).resolve().parent.parent/'v163'/'frontmatter_v163.py'
spec=importlib.util.spec_from_file_location('front163',p)
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
I_ABSTRACT=old.I_ABSTRACT+r''' A concrete collision family identifies the
horizontal boundary, its vertical excess, and the global nilpotent
sheaf on the first nonreduced fibre.'''
I_INTRO=old.I_INTRO.replace('sec:paper-i-v163','sec:paper-i-v164')+r'''
\subsection{Moving supports and effective families}
The boundary changes when two reduced incidences merge. The
companion's Theorem~\ref{thm:collision-family-v164} distinguishes
the entire pullback of the Hilbert modification from the closure
of its generic fibres. The latter is a smooth flat threefold with
central divisor $\mathbb F_2+2\Pj^2$. The full pullback has an
additional vertical $\Pj^4$, attached along the singular-conic
plane. Its base-torsion is that plane's ideal inside $\Pj^4$.
Proposition~\ref{prop:genuine-collision-v164} realizes this by an
explicit four-dimensional symmetric pencil, rather than by an
arbitrary deformation of a residual matrix. The interpretation for
failure families remains through the effective inverse. It does
not assert that a closed algebra chooses a deformation direction,
or that all raw Artin-algebra deformations lie in the pencil image.
'''
II_TITLE='Power ideals and the Hilbert boundary of quadratic pencils'
II_ABSTRACT=r'''We determine scheme fibres and collision families in the Hilbert
graph of lifted quadratic pencils. A corank-two contact of length
two has a projective four-space of conic tails and a Hirzebruch
surface of line jets, meeting along the doubled-line curve. Its
nilradical is the extension by zero of $O_{P^2}(-1)$ from the
singular-conic plane. For a collision of two reduced incidences,
the horizontal closure is the quotient of the blow-up of the
ordered direction product along its diagonal at the collision
parameter. This is a smooth flat threefold whose central divisor
is $F_2+2P^2$. The full pullback also contains a vertical $P^4$;
its exact base-torsion measures the excess. Ordering the supports
by a quadratic base change and normalizing gives a reduced
normal-crossing model. Independent collisions have explicit
product multiplicities. The proof uses retained-coefficient
Hilbert charts, an embedded fixed-target comparison, and universal
multiplication ideals equal to balanced products of symmetric
minor ideals. All statements concern scheme fibres of the
normalization of the total graph, not normalizations of fibres.'''
II_INTRO=r'''\section{Introduction}
\label{sec:paper-ii-v164}
The specialization of two independent boundary choices need not
fill the boundary attached to their common limit. For quadratic
pencils this distinction already appears when two reduced
corank-two incidences merge. The complete limiting Hilbert fibre
has components of dimensions two and four. The flat limit of the
separated direction spaces has pure dimension two, a double
component, and a nontrivial ordering monodromy. We determine both
objects and the scheme-theoretic excess relating them.

Let $V$ be a complex vector space, $G=\Gr(2,\Sym^2V)$, and
$\pi:\mathrm{CQ}(V)\to\Pj(\Sym^2V)$ the classical complete-quadric
morphism. Lift a pencil line avoiding corank two to $\mathrm{CQ}(V)$.
These curves have Hilbert polynomial $\binom n2l+1$ for the
polarization $\bigotimes_{q=1}^{n-1}H_q$, where $H_q$ is the resolved
exterior hyperplane bundle. We write $\widehat G$ for the
normalization of the total reduced graph of this Hilbert map.
The base pencil and the embedded curve are both retained; curves
are not identified by ambient target automorphisms. A scheme fibre
of $\widehat G\to G$ may be nonreduced although the total space is
normal. We never replace it by its own normalization.

\subsection{Complete contact fibres}
The local coefficient base $B_2$ parametrizes triples $(f,g,r)$,
with $f$ monic quadratic and $g,r$ of degree at most one. The
corresponding graph retains its map to $B_2$. Theorem
\ref{thm:complete-fibre-v163} determines its complete fibre $X_2$
over $(x^2,0,0)$. Its reduced components are
$\mathcal Q_P=\Pj^4$, parametrizing conic tails through the
attaching point $P$, and $E=\mathbb F_2$, compactifying
$J_1(\Pj^1)=\operatorname{Tot}(T\Pj^1)$. They intersect in the
curve of doubled lines, which is the negative section of $E$.
The local fibre equation is
\[
                  (eA,eB,e^2C).
\]
This equation also records a square-zero ideal supported on
$S=\{Q:Q\text{ is singular at }P\}=\Pj^2\subset\mathcal Q_P$.
Theorem~\ref{thm:nilradical-sheaf-v164} identifies that ideal globally
as $j_*\OO_S(-1)$, including its line-bundle twist. This is a module
identification, not an assertion that the algebra extension splits.

For distinct contacts with smaller positive Smith exponents at most
two, Theorem~\ref{thm:product-fibres-v163} determines the entire
scheme fibre as $X_2^r\times(\Pj^1)^s$. It gives all $2^r$ reduced
components, their dimensions, their intersections and the nilpotence
order $r+1$. The larger Smith exponents are arbitrary. These complete
fibres retain the all-pencil invariant theory developed in the
appendices; they do not replace the singular-pencil theorem by a
regular-pencil restriction. Higher contact lengths have their own
primitive open charts and a separately labelled component conjecture.

\subsection{Collision and vertical excess}
Consider the coefficient curve
\[
 \delta\longmapsto(f,g,r)=(x^2-\delta,0,0).
\]
Let $\mathcal H$ be the full pullback of the normalized Hilbert graph
and $\mathcal Y$ the schematic closure of its restriction to
$\delta\ne0$. Theorem~\ref{thm:collision-family-v164} identifies
$\mathcal Y$ with
\[
 \operatorname{Bl}_{\Delta\times\{0\}}
   (\Pj^1\times\Pj^1\times\mathbb A^1_t)
       /\bigl((\ell_+,\ell_-,t)\sim(\ell_-,\ell_+,-t)\bigr),
 \qquad \delta=t^2.
\]
Its explicit invariant charts are polynomial rings. It is smooth,
projective and flat, and its central divisor is
\[
                            \mathcal Y_0=E+2S.
\]
Here $S=\operatorname{Sym}^2\Pj^1$ parametrizes unordered pairs of
lines through $P$; $E\cap S$ is the doubled-line conic in $S$ and
the negative section in $E$. Only singular-at-$P$ conics occur in
this horizontal specialization, whereas the full limiting fibre
contains every conic through $P$.

The full family is the scheme union
$\mathcal H=\mathcal Y\cup_S\mathcal Q_P$. Its vertical part is
measured exactly by
\[
 \ker(\OO_{\mathcal H}\to\OO_{\mathcal Y})
      =i_*\mathcal I_{S/\mathcal Q_P}
      =\operatorname{Tor}^{\C[\delta]}_1(\OO_{\mathcal H},\C).
\]
Thus the failure of flatness is identified as a coherent sheaf,
not inferred only from the dimensions of two fibres. The nilpotent
sheaf of $X_2$ is the same one seen in the double component of this
horizontal collision. The family supplies a geometric explanation
of the equation $e^2C=0$.

Theorem~\ref{thm:ordered-resolution-v164} identifies normalization
after the root base change with the ordered blow-up. Its parameter
space has a reduced normal-crossing special fibre. On the punctured
base the two ruling classes are exchanged by monodromy. Neither
statement changes thick Hilbert curves into stable maps: the family
being resolved here is a parameter space, and its universal embedded
curves remain the specified Hilbert objects. Independent collisions
have central multiplicities $2^{|J|}$ by
Corollary~\ref{cor:multiple-collisions-v164}.

\subsection{Proof mechanism and comparison}
The principal algebraic input is the exact universal identity
$J_{hq+s}=I_q^{h-s}I_{q+1}^s$ for determinant-apolar multiplication
over arbitrary complex algebras. The classical invariant-ideal,
determinantal and complete-quadric ingredients are attributed where
used. The embedded comparison is a theorem about retained-coefficient
quotients with their incidence maps. Parameter-dependent congruences
are undone before a fixed-target Hilbert point is taken; they do not
become constant source automorphisms by notation. Hilbert--Burch and
Euclidean graph charts have regular recovery maps. The full-fibre
exhaustion then uses proper connected fibres and the already proved
open charts, rather than the existence of a few limiting arcs.

The collision theorem compares a discriminant specialization and its
horizontal closure. It is not a change of a stability condition or
a completion of Mori's program. The latter perspective for conics
in Grassmannians has a much broader established theory; see
\cite[Theorem~1.1 and Section~3.1]{ChungMoon164}. Stable-quotient,
quasimap and low-degree Hilbert comparisons are discussed in the
preserved literature sections. None of those different moduli
objects is silently identified with our retained-coefficient graph.
The new claim is the exact collision pullback, its quotient model,
and its excess and nilpotent sheaves in this specified Hilbert
problem, not the novelty of blow-ups or finite quotients themselves.

\subsection{Dependence and scope}
The universal power and Hilbert results can be read for an independently
given source and pencil. The companion's sharp inverse is not used
in their proofs. Conversely that inverse does not rely on the
collision geometry. Proposition~\ref{prop:genuine-collision-v164}
realizes the present model by an explicit symmetric pencil of size
four and then transfers it to the effective failure-family image.
The transfer is not a theorem about the full deformation stack of
all Artin algebras. No external independent audit of the entire sharp
inverse has been obtained, and no such audit is inferred from exact
computations. The theorem/proof-level comparison with Ballico's
1993 failure-locus paper remains documentary-incomplete, as recorded
also in the companion; unavailable text is not evidence of priority.

The main route proceeds from the power ideals and formal contact
coordinates through the fixed-target chart comparison and the
complete first-contact fibre to the collision family. The appendices
retain all earlier proofs, higher-contact slices, singular-pencil
data, normalization and homological calculations. There is no claim
of a complete Hilbert-boundary classification at higher corank or
arbitrary contact length.
'''
MASTER_ABSTRACT=old.MASTER_ABSTRACT+r''' We also determine the collision of
two reduced incidences, separating its flat horizontal closure from
its vertical conic excess and identifying the global nilradical sheaf.'''
MASTER_INTRO=old.MASTER_INTRO+r'''
\subsection{Collision families}
Theorem~\ref{thm:collision-family-v164} identifies a full discriminant
pullback and its horizontal closure. Theorem~\ref{thm:ordered-resolution-v164}
gives its ordered normalization after a quadratic base change.
Theorem~\ref{thm:nilradical-sheaf-v164} identifies the global square-zero
sheaf, and Proposition~\ref{prop:genuine-collision-v164} supplies a
fixed-target pencil realization. The parameter-space semistable
model is kept distinct from the universal embedded curve.
'''
BIB=r'''\bibitem[Stacks Project]{Stacks164}
The Stacks Project Authors, \emph{The Stacks Project},
Tag 0539 (torsion-free modules over valuation rings),
\url{https://stacks.math.columbia.edu/tag/0539}, accessed September 26, 2026.
\bibitem[Chung and Moon(2017)]{ChungMoon164}
K.~Chung and H.-B.~Moon, \emph{Mori's program for the moduli space
of conics in Grassmannian}, Taiwanese J. Math. \textbf{21} (2017),
621--652; arXiv:1608.00181.
'''
DISCLOSURE=''
