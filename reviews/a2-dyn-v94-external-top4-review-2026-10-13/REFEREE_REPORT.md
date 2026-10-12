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
**Qualification runs at review freeze:** response `38272339932`; referee-copy `38272356974`; both queued with no conclusion  
**Date:** 13 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, probability, o-minimal-geometry, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 94 is a serious theorem-bearing response to the revision-93 report. It is not a cosmetic rephrasing of the two positive forcing terms isolated there. The three new modules establish new source-specific geometry:

1. a collision-normalized essential-height estimate for every noncritical ancestral entrance having a previously fixed positive gradient and positive total-residence cutoff;
2. an exact identification of the remaining zero-residence entrance charge with the original weighted volume carried by the same short physical segments;
3. a radial-shell transit estimate for target ancestors crossing from gradient scale `b` to `2b` inside a prescribed backward roof window;
4. the optimized bound

   ```text
   C r^(129/256) + C(1+epsilon^(-1)) r^(257/256)
   ```

   for the complete radial-transit target at `b=sqrt(r)`;
5. a signed projected forcing construction which retains physical losses, completed-prefix losses, and high-gradient old-sheet losses before taking a positive upper estimate;
6. domination of both the ramped and sharp signed forcing by the original unrenormalized source; and
7. an exact criterion identifying vanishing of this signed forcing along legal prescribed radii with the original pointwise endpoint.

I found no decisive sign reversal in the projected forcing, no exponent error in the radial-shell optimization, no missing ramp factor in the ancestral comparison, no illicit removal of a positive residence or gradient cutoff before the collision limit, no hidden collision-dependent auxiliary Fourier band, and no use of a physical-word count in the normalized estimates. Subject to the inherited physical-flow, coarea, Borel-segment, positive scalar remainder, critical-volume, backward-end, and positive-cutoff source inputs, modules 223--225 are internally coherent at their stated scope.

The recommendation remains negative because revision 94 still does not prove the governing theorem. The final forcing localization leaves two concentrations unestimated:

```text
zero-residence ancestral entrance concentration,
target-critical source concentration.
```

The radial-shell theorem pays histories which traverse a nontrivial gradient shell. It does not pay histories whose target state remains inside the critical core. The entrance theorem pays every previously fixed positive-residence class and then identifies, rather than eliminates, the zero-residence limit. The signed projected criterion is therefore an exact and useful reduction, but its vanishing hypothesis is not proved.

Accordingly the manuscript still does not establish:

- unconditional upper-spike persistence;
- zero essential-height charge for the original critical-or-short-residence source;
- the upper pointwise half of the exact-label raw local limit;
- the unrestricted pointwise exact-label raw local limit theorem; or
- the downstream unrestricted point-conditioned and essential-likelihood laws.

At the requested benchmark, a manuscript organized around unrestricted pointwise raw inversion must prove the pointwise theorem or be reorganized around a comparably broad completed theorem. Revision 94 considerably narrows the remaining obstruction, but it does not close it.

## 2. Frozen source, chronology, and source identity

Both reviewed revision-94 author refs resolve to

`b672cc3f880052fd461b6a4d6099f92008ba47ba`.

The repository tree at that commit is

`fcda1babe0e8ae2b19939c00df6edaf63e038017`.

The active article is

`papers/A2-DYN-v94-referee-response`.

The source manifest identifies revision 93 as the immediate author baseline:

`d96c956e083bbcd15eb4eb35de17cc57857a9588`,

with frozen paper tree

`ef2f30899784526ad41aac95fe88c7417761e558`.

The revision-94 author commit descends from the controlling revision-93 review commit

`0d59a3035d567286d3bc120117d8ea13bf4d386d`.

The packet preserves 222 inherited core modules and adds exactly:

- `core/223_noncritical_entrance_residence.tex`;
- `core/224_critical_radial_transit_packets.tex`;
- `core/225_signed_projected_forcing_and_endpoint.tex`.

The complete revision-93 article is assembled in the supplement, the v93 root documents are snapshotted, the unchanged v93 sibling remains the inherited claim authority, and both distinct revision-88 variants remain separately preserved. Revision 94 does not overwrite or silently combine the incompatible historical sources.

The present review branch starts directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v94-external-top4-review-2026-10-13/`.

No author manuscript, author revision branch, workflow, prior review, preserved source variant, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The revision-94 workflow is

`.github/workflows/a2-dyn-v94-qualification.yml`.

At review freeze, the two author refs had the following runs:

- response branch: `38272339932`;
- referee-copy branch: `38272356974`.

Both were `queued` with `conclusion=null` at the reviewed SHA. I therefore do not describe revision 94 as having completed fresh exact-SHA remote qualification.

The declared validation contract is meaningful. A completed run is designed to verify:

- the frozen revision-93 paper tree;
- the root-document snapshot;
- the controlling revision-93 report blob;
- preservation of both revision-88 variants;
- byte and mode preservation of inherited files;
- normal and optimized finite-diagnostic agreement;
- native compilation of the focused article and complete supplement;
- recorder coverage of all 225 active cores;
- stabilized references and warning gates; and
- page-by-page PDF geometry.

These checks would establish source identity, finite algebraic consistency, and reproducible assembly. They would not certify the continuum coarea identities, maximal-segment disintegration, radial-shell packet geometry, inherited four-record spectral theorem, positive scalar remainder, or either of the two residual concentration estimates. The manuscript states this limitation correctly.

The authors report an eleven-page local article preview and 16,462 exact-rational finite checks with ordinary/optimized agreement. I treat this as finite-consistency evidence, not as remote qualification or a proof of the continuum theorems.

## 4. Scope of this audit

The complete source contains 225 core modules and a very large inherited supplement. I have not independently reconstructed every historical theorem.

The substantive audit concentrates on:

1. the primary requests in the revision-93 external report;
2. the noncritical ancestral entrance decomposition in module 223;
3. the anchor and variation estimates on positive-residence segments;
4. the dyadic summation over short residence bands;
5. the comparison of entrance traces with the original interior volume on the same segments;
6. the order of the zero-residence and zero-gradient limits;
7. the radial-shell traversal estimate in module 224;
8. the exponent arithmetic at `b=sqrt(r)`;
9. the signed birth-packet estimate;
10. the target-critical core left outside the shell transit;
11. the projected signed derivative and positive forcing in module 225;
12. the target-ancestral pointwise and persistence inequalities;
13. the exact forcing criterion and its logical relation to the original endpoint;
14. preservation of the original exact event, source, guard, labels, arithmetic classes, and normalization;
15. source identity, limit order, and qualification status; and
16. the requested top-four completeness, novelty, and significance standard.

The inherited endpoint field, angular density, positive optical recurrence, Borel maximal-segment map, backward-end local estimate, critical-volume layer cake, positive-cutoff inverse-gradient source theorem, fixed-width bad-source theorem, and positive scalar remainder are treated as source-pinned inputs. Their interfaces with the new proofs are checked here. This report does not convert those inputs into independently certified theorems.

## 5. The governing pointwise assertion

The manuscript retains the uniform pointwise exact-label target

```text
sup_{R, 1<=n<=m, k in Z^2}
esssup_{t in C_{m,R,n,k}(M)}
|m^2 p_{n,R}(k,m,t) - L_{m,R}(k_1,k_2,t,n)| -> 0.
```

Write

```text
P = m^2 p,
G = L,
f = P-G.
```

The historical positive scalar remainder gives the pointwise lower half

```text
[G-P]_+ -> 0.
```

The unresolved part is the upper half

```text
[P-G]_+ -> 0.
```

Revision 94 studies this upper half through the original positive source before taking absolute roof increments. The new signed forcing is substantially more precise than the pre-projection sum of positive sheetwise terms used in revision 93. Nevertheless, the paper itself leaves the forcing-zero statement unproved.

This distinction remains decisive. Weak-critical convergence, local mass decay, logarithmic endpoint convergence, finite-roof-norm convergence, and the new radial-shell packet estimate all remain compatible with a high source value concentrated at a zero-residence entrance or inside the target critical core.

## 6. Response to the revision-93 report

Revision 94 addresses the preceding report seriously and in the correct scalar topology.

### 6.1. Ancestral entrance decomposition

**Substantially addressed.** The new source is decomposed by entrance gradient and total residence. Every class with fixed positive entrance gradient and positive total-residence cutoff receives a collision-normalized essential-height estimate. The remaining zero-residence limit is identified with the original weighted volume on the same short segments.

**Not closed.** The resulting zero-residence volume charge is not proved zero.

### 6.2. Critical radial capacity or shell transit

**Substantially addressed.** Module 224 introduces a radial shell and uses the physical radial-growth inequality to force a minimum traversal time. It obtains a complete target-ancestral packet estimate without inserting a word count.

**Not closed.** Histories whose target lies in the critical core and which do not cross the chosen shell remain as a separate target-critical charge.

### 6.3. Signed-current alternative

**Addressed.** Module 225 retains negative physical and prefix contributions through projection and defines a smaller signed forcing rather than summing all pre-projection positive pieces.

### 6.4. Comparison with the original source charge

**Improved.** The ramped and sharp signed forcings are dominated by the original source, and the paper proves an exact endpoint criterion along legal prescribed radii.

**Not a closure theorem.** The criterion's vanishing side is still a hypothesis. It does not show that the original charge or either localized residual vanishes.

### 6.5. Exact limit order

**Respected in the new statements.** Radius, shell scale, positive gradient cutoff, positive residence cutoff, and auxiliary spectral bands are fixed before the collision limit. Auxiliary bands are enlarged afterwards. Critical cutoffs are removed only inside their ordered height, and the reconstruction band remains outermost.

### 6.6. Downstream promotion

**Properly restrained.** No new unrestricted path ratio, path total variation, path entropy, forward essential likelihood, or arithmetic-zero normalization is promoted.

### 6.7. Independent verification

**Not supplied.** Source preservation and finite diagnostics are not an independent specialist reconstruction of the continuum argument.

Thus revision 94 answers most of the requested structural work, but it does not answer the final quantitative request: prove the two residual concentrations vanish.

## 7. Audit of module 223: noncritical ancestral entrances

### 7.1. The entrance object

The module works with the same maximal physical segments and the same original weighted angular density

```text
f_sigma^epsilon = A_sigma W^epsilon,
A_sigma = omega/(4 pi c_* chi).
```

The entrance budget is target-ancestral: an entrance is counted only when its selected segment reaches the target roof. Completed prefixes and later re-entries are not reintroduced as positive births.

This is the correct object for the revision-93 pointwise comparison. It avoids the overcounting that would result from taking all entrance traces independently of the target.

### 7.2. Positive gradient and positive residence

Fix positive entrance-gradient and total-residence cutoffs `rho,delta`. The theorem proves an ordered bound of the form

```text
limsup_m sup_{R,n,k,c}
m^2 ||B_{c,r}^{epsilon,rho,delta,sharp}||_infinity
    <= C_{rho,delta}(r^(1/32)+r).
```

The estimate has two components.

For segments with residence longer than the averaging window, the entrance trace is compared with a positive interior anchor. The full angular variation between the entrance and the anchor is then paid by the positive inverse-gradient source at the fixed cutoff `rho`.

For short positive-residence segments, the proof groups lengths into dyadic bands. The backward-end local estimate contributes the `r^(1/32)` behavior, while the positive-cutoff variation contributes the linear `r` term. The dyadic geometric sum is formed at finite collision count before the collision limsup.

I find this architecture coherent. In particular:

- the trace is not equated with unweighted flux;
- the physical angular density and guard remain present;
- each selected physical interior state is counted through the Borel segment identity, not through an upper bound on the number of words;
- the residence cutoff is fixed before the collision limit; and
- no conclusion at `rho=0` or `delta=0` is inferred from a theorem whose finite-count remainder depends singularly on those cutoffs.

### 7.3. Exact short-segment trace-volume comparison

For the same short segments the module defines:

- an entrance-trace source; and
- the original weighted interior-volume source.

Their difference is controlled by integrating the absolute physical-density variation along the segment. At fixed positive gradient cutoff this variation is bounded by the positive inverse-gradient source. Consequently the ordered zero-residence limits of the trace and volume charges agree.

This is a useful and nontrivial identification. It means the unestimated zero-residence entrance is not an artificial boundary object introduced by the pointwise comparison; it is exactly the concentration already present in the original weighted source on collapsing physical segments.

The proof correctly avoids the false inference that a boundary trace is zero because the corresponding boundary has zero two-dimensional area.

### 7.4. What the theorem does not prove

The equality of two charges does not prove either charge is zero. The module does not establish a collision-uniform modulus converting the small mass of short segments into small essential height.

Moreover, the comparison is proved at every fixed positive gradient cutoff. The inherited finite-count positive-cutoff estimate has a remainder which deteriorates as the cutoff tends to zero. The legal statement therefore takes the collision limit before removing that cutoff. No uniform `rho -> 0` estimate is supplied.

The remaining zero-residence term is thus a genuine pointwise concentration problem, not a bookkeeping defect.

## 8. Audit of module 224: critical radial transit packets

### 8.1. Radial shell geometry

Let the shell run from gradient scale `b` to `2b`, and let

```text
D = sqrt(b^2 + 2 Lambda r).
```

The physical radial-growth inequality gives a lower traversal time of order `b^2` for a history to cross the shell. Therefore a target ancestor which makes such a transit during a backward interval of length `r` must spend a quantitatively controlled amount of roof time in the critical-gradient source.

The module turns this occupation statement into a pointwise target estimate rather than merely an integrated source estimate. This directly addresses the revision-93 request to control histories crossing a critical shell.

### 8.2. The complete packet estimate

The finite-count inequality has the structure

```text
N_{c,r}^{epsilon,b}(t)
 <= C b^(-2) int_{t-r}^t p_{2b}(u) du
    + C(1+epsilon^(-1)) int_{t-r}^t v^{b,D}(u) du.
```

The first term is paid by the critical-volume estimate. The second is paid by the positive inverse-gradient layer cake over the shell.

After the collision limit, the resulting height bound is

```text
C r b^(alpha-2)
 + C(1+epsilon^(-1)) r D^(alpha-1),
alpha = 129/128.
```

Choosing

```text
b = sqrt(r)
```

gives

```text
r b^(alpha-2) = r^(alpha/2) = r^(129/256),
```

and, since `D` is of order `sqrt(r)`,

```text
r D^(alpha-1) = r^(1+(alpha-1)/2) = r^(257/256).
```

The printed exponents are correct.

### 8.3. Limit order

The shell scale is fixed before the collision limit. The finite-count remainder is not evaluated at a collision-dependent cutoff. Auxiliary spectral bands are enlarged only after the collision limit. The shell may then be selected as a function of the outer prescribed radius, and the reconstruction band remains outermost.

This is the correct quantifier order for the stated theorem.

### 8.4. Signed birth packet

The module also records that a radial-shell birth packet is bounded by a selected submeasure of the original target source. This is consistent with the physical ancestor construction and does not introduce an independent normalization.

### 8.5. The unestimated critical core

The radial theorem controls histories which traverse the shell. It does not control a target history which is already inside `z<2b` and does not produce the required shell crossing in the prescribed backward interval.

That residual appears in module 225 as a target-critical source. The local mass estimate for `z<2b` cannot by itself be promoted to an essential-height estimate. A fixed-height pulse supported on a roof set of vanishing measure remains compatible with all such mass bounds.

Thus the radial packet theorem is genuine progress, but it is not the critical-source charge-zero theorem.

## 9. Audit of module 225: signed projected forcing

### 9.1. The projected signed derivative

The module starts from the finite-count signed derivative of the original prefix source. Schematically,

```text
D R_c^epsilon
 = entrance + positive growth
   - terminal cuts - negative growth.
```

It then separates the high-gradient positive-growth contribution already paid by the noncritical source theorem. The residual signed measure retains negative terms before projection.

This is preferable to taking the positive part separately on every sheet. Jordan decomposition does not commute with projection, so a pre-projection sum of positive pieces may overcount the actual projected positive forcing. Revision 94 explicitly avoids claiming equality between those objects.

### 9.2. Ramped and sharp forcing

The paper defines a ramped forcing `S` and a sharp forcing `S_sharp`. At finite collision count they satisfy

```text
0 <= S <= S_sharp <= R_c^epsilon.
```

The first inequality follows from retaining only the positive part of the appropriate projected signed forcing. The final domination follows because the forcing is built from the same original target-ancestral source and does not add later re-entries or unrelated completed prefixes.

I find this comparison credible at the stated source level.

### 9.3. Pointwise upper comparison

The central inequality has the form

```text
R_c^epsilon(t)
 <= backward_average_r R_c^epsilon(t)
    + S_{c,r}^epsilon(t)
    + C(1+epsilon^(-1)) int_{t-r}^t v^rho(u) du.
```

The last term is the paid noncritical positive growth. The radius is prescribed before the collision limit. The left side is the actual source value at the target roof, not an average in the starting roof.

A corresponding sharp inequality gives backward persistence unless the sharp signed forcing is large. This is a genuine pointwise statement.

### 9.4. Physical localization of the forcing

The sharp forcing is localized by three pieces:

1. a target-critical core;
2. a noncritical entrance term which reduces, after positive-cutoff analysis, to the zero-residence charge; and
3. a radial-transit packet already controlled by module 224.

This is substantially sharper than the revision-93 pair of pre-projection positive forcing charges. It identifies exactly which physical mechanisms still permit a nonpersistent high source value.

### 9.5. The exact endpoint criterion

The manuscript obtains

```text
E_M
 <= C_M B^(-1/192)
    + S_{epsilon(B),M}(r)
    + C(1+epsilon(B)^(-1)) r.
```

It then proves that the original pointwise endpoint holds if and only if the signed forcing vanishes along a legal family of prescribed radii; the same holds for the sharp forcing.

The sufficiency direction follows from the displayed upper comparison and the historical lower pointwise law.

The necessity direction uses

```text
S_sharp <= original source
```

and the positive scalar remainder: if the original pointwise error vanishes, the original positive source vanishes in the same ordered limit, hence so does the forcing.

The logic is correct. The result is useful because the equivalent object has a more physical signed localization than the original source charge.

It is nevertheless a criterion, not a proof of the endpoint. The manuscript does not establish the forcing-zero hypothesis.

## 10. The two residual concentrations

### 10.1. Zero-residence ancestral entrance

For every fixed positive residence cutoff, the entrance height is controlled. The limit as residence tends to zero is identified with the original weighted short-segment volume charge.

What remains missing is a source-specific theorem of the form

```text
Z_{epsilon,M}(delta)
 <= C_M epsilon^(-q) delta^beta,
beta>0,
```

or another estimate forcing the ordered essential height to vanish.

An interval-mass bound is insufficient. The proof needs a collision-uniform anti-concentration mechanism, a persistence result for short-segment source values, a signed cancellation, or regularity above the one-dimensional embedding threshold.

### 10.2. Target-critical core

The radial transit theorem controls shell-crossing histories. The residual target-critical source consists of histories reaching the target roof within a collapsing gradient core without generating a paid transit packet in the prescribed backward window.

What remains missing is a theorem of the form

```text
T_{epsilon,M}(q)
 <= C_M epsilon^(-q_0) q^eta,
eta>0,
```

or an equivalent signed-current estimate.

The critical-volume exponent `129/128` is favorable at the mass level, but it does not itself control pointwise height. The proof must connect a high target value either to a shell crossing of controlled capacity, to a critical entrance trace of controlled height, or to a projected signed cancellation.

### 10.3. Why the two terms cannot be dismissed

Both mechanisms can create a high source value on a roof set whose measure collapses. Such a sequence is invisible to finite `L^p`, weak-critical, logarithmic, and local-mass estimates while retaining nonzero essential height.

They are therefore exactly the remaining pointwise obstruction, not merely technical remainder terms after the theorem.

## 11. Order of limits

The new arguments generally respect the required order:

1. form all physical sources, segment sums, shell packets, and signed projections at finite collision count;
2. fix the prescribed radius, positive gradient cutoff, positive residence cutoff, shell scale, and auxiliary spectral bands;
3. take the collision limsup and the uniform physical/arithmetic suprema;
4. enlarge auxiliary bands only afterwards;
5. remove positive gradient or residence cutoffs only inside their ordered height statements; and
6. send the reconstruction band to infinity last.

This order is essential. The positive-cutoff inverse-gradient theorem contains a finite-count remainder which deteriorates as the cutoff tends to zero. A cutoff selected directly as a function of collision count would not prove the stated theorem.

The paper correctly refrains from making that interchange.

## 12. Claims which remain unproved

The manuscript correctly leaves unproved:

- zero height of the complete noncritical zero-residence inlet;
- zero height of the full target-critical core;
- zero signed projected forcing;
- unconditional upper-spike persistence;
- zero original critical-or-short-residence source charge;
- the upper pointwise exact-label raw local limit;
- the full pointwise exact-label raw local limit theorem;
- a collision-uniform projected Hölder modulus obtained by summing sheetwise moduli;
- strong raw convergence at the critical exponent in a topology embedded in `L-infinity`;
- unrestricted uniform same-roof kernel convergence;
- path-space total variation or path-space entropy convergence;
- unrestricted forward essential-likelihood convergence;
- normalization of arithmetic zero classes;
- an unnormalized growing-window theorem;
- independent human specialist approval; and
- a formal proof certificate.

The active status and manifest files represent these boundaries accurately.

## 13. No decisive internal error found in the new modules

Within the stated inherited-input framework, I did not find:

- a sign error at an interior prefix cut;
- a reversal between entrance and exit traces;
- a lost physical angular-density or coarea factor;
- an incorrect radial shell traversal exponent;
- an illegal use of the critical-volume theorem as a pointwise theorem;
- a collision-dependent positive cutoff inserted before the collision limit;
- a word-count multiplier hidden in the source estimate;
- a promotion of the sheetwise half-Hölder modulus to a complete projected modulus;
- an assertion that zero area of a critical set removes its directional trace;
- a false equivalence between pre-projection positive pieces and the projected Jordan positive part;
- an unjustified claim that the forcing-zero criterion has already been verified; or
- an unrestricted downstream normalization on reference-zero arithmetic classes.

This is a positive assessment of the internal interfaces I audited. It is not independent certification of all 225 modules or of the inherited spectral and coarea pipeline.

## 14. What a successful next revision must prove

The next revision should concentrate on the two remaining scalar concentrations. Further reciprocal, posterior, entropy, or finite-roof-norm consequences will not close the pointwise theorem.

### 14.1. Eliminate the zero-residence inlet

Use the exact trace-volume identity of module 223 to prove that the original weighted source on collapsing physical segments has vanishing collision-normalized essential height.

A successful estimate must act on the original source and may take one of the following forms:

- a residence-shell persistence theorem;
- a collision-uniform maximal inequality for short segments;
- a Carleson or capacity estimate for entrance traces;
- a projected signed cancellation across paired short segments; or
- a regularity estimate above the one-dimensional pointwise embedding threshold with norm tending to zero.

It is not enough to prove another fixed-interval mass bound or another finite `L^p` estimate.

### 14.2. Eliminate the target-critical core

Extend the radial-shell mechanism to histories which remain inside the target core. A high target-critical value should be forced into at least one quantitatively controlled event:

- a backward shell crossing;
- a critical entrance trace;
- a positive radial-growth packet of controlled capacity;
- or a projected signed-current contribution admitting a collision-uniform bound.

The required output is a positive power of the critical scale in normalized essential height, not merely in integrated mass.

### 14.3. Preserve projected cancellation

Any new estimate should continue to work with the projected signed current where possible. Summing positive sheetwise contributions before projection may destroy the cancellation which revision 94 has correctly retained.

If a positive majorant is unavoidable, the manuscript must show quantitatively that the overcount is harmless at the collision-normalized scale.

### 14.4. Produce rates compatible with the outer reconstruction band

A sufficient package would be

```text
Z_{epsilon,M}(r) <= C_M epsilon^(-q_1) r^beta_1,
T_{epsilon,M}(r) <= C_M epsilon^(-q_2) r^beta_2,
```

with positive `beta_1,beta_2` and finite exponents `q_1,q_2`.

One could then choose a legal prescribed radius `r(B)` after fixing the reconstruction band, while keeping `r(B)` fixed during the collision limit and sending `B` to infinity last.

### 14.5. Close the scalar theorem before further promotion

Only after the forcing-zero theorem is proved should the manuscript promote:

- uniform roof kernel convergence;
- unrestricted same-roof ratios;
- forward essential-likelihood convergence; or
- actual-return point-conditioned path laws.

Revision 92 already records the strongest finite-roof-norm consequences available without scalar upper closure.

### 14.6. Obtain independent specialist verification

A submission of this breadth needs independent reconstruction of at least:

- the four-record spectral theorem and finite-peak reference;
- the common coarea and Borel-segment disintegrations;
- the positive optical recurrence and trace conventions;
- the backward-end and critical-volume local estimates;
- the positive scalar remainder; and
- the new radial-shell and signed projected forcing arguments.

Source identity and finite diagnostics are valuable but are not substitutes for mathematical verification.

## 15. Exposition and architecture

The focused article is concise and materially clearer than the complete archive. Several points should remain explicit in any subsequent version.

1. Every summary of the endpoint criterion should say that forcing-zero is equivalent to the pointwise theorem but has not been proved.
2. The zero-residence entrance identity should not be described as decay; it is an exact identification of the remaining charge.
3. The radial-shell theorem should always distinguish the paid transit packet from the unestimated target-critical core.
4. The distinction between integrated critical mass and critical essential height should remain visible in theorem statements.
5. The signed projected forcing should be distinguished from the sum of pre-projection positive sheetwise terms.
6. The fixed-positive-cutoff quantifiers and the deterioration of finite-count remainders as the cutoff vanishes should be stated near every ordered limit.
7. Historical credit for the optical recurrence, Borel segment map, critical residue, one-sided lower law, and earlier finite-norm theorems should remain explicit.
8. The queued exact-SHA workflow status should be resolved before any claim of completed remote qualification.
9. Provenance and source-preservation material should remain supplementary rather than carrying the principal theorem narrative.

These are exposition points. They do not alter the recommendation.

## 16. Significance and venue assessment

Revision 94 contains more substantial new geometry than revision 92 and a sharper closure architecture than revision 93. The noncritical entrance theorem, exact zero-residence trace-volume identity, radial-shell transit packet, and signed projected forcing may be reusable in other singular transport problems.

If independently verified, this material could form an important component of a strong specialized paper on pointwise inversion and singular source transport in dispersing billiards. The exact forcing criterion is also a meaningful structural result because it replaces a larger pre-projection positive majorant by a projected signed object tied to the target's actual ancestors.

At the requested four-journal benchmark, however, the current manuscript must deliver either:

- the unrestricted pointwise theorem retained as its governing assertion; or
- a self-contained completed theorem of comparably broad significance, with the paper reorganized around that result.

The two residual concentrations are precisely the mechanisms capable of sustaining a nonpersistent upper spike. Since neither is estimated, the central theorem remains open. The reduction is strong, but it is still a reduction.

## 17. Final recommendation

Revision 94 responds seriously and positively to the revision-93 report. It proves new noncritical entrance control, identifies the exact zero-residence entrance object, establishes a radial-shell transit estimate with correct exponent arithmetic, preserves signed cancellation through projection, and derives an exact forcing criterion for the original pointwise endpoint.

I found no decisive internal error in modules 223--225 at their stated scope, conditional on the inherited inputs.

Nevertheless, the zero-residence entrance concentration and target-critical source concentration are not proved to vanish. The signed forcing is therefore not proved zero, unconditional upper-spike persistence is unavailable, the original essential-height charge remains open, and the unrestricted pointwise exact-label raw local limit theorem is still unproved.

**I therefore recommend rejection in the present form at the requested Annals/Acta/Inventiones/JAMS benchmark.**
