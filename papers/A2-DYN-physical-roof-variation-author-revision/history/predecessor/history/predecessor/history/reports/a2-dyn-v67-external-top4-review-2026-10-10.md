# External top-four referee report on A2-DYN revision 67

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v67-referee-response-2026-10-10`, `revision/a2-dyn-v67-referee-copy-2026-10-10`  
**Reviewed commit:** `add4d884ec0902fd5c70c68e1a82065442eab58f`  
**Reviewed repository tree:** `c70a4408b9dbabda3f0268cd99466c315e111c7b`  
**Complete revision-67 paper tree:** `266c432351a184e230b7e4df4f970c9d9f87208c`  
**Ordinary source payload tree:** `406dfc9ba6935c18e0128c3e387c6c61b5fee957`  
**Active manuscript directory:** `papers/A2-DYN-v67-referee-response`  
**Active mathematical source:** one hundred forty-five numbered core modules; revision 67 retains all one hundred forty-two revision-66 modules and adds modules 143--145  
**Frozen revision-66 author baseline:** `e96761c0b12dbc46c187f4aeb4ee8d537863dec5`  
**Frozen revision-66 complete paper tree:** `fdf737e94888a540c05d86c458d77b500895e713`  
**Controlling external report:** `reviews/a2-dyn-v66-external-top4-review-2026-10-10/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `31eae1cab4ac138d0d9c892cb76c63286cb73307` / `e3e06c75e0b6a73b613c944223423c0dc03b3854`  
**Date:** 10 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 67 is a genuine theorem-bearing advance over revision 66. The preceding report identified a precise obstruction: revision 66 controlled a finite-width positive collar trace, but the passage to the physically relevant zero-width coefficients required a collision-count-uniform angular-loss estimate. Fixed-word dominated convergence did not justify interchanging the collar-width limit with the long-orbit limit.

Revision 67 resolves this passage on every fixed, explicitly defined angular-condition stratum.

The new source introduces primitive physical and section margins on the count-uniform Morse charts, separates active homogeneous thresholds from inactive translated thresholds, and defines a scale-invariant angular condition number

\[
 \mathfrak a_{z,\lambda}
 =\max\left\{\rho_z^{-1},\frac{\kappa_z}{\theta_{z,\lambda}}\right\},
 \qquad
 \kappa_z=\sum_{f(0)=0}\frac{L_f}{|Df(0)|}.
\]

It proves that on the stratum `mathfrak a <= K`, the actual nonlinear angular fraction and its tangent fraction satisfy

\[
 (1-Kr)\theta_{z,\lambda}
 \le a_{z,\lambda}(u)
 \le(1+Kr)\theta_{z,\lambda},
 \qquad r=\sqrt{2u}.
\]

This estimate is relative to the physical coefficient. Combined with the inherited lower multiplicative density profile, it can be absorbed into the positive finite-width trace before taking the collision-count limit. The manuscript thereby obtains an unconditional ordered zero-width bound for

\[
 \mathcal B^K_{m;\lambda,R}
 =\sum_{\mathfrak a_{z,\lambda}\le K}
       J_z\theta_{z,\lambda}\delta_{t_z}
\]

at every fixed `K`, and then converts that atomic bound into an essential-height estimate for the corresponding original-source caustic collars.

This is the first revision in the recent critical-trace sequence which actually proves a zero-width physical trace theorem, rather than a finite-width surrogate, on a nontrivial positive part of the original Lorentz source.

I audited the new modules

- `core/143_relative_angular_stability.tex`;
- `core/144_stratified_zero_width_trace.tex`;
- `core/145_angular_tails_and_complete_source.tex`;

and their use in the revised front matter. I also checked the inherited finite-width trace statement, nonlinear multiplicative profile, exact-label Boolean masking, source normalization, order of limits, and positive raw-error identity on which the new modules depend.

I found no decisive counterexample, normalization error, missing label factor, incorrect polar/coarea factor, invalid sign-union estimate, or reversal of the proved limits in the new three-module chain. In particular:

1. inactive translated margins are protected by an explicit radius rather than treated as homogeneous;
2. active-margin disagreement is charged to a sum of curvature-to-gradient ratios, with no angle-separation hypothesis;
3. exact outputs are zero or one-hot, so summing label errors costs at most a factor two rather than the number of labels;
4. the relative estimate is stated only for positive tangent fraction and keeps zero-fraction nonlinear source in the positive complement;
5. the lower nonlinear density profile is used before the collision-count limit, producing a genuinely positive absorption;
6. the finite-width collar theorem applies to arbitrary positive subfamilies, so restricting to a fixed stratum creates no word-count multiplier;
7. the collision-count limit is taken at fixed stratum and fixed collar width, followed by the collar-width limit;
8. the essential-height estimate uses the physical atomic mass in the interval of critical centers which can contribute to the prescribed roof;
9. the tail functional `E(K)` is built from physical coefficients `J_z theta`, not the larger reversible weights; and
10. the manuscript does not claim that a constant independent of `K` gives convergence uniform in `K`.

These are substantial improvements and the new component theorem appears internally coherent, subject to specialist verification of its inherited geometric inputs.

The negative recommendation is nevertheless unavoidable.

The manuscript has not proved

\[
 \lim_{K\to\infty}E(K)=0,
\]

where `E(K)` is the collision-limsup physical weight of the high-condition strata. Every fixed word belongs to some finite stratum, but fixed-count exhaustion does not imply tightness after the long-count limsup. The optional moment condition in module 145 is a correct sufficient criterion, but no such Lorentz moment estimate is established.

More importantly, even a proof of `E(K) -> 0` would close only the seam-chart angular passage. The exact positive complement still contains

- failed incidence taper;
- selected grazing;
- noncritical-rank components;
- non-seam critical centers;
- labels with zero tangent fraction but positive nonlinear source;
- large-condition strata;
- omitted chart annuli; and
- every physical source piece outside the selected normal-critical disks.

No ordered essential-height estimate is proved for this complement. The complete first-incidence height also remains open.

Consequently revision 67 still does not prove

- the complete ordered incidence height;
- the complete ordered clearance height;
- the unrestricted two-sided pointwise arithmetic raw-density theorem;
- unrestricted same-roof collision and actual-return bridges;
- forward essential-likelihood convergence; or
- the unrestricted pointwise roof-conditioned path theorem.

These are not cosmetic extensions. They remain the endpoint around which the title, the positive-error representation, and a substantial part of the one-hundred-forty-five-module architecture are organized.

At the requested benchmark, the article would need either

1. a proof of the physical condition-number tail together with ordered control of the complete incidence and complementary clearance sources, thereby closing the title-level pointwise theorem; or
2. a substantially broader theorem, with quantitatively verifiable hypotheses and several genuinely different singular-hyperbolic realizations, whose significance no longer depends on the unfinished Lorentz endpoint.

Revision 67 provides neither yet. No independent human specialist audit has been obtained.

My assessment is therefore positive about the new zero-width stratum theorem and negative about readiness for *Annals*, *Acta*, *Inventiones*, or *JAMS*.

## 2. Frozen source, chronology, and preservation

Both reviewed author branches resolve to

`add4d884ec0902fd5c70c68e1a82065442eab58f`.

The repository tree at that commit is

`c70a4408b9dbabda3f0268cd99466c315e111c7b`.

The complete revision-67 paper tree is

`266c432351a184e230b7e4df4f970c9d9f87208c`.

The active article is

`papers/A2-DYN-v67-referee-response`.

The ordinary source payload tree recorded in the manifest is

`406dfc9ba6935c18e0128c3e387c6c61b5fee957`.

The immediate mathematical baseline is revision 66 at

`e96761c0b12dbc46c187f4aeb4ee8d537863dec5`.

The controlling review is the revision-66 report at

`31eae1cab4ac138d0d9c892cb76c63286cb73307`.

Revision 67 begins from a source-preserving checkpoint whose parent is the frozen review state and then lands a complete new author source. The final source manifest records

- all 142 inherited core modules byte-identical;
- all 194 inherited Python files byte-identical;
- all six inherited appendix files byte-identical;
- the bibliography byte-identical;
- every one of the 1,895 inherited mathematical labels retained;
- 145 compiled core modules and 1,928 current labels;
- the old abstract and introduction compiled verbatim in `appendices/v66_frontmatter.tex`;
- the old complete main source and replaced metadata archived in provenance;
- `lorentz_relative_angular_strata_proved: true`;
- `lorentz_stratified_zero_width_trace_proved: true`;
- `lorentz_stratified_caustic_height_proved: true`;
- `lorentz_angular_condition_tail_proved: false`;
- `lorentz_complete_source_coverage_proved: false`;
- `grazing_boundary_pointwise_smallness_proved: false`;
- `clearance_boundary_pointwise_smallness_proved: false`;
- `full_raw_return_LLT_proved: false`;
- `pointwise_roof_density_LLT_proved: false`;
- and `independent_human_review: false`.

These flags accurately distinguish the new component theorem from the unproved complete-source endpoint.

The present review branch begins directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v67-external-top4-review-2026-10-10/`.

No author manuscript source, workflow, prior review, historical manuscript, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-SHA revision-67 qualification on the response branch completed successfully:

- response run `38052540554`;
- reviewed SHA `add4d884ec0902fd5c70c68e1a82065442eab58f`;
- conclusion `success`.

At the time of this audit, the referee-copy branch points to the same SHA but has no separate workflow run listed. The mathematical source is therefore frozen identically on both refs, but the repository should not describe the packet as having completed two-ref qualification until an actual copy-branch run exists.

The validation protocol checks

- the frozen revision-66 complete paper tree;
- the controlling revision-66 report blob;
- all 142 inherited core files;
- all 194 inherited Python files;
- all six inherited appendices;
- the unchanged bibliography;
- all 145 compiled core modules;
- every inherited label and compiled input;
- the ordinary source payload and workflow hashes;
- normal and optimized finite diagnostics;
- native TeX compilation without shell escape;
- stabilized cross-references and warning-free typesetting; and
- theorem-label-based rendering of the new proof pages.

The new finite fixtures test homogeneous threshold geometry, inactive offsets, near-coincident normals, one-hot label partitions, positive absorption, coincident atoms and the conditional moment exponent. Deliberate negative controls distinguish

- bounded absolute jets from relative angular control;
- near-zero inactive offsets from stable inactive signs;
- zero tangent fraction from zero nonlinear source; and
- the proved order of limits from a reversed diagonal.

These are useful source, algebra and typesetting checks. They do not certify

- the inherited physical margin description;
- the selected-contact continuation;
- the relative nonlinear density profile;
- the finite-width two-strip local theorem;
- the physical condition-number tail;
- the complete incidence or clearance height;
- the unrestricted pointwise theorem; or
- independent human review.

The manuscript and its validation files state this boundary accurately.

## 4. Scope of this review

I did not attempt to re-prove all 145 core modules. The substantive audit concentrates on the mathematics that can change the revision-66 assessment:

1. the primitive scalar-margin list;
2. the inactive-sign stability radius;
3. the active curvature-to-gradient budget;
4. the homogeneous angular-threshold estimate;
5. the exact Boolean output and one-hot label structure;
6. the relative angular estimate;
7. the definition and scaling invariance of the condition number;
8. restriction to a fixed physical stratum;
9. use of the inherited lower multiplicative density profile;
10. positive absorption into the finite-width collar trace;
11. order of the collision-count and collar-width limits;
12. ordered zero-width atomic concentration;
13. conversion from atomic concentration to essential height;
14. the physical weighted tail `E(K)`;
15. the optional moment criterion;
16. the treatment of zero tangent fraction;
17. the complete positive source partition;
18. the unchanged incidence obstruction;
19. the exact arithmetic factor and zero classes;
20. source preservation and workflow evidence; and
21. the remaining top-four endpoint.

The inherited modules 1--142 are treated as a source-pinned baseline, not as independently recertified mathematics. Their load-bearing continuum claims remain subject to the specialist-audit requests in earlier reports.

## 5. Primitive margins and the verified local description

For each selected normal-critical word, the manuscript chooses a closed disk contained in

- the inherited Morse chart;
- the saturated first-clearance disk; and
- a disk on which a finite Boolean description of every physical and section decision has been verified.

This last restriction is essential. A local physical source cannot be described by keeping only the visibly active seam while silently omitting a competing disk, first-hit condition, section edge, occupation decision or terminal decision.

For every scalar margin `f` the paper records

\[
 b_f=f(0),\qquad A_f=|Df(0)|,
 \qquad L_f=\frac12\sup\|D^2f\|.
\]

The inactive radius is

\[
 \rho_z=\min\left\{
 \bar r_z,
 \min_{b_f\ne0}
       \frac{|b_f|}{2(A_f+L_f\bar r_z)}
 \right\}.
\]

For `r < rho_z`, Taylor's theorem gives

\[
 |f(r\omega)-b_f|
 \le r(A_f+L_f\bar r_z)<|b_f|/2,
\]

so every inactive sign remains fixed.

This is the correct way to handle translated thresholds. A homogeneous sign-disagreement estimate cannot be applied uniformly to a threshold whose offset approaches zero.

The radius is positive for each fixed word, but no lower bound uniform in the collision count is asserted. The manuscript correctly incorporates its reciprocal into the condition number rather than hiding it inside a nominally uniform chart radius.

The principal inherited issue is whether the finite Boolean description is indeed complete on the selected disk for every physical-side continuation. That statement is imported from the earlier margin-description module and remains a high-priority specialist check.

## 6. The homogeneous threshold estimate

For an active margin, the manuscript assumes

\[
 f(0)=0,\qquad |Df(0)|=A>0,\qquad
 |f(r\omega)-rDf(0)\cdot\omega|\le Lr^2.
\]

Sign disagreement implies

\[
 |Df(0)\cdot\omega|\le Lr.
\]

After rotation, the normalized angular measure of this set is

\[
 \frac2\pi\arcsin\left(\min\{1,Lr/A\}\right)
 \le\min\{1,Lr/A\}.
\]

The constant is correct. No separation between the gradients of different margins is needed because the proof uses a union bound over the primitive scalar tests.

This point is important. Near-coincident active directions can make the physical angular cell very small, but they do not invalidate the absolute union estimate. Their effect appears later through division by the physical fraction `theta`.

The estimate uses only second derivatives and one-dimensional angular geometry. I found no exponent or normalization error here.

## 7. Exact labels and the one-hot Boolean output

Let

\[
 \kappa_z=\sum_{b_f=0}\frac{L_f}{A_f}.
\]

The union of all active sign-disagreement arcs has normalized angular measure at most

\[
 \min\{1,\kappa_zr\}.
\]

Outside this union, every primitive physical and section bit agrees with its tangent bit. The manuscript explicitly includes

- first-hit selection;
- initial section membership;
- occupation at collision times `0,...,m-1`;
- terminal section membership at collision `m`;
- displacement; and
- exact return count.

The nonlinear and tangent output vectors are each either zero or a single unit vector. Therefore their pointwise `ell^1` distance is at most two, and

\[
 \sum_\lambda|a_{z,\lambda}(u)-\theta_{z,\lambda}|
 \le2\min\{1,\kappa_zr\}.
\]

This avoids multiplying the angular error by the number of possible labels.

The one-hot argument is structurally correct. It depends on using the actual visit rule after all primitive bits have been compared; one must not freeze the exact label at the singular center.

## 8. The relative angular estimate

For positive tangent fraction define

\[
 \mathfrak a_{z,\lambda}
 =\max\left\{ho_z^{-1},
              \kappa_z/\theta_{z,\lambda}ight\}.
\]

This quantity is invariant under positive rescaling of an individual scalar margin. On the stratum

\[
 \mathfrak a_{z,\lambda}\le K
\]

and for `r < K^{-1}`, one has `r < rho_z` and

\[
 \kappa_zr\le Kr\theta_{z,\lambda}.
\]

The absolute angular estimate therefore becomes

\[
 (1-Kr)\theta_{z,\lambda}
 \le a_{z,\lambda}(u)
 \le(1+Kr)\theta_{z,\lambda}.
\]

I find this deduction correct.

The result is stronger than the fixed-word dominated-convergence statement in revision 66. It gives an explicit relative modulus on a physically weighted stratum and permits simultaneous seams and arbitrarily close tangent directions.

It does not provide any collision-count control of `mathfrak a`. A very small inactive radius or a very small physical fraction can move a word into a high-condition stratum even if all selected contact jets are bounded.

## 9. Positive absorption into the finite-width trace

The inherited nonlinear density profile has the lower bound

\[
 b_{z,\lambda}^{\varepsilon,\mathrm{clr}}(t_z+u)
 \ge e^{-K_\chi\sqrt{2u}}
       J_za_{z,\lambda}(u).
\]

On the fixed stratum and for `u < s`, the relative estimate gives

\[
 a_{z,\lambda}(u)
 \ge(1-K\sqrt{2s})\theta_{z,\lambda}.
\]

Hence

\[
 b_{z,\lambda}^{\varepsilon,\mathrm{clr}}(t_z+u)
 \ge e^{-K_\chi\sqrt{2s}}
      (1-K\sqrt{2s})\beta_{z,\lambda}.
\]

Averaging and summing positive coefficients at unchanged critical values yields

\[
 \mathcal B^K_m(I)
 \le
 \frac{e^{K_\chi\sqrt{2s}}}{1-K\sqrt{2s}}
 \mathcal Q^K_{m,s}(I).
\]

This is the decisive new step. It avoids the additive angular-loss term by absorbing a relative error on the physical coefficient itself.

No estimate for the larger reversible trace

\[
 \sum_zJ_z\delta_{t_z}
\]

is used. This is conceptually appropriate: the observable coefficient is `J_z theta`, not `J_z`.

The positivity argument is exact. Coincident critical values simply add, and restriction to a subfamily only deletes positive source pieces from the inherited collar comparison.

## 10. Ordered zero-width trace concentration

For fixed `K`, `chi`, `epsilon`, `s` and `h`, the inherited finite-width theorem gives

\[
 \limsup_m\sup_{R,\lambda,t}
 m^2\mathcal Q^K_{m,s;\lambda,R}([t-h,t+h])
 \le C(2h+s).
\]

Combining this with positive absorption gives

\[
 \limsup_m\sup_{R,\lambda,t}
 m^2\mathcal B^K_{m;\lambda,R}([t-h,t+h])
 \le C\frac{e^{K_\chi\sqrt{2s}}}{1-K\sqrt{2s}}(2h+s).
\]

The left side is independent of `s`. Letting `s` decrease to zero after the collision limsup proves

\[
 \limsup_m\sup_{R,\lambda,t}
 m^2\mathcal B^K_{m;\lambda,R}([t-h,t+h])
 \le2Ch.
\]

The order of limits is valid. The proof does not use the fixed-count identity `Q_{m,s} -> B_m` and does not choose a collar width depending on `m`.

The constant in the final inequality is independent of `K`, but this does not imply that convergence in `m` is uniform in `K`. The manuscript explicitly preserves this distinction.

Subject to the inherited collar theorem, I find the argument internally sound.

## 11. The stratified angular-loss bound

The one-sided relative estimate gives, on the fixed stratum,

\[
 (\theta-a(u))_+
 \le K\sqrt{2u}\,\theta.
\]

Averaging from zero to `s` yields the factor

\[
 s^{-1}\int_0^s\sqrt{2u}\,du
 =\frac23\sqrt{2s}.
\]

Therefore

\[
 \mathcal D^K_{m,s}(I)
 \le\frac23K\sqrt{2s}\,\mathcal B^K_m(I).
\]

Using the atomic concentration on a unit window gives

\[
 \limsup_m\sup m^2\mathcal D^K_{m,s}([t-1,t+1])
 \le\frac43CK\sqrt{2s}.
\]

The constants and the Cesaro factor are correct.

This result genuinely replaces the fixed-word dominated-convergence argument on each fixed stratum.

## 12. Essential height of the original source on a good collar

The positive density

\[
 b^{K,H}_{m;\lambda,R}(t)
 =\sum_{z\in\mathcal Z_{m,R,\lambda}(K)}
  \mathbf1_{\{0<t-t_z<H\}}
  b_{z,\lambda}^{\varepsilon,\mathrm{clr}}(t)
\]

is a restriction of the original source.

The upper nonlinear profile and relative angular estimate give, for every contributing center,

\[
 b_{z,\lambda}^{\varepsilon,\mathrm{clr}}(t)
 \le e^{K_\chi\sqrt{2H}}
      (1+K\sqrt{2H})\beta_{z,\lambda}.
\]

If a center contributes at roof `t`, then

\[
 t_z\in[t-H,t].
\]

Applying the atomic concentration to this interval gives

\[
 \limsup_m\sup_{R,\lambda}
 m^2\|b^{K,H}_{m;\lambda,R}\|_\infty
 \le CH e^{K_\chi\sqrt{2H}}
          (1+K\sqrt{2H}).
\]

This is an actual ordered essential-height estimate, not a mass bound or an interval-average theorem.

The argument uses common coarea representatives and removes only finite-count null sets. I found no missing factor of `H` or `sqrt(H)`.

This is the strongest new theorem in revision 67.

## 13. The physical condition-number tail

The high-condition physical trace is

\[
 \mathcal E^K_{m;\lambda,R}
 =\sum_{\mathfrak a_{z,\lambda}>K}
    \beta_{z,\lambda}\delta_{t_z},
\]

with

\[
 E(K)=\limsup_m\sup_{R,\lambda,t}
 m^2\mathcal E^K_{m;\lambda,R}([t-1,t+1]).
\]

This is the correct tail to consider. It is weighted by the physical coefficients and keeps the original exact labels. An unweighted count of critical words would be far too large and would not reflect the source.

The full angular loss satisfies

\[
 \limsup_m\sup m^2\mathcal D_{m,s}([t-1,t+1])
 \le\frac43CK\sqrt{2s}+E(K).
\]

The proof is correct: outside the good stratum, one-sided angular loss is at most the complete tangent fraction, hence at most the bad physical coefficient.

The additional statement

\[
 E(K)\longrightarrow0
\]

would close the angular-loss passage for the seam-chart family. It is not proved.

The fact that each fixed word has a finite condition number is insufficient. A sequence of collision counts may place an increasing proportion of the physical atomic weight on strata whose inactive radii shrink, whose curvature-to-gradient budgets grow, or whose physical angular fractions collapse.

The conditional moment criterion

\[
 \limsup_m\sup m^2
 \sum\beta_{z,\lambda}\mathfrak a_{z,\lambda}^p<\infty
\]

correctly implies `E(K) <= C K^{-p}`. No such moment bound is established for the Lorentz source.

This is now the sharpest new blocker inside the seam-chart family.

## 14. Zero tangent fraction is not zero physical source

Labels with

\[
 \theta_{z,\lambda}=0
\]

have zero atomic coefficient and contribute no one-sided loss

\[
 (\theta-a(u))_+.
\]

They may nevertheless have

\[
 a_{z,\lambda}(u)>0
\]

for positive `u` because nonlinear boundaries can create a small physical sector which is absent from the tangent cone.

The manuscript correctly excludes these labels from the condition number and keeps their nonlinear density in the positive remainder.

This distinction is essential. It would be invalid to delete such source merely because the zero-width tangent coefficient vanishes.

The finite negative control in the validation packet is useful, but the continuum conclusion still depends on the inherited completeness of the physical margin description.

## 15. The complete positive source partition

For fixed `K`, `H`, `chi` and `epsilon`, the article writes

\[
 b^{\varepsilon,\mathrm{clr}}
 =b^{K,H}+r^{\varepsilon,\chi,K,H},
 \qquad r^{\varepsilon,\chi,K,H}\ge0.
\]

The remainder includes

- the original outside source;
- failed tapered incidence;
- selected grazing;
- noncritical rank components;
- non-seam critical centers;
- zero-tangent-fraction labels;
- large-condition strata;
- source outside the `H` collar;
- omitted annuli; and
- every other uncovered physical class.

The height budget is

\[
 \mathcal H(b^{\varepsilon,\mathrm{clr}})
 \le CH e^{K_\chi\sqrt{2H}}(1+K\sqrt{2H})
      +\mathcal H(r^{\varepsilon,\chi,K,H}).
\]

This is a useful exact reduction. It is not a proof that the second term is small.

A bound on `E(K)` controls only the atomic high-condition part inside the seam-chart angular passage. It does not estimate the nonlinear height of the entire remainder.

The complete clearance-height problem is therefore not reduced to `E(K)` alone.

## 16. The complete first-incidence source

Revision 67 concerns clearance-seam charts on which the incidence guards are already saturated.

It does not improve the ordered first-incidence height.

The inherited inverse-incidence and finite-count coarea theorems yield bounds with exponential collision-count constants. They do not produce the fixed-band ordered estimate required by the positive raw-error criterion.

Thus even a complete solution of the angular and clearance complement problems would leave a separate incidence task unless a new argument treats both source types simultaneously.

The source manifest accurately keeps

`grazing_boundary_pointwise_smallness_proved: false`.

## 17. Order of limits

The proved stratum theorem uses the legitimate order

1. fix the reconstruction band and its physical width;
2. fix `chi`, `epsilon`, `K`, collar width `s` and roof interval radius `h`;
3. let the collision count tend to infinity;
4. let `s` tend to zero;
5. only with an additional tail theorem may one let `K` tend to infinity.

The essential-height theorem similarly fixes `K` and `H` before the collision limit, then lets `H` decrease.

The following shortcuts are invalid:

- choosing `K=K_m` from fixed-count exhaustion;
- choosing `s=s_m` from pointwise convergence of one word;
- using a constant independent of `K` as if the convergence in `m` were uniform in `K`;
- replacing `E(K)` by an unweighted count of words;
- deleting zero-tangent-fraction nonlinear source;
- choosing the reconstruction band exponentially in `m` to pay an exponential geometric constant.

The manuscript avoids these shortcuts.

Any future revision must preserve this order.

## 18. What revision 67 closes

Relative to revision 66, the new manuscript closes the following issues.

- Inactive translated physical margins are protected by an explicit radius.
- Active nonlinear sign changes have a quantitative homogeneous angular bound.
- Exact-label angular error is controlled without a label-count factor.
- On every fixed physical condition stratum, angular error is relative to the physical coefficient.
- The relative error is absorbed into the positive collar trace before the collision limit.
- The finite-width physical trace yields a zero-width physical trace theorem on that stratum.
- The zero-width physical coefficient receives an ordered critical-value concentration estimate.
- The corresponding original-source caustic collar receives an ordered essential-height bound.
- The remaining angular passage is expressed as a positive physical weighted tail.
- The complete nonlinear complement remains visible as an exact positive source.

These are meaningful advances, not merely changes in notation or topology.

## 19. What revision 67 does not close

The manuscript still lacks

1. a proof that `E(K) -> 0`;
2. any uniform physical moment or tail estimate for the condition number;
3. ordered height control for the positive complement;
4. ordered height control for zero-tangent-fraction nonlinear sectors;
5. selected-grazing coverage;
6. failed-taper coverage;
7. all noncritical-rank and non-seam components;
8. the complete first-incidence height;
9. the complete clearance height;
10. the unrestricted two-sided pointwise raw-density law;
11. unrestricted same-roof bridge convergence;
12. forward essential likelihood on the full central window; and
13. an unrestricted pointwise roof-conditioned path theorem.

The new result is a component theorem. It does not yet prove the title-level endpoint.

## 20. Consequences for the unrestricted pointwise law

The target remains

\[
 \sup_{R,n,k}
 \operatorname*{ess\,sup}_{|Z_{m,R}|\le M}
 \left|m^2p_{n,R}(k,m,t)
       -\mathcal L_{m,R}(k_1,k_2,t,n)\right|
 \longrightarrow0.
\]

The inherited positive-error representation is

\[
 \limsup_m\sup_{R,n,k}
 \|P-G-m^2(b^{\varepsilon(B),\mathrm{inc}}
              +b^{\varepsilon(B),\mathrm{clr}})\|_\infty
 \le CB^{-1/192}.
\]

Revision 67 gives an ordered small-height estimate only for `b^{K,H}`, a positive part of the clearance source.

The complete incidence source and the positive complement remain in the formula. Positivity prevents cancellation from removing them.

Therefore the raw pointwise theorem cannot yet be deduced.

The integrated record law, full-space total variation, local `L^q` laws, positive lower law, good-set likelihoods, finite-width posteriors and coupled bridge theorems retain their prior scope. None converts an integrated or partial-source estimate into the missing unrestricted essential-supremum theorem.

## 21. Arithmetic modulation and exact labels

The uniform theorem continues to use the finite transition kernel

\[
 \mathcal L_{m,R}.
\]

At fixed radius the main term contains the actual finite residue

\[
 \mathfrak a_R(k,n,m),
\]

including zero classes.

Revision 67 neither proves residue triviality nor assigns conditional laws to a zero arithmetic denominator.

The new angular strata retain the original half-word label, occupation convention, displacement and terminal membership. There is no averaging of return index, collision count or displacement.

This is mathematically correct and should remain visible in every future title-level statement.

## 22. Novelty and significance

The relative angular absorption is nontrivial and tailored to the original Lorentz source. It advances the physical critical-source program beyond finite-width traces and fixed-count tangent limits.

Subject to specialist verification, the following package could form a valuable focused contribution:

- count-uniform selected-contact coordinates;
- exact nonlinear physical masks;
- finite-width positive collar comparison;
- relative angular stability;
- zero-width physical trace concentration on controlled strata; and
- original-source caustic-collar essential height.

At the requested top-four benchmark, however, the following factors remain decisive:

1. the title and architecture still center an unproved unrestricted pointwise endpoint;
2. the new theorem covers a condition-number stratum rather than the complete source;
3. the physical weighted tail is unproved;
4. the positive complement and complete incidence source remain open;
5. the article contains 145 tightly interdependent modules;
6. the hardest continuum inputs are highly model-specific; and
7. no independent expert audit has been obtained.

A top-four significance case would be materially stronger after the complete pointwise theorem is closed, or after the chart/trace/absorption mechanism is extracted as a general theorem with several independently verified singular-hyperbolic applications.

## 23. Independent specialist verification

No independent human specialist audit has been obtained.

For the new modules, the highest-priority checks are:

1. completeness of the primitive physical and section margin list on the selected disk;
2. the inherited statement that every active margin has nonzero gradient;
3. stability of every inactive sign under the stated radius;
4. preservation of first-hit and section conventions in the Boolean output;
5. guard saturation on the physical source and only there;
6. common coarea representatives for all exact labels;
7. the inherited relative density identity and Morse Jacobian;
8. use of the finite-width collar theorem on arbitrary subfamilies;
9. positivity of the absorption inequality;
10. the essential-supremum passage from atomic centers to roof density;
11. treatment of coincident critical values;
12. definition and measurability of the condition-number strata;
13. the physical weighting in `E(K)`;
14. the exact positive complement partition; and
15. all inherited anisotropic transfer-operator, arithmetic and source-normalization inputs.

The exact-source workflow, deterministic fixtures and native build do not replace this audit.

## 24. Required mathematical changes before another top-four review

A subsequent revision seeking the same benchmark should address the following.

### 24.1 Prove physical weighted tightness of the condition number

Establish

\[
 \lim_{K\to\infty}E(K)=0.
\]

A valid proof must use the physical weights `J_z theta`, exact labels and the collision limsup. Fixed-count finiteness or an unweighted word-count bound is insufficient.

A verified uniform moment estimate would suffice, but its hypotheses must be proved on the actual Lorentz source.

### 24.2 Control the positive complement

Prove an ordered essential-height estimate for

\[
 r^{\varepsilon,\chi,K,H}.
\]

This must include zero-tangent-fraction nonlinear source, selected grazing, failed incidence taper, noncritical rank pieces, non-seam centers, omitted annuli and every other uncovered physical class.

Small mass, small support or a finite-width estimate is insufficient.

### 24.3 Complete the first-incidence height

Use the incidence-normalized geometry, or a different argument, to prove the complete exact-label ordered incidence estimate required by the raw-error criterion.

The finite-count exponential inverse-incidence bound does not suffice.

### 24.4 Complete the clearance height

Combine the new stratum theorem, a proof of the physical tail, complement control, transverse and finite-type coarea, buffered caustics and all remaining physical pieces into one complete ordered clearance estimate.

### 24.5 Deduce the unrestricted pointwise theorem

Insert the complete incidence and clearance estimates into the established positive-error identity. Retain the finite arithmetic transition kernel and zero classes unless a separate residue theorem is proved.

### 24.6 Derive the unrestricted same-roof consequences

Only after the full pointwise theorem is proved should the paper claim unrestricted same-roof bridges, forward essential likelihood and pointwise roof-conditioned path laws.

### 24.7 Obtain independent specialist review

The physical margin description, selected-contact continuation, nonlinear profile, angular strata, inherited local law and complete positive source decomposition require expert human verification.

### 24.8 Complete two-ref qualification if it is claimed

The response branch has a successful exact-SHA run. The copy branch had no separate run at the time of this audit. Either run the qualification on that ref or describe the evidence as single-ref exact-source qualification.

### 24.9 Reduce the proof burden

A journal submission should expose the shortest complete route to one principal theorem. Historical front matter, source ledgers, validation material and unfinished alternative routes may remain in the repository without dominating the article.

### 24.10 Sharpen the generality claim only after verification

If a broader top-four route is sought, state a reusable angular-absorption theorem with quantitatively checkable hypotheses and verify the physical tail and complement in several genuinely different singular systems. The present Lorentz component theorem alone does not yet supply that breadth.

## 25. Technical and presentation comments

1. Keep the finite-width trace `Q`, physical zero-width trace `B`, and full reversible trace `T` distinct in every statement.
2. State explicitly whenever `K` is fixed before the collision limit.
3. Do not infer convergence uniform in `K` from a bound whose constant is independent of `K`.
4. Keep the local Boolean-description radius, inactive-sign radius and Morse-chart radius distinct.
5. State that `rho_z` may shrink with the collision count.
6. Keep translated inactive margins out of the homogeneous threshold estimate.
7. Preserve the distinction between absolute and relative angular error.
8. Retain the physical fraction `theta` in the condition number and atomic coefficient.
9. Do not replace the physical tail by an unweighted critical-word count.
10. Keep zero-tangent-fraction nonlinear source in the positive remainder.
11. State that exact-label vectors are one-hot only after the complete physical visit rule is evaluated.
12. Keep the image mark `j+1`, half-open occupation and separate terminal membership conventions visible.
13. Keep collar width `s`, roof height width `H`, reconstruction band `B`, incidence cap `chi` and stratum cutoff `K` distinct.
14. State whether an estimate is finite-count, collision-limsup, or ordered after an outer width limit.
15. Use common coarea representatives and retain “almost everywhere” in pointwise density statements.
16. Do not identify atomic concentration with essential height without the interval-of-centers argument.
17. Keep coincident critical values additive; do not assume separation.
18. State that selection of a positive subfamily does not establish complete source coverage.
19. Keep the complete source partition next to every partial height theorem.
20. Do not describe `E(K) -> 0` as proved or as a consequence of fixed-word exhaustion.
21. Keep the optional moment criterion explicitly conditional.
22. Do not infer complement height from angular-loss control.
23. Preserve the finite arithmetic transition kernel and zero classes.
24. Keep probability total variation, variation mass, path bounded-Lipschitz dual and essential-supremum density norms distinct.
25. Do not infer a pointwise bridge from integrated bridge convergence.
26. Keep workflow qualification separate from continuum proof certification.
27. Record that only the response ref had a successful run at the time of this review.
28. Preserve every false status flag until the corresponding complete theorem is actually proved.
29. Consider moving extensive provenance and validation discussion outside the journal narrative.
30. A future complete theorem should state one canonical sequence of limits rather than relying on readers to reconstruct it from several partial modules.

## 26. Final assessment

Revision 67 is a serious and mathematically coherent response to the revision-66 report.

It proves a correct-looking primitive angular estimate, converts it into a relative exact-label bound, absorbs that bound positively into the finite-width collar trace, and obtains ordered zero-width concentration on every fixed physical condition stratum. It then proves an original-source essential-height estimate for the corresponding caustic collars.

This is a genuine advance. I found no decisive error in modules 143--145.

The advance nevertheless remains stratified. The physical weighted condition-number tail is unproved, the nonlinear positive complement is unestimated, and the complete first-incidence height remains open. Therefore the complete clearance height and unrestricted pointwise raw-density theorem are not established.

The article also remains extraordinarily long, model-specific and dependent on continuum inputs which have not received independent specialist verification.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**

A focused specialist-journal paper centered on relative angular stability, positive absorption and zero-width critical traces could be valuable if the inherited geometry withstands expert audit. A future top-four submission should return only after the physical tail, complete complement and incidence source have been controlled in the correct ordered regime, or after the mechanism has been extracted and independently verified as a substantially broader theorem.