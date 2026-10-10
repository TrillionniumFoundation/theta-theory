# External top-four referee report on A2-DYN revision 73

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v73-referee-response-2026-10-11`, `revision/a2-dyn-v73-referee-copy-2026-10-11`  
**Reviewed commit:** `39575228f055862103edbebdd984bd6764fa0ad9`  
**Reviewed repository tree:** `73fba4f71220b8582b21bdabf06a80920adbadaa`  
**Active manuscript directory:** `papers/A2-DYN-v73-referee-response`  
**Active mathematical source:** one hundred sixty-three numbered core modules; revision 73 adds modules 160--163  
**Frozen revision-72 author baseline:** `295800b658aa2ff3aada1707d5785ff757d60724`  
**Frozen revision-72 paper tree:** `bd761b97e603b666ed97b27241f9ab83c7f2550b`  
**Controlling report:** `reviews/a2-dyn-v72-external-top4-review-2026-10-11/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `fad5823b36f2c68595c6b17bebf62c70032d30a9` / `f10920ea44a658b3b0ab75eac1f1d910a0946417`  
**Date:** 11 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, or o-minimality audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 73 is a genuine theorem-bearing revision and a meaningful response to the revision-72 report. The previous report separated two obligations which had repeatedly been conflated in the historical pipeline:

1. prove that the literal, unremoved, exact-label physical source has a well-defined finite distributional current at each collision count; and
2. prove a collision-uniform quantitative cancellation estimate strong enough to pass from finite-band or averaged control to the actual pointwise endpoint.

Revision 73 closes the first obligation. Its threshold-mixture argument establishes that, for every fixed collision count, the complete original roof density belongs to `BV(R)`, uniformly in the radius, guard scale and attainable exact labels at that fixed count. The canonical derivative is therefore a genuine finite signed measure with legitimate Jordan parts. This is a theorem about the complete original physical source, not a removed source, selected word, inserted finite-band measure, or auxiliary allocated source.

The revision also sharpens the second obligation. It proves a two-sided averaging inequality which bounds the pointwise excess above a reserve-two local average by the minimum of an incoming positive current and an outgoing negative current near the same roof. It then defines the corresponding collision-normalized paired-flux quantity and shows that a power estimate for that quantity would close the scalar endpoint. Finally, within the inherited positive path-remainder theorem, it proves equality of the ordered scalar endpoint error and the bounded-Lipschitz path-numerator error.

I audited the new modules

- `core/160_common_source_versions_and_interfaces.tex`;
- `core/161_full_source_bv_by_threshold_mixtures.tex`;
- `core/162_paired_flux_capacity_bound.tex`;
- `core/163_scalar_path_error_equivalence.tex`;

as well as the revised front matter, response, proof ledger and source manifest. I found no decisive counterexample to the fixed-count `BV` theorem, no misuse of positivity in the signed threshold superposition, no sign error in the two-sided Jordan-mass inequality, and no hidden claim that finite variation alone supplies endpoint decay.

The manuscript is explicit about the remaining gap. The fixed-count bound has uncontrolled growth in the collision count. Its height factor is exponential and the o-minimal monotonicity number has no stated growth estimate. More importantly, the manuscript does not prove the collision-uniform paired-flux estimate

```text
P_epsilon(delta) <= A epsilon^{-q} delta^beta
```

or any alternative estimate making the normalized paired flux vanish in the required order of limits.

That missing estimate is precisely what would convert the already proved averaged and inserted control into the actual pointwise density theorem. Consequently revision 73 does not prove the unrestricted raw actual-return local limit theorem, the pointwise roof-density theorem, the positive endpoint denominator, the same-roof point-conditioned path theorem, or the forward essential-likelihood conclusion.

At the requested benchmark, proving that the final obstruction is a well-defined finite current and identifying its correct paired form is important progress. It is not a substitute for proving the obstruction small.

## 2. Frozen source and qualification

Both reviewed author branches resolve to

`39575228f055862103edbebdd984bd6764fa0ad9`.

The Git tree at that commit is

`73fba4f71220b8582b21bdabf06a80920adbadaa`.

The active source directory is

`papers/A2-DYN-v73-referee-response`.

The source manifest identifies revision 72 at

`295800b658aa2ff3aada1707d5785ff757d60724`

as the frozen author baseline and the revision-72 report at

`fad5823b36f2c68595c6b17bebf62c70032d30a9`

as the controlling review. All 159 inherited core modules are retained byte-for-byte, together with the inherited Python sources, appendices and bibliography. Revision 73 adds exactly the four modules listed above.

The source manifest correctly changes one central inherited status: existence of the complete full-source finite-measure current is now proved. It leaves false the flags for collision-uniform current variation, paired-flux decay, the full raw return LLT, the pointwise roof-density LLT, unrestricted same-roof path conditioning, forward essential-likelihood convergence, independent human review and formal proof certification.

The exact-source qualification runs completed successfully on both reviewed branches:

- response branch run `38079689357`;
- referee-copy branch run `38079695588`.

These runs establish source identity, preservation of the frozen baseline, finite-fixture consistency, native TeX compilation and rendered-page checks. They do not certify constructible integration, o-minimal cell decomposition, coarea interfaces, Jordan-flux concentration or the inherited spectral/path chain.

The present review branch starts at the reviewed author commit and adds this report only under

`reviews/a2-dyn-v73-external-top4-review-2026-10-11/`.

## 3. Scope of this review

The manuscript now contains 163 core modules and an extensive inherited pipeline. I have not attempted to re-certify every historical theorem. The substantive audit concerns:

1. the common disintegration kernel and interface ledger in module 160;
2. the threshold-mixture representation and fixed-count `BV` proof in module 161;
3. the paired directed-flux inequality and endpoint budget in module 162;
4. the scalar/path error comparison in module 163;
5. the relationship between these results and the revision-72 blockers; and
6. source identity and qualification evidence.

The inherited density-height bound, coarea current, finite-band insertion, positive remainder estimate, path-remainder theorem, cylinder inversion, arithmetic coefficients and collision-to-return transfer are treated as the source-pinned baseline claimed by the packet. This report does not independently certify them.

## 4. Common roof versions

Module 160 fixes the exact event, roof and original source measure, then disintegrates that source over the roof variable to obtain one positive finite kernel `D_t`. Every specified physical weight is evaluated on this same kernel.

This is a useful correction. Pointwise source decompositions and path inequalities can otherwise be written using unrelated almost-everywhere versions. The manuscript restricts to a finite or countable family of identities before fixing the exceptional set and therefore avoids an uncountable union of null sets.

For path-valued kernels it fixes a countable bounded-Lipschitz norming class. Across the radius parameter it takes `sup_R esssup_t`, rather than assuming one null roof set works for every radius.

The allocation formula is also source-preserving. Its coefficient is a Borel function of the physical roof and original densities, and the replacement is performed by multiplying actual source weights on the unchanged trajectory space. No new conditioning event or transport map is introduced.

I found this common-version construction coherent.

## 5. The interface ledger

Module 160 also records how patchwise coarea currents are combined before Jordan decomposition.

Artificial chart interfaces cancel when the physical roof and source agree on both sides. True source jumps, itinerary boundaries, exact-label boundaries and physical endpoints remain. For a compactly supported window the derivative includes both endpoint atoms:

```text
D(f 1_(a,b)) = (Df)|_(a,b) + f(a+) delta_a - f(b-) delta_b.
```

The text correctly refuses to infer total-variation convergence of arbitrary patch exhaustions from distributional convergence alone. The ledger identifies the canonical current later proved finite in module 161; it does not itself assume that finiteness.

## 6. Exact threshold representation

The principal new device in module 161 is an exact threshold superposition of the smooth product guard. With `sigma=d Theta`, each cutoff is represented by threshold indicators, giving

```text
1-H^epsilon = integral W_y d sigma^{tensor N}(y).
```

For each threshold vector, `W_y` is nonnegative and indicator-valued. Its roof density `b_y` is a positive restriction of the exact-label source. The original smooth-guard density is recovered by integration against the finite signed product measure.

This use of a signed threshold measure is legitimate. Positivity is invoked only for each threshold source before the signed superposition. The total variation of the product measure is paid explicitly at the final variation estimate.

The argument does not require the fixed cutoff to be monotone. If it is nonmonotone, the factor `V_Theta^(2m+1)` remains visible. Finite signed Fubini is available because every threshold weight is bounded by one and the physical source is finite.

I found no normalization or sign error in this representation.

## 7. Height of threshold sources

Each `b_y` is dominated by the complete exact-label density. The inherited finite-count height theorem yields

```text
0 <= b_y <= L_m,
L_m = C A^m / c_*.
```

This is a height estimate for every positive threshold restriction, not a variation estimate for a symbolic word. Its exponential dependence on the collision count is explicit and later becomes one reason the fixed-count theorem is insufficient for the asymptotic endpoint.

## 8. Constructible integration and monotonicity

The delicate step is the assertion that, for each fixed collision count, every threshold density has a representative with a uniformly finite number of monotonicity intervals over all continuous parameters and attainable exact labels.

The manuscript works on the finite physical collision graph. Uniform finite horizon gives a finite candidate alphabet. In rational angular charts, collision, reflection, first-hit, positive-incidence, section, exact-label and threshold conditions are encoded by finite semialgebraic or globally subanalytic data. The cumulative distribution

```text
M(R,epsilon,y,t)
 = integral W_y 1_{L<=t} d mu
```

is placed in the constructible class by parameterized integration. Constructible functions are definable in `R_an,exp`. The height bound makes each roof section Lipschitz. Defining its finite derivative by quantified inequalities gives a definable representative equal almost everywhere to `b_y`.

O-minimal cell decomposition and one-variable monotonicity then give a finite number `J_m` of monotonicity intervals and point cells for the fixed formula at collision count `m`. The number is uniform in the continuous parameters and finite exact-label set at that count. No growth bound in `m` is claimed.

At the level of the written proof this is plausible and internally coherent. It remains a major target for independent verification. A specialist should check:

- the exact globally subanalytic description of the physical first-hit graph;
- disjointness or multiplicity control of the projection to initial coordinates;
- inclusion of the section normalization and chart Jacobian in the integration theorem;
- uniformity of the definable family in all displayed parameters;
- identification of the definable derivative with the physical density on common versions; and
- the absence of hidden branch families outside the fixed formula.

I found no concrete contradiction in these points.

## 9. Fixed-count full-source BV

Given the monotonicity lemma, every threshold density has variation bounded by a fixed multiple of `(J_m+1)L_m`. Signed Fubini against the total variation of the threshold product measure gives

```text
||Db||_TV
 <= 4 (J_m+1) L_m V_Theta^(2m+1)
 = C_m.
```

The distributional characterization of `BV` identifies the canonical current with a finite signed measure. Compact support gives total mass zero.

This is the main unconditional theorem of revision 73. It closes a real logical gap: the Jordan parts used later now exist for the complete original source.

Its scope is exact and limited:

- the collision count is fixed;
- `C_m` has uncontrolled growth;
- `L_m` is exponential;
- `J_m` has no quantitative bound;
- arbitrary bounded marked or allocated sources are not asserted `BV`; and
- patch currents are not asserted to converge in total variation.

The manuscript states these limitations correctly.

## 10. Why total variation is not enough

A total-variation estimate can charge an isolated physical entrance or exit atom even when the neighboring positive average already accounts for the density height. It can therefore be too crude for the actual pointwise endpoint.

The endpoint error only requires control of a value which exceeds a reserve of two times a symmetric local average. Such an excess requires both a rise on the left and a fall on the right within the same neighborhood. This motivates pairing incoming positive and outgoing negative current rather than summing all directed current masses.

This is a useful conceptual sharpening.

## 11. The paired-flux inequality

For a nonnegative compactly supported `BV` function, module 162 proves

```text
[f(t)-2 A_delta f(t)]_+
 <= min{
      (Df)^+([t-delta,t]),
      (Df)^-([t,t+delta])
    }
```

for almost every roof.

The proof is correct. The increment formula bounds `f-L_delta f` by incoming positive variation and `f-R_delta f` by outgoing negative variation. Because the unused average is nonnegative, the excess above the sum of the two averages is bounded by either discrepancy. The same estimate for every reserve `K>=2` follows immediately.

The inequality does not erase physical atoms. It avoids paying an isolated edge twice and still charges a narrow positive excursion whose rise and fall lie in the same microscopic neighborhood.

## 12. Collision-normalized paired flux

The manuscript defines

```text
P_epsilon(delta)
 = limsup_m sup_{R,n,k} esssup_t
   m^2 min{
      (Db)^+([t-delta,t]),
      (Db)^-([t,t+delta])
   }.
```

The quantity is nonnegative and may be infinite. Its definition becomes legitimate only after module 161 proves that the full current has finite Jordan parts for every fixed count.

The theorem gives

```text
U_{epsilon,delta}(K)
 <= P_epsilon(delta)
 <= (1/2) V_epsilon(delta)
```

and, after combining it with the inherited averaged-height estimate,

```text
E_M
 <= C_M B^(-1/192)
    + P_{epsilon(B)}(delta(B)).
```

All widths and bands are fixed before the collision limit. No count-dependent spectral band is used.

This is a clean reduction. It is not a decay theorem.

## 13. The decisive missing estimate

The sufficient premise is

```text
P_epsilon(delta)
 <= A epsilon^(-q) delta^beta
```

for fixed `q>=0` and `beta>0`. Choosing `delta` as a power of `epsilon` would then close the scalar endpoint.

No such estimate is proved.

The fixed-count `BV` theorem cannot imply it. Its constant has uncontrolled collision-count growth, while the paired quantity contains a collision limsup after multiplication by `m^2`. Moreover, even a collision-uniform total-variation bound would not automatically imply a positive power of `delta`; finite measures can concentrate on arbitrarily small intervals.

The remaining problem is therefore genuinely quantitative: control of simultaneous incoming and outgoing physical flux near the same exact roof and labels.

This is the decisive reason for the negative recommendation.

## 14. Scalar and path errors

Module 163 uses the inherited positive path-remainder theorem on the common kernel. Positivity and the constant test one give

```text
|P-G|
 <= ||mathbf P-G W_R||_{BL*}
 <= |P-G| + 2 e_B.
```

The inherited theorem makes the collision-limsup of `e_B` vanish after the fixed-band collision limit and subsequent band enlargement. Hence the ordered scalar and bounded-Lipschitz path-numerator errors are equal.

This result is useful: a separate path-numerator height estimate is unnecessary once the scalar endpoint is proved. The result is in bounded-Lipschitz dual norm, not total variation on path space.

It does not prove either error zero. The scalar endpoint remains the governing obstruction.

## 15. Normalization and positive classes

On central targets with a positive Gaussian floor, scalar endpoint convergence would imply density-ratio convergence, bounded-Lipschitz convergence of the point-conditioned path law and forward essential-likelihood convergence on normalized roof windows.

The manuscript does not assign ratios or conditional laws to zero arithmetic classes. It keeps the unnormalized comparison there and normalizes only on positive reference classes. This distinction is correct.

## 16. Relation to the raw-return theorem

Revision 73 advances the endpoint pipeline but does not complete the raw actual-return theorem. The source manifest correctly leaves false:

- `full_raw_return_LLT_proved`;
- `pointwise_roof_density_LLT_proved`;
- `unrestricted_same_roof_pair_bridge_proved`;
- `forward_essential_likelihood_convergence_proved`;
- `lorentz_collision_uniform_current_variation_proved`; and
- `lorentz_paired_flux_decay_proved`.

The number of intermediate modules cannot substitute for the theorem-bearing endpoint. That endpoint remains conditional.

## 17. Significance at the requested benchmark

The threshold-mixture and paired-flux ideas have mathematical value. The first converts a smooth product guard into positive semialgebraic threshold sources without changing the physical orbit. The second identifies a sharper endpoint obstruction than total variation. The scalar/path equality removes duplicated downstream work.

In the present manuscript, however, the fixed-count theorem is tied to a specific triangular Lorentz source and a large inherited graph, height and exact-label pipeline. The hard collision-uniform Lorentz estimate remains open.

At *Annals*, *Acta*, *Inventiones* or *JAMS* level, the work would need at least one of the following:

- completion of the actual pointwise raw-return theorem;
- a general quantitative paired-flux theorem for a broad class of singular hyperbolic systems with independent applications; or
- another theorem of comparable scope which no longer depends on the unresolved endpoint.

Revision 73 does not yet meet that standard.

## 18. Architecture and metadata

The packet is careful about provenance and nonclaims. The new lead theorems distinguish fixed-count finite variation, the paired-flux criterion and the conditional endpoint.

The article is nevertheless approximately five hundred pages and depends on a long historical chain. A future submission should insert a compact dependency theorem immediately before modules 160--163, listing only the inherited hypotheses needed by the new proof. Historical material can remain in provenance or a companion archive.

Some active-path status and validation files still describe revision 72. The new `SOURCE_MANIFEST.json` declares itself authoritative, but files named `PUBLICATION_STATUS.json`, `VALIDATION.md` or `JOURNAL_ROUTE.md` should not carry stale revision identities in the active revision-73 directory. They should be updated or moved under `provenance/`.

## 19. Independent verification boundary

No independent human specialist audit is claimed. The highest-priority checks are:

1. the physical first-hit graph and threshold family;
2. applicability of parameterized constructible integration;
3. the uniform o-minimal monotonicity partition;
4. identification of the derivative representative with the roof density;
5. the inherited complete-density height bound for every threshold source;
6. source-interface cancellations and endpoint atoms;
7. the averaged-height and positive-remainder estimates used in module 162;
8. the collision-normalized order of limits in paired flux; and
9. the inherited path-remainder theorem used in module 163.

Source hashes, finite fixtures and native compilation do not certify these continuum statements.

## 20. Required changes before another top-four review

1. **Prove collision-uniform paired-flux decay.** Establish the stated power estimate or another bound sufficient to make `P_{epsilon(B)}(delta(B))` vanish in the required order of limits.
2. **Close the actual scalar endpoint unconditionally.** Prove the pointwise density theorem for the literal full source and exact labels.
3. **Propagate only after scalar closure.** Then normalize positive classes and invoke scalar/path equality and the inherited clock transfer.
4. **Give quantitative collision-count dependence where used.** Fixed-count existence constants do not suffice for `m->infinity`.
5. **Obtain independent specialist audits.** The threshold/o-minimal proof and the coarea/paired-flux chain require expert review.
6. **Consolidate metadata.** Active status, validation, route, manifest and branch identities should all describe revision 73.
7. **Provide a compact dependency layer.** Separate theorem-bearing inputs from the historical archive.
8. **Preserve the present claim boundary.** Do not replace paired-flux decay by total mass, finite variation, patch variation or finite-band insertion.

## 21. Final assessment

Revision 73 proves, for the first time in the current pipeline, that the complete original exact-label roof current is a finite signed measure at every fixed collision count. It does so through an exact threshold superposition and an o-minimal monotonicity argument, without deleting singular pieces or replacing the original source. It also identifies paired incoming/outgoing flux as the sharper obstruction and proves equality of scalar and path endpoint errors.

I found no decisive error in the four new modules within the scope audited here. Subject to specialist verification, the fixed-count `BV` theorem is credible and closes one of the two principal revision-72 gaps.

The second and decisive gap remains. No collision-uniform decay estimate for the paired physical flux is proved. Therefore the actual pointwise scalar endpoint, its denominator, same-roof conditioned path theorem, forward likelihood and full raw actual-return LLT remain conditional.

This is not a minor remainder. It is the quantitative statement distinguishing the actual full-source endpoint from the inserted, averaged and fixed-count objects already controlled.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**

The fixed-count full-source `BV` theorem and abstract paired-flux reduction may already be publishable components after independent audit and substantial reorganization. A positive top-four recommendation requires closure of the collision-uniform paired-flux problem or a comparably broad theorem which makes that endpoint no longer central.