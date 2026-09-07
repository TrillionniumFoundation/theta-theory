# Response to the referee on A1 English v21

**Revised manuscript:** *Attainable information geometry in positive experiments*, Qian Qi, English v22.  
**Controlling report:** `reviews/a1-english-v21-independent-2026-09-07/REFEREE_REPORT.md`, commit `36910a7c6fd08e5ad2e8e10db7c2d8c71c463de8`.  
**Examined submission:** `7c44bdccc91667c583b5d5cbcff3f8d9160a57d6`, `papers/A1-english-v21/`.  
**New manuscript:** `papers/A1-english-v22/`.  
**Date:** 7 September 2026.

We thank the referee for separating the correctness of the inspected arguments from the editorial assessment of their significance. We have made the three requested local corrections and added a second complete multistep application of the transfer theorem. The latter is a mathematical response to E21.4, not a claim that a publication decision follows from a proof ledger or a test count.

The monomial collision theorem, its parameter chamber, its uniformity and its full proof are unchanged. The exact-kernel theorem is unchanged, including exact realization rather than mere containment. All 122 v21 theorem, lemma, proposition and corollary blocks remain byte-identical in the compiled manuscript. Of the 120 prior proof blocks, 118 remain byte-identical; the other two have only the references requested in E21.2 changed. Their original versions remain in the inherited core and original v21 sources. Seven additional statement/proof pairs develop the new application. No companion argument has been replaced by a summary.

## E21.1 — definitions in the actual reading route

The first main-theorem setup now explicitly defines

`I=[l,u]=[0,1]`, `D=a_{r-1}`, `mA={a_{i_1}+...+a_{i_m}}`, `h_A(m)=|mA|`, `0A={0}`, and `h_A(0)=1`.

It distinguishes sets of distinct sums from the formal labels that retain collisions. This paragraph precedes `core/02_experiments.tex`, `build/exact_information.tex` and the mixed-moment and binomial-tangent arguments in the actual `main.tex` input order. Thus the definition is available where each inherited symbol is first used. The source validator checks these mathematical definitions explicitly, in addition to TeX references.

**Locator:** `sections/introduction.tex`, first main-theorem setup. **Disposition:** corrected without changing a theorem.

## E21.2 — consequences follow the principal proof

The intrinsic-bit proof now invokes `thm:resolution-main` instead of the alternative streaming equation. The collision-tree proof likewise invokes `thm:resolution-main` instead of the pair of direct appendix classification theorems. All their calculations, statements and other text remain intact.

`REVISION_EDITS_V22.json` records the two exact old/new replacements. `build.py` derives the consequence file from the unchanged inherited core and checks that these are the only differences to the retained proof blocks. The complete alternative route remains in Appendix D and is described as an alternative in the introduction, not a dependency of the revised main consequences.

**Locators:** `build/collision_consequences.tex`, `cor:intrinsic-bits`, `thm:collision-tree`. **Disposition:** corrected.

## E21.3 — SWAT metadata

The active bibliography now reads **20th Scandinavian Symposium on Algorithm Theory (SWAT 2026)** for Terao's paper. LIPIcs 370, article 39, pages 39:1–39:19, and DOI `10.4230/LIPIcs.SWAT.2026.39` are retained. The publisher record was checked directly on 7 September 2026. The old bibliography source remains unchanged for provenance; `main.tex` uses the corrected `references-v22.tex`.

**Locator:** `references-v22.tex`, `Terao2026`. **Disposition:** corrected.

## E21.4 — substantive reuse rather than an umbrella formulation

The referee identifies a precise gap in the contribution case: the one-step covariance theorem, local exact-kernel theorem and monomial multistep law operate at different levels, and their coexistence does not demonstrate a second multistep use of the transfer principle. We have not responded by giving that coexistence a new name. The new section proves a second complete experiment-level classification.

Let `f=(f_1,...,f_d)` be bounded continuous functions on a compact latent space, with `span{1,f_i}` closed under multiplication through bounded coefficients. Acquisition uses the positive binary reports `(1+y u^t f)/2` on a fixed command cube. The future query menu is explicitly constructed from actual remaining-trial products and selected after the label. For `Sigma=Cov_mu(f,f)`, Theorem `thm:algebra-multistep` proves

`R_{M;n} ~ max_l (||wedge^l Sigma|| / M)^(2/l)`

at every positive checkpoint, and the corresponding maximum-over-stages law for a single causal filter with arbitrary integer stage budgets. Its constants depend only on the dimensions, multiplication bound, command radius and fixed horizon. They are uniform over **all** priors, including support loss, and simultaneous covariance rank losses. This additional prior uniformity belongs to the new class; it is not retroactively asserted for the monomial theorem.

The geometric and causal verifications are supplied, not assumed:

1. **Whole histories.** Bounded multiplication represents every likelihood product as `a_n+b_n^t f`. Exact integration gives `v_n=mu f+Sigma b_n/(a_n+b_n^t mu f)`. Both the coefficient bounds and evidence lower bound are uniform. This puts the complete reachable image in a covariance ellipsoid, not just a local patch.
2. **Actual acquisition mass.** At a constant-command prefix, the first-command derivative of the coefficient coordinate is the identity before applying `Sigma`. A quantitative inverse argument integrates a positive-volume neighborhood of the remaining commands and includes the actual all-positive-word probability. This gives a ball-density lower bound for one common exploration law at every checkpoint, without a covariance inverse.
3. **Causality.** Multiplication supplies a displayed raw-moment Bayes update with denominator at least `3/4`. It preserves reachability and is uniformly Lipschitz without recovering discarded commands or inverting a covariance. The transfer theorem supplies the accumulated-error convolution and the sharp integer-budget causal law.

The proof is therefore a substantive reuse of the existing transfer theorem, with a different mechanism for every geometric input. It also extends the earlier affine covariance calculation beyond one step under a verifiable algebraic condition. The finite-channel corollary computes the joint acquisition/query attenuation scales and their crossover; the operational-inverse corollary recovers the covariance exterior-power products from the entire causal budget curve.

We have stated the scope of this extension exactly. A finite-dimensional real function algebra has a finite observable quotient; this is proved in `prop:finite-observable-quotient`, including the fact that a well-conditioned partition basis is unnecessary. Multiplication closure is not asserted for arbitrary continuous detector spaces. The new result does not turn the general exact-kernel theorem into an unrestricted multistep theorem, remove the fixed horizon, or replace persistent label cardinality by total machine memory. Those statements would require different arguments. The original interval theorem and all companion results remain in full.

**Principal locators:** `sections/algebra_multistep.tex`; `thm:algebra-multistep`, `lem:algebra-product-chart`, `lem:algebra-acquired-density`, `lem:algebra-update`, `prop:finite-observable-quotient`, `cor:algebra-attenuation`, `cor:algebra-operational-inverse`.

**Disposition:** new mathematical response provided for independent evaluation. We do not label the referee's significance judgment a missing lemma, claim to have proved an acceptance recommendation, or infer significance from compilation and diagnostics.

## Verification and preservation

The published v21 manifest is pinned by Git blob `14d877c7db051926fe461ccfbe007093a786e860`, independently matched to the downloaded source. The build verifies all 748 listed baseline source hashes, reconstructs its generated TeX from the pinned historical preparation chain, and checks formal-block and label preservation against that reconstruction. The current source manifest and explicit edit registry are separate from the generated execution reports.

`validate.py` reruns the inherited suites and the new exact diagnostic script, checks optimization-mode reproducibility, rejects an actual mutation of an inherited proof, and compiles the full manuscript three times without shell escape. Actual counts and PDF hashes are recorded in `validation/EXECUTION_REPORT.json`, not presumed here. `tests/verify_v22.py` compares coefficient products and raw updates with direct finite-latent Bayes calculations, including zero channels, boundary priors and redundant character algebras. Finite diagnostic success is not a substitute for the analytic density, covering or coding proofs.
