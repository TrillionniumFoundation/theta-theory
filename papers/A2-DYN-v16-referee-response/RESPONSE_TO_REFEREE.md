# Response to the latest referee: A2-DYN revision 16

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Active source:** `papers/A2-DYN-v16-referee-response`  
**Controlling report:** `reviews/a2-dyn-v14-external-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Report commit / blob:** `43d797ce65ad5e4cf92f874a6656c9cd0af9d572` / `197a42fbe2c815860423fa405f10e96cbe82e3d4`  
**Immediate author baseline:** `656104408b8f9d62ccab0b1d7bc847e3be950a08` (v15)  
**Date:** 6 October 2026

We thank the referee for distinguishing the completed joint nondegeneracy theorem from the remaining raw-inversion estimates. The already landed v15 revision supplied fixed-band quantitative collision-phase bounds and the detailed conditional-pair descriptions requested in the report. This revision continues from that source rather than duplicating it. Its principal addition addresses frequencies tending to zero and the passage from collision functions to the actual unbounded return record. It is stated as Theorem G and proved in Sections 29 and 30.

The title, physical table, actual return section, four-coordinate record, and raw mixed-density endpoint are unchanged. No inherited theorem or mathematical module is removed. Revision 15 has not received a separately located referee report in the branch set inspected for this revision; the present response therefore continues the v14 report, not an invented v15 assessment.

## A. Complementary frequencies and the actual induced record

The new result is a parameter-uniform lower bound for the one-step function defect of the genuine return record on a quantified region that includes the entire intervening annulus. It is not inferred merely from the absence of exact eigenfunctions.

### A.1. Diffusive collision damping with controlled endpoints

The established uniform ellipticity of `Gamma_R=c*D_R` and the inherited shrinking-scale perturbation theorem give a contraction of the stationary middle-block pairing at length `m=ceil(A/|z|^2)`. The collision observable is smoothed only in that middle block, at scale `delta=|z|^(1/12)/4`. The unsmoothing error is explicitly `O(|z|^(1/24)*sqrt(1+|log |z||))`.

The endpoints of an approximate unit phase are smoothed separately. They are separated from the twisted middle block by `O(1+log H)` untwisted collision iterates. Spectral mixing of those short end blocks removes the large endpoint BV cost, while deleting their phase costs only `O(|z|(1+log H))`. The full phase equation telescopes exactly with a defect cost equal to the full block length times its one-step defect. This proves a quadratic lower bound `c|z|^2`, uniformly in the radius and in any constant collision phase, when `|z|(1+log H)` is sufficiently small.

The modulus-variance and circle-truncation argument then proves an `L2` lower bound `c|z|^2/[1+log(H/|z|)]` for normalized complex collision functions, including functions with zeros. No positive lower modulus is assumed, and the proof never makes the discontinuous compensation an anisotropic multiplier.

### A.2. Quantitative finite collision geometry

The new finite-record lemma does not infer a long-iterate variation bound from one-collision BV. It encodes each actual flight and reflection with a bounded-degree polynomial graph and auxiliary state variables. The no-earlier-hit condition is obtained by explicitly minimizing the squared distance along each candidate flight segment. A word of length `L` uses `O(L)` variables and polynomial tests, with only exponentially many label alternatives.

The finite sign-condition connected-component bound recorded by Basu--Pollack--Roy in Section 3.2, equation (3.3), applied before projection, bounds components of slice superlevel sets. One-dimensional coarea then bounds both first distributional derivatives, including itinerary jumps. This gives a safe budget `exp(C L log(2+L))` for the bounded coordinate record and smooth compositions. It is uniform in the radius and in the moving rectangle coefficients, and does not assert a pointwise derivative bound at grazing. The source import and all geometry-to-complexity steps are documented in `FINITE_RECORD_INPUT_MAP.md`.

### A.3. Exact tower localization and regularization

For a section function `f`, the lift at age `j` is the original `f` multiplied by the exact compensation phase accumulated since the last section visit. At every nontop level the collision equation is exact. The only error occurs at the true tower top and is exactly `f o F - exp(i z.(G-Gbar)) f`. The `Lp` defect identity has the factor `c*`, while the lifted function norm uses `c* integral r* |f|^p`; these two normalizations are not interchanged.

The lift is not presumed BV. Truncation in age, smoothing of the initial section function, and the finite-record lemma give an explicit regular approximant. The actual one-return exponential tail controls the omitted ages. For age cutoff `L` and smoothing scale `epsilon`, the `L1` error is `C[L epsilon V_f + M_f exp(-cL)]`, and the first-variation budget is at most `M_f exp(C L log(2+L)) (1+epsilon^(-1)+|z|)`. The `L2` error is obtained using the actual supremum bound. This is a proof approximation only; the theorem concerns the full unmodified return law.

### A.4. New actual-return conclusion and annulus

Let `r=|z|`, `Lambda=1+log(H/r)`, and `K=Lambda log(2+Lambda)`. When `r*K` is small, the actual return circle defect is at least `c r^2`; the normalized complex-function defect is at least `c r^2/K`. These constants are uniform in the original physical parameter. The proof of the complex case accounts for the dependence of the regularity bound on the selected approximation accuracy, so the choice of accuracy is not circular.

For `H<=H0 n^zeta`, the estimates apply on the whole physical annulus `2 n^(-99/200)<=|z|<=n^(-2/5)`. Its rescaled version is `2 n^(1/200)<=|sqrt(n) z|<=n^(1/10)`. The complex defect lower bound is at least `c|z|^2/[log(2+n) log log(e^e+n)]`. This supplies a quantitative actual-return input in the frequency region singled out in the report, with both frequency scales and the regularity loss explicit.

### A.5. The remaining conversion to a complementary integral

The new theorem is for a physical function defect at the centered multiplier `exp(i z.(G-Gbar))`. It does not assert an arbitrary induced eigenvalue bound, a quasi-compact realization for the full induced twists, or decay of their powers. For a distribution-space application, the vector reconstruction, its normalization and regularity, and its defect comparison must still meet the displayed budgets. The actual complementary Fourier integral, including the compact nonzero band and growing/far roof regimes, remains a separate estimate. The new annulus defect is not relabeled as that integral.

## B. Complete critical and singular branch extraction

The original critical-edge and localized/global residual-inversion sections remain intact. The finite-record lemma estimates first variation of bounded functions in initial collision coordinates; it does not estimate inverse-coarea Jacobians, their second distributional derivatives, or the sum of local density jumps. All critical, grazing, competing-root and dynamically generated image-boundary contributions remain in the required raw extraction. No claim about their summation is made merely from the finite graph complexity.

## C. Weighted exact-conditioning chain

The inherited initial and single-marked central and moment theorems retain their original insertions, measure conventions, and exact denominators. The new tower lift is a map for a specified section function, not permission to replace an exact physical event or to identify a multiple-time indicator with a controlled marked-state function. Weighted complementary tails, weighted local-edge bounds, and relative event replacement remain the exact tasks required for the physical conditioning endpoint.

## D. Independent review and presentation

The next specialist review should check the middle-block spectral word, the sign and top normalization of the exact lift, the lifted finite-word semialgebraic graph, projection/component and slice-coarea argument, and the accuracy-versus-BV budget. The new imported input is precisely the finite sign-condition bound; the previously reviewed billiard, BV, covariance and return-tail inputs are retained. Independent human review is not claimed.

All fourteen presentation comments are covered by the retained v15 clarifications and the new source: stable/unstable coordinates and pair densities, four-corner orientation, same holonomy signs, physical-cover geometry, separate coprime rotation products, exact-versus-approximate distinctions, both cutoff scales, Gaussian-versus-physical tails, Cesaro terminology and the exact edit ledger remain visible. Theorems A--F are retained, and Theorem G is an additional result on the same record.

## E. Source preservation and qualification

All 35 inherited core modules are byte-identical. Every inherited Python script and every old mathematical label remains. The exact inherited edits occur only in the introduction and bibliography: the new theorem, abstract and proof-route additions, two new inputs, revision identity, and one new reference. `SOURCE_MANIFEST.json` records every actual file hash and the frozen baseline hashes. The read-only qualification workflow runs normal and optimized diagnostics and native TeX on the exact committed source. Its dynamic receipt records the event SHA, run ID and PDF hash; this response does not predeclare a future run successful.

The revision is submitted for renewed substantive review of this additional actual-return near-origin proof, while retaining the original raw mixed-density objective and its remaining analytical requirements.
