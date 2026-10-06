# Response to the external referee: A2-DYN revision 22

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Active source:** `papers/A2-DYN-v22-referee-response`  
**Controlling report:** `reviews/a2-dyn-v20-external-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Report commit / blob:** `a77d1b0af695877bcd43ddb494c637d8353d9b10` / `43f1370dec04d18fcbdebb91b0ddb3b95bb74359`  
**Reviewed author baseline:** `b5b209000bbef852076f413ef4f718137aeb4dd3`  
**Frozen baseline paper tree:** `cbfa76a8957d3d327655a9969d55cb4a9d3e24bb`  
**Date:** 6 October 2026

We thank the referee for identifying precisely the difference between the direct mean-square theorem and the prescribed-count raw inversion problem. The new revision supplies a theorem at each prescribed return count, on an enlarged inner frequency annulus and with the actual raw normalization. It does not try to extract a pointwise coefficient from an averaged estimate. The title, physical family, actual section, four-coordinate record, and raw mixed-density endpoint remain unchanged. All inherited core modules and theorem labels remain; the new result is additional to Theorems A--K.

The existing v21 response branch was inspected and still pointed to the v20 review commit, rather than to a distinct revised article. Revision 22 uses new branches and does not alter that reserved branch. It continues the actual v20 report, not an inferred or invented later review.

## A. A fixed-return estimate, rather than another return-count average

Theorem L in the introduction and `thm:fixed-return-inner-annulus` prove, uniformly in the physical radius and the location of one actual-return mark,

`n^2 integral_{2 n^(-99/200) <= |z| <= 2 n^(-12/25)} |Phi_n^[k],a(z)| dz <= C[M_a n^(-1/200) sqrt(log(2+n)) + V_a n^(-13/100)]`.

The count is precisely the prescribed `n`. The integration is not divided by the annular volume. The original probability is obtained by `a=s_R`. This proves a fixed-count raw-scale estimate on the inner portion of the region in request A; it does not claim to cover its entire outer, peripheral, or far-roof region.

### A.1. Finite connected correlations

The collision-gap smoothing proof used at orders two through four in the inherited moment section extends to each fixed finite order. With `q` factors, smoothing error is `O(epsilon)` and the chronological operator word across the selected gap costs `O(epsilon^(-2q) theta^gap)`. The choice `epsilon=theta^(gap/(2q+1))/4` gives exponential factorization at that order. No long-pullback BV bound is used.

The joint cumulant is defined by its finite set-partition polynomial. Split the ordered collision times at a largest gap and compare with independent copies of the two whole blocks. Every mixed subset moment changes exponentially little across that gap, and the independent-block cumulant is zero. This bounds the original cumulant by an exponential in the largest gap. The sum over anchored relative times, including a diameter factor, is consequently finite. The exact multiplicity of an anchored tuple is `(m-diameter)_+`, giving a linear-in-length cumulant with a uniformly bounded boundary correction.

All orders are fixed before any limit is taken. There is no assertion of a common factorial bound in the order, analyticity of the unsmoothed moment generating function, or validity of a cumulant series at a frequency growing with the order.

### A.2. Finite spectral jets with the true analytic remainder

For the smoothed bounded collision observable, the stationary finite-time pairing is `exp(m psi(t)) A(t)+E_m(t)`. At a fixed smoothing scale, divide the derivatives of its logarithm by `m` and let `m` tend to infinity. The relative complementary term decays exponentially, and the amplitude term divided by `m` vanishes. The connected-correlation limit identifies each derivative of `psi` at zero, with a bound independent of the smoothing scale.

This identification is done at fixed smoothing scale; no uniform interchange of two limits is assumed. Only after identification are the uniform cumulant bounds used. A Taylor polynomial of degree `Q` therefore has uniformly bounded coefficients, while its remainder is still `O_Q(delta^(-2(Q+1)) |z|^(Q+1))` from the original complex disk of radius `a delta^2`. This remainder is not replaced by a scale-free error.

Uniform covariance positivity makes the quadratic part negative on real frequencies. With the displayed remainder small relative to `|z|^2`, the smoothed collision powers satisfy `C exp(-c m |z|^2)` in their existing local distribution spaces. This is not decay of the unitary return Koopman operator norm.

### A.3. Actual marked stopping and the explicit feasible scale

At the marked return, the deterministic approximation is a two-sided interval with length `n/c*+O(1)`. Its smoothed pairing has exactly one multiplier between two chronological collision powers. The multiplier costs `C M_a delta^(-2)`, including the initial and terminal marks where one power has length zero. The new damping controls both powers.

Removing insertion smoothing costs `C delta V_a`. Removing observable smoothing costs `C M_a |v| sqrt(delta(1+|log delta|))`. The inherited actual stopping theorem costs `C M_a(1+|v|) n^(-2/9)`. No induced gap or grid reconstruction is introduced.

Choose `Q=19`, `delta=n^(-21/100)/4`, and `|v|<=2 n^(1/50)`. The analytic-radius margin is `3/50`; the Taylor remainder relative to the quadratic term has margin `6/25`. After four-dimensional integration, the insertion, observable, and stopping margins are respectively `13/100`, `1/200`, and `11/90`. The damping term on the inner annulus is at most a fixed power of `n` times `exp(-c n^(1/100))`.

These strict inequalities provide one feasible set of exponents independent of the radius and of `n`. The older cubic remainder cannot be reused at this scale: its bound grows with exponent `41/50`. The finite-jet proof is essential. The finite diagnostics explicitly reject that invalid substitution and reject a degree-15 polynomial, whose remainder margin at the chosen scale is zero rather than strictly positive.

### A.4. Larger central integral and its boundary

Combining the new annulus theorem with the unchanged central theorem gives an integrated Gaussian comparison on `|v|<=2 n^(1/50)`, with error `C[M_a n^(-1/200) sqrt(log n)+V_a n^(-9/175)]`. The original narrower band retains its sharper `n^(-3/280)` rate. The proof also gives a general sufficient range `1/200<epsilon<1/42`, by choosing a fixed finite Taylor degree and a smoothing exponent in `10 epsilon<theta<1/4-epsilon/2`.

The concrete outer radius `2 n^(-12/25)` remains below the previously contemplated `n^(-2/5)` regime. The intervening farther annulus, compact nonzero lattice frequencies, growing roof frequencies, and the full edge-subtracted complement still require estimates. The new theorem proves a proper inner-region result; it does not declare the full complementary integral complete or turn a sufficient parameter range into an impossibility statement.

## B. The long-time constructible packet

The full finite-count extraction, including all critical, singular, grazing, competing-root and image-boundary contributions, is retained byte-for-byte. The convergent analytic-unit explanation in the v20 source is also retained. The present cumulant bounds are bounds for collision observables, not for the inverse-coarea density or its derivatives.

The new raw inversion theorem exposes the exact same `A_2(n,L_n,R,1)` at a linear count cutoff. It establishes no new uniform growth bound for its coefficients, germ radii, exponent gaps, number of singular cells, or second-derivative sum. Those quantitative requirements remain explicit in the proof ledger and are not replaced by the finite-order collision estimates.

## C. The local extracted-edge correction

The new theorem `thm:expanded-count-localized-inversion` replaces the proof cutoff by physical radius `n^(-12/25)`, with support twice that radius. The exact extraction identity is repeated with this kernel. In particular the edge correction is now `e^L - Ktilde_n*E^L`; it is not assumed to satisfy an estimate for the old kernel.

The original high-count measure is separated from the true central count labels by order `n`. For the new kernel the normalized Schwartz bound is `C n^(2/25-13M/25)`, so it is smaller than any prescribed inverse power after choosing `M`. The central full-law term is controlled by the new fixed-count comparison. The remaining local edge correction, finite-band residual integral and far-roof term `n^2 A_2/(pi B)` are displayed without suppressing their actual `n` and radius dependence.

Thus the larger cutoff is used in an exact identity for the original raw density, not merely reported as a separate spectral observation. A uniform local bound for the extracted-edge correction itself is not established in this revision.

## D. Weighted fixed-count conclusions and insertion classes

The new inner-annulus theorem covers a complex bounded-BV function of one actual return state, uniformly in the location of that return. Its supremum and zero-extension variation losses are separate. It does not extend the fixed-count estimate to every arbitrary `L2` weight in Theorem K; that earlier arbitrary-`L2` averaged theorem is retained with its exact scope.

The new unchanged-event corollary divides the exact marked numerator by its actual event probability. On the enlarged band, convergence follows when `p_n>=c n^(-beta)`, `V_n<=C n^kappa`, `beta<1/200`, and `beta+kappa<9/175`. Events may vary with the specified count under these budgets, but no indicator or denominator is replaced. This absolute-error estimate and the averaged squared-`L2` theorem are not assigned the same normalization by analogy.

The complete weighted residual, local-edge and denominator asymptotics for the original physical observation classes remain additional requirements. A finite-record subanalytic weight is not presumed to have the uniform BV budget of the new marked theorem, and a logarithmic-window event is not silently identified with a single controlled state weight.

## E. Exact physical-event replacement

No comparison of a completed-return event with an exact physical-time/lattice event is performed here. The original unfinished-return bounds and same-event conclusions remain intact. The required relative event error must still be estimated against the true raw-scale denominator. The new conditional statement is not used to discard a pathwise unfinished-return error under a rare lattice constraint.

## F. Independent review and source inputs

The load-bearing inputs are the inherited collision-space spectral splitting and smooth multiplier estimate, mean-preserving BV smoothing, the actual covariance positivity, and the established two-sided stopping comparison. The added cumulant algebra, anchored summation, spectral derivative identification, finite Taylor estimate and frequency bookkeeping are all proved in the two new sections. The added Doring--Jansen--Schubert bibliography entry is background, not an imported theorem closing one of these steps.

An independent specialist should particularly examine the finite-order mixed-moment comparison, the fixed-smoothing spectral limit, the relative quadratic remainder, and the marked chronological product. Independent human review and formal proof certification have not been obtained in this author revision. The exact finite models test algebra and implementation, not continuum billiard inputs.

## Presentation comments 1--15

Theorem K keeps the word "averages" and all its bounds unchanged. The prescribed-count target with the `n^2` factor, and the growing `n^(2/5-2/495)` budget of the old average, are now immediately after its synopsis. The Cauchy statement is followed by its fixed-rescaled-test-frequency limitation and remains distinct from the physical Gaussian law. Fixed-mark and terminal-mark averaged arguments, exterior cyclic-vector Abel terminology, the exact historical exponents, the analytic-unit convergence source, and the negative average-to-fixed-time diagnostic are all retained.

Theorem L is explicitly a fixed-count result for an inner annulus and uses a controlled marked BV class. Its enlarged-cutoff raw identity lists every residual requirement. The new source preserves exact edit accounting and records dynamic execution evidence separately from proof status. The raw-density topic is not separated into a different paper or replaced by a specialist-journal target. It remains the organizing problem, with a new proved fixed-count region and the farther requirements stated precisely.
