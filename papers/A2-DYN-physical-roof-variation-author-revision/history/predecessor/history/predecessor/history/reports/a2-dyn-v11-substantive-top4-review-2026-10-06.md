# Substantive external top-four referee report on A2-DYN revision 11

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v11-referee-response-2026-10-06`, `revision/a2-dyn-v11-referee-copy-2026-10-06`  
**Reviewed commit:** `dfacd56110f80a9621671028d2aa0a5782659055`  
**Reviewed repository tree:** `90fbf66bc99b6b0ba2df7b9e93f36c74d79dd463`  
**Active manuscript directory:** `papers/A2-DYN-v11-referee-response`  
**Reviewed v10 author baseline:** `3e45e41b5be6ef636944f67dce529fdc9fd4fcc9`  
**Controlling v10 report:** `reviews/a2-dyn-v10-external-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Controlling v10 report commit / blob:** `a42dc1401007f9f8025c916106884e09d7d864f0` / `e6732df7a22bc7e161ac4650e74e9fdce80d52b3`  
**Earlier v11 identity-notice review commit:** `7816b7acc4b6e35bf5183161fb7b7776fed5b3ef`  
**Date:** 6 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards-specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 11 contains a genuine new mathematical result. It is not merely a publication wrapper around revision 10. The new marked-return theorem extends the integrated growing central band from initial collision-state insertions to one initial, terminal, or intermediate actual-return insertion, uniformly in the location of the mark. The argument recenters the physical orbit at the marked return, splits the centered record into an actual backward and forward collision sum, and places the smoothed insertion exactly between two chronological collision-operator powers. It does not replace the randomly evaluated mark by a deterministic-clock surrogate, and it does not assume mixing or a spectral gap for the induced first-return map.

I found no decisive counterexample in the new marked-return proof chain. The two-sided compensation identity is consistent with the convention on section visits; the backward and forward clock-window estimates follow from collision-space covariance bounds and invertibility; the long/short block separation in the spectral product is logically appropriate; and the displayed frequency and variation exponents are internally coherent. The same-event conditioning corollary correctly divides an unconditional marked estimate by the probability of the unchanged event, with explicit restrictions on probability decay and variation growth.

The negative recommendation has two independent grounds.

First, the paper continues to organize itself around the parameter-uniform raw mixed-density local limit theorem. Revision 11 advances the class of admissible central insertions, but it does not close the remaining load-bearing parts of that theorem: uniform positive definiteness of the four-dimensional covariance; the full complementary-frequency integral, including the annulus beyond the proved growing central band; and the complete critical/singular raw branch decomposition with quantitative local edge and derivative-sum estimates. The exact-event physical conditioning problem also remains open beyond the same-event return-state bridge proved here.

Second, the exact reviewed SHA does **not** pass its own source-qualification workflow. GitHub Actions run `37349121832` completed with conclusion `failure`. The failing step was the source-preservation/build step, and the exact error was

`RuntimeError: changed inherited mathematics: 06_downstream.tex`.

This directly contradicts the source manifest and validation prose claiming that all twenty-seven inherited v10 core files remain byte-identical. The exact-SHA workflow stopped before completing the native article build. The reviewed source also contains visible source defects, including `Section~\nef{sec:marked-return-band}` in `main.tex`, and a stray punctuation/operator fragment in the event display in the new marked-return section. These packaging defects are repairable and do not themselves refute the marked theorem, but a top-four submission cannot be source-qualified by a manifest whose preservation assertion is disproved by the repository's own exact-SHA check.

Accordingly, the present packet is not ready for acceptance at any venue. After the source identity and exact build are repaired, the unconditional Gaussian, functional, growing-major-arc, and marked-central-band package may form a strong specialist contribution, subject to independent expert verification. At the requested top-four benchmark, however, the main raw-density endpoint remains incomplete.

## 2. Frozen source and chronology

The two named revision-11 branches resolve to the same commit:

`dfacd56110f80a9621671028d2aa0a5782659055`.

The active article is `papers/A2-DYN-v11-referee-response`. Its source manifest identifies revision 10 at `3e45e41b5be6ef636944f67dce529fdc9fd4fcc9` as the mathematical baseline and the substantive v10 referee report at `a42dc1401007f9f8025c916106884e09d7d864f0` as the controlling review.

Revision 11 adds two named core files:

- `core/28_marked_return_band.tex`;
- `core/29_norm_source_map.tex`.

The first contains the new mathematics. The second is principally a source-to-norm map for the collision-space framework already used in the v9/v10 chain.

There is already a branch named `review/a2-dyn-v11-external-top4-review-2026-10-06`. Its report is a source-identity notice written before the substantive v11 source was visible to that review; it explicitly says that it is not a new mathematical review of a distinct revision. I therefore do not treat it as the referee report on the present v11 article. This report is placed in a separately named substantive-review path and branch so that the two historical objects are not conflated.

The source chronology itself is clear enough to identify the mathematical object under review. The defect is not ambiguity about which SHA was reviewed. The defect is that the supporting preservation and workflow claims at that SHA are false.

## 3. What revision 11 actually adds

For a complex collision-state insertion `a`, zero off the actual section, and a mark `0 <= k <= n`, the new transform is

\[
 C^{[k],a}_{n,R}(v)
 =\int_{Y_R^*} a((F_R^*)^k x)
   \exp\!\left(\frac{i v\cdot(J_{n,R}(x)-n\bar G_R)}{\sqrt n}\right)
   \,d\nu(x).
\]

The theorem proves, uniformly in the radius, mark index, return count, and insertion,

\[
 \int_{|v|\le 2n^{1/200}}
 \left|C^{[k],a}_{n,R}(v)
       -\alpha_a e^{-v^{\mathsf T}D_Rv/2}\right|\,dv
 \le C\left(
 M_a n^{-3/280}\sqrt{\log(2+n)}
 +V_a n^{-9/175}
 \right),
\]

where `M_a` is the supremum norm, `V_a` is the initial-coordinate BV norm, and `alpha_a` is the insertion mass.

This is stronger than the v10 initial-insertion theorem in two respects.

1. The insertion may be evaluated at any actual return from zero through `n`, including the terminal state.
2. The supremum and variation losses are separated, so the BV norm may grow at a controlled polynomial rate even when the supremum norm remains bounded.

The theorem remains a central Fourier integral. It is not a complementary-frequency estimate and it is not a raw density theorem.

The same section derives a conditional characteristic estimate for a return-state event left unchanged on both sides of the comparison. If the event probability is bounded below by `c n^{-beta}` and the event indicator has BV norm at most `C n^kappa`, the stated sufficient conditions

\[
 \beta<3/280,
 \qquad
 \beta+\kappa<9/175
\]

make the conditioned central characteristic error tend to zero. This is a useful and nontrivial bridge, but its scope is exactly a single return-state event with controlled initial-coordinate variation.

## 4. Audit of the exact marked compensation identity

The conceptual step is to set the marked return `y=(F_R^*)^k x` as collision time zero. The manuscript defines `N^-_{k,R}(y)` as the collision distance to the `k`th preceding section visit and `N^+_{n-k,R}(y)` as the collision distance to the `(n-k)`th following visit. It then asserts

\[
 J_{n,R}((F_R^*)^{-k}y)-n\bar G_R
 =\sum_{j=-N^-_{k,R}(y)}^{N^+_{n-k,R}(y)-1}
       h_R(T_R^j y).
\]

I checked the endpoint convention. The negative part contains the `k` visits from the initial return state through the visit immediately before the mark. The nonnegative part contains the remaining `n-k` visits, including the marked state when nonempty and excluding the terminal right endpoint. Thus the indicator of the section sums to exactly `n` over the full collision interval. Substitution of

\[
 h_R=f_R-\bar G_R\mathbf 1_{Y_R^*}
\]

then gives the identity with no random remainder.

The change of variables from `x` to `y=(F_R^*)^k x` is legitimate because the actual first-return map is invertible and preserves the normalized section measure. The manuscript writes the integral against the restricted collision measure rather than always against its normalization; the constants are consistent with the definition of the insertion mass.

No independence of the past and future is used or needed. This is an important strength of the argument.

## 5. Audit of the two-sided clock windows and stopping error

The backward clock estimate is not obtained by a time-reversal symmetry of the section. Instead the proof applies the same bounded section-indicator covariance estimate to forward and backward collision iterates. Invariance identifies the scalar lag correlations, and invertibility supplies the actual preceding visits. Chebyshev's inequality then gives

\[
 \nu_R^*\{|N_{j,R}^{\pm}-\lfloor j/c_*\rfloor|>b\}
 \le C\frac{j+b}{b^2}.
\]

This form is appropriate also near the endpoints `j=0` and for a threshold larger than `j`; the lower event is empty when the corresponding deterministic collision time is negative.

The stopping comparison takes `b_n` of order `n^{3/5}`. The union of the two exceptional clock events has probability `O(n^{-1/5})`. On the complement, a forward and a backward deterministic-window maximal estimate controls the difference between the random two-sided sum and the deterministic interval centered at the mark. This produces

\[
 C M_a\left(n^{-1/5}+|v|n^{-1/5}\log n\right).
\]

The proof does not try to estimate an unbounded stopped sum on the exceptional event. That avoids a common mistake in random-time characteristic estimates.

The argument is uniform in `k`, including the two endpoints. I found no contradiction in this portion of the proof.

## 6. Audit of the marked collision-operator product

After smoothing, the deterministic two-sided collision integral is represented as

\[
 \ell\!\left(L_z^s M_{a_\delta}L_z^r\nu\right).
\]

The chronological order is correct: the right power records the collisions before the marked state, the multiplier is evaluated at the mark, and the left power records the collisions after the mark.

When both blocks are long, the spectral decomposition is applied on both sides of the multiplier. The principal amplitude at zero is the insertion mass. The projector perturbations produce an amplitude loss controlled by the multiplier norm and one factor of the spectral perturbation; the cubic eigenvalue remainder is multiplied by the insertion supremum rather than by a second unnecessary multiplier loss. Complementary terms decay with the shorter long block.

When one side is shorter than the logarithmic threshold, the proof deletes that short real-frequency segment directly and applies the one-sided collision estimate to the remaining long block. This is preferable to claiming exponential complementary decay on a block whose length is too small. The two short blocks cannot occur simultaneously because the total deterministic collision length is comparable to `n`.

The resulting bound separates

- `delta V_a`, from smoothing the insertion;
- errors multiplied by `M_a`, from the bounded multiplier and collision observable;
- the logarithmic short-block cost;
- the collision smoothing, covariance, amplitude, cubic, and complementary terms.

This separation is the main technical advance of revision 11. It is also what permits an indicator with growing boundary complexity to remain admissible under the displayed rate condition.

The imported collision-space multiplier and density embeddings remain load-bearing. The new norm-source map is helpful, but an independent specialist should still check the exact local-space identification, boundary reparametrization, matched stable-curve estimates, and restriction from the rectangular cover to the triangular quotient.

## 7. Frequency bookkeeping and the variation budget

The final choice uses the same growing rescaled radius as revision 10 and a smoothing scale selected so that

\[
 \delta V_a=V_a n^{-9/175}.
\]

The remaining integrated terms reproduce the v10 central rate or decay faster. The displayed rational exponents are mutually consistent. In particular, the theorem does not conceal the four-dimensional volume factor in a pointwise estimate.

The condition

\[
 M_a+n^{-3/280}V_a\le B
\]

is a convenient sufficient uniform class because the variation contribution then decays faster than, or at least is controlled relative to, the main central error. The more explicit theorem with separate `M_a` and `V_a` is preferable and should remain the primary statement.

For an event indicator, `M_a` is fixed while `V_a` measures boundary complexity in the original collision coordinates. This is a real restriction. A long dynamically pulled-back event will generally not have a uniformly controlled variation norm merely because it is measurable at one return. The theorem avoids that problem only for events that are given as controlled functions of the marked return state itself.

## 8. Audit of the conditional bridge

The conditional corollary applies the marked theorem with the indicator of an event measurable at the chosen return. Its numerator is the marked complex measure, and its zero-frequency mass is exactly the event probability with the same normalization. Dividing by that probability gives the conditional characteristic function.

The sufficient inequalities on `beta` and `kappa` are obtained by comparing the denominator loss with the two unconditional rates. This algebra is correct.

The theorem does **not** replace one conditioning event by another. It does not compare an exact physical-time observation with a completed-return observation, and it does not control the relative symmetric difference of two rare lattice events. The paper is careful about this limitation, and the referee report should preserve it.

Likewise, a central characteristic estimate under a rare event is not yet a conditional local limit theorem. Such a result still needs the weighted complementary-frequency integral, weighted edge extraction, and a nondegenerate covariance on the relevant conditional scale.

## 9. Exact-source qualification failure

This issue must be corrected before the manuscript is circulated as a qualified revision.

The source manifest states:

> All 27 v10 core files and inherited Python diagnostics remain byte-identical and included.

The exact reviewed SHA disproves this statement. Workflow run `37349121832`, job `111895192485`, checked out exactly `dfacd56110f80a9621671028d2aa0a5782659055`. The source-preservation/build step failed with

`RuntimeError: changed inherited mathematics: 06_downstream.tex`.

Inspection confirms that the v11 copy of `core/06_downstream.tex` is not the v10 blob. A stray leading `+` was inserted before a displayed centered sum. This particular character does not appear to change the intended mathematical assertion, but it invalidates the blanket byte-identity claim and correctly triggers the preservation gate.

Because the verification script exits at this point, the exact-SHA workflow does not establish a successful native build of the v11 article. The uploaded artifact contains partial evidence, not a qualified final PDF produced after all checks.

There are further visible source defects:

1. `main.tex` contains `Section~\nef{sec:marked-return-band}` rather than `Section~\ref{sec:marked-return-band}`. Unless an undocumented macro exists, this is an undefined command.
2. The marked-return section contains a stray punctuation/operator fragment in the displayed definition of the event used for the conditional corollary.
3. Supporting validation prose should not describe preservation or remote qualification as successful when the exact remote run failed.

The authors should create a new revision SHA, restore every inherited file exactly or explicitly document any intended modification, correct the TeX defects, regenerate all hashes, and obtain a successful exact-SHA workflow. The old SHA should remain immutable as the failed packet.

This objection is not cosmetic. Source identity and reproducibility are repeatedly presented as part of the manuscript's proof governance. Those representations must be accurate.

## 10. Remaining mathematical blockers for the raw LLT

### 10.1 Uniform positive definiteness

The paper proves a continuous positive-semidefinite covariance and identifies its kernel with an actual `L^2` coboundary. It still lacks a regularity theorem permitting the transfer function to be evaluated or telescoped on the selected periodic orbits. Therefore the periodic rank calculation cannot yet rule out a nonzero zero-variance direction.

The growing and marked central-band theorems are valid at singular covariance. The raw four-dimensional density theorem is not. A uniform lower eigenvalue bound remains indispensable.

### 10.2 The complementary-frequency integral

The proved physical central radius is of order

\[
 n^{-1/2+1/200}.
\]

The previously contemplated outer control begins farther away, around a scale such as `n^{-2/5}`. The intervening annulus is genuine. Revision 11 does not supply an integrated estimate over it, nor over the full compact nonzero torus frequencies, growing roof frequencies, and far tail.

The marked theorem inherits this boundary. Moving a multiplier to an intermediate return does not create a complementary-frequency resolvent estimate.

### 10.3 Complete critical and singular branch decomposition

The individual critical-edge calculations and exact jump subtraction remain valuable. The initial-coordinate BV norm of a one-collision observable, however, does not control second distributional derivatives of all many-return inverse-coarea densities.

The full raw theorem still requires a decomposition that includes every regular critical word, central critical branch, grazing or competing-root singular boundary, and any dynamically generated image boundary. All nonintegrable jumps must be extracted, and the remaining derivative norms must be summed with their actual `n`-dependence.

### 10.4 Weighted and exact-event tails

Revision 11 extends the central theorem to one marked return-state insertion. It does not establish complementary tails for terminal, intermediate, or exact-event weights. Nor does it prove the relative event-replacement estimate needed to pass from completed-return conditioning to an exact physical observation.

These are not consequences of the same-event central bridge.

## 11. Top-four significance assessment

The compensation-and-stopping architecture is elegant. Revision 9 proved Gaussian and functional limits for an unbounded induced record using a bounded collision compensation. Revision 10 upgraded the compact central limit to a growing integrated major arc. Revision 11 now shows that one can insert a controlled observable at any actual return without pulling its variation back through a long induced iterate.

Taken together, these results are mathematically substantial. A reorganized paper whose main endpoint is this unconditional package could be competitive in a strong specialist journal after source repair and independent expert review.

At the requested benchmark, however, one normally expects either the advertised raw mixed-density theorem to be completed, or the compensation/marked-insertion method to be formulated as a general theorem with several genuinely different and substantial applications. The current article remains tied to one carefully engineered triangular Lorentz family and leaves the main density mechanisms conditional. I therefore do not regard the present result as meeting the significance and closure threshold of *Annals*, *Acta*, *Inventiones*, or *JAMS*.

## 12. Required work before another top-four review

The following order is recommended.

### A. Repair and requalify the exact source

- restore or explicitly account for every inherited core file;
- correct `\nef`, the stray marked-event fragment, and any further TeX defects;
- regenerate the source manifest from the actual tree rather than from an intended local packet;
- rerun normal and optimized diagnostics at the exact remote SHA;
- complete native typesetting and inspect the produced PDF;
- make the supporting validation and publication-status records match the actual workflow result.

A new referee should review the repaired SHA, not silently reinterpret the failed one.

### B. Prove covariance nondegeneracy

Supply a theorem converting the `L^2` coboundary into a representative or periodic approximation to which the explicit periodic rank applies, or prove uniform positive definiteness by another method. The theorem must handle the discontinuous section contribution and be uniform in the radius.

### C. Close the full complementary frequency region

Give an integrated estimate from the edge of the proved central ball through the intermediate annulus, compact nonzero frequencies, growing roof frequencies, and the far tail. All constants and splice inequalities must be explicit enough to verify a strictly nonempty parameter range.

### D. Complete the raw branch sum

Construct the full extracted edge measure and prove the uniform residual integrability/local edge conditions with actual return-count growth. Do not infer these bounds from trajectory total variation or one-collision BV.

### E. Extend the weighted theory to the conditioning application

For the exact physical conditioning theorem, prove weighted complementary tails, edge bounds, and a relative event-replacement estimate for the actual indicators being used. State precisely which insertion classes are stable under the required operations.

### F. Obtain independent specialist review

At minimum, the following should be checked by experts in dispersing billiards and anisotropic transfer operators:

- the Demers--Zhang common-space and multiplier import;
- the semialgebraic treatment near grazing, tangency, and competing roots;
- the collision covariance and smooth perturbation chain;
- the two-sided marked spectral product;
- the future cohomology/nondegeneracy bridge;
- the complete raw critical/singular decomposition.

## 13. Presentation and technical comments

1. Theorem C should state explicitly in its introductory synopsis that `a` is integrated with respect to the unnormalized restricted collision measure used in the displayed transform, and relate this once to the normalized section probability.
2. Keep the separated `M_a` and `V_a` estimate prominent. The combined admissibility norm is useful but hides the reason growing boundary complexity is allowed.
3. Distinguish consistently among a marked return-state event, a terminal event, a multiple-time path event, and an exact physical observation event.
4. State the backward-clock endpoint conventions before the first two-sided identity.
5. The phrase “terminal insertion” should not be read as a terminal raw lattice indicator; it is a bounded-BV function of the terminal return state.
6. Retain the explicit warning that the marked theorem does not imply induced mixing.
7. Record the physical and rescaled cutoff radii beside every inversion statement.
8. Do not describe the existing v11 identity-notice report as a substantive referee acceptance of the present mathematics.
9. Remove publication-status wording that can be mistaken for journal publication or proof certification.
10. After source repair, include the exact successful workflow run ID and artifact hash in the validation record.

## 14. Verification boundary

I reviewed the source text, the new marked-return arguments, the source manifests and proof ledgers, the exact branch and commit identities, and the actual GitHub Actions result at the reviewed SHA. I did not independently reconstruct all continuum billiard singularity estimates or formally certify every inherited proof.

Finite arithmetic diagnostics can check exponent identities, clock-counting models, and source hashes. They cannot establish the imported collision-space theorem, the semialgebraic continuum partition, covariance nondegeneracy, a high-frequency resolvent, or the global coarea branch sum.

The present recommendation is therefore an editorial and mathematical referee assessment at the requested standard, not a formal proof certificate.

## 15. Final conclusion

Revision 11 makes a credible mathematical advance: the integrated central Gaussian comparison survives a single insertion at any actual return, uniformly in the mark, with a useful separated variation budget and a correct same-event rare-conditioning consequence. I found no decisive counterexample in that new proof chain.

Nevertheless, the raw mixed-density LLT advertised as the organizing endpoint remains conditional on nondegeneracy, the complementary-frequency integral, and the complete raw residual decomposition. In addition, the reviewed source packet fails its exact-SHA preservation/build workflow and contains inaccurate source-identity claims. For these reasons I recommend rejection at the requested top-four benchmark and require a repaired, newly qualified source before any further mathematical review.