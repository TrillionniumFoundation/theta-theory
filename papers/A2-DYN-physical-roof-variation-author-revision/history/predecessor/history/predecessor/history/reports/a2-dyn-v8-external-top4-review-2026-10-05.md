# External top-four referee report on A2-DYN revision 8

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v8-referee-response-2026-10-05`, `revision/a2-dyn-v8-referee-copy-2026-10-05`  
**Reviewed commit:** `36427a184ea256f0336fbc431dc76110a9b14592`  
**Reviewed repository tree:** `4531d7d44db3f2e7824b957f17fbe2c6fbdd6e5f`  
**Active manuscript directory:** `papers/A2-DYN-v8-referee-response`  
**Active core tree:** `a6dd990d54b5db1efa3c81c29779356dcd4ffe6f`  
**Immediate author parent:** `52278437b6313f1ad5eb53dd95c306f2651f30cb`  
**Controlling earlier report:** `reviews/a2-dyn-v4-external-top4-review-2026-10-05/REFEREE_REPORT.md`  
**Date:** 5 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards-specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 8 is a genuine mathematical revision. It is not a relabeling of the previously reviewed source. In particular, it proves a useful cumulative return-time tail for the actual deterministic first-return process, derives a linear physical-count truncation budget on exponentially expanding finite Fourier bands, constructs the genuine first-return operators on a common collision probability space, proves the exact damped renewal and Schur-complement identities, and obtains a fixed complex neighborhood of holomorphic `L^p -> L^q` block operators with strong continuity in the disk radius. The intervening revision also supplies a conditioned logarithmic maximal-block estimate that closes the earlier square-root unfinished-return objection for conditioning events of polynomially small probability.

I found no decisive counterexample in the new arguments audited below. The cumulative-count proof correctly avoids any independence assumption, and the renewal formulas use the chronological order of the actual collision dynamics. The manuscript is also unusually explicit about what these results do not prove.

The negative recommendation is therefore not a claim that revision 8 is mathematically vacuous or that its new theorems are false. It is based on the fact that the paper continues to identify its endpoint as a parameter-uniform raw mixed-density local limit theorem, while the three central analytical bridges to that endpoint remain hypotheses or criteria rather than established results:

1. an anisotropic realization of the unbounded induced twists together with phase reconstruction, Fredholm control, and quantitative high-frequency resolvent estimates;
2. uniform summability of correlations, continuity and uniform nondegeneracy of the Green--Kubo covariance, and a cohomology theorem whose transfer functions may legitimately be evaluated on the selected periodic orbits;
3. a complete critical/singular branch decomposition with a uniformly integrable raw residual, including quantitative growth constants sufficient for the required frequency splice.

The exact residual-inversion theorem in the manuscript remains conditional on these inputs. Thus the motivating raw LLT, its weighted inserted versions, and the final conditioned physical-time consequences are still not unconditional theorems of the article. At the requested benchmark, the newly completed return-tail and renewal infrastructure does not compensate for the continued absence of the central probabilistic theorem or of a comparably broad new general principle.

## 2. Frozen source, chronology, and reproducibility

Both named revision-8 branches resolve to the same commit,

`36427a184ea256f0336fbc431dc76110a9b14592`.

The revision preserves the nineteen mathematical core files of the v6/v7 source and adds precisely two new mathematical files:

- `core/20_cumulative_returns.tex`;
- `core/21_common_renewal.tex`.

The source manifest records the preserved hashes, the earlier mathematical baseline, the controlling review, and the fact that neither the full raw LLT nor independent human review is claimed. This makes the chronology materially clearer than the earlier v4/v5 branch alias.

The exact-source GitHub workflow attached to the reviewed SHA completed successfully. According to the author-side validation, the complete article typesets to 49 pages, all references resolve, the preservation audit passes, and the finite renewal/counting diagnostics pass in normal and optimized Python modes. These facts establish source identity and reproducibility of the finite checks. They do not establish the continuum theorems or replace mathematical review.

The present review branch starts directly from the reviewed author SHA and adds this report only under

`reviews/a2-dyn-v8-external-top4-review-2026-10-05/`.

No manuscript file, author branch, prior report, workflow, or unrelated repository path is modified by the review.

## 3. Mathematical package after revision 8

The paper studies a triangular finite-horizon periodic Lorentz gas for disk radii

\[
R\in[0.45,0.47],
\]

and records, for actual first returns to a physical section, a joint variable consisting of planar lattice displacement, physical collision count, and flight time. The reference measure is counting measure in the three lattice coordinates and Lebesgue measure in the time coordinate. This mixed nature is essential to the raw-density problem.

The unconditional package now contains the following substantial components.

- A concrete physical periodic-orbit family, exact record matrices, a trivial joint periodic annihilator, and quantitative phase separation from logarithmic-length periods.
- A positive-measure one-step coercivity estimate for locally Hölder circle-valued phases satisfying explicit regularity bounds.
- Exact critical-edge coefficients for selected physical words, exact subtraction of a genuine jump, and a local inversion principle that allows extracted edge mass provided its density is negligible on the diffusive central window.
- Fixed-return moving-domain continuity, common regular submersion patches, exact Kac normalizations, and uniform first-order physical-clock statements.
- Collision-space soft killing and exponential tails for a genuine return block.
- A maximal-block estimate implying an `o_P(sqrt(t))` unfinished-block error even under conditioning of polynomially small probability.
- The new cumulative tail
  \[
  \nu_R^*\{N_{n,R}>L\}\le A\exp(an-cL),
  \]
  fixed-strip exponential moments of the complete record, and a linear physical-count truncation budget on exponentially growing finite bands.
- The new exact first-return renewal realization on the common collision space, its Schur formula, exact physical record pairings, and holomorphic `L^p -> L^q` block operators with strong radius continuity.

The manuscript does **not** yet prove the following.

- A quasi-compact anisotropic family for the actual unbounded induced observables.
- Reconstruction of a regular nonvanishing phase from approximate spectral vectors, or the associated quantitative large-frequency resolvent estimate.
- A uniform perturbative leading eigenvalue expansion for the actual induced family that yields the asserted four-dimensional covariance.
- Uniform summability of the Green--Kubo series and a periodic-evaluable zero-variance cohomology theorem.
- A classification and uniform summation of all critical words, singular itinerary boundaries, and central residual branches.
- The raw mixed-density LLT stated in the residual-inversion theorem.
- The weighted raw-density estimates needed to replace an exact physical conditioning event by a completed-block event.

This distinction is accurately stated in revision 8. It is also the decisive editorial distinction.

## 4. Audit of the cumulative return-tail theorem

Theorem `thm:cumulative-return-tail` is the cleanest new result. Write `N_{n,R}` for the physical collision time of the `n`th actual return. For a trajectory starting in the section, the event `N_{n,R}>L` is exactly the event that fewer than `n` section visits occur during the first `L` collisions. Since the fixed smooth killing weight satisfies

\[
0\le \chi\le \mathbf 1_{Y_R^*},
\]

that event implies

\[
\sum_{j=1}^{L}\chi(T_R^j x)\le n-1.
\]

The pointwise exponential domination used in the manuscript follows immediately. Integrating, enlarging the domain from the section to the collision space, shifting by invariance, and applying the previously established soft-killing estimate gives

\[
\nu_R^*\{N_{n,R}>L\}\le A e^{an-cL}.
\]

This is a valid single-orbit counting argument. It does not multiply return probabilities, assert mixing of successive blocks, or import an independent-renewal surrogate.

The passage from the tail to fixed-strip exponential moments is also sound. Applying the layer-cake identity to

\[
X=(N_{n,R}-vn)_+
\]

gives a bound uniform in `n` and `R`, and the deterministic domination of the complete record by the physical collision count transfers the estimate to all four recorded coordinates.

The weighted finite-band truncation proposition is a legitimate consequence. Total variation contracts under pushforward, while derivatives of the characteristic function insert polynomial factors bounded by powers of `N_{n,R}`. Tail integration therefore gives

\[
C_{d,\gamma}(1+L)^{d+|\gamma|}e^{an-cL}.
\]

Solving this inequality yields a cutoff of order

\[
n+\log(V/\varepsilon),
\]

rather than the earlier `n log(V/epsilon)` budget. In particular, exponential growth of the finite frequency-band volume still permits a collision cutoff linear in `n`.

This is useful progress, but its scope must not be overstated. The result is a coarse upper tail for the cumulative physical count, not a centered large-deviation theorem. More importantly, deleting high-count trajectories in total variation does not estimate the variation of inverse coarea Jacobians, the density near critical values, the number and geometry of singular branch boundaries, or the second-derivative norms of the residual densities. It improves a truncation step inside a future proof; it does not prove the raw Fourier-tail estimate itself.

I therefore regard Theorem `thm:cumulative-return-tail` and Proposition `prop:linear-count-budget` as correct and useful enabling results, but not as closure of the principal LLT obstruction.

## 5. Audit of the exact renewal realization

Theorem `thm:common-renewal` places the collision dynamics on the common probability space

\[
M=\mathbb T\times(-1,1),\qquad d\nu=(4\pi)^{-1}d\alpha\,dp,
\]

uses the hard section projection `P_R`, and defines the real-frequency weighted collision operator by backward composition with the invertible billiard map. On `L^1`, this operator is an isometry. The first-return terms

\[
\mathcal R_{m,R,\omega}
 =P_R\mathcal A_{R,\omega}
   (Q_R^\perp\mathcal A_{R,\omega})^{m-1}P_R
\]

have the correct chronological order: the initial and terminal states lie in the section, and the intervening collision states lie outside it. Their initial domains are exactly the first-return sets `{r_R^*=m}`. Invertibility of the induced map makes the corresponding image domains a partition as well.

Consequently, for `|z|<1`, the series converges in operator norm, while on `|z|=1` it converges strongly for each input. The manuscript correctly does not claim operator-norm convergence on the boundary. The renewal equation obtained by partitioning a section-to-section collision trajectory according to its first return yields

\[
P_R(I-z\mathcal A_{R,\omega})^{-1}P_R
   =(I-\mathcal R_R(z,\omega))^{-1}
\]

on the section subspace, and the displayed Schur-complement formula is consistent with the same decomposition. Iteration gives the actual `n`-return record pairing; no independence enters.

The construction is valuable because it removes an ambiguity that affected earlier versions: the operator is now visibly the operator of the true physical induced process, not an abstract block model. It also supplies a precise compatibility target for any later anisotropic construction.

The second theorem in the section defines the `n`-block operator directly and proves holomorphy from the cumulative exponential moment. For `q<p`, Hölder's inequality with

\[
1/q=1/p+1/t
\]

produces the stated `L^p -> L^q` bound on a fixed complex tube. Polynomial insertions from derivatives are absorbed by a slightly larger exponential weight, giving operator-norm holomorphy on compact subsets. The strong radius-continuity argument for fixed `n` is plausible and, in its stated scope, coherent: remove the relevant finite collision singularities and moving section boundaries, stabilize the finite backward itinerary, prove pointwise convergence for bounded continuous inputs, use an exponent with slack for uniform integrability, and then pass to general inputs by density. The separate treatment of `p=infinity` avoids the false assertion that smooth functions are norm dense in `L^infinity`.

Several limitations are correctly acknowledged and are editorially decisive.

1. These are block operators from `L^p` to the weaker space `L^q`; outside the damped region they are not iterates of one bounded endomorphism on a fixed space.
2. At real frequencies the `L^1` induced operator is isometric, so its existence gives no spectral gap, contraction, or Dolgopyat estimate.
3. Strong continuity for each input and fixed `n` is not operator-norm continuity in `R`, and no estimate uniform in long time follows from it.
4. The construction does not show that the hard section projection is bounded on the anisotropic distribution space ultimately needed for spectral analysis.
5. Holomorphic continuation of inserted pairings across the damping boundary is not a meromorphic resolvent theorem and does not provide the leading eigenvalue expansion required near zero frequency.

For exposition, the phrase that the first three complex frequencies are “interpreted modulo `2pi`” should be replaced by a precise local complexification or universal-cover formulation. A globally holomorphic complex torus is not being constructed here. This is a correctable presentation issue, not a fatal flaw in the estimates.

I regard the exact renewal theorem as a sound identification theorem and the common-scale theorem as a useful integrability result. Neither is the missing anisotropic spectral theorem.

## 6. Collision-space input, common charts, and conditioned clocks

Revision 8 inherits several v6 results that were not present in the previously reviewed v4 source. They materially improve the paper and should be credited separately.

### 6.1 Soft killing and return tails

The manuscript invokes the Demers--Zhang perturbation framework for finite-horizon Lorentz maps to obtain local common collision spaces, a uniform spectral splitting, and bounded multiplication by a smooth function. A smooth weight supported strictly inside the section then gives an exponentially decaying avoidance functional. This is used only for a scalar collision-space estimate, not as an unjustified anisotropic realization of the discontinuous induced observable.

The logic of the soft-killing perturbation is standard and plausible: analytic perturbation of the simple eigenvalue at one, a uniformly negative derivative determined by the mean of the killing weight, and a uniform complementary power bound imply exponential decay at a fixed small positive weight. The subsequent comparison with actual section avoidance correctly yields exponential tails for a single genuine return block.

This is nevertheless a load-bearing import. A final version should map the geometric family and every chosen coordinate change explicitly to the precise hypotheses and norms of the cited perturbation theorems. In particular, the common-space identification, boundary-length reparametrization, deck-invariant reduction, and multiplier estimate should receive a specialist check. I found the present argument credible, but it is compressed relative to its importance.

### 6.2 Common moving-domain charts

The common-submersion lemma is elementary and correctly handles the zero extension because the cutoff is supported away from the moving chart boundary. The finite-patch proposition first truncates large physical counts, removes finite singular and critical sets, takes a compact subset of almost full mass, and covers it by finitely many regular patches stable under nearby radius changes. This produces fixed-return `L^1` continuity with an explicit small remainder.

The result is an improvement over the compressed moving-domain discussion in the earlier revision. Its constants are deliberately not uniform in `n` or in the inverse error tolerance. It therefore supplies finite-record continuity, not the quantitative long-time perturbation theory required for the LLT.

### 6.3 Conditioned maximal unfinished blocks

The marked-visit intensity formula in the suspension correctly distinguishes the stationary length-biased initial block from blocks launched by later section visits. Combining this intensity with the genuine return-block exponential moment gives

\[
\mu_R\{\mathcal M_R(t)>q\}\le C(1+t)e^{-aq}.
\]

Division by the conditioning probability is legitimate for an arbitrary positive-probability event, without an independence assumption. For polynomially small conditioning probabilities, the maximum block is logarithmic and hence `o_P(sqrt(t))`. The path-comparison estimate then controls all unfinished prefixes and suffixes uniformly over the observation interval.

This closes the specific unfinished-block objection in the earlier report. It does **not** prove a functional Gaussian theorem for the completed induced record, nor does it justify replacing one exact lattice conditioning event by another. The manuscript explicitly notes that the symmetric-difference probability must be small relative to the conditioning probability. That remaining boundary comparison requires the weighted local-density theorem that is still open.

## 7. The unresolved anisotropic operator and phase-reconstruction problem

The paper's quantitative periodic geometry and one-step coercivity theorem are potentially useful high-frequency inputs. They show that any sufficiently regular circle-valued phase with controlled Hölder norm has a polynomially detectable one-step defect on a set of positive measure.

Theorem `thm:phase-resolvent-criterion`, however, is a criterion rather than an application. It assumes all of the following for the actual high-frequency induced operator:

- a Banach space on which the operator is bounded;
- Fredholm index zero for `z-\mathcal L` on the unit circle;
- reconstruction from every approximate spectral vector of a nonvanishing circle-valued phase;
- quantitative local Hölder control of that phase;
- an estimate converting approximate spectral error into the physical phase defect.

None of these statements is proved for the actual unbounded induced record. The new `L^p -> L^q` construction does not supply them. In particular, an approximate spectral vector in an anisotropic distribution space need not have a pointwise modulus or a regular phase without a separate regularization and nonvanishing theorem.

This is not a technical footnote. It is the precise bridge from selected periodic phase discrepancies to a uniform compact-frequency or large-roof-frequency operator estimate. Until it is proved, the polynomial phase lower bounds cannot be inserted into the frequency splice of the raw LLT.

A future top-four resubmission would need to construct the actual anisotropic induced family, prove compatibility with the exact physical renewal pairing, establish its Fredholm/quasi-compact structure, and derive the reconstruction estimate with constants strong enough to satisfy the final splice inequalities. Stating this chain as a theorem with unverified hypotheses is useful bookkeeping, but it does not discharge the chain.

## 8. The unresolved covariance and cohomology problem

Finite-record exponential moments and moving-domain continuity imply continuity of every fixed-lag moment and covariance. They do not imply uniform summability of the infinite correlation series.

Proposition `prop:covariance-closure` assumes the uniform tail condition

\[
\lim_{m\to\infty}\sup_R\sum_{k>m}
 \left\|\int g_R\otimes(g_R\circ(F_R^*)^k)\,d\nu_R^*\right\|=0.
\]

It also assumes that zero asymptotic variance yields a coboundary whose transfer function has a representative on which the identity telescopes along the selected periodic orbits. Given those hypotheses, continuity and uniform positive definiteness of the covariance follow. The proof of that conditional implication is reasonable.

The hypotheses themselves remain unproved. The common `L^p -> L^q` holomorphy theorem is not a perturbative spectral theorem on one space and therefore does not yield a Green--Kubo expansion, exponential decay for the induced unbounded observable, or differentiability of a leading eigenvalue. Likewise, a merely measurable Livšic identity cannot automatically be evaluated at singular billiard periodic points.

This low-frequency issue is as central as the high-frequency issue. The Gaussian in the claimed LLT has no established uniform covariance matrix until correlation summability and zero-variance rigidity are proved for the actual induced family.

## 9. The unresolved all-branch raw residual problem

The paper correctly identifies and subtracts an explicit jump from selected regular critical words. It also gives a useful abstract lemma: if the residual densities `q_w` satisfy

\[
\sum_w\|q_w\|_1<\infty,
\qquad
\sum_w\|D^2q_w\|_{TV}<\infty,
\]

then their aggregate transform is integrable with a quantitative outer-frequency tail.

The manuscript does not prove these sums for the full physical measure. The missing decomposition must include:

- every regular critical word, with its exact extracted edge;
- singular itinerary boundaries and competing-root transitions;
- central and noncritical branches;
- the actual multiplicity of physical words;
- parameter-uniform inverse-Jacobian and derivative estimates;
- the dependence of all constants on the return count `n`.

An exponential bound for an individual edge coefficient cannot be multiplied by an uncontrolled symbolic word count. Conversely, a total-variation deletion of all trajectories with `N_{n,R}>L` does not control the second derivative of the density on the surviving branches. The new linear count cutoff is therefore compatible with, but not a substitute for, the all-branch estimate.

The residual-inversion theorem also requires the extracted edge measure to have negligible total variation at the `n^{-2}` scale and negligible density on the central diffusive window, together with an `L^1` residual tail outside the major arc. These conditions remain interfaces. The displayed frequency-splice lemma rightly warns that one must verify an actual strict interval for the splice parameter using the true derivative-growth constants; formal choices of “small” and “large” parameters do not suffice.

Until the full branch sum and its growth rates are established, the raw mixed-density LLT is not proved.

## 10. Relation between the declared endpoint and the proved theorems

The manuscript repeatedly and correctly says that the full raw LLT is not yet established. This honesty is preferable to an overclaim. It creates, however, a structural problem for the article at the requested venue.

The title, introduction, residual-inversion theorem, and final realization section continue to make the raw local limit the organizing endpoint. Much of the article then consists of exact physical modules and conditional closure criteria surrounding that endpoint. Revision 8 closes several genuine modules but leaves the central spectral, covariance, and residual estimates open.

At a specialist level, the combination of explicit periodic arithmetic, physical edge singularities, moving-domain continuity, conditioned clock control, and exact renewal identification may form a substantial paper. At the four-journal benchmark requested here, one normally expects either the completed probabilistic theorem or a new general mechanism whose importance does not depend on that theorem. The new cumulative tail is an elegant consequence of soft killing, and the renewal identity is an exact and useful physical realization, but neither is by itself such a general mechanism.

The editorial assessment therefore remains negative even though the mathematical assessment of the new material is positive.

## 11. Required work for a future top-four resubmission

A future manuscript seeking the stated benchmark should, in my view, complete the following chain rather than add further conditional interfaces around it.

### A. Actual anisotropic induced operator

Construct a Banach-space realization of the true four-coordinate induced twists that is compatible with the exact renewal pairing of revision 8. Prove boundedness, quasi-compactness or the necessary Fredholm alternative, perturbation control near zero frequency, and large-frequency estimates. Establish the phase-reconstruction theorem for approximate spectral vectors, including nonvanishing and quantitative regularity, rather than assuming it.

### B. Low-frequency spectral and covariance theorem

Derive the leading eigenvalue expansion with a uniform cubic remainder. Prove uniform correlation summability for the unbounded induced record, continuity of the full Green--Kubo matrix, and a zero-variance cohomology theorem whose representative can be evaluated on the selected periodic family. Deduce a uniform positive lower covariance bound from the real-rank periods.

### C. Complete raw branch decomposition

Classify and subtract all nonintegrable critical edges and singular boundary contributions. Prove quantitative uniform bounds for the aggregate residual, including the actual `n`-dependence of the `L^1` and second-derivative sums. Verify the strict frequency-splice inequalities with those constants.

### D. Unconditional raw and weighted local limits

Insert A--C into the residual-inversion theorem and state the resulting raw mixed-density LLT as an unconditional principal theorem. Prove the weighted versions needed for conditioning, and quantify the symmetric difference between exact physical observations and completed-block observations relative to the local conditioning probability.

### E. Dynamics-specific independent proof review

The collision-space perturbation input, explicit periodic action, moving-return-domain coarea analysis, induced anisotropic construction, and global branch sum should be checked by an independent specialist in dispersing billiards. Source audits and finite rational diagnostics are useful but cannot substitute for this review.

## 12. Expository and technical comments

1. **Separate the unconditional theorem package from closure criteria at the beginning.** The abstract is accurate, but a single theorem-level synopsis would make it immediately clear which conclusions are proved and which are hypotheses of the final inversion interface.

2. **Clarify the complex-frequency domain.** Replace the statement that complexified torus frequencies are interpreted modulo `2pi` with a local chart or universal-cover formulation.

3. **Add an explicit compatibility diagram.** The collision operator, damped renewal operator, direct `n`-block `L^p -> L^q` operator, and proposed anisotropic induced operator should be connected by precise intertwining or pairing statements.

4. **Keep fixed-`n` continuity distinct from long-time uniformity.** The common-chart and strong operator-continuity theorems are fixed-record statements. Their constants are not uniform in `n`; this should remain visible whenever they are cited later.

5. **Reduce notation collisions.** The record-size variable `Q_R` and the complementary projection `Q_R^perp` are distinguishable but unnecessarily close in a technically dense section.

6. **State normalization constants at the renewal theorem.** The role of `c_*`, the section mass, and the normalized measure `nu_R^*` should be recalled locally before the exact pairing.

7. **Position the renewal identity in the literature.** The novelty is its exact implementation for this physical record and moving family, not the abstract renewal algebra. The exposition should make that distinction explicit.

8. **Avoid letting audit prose dominate theorem flow.** Version identity, preservation manifests, and validation limitations belong in supporting material. The main article should read as a mathematical argument rather than a sequence of responses to repository history.

9. **Do not infer density regularity from count truncation.** Revision 8 itself avoids this mistake; later revisions should preserve the separation between total-variation trajectory deletion and branchwise density-derivative estimates.

10. **Keep the conditioned-clock boundary explicit.** The maximal unfinished-block theorem permits comparison under the same conditioning event. Changing the exact event remains a weighted local-density problem.

## 13. Verification limits

I reviewed the source-pinned revision, the two new mathematical sections, their dependency on the collision-space killing estimate, the common-chart and conditioned-clock additions inherited from v6, the operator and covariance criteria, the raw residual criterion, and the final realization statement. I also checked the chronology of the prior report and the successful exact-source workflow associated with the reviewed SHA.

I did not treat the author's finite diagnostics as proof of continuum billiard statements. I did not independently rederive every geometric certificate in the nineteen preserved files, which were already the subject of the earlier source-pinned review, nor did I contact an independent human billiards specialist. This report is therefore a mathematical referee-style assessment with explicit source provenance, not a proof certification.

## 14. Final assessment

Revision 8 materially improves A2-DYN. The cumulative return tail, exact physical renewal realization, fixed-strip record moments, linear finite-band count budget, common-scale holomorphy, and conditioned square-root unfinished-block control are genuine achievements. On the arguments audited, I found no fatal mathematical error in these additions.

Nevertheless, the revision still proves neither the paper's declared raw mixed-density LLT nor the full conditioned physical-time theorem. The unresolved anisotropic phase reconstruction, covariance/cohomology closure, and all-branch raw residual sum are exactly the central analytical content needed to pass from the present modules to the claimed endpoint. They cannot be regarded as routine cleanup.

**I therefore do not recommend publication in *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or the *Journal of the AMS* in the present form. A future assessment could change substantially if the complete operator/covariance/residual chain is proved and the unconditional raw LLT is obtained.**
