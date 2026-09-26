"""Front matter for the complete v167 manuscripts; no proof is replaced."""
II_ABSTRACT=r'''
We give a determinantal description of the retained-coefficient Hilbert
graph of polynomial contacts of every order. For a monic polynomial
$f$ of degree $a$ and two polynomials $g,r$ of smaller degree, an
explicit evaluation matrix in degree $a(a+1)/2+1$ has maximal minors
whose Rees blow-up is this Hilbert graph. The primitive minor vector
along a discrete valuation ring arc determines the entire embedded
limit and gives a finite jet bound for that arc. For exact monomial
coefficient arcs, the supports of these minors and their residue
cancellations give a finite decorated chamber classification. On the
nonsymmetric double-contact slice $(x^2,b,cx)$ we compute the model
completely: it is a smooth surface obtained by two point blow-ups,
with walls $\operatorname{ord}(b)=\operatorname{ord}(c)$ and
$\operatorname{ord}(b)=2\operatorname{ord}(c)$. We determine all five
resulting limit types, their multiplicities, and their scheme
structures. The comparison with horizontal modifications of parameter
families distinguishes strict base change from full pullback. The
power-ideal construction, the complete first nonreduced contact fibre,
and its extension algebra remain available in the same framework.
'''
II_INTRO=r'''
\section{Introduction}
\label{sec:paper-ii-v164}\label{sec:paper-ii-v166}\label{sec:paper-ii-v167}
An embedded limit of graphs contains more information than a limiting
cycle. At a common zero of the coordinate polynomials, a graph can
acquire a thick tail, a smooth conic, or a reducible conic, with the
same total degree. The coefficient orders alone can fail to distinguish
these alternatives. This paper studies the scheme structures of such
limits while retaining the coefficients and the fixed target.

Our main result is the determinantal Hilbert-state theorem, consisting
of Theorem~\ref{thm:determinantal-v167}, its finite determinacy
Proposition~\ref{prop:jet-v167}, and its monomial classification in
Theorem~\ref{thm:finite-fan-v167}. For the coefficient space
\[
 B_a=\{(f,g,r):f\text{ monic of degree }a,\quad\deg g,\deg r<a\},
\]
the generic graph in $\Pj^1\times\Pj^2$ has polynomial $(a+1)l+1$.
Put $m=a(a+1)/2+1$. The coefficient vectors of
$s^{m-i}t^i F_0^{j_0}F_1^{j_1}F_2^{j_2}$, with
$i=0,\ldots,m$ and $j_0+j_1+j_2=m$, form a matrix $M_a$.
The retained-coefficient Hilbert graph is the blow-up of the ideal
of its maximal minors. A primitive maximal-minor vector over a DVR
is the special Hilbert point. Thus the scheme of the embedded limit
is specified by finite linear algebra in one projective degree.
For a given arc, the least minor valuation plus one is a sufficient
coefficient-jet length. There is no uniform jet length even at
$a=2$; these assertions are compatible rather than contradictory.

For exact monomial coefficient arcs the supports of the minors give
a finite rational fan. Leading-coefficient cancellation is retained
by a finite locally closed partition of the residue torus. This gives
finitely many algebraic families of embedded limits, with explicit
projective coordinates on each piece; it is not a claim of finitely
many isomorphism classes as residues vary. It does not replace an
arbitrary formal arc by its leading monomials. The underlying
Hilbert immersion and graph blow-up are classical
\cite{Grothendieck166,Gotzmann167}; the explicit evaluation map,
its application to all $B_a$, and the calculated specialization
models are the content used here. The construction is not advertised
as a new representability theorem.

\subsection{A complete two-parameter model}
On $(f,g,r)=(x^2,b,cx)$ the answer becomes geometric without an
enumeration of minors. Theorem~\ref{thm:two-wall-v167} identifies
the horizontal graph over this slice with the blow-up of
$(b,c)(b,c^2)$, or two successive point blow-ups. Three affine
charts give every family and every overlap in the fixed target.
For $b=\beta\tau^p$ and $c=\gamma\tau^q$, the complete valued-arc table
\eqref{eq:slice-table-v167} has walls $p=q$ and $p=2q$.
It includes primitive double tails, a doubled conic, a smooth conic,
and a chain of reduced lines. The exceptional chain parametrizes
the transitions, and its self-intersections and relative canonical
divisor are computed. These are statements about a parameter
surface and embedded curves, not a stable-curve compactification.

\subsection{Two different Hilbert problems}
The graph $\Gamma_a$ parametrizes embedded curves of a fixed
polynomial. Its own fibres over $B_a$ need not have the same
polynomial. Consequently the horizontal Hilbert-main-component
modification for a family of these \emph{parameter fibres} is a
second construction, not another name for $\Gamma_a$.
Theorem~\ref{thm:basechange-v167} identifies strict base changes
of the latter horizontal construction and gives compatible maps
under iterated base change. Common refinements on one generic
open are supplied by Proposition~\ref{prop:refinement-v167}.
Different generic polynomials are not silently glued together.

For a regular symmetric pencil, the contact charts compare this
fixed-target polynomial problem with the Hilbert boundary of the
complete-quadric lift. The complete first nonreduced fibre,
the seven-chart presentation of arbitrary arcs, the square-zero
extension, and the ramified torsion computations supply the local
scheme-theoretic infrastructure. They are preserved here in full.
For higher contact order, the determinant theorem supplies the
whole graph and its embedded specializations, but a component,
normalization, and adjacency classification of every parameter
fibre remains a separate problem. This distinction is necessary
for reading the higher-contact statements correctly.

\subsection{Dependencies and publication units}
The proof dependencies for the main results are
\[
 \begin{gathered}
 \text{Gotzmann regularity and graph Rees algebra}\\
 \Longrightarrow\ \text{determinantal Hilbert graph and finite jets}\\
 \Longrightarrow\ \text{decorated coefficient chambers},\\[3pt]
 \text{division and Hilbert--Burch recovery}\\
 \Longrightarrow\ \text{three slice charts}\\
 \Longrightarrow\ \text{two walls and complete limit table}.
 \end{gathered}
\]
The horizontal comparison theorem uses relative Hilbert
representability and schematic density, not the sharp inverse of
Paper I. That inverse is used only afterward to obtain an
application to the effectively rigidified failure-family image.
Paper I and the present paper are distinct publication units;
the preservation master is not a third submission. The inherited
power and reciprocal material is retained in appendices rather
than removed from the mathematical record.

\subsection{Historical boundary of the claims}
State polytopes and initial ideals already organize torus actions
on Hilbert points \cite{BayerMorrison167}. Here the weighted
variables are input coefficients of a polynomial map and their
cancellations are kept. This difference of input is not offered
as a proof of nonanticipation. Likewise Hilbert-main-component
and pure-transform constructions are classical, while the full
pullback flattening functor is different. The theorem-level
comparison and its documentary limits are recorded alongside the
proofs. The complete text of Ballico's 1993 work has not been
obtained for a theorem-by-theorem comparison; no priority claim
that depends on such a comparison is made. No external independent
full audit of the sharp inverse is represented as completed.
'''
I_ADD=r'''
\subsection{Embedded specialization after the inverse}
The inverse theorem is logically prior to the boundary application.
The companion paper now identifies each polynomial contact Hilbert
graph with an explicit determinantal blow-up, proves pointwise finite
jet determination of embedded limits, and computes the two-wall
slice $(x^2,b,cx)$. Corollary~\ref{cor:effective-states-v167}
states the application after effective reconstruction. It is not an
operation on an arbitrary raw finite algebra without a specified
family. The sharp-inverse proof is unchanged; an independent external
proof audit and the full-text comparison with Ballico 1993 remain
separate obligations, not consequences of this application.
'''
BIB=r'''
\bibitem[Gotzmann(1978)]{Gotzmann167}
G.~Gotzmann, \emph{Eine Bedingung f\"ur die Flachheit und das
Hilbertpolynom eines graduierten Ringes}, Math. Z. \textbf{158}
(1978), 61--70, doi:10.1007/BF01214566.
\bibitem[Bayer--Morrison(1988)]{BayerMorrison167}
D.~Bayer and I.~Morrison, \emph{Standard bases and geometric invariant
theory. I. Initial ideals and state polytopes}, J. Symbolic Comput.
\textbf{6} (1988), no.~2--3, 209--217,
doi:10.1016/S0747-7171(88)80043-9.
'''
