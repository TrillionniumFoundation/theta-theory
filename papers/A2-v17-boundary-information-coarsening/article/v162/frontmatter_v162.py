"""A2 v162 front matter. Complete predecessor introductions are archived."""
from pathlib import Path
import importlib.util
p=Path(__file__).resolve().parent.parent/'v161'/'frontmatter_v161.py'
spec=importlib.util.spec_from_file_location('front161',p)
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
I_ABSTRACT=old.I_ABSTRACT+r''' The boundary application now includes formal
contact neighbourhoods and non-equidimensional Hilbert fibres, in the
explicitly effective deformation category.'''
I_INTRO=old.I_INTRO.replace('sec:paper-i-v161','sec:paper-i-v162').replace(r'\subsection{Dependencies and historical scope}',r'''\subsection{Nonreduced contact neighbourhoods}
The companion's Theorem~\ref{thm:ambient-versal-v162} replaces selected
Jordan slices by full formal contact coordinates. Theorem
\ref{thm:ambient-jet-tails-v162} identifies open charts of the ambient
Hilbert modification and their mixed-thickness collision law. At a
single contact with exponents $(2,2)$ the fibre has a dimension-two
component containing the thick line-tail jets and a distinct component
of dimension at least four containing reduced conic limits
(Theorem~\ref{thm:nonequidimensional-v162}). Corollary
\ref{cor:effective-contact-v162} transports these statements to the
effective failure image. This uses the inverse on families; it does
not assign a chosen tail to a closed algebra before reconstruction.

Proposition~\ref{prop:algebraic-envelope-v162} gives an algebraic
classifying stack for the fppf forms of the specified envelope bundle.
Proposition~\ref{prop:invariant-lifting-v162} identifies the earlier
slope defects with the relative cotangent-complex obstruction and
writes their transition on the opposite chart. These supplementary
results are not premises of the sharp inverse.

\subsection{Dependencies and historical scope}''')
II_TITLE='Power ideals and the Hilbert boundary of quadratic pencils'
II_ABSTRACT=r'''We determine formal contact neighbourhoods and open charts of the
Hilbert boundary of regular symmetric pencils. At a corank-two contact
with Smith exponents $a\leq b$, the full contact base has $2a+b$
parameters. Euclidean division gives an open chart of the ambient
Hilbert graph, rather than a selected family of limits. Its fibres
obey an exact greatest-common-divisor law, describing collisions and
simultaneous thick tails with unequal multiplicities. Over a fixed
pencil the primitive line-tail locus is the product of jet schemes
$J_{a_i-1}(\mathbf P^1)$. At one contact of type $(2,2)$ the actual
normalized Hilbert fibre is reducible and non-equidimensional: it has
a two-dimensional component with this jet open and a distinct component
of dimension at least four, containing reduced conic-tail limits.
The construction uses an exact multiplication-ideal identity over
arbitrary complex algebras. The full reduced-incidence modification,
all-order contact slices, singular-pencil invariants and earlier
reciprocal-fibre theory are retained with their proofs.'''
II_INTRO=r'''\section{Introduction}
\label{sec:paper-ii-v162}
A pencil can have different embedded Hilbert limits even after its
complete elementary-divisor data are fixed. The first nonreduced
corank-two contact already has two different ways to retain degree:
a thickened line over the contact algebra, and a reduced conic over
its support. We prove that these occur in different-dimensional
components of the actual normalized Hilbert fibre. To make this an
ambient statement, we first determine the missing contact parameters
and construct open Hilbert charts with a regular inverse.

Let $V$ have dimension $n$, put $G=\Gr(2,\Sym^2V)$, and write
$\pi:\mathrm{CQ}(V)\to\Pj(\Sym^2V)$ for complete quadrics.
On the dense open of regular pencil lines avoiding corank two, their
unique lifts have Hilbert polynomial $\binom n2 l+1$ for
$\bigotimes_{q=1}^{n-1}H_q$, where $H_q$ is the resolved $q$th
exterior hyperplane bundle. Let $\widehat G$ be the normalization
of the reduced graph of this map to the Hilbert scheme. This fixes
both the embedded moduli problem and the polarization. No target
automorphism quotient is taken in a fibre of $\widehat G\to G$.

\subsection{Full contact parameters and an open Hilbert chart}
At a corank-two point with local Smith exponents $a\leq b$, the
residual symmetric matrix admits formal coordinates
\[
 \begin{pmatrix}f&g\\g&fk+r\end{pmatrix},\qquad
 \deg f=a,\quad\deg k=b-a,\quad\deg g,\deg r<a,
\]
where $f,k$ are monic and their central values are $x^a,x^{b-a}$.
There are $2a+b$ parameters, independent at distinct spectral points.
Theorem~\ref{thm:ambient-versal-v162} proves formal smoothness from
the full framed pencil base to these coordinates. Its tangent
calculation uses actual constant pencil perturbations, not merely
arbitrary matrix power series. The underlying congruence-miniversal
principle is classical \cite{Dmytryshyn162}; the contact coordinates
are used here to analyze a different, embedded Hilbert problem.

The exact incidence module is the cokernel of the two multiplication
matrices $[M_g\ M_r]$ on $\OO[x]/(f)$. Over the nonreduced locus,
its Fitting ideal alone is not asserted to define the Hilbert
modification. Instead Theorem~\ref{thm:division-chart-v162} gives
the chart
\[
 (f,g,w)\longmapsto(f,g,\operatorname{rem}_f(gw)),
                        \qquad\deg w<a.
\]
The relative graph has equation $gU-fV=0$, and its third coordinate
is $wV-qU$, with $q=(gw-r)/f$. Cohomology of the attaching scheme
recovers the coefficients $w,q$ regularly from a Hilbert point.
This regular inverse is what proves that the displayed family is
an open chart of the full graph, not just an injective parametrization
of selected limits.

Theorem~\ref{thm:ambient-jet-tails-v162} transfers these charts to
actual pencils by retaining the pencil parameter in the incidence
target. At a fixed pencil with contact orders $a_i$, their primitive
line-tail locus is
\[
                    \prod_iJ_{a_i-1}(\Pj^1).
\]
The scheme $J_{a-1}(\Pj^1)$ parametrizes directions over the entire
Artin algebra $\C[x]/(x^a)$ and has dimension $a$; constant directions
are only a smaller locus when $a>1$. In a chart the boundary is a
resultant locus, and every fibre is obtained from
$d=\gcd(f,g)$. Its tail is $\Pj^1_{\C[x]/(d)}$, attached along
$\Spec\C[x]/(d)$. This computes splitting, collision and unequal
thicknesses in a full neighbourhood of every primitive line-tail
lift. It does not identify this open locus with the whole proper fibre.

\subsection{A non-equidimensional actual fibre}
Theorem~\ref{thm:nonequidimensional-v162} proves that a regular
pencil with one contact of type $(2,2)$ and otherwise only corank-one
points has a dimension-two irreducible component in its normalized
Hilbert fibre, with open part $J_1(\Pj^1)$. The same fibre contains
a four-dimensional family of reduced conic tails through the
attaching point in the exceptional $\Pj^2$. A component containing
a finite inverse image of that family has dimension at least four.
Thus the fibre is reducible and not equidimensional.

Both types are realized by genuine pencil deformations through the
full contact base. The thick-tail direction comes from the division
chart. A reduced conic comes from three independent quadratic forms
in the parameter and deformation variable, whose ideal is the square
of the point ideal. In the latter limit the contact parameter acts
by its closed-point value, and degree is carried by a reduced curve.
This is not the same Hilbert object as a line over a length-two
algebra. The theorem neither assumes that nondominant maps lift to
normalizations nor claims that these are all components of the fibre.

\subsection{The multiplication input and the retained results}
For the determinant-apolar algebra $B_{n,h}$, the coefficient ideal
of a power satisfies
\[
 J_{hq+s}(A)=I_q(A)^{h-s}I_{q+1}(A)^s,
                          \qquad0\leq s<h,
\]
over every complex base algebra (Theorem~\ref{thm:universal-power-v157}).
This is an equality of ordinary ideals, not a statement only about
radicals, integral closures or geometric fibres. Its simultaneous
graph is complete quadrics. On the corank-two rank open the ideal
$J_{h(n-2)+1}$ is exactly $I_{n-1}$. The new Hilbert charts therefore
resolve actual multiplication systems. Proposition
\ref{prop:Artin-powers-v162} makes their full coefficient modules
explicit over nonreduced contact algebras. The choice $h=1$ is
distinguished when no auxiliary exponent is desired.

The full reduced-incidence theorem remains in the main text. It
identifies $\widehat G$ there with the blow-up of
$\Fitt_0(q_*\OO_D)$ and gives entire fibres $(\Pj^1)^k$.
The all-order Jordan slices, their transverse $A$-type singularities,
ramified normalizations and stable-map tails also remain. They
are exact specializations, not a substitute for the ambient contact
charts. All-rank power graphs, singular-pencil data, ordinary
higher-corank collisions and the reciprocal-fibre results retain
their complete proofs in the appendices.

\subsection{Related constructions and logical dependence}
Complete quadrics and their rank blow-ups are classical
\cite[Remark~2.5 and Construction~2.6]{Massarenti2020}.
Congruence-miniversal deformations of symmetric pencil pairs are
known \cite[Theorem~2.1]{Dmytryshyn162}. Our ambient realization
calculation is consistent with those parameter counts; it is not
claimed as the first miniversal pencil classification.
Hu--Lin--Shao construct a smooth compactification of parameterized
maps from $\Pj^1$ using resultant strata and exterior-map graphs
\cite[Theorem~1.1]{HuLinShao162}. Their moduli object is not the
embedded Hilbert graph used here. Chung--Hong--Kiem compare
Kontsevich, Simpson and Hilbert compactifications of rational curves
\cite{ChungHongKiem162}; their degree-two comparison illustrates why
maps and embedded limits must be distinguished. These precedents
motivate a theorem-level distinction of moduli objects, rather than
a claim of novelty based on an unsuccessful title search.

The new assertions are the open division charts with their Hilbert
inverse, their ambient realization and gcd fibre law, and the
non-equidimensional pencil fibre. The familiar congruence, Rees,
Cartier-flatness and normalization facts are credited as inputs.
The sharp inverse in the companion is not used to prove these
boundary theorems. Their interpretation for failure-algebra families
does use that inverse on the effective image. It is neither a new
closed-point Torelli statement nor a claim about all raw Artin-algebra
deformations. Finally, the theorem/proof-level comparison with
Ballico's 1993 failure-locus paper \cite{Ballico93} remains limited
by unavailable full text; the accessible 1996 comparison retained
in the companion does not remove that limitation.
'''
MASTER_ABSTRACT=I_ABSTRACT+r''' The paired geometry now includes ambient
versal contact coordinates, open Euclidean Hilbert charts with an exact
gcd collision law, and a non-equidimensional fibre with thick-line and
reduced-conic limits. The master preserves both complete mathematical
bodies and is not a third submission.'''
MASTER_INTRO=old.MASTER_INTRO+r'''
The new boundary reading route is Theorem~\ref{thm:ambient-versal-v162},
Theorem~\ref{thm:division-chart-v162}, Theorem~\ref{thm:ambient-jet-tails-v162}
and Theorem~\ref{thm:nonequidimensional-v162}. Their proofs pass from
full contact coordinates to an embedded Hilbert inverse and then to
two different-dimensional ambient fibre components. The additional
technical section expands the earlier descent, normality, coefficient
and deformation arguments without deleting their statements.
'''
DISCLOSURE=''
BIB=r'''\bibitem[Dmytryshyn(2011/2018)]{Dmytryshyn162}
A. Dmytryshyn, \emph{Miniversal deformations of pairs of symmetric
matrices under congruence}, arXiv:1104.2530, version 2 (2018),
Theorem~2.1, Corollary~2.1 and Lemma~3.1;
\url{https://arxiv.org/abs/1104.2530}.
\bibitem[Hu--Lin--Shao(2011)]{HuLinShao162}
Y. Hu, J. Lin and Y. Shao, A compactification of the space of algebraic
maps from $\Pj^1$ to $\Pj^n$, \emph{Comm. Anal. Geom.}
\textbf{19} (2011), 1--30; arXiv:math/0701255.
\bibitem[Chung--Hong--Kiem]{ChungHongKiem162}
K. Chung, J. Hong and Y.-H. Kiem, \emph{Compactified moduli spaces
of rational curves in projective homogeneous varieties},
arXiv:1010.0068; \url{https://arxiv.org/abs/1010.0068}.
\bibitem[Stacks Project]{Stacks162}
The Stacks Project Authors, \emph{The Stacks Project},
Tags 062Y (relative effective Cartier divisors), 02LS (finite morphisms),
and 0806 (the blow-up universal property),
\url{https://stacks.math.columbia.edu}, accessed September 25, 2026.
'''
