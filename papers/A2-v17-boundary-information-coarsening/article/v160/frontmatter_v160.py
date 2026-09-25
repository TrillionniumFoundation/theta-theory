"""Focused front matter: all predecessor results and introductions are preserved."""
from pathlib import Path
import importlib.util
p=Path(__file__).resolve().parent.parent/'v159'/'frontmatter_v159.py'
spec=importlib.util.spec_from_file_location('front159',p)
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
I_ABSTRACT=old.I_ABSTRACT+r''' On the simple corank-two incidence open, the
multiplication diagram also recovers the centre and Rees algebra of
the Hilbert boundary modification; a first normal deformation selects
its embedded limit.'''
I_INTRO=old.I_INTRO.replace(r'\subsection{Relation to the companion paper}',r'''\subsection{The boundary centre as a multiplication invariant}
Theorem~\ref{thm:failure-incidence-v160} is an application with an
explicit geometric input from the companion. On the open of regular
pencils with at most one reduced corank-two incidence, the zero scheme
of $J_{h(n-2)+1}$ on the intrinsic pencil line is the incidence centre
itself. Its scheme ideal and Rees algebra are therefore recovered
from the multiplication diagram. The companion identifies their
Proj with the full normalized Hilbert incidence modification. For an
arc with nonzero normal derivative the first-order algebra determines
its exceptional point and its embedded tail. This is not a choice of
one tail from the closed algebra: that algebra has a full projective
line of possible boundary directions. The construction is made on
the effective first-relation image, where the inverse is a scheme
isomorphism, and descends along the oriented source torsor.

\subsection{Relation to the companion paper}''')
II_TITLE='Intrinsic power geometry and the boundary of quadratic pencils'
II_ABSTRACT=r'''Multiplication in a determinant-apolar algebra realizes balanced
products of symmetric minor ideals over every complex base algebra.
Its all-rank power graphs recover relative complete quadrics, and
power contacts together with finite syzygy maps recover the complete
data of arbitrary symmetric pencils. We identify the normalized
Hilbert incidence space, on the simple corank-two open in every
dimension, with the blow-up of a smooth codimension-two centre.
This determines the whole exceptional projective line, its nodal
universal family, its discrepancy, and all multiplication systems,
including residual directions tangent to the determinant conic.
The centre and its Rees algebra are intrinsic multiplication data
of the sharp failure family. For simultaneous ordinary collisions
of arbitrary multiplicities we retain the full nodal-tree calculation,
its exact power ideals and its residual-pencil moduli.'''
new=r'''\subsection{The full simple-incidence modification}
Let $\mathcal U\subset\Gr(2,\Sym^2V)$ be the open of regular pencils
whose lines avoid rank at most $n-3$ and meet rank at most $n-2$
in at most one reduced point. The locus $\Sigma_2$ of nonempty
intersection is smooth of codimension two. The normalized Hilbert
incidence modification satisfies
\[
       \widehat G|_{\mathcal U}
                 =\operatorname{Bl}_{\Sigma_2}\mathcal U
\]
(Theorem~\ref{thm:incidence-blowup-v160}). This is an identification
of the entire space over this open, not a chosen family in one fibre.
Over an incident line with intersection $p$, the fibre is the full
$\Pj^1$ of lines through the tangent-normal point in the exceptional
$\Pj(N_{Z_{n-2}/P,p})=\Pj^2$. Each parameter gives the strict
transform of the original line with one reduced nodal tail. Locally
the universal family is $xy=t$, with $t$ a boundary parameter, and
the exceptional divisor has discrepancy one. The identification
supplies a Cartier-ideal universal property.

All resolved multiplication systems on the exceptional plane are
complete Veronese systems of degrees
\[
             (j-h(n-2))_+-2(j-h(n-1))_+,
                    \qquad 1\leq j\leq hn
\]
(Proposition~\ref{prop:exceptional-powers-v160}). This includes every
exceptional direction, whether or not its residual determinant is
squarefree. The incidence centre is the image, as a closed subscheme,
of the zero scheme of $J_{h(n-2)+1}$ on the universal pencil line.
Consequently the centre's ordinary powers and their Rees algebra
come from the intrinsic multiplication diagram of the failure family
(Theorem~\ref{thm:failure-incidence-v160} in the companion).
A nonzero first normal deformation selects the actual embedded tail.
The geometry of the closed algebra and the additional direction in
its deformation family are thus distinguished precisely.

The proof uses classical smooth blow-ups and complete quadrics.
The assertion proved here is the identification with the specified
Hilbert graph, the classification of all its fibres over $\mathcal U$,
and its realization by failure multiplication. No novelty is assigned
to the general blow-up universal property or the ambient variety of
complete quadrics.

'''
II_INTRO=old.II_INTRO.replace(r'\subsection{Embedded boundary fibres}',new+r'\subsection{Embedded boundary fibres}')
MASTER_ABSTRACT=old.MASTER_ABSTRACT+r''' On the simple corank-two open in
every dimension, the entire normalized Hilbert incidence modification
is a smooth codimension-two blow-up, with centre and normal directions
recovered from failure multiplication.'''
MASTER_INTRO=old.MASTER_INTRO+r'''
Theorem~\ref{thm:incidence-blowup-v160} identifies the full incidence
modification on its simple corank-two open, including every residual
direction. Proposition~\ref{prop:exceptional-powers-v160} determines
all exceptional coefficient systems. Theorem~\ref{thm:failure-incidence-v160}
recovers the centre and its Rees algebra from the failure family's
multiplication and identifies the information in its first normal jet.
'''
BIB=r'''\bibitem[Stacks Project]{StacksProject160}
The Stacks Project Authors, \emph{The Stacks Project},
Tags 0806 (universal property of blowing up), 02LS (proper quasi-finite
morphisms), and 0H1G (smooth centres and their blow-ups),
\url{https://stacks.math.columbia.edu}, accessed September 25, 2026.
'''
DISCLOSURE=''
