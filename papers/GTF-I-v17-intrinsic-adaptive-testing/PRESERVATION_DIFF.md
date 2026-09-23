# Preservation map and exact local differences

No predecessor repository file is changed or deleted. INHERITED_INPUTS.json fixes all 402 inputs of the successful v16 source closure. All 812 labels in the v16 development are required in the new development. The sixteen mathematical modules in the prior canonical core are retained as local v17 copies; their original theorem labels remain. A local preamble makes the canonical article self-contained. The submission archive includes only canonical local inputs, not the historical archive or font files.

Three local mathematical copies differ: nonlinear-testing.tex (certificate terminology and classical credit), collective-hard-spheres.tex (collective collision-insensitivity and joint visible reference), physical-testing.tex (v15 attribution and uniform algorithmic hypotheses). They are clarified rather than removed. The following exact patches are applied only to the new local copies. New introduction, adaptive testing, collision gap, optional stability and dependency appendix are additional content. The complete development also preserves the old v16 introduction.

```diff
--- papers/GTF-I-v16-constructive-causal-certification/nonlinear-testing.tex
+++ v17/nonlinear-testing.tex
@@ -4,6 +4,8 @@
 can nevertheless be written as a limit of finite algebraic lower
 certificates, without replacing that image by randomized designs.
 The testing weights in this section depend on the candidate simulator.
+Unlike Theorem~\ref{thm:v17-dual}, this identity is a certificate
+transform, not an independent variational dual.
 They are universal proof functions, not a hidden selector supplied to
 an executed experiment.
 
@@ -29,7 +31,7 @@
 All $h_i$ are rational polynomials, $0\le g_i\le1$, and $g_1=1/2$.
 The case $D=0$ is a single feasible table and is interpreted directly.
 
-\begin{theorem}[Endogenous polynomial testing dual]
+\begin{theorem}[Strict polynomial lower-certificate hierarchy]
 \label{thm:v16-dual}
 For $p\ge1$ define
 \[
@@ -87,6 +89,11 @@
 strict positive uniform gap above $L$.
 \end{proof}
 
+\noindent Positive Bernstein certificates and their degree elevation are
+classical; see de Klerk--Laurent~\cite{deKlerkLaurent2010}. The next
+elementary bound is retained for a self-contained exact verifier, not
+as a new general hypercube positivity theorem.
+
 \begin{lemma}[An explicit positivity degree]
 \label{lem:v16-bernstein}
 Let $P(x)=\sum_k c_kx^k$ be a rational polynomial in $D$ variables and
@@ -143,21 +150,22 @@
 family conclusion uses only the same pointwise maximum argument.
 \end{proof}
 
-\begin{remark}[What is, and is not, dualized]
+\begin{remark}[Meaning and size of the strict certificate transform]
 A constant distribution on tests generally detects only the convex hull
 of the behavior image. The functions $g_i^p/\sum_jg_j^p$ are instead
 functions of a proposed row table. Their universally quantified weighted
 inequality is an algebraic certificate; the tester need not observe a
-private state in an experiment. The displayed dual is not an equality
+private state in an experiment. The displayed certificate identity is not an equality
 obtained by exchanging a private minimum with a fixed mixed test.
 Power means and Bernstein degree elevation are classical algebraic
 approximation devices, proved here in the precise form needed. The
-claim is the complete application to the original marked causal
+claim here is strict-level completeness for the original marked causal
 resource image, including visible selectors, and its physical transfer
 below. The coefficient count $(n+1)^D$, the number of original tests,
-and the algebraic degrees may be large. No polynomial complexity or
-intrinsic-dimension bound on coefficient count is asserted. The
-behavior-dimension witness theorem remains a separate useful bound.
+and the algebraic degrees may be large. No polynomial complexity or intrinsic-dimension bound on this
+row-cube coefficient count is asserted. The independent adaptive
+test has the separate behavior-size bound of
+Theorem~\ref{thm:v17-degree}; its verification is a different cost.
 \end{remark}
 
 \subsection{A sharp two-time nonconvex example}
```

```diff
--- papers/GTF-I-v16-constructive-causal-certification/collective-hard-spheres.tex
+++ v17/collective-hard-spheres.tex
@@ -4,8 +4,11 @@
 interacting hard-sphere system. It is neither a collision-free restriction
 nor an observable constant along the flow. Its explicitly solvable
 collective mode permits simultaneous evaluation of a nonzero generator
-residual and of a marked decision deficiency. This distinguishes the
-example from the two separate constructions of the preceding section.
+residual and of a marked decision deficiency. The orbit factors through total momentum, so collisions cancel from
+this particular observable. The residual measures projection error,
+not interaction strength. The collision-sensitive comparison is proved
+in Section~\ref{sec:v17-collision}; the solvable collective calculation
+is retained here as a separate exact benchmark.
 
 Fix $N\ge2$ equal-mass hard spheres on the square flat torus of side
 $\ell>0$, with positive admissible configuration volume. Velocities
@@ -179,8 +182,11 @@
 
 \begin{theorem}[Exact marked physical deficiency]
 \label{thm:v16-exactphysical}
-For every nonempty finite private, hidden-selector, or visible-selector
-signature in this one-acquisition model, its intrinsic deficiency equals
+Here the action precedes any informative report and its reversal
+symmetry leaves the relevant marked law unchanged. In the visible
+comparison the independent selector is retained jointly with the same
+selector law on the target side. For every nonempty finite private,
+hidden-selector, or visible-selector signature in this one-acquisition model, its intrinsic deficiency equals
 \begin{equation}\label{eq:v16-delta}
  d(\tau)=\mathbb E\bigl[W\{\Phi(\cos(\vartheta+\tau X))-1/2\}\bigr]>0.
 \end{equation}
```

```diff
--- papers/GTF-I-v16-constructive-causal-certification/physical-testing.tex
+++ v17/physical-testing.tex
@@ -2,6 +2,9 @@
 \label{sec:v16-joint}
 The finite testing and microscopic approximation results now give a
 single lower--upper certificate for the original resource problem.
+The stateless transfer inequality and physical-to-rational bridge
+are those of Theorem~\ref{thm:v15-main}; the polynomial lower module
+is a separate strengthening, not a new physical transfer principle.
 Unlike a constant mixture of tests, the polynomial lower certificate
 can separate a target from a private behavior image even when the
 target belongs to its convex hull.
@@ -12,7 +15,10 @@
 visible-selector signatures. Let $E,F$ be marked physical acquisitions
 with finite compatible controls and marks. Suppose that rational finite
 presentations $E_j,F_j$ have executable two-sided stateless marked
-feedback errors $a_j,c_j\to0$, with computable upper bounds. Let
+feedback errors $a_j,c_j\to0$, with computable upper bounds. For the algorithmic assertion require
+the uniform enumeration and rational error enclosures of
+Proposition~\ref{prop:v17-effective}, not merely individual
+computability of each presentation. Let
 $P_{p,L}$ be the polynomial \eqref{eq:v16-positivepoly} of the finite
 intrinsic deficiency problem for $E_j,F_j$, and let a nonnegative
 rational Bernstein array certify it. Let an actual rational simulator
```

