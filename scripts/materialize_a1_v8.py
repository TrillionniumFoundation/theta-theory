from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'papers/A1-english-v8'
BASE=ROOT/'papers/A1-english-v7'
P.mkdir(parents=True,exist_ok=True)
# Only the new revision is materialized. The pinned predecessor is never edited.
for rel in ['main.tex','references.tex','build.sh'] + [str(x.relative_to(BASE)) for x in (BASE/'sections').glob('*.tex')]:
    target=P/rel
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(BASE/rel,target)
(P/'tests').mkdir(exist_ok=True)
shutil.copy2(BASE/'tests/test_v7.py',P/'tests/test_v7.py')
f=P/'main.tex'; s=f.read_text()
s=s.replace(r'\title[Confluent observation algebras and memory]{Sparse observation algebras, confluent directions,\\ and finite-state memory}',r'\title[Attainable resolution flags and memory]{Sparse observation algebras, attainable resolution flags,\\ and finite-state memory}')
s=s.replace('pdftitle={Sparse observation algebras, confluent directions, and finite-state memory}','pdftitle={Sparse observation algebras, attainable resolution flags, and finite-state memory}')
a=s.index(r'\begin{abstract}');b=s.index(r'\end{abstract}',a)+len(r'\end{abstract}')
s=s[:a]+r'''\begin{abstract}
For a positive finite detector spanning monomials with exponent set $A$,
we identify the generic attainable information dimension for $n$ past
and $m$ future observations as $\min\{n(|A|-1),|mA|-1\}$, for every
full-support prior. We determine its finite-resolution counterpart when
additive exponents coalesce in an affine calibration family. Order the
nonconstant future jet orders as $\nu_1\le\cdots\le\nu_q$ and put
$p=\min\{n(|A|-1),q\}$. The optimal $M$-message checkpoint regret has
uniform order
\[
 \max_{1\le\ell\le p}
    \theta^{2(\nu_1+\cdots+\nu_\ell)/\ell}M^{-2/\ell}.
\]
The initial $p$ orders, rather than the entire ambient list, govern the
law. A binomial product tangent is transverse to every initial resolution
flag; a bounded-format covering argument controls the whole attainable
image. Raw moment updates then yield the corresponding uniform streaming
law at every fixed horizon, with only $M$ persistent labels and no
division by $\theta$. For $A_\theta=\{0,1,2+\theta\}$ the five- and
seven-trial laws are respectively
$\max\{M^{-1/2},\theta^{2/5}M^{-2/5}\}$ and
$\max\{M^{-1/3},\theta^{1/2}M^{-1/4}\}$.
In a common binary decision task the budget needed to beat an exact
weak-coordinate-erased statistic has order $\theta^{-4}$.
Exact causal states, fixed-calibration control bounds, and a counted
mechanical collision-bit comparison are also established.
\end{abstract}'''+s[b:]
s=s.replace(r'\input{sections/06_streaming}',r'\input{sections/06_streaming}'+'\n'+r'\input{sections/06a_attainable_filtration}')
f.write_text(s)
f=P/'sections/05_confluence.tex';s=f.read_text().replace('For a fixed future length $m$, let', 'For a fixed positive future length $m\\ge1$, let')
s=s.replace('streaming bound across an entire singular family.',r'''streaming bound across an entire singular family. Theorem~\ref{thm:attainable-checkpoint}
below removes the full-future restriction by truncating the resolution flag,
and Theorem~\ref{thm:general-uniform-streaming} proves the fixed-horizon
causal version for the affine class. When $m=0$ there is no nonconstant
future query and the prediction regret is zero; formula
\eqref{eq:resolution-function} is not used in that case.''')
f.write_text(s)
f=P/'sections/01_introduction.tex';s=f.read_text();pos=s.index('The family $A_\\theta=')
new=r'''The full-future formula has a general attainable counterpart. Put
$p=\min\{n(r-1),d\}$. Theorem~\ref{thm:attainable-checkpoint} proves
\begin{equation}\label{eq:intro-attained}
 R_{M;n,m}^\theta\asymp
 \max_{1\le\ell\le p}
       \theta^{2(\nu_1+\cdots+\nu_\ell)/\ell}M^{-2/\ell},
\end{equation}
without the full-future inequality. The proof has two distinct parts.
The binomial tangent is transverse to every initial jet flag, including
at the collision. On the other hand, the complete reachable image is a
bounded-format rational image of normalized factor coordinates. A real
integral-geometric covering estimate truncates its entropy at its
attainable dimension even when the image is curved. Theorem~\ref{thm:general-uniform-streaming}
then proves that the maximum of \eqref{eq:intro-attained} over
$n+m=N$ is the uniform streaming law at any fixed horizon $N$.
Raw moments give uniformly Lipschitz transitions between its successive
reachable sets. No transversality assumption or global quotient chart
is added to obtain this conclusion.

This truncation changes the predicted exponent inside the same detector
family. At seven trials, the peak has eight attainable directions, whereas
the ambient future space has nine. Corollary~\ref{cor:seven-trial}
gives $\max\{M^{-1/3},\theta^{1/2}M^{-1/4}\}$, with six strong
and two weak directions. Counting all three ambient weak directions would
give a false nine-dimensional high-resolution exponent. The seven-trial
law is thus a consequence of the general attained geometry, not of the
full-future formula alone.

'''
s=s[:pos]+new+s[pos:]
s=s.replace('A singular coordinate system would not suffice to prove', 'Even in this smaller example, a singular coordinate system would not suffice to prove')
needle='quantitative value in one precisely specified sequential decision.'
s=s.replace(needle,needle+r''' Corollary~\ref{cor:necessary-budget}
also proves that order $\theta^{-4}$ is necessary for beating the
\emph{uncompressed} erased statistic. This is an operational consequence
of the resolved geometry and an exact score identity, not an independent
optimal-acquisition theory.''')
s+=r'''
\paragraph{The clustered spectral comparison.}
Batenkov, Diederichs, Goldman and Yomdin
\cite[Theorems 2.2--2.3 and Corollary 2.1]{BatenkovEtAl} study Fourier
Vandermonde matrices with separated clusters of nodes on the unit circle.
For a quasiuniform cluster their singular values, after a common
$N^{1/2}$ normalization, scale as $(Nh)^{j-1}$; the cluster
multiplicities determine how often each power occurs. Divided differences
also enter their limiting bases. We do not claim that the hierarchy of
integer collision powers is new.

The additional statement here concerns the image that an experiment can
actually produce. Theorem~\ref{thm:attainable-checkpoint} pairs a
normalized product tangent with the initial future jet flag for every
full-support prior, and converts that transversality into an unconditional
minorization retaining the acquisition probability. Its global upper bound
uses the dimension of the nonlinear reachable image rather than the
ambient spectral multiplicities. Theorem~\ref{thm:general-uniform-streaming}
adds a causal compatibility assertion: raw formal moments update with a
positive denominator and uniformly bounded derivatives, so the same
attained scales govern repeated finite-state compression. The spectral
comparison neither supplies these statements nor contradicts them.
The integral-geometric entropy inequality and bounded-format component
bounds used for the global upper estimate are classical
\cite{YomdinComte,ComteHalupczok,ZhangKileel}; their precise use is
isolated in Lemma~\ref{lem:tame-rectangle}.

The hierarchy of conclusions is therefore as follows. The class-wide
attainable theorem and its causal realization are the structural results.
The five- and seven-trial laws display distinct consequences of that same
classification. The ticket identity transfers one of these laws to a
common payoff and does not constitute a second source of geometric
independence. The earlier mechanical and control results remain available
with their complete proofs and their separate operational assumptions.
'''
f.write_text(s)
f=P/'sections/08_sequential_value.tex';s=f.read_text();s+=r'''

\begin{corollary}[Necessary and sufficient budget order]\label{cor:necessary-budget}
Define
\[
 M_{\rm beat}(\theta)=\min\{M\in\N:V_M^\theta>V_T^\theta\}.
\]
For $0<\theta\le1/2$ this minimum exists and
$M_{\rm beat}(\theta)\asymp\theta^{-4}$, with uniform constants.
More explicitly, for some $0<k<K<\infty$,
\[
 \begin{aligned}
 1\le M\le k\theta^{-4}&\quad\Longrightarrow\quad
 V_M^\theta-V_T^\theta\le-C_e\theta^2<0,\\
 M\ge K\theta^{-4}&\quad\Longrightarrow\quad
 V_M^\theta-V_T^\theta\ge\tfrac12c_e\theta^2>0.
 \end{aligned}
\]
The first assertion is vacuous if its integer range is empty.
\end{corollary}
\begin{proof}
Write $E_\theta=V_*^\theta-V_T^\theta$ and
$L_M^\theta=V_*^\theta-V_M^\theta$. Theorems already proved give
$E_\theta\le C_e\theta^2$ and $L_M^\theta\ge c_sM^{-1/2}$.
Their exact difference uses the same experiment and baseline, hence
\[
 V_M^\theta-V_T^\theta=E_\theta-L_M^\theta
             \le C_e\theta^2-c_sM^{-1/2}.
\]
Choose $k=(c_s/(2C_e))^2$, decreasing it if necessary so that $k<K$.
The first inequality follows. The second is
Theorem~\ref{thm:resolved-value}, with $K$ increased if needed.
The admissible filter classes are nested as $M$ increases because extra
states can be unused. Thus the first-crossing budget exists; the two
bounds and integer rounding give its stated order.
\end{proof}

This consequence was extracted in the source-pinned v7 referee technical
note \cite{A1v7note}. It concerns beating the exact, uncompressed
$T_\theta$ comparator. It does not locate an exact integer transition,
and it does not assert equality of the full and erased experiments at
smaller \emph{equal compressed} budgets. At zero $T_0$ is sufficient,
so no finite-state policy has value exceeding $V_T^0=V_*^0$.
''';f.write_text(s)
f=P/'sections/10_scope.tex';s=f.read_text();a=s.index('Uniformity in this paper has a specified range.')
s=s[:a]+r'''Uniformity in this paper has a specified range. The initial checkpoint
theorem assumes \eqref{eq:full-future-condition}; its extension in
Section~\ref{sec:attainable-flag} removes that restriction and gives a
uniform causal law for every fixed horizon in the affine calibration
class, on a compact interval without positive crossings in the relevant
formal future sumsets. The five- and seven-trial consequences hold on
the entire stated interval $[0,1/2]$; the seven-trial proof explicitly
allows irrelevant longer-sumset crossings. The binary-decision comparison
uses the same five-trial prescribed acquisition problem as before.
Constants may depend on the fixed full-support prior and physical
protocol. No prior-uniform or horizon-uniform lower constant, computable
synthesis from approximate moment data, or arbitrary non-affine collision
classification is asserted. Nor is the history erasure $T_\theta$
identified with a one-step mechanical sign erasure. These distinctions
specify the objects being compared without removing any positive theorem.
''';f.write_text(s)
f=P/'references.tex';s=f.read_text().replace(r'\end{thebibliography}',r'''
\bibitem{BatenkovEtAl}
D. Batenkov, B. Diederichs, G. Goldman and Y. Yomdin,
\emph{The spectral properties of Vandermonde matrices with clustered nodes},
arXiv:1909.01927v2 (2020), Theorems 2.2--2.3 and Corollary 2.1.
\url{https://arxiv.org/abs/1909.01927}.
\bibitem{YomdinComte}
Y. Yomdin and G. Comte, \emph{Tame Geometry with Application in Smooth
Analysis}, Lecture Notes in Mathematics 1834, Springer, Berlin, 2004.
\bibitem{ComteHalupczok}
G. Comte and I. Halupczok, \emph{Motivic Vitushkin invariants},
arXiv:2206.15412v2 (2024). The classical real variations and entropy
inequality used here are recalled in the introduction, equations (4)--(5).
\url{https://arxiv.org/abs/2206.15412}.
\bibitem{ZhangKileel}
Y. Zhang and J. Kileel, \emph{Covering Number of Real Algebraic Varieties
and Beyond: Improved Bounds and Applications}, arXiv:2311.05116,
Lemma 2.18. \url{https://arxiv.org/abs/2311.05116}.
\bibitem{A1v7note}
\emph{What the v7 theorems imply, and where their hypothesis matters},
technical note accompanying the owner-requested AI-assisted A1 v7
repository review, September 6, 2026,
\href{https://github.com/TrillionniumFoundation/theta-theory/blob/72eb41e358bd9af122367fea66d0de9bdda07456/reviews/a1-english-v7-2026-09-06/TECHNICAL_NOTE.md}{commit \texttt{72eb41e358bd}}.
This note gives the necessary-budget deduction and the seven-trial
past-limited boundary, not the attainable-flag classification proved here.
\end{thebibliography}''');f.write_text(s)
f=P/'build.sh';s=f.read_text().replace('"$PYTHON" tests/test_v7.py','"$PYTHON" tests/test_v7.py\n"$PYTHON" tests/test_v8.py').replace('A1 v7 principal','A1 v8 principal');f.write_text(s)
