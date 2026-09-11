# Independent harsh referee-style report on A2 v20

**Manuscript:** Qian Qi, *Boundary laws, signed contact rigidity, and physical information in dispersing billiards*  
**Review date:** 11 September 2026  
**Requested standard:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the American Mathematical Society*  
**Author revision branch:** `revision/a2-v20-raw-physical-multirate-lan-2026-09-11`  
**Immutable author head reviewed:** `f3839d34fcc045da47f257fbbf61fb1699adc76e`  
**Immediate predecessor report:** `review/a2-v19-independent-harsh-top4-2026-09-11`  
**Principal active entry point:** `papers/A2-v17-boundary-information-coarsening/main.tex`

This is an author-requested, AI-assisted independent referee-style assessment. It is not a journal-commissioned report and is not an editorial decision by any journal named above. I have deliberately separated mathematical correctness, theorem scope, experiment formulation, novelty/significance, exposition, and submission readiness. Repository proof ledgers, response letters, literature audits, source manifests and CI metadata are useful navigation aids but are not treated as proof certificates.

## 1. Recommendation to the editor

**Recommendation: reject in the present form at the requested top-four level. A substantially reconstructed manuscript could merit a fresh assessment.**

V20 is a serious and mathematically meaningful revision. It should not be described as cosmetic, and I do not repeat the v19 objections as though nothing changed. In particular, v20 makes three important repairs.

1. The unknown-gap statistical experiment is no longer centered at the parameter-dependent time `jg(eta)+d`. The new design uses fixed physical times `t_{j,l}=j g_0+d_l` and places the gap at the faster local scale `g=g_0+delta_n a/j_n`.
2. The gap/onset direction is inserted into the moving-support velocity as a constant component, and the finite-design kernel argument now attempts to prove nonsingularity jointly in the gap and finite labelled contact-jet directions.
3. The finite-versus-boundary comparison is promoted to a stopped-transcript statement retaining failures, designs and stopping times, with an explicit `k_n tau^{j_n}->0` transfer condition and explicit preparation cost.

Those are genuine improvements. The signed-endpoint inverse theorem also remains the strongest and most interesting deterministic component of the manuscript: no direct algebraic contradiction emerged in my re-audit of the displayed determinant-one last-jet block under the explicitly labelled, signed, fixed-frame hypotheses.

The present revision nevertheless contains a new foundational defect in the central vector LAN theorem. The theorem writes a Radon--Nikodym likelihood ratio

`dP_{n,h}^{\otimes n}/dP_{n,0}^{\otimes n}`

for a family with genuinely parameter-dependent support. For outward-moving directions the alternative has positive mass on a region where the null has zero mass, so `P_{n,h}` is not absolutely continuous with respect to `P_{n,0}`. The displayed likelihood ratio does not exist as stated. The scalar predecessor in the same manuscript handled exactly this issue correctly by separating the absolutely continuous likelihood from the singular support-exclusive mass. The new vector theorem has regressed on that point. The conclusion is plausibly repairable, because the singular mass is of lower order at the critical logarithmic scale, but the theorem and proof in their current form are not mathematically well posed.

There is also an unresolved interface issue between the newly declared “fixed registered endpoint coordinates” and the historical geometric construction of the half-line actions in contact-centered frames. If the v20 statistical family is intended to consist only of anchored graph deformations for which the two contact origins and tangent axes are fixed in a common laboratory chart, the theorem can be coherent, but its scope is substantially narrower than a generic local family of unknown billiard tables and should be stated as such at theorem level. If generic nearby tables are intended, then contact-point and frame motion contribute additional terms to the support velocity, and a parameter-independent observation map plus a calibration/equivalence argument is still missing.

At the requested standard these are not matters for routine editorial correction. They affect the central theorem package and the interpretation of the paper's final arrow

`relative boundary law -> signed local rigidity -> raw physical local experiment`.

I therefore would not recommend “major revision” in the journal sense if that wording carries an implied path to acceptance. I would recommend rejection of the present submission, with the explicit observation that a substantially rewritten version closing the mathematical gaps below could deserve a fresh review.

## 2. Scope of this review

I reviewed the v20 active source graph at the immutable head above, with special attention to the material changed after the v19 report. In particular I inspected:

- `main.tex` and `article/01_introduction_v20.tex`;
- `article/01c_geometric_setup_v18.tex` and its coordinate conventions;
- `article/01a_protocol_scope.tex`;
- the retained relative-law and physical-transfer framework;
- `article/23a_signed_endpoint_rigidity_v19.tex`;
- `article/18_boundary_information_v18.tex`, especially its treatment of support singularity;
- `article/18a_vector_boundary_information_v20.tex` in detail;
- `article/18b_raw_physical_multirate_v20.tex` in detail;
- `article/17_adaptive_experiments.tex` and `v6/10_experiment_transfer.tex`;
- `RESPONSE_TO_REFEREE_V20.md`, `PROOF_LEDGER_V20.md`, `LITERATURE_VERIFICATION_V20.md`, `ACTIVE_SOURCE_MANIFEST_V20.md`, and `VERIFICATION_V20.json` as audit aids;
- the current GitHub Actions evidence for the v20 native build.

I also rechecked the paper's literature positioning against the contemporary marked/enriched-length rigidity literature and the classical nonregular-support statistical literature. The manuscript's revised positioning is materially more responsible than in earlier versions: it does not claim that generic parameter-dependent-support asymptotics, generic Le Cam theory, or one-dimensional linearly vanishing endpoint normality originate here, and it does not claim that one local endpoint channel globally subsumes marked-length rigidity.

As in any referee report of this scale, I have not machine-reproved every historical lemma in the auxiliary compendium. My audit concentrates on the theorem chain promoted into the title, abstract and introduction, and especially on the new v20 steps that purport to close the v19 blockers.

## 3. What v20 genuinely fixes

### 3.1 The fixed physical-time construction is the right conceptual response to C19-M1

The change

` t_{j,l}=j g_0+d_l `

is conceptually correct. The acquisition time is now programmed from the reference experiment and remains unchanged under the local alternative. With

` g_n(a)=g_0+delta_n a/j_n `,

one obtains the exact fixed-window excess

` d_l-delta_n a `.

This is the natural multirate mechanism: a gap perturbation of order `delta_n/j_n` produces an order-`delta_n` normal displacement of the support after `j_n` flights. This directly addresses the most serious time-centering objection in the v19 report.

The additional requirement `j_n delta_n -> 0` is also sensible in context. Contact-geometry perturbations of size `delta_n` change the long-bridge rarity exponent, and this condition keeps the success prefactors uniformly comparable to their reference values while still allowing, for example, logarithmic growth of `j_n` relative to the successful-record budget.

### 3.2 The gap direction is now present in the information kernel

For a same-type endpoint design the new support velocity is

`U_b(u,v)(a,h)=a+dot S_b(u)h+dot S_b(v)h`.

This correctly separates the constant onset/gap displacement from the contact-shape displacement. The argument that a vector in the common kernel satisfies

`a+dot S_b(u)h+dot S_b(v)h=0`

on every sufficiently small support level, then takes `v=0` and lets `u->0` to force `a=0`, is the right structural repair of C19-M2.

Once `a=0`, the displayed determinant-one triangular recursion strongly suggests tangent injectivity on any fixed finite labelled graph-jet model. I regard this as a real improvement over v19, subject to the proof-completeness comments below.

### 3.3 The stopped experiment transfer is now stated at the correct level

The new theorem compares the complete actual finite-bridge stopped transcript with the corresponding boundary transcript under the same capped policy and claims

`sup_{z in K} ||P^{fin}_{n,z}-Q^{partial}_{n,z}||_TV <= C k_n tau^{j_n}`.

The historical adaptive comparison theorem already contains the appropriate coupling mechanism and success-weighted budget. Specializing it to deterministic caps and a common fixed-time policy is mathematically natural. Failures are retained, stopping times are retained, and the cost is not replaced by the number of successful records. This substantially closes C19-M3, conditional on the common-coordinate issue discussed in Section 5 below.

### 3.4 The manuscript now admits that waiting counts may be more informative

The statement that waiting counts need not be ancillary is important. Because the success probability contains the long-bridge factor involving `sinh(j gamma)^{-1}`, the complete stopped transcript can carry information at a different scale from the endpoint-output coarsening. V20 no longer conflates the LAN/minimax result for the selected endpoint output with an assertion that the complete raw transcript has no additional information.

This is the correct scope. It should be preserved, and the abstract/introduction should be edited so that “physical minimax” cannot be read as optimality among all procedures using the complete raw transcript.

### 3.5 The introduction and literature positioning are substantially better

The introduction now makes a defensible comparison of information sets. Modern marked/enriched-length results are global and use very different data; the present signed endpoint law is locally richer in collision-coordinate information but globally much narrower. This is a meaningful comparison and avoids the earlier temptation to rank incomparable data sets by a single “stronger/weaker” slogan.

The statistical priority claims are also more disciplined. Classical linearly vanishing endpoint asymptotics and general parameter-dependent-support methods are acknowledged as prior mechanisms. The manuscript instead claims novelty for the geometric coefficient, the billiard coupling, the signed inverse, and the stopped physical transfer. That is a much better basis for a serious significance discussion.

## 4. Major blocker C20-M1: the vector LAN likelihood ratio is not defined as written

This is the most concrete mathematical error I found in v20.

The vector model is

`f_theta(x)=a_theta(x)(w_theta(x))_+`

and the triangular experiment is

`P_{n,h}=(1-p_n) delta_dagger + p_n f_{delta_n h}(x) dx`.

The theorem then asserts, under `P_{n,0}^{\otimes n}`,

`log dP_{n,h}^{\otimes n}/dP_{n,0}^{\otimes n}`

has a quadratic LAN expansion uniformly for `h` in compact sets.

That Radon--Nikodym derivative generally does not exist.

To see the issue, take any local direction for which the support boundary moves outward. On a collar patch where the normal velocity has the corresponding sign, there is a set

`A_{n,h}={w_0<=0, w_{delta_n h}>0}`

with positive Lebesgue measure and positive `P_{n,h}` mass, while `P_{n,0}(A_{n,h})=0`. Therefore

`P_{n,h} not << P_{n,0}`.

Adding the independent failure atom does not repair this: the singularity occurs inside the successful part of the experiment. For the opposite sign of the local direction one obtains the reverse support inclusion. A LAN theorem on a full neighbourhood of `h=0` cannot avoid both signs by a one-sided nesting convention.

The manuscript already contains the correct conceptual treatment in the scalar predecessor `article/18_boundary_information_v18.tex`. There the author explicitly speaks about the likelihood of the **absolutely continuous part**, estimates the support-exclusive mass separately, and allows an alternative singular component. That is exactly what the vector theorem must do as well.

At the critical scale the defect is likely repairable. The support-exclusive mass of one successful record is of order `delta_n^2`; under

`n p_n delta_n^2 log(1/delta_n) -> 1`

its accumulated probability is only of order `1/log(1/delta_n)` and hence tends to zero. But this observation does not make the finite-`n` Radon--Nikodym derivative exist. The theorem has to be reformulated.

### Required repair for C20-M1

A correct vector statement should do at least the following.

1. Fix a common dominating measure for the absolutely continuous pieces and write the Lebesgue decomposition of each local alternative relative to the null.
2. Define the log likelihood on the common-support event, with a precise convention on null-exclusive sets, rather than writing a nonexistent global Radon--Nikodym derivative.
3. Prove that the total mass of all support-exclusive events tends to zero uniformly for `h` in compact sets at the critical scale.
4. Prove the required mutual contiguity or asymptotic contiguity statement for the triangular local family.
5. Establish the quadratic likelihood expansion for the absolutely continuous part uniformly on compact local sets.
6. Only then invoke Le Cam's third lemma, Gaussian shift convergence, testing limits and local asymptotic minimax theory.

The current proof jumps from “support-exclusive observations occur with probability tending to zero” to an ordinary likelihood-ratio identity that is false at every finite `n` in the outward-moving directions. A top-four proof cannot leave this at the level of an understood convention.

This issue propagates directly into `article/18b_raw_physical_multirate_v20.tex`, because the physical LAN theorem invokes the vector theorem as its local statistical engine.

## 5. Major blocker C20-M2: the common registered spatial observation model is still not fully constructed

V20 convincingly fixes the **time** coordinate problem of v19. The status of the **spatial** endpoint coordinates is less clear.

The historical geometric setup constructs the half-line actions in transverse endpoint coordinates “at the contacts” and normalizes

`S_b(0)=S_b'(0)=0`.

For a generic smooth family of billiard tables the closest points and their tangent frames move with the parameter. A coordinate that remains centered at the moving contact is parameter dependent. Conversely, a truly fixed laboratory coordinate does not automatically preserve `u=0` at the perturbed contact or the normalization `S_b'(0)=0`.

The v20 introduction suggests a legitimate way out: restrict the local family to a **registered anchored graph model** in a fixed Euclidean chart,

`(-psi_0(u),u), (g+psi_1(v),v)`,

with the two contact origins and tangent axes fixed and only the gap and graph jets varying. In such a model the signed coordinate `u` can indeed be a common laboratory coordinate and the normalization can hold throughout the family.

If this is the intended theorem, it should be stated explicitly as a theorem hypothesis, not left to prose about “registration variables.” The phrase “unknown geometry” should then be understood as “unknown gap and anchored contact graphs in a fixed registered channel,” not as a generic nearby unknown billiard table.

If, on the other hand, the theorem is intended for generic nearby tables whose closest points and tangent frames move, more work is required. One must define a parameter-independent measurable map from the raw collision record to the common endpoint coordinates and calculate the derivative induced by contact translation and frame rotation. Those coordinate-motion terms enter the moving-support velocity and therefore the information matrix. They cannot be removed by saying that a frame is “registered” unless the registration itself is observed, fixed by the model, or justified by a charged calibration theorem.

The historical transfer theorem does not by itself settle this issue. It compares finite and boundary laws in common unscaled coordinates **for a fixed parameterized channel construction**. The end-of-section phrase about using the same boundary embeddings at each parameter is not automatically a parameter-independent observation map across the whole statistical family.

### Required repair for C20-M2

The manuscript should choose one of two mathematically precise routes.

**Route A: anchored registered submodel.** Define the admissible local parameter family by explicit fixed-chart graph equations, with contact origins and tangent axes fixed for every parameter. State that the theorem concerns only this submodel. Prove that the relative-law objects used in the statistical theorem are constructed in those same fixed coordinates.

**Route B: generic nearby tables.** Work in a fixed laboratory record space, add the moving contact/frame coordinates as nuisance parameters, derive the full support velocity including their contributions, and prove a pilot/asymptotic-equivalence theorem if one wants to transform to contact-centered coordinates.

Until this is done, the phrase “raw physical local experiment” is stronger than the theorem that has actually been constructed.

## 6. Major blocker C20-M3: the abstract-to-billiard LAN transfer is asserted, not quantified at the critical nonregular scale

The proof of the fixed-window multirate endpoint LAN theorem says, in essence, that the billiard endpoint family differs from the abstract moving-boundary model by

- an `o(delta_n)` perturbation of the defining function in `C^2`, and
- an `O(delta_n)` smooth amplitude perturbation,

and then states that the proof of the abstract likelihood lemma is uniform under such perturbations.

The conclusion is plausible, but for this paper it is a central theorem, not a routine parenthetical remark.

At a linearly vanishing moving boundary, a normal displacement `epsilon` contributes Hellinger scale

`epsilon^2 log(1/epsilon)`.

Thus the correct way to transfer the abstract LAN theorem is to prove an explicit experiment-distance or likelihood-remainder estimate comparing the exact fixed-window billiard endpoint family to the ideal vector boundary family. If the support error is `r_n=o(delta_n)`, one expects

`k_n r_n^2 log(1/r_n) -> 0`

under the stated critical scaling, but this should be demonstrated uniformly on compact local parameter sets. The regular amplitude perturbation is lower order because `k_n delta_n^2=O(1/log(1/delta_n))`, but that statement also deserves a clean lemma that keeps track of normalization.

This is especially important because the abstract theorem itself is non-dominated and must be repaired as explained above. Once the exact support bookkeeping is rewritten, “uniform under such perturbations” can no longer be treated as an automatic consequence of an ordinary dominated Taylor expansion.

### Required repair for C20-M3

Promote the abstract-to-billiard step to a standalone quantitative lemma or proposition. It should state the exact common observation space, the ideal and exact endpoint laws, and an `o(1)` Hellinger/TV/Le Cam bound under the printed sequence conditions. Then the physical LAN theorem can be obtained by a genuine transfer of experiments rather than by informal stability of a proof.

## 7. Major blocker C20-M4: the positive-definite finite design needs a tangent-level proof, not only an appeal to nonlinear rigidity

The finite positive-offset design lemma is structurally reasonable. However, after proving that `dot S_b h=0` for both labels, the manuscript says that “the leading reconstruction formulas and determinant-one recursion” force `h=0`.

For the particular finite graph-jet coordinates intended here, this should be true. But the tangent statement should be proved directly.

Global or local injectivity of a nonlinear inverse map does not, by itself, imply injectivity of its differential. In the present case the author has much stronger information available: the leading reconstruction formulas have a nondegenerate differential at fixed positive gap, and at each degree the new jet pair enters through an explicit determinant-one block. Those facts can be differentiated inductively to obtain the exact tangent injectivity needed for the information-kernel argument.

That direct proof would also make clear precisely which coordinates are included in `h` and which are excluded as registration variables.

A second scope point should be explicit: the finite set of positive offsets may depend on the chosen finite jet dimension. The manuscript says “every fixed finite labelled contact-jet model,” which is acceptable, but it must not be read as asserting that one universal finite set of windows simultaneously controls the full infinite jet.

## 8. The signed endpoint rigidity theorem remains promising, but its all-order proof is too compressed for the role it plays

I reiterate an important positive point from v19: I did not find an obvious sign, label or determinant contradiction in the claimed block

`[[coth(n gamma), r_0^n csch(n gamma)], [r_1^n csch(n gamma), coth(n gamma)]]`

with the curvature-ratio factors satisfying product one. Once the displayed formula is granted, its determinant is indeed one.

The support-threshold observation

`T_b(u,v)=S_b(u)+S_b(v),  S_b(u)=T_b(u,0)`

is also clean and conceptually useful. It explains exactly where the odd information is lost when the endpoint signs are integrated out.

The weakness is proof presentation. For a theorem carrying a large fraction of the paper's claimed originality, sentences of the form “the finite-jet dependence is proved exactly as in the previous theorem” and an envelope-principle sketch are not enough at the requested level. The nonsymmetric odd-jet extension should be made standalone.

A top-four version should include a precise all-order proposition that:

- writes the stationary half-line equations in the weighted sequence space;
- states the invertibility and uniform bounds for the Jacobi operator used in the implicit differentiation;
- proves that the first appearance of `q_{b,n}` in the degree-`n` action coefficient is unaffected by variations of the stationary orbit;
- derives the two geometric sums with all multiplicities and label conventions explicit;
- proves that lower jets cannot contaminate the highest new homogeneous degree;
- differentiates the leading recovery formulas and the triangular recursion to obtain quantitative local inverse bounds;
- explains the coordinate invariance or fixed-chart dependence of the odd jets.

This is not a request to weaken the result. It is a request to expose the actual mechanism that makes the result believable and reusable.

## 9. Statistical scope: the minimax statement is for a deliberate coarsening, not for the richest physical transcript

V20 now acknowledges this in a remark, but the distinction should govern the headline language more consistently.

The fixed-window endpoint-output experiment is obtained after discarding waiting counts and retaining a prescribed number of successful endpoint records. The preparation cost is charged, which is good, but the complete stopped transcript is statistically richer. Indeed the manuscript explicitly observes that the success probability may carry additional information through the long-bridge exponent.

Therefore the Gaussian information matrix `K_design` and its local asymptotic minimax value characterize the **endpoint-output coarsening**. They are not an efficiency bound for all procedures based on the complete raw physical experiment under a fixed preparation budget.

This distinction matters for the phrase “physical information.” There is nothing wrong with studying a meaningful coarsening, but the abstract and theorem summaries should say “physical endpoint-output LAN” or equivalent rather than invite the reading that the complete physical experiment has been asymptotically characterized.

A future paper could separately ask for the joint multiscale limit experiment of endpoint marks plus waiting counts. That might be mathematically richer than the present coarsened LAN and could strengthen the significance case.

## 10. Pilot-centered equivalence: useful, but the sigma-field must remain explicit

The charged pilot is a good addition. The condition

`k_n r_n^{2m+2} log(1/r_n) -> 0`

is of the right Hellinger form for making the residual centering error negligible across the retained endpoint records.

The corollary correctly states the conclusion for the endpoint-output experiment. That qualification should remain explicit everywhere. If one retains the programmed acquisition times, pilot transcript, waiting counts or other design variables, the sample spaces and Markov kernels used in the claimed Le Cam comparison should be written down. Data-dependent design times are not literally identical to oracle design times as random transcript coordinates.

This is a repairable exposition/proof-interface issue, not an independent reason for rejection once the main non-dominance problem is fixed.

## 11. Native build and submission readiness

The repository's own verification file correctly refuses to predeclare a successful native build. I checked the final v20 workflow evidence at the reviewed head.

The latest run of **“A2 v20 complete native build”** on head

`f3839d34fcc045da47f257fbbf61fb1699adc76e`

completed with conclusion **failure**. However, the job contains **no runner steps at all** (`steps=[]`, `runner_id=0`). Thus this is not evidence of a LaTeX compilation error. It is a failure before a runner executed.

The correct conclusion is therefore:

- there is **no demonstrated TeX failure from this run**;
- there is also **no successful native-build certificate for the final v20 head**.

Before submission, the workflow should be rerun in an environment where the job actually starts, and the canonical manuscript should compile with references, labels, bibliography and diagnostics checked from the exact submission source.

There is also avoidable source-version friction: the active v20 paper still lives under a directory named `A2-v17-boundary-information-coarsening`. That is harmless to the mathematics but undesirable for a high-stakes submission. I recommend freezing a single canonical v20 submission directory or release artifact. Historical response letters, proof ledgers and earlier modules can remain in the repository; they need not be deleted. They simply should not obscure which source and PDF constitute the paper being refereed.

## 12. Top-four significance assessment

The strongest potential contribution is not the generic nonregular statistics. The manuscript itself now acknowledges that linearly vanishing endpoint models, parameter-dependent support, limit experiments and local asymptotic minimax methods have substantial classical antecedents.

The strongest potential contribution is the **coupling** of three structures:

1. a uniform nonlinear long-bridge boundary law after normalization by an exponentially small twist;
2. recovery of unsymmetrized half-line actions and arbitrary labelled contact jets from signed endpoint support;
3. a physical observation scheme in which those same boundary actions control a nonregular local statistical experiment.

That is conceptually interesting. The determinant-one all-order signed jet block, if fully proved and robustly formulated, is particularly attractive.

I am not yet convinced that the current package clears the significance threshold of the four journals named above, even after the technical errors are repaired. The inverse theorem is deliberately local to one labelled channel, whereas the strongest modern rigidity results in the area obtain global conclusions from global periodic data. The statistical component is also deliberately coarsened and local around a registered reference channel. These differences do not make the theorem unimportant, but they make the top-four case depend heavily on the conceptual force and proof depth of the coupling itself.

A repaired version would be stronger if it produced at least one of the following:

- a genuinely coordinate-free local inverse theorem with a clear geometric interpretation beyond a registered graph chart;
- a global or multi-channel consequence that assembles the local signed data into a table-level rigidity statement;
- a joint limit experiment for the complete physical transcript, showing how waiting-time and endpoint information interact rather than deliberately discarding the faster channel;
- a sharp theorem explaining why the boundary law is a universal normal form for a broader class of hyperbolic scattering systems.

I do **not** make any claim here that an existing published theorem directly duplicates the signed endpoint determinant-one mechanism. My literature check did not reveal an obvious direct duplicate. The issue is that novelty and top-four significance are different questions: a result may be new yet still require a more compelling conceptual consequence or broader theorem architecture for this venue class.

## 13. Status of the v19 blockers after v20

For clarity, my assessment is:

| Previous issue | V20 status | Referee assessment |
|---|---|---|
| C19-M1 parameter-dependent time window | materially repaired | fixed physical times are the correct repair; spatial registration remains incomplete/ambiguous |
| C19-M2 missing gap direction | substantially repaired | constant gap velocity and finite-design kernel argument are structurally correct; tangent proof should be explicit |
| C19-M3 stopped experiment transfer | substantially repaired | theorem-level full-transcript TV statement is now present, conditional on common-coordinate kernels |
| C19-M4 local estimator overinterpretation | repaired | estimator is now explicitly local around a specified reference |
| vector theorem self-containment | improved but not closed | proof is expanded, but the new theorem writes a nonexistent RN derivative in non-dominated directions |
| literature positioning | substantially repaired | scope and nonclaims are much more responsible |
| native build | unresolved | final-head workflow failed before runner; no successful build evidence yet |

Thus v20 deserves credit for closing much of the previous review. The present rejection is driven primarily by **newly exposed mathematical formulation issues in the promoted v20 theorem**, not by mechanically carrying forward the old objections.

## 14. Required mathematical repairs before I would recommend fresh top-four review

I would want the following items completed before a new top-four assessment.

### R20-1. Rebuild the vector moving-support LAN theorem correctly in the non-dominated setting

Do not write a global Radon--Nikodym derivative when it does not exist. Separate absolutely continuous and singular pieces, prove compact-uniform negligible singular mass at critical scale, establish contiguity, and then derive the Gaussian shift and minimax consequences.

### R20-2. Define the physical common-coordinate family without ambiguity

Either restrict explicitly to an anchored registered graph model in one fixed laboratory chart, or add moving contact/frame nuisance coordinates and prove a charged calibration/equivalence theorem. The half-line actions, endpoint observations and support velocity must all live in the same parameter-independent record space.

### R20-3. Prove a quantitative abstract-to-billiard experiment transfer at the LAN scale

Replace “the likelihood proof is uniform under such perturbations” by a theorem giving an explicit `o(1)` Hellinger/TV/Le Cam comparison between the exact fixed-window billiard endpoint family and the ideal vector boundary family.

### R20-4. Make the finite-design nonsingularity proof tangent-level and explicit

Differentiate the leading recovery and determinant-one triangular recursion and prove injectivity of the derivative on the exact finite jet chart used by the statistical theorem.

### R20-5. Give the signed all-order jet recursion a standalone proof

The displayed matrix is elegant enough to deserve a complete proof rather than a cross-reference plus envelope sketch. This is central to both the inverse theorem and the information-kernel argument.

### R20-6. Keep coarsened and complete physical experiments terminologically separate

State all LAN/minimax claims as properties of the endpoint-output experiment unless and until the complete stopped transcript is analyzed. Preparation cost may remain charged, but cost accounting is not the same as statistical equivalence of the richer transcript.

### R20-7. Produce an actual successful canonical build

Rerun the native build until runner steps execute; compile the exact final source; freeze a canonical submission artifact and version pointer.

## 15. Smaller comments and presentation issues

1. Write `L_n=(log(1/delta_n))^{1/4}` rather than `log(1/delta_n)^{1/4}` to remove parsing ambiguity.
2. In the vector theorem, distinguish carefully between “finite-dimensional convergence of experiments,” “LAN expansion,” and “uniform LAN on compact local sets.” The last is stronger than pointwise third-lemma reasoning.
3. The claimed uniform convergence of the local central-sequence estimator under `P_{n,h}` on compact `h`-sets should be proved after uniform contiguity is established, not inferred from the fixed-`h` third lemma in one sentence.
4. The passage from bounded truncated quadratic loss to unbounded quadratic risk requires uniform integrability under local alternatives; after the non-dominated theorem is repaired, recheck that the fourth-moment argument is uniform under those alternatives, not only under the null.
5. The finite offset design is existential. That is acceptable, but the introduction should not suggest a universal finite measurement set independent of the chosen finite jet dimension unless such a theorem is actually proved.
6. The pilot theorem should state whether the pilot and post-pilot outputs are included in the compared experiment or whether only the endpoint-output sigma-field is compared.
7. The phrase “physical onset gives `g`” is appropriate for the deterministic inverse, but in a statistical theorem the cost and resolution of estimating onset must remain separate from an oracle observation. V20 mostly fixes this; keep that discipline throughout.
8. The auxiliary compendium is valuable for provenance, but a journal submission should expose a shorter proof dependency graph. A reader should not need proof ledgers to identify which lemmas are actually used by the main theorem.
9. Internal version names (`v17` directory, v18/v19 theorem labels, v20 active source) make the manuscript harder to audit. This can be cleaned without deleting any historical material from the repository.
10. The acknowledgement of AI-assisted independent memoranda is unusually transparent. It should remain factual and should not be used as evidence of correctness; the present manuscript appropriately says those memoranda are not editorial decisions.

## 16. Final editorial assessment

V20 is the strongest version of A2 I have reviewed so far. The fixed-window multirate idea is a genuine conceptual improvement, the gap direction is no longer silently omitted, the stopped-transfer theorem is much better formulated, and the signed-endpoint inverse remains potentially significant.

But the central vector LAN theorem is presently written in a mathematically invalid dominated-likelihood form, and the spatial common-coordinate realization of the advertised raw physical experiment is not yet pinned down at theorem level. Because the physical LAN theorem rests on those two interfaces, the headline statistical conclusion is not proved in the form claimed.

At *Annals/Acta/Inventiones/JAMS* standard, that is decisive. I recommend **rejection in the present form** rather than a routine major revision. If the author reconstructs the non-dominated LAN theorem, makes the laboratory/registered observation model exact, promotes the abstract-to-billiard transfer to a quantitative theorem, and expands the signed all-order inverse into a standalone proof, I would regard the resulting manuscript as sufficiently different to deserve a fresh mathematical and significance review.
