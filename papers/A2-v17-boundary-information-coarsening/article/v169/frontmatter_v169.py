"""Front matter for v169. The previous front matters are archived intact."""
TITLE='Primitive graph ideals and higher-contact Hilbert limits'
II_ABSTRACT=r'''
We determine the Hilbert graph and every embedded boundary curve of
$[t^a:bs^a:cst^{a-1}]$ for arbitrary $a\geq2$. After removing its
explicit divisorial content, the evaluation ideal factors into powers
of $(b,c^j)$, $1\leq j\leq a$, and its Rees algebra is normal. The
graph is a smooth surface obtained by $a$ successive point blow-ups.
Uniform monic equations give all $2a+1$ chamber and wall families,
their associated points, and a sharp coefficient-jet bound independent
of the Hilbert embedding degree. On the last wall a rational cuspidal
tail acquires a punctual nilradical of length $(a-1)(a-2)/2$ and
nilpotence order $a-1$: this is the exact arithmetic-genus correction
required by flatness. We also glue the full polynomial-contact graphs
at fixed degree under source and target changes, and compute the
contraction of the marked boundary chain to one fixed-source Quot
point. The all-order curve classification concerns the specified
marked family, not every fibre over the full contact coefficient
space. Its application to quadratic pencils retains the fixed-target
comparison and the reconstruction theorem of the companion paper.
'''
II_INTRO=r'''
\section{Introduction}
\label{sec:paper-ii-v164}\label{sec:paper-ii-v166}\label{sec:paper-ii-v167}
\label{sec:paper-ii-v169}
A flat limit of embedded rational curves can remember arithmetic genus
through a zero-dimensional nilpotent structure. Taking a cycle, taking
a reduced support, or taking the scheme image of a stable map loses
that information. This paper determines this phenomenon together with
the parameter space that carries it in an all-order contact family.

Our central result is Theorem~\ref{thm:chain-model-v169} and its
embedded-curve description in Theorems~\ref{thm:arc-table-v169}
and~\ref{thm:genus-correction-v169}. For
\[
 [s:t]\longmapsto[t^a:bs^a:cst^{a-1}],\qquad a\geq2,
\]
let $T_a$ be the closure of the coefficient-retaining graph in the
Hilbert scheme of $\Pj^1\times\Pj^2$. We prove
\[
 T_a=\operatorname{Bl}_{\prod_{j=1}^a(b,c^j)}\A^2.
\]
The surface is smooth, with $a$ exceptional curves. It carries an
explicit universal curve described by at most $a+1$ equations per
intermediate or terminal chart. The equations form monic Gr\"obner
bases over the entire parameter charts. Consequently all boundary
rings, including embedded associated points, follow from one uniform
proof rather than separate saturation calculations for individual
arcs.

For a degree-$m$ Hilbert evaluation matrix the exact ideal is
\[
 b^{(a-1)m(m+1)/2}
 \left(\prod_{j=1}^{a-1}(b,c^j)^{m-j+1}\right)
 (b,c^a)^{(m-a+1)(m-a+2)/2}.
\]
Its principal factor has no effect on the graph. We compute the
normal Rees algebra of the remaining ideal, its primitive exceptional
valuations, the boundary intersection matrix, and its contractions.
For a formal arc with $\operatorname{ord}(b)=p$, the coefficient jet
modulo $\tau^{p+1}$ determines the embedded closed limit. This bound
is uniformly optimal on that class of arcs and is independent of
contact order and of the chosen Hilbert degree. It is different from
the much larger raw maximal-minor order.

The last wall is particularly instructive. Its reduced tail is
$R^a=\lambda F^{a-1}G$, attached to the main component at a smooth
point. At the cusp the actual Hilbert limit has nilradical
\[
 xk[x,F]/x(x,F)^{a-2},\qquad R\mathcal N=0.
\]
Its length is the arithmetic genus of the plane tail. For $a=3$ this
is one square-zero embedded point; for larger $a$ the nilpotence
order grows. It cannot be removed while retaining the Hilbert
polynomial. Theorem~\ref{thm:punctual-v169} also calculates the
punctual excess and generic transverse algebras on every preceding
wall and chamber.

\subsection{Intrinsic objects and their presentations}
A maximal-minor ideal is a Fitting ideal of a specified evaluation
module. Its order and Smith factors are not numerical invariants of
the underlying Hilbert map under arbitrary changes of embedding.
Section~\ref{sec:content-v169} separates divisorial content, a primitive
ideal, the finite-module length, and the exceptional Rees valuations.
On the full monic coefficient chart the evaluation ideal already has
no divisorial content, because its base locus has codimension two.
Nonflat restriction can introduce content, as the displayed family
shows. This distinction is necessary; merely dividing a restricted
factor out of a matrix does not make all its numerical data intrinsic.

Theorem~\ref{thm:global-gluing-v169} then gives a single equivariant
projective graph over the projective space of degree-$a$ triples.
Every monic pivot chart is an explicit product with the full
polynomial-contact graph $\Gamma_a$, with actual source and target
undo maps and cocycles on overlaps. This is a fixed-degree rational-map
compactification. It does not glue unaugmented graph functors with
different generic Hilbert polynomials, nor does it classify all
higher-corank or singular-pencil fibres. The complete classification
proved here is the all-order marked family and its equivariant
extensions, including moving contact centres.

\subsection{Comparison and an application independent of reconstruction}
The minimal fan of $T_a$ is the Newton fan of its primitive monomial
ideal. Its wall residues are genuine embedded parameters, even when
their valuation vectors agree. General coefficient-support
arrangements, by contrast, need not be minimal or invariant under
polynomial coordinate changes. Section~\ref{sec:equivariant-v169}
compares these constructions with tropical Pl\"ucker data and
comprehensive Gr\"obner systems.

The same coefficient family has a flat quotient of
$\OO_{\Pj^1}^{\oplus3}$ before any blow-up. At the origin that quotient
is independent of the coefficient direction, so the map to the
fixed-source Quot scheme contracts the whole exceptional chain.
The Hilbert graph separates its points and retains the punctual genus
correction. This is a concrete comparison of objects, not an
identification based on a difference in terminology.
Corollary~\ref{cor:external-curves-v169} gives smooth rational graphs
whose Hilbert limits have isolated nilradicals of arbitrarily large
nilpotence order. It uses none of the inverse theory of Paper I.

\subsection{Proof route and retained theory}
The main proof proceeds from row ideals to the normal Rees algebra,
then to monic universal equations and their local rings. The
fixed-degree gluing and Quot comparison follow separately. Hilbert
representability, regularity, Rees graph constructions, and toric
normalization are classical inputs. The calculated all-order
factorization, the uniform chart equations, the complete arc table,
and the punctual genus-correction algebra are the explicit results
proved here; no new general representability mechanism is claimed.

The previous determinantal graph, complete first-contact fibre,
horizontal comparison, power ideals, complete quadrics, and singular
pencil results are retained in the appendices, with their proofs and
labels intact. They provide the full earlier framework and the
fixed-target bridge to quadratic pencils without competing with the
central proof route. The preservation master contains both paper
bodies and is not a third submission. The sharp inverse is needed
only when a specified effective failure family is first reconstructed
and then inserted into this boundary construction. No internal
boundary operator on an isolated raw finite algebra is asserted.

Historical claims are restricted to the explicitly stated theorems.
No claim about priority over Ballico's 1993 work is made without a
full-text comparison, which remains unavailable. The unchanged
sharp-inverse proof is not represented as having received an external
independent audit. Neither compilation nor finite symbolic checks can
supply that audit or certify the originality of a general theorem.
'''
I_ADD=r'''
\subsection{The higher-contact boundary application}
The companion paper now determines the complete marked family
$[t^a:bs^a:cst^{a-1}]$ for every $a\geq2$, including its normal Rees
algebra and its punctual genus correction. Its fixed-degree graph
also glues under source and target changes
(Theorem~\ref{thm:global-gluing-v169}). These results apply after the
sharp inverse to a specified effective family with the required
fixed-target contact comparison. They do not recover a missing arc
from a closed multiplication table. The proof of the inverse in this
paper is retained unchanged; the new application is not an external
independent audit of that proof. The historical framing makes no
priority claim requiring the still unavailable full Ballico 1993
comparison.
'''
BIB=r'''
\bibitem[Stacks Project]{Stacks169}
The Stacks Project Authors, \emph{The Stacks Project},
Section~31.33, ``Blowing up'', Tag~01OF,
\url{https://stacks.math.columbia.edu/tag/01OF}.
\bibitem[Speyer--Sturmfels(2004)]{SpeyerSturmfels169}
D.~Speyer and B.~Sturmfels, \emph{The tropical Grassmannian},
Adv. Geom. \textbf{4} (2004), 389--411;
arXiv:math/0304218.
\bibitem[Manubens--Montes(2006)]{ManubensMontes169}
M.~Manubens and A.~Montes, \emph{Improving DISPGB algorithm using
the discriminant ideal}, J. Symbolic Comput. \textbf{41} (2006),
1245--1263; arXiv:math/0601763.
\bibitem[Marian--Oprea--Pandharipande(2011)]{MOP169}
A.~Marian, D.~Oprea, and R.~Pandharipande,
\emph{The moduli space of stable quotients}, Geom. Topol.
\textbf{15} (2011), 1651--1706; arXiv:0904.2992.
\bibitem[Manolache(2014)]{Manolache169}
C.~Manolache, \emph{Stable maps and stable quotients},
Compos. Math. \textbf{150} (2014), 1457--1481; arXiv:1301.4393.
'''
