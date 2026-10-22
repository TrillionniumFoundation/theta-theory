# External top-four referee report on A2-DYN revision 97

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v97-referee-response-2026-10-13`, `revision/a2-dyn-v97-referee-copy-2026-10-13`  
**Reviewed author commit:** `6dd3149985ff5f6aca9dce9e2c186589df309872`  
**Reviewed repository tree:** `908dd6b0e2a82a018986aad9f3ced8ea90cbaaac`  
**Active manuscript directory:** `papers/A2-DYN-v97-referee-response`  
**Canonical revision identity:** `a2-dyn-v97-quantitative-failure-source-reduction-2026-10-13`  
**Active mathematical source:** 234 numbered core modules; revision 97 adds modules 232--234  
**Immediate author baseline:** revision 96 at `4b3ea4f4ce112338654279797cd4ce380842b4af`  
**Frozen revision-96 paper tree:** `4490eb342ee9b446136b3b1940dad03e9cb43ff6`  
**Controlling external report:** `reviews/a2-dyn-v96-external-top4-review-2026-10-13/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `c08d8186293dc55a7705945ca917596ff6eb859d` / `36185f23a7221f59e88706531908f0244806ead3`  
**Exact-SHA qualification runs:** response `38292053081`; referee-copy `38292061194`; both completed successfully  
**Date:** 13 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, probability, o-minimal-geometry, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 97 is a substantial and mathematically focused response to the revision-96 report. It does not merely rename the three continuation-failure mechanisms isolated in revision 96. Its new contribution is to place the old failure source into a quantitative decomposition

```text
old failure source
  = recovered high-clock part
  + recovered protected low-clock part
  + residual near-entrance/short-residence part,
```

and to prove that the first two parts have vanishing normalized essential height along an explicit legal outer schedule. The residual is supported on a geometrically precise restriction of the original source.

More specifically, modules 232--234 establish, conditional on the inherited interfaces:

1. uniform exclusion of the artificial momentum caps on every sufficiently short comparison orbit;
2. a capped same-label occupation clock and a target-value anchor for histories carrying a definite amount of that clock;
3. a lower clock bound for the old positive-occupation admission mechanism;
4. an essential-height bound for the high-clock portion of the old failure source;
5. a running density-compression estimate on protected same-event intervals;
6. containment of protected low-clock histories in the running-compression source;
7. an exact three-way decomposition of the revision-96 failure source;
8. localization of the residual to near-entrance critical targets or genuinely short physical segments;
9. an explicit outer choice of `epsilon`, `q`, `r`, and `a` for which the recovered failure source tends to zero in essential height; and
10. a scalar upper reduction in which the only remaining pointwise obstruction is the essential height of the residual source.

I found no decisive error in the collar arithmetic, capped-clock anchor, protected compression argument, support calculation, exponent bookkeeping, or stated order of limits in modules 232--234. I also found no hidden collision-dependent component count, no use of a cutoff depending on the collision index, no promotion of a small integral mass to a small essential height, and no assertion that the residual has already vanished.

The recommendation nevertheless remains negative because the governing pointwise theorem is still not proved. Revision 97 proves that the recovered part of the old continuation-failure source is negligible. It proves only an integrated small-mass statement for the residual

```text
Y_{a,q,r},
```

not the normalized essential-height estimate required at the original pointwise topology. The residual may occupy a roof set of vanishing measure while retaining fixed or increasing height. That possibility is exactly what the upper pointwise endpoint must exclude.

Consequently revision 97 still does not prove:

- vanishing of the residual source in normalized essential height;
- vanishing of the complete signed projected upper forcing;
- unconditional upper-spike persistence;
- zero essential-height charge for the original near-critical or short-residence source;
- the upper pointwise half of the exact-label raw local limit theorem;
- the unrestricted pointwise exact-label raw local limit theorem; or
- the downstream unrestricted point-conditioned kernel and essential-likelihood laws.

At the requested benchmark, the exact reduction to a single residual source is important, but a paper organized around unrestricted pointwise raw inversion must prove the residual-height theorem, not only identify its support and show its mass tends to zero.

## 2. Frozen source, chronology, and source identity

Both reviewed author refs resolve to

`6dd3149985ff5f6aca9dce9e2c186589df309872`,

with repository tree

`908dd6b0e2a82a018986aad9f3ced8ea90cbaaac`.

The active manuscript packet is

`papers/A2-DYN-v97-referee-response`.

The source manifest pins revision 96 as the immediate author baseline at

`4b3ea4f4ce112338654279797cd4ce380842b4af`,

with frozen paper tree

`4490eb342ee9b446136b3b1940dad03e9cb43ff6`.

The controlling revision-96 external report is frozen at

`c08d8186293dc55a7705945ca917596ff6eb859d`,

with report blob

`36185f23a7221f59e88706531908f0244806ead3`.

Revision 97 preserves 231 inherited core modules and adds exactly:

- `core/232_capped_coarea_occupation.tex`;
- `core/233_running_compression_height.tex`;
- `core/234_quantitative_failure_source_reduction.tex`.

The complete revision-96 article and source packet remain frozen through the declared provenance structure. No historical theorem is silently replaced by a revised statement, and the distinct preserved revision-88 variants remain separate.

The present review branch starts from the exact reviewed author commit and adds only this report under

`reviews/a2-dyn-v97-external-top4-review-2026-10-13/`.

No author manuscript source, author revision branch, workflow, earlier report, preserved source variant, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The revision-97 exact-source workflow is

`.github/workflows/a2-dyn-v97-qualification.yml`.

At the reviewed author SHA, the two author refs have completed successful runs:

- response branch: `38292053081`;
- referee-copy branch: `38292061194`.

The workflow contract checks, among other things:

- the frozen revision-96 paper tree and complete revision-96 snapshot;
- the controlling revision-96 report blob;
- both preserved revision-88 variants;
- byte and executable-mode preservation for inherited nonreplaced files;
- the overlay hashes for all new sources;
- agreement of ordinary and optimized finite diagnostics;
- native compilation of the focused article and full archive;
- recorder coverage of the three new journal modules and all 231 inherited supplement modules, with union 234;
- stabilized references and warning gates; and
- PDF word boxes and rendered journal-page geometry.

This is materially stronger qualification evidence than a queued workflow, a local preview, or the presence of a workflow file alone. It supports source identity, reproducible assembly, and finite algebraic consistency at the exact author SHA.

It does not certify the continuum coarea identities, maximal-segment disintegration, optical recurrence, inherited spectral theorem, positive scalar remainder, signed forcing identities, or the new residual-height problem. The validation contract states this boundary correctly.

## 4. Scope and limitations of this audit

The complete active source contains 234 core modules and a large inherited archive. I have not independently reconstructed every historical theorem from first principles.

The substantive audit concentrates on:

1. the precise requests in the revision-96 external report;
2. the new collar-exclusion constant and its dependence on the inherited momentum-flow bound;
3. the definition and measurability of the capped occupation clock;
4. the target-value anchor for positive clock;
5. the passage from old positive occupation to a uniform clock lower bound;
6. the protected sets and direction choice in the running-compression argument;
7. the lower-gradient protection along the selected interval;
8. the conversion of a large running density ratio into an integrated optical-variation charge;
9. the absence of an uncontrolled word or component count in that conversion;
10. the exact three-way split of the old failure source;
11. the support computation for the residual;
12. the explicit outer schedule and exponent arithmetic;
13. the distinction between residual mass and residual essential height;
14. the reconnection to the inherited signed projected endpoint;
15. source identity and limit order; and
16. completeness and significance at the requested four-journal standard.

The inherited physical graph, signed prefix balance, Borel segment map, positive-cutoff source estimate, backward-end estimate, critical-volume layer cake, fixed-width scalar reduction, and positive scalar remainder are treated as source-pinned inputs. I checked their interfaces with modules 232--234, but this report is not a substitute for an independent specialist reconstruction of those inputs.

## 5. Response to the revision-96 report

Revision 96 isolated three exact continuation-failure mechanisms:

```text
physical availability failure,
running density-compression failure,
positive-occupation failure.
```

It did not prove any of the three small in normalized essential height. Revision 97 responds as follows.

### 5.1. Physical availability and collar obstruction

**Substantially addressed on the short scales used in the new reduction.**

Module 232 proves that an orbit starting in the original momentum range cannot reach the artificial `19/20` collar walls during a comparison interval of length at most

```text
r_col = R_-^2 / (800 Lambda_circ).
```

Thus the cap is not an active source of failure on the new short windows. This removes the particular artificial-collar obstruction from the quantitative reduction.

It does not prove a global full-domain continuation theorem at arbitrary comparison scales. Revision 97 does not claim such a theorem.

### 5.2. Running density compression

**Quantitatively addressed on protected same-event intervals.**

Module 233 proves an `O(qr)` normalized essential-height estimate for histories whose angular density undergoes a prescribed running compression on a protected interval of length `2qr` contained in the same original exact event.

This is the first collision-uniform height estimate for a genuine revision-96 failure mechanism. It is not a full comparison-domain derivative theorem, and it does not cover histories for which the protected interval does not exist. Those histories are transferred to the residual.

### 5.3. Positive occupation and sparse occupation

**Partially but substantially addressed.**

Module 232 introduces the capped occupation clock. Definite clock gives a target-value anchor into an interval average of the comparison source plus an explicit optical-variation term. The old positive-occupation admission mechanism gives a uniform lower bound on the new clock, so that its high-clock portion is quantitatively controlled.

Revision 97 does not prove a global sparse-occupation tail for all comparison histories. Low-clock histories outside the protected sets remain in the residual. This is represented accurately.

### 5.4. Exhaustion of the three failure classes

**Reduced to one exact residual, not fully closed.**

Module 234 gives an exact partition and proves that every nonresidual part has vanishing height along the prescribed outer schedule. The remaining residual has a precise support in the original near-entrance critical or short-residence source.

The residual itself is not estimated in essential height. Thus the old three-way obstruction has been geometrically compressed, but not eliminated.

### 5.5. Reconnection to signed projected forcing

**Addressed at the level of an exact scalar reduction.**

The new estimates are inserted back into the inherited signed projected endpoint. Revision 97 obtains an upper bound of the form

```text
pointwise scalar error
  <= residual essential height
     + explicit vanishing terms.
```

It also records the corresponding necessity/equivalence statement. The projected sign structure is preserved; the authors do not replace it by an uncontrolled sum of sheetwise positive parts.

The signed forcing is not proved to vanish because the residual height remains open.

### 5.6. Legal outer schedule

**Addressed.**

Revision 97 supplies a concrete schedule

```text
epsilon(B) = A_0 B^(-1/12),
q = 1/8,
r(B) = c epsilon(B)^4,
a(B) = sqrt(q r(B)).
```

For each fixed outer `B`, all positive cutoffs and comparison radii are fixed before the collision limit. No cutoff depends on the collision index.

### 5.7. Scalar-first discipline

**Addressed.**

The revision does not use the new failure-source reduction to promote unrestricted posterior, entropy, likelihood, or path-space conclusions. It keeps those downstream statements at their previously justified scope.

### 5.8. Independent specialist verification

**Not addressed.**

The exact-SHA workflows are successful, but the repository still records no independent human specialist audit of the inherited or new continuum arguments.

## 6. The revision-97 reduction architecture

Let `Z` denote the old continuation-failure source isolated in revision 96. Revision 97 introduces a capped occupation clock `c_r`, protected sets `P_{a,q,r}`, and the residual

```text
Y_{a,q,r} = {c_r < q} intersect P_{a,q,r}^c.
```

The old source is partitioned as

```text
Z
 = Z intersect {c_r >= q}
   disjoint-union
   Z intersect {c_r < q} intersect P_{a,q,r}
   disjoint-union
   Y_{a,q,r}.
```

The first part is controlled by the capped-clock anchor. The second is controlled by the running-compression theorem. The third is localized to the original singular source.

This architecture is logically appropriate. It avoids the principal defect of summing a one-sheet modulus over an uncontrolled number of histories. The proof pays target mass through actual interval occupation or actual optical variation, with multiplicity controlled by the inherited physical transport rather than by a count of symbolic words.

## 7. Audit of module 232: capped coarea occupation

### 7.1. Uniform exclusion of the artificial caps

The module uses the inherited momentum-flow estimate to choose

```text
r_col = R_-^2 / (800 Lambda_circ).
```

The maximum normalized momentum displacement during such a roof interval is

```text
sqrt(2 Lambda_circ r_col) / R_- = 1/20.
```

The original section momenta lie below `17/20`. Hence the comparison orbit stays below `18/20` and cannot reach the artificial `19/20` collar wall.

The numerical constants are consistent. The argument is uniform in the collision count because it uses the inherited collision-uniform momentum-flow constant, not a local chart count.

### 7.2. The capped occupation clock

For a comparison-domain set `H`, the clock is of the form

```text
c_{H,r}(x)
 = r^(-1) integral over T_r(x) of
     1_H(Phi_s x) min{1, A(Phi_s x)/A(x)} ds.
```

The cap is essential: it prevents a large density ratio at one sampled roof from creating artificial occupation. The clock is nonnegative and bounded by the normalized length of the comparison interval.

The target-value anchor follows by multiplying the clock inequality by the target density. Pointwise,

```text
A(x) min{1, A(Phi_s x)/A(x)}
 = min{A(x), A(Phi_s x)}
 <= A(Phi_s x),
```

up to the inherited guard/weight comparison and the optical-variation correction. Integration in `s`, followed by the inherited same-label transport and multiplicity-one projection, gives the stated interval-average control.

I found no missing factor of `r`, `q`, or the guard weight in the stated scale of the result.

### 7.3. Old positive occupation implies positive capped clock

If an old comparison history remains admissible on an interval of relative length at least `beta` and has density distortion at most `D`, then

```text
c_{H,r} >= beta / D.
```

This is the correct lower bound: the occupied time contributes `beta r`, while the capped density ratio is at least `D^(-1)`.

Thus the old positive-occupation class is genuinely included in a high-clock class. The result is stronger than merely observing that each individual history has nonzero occupation.

### 7.4. Height estimate for the high-clock source

The resulting bound has the form

```text
H_M(high-clock source)
 <= C_M q^(-1)
      [epsilon^(1/16) + epsilon^(-1) sqrt(r)].
```

The `q^(-1)` factor is unavoidable in this anchor. Since revision 97 fixes `q=1/8`, it does not threaten the outer limit.

The proof remains relative to the inherited interval-average and optical-variation inputs. Within that scope, I found the quantifiers and normalization consistent.

## 8. Audit of module 233: running compression height

### 8.1. Protected sets and direction choice

The module fixes

```text
d = 2 q r
```

and separates protected histories into a backward-long class and a forward-long class. Schematically,

```text
P_- = {tau^- > 2d},
P_+ = {tau^- <= 2d, z >= a, tau^+ > d}.
```

A direction `e(x)` is chosen so that the interval of length `d` stays inside the same original exact event.

This is the correct way to avoid charging an artificial comparison cut as if it were a physical source. The selected interval is not created by the proof; it is contained in the actual history.

### 8.2. Lower-gradient protection

On the selected interval, the radial-speed estimate gives a positive lower gradient cutoff of the form

```text
rho = min{a, sqrt(2 lambda_circ d)}.
```

For each fixed outer scale, `rho>0` is fixed before the collision limit. The positive-cutoff optical source theorem may therefore be applied without an illegal `rho=rho(m)` choice.

### 8.3. Running compression pays target mass

Suppose the running density ratio satisfies

```text
sup_{0 <= s <= d} A(x)/A(Phi_{e(x)s}x) > D_0 > 1.
```

Then along the selected interval the total decrease in density is at least

```text
(1 - D_0^(-1)) A(x).
```

The inherited differential inequality bounds this decrease by the integrated optical sensitivity source. Summing over histories and transporting at each intermediate roof yields

```text
H_M(running-compression source)
 <= C_M (1-D_0^(-1))^(-1) d
 = C_M (1-D_0^(-1))^(-1) q r.
```

The argument uses physical multiplicity one at the intermediate roof. It does not multiply by the number of words or components. This point is decisive and appears correctly handled.

### 8.4. Protected low clock implies compression

With `D_0=2`, if the density ratio stays above `1/2` throughout the protected interval of length `d=2qr`, then the capped clock receives at least

```text
(d/r) * (1/2) = q.
```

Therefore

```text
{c_r < q} intersect P_{a,q,r}
```

is contained in the `D_0=2` running-compression source. The inclusion and constants are correct.

### 8.5. Scope boundary

This theorem does not control histories outside the protected sets. It is therefore not a global compression theorem. Module 234 transfers precisely those unprotected histories to the residual rather than silently discarding them.

## 9. Audit of module 234: quantitative failure-source reduction

### 9.1. Exact source partition

The partition into high-clock, protected low-clock, and residual classes is a genuine disjoint decomposition. No history is lost at the interfaces, and the inequalities are applied after the source restrictions have been defined at finite count.

### 9.2. Residual support calculation

The residual is supported in

```text
{tau^- <= 4 q r, z < a}
 union
{ell <= 6 q r}.
```

The constants follow from `d=2qr`:

- failure of backward protection gives `tau^- <= 2d = 4qr`;
- once backward protection fails, failure of forward protection gives either `z<a` or `tau^+<=d`;
- in the latter case `ell=tau^-+tau^+<=3d=6qr`.

The support arithmetic is correct. The residual is therefore not a new artificial source. It is a restriction of the original near-entrance critical or short-residence source.

### 9.3. Recovered failure-source height

Combining modules 232 and 233 gives

```text
H_M(Z - Y_{a,q,r})
 <= C_M q^(-1)
      [epsilon^(1/16) + epsilon^(-1) sqrt(r)]
    + C_M q r.
```

No term in this estimate requires `a` or `r` to depend on the collision count. The lower-gradient cutoff used in the compression theorem remains positive at every fixed outer scale.

### 9.4. Explicit outer schedule

Revision 97 chooses

```text
epsilon(B) = A_0 B^(-1/12),
q = 1/8,
r(B) = c epsilon(B)^4,
a(B) = sqrt(q r(B)).
```

Then

```text
epsilon(B)^(1/16) = O(B^(-1/192)),
epsilon(B)^(-1) sqrt(r(B)) = O(epsilon(B)),
q r(B) = O(epsilon(B)^4).
```

Hence the recovered source is `O(B^(-1/192))`, with the first term dominant. The exponent arithmetic is correct.

The inherited scalar endpoint becomes

```text
E_M
 <= H_M(Y_{a(B),q,r(B)})
    + C_M B^(-1/192).
```

This is a genuine improvement over revision 96, where all three failure classes remained as unquantified height terms.

### 9.5. Residual mass estimate

The support localization and inherited critical/short-residence volume estimates give a fixed-window mass bound with powers of the form

```text
(qr)^(129/256) + (qr)^(1/32).
```

Both tend to zero along the prescribed schedule.

The module correctly refrains from concluding that the residual essential height tends to zero. That implication would be false without an additional persistence, capacity, or regularity theorem.

### 9.6. Exact endpoint criterion

The revision records that the original pointwise endpoint is equivalent, along the legal schedule, to

```text
H_M(Y_{a(B),q,r(B)}) -> 0
```

for every fixed reconstruction window `M`. This criterion is appropriately formulated at the original pointwise topology. It is not asserted to hold.

## 10. Limit order and quantifier audit

The legal order used by revision 97 is:

1. form the complete finite-count physical source restrictions and signed projection;
2. fix the outer reconstruction parameter `B`;
3. at that fixed `B`, fix `epsilon(B)`, `q`, `r(B)`, `a(B)`, the induced positive gradient cutoff, and all auxiliary bands;
4. take the collision limsup and normalized essential height;
5. enlarge auxiliary bands where the inherited inputs require it;
6. only after these ordered limits let the outer parameter `B` tend to infinity.

This is the correct order for the positive-cutoff source estimates used in module 233. I found no step choosing a cutoff as a function of the collision count.

The finite-count remainders are not declared uniform at zero cutoff. The proof avoids needing such a declaration by fixing the positive cutoff at each outer scale.

## 11. Signed projection and cancellation

Revision 97 preserves the signed projected forcing architecture developed in the preceding revisions. This matters because a sum of positive sheetwise derivative terms can be much larger than the projected positive forcing.

The new high-clock and compression estimates are used to control a positive majorant of the old continuation-failure subsource. After this control, the proof returns to the inherited signed scalar inequality. Completed-prefix losses and physical negative contributions are not reintroduced as positive costs.

The residual `Y_{a,q,r}` is left as a restriction of the original target source. It is not called the Jordan positive part of the projected derivative, and the paper does not claim that its small mass forces small height.

I found no decisive sign reversal or projection-order error in this interface.

## 12. Exact theorem-bearing contribution of revision 97

Subject to the inherited inputs, I regard the following as the genuine contribution of this revision:

1. a collision-uniform short-window exclusion of the artificial momentum caps;
2. a capped same-label occupation clock adapted to the target density;
3. a high-clock target-value anchor at the original normalized height;
4. a proof that old positive occupation produces definite capped clock;
5. a protected same-event running-compression theorem with `O(qr)` height;
6. a proof that protected low clock forces density compression;
7. an exact finite-count partition of the old continuation-failure source;
8. a geometric support theorem for the residual;
9. an explicit legal outer schedule eliminating the recovered failure source;
10. a scalar reduction from three unquantified failure classes to one residual source; and
11. an exact residual-height criterion for the original pointwise endpoint.

These are not bookkeeping-only results. In particular, the running-compression theorem is a new transverse weighted-capacity estimate, and the capped-clock anchor gives a usable pointwise mechanism rather than merely an integrated occupation statement.

The contribution stops one theorem before scalar closure.

## 13. Claims that remain unproved

Revision 97 correctly leaves unproved:

- decay of `H_M(Y_{a(B),q,r(B)})`;
- a collision-uniform essential-height estimate for the near-entrance critical residual;
- a collision-uniform essential-height estimate for the genuinely short-residence residual;
- a full comparison-domain derivative or compression theorem;
- a global sparse-occupation tail theorem;
- zero signed projected forcing;
- unconditional prescribed-width persistence of every upper spike;
- zero essential-height charge for the original critical-or-short-residence source;
- the upper pointwise half of the exact-label raw local limit;
- the unrestricted pointwise exact-label raw local limit theorem;
- unrestricted same-roof point-conditioned kernel convergence;
- forward essential-likelihood convergence;
- unrestricted path-space total variation or relative entropy convergence;
- unrestricted normalization on zero or merely positive arithmetic classes;
- an unnormalized growing-window theorem;
- independent human specialist approval; and
- a formal proof certificate.

The source manifest, publication-status file, proof ledger, referee-status file, and specialist-audit file represent these boundaries accurately.

## 14. Decisive remaining obstruction

The remaining residual is supported on two geometric mechanisms:

```text
near-entrance critical target:
  tau^- <= 4qr and z < a,

genuinely short physical segment:
  ell <= 6qr.
```

The inherited mass estimates show that the total source mass of these sets tends to zero. This does not rule out concentration.

A sequence of nonnegative roof functions may have integral tending to zero while its essential supremum stays equal to one or diverges. The entire pointwise upper problem is to show that the physical source cannot realize such a sequence after collision normalization.

Revision 97 has therefore reached a much sharper formulation of the endpoint, but it has not crossed the topology gap from small mass to small height.

## 15. Requirements for a successful next revision

### 15.1. Prove a normalized essential-height theorem for the residual

The next revision needs a bound of the form

```text
H_M(Y_{a,q,r})
 <= C_M epsilon^(-Q)
      [a^eta + (qr)^beta]
```

for finite `Q` and positive `eta,beta`, or another estimate which vanishes under a legal outer schedule.

An estimate only for fixed-window mass, weak type below the pointwise threshold, or finite `L^p` with fixed `p` is not sufficient.

### 15.2. Separate the two residual mechanisms

It would be useful to define

```text
Y_critical = Y intersect {tau^- <= 4qr, z < a},
Y_short    = Y intersect {ell <= 6qr},
```

with overlap assigned consistently, and prove a distinct height mechanism for each.

The critical component and the short-residence component have different geometry. Treating them separately may avoid paying an unnecessarily large common majorant.

### 15.3. Control the near-entrance critical component

A successful theorem should show that a high target value in the near-critical entrance region forces at least one of:

- a controlled radial-shell crossing;
- a quantitatively bounded critical entrance trace;
- a signed radial-current contribution;
- a Carleson/capacity charge in the two-dimensional source variables; or
- persistence over a roof interval whose width is sufficient to convert mass control into height control.

Zero area of the exact critical set is not enough. Directional traces and transverse weighted capacity must remain visible.

### 15.4. Control the genuinely short-residence component

The existing zero-residence trace-volume identity and short-segment mass estimates should be upgraded to a pointwise-height statement.

Possible routes include:

- a short-segment maximal inequality;
- a two-sided entrance/exit trace comparison;
- a residence-shell persistence theorem;
- a bounded-overlap theorem for target ancestors;
- a signed entrance-and-termination current; or
- regularity above the one-dimensional pointwise embedding threshold with a vanishing norm.

A raw count of short histories is not acceptable unless it is collision-uniform after the correct weights.

### 15.5. Prove a persistence-or-capacity dichotomy for high residual targets

The central missing implication is:

```text
large residual target height
  => enough nearby roof mass or enough transverse capacity.
```

The theorem must be formulated for the complete projected source, not for one physical sheet at a time. Summing a single-sheet one-half modulus over an uncontrolled number of sheets does not solve the problem.

### 15.6. Preserve signed cancellation

The next revision should retain the projected signed forcing before taking positive parts. If a positive residual majorant is introduced, the manuscript must prove that projection overcount is quantitatively harmless.

### 15.7. Close the scale arithmetic explicitly

Once residual-height bounds are available, the authors should state one explicit legal choice of

```text
epsilon(B), q(B), r(B), a(B),
positive gradient cutoffs,
auxiliary bands,
```

and verify term by term that every error tends to zero in the declared order.

The current fixed choice `q=1/8`, `r=c epsilon^4`, `a=sqrt(qr)` is a viable baseline, but the final residual estimates may require rebalancing.

### 15.8. Do not promote downstream laws before scalar closure

The strongest finite-roof-norm posterior and entropy statements already available may remain at their stated scope. Uniform point-conditioned, essential-likelihood, and unrestricted path-space conclusions should be promoted only after the scalar upper endpoint is proved.

### 15.9. Obtain independent specialist verification

Before a claim of top-tier readiness, independent specialists should reconstruct at least:

- the four-record spectral input and finite-peak reference;
- the physical graph and exact-event conventions;
- the coarea and Borel-segment disintegrations;
- the optical recurrence, traces, and positive-cutoff source bounds;
- the backward-end and critical-volume estimates;
- the positive scalar remainder;
- the signed projected forcing;
- the capped-clock anchor;
- the running-compression theorem; and
- the eventual residual-height theorem.

Successful CI is valuable but cannot replace this mathematical audit.

## 16. Exposition and architecture

The focused revision-97 article is clearer than the complete archive and accurately states its remaining boundary. Several exposition points should be preserved in the next version.

1. Every summary should say that the recovered failure source vanishes but the residual height does not yet.
2. The residual mass estimate must never be paraphrased as residual-height decay.
3. The distinction between artificial cap exclusion on short windows and global comparison-domain availability should remain explicit.
4. The protected running-compression theorem should not be described as a full-domain derivative theorem.
5. The residual should continue to be identified as a restriction of the original physical source, not a proof-generated defect.
6. The fixed-positive-cutoff quantifiers should remain adjacent to every collision limit using the positive-cutoff source theorem.
7. The signed projected forcing should remain distinct from a sum of pre-projection positive sheetwise charges.
8. The successful exact-SHA workflows should be reported as source and build qualification, not as mathematical certification.
9. Historical provenance and archive-preservation material should remain supplementary rather than carrying the principal theorem narrative.
10. The final paper should provide a compact dependency diagram from the residual-height theorem back to the few inherited inputs actually used.

The current source and publication-status metadata are notably candid. That accuracy should be retained.

## 17. Significance and venue assessment

Revision 97 is the strongest continuation-failure reduction in the revision sequence reviewed here. It converts three qualitative obstruction classes into two quantitatively negligible recovered classes and one explicit residual supported on the original singular source. The capped-clock and running-compression tools may be useful in other singular transport or billiard problems where transverse multiplicity prevents direct summation of sheetwise regularity.

If independently verified and completed by a residual-height theorem, the resulting pointwise raw inversion theorem could be a substantial contribution. Even without final closure, modules 232--234 could form part of a strong specialized paper centered on quantitative failure-source reduction.

At the requested *Annals/Acta/Inventiones/JAMS* benchmark, however, the manuscript's governing assertion is the unrestricted pointwise theorem. The current revision ends with an exact equivalence to an unproved residual-height condition. That is an important reduction, but not a completed theorem of the advertised breadth.

## 18. Final recommendation

Revision 97 responds seriously and positively to the revision-96 report. It removes the short-window artificial-collar obstruction, introduces a capped occupation clock, proves a protected running-compression height theorem, decomposes the old failure source exactly, localizes the residual, and supplies a legal schedule under which every recovered part has vanishing normalized essential height.

The two exact-SHA qualification runs complete successfully, and I found no decisive internal error in modules 232--234 at their stated scope, conditional on the inherited inputs.

Nevertheless, the residual `Y_{a,q,r}` is proved small only in integrated mass, not in normalized essential height. Its vanishing is exactly equivalent to the unresolved pointwise upper endpoint. The signed forcing is therefore not proved zero, the upper pointwise half remains open, and the unrestricted exact-label raw local limit theorem is still unproved.

**I therefore recommend rejection in the present form at the requested Annals/Acta/Inventiones/JAMS benchmark.**
