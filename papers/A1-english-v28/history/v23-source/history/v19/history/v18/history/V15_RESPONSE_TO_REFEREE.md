# Response to the referee — A1, English revision 15

**Manuscript:** *Attainable information geometry in positive experiments*  
**Controlling report:** A1 v14, `3d58bb33ae122ebb2430874e2a57a5863e6a876a`  
**Reviewed submission:** `ffb9214b0fc7e218d6183c1f81bccb3e47587421`  
**Date:** 6 September 2026

We thank the referee for distinguishing mathematical validity from the assessment of significance, and for explicitly recording the closure of earlier issues. The report does not identify a blocking counterexample or an essential missing step in the chain it examined. We therefore do not present this revision as repairing a newly false theorem, nor reopen the previously closed precision, uniformity, horizon or common-name objections. The response strengthens the mathematical presentation and its demonstrated reach.

The revision retains the full v14 classification, all local width and exact-prefix results, the common-name law, and the complete implementation appendices. All 77 complete proof blocks and all 80 complete named statements from the expanded v14 manuscript occur byte-identically in the new expansion. The older source directories and reviews are unchanged. These preservation statements concern source identity, not proof verification.

## E14.1 — Identify the bounded-dual mechanism at its proper level

We agree with the reduction in audit A1. Proposition 8.1 (`prop:general-bounded-dual`) states it before the confluent application, for an arbitrary bounded finite test vector with covariance bounded below and an arbitrary linear observation map. Its proof is complete, includes the prior normalization denominator, and works at a finite perturbation radius rather than only infinitesimally. The constants are independent of the singular values and rank of the observation map. The result and its provenance are explicitly attributed to the controlling audit.

This makes the logical dependency unambiguous: the full confluent covariance bound and `A=L_a D_a` yield all local ambiguity-width orders. We have not relabeled the covariance right inverse as a second positive-history mechanism. Conversely, none of the established conclusions is removed: simultaneous body inclusions, zero widths at exact collisions, the exact-prefix radius, and the positive-probability physical realization all remain with their full original proofs.

The title and abstract now describe positive-history attainment and two resolved experiments. The ambiguity section is a further consequence, not the principal substitute for attainment. This is a clarification of the hierarchy of complete results, not a weakening of the width theorem.

## E14.2 — A standalone principle and a genuinely different resolved experiment

### The standalone positive-history statement

Section 3 separates an algebraic criterion from an ordered-space criterion. Proposition 3.1 (`prop:product-criterion`) gives the normalized product derivative and proves that normalization removes exactly one rank whenever the product lies in the true product tangent. It then gives a quantitative change-of-variables statement. The square inverse map retains complementary kernel coordinates, and their integration yields a full-dimensional minorization under the actual command-and-report subprobability law. The report evidence is retained; a zero-measure section is not mistaken for a distribution of histories.

Theorem 3.2 (`thm:positive-attainment`) applies for every full-support prior when the true product tangent contains one strict Chebyshev system and the selected future tests with the constant form another. Determinant integration supplies the pairing rank. The theorem includes compact-family uniformity, finite unions of test orders, and dominated prior envelopes. Its hypotheses explicitly concern the actual tangent and actual finite commands. It does not assert that a future spectrum or the dimension of a factor space alone entails attainability.

The monomial binomial tangent and complete Hermite flag verify these hypotheses. The introduction now states what the closest spectral and entropy results contribute and what they do not: evaluation-matrix singular values, coefficient-independent regularity, and an upper cover do not provide a positive-history lower measure, a matching truncation, or a causal code. The global cover and the raw-moment recurrence remain separate obligations with their full original proofs.

### A positive circular detector whose acquisition also degenerates

Section 7 is a new application, not an additional interpretation of the old linear ambiguity map. The hidden parameter lies on a circle, with Haar prior, and the four detector cells are `(1 ± tau cos theta)/4` and `(1 ± tau sin theta)/4`. The controller has only four bounded lookup probabilities; it cannot inspect the hidden angle. Every trial and failure is counted. Calibration is known exactly. All cells remain uniformly positive as contrast tends to zero, while the one-step likelihood span loses its nonconstant directions at zero.

An actual report has normalized factor `1+tau(z w+conj(z)/w)`. For a length-n product its jth Fourier coefficient factors exactly as `tau^j` times a polynomial in `tau^2`. The normalized coefficient map extends to zero contrast, where it is the elementary-symmetric-polynomial map. At one fixed interior tuple of distinct complex coordinates this map has full real rank. Lemma 7.2 proves a uniform neighborhood of zero contrast and an evidence-weighted minorization of every initial harmonic flag. This is a new acquisition calculation; it is not supplied by the bounded-dual argument.

A fixed finite menu of `2m+1` attainable repeated-failure queries contributes a second factor `tau^j`. Lemma 7.3 gives its exact discrete Parseval metric. The physical jth harmonic therefore has scale `tau^(2j)`, repeated twice over the reals. Rectangle covering and the attained subprobability give the matching checkpoint law

`H(n,m;M,tau) = max_{1 <= j <= min(n,m)} tau^(2(j+1)) M^(-1/j)`.

Theorem 7.1 proves the corresponding single-transducer maximum-checkpoint law, uniformly for all integer M and sufficiently small contrast including zero. In weighted Fourier coordinates, the exact update is

`Y'_j = (Y_j + tau^2 z Y_(j-1) + conj(z) Y_(j+1)) / (1+z conj(Y_1)+conj(z) Y_1)`.

Its denominator is bounded below on segments of posterior states; no reciprocal contrast appears. The complete proof handles reachable codebook centers, the integer label budget, missing high harmonics, the shrinking future state, and independent coding randomization in the converse. The same independent exploration law supplies all checkpoint lower bounds. The exact continuous state dimension is `2 min(n,m)` at positive contrast and zero at zero contrast.

Corollary 7.4 identifies the successive harmonic phases and their transitions at `M=tau^(-2j(j+1))`. Already at one past and one future trial, using only the future attenuation would give the wrong contrast power. Thus this example tests the interaction of acquisition and observation inside one model, rather than comparing local exact advice with a different common noisy name.

We do not infer journal-level significance from the existence of this application or its test count. Its role is to supply a concrete theorem beyond the real-monomial collision setting, with an independently derived acquisition map, physically attainable queries and a collision-free causal update. Those proofs and their significance remain matters for the next referee to assess.

## Limited editorial requests

The introduction now contains a direct theorem-level comparison with the nearest interpolation, rational-image and real metric-entropy inputs. The real variation inequality is distinguished from the nonarchimedean results of Comte–Halupczok. A newly checked August 2026 Fourier-matrix preprint concerns nonuniform nodes, whereas the circular query grid here is fixed and equally spaced; it is not invoked to prove our acquisition theorem.

“All width orders” is used in the abstract and explanatory text. We do not claim an exact ellipsoid or canonical physical axes. The known-calibration, fixed-history, exact-prefix convention remains adjacent to the local risk formula. The exact-prefix experiment is not identified with the imperfect-common-name experiment. The scalar common-name law retains its dominated-family, interior and name-slack hypotheses.

The principal narrative consists of the attainment criterion, the two geometric classifications, the local ambiguity consequence and the common-name law. The complete compiler, numerical interfaces, precision estimates, workspace bounds and request conformance remain in their technical appendices. Revision and execution records remain outside the manuscript narrative.

## Verification and the next review boundary

The six author suites are executed by `validate.py`: the five unchanged suites have 62,613 assertions; the new circular suite has 5,868. The new suite uses exact rational and Gaussian-rational Laurent arithmetic without importing author helpers. It checks physical query identities, discrete orthogonality, product normalization, weighted updates, finite full-rank samples, exterior-volume powers and phase crossings. Deliberately omitting the update's `tau^2`, the evidence denominator, or the acquisition attenuation produces detectable failures. These are successful negative controls, not counterexamples to the manuscript.

Finite rank samples do not determine the uniform contrast interval. Its existence is proved by the explicit central Jacobian and continuity in `tau^2`. Likewise, a source-preservation count is not a proof audit, and a successful build does not establish minimax optimality. `validation/EXECUTION_REPORT.json` records what was actually run. The optional prior-review replay runs the original v14 diagnostic on its unchanged source, not on the new application and not as an independent endorsement of v15.

The next review should examine the quantitative minorization in Proposition 3.1, the compact-prior uniformity in Theorem 3.2, and the complete circular chain in Section 7. The original monomial full-support theorem and all previously closed correctness issues retain their stated scope. No acceptance recommendation is asserted on the referee's behalf.
