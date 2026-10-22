# External top-four referee report on A2-DYN revision 91

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v91-referee-response-2026-10-12`, `revision/a2-dyn-v91-referee-copy-2026-10-12`  
**Reviewed author commit:** `5c7512a4341d8277101d9c0b609dc7d2cda1512a`  
**Reviewed repository tree:** `193863f2720774e2226e3ca866dd80c7d0f05b0a`  
**Active manuscript directory:** `papers/A2-DYN-v91-referee-response`  
**Active paper tree:** `5637513690e13d4abf1a46eedb568327648a0b1f`  
**Canonical revision identity:** `a2-dyn-v91-unweakened-critical-and-maximal-source-2026-10-12`  
**Active mathematical source:** 216 numbered core modules; revision 91 adds modules 214--216  
**Immediate author baseline:** revision 90 at `4f0432884896a5a470a31aa18d4a8b7f4d9b8a23`  
**Frozen revision-90 paper tree:** `01d42f467a87817d7b756615a438f95bd8072369`  
**Controlling external report:** `reviews/a2-dyn-v90-external-top4-review-2026-10-12/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `3ffe7d107ef847562fd503ec98a41e33e7963c91` / `6fb5c325fc24eff1934b8134a5c4432a90d04486`  
**Qualification runs at review freeze:** response `38242554387`; referee-copy `38242567270`; both queued, with no conclusion  
**Date:** 12 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, probability, Lorentz-space, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 91 is a genuine theorem-bearing advance. It closes one mathematically meaningful gap left open in revisions 89 and 90: the logarithmic loss at the finite critical distribution exponent is removed. Subject to the inherited geometric, coarea, source-shift, and four-record spectral inputs, the new modules prove:

1. fixed-window decay of the complete first-exit surface in weak `L^(32/31)`;
2. convergence of the original exact-label raw error in the unweakened weak `L^(32/31)` norm on every fixed roof interval;
3. the corresponding critical weak convergence on the complete central window in the explicitly normalized diffusive roof measure;
4. a polynomial critical-norm bound on the original critical-or-short-residence exceptional union; and
5. a weak maximal estimate producing one quantified exceptional roof set, for each fixed data set, which controls all local averaging radii and all dominated smaller-cutoff weighted selectors.

I found no decisive sign error, exponent mismatch, missing finite-partition factor, collision-dependent Fourier band, illicit interchange of an infinite scale sum with a collision limsup, or substitution of a different source in modules 214--216. The scale-matched gluing, the positive domination inequality, the cofinal exponent `31/4096`, and the Hardy--Littlewood maximal calculation are mutually consistent at the stated topology.

The negative recommendation is nevertheless forced by the manuscript's own unchanged organizing assertion. The paper continues to retain the unrestricted pointwise exact-label raw local limit theorem as its governing target. Revision 91 explicitly does not prove that theorem. It leaves the original exceptional-source essential-height charge unproved and leaves `full_raw_return_LLT_proved` and `primary_referee_request_closed` false.

This remaining gap is not eliminated by passing from logarithmically weakened weak convergence to unweakened weak convergence. A fixed-height pulse supported on a shrinking roof interval has weak `L^(32/31)` norm tending to zero, and its maximal superlevel sets have measure tending to zero, while its essential height remains fixed. Thus the new endpoint theorem and maximal theorem strongly constrain concentration but do not exclude collapsing high spikes.

At the requested benchmark, a manuscript whose title, introduction, source architecture, and main endpoint remain the unrestricted pointwise theorem must prove that theorem. Revision 91 substantially improves the final source analysis, but the primary theorem is still open within the manuscript's own status system.

## 2. Frozen source, chronology, and source identity

Both reviewed author branches resolve to

`5c7512a4341d8277101d9c0b609dc7d2cda1512a`.

The repository tree at that commit is

`193863f2720774e2226e3ca866dd80c7d0f05b0a`.

The active article is

`papers/A2-DYN-v91-referee-response`.

The active paper tree is

`5637513690e13d4abf1a46eedb568327648a0b1f`.

The immediate author baseline is revision 90 at

`4f0432884896a5a470a31aa18d4a8b7f4d9b8a23`,

with frozen paper tree

`01d42f467a87817d7b756615a438f95bd8072369`.

The revision-91 author commit has the controlling revision-90 review commit as its parent. The complete revision-90 source is also snapshotted under `provenance/v90-source`. The active source preserves 213 inherited core modules and adds exactly:

- `core/214_scale_gluing_and_unweakened_critical_limit.tex`;
- `core/215_original_source_critical_power.tex`;
- `core/216_all_radius_maximal_source_control.tex`.

The source packet states that inherited mathematical cores, Python sources, appendices, bibliographies, included input/problem files, provenance, the complete preceding article, and both distinct revision-88 variants are preserved. The new result is therefore traceable to the frozen revision-90 source and report rather than being assembled by silently replacing a prior variant.

The present review branch starts directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v91-external-top4-review-2026-10-12/`.

No author manuscript, author revision branch, workflow, prior report, preserved source variant, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The revision-91 exact-SHA workflow runs at report freeze are:

- response branch run `38242554387`;
- referee-copy branch run `38242567270`.

Both were queued and had `conclusion=null`. I therefore do not describe revision 91 as having completed remote qualification.

The declared workflow is designed to verify, among other items:

- the frozen revision-90 paper tree and complete snapshot;
- the controlling revision-90 report blob;
- both separately preserved revision-88 variant trees;
- byte and mode preservation of inherited sources;
- the explicitly theorem-backed supersession of only the weak-critical-convergence flag;
- ordinary and optimized finite-fixture agreement;
- native builds of the focused article and complete supplement;
- recorder coverage of all 216 active core modules;
- stabilized references and warning gates; and
- page geometry and rendered output.

These checks are useful evidence of source identity, finite algebra, and reproducible assembly. They would not certify the continuum coarea identities, Borel maximal-segment disintegration, endpoint contact classification, inherited four-record spectral theorem, source-shift comparison, or the missing pointwise source estimate. The manuscript correctly states this limitation.

## 4. Scope of this audit

The complete archive contains 216 core modules and a large inherited supplement. I have not independently reconstructed every historical theorem.

The substantive review concentrates on:

1. the revision-90 referee requests and the exact revision-91 response;
2. the measurable-set norm and its finite partition law;
3. the use of the revision-89 matched-window critical surface estimate;
4. the fixed-window `r^(1/32)` surface decay in module 214;
5. the matched-scale fractional-potential estimate;
6. the source comparison and outer-limit schedule proving unweakened critical weak convergence;
7. the exact diffusive-window scale cancellation;
8. the bounded-reference domination lemma in module 215;
9. the mass estimate for the original exceptional union;
10. the cofinal exponent `31/4096`;
11. the local maximal inequality and all-radius source estimate in module 216;
12. the parameter dependence of the resulting exceptional set;
13. preservation of exact labels, physical components, original weights, normalization, and arithmetic classes;
14. the distinction between finite critical topology and essential height; and
15. the requested top-four completeness and significance standard.

The inherited physical flow, local source bounds, capped residence theorem, positive scalar remainder, finite-peak reference bound, Borel segment map, and four-record spectral chain are treated as source-pinned inputs. Their use at the new interfaces is inspected here; this report does not convert them into independently certified theorems.

## 5. The governing pointwise assertion

The target retained in the journal remains the uniform pointwise raw local limit

```text
sup_{R, 1<=n<=m, k in Z^2}
esssup_{t in C_{m,R,n,k}(M)}
|m^2 p_{n,R}(k,m,t) - L_{m,R}(k_1,k_2,t,n)| -> 0.
```

Equivalently, the retained scalar reduction still requires the cofinal original exceptional-source essential-height charge to vanish in the outer reconstruction limit.

Revision 91 does not assert this. Its active status correctly leaves the following claims false:

- `strong_critical_LQ_convergence_proved`;
- `original_critical_residence_source_charge_zero_proved`;
- `mean_oscillation_promoted_to_essential_height`;
- `full_raw_return_LLT_proved`;
- `primary_referee_request_closed`;
- `independent_human_review`; and
- `formal_proof_certificate`.

The one inherited flag explicitly superseded is

`unweakened_critical_weak_error_convergence_proved`,

which changes from false in the frozen revision-90 packet to true in revision 91 by Theorem `thm:v91-raw`. This is a legitimate and accurately delimited status transition.

## 6. Audit of module 214: finite critical-norm gluing

### 6.1. The measurable-set norm

For `q>1`, the manuscript uses

```text
N_q(f;J) = sup_{E subset J} |E|^(-1+1/q) int_E |f|.
```

Writing `beta=1-1/q`, partitioning `J` into `N` pieces, and setting

```text
v_i = |E intersect J_i|
```

gives

```text
int_E |f| <= A sum_i v_i^beta
           <= A N^(1-beta) |E|^beta
           =  A N^(1/q) |E|^beta.
```

Thus

```text
N_q(f;J) <= N^(1/q) A.
```

The exponent is correct. The inequality is proved for each actual finite-count function before parameter suprema and limits. It permits moving interval locations and introduces no infinite sum of collision limsups.

### 6.2. From a matched window to a fixed window

If every interval of length `r` has norm at most `C r^zeta`, a partition of a length-`L` interval into at most `(L+r)/r` pieces gives

```text
N_q(f;J) <= C (L+r)^(1/q) r^(zeta-1/q).
```

For the complete first-exit surface, the inherited critical estimate evaluated at `L=r` is `O(r)`. This follows from the already printed bound

```text
C {L^(31/32) r^(1/32)
   +(L+4r)(1+r^(19/32))}.
```

Setting `L=r` makes both contributions `O(r)`. With

```text
q = Q = 32/31,  zeta = 1,
```

the fixed-window conclusion is

```text
limsup N_Q(m^2 Fbar_r;J)
 <= C (L+r)^(31/32) r^(1/32).
```

This is the missing scale-gluing observation. The partition is finite at each fixed `r` and is chosen before the collision limit. I find this argument correct, subject to the inherited complete-surface estimate.

### 6.3. Complete physical scope

The new partition is only a partition of the roof interval. It does not partition the physical source by symbolic word, drop incoming types, introduce a lower residence cutoff, or replace the first-exit surface by a collar. The inherited finite-count residence sum has already included every positive residence scale before the gluing step.

The resulting `r^(1/32)` decay is therefore a genuine complete-surface statement at the finite critical exponent.

## 7. Audit of module 214: the matched-scale fractional potential

The potential is

```text
P_r v(t) = int_0^r s^(-3/8) v(t+s) ds,
```

with `v=v^(1/4)`. The convolution kernel belongs to `L^Q(0,r)` because

```text
(3/8)Q = 12/31 < 1.
```

Young--Minkowski with the source in `L1` gives, on an interval of length `r`,

```text
||m^2 P_r v||_LQ
 <= C r^(1/Q-3/8) m^2 int v.
```

The inherited fixed-width source mass on the enlarged interval is `O(r)`. Hence the local norm is

```text
O(r^(1/Q+5/8)).
```

Summing `Q`th powers over at most `(L+r)/r` pieces yields

```text
||m^2 P_r v||_LQ(J)
 <= C (L+r)^(31/32) r^(5/8).
```

The exponents and the finite partition order are correct. The width `r` remains fixed through the collision and auxiliary-band limits.

## 8. Audit of module 214: unweakened critical raw convergence

### 8.1. Source budget

The retained positive source comparison is

```text
b^epsilon
 <= 2 A_r b^epsilon
  + C Fbar_r
  + C P_r v
  + C_Theta (1+epsilon^(-1)) sqrt(r) A_r p.
```

Applying the critical measurable-set norm and the inherited local estimates gives

```text
limsup N_Q(m^2 b^epsilon;J)
 <= C (L+r)^(31/32)
       {epsilon^(1/16)
        +r^(1/32)
        +r^(5/8)
        +(1+epsilon^(-1)) sqrt(r)}.
```

Each term has the stated origin:

- averaged bad-source mass;
- complete first-exit surface;
- fractional optical potential; and
- original guard displacement.

For fixed `epsilon`, sending `r` to zero only after the collision limit and permitted auxiliary-band enlargement gives

```text
limsup N_Q(m^2 b^epsilon;J)
 <= C L^(31/32) epsilon^(1/16).
```

No pointwise estimate for the bad source is used.

### 8.2. The reconstruction schedule

The retained positive scalar remainder has

```text
m^2 p - L = m^2 b^(epsilon(B)) + e_B,

epsilon(B)=A_0 B^(-1/12),

||e_B||_infinity <= C_M B^(-1/192)
```

in the ordered collision limit. Since

```text
epsilon(B)^(1/16) = O(B^(-1/192)),
```

the bad-source and remainder terms decay at the same outer power. Sending `B` to infinity last proves convergence in `N_Q` itself, without a logarithmic denominator.

The equivalent explicit choice

```text
r(B)=c epsilon(B)^4
```

is legal because each `B` and `r(B)` is fixed before `m` tends to infinity. No frequency band or roof scale depends on collision count.

I find this outer-limit arithmetic correct.

### 8.3. Exact topology

The conclusion is weak `L^(32/31)` convergence in the measurable-set norm. It is not strong `L^(32/31)` convergence and is not essential-supremum convergence. The manuscript, response, proof ledger, abstract, and status files state this distinction consistently.

## 9. Audit of module 214: the complete diffusive window

The central roof interval is partitioned into at most

```text
2M sqrt(m)+2
```

pieces of length at most one. If `d_m` is the uniform local critical norm, gluing gives the roof-coordinate bound

```text
d_m (2M sqrt(m)+2)^(1/Q).
```

Under

```text
t = m bar(tau_R) + sqrt(m) u,
```

the weak `L^Q` measurable-set norm is multiplied by

```text
m^(-1/(2Q)) = m^(-31/64).
```

The growth from the number of unit intervals is exactly `m^(1/(2Q))`, so the two factors cancel and the remaining bound is a fixed multiple of `d_m`, which tends to zero.

The argument is correct at the stated normalized topology. The conclusion uses `dt/sqrt(m)`, not unnormalized `dt`, and does not imply the pointwise theorem.

## 10. Audit of module 215: bounded-reference domination

### 10.1. The real-variable inequality

For `g,e>=0`, `g<=D+e`, and `int g<=mu`, the proof uses

```text
int_E g <= min(mu,D|E|)+int_E e.
```

The supremum of

```text
|E|^(-beta) min(mu,D|E|)
```

is

```text
D^beta mu^(1-beta)
```

with `beta=1-1/q`. Thus

```text
N_q(g) <= D^beta mu^(1/q) + N_q(e).
```

The inequality is correct, including the zero cases, and is applied to each actual finite-count function before limits.

### 10.2. Application to the original union

The unweighted upper source is

```text
U_{a,delta}
 = integral 1_{z<a or ell<delta} dmu_t.
```

It is used only for domination:

```text
0 <= R_{a,delta}^epsilon <= U_{a,delta} <= p.
```

The exact weighted target is not replaced. No monotonicity of the smooth guard in `epsilon` is assumed.

The inherited fractional source estimate and short-residence estimate give

```text
limsup m^2 int_J U_{a,delta}
 <= C_L (a^(129/128)+delta^(1/32)).
```

On the central window,

```text
m^2 U_{a,delta}
 <= m^2 p
 <= D_M + |m^2p-L|,
```

because the finite-peak reference is uniformly bounded. Combining the domination lemma with the new unweakened critical raw convergence yields

```text
limsup N_Q(m^2 U_{a,delta})
 <= C_{M,L}(a^(129/128)+delta^(1/32))^(31/32).
```

This application is valid at the stated topology.

### 10.3. Cofinal exponent

For

```text
a=h^(1/8),  delta=h^(1/4),
```

the two mass powers are

```text
a^(129/128) = h^(129/1024),

delta^(1/32)= h^(1/128).
```

The short-residence term is larger for `0<h<1`. Raising it to `1/Q=31/32` gives

```text
h^(31/4096).
```

The printed exponent is correct.

The bound is polynomial and improves the earlier logarithmic critical estimate on the same original union. It still permits fixed-height pulses on collapsing roof sets and therefore is not an essential-height estimate.

## 11. Audit of module 216: the maximal inequality

### 11.1. Weak distribution estimate

For a zero-extended nonnegative `g`, the manuscript selects a disjoint interval subcollection whose triple dilates cover a compact subset of `{Mg>lambda}`. If `V` is the union of the selected intervals, then

```text
lambda |V| < int_V g <= A |V|^(1-1/q),
```

and hence

```text
|{Mg>lambda}| <= 3(A/lambda)^q.
```

This is the standard one-dimensional covering argument. Integrating

```text
min(|E|,3(A/lambda)^q)
```

in `lambda` gives

```text
N_q(Mg;J) <= 3^(1/q) q/(q-1) A.
```

The constants and exponents are correct.

### 11.2. All-radius source estimate

For a fixed interval `J`, enlarged interval `K`, collision count, radius, exact labels, and cutoffs, the finite-count source is

```text
G_{m,a,delta}=m^2 U_{a,delta} 1_{C(M) intersect K}.
```

The critical norm from module 215 gives

```text
A = O((a^alpha+delta^gamma)^(1/Q)).
```

Raising the maximal level estimate to power `Q` yields

```text
limsup |{t in J: M G_{m,a,delta}(t)>lambda}|
 <= C lambda^(-Q)(a^alpha+delta^gamma).
```

At the cofinal cutoffs this becomes

```text
C lambda^(-32/31) h^(1/128).
```

All smaller-cutoff original weighted sources are pointwise dominated by the unweighted union, so the same exceptional set controls their interval averages simultaneously.

### 11.3. Parameter dependence

The phrase "one exceptional roof set" must be read within each fixed finite-count data set and enlarged window. The theorem does not construct one universal set valid simultaneously for every billiard radius, exact label, collision count, and roof window. The manuscript already states that no common null set for all radii is asserted.

This parameter dependence should remain explicit in any future abstract or summary. It does not affect the printed supremum estimate, but it prevents an accidental interpretation of the maximal theorem as a universal pointwise exceptional-set removal.

### 11.4. Lebesgue points

Outside the maximal superlevel set, Lebesgue differentiation bounds source values at Lebesgue points for each source. This is a valid almost-everywhere statement for each fixed finite-count density. It is not a uniform lower-width theorem for high values and supplies no common null set across the uncountable radius parameter.

## 12. Why revision 91 still does not close the pointwise theorem

Let

```text
f_delta = 1_(0,delta).
```

Then

```text
||f_delta||_infinity = 1,

N_Q(f_delta) = delta^(1/Q),

|{M f_delta>lambda}| = O_lambda(delta)
```

for every fixed positive `lambda<1`. Thus both the critical norm and the maximal exceptional-set measure tend to zero while the essential height remains one.

This is not asserted to be a billiard counterexample. It is a topology test. It shows that the exact topology proved in modules 214--216 cannot by itself imply the pointwise target.

The maximal theorem says that high local averages occur on a small set. It does not say the set is empty, and it does not force a high point to persist on a roof interval of quantitatively positive width. A collision-uniform spike-persistence theorem or an equivalent pointwise physical estimate is still necessary.

The gap therefore remains qualitative:

- weak critical convergence controls distribution;
- the maximal estimate controls the measure of bad roofs across all averaging radii;
- the target controls the essential height uniformly in all parameters.

No finite distribution exponent, by itself, reaches the last topology.

## 13. Response to the revision-90 report

Revision 91 responds positively and accurately to several prior points.

### 13.1. Unweakened critical weak convergence

**Addressed.** The scale-matched complete-surface bound and finite partition law give genuine fixed-window decay. The positive source comparison and outer reconstruction schedule then remove the logarithmic loss from the original raw error.

### 13.2. Critical control on the original exceptional union

**Strengthened.** The earlier logarithmic bound is replaced by a polynomial critical-norm estimate on the exact original union, uniformly over smaller cutoffs and original weights.

### 13.3. A maximal formulation

**Addressed at weak type.** One exceptional set controls every local averaging radius and every dominated smaller-cutoff selector for each fixed finite-count data set.

### 13.4. Pointwise maximal closure

**Not addressed to completion.** The revision-90 report expressly warned that a weak maximal estimate reproducing only superlevel-set measure decay would not suffice. Revision 91 proves precisely such a weak maximal estimate and correctly acknowledges its limitation.

### 13.5. Quantitative spike persistence

**Not proved.** There is no theorem forcing a high source value to occupy a roof interval of collision-uniform positive width or capacity.

### 13.6. Above-threshold regularity

**Not proved.** The inherited `W^{s,1}` result remains below a pointwise embedding threshold, and the new weak critical theorem is not a strong critical or supercritical regularity theorem.

### 13.7. Independent specialist verification

**Not supplied.** Source preservation, finite fixtures, and compilation checks are not an independent audit of the continuum proof chain.

The revision is therefore a serious and correctly scoped response, but the primary pointwise request remains open.

## 14. Exact theorem-bearing contribution of revision 91

Subject to the inherited inputs, I regard the following as the genuine new contribution:

1. a finite measurable-set gluing theorem retaining the local scale;
2. complete critical surface decay `C(L+r)^(31/32)r^(1/32)` on fixed roof windows;
3. a matched-scale strong `L^(32/31)` estimate for the actual fractional optical potential;
4. unweakened weak `L^(32/31)` convergence of the original exact-label raw error;
5. the corresponding complete central-window convergence in diffusive roof measure;
6. a bounded-reference domination principle converting mass and raw-error control into critical control of a positive subsource;
7. polynomial critical-norm decay `h^(31/4096)` on the original cofinal exceptional union; and
8. an all-radius weak maximal exceptional-set estimate of order `lambda^(-32/31)h^(1/128)`.

These are not cosmetic additions. In particular, item 4 closes a real gap explicitly recorded in the revision-90 status. The result should be stated and credited as an endpoint weak local-limit theorem, while remaining distinct from the pointwise theorem.

## 15. Claims that remain unproved

The revision correctly leaves unproved:

- zero essential-height charge for the original exceptional source;
- the unrestricted pointwise exact-label raw local limit theorem;
- strong `L^(32/31)` convergence;
- any finite-norm implication to essential height;
- an unnormalized growing-window theorem;
- a universal exceptional set across every radius and exact label;
- uniform pointwise denominator estimates on positive arithmetic classes;
- unrestricted same-roof pair ratios;
- forward essential-likelihood convergence;
- any normalization of arithmetic zero classes;
- independent human specialist approval; and
- a formal proof certificate.

The scalar-first order remains necessary. No downstream point-conditioned law should be promoted before the pointwise scalar source is closed.

## 16. What a successful next revision must prove

The next revision should not merely replace the exponent `32/31` by another finite exponent or improve the power `31/4096`. It needs a theorem using additional physical structure to exclude collapsing high spikes.

### 16.1. Quantitative spike persistence

Prove that if the normalized original exceptional source exceeds a level `lambda` at a Lebesgue point, then it remains above a fixed fraction of `lambda` on a roof interval whose length is bounded below by an explicit function of `lambda`, uniformly in collision count, exact labels, billiard radius, and cofinal cutoffs.

Combined with the established interval-mass or critical-norm decay, such a result would force the essential height to vanish.

### 16.2. A genuinely pointwise maximal inequality

A sufficient inequality would control the source value almost everywhere by a prescribed-scale average plus a remainder that tends to zero uniformly in the legal outer limit, with constants independent of exact labels and cutoffs. The prescribed averaging radius must have a collision-uniform lower bound determined by the source value or physical geometry.

The present weak maximal distribution estimate is not enough because it permits a nonempty shrinking exceptional set at every collision count.

### 16.3. Stronger regularity with a vanishing norm

A Sobolev, Besov, or bounded-variation route must reach a space embedded into `L-infinity` and must have a norm that actually tends to zero. A bounded norm, or a vanishing norm below the one-dimensional pointwise threshold, still permits narrow fixed-height pulses.

### 16.4. Direct superlevel geometry

Use maximal-segment geometry, monotone radial growth, the exact angular density, two-sided end classification, and the prefix representation to show that a high roof source cannot be confined to arbitrarily thin components. The existing source-specific architecture appears relevant, but the present theorems control integrated crossings and distribution functions rather than a lower bound on component width.

### 16.5. Preserve the exact limit order

Any new argument must continue to respect:

1. finite-count positive source formation;
2. fixed auxiliary spectral bands before collision limits;
3. complete summation of physical residence or translation scales before limsup where required;
4. auxiliary-band enlargement only after the collision limit;
5. cofinal cutoffs fixed before each collision limit; and
6. the reconstruction band as the outermost limit.

A choice depending directly on collision count would not close the theorem proved here.

### 16.6. Independent specialist verification

A submission of this breadth should include independent checks by specialists in dispersing billiards, anisotropic transfer operators, geometric coarea/disintegration, and probability. At minimum, the load-bearing inherited inputs used by modules 214--216 should be reconstructed independently rather than accepted solely from source preservation and finite diagnostics.

## 17. Exposition and architecture

The focused article is more disciplined than the underlying archive. It states the new weak endpoint theorem, its explicit inputs, and the remaining pointwise obligation without claiming a false implication.

Before journal submission, I recommend the following editorial changes:

1. state in the introduction that "critical" means the finite exponent `32/31`, not the `L-infinity` endpoint;
2. keep the phrase "one exceptional set" explicitly parameterized by collision count, radius, exact labels, cutoffs, and roof window;
3. isolate the scale-matched `O(r)` surface input as a named proposition before the gluing theorem;
4. display the two cancellations separately: `N^(1/Q)` versus `r`, and `m^(1/(2Q))` versus the diffusive Jacobian;
5. distinguish throughout between weak `L^Q`, strong `L^Q`, maximal weak type, and essential height;
6. provide a compact dependency table linking each inherited input to its exact theorem and source tree;
7. state the workflow status as evidence only after a completed exact-SHA run; and
8. reduce archive-facing provenance discussion in the mathematical narrative while retaining it in supplementary documentation.

These changes would improve readability but would not alter the present recommendation, which is based on the unproved pointwise theorem.

## 18. Significance and venue assessment

The endpoint weak theorem is mathematically stronger than the revision-90 result and appears to be the natural culmination of the finite-distribution part of the program. The polynomial estimate on the original exceptional union and its all-radius maximal consequence are also useful refinements.

If independently verified and reorganized around the finite critical theorem actually proved, this material could support a substantial specialized paper. That would require a title, introduction, and theorem hierarchy centered on weak critical raw inversion rather than on a pointwise theorem still listed as open.

The present manuscript, however, explicitly retains the unrestricted pointwise theorem as its organizing objective and retains its essential-height charge as an unclosed primary referee request. At the requested four-journal benchmark, that incompleteness is decisive.

## 19. Final recommendation

Revision 91 makes a real advance:

- it correctly exploits the matched-window surface gain;
- it removes the logarithmic loss at weak exponent `32/31`;
- it preserves the original exact-label source and legal limit order;
- it strengthens the exceptional-union estimate from logarithmic to polynomial critical decay; and
- it proves a coherent all-radius weak maximal statement.

I found no decisive internal error in the three new modules at their stated topology, conditional on the inherited inputs.

Nevertheless, the manuscript does not prove its governing pointwise theorem. The original exceptional-source essential-height charge remains open, and the new weak maximal estimate does not exclude a nonempty sequence of shrinking high-roof sets.

**I therefore recommend rejection in the present form at the requested Annals/Acta/Inventiones/JAMS benchmark.**

This recommendation should not be read as denying the value of the finite critical results. It reflects the mismatch between the theorem the manuscript continues to organize around and the theorem it currently proves.
