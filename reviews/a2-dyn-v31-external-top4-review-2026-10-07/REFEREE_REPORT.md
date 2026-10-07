# External top-four referee report on A2-DYN revision 31

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v31-referee-response-2026-10-07`, `revision/a2-dyn-v31-referee-copy-2026-10-07`  
**Reviewed commit:** `c0b184a89ff3d38675d0bc90a9e60b584476e5c3`  
**Reviewed repository tree:** `d72006cb8d1a39c879ca04af4f61519c19f6b3b4`  
**Frozen ordinary paper tree:** `06d63ae32efec644d907a0d3d0118c54b8e74c4c`  
**Active manuscript directory:** `papers/A2-DYN-v31-referee-response`  
**Active core tree:** `71dd0bc4fad553308e57e2d18a474b75eed15368`  
**Qualified revision-30 baseline:** `a8b400deb4c262bee2978aec3e19cc68aa5439e2`  
**Controlling substantive report:** `reviews/a2-dyn-v30-external-top4-review-2026-10-07/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `cbe93c16bfde35e40b0de647c17d91939cfd6cc1` / `5a92130e7ef47c27cd77d34337e02c02205eccc2`  
**Date:** 7 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards-specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 31 is a genuine and mathematically substantive response to the latest report. It does not merely enlarge the theorem list or rename a previous cutoff. The new geometric extraction supplies, for the first time in this manuscript, an explicit long-time second-derivative budget for an exact residual at a physical-collision cutoff proportional to the number of returns. The proof is organized on the initial collision cylinder and sums over disjoint source pieces, rather than multiplying a per-itinerary estimate by an uncontrolled number of symbolic words. This directly addresses one of the most serious unresolved obligations identified in revision 30.

The same construction yields an exact reduction of the full actual prescribed-return law at three singleton lattice coordinates and a bounded, or even shrinking, roof interval to one finite Fourier integral with arbitrarily small inverse-polynomial absolute error. The far-roof part is now controlled with an explicit bandwidth whose logarithm is `O(n log n)`. This is real progress at the original microscopic resolution, rather than another mesoscopic window statement.

I found no decisive counterexample in the two new mathematical modules audited below:

- `core/63_geometric_raw_regularization.tex`;
- `core/64_microscopic_finite_band_inversion.tex`.

In particular, the positive-matrix argument behind the transverse roof direction, the use of all candidate tangencies, the source-side integrations by parts, the all-label derivative summation, and the logarithmic total-variation cost in finite-band interval inversion form a coherent chain. The manuscript also states the scope of the new results with unusual care.

The negative recommendation is nevertheless unavoidable at the requested benchmark. Revision 31 reduces the microscopic probability to a finite Fourier integral but does not estimate that integral on the remaining complementary frequency region. Its cutoff may be as large as

```text
B_n = exp(O(n log n)),
```

whereas the inherited prescribed-return spectral estimates cover much smaller, explicitly delimited bands. The new theorem therefore does not turn the finite integral into a Gaussian main term.

Moreover, the exact pointwise raw identity still contains two uncontrolled terms:

1. the density of the geometrically extracted small-total-variation measure, which is small in `L^1` but may be arbitrarily tall on a set of small measure;
2. the finite complementary inverse of the new residual, covering balanced, compact nonzero, peripheral, and growing-roof regimes outside the proved domains.

Thus the pointwise common signed correction remains open. So do the microscopic Gaussian denominator, the relative replacement of the original exact physical-time event, and the necessary weighted theory for the final downstream conditioning class. The parameter-uniform raw mixed-density local limit theorem around which the article is titled and organized is still not proved.

At a top-four journal, a technically powerful reduction is not a substitute for the headline local theorem when the remaining finite integral and pointwise correction contain the central Fourier-analytic difficulty. The manuscript has accumulated a large and valuable body of unconditional geometry, Gaussian theory, phase arithmetic, conditioning, and bridge results, but revision 31 still stops one theorem before the advertised raw endpoint.

## 2. Frozen source and revision chronology

The two named revision-31 author branches resolve to the same commit:

`c0b184a89ff3d38675d0bc90a9e60b584476e5c3`.

The repository tree at that commit is

`d72006cb8d1a39c879ca04af4f61519c19f6b3b4`,

and the ordinary paper tree is

`06d63ae32efec644d907a0d3d0118c54b8e74c4c`.

Revision 31 is based on the qualified revision-30 article and preserves all sixty-two inherited core modules and all inherited Python files. It adds exactly two mathematical modules:

- `core/63_geometric_raw_regularization.tex`;
- `core/64_microscopic_finite_band_inversion.tex`.

The article synopsis adds Theorem V. The new source also records the exact six main-text and bibliography edits, retains the inherited labels, and distinguishes the new geometric residual from the earlier power--logarithm jet residual.

The controlling report is the revision-30 report at commit

`cbe93c16bfde35e40b0de647c17d91939cfd6cc1`.

That report acknowledged the completion of the mesoscopic stationary conditioning and Gaussian-bridge pipeline, but identified the following remaining microscopic obligations:

- the complete prescribed-return-count complementary Fourier integral;
- a pointwise common signed raw correction, or an equivalent full inversion estimate;
- a long-time inverse-coarea derivative budget at a collision cutoff proportional to the return count;
- a fixed-label and microscopic-time denominator;
- relative replacement of the original microscopic physical event;
- weighted raw estimates for the actual downstream selector class.

Revision 31 closes one of these obligations in a strong form and advances another to an exact finite-band reduction. It does not close the full list.

The present review branch starts directly from the reviewed revision-31 author commit and adds this report only under

`reviews/a2-dyn-v31-external-top4-review-2026-10-07/`.

No manuscript source, author branch, workflow, prior report, or unrelated repository path is modified.

## 3. Source qualification and verification boundary

The exact-source qualification runs for both reviewed author branches completed successfully:

- response branch run: `37598429395`;
- referee-copy branch run: `37598494805`.

The static validation record states that the verifier checks the complete ordinary source tree, all sixty-four included core modules, all inherited labels, byte identity of the sixty-two inherited core modules and inherited Python files, exact edit replay, references, environments, workflow identity, and source/build receipts. The finite diagnostics check the collision differential conversion, positive matrix products, degree-eight discriminants, divergence signs, long-time exponent budgets, and selected high-precision physical words.

These checks are useful provenance and execution evidence. They do not certify the continuum all-candidate cutoff, the zero extensions across every finite branch, the source-side derivative summation, the finite complementary integral, or the raw local limit theorem. The manuscript and its validation record correctly disclaim such a certification.

## 4. Scope of this review

I have not attempted to re-prove every result in the 197-page, sixty-four-module article. The substantive mathematical scope is:

1. the two modules added in revision 31;
2. their interfaces with the cumulative return tail, inherited prescribed-count bands, coherent raw correction, and local inversion theorem;
3. the claims made in the abstract, Theorem V, proof ledger, referee response, and publication-status record;
4. the exact distinction between a finite-band reduction and a completed microscopic LLT.

The inherited Gaussian, covariance, phase-rigidity, mesoscopic-window, physical-conditioning, and bridge theorems are treated as the qualified baseline of the present revision. This report does not convert their previous referee-style assessment into formal proof certification.

## 5. Audit of the transverse roof direction

### 5.1. The one-collision differential

On a regular collision branch the manuscript writes the one-step differential in `(alpha,p)` coordinates as

```text
DT_R = -P,
P = [[(v+c)/c', v/(c c')],
     [v+c+c',   (v+c')/c]],
```

where `v=tau_R/R`, `c=sqrt(1-p^2)`, and `c'=sqrt(1-(p')^2)`.

This is consistent with the standard derivative formula in arc-length and angle coordinates after the stated changes `r=R alpha` and `p=sin(phi)`. Its determinant is one in the invariant flat coordinates. All entries of `P` are positive away from grazing.

The manuscript then observes that the ratio of the first to the second entry in either row of `P` is bounded by

```text
H_0 = 1 + R_+/ell_0 = 53/6.
```

The first row of a positive product is a positive linear combination of the rows of the rightmost factor. Its entry ratio is therefore a weighted average of those two row ratios. Up to the harmless common sign of the derivative product, this gives

```text
0 < A_m/B_m <= H_0
```

uniformly in the word length.

I find this argument correct and notably efficient. It avoids an interior incidence-angle lower bound, which would be false near grazing and would destroy the desired all-word statement.

### 5.2. Exact action identity and the vector field

Using the retained collision-action identity, the manuscript has

```text
partial_alpha L_m = R(p_m A_m-p),
partial_p     L_m = R p_m B_m.
```

Consequently,

```text
partial_alpha L_m - (A_m/B_m) partial_p L_m = -R p.
```

This gives

```text
|grad L_m| >= c |p|
```

and, outside the initial normal strip,

```text
X_m = -(Rp)^(-1)(partial_alpha-(A_m/B_m)partial_p),
X_m L_m = 1.
```

This is the conceptual core of revision 31. It replaces branchwise critical-value analysis by one source-space direction transverse to every regular total-roof level. The normal line `p=0` is removed once in the initial state; separate neighborhoods of every output critical value are not needed.

I found no algebraic defect in this step. For publication, however, the coordinate conversion and action identity should be placed together in one self-contained lemma or appendix. They are load-bearing enough that a reader should not have to reconstruct signs, curvature conventions, and invariant-coordinate determinants from several distant sections and one external reference.

## 6. Audit of the all-candidate singularity cutoff

### 6.1. Why all candidates are needed

The cutoff uses a finite parameter-independent set of possible next scatterer centers and includes the discriminant of every candidate disk, not merely the disk selected on the current branch. This is the correct geometric choice. At a tangency, the selected first-hit disk may disappear on one side of the singularity; a cutoff referring only to the selected branch would not automatically vanish on both sides.

Uniform finite horizon makes the candidate set finite. Distinct disks are separated, so a positive collision root cannot switch between two disks through an ordinary root crossing at the same entry point; the change occurs through one of the candidate tangencies. Together with grazing and the explicit section boundaries, these are the one-step branch-change loci relevant to the construction.

### 6.2. Polynomial sublevel estimate

In bounded half-angle charts the discriminant is a rational function whose denominator is positive and bounded, while its numerator has degree at most eight. The manuscript proves an elementary two-variable polynomial sublevel lemma with exponent `1/(2D)` and applies it with `D=8`, obtaining the safe loss

```text
epsilon^(1/16).
```

Finiteness of the candidate set and compactness of the radius interval are used to obtain a uniform positive lower bound for the maximum coefficient of each nonzero numerator. The proof that the numerator cannot vanish identically is sound: at a fixed boundary point, varying the outgoing unit direction cannot make the squared cross product with a point outside the disk identically equal to `R^2`.

This yields a one-step cutoff with removed measure `C epsilon^(1/16)` and fixed-order derivative bounds polynomial in `epsilon^(-1)`.

The argument is plausible and, in my judgment, substantially stronger than an itinerary-count estimate. It is also one of the passages that most needs an independent billiards specialist. A journal version should spell out:

- the finite candidate set and its uniform construction;
- the complete bounded chart cover of the angular circle;
- the positive denominator bounds in every chart;
- the continuity argument giving the uniform coefficient lower bound;
- a standalone lemma that every first-hit label transition is covered by the listed discriminants.

These details are currently present in compressed form. I did not find a contradiction, but they should not remain dependent on an expert filling in several geometric steps.

## 7. Whole-itinerary cutoff and zero extension

The full cutoff is

```text
Gamma_{L,R,epsilon}(x)
 = theta(p(x)/epsilon) product_{j=0}^L chi_{R,epsilon}(T_R^j x).
```

The removed mass satisfies

```text
int(1-Gamma) dnu_R^* <= C(L+1) epsilon^(1/16),
```

by invariance and a union bound. This is an important point: no number of itinerary cells appears.

On derivative supports, the chain rule through `j` collisions gives the stated exponential bound

```text
||Gamma||_{C^3}, ||X_m||_{C^2}
 <= exp(C(L+1) log(C/epsilon)).
```

At a finite-itinerary or section-decision boundary, an earlier one-step factor is zero on a neighborhood on both sides. This is used to extend the piecewise derivatives by zero and obtain a global `C^3` source cutoff.

The logic is coherent. The global zero-extension statement is nevertheless load-bearing. The final paper should explicitly index the first singular or decision time and show that the corresponding factor remains identically zero on a two-sided neighborhood before differentiating later iterates. This would make clear that no derivative of a branch defined only on one side is being extended through the singularity.

The lower bound on `B_m` used for quotient derivatives is deliberately coarse but sufficient. Since every positive one-step matrix entry is bounded below by a fixed constant that may be less than one, an exponential lower bound is enough, and the resulting reciprocal loss is already absorbed into the exponential derivative budget.

## 8. Audit of the exact geometric extraction

### 8.1. Bounded-variation marks

For a fixed number of return-state marks, the manuscript smooths the zero extensions before composing them with the actual return orbit. The telescoping `L^1` error is

```text
C_q epsilon V,
```

where `V` is the sum of the BV norm of one mark times the sup norms of the others. This avoids assuming a BV bound for a long dynamical pullback.

The residual is defined directly on the source space by

```text
Q = (J_{n,R})_*
    (1_{N_{n,R}<=L} Gamma_{L,R,epsilon} w_epsilon nu_R^*),
E = mu_{n,R}^{w,L}-Q.
```

The exact variation estimate is

```text
||E||_TV <= C_q{epsilon V+M(L+1)epsilon^(1/16)}.
```

For the unweighted law, both `E` and `Q` are positive. For complex marks the exact signed decomposition and variation estimates remain valid.

### 8.2. Source-side integrations by parts

The initial section is partitioned by regular collision itinerary, all section decisions, the actual collision time `m=N_{n,R}`, and the output lattice label. On each source piece, the time coordinate is `L_m` and the smoothed source density extends by zero with two derivatives.

Because `X_m L_m=1`, two integrations by parts identify the first and second distributional derivatives of the pushed-forward time density with pushforwards of

```text
div(b_D X_m),
div(X_m div(b_D X_m)).
```

The source pieces have disjoint interiors. Summing the absolute source integrals over all pieces and all output labels therefore pays the area of the initial collision cylinder rather than the number of words. This yields

```text
sum_ell ||partial_t^2 q_epsilon(ell,.)||_1
 <= C_q M exp(C_q(L+1)log(C_q/epsilon)).
```

This is the strongest new theorem in the revision. It directly resolves the previous absence of a long-time all-label derivative budget, albeit for a new exact residual rather than the inherited power--logarithm residual.

I found the source-summation principle correct. It is exactly the right way to avoid a hidden symbolic multiplicity. The proof would benefit from a displayed measure-theoretic partition lemma specifying that boundaries are null, all zero extensions have the required Sobolev regularity, and the union of the interiors accounts for the source almost everywhere. These are standard but important facts in a discontinuous billiard system.

## 9. Audit of microscopic finite-band inversion

### 9.1. Far-roof estimate

The all-label `W^{2,1}` budget gives

```text
|Q_hat(u,b)| <= A_2/|b|^2.
```

After integration over the three-frequency torus, this yields a density tail `A_2/(pi B)`. Multiplication by the interval transform

```text
|H_I(b)| <= min{|I|,2/|b|}
```

improves the interval-probability tail to `A_2/(pi B^2)`. The constants and powers are consistent with the manuscript's Fourier convention.

### 9.2. Replacing the residual by the full law

If `delta` is the total-variation difference between the full law and the geometric residual, replacing the residual by the full law inside the finite interval integral costs

```text
C delta [1+log(1+B|I|)],
```

not `C delta B`. The logarithm follows from integrating `min{|I|,2/|b|}`. This observation is essential: a linear factor in `B` would make the subsequent choice of bandwidth unusable.

The resulting exact error bound is sound. With

```text
L_n = ceil(lambda n),
epsilon_n = epsilon_0 n^(-d),
B_n = n^(P+4) A_n,
```

and `lambda>a/c`, one obtains

```text
log B_n = O(n log n)
```

and an arbitrarily small inverse-polynomial absolute error after multiplication by `n^2`, uniformly at all three singleton lattice labels and bounded or shrinking roof intervals.

This is a meaningful microscopic theorem. It should not be described as merely another window estimate.

### 9.3. What the theorem does not do

The finite integral is the transform of the full actual law, but it is not asymptotically evaluated. The previously proved central, annular, compact, and peripheral estimates do not cover the entire interval up to `B_n`. In particular, `log B_n=O(n log n)` means that the bandwidth itself can be of order `exp(C n log n)`, not of order `n log n`.

The abstract phrase “a roof bandwidth of logarithmic size `O(n log n)`” should be replaced everywhere by the unambiguous statement “a roof bandwidth whose logarithm is `O(n log n)`.” The theorem and response use the latter meaning; the presentation should not invite the former reading.

The sentence in the far-roof proof saying that bounded-frequency transform control makes absolute inversion legitimate should also be expanded by one line: local boundedness near `b=0` together with the `|b|^{-2}` tail gives integrability on the full roof-frequency line.

## 10. The common pointwise correction

Revision 31 substitutes the new exact extraction into the intrinsic signed correction and obtains the ledger

```text
R_chi
 = e_epsilon-K_chi*E_epsilon
   + finite_complementary_inverse(Q_epsilon)
   + far_roof_inverse(Q_epsilon).
```

Two terms are quantitatively controlled:

- `K_chi*E_epsilon` by the total variation of `E_epsilon` and the kernel supremum;
- the far-roof inverse by the explicit second-derivative budget and `1/B`.

Two terms are not controlled in the norm required for the raw LLT:

- `e_epsilon` has small `L^1` norm but no small essential supremum;
- the finite complementary inverse is not bounded throughout all remaining frequency regimes.

The manuscript correctly emphasizes that a positive density of small total mass may be tall on a very small set. The Chebyshev estimate for its level sets does not imply an essential-supremum bound on a prescribed central window. The two uncontrolled terms may also require signed cancellation, so bounding them independently by absolute values may be unnecessarily strong or impossible.

This is the decisive mathematical boundary of revision 31. The new extraction controls the far-roof geometry, but it does not close the pointwise common correction.

## 11. What revision 31 closes, advances, and leaves open

The status relative to the revision-30 report is as follows.

| Obligation from revision 30 | Revision-31 status |
|---|---|
| Long-time inverse-coarea / second-derivative budget at linear collision cutoff | **Closed for the new geometric residual.** The bound is explicit and summed over all labels without a word-count loss. |
| Far-roof truncation at singleton lattice labels and bounded roof intervals | **Closed as an exact finite-band reduction.** Arbitrary inverse-polynomial absolute accuracy is available. |
| Complete prescribed-return complementary Fourier integral | **Open.** The finite integral up to `B_n` is not evaluated on all remaining regimes. |
| Pointwise common signed raw correction | **Open.** The extracted density is only `L^1`-small and the finite complementary inverse is uncontrolled. |
| Microscopic Gaussian denominator | **Open.** The finite-band formula supplies no Gaussian main term or positive local denominator. |
| Relative replacement of the original microscopic physical event | **Open.** The stationary bridge theorem remains mesoscopic. |
| Weighted raw theory for the final path-selector class | **Partially advanced.** Structural extraction allows a fixed product of BV return marks, but inherited Fourier estimates are not thereby multiple-mark or arbitrary physical-time selector theorems. |

This table should remain visible in any future submission. It is more informative than counting the number of completed modules.

## 12. Significance at the requested benchmark

Revision 31 strengthens the paper materially. The uniform transverse-field idea and source-side all-itinerary derivative summation are elegant. They may be useful beyond the immediate manuscript, especially if formulated as a general geometric regularization principle for finite-horizon dispersing billiards with piecewise smooth sections and marked return records.

In the present article, however, the result is still tied to the triangular one-parameter family, its exact action identity, its finite candidate geometry, and the particular raw inversion architecture. The new theorem is an enabling theorem for the original LLT rather than a completed theorem of comparable breadth.

The article now contains substantial unconditional results that could form one or more strong specialist papers:

- uniform Gaussian and functional limits for the actual record;
- joint nondegeneracy and quantitative phase arithmetic;
- unsmoothed mesoscopic denominators and stationary physical conditioning;
- Gaussian bridge limits under exact shrinking physical windows;
- the new all-itinerary geometric regularization and microscopic finite-band reduction.

But the current title, abstract, theorem architecture, and final application continue to make the raw mixed-density LLT the principal endpoint. At the top-four level, leaving the finite complement and pointwise correction open is not a secondary technical omission. It is the principal local-inversion theorem.

A specialist-journal submission organized around the unconditional results, after independent expert verification, would be a different editorial proposition and could be compelling. That possibility does not justify acceptance at the requested four-journal benchmark in the present form.

## 13. Required mathematical changes before a future top-four resubmission

A future top-four submission should not return until the following chain is closed.

1. **Evaluate the actual finite complementary integral.** Prove bounds covering the balanced, compact nonzero, peripheral, and growing-roof regimes for the full prescribed-return transform, with constants compatible with the bandwidth chosen from the geometric derivative budget. An alternative theorem exploiting cancellation in the exact raw ledger would also be acceptable, but it must produce the required local norm.

2. **Control the pointwise common correction.** Either prove a small essential-supremum estimate for the total signed correction on central microscopic windows, or establish an equivalent local inversion theorem that preserves and quantitatively exploits cancellation between `e_epsilon` and the finite complementary inverse.

3. **Derive the microscopic Gaussian denominator.** The singleton-lattice and bounded-time-interval probability must be shown to have the Gaussian main term with uniform error. A finite-band identity alone does not establish positivity or asymptotics.

4. **Transfer to the original microscopic physical event.** Prove the relative symmetric-difference or equivalent coupling estimate at the exact microscopic conditioning resolution, under the stationary physical law relevant to the final theorem.

5. **Close the weighted class.** Verify the raw Fourier and correction estimates for the actual weighted indicators or path selectors used in the downstream conditioned physical theorem. A fixed-product structural extraction and a one-mark central theorem do not automatically supply this.

6. **Give the new geometry an independent specialist audit.** The one-collision coordinate conversion, all-candidate tangency guard, uniform polynomial coefficient bound, global zero extension, and disjoint-source derivative summation should be checked by an independent billiards expert.

## 14. Presentation changes

Even before the final closure, the following revisions would materially improve the manuscript.

1. Replace every ambiguous description of the new bandwidth by “`log B_n=O(n log n)`.”
2. Put the derivative matrix, coordinate conversion, determinant, and action identity in one self-contained proof block.
3. Expand the all-candidate first-hit-transition lemma and the compactness argument for the polynomial coefficient lower bound.
4. State a formal partition-and-zero-extension lemma for the source pieces used in the two integrations by parts.
5. Separate in the introductory theorem list the unconditional headline theorems from reductions and conditional interfaces. Theorem V is a theorem, but it is a reduction rather than the raw LLT.
6. Reduce repeated scope disclaimers by consolidating them into one dependency diagram and one final status table. The present 197-page architecture is difficult to audit even though the individual disclaimers are accurate.
7. Expand the comparison with existing local-limit and billiard-flow literature around the actual completed theorems, rather than primarily around the still-open endpoint.

## 15. Verification limitations

The successful exact-source workflows show that the reviewed source builds and that the declared finite diagnostics run on the reviewed SHA. They also support the source-preservation claims.

They do not establish:

- the continuum completeness of the candidate singularity list;
- the global smoothness of every zero extension;
- the absence of hidden boundary distributions in the source integrations by parts;
- the complementary spectral estimates to the new bandwidth;
- a pointwise raw remainder bound;
- the microscopic Gaussian denominator;
- the full raw mixed-density LLT.

No independent human specialist review is claimed by the author, and this report should not be represented as one.

## 16. Final assessment

Revision 31 should be recognized as a substantial mathematical advance. It resolves the long-time derivative-budget obstruction for a new exact residual and reaches genuine singleton-lattice finite-band inversion. Those achievements materially narrow the gap to the original local theorem.

They do not eliminate that gap. The finite complementary integral, pointwise common correction, microscopic Gaussian denominator, microscopic physical-event replacement, and final weighted theory remain open. These are precisely the steps that convert a reduction into the advertised raw local limit theorem.

For that reason my recommendation at the requested four-journal benchmark remains:

**reject in the present form.**

A future assessment could change substantially if the exact raw ledger is closed in the required pointwise norm and the resulting microscopic physical conditioning theorem is proved for the original record.