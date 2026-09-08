# Response to the referee report on A1 English v17

**Revised manuscript:** *Attainable information geometry in positive experiments*, A1 English v18.  
**Author:** Qian Qi.  
**Date:** 7 September 2026.  
**Controlling report:** `reviews/a1-english-v17-independent-2026-09-07/REFEREE_REPORT.md` at `a2adb648c08b3c9e803e916f533605203963ee35`.  
**Preceding submission:** `papers/A1-english-v17/` at `1f3838d89a5820b853d1e4b78194293b23e70bd2`.

## 1. The issue addressed

The report distinguishes its negative publication recommendation from its mathematical assessment. It identifies no new blocking counterexample or essential unfilled step in the principal chains it examined, closes the finite-command wording issue, and accepts the integer-envelope inverse under its stated hypotheses. We preserve those results and those qualifications. This revision does not describe the preceding paper as disproved, and does not present an editorial reservation as a missing correctness lemma.

E17.1 concerns the cumulative mathematical significance after the inverse formulation. The report observes that inversion within an already represented ordered-product family does not identify the geometry of a previously unclassified experiment. It asks for a substantive mathematical consequence rather than another declaration of importance or a larger diagnostic count. There is no correction-sized checklist promising a different editorial recommendation.

The response is therefore mathematical. We add an experiment-first rank classification for a broad class of positive finite experiments, an exact algebraic description of its exceptional-prior strata, a uniform full-profile classification for the entire positive affine acquisition class, and a necessary and sufficient attainment criterion in the square pairing regime. Their proofs are integrated into the principal manuscript. The previous multi-step classifications, inverse, and all numerical and uncertainty results remain.

## 2. E17.1: classification before assuming a scale envelope

### 2.1 Positive command-polynomial experiments

Section `sec:v18-structure` begins with arbitrary compact metric latent space, arbitrary probability prior, finite horizon, finite report alphabets, and strictly positive likelihoods polynomial in the command variables with continuous latent-variable coefficients. This includes affine retention of arbitrary continuous finite-detector cells; the latent space itself need not be algebraic or ordered.

For each report word the evidence and weighted future-query numerators form a polynomial vector `Y`. The new normalized-rank identity uses `[Y,DY]` and removes exactly the evidence column after normalization. It does not assume that the product itself is an available radial command derivative. The actual checkpoint rank is

`d_n = max_a rank_{R(u)}[Y_a,DY_a] - 1`.

Theorem `thm:v18-rank-classification` proves that this number is the dimension of the entire reachable physical prediction image and the sharp squared-loss memory exponent: `R_{M,n} ~ M^{-2/d_n}` for positive rank. One causal finite-state filter attains the maximum checkpoint exponent. This is a statement about the complete input experiment and its specified prior, not a restatement of a sufficient flag hypothesis.

The proof has three logically separate parts. Rational command maps give bounded-format semialgebraic whole images; a maximal-rank actual report word yields a positive-history minorization after integrating the unused command coordinates and its evidence; closure of the future test spaces under multiplication by the next likelihood gives an exact rational update with denominator bounded away from zero. Quantization of reachable representatives and a finite Lipschitz recurrence account for every preceding lossy update.

The zero-rank endpoint is stated correctly. A general finite-report experiment can have multiple report-constant prediction states, so zero differential rank gives a finite exact state set, not necessarily one label. The new exact diagnostic includes such a positive detector. For a positive rank the constants may depend on the specified experiment; uniformity is asserted on compact constant-rank prior-moment sets, not across all rank changes without additional scale information.

### 2.2 Algebraic exceptional-prior strata

Theorem `thm:v18-moment-strata` identifies `d_n <= k` by the vanishing of the command coefficients of all `(k+2)`-minors of the augmented matrices. These are finitely many explicit polynomials in the actual prior moments.

The full-support moment set is exactly the interior of the finite moment body. All checkpoint ranks attain their maxima simultaneously off a proper algebraic subset, and arbitrarily small bounded-density perturbations of any full-support prior reach this generic set. The proof uses positive definiteness of the covariance of an independent finite function system to fill a moment neighborhood. Exceptional full-support priors are included in the exact classification rather than discarded under a genericity assumption. The moment body itself is not asserted to be semialgebraic.

This is a necessity-and-sufficiency description of the memory exponent for the stated broad class, including a finite algebraic test for every exceptional locus. It is not a claim that dimension determines the entire uniform metric profile of every such experiment, nor a numerical equality test from inexact moments.

### 2.3 The whole positive affine class, uniformly through degeneration

Section `sec:v18-affine` supplies a full-profile result derived directly from a previously unclassified class. For

`L_y(u,x) = (1+y u^t f(x))/2`, `u in [-1,1]^b`, `sup_x ||f(x)||_1 <= a < 1`,

and arbitrary finite physical future tests `h` weighted by the square roots of their query probabilities, the invariant is the unwhitened cross-covariance `C_mu = Cov_mu(h,f)`.

Theorem `thm:v18-affine-classification` proves

`R_M ~ max_l (||wedge^l C_mu||_op / M)^(2/l)`

with constants depending only on `a,b,q`, uniformly over priors, query weights, all singular-value multiplicities, and every rank loss. The proof does not assume a forward profile. It derives the exact posterior prediction as `mu h + C_mu theta`, where `theta = v/(1+(mu f)^t v)` and `v=yu`. The law of `v` includes the two report probabilities. Its transformed density has exponent `b+2`, combining its evidence factor with the `b+1` Jacobian exponent. Uniform inner and outer balls in these projective coordinates provide the same covariance scales for actual acquisition mass and the whole prediction image.

The linear-image quantization lemma includes all integer budgets, arbitrary prediction centers, randomization, zero axes, and centers lying in the reachable image. No inverse covariance or query-weight conditioning constant appears. When the cross-covariance is zero, the exact formula proves that one label suffices for this query task.

The resulting complete-invariant corollary uses the retained envelope inverse only *after* the new forward classification. Its role is therefore distinct from v17: the substantive addition is the derivation of the geometry of a whole input-defined experiment class, not the dualization step.

An explicit full-support family on `[-1,1]` has acquisition feature `alpha x`, query `1/2+beta x^2`, and prior `(1+t x)dx/2`. Its covariance is `4 alpha beta t/45`. The uniform risk is proportional in order to `(alpha beta)^2 t^2 M^{-2}`, including exact zero at the interior prior `t=0`. This illustrates the algebraic moment stratum `mu x^3 - mu x mu x^2 = 0`. The example is a consequence of the whole-class theorem, not the proposed replacement for a structural contribution.

### 2.4 Necessity as well as sufficiency for the all-prior quantifier

Section `sec:v18-universal` fixes an actual augmented product tangent `Ttilde = span{P} + im DP` and future test space `Phi`, each of dimension `p+1`. Theorem `thm:v18-universal-pairing` proves that normalized acquisition has rank `p` under every full-support prior if and only if the product of the two evaluation determinants has one weak sign everywhere and is nonzero somewhere.

Sufficiency follows from the classical determinant integration identity. Necessity uses the common sign of the pairing determinant along the convex set of full-support probabilities and approximation of atomic measures by such probabilities. Thus neither separate Chebyshev systems nor an ordered latent space is required. The matched-space consequence `Ttilde = P Phi` works on compact latent spaces of arbitrary dimension.

The square hypothesis is essential to the statement being proved and is explicit. We do not assert that every rectangular pairing has this characterization. Quantitative uniformity is proved on compact data families with a common positive likelihood bound, interior command neighborhood, and dominated full-support prior envelope. It is not asserted uniformly over unrestricted full-support priors approaching singular support.

## 3. Items already resolved and boundaries retained

The continuous-command model is retained verbatim in the finite-state definition and the circular and structural comparison sections. Finite reports, queries, detector cells, and persistent labels do not turn a real gate cube into a finite command alphabet. Neither a retained command-generation seed nor discarded history is available outside the charged state.

All four v17 inverse results remain unchanged. The real-budget envelope identity and the factor-two integer-budget sandwich remain distinct; repeated scales, zero padding, and zero contrast remain covered. The inverse concerns the complete unbounded checkpoint-risk curve within a proved representation, up to uniform comparison. It does not infer an unknown latent model, exact geometric configuration, exact minimax constants, or a last nonzero scale from finitely observed budget values.

The maximum over checkpoints is not fed into a checkpoint attribution inverse. The common-moment uncertainty law is not fed into the zero-product inverse because it has a positive error floor. The new affine invariant preserves these exclusions.

The original fixed-horizon collision and circular causal laws are retained with their full proofs. Known calibration and fixed read-only exact-real program remain part of their model. A general finite-precision compiler is not claimed for the newly introduced arbitrary compact latent-space class; all earlier monomial synthesis and resource theorems remain under their printed numerical interfaces.

## 4. Preservation, writing, and reproducibility

The principal exposition now proceeds from the broad rank classification to the affine resolution theorem, the universal criterion, and then the stronger multi-step collision and contrast laws. Detailed Fourier and information-state comparisons have been placed with the retained literature comparison appendix. No complete mathematical statement or proof from the preceding compiled submission is deleted or weakened.

The build reconstructs the pinned v17 compilation using its original unmodified preparer, then compares hashes of complete compiled statements and proof blocks, as well as labels, against the actual expanded v18 compilation. It expects all 88 preceding proofs and all 91 preceding statements, and eleven new statements with eleven proofs. Source preservation is a separate check from correctness. Historical administrative records and their original execution receipts are explicitly archived, never relabeled as current runs.

`validate.py` executes the unchanged v10–v15 and v17 author suites, the new rational diagnostics, and the complete three-pass LaTeX build. New checks cover the augmented-rank identity, actual report evidence and covariance normalization, projective inverse and Jacobian, determinant integration and its sign endpoints, the interior prior stratum, and an exact scalar quantization integral. They do not optimize over all encoders, certify uniform inverse-function radii, or replace the written arguments. The current execution receipt is the evidence for which checks actually ran.

The new real-geometric input is attributed to Bochnak–Coste–Roy, and the determinant identity to its classical source via Forrester's account. Existing references and equation-level Fourier attribution remain unchanged. This is a targeted source check, not an exhaustive priority investigation.

## 5. Requested renewed assessment

The renewed mathematical question is whether the experiment-first rank and prior-stratum classification, the whole-class covariance resolution theorem, and the exact square-pairing criterion supply consequences of greater reach than the preceding two model classifications and their envelope inverse. The existing collision-uniform and causal achievements remain part of that assessment.

We do not assert that a new section count, diagnostic total, or successful compilation reverses the referee's editorial judgment. Nor do we substitute a weaker theorem for a challenged one. The revised submission supplies the new statements and their complete arguments for an independent mathematical and editorial assessment at the originally requested standard.
