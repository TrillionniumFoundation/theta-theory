# Exact preservation and local annotations — v13

All 290 entries of the inherited v12 source closure remain byte-identical. No original file is overwritten. The new canonical article is followed in the complete companion by the whole v12 mathematical core and all older bodies it preserved. `preserved-core.tex` relocates local input paths only, except that it selects the two annotated copies below. The v12 supporting-theory prose is retained as historical text. The build checks every label from the v12 complete-development auxiliary file and identical numbering of the new canonical statements in both views.

The source archive additionally retains old drivers, front matter, references, audits, code and manifests even where they are not typeset twice. No predecessor theorem or proof is omitted from the complete companion.

## Exact changes in local annotated copies

The first copy adds a differentiability clarification, a precise classical attribution, a passive-scope sentence, and the fixed row-interface clause. The second changes only the summability qualifier of its theorem heading. The original v12 files stay unchanged.

```diff
--- v12/operator-memory.tex
+++ v13/operator-memory-annotated.tex
@@ -93,7 +93,9 @@
  y(t)&=T_Q(t)Qf+\int_0^t T_Q(t-s)Cx(s)\,ds.
 \end{align*}
 The first expression is continuously differentiable because $A$ is
-bounded and $By(s)$ is continuous. Substituting the second proves
+bounded and $By(s)$ is continuous. In particular this differentiation
+uses the bounded block integral formula, not a derivative of $U(t)f$
+for an arbitrary $f\notin D(L)$. Substituting the second proves
 \eqref{eq:v12-volterra}--\eqref{eq:v12-kernel} for every $f\in H$.
 Contractivity gives \eqref{eq:v12-kernel-bound}. The operator-valued
 kernel is norm continuous, since $C$ has finite-dimensional domain and
@@ -198,6 +200,11 @@
 Let $P_n$ be their orthogonal projections and set $G_n=P_nLP_n$ on $H$.
 It is bounded and skew-adjoint; on $V_n^\perp$ it is zero.
 
+The stable graph-core resolvent approximation below is a specialization
+of Trotter's classical approximation theorem
+\cite[Theorem~5.2]{Trotter1958}; the proof spells out its core consistency,
+uniform contraction bound, and resolvent-to-orbit implication.
+
 \begin{theorem}[Microscopic graph-core Galerkin limit]
 \label{thm:v12-galerkin}
 For every $f\in H$ and every finite $T$,
@@ -256,6 +263,12 @@
 Trotter--Kato theorem.
 
 \subsection{The common-encoder limit for actual physical observations}
+
+\emph{Scope of this preserved physical theorem: fixed microscopic flow,
+passive observation control, fixed particle number and positive noise;
+no kinetic or Boltzmann--Grad limit. The active intervention theorem of
+Section~\ref{sec:v13-active} is a separate result.}
+
 Fix a family of initial densities $f_\theta$ with respect to $\mu$ such
 that
 \begin{equation}
@@ -347,7 +360,9 @@
 
 \begin{corollary}[Combining compact duality with microscopic approximation]
 \label{cor:v12-physical-duality}
-Assume in addition that the density family is continuous in $L^1(\mu)$
+In this corollary only the preparation density and the bounded losses
+vary with the row. The flow, observables, noise laws, and actual mark
+channel are fixed. Assume in addition that the density family is continuous in $L^1(\mu)$
 on a compact parameter space, and that the bounded row losses are
 uniformly continuous in their row index in supremum norm. With the
 finite task alphabets of Theorem~\ref{thm:v12-infinite}, both physical

--- v12/infinite-horizon.tex
+++ v13/infinite-horizon-annotated.tex
@@ -80,7 +80,7 @@
 resource; no finite storage bound is inferred from this realization.
 \end{proof}
 
-\begin{theorem}[Infinite-horizon common-encoder duality]
+\begin{theorem}[Summable infinite-horizon common-encoder duality]
 \label{thm:v12-infinite}
 Under the finite-prefix hypotheses above, the following statements hold.
 The private risk body $\mathcal R(S,1)=\{r(\pi):\pi\in K\}$ is compact

```
