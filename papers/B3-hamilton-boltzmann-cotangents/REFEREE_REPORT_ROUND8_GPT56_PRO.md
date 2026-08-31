# Round-Eight Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B3 — *Hamilton–Boltzmann Cotangents and Prepared Fluctuation Fields*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round8-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `ad2b5106678b29b7d9ffb3824f61ddbd141ac4b8`  
**Reviewed tree:** `00d7ef9edcddda26fc88962e206677f9b399bebe`  
**Active controlling module:** `ROUND8_POSITIVE_CLOSURE.tex`, blob `1fd8ae0813a56dfbb40554e0aa765575d865cbbb`

## Executive assessment

Round eight correctly admits that the raw second variation of the perspective entropy along `A=A_f` is not positive. It also tries to construct covariance from finite-volume cumulants before identifying an inverse action. This is a better logical order than the previous paper.

The central repair is still invalid. Introducing an auxiliary variable `a` and its KKT multiplier does not alter the reduced Hessian of the constrained functional; after eliminating the constraint, the same indefinite term `(1-q)D^2A_f` remains. One cannot define a positive inverse covariance and then declare that the KKT Schur complement closes to it. Positivity of finite covariances does not imply a uniformly coercive inverse on an infinite-dimensional tangent space, nor does it identify the complete null space. The observability, Mosco convergence, and tree-decaying cumulant density used to bridge those gaps are asserted rather than proved and depend on the unresolved B2 theorem.

## Genuine repairs recognized

The manuscript should retain:

- the exact chain-rule term involving `D^2 A_f`;
- the distinction between local analytic response and global convex duality;
- exact finite-volume centering of fluctuation fields;
- the attempt to obtain process tightness from deterministic-interval cumulants rather than a fictitious contact compensator;
- the recognition that an infinite-dimensional Legendre Hessian cannot simply be inverted formally.

## Major mathematical objections

### 1. The KKT multiplier does not cancel the indefinite reduced curvature

For the constraint

\[
a-A_f=0
\]

and the Lagrangian

\[
\Phi(\Gamma,a)+\lambda(a-A_f),
\]

stationarity in `a` at `Gamma=q a` gives

\[
\lambda=q-1.
\]

Restricting the bordered Hessian to the linearized constraint `dot a = DA_f dot f` produces

\[
\frac{|\dot\Gamma-qDA_f[\dot f]|^2}{qA_f}
-(q-1)D^2A_f[\dot f,\dot f],
\]

which is exactly

\[
\frac{|\dot\Gamma-qDA_f[\dot f]|^2}{qA_f}
+(1-q)D^2A_f[\dot f,\dot f].
\]

This is the same reduced Hessian the manuscript already found. Introducing the multiplier reproduces the curvature term; it does not turn it positive.

A scalar model makes the issue explicit. If `A_f=f^2`, `q>1`, and

\[
\dot\Gamma=qDA_f[\dot f],
\]

then the residual square vanishes and the reduced second variation is

\[
2(1-q)(\dot f)^2<0.
\]

Any positivity must come from additional balance, initial-cost, or dynamical terms proved to dominate this direction. No such domination is established.

### 2. The Schur-completion theorem is circular

The paper defines

\[
\mathfrak q^{\rm sc}=\Sigma^{-1}
\]

on the range of the covariance, then states that the KKT Schur complement closes to this positive form. This makes positivity true by definition rather than by analysis. The missing theorem is precisely the equality between the variational second derivative and the inverse cumulant covariance.

Finite-dimensional convex duality can give this equality at a strictly convex smooth minimizer. In the present infinite-dimensional path problem it requires:

- a proved full local LDP;
- uniqueness and smooth dependence of the minimizing path;
- a closed linearized constraint range;
- second epi-differentiability/Mosco convergence; and
- control of unbounded inverse operators.

These are the paper's desired conclusions, not established inputs.

### 3. Positive covariance does not imply a bounded coercive inverse

Every finite-volume covariance is positive semidefinite. Its limit can have a nonclosed range and eigenvalues tending to zero. In an infinite-dimensional nuclear/distribution setting this is typical.

The estimate

\[
c\|u\|_{\mathsf T}^2
\le \Sigma^{-1}(u,u)
\le C\|u\|_{\mathsf T}^2
\]

requires uniform ellipticity on infinitely many modes. No finite source curvature theorem can supply this automatically. If the norm of `T` is defined from `Sigma^{-1}`, the estimate is tautological; if it is inherited from the kinetic graph spaces, it is unproved and likely false for high spatial/velocity frequencies.

### 4. The exact null-space theorem is not obtained from covariance convergence

The proof establishes only one inclusion: invariants and telescoping gauges have zero scaled variance. The converse relies entirely on the later observability lemma. There may be additional zero modes from prepared constraints, inaccessible collision directions, boundary traces, phase symmetries, or a nonclosed covariance range.

“Every two-sided pressure derivative vanishes” does not by itself identify a source with a gauge in the declared infinite-dimensional topology.

### 5. The backward hypocoercive estimate is not proved

The estimate combines transport, collisions, spatial derivatives, reflected boundary traces, and a time-dependent regular biased phase. A velocity collision spectral gap controls only microscopic velocity modes. Recovering hydrodynamic spatial modes is a full hypocoercivity theorem with boundary/domain conditions and commutator estimates.

The one-paragraph proof gives no operator domains, no boundary conditions, no macro–micro decomposition, and no estimate uniform over the source chart. It also depends on B2's graph trace theorem, which is not valid in its current form.

### 6. Closed range does not identify the source gauge without a complete adjoint calculation

Even if `B` had closed range, the annihilator of its kernel is the closure of the adjoint range in the chosen Hilbert pairing. Showing that this range is exactly the stated dynamic gauge requires an explicit characterization of the adjoint domain and all endpoint/contact boundary terms. “Expanding the pairing” is not enough.

### 7. Mosco convergence is merely announced

The proof of Theorem `r8-b3-schur` says that finite quadratic forms Mosco-converge. No liminf theorem, recovery sequence, common Hilbert embedding, or compactness statement is supplied. This is the main analytical bridge between finite-volume covariance and the kinetic tangent form; without it, the identification is unsupported.

### 8. B2 source sewing does not yield exponential time-tree decay

The cumulant-density lemma asserts

\[
|\kappa_r(t_1,\ldots,t_r)|
\le C^r r! e^{-c\mathsf T(t_1,\ldots,t_r)}.
\]

B2 attempts a fixed-horizon cluster/consistency theorem. It does not prove an exponential temporal mixing gap for the source-biased, generally time-inhomogeneous kinetic phase. A connected genealogy can span a long free-flight interval without the “largest gap” argument asserted here, and transport/hydrodynamic modes require separate hypocoercive control.

The claimed `graph semigroup gap` is not a theorem in B2.

### 9. The process tightness conclusion needs finite-volume moment bounds, not only limiting covariances

A covariance bound for adjacent intervals does not by itself give fourth-moment or fractional-Sobolev tightness. The higher finite-volume cumulants must be bounded uniformly at the correct scale, including diagonal contact atoms. The manuscript states a limiting density estimate and immediately applies Kolmogorov/Mitoma without constructing those uniform finite-volume estimates.

## Dependency assessment

B3 cannot close the hard-sphere cotangent or Gaussian interface while B2-GC and B1 remain unproved. B4, C1, C2, and D1 may not use the asserted covariance inverse, exact gauge, or process Gaussian limit as established inputs.

## Required reconstruction

A credible reconstruction should first prove finite-dimensional covariance and fluctuation limits for a fixed separating family. The reduced quadratic action must then be computed on the exact linearized balance and shown positive by an explicit stability theorem, not by introducing an auxiliary variable. Only after proving closed range and second-order epi-convergence should one pass to an infinite-dimensional Cameron–Martin space. Process tightness needs independent, quantified time-local cumulant estimates.

## Recommendation

**Reject.** The paper recognizes the negative raw curvature but then defines a positive inverse covariance and declares the two objects equal. The KKT constraint does not remove the negative term, and every theorem intended to bridge that gap remains unproved.