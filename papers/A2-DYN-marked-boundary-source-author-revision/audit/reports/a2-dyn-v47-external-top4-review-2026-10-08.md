# External top-four referee report on A2-DYN revision 47

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v47-referee-response-2026-10-08`, `revision/a2-dyn-v47-referee-copy-2026-10-08`  
**Reviewed commit:** `ec4e7cca65ee3cbdc441c8264b39aca3ead112ac`  
**Reviewed repository tree:** `4abdf4260eb1d561e4bb21087d2455f000f27868`  
**Ordinary source payload tree:** `bf32f519accb691eddb4329660b9509a25b875cc`  
**Active manuscript directory:** `papers/A2-DYN-v47-referee-response`  
**Active mathematical source:** one hundred one numbered core modules; revision 47 adds modules 100--101  
**Frozen revision-46 author baseline:** `fb16f06fb2bd205322d4a15979aef5a9a83d4970`  
**Frozen revision-46 full paper tree:** `9bea85c50917e3f3de1410cb140cdce9966d6f8d`  
**Controlling report:** `reviews/a2-dyn-v46-external-top4-review-2026-10-08/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `ae02860fe7182078ed738d1b23213b3ce8f8afe3` / `b222d90012ac419cd0cfe3b09a21e680da672205`  
**Date:** 8 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 47 is a genuine theorem-bearing advance over revision 46. It does not merely repartition the collapsing-margin source or replace the original exact coefficient by an averaged return-index statement. It proves an actual pointwise estimate, at the natural `m^{-2}` scale, for the source on which finitely many endpoint section decisions are allowed to collapse while every incidence, clearance, and retained middle decision remains protected.

The principal new estimate is

```text
limsup_m sup_{R,n,k,|a|<=M}
  m^2 ||d^{eta,epsilon,J,a}_{n,k,m,R}||_infinity
  <= C M (J+1) epsilon.
```

The source on the left retains the original exact return index `n`, displacement `k`, collision count `m`, and roof variable. The proof uses a finite occupation enlargement only on the upper side of a positive comparison. It does not identify the target coefficient with a packet average. The same pointwise estimate controls the complete signed smoothing correction of this component uniformly over every bandwidth, and it holds for arbitrary bounded measurable source insertions by Radon--Nikodym domination.

The manuscript also gives an exact positive source factorization and a disjoint first-bad-margin partition of the remaining source. With

```text
epsilon(B)=A B^(-1/12),
J(B)=floor(B^(1/24)),
```

the smoothly protected correction and the endpoint-decision correction are together reduced to `O(B^(-1/24))` after the collision limit. The unresolved pointwise theorem is thereby localized to three positive residual sources: first bad incidence, first bad clearance, and first bad interior section decision.

I audited the new modules

- `core/100_endpoint_decision_deconcentration.tex`;
- `core/101_first_bad_margin_resolution.tex`;

and their use in the new leading theorem, together with the response, proof ledger, specialist audit map, source manifest, publication status, validation record, branch chronology, and exact-source workflow evidence.

Within the scope of this audit, I found no decisive counterexample, collision/return endpoint mismatch, missing factor of the section mass, incorrect occupation convention, illicit replacement of the exact return index by a finite packet, Fourier-sign error, or hidden use of a bandwidth growing with the collision count inside a theorem proved only at fixed band.

The following features of the revision are particularly important.

1. The high-gradient roof flow is allowed to cross only named section-decision cuts, not a grazing, competing-hit, clearance, or physical-word boundary.
2. The original density remains on the left side throughout; the finite occupation allowance is used only in a positive upper comparison.
3. The ambient continued source is explicitly `nu/c`, which agrees with the return source on the initial section and remains meaningful after an endpoint crosses that section.
4. The terminal section membership at collision time `m` is not counted in the occupation sum over `0,...,m-1`.
5. The local-window theorem is applied with all geometric and Fourier parameters fixed before the collision limit; the roof-window length cancels only after that fixed-window estimate.
6. Low-gradient points are completed to physical normal-to-normal critical centers with the same middle occupation and the same finite endpoint allowance.
7. Each physical critical collar is charged once, even if free section decisions split it into several return-index pieces.
8. Arbitrary bounded insertions are handled by domination of the positive source, not by differentiating a measurable selector.
9. The first-defect decomposition is made before pushforward and is genuinely positive and disjoint.
10. The arithmetic transition kernel and fixed-radius residue factor are retained unchanged.

These are substantive improvements.

The negative recommendation is nevertheless unavoidable. The article still does not prove the theorem around which its title and raw-inversion architecture are organized. The residual incidence, clearance, and interior-decision sources have small total variation masses,

```text
O(epsilon^2),
O(epsilon),
O(epsilon q^((J+1)/4)),
```

respectively, but their pointwise signed corrections are not estimated at scale `m^{-2}`. Small mass does not control density height or the difference between a density and its band-limited convolution. Incidence and clearance crossings can change the physical collision word and, in the incidence case, the collision count itself. The endpoint-decision roof flow cannot simply be repeated for those sources. The interior-decision mass is exponentially small in the endpoint depth, but no theorem prevents it from concentrating on a correspondingly small roof set.

The manuscript itself records the exact remaining criterion:

```text
lim_{B->infinity} limsup_{m->infinity} sup_{R,n,k}
  m^2 esssup_central_t
  |r^{epsilon(B),J(B)} - K_B*r^{epsilon(B),J(B)}| = 0.
```

This criterion is not proved. Consequently the full arithmetic pointwise roof-density local limit, the complete raw return LLT, and the pointwise roof-conditioned bridge remain open.

There is a second independent issue. The concrete section residues are still not shown to vanish. At a fixed radius the exact-index main term is naturally

```text
c mathfrak a_R(k,n,m) g_{Omega_R},
```

or the equivalent `D_R` normalization. Uniformly through changes of arithmetic type, the correct main term is the finite transition kernel `mathcal L_{m,R}`. Revision 47 treats this correctly. It does not prove the unmodulated radius-uniform singleton theorem, and any final raw theorem must retain the arithmetic modulation unless a new zero-residue theorem is supplied.

At the requested venue level, the paper would need either

- a complete arithmetic pointwise raw-density theorem, including the remaining incidence, clearance, and interior-decision correction and the correct arithmetic main term; or
- a substantially broader conceptual theorem whose independent significance does not depend on the unfinished raw endpoint.

Revision 47 supplies neither yet, although it materially narrows the first problem.

## 2. Frozen source, chronology, and preservation

Both reviewed author branches resolve to

`ec4e7cca65ee3cbdc441c8264b39aca3ead112ac`.

The repository tree at that commit is

`4abdf4260eb1d561e4bb21087d2455f000f27868`.

The active manuscript is

`papers/A2-DYN-v47-referee-response`.

The ordinary source payload tree recorded in the source manifest is

`bf32f519accb691eddb4329660b9509a25b875cc`.

Revision 47 starts from the frozen revision-46 external-review commit `ae02860fe7182078ed738d1b23213b3ce8f8afe3`. The reviewed revision-46 author source is `fb16f06fb2bd205322d4a15979aef5a9a83d4970`. Thus the chronology is correct: the author revision descends from the controlling report rather than silently rewriting the already reviewed author branch.

The source records state that all ninety-nine inherited core modules and all one hundred twenty-three inherited Python scripts are retained byte-for-byte. The bibliography, all inherited mathematical labels, and the compiled A--X synopsis are preserved. Modules 100 and 101, revised front matter, proof maps, diagnostics, provenance, and the new qualification workflow are added without deleting the inherited mathematical corpus.

The present review branch begins directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v47-external-top4-review-2026-10-08/`.

No author source, prior review, workflow, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-source qualification workflows completed successfully at the reviewed SHA:

- response branch run `37789082590`;
- referee-copy branch run `37789105202`.

The workflow checks the exact event SHA, the frozen revision-46 source and controlling report, all one hundred one core inclusions, byte identity of inherited cores and scripts, mathematical-label retention, bibliography and A--X retention, the ordinary-source Merkle identity, normal/optimized finite-check agreement, native TeX compilation, stabilized references, and theorem-label-based page rendering.

The new finite diagnostics check, among other things,

- the occupation convention with the terminal membership excluded from the sum;
- finite occupation changes under endpoint section crossings;
- positive source factorizations;
- disjoint first-defect partitions;
- geometric depth sums;
- a radial roof-flow/coarea model;
- and the rational bandwidth exponents.

Negative controls correctly reject both of the following invalid inferences:

1. that crossing a section decision must preserve the return index;
2. that small source mass alone controls density height.

These checks are useful source, algebra, and bookkeeping evidence. They do not certify

- the full occupation-torus anisotropic spectrum;
- the endpoint continuation on singular billiard branches;
- parameter-uniform smooth endpoint envelopes;
- global injectivity of the roof flow across section cuts;
- critical completion outside the section;
- the physical collar disjointness and coefficient cluster estimate;
- or the missing residual pointwise theorem.

The manuscript and its validation record state this distinction accurately.

## 4. Scope of this review

I did not attempt to re-prove the complete one-hundred-one-module article. The substantive audit concentrates on the new chain that could alter the revision-46 assessment:

1. the full-occupation local upper bound with general smooth endpoint functions and no compulsory section factors;
2. the control of surviving physical projection amplitudes by endpoint masses;
3. uniformity through radius-dependent arithmetic transitions;
4. smooth positive upper approximation of finite endpoint histories;
5. the geometric-series endpoint mass bound independent of the depth `J`;
6. continuation after deleting finitely many section-margin checks;
7. preservation of the physical word, displacement, and collision count;
8. the exact occupation allowance and terminal-time convention;
9. the scaled section-distance derivative estimate;
10. use of the ambient source `nu/c` across initial and terminal section cuts;
11. high-gradient roof transport through free section decisions;
12. fixed-window coarea conversion and cancellation of the roof-window length;
13. injectivity on a physical word across the decision cuts;
14. low-gradient completion to normal-to-normal physical critical centers;
15. positive collar comparison with centers outside the section;
16. the count of occupation coefficients in the upper comparison;
17. the endpoint-decision essential-supremum estimate;
18. the all-band convolution consequence;
19. extension to arbitrary bounded measurable insertions;
20. exact factorization of the original graded guard;
21. the disjoint first-bad-margin partition;
22. the three residual mass estimates;
23. the exponent ledger in the ordered bandwidth/depth choice;
24. and the exact equivalence between the full arithmetic raw theorem and the remaining residual correction.

Inherited load-bearing inputs include the full occupation-torus fixed-band spectrum, physical peripheral projection formula, moving spectral maxima, arithmetic transition theorem, endpoint action and Hessian bounds, relative source distortion, protected flow-box theorem, protected critical-cluster deconcentration, normal endpoint local bounds, complete fixed-count source density, and the coefficient-first arithmetic reconstruction criterion.

## 5. Overview of the new source decomposition

Let `Xi_m,R^epsilon` be the full graded protection from revision 46. Revision 47 factors it as

```text
Xi = G E,
```

where `E` contains the section-decision factors in the two endpoint layers

```text
{0,...,J} union {m-J,...,m},
```

and `G` contains

- every incidence factor;
- every clearance factor;
- and every section-decision factor outside those endpoint layers.

The exact identity

```text
1-Xi = G(1-E) + (1-G)
```

is made before pushforward. For the original exact event, the full roof density is therefore

```text
p = f^epsilon + d^{epsilon,epsilon,J} + r^{epsilon,J},
```

where

- `f^epsilon` is the smoothly protected source already controlled in revision 46;
- `d` is the newly controlled endpoint-decision source;
- `r` is the positive residual with at least one bad incidence, clearance, or retained middle decision.

The residual is then split by the first factor of `G` which is strictly less than one. This includes the transition region of the smooth guard, not only the set on which a factor vanishes. The partition is disjoint and positive.

This decomposition is exact, source-level, and coefficient-preserving. It is not a mixture of separately normalized conditional laws.

## 6. The small-endpoint local upper bound

Lemma `v47-small-endpoint-local` is the first new analytical input. For fixed smooth endpoint functions `a_R,d_R` of masses at most `alpha,beta`, it proves

```text
limsup_m sup_{R,k,ell,t} m^2
  int a_R(x)d_R(T_R^m x)
      1_{K^c_m=k,A_m=ell,S_m-t in I} dnu
  <= C alpha beta |I|.
```

The proof uses the finite moving-peak reduction inherited from the radius-uniform transition theorem. A branch which contributes along a convergent sequence of radii must limit to an actual physical resonance. At such a resonance the endpoint projection coefficient is bounded by

```text
|nu(d q_gamma) nu(a conjugate(q_gamma))|
  <= alpha beta,
```

because the physical phase has modulus one.

The order of limits is important and is stated correctly:

1. the endpoint family and roof interval are fixed;
2. a positive Fourier majorant is fixed;
3. the collision count tends to infinity;
4. the outer roof band is then enlarged;
5. any excess mass in a smooth endpoint approximation is removed last.

The constant in the final limsup is independent of the fixed smooth norms, while the collision threshold is permitted to depend on those norms. Thus the lemma is not a quantitative theorem uniform over endpoint sets shrinking with `m`. Revision 47 does not use it that way.

I found no contradiction in this argument. It remains a specialist-level step. In particular, one should verify the continuity of scalar amplitudes on every moving peak chart and the claim that the finite chart count is independent of the chosen endpoint functions.

## 7. Finite endpoint histories

The endpoint bad sets are unions of section-boundary neighborhoods along the first or last `J+1` collision states, with thresholds weighted by the geometric depth factor `q^{j/4}`. Invariance gives

```text
nu(U^+_{R,J}(s)) + nu(U^-_{R,J}(s))
  <= C s sum_{j=0}^J q^{j/4}
  <= C s.
```

The constant is therefore independent of `J`, although the smooth norms of an upper approximation and the collision threshold may depend on `J`, `s`, and the approximation excess.

The proof avoids claiming that a long pullback of a section indicator has a uniformly bounded anisotropic norm. It instead removes a small neighborhood of the finitely many singularities involved in a fixed endpoint history, uses persistence on the compact regular complement, and then constructs smooth positive upper functions on a finite parameter cover.

This is the correct qualitative mechanism for fixed `J`. It does not supply an estimate uniform when `J` grows with `m`. In the later ordered limit, `J(B)` is fixed before the collision limit, so that stronger assertion is not needed.

The same lemma also gives the two-normal-strip bound used in the low-gradient completion. With strip widths of order `sqrt(r)` and a roof interval of order `r`, the local probability is of order `r^2 m^{-2}`, as required by the collar calculation.

## 8. Continuation with free endpoint decisions

The partial guard deletes only section-decision factors at the two endpoint layers. Every incidence and clearance factor remains protected, as do all middle section decisions.

Consequently the inherited endpoint continuation preserves

- the physical center word;
- the displacement `K^c_m`;
- the collision count `m`;
- and every retained middle decision.

The omitted section decisions may change. Starting from occupation `A_m=n`, the continued occupation lies in a fixed finite set around `n`. The manuscript uses the safe allowance

```text
|ell-n| <= 2J+2.
```

This convention correctly treats `A_m` as the sum over collision times `0,...,m-1`. The terminal section membership at time `m` is not another summand, although it is included among the free membership conditions.

The scaled derivative estimate

```text
max_j e_j^(-1) |grad s_j| <= C eta^(-1)
```

is compatible with the inherited endpoint influence bound. Distances to the rectangle boundary are only Lipschitz at corners, so the statement is correctly made almost everywhere.

The physical reduced action and its cross Hessian do not depend on a section membership decision. They therefore glue across a free section cut. The continued source is explicitly

```text
nu/c,
```

not a renormalized section probability. This point is essential when the initial endpoint leaves the section during the positive upper comparison.

I found no missing factor of `c` in the displayed comparison. The normalization should nevertheless be checked carefully in any later use outside module 100.

## 9. High-gradient roof transport

On the high-gradient part the manuscript uses

```text
V = grad F / |grad F|^2
```

and chooses the fixed roof width

```text
h = c_2 min(eta^3 delta^2, epsilon eta delta).
```

The first term keeps the trajectory inside the continuation, retains a gradient lower bound, and bounds the relative physical density Jacobian. The second term ensures that an initially bad free section decision remains in a slightly enlarged bad endpoint set during the flow.

The flow is allowed to cross free section cuts. It is not allowed to cross a physical-word boundary, incidence boundary, clearance boundary, or protected middle-decision boundary.

The resulting image lies in a positive collision event with

- the same displacement `k`;
- the same collision count `m`;
- occupation in the finite allowance around `n`;
- a fixed roof interval of length `2h`;
- and a bad initial or terminal endpoint history of mass `O(epsilon)`.

The coarea estimate is

```text
rho_A(t) <= e/(2 h c)
  sum_{ell in I_{n,J}}
  nu{K^c_m=k,A_m=ell,|S_m-t|<h,bad endpoint}.
```

The allowance has at most `4J+5` integer values. Since `h`, `J`, `eta`, `epsilon`, and `delta` are fixed before the collision limit, the small-endpoint local upper bound applies. Its factor `2h` cancels the coarea denominator only after that fixed-window estimate.

This is not a shrinking-window substitution. It also does not replace the exact coefficient on the left by the finite occupation sum on the right.

The most delicate point is injectivity. The argument uses the roof value to recover the flow time and ODE uniqueness to recover the starting point, treating all free section pieces as one physical-word domain. Different physical words remain disjoint. I did not find an immediate multiplicity contradiction, but this global gluing is one of the parts most in need of independent billiard-geometric verification.

## 10. Low-gradient critical completion

The low-gradient source is completed to nearby normal-to-normal physical critical centers. Because only section decisions have been freed, the inherited strong convexity, incidence and clearance control, Hessian bounds, and relative density distortion remain available.

The completed center may lie outside the initial or terminal return section. The proof therefore uses physical collars in the ambient source `nu/c`. The middle occupation is unchanged. The total occupation differs from the original `n` only through the same finite set of free endpoint decisions.

For a collar of roof width `r`, the inherited positive mass bound is proportional to

```text
r J_z,
```

where `J_z` is the intrinsic critical coefficient in the ambient physical source. A positive comparison using

- a roof interval of length `O(r)`;
- two normal endpoint strips of width `O(sqrt(r))`;
- and at most `4J+5` occupation coefficients

has normalized mass `O((J+1)r^2)`. Dividing by the collar mass gives a cluster estimate `O((J+1)r)` for the sum of critical coefficients in a roof interval of length `O(r)`.

With `r` chosen on the order of `delta^2`, the low-gradient density is therefore `O((J+1)delta^2 m^{-2})`.

The proof correctly removes `delta` only after the collision limsup with `eta`, `epsilon`, and `J` fixed.

I found the scaling internally consistent. The load-bearing points are

- uniqueness of the completed physical center;
- disjointness of the physical collars;
- counting each collar only once when free decisions split it;
- and the assertion that the occupation allowance is not enlarged a second time.

These points should receive an independent specialist audit.

## 11. Endpoint-decision density and all-band correction

Combining the high- and low-gradient estimates gives

```text
limsup_m sup m^2 ||d||_infinity
  <= C (J+1)(epsilon+delta^2).
```

Sending `delta` to zero after the limsup proves the endpoint-decision theorem.

For a bounded measurable insertion `a`, the absolute source is dominated by `M` times the positive unweighted source. The same essential-supremum estimate therefore holds without differentiating `a` and without requiring an endpoint regularity norm.

The all-band estimate follows from

```text
||f-K_B*f||_infinity
  <= (1+||K_1||_1) ||f||_infinity.
```

This is a convolution consequence of pointwise source smallness. It is not a spectral theorem with a roof band depending on the collision count.

The finite-jump corollary is also correctly limited. If one-sided traces exist, each jump is at most twice the essential height bound. The manuscript does not infer an absolute sum over all jumps and does not apply the result to incidence or clearance sources.

## 12. First-bad-margin resolution

The original guard factorization is exact:

```text
Xi = G E,
1-Xi = G(1-E) + (1-G).
```

The factors of `G` are ordered by distance from the nearest endpoint and then by type. The set on which the `i`th factor is the first factor strictly less than one is

```text
A_i = {w_i<1} intersection_{h<i}{w_h=1}.
```

These sets partition the entire smooth transition region `{G<1}`, not only the set on which some factor vanishes.

The three residual densities are nonnegative and retain the original labels and normalization. Summing over `n,k` at fixed collision count is legitimate because the original exact events are disjoint.

The variation-mass estimates are

```text
incidence: C epsilon^2,
clearance: C epsilon,
interior decision: C epsilon q^((J+1)/4).
```

They use invariance and the one-flight neighborhood estimates, not independence. The geometric depth weights make the sums uniform in the collision count.

These are useful estimates. The manuscript correctly states that they are not pointwise density bounds.

## 13. The ordered bandwidth and endpoint depth

The choice

```text
epsilon(B)=A B^(-1/12),
J(B)=floor(B^(1/24))
```

is made with `B` fixed before the collision limit.

The protected correction from revision 46 requires

```text
B >= C_2 epsilon(B)^(-12).
```

Since

```text
epsilon(B)^(-12)=A^(-12) B,
```

this condition is satisfied for all large `B` after choosing `A^12>=C_2`.

The endpoint-decision correction is

```text
O((J(B)+1)epsilon(B)) = O(B^(-1/24)).
```

The protected part is `O(B^(-1/2))`, so the combined paid correction is `O(B^(-1/24))`.

The residual mass bounds become

```text
incidence: O(B^(-1/6)),
clearance: O(B^(-1/12)),
interior decision:
  O(B^(-1/12) q^((floor(B^(1/24))+1)/4)).
```

The exponent ledger is correct.

The argument does not produce a count-dependent protection scale. It gives an ordered double limit: fix `B`, hence fix `epsilon(B)` and `J(B)`; take the collision limsup; then send `B` to infinity. Revision 47 does not claim more.

## 14. What revision 47 has closed

Subject to specialist verification of the continuum geometry, the following obstruction from revision 46 has been genuinely closed.

A collapsing section-decision boundary in any fixed endpoint layer, with all physical margins and middle section decisions protected, contributes at most

```text
C(J+1)epsilon m^(-2)
```

in essential supremum. Its complete signed smoothing correction is controlled uniformly over every roof bandwidth. The estimate remains valid for arbitrary bounded measurable source insertions.

This is materially stronger than

- a total-mass bound;
- a finite-cutoff reconstruction statement;
- a trace-jump extraction;
- or an equivalence criterion.

The finite occupation allowance does not alter the target coefficient. The exact return index remains fixed on the left side.

## 15. The decisive residual obstruction

The remaining source is

```text
r = r_inc + r_clr + r_mid.
```

The full arithmetic raw theorem is equivalent to pointwise vanishing of

```text
r-K_B*r
```

at scale `m^{-2}` in the ordered collision/bandwidth limit.

This is not proved.

### 15.1. Incidence defects

A near-grazing incidence is a physical singular regime. Crossing it can change the branch, and at an actual grazing boundary the collision map itself loses the regularity used by the endpoint roof flow. The new continuation deliberately retains incidence protection. Thus the endpoint-decision theorem gives no pointwise estimate for `r_inc`.

The total mass `O(epsilon^2)` is favorable, but a density of that mass can still have arbitrarily large height on a sufficiently thin roof set.

### 15.2. Clearance defects

A small competing-hit clearance is also a physical-word boundary. Crossing it can change which obstacle is hit next. The reduced action and its derivatives need not glue across that boundary in the manner used for a section decision.

The mass bound is only `O(epsilon)`. No local coarea or Fourier norm for `r_clr` is supplied.

### 15.3. Interior section decisions

The middle-decision source has mass exponentially small in `J`, and under the ordered choice its mass is smaller than any fixed power of the displayed geometric factor. This does not alone control the density or signed smoothing correction.

A proof could require a pointwise deconcentration theorem whose constants remain effective at a decision depth growing with `B`, or a cancellation mechanism for the signed sum. No such theorem is present.

### 15.4. Signed sum versus separate estimates

The criterion requires only the signed sum of the three residual corrections to vanish; it does not require a separate absolute estimate for each component. Revision 47 states this correctly.

Nevertheless, no theorem proves cancellation among the three components. Their positivity before applying `I-K_B*` does not imply positivity after smoothing subtraction.

## 16. Small mass, finite-count height, and the residual

The article contains a radius-uniform exponential-in-count height bound for complete fixed-collision-count densities and their bounded restrictions. This is useful for finite-count absolute continuity and for excluding divergent local germs.

It does not close the residual criterion. Combining

```text
mass <= small number
```

with

```text
height <= C A^m
```

still allows concentration far above the local scale `m^{-2}`. A qualitative diagonal in the protection parameter likewise gives no prescribed rate that can be inserted into the pointwise local theorem.

The source manifest keeps the relevant flags false:

- `central_scale_boundary_source_smallness_proved`;
- `clearance_boundary_pointwise_smallness_proved`;
- `grazing_boundary_pointwise_smallness_proved`;
- `interior_decision_boundary_pointwise_smallness_proved`;
- `full_signed_correction_proved`;
- `full_raw_return_LLT_proved`;
- `pointwise_roof_density_LLT_proved`.

This is the correct status.

The separate flag `pointwise_boundary_source_bound_proved` refers only to an exponential finite-count height bound. It should not be read as central-scale boundary deconcentration. I recommend renaming or displaying its scope prominently in future front matter to avoid ambiguity.

## 17. Arithmetic form of the main term

Revision 47 preserves the correct arithmetic formulation.

At fixed radius the exact-index fixed-interval theorem has main term

```text
c mathfrak a_R(k,n,m) g_{Omega_R}(Z),
```

or equivalently

```text
mathfrak a_R(k,n,m) g_{D_R}(V_n)
```

in the original return normalization.

Uniformly through changes of arithmetic type, the main term is the finite transition kernel

```text
mathcal L_{m,R}.
```

The endpoint-decision comparison includes all surviving occupation resonances. A zero arithmetic residue is not assigned a positive conditional law. The finite occupation allowance is used only in an upper bound and is never averaged into the final coefficient.

No proof is given that the actual section phase masses are uniform or that every nontrivial endpoint residue vanishes. Therefore an unmodulated radius-uniform singleton theorem remains unproved.

Any eventual pointwise roof-density theorem should state its arithmetic main term explicitly unless the concrete zero-residue criterion is established.

## 18. Fixed interval, pointwise density, and conditioning

The article now has several strong but distinct statements:

- a stationary microscopic singleton law;
- fixed-radius exact-index arithmetic local laws for fixed roof intervals;
- a radius-uniform transition formula for those intervals;
- an exact-event Gaussian return bridge under a microscopic denominator;
- arithmetic endpoint posteriors;
- finite-packet consequences;
- coefficient-first pointwise reconstruction at chosen componentwise bands;
- protected-source pointwise correction bounds;
- and the new endpoint-decision pointwise source bound.

None of these alone proves the full pointwise roof-density LLT for the unprotected original source.

A fixed positive roof interval is not a density value. An existential slowly shrinking interval is not a prescribed differentiation scale. A componentwise reconstruction certificate is not a common long-time spectral estimate. A small positive source mass is not pointwise source smallness. The manuscript increasingly distinguishes these statements accurately, but the submission remains organized around a theorem which still requires the residual criterion.

The pointwise roof-conditioned bridge also remains open because its denominator and numerator would require the missing density theorem at the same roof value.

## 19. Weighted statements

For the endpoint-decision source, arbitrary bounded measurable insertions are handled cleanly by domination:

```text
|a| <= M.
```

This gives both the pointwise density bound and the all-band correction with a factor `M`.

This should not be conflated with the inherited protected regular theorem, whose derivative estimate requires an endpoint-gradient budget. Nor does the endpoint-decision domination theorem provide Gaussian amplitudes for arbitrary path selectors.

The remaining incidence, clearance, and interior-decision residuals have only variation-mass domination for bounded insertions. A complete weighted raw theorem and a pointwise roof-conditioned path bridge therefore remain unproved.

## 20. Novelty and top-four significance

The new endpoint-decision argument is technically interesting. It combines

- a moving-family arithmetic local upper bound;
- finite-history positive endpoint envelopes;
- exact physical roof transport across discontinuous section decisions;
- a finite occupation allowance used only in an upper comparison;
- and critical completion outside the return section.

This is not merely formal bookkeeping.

The manuscript, however, is now a very large compilation of stationary local laws, compact-family action estimates, return-window laws, arithmetic exact-index interval laws, bridge theorems, phase posteriors, coefficient reconstructions, height bounds, critical-cluster estimates, protected inversion, and partial boundary deconcentration. The central raw-density theorem remains incomplete.

At the requested four-journal benchmark, the editorial burden is therefore too high relative to the completed principal theorem. The finished interval, bridge, posterior, stationary, and protected-boundary results may support a strong focused dynamics/probability paper after independent verification and substantial reorganization. They do not yet amount to a complete top-four raw local inversion theorem.

A broader general theorem could change this assessment, but revision 47 remains specialized to the same triangular finite-horizon Lorentz family, its moving section, and the inherited anisotropic-space architecture.

## 21. Independent specialist verification

No independent human specialist audit has been obtained.

The new load-bearing items requiring expert review include

1. the full-occupation endpoint local upper bound without compulsory section factors;
2. scalar amplitude continuity through arithmetic transitions;
3. smooth positive endpoint envelopes uniform on the moving radius family;
4. continuation after deleting only finitely many section checks;
5. the scaled distance derivative at rectangle corners;
6. physical-word gluing of the roof vector field across section cuts;
7. global flow injectivity and coarea multiplicity;
8. the ambient-source normalization after initial-section exit;
9. low-gradient completion to critical centers outside the section;
10. disjointness and single charging of physical critical collars;
11. the occupation allowance in the collar comparison;
12. and the first-defect mass estimates under the exact source conventions.

Inherited items which remain load-bearing include the contact second variation, endpoint injectivity, relative distortion, the full occupation-torus anisotropic inequalities, physical projection formula, integer-holonomy argument, moving spectral peaks, arithmetic transition expansion, and bridge tightness.

Finite models, source hashes, compilation, and rendering do not certify these continuum arguments.

## 22. Required mathematical work for another revision at the same benchmark

A subsequent revision seeking the same benchmark should address the following.

1. **Prove the residual pointwise criterion.**  
   Establish the `m^{-2}`-scale signed correction estimate for the sum of first bad incidence, clearance, and interior-decision sources.

2. **Treat physical-word boundaries.**  
   Develop a replacement for the endpoint section-cut flow that remains valid, or gives a controlled boundary term, when an incidence or competing-hit decision changes the physical collision word.

3. **Control interior decisions pointwise.**  
   The exponentially small mass in endpoint depth must be converted into a roof-density or Fourier-norm estimate with constants compatible with the ordered `J(B)` limit.

4. **Keep the arithmetic main term.**  
   Either prove the concrete zero-residue condition or formulate the final density theorem with `mathfrak a_R` at fixed radius and `mathcal L_{m,R}` uniformly.

5. **Close a complete weighted theorem.**  
   If a pointwise conditioned path theorem is retained as a goal, provide numerator and denominator estimates for the same roof value and the same residual source.

6. **Provide independent expert verification.**  
   The anisotropic spectral and singular-geometry chains are too load-bearing to rely only on source qualification and finite diagnostics.

7. **Strengthen the novelty comparison.**  
   State theorem by theorem which completed results go beyond existing billiard local-limit and suspension-flow frameworks.

8. **Reduce the central route.**  
   Present one completed principal theorem. Move unresolved or conditional companion programs out of the main route unless they are closed.

## 23. Technical comments

1. Keep the collision count `m`, return index `n`, roof bandwidth `B`, protection scale `epsilon` or `eta`, endpoint depth `J`, and gradient cutoff `delta` visually distinct.
2. State explicitly whenever the source changes from the return probability to the ambient measure `nu/c`.
3. Retain the convention that the occupation sums times `0,...,m-1`; terminal membership at `m` is not an additional summand.
4. Keep the finite occupation allowance on the upper-comparison side only.
5. Do not describe the allowance as preservation of the return index under the roof flow.
6. Keep `J`, `epsilon`, `eta`, and the roof window fixed before the collision limit in every invocation of the local upper bound.
7. Do not infer a theorem uniform in `J(m)` from the finite-history endpoint envelopes.
8. State the dependence of collision thresholds on the fixed smooth endpoint approximants.
9. Preserve the almost-everywhere qualification in the scaled section-distance derivative at rectangle corners.
10. When using the high-gradient flow, list all physical and retained decision boundaries which the flow is forbidden to cross.
11. Keep the factor `1/c` visible in the coarea comparison after the initial endpoint leaves the section.
12. In the low-gradient argument, state again that each physical collar is charged once.
13. Do not enlarge the occupation allowance a second time after critical completion.
14. The all-band endpoint result is a convolution consequence, not a growing-band spectral theorem.
15. The finite trace-jump corollary does not control the sum of all absolute jump heights.
16. Keep the first-defect sets defined by the first factor strictly below one, so the smooth transition region is included.
17. Variation-mass estimates should not be described as pointwise bounds.
18. The signed residual criterion concerns the sum of the three corrections; no separate vanishing theorem is presently available.
19. Do not infer cancellation of the residual corrections from positivity of their pre-convolution sources.
20. Keep `epsilon(B)` and `J(B)` fixed before the collision limit; they are not count-dependent rates.
21. The source-manifest flag for a pointwise boundary bound should remain visibly qualified as an exponential finite-count height estimate.
22. Preserve `mathfrak a_R` and `mathcal L_{m,R}` in every candidate raw main term.
23. A fixed interval theorem should not be cited as a pointwise roof-density theorem.
24. Source qualification should remain separated from continuum proof certification.

## 24. Final assessment

Revision 47 is a serious and mathematically constructive response to the revision-46 report.

It proves pointwise `m^{-2}` deconcentration for a genuine collapsing endpoint section-decision source, while retaining the original exact labels. It controls that component's complete signed correction at all bandwidths and for arbitrary bounded insertions. It also gives a clean positive first-bad-margin resolution and an explicit ordered endpoint-depth ledger.

I found no decisive error in the new modules within the scope of this review.

The paper nevertheless remains short of the theorem which governs its title and raw-inversion architecture. The incidence, clearance, and interior-decision residual corrections are not controlled pointwise; their small masses do not close the criterion. The complete raw roof-density LLT and pointwise roof-conditioned bridge remain open, and the concrete arithmetic residues are not proved trivial.

Subject to independent specialist verification, the completed stationary, interval, bridge, posterior, protected-inverse, critical-cluster, and endpoint-decision results could form a strong focused paper. They do not yet constitute a complete top-four raw local inversion theorem.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
