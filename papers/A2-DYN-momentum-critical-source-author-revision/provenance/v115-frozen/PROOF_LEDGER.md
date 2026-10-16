# Proof and dependency ledger — clearance-to-roof / critical-stability revision

## Scope and status language

This ledger concerns complete written author proofs, not independent human verification or a formal certificate. **Direct local proof** means a deduction on the stated physical/analytic chart; it does not mean uniformity across all collision counts. **Retained input** denotes an explicitly inherited dynamical statement not reconstructed independently here. **Open** means no subtraction or completed theorem may rely on it.

The original model is exactly `model.tex`: triangular equal-disk lattice, R in [9/20,47/100], collision measure dαdp/(4π), original augmented section and its fixed factor c*, physical roof, exact displacement k and occupancy n, and original central roof set. No independent events or altered clock are introduced.

## New proof bodies

| Anchor | Statement and exact range | Dependencies | Status |
|---|---|---|---|
| `thm:cr-jacobian` | At every regular finite marked itinerary and flight j, determinant of clearance-to-endpoint map is 1/(Rω); roof/Gauss determinant χ/(Rω); full Hessian chain rule | Exact line Jacobian270; actual invariant collision map; regular endpoint optical map260,265 | Direct finite-itinerary identity |
| `cor:cr-determinant-growth` | Determinants grow at least (600/2209)ρ^(-(m−1)), with an extra λ for roof/Gauss or critical Hessian | Previous identity; retained uniform optical bound and endpoint Hessian bound | Uniform physical determinant bound, not a condition-number or sum bound |
| `lem:cr-band` | C^ell real function with |f^(ell)|≥κ: band measure≤2ell(h/κ)^(1/ell) | Divided differences; repeated Rolle; measure quantiles | Direct analytic proof |
| `thm:cr-finite-type` | Local positive roof density≤(2ell H/b)(Bδ/κ)^(1/ell), arbitrary Borel selector | Explicit nonvanishing clearance derivative and finite-type constants on that rectangle; band lemma; Tonelli | Direct local conditional-hypothesis theorem; global constants not supplied |
| `thm:cr-fold` | Integrated simple fold≤2H√(2δ/(ab)); fixed-clearance density may diverge | Sθθ≥a, Su≥b, angular minimum exists; positive coarea | Direct local theorem with sharp analytic constant |
| `thm:cr-periodic` | Critical endpoint roof iff p0=pm=0; actual 2m reversing periodic orbit; roof2t, displacement0, occupancy A_m+A_m^I | Retained physical first variation; specular reversibility; unchanged section tests | Direct physical finite-itinerary theorem |
| `thm:cr-monodromy` | tr DT^(2m)−2=4 detG/G0m²; exact coefficient J=ω/(2c*√detG)=1/(Rc*√|det(I−DT^(2m))|) | Signed optical corner264; generating derivative; actual regular reversibility | Direct physical identity; not a trace formula |
| `thm:cr-critical-density` | D_E(t_x+s)=J a_E(s)+error; error≤2π√3(2Lw+Kw0)√s, 0<s<r0²/3 | Positive regular Hessian; smooth optical density; radial substitution; arbitrary Borel E | Direct local theorem; selector-uniform, not collision-uniform |
| `cor:cr-one-sided` | Same action-sector formula on actual physical side of unvisited tangency/section cut, positive visited incidences | Positive interior Hessian; IFT; previous theorem | Direct one-sided local theorem; no singular physical return derivative asserted |
| `prop:cr-critical-sum` | All regular exact-label critical coefficients at fixed m bounded by C0Q*/(2c*λ); individual bound47ρ^(m−1)/(12c*λ) | One-critical-per-word uniqueness265; explicitly retained pressure266; optical bound260 | Complete finite-count positive sum relative to retained input; unscaled |

## Explicit inequalities and normalization checks

1. Line mass is `(4π R c*)^-1 dθdu`, and `det D(S,arg g)=χ/(Rω)`. Dividing yields exactly `ω/(4π c*χ)`. There is one, not two, section factors.
2. Away from g=0, `D²(F∘Q)=DQᵀ G DQ+Σg_aD²Q_a`. The last term is not assumed positive or zero. At g=0 it vanishes and the determinant identity follows.
3. Divided differences cancel the constant a; separated quantiles give the factorial denominator. The safe coefficient is2ell, not an asserted optimal coefficient.
4. Fold integration gives `2H√(2δ/(ab))`; the fixed-u singularity is integrable in u under v'(u)≥b. No assertion at a zero clearance derivative follows.
5. Critical action density includes the two-dimensional polar Jacobian r and the inverse radial derivative. Their ratio tends to1 after Hessian normalization. This produces `2π w0`, not `π w0`.
6. The actual half-map derivative retains the sign of e=G0m. `det(I−M)` is negative, while the displayed positive weight uses its absolute value.
7. `A_(2m)=A_m+A_m^I` uses both endpoint section tests. The original section is not assumed reversal invariant. The doubled orbit has zero displacement even when its half displacement is nonzero.
8. The radial error is uniform over Borel selectors because their indicators are never differentiated. A limiting sector fraction needs the stated tangent-sector hypothesis.
9. At unvisited tangency, a smooth extension of the visited action is only a calculus device. The positive measure is still restricted to the real physical side. All visited incidences must remain positive for that extension.
10. The pressure input is used only after selecting at most one critical point per physical word. The per-path exponential bound is never multiplied by an unbounded word cardinality.

## Retained chain and novelty boundary

All active proof bodies260–269, and `model.tex`, `inputs.tex`, `comparison-scope.tex`, are byte-identical to the downloaded SHA-bound v112 source. Modules270–273 are byte-identical to the previous local clearance-flux extension. The earlier exact flux, transverse strip, conditional stable-test estimate, and exact mark kernel are not counted as new results. Original incidence MGF, two-ended depth polynomial, count tail, source identities, and normalized incidence payments are retained. The count restriction on the final retained source is already implied by its load condition.

Historical optical anchors238,239,241 available in the source packet remain pinned to blobs `c79fb9d660ab90370700c4fbfe4d4311175ac60f`, `fc76d61faeb70c0eeca6217c2c09daea4c3b2bde`, and `fa0f71468d1f304da492687d949ad00c953402e7`. Their inclusion is not an independent verification of the uniform pressure theorem.

## Current minimum closure interfaces — all still open

The controlling statement remains the original `eq:v112-remaining`, not a new residual. A proof must bound the complete positive shortage after the original physical summation, exact-label/radius/roof suprema and collision limsup, with B outermost.

**Clearance chart sum.** Establish sufficient control of the full one-copy exact-label weighted chart sum, including folds, non-fold finite type, full critical roofs and currently unclassified degeneracies. The bounds must yield the needed m^-2 normalized topology on fixed outer windows. Locally positive clearance powers alone do not supply this.

**Critical and boundary budgets.** Control the actual coefficient sums, their roof localization, and the explicit radial remainder constants on neighborhoods compatible with the original window. A separate shrinking chart at every collision count does not justify this uniform step. Integrate one-sided action coefficients with the original pairing construction; do not identify a bulk null set with a zero trace.

**Low-incidence and capacity.** Prove an original-source bound or valid full-pool abundance for the remaining shallow-incidence and capacity-deficient classes. Nothing in the new critical calculation establishes that abundance.

**Inherited global interfaces.** Reconstruct or independently verify the uniform pressure, stable optical comparison, complete one-copy pairing, null-set extension, spectral/arithmetic and inverse-problem dependencies under their actual norms and quantifiers. No generic correlation or fixed-window result is substituted for raw pointwise control.

These are unresolved interfaces, not additional assumptions under which we declare the requested main theorem proved. The final theorem and four-coordinate inversion target have not been weakened.


## V115 author revision — theorem-bearing double clearance geometry

- **Fixed genuine author baseline:** v114 branch `revision/a2-dyn-v114-clearance-roof-author-revision-2026-10-15`, complete source commit `8a5a7c2be5630bf5919e9f74ee79de01af0dbb85`, original packet tree `c2e9e83f39985a34690300433f4b40de4f1f88ac`, subsequent documentation-only head `d98549fc721f757ad2a4b5918d57110368acbf9f`. The full v114 packet is retained in `provenance/v114-frozen`; active modules 260–275 are byte-identical.
- **Controlling mathematical referee:** v112 report at `d7fd0b24314d7341f9a611130bb650371d2d5ef2`, blob `0ad9f500c92db32ea4fc9f6d9ee28630b4484699`. Supplementary v113 submission-state report at `d6e748a89845803d92b85570147bdc69825e49da` only addressed a workflow-only branch; it did not review v114/v115 math.
- **New complete lemma `lem:dc-transverse` (core/276):** for two *distinct* unvisited disks marked on one actual physical flight, finite horizon bounds their center difference and lattice spacing yields `|(z2-z1)·v| >= sqrt(591)/100`, because both signed impacts are within `2(R_+ + delta_*)=97/100`. Proof is finite-dimensional Euclidean geometry; no inherited statistical/dynamical transfer theorem.
- **New complete theorem `thm:dc-exact` (core/276):** exact positive, one-copy ordered two-mark collision-measure disintegration. Conditional inputs: the previously proven physical one-mark flux (`thm:cf-flux`), finite-horizon geometry, exact original line-coordinate Jacobian and the preserved physical mask. The extra denominator is precisely `sqrt(|w|^2-[sigma2(R+u2)-sigma1(R+u1)]^2)`. No symbolic word count or independence. Original return/displacement/collision/roof/section events are permitted as Borel selectors on both sides.
- **New complete theorem `thm:dc-factorial` (core/276):** the full invariant one-flight second factorial marked mass is bounded above by `2 Q_* delta1 delta2/(pi R c_pair)` with `Q_*` an explicitly finite lattice difference count using the original finite-horizon `tau_+`. This bounds *every* physical line/flight and both signs at fixed `R`. Nothing involving an unbounded number of physical words is inserted.
- **New complete corollary `cor:dc-unique` (core/276):** the first-order probability `nu(N_delta>=1)=delta/R+O(delta^2)` with explicit constants and positive unique-mark mass, derived from exact `nu(N_delta)=delta/R` and integer factorial inequalities. No Poisson model or independence is assumed.
- **New complete corollary `cor:dc-schedule` (core/276):** for the full original exact-label event and each original depth threshold `delta_j=2epsilon r^{d'_j}`, the positive total mass of **within-flight duplicate marking** is `<=8 C_pair epsilon^2/[c_*(1-r^2)]`, uniformly over `m,R,n,k` and bounded Borel roof tests. The derivation uses actual collision invariance and the two-ended depth sum. It is a weak positive-measure estimate and **not** an `m^2 L^infty` roof bound.
- **Verification boundaries:** `tools/check_two_mark.py` checks the exact rational discriminant, 1296 two-root/Jacobian identities, 18 sine-wave angular coarea comparisons, and 3000 actual Lorentz next-hit rays. Normal and optimized Python results are compared byte-for-byte. These diagnostics are not a continuum mathematical certificate, nor do they validate independent pressure or pairing-space inputs.
- **Unproved research target unchanged:** single unvisited near misses, clearance on different flights, low-incidence shallow source, capacity abundance, singular endpoints, global uniform normalized chart summation and the full `H_M(R_B^low)->0` remain unproved. They require the original `m^2 ess-sup`, `sup_{R,n,k}`, collision `limsup`, and outer `B` limit. No payment is spent twice.
