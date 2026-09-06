# Referee report — A1, English revision 14

**Manuscript:** *Attainable information geometry across exponent collisions*  
**Author named in the manuscript:** Qian Qi  
**Date:** 6 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica  
**Recommendation: REJECT at the requested four-journal level in its present form.**

This is an owner-requested, AI-assisted external referee-style assessment, not a report commissioned by any of the named journals. The recommendation is an editorial judgment about this submission. It is not a claim that the principal theorem is false, that the work is unoriginal, or that the research program cannot succeed.

## 1. Submission and scope

```text
repository:          TrillionniumFoundation/theta-theory
revision branch:     revision/a1-english-v14-geometric-response-2026-09-06
submission commit:   ffb9214b0fc7e218d6183c1f81bccb3e47587421
submission tree:     31365d60bd9740f2d1584b0defe4043f0e074755
submission time:     2026-09-06T13:49:26Z
principal directory: papers/A1-english-v14/
controlling review:  00b0844a7c2fb16b3231abf163d5004fd9e253cd
new review branch:   review/a1-english-v14-harsh-referee-2026-09-06
```

The branch head was checked again before publication and still pointed to this submission. The report applies to that immutable version. Source identifiers S0–S9 and literature identifiers L1–L4 are resolved in `SOURCE_INDEX.md`. Detailed calculations appear in `MATHEMATICAL_AUDIT.md`; executed checks and their limits appear in `EXECUTION.json` and `reproduce_review.py`.

I examined the new Section 6 in full, reconstructed its covariance, simultaneous perturbation, width and exact-prefix arguments, and checked their relationship to the main attainable classification. I also examined the main chain from the physical experiment and product tangent through confluent pairing, positive-history flag attainment, the bounded-format global cover and the causal recurrence. For the retained common-name result, I checked the overlapping-history converse, prior-envelope uniformity, paired-history stability and the common-advice upper construction. The numerical construction was inspected selectively and its current author suites were rerun. This is not a claim that every historical appendix has received a fresh, independent line-by-line verification. [S1–S8]

## 2. Overall assessment

Revision 14 is a substantive and substantially better organized response. It does not merely rename the scalar uncertainty floor. Section 6 proves a simultaneous ambiguity-set inclusion and resolves every Kolmogorov-width order, including directions that vanish at collisions. The distinction between the past's attainable dimension and the full future prior-ambiguity dimension is mathematically correct. The title, introduction and principal theorem now put the actual geometric classification first, and the implementation contracts have been moved out of the principal narrative. These changes deserve explicit credit. [S1, S4, S5]

**I found no blocking counterexample or essential unfilled step in the mathematical chain examined under its printed hypotheses. I found no new implementation defect in the scope of the present inspection and executed diagnostics.** Neither statement is a formal certificate of the entire manuscript. Both rule out using the previously repaired precision, horizon or common-name defects as grounds for rejecting this version.

My negative recommendation has a narrower basis. The paper still does not persuade me that its demonstrated contribution has the exceptional mathematical importance needed for the requested journals. The strongest result remains the collision-uniform attainment and resolution theorem. The new ambiguity theorem is correct, but its additional mechanism is a bounded right inverse for a finite-dimensional moment map followed by the already established Newton scaling. It gives a useful new interpretation and consequence; it does not establish a second comparably deep attainable-geometry theorem. The audit makes this reduction explicit rather than relying on the adjective “routine.”

This is a judgment about mathematical significance, not a disguised allegation of incorrectness. I have not found an existing paper containing the identical positive-history theorem, and I do not claim otherwise.

## 3. Disposition of the previous report

| Previous item | What v14 supplies | Disposition in this report |
|---|---|---|
| E13.1: an isotropic uncertainty floor does not resolve weak collision directions | Lemma 6.1, Proposition 6.2 and Corollary 6.3 give all ambiguity-width orders and an exact-prefix residual risk, under an expressly different local-data convention. | **A genuine mathematical response.** The previous absence of any direction-resolved result must not be repeated. The imperfect common-name theorem itself remains isotropic, as the author explicitly states. |
| E13.2: the attainable classification must carry the submission | The title, abstract, Theorem 1.1 and Sections 3–5 now identify the positive-history, global-cover and causal obligations separately. | **The expository part is addressed.** My remaining reservation concerns the significance of that clearly identified contribution, not a missing statement of it. |
| E13.3: the principal narrative is dominated by revision and implementation apparatus | The geometric/common-name/implementation hierarchy is explicit; the full compiler and contract material is in Appendices H–K. | **Substantially closed.** I do not retain this as a principal reason for rejection. Only limited editorial refinements remain below. |
| Earlier P12.1–P12.3 and the uniformity issue behind E12.2 | The relevant compiler/test sources are preserved; current suites pass, and the retained common-name proof has been checked in the stated scope. | **Remain closed in their previously identified scope.** The original independent v13 fault-injection script was not rerun in this standalone review. |

A fair review cannot convert compliance with a specific earlier request into a new claim that the requested result is absent. Conversely, closing these items is not an automatic positive decision on journal significance. [R, S1, S5–S8]

## 4. Mathematical findings

### 4.1 The main classification is more than a Vandermonde calculation

The profile is

\[
\Psi_{n,m}(M,a)=\max_{1\le j\le \min\{n(r-1),q_m\}}
 \left(\frac{\mathcal V_{m,j}(a)}{M}\right)^{2/j},
\qquad
\Xi_N(M,a)=\max_{1\le n<N}\Psi_{n,N-n}(M,a).
\]

Its nontrivial statistical content is the identification of which spectral directions can be excited by an actual past. The common interior binomial history has a product tangent of dimension \(n(r-1)+1\), supported on separated exponents even when future sums collide. Complete Hermite test blocks retain the required mixed-pairing rank. In the normalized differential, the product itself lies in the tangent and the evidence coordinate is nonzero, so exactly one direction is lost. This is the required rank argument; merely subtracting one from an ambient dimension would not suffice. [S2, S3]

The quantitative inverse argument retains the kernel coordinates and then integrates them out. The all-failure evidence remains in the subprobability measure. Consequently the lower bound is realized under one ordinary exploration law, not by conditioning on an event whose probability has disappeared from the loss. The compactness argument is taken separately for finitely many formal node orders; discontinuities in the selected Leja order do not invalidate the uniform bound. [S3]

The global cover is a separate argument. For each report word, the scaled posterior image is a rational image of command coordinates with positive polynomial evidence. Prior integrals are real coefficients in a formula of fixed semialgebraic format. Neither a semialgebraic prior nor a semialgebraic calibration set is needed. The thin-rectangle covering estimate uses this global complexity bound, not the local attained cube. The real metric-entropy input is applicable, and the integer label budget is handled explicitly. [S2, S3; L1, L2]

Finally, the causal update is performed in raw moments. Its denominator is bounded below on posterior mixtures, so its Lipschitz bound has no reciprocal collision gap. Updating a reachable representative gives another reachable state; a finite-horizon error recurrence then combines the checkpoint covers. This correctly distinguishes one causal transducer from unrelated checkpoint encoders. I found no gap in these steps. [S3]

### 4.2 The full normalized covariance remains nonsingular at collisions

Lemma 6.1 concerns the complete normalized test vector, not the raw observable vector. At a collision, repeated formal nodes generate complete logarithmic Hermite blocks. Together with the constant, these functions remain independent under any fixed full-support prior. Thus the covariance is positive definite even when multiplication by \(D_a\) subsequently annihilates some physical directions. [S4]

Continuity in the uniform norm, compactness of the exponent chamber and finitely many orders give a positive lower bound for a fixed prior. For a dominated family, the posterior inequality \(\nu_h\ge\kappa^n c_-\mu_0\), combined with the variational formula for variance, transfers that lower bound uniformly. This argument does not assume a Lebesgue density. Nor does it establish uniform constants over all full-support priors without a common lower envelope; the manuscript does not make that stronger claim.

### 4.3 The simultaneous body inclusion has the correct prior normalization

Let \(\Gamma=\operatorname{Cov}_{\nu_h}(\phi_a,\phi_a)\). For any \(v\in[-1,1]^q\), set

\[
f_v=v^{\mathsf T}\Gamma^{-1}(\phi_a-\nu_h\phi_a),
\qquad s=\varepsilon/(4C_0).
\]

Then \(\nu_h f_v=0\), \(\nu_h(\phi_a f_v)=v\), and the same \(C_0\) bounds every such perturbation. The prior is defined by

\[
d\mu'=\frac{1+s f_v}{1+s\mu f_v}\,d\mu.
\]

The denominator is essential at a nonconstant history. It makes the prior a probability and keeps its density ratio in the declared relative neighborhood. Bayes normalization then gives exactly \(d\nu_h'=(1+s f_v)d\nu_h\), not just a first-order expansion. Thus the lower inclusion realizes a whole common cube of normalized displacements. The upper inclusion follows from the exact normalized difference formula. [S4; audit A1]

The active block of \(L_a\) has uniform upper and lower operator bounds. Applying it to the diagonal cube therefore gives the claimed width orders \(\varepsilon d_{k+1}\), including zero widths at exact collisions. This is a valid simultaneous set statement, not an aggregation of incompatible directional two-point alternatives. The result determines comparison orders of widths; it does not determine an exact ellipsoidal shape or canonical principal axes.

### 4.4 Exact prefix information and the physical event are correctly scoped

For a nonzero active prefix, triangular back substitution makes equality of the first raw moments equivalent to equality of the corresponding normalized moments. This is an exact identity, not a stable inversion of noisy small pivots. The choices \(v=\pm e_{k+1}\) then give the lower bound, while the central prediction gives the upper bound. Hence the squared local minimax radius is \(\asymp\varepsilon^2d_{k+1}^2\). If the prefix fixes all distinct physical moments, the radius is zero. [S4]

The three-trial example is also correct. For \(A_\theta=\{0,1,2+\theta\}\), the two-trial future set has four separated groups and one merging pair. Its fifth Newton scale is of order \(|\theta|\), but neither checkpoint of the three-trial memory problem reaches that fifth direction. Thus \(\Xi_3\asymp M^{-1}\) coexists with the prefix-four residual radius \(\asymp\varepsilon^2\theta^2\).

The common-prior physical realization uses the event of constant failures, of probability \(2^{-n}\), and assigns zero payoff off that event. On it, exact conditional-moment constraints become exact prior-moment advice supplied before acquisition. This is a legitimate event-weighted decision problem. It is not the full unconditional payoff of Section 7, and it is not the uncertain-calibration, noisy-name problem. The text says so. Requiring those different problems to satisfy the same formula would change the theorem rather than identify an error in it.

### 4.5 The retained common-name law does not secretly choose the center

The common-name class has a dominated prior envelope, an interior center and explicit error slack. Those hypotheses allow two distinct priors to share the same name. Their history laws overlap and dominate a common law; they need not be equal. The prior-tilt converse gives a uniform \(\delta^2\) term using a visible one-step direction. The fixed center supplies the independent memory lower term. Combining these gives a lower bound of the order of their sum. [S5]

For the upper bound, paired histories give a Hausdorff comparison of the reachable raw moment sets, uniformly over the dominated family. The common numerical construction uses the name, not the unknown center, and stops on either its covering-radius test or the advice floor. This provides the matching order. The theorem is joint prior-and-calibration uncertainty, not calibration identification with a known prior. These distinctions remain valid and are not reopened by the new local result. [S5, S6]

## 5. Why the publication recommendation remains negative

### E14.1 — The new ambiguity theorem is a consequence of a general bounded-dual principle

The audit proves the following reduction without any monomials, sparse algebra, attainable-history dimension, or collision structure. For any bounded finite test vector with uniformly positive posterior covariance, bounded relative prior perturbations produce a normalized moment-displacement set containing and contained in constant multiples of an \(\varepsilon\)-cube. Applying any fixed linear observation map gives the corresponding pair of inclusions for its image.

The proof is exactly the centered covariance right inverse followed by the normalized pullback displayed above. In the present manuscript, the collision dependence is introduced by taking that linear observation map to be the already established \(L_aD_a\). The width calculation is then finite-dimensional singular-value comparison. The problem-specific work is the complete-flag covariance bound and its uniformity; that work is real, but its ingredients have already been established in the confluent flag analysis. [S4; audit A1–A2]

This observation does not make Proposition 6.2 false or vacuous. It correctly identifies its incremental mathematical content. The new statement is stronger than the old scalar floor, and its exact finite-radius formulation is useful. Nevertheless, the manuscript should not rely on it as a second major mechanism commensurate with the physical attainment theorem. The example separates two information classes on one model; it does not establish a new interaction between finite-memory acquisition and anisotropic uncertainty under one common imperfect name.

The latter interaction is not claimed, so its absence is not a correctness objection or a new mandatory theorem request. It explains why the author has answered a directional question without, in my assessment, resolving the outstanding case for exceptional significance.

### E14.2 — The strongest theorem is now visible, but its demonstrated reach remains insufficient for this recommendation

The central attainment result is the best part of the paper. My reservation is not that its tools are classical, that it fixes a horizon, or that it studies a special class; none of those facts alone rules out an outstanding paper. The reservation is the balance of what is actually established.

After the complete normalized flag is attained in this positive monomial setting, the remaining quantitative laws are controlled by a finite list of exterior products, a bounded-format covering estimate and a finite Lipschitz recurrence. The phase trees and examples evaluate that list. The prior-ambiguity widths apply the bounded-dual reduction. The common-name consequence combines an existing memory law with a visible uncertainty direction. The compiler implements covers with a carefully stated numerical interface. These are coherent results, but most are consequences of one model-specific geometric identification rather than independent mathematical advances of comparable weight. [S2–S7]

For the requested journals, I remain unpersuaded that the submission demonstrates a sufficiently substantial conceptual advance beyond that identification. The examples make its resolution phases transparent, but do not by themselves show wider mathematical force. This is a reasoned editorial assessment, not a theorem about journal policy and not an assertion that the identical result is already known.

A stronger presentation of the existing work would identify the attainment principle as a standalone result and give a theorem-level account of precisely what it adds to the closest spectral and entropy results. A genuinely different application could also change the significance assessment. Neither is prescribed here as an artificial extension checklist or a guarantee of acceptance. More preservation counts, another equivalent saturation formula, or another implementation contract would not answer the present reservation.

### Limited editorial refinements, not new blocking objections

The hierarchy requested in E13.3 is now present. It should be retained. The main introduction would benefit from a shorter theorem-level comparison with the nearest interpolation and real metric-entropy inputs, rather than leaving most detailed comparisons to Appendix L. In Section 6, “all width orders” is more precise than language suggesting an exact classification of the body or its axes. When describing the example, the known-calibration exact-prefix experiment should remain adjacent to its formula. The existing local/common-name distinction must not be lost in a future abstract or response letter.

These are local refinements. I do not characterize the revised main text as an uncorrected stack of implementation repair notes, and I do not ask the author to delete or weaken complete results.

## 6. Independent execution and its limits

The full workflow artifact was obtained through the authorized repository connection. Its archive digest matches GitHub's digest. The local source manifest has the same Git blob as the manifest at the pinned submission, and all **80** listed source SHA-256 hashes match. The standalone `validate.py` pipeline was actually executed, without the optional historical-review flag. [X]

The five author-written suites passed with **7,904; 8,207; 26,158; 12,944; and 7,400 assertions**, respectively: **62,613** in total. These are independent executions of author tests, not 62,613 independently designed checks or mathematical proofs. The three-pass rebuild produced **72 pages** with no undefined-reference or overfull warnings reported by the build checker. All 72 pages have the same extracted text as the submitted PDF. I visually inspected submitted pages **20, 21 and 22** at readable resolution, not all 72 pages. [X]

The preservation checks report **74** retained complete v13 proof blocks and **77** retained complete v13 named statements; the expanded manuscript contains **77** proof blocks and **80** named results. Source preservation is not proof verification. The older v13 independent reviewer script was not executed in this standalone run, and archived historical receipts are not counted as current execution.

The separately written `reproduce_review.py` imports no manuscript or author-test module. It constructs Newton functions through the leading coefficient of a confluent Hermite interpolation polynomial and uses exact rational power-log integrals. Its **60 configurations and 21,691 assertions** cover nonuniform full-support priors, a full-support prior with atoms at both endpoints, two nonconstant failure factors, interleaved repeated nodes, the three-pair additive collision for \(\{0,1,2,3\}\), and one-sided small gaps. It checks full covariance inverses, positive exact LDL pivots, simultaneous mixed directions, normalized prior pullback, raw-prefix preservation, physical product-query shifts, zero pivots and determinant products. All pass. [X]

In **30 nonconstant-history configurations**, an intentionally unnormalized prior tilt fails the total-mass check. These are successful negative controls showing that the diagnostic can detect the omitted denominator. The manuscript includes that denominator; these controls are not counterexamples to the submitted theorem.

These tests neither enumerate the continuum calibration chamber nor prove uniform constants, minimax lower bounds or priority. Their value is reproducibility and targeted fault detection. The mathematical judgment rests on the proofs discussed above.

## 7. Literature boundary

Selected primary sources were checked independently of the repository's literature log. Zhang–Kileel supplies the relevant bounded-format semialgebraic regularity input; the real inequality recalled by Comte–Halupczok supports the variation-based covering argument. Their entropy results are not positive-history lower theorems. Clustered Vandermonde spectral results concern matrix scales and require a separate comparison of their regimes with this fixed real-node setting; they do not construct admissible histories. Approximate-information-state theory provides related control context, not the exact collision-uniform label profile established here. [L1–L4]

This targeted comparison does not constitute an exhaustive priority search. None of the checked sources is presented as an identical-theorem refutation. The negative recommendation must not be inflated into an unsupported assertion of nonoriginality.

## 8. Final recommendation

I do not recommend acceptance or minor revision at the requested four-journal level. **The unresolved issue is the demonstrated mathematical significance of the principal classification and the incremental nature of its new bounded-dual consequence, not a newly discovered false theorem.**

The direction-resolved result is a real advance over the scalar uncertainty discussion, and the principal organizational request has been addressed. No new blocking mathematical or implementation error is asserted in this report. The earlier repaired issues remain closed in their stated scope. A further review should not manufacture new defect labels simply because this editorial recommendation remains negative.

Only this new review directory is added. The submitted manuscript, historical derivations, existing reviews, default branch and revision branch are not modified by this report.
