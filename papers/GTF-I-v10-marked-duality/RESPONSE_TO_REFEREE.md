# Response to the ninth General Theta Foundations I report

**Controlling report:** `e5373d129545b269ee4f5477a94542517dbfd0d1`, `reviews/general-theta-foundations-i-v9-causal-minimax-harsh-referee-2026-09-23/REFEREE_REPORT.md`.

**Reviewed predecessor:** `71d5fa4c5d8b6d6f0f3d5c61aba07cedd342373a`; source-bound mathematical commit `6bcd0de01f7d164a8feab28f82d44f6149ba385f`.

We thank the referee for distinguishing the genuine v9 advances from the remaining questions. This revision takes the strengthening route: it adds a nonfinite common-encoder theorem, an operationally minimal marked state, constructive synthesis and proved model consequences. It does not replace the article by a shorter finite-only paper. The full previous mathematical development remains available, with the two presentation corrections identified below.

## E9.1. Preserve the actual hidden target

**Change:** `marked-quotients.tex`, Definition `def:v10-continuation`, Theorem `thm:v10-reconstruction`, Example `ex:v10-xor`; local correction in `report-saturation.tex`.

The objection is correct. The old posterior-plus-report key does not preserve arbitrary latent decision marks. In the referee's binary experiment, the parameter posterior remains constant but the target is `W=Y xor theta`; forgetting Y changes the optimal classification error from 1/10 to 1/2. The example is now worked through explicitly, and the finite verifier retains the exact rational regression.

The new equivalence compares the conditional law of `(theta, future reports, W)` under every future control word. At the terminal time it preserves the joint posterior of theta and W. A backward conditional-law argument proves controlled successor compatibility. The reverse kernel, conditional on the old and new classes, is independent of theta: the parameter likelihood ratio is constant on each successor fibre and cancels. The proof multiplies this kernel by the class transition and the terminal marked kernel to recover the original joint report–target law, before inserting feedback factors. It does not generate an independent target with the same marginal.

The original v9 report-only result is retained in a local copy under the title “Minimal posterior-and-report-predictive coordinates.” Its simulation assertion now says **parameterized report experiments**, and its proof and labels are preserved. The new marked theorem strengthens the article rather than merely restricting its subject. Original source bytes are untouched.

## E9.2. An operational necessity theorem, including randomized statistics

**Change:** Theorem `thm:v10-minimal`, Proposition `prop:v10-overlap`.

The new definition asks for equality of Bayes risks, not for the storage of specified coordinates. At each checkpoint, a restart preparation selects any supported actual history and runs its conditional continuation. The statistic must consume that history. Each test predicts a future marked event under a fixed continuation control word, using squared loss before observing the continuation.

The exact excess is the conditional variance of the full-history event probability given the statistic. Requiring zero excess for every preparation and event forces every retained label to have support within one continuation class. Thus **every privately randomized source-consuming statistic** needs at least `K_t` labels. The canonical deterministic quotient attains all these widths simultaneously. With a public seed the recovery criterion is from `(seed, register)`, not from the register alone; conditioning the nonnegative zero-excess identities on the seed gives the same exact-width lower bound. A one-time-pad relabeling therefore is not a counterexample to the statement as written.

The comparison category is explicit. This is not minimality among independent resimulators with unpriced histories, nor among statistics for an arbitrarily small task list. It is a necessity theorem for a decision-complete family of the specified marked continuation experiment. A quantitative two-history lower bound also measures the penalty when a randomized state overlaps two distinguishable classes.

## E9.3. Nonfinite compact common-encoder duality

**Change:** `dominated-duality.tex`, Theorem `thm:v10-compact`, Corollaries `cor:v10-effects`, `cor:v10-countable`, `cor:v10-seeds`, Theorem `thm:v10-approximation`.

The new theorem admits standard Borel report spaces, a compact parameter/row set and every measurable finite-state encoder kernel. Controls, individual decision alphabets and the horizon are finite. Loss effects have a dominated `L1` representation continuous in the row. The theorem is not proved by enumerating deterministic designs.

Each encoder row is a weak-star simplex in `L-infinity`. Compactness and metrizability are proved. Because one encoder factor occurs in each report-time coordinate, tensor testing gives continuity against a full path `L1` effect; compactness of the effect family makes it uniform in the decision row. This yields a continuous risk map into `C(J)`. Increasing finite partitions give jointly measurable representatives of the weak-star classes, so a probability on the design space is an executable public seed, not merely an abstract relaxation.

The barycenter risk set is compact and convex; adding the positive cone gives a closed upper set. Positive separation identifies its supports with probability measures on J. Convex minimax then gives exact duality and attainment. The private attainable set is compact but generally nonconvex; it is not replaced by the public convexification.

Countably many tasks have an attained primal and a supremum over finitely supported dual weights, with no false dual attainment or universal finite seed bound. For compact rows a row-covering modulus gives an explicit finite-mixture approximation and charges the stored mixture index at every checkpoint, including initialization. Dyadic randomization has its own approximation cost.

Finally, finite report partitions approximate the actual joint marked laws uniformly in all widths and controllers. The bound follows by causal report simulation and the finite control-path expansion, not by postulating a uniform encoder approximation. Continuous Gaussian hidden Markov models verify the hypotheses from their primitives. The effect-only corollary also treats actual targets without a common dominating target measure, when their specified loss effects are dominated.

The hypotheses exclude some singular repeated-observation laws and do not assert arbitrary infinite-horizon compactness. These are explicit hypotheses of the stronger theorem, not an unannounced change in the v9 finite result.

## E9.4. Isolate classical ingredients and the claimed contribution

**Change:** introduction and `LITERATURE_COMPARISON.md`.

The proof-level comparisons now include Saldi's weak-star policy topology and existence theorems; Yüksel–Saldi's strategic-measure convexification, private nonconvexity and nonclosure examples; Yüksel's real-time partial-observation coding reductions; the common-information coordinator results of Nayyar–Mahajan–Teneketzis; and Kiefer's weighted-automaton span/equivalence construction. The application mechanisms are explicitly attributed to positive-matrix filtering, Nisio's control semigroup and Bäuerle–Rieder's risk-sensitive information state. These ingredients are not relabeled as new theorems of this program.

The contribution submitted for judgment is the coupled, bounded-register risk-function theorem with executable weak-star representatives and width-uniform marked approximation, together with the operational marked quotient and the synthesis/application consequences. The article does not infer originality from a newly assembled list of topics.

A limitation of the audit is recorded rather than hidden: the complete original texts of Norberg (2002) and Witsenhausen (1979) were not both available for a fresh full proof audit. The accessible modern author text gives Witsenhausen's statement and related proofs, and the filtered-experiment antecedent is acknowledged. We do **not** declare exhaustive priority exclusion proved. Journal-level novelty remains a matter for independent comparison and referee judgment; successful source verification cannot decide it.

## E9.5. Actual model consumers

**Change:** `model-consumers.tex`; `PIPELINE_DEPENDENCIES.json` separates model-scoped consequences from the retained historical source gates.

Four named interfaces now have proved, primitive-model consumers, rather than only a proposed map of terminology.

**A4, finite-history reduction.** For strictly positive controlled transition matrices and Gaussian observations of the new hidden state, the proof derives the positive-matrix Hilbert contraction and a uniform exponentially decreasing last-L-history error. A literal finite-report suffix implementation has an explicit label bound. This proves an actual sufficient model hypothesis; it does not infer exponential decay from summable variation alone. The parameter is fixed in the forgetting assertion, whose decision corollary concerns the current state; an unknown static phase or arbitrary past-path target is not incorrectly declared forgettable.

**C1, nonlinear filtering/observation interface.** The joint kernel is derived as `P_a(z,z') g_{a,z'}(y)`, with the report attached to the new state. Finite hidden-path expansion proves dominated `L1` continuity for compact primitive families. A Gaussian cell/tail estimate gives a marked approximation error uniform in memory and feedback. This supplies a concrete continuous-report consumer of the nonfinite duality, not an assumption that a desired posterior filter exists.

**B4, nonlinear semigroup.** For the stated finite-state exponential Hamiltonian, maximal-coordinate comparison proves global flow, comparison and sup-norm nonexpansiveness. A contracting damped equation proves the full resolvent range condition for every positive lambda. The matrix log-moment mesh converges with first-order error, and its actual reward effects enter the compact common-encoder theorem. A sign-reversing affine loss handles reward maximization. Stability estimates in rates and potentials are explicit. An exponential matrix is not misidentified as a stochastic kernel.

**D1, hidden-phase risk-sensitive control.** The source includes a latent phase and hidden state, with an unnormalized information row carrying accumulated exponential reward. The proof derives the one-policy recursion and measurable selectors. A two-phase example separates the legal common action from the illegal phasewise minimization. The posterior alone is not treated as sufficient when hidden accumulated costs matter.

These are genuine consumers for their stated model classes. They do not prove the unrestricted microscopic Hamiltonian, billiard, infinite-dimensional kinetic or phase-escape models of all historical papers. The old gate ledger is preserved, not relabeled as complete. This distinction permits positive mathematical progress without laundering an unproved historical extension into the foundation. The active contract now has two protocol adapters, four model-scoped consumers and five other conditional interfaces; this is **not** a claim that six entire downstream papers are complete.

## E9.6. Current A2 and the logical architecture

The live A2 primary entry inspected at commit `0ce25b1a492c230876930d45daf3f4d55a276358` is revision 126, entitled “Canonical nilpotent specialization, stratified contact algebra, and polarized reconstruction in multiplication failure.” Its entry imports the algebraic-geometric v123–v126 development. The v126 entry and frontmatter, rather than the stale root README, were used for this update. This is an identity/scope audit, not a re-refereeing of every A2 proof.

The primary A2 chain is recorded as independent. The finite statistical acquisition protocol retained from the earlier source is a different adapter and retains its own frozen citation. The research architecture is consequently a dependency graph, not a claim that a shared repository or the label A2 creates a theorem dependency. GTF is the common operational layer for verified acquisition and decision interfaces; the independent geometric branch can supply such a protocol when one is actually defined. No GTF premise is retroactively inserted into A2, and its branch is not modified.

## E9.7. Strengthen rather than shorten

We pursued the stronger route. No predecessor manuscript or historical derivation file is deleted. The canonical article retains the substantive v9 core, with the report/mark correction made explicitly, and adds the nonfinite and marked theory. The companion preserves the earlier bodies and introductions. The input manifests, compiled-label checks and source archive make this preservation testable. Mathematical content is organized into theorem–proof sections; response and pipeline governance stay outside the article.

## Other technical comments

**Sections 3, 12 and 13 of the report:** the common encoder, task-uniform parameter controller, initialization, public/private distinction and charged design index remain explicit. The three-membership-task example now has genuinely conflicting taskwise optima, a strict common-encoder penalty and an interior nine-row dual witness. It complements rather than replaces the v9 three-symbol reconstruction example.

**Finite synthesis:** the old exhaustive lossy-design compiler is retained with its honest worst-case scope. The new exact-state synthesis uses backward rational continuation bases and forward exploration of distinct reachable classes. A rank-two source with `K_t=t+1` prevents conflating weighted-automaton rank with retained-state cardinality. Table description, persistent state, transient workspace and acquisition are separated.

**Section 17, Gaussian experiment:** the formal signature adjacent to the theorem fixes the pre-query register, discarded reports, independent later query and terminal decoder inputs. A finite ADC/table proposition quantifies bin width, tail range, posterior evaluation error and memory. The continuous lower bound uses conditional-variance geometry directly; it is not falsely attributed to a finite partition theorem.

**Relation of retained regimes:** `projections-precision.tex` proves the quadratic projection identity and specifies how tree distortion, terminal comparison and realized-law Wasserstein presentation fit the marked spectrum. It explicitly does not identify the realized-measure task with a single marginal probe, or place every singular measure experiment inside the dominated compact theorem.

## Verification and next review

The source-bound build executes finite regressions in ordinary and optimized Python, rejects nine designated incorrect variants in both modes, reruns predecessor diagnostics, verifies pinned inputs and compiles both views with stable labels. The numerical checks include floating-point semigroup tests and are labeled accordingly. Exact finite tests do not certify general compactness, measurable selection or asymptotic theorems. The proofs are in the manuscript and remain subject to independent mathematical review. The final build receipt supplies the actual counts and immutable source identity.
