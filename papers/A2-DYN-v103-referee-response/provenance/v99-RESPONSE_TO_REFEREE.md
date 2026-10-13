# Response to the external report on A2-DYN revision 98

**Author:** Qian Qi. **Revision:** 99, 13 October 2026.

**Controlling report:** `reviews/a2-dyn-v98-external-top4-review-2026-10-13/REFEREE_REPORT.md`, commit `357e47da83265ac52bbc65b524aecccc6100508b`, blob `041bdf3eb46f24c09dbc1a469a5e728713c4d900`.

**Frozen author baseline:** `3727d8bdcf7751f4aaec9b92cf9fa85be1ea0ce2`, paper tree `8f84ba8e9b48373d1acbeac7a3c2d93cb3403bfb`. The new author branch starts directly from the controlling review commit. All 237 inherited cores and the entire preceding article are preserved.

We thank the referee for requiring an actual comparison from the endpoint-momentum fiber to a dynamical pressure sum. This revision proves that comparison. It begins with a global uniqueness theorem for prescribed lifted itinerary and endpoint momenta, then compares the precise optical weight to the stable Jacobian and removes a marked incidence without leaving an uncontrolled homogeneity-strip count. The fixed-table pressure theorem consequently verifies spectral capacity at every fixed radius. A separate finite-block theorem bounds the full-family capacity exponentially through uniform geometric block sums. Its strict family-uniform spectral margin, and the positive nongrazing paired short-trace height, remain separate tasks. The original uniform pointwise objective is unchanged.

## 1. Weighted fiber growth and condition (SC) — request 12.1; report §§5,9,11

Theorem `thm:v99-unique` supplies a genuinely global statement, not an inference from the local Hessian: for a fixed lifted scatterer itinerary and prescribed two endpoint momenta there is at most one regular physical trajectory. The proof applies monotonicity of the gradient of the convex Cartesian flight action to two physical configurations. Reflection turns its monotonicity pairing into a negative sum of squared normal differences, while equality of the two endpoint momenta cancels the tangential terms. All coefficients are positive. No convexity of the physical angular domain or continuation through a singularity is assumed.

Lemma `lem:v99-stable-weight` proves the required optical normalization against the invariant stable Jacobian. In standard arclength/angle coordinates, the full twist is the upper-right entry of a product of positive flight matrices. A fixed initial-column comparison and a fixed final cone comparison give `omega` comparable to `c_m J^s T^m` with constants that do not grow with collision count. Conservation of collision area includes the ratio of the two stable/unstable angles. The one-step bound `J^s T/c <= C` removes the inverse incidence at each internal mark.

Theorem `thm:v99-pressure-comparison` now proves

`K_m(R) <= 1+C[P_m(R)+D sum_i q0^d_i P_i(R) P_(m-i-1)(R)]`.

The sums are over actual lifted itineraries with the supremum of their stable Jacobian, not over unweighted words. Global uniqueness supplies one momentum preimage per itinerary. The single omitted step has only `D` physical displacement choices; an infinity of homogeneous strips is not counted at that step. Each geometric itinerary sum is bounded by the established homogeneous continuity pressure sum, because that partition refines true physical itineraries. Thus this is precisely a bridge to the same fiber weight requested by the referee, not an identification of unlike partition sums.

For each fixed radius, Baladi–Demers' proof of Lemma 3.8 gives a bounded stable-Jacobian partition sum at potential parameter one. Corollary `cor:v99-fixed-radius` therefore gives `sup_m K_m(R)<infinity` and verifies fixed-radius (SC) at every fixed auxiliary band. This is a collision-asymptotic conclusion, stronger than fixed-count definable finiteness. It no longer assumes a rate for an unspecified fiber cardinality.

The source's principal uniform radius quantifier is not silently changed. The cited fixed-table theorem alone does not provide a uniform constant on the full interval of radii. Theorem `thm:v99-block` instead proves an actual family-uniform exponential bound through `sup_R P_L(R)` at each fixed block length `L`. Its strict margin `(max(1,sup_R P_L^(1/L))) theta_Bstar^2<1` is a concrete sufficient certificate for uniform (SC). It is not verified over the whole continuum of radii in this revision. The uniform SC flag consequently remains false; only the previously absent growth-bound flag is explicitly superseded.

## 2. Positive paired short trace — request 12.2; report §7

The two physical endpoint traces remain paired on the same original maximal segment and with the same target selector. The new capacity comparison makes the full comparison error and every grazing-ended short source unconditionally small at each fixed radius: their ordered heights are at most `C(1+epsilon^-1)delta`. No positive initial-gradient or internal-incidence corridor remains. This is a genuine removal of the previous capacity premise for those source components.

It does not make a positive nongrazing paired minimum vanish. Such a minimum is neither the Jordan positive part of a projected signed current nor a source that can be canceled merely because the difference of its two traces is small. The positive nongrazing paired height remains unproved, even for a fixed radius. The response does not declare request 12.2 closed or replace it by an integrated trace-mass result. A backward critical trace is also retained unless an actual grazing incidence forces it to vanish.

## 3. Independence of the two obligations — request 12.3

The pressure comparison addresses the inverse-gradient capacity mechanism. It is sufficient to remove the capacity hypothesis at fixed radius and provides an explicit uniform block criterion. It does not assert a short-trace deconcentration theorem. Conversely, a hypothetical paired-trace height theorem would not certify the remaining uniform block margin. The final section displays the fixed-radius consequence and the original uniform consequence separately, with their distinct conditions adjacent to the formulas.

## 4. Scalar reduction and retained schedule — request 12.4

Theorem `thm:v99-fixed-recovery` first inserts the bounded fixed-radius capacity into the complete finite-count two-cap remainder. At each fixed band, the remainder is bounded by a polynomial times `K_R^(1/3) theta_Bstar^(2m/3)`, and tends to zero. The auxiliary band is enlarged only afterwards. The target-direction loss certificate then proves the fixed-radius critical height `C(qr)^(257/256)`. The short-trace comparison uses the same uncut insertion and retains the original guard cost.

With `q=1/8`, `r=c epsilon(B)^4`, `a=sqrt(qr)` and `delta=6qr`, the scalar reduction is valid at every fixed radius without an extra capacity hypothesis. Its critical term has power `epsilon^(257/64)` and its comparison term has order `epsilon^3`. The positive nongrazing trace remains in the inequality, so the scalar pointwise theorem is not marked proved. For the full radius-uniform assertion the same reduction is conditional on the explicitly stated finite-block margin. No interchange of `sup_R` and `limsup_m` is made.

## 5. Downstream laws — request 12.5

No unrestricted denominator, reciprocal, posterior, likelihood, relative entropy or path-space law is promoted. The prior lower pointwise and finite-roof-norm results retain their stated status. The unrestricted upper half and full raw LLT still require scalar closure. All zero arithmetic classes remain in the unnormalized target and are never divided by.

## 6. Independent verification — request 12.6

No independent human specialist approval has been obtained. The new audit map isolates the global convexity pairing, the endpoint tangent signs, the nonaccumulating matrix comparison, the collision-area angle factor, the removal of the marked stable step, refinement by the true homogeneous continuity partition, and the fixed-radius versus uniform quantifiers. The inherited four-record spectral theorem, coarea disintegration, positive scalar remainder and paired trace construction remain precisely stated inputs, not claims certified by finite tests.

The primary pressure reference was read directly: the published paper's arXiv v3, including the explicit boundedness of `Q_n(1)` in the proof of Lemma 3.8. That reference is not represented as an endpoint-momentum theorem, nor as a theorem with a parameter-uniform constant not stated there.

## 7. Exposition — report §13

The active abstract and new results say “down to zero gradient” where integrability is meant; inherited historical text is preserved verbatim. Each capacity-dependent result keeps its condition adjacent to its statement. The principal new uniform growth bound is not labeled uniform (SC). Fixed-radius capacity boundedness is not labeled radius-uniform convergence. The positive paired minimum, a grazing zero trace and a possibly nonzero critical trace remain distinct objects.

The manuscript uses the original title, physical problem, exact source, guard and arithmetic reference. Its theorem-proof narrative now contains the global uniqueness and pressure comparison before the new unconditional fixed-radius consequences. All six active proof modules are in the focused article; all 237 inherited cores and the complete preceding article are in the archive. No historical paper or review is edited, and no different journal objective or substitute problem is introduced.

## Qualification and exact claim boundary

The new exact-SHA workflow pins the v98 paper tree, its complete v99 snapshot, the current controlling review blob and both v88 variant trees. It checks inherited bytes and executable modes, the single explicitly justified growth-flag supersession, normal/optimized finite fixtures, native article and complete archive, all 240 recorded cores, reference stability and page geometry. Passing v98 workflows are baseline receipts only; v99 remote results must belong to the final v99 SHA.

The substantive improvement is an explicit dynamical estimate for the actual momentum-fiber capacity and its fixed-radius closure. Uniform (SC), positive nongrazing paired-trace height decay and the original full pointwise theorem are not marked complete. Neither successful qualification nor the presence of a new theorem file changes those mathematical boundaries.
