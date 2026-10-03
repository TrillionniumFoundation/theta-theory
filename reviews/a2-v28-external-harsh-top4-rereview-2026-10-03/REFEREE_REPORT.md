# External top-four referee report on A2 v28

**Manuscript:** Qian Qi, *Reference-free certification from intrinsic boundary laws*  
**Reviewed revision:** `revision/a2-v28-local-period-recognition-2026-10-03`  
**Equivalent referee-copy alias:** `revision/a2-v28-referee-copy-2026-10-03`  
**Reviewed commit:** `3ac2df58d175010f338dd6ae8af84158c1590d20`  
**Reviewed tree:** `c3afed66d39b03ea05b72fde9be13ee03b3e82b9`  
**Immediate author base:** A2 v27, commit `f230e014911f3b7104db0ec742969789ed5a88c9`  
**Controlling preceding external report:** `24b9c5f6a586a35975e6f6b67d25ec431390f57a`  
**Manuscript directory:** `papers/A2-v28-local-period-recognition`  
**Date:** 3 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision or a formal proof certificate.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

Version 28 is a genuine and mathematically substantive advance over the previously reviewed programme. The decisive new point is not the already established v27 fixed-aperture theorem, but the removal of its individual translation-type separation hypothesis. The paper now permits repeated congruent obstacles, arbitrary body symmetries and a nonprimitive bounded period presentation. It recovers the intrinsic full translation group of the physical obstacle union by testing candidate translations on a complete central patch rather than by naming an individual body shape. It then separates three logically distinct conclusions:

1. exact determination with no positive mismatch margin;
2. uniform finite-confidence recovery on classes with a numerical nonperiod patch-defect margin; and
3. pointwise eventual recovery when that numerical margin is unknown.

That separation is correct and important. The repeated-disk family also correctly explains why the discrete primitive lattice and orbit count cannot obey a uniform stability modulus across a translation-symmetry increase.

On the new v28 core audited in detail, I found no fatal counterexample. The first-impact support argument, finite central-patch completeness, two-sided local-to-global period criterion, quotient-index bound, protected generation of the full lattice, repeated-shape orbit count, noisy patch comparison, bounded-denominator rational locking, Hermite reconstruction, compensated smoothing and repeated-disk symmetry jump are coherent under the stated hypotheses. The retained v27 fixed-aperture proof is likewise consistent on the points relevant to the new theorem. Independent finite diagnostics accompanying this report support the displayed finite group, arithmetic and error inequalities. I therefore do **not** base the negative recommendation on a known false central theorem.

The negative recommendation is instead a top-four editorial judgment. The principal exact datum is exceptionally direct: resettable launches are made from chosen positions in a known laboratory square with independent chosen directions, and the support of the resulting first-impact position law is known. The local flux construction makes every boundary arc in a protected finite patch appear in that support. Thus the datum directly exposes the relevant physical boundary components in one common Euclidean frame. Once that finite patch is available and periodicity under some numerically bounded presentation is assumed, the new period theorem becomes an elegant finite local-symmetry and lattice-recovery argument.

This is serious mathematics, and the removal of shape separation is a real improvement. It is nevertheless not, in my judgment, the kind of indirect rigidity phenomenon, broad structural principle or transformation of a major area that reaches the exceptional threshold of the four journals named above. The finite-confidence theorem additionally requires a numerical global patch-mismatch margin, certified impact localization of order `nu^(3/2)`, strong separation/curvature/smoothness bounds and an a priori bounded lattice presentation. Its launch exponent is obtained from classical boundary coverage, convex-hull approximation and compensated smoothing; no minimax or end-to-end complexity theorem is claimed.

The fixed-aperture theorem and the repeated-motif period criterion could form a strong, focused specialist-journal paper after a fresh human proof review and the editorial corrections below. I would not recommend another open-ended revision cycle at the requested four-journal benchmark.

## 2. Frozen source and chronology

The two v28 branch names listed above resolve to the same author head

`3ac2df58d175010f338dd6ae8af84158c1590d20`

with tree

`c3afed66d39b03ea05b72fde9be13ee03b3e82b9`.

Its parent is the v27 author commit

`f230e014911f3b7104db0ec742969789ed5a88c9`.

The controlling retrieved report is the v26 external report at

`24b9c5f6a586a35975e6f6b67d25ec431390f57a`,

which reviewed v26 author commit

`8c6f1113296c5401258ff052e5ce734fabfb3909`.

The author correctly does not invent a v27 referee report. Version 27 was an intervening author revision that introduced the fixed-aperture first-impact route. Version 28 builds on that route and addresses the repeated-shape/nonprimitive-presentation issue. For this reason the present audit read both the new v28 section and the active v27 fixed-aperture section; it does not count the v27 result as a new v28 contribution.

The source pins record the exact retained v27 tree as

`c9e18bc786b795e61a6ed8c0048249bb14713a04`.

All eight inherited v27 core blobs remain active and byte-identical. The only new mathematical core is

`core/00_local_period_recognition.tex`.

No `revision/a2-v29...` branch existed when this review branch was created. The review branch starts directly from the frozen v28 author head and adds files only under

`reviews/a2-v28-external-harsh-top4-rereview-2026-10-03/`.

No author source, author workflow, preceding report, retained volume or unrelated paper is modified by this review.

## 3. Observation category and principal theorem

The new global route uses one fixed laboratory square. Each attempt chooses a launch position uniformly in that square and an independent direction uniformly on the circle. A solid start, no collision before the fixed cutoff, or a first impact outside the retained inner region is recorded as failure. Otherwise only the first-impact position is retained, with a certified spatial error in the finite experiment.

The route does **not** use later collisions, return selection, collision angles, boundary arclength labels, endpoint histograms, free-area normalization or adaptive recentering. These are genuine reductions relative to the record-local route retained later in the paper. The common laboratory frame, resettable chosen launches, known square, fixed short-time cutoff, bounded period-presentation prior and calibrated collision localization remain part of the information contract.

For the repeated-shape class the table has some unknown presentation

\[
\mathcal O=\bigcup_{i=1}^{r}(C_i+\Lambda_0),
\qquad \Lambda_0=L\mathbb Z^2,
\]

with bounded `L` and `L^{-1}`. The presentation need not be primitive. The intrinsic period group is

\[
\Pi(\mathcal O)=\{v\in\mathbb R^2:\mathcal O+v=\mathcal O\}.
\]

The exact theorem says that the support of the single first-impact position law determines the whole union, `Pi`, the number of component orbits under `Pi`, and the free area of a primitive cell.

This theorem should be read accurately. It is not a crystallinity theorem for an arbitrary locally finite set, and it is not rigidity from a passive trajectory or marked spectrum. Periodicity under a bounded presentation is assumed. The support datum then reveals a complete finite boundary patch, and the new mathematics identifies the full translation group from that patch even when one-body shapes do not serve as labels.

## 4. Audit of the exact first-impact reconstruction

### 4.1 Every protected boundary arc is observed

For a point `x` on a boundary arc, launch from `q=x-rv`, with `r` in a fixed interval shorter than the inter-body separation and `v` in a fixed cone about the inward normal. Convexity prevents an earlier hit on the same body, while the physical separation prevents an intervening body. The first-hit coordinate Jacobian contains `cos(phi)`, bounded below on the cone. Therefore every open arc of every relevant component has positive first-impact mass.

The launch square and retained inner square are chosen from the numerical presentation bound, the body diameter bound and the separation bound. Every component needed by the period test has its complete boundary and an exterior launch collar inside the observation region. Hence, for exact data, the support in the protected patch is precisely the union of the relevant physical boundaries.

This argument is sound. It also shows why the exact inverse is informationally direct: the support itself is a boundary sampler. The main inverse difficulty is not recovering a hidden boundary from indirect travel data, but deciding the global period group of the now visible finite motif.

### 4.2 Complete-body selection from the finite patch

Connected support components are convexified. A partial outer component has its hull inside its true body. If the hull's Steiner point lies in the inner selection square, the body itself meets that square; the aperture margins then imply that its whole boundary lies in the fully observed region. Thus every retained hull is a complete physical component.

The same argument is used in the noisy theorem on the simultaneous coverage event. I found no missing “closed fragment” assumption in this selection step.

## 5. Audit of the local-to-global period criterion

For translated bodies in the common laboratory frame, the manuscript uses

\[
d_*(C,D)=\|z_C-z_D\|_\infty+
          \|p_C-p_D\|_\infty,
\]

where `z_C` is the Steiner point and `p_C` the centered support function. For a candidate `v`, the central defect tests every component whose center is in a fixed central square, in both the `+v` and `-v` directions.

### 5.1 Why two-sided matching is sufficient

The bounded presentation places a representative of every `Lambda_0`-component orbit in the central square. If every such representative has both a `+v` and a `-v` partner, periodic translation by `Lambda_0` gives

\[
\mathcal O+v\subseteq\mathcal O,
\qquad
\mathcal O-v\subseteq\mathcal O.
\]

The second inclusion, translated by `v`, gives the reverse inclusion. Hence `O+v=O`. The converse is immediate. A single matched pair is not enough, and the paper includes the correct negative control.

This is the key new argument. It is elementary once formulated, but it closes a real logical gap left by individual shape naming.

### 5.2 Full group rather than the supplied sublattice

The full group `Pi` contains `Lambda_0`. Mapping a period coset in `Pi/Lambda_0` to the `Lambda_0`-orbit of a fixed component is injective, since a compact body has no nonzero translational symmetry. Consequently

\[
[\Pi:\Lambda_0]\le r\le r_0,
\qquad
\operatorname{covol}\Pi\ge V_0/r_0.
\]

The quotient action on the `Lambda_0` component orbits is free, so its order divides `r`, and the primitive orbit count is `r/[Pi:Lambda_0]`.

The bounded columns of `L`, together with bounded representatives of all cosets of `Pi/Lambda_0`, occur as root-to-copy differences inside the protected target square. Every accepted difference is a true period by the central-patch test, while this protected list contains generators of `Lambda_0` and representatives of all quotient cosets. Its integer span is therefore exactly `Pi`.

I found no defect in the index or generation argument.

### 5.3 Primitive free area

Once `Pi` and its component orbits have been recovered, the primitive free area is

\[
A_* = \operatorname{covol}\Pi-
      \sum_{j=1}^{r_*}\operatorname{area}(C_j).
\]

This calculation occurs after the period group is known. It does not use area calibration to guess the lattice and is invariant under an externally chosen multiple-cell presentation.

## 6. Audit of the finite-confidence theorem

### 6.1 Simultaneous boundary coverage and hull error

A packing estimate bounds the number of bodies meeting the finite patch. The first-hit flux lower bound on an arc of length comparable to `q`, followed by a coupon union bound, gives full `q`-coverage with

\[
N\lesssim q^{-1}\log(C/(q\delta)).
\]

On this event, separation clusters the localized impacts by physical component and the convex hull satisfies

\[
d_H(P_C,C)\le \kappa_+q^2/2+\varepsilon_x=:e.
\]

The argument correctly counts failures and does not treat the singular impact law as a two-dimensional smooth density.

### 6.2 Noisy patch classification

Measured centers have error at most `2e`, and centered support functions have error at most `3e`. The manuscript obtains a `14e` change bound for each source-target comparison and reserves a further `6e` for certified numerical operations. True periods therefore have measured defect at most `20e`, while a false period in the finite candidate set has measured defect at least `eta-20e`.

With a numerical nonperiod patch margin `eta` and sufficiently small `e`, thresholding at `eta/2` classifies exactly the period candidates. Applying the same test to all central body differences recovers the component-orbit equivalence relation without assigning shape names.

The constants are conservative but coherent. The substantive qualification is that `eta` is global information about all false candidate translations in the central motif. It is pointwise positive for each fixed table because the candidate set is finite, but it need not admit a uniform lower bound near an increase of translation symmetry.

### 6.3 Rational lattice locking

Only vectors already certified geometrically as periods enter the arithmetic stage. A nonzero determinant of two periods is an integer multiple of `covol(Pi)` and hence at least `V_0/r_0`. An independent pair can therefore be detected under small continuous error. Its index in `Pi` is bounded, so every other period has bounded-denominator rational coordinates. Separation of rationals and a finite search recover those coordinates exactly. A column Hermite basis then gives the full lattice and a matched basis with continuous `O(e)` error.

This order of operations is correct. No integer span of noisy real vectors is taken.

### 6.4 Smoothing and sample exponent

The inherited compensated kernel cancels moments through degree three. With `C^6` control,

\[
\|K_h*p_P-p_C\|_{C^2}
 \le C e h^{-2}+C h^4.
\]

The choices

\[
h\asymp\nu^{1/4},
\qquad e\asymp\nu^{3/2},
\qquad q\asymp\nu^{3/4},
\qquad \varepsilon_x=O(\nu^{3/2})
\]

give `C^2` error `O(nu)` and the displayed attempt bound

\[
O\!\left(\nu^{-3/4}\log\frac{C}{\nu\delta}\right).
\]

The exponent algebra and convexity check are sound. The result is an upper bound conditional on the stated apparatus and numerical priors. It is not a minimax theorem or an end-to-end bit-complexity result.

## 7. Unknown margin and the symmetry jump

The manuscript correctly declines to issue a uniform finite certificate when `eta` is unknown. For a fixed table the finite false-candidate set has a positive minimum defect. Fresh dyadic batches, summable coverage errors and a threshold tending to zero more slowly than the geometric error eventually separate true periods from false periods almost surely. This is consistency, not an observable stopping rule on the union of all margin classes.

The repeated-disk example makes the distinction concrete. With disk centers at

\[
(4k,4\ell),
\qquad
(4k+2+t,4\ell),
\]

the full horizontal period is `2` at `t=0` and `4` for small positive `t`. The primitive orbit count changes from one to two. The false exchange shift has patch defect `2t`, which tends to zero as the symmetry increases. Thus the exact discrete invariant is determined at every fixed table but is not uniformly stable across this family.

This example is correct and should remain prominent. It also limits the practical interpretation of the uniform finite theorem: its constants necessarily deteriorate as the table approaches a symmetry jump.

## 8. Independent diagnostics and source qualification

The accompanying `verify_review.py` imports no author module. In ordinary and optimized Python it performs **136,740** checks covering:

- exhaustive nonempty uncoloured `3 x 3` periodic motifs;
- exhaustive two-shape `4 x 2` periodic motifs;
- equality of the two-sided finite-patch test and the independently computed global period group;
- generation of the full group and primitive orbit counts;
- one-sided false-positive controls;
- exact `14e` noisy defect comparisons and threshold separation;
- bounded-denominator rational uniqueness and Hermite covolume identities;
- protected-cutoff inequalities;
- the repeated-disk defect and primitive-covolume jump; and
- the displayed smoothing and localization exponent balances.

These diagnostics do not certify the smooth-table compactness arguments, the physical first-hit experiment, the full proof chain, novelty or journal significance.

The author reports 113,969 finite checks and 25 validation-contract controls. More importantly, the exact-source GitHub Actions run

`37128373358`

is bound to the reviewed SHA and completed successfully. The exact checkout, entry-point checks, eleven-document qualification, source-bound evidence archive and artifact upload all succeeded. The artifact is

`11276051085`

with recorded SHA-256 digest

`48ea5bfedee38bcbfe85674b008bdfeb2dd0faf4a43fd5f030a75d877d47abf9`.

Accordingly, source delivery and hosted qualification are not reasons for the present negative recommendation.

## 9. Corrections and editorial changes required for any resubmission

### 9.1 Retitle and reorganize around the actual primary theorem

The current title, *Reference-free certification from intrinsic boundary laws*, no longer describes the dominant route. The new theorem is a fixed-aperture first-impact boundary-sampling and local-period-recognition result. The older intrinsic return-law programme should be moved to a clearly separate supplement or companion paper rather than kept as eight active chapters after the new theorem.

### 9.2 State the directness of the exact data

The introduction should say plainly that the support of the exact first-impact law reveals the complete relevant boundary patch. This is a strength of the experimental design, but it matters for novelty assessment. The theorem is not an indirect recovery from travel times, counts or a spectral invariant.

### 9.3 Keep the patch margin in every finite-data headline

The finite-confidence theorem is uniform only on `B_eta`. The value of `eta` controls the discrete period decision and may vanish at symmetry increase. Every abstract, theorem summary and complexity statement should keep that dependence adjacent to the launch bound.

### 9.4 Correct the v27 status language

The README calls v27 “already published.” The repository evidence establishes a deposited, source-authenticated author revision and successful qualification, not publication in a journal. Unless a genuine publication record exists, replace this with “previously deposited,” “authenticated,” or “completed author revision.”

### 9.5 Broaden the local-periodicity comparison

The comparison to Dolbilin is relevant. A revised literature audit should also discuss more recent work on periodicity and local complexity of Delone sets, including the distinction between forced periodicity from complexity/local-pattern hypotheses and the present reconstruction under an already assumed bounded periodic presentation.

### 9.6 Do not market the launch exponent as global optimality

The `nu^{-3/4}` exponent is a conditional sufficient upper bound inherited from a particular boundary-coverage and compensated-smoothing design. It excludes localization bit cost, arithmetic, apparatus motion and setup, and no matching lower bound is proved. The paper currently states these limitations; they should remain unavoidable in summaries.

## 10. Top-four significance assessment

The strongest positive case for the paper is now clear. A single fixed physical aperture replaces the earlier hierarchy of selected return laws. Exact whole-table recovery no longer needs analyticity, asymmetry, shape naming, a primitive cell, a return network or an area-normalized endpoint experiment. The finite central-patch criterion correctly recovers the intrinsic full translation group even for repeated symmetric motifs. This is a meaningful simplification and extension.

At the requested benchmark, however, the following limitations remain decisive.

1. **The exact sensor directly samples the unknown boundary.** The support of the first-impact law is the relevant boundary union in a common laboratory frame.
2. **Periodicity and a quantitative presentation bound are assumed.** The finite patch is known in advance to contain representatives of all orbits and protected generators.
3. **The new group theorem is a finite local-symmetry argument.** It is elegant and useful, but its conceptual reach is limited once the whole patch is visible.
4. **Uniform noisy recovery requires a nonperiod patch gap.** The repeated-disk example shows unavoidable instability of the discrete lattice and orbit count without it.
5. **The statistical rate comes from classical ingredients.** Boundary coupon coverage, convex hulls, compensated convolution, rational separation and Hermite normal form are combined carefully rather than replaced by a new general principle.
6. **The result does not address standard passive invariants.** It proves neither passive-trajectory, marked-length, travelling-time, collision-count nor spectral rigidity.
7. **The manuscript architecture remains accreted.** The fixed-aperture result and the older intrinsic-law programme are different papers in information model, assumptions and proof strategy.

For these reasons I do not regard the paper as reaching the exceptional conceptual threshold of *Annals*, *Acta*, *Inventiones* or *JAMS*. This conclusion does not diminish the correctness or specialist interest of the repeated-motif theorem.

## 11. Final verdict

**Response to the preceding concrete objections:** substantively successful. Version 28 removes individual shape separation and primitive-presentation input from the new fixed-aperture route, preserves the corrected inherited source, and closes the exact-source qualification loop.

**Mathematical audit:** no fatal counterexample found in the new v28 core; the exact, uniform-noisy and pointwise scopes are properly distinguished. Minor editorial corrections remain.

**Editorial assessment:** potentially strong for a specialist journal after substantial refocusing, but insufficiently indirect, universal or conceptually transformative for the requested four-journal benchmark.

**Recommendation: reject at the Annals / Acta / Inventiones / JAMS benchmark.**
