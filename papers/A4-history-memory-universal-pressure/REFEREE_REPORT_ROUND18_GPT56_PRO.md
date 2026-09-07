# Referee Report — Round 18 (Independent Harsh Review)

**Paper:** A4 — *Exact History Dynamics, Domain-Safe Memory, and Universal Excess Path Pressure*  
**Version reviewed:** `revision/round17-referee-positive-closure-11paper-2026-09-01@d13b48757f85d9ec1c6998f89c861845094891fa`  
**Controlling source:** `ROUND17_POSITIVE_CLOSURE.tex` (`A4_GLOBAL_HARRIS_FORCED_MEMORY.tex`)  
**Date:** 1 September 2026  
**Editorial recommendation:** **REJECT**  
**Present mathematical status:** Neither the claimed global spectral platform nor the renewal/memory theorem is established.

## 1. Overall assessment

The revision makes two useful conceptual corrections. It no longer patches genuinely different transition kernels with a partition of unity, and the Mori–Zwanzig formula retains the contribution from an unresolved initial component rather than silently setting it to zero. The finite-dimensional right-half-plane accretivity observation for a compressed resolvent is also potentially valid under appropriate fixed-domain assumptions.

The paper nevertheless promotes several hypotheses to the status of proved theorems without supplying the estimates. In particular, summable variation is strengthened to exponential variation, a weak-Harris contraction is promoted to an operator spectral gap, a class that is not an algebra is called a multiplier algebra, and an A2 scalar matrix-coefficient estimate is promoted to operator-valued meromorphic continuation and exponential memory decay. The main theorem package is therefore not proved.

## 2. Decisive mathematical objections

### 2.1. [FATAL] Summable variation does not imply the exponential coupling estimate in `lem:r17-a4-coupling`

The paper assumes only

\[
\sum_{n\ge1}\operatorname{var}_n(\log g)<\infty.
\]

It then concludes that histories agreeing through depth `N` have next-edge kernels at total variation distance at most `Ce^{-cN}`. This is false without an exponential variation hypothesis. Summability allows rates such as `N^{-2}` or many other subexponential tails. The correct bound is controlled by a tail or pointwise variation quantity determined by the actual modulus of the `g`-function.

The next step—failed matching probability bounded by `C d_\beta(x,y)^\alpha`—also requires a quantitative relation between the variation tail and the exponentially weighted history metric. It does not follow from mere summability. Since the small-distance contraction is the first input to the patched weak-Harris metric, the proof of `thm:r17-a4-harris` already fails here.

### 2.2. [FATAL] The drift and small-set minorization are not derived from the stated data

The proof of `lem:r17-a4-drift` says that the current edge is shifted out and the new exponential moment is uniformly bounded, hence `PW\le\lambda W+C` with `\lambda<1`. If `W(x)` depends only on the current edge and the next-edge exponential moment is uniformly bounded, one may obtain a bound `PW\le C`; but the claimed strict drift coefficient and its compatibility with the full history metric still require a precise kernel estimate. If the mark includes history-dependent singularity/path cost, even the uniform moment is not shown.

The minorization argument is more seriously incomplete. The fact that finitely many edge cylinders carry most of the probability does not imply that **every** history in `{W\le R}` admits a common `n_R`-step subprobability measure. One needs:

1. a finite family covering the entire Lyapunov sublevel, not merely most mass under one measure;
2. connector words of a common length or a synchronized construction;
3. a uniform positive lower Gibbs bound over all starting histories;
4. a common terminal set carrying an identical measure component, not only a common symbolic cylinder;
5. treatment of continuous coordinates and suspension residuals.

None of these is supplied. Thus the claimed small set is postulated rather than proved.

### 2.3. [FATAL] Weak-Harris contraction is not automatically an operator spectral gap on the stated Banach space

Theorem `thm:r17-a4-harris` concludes from a Wasserstein contraction in `\widetilde d` that `P` has a spectral gap on

\[
\mathcal B=\{f:\|f\|_W+\operatorname{Lip}_{\widetilde d}f<\infty\}.
\]

A weak-Harris theorem can yield uniqueness and contraction of probability measures in a weighted Wasserstein distance. To obtain a bounded-operator spectral decomposition on a weighted Lipschitz Banach space, one must establish the exact dual norm, invariance of the space, a Lasota–Yorke/Doeblin–Fortet inequality, completeness, and a bound for the centered operator. None is written. The metric itself contains `W` and can be unbounded or degenerate relative to the proposed function norm unless carefully normalized.

The proof's sentence “iteration gives the spectral gap” skips the central functional-analytic theorem on which the Poisson equation, analytic perturbation, and rough-path limit all depend.

### 2.4. [FATAL] The class `\mathcal A` is not the fixed multiplier Banach algebra claimed in `thm:r17-a4-fk`

The norm permits

\[
|V(x)|\lesssim 1+\log W(x).
\]

If `V_1,V_2` both have this growth, their product can grow like `(\log W)^2`, which is not controlled by the same norm. Hence `\mathcal A` is not an algebra under pointwise multiplication as stated.

More importantly, the displayed estimate

\[
e^{|V|}W^\theta\le C W^{\theta'}
\]

shows at best that multiplication by `e^V` maps a `W^\theta`-weighted space into a **heavier** `W^{\theta'}` space. It does not show that `P_V=P(e^V\cdot)` is a bounded analytic family on one fixed Banach space `\mathcal B_\theta`. A smoothing or drift estimate returning from `\theta'` to `\theta` would have to be proved uniformly. Without it, the operator power series is not an operator-norm power series on the claimed fixed space, and analytic eigenvalue perturbation is unavailable.

The existence of a strictly positive eigenfunction with an inverse that acts boundedly on the required weighted space is also not shown. Therefore the Doob transform and the asserted nonlinear tower are not yet well typed.

### 2.5. [MAJOR] The enhanced invariance principle is not proved by the cited ingredients

Theorem `thm:r17-a4-rough` claims a Brownian rough-path limit for suspension observables and stability under conditioning on a compact past cylinder. Even granting a spectral gap, the paper must verify:

- the precise `L^{2+\epsilon}` bounds for the Poisson solution and martingale differences;
- convergence of predictable quadratic variations;
- tightness of second-level iterated integrals and the area anomaly;
- control of the random suspension time change and terminal residual;
- uniform estimates under the conditioned initial densities.

A bounded density change at time zero does not automatically preserve every quenched/conditional bracket estimate, and “the iterated-integral version” is not identified. This section is an outline, not a proof.

### 2.6. [FATAL] A2 matrix-coefficient bounds do not yield the operator-valued renewal theorem `thm:r17-a4-renewal`

A2 concerns matrix coefficients of a particular induced Sinai transfer operator with finitely many central insertions. A4 introduces a history kernel, a source-dependent Feynman–Kac family, a suspension generator `L_V`, residual operators, and a common graph domain. The manuscript gives no theorem transporting A2's estimates to this different operator realization, uniformly over an infinite-dimensional source ball `V` and after source derivatives.

The renewal identity for `\Re z` large may be formalized by path decomposition. The claimed meromorphic continuation and integrable vertical bounds require much more:

1. a Fredholm or quasi-compact operator family on a fixed Banach pair;
2. compactness of the relevant perturbation or a finite-rank spectral decomposition;
3. a precise relationship between `R_V(z)` and the A2 twisted operator;
4. uniform high-frequency estimates for all residual operators and source derivatives;
5. control of essential spectrum in the strip.

“Analytic Fredholm reduction on the isolated finite-dimensional leading spectral subspace” is not sufficient: analytic Fredholm theory applies to an operator family of the form identity minus compact/Fredholm perturbation, not merely to a selected eigenprojection while the complement is uncontrolled.

### 2.7. [FATAL] The compressed-resolvent proof contains an algebraic typing error

In `lem:r17-a4-compression`, for `x\in\mathcal R_V` and `y=(z-L_V)^{-1}x`, one has

\[
C_V(z)x=P_Vy.
\]

The proof writes

\[
\Re\langle C_V(z)x,x\rangle
=\Re\langle y,(z-L_V)y\rangle.
\]

This equality does hold if the inner product is handled as
`\langle P_Vy,x\rangle=\langle y,x\rangle` and `x=(z-L_V)y`, so the basic strict accretivity conclusion is plausible for `\Re z>0`. But the rest of the lemma—uniform minimum singular value over source sets and contour segments, and the `O(|z|^{-2})` expansion—requires uniform compactness of the parameter family, a fixed transported resolved space, and uniform `D(L_V^2)` bounds. Those hypotheses are declared but not proved from the preceding construction.

This is one of the few potentially salvageable pieces, but it cannot bear the later continuation claims by itself.

### 2.8. [FATAL] The memory theorem does not follow from meromorphic continuation, and the “mode promotion” changes the problem

Theorem `thm:r17-a4-memory` defines

\[
\widehat K_V(z)=zP_V-P_VL_VP_V-C_V(z)^{-1}.
\]

The right-half-plane algebraic identity can be valid under domain assumptions. The paper then claims that every left-half-plane transmission zero can be promoted to the resolved space, that finitely many steps remove all zeros in a strip, and that contour shifting yields exponential integrability.

No proof is given that:

- there are only finitely many compression zeros in the chosen strip;
- their multiplicities and Riesz ranges vary controllably with `V`;
- adjoining those ranges preserves finite dimensionality uniformly, the common `D(L_V^2)` domain, and the intended physical resolved variables;
- cancellation of poles of `C^{-1}` removes all growth from the remaining transform;
- the transform has adequate vertical decay for inverse Laplace integration.

Promoting a zero mode changes `P_V`, hence changes `C_V`, and may create new zeros. It is not a finite algorithm by assertion. Meromorphicity alone never implies exponential integrability of the inverse transform; one also needs uniform vertical bounds and contour estimates.

## 3. Dependency consequences

A4 depends on the unproved A2 Fourier theorem and on the exact history/path platform claimed in A3. It also fails independently through the variation, Harris, multiplier, renewal, and transmission-zero gaps above. Its history spectral gap, Feynman–Kac pressure, rough path, and memory kernel cannot be used as inputs to C1, C2, or D1.

## 4. Minimum requirements for reconsideration

A future submission would need:

1. an explicit variation rate and a correct quantitative coupling theorem;
2. a genuine Lyapunov/minorization proof on the exact history state;
3. a theorem linking weighted Wasserstein contraction to the precise function-space spectral gap used later;
4. a fixed operator scale on which `V\mapsto P_V` is analytic;
5. a complete rough-path martingale argument;
6. an operator-valued renewal theorem with verified Fredholm and high-frequency hypotheses;
7. a fixed-resolved-space memory theorem with domain control, transmission-zero analysis, and inverse-Laplace bounds.

## 5. Recommendation

**Reject.** The revised paper has improved conceptual typing, but its central analytic claims remain a sequence of unproved upgrades: summable to exponential variation, Wasserstein contraction to spectral gap, cross-weight multiplication to a fixed analytic algebra, scalar Fourier estimates to an operator resolvent, and meromorphic continuation to exponentially integrable memory. These are the substance of the paper, not routine details.