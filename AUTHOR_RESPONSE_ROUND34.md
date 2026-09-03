# Author response to Round 34 — Round 35

**Controlling report:** `REFEREE_REPORT_ROUND34_GPT56_PRO_HARSH.md`, Git blob
`9aae7570d710c5804f703c21fab212bc11e21aa1`, at immutable review commit
`9f5276233b63218a0d89df6611381975dc873232`.

## Principal response: a verified mechanical interface

The new manuscript proves results for an explicitly coupled infinite damped
oscillator lattice. Unknown damping and stiffness enter the physical generator;
the observation is one position coordinate with Gaussian readout noise. The
initial state is an infinite-dimensional nuisance and need not be known,
reinitialized, Gaussian, or supported by a density. Any prior on the prescribed
bounded initial-state ball is allowed, even if it misses the true initial state.
Its effect on parameter inference is proved to be transient.

Four force-duration words produce global parameter separation. Positive
conditional probabilities for these words are implemented on disjoint blocks.
The random signs eliminate interference from the pre-existing state. A physical
energy estimate independently gives filter forgetting. The posterior theorem
then follows from proved empirical contrast and likelihood localization, rather
than an assumed testing package. The same infinite model supplies a nonzero
memory kernel with an explicit square-root resolvent and derived finite-initial-
preparation evidence amplitudes.

This addresses the report's demand for a real mechanical interface, not another
independent calibration sensor. It does not falsely identify a damped lattice
with an elastic hard-sphere gas or a Sinai billiard.

## R34-M1 and R34-M5: a definite research object

The new focused publication unit is `ROUND35_REVISION.tex`. Its principal
construction is `lem:r35-embedding` / `prop:r35-certificate` /
`lem:r35-excitation`; the verified statistical consequences are
`thm:r35-lan`, `thm:r35-bvm`, and `thm:r35-filter`. They concern a specified
infinite mechanical model, not an unspecified hypothesis library. The original
eleven targets remain in the ledger, but this revision does not call eleven
corrected notes eleven newly completed research papers.

The proposed contribution is the constructive combination of a finite
persistent-excitation library, nonlinear mechanical parameter response,
infinite transient nuisance, uniformity across bounded feedback policies, and
explicit posterior/filter/memory consequences. Novelty and journal significance
remain matters for independent evaluation; a build or a proof label cannot
settle priority.

## R34-M2: hypothesis-level literature comparison

| Interface | Closest checked material | What is used or different here |
|---|---|---|
| Adaptive posterior without normalized information convergence | Du, Nair, Janson, arXiv:2511.06639v1, Theorem 1 and Appendix F | Theorem 1 has adaptive observed covariates and a mean linear in the unknown coefficient. Here the mean is the nonlinear response of an infinite hidden lattice. Its global contrast, derivative bounds, and integrated initial-state correction are proved. The absence of an information limit is not claimed as a new general principle. |
| Analytic-scale evolution | Finkelshtein, arXiv:1412.8628, equation (2.12), Theorems 2.1/2.4/2.10 | The Round 33 equal-radius majorant is retained as classical methodology. The new bounded-generator model does not need that theorem and does not claim to improve its constants or uniqueness class. |
| Bayesian linear system identification | Bryutkin, Levine, Urteaga, Marzouk, arXiv:2507.11535v2 | Their abstract describes canonical finite-dimensional LTI parameterizations. That prior scope is acknowledged. No unverified theorem from that paper is imported. |
| Infinite-dimensional evolution posteriors | Nickl, arXiv:2407.14781v3 | The abstract concerns inference on an initial function for parabolic evolution. Our unknown is a fixed local coefficient pair under adaptive forcing, and initial-state uncertainty decays. This scope comparison is not a claim of stronger infinite-dimensional BvM theory. |

The latter two comparisons were made from the authors' research-scope statements,
not represented as complete theorem audits. No exhaustive priority search is
claimed. The paper retains the distinction between an adaptive Gaussian
posterior approximation and frequentist confidence coverage.

## R34-M3: nonemptiness now includes coupled mechanics

Take c,k in [1,2], bath damping 3/2, bath pinning 1, coupling 1/10 and duration
1/32. The exact rational certificate proves the derivative condition over the
whole rectangle. Nine banded-operator powers are computed locally; a norm-series
tail bounds every omitted infinite-lattice power. The squared Frobenius upper
bound is below 0.036375 < 1/4, and the accompanying first-coordinate value bound
is below 3. This is neither a parameter grid nor an assertion that a finite
truncation alone proves the infinite system.

The excitation result permits arbitrary remaining feedback actions, unknown
persistent initial states, and positive coupling to infinitely many unresolved
coordinates. The state forgetting comes from the physical energy identity;
it is not asserted for an undamped measure-preserving system.

## R34-M4: no unsupported dependency promotion

The new theorem chain is energy -> response/initial-transient estimates ->
two-duration embedding -> randomized global contrast -> likelihood localization
-> parameter posterior/evidence. Filter-jet contraction uses energy and nuisance
bounds on a separate branch of that chain. Memory is proved directly by the
physical block equations. Finite-preparation amplitudes are consequences of the
proved evidence formula.

The original 40 application-open response items are not mechanically relabelled
closed. The new lattice interfaces are additional verified model results; the
stronger billiard/hard-sphere exports keep their own identifiers and obligations.
The revised ledger explicitly sets `all_original_gaps_closed` to false.

## R34-C2-01: bounded versions on zero-evidence sets

Corrected in active `round35/supporting/C2.tex`, retained locator
`thm:r33-c2-evidence`, and in `thm:r35-bounded-evidence` of the focused appendix.
Both conditional versions stay in [-||F||infinity,||F||infinity], with zero as
an allowed null-set version. The proof now uses N=ru and N_n=r_nu_n everywhere.
The report's exact rational epsilon=1/10 counterexample is reproduced, and the
corrected F=0 version has zero error. A further finite nontrivial hidden-state
example exercises the inequality with a limiting zero-evidence observation.

## R34-B1-01: the singleton endpoint

Corrected in active `round35/supporting/B1.tex`, retained locator
`thm:r33-b1-density`, and in `prop:r35-anchor-endpoint`. The whole Gamma statement
now requires integer m>=2. At m=1, W_1=0 almost surely and the joint law is the
Gaussian graph law, not a Lebesgue density. The larger-anchor Fourier smoothing
budget is unchanged. The tests check both the singleton and relative-energy
orthogonal decomposition.

## Additional specification remarks

Active B3 now assumes p>=2 before invoking Minkowski in L^(p/2), proves finite
sums first and passes by monotone convergence. Its later p>2 grid theorem is
unchanged. Active C2 specifies a standard Borel mark space, sigma-finite
deterministic intensity, predictable integrands, joint/progressive driver
measurability and the common usual filtration with representation property.
No varying-filtration conclusion is inserted.

## Source integrity and independent review scope

The new sources are materialized before verification and publication. Four
canonical entries point to Round 35 wrappers; the remaining entries and all
Round 33 chapter sources stay intact as historical material. The read-only
verifier builds only the declared new review unit and supporting corrections,
not uninspected old manuscripts. Tests read the active erratum statements as
well as exercising independent examples. The exact certificate is an explicit
limited proof certificate; the full statistical manuscript has not been
checked in a formal proof assistant.

The next review should scrutinize in particular the two-duration global
embedding, uniform net argument, nuisance derivative bound, posterior tail
normalization, strong filter-jet topology, and infinite Jacobi branch choice.
None is hidden under a reference to a failed upstream manuscript.
