# Referee Report — General Theta Foundations I, Revision 51

**Manuscript:** *General Theta Foundations I: Compatible Lifts, Finite-Group Rigidity, and Stable Stochastic Width*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v51-compatible-lifts-2026-09-27`
- `revision/general-theta-foundations-i-v51-referee-ready-2026-09-27`

**Reviewed publication head:** `6363748923a5623801a53cfdb507a776aad414c3`  
**Artifact publication commit:** `79b9e564cefb5300b9aa4faf317938e3fbf1d3b1`  
**Validated native-source commit:** `d98d9f38752985a66c004d935834fa5b08500b40`  
**Source predecessor:** Revision 50 publication `2024b419eab2e6e6d34a21c9bec2a18b6afb6222`  
**Controlling prior report:** r32, `ca5efb0e6e50c1deb267f8b6f98551ff56197890`  
**Review branch:** `review/general-theta-foundations-i-v51-compatible-lifts-harsh-top4-r33-2026-09-27`  
**Date:** 27 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

**Mathematical disposition:** Revision 51 is a serious and substantial advance over Revision 50. It is the first revision in this sequence that supplies an all-width structural theorem rather than only a minimum-rank normal form, a finite-table certificate, or a special exact frontier. I did not find a fatal counterexample to the reachable-section theorem, the local projector characterization, the arbitrary-width occupation bound, the finite-group stationarization theorem, the one-surplus six-state frontier, or the quantitative rank-tight stability theorem.

The negative recommendation is therefore not a correctness dismissal. It is a judgment about scope, depth relative to the classical machinery used, and the level of generality required for the four leading general mathematics journals.

The strongest new statement is the following classification, under signed spanning seeds, all coordinate queries, an identity command, and a finite orthogonal command alphabet:

```text
exact clocked width is uniformly bounded over all horizons
        if and only if
the generated orthogonal command group is finite,
        if and only if
one stationary finite permutation realization works at every horizon.
```

This is a clean theorem. Its proof uses reachable probability sections, a finite vertex bound, compactness of physical polytopes, a volume-expansion variational constant, and stationarization at equality. The manuscript also gives a fixed-dimensional rational noncommuting infinite-group example with diverging exact width, an eventual exact six-state result in dimension three, and an explicit horizon-independent positive-error four-state interval in dimension two.

These conclusions are mathematically worthwhile and potentially publishable in a strong specialist journal. They are not yet a top-four result for the following reasons.

1. The all-width classification is exact and qualitative. For infinite groups it proves divergence but gives no usable rate unless one can estimate a generally non-explicit variational multiplier.
2. The explicit noisy theorem is restricted to rank-tight cuts. There is no approximate all-width finite-group classification and no noisy one-surplus six-state theorem.
3. The one-surplus constant is obtained by compactness and strict inequality; it is neither evaluated nor related to a sharp transition horizon.
4. The local arbitrary-profile criterion is a finite cubic semialgebraic encoding. It is useful, but it does not constitute an efficient optimizer or a new general duality for higher positive realization order.
5. The model remains a highly nonuniform atomic-real-row resource. It does not price row descriptions, real arithmetic, or exact sampling in the primary width invariant.
6. The fifty-seven-page article remains an accumulation of several largely independent programs: compatible lifts, two-state tensor duality, Gram and grid certificates, arithmetic width exponents, Liouville fluctuations, and a finite-bit compiler.
7. None of the new finite-dimensional theorems closes the independent analytic A/B/C/D proof pipeline recorded elsewhere in the repository.

**Disposition outside the four leading general journals:** major revision, strong compression, and a conventional independent priority audit before submission to a specialist journal in positive realization, finite automata, switched systems, convex geometry, or algebraic optimization. A focused paper centered on reachable sections, bounded-width rigidity, and quantitative occupation could be a substantial contribution.

---

## 1. Scope, genealogy, and materials reviewed

At the final branch survey used for this report, Revision 51 was the latest referee-ready `General Theta Foundations I` revision. The work branch and referee-ready branch both pointed to

```text
6363748923a5623801a53cfdb507a776aad414c3.
```

No pre-existing Revision 51 review branch was present.

I reviewed the complete active input graph and the records needed to assess correctness, provenance, reproducibility, literature positioning, and relation to the repository-wide pipeline. In particular, I examined:

- `papers/GTF-I-v51-compatible-lifts/main.tex`;
- `introduction.tex`;
- `inherited/machine-model.tex`;
- `inherited/hankel-compatibility.tex`;
- `reachable-lifts.tex`;
- `all-width-rigidity.tex`;
- `compatible-simplex.tex`;
- `stable-occupation.tex`;
- `orthogonal-circuit.tex`;
- `inherited/two-state-compatibility.tex`;
- `inherited/magnitude-duality.tex`;
- `inherited/exact-error-examples.tex`;
- `certificate-complexity.tex`;
- `inherited/encoding-and-comparison.tex`;
- `literature-and-resources.tex`;
- the mathematical appendices retained from the v44–v50 line;
- `RESPONSE_TO_REFEREE.md`;
- `README.md`;
- `PROOF_STATUS.json`;
- `PIPELINE_STATUS.json`;
- `RESOURCE_LEDGER.md`;
- `HISTORY_AUDIT.md`;
- `LITERATURE_AUDIT.md`;
- `PRESERVATION_MANIFEST.json`;
- `EXPECTED_V50.json`;
- `check_revision.py`;
- the inherited exact-check programs;
- the build receipt, active-input manifest, theorem-location map, isolated-core receipt, and workflow status;
- the complete r32 report;
- the Revision 50 source package and the Revision 33 compatible-lift predecessor identified by the author; and
- the repository-level Round-Seventeen proof-dependency ledger.

I also made targeted comparisons with the positive-realization and invariant-cone literature, classical stochastic-extension separation, static extension complexity, rank-one tensor completion, and local noisy tensor recovery. This was not an exhaustive independent priority search.

The repository genealogy is clean. The validated source commit, generated-artifact commit, and final documentation correction are distinct. The final head differs from the artifact publication only by a review-index correction and does not silently alter theorem source. Existing manuscripts and review branches are not overwritten.

A successful source-bound build is useful evidence of delivery and regression control. It is not independent mathematical proof or priority certification. Conversely, the editorial recommendation below is not based on a packaging failure.

---

## 2. Executive assessment of the new mathematics

Revision 51 adds four major structural advances and several secondary ones.

### 2.1 Reachable sections at arbitrary width

For an exact machine at cut `t`, let `E_t` contain all actual reachable state distributions after prefixes, let

```text
R_t = rowspan(E_t),
P_t = R_t intersect Delta_{K_t-1},
```

and let `Z_t` be the identity-suffix mean matrix. The physical image is

```text
S_t = (P_t Z_t)^T.
```

Theorem `section51` proves:

```text
C_rho subset S_t subset Q_t subset [-1,1]^D,
U_a S_t subset S_{t+1},
f_0(S_t) <= binom(K_t, dim(R_t)-1),
```

and gives the affine observation-kernel dimension

```text
dim(R_t)-D-1.
```

The command identities are asserted only on the reachable span, not on every ambient hidden basis vector. This is the correct way to move above minimum rank.

The theorem also survives separated cuts: every intervening word sends the earlier physical polytope into the later one even when all intermediate registers are arbitrarily large.

### 2.2 A finite local characterization of arbitrary profiles

Theorem `local51` replaces exponentially many suffix coordinates by bounded matrices and orthogonal projectors. Exact feasibility is equivalent to the existence of:

```text
orthogonal projectors Pi_t,
bounded mean matrices Z_t,
stochastic command matrices T_{t+1,a},
and seed distributions p_x,
```

satisfying range invariance and observable intertwining:

```text
Pi_t T_{t+1,a}(I-Pi_{t+1}) = 0,
Pi_t(T_{t+1,a} Z_{t+1} - Z_t U_a^T) = 0.
```

The system has degree at most three and polynomial description length in the explicitly listed horizon, widths, alphabet, and dimension. This is an exact semialgebraic characterization, not a polynomial-time algorithm.

### 2.3 All-width boundedness versus finite command groups

For physical polytopes with at most `V` vertices, the paper minimizes the volume-expansion ratio

```text
vol(conv union_a U_a S) / vol(S).
```

Compactness makes the minimum attainable. Equality to one occurs exactly when there is a common invariant finite-vertex polytope, in which case the command group acts faithfully by vertex permutations.

Combining this with the reachable-section vertex bound gives an occupation inequality for every fixed available width, with arbitrary wider cuts between the selected ones. It follows that exact clocked widths remain bounded over all horizons if and only if the generated orthogonal group is finite.

This is the principal theorem of the revision.

### 2.4 Quantitative stability at rank-tight cuts

The paper constructs an affine anchor from the prescribed signed seeds. At a rank-tight cut, a Neumann-series estimate recovers every statewise suffix-response row from the observable identity-suffix means, without dividing by a potentially tiny individual state probability and without accumulating one error per epoch.

For mean error `delta=2 epsilon`, it obtains approximate containment

```text
U_w S_s subset S_t + h[-1,1]^D subset Lambda S_t
```

and the robust occupation bound

```text
(c_D/Lambda^D)^(m-1) <= D!(rho-D delta)^(-D).
```

In the planar signed-permutation case this yields the explicit sufficient frontier

```text
rho=1/10,
N>=16,
epsilon<=1/200000
    => W_{N,epsilon}=4.
```

The interval is independent of the horizon.

### 2.5 Secondary new consequences

The one-surplus geometry at width `D+2` leads, in dimension three, to an eventual exact six-state frontier for signed-permutation alphabets containing `I` and `-I`.

A rational planar rotation of infinite order together with a reflection supplies a fixed-dimensional, fixed-alphabet, noncommuting family with exact width tending to infinity.

The manuscript also retains the v50 orthogonal cubic example, the v49 two-state global alternative, and the earlier arithmetic and finite-bit results.

---

## 3. Detailed correctness audit

### 3.1 The reachable row span and its probability section

I regard the basic construction as correct.

Every row of `E_t` has mass one. Because these rows linearly span `R_t`, their affine hull is exactly

```text
R_t intersect {p : p 1 = 1}.
```

Indeed, any zero-mass vector in `R_t` can be written as a linear combination of reachable rows with coefficients summing to zero, and hence as an affine-direction combination of their differences.

The convex hull of the actual reachable rows lies in `P_t` and has affine dimension `r_t-1`, where `r_t=dim R_t`. Thus `P_t` also has that dimension.

This small affine-hull fact is used repeatedly and should be stated as a named lemma or proved in one explicit sentence; at present the argument is correct but compressed.

### 3.2 Rank of the observation map and the hidden fiber

On `R_t`, consider

```text
y -> (y1, yZ_t).
```

The identity-prefix rows for the signed coordinate seeds map to

```text
(1, +rho e_i^T), (1, -rho e_i^T),
```

which span `R^{D+1}`. Therefore the map has rank `D+1`, giving

```text
r_t >= D+1
```

and affine observation fibers of dimension

```text
r_t-D-1.
```

This correctly distinguishes two phenomena:

1. unused directions outside the reachable span; and
2. unobservable directions inside the reachable span.

The paper does not conflate either of them with a physical state.

### 3.3 Legality of physical images for non-reachable section points

A point `p` in `P_t` need not be an actually reached distribution. Nevertheless it lies in the reachable linear span and in the simplex. Exactness on actual prefix rows extends linearly to `R_t`, so for every suffix `v`,

```text
p B_t(v) = p Z_t U_v^T.
```

The left side is a convex combination of legal hidden-state response rows. Hence the physical image is legal for every continuation and lies in `Q_t`.

This is an important point. It justifies use of the whole positive section rather than only the convex hull of observed prefixes.

### 3.4 The vertex bound

Inside its affine hull, `P_t` is cut out by the `K_t` coordinate nonnegativity inequalities. A vertex is determined by at least `r_t-1` linearly independent active coordinate restrictions. Choosing one such independent subset assigns the vertex to a subset of size `r_t-1`; that subset determines at most one point in the affine hull.

Thus

```text
f_0(P_t) <= binom(K_t,r_t-1).
```

Projection cannot increase the number of vertices, so the same bound applies to `S_t`.

This is correct. The proof would be easier to audit if it explicitly said that a canonical independent active subset is chosen for each vertex, or that the map to subsets is made injective by a fixed ordering convention.

### 3.5 Command compatibility on reachable sections

For every actual prefix row `p`, the updated row `pT_{t+1,a}` is reachable at the next cut. Hence

```text
R_t T_{t+1,a} subset R_{t+1}.
```

Stochasticity preserves the simplex, giving

```text
P_t T_{t+1,a} subset P_{t+1}.
```

Exactness with identity padding yields, on `R_t`,

```text
T_{t+1,a} Z_{t+1} = Z_t U_a^T
```

in the restricted sense required by the theorem. This gives the physical containment and, after composition, the separated-cut containment.

The quantifiers are correct: no restriction is imposed on intermediate widths.

### 3.6 The one-surplus dichotomy

At width `D+2`, only two reachability ranks are possible.

If `r_t=D+2`, the positive section is the whole simplex and the physical projection has a one-dimensional affine kernel. Its image has at most `D+2` vertices.

If `r_t=D+1`, the observation map is an affine isomorphism on a `D`-dimensional section of the `(D+1)`-simplex. The section has at most `D+2` coordinate facets. A `D`-polytope with at most `D+2` facets has at most `binom(D+2,2)` vertices by the same active-facet counting argument.

The dichotomy is sound. The vertex bound in the second case should be justified explicitly rather than left as an immediate consequence of the facet statement.

### 3.7 The projector characterization

Theorem `local51` is correct.

For necessity, take the orthogonal projector onto the actual reachable row span. Range invariance gives

```text
Pi_t T_{t+1,a}(I-Pi_{t+1})=0,
```

and exactness on that span gives the observable identity.

For sufficiency, if a running probability row satisfies `pPi_t=p`, range invariance gives

```text
(pT)Pi_{t+1}=pT,
```

while the intertwining identity gives

```text
pT Z_{t+1}=pZ_t U_a^T.
```

Induction therefore realizes every word. The bounded columns of `Z_N` are legal decoder means on every available state, including unreachable ones.

This is a genuine exact characterization of arbitrary prescribed profiles. It does not find a minimum profile efficiently.

Two presentational corrections are needed.

1. The displayed count is a variable count, not a complete equation count or bit-complexity estimate. The theorem should say so in its statement rather than only afterward.
2. In Proposition `dual51`, the matrix `B` must include both linear projector-range invariance equations and observable intertwining equations, in addition to row sums. The current phrase “row-sum and intertwining equations” is ambiguous because the manuscript uses a separate label for the invariance equation. If invariance is omitted, the alternative is false.

### 3.8 The supplied-section Farkas alternative

Once all projectors and mean matrices are fixed, every condition on one transition is linear in the transition entries, and the remaining inequality is entrywise nonnegativity. Equality-form Farkas separation therefore gives a finite infeasibility witness.

For rational supplied data, rational polyhedral separation gives rational witnesses.

This is classical and correctly scoped. It is not a global dual over unknown reachable sections.

The quarter-error example is a useful reminder that an affine map which is positive on a section need not extend to an ambient stochastic map.

### 3.9 Compactness of the physical polytope class

The class of full-dimensional polytopes

```text
C_rho subset S subset [-1,1]^D,
f_0(S)<=V
```

is compact in the Hausdorff metric. Padding the vertex list by repetitions and passing to a convergent subsequence gives the limit polytope. Containment of the fixed crosspolytope prevents loss of dimension.

Volume is continuous because every body has a uniform inner ball and a uniform outer bound. The volume-expansion ratio therefore attains its minimum.

Since the identity belongs to the alphabet, the convex hull of all command images contains `S`, and the ratio is at least one.

### 3.10 Equality and invariant finite polytopes

If the expansion ratio is one, the containing convex body and `S` have equal volume. A proper inclusion of full-dimensional compact convex bodies would add positive volume, so equality of bodies follows. Hence every command sends `S` into itself. Orthogonality gives equal volume, so the inclusion is equality.

Each command permutes the vertices. A group element acting trivially on all vertices fixes their affine hull pointwise and is the identity. The induced permutation action is faithful.

Therefore an infinite command group forces a strict expansion multiplier greater than one.

This argument is correct.

### 3.11 The all-width occupation inequality

At a selected cut of width at most `K`, the reachable-section theorem bounds the number of physical vertices by at most the central binomial coefficient

```text
V_K=binom(K,floor(K/2)).
```

Between consecutive selected cuts, a word with one prescribed command and identity padding realizes each generator `U_a`. Thus the later physical polytope contains

```text
conv union_a U_a S.
```

The variational multiplier increases volume at every selected interval. Comparing the first crosspolytope volume with the final cube volume gives

```text
gamma_A(V_K,rho)^(m-1) <= D! rho^(-D).
```

The argument correctly allows arbitrary wider registers between selected cuts.

The theorem is qualitative unless `gamma_A` can be estimated. That limitation is central to the editorial assessment.

### 3.12 Bounded width if and only if the command group is finite

Suppose every horizon has an exact machine of peak at most `K`. Every one of its `N+1` command cuts is selected, so

```text
gamma_A(V_K,rho)^N <= D!rho^(-D)
```

for all `N`. Hence the multiplier equals one, and an invariant finite-vertex physical polytope exists.

Its vertices yield one stationary permutation machine working at every horizon. Conversely, if the generated group is finite, storing a point in the finite orbit of the signed coordinate seeds gives an exact stationary realization.

The monotonicity of `W_{N,0}` is also correct: an `(N+1)`-horizon machine can absorb a final identity update into its decoder and answer at horizon `N` without increasing the previous peak.

Thus an infinite group gives

```text
W_{N,0} -> infinity.
```

This is the strongest theorem in the paper.

The stationary label bound can be exponentially larger than the original uniform clocked bound. The manuscript states this and does not assert equality between hidden-state width and physical vertex count.

### 3.13 The rational noncommuting planar family

For

```text
R = [[3/5,-4/5],[4/5,3/5]],
F = diag(1,-1),
```

one has `FRF=R^{-1}` and `FR != RF`. If the eigenvalue `(3+4i)/5` were a root of unity, its sum with its inverse would be the rational algebraic integer `6/5`, impossible because rational algebraic integers are integers.

Thus the rotation has infinite order and the generated group is infinite. The finite-group theorem gives divergence of exact width at fixed dimension and fixed alphabet.

The example is correct. It does not provide a quantitative divergence rate.

### 3.14 The one-surplus variational gap

For `D>=3`, a centrally symmetric full-dimensional polytope has at least `2D` vertices and at least `2D` facets. Since `D+2<2D`, no polytope with at most `D+2` vertices or at most `D+2` facets can be centrally symmetric.

The vertex-bounded subclass is compact. The facet-bounded subclass becomes vertex-bounded after polarity; the fixed crosspolytope/cube inner and outer bounds make polarity continuous. Hence the union is compact.

For every member, `conv(S union -S)` strictly contains `S` in volume. Compactness makes the minimum ratio strictly larger than one.

This yields an occupation inequality for cuts of width at most `D+2`.

The argument is sound. The manuscript should explicitly note that `0` lies in the interior of every admissible `S`, so polarity is well defined, and should state continuity of the numerator under Hausdorff convergence in the proof.

### 3.15 The eventual six-state frontier

In dimension three, the tetrahedron with the four parity vertices of the cube contains every signed coordinate vector as an edge midpoint. Thus the one-surplus polytope class is nonempty.

If peak width were at most five at every cut, all cuts would enter the one-surplus occupation inequality. Beyond the variational threshold, this is impossible.

Six labels suffice by storing the six signed coordinate vectors and permuting them under signed-permutation commands.

Therefore

```text
W_{N,0}=6
```

for all sufficiently large horizons in the stated class.

This exact result is valid. Its transition horizon is not effective until the variational constant is bounded away from one quantitatively.

### 3.16 The anchor matrix and inverse bound

At a rank-tight cut, the paper chooses `D+1` anchor distributions: the average of the `+e_1` and `-e_1` distributions, followed by the `+e_i` distributions.

Multiplying them by `[1,Z_t]` gives a square matrix within row-sum norm `D delta` of

```text
[[1,0],
 [1,rho I_D]].
```

The target inverse has infinity norm `2/rho`. The condition

```text
delta < rho/(2D)
```

allows a Neumann-series inverse bound.

When the cut width is `D+1`, both the anchor distribution matrix and `[1,Z_t]` are square and invertible. The identity

```text
F_t^{-1} = [1,Z_t] M_t^{-1}
```

and the row-sum bound on `[1,Z_t]` give the displayed estimate.

No lower bound on an individual hidden-state probability is used.

### 3.17 Statewise suffix recovery

For the same anchor prefixes, the actual means after an arbitrary suffix differ from the target by at most `delta` per coordinate. The identity-suffix means multiplied by the orthogonal target transformation contribute at most `sqrt(D) delta` per coordinate.

Multiplication by the anchor inverse therefore yields the uniform statewise bound

```text
h = 2(D+1)(1+sqrt(D)) delta / (rho-2D delta).
```

This controls the entire suffix at once and does not telescope over its length.

This is the key new robust idea, and it is correct.

### 3.18 The inner crosspolytope at positive error

The physical simplex contains the realized means of the signed seed anchors, each within coordinate error `delta` of `+/- rho e_i`.

For every direction `u`, its support function is therefore at least

```text
rho ||u||_infty - delta ||u||_1
    >= (rho-D delta)||u||_infty.
```

Hence it contains the crosspolytope of radius

```text
b=rho-D delta.
```

The outer cube bound follows from decoder legality. Since `b>0`, the `D+1` generating points are affinely independent and form a simplex.

### 3.19 Approximate containment and robust volume growth

The actual composed stochastic kernel between two rank-tight cuts maps later state means into convex combinations. The statewise suffix-recovery estimate therefore gives

```text
U_w S_s subset S_t + h[-1,1]^D.
```

Because `S_t` contains the crosspolytope `C_b`, one has

```text
h[-1,1]^D subset (D h/b) S_t,
```

and convexity gives

```text
S_t + (D h/b)S_t = (1+D h/b)S_t.
```

This is the displayed factor `Lambda`.

Applying the simplex difference-body estimate to `Lambda S_t` gives the robust occupation inequality. The endpoint volume estimates use `C_b` and the coordinate cube.

The proof is correct.

### 3.20 The explicit planar constants

With `D=2`, `delta=2 epsilon`, and

```text
epsilon <= rho^2/2000,
```

one obtains the rational lower bounds on `b`, the denominator margins in `Lambda`, and

```text
c_2/Lambda^2 >= 512/363.
```

If a peak-three machine existed, the anchor lemma would force all command cuts to have exactly three labels. The robust occupation bound with `m=N+1` contradicts the strict horizon inequality.

The exact signed-coordinate four-state machine supplies the upper bound.

The arithmetic for `rho=1/10`, `N>=16`, and `epsilon<=1/200000` is consistent.

---

## 4. What Revision 51 genuinely resolves from r32

The prior report identified four principal mathematical deficiencies. Revision 51 makes real progress on all four.

### 4.1 It moves beyond rank-tight geometry

The reachable-section theorem covers arbitrary width and explicitly tracks reachable rank and hidden observation fibers. The all-width occupation theorem and finite-group criterion are not confined to `D+1` labels.

### 4.2 It supplies quantitative positive-error stability

The rank-tight positive-error theorem now has explicit constants independent of the horizon. This is substantially stronger than the fixed-horizon compactness interval in Revision 50.

### 4.3 It treats one surplus label

The vertex/facet dichotomy and the polarity compactness argument give an eventual exact six-state result in dimension three.

### 4.4 It gives a fixed-dimensional long-horizon noncommuting family

The rational rotation/reflection example keeps dimension and alphabet fixed while the horizon grows and exact width diverges.

These are not cosmetic responses. They materially strengthen the paper.

---

## 5. Why the paper still falls short of the four-journal level

### 5.1 The all-width theorem is exact but not quantitatively effective

For an infinite group, the paper proves

```text
gamma_A(V,rho)>1.
```

This is enough for qualitative occupation and divergence. It does not provide a lower bound on `gamma_A-1` in terms of spectral, arithmetic, group-theoretic, or geometric data.

Consequently the central theorem does not quantify how width grows for a general infinite command group. The retained arithmetic sections do so only for special planar rotations and special Diophantine classes.

A top-level theorem would relate the variational expansion constant to intrinsic data of the generated action, or derive a broad rate classification.

### 5.2 No approximate all-width finite-group theorem is proved

The robust theorem controls rank-tight cuts. The all-width theorem controls exact machines.

The paper does not characterize whether widths remain bounded for a fixed positive tolerance when the command group is infinite. It does not establish a noisy analogue of

```text
bounded width iff finite group.
```

For positive error, approximate invariant polytopes may exist even when no exact invariant finite polytope exists. This is a different and potentially deep problem. Revision 51 does not solve it.

### 5.3 The six-state theorem remains qualitative

The constant `beta_3(rho)` is known only to exceed one by compactness. There is no explicit lower bound, no computable first horizon, and no positive-error extension.

Thus the “eventual exact six-state frontier” is an existence theorem rather than a calibrated frontier comparable to the explicit planar result.

### 5.4 The local polynomial system is an encoding, not a structural optimizer

The projector formula is useful and avoids enumerating command words. Nevertheless it is a generic compact semialgebraic feasibility system. Quantifier elimination can decide it, but no meaningful complexity bound, convexity theorem, dual hierarchy, or efficient structural algorithm is obtained.

The supplied-section Farkas alternative becomes linear only after the hard geometric variables are fixed.

### 5.5 The assumptions remain specialized

The all-width theorem uses:

- orthogonal command maps;
- the signed coordinate seed set;
- all coordinate queries;
- identity padding;
- exact terminal numerical probabilities; and
- a nonuniform horizon-dependent atomic-row model.

These assumptions are natural for the paper's experiment but should not be presented as a general positive-realization classification.

It remains unclear which conclusions survive:

- nonorthogonal contractions;
- partial query families;
- nonspanning seeds;
- continuous command sets;
- approximate response semantics; or
- uniform row descriptions.

### 5.6 Much of the mechanism is classical

The paper correctly credits:

- invariant polyhedral cones in positive realization;
- nonnegative intertwining requirements;
- stochastic-extension separation;
- static extension complexity;
- Farkas alternatives;
- compactness of bounded polytopes;
- difference-body volume;
- Segre circuits; and
- real-algebraic elimination.

The principal addition is their controlled, cut-dependent assembly and the nonuniform-to-stationary conclusion. This is valuable. It is not obviously transformative enough for a top-four general journal without a broader quantitative or conceptual consequence.

### 5.7 The article remains structurally overgrown

The current paper has fifty-seven pages and retains, largely in appendices:

- compatible lifts and finite-group rigidity;
- stable occupation;
- rank-tight simplex geometry;
- two-state sign/magnitude duality;
- exact tensor examples;
- Gram and moment certificates;
- rational-grid approximation;
- word distortion and enclosure profiles;
- Diophantine width laws;
- Liouville fluctuations; and
- a finite-bit compiler.

These are related through the broad topic of stochastic width, but they do not form one tightly organized theorem chain. The new all-width result deserves a focused paper rather than being one layer in a revision archive.

### 5.8 The primary resource remains permissive

The atomic-row width invariant allows:

- a new machine for every horizon;
- free knowledge of the epoch and horizon;
- free horizon-dependent real tables;
- free construction and lookup of those tables;
- exact real arithmetic; and
- exact sampling of arbitrary prescribed real stochastic rows.

The finite-bit compiler addresses a distinct special model. It does not price the general exact rows used by the structural theorems.

This limitation is clearly disclosed but materially narrows the interpretation of “memory” or “state complexity.”

---

## 6. Literature and priority assessment

The literature discussion is much improved. The article now confronts several close antecedents directly rather than relegating them to a repository audit.

In particular, it recognizes that:

- positive rank alone does not determine positive realization order;
- nonnegative intertwining is classical;
- invariant polyhedral cones are classical;
- static extension complexity does not supply stochastic dynamics;
- toric tensor circuits and real sign conditions are classical; and
- local noisy tensor recovery has a separate modern literature.

However, an independent priority review is still required for the exact theorem

```text
uniformly bounded horizon-dependent positive width
iff finite generated orthogonal group.
```

The author should compare this theorem not only with positive realization but also with:

- finite-dimensional linear representations of probabilistic automata;
- invariant-polytope criteria for switched systems;
- finite semigroup and group automata;
- common polyhedral Lyapunov/invariant sets; and
- stationarization of nonuniform finite-state transducers.

The repository's targeted audit is responsible and useful. It is not exhaustive enough to support a claim of top-four originality.

The paper should add a conventional theorem-by-theorem comparison table containing:

```text
current theorem | closest published theorem | shared mechanism |
new hypotheses | genuinely new conclusion
```

for `section51`, `finitegroup51`, `surplus-budget51`, and `robust51`.

---

## 7. Relation to the wider repository pipeline

The repository-level analytic dependency chains remain:

```text
A2 -> A3 -> A4 -> C2 -> D1
```

and

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1 -> C2 -> D1,
```

with A1 independent.

Those gates require model-specific results including:

- raw returned Fourier and density estimates;
- stopped entropy-controlled large deviations;
- one global past kernel and renewal resolvent;
- source-dependent canonical conditioning;
- process Gaussian and Mosco limits;
- nonlinear resolvents and graph cores;
- regular filtering and QMD;
- operator-domain response identities; and
- labelled posterior contraction.

Revision 51 proves none of those analytic statements. Its local dependency graph is instead:

```text
reachable probability spans
    -> positive physical sections
    -> variational volume expansion
    -> exact bounded-width/finite-group rigidity,
```

and

```text
rank-tight anchors
    -> statewise suffix recovery
    -> approximate simplex containment
    -> robust occupation.
```

These are valid and self-contained finite-dimensional results. They are mathematically orthogonal to most of the A/B/C/D pipeline.

The manuscript's `PIPELINE_STATUS.json` correctly says that analytic closure is not inferred. No A2, B4, C2, D1, or eleven-paper aggregate credit should be assigned from the present work.

The series title continues to invite a foundational pipeline interpretation. Either the article should state a concrete downstream theorem that uses the new finite-group rigidity, or it should be presented as a self-contained realization-theory paper whose merits do not depend on the surrounding archive.

---

## 8. Reproducibility and publication status

The v51 release is reproducible at a level materially better than the earlier v46 release.

The source-bound workflow `36293584115` completed successfully. It:

1. assembled readable native source from the frozen predecessor;
2. installed fixed dependencies;
3. executed the v51 and inherited finite checks;
4. built the article;
5. rebuilt the isolated core package;
6. compared all page text and rasters; and
7. atomically published the work and referee-ready refs after source-freshness checks.

The build receipt records:

- a 57-page article;
- no undefined references;
- no overfull boxes;
- ordinary/optimized Python agreement;
- preservation of the active inherited labels;
- 68 named negative-control executions;
- successful isolated-core text and raster equality; and
- source binding to `d98d9f38752985a66c004d935834fa5b08500b40`.

The new finite checker verifies:

- both one-surplus reachability ranks;
- a globally unreachable state for which ambient intertwining fails;
- six-state signed-permutation witnesses;
- the rational noncommuting group identities;
- anchor inversion constants;
- the explicit robust horizon/error certificate; and
- the quarter stochastic-extension defect.

These checks are useful and honestly scoped. They do not prove the universal compactness, occupation, or stationarization theorems.

The final head `6363748923...` only corrects the revision number in the root review index and does not alter validated mathematical source or generated artifacts.

---

## 9. Required revision before specialist submission

### 9.1 Split or radically focus the article

The main submission should center on:

1. reachable sections at arbitrary width;
2. the local projector characterization;
3. all-width occupation and finite-group rigidity;
4. one-surplus occupation; and
5. quantitative rank-tight stability.

The two-state tensor theory can be a companion article or a concise prerequisite section. The arithmetic and finite-bit material should be a separate paper or cited predecessor rather than reproduced in full.

### 9.2 State the finite-group theorem as the central result

The abstract currently lists many results at equal weight. The bounded-width/finite-group equivalence is the conceptual center and should lead the title, abstract, introduction, and conclusion.

The theorem should be stated once in a prominent form with all hypotheses:

- signed spanning coordinate seeds;
- all coordinate queries;
- finite orthogonal alphabet;
- identity command;
- exact numerical realization; and
- nonuniform clocked atomic-row width.

### 9.3 Quantify the variational multiplier in meaningful classes

The paper should derive explicit lower bounds for `gamma_A(V,rho)-1` from intrinsic data in at least one broad class beyond the antipodal simplex case.

Possible targets include:

- finite-dimensional rotations with a Diophantine parameter;
- groups with a quantitative displacement from every `V`-vertex polytope;
- finite-order approximations with controlled denominator; or
- a compactness modulus for rational input of bounded height.

Without such a result, the general infinite-group theorem gives divergence but little quantitative information.

### 9.4 Develop an approximate all-width theorem

The main open structural question created by the paper is whether fixed positive-error width can remain bounded for an infinite command group.

At minimum, the author should formulate the correct approximate invariant-polytope object and prove one nontrivial theorem beyond rank-tight cuts. Even a result under a uniform reachability-rank or conditioning hypothesis would materially deepen the paper.

### 9.5 Make the one-surplus theorem effective

For `D=3`, estimate `beta_3(rho)` explicitly, even crudely, or give a finite semialgebraic program whose certified output determines a numerical horizon.

A purely variational strict inequality is mathematically valid but weakens the meaning of “exact six-state frontier.”

### 9.6 Clarify Proposition `dual51`

State explicitly that `B vec(T)=b` contains:

- row-sum equations;
- projector-range invariance equations; and
- observable intertwining equations.

Provide the dimensions of `B`, `b`, and the dual witness, and distinguish verification complexity from search over unknown projectors.

### 9.7 Separate description complexity from arithmetic complexity

For the cubic projector system, specify:

- number of equations and inequalities;
- rational/algebraic coefficient encoding;
- whether `D`, alphabet size, and horizon are variable;
- output representation of projectors and rows; and
- the complexity statement actually claimed.

The current variable bound is not a quantifier-elimination complexity bound.

### 9.8 Complete a conventional priority audit

The author should search and compare directly with the literature on invariant polytopes of orthogonal and switched systems, finite semigroup realizations, probabilistic automata, and nonuniform-to-stationary conversion.

Internal revision genealogy should remain provenance, not substitute for conventional citation.

### 9.9 Add a concise resource theorem or table in the main text

The current resource table is useful. It should be moved earlier and made more formal, distinguishing:

```text
atomic label width,
row-description size,
random-bit cost,
uniform workspace,
time,
and fixed-horizon versus anytime correctness.
```

### 9.10 Keep the wider analytic pipeline explicitly separate

Do not describe the present finite-group theorem as closure of the General Theta analytic program unless an actual downstream dependence is proved. The current fail-closed status is correct and should be retained.

---

## 10. Local and technical comments

1. In Theorem `section51`, state explicitly that the affine hull of the reachable rows is `R_t intersect {p1=1}` and give the one-line coefficient-sum proof.
2. Define `r_t` before the first display containing `binom(K_t,r_t-1)` in every summary of the theorem.
3. Explain that permanently zero coordinates give redundant inequalities but do not invalidate the independent-active-set vertex count.
4. Fix a deterministic rule for choosing an independent active subset if the proof literally claims an injection from vertices to subsets.
5. In the projected vertex bound, say that the image polytope is the convex hull of images of vertices of `P_t`.
6. In Corollary `surplus51`, justify the bound `binom(D+2,2)` from the number of facets in one sentence.
7. Avoid calling the reachability rank a positive rank or stochastic rank; it is an ordinary dimension of the actual reachable linear span.
8. In Theorem `local51`, state that the projection rank is unconstrained because unreachable protected directions may be included; minimality is not claimed.
9. Give an equation/inequality count in addition to the variable count.
10. State the algebraic-number input representation adjacent to the RCF decision assertion.
11. In Proposition `dual51`, include both invariant-range and observable equations in `B` explicitly.
12. Record whether the dual witness is normalized or only homogeneous.
13. In the definition of `gamma_A(V,rho)`, state once that `I in A` is inherited from the section hypotheses.
14. Write `gamma_A(V,rho)` with all parameters in subsequent theorem summaries; the constant is not universal.
15. In the compactness lemma, explicitly cite continuity of `S -> conv union_a U_aS` in Hausdorff distance.
16. In the equality case, say that equal-volume inclusion implies equality because both bodies are full dimensional.
17. In the finite-group theorem, keep the distinction between the original bound `K` and the stationary bound `V_K` prominent.
18. The group-size estimate `V_K!` is extremely coarse; label it as such.
19. In the monotonicity proof for `W_{N,0}`, write the new decoder as `T_{N+1,I}d` explicitly.
20. In the rational-rotation example, state that trace `6/5` is the sum of the two eigenvalues and hence an algebraic integer under the root-of-unity assumption.
21. In the polarity compactness proof, state that `0` lies in the interior of every admissible body because it contains `C_rho`.
22. State continuity of `S -> conv(S union -S)` and of its volume before invoking the attained strict minimum.
23. In the six-state theorem, call the horizon condition sufficient and variational, not an effective numerical frontier.
24. In the anchor lemma, spell out why the averaged first anchor row has coordinate error at most `delta`, not `2 delta`.
25. Define the induced infinity norm before the inverse estimates.
26. In the statewise recovery estimate, distinguish entrywise maximum from matrix infinity norm.
27. In the approximate-containment proof, identify the full suffix as the selected word followed by identity padding.
28. State `delta=2 epsilon` at every corollary where mean and TV errors coexist.
29. The phrase “horizon-independent interval” refers to the upper error bound, not to the sufficient horizon; avoid possible ambiguity.
30. The exact four-state upper machine works for every horizon and error; say this once rather than repeating it in multiple sections.
31. Move the five-resource table before the first use of “width” as an interpretation of memory.
32. The term “local cubic realization criterion” may be misread as local analytic geometry; “degree-three finite projector criterion” would be clearer.
33. Distinguish ordinary polynomial description size from polynomial bit complexity when algebraic matrices are input.
34. The appendices reproduce a large historical development; a journal submission should cite predecessors rather than ask a referee to re-audit them.
35. Add a brief conclusion listing exactly what remains open: quantitative `gamma`, noisy all-width rigidity, effective `beta_3`, higher surplus, and general partial-query models.

---

## 11. Final assessment

Revision 51 has crossed an important threshold. It is no longer merely a collection of finite certificates and special arithmetic examples. It now contains a coherent structural theorem:

```text
bounded exact clocked stochastic width across all horizons
is equivalent to finite command-group action,
```

under a precise orthogonal numerical interface.

The reachable-section formalism is the correct arbitrary-width object. The stationarization argument is clean. The explicit rank-tight stability theorem is technically useful and avoids the usual uncontrolled state-probability division. The one-surplus six-state theorem is a legitimate higher-width consequence.

I therefore view the work as potentially publishable after major revision in a strong specialist venue, subject to an independent priority check.

I do not recommend publication in Annals, Inventiones, JAMS, or Acta in the present form. The central result remains specialized, largely exact and qualitative, and assembled from classical convex and positive-realization mechanisms. The broader quantitative and approximate theory that would elevate it to a top general-journal contribution is still missing. The article is also much too cumulative for its strongest theorem to be evaluated cleanly.

**Recommendation: reject at the four leading general journals; major revision and refocusing for a specialist journal.**
