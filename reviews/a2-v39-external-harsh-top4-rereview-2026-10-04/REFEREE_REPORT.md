# External top-four referee report on A2 v39

**Manuscript:** Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
**Reviewed revision:** `revision/a2-v39-response-rigidity-2026-10-04`  
**Equivalent alias:** `revision/a2-v39-referee-copy-2026-10-04`  
**Reviewed commit:** `f815a7acdb5c03e03b9996fc7052b405db66936d`  
**Repository tree:** `3d26fc322785102d5eda2964bdfd94fdaacf0fc7`  
**Active core tree:** `113a60e9545374aee5ae6fd80b14f4fedf8e8ed6`  
**Controlling report:** `5dd7a7e346a9d31d7541efe791335d4e965cadb0`  
**Date:** 4 October 2026  
**Benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision or formal proof certificate.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

Version 39 is a substantial and intellectually cleaner revision. Its principal theorem no longer depends on a second homothetic setting or on a separately prescribed reciprocal preparation. It uses one unknown stationary launch law and raw forward collision bits. From the complete direction-resolved first-order short-flight germ, the paper reconstructs the centered launch footprint, the entire launch density up to almost-everywhere equality, and an arbitrary locally finite separated configuration of smooth strictly convex obstacles. It classifies the complete common-translation fiber, identifies the obstacle period group, and determines every finite-length forward response. A second exact theorem replaces the uniform obstacle-width condition by the existence of one obstacle whose diameter exceeds the footprint diameter. A separate finite theorem regularizes the germ and gives an explicit forward-only geometric experiment.

On the new core audited in detail, I found no fatal counterexample. The short-flight strip limit, angular distribution identity, separation and normalization of translated density copies, recovery of boundary contacts from component Steiner points, common-translation fiber, odd-germ occupation-gradient identity, minimum-area pure-copy argument, positive regularization, and displayed resource exponents are mutually coherent under the stated hypotheses.

The negative recommendation is editorial and conceptual. The exact datum remains extremely rich: raw forward means are supplied at every nominal center, in every commanded direction, and through arbitrarily short positive lengths. Applying a classical angular differential operator to this continuum active field exposes spatially separated copies of the unknown density. Once the copies are separated, their supports, masses, and centers make the blind factorization nearly explicit. This is an elegant collision-specific inverse, but the information model is much closer to a complete active boundary-response field than to a standard passive billiard invariant.

The finite theorem has strong compact-class priors, extremely fine commanded scales, and a large nonsharp sufficient exponent. It reconstructs geometry but does not give finite strong-norm recovery of an unrestricted unknown density. Uniform finite period decisions retain a bounded periodic presentation and a positive nonperiod-patch margin; the nonperiodic corollary instead assumes a protected aperture containing the complete finite configuration.

In my judgment v39 is a serious and potentially strong specialist- or broad-field-journal paper after fresh human proof review and substantial editorial compression. It is the strongest A2 revision so far. It nevertheless remains below the exceptional naturality, breadth, and field-transforming threshold of the four journals named above. I would not recommend another open-ended revision cycle at that benchmark.

## 2. Source and chronology

Both v39 revision names resolve to the same author commit and tree listed above. The author commit is based directly on the completed v38 external-review commit `5dd7a7e...`, which reviewed author source `a346669...`. The v39 source pins preserve the reviewed v38 paper tree `36a5f28721e4aa336dba7a2eb0d07132589cd301` and the controlling review tree `91797dde92b95cbaa36d3ef5f543fee025268855`.

No later A2 revision branch existed when this report was frozen. The review branch starts directly from the v39 author head and adds files only under `reviews/a2-v39-external-harsh-top4-rereview-2026-10-04/`. No manuscript source, workflow, prior report, retained paper, or unrelated path is modified.

The genuinely new mathematical inputs are principally:

- `core/00h_single_law_overview.tex`;
- `core/19_single_law_rigidity.tex`;
- `core/19a_one_resolved_component.tex`;
- `core/20_single_law_finite.tex`.

The v38 theorem package remains active in appendices.

## 3. Observation model

For nominal center `x`, direction `n_theta`, and length `t>0`, a hidden start is `x+Z`, where `Z` has one unknown stationary density `j` supported on an unknown convex body `A`. The only output is the original first-collision bit. Solid starts and free misses both return zero and remain in the denominator.

The exact datum is

\[
F_{t,\theta}(x)=\int_A j(z)B_{t n_\theta}(x+z)\,dz
\]

for every center, every direction, and arbitrarily short positive lengths. The germ

\[
q_\theta=\lim_{t\downarrow0}t^{-1}F_{t,\theta}
\]

is taken in local `L^1`. This is a direction-labelled active whole-field datum, not a pooled scalar field, finite-dimensional record, or passive trajectory invariant.

## 4. Short-flight boundary germ

For one convex obstacle and fixed direction, free starts whose short segment first enters the obstacle form a strip of width `t` attached to the incoming boundary. Since `t` is smaller than the inter-obstacle separation, a segment cannot meet two different obstacles.

Strip disintegration and translation continuity of an arbitrary `L^1` density give

\[
q_\theta(x)=\sum_C\int_{\partial C}
 j(y-x)(-n_C(y)\cdot n_\theta)_+\,ds(y).
\]

In Gauss coordinates,

\[
q_\theta(x)=\sum_C\int_0^{2\pi}r_C(\phi)j(c_C(\phi)-x)
(-\cos(\theta-\phi))_+\,d\phi.
\]

The weak finite-length estimate is correctly normalized: averaging the strip depth over `[0,t]` produces the coefficient `t/2`. I found no missing factor, sign error, or pointwise use of the unknown density.

## 5. Angular resolution and density-copy recovery

For `k(alpha)=(-cos alpha)_+`, the periodic distribution identity is

\[
k''+k=\delta_{\pi/2}+\delta_{-\pi/2}.
\]

Therefore

\[
S_\theta=(\partial_\theta^2+1)q_\theta
 =\sum_{C,\sigma=\pm1}r_C(\theta+\sigma\pi/2)
 j(c_C(\theta+\sigma\pi/2)-\,\cdot\,).
\]

The proof works with supports of positive measures and `L^1` angular slices, so it does not depend on a representative of `j` that may vanish on a dense null set.

Under

\[
\operatorname{diam}A<\min\{d,w_*\},
\]

the support components are precisely `K=c-A`. On such a component the field is `r j(c-x)`, its mass is `r`, and its Steiner point is `c-s(A)`. Hence

\[
A_0=-(K-s(K)),\qquad
j_0(z)=\frac{S_{\theta,K}(s(K)-z)}{\int_KS_\theta}.
\]

This removes the curvature weight and recovers the complete centered density. As the direction varies, the component centers traverse all obstacle boundaries in the same centered frame; connected components and convex hulls recover the bodies. The argument is clean in its stated separated-copy regime.

## 6. Fiber, completion, and periods

The germ determines the canonical triple

\[
(\mathcal O-s(A),\ A-s(A),\ j(\cdot+s(A))).
\]

Thus equality of germs is equivalent to a common translation of the table and launch law. The converse follows by coupling all starts and segments under that common translation. Since the exact triple is recovered, every finite-length raw forward response is determined.

A period of the germ preserves each angular measure support, permutes its connected components, and hence preserves the recovered boundary union. Conversely every obstacle period preserves every response. The germ period group therefore equals the obstacle period group and is discrete. This is an exact whole-field result, not a finite periodicity test.

## 7. One-resolved-obstacle extension

Theorem 2.6 assumes only `diam A<d` and the existence of one obstacle with diameter larger than `diam A`. Different obstacles' angular support pairs remain separated, while the two antipodal copies of a small obstacle may overlap.

A connected component containing two distinct translates of `-A` has strictly larger area than one copy. A diameter pair of the resolved obstacle supplies an angular slice with two separated pure copies. Hence the global minimum component area equals `area(A)` and a minimizer identifies the density and footprint.

The odd germ satisfies, distributionally,

\[
q_\theta-q_{\theta+\pi}=\partial_{n_\theta}v,
\]

where `v` is the occupation. Translation continuity of `j` gives bounded continuity of `v`; separated expanded components imply `inf v=0`. The two coordinate derivatives and this normalization determine `v`, whose positive components are `C+(-A)`. Support cancellation recovers every obstacle.

I found the chain coherent. The minimum-area argument, distributional potential normalization, and passage to arbitrary locally finite configurations deserve independent human review because they carry most of the extension's load.

## 8. Finite forward-only reconstruction

The finite theorem intentionally uses stronger hypotheses: uniform angular-copy separation, `C^{6,beta}` obstacle and footprint bounds, positive curvature margins, a lower density boundary-mass condition, and a protected aperture.

A positive spatial/angular regularization is defined by convolving the positive angular measure. Integration by parts moves the angular derivatives onto known kernels. Replacing the germ by a finite command length, spatial quadrature, angular quadrature, and rational vector rounding yields deterministic bias

\[
C\left(tr^{-3}b^{-2}+\frac{\ell r^{-2}b^{-2}}t
+d_\theta r^{-2}b^{-3}+\frac{\zeta r^{-2}b^{-2}}t\right).
\]

Importance sampling over rational command menus gives a signed bounded estimator with variance at most `C t^{-1}r^{-2}b^{-4}`, without a density upper bound or continuity modulus.

With geometric support error `e`, the choices

\[
r,b\asymp e,\quad t\asymp e^{\gamma+5},\quad
\ell,\zeta\asymp e^{2\gamma+9},\quad d_\theta\asymp e^{\gamma+5}
\]

make every deterministic bias `O(e^gamma)`. Per-target cost is `O(e^{-(3 gamma+11)})`; the spatial and angular target count is `O(e^{-5/2})`. With `e\asymp\nu^{s/(s-2)}`, the sufficient exponent is

\[
Q_\gamma=\frac{(3\gamma+27/2)s}{s-2}.
\]

Thresholding the positive field recovers complete footprint copies, their Steiner points recover boundary contacts, an angular mesh of order `sqrt(e)` gives `O(e)` support error, and high-order support smoothing converts this to `C^2` error `O(nu)`. I found no exponent or sign contradiction.

The finite proof is long and delicate, especially the uniform quadrature, complete-copy discard rule, and final support smoothing. It reconstructs geometry, not the unknown density in a strong norm. Its exponent is nonsharp; for `gamma=0` and `s=7` it is `18.9`. Physical manufacture, movement, metrology, and realization of the very fine command scales are separate from attempted-bit and digital-description counts.

## 9. Retained known-disk minimax benchmark

The retained v38 theorem identifies the polynomial minimax power

\[
q_0=\frac{3s/2+1}{s-2}
\]

for a fixed known uniform-disk law, fixed positive spread, specified bounded smooth class, centered `C^2` loss, fixed confidence, and worst-case expected attempts, up to one logarithmic factor. This is a different experiment and is not a minimax theorem for simultaneous unknown-density and unknown-footprint recovery. The manuscript now states this distinction correctly.

## 10. Required qualifications

Any journal version should make the following visually unavoidable.

1. The exact input is a full continuum active germ: all centers, all directions, and `t` tending to zero.
2. Exact identification and finite acquisition are distinct. The exact density recovery has no finite strong-norm statistical analogue here.
3. The direct theorem, one-resolved-obstacle extension, and finite theorem use different hypotheses.
4. Exact response completion is not a finite-cost extrapolation theorem.
5. Exact period recovery needs no periodicity prior; uniform finite primitive-lattice decisions still use a positive patch margin, while the finite-cloud theorem assumes a complete aperture.
6. Distinct spatial sites, command occurrences, attempted bits, controller-description length, and physical control costs must remain separate.
7. The 85-page primary retains 76 proof environments and several older self-contained programmes. The new single-law theorem can support a focused paper; substantial splitting or compression is warranted.

## 11. Literature and top-four significance

The planar angular inversion is classical. Directional covariogram derivatives and first variations of dilations are established ways to extract boundary variation, and blind unknown-probe reconstruction has a substantial morphological literature. The genuine v39 contribution is the collision-specific joint identification: angular filtering exposes positive spatial copies of one unknown density; separation, mass normalization, and translation centers recover both the law and obstacle contacts; the odd germ extends recovery when only one obstacle resolves the density.

This is new and elegant within the stated sensor. At the requested benchmark, however, the strongest data remain a full active continuum field, and the principal separation becomes explicit after applying a classical angular identity. The finite theorem is highly prior-dependent and far from sharp for the joint unknown-law problem. The paper proves neither rigidity from a standard passive dynamical invariant nor finite prior-free reconstruction of arbitrary configurations. These are legitimate scopes, but they govern the editorial decision.

## 12. Reproducibility

The exact-head workflow run `37194180565` completed successfully at the reviewed SHA. Checkout, environment installation, source and diagnostic qualification, complete-primary build, evidence binding, and artifact upload all passed.

Artifact:

- ID: `11300382154`;
- digest: `sha256:6f0d880928ba34e65edcab8b47b27978e62e74650392173da147d970c00dd0b9`.

The receipt records an 85-page primary, 322 active labels, 79 formal result blocks, 76 proof environments, all 265 reviewed v38 labels retained, all 66 reviewed v38 proof bodies byte-identical, 622,976 author finite diagnostics, 66 qualification-contract checks, no final TeX findings, and PDF SHA-256 `5f2bbdee93ddeb7a47604c16c5ea015653fcb3f33328a43e79974bfdc777d60b`.

The independent `verify_review.py` imports no author code. Ordinary and optimized executions are byte-identical at SHA-256 `3b2d108539790bc88541e207655fc6d93d362c870e0f0dc62cef29f8a3ab8de5` and record 162,863 checks of the angular identity, density-copy normalization and translation, minimum-area models, odd-flux signs, weak-error coefficient, signed estimator algebra, and finite resource exponents. These checks are not continuum proof certification or physical-apparatus validation.

## 13. Final verdict

**Response to the v38 report:** substantively successful. The principal inverse now uses one unknown stationary law and forward bits, removes the cross-setting homothety apparatus from the main theorem, classifies the exact translation fiber, and supplies a separate finite geometric experiment.

**Mathematical audit:** no fatal counterexample found in the new v39 core; the one-resolved-obstacle and finite quadrature/support-recovery chains warrant independent human proof review; theorem scopes must remain exact.

**Source delivery:** successful exact-SHA qualification with archived evidence.

**Editorial assessment:** technically serious with a clear central theorem, but the full active continuum datum, strong finite priors, classical transform/variation engines, nonsharp finite rate, and retained accreted architecture leave it below the requested top-four threshold.

**Recommendation: reject at the Annals / Acta / Inventiones / JAMS benchmark.**