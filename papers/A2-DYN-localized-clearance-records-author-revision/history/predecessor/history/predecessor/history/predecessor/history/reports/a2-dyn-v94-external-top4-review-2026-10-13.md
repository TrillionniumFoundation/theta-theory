# External top-four referee report on A2-DYN revision 94

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v94-referee-response-2026-10-12`, `revision/a2-dyn-v94-referee-copy-2026-10-12`  
**Reviewed author commit:** `b672cc3f880052fd461b6a4d6099f92008ba47ba`  
**Reviewed repository tree:** `fcda1babe0e8ae2b19939c00df6edaf63e038017`  
**Active manuscript directory:** `papers/A2-DYN-v94-referee-response`  
**Canonical revision identity:** `a2-dyn-v94-radial-entrance-signed-forcing-2026-10-12`  
**Active mathematical source:** 225 numbered core modules; revision 94 adds modules 223--225  
**Immediate author baseline:** revision 93 at `d96c956e083bbcd15eb4eb35de17cc57857a9588`  
**Frozen revision-93 paper tree:** `ef2f30899784526ad41aac95fe88c7417761e558`  
**Controlling external report:** `reviews/a2-dyn-v93-external-top4-review-2026-10-12/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `0d59a3035d567286d3bc120117d8ea13bf4d386d` / `7625de487f043ac21dc59fe7d98639284ed8736a`  
**Qualification runs at final review freeze:** response `38273595749`; referee-copy `38273606374`; both queued with no conclusion  
**Date:** 13 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, probability, o-minimal-geometry, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 94 is a serious theorem-bearing response to the revision-93 report. It is not a cosmetic restatement of the two forcing terms isolated there. The new modules establish:

1. collision-normalized essential-height control for every noncritical ancestral entrance with previously fixed positive gradient and positive total-residence cutoffs;
2. an exact identification of the remaining zero-residence entrance charge with the original weighted volume on the same short physical segments;
3. a radial-shell transit estimate for target ancestors crossing from gradient scale `b` to `2b` in a prescribed backward roof window;
4. the optimized complete transit estimate

   ```text
   C r^(129/256) + C(1+epsilon^(-1)) r^(257/256)
   ```

   at `b=sqrt(r)`;
5. a signed projected forcing which retains physical losses, completed-prefix losses, and high-gradient old-sheet losses before taking a positive upper estimate;
6. domination of the ramped and sharp forcings by the original unrenormalized source; and
7. an exact criterion equating forcing-zero along legal radii with the original pointwise endpoint.

I found no decisive sign error in the projected balance, no exponent error in the shell optimization, no missing ramp factor in the ancestral comparison, no illicit collision-dependent cutoff, no hidden word-count multiplier in the normalized estimates, and no incorrect promotion of sheetwise regularity to projected regularity. Subject to the inherited physical-flow, coarea, Borel-segment, positive scalar remainder, critical-volume, backward-end, and positive-cutoff inputs, modules 223--225 are internally coherent at their stated scope.

The recommendation remains negative because the governing theorem is still not proved. Two concentrations remain unestimated:

```text
zero-residence ancestral entrance concentration,
target-critical source concentration.
```

The radial-shell theorem pays histories which traverse a nontrivial gradient shell; it does not pay histories remaining inside the target critical core. The entrance theorem pays all fixed positive-residence classes and then identifies, rather than eliminates, the zero-residence limit. The signed criterion is therefore an exact and useful reduction, but its vanishing hypothesis is not established.

Consequently the manuscript still does not prove unconditional upper-spike persistence, zero essential-height charge for the original exceptional source, the upper pointwise half, or the unrestricted pointwise exact-label raw local limit theorem.

At the requested benchmark, a paper organized around unrestricted pointwise raw inversion must prove that theorem or be reorganized around a comparably broad completed theorem. Revision 94 sharply narrows the obstruction but does not close it.

## 2. Frozen source and chronology

Both author refs resolve to

`b672cc3f880052fd461b6a4d6099f92008ba47ba`,

with repository tree

`fcda1babe0e8ae2b19939c00df6edaf63e038017`.

The active article is

`papers/A2-DYN-v94-referee-response`.

The source manifest pins revision 93 at

`d96c956e083bbcd15eb4eb35de17cc57857a9588`,

with paper tree

`ef2f30899784526ad41aac95fe88c7417761e558`.

The v94 author commit descends from the controlling v93 review commit. The packet preserves 222 inherited cores and adds exactly:

- `core/223_noncritical_entrance_residence.tex`;
- `core/224_critical_radial_transit_packets.tex`;
- `core/225_signed_projected_forcing_and_endpoint.tex`.

The full preceding article is assembled in the supplement; the v93 root documents are snapshotted; the unchanged v93 sibling remains the inherited claim authority; and the two v88 variants remain distinct.

The review branch starts directly from the reviewed author SHA and adds only this report. No manuscript source, author branch, workflow, prior review, preserved variant, or unrelated path is intentionally modified.

## 3. Qualification evidence and boundary

At final review freeze the exact-SHA workflow runs were:

- response: `38273595749`;
- referee-copy: `38273606374`.

Both were `queued` with `conclusion=null`. I therefore do not describe v94 as having completed remote qualification.

The validation contract is meaningful: it pins the v93 tree, root snapshot, controlling report and both v88 variants; checks inherited bytes and modes; compares ordinary and optimized fixtures; compiles the article and complete supplement; requires coverage of all 225 cores; and checks references, warning gates, and PDF geometry.

Those checks establish source identity, finite consistency, and reproducible assembly. They do not certify the continuum coarea identities, maximal-segment disintegration, radial-shell packet geometry, inherited four-record spectral theorem, positive scalar remainder, or the two residual concentration estimates.

The reported eleven-page local preview and 16,462 exact-rational checks are finite-consistency evidence, not mathematical certification.

## 4. Scope of this audit

The full source contains 225 cores and a very large inherited supplement. I have not independently reconstructed every historical theorem. The substantive audit concentrates on:

- the requests in the v93 report;
- noncritical entrance decomposition and positive-residence control;
- short-residence dyadic summation;
- entrance-trace/original-volume comparison;
- zero-residence and zero-gradient limit order;
- radial-shell traversal and exponent arithmetic;
- signed birth packets and target-critical residuals;
- projected signed forcing and persistence;
- the exact endpoint criterion;
- preservation of exact events, labels, guard, arithmetic classes, and normalization; and
- the requested top-four completeness and significance standard.

Inherited spectral, coarea, Borel-segment, local-source, and scalar-remainder statements are treated as source-pinned inputs. Their interfaces are checked; they are not independently certified here.

## 5. Governing pointwise assertion

The target remains

```text
sup_{R,1<=n<=m,k in Z^2}
esssup_{t in C_{m,R,n,k}(M)}
|m^2 p_{n,R}(k,m,t)-L_{m,R}(k_1,k_2,t,n)| -> 0.
```

Writing `P=m^2p` and `G=L`, the historical positive scalar remainder gives the pointwise lower half

```text
[G-P]_+ -> 0.
```

The unresolved half is

```text
[P-G]_+ -> 0.
```

Revision 94 attacks this upper half through the original positive source and a signed projected derivative. This is the correct topology. Nevertheless, the forcing-zero theorem remains open.

Weak-critical convergence, local mass decay, logarithmic convergence, finite-roof-norm convergence, and shell-transit decay all permit high values concentrated at a zero-residence entrance or inside the target critical core.

## 6. Response to the v93 report

### 6.1. Entrance decomposition

**Substantially addressed.** Every class with fixed positive entrance gradient and positive total residence receives an essential-height estimate. The residual zero-residence trace is identified with the original weighted short-segment volume.

**Not closed.** That volume charge is not proved zero.

### 6.2. Critical shell capacity

**Substantially addressed.** Module 224 forces a quantitative shell traversal time and converts it into a complete target-ancestral packet estimate.

**Not closed.** The target-critical core which does not produce the paid shell crossing remains.

### 6.3. Signed-current route

**Addressed.** Module 225 retains negative contributions through projection and defines a smaller forcing than the sum of pre-projection positive sheetwise pieces.

### 6.4. Relation to the original charge

**Improved.** The forcing is dominated by the original source and gives an exact endpoint criterion.

**Still conditional.** Its vanishing is not proved.

### 6.5. Limit order

**Respected.** Radius, shell, positive cutoffs and auxiliary bands are fixed before collision limits; auxiliary bands are enlarged afterwards; reconstruction `B` is outermost.

### 6.6. Downstream laws

**Properly restrained.** No unrestricted path ratio, path total variation, path entropy, essential likelihood, or zero-class normalization is promoted.

### 6.7. Independent verification

**Not supplied.** Finite diagnostics and source preservation are not an independent specialist reconstruction.

## 7. Module 223: noncritical ancestral entrances

The module uses the same maximal physical segments and original weighted angular density

```text
f_sigma^epsilon=A_sigma W^epsilon,
A_sigma=omega/(4 pi c_* chi).
```

The entrance object is genuinely target-ancestral: an entrance is counted only when its selected segment reaches the target roof. Completed prefixes and later re-entries are not recreated as births.

For fixed positive gradient and residence cutoffs `rho,delta`, the theorem proves

```text
limsup_m sup_{R,n,k,c}
m^2 ||B_{c,r}^{epsilon,rho,delta,sharp}||_infinity
 <= C_{rho,delta}(r^(1/32)+r).
```

Long-residence segments are paid by an interior anchor plus positive variation. Short positive-residence segments are summed through dyadic bands. The backward-end estimate supplies `r^(1/32)` and the positive-cutoff inverse-gradient source supplies the linear term.

The argument correctly keeps the physical angular density and guard, uses the Borel segment identity rather than a word count, fixes the cutoffs before the collision limit, and does not infer a theorem at zero cutoff from a remainder which deteriorates there.

The module then compares the entrance trace on short segments with the original weighted interior volume on exactly the same segments. Their difference is paid by absolute physical-density variation at fixed positive gradient cutoff. Hence the ordered zero-residence trace charge equals the ordered zero-residence original-volume charge.

This is a useful identification: the residual entrance is not an artificial boundary term. It is the original source concentration on collapsing physical segments.

However, equality does not imply vanishing. No collision-uniform modulus converts the small mass of those segments into small essential height. The cutoff is removed only after the collision limsup; no uniform `rho -> 0` estimate is obtained.

## 8. Module 224: critical radial transit packets

Let the shell run from `b` to `2b`, and put

```text
D=sqrt(b^2+2 Lambda r).
```

Radial growth gives a lower traversal time of order `b^2`. A target ancestor crossing the shell in the backward window must therefore carry a controlled amount of critical-gradient occupation.

The finite-count estimate has the structure

```text
N_{c,r}^{epsilon,b}(t)
 <= C b^(-2) int_{t-r}^t p_{2b}(u) du
  + C(1+epsilon^(-1)) int_{t-r}^t v^{b,D}(u) du.
```

After the collision limit this yields

```text
C r b^(alpha-2)
 + C(1+epsilon^(-1)) r D^(alpha-1),
alpha=129/128.
```

At `b=sqrt(r)`,

```text
r b^(alpha-2)=r^(129/256),
r D^(alpha-1)=O(r^(257/256)).
```

The exponent arithmetic is correct. The shell scale is fixed before the collision limit, and no collision-dependent cutoff or word-count factor is introduced.

The theorem pays shell-crossing histories. It does not control a history already inside `z<2b` which does not generate the required crossing in the prescribed window. That target-critical residual is explicitly retained in module 225. Critical mass estimates alone do not imply its height vanishes.

## 9. Module 225: signed projected forcing

At finite count the source derivative has the schematic form

```text
D R_c^epsilon
 = entrance + positive growth
   - terminal cuts - negative growth.
```

The module retains these signs through projection and removes the already-paid high-gradient positive growth. This is preferable to summing positive sheetwise pieces before projection: Jordan decomposition need not commute with projection.

The ramped and sharp forcings satisfy

```text
0 <= S <= S_sharp <= R_c^epsilon.
```

The pointwise comparison is

```text
R_c^epsilon(t)
 <= backward_average_r R_c^epsilon(t)
  + S_{c,r}^epsilon(t)
  + C(1+epsilon^(-1)) int_{t-r}^t v^rho(u) du.
```

A sharp version gives backward persistence unless the sharp forcing is large. The radius is prescribed before the collision limit, and the left side is the actual target value rather than an averaged starting-roof quantity.

The sharp forcing is localized into:

1. a target-critical core;
2. a noncritical entrance term reducing to the zero-residence charge; and
3. the radial-transit packet paid in module 224.

This is materially sharper than the v93 pre-projection forcing pair.

The final estimate is

```text
E_M
 <= C_M B^(-1/192)
  + S_{epsilon(B),M}(r)
  + C(1+epsilon(B)^(-1)) r.
```

Sufficiency of forcing-zero follows from this estimate and the historical lower law. Necessity follows from `S_sharp<=original source` and the positive scalar remainder. The equivalence is logically correct and physically informative.

It remains a criterion, not a proof. The manuscript does not establish the forcing-zero side.

## 10. The two residual concentrations

### 10.1. Zero-residence inlet

For every fixed positive residence cutoff the entrance is controlled. The limit as residence collapses is exactly the original weighted source on the same short segments.

A successful closure needs a bound such as

```text
Z_{epsilon,M}(delta)
 <= C_M epsilon^(-q) delta^beta,
beta>0,
```

or another mechanism forcing the ordered essential height to zero. Another fixed-interval mass or finite-`L^p` estimate is insufficient.

### 10.2. Target-critical core

The shell theorem controls transit but not histories staying inside the target core. Closure needs a bound such as

```text
T_{epsilon,M}(q)
 <= C_M epsilon^(-q0) q^eta,
eta>0,
```

or an equivalent signed-current estimate.

A high target-critical value must be forced into a backward shell crossing, a controlled critical entrance trace, a positive radial packet of controlled capacity, or a projected cancellation. Integrated critical mass alone does not suffice.

### 10.3. Why these terms are decisive

Either mechanism may support a fixed-height pulse on a roof set of vanishing measure. Such pulses are invisible to all established finite norms and mass bounds while retaining nonzero essential height. These are therefore the pointwise obstruction itself, not harmless remainders after the theorem.

## 11. Limit order

The new proof respects the necessary order:

1. finite-count physical sources, segment sums, shell packets and signed projections;
2. fixed radius, positive cutoffs, shell scale and auxiliary bands;
3. collision limsup and uniform physical/arithmetic suprema;
4. auxiliary-band enlargement;
5. cutoff removal only in ordered height; and
6. reconstruction `B` last.

This matters because the positive-cutoff finite-count remainder deteriorates as the cutoff tends to zero. A cutoff chosen as a function of collision count would not prove the theorem.

## 12. Claims still unproved

The manuscript correctly leaves unproved:

- zero height of the noncritical zero-residence inlet;
- zero height of the target-critical core;
- zero signed projected forcing;
- unconditional upper-spike persistence;
- zero original exceptional-source charge;
- the upper pointwise exact-label raw local limit;
- the full pointwise exact-label raw LLT;
- a projected Hölder modulus obtained by summing sheetwise moduli;
- a vanishing norm above the one-dimensional pointwise embedding threshold;
- unrestricted uniform same-roof kernel convergence;
- path-space total variation or entropy;
- unrestricted essential-likelihood convergence;
- arithmetic-zero normalization;
- an unnormalized growing-window theorem;
- independent human specialist approval; and
- a formal proof certificate.

The active status files represent these boundaries accurately.

## 13. Internal-consistency assessment

Within the stated inherited-input framework I found no:

- sign error at an interior prefix cut;
- reversal of entrance and exit traces;
- lost angular-density or coarea factor;
- erroneous shell exponent;
- promotion of critical mass to critical height;
- illegal cutoff/collision-limit interchange;
- word-count multiplier hidden in a normalized estimate;
- promotion of sheetwise Hölder regularity to projected regularity;
- deletion of critical trace because its area is zero;
- identification of pre-projection positive pieces with the projected Jordan positive part;
- assertion that forcing-zero has already been proved; or
- unrestricted normalization on reference-zero classes.

This is not independent certification of all inherited mathematics.

## 14. Requirements for a successful next revision

### 14.1. Eliminate the zero-residence inlet

Use the exact trace-volume identity to prove that the original weighted source on collapsing segments has vanishing normalized essential height. Plausible routes include a residence-shell persistence theorem, a short-segment maximal inequality, a Carleson/capacity estimate, a projected signed cancellation, or regularity above the pointwise embedding threshold with a vanishing norm.

### 14.2. Eliminate the target-critical core

Extend the shell mechanism to histories remaining inside the core. A high target value must imply a controlled shell crossing, critical entrance trace, radial packet, or signed-current contribution.

### 14.3. Preserve projected cancellation

Do not revert to an uncontrolled sum of positive sheetwise terms. If a positive majorant is used, prove quantitatively that projection overcount is harmless.

### 14.4. Produce rates compatible with `epsilon(B)`

A sufficient package would be

```text
Z_{epsilon,M}(r)<=C_M epsilon^(-q1) r^beta1,
T_{epsilon,M}(r)<=C_M epsilon^(-q2) r^beta2,
```

with positive `beta1,beta2`. A legal `r(B)` can then be fixed during each collision limit and sent to zero only with outer `B`.

### 14.5. Close the scalar theorem before further promotion

Only after forcing-zero should the paper promote uniform roof kernels, unrestricted same-roof ratios, forward essential likelihood, or actual-return point-conditioned laws.

### 14.6. Obtain independent specialist verification

At minimum, independent audits are needed for the four-record spectral theorem, coarea/Borel disintegrations, optical recurrence and traces, backward-end and critical-volume estimates, positive scalar remainder, and the new shell/forcing arguments.

## 15. Exposition and significance

The focused article is clearer than the complete archive. Future versions should continue to state explicitly that:

- forcing-zero is equivalent to the endpoint but unproved;
- zero-residence identification is not decay;
- shell transit is distinct from the target-critical core;
- critical mass is not critical height;
- projected signed forcing is not a pre-projection positive sum; and
- all zero-cutoff limits occur only after collision limits.

Revision 94 contains more substantial geometry than v92 and a sharper closure architecture than v93. If independently verified, the entrance theorem, trace-volume identity, radial packet, and signed forcing could form an important part of a strong specialized paper on singular source transport in dispersing billiards.

At the requested four-journal benchmark, however, the two mechanisms capable of sustaining a nonpersistent upper spike remain unestimated. The reduction is strong, but it is still a reduction.

## 16. Final recommendation

Revision 94 responds seriously and positively to the preceding report. It proves noncritical entrance control, identifies the exact zero-residence object, establishes a radial-shell transit theorem with correct exponent arithmetic, preserves signed cancellation through projection, and derives an exact criterion for the original endpoint.

I found no decisive internal error in modules 223--225 at their stated scope, conditional on the inherited inputs.

Nevertheless, the zero-residence entrance concentration and target-critical source concentration are not proved to vanish. The signed forcing is not proved zero, unconditional upper-spike persistence is unavailable, the original essential-height charge remains open, and the unrestricted pointwise exact-label raw local limit theorem is still unproved.

**I therefore recommend rejection in the present form at the requested Annals/Acta/Inventiones/JAMS benchmark.**
