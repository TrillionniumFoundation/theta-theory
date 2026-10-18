# External top-four referee report on A2-DYN revision 81

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v81-referee-response-2026-10-11`, `revision/a2-dyn-v81-referee-copy-2026-10-11`  
**Reviewed commit:** `49957346c784071bf6f2e18a7ae6f2d724254f20`  
**Reviewed repository tree:** `0919c3785e33a6a1c7b169f43db23ba88d6df511`  
**Active manuscript directory:** `papers/A2-DYN-v81-referee-response`  
**Journal entry / technical supplement:** `main.tex` / `supplement.tex`  
**Active mathematical source:** one hundred eighty-eight numbered core modules; revision 80 adds modules 183--185 and revision 81 adds modules 186--188  
**Preserved revision-80 author baseline:** `d05c5ed180fb0e0a9488700e30523dc336fef00a`  
**Preserved revision-80 paper tree:** `36fd73cb74917dcd1af315fd9696ac3026ff7bab`  
**Controlling external report:** `reviews/a2-dyn-v79-external-top4-review-2026-10-11/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `6764d25a4e3aaeb826d4ec24a12a55d16989d9e2` / `dd7a2e7ee91757cdb253eaf8e605cd330ca11e3f`  
**Final-SHA qualification runs:** response `38144140003`; referee-copy `38144150297`  
**Date:** 11 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, optical-geometry, geometric-measure-theory, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 81 should be assessed together with revision 80. Revision 80 was already an author response to the revision-79 report, revision 81 preserves its complete source as the immediate author baseline, and there is no intervening external report on the three revision-80 modules. I have therefore reviewed the six-module mathematical increment

- `core/183_homogeneous_incidence_localization.tex`;
- `core/184_singular_optical_transport.tex`;
- `core/185_common_coarea_and_remaining_boundary.tex`;
- `core/186_joint_endpoint_incidence_localization.tex`;
- `core/187_mixed_critical_volume_insertions.tex`;
- `core/188_uniform_critical_truncation_transport.tex`;

including the final revision-81 clarification which justifies stable-curve length estimates through bounded strong approximants to the physical peripheral vector.

The combined revision contains genuine and substantial new mathematics.

Revision 80 proves a physically capped, superlinear local estimate for a marked internal incidence. The cap permits positive layer-cake integration all the way to zero incidence, producing actual inverse-incidence insertions rather than a formal use of an unbounded multiplier. It then sums the depth-weighted internal optical source over all marked collision times and obtains a fixed-width complete-source bound. On the common exact-label coarea survivor graph, this pays optical loss and genuine grazing starting mass away from a positive initial endpoint-gradient cutoff. It also gives a correct first-exit representation for the remaining nongrazing surface source.

Revision 81 retains both endpoint momenta and one internal incidence in the same characteristic pairing. It obtains a common endpoint-width exponent

```text
alpha = 129/128
```

and incidence exponent

```text
beta = 17/16.
```

The resulting mixed local estimate has a physically capped finite-count remainder. Positive layer cake gives actual untruncated insertions with endpoint-gradient power below one half and a first inverse-gradient estimate with a fixed positive lower cutoff whose leading fixed-width bound is independent of that cutoff. On the physical coarea graph this improves the paid optical and genuine grazing starting-mass contribution from `C r/a` to `C r`; the same improvement pays the inverse-Jacobian compression cost in the nongrazing pullback.

I found no decisive counterexample, exponent reversal, lost exact label, altered occupation convention, illegal collision-dependent Fourier band, sign error in the layer-cake calculation, or hidden claim that a fixed-cutoff estimate permits the cutoff to pass through the collision limit. The manuscript is materially more careful than several earlier revisions about the difference between a particular small vector and a small multiplier, between volume and surface sources, and between fixed-cutoff uniformity and an untruncated theorem.

The negative recommendation is nevertheless unavoidable. The revised endpoint budget is

```text
E_M <= C_M B^(-1/192)
       + Ccrit_{epsilon(B),M}(a,r)
       + C F_M(a,r)
       + C r
       + C_Theta (1+epsilon(B)^(-1)) sqrt(r),
```

where `Ccrit` is the complete initial critical defect and `F_M` is the complete nongrazing outgoing first-exit flux height. Neither quantity is proved to tend to zero for legal outer choices `a(B), r(B)` made before the collision limit.

These are not decorative terms. The critical source is precisely where a fixed-width volume estimate need not control a moving pointwise roof peak. The outgoing term is a one-sided surface source; the new singular volume insertion theorem does not constitute a spectral or local estimate for that surface measure. The manuscript itself accurately keeps the following claims false:

- `complete_critical_initial_defect_height_decay_proved`;
- `complete_nongrazing_outgoing_flux_height_decay_proved`;
- `untruncated_first_inverse_gradient_concentration_proved`;
- `primary_referee_request_closed`;
- `full_raw_return_LLT_proved`;
- `pointwise_roof_density_LLT_proved`;
- `unrestricted_same_roof_pair_bridge_proved`; and
- `forward_essential_likelihood_convergence_proved`.

Thus revision 81 proves a stronger reduction and pays a formerly divergent transport cost. It still does not prove the organizing exact-label pointwise theorem stated in equation `eq:v76-target`.

At the requested benchmark, isolating the two final positive mechanisms and proving all other displayed costs finite or small is important progress. It is not a substitute for controlling those mechanisms.

## 2. Frozen source and chronology

Both reviewed author branches resolve to

`49957346c784071bf6f2e18a7ae6f2d724254f20`.

The repository tree is

`0919c3785e33a6a1c7b169f43db23ba88d6df511`.

The active paper directory is

`papers/A2-DYN-v81-referee-response`.

The controlling report is the revision-79 report at

`6764d25a4e3aaeb826d4ec24a12a55d16989d9e2`.

Revision 80 at

`d05c5ed180fb0e0a9488700e30523dc336fef00a`

is the immediate preserved author baseline. It adds modules 183--185. Revision 81 first adds modules 186--188 at

`fbc577cc79b1300d399f66ab4e72de0b1513b8e0`

and then adds the final fourteen-line clarification in module 186 at the reviewed SHA. That clarification is mathematically relevant: it no longer treats a merely `L-infinity` representative as having arbitrary stable-curve traces. Instead it passes the endpoint and homogeneous-incidence length estimates through uniformly bounded finite Cesaro approximants in the common strong space.

The source manifest records one hundred eighty-five inherited core modules and one hundred eighty-eight active modules. It states that the inherited cores, Python sources, appendices, bibliographies and provenance are byte-preserved, that the complete revision-80 article is assembled in the supplement, and that the journal plus supplement recorder union contains all one hundred eighty-eight cores.

The present review branch starts directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v81-external-top4-review-2026-10-11/`.

No author source, workflow, prior report, historical manuscript or unrelated repository path is intentionally modified.

## 3. Source qualification and its boundary

The final-SHA workflow runs attached to the two reviewed author refs are

- response branch run `38144140003`;
- referee-copy branch run `38144150297`.

At the time this report was frozen, both runs were still queued and the combined commit status was pending. I therefore do not count an unobserved future conclusion as successful qualification. Earlier runs on the pre-clarification revision-81 SHA were cancelled by the branch concurrency rule and are not substitutes for final-SHA evidence.

The repository also records local journal and supplement checks, but the validation protocol correctly states that only an actual successful final-SHA remote run qualifies the remote source. A later completed run may provide source, build, recorder and rendering evidence for the same author SHA; it would not alter the mathematical assessment below.

The intended workflow verifies

- the preserved revision-80 paper tree;
- the controlling revision-79 report blob;
- byte preservation of all inherited sources;
- normal and optimized finite-fixture agreement;
- native compilation of the journal and complete supplement;
- union coverage of all one hundred eighty-eight core modules;
- stabilized references and typesetting gates; and
- PDF geometry and selected rendering checks.

These checks are useful. They do not certify the anisotropic-space endpoint estimates, continued-peak normalization, mixed characteristic pairing, target-direction coarea covariance, first-exit surface source, or the two remaining endpoint heights.

## 4. Scope of this review

The supplement now contains one hundred eighty-eight modules and a long inherited pipeline. I have not attempted to re-prove every historical theorem. The substantive audit concerns:

1. the homogeneous grazing-strip weak estimate;
2. the peak interpolation and physically capped marked-incidence estimate;
3. positive layer cake for actual inverse-incidence insertions;
4. the complete depth-weighted internal optical source;
5. common exact-label coarea kernels and regular first-exit exhaustion;
6. the revision-80 nongrazing boundary reduction;
7. the strong norm of the specific two-sided endpoint indicator vector;
8. normalization of arbitrary continued rank-one peaks without division by `Pi 1`;
9. the two chronological cases in the joint endpoint/incidence pairing;
10. the mixed critical-volume layer cakes and their finite-count errors;
11. the cutoff-independent paid optical drift;
12. the revised endpoint budget and its remaining positive terms; and
13. exact source identity and workflow status.

The inherited four-record spectral theorem, moving-peak Gaussian expansion, Doeblin--Fortet inequalities, physical peripheral-vector theorem, reduced-action geometry, angular Jacobian estimate, complete-source fixed-width theorem, positive scalar remainder, path remainder and collision-to-return transfer are treated as source-pinned inputs. This report does not independently certify all of those chains.

## 5. Homogeneous incidence localization in revision 80

The operator convention is important. Densities are relative to the invariant collision probability, and for a real twist the physical power of the constant density has modulus one on every regular branch:

```text
|Q^j 1| = 1.
```

Consequently there is no additional cosine-density factor in the stable-curve estimate.

For the standard quadratic homogeneity strips, incidence is comparable to `k^(-2)` while the length of a homogeneous stable curve in the `k`th strip is `O(k^(-3))`. If the strip meets `{c<s}`, then `k` is at least a constant times `s^(-1/2)`, hence

```text
|M_s Q^j 1|_w <= C s^(3/2).
```

This is a real gain over the general piecewise-multiplier estimate. It is specific to the physical power and the geometry of a homogeneous strip; the manuscript does not promote it to a small strong multiplier norm.

The proof is structurally correct. A specialist should still verify that the homogeneity-strip and stable-graph conventions are exactly those of the pinned collision spaces and that threshold crossings at strip boundaries introduce no extra curve component. I found no missing word-count factor in the written estimate.

## 6. Peak interpolation and the revision-80 incidence theorem

On a fixed refined peak chart, revision 80 balances the strong contraction against the weak power estimate and obtains an interpolation close to the weak endpoint. Its original projected-incidence argument was written using `Pi 1`; revision 81 correctly recognizes that this vector can vanish at a nontrivial arithmetic peak and replaces it by a physical peripheral reference vector.

The revision-80 local theorem is

```text
m^2 P(exact labels, roof in J, c_j<s)
 <= C s^(5/4) (|J|+B_*^(-1))
    + C_{B_*}(1+B_*|J|) m^2 min(rho_{B_*}^{m/2},s^2).
```

The second bound in the minimum is the physical mass estimate

```text
nu{c<s} <= s^2.
```

This cap is essential. Without it, the spectral remainder could not be integrated against an inverse incidence near zero.

The theorem keeps the marked collision time, exact displacement and exact occupation coefficient. The auxiliary band is fixed before the collision limit. I found no illegal use of a collision-dependent band in this part of the argument.

## 7. Actual unbounded incidence insertions

Revision 80 applies the positive identity

```text
c^(-a) 1_{c<s}
 = s^(-a) 1_{c<s}
   + a integral_0^s v^(-a-1) 1_{c<v} dv.
```

The leading term is integrable for `a<5/4`. The capped remainder obeys

```text
s^(-a) min(D,s^2)
 + a integral_0^s v^(-a-1) min(D,v^2) dv
 <= C_a min(s^(2-a),D^(1-a/2)).
```

With `D=rho^{m/2}`, this gives an actual physical insertion, not multiplication by a claimed bounded operator `M_{c^{-a}}`.

For the depth-weighted source

```text
I_m = 1 + sum_{j=1}^{m-1} q_0^{d_j}/c_j,
```

the geometric weights have a uniformly bounded sum. Summing the marked estimates therefore gives a fixed-width collision-normalized bound for the complete internal optical source. The thin-incidence part gains a positive power of its threshold.

This is a genuine advance over revision 79, where the complement of the regular incidence corridor had been dominated by another unresolved pointwise source.

## 8. Common coarea versions and the first-exit source

Module 185 constructs jointly measurable roof kernels and an injective survivor graph, then records target-direction covariance in the form

```text
integral_{S_h(t)} f(Phi_h x) J_h(x) dmu_t(x)
 = integral_{Phi_h S_h(t)} f(y) dmu_{t+h}(y).
```

It also gives an explicit precompact flow-box exhaustion. Artificial Borel seams are used only for disjoint summation and are not treated as physical exits. At fixed collision count, the first-exit source is recovered by monotone exhaustion.

Within the written scope this is coherent. It is the correct kind of common-version statement needed to compare the target optical insertion with the original exact-label source without selecting incompatible density representatives on different words.

For a positive initial cutoff `|g|>=a`, revision 80 obtains

```text
optical loss + genuine grazing starting mass <= (C/a) integral_0^h u(t+s) ds.
```

For nongrazing exits it obtains

```text
exit defect + optical loss
 <= C outgoing_flux + (C/a) integral_0^h u(t+s) ds.
```

The outgoing term is retained with its first-exit selection and one-sided physical component. The inverse-Jacobian pullback cost is paid by the volume drift; it is not deleted from the boundary identity.

This distinction is correct and remains essential in revision 81.

## 9. The specific endpoint vector in revision 81

Let `P_b` denote multiplication by `1_{|p|<b}`. Revision 81 proves

```text
||P_b 1|| <= C b^(7/8),
|P_b 1|_w <= C b,
```

while retaining only boundedness, not smallness, for `P_b` on arbitrary strong vectors.

For the stable seminorm the estimate is

```text
min(|W|,b) |W|^(-1/8) <= C b^(7/8).
```

For two matched stable graphs at distance `d`, the symmetric-difference and Jacobian contribution is bounded by `C min(b,d)`. Division by `d^gamma` gives `C b^(1-gamma)`, which is better than the stable exponent for the chosen `gamma`. The weak estimate is the direct intersection-length bound.

This calculation is plausible and the vector/multiplier distinction is correctly stated. The load-bearing specialist check is whether the horizontal endpoint cuts, graph reparametrizations and little-Hölder test closures satisfy the exact matched-curve conventions of the inherited norm at every local parameter. The finite fixtures cannot establish that point.

## 10. Continued peak vectors and the final clarification

At a unit-modulus reference frequency, the inherited peripheral theorem provides a circle-valued physical eigenvector `u_*`. Revision 81 chooses a smooth weak test with nonzero pairing, uses weak continuity to keep `Pi_xi u_*` nonzero on a smaller chart, and normalizes by that pairing. This avoids dividing by `Pi_xi 1`, which may vanish.

The final reviewed commit adds the necessary trace clarification. The physical peripheral vector is obtained as a strong limit of uniformly bounded finite Cesaro sums of real twisted powers applied to a fixed smooth bounded vector. For a neighboring real parameter and a fixed power, those finite physical sums remain uniformly bounded in modulus. Endpoint and incidence intersection-length bounds are applied to the approximants, and boundedness on the common strong space permits passage to the weak limit. Only then is the balancing power chosen.

This is the correct direction of repair. It removes an unjustified direct trace assertion for an arbitrary `L-infinity` representative.

The point remains suitable for independent specialist verification. In particular one must check the common-space identification across nearby parameters, the strong convergence of the normalized Cesaro vectors, the order in which the continued projection and fixed power are applied, and uniform nonvanishing of the chosen test pairing on the finite chart cover. I found no direct contradiction in the revised text.

The resulting localized peak estimates are

```text
|P_b v_xi|_w <= C b^(63/64),
|M_s v_xi|_w <= C s^(47/32),
||M_s v_xi|| <= C.
```

## 11. The two chronological cases

The exact characteristic pairing for two endpoint strips and an incidence mark at time `j` is

```text
ell(P_b Q^(m-j) M_s Q^j P_b 1).
```

The occupation coefficient is the original forward coefficient in both cases.

If the terminal block is long, revision 81 combines

- the terminal peak-vector factor `b^(63/64)`;
- the initial strong factor `b^(7/8)` raised to `1/32`; and
- the incidence weak factor `s^(3/2)` raised to `31/32`.

The resulting leading amplitude is

```text
b^(259/256) s^(93/64).
```

If the initial block is long, the projected initial coefficient is `b^(255/256)`. The remaining terminal pairing has the two bounds

```text
C b^(1/8)
```

and

```text
C s^(1457/1024).
```

Geometric interpolation with powers `1/4` and `3/4` gives

```text
b^(1/32) s^(4371/4096),
```

and hence the complete second amplitude

```text
b^(263/256) s^(4371/4096).
```

Both cases imply the common exponents

```text
alpha = 129/128,
beta  = 17/16.
```

The complementary term carries an endpoint factor `b` and exponential decay. Independently, the physical pairing is at most `s^2`. After Gaussian integration and positive roof majorization, the theorem is

```text
m^2 P(exact labels, roof in J, D_b, c_j<s)
 <= C b^alpha s^beta (|J|+B_*^(-1))
    + C_{B_*}(1+B_*|J|)m^2 min(b rho_{B_*}^{m/2},s^2).
```

The printed exponent arithmetic is consistent. No number of physical words is introduced.

The decisive unverified inputs here are functional analytic: the fixed family of continued peak charts, the rank-one interpolation constants, the terminal pairing estimates, and the exact four-frequency local inversion. The paper treats those as inherited spectral theorems. Subject to those inputs, I found the two-case calculation coherent.

## 12. Mixed critical-volume layer cakes

The endpoint gradient is

```text
|g| = R sqrt(p_0^2+p_m^2).
```

Thus `{|g|<b}` is contained in a two-endpoint strip of comparable width. Inserting the positive layer cake for every internal `c_j^{-1}` into the joint theorem gives

```text
m^2 integral_J u^b(t) dt
 <= C b^alpha (|J|+B_*^(-1))
    + C_{B_*}(1+B_*|J|)m^2 b^(1/2) rho_{B_*}^{m/4}.
```

The exponent `beta>1` makes the leading incidence integral finite. Integrating the cap `min(b rho^{m/2},s^2)` against `s^{-2}` produces the stated square-root remainder. The depth weights are summable.

For `0<eta<1/2`, a second positive layer cake gives an actual untruncated source with insertion

```text
I_m |g|^(-eta).
```

Both the leading endpoint integral and the finite-count remainder are integrable in this range. For the first inverse power, the positive majorant over `a<=|g|<b` produces a leading bound `C b^(1/128)` independent of the fixed lower cutoff, while the finite-count error contains `a^(-1/2)`.

This distinction is correct. The manuscript does not pass `a` to zero before the collision limit. The statement

```text
limsup_m H(v^a) <= C
```

for every fixed `a>0`, with `C` independent of `a`, is not promoted to a theorem for the untruncated first inverse gradient.

## 13. Cutoff-independent paid optical drift

The optical derivative has the form

```text
|X omega| <= C omega I_m / |g|.
```

Revision 80 replaced `|g|^{-1}` by `a^{-1}` on the initial source `|g|>=a`. Revision 81 retains the inverse gradient in the target insertion. Common coarea covariance then yields

```text
O_h^{epsilon,a}(t) + E_h^{epsilon,gr,a}(t)
 <= C integral_0^h v^a(t+s) ds.
```

Averaging in `h` and using the fixed-width bound for `v^a` proves

```text
limsup_m sup_{R,n,k} m^2
 ||bar O_r^{epsilon,a}+bar E_r^{epsilon,gr,a}||_infinity
 <= C r,
```

with a constant independent of the previously fixed positive cutoff `a`.

For an initial annulus `a<=|g|<b`, the radial-speed upper bound keeps the transported gradient below

```text
b' = sqrt(b^2+2 Lambda r).
```

The truncated critical insertion gives the sharper annular bound

```text
C r (b')^(1/128).
```

The same insertion pays the pullback compression in the nongrazing boundary comparison. The revised endpoint budget therefore no longer requires `r/a` to tend to zero.

This is the central new result of revision 81. It is meaningful and appears internally consistent within the stated inherited inputs.

## 14. Why the pointwise theorem is still open

The final budget retains two complete positive heights.

### 14.1 The initial critical defect

The quantity `Ccrit_{epsilon,M}(a,r)` contains the true-exit and optical defects whose initial endpoint gradient satisfies `|g|<a`.

Revision 81 proves excellent fixed-width bounds for positive volume sources localized by `|g|<a`. It does not prove an essential roof-height bound for the initial critical defect after the collision-normalized supremum. A family can have uniformly small mass in every previously fixed roof interval and still concentrate in an interval whose center and width depend on the collision count. This is precisely the limit-order issue the manuscript correctly refuses to suppress.

The untruncated fractional Abel inequality is useful, but its kernel remains singular. A fixed-width bound for the fractional insertion does not by itself control the singular convolution at a collision-dependent roof peak.

### 14.2 The nongrazing outgoing flux

The quantity `F_M(a,r)` is a one-sided first-exit surface source. Revision 81 pays the inverse-Jacobian compression required to pull initial mass to that surface. It does not estimate the surface density itself.

A volume insertion theorem for `I_m/|g|` cannot be reinterpreted as a surface-current spectral theorem. The outgoing face includes section, competing-hit, itinerary and exact-event boundaries, with first-exit selection and backward lifetime. A new argument is required to show that its roof-height contribution vanishes uniformly in collision count and exact labels.

### 14.3 The first inverse-gradient limit

The first inverse-gradient estimate has a leading constant independent of every fixed lower cutoff, but its finite-count error grows like `a^{-1/2}`. This prevents the present proof from taking `a` to zero before the collision limit.

The full pointwise theorem might be closed without first proving a standalone untruncated `|g|^{-1}` theorem, but the current route does not supply the missing interchange.

### 14.4 Downstream consequences

The same-roof path numerator, actual-return clock transfer and forward essential likelihood remain conditional on scalar closure and on positivity of the arithmetic reference. Zero arithmetic classes are not normalized. This separation is correct.

## 15. Mathematical significance and presentation

The journal/supplement split is an improvement over earlier versions. The active journal is reported as twenty-seven pages and the full supplement as roughly five hundred eighty pages. The journal now identifies the exact physical event, arithmetic reference, analytic inputs, new transport mechanism and remaining error terms.

Nevertheless, at a top-four benchmark the central advertised theorem must be proved. The present article still states the exact-label pointwise limit as a governing assertion rather than a theorem. The strongest new results are highly technical estimates inside a very long source-pinned program, and their interpretation depends on numerous inherited operator, arithmetic, coarea and path statements which have not received an independent specialist audit.

Even if every scoped theorem in modules 183--188 is correct, the article remains a reduction with two unresolved positive mechanisms. It therefore does not yet have a complete principal theorem commensurate with its title and claimed endpoint.

The manuscript also remains unusually burdensome to verify. A serious resubmission should provide one compact dependency theorem which lists every inherited analytic assumption actually used by modules 183--188, and a specialist appendix proving the common-space and coarea interfaces in a form independent of the historical revision archive. Source preservation is valuable, but it is not a replacement for a conventional proof architecture.

## 16. Required changes before another top-four review

A new theorem-bearing revision should address the following points.

1. **Control the complete initial critical height.** Prove, with `a(B),r(B)` fixed before the collision limit, that the full critical contribution in the revised endpoint budget tends to zero. A fixed-width volume estimate or a formal fractional Abel representation is not sufficient.

2. **Control the complete nongrazing outgoing surface height.** Establish a surface-source local estimate retaining first-exit selection, exact labels, backward lifetime, physical one-sided components and the original section decisions. Do not infer this from the volume insertion theorem.

3. **Close the exact endpoint.** Insert the two new estimates into `eq:v81-endpoint-budget`, choose all outer scales explicitly, and prove `eq:v76-target` with the finite arithmetic reference and zero classes unchanged.

4. **Keep the cutoff order explicit.** Any use of cutoff-independent constants must preserve the order: choose outer Fourier and geometric scales, fix every positive cutoff, take the collision limit, enlarge auxiliary bands, and only then take the final outer limits.

5. **Audit the continued-peak localization.** An expert in anisotropic billiard spaces should verify the endpoint-vector strong norm, the bounded Cesaro approximants, the common-space parameter identification, the nonvanishing test normalization, and both chronological characteristic pairings.

6. **Audit the coarea and exit chain.** An expert should verify the common `(t,h)` kernels, target-direction Jacobian, optical normalization, negative-variation payment of genuine grazing mass, regular exhaustion and one-sided nongrazing surface measure.

7. **Obtain final-SHA qualification evidence.** The final author SHA should have observed successful runs on both response and copy refs. Source qualification will not prove the mathematics, but pending runs should not be described as successful evidence.

8. **Provide a conventional submission dependency map.** Separate the journal theorem, the indispensable technical supplement and the historical derivation archive. The active proof should not require a referee to reconstruct claim authority from many generations of status files.

9. **Obtain independent human specialist review.** The repository correctly records that no such review has occurred. It is now essential because the remaining argument combines delicate anisotropic traces, moving arithmetic peaks, singular positive insertions and one-sided coarea surface flux.

## 17. Final assessment

Revisions 80 and 81 make substantial progress.

They replace a corridor-restricted optical estimate by an all-incidence volume estimate, construct actual singular insertions with a physically capped remainder, retain both endpoint momenta in a joint local bound, produce untruncated fractional endpoint-gradient moments, and improve the paid optical drift from `C r/a` to `C r`. The final revision-81 patch also repairs a genuine trace-justification issue in the continued peak argument.

Within the scope audited, I found no decisive mathematical contradiction in these new statements.

The complete initial critical defect and the nongrazing outgoing surface height remain unproved. These are exactly the two terms which prevent the scalar pointwise local limit theorem and all unconditional downstream consequences.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
