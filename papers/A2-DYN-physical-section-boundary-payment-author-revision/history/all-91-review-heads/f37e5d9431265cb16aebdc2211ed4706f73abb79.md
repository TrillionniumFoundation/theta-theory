# External top-four referee report on A2-DYN revision 69

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v69-referee-response-2026-10-10`, `revision/a2-dyn-v69-referee-copy-2026-10-10`  
**Reviewed commit:** `b959bbca34c35db82176c8f35bf029fec347e739`  
**Reviewed repository tree:** `d26634d9405dcd052b24a26ee8bef440839954bb`  
**Active manuscript directory:** `papers/A2-DYN-v69-referee-response`  
**Active mathematical source:** one hundred fifty-one numbered core modules; revision 69 retains all one hundred forty-eight revision-68 modules and adds modules 149--151  
**Frozen revision-68 author baseline:** `c8268a608a971c6832bcfed2a827af951e84c577`  
**Frozen revision-68 complete paper tree:** `dce4295d9d660f64e4d25bb0463045dddc546249`  
**Controlling external report:** `reviews/a2-dyn-v68-external-top4-review-2026-10-10/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `7fd1ca003cebd920e3f5a1f7af136e4c86cadcf4` / `6c2501c22189fb04ee565d844003a589c6272f07`  
**Date:** 10 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 69 is a genuine theorem-bearing advance over revision 68. The preceding report accepted the analytic angular-germ classification and the order-free annular estimate on fixed persistence strata, but identified three decisive gaps in the physical-source endpoint:

1. the old proof divided by a positive center value of the clearance guard and therefore did not cover zero-center or infinitely flat guards;
2. an inner analytic-germ collar did not control the source outside the certified germ disk or labels born only at positive radius; and
3. fixed-chart finiteness did not imply ordered weighted tightness after the parameter, label and collision-count suprema.

Revision 69 addresses the first two issues in a mathematically meaningful way and isolates the third in a more physical form.

The new source constructs an unguarded comparison density which removes only the clearance multiplier while retaining the actual physical itinerary, all first-hit tests, the exact one-hot label, the initial/occupation/terminal decisions, the next-collision mark and the original section normalization. It proves an ordered positive-width collar trace for this comparison source. Applying the original guard only as an absolute upper bound gives, on every fixed angular-persistence stratum,

```text
6 C H F_{chi,K}(H) min{1, delta + C_g epsilon^(-1) sqrt(2H)}.
```

In particular, the zero-center source has the additional gain

```text
6 sqrt(2) C C_g epsilon^(-1) H^(3/2) F_{chi,K}(H).
```

No analytic classification of the guard is used, so infinitely flat guards are genuinely included on the stated angular strata.

The second new mechanism replaces germ information by the exact physical angular occupation on a fixed radial interval. With

```text
V = (essential radial supremum of the angular fraction)
    / (its positive radial average),
```

the manuscript proves a complete interval height bound on each fixed `V <= T` stratum, including portions outside a germ disk and labels born only at positive radius. It also proves the correct conditional implication from a physically weighted `(1+alpha)` collar moment to a `T^(-alpha)` tail.

I audited the new modules

- `core/149_unguarded_physical_comparison.tex`;
- `core/150_absolute_guard_collar_height.tex`;
- `core/151_finite_scale_radial_coverage.tex`;

and their use in the revised front matter. I also checked the inherited exact physical chart and one-hot indicator in modules 140--141, the positive collar trace in module 142, the analytic angular classification and relative annular theorem in modules 146--148, the fixed-width exact-label local bound, the complete positive source partition, the source/status manifests, and both exact-SHA qualification runs.

I found no decisive counterexample, missing section factor, missing polar coarea cancellation, incorrect annular power, hidden division by a zero guard, target-count multiplier, word-count multiplier, reversal of the fixed-band order of limits, or deletion of the original positive source in the new three-module chain.

In particular, the following points are internally coherent.

1. The comparison source omits only a multiplier in `[0,1]`; it does not continue a nonphysical orbit or alter an exact label.
2. The physical angular density remains between the same relative Jacobian bounds because the clearance guard is not used in those bounds.
3. The direct comparison with the exact two-endpoint event gives one collar trace estimate for every positive subfamily, without a combinatorial factor.
4. The angular annulus comparison is uniform in every finite birth order because it uses monotonicity of `r^d`, not an upper bound on `d`.
5. An identically zero angular germ contributes zero inside its certified zero disk; it is not assigned an invented finite order.
6. The original guard is used only through its absolute Lipschitz estimate, so zero center values and infinitely flat guards are allowed.
7. The zero-center factor is `H * sqrt(H)`, hence `H^(3/2)` with the displayed `epsilon^(-1)` coefficient.
8. The shrinking-collar corollary follows by positive domination by every fixed collar before taking that fixed width to zero; it does not evaluate a spectral theorem at a width depending on the collision count.
9. The finite-scale ratio is defined from the actual measurable physical angular fraction, not from a Taylor polynomial.
10. The zero-average convention is legitimate because the angular fraction is nonnegative.
11. The whole fixed radial interval is controlled on the `V <= T` stratum with one positive collar average.
12. The high-ratio estimate is stated only as an implication from the displayed weighted physical moment and does not silently assume that moment is finite.
13. The source decomposition into `b_angular_inner + o69 + t69 + e69` is disjoint and positive.
14. The canonical pointwise budget retains the first-incidence source, the high-ratio source and the exterior source as explicit terms.
15. Every geometric cutoff is fixed before the collision-count limsup.

These are substantial improvements. The negative recommendation is therefore not based on a failure of the new restricted theorems.

The recommendation is forced by the unchanged endpoint of the paper.

Revision 69 does **not** prove the weighted radial moment which controls the high-`V` source. It does not prove the older angular-persistence or angular-condition tails. It does not control the exterior source `e69`, which still contains failed taper, selected grazing, noncritical-rank pieces, uncovered physical states and omitted outer annuli. The complete first-incidence height also remains open. The new theorems therefore enlarge the controlled positive source but do not establish complete source coverage.

Consequently revision 69 still does not prove

- the complete ordered first-incidence height;
- the complete ordered clearance height;
- the unrestricted two-sided pointwise arithmetic raw-density theorem;
- unrestricted same-roof collision and actual-return bridges;
- forward essential-likelihood convergence;
- or the unrestricted pointwise roof-conditioned path theorem.

These are not cosmetic corollaries. They are the hypotheses in the paper's own positive raw-error identity and the title-level endpoint around which a substantial part of the one-hundred-fifty-one-module architecture is organized.

At the requested benchmark, the article would need either

1. complete ordered control of the weighted radial/angular tails, the exterior clearance source and the first-incidence source, followed by the unrestricted pointwise theorem; or
2. a substantially broader theorem with quantitatively verifiable hypotheses and several genuinely different singular-hyperbolic realizations, so that the paper's significance no longer depends editorially on the unfinished Lorentz endpoint.

Revision 69 supplies neither yet. No independent human specialist audit has been obtained.

My assessment is therefore positive about the new physical comparison machinery and negative about readiness for *Annals*, *Acta*, *Inventiones* or *JAMS*.

## 2. Frozen source, chronology and preservation

Both reviewed author branches resolve to

`b959bbca34c35db82176c8f35bf029fec347e739`.

The repository tree is

`d26634d9405dcd052b24a26ee8bef440839954bb`.

The active article is

`papers/A2-DYN-v69-referee-response`.

The immediate mathematical baseline is revision 68 at

`c8268a608a971c6832bcfed2a827af951e84c577`.

The controlling report is the revision-68 report at

`7fd1ca003cebd920e3f5a1f7af136e4c86cadcf4`.

The final v69 author commit follows the frozen report state through the recorded revision checkpoints and lands a complete author manuscript. The source manifest records

- all one hundred forty-eight inherited core modules retained;
- every inherited Python source retained;
- all eight inherited appendices retained;
- the bibliography retained;
- every inherited compiled input and mathematical label retained;
- the revision-68 opening compiled in `appendices/v68_frontmatter.tex`;
- one hundred fifty-one active core modules;
- `lorentz_unguarded_physical_comparison_trace_proved: true`;
- `lorentz_absolute_guard_all_center_strata_height_proved: true`;
- `lorentz_zero_center_guard_strata_height_proved: true`;
- `lorentz_finite_scale_radial_strata_height_proved: true`;
- `lorentz_weighted_radial_tail_implication_proved: true`;
- `lorentz_angular_persistence_tail_proved: false`;
- `lorentz_radial_moment_bound_proved: false`;
- `lorentz_complete_zero_center_guard_height_proved: false`;
- `lorentz_complete_source_coverage_proved: false`;
- `grazing_boundary_pointwise_smallness_proved: false`;
- `clearance_boundary_pointwise_smallness_proved: false`;
- `full_raw_return_LLT_proved: false`;
- `pointwise_roof_density_LLT_proved: false`;
- and `independent_human_review: false`.

These flags accurately distinguish the new partial source theorems from the unproved complete endpoint.

The present review branch starts directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v69-external-top4-review-2026-10-10/`.

No author source, workflow, prior review, historical manuscript or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-SHA revision-69 qualification workflows completed successfully on both reviewed author refs:

- response branch run `38060559518`;
- referee-copy branch run `38060564078`.

Both runs use the reviewed SHA

`b959bbca34c35db82176c8f35bf029fec347e739`.

According to the validation record, the verifier checks

- the frozen complete revision-68 paper tree;
- the controlling revision-68 report blob;
- all inherited mathematical, Python, appendix and bibliography bytes;
- all one hundred fifty-one active core inputs;
- all inherited mathematical labels and compiled inputs;
- the effective inherited theorem/status map;
- declared metadata and front-matter changes;
- normal and optimized finite diagnostics;
- native TeX compilation without shell escape;
- stabilized references, duplicate-label checks, warning-free typesetting and proof-page rendering; and
- the actual checkout SHA and active source tree.

The new finite fixtures include very high monomial orders, zero-center flat guards, finite-scale later births, zero denominators, exact density-distortion inequalities, weighted-tail inequalities and disjoint source allocation. Negative controls reject guarded-annulus division, fixed-count exhaustion as ordered tightness, and mass-to-height substitution.

These checks are useful source, algebra and typesetting evidence. They do not certify

- completeness and disjointness of the selected physical chart restrictions;
- the continuum one-hot physical indicator;
- the inherited two-endpoint collar local bound;
- the analytic angular classification for every physical word;
- the new radial-moment estimate, which is not proved;
- the exterior clearance height;
- the complete first-incidence height;
- the unrestricted pointwise theorem;
- or independent human review.

The manuscript and validation file state this boundary accurately.

One source-governance defect should be corrected before the next review: `SPECIALIST_AUDIT_MAP.md` in the v69 directory is still titled “revision 68” and lists only the revision-68 audit questions. It does not identify the new obligations in modules 149--151, especially the event domination for the unguarded comparison, common coarea versions, the finite-scale ratio, and the weighted radial moment. This does not invalidate the mathematics, but it conflicts with the v69 packet's stated audit route.

## 4. Scope of this review

I did not attempt to re-prove all 151 core modules. The substantive audit concentrates on the new claims and the inherited statements they use directly:

1. the definition of the unguarded comparison source;
2. preservation of the actual physical itinerary and exact label;
3. the original section normalization;
4. the common coarea representative;
5. the relative physical-density bound after omitting the guard;
6. the absolute guard-Lipschitz comparison;
7. the direct comparison with the exact two-endpoint event;
8. disjointness and uniqueness of selected physical charts;
9. the absence of a word or label count in the collar trace;
10. the angular-only persistence certificate;
11. the zero-germ certified disk;
12. the all-order annular comparison;
13. the zero-center `H^(3/2)` gain;
14. the shrinking-collar monotonicity argument;
15. the finite-scale angular occupation ratio;
16. the zero-average convention;
17. the complete fixed radial interval theorem;
18. the physically weighted moment and tail transfer;
19. the disjoint source partition;
20. the canonical endpoint budget;
21. the fixed-band order of limits;
22. source preservation and workflow evidence; and
23. the remaining top-four endpoint.

The inherited modules outside this route are treated as a source-pinned baseline, not as independently recertified mathematics. Their load-bearing billiards, anisotropic-operator, arithmetic and physical-source claims retain the qualifications of the earlier reports.

## 5. The unguarded comparison source

Module 149 defines

```text
hat b_z,lambda(t_z+u)
 = integral tilde w_z(sqrt(2u) omega_phi)
            B_z,lambda(sqrt(2u) omega_phi) dphi.
```

This is the right object for the intended upper comparison. The original first-clearance source contains one additional factor `D_z^epsilon` taking values in `[0,1]`. Removing this factor does not remove the primitive first-hit tests because those tests remain in `B_z,lambda`; it does not remove the section endpoints, the occupation count, the displacement, the terminal decision or the exact label.

The distinction matters. A full reversible trace on a formal continuation could count directions which are not physical. The present comparison assigns zero weight whenever the selected continuation fails the physical indicator. Thus the comparison is larger than the guarded source but still a restriction of the original physical probability space.

The displayed profile

```text
exp(-K_chi r) J_z ell_z,lambda(r)
 <= hat b_z,lambda(t_z+u)
 <= exp(K_chi r) J_z ell_z,lambda(r)
```

is consistent with the inherited relative Jacobian bound and with

```text
integral B_z,lambda dphi = 2 pi ell_z,lambda.
```

There is no missing radial factor: the polar arclength `r` cancels the derivative of `r^2/2` in the coarea formula.

The absolute guard estimate

```text
b_z,lambda^epsilon,clr(t_z+u)
 <= min{1, g_z + C_g epsilon^(-1) sqrt(2u)}
       hat b_z,lambda(t_z+u)
```

is also correctly oriented. It uses only positivity and the original Lipschitz guard. In particular it remains meaningful at `g_z=0` and does not presume a finite Taylor order for the guard.

The specialist check is geometric rather than algebraic: the indicator called `B_z,lambda` must contain every physical decision which can change the exact event, and the selected chart restrictions must remain disjoint after the guard is removed. The manuscript states these properties through the inherited construction; the finite tests do not establish them.

## 6. The ordered comparison collar trace

For a positive subfamily of selected charts, the manuscript averages the unguarded source over `0<u<s` and places the mass at the critical value `t_z`. The key comparison is

```text
s hat Q([a,a+w])
 <= nu_R^*( exact event with roof in [a,a+w+s]
             and two endpoint strips of width C sqrt(s) ).
```

This is structurally sound. The selected chart source has the same exact initial, occupation, terminal and displacement constraints as the event on the right. Removing the guard can only add physical points. Distinct physical itineraries are disjoint, and the selected normal critical point is unique within its word.

The inherited two-strip local upper bound then gives

```text
limsup_m sup m^2 hat Q([a,a+w]) <= C(w+s).
```

The two endpoint strips each have width of order `sqrt(s)`, so the source event contributes the required factor `s` before division by the collar width. No word count or label count is needed because the comparison is made after summing a disjoint physical source.

The order of quantifiers is correct: `s` and `w` are fixed before the collision-count limit. The theorem is not used with `s=s_m` inside the spectral estimate.

The statement that the constant is independent of the chart subfamily is credible only because the comparison is to one positive event. This should remain explicit in every later use; an arbitrary sign-changing selector would not enjoy the same argument.

## 7. The angular-only persistence certificate

Module 150 removes the guard from the persistence number. For a nonzero analytic angular germ it keeps the certified radius and relative angular remainder. For an identically zero germ it records only a zero disk. This is the correct separation.

An identically zero germ need not remain zero outside its certified disk. The manuscript does not make that inference. The condition

```text
p^a <= K,  2 K sqrt(H) < 1
```

places the entire inner and outer annuli inside the certified disk when the germ is zero.

For a nonzero germ, the relative bounds

```text
(1-Kr) eta r^d <= ell(r) <= (1+Kr) eta r^d
```

hold on the same disk. The inner radius is at most `sqrt(2H)` and the outer annulus has radius between `sqrt(2H)` and `2 sqrt(H)`. Hence the manuscript obtains the factor

```text
F_chi,K(H)
 = exp((2+sqrt(2)) K_chi sqrt(H))
   (1+sqrt(2)K sqrt(H))/(1-2K sqrt(H)).
```

The computation is correct. The comparison constant does not depend on `d`, because `r^d` is monotone and both inner and outer estimates use the common scale `(2H)^(d/2)`.

This is an important improvement over a proof which would sum constants depending on an unbounded birth order.

## 8. Absolute guard control and the zero-center gain

The original source is bounded by the unguarded source times

```text
min{1, delta + C_g epsilon^(-1) sqrt(2H)}
```

on the small-center class. Combining the all-order annular comparison with the trace bound on critical centers in `[t-H,t]` gives

```text
H(b^a,K,H;<=delta)
 <= 6 C H F_chi,K(H)
      min{1, delta + C_g epsilon^(-1) sqrt(2H)}.
```

The factor six is consistent: the pointwise annular comparison costs two, while the trace of a center interval of length `H` with collar width `2H` costs `3 C H`.

At `delta=0`, the guard contributes `C_g epsilon^(-1) sqrt(2H)`, so the height is proportional to `epsilon^(-1) H^(3/2)`. This conclusion genuinely includes an infinitely flat guard, because the proof uses no lower derivative and no analytic expansion of the guard.

The theorem remains a stratum theorem. It requires the angular certificate `p^a <= K`; it does not prove that the complement of this certificate has small ordered height.

## 9. Shrinking collars

The corollary allowing an arbitrary deterministic sequence `H_m -> 0` is logically valid in its stated fixed-stratum setting.

For every fixed admissible `H`, eventually `H_m < H`, and the positive source restricted to the smaller collar is dominated by the source in the fixed collar. Therefore

```text
limsup_m sup m^2 ||b^{a,K,H_m}||_infinity
 <= H(b^{a,K,H}).
```

The right side tends to zero as `H -> 0` at fixed `K`, `chi` and `epsilon`. This proves the corollary without evaluating the collar trace at a moving width.

The same argument would fail if the chart family or the persistence cutoff depended on `m`. The manuscript correctly forbids such a choice.

## 10. The finite-scale radial ratio

Module 151 defines, on a fixed radial interval,

```text
A(S) = S^(-1) integral_0^S L(u) du,
U(I) = ess sup_{u in I} L(u),
V(I,S) = U(I)/A(S).
```

Here `L` is the actual physical angular fraction. Since `0 <= L <= 1`, `V` is finite for every fixed chart with positive average. If the average is zero, nonnegativity implies `L=0` almost everywhere on the whole averaging interval, so setting `V=0` introduces no source on `I`.

The comparison

```text
ess sup_{u in I} b_z,lambda^epsilon,clr(t_z+u)
 <= exp(K_chi(sqrt(2b)+sqrt(2S)))
    V(I,S)
    min{1,g_z+C_g epsilon^(-1)sqrt(2b)}
    hat q_z,S;lambda
```

follows directly from the upper and lower physical Jacobian bounds. Unlike the germ theorem, it does not require analytic root ordering on the whole interval.

This is useful because it includes later positive-radius births and source outside a certified germ disk. It is nevertheless a ratio theorem: a narrow angular spike can make `V` arbitrarily large while leaving the average small.

## 11. Height on a complete fixed radial interval

On the stratum `V <= T`, summing the comparison over centers contributing to a roof value and applying the same positive collar trace yields

```text
H(b^{I,S,V<=T;<=delta})
 <= C T exp(K_chi(sqrt(2b)+sqrt(2S)))
    min{1,delta+C_g epsilon^(-1)sqrt(2b)}
    (b-a+S).
```

For `I=(0,S)` this becomes

```text
H(b^{(0,S),S,V<=T})
 <= 2 C T S exp(2 K_chi sqrt(2S)).
```

The interval theorem is genuinely stronger than an inner-germ statement on its selected stratum. It covers the entire chosen radial range. It also keeps the averaging width fixed before the collision limit.

The theorem does not say that most of the source has bounded `V`. That is the remaining tail problem.

## 12. The weighted radial moment

The manuscript introduces

```text
M_alpha(S)
 = limsup_m sup_{R,lambda,t} m^2
   sum_{z:t_z in [t-S,t]}
   V_z(S)^(1+alpha) hat q_z,S;lambda.
```

This is the correct type of physical weighting. It is not an unweighted count of words and therefore avoids the most obvious combinatorial obstruction. The tail estimate

```text
H(b^{V>T})
 <= exp(2 K_chi sqrt(2S)) T^(-alpha) M_alpha(S)
```

is an immediate and correct Markov-type consequence.

However, the proposition is conditional in the decisive sense: the manuscript supplies no finite bound for `M_alpha(S)`, uniformly in the exact labels, radius and collision count. The moment contains essentially the concentration information needed to exclude narrow angular spikes. Fixed-chart finiteness of `V` gives no control of this ordered moment.

A future revision must prove this moment, or an equivalent tail estimate, from the physical geometry and dynamics. Merely renaming the tail as a moment would not advance the endpoint.

## 13. The complete positive source partition

The manuscript gives the disjoint decomposition

```text
b_clr = b^{a,K,H} + o69 + t69 + e69.
```

The meanings are clear.

- `b^{a,K,H}` is the angular-certified inner collar.
- `o69` is the remaining source below radius `S` whose chart-label ratio satisfies `V <= T`.
- `t69` is the remaining source below `S` with `V > T`.
- `e69` contains every point not yet assigned, including the original outside source and source at offsets at least `S`.

All four terms are positive restrictions of the original first-clearance source. Zero-center source is allocated rather than deleted. Removing an overlap from the `V <= T` source only decreases its height, so the stated bound for `o69` is legitimate. Likewise `t69` is dominated by the complete high-`V` source.

The resulting endpoint budget is

```text
E_M <= C_M B^(-1/192)
       + H(b_inc)
       + 6 C H F_chi,K(H)
       + 2 C T S exp(2 K_chi sqrt(2S))
       + H(t69) + H(e69).
```

This budget is mathematically honest. It does not set the last three physical obligations to zero.

It also shows precisely why the top-four endpoint remains open. One must choose `H` and `S` small, `K` and `T` large, and control the corresponding tails in an order compatible with the fixed-band collision limit. No such complete parameter selection is presently proved.

## 14. The complete first-incidence source

The first-incidence term remains independent of the clearance analysis.

The inherited inverse-incidence theorem gives a finite-count density estimate with an exponential collision-count constant. That result is nontrivial, but it does not imply

```text
lim_{B -> infinity} limsup_{m -> infinity}
  sup m^2 ||b_inc^{epsilon(B)}||_infinity = 0
```

in the fixed-band order required by the raw inversion.

Revision 69 correctly leaves this term visible. The title-level pointwise theorem cannot be declared complete until this source is controlled on the original exact labels.

## 15. What revision 69 closes

Relative to revision 68, the manuscript closes several real issues.

- The guard is removed from the annular denominator.
- Zero-center guards are treated without division.
- Infinitely flat guards are included on the angular strata.
- Arbitrarily small positive center guards require no separate cutoff.
- Every finite angular birth order has the same annular constant.
- The zero-center source gains an additional square root of the collar width.
- The comparison trace keeps the unchanged physical record and exact labels.
- Source beyond a germ disk can be treated on finite-scale physical ratio strata.
- Positive-radius births of a zero germ can enter the finite-scale theorem.
- The high-ratio obstruction is expressed through a physically weighted moment rather than an unweighted word count.
- The complete clearance source is partitioned disjointly with no deleted positive remainder.

These are meaningful advances in the physical-source analysis.

## 16. What revision 69 does not close

The following remain open.

1. Ordered tightness of the angular-only persistence certificate.
2. The older angular-condition tail.
3. Finiteness of the weighted radial moment `M_alpha(S)`.
4. Essential-height control of the high-`V` source.
5. Essential-height control of the exterior source `e69`.
6. Complete first-incidence height.
7. Complete ordered clearance height.
8. The unrestricted two-sided pointwise raw-density theorem.
9. Unrestricted same-roof bridge convergence.
10. Forward essential-likelihood convergence.
11. The unrestricted pointwise roof-conditioned path theorem.
12. Independent expert verification of the inherited and new continuum chain.

Small support or small mass of any remaining source would not by itself prove its essential-height smallness.

## 17. Top-four significance and architecture

If the full inherited chain is correct, A2-DYN contains a large and technically impressive body of specialist mathematics: exact arithmetic return kernels, complete mixed-record total variation, bridge laws, positive source decompositions, caustic localization, analytic angular births, all-order annular estimates, and now absolute-guard and finite-scale physical comparisons.

The present article nevertheless remains difficult to assess as a top-four submission for three reasons.

First, its title and principal raw-inversion architecture continue to center an unrestricted pointwise theorem which is explicitly unproved.

Second, the hardest new inputs remain specific to one triangular finite-horizon Lorentz family and a long sequence of paper-specific constructions. The conditional weighted-moment transfer is not yet a broader theorem with independently verifiable hypotheses in several systems.

Third, the source contains 151 mathematical modules plus extensive historical, provenance and validation material. The new journal route is useful, but the proof burden remains far beyond what can be justified by an incomplete endpoint.

A focused paper centered on the proved comparison trace, zero-center height theorem and finite-scale source decomposition could be valuable in a specialist dynamics/probability venue after expert verification. At the requested benchmark, the complete positive-source endpoint or a genuinely broader theorem is still required.

## 18. Independent specialist verification

No independent human specialist audit has been obtained.

For modules 149--151, the highest-priority checks are:

1. the comparison density must be the pushforward of the actual selected physical source with only the clearance multiplier omitted;
2. the one-hot indicator must include every primitive physical and section decision;
3. selected physical chart restrictions must be disjoint after omission of the guard;
4. the two-endpoint comparison event must contain the complete comparison collar with the claimed endpoint widths;
5. the inherited two-strip local estimate must be applicable uniformly to that event and exact label;
6. common coarea versions must support all almost-everywhere sums and essential suprema;
7. the analytic angular radius and relative remainder must be correct for every selected physical word;
8. the zero-germ disk must not be used outside its certified radius;
9. the finite-scale ratio must use the actual physical angular fraction on the full interval;
10. the collar average in the denominator must be positive precisely when source is present;
11. the complete source partition must be measurable, disjoint and exhaustive;
12. the high-ratio moment must not be assumed finite; and
13. no parameter depending on the collision count may enter the fixed-band limsup.

The inherited anisotropic spectral theory, first-defect construction, exact arithmetic kernel, caustic geometry and bridge transfer remain separate audit obligations.

Source qualification and finite profile checks do not replace these continuum verifications.

## 19. Required mathematical changes before another top-four review

### 19.1 Prove the weighted radial tail

Establish a finite bound for `M_alpha(S)`, or an equivalent ordered tail estimate, on the original physical source uniformly in the radius and exact labels.

The proof must use the collar weights and must survive the collision-count limsup. Fixed-word finiteness and unweighted word counts are insufficient.

### 19.2 Control the exterior clearance source

Prove that the source `e69` has vanishing ordered central height under a legal sequence of cutoffs. This includes failed taper, selected grazing, noncritical-rank pieces, uncovered states and omitted outer annuli.

The source may be repartitioned positively, but no roof values may be deleted and no mass estimate may be substituted for a height estimate.

### 19.3 Control the complete first-incidence height

Upgrade the finite-count inverse-incidence estimate to the fixed-band ordered central-scale estimate required by the positive raw-error identity.

### 19.4 Complete the pointwise theorem

Combine the previous estimates with the existing band error and finite arithmetic kernel to prove the unrestricted two-sided pointwise law on the original exact return record.

Arithmetic zero classes must remain in the theorem unless the separate residue criterion is proved.

### 19.5 Deduce same-roof consequences only after full source closure

Unrestricted same-roof bridges, essential likelihood and pointwise roof-conditioned path laws should be deduced only after the scalar pointwise denominator and complete source height are available.

### 19.6 Obtain independent specialist review

The selected-contact chart, exact one-hot physical indicator, positive comparison event, coarea representatives, weighted moment and inherited two-strip local bound require human review by experts in dispersing billiards and anisotropic transfer operators.

### 19.7 Repair the audit metadata

Replace the stale revision-68 `SPECIALIST_AUDIT_MAP.md` with a revision-69 map covering modules 149--151. Ensure every status, route, manifest and validation file identifies the same active revision and reviewed SHA.

### 19.8 Reduce the journal proof burden

Present the shortest complete proof of one principal endpoint. Historical modules and operational evidence may remain archived, but they should not dominate the mathematical narrative submitted to a journal.

### 19.9 Sharpen the literature comparison

Explain theorem by theorem which exact-label, density-height, arithmetic and source-tail statements are unavailable from existing Lorentz-process, billiard endpoint-LLT and suspension-flow local-limit frameworks after checking their hypotheses.

## 20. Technical and presentation comments

1. Keep `b`, `hat b`, the guarded trace, the unguarded comparison trace and the full reversible trace notationally distinct.
2. State whenever a comparison removes only the clearance multiplier and retains all physical decisions.
3. Keep the exact label `lambda=(n,k)` visible in the definitions of `L`, `A`, `U`, `V` and the weighted moment.
4. Specify the common coarea representative before taking an essential supremum over roofs.
5. Retain the factor `2 pi` in the angular fraction normalization.
6. Keep the polar cancellation explicit so that no reader inserts an erroneous radial power.
7. State that `g_z` may vanish and that no division by `g_z` occurs.
8. Keep the guard Lipschitz constant `C_g epsilon^(-1)` visible.
9. State that an infinitely flat guard is allowed only because the proof uses absolute domination, not a finite-order expansion.
10. Keep the angular certificate independent of the collar width `H`.
11. Keep `2K sqrt(H)<1` and `2H<h_chi` adjacent to the annular theorem.
12. Do not replace an identically zero germ by a zero source outside its certified disk.
13. State that every finite birth order is summed at fixed collision count before the limsup.
14. Keep the fixed-width interpretation of the comparison collar theorem explicit.
15. Do not call the shrinking-collar corollary a moving-band spectral estimate.
16. In the finite-scale theorem, state that `V` is a chart-label quantity, not a pointwise orbit observable.
17. Keep the `A=0` convention and its nonnegative-Fubini justification.
18. Distinguish a verified geometric upper/lower certificate for `V` from its mere fixed-chart finiteness.
19. Keep the finite-scale interval and averaging collar fixed before the collision limit.
20. Do not infer a high-`V` tail from the fact that every individual `V` is finite.
21. State prominently that `M_alpha(S)` is allowed to be infinite.
22. Keep the physically weighted moment distinct from an unweighted count of words.
23. Retain the exact disjoint source identity near every endpoint budget.
24. Keep `t69` and `e69` positive and visible; do not absorb them into an unnamed error.
25. State which classes are contained in `e69`.
26. Keep the first-incidence source separate from the clearance source.
27. Preserve the fixed-band order: choose geometric parameters, then take the collision limsup, then make outer choices.
28. Do not choose `K`, `T`, `H` or `S` as functions of the collision count inside the proved statements.
29. Keep arithmetic zero classes in every pointwise formulation.
30. Distinguish essential-height convergence from local `L^1`, total variation and weak-integrability statements.
31. Do not infer height from small support or small source mass.
32. Keep probability total variation, variation density and path bounded-Lipschitz dual norms distinct.
33. State that the unguarded comparison is not the full reversible atomic trace.
34. Update the specialist audit map to the active revision.
35. Keep exact-SHA qualification separate from mathematical proof certification.
36. Consider moving the extensive validation and historical material outside the journal-facing narrative while preserving it in the repository.

## 21. Final assessment

Revision 69 is a serious and mathematically coherent response to the revision-68 report.

It introduces the correct unguarded physical comparison source, proves a uniform ordered collar trace for every positive subfamily, removes the relative guard denominator, includes zero-center and infinitely flat guards, obtains the `epsilon^(-1) H^(3/2)` zero-center gain, and extends the source-height analysis beyond analytic-germ disks through a finite-scale physical ratio.

The exponent and normalization bookkeeping in modules 149--151 is internally consistent. I found no decisive error in the new restricted theorems.

The advance is nevertheless a partial source theorem. The weighted radial moment is not proved, the high-ratio and exterior sources remain uncontrolled, and the complete first-incidence height remains open. The unrestricted pointwise arithmetic raw-density theorem and its same-roof consequences therefore remain unproved.

The article also remains exceptionally long, highly model-specific and dependent on continuum inputs which have not received independent specialist verification.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**

A future top-four review should begin only after the complete ordered physical tails and first-incidence source are controlled, or after the comparison mechanism is elevated to a broader independently verified theorem whose significance does not depend on the unfinished Lorentz endpoint.
