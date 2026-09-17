# Response to the referee on A2 v73

Qian Qi · September 17, 2026 · Revision 74

**Report:** `reviews/a2-v73-independent-harsh-top4-2026-09-17/REFEREE_REPORT.md`, immutable review commit `9c69f03f97dea57e83061af96aeb9bfe4dcc80d3`. The report reviewed source `3b1e7ce971cf84c8eed10a0077914f43b1b7ca68` and native-product head `70b0e466bdd2615381e007ed73b1576aaa21f3a0`. The source tree used here is independently matched to `80996c207ce723e8d84068f4fe95172f5d18fa65` from the frozen v73 source archive.

This is a response to an author-requested AI-assisted referee-style memorandum, not to a commissioned journal report. We retain the mathematical target and the complete inherited proof chain. The report explicitly identifies no new fatal core error and does not impose a hidden list of new research obligations. We therefore distinguish concrete corrections, mathematical preservation, an additional theorem, and the defense of significance. We do not relabel the referee's negative significance recommendation as a theorem gap that a build script can close.

## 1. Concrete corrections

### R73-P1: the missing current-version handoff

The report correctly identifies that the root index was still routed to v72 while the v73 subtree README named a nonexistent root `A2_REVISION_V73_REVIEW_READY.md`. Revision 74 supplies both the missing historical v73 entry and a current `A2_REVISION_V74_REVIEW_READY.md`, and prepends a clear current-A2 route to the root README without deleting its historical content. The subtree README links to the actual root entry with a working relative path.

The current entry separates the immutable review baseline, materialized source branch, and native-product branch. Native publication records the exact source commit and delivery directory. The product directory is pinned by the source commit and contains the complete PDFs, frozen source archive, logs, source/recorder manifests, numerical diagnostics, and a content-hash manifest. Publication verifies the fetched remote Git object bytes against the files before reporting success. The entry does not treat a scheduled workflow or an artifact name as proof that a native PDF exists.

The principal article, full technical manuscript and two-collision companion share content. Their lengths are reported separately, never summed as independent mathematical output.

### R73-P2: supplied amplitudes versus the preparation measure

We agree that “without a flux model” can be read more broadly than the proved observation model. The unified abstract and the definition of the marked experiment now state that charged preparations are independent draws from normalized unit-speed Liouville measure on full phase space and that success tags and acceptance gates are exact. The charged overview repeats this convention. The smooth-rigidity statement now says “separately calibrated local flux amplitude,” and the charged conclusion states the preparation hypothesis again.

No theorem hypothesis has been weakened or removed. Local amplitudes and curvatures are reconstructed rather than supplied. The area normalization is nevertheless tied to the specified preparation measure. The theorem does not assert area identification under an unknown reset density or an unknown acceptance efficiency. Bounded errors are post-acceptance coordinate readout errors, not corrupted tags. The same-gate finite central identity remains exact.

## 2. Mathematical findings retained, not misrepresented as repaired defects

**R73-M1, exact phase-volume anchor.** Proposition `prop:v73-area-anchor` and both its finite and limiting alternatives are retained. The factor `2π`, the zero action gauge, the exact identity `β_N(0,0)=1`, and the distinction between central conditional density and unconditional subdensity are unchanged. The offset and Jacobi normalization are recovered in the stated order; no curvature oracle is introduced. The full success prefactor, not merely its decay exponent, carries the area information.

**R73-M2, both directions of the observation fibers.** Theorem `thm:v73-fibers`, its common-collar qualification, the area-changing and exactly compensating remote deformations, and the finite adaptive-kernel argument remain. The new moment corollary invokes both directions instead of inferring global boundary equality from local germs. Equality is asserted on sufficiently small common gates, with their own normalization, not outside common representatives. Finite-family equality is not labeled a sufficient statistic of one finite sample.

**R73-M3, logarithmic twist sensitivity.** Lemma `lem:v73-log-twist` remains unchanged. Both the new finite comparison and its sampling theorem retain `C(1+N)` in area error. The nonzero derivative of the Floquet exponent prevents deleting this factor from that comparison, but is not asserted to be a minimax lower bound.

**R73-M4, curvature control before profile control.** The new compression inverse controls the limiting density in `C^m`, not merely in `C^0`. It therefore feeds the same fixed-slice action inverse and quadratic curvature inverse as v73. The proof explicitly obtains curvature from differentiated action data before invoking actual smooth profile stability. It never infers curvature control from a uniform graph error.

**R73-M5, joint physical realizability.** The estimator is selected from a countable dense subset of the *finite compressed image of actual table–offset pairs*, with one actual representative retained at each point. Its area belongs to that same table. Closedness or compactness of this image is not assumed; separability suffices. The near-minimum selection is measurable and includes a fixed physical fallback. It is an existence construction, not an efficient enumeration algorithm, and an arbitrary reconstructed factor-model density is not declared to be a billiard law.

**R73-M6, charged statistical estimates.** The inherited two-dimensional estimate and its hypotheses remain. The new theorem charges the same `rB` independent preparations, including failures, and uses the count at one existing phase for area. It proves the four weighted one-dimensional kernel estimates directly, including the envelope term, derivative supremum, deterministic bounded-readout perturbation, count concentration, finite-flight bias and noisy-readout-dependent stopping rule. Correlation among the four profiles is handled by a union bound, not by claiming their independence. There is no optimality claim.

**R73-M7, the finite clock correction.** The finite mixed-log-density formula and its unsigned amplitude correction in the v72 module remain unchanged. The new moment identity is exact for the separated *limiting* law, not for a general finite-flight density. The proof explicitly carries the `O(exp(-ωN))` defect and does not substitute a rank-two surrogate into the finite exact area formula.

## 3. A stronger consequence of the same physical record

The report did not require another theorem merely to keep the project viable. The following addition arose from reexamining the existing separated law and addresses the statistical content without replacing or reducing the geometric theorem.

Write the limiting density on a full gate `J²` as

`f(u,v) = Z^{-1} w(u) z(v) [d - A(u) - C(v)]`.

Define four functions `M_j(u)=∫_J v^j f(u,v)dv` and `N_j(v)=∫_J u^j f(u,v)du`, for `j=0,1`, and the matrix `H_f=E_f[(1,U)^T(1,V)]`. Lemma `lem:v74-skeleton` proves

`f(u,v) = (M_0(u),M_1(u)) H_f^{-1} (N_0(v),N_1(v))^T`.

This low-rank algebra is classical in character and is attributed accordingly to the exact CUR literature; it is not advertised as an invented general matrix theorem. What must be supplied in the present problem is its nondegeneracy and compatibility with physical asymptotics and the smooth inverse.

Proposition `prop:v74-nondegeneracy` proves the determinant formula

`det H_f = -(W² V²/Z²) Cov_w(U,A(U)) Cov_z(V,C(V)) > 0`.

The opposite marked derivatives `A'(0)=-p` and `C'(0)=p` give opposite monotonicities on a class-uniform small gate. The covariance identity then gives an explicit positive floor. The proof tracks the dependence on the gate radius, amplitude bounds and slope lower bound. No new supplied amplitude, curvature, or matrix-conditioning oracle is added. Normal incidence is not silently included in this first-moment theorem: a symmetric quadratic example has a singular first-moment matrix, and the existing normal-incidence two-offset theorem is retained without change.

The reconstruction map is locally Lipschitz in `C^m` with no derivative loss. Proposition `prop:v74-finite-stability` combines it with the relative finite-to-limit estimate and the inherited physical-image stability. Lemma `lem:v74-estimation` then estimates four functions of one variable using the same paired observations. The variance and bounded-readout terms are respectively

`[L_n/(n h^(2m+1))]^(1/2)` and `δ h^(-(m+2))`.

Theorem `thm:v74-charged` gives the improved exponents

`α_1=s/[2(m+s)+1]`, `γ_1=s/(m+s+2)`.

Corollary `cor:v74-budget` gives `β_1=α_1ω/(ω+α_1Γ)` and joint error `C t log(e/t)`, where `t=(L_B/B)^β_1+δ^γ_1`, subject to its explicit count, gate, bandwidth and small-error conditions. The local profile-and-offset bound is `Ct`; the additional logarithmic factor is retained for area.

This is a strict improvement of sufficient upper bounds over the previous two-dimensional smoothing calculation on the same oblique bounded class. It is not a claim of minimax optimality, exact finite-sample sufficiency, replacement by unpaired marginal observations, or an information comparison with lens data.

## 4. Significance and organization

We respectfully maintain the case for the paper on the combined mechanism: a relative physical law at an exponentially small scale, followed by an inverse on actual smooth boundary functions, including flat parts. The exact scalar area anchor is not presented as a substitute for these mechanisms or as an independent global shape theorem. The moment reconstruction supplies a further structural consequence with a quantified improvement from the same observation record.

The paper continues to distinguish its data from exterior travelling times, marked lengths, and enriched marked lengths. No dominance, same-data superiority or exhaustive priority claim is asserted. The comparison remains with the planar Noakes–Stoyanov result, the analytic symmetric/generic open-billiard result of De Simoi–Kaloshin–Leguil, and the enriched-spectrum finite-horizon Sinai result of Finamore–Leguil, under their actual hypotheses. The primary records were checked on September 17, 2026. Hamm–Huang, arXiv:1903.09698v2, is added for the classical low-rank reconstruction context.

The principal article keeps a mechanism-first introduction and complete proofs, with revision administration outside the mathematics. The abstract is unified to state the smooth result, the one-law/moment consequence, and the charged model coherently. Every inherited mathematical input remains active in its previous principal/full/companion route. The full technical manuscript preserves the information, analytic, global and multichannel developments; it is not substituted for a missing proof in the principal route where those results were already proved.

We do not claim that this response reverses the referee's recommendation. Exceptional significance remains a judgment for the next independent assessment. The revision supplies a precise mathematical case and stronger proved statements for that assessment rather than a self-issued acceptance certificate.

## 5. Verification and limits of verification

The frozen v73 archive was checked against its per-file hashes and modes and reconstructs the exact pinned source tree. The preservation checker verifies all 969 inherited paths, the nine archived originals, and inclusion of every previously active mathematical input. Only the four abstract fragments are replaced as active summaries; their files are retained unchanged.

The new exact diagnostics cover a generic nonsymmetric two-by-two matrix identity, six positive polynomial factor models with both signs of obliquity, the covariance determinant, rate balances, and negative controls for a transposed matrix, finite rank defect, normal incidence and mixed gate normalization. They use explicit exceptions and are run both normally and under Python optimization. These are model/algebra checks, not actual-table realization proofs or proofs of uniform statistical bounds.

Native verification builds the three complete source-matched entries from Git objects and checks unresolved references/citations, duplicate destinations, missing glyphs and recorder provenance. The delivery manifest records actual PDF page counts and SHA-256 hashes. Visual inspection is separate and its actual coverage is named in the delivery; the build script alone does not perform it. The inherited analytic/global catalogue and companion are preserved and compiled, not newly independently recertified theorem by theorem.
