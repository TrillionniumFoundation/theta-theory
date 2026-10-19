# External top-four referee report on A2-DYN revision 75

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v75-referee-response-2026-10-11`, `revision/a2-dyn-v75-referee-copy-2026-10-11`  
**Reviewed commit:** `fa296376d1b25b0d10459c00d02c58834c500b45`  
**Reviewed repository tree:** `f6a6ccd8eb9cf65816051a18329fe31e88b71fd4`  
**Active manuscript directory:** `papers/A2-DYN-v75-referee-response`  
**Active mathematical source:** one hundred seventy numbered core modules; revision 75 adds modules 168--170  
**Frozen revision-74 author baseline:** `5a4704bc945d75e0fa181983a7b66a5dc5a73350`  
**Frozen revision-74 paper tree:** `02bac634205e7f776793ba330c98c11039fd71d5`  
**Controlling report:** `reviews/a2-dyn-v74-external-top4-review-2026-10-11/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `18c51226fbc3bcc580ae66bee926d944be590c81` / `83ab4fa82c4f5be6ee930865c87633ef5d94717f`  
**Exact-source qualification runs:** response `38104806102`; referee-copy `38104818195`  
**Date:** 11 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, convex-geometry, geometric-measure-theory, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 75 is a genuine theorem-bearing revision and a mathematically substantive response to the revision-74 report. The preceding revision had isolated the remaining scalar obstruction as the collision-normalized height of short positive superlevel excursions of the complete exact-label roof density. Its fixed-count tame and `BV` arguments did not control the number or total turning of all physical level components of one long collision word uniformly in the collision count.

Revision 75 removes that particular geometric loss. For every regular physical word it constructs, on a fixed cover of at most 256 endpoint-cap coordinate rectangles, a single strongly convex supporting action on the whole endpoint rectangle. The supporting action agrees with the actual reduced roof on every regular physical component of the word, even when the physical endpoint image is disconnected. The physical reduced Hessian is bounded between the explicit constants

```
50/47  and  1360/9
```

independently of the word length and of every positive incidence and clearance.

The manuscript then uses the boundary of one convex sublevel set to control all physical level arcs of that word simultaneously. The outward Gauss map is injective on those arcs up to null sets, and the coarea integral satisfies

```
integral_{physical level} dH^1 / |grad F_w| <= 2*pi/lambda.
```

This removes the former wordwise level-complexity factor. It also yields an exact positive Gauss trace for the original exact-label return density and a sharper complete inverse-incidence height estimate.

I audited the new modules

- `core/168_convex_support_endpoint_caps.tex`;
- `core/169_wordwise_gauss_coarea.tex`;
- `core/170_physical_gauss_trace_tail.tex`;

as well as their use in the journal-facing `main.tex`, the response, proof ledger, active audit map, source manifest, and qualification evidence. I found no decisive counterexample, sign reversal in the endpoint gradients, loss of an exact label, illicit addition of an auxiliary trajectory to the source, incorrect orientation of the Gauss map, or hidden claim that a per-word estimate already controls the complete word sum.

The revision is explicit about its remaining gap. The new geometry bounds one word uniformly, but it does not prove a collision-normalized modulus for the **complete weighted sum over all physical words**. The sufficient hypothesis in module 170 is

```
D_{epsilon,M}(r) <= A epsilon^{-q} r^beta,
```

where `D_{epsilon,M}(r)` is the normalized paired roof modulus of the entire exact-label Gauss trace after the word sum has been taken. This estimate is not proved. The available complete inverse-incidence bound still contains an exponential word sum and cannot be used as an `m^{-2}` estimate.

Consequently revision 75 does not prove the organizing pointwise raw local limit theorem, the pointwise roof-density theorem, unconditional same-roof path conditioning, or forward essential-likelihood convergence. At the requested benchmark, replacing an uncontrolled level-complexity factor by a precise positive trace is important progress, but it is not a substitute for proving that trace small in the required dynamical scaling.

## 2. Frozen source, preservation, and qualification

Both reviewed author branches resolve to

`fa296376d1b25b0d10459c00d02c58834c500b45`.

The repository tree at that commit is

`f6a6ccd8eb9cf65816051a18329fe31e88b71fd4`.

The active source directory is

`papers/A2-DYN-v75-referee-response`.

The source manifest identifies revision 74 at

`5a4704bc945d75e0fa181983a7b66a5dc5a73350`

as the frozen author baseline and the revision-74 report at

`18c51226fbc3bcc580ae66bee926d944be590c81`

as the controlling review.

The manifest records 167 inherited core modules and 170 active modules. The three additions are precisely modules 168--170. All inherited cores, appendices, Python sources, and both bibliographies are recorded as byte-preserved. The active journal article contains the new proof route, while the complete technical supplement retains the preceding proof archive.

The active status files correctly distinguish the new geometry from the missing endpoint. In particular, they record as true:

- the fixed endpoint-cap cover;
- global convex support for each physical word;
- collision-independent wordwise endpoint curvature;
- collision-independent wordwise Gauss coarea;
- the complete exact-label positive Gauss trace;
- removal of the level-complexity loss from the inverse-incidence estimate; and
- the implication from a paired Gauss-trace modulus to the scalar endpoint.

They retain as false:

- collision-uniform weighted-word trace decay;
- physical short-excursion decay;
- the unrestricted raw return LLT;
- the pointwise roof-density LLT;
- unrestricted same-roof path conditioning;
- forward essential-likelihood convergence;
- independent human review; and
- formal proof certification.

The exact-SHA qualification workflows completed successfully on both reviewed refs:

- response branch run `38104806102`;
- referee-copy branch run `38104818195`.

The build evidence establishes source identity, preservation of the frozen baseline, finite-fixture agreement, native compilation of the eight-page journal article and the complete supplement, recorder coverage of all 170 cores, and PDF geometry checks. It does not certify the continuum convex-support argument, the all-level coarea passage, the inherited spectral and arithmetic inputs, or the missing weighted trace estimate.

The present review branch starts directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v75-external-top4-review-2026-10-11/`.

No author source, workflow, prior report, historical module, or unrelated repository path is intentionally modified.

## 3. Scope of this audit

The complete source contains 170 core modules and a long inherited pipeline. I have not attempted to re-prove every historical statement. The substantive audit concentrates on:

1. the sixteen-direction endpoint-cap cover;
2. the endpoint orientation and the physical length gradient;
3. the auxiliary convex endpoint value;
4. the global affine support inequality;
5. uniqueness of the physical internal contact tuple;
6. construction and finiteness of the supporting envelope;
7. the lower and upper reduced-Hessian bounds;
8. the treatment of disconnected physical endpoint images;
9. injectivity of the Gauss map across all physical level pieces of one word;
10. the complexity-free coarea estimate;
11. the exact endpoint coordinate Jacobians and inverse twist;
12. retention of the original exact event and source normalization;
13. the inverse-incidence corollary;
14. the complete trace and its one-sided roof moduli;
15. the implication from trace modulus to level-component tails;
16. the legal order of the finite Riemann sums and collision limits;
17. the distinction between uniform per-word geometry and the unproved complete weighted sum;
18. journal and supplement architecture; and
19. source identity and qualification evidence.

The inherited fixed-count `BV` theorem, fixed-width estimate, positive scalar remainder, short-excursion equivalence, path-remainder theorem, arithmetic transition reference, and collision-to-return clock transfer are treated as source-pinned inputs. This report does not independently recertify them.

## 4. The endpoint-cap cover

Module 168 fixes sixteen evenly spaced directions

```
e_j = (cos(2*pi*j/16), sin(2*pi*j/16)).
```

For any unit normal `n` and endpoint velocity direction `w` with positive scalar product, the shorter angle between `n` and `w` is less than `pi/2`. The midpoint is within `pi/4` of each, and a closest grid direction is within `pi/16` of that midpoint. Hence the selected direction is within `5*pi/16 < pi/3` of both vectors, so both scalar products exceed one half.

This calculation is correct. It gives a fixed cover independent of the collision count and does not require a positive lower incidence margin.

On each selected cap the projection coordinate

```
Q_j(s) = C + s e_j^perp + sqrt(R^2-s^2) e_j
```

is single-valued for `|s| < sqrt(3)R/2`. The printed first- and second-derivative bounds follow from the explicit formula and the radius lower bound. Choosing the first admissible direction at each endpoint gives a Borel partition into at most 256 cap pairs.

This cap partition is an efficient way to avoid singular normal coordinates near grazing. A later quantitative trace theorem must nevertheless control transitions across first-admissible cap boundaries; those transitions are harmless for the exact density identity but can contribute to the chosen trace modulus.

## 5. The global supporting inequality

For a fixed word `w=(C_0,...,C_m)`, the auxiliary value

```
V_w(q_0,q_m) = min sum |q_{i+1}-q_i|
```

is taken over internal points in the corresponding closed disks. These minimizers are comparison objects only; the manuscript does not assign them physical labels or source mass.

At a regular physical reflected contact, the gradient of the two adjacent length terms with respect to the contact position is

```
-2 c_i n_i,
```

with `c_i>0`. If the comparison point remains in the closed disk, its displacement from the physical boundary point has nonpositive outward-normal component. The internal first-order contribution is therefore nonnegative and is strictly positive unless the contact is unchanged.

The joint convexity of polygonal length then gives the affine support inequality printed in module 168. With the endpoints fixed, it also proves that the physical internal contact tuple is the unique minimizer. Two regular physical trajectories of the same word with the same endpoints must coincide.

I found this argument coherent. It is important that the minimization is over the closed disks and that all physical flights and incidences are strictly positive. The proof uses the auxiliary minimization only as a convex comparison and does not continue a billiard orbit through a singularity.

## 6. The supporting envelope and the lower curvature bound

For a cap pair, the manuscript takes the supremum of the affine supports supplied by all regular physical trajectories of the word satisfying the strict cap tests.

Each support is strongly convex in the two cap coordinates. Its diagonal second derivative contains

```
(w_i dot e_{j_i}) R^2 / (R^2-s_i^2)^(3/2),
```

which is at least `1/(2R_+)`. Subtracting the corresponding quadratic leaves a convex function; taking a supremum preserves convexity. The supports are uniformly finite at each fixed word because the roof and endpoint displacements are bounded.

The support inequality shows that every support lies below `V_w`, while the support belonging to a physical trajectory attains the physical roof at its own endpoint pair. Hence the envelope agrees with the physical reduced roof on every regular open physical component.

This is the decisive global step. It avoids the invalid inference that local positive Hessians on disconnected physical pieces control the total turning of all those pieces. Instead, every physical piece lies on the boundary of one strongly convex sublevel set.

I found no contradiction in this argument. A specialist should still check the regularity statement at every active constraint and the precise identification of the reduced action with the endpoint value on all regular branches, but the written proof supplies the correct convex mechanism.

## 7. The upper reduced-Hessian bound

The lower Hessian bound follows from equality with the strongly convex envelope on a regular open physical piece.

For the upper bound, the manuscript freezes the internal contacts and varies only the two endpoints. This produces an admissible trial polygonal length touching the reduced action from above. Equivalently, the physical reduced Hessian is bounded by the endpoint block of the full second variation after minimizing over internal variations.

The endpoint projection derivatives are bounded, every physical flight has length at least the uniform gap `tau_-`, and the cap curvature is bounded by the radius lower bound. The printed constant is deliberately coarse. The one-flight case is treated by allowing both endpoint variations on the same segment.

This yields the stated upper bound without a word-length factor. The proof makes no claim of a uniform physical neighborhood, a uniform third derivative, or a smooth continuation through grazing or first-hit boundaries.

I found the scale and dependence of this estimate plausible and internally consistent. Independent verification should reproduce the full endpoint second-variation calculation, particularly the one-flight cross term and the endpoint-curvature contribution.

## 8. All-level Gauss coarea without a complexity factor

At a regular point of a physical level, the physical roof agrees locally with the convex envelope, so the point lies on the boundary of the envelope's convex sublevel set. Its outward normal is the normalized roof gradient.

Two distinct points of a convex boundary with the same supporting normal lie in the same exposed face. A positive-curvature physical point in an open regular arc cannot lie in a nontrivial exposed segment. Thus the outward Gauss map is injective across all regular physical level arcs of the word and cap pair, even when physical exclusions split the level into many components.

Along a smooth level arc,

```
d theta = (H_T/|grad F|) dH^1.
```

The angular image has measure at most `2*pi`, and `H_T >= lambda`. Therefore

```
integral dH^1/|grad F| <= 2*pi/lambda.
```

The manuscript applies the argument on compact regular exhaustions and uses monotone convergence. Stationary levels and artificial rectangle edges do not receive physical source mass in the formula.

This is a genuine removal of the earlier level-component complexity factor. I found no missing orientation or repeated-normal counterexample in the written argument.

## 9. The exact positive Gauss trace

On a regular word, the change of variables from the initial collision coordinates to the two endpoint angles has Jacobian `|B_m|^{-1}`, where `B_m=partial_{p_0} alpha_m` is the nonzero twist. The cap coordinates contribute the two projection Jacobians, and the Gauss change of variables contributes `H_T^{-1}`.

The trace term is therefore

```
W * 1_Pi * 1_a
----------------------------------------------
4*pi*c_* * R^2 * cap_0 * cap_m * |B_m| * H_T.
```

The first-admissible cap partition is disjoint at the source. The event indicator retains the exact displacement, occupation count, terminal section membership, and original source normalization. Auxiliary convex minimizers are never included in the measure.

Endpoint injectivity and nonzero twist give a Borel inverse on each regular piece. Summing the nonnegative terms by Tonelli yields the original pushforward density. The formula extends to bounded signed or complex insertions by linearity.

I found no label pooling or missing `c_*^{-1}` factor. The lower cap bounds and `H_T>=lambda` give the stated geometric majorant.

There is, however, an important quantitative distinction. The trace parameter `theta` is chart-dependent: changing a cap pair changes the endpoint coordinates and therefore the numerical normal angle used in that term. The exact density identity is unaffected because each term is integrated over its own full angular circle. The paired trace modulus in module 170 is consequently a sufficient, representation-dependent upper bound. A proof of its collision-uniform decay must control artificial cap reassignment and zero-extension effects, or replace the first-admissible representation by a chart-invariant coupling. This is not a logical flaw in the current implication, but it is part of the remaining dynamical burden.

## 10. The inverse-incidence corollary

The inherited contact-determinant identity bounds the product of inverse incidences times the mixed endpoint derivative by a product of inverse flight lengths. Combining that identity with the cap Jacobians and the complexity-free coarea estimate gives the explicit complete inverse-incidence height bound.

The former level-complexity factor is absent. This is a real improvement.

The resulting estimate still includes

```
D^m * (R_+/(2*tau_-))^(m-1),
```

where `D` is the finite next-center alphabet size. It is therefore exponential in the collision count. The manuscript correctly states that this cannot be inserted as a central-scale `m^{-2}` estimate.

The corollary controls an unbounded geometric insertion at fixed collision count and may be useful in later distortion estimates. It does not control the complete exact-label trace modulus required by the pointwise theorem.

## 11. From the trace to short superlevel excursions

Module 170 writes the complete guarded source as

```
b^epsilon(t) = integral Gamma^epsilon(t,theta) dtheta.
```

The whole word and cap sum is taken before the positive part in the one-sided trace moduli. This ordering is necessary: applying the positive part word by word would destroy cancellations already present in the positive density representation.

If the essential superlevel component of `f` through `t` has length less than `r`, both of its endpoints lie within distance `r`. Immediately outside each endpoint there is positive measure on which `f` is below the level. Hence the measure of all such levels is bounded by the smaller of the left and right one-sided drops of `f`.

For either sign,

```
[f(t)-f(t+h)]_+ <= integral [Gamma(t,theta)-Gamma(t+h,theta)]_+ dtheta.
```

This proves the trace-to-tail inequality. Averaging in `r` gives the short-excursion bound.

I found this deterministic implication correct. It uses the complete scalar density, not superlevel components formed separately for individual words.

## 12. The legal order of limits

The sufficient trace premise is inserted through finite upper Riemann sums. The outer Fourier band, guard scale, roof width, finite mesh, and auxiliary fixed-width spectral band are chosen before the collision limsup. The mesh is refined and the auxiliary band enlarged only afterwards; the outer band is enlarged last.

This respects the order already required by the inherited fixed-band estimates. No collision-dependent spectral band is introduced.

The constant `1/(beta+1)` in the resulting estimate is the correct Riemann-sum limit under the stated power premise.

## 13. The decisive unresolved estimate

The remaining quantity is

```
D_{epsilon,M}(r)
 = limsup_m sup_{R,n,k} m^2 esssup_{central t}
      min{omega_r^- Gamma(t), omega_r^+ Gamma(t)}.
```

Revision 75 proves only that a bound of the form

```
D_{epsilon,M}(r) <= A epsilon^{-q} r^beta
```

would imply the original scalar endpoint.

It does not prove this bound.

The uniform geometry of a single word does not control the following effects after summing all physical words:

1. the exponential number of admissible center words;
2. the distribution of the inverse twist `|B_m|^{-1}`;
3. the exact occupation and displacement constraints;
4. creation and disappearance of first-hit branches as the roof varies;
5. changes of the guard near incidence and clearance defects;
6. cap reassignment in the first-admissible coordinate partition;
7. zero-extension across word and cap boundaries;
8. concentration of many small positive terms on a short roof interval; and
9. the required `m^2` normalization on every central exact label.

The complete trace is positive, so one cannot appeal to cancellation between signed word contributions. What is needed is a genuine weighted dynamical summability or regularity theorem for the exact-label inverse branches.

The explicit inverse-incidence bound remains exponential and is therefore far too weak. Source mass, fixed-count `BV`, total turning of each word, and the exact density identity do not rule out narrow high trace peaks.

This is the principal reason for the negative recommendation.

## 14. What revision 75 has achieved relative to revision 74

Revision 75 is not a relabeling of the previous obstruction.

Revision 74 reduced the endpoint to the length distribution of short positive superlevel components but retained a possible collision-dependent complexity loss in wordwise coarea. Revision 75 proves that this complexity loss is artificial: one convex envelope controls all level pieces of a word and gives one inverse per normal direction.

The remaining obstruction is now located in a completely explicit positive trace carrying the original labels and inverse-twist weights. This is a cleaner and more useful reduction.

The reduction nevertheless remains a reduction. It has moved the difficulty from the number of level pieces to the weighted sum of physical inverse branches. The latter is exactly the dynamical estimate needed for the local limit theorem and remains open in the submitted source.

## 15. Consequences still unavailable

Until the complete weighted trace modulus is controlled, the manuscript does not establish unconditionally:

- the exact-label scalar pointwise raw local limit theorem;
- the pointwise roof-density local limit theorem;
- a positive pointwise denominator on every positive arithmetic class;
- the same-roof point-conditioned collision bridge;
- the actual-return path theorem after the inherited clock transfer;
- forward essential arithmetic likelihood convergence; or
- the full endpoint consequences claimed by the historical pipeline.

The inherited scalar/path equivalence shows that these downstream claims share the scalar obstruction. It does not make them unconditional.

## 16. Top-four significance

The convex-support and all-level coarea mechanism is an elegant technical advance. It may be useful beyond this particular manuscript, especially in settings where singular exclusions disconnect the physical image of a variationally convex action.

In the current article, however, the mechanism remains specialized to circular dispersing billiards, a fixed lattice and section, and a source-pinned analytic pipeline. No broad theorem is stated for a general class of convex scatterers or singular twist systems, and no second independent realization is supplied.

More importantly, the article's organizing pointwise local limit theorem remains unproved. At the requested venue level, a technically strong reduction cannot replace the central theorem around which the title, abstract history, and 505-page supplement are organized.

A positive top-four case would require at least one of the following:

1. proof of the complete collision-normalized weighted trace modulus and hence the original raw pointwise theorem;
2. a general weighted Gauss-trace theorem for a broad class of singular hyperbolic systems, with several genuinely different applications; or
3. another theorem of comparable independent significance whose editorial value does not depend on the unfinished Lorentz endpoint.

Revision 75 does not yet meet any of these alternatives.

## 17. Journal and supplement architecture

Separating an eight-page journal-facing article from the complete technical supplement is an editorial improvement. The journal article clearly states which analytic interfaces are imported and which new geometry is proved.

The present separation is not yet a conventional submission package. The journal theorem relies on numerous source-pinned inputs whose statements and proofs are distributed through a 505-page historical supplement. Before formal submission, every imported hypothesis, uniformity, and conclusion needed by the journal argument should be restated in a self-contained theorem chain, with provenance and revision history moved outside the mathematical supplement.

The main article should also make the representation dependence of the paired trace modulus explicit. The exact density is canonical; the chosen trace on the common numerical `theta` circle depends on the cap partition. This is acceptable for a sufficient criterion, but it matters for the feasibility and interpretation of the missing estimate.

## 18. Independent specialist audit still required

No independent human audit is recorded. The highest-priority checks are:

1. the endpoint orientation and the sign `-2 c_i n_i`;
2. strictness of the support inequality over closed disks;
3. uniqueness and smooth dependence of the physical constrained minimizer;
4. equality of the envelope and the reduced roof on every regular physical component;
5. the endpoint second-variation upper bound, including the one-flight case;
6. Gauss-map injectivity across disconnected physical pieces;
7. treatment of stationary levels, singular boundaries, and compact exhaustions;
8. the endpoint twist change of variables and both cap Jacobians;
9. the inverse-incidence determinant identity and all constants in the corollary;
10. Borel inversion and zero extension of the word/cap traces;
11. the trace-to-tail argument on essential superlevel components;
12. the inherited fixed-width and positive-remainder estimates;
13. the arithmetic transition and path-remainder chains; and
14. the eventual collision-uniform weighted trace estimate.

Finite fixtures, source hashes, recorder coverage, and PDF checks cannot certify these continuum arguments.

## 19. Required changes before another top-four review

A genuinely new revision should address the following matters.

1. **Prove the complete weighted trace modulus.** Establish the stated power bound, or another estimate which makes the ordered trace modulus and short-excursion budget vanish in the legal limit order.
2. **Control cap and word transitions.** Either prove that the present first-admissible trace has a collision-uniform modulus despite chart switching and zero extensions, or replace it by a chart-invariant trace/coupling with an equally exact density formula.
3. **Derive weighted summability from the dynamics.** A per-word turning bound must be combined with actual control of the inverse twist, branch weights, occupation constraint, and exact-label word sum.
4. **Keep every original label.** Displacement, collision count, return index, section occupation, terminal membership, and arithmetic zero classes must not be pooled to obtain the estimate.
5. **Respect the order of limits.** Guard scales, roof widths, trace meshes, and auxiliary spectral bands must be fixed before the collision limsup in the order stated by the inherited interfaces.
6. **Close the scalar theorem first.** Invoke path and likelihood consequences only after the scalar pointwise endpoint is unconditional.
7. **Make the journal theorem self-contained.** Restate all imported analytic inputs in a compact theorem chain rather than relying on revision-index navigation.
8. **Obtain independent human review.** The convex support, coarea, twist, tame, spectral, and arithmetic components require specialists in the relevant areas.

## 20. Final assessment

Revision 75 is a meaningful mathematical advance over revision 74.

It proves collision-independent convex support and curvature for every regular physical word, controls all physical level pieces of a word through one convex Gauss map, removes the wordwise level-complexity factor, and gives an exact positive trace retaining the original labels and source.

I found no decisive error in modules 168--170.

The remaining obstruction is now sharper but still unproved: collision-uniform control of the complete weighted exact-label Gauss trace after summing all physical words. The available estimate is exponential rather than central-scale, and the sufficient trace modulus remains a hypothesis.

Until that estimate is established, the manuscript does not prove its organizing raw pointwise local limit theorem and is not ready for *Annals*, *Acta*, *Inventiones*, or *JAMS*.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
