# External top-four referee report on A2-DYN revision 84

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v84-referee-response-2026-10-12`, `revision/a2-dyn-v84-referee-copy-2026-10-12`  
**Reviewed commit:** `f94ff549308db3fbba2087be0852c3f1e4d0739a`  
**Reviewed repository tree:** `3e36bd21be97e51d3f4a3f28e2bee46ca1de74c7`  
**Active manuscript directory:** `papers/A2-DYN-v84-referee-response`  
**Active mathematical source:** one hundred ninety-five numbered core modules; revision 84 adds modules 193--195  
**Frozen revision-83 author baseline:** `658f42b2ce6c177687208287201abb7a86193e37`  
**Frozen revision-83 paper tree:** `5422c924a1a26006a2cd39c5776eae56a684849c`  
**Controlling report:** `reviews/a2-dyn-v83-external-top4-review-2026-10-12/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `e6bf3cece623a6c7c02a160b43c4dd8c5fe569e1` / `d5cb27a2f9bd769241c32941d77a08c5b438803f`  
**Exact-source qualification runs:** response `38189870318`; referee-copy `38189885108`  
**Date:** 12 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 84 is a genuine theorem-bearing response to the revision-83 report. It does not merely rename a local-mass remainder or infer an essential-height estimate from small total mass. The new manuscript proves an ordered essential-height bound for every long-residence component of the actual first-exit surface, proves a separate ordered height estimate for the change of physical angular density between the two ends of every short noncritical regular segment, treats the complete short component with a grazing incoming end, improves the local-mass exponent for the short critical surface, and isolates the microscopic fractional tail as a canonical concentration charge with an outer-scale rigidity property.

I audited the new modules

- `core/193_backward_residence_surface_height.tex`;
- `core/194_paired_boundary_optical_transfer.tex`;
- `core/195_canonical_concentration_and_endpoint.tex`;

and their interfaces with the stated inherited inputs in modules 187--192 and the dependency appendix. I found no decisive counterexample, no sign error in the residence kernel, no reversal of the roof-shift direction, no illicit collision-dependent Fourier cutoff, and no hidden promotion of a local-mass estimate to an essential-height theorem in the portions that are declared proved.

The long-residence argument is a real advance. If an outgoing face has backward regular lifetime greater than `2r`, then its width-`r` exit kernel persists, with a fixed factor, throughout a full backward roof interval of length `r`. This converts the already proved local surface-mass estimate into an essential-height estimate by a genuine persistence mechanism. The manuscript obtains

```text
L_r(t) <= (2/r) integral_{t-r}^t Fbar_{2r}(v) dv,
```

and hence

```text
limsup_m sup_{R,n,k} m^2 ||L_r||_infinity <= C_eta r^(1/32).
```

This closes the entire long-residence part of the revision-83 surface obstruction.

The short noncritical transfer argument is also substantive. The manuscript differentiates the full physical angular density

```text
A = omega / (4 pi c_* chi),
```

rather than only the optical factor `omega`. Radial monotonicity keeps the entire selected short segment above a positive gradient cutoff fixed by `r`. The variation between the outgoing and incoming traces is then paid by an inherited positive first-inverse-gradient source estimate. This gives

```text
limsup_m sup_{R,n,k} m^2
  ||S_r^nc - J_r||_infinity <= C r.
```

For a grazing incoming end the incoming angular trace is zero, so the corresponding outgoing component is controlled outright.

These are meaningful achievements. They significantly sharpen the geometry of the remaining pointwise obstruction.

The negative recommendation is nevertheless unavoidable. Revision 84 explicitly leaves three nonnegative quantities unproved:

1. the ordered essential height of the paired incoming assignment on short nongrazing-to-nongrazing segments;
2. the ordered essential height of the short critical outgoing surface; and
3. the vanishing of the canonical microscopic concentration charge.

The final endpoint theorem is

```text
E_M <= C_M B^(-1/192)
       + C J_M(r) + C K_M(r)
       + C_eta A_{eta,M}
       + C_eta r^(1/32)
       + C_Theta (1 + epsilon(B)^(-1)) sqrt(r).
```

Here `J_M(r)` is the paired short nongrazing height, `K_M(r)` is the short critical surface height, and `A_{eta,M}` is the canonical microscopic concentration charge. None is proved to vanish in the unrestricted Lorentz family.

The canonical-charge theorem makes the remaining tail issue sharper, but not smaller. It shows that the dyadic tail height is invariant under dyadic changes of the outer width and is comparable to one fixed charge. Consequently, merely choosing a smaller reconstruction width cannot pay a nonzero charge. A source-specific uniform-integrability estimate is still required.

Similarly, the short critical surface has very small local mass on intervals of length `r`, with exponent `385/256`, but the manuscript correctly does not infer an essential-height estimate from that mass. The same distinction that drove the preceding referee reports therefore remains decisive.

Revision 84 has proved that large portions of the obstruction are small. It has not proved that the complete obstruction is small. The original exact-label pointwise raw local limit theorem and its same-roof consequences remain unproved.

## 2. Frozen source, chronology, and preservation

Both reviewed author branches resolve to

`f94ff549308db3fbba2087be0852c3f1e4d0739a`.

The Git tree at that commit is

`3e36bd21be97e51d3f4a3f28e2bee46ca1de74c7`.

The active source directory is

`papers/A2-DYN-v84-referee-response`.

The author commit descends directly from the controlling revision-83 review commit. The frozen mathematical baseline is revision 83 at

`658f42b2ce6c177687208287201abb7a86193e37`,

with paper tree

`5422c924a1a26006a2cd39c5776eae56a684849c`.

The source manifest records 192 inherited core modules and 195 active core modules. The three new modules are precisely 193--195. The focused article is `main.tex`; the complete inherited article is assembled as `supplement.tex`. All inherited cores, Python sources, appendices, bibliographies, provenance records, and the preceding article are declared byte-preserved.

The manuscript consistently retains the original exact-label pointwise target, the original section, guard, source normalization, arithmetic reference, zero classes, and actual-return interpretation. It does not substitute a collision-count window, roof interval theorem, pooled occupation class, or removed-source statement for the organizing endpoint.

The active source manifest accurately leaves false the flags for

- complete paired short nongrazing surface-height decay;
- complete short critical surface-height decay;
- vanishing canonical microscopic concentration charge;
- the full raw return LLT;
- the pointwise roof-density LLT;
- unrestricted same-roof pair bridges;
- forward essential-likelihood convergence;
- independent human review; and
- formal proof certification.

This source-level honesty is important and should be preserved.

## 3. Qualification evidence and its boundary

The final exact-SHA workflows completed successfully on both author refs:

- response branch run `38189870318`;
- referee-copy branch run `38189885108`.

Both runs identify the reviewed SHA `f94ff549308db3fbba2087be0852c3f1e4d0739a` and tree `3e36bd21be97e51d3f4a3f28e2bee46ca1de74c7`.

According to the workflow and validation documents, the qualification checks include

- the frozen revision-83 paper tree and controlling report blob;
- preservation of all inherited files;
- inclusion of all 195 core modules across the article and supplement;
- ordinary and optimized finite diagnostics;
- native TeX compilation of the focused article and complete supplement;
- stabilized references and warning checks;
- recorder coverage; and
- source-bound rendering evidence.

These checks are meaningful evidence of source identity, finite algebra, and typesetting integrity. They do not certify

- the inherited local surface-mass theorem;
- cutoff-uniform first-inverse-gradient insertion;
- completeness of the physical first-exit sheet parametrization;
- injectivity or measurable multiplicity of the segment-to-interior correspondence;
- one-sided optical traces at all physical boundaries;
- the full anisotropic spectral pipeline; or
- the three remaining endpoint estimates.

The manuscript and audit map correctly state this boundary.

## 4. Scope of this review

The complete archive now contains 195 core modules and a 646-page supplement. I have not attempted to re-prove every historical theorem. The substantive audit concentrates on

1. the actual residence kernel and its physical lifetime convention;
2. the persistence inequality for long-residence faces;
3. conversion of local surface mass to long-residence height;
4. differentiation of the full physical angular density;
5. the positive-gradient cutoff on short noncritical segments;
6. summation over paired incoming/outgoing faces without a word-count factor;
7. the treatment of grazing incoming ends;
8. the short critical local-mass estimate;
9. the reduction of full surface height to two short-segment heights;
10. the canonical microscopic charge and dyadic rigidity;
11. the final exact-label pointwise error budget;
12. the legal order of all limits and cutoffs; and
13. source and workflow identity.

The inherited spectral, arithmetic, coarea, fractional-source, local-mass, positive-remainder, path-remainder, and collision-to-return chains are treated as source-pinned inputs, not as independently recertified results.

## 5. The complete residence kernel

For an outgoing nongrazing face `y`, the manuscript writes

```text
b(y) = F(y),
l(y) = tau^-(y),
a(y) = b(y) - l(y).
```

The maximal backward regular segment occupies the roof interval `(a,b)`. The averaged first-exit kernel is

```text
k_r(t;y) = (1 - (b(y)-t)/r)_+ 1_{a(y)<t<b(y)}.
```

This formula follows from averaging the first-exit indicator over widths `0<h<r`. It keeps the original outgoing-face normalization and counts no later re-entry. The lifetime belongs to the same exact physical event and maximal regular segment.

I find the kernel formula and its endpoint conventions coherent.

One point should remain explicit in any subsequent version: the incoming endpoint `a` may be a true physical face or an interior critical endpoint removed from the regular-flow domain. It is not an artificial chart seam. This distinction is essential to the later short-segment decomposition.

## 6. Long-residence persistence

Suppose `k_r(t;y)>0`, put `s=b(y)-t`, and assume `l(y)>2r`. For `0<u<r`,

```text
s+u < 2r < l(y)
```

and

```text
k_{2r}(t-u;y)
 = 1 - (s+u)/(2r)
 >= (1/2)(1-s/r)
 = (1/2) k_r(t;y).
```

Integrating this inequality first in `u` and then over the same outgoing faces gives the persistence estimate.

The direction of the shift is correct: one moves backward in roof from `t` to `t-u`. The comparison uses the same face and the same exact event. No new word or re-entry is introduced.

This is the right mechanism to turn a local-mass theorem into an essential-height theorem. It is not the invalid inference that small mass on short intervals alone forces small density height.

Applying the inherited surface local-mass estimate at width `2r` and interval length `r`, and dividing by `r`, yields the printed exponent `r^(1/32)`. I found no arithmetic error in this step.

The conclusion

```text
F_all(r) = S_short(r) + O(r^(1/32))
```

in ordered height is therefore a genuine localization of the full surface obstruction to short maximal regular segments.

## 7. Full physical angular-density variation

On a regular angular sheet the manuscript uses

```text
A(u,theta) = omega(u,theta)/(4 pi c_* chi(u,theta)).
```

The derivative estimate

```text
|partial_u A| <= C A I_m/z
```

combines the inherited optical sensitivity of `omega` with a cubic-action bound for the motion of `chi`. This is structurally correct: differentiating only `omega` would miss an equally physical Jacobian factor.

The manuscript also states that an incoming endpoint with positive limiting `z` and a vanishing internal incidence has trace `A(a+,theta)=0`, because `omega` tends to zero while `chi` remains bounded below. At a fully nongrazing incoming endpoint, the one-sided regular reflection equations provide a trace.

I found no formal sign inconsistency here. This is nevertheless a load-bearing specialist point. The next audit should verify, for every allowed physical endpoint type, that

- the selected incidence identity really forces the stated behavior of `omega`;
- the lower bound for `chi` remains valid up to the one-sided face;
- the angular parametrization has no hidden multiplicity; and
- no continuation through a forbidden first-hit or section-decision boundary is being used.

The present text explicitly disclaims such a continuation, which is appropriate.

## 8. The noncritical short-segment cutoff

The manuscript divides short segments by the outgoing condition

```text
z(b-)^2 >= 8 Lambda_circle r.
```

Since the segment length is at most `2r` and the radial derivative of `z^2` is bounded above by `2 Lambda_circle`, every point on a noncritical short segment satisfies

```text
z(u) >= c_r = 2 sqrt(Lambda_circle r).
```

The constants are consistent:

```text
8 Lambda r - 4 Lambda r = 4 Lambda r.
```

Thus the whole segment remains in a positive-gradient region. The cutoff `c_r` depends on the previously fixed outer width `r`, not on the collision count.

This ordering is essential. The manuscript does not evaluate a fixed-band estimate at a collision-dependent cutoff.

## 9. Paired incoming/outgoing transfer

For each selected noncritical short segment, the manuscript keeps the same exit-window kernel and replaces the outgoing angular density by the incoming angular density. The resulting positive assignment is denoted `J_r`.

The variation inequality gives, on one segment,

```text
|A(b-,theta)-A(a+,theta)|
 <= C integral_a^b A(u,theta) I_m(u,theta)/z(u,theta) du.
```

Whenever the exit-window kernel is nonzero, the full short segment lies in `(t-2r,t+2r)`. The manuscript then sums the variation integrals over the physical source and invokes the positive truncated source `v^{c_r}`.

The conclusion

```text
|S_r^nc(t)-J_r(t)|
 <= C integral_{t-2r}^{t+2r} v^{c_r}(u) du
```

is plausible and the resulting height bound `Cr` follows from the stated fixed-window estimate.

The most delicate point is the assertion that the map from selected outgoing faces to intermediate states on their incident segments has multiplicity one, so no word-count factor appears. Physically, uniqueness of the regular first-exit flow suggests this is correct. For a top-tier proof, however, I recommend replacing the current prose with an explicit measurable parametrization statement:

- specify the disjoint union of angular sheets;
- define the map `(face,theta,u)` to the collision source;
- state its measurable image;
- prove injectivity outside the already excluded null set; and
- identify the pushforward density exactly.

This would make the no-word-count step auditable without relying on geometric intuition.

A second load-bearing input is that the leading constant in the fixed-window estimate for `v^c` is independent of every positive cutoff `c`. Since `c_r` tends to zero with `r`, any hidden cutoff dependence would destroy the final `Cr` estimate. The active article states the uniformity explicitly and points to the inherited source. A specialist rereview should verify that source line by line.

I do not identify a contradiction here; these are proof-verification requirements.

## 10. Grazing incoming ends

When the incoming endpoint is grazing, the incoming trace is zero. Restricting the positive variation argument to this subfamily therefore bounds the entire outgoing source by `Cr`.

This is stronger than bounding only an outgoing-minus-incoming difference and is a useful closure of a complete physical component.

Again, the validity rests on the exact one-sided optical trace. No lower-incidence corridor or removed source is introduced in the displayed proof.

## 11. The short critical surface

The critical part is defined by

```text
z(b-)^2 < 8 Lambda_circle r.
```

Radial monotonicity keeps `z` below the corresponding `b_r` throughout the selected segment. The proof then uses the unweighted small-gradient exact source and the truncated fractional source.

For an interval `J` of fixed length `L`, the manuscript obtains

```text
limsup_m sup_{R,n,k} m^2 integral_J K_r(t) dt
 <= C L b_r^alpha
    + C_eta (L+r) r^((1+eta)/2) b_r^(alpha-eta).
```

With `L=r` and `b_r` of order `sqrt(r)`, the leading exponent is

```text
1 + alpha/2 = 385/256.
```

The arithmetic is correct.

This is a strong local-mass estimate. It is not an essential-height estimate. The manuscript repeatedly states that distinction and does not promote the corresponding flag.

The remaining task is therefore not a cosmetic improvement of the exponent. One must rule out concentration of this mass in roof intervals much narrower than `r`, uniformly after multiplying by `m^2` and taking the exact-label supremum.

## 12. Reduction of full surface height

The new estimates imply

```text
F_all(r) <= J_M(r) + K_M(r) + C_eta r^(1/32).
```

Conversely, the two short assignments are bounded by the full surface height up to the controlled transfer difference. Hence full surface-height decay is equivalent to decay of the two explicitly identified short-segment heights.

This is a useful structural reduction. It is not yet a vanishing theorem because `J_M(r)` and `K_M(r)` remain unestimated in essential height.

The terminology “paired transfer” should not obscure this point. The proved small quantity is the change between outgoing and incoming traces. The incoming paired assignment itself is still positive and may retain large roof concentration. Exact pairing is not the same as cancellation in the nonnegative endpoint budget.

## 13. Canonical microscopic concentration charge

The manuscript defines

```text
A_{eta,M}
 = lim_{delta downarrow 0}
   H_M(P_{eta,delta} v^eta),
```

where the complete finite-count potential remains inside the normalized essential-height functional before the microscopic width is removed.

The dyadic annuli in the tail partition `(0,delta_N]`, so at finite count

```text
T_{eta,r,N}
 <= P_{eta,delta_N} v^eta
 <= 2^kappa T_{eta,r,N}.
```

Taking the ordered height before `N` tends to infinity gives comparability between the tail and the canonical charge. The identity

```text
T_{eta,r/2,N} = T_{eta,r,N+1}
```

then yields dyadic outer-width invariance.

I find this argument internally coherent. It correctly avoids commuting an essential supremum or collision limsup with an infinite sum.

The theorem has an important negative implication: a nonzero microscopic charge cannot be reduced by choosing a smaller dyadically related outer width. The remaining requirement is genuine uniform integrability or an equivalent source-specific estimate. The finite-count fact that truncated potentials tend to zero almost everywhere is irrelevant to the ordered charge.

Thus the charge theorem clarifies the blocker but does not close it.

## 14. The final endpoint budget

The final theorem combines the scalar positive remainder, the surface reduction, and the canonical-charge comparison. It preserves the legal order

1. fix `B`;
2. fix `epsilon(B)`, `r`, `c_r`, `eta`, and all auxiliary bands;
3. take the collision-count limit and exact-label suprema;
4. enlarge auxiliary bands;
5. choose the outer relation `r(B)`; and
6. send `B` to infinity last.

I found no reversal of this order in the new modules.

The theorem proves that the original exact-label pointwise LLT would follow from

```text
A_{eta,M} = 0,
J_M(r) -> 0,
K_M(r) -> 0
```

as `r` tends to zero, with the prescribed outer choices.

Those are three substantive analytic assertions, not notational cleanup. None follows from the proved local masses, weak-`L^q` estimates, fixed-width averages, or finite-count integrability.

The following central conclusions therefore remain unavailable:

- the unrestricted scalar exact-label pointwise raw LLT;
- a pointwise roof-density LLT;
- a uniform positive pointwise denominator on every positive arithmetic class;
- same-roof collision path conditioning;
- the actual-return path bridge after clock transfer; and
- forward essential arithmetic likelihood convergence.

The manuscript properly leaves these statuses false.

## 15. Exact physical data and source scope

The new proofs continue to use the actual one-sided first-exit surface. The paired incoming trace belongs to the same maximal regular exact-event segment as the outgoing face. Initial, internal, and terminal section decisions remain genuine boundaries. Competing-hit boundaries are not erased. Chart seams are not promoted to physical exits.

No pooling of exact labels, displacement classes, occupation classes, or arithmetic zero classes occurs in the statements reviewed here.

The long-residence proof and noncritical transfer proof both use positive source comparisons. They do not obtain smallness by cancellation of unrelated signed sources.

This is the correct scope for the organizing theorem.

## 16. Historical dyadic notation

The article declares one active offset convention in module 192 and marks the ambiguous historical module-189 display as superseded at its supplement inclusion while preserving the original bytes.

This is an acceptable provenance solution. The active theorem should remain self-contained enough that no reader needs the superseded display to reconstruct the argument.

## 17. Mathematical significance at the requested benchmark

The manuscript now contains a substantial body of original geometric and analytic work: exact return arithmetic, operator constructions, positive source decompositions, coarea transport, fractional inverse-gradient sources, first-exit surface geometry, residence persistence, and paired angular transfer.

Revision 84 materially improves the endpoint analysis. In particular, it proves actual essential-height estimates on large complete physical subfamilies rather than replacing the target by an averaged theorem.

Nevertheless, the requested four-journal benchmark is a theorem benchmark, not a progress-ledger benchmark. The title and opening continue to organize the paper around an unrestricted exact-label pointwise raw local limit theorem. That theorem is not proved.

The remaining quantities are not obviously lower-order technicalities. Each represents a possible concentration mechanism at a scale invisible to the already proved fixed-width and weak-norm estimates. The canonical-charge rigidity theorem itself demonstrates that one of them cannot be removed by a formal choice of smaller scale.

At this level, the paper needs either

1. a proof of all three remaining vanishing statements and hence the full endpoint; or
2. a separate, broad theorem of independent significance whose statement and applications do not depend editorially on the unfinished Lorentz endpoint.

Revision 84 supplies neither yet.

## 18. Presentation and architecture

The focused article is substantially easier to read than the historical archive. It states the active inputs, proves the three new modules, and gives the current endpoint budget. The complete preceding article remains available in a separate supplement.

This is the right direction. Before a formal submission, however, I recommend a stricter separation between

- the journal theorem and indispensable proof;
- a technical supplement containing inherited machinery actually used;
- provenance and historical revision material; and
- finite diagnostics and build records.

The current 646-page supplement remains too large to function as an ordinary top-four supplement without an exceptionally clear dependency map and independent specialist verification.

## 19. Required mathematical changes before another top-four review

A further revision should address the following points.

### 19.1. Prove the paired nongrazing short-face height decay

The manuscript controls `S_r^nc-J_r`, not `J_r` itself. It must prove

```text
J_M(r) -> 0
```

in the exact ordered essential-height norm, uniformly in radius and exact labels, with all widths fixed before the collision limit.

A viable proof must exploit more than equality of incoming and outgoing optical mass. It must exclude concentration of the paired positive trace in arbitrarily narrow roof intervals.

### 19.2. Prove the short critical surface-height decay

The interval-mass exponent `385/256` is not enough. The paper needs a genuine height or uniform-integrability mechanism for the critical outgoing surface, preserving the original physical branches and exact labels.

### 19.3. Prove the canonical charge is zero

The dyadic rigidity theorem reduces all outer widths to one charge. The next revision must provide a finite-count envelope, a Carleson-type estimate, a monotonicity formula, or another source-specific argument that actually gives

```text
A_{eta,M}=0.
```

A collection of separate fixed-width collision limsups will not suffice.

### 19.4. Make the no-word-count transfer map fully formal

State and prove the measurable injective parametrization used to sum segment variation over the physical source. Include the treatment of angular-sheet multiplicity and all excluded null sets.

### 19.5. Re-audit cutoff uniformity

Give a direct theorem-level citation or restatement proving that the leading constant in the `v^c` fixed-window estimate is independent of every positive cutoff `c`. This is essential because `c_r` tends to zero.

### 19.6. Obtain independent specialist review

At minimum, the following should be independently checked by experts:

- the inherited anisotropic insertion and fixed-cutoff source estimate;
- the coarea surface normalization;
- one-sided optical traces;
- maximal regular segment disintegration;
- injectivity of paired sheets;
- the critical-source local-mass chain; and
- the canonical-charge limit order.

### 19.7. Promote downstream conclusions only after scalar closure

The same-roof path and likelihood statements should remain conditional until the scalar endpoint is proved. No zero arithmetic class should be normalized.

## 20. Expository comments

1. The notation `L_r` for the long-residence surface assignment is close to the arithmetic reference `mathcal L_{m,R}`. The manuscript warns about this, but a more visibly different symbol would help.
2. State the domain of negative dyadic shifts in the charge theorem directly in the theorem display, not only in prose.
3. In the proof of paired transfer, replace “injective in the physical collision source” by a named lemma with a precise map and sigma-algebras.
4. Restate the cutoff-independent constant in the theorem that invokes it, not only in the preceding input paragraph.
5. Keep the sentence “critical mass is not critical height” near every summary theorem; it is the central logical distinction.
6. The supplement should include a compact table mapping each active input statement to its original theorem, exact equation, and proof page.
7. The active article should state the number and nature of unresolved nonnegative quantities in the abstract or final theorem discussion.
8. The exact-SHA qualification records should remain separated from mathematical certification language.

## 21. Final assessment

Revision 84 is a substantial mathematical advance over revision 83.

It proves

- an exact residence-kernel representation;
- an ordered essential-height estimate for all long-residence outgoing faces;
- a full angular-density variation formula;
- an ordered `Cr` bound for the outgoing-minus-incoming transfer on every short noncritical segment;
- the complete grazing-incoming short estimate;
- a sharper short-critical local-mass bound; and
- a canonical microscopic charge with dyadic outer-scale rigidity.

I found no decisive flaw in the new proofs at the level of this referee-style audit. Their most delicate imported constants, trace assertions, and multiplicity statements still require human specialist verification.

The revision does not prove

- decay of the paired short nongrazing height;
- decay of the short critical surface height;
- vanishing of the canonical microscopic concentration charge;
- the unrestricted exact-label pointwise raw LLT; or
- its unconditional path and likelihood consequences.

The full organizing theorem therefore remains open within the submitted manuscript.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
