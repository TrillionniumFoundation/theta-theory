# External top-four referee report on A2-DYN revision 25

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v25-referee-response-2026-10-07`, `revision/a2-dyn-v25-referee-copy-2026-10-07`  
**Reviewed commit:** `4c07267338175932688a20a6021dae1b602074a0`  
**Reviewed repository tree:** `0149439a9b7bf37e39b60079c6126c89f4cec383`  
**Frozen ordinary paper tree:** `5c5378441102a155ccbf76f4b7f18d426390d3a9`  
**Active manuscript directory:** `papers/A2-DYN-v25-referee-response`  
**Immediate author baseline:** revision 24 at `c1d6940a875f501ee1957204e81772df7b9b39d6`  
**Controlling substantive report:** `reviews/a2-dyn-v24-external-top4-review-2026-10-07/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `92a8236e149c79c797fa85dacf5953e69b8960ff` / `9f58ef5d84b9e91d5eadd8d4a49317158db695e0`  
**Date:** 7 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards-specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 25 is a genuine and technically substantial advance. It responds to the principal frequency-geometric limitation identified in the revision-24 report: the preceding prescribed-count theorem controlled an isotropic ball only up to rescaled exponent `67/1400`, while the raw mixed-density problem also requires substantially larger roof frequencies and eventually the complete fixed-count complement.

The revision develops two new mathematical mechanisms.

First, it extends damped removal of smoothing from the inherited cubic residual expansion to every fixed even residual order. For a fixed integer `P`, all residual degrees through `2P-1` remain inside a full chronological word of damped collision powers, while only the `2P`-th remainder is estimated by small-mass moments. The spectral Taylor degree, residual degree, coarse smoothing scale, and fine multiplier scale are kept distinct.

Second, it uses this high-order theorem to prove fixed-count Fourier estimates on boxes with different widths in the four frequency coordinates. For rescaled half-width exponents

\[
 \boldsymbol\theta=(\theta_1,\theta_2,\theta_3,\theta_4),
 \qquad
 \theta_* = \max_i\theta_i,
 \qquad
 \Theta=\sum_i\theta_i,
\]

the sufficient region is

\[
 \min_i\theta_i\ge\frac1{200},
 \qquad
 \theta_*<\frac1{10},
 \qquad
 \Theta+	heta_*<\frac14.
\]

The concrete new box uses

\[
 \boldsymbol\theta
 =\left(\frac1{100},\frac1{100},\frac1{100},\frac9{100}\right).
\]

Thus its physical half-widths are

\[
 |u_1|,|u_2|,|s|\le2n^{-49/100},
 \qquad
 |b|\le2n^{-41/100},
\]

and its rescaled half-widths are `2 n^(1/100)` in the three discrete-coordinate directions and `2 n^(9/100)` in the flight-time direction. On this box outside the inherited central ball, the paper proves the prescribed-count raw estimate

\[
 n^2\int
   |\Phi^{[k],a}_{n,R}(z)|\,dz
 \le
 C\left(M_a n^{-1/40}+V_a n^{-497/25}\right),
\]

uniformly in the radius, the prescribed count, and the position of one actual-return insertion. There is no average over return counts and no division by the frequency volume.

The union of this box with the entire inherited isotropic band retains the old principal central error

\[
 C\left(
 M_a n^{-3/280}\sqrt{\log(2+n)}
 +V_a n^{-9/175}
 \right).
\]

I found no decisive counterexample in the two new proof modules:

- `core/52_high_order_damped_unsmoothing.tex`;
- `core/53_anisotropic_fixed_count_bands.tex`.

The accompanying `core/54_dependency_guide.tex` accurately separates unconditional outputs from the remaining raw estimates.

The fixed-order moment partition retains every nonsingleton block count. The heterogeneous cumulant comparison expands the change of each partition product and uses independent-block cancellation correctly. The chronological word contains at most `2P` smooth multipliers and `2P+1` collision powers, whose nonnegative lengths sum to the full deterministic interval. The fine scale is not inserted into the twisted operator. The anisotropic volume, maximal-frequency loss, stopping loss, analytic radius, finite spectral remainder, raw Jacobian, and active count-coordinate kernel are all tracked with coherent exponents.

This is meaningful progress. In particular, the manuscript now reaches flight-time frequencies close to the rescaled exponent `1/10` while preserving the previously proved isotropic region.

The negative recommendation nevertheless remains necessary. The new region is an elongated box, not the complete isotropic complement. The three discrete-coordinate widths have rescaled exponent only `1/100`, while the roof direction has exponent `9/100`. The previously proved isotropic ball has exponent `67/1400`, approximately `0.04786`. Their union leaves substantial four-dimensional frequency regions before the target isotropic scale `n^(1/10)`, and it does not cover compact nonzero torus frequencies, the complete peripheral regimes, or the growing and far roof-frequency splice.

Moreover, the exact raw identity continues to contain the genuine long-time second-derivative sum, the active-kernel local extracted-edge correction, and the finite-band residual integral. Weighted denominator asymptotics and the relative replacement of completed-return events by exact physical-time/lattice events also remain open.

These are load-bearing mechanisms of the raw mixed-density local limit theorem that organizes the article. They are not presentation details, and they do not follow from fixed-order collision moments or from the new box estimate.

The unconditional package is now unusually substantial for one Lorentz family. A reorganized paper centered on the completed Gaussian, marked-moment, phase, finite-extraction, averaged-orbit, isotropic fixed-count, and anisotropic fixed-count theorems could be a strong specialist contribution after independent expert review. That is a distinct editorial claim from acceptance at the requested four-journal benchmark for the still-unproved full raw endpoint.

## 2. Frozen source, chronology, and exact qualification

The two named revision-25 author branches resolve to the same commit:

`4c07267338175932688a20a6021dae1b602074a0`.

The repository tree at that commit is

`0149439a9b7bf37e39b60079c6126c89f4cec383`.

The frozen ordinary paper tree is

`5c5378441102a155ccbf76f4b7f18d426390d3a9`.

The immediate mathematical baseline is revision 24 at

`c1d6940a875f501ee1957204e81772df7b9b39d6`,

with ordinary paper tree

`f15ab9854d022319db374f8ce38f4e6a4273dd84`.

The controlling revision-24 report is frozen at commit

`92a8236e149c79c797fa85dacf5953e69b8960ff`

and blob

`9f58ef5d84b9e91d5eadd8d4a49317158db695e0`.

Revision 25 preserves all fifty-one inherited core files, all inherited Python sources, and `references.tex` byte-for-byte. Six exact replacements affect `main.tex` only. All old mathematical labels are retained.

The revision adds:

- `core/52_high_order_damped_unsmoothing.tex`;
- `core/53_anisotropic_fixed_count_bands.tex`;
- `core/54_dependency_guide.tex`;
- `HIGH_ORDER_INPUT_MAP.md`;
- the v25 verifier and finite diagnostic.

The source manifest accurately records:

- `fixed_arbitrary_order_damped_unsmoothing_proved: true`;
- `anisotropic_fixed_count_band_proved: true`;
- `retained_rate_union_proved: true`;
- `active_box_raw_identity_proved: true`;
- `full_isotropic_one_tenth_band_proved: false`;
- `full_fixed_return_complementary_integral_proved: false`;
- `exact_physical_event_replacement_proved: false`;
- `full_raw_LLT_proved: false`.

The exact-source qualification completed successfully on both reviewed branches:

- response branch run `37530699923`;
- referee-copy branch run `37530726302`.

For the response branch, exact checkout, source/report-scope archiving, native TeX and numerical-check installation, normal and optimized verification, complete article build, PDF metadata and proof-page rendering, and artifact upload all completed successfully.

The response artifact is

`11443489844`,

named

`a2-dyn-v25-4c07267338175932688a20a6021dae1b602074a0`,

with digest

`sha256:5d06be36ffd606b2c8522edcfe0284a66f6cca0ddf0b7e2fa2d3b83dfd730a1c`.

These facts establish exact source identity and successful execution of the declared finite checks and native build. They do not certify the continuum collision-space inputs, the new fixed-order proofs, the missing complementary regions, the long-time finite-count constants, or the full theorem.

The present review branch starts directly from the reviewed author commit and adds only this report under

`reviews/a2-dyn-v25-external-top4-review-2026-10-07/`.

No manuscript source, author branch, workflow, earlier report, or unrelated repository path is modified.

## 3. What revision 25 actually proves

Let

\[
 h_R=f_R-\bar G_R\mathbf 1_{Y_R^*}
\]

be the inherited bounded collision compensation. Let

\[
 I^a_{r,s,R}(z)
 =\int_M a(y)e^{iz\cdot\mathsf H_{r,s,R}(y)}\,d\nu(y),
 \qquad m=r+s,
\]

be the deterministic two-sided marked collision pairing, and let

\[
 \Phi^{[k],a}_{n,R}(z)
 =\int_{Y_R^*}a((F_R^*)^kx)e^{iz\cdot J_{n,R}(x)}\,d\nu(x)
\]

be the physical transform at the prescribed actual return count.

Revision 25 adds the following conclusions.

### 3.1 Every fixed even moment of a small-mass residual

For each fixed integer `P>=1`, a centered real collision observable `u` satisfying

\[
 \|u\|_{\mathcal V}\le B,
 \qquad
 \|u\|_1\le B\delta
\]

obeys

\[
 \int|S_{m,R}u|^{2P}\,d\nu
 \le
 C_{P,B}
 \sum_{b=1}^{P}
 (m\delta)^b
 L_\delta^{2P-b},
 \qquad
 L_\delta=1+|\log\delta|.
\]

The estimate also holds on translated and reversed deterministic intervals.

The formula retains all block counts `b=1,...,P`. In particular, the connected contribution with one nonsingleton block is not discarded. The theorem is fixed-order: its constant may depend on `P`, and neither `P` nor a factorial cumulant bound is allowed to grow with `n`.

### 3.2 Heterogeneous connected-correlation decay

For each fixed `q`, bounded-variation collision observables `u_1,...,u_q` at arbitrary integer times satisfy

\[
 \left|
 \operatorname{cum}
 (u_1\circ T_R^{t_1},\ldots,u_q\circ T_R^{t_q})
 \right|
 \le
 C_qe^{-c_q\operatorname{diam}\{t_1,\ldots,t_q\}}
 \prod_j\|u_j\|_{\mathcal V}.
\]

The proof orders the times, splits at a largest gap, replaces the two whole blocks by independent copies with unchanged marginals, and compares every subset moment crossing the gap. For a partition product, it uses the exact telescoping identity

\[
 \prod_{j=1}^{b}m_{A_j}
 -
 \prod_{j=1}^{b}m_{A_j}^{\circ}
 =
 \sum_{i=1}^{b}
 (m_{A_i}-m_{A_i}^{\circ})
 \prod_{j<i}m_{A_j}
 \prod_{j>i}m_{A_j}^{\circ}.
\]

Independent-block cancellation makes the comparison cumulant zero. The bound is summable, with one diameter weight, over all relative times after anchoring one time.

This explicitly covers one centered section mark together with collision factors and supports the marked-moment parity calculation in the inherited multiscale section.

### 3.3 High-order damped removal of smoothing

Fix integers `P>=1` and `Q>=3`. The residual Taylor degree is `2P-1`; the collision spectral degree is `Q`. They are independent.

For real frequencies in the inherited finite-jet damping domain, and for a fine scale `epsilon`, revision 25 proves

\[
 |I^a_{r,s,R}(z)|
 \le
 C_{P,Q}M_a\epsilon^{-4P}
 (1+m|z|)^{2P-1}e^{-cm|z|^2}
 +C\epsilon V_a
\]

\[
 \quad
 +C_PM_a\epsilon(1+m|z|)^{2P-1}
 +C_PM_a|z|^{2P}
 \sum_{b=1}^{P}(m\delta)^bL_\delta^{2P-b}.
\]

All residual degrees through `2P-1` remain inside a chronological word of the coarse twisted collision operator. Only the `2P`-th Taylor remainder is estimated without damping.

The fine scale smooths the mark and finitely many residual multipliers. It never changes the coarse twist or its analytic domain.

At degree `j`, there are `j` residual multipliers and one mark, hence at most `2P` multipliers. The chronological word contains at most `2P+1` collision powers. Their nonnegative lengths sum exactly to `m`. Repeated insertion times give zero-length powers, and endpoint marks are covered without a separate argument.

At `P=2`, the theorem recovers the inherited cubic formula, including the multiplier loss `epsilon^(-8)` and both fourth-moment terms

\[
 m^2\delta^2L_\delta^2,
 \qquad
 m\delta L_\delta^3.
\]

### 3.4 A family of prescribed-count anisotropic boxes

For

\[
 B_{n,i}=n^{-1/2+\theta_i},
 \qquad
 \mathcal B_n=\prod_{i=1}^{4}[-2n^{\theta_i},2n^{\theta_i}],
\]

suppose

\[
 \min_i\theta_i\ge\frac1{200},
 \qquad
 \theta_*<\frac1{10},
 \qquad
 \Theta+	heta_*<\frac14.
\]

For any fixed

\[
 0<\eta\le\frac14-\Theta-\theta_*,
\]

there is `sigma>0` such that

\[
 n^2
 \int_{\substack{z\in n^{-1/2}\mathcal B_n\\
                    |z|\ge2n^{-99/200}}}
 |\Phi^{[k],a}_{n,R}(z)|\,dz
 \le
 C\left(M_an^{-\eta}+V_an^{-\sigma}\right).
\]

The count `n` and the mark `k` are prescribed. There is no count average, directional average, or volume normalization.

The proof chooses a coarse exponent `alpha` with

\[
 2\theta_*<\alpha<\frac14-\frac{\theta_*}{2}.
\]

This interval is nonempty exactly under the displayed sufficient condition `theta_*<1/10`.

It then chooses fixed integers `P,Q` such that

\[
 P(\alpha-2\theta_*)>\Theta+\eta,
\]

\[
 (Q-1)(1/2-\theta_*)>2\alpha(Q+1),
\]

and a sufficiently large fixed fine exponent `beta`.

### 3.5 Central comparison on the same box

If

\[
 \eta\ge\frac3{280},
 \qquad
 \sigma\ge\frac9{175},
\]

then the marked Gaussian comparison on the entire rescaled box satisfies

\[
 \int_{\mathcal B_n}
 \left|
 C^{[k],a}_{n,R}(v)
 -\alpha_ae^{-v^{\mathsf T}D_Rv/2}
 \right|\,dv
 \le
 C\left(
 M_an^{-3/280}\sqrt{\log(2+n)}
 +V_an^{-9/175}
 \right).
\]

The small inherited central ball lies inside the box because every coordinate width exponent is at least `1/200`. The rest is handled by the new prescribed-count transform estimate and the uniformly elliptic Gaussian tail.

### 3.6 A concrete roof-direction box

The explicit choice is

\[
 \boldsymbol\theta
 =\left(\frac1{100},\frac1{100},\frac1{100},\frac9{100}\right),
 \qquad
 \alpha=\frac{19}{100},
 \qquad
 P=16,
 \qquad
 Q=29,
 \qquad
 \beta=20.
\]

The residual Taylor degree is `31`; the spectral Taylor degree is `29`. Their inequality is intentional: they control different expansions.

The physical support is

\[
 |u_1|,|u_2|,|s|\le2n^{-49/100},
 \qquad
 |b|\le2n^{-41/100}.
\]

The raw estimate is

\[
 n^2\int_{\substack{z\in n^{-1/2}\mathcal B_n^{\rm roof}\\
                     |z|\ge2n^{-99/200}}}
 |\Phi^{[k],a}_{n,R}(z)|\,dz
 \le
 C\left(M_an^{-1/40}+V_an^{-497/25}\right).
\]

### 3.7 Retaining the old isotropic region

Let

\[
 \mathcal U_n
 =
 \mathcal B_n^{\rm roof}
 \cup
 \{v:|v|\le2n^{67/1400}\}.
\]

On this union the paper retains the original central error

\[
 C\left(
 M_an^{-3/280}\sqrt{\log(2+n)}
 +V_an^{-9/175}
 \right).
\]

The roof exponent `9/100` is larger than `67/1400`, so the box contains genuinely new frequencies beyond the old sphere. The old sphere is not deleted or replaced.

### 3.8 Same-event conditioning

For the unchanged marked-state event with exact probability `p_{n,R}` and indicator variation `V_{n,R}`, the same union estimate holds after division by precisely the same probability:

\[
 \int_{\mathcal U_n}
 \left|
 \mathbb E[e^{iv\cdot U_{n,R}/\sqrt n}\mid A_{n,k,R}]
 -e^{-v^{\mathsf T}D_Rv/2}
 \right|\,dv
\]

\[
 \le
 \frac{C}{p_{n,R}}
 \left(
 n^{-3/280}\sqrt{\log(2+n)}
 +V_{n,R}n^{-9/175}
 \right).
\]

No event or denominator is replaced.

### 3.9 A coordinatewise-kernel raw identity

For the concrete box, the active cutoff is

\[
 \chi_n^{\rm box}(\omega)
 =\prod_{i=1}^{4}\chi_0(\omega_i/B_{n,i}),
 \qquad
 K_n^{\rm box}=\mathcal F^{-1}\chi_n^{\rm box}.
\]

The associated exact raw error budget contains:

- the new-box central Gaussian error;
- the missing Gaussian tail `exp(-c n^(1/50))`;
- a rapidly decaying high-count convolution correction;
- the active-kernel local edge correction;
- the finite-band edge-subtracted residual integral;
- the true finite-count second-derivative sum.

The high-count correction satisfies

\[
 n^2\sup|K_n^{\rm box}*\mathsf T^{a,L_n}|
 \le
 C_JM_a n^{3/25-51J/100}.
\]

The last three raw terms are retained explicitly and are not declared small.

## 4. Audit of the fixed small-mass moment formula

The moment estimate in Lemma `all-small-mass-moments` is logically consistent with the inherited fixed-order cumulant bound.

For each order `j<=2P`, the inherited result gives

\[
 |\operatorname{cum}_j(S_mu)|
 \le
 C_{P,B}m\delta L_\delta^{j-1}.
\]

The finite moment-cumulant identity expresses the `2P`-th moment as a sum over set partitions. Centering removes singleton blocks. A partition with `b` remaining blocks has `1<=b<=P`; multiplying the cumulant estimates gives

\[
 (m\delta)^b
 L_\delta^{\sum_{A\in\pi}(|A|-1)}
 =
 (m\delta)^bL_\delta^{2P-b}.
\]

This accounts for every partition type. The sum begins at `b=1`, which is essential when `m delta` is small. Keeping only the paired term `b=P` would not give a uniform estimate.

Translation and reversal follow from collision invariance. The order is fixed before all dynamical parameters vary, so no hidden uniformity in `P` is required.

I found no contradiction in this calculation.

An independent specialist should nevertheless verify that all constants in the inherited small-mass cumulant theorem are indeed simultaneous through order `2P` on the stated common collision-space cover. The manuscript makes only this finite-order use and does not require all-order control.

## 5. Audit of the heterogeneous cumulant comparison

The new heterogeneous lemma addresses a point that deserved explicit treatment in the preceding report: the marked moment argument uses one section-state observable and several collision observables, rather than identical copies of one observable.

The proof correctly uses the multilinearity of the finite-product decoupling theorem. After splitting the chronologically ordered variables at a largest gap, it forms the product of the two unchanged marginal laws. For every subset meeting both sides, the original subset moment differs from its product-law value by an exponentially small quantity. Same-side subset moments are unchanged.

The displayed telescoping identity for each partition product shows that its change is controlled by the sum of its cross-gap subset-moment changes. The comparison cumulant vanishes because its variables split into two independent nonempty families.

The largest gap `d` satisfies

\[
 \operatorname{diam}\{t_1,\ldots,t_q\}
 \le(q-1)d.
\]

Thus exponential decay in `d` gives exponential decay in the diameter, and fixed-degree lattice counting yields anchored summability with an additional diameter weight.

The worked centered four-variable example is also correct. For centered `A,B,C,D`, the fourth cumulant contains the fourfold moment and the three pair products. Under a split between `B` and `C`, the fourfold moment factors as the same-side pair product; the cross pair moments factor through centered one-point means and vanish.

This supports the inherited parity argument for all fixed marked moments. I found no identical-distribution assumption hidden in the proof.

## 6. Audit of high-order damped unsmoothing

The high-order theorem retains the essential distinction between three mechanisms:

1. the finite spectral jet of the coarse smoothed twist;
2. the real residual-phase Taylor polynomial;
3. the fine smoothing of the mark and finitely many residual multipliers.

This distinction is mathematically necessary.

### 6.1 The remainder

With

\[
 X=|z|S_mu,
\]

the exact real Taylor formula through degree `2P-1` leaves a remainder bounded by

\[
 |X|^{2P}/(2P)!.
\]

The full small-mass moment sum therefore produces

\[
 M_a|z|^{2P}
 \sum_{b=1}^{P}(m\delta)^bL_\delta^{2P-b}.
\]

No damping is claimed for this remainder, and no term of the moment sum is suppressed.

### 6.2 Replacing the residual factors

For each lower degree `j`, the residual sum expands into `m^j` time tuples. Replacing each residual factor by its fine smoothing costs `O(epsilon)` per tuple after integration, by invariance and the uniform supremum bounds. Multiplication by `|z|^j` and summation over the fixed degrees gives

\[
 C_PM_a\epsilon(1+m|z|)^{2P-1}.
\]

This is the correct polynomial budget at fixed `P`.

### 6.3 The corrected chronological word

At degree `j`, sorting the residual times together with the actual-return mark gives `d=j+1<=2P` multipliers. The corresponding word is an exact alternating product of coarse twisted powers and smooth multipliers.

Repeated times give zero-length powers. Endpoint marks likewise produce zero-length initial or terminal powers. In all cases the nonnegative power lengths add to `m`.

Each smooth multiplier costs at most a fixed supremum bound times `C epsilon^(-2)`. Thus the maximal multiplier loss is `epsilon^(-4P)`.

The inherited real-frequency power bound applies separately to every coarse twisted power. Since the number of segments is fixed and their lengths sum to `m`, multiplying the bounds gives

\[
 C_{P,Q}e^{-cm|z|^2}.
\]

Summing all time tuples and residual degrees gives

\[
 C_{P,Q}M_a\epsilon^{-4P}
 (1+m|z|)^{2P-1}e^{-cm|z|^2}.
\]

The fine residual is never inserted into the twist. Therefore the fine scale does not reduce the coarse analytic neighborhood.

I found this chronology coherent. It is nevertheless a load-bearing place for independent collision-operator verification because the concrete application permits up to thirty-two smooth multipliers.

## 7. Audit of the anisotropic feasible region

The separate-width theorem depends on four independent scaling effects.

### 7.1 The stopping term

The inherited fourth-root stopping error is

\[
 CM_a|v|n^{-1/4}.
\]

The rescaled box has volume of order `n^Theta`, and `|v|` is at most a constant times `n^theta_*`. Hence its integrated stopping cost is

\[
 CM_an^{-1/4+\Theta+\theta_*}.
\]

The condition

\[
 \eta\le\frac14-\Theta-\theta_*
\]

is therefore exactly the available stopping margin.

### 7.2 The coarse analytic disk

With

\[
 \delta=n^{-\alpha}/4,
 \qquad
 z=v/\sqrt n,
\]

the first perturbative quantity has exponent

\[
 -\left(\frac12-\theta_*-2\alpha\right).
\]

It decays when

\[
 \alpha<\frac14-\frac{\theta_*}{2}.
\]

### 7.3 The finite spectral remainder

The second damping quantity has exponent

\[
 -\left[(Q-1)(1/2-\theta_*)-2\alpha(Q+1)\right].
\]

For a sufficiently large fixed `Q`, a strict positive margin exists exactly when

\[
 \alpha<\frac14-\frac{\theta_*}{2}.
\]

### 7.4 The residual moment sum

The `b`-block residual term has integrated power

\[
 \Theta+2P\theta_*-P+(1-\alpha)b.
\]

Because `alpha<1`, the largest exponent occurs at `b=P`. It equals

\[
 \Theta-P(\alpha-2\theta_*).
\]

Thus the condition

\[
 P(\alpha-2\theta_*)>\Theta+\eta
\]

makes every residual term strictly smaller than `n^(-eta)`, with enough power slack to absorb its fixed logarithm.

### 7.5 Feasibility

The coarse interval

\[
 2\theta_*<\alpha<\frac14-\frac{\theta_*}{2}
\]

is nonempty precisely when

\[
 \theta_*<\frac1{10}.
\]

After choosing `alpha`, fixed large `P` and `Q` exist. A sufficiently large fixed fine exponent `beta` controls both the insertion smoothing and the finite-product replacement. No order grows with `n`.

The change of variables

\[
 v=\sqrt n\,z
\]

has four-dimensional Jacobian `dv=n^2 dz`, exactly matching the raw normalization.

I found the displayed sufficient region internally consistent.

## 8. Audit of the concrete roof-direction box

For

\[
 \Theta=\frac3{25},
 \qquad
 \theta_*=\frac9{100},
 \qquad
 \alpha=\frac{19}{100},
 \qquad
 P=16,
 \qquad
 Q=29,
 \qquad
 \beta=20,
\]

the manuscript records the following margins.

### 8.1 Coarse analytic margin

\[
 \frac12-\theta_*-2\alpha
 =
 \frac12-\frac9{100}-\frac{38}{100}
 =
 \frac3{100}.
\]

### 8.2 Finite spectral remainder margin

\[
 (Q-1)(1/2-\theta_*)-2\alpha(Q+1)
\]

\[
 =28\cdot\frac{41}{100}
 -2\cdot\frac{19}{100}\cdot30
 =
 \frac2{25}.
\]

### 8.3 Insertion variation margin

\[
 \beta-\Theta
 =20-\frac3{25}
 =\frac{497}{25}.
\]

### 8.4 Fine residual-replacement margin

Since `2P-1=31`,

\[
 \beta-\Theta-(2P-1)(1/2+\theta_*)
\]

\[
 =20-\frac3{25}-31\cdot\frac{59}{100}
 =\frac{159}{100}.
\]

### 8.5 Residual moment margin

\[
 P(\alpha-2\theta_*)-\Theta
 =16\left(\frac{19}{100}-\frac{18}{100}\right)-\frac3{25}
 =\frac1{25}.
\]

### 8.6 Stopping margin

\[
 \frac14-\Theta-\theta_*
 =\frac14-\frac3{25}-\frac9{100}
 =\frac1{25}.
\]

The slow residual term is therefore

\[
 n^{-1/25}[\log(2+n)]^{16}.
\]

Because

\[
 \frac1{25}>\frac1{40},
\]

the fixed logarithm is absorbed, giving the stated `n^(-1/40)` rate. Every other residual block count has an additional power of `n^{-(1-alpha)}`.

The calculation is correct. The concrete box genuinely adds roof-frequency points beyond the inherited isotropic ball because

\[
 \frac9{100}>rac{67}{1400}.
\]

At the same time, the first three widths remain only `n^(1/100)` after rescaling.

## 9. Audit of the retained-rate union

The union

\[
 \mathcal U_n
 =
 \mathcal B_n^{\rm roof}
 \cup
 \{|v|\le2n^{67/1400}\}
\]

is handled by adding nonnegative integrals over the two regions. Overlap only enlarges the bound by a constant.

On the box, the new principal rate `n^(-1/40)` is faster than the inherited rate because

\[
 \frac1{40}>rac3{280}.
\]

The box variation loss is also much faster than `n^(-9/175)`. Therefore the old central error remains valid on the union.

This is a useful way of retaining every previously proved frequency while adding a long roof-direction extension. It is not equivalent to a larger isotropic ball.

## 10. Audit of the coordinatewise raw kernel

The active box cutoff is a product of four one-dimensional smooth cutoffs. For large `n`, the first three supports lie strictly inside the fundamental torus chart. The inverse kernel satisfies

\[
 |K_n^{\rm box}(x)|
 \le
 C_J\prod_{i=1}^{4}B_{n,i}
 \prod_{i=1}^{4}(1+B_{n,i}|x_i|)^{-J}.
\]

No discrete lattice coordinate is replaced by a continuous variable.

For the concrete widths,

\[
 n^2\prod_iB_{n,i}
 =n^{3/25}.
\]

The third coordinate is the collision count and has physical scale `n^(-49/100)`, so

\[
 nB_{n,3}=n^{51/100}.
\]

The high-count support is separated from the central count labels by order `n`. Consequently

\[
 n^2\sup|K_n^{\rm box}*\mathsf T^{a,L_n}|
 \le
 C_JM_an^{3/25-51J/100}.
\]

Choosing a fixed large Schwartz order gives any desired inverse power.

The missing Gaussian region outside the box has at least one coordinate of rescaled size `n^(1/100)`. Uniform ellipticity therefore gives

\[
 Ce^{-cn^{1/50}}.
\]

The remaining raw terms are exactly

\[
 n^2\mathcal E^{{\rm box},a,L_n}_{n,k,R,A},
\]

\[
 (2\pi)^{-4}n^2
 \mathcal C^{{\rm box},a,L_n}_{n,k,R}(B),
\]

and

\[
 \frac{n^2}{\pi B}
 A_2(n,L_n,R,w_{n,k,R}).
\]

The manuscript correctly recomputes the edge correction for the active box kernel and does not import an estimate from either preceding isotropic cutoff.

## 11. What revision 25 closes from the preceding report

Revision 25 closes or materially advances the following points.

### 11.1 It removes the fixed cubic-order restriction

The damping argument now works after retaining every residual degree through an arbitrary fixed odd degree `2P-1`. This is a real theorem, not a suggestion that one should “take more Taylor terms.”

### 11.2 It gives an explicit heterogeneous cumulant proof

The marked cumulant comparison is no longer left to an analogy with identical collision factors.

### 11.3 It reaches substantially larger roof frequencies

The prescribed-count physical roof width improves to `n^(-41/100)`, corresponding to rescaled exponent `9/100`, while retaining the actual return count, actual mark, raw normalization, and old central rate on the union.

### 11.4 It provides an active coordinatewise raw identity

The correct product kernel, high-count correction, Gaussian tail, and exact remaining raw quantities are displayed at the new scales.

These are all meaningful achievements.

## 12. The full fixed-count complementary integral remains open

The new box should not be confused with the complete small-frequency complement.

The target isotropic physical radius `n^(-2/5)` corresponds to the rescaled ball

\[
 |v|\lesssim n^{1/10}.
\]

The old isotropic theorem covers

\[
 |v|\lesssim n^{67/1400}
 \approx n^{0.04786}.
\]

The new box covers

\[
 |v_1|,|v_2|,|v_3|\lesssim n^{1/100},
 \qquad
 |v_4|\lesssim n^{9/100}.
\]

Its union with the old sphere leaves, among others:

1. frequencies with a discrete-coordinate component between `n^(67/1400)` and `n^(1/10)`;
2. mixed directions in which several coordinates are simultaneously larger than the box widths;
3. roof frequencies between `n^(9/100)` and `n^(1/10)`;
4. the parts of the farther annulus not contained in either set;
5. compact nonzero lattice/count torus frequencies;
6. the relevant full peripheral return regimes;
7. growing roof frequencies beyond the local scale;
8. the final far-roof splice.

The anisotropic theorem shows that one coordinate can approach exponent `1/10` if the sum budget is respected. It does not yield the isotropic vector `(1/10,1/10,1/10,1/10)`, for which both `theta_*<1/10` and `Theta+theta_*<1/4` fail at the endpoint.

No impossibility conclusion follows; a different argument may cover the missing regions. They are simply not controlled by revision 25.

## 13. The finite-band residual integral remains open

The new transform theorem concerns the full marked law on the active box. The exact raw inversion uses the finite-count edge-subtracted residual.

Outside the active cutoff one still needs a fixed-count integral estimate for

\[
 (1-\chi_n^{\rm box})\widehat Q^{a,L_n},
\]

through all remaining lattice, count, roof, and peripheral regimes. The current theorem exposes this quantity as

\[
 \mathcal C^{{\rm box},a,L_n}_{n,k,R}(B)
\]

but does not prove that its normalized contribution vanishes.

A full proof must treat this residual with the same extraction and weight used in the raw identity. A bound for the unextracted full characteristic function on a different region is not automatically a bound for the active residual complement.

## 14. The long-time derivative budget remains open

At each fixed finite packet, the constructible extraction gives a `W^{2,1}` residual and a finite number

\[
 A_2(n,L,R,w)
 =
 \sum_\ell
 \|\partial_t^2r^{w,L}_{n,R}(\ell,\cdot)\|_1.
\]

For the raw theorem, however, the count cutoff satisfies

\[
 L_n\asymp n.
\]

The paper still needs a uniform quantitative bound on the actual preparation data, including:

- the number and geometry of singular cells;
- the number of prepared germs;
- the rational exponents and their separation from critical thresholds;
- logarithmic degrees;
- germ radii;
- power-logarithm coefficients;
- coalescing critical values;
- inverse-coarea Jacobians;
- regular-interval second-derivative integrals;
- dependence on `R,n` and the weight.

The new small-mass moments concern bounded collision sums. They do not estimate these second derivatives of pushed-forward densities.

## 15. The active-kernel local edge correction remains open

For the box kernel, the combined local edge quantity is

\[
 \mathcal E^{{\rm box},a,L_n}_{n,k,R,A}
 =
 \operatorname*{ess\,sup}_{\mathcal W_{n,R,A}}
 |e^{a,L_n}-K_n^{\rm box}*E^{a,L_n}|.
\]

The raw theorem requires

\[
 n^2\mathcal E^{{\rm box},a,L_n}_{n,k,R,A}	o0
\]

uniformly on the stated central windows and in the physical radius.

Revision 25 correctly permits this quantity to be infinite before the density germs are uniformly estimated. It supplies no asymptotic smallness theorem for it.

Changing from an isotropic kernel to the box kernel changes the convolution geometry. The previous edge quantities cannot be substituted without a new proof.

## 16. Weighted raw denominators remain open

The Fourier theorem applies to a bounded-BV function at one actual return. The structural finite-count extraction additionally requires finite-record subanalytic admissibility of the exact weight

\[
 w_{n,k,R}=c_*a\circ(F_R^*)^k.
\]

These two classes have a nontrivial intersection, but they are not identical to:

- arbitrary `L^2` weights in the averaged-orbit theorem;
- logarithmic return-window events;
- arbitrary finite-record subanalytic weights;
- exact physical-time and lattice indicators.

The same-event corollary divides by its unchanged probability and gives a central Fourier comparison. It does not prove the raw-scale denominator asymptotic needed in the downstream conditional local theorem.

A complete weighted raw theorem must establish, for the same actual indicator class:

1. the full fixed-count complementary integral;
2. the long-time derivative budget;
3. the active-kernel local edge estimate;
4. the raw denominator asymptotic;
5. stability of the weight class under every extraction and replacement step.

## 17. Exact physical-event replacement remains open

No completed-return event is replaced in revision 25. The event and denominator in the same-event theorem are identical throughout.

The downstream application still requires a relative comparison between:

- the event formulated at completed actual returns; and
- the exact physical-time/lattice observation event.

An absolute clock or unfinished-return estimate is insufficient under a rare lattice constraint unless it is small relative to the exact denominator at the raw scale.

The all-fixed-moment and high-order residual estimates do not establish this relative event comparison.

## 18. Correctness assessment

Within the scope of the reviewed text, I found no decisive contradiction in the new mathematics.

In particular:

- the small-mass partition exponents are correct;
- the heterogeneous cumulant comparison is explicit and coherent;
- the fine and coarse smoothing scales remain separate;
- the residual and spectral degrees have distinct roles;
- the chronological power lengths sum to the full collision interval;
- repeated times and endpoint marks are included;
- every residual block count is retained;
- the anisotropic feasibility inequalities are nonempty;
- the concrete exponent ledger is correct;
- the four-dimensional raw Jacobian is present;
- the union retains the old isotropic theorem;
- the active count coordinate is used in the high-count correction;
- the active-kernel edge and residual terms remain exposed.

This conclusion is not a formal proof certificate. Several inherited and new continuum steps remain sufficiently specialized to require independent human checking.

## 19. Items requiring specialist verification

An independent billiards and anisotropic-operator specialist should examine at least the following points.

### 19.1 Simultaneous finite-order constants

The small-mass theorem requires inherited cumulant bounds through order `2P=32` for the concrete application. The argument is fixed-order, but the common collision-space constants and multiplier conventions should be checked carefully.

### 19.2 Heterogeneous block comparison

The independent-block comparison should be verified for every subset moment and for factors on both sides of the actual mark, including repeated times and zero-length intervals.

### 19.3 Thirty-two multiplier chronological words

The product of local collision-space power estimates and smooth-multiplier estimates should be checked on every chart and across all common-space identifications. The number of factors is fixed but large.

### 19.4 Spectral versus residual degrees

The concrete use of residual degree `31` with spectral degree `29` is logically permissible because the two estimates have separate inputs. This separation is load-bearing and should be confirmed against the precise norms of the local collision-space construction.

### 19.5 Separate-width frequency normalization

The product box, physical/rescaled coordinate conventions, torus restriction, and raw `n^2` normalization should be independently checked against the mixed counting/Lebesgue Fourier convention.

### 19.6 Product-kernel count separation

The high-count correction uses the third frequency coordinate, not the larger roof width. The coordinate order and the scale `nB_{n,3}=n^(51/100)` should be checked against the exact record convention.

### 19.7 Weight-class intersection

The marked BV theorem and the finite-record subanalytic extraction use distinct regularity structures. The exact class used in every weighted raw identity should be verified rather than inferred from either structure alone.

## 20. Top-four significance assessment

The manuscript now contains a broad and technically sophisticated package:

- Gaussian and functional laws for an actual unbounded return record;
- uniform covariance positivity;
- growing central Fourier comparisons;
- single-return and logarithmic-window marks;
- all fixed marked Gaussian moments;
- measurable phase rigidity and complete collision-phase arithmetic;
- quantitative collision and return function defects;
- exact peripheral phase lifting;
- finite-rank compressed resolvent statements;
- direct averaged estimates for the uncompressed orbit;
- finite-count constructible edge extraction;
- exact count-localized raw identities;
- isotropic prescribed-count Fourier bands;
- anisotropic prescribed-count Fourier boxes.

Several ideas are interesting in their own right. The bounded compensation, exact marked stopping, complete phase arithmetic, observed-count localization, finite power-logarithm extraction, damped residual expansion, and separate-width fixed-count theorem all merit specialist attention.

At the requested benchmark, however, the article is still organized around a raw mixed-density local limit theorem whose central mechanisms remain unfinished. The missing full complement, long-time derivative sum, local edge smallness, weighted denominator, and exact-event replacement are the steps that convert the extensive structural framework into the announced endpoint.

Alternatively, a top-four claim might arise from a broad general theorem abstracting the compensation, multiscale stopping, high-order damped unsmoothing, or anisotropic-box method and applying it to several substantially different hyperbolic systems. Revision 25 remains focused on one carefully designed triangular Lorentz family and does not yet supply such breadth.

I therefore do not regard revision 25 as meeting the closure and breadth threshold of *Annals*, *Acta*, *Inventiones*, or *JAMS*.

## 21. Required work before another top-four review

### A. Close the complete prescribed-count Fourier complement

Prove one compatible estimate for the actual full law or exact edge-subtracted residual from the present active region through:

- the remaining small-frequency directions;
- the full isotropic scale toward `n^(1/10)`;
- compact nonzero lattice/count frequencies;
- all relevant peripheral return phases;
- growing roof frequencies;
- the far-roof splice.

The result must apply at the prescribed count, with the raw four-dimensional normalization and the actual weight class used in inversion.

### B. Quantify the finite-count preparation at linear cutoff

For `L_n` proportional to `n`, prove a uniform bound on

\[
 A_2(n,L_n,R,w)
\]

strong enough to choose the far-roof cutoff while keeping the normalized error small. Track the actual number, radii, exponents, coefficients, and derivative integrals of all prepared germs.

### C. Prove the active-kernel local edge estimate

For the box kernel actually used in revision 25, prove the normalized smallness of

\[
 e^{a,L_n}-K_n^{\rm box}*E^{a,L_n}
\]

on every required central window. Do not import an estimate from a different kernel.

### D. Close the finite-band residual integral

Control

\[
 \mathcal C^{{\rm box},a,L_n}_{n,k,R}(B)
\]

on the same frequency partition and with constants compatible with the derivative and edge budgets.

### E. Complete the weighted raw theory

For the actual downstream indicators, prove weighted versions of the complete complement, derivative budget, edge correction, and denominator asymptotic. State one stable common weight class.

### F. Prove relative physical-event replacement

Compare the completed-return and exact physical-time/lattice events at the raw denominator scale. The comparison must be relative, not only absolute.

### G. Obtain independent specialist verification

Before another claim at this benchmark, the collision-space, cumulant, chronological-word, finite-preparation, and mixed Fourier-normalization arguments should be checked by independent experts.

## 22. Presentation and source comments

1. The title and physical problem remain unchanged.
2. Theorem O should continue to be called a box or anisotropic theorem, not a full-annulus theorem.
3. Both physical and rescaled widths should remain adjacent to every frequency statement.
4. The residual degree `2P-1` and spectral degree `Q` should remain visibly distinct.
5. The fixed-order quantifiers should remain explicit wherever `P` or `Q` appears.
6. The concrete value `P=16` should not be presented as an all-orders estimate.
7. The fine scale should remain absent from the twisted-operator definition.
8. The `b=1` connected residual term should remain displayed.
9. The old isotropic theorem should remain separate from the new box theorem.
10. The union should not be drawn or described as a larger isotropic ball.
11. The coordinate order `(K_1,K_2,N,T)` should remain explicit near the box kernel.
12. The count-coordinate separation must continue to use the third width.
13. The active-kernel edge correction should remain defined immediately before use.
14. Extended-real qualifications should remain wherever that edge quantity may be infinite.
15. BV and finite-record subanalytic weight classes should remain distinguished.
16. Same-event conditioning should not be described as physical-event replacement.
17. The induced covariance statement should remain Cesaro, not absolutely summable.
18. Exact-source CI should remain described as execution evidence, not proof certification.
19. The dependency appendix is useful and should be retained.
20. The next revision should prioritize closure of a full raw term rather than adding another disconnected interface.

## 23. Final assessment

Revision 25 is a serious and positive response to the preceding referee report. It proves an arbitrary fixed-order damped-unsmoothing theorem, supplies the missing heterogeneous cumulant comparison, establishes a nontrivial family of coordinatewise prescribed-count bands, reaches substantially larger roof frequencies, preserves the inherited isotropic result, and gives the correct active-kernel raw identity.

I found no decisive counterexample in those new arguments.

The paper nevertheless does not yet prove its organizing raw mixed-density local limit theorem. The new box does not cover the full isotropic complement; the finite-band residual, long-time derivative sum, local edge correction, weighted denominator, and exact physical-event replacement remain open.

At the requested four-journal benchmark, the appropriate recommendation is therefore **reject in the present form**.

A future top-four resubmission should be judged on whether it closes these remaining raw mechanisms or replaces the current one-family endpoint by a genuinely broad general theorem with several nontrivial applications.