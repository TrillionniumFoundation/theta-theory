# Response to the referee — A1, English revision 17

**Manuscript:** *Attainable information geometry in positive experiments*  
**Author:** Qian Qi  
**Date:** 7 September 2026  
**Controlling review:** `reviews/a1-english-v16-independent-2026-09-07/REFEREE_REPORT.md`, with its `MATHEMATICAL_AUDIT.md` and `SOURCE_INDEX.md`, at `0ef7e8bd90c0767b7fdc0f2bd175548242e39cec`.  
**Reviewed submission:** `9f6875ebf1473b84dcde2ccabcb1556202233276`, `papers/A1-english-v16/`.  
**Revision branch:** `revision/a1-english-v17-referee-response-2026-09-07`.

We thank the referee for distinguishing the correctness of the principal arguments from the assessment of their significance, and for identifying the command-alphabet ambiguity precisely. We respond to both current items. The earlier positive-history, arbitrary-collision, circular, directional-ambiguity, common-name and effective results remain in the manuscript, with their full statements and proofs. The revision adds an inverse classification result, rather than a third application or a relaxation of the experiments.

## E16.1 — Continuous commands, finite detector and finite memory

**Correction made.** In `sections/structural_comparison.tex`, the phrase “the specified finite detector commands” is replaced by commands acting on the specified four-cell detector with acceptance probabilities in the continuous gate cube. The same distinction is now stated beside the physical circular interface and in the introduction.

The command is a real vector in `[eta,1-eta]^4`. The four detector cells, five possible reports, finite future-query menu and `M` persistent labels are separate objects. The independent uniform acquisition law is on the continuous cube. No finite command alphabet is assumed in either lower bound.

We agree with audit A6: replacing that cube by a fixed alphabet of `B` commands produces at most `(5B)^n` command-report prefixes at checkpoint `n`; at fixed horizon a finite read-only-clock transducer can index all of them. That is a different experiment and it is not the one covered by the positive all-budget contrast profile. We have corrected the wording without altering the command domain, any theorem, the query convention, the treatment of failures, or a proof.

**Locations:** the physical-experiment paragraph of `sections/circular.tex`; the comparison paragraph of `sections/structural_comparison.tex`; the circular-model paragraph of `sections/introduction.tex`.

## E16.2 — The mathematical content of the classification

The referee credits the match of actual attainment, observation scales, global entropy and causal compatibility, but asks whether the resulting theorem package establishes a sufficiently consequential classification. We answer mathematically, rather than changing the description of the same formula.

### 1. A converse to the direction already proved

The new section `sections/operational_reconstruction.tex` proves that the entire optimal integer-budget regret curve determines every past-attainable exterior-volume order, uniformly through the singular strata. If

\[
V_\ell=\prod_{i=1}^{\ell}s_i,\qquad
 e_s(M)=\max_j(V_j/M)^{1/j},\qquad
 c e_s(M)^2\le R_s(M)\le C e_s(M)^2,
\]

for ordered nonnegative scales, then the operational transform

\[
\mathcal I_\ell(R_s)=\inf_{M\in\mathbb N,\,M\ge1} M R_s(M)^{\ell/2}
\]

satisfies

\[
c^{\ell/2}V_\ell\le\mathcal I_\ell(R_s)\le2C^{\ell/2}V_\ell.
\]

The proof supplies the supporting real budget `V_ell/s_ell^ell`, controls its upward integer rounding, and treats repeated scales, zero scales and zero products beyond the attained rank separately. It does not replace a finite alphabet by a real-valued “budget.” In the zero-product case the infimum is obtained as a limit over arbitrarily large integer budgets, not by claiming exact prediction at some finite budget.

It follows that uniform comparison of whole regret curves is equivalent to uniform comparison of all the corresponding truncated products. The products are therefore necessary as well as sufficient for this operational comparison. Consecutive nonzero ratios recover the individual scale orders; their zero sets recover the acquired rank. This is stronger information than the small-error dimension slope alone.

### 2. What this says for the principal monomial theorem

The new monomial corollary applies the inversion to the actual optimal unconditional and worst-history checkpoint regrets of Theorem `thm:intrinsic-checkpoint`. The complete Leja-product estimate identifies its ordered products with the maximal determinant volumes, uniformly even at coincidences. Thus

\[
\inf_{M\ge1} M\bigl(R^a_{n,m}(M)\bigr)^{\ell/2}
\asymp \widehat{\mathcal V}_{n,m;\ell}(a),
\]

where the right side is the determinant volume through `p_(n,m)` and zero thereafter. A change in a past-attainable volume order cannot be hidden from every memory budget by a dimension calculation. Conversely, uniformly comparable truncated volume profiles give uniformly comparable curves.

This is a classification of finite-resolution prediction laws up to uniform constants. It does not purport to recover the locations of every exponent or every additive relation from the risk curve, or to prove an isomorphism of statistical experiments. In particular the exact order of each unresolved collision volume, not an arbitrary label assigned to a stratum, is the operational quantity.

### 3. Why the circular example remains part of the same theorem structure

The second new corollary recovers

\[
\mathcal I_{2j-1}(R^\tau)\asymp\tau^{2j^2},\qquad
\mathcal I_{2j}(R^\tau)\asymp\tau^{2j(j+1)}.
\]

Their ratios recover both real copies of `tau^(2j)`. Even though odd orders do not add a dominant branch to the displayed circular risk law, they are not lost: repeated scales give a concave product sequence and its odd products are recovered at the common supporting budgets. At zero contrast all physical products vanish. The acquired `tau^j` and future-query `tau^j` factors therefore have a measurable consequence in the complete memory law; the theorem is not just a Fourier representation theorem.

### 4. Relation to the referee's coding reduction

We agree with audit A3 that once a minorized attainable flag, a dimension-controlled global cover and a compatible Lipschitz stage update have been established, the coding implication is a rectangular covering and quantization calculation. We do not present that reduction, or the elementary envelope inversion in the new lemma, as a novel general coding theory. The experiment-specific work remains exactly where the referee locates it: the separated product tangent and complete confluent pairing for arbitrary additive collisions, and the symmetric-polynomial acquisition map together with the physical Fourier metric for vanishing contrast.

The new conclusion specifies why identifying those particular products is a classification rather than merely a useful bound: the operational curve recovers them. This necessity statement depends on the already proved uniform two-sided laws. A local rank or a matrix singular-value estimate without histories would not supply it for the actual experiment. Its proof also explains why the entire curve, rather than one asymptotic exponent, is needed.

The inverse statement is confined to exact-known-experiment checkpoint curves. It does not infer every checkpoint from the maximum-checkpoint causal curve, does not reinterpret a common-name error floor as acquired memory, and does not recover the untruncated ambiguity body from a short past. The manuscript states these distinctions explicitly. The original causal and common-name theorems remain complete and unchanged.

### 5. Significance and the requested standard

Our positive case is now a two-way operational classification: the attained volume profile determines the sharp curve and is recoverable from it, while actual histories and a single causal implementation give the forward law its operational meaning. The arbitrary-collision and vanishing-contrast mechanisms identify different physical origins for that profile within the same finite-memory question. No additional application is being offered as a substitute for this assertion.

The manuscript retains its full theorem scope and the requested mathematics-journal presentation. The new theorem is supplied with its complete proof and separate corollaries, not with a claim that a wording correction or a successful build settles mathematical importance. Whether this package merits the requested journal standard is a matter for renewed specialist assessment; this response does not record a journal acceptance or an independent referee decision.

## Current-item disposition

| Item | Revision action | Evidence for re-review |
|---|---|---|
| E16.1 | Corrected the finite-command wording and clarified the four distinct finite/continuous objects. | Introduction, structural comparison, circular physical model. |
| E16.2 | Added inverse reconstruction and a complete uniform-comparison characterization, with full proofs for both model specializations. | `lem:integer-envelope-duality`, `thm:operational-reconstruction`, `cor:monomial-operational-recovery`, `cor:circular-operational-recovery`. |
| Previously accepted E15.1/E15.2 response | Retained the Bayesian Fourier attribution, acquisition-observation comparison and resource disclosures; linked the new inverse theorem to that comparison. | Original comparison text, bibliography and new section. |
| Preserve the complete theorem package | Every v16 named statement and complete proof is retained byte-for-byte in the compiled expansion. | `V16_PRESERVATION_MANIFEST.json` and the newly executed preservation report. |

## Verification and scope

`validate.py` runs the six inherited author suites unchanged, the new exact rational envelope diagnostics, and a three-pass TeX build. With `--prior-review`, it also executes the pinned v16 referee's mathematical diagnostics without the optional old-artifact check. That execution is a regression rerun, not an independent review of revision 17. Its original source is pinned by SHA-256.

The actual run receipts, not expected counts, are in `validation/EXECUTION_REPORT.json`; source and statement/proof preservation are checked separately. None of these finite tests proves the continuum-uniform analytic theorems, novelty, or journal significance. The old review, old revisions and default branch are not modified or merged.
