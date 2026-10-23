# Response to the controlling referee report — General Theta Foundations I, R79

## 1. Identity of this revision and of the controlling report

This is an author revision of **General Theta Foundations I: Acquired Geometry and Causal Resource Transfer**, by Qian Qi. The paper's research identity and its objective of consideration at Annals of Mathematics, Acta Mathematica, Inventiones Mathematicae, or the Journal of the American Mathematical Society are unchanged. We respond to the contribution objection by identifying and proving additional structure, while retaining the valid mathematical inheritance. We do not interpret source reconstruction, additional pages, or successful finite tests as a favorable editorial assessment.

The immediate mathematical baseline is the complete R78 source at commit `e0377beea364e456af2301f5e4fec98fe343cbcb`, root tree `f17e457a57a2a7f14d1fe4996258dde167ea678f`, with paper subtree `072a5a8c7b251964c0f5ba8c1c109d88a93302ee` at `papers/General-Theta-Foundations-I-restart/r78-reset-memory-frontier`. This is actual native source, including the complete reset-frontier proof and its recursively preserved predecessors. R79 continues that source. A reference inside an earlier reading guide to a proposed publication directory is not, by itself, evidence that such a publication or its build has been deposited. Current source, current native execution, and current publication identity are recorded separately in this revision's provenance and publication records.

The controlling substantive report remains the R65 report at commit `358481b21ceeeedb1205ebd30f86982e32a2cb04`, original path `GENERAL_THETA_FOUNDATIONS_I_RESTART_R65_BOUNDARY_MEMORY_EXTERNAL_REFEREE_REPORT_R65.md`, Git blob `d1ff9c5662390156ee212c82b173e86a21180e84`, SHA-256 `8c7d45d762736009fda667621fdf5019fa934f5f45f39364c747f837e6d7343c`. It reviewed R65 mathematical source `0469eb4f852eeea953cb3725d4b34dfdd2bf9d36` and publication `ee79ca9114f8009d62c056d07381b766645e3fc4`. It did not review R66–R79.

That report has already received substantive responses in R66–R78. It is the latest applicable report whose broader objections continue to require a response, not a newly discovered wholly unanswered report. The current branch and content census found no later substantive report assessing the newer mathematical source. Empty review refs, repeated reports, source-transfer attempts, pipeline audits, internal author-team challenges, and reports about other Theta papers do not supply a later independent assessment. The actual enumeration, retrieval, hashes, and classification coverage are recorded in `SOURCE_PROVENANCE.md`; they are not presented as a new independent proof review of every historical theorem.

The main historical dependencies include the R64 report at `0a66ca2ede7835ede2a62fe2363ba5dd3ccd2ed8`, the R59 round-three report at `c39922c242f9bd03d2e0d7f05d6e9b483362e26d`, and the original-paper v94/R62 report at `58581d5a6391642fb0849f8c8bb49c8c0c20b63c`. Their scopes and remaining obligations are addressed below. They are not reports on R79.

## 2. What changes mathematically, and what is inherited

The central new question is whether the full cost frontier at every **fixed classical memory budget** remains stable when a quantum instrument or its fixed hidden-model family is perturbed, including when reachable supports change. This is stronger than a comparison that truncates history and then allocates additional labels. A nearly optimal controller may have an unreachable dark label in one model, or continuation values that diverge near a parameter boundary despite a uniformly bounded initial value. A full-space inverse therefore cannot simply be assumed, and a bound on the initial value cannot be assigned to every continuation block.

R79 proves that returning occasionally to the already counted initial **classical label** cures this obstruction without resetting the quantum system or enlarging memory. If an M-label controller has robust initial cost at most b and the conditional mean call costs lie between positive constants c_* and c^*, changing only the update probabilities by

`u_epsilon = (1-epsilon) u + epsilon delta_initial`

gives robust initial cost at most

`U_epsilon = b / (1 - epsilon b/c_*)`

and cost at most

`K_epsilon = c^*/epsilon + U_epsilon`

from every physical state at every controller label, provided `epsilon b < c_*`. The proof derives finite cost by summing restart generations; it does not rearrange an inequality whose unknown value might be infinite. The physical posterior and the hidden model are unchanged at a label restart. The all-initial-state guarantee supplies the conditional bound needed after each restart.

These global cost witnesses yield a directed primitive-perturbation bound at the same M. If paired source and target models have normalized instrument error at most eta and cost-operator error at most zeta, the target value is at most

`U_epsilon / (1 - (zeta + eta K_epsilon)/c_*)`

when the displayed denominator is positive. For two nearby compact model families with common positive cost bounds and a common one-row upper bound B, this gives a local `O(sqrt(eta) + zeta)` modulus whose constants are independent of M. The statement includes changes of reachable support. It does not assert continuity of an optimizer, its support projection, or its unregularized continuation potentials, and it does not claim that the square-root exponent is sharp.

When every command in every compared model has success effect at least `kappa I`, the stronger classical resolvent estimate gives the explicit same-M, uniform-in-M Lipschitz bound `zeta/kappa + c^* eta/kappa^2`. The scalar one-command problem shows that the coefficients are locally sharp at the stated bounds. The counted finite-prefix approximation also improves to an exponential tail `C_0 (1-kappa)^T`. This separate positive-success regime is credited to the standard resolvent mechanism; its sharp scalar dependence does not establish sharpness of the square-root estimate at support degeneracies.

The exact cost-certificate layer is presented with a self-contained proof so that this stability theorem has a short mathematical entry. Its relationship to the earlier source is explicit:

| Mathematical component | Inheritance and present use |
|---|---|
| Finite reachable support, supported resolvents, modelwise cost and score certificates | Already proved in `sections/12-finite-memory.tex`, `lem:reachable-support`, `thm:memory-certificate`, and in `supplement.tex`, `thm:face`. R79's cost-only formulation is an explicit specialization and assembly, not a first discovery of these facts. |
| Finite-family exact fixed-memory algebraic synthesis and attained loss optima | Already proved in `cor:memory-algebraic`. The R79 formulation extends the exact cost-frontier statement to compact semialgebraic fixed-model families and arbitrary nonreset feedback, with the quantifier order displayed. Generic controller nonlinear programming and real-algebraic elimination remain classical. |
| Dark-subspace feasibility and a common one-row fallback | Inherited from `thm:primitive-fallback` and the compact-family fallback argument. R79 restates and proves the required mandatory-success specialization; it does not claim priority for invariant-subspace reachability. |
| Centering a bounded observable on a normalized instrument output | Already used in `sections/19-compact-risk.tex`, `eq:effect-distance`. R79 applies that estimate to the new global same-memory cost witnesses. |
| Truncation followed by an actual fallback | An inherited completion method. The new history-limit corollary records its relation to the current all-M cost frontier with every history/fallback label counted. |
| Same-label regularization and an explicit primitive modulus uniform in M | The new structural step in `sections/55-memory-regularization.tex`: it obtains globally bounded cost witnesses and stable costs without adding live labels, even though the exact unregularized support may change. |
| Exact hidden-model frontier | `sections/56-exact-hidden-model.tex` proves `V_1=2`, `V_2=(1+sqrt(5))/2`, and `V_M=3/2` for `M>=3`, with a counted pure initial label, matching lower bounds against all permitted stochastic controllers, and explicit model-dependent supports. It is a fully solved example, not the scope of the general stability theorem. |

The robust controller condition has the order

`exists one common controller; for every fixed model; there exist modelwise support and cost witnesses`.

Neither the witnesses nor the model are inputs to the executing controller. The cost minimum at each fixed M is attained by lower semicontinuity on the compact controller parameter space. Compact semialgebraic uncertainty permits exact real-algebraic synthesis under the specified encoded-input hypotheses. This does not decide whether the unrestricted-history value is attained at some finite M. The history-limit result proves convergence of the finite-memory costs, with an explicit counted finite-prefix construction, while preserving that distinction.

**Current native locations.** The consolidation and compact-model cost frontier are in `sections/54-robust-instrument-frontier.tex`, especially `thm:r79-exact-certificate`, `thm:r79-quantum-frontier`, and `eq:r79-robust-budget-quantifiers`. The new regularization and stability chain is in `sections/55-memory-regularization.tex`, `thm:r79-label-restart`, `lem:r79-centered-perturbation`, `thm:r79-frontier-stability`, and `cor:r79-history-limit`. The uniformly positive-success refinement is `cor:r79-positive-success` in the same source. The exact example is `sections/56-exact-hidden-model.tex`, `prop:r79-golden-ratio-memory`. The theorem map supplies their actual compiled numbers and page locations.

## 3. Accepted conclusions that remain accepted inheritance

The R65 report explicitly did not reject the paper for a technical-correctness defect. It found the first-herald least-cost identity, compact minimax and zero slack, the unique-decision residual criterion, stochastic determinization under its actual hypotheses, the one-model tie criterion, robust randomization example, fixed-memory attainment and strict gaps, rotating-qubit obstruction, uncertain-polarization extension, unitary periodicity result, strict-gap contraction mechanism, contraction-only counterexample, exact one/two-label qubit formula, and unary rational synthesis argument technically credible. Its assessment also inherited the preceding R64 boundary-attainment, complete performed-law, resource-price dual, sparse-witness, Bellman, multi-resource, timing, and actual-history-transfer conclusions at their stated scopes.

Those conclusions and their original proofs remain in the current mathematical packet and preserved source chain. R79 does not manufacture a new defect in a previously accepted argument. It also does not infer that the acceptance of an earlier scoped proof is an independent assessment of a later theorem. The response below distinguishes preserved closures, new consequences, and still-open questions.

## 4. Responses to the ten major requests in R65 section 17

### R65-17.1 — Identify the mathematical center and separate the theorem layers

**Issue: organization, breadth, and exact scope.** The main article now centers on the stability of the complete finite-memory cost frontier under primitive perturbations. The support certificate and exact fixed-M optimization supply the necessary foundation, with their inherited origin identified. The principal new theorem is the same-memory regularization and uniform-in-M stability result; the exact hidden-model frontier makes the role of the initial label and inaccessible modelwise supports explicit.

This does not erase the stronger special structure of known reset experiments. Their scalar Bellman normal form, deterministic report-only routing, exact action-cover formula, and stable strict hierarchy remain intact. The arbitrary-experiment causal-transfer theorem, fixed-memory quantum certificate, known-reset specialization, exact model families, and local geometric theorems retain separate hypotheses and conclusions. In particular, the new general quantum controller theorem is about a declared finite-dimensional time-homogeneous interface with globally legal commands, positive mean costs, and mandatory success stopping; it is not a classification of every causal experiment.

**Locations:** `sections/54-robust-instrument-frontier.tex`, `thm:r79-quantum-frontier`; `sections/55-memory-regularization.tex`, `thm:r79-label-restart`, `thm:r79-frontier-stability`; `sections/56-exact-hidden-model.tex`, `prop:r79-golden-ratio-memory`; retained `sections/53-reset-memory-frontier.tex`, `thm:r78-palette-normal-form`, `thm:r78-reset-frontier`; `THEOREM_MAP.md` and the current dependency map.

**Disposition:** the mathematical center follows the new proved structural result. The report's broader significance judgment remains subject to independent assessment.

### R65-17.2 — Compare directly with Moore/Myhill–Nerode and other classical antecedents

**Issue: priority and the meaning of the claimed contribution.** We retain the explicit attribution of finite residual equivalence and minimal deterministic output machines. The old contribution is the operational derivation of a forced output rule and its zero-slack stochastic determinization, not the classical residual theorem itself. The residual quotient remains task/dictionary specific and is not the whole predictive quotient.

The current revision makes an additional internal-priority distinction. Reachable quantum supports, supported potential equations, and finite-family fixed-memory algebraic synthesis were already present in this paper. Their self-contained restatement in the new main chain is not counted as new mathematics. Classical controller nonlinear programs, positive-operator transience, bounded-observable centering, and real-algebraic elimination are likewise credited. The added structural claim is that an arbitrarily prescribed finite memory can be regularized by changing only its existing update rows, obtaining global cost witnesses and a primitive perturbation modulus with constants independent of that memory size. The exact hidden-model example is a sharp illustration with proved matching bounds, not a claimed new principle of automata minimization.

**Locations:** `sections/22-boundary-memory.tex`, `thm:boundary-regularity`, `prop:boundary-ties`; `sections/12-finite-memory.tex`, `thm:memory-certificate`, `cor:memory-algebraic`; `supplement.tex`, `thm:face`; `sections/19-compact-risk.tex`, `eq:effect-distance`; `sections/55-memory-regularization.tex`, `thm:r79-label-restart`; `LITERATURE_AND_PRIORITY.md` and `references.tex`.

**Disposition:** the old attribution closure is preserved, and the added contribution is separated from both external and internal antecedents. No exhaustive priority clearance is claimed.

### R65-17.3 — Develop the robust tied case

**Issue: missing uniqueness, shared realization, and quantifiers.** The previously proved weighted-face and invariant-polytope criteria continue to handle robust tied terminal decisions on their declared boundary-rigidity interfaces. R79 does not replace those criteria by selecting an arbitrary tied Bayes action. In the current cost problem, the exact fixed-M condition imposes no uniqueness of a minimizing command or update. It includes all stochastic command/update rows, one common controller over a compact fixed hidden-model family, singular effects, and modelwise reachable supports. Exact compact-semialgebraic synthesis uses that shared-controller quantifier rather than a separate optimizing controller in each model.

The distinction between robustness over initial preparations for one known instrument and robustness over a fixed unknown primitive model is now explicit. The latter can retain useful historical information after a physical reset. The positive-probability example proves that the known-instrument report-only normal form cannot simply be exported to that hidden-model setting. The golden-ratio example gives a matching all-M cost law with arbitrary permitted stochastic updates. These are substantive cost and realization results. They do not identify the optimal tied word-response function for every bounded terminal-loss problem or remove optional-stopping hypotheses from the earlier boundary theorems.

**Locations:** `sections/23-robust-realization.tex`, `thm:weighted-face`, `thm:convex-memory`; `sections/25-stopping-rigidity.tex`, `thm:r67-optimal-face`, `thm:r67-polytope`; `sections/54-robust-instrument-frontier.tex`, `eq:r79-robust-budget-quantifiers`, `ex:r79-hidden-model-memory`; `sections/56-exact-hidden-model.tex`, `prop:r79-golden-ratio-memory`.

**Disposition:** prior scoped tie closures remain closed; exact shared-model cost optimization and stability are strengthened. An arbitrary tied terminal-loss/optional-stopping classification is not claimed.

### R65-17.4 — Broaden the physical interface beyond the heralded-word model

**Issue: restrictive primitive assumptions and the source of sufficient information.** The original R65 herald theorem retains its premises. The current cost-frontier/stability chain permits arbitrary finite-dimensional completely positive failure maps; state-dependent success probabilities and costs; several commands and reports; nonreset posteriors; singular reachable supports; stochastic updates; and a compact unknown model that stays fixed during a run. The quantum state need not be determined by the latest report. No fixed prior, unique sign sequence, or model-independent word law is assumed.

We do not claim that these general nonreset certificate ideas first appear in R79: the earlier finite-memory potential theorem already supplied them for its analytic scope. The present advance assembles an attained robust cost frontier, extends its exact encoded synthesis to compact semialgebraic model uncertainty, and proves a same-memory primitive stability theorem across support degeneracies. The regularization writes an existing classical label and performs no quantum reset. The source and target comparison pairs complete fixed models only in the proof; it never changes the model during an execution.

The remaining assumptions are explicit: finite time-homogeneous primitive interface, all initial density matrices, globally legal commands, a positive conditional mean-cost floor and finite upper bound, the declared observation port, and mandatory stopping at success. Arbitrary rejection of success or optional commitment is not silently added.

**Locations:** `sections/54-robust-instrument-frontier.tex`, `sec:r79-quantum-frontier`, `eq:r79-positive-costs`, `eq:r79-controller-parameters`; `sections/55-memory-regularization.tex`, `eq:r79-label-restart`, `thm:r79-frontier-stability`; inherited `sections/12-finite-memory.tex` and `sections/17-primitive-risk.tex`.

**Disposition:** the active structural theorem now covers nonreset fixed-model feedback and support-changing perturbations, while preserving the limitations of the original herald theorem and the stronger known-reset normal form.

### R65-17.5 — Obtain a sharp general-M noisy-qubit risk law

**Issue: a particular unresolved quantitative frontier.** The requested general-M squared-sign noisy-qubit risk law remains unresolved. R79 does not rename a total-cost frontier as that risk law. The existing exact one-/two-label formulas, strict finite-memory nonattainment, distinguishing-depth lower certificates, and prefix upper bounds remain unchanged. The separate unrestricted-decoder qubit approximation lower/upper rate gap also remains open.

The revision proves a different exact all-M robust cost frontier, including a two-label algebraic optimum with a matching converse against every allowed stochastic update. It also proves continuity of the complete general cost frontier with constants uniform in M and convergence to the unrestricted visible-history cost. These results respond to the broader demand for resource-dependent optimality without pretending to solve the originally specified qubit objective. The history-limit estimate is an explicit upper approximation bound, not a sharp rate and not a theorem that some finite M attains the limiting value.

**Locations:** retained `sections/22-boundary-memory.tex`, `thm:two-label-quantum`, `thm:qubit-boundary`, `prop:boundary-depth-gap`; `sections/26-squared-memory.tex`; `sections/51-unrestricted-approximation.tex`, `thm:r77-unrestricted-qubit`; new `sections/55-memory-regularization.tex`, `cor:r79-history-limit`; `sections/56-exact-hidden-model.tex`, `prop:r79-golden-ratio-memory`.

**Disposition:** the specified qubit-risk problem stays open. The new exact cost and stability results are stated as separate proved progress.

### R65-17.6 — Obtain a substantive external quantum or causal consequence

**Issue: applicability and mathematical significance.** The main stability theorem applies directly to arbitrary supplied finite-dimensional nonreset quantum failure instruments under the declared hypotheses. It quantifies how the optimal cost at each prescribed classical memory changes when the full primitive model family changes. Its constants do not grow with the number of controller labels. This is a control consequence about the entire resource frontier, rather than a realization of one chosen output language.

The examples include a known-instrument realization with invertible failure Kraus operators, for which the post-failure quantum state retains input information. A counted three-label controller strictly improves on the optimum over every one-label controller. The hidden-model golden-ratio family supplies exact matching values at every memory size and exposes the necessity of model-dependent supports and initial-label accounting. These are concrete consequences of the declared theory. The examples remain constructed mathematical tasks. We do not claim that they settle a separately recognized landmark open problem in quantum information or POMDP theory, or that an independent expert has judged them sufficient for the four leading general journals.

**Locations:** `sections/54-robust-instrument-frontier.tex`, `ex:r79-hidden-model-memory` and the following nonreset quantum realization; `sections/55-memory-regularization.tex`, `thm:r79-frontier-stability`; `sections/56-exact-hidden-model.tex`, `prop:r79-golden-ratio-memory`.

**Disposition:** the general control consequence is strengthened; external significance and independent assessment remain genuine further obligations.

### R65-17.7 — Strengthen effective synthesis and complexity content

**Issue: necessity versus a one-sided construction, encoded inputs, and computational limits.** The inherited finite-model fixed-memory potential system is already a necessary-and-sufficient algebraic synthesis criterion. R79 retains that result and extends the exact cost-frontier formulation to compact semialgebraic fixed-model families with polynomial or rational primitive coefficients over the real algebraic numbers and no poles on the parameter set. The formula has one outer common-controller choice, a universal model quantifier, and modelwise support/cost witnesses. It does not assume a uniform bound on unregularized continuation witnesses; the compact-parameter counterexample explains why that shortcut would be false.

For each fixed M, exact elimination determines feasibility at an algebraic cost budget, the attained algebraic optimum, and an algebraic attaining controller. The fixed-memory existence and optimization statements do not require solving an unknown residual-language problem first. The inherited reset action-cover hardness and explicit family formulas remain available. No polynomial runtime, general bit-optimal synthesis, finite-bit exact implementation of arbitrary algebraic sampling, or decidability of eventual finite saturation of the unrestricted-history optimum is asserted. Model identification from observations is also distinct from synthesis for supplied primitive data.

**Locations:** inherited `sections/12-finite-memory.tex`, `cor:memory-algebraic`; `sections/26-squared-memory.tex`; `sections/52-optimal-reset-memory.tex`, `thm:r77-reset-universality`; new `sections/54-robust-instrument-frontier.tex`, `thm:r79-quantum-frontier`, `ex:r79-unbounded-reachable-witness`; `sections/55-memory-regularization.tex`, `cor:r79-history-limit`.

**Disposition:** exact compact-model fixed-memory synthesis is extended and its support boundary is made explicit. Unbounded-memory decidability and matching computational-resource bounds remain open.

### R65-17.8 — Complete the execution record without substituting old runs

**Issue: source-bound execution evidence.** The R65 report's observation that run `38861581555` was queued at its cutoff remains a historical fact about R65. A later terminal readback belongs to that run and its exact SHA. Neither observation establishes that the current R79 source has passed a hosted workflow.

The current delivery separates the immutable mathematical source, the native build and diagnostic execution performed against that source, and any later publication commit and hosted-run readback. A local build, a source archive, an earlier pass, or a workflow configured to run is not reported as a completed current hosted success. The publication/evidence records give the actual result and SHA rather than a prospective assertion in this response. Written proofs, finite exact computations, floating probes, source authentication, LaTeX compilation, human expert review, and editorial decisions remain distinct.

**Locations:** `SOURCE_PROVENANCE.md`, `PROOF_AUDIT.md`, the current validation and publication receipts, and `START_HERE.md`. The historical R65 record remains in its preserved provenance chain.

**Disposition:** the reporting requirement is enforced. The actual current execution result is the one recorded by the source-bound receipts, not an inference from an old or pending run.

### R65-17.9 — Make the submitted mathematical dependency structure readable

**Issue: organization without loss of valid mathematics.** The central route is now: declared primitive interface; inherited support-safe certificate and proper fallback; attained compact-model cost frontier; same-label regularization; bounded-witness perturbation; uniform-in-M frontier stability; and exact resource examples. The proofs of the main current conclusions are in the main article. The new stability proof does not hide a quantum reset, uniform support-exposure assumption, or an unproved global potential bound inside an external citation.

The paired supplement retains the independent earlier developments, including the stronger preparation-face and terminal-score version of the support certificate. Historical wrappers, source manifests, reports, original proofs, and the separately compilable R58 companion remain traceable. Reordering the active center does not remove the finite-order measurement, two-stage reset, rank/discrimination, communication, spectral, geometric, or original causal results. The theorem/dependency map distinguishes mathematical prerequisites from independent preserved results and from historical evidence. A preserved report or failed pipeline attempt is not a premise of a theorem.

**Locations:** `main.tex`, `supplement.tex`; `sections/54-robust-instrument-frontier.tex`–`sections/56-exact-hidden-model.tex`; `THEOREM_MAP.md`, the current theorem/dependency map, `PRESERVATION_MAP.md`, and `START_HERE.md`.

**Disposition:** the entry and minimal proof chain are explicit, and preservation is maintained without treating the whole archive as a prerequisite.

### R65-17.10 — Keep memory and implementation resources distinct

**Issue: resource conventions and hidden initialization.** M counts live classical labels and includes the prescribed pure initial label. The command and update probabilities are fixed program data. Modelwise projections and operator potentials are offline proof variables, not extra controller registers. The quantum system is the protected physical experiment, not observer-owned coherent memory. A label restart uses a fresh current coin and an existing update row; it adds no clock, persistent seed, hidden mode, or physical reset.

With the current single constant terminal decoder, event stopping uses the live-label frontier directly, whereas state stopping requires one disjoint terminal label. The golden-ratio example shows why an uncounted random initial selection of labels cannot be added for free: two labels would then attain a different value. Program-table size, temporary arithmetic storage, exact-sampling resources, primitive/model encoding length, decoder width, and live memory continue to have different meanings.

**Locations:** `sections/54-robust-instrument-frontier.tex`, `eq:r79-controller-parameters` and the event/state-count paragraph after `thm:r79-quantum-frontier`; `sections/55-memory-regularization.tex`, `eq:r79-label-restart`; `sections/56-exact-hidden-model.tex`, `prop:r79-golden-ratio-memory` and its final initialization paragraph; inherited `sections/02-experiments.tex`, `sec:data`, and `sections/12-finite-memory.tex`.

**Disposition:** the existing resource conventions remain controlling and are tested by an exact new separation.

## 5. Responses to all forty technical comments in R65 section 18

### R65-18.1 — Fixed dictionary

The original boundary-memory theorem still fixes C. The new cost-only chain has one constant terminal decoder and optimizes command/update rows at a fixed live-memory budget. It is not a theorem about free optimization of hard dictionary width. **Locations:** `sections/22-boundary-memory.tex`, `thm:boundary-regularity`; `sections/54-robust-instrument-frontier.tex`, the controller definition and event/state-count paragraph. **Disposition:** retained scope; no dictionary convexification is introduced.

### R65-18.2 — Model-independent word probabilities

That premise remains explicit in the original heralded theorem. R79's cost/stability chain instead uses the actual completely positive continuing map and a model fixed throughout the run. It never divides by a reference word probability or replaces the current physical posterior by a reference posterior. **Locations:** `sections/22-boundary-memory.tex`, `lem:boundary-herald`, `thm:boundary-regularity`; `sections/54-robust-instrument-frontier.tex`, `eq:r79-product-map`, `eq:r79-total-cost`. **Disposition:** the old premise is preserved; the broader formulation has a different proof.

### R65-18.3 — The compulsory initial call

Every cost series begins with its n=0 term, so the initial call is included. The counted initializer in the golden-ratio example executes a real command and incurs unit cost. The history-prefix construction includes the level-zero initial label. **Locations:** `sections/54-robust-instrument-frontier.tex`, `eq:r79-total-cost`; `sections/55-memory-regularization.tex`, `cor:r79-history-limit`; `sections/56-exact-hidden-model.tex`, `prop:r79-golden-ratio-memory`. **Disposition:** the accepted convention is unchanged.

### R65-18.4 — Audit charges

A separately executed audit remains an additional physical charge. The current cost problem stops at the primitive success outcome and has a constant terminal decoder; it does not silently execute an additional free measurement. A different application with a charged terminal operation must include that operation in its specified cost model. **Locations:** `sections/54-robust-instrument-frontier.tex`, primitive-instrument definition; inherited `sections/17-primitive-risk.tex`, primitive-interface cost convention, and `supplement.tex`, `prop:compile`. **Disposition:** no audit cost is removed by the regularization.

### R65-18.5 — Least-favorable witness versus runtime model knowledge

The old least-favorable measure remains an offline dual witness. The new fixed-M formula does not assert a convex minimax saddle at a hard memory bound. Its modelwise support/potential matrices and the model pairing in the perturbation proof are also offline witnesses. The same command/update rows execute in every model. **Locations:** `sections/22-boundary-memory.tex`, `thm:boundary-regularity`; `sections/54-robust-instrument-frontier.tex`, `eq:r79-robust-budget-quantifiers`; `sections/55-memory-regularization.tex`, `thm:r79-frontier-stability`. **Disposition:** the quantifier distinction is preserved.

### R65-18.6 — Wordwise uniqueness under one attaining measure

The original stochastic determinization still requires its stated wordwise uniqueness. R79 does not generalize that proof by deleting the premise. Its cost controller remains stochastic, and its regularization adds a permitted fresh mixture to existing update rows. The inherited tied-face criteria keep their separate proofs. **Locations:** `sections/22-boundary-memory.tex`, `thm:boundary-regularity`; `sections/25-stopping-rigidity.tex`, `thm:r67-polytope`; `sections/55-memory-regularization.tex`, `thm:r79-label-restart`. **Disposition:** old closure preserved; no universal determinization claim.

### R65-18.7 — Positive masses and null histories

Positive word masses remain necessary for the old pointwise zero-slack conclusion. The current support certificate explicitly permits inaccessible labels and quantum directions. The exact unregularized potential is required only on an invariant support containing all initial states in the prescribed initial label. The compact-parameter example shows why inaccessible limits cannot be treated as positively exposed. **Locations:** `sections/22-boundary-memory.tex`, `thm:boundary-regularity`; `sections/54-robust-instrument-frontier.tex`, `lem:r79-reachable-corner`, `thm:r79-exact-certificate`, `ex:r79-unbounded-reachable-witness`. **Disposition:** null histories impose no unjustified continuation constraints.

### R65-18.8 — Residual output relation versus predictive state

The old residual right congruence remains attached to one task decision. The new reachable quantum support is yet another object: a modelwise invariant subspace used to verify cost, not an observable predictive state. Neither construction yields a common minimal predictive quotient for an arbitrary unknown-model family. **Locations:** `sections/22-boundary-memory.tex`, `thm:boundary-regularity`; `sections/A-predictive-quotient.tex`, `thm:quotient`; `sections/54-robust-instrument-frontier.tex`, `lem:r79-reachable-corner`. **Disposition:** all three meanings remain distinct.

### R65-18.9 — Event and state stopping counts

The new cost chain has a single constant terminal decoder. Its M live labels are M total labels in event stopping; the state-stopped implementation needs one disjoint terminal label and therefore M+1 total labels. The prescribed initial live label is counted in either convention. **Locations:** `sections/54-robust-instrument-frontier.tex`, event/state-count paragraph; `sections/56-exact-hidden-model.tex`, initialization discussion. **Disposition:** counts accompany the new frontier, and the older multiple-decoder conventions remain unchanged.

### R65-18.10 — Unreachable stochastic rows

Unused rows may be arbitrary, including improper rows, in an unregularized controller. The exact certificate is support-restricted. The new global witness theorem applies only after the explicitly performed label-update regularization, whose extra cost is bounded. The golden-ratio optimum has a genuinely unreachable dark label in one model. **Locations:** inherited `sections/12-finite-memory.tex`, `ex:unreachable-loop`; new `sections/54-robust-instrument-frontier.tex`, `thm:r79-exact-certificate`; `sections/55-memory-regularization.tex`, `thm:r79-label-restart`; `sections/56-exact-hidden-model.tex`. **Disposition:** no global-transience assumption is imposed on the original controller.

### R65-18.11 — Positive successors in the old determinization

The old proof still chooses only successors having positive transition probability. The new reachable-support proof uses positive sums of actual continuing images; it does not infer reachability from a syntactically available zero-probability transition. **Locations:** `sections/22-boundary-memory.tex`, proof of `thm:boundary-regularity`; inherited `sections/12-finite-memory.tex`, `lem:reachable-support`; new `sections/54-robust-instrument-frontier.tex`, `lem:r79-reachable-corner`. **Disposition:** the accepted requirement remains intact.

### R65-18.12 — Robust ties near informal determinization statements

The robust tie examples remain in the current supplement. The known-reset theorem determinizes post-report row selection only under its stated fixed-instrument hypotheses; it does not purify mixed command rows. The hidden-model example explicitly disproves an unqualified extension of that same-row conclusion. R79 regularizes stochastic rows instead of asserting their determinization. **Locations:** `sections/22-boundary-memory.tex`, `prop:boundary-ties`; `sections/53-reset-memory-frontier.tex`, `thm:r78-palette-normal-form`; `sections/54-robust-instrument-frontier.tex`, `ex:r79-hidden-model-memory`. **Disposition:** the boundary is explicit.

### R65-18.13 — Finite distinguishing depth and computability

The old H_M is not declared computable from arbitrary real primitive data. The new finite support depth concerns a supplied finite-dimensional linear continuing map; it is a different invariant. Exact synthesis additionally assumes a finite algebraic description of the primitive model family. **Locations:** `sections/22-boundary-memory.tex`, `prop:boundary-depth-gap`; `sections/54-robust-instrument-frontier.tex`, `lem:r79-reachable-corner`, `thm:r79-quantum-frontier`. **Disposition:** existential finiteness and effective encoded computation are not conflated.

### R65-18.14 — A gap certificate is not a sharp risk rate

The old distinguishing-depth bound continues to establish a positive gap only. The current uniform primitive modulus is an upper stability estimate, not a matching perturbation lower bound. The history-limit estimate is also an upper approximation bound. Only the explicitly solved golden-ratio family has the stated exact all-M values. **Locations:** `sections/22-boundary-memory.tex`, `prop:boundary-depth-gap`; `sections/55-memory-regularization.tex`, `eq:r79-uniform-modulus`, `eq:r79-history-rate`; `sections/56-exact-hidden-model.tex`. **Disposition:** sharpness is claimed only where a matching proof is supplied.

### R65-18.15 — Irrationality of the rotating-qubit phase

The existing argument using the rational-algebraic-integer obstruction is retained in the rotating-qubit proof. The new algebraic golden-ratio optimum neither replaces nor weakens it. **Locations:** `sections/22-boundary-memory.tex`, `thm:qubit-boundary`; `sections/56-exact-hidden-model.tex`, `prop:r79-golden-ratio-memory`. **Disposition:** the accepted old arithmetic argument remains unchanged.

### R65-18.16 — Excluding zero cosine

The original root-of-unity implication excluding zero cosine remains part of the qubit obstruction. No numerical sign test is substituted for that exact argument. The new finite diagnostics do not certify this universal orbit fact. **Location:** `sections/22-boundary-memory.tex`, proof of `thm:qubit-boundary`. **Disposition:** inherited closure preserved.

### R65-18.17 — Positive uncertain polarization

The old uncertain-polarization corollary retains its strictly positive lower polarization requirement. At zero polarization its uniqueness conclusion is not asserted. R79's arbitrary initial density matrices are a different cost robustness condition and do not remove the premise from the old decision-risk theorem. **Locations:** `sections/22-boundary-memory.tex`, `cor:polarization-boundary`; `sections/54-robust-instrument-frontier.tex`, initial-state quantifier. **Disposition:** no transfer of a quantifier between different objectives.

### R65-18.18 — Uniqueness in the unitary periodicity theorem

The unitary-orbit result retains uniqueness at every orbit time. The new quantum cost theorem does not rely on periodicity, a unitary orbit, or a uniquely minimizing action. **Locations:** `sections/22-boundary-memory.tex`, `cor:unitary-period`; `sections/54-robust-instrument-frontier.tex`, `thm:r79-quantum-frontier`. **Disposition:** the old hypothesis stays attached to its conclusion.

### R65-18.19 — Common limiting state and strict decision gap

Both premises remain in the contraction-based finite decision-memory theorem. The label-restart operation is not a statement that the protected physical dynamics converge to a common state. It changes classical update probabilities and obtains cost properness from the all-initial-state guarantee. **Locations:** `sections/22-boundary-memory.tex`, `prop:contractive-boundary`; `sections/55-memory-regularization.tex`, `thm:r79-label-restart`. **Disposition:** physical contraction and controller regularization are separate mechanisms.

### R65-18.20 — Contraction alone is insufficient

The depolarizing rotating-qubit counterexample is preserved. A stable cost frontier does not imply that an exact optimal decision language becomes finite-state, or that exact finite-memory attainment follows from a small physical perturbation. The new theorem controls values, not an exact optimal-memory threshold. **Locations:** `sections/22-boundary-memory.tex`, `cor:noisy-boundary`; `sections/55-memory-regularization.tex`, `thm:r79-frontier-stability` and the paragraph following its proof. **Disposition:** no false finite-attainment consequence is inferred.

### R65-18.21 — Matrix and row conventions

The old two-state calculation keeps its stated row convention. In the new general definition, a source label k contributes to destination label ell through `p^k_a u^{k,a,y}_ell Phi_{a,y}(X_k)`; the initial label is 1. The examples specify their failure updates explicitly, including the otherwise unreachable dark-label row. **Locations:** `sections/22-boundary-memory.tex`, `thm:two-label-quantum`; `sections/54-robust-instrument-frontier.tex`, `eq:r79-product-map`; `sections/56-exact-hidden-model.tex`, attainment construction. **Disposition:** transition orientation and initialization are explicit.

### R65-18.22 — Randomized terminal decisions

The old exact two-label qubit theorem still optimizes decoder expectations over the whole interval [-1,1]. Its randomization is not removed. The new cost example instead has one constant terminal decoder and permits every stochastic command/update choice in its lower bound. **Locations:** `sections/22-boundary-memory.tex`, `thm:two-label-quantum`; `sections/56-exact-hidden-model.tex`, converse in `prop:r79-golden-ratio-memory`. **Disposition:** the two different randomization classes are correctly stated.

### R65-18.23 — Degenerate endpoints

The earlier formula retains its zero-signal and phase endpoint cases. The golden-ratio converse treats zero success probability as infinite remaining cost and handles zero first-failure probability separately, so it never divides a positive mass by zero or assigns a condition to a null event. The general certificate includes singular supports rather than taking an unsupported interior limit. **Locations:** `sections/22-boundary-memory.tex`, `thm:two-label-quantum`; `sections/54-robust-instrument-frontier.tex`, `thm:r79-exact-certificate`; `sections/56-exact-hidden-model.tex`, lower-bound proof. **Disposition:** endpoints are part of the statements.

### R65-18.24 — The old numerical threshold

The threshold `q alpha > 1/3` remains confined to its specified `c=3/5` noisy-qubit family. Neither the golden-ratio constants nor the primitive stability smallness conditions redefine that threshold. **Locations:** `sections/22-boundary-memory.tex`, `thm:two-label-quantum`; `sections/55-memory-regularization.tex`, `eq:r79-stability-smallness`; `sections/56-exact-hidden-model.tex`. **Disposition:** constants retain their actual models and roles.

### R65-18.25 — The independent timing frontier

The intermediate phase-type timing frontier remains open. The exact qubit two-label risk, the full reset cost family, the current hidden-model golden-ratio cost, and the general primitive stability theorem are different questions. None supplies the missing timing curve. **Locations:** `sections/21-timing-memory.tex`, `thm:timer-frontier`; `sections/56-exact-hidden-model.tex`, `prop:r79-golden-ratio-memory`; `RESEARCH_STATUS.md`. **Disposition:** preserved as an explicit independent problem.

### R65-18.26 — Exact primitive input

The rational prefix algorithm still assumes exact rational primitives and losses. The current exact synthesis statement assumes a compact semialgebraic model set over the real algebraic numbers and polynomial/rational matrix entries with no poles on that set. Numerical optimizers or fitted empirical matrices are not used to decide exact ties or universal model constraints. **Locations:** `sections/22-boundary-memory.tex`, `thm:boundary-algorithm`; `sections/54-robust-instrument-frontier.tex`, algebraic clause of `thm:r79-quantum-frontier`. **Disposition:** exact input and learned approximation remain separate.

### R65-18.27 — Herald-rate and properness dependence

The old polynomial-precision statement retains its herald-rate lower bound. The new estimates display their dependence on c_*, c^*, and the one-row cost cap B. They are uniform in M, not independent of the physical properness margin or of all primitive dimensions/encodings. A vanishing success/properness margin can make B large. Under the stronger uniform success condition `B_a >= kappa I`, the explicit Lipschitz bound is `zeta/kappa + c^* eta/kappa^2`, and the counted prefix error is at most `C_0 (1-kappa)^T`. The scalar one-command example gives local sharpness of those Lipschitz coefficients, while sharpness at a degenerate success boundary remains a different question. **Locations:** `sections/22-boundary-memory.tex`, `thm:boundary-algorithm`; `sections/54-robust-instrument-frontier.tex`, `eq:r79-fallback-cap`; `sections/55-memory-regularization.tex`, `eq:r79-uniform-modulus`, `cor:r79-positive-success`. **Disposition:** no hidden rate-free or dimension-only cost bound; the stronger positive-success regime has its own explicit sharp dependence.

### R65-18.28 — Primitive and dictionary descriptions

Instrument coefficients, parameter-set formulas, command/report alphabets, costs, and algebraic number representations remain input descriptions. The finite-label count is not a bound on their storage. A modelwise proof witness may vary with a hidden parameter without becoming runtime information. **Locations:** `sections/54-robust-instrument-frontier.tex`, `eq:r79-controller-parameters`, `eq:r79-robust-budget-quantifiers`, and the exact-synthesis hypotheses; inherited `sections/C-scope.tex`. **Disposition:** live-label and program/input resources remain distinct.

### R65-18.29 — Dense superoperator arithmetic

The original rational-channel bound retains its dense Hermitian-coordinate interpretation. The general supported quantum formulation uses actual matrix/superoperator coordinates and does not import the reset-specific s-dimensional scalar reduction. Neither finite support depth nor the new uniform-in-M stability constant is an arithmetic-complexity bound for a general synthesis instance. **Locations:** `sections/22-boundary-memory.tex`, `thm:boundary-algorithm`; `sections/53-reset-memory-frontier.tex`, `thm:r78-reset-frontier`; `sections/54-robust-instrument-frontier.tex`, `eq:r79-product-map`. **Disposition:** representation costs are not silently reduced.

### R65-18.30 — Program table, temporary storage, and sampling

The exact procedure may require large transition tables, algebraic arithmetic, and substantial temporary storage. Its output is a controller with specified algebraic probabilities; this is not a finite-bit exact-sampler theorem. The regularization needs one fresh current coin, not a retained random seed, and preserves the live-label bound only. **Locations:** `sections/54-robust-instrument-frontier.tex`, final synthesis qualifications; `sections/55-memory-regularization.tex`, implementation of `eq:r79-label-restart`; inherited `sections/12-finite-memory.tex`, `cor:memory-algebraic`, and `sections/C-scope.tex`. **Disposition:** no identification of these resources.

### R65-18.31 — Meaning of finite verification

The written quantified proofs are the mathematical arguments. Exact arithmetic checks test finite instances and identities; floating probes test their stated approximations; compilation checks the native assembly. Internal author-team AI challenges are identified as such. None is formal proof, independent human refereeing, a priority certificate, or a journal decision. **Locations:** `PROOF_AUDIT.md`, diagnostic scripts and actual execution receipts, `LITERATURE_AND_PRIORITY.md`. **Disposition:** every evidence category keeps its actual meaning.

### R65-18.32 — The queued R65 workflow

The old queued-at-cutoff observation is retained with its original run and SHA. Any later completed result is historical evidence for that exact object. Current R79 hosted status must be read back for the actual current commit and cannot be inferred from it. **Locations:** preserved R65 provenance, `SOURCE_PROVENANCE.md`, current publication/validation receipts. **Disposition:** no absent, pending, failed, old, or mismatched run is called a successful current run.

### R65-18.33 — Paired native cross-references

The main and current technical supplement are one paired native mathematical submission and are built with their corresponding cross-document auxiliary references. The theorem map uses current compiled locators. The complete R58 companion remains a separately compiled document. **Locations:** `main.tex`, `supplement.tex`, `THEOREM_MAP.md`, current build receipts, and `companion-r58/main.tex`. **Disposition:** old PDF numbering does not substitute for current paired references.

### R65-18.34 — Preservation is not independent re-review

The predecessor source, reports, wrappers, mathematical bodies, and independent companion remain traceable through exact preservation mappings. Accepted inherited results are not reopened without a concrete defect. Their preservation does not claim that every archived proof has undergone a new independent review, or that a previous report approved a new statement. **Locations:** `PRESERVATION_MAP.md`, `SOURCE_PROVENANCE.md`, preserved `inputs/` and historical corpus. **Disposition:** source continuity and mathematical assessment remain different facts.

### R65-18.35 — Actual audit coverage

The new provenance records distinguish ref enumeration, exact commit/tree identity, source reconstruction, body retrieval, file hashes, lexical historical indexing, candidate-report classification, and mathematical scrutiny. The author-side review-ref census and the historical corpus authentication are evidence at those stated levels. They do not become a claim of exhaustive independent mathematical review. **Locations:** `SOURCE_PROVENANCE.md`, current census/classification records, and `PROOF_AUDIT.md`. **Disposition:** the actual coverage and any failed intermediate attempts are stated rather than replaced by a branch-name claim.

### R65-18.36 — Bounded-score comparison versus unbounded duration

The new cost proof does not derive an expected duration from total variation of a stopped record. Positive expected call cost bounds the survival series; supported or regularized Lyapunov potentials then control actual total cost. In the history-limit argument, the small survival probability multiplies the cost of an actual all-state fallback; it is not used to claim a uniform vanishing tail for the original unbounded cost. **Locations:** `sections/54-robust-instrument-frontier.tex`, proof of `thm:r79-exact-certificate`; `sections/55-memory-regularization.tex`, `thm:r79-label-restart`, `cor:r79-history-limit`; inherited `supplement.tex`, `prop:tail`. **Disposition:** the old tail warning remains load-bearing.

### R65-18.37 — Hard width and nonconvex controller classes

The parameter product of stochastic rows is compact, but its robust infinite-horizon objective need not be convex. The new attainment proof uses lower semicontinuity, not an unjustified convex minimax theorem. The label-restart operation modifies one controller's existing rows; it does not grant a free persistent choice between two programs. The old hard-width dual gap remains valid. **Locations:** `sections/20-primal-dual.tex`, `prop:width-dual-gap`; `sections/54-robust-instrument-frontier.tex`, proof of `thm:r79-quantum-frontier`; `sections/55-memory-regularization.tex`, `eq:r79-label-restart`. **Disposition:** hard resource constraints are respected.

### R65-18.38 — Sparse dual atoms and other witness sizes

The earlier `k_T+1` support count concerns dual physical witnesses, not live controller labels. The new block potentials and support projections are also proof certificates. A finite support construction or a bounded potential does not mean that the controller observes or stores its entries. **Locations:** `sections/20-primal-dual.tex`, `thm:sparse-witness`; `sections/54-robust-instrument-frontier.tex`, `eq:r79-robust-budget-quantifiers`; `sections/55-memory-regularization.tex`, `eq:r79-global-witness`. **Disposition:** none of these analytic sizes is reclassified as operational memory.

### R65-18.39 — Protected quantum state and the declared observation port

The device observes its sampled command and the declared report/success, not the protected state, a hidden model index, an unreported cost suboutcome, or a future audit. Label restart leaves the physical state unchanged. The primitive discrepancy is defined on the declared finite physical space and normalized output instrument; no free external entangled register or observer-owned quantum memory is added. **Locations:** `sections/54-robust-instrument-frontier.tex`, primitive/interface definition; `sections/55-memory-regularization.tex`, `eq:r79-label-restart`, `eq:r79-instrument-distance`. **Disposition:** no hidden observation or reset resource.

### R65-18.40 — Open scope

Previously proved tied-face, nonreset certificate, reset-frontier, and exact example results remain at their scopes. R79 adds same-memory regularization and uniform primitive stability, but does not close the original general-M squared-sign risk, sharp unrestricted qubit approximation rate, intermediate timing curve, arbitrary optional-commitment control, general intrinsic necessity for the causal-transfer certificates, a common unknown-model predictive quotient, or the decision whether unrestricted cost saturates at some finite M. Independent A1/A2/B4/C2/Theta goals and human priority assessment remain separate. **Locations:** `RESEARCH_STATUS.md`, `sections/55-memory-regularization.tex`, final scope paragraphs, and the historical crosswalk below. **Disposition:** open problems are refined by proved progress rather than silently erased.

## 6. Historical reports and remaining obligations

### 6.1 R59 round three: causal-transfer geometry and common models

The R59 round-three report at `c39922c242f9bd03d2e0d7f05d6e9b483362e26d` remains applicable to the inherited actual-history transfer route. It accepted the displayed theorem at its certificate hypotheses and asked for an intrinsic or near-necessary primitive characterization, a natural external consequence, careful comparison with statistical experiment order and rejection/selection theory, and stronger computational information.

The new fixed-memory cost stability theorem does not make the lower/upper certificates of `thm:transfer` automatic. An exact potential system for a supplied time-homogeneous controller is also not a universal common predictive quotient. The former is retained at `sections/03-main-theorem.tex`, `thm:transfer`, with its proof in `sections/04-proof.tex`; the latter remains fixed-law at `sections/A-predictive-quotient.tex`, `thm:quotient`. The new same-model quantifiers and primitive stability address a different, explicit controller question. The literature comparison and finite-description conventions remain in the native references and priority ledger. Effective construction is not identified with optimal complexity.

**Continuing obligations:** general necessity for the geometric transfer certificates; a general unknown-model predictive quotient; recognized natural external consequences; matching computational lower bounds; and the independent realization/geometry programme. The stability of the present quantum cost frontier is not declared a solution of those other problems.

### 6.2 R64: boundary attainment, complete stopped laws, duality, and timing

The R64 report at `0a66ca2ede7835ede2a62fe2363ba5dd3ccd2ed8` accepted the boundary-attainment and complete performed-law chain while identifying scope and contribution limitations. Its accepted results remain in `sections/20-primal-dual.tex`: `thm:boundary-attainment`, `cor:resource-price`, `thm:complete-stopped-order`, `thm:sparse-witness`, `prop:dual-bellman`, `thm:multi-resource`, and `prop:width-dual-gap`.

R79's history-limit corollary concerns convergence of optimal **total cost** with increasing memory. It does not imply that a full-history constrained-risk optimum can be approximated at every exact boundary budget with the same finite labels. The earlier same-budget fallback arguments keep their required slack unless a separate boundary theorem removes it. Likewise, primitive stability of cost does not replace complete bounded-score comparison, and neither gives an unbounded waiting-time comparison by total variation alone.

The delayed-release theorem remains at `sections/21-timing-memory.tex`, `thm:timer-frontier`. Its exact unrestricted curve, one-label curve, threshold, and pumping gap are preserved. Its intermediate phase-type curve remains unresolved. The new golden-ratio frontier has a different task, observation law, and objective; it is not relabeled as that timing solution.

### 6.3 Original v94/R62 and the preceding R61 chain

The original-paper controlling report is `GENERAL_THETA_FOUNDATIONS_I_V94_INDEPENDENT_REFEREE_REPORT_R62.md` at commit `58581d5a6391642fb0849f8c8bb49c8c0c20b63c`, blob `232a7c9e2c7397acb171df115d5ea1f1792ecbfc`, SHA-256 `e03df5d0b8a5ddbd4b9d2f889435ce71477710b1291a2d35326fb5a260958b29`. It reviewed the v94 source/publication/final-review objects identified in the preserved report. Its fifteen required revisions and twenty-two detailed comments, and the preceding R61 report's eighteen required revisions and thirty detailed comments, received itemized author responses in v96 source commit `d19a424f19ab5c1492b621a55bb3c8a20de7392d`, path `papers/GTF-I-v96-referee-resolution/RESPONSE_TO_REFEREE.md`, blob `8214ebcf78d0092aac2880875d7d6ee9bc662dfb`, SHA-256 `122a9375575ff07c60bc46229a50d6c1f96c32517a20e4740cbc28f72b579068`.

The preceding R61 report and its separate proof/pipeline audit remain pinned at `df919e7a2d917d71f5525d2034f524b97809121b` and `a5b01294ce8fe7d4ca3782f762fba71f0cd44509`. The apparent v96/R63 review ref that adds no report is not a later independent assessment. An author response can resolve a proof or organizational obligation without being an independent endorsement of the paper.

The following crosswalk retains every original R62 required-revision category and its continuing limits:

| Original R62 items | Preserved resolution and current boundary |
|---|---|
| R01, R10, R11, R15; D01, D19 | Source, publication, review-object, metadata, and reading-route identities remain separate. Current source identity and native execution have current receipts. An incomplete source transfer or an old PDF is not selected merely because its version number is large. |
| R02, R03; D02 | The arbitrary-experiment two-call variational/dual principles, special shared-latent-basis exact formulas, and independent local geometry remain distinct mathematical families. R79 continues the original paper and preserves all valid bodies; it does not replace that identity with the new cost-only example. |
| R04; D11, D12 | The Heisenberg postponement/no-message reduction retains its actual old-register and fresh-reference bounds. Labelwise continuation concavity remains the uniform criterion with its stated binary witness. It does not bypass a smaller old-memory cap or imply strict gain at every prescribed initial state. |
| R05; D03–D10 | The rank-capped majorant, boundary-safe functional, secular root, active ties, and water-map properties retain their exact statements. Rank means at most; zero signal, rank one, support saturation, strict-Schur qualifications, optimizer nonuniqueness, and trace/Bayes factors stay explicit. |
| R06, R07; D18 | Gram weights are not hypothesis-dependent path probabilities. The support-pseudoinverse instrument, complement completion, first-acquisition preservation, finite-atom bounds, and countable positive-tail control remain at their proved hypotheses. |
| R08; D13–D17 | The theorem-level priority comparison distinguishes reset cuts, feasible sets, objectives, saturation, equal/biased priors, and a latent basis selected once and reused. Finite instrument existence is not efficient hardware design, circuit synthesis, tomography, or device-independent calibration. |
| R09; earlier R61 R13 and pipeline P5 | Independent human specialist priority assessment remains unfulfilled. Search, chronology, author-team AI checking, compilation, and stronger theorems do not supply it. The current response makes no firstness claim beyond the precise mathematical assertions and checked antecedents. |
| R12; D20, D21 | Written proofs, finite computations, native reconstruction, human signatures, and independent endorsement remain different evidence. Commit/tree identity authenticates repository content, not a human signature or mathematical approval. |
| R13; D22 | No arbitrary-pair closed value, arbitrary-horizon exact memory classification, global ordered-POVM geometry, uniform changing-support geometric theorem, or A1/A2/B4/C2/Theta completion follows from the scoped exact formulas or R79 cost stability. |
| R14 | The explicit prescribed-spectrum `d=3, r=2` finite-basis/two-outcome example and its communicated/no-message values remain preserved. Its rational weights and algebraic vectors/values retain their exact distinction. It remains an example rather than a permanent restriction of subsequent general theorems. |

R62 accepted the fixed-spectrum converse and value, rank-constrained filtered-swap optimization, rank-capped concave envelope, finite first-acquisition-preserving attainment map, and initial-face rigidity results at their stated hypotheses. Those results are inherited. The open issues concern their broader generalization, priority, organization, and intrinsic significance, not a newly invented rejection of their correctness.

## 7. Exact limits of this response and the current submission

The following distinctions remain part of the mathematical submission:

- The new primitive modulus is uniform in the controller memory budget, but its square-root exponent at support degeneracies is not proved optimal. The separate uniformly positive-success Lipschitz estimate has locally sharp scalar coefficients at its specified cost and success bounds.
- Exact synthesis is for a prescribed finite M and an explicitly encoded primitive family. It does not decide whether some finite M reaches the unrestricted-history optimum.
- The history-limit theorem proves convergence with counted finite implementations. It does not prove finite saturation, a sharp memory rate, or same-budget approximation of every distinct constrained terminal-risk problem.
- The optional-commitment, original squared-sign qubit risk, unrestricted qubit approximation-rate gap, intermediate phase-type timing, general causal-transfer necessity, and unknown-model predictive-quotient questions remain at their recorded scopes.
- The all-initial-state quantifier is essential to the current label-restart proof. A restricted preparation set cannot silently be enlarged to its whole support face or used as though it contained every post-restart physical state.
- Original finite-order measurement, two-stage reset, memory/communication, rank/discrimination, variational/dual, spectral/geometric, and independent companion results remain preserved. The new center neither deletes them nor makes all of them hidden prerequisites.
- The four-journal objective is unchanged. The report's significance objection receives a mathematical response through the new same-memory stability mechanism and its consequences; the authors do not pronounce the editorial question closed.

## 8. Current independent-reading route and evidence

Begin with `START_HERE.md`, the current main article, and the paired technical supplement. For the new mathematical contribution, read the inherited/source-attribution paragraph with the cost-certificate assembly, then `thm:r79-label-restart`, `lem:r79-centered-perturbation`, `thm:r79-frontier-stability`, and `prop:r79-golden-ratio-memory`. `cor:r79-history-limit` relates the complete finite-memory frontier to unrestricted visible history without claiming finite saturation; `cor:r79-positive-success` records the sharper positive-success stability and prefix estimates with their scalar sharpness check.

The theorem map and dependency ledger give current compiled numbers, hypotheses, and source locations. `PRESERVATION_MAP.md` identifies the immediate predecessor and the recursive original-content chain. `SOURCE_PROVENANCE.md` fixes the manuscript/review identities and actual historical-audit coverage. `PROOF_AUDIT.md` identifies the author-side proof challenges, including the discovery and explicit attribution of the already inherited support-certificate and algebraic-synthesis results. Current validation and publication receipts state the actual native build, exact and floating diagnostic counts, source hashes, remote commit identity, and any hosted-run readback.

The present response offers the strengthened complete mathematics for the next independent referee. Neither the response itself nor the associated finite verification supplies an independent human report, exhaustive priority clearance, or an editorial decision.
