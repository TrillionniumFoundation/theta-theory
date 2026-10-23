# R78 theorem dependencies, hypotheses and claim boundaries

This is the author dependency addendum for General Theta Foundations I. The actual paired native index has **240 statement labels**: all **235 inherited R77 labels** and **5 additions** (5 main, 0 supplement). Supporting lemmas and corollaries are included; this is not a novelty count. The independent R58 companion keeps its separate source and numbering.

## Reading the map

Direct logical prerequisites are actual premises of the proof. Inherited mechanisms identify related retained arguments or a construction reproduced in full. Definition labels and internal facts are separate. Automatically extracted references in the structured record are syntactic evidence and do not replace this author analysis.

The actual compiled index and every new proof source are hashed in `provenance/R78_PROOF_DEPENDENCIES.json`. The final Git identity is supplied by the source/publication handshake. Current native kind is authoritative: a label beginning `thm:` may name a compiled corollary and is not counted again as an independent theorem.

## 1. Dominance with the same command rows

**Native locator:** main, theorem 4.1, page 10; `thm:r78-palette-normal-form` in `sections/53-reset-memory-frontier.tex`.

**Hypotheses.** Finite reported reset instrument as in thm:reset-control: finite Hilbert dimension, commands and reset states, positive semidefinite failure effects, strictly positive conditional mean cost floor, mandatory immediate success stopping, and no closed failure set. An autonomous controller with at most M live labels, fixed command rows p^1,...,p^M, prescribed pure initial label 1, and finite cost bounded by C for every initial density matrix. The observation port includes only the declared report and the controller knows its own sampled command; it has no free state measurement, cost observation, clock, hidden initial label mixture or additional history store.

**Conclusion.** One controller with exactly the same list of command rows and the same initial label, whose post-report update is a deterministic function of the reset report alone, weakly improves expected cost at every initial density matrix. The finite row-choice Bellman system has a unique nonnegative finite solution x with x_i<=C; the new controller has initial cost operator H(p^1,x).

**Direct logical prerequisites.** `thm:reset-control`

**Inherited mechanisms and contextual authorities.** `prop:reset-rigidity`

**Proof mechanism.** Treat existing fixed command distributions as finite choices on the observed reset states. Restarting the original controller at label 1 from each sigma_i bounds finite-horizon optimal row-choice values by C. Monotone value iteration gives a finite Bellman solution. Greedy equality and the positive conditional mean cost floor prove finite expected duration, vanishing bounded potential, and exact costs. Bellman inequalities dominate every history policy using these rows, including those remembering sampled commands and private coins; after each first failure the reset state alone fixes the continuation lower. The deterministic selector attains all these continuation lowers using existing labels, proving simultaneous initial-state dominance and uniqueness.

**Classical ingredients and priority boundary.** Finite stochastic shortest-path Bellman verification; Monotone finite-horizon dynamic programming; Markov sufficiency of an observed reset state; Prior nonlinear programming formulations of optimal fixed-size stochastic controllers. A counted-memory consequence of finite reset sufficiency: simultaneous pointwise dominance with the exact existing command-row list and pure initializer. Classical Bellman optimality is credited, not claimed as newly discovered.

**Limits.** No assertion that all command rows can be made pure, no general partially observed-process normal form, no properness inference from a single initial preparation, and no convexification of the memory constraint.

## 2. Exact attained frontier at every memory

**Native locator:** main, theorem 4.2, page 11; `thm:r78-reset-frontier` in `sections/53-reset-memory-frontier.tex`.

**Hypotheses.** The full finite reset class and observation conventions of thm:reset-control, with positive mean cost floor and no closed failure set; failure effects may be merely positive semidefinite. M>=1 counts live controller labels and includes the prescribed pure initial label. A fixed full-support command distribution supplies the explicit finite one-label cap C0 from eq:r78-explicit-cap.

**Conclusion.** The complete constrained value V_M is the attained finite minimum of lambda_max H(p^1,x) over M command rows, one deterministic selector of rows for each reset report, and x in [0,C0]^s satisfying the displayed Bellman supersolution inequalities. For budgets b in [0,C0], adding H<=bI is necessary and sufficient for an actual M-label controller. This determines the exact optimal-memory threshold without strict positive exposure, and gives a strict gap at every insufficient M. Algebraic primitive data yield finite exact algebraic synthesis, without polynomial-time or fixed-M minimax claims.

**Direct logical prerequisites.** `thm:r78-palette-normal-form`, `thm:reset-control`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Prove both budget implications. A supersolution bounds finite-prefix continuation cost; the positive floor gives properness, and positivity of the initial failure effects gives H as an upper cost certificate. Conversely apply the same-row normal form to any controller with robust cost b<=C0; its Bellman vector lies in the compact cube and supplies equality constraints plus H<=bI. The one-label baseline makes the finite union nonempty, compactness yields an optimum, and equality of feasible budgets identifies it with the original controller infimum. Finite unrestricted implementation bounds the saturation memory. With algebraic data, simplex, supersolution and Hermitian principal-minor constraints are real-algebraic; elimination and sample-point selection give exact values and attaining coordinates.

**Classical ingredients and priority boundary.** Bellman supersolutions and stochastic shortest-path verification; Compact finite-dimensional optimization; Positive semidefinite matrix order and the spectral variational principle; Real-algebraic decision and sample-point procedures; Prior nonlinear programming formulations of optimal fixed-size stochastic controllers. An exact entire hard-memory cost frontier, compact budget certificate, and synthesis theorem for the stated reset class, extending the inherited optimum-threshold and first-residual lower certificate. The semialgebraic methods themselves are classical.

**Limits.** The result is not a closed form for arbitrary inputs or a polynomial algorithm; it does not solve the original squared-sign risk frontier, general partially observed control, or arbitrary stopping. The precise row-initializer convention and all-initial-state quantifier are retained.

## 3. Continuity of the full frontier

**Native locator:** main, proposition 4.3, page 12; `prop:r78-frontier-stability` in `sections/53-reset-memory-frontier.tex`.

**Hypotheses.** Fixed finite Hilbert dimension and fixed finite command and reset-report alphabets. Valid primitive reset data with positive mean cost floor and no closed failure set. A fixed finite live memory M with the pure-start observation and counting conventions of thm:r78-reset-frontier.

**Conclusion.** V_M is continuous in the primitive effects, mean costs and reset states throughout the valid class. Every strict gap V_M>V_* persists locally. This is a statement about values, not continuity of the discrete optimal-memory threshold.

**Direct logical prerequisites.** `thm:r78-reset-frontier`, `thm:reset-control`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Upper semicontinuity follows by retaining an attaining controller: its transient reset matrix has spectral radius below one, and the continuation resolvent and spectral start cost vary continuously. A full-support proper row provides locally uniform upper bounds. For lower semicontinuity take attaining certificate sequences, extract convergent rows and bounded continuation vectors with a constant selector, and pass the closed supersolution and spectral inequalities to the limit. The resulting finite supersolution constructs a proper controller. The unrestricted value is a fixed sufficiently-large-memory value, so strict gaps persist.

**Classical ingredients and priority boundary.** Continuity of finite matrix resolvents and eigenvalues; Compact subsequences and closed inequalities; Transient finite substochastic matrices. Stability of the exact counted-memory reset frontier derived from the compact certificate and transient optimal realization.

**Limits.** Dimensions and alphabets are fixed; perturbations remain valid reset instruments with a positive cost floor and no closed failure set. The discrete threshold can jump, including when failure effects vanish.

## 4. The complete action-cover cost frontier

**Native locator:** main, theorem 4.4, page 13; `thm:r78-cover-frontier` in `sections/53-reset-memory-frontier.tex`.

**Hypotheses.** The explicit reset family associated with nonempty proper subsets A_1,...,A_s of [q], q>=2: reset states e_i, E_(a,i)=(r/s)I, cost entries 1+1_(a notin A_i) on e_i and 3+1_(a=j) on f_j. 0<=r<1, finite live memory M>=1, and the same all-initial-state pure-start controller class. H is a set of at most M-1 continuing pure actions; U(H) are the uncovered A_i, b_a(H) counts uncovered sets omitting a, and lambda=r/[s(1-r)].

**Conclusion.** The exact entire frontier is V_M=3+r/(1-r)+min_(H:|H|<=M-1) min_(1<=k<=q) [1+lambda sum_(j<=k) b_(j)(H)]/k. An optimum uses pure continuing rows and an initial row uniform on k smallest uncovered-penalty actions. The finite enumeration includes arbitrary ties and r=0. After the common term is subtracted, each fixed-M frontier is a continuous nondecreasing piecewise affine concave function of lambda.

**Direct logical prerequisites.** `thm:r78-palette-normal-form`

**Inherited mechanisms and contextual authorities.** `thm:r77-reset-universality`

**Proof mechanism.** Solve the row-choice Bellman equations explicitly for action-independent reset transitions, compute the dominating start eigenvalues, and obtain the compact continuous row objective. Separate concavity allows all rows except the initializer to be purified at an optimum. They form H; hit states have zero penalty and unhit states have the initializer penalty, producing b(H) dot p. Introducing t>=max p reduces the linear allocation to saturating the smallest coefficients; on each interval [1/(k+1),1/k] the result is affine, so t=1/k endpoints and uniform supported rows suffice. Finite minimization proves the formula and realization. The endpoint r=0 and positive-r cover threshold are checked separately.

**Classical ingredients and priority boundary.** Finite Bellman equations with action-independent transition; Concave minimization on a simplex; Capped simplex linear optimization and rearrangement; Finite lower envelopes of affine functions; Classical transversal/set-cover combinatorics. A closed all-memory cost spectrum and exact synthesis formula for every finite action-cover incidence system in the retained physical reset family, not merely its saturation threshold.

**Limits.** The set-system enumeration retains combinatorial hardness; there is no claim of a polynomial algorithm. Pure continuation is proved for this family, not for arbitrary reset instruments. The original quantum discrimination risk and timing frontiers remain different problems.

## 5. Arbitrarily long strict memory hierarchies

**Native locator:** main, corollary 4.5, page 14; `cor:r78-strict-hierarchy` in `sections/53-reset-memory-frontier.tex`.

**Hypotheses.** For every n>=2 take the explicit action-cover instrument with s=q=n, A_i={i}, r=1/2, in Hilbert dimension 2n. M>=1 live labels with counted pure initialization, mandatory success stopping and no additional observations. For the noncommuting perturbation, X=|e_1><f_1|+|f_1><e_1| and only E_(1,1) is changed by epsilon X, with 0<epsilon<(n-1)/(8n^2).

**Conclusion.** For the unperturbed rational instrument V_M=4+1/n+(n-1)max(n-M+1,0)/n^2, giving n consecutive strict gaps with success probability 1/2 and actual costs in [1,4]. Its first-residual certificate is exactly D_M=(V_M-V_*)/2. The strict hierarchy persists in a valid open neighborhood and under the explicit noncommuting effect perturbation. The latter has positive failure/success effects, unchanged mean cost operators I<=G_a<=4I, a joint physical paid-cost realization with costs {1,9}, and |V_M(epsilon)-V_M(0)|<=4epsilon.

**Direct logical prerequisites.** `thm:r78-cover-frontier`, `prop:r78-frontier-stability`, `thm:r77-reset-gap`

**Inherited mechanisms and contextual authorities.** `thm:r77-reset-universality`

**Proof mechanism.** Evaluate the finite cover-spectrum formula by the two ranges k<=u and k>=u, showing a minimum at k=n and then largest allowable H. Repeat with the first-residual coefficient to compute D_M. Continuity protects the finite collection of gaps. For explicit noncommuting perturbations verify positivity of E and B, a nonzero commutator with G_1, unchanged reset expectations, and the uniform 4epsilon spectral perturbation bound. Adjacent gaps stay larger than (n-1)/n^2-8epsilon. A success-effect split supplies a full CP joint report/cost realization, avoiding any unproved compatibility of noncommuting cost and failure observables.

**Classical ingredients and priority boundary.** Spectral norm perturbation bounds for largest eigenvalues; Finite simplex allocation; Measure-and-prepare completely positive instruments; Continuity of attained optimal values. An explicit arbitrary-length exact memory hierarchy with matched optimal upper and lower values, a strict comparison with the inherited one-residual lower certificate, and persistence beyond commuting primitive effects.

**Limits.** n>=2 is necessary for strict gaps. The exact formula and D_M ratio concern only the unperturbed displayed family. Perturbed mean costs retain [I,4I], but the demonstrated physical realized cost support is {1,9}, not [1,4]; initial success probability need not remain exactly 1/2. No other paper frontier or general quantum advantage is inferred.

## Retained authority and unresolved questions

All 235 predecessor proof records retain every nondisplay field unchanged. Current document, number, page, source and locator-description fields are refreshed. The original ledger remains byte-identical, as do the R74/R75/R76/R77 addenda and all protected proof bodies. Edition-relative words such as 'new' within an unchanged old record refer to that original edition, not to R78.

The original general-M squared-sign risk frontier, nonreset or optional-stopping tied control, unrestricted high-contrast classification for every finite group, the matching unrestricted-decoder approximation rate, intermediate timing, coefficient-bit/precision/program/workspace costs, unknown-model recovery and independent Theta objectives remain distinct. In particular matrix parameter-feasibility equivalence does not classify every off-boundary positive factorization, and a sharp excursion probability is not a sharp universal approximation cost. The inherited R76 matching leading logarithm applies only to the stated fixed physical density dictionaries with Born terminal decoders, at fixed positive target budget and a fixed badly approximable phase.

## Evidence categories

The written proofs are ordinary author arguments. Author-team AI challenges, finite exact/floating diagnostics, native compilation, source hashing, independent human assessment and editorial decisions remain separate evidence types. General real quantifier elimination is an existence/computability ingredient; these maps do not claim it was executed. The R65 deposited report is not reclassified as a review of R78.

Regenerate with `python build_theorem_map.py` and check with `python build_theorem_map.py --check`. Missing labels, a different inherited authority, altered nondisplay old proof fields or an incomplete current statement inventory are rejected.
