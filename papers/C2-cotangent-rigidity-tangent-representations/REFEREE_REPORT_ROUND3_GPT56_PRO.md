# Round-Three Referee Report — GPT-5.6 Pro

**Manuscript:** C2 — *Path-Space Cotangent Rigidity, Universal Contractions, and Tangent Representations*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round3-full-positive-closure-11paper-2026-08-30@6a31720e5b0b6ab156b575f947596f9b66f56efe`  
**Controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `06bff8bd2ba864607f19c1127031d5cb5b1f24b6`

## Executive assessment

The paper has corrected its most obvious category error. It no longer claims that physically different systems share one unlabelled parent probability law. Instead it introduces a disjoint, platform-labelled coproduct and requires a separately proved scaling theorem for cross-platform maps. It also attempts to use a weighted strict topology with a countably additive Radon dual and conditions second derivatives on actual spectral/cluster analyticity.

These are welcome truth-boundary repairs. The active manuscript still does not prove its principal representation theorems. Its contraction ledger depends on A3’s invalid path LDP; its pressure derivatives depend on the unproved A2/B2 packets; its likelihood-ratio convergence is inferred from weak rough-path convergence without convergence of conditional expectations or filtrations; and its memory-pressure formula is ill-typed and uses the wrong generator. The repository’s internal audit produced a corrected strict-memory file, but it was never incorporated into the controlling paper.

After removing those conditional consequences, the manuscript is a synthesis of generic contraction, convex-duality, entropic-utility, Girsanov, and BSDE facts. It has no independent top-four theorem.

## Improvements relative to the preceding circulation

1. Platform labels are explicit, and cross-platform substitutions are prohibited without a scaling theorem.
2. Mechanical observables are required to be continuous or exponentially approximable on each platform.
3. The manuscript attempts to choose a locally convex topology whose dual consists of countably additive measures.
4. It no longer infers a Hessian from uniqueness alone; it invokes model-specific analytic packets.
5. Entropic axioms are separated from the extra mechanical calibration condition.
6. Diffusion/Girsanov/BSDE statements are explicitly described as consequences of a proved tangent, not substitutes for the microscopic theory.

These changes improve the logical architecture but do not provide the missing proofs.

## Major mathematical objections

### 1. The contraction ledger is downstream of a false A3 exponential approximation

The Sinai continuity lemma cites A3’s claims that long blocks, singularity neighborhoods, and clock residuals have arbitrarily large exponential cost. A3’s long-block statement is false under an exponential return tail because one excursion of order the horizon has finite exponential cost. Hence the proposed exponentially good truncations for collision activity, path windows, and physical clocks are not established on the full rate domain.

The platform-labelled formulation prevents model substitution, but it cannot repair the missing parent LDP or the discontinuous path maps.

### 2. The strict-dual theorem omits the coercivity needed for the variational pressure

Identifying the dual of an appropriate weighted bounded-strict topology with Radon measures is a standard type of result, but the active definition and proof are only a sketch. More importantly, a good rate `I` in a weighted weak topology does not by itself imply that

\[
Q(F)=\sup_\nu\{\nu(F)-I(\nu)\}
\]

is finite, attained, and continuous for every `beta_W`-bounded source. One needs an explicit coercive inequality controlling `nu(W)` by `I(nu)` or a uniform exponential-moment domain. “Goodness and weight coercivity” is invoked, but no weight-coercivity hypothesis is stated in the theorem.

Without it, the compact maximizing-phase set and the subdifferential identity can fail.

### 3. The coboundary converse inherits A3’s invalid dual argument

The paper states that two potentials have the same integral under every invariant finite-weight phase exactly when their difference belongs to the closed coboundary span. Its proof delegates the converse to A3. A3 attempts to obtain an invariant measure from an arbitrary Hahn–Banach separator on a weighted Hölder algebra by Jordan decomposition, which is not valid for a general Banach-dual functional.

Thus the claimed cotangent quotient has not been shown to be exactly the kernel seen by all invariant phases.

### 4. The pressure-response theorem depends on unproved model packets

The Green–Kubo formula on the Sinai branch assumes A2’s uniform higher-block spectral theorem and high-frequency roof control. Those are not proved in the controlling A2 manuscript. The hard-sphere derivative statement assumes B2 normal convergence on the required source domain and B3 process covariance, neither of which is established.

The paper’s conditional calculus is formally correct; its asserted model realization is not.

### 5. Weak rough-path convergence does not imply convergence of conditional likelihood martingales

The deterministic likelihood process is

\[
M_t^\epsilon
=
\frac{E[e^{\theta\Phi(X_T^\epsilon)}\mid\mathcal F_t^\epsilon]}
{Ee^{\theta\Phi(X_T^\epsilon)}}.
\]

Joint weak convergence of `X^epsilon` and its iterated integrals, even with uniform exponential moments, does not generally imply convergence of the optional projections above. Conditional expectations are not continuous functionals of the joint law when the filtrations vary.

A valid theorem needs stable convergence of filtrations, convergence of the associated martingale problems or transition kernels, and uniform integrability of the conditional densities. None is supplied. The phrase “conditional convergence on cylinder filtrations” is the conclusion that must be proved.

This is especially important because complete microscopic observation makes the future deterministic, whereas the limiting Brownian filtration contains innovation noise. The information structures must be matched by a theorem, not silently identified.

### 6. The active memory-pressure identity is ill-typed

The paper writes

\[
\int_0^\infty e^{-zt}
D\mathcal E_t^\Psi(0)[A](B)\,dt
=
\langle B,P(z-L_\Psi)^{-1}PA\rangle.
\]

After applying the derivative to `A`, the result is an observable; `(B)` has no defined meaning. The required expression is an `L²` pairing

\[
\langle B,D\mathcal E_t^\Psi(0)A\rangle.
\]

The repository’s internal audit identified this exact typing error and created `revision/round3-rereview/C2_STRICT_MEMORY.tex` with a corrected formula. That file is not included in the controlling manuscript.

### 7. The generator in the memory formula is the wrong object

The active text calls `L_Psi` a “tilted Koopman/Feynman–Kac generator.” A Feynman–Kac semigroup is not a stationary Markov/Koopman group and is generally not skew-adjoint in the prepared `L²` space. A4’s compressed-resolvent memory construction is formulated for the generator of the prepared linear dynamics. To connect pressure and memory one must first perform the normalized Doob transform and use its stationary generator.

The orphaned C2 repair file makes this correction. The active theorem does not.

### 8. A4’s normalized nonlinear history semigroup is itself not a semigroup

C2 differentiates and composes A4’s normalized Feynman–Kac log transform. As reviewed in A4, subtracting `log P_t^Psi 1` statewise destroys the tower unless a Doob normalization is performed. Therefore the “pressure tangent” being differentiated in the active C2 proof has no established semigroup structure.

### 9. The entropic-rigidity theorem is underspecified

The classification of strongly time-consistent law-invariant certainty equivalents requires a precise filtered probability setting, continuity/Fatou conditions, relevance, normalization, and the exact notion of conditional law invariance. The paper replaces these with a short utility functional equation. Even if the scalar conclusion is accepted, it is a generic theorem and the extra equality `vartheta=theta` follows only because the same cocycle is imposed as an axiom.

### 10. The manuscript has no independent theorem after dependencies are removed

The platform coproduct is bookkeeping; the fixed-platform contraction theorem is standard; the strict dual is a functional-analytic infrastructure claim; entropic rigidity, Girsanov, and quadratic BSDEs are established general theory. The purported new content is the commutation of these objects for the specific deterministic platforms, precisely the part that remains unproved upstream.

### 11. The controlling manuscript is not standalone

The active source is a preamble plus one closure module. It does not define the platform laws, rates, weights, A4 history semigroup, A2 pressure domain, or B2 source space at submission-level completeness.

## Editorial recommendation

**Reject.** The platform-labelled coproduct is a necessary correction and should remain as a series-level organizational device. C2 should not be a standalone top-journal paper until one fixed-platform representation theorem is proved completely. A viable paper would select either the Sinai strict-dual/pressure-response theorem or a rigorously matched deterministic-to-diffusion likelihood theorem, incorporate the corrected Doob-memory formulation into the controlling source, and supply stable filtration convergence. The present universal synthesis is premature.