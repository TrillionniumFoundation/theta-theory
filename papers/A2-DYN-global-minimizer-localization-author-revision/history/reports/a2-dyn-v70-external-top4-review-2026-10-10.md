# External top-four referee report on A2-DYN revision 70

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v70-referee-response-2026-10-10`, `revision/a2-dyn-v70-referee-copy-2026-10-10`  
**Reviewed commit:** `9eb04448ca20772c99c500b406a62bca1d2172c7`  
**Reviewed repository tree:** `a87fa837043bd4e8cc8477821fc0bb0a4a49ed79`  
**Active manuscript directory:** `papers/A2-DYN-v70-referee-response`  
**Active mathematical source:** one hundred fifty-four numbered core modules; revision 70 retains all one hundred fifty-one revision-69 modules and adds modules 152--154  
**Frozen revision-69 author baseline:** `b959bbca34c35db82176c8f35bf029fec347e739`  
**Frozen revision-69 complete paper tree:** `8209e73091651e5e95eebec221b1f0517a5d4863`  
**Controlling external report:** `reviews/a2-dyn-v69-external-top4-review-2026-10-10/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `f37e5d9431265cb16aebdc2211ed4706f73abb79` / `88ee6f3f4271119c39aaa84420db8f2446940ff6`  
**Date:** 10 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 70 is a genuine theorem-bearing advance over revision 69. The controlling report accepted the new physical comparison collar and finite-scale radial decomposition, but identified three decisive unresolved source-height terms:

1. the high radial/angular loss inside the selected physical charts;
2. the original clearance source outside those selected charts; and
3. the complete first-incidence source.

Revision 70 makes a mathematically meaningful improvement to the first of these issues. It observes that a large radial supremum-to-average ratio can arise from rapid angular growth rather than angular disappearance. It therefore replaces the radial-ratio cutoff by an exact positive overlap weight on the original physical source. The resulting theorem controls a canonical part of every selected chart without assuming a radial moment, an angular birth-order bound, or a radial-ratio cutoff.

The new manuscript proves, in particular, that the complete overlap component on every selected Morse disk has ordered height

```text
H(s70) <= C chi^6.
```

With the legally ordered fixed-band choice

```text
varepsilon(B) = A0 B^(-1/12),
chi(B) = sqrt(varepsilon(B)),
```

this gives the new contribution

```text
H(s70) = O(B^(-1/4)).
```

The manuscript also proves a finite-word bounded-variation theorem for the actual angular occupation and identifies its distributional radial derivative as a signed physical boundary current. Atomic angular deaths are retained, and the negative radial current controls loss to an outer collar.

I audited the new modules

- `core/152_finite_scale_angular_overlap.tex`;
- `core/153_signed_radial_boundary_current.tex`;
- `core/154_whole_chart_source_budget.tex`;

and their direct inherited inputs in modules 140--151. I also checked the revised front matter, proof ledger, source manifest, specialist audit map, validation protocol, exact-SHA workflow runs, and the complete positive source identity.

I found no decisive counterexample, missing section normalization, polar coarea error, incorrect overlap factor, hidden radial-ratio assumption, missing exact-label restriction, word-count multiplier, invalid collision-count-dependent cutoff, incorrect sign in the radial current, or arithmetic error in the `B^(-1/4)` rate.

In particular, the following points are internally coherent.

1. The overlap coefficient is the maximal scalar coefficient allowed by the two angular capacities; it is not presented as an orbit transport.
2. Multiplication by the overlap and deficit coefficients is a partition of positive weights on the same source, not a false disjoint-event partition.
3. The `L=0` convention changes no source because the physical density vanishes almost everywhere on those levels.
4. The ordered overlap estimate uses one positive collar trace after summing the physical source, so no word or exact-label count appears.
5. The factors `d/(d-c)` and `b-a+d` arise from the receiving average and the center interval plus collar width, respectively.
6. The two relative-Jacobian exponents are combined correctly.
7. The no-loss corollary includes nondecreasing angular occupation, positive-radius births, zero-center guards, and infinitely flat guards within its stated class.
8. The bounded-variation identity uses the distributional derivative and retains radial jump atoms.
9. The negative part is taken only after the signed physical current is radially projected, preserving cancellations.
10. The whole selected disk is allocated: no additional selected-disk annulus is hidden in the outside source.
11. The exponent calculation `chi^6 = varepsilon^3 = O(B^(-1/4))` is correct.
12. Every geometric choice is fixed before the collision-count limsup.

These are substantial improvements. The negative recommendation is therefore not based on failure of the new restricted theorems.

It is forced by the unchanged endpoint of the paper.

The complete source identity is now

```text
b_clr = s70 + d70 + e70,
```

where only `s70` has a proved ordered height. The term `d70` is the angular-loss component inside the selected disks, and `e70` is the original physical source outside those disks. The complete first-incidence source remains separate. Thus the pointwise error budget still contains

```text
H(b_inc) + H(d70) + H(e70).
```

No one of these three quantities is proved to vanish in the required ordered regime.

Finite-word bounded variation does not provide a collision-uniform weighted negative-current estimate. Complete allocation of selected annuli does not make their loss component small. The outside source still contains failed taper, selected grazing, noncritical roof-rank pieces, and uncovered physical states. The inherited first-incidence estimate still has an exponential collision-count constant and cannot be inserted into the fixed-band limit.

Consequently revision 70 still does not prove

- the complete ordered first-incidence height;
- the complete ordered clearance height;
- the unrestricted two-sided pointwise arithmetic raw-density theorem;
- unrestricted same-roof collision and actual-return bridges;
- forward essential-likelihood convergence; or
- the unrestricted pointwise roof-conditioned path theorem.

These are not secondary editorial details. They are the explicit remaining hypotheses in the paper's own positive raw-error identity and the title-level endpoint around which a substantial part of the one-hundred-fifty-four-module architecture is organized.

At the requested benchmark, the article would need either

1. complete ordered control of `H(b_inc)`, `H(d70)`, and `H(e70)`, followed by the unrestricted pointwise theorem; or
2. a substantially broader theorem with quantitatively verifiable hypotheses and several genuinely different singular-hyperbolic realizations, so that the paper's significance no longer depends editorially on the unfinished Lorentz endpoint.

Revision 70 supplies neither endpoint yet. No independent human specialist audit has been obtained.

My assessment is therefore positive about the new source comparison and negative about readiness for *Annals*, *Acta*, *Inventiones*, or *JAMS*.

## 2. Frozen source, chronology, and preservation

Both reviewed author branches resolve to

`9eb04448ca20772c99c500b406a62bca1d2172c7`.

The repository tree at that commit is

`a87fa837043bd4e8cc8477821fc0bb0a4a49ed79`.

The active article is

`papers/A2-DYN-v70-referee-response`.

The immediate mathematical baseline is revision 69 at

`b959bbca34c35db82176c8f35bf029fec347e739`.

The controlling report is the revision-69 report at

`f37e5d9431265cb16aebdc2211ed4706f73abb79`.

The chronology is correct. Revision 70 begins from the frozen revision-69 report state, preserves the complete revision-69 author tree, and lands a new complete manuscript rather than relabeling a review commit or an incomplete checkpoint.

The source manifest records

- all one hundred fifty-one inherited core modules byte-identical;
- all two hundred three inherited Python sources byte-identical;
- all nine inherited appendices byte-identical;
- `references.tex` byte-identical;
- every inherited compiled input and mathematical label retained;
- the revision-69 opening retained in a compiled appendix;
- one hundred fifty-four active core modules;
- `lorentz_finite_scale_overlap_height_proved: true`;
- `lorentz_no_radial_loss_inner_height_proved: true`;
- `lorentz_fixed_word_radial_BV_proved: true`;
- `lorentz_signed_physical_boundary_current_identity_proved: true`;
- `lorentz_whole_chart_overlap_height_proved: true`;
- `lorentz_overlap_band_rate_proved: true`;
- `lorentz_ordered_angular_loss_height_proved: false`;
- `lorentz_radial_moment_bound_proved: false`;
- `lorentz_complete_source_coverage_proved: false`;
- `grazing_boundary_pointwise_smallness_proved: false`;
- `clearance_boundary_pointwise_smallness_proved: false`;
- `full_raw_return_LLT_proved: false`;
- `pointwise_roof_density_LLT_proved: false`;
- `unrestricted_same_roof_pair_bridge_proved: false`;
- `forward_essential_likelihood_convergence_proved: false`; and
- `independent_human_review: false`.

These flags accurately distinguish the new scoped theorems from the unproved complete endpoint.

The present review branch starts directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v70-external-top4-review-2026-10-10/`.

No author source, workflow, prior review, historical manuscript, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-SHA revision-70 qualification workflows completed successfully on both reviewed author refs:

- response branch run `38064507660`;
- referee-copy branch run `38064803063`.

Both runs use the reviewed SHA

`9eb04448ca20772c99c500b406a62bca1d2172c7`.

According to the validation protocol, the verifier checks

- the frozen complete revision-69 paper tree;
- the controlling revision-69 report blob;
- all inherited core, Python, appendix, bibliography, input, and label bytes;
- all one hundred fifty-four active core inputs;
- the complete inherited boolean status map;
- the exact archived opening text;
- normal and optimized finite diagnostics;
- native TeX compilation without shell escape;
- stabilized references, duplicate-label checks, warning-free typesetting, and proof-page rendering; and
- the actual checkout SHA and active source tree.

The new finite diagnostics cover zero angular capacity, full/no/partial overlap, monotone high-ratio profiles, later births, jump losses invisible to classical derivatives, signed-current cancellation, coincident-interface attribution, density distortion, complementary source weights, and the legal fixed-band parameter choice. Negative controls reject treating the weight partition as a disjoint event partition and reject treating a narrow disappearing angular spike as loss-free.

These checks are useful source, algebra, and typesetting evidence. They do not certify

- completeness of the physical one-hot mask;
- disjointness of the selected physical chart restrictions after only the clearance multiplier is omitted;
- the inherited two-endpoint comparison collar theorem;
- common coarea versions through all source sums and essential suprema;
- the restricted-analytic description of every physical decision at a fixed word;
- a collision-uniform weighted negative-current estimate;
- the outside-source height;
- the complete first-incidence height;
- the unrestricted pointwise theorem; or
- independent human review.

The manuscript and its validation files state this boundary accurately.

## 4. Scope of this review

I did not attempt to re-prove all one hundred fifty-four core modules. The substantive audit concentrates on the new claims and the inherited statements they use directly:

1. the exact physical angular fraction for one fixed exact label;
2. the common coarea representatives;
3. the unguarded comparison density;
4. the relative physical Jacobian bounds;
5. the original guard's absolute Lipschitz envelope;
6. the ordered positive comparison collar trace;
7. arbitrary positive chart subfamilies;
8. the maximal scalar overlap coefficient;
9. the angular deficit identity;
10. the complementary positive source weights;
11. the factors in the ordered overlap estimate;
12. the no-loss inner-collar corollary;
13. positive-radius births and zero-center guards;
14. the restricted-analytic physical angular set;
15. finite perimeter and bounded variation at fixed word;
16. the signed reduced-boundary current;
17. radial projection and negative variation;
18. the triangular kernel in the loss formula;
19. atomic radial deaths;
20. whole selected-disk allocation;
21. the original outside source;
22. the `chi^6` height;
23. the fixed-band `B^(-1/4)` rate;
24. the remaining three-height endpoint;
25. source preservation and exact-SHA evidence; and
26. the requested top-four significance standard.

The inherited modules outside this route are treated as a source-pinned baseline, not as independently recertified mathematics. Their load-bearing billiards, anisotropic-operator, arithmetic, critical-geometry, and physical-source claims retain the qualifications of the earlier reports.

## 5. The scalar angular overlap

For one selected chart and one exact label, the manuscript defines

```text
a_J(u) = average over v in J of min(1, L(v)/L(u))
```

when `L(u)>0`, and sets `a_J(u)=1` when `L(u)=0`.

This is a useful and mathematically correct scalar construction. For fixed `u,v`, it is the largest coefficient in `[0,1]` satisfying

```text
L(u) a <= L(v).
```

Multiplication by `L(u)` gives

```text
L(u) a_J(u) = average min(L(u),L(v)),
L(u)(1-a_J(u)) = average (L(u)-L(v))_+.
```

The convention at `L(u)=0` is harmless. The physical density contains the same angular indicator with bounded remaining weights, so it vanishes for almost every such roof level.

The manuscript correctly warns that this scalar capacity identity does not mean that angular sets are nested and does not construct a physical orbit joining two radial levels.

The resulting source split

```text
s = a_J b,
d = (1-a_J) b
```

is an exact decomposition of positive weights on the unchanged physical probability space. It is not a partition into disjoint physical events. This distinction is maintained in the theorem statements, proof ledger, finite diagnostics, and source manifest.

I find no error in this construction.

## 6. The ordered overlap-height theorem

The key estimate begins from the inherited physical profile and absolute guard bound. On a source interval `I=(a,b)`, for a subfamily with center guard at most `delta`, one has

```text
b_z(t_z+u)
 <= exp(K_chi sqrt(2b)) J_z W_delta(b) L_z(u).
```

Multiplication by the overlap coefficient gives

```text
b_z a_J
 <= exp(K_chi sqrt(2b)) J_z W_delta(b)
    average_J min(L_z(u),L_z(v)).
```

Dropping the first entry of the minimum bounds this by the average of `L_z(v)` over `J=(c,d)`. The lower inherited physical-density bound on `(0,d)` gives

```text
average_J L_z(v)
 <= exp(K_chi sqrt(2d)) [d/(d-c)] J_z^(-1) q_hat(z,d).
```

The cancellation of `J_z` is correct. The relative distortion factor is therefore

```text
exp(K_chi (sqrt(2b)+sqrt(2d))).
```

At a fixed roof, contributing chart centers lie in an interval of length `b-a`. The inherited collar theorem with collar width `d` gives a bound proportional to

```text
b-a+d.
```

Thus the displayed theorem

```text
H(s^{I,J;<=delta})
 <= C [d/(d-c)] (b-a+d)
      exp(K_chi(sqrt(2b)+sqrt(2d))) W_delta(b)
```

has the correct factors.

Three aspects are important.

First, the theorem is count-uniform in the ordered height because the comparison is made with one positive physical event after the charts have been summed. It does not sum a per-word estimate.

Second, the theorem permits an arbitrary positive chart subfamily. The proof does not require a spectral estimate for its selecting insertion; positive event domination is used instead.

Third, no radial-ratio cutoff, angular-germ order, or weighted radial moment appears.

Subject to specialist verification of the inherited physical mask, chart disjointness, and comparison collar theorem, I find this argument internally sound.

## 7. The no-angular-loss corollary

For `I=(0,H)` and `J=(H,2H)`, assume

```text
L(u) <= L(v)
```

for almost every pair `(u,v)` in the indicated product. Fubini then makes the angular deficit zero for almost every `u` in the inner interval, so the overlap component equals the entire original inner source.

Substitution in the general theorem gives

```text
d/(d-c) = 2,
b-a+d = 3H,
```

and hence the factor `6H`.

The distortion exponent

```text
(2+sqrt(2)) K_chi sqrt(H)
```

is correct. At zero center guard the absolute Lipschitz envelope contributes `epsilon^(-1) sqrt(H)`, so the total power is `epsilon^(-1) H^(3/2)`.

The theorem genuinely includes

- nondecreasing angular occupation;
- positive-radius births followed by no later loss;
- arbitrarily high scalar growth order;
- zero center guards; and
- infinitely flat guards.

It does not assert that every Lorentz word satisfies the no-loss condition. The manuscript is explicit on this point.

## 8. The fixed-word physical angular current

The manuscript forms the actual physical angular set

```text
E = {(u,phi): B_z,lambda(sqrt(2u) omega_phi)=1}
```

on the radial-angular cylinder.

For a fixed word and exact label, the claim that `E` is definable in a restricted-analytic structure on compact annuli is plausible. The selected contact graph and Morse map are analytic away from their physical singularities. First-hit decisions, closest-foot cases, section membership, occupation, terminal membership, displacement, and exact-label decisions are finite Boolean combinations of restricted-analytic tests after a finite case refinement.

Cell decomposition then gives finite angular fibers and finitely many radial changes. Monotonicity gives finite variation of the angular fraction at each fixed word. The manuscript correctly makes no claim that the number of cells or the variation is uniform in the collision count.

Near the center it invokes the inherited analytic angular-germ classification and joins that neighborhood to a compact annulus. This is a reasonable route to fixed-word finite perimeter and radial bounded variation.

The distributional identity

```text
D L = (1/(2 pi)) pi_# D_u 1_E
    = -(1/(2 pi)) pi_#(n_u H^1|partial*E)
```

has the correct outward-normal sign and normalization. No artificial mass is introduced at the radial endpoints or at an angular coordinate cut.

For a signed measure, the negative part of a pushforward is bounded by the pushforward of the negative part. The corresponding inequality used in the paper is therefore correct.

A specialist should verify that every exact-label decision is indeed included in the finite Boolean description and that the inherited center classification covers all physical chart boundaries claimed here. I did not find a formal contradiction in the written argument.

## 9. Attribution to primitive physical interfaces

The manuscript attributes the reduced boundary to an ordered list of original primitive decision interfaces. Coincident interfaces are assigned once, using the jump of the actual Boolean one-hot indicator rather than summing the jumps of all tests which vanish there.

This is the correct convention. Summing primitive jumps before evaluating the Boolean event could create artificial current or destroy cancellation. The paper avoids that error.

The first-clearance witness and next-collision mark remain part of the original source. The boundary attribution is diagnostic and does not replace either physical convention.

## 10. The one-sided loss formula

For the precise representative of a BV function and continuity points `u<v`, one has

```text
L(u)-L(v) <= (D L)^-((u,v)).
```

Averaging over `v in (H,2H)` and applying Tonelli yields the triangular kernel

```text
kappa_H(s) = 1                       for s <= H,
             (2H-s)/H               for H < s < 2H.
```

The manuscript's formula is correct. A negative jump in `(H,2H)` is paid with the appropriate fractional weight; an upward jump is not charged. Replacing the distributional derivative by the classical derivative would indeed miss atomic deaths.

The resulting physically weighted negative-current quantity is only a sufficient upper bound for the loss. It may be infinite. The manuscript explicitly states that fixed-word finite perimeter does not prove the collision-uniform weighted estimate.

This limitation is decisive.

## 11. Complete allocation of the selected disks

Revision 69 left selected-chart annuli outside an additional radial cutoff in its exterior term. Revision 70 removes that bookkeeping gap.

For every selected physical disk it takes

```text
I_chi = (0,h_chi),
J_chi = (0,h_chi/2)
```

and splits the complete chart source into overlap and angular loss. Adding the unchanged physical complement outside the selected disks gives

```text
b_clr = s70 + d70 + e70.
```

The selected-chart event and outside event are disjoint. Within a selected chart, `s70` and `d70` are complementary weights rather than disjoint events. This is a complete and honest source allocation.

A late birth with no occupation in the receiving collar belongs entirely to `d70`; it is not declared controlled. This example correctly exposes the remaining gap.

## 12. The `chi^6` selected-chart overlap height

Apply the overlap theorem with

```text
(a,b,c,d) = (0,h_chi,0,h_chi/2),
delta = 1.
```

Then

```text
d/(d-c) = 1,
b-a+d = 3h_chi/2.
```

Since `sqrt(2h_chi)=r_chi`, the distortion exponent is

```text
(1+1/sqrt(2)) K_chi r_chi.
```

The inherited definitions give

```text
h_chi = r0^2 chi^6 / 2,
K_chi r_chi = C r0 chi.
```

Thus the exponential is uniformly bounded for small `chi`, and

```text
H(s70) <= C chi^6.
```

The use of the open interval means that the boundary of the Morse disk does not create an unproved endpoint evaluation.

I find the exponent and normalization calculation correct.

## 13. The legal fixed-band rate

The manuscript chooses

```text
varepsilon(B)=A0 B^(-1/12),
chi(B)=sqrt(varepsilon(B)).
```

For sufficiently large fixed `B`, the conditions

```text
4 varepsilon <= chi <= 1/10
```

hold. These parameters are chosen before the collision-count limit.

The selected-chart overlap therefore contributes

```text
chi^6 = varepsilon^3 = A0^3 B^(-1/4).
```

The inherited band error is `O(B^(-1/192))`. The complete displayed pointwise budget is consequently

```text
E_M <= C_M B^(-1/192) + C B^(-1/4)
       + H(b_inc) + H(d70) + H(e70).
```

No cutoff in this inequality depends on the collision count. The order of limits is respected.

## 14. What revision 70 closes

Relative to revision 69, the new manuscript closes the following issues.

- Rapid angular growth is no longer automatically treated as a bad radial tail.
- A canonical overlap part is controlled without a radial-ratio cutoff.
- The overlap theorem applies to arbitrary positive selected subfamilies.
- Zero angular capacity is handled without division.
- The no-loss class includes positive-radius births and flat center guards.
- The complete selected Morse disks, including their outer annuli, are allocated.
- The controlled selected-disk component has a collision-uniform `O(chi^6)` height.
- The legal fixed-band contribution is `O(B^(-1/4))`.
- The signed physical current is identified at each fixed word.
- Atomic angular deaths and coincident-interface cancellations are retained.
- The v69 audit-map governance defect has been corrected.

These are mathematically meaningful advances.

## 15. What revision 70 does not close

The manuscript does not prove a collision-uniform bound for the weighted negative radial current. It therefore does not prove

```text
H(d70) -> 0
```

in the required ordered regime.

It does not prove the height of the physical source outside the selected Morse disks. It therefore does not prove

```text
H(e70) -> 0.
```

It does not improve the inherited finite-count first-incidence estimate to a central-scale ordered estimate. It therefore does not prove

```text
H(b_inc) -> 0.
```

These are precisely the last three terms in the paper's endpoint inequality.

## 16. Why finite-word BV is not enough

At every fixed word, a restricted-analytic angular set has finite perimeter and its angular fraction has finite radial variation. The number and total weighted size of its interfaces can nevertheless grow rapidly with the collision count.

The endpoint needs a statement after

- summing the exact physical selected charts;
- weighting by the physical Jacobian and section normalization;
- taking the exact-label supremum;
- multiplying by the `m^2` local scale; and
- taking the collision-count limsup at fixed band.

Finite definability supplies none of these uniform estimates by itself.

An exponentially large number of small angular deaths, or a smaller number with large physical weights, is compatible with fixed-word bounded variation. The manuscript correctly does not infer otherwise.

## 17. The angular-loss problem

A sufficient next theorem would control the quantity isolated at the end of module 153:

```text
limsup_m sup_{R,lambda,t} m^2
  sum_{z: t_z in [t-H,t]} J_z
  integral kappa_H d(D L_z)^-.
```

The estimate must be proved with the legal fixed-band choices `chi(B)` and `epsilon(B)`, and with a bound that tends to zero after the collision limsup and then `B -> infinity`.

It is not enough to show

- fixed-word finiteness;
- small unweighted interface length;
- small source mass;
- a finite number of decision interfaces at each count; or
- an estimate with an exponential factor offset by choosing `B=B_m`.

The physically weighted current must be controlled in the actual ordered topology of the raw theorem.

## 18. The outside-source problem

The outside source `e70` is improved relative to `e69`: it no longer contains annuli artificially removed from selected disks. It nevertheless contains genuine physical states not covered by the selected Morse charts, including failed taper, selected grazing, noncritical roof-rank pieces, and uncovered states.

A complete theorem must give a central-scale essential-height estimate for this exact source. A small parameter-space or roof-space measure is insufficient. A positive density can concentrate on a very small set with arbitrarily large height.

Any further chart enlargement must preserve

- the actual first-clearance witness;
- the next-collision mark;
- exact return, displacement, and collision labels;
- section normalization;
- arithmetic zero classes; and
- the original positive source identity.

## 19. The complete first-incidence problem

The inherited incidence theorem gives a finite-count estimate of the form

```text
C A^m epsilon.
```

This is a genuine density estimate, but it does not tend to zero at a fixed reconstruction band. Choosing the protection width or band as an exponential function of `m` would reverse the proved order of limits.

The paper still needs a collision-uniform exact-label level-sum estimate for the complete first-incidence source in the central pointwise topology.

The angular-overlap theorem does not address this source.

## 20. Consequences which remain unavailable

Until the three remaining heights vanish, the paper cannot deduce the unrestricted scalar pointwise law. Without that scalar denominator and upper estimate, it also cannot deduce

- the unrestricted same-roof collision bridge;
- the unrestricted same-roof actual-return bridge;
- forward essential likelihood convergence;
- exact-roof path conditioning on every positive-reference class; or
- an unmodulated Gaussian theorem on arithmetic zero classes.

The existing integrated, local-variation, good-set, and mean-bridge results retain their value and scope. They do not substitute for the missing essential-height endpoint.

## 21. Arithmetic modulation

The finite arithmetic transition kernel remains part of the uniform theorem. Zero classes are retained. Revision 70 does not prove that the fixed-radius arithmetic factor is identically one.

This is mathematically honest. The final pointwise theorem, if obtained, should retain the arithmetic transition kernel unless a separate concrete residue theorem proves a simplification.

No conditional law should be assigned to a zero arithmetic denominator.

## 22. Novelty and relation to prior methods

The scalar overlap identity itself is elementary. Its mathematical value here lies in its insertion into a difficult, exactly labelled physical source with a count-uniform comparison collar.

The signed-current theorem is a natural application of finite-perimeter and o-minimal tools to the actual angular decision set. The physically important point is the preservation of signs, jump atoms, and exact labels.

These contributions are useful within the A2-DYN program. They do not yet amount to a broad new local-limit mechanism for singular hyperbolic systems. The hard uniform dynamical estimate remains the weighted negative-current and outside-source control.

The manuscript's literature comparison is appropriately restrained. Existing Lorentz cell-index local limits, billiard endpoint local limits, and suspension mixing local limits do not directly provide the present density-height estimate. Conversely, revision 70 should not be described as replacing those theories or as proving a new general suspension theorem.

## 23. Editorial significance at the requested benchmark

The combined article now contains many substantial results:

- stationary microscopic local laws;
- compact-family action estimates;
- exact occupation arithmetic;
- local and global variation laws;
- positive source decompositions;
- bridge and posterior results;
- pressure-controlled arithmetic transitions;
- model pointwise coarea theorems;
- Lorentz incidence and clearance reductions;
- caustic and angular-germ analysis;
- finite-scale radial comparison; and
- the new angular-overlap and signed-current theorems.

If the inherited continuum chain withstands expert scrutiny, this is a significant specialist research program.

At the requested four-journal benchmark, however, the article remains extraordinarily long, highly model-specific, and organized around an unproved title-level endpoint. The new modules isolate the remaining obstruction more sharply but do not eliminate it.

A focused specialist paper on the count-uniform overlap theorem, physical angular current, and exact source allocation could be valuable. The present unified top-four submission remains premature.

## 24. Independent specialist verification

No independent human specialist audit has been obtained.

For the inherited inputs, the most important checks remain

1. the selected-contact continuation and relative physical density;
2. inclusion of all primitive first-hit and section decisions in the one-hot mask;
3. disjointness of selected chart restrictions after omitting only the clearance multiplier;
4. the exact two-endpoint comparison event;
5. the fixed-width local estimate used by the collar trace;
6. common coarea representatives;
7. exact section normalization;
8. the original positive raw-error identity; and
9. preservation of exact labels and arithmetic classes.

For module 152, an expert should check

- measurability and the `L=0` convention;
- the fact that the overlap is only a scalar capacity;
- the use of arbitrary positive subfamilies;
- the factor `d/(d-c)`;
- the interval length `b-a+d`;
- both relative-Jacobian exponents;
- the absolute guard envelope; and
- the passage from chartwise overlap to the count-uniform collar trace.

For module 153, an expert should check

- the restricted-analytic description of every physical decision;
- finite perimeter near and away from the center;
- the outward-normal sign;
- the factor `1/(2 pi)`;
- cancellation at angular coordinate cuts;
- radial projection before taking the negative part;
- retention of jump atoms;
- single attribution of coincident interfaces; and
- the BV/Tonelli derivation of the triangular kernel.

For module 154, an expert should check

- complete allocation of every selected disk;
- identification of `e70` with exactly the original outside source;
- the factor `3h_chi/2`;
- the exponent `(1+1/sqrt(2)) K_chi r_chi`;
- uniformity in the exact label and collision count;
- the legal choice `chi(B)=sqrt(epsilon(B))`; and
- the fact that only `s70` receives the `B^(-1/4)` estimate.

Source hashes, finite fixtures, and a successful native build do not replace this audit.

## 25. Required mathematical changes before another top-four review

### 25.1 Prove an ordered angular-loss estimate

Establish a collision-uniform physically weighted negative-current theorem, or another estimate directly controlling `H(d70)`, at the legal fixed-band order of limits.

The theorem must include jump atoms, exact labels, physical Jacobians, and all selected charts. It may not infer uniformity from finite-word definability.

### 25.2 Prove the outside-source height

Control `H(e70)` on the original physical source. The estimate must cover failed taper, grazing, noncritical-rank, and uncovered states without deleting a small set of roofs or replacing height by mass.

### 25.3 Prove the complete first-incidence height

Upgrade the finite-count exponential incidence estimate to the ordered central-scale topology. Do not choose a band depending exponentially on the collision count.

### 25.4 Complete the pointwise arithmetic theorem

Insert the three height estimates into the exact positive raw-error identity and prove the original two-sided pointwise law with the finite arithmetic transition kernel and zero classes retained.

### 25.5 Derive same-roof consequences only after scalar closure

Once the scalar pointwise denominator and upper law are established, deduce the collision and actual-return same-roof bridges, essential likelihood, and path conditioning with their exact positivity assumptions.

### 25.6 Obtain independent specialist review

The physical mask, collar comparison, current identity, weighted source estimates, anisotropic operator chain, and arithmetic inversion require human review by experts in dispersing billiards and transfer operators.

### 25.7 Reduce the journal proof burden

Present the shortest complete proof of one principal endpoint. Extensive historical pipelines, validation ledgers, and alternative incomplete routes should not dominate the journal narrative.

### 25.8 Sharpen the general theorem or narrow the claim

If top-four breadth is sought, formulate a reusable weighted-current/source-height theorem with hypotheses verified in several genuinely different singular systems. Otherwise align the title and main theorem with the strongest completed result.

### 25.9 Preserve the corrected audit metadata

Keep the active revision-70 specialist map and the full inherited status map. Do not allow older version-named checkpoint files to be mistaken for current status.

## 26. Technical and presentation comments

1. Keep `a_J` explicitly indexed by the exact label; readers should not mistake it for a label-free geometric coefficient.
2. State near every use that `s` and `d` are complementary weights, not disjoint events.
3. Retain the `L=0` convention and the reason the corresponding density is zero almost everywhere.
4. Keep `I` and `J` distinct; in the whole-chart theorem the receiving interval is half the source interval.
5. Do not omit the factor `d/(d-c)` in general statements.
6. Keep the source-center interval length `b-a` separate from the collar width `d`.
7. State that the collar theorem is applied after summing the physical source, which is why no word count occurs.
8. Keep the absolute guard estimate separate from the unguarded comparison profile.
9. Do not describe the overlap as a coupling of physical trajectories.
10. Keep the no-loss hypothesis as an exact finite-scale assumption rather than an inferred monotonicity theorem for all words.
11. Preserve the distinction between scalar diagnostic profiles and realized Lorentz profiles.
12. In the BV theorem, keep the cylinder open in the radial coordinate so no artificial endpoint current appears.
13. Retain the factor `1/(2 pi)` and the outward-normal sign.
14. Take the negative part only after summing the actual Boolean jump and projecting the signed current.
15. Keep atomic deaths in the loss measure.
16. Do not replace the negative variation by the almost-everywhere classical derivative.
17. State whenever a BV or definability assertion is fixed-word only.
18. Keep `d70` in every complete source identity and endpoint budget.
19. Keep `e70` identified as the original outside source, not a newly defined negligible remainder.
20. State that all selected-disk annuli are allocated but not all are controlled.
21. Keep `chi(B)` and `epsilon(B)` fixed before the collision limit.
22. Retain the exact exponent calculation from `chi^6` to `B^(-1/4)`.
23. Do not attach the `B^(-1/4)` rate to `d70`, `e70`, or incidence.
24. Keep source height distinct from source mass and source total variation.
25. Preserve arithmetic zero classes in all principal statements.
26. Do not define conditional laws on a zero reference class.
27. Keep probability total variation distinct from variation mass and from path bounded-Lipschitz dual.
28. Do not promote workflow success or finite diagnostics to proof certification.
29. Keep the active source manifest's false endpoint flags visible.
30. Consider moving operational and historical metadata outside the journal-facing proof narrative.

## 27. Final assessment

Revision 70 is a serious and mathematically coherent response to the revision-69 report.

It proves a new count-uniform overlap-height theorem on the original exactly labelled physical source. The theorem correctly distinguishes angular growth from angular loss and does not require the unproved radial moment. It covers the complete selected disks, including their outer annuli, and yields the legal fixed-band contribution `O(B^(-1/4))`.

It also gives a credible fixed-word bounded-variation theorem for the physical angular set and an exact signed-current formula which retains cancellations and atomic radial deaths.

I found no decisive error in modules 152--154 or in their immediate use of the inherited positive comparison collar.

The advance is nevertheless a partial source theorem. The complete angular-loss source, the source outside selected disks, and the complete first-incidence source remain uncontrolled in the ordered essential-height topology. Those three terms are exactly the remaining obstruction in the paper's own pointwise raw-error identity.

The unrestricted two-sided arithmetic raw-density theorem and its same-roof consequences therefore remain open. The article also remains highly model-specific, extraordinarily large, and dependent on continuum inputs which have not received independent specialist verification.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**

A focused specialist-journal paper built around the positive overlap comparison, physical radial current, and exact selected-chart allocation could be valuable if the inherited physical collar chain survives expert audit. A future top-four submission should return only after the ordered angular-loss, outside-source, and first-incidence heights have been closed, or after the method has been elevated to a broad independently significant theorem with multiple verified realizations.
