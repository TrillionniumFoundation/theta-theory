# External top-four referee report on A2 v13 — canonical rereview

**Manuscript:** Qian Qi, *Nonlinear boundary laws and two-contact rigidity in dispersing billiards*  
**Date:** 28 September 2026  
**Requested benchmark:** Annals / Acta / Inventiones / JAMS  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision or proof certificate.

## 1. Frozen source and verdict

I reviewed

`revision/a2-v13-major-revision-canonical-2026-09-28`

at commit

`0e54099f079232df233316ae6fe7986fc51b7ea1`

(tree `41f68e02205e10d48e917559f0f5092c10799948`), manuscript directory

`papers/A2-v13-two-flight-relative-invariants`.

The branch name is dated 28 September, but its head is the A2 v13 author commit of 10 September. I found no later manuscript commit. The canonical branch is therefore a new reference name for the already reviewed v13 source, not a new mathematical revision answering the v13 reports.

**Recommendation at the requested four-journal benchmark: reject in the present form.**

This is not a finding that the central theorems are false. In the principal chain examined, I found no fatal counterexample to the two-flight inverse, the correctly scoped finite physical experiment, the relative determinant mechanism, the Volterra uniqueness step, or the Abel/regularized acquisition architecture. The recommendation is negative because the source still contains a false headline quantifier, still omits the closest forward normal-form comparison, and does not persuade me that the remaining contribution reaches the exceptional conceptual level requested.

## 2. What v13 genuinely achieves

V13 materially improves v12. It supplies:

- an all-order two-flight inverse for two labelled individually even contacts, including equal curvatures;
- fixed-order analytic changes between finite two-flight and limiting jet coordinates;
- a genuine physical realization of independent contact jets at fixed leading data;
- a direct two-flight finite-window experiment with a locally bi-Lipschitz mean map;
- a clearer separation of finite-jet recovery, long-bridge factorization, and smooth function-valued recovery;
- theorem-level comparisons with selected global inverse-spectral results.

These are substantive results. They should not be dismissed as absent merely because I withhold a top-four recommendation.

## 3. Correctness audit

### 3.1 Two-flight block

For itinerary `b,o,b`, the quadratic stationary action gives

`H_b = g^{-1} [[c_b-(2c_o)^{-1}, -(2c_o)^{-1}], [-(2c_o)^{-1}, c_b-(2c_o)^{-1}]]`.

With `z=c_0 c_1-1` and `L_b=g/(2 c_b z)`, inversion gives

`nu(u)=nu(v)=L_b(1+2z)` and `nu(w_0)=L_o`.

The other-contact contribution must include both action variation and variation of the normalized mixed endpoint derivative. The latter supplies the essential `2 m z` term. The printed last-jet block is therefore

`- [[(1+2z)^m, 1+2mz], [1+2mz, (1+2z)^m]] diag(k_m L_0^m, k_m L_1^m)`,

where `k_m=4/[2^m(m+1)(m!)^2]`. Its smaller symmetric-factor eigenvalue is positive because

`(1+2z)^m-(1+2mz)=sum_{r=2}^m binom(m,r)(2z)^r > 0`.

Thus no denominator involving `kappa_0-kappa_1` is needed; equal curvature is not a degeneracy. The source also addresses finite-jet dependence, affine last-jet dependence, nonlinear-domain degree bookkeeping, and the recursive inverse. I found no new objection to this theorem in its stated even-contact, supplied-leading-geometry setting.

### 3.2 Physical family and experiment

The physical realization theorem constructs a particular locally full-rank analytic family near a disk geometry. It fixes the selected gap, area, curvatures, and leading channel hierarchy. This is a real physical image, not a formal perturbation.

The direct observation theorem then fixes one such family and `M`, assumes the family and leading data are supplied, and uses positive nodes to obtain two Vandermonde blocks plus an `O(h)` preconditioned remainder. Local invertibility and the `N^{-1}` risk follow. The statistical rate is a regular finite-dimensional consequence once the physical mean map is bi-Lipschitz; it is not a second rigidity theorem.

### 3.3 General smooth chain

The relative proof normalizes the exact cofactor before comparison, uses endpoint localization and trace-norm control to avoid an interior-dimension loss, and transfers the result through a common Morse chart to the physical residual-time integral. I found no basis for reviving the objection that it divides an uncontrolled absolute error by an exponentially small flux.

The profile argument obtains complete smooth uniqueness through a Volterra equation rather than equality of formal jets. The Abel and self-calibration stages keep structured bridge error, approximation bias, and scalar sampling noise distinct. Their final exponent is sufficient under supplied certificates, not minimax; the source now says so.

This remains a scoped audit, not certification of every retained appendix result.

## 4. Major statement error: the abstract's family quantifier is false

The abstract says that “every fixed finite-dimensional family can be observed through positive windows at two flights.” The theorem proves this only for the specially constructed locally full-rank families of the physical realization theorem, or under an equivalent rank hypothesis.

A counterfamily is immediate. In a sufficiently large periodic cell, keep the two obstacles forming the selected isolated shortest channel fixed. Add a third small analytic strictly convex obstacle far from the selected contact neighborhoods and chords, with strict clearance. Translate only that third obstacle through a small interval, generically producing non-isometric tables.

The selected gap, participating boundary germs, two-flight action, mixed derivative, phase normalization, and near-onset residual-time collar remain unchanged. Hence all selected two-flight probabilities—and indeed the selected near-onset laws at every flight number—are constant along the family. They cannot be bi-Lipschitz coordinates for the translation parameter.

The abstract must say “each locally full-rank physical finite-jet family constructed here,” or state an explicit full-rank hypothesis. This is a material theorem-scope error, although easy to repair.

## 5. Missing closest forward comparison

The introduction compares A2 with global inverse-spectral theorems. That is useful but does not address the closest mechanism for the forward product law.

In analytic hyperbolic coordinates near a period-two orbit, consider the normal form

`N(s,p)=(Delta(sp)s, Delta(sp)^{-1}p)`, with `Delta(0)=lambda in (0,1)`.

For incoming stable coordinate `s` and outgoing unstable coordinate `t` after `n` returns, the invariant satisfies

`I = s t Delta(I)^n`.

The initial unstable coordinate is `p_0=t Delta(I)^n`, so exact differentiation gives

`d p_0/d t = Delta(I)^n / [1-n I Delta'(I)/Delta(I)]`.

On a fixed small box, `I=O(mu^n)` and the denominator stays away from zero. After normalization by `lambda^n`, the derivative converges exponentially in every fixed derivative order. Passing through physical endpoint charts contributes left and right projection Jacobians, yielding a product limit for the normalized physical mixed derivative; the action separates similarly after integrating limiting endpoint gradients.

This does **not** subsume A2: it does not provide the arbitrary smooth-family theorem, half-line determinant representation, channel localization, parity compatibility, profile inverse, independent-contact jet separation, or charged acquisition. It nevertheless shows that the qualitative analytic product mechanism is already accessible from classical local hyperbolic structure plus a physical projection calculation.

The manuscript should state this restricted benchmark and identify precisely what Theorem 1.1 adds. Distinguishing marked lengths, Laplace spectra, and selected probabilities does not answer this forward comparison.

## 6. Significance at the requested level

The strongest positive case is the integration of a smooth relative law, a complete symmetrized energy-profile invariant, an explicit even-contact inverse, and an operational observation procedure.

My reservation is that:

- the general target is a selected-channel symmetrized profile, not unrestricted contact or whole-table geometry;
- the forward proof is a technically careful synthesis of localized contraction, tridiagonal/cofactor algebra, trace ideals, and Morse transport, but no broader rigidity principle is yet demonstrated;
- the explicit geometric inverse remains in an individually even analytic class with supplied labelled leading geometry;
- the finite-window risk is parametric after local invertibility;
- the full-profile preparation rate is sufficient under supplied class and convergence certificates, without an optimal physical experiment or matching infinite-dimensional lower bound.

These are not logical defects. They delimit the reach of the completed package. Combined with the missing normal-form comparison, they leave me unconvinced at the requested benchmark.

## 7. Required corrections

1. Correct the abstract quantifier and expose the supplied family, labels, leading data, and fixed-order hypothesis.
2. Add the direct analytic normal-form comparison, including the physical endpoint projection step.
3. Clarify the finite-law normalization: the section initially supplies `g,kappa_0,kappa_1`, while the normalized law also uses `A`; distinguish normalized-germ data from finite noisy calibration.
4. State explicitly that the 28 September branch is a canonical alias of the 10 September source commit.
5. Preserve the distinctions between fixed and growing order, analytic and noisy continuation, constructed and arbitrary families, finite parametric and full-profile risk, and selected-channel and whole-table conclusions.

I am not requesting unrestricted asymmetric rigidity, global isometry, growing-order stability, minimax optimality, removal of every certificate, or deletion of valid historical proofs.

## 8. Independent diagnostics and limits

The accompanying `verify_review.py` imports no author verification code. On

`c_0,c_1 in {11/10,3/2,2,4}`, `g in {1/2,1,3/2}`, `m=2,...,15`,

and both orientations, it passes 8,064 exact-rational grid checks, plus the printed quartic example. It checks the Schur determinant, variances, action-plus-twist rows, binomial separation, and inverse identity.

These checks support only the finite algebra. I did not independently obtain a full TeX build or reproduce the author's complete diagnostic suite in this execution environment. Author build and retention claims are not converted into independent findings.

## 9. Final verdict

**Mathematical:** no fatal counterexample found in the principal chain examined; the new two-flight block appears sound in its actual scope.

**Statement:** the abstract contains a false universal quantifier.

**Top-four:** the canonical branch contains no new mathematical response to the v13 objections, and the central novelty comparison remains unresolved.

**Recommendation: reject in the present form at the requested benchmark.**
