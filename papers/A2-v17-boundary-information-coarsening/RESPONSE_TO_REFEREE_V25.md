# Author response to the A2 v24 referee report

**Manuscript:** Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards  
**Author:** Qian Qi  
**Revision:** v25, September 12, 2026  
**Branch:** `revision/a2-v25-observable-calibration-signature-top4-2026-09-12`

## Frozen sources and nature of this response

The report answered here is [the v24 external referee-style report](../../reviews/a2-v24-external-harsh-top4-2026-09-12/REFEREE_REPORT.md), together with its source-notation addendum, at review-branch tip `8129defd970bbc1e011bb480b70603d39a31324d`. Its reviewed manuscript is pinned at `c35b31b1924a1621374eab72ee60e4cb5ab37df5`. The new branch descends from the review tip, so both the reviewed manuscript and the report are retained.

This is a substantive author revision for a further independent reading. It does not represent a journal decision or a formal proof certificate. The main manuscript contains the mathematical arguments; this response and the verification records are separate. The requested native clean build has not been certified merely because a workflow exists: see `VERIFICATION_V25.md` for the execution boundary.

## The results retained

The revision preserves the relative fixed-collar law and its differentiated operator construction, the full signed all-order contact inverse, analytic continuation, intrinsic gluing classification, rank-two lattice recovery without a supplied Gram form, the moving-support local information arguments, the count normal quotient, the stopped physical transfer and the complete auxiliary compendium. Neither odd contact jets nor the global reconstruction conclusion has been removed. The previous source files are retained, including the superseded v24 argument files; `main.tex` now selects their explicit replacements rather than compiling incompatible old and new claims side by side.

The report's favorable assessment of the determinant-one contact blocks, the rank-two lattice formula, the reverse Poisson construction and the intrinsic count quotient is respected. The additional proofs below address the points at which those mechanisms had not yet been joined into an observable global experiment.

## M1. A common observable physical experiment, including contact-frame calibration

**Objection.** A table-dependent transverse origin and tangent cannot be used as an observed statistic. A pilot for the onset alone does not acquire those coordinates, and a same-table total-variation comparison does not construct a parameter-independent centering kernel.

**Revision.** `article/25a_common_observables_v25.tex` starts with actual common standard Borel design and record spaces, equation `eq:v25-design-record-spaces`. A design is the marked channel, endpoint type, even flight number and physical time. A successful record is the first and last two-dimensional collision position in that channel's sensor frame, and the preparation-to-first-impact time; a failed preparation has its own atom. Selection is by a marked timed collision word, not by an unknown tangent or a parameter-dependent spatial gate.

The sensor assumption is explicit. Both endpoint types of one channel are read in the same oriented Euclidean sensor frame and physical length unit. Different channels have no supplied registration. Contact centers, normals, gaps and lattice vectors are not inputs. This is the global **endpoint-position** acquisition. It is not a claim that an unregistered scalar projection, with its construction left unspecified, has suddenly become observable. The inherited anchored scalar laboratory-coordinate experiment remains the setting of the local information theorems. The new introduction and `01a_protocol_scope_v25.tex` distinguish these two experiments, and do not claim that the local Poisson information exhausts the richer two-dimensional sensor record.

`lem:v25-physical-localization` proves that success at excess at most `2h` localizes both endpoints to `C sqrt(h)` of their true contact, uniformly in the even flight number. Every flight is at least the gap; uniform nondegeneracy of the closest-pair minimum and its outside-neighborhood margin turn total small excess into endpoint localization. The relative flux estimates also give the uniform success lower bound `c_* h^2 exp(-j gamma_+)` when the excess is in `[h,2h]`.

`thm:v25-observable-calibration` then supplies a finite capped scan for each channel and each endpoint type. At one grid point the true excess is in `[h,2h]`. An earlier success is also valid because no success occurs before onset. With probability at least `1-beta`, all first successful times lie in `(jg,jg+2h]`. The estimators obey

`max_e j |g_hat_e-g_e| <= h`,

`max_(e,b) |p_hat_(e,b)-p_(e,b)| + max_e |t_hat_e-t_e| <= C sqrt(h)`.

The cap is `2|E|(L+1)N`, with `L` and `N` displayed in the theorem. Every failed preparation is included. The construction does not infer zero probability from finitely many failures. Defaults and failure flags define it measurably on every transcript, and its error bounds are invariant under independent rigid motions of the channel sensor frames.

The subsequent normalization uses **estimated** points and tangents, equation `eq:v25-observable-normalization`. For a fixed finite family of bounded Lipschitz tests, `prop:v25-test-implementation` proves the conditional uniform bias bound

`C_F (sqrt(h) + h + tau^J)`.

The unknown ideal normalization appears only in the proof of that bound. It is not an operation required of the observer. This completes the within-channel calibration step; intrinsic gluing continues to solve the different inter-channel registration problem.

## M2. The onset coordinate is now part of separation and estimation

**Objection.** Equality of centered conditional law families cannot simply be said to recover gaps. The target includes gaps, but the old statistical criterion omitted them.

**Revision.** `lem:v25-augmented-separators` uses the mixed moment map

`F(T) = ((g_e(T)/g_*)_e, (Q^infty_(T,a_r) phi_r)_r)`.

For pairs separated by `eta` in the finite data vector, either a gap coordinate separates the pair, or all gaps agree. In the latter case equality of all conditional laws gives equality of the support thresholds and action germs, contradicting separation of the finite data. Compactness of the separated pair set selects finitely many gap/law coordinates with a common positive margin. The law tests are bounded Lipschitz functions, and their expectations are continuous by the explicitly proved centered-law estimate.

The actual estimator includes `(g_hat_e/g_*)` in `F_hat`. A finite template library has an image forming a `c`-net of `F(K)`. The estimator takes the first minimizing template under a fixed tie rule. If `F_hat` is within `c` of the truth, the selected template is within `3c`, while finite-data separation requires at least `8c`. This is a finite Borel minimum-distance rule, not an unspecified search over a parameter-dependent chart.

`thm:v25-fixed-order-physical` proves the uniform fixed-order risk bound using this mixed criterion. `thm:v25-global-physical-reconstruction` supplies one growing-order sequence recovering the entire marked periodic table, including the lattice, in each fixed labelled `C^q` loss. The quadratic family noted by the referee is included as an illustration of why the gap coordinate must remain. We do not claim that it has identical complete nonlinear laws at different gaps.

## M3. Finite signatures: local uniqueness is proved separately from outside-arc exclusion

**Objection.** A signature gap outside a target arc does not rule out two matches inside that arc. The scalar-curvature minimum example demonstrates the issue.

**Revision.** `article/23e_signature_stability_v25.tex` does not reuse that inference. It first observes that the transition obstacles in an exactly signature-rigid gluing have trivial orientation-preserving symmetry: a nontrivial symmetry of a compact strictly convex body would duplicate every framed complete signature. This is a consequence of the already stated unique-transition hypothesis, not a newly imposed reflection assumption. Obstacles not used for such transitions can retain their symmetries, and the general gluing-space classification is preserved.

`thm:v25-finite-signature-embedding` selects a sufficiently rich finite oriented curvature signature uniformly over the compact class. At every point a nonconstant analytic curvature has a nonzero derivative of some positive order. A finite compact cover selects an order giving a uniform immersion bound. Taylor's formula gives the local chord lower bound. A second finite cover of the pairs outside that short arc uses complete-signature injectivity to select enough additional coordinates for a uniform global separation. The resulting statements are separately printed as `eq:v25-signature-immersion`, `eq:v25-inarc-embedding` and `eq:v25-outarc-separation`.

`lem:v25-noisy-signature-match` addresses an actual noisy matching functional. If the recovered signature curve is close in `C^2` and the target vector is close, outside-arc separation confines its least-squares minimizer. Inside that arc,

`f'' = |J_tilde'|^2 + (J_tilde-y) dot J_tilde'' >= v^2/8`.

Thus the minimizer is unique and its position error is `O(epsilon)`. The gradient equation gives local Lipschitz dependence on the target and the recovered curve in `C^1`. No uniqueness under an arbitrary `C^0` curve perturbation is asserted. The scalar-minimum counterexample is explicitly contrasted with this enriched-signature construction.

The gluing-persistence lemma then propagates recovered point/tangent errors through the finite graph and uses the fixed-matrix formula `L=VM^{-1}` for lattice stability. Finally, the uniform inverse modulus is proved **independently** by exact full-data injectivity and compactness. A compact inverse modulus is not substituted for local matching uniqueness, and a product-metric tail is not misrepresented as an analytic-continuation error rate.

## 6.1. The finite-dimensional variation model is constructed rather than inferred

`article/25c_analytic_variation_bundles_v25.tex` separates the local positive-design assertion from global consistency. On a compact contact stratum, coincident incidences are identified and distinct contact normal angles are uniformly separated. A finite real trigonometric space interpolates support-function jets simultaneously at all contacts. The proof gives explicit interpolation factors and the right inverse

`R_T = E_T^t (E_T E_T^t)^(-1)`.

Zero support value and first-derivative increments preserve contact positions and tangents. The higher support jets and graph jets are related by an invertible triangular differential. The inverse function theorem and the Hermite right inverse produce actual compatible analytic obstacle variations, not mutually inconsistent formal germs.

The resulting finite-rank bundle is specified by its local coordinates and frame-change differentials; its unit sphere bundle over the compact base is genuinely compact. It is a bundle of **ambient analytic variations through the base tables**, not a tangent bundle to an arbitrary closed analytic subset. Uniform finite positive design is proved on this explicit bundle. The gap is fixed in this network bundle; independent gap directions are not assigned where global incidence compatibility could forbid them. The established anchored one-channel local theorem still includes its own gap coordinate.

The global physical theorem does not rely on this auxiliary bundle or the extra contact-stratum separation. It uses the mixed observable finite-separation argument on the original compact analytic class. Finite target truncation is nowhere used to assert finite dimensionality of the whole statistical family.

## 6.2. Pilot order, parity and charged caps

The fixed-order construction chooses the separator list and library, then the success target `k`, then the **final even** flight number `J`, and only then the pilot resolution `h`. The pilot itself uses `j=J`. Its bound therefore controls `J|g_hat-g|`, the quantity entering the actual post-pilot window. `J` is never increased after the pilot has been run.

Both pilot endpoint types and every inference batch are even-flight same-type designs. Every stage can impose an arbitrary prescribed lower bound `J_0`; the global sequence takes `J_0=s`.

The post-pilot batch cap is given explicitly from a uniform positive success lower bound. Concentration is applied to the uncapped iid sequence of successful marks and the cap-exhaustion probability is then added. The proof does not condition on cap completion and incorrectly retain an iid assertion under that conditioning. The full stopped physical comparison retains failures, designs, waiting counts and stopping times.

## 6.3. Continuity and finite measurable tests

Equation `eq:v25-centered-TV-continuity` proves total-variation continuity of the centered conditional law on a fixed box and a strictly positive offset subcollar. The proof bounds the amplitude difference and integrates the fiberwise ceiling symmetric difference, including the change in the normalizer. It does not assert ambient-position total-variation continuity between different boundary curves.

Bounded Lipschitz functions are then selected because they separate probability measures and allow an explicit plug-in coordinate-error estimate. This supplies both the open-separation step and the observable normalization estimate; they are different uses and are both proved.

## Poisson reverse deficiency and the notation addendum

The complete reverse-kernel argument remains active in `18c1_endpoint_time_deficiency_v25.tex`. The intensity token is literally `\rho(u,v)`, not a carriage return followed by bare letters. The source diagnostic checks that token.

The revised section explicitly requires `rho_(n,z)/rho_(n,0)=1+O_K(1/k)` on the common bulk and verifies it for the smooth anchored fixed-window model. Normalizing the bulk preserves the relative bound, yielding one-record squared Hellinger distance `O_K(k^-2)` and product total variation `O_K(k^-1/2)`. Bare `C^0` trace convergence is not used to infer this rate.

The layer estimate now includes both the fixed-face corner and any alternative support just outside the reference endpoint domain. The reverse kernel is defined on every Poisson configuration: invalid nonpositive residual coordinates receive a reference replacement, and excess counts receive a fixed output. These exceptions have the stated negligible probabilities. Thus the density repair does not conceal a missing sampling convention at the corner.

## The short-flight benchmark and theorem-level comparison

`29a_signed_one_flight_benchmark_v25.tex` proves the mixed-type one-flight support inverse directly:

`psi_0(u) = sqrt(ell(u,0)^2-u^2)-g`,

`psi_1(v) = sqrt(ell(0,v)^2-v^2)-g`.

It is presented alongside, not in place of, the inherited two-flight integrated-probability benchmark. We do not claim that unrestricted finite-flight consistency alone makes long bridges necessary. The new physical theorem instead works when **every** used flight number is even and its minimum tends to infinity. The pilot obeys the same restriction. The all-order half-line inverse, uniform relative long-bridge law and record-coarsening information theorems retain their separate content.

The introduction compares the actual data and hypotheses with De Simoi--Kaloshin--Leguil, Finamore--Leguil, Smith and Meister--Reiss. Marked lengths, enriched marked lengths and intrinsic channel-law data are not ordered by an unproved implication. Poissonization and nonregular Gaussian rates are not claimed as new statistical principles in themselves. The comparison identifies the billiard-specific geometric inverse, observation restrictions and physical acquisition bounds.

## Native build, navigation and remaining verification boundary

`main.tex` activates all revised proofs and the complete auxiliary compendium. Root and manuscript navigation point to v25 rather than the stale v20 index. `ACTIVE_SOURCE_MANIFEST_V25.md` records the active replacements and retained inputs. `check_revision_v25.py` provides finite diagnostics, native source-reference checks, preservation comparisons and the exact density-token check.

The 337 finite mathematical diagnostics were executed locally in both normal and optimized Python with identical output, and the locally executed script's Git blob hash was checked against the committed script. This is not a native whole-paper build or a proof-assistant certificate.

The first exact-head hosted native-build attempt, run `34661518521`, failed before any job step was executed; the job had no assigned runner and no downloadable log. The workflow was then routed to the repository's existing `self-hosted`, `linux`, `x64` labels. A queued or unexecuted run is not reported as a passed build. The verification record distinguishes this infrastructure/execution boundary from the committed mathematical revision. A further referee should assess the complete new proofs and require the native build report before treating typesetting and cross-references as verified.
