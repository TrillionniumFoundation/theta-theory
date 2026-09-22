# Exact local-copy changes

Original sources remain unchanged. These are the complete changes to the two local copies; all other v9 core proof files are imported directly.

## effective-saturation.tex

```diff
--- v9/effective-saturation.tex
+++ v10/report-saturation.tex
@@ -1,4 +1,4 @@
-\section{The least saturated finite quotient}
+\section{Minimal posterior-and-report-predictive coordinates}
 \label{sec:v9-saturation}
 The variational theorem does not require a sufficient statistic. When
 such a statistic is desired, the finite instrument admits a direct
@@ -37,6 +37,8 @@
 in Section~\ref{sec:v8-sufficiency}. Additional latent-target marks
 require the corresponding conditional kernels as further decorations;
 parameter sufficiency alone does not imply their sufficiency.
+Sections~\ref{sec:v10-marked}--\ref{sec:v10-synthesis} supply the
+marked reconstruction theorem and an output-sensitive construction.
 
 Construct partitions backwards. At level $T$ group histories with the
 same vector $\lambda(h)$. Having constructed the class map $c_{t+1}$,
@@ -49,7 +51,7 @@
 For an unsupported continuation its class entry is one fixed cemetery
 symbol. Let $K_t$ be the number of classes at level $t$.
 
-\begin{theorem}[Constructive minimal saturation]
+\begin{theorem}[Minimal posterior-and-report-predictive coordinate]
 \label{thm:v9-saturation}
 For every finite controlled instrument the partitions
 \eqref{eq:v9-saturatedkey} form a saturated predictive coordinate. Every
@@ -61,8 +63,10 @@
 There is a parameter-independent finite reconstruction kernel
 $L_t(y\mid c,a,c')$ which, from successive quotient classes and the
 chosen controls, reconstructs the report stream under every admissible
-policy. The original and quotient instruments have mutually exact
-causal simulations. Their additional persistent state is at most
+policy. The original and quotient parameterized report experiments have
+mutually exact causal simulations. This assertion concerns reports and
+parameter likelihoods only; latent-target preservation is the separate
+marked statement of Theorem~\ref{thm:v10-reconstruction}. Their additional persistent state is at most
 $\max_tK_t$ labels, so composing either simulation with an $S$-state
 encoder costs at most $(\max_tK_t)S$ states.
 
```

## delayed-gaussian.tex

```diff
--- v9/delayed-gaussian.tex
+++ v10/delayed-gaussian.tex
@@ -25,6 +25,20 @@
 Let $\mathcal E_S$ be the infimal excess above $\beta$ when the total
 register has at most $S$ states at every stage. Independent shared
 randomness is permitted; the same conclusions hold without it.
+
+\begin{definition}[Delayed-query information signature]\label{def:v10-gaussian-signature}
+There are $d$ sequential scalar-acquisition updates
+$I_j=F_j(I_{j-1},X_j,U_j)$, followed by one query update
+$I_{d+1}=F_{d+1}(I_d,J,U_{d+1})$ and a terminal output
+$\widehat\theta=D(I_{d+1},U_{d+2})$. Each register has at most $S$
+values. The $U_j$ are independent private draws; an optional
+independent retained public seed may be an argument of every rule.
+The query is independent of the pre-query history, and neither $J$
+nor an old report is available to the terminal decoder except through
+$I_{d+1}$. The cardinality signature permits arbitrary measurable
+real arithmetic. Proposition~\ref{prop:v10-gaussian-precision} gives
+a distinct finite-acquisition and finite-table implementation.
+\end{definition}
 
 \begin{theorem}[Delayed Gaussian query law]\label{thm:v9-delayed}
 There are constants $0<c_{d,\sigma}\le C_{d,\sigma}<\infty$ such that
```
