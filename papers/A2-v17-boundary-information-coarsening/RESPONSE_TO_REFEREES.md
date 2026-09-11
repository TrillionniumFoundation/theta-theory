# Response to the independent report on A2 v16

Manuscript: **Nonlinear boundary laws and two-contact rigidity in dispersing billiards**. Author: Qian Qi. Revision: **A2 v17**, September 11, 2026.

The report addressed here is `reviews/a2-v16-independent-harsh-adaptive-experiments-2026-09-11/REFEREE_REPORT.md`, at review commit `c5fed5340df3147f64cb3479cf1837357f73e7a8`. Its reviewed author source is `bd27ed3208cc869f6c7a6547453a2557bfcd03ed`, native directory `papers/A2-v16-integrated-submission`. These identities, not an unpinned default branch, determine this response.

The referee distinguishes editorial significance from a newly identified fatal mathematical error. We retain that distinction. We do not interpret the report as acceptance, and do not answer its significance objection merely by counting elementary consequences or enlarging the list of qualifications.

## C16-E1: the mathematical advance and its comparison with classical mechanisms

**Response: a new proved observation-dependent critical law, not a rebranding of the stopped coupling.**

The complete relative law, its geometric inverse, the scalar determinant identification, and the two-flight benchmark remain in the main article. Four new active inputs are added; none of the 56 old direct inputs is removed. The second part now begins with a boundary-information theorem and its physical application, before returning to complete-profile observation.

Let `q_j = exp(-j gamma)` and `r_j = q_j^2 log(1/q_j)`. After residual time is integrated out, the two tangent endpoint densities, in common whitened coordinates, are

`f_zeta(x) = (2/pi) (1 - exp(-zeta) x_1^2 - exp(zeta) x_2^2)_+`,

with `zeta_j = log((1+q_j)/(1-q_j))`, and `f_0`. The two tangent raw laws have exactly the same success mass `p^0_{j,d} = d^2/(2 A sinh(j gamma))`. Consequently the success bit contains no tangent shape information at any sample size, whereas the endpoints do.

The new theorem `thm:v17-boundary-information`, in `article/18_boundary_information.tex`, proves for a normalized density `a_t(w_t)_+` that

`H^2(f_t,f_0) = (I_Sigma/4) t^2 log(1/|t|) + O(t^2)`,

where `I_Sigma` is the integral of `a_0 (partial_t w_0)^2 / |grad w_0|` over the moving boundary at zero. The proof includes the coarea estimates, the truncated-score central limit argument, the negligible exclusive-support mass, the quadratic-likelihood term, and a bounded-overlap argument for total variation. Independent rare-event thinning retains the failure atom and contributes its exact success mass. This is not an invocation of finite Fisher information, which is infinite here.

For the physical cap this boundary coefficient is exactly one. Theorems `thm:v17-endpoint-tangent` and `thm:v17-endpoint-physical`, in `article/19_endpoint_critical.tex`, give the full critical testing profile

`TV -> 2 Phi(sqrt(b)) - 1`, `Bayes error -> Phi(-sqrt(b))`,

when the effective number of successes times `r_j` tends to `b`. At a finite positive limit the tangent log likelihood under the boundary hypothesis tends to `N(-2b,4b)`. The theorem includes subcritical necessity and sufficiency, supercritical separation, both flight parities, and unequal contact curvatures. Physical transfer is proved at positive offsets satisfying `omega(d_j) = o(r_j)`, with `omega(d)=sqrt(d)` generally and `omega(d)=d` for individually even contacts. Explicit nonempty offset sequences are supplied. The supercritical proof uses critical subsamples rather than imposing vanishing approximation error over the entire supercritical sample.

The sharp endpoint success scale is therefore `exp(2 j gamma)/(j gamma)`, and its raw preparation scale is `d_j^(-2) exp(3 j gamma)/(j gamma)`. These use the exact hyperbolic multiplier, not a supplied upper convergence certificate `tau`.

Corollary `cor:v17-coarsening-hierarchy` compares three experiments for the **same fixed table, same finite/boundary pair and same physical preparations**. At the endpoint-critical scale their limiting distances are respectively `1`, `2 Phi(sqrt(b))-1`, and `0` for complete endpoint--residual records, endpoints alone, and the success bit. Conversely, at the former full-record critical scale the endpoints alone are asymptotically indistinguishable while the complete record has its previously established erasure limit. The new normal transition cannot be recovered sharply by applying the old total-variation contraction bound to the coarsened observation.

**Attribution and scope.** Smith's 1985 nonregular-likelihood work already contains the different normal rate for linear vanishing at a moving endpoint. We explicitly cite that comparison and prove the hypersurface coefficient and rare-event application needed here directly. Neither the existence of scalar linearizers, elementary sequential coupling, nor the classical nonregular phenomenon is claimed as an original general discovery. The added result is the exact observation-dependent billiard transition and its boundary-information calculation. It does not assert a minimax full-profile acquisition exponent, a parameter-free simulator for an unknown table, or geometric rigidity for unrestricted asymmetric contacts. The original general smooth forward/profile theorems and the independent even-contact inverse retain all their statements and proofs. Whether the resulting combined contribution meets the requested journals' significance threshold remains a question for independent mathematical and editorial assessment.

## C16-R1 and C15-1: full native build evidence

The requested target is the actual `main.tex` with **every active appendix**, following a build of the unmodified `two_collision.tex`. An isolated section build is not substituted for that target. `VERIFICATION.json` and the build reports distinguish executed checks from the status of that complete build. This response does not infer a TeX failure or an infrastructure cause merely from a failed Actions job.

During this revision the pinned v16 job was explicitly re-run. The connector accepted the rerun; run `34555357324` then returned job `103149717735` with conclusion `failure` and no returned step list. That observation does not establish that LaTeX ran. Full-source materialization and local build evidence, rather than the existence of a workflow file, are the relevant completion criteria. The verification record is authoritative for the currently executed build status.

The native directory is copied by its exact Git tree `522585afd2e14d3380c3305fed5f5ea03d208192`; the original companion remains blob `df44402b17031525c087d39dfedf8dac3ada611d`. Overwritten metadata, the old entry point and the old bibliography are preserved by blob identity in `history/v16/`. The old direct-input list is contained in `history/v16/main.tex` and is a subset of the new active list. The new mathematical proof files are additions, not replacements for earlier content.

## C16-R2: stale root discovery pointer

The repository-root README on the new revision branch now identifies A2 v17 and links its complete native directory, this response and its verification record. The prior v15 and v14 navigation is explicitly historical. The A1 and other workstream sections are retained, and no change is made to the default branch by creating this revision branch.

## Section 4.1: stopped physical comparison and pilot charge

The whole v16 stopped-kernel argument, success-weighted budget, retained failures and stopping time are preserved. The pilot remains exact in both experiments; bad pilot histories use the specified valid fallback kernel and their probability is charged. The new endpoint theorem does not use an unknown gap to select physical windows or convert a proof coupling into an observation rule. Its whitening is common to a known simple pair, solely for comparing their distances.

## Sections 4.2--4.3: adaptive common-history measure

The exact overlap remains the expectation of the product under the auxiliary common-history law. The reverse erasure kernel remains weighted by that product. The new diagnostic repeats the referee's `117/250` common-mass example, checks its distinction from `9/20`, and checks the `9/13` weighted reverse probability. These are finite exact negative controls, not counterexamples to v16 and not substitutes for its general proof.

## Section 4.4: random accumulated hazard

The optional extension is now stated and proved as `cor:v17-random-hazard` in `article/32_random_hazard.tex`, with explicit attribution to this section of the report. When the hazard sum converges in distribution under the common-history laws to a finite nonnegative random variable `B`, and the maximum hazard vanishes, the common mass tends to `E exp(-B)`. The proof uses tightness and the bounded product, not a replacement by `exp(-E B)`. The physical approximation budget and every failed preparation are retained. This corollary is presented as a clarification, not as the response to the significance objection.

## Previously closed mathematical comments and contribution hierarchy

The revisions do not reopen the scalar/physical distinction of C14-1, the multiplier notation of C14-2, the width/profile equivalence, or the corrected hierarchy of C15-2. The first-flight factors, two-flight return multiplier, physical Schur normalization and determinant product remain separate. The strict-margin benchmark remains attributed to the v15 memorandum. The finite two-flight and limiting jets remain fixed finite-jet coordinates, not equivalent noisy smooth-function experiments. General smooth profile determination is still a function-valued Volterra result rather than equality of formal Taylor series.

## Verification boundary

`tools/check_boundary_information.py` uses explicit exceptions, not assertions. It was executed in ordinary and optimized Python modes, with identical JSON outputs: 143 finite algebraic, source and quadrature checks. Their exact scope is printed in the output. The coarea proof, infinite-dimensional hypotheses, physical tangent estimates and full manuscript are not certified by that count. Independent referee review remains necessary.
