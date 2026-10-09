# Response to the v54 external report: A2-DYN revision 55

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v54-external-top4-review-2026-10-09/REFEREE_REPORT.md`.  
**Frozen report commit / blob:** `7d4e3f6cafebf96da91d2d3a81147841418d9e61` / `a5fc63527861cda25889357bbdd395b2c1efa57e`.  
**Reviewed author commit:** `63135318e1eadd80341d4d0656a17e8caba60c90`.  
**Frozen complete v54 paper tree:** `f5374f17d39e11b8ee489a2ced0818aad12d5a10`.  
**Active article:** `papers/A2-DYN-v55-referee-response/main.tex`.

We thank the referee for separating the positive-height obstruction from the finite-norm results. The title, mechanical family, actual return record, exact labels and pointwise arithmetic target are unchanged. Revision 55 supplies a new finite-count boundary estimate, an explicit weak endpoint and endpoint-modular laws. It does not repeat a cap-dependent integrability argument with renamed constants.

## 1. Positive incidence height

The full essential-height estimate is not established in this revision. The new theorem does prove, for the complete positive first-incidence source and at **every finite count**, the local mass bound `C(1+h) epsilon^(1/16)` with no additive spectral error. It also proves the finite-count estimate

`integral |m^2 b_inc|^q <= C_q(1+h) epsilon^(9(145/144-q))`, for `1<q<145/144`.

This follows from the original positive source rather than from a source selected after fixing a roof value. Bounded insertions are handled by Radon--Nikodym domination. The theorem retains the distinction between these estimates and essential supremum.

## 2. Positive clearance height

The same finite-count estimates hold separately for the first-clearance source and for the sum of the two physical sources. Clearance is still observed at the next collision. No trajectory is continued through a competing-hit seam. The exact global source mass used in the new proof comes from invariant one-flight neighborhoods and their graded depth sum; it is not a coarea argument at a seam. Full clearance essential-height smallness remains a separate proof obligation.

## 3. The two-sided arithmetic raw theorem

The organizing pointwise theorem and its two positive-height requirements are retained without weakening or unmodulated substitution. The substantive advance is that the interval of proved finite powers is now the **explicit range `1<q<145/144`**, together with a weak `L^(145/144)` bound and logarithmically weakened endpoint convergence. It no longer depends on `kappa/Gamma`, and the complete exponential height cap is removed from this proof route.

The two-regime mechanism is elementary but changes the available theorem. Revision 54 has simultaneously

`U_m(epsilon) <= C(epsilon^(1/16)+exp(-kappa*m))`.

The exact global geometry gives for the **same** normalized source

`U_m(epsilon) <= C m^2 epsilon`.

For `kappa*m >= (1/16)log(1/epsilon)` use the first estimate. Otherwise use the second and the bound `log(1/epsilon)^2 epsilon <= C epsilon^(1/16)`. The error-free bound holds at every finite count and scale. Combined with protected height `C epsilon^(-9)`, it gives density-weighted tail `C L^(-1/144)` with no remaining error to integrate and no complete-source cap. All layers, labels and normalizations are those already specified in the article.

Modules `117_cap_free_boundary_layers.tex` and `118_endpoint_raw_laws.tex` contain full proofs. The original essential-height criterion is not claimed as a consequence of a weak endpoint.

## 4. Uniform same-roof bridges

The new local power and endpoint-modular laws also hold for the common path-measure error in the bounded-Lipschitz dual norm, and for the actual-return path on the inherited central target class. They strengthen the roof norm of the existing common-numerator theorem. The path error is dominated by `P+abs(G)`; it is not separately regularized for each test. The established finite-order Wasserstein-in-mean conclusions remain. Uniform convergence at every positive-reference roof still requires the original scalar height condition.

## 5. Arithmetic presentation

The arithmetic transition kernel is now stated expressly as a permanent part of the leading result and direct proof route. Uniform statements use `mathcal L_{m,R}`; the fixed-radius specialization retains `c mathfrak a_R g_{Omega_R}`. No phase-mass equality or zero-residue condition is assumed. Signed `G` is used in unnormalized raw estimates. Forward likelihood and its convex modular use `G >= d > 0` pointwise on the window, not merely a positive integral.

## 6. Independent specialist review

No independent human audit is represented as obtained. The exact-source workflow, finite rational tests and PDF inspection are reproducibility evidence only. The new proof isolates three inherited continuum inputs: the one-flight global strip masses, the finite-band marked local estimate and the polynomial protected-height inequality. The extensive specialist map remains, with these dependencies added. This revision does not treat a successful compilation as evidence for the singular-geometry or anisotropic-space arguments.

## 7. Reusable theorem

Theorem `thm:v55-endpoint-principle` separates the positive decomposition, a polynomial protected-height loss, finite-count local thin mass and an exact polynomial-in-count global thin mass with a strictly larger width exponent. It proves a cap-free weak endpoint `1+alpha/K`. The theorem is stated on an arbitrary finite measure space and is proved without a dynamical hypothesis. The billiard verification is fully supplied, with `(alpha,beta,K,r)=(1/16,1,9,2)`.

We do not claim that this measure-theoretic principle supplies a second independently verified singular-hyperbolic system, or that generality of its statement alone meets a venue's significance threshold. It is a reusable strengthening of the actual density theorem, not a replacement topic.

## 8. Shortest current route and preservation

The introduction gives the three-input proof route directly and names its exact source lemmas. The full exponential finite-count height bound remains part of the historical body but is not required for the new integrability proof. All 116 inherited core files, all 151 inherited Python files, the bibliography, compiled appendices and all 1549 inherited labels are preserved. The former main source and controlling status documents are archived under `provenance/v54-*`. Only the front matter, current proof/status maps and new modules/scripts are revised. No previous manuscript or review branch is overwritten.

## 9. Novelty comparison

The new theorem is not obtained by differentiating a billiard or suspension interval local limit. Its additional inputs are the simultaneous positive-layer estimates and finite protected density height. The reference to Baladi--Demers--Liverani is not used as an occupation-torus pointwise inversion theorem; their flow result is not substituted for the unresolved singular source estimate. The existing theorem-level comparison with Lorentz-process, endpoint mixing-local-limit and suspension frameworks is retained. No historical priority or top-four acceptance is asserted by the source metadata.

## Technical comments and verification

The auxiliary band is fixed once; the reconstruction band, protection width, density level and collision count remain distinct. The new mass bounds are finite inequalities, not separate fixed-scale limsups. Every factor `1/c`, the next-collision clearance convention and half-open occupation interval are retained. The inverse short-window length remains in the inherited protected-height proof. The exact exponent `(1/16)/9=1/144` is displayed, but the former rate-ratio restriction has a new proof removing it rather than being silently dropped. Weak endpoint, strong subcritical, endpoint modular, roof mean, path-dual and essential-supremum statements remain distinguished.

The convex endpoint modular is defined by a positive second derivative, so its likelihood conclusion is a genuine nonnegative convex f-divergence, not an unverified expression called a divergence. Both source components have finite-count estimates with arbitrary bounded insertions; arbitrary path-selector Gaussian amplitudes are still not inferred. All tests share the inherited common roof versions.

The new branches start at the frozen v54 review commit. The final workflow validates the actual report blob, complete v54 baseline tree, new ordinary-source identity, inherited bytes and labels, normal/optimized finite checks, stabilized native compilation and theorem-label renders at the exact event SHA. Results are reported only from the actual execution. A local missing-report preflight, if used during preparation, cannot qualify a GitHub Actions build.
