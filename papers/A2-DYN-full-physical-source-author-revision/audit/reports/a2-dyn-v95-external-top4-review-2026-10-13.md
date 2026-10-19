# External top-four referee report on A2-DYN revision 95

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v95-referee-response-2026-10-13`, `revision/a2-dyn-v95-referee-copy-2026-10-13`  
**Reviewed author commit:** `be6116aab636b8afb3cceb834e10cb7559c1d992`  
**Reviewed repository tree:** `d5f0afd04d3d6889770666b8894ab45835afa4a7`  
**Active manuscript directory:** `papers/A2-DYN-v95-referee-response`  
**Canonical revision identity:** `a2-dyn-v95-two-ended-radial-source-2026-10-13`  
**Active mathematical source:** 228 numbered core modules; revision 95 adds modules 226--228  
**Immediate author baseline:** revision 94 at `b672cc3f880052fd461b6a4d6099f92008ba47ba`  
**Frozen revision-94 paper tree:** `f0788580c4fab60cdcef0277f8d92052fd12dd15`  
**Controlling external report:** `reviews/a2-dyn-v94-external-top4-review-2026-10-13/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `8dc6ce40f455a033b0473758cf1a85d61dbbf8a1` / `e8804c69db02415d59d244529ceb6d422fa4ddde`  
**Qualification runs at review freeze:** response `38280354990`; referee-copy `38280360163`; both queued with no conclusion  
**Date:** 13 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, probability, o-minimal-geometry, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 95 is a mathematically substantive response to the revision-94 report. It does not merely rename the two residual concentrations. The three new modules add the following theorem-bearing mechanisms:

1. a complete finite-count replacement of the original short-segment source by the smaller of the two physical endpoint traces on each same segment, with a pointwise error paid by the actual positive-cutoff inverse-gradient source;
2. vanishing of the zero-residence charge of every short segment having at least one grazing physical endpoint, at each previously fixed positive entrance or target gradient;
3. an intrinsic two-sided radial anchor for critical targets with sufficient residence on the scale of their own target gradient, without requiring the prescribed shell crossing used in revision 94;
4. an annular essential-height estimate

   ```text
   C q^(129/128) + C(1+epsilon^(-1)) q^(257/128)
   ```

   for the relatively long target-critical class;
5. a proof that relatively thin target segments cannot be born at a critical backward endpoint;
6. a stronger annular estimate for relatively thin segments having a grazing physical endpoint;
7. a forward signed projected balance paired with the backward balance of revision 94;
8. a joint forcing obtained by taking the minimum of the two projected forcings only after projection; and
9. a necessary-and-sufficient criterion relating vanishing of that joint forcing along legal prescribed radii to the original pointwise endpoint.

I found no decisive sign error in the two-ended packet algebra, no exponent error in the intrinsic-anchor estimate, no illicit replacement of a physical segment by a word count, no interchange of a sheetwise minimum with projection, no hidden removal of the positive gradient cutoff before the collision limit, and no promotion of the finite-annulus theorem to a zero-gradient theorem. Subject to the inherited common-segment coarea map, radial-flow estimates, critical-volume bounds, positive-cutoff source theorem, signed-prefix identity, and scalar reconstruction inputs, modules 226--228 are internally coherent at their stated scope.

The recommendation nevertheless remains negative because the governing theorem is still not proved. Revision 95 eliminates only a proper subfamily of the residence-zero obstruction. The short-source charge carried by segments with **two nongrazing physical endpoint traces** remains unestimated. Likewise, the annular theorem controls every previously fixed positive radial scale but does not control concentration in annuli whose scale tends to zero with the collision count. The bidirectional forcing is smaller than the previous backward forcing, but its vanishing is not established.

The manuscript therefore still does not prove:

- zero essential-height charge for the complete original critical-or-short-residence source;
- unconditional prescribed-width persistence of every upper spike;
- the upper pointwise half of the exact-label raw local limit;
- the unrestricted pointwise exact-label raw local limit theorem;
- unrestricted same-roof point-conditioned kernel convergence;
- forward essential-likelihood convergence; or
- the other downstream laws whose unrestricted forms depend on scalar pointwise closure.

At the requested benchmark, a manuscript whose governing objective remains the unrestricted pointwise raw local limit theorem must prove that theorem or be reorganized around a different completed theorem of comparable breadth. Revision 95 is a genuine advance, but it remains a reduction of the pointwise obstruction rather than its elimination.

## 2. Frozen source, chronology, and preservation

Both reviewed author branches resolve to

`be6116aab636b8afb3cceb834e10cb7559c1d992`,

with repository tree

`d5f0afd04d3d6889770666b8894ab45835afa4a7`.

The active paper is

`papers/A2-DYN-v95-referee-response`.

The source manifest pins the immediate author baseline at

`b672cc3f880052fd461b6a4d6099f92008ba47ba`,

with frozen revision-94 paper tree

`f0788580c4fab60cdcef0277f8d92052fd12dd15`.

The revision-95 author commit descends directly from the controlling revision-94 review commit

`8dc6ce40f455a033b0473758cf1a85d61dbbf8a1`.

The packet preserves 225 inherited core modules and adds exactly:

- `core/226_two_ended_short_segment_packets.tex`;
- `core/227_intrinsic_radial_residence_anchors.tex`;
- `core/228_bidirectional_signed_pointwise_forcing.tex`.

The full preceding article is assembled in the technical archive, the revision-94 root documents are snapshotted, the unchanged revision-94 sibling remains the inherited claim authority, both revision-88 variants remain distinct, and historical reports are retained. I found no indication that revision 95 silently overwrites an incompatible historical source or changes the original exact-event target.

The present review branch starts from the exact author SHA and adds only this report under

`reviews/a2-dyn-v95-external-top4-review-2026-10-13/`.

No author manuscript source, author revision branch, workflow, historical review, preserved source variant, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

At review freeze the two exact-SHA workflow runs were:

- response branch: `38280354990`;
- referee-copy branch: `38280360163`.

Both were `queued` with `conclusion=null`. I therefore do not describe revision 95 as having completed fresh remote qualification.

The committed validation contract is meaningful. A completed exact-SHA run is designed to verify:

- the frozen revision-94 paper tree;
- the revision-94 root snapshot and complete prior article;
- the controlling revision-94 report blob;
- preservation of both revision-88 variants;
- byte and executable-mode preservation of inherited sources;
- consistency of inherited claim flags;
- ordinary and optimized finite diagnostics;
- native compilation of the focused article and complete supplement;
- actual recorder coverage of all 228 active core modules;
- stabilized references and warning gates; and
- page-box and render checks.

The recorded local evidence is narrower: a ten-page focused article preview and 4,948 exact-rational fixtures passing in ordinary and optimized Python with identical output. The local record explicitly says that the complete inherited archive was not materialized for that preview.

These checks are useful evidence of source identity, finite algebraic consistency, and reproducible typesetting. They do not certify the continuum coarea disintegration, multiplicity-one segment parametrization, inherited four-record spectral theorem, critical-volume estimates, positive scalar remainder, or the new zero-scale passages. A successful workflow would not change that mathematical boundary.

## 4. Scope of this audit

The complete source contains 228 core modules and a large inherited technical archive. I have not independently reconstructed every historical theorem. The substantive audit concentrates on:

1. the exact requests in the revision-94 external report;
2. the four same-segment quantities in module 226;
3. the per-segment minimum and total-variation error;
4. the grazing-ended zero-residence conclusion;
5. the distinction between fixed positive gradient and gradient zero;
6. the intrinsic two-sided anchor in module 227;
7. the annular exponent arithmetic and finite-count remainder;
8. the relatively thin/relatively long geometric dichotomy;
9. the treatment of forward anchors lying outside an artificial prefix but inside the same physical segment;
10. the forward and backward projected signed measures in module 228;
11. the order in which positive parts and minima are taken;
12. the joint pointwise and persistence comparisons;
13. the endpoint equivalence and legal outer rates;
14. preservation of the original event, guard, labels, source normalization, arithmetic classes, and target topology;
15. source identity and qualification status; and
16. completeness, novelty, self-containedness, and significance at the requested four-journal benchmark.

The inherited Borel segment bijection, physical density, radial growth, derivative bounds, critical-volume layer cake, positive-cutoff source theorem, signed prefix balance, fixed-width bad-source estimate, and positive scalar remainder are treated as source-pinned inputs. Their interfaces with modules 226--228 are checked here. This report is not an independent proof of those inherited inputs.

## 5. Governing pointwise assertion

The original target remains the unrestricted exact-label pointwise statement

```text
sup_{R,1<=n<=m,k in Z^2}
esssup_{t in C_{m,R,n,k}(M)}
|m^2 p_{n,R}(k,m,t)-L_{m,R}(k_1,k_2,t,n)| -> 0.
```

Writing `P=m^2p` and `G=L`, the inherited positive scalar remainder supplies the lower half

```text
[G-P]_+ -> 0.
```

The unresolved half is

```text
[P-G]_+ -> 0.
```

Revision 95 continues to work at the correct topology: actual target values and collision-normalized essential height. It does not replace the objective by a finite-roof norm. This is important and should be retained.

The obstacle remains that a source can have vanishing integrated mass, vanishing finite `L^p` norms, and small mass in every fixed radial annulus while maintaining a nonzero essential-height spike on segments or annuli whose physical scale tends to zero with the collision count. The new results remove several such spike mechanisms but not all of them.

## 6. Response to the revision-94 report

### 6.1. Eliminate the zero-residence inlet

**Genuinely advanced, but not closed.**

Revision 95 proves that at each fixed positive entrance gradient the complete zero-residence charge of every segment with at least one grazing physical endpoint is zero. This includes the previously untreated configuration of a nongrazing entrance followed by a grazing physical exit.

The remaining two-nongrazing packet is not estimated. Since both endpoint traces may stay positive on a sequence of collapsing segments, the original zero-residence source can still retain pointwise height.

### 6.2. Eliminate the target-critical core

**Genuinely advanced, but not closed.**

The intrinsic-anchor theorem controls relatively long target-critical histories in each fixed annulus even when they do not cross the prescribed shell of revision 94. The thin/long dichotomy also proves that a relatively thin segment cannot be born at a critical backward endpoint, and the thin grazing-ended subfamily receives a stronger annular height estimate.

The theorem does not control concentration in annuli whose lower gradient scale tends to zero with the collision count. Nor does it control all relatively thin segments with two nongrazing endpoints.

### 6.3. Preserve projected cancellation

**Addressed and improved.**

The forward and backward balances retain physical and artificial end signs through projection. The minimum is formed only after both projected positive parts are defined. This is strictly preferable to summing sheetwise positive terms or taking the minimum sheet by sheet.

### 6.4. Produce rates compatible with `epsilon(B)`

**Addressed for the newly explicit errors, not for the residual charges.**

The schedule

```text
r(B)=c epsilon(B)^N,
q(B)=sqrt(r(B)),
N>1,
```

pays the explicit linear, annular, and grazing-ended packet errors. No rate is proved for the two-nongrazing packet charge, the disappearing-annulus concentration, or the joint forcing itself.

### 6.5. Close the scalar theorem before downstream promotion

**Respected.**

The manuscript does not promote unrestricted point-conditioned, likelihood, entropy, or arithmetic-zero-class conclusions.

### 6.6. Independent specialist verification

**Not supplied.**

Source preservation, local compilation, and finite fixtures do not replace independent reconstruction of the billiard geometry, coarea conventions, spectral inputs, critical-volume estimates, positive scalar remainder, two-ended packet argument, intrinsic anchor, or bidirectional signed comparison.

## 7. Module 226: two-ended packets on actual short segments

For each physical segment the module defines

```text
F^-_sigma = f_sigma^epsilon(a_sigma+),
F^+_sigma = f_sigma^epsilon(b_sigma-),
M_sigma   = min(F^-_sigma,F^+_sigma).
```

For the same selected family of segments containing the target roof, with length at most `delta` and entrance gradient at least `rho`, it then defines:

```text
Q = current target source,
I = inlet-trace packet,
O = outlet-trace packet,
M = integral of the per-segment minimum.
```

The minimum is taken before summing, but it is taken between the two traces of the **same physical segment**. It is not a minimum between two projected totals and it is not used as a signed cancellation. This distinction is correct.

### 7.1. Finite-count packet error

The theorem proves

```text
|Q-M|(t) <= V(t),
|I-M|(t)+|O-M|(t) <= V(t),
V(t)=C(1+epsilon^(-1)) int_{t-delta}^{t+delta} v^rho(u) du.
```

The per-segment identities are elementary but useful:

```text
|f_sigma(t)-M_sigma|
 <= int_{a_sigma}^{b_sigma}|(f_sigma^epsilon)'|,

(F^-_sigma-M_sigma)+(F^+_sigma-M_sigma)
 = |F^-_sigma-F^+_sigma|.
```

Because every selected segment lies inside `(t-delta,t+delta)` and the inherited Borel parametrization counts its intermediate physical states once, the complete variation sum is paid by the actual `v^rho` source. No raw number of physical words appears.

At fixed positive `rho`, the retained cutoff theorem gives ordered height

```text
H_M(V) <= C(1+epsilon^(-1)) delta.
```

I find this argument coherent, conditional on the inherited common-segment coarea map and derivative estimate.

### 7.2. Equality of the four residence-zero charges

The four selected sources are monotone in the residence threshold. Since their pairwise differences have ordered height tending to zero, the module correctly concludes equality of their ordered zero-residence charges as extended nonnegative numbers.

This is an exact transfer of the obstruction. It does not by itself prove that the common charge is finite or zero.

### 7.3. Grazing-ended elimination

If either physical endpoint is grazing, the corresponding weighted trace is zero and hence the per-segment minimum is zero. Restricting the same variation proof to this Borel family gives

```text
H_M(Q_grazing-ended) <= C(1+epsilon^(-1)) delta.
```

Thus this family's ordered zero-residence charge is zero at each fixed positive entrance gradient. The target-gradient corollary is also legitimate under

```text
delta <= rho^2/(8 Lambda),
```

because radial growth keeps the entire joining segment above a fixed multiple of `rho`.

This is a real closure result. It treats a nongrazing inlet followed by a grazing outlet as well as a grazing inlet.

### 7.4. What module 226 does not prove

The common packet on segments with two nongrazing endpoints remains. On such a segment both traces can be positive and comparable, so the total-variation error may tend to zero while the minimum itself remains large. The theorem then says that `Q`, `I`, `O`, and `M` carry the same obstruction; it does not make the obstruction disappear.

The positive entrance-gradient cutoff is also essential. The leading cutoff estimate is uniform in a previously fixed positive `rho`, but its finite-count remainder is not uniform as `rho` tends to zero. The module correctly does not exchange this cutoff with the collision limit.

## 8. Module 227: intrinsic radial residence anchors

Revision 94 controlled histories crossing a prescribed shell. Revision 95 instead assigns an anchor on the longer physical side of the target, at a scale determined by the target gradient itself.

Set

```text
eta_0 = 1/(16 Lambda),
d_q   = q^2/(256 Lambda).
```

The selected target family satisfies

```text
q <= z(t) < 2q,
ell_sigma >= eta_0 q^2.
```

Since the total physical segment has length at least `16 d_q`, one side of the target has length at least `8 d_q`. The chosen anchor interval lies between distances `2d_q` and `3d_q` on that side. Radial growth keeps every joining interval inside

```text
q/2 < z < 3q.
```

### 8.1. Pointwise anchor inequality

Averaging the fundamental-theorem comparison over the anchor gives

```text
H_{c,q}^epsilon(t)
 <= d_q^(-1) int_{t-4d_q}^{t+4d_q} p_{3q}(u) du
  + C(1+epsilon^(-1))
      int_{t-4d_q}^{t+4d_q} v^{q/2,3q}(u) du.
```

A forward anchor may lie beyond an artificial prefix endpoint, but it remains inside the same complete physical segment and is used only as a positive majorant. The target selector is not redefined. Conditional on the inherited multiplicity-one physical-fiber statement, this use is legitimate.

### 8.2. Exponent arithmetic

The first term uses the critical-volume estimate and contributes

```text
q^(alpha-2) q^2 = q^alpha.
```

The shell term contributes

```text
(1+epsilon^(-1)) q^(alpha-1) q^2
 = (1+epsilon^(-1)) q^(alpha+1).
```

With `alpha=129/128`, the final height is

```text
C q^(129/128)
 + C(1+epsilon^(-1)) q^(257/128).
```

The finite-count remainder displayed in the manuscript has the expected factors

```text
q^(-3/2) theta^m,
(1+epsilon^(-1)) q^(-1/2) theta^m,
```

plus the fixed-band floor. The manuscript fixes `q`, `epsilon`, and the auxiliary band before the collision limsup and enlarges the band afterwards. I found no exponent or limit-order error in this calculation.

### 8.3. Relatively thin segments

If

```text
ell_sigma < eta_0 z(t)^2,
```

radial growth gives

```text
(z^-_sigma)^2 >= (7/8) z(t)^2.
```

Such a segment cannot have a critical backward endpoint. Conversely, a segment born at a critical endpoint must have residence at least a fixed multiple of `z(t)^2` and therefore lies in the relatively long class.

If a relatively thin segment has a grazing physical endpoint, its target value is paid entirely by the absolute derivative integral over the segment. This yields the annular height

```text
C(1+epsilon^(-1)) q^(257/128).
```

These are useful geometric exclusions.

### 8.4. Fixed annuli versus the zero-gradient source

For every fixed positive lower cutoff `a`, finitely many dyadic annuli cover `[a,q)`, and their leading bounds form a convergent geometric series independent of `a`. This proves the manuscript's positive-cutoff estimate.

It does **not** prove the corresponding estimate for the full zero-gradient source. The logical distinction is

```text
lim_{a downarrow 0} limsup_m H(source with z>=a)
```

versus

```text
limsup_m H(full source).
```

A spike supported in an annulus `z approximately q_m` with `q_m -> 0` is eventually excluded by every fixed `a`, yet remains present in the full source at each `m`. Thus a common leading constant for every fixed finite annulus head does not control a collision-dependent disappearing tail.

The displayed negative powers in the finite-count remainder make this obstruction visible. The authors correctly retain it.

## 9. Module 228: bidirectional signed pointwise forcing

The module defines the backward and forward projected measures

```text
K^-_rho = D R - G^{+,>=rho},
K^+_rho = -D R - G^{-,>=rho}.
```

The forward expansion is

```text
K^+_rho
 = terminal cuts + low-gradient negative growth
   - entrances - all positive growth.
```

Thus a critical entrance is positive in the backward comparison and negative in the forward comparison. Artificial and physical upper cuts remain positive in the forward balance rather than being discarded.

### 9.1. Order of operations

The module first projects each complete signed measure, then forms its Stieltjes ramp, then takes a positive part, and only finally defines

```text
J = min(S^-,S^+).
```

This order is essential. The manuscript does not interchange projection with Jordan decomposition and does not replace the minimum of two projected forcings by an integral of sheetwise minima.

The two-ended positive packet of module 226 is also kept separate from `J`. No unjustified identity between that packet and a Jordan component of `D R` is asserted.

### 9.2. Pointwise comparison

The two Stieltjes identities are

```text
R-A_r^-R = T_r^- K^-_rho + T_r^- G^{+,>=rho},
R-A_r^+R = T_r^+ K^+_rho + T_r^+ G^{-,>=rho}.
```

They imply

```text
0 <= J <= J^sharp <= R
```

and

```text
R(t)
 <= max(A_r^-R(t),A_r^+R(t))
  + J(t)
  + C(1+epsilon^(-1))
      int_{t-r}^{t+r} v^rho(u) du.
```

The elementary inequality used to combine the two sides is valid: whichever forcing is smaller supplies an upper bound with the larger of the two averages and the common derivative error.

The sharp version also gives persistence on at least one complete adjacent interval whenever the smaller sharp forcing and derivative error are below the target excess. I found no decisive sign reversal in this argument.

### 9.3. Endpoint criterion

After the ordered positive-gradient limit, the full bad source satisfies

```text
E_M
 <= C_M B^(-1/192)
  + J_{epsilon(B),M}(r)
  + C(1+epsilon(B)^(-1)) r.
```

For any prescribed legal radius with the explicit final term tending to zero, vanishing of the ramped or sharp joint forcing is sufficient for the original pointwise theorem. Necessity follows from `J^sharp<=b^epsilon` and the inherited positive scalar remainder.

The equivalence is logically correct. It is also sharper than the backward-only criterion because a critical entrance is not automatically positive forcing on both sides.

It remains a criterion. No theorem forces `J` to vanish. A target spike may have a large backward budget and a large forward budget for different physical reasons. The minimum-after-projection construction reduces overcount, but reduction alone is not decay.

## 10. The exact residual mechanisms

### 10.1. The two-nongrazing short packet

After module 226, the complete fixed-positive-gradient zero-residence obstruction is concentrated on segments with two positive physical endpoint traces. Its representative is

```text
M_sigma=min(F^-_sigma,F^+_sigma).
```

A successful closure needs a quantitative theorem such as

```text
H_M(M_{rho,delta}^epsilon)
 <= C_M epsilon^(-a) delta^beta,
beta>0,
```

at fixed positive `rho`, followed by a separate lawful treatment of `rho downarrow 0`.

The current packet theorem gives a vanishing **error** between `M` and the original source. It gives no vanishing estimate for `M` itself.

### 10.2. The disappearing critical-annulus tail

The intrinsic anchor controls every fixed annulus and all finite annulus heads. It does not control a family whose support scale depends on the collision count and tends to zero.

Closure requires an all-scales estimate formed before the collision limsup, for example:

```text
H_M(sum_j target source on annulus q_j)
 <= C q_0^eta
```

with a summable finite-count remainder uniform in the number of active annuli, or an equivalent stopping-time, Carleson, square-function, or signed-current estimate.

A finite dyadic sum after fixing a lower cutoff is insufficient.

### 10.3. The joint forcing

The bidirectional criterion will close the scalar theorem only if the joint forcing is localized into already controlled source classes plus quantitatively vanishing residuals. Revision 95 does not prove such a localization theorem.

In particular, it does not establish a bound of the schematic form

```text
J
 <= controlled long-annulus source
  + controlled grazing-ended source
  + two-nongrazing packet residual
  + disappearing-annulus residual,
```

with the last two terms shown to vanish. Without that bridge, the new criterion remains exact but conditional.

### 10.4. Why these are genuine pointwise obstructions

Both residual mechanisms can support a fixed-height pulse on a roof set whose measure tends to zero. Such a pulse is invisible to integrated mass bounds and every established finite norm but remains visible to essential supremum. These terms are therefore not harmless technical tails after the theorem; they are the remaining content of the upper pointwise problem.

## 11. Limit order

Revision 95 generally respects the required order:

1. construct exact physical segment sources and signed measures at finite collision count;
2. take per-segment endpoint minima and projected signed ramps before any uniform height;
3. fix residence widths, radial scales, positive gradient cutoffs, and auxiliary bands;
4. take the collision limsup and exact-label suprema;
5. enlarge the auxiliary band only afterwards;
6. remove only cutoffs for which an ordered passage is explicitly proved; and
7. keep the reconstruction band `B` outermost.

The manuscript explicitly refuses the following invalid operations:

- choosing the gradient cutoff as a function of collision count;
- converting a finite-annulus estimate into an infinite-annulus estimate inside the limsup;
- summing a single-sheet modulus by an uncontrolled number of components;
- treating a cutoff-independent leading constant as a cutoff-uniform finite-count theorem;
- taking a sheetwise minimum before projection; and
- promoting source identity to source decay.

These restrictions are mathematically necessary and should remain prominent.

## 12. Exact theorem-bearing contribution of revision 95

Conditional on the inherited inputs, I regard the following as the genuine new mathematical contribution of this revision:

1. a same-segment two-ended trace packet for the complete short physical source;
2. a collision-normalized pointwise error estimate between the original source and that packet;
3. equality of the inlet, outlet, target-volume, and two-ended ordered residence-zero charges at fixed positive gradient;
4. elimination of every grazing-ended residence-zero class at fixed positive entrance or target gradient;
5. a target-adapted intrinsic radial anchor which does not require a prescribed shell crossing;
6. a complete annular target-height estimate with powers `129/128` and `257/128`;
7. a proof that relatively thin target segments cannot be critical births;
8. a complete thin grazing-ended annular height estimate;
9. a forward projected signed comparison retaining all entrance and terminal signs;
10. a post-projection bidirectional forcing no larger than the previous backward forcing;
11. one-sided adjacent-interval persistence selected by the smaller sharp forcing; and
12. an exact bidirectional criterion for the original scalar pointwise endpoint.

These are not cosmetic metadata or consequences of a finite-norm embedding. They add real physical-segment geometry and a sharper signed pointwise architecture.

The contribution stops before the central theorem because items 1--12 do not prove decay of the two-nongrazing packet, the disappearing-annulus tail, or the joint forcing.

## 13. Claims that remain unproved

The manuscript correctly leaves unproved:

- zero charge of the complete two-nongrazing short packet;
- a collision-uniform zero-gradient short-source estimate;
- a summable all-annulus critical target-height theorem;
- decay of the disappearing critical-annulus tail;
- full target-critical core height decay;
- vanishing of the bidirectional signed forcing;
- vanishing of the earlier joint upper forcing;
- zero essential-height charge of the original critical-or-short-residence source;
- unconditional prescribed-width persistence of every upper spike;
- the upper pointwise half `[P-G]_+ -> 0`;
- the unrestricted pointwise exact-label raw local limit theorem;
- unrestricted same-roof point-conditioned kernel convergence;
- forward essential-likelihood convergence;
- unrestricted path-space total variation or entropy convergence;
- unrestricted normalization on all merely positive or zero arithmetic classes;
- an unnormalized growing-window theorem;
- independent human specialist approval; and
- a formal proof certificate.

The source manifest, proof ledger, publication status, abstract, and final section represent these boundaries accurately.

## 14. Requirements for a successful next revision

### 14.1. Prove decay of the two-nongrazing packet

The next revision should attack the common positive packet itself, not another comparison error. Plausible routes include:

- a two-end coarea map showing that simultaneous positive inlet and outlet traces on a collapsing segment have additional codimension or capacity decay;
- a paired endpoint-flux theorem with collision-uniform transverse control;
- a Carleson packing estimate for segments carrying two positive endpoint traces;
- a signed physical-current identity pairing the two traces before positive projection; or
- a quantitative persistence theorem showing that a large two-ended packet forces a paid interval of original source mass.

A raw count of words or components is not acceptable. The estimate must be weighted by the actual physical density and normalized uniformly in collision count.

### 14.2. Prove an all-scales zero-gradient annular theorem

The next revision must control the radial tail before the collision limsup. It is not enough to prove a common leading estimate for every fixed finite annulus head.

A successful theorem could take the form of:

- a stopping-time decomposition whose finite-count remainders are summable over all active annuli;
- a radial Carleson measure estimate;
- an all-scale square-function or maximal estimate;
- a signed annular current with telescoping cancellation; or
- a direct two-dimensional capacity bound for the full target-critical source.

The proof must explicitly absorb the fixed-band floor and the factors `q^(-3/2) theta^m` and `q^(-1/2) theta^m`, rather than choosing a collision-dependent lower gradient cutoff.

### 14.3. Connect the bidirectional forcing to the paid physical classes

The joint forcing criterion should be accompanied by a localization theorem identifying every positive joint increment with one of:

- a controlled long intrinsic annulus;
- a controlled grazing-ended thin segment;
- a controlled noncritical positive-residence entrance;
- a controlled radial transit packet;
- the two-nongrazing short packet; or
- the disappearing-annulus tail.

Once the last two residual classes have quantitative decay, this localization should imply `J -> 0` with explicit legal rates.

### 14.4. Give a complete outer parameter schedule

After proving residual rates, the paper should state one explicit schedule for

```text
epsilon(B),
r(B),
delta(B),
q(B),
positive gradient cutoffs,
auxiliary bands,
```

and verify every exponent in the legal order. No parameter may depend on the collision count in a way that bypasses a nonuniform remainder.

### 14.5. Close the scalar theorem before further downstream promotion

Only after the bidirectional forcing is proved to vanish should the manuscript promote:

- uniform roof kernel convergence;
- unrestricted same-roof ratios;
- forward essential-likelihood convergence;
- point-conditioned actual-return path laws;
- unrestricted path-space total variation or entropy; or
- normalization on zero arithmetic classes.

### 14.6. Obtain independent specialist verification

A submission of this breadth needs independent reconstruction of at least:

- the four-record spectral theorem and finite-peak reference;
- the common physical coarea and Borel-segment disintegration;
- the optical recurrence, radial monotonicity, and endpoint traces;
- the backward-end and critical-volume estimates;
- the positive scalar remainder;
- the two-ended packet theorem;
- the intrinsic radial anchor and all-scale limit order; and
- the bidirectional signed forcing argument.

Finite fixtures cannot certify these continuum facts.

## 15. Exposition and architecture

The ten-page focused article is clearer than the full archive and is honest about its remaining scope. Several points should remain explicit in any subsequent revision.

1. The grazing-ended zero theorem is at fixed positive gradient; it is not the full zero-gradient theorem.
2. Equality of the four residence-zero charges is not decay of their common two-nongrazing value.
3. The intrinsic-anchor theorem is annular and positive-scale; it is not an all-scale target-critical theorem.
4. A common bound for every fixed lower cutoff does not rule out collision-dependent concentration below that cutoff.
5. The two-ended positive packet and the bidirectional signed forcing are different objects.
6. The minimum defining `J` is taken after projection and must never be moved inside the segment integral.
7. The endpoint equivalence is a criterion, not a forcing-zero theorem.
8. Local preview evidence is not complete exact-SHA qualification.
9. Qualification is not mathematical certification.
10. Historical credit and the precise inherited-input boundary should remain visible.

The full technical archive is exceptionally large. For journal use, the authors should continue to separate the principal theorem narrative from provenance, software qualification, and historical variants. At the same time, every load-bearing inherited theorem used by the focused article must be stated at sufficient precision for independent checking.

## 16. Significance and venue assessment

Revision 95 contains a sharper physical mechanism than revision 94. The same-segment two-ended packet is a natural way to avoid charging a short pulse solely by its inlet. The intrinsic anchor replaces a prescribed shell-crossing condition by target-adapted geometry. The bidirectional forcing correctly exploits the fact that an entrance has opposite signs when viewed from the two roof directions.

If independently verified, these ideas may be useful beyond this manuscript in singular transport problems where projected densities are assembled from short physical histories and where one-sided positive variation overcounts the true source.

For a strong specialized paper, the authors could potentially reorganize around the completed packet, anchor, and signed-comparison theorems, with a sharply delimited conditional endpoint application. That would require a self-contained significance case independent of the still-open unrestricted raw local limit theorem.

At the requested Annals/Acta/Inventiones/JAMS benchmark, however, the present manuscript remains incomplete in its governing direction. The two-nongrazing packet and disappearing-annulus tail are exactly the classes capable of sustaining the unresolved essential-height spike, and the joint forcing is not proved to vanish. The central pointwise theorem remains an objective rather than a conclusion.

## 17. Final recommendation

Revision 95 responds seriously and positively to the revision-94 report. It proves a complete two-ended short-source replacement, eliminates the grazing-ended residence-zero class at fixed positive gradient, establishes an intrinsic critical-annulus anchor with correct exponent arithmetic, separates thin segments from critical births, preserves signed cancellation in both roof directions, and derives a smaller exact pointwise criterion.

I found no decisive internal error in modules 226--228 at their stated scope, conditional on the inherited inputs.

Nevertheless, the common packet carried by two nongrazing endpoint traces is not proved to vanish; concentration in radial annuli disappearing with collision count is not controlled; the bidirectional forcing is not proved zero; the original critical-or-short-residence charge remains open; and the unrestricted pointwise exact-label raw local limit theorem is still unproved.

**I therefore recommend rejection in the present form at the requested Annals/Acta/Inventiones/JAMS benchmark.**
