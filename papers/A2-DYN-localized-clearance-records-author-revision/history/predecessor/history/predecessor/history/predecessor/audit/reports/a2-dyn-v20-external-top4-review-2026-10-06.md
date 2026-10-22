# External top-four referee report on A2-DYN revision 20

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v20-referee-response-2026-10-06`, `revision/a2-dyn-v20-referee-copy-2026-10-06`  
**Reviewed commit:** `b5b209000bbef852076f413ef4f718137aeb4dd3`  
**Reviewed repository tree:** `4461ecd56fd7a02ca0ae2fe88484ba3942d68205`  
**Frozen ordinary paper tree:** `cbfa76a8957d3d327655a9969d55cb4a9d3e24bb`  
**Active manuscript directory:** `papers/A2-DYN-v20-referee-response`  
**Immediate author baseline:** revision 19 at `e56eed31c3b7d70ceb71a7f4b075092c2bd3e98d`  
**Controlling report:** `reviews/a2-dyn-v19-external-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `da89f3ae6f0b9e5fedb1ae6aa7a9dcfc20f623aa` / `c41b48727e3b3278f65ea8aed6c861fb0086c88e`  
**Date:** 6 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards-specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 20 is a genuine and mathematically useful response to the most concrete objection in the revision-19 report. It does not conceal the incompatibility between the displayed grid-consistency scale and the local compressed-resolvent scale. It proves that incompatibility explicitly and then changes methods: short-lag Gaussian estimates are used to control Gram matrices of the exact, uncompressed return orbit. The resulting theorem gives radius-uniform mean-square cancellation on every sufficiently long moving window throughout the physical annulus

\[
 2n^{-99/200}\le |z|\le n^{-2/5},
\]

with rate `n^(-4/495)`. It also gives arbitrary `L^2` initial weights, exact unchanged-event normalization, fixed and terminal actual-return marks, full-angle cyclic spectral arc bounds, an exterior Abel estimate for the constant vector, and a Cauchy scaling law for the corresponding spectral probability.

I found no decisive counterexample in the two new mathematical modules:

- `core/44_direct_orbit_bounds.tex`;
- `core/45_weighted_spectral_averages.tex`.

The pointwise short-lag estimate is derived from the actual return characteristic function rather than from the integrated major arc. The Gram-matrix row-sum argument is exact. The long interval is partitioned into exact orbit blocks, not projected or Markov blocks. The conditional normalization is `1/p`, as it should be for a squared `L^2` estimate with weight `1_A/p`. The peripheral arc and Abel estimates apply to the exact cyclic spectral measure of the constant vector. The Cauchy limit is a spectral statement and is not confused with the physical Gaussian law.

These are meaningful advances. They provide a direct theorem on the uncompressed dynamics and remove the need for the incompatible spatial grid in the averaged conclusions.

The negative recommendation is nevertheless unchanged at the requested benchmark. The organizing endpoint of the manuscript is a parameter-uniform raw mixed-density local limit theorem at each prescribed return count. Revision 20 proves Cesaro or mean-square cancellation over a window of return counts and cyclic-vector spectral estimates. It does **not** prove the fixed-count complementary Fourier integral required by raw inversion. In particular, it does not prove decay of the physical characteristic function at the specified count `n`, decay of the edge-subtracted residual at that count, or an uncompressed operator-power estimate from which such decay follows.

The manuscript itself correctly records this distinction. The normalized annular mean-square integral is too weak after the raw `n^2` normalization, and the Cauchy spectral limit controls fixed rescaled spectral test frequencies, whereas the Fourier index relevant to the raw theorem grows polynomially across the annulus. The finite-count raw extraction also continues to require uniform long-time derivative and local-edge estimates. The weighted exact-conditioning application continues to require weighted raw estimates and a relative physical-event replacement.

At the four-journal standard, these are central missing mechanisms rather than presentation details. The unconditional package is substantial and may support a strong specialist paper after independent expert review and a reorganization around the completed Gaussian, phase, finite-extraction, window, and averaged-orbit theorems. That is a different editorial claim from the raw LLT currently organizing this article.

## 2. Frozen source, chronology, and exact qualification

The two named revision-20 author branches resolve to the same commit:

`b5b209000bbef852076f413ef4f718137aeb4dd3`.

The commit has repository tree

`4461ecd56fd7a02ca0ae2fe88484ba3942d68205`.

Its immediate author baseline is the reviewed revision-19 commit

`e56eed31c3b7d70ceb71a7f4b075092c2bd3e98d`,

whose frozen ordinary paper tree is

`57ea4229c9e344f9d61fd08be6ef7f7954d29feb`.

Revision 20 preserves all forty-three inherited core modules and adds:

- `core/44_direct_orbit_bounds.tex`;
- `core/45_weighted_spectral_averages.tex`.

Forty-one inherited core files, every inherited Python file, and the bibliography are byte-identical. Seven exact inherited edits are recorded. Five edit the introduction and include the two new modules; one places the v19 scale incompatibility warning before the compressed finite-time comparison; one clarifies the analytic-unit source of the convergent one-variable power--logarithm expansions in the finite-count extraction.

The final ordinary paper tree is

`cbfa76a8957d3d327655a9969d55cb4a9d3e24bb`.

The exact-source qualification completed successfully on both reviewed branches at the reviewed SHA:

- response branch run `37462184536`;
- referee-copy branch run `37462214303`.

For the response branch, exact checkout, source archiving, native TeX and diagnostic installation, verification/build, and artifact upload all completed successfully. The response artifact is

`11413918801`,

named

`a2-dyn-v20-b5b209000bbef852076f413ef4f718137aeb4dd3`,

with digest

`sha256:7c1e507ffaf246265993d1989f8a28c4df99a9f5024d1a72b0ccb4d50944050c`.

These facts establish exact source identity and successful execution of the declared finite checks and native build. They do not certify the continuum billiard arguments, the constructible-preparation uniformity, the missing complementary integral, or the full raw theorem.

The present review branch starts directly from the reviewed author commit and adds only this report under

`reviews/a2-dyn-v20-external-top4-review-2026-10-06/`.

No manuscript source, author branch, workflow, earlier report, or unrelated repository path is modified.

## 3. What revision 20 actually proves

Let

\[
 \mathcal U_{R,z}f=e^{-iz\cdot g_R}f\circ F_R^*,
 \qquad g_R=G_R-\bar G_R,
\]

on `L^2(nu_R^*)`, and let `e=1`. This is the exact unitary twisted return Koopman operator. Its constant-vector correlations are

\[
 c_{j,R}(z)=\langle e,\mathcal U_{R,z}^j e\rangle
 =\int e^{-iz\cdot U_{j,R}}\,d\nu_R^*,
 \qquad U_{j,R}=J_{j,R}-j\bar G_R.
\]

Revision 20 adds the following unconditional conclusions.

### 3.1 The compressed-grid incompatibility is made explicit

If the displayed v19 finite-time grid error is required to vanish at time `n`, with collision cutoff `L_n>=n`, then

\[
 \log(1/h_n)\ge C_gL_n+2\log n+o(1).
\]

Hence the reconstructed regularity logarithm is at least a positive multiple of `n`. On the physical annulus, the local compressed-resolvent quantity satisfies

\[
 \rho_n^2\{1+\log(C_0/(h_n\rho_n))\}
 \ge c n^{1/100},
\]

at the lower annular boundary, and therefore leaves the local resolvent domain. This proves that the two displayed v19 estimates cannot be concatenated with a common vanishing-grid-error scale.

The proposition does not claim that every possible approximation has a large actual error. It identifies the incompatibility of the proved upper-bound interfaces, exactly as requested by the preceding referee.

### 3.2 A pointwise short-lag Gaussian estimate

For

\[
 \gamma=\frac1{28}-\frac1{200}=\frac{43}{1400},
\]

the manuscript proves, uniformly in the radius,

\[
 \left|c_{j,R}(z)-e^{-jz^{\mathsf T}D_Rz/2}\right|
 \le Cj^{-\gamma}\sqrt{\log(2+j)}
\]

whenever

\[
 |z|\le2j^{-99/200}.
\]

This is derived from the frequency-explicit collision estimate and the actual stopping comparison before frequency integration. It is not inferred from the existing integrated central theorem.

### 3.3 A finite Gram-row budget

For `r=|z|`, set

\[
 \alpha=\frac{200}{99},
 \qquad
 m(r)=\lfloor r^{-\alpha}\rfloor,
 \qquad
 \kappa=\alpha-2=\frac2{99}.
\]

All lags below `m(r)` lie inside the pointwise Gaussian band. Uniform ellipticity and summation of the error give

\[
 \mathcal B_m(R,z)
 =1+2\sum_{j=1}^{m-1}|c_{j,R}(z)|
 \le C\{r^{-2}+m^{1-\gamma}\sqrt{\log(2+m)}\},
\]

and

\[
 \frac{\mathcal B_m(R,z)}m\le Cr^{2/99}.
\]

The positive exponent margin is

\[
 \alpha\gamma-\kappa
 =\frac{29}{693}>0.
\]

### 3.4 Direct mean-square estimates for the exact orbit

For any unitary `U`, unit vector `e`, and a block of orbit vectors `U^(N+j)e`, the Gram matrix has row sums bounded by `B_m`. The manuscript proves both the synthesis and adjoint analysis inequalities. Applying these inequalities blockwise gives, for every `T>=m(r)`, every integer `N`, every test vector `b`, and every peripheral phase `xi`,

\[
 \frac1T\sum_{j<T}
 |\langle b,\mathcal U_z^{N+j}e\rangle|^2
 \le Cr^{2/99}\|b\|_2^2,
\]

and

\[
 \left\|\frac1T\sum_{j<T}
 e^{-ij\xi}\mathcal U_z^{N+j}e\right\|_2^2
 \le Cr^{2/99}.
\]

These are statements about the exact uncompressed return dynamics. No fitted spatial grid, truncated return operator, Markov replacement, induced mixing theorem, or long-pullback BV estimate is used.

### 3.5 One feasible scale on the entire small annulus

On

\[
 \mathcal A_n=\{z:2n^{-99/200}\le|z|\le n^{-2/5}\},
\]

one has

\[
 m(|z|)<n/4,
 \qquad
 |z|^{2/99}\le n^{-4/495}.
\]

Thus the preceding mean-square estimates hold uniformly throughout the annulus for every averaging horizon `T>=n`, every later starting index, and every peripheral angle.

### 3.6 Arbitrary square-integrable weights and unchanged events

For every `a in L^2`,

\[
 \frac1T\sum_{j<T}
 \left|\int a\,e^{-iz\cdot U_{N+j,R}}d\nu_R^*\right|^2
 \le Cn^{-4/495}\|a\|_2^2.
\]

For one unchanged event `A` of exact probability `p>0`, taking `a=1_A/p` gives

\[
 \frac1T\sum_{j<T}
 \left|\mathbb E[e^{-iz\cdot U_{N+j,R}}\mid A]\right|^2
 \le Cp^{-1}n^{-4/495}.
\]

The event is the same at every averaging index. A fixed actual-return mark and a moving terminal actual-return mark are also treated exactly through the unitary and its inverse.

### 3.7 Cyclic peripheral arcs and exterior Abel bounds

Let `varsigma_(R,z)` be the spectral probability of the constant vector for `U_(R,z)`. For every peripheral center `xi`, the mass of an arc of radius `1/m(r)` is bounded by

\[
 \varsigma_{R,z}\{
   \operatorname{dist}(\theta-\xi,2\pi\mathbb Z)\le m^{-1}
 \}
 \le Cr^{2/99}.
\]

For `0<s<1` with `(1-s)m<=1`,

\[
 \|(1-s)(I-se^{-i\xi}\mathcal U_z)^{-1}e\|_2^2
 \le Cr^{2/99}.
\]

These estimates cover every angle, but only for the specified cyclic vector. They are not unit-circle inverses or operator-norm resolvent bounds.

### 3.8 A spectral Cauchy scaling law

For `z=ru`, `|u|=1`, let the principal spectral angle be divided by `r^2`. The resulting probability converges, uniformly in the physical radius and direction, to the Cauchy law with scale

\[
 \frac12u^{\mathsf T}D_Ru.
\]

The proof combines the true one-return second moment, principal-angle rounding, and the physical Gaussian theorem at lag `floor(t/r^2)`. The physical return record remains Gaussian. The Cauchy law concerns the constant vector's spectral probability.

## 4. Audit of the grid-scale proposition

The scale calculation in Proposition 44.1 is correct.

Squaring

\[
 n\sqrt{h_n(1+|z_n|)e^{C_gL_n}}\to0
\]

forces

\[
 \log(1/h_n)-C_gL_n-2\log n-\log(1+|z_n|)\to+\infty.
\]

Since `L_n>=n`, the reconstructed logarithmic budget is at least `cn`. At the lower physical annular radius,

\[
 \rho_n^2\ge4n^{-198/200},
\]

so multiplication by a budget of order `n` gives at least `cn^(1/100)`. This leaves the stated local-resolvent domain.

The revision is commendably explicit that this does not contradict either compressed theorem separately. It is an incompatibility of the two proved interfaces. The direct averaged argument genuinely avoids both interfaces.

## 5. Audit of the pointwise short-lag estimate

The exponent bookkeeping is coherent.

With

\[
 v=-\sqrt j\,z,
 \qquad
 \delta=\frac14j^{-1/14},
 \qquad
 |v|\le2j^{1/200},
\]

the seven displayed polynomial margins are

\[
 \frac1{14},
 \quad
 \frac1{28}-\frac1{200},
 \quad
 \frac1{14}-\frac2{200},
 \quad
 \frac3{14}-\frac1{200},
 \quad
 \frac1{14}-\frac3{200},
 \quad
 \frac15-\frac1{200},
 \quad
 1-rac2{200}.
\]

The unique smallest margin is `43/1400`, arising from removal of the collision smoothing and carrying the square-root logarithm. The analytic-domain inequalities

\[
 \frac6{14}+rac3{200}<\frac12,
 \qquad
 \frac2{14}+rac1{200}<\frac12
\]

hold strictly. The actual stopping and rounding terms have larger margins. The use of `s_R` as the initial density gives the normalized actual section law.

I found no scale or normalization error in this lemma.

## 6. Audit of the short-lag summation

For `j<m(r)`,

\[
 rj^{99/200}\le1,
\]

so every required correlation lies inside the pointwise band. The Gaussian contribution sums to `O(r^(-2))`. The pointwise remainder sums to

\[
 O(m^{1-\gamma}\sqrt{\log m}).
\]

After division by `m`, these become

\[
 O(r^{\alpha-2})=O(r^{2/99})
\]

and

\[
 O(r^{\alpha\gamma}\sqrt{|\log r|}).
\]

Because

\[
 \alpha\gamma=\frac{43}{693}
 >\frac{14}{693}=rac2{99},
\]

the logarithm is absorbed. No estimate of a lag `j>=m` is used.

This is precisely the appropriate way to obtain a finite Gram budget without assuming long-time correlation decay.

## 7. Audit of the exact Gram argument

The orbit vectors are

\[
 \mathcal U_z^{N+j}e.
\]

Their Gram entries are

\[
 \langle e,\mathcal U_z^{j-i}e\rangle,
\]

independent of `N`. Every absolute row sum is bounded by `B_m`. Expansion of the quadratic form and the elementary inequality

\[
 2|a_i||a_j|\le |a_i|^2+|a_j|^2
\]

give the synthesis estimate. Taking adjoints gives the analysis estimate. Multiplication by arbitrary unit scalars conjugates the Gram matrix by a diagonal unitary.

For a long interval, each analysis block contributes at most `B_m||b||^2`; there are at most `2T/m` blocks. For synthesis, the triangle inequality across blocks gives the stated `4B_m/m` bound after normalization.

The synthesis estimate is intentionally a Cesaro estimate; it does not claim cancellation between separate blocks. This makes the proof robust but also explains why it cannot yield a fixed-time coefficient.

I found this Hilbert-space argument correct.

## 8. Audit of the full-annulus scaling

At the lower annular radius,

\[
 |z|^{-200/99}\le2^{-200/99}n<n/4.
\]

At the upper annular radius,

\[
 |z|^{2/99}\le n^{-4/495}.
\]

Thus one lag-window construction works throughout the entire annulus and for all averaging horizons `T>=n`. This genuinely resolves the v19 mesh problem for the new averaged statement.

It does not resolve the fixed-count complementary integral; the theorem states this limitation accurately.

## 9. Audit of weights, unchanged events, and actual marks

The weighted normalization is correct. With the convention

\[
 \langle f,g\rangle=\int\overline f g\,d\nu_R^*,
\]

taking `b=conjugate(a)` identifies the matrix coefficient with

\[
 \int a\,e^{-iz\cdot U_j}d\nu_R^*.
\]

For an event `A`, the weight `1_A/p` has squared `L^2` norm exactly `1/p`, not `1/p^2`. Hence the conditional mean-square cost is `p^(-1)`.

The fixed-mark change of variables leaves a test vector of norm `||a||_2` independent of the averaging index. For the moving terminal mark, changing variables to the terminal return converts the expression into a matrix coefficient of the inverse unitary. The inverse orbit has the same absolute lag correlations.

These arguments use the genuine return map. No deterministic collision-clock surrogate or event factorization is introduced.

The essential limitation is equally clear: the event must remain unchanged across the averaging window. An exact physical observation reselected at every return count is a different family of weights.

## 10. Audit of the cyclic arc and Abel estimates

For the arc estimate, the squared norm of the modulated Cesaro sum is the spectral integral of the squared normalized Dirichlet kernel. On an arc of radius `1/m`, that kernel is bounded below by an absolute positive constant. The synthesis estimate therefore bounds the arc mass by `B_m/m`.

For the Abel estimate, the norm-convergent Neumann series is divided into blocks of length `m`. A block has norm at most

\[
 s^{km}\sqrt{mB_m}.
\]

When `(1-s)m<=1`,

\[
 \frac{1-s}{1-s^m}\le\frac C m,
\]

and the normalized resolvent vector is bounded by `C sqrt(B_m/m)`. Squaring gives the stated result.

No normality, absolute continuity of the spectral measure, or operator-norm inverse on the unit circle is used. I found no defect in these arguments.

## 11. Audit of the spectral Cauchy limit

The one-return second moment gives

\[
 1-\operatorname{Re}c_{1,R}(ru)\le Cr^2.
\]

For the principal angle `theta in [-pi,pi)`, this implies

\[
 \int|\theta|\,d\varsigma_{R,ru}\le Cr.
\]

For fixed real `t`, choosing

\[
 j=\lfloor |t|/r^2\rfloor
\]

changes the spectral characteristic function at `t/r^2` to the integer coefficient `c_j(ru)` at cost `O(r)`. The physical Gaussian theorem applies because `r sqrt(j)` remains in a fixed compact set for fixed `t`, and gives

\[
 c_j(ru)\to
 \exp\left(-\frac12|t|u^{\mathsf T}D_Ru\right).
\]

This is the characteristic function of the asserted Cauchy family. Compactness of the radius interval and unit sphere upgrades sequential convergence to the stated uniform bounded-Lipschitz convergence.

The argument is correct at the level claimed. It neither proves a density for `varsigma_(R,z)` at fixed nonzero `z` nor gives convergence of characteristic functions at test frequencies growing with `r^(-1)`.

## 12. Clarification of the finite-count power--logarithm germs

Revision 20 adds a useful clarification to the fixed-count extraction.

The twice-differentiated one-variable representation is not obtained by differentiating a merely formal asymptotic series. The manuscript identifies the strong analytic unit `U composed with phi`, with `U` analytic on a neighborhood of the monomial-image closure. After clearing denominators in one variable, bounded rational monomials become nonnegative integral powers of a root variable. The rational prefactor has only a finite Laurent principal part, and a positive generator has the form `x^r u(x^(1/q))` with `u(0)>0`, so its logarithm splits into `r log x` plus a convergent analytic series.

This makes the convergent Laurent--Puiseux--logarithm expansion, and hence two termwise differentiations after removal of the finite jet, credible. It addresses the principal source-level verification request in the v19 report.

It does not provide any uniform-in-`n` control of germ radii, coefficients, exponent gaps, the number of singular points, or the second-derivative budget.

## 13. What revision 20 closes from the v19 report

Revision 20 closes or materially advances the following points.

1. **The scale conflict is no longer implicit.** The incompatible compressed interfaces are stated and proved incompatible on the target annulus.
2. **There is a direct theorem on the exact uncompressed dynamics.** No spatial mesh is used in Theorem K.
3. **The whole small annulus has one feasible averaging scale.** The lag scale is explicit and radius-uniform.
4. **The result permits arbitrary `L^2` weights.** No BV reconstruction of the final test vector is needed.
5. **Every peripheral angle is covered at the cyclic-vector level.** Both a local arc-mass estimate and an exterior Abel estimate are proved.
6. **The spectral concentration scale is identified.** The constant vector's principal spectral angle has a uniform Cauchy scaling law.
7. **The constructible-germ convergence source is stated.** The power--logarithm jet proof no longer relies on an unexplained differentiation of an asymptotic expansion.
8. **The exact v20 source is remotely qualified.** Both author branches pass the read-only exact-SHA workflow.

These are real advances. The report should not describe revision 20 as a repackaging of revision 19.

## 14. Why the fixed-return complementary integral remains open

### 14.1 A mean-square window does not control the prescribed count

The raw theorem needs an estimate at one specified return count `n`. Revision 20 proves

\[
 \frac1T\sum_{j<T}|c_{N+j,R}(z)|^2
 \le Cn^{-4/495}
\]

for `T>=n` and frequencies in `A_n`.

This implies that most indices in a long window are good, with an explicit exceptional fraction. It does not identify the particular index required by the local limit theorem. Translation invariance of the Gram matrix does not turn a Cesaro estimate into a pointwise coefficient estimate.

The distinction is structural. A spectral probability can have small mass in every arc of one prescribed width and still possess fine-scale arithmetic capable of producing large Fourier coefficients at selected large integers. Additional spectral regularity or a direct fixed-time argument is required.

### 14.2 The normalized annular integral has the wrong raw scale

The new theorem gives

\[
 \frac1{|\mathcal A_n|}
 \int_{\mathcal A_n}
 \frac1T\sum_{j<T}|c_{N+j,R}(z)|^2dz
 \le Cn^{-4/495}.
\]

Since

\[
 |\mathcal A_n|\asymp n^{-8/5},
\]

Cauchy--Schwarz gives, after the raw four-dimensional normalization `n^2`, only a budget of order

\[
 n^{2/5-2/495},
\]

which grows rather than tends to zero. Thus even the return-count average of the unnormalized raw annular integral is not closed by the present exponent.

### 14.3 The Cauchy limit is a fixed-test-frequency result

For the raw coefficient at return count `n`, the spectral Cauchy scaling would be tested at

\[
 t_n=n|z|^2.
\]

Across the annulus,

\[
 4n^{1/100}\lesssim t_n\le n^{1/5}.
\]

These test frequencies diverge. The proved Cauchy convergence controls each fixed `t`; weak convergence and bounded-Lipschitz convergence do not imply convergence of characteristic functions on a polynomially growing `t_n` range. Therefore the exponential decay of the limiting Cauchy characteristic function cannot be inserted into the fixed-count raw inversion without a quantitative growing-frequency theorem.

### 14.4 The cyclic vector is not the edge-subtracted residual

The spectral measure `varsigma_(R,z)` belongs to the constant vector of the full twisted unitary. Raw inversion after finite-count edge extraction involves an exact signed residual and local extracted-edge corrections. Those objects are not automatically matrix coefficients of the same constant-vector cyclic measure with uniformly controlled `L^2` weights.

Even for weights that can be represented as `L^2` vectors, the result remains averaged in the return count.

### 14.5 No uncompressed operator-power estimate is proved

The full twisted Koopman operator is unitary, so its operator norm never decays. A useful fixed-time theorem must exploit a regularity class, a spectral density statement for the relevant vectors, an anisotropic/regularized operator, or a direct probabilistic mechanism. Revision 20 proves none of these at the strength needed for every prescribed return count.

### 14.6 Other frequency regimes remain

The new direct theorem concerns the small physical annulus. The fixed-count raw complement still requires uniform estimates for:

- compact nonzero lattice frequencies with the actual growing vector classes;
- the full peripheral return phase at fixed count;
- growing roof frequencies;
- the far roof-frequency tail;
- a strict quantitative splice among all regions.

## 15. Remaining raw-density estimates

Revision 18 and the v20 convergence clarification give a complete finite packet at each fixed `(n,L,R,w)`. For the linearly growing cutoff used in the raw theorem, the following estimates remain unproved.

### 15.1 Uniform second-derivative growth

One needs a radius-uniform bound on

\[
 A_2(n,L_n,R,w)
 =\sum_\ell
 \|\partial_t^2r_{n,R}^{w,L_n}(\ell,\cdot)\|_1,
 \qquad L_n\asymp n,
\]

strong enough to select the far-roof cutoff while making the normalized error vanish.

The fixed-packet theorem supplies finiteness, not the required growth rate. Prepared exponents may approach the threshold, germ neighborhoods may shrink, coefficients may grow, and singular cells may proliferate.

### 15.2 The local extracted-edge correction

The exact term

\[
 e^{L_n}_{n,R}-K_n*E^{L_n}_{n,R}
\]

must be negligible on the actual central windows after multiplication by `n^2`. Complete extraction identifies the term but does not bound it uniformly in the long-time regime.

### 15.3 The finite-band edge-subtracted residual

The exact residual transform must be integrated at the specified count over the complement of the central cutoff up to the chosen roof cutoff. The averaged full-law theorem does not establish this estimate.

All three estimates must be uniform in the disk radius and in every weight class used downstream.

## 16. Weighted exact conditioning remains incomplete

The arbitrary-`L^2` weighted average is a strong and clean result. Its exact scope must be retained.

For an unchanged event `A`, the same indicator and exact probability occur at each averaging index. This is not the same as a family of exact physical observation events whose terminal lattice/time condition changes with the return count.

The original physical conditioning application still requires:

- weighted fixed-count complementary-frequency estimates;
- weighted finite-count derivative bounds;
- weighted local-edge correction bounds;
- a raw-scale lower asymptotic for the exact denominator;
- a relative comparison between the completed-return event and the exact physical-time/lattice event.

The terminal-mark corollary does not perform this event replacement. The unfinished-return error cannot be discarded under a single lattice constraint without a relative estimate.

## 17. Top-four significance assessment

The manuscript now contains a broad and technically sophisticated unconditional package for this Lorentz family:

- Gaussian and functional laws for the actual unbounded return record;
- growing central Fourier integrals;
- initial, intermediate, terminal, and logarithmic-window observations;
- unsmoothed moments and actual covariance convergence;
- uniform joint nondegeneracy;
- complete measurable phase arithmetic;
- quantitative collision and return function defects;
- exact peripheral return-phase lifting;
- finite-rank compressed resolvents with an exact residual identity;
- complete structural finite-count raw extraction;
- count-localized inversion identities;
- direct uncompressed moving mean-square cancellation;
- cyclic peripheral arc and Abel estimates;
- a spectral Cauchy scaling law.

Several ideas are individually interesting. In particular, the exact top-localized phase lift, measurable phase rigidity, use of the observed count coordinate in inversion, and the exact-orbit Gram argument deserve attention.

At the requested four-journal benchmark, however, the paper continues to organize itself around a raw mixed-density LLT whose fixed-count complementary transform, uniform long-time raw derivative budget, local-edge correction, and exact conditioning extension are not proved. The new averaged theorem is not a substitute for those mechanisms, and the article correctly says so.

A top-four claim could alternatively be supported by extracting a broad abstract theorem from these methods and proving substantial applications in several distinct hyperbolic systems. The present manuscript remains a long sequence of specialized interfaces for one triangular Lorentz family.

I therefore do not regard revision 20 as meeting the closure and breadth threshold of *Annals*, *Acta*, *Inventiones*, or *JAMS*.

A reorganized specialist paper centered on the completed theorems could be strong after independent expert review. In such a version, the raw LLT should be separated as a future theorem or conditional interface unless the remaining fixed-count estimates are supplied.

## 18. Required work before another top-four review

### A. Prove a fixed-return complementary theorem

The next revision should state and prove an estimate at the specified count, not only after averaging in the count. A successful result must control the physical characteristic function or the exact edge-subtracted residual from the central cutoff through the relevant annular and peripheral regions.

Possible routes include:

- a direct fixed-time probabilistic argument extending the short-lag Gaussian control;
- quantitative regularity of the cyclic spectral measure strong enough to control Fourier coefficients at the growing indices `n|z|^2`;
- an anisotropic or regularized induced operator with proved reconstruction and power bounds;
- a Tauberian theorem whose hypotheses are actually verified for the relevant residual vectors.

The theorem must display one feasible set of constants and cutoff exponents over every required frequency regime.

### B. Quantify the long-time constructible packet

For `L_n` proportional to `n`, prove explicit uniform bounds for:

- the number of singular germs and lattice components;
- germ radii and rational exponent separation;
- jet coefficients and transition cutoffs;
- regular-interval derivative integrals;
- the complete second-derivative sum `A_2`.

Finiteness at each packet and exponential first variation in the initial coordinates do not imply these estimates.

### C. Prove the local extracted-edge estimate

Bound the exact extracted density and its low-frequency convolution on the true central windows, with the full count and radius dependence. The statement must include every regular, critical, singular, grazing, competing-root, and image-boundary contribution already present in the structural extraction.

### D. Complete the weighted raw theory

For the actual conditioning classes, prove weighted versions of the fixed-count complementary integral, derivative budget, local-edge correction, and denominator asymptotic. Keep the distinctions among arbitrary `L^2`, bounded variation, finite-record subanalytic, marked, and logarithmic-window classes explicit.

### E. Prove the physical-event replacement

Give a relative error estimate comparing the completed-return event with the exact physical-time/lattice observation event on the shrinking raw scale. The estimate must be relative to the actual denominator; a pathwise `O(log t)` unfinished-return bound alone is insufficient.

### F. Obtain independent specialist review

At minimum, independent experts should check:

- the inherited collision-space spectral import;
- the measurable product-set and finite-cover arguments;
- the peripheral return-phase lift;
- the fixed-band and near-origin defect estimates;
- the complete finite collision graph and constructible preparation;
- the long-time raw derivative and local-edge estimates when developed;
- any future fixed-time complementary-frequency argument.

## 19. Presentation and technical comments

1. Keep the word **averaged** in every theorem title and synopsis concerning Theorem K.
2. Place the fixed-count raw target immediately after Theorem K, including the `n^2` normalization, so the distinction cannot be missed.
3. Retain the explicit calculation `n^(2/5-2/495)` showing why the normalized annular average does not close raw inversion.
4. State beside the Cauchy theorem that its characteristic convergence is for fixed rescaled spectral test frequency; it gives no uniform control when `t=n|z|^2` grows.
5. Continue to distinguish the spectral Cauchy law from the physical Gaussian law.
6. In weighted statements, say explicitly whether the event is fixed across the averaging window or changes with the return count.
7. Keep the fixed-mark and terminal-mark proofs separate; the former uses a fixed test vector, the latter the inverse unitary.
8. Continue to call the peripheral resolvent an **exterior cyclic-vector Abel estimate**, not a unit-circle operator resolvent.
9. Preserve the exact `43/1400`, `29/693`, `2/99`, and `4/495` exponent calculations.
10. Keep the analytic-unit convergence clarification in the finite-count extraction and cite the exact definitions/theorem used.
11. Do not describe spectral arc mass at one scale as absolute continuity or a density bound.
12. Retain the negative diagnostic forbidding inference of single-time decay from the average.
13. Keep the complete list of unresolved raw terms in the proof ledger and introduction.
14. Record the exact successful workflow run and artifact digest in the dynamic validation evidence, while preserving the distinction between build success and proof certification.
15. Consider separating the completed probabilistic/spectral paper from the still-open raw-density program if the next revision does not close the fixed-count theorem.

## 20. Verification boundary

I reviewed the frozen v20 source, the two new core modules, the exact inherited edits, the response to the revision-19 report, the proof ledger, source manifest, validation record, branch and commit identities, and the actual GitHub Actions results at the reviewed SHA.

I checked the short-lag exponent arithmetic, analytic-radius inequalities, lag-window scale, Gram row-sum argument, block analysis and synthesis bounds, weighted normalization, fixed and terminal mark changes of variables, peripheral Dirichlet-kernel estimate, Abel block estimate, principal-angle rounding, and the sequential argument for uniform bounded-Lipschitz Cauchy convergence.

I also examined the new analytic-unit clarification in the finite-count power--logarithm extraction. I did not independently reconstruct every inherited billiard singularity estimate, formally verify all constructible-preparation hypotheses for every chart, or certify the complete 132-page manuscript proof-by-proof.

Finite diagnostics can test the rational exponents, Gram inequalities, block decompositions, spectral kernels, Abel estimates, conditional normalization, wrapped-Cauchy models, source hashes, and TeX build. They cannot prove the continuum billiard estimates, uniform long-time constructible constants, fixed-count complementary integral, local-edge correction, exact physical-event replacement, or journal acceptance.

This report is therefore a mathematical and editorial referee assessment at the requested standard, not a formal proof certificate.

## 21. Final conclusion

Revision 20 responds honestly and constructively to the preceding report. It proves the compressed-grid scale incompatibility, does not attempt to hide it, and supplies a different theorem on the exact uncompressed orbit. The direct Gram argument, arbitrary-`L^2` weighted extension, cyclic peripheral estimates, and spectral Cauchy law are coherent and mathematically worthwhile. I found no decisive counterexample in the new proof chain.

The revision also has successful exact-SHA qualification on both author branches and an accurate statement of its verification boundary.

Nevertheless, the theorem is averaged in the return count and cyclic in the input vector. The raw mixed-density LLT requires a fixed-count complementary estimate for the edge-subtracted physical law, together with uniform long-time derivative and local-edge bounds. The exact physical conditioning application additionally requires weighted fixed-count estimates and relative event replacement.

Those mechanisms remain unproved. For that reason I recommend rejection at the requested top-four benchmark in the present form, while recognizing revision 20 as a substantial mathematical advance and a potentially strong specialist contribution.