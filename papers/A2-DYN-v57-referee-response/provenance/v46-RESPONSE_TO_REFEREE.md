# Response to the external referee: A2-DYN revision 46

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v45-external-top4-review-2026-10-08/REFEREE_REPORT.md`.  
**Frozen report commit / blob:** `0ada8feead815b267b530a92ed4e14f5445867f2` / `d9169afd510d4acb97bf79da6d811c2af0a04f9a`.  
**Reviewed author SHA:** `5ab781065787b1aca00ff5182a62da49f847d2e4`.  
**Frozen ordinary paper tree:** `7018b86390ed6090f6bc9cb043d4302cd31492e7`.  
**New article:** `papers/A2-DYN-v46-referee-response/main.tex`.

We thank the referee for the detailed audit of the complete-height, cusp-separation and protected-collar arguments. This revision responds to the new v45 report. It does not recycle the v35 response, change the record, average the exact return index, or replace the arithmetic transition kernel by an unmodulated Gaussian. The principal addition is a genuine local-scale estimate for the protected noncritical inverse, which was outside the v45 critical-source theorem. It is combined with the retained critical analysis to control the entire smoothly protected source.

## 20.1. Exhaustion of protection scales

The new guard `Xi_m^epsilon` is an explicit product over the original incidence, section-decision and nonincident-clearance margins. It equals one on all `2 epsilon`-protected histories and vanishes outside the `epsilon`-protected class. Its weak endpoint gradient is bounded by `C epsilon^-2`, independently of word length: a differentiated guard costs `epsilon^-2 q^(d/2)`, and the contact-distance sum is geometric.

Theorem `thm:v46-protected-correction` gives an explicit protection/bandwidth relation, `B >= C epsilon^-12`, and a normalized collision-limsup correction bound `C(M+L) B^-1/2`. Hence protection can be exhausted in the ordered scale `epsilon(B)=A B^-1/12`, with the collision limit taken at every fixed band first. Proposition `prop:v46-protection-mass` shows that the complementary original source has mass at most `C epsilon`, uniformly in the collision count. This is an actual source exhaustion, not a word-count assertion.

There is also a count-dependent slow diagonal for any prescribed diverging bandwidth. It is stated explicitly as qualitative, with no prescribed decay rate for `epsilon_m`. We do not infer arbitrary count-dependent protection thresholds from the fixed-protection theorem. Nor do we claim that exhausting the source in mass exhausts its central pointwise density. The remaining pointwise condition is retained in `eq:v46-boundary-criterion`.

## 20.2. Unprotected boundary source

The new mass estimate includes all three kinds of collapsing margin. In collision coordinates the grazing mass is `O(s^2)`, the section-boundary neighborhood has mass `O(s)`, and nonincident near-clearance has mass `O(s)`. The last assertion is proved directly: for a regular flight close to a nonincident disk, the closest point is interior; the angular derivative of the line-to-center distance is uniformly separated from zero because the initial point is at least `53/100` from that center and the radius is at most `47/100`. Summing the exponentially decreasing thresholds and using collision invariance gives `O(epsilon)` uniformly in the history length. No mixing or independence is needed for this step.

The complement is defined as the positive source `(1-Xi_m^epsilon) nu_R^*`, at unchanged exact labels. It includes the unprotected finite jumps and their noncritical residuals. The theorem does **not** assert central-scale pointwise smallness for this complement. The mass bound is not promoted to such a statement.

## 20.3. The noncritical signed inverse

This is the main new analytical estimate. Module 98 proves it in four steps.

1. The existing tridiagonal endpoint-response argument is extended to arbitrary protected regular histories. Normal endpoints were not needed for the internal inverse or continuation. General endpoint cosines cost only `epsilon^-2` in the logarithmic derivative; the internal potential still costs `epsilon^-3`. The endpoint Hessian has a uniform upper bound.
2. On `|grad F| >= delta`, the vector field `V=grad F/|grad F|^2` translates the roof exactly. It is followed for `h=c epsilon^3 delta^2`, staying on the same physical word and retaining every section decision and exact integer label. Its weighted divergence is bounded by `C(delta^-2+epsilon^-3 delta^-1)`, so its physical Jacobian ratio is between `e^-1` and `e`.
3. The flow is injective on a roof level times its flow interval; distinct words remain disjoint. Consequently a level integral is bounded by `e/(2h)` times the original exact-label roof-window probability. The fixed-window transition theorem bounds the latter by `O(h m^-2)` after the collision limsup. No word count is present.
4. Integration by parts with the explicit source and gradient cutoffs proves that the actual noncritical density is in `W^{1,infinity}`. Its first-derivative budget is
   `m^2 ||g'||_infinity <= C [L/delta + M(epsilon^-3/delta + delta^-2)] Q_m(h)`.
   Here `Q_m(h)` is the original positive window probability divided by `2h/m^2`; it is eventually bounded for each fixed `h`.

The common-band inequality then follows directly from the first moment of the same Schwartz kernel: `||g-K_B*g||_infinity <= kappa_1 ||g'||_infinity/B`. This is a quantitative bound for an actual signed correction, not a componentwise reconstruction bandwidth depending on unestimated second derivatives. It resolves the noncritical inverse throughout the smoothly protected source. It does not yet estimate the unprotected noncritical inverse.

## 20.4. Combination with the arithmetic correction

A source with small endpoint gradient is completed, within its label-preserving endpoint square, to the unique normal-to-normal minimum. If `delta < d_* epsilon^3`, its roof excess is `O(delta^2)` and the center is `epsilon/2`-protected. The retained positive critical-cluster theorem therefore bounds the whole low-gradient density, including coalescing centers, by `O(delta^2 m^-2)` in collision limsup.

Combining this bound with the derivative estimate gives
`C{[L/delta + M(epsilon^-3/delta+delta^-2)]/B + M delta^2}`.
Choosing `delta=B^-1/4` after fixing `B` gives the stated `B^-1/2` modulus when `B >= C epsilon^-12`. This treats the entire smooth protection, not just its shrinking critical collars.

Theorem `thm:v46-boundary-reduction` writes the exact full-source split and proves an equivalence with the signed correction of the positive collapsing-margin remainder, in the order `m -> infinity` and then `B -> infinity`. The main term is exactly `mathcal L_{m,R}`, with `mathfrak a_R` at a fixed radius. The remaining boundary correction is not declared small. In particular this revision does not mark the complete arithmetic raw LLT or the full signed correction proved.

## 20.5. Weighted class

The new regular theorem states both a supremum and a weak endpoint-gradient budget. Products of uniformly Lipschitz initial and terminal collision-state insertions meet it, since the endpoint state maps have uniformly bounded derivatives in the reduced-action coordinates. The critical part needs only the supremum bound and retains the previous arbitrary-measurable-weight domination. The complementary source has the same total-variation mass bound for arbitrary bounded weights.

These facts do not give an unrestricted path-weighted pointwise theorem. The complete weighted boundary correction and pointwise roof-conditioned bridge remain separate requirements. No unknown path indicator is treated as a differentiable endpoint insertion.

## 20.6. Quantifier order

The finite-time estimate retains `Q_m(h)` and the actual protected critical-cluster budget explicitly. Its constants do not hide a uniform shrinking-window local theorem. The `B^-1/2` rate is a bandwidth modulus **after the collision limsup**, not a polynomial convergence rate in `m`. The result for a prescribed `B_m -> infinity` is proved separately with the protection and gradient thresholds fixed, taking their final small-threshold limit afterwards. It does not evaluate a spectral theorem at a growing band.

The protection `epsilon(B)=A B^-1/12` is likewise fixed in every collision limsup. The count-dependent diagonal has no prescribed rate, and its small complementary mass is never substituted for a density estimate.

## 20.7. Independent specialist audit

No independent human audit has been obtained by writing this revision. The existing contact geometry, occupation-torus spectrum and arithmetic transition theorem remain load-bearing. `SPECIALIST_AUDIT_MAP.md` adds specific checks for arbitrary-endpoint continuation, the Lipschitz guard, flow-box injectivity and coarea Jacobian, the distributional derivative including boundary terms, the near-critical completion and the angular clearance estimate. Finite models, source hashes and successful typesetting are not continuum proof certification.

## 20.8. Conceptual statement

The positive flow-box lemma isolates a local mechanism: an exact label-preserving roof translation with controlled relative source Jacobian transfers a positive window upper bound to density and derivative bounds. It is proved in the article and then verified for the same physical collision words. No broad historical priority claim or application to an unverified second system is added. The pointwise raw-return endpoint remains the original target; the stationary or interval theorem is not substituted for it.

## 20.9. Main route and preservation

The new opening paragraph and Theorem 9 give the direct route: regular endpoint continuation, explicit guard, positive flow comparison, noncritical derivative, critical completion, protected correction, and the exact boundary remainder. All 97 inherited core modules and all 119 inherited Python scripts are byte-identical. All original mathematical labels, the bibliography and the compiled A--X synopsis remain. The new modules are 98 and 99. The former main and principal supporting records are archived verbatim under `provenance/v45-*`. No historical report or unrelated paper is edited.

## Technical comments 1--18

The manuscript keeps `m` for collision count, `n` for return index, `B` for roof bandwidth, and `J_z` for intrinsic jumps. Every limit states which guard or band is fixed. The arithmetic transition and residue factors remain unchanged. Continuous cusp localization, exponential fixed-count height, source mass, density supremum, relative distortion and derivative budgets are kept distinct. The original section factor `c^-1` remains in the endpoint source density and the positive event throughout the flow. The old right-trace convention and all intrinsic coefficients are unchanged; the new estimates use essential suprema, not assigned values at singular points. No finite packet replaces a prescribed singleton. No pointwise roof bridge, arbitrary selected-path Gaussian amplitude, or growing-band spectral theorem is claimed.

## Exact execution evidence

The v45 baseline evidence consists of response run `37770668369` and copy run `37770699128` at the reviewed SHA. The response artifact is `11547711104`, with archive digest `8f4b4acf6c77692d76f28e80a2008a567b99c92ff58a7ff11c88b66d50c57d11`. These are baseline runs only. The v46 dynamic receipts identify their own event SHA, run ID, source payload, PDF and log hashes; no future run is predeclared successful in this response.
