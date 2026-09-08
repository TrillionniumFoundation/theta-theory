# Response to the independent A2 two-collision report

**Revised submission:** *Uniform collision-threshold laws and marked response in a periodic Lorentz gas*, with the complete reviewed *Two-collision counting response* article as its unchanged companion.  
**Author:** Qian Qi.  
**Controlling review commit:** `50e2bd898e3168d43f1519729a0d88ccbc03946a`.  
**Reviewed manuscript commit:** `e8d3b658ead4996dabfc9f31a07b812e070f5446`.  
**New branch:** `revision/a2-uniform-collision-thresholds-2026-09-09`.

The report found no fatal error in the printed fixed-window theorem, but required additional mathematics beyond its one-roof positive-part integral. We follow the structural-threshold route discussed in the report. The revision adds a theorem for every collision order, including true multi-roof dependence, uniform relative errors, marked records and summable response. The original radius interval, window, theorem statements, proofs and all-order regular-level calculation remain available without deletion or alteration.

This response does not describe the new theorem as journal-accepted or as a proof of the entire historical A2 long-time programme. Its mathematical claims and the older conditional claims are separated by the new source-pinned submission index.

## TC-R1 — A structural result beyond the regular one-roof window

**Locations:** Theorems 1.1 and 1.2; Sections 3--5; Corollary 7.1.

For any compact radius interval K contained in (0, 1/2), put g_R=1−2R and chi_R=arcosh((1−R)/R). The new law is

\[
\Pr_R(N_{jg_R+\varepsilon}=j+1)
=\frac{3\lambda_R}{2R\sinh(j\chi_R)}\,
 \varepsilon^2[1+\varepsilon h_j(R,\varepsilon)],\qquad j\ge1.
\]

The same positive threshold width works for every j. The relative remainder and every fixed mixed derivative of h_j are bounded uniformly in j. The probability is zero on the other side of each onset. Thus the theorem determines an infinite hierarchy of threshold singularities, not further derivatives on the old safely regular window. The parameter range includes the entire original radius interval and also compact intervals with infinite horizon; only the positive inter-obstacle gap is used.

The case j=1 agrees with the onset coefficient derived in the referee report. That coefficient is not claimed as newly discovered here. For j≥2, the law uses the actual iterates S_j tau_R. Its uniform proof is not obtained by substituting j into the original one-roof calculation.

The main steps are explicit. Small total excess forces the complete event into six alternating nearest-neighbor itineraries, independently of j. Their stationary broken-length action is solved as an endpoint boundary-value problem. The inverse Dirichlet Jacobi matrix has an explicit exponentially decaying Green kernel; a weighted contraction gives a common analytic neighborhood and endpoint-localized errors. The effective endpoint Hessian is uniformly nondegenerate. Its mixed derivative, however, is exponentially small. Lemma 4.3 proves a relative determinant estimate by an exact corner cofactor and a trace-norm perturbation bound. The trace bound sums the endpoint-localized errors rather than multiplying an absolute error by j. Uniform Morse integration then gives the whole threshold law.

Corollary 7.1 compares with an independent-roof suspension having exactly the same section marginal and intensity. Its onset power is j+1; the specular billiard's power is two at every j. For three collisions, in particular, the true probability is quadratic while the independent surrogate is cubic. This is a concrete mechanical consequence of correlations that the old two-event law could not detect.

## TC-R2 — Multi-impact records, sources and summability

**Locations:** Proposition 2.1; Theorem 1.2 and its proof; Theorem 6.1; Section 5.1.

Proposition 2.1 retains the first-impact residual time r. Its integration domain is determined by r+S_j tau_R<T; the full equilibrium normalization is lambda_R. It does not use invariance to move a marked integrand without also moving its mark. The initial and terminal free-flight pieces, both velocity traces, impact positions and all collision times are reconstructed from the actual specular segment.

For a smooth impact mark f_R, Theorem 1.2 proves the source-dependent expansion with axial weights exp(q w_{j,e}). Deviations of the sum of marks from its axial value have uniform derivatives because the bridge decays from both endpoints and its weights sum uniformly. On a compact source interval satisfying q_0 F_*<min_K chi_R, every prescribed radius/source/threshold derivative of Z_j/epsilon^2 is bounded by a polynomial in j times exp[−(chi_*−q_0 F_*)j]. Its series is consequently uniformly summable, with termwise differentiation. This is an actual proved estimate for the mechanical family, not an assumed Fourier envelope.

Theorem 6.1 identifies the entire onset record in a common scaled domain. Its conditional density differs by O(epsilon) in total variation from the normalized paraboloid measure. It gives all scaled collision times and transverse positions with errors uniform in the impact index and itinerary length. Samples near kg_R are cut by eta+sum_{h<k}Q_h(z)=kappa. The eta derivative is one, so a strip estimate controls crossings rather than deleting their contribution. The leading velocities and both end pieces are explicitly supplied. For source-weighted conditional laws the general total-variation error is O(sqrt(epsilon)); it is not incorrectly promoted to the stronger cancellation available for integrated source normalizers.

Section 5.1 gives the second-derivative jump across each onset and its distributional higher-order interpretation. Thus the singularity at the onset is included. The geometry proves that grazing trajectories do not belong to the sufficiently small complete onset event; it does not impose a cutoff on a selected initial ensemble.

These are uniform and summable results for the extremal threshold hierarchy. They do not assert corresponding estimates on every itinerary at every time. That distinction is essential: windows grow like jg_R but the selected count is the maximal possible one, not a typical long-time fluctuation.

## TC-R3 — Relation to the historical A2 root theorem

**Locations:** Section 8.3; `SUBMISSION_INDEX.md`; preserved Round 33 source.

The new submission now contains a model-level theorem involving arbitrarily many genuine reflections and source derivatives with a summability bound. It is therefore more than the one-roof marginal input available to the reviewed note. Its coefficient hierarchy also determines the normal period-two multiplier, proved from the physical Jacobi recurrence, and admits the explicit coefficient-generating identity in Corollary 7.2.

We do not identify this threshold series with the characteristic function of one unrestricted long record. The original mixed local Edgeworth goal still requires a specified periodic-data realization, source-dependent stable-curve operators, high-frequency bounds for the correct matrix coefficients, and a source-differentiated integrable central remainder. Those conclusions are not proved in this revision and are not reported as closed. The old Round 33 chapter remains a conditional arithmetic/inversion component; no theorem from statistical A1 is used to bridge the missing mechanical implications.

The report expressly allowed a substantial structural classification of mechanical thresholds as an alternative publication route. This revision develops that route while preserving the older programme intact. The new submission index prevents the new uniform extremal theorem, the retained regular-window theorem and the older conditional compiler from being counted as the same result.

## TC-R4 — Precise comparison and the contribution claimed

**Location:** Section 8 and the completed main bibliography.

The stationary/Palm mechanism is attributed to its classical setting, with Marklof as the direct comparator. The length-generating function and action-Hessian relation are also classical; the comparison with Bolotin--Treschev explains the finite Dirichlet cofactor's role without claiming a new general Hill formula. The contribution claimed here is the complete-event localization, collision-order-uniform boundary-value calculus and relative flux estimate, followed by its full-preparation threshold and marked-record consequences.

The comparison with Balint--De Simoi--Kaloshin--Leguil distinguishes their marked periodic-length data and inverse geometry from our equilibrium count-tail coefficients. Recovering the normal multiplier here is a statement about a different statistical observable, not stronger general inverse rigidity. Demers--Zhang's perturbative spectral theory and Demers--Melbourne--Nicol's typical-orbit limit laws are compared in terms of their observables and operator/singularity scope. They are neither dismissed nor invoked as automatic all-order extensions.

The current comparison is targeted, not an exhaustive priority certification. Whether the new structural result has the breadth and significance required by a particular journal remains for an independent referee and editor to assess. A larger numerical check count is not offered as the originality argument.

## Smaller presentation requests and preservation

Section 7.3 supplies the explicit terminal-level witness for the old fixed window, checks its incoming sign and non-obstruction, and concludes that the level contribution is strictly positive. Complete bibliographic volume, page and DOI data appear in the new main reference list. Every fixed derivative order remains distinct from a uniform-in-order assertion.

The companion has exactly the reviewed source blob `df44402b17031525c087d39dfedf8dac3ada611d`: 20,663 bytes, all five theorem-like environments and all four explicit proof environments preserved, together with proofs written outside those environments. Its entire text, not a theorem-only extract, is compiled. The repository publication is an addition-only directory based on the latest review tree. Original papers, all historical reports, A1 and B2 sources and their branches are untouched.

## Executed checks and present verification limits

The current native build produces a 14-page main article and the complete 7-page companion. Six compiler invocations succeed, actual auxiliary files stabilize, final references/citations are resolved, and no overfull boxes remain. The TeX recorder agrees with the declared 12-file native input closure. The receipt records every current input's Git object and SHA-256, compiler and PDF hashes. Its source-commit field is null because the content-addressed build precedes the publication commit.

The new script passes 411 explicit checks: 141 exact rational identities and 270 non-interval floating checks. Normal and optimized executions are byte-identical. The tests include exact Schur complements and Hessian determinants; terminal witnesses; physical reflection, positive energy and relative-twist stress tests up to j=128; and independently evaluated endpoint integrals for j=1,2,3,8. The measured integral-to-leading ratios approach one at the predicted relative order. These diagnostics are not a directed interval proof or a continuum check. The current revision does not claim replay of the referee's separate 31-case program or a full billiard-flow simulation.

The page-inspection record distinguishes contact-sheet inspection of the whole new article from selected full-page inspection. No formal proof assistant, exhaustive original-program closure, remote CI result or journal acceptance is claimed. The manuscript, proofs and source-pinned evidence are submitted for a new independent review.
