# R79 theorem dependencies, hypotheses and claim boundaries

This is the author dependency addendum for General Theta Foundations I. The actual paired native index has **252 statement labels**: all **240 inherited R78 labels** and **12 additions** (12 main, 0 supplement). Supporting lemmas and corollaries are included; this is not a novelty count. The independent R58 companion keeps its separate source and numbering.

## Reading the map

Direct logical prerequisites are actual premises of the proof. Inherited mechanisms identify related retained arguments or a construction reproduced in full. Definition labels and internal facts are separate. Automatically extracted references in the structured record are syntactic evidence and do not replace this author analysis.

The actual compiled index and every new proof source are hashed in `provenance/R79_PROOF_DEPENDENCIES.json`. The final Git identity is supplied by the source/publication handshake. Current native kind is authoritative: a label beginning `thm:` may name a compiled corollary and is not counted again as an independent theorem.

## 1. Feasibility from arbitrary initial quantum states

**Native locator:** main, theorem 3.1, page 9; `thm:r79-dark-feasibility` in `sections/54-robust-instrument-frontier.tex`.

**Hypotheses.** Finite Hilbert dimension, finite command/report alphabets and arbitrary CP failure branches continuous in a compact fixed-model family. All commands legal; mandatory immediate success stopping; common positive mean cost bounds c_* I <= G <= c^* I. One autonomous model-independent classical controller, prescribed pure initial label counted, no uncounted clock/history/seed, and worst cost over every initial density matrix.

**Conclusion.** Uniform finite-cost feasibility for arbitrary visible history is equivalent to absence of a closed common dark subspace in every fixed model and to properness of every one-row full-support command policy; its resolvent gives finite cap C0.

**Direct logical prerequisites.** None listed in this category.

**Inherited mechanisms and contextual authorities.** `thm:primitive-fallback`, `lem:compact-fallback`

**Proof mechanism.** If a dark space exists, every policy stays there. Otherwise a spectral-radius-one full-support failure map has a positive nonzero Cesaro fixed point whose support is common and dark. Inverse continuity on the compact family bounds the one-row cost.

**Classical ingredients and priority boundary.** Finite-dimensional positive-map order and compactness; Classical reachability, cost-potential verification and stochastic controller theory, as individually attributed in the manuscript. Inherited compact primitive fallback in a self-contained positive-cost formulation, not a new dark-space criterion.

**Limits.** The all-initial-state and all-commands-legal requirements are essential. Does not decide partial-prior reachability or optional commitment.

## 2. Finite reachable-support construction

**Native locator:** main, lemma 3.2, page 10; `lem:r79-reachable-corner` in `sections/54-robust-instrument-frontier.tex`.

**Hypotheses.** Finite Hilbert dimension, finite command/report alphabets and arbitrary CP failure branches continuous in a compact fixed-model family. All commands legal; mandatory immediate success stopping; common positive mean cost bounds c_* I <= G <= c^* I. One autonomous model-independent classical controller, prescribed pure initial label counted, no uncounted clock/history/seed, and worst cost over every initial density matrix. One fixed controller and model; total product Hilbert dimension Md.

**Conclusion.** The support of the sum of T^n iota_1(I), 0<=n<=Md-1, is the least invariant corner. Finite all-initial cost implies finite cost and transience on that corner.

**Direct logical prerequisites.** None listed in this category.

**Inherited mechanisms and contextual authorities.** `lem:reachable-support`, `thm:face`

**Proof mechanism.** Increasing supports stabilize by finite rank. A positive finite reachability sum dominates a multiple of its support projection. Its cost is a finite sum of tails of the initial cost series; the positive cost floor then makes all restricted powers tend to zero.

**Classical ingredients and priority boundary.** Finite-dimensional positive-map order and compactness; Classical reachability, cost-potential verification and stochastic controller theory, as individually attributed in the manuscript. Inherited reachable-support construction; repeated proof makes the new stability argument independent of an external black box.

**Limits.** No full-space transience at inaccessible labels or physical directions.

## 3. Exact finite support and Lyapunov certificate

**Native locator:** main, theorem 3.3, page 10; `thm:r79-exact-certificate` in `sections/54-robust-instrument-frontier.tex`.

**Hypotheses.** Finite Hilbert dimension, finite command/report alphabets and arbitrary CP failure branches continuous in a compact fixed-model family. All commands legal; mandatory immediate success stopping; common positive mean cost bounds c_* I <= G <= c^* I. One autonomous model-independent classical controller, prescribed pure initial label counted, no uncounted clock/history/seed, and worst cost over every initial density matrix. Fixed controller, fixed model, finite proposed cost bound b.

**Conclusion.** Cost <=b for every initial density matrix iff a supported invariant projection P and positive potential W satisfy the displayed Lyapunov inequality and W_1<=bI. The least reachable true cost witness satisfies equality.

**Direct logical prerequisites.** `lem:r79-reachable-corner`

**Inherited mechanisms and contextual authorities.** `thm:memory-certificate`, `thm:face`

**Proof mechanism.** Iterating a positive supersolution bounds every finite prefix and hence the full cost. Conversely, restrict the geometric cost series to the reachable corner; the all-state initial bound is exactly the first-block operator bound.

**Classical ingredients and priority boundary.** Finite-dimensional positive-map order and compactness; Classical reachability, cost-potential verification and stochastic controller theory, as individually attributed in the manuscript. Inherited support-potential theorem specialized to positive-cost success stopping; no separate novelty claim.

**Limits.** A global all-label inequality is not necessary before regularization.

## 4. Robust quantum finite-memory frontier

**Native locator:** main, theorem 3.4, page 11; `thm:r79-quantum-frontier` in `sections/54-robust-instrument-frontier.tex`.

**Hypotheses.** Finite Hilbert dimension, finite command/report alphabets and arbitrary CP failure branches continuous in a compact fixed-model family. All commands legal; mandatory immediate success stopping; common positive mean cost bounds c_* I <= G <= c^* I. One autonomous model-independent classical controller, prescribed pure initial label counted, no uncounted clock/history/seed, and worst cost over every initial density matrix. No model has a closed dark subspace. For the effective clause: a compact semialgebraic parameter set and algebraic polynomial/rational primitive coefficients with no poles.

**Conclusion.** Every finite-M robust optimum is attained and nonincreasing in M. Its exact certificate has order exists common controller, for every fixed model, exists model-specific P,W. Algebraic primitive families give an algebraic value and attaining algebraic controller by finite real elimination.

**Direct logical prerequisites.** `thm:r79-dark-feasibility`, `thm:r79-exact-certificate`

**Inherited mechanisms and contextual authorities.** `cor:memory-algebraic`, `thm:memory-certificate`

**Proof mechanism.** The robust objective is a supremum of continuous finite-prefix objectives, hence lower semicontinuous on a compact controller simplex. The support certificate is applied modelwise with the same controller. Real/imaginary coordinates and PSD principal minors give a quantified semialgebraic formula; the attained finite endpoint and sample controller are algebraic.

**Classical ingredients and priority boundary.** Finite-dimensional positive-map order and compactness; Classical reachability, cost-potential verification and stochastic controller theory, as individually attributed in the manuscript. Consolidation of inherited finite-model synthesis and compactness, extending compact semialgebraic uncertainty to unrestricted legal feedback. The distinct central addition is subsequent same-memory stability.

**Limits.** No efficient algorithm, executed general QE, attained worst model, universal closed form or finite saturation of unrestricted history.

## 5. Information remains after a physical reset

**Native locator:** main, example 3.5, page 12; `ex:r79-hidden-model-memory` in `sections/54-robust-instrument-frontier.tex`.

**Hypotheses.** Two scalar hidden models with success probabilities (1/2,1/10) and their swap; unit costs, one failure report, fixed hidden model and counted pure initializer. The same example is lifted to a known nonreset qubit instrument with diagonal failure Kraus operators.

**Conclusion.** A uniform initial row followed by pure alternating rows costs 34/11, below the one-row robust value 10/3. Every report-only deterministic routing of that same palette costs at least 10/3. The known-model qubit lift has the same all-initial-state values.

**Direct logical prerequisites.** None listed in this category.

**Inherited mechanisms and contextual authorities.** `thm:r78-palette-normal-form`

**Proof mechanism.** Compute the two alternating Bellman recurrences exactly and minimize the single-row worst cost. For report-only routing a single destination row is used after all failures. Diagonal qubit costs and branch traces depend only on the diagonal initial mixture, whose extremes are the two models.

**Classical ingredients and priority boundary.** Finite-dimensional positive-map order and compactness; Classical reachability, cost-potential verification and stochastic controller theory, as individually attributed in the manuscript. Explicit positive-probability boundary example for the reset same-row theorem, not an all-controller two-row optimum or general POMDP novelty claim.

**Limits.** The three-label value is an achievable upper bound, not a claimed exact V3 for this example. Physical reset with unknown fixed model differs from a known reset state sufficient for control.

## 6. Finite initial cost with unbounded continuation witnesses

**Native locator:** main, example 3.6, page 13; `ex:r79-unbounded-reachable-witness` in `sections/54-robust-instrument-frontier.tex`.

**Hypotheses.** Scalar compact family theta in [0,1], unit costs; failure of a is theta(1-theta), failure of b is 1-theta. Start at a then stay at b after failure, with the initial label counted.

**Conclusion.** Initial cost is 2-theta for theta>0 and 1 at theta=0, with unattained supremum 2. For 0<theta<1 the reachable second-label true cost is 1/theta; no uniform original-witness bound exists.

**Direct logical prerequisites.** `thm:r79-exact-certificate`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Sum the geometric tail after the first failure. At theta=0 the second label is dark but inaccessible; at theta=1 it is also inaccessible. Every interior second label is reachable and has reciprocal-theta cost.

**Classical ingredients and priority boundary.** Finite-dimensional positive-map order and compactness; Classical reachability, cost-potential verification and stochastic controller theory, as individually attributed in the manuscript. Explicit compact boundary obstruction motivating same-memory regularization.

**Limits.** Does not contradict initial robust boundedness, attained minimization over controllers, or regularized global witness bounds.

## 7. Regularization with the same live-label budget

**Native locator:** main, theorem 4.1, page 13; `thm:r79-label-restart` in `sections/55-memory-regularization.tex`.

**Hypotheses.** Finite Hilbert dimension, finite command/report alphabets and arbitrary CP failure branches continuous in a compact fixed-model family. All commands legal; mandatory immediate success stopping; common positive mean cost bounds c_* I <= G <= c^* I. One autonomous model-independent classical controller, prescribed pure initial label counted, no uncounted clock/history/seed, and worst cost over every initial density matrix. An M-label controller has robust all-initial cost <=b. After each failure, independently return its label to 1 with probability epsilon; 0<epsilon<=1 and epsilon*b<c_*.

**Conclusion.** The same command rows and M labels have initial cost <=U=b/(1-epsilon*b/c_*) and cost <=K=c^*/epsilon+U from every physical state at every label. Full-space exact cost witnesses obey these bounds.

**Direct logical prerequisites.** `lem:r79-reachable-corner`

**Inherited mechanisms and contextual authorities.** `lem:compact-fallback`, `thm:compact-risk`

**Proof mechanism.** Cut each label-1 segment at success or its first restart coin. Its cost is <=b and restart probability <=epsilon*b/c_*. Bound finite numbers of segments by a geometric sum, then use monotone convergence. From any label the first segment costs <=c^*/epsilon; after a restart the label-1 bound applies. Positive-cost transience gives full-space cost operators.

**Classical ingredients and priority boundary.** Finite-dimensional positive-map order and compactness; Classical reachability, cost-potential verification and stochastic controller theory, as individually attributed in the manuscript. Principal new resource-preserving construction: no additional label, no physical reset, uniform over a fixed hidden model. It is distinct from inherited finite-prefix completion with growing memory.

**Limits.** Requires the all-initial-state cost guarantee. The hidden model never changes during execution; command rows remain identical but update probabilities change. The constants are upper bounds without sharpness claim.

## 8. Perturbation of a bounded cost witness

**Native locator:** main, lemma 4.2, page 15; `lem:r79-centered-perturbation` in `sections/55-memory-regularization.tex`.

**Hypotheses.** Finite Hilbert dimension, finite command/report alphabets and arbitrary CP failure branches continuous in a compact fixed-model family. All commands legal; mandatory immediate success stopping; common positive mean cost bounds c_* I <= G <= c^* I. One autonomous model-independent classical controller, prescribed pure initial label counted, no uncounted clock/history/seed, and worst cost over every initial density matrix. The same counted controller in two models; a source global witness 0<=W_k<=KI. Normalized output includes success, with instrument half-trace distance <=eta; cost operator distance <=zeta; target has positive cost floor c_*.

**Conclusion.** The adjoint continuation error is bounded in order by eta*K I. If delta=zeta+eta*K<c_*, scaling W by 1/(1-delta/c_*) gives a target global supersolution.

**Direct logical prerequisites.** None listed in this category.

**Inherited mechanisms and contextual authorities.** `eq:effect-distance`

**Proof mechanism.** The difference of normalized full output states has zero trace. Center its bounded block observable at K I/2, including zero success observable. Transfer the source supersolution and use the target positive-cost floor to absorb its scalar error by scaling.

**Classical ingredients and priority boundary.** Finite-dimensional positive-map order and compactness; Classical reachability, cost-potential verification and stochastic controller theory, as individually attributed in the manuscript. Inherited centered trace estimate in the controller-block setting; a supporting transfer lemma, not a new general norm inequality.

**Limits.** Requires bounded global witnesses, not only bounded initial cost. The success outcome cannot be omitted in the centered estimate.

## 9. Uniform stability of the complete memory frontier

**Native locator:** main, theorem 4.3, page 15; `thm:r79-frontier-stability` in `sections/55-memory-regularization.tex`.

**Hypotheses.** Finite Hilbert dimension, finite command/report alphabets and arbitrary CP failure branches continuous in a compact fixed-model family. All commands legal; mandatory immediate success stopping; common positive mean cost bounds c_* I <= G <= c^* I. One autonomous model-independent classical controller, prescribed pure initial label counted, no uncounted clock/history/seed, and worst cost over every initial density matrix. A feasible source compact model family. Each target model pairs with one source model satisfying both distance bounds; pairing is only an offline proof choice. For two-sided uniformity both families have a common one-row cap B and cost bounds, with explicit smallness conditions on eta,zeta.

**Conclusion.** The target M-label value is <=U_epsilon/[1-(zeta+eta*K_epsilon)/c_*]. Under the displayed smallness assumptions every M simultaneously satisfies |V_M(U)-V_M(V)| <= ((10B^2+4Bc^*)/c_*)*sqrt(eta)+(4B/c_*)*zeta. This holds across changes in supports and extends to eta=0.

**Direct logical prerequisites.** `thm:r79-quantum-frontier`, `thm:r79-label-restart`, `lem:r79-centered-perturbation`, `thm:r79-dark-feasibility`

**Inherited mechanisms and contextual authorities.** `thm:compact-risk`, `prop:r78-frontier-stability`

**Proof mechanism.** Regularize one attaining common source controller without adding memory. Transfer its bounded full-space witnesses model by model. The same probabilities implement all target models. Set epsilon=sqrt(eta), bound U<=2B and delta<=c_*/2, and reverse directions. Treat eta=0 by taking epsilon down to zero. Local properness of a fixed full-support row supplies common neighborhood caps.

**Classical ingredients and priority boundary.** Finite-dimensional positive-map order and compactness; Classical reachability, cost-potential verification and stochastic controller theory, as individually attributed in the manuscript. Principal new theorem: a complete optimal-frontier modulus uniform in all counted memory budgets, with same-size controllers and nonreset quantum back-action. Search found no exact matching theorem; priority and top-journal significance remain subject to independent assessment.

**Limits.** The exponent is not claimed optimal. Family matching is not adversarial switching, model revelation, optional commitment or a restricted-prior theorem.

## 10. Finite-memory approximation to unrestricted control

**Native locator:** main, corollary 4.4, page 16; `cor:r79-history-limit` in `sections/55-memory-regularization.tex`.

**Hypotheses.** Finite Hilbert dimension, finite command/report alphabets and arbitrary CP failure branches continuous in a compact fixed-model family. All commands legal; mandatory immediate success stopping; common positive mean cost bounds c_* I <= G <= c^* I. One autonomous model-independent classical controller, prescribed pure initial label counted, no uncounted clock/history/seed, and worst cost over every initial density matrix. The compact model family is feasible with full-support one-row cap C0.

**Conclusion.** V_M decreases to the unrestricted visible-history infimum. With M_T=1+sum_{t=0}^{T-1}(|A||Y|)^t, V_M_T <= V_hist*(1+C0/(c_*T)). The same uniform stability bound holds for V_hist.

**Direct logical prerequisites.** `thm:r79-dark-feasibility`, `thm:r79-quantum-frontier`, `thm:r79-frontier-stability`

**Inherited mechanisms and contextual authorities.** `thm:compact-risk`

**Proof mechanism.** Store the first T command/report pairs in counted history-tree labels and then use one additional fallback label. Positive cost bounds survival by b/(c_*T); all-initial fallback handles the actual posterior. Infimize without assuming an optimal unrestricted policy and pass the uniform-in-M stability bound to the limit.

**Classical ingredients and priority boundary.** Finite-dimensional positive-map order and compactness; Classical reachability, cost-potential verification and stochastic controller theory, as individually attributed in the manuscript. Inherited completion mechanism with explicit cost and memory count; the extension of the new uniform modulus to its limit is a consequence.

**Limits.** No exact finite saturation or efficient history tree. Model-independent visible-history kernels have no undeclared observation port.

## 11. Positive-success refinement

**Native locator:** main, corollary 4.5, page 17; `cor:r79-positive-success` in `sections/55-memory-regularization.tex`.

**Hypotheses.** Same finite-dimensional primitive interface and positive-cost conventions, with common cost ceiling c^*. For every command and model in both compared compact families, success effect B_a>=kappa I with fixed 0<kappa<=1. Mutual model pairing simultaneously bounds normalized instrument and cost distances by eta and zeta.

**Conclusion.** All M simultaneously satisfy |V_M(U)-V_M(V)|<=zeta/kappa+c^* eta/kappa^2 without small-error restriction; the same holds for V_hist. Counted history completion has error at most C0(1-kappa)^T. Scalar geometric waiting proves local sharpness of both coefficients for 0<kappa<1.

**Direct logical prerequisites.** `lem:r79-centered-perturbation`, `cor:r79-history-limit`

**Inherited mechanisms and contextual authorities.** `eq:effect-distance`

**Proof mechanism.** Bound every full-space inverse by 1/kappa and every positive cost witness by c^*/kappa. Subtract the two fixed-controller cost equations, apply the centered estimate, then take model suprema and controller infima. Uniform success gives a geometric survival tail for counted prefix completion. Solve the scalar geometric waiting laws to prove sharpness.

**Classical ingredients and priority boundary.** Positive-map norm contraction and the resolvent identity; Geometric waiting-time cost and conditional survival bounds. A quantitative refinement in a stronger structural class, using the classical resolvent perturbation mechanism; no claim that this classical mechanism is novel or the general square-root exponent is sharp.

**Limits.** Uniform per-command success is stronger than common-dark-space exclusion. Exponential approximation is in history horizon, generally a power law in the number of history labels. Coefficient sharpness is local and does not classify support-degenerate instruments.

## 12. Golden-ratio memory cost

**Native locator:** main, proposition 5.1, page 19; `prop:r79-golden-ratio-memory` in `sections/56-exact-hidden-model.tex`.

**Hypotheses.** Two fixed hidden scalar models: command a succeeds surely only in model 0, b surely only in model 1; other calls fail, unit costs and one failure report. Arbitrary randomized updates allowed; one pure initial live label is counted.

**Conclusion.** Exactly V1=2, V2=(1+sqrt(5))/2, and V_M=3/2 for M>=3, which also equals the unrestricted visible-history optimum. The two-label optimizer has model-specific supports (1,0) and (1,1).

**Direct logical prerequisites.** None listed in this category.

**Inherited mechanisms and contextual authorities.** `thm:r79-exact-certificate`

**Proof mechanism.** One label minimizes max(1/r,1/(1-r)). For two label rows r,s, split r>=s and r<=s; maximal conditional success gives reciprocal bounds, while failure of the first call gives affine bounds. Balancing max(1/r,1+r) gives the golden ratio, attained by the explicit transition rule. Any first command incurs worst cost at least 3/2; three labels attain it.

**Classical ingredients and priority boundary.** Finite-dimensional positive-map order and compactness; Classical reachability, cost-potential verification and stochastic controller theory, as individually attributed in the manuscript. Exact special-model all-M law and counted-initializer separation; not a general closed quantum frontier.

**Limits.** A free mixed initializer changes the resource problem and attains 3/2 with two labels. The zero-success degeneracy is explicit; the separate positive example tests a different structural boundary.

## Retained authority and unresolved questions

All 240 predecessor proof records retain every nondisplay field unchanged. Current document, number, page, source and locator-description fields are refreshed. The original ledger remains byte-identical, as do the R74/R75/R76/R78 addenda and all protected proof bodies. Edition-relative words such as 'new' within an unchanged old record refer to that original edition, not to R79.

The original general-M squared-sign risk frontier, optional-stopping tied control and universal finite-memory saturation, unrestricted high-contrast classification for every finite group, the matching unrestricted-decoder approximation rate, intermediate timing, coefficient-bit/precision/program/workspace costs, unknown-model recovery and independent Theta objectives remain distinct. In particular matrix parameter-feasibility equivalence does not classify every off-boundary positive factorization, and a sharp excursion probability is not a sharp universal approximation cost. The inherited R76 matching leading logarithm applies only to the stated fixed physical density dictionaries with Born terminal decoders, at fixed positive target budget and a fixed badly approximable phase.

## Evidence categories

The written proofs are ordinary author arguments. Author-team AI challenges, finite exact/floating diagnostics, native compilation, source hashing, independent human assessment and editorial decisions remain separate evidence types. General real quantifier elimination is an existence/computability ingredient; these maps do not claim it was executed. The R65 deposited report is not reclassified as a review of R79.

Regenerate with `python build_theorem_map.py` and check with `python build_theorem_map.py --check`. Missing labels, a different inherited authority, altered nondisplay old proof fields or an incomplete current statement inventory are rejected.
