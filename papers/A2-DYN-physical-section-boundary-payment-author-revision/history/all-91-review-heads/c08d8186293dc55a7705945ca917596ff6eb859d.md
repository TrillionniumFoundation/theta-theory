# External top-four referee report on A2-DYN revision 96

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v96-referee-response-2026-10-13`, `revision/a2-dyn-v96-referee-copy-2026-10-13`  
**Reviewed author commit:** `4b3ea4f4ce112338654279797cd4ce380842b4af`  
**Reviewed repository tree:** `e7ddd4ee012b8ffabb556b8a88542ef770c283aa`  
**Active manuscript directory:** `papers/A2-DYN-v96-referee-response`  
**Canonical revision identity:** `a2-dyn-v96-exact-label-continuation-occupation-2026-10-13`  
**Active mathematical source:** 231 numbered core modules; revision 96 adds modules 229--231  
**Immediate author baseline:** revision 95 at `be6116aab636b8afb3cceb834e10cb7559c1d992`  
**Frozen revision-95 paper tree:** `5d15fd482383c35aac22d922c730a5d20cd69507`  
**Controlling external report:** `reviews/a2-dyn-v95-external-top4-review-2026-10-13/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `6a34c211c84868fb1866d7613985a164257debe0` / `23d0415a5c2823b67259c3697fb46d5b896c7584`  
**Qualification runs at review freeze:** response `38286036069`; referee-copy `38286046386`; both queued with no conclusion  
**Date:** 13 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, probability, o-minimal-geometry, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 96 is a substantive and theorem-bearing response to the revision-95 report. It attacks the two residual mechanisms identified there rather than adding downstream consequences. In particular, it proves new estimates for the positive two-nongrazing packet itself and for an all-gradient target-critical source, both on a geometrically defined physical-continuation class. It also gives an exact, disjoint localization of every nonadmitted target into three original-source failure classes.

The new contribution is not cosmetic. Conditional on the inherited inputs, revision 96 establishes:

1. a physical comparison flow which crosses section-decision walls but not true physical, collar, or backward-critical boundaries;
2. an exact-label occupation anchor retaining the inverse coarea-density ratio and requiring no return-count or word-count factor;
3. collision-normalized essential-height decay of the full admitted original union `z<a or ell<delta`, with all gradients below `a` present before the collision limit;
4. an inner target-critical estimate without a lower gradient cutoff or a finite-annulus truncation;
5. decay of the admitted positive two-nongrazing same-segment packet itself, not merely decay of its comparison error;
6. a disjoint partition of the nonadmitted original source into physical-interruption, coarea-compression, and insufficient exact-label occupation classes; and
7. a necessary-and-sufficient failure-source criterion for the original pointwise endpoint along an explicit legal outer parameter schedule.

I found no decisive sign error in the comparison flow, no missing inverse Jacobian in the occupation transfer, no pooling of neighboring exact labels, no uncontrolled visit or component count, no exponent error in the cofinal source estimate, no illicit lower-gradient cutoff inside the collision limsup, no circular use of the desired pointwise theorem in the admission tests, and no unjustified promotion of the admitted estimates to the full source.

The recommendation remains negative because the governing pointwise theorem is still not proved. The manuscript does not show that every possible spike target is admitted, and it proves no vanishing estimate for the exact failure source

```text
Z_{r,D,beta}^epsilon
 = physical-interruption source
   + coarea-compression source
   + insufficient-same-label-occupation source.
```

These three classes are not peripheral bookkeeping. They are precisely the mechanisms by which a target can evade the new occupation anchor. A fixed-height pulse can have a short comparison lifetime, an arbitrarily large inverse density ratio, or an arbitrarily small exact-label occupation fraction. Such a pulse may be invisible to integrated estimates while remaining visible to the essential supremum.

Consequently revision 96 still does not establish:

- zero essential height of the complete comparison-failure source;
- admission of all two-nongrazing short packets;
- decay of the complete zero-gradient critical target core;
- vanishing of the bidirectional or joint signed forcing;
- unconditional upper-spike persistence;
- zero charge of the original critical-or-short-residence source;
- the upper pointwise half of the exact-label raw local limit theorem;
- the unrestricted pointwise exact-label raw local limit theorem; or
- the unrestricted point-conditioned, essential-likelihood, total-variation, or entropy consequences.

At the requested benchmark, a paper organized around unrestricted pointwise raw inversion must prove that pointwise theorem or supply a comparably broad completed theorem around which the manuscript is reorganized. Revision 96 makes the residual obstruction far more geometric and testable, but it remains an obstruction.

## 2. Frozen source, chronology, and preservation

Both reviewed author refs resolve to

`4b3ea4f4ce112338654279797cd4ce380842b4af`,

with repository tree

`e7ddd4ee012b8ffabb556b8a88542ef770c283aa`.

The active article is

`papers/A2-DYN-v96-referee-response`.

The source manifest identifies revision 95 as the immediate author baseline:

`be6116aab636b8afb3cceb834e10cb7559c1d992`,

with frozen paper tree

`5d15fd482383c35aac22d922c730a5d20cd69507`.

The revision-96 author commit descends from the controlling revision-95 review commit

`6a34c211c84868fb1866d7613985a164257debe0`.

The packet preserves 228 inherited core modules and adds exactly:

- `core/229_same_label_continuation_occupation.tex`;
- `core/230_recurrent_packets_and_untruncated_radial_core.tex`;
- `core/231_continuation_failure_and_joint_forcing.tex`.

The complete revision-95 article is retained in the archive, every revision-95 root file is snapshotted, the unchanged revision-95 sibling remains the inherited claim authority, and both distinct revision-88 variants remain separately identified. I found no silent overwrite or merger of incompatible historical sources.

The present review branch starts directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v96-external-top4-review-2026-10-13/`.

No author manuscript, author revision branch, workflow, prior report, preserved source variant, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The revision-96 workflow is

`.github/workflows/a2-dyn-v96-qualification.yml`.

At review freeze the exact-SHA runs were:

- response branch: `38286036069`;
- referee-copy branch: `38286046386`.

Both were `queued` with `conclusion=null`. I therefore do not describe revision 96 as having completed fresh remote qualification.

The declared qualification contract is meaningful. It is designed to verify:

- the frozen revision-95 paper tree;
- every revision-95 root snapshot;
- the controlling revision-95 report blob;
- preservation of both revision-88 source variants;
- byte and executable-mode preservation of inherited nonreplaced sources;
- a SHA-256 inventory for newly authored sources;
- ordinary and optimized finite-fixture agreement;
- native compilation of the focused article and complete supplement;
- recorder coverage of all 231 active cores;
- stabilized references and warning gates; and
- page-box and selected-render checks.

The local evidence reports a ten-page focused preview and 28,479 rational finite fixtures agreeing in normal and optimized modes. The complete baseline archive was not materialized for that local preview.

These checks can establish source identity, finite algebraic consistency, and reproducible assembly. They cannot certify the continuum coarea identities, physical continuation through section decisions, exact-label occupation disintegration, inherited spectral and critical-volume inputs, or the missing failure-source estimates. Qualification is not mathematical certification.

## 4. Scope of this audit

The complete archive contains 231 numbered core modules and a large inherited pipeline. I have not independently reconstructed every historical theorem.

The substantive audit concentrates on:

1. the requests in the revision-95 external report;
2. the comparison collar and its distinction from the original stopped exact-event segments;
3. the extension of the canonical endpoint flow across section-decision walls only;
4. the original coarea density on the enlarged physical continuation domain;
5. the exact-label occupation selector and the absence of label pooling;
6. the inverse coarea-density ratio `D` and occupation fraction `beta`;
7. injectivity at each sampled roof and the absence of a return-count factor;
8. the all-gradient admitted source estimate in module 230;
9. the inner critical-core corollary;
10. the estimate of the positive two-nongrazing packet itself;
11. the fixed-positive-gradient and full-event occupation variants of that estimate;
12. the exact three-way failure partition in module 231;
13. the endpoint inequality and outer parameter schedule;
14. the relation to the inherited bidirectional signed forcing criterion;
15. limit order, source preservation, and qualification status; and
16. completeness, novelty, and significance at the requested four-journal standard.

The inherited endpoint Hessian, all-contact motion, collision-uniform cubic estimate, optical density sensitivity, Borel maximal-segment parametrization, critical-volume estimate, backward-end estimate, fixed-width scalar average, positive scalar remainder, two-ended packet theorem, and bidirectional forcing theorem are treated as source-pinned inputs. Their interfaces with modules 229--231 were checked directly. This report does not independently certify those inherited theorems.

## 5. Response to the revision-95 report

### 5.1. Estimate the positive two-nongrazing packet itself

**Substantially advanced, but only on the admitted continuation class.**

Revision 95 proved that the target source, inlet trace, outlet trace, and per-segment two-ended minimum have the same ordered zero-residence obstruction at fixed positive gradient. It did not estimate the common positive packet on segments with two nongrazing endpoints.

Revision 96 now proves, for the admitted family,

```text
H_M(M_{rho,delta}^{epsilon,adm})
 <= C(D/beta) delta^(1/32)
    + C(1+epsilon^(-1)) delta.
```

This is an estimate of the packet itself. It is therefore a direct response to the principal revision-95 request.

The theorem does not cover the two-nongrazing packet failing continuation, compression, or occupation. The full packet charge remains unproved.

### 5.2. Replace finite annulus heads by an all-gradient theorem

**Substantially advanced, but only on the admitted continuation class.**

The admitted source `z<a or ell<delta` is formed at finite collision count with every gradient below `a` present. The resulting estimate

```text
C(D/beta) [a^(129/128) + delta^(1/32)]
```

has no lower gradient cutoff and does not sum annular limsups after the collision limit. This genuinely closes the disappearing-annulus defect for admitted targets.

It does not prove that every target in the full critical core is admitted. The disappearing-tail problem has therefore been transformed into failure-source control rather than eliminated globally.

### 5.3. Localize the joint forcing into physical classes

**Addressed structurally, but not quantitatively closed.**

Module 231 partitions the original source exactly into the admitted part and three disjoint failed-test sources. Since the earlier bidirectional joint forcing is bounded by the original source, this gives a physical localization of the remaining forcing obligation.

No quantitative estimate proves that the failed-test source vanishes. The localization is exact and useful, but it remains conditional.

### 5.4. Produce a legal parameter schedule

**Addressed for all explicit admitted-source errors.**

The displayed choice

```text
D=2,
beta=1/4,
r(B)=c epsilon(B)^4,
epsilon(B)=A_0 B^(-1/12)
```

makes

```text
epsilon^(1/16) -> 0,
epsilon^(-1) sqrt(r) = O(epsilon) -> 0.
```

For the cofinal admitted union

```text
a=r^(1/8),
delta=r^(1/4),
```

the slower contribution is

```text
delta^(1/32)=r^(1/128).
```

The exponent arithmetic is correct. No rate is available for the failure source itself.

### 5.5. Close the scalar theorem before downstream promotion

**Respected.**

The manuscript does not promote unrestricted same-roof ratios, forward essential likelihood, path-space total variation, relative entropy, or arithmetic-zero-class normalization.

### 5.6. Independent specialist verification

**Not supplied.**

The author-side source audit is useful, but it is not an independent human reconstruction of the physical flow, coarea density, exact-label occupation argument, inherited spectral inputs, or continuum endpoint closure.

## 6. Module 229: same-label continuation occupation

### 6.1. The comparison domain

The module separates two notions which had previously been conflated:

- the original exact-event segment, stopped at section decisions; and
- the underlying regular physical word, which may continue through a section-decision wall.

The auxiliary domain retains actual regular physical trajectories, the endpoint collar

```text
|p_0|, |p_m| < 19/20,
```

and `z>0`. It still stops at true grazing, first-hit, competing-hit, collar, and backward-critical boundaries. The original stopped flow and all original source definitions are left unchanged.

This distinction is legitimate and important. A section decision can terminate an exact label without terminating the physical stationary word.

### 6.2. The physical comparison flow

On the comparison collar the reduced Hessian remains uniformly positive because the endpoint incidences remain uniformly positive. The vector field

```text
X_hat = K^(-1) g / (g^T K^(-1) g)
```

therefore satisfies

```text
X_hat F = 1,
X_hat theta = 0.
```

The inherited all-contact motion and cubic estimates control the original guard and angular Jacobian on each surviving regular physical word. The module does not assert continuation through a true singularity.

The physical angular density

```text
A_hat = omega / (4 pi c_* chi)
```

is retained. The comparison is not made with an artificial invariant density.

### 6.3. Exact-label occupation and distortion

For a Borel subevent `H` of the original exact event, the module defines:

```text
d_{e,r}(x)
 = ess sup_s A_hat(x)/A_hat(Phi_{es}x),

o_{H,e,r}(x)
 = r^(-1) int_0^r 1_H(Phi_{es}x) ds.
```

A target is admitted when one comparison direction survives for the prescribed interval, the inverse density ratio is at most `D`, and at least a fraction `beta` of the interval returns to the identical original selected event.

The selector includes the exact `n` and `k`, both endpoint section tests, and any additional original selector. A nearby label does not count. This avoids a hidden pooling of occupation classes.

### 6.4. The anchoring inequality

For the admitted source the theorem proves

```text
R_{H_adm}^epsilon(t)
 <= D/(beta r)
    int_{t-r}^{t+r}
       [R_H^epsilon(u) + kappa_epsilon(r) U_H(u)] du,

kappa_epsilon(r)
 <= C epsilon^(-1) sqrt(r).
```

The proof averages only over sampled roofs returning to `H`. At each fixed sampled roof the comparison flow is injective, so arbitrarily many decision-wall crossings do not create a return-count factor. The positive and negative comparison directions occupy disjoint sides of the target roof, so no additional multiplicity is hidden in the two-sided integral.

I find this argument coherent at finite collision count, conditional on the inherited physical coarea density and regular-word flow.

### 6.5. Noncircularity

The admission tests use:

- physical survival;
- the ratio of original coarea densities; and
- occupation of the original exact event.

They do not use the size of the projected target density, the desired upper theorem, or an assumed pointwise persistence conclusion. The construction is therefore not circular.

### 6.6. Limitation of module 229

The theorem supplies an implication:

```text
admission  =>  occupation anchor.
```

It supplies no theorem of the form

```text
large target source  =>  admission,
```

nor a normalized estimate for the complement. In particular:

- the comparison lifetime may be shorter than `r`;
- the density ratio may exceed every prescribed legal `D`; or
- the same exact label may occupy less than every prescribed legal fraction `beta`.

Those are exactly the three failure mechanisms retained in module 231.

## 7. Module 230: recurrent packets and the untruncated admitted core

### 7.1. The original-union estimate

For

```text
H_{a,delta}=Pi intersect {z<a or ell<delta},
```

the unweighted source is bounded by the inherited complete critical-volume source plus the backward-end source. The union is counted once.

Applying the unweighted occupation anchor before the collision limit gives

```text
limsup_m sup_{R,n,k}
 m^2 ||R_{H_{a,delta}^{adm}}^epsilon||_infinity
 <= C(D/beta)
    [a^(129/128) + delta^(1/32)].
```

The entire set `z<a` is present at finite count. There is no lower gradient cutoff and no post-limsup summation of annular estimates.

The fixed auxiliary-band floor is divided by the previously fixed sampling radius and removed only after the collision limsup by enlarging the band. The spectral remainders vanish at fixed parameters. I found no illegal limit exchange in this step.

### 7.2. Cofinal exponent arithmetic

For

```text
a=h^(1/8),
delta=h^(1/4),
alpha=129/128,
gamma=1/32,
```

one has

```text
a^alpha     = h^(129/1024),
delta^gamma = h^(1/128).
```

The latter is the slower decay. The stated bound

```text
C(D/beta) h^(1/128)
```

is correct.

### 7.3. The inner critical core

If the target satisfies

```text
z(t)<a/2,
r<=a^2/(8 Lambda),
```

radial monotonicity keeps every available comparison interval inside `z<a`. Admission to the ordinary exact event then already supplies occupation of the critical selector. The full admitted inner core obeys

```text
C(D/beta) a^(129/128).
```

This removes the need for a separate radial-return test on the admitted inner core and includes annuli which may disappear with the collision count.

The conclusion is still conditional on ordinary-event admission.

### 7.4. The positive two-nongrazing packet

For short physical segments with two nongrazing endpoints, module 226 defined the positive same-segment packet

```text
M_sigma=min(F_sigma^-,F_sigma^+).
```

Revision 96 restricts to targets admitted to the original short-segment event and proves

```text
H_M(M_{rho,delta}^{epsilon,adm})
 <= C(D/beta) delta^(1/32)
    + C(1+epsilon^(-1)) delta
```

at every previously fixed positive entrance-gradient cutoff `rho`.

This estimate is genuinely stronger than the revision-95 comparison theorem. It controls the common positive packet itself rather than only the difference between that packet and the target, inlet, or outlet source.

A second theorem, testing occupation only in the ordinary exact event, gives

```text
C(D/beta)
  [epsilon^(1/16)+epsilon^(-1)sqrt(r)]
 + C(1+epsilon^(-1)) delta.
```

This is compatible with the original reconstruction schedule.

### 7.5. Limitation of module 230

The module does not prove:

- admission of every two-nongrazing short segment;
- decay of the packet on nonadmitted segments;
- a zero-gradient theorem obtained by exchanging `rho downarrow 0` with the collision limit; or
- decay of the full critical core outside the admitted family.

Thus both principal revision-95 residual mechanisms are solved on the admitted class and transferred to the failure source on its complement.

## 8. Module 231: continuation failure and the endpoint

### 8.1. Exact three-way partition

For the full original exact event, the module partitions every nonadmitted target into:

```text
N_T: neither comparison direction survives for length r;
N_D: a direction survives, but no available direction has d<=D;
N_O: bounded compression is available, but no such direction has
     same-label occupation at least beta.
```

The classes are disjoint by construction and exhaustive with the admitted class. Each failed target is charged once with its original weight and original coarea measure.

This is a clean physical localization. It does not replace the original pointwise target by a subfamily.

### 8.2. Pointwise inequality

Writing `Z_{r,D,beta}^epsilon` for the total failed-test source, the module obtains

```text
b^epsilon(t)
 <= Z_{r,D,beta}^epsilon(t)
  + D/(beta r)
      int_{t-r}^{t+r}
        [b^epsilon(u)+kappa_epsilon(r)p(u)] du.
```

The scalar endpoint estimate is consequently

```text
E_M
 <= C_M B^(-1/192)
  + H_M(Z_{r,D,beta}^epsilon)
  + C(D/beta)
      [epsilon^(1/16)+epsilon^(-1)sqrt(r)].
```

The positive scalar remainder and reconstruction exponents are used in the same order as in the inherited endpoint argument.

### 8.3. Legal schedule and equivalence

More generally, if

```text
D/beta <= C epsilon^(-tau),
tau<1/16,
r=c epsilon^N,
N>2(1+tau),
```

then both explicit admitted-source errors vanish. Along such a schedule, the original pointwise theorem is equivalent to

```text
H_M(Z_{r,D,beta}^{epsilon(B)}) -> 0.
```

Necessity follows from `0<=Z<=b^epsilon` and the inherited positive scalar remainder. Sufficiency follows from the displayed endpoint estimate. I find this equivalence logically correct.

### 8.4. Why the criterion is not closure

The module itself gives an elementary pulse model with occupation fraction `delta/r`. This correctly demonstrates that a large target can fail the occupation test even when its total mass is small.

Likewise, the inherited exit-flux formula retains an inverse physical Jacobian. A small unweighted boundary flux does not imply a small initial weighted exit source. The compression and short-lifetime classes therefore cannot be discarded by zero-area or integrated-mass reasoning.

The criterion identifies the remaining theorem. It does not prove it.

## 9. Cross-checks against inherited geometry

### 9.1. Endpoint Hessian and radial flow

The inherited general endpoint Hessian estimate is stated on every actual regular physical word, before restriction to the original section. On the comparison collar `|p_0|,|p_m|<19/20`, both endpoint incidences remain uniformly positive. This supports the uniform positive Hessian required by module 229.

### 9.2. All-contact motion and the unchanged guard

The inherited contact inverse and depth-decay estimates are pointwise statements on actual regular physical trajectories and do not require a positive lower bound on internal incidence or clearance. They therefore apply while the physical word continues through a section-decision wall. The original guard remains controlled; no protected replacement guard is inserted.

### 9.3. Cubic and angular-Jacobian variation

The inherited cubic reduced-action theorem uses stationary-action cancellation and gives collision-uniform third derivatives on regular words. It supports the angular Jacobian variation used in the comparison density. It does not supply continuation through singularities, and revision 96 does not use it for that purpose.

### 9.4. Optical density

The inherited optical-sensitivity formula retains inverse internal incidences and explicitly warns that positivity alone does not make their complete source sum finite. Revision 96 therefore correctly retains the density-ratio test `d<=D` rather than claiming uniform distortion for every comparison orbit.

### 9.5. Borel segments and multiplicity

The inherited maximal-segment theorem gives a Borel bijection between complete regular segments and their roof-angle coordinates. Each intermediate physical state is counted once, with its incident component retained. This supports both the two-ended variation sum and the fixed-roof injectivity used by the occupation anchor.

These cross-checks support the stated conditional proofs. They also explain why the compression and physical-interruption failures remain genuine rather than removable artifacts.

## 10. Limit order

Revision 96 generally respects the required order:

1. define the original, admitted, and failed physical sources at finite collision count;
2. keep all gradients in the admitted critical selector before any collision limit;
3. fix `epsilon`, `r`, `D`, `beta`, `a`, `delta`, positive entrance-gradient cutoffs, and auxiliary bands;
4. take the collision limsup and exact-label suprema;
5. enlarge the auxiliary band only afterwards;
6. remove only those cutoffs for which an ordered passage is explicitly proved; and
7. keep the reconstruction band `B` outermost.

The manuscript does not:

- choose `a`, `delta`, `D`, `beta`, or a gradient cutoff as a function of collision count;
- infer full-source decay from a theorem on the admitted subfamily;
- sum a single-sheet modulus by a raw number of words;
- remove the inverse coarea ratio from the occupation transfer;
- replace exact-label occupation by occupation of neighboring labels;
- move a minimum or positive part through projection; or
- treat source localization as source decay.

These restrictions are mathematically necessary and should remain explicit.

## 11. Exact theorem-bearing contribution of revision 96

Conditional on the inherited inputs, I regard the following as the genuine new mathematical contribution:

1. a regular physical comparison collar across section-decision walls;
2. preservation of the original physical coarea density on that collar;
3. an exact-label occupation selector retaining all original label tests;
4. a two-sided finite-count occupation anchor with inverse density ratio `D`;
5. elimination of any return-count or component-count factor by fixed-roof injectivity;
6. an all-gradient admitted source-height theorem for `z<a or ell<delta`;
7. an admitted inner critical-core theorem without a lower gradient cutoff;
8. essential-height decay of the admitted positive two-nongrazing packet itself;
9. a second packet estimate directly compatible with the reconstruction limit;
10. an exact disjoint partition into interruption, compression, and sparse-occupation failures;
11. a complete pointwise localization of the original source into the admitted and failed parts; and
12. a legal necessary-and-sufficient failure-source criterion for the original endpoint.

These are not metadata changes, finite-norm interpolation, or a restatement of the revision-95 packet identity. They add a new physical recurrence mechanism and turn the remaining pointwise obstruction into three explicit geometric tests.

The contribution stops before the manuscript's governing theorem because no estimate proves that the three failed-test sources have vanishing normalized essential height.

## 12. Claims that remain unproved

The manuscript correctly leaves unproved:

- admission of every possible upper-spike target;
- zero height of the physical-interruption failure source;
- zero height of the coarea-compression failure source;
- zero height of the insufficient exact-label occupation source;
- zero height of their union `Z_{r,D,beta}^epsilon`;
- zero charge of the complete two-nongrazing short packet;
- a collision-uniform zero-gradient short-source theorem for the full source;
- full target-critical core height decay;
- vanishing of the bidirectional signed forcing;
- vanishing of the earlier joint signed upper forcing;
- zero essential-height charge of the original critical-or-short-residence source;
- unconditional prescribed-width persistence of every upper spike;
- the upper pointwise half `[P-G]_+ -> 0`;
- the unrestricted pointwise exact-label raw local limit theorem;
- unrestricted same-roof point-conditioned kernel convergence;
- forward essential-likelihood convergence;
- unrestricted path-space total variation or relative entropy convergence;
- unrestricted normalization on all merely positive or zero arithmetic classes;
- an unnormalized growing-window theorem;
- independent human specialist approval; and
- a formal proof certificate.

The abstract, source manifest, proof ledger, publication status, response to the referee, and final theorem statements represent these boundaries accurately.

## 13. Requirements for a successful next revision

The next revision should not introduce another conditional source criterion unless it quantitatively decreases the present failure source. The three failure classes are now explicit enough to be attacked separately.

### 13.1. Physical-interruption source `N_T`

The authors need a source-weighted pointwise estimate for targets whose comparison lifetime is shorter than `r` in both directions.

This class should be decomposed by the actual first obstruction:

- true grazing;
- competing hit or first-hit loss;
- endpoint collar exit;
- backward critical termination; and
- any remaining physical boundary mechanism.

The inherited first-exit formula shows that the initial source carries an inverse flow Jacobian. A successful theorem must retain that factor and control the normalized essential height of the initial source, not merely the unweighted boundary flux or the geometric size of the boundary.

A useful target would be

```text
H_M(Z_T^epsilon(r))
 <= C_M epsilon^(-q_T) r^(beta_T),
beta_T>0,
```

or an equivalent signed-current or capacity estimate compatible with the outer reconstruction schedule.

The artificial endpoint collar should either be exhausted with a uniform estimate or shown to contribute a quantitatively vanishing source. It cannot remain an uncontrolled part of `N_T`.

### 13.2. Coarea-compression source `N_D`

The authors need a tail theorem for

```text
sup_s A_hat(x)/A_hat(Phi_{es}x) > D.
```

The optical-sensitivity formula identifies the possible inverse-incidence contribution, but a local logarithmic derivative bound is not yet a transverse, collision-uniform pointwise estimate.

A useful target would be

```text
H_M(Z_D^epsilon(r,D))
 <= C_M epsilon^(-q_D) D^(-eta_D)
    + C_M epsilon^(-q_D') r^(beta_D),
eta_D,beta_D>0,
```

with a legal choice of `D=D(B)` whose cost in the anchor factor `D/beta` is explicitly balanced.

The proof must use the actual physical density and cannot sum a raw number of words or visits.

### 13.3. Sparse same-label occupation source `N_O`

The authors need a pointwise recurrence theorem showing that a large target source cannot repeatedly carry too little occupation of its own exact label.

An integrated ergodic theorem is not sufficient: a pulse may occupy a very small roof interval and still have fixed essential height. The argument must either prove a lower occupation fraction for every large spike or charge low-occupation spikes to a source with vanishing normalized height.

A useful target would be

```text
H_M(Z_O^epsilon(r,D,beta))
 <= C_M epsilon^(-q_O) beta^(eta_O)
    + C_M epsilon^(-q_O') r^(beta_O),
eta_O,beta_O>0,
```

uniformly in collision count, with the loss `D/beta` in the admitted estimate balanced against this decay.

No return-count factor may be introduced.

### 13.4. Exhaustion of spike mechanisms

After estimating the three pieces, the paper should prove at finite count that every target belongs to exactly one paid class and then take the ordered height. It is not enough to show that each fixed physical mechanism is small after a mechanism-dependent collision limit.

The final theorem should give a single bound of the form

```text
H_M(Z_T+Z_D+Z_O)
 <= explicit vanishing function of
    epsilon,r,D,beta and the outer reconstruction band.
```

### 13.5. Reconnect to the signed forcing

The bidirectional signed forcing remains the sharpest post-projection criterion. Once the failure source is controlled, the paper should state explicitly how the occupation localization implies vanishing of that forcing and then the original scalar endpoint.

The proof should preserve projection before positive parts. It should not return to an uncontrolled sum of positive sheetwise contributions.

### 13.6. Give one complete outer schedule

After deriving failure-source rates, the authors should state one explicit legal schedule for

```text
epsilon(B),
r(B),
D(B),
beta(B),
a(B),
delta(B),
positive gradient cutoffs,
auxiliary bands,
```

and verify every exponent in the required order. No parameter may depend on collision count in a way that bypasses a nonuniform finite-count remainder.

### 13.7. Close the scalar theorem before downstream promotion

Only after `Z -> 0` and the scalar upper endpoint are proved should the manuscript promote:

- uniform roof-kernel convergence;
- unrestricted same-roof ratios;
- forward essential-likelihood convergence;
- point-conditioned actual-return path laws;
- unrestricted path-space total variation or entropy; or
- normalization on zero arithmetic classes.

### 13.8. Obtain independent specialist verification

A submission of this breadth needs independent reconstruction of at least:

- the four-record spectral theorem and finite-peak reference;
- the common physical coarea and Borel-segment disintegrations;
- the endpoint Hessian, optical recurrence, and radial monotonicity;
- the backward-end and critical-volume estimates;
- the positive scalar remainder;
- the two-ended packet theorem;
- the section-decision comparison flow;
- the exact-label occupation anchor; and
- the three failure-source estimates once supplied.

Finite fixtures and source-preservation checks cannot certify these continuum facts.

## 14. Exposition and architecture

The focused ten-page article is substantially clearer than the complete archive and is commendably explicit about its conditional scope. The following distinctions should remain visible in any subsequent version.

1. Physical continuation through a section-decision wall is not continuation through a true singular or first-hit boundary.
2. The comparison flow does not alter the original stopped source or exact-event definition.
3. Exact-label occupation is not pooled occupation of neighboring labels.
4. The inverse coarea-density ratio `D` is a hypothesis of admission, not a globally proved distortion bound.
5. The occupation fraction `beta` is a hypothesis of admission, not a consequence of recurrence already established for all targets.
6. The all-gradient theorem concerns the admitted class; it is not the full critical-core theorem.
7. The packet theorem estimates the admitted two-nongrazing packet itself; the failed packet remains.
8. The three-way partition is source localization, not source decay.
9. Endpoint equivalence is a criterion, not a proof that its criterion is satisfied.
10. Local preview evidence is not exact-SHA remote qualification.
11. Qualification is not mathematical certification.
12. Historical credit and the exact inherited-input boundary should remain explicit.

The full technical archive remains exceptionally large. For journal use, provenance, software qualification, historical variants, and theorem narrative should remain separated. At the same time, every load-bearing inherited theorem used by the focused article must be stated with enough precision for independent checking.

## 15. Significance and venue assessment

Revision 96 contains a genuinely useful new mechanism. Exact-label occupation anchoring can pay a short source pulse by its own original event at other roofs without counting returns. The all-gradient admitted theorem also shows how to avoid the disappearing-annulus defect when a physical continuation class is available. The three-way failure partition converts a diffuse pointwise obstruction into concrete physical questions.

If independently verified, these ideas could be important in singular transport problems where projected densities are assembled from many short physical histories and where section decisions interrupt labels without interrupting the underlying dynamics.

For a strong specialized paper, the authors could potentially organize around the completed occupation-anchor, admitted-core, packet, and failure-localization theorems, with a sharply delimited conditional endpoint application. Such a paper would still need a self-contained significance case and a manageable inherited-input boundary.

At the requested Annals/Acta/Inventiones/JAMS benchmark, however, the governing direction remains incomplete. The three failed admission tests are exactly the mechanisms capable of carrying the unresolved essential-height spike, and no theorem proves their source small. The unrestricted pointwise theorem remains an objective rather than a conclusion.

## 16. Final recommendation

Revision 96 responds seriously and positively to the revision-95 report. It constructs a legitimate physical continuation across section decisions, proves an exact-label occupation anchor without a return-count factor, estimates the admitted positive two-nongrazing packet itself, controls the complete admitted radial core without a lower gradient cutoff, and localizes every remaining target into three disjoint original-source failure mechanisms.

I found no decisive internal error in modules 229--231 at their stated scope, conditional on the inherited inputs.

Nevertheless, the manuscript does not prove that all targets are admitted and does not prove vanishing of the physical-interruption, coarea-compression, or sparse same-label occupation sources. The failure-source criterion is therefore not shown to hold; the bidirectional forcing is not proved zero; unconditional upper-spike persistence is unavailable; the original critical-or-short-residence charge remains open; and the unrestricted pointwise exact-label raw local limit theorem is still unproved.

**I therefore recommend rejection in the present form at the requested Annals/Acta/Inventiones/JAMS benchmark.**
