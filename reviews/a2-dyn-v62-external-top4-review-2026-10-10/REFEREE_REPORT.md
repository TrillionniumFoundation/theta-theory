# External top-four referee report on A2-DYN revision 62

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v62-referee-response-2026-10-10`, `revision/a2-dyn-v62-referee-copy-2026-10-10`  
**Reviewed commit:** `45425f65832e3f1e69336c791de5fc32f8ed22bb`  
**Reviewed repository tree:** `af3b5e27a2aec1f022bc1f2a7d82dd373acb8703`  
**Ordinary source payload tree:** `03ead652e9a13dade8237838243feecdbd1db581`  
**Active manuscript directory:** `papers/A2-DYN-v62-referee-response`  
**Active mathematical source:** one hundred thirty-four numbered core modules; revision 62 adds modules 133--134 and retains the unreviewed revision-61 additions 131--132  
**Immediate author baseline:** revision 61, commit `3fb563abbef5a119164cc92a360e6e8434e0d92b`  
**Frozen revision-61 complete paper tree:** `a377d9bd972092af8e7fcd263de7d72f5509629b`  
**Controlling external report:** `reviews/a2-dyn-v60-external-top4-review-2026-10-09/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `47263fb3033b4545ed3b1e96646f56c9812e7de4` / `5e2f3538ce3d09d3ee1075464f05c2e6354e0709`  
**Date:** 10 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 62 contains genuine new mathematics on the original Lorentz source. It also incorporates the substantive revision-61 author additions, which had not received a separate external report. I therefore reviewed the four-module physical chain

- `core/131_inverse_incidence_coarea.tex`;
- `core/132_transverse_clearance_coarea.tex`;
- `core/133_finite_type_clearance_coarea.tex`;
- `core/134_clearance_caustic_localization.tex`.

The chain is materially stronger than the state reviewed in revision 60.

Revision 61 proves an exact determinant cancellation for the full inverse-incidence product along a regular physical orbit. It converts this into a finite-count roof-density estimate of size `C A^m`, a first-incidence height gain of size `C A^m epsilon`, and a two-coordinate area estimate of size `C A^m epsilon/eta` for the transverse portion of the actual next-collision clearance source. The rank-deficient clearance source is retained positively.

Revision 62 goes beyond a first-order determinant cutoff. It differentiates the actual clearance coordinate along an actual roof fiber, proves a fixed-order sublevel estimate, controls the number of physical fiber graph pieces by `C_r A_r^m`, and obtains

```text
C_r M A_r^m a^(-1) (epsilon/b)^(1/r)
```

for the part of the original first-clearance source having roof pivot at least `a` and `r`th fiber derivative at least `b`. The order-two statement includes fold points at which the first clearance derivative, and hence the two-coordinate Jacobian, vanishes.

The final module defines a physical seam/rank caustic in parameter--roof space. At each fixed radius and collision count, after imposing a positive incidence cap, the caustic has finitely many roof values, with an exponential component bound. A compact semialgebraic separation inequality supplies a determinant lower bound away from its neighborhood. This yields an exact positive localization of the original clearance source, retaining later low-incidence history and the complete source over the caustic neighborhood. A separate tube estimate proves small mass of that retained source for fixed collision count.

I found no decisive counterexample, missing section normalization, incorrect image mark, wrong coarea denominator, invalid target-count factor, or false replacement of the original source in this new chain. The elementary exponent calculations, source partitions, and order-two fold interpretation are internally coherent. The manuscript is also commendably explicit about what remains open.

The negative recommendation is nevertheless unavoidable.

The new bounds are finite-count bounds with constants of the forms

```text
C A^m,
C_r A_r^m,
C_{m,chi},
N_{m,chi},
D_{m,chi},
beta_{m,chi}.
```

No useful growth control is proved for the latter four quantities, and the first two are explicitly exponential in the collision count. The unrestricted raw theorem requires the ordered regime in which the reconstruction band is fixed, the collision count tends to infinity, and only then the band is enlarged. At a fixed band the protection width is fixed. Factors such as `m^2 A^m epsilon(B)` therefore do not tend to zero. Choosing the band exponentially in the collision count would reverse the proved order of limits and is not licensed by the spectral estimates.

More importantly, the exact caustic source remains a positive source. Its roof support has small measure for fixed `m`, but no essential-height estimate is proved on that support. A positive density may have arbitrarily small mass and arbitrarily large height. The manuscript correctly refuses to identify the tube-mass estimate with height control.

Consequently revision 62 still does not prove

- the ordered central-scale incidence height;
- the ordered central-scale complete clearance height;
- the unrestricted two-sided pointwise arithmetic raw-density theorem;
- unrestricted same-roof collision/return bridges;
- forward essential-likelihood convergence;
- or the unrestricted pointwise roof-conditioned path theorem.

These are not peripheral editorial details. They are the endpoint around which the title, the positive-error representation, and a substantial part of the one-hundred-thirty-four-module architecture are organized.

At the requested benchmark, the paper would need either

1. a completion of the two ordered Lorentz height estimates and hence of the title-level pointwise theorem; or
2. a general theorem of independent breadth, with quantitatively usable hypotheses and several genuinely different singular-hyperbolic realizations, so that the article no longer depends editorially on the unresolved Lorentz endpoint.

Revision 62 provides neither yet. Its new finite-type and semialgebraic reductions are mathematically useful, but they isolate rather than eliminate the remaining obstruction. No independent human specialist audit has been obtained.

My assessment is therefore positive about the local geometric progress and negative about readiness for *Annals*, *Acta*, *Inventiones*, or *JAMS*.

## 2. Frozen source, chronology, and preservation

Both reviewed author branches resolve to

`45425f65832e3f1e69336c791de5fc32f8ed22bb`.

The repository tree at that commit is

`af3b5e27a2aec1f022bc1f2a7d82dd373acb8703`.

The active article is

`papers/A2-DYN-v62-referee-response`.

The ordinary source payload tree recorded in the manifest is

`03ead652e9a13dade8237838243feecdbd1db581`.

The immediate mathematical baseline is revision 61 at

`3fb563abbef5a119164cc92a360e6e8434e0d92b`.

That revision added modules 131--132 in response to the revision-60 report. Revision 62 begins from the complete revision-61 source, with a small checkpoint commit recording the frozen route, and adds modules 133--134. Since revision 61 did not have its own external assessment, the present report treats modules 131--134 as the substantive new packet relative to the last external report.

The source manifest records

- all 132 inherited core modules byte-identical;
- all 179 inherited Python files byte-identical;
- every inherited compiled appendix retained;
- all 1761 inherited mathematical labels retained;
- an append-only bibliography change;
- two new modules, 133 and 134;
- the revision-61 physical modules retained unchanged;
- `lorentz_finite_type_clearance_height_proved: true`;
- `lorentz_fold_clearance_height_proved: true`;
- `lorentz_clearance_caustic_finiteness_proved: true`;
- `lorentz_caustic_positive_localization_proved: true`;
- `lorentz_caustic_tube_mass_proved: true`;
- `clearance_boundary_pointwise_smallness_proved: false`;
- `grazing_boundary_pointwise_smallness_proved: false`;
- `full_raw_return_LLT_proved: false`;
- `pointwise_roof_density_LLT_proved: false`;
- `unrestricted_same_roof_pair_bridge_proved: false`;
- `forward_essential_likelihood_convergence_proved: false`;
- `arithmetic_factor_identically_one_proved: false`;
- and `independent_human_review: false`.

These status flags accurately distinguish the finite-count physical reductions from the ordered pointwise endpoint.

The present review branch starts directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v62-external-top4-review-2026-10-10/`.

No author source, prior report, workflow, historical manuscript, or unrelated repository path is intentionally modified.

## 3. Exact-source qualification and its boundary

The exact-SHA qualification workflows completed successfully on both reviewed branches:

- response branch run `38019081482`;
- referee-copy branch run `38019089534`.

Both runs identify

`45425f65832e3f1e69336c791de5fc32f8ed22bb`

as the checked-out SHA.

According to the validation record, the verifier checks

- the complete frozen revision-61 paper tree;
- the controlling revision-60 report blob;
- all 132 inherited core files;
- all 179 inherited Python files;
- all 134 core inclusions;
- all inherited appendices and labels;
- fourteen provenance snapshots;
- the append-only bibliography;
- the ordinary source Merkle identity;
- the read-only workflow hash;
- agreement of normal and optimized finite diagnostics;
- native TeX compilation;
- and theorem-label-based page rendering.

The new finite regressions cover fixed-order jet recurrences, the first-derivative/Jacobian identity, monomial finite-type exponents, shifted fold models, rational chart densities, geometric depth sums, later-incidence envelopes, separation orientation, rank thresholds, positive source partitions, and the weak-`L^p` mass exponent. Negative fixtures are required to fail.

These checks are useful for source identity, algebraic normalization, and reproducibility. They do not certify

- the physical collision graph and its closures;
- endpoint injectivity;
- the inherited total-curvature and sign-component estimates;
- implicit collision jets on all physical strata;
- the actual first-defect decomposition;
- the anisotropic operator and arithmetic chain;
- the ordered Lorentz height limits;
- or any independent specialist review.

The manuscript and validation documents state this boundary correctly.

## 4. Scope of the substantive audit

I did not attempt to re-prove all 134 core modules. The present audit concentrates on the chain that can change the revision-60 assessment:

1. the exact endpoint determinant identity;
2. simultaneous inverse-incidence cancellation;
3. endpoint level-set integrals;
4. the finite-count inverse-incidence roof density;
5. the first-incidence height gain;
6. the marked two-coordinate clearance map;
7. finite-word multiplicity of that map;
8. transverse clearance coarea;
9. the one-dimensional derivative sublevel lemma;
10. fixed-order implicit collision jets;
11. graph-interval complexity on an actual roof fiber;
12. finite-type and fold clearance height;
13. the physical-side capped closure;
14. finite caustic fibers;
15. the semialgebraic separation inequality;
16. positive source localization, including later low incidence;
17. the caustic tube estimate;
18. conversion of tube length to source mass;
19. the order of limits in the raw inversion criterion;
20. the unchanged arithmetic and pointwise boundaries.

The inherited spectral, arithmetic, raw-error, path, and bridge results are treated as source-pinned inputs, not as independently re-certified mathematics.

## 5. The endpoint determinant and simultaneous incidence gain

Module 131 uses oriented endpoint arclengths and the reduced action of a fixed regular word. The internal contact matrix is tridiagonal, with diagonal

```text
t_{j-1}+t_j+2/(R c_j)
```

and neighboring entries `-t_j`.

The stated identity

```text
|F_uv| = c_0 c_m prod_j t_j / det A
```

is compatible with the corner cofactor of the full contact Hessian after the internal incidence factors are extracted. Multiplying by

```text
I_m = prod_{j=0}^m c_j^(-1)
```

leaves internal inverse incidences to be paid by the determinant.

Writing `A=L+D`, with `L` the weighted Dirichlet path Laplacian and `D_jj=2/(R c_j)`, gives

```text
det A >= prod_{j=1}^{m-1} 2/(R c_j).
```

This yields the printed estimate

```text
I_m |F_uv| <= (R/2)^(m-1) prod_j t_j.
```

I found no missing endpoint incidence factor in this calculation. The one-flight case also agrees with the direct mixed derivative.

The refined selected-contact ratio is derived by changing one diagonal potential at a time. The relevant Schur complement is bounded above by the corresponding diagonal, and restoring the physical `c_j` increases that diagonal. The resulting ratio

```text
(1+R/ell_0)c_j / (1+(R/ell_0)c_j)
```

is bounded by

```text
53 c_j/(6+47 c_j)
```

on the stated radius interval. The orientation of the determinant ratio is correct.

This is a meaningful physical identity. It is stronger than a separate one-contact cutoff because it cancels the complete inverse-incidence product simultaneously.

The load-bearing specialist checks are the exact Hessian convention, the endpoint Schur complement, and the inherited global endpoint parametrization for each regular word. I did not find a contradiction in the displayed algebra.

## 6. Endpoint level integrals

The endpoint level-set lemma splits into two regions.

Where one endpoint momentum is bounded away from zero, the gradient of the reduced action has a uniform lower bound. The inherited semialgebraic component estimate supplies an exponential bound on total level length across all pieces.

Where both endpoint momenta are small, the rational-coordinate Hessian is uniformly positive. On a regular level, the curvature identity gives

```text
1/|grad f| <= |k_f|/lambda_0.
```

The inherited total absolute curvature bound then controls the coarea integral.

This is a plausible and structurally appropriate way to handle levels approaching a nondegenerate critical value. It does not require convexity of the entire physical endpoint image.

The conclusion is nevertheless dependent on two substantial inherited inputs:

- coefficient-independent control of all endpoint level components;
- and the total absolute curvature estimate on the rational chart refinements.

A specialist should verify that compact regular exhaustion includes every physical component ending on a seam and that no endpoint multiplicity is counted incorrectly. Subject to those inputs, I find the finite-count bound coherent.

## 7. The complete inverse-incidence roof density

After the determinant cancellation, the weighted endpoint density on one chart is bounded by an exponential function of `m`. Finite horizon gives a fixed alphabet of next centers, hence exponentially many words. Coarea and the level-set integral therefore give

```text
||rho_m^I||_infinity <= C A^m.
```

The proof also covers fractional inverse-incidence products because every `c_j` lies in `(0,1]`, so such products are pointwise dominated by `I_m`.

For fixed collision count, the actual-return events indexed by `(n,k)` are disjoint. Restricting the positive weighted source before pushforward therefore proves the sum of exact-label variation densities without multiplying by the number of labels.

This disjointness point is important and appears to be used correctly.

The result proves finite-count integrability and an essential roof-height bound for an unbounded physical observable. It does not prove any count-uniform estimate.

## 8. The first-incidence height gain

The first-incidence guard has depth-dependent width

```text
2 epsilon q_0^(d_j/4).
```

The pointwise comparison

```text
1_{c_j < s_j} <= s_j/c_j <= s_j I_m
```

combined with the convergent geometric depth sum gives

```text
ess sup_t sum_{n,k} |b_inc(t)| <= C M A^m epsilon.
```

The more general simultaneous-contact estimate gains the product of the prescribed widths. This is a legitimate positive upper comparison on the unchanged orbit and does not average or replace the exact labels.

This is the first direct finite-count density gain for the original Lorentz incidence source in the present pipeline. Its limitation is equally clear: at a fixed reconstruction band, `epsilon(B)` is fixed while `m` tends to infinity, so `m^2 A^m epsilon(B)` is not small.

## 9. The marked clearance map

Module 132 marks the clearance at the image collision `j+1`, including for the last flight. This agrees with the inherited next-collision convention.

The map

```text
x -> (L_m(x), Z_d(T^(j+1)x))
```

uses the complete original roof and the actual selected competing disk. The source is partitioned, rather than replaced, according to whether the determinant of this map is at least `eta`.

The finite-word multiplicity lemma uses the auxiliary physical collision graph and adds the two target equations. At a nonzero determinant, a preimage is isolated in the fiber and therefore forms an isolated connected component. A coefficient-independent semialgebraic component bound then gives `C D^m`, after summing words and charts.

This is the right type of multiplicity estimate for the area formula. Its validity depends on the inherited polynomial encoding of actual first-hit inequalities and on the claim that the auxiliary variables are uniquely determined by the physical state and word. These are appropriate specialist audit points; I found no immediate target-dimension or component-count inconsistency.

## 10. Transverse clearance coarea

On the determinant region, the two-dimensional area formula gives a density at `(t,z)` bounded by multiplicity divided by `eta`. Integrating `z` over the two clearance bands and summing the geometrically decaying widths gives

```text
C M A^m epsilon/eta.
```

The exact-label restrictions and first-defect indicator are deleted only for a positive upper comparison. The disjoint exact-label partition is then restored before pushforward, so there is no factor equal to the number of targets.

I find the normalization and width summation consistent. The proof also keeps the selected responsible disk and does not continue a trajectory through a competing-hit seam.

The rank-deficient part remains a positive source. This is essential: a roof-critical word satisfies `dL_m=0`, so every two-coordinate determinant vanishes there. Module 132 does not misclassify that source as controlled.

## 11. The derivative sublevel lemma

The one-dimensional lemma states that if

```text
|f^(r)| >= b
```

on an interval, then the inverse image of an interval of length `s` has measure at most

```text
C_r (s/b)^(1/r).
```

Because `f^(r)` is continuous and nonzero, its sign is constant. The divided-difference proof is standard. A set of positive measure contains `r+1` sufficiently separated points; Lagrange's formula bounds the divided difference by `s` divided by the product of separations; repeated Rolle gives the value of `f^(r)/r!` at an intermediate point.

The exponent and dependence on `b` are correct. No monotonicity of the lower derivatives is required.

## 12. Tangential differentiation on the actual roof fiber

At the marked image collision, the full roof is written as a function `F` of the marked collision state and the selected clearance coordinate as `Z`. On a pivot where `F_i` is nonzero, the vector field

```text
D_i = partial_{i'} - (F_{i'}/F_i) partial_i
```

is tangent to the level set of `F` and is the ordinary derivative when the level is parametrized by `x_{i'}`.

The manuscript explicitly differentiates the variable coefficient at every subsequent order. This matters: freezing `F_{i'}/F_i` would give the wrong second and higher derivatives. The finite diagnostics include a negative control for that error.

The carrier

```text
|F_i| >= a,
|D_i^r Z| >= b
```

therefore describes an actual finite-type condition on the physical roof fiber. For `r=2`, a point can belong to the carrier even when the first tangential derivative vanishes.

I found no endpoint-indexing error in the recentering. The roof includes both the backward and forward portions of the original `m`-collision orbit.

## 13. Fixed-order jet complexity

For a fixed derivative order `r`, the proof adjoins implicit collision jets through order `r` to the physical collision graph. A simple selected root determines the highest jet linearly from lower jets. Reciprocal variables record the nonzero denominators, and no inverse is taken at grazing.

At fixed `r`, the number of variables and polynomial sign conditions is linear in `m`, while the degree is bounded in terms of `r`. The cited sign-component estimate can therefore be bounded by

```text
C_r A_r^m
```

rather than by an `exp(C m log m)` expression. The number of physical center words is itself exponential and can be absorbed into `A_r`.

On a pivot region, `F_i` has fixed nonzero sign after sign stratification. The projection to `x_{i'}` is consequently strictly monotone on a connected regular level component, so that component is a graph over an interval. Subdivision at sign and frontier strata preserves the exponential component bound.

This is a plausible semialgebraic implementation of finite-type coarea. It is also one of the most load-bearing new arguments. A specialist should verify

- uniqueness of the forward and backward implicit jets;
- the degree bound after repeated rational differentiation;
- homeomorphic projection of the augmented graph to the physical source;
- the frontier stratification;
- and the claim that physical seam endpoints are not silently filled by a continued word.

I found no obvious combinatorial exponent error in the written count.

## 14. Finite-type clearance height

On one pivot graph, coarea in the roof variable gives

```text
integral r(X_i(t,v))/|F_i(X_i(t,v))| dv.
```

The chart density is uniformly bounded, the pivot denominator costs `a^(-1)`, and the derivative sublevel lemma bounds the contributing parameter length by `(s_j/b)^(1/r)`. Summing the graph pieces and the depth-dependent widths gives

```text
C_r M A_r^m a^(-1) (epsilon/b)^(1/r).
```

The depth sum

```text
sum_j s_j^(1/r)
```

is uniformly bounded by a constant times `epsilon^(1/r)`. This exponent calculation is correct.

The exact return and displacement events remain disjoint at fixed collision count, so the sum of exact-label inserted variation densities does not acquire a target-count factor.

The theorem is a true essential-height estimate on the stated carrier. It is not merely a mass estimate or an interval-average estimate.

Its limitation is that no uniform finite-type statement is proved. The complementary positive source may contain

- points with no roof pivot above the chosen threshold;
- points whose first `r_*` tangential derivatives are too small;
- roof-critical contacts;
- and physical seam limits.

## 15. The fold corollary

The order-two corollary covers points at which the first tangential clearance derivative vanishes but the second derivative is bounded below. This is a genuine extension of the nonzero-Jacobian estimate in module 132.

Assigning each point to its first qualifying derivative order yields a positive partition. The raw-error inequality then retains one positive remainder and bounds all assigned carriers.

The displayed inequality is algebraically consistent, but it does not improve the order of limits. Every controlled term still contains an exponential factor in `m`, and the unassigned remainder remains present.

## 16. Construction of the physical caustic

The caustic construction imposes a positive incidence cap `chi` and takes physical-side closures of the original word graphs. The selected contact roots remain simple under this cap, so the implicit jets extend continuously to those closures.

The seam condition is

```text
|Z| = R,
```

and the rank condition is

```text
det D(F,Z) = 0.
```

The inherited one-flight geometry gives a nonzero derivative of `Z` in the angular direction on the selected envelope. Thus `dZ` never vanishes there.

At fixed radius, on a smooth path in the seam/rank set, the seam equation gives `dZ=0` along the tangent. Rank zero makes `dF` proportional to `dZ`, so `dF=0` along the tangent. Therefore `F` is constant on each connected component. Continuity propagates the constant across the finitely many semialgebraic junctions.

This is the correct differential mechanism behind finite roof fibers.

## 17. Counting caustic values

For counting only, the proof enlarges the physical-side closure by replacing strict first-hit inequalities with weak inequalities while keeping the contact equations, incidence cap, root-selection signs, jets, seam equation, and rank equation.

This larger graph carries no source measure. It is used only to overcount critical values.

Because the same differential relation holds on each smooth stratum, `F` is constant on each connected component of the enlarged critical graph. A disconnected physical subset of one enlarged component cannot create additional values because the value is already constant on the entire enlarged component.

The fixed-degree semialgebraic component bound, followed by the word and mark count, gives at most `C A^m` roof values in each fixed-radius fiber.

I find the logic coherent. The main point requiring specialist expansion is the passage through singular strata of the weak-inequality graph: one should verify explicitly that the implicit jets and the rank identity persist on every relevant stratum and that continuity identifies the constants at their junctions. This appears repairable if any exposition is missing; I do not identify a counterexample.

## 18. Semialgebraic separation

On the compact capped graph, define

```text
d = min(1, distance((R,F), C_{m,chi})),
f = ||Z|-R| + |J|.
```

The implication

```text
f=0 => d=0
```

has the correct orientation for the compact semialgebraic Lojasiewicz inequality. It yields

```text
d^N <= C f.
```

At an original clearance point, the seam error is at most `2 epsilon`. Therefore, if `d>=h` and

```text
epsilon <= h^N/(4C),
```

then

```text
|J| >= h^N/(2C).
```

The constants and exponents are allowed to depend on `m` and `chi`. The paper does not hide this dependence.

This is a correct finite-count conversion from distance to the caustic into a coarea denominator.

## 19. Positive caustic localization

The clearance source is split into three positive pieces:

1. a later incidence below `chi`;
2. capped incidence and distance below `h` from the caustic;
3. capped incidence and distance at least `h`.

The first piece is not erased merely because the first defect was clearance. The inequality

```text
1_{min_i c_i<chi}
 <= sum_i chi/c_i
 <= (m+1) chi I_m
```

retains the complete later history and is then bounded by the inverse-incidence theorem.

The third piece has a determinant lower bound from the separation lemma and is treated by the same physical area formula as the transverse source.

The result is

```text
C M A^m [ (m+1) chi + C_{m,chi} epsilon h^(-N_{m,chi}) ].
```

The middle piece is the exact original source restricted to the caustic neighborhood. It remains positive.

I find no false source cancellation or exact-label replacement in this partition.

## 20. The raw-error formula with a caustic remainder

The inherited positive raw-error representation gives

```text
P = G + incidence source + clearance source + small fixed-band error
```

in the relevant normalized form. Inserting the incidence gain and the caustic localization yields an all-roof estimate in which the only uncontrolled physical contribution is the positive caustic source, plus explicit finite-count terms.

The canonical finite arithmetic reference `G` is unchanged. Zero residue classes remain zero classes. The new physical bounds do not presume that the arithmetic factor is one.

This is a useful reduction. It identifies a geometric remainder rather than a maximal-function exceptional set defined from the unknown density.

It is not closure of the raw theorem because the caustic source remains and the explicit errors are not small in the required collision limit.

## 21. Tube measure and source mass

A compact semialgebraic subset of parameter--roof space with finite vertical fibers has a vertical `h`-neighborhood whose length tends uniformly to zero. Cell decomposition expresses each vertical section as a finite union of intervals with semialgebraic endpoints. Taking the supremum over the compact radius interval preserves definability. A one-variable growth theorem then gives a positive power modulus

```text
D_{m,chi} h^(beta_{m,chi}).
```

This is a reasonable definable-geometry argument. The proof correctly avoids claiming that an arbitrary integral of a semialgebraic function is semialgebraic.

The inherited weak-`L^(145/144)` estimate converts this roof length to source mass with exponent `1/145`.

The conclusion is a mass bound. It gives no essential-height control inside the tube. The manuscript states this distinction repeatedly and correctly.

## 22. Exact labels and physical conventions

The new physical modules retain

- the original actual-return source `nu_R^*`;
- exact return index `n`;
- exact displacement label `k`;
- exact collision count `m`;
- occupation at collision times `0,...,m-1`;
- terminal section membership separately at `m`;
- clearance read at image collision `j+1`;
- the original first-physical-defect ordering;
- the selected responsible competing disk;
- later low-incidence history after a first clearance;
- the canonical arithmetic transition kernel and its zero classes.

The factor `1/c_*` is introduced once through the section source and is not duplicated in the new coarea bounds.

I found no convention mismatch in the audited chain.

## 23. The decisive order-of-limits obstruction

The unrestricted pointwise criterion uses a reconstruction width of the form

```text
epsilon(B) = A_0 B^(-1/12)
```

and a fixed-band error whose collision-count limit is taken before `B` tends to infinity.

The new finite-count bounds contain

```text
m^2 A^m epsilon(B),
m^2 A_r^m a^(-1)(epsilon(B)/b)^(1/r),
m^2 A^m C_{m,chi} epsilon(B) h^(-N_{m,chi}).
```

For a fixed `B`, these quantities are not shown to tend to zero as `m` tends to infinity. Choosing `a`, `b`, `chi`, or `h` as functions of `m` merely shifts the problem into the uncovered source or into uncontrolled separation constants. Choosing `B` exponentially in `m` is not permitted by the fixed-band spectral theorem.

The tube estimate has the same limitation. Its exponent and constant depend on `m` and `chi`; no uniform modulus is available in the collision limit.

Thus the new work does not merely lack a final epsilon-management paragraph. It lacks the central quantitative bridge from finite-word geometry to the ordered asymptotic regime.

## 24. What revisions 61--62 close

Relative to the revision-60 report, the combined packet closes several real mathematical questions.

- The complete inverse-incidence product has a finite roof density at every finite collision count.
- The original first-incidence source gains its physical width in essential height.
- The transverse part of the original next-collision clearance source has a direct two-coordinate coarea bound.
- Rank deficiency is retained explicitly rather than hidden.
- Fixed-order tangency along a regular roof fiber is controlled.
- Second-order folds are included.
- The physical seam/rank caustic has finite fixed-radius fibers.
- Away from the caustic, a quantitative physical determinant is recovered.
- A later low incidence after a first clearance is retained in the source partition.
- The remaining source is geometrically localized rather than defined by an unknown-density level set.
- Its roof tube and source mass are small at fixed count.

These are genuine advances on the original Lorentz geometry, not transfers from the Markov model.

## 25. What revisions 61--62 do not close

The following remain unproved.

1. A collision-uniform or ordered central-scale incidence height.
2. A collision-uniform or ordered central-scale clearance height.
3. Uniform finite type on the full clearance source.
4. Quantitative count control of the caustic separation exponents.
5. Essential-height control of the retained caustic source.
6. The unrestricted two-sided pointwise arithmetic raw-density theorem.
7. Unrestricted same-roof collision and return bridges.
8. Forward essential-likelihood convergence.
9. The unrestricted pointwise roof-conditioned path theorem.
10. Triviality of the finite arithmetic factor.
11. Independent specialist certification of the inherited and new continuum chain.

The status files acknowledge every item in this list.

## 26. Why small caustic mass is not sufficient

Suppose a positive density is supported on an interval of width `w` and has height `w^(-1/2)`. Its mass tends to zero as `w` tends to zero while its height diverges.

More extreme examples can have arbitrarily small mass and arbitrarily large height.

Therefore none of the following implications is valid:

- a small caustic tube implies a small caustic density;
- a small original-source probability implies an essential-height bound;
- fixed-count finite fibers imply a count-uniform density estimate;
- finite-type control off the remainder implies finite type on the remainder;
- total variation of the complete mixed record implies pointwise roof-density convergence;
- good-set same-roof control implies an unrestricted same-roof theorem.

The manuscript avoids these invalid implications. The point is not an overclaim by the authors; it is the reason the title-level theorem remains open.

## 27. Novelty and significance

The determinant cancellation and its use for an unbounded inverse-incidence insertion are interesting billiard-specific observations. The finite-type fiber coarea and physical caustic localization provide a more geometric description of the remaining obstruction than the earlier maximal-function good-set theorem.

The general tools used in revision 62 are classical:

- divided differences and Rolle's theorem;
- semialgebraic sign-component bounds;
- Tarski--Seidenberg projection;
- compact semialgebraic Lojasiewicz separation;
- cell decomposition;
- layer cake and weak-`L^p` source conversion.

Their value lies in the exact implementation on the original physical source with all labels and marking conventions retained.

At the requested venue level, however, the new result is still a finite-count reduction with uncontrolled asymptotic constants. It does not yet produce a new asymptotic phenomenon, a completed pointwise theorem, or a reusable quantitative theorem verified in several distinct singular systems.

The broader manuscript contains substantial integrated arithmetic, bridge, pressure-contact, and Markov realization results. Those results may support one or more strong specialist papers if the inherited chain survives expert audit. The current combined submission still derives much of its editorial claim from an endpoint which remains unproved.

## 28. Architecture and readability

The direct route document is helpful. A reader interested only in the new physical source analysis can move through modules 104, 105, 94, 131, 133, and 134 without first traversing the entire Markov and pressure chain.

Nevertheless, the journal article still contains

- 134 numbered core modules;
- several generations of leading statements;
- the full pressure/contact and model-realization program;
- the global integrated raw law and bridge theory;
- the unresolved pointwise Lorentz program;
- extensive provenance and validation material.

This is an extraordinary verification burden for any editorial process. The new synopsis does not by itself resolve the mismatch between the completed integrated theorems and the unfinished pointwise title-level theorem.

For a high-level dynamics or probability submission, the authors should choose one principal endpoint and organize the paper around the shortest complete proof of that endpoint. Preservation of historical source in the repository need not imply that all historical stages belong in one journal article.

## 29. Independent specialist verification

No independent human audit has been obtained. The following points are especially load-bearing.

### Revision-61 inputs

1. The exact reduced-action Hessian and corner-cofactor identity.
2. Positivity of the internal contact matrix on every regular word.
3. Endpoint injectivity for a fixed center word.
4. The rational chart convexity and total-curvature estimates.
5. Coefficient-independent level complexity.
6. The complete inverse-incidence density near all grazing boundaries.
7. Physical multiplicity of `(L_m,Z)` with nonzero determinant.
8. The exact `j+1` next-collision convention.

### Revision-62 inputs

9. Repeated tangential differentiation with all variable coefficients.
10. Uniqueness of fixed-order implicit forward and backward collision jets.
11. Fixed-degree polynomial encoding of those jets.
12. Projection of augmented jet graphs to the physical source.
13. Graph-interval subdivision without continuation across seams.
14. Coarea with the marked recentered source and exact labels.
15. Compactness and semialgebraicity of the capped physical-side closures.
16. Nonvanishing of `dZ` on the seam envelope.
17. Constancy of `F` on every connected seam/rank stratum.
18. Use of the weak-inequality graph only as a counting overcover.
19. The direction and uniformity domain of the separation inequality.
20. The complete three-piece positive source partition.
21. Definability and power control of vertical tube length.
22. The inherited weak-integrability constant used in the mass conversion.

### Inherited global chain

23. The anisotropic collision operators and full occupation twist.
24. Moving resonance branches and physical peripheral representatives.
25. The canonical finite arithmetic transition kernel.
26. The complete positive raw-error representation.
27. The exact first-physical-defect source partition.
28. The path-valued source identities and joint clock transfer.
29. Uniformity in the radius through arithmetic changes.
30. Exact normalization by the section mass.

Source hashes, finite polynomial fixtures, and successful typesetting do not substitute for this audit.

## 30. Required mathematical changes before another top-four review

A subsequent revision seeking the same benchmark should address the following items.

### 30.1 Convert finite-count incidence control into the ordered height limit

Prove the actual statement required by the positive criterion:

```text
lim_{B->infinity} limsup_{m->infinity}
  sup_{R,n,k,central u}
  m^2 b_inc^{epsilon(B)}(u) = 0.
```

A bound `C A^m epsilon(B)` is not enough. The proof must respect the fixed-band/collision-count order.

### 30.2 Control the complete clearance source

Either prove a uniform finite-type theorem with quantitatively usable constants, or obtain another mechanism which controls the retained roof-critical/seam source in essential height.

A tube-mass estimate is not a substitute.

### 30.3 Quantify the caustic geometry in the collision count

The quantities

```text
C_{m,chi}, N_{m,chi}, D_{m,chi}, beta_{m,chi}
```

must be controlled in a way compatible with the reconstruction width and the collision limit. Merely proving their finiteness for each `m` does not affect the central asymptotics.

### 30.4 Close the unrestricted pointwise theorem

Combine the two physical height estimates with the existing positive raw-error representation and canonical arithmetic kernel. Retain zero arithmetic classes and the actual fixed-radius residue unless a separate triviality theorem is proved.

### 30.5 Derive the exact-roof consequences only after height closure

Unrestricted same-roof bridges, pointwise conditional laws, and forward essential likelihood should be deduced from the completed scalar theorem, not from mass localization or integrated variation.

### 30.6 Obtain independent specialist review

The endpoint action, contact determinant, physical graph, jet encoding, caustic geometry, anisotropic spectrum, and raw source decomposition require external human verification.

### 30.7 Decide the paper's principal contribution

Either complete the Lorentz pointwise theorem and retain the unified title, or center a shorter article on the strongest completed integrated/pressure/coarea theorem and present the unfinished pointwise program separately. This is not a request to delete repository history.

### 30.8 State the quantitative novelty theorem by theorem

For each completed theorem, explain precisely what is not supplied by existing Lorentz-process local limits, billiard endpoint local limits, suspension-flow local limits, finite-state Markov additive theory, or standard semialgebraic coarea arguments after their hypotheses are checked.

## 31. Technical and presentation comments

1. Keep `epsilon`, `eta`, `a`, `b`, `chi`, `h`, `B`, `m`, and the finite-type order visibly distinct.
2. State in every finite-type theorem that `r` is fixed before the component constants are chosen.
3. Keep the physical source and the counting overcover separate in notation.
4. State explicitly whenever weak first-hit inequalities are used only for component counting.
5. Keep the exact image mark `j+1` visible in all clearance formulas.
6. Retain the entire two-sided roof in `F` after recentering at the mark.
7. Do not abbreviate `D_i^r Z` in a way that suggests frozen coefficients.
8. State that `|F_i|>=a` includes a sign stratification before graph monotonicity is invoked.
9. Keep the source outside the finite-type carrier explicitly positive.
10. Do not call the order-two carrier the complete rank-zero source.
11. Keep the capped caustic distinct from the full uncapped clearance geometry.
12. State that the distance in the separation lemma is in parameter--roof space.
13. Keep all dependence of separation constants on `(m,chi)` explicit.
14. State that finite vertical fibers are a fixed-count conclusion.
15. Keep tube length, source mass, and source height as three separate quantities.
16. Do not infer an essential-height estimate from the exponent `1/145`.
17. Keep later low incidence after first clearance in the source partition.
18. State when exact-label restrictions are deleted only for positive domination.
19. Keep the sum of exact-label variation densities distinct from probability TV.
20. Retain the factor one half in probability total variation elsewhere in the article.
21. Keep `G` as the signed canonical transition kernel in raw inversion.
22. Normalize only its positive part when constructing a probability reference.
23. Do not assign a conditional law to a zero arithmetic class.
24. Preserve the fixed-band/collision-limit/band-limit order in every synopsis.
25. Do not advertise exponentially count-dependent finite estimates as central-scale estimates.
26. State which null sets arise from coarea and which arise from regular conditional versions.
27. Keep the specialist audit boundary adjacent to the main new theorem.
28. Separate native build evidence from mathematical verification.
29. Consider moving provenance and validation ledgers outside the journal narrative.
30. Give a short dependency diagram for modules 131--134 in the compiled paper, not only in repository Markdown.

## 32. Final assessment

Revisions 61 and 62 make real progress on the original Lorentz source.

The inverse-incidence determinant cancellation is a useful physical identity. It yields a finite-count essential-height gain for the first-incidence source. The direct two-coordinate coarea theorem controls transverse clearance without changing the next-collision convention. The finite-type theorem reaches tangencies along regular roof fibers and includes second-order folds. The caustic theorem gives a concrete geometric location for the remaining loss of rank and retains the exact positive source there.

I found no decisive error in the formulas or positive source bookkeeping of modules 131--134, subject to the specialist checks listed above.

The mathematical boundary, however, is unchanged at the level decisive for the title and requested venue. Every new height estimate has exponential or otherwise uncontrolled collision-count dependence. The caustic source has small fixed-count mass but no essential-height bound. The two ordered physical height limits therefore remain open, and so does the unrestricted pointwise arithmetic raw-density theorem.

The combined manuscript also remains extremely large, model-specific, and dependent on a continuum proof chain that has not received independent expert verification.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**

A focused specialist-journal paper on the determinant cancellation, finite-type clearance coarea, and physical caustic localization could be valuable if the inherited geometric inputs are independently checked and the scope is sharply stated. A future top-four submission should return only after the retained positive caustic source is controlled in the correct ordered central regime, or after the authors extract and validate a substantially broader theorem whose significance no longer depends on that unresolved endpoint.
