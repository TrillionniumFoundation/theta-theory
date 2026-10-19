# External top-four referee report on A2-DYN revision 22

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v22-referee-response-2026-10-06`, `revision/a2-dyn-v22-referee-copy-2026-10-06`  
**Reviewed commit:** `a656998fee8176316850ef87ac447970d712aae2`  
**Reviewed repository tree:** `57696f5c75aadb0a4461711179c0142e3ff8331a`  
**Frozen ordinary paper tree:** `48ee252fdffc68d779069ce7a6c43ac564f8217f`  
**Active manuscript directory:** `papers/A2-DYN-v22-referee-response`  
**Immediate author baseline:** revision 20 at `b5b209000bbef852076f413ef4f718137aeb4dd3`  
**Controlling report:** `reviews/a2-dyn-v20-external-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `a77d1b0af695877bcd43ddb494c637d8353d9b10` / `43f1370dec04d18fcbdebb91b0ddb3b95bb74359`  
**Date:** 6 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards-specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 22 is a genuine and important mathematical advance. It responds directly to the principal objection in the revision-20 report: the preceding direct-orbit theorem controlled an average over return counts, whereas raw local inversion requires an estimate at the prescribed return count. The new revision proves a fixed-count, raw-normalized estimate on a proper inner annulus,

\[
 2n^{-99/200}\le |z|\le 2n^{-12/25},
\]

uniformly in the physical radius and with a bounded-variation insertion at any actual return. In particular, it proves

\[
 n^2\int_{2n^{-99/200}\le |z|\le2n^{-12/25}}
       |\Phi^{[k],a}_{n,R}(z)|\,dz
 \le C\left(
 M_a n^{-1/200}\sqrt{\log(2+n)}
 +V_a n^{-13/100}
 \right)
\]

at every sufficiently large specified `n`, without averaging over the return count and without dividing by the annular volume.

The proof is not a disguised extraction from the averaged theorem. It develops fixed-order collision decoupling, connected-correlation summability, smoothing-independent finite spectral jets, and a degree-19 real-frequency damping argument for the smoothed collision operator. It then removes smoothing, performs the genuine two-sided marked stopping, and inserts the resulting band into an exact enlarged-cutoff raw inversion identity.

I found no decisive counterexample in the two new mathematical modules:

- `core/46_finite_order_damping.tex`;
- `core/47_fixed_return_annulus.tex`.

The finite-order cumulant argument keeps the order fixed; the spectral derivative identification is performed at fixed smoothing scale before uniform cumulant bounds are invoked; the analytic Taylor remainder retains its true smoothing dependence; the marked chronological product has exactly one smoothed multiplier between two collision powers; and the four-dimensional raw Jacobian and all displayed exponent margins are correctly tracked.

This closes a real part of the fixed-count complementary-frequency problem. The proved central support now extends from physical radius `2 n^(-99/200)` to `2 n^(-12/25)`, or from rescaled radius `2 n^(1/200)` to `2 n^(1/50)`.

The negative recommendation nevertheless remains necessary at the requested benchmark. The article continues to be organized around a parameter-uniform raw mixed-density local limit theorem that is not yet proved. Revision 22 controls only an inner part of the fixed-count complement. It does not control:

1. the farther small-frequency annulus from the new boundary toward the previously targeted `n^(-2/5)` regime;
2. compact nonzero lattice frequencies and the relevant full peripheral return phases at the fixed count;
3. growing roof frequencies and the remaining far-roof splice;
4. the uniform long-time second-derivative budget of the finite-count residual when the collision cutoff is proportional to `n`;
5. the recomputed local extracted-edge correction for the enlarged kernel;
6. weighted versions of those raw estimates for the downstream conditioning classes;
7. the relative replacement of completed-return events by the exact physical-time/lattice observation events.

These are central mechanisms of the advertised raw theorem. They are not presentation issues or routine consequences of the new inner-annulus result.

The unconditional package is now unusually substantial for a single Lorentz family. A reorganized paper centered on the completed Gaussian, marked, moment, phase, finite-extraction, logarithmic-window, direct-orbit, and fixed-count inner-annulus theorems could be a strong specialist contribution after independent expert review. That assessment is distinct from acceptance at the four-journal benchmark for the raw LLT claim currently organizing the article.

## 2. Frozen source, chronology, and qualification

The two named revision-22 author branches resolve to the same commit:

`a656998fee8176316850ef87ac447970d712aae2`.

The repository tree at that commit is

`57696f5c75aadb0a4461711179c0142e3ff8331a`.

The ordinary paper tree is

`48ee252fdffc68d779069ce7a6c43ac564f8217f`.

The branch named `revision/a2-dyn-v21-referee-response-2026-10-06` is not a distinct intervening article. It points to the revision-20 review commit `a77d1b0af695877bcd43ddb494c637d8353d9b10`. Revision 22 is therefore the first distinct author manuscript after the substantive revision-20 report, and it is the correct object for the present review.

Revision 22 preserves all forty-five inherited core modules and adds:

- `core/46_finite_order_damping.tex`;
- `core/47_fixed_return_annulus.tex`.

Every inherited core module and every inherited Python script is recorded as byte-identical. Eight exact inherited edits occur only in `main.tex` and `references.tex`: revision identity, the abstract and proof-route synopsis, the prescribed-count warning after Theorem K, the fixed-test-frequency qualification for the spectral Cauchy law, the statement and inclusion of Theorem L, and one background cumulant reference. All inherited mathematical labels are retained.

The source manifest correctly records:

- `finite_order_spectral_jet_proved: true`;
- `fixed_count_inner_annulus_proved: true`;
- `expanded_marked_central_band_proved: true`;
- `full_fixed_return_complementary_integral_proved: false`;
- `exact_physical_event_replacement_proved: false`;
- `full_raw_LLT_proved: false`.

The exact-source qualification completed successfully on both reviewed author branches:

- response branch run `37481620777`;
- referee-copy branch run `37481675355`.

For the response branch, exact checkout, source and controlling-report archiving, native TeX and finite-check installation, verification/build, and artifact upload all completed successfully. The response artifact is

`11421367256`,

named

`a2-dyn-v22-a656998fee8176316850ef87ac447970d712aae2`,

with digest

`sha256:2028543de2b832847fd310eda5615610be1513a9fe308219f75d10b1d5539bec`.

These facts establish exact source identity and successful execution of the declared diagnostics and native build. They do not certify the continuum billiard inputs, the new cumulant proof, the missing outer-frequency estimates, or the full raw theorem.

The present review branch starts directly from the reviewed author commit and adds only this report under

`reviews/a2-dyn-v22-external-top4-review-2026-10-06/`.

No manuscript source, author branch, workflow, earlier report, or unrelated repository path is modified.

## 3. What revision 22 actually proves

Let

\[
 h_R=f_R-\bar G_R\mathbf 1_{Y_R^*}
\]

be the bounded centered collision compensation. Let

\[
 C^{[k],a}_{n,R}(v)
 =\int_{Y_R^*}a((F_R^*)^kx)
 e^{iv\cdot(J_{n,R}(x)-n\bar G_R)/\sqrt n}\,d\nu(x)
\]

be the marked centered transform, and let

\[
 \Phi^{[k],a}_{n,R}(z)
 =\int_{Y_R^*}a((F_R^*)^kx)e^{iz\cdot J_{n,R}(x)}\,d\nu(x).
\]

Their absolute values agree under `v=sqrt(n) z`.

Revision 22 establishes the following new conclusions.

### 3.1 Arbitrary fixed-order collision decoupling

For every fixed integer `q>=2`, bounded-variation collision observables at ordered times factor exponentially across any selected gap:

\[
 \left|
 \mathbb E\prod_{j=1}^q u_j\circ T_R^{t_j}
 -\mathbb E\prod_{j\le p}u_j\circ T_R^{t_j}
  \mathbb E\prod_{j>p}u_j\circ T_R^{t_j}
 \right|
 \le C_qe^{-\gamma_q(t_{p+1}-t_p)}
       \prod_j\|u_j\|_{\mathcal V}.
\]

The proof smooths all `q` factors at scale `epsilon`. The total replacement error is `O_q(epsilon)`, while the chronological collision-space word across the chosen gap costs

\[
 O_q(\epsilon^{-2q}\vartheta^{\text{gap}}).
\]

Balancing at

\[
 \epsilon=\tfrac14\vartheta^{\text{gap}/(2q+1)}
\]

gives the claimed exponential rate. Negative and repeated times are included, and a zero gap uses the bounded operator `I-Pi_R`.

The constants may deteriorate with `q`. The manuscript uses only a fixed maximum order, eventually `Q=19`; it does not claim an all-orders factorial estimate or analyticity of the unsmoothed twist.

### 3.2 Absolute summability of fixed-order connected correlations

Using the finite partition polynomial for joint cumulants, the paper compares an ordered tuple with a law in which the two blocks separated by a largest gap are independent while each block marginal is unchanged. Every mixed subset moment changes exponentially in that gap, whereas the cumulant of the independent two-block law vanishes.

For anchored times this gives

\[
 \sum_{\mathbf k\in\mathbb Z^{q-1}}
 (1+\operatorname{diam}\{0,k_2,\ldots,k_q\})
 \left|\operatorname{cum}
 (u,u\circ T_R^{k_2},\ldots,u\circ T_R^{k_q})
 \right|<\infty
\]

uniformly in the radius and in bounded `BV` classes.

The exact number of translates of an anchored tuple that fit inside a collision interval of length `m` is

\[
 (m-\operatorname{diam})_+.
\]

Consequently,

\[
 \operatorname{cum}_q(S_m u)
 =m\mathfrak c_q(R,u)+O_q(1)
\]

with a radius-uniform error for each fixed order.

### 3.3 A smoothing-independent finite spectral jet

For a real unit direction `xi`, the smoothed collision eigenvalue is written

\[
 \psi_{R,\delta,\xi}(t)
 =\log\lambda_{R,\delta}(t\xi).
\]

At fixed smoothing scale, the stationary pairing has the form

\[
 F_m(t)
 =e^{m\psi(t)}A(t)+E_m(t).
\]

On a smaller `delta`-dependent complex neighborhood, the relative complementary term is exponentially small in `m`. Taking an analytic logarithm there, dividing derivatives by `m`, and sending `m` to infinity identifies

\[
 \psi^{(q)}(0)
 =i^q\mathfrak c_q(R,u_{R,\delta,\xi}),
 \qquad 2\le q\le Q.
\]

The connected-correlation theorem makes these finitely many coefficients uniformly bounded independently of `delta`, `R`, and `xi`.

The proof does not exchange the limits `m->infinity` and `delta->0`. The derivative identification is first made at fixed `delta`; only afterward is the uniform cumulant bound used.

The analytic disk still has radius proportional to `delta^2`. Thus the degree-`Q` expansion retains the genuine remainder

\[
 O_Q\bigl(\delta^{-2(Q+1)}|t|^{Q+1}\bigr).
\]

This is a finite jet, not a scale-free analytic expansion or an infinite cumulant series.

### 3.4 Real-frequency damping of the smoothed collision operator

Uniform positivity of the smoothed covariance supplies a negative real quadratic term. If

\[
 |z|\le a\delta^2,
 \qquad
 \delta^{-2(Q+1)}|z|^{Q-1}\le a,
\]

then the finite higher-order polynomial and the analytic remainder are dominated by the quadratic term. The manuscript obtains

\[
 |\lambda_{R,\delta}(z)|\le e^{-c|z|^2}
\]

and

\[
 \|\mathcal L_{R,\delta,z}^m\|
 \le Ce^{-cm|z|^2}
\]

for real frequencies on every local collision space.

The complementary spectral term is absorbed by decreasing the exponential constant on the stated small-frequency domain. The result is a norm bound for the smoothed collision transfer operator, not for the unitary actual-return Koopman operator.

### 3.5 A marked deterministic comparison at the prescribed count

After recentering the physical orbit at an arbitrary actual return and applying the genuine two-sided stopping comparison, the random record is replaced by a deterministic two-sided collision interval of total length

\[
 m_k+m_{n-k}=n/c_*+O(1).
\]

Smoothing the insertion costs `C delta V_a`. Removing observable smoothing costs

\[
 CM_a|v|\sqrt{\delta(1+|\log\delta|)}.
\]

The actual stopping costs

\[
 CM_a(1+|v|)n^{-2/9}.
\]

The remaining exact chronological pairing is

\[
 \ell\!\left(
 \mathcal L_{R,\delta,z}^{m_{n-k}}
 M_{a_\delta}
 \mathcal L_{R,\delta,z}^{m_k}\nu
 \right),
 \qquad z=v/\sqrt n.
\]

The multiplier has norm `O(M_a delta^(-2))`, and the product of the two collision powers yields damping in their total length. This gives

\[
 |C^{[k],a}_{n,R}(v)|
 \le CM_a\delta^{-2}e^{-c|v|^2}
 +C\delta V_a
 +CM_a\left\{
 |v|\sqrt{\delta(1+|\log\delta|)}
 +(1+|v|)n^{-2/9}
 \right\}.
\]

Length-zero blocks are covered by the same power bound, so the initial and terminal marks require no separate limiting argument.

### 3.6 The fixed-return raw-scale inner annulus

The concrete choice is

\[
 Q=19,
 \qquad
 \delta=\tfrac14n^{-21/100},
 \qquad
 |v|\le2n^{1/50},
 \qquad
 z=v/\sqrt n.
\]

The two damping-domain quantities are

\[
 |z|\delta^{-2}=O(n^{-3/50}),
\]

and

\[
 |z|^{18}\delta^{-40}=O(n^{-6/25}).
\]

Both have strict positive margins.

The lower rescaled radius is `2 n^(1/200)`, so the Gaussian damping term is exponentially small like a fixed polynomial times

\[
 e^{-c n^{1/100}}.
\]

The change of variables `v=sqrt(n)z` in four dimensions has Jacobian `n^(-2)`, exactly cancelling the raw factor `n^2`.

After integration, the three nondamping losses are

\[
 V_a n^{-21/100+4/50}=V_a n^{-13/100},
\]

\[
 M_a n^{-21/200+5/50}\sqrt{\log n}
 =M_a n^{-1/200}\sqrt{\log n},
\]

and

\[
 M_a n^{-2/9+5/50}=M_a n^{-11/90}.
\]

The slow term is the observable-unsmoothing contribution `n^(-1/200) sqrt(log n)`. The volume factors are included in these powers.

### 3.7 A wider marked central band

Combining the inherited sharper marked central theorem on

\[
 |v|\le2n^{1/200}
\]

with the new fixed-count annulus and the uniformly elliptic Gaussian tail gives

\[
 \int_{|v|\le2n^{1/50}}
 \left|
 C^{[k],a}_{n,R}(v)
 -\alpha_a e^{-v^{\mathsf T}D_Rv/2}
 \right|\,dv
 \le C\left(
 M_a n^{-1/200}\sqrt{\log(2+n)}
 +V_a n^{-9/175}
 \right).
\]

The older central theorem remains stronger on its smaller band.

### 3.8 Same-event conditioning on the wider band

For an event measured at one actual return, with probability `p_n` and zero-extension variation `V_n`, division by the unchanged exact probability gives

\[
 \int_{|v|\le2n^{1/50}}
 \left|
 \mathbb E[e^{iv\cdot U_{n,R}/\sqrt n}\mid A_{n,k,R}]
 -e^{-v^{\mathsf T}D_Rv/2}
 \right|\,dv
 \le \frac{C}{p_n}
 \left(
 n^{-1/200}\sqrt{\log(2+n)}
 +V_n n^{-9/175}
 \right).
\]

A sufficient polynomial regime is

\[
 p_n\ge cn^{-\beta},
 \qquad
 V_n\le Cn^\kappa,
 \qquad
 \beta<1/200,
 \qquad
 \beta+\kappa<9/175.
\]

No event is replaced, and the statement remains a central-band conditional theorem rather than a conditional raw LLT.

### 3.9 Exact raw inversion with the enlarged cutoff

The new physical cutoff is

\[
 \widetilde B_n=n^{-12/25}.
\]

Its smooth Fourier support has radius `2 n^(-12/25)`, precisely the region covered by the expanded fixed-count theorem. Repeating the exact count-localized decomposition gives

\[
 p_{n,R}
 =\widetilde K_n*\mu_{n,R}
 +(e^{L_n}_{n,R}-\widetilde K_n*E^{L_n}_{n,R})
 +\mathcal F^{-1}[(1-\widetilde\chi_n)\widehat Q^{L_n}_{n,R}]
 -\widetilde K_n*\mathsf T^{L_n}_{n,R}.
\]

The high-count support is separated from the central count labels by order `n`. The enlarged kernel gives, after raw normalization,

\[
 n^2\sup|\widetilde K_n*\mathsf T^{L_n}|
 \le C_M n^{2/25-13M/25},
\]

which is smaller than every prescribed inverse power after choosing `M`.

The Gaussian tail beyond the enlarged central rescaled cutoff is

\[
 O(e^{-c n^{1/25}}).
\]

The exact raw error budget therefore exposes only the same three unresolved finite-count terms, recomputed for the enlarged cutoff:

- the local extracted-edge correction;
- the finite-band complementary residual integral;
- the far-roof term involving the actual second-derivative budget `A_2(n,L_n,R,1)`.

The theorem explicitly remains an extended-real inequality until the local-edge term is bounded.

## 4. Audit of the arbitrary fixed-order decoupling

The extension of the earlier two-to-four factor argument to each fixed order is mathematically natural and, in the form stated, coherent.

Smoothing all factors costs only the sum of their individual `L^1` errors because the remaining factors are uniformly bounded. No variation norm of a composed long iterate is used. After translating the first time to zero, the chronological transfer word contains the selected gap as one collision power. Replacing that power by the rank-one projector produces exactly the product of the two whole-block expectations. Every other collision power remains uniformly bounded.

The cost `epsilon^(-2q)` is deliberately crude but adequate for fixed `q`. A zero selected gap is handled by `I-Pi`, giving a bounded error consistent with the right side at gap zero.

The theorem correctly states simultaneous constants only for orders up to a specified finite `Q`. Nothing in the proof gives a useful all-order growth bound, and the article does not use it as one.

A specialist should nevertheless verify the local-space bookkeeping for arbitrary numbers of smooth multipliers, especially the passage among the finite family of collision spaces and the repeated-time convention. I found no contradiction in the printed argument.

## 5. Audit of the connected-correlation summation

The independent-block comparison is appropriate for cumulants.

Choose a largest consecutive gap after ordering the times. Introduce independent copies of the two entire blocks, preserving all within-block joint moments. For every subset meeting both blocks, the actual subset moment differs from the product of its two block moments by the fixed-order decoupling estimate. Subsets contained in one block are unchanged. The finite partition polynomial is Lipschitz on a bounded set of moments, with a constant depending only on the fixed order. The independent-block cumulant is zero.

The resulting exponential bound in the largest gap is enough for absolute summability. If the anchored diameter is `D`, some consecutive gap is at least `D/(q-1)`. Polynomially many anchored integer tuples have diameter at most `D`, so the exponential estimate sums even with the extra diameter factor.

The exact coefficient `(m-D)_+` in the finite collision interval follows from translating the anchored tuple until its minimum and maximum both lie in the interval. This coefficient treats negative offsets and repeated indices correctly.

The argument proves bounded boundary corrections to linear cumulant growth. It does not prove uniform control as the cumulant order tends to infinity. The distinction is correctly maintained.

## 6. Audit of the finite spectral jet

The order of limits is the main delicate point, and the manuscript handles it in the right direction.

At a fixed smoothing scale, the smoothed collision operator is analytic on a nonzero, though shrinking, complex neighborhood. On a smaller neighborhood, the leading eigenvalue stays uniformly separated from zero and from the complementary spectral radius. The principal amplitude is nonzero. Hence the scalar characteristic pairing has an analytic logarithm for sufficiently large collision length, and the relative complementary error tends to zero exponentially.

Dividing the `q`th derivative of this logarithm by the collision length identifies the derivative of the eigenvalue logarithm. The finite-sum logarithmic derivatives at zero are exactly cumulants. Only after this fixed-scale identification does the proof use the smoothing-independent connected-correlation bound.

This avoids an unjustified interchange of the smoothing and long-time limits.

The remainder estimate remains tied to the analytic disk of radius `O(delta^2)`. Cauchy's estimate gives the factor `delta^(-2(Q+1))`. The paper does not erase that dependence after proving uniformity of the first `Q` coefficients.

I found no decisive flaw in this step. An independent operator specialist should check the common local neighborhood on which the scalar relative error admits the chosen analytic logarithm and the precise uniform bound on the eigenvalue logarithm used in the Cauchy remainder. These are inherited perturbative ingredients, but they are load-bearing at order nineteen.

## 7. Audit of the real-frequency damping

For real frequencies, odd cumulant coefficients contribute imaginary terms, while the proof in any event bounds the complete degree-at-least-three polynomial by `C_Q|t|^3`. Uniform positivity of the smoothed covariance gives a negative real quadratic term.

The two domain inequalities have distinct roles:

1. `|z|<=a delta^2` keeps the frequency inside the analytic perturbation disk;
2. `delta^(-2(Q+1))|z|^(Q-1)<=a` makes the analytic remainder small relative to `|z|^2`.

After decreasing fixed constants, the real part of the eigenvalue logarithm is at most `-c|z|^2`. The complementary spectral power is dominated by the same exponential because the real-frequency region is uniformly small.

This yields a genuine power estimate for the smoothed collision operator. It does not say that the actual return Koopman operator has decaying norm; the latter remains unitary. The manuscript states this distinction correctly.

The degree `Q=19` is not cosmetic. With the selected smoothing and frequency exponents, the degree-19 remainder has margin `6/25`, while the inherited cubic bound would grow rather than decay. The finite diagnostic that rejects degree fifteen is consistent with the strict-domain calculation.

## 8. Audit of the marked chronological product and stopping

The exact two-sided compensation about a marked return was established in the inherited paper. Revision 22 uses it without changing the event or record.

The deterministic comparison interval has one backward and one forward collision block. The total length is `n/c_*+O(1)` uniformly in the mark. The smoothed insertion lies exactly between the two collision powers. Thus the product of the two damping factors depends on the total deterministic length even when one block has length zero.

The insertion smoothing error depends on `V_a`, whereas the multiplier norm and observable-unsmoothing error depend on `M_a`. This separation is important and is preserved.

For the residual observable, stationarity of the whole deterministic interval and the inherited small-`BV` variance estimate give the stated `sqrt(delta log(1/delta))` loss after normalization by `sqrt(n)`. No independence of the backward and forward pieces is used.

The stopping error is the inherited actual two-sided theorem, not a new deterministic-clock substitution. It applies uniformly in the mark and at all real frequencies with the displayed linear `|v|` loss.

I found the chronological order, normalization, and endpoint cases coherent.

## 9. Audit of the exponent bookkeeping and raw normalization

The concrete parameters are internally consistent.

With

\[
 \delta=n^{-21/100}/4,
 \qquad
 |z|\le2n^{-12/25},
\]

the analytic-disk quantity is

\[
 |z|\delta^{-2}=O(n^{-12/25+42/100})
 =O(n^{-3/50}).
\]

For `Q=19`, the remainder quantity is

\[
 |z|^{18}\delta^{-40}
 =O(n^{-216/25+840/100})
 =O(n^{-6/25}).
\]

The rescaled inner boundary is `2n^(1/200)`, so collision damping contributes an exponentially small term.

The four-dimensional Jacobian under `v=sqrt(n)z` is `n^(-2)`. This exactly cancels the raw factor `n^2`; no volume factor is hidden.

The integrated exponents are:

- insertion smoothing: `21/100-4/50=13/100`;
- observable unsmoothing: `21/200-5/50=1/200`;
- stopping: `2/9-5/50=11/90`.

All are strictly positive. The slow observable-unsmoothing rate explains the final `n^(-1/200) sqrt(log n)` bound.

The general parameter range is also correct. For outer rescaled exponent `epsilon`, smoothing exponent `theta`, and fixed Taylor degree `Q`, the conditions

\[
 10\epsilon<\theta<\frac14-\frac\epsilon2
\]

and

\[
 (Q-1)(1/2-\epsilon)>2(Q+1)\theta
\]

make the displayed losses and analytic remainder decay. The interval for `theta` is nonempty when `epsilon<1/42`.

This is a sufficient range for the current method. It is far smaller than the rescaled exponent `1/10` associated with the previously targeted physical radius `n^(-2/5)`. Thus the printed finite-order argument, without further improvement, does not close the remaining farther annulus. The manuscript appropriately does not call `1/42` an impossibility barrier.

## 10. Audit of the enlarged central band and conditional corollary

On the original central ball, the inherited marked theorem supplies the sharper rate. On the new annular portion, the physical transform is bounded absolutely and the Gaussian is exponentially small by uniform ellipticity. Adding the two pieces gives the wider comparison.

The variation loss in the combined theorem is the worse inherited central loss `n^(-9/175)`, not the faster new annular loss `n^(-13/100)`. The supremum loss is the slower new `n^(-1/200) sqrt(log n)` rate. This bookkeeping is correct.

For an unchanged marked event, the insertion mass is precisely its invariant probability. Dividing the complex numerator by that exact probability gives the conditional characteristic function. The factor is `p^{-1}`, appropriate to a fixed-count absolute-error estimate.

This corollary does not compare two events and does not prove a conditional raw local limit theorem. Its scope is correctly stated.

## 11. Audit of the enlarged-cutoff raw identity

The observed collision-count coordinate makes the finite-count support identity exact on central labels. Changing the smooth Fourier cutoff does not alter that support argument or the absolute residual inversion.

The full-law central term is now controlled to the enlarged radius. The Gaussian tail outside the radius `n^(1/50)` is exponentially small, with exponent `n^(1/25)`.

The high-count measure is not discarded. It is convolved with the enlarged kernel. The count-coordinate separation is of order `n`, and the kernel scale satisfies `B_n n=n^(13/25)`. After multiplying by `n^2`, the stated bound

\[
 n^{2/25-13M/25}
\]

is consistent with four-dimensional kernel scaling and rapid Schwartz decay.

Most importantly, the local edge correction is recomputed as

\[
 e^{L_n}_{n,R}-\widetilde K_n*E^{L_n}_{n,R}.
\]

The manuscript does not transfer an estimate for the old kernel to the new one.

The exact error budget still contains:

\[
 n^2\widetilde{\mathcal E}_{n,R,A}^{L_n},
\]

\[
 n^2\widetilde{\mathcal C}_{n,R}^{L_n}(B),
\]

and

\[
 \frac{n^2}{\pi B}A_2(n,L_n,R,1).
\]

No one of these is shown to vanish uniformly. Thus the enlarged identity is a sharpened reduction, not the raw LLT itself.

## 12. What revision 22 closes

Relative to the revision-20 report, the new manuscript closes the following point:

- it supplies a prescribed-count, unnormalized, raw-`n^2` estimate on a nontrivial inner annulus, rather than another return-count average;
- it carries one actual-return `BV` mark throughout that estimate;
- it extends the integrated marked Gaussian comparison from rescaled radius `n^(1/200)` to `n^(1/50)`;
- it inserts the larger cutoff into the exact raw inversion identity;
- it recomputes, rather than suppresses, the kernel-dependent local edge term.

This is substantial progress. The fixed-count objection in the previous report is no longer valid on the newly proved inner region.

Revision 22 does not close the complete fixed-count complement, the long-time raw preparation constants, or the physical conditioning application.

## 13. Remaining fixed-count complementary-frequency problem

The new physical boundary is

\[
 |z|=2n^{-12/25}=2n^{-0.48}.
\]

The previously contemplated next regime begins around

\[
 |z|=n^{-2/5}=n^{-0.4}.
\]

There remains a genuine farther annulus between these scales. In rescaled variables it runs from approximately `n^(1/50)` to `n^(1/10)`.

Beyond it, the raw theorem still needs fixed-count control of:

- compact nonzero spatial and collision-count torus frequencies;
- the full relevant peripheral return phase;
- growing roof frequencies;
- the far roof-frequency tail;
- a strict splice among all regions with actual constants.

The general finite-order construction reaches only `epsilon<1/42`. Increasing the fixed Taylor degree alone cannot reach rescaled exponent `1/10` while the current smoothing and unsmoothing errors remain unchanged. A sharper unsmoothing estimate, a different collision-space argument, a genuine induced anisotropic construction, or another direct fixed-count method appears necessary.

The direct averaged theorem, cyclic arc bounds, and fixed-test-frequency spectral Cauchy limit remain valuable but cannot fill this fixed-count gap.

## 14. Remaining uniform raw-density estimates

Revision 18 and its retained descendants establish a complete finite-count constructible extraction at every fixed packet. Revision 22 does not add uniform long-time control of the packet.

For

\[
 L_n\asymp n,
\]

the raw theorem still needs a radius-uniform bound on

\[
 A_2(n,L_n,R,w)
 =\sum_\ell
 \|\partial_t^2r^{w,L_n}_{n,R}(\ell,\cdot)\|_1
\]

strong enough to choose the roof cutoff and make the normalized far-tail term vanish.

Fixed-packet finiteness is insufficient. As `n` grows:

- the number of cells and singular germs may grow;
- prepared exponents may approach the derivative threshold;
- germ radii may shrink;
- jet coefficients and logarithmic degrees may grow;
- critical values may coalesce;
- regular-interval derivative integrals may deteriorate.

The finite collision cumulants concern bounded collision observables. They do not control inverse-coarea Jacobians or the second weak derivatives of the raw pushforward density.

The local edge correction must also be estimated uniformly on the true central windows. Exact extraction of every edge does not by itself show that

\[
 e^{L_n}-\widetilde K_n*E^{L_n}
\]

is negligible after raw normalization.

Finally, the edge-subtracted finite-band residual integral outside the enlarged cutoff must be bounded at the prescribed count. These three terms are precisely the unresolved quantities in the new exact error budget.

## 15. Weighted raw theory and exact physical conditioning

The new fixed-count theorem allows one bounded-variation function evaluated at one actual return. The inherited logarithmic-window theorem treats a multiple-return event on a central band under different approximation budgets. The inherited arbitrary-`L^2` theorem is averaged over the return count.

These classes are not interchangeable.

For the downstream exact physical conditioning theorem, the manuscript still needs weighted fixed-count versions of:

- the complete complementary-frequency estimate;
- the long-time second-derivative budget;
- the local extracted-edge correction;
- the raw denominator asymptotic.

It must also prove a relative comparison between the completed-return event and the exact physical-time/lattice observation event. The unfinished-return error cannot be discarded under a rare lattice constraint using only an absolute probability estimate.

The same-event corollary in revision 22 performs no such replacement.

## 16. Top-four significance assessment

The manuscript now contains a broad and technically ambitious unconditional package:

- Gaussian and functional laws for the actual unbounded return record;
- growing and marked central Fourier integrals;
- actual fourth moments and covariance convergence;
- uniform joint covariance nondegeneracy;
- complete measurable phase arithmetic;
- quantitative collision and actual-return function defects;
- exact peripheral phase lifting;
- finite-rank compressed resolvents with an explicit scale limitation;
- complete finite-count structural raw extraction;
- logarithmic return-window conditioning;
- direct uncompressed averaged-orbit estimates;
- cyclic peripheral and spectral Cauchy statements;
- a prescribed-count raw-scale inner-annulus theorem.

Several techniques are notable: bounded collision compensation for an unbounded induced record, measurable phase rigidity via symplectic area and finite covers, exact tower-top localization of return defects, use of the observed count coordinate in raw inversion, and the new finite spectral-jet method.

At the requested benchmark, however, the paper remains organized around a raw mixed-density LLT whose decisive outer-frequency and long-time density estimates are still absent. The newly proved inner annulus is a real theorem, but it is not the announced endpoint.

A top-four case could also be made by extracting a broad general theorem from these methods and proving substantial applications in several distinct hyperbolic systems. The present article remains centered on one carefully engineered triangular Lorentz family and a long sequence of specialized interfaces.

I therefore do not regard revision 22 as meeting the closure and breadth threshold of *Annals*, *Acta*, *Inventiones*, or *JAMS*.

A reorganized specialist paper centered on the completed theorems could be very strong after independent review. In that form, the remaining raw LLT should be presented as a precise future theorem or conditional synthesis unless its remaining estimates are supplied.

## 17. Required work before another top-four review

### A. Close the rest of the fixed-count complement

Prove a prescribed-count integrated estimate from the new boundary through:

- the farther small annulus;
- compact nonzero torus frequencies;
- all necessary peripheral return phases;
- growing roof frequencies;
- the far roof tail.

The estimate must apply to the physical characteristic function or the exact edge-subtracted residual with the raw normalization. It cannot be replaced by a return-count average or a constant-vector spectral statement.

### B. Quantify the long-time finite-count extraction

For the packets with `L_n` proportional to `n`, bound uniformly:

- the number and geometry of singular cells;
- prepared exponents and their separation from the derivative threshold;
- germ radii and coefficients;
- logarithmic degrees;
- regular-interval derivative integrals;
- the complete `A_2` sum.

The resulting bound must be compatible with the roof cutoff used in the full Fourier splice.

### C. Prove the enlarged-kernel local edge estimate

Estimate

\[
 n^2\widetilde{\mathcal E}_{n,R,A}^{L_n}
\]

uniformly on the actual central windows. The estimate must include all extracted regular, singular, grazing, competing-root, and image-boundary jets and their convolution with the enlarged kernel.

### D. Complete the weighted raw theory

For the exact downstream indicator classes, prove weighted versions of:

- the full fixed-count complement;
- the finite-count derivative budget;
- the local edge correction;
- the raw denominator asymptotic.

State precisely which one-mark, multiple-return, `BV`, and finite-record subanalytic classes survive every step.

### E. Prove the exact physical-event replacement

Compare the completed-return conditioning event with the true physical-time/lattice event on the raw local scale. The error must be relative to the same exact denominator and uniform in the radius.

### F. Obtain independent specialist review

At minimum, independent experts should examine:

- arbitrary fixed-order collision-space multiplication and decoupling;
- the independent-block cumulant comparison and anchored summation;
- the fixed-smoothing analytic logarithm and derivative limit;
- the order-19 Taylor remainder and real-frequency operator damping;
- the marked chronological product and two-sided unsmoothing;
- the finite-count constructible preparation and future long-time bounds;
- the complete outer-frequency splice.

## 18. Presentation and technical comments

1. Keep Theorem L explicitly labeled as an inner-annulus theorem. The current wording is accurate.
2. Retain both physical and rescaled radii beside every new inversion statement.
3. Keep the old sharper central rate visible; the larger band has a slower rate for a mathematical reason.
4. State near the finite-order decoupling theorem that `C_q` and `gamma_q` are not controlled uniformly as `q` grows.
5. Preserve the order of limits in the spectral-jet proof: fixed smoothing first, collision length second, uniform coefficient bound last.
6. Do not abbreviate the analytic Taylor remainder to `O(|z|^(Q+1))`; the factor `delta^(-2(Q+1))` is essential.
7. Keep the distinction between real-frequency smoothed collision damping and unitary return-operator behavior.
8. The proof would benefit from one displayed schematic of the chronological word with the mark between the two damped powers.
9. Retain the separate `M_a` and `V_a` losses.
10. Beside the general parameter range, note numerically that `1/42` is much smaller than the exponent `1/10` needed to reach the old annular endpoint in rescaled variables.
11. Continue to distinguish one marked-state event, a logarithmic return-window event, and an exact physical observation event.
12. The enlarged raw identity should continue to call the edge correction kernel-dependent.
13. Do not describe fixed-packet constructible finiteness as a uniform long-time derivative estimate.
14. Keep the exact-source execution record separate from mathematical proof status.
15. The background cumulant reference should remain background; no theorem from it is needed to replace the printed fixed-order proof.

## 19. Verification boundary

I reviewed the frozen revision-22 source, the two new core modules, the response to the controlling report, source manifest, proof ledger, finite-cumulant input map, exact edit ledger, branch and commit identities, and the actual GitHub Actions results at the reviewed SHA.

I checked the fixed-order factorization logic, connected-correlation summation, anchored multiplicity, spectral derivative identification, damping-domain inequalities, degree-19 exponent arithmetic, four-dimensional raw Jacobian, marked unsmoothing losses, enlarged Gaussian tail, high-count Schwartz exponent, and the exact form of the new raw error budget.

I did not independently reconstruct every inherited dispersing-billiard singularity estimate, formally certify the local collision Banach spaces, or prove the future uniform constructible-preparation bounds.

Finite diagnostics can test partition algebra, rational exponents, finite-state spectral identities, and source hashes. They cannot establish the continuum collision-space theorem, the complete raw complementary integral, uniform long-time inverse-coarea derivatives, the local extracted-edge estimate, or the physical-event replacement.

This report is therefore a mathematical and editorial referee assessment at the requested standard, not a formal proof certificate.

## 20. Final conclusion

Revision 22 makes a credible and substantial advance. It replaces the return-count average at the center of revision 20 with a genuine prescribed-count theorem on a nontrivial raw-scale inner annulus. The finite-order cumulant and spectral-jet mechanism is carefully delimited, the order-19 bookkeeping is coherent, and the exact enlarged-cutoff inversion identity preserves every unresolved raw term.

I found no decisive counterexample in the new proof chain.

The exact source is properly qualified and both author branches resolve to the same reviewed SHA.

Nevertheless, the complete fixed-count complement, uniform long-time residual derivative budget, enlarged-kernel local edge correction, weighted raw theory, and exact physical-event replacement remain unproved. Since these are load-bearing components of the article's organizing raw mixed-density local limit theorem, I recommend rejection at the requested top-four benchmark in the present form.

The completed results merit serious consideration as the basis of a strong specialist paper after independent expert verification and appropriate reorganization.