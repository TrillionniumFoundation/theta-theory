# Response to the tenth-revision independent referee report

**Manuscript:** General Theta Foundations I: Causal Experiments, Predictive Quotients, and Resource-Aware Reduction  
**Author:** Qian Qi  
**Revision:** eleventh resource-comparison revision, 23 September 2026  
**Controlling report:** `8e44610a9826b799f190639cec80c0435f14487c`  
**Reviewed predecessor:** `4507bd5b6e61206d0d82c9f52fcbe279585ce1c7`  
**Report path:** `reviews/general-theta-foundations-i-v10-marked-duality-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`

We have treated the report's central request as a request for mathematics, rather than another collection of local qualifications. The new article is organized around the executable cost of comparison and its cancellation for complete retained states. All predecessor mathematical bodies remain in the complete development, and the entire v10 canonical mathematical core remains in the canonical article. We do not ask the referee to regard compilation, finite checks, manifests, or the author's own response as independent verification of a theorem.

## E10.1 — A genuinely resource-aware comparison theorem

**Revision:** `resource-comparison.tex`, Definition `def:v11-simulator`, Theorem `thm:v11-comparison`, Corollary `cor:v11-frontier`, and Theorem `thm:v11-fusion`.

A primitive simulator now has an explicit persistent register of sizes K_t and a separately charged independent public seed of size r. It is a parameter- and task-independent causal machine, not an abstract assertion that a simulation exists. Its error preserves the actual marked feedback law, including the independent randomization used by an output strategy. The same simulator must serve all decision rows.

The source implementation of a target S_t-state, q-seed consumer retains the reachable pairs of its own and the simulator's states. Thus it has width at most K_t S_t and seed size rq, and a uniform row-risk error at most epsilon. We prove the associated upper-risk inclusion, lower-support inequality, composition law, deficiency-frontier triangle inequality, and decision-witness lower bound. The centered spectrum has an explicitly stated baseline comparison; no parameter oracle or timing change is inserted into the baseline. Constant-cost two-sided simulations preserve a power exponent only in the fixed-horizon constant-factor regime.

This deliberately builds on, and cites, the earlier abstract spectrum transport theorem rather than claiming that theorem afresh. The additional structural result is **complete-state fusion**. When the consumer already determines the marked continuation class, the class component of the reverse transducer can be recovered from the consumer's old register. Its synthetic report is consumed within the step, and the new register again determines the new class. This gives equality of complete-consumer risk bodies at exactly the same widths and seed signature on the original and quotient experiments. For general consumers the K_t S_t charge remains.

The repeated-report example proves that this distinction is real and sharp. At intermediate width s, one presentation permits zero classification error while the other has optimal error 1-s/k, despite exact marked full-history equivalence. Its exact repeat simulator needs k persistent states. This gives one organizing statement joining simulation, the risk invariant, the operational quotient, and memory cost.

**Boundary:** support inequalities characterize closed convex upper risk sets, not the existence of a simulator of a prescribed cost. We do not assert an unproved constrained inverse randomization theorem.

## E10.2 — Broaden the nonfinite theorem beyond product domination

**Revision:** `conditional-duality.tex`, especially Theorem `thm:v11-conditional`.

We take the constructive extension route. A physical covariate X is displayed afresh at each checkpoint. Conditional innovation loss effects are dominated by one reference for X and a product reference for the innovations. The full report path need not have a product dominating measure: a nonatomic covariate repeatedly displayed at two times already yields a diagonal singular law.

At fixed x the private innovation policy space is the compact space from v10. Its conditional risk integrands belong to L1(nu;C(K_S)). We give the representation and compactness proof for probability kernels Lambda_x on that policy space, using positive normalized functionals, a countable lattice, Radon–Nikodym representatives and the Riesz theorem. We then prove uniform risk continuity over the compact row family, executable realization with one independent public uniform seed, compact convexity, support-function minimization by a measurable private section, and attained common-encoder minimax duality.

This is not a finite partition approximation of X. Its arbitrary measurable dependence survives the compactification, and its public seed is independent of X and the source. The source's physical display of X is part of the stated interface, not an uncharged private observation tape. If X is no longer displayed, those policies are not admissible. The article makes this distinction explicit and retains the v10 product-dominated theorem with its hypotheses visible in the abstract and introduction.

**Boundary:** this extension is a concrete singular finite-horizon class. It is not a proof of weak closure for every standard-Borel filtered information structure, and it does not assert compactness of the entire private body in the new conditional model.

## E10.3 — Connect task-specific compression to universal marked minimality

**Revision:** `task-completion.tex`, Theorem `thm:v11-taskcover`, the prediction-completion corollary, and Theorem `thm:v11-causal-tasks`.

For a declared finite family with conditional loss table L_d(h,a), let A_d(h) be the nonempty set of Bayes-optimal actions. A set C of histories is compatible when the intersection of A_d(h) over h in C is nonempty for every task d. We prove that the smallest exact restart width is the minimum number of compatible sets covering the histories. This holds for arbitrary privately randomized encoders and for independent public randomization: zero total excess forces every message's support to be compatible. Conversely a compatible cover supplies deterministic labels and task-dependent optimal decisions.

This description is genuinely task dependent. The common width can be one while the marked quotient is arbitrarily large. Compatibility is not silently treated as an equivalence relation; even pairwise compatibility need not imply joint compatibility. We give the three-set counterexample and elementary quantitative upper/lower bounds.

For Brier predictions, unique optima turn compatibility into equality of the probability-feature vector. Completing the family under all marked continuation-event predictions recovers the v10 marked quotient, with a finite pair-separating family when the instrument is finite. For exact causal prediction under strictly positive report probabilities, a backward right-congruence closure gives the coordinatewise least width profile. The proof treats support overlap of randomized registers explicitly.

**Boundary:** an optimal checkpoint cover need not be sequentially implementable at its checkpoint minima. We do not conflate that theorem with the causal positive-report theorem. The latter's strict-positivity assumption and the separate universal support-aware v10 theorem are both stated.

## E10.4 — A difficult historical model-specific consumer

**Revision:** `hard-sphere-core.tex`, Lemma `lem:v11-flow`, Theorems `thm:v11-core` and `thm:v11-physical-transfer`, and Corollary `cor:v11-physical-duality`.

We return to the exact microscopic hard-sphere object in the historical B4 source, rather than adding another finite positive model. The physical phase space has unbounded velocities; a summably weighted family of finite particle sectors is also allowed. The almost-everywhere hard-sphere flow supplies a strongly continuous isometric group on weighted symmetric Lp, 1<=p<infinity. The periodic adaptation and the precise classical flow input are recorded.

Orbit convolution gives a collision-compatible graph core for its unbounded transport generator. We prove all generator-derivative formulas and bounds, construct one diagonal graph-convergent sequence from smooth interior finite-sector observables, and establish specular trace agreement in local collision-flux charts. No smoothness across grazing configurations is inferred. This is an actual microscopic operator-domain result.

We then verify a GTF consumer with these physical observables. Gaussian noisy acquisitions, whose control selects an observable but does not alter the microscopic dynamics, admit identity report simulators in both directions. A conditional coupling, followed by a sum over control choices and Holder's inequality against the invariant measure, gives an explicit Lp error bound uniform over all memory widths and feedback designs. Actual marks are coupled through the same microscopic state. Thus graph-core approximation transfers every common-encoder risk body and its centered spectrum. A compact family of preparation densities also verifies, rather than assumes, the dominated duality hypotheses.

**What this discharges:** a collision-compatible microscopic graph-domain/acquisition approximation in a stated weighted Lp topology. The resulting width-uniform decision theorem genuinely uses the resource-comparison theorem.

**What it does not yet discharge:** the historical B4 corrector requires local uniform convergence on kinetic action sublevels, BBGKY hierarchy control and a joint microscopic/kinetic limit. The old proof sketch additionally relies on B2 factorial/recollision estimates and B3 control-transfer inputs. The new Lp theorem is not identified with those stronger conclusions. In particular no sector-uniform exponential estimate, nonlinear kinetic range theorem, or unrestricted historical B4 closure is claimed. Accordingly E10.4 is materially advanced, but its strongest interpretation—completion of a formerly open full historical kinetic target—is not reported as closed.

The historical nonlinear resolvent line is also examined. We prove the proper implicit resolvent identity under its explicit resolvent hypothesis, rather than reusing a linear resolvent identity for nonlinear maps. The old source is preserved, not silently rewritten.

## E10.5 — Nearest-neighbour theorem comparison

**Revision:** `LITERATURE_COMPARISON.md`, and the antecedent discussion in `introduction.tex`.

The comparison now identifies the specific original statements being used or distinguished: Saldi's policy-topology Theorems 6, 7 and 9; Yüksel–Saldi's strategic-measure representation and closure discussion; Nayyar–Mahajan–Teneketzis's common-information Theorem 3 and no-shared-memory Corollary 5; Kiefer's continuation-span Proposition 2.1 and equivalence Theorem 2.3; classical zero-error graph coloring; and the physical hard-sphere flow and nonlinear-resolvent literature. We explicitly subtract convex separation, weak-star existence, conditional probability-kernel compactness, offline common-information dynamic programming, linear automata equivalence, orbit smoothing and graph coloring from any novelty claim.

What remains for assessment is the resource-sensitive connection: explicit machine cost in marked comparison; exact cancellation of class memory for complete consumers; the task-cover/prediction-completion link to that cancellation; and width-uniform microscopic acquisition comparison. We do not argue that a list of classical ingredients automatically reaches a top-four novelty threshold.

**Unfinished priority boundary:** the original full text of Norberg's 2002 filtered-experiment paper was not obtained. Its bibliographic identity and relevance are recorded, but its hypotheses and proofs are not invented. Consequently this response does not claim complete proof-level exclusion against all nearest neighbours. This remaining audit item is visible, rather than replaced by an unsupported originality claim.

## E10.6 — Logical status of A2 and the eleven-component architecture

**Revision:** `PIPELINE_GRAPH.json` and `HISTORY_AUDIT.md`.

The program is represented as a typed dependency graph. A theorem implication, a verified protocol adapter, a model-scoped consumer, and a conditional interface are different edge types. The primary A2 algebraic-geometric chain is an independent branch, not a consequence of GTF obtained from numbering or naming.

The observed A2 v127 head is frozen at `d6c730f8caff71ddbc8208c0bd00cb90138de85a`. Its geometry entry was read directly; it imports the boundary-atlas, depth, polarization, corank and Rees/nilpotent developments, and does not import the GTF source. This source observation is not a re-refereeing of every primary A2 proof. The older verified Poisson/contact acquisition adapter is retained with its narrower hypotheses, without relabeling it a proof of the independent primary chain.

For B4 the remaining-work description now says explicitly that range, dissipativity and kinetic core questions refer to the historical infinite-dimensional nonlinear target. The already proved finite-dimensional v10 Nisio theorem is not incorrectly listed as unfinished.

## E10.7 — Article architecture without arbitrary deletion

We add the requested unifying theorem rather than deleting mathematical sections. The canonical article begins with the resource-costed comparison and complete-state fusion, then develops the compact risk realization, task interpretation, positive-state synthesis and consumers. All of the v10 canonical mathematical core remains. The complete-development view additionally preserves all predecessor bodies and introductions, including the v10 introduction as a historical document. Its old assumptions remain local to its old statements; historical text is not promoted into a premise of the new theorem.

The manuscript's prose separates theorem hypotheses and conclusions from repository/build governance. The latter resides in this response and the evidence files. This preserves the full scientific material while making the structural thesis explicit.

## Additional numbered technical comments

**11.1 Product domination in positioning.** The abstract and introduction explicitly name product-dominated finite-horizon loss effects for the v10 theorem and separately state the new singular displayed-covariate class.

**11.2 Exact public versus finite stored randomness.** The main definition distinguishes q=1, finite q and an ideal uniform seed. Proposition `prop:v11-seed` proves exact qS storage conversion and the approximate (N(J,h)+1)S cost; no finite seed is inferred without paying its index.

**11.3 Reverse simulation multiplier.** K_t S_t is now part of the main comparison theorem and its support/spectrum consequences. The complete-state fusion theorem states the precise additional condition under which it cancels.

**11.4 Universal versus task minimality.** The compatible-cover and Brier-completion results answer this distinction directly, with strict support/timing qualifications.

**11.5 Median index.** The new local copy of `common-membership.tex` first chooses d for which p_d is a median and then applies the task-d affine argument. The predecessor source is unchanged.

**11.6 B4 ledger.** The historical infinite-dimensional nonlinear target is now explicitly distinguished from the finite-dimensional result already proved in v10 and from the new microscopic linear Lp graph core.

**11.7 Pipeline checks.** `verify_pipeline.py` checks source identities, graph declarations and label existence. It does not prove any semantic edge or downstream hypothesis.

**11.8 Build/test evidence.** Both manuscript views are compiled from hash-pinned sources. Normal and optimized finite diagnostics, designated negative controls and predecessor suites are rerun. Their receipt describes reproducibility, not analytic proof certification.

## Requested reconsideration

The revision supplies new theorem–proof content answering the structural comparison, task-compression, singular compactness and computational requests while retaining the previous results. It also advances the genuine microscopic B4 domain/acquisition question. We submit those proofs for independent examination. The stronger historical kinetic closure and the unretrieved filtered-experiment priority comparison remain explicitly identifiable review items; neither is marked solved merely because this revision has a new version number.
