# Response to the referee: A2-DYN revision 33

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Active source:** `papers/A2-DYN-v33-referee-response`  
**Controlling report:** `reviews/a2-dyn-v32-external-top4-review-2026-10-07/REFEREE_REPORT.md`  
**Report commit / blob:** `c41e23ea3494aaa40502aed990c6d46b9bce1153` / `9b25d7264504a0cf214d0e473281010505713310`  
**Qualified author baseline:** `f63fb5101c8bcf6202abf4468d703be6242923a1`  
**Baseline ordinary paper tree:** `d6462c94e0cb7a702bf4e46e60da0440fb94a5ac`  
**Date:** 7 October 2026

We thank the referee for distinguishing the preceding-section record from the original stationary physical observation, and for identifying the difference between an accurate reconstruction and evaluation of its finite Fourier integral. This revision takes up the original physical event directly. It does not transfer an entrance-record event by an unproved microscopic clock comparison.

The new Theorem X keeps singleton spatial displacement and a prescribed integer physical collision count at the deterministic observation time. Exact integration of the true initial flight age gives a uniform distributional second-derivative bound for these time profiles. Their high-time-frequency inverse is consequently controlled pointwise with a polynomial bandwidth, with no discarded-density term. We also evaluate their three-dimensional central Gaussian term, including the two endpoint roof weights and the exact physical covariance normalization. This is a pointwise Gaussian-plus-complement identity for the original physical event, not only an unevaluated positive reconstruction.

The title, triangular Lorentz family, actual return section, original four-coordinate return record and full raw mixed-density target remain unchanged. All 66 inherited core files, all 71 inherited Python files and the bibliography are byte-identical. The original mesoscopic results and the original microscopic return-density requirements are retained. The new physical calculation is an additional route within the same conditioning problem, not a replacement by a specialist-paper topic.

## 1. The original stationary event, without discarding cell corrections

In current-collision coordinates the actual stationary probability is

`dP_R(x,a) = dnu(x) da / mean(tau_R)`, with `0 <= a < tau_R(x)`.

This is the probability already derived in `lem:stationary-length-bias`, not an unbiased section probability or a substituted entrance law. For a fixed convex polygonal fundamental cell, a straight flight visits only a uniformly finite set of cell labels. Its intersection with each translated cell is an age interval. The fixed cell convention is used at both observation times.

For `C_R(t)=m`, put `y=T_R^m x` and `v=t+a-S_m tau_R(x)`. The exact displacement is

`K_m^c(x) + d_R(y,v) - d_R(x,a)`.

Both bounded within-flight corrections remain inside every singleton indicator and every Fourier amplitude. They are not negligible at this resolution. Lemma `lem:finite-flight-cell-partition` proves the finite interval partition directly from convexity, the fixed cell geometry and uniform finite horizon. It uses no derivative or regularity of a crossing time.

For intervals `I,J`, the age integral is the exact overlap

`H_{I,J}(s) = integral 1_I(a) 1_J(s+a) da = 1_{-I} * 1_J(s)`.

Theorem `thm:stationary-overlap-regularity` expresses the original probability `P_R(W_R(t)=k,C_R(t)=m)` as the positive average of these overlaps shifted by the true collision sum. The count `m` is prescribed; it is neither an averaged count nor the return count `n`.

## 2. Pointwise time regularity and a polynomial far-frequency band

Every interval indicator has an endpoint derivative measure of variation at most two. Therefore the second derivative of one overlap has variation at most four. Summing over cell pairs counts a fixed number of pairs per source point, not the number of long collision words. This proves

`sum_k ||D_t^2 p_{m,R}(k,.)||_TV <= 4 J_*^2 / min_R mean(tau_R)`

uniformly in `m,R`. The derivative is a measure; the theorem does not claim that it has an `L1` density. The probability profiles are also globally Lipschitz in observation time with an all-label bound.

The first and last flight amplitudes are

`A_R^-(x;u,b) = integral_0^tau(x) exp(-i[u.d_R(x,a)+ba]) da`,

`A_R^+(y;u,b) = integral_0^tau(y) exp( i[u.d_R(y,v)+bv]) dv`.

Each is bounded by `min(tau_+,2 J_*/|b|)`. Their product therefore decays as `|b|^(-2)` independently of the intervening collision count. The full time-frequency integral for the original singleton event is absolutely convergent. Its sharp truncation satisfies the genuinely pointwise estimate

`sum_k ||p_{m,R}(k,.) - p^sharp_{m,R,B}(k,.)||_infinity <= A_2/(pi B)`.

With `B_m=m^(P+3/2)` the error is `O(m^(-P))` after multiplication by the physical local scale `m^(3/2)`. There is no super-exponential band and no small-mass discarded density in this physical formula.

This closes the far-frequency and discarded-density difficulties for this direct stationary endpoint representation. It does not assert the same bound for the different four-coordinate return density. Theorem W's reconstruction may still require `B_n=exp(O(n log n))`; that fact is repeated beside the main results.

## 3. An evaluated Gaussian central term, not a trace of the old estimate

The collision vector is

`f_R^c=(kappa_1,kappa_2,tau_R-mean(tau_R))=P_R h_R`.

Its covariance `Sigma_R=P_R Gamma_R P_R^T` is uniformly positive definite by the retained joint covariance theorem. The new central proof is written for a three-dimensional integral from the outset. It does not restrict an `L1(R4)` error to a three-dimensional frequency subspace.

The exact single-flight amplitudes differ from `tau_R` by `O(|(u,b)|)` near zero, including the cell corrections. A two-endpoint collision pairing with weights `tau_R(x)` and `tau_R(T_R^m x)` is then estimated by the inherited smooth collision splitting. The initial vector, terminal functional and projector difference are all paid: the amplitude error is `O(delta^(-6)|v|/sqrt(m))`, not the smaller one-endpoint bound.

At `delta=m^(-1/14)/4` and rescaled radius `2 m^(1/200)`, the five polynomial error exponents are

`79/1400, 11/700, 13/280, 9/175, 29/700`.

Both analytic smallness inequalities have strict positive margins. Thus the integrated central error is `O(m^(-11/700) sqrt(log(2+m)))`. Removing the bounded within-flight amplitudes from the central pairing costs only `O(m^(-12/25))` on that normalized scale. The central main term is

`mean(tau_R) g_{Sigma_R}(k/sqrt(m),(t-m mean(tau_R))/sqrt(m))`.

The factor is derived from the two roof means divided by the stationary suspension mean. The physical covariance identity is

`V_R = mean(tau_R)^(-1) D_R^clk Sigma_R (D_R^clk)^T`,

with `D_R^clk=diag(1,1,-1/mean(tau_R))`. In particular `det(V_R)=det(Sigma_R)/mean(tau_R)^5`. This gives the standard physical central density `g_{V_R}(xi)` at scale `t^(-3/2)`, without an omitted lattice covolume in lattice coordinates.

## 4. What remains of the finite complement and the local correction

Theorem `thm:physical-singleton-reduction` gives the explicit pointwise identity

`t^(3/2) p_{m,R}(k,t) = g_{V_R}(xi) + t^(3/2) M_{m,R,B_m}(k,t) + O(t^(-11/700) sqrt(log(2+t)) + t^(-P))`

uniformly on compact central sets, where `M` is exactly the signed inverse over `u in T^2`, `|b|<=B_m` and outside the physical ball `2 m^(-99/200)`. The corresponding rescaled radius is `2 m^(1/200)`.

For the original stationary physical singleton, this leaves one specified finite signed middle integral. The formula has no discarded-density error, no preceding-section event error and no unbounded count truncation. A Gaussian denominator asymptotic on that class is equivalent to vanishing of this normalized signed middle term. Separate absolute estimates are sufficient but not required; cancellation in the complete integral is permitted.

We have not proved that vanishing. The new result evaluates the central contribution and controls the complete far tail; it does not claim an estimate for every intermediate spatial/time frequency. The pointwise common correction of the original return-density theorem also remains, because it is an estimate for a different law. Neither absence of exact phases nor positivity is promoted to the missing dynamical estimate.

## 5. Arbitrary selectors for the actual physical event

Time-smoothing the indicator of the same original event gives a positive likelihood between zero and one. Before averaging over initial states, the interval partition proves

`sum_k E|1_{A_{m,k}(t)}-1_{A_{m,k}(s)}| <= L_0 |t-s|`.

Averaging against the existing positive kernel gives source total-variation error `L_0 kappa_1/B`, uniformly in the spatial event, physical time, radius and prescribed collision count. This is a pointwise-in-observation-time bound on the original source, not a global time-averaged statement.

Any bounded measurable trajectory selector can multiply this estimate by contraction. Its exact finite Fourier expression retains the selector in the initial flight-age amplitude; no derivative of the selector is used. The selector is held fixed while transforming the observation-time variable. Unlike the unweighted product, its initial amplitude is not claimed to decay as `1/|b|` for arbitrary selectors.

The posterior bounds explicitly divide by the actual selected denominator or an evaluated finite-band lower-bound test. A positive unselected Gaussian denominator, if obtained by controlling the middle term, does not supply a selected denominator for every path selector. The weighted dynamical evaluation remains distinct from source-TV reconstruction.

## 6. Response to the six required changes and seven presentation comments

`REFEREE_STATUS.md` preserves the complete obligation table and distinguishes the original return law, the original physical endpoint, and weighted conditioning. The same distinction appears in the final table of the new proof section.

For requests 1--4, the new direct physical formula evaluates the Gaussian central term, eliminates the physical far tail at polynomial bandwidth and has no discarded-density or event-replacement term. Its signed middle integral, the full return complement and the unconditional microscopic Gaussian denominator remain unproved. This is progress in the requested local norm, not a replacement of that norm by global `L1`.

For request 5, the absolute arbitrary-selector estimate now applies directly to the actual physical endpoint, with a polynomial bandwidth. Evaluation of the weighted integral and a positive selected denominator remain explicit. For request 6, the new mechanism uses only finite horizon and straight-flight geometry, so it introduces none of the long-itinerary zero-extension questions. The earlier geometry is retained and still requires the independent specialist audit requested by the referee; no such independent human review is claimed.

Every microscopic estimate now distinguishes an absolute error from a denominator-sensitive relative conclusion. The super-exponential size permitted in the preceding-section reconstruction remains visible. Global mixed `L1`, unnormalized source TV, time-profile derivative measures and local pointwise inverses are named separately. Selector uniformity is described as contraction. The status table replaces repeated discussion inside the new proofs. We retain the single article and its original topic rather than split the manuscript. The new literature paragraph compares the exact age inversion with the Lorentz-process and suspension MLCLT literature, without treating those theorems as a radius-uniform local theorem for the moving-section record.

## 7. Source and execution evidence

The new source adds `core/67_exact_stationary_endpoint_inversion.tex` and `core/68_stationary_gaussian_complement.tex`. All 66 inherited core modules, 71 inherited Python files, 887 inherited labels and 18 bibliography entries remain; core, Python and bibliography files are byte-identical. Five replayable main-article edits add Theorem X and its proof route, with the prior abstract retained separately.

The baseline v32 verifier was executed before modification. The new source verifier checks the full baseline tree, every source hash, exact edit replay, all inherited labels and new references, and the exact controlling report in remote qualification. Finite diagnostics independently compare an overlap formula with direct trajectory evolution in a periodic suspension, test interval/Fourier identities, all-label tails, source-TV differences, polynomial bandwidth and covariance Jacobians, and detect omitted initial cell corrections and wrong Fourier signs. The model is deliberately not mixing; these checks do not pretend to establish the Gaussian theorem or the unresolved middle integral.

The final read-only workflow checks and compiles ordinary committed source, compares normal and optimized diagnostics, renders the new proof interval and emits an exact-run receipt. This static response does not predeclare that a future run passed. The revision is offered for substantive mathematical review of the same raw local-limit and physical-conditioning program.
