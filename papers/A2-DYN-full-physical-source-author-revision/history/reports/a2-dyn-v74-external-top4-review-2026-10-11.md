# External top-four referee report on A2-DYN revision 74

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v74-referee-response-2026-10-11`, `revision/a2-dyn-v74-referee-copy-2026-10-11`  
**Reviewed commit:** `5a4704bc945d75e0fa181983a7b66a5dc5a73350`  
**Reviewed repository tree:** `7cdff049a54d2feda0d55f4e3bd757b8f0c3a568`  
**Active manuscript directory:** `papers/A2-DYN-v74-referee-response`  
**Active mathematical source:** one hundred sixty-seven numbered core modules; revision 74 adds modules 164--167  
**Frozen revision-73 author baseline:** `39575228f055862103edbebdd984bd6764fa0ad9`  
**Frozen revision-73 paper tree:** `995790396ccb81e24a97949b7d0143b222ad4b20`  
**Controlling report:** `reviews/a2-dyn-v73-external-top4-rereview-2026-10-11/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `e31a74560d86082da1c2f2ef55c513343cfd41a0` / `28d7999c60fc0083f99ffcb8550a932057af5b8f`  
**Exact-source qualification runs:** response `38099332009`; referee-copy `38099336557`  
**Date:** 11 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, o-minimality, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 74 is a genuine theorem-bearing response to the revision-73 rereview. It does not merely rename the paired-current obstruction. It introduces a more selective geometric quantity: entrances and exits are matched on the same connected component of the same superlevel set of the complete scalar roof density. This removes the false charge caused when an incoming positive Jordan mass and an outgoing negative Jordan mass near the same roof belong to different height layers or different excursions.

The new short-excursion functional is

\[
 S_\delta f(t)=\int_0^{f(t)}
       \left(1-\frac{|I_u(t)|}{\delta}\right)_+\,du,
\]

where `I_u(t)` is the component of the essential superlevel set
`{f>u}` containing `t`. The manuscript proves

\[
 [f(t)-2A_\delta f(t)]_+
 \le S_\delta f(t)
 \le \min\{(Df)^+([t-\delta,t]),(Df)^-([t,t+\delta])\},
\]

as well as the sharp integrated estimate

\[
 \int S_\delta f\le \frac{\delta}{8}\|Df\|_{TV}.
\]

It then applies this functional to the complete original exact-label source and proves a two-sided comparison with the original pointwise error:

\[
 \mathcal S_M(B,\delta)
 \le \mathcal E_M+C_MB^{-1/192},
\]

\[
 \mathcal E_M
 \le \mathcal S_M(B,\delta)+C_MB^{-1/192}.
\]

Under the source-pinned fixed-width estimate, the constants are independent of the width chosen before the collision limit. Consequently the short-excursion budget and the original scalar pointwise error have the same outer limit, including in the extended nonnegative reals. The same limit also equals the bounded-Lipschitz path-numerator error under the inherited common positive path-remainder theorem.

These statements are real mathematical progress. In particular, revision 74 identifies the physical shape of the remaining obstruction more sharply than revision 73. The obstruction is no longer an undifferentiated sum of directed variation, nor merely the minimum of two nearby Jordan masses. It is the collision-normalized height of genuinely short positive superlevel excursions through the same roof.

I audited the new modules

- `core/164_explicit_tame_physical_graph.tex`;
- `core/165_level_matched_short_excursions.tex`;
- `core/166_short_excursion_endpoint_budget.tex`;
- `core/167_same_roof_normalization.tex`;

and their direct interfaces with the inherited complete-height, fixed-width, positive-remainder, path-remainder, and return-clock results. I found no decisive counterexample, coarea-orientation error, missing endpoint, incorrect reserve constant, illegal interchange of a collision limsup with an infinite integral, or hidden pooling of exact labels in the new proof chain.

The negative recommendation is forced by the endpoint which the manuscript itself correctly leaves open. Revision 74 does **not** prove collision-uniform decay of short superlevel excursions for the Lorentz source. Its sufficient length-tail estimate

\[
 \mathcal T_{\varepsilon,M}(r)
 \le A\varepsilon^{-q}r^\beta
\]

and its moment alternative are hypotheses, not conclusions. The fixed-count `BV` theorem, the sharp integrated estimate, and the finite tame description do not supply the required normalized essential-supremum bound after multiplication by `m^2`.

Thus revision 74 gives a substantially better equivalence theorem, but it does not establish the organizing pointwise local limit theorem. At the requested benchmark, identifying the exact remaining obstruction is not a substitute for proving it small.

## 2. Frozen source, preservation, and qualification

Both reviewed author branches resolve to

`5a4704bc945d75e0fa181983a7b66a5dc5a73350`.

The Git tree at that commit is

`7cdff049a54d2feda0d55f4e3bd757b8f0c3a568`.

The active source directory is

`papers/A2-DYN-v74-referee-response`.

The source manifest identifies revision 73 at

`39575228f055862103edbebdd984bd6764fa0ad9`

as the frozen author baseline and the independent revision-73 rereview at

`e31a74560d86082da1c2f2ef55c513343cfd41a0`

as the controlling report.

The manifest records 163 inherited core modules and 167 active core modules. The four additions are precisely modules 164--167. It also records byte preservation of the inherited core modules, Python sources, appendices, and bibliography, and separates the short journal article from the complete technical supplement.

The active status flags are appropriately conservative. In particular, the manuscript records as false:

- `lorentz_complete_current_excess_decay_proved`;
- `lorentz_collision_uniform_current_variation_proved`;
- `lorentz_paired_flux_decay_proved`;
- `lorentz_level_matched_tail_decay_proved`;
- `full_raw_return_LLT_proved`;
- `pointwise_roof_density_LLT_proved`;
- `unrestricted_same_roof_pair_bridge_proved`;
- `forward_essential_likelihood_convergence_proved`;
- `independent_human_review`; and
- `formal_proof_certificate`.

It records as true the fixed-count tame graph, the level-matched short-excursion inequality, the sharp integrated bound, the scalar-error comparison, and the conditional length-tail implication. This is the correct distinction between deterministic reduction and dynamical closure.

The exact-SHA qualification workflows completed successfully on both reviewed refs:

- response branch run `38099332009`;
- referee-copy branch run `38099336557`.

These runs establish source identity, preservation, finite-fixture agreement, native compilation of the journal article and supplement, recorder coverage, and PDF geometry checks. They do not certify the continuum billiard geometry, parameterized integration, inherited anisotropic estimates, or the missing collision-uniform tail bound.

The present review branch starts at the reviewed author SHA and adds this report only under

`reviews/a2-dyn-v74-external-top4-review-2026-10-11/`.

No author manuscript, workflow, historical proof module, prior report, or unrelated repository path is intentionally modified.

## 3. Scope of this audit

The complete source now contains 167 core modules and an extensive historical pipeline. I have not attempted to re-prove every inherited statement. The substantive audit concentrates on:

1. the explicit fixed-collision physical graph in module 164;
2. the moving-section algebraic parameterization;
3. the exact-label finite candidate set;
4. the constructible sublevel-mass family and fixed-count monotonicity bound;
5. the one-dimensional oriented coarea identity in module 165;
6. the level-matched short-excursion upper bound;
7. the sharp integrated and length-tail identities;
8. the ordered exact-label budget in module 166;
9. the two-sided comparison with the original scalar error;
10. the finite-Riemann-sum treatment of the length-tail hypothesis;
11. preservation of the already controlled source under complementary physical weights;
12. the scalar/path comparison and normalization in module 167;
13. the distinction between the new deterministic theorems and the missing Lorentz estimate; and
14. exact-source and build evidence.

The inherited complete-density bound, fixed-width estimate, positive scalar remainder, common positive path remainder, cylinder inversion, finite arithmetic transition law, and collision-to-return clock theorem are treated as source-pinned inputs. This report does not independently recertify those results.

## 4. The moving section and the fixed-collision tame graph

Module 164 makes the finite-dimensional geometry more explicit than the preceding revision.

The moving winding angle is algebraized by the half-angle coordinate

\[
 q_R=\tan(\theta_R/2),
\]

which satisfies a quartic equation on a fixed interval. The derivative of that polynomial is bounded away from zero there, giving a unique semialgebraic graph. This places all five section centers, including the moving centers, in a common tame parameter family.

For a fixed collision count, the manuscript then introduces a finite candidate alphabet of lattice-center increments. The bound is obtained from finite horizon and from the fact that a disk which changes a first-hit or nearest-third-center comparison must lie within an explicit bounded distance of the current flight segment. Exact displacement and occupation labels remain discrete parameters in a finite set at that fixed count; unattainable labels yield the zero source rather than being pooled with attainable labels.

The auxiliary collision graph contains contact points, normals, velocities, flight lengths, reflection equations, first-hit inequalities, incidence margins, clearance branches, exact section occupation, terminal membership, displacement, and roof time. The graph projects to the two physical initial coordinates. Integration is performed in those two variables, not with ambient volume on the auxiliary graph.

This is the correct architecture for the claimed parameterized-integration argument.

I found the half-angle computation and the fixed-candidate reduction internally consistent. The proof also correctly limits its uniformity statement to a fixed collision count. It does not infer a collision-uniform cell count or a collision-uniform `BV` constant.

The remaining audit burden is substantial. A specialist should still verify that the finite candidate alphabet captures every branch which can change the original clearance minimum, that all first-hit branch inequalities survive projection exactly as claimed, and that no singular continuation is introduced when a margin vanishes. I found no concrete counterexample in the written construction.

## 5. Constructible integration and fixed-count variation

For each threshold vector, module 164 defines a positive threshold source on the unchanged exact event. Its cumulative roof mass is expressed as an integral of a globally subanalytic integrand in the original initial variables.

The argument then uses stability of constructible functions under parameterized integration, definability of the finite derivative by quantified inequalities, and one-variable monotonicity in an o-minimal structure. For each fixed collision formula this yields a finite number `J_m` of monotonicity intervals and point cells, uniform over the continuous parameters and the finite exact-label set at that count.

The unchanged smooth guard is recovered by a signed Stieltjes threshold superposition. Every threshold source remains positive; the signed measure occurs only in the external parameter integral. Total variation of the Stieltjes product measure then gives the fixed-count `BV` estimate for the complete original source.

This proof is conceptually coherent and addresses the principal tame-geometry objection raised in the preceding rereview. In particular, it does not assume the original smooth cutoff itself is definable.

It is important, however, that the result remains fixed-count. Neither the height factor nor `J_m` has controlled growth. This theorem legitimizes the Jordan decomposition used later; it does not by itself provide local concentration or endpoint decay.

## 6. Oriented superlevel decomposition

Module 165 applies the one-dimensional `BV` coarea theorem after the entire physical source has been summed.

For almost every level, the essential superlevel set is a finite union of bounded intervals. The oriented decomposition

\[
 (Df)^+=\int_0^\infty\sum_{(a,b)\subset\{f>u\}}\delta_a\,du,
\]

\[
 (Df)^-=\int_0^\infty\sum_{(a,b)\subset\{f>u\}}\delta_b\,du
\]

has the correct orientation. Entrance points contribute to the positive variation and exit points to the negative variation.

The manuscript also supplies a measurable choice of component endpoints by rational tests and parameterized integration. This is sufficient for the subsequent Tonelli arguments.

I found no missing endpoint or reversal of orientation in this part of the proof.

## 7. The level-matched height estimate

The principal deterministic theorem states

\[
 [f-2A_\delta f]_+
 \le S_\delta f
 \le \min\{f,(Df)^+([t-\delta,t]),(Df)^-([t,t+\delta])\}.
\]

The first relation is an upper bound, not a general equality. This distinction is important. Other superlevel components inside the averaging window can contribute negatively to `f-2A_delta f`, and the containing component may intersect the averaging window in more than its minimum guaranteed length. The proof uses exactly the inequality which follows from these facts.

For an isolated pulse shorter than `delta`, equality does hold, and the manuscript uses that example correctly. For a long component, the short-excursion functional vanishes even near an edge, explaining why reserve two is the optimal constant for a component-only estimate.

The right-hand bounds are also correct. Every contributing short component has both its entrance and exit in the corresponding one-sided windows, and its level weight is at most one. The oriented coarea formula then supplies the two Jordan-mass estimates.

The functional is homogeneous in the density and nondecreasing in the width. These properties are used consistently in the ordered application.

## 8. Sharp integrated estimate and length tails

Tonelli's theorem gives

\[
 \int S_\delta f(t)\,dt
 =\int_0^\infty\sum_{I\subset\{f>u\}}
        |I|\left(1-\frac{|I|}{\delta}\right)_+du.
\]

The elementary bound

\[
 x(1-x/\delta)_+\le\delta/4
\]

and the one-dimensional perimeter identity give

\[
 \int S_\delta f\le\frac\delta8\|Df\|_{TV}.
\]

A pulse of width `delta/2` attains equality, so the constant is sharp.

The tail representation

\[
 S_\delta f(t)=\frac1\delta\int_0^\delta T_f(t,r)\,dr
\]

and the negative-moment estimate are also correct.

The manuscript is right not to turn the integrated estimate into an essential-supremum estimate. An `L1` bound permits concentration on increasingly small roof sets. This distinction is precisely why revision 74 still needs a separate Lorentz-specific tail theorem.

## 9. Strict improvement over the paired Jordan minimum

The new functional is genuinely sharper than

\[
 \min\{(Df)^+([t-\delta,t]),(Df)^-([t,t+\delta])\}.
\]

Two nearby atoms may belong to different height layers or different components and therefore have no short positive excursion through the roof. The example in module 165 demonstrates this correctly. Conversely, a narrow positive pulse is charged by the exact amount left above twice its symmetric average.

This is not merely a change of notation. It removes a real overcounting mechanism in the revision-73 obstruction.

It does not, however, show that physical short excursions are rare. The improvement is geometric matching, not dynamical decay.

## 10. Comparison with the original pointwise error

Module 166 defines

\[
 \mathcal S_M(B,\delta)
 =\limsup_m\sup_{R,n,k}m^2
   \operatorname*{ess\,sup}_{t\in\mathcal C_{m,R,n,k}(M)}
             S_\delta b^{\varepsilon(B)}(t).
\]

The radius supremum is outside the roof essential supremum, and empty target sets contribute zero. No common exceptional roof set across uncountably many radii is assumed.

The upper comparison follows from `S_delta b <= b` and the positive scalar remainder identity. The lower comparison follows from

\[
 b\le2A_\delta b+S_\delta b
\]

and the inherited fixed-width estimate.

The journal article explicitly states that the fixed-width constant is independent of the width previously fixed before the collision limit. Under that source-pinned input, the constants in the two-sided comparison are independent of `delta`, and the conclusion for an arbitrary legal choice `delta(B)>0` follows.

The proof maintains the required order:

1. choose the outer frequency band;
2. choose the guard scale and roof width;
3. hold the auxiliary fixed-width spectral band fixed;
4. take the collision limit;
5. enlarge the auxiliary band;
6. finally enlarge the outer band.

No collision-dependent spectral width is inserted.

I found the squeeze argument correct under the stated inherited input.

## 11. What the equivalence theorem does and does not prove

The equality

\[
 \lim_{B\to\infty}\mathcal S_M(B,\delta(B))=\mathcal E_M
\]

is a useful structural theorem. It says that the original scalar endpoint vanishes exactly when the normalized short-excursion budget vanishes, for any width schedule chosen legally before the collision limit.

It does not imply that either side vanishes.

When the original error is positive, the short-excursion budget converges to the same positive obstruction. When the original error is infinite, the extended-real squeeze forces the short-excursion budget to be infinite as well. The theorem identifies the endpoint; it does not solve it.

This distinction is stated correctly in the manuscript and must remain explicit in every abstract, status file, and future response.

## 12. The sufficient length-tail criterion

The proposed closure hypothesis is

\[
 \mathcal T_{\varepsilon,M}(r)
 \le A\varepsilon^{-q}r^\beta.
\]

Since the tail function is nondecreasing, module 166 replaces the integral representation by a finite upper Riemann sum, fixes its mesh before the collision limit, and only then lets the mesh size tend to zero. This avoids an unjustified exchange of a limsup with an integral.

The resulting estimate

\[
 \mathcal S_M(B,\delta)
 \le \frac{A}{\beta+1}\varepsilon(B)^{-q}\delta^\beta
\]

has the correct constant for the stated tail hypothesis. The legal choice of `delta(B)` then closes the scalar and path endpoints conditionally.

The moment alternative follows directly from the deterministic moment inequality.

Neither condition is proved for the Lorentz source. The source manifest and publication status record this accurately.

## 13. Why fixed-count `BV` and the integrated bound are insufficient

The fixed-count variation bound may grow exponentially and contains an uncontrolled monotonicity number. Even a much smaller total-variation bound would not automatically control

\[
 m^2\operatorname*{ess\,sup}_t S_\delta b(t).
\]

A family of nonnegative densities can have finite variation and small integrated short-excursion mass while concentrating that mass into roof intervals whose length tends rapidly to zero. The essential height may remain large or diverge.

Likewise, the fact that each derivative has total mass zero gives no local cancellation estimate. The positive and negative Jordan parts may be closely paired but large.

A proof of the endpoint therefore needs quantitative information on the distribution of component lengths and heights, not only existence of a finite current.

## 14. Preservation of the controlled source

The complementary-weight construction keeps the already controlled source `s_{71,1}` in the controlled part and reallocates only the original residual source. The allocation coefficient is a Borel function of the physical roof and is applied on the common physical kernel.

The two allocated densities sum to the unchanged full source, and the residual is bounded by the short-excursion functional. Exact labels, trajectories, and conditioning events are preserved.

The manuscript appropriately does not assert that the allocated densities themselves are `BV`.

I found no source deletion or event replacement in this construction.

## 15. Scalar and path-valued errors

Module 167 uses the inherited positive path-remainder decomposition

\[
 \mathbf P-G\mathsf W_R=\mathbf b_B+\mathbf E_B,
 \qquad \mathbf b_B\ge0.
\]

The constant test and positivity give

\[
 |P-G|
 \le\|\mathbf P-G\mathsf W_R\|_{BL^*}
 \le |P-G|+2\|\mathbf E_B\|_{BL^*}.
\]

Taking the collision limit at fixed band and then enlarging the band proves equality of the ordered scalar and bounded-Lipschitz path-numerator errors.

On positive reference classes, vanishing of the scalar endpoint then gives the displayed conditional path, density-ratio, and window-normalized likelihood conclusions. Zero arithmetic classes are not normalized.

This is a correct downstream reduction under the inherited path theorem. It is not a path-space total-variation theorem, and it does not independently audit the inherited cylinder inversion, tightness, or clock-transfer inputs.

## 16. The decisive unresolved Lorentz estimate

The next revision must prove a collision-uniform estimate on the lengths of the superlevel components of the complete exact-label density. A sufficient form is

\[
 \mathcal T_{\varepsilon,M}(r)
 \le A\varepsilon^{-q}r^\beta,
\]

uniformly in the radius, return index, displacement, collision count, and central roof target, with the guard and width chosen before the collision limit.

An equivalent moment estimate would also suffice.

The estimate must arise from the actual Lorentz geometry and dynamics. It cannot be obtained merely from:

- the fixed-count tame cell decomposition;
- the number of physical words;
- finite total variation;
- total current mass zero;
- a small source mass;
- the fixed-width average estimate;
- or the sharp integrated short-excursion inequality.

The required theorem must rule out positive roof spikes whose level components become too short at the `m^{-2}` normalized scale.

Possible routes include a collision-uniform coarea/transversality theorem, a quantitative bound on the creation and pairing of roof critical values, or a multiscale estimate on the length distribution of positive superlevel components. Any such route must preserve the original exact labels and zero arithmetic classes and respect the fixed-band order of limits.

## 17. Consequences still unavailable

Until the short-excursion tail is controlled, the manuscript does not establish unconditionally:

- the exact-label scalar pointwise raw local limit theorem;
- the pointwise roof-density local limit theorem;
- the same-roof point-conditioned collision bridge;
- the actual-return path theorem after clock transfer;
- the forward essential arithmetic likelihood convergence; or
- the complete endpoint consequences on every positive arithmetic class.

The deterministic equivalence theorem shows that these conclusions share one scalar obstruction. It does not make them unconditional.

## 18. Generality and top-four significance

Revision 74 improves the conceptual quality of the program. Matching entrance and exit fluxes on the same superlevel component is a natural one-dimensional geometric-measure-theoretic refinement, and the exact-label application is nontrivial.

At the requested venue level, however, the article remains governed by an unfinished theorem. The completed new deterministic lemmas are not by themselves sufficiently broad to replace the missing Lorentz endpoint as the principal claim.

A positive top-four case would require at least one of the following:

1. completion of the collision-uniform short-excursion estimate and hence of the original raw pointwise theorem;
2. a general theorem controlling level-component tails for a broad class of singular hyperbolic pushforward densities, with several genuinely distinct applications; or
3. another theorem of comparable independent significance which does not rely editorially on the unresolved Lorentz endpoint.

Revision 74 does not yet meet any of these alternatives.

## 19. Journal architecture and exposition

The separation into a short journal-facing `main.tex` and a complete technical `supplement.tex` is a substantial editorial improvement over treating the entire archival pipeline as one uninterrupted manuscript. The source-pinned input statement in the journal article is useful: it makes clear which inherited interfaces are being invoked.

For an eventual submission, each source-pinned input used by the journal theorem should nevertheless be stated in a form that a reader can verify without navigating a long revision archive. The supplement may contain the proofs, but the main article should state all hypotheses and uniformities precisely.

One metadata issue remains: `SPECIALIST_AUDIT.md` in the active v74 directory still identifies itself as a revision-73 audit and discusses modules 160--163 rather than the new modules 164--167. This does not change the mathematical source or the authoritative manifest, but it should be regenerated or moved to provenance before another handoff.

## 20. Independent specialist audit still required

No independent human audit is recorded. The highest-priority checks are:

1. the finite candidate alphabet for first-hit and clearance comparisons;
2. exact semialgebraic encoding of the moving section and exact labels;
3. the application of constructible parameterized integration to the projected physical graph;
4. the uniform fixed-formula monotonicity count at each collision count;
5. measurable selection of essential superlevel components;
6. the localized oriented coarea identity;
7. the inherited fixed-width estimate and its width-independent constant;
8. the inherited positive scalar and path remainder chains;
9. the collision-to-return clock transfer; and
10. the eventual collision-uniform short-excursion tail estimate.

Finite fixtures, source hashes, and PDF checks cannot certify these continuum arguments.

## 21. Required changes before another top-four review

A genuinely new revision should address the following matters.

1. **Prove physical short-excursion decay.** Establish the stated tail or moment estimate, or another estimate which makes the ordered short-excursion budget vanish in the legal limit order.
2. **Keep every exact label.** Do not pool displacement, collision count, return index, or arithmetic zero classes to obtain the estimate.
3. **Respect the order of limits.** All guard scales, roof widths, finite meshes, and auxiliary bands must be chosen before the collision limsup in the order stated by the source-pinned interfaces.
4. **Close the scalar theorem first.** Use the established equivalence to derive path and likelihood consequences only after the scalar endpoint is unconditional.
5. **Give a specialist-auditable geometric mechanism.** State quantitative constants and identify how critical values, coarea Jacobians, and short level components are controlled uniformly in collision count.
6. **Update active audit metadata.** Replace the stale revision-73 specialist-audit file with a v74 audit map or move it into provenance.
7. **Retain the journal/supplement separation.** Keep the short proof route while ensuring every imported theorem is stated precisely in the journal article.
8. **Obtain independent human review.** The tame-geometry, geometric-measure-theory, and inherited spectral chains require specialists in the relevant areas.

## 22. Final assessment

Revision 74 is a meaningful advance over revision 73.

It makes the fixed-collision physical graph explicit, refines paired variation into a same-level same-component short-excursion functional, proves a sharp integrated estimate and length-tail representation, and identifies the exact equality of outer limits between the short-excursion budget, the original scalar error, and the bounded-Lipschitz path-numerator error.

I found no decisive error in modules 164--167.

The remaining obstruction is now cleaner, but it remains unproved: collision-uniform decay of physical short superlevel excursions for the complete original exact-label Lorentz source.

Until that estimate is established, the manuscript does not prove its organizing pointwise raw local limit theorem and is not ready for *Annals*, *Acta*, *Inventiones*, or *JAMS*.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
