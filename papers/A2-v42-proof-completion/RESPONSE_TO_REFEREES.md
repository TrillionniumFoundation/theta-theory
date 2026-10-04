# Response to the v40 referee report — A2 v41

We thank the referee for the detailed examination of the two-field inverse and for the recommendation of major revision with reconsideration at the requested mathematical-journal benchmark. This revision addresses the stated proof, comparison and presentation requirements within the same theorem package.

## Sources addressed

The controlling report is [REFEREE_REPORT.md](../../reviews/a2-v40-external-harsh-top4-rereview-2026-10-04/REFEREE_REPORT.md), in the completed review commit `24baf07cf2952668d61881c727cc6417e952c76e`. Its directory tree is `75107868144f15707ef63c465ffe14ca25244d4c`, and its report blob is `aab6da8d2ee5964d1baf5527ffc84cf790db1956`.

The reviewed manuscript is [A2 v40](../A2-v40-joint-response/README.md), author commit `c5593b05546889f436ce858c327670d080aae204`, repository tree `1e794c5161114d34a4d46e6e5b5cb50567dfc731`, manuscript tree `3aab67827e78db4063d8a0b6b4f137286af96171`. We also read the report's source audit, literature audit, verification record and independent diagnostic source.

The ordered pair of fixed positive-length commands, the unknown stationary law, the exact and finite theorem classes, the complete translation fiber, response completion and period conclusions are preserved. All 92 v40 proof bodies remain byte-identical in the active article/supplement union. The revision adds 18 complete proofs and 54 labels.

## 11.1. Closest-prior-work comparison

The article now has a dedicated [Related inverse problems](core/28_theorem_comparison.tex) subsection, supported by the expanded [literature audit](LITERATURE_AUDIT.md). The comparison identifies data, hypotheses, competitors, ambiguity and conclusions at theorem level.

The principal additional geometric comparison is the cross covariogram. We cite Bianchi's polygon theorem with its exceptional families and his smooth two-body theorem with its `C^8_+` hypothesis on both factors and competitors. We retain the common-translation and reflected-interchange equivalences and the normalization `v_C = |A|^{-1} g_{C,A}` for a uniform launch law. The noisy-covariogram comparison states the required preliminary symmetric-body estimate as well as the noise conditions. Unknown-probe morphology is compared through its largest-consistent-tip conclusion and its actual contact constraints.

For unknown-noise deconvolution, we state the coordinate-block independence and complex-slice condition in the Gassiat–Le Corff–Lehéricy theorem. The Capitao-Miniconi–Gassiat–Lehéricy geometric criterion explicitly includes strictly convex compact supports. Thus we acknowledge the overlapping product-launch submodel after occupation reduction. The distinction established by the collision theorem is identification for an arbitrary dependent planar launch law using the additional matched collision supports. This is a comparison of information models and hypotheses, not an assertion that joint support/distribution inference is new in itself.

The support-measure discussion attributes signed-difference uniqueness and identifies the extra atomic/nonatomic separation supplied by the obstacle-minus-chord identity. The compact-transform discussion separates multivariable exact uniqueness from the hypotheses of statistical deconvolution with zeros. The inspected versions and theorem numbering, including the accepted CGL manuscript, are recorded. Screened sources whose full texts were unavailable are not used to claim a theorem or priority.

## 11.2. Singular-law support argument

The new [measure-support subsection](core/24_measure_support.tex) contains three self-contained results.

1. `lem:positive-convolution-support` proves the support formula for two nonzero nonnegative compact finite measures. It also proves, by Tonelli, that changing a planar indicator on a null set changes its convolution with an arbitrary finite measure only almost everywhere.
2. `prop:singular-support-components` defines the incoming arcs through continuous interval-section endpoints. It gives the exact physical strip convention `0 < s <= t`, identifies the open strip and its essential closure, and proves the occupation and collision support formulas for arbitrary compact launch laws. It establishes local finiteness, connectedness, the gaps `d - Delta` and `d - t - Delta`, and the observable intersection matching.
3. `cor:singular-support-ae-periods` proves that the finite-prefix operation is well defined on almost-everywhere data, and that almost-everywhere field periods, pointwise periods of the physical means and obstacle periods agree.

The distinction between measure support and pointwise positivity is explicit. Boundary atoms retain the physical bit convention. A purely atomic probability on a dense sequence in any compact convex support illustrates that the statements cover zero-, one- and two-dimensional supports without a density assumption.

These results are placed before the existing collision-support lemma, outside its proof environment. The original proof chain is preserved and now has a complete local support-theoretic account.

## 11.3. Nonsmooth strict convexity and curvature

The new [nonsmooth curvature subsection](core/25_nonsmooth_curvature.tex) precedes the existing calibration lemma.

`lem:nonsmooth-arc-support` proves the closed-hemisphere support identities from convex and concave interval-section functions. It uses no boundary normal parametrization or differentiability assumption, and it includes corners and the transverse directions.

`lem:nonsmooth-surface-atoms` defines `S_K = h_K'' + h_K` as a distribution, proves positivity, and derives the one-sided derivative identities directly from support maxima. Their jump equals the length of the exposed face. Consequently strict convexity is exactly the absence of surface-area atoms. The proof explains both corners, where the contact point can remain fixed through an angular interval, and the possible singular continuous part of the measure.

`lem:nonsmooth-jordan-chord` computes the segment's two atoms with their exact mass, proves mutual singularity with the obstacle measure, and recovers the centered chord and translated obstacle support. The sign convention is determined by positive transverse width; the contact chord need not be perpendicular to the commanded direction.

Classical support and signed-measure identities are attributed. The observable cancellation remains the geometric input specific to the collision experiment.

## 11.4. Exact uniqueness and finite stability

The abstract and introduction now state the distinction at the point where the principal conclusions are announced. Exact identification uses the density of the nonzero real frequencies of a compact factor, continuity and Fourier uniqueness. No lower bound near its zeros is assumed in that exact argument.

Finite recovery instead estimates supports and a finite array of occupation moments. The new [moment appendix](core/27_moment_factor_details.tex) makes the amplification explicit:

\[
\Lambda_m=C_*m^2 24^{4m}(4m)!\le(Cm)^{4m+2}.
\]

For the fitted law it proves

\[
W_1(\widehat\mu_0,\mu_0)
\le R\{C/m+\Lambda_m(2e_y+e_f+4m\sqrt2h)\}.
\]

Here `e_f` controls the actual polygon-factor probability in variation, `e_y` controls normalized occupation moments, and `h` is the padded normalized grid mesh. The explicit error allocation yields the existing exponential sufficient attempted-bit bound. The finite prediction conclusions retain their declared local spatial `L^1` norm, and their stronger BV-density conclusion retains its additional hypothesis. No finite extrapolation theorem through Fourier zeros is used.

## 11.5. Primary article and supplement

We have chosen one article with a technical supplement. The primary contains the complete exact proof chain, the finite main theorems, and two appendices with the detailed finite arguments. Its [supplement interface](core/29_supplement_interface.tex) gives a concise dependency table followed by the input and output of every cited auxiliary estimate: cap mass, coarse complete components, fixed-accuracy normals, relaxed bisection, radial interpolation, signed smoothing, and period locking with common-translation invariance.

The interface explicitly supplies the geometric hypotheses used by these estimates and explains how the present two-command observations satisfy their premises. The angular and randomized preparation models of other supplement theorems are not imported into this experiment. A reader can follow the main theorem without reconstructing manuscript history.

The supplement retains all earlier theorem statements and proof bodies, with their original assumptions and order. Its opening guide points to the primary interface. The PDFs are independently compiled, have stable theorem labels and reciprocal hyperlinks, and are delivered as a single matched package. Source-history and preservation information is maintained in the repository documents.

## 11.6. Resources and finite output

The main finite geometry theorem now explicitly separates attempted bits and command description from deterministic support fitting, numerical integration, apparatus calibration, physical travel, positioning, grid realization, arithmetic and storage.

The finite law theorem gives the candidate grid size and the compressed positive output next to its observation bound. `cor:moment-positive-compression` proves a useful strengthening: at most

\[
\binom{4m+2}{2}=8m^2+6m+1
\]

nonzero rational weights suffice. Rational linear-dependence elimination preserves mass, all fitted convolution moments and the linear-program objective. Reapplying the same moment estimate gives the transportation bound; a separate transportation estimate for the compression map is unnecessary. No additional observations are used. The representation length of the output weights and the linear-program arithmetic remain separate resources.

The bit counts include solid starts, free misses, all repetitions and both fixed-command channels. The commanded length and directions do not vary with accuracy.

## 11.7. Specialist proof review

The five mathematical areas named by the referee now have complete, individually labeled arguments and explicit audit entry points. We have carried out parallel AI-assisted internal mathematical reviews of those arguments and added targeted finite checks. Their scope is recorded in [INDEPENDENT_SOURCE_AUDIT.md](INDEPENDENT_SOURCE_AUDIT.md).

A human specialist's independent review is not something an AI-assisted author revision can attest. No human report is claimed. The requested next review is made concrete by [SPECIALIST_REVIEW_BRIEF.md](SPECIALIST_REVIEW_BRIEF.md), which gives the hypotheses, conclusion and exact proof location for each of the five areas and asks the reviewer to record a signed assessment against the frozen author commit. No person has been contacted through this workflow.

This external-review requirement remains for the subsequent referee process. The mathematical and presentation changes requested of the revision have been made in the manuscript, with their full source and proof bodies available for that review.

## Additional finite details and verification

The new geometric appendix proves the fixed tangential collar, the uniform grazing-strip bound, cap probabilities after conditioning on the hidden displacement, finite-grid boundary-cell control, numerical assignment with explicit margins, the complete-component cutoff, and an exact invertible moment matrix for the signed plateau. These details leave the fixed two-command geometry rate unchanged.

The moment appendix gives a rational cutoff valid pointwise even for boundary atoms, exact moments of a positive rational polygon factor, uniform quadrature conditional on each hidden displacement, the positive programme and its feasible comparison law, sparse compression and the complete cost allocation. It avoids treating unrelated numerical moment approximations as an automatically consistent probability factor.

The final qualification compares the whole v40 active article/supplement union against v41, checks the eleven historical tree pins, executes mathematical and contract diagnostics in ordinary and optimized Python modes, and compiles both documents to stable cross references. Its exact source commit and PDF hashes are recorded in the receipt and uploaded artifact. These checks establish reproducibility and source identity; the mathematical proofs remain in the article and supplement.
