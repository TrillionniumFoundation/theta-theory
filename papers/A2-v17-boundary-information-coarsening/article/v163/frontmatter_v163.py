"""Front matter for complete v163 manuscripts. Prior front matter is archived."""
from pathlib import Path
import importlib.util
p=Path(__file__).resolve().parent.parent/'v162'/'frontmatter_v162.py'
spec=importlib.util.spec_from_file_location('front162',p)
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
I_ABSTRACT=old.I_ABSTRACT+r''' On the first nonreduced corank-two boundary,
the effective-family application determines the whole Hilbert fibre,
its two component types, their intersections, and its nilpotent ideal.'''
I_INTRO=old.I_INTRO.replace('sec:paper-i-v162','sec:paper-i-v163')+r'''
\subsection{Complete fibres of effective families}
The companion's Theorem~\ref{thm:complete-fibre-v163} determines the
entire first nonreduced contact fibre, rather than only its primitive
open and a family in its complement. Its reduced components are
$\Pj^4$ and $\mathbb F_2$, meeting along the doubled-line
$\Pj^1$. The local equation $(eA,eB,e^2C)$ also exhibits a
square-zero nilpotent ideal. Theorem~\ref{thm:product-fibres-v163}
then determines all fibres whose smaller corank-two Smith exponents
are at most two, with arbitrary larger exponents and any number
of distinct contacts. Corollary~\ref{cor:effective-full-fibres-v163}
transports this scheme-level description through the effective
family inverse. This transfer is an application, not a premise
of the sharp inverse or an assertion about every raw Artin-algebra
deformation. Proposition~\ref{prop:linearized-envelope-v163}
specifies the linearization splitting the envelope automorphism
extension. No external independent proof audit of the whole sharp
inverse is claimed by the present manuscript.
'''
II_TITLE='Power ideals and the Hilbert boundary of quadratic pencils'
II_ABSTRACT=r'''We determine complete scheme fibres of the Hilbert graph of lifted
quadratic pencils along the first nonreduced corank-two boundary.
The local fibre of contact length two has exactly two reduced
components, a projective four-space of conic tails and a Hirzebruch
surface compactifying primitive line jets. They meet along the
projective line of doubled tails. At that locus its equation is
$(eA,eB,e^2C)$, which records a square-zero nilpotent ideal invisible
in its reduced support. For several contacts of lengths one and
two, with arbitrary larger Smith exponents, the whole fibre is the
product of these local schemes. This determines all components,
intersections, dimensions and nilpotence orders in that class.
The proof constructs a Hilbert--Burch graph chart with a regular
inverse and an explicit fixed-target comparison on completed
embedded deformation functors. The underlying multiplication
ideals are balanced products of symmetric minor ideals over
arbitrary complex base algebras.'''
II_INTRO=r'''\section{Introduction}
\label{sec:paper-ii-v163}
An embedded limit of pencil curves retains more than its degree or
its reduced support. Already at contact length two, a thick line
and a plane conic lie in different components of one Hilbert fibre.
The components meet, but their reduced union still does not describe
the fibre: a nilpotent ideal is supported on singular conic tails.
We determine this fibre completely and then its independent-contact
products. The argument supplies both the component geometry and
the scheme structure with which it occurs in a fixed target.

Let $V$ have dimension $n$, $G=\Gr(2,\Sym^2V)$, and
$\pi:\mathrm{CQ}(V)\to\Pj(\Sym^2V)$ be complete quadrics.
On the dense open of regular pencil lines avoiding corank two,
the lifted lines have Hilbert polynomial $\binom n2l+1$ for
$\bigotimes_{q=1}^{n-1}H_q$, where $H_q$ is the resolved exterior
hyperplane bundle. Let $\widehat G$ be the normalization of the
\emph{total reduced graph} of the map to this Hilbert scheme.
Our fibres are scheme fibres of $\widehat G\to G$, not
normalizations of individual fibres. The target is fixed; no
ambient automorphism quotient is taken.

\subsection{The first nonreduced fibre}
The polynomial contact base $B_2$ consists of triples $(f,g,r)$,
where $f$ is monic quadratic and $g,r$ have degree at most one.
The reduced graph $\Gamma_2$ retains this triple and the graph
curve in $\Pj^1\times\Pj^2$, with polarization $\OO(1,1)$ and
Hilbert polynomial $3l+1$. Write $X_2$ for the fibre at
$(x^2,0,0)$ of the normalization of this total graph.
Theorem~\ref{thm:complete-fibre-v163} proves
\[
 (X_2)_{\rm red}=\Pj^4\ \cup_{\Pj^1}\ \mathbb F_2.
\]
The first component parametrizes all conics through the attachment;
the second compactifies $J_1(\Pj^1)=\operatorname{Tot}(\OO(2))$.
Their common projective line consists of doubled lines and is the
negative section of $\mathbb F_2$. Near a doubled line the full
fibre has completed local ring
\[
 \C[[\lambda,e,A,B,C]]/(eA,eB,e^2C).
\]
Its nilradical is $(eC)$ and has square zero. Its support inside the
conic component is the locus of conics singular at the attaching
point. In particular normalization of the total space does not
make this fibre reduced.

The proof is not a classification by selected arcs. The minors of
one explicit $3\times2$ matrix give a flat Hilbert--Burch family.
Quadratic and bilinear equation bundles recover its six parameters
regularly, proving that it is an open graph chart around every
conic tail. Its central fibre gives the displayed ideal. The
primitive jets compactify inside the same chart; their reciprocal
slope gives an algebraic specialization to a doubled line.
The resulting two proper component families form an open as well
as closed subset of the fibre. Connectedness from Stein
factorization proves exhaustion. The primary decomposition then
recovers the nilpotents and embedded associated prime.

\subsection{Complete products and adjacency}
For a regular pencil with no corank at least three, let its
positive corank-two Smith exponents be $(a_i,b_i)$, $a_i\leq b_i$.
Suppose $a_i\in\{1,2\}$, with $r$ occurrences of two and $s$
occurrences of one. There is no additional restriction on $b_i$.
Theorem~\ref{thm:product-fibres-v163} gives, after local frames,
\[
             (\widehat G)_{R_0}\simeq X_2^r\times(\Pj^1)^s
\]
as schemes. Its $2^r$ reduced components are indexed by choosing a
conic or a jet component at each length-two support. A component
with $j$ conic choices has dimension $s+2r+2j$. All intersections
are the products obtained by replacing differing choices by the
doubled-line projective line. The nilradical has exact nilpotence
order $r+1$ when $r>0$. These statements include the whole fibre
in the indicated class, not only its primitive open. For larger
contact lengths the earlier division charts and their gcd law
remain available; Proposition~\ref{prop:resultant-strata-v163}
adds codimensions of their gcd-partition strata. A further
component conjecture is explicitly separated from the theorems.

\subsection{The fixed-target proof and multiplication}
A parameter-dependent congruence is not a constant automorphism
of $\mathrm{CQ}(V)$. Proposition~\ref{prop:embedded-functors-v163}
compares embedded quotient functors in the relative incidence
target, retains the pencil parameter, and undoes the congruence
before returning to the fixed Hilbert target. Its patching lemma
uses the flat-completion case of formal gluing
\cite[Proposition~5.6(4), Example~5.8]{Bhatt163}, which permits
torsion at the contact. Algebraic ideal families are constructed
before completed local rings are compared. Thus formal miniversal
coordinates are not silently treated as algebraic morphisms.

The global power identity
\[
       J_{hq+s}(A)=I_q(A)^{h-s}I_{q+1}(A)^s,\qquad 0\leq s<h,
\]
is an ordinary ideal equality over every commutative complex
algebra. It supplies the graph and its Artin coefficient structure.
The representation-theoretic and determinantal ingredients and
the ambient complete-quadric construction are classical and are
credited in their proofs. The new fibre theorem concerns the
specified embedded Hilbert graph, its complete component structure
and its nilpotent fibre equations, not a new construction of
complete quadrics.

\subsection{Related compactifications and dependencies}
Hilbert graphs, stable maps, stable quotients and quasimaps retain
different boundary objects. The stable-quotient construction of
\cite{MOP163} and the stable-quasimap spaces of \cite{CFKM163}
compactify map problems using quotient or section data and
stability conditions; the latter paper also treats a parametrized
component. The comparison space of \cite{Manolache163} relates
stable maps and stable quotients. These works are not being
replaced by a new general compactification theorem here. Our
question is the scheme fibre of a retained-coefficient embedded
Hilbert graph; its thick tails and its nilpotents cannot be read
merely from the image cycle of a stable map. Determinantal
presentations of low-degree rational-curve Hilbert spaces are
also classical, as recalled in \cite[\S1.1--1.2]{LLMS163}. We use that
method of equations but prove the specific chart and fibre
identifications needed here directly.

The contact comparison uses the classical congruence deformation
principle recalled in \cite{Dmytryshyn162}. The fibre and ideal
proofs for a given pencil do not require the sharp failure-algebra
inverse in the companion. Their interpretation for unmarked
failure families explicitly does use that inverse, and remains
restricted to its effectively rigidified image. The exponent
$h=1$ requires no auxiliary choice; larger $h$ give the same graph.
The closest named failure-locus predecessor, Ballico's 1993 paper,
has not been obtained at theorem/proof level through the legitimate
sources inspected. No nonanticipation or broad historical priority
conclusion is inferred from that limitation. Likewise no new
external independent audit of the companion's long inverse proof
is claimed.

The main text follows the power construction, the fixed-target
comparison and the complete fibre theorem. The reduced-incidence,
higher-contact, reciprocal-fibre and singular-pencil results are
kept with their full proofs in the supplementary sections. The
class of complete fibres treated here is specified by $a_i\leq2$;
higher corank and singular pencils in the Hilbert problem are not
included by implication.
'''
MASTER_ABSTRACT=r'''We reconstruct quadratic pencils from their sharp unmarked finite
failure algebras and analyze the associated multiplication graphs.
The complete first nonreduced Hilbert fibre has reduced components
$\Pj^4$ and $\mathbb F_2$ meeting along doubled lines, together with
a square-zero nilpotent ideal. Products give all fibres with smaller
corank-two Smith exponents at most two. An explicit Hilbert--Burch
chart, a fixed-target embedded comparison, and a connectedness
argument establish the full scheme statement. This master contains
the complete proofs of both companion papers and their supplementary
results.'''
MASTER_INTRO=r'''\section*{The paired manuscripts}
\label{sec:introduction-v153}
The sharp inverse is the main theorem of the first paper. The second
paper's new main results are
Theorems~\ref{thm:complete-fibre-v163} and
\ref{thm:product-fibres-v163}, based on
Proposition~\ref{prop:embedded-functors-v163} and
Lemma~\ref{lem:HB-family-v163}. This unified source is a preservation
master, not a third submission. Prior proof blocks are retained,
while the focused companion sources provide the primary reading order.
The effective-family application uses reconstruction; it does not
assert an internal boundary operation before it. The Ballico 1993
full-text comparison and an external independent audit of the whole
inverse proof remain uncompleted.
'''
BIB=r'''\bibitem[Bhatt(2014)]{Bhatt163}
B. Bhatt, \emph{Algebraization and Tannaka duality},
arXiv:1404.7483, 2014, Theorem 1.4 and \S5.
\bibitem[Marian--Oprea--Pandharipande(2011)]{MOP163}
A. Marian, D. Oprea, and R. Pandharipande,
\emph{The moduli space of stable quotients}, Geom. Topol.
\textbf{15} (2011), 1651--1706; arXiv:0904.2992.
\bibitem[Ciocan-Fontanine--Kim--Maulik(2011)]{CFKM163}
I. Ciocan-Fontanine, B. Kim, and D. Maulik,
\emph{Stable quasimaps to GIT quotients}, arXiv:1106.3724, 2011.
\bibitem[Manolache(2013)]{Manolache163}
C. Manolache, \emph{Stable maps and stable quotients},
arXiv:1301.4393, 2013.
\bibitem[Lahoz--Lehn--Macr\`i--Stellari(2016)]{LLMS163}
M. Lahoz, M. Lehn, E. Macr\`i, and P. Stellari,
\emph{Generalized twisted cubics on a cubic fourfold as a moduli
space of stable objects}, arXiv:1609.04573, 2016.
\bibitem[Stacks Project]{Stacks163}
The Stacks Project Authors, \emph{The Stacks Project},
Lemma 37.53.6 (connected fibres of a proper birational morphism)
and Lemma 41.11.3 (completed local criterion for etaleness),
\url{https://stacks.math.columbia.edu}, accessed September 25, 2026.
'''
DISCLOSURE=''
