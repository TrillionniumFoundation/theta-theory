# External top-four referee report on A2-DYN revision 9

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v9-referee-response-2026-10-05`, `revision/a2-dyn-v9-referee-copy-2026-10-05`  
**Reviewed commit:** `872f8695670373a3ca67ff84841a1ea38ed64227`  
**Reviewed repository tree:** `d9fa9aa0cca276da6caa596a013ef6701533aa2a`  
**Active manuscript directory:** `papers/A2-DYN-v9-referee-response`  
**Active core tree:** `c38e24f02fae423f231ccfa1389751abd8a51789`  
**Immediate author parent:** `a63f437f37f9a210734d2c607885645250630739`  
**Controlling earlier report:** `reviews/a2-dyn-v8-external-top4-review-2026-10-05/REFEREE_REPORT.md`  
**Controlling report commit:** `9d1904397400529aae4a5d3cccede9081b4dfb33`  
**Date:** 5 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards-specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 9 is a substantial and mathematically genuine revision. It closes an important part of the objection made in the preceding report. The manuscript now proves, for the actual deterministic first-return record and uniformly over the radius interval, a continuous collision Green--Kubo covariance, a quantitative central characteristic-function estimate, a Gaussian weak limit, a characterization of the Gaussian kernel by an actual `L^2` coboundary, a functional central limit theorem for the return process, and an unconditioned stationary physical-time functional limit for displacement and collision count. These are not obtained by replacing the billiard by independent excursions, and they are not merely conditional operator statements.

I found no decisive counterexample in the three new proof sections audited below. The bounded collision compensation is an effective idea: it converts the unbounded induced record into a bounded collision observable, and the exact stopping identity then returns to the true induced process. The smoothing exponents, stopping window, covariance normalization, and random-time changes are internally coherent. The manuscript also continues to state its limitations with unusual care.

The negative recommendation is therefore not based on mathematical vacuity, a version alias, or a detected fatal error in the new Gaussian chain. It is based on the mismatch between the paper's continuing organizing endpoint and what is presently proved. The title and final synthesis retain the parameter-uniform raw mixed-density local limit theorem as the central problem. That theorem, its weighted inserted forms, and the exact-event conditioned physical-time consequences remain conditional on three load-bearing analytical bridges:

1. an actual anisotropic realization of the unbounded induced twists, together with Fredholm control, regular phase reconstruction, and quantitative complementary-frequency resolvent estimates;
2. regularity permitting the measurable zero-variance transfer function to be evaluated on the selected periodic orbits, and hence uniform positive definiteness of the four-dimensional covariance;
3. a complete critical/singular branch decomposition with quantitative, `n`-dependent residual derivative sums strong enough to close the strict frequency splice.

The new compact-rescaled-frequency Gaussian estimate does not replace an integrated Fourier-tail estimate. A positive semidefinite weak-limit covariance does not provide the nondegenerate density required by the raw local theorem. Initial-coordinate bounded variation does not control the second variation of all inverse-coarea densities. Consequently the central theorem suggested by the title remains unproved.

At a top-four benchmark, the new uniform Gaussian and functional-limit package is valuable but, in my judgment, not by itself a sufficiently broad or transformative replacement for the still-open raw LLT. The method is elegant and may be publishable in a strong specialist venue after independent expert checking and substantial reorganization. A future top-four submission would require either completion of the raw density and conditioning chain or extraction of a general compensation-and-stopping principle with applications substantially beyond this one triangular Lorentz family.

## 2. Frozen source and chronology

The two named revision-9 branches resolve to the same commit:

`872f8695670373a3ca67ff84841a1ea38ed64227`.

This is not an alias of revision 8. Relative to the reviewed revision-8 source, revision 9 adds three mathematical sections:

- `core/22_collision_covariance.tex`;
- `core/23_stopped_gaussian.tex`;
- `core/24_functional_gaussian.tex`.

It also makes documented expository changes to `07_realization.tex`, `13_uniform_physical_clock.tex`, `19_raw_closure_contracts.tex`, and `21_common_renewal.tex`. The twenty-one inherited mathematical core files remain included, and the source manifest records preservation of the inherited formal statement-and-proof environments, modulo the declared complementary-projection renaming.

The immediate parent `a63f437f37f9a210734d2c607885645250630739` is an explicitly labeled checkpoint containing the first two new derivations. The complete manuscript delivery is the reviewed child commit. The earlier revision-8 referee report is in the ancestry and is identified by path, commit, and blob in the response and source manifest. Version identity is therefore materially improved over the v4/v5 history.

The exact-source GitHub workflow for the reviewed revision completed successfully at the reviewed SHA. The local validation reports a 60-page native build, 24 unique core inclusions, 77 proof environments, 234 labels, preservation checks, and normal/optimized finite diagnostics. These facts qualify the source and build; they do not certify the continuum billiard arguments.

The present review branch starts from the reviewed author commit and adds only this report under

`reviews/a2-dyn-v9-external-top4-review-2026-10-05/`.

No manuscript source, author branch, previous review, workflow, or unrelated repository path is modified.

## 3. What revision 9 actually proves

The principal new construction is the bounded collision observable

\[
 h_R=f_R-\bar G_R\mathbf 1_{Y_R^*},
\]

where `f_R` is the one-collision four-coordinate record and `bar G_R` is the mean induced record. Although the first-return record is unbounded, `h_R` is bounded and centered on the collision space. For the physical time `N_{n,R}` of the `n`th return, the manuscript proves the exact identity

\[
 J_{n,R}-n\bar G_R=S_{N_{n,R}}h_R.
\]

This identity is the conceptual center of the revision. It permits the use of the established smooth collision-map spectral theory without asserting that the hard section projection or the unbounded induced twist acts on the same anisotropic space.

The new unconditional conclusions are:

- a uniform bounded-variation estimate for the one-collision observables and the moving section indicator;
- exponential correlation bounds for bounded BV collision observables obtained by mean-preserving smoothing and the smooth collision spectral splitting;
- an absolutely convergent, parameter-continuous, positive semidefinite collision Green--Kubo matrix `Gamma_R`;
- a quantitative collision characteristic estimate after shrinking-scale smoothing;
- a uniform Gaussian limit for the actual unsmoothed return record, with covariance
  \[
  D_R=c_*^{-1}\Gamma_R;
  \]
- an equivalence between zero Gaussian variance and collision/induced `L^2` coboundaries;
- a uniform collision functional CLT, including bounded BV initial densities;
- a uniform functional CLT for the actual return process;
- an unconditioned stationary physical-time functional CLT for lattice displacement and centered collision count.

The covariance is proved continuous and positive semidefinite, not uniformly positive definite. The physical-time functional theorem is unconditioned. Neither statement should be silently strengthened in later summaries.

## 4. Audit of the collision-space input

The imported functional-analytic input is the local perturbation theory for finite-horizon dispersing collision maps developed by Demers and Zhang. The manuscript identifies the relevant spectral splitting, complementary power estimate, perturbation theorem, boundary-length reparametrization, transfer convention, and strong/weak norms. It also distinguishes these collision-map results from the missing anisotropic realization of the induced unbounded record.

The geometric correspondence is plausible and substantially better documented than in earlier revisions. On the compact radius interval the obstacles are strictly dispersing, the inter-obstacle gap is uniformly positive, and the finite horizon is uniform. Reparametrizing the nearby circular boundary by the reference arclength is the kind of boundary-length change expressly contemplated in the cited perturbation framework. The rectangular two-scatterer cover and the restriction to the deck-invariant part avoid an affine deformation of specular reflection.

The use made of this input in revision 9 is also appropriately limited. Smooth densities and smooth multipliers are inserted into the collision spaces; the hard section indicator is first smoothed in ordinary coordinates. No theorem about an induced operator with an unbounded roof is imported from the cited collision theory.

Nevertheless, this remains a load-bearing specialist point. Before publication, a billiards expert should check in detail:

1. the identification of the local common collision spaces under the chosen boundary reparametrization;
2. the claimed uniform strong-norm bound for a smooth density times the invariant reference measure;
3. the multiplier estimate, including the matched-curve term and the precise source exponents;
4. the restriction from the rectangular cover to the deck-invariant subspace and the simplicity of the relevant eigenvalue there.

I found the source map consistent with the cited framework, but this referee-style audit is not a substitute for that expert verification.

## 5. Audit of the one-collision BV and covariance argument

The proof of uniform BV regularity is original to this revision and deserves attention. In rational angular charts, the outgoing velocity, candidate entry roots, admissibility conditions, and finite lattice labels form a bounded semialgebraic family. Uniform finite horizon reduces the next collision to finitely many candidate centers. Differentiable cell decomposition and one-dimensional monotonicity then give a uniform bound on the number of monotonicity intervals in each coordinate slice. Integrating the slice variations yields the two distributional first derivatives.

This route is credible. In particular, it does not claim bounded variation for an arbitrary long itinerary or for a pushed-forward density. Values assigned on tie and singular sets are irrelevant at the level of BV equivalence classes. The moving section indicator has uniformly bounded perimeter, so its BV control is elementary.

The reflected convolution is designed to preserve the invariant flat measure in `(alpha,p)`, retain positivity, and avoid applying the inverse `p=sin(phi)` map at grazing. The stated estimates

\[
 \|u-S_\delta u\|_1=O(\delta),\qquad
 \|S_\delta u\|_{C^2}=O(\delta^{-2})
\]

have the correct scaling. Combining them with the smooth collision spectral estimate gives

\[
 |\operatorname{Cov}(a,b\circ T_R^k)|\le Ce^{-\gamma k}
\]

for uniformly bounded BV observables. The optimization of the smoothing scale is correct. For a residual with `L^1` size `O(delta)`, summing

\[
 \min\{C\delta,Ce^{-\gamma k}\}
\]

produces the required `delta(1+|log delta|)` variance bound.

The resulting collision Green--Kubo series converges absolutely with a uniform tail. Fixed-lag parameter continuity follows by finite-itinerary stability away from the moving singular curves, and the uniform tail then gives continuity of the full series. The smoothing error in the covariance has the same logarithmic form. I found no hidden appeal to independence or to an induced correlation series in this argument.

The presentation should nevertheless be strengthened. The semialgebraic-to-BV step should be promoted to a standalone proposition with a precise two-dimensional slicing statement, explicit treatment of chart boundaries, and a finite candidate-center lemma. At present several nontrivial geometric-measure details are compressed into prose. This is a request for proof exposure, not an assertion that the conclusion is false.

## 6. Audit of the stopped Gaussian theorem

For the smoothed collision observable, the manuscript perturbs the genuine collision transfer operator by a smooth complex multiplier. The perturbation size is `O(|z| delta^{-2})`, so the simple eigenvalue and complementary power estimate persist on a ball of radius proportional to `delta^2`. Differentiation at zero identifies the Hessian with the smoothed collision covariance, and Cauchy estimates give the cubic remainder

\[
 O(\delta^{-6}|z|^3).
\]

The balance `delta=(1/4)m^{-1/13}` is consistent:

- the unsmoothing error is of order `m^{-1/26} sqrt(log m)`;
- the accumulated cubic spectral error is of order `m^{-1/26}`;
- the projection-amplitude and complementary-spectrum errors are smaller;
- the perturbation remains inside its analytic domain for fixed rescaled frequencies.

The return-time substitution is handled by an exact identity rather than an approximate renewal argument. The visit-count variance gives

\[
 \Pr\{|N_{n,R}-n/c_*|>a\}\le Cn/a^2.
\]

A dyadic maximal estimate controls collision sums on the deterministic window around `n/c_*`. With `a=n^{3/5}`, both the exceptional probability and the normalized window fluctuation are of order at most `n^{-1/5}` up to logarithms, smaller than the stated central characteristic error. This yields the covariance scaling `D_R=c_*^{-1}Gamma_R` with the correct normalization.

This is a meaningful advance over revision 8. It establishes the actual low-frequency Gaussian law without assuming an induced spectral expansion. The proof also correctly permits a singular limiting Gaussian.

Two qualifications are important. First, the estimate is uniform only on fixed compact sets of the rescaled variable. It is not a bound on the entire complementary Fourier region required for local inversion. Second, because `D_R` may be singular, this theorem alone cannot supply the four-dimensional Gaussian density in the raw LLT.

## 7. Audit of the Gaussian-kernel theorem

The zero-variance argument is economical and essentially correct. Exponential collision correlation decay turns zero Green--Kubo variance into a uniform bound on all collision partial-sum variances. The Cesaro averages

\[
 b_M=M^{-1}\sum_{m=1}^M S_m u
\]

are therefore bounded in `L^2`. The mean ergodic theorem and a weakly convergent subsequence produce `u=b-b\circ T_R`. Telescoping to the first return gives the induced coboundary, and the converse follows from the Gaussian characteristic limit.

This closes the measurable cohomological part of the previous low-frequency objection. It does **not** close the periodic-orbit argument. The transfer function is an `L^2` equivalence class. The selected periodic points have zero invariant measure, and one cannot insert them into an almost-everywhere identity without a Livsic-type regularity theorem adapted to the actual observable and singular billiard structure.

Accordingly, the manuscript is correct to retain uniform positive definiteness as an open step. This distinction must remain visible in the abstract, introduction, theorem statements, and any future submission letter.

## 8. Audit of the functional limits

The functional proof does more than quote the one-time Gaussian theorem. Fourth derivatives of the smooth spectral pairing give

\[
 E|S_m h_{R,\delta}|^4
 \le C\{m^2+(m+1)\delta^{-8}\}.
\]

The residual is removed in path supremum norm using the small-`L^1` dyadic maximal estimate. With the slower scale `delta_n=(1/4)n^{-1/32}`, the manuscript obtains finite-dimensional convergence from chronological products of differently twisted collision powers. The order of composition is correct, and the complementary terms vanish uniformly.

Tightness is established on a coarse collision grid of mesh

\[
 L_n\asymp\delta_n^{-8}\asymp n^{1/4}.
\]

For increments containing at least one complete coarse block, the fourth moment has the Brownian `|t-s|^2` form. Linear interpolation handles shorter intervals, while the deterministic difference between the fine and coarse smoothed processes is `O(L_n/sqrt n)=O(n^{-1/4})`. The residual process then transfers tightness to the original observable.

The actual-return functional theorem uses the uniform return-clock law and the exact stopped compensation. Dependence between the clock and the collision process is not ignored; continuity of the limiting paths and a probabilistic modulus of continuity suffice. Exponential one-block tails make the return-index interpolation negligible.

For physical time, the stationary outgoing collision state has the expected roof-biased density. The linear map

\[
 B_R(x_1,x_2,x_3,x_4)
 =(x_1,x_2,x_3-x_4/\bar\tau_R)
\]

cancels the section compensation exactly. Uniformly bounded partial flights and cell-position errors then give the unconditioned physical displacement/collision functional limit.

I found this chain coherent. For a journal version, however, the multi-twist product estimate and the coarse-grid tightness argument should each be isolated as formal lemmas. Their present compressed form makes it harder to verify that every norm and constant remains uniform in the radius and initial density.

## 9. Which objections from the revision-8 report are now closed

Revision 9 materially changes the status of the paper. The following earlier objections should no longer be repeated as if nothing had been proved:

- The actual return record now has a proved continuous Gaussian covariance, obtained from a uniformly summable collision Green--Kubo formula and exact stopping.
- A uniform central characteristic estimate is now proved for the original unsmoothed record.
- Zero Gaussian variance is now equivalent to an actual collision and induced `L^2` coboundary.
- The unconditioned collision, return, and physical-time functional Gaussian limits are now proved.
- The square-root unfinished-block issue had already been closed in the preceding revision for polynomially small same-event conditioning, and it remains closed.
- Renewal normalization, universal-cover frequency notation, and the compatibility of the collision, renewal, block, and physical pairings are presented more clearly.

These are substantial achievements. Any future review should evaluate them as theorems, not as proposed interfaces.

## 10. What remains open for the raw mixed-density LLT

The remaining gaps are narrower than in revision 8, but they are still central.

### 10.1 Nondegeneracy and a usable low-frequency local expansion

The proved matrix `D_R` is positive semidefinite. The raw four-coordinate LLT requires a uniformly positive definite covariance. The periodic rank calculation can prove this only after the `L^2` coboundary has a representative for which the identity may be evaluated on the selected periodic orbits.

Moreover, the quantitative Gaussian estimate concerns `t=O(1)` after `n^{-1/2}` rescaling. The residual-inversion theorem requires control beyond this compact central region. One may either establish an induced leading-eigenvalue expansion on a fixed neighborhood or reformulate the local inversion argument around the weaker central estimate plus a separate moderate-frequency theorem. Neither route is completed here.

### 10.2 High-frequency induced operators

The one-step periodic coercivity remains conditional on reconstructing a regular nonvanishing phase from approximate spectral vectors on an actual anisotropic induced space. Fredholm index zero, compatibility with the physical renewal operators, and quantitative resolvent bounds have not been proved. The exact `L^1` renewal realization and the `L^p -> L^q` block holomorphy do not provide these properties.

This is not a cosmetic technicality. It is the mechanism needed to control large roof frequencies before the raw branch asymptotics take over.

### 10.3 Complete critical and singular branch summation

The manuscript retains correct individual critical-edge calculations and an abstract absolute residual criterion. It still does not classify and sum all regular critical words, central branches, and singular itinerary boundaries with the actual `n`-dependent constants. The new initial-coordinate BV estimate is not an estimate on second derivatives of inverse-coarea densities. The physical-count tail deletes rare trajectories in total variation, but it does not control the density variation of the retained branches.

The strict frequency splice must be checked with genuine growth constants. Phrases such as "take the cutoff small" or "then take the derivative order large" are not substitutes for the required inequality.

### 10.4 Weighted local limits and exact conditioning events

The physical functional theorem is unconditioned. The conditioned maximal-block result compares two paths under the same event. Replacing an exact physical lattice event by a completed-block event requires relative control of their symmetric difference at the scale of the event probability. That is a weighted local-density problem, not a consequence of weak convergence or an `O(log t)` path discrepancy.

Thus the final conditioned physical-time claims remain dependent on the raw and weighted LLTs.

## 11. Top-four significance assessment

The new compensation-and-stopping argument is the strongest probabilistic contribution of the manuscript to date. It converts a difficult unbounded induced observable into a bounded collision observable, proves a uniform covariance and functional limit, and does so while respecting the moving physical section. This is technically interesting and potentially useful.

At the requested benchmark, however, one must compare the result with the extensive existing limit theory for finite-horizon dispersing billiards. Central and functional limit theorems, spectral perturbation methods, Young-tower methods, and suspension-flow limit theorems are established parts of the field. The present work's novelty lies in the precise joint physical record, the moving-radius uniformity, the exact compensation, and its integration with the arithmetic and raw-edge programme. That is significant specialist mathematics, but it is not yet presented as a general theorem whose reach clearly exceeds the concrete family.

The manuscript still asks the reader to assess a large collection of geometry, arithmetic, edge, renewal, clock, Gaussian, and conditional inversion modules against a raw LLT that remains open. At a top-four journal, such a package would normally need either:

1. completion of the advertised raw mixed-density LLT and its principal conditioned consequences; or
2. a general conceptual theorem, with several nontrivial applications, showing that the compensation-and-stopping mechanism creates new uniform Gaussian theory beyond this model.

Revision 9 achieves neither form of closure. I therefore maintain a negative top-four recommendation while substantially upgrading my assessment of the mathematical progress.

## 12. Required changes for a future submission

### Essential mathematical work for the present endpoint

1. **Prove periodic-evaluable regularity and uniform nondegeneracy.** Establish an applicable Livsic-type regularity theorem or another rigorous bridge from the `L^2` coboundary to the selected periodic records.
2. **Construct the actual induced anisotropic family.** Verify its compatibility with the exact renewal and physical pairings, Fredholm structure, phase reconstruction, and quantitative high-frequency resolvent bounds.
3. **Complete the raw branch decomposition.** Include all regular critical words and singular itinerary boundaries, with uniform derivative-norm sums and explicit `n`-dependence.
4. **Close the frequency splice.** Insert the actual constants from the induced and raw estimates and verify a nonempty range of splice parameters.
5. **Prove weighted inserted local limits.** These are required for positive denominators, exact-event replacement, and the conditioned physical-time conclusions.

### Proof-presentation work even for a specialist Gaussian paper

6. **Extract the semialgebraic BV argument.** State a precise uniform slicing lemma, candidate-center lemma, and chart-gluing proposition.
7. **Formalize the collision-space embedding.** Record the exact norm bounds for smooth densities and multipliers on each local Demers--Zhang space.
8. **Expand the multi-twist finite-dimensional proof.** Give a lemma controlling products of perturbed spectral projectors and complementary powers with all `delta_n` factors visible.
9. **Expand the coarse-grid tightness proof.** State the interpolation and adjacent-block estimates explicitly.
10. **Sharpen the literature comparison.** Explain exactly which part of the uniform joint physical-record CLT/FCLT is not already available from standard billiard or tower limit theory.
11. **Separate venue paths.** A specialist submission centered on the unconditional Gaussian and functional theorems should not make an unproved raw LLT the implicit measure of completeness. A top-four resubmission retaining the present title should complete the raw endpoint.
12. **Obtain an independent dynamics review.** The collision-space identification, singular BV argument, periodic geometry, and raw branch structure should be checked by a human specialist in dispersing billiards.

## 13. Technical and expository comments

1. The introductory Theorem A is a useful improvement. Its statement should continue to say "positive semidefinite" and should not use language suggestive of a nondegenerate local Gaussian density.
2. The notation `D_R`, `Gamma_R`, and the physical covariance `mathcal V_R` is now sufficiently separated from the visit count. Preserve this distinction.
3. State explicitly, near every quantitative characteristic estimate, whether the frequency variable is physical or rescaled. This will reduce confusion with the fixed-torus variables in the raw inversion sections.
4. The proof that smoothing the initial density gives a uniformly bounded vector in the local distribution space should be written once as a cited lemma.
5. In the fourth-moment proof, record the complex uniform bound used before applying Cauchy's estimate to the fourth derivative of the complementary term.
6. In the multi-increment proof, make clear how zero or very short blocks are handled before the asymptotic regime in which every interval length is proportional to `n`.
7. The contradiction argument for uniform bounded-Lipschitz convergence is sound, but it would help to state the continuity of `R -> Gamma_R^{1/2}` as a finite-dimensional fact.
8. The induced coboundary theorem should state explicitly that no pointwise representative is selected. The subsequent warning already conveys this correctly.
9. The common-renewal compatibility diagram is helpful. It should not be read as providing an anisotropic extension at `|z|=1`; the text correctly denies this.
10. The raw residual criterion uses second distributional derivatives. Keep emphasizing that one-collision BV is a different norm on a different object.
11. The physical-time theorem controls displacement and collision count, not the complete four-coordinate raw density or a bridge under exact conditioning. The current statement is appropriately limited.
12. The paper is now 60 pages with several historical layers. Even without deleting results, a dependency-oriented introduction and a compact theorem map would help readers distinguish unconditional conclusions from interfaces.

## 14. Reproducibility and verification boundary

The source package is materially better organized than the versions first reviewed. Both public revision-9 branches point to the same commit. The complete article is included rather than represented by a response supplement. The exact-source workflow completed successfully on the reviewed SHA. The source manifest and verification script distinguish inherited files, documented exposition changes, and the three new mathematical files.

The new finite checks cover stopped compensation, visit counting, physical-clock cancellation, dyadic decompositions, and exponent arithmetic. They are useful guards against algebraic and source-integrity errors. They cannot verify:

- the Demers--Zhang space identification;
- semialgebraic BV across billiard singularities;
- continuum spectral perturbation estimates;
- the functional tightness theorem;
- covariance nondegeneracy;
- the complete singular-branch residual sum;
- the raw LLT.

The manuscript and validation record state these limits accurately. I have not treated successful compilation or finite diagnostics as proof certification.

## 15. Final assessment

Revision 9 deserves credit for converting a central part of the programme from conditional interfaces into unconditional probability theorems. The bounded collision compensation, continuous collision covariance, stopped Gaussian limit, measurable cohomology characterization, and functional time changes form a coherent new chain. On the portions audited, I found no decisive contradiction.

The paper nevertheless remains incomplete relative to its stated raw local-limit endpoint. The missing nondegeneracy/regularity, high-frequency induced operator, global raw residual, and weighted exact-conditioning estimates are precisely the steps that distinguish a weak Gaussian theory from the advertised raw mixed-density theorem. They are not routine finishing details.

Accordingly, my recommendation remains **reject at the four-journal benchmark in the present form**. I would view a carefully focused Gaussian/functional-limit paper as a plausible strong specialist submission after independent proof review, and I would reassess a future top-four version if it closes the raw density and conditioning chain or elevates the compensation method to a demonstrably general principle.