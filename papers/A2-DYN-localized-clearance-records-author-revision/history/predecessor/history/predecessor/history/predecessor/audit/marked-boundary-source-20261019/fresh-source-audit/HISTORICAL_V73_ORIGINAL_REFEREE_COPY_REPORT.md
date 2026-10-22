# External top-four referee report on A2-DYN revision 73

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v73-referee-response-2026-10-11`, `revision/a2-dyn-v73-referee-copy-2026-10-11`  
**Reviewed commit:** `39575228f055862103edbebdd984bd6764fa0ad9`  
**Reviewed repository tree:** `73fba91196dffb2714685a55706545124aea3ba0`  
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

Revision 73 closes the first obligation. Its new threshold-mixture argument establishes that, for every fixed collision count, the complete original roof density belongs to `BV(R)`, uniformly in the radius, guard scale and attainable exact labels at that fixed count. The corresponding canonical derivative is therefore a genuine finite signed measure, with legitimate Jordan parts. This is not a theorem about a geometrically removed source, a selected word, an inserted finite-band measure, or an auxiliary allocated source. It is a theorem about the complete original physical source.

The revision also gives a useful structural sharpening of the second obligation. It proves an elementary but consequential two-sided averaging inequality which bounds the pointwise excess above a reserve-two local average by the minimum of an incoming positive current and an outgoing negative current near the same roof. It then defines the resulting collision-normalized paired-flux quantity and shows that a power bound for that quantity would close the scalar endpoint. Finally it proves that, within the inherited positive path-remainder theorem, the ordered scalar endpoint error and the bounded-Lipschitz path-numerator error are exactly equal. Thus no second independent numerator estimate is needed once the scalar endpoint is closed.

I audited the new modules

- `core/160_common_source_versions_and_interfaces.tex`;
- `core/161_full_source_bv_by_threshold_mixtures.tex`;
- `core/162_paired_flux_capacity_bound.tex`;
- `core/163_scalar_path_error_equivalence.tex`;

as well as the new front matter, response, proof ledger and source manifest. I found no decisive counterexample to the fixed-count `BV` theorem, no misuse of positivity in the signed threshold superposition, no sign error in the two-sided Jordan-mass inequality, and no hidden claim that finite variation alone gives the required endpoint decay.

The manuscript is commendably explicit about the remaining gap. The fixed-count bound has uncontrolled growth in the collision count. In particular its height factor is exponential and the number of o-minimal monotonicity cells has no stated growth estimate. More importantly, the manuscript does **not** prove the collision-uniform paired-flux decay

```text
P_epsilon(delta) <= A epsilon^{-q} delta^beta
```

or any alternative estimate implying that the normalized paired flux vanishes in the required order of limits. This is precisely the estimate which would convert the already proved averaged/inserted control into the actual pointwise density theorem.

Consequently the principal endpoint remains conditional. Revision 73 does not prove the unrestricted raw actual-return local limit theorem, the pointwise roof-density local theorem, the original positive endpoint denominator, the same-roof point-conditioned path theorem, or the forward essential-likelihood conclusion. It proves that all of these reduce to a sharper scalar cancellation problem on a now legitimate finite current.

At the requested benchmark, proving that the last obstruction is well-defined and identifying its correct two-sided form is important progress, but it is not a substitute for proving its decay. The central theorem advertised by the long-running raw-inversion programme remains open.

## 2. Frozen source, chronology and qualification

Both reviewed author branches resolve to

`39575228f055862103edbebdd984bd6764fa0ad9`.

The repository tree at that commit is

`73fba91196dffb2714685a55706545124aea3ba0`.

The active source directory is

`papers/A2-DYN-v73-referee-response`.

The source manifest identifies revision 72 at

`295800b658aa2ff3aada1707d5785ff757d60724`

as the exact author baseline and the revision-72 external report at

`fad5823b36f2c68595c6b17bebf62c70032d30a9`

as the controlling review. Every one of the 159 inherited core modules is retained byte-for-byte, as are the inherited Python sources, appendix and bibliography. Revision 73 adds exactly the four modules listed above.

The source manifest changes one inherited mathematical status in substance: existence of the complete full-source finite-measure current is now proved. It correctly leaves false the flags for collision-uniform current variation, paired-flux decay, the full raw return LLT, the pointwise roof-density LLT, unrestricted same-roof path conditioning, forward essential-likelihood convergence, independent human review and formal proof certification.

The exact-source qualification runs completed successfully on both reviewed branches:

- response branch run `38079689357`;
- referee-copy branch run `38079695588`.

These runs establish source identity, preservation of the frozen baseline, agreement of finite fixtures under ordinary and optimized execution, native TeX compilation, recorder coverage and rendered-page consistency. They do not certify the continuum threshold decomposition, constructible integration, uniform o-minimal cell count, coarea interfaces, Jordan-flux concentration, or the inherited spectral/path chain.

The present review branch starts directly from the reviewed author commit and adds only this report under

`reviews/a2-dyn-v73-external-top4-review-2026-10-11/`.

No manuscript source, author branch, prior report, workflow or unrelated repository path is intentionally modified.

## 3. Scope of this review

The article now contains 163 core modules and an extensive inherited proof pipeline. I have not attempted to re-certify every historical theorem. The substantive audit concerns:

1. the common disintegration kernel and interface ledger in module 160;
2. the threshold-mixture representation and fixed-count `BV` proof in module 161;
3. the paired directed-flux inequality and its use in the endpoint budget in module 162;
4. the scalar/path error comparison in module 163;
5. the relation of these results to the precise blockers in the revision-72 report;
6. the claims and nonclaims in the new abstract, leading theorem, response, proof ledger and source manifest; and
7. exact-source qualification and version identity.

The inherited density height bound, coarea current, finite-band insertion, positive remainder estimate, path-remainder theorem, cylinder inversion, tightness, arithmetic coefficients and collision-to-return clock transfer are treated as the source-pinned baseline claimed by the packet. This review does not convert that baseline into independent proof certification.

## 4. What revision 72 required

The revision-72 report accepted substantial finite-band and positive-source infrastructure but identified a basic mismatch between the object controlled and the object appearing in the desired endpoint theorem.

The manuscript had meaningful bounds for selected regular pieces, inserted sources, averaged roofs and positive remainders. It had also written a canonical distributional current for the complete source. It had not, however, proved that this complete current was a finite signed measure, and hence it had not justified taking its Jordan parts or applying total-variation arguments to it.

Even if finite variation were supplied, a second issue remained. An upper bound on total variation, or on the sum of all directed boundary masses, can charge an isolated physical entrance or exit atom even when a neighboring positive average already pays for the density height. Such a bound can therefore be too crude to prove the actual endpoint. The report requested a mechanism which distinguished an isolated edge from a genuinely narrow positive excursion.

Revision 73 addresses these two points in the correct order:

1. it first proves finite variation for the literal full source at each fixed collision count;
2. it then defines a paired incoming/outgoing flux on the Jordan parts of that full current; and
3. it states, without claiming proof, the collision-uniform power estimate which would close the endpoint.

This is a mathematically honest response. The remaining issue is no longer whether the relevant current exists. It is whether its oppositely directed masses can concentrate at the same microscopic roof with the required normalized rate.

## 5. Common roof versions and source identities

Module 160 begins by fixing the exact event, the physical roof and the original source measure. It disintegrates that source over the roof variable and obtains a single positive kernel

```text
D_t
```

such that every specified physical weight is evaluated on the same conditional source. This is a useful technical clarification. Pointwise source decompositions, domination by bounded marks and path pushforwards can otherwise be written using unrelated almost-everywhere versions, after which pointwise inequalities need not hold on a common set.

The construction is standard and appropriate. The collision source is standard Borel; its roof marginal already has a density; disintegration therefore gives a probability kernel on almost every fiber. Multiplying by the marginal density gives the finite kernel used in the text. Restricting to a finite or countable family of source identities avoids the invalid operation of taking an uncountable union of exceptional null sets.

The same point is handled correctly for path-valued kernels. A countable bounded-Lipschitz norming class is fixed before the common exceptional set is chosen. Across the radius parameter the manuscript takes

```text
sup_R esssup_t
```

rather than pretending that a single Lebesgue-null roof set works simultaneously for an uncountable parameter family.

The allocation formula involving the original regular and residual weights is also source-preserving. The coefficient is a Borel function of the physical roof and the original densities. The resulting two densities are obtained by multiplying the actual source weights on the unchanged trajectory space. No new conditioning event, transport map or path coupling is introduced.

I found this common-version ledger coherent. It should remain in the final manuscript because several later scalar and path comparisons depend on literal pointwise order relations rather than merely equality of equivalence classes.

## 6. The interface ledger

The second part of module 160 records how patchwise coarea currents are to be combined before taking Jordan decompositions.

This is the correct order. If two local charts describe the same physical source and the same roof on opposite sides of an artificial interface, their oriented normal fluxes cancel. A true jump of the source, an actual itinerary boundary, an exact-label boundary, or a physical endpoint is retained. A compactly supported window contributes both endpoint atoms in addition to its interior derivative.

The one-dimensional identity

```text
D(f 1_(a,b)) = (Df)|_(a,b) + f(a+) delta_a - f(b-) delta_b
```

is correctly used to prevent the historical error of counting one endpoint but not the other. The text also correctly refuses to infer total-variation convergence of arbitrary patch exhaustions merely from distributional convergence of the full current.

This interface ledger does not itself prove finite variation. Its role is to identify the canonical distributional derivative which module 161 later proves to be a finite measure. The separation of these tasks is sound.

## 7. Exact threshold representation of the smooth guard

The main new idea of module 161 is to avoid differentiating the full smooth guard word by word. Let the complete physical guard be a product of fixed smooth cutoff factors and let

```text
sigma = d Theta.
```

The manuscript writes each cutoff exactly as a threshold superposition and obtains

```text
1 - H^epsilon = integral W_y d sigma^{tensor N}(y).
```

For each threshold vector `y`, the source weight `W_y` is an indicator-valued union and is therefore nonnegative. Its pushforward roof density `b_y` is a positive restriction of the exact-label source. The original smooth-guard density is recovered by integration against the finite signed product measure.

This use of a signed threshold measure is legitimate. The proof does not multiply a signed weight by an order inequality. Positivity is used only for each threshold source before the signed superposition is taken. At the final variation estimate the total variation of the product measure is paid explicitly.

The manuscript does not require the fixed cutoff to be monotone. If it is monotone the threshold measure is positive and has total variation one; otherwise its total variation appears as

```text
V_Theta^(2m+1).
```

This factor is potentially large, but it is not hidden.

Finite signed Fubini is available because every threshold weight is bounded by one and the physical source is finite. The common kernel from module 160 supplies compatible Radon--Nikodym versions. I found no normalization error in this representation.

## 8. Uniform height of each threshold source

Each `b_y` is dominated by the complete exact-label density. The inherited finite-count height theorem therefore gives

```text
0 <= b_y <= L_m,
L_m = C A^m / c_*.
```

This is the correct type of input for the later monotonicity argument. It is a height bound for every positive threshold restriction, not a variation estimate for a symbolic word.

The exponential dependence on the collision count is fully visible. Revision 73 does not claim that `L_m` is harmless when the relevant collision count tends to infinity. This point is decisive when interpreting the final theorem.

## 9. Constructible integration and o-minimal monotonicity

The most delicate part of the fixed-count `BV` proof is the assertion that every threshold density has a representative with a uniformly finite number of monotonicity intervals, for a fixed collision count and uniformly in the continuous parameters.

The manuscript works on the finite collision graph of length `m`. Uniform finite horizon gives a finite candidate alphabet. In rational angular charts, collision, reflection, first-hit, positive-incidence, section, exact-label and threshold conditions are described by finite semialgebraic or globally subanalytic data. The cumulative distribution

```text
M(R, epsilon, y, t)
 = integral W_y 1_{L <= t} d mu
```

is then placed in the constructible class by a parameterized integration theorem. Constructible functions are definable in `R_an,exp`. The already proved height bound makes every roof section of `M` Lipschitz. Defining the finite derivative by a first-order formula therefore gives a definable representative `g`, equal almost everywhere to `b_y`.

For one-variable definable functions, the o-minimal monotonicity theorem gives a finite partition into intervals on which the function is continuous and monotone or constant, together with point cells. Uniform cell decomposition makes the number of cells independent of the continuous parameters appearing in the fixed formula. Taking a maximum over the finitely many exact labels and chart unions gives `J_m`.

At the level of the written argument, this is plausible and internally coherent. In particular, the text does not claim that the derivative of a constructible function is constructible; definability is enough. It also does not continue a collision branch through a singularity or replace the first-hit inequalities by a merely algebraic collision equation.

This step remains a major target for specialist verification. An independent audit should check:

- that the chosen auxiliary graph is globally subanalytic on every bounded chart after all first-hit and exact-label conditions are imposed;
- that the projection to the two initial collision coordinates is single-valued on the physical graph or is decomposed into genuinely disjoint physical pieces;
- that the integration theorem is applied to the exact density, including the section normalization and rational angular Jacobian;
- that every parameter entering the claimed uniform cell count occurs in one fixed definable family for the chosen collision count;
- that the passage from the Lipschitz cumulative distribution to the definable derivative representative preserves the claimed common height bound; and
- that no label or branch family whose complexity grows outside the fixed formula has been silently included.

I did not find a concrete contradiction in these points. The concern is verification burden, not an identified counterexample.

## 10. The fixed-count full-source `BV` theorem

Once the monotonicity lemma is accepted, the variation estimate follows cleanly. A monotone interval with values in `[0,L_m]` has variation at most `L_m`; the finitely many traces and point cells cost another fixed multiple. Thus

```text
||D b_y||_TV <= 4 (J_m+1) L_m.
```

Signed Fubini against the total variation of the threshold product measure gives

```text
||D b||_TV
 <= 4 (J_m+1) L_m V_Theta^(2m+1)
 =: C_m.
```

The distributional characterization of `BV` then identifies the canonical current with a finite signed measure. Compact support gives total mass zero.

This is the principal unconditional theorem of revision 73. It closes a real logical gap. The Jordan parts used in the next module now exist for the complete original source, not merely for finite patch currents or selected regular pieces.

The scope must nevertheless be stated exactly:

- the collision count is fixed;
- the constant `C_m` has no controlled growth as `m` tends to infinity;
- `L_m` is exponential;
- `J_m` has no quantitative bound;
- arbitrary bounded marked sources are not asserted to be `BV`;
- allocated subsources are not asserted to be `BV`; and
- total-variation convergence of patchwise currents is not asserted.

The manuscript states all of these limitations. They prevent the theorem from being used, by itself, in the asymptotic collision regime of the desired endpoint.

## 11. Why ordinary total variation is too crude

The revision correctly explains why an estimate on

```text
|D b|((t-delta,t+delta))
```

can be structurally wasteful. For an interval pulse, the incoming and outgoing boundary atoms are genuine physical jumps. A total-variation bound charges both even when the interval is wide enough that a one-sided local average already accounts for the height at every interior roof.

The desired pointwise endpoint estimate only needs to control a density value which exceeds a reserve of two times a symmetric local average. Such an excess can occur only if the density rises on the left and falls on the right within the same microscopic neighborhood. This motivates pairing positive incoming and negative outgoing Jordan masses instead of summing all directed masses.

This is a useful conceptual correction to the previous budget.

## 12. The two-sided averaging inequality

For a nonnegative compactly supported `BV` function, module 162 defines left and right local averages and proves

```text
[f(t) - 2 A_delta f(t)]_+
 <= min{
      (Df)^+([t-delta,t]),
      (Df)^-([t,t+delta])
    }.
```

The proof is elementary and correct outside the countable jump set of the usual representative. The increment formula shows that `f(t)-L_delta f(t)` is bounded above by the incoming positive variation and that `f(t)-R_delta f(t)` is bounded above by the outgoing negative variation. Since the unused average is nonnegative, the excess above the sum of the two averages is bounded by either discrepancy. Taking the minimum gives the result.

The same bound for every reserve `K>=2` follows by monotonicity of the positive part. The essential-supremum formulation makes exclusion of the jump set harmless.

The estimate does not cancel a physical atom. It says that an isolated edge need not be paid twice by a height budget. A narrow positive excursion, whose rise and fall both lie in the same neighborhood, remains charged. This is the appropriate qualitative distinction.

## 13. The paired-flux quantity

Using the now legitimate Jordan parts of the full current, the manuscript defines

```text
P_epsilon(delta)
 = limsup_m sup_{R,n,k} esssup_t
   m^2 min{
       (Db)^+([t-delta,t]),
       (Db)^-([t,t+delta])
   }.
```

This is a nonnegative extended quantity. It may be infinite. The interval masses are measurable in the roof variable. The definition is taken after fixing the guard scale and averaging width, in the same order of limits used by the inherited endpoint budget.

The theorem proves

```text
U_{epsilon,delta}(K)
 <= P_epsilon(delta)
 <= (1/2) V_epsilon(delta).
```

The left inequality is the two-sided averaging lemma. The right inequality is the elementary bound `min(x,y)<=(x+y)/2`.

Combining this with the inherited fixed-width averaged-height estimate gives

```text
E_M
 <= C_M B^(-1/192)
    + P_{epsilon(B)}(delta(B)),
```

with all choices made before the collision limit. No collision-dependent spectral band is inserted.

This reduction is useful, but it does not estimate the paired flux.

## 14. The decisive missing estimate

The manuscript states the sufficient premise

```text
P_epsilon(delta)
 <= A epsilon^(-q) delta^beta
```

for some fixed `q>=0` and `beta>0`. Choosing `delta` as a power of `epsilon` would then force the scalar endpoint error to zero.

No such estimate is proved.

The fixed-count `BV` theorem cannot supply it. Its constant depends uncontrollably on the collision count, whereas `P_epsilon(delta)` contains a collision limsup after multiplication by `m^2`. Even a collision-uniform total-variation bound would not automatically give the desired positive power of `delta`; a finite measure can concentrate arbitrarily near one roof. The paired estimate requires geometric or dynamical information about how incoming and outgoing physical flux can coexist near the same exact roof and labels.

The remaining problem is therefore genuinely quantitative. It is not a bookkeeping consequence of the existence of Jordan parts.

The author packet is transparent on this point. The source manifest leaves both collision-uniform variation and paired-flux decay false. The new leading theorem is conditional at precisely this premise. I agree with that boundary.

## 15. What kind of argument is still needed

A future revision must prove a collision-uniform concentration estimate for the actual full-source current. Several routes might be possible, but each would require new mathematics beyond the present fixed-count finiteness theorem. For example, one could seek:

1. a quantitative o-minimal complexity and transversality theorem giving explicit control of `J_m`, the roof derivative and the frequency of paired turns at scale `delta`;
2. a cancellation or nonconcentration theorem for incoming/outgoing coarea fluxes on the same exact-label fiber;
3. a transfer-operator estimate for a signed two-sided current observable which is stronger than the existing density height bound;
4. a geometric exclusion of narrow positive excursions at the normalized central scale; or
5. a direct pointwise inversion which bypasses paired flux while still retaining the literal full source.

Merely improving the fixed-count constant from one unspecified finite number to another will not suffice. The estimate must survive `m->infinity` in the exact order used by the target theorem.

## 16. Scalar and path-valued endpoint errors

Module 163 uses the inherited positive path-remainder theorem on the common disintegration kernel. Let `P` be the normalized scalar roof density, let the path-valued numerator be `mathbf P`, and let `G W_R` be the Gaussian reference measure. For each fixed finite band, the difference is decomposed into a positive path remainder and a small signed error.

The constant test one and positivity give the pointwise comparison

```text
|P-G|
 <= ||mathbf P - G W_R||_{BL*}
 <= |P-G| + 2 e_B.
```

The inherited theorem makes the collision-limsup of `e_B` tend to zero after the fixed-band collision limit and the subsequent band enlargement. Hence the ordered scalar and path errors are equal.

This is a useful theorem. It shows that the path numerator does not require a separate vanishing-height argument after the scalar endpoint has been established. The conclusion is in the bounded-Lipschitz dual norm, not total variation on path space.

It is equally important that the equality does not prove either error to be zero. Revision 73 states this correctly. The scalar endpoint remains the governing obstruction.

## 17. Positive arithmetic classes and normalization

On central targets where the Gaussian reference has a positive uniform floor, vanishing of the scalar error would imply:

- convergence of the scalar density ratio;
- bounded-Lipschitz convergence of the point-conditioned path law;
- convergence of the inverse ratio; and
- forward essential-likelihood convergence on normalized roof windows.

The manuscript does not assign conditional laws or ratios to zero arithmetic classes. It keeps the unnormalized comparison valid there and normalizes only on positive reference classes.

This distinction is correct. It should remain explicit in any later statement of the endpoint theorem.

## 18. Relation to the full raw-return theorem

Revision 73 advances the collision-roof endpoint pipeline, but it does not complete the full raw actual-return theorem.

The unproved scalar endpoint still sits before the final normalization and collision-to-return path transfer. Moreover, the article's historical raw-return programme contains its own exact-label, return-clock and pointwise roof requirements. The new fixed-count `BV` theorem and paired-flux reduction do not by themselves prove all of those downstream statements.

The source manifest correctly leaves false:

- `full_raw_return_LLT_proved`;
- `pointwise_roof_density_LLT_proved`;
- `unrestricted_same_roof_pair_bridge_proved`;
- `forward_essential_likelihood_convergence_proved`;
- `lorentz_collision_uniform_current_variation_proved`; and
- `lorentz_paired_flux_decay_proved`.

A top-four assessment must be based on the actual theorem-bearing endpoint, not on the number of intermediate modules. That endpoint remains conditional.

## 19. Significance at the requested benchmark

There is real mathematical value in the new threshold-mixture and paired-flux ideas.

The threshold representation converts a smooth product guard into positive semialgebraic threshold sources without changing the physical orbit. The constructible-integration step then gives fixed-count finite variation for a source whose direct symbolic differentiation would be unmanageable. The paired flux identifies a sharper object than total variation for recovering pointwise height from positive local averages. The scalar/path equality removes a duplicated downstream obstruction.

These ideas may be reusable beyond this exact manuscript. In their present form, however, they are not yet stated as a general theorem with independent applications. The fixed-count argument is embedded in a very specific triangular Lorentz source and depends on an extensive inherited graph, height and exact-label pipeline. The paired-flux theorem is an abstract `BV` inequality, while the hard Lorentz estimate for its normalized size remains open.

At *Annals*, *Acta*, *Inventiones* or *JAMS* level, the manuscript would need one of the following:

- completion of the actual pointwise raw-return theorem;
- a general quantitative theorem controlling paired physical flux for a broad class of singular hyperbolic systems, with multiple nontrivial applications; or
- another theorem of comparable scope which no longer depends on the unresolved endpoint.

Revision 73 has not yet reached any of these thresholds.

## 20. Architecture and exposition

The author packet is unusually careful about provenance and nonclaims. The new abstract and lead theorem clearly distinguish fixed-count finite variation, the paired-flux criterion and the remaining conditional endpoint. The proof ledger lists the exact new statements and false claims.

The article is nevertheless approximately five hundred pages and carries a long sequence of historical intermediate constructions. For external mathematical evaluation, this creates a serious burden: the four new modules depend on height, coarea, positive-remainder, finite-band and path theorems spread across the archive.

A future submission should provide a compact dependency theorem immediately before the new proof, with exact hypotheses and outputs sufficient to read modules 160--163 without reconstructing the entire revision history. This is not a request to delete the historical mathematics. It is a request to separate the theorem-bearing proof from provenance and exploratory ledgers.

There is also a metadata issue. The active directory retains some status and validation documents whose headings or content still describe revision 72. The new `SOURCE_MANIFEST.json` correctly declares itself authoritative, but active-path files named `PUBLICATION_STATUS.json`, `VALIDATION.md` or `JOURNAL_ROUTE.md` should not present stale revision identities. They should be updated for revision 73 or moved under `provenance/`. A top-level reader should not have to infer which status file is current.

## 21. Independent verification boundary

No independent human specialist audit is claimed, and none has been obtained in this review.

The highest-priority checks are:

1. the exact physical graph and first-hit semialgebraic description used in the threshold family;
2. applicability of the cited parameterized constructible-integration theorem to the full density and event;
3. the uniform o-minimal cell decomposition with the roof coordinate last;
4. the identification of the definable derivative with the physical roof density on common versions;
5. the inherited complete-density height bound for every positive threshold restriction;
6. the source-interface cancellations and endpoint atoms in the canonical current;
7. the inherited averaged-height and positive-remainder estimates used in module 162;
8. the collision-normalized order of limits in the definition of paired flux; and
9. the inherited path-remainder theorem used to deduce scalar/path equality.

The qualification scripts and finite fixtures can detect algebraic, sign, source-identity and typesetting regressions. They cannot establish these continuum statements.

## 22. Required changes before another top-four review

A further top-four submission should address the following items.

1. **Prove collision-uniform paired-flux decay.** Establish the stated power estimate, or another bound sufficient to make `P_{epsilon(B)}(delta(B))` vanish in the required order of limits.
2. **Close the actual scalar endpoint unconditionally.** State and prove the pointwise density theorem for the literal full source, including every exact label and arithmetic class in its proper unnormalized form.
3. **Propagate only after the scalar theorem is proved.** Then normalize positive classes and invoke the scalar/path equality and the inherited clock transfer to state the actual conditional path theorem.
4. **Give quantitative dependence on collision count where used.** Fixed-count existence constants are not enough for an asymptotic theorem with `m->infinity`.
5. **Obtain independent specialist audits.** At minimum, experts in dispersing billiards/coarea geometry and o-minimal integration should verify modules 160--162, while an expert in the inherited spectral/path chain should verify the input to module 163.
6. **Consolidate current metadata.** Active status, validation, route, source manifest, branch names and theorem claims should all identify revision 73 and the same commit.
7. **Provide a compact dependency layer.** Isolate the precise inherited hypotheses needed by the new proof from the historical archive.
8. **Preserve the present claim boundary.** Do not replace paired-flux decay by total mass, finite variation, patchwise variation, a finite-band insertion, or a fixed-count constant.

## 23. Final assessment

Revision 73 makes a genuine advance. It proves, for the first time in the current pipeline, that the complete original exact-label roof current is a finite signed measure at every fixed collision count. It does so by an exact threshold superposition of positive physical sources and an o-minimal monotonicity argument, rather than by deleting singular pieces or differentiating a proliferating symbolic partition. It also identifies paired incoming/outgoing flux as the correct sharper obstruction and proves that the scalar and path endpoint errors coincide.

I found no decisive error in the four new modules on the scope audited here. Subject to specialist verification, the fixed-count `BV` theorem is credible and should be regarded as closing one of the two principal revision-72 gaps.

The second and decisive gap remains. No collision-uniform decay estimate for the paired physical flux is proved. Therefore the actual pointwise scalar endpoint, its denominator, the same-roof conditioned path theorem, the forward likelihood and the full raw actual-return LLT remain conditional.

This is not a minor technical remainder. It is the quantitative statement which distinguishes the actual full-source endpoint from the inserted, averaged and finite-count objects already controlled.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**

The work may already contain publishable components after independent audit and substantial reorganization, notably the fixed-count full-source `BV` theorem and the abstract paired-flux reduction. A positive top-four recommendation, however, requires closure of the collision-uniform paired-flux problem or a comparably broad theorem which makes that endpoint no longer central.