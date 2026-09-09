# A2 v2 — proof dependencies and source preservation

Controlling review: 14aaea8937f8b2d373bc642f3568d7280dcbbbd7.  
Reviewed source: 500cf06faccb6eadd6c122abeb63c60a0cb7522e.  
Full reviewed native tree: 2e4303afeec148b5c318629443463db301d6e3c5.

## Primary geometric chain

1. **Lemma 9.1**, `lem:g-channels`: support parametrization, strict convexity, the nearest/next-nearest lattice gap, positive distance Hessian and specular angular separation verify complete-event localization. This supplies the actual itinerary selection and first-hit clearance; no initial transverse ensemble is assumed.
2. **Lemma 10.1**, `lem:g-jacobi`: two-periodic diagonal scaling reduces the alternating-curvature Jacobi recurrence to a constant one. The effective endpoint Hessian and its twist/determinant quotient are explicit, with curvature parity retained. The quotient is csch(j gamma), while the physical return multiplier is exp(2 gamma).
3. **Lemma 10.2**, `lem:g-relative`: exponential Green bounds and weighted contraction produce a nonlinear endpoint bridge on a length-independent chart. Cubic action terms and first-order relative amplitude errors are allowed. Summability of endpoint weights and trace-norm perturbation of the tridiagonal determinant preserve relative, rather than merely absolute, flux accuracy. Finite-order smooth derivatives follow by differentiated inverse equations.
4. **Lemma 11.1**, `lem:g-radial`: a uniform smooth Morse chart and odd-term cancellation in radial integration yield a smooth right remainder in the onset offset, without assuming reflection symmetry of the scatterer.
5. **Theorem 1.1**, `thm:g-stability`: stationary first-impact flux is integrated with the full residual variable. Coercivity covers the entire active sublevel. Localization partitions the complete maximal-count event into the six smooth candidate channels. Positive parts of their own offsets retain minimizer switches; there is no differentiation of the nonsmooth shortest-gap minimum.
6. **Theorem 1.2**, `thm:g-marked`: deviations of smooth additive marks from axial values have summable endpoint derivatives. Smooth radial integration proves the relative expansion. Exact parity and positivity give necessity and sufficiency of the axial real-source domain and allow fixed-order differentiated summation on its compact interior.

The old circle is obtained by equal curvatures 1/R, gap 1-2R and six equal orientations. The complete former proof remains active, so the general statement does not remove any previously established special-case detail.

## Moving geometry and inverse consequence

**Corollary 11.2**, `cor:g-interfaces`, differentiates the exact positive-part sum and retains the second-derivative jump of each oriented contribution. Reversed and other coincident orientations are added. The support family R+s cos(2 theta) verifies an actual change of shortest pair. The transition width epsilon/j follows from the smooth gap difference.

**Theorem 12.1**, `thm:g-inverse`, constructs support functions with identical values and first jets at all six lattice normals but independent second jets at the three unoriented contacts. Supporting halfplanes prove exact equality of their gaps. The general threshold theorem gives their unlabelled amplitude sum. Absolute convergence justifies odd Möbius inversion. Positive finite Hankel factorization recovers the exponential nodes, weights, free area and multiplicities. The observed gap then recovers the curvature multiset. In the equal-curvature one-parameter subfamily the first two amplitudes suffice. Neither a global boundary-rigidity result nor noisy-data stability is asserted.

**Corollary 12.2**, `cor:g-selection`, compares positive channel coefficients at equal metric thresholds. It proves exponential selection by the smallest instability exponent and distinguishes leading-amplitude weights from fixed-positive-offset corrections.

## Record topology and differentiated tests

The density in Section 13 is on a common latent domain. The record metric is the maximum over scaled positions, excess impact times and transverse traces, not an unnormalized Euclidean norm whose dimension grows with j.

**Proposition 13.1**, `prop:g-smooth-tests`, proves response for smooth tests with bounded maximum-norm operator derivatives. Taylor division extends the scaled records smoothly at zero; endpoint summability controls full time sums. Parameter derivatives act on the exact density and parametrization. The stronger circular unweighted convergence statement remains unchanged.

**Proposition 13.2**, `prop:g-moving-cut`, integrates a transverse sampling inequality over its exact interval and applies Leibniz' rule. The boundary evaluation term is essential. The support |z|<1/2 with moving offset a=1/2 verifies uniform margins for every chosen impact index. Fixed schedules produce additional k/d factors; arbitrary bounded decoders are not silently included.

## Literature and historical inputs

Section 14.3 reads Carney–Nicol–Zhang's periodic rare-event theorems against the physical onset regime; it does not assert that statistical detection of instability is new in itself. Classical stationary/Palm identities, action-Hessian identities, marked-length inverse data and perturbative statistical limit laws retain their separate uses.

The preserved Round 33 A2 chapter proves a Diophantine separation statement and a Fourier inversion theorem conditional on actual frequency envelopes and an integrable central remainder. None of those model-level analytic hypotheses is supplied merely by the threshold series. The new geometric proof does not import statistical A1 as a replacement for dynamical operator estimates.

## Exact preservation

All original eight section objects, all 18 inherited statement blocks, and all 17 inherited proof blocks remain intact. The companion is unchanged. The new active closure has 16 TeX objects and contains 29 statement blocks and 28 proof blocks. Historical source, review and verification subtrees are preserved by using the full prior native tree as the Git base, with additions only except the explicitly versioned main entrypoint, README and submission index.

`verification-v2/PRESERVATION.json` records the block comparison and unchanged section identities. `NATIVE_BUILD.json` identifies the current compiled source objects, all six passes, PDF hashes and final reference/layout checks. `VALIDATION.json` separates exact identities and non-interval numerical diagnostics from analytic proofs. Historical v1 verification files do not purport to describe the new build.
