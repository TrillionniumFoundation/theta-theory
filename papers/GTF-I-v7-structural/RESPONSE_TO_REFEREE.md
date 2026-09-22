# Response to the v6 Markov report — seventh structural revision

**Manuscript:** *General Theta Foundations I: Causal Experiments, Predictive Quotients, and Resource-Aware Reduction*. **Author:** Qian Qi.

This reply addresses the report at `ff34427b2a5539ad23e2aea5cd57ce9f88d2b627`, report blob `14e052135fc188f51998aac81742e7cb0ef4e2c4`. That report reviewed `f6f08bd529be23b7b97f5cc78829006c08e29e67`. Its Sections 1–17, and especially the structural opportunity in Section 13, control this revision. We do not recycle the E-numbering of an older report.

We thank the referee for separating the validity of local proofs from the architecture and mathematical reach of Volume I. We have rebuilt the canonical article around the causal-experiment spine and extracted the predictive-energy mechanism as an abstract theorem. There is one main paper, with complete proofs, and one same-source complete-development companion. Earlier results have not been removed or silently weakened.

## New mathematical chain

The principal results are:

- `thm:v7-tree`: a predictive-tree theorem with exact deletion and insertion updates, a charged whole-tree state count, matching static and causal profiles, and converses for randomized time-dependent registers;
- `thm:v7-shift`: a sharp continually observed infinite hidden-shift model, derived from the same theorem rather than a new regeneration argument;
- `thm:v7-transport` and `thm:v7-filter`: resource-typed recursive approximation on the true predictive state, including a constructive measure-valued filter and an explicit nonlinear instrument;
- `thm:v7-gaussian-budget`: the sharp `M^(-2/r)` Le Cam approximation order of a Gaussian location experiment by arbitrary M-outcome experiments;
- `thm:v7-a2`: a deterministic physical count statistic with error `C[N^(-1/2)+J/sqrt(N)+J^(-2)]`, `J^r` designated labels, and a matching universal cardinality lower bound in the joint window `M <= K N^(r/6)`.

The quotient, instrument, Bayes geometry and simulation statements are visible in the main paper. Their classical parts are attributed rather than presented as new discoveries.

## Sections 1–3 — reviewed object and credited v6 advances

The prior Markov-renewal, pressure, critical, contracting-mean, finite-interface and A2 arguments are preserved verbatim in the companion. Their source files and old editions remain unchanged. The improvements credited by the referee—legal forbidden transitions, unary accounting, strict energy rather than strict mass, delay observability and the nongeometric clock—are not discarded. The canonical article now uses the Markov result as a verification of a foundation-level theorem instead of identifying the whole foundation with that model.

## Section 4 — Markov-renewal proof and the exponent passage

Section 5 verifies the structural hypotheses directly for the v6 energy: actual legal children, bounded unary chains, mass-weighted renewal diameters, and separation from the first post-prefix gap and delayed observability. It proves the static-to-causal realization by invoking `thm:v7-tree`.

`prop:v7-exponent-squeeze` writes out the passage from upper and lower power estimates to the logarithmic limit. The pressure theorem is retained in the companion with all its hypotheses; it is not used as a premise of the abstract tree theorem. The exponent is thus a downstream identification of a profile, not part of the definition of the foundation.

## Section 5 — scope of critical corrections

The complete Parry/equal-ratio/polynomial-survival theorem and finite-window calculation are preserved. They remain a family theorem. The revision does not infer a universal second-order Gibbs law from first-order pressure. The canonical main result is the finite-budget profile theorem, which does not erase second-order structure. No new universal critical logarithm is asserted.

## Section 6 — restore the declared Volume-I identity

The canonical paper now follows the requested sequence:

`positive experiment -> future-test quotient -> causal morphism -> attainable geometry -> charged realization`.

Section 2 constructs the actual normalized kernel history, including failure and cost records; defines executable future tests; proves quotient minimality and update descent; states a sufficient topological realization criterion without assuming all Borel quotients are smooth; proves the Bayes quantization, posterior barycentre and information-loss identities; and identifies normalized response and the observation-product annihilator.

Section 3 includes the simulator's initialized state and a monotone resource transformer in the morphism. It distinguishes same-observation approximation, policy-uniform history-law comparison, and terminal experiment deficiency. Sections 4–8 then provide nonclassical realizations and applications of these interfaces. A journal reader no longer needs to open an archived first-edition appendix to discover what the title means.

The title and programme are retained. The solution is synthesis around actual structural theorems, not a lower venue target or a replacement title.

## Section 7 — remove exact finite-dimensional posterior-mean closure

Two new results address this point at different strengths.

First, `thm:v7-shift` has the entire infinite past of hidden bits as its hidden state. Noisy continuing observations give a posterior product law with infinitely many observation-dependent coordinates. The shifted old tail persists at every step, so there is no fixed-step common minorizer. Its true conditional-mean vector lies in a Hilbert space. The insertion half of `thm:v7-tree` gives a matched finite-register law. For a fair binary symmetric channel the result is

`epsilon(1-epsilon) + Theta((1-2 epsilon)^2 M^(-alpha))`,

where `alpha=-2 log(r)/log(2)`. At complete observation erasure the excess is exactly zero. Initialization is paid and vanishes only in the specified long-time average.

Second, `thm:v7-filter` works on the actual space of probability measures on `[0,1]`. An explicit quantile-grid presentation has exactly `binomial(2n,n)` possible laws and radius at most `3/(2n)`. Its recursive error is at most `rho^t + [3/(2n)+eta]/(1-rho)`, with numerical defect eta separately charged. For M states this yields a constructive logarithmic approximation rate; it is not claimed to be universally optimal.

The nonlinear polynomial-branch instrument in `cor:v7-nonlinear` verifies uniform Wasserstein contraction, exact rational implementation, failure of a fixed-step common minorizer, and failure of every fixed finite polynomial-moment list to close its own recursion on all priors. The proof does not replace the posterior measure by a scalar conditional mean. The claim about moment closure is not an impossible assertion that standard Borel measures cannot be coded by real numbers.

## Section 8 — resources belong to the morphisms

`thm:v7-transport` uses declared resource signatures and implementation-backed monotone transformers. It proves composition, the KM product-register cost, same-path recursive error, report-law comparison and bounded-loss transport. Precision, workspace, description, preparations and time remain separate coordinates rather than being identified with cardinality. A finite decoder event costs a finite factor; a continuous free observation does not.

The nonlinear measure implementation specifies its transient rational atoms and discards them before the next step. The tree theorem counts all vertices. A2 retains only its designated label, not an uncharged exact score. The default cardinality signature explicitly leaves the other resources unlimited; the theorem does not claim that a transition table with scale-dependent entries has zero bit-description cost in a different resource model.

## Section 9 — a two-sided A2 bridge and the five probability steps

The previous sufficient-only application has been strengthened, not merely expanded editorially.

1. `lem:v7-poisson-normal` proves parameter-uniform jittered Poisson/normal comparison of order `mu^(-1/2)` using a displayed Stirling remainder and controlled tails, with an explicit absolute constant.
2. `lem:v7-variance` proves the variance replacement by the Gaussian entropy formula and gives the constants in terms of the fixed exposure parameters.
3. `lem:v7-boundary` compares deterministic unjittered compactified labels, charging boundary crossing by `C J/sqrt(N)`. It never compares a discrete unjittered real statistic with a continuous Gaussian in total variation.
4. `lem:v7-hat` constructs a positive tensor-hat reconstruction. Compactification removes the growing overflow box; affine reproduction removes the first-order histogram error. Its uniform total-variation error is at most `r H_2/(12 J^2)`.
5. The proof of `thm:v7-a2` composes the two parameter-independent kernels explicitly. No jitter occurs in the physical statistic.

The new lower bound is independent of these upper constructions. `lem:v7-cardinality` uses a bounded Bayes decision problem and a full-dimensional posterior-mean law to show that every M-output experiment has distance at least `c M^(-2/r)` from the Gaussian shift. It covers randomized experiments and non-grid encoders. Thus the physical A2 statistic is order-optimal for `2^r <= M <= K N^(r/6)`.

At the earlier target error `N^(-1/5)`, the necessary and sufficient order of the designated-label budget is `N^(r/10)`, without the old overflow logarithm. At the top of the displayed window the constructed comparison has order `N^(-1/3)`. This is not claimed as the optimal sample-size distance with arbitrarily many labels. The fixed known-mark, fixed-rank, positive-definite protocol remains explicit. No conductor multiplicity is turned into a noise variance, and the new theorem is not a classification of A2's higher-defect schemes.

## Section 10 — whole-pipeline interpretation and current endpoints

`HISTORY_AUDIT.md` distinguishes the fixed eleven-paper snapshot from modern A1 and A2. This revision freshly consults all eleven Round-20 reports and inventories the native theorem headings, with additional reads of the A4/C1 arguments, the Volume-I blueprint, modern A1's predictable network, and modern A2's current algebra and statistical protocol. Exact ranges and hashes, not an assertion that 9,000 files were reread, are recorded.

A1-v37 is fixed at `90465076589f5e5c69227d624f278c47744f1c1d`. The A2-v118 mathematical source is fixed at `44bfc648ead008896a6981a7302a6d5ab8b21bb8`. The newer named v119 branch is fixed at `d4254d9b01405ad02c64d2ff591503d4cc7a6aa7`; direct comparison shows one added independent v118 review and no manuscript changes. The named-branch and mathematical-source facts are distinguished.

The actual new dependency is explicit: A2's declared exposure matrices instantiate `thm:v7-a2`, whose necessity invokes the general `thm:v7-gaussian-budget` verbatim. The historical spectral, path-LDP, particle, semigroup, common-domain and phase gates are not premises of any new proof. Their preservation is not represented as closure.

## Section 11 — closest literature

The new introduction compares with Kesseböhmer–Zhu's graph-directed Markov quantization theorem, including the spectral matrix and coefficient issue, and with Demirci–Kara–Yüksel's average-cost contraction/quantized-belief/finite-window results. The latter uses a distinct bibliography key from the older, different 2024 preprint already in the inherited references.

Static separated-cylinder quantization, greedy coding trees, conditional expectation, and contraction-plus-quantization are credited as antecedents. The new structural feature is exact suffix closure supporting both deletion and insertion of the complete predictive record, with a whole-register arbitrary-machine converse. The new statistical feature is the universal finite-experiment cardinality obstruction and the positive quadratic reconstruction, applied to the physical protocol. `LITERATURE_AUDIT.md` identifies the exact primary texts and does not claim exhaustive priority determination.

## Sections 12–13 — dispositions and the proposed structural opportunity

The theorem suggested in Section 13 is now an actual theorem, `thm:v7-tree`, not an informal reformulation. All six ingredients are visible: a factorial admissible language, strict predictive prefix-attachment decrease, legal child comparability, bounded unary chains, Hilbert-image separation, and compatible suffix evolution. Greedy balance, fixed-budget dilation, disjoint tubes and exact closure are proved separately.

The second model is qualitatively different: it continually inserts noisy observations about newly entering hidden coordinates and never refreshes the old hidden tail. Its lower bound is direct Bayes geometry of a stationary posterior vector, not the renewal converse under a different name. The same abstract energy theorem supplies both causal realizations.

## Section 14 — response to the alternative routes

| Route | Action in this revision |
|---|---|
| A: focused v6 paper | The complete v6 argument remains intact and independently readable; it is not made the identity of Volume I. No duplicate renamed paper is needed to preserve it. |
| B: restore Volume I | Positive experiments, quotient minimality, information geometry, causal morphisms and charged realization are in the canonical main article. |
| C: abstract suffix mechanism | The full two-orientation structural theorem, Markov-renewal verification and sharp nonrenewing hidden-shift application are proved. |
| D: beyond exact finite posterior means | Infinite-coordinate posterior law plus constructive measure-valued recursion and a nonlinear physical instrument. |
| E: necessary A2 budget | Universal M-output Gaussian lower bound and a matching physical upper law in a growing joint window. |
| F: historical hard interface | No unrelated historical gate is declared proved. The current A2 necessity/sufficiency bridge is the precise pipeline consequence. |
| G: nearest neighbours | Direct primary-text comparison with graph-directed Markov quantization and contraction-based average-cost approximation. |

## Sections 15–17 — final form and submission status

`paper.pdf` is the one canonical article. `complete-development.pdf` preserves the same core and every preceding theorem/proof body, with identical core labels. Response, proof ledger, audit and build records are outside the mathematical narrative. The previous sources and reviews are not rewritten.

The proofs rather than the diagnostics are the response. The build identifies the submitted object and catches finite regressions; it is not a mathematical proof certificate, independent acceptance, or a decision on priority or journal suitability. The final frozen branch and source/publication identities are recorded in the repository index after publication verification.
