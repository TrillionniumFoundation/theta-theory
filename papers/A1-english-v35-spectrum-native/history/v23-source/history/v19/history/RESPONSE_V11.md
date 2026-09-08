# Response to the effective-finite-memory v10 report

**Revised manuscript:** *Sparse observation algebras and certified memory across exponent collisions* (A1 v11).  
**Controlling review commit:** `1aa4599eedca650d34c3778a00f3ad854c2bc9d7`.  
**Reviewed submission:** `d9f48fe08fd694e636c287be7646ae7d723ce3b8`.  
**New branch:** `revision/a1-english-v11-referee-response-2026-09-06`.

We thank the referee for distinguishing the validity of the classification, the effectiveness of its numerical realization, the sensitivity of the diagnostics, and the judgment of mathematical significance. This revision addresses each of those matters without replacing the full profile by a single floor, restricting the arbitrary-prior classification, or deleting the retained proofs. The response concerns the effective-finite-memory report, not the other v10 submission with a different mathematical subject.

The new manuscript contains the complete old proof chain and ten additional proved results. The mathematical response goes beyond the sharper uniform mesh suggested in the technical note: a finite two-sided covering certificate now selects a profile-dependent mesh from approximate feasible histories. This gives explicit sufficient program-size phases for the full collision profile. We request a fresh assessment of that combined statement, not an inference of editorial merit from passing tests.

## P10.1 — Replace insensitive decoder and off-grid diagnostics

**Change.** `tests/test_v11.py` checks every stored output at every retained representative and every physical query, including all nonconstant queries. The reference probabilities are independently computed by multiplying univariate exponent-keyed polynomials and integrating them against the exact prior. This differs from the formal-label, perturbed-input algebra used by `MomentAdvice`. Neither `Audit.exact_vectors` nor the approximate compiler output is treated as ground truth.

Nine physical programs cover exact collision, a gap of `10^-12`, and a separated calibration, with budgets 1, 2 and 4 and two full-support priors. There are 495 stored query entries. The original output tables satisfy their declared accuracy allowance. Replacing every output by zero is detected in all 495 entries. Replacing only nonconstant outputs by zero is detected in all 444 affected entries. The actual index-only `Machine` is used for the causal checks.

The finite program also has a separate residual certificate, Proposition 7.6 (`prop:program-certificate`). It measures the chosen transition targets and each decoder entry against independently reevaluated representative histories. A zero decoder has a large measured output residual; it cannot inherit a small certificate merely because its entries lie in [0,1].

**Off-grid sensitivity.** The physical fixtures use the sharper, explicitly justified constants `L=13/2`, `G=8`, and query Lipschitz bound 1. For accepted reports the command multiplier cancels; their state constant is at most 22/5. A failure factor has coefficient l1 norm at most 13/16 and evidence at least 1/4, giving L=13/2. Its pointwise command variation is at most the command maximum norm, giving G=8 after normalization. The actual off-grid command distance is at most 1/2048. The resulting 864 state checks and 5,184 all-query causal checks use bounds strictly below one half, not a threshold larger than the entire unit error range. The largest query bound is about 0.433271; the largest observed error is about 0.003355.

The domain of these physical fixtures is stated precisely: a finite off-grid neighbourhood of the eight command vertices, not an asserted 1/2048-net of the entire three-dimensional cube. Separate adaptive interval fixtures use genuine nets of their full command domain and exhaustive words from a non-dyadic off-grid test alphabet. This keeps diagnostic coverage distinct from the all-history analytic theorem.

**Historical reproduction.** The exact original author files again pass 7,904 checks. The unmodified referee mutation script again shows that zeroing the old decoder passes that old suite. Both receipts are preserved separately; the defect is not hidden by overwriting the old test or relabelling its result.

## P10.2 — Exercise actual finite numerical inputs

**Change.** The compiler now receives dyadic cell coefficients and formal prior moments with signed entrywise errors. It does not compute exact prior integrals and only round its final output. Equal true moments at exact collisions are deliberately supplied with unequal numerical values, retaining all formal labels. The original parameter values and exact priors are available only to the independent test oracle.

Lemma 7.7 (`lem:explicit-moment-certificate`) supplies a fully explicit input certificate. If each report factor has coefficient norm at most B, put `Cf=Jr` and

`D_n = n Cf (B+1)^(n-1) + (B+1)^n`.

Entrywise errors at most epsilon imply errors at most `epsilon D_n` in prefix evidence and raw numerators. The condition `epsilon D_n <= kappa^n/2` gives positive computed evidence. A quotient error is bounded by `2 epsilon D_n / Z_tilde`; exact query coefficient norms give the stated query variant. The proof telescopes products in coefficient l1 norm and then controls the two integrations and the quotient. It does not assume that approximate moment tables describe an actual posterior.

`MomentAdvice` implements that interface and its positivity checks. Every physical program is compiled from these perturbed tables. Independent raw-state comparisons, all-query comparisons and off-grid execution then check the resulting program against the true experiment. The fixed input tolerance is strictly inside the proved budget; both positive and negative perturbations occur. These finite tests exercise the new hypothesis without being offered as its proof.

## P10.3 — Stronger precision and read-only program accounting

**Adopted refinement, with attribution.** Proposition 7.1 (`prop:separated-floor`) proves the separated-chain argument from the referee's technical note, including r=2 and d0=1. For `d0=(r-1) floor(N/2)`, it gives

`Xi_N(M,a) >= (delta_K/H)^(d0-1) M^(-2/d0)`.

Corollary 7.2 (`cor:uniform-resources`) deduces sufficient precision `log2(M+1)/d0 + O(1)` and program size `O(M^(1+J/d0) log(M+1))`. The synthesis count and exclusion of arbitrary oracle running time are explicit. The choice of variable precision uses integer comparisons and needs no numerical additive-gap lower bound. The entire profile Xi, not merely the separated-chain floor, remains the target and the achieved regret.

**Further mathematical consequence.** Lemma 7.3 (`lem:radius-certificate`) proves

`max(0,r/2-h) <= e(M) <= r+(A+2)h`

from the observable greedy radius r of approximate feasible-history samples. Theorem 7.4 (`thm:adaptive-compiler`) stops at the first dyadic mesh satisfying `r >= 4(A+2)h`. It proves termination when `e(M)>0`, first-success scale control, a two-sided final certificate, an all-history causal error bound, and finite program-size and synthesis bounds. An absolute-tolerance variant handles e=0 without testing equality.

Lemma 7.8 (`lem:cover-profile`) then proves `e(M)^2 ~ Xi_N(M,a)` in both directions. The lower direction uses the existing checkpoint converse through an admissible clipped linear query decoder; it does not assume the new causal theorem. Theorem 7.9 (`thm:profile-adaptive`) consequently selects

`b(M,a) = (1/2) log2(1/Xi_N(M,a)) + O(1)`

with sufficient program size

`O(M Xi_N(M,a)^(-J/2) log(M+1))`.

The algorithm receives neither Xi nor a collision stratum. Data are requested at successive certified tolerances offline. It learns a covering scale, not an exact exponent equality.

For the four-cell, five-trial example, Corollary 7.10 (`cor:resource-phases`) gives

`O(min{ M^(5/3), rho^(-1) M^(3/2), (rho^2 tau_c)^(-4/9) M^(13/9) } log(M+1))`

as a sufficient program bound, omitting reciprocals of zero. These scales track the full three-term regret profile. The uniform precision is at most `(1/6) log2(M+1)+O(1)`, independently of the high-contact order. The old logarithmic-precision and M^5 program bounds remain true and their proofs remain in Section 6; Section 7 explicitly supersedes them with the stronger statements.

**Resource quantifiers.** Only the persistent-label regret has a matching converse. The displayed precision is the precision chosen by this algorithm, not the minimum precision required by every possible algorithm. No program-size converse, uniform oracle-time bound, unknown-calibration guarantee, or growing-horizon assertion has been substituted for a proved statement. The original scope of the intrinsic theorem is preserved.

## P10.4 — Theorem-specific comparison with finite approximation literature

Section 1.2 compares the assumptions, input objects and conclusions of the specific results requested by the referee. The full primary theorem statements were consulted, including the displayed formulas rather than abstracts alone:

* Saldi–Yüksel–Linder, Theorem 5.3 and its supplementary assumptions, with the Section 6 order-optimality discussion acknowledged.
* Kara–Yüksel, Assumption 4 and Theorem 12, including the stability and discount conditions and the finite-window resource.
* Subramanian–Sinha–Seraj–Mahajan, Definition 7 and Theorem 9, with their action-compression Theorem 17 acknowledged.

The comparison does not claim that finite-state approximation, predictive representations, a Lipschitz error recurrence, action compression, or farthest-first selection originates in this manuscript. Nor does it say that the cited theories are contained in the present theorem. The precise added conclusion being defended is synthesis with a prescribed M-label budget from finite evaluation data, with a computable two-sided covering certificate and a profile-sensitive numerical realization tied to an independently attained lower law.

The classical Vandermonde, divided-difference and greedy components remain separately attributed. The separated-chain improvement is attributed to the controlling referee technical note. No exhaustive priority certification is claimed from this targeted comparison.

## P10.5 — Preserve the mathematical scope and proof chain

All ten inherited body files retain their exact Git blob hashes. The new preservation manifest checks all 49 complete proof blocks in the expanded v10 manuscript and all 52 old named-result labels. The current expanded manuscript contains 59 complete proofs; no v10 complete proof was removed or rewritten. The main summary theorem is strengthened, while the underlying exact-state statements and the earlier sufficient numerical realizations remain present.

The direct proof order remains: experiment and operational model; attainable transversality; classical analytic inputs with their attribution; global intrinsic collision classification; finite numerical compilation; certified resources. The observation algebra, affine specializations, five- and seven-trial laws, sequential decision results and mechanical/common-risk comparison remain in the appendices with their own hypotheses. No saturated affine argument is used to replace the sparse curved-image argument. Positive prefix evidence, actual future-trial cost, query-after-compression timing, and the absence of uncharged history are maintained.

## E10.1–E10.3 — Mathematical significance and the revised claim

The new section is not offered as a new interpolation theory. Its concrete additional consequence is that the attained collision profile controls a sufficient finite numerical realization and can be recovered to the needed order without prior identification of the collision geometry. The proof includes the adaptive stopping rule, its two-sided certificate, certified perturbed input, separate decoder residuals, and resource phases of the full intersecting arrangement. These strengthen the theorem actually submitted, not only its introductory description.

The report's editorial judgment is not marked as mechanically closed. Correct proofs, meaningful tests and explicit resource accounting provide grounds for renewed mathematical assessment; they do not predetermine that assessment. The revision maintains the full mathematical ambition through stronger statements and complete proofs rather than asserting acceptance or enlarging a test count.

## Execution and verification record

`validate.py` checks the source manifest, freshly reruns the exact v10 author suite, the independent referee suite and original mutation control, runs the new suite, and compiles the paper three times without shell escape. The new suite records 8,207 finite checks; the legacy counts remain separately reported as 7,904 and 36,960. The manuscript compiles to 55 pages locally with no undefined references or overfull boxes. All 55 rendered pages were inspected in page contact sheets, with the principal theorem and new certificate pages inspected at larger size.

The receipts distinguish source preservation, finite numerical diagnostics, and mathematical arguments. `validation/REVISION_VALIDATION.json` identifies the actual build environment and PDF hash. The publication workflow commits only to the new revision branch after successful checks and preserves all older source and review paths.
