# Independent Referee Report — Round 15

**Manuscript:** D1 — *Deterministic Theta Contractions*  
**Submitted revision branch:** `revision/round15-referee-positive-closure-11paper-2026-09-01`  
**Locked branch commit:** `e25e565cc15ae65693c87eda37fd3a1f29357ecd`  
**Locked tree:** `d3c54fc19f0881ce3d38253f62ca3215fbf5000c`  
**Actual controlling module at review lock:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject; remove as a standalone submission**

## Evidence and submission integrity

The branch contains no Round-Fifteen D1 source or certificate. The paper still inputs Round Fourteen. The purported publication commit therefore does not provide a new D1 manuscript for peer review.

## Executive assessment

Positive measurable basin labels and log-sum-exp aggregation are preferable to signed spectral labels and linear averaging. The controlling text nevertheless has an explicit sign error in the restricted pressure and does not construct horizon-consistent, adapted phase labels capable of supporting component semigroups. Its component LDP and analytic chart theorems assume the hard platform-specific results that remain open upstream.

D1 remains a conditional synthesis rather than an independent theorem.

## Decisive objections

### 1. The restricted-pressure identity has the wrong sign

Let

\[
w_{n,j}=P(J_n=j),\qquad
\alpha_{n,j}=-\frac1n\log w_{n,j},
\]

and

\[
\widetilde Q_{n,j}(F)
=\frac1n\log E[e^{nF}\mid J_n=j].
\]

Then exactly

\[
\begin{aligned}
Q^{\rm un}_{n,j}(F)
&=\frac1n\log E[e^{nF};J_n=j]\\
&=\frac1n\log w_{n,j}+\widetilde Q_{n,j}(F)\\
&=-\alpha_{n,j}+\widetilde Q_{n,j}(F).
\end{aligned}
\]

The manuscript writes \(-n^{-1}\log w_{n,j}+\widetilde Q_{n,j}\), which is \(+\alpha_{n,j}+\widetilde Q_{n,j}\). Later formulas use the opposite, correct convention. The central pressure bookkeeping is internally inconsistent.

### 2. A full-horizon basin label is anticipative

The label \(J_n\) is defined from the complete path order parameter \(M(X_n)\). At an intermediate time \(t<n\), this label can depend on future observations and is not shown measurable with respect to the current filtration.

A fixed-horizon law can always be disintegrated by such an event. That does not produce causal component transition kernels or semigroups. To claim component dynamic evolution, the paper needs labels consistent under restriction and concatenation, or an augmented posterior over eventual labels with explicit Bayes updates.

### 3. Labels are not shown consistent as the horizon changes

The Voronoi basins are defined using rate components of a limiting full-horizon order parameter. There is no proof that \(J_n\) is the restriction or refinement of \(J_m\) for \(m<n\), nor that projected finite-time labels form a projective process. “The label is unchanged under every finite observable projection” does not address changing the observation horizon.

### 4. Component LDPs are assumed through internal recovery

Defining

\[
I_j(x)=\lim_{\varepsilon\downarrow0}
\inf\{I(y)-\alpha_j:y\in G_j,d(x,y)<\varepsilon\}
\]

creates a candidate basin-internal envelope. It does not prove that the conditioned microscopic laws have that rate. The key lemma simply invokes A3 or B2 recovery and says it can be kept inside the open basin. Those upstream full recovery theorems are not proved, and boundary components need separate topology and recovery.

### 5. The analytic component chart is not obtained from a real rate gap alone

A real LDP gap outside a cutoff does not automatically yield a complex zero-free partition function. Complex contributions can cancel. The manuscript invokes a positive killed transfer operator for A3 and an inserted coefficient for B2/B1, but neither component operator/coefficient is constructed with the basin label. Rouché's theorem applies only after a quantitative complex relative error is proved.

### 6. Log-sum-exp is correct but not a new closure theorem

The finite identity

\[
\frac1n\log\sum_j e^{n[-\alpha_{n,j}+V_{n,j}]}
\]

and its maximum limit are elementary once a genuine positive disintegration exists. The difficult work is establishing the component laws, their LDPs, response charts, conditioned coefficients, and dynamic consistency. D1 assumes those results from A2–C2.

### 7. The phase-conditioned Gaussian statement is incomplete at ties

At coexistence, the limiting distribution can be a mixture whose weights depend on subexponential factors and on the conditioning sequence. A mixture of Gaussians is generally not described by one covariance or one Cameron–Martin space. The text acknowledges mixtures but then speaks of commuting Gaussian tangents without constructing the labelled joint convergence needed to identify the weights and centers.

### 8. The title overstates mechanical theta selection

Even componentwise, a preparation Lagrange multiplier and a risk-sensitive valuation coefficient are not identical without an explicit compatibility axiom. Phase decomposition does not supply that missing identification.

## Required reconstruction

Remove D1 as a standalone paper. If upstream platform papers eventually prove positive component LDPs and adapted label dynamics, include the correct sign and log-sum-exp formulas as a synthesis section. Define phase labels at the law/filter level rather than by an anticipative terminal path event.

## Recommendation

**Reject; remove as a standalone submission.** The submitted Round-Fifteen paper is absent, the controlling pressure formula contains a sign error, and the dynamic phase decomposition is not causal or horizon-consistent.
