# Research status — General Theta Foundations I, R74

## Identity and controlling continuation

**General Theta Foundations I: Acquired Geometry and Causal Resource Transfer** remains the paper being developed. Its scientific subject is the relation between information acquired by causal experiments, their predictive states, and the resources needed to realize and use those states. The intended mathematical standard remains that of Annals of Mathematics, Acta Mathematica, Inventiones Mathematicae, and the Journal of the American Mathematical Society. This document states proved results, exact scopes, and remaining research obligations. It is not an editorial verdict or a prediction of acceptance.

The controlling complete predecessor is R73 mathematical source commit `e9d5f2765a2369ed7e136ca02e47fda8f3e9a49b`, paper tree `0507d04ad0bebd20cb0ce609ab94f7cc67d11f56`, at `papers/General-Theta-Foundations-I-restart/r73-reversible-normal-form`. Its completed publication is commit `39980d65d6665e52c30aa340cfb0e2eb199c0f9a`, preserving that mathematical tree. R74 is a new sibling source; the predecessor and historical branches remain unchanged.

The latest substantive deposited report is still R65, commit `358481b21ceeeedb1205ebd30f86982e32a2cb04`, blob `d1ff9c5662390156ee212c82b173e86a21180e84`, SHA-256 `8c7d45d762736009fda667621fdf5019fa934f5f45f39364c747f837e6d7343c`. It evaluated R65 source `0469eb4f852eeea953cb3725d4b34dfdd2bf9d36`, not R73 or R74. Several requests were already answered by R66–R73. The current history audit found no later independent report; its absence is not inferred merely from a branch-name ordering. Current source and delivery SHAs, native PDF hashes, and actual executions are supplied by the final receipts linked from `START_HERE.md`.

## The current theorem center

The inherited reversible classification and stochastic normal form establish the starting point. For a finite-dimensional compactly reversible response, exact finite stochastic realizability is equivalent to finiteness of the observable group. Every finite realization reduces, without increasing its live-label count, to a permutation core and at most one counted initializer. For a finite observable group `G`, residual count `N`, and least positive permutation-factorization size `kappa_G(b)`,

\[
 m(b)=\min\{N,1+\kappa_G(b)\}.
\]

This is a complete inherited theorem, not a conjectural assumption of R74. The preparation and decoder in the factorization must be nonnegative and normalized. The dimension of a containing permutation module is a lower bound; it need not be the optimum at full contrast. R74 studies and partly resolves that positivity problem, then compares it with the resource carried by observed instrument branches.

### 1. Universal finite-group attainment at small terminal contrast

Let `pi` be the group average of a nonconstant response and `b_t=pi+t(b-pi)`, `0<=t<=1`. `thm:r74-low-contrast` proves, for every finite observable group and every finite outcome alphabet, that some explicit `t_0>0` satisfies

\[
 \kappa_G(b_t)=\nu_G(V_b),\qquad
 m(b_t)=\min\{N,1+\nu_G(V_b)\}\quad(0<t\le t_0).
\]

Here `nu_G(V_b)` is the least cardinality of a permutation action whose real module contains the observable response module. The proof embeds the zero-average part, perturbs the uniform preparation within the probability simplex, and scales a zero-row-sum decoder perturbation. Its explicit constants ensure positivity. Outputs with zero group average are identically zero and are harmless. Positive contrast preserves the group, module and residual equality pattern; zero contrast is a separate one-label degeneracy.

This is a theorem for arbitrary finite groups, not a statement restricted to an abelian, fixed-rank, binary, or qubit model. It does not say that small positive contrast makes an infinite compact observable group finitely realizable: the unchanged infinite group still obstructs every finite exact realization. For prepared unitary commands the contrast is realized by mixing the terminal POVM with the constant group-average readout, without changing the commands.

`thm:r74-contrast-thresholds` further proves that, for each core budget `k`, the set of feasible contrasts is a closed initial interval `[0,tau_k]`. Its endpoint is attained and lower memory is retained at that endpoint. The thresholds are nondecreasing, `tau_N=1`, budgets below the module minimum have endpoint zero, and the module-minimum budget has a positive endpoint. Algebraic input makes the thresholds computable real algebraic numbers. This does not give a universal elementary closed formula or a polynomial algorithm.

### 2. Exact quotient optimization and payoff duality

If every subgroup of `G` is normal, `lem:r74-normal-orbits` absorbs the mixed preparation inside each quotient orbit into its decoder. Repeated copies of the same quotient can be merged. This reduces positive factorization to a finite selection of distinct subgroups `H` with cost `sum_H [G:H]` and nonnegative quotient tables `f_H` of constant row mass `p_H`, satisfying

\[
 \sum_c f_H(q,c)=p_H,\qquad
 \sum_Hp_H=1,\qquad
 \sum_Hf_H(Hg,c)=b(g,c).
\]

`thm:r74-quotient-lp` proves that the least feasible cost is exactly `kappa_G(b)`. The minimal observable residual count in this class is `|G|`; hence the pure-start minimum is `min{|G|,1+kappa_G(b)}`. Rational data admit rational optimal tables. Data in a specified real algebraic number field admit a controller in that same field. These conclusions include every finite abelian group and also the finite nonabelian groups whose subgroups are all normal. Normality is used in the absorption proof and is not omitted.

For a selected family, `thm:r74-quotient-dual` computes its support function as the maximum, over its quotients, of a sum of cosetwise best-output payoffs. All signed-payoff inequalities are necessary and sufficient for feasibility. Infeasibility has a strict rational witness, and its margin yields a quantitative table-perturbation exclusion. Contrast endpoints have attained primal and dual LP descriptions, including degenerate affine-hull cases. The budget optimum still requires a finite combinatorial family selection: one family witness does not automatically separate the entire union of all low-cost families.

For abelian groups, `cor:r74-abelian-cover` computes the module minimum from character support and quotient-character covers. It is exact for sufficiently small contrast. At larger contrast, the actual table can force additional positive states even while that support is unchanged.

### 3. Matching model laws and a robust finite-table lower

The new exact examples expose the distinction between representation data and positivity.

| Response family | Fixed positive-parameter data | Exact core / pure-start memory |
|---|---|---|
| Prepared-qubit `S_3` response `beta_t(g)=1/2+(t/4)uP_gu^T`, `u=(1,-1,0)` | Observable group `S_3`, dimension three, six residuals | Core three and pure-start four for `0<t<=2/3`; core and pure-start six for `2/3<t<=1`; one at zero. |
| Five-character circuit on `(F_2)^4`, `beta_t=3/8+(t/8)sum_{i=1}^5 chi_i` | Dimension six, sixteen residuals, permutation-module minimum ten | Core ten / pure-start eleven for `0<t<=3/5`; core twelve / pure-start thirteen above `3/5`; one at zero. |

The `S_3` lower examines every action of size at most five. An explicit four-matrix spanning argument forces the standard-component preparation and decoder to have the stated rank-one directions; their separate probability bounds give `t<=2/3`. The upper realizes every group response, including the endpoint.

The four-bit lower classifies every possible quotient family of cost at most eleven. Its active character blocks must partition a five-element circuit into singletons and pairs. A signed payoff for each partition has nonnegative averages on the relevant quotient fibers and target value `(3-5t)/8`. This excludes all those families above `3/5`. A degree-ten construction attains the low branch; a four-point plus eight-point construction attains the high branch by exact Fourier cancellation.

`cor:r74-circuit-robust` extends the lower to any binary probability table on the same group and generator quotient within supremum distance `(5t-3)/18` of the target, for `t>3/5`. All five active coefficients survive, and every candidate partition has a witness of normalized absolute sum at most `9/4`. Consequently its core needs at least twelve labels and its pure-start memory at least thirteen. This is a sufficient lower neighborhood, not a sharp radius or a matching thirteen-label upper for every perturbed table. The sixteen-dimensional diagonal physical implementation of this example is classical; no quantum advantage is claimed for it.

### 4. A common contracting probability-response realization

`thm:r74-contraction` treats a supplied linear response `b(w,c)=p_c+ell_c(x_w)` with `x_{wa}=F_a x_w`. Assume one norm contracts every command by `rho<1`, the actual response is probabilistically valid, and a radius `r` satisfies `r||ell_c||_*<=p_c` for every output. A finite net supplies a polytope containing `rho` times the unit ball and contained in the unit ball, invariant under all command maps after scaling. Transient prefix labels lead into this common recurrent polytope. With `a` commands and `rho^(T-1)||x_0||<=r`, the count is at most

\[
 \sum_{j=0}^{T-1}a^j+
 \left\lceil\left(1+\frac{2}{1-\rho}\right)^n\right\rceil.
\]

All decoder rows are bounded probabilities; the empty-word label and first transition are counted. This is a sufficient construction, without minimality or efficiency claims. It uses classical invariant-polytope realization and should be assessed as a quantitative corollary with these operational conventions. A supplied uniform product-decay certificate yields a suitable common norm; the theorem does not decide joint spectral radius.

This differs from the retained unique-decision convergence theorem: a discontinuous sign selector can keep changing despite physical contraction. It also does not contradict the retained leakage obstruction with a vanishing limiting output, because that example fails the whole-ball decoder margin.

### 5. A sharp conditional-memory law in a fixed qubit

`thm:r74-depolarizing-obstruction` uses three completely positive branches on a qubit. Their sum is exactly the completely depolarizing channel, and their probabilities are respectively `1/8`, a value in `[1/16,3/16]`, and a value in `[11/16,13/16]`, for every incoming state. From `I/2` the outcome process is stationary and one-dependent. Its word-Hankel rank is exactly three.

If the conditional phase has order `q>=3`, the minimum classical hidden-state count is exactly `q` with a free mixed initialization and `q+1` with a pure counted initialization. A regular `q`-gon gives one positive realization for all branches. The strict third-branch bound `5/11<1/2` keeps its normalized output inside that polygon. A stationary hidden initial distribution also exists without enlarging the count.

For the lower, the cylinder `1 0^n 1` carries three distinct exponential modes. Every classical realization has an active nonnegative zero-branch block whose relative peripheral spectrum contains the phase. Irreducibility propagates the phase relation to every positive edge, so every cycle length is a multiple of `q`. At exactly `q` states the block is a weighted full cycle. A pure starting point and the probabilities of `0^n` force all weights to be `1/8`; the probabilities of `0^n1` force constant terminal masses, contradicting the oscillating cylinder already at `11`. This proves the exact initializer charge. A phase of infinite order cannot occur in any finite positive block, ruling out all finite classical realizations with arbitrary real entries.

The irrational algebraic phase `(3+4i)/5` yields rational superoperator coefficients and infinite memory. This is not the first quantum process without a finite classical realization, the first one-dependent non-HMM process, or the first commensurate/irrational phase memory distinction. The manuscript credits the existing positive-realization and FRDN antecedents, including the explicit comparison in Fanizza–Lumbreras–Winter. The new assertion is the simultaneous fixed-qubit, rank-three, uniform-outcome-floor, exactly depolarizing and one-dependent family with the precise mixed/pure resource law. Its lower is unrestricted classical response memory, stronger than a lower restricted to physical-state dictionaries.

## Inherited results and corrected statuses

The complete R68 posterior-interiority theorem is retained as a proved physical realization mechanism, not counted as a new R74 result. `thm:r68-instrument` already preserves adaptive command/report laws, complete stopped laws including nontermination, terminal measurements and nonnegative path costs; it counts prescribed preparations, gives sparse branch rows, and has an algebraic construction. `thm:r68-noise-exponent` already gives the sharp fixed-dimension small-noise exponent for universal **state-positive** dictionaries, including a finite-command lower example. That exponent is not a lower bound for arbitrary abstract classical realizations of every selected instrument. Provisional duplicate drafts were archived as superseded author research and removed from the active theorem list.

The four-period response

\[
 b_\alpha(n)=\tfrac12(1+\alpha^n\cos(\pi n/2))
\]

already has its complete count from the retained R69 first-sector theorem:

\[
 m(b_\alpha)=
 \begin{cases}
 2,&\alpha=0,\\
 3,&0<\alpha\le1/\sqrt3,\\
 4,&1/\sqrt3<\alpha\le1.
 \end{cases}
\]

The new labeled corollary records this inherited consequence. The earlier period-four finite-probe inequality and its sufficient rational interval remain valid separate certificates. The exact first transition for this family must not remain on an open-problem list.

The R66/R67 robust optimal-face and anchored stochastic realization criteria remain complete on the declared stopping-rigid class, including model-dependent probabilities and ties. The necessary and sufficient stopping-rigidity theorem and explicit nonrigid example remain controlling. R70 relative-spectrum and leakage laws, R71 arithmetic envelopes, and R72/R73 reversible realization, normal form, rank rigidity, factorial separation, algebraic synthesis, finite-word equivalence and stable-memory results remain active with full proofs.

The current source also preserves the original causal and actual-history transfer, predictable-state compression, finite-resource synthesis, performed-law compactness, minimax and dual attainment, finite-width qualifications, reusable continuation, two-stage reset, memory/communication distinction, rank-constrained optimal discrimination, spectral/variational principles, acquired geometry and strategy realizability. Local geometry remains local. General fixed-acquisition no-message criteria are not reduced to a low-dimensional or equal-prior example. Independent finite-order measurement/reset sources and the complete independently compiled R58 companion keep their own immutable identities and proof authority, as recorded in `PRESERVATION_MAP.md`.

The native statement index is a source/number/page inventory, not a novelty count. The R74 addition includes an explicitly inherited four-period corollary, supporting lemmas, classical-method consequences, and model specializations. Removing duplicate R68 statements does not remove the original mathematics or its current complete proofs.

## Remaining research obligations

| Scientific problem | Established contribution and exact boundary | What is still needed |
|---|---|---|
| General-`M` squared-sign minimax risk | Exact one-/two-label formulas, strict attained finite-memory gaps, same-boundary prefix approximation, and additional exact response-memory tools are retained. | A sharp formula or matching asymptotic for `V_{p,alpha,M}-V_{p,alpha}` at arbitrary `M`, with admissible minimizing controllers. |
| General nonrigid boundary ties | Robust tied optimal faces and finite stochastic realization are classified on the stopping-rigid class; nonrigidity has explicit paid examples. | A complete optimum/attainment/density classification when stopping freedom and tied robust choices interact outside that class. |
| Several-command optimal feedback | All-command response realizations and exact same-policy instrument simulation are available under their stated conditions. | A general criterion for optimal command choice and stopping with the original report information, without exposing a simulator's private state. |
| Positive factorization for general nonabelian groups | Exact variational formula, all-group small-contrast attainment, attained thresholds, algebraic synthesis, and normal-subgroup LPs are proved. | Sharper structural formulas and tractable optimization beyond normal stabilizers; representation data alone are insufficient at high contrast. |
| Other damping transitions | Four-period first transition is closed; periodic partition, leakage, sector and stable-neighborhood theorems cover their stated classes. | Complete thresholds for other responses and uncovered transition regions; terminal contrast is not repeated damping or branch noise. |
| Timing resources | Existing delayed-release thresholds and valid phase-type bounds remain proved. | The exact intermediate phase-type frontier and matching general tradeoffs. |
| Arithmetic memory growth | The arbitrary-phase logarithmic exponents and badly-approximable criterion remain proved. | Sharp constants and further simultaneous-scale questions; no particular irrationality exponent for `(3+4i)/5` is inferred from algebraicity or finite samples. |
| Computational resources | Exact rational/algebraic controllers and finite certificates can be constructed in declared classes. | Efficient general algorithms and matching table-bit, arithmetic-time, precision, workspace and exact-sampling lower bounds. |
| Unknown models and predictive recovery | Fixed-law quotients and exact supplied-model observable reductions are proved. | Learning or certifying a generally unknown predictive quotient from finite observations, with necessary additional assumptions. |
| Wider Theta construction | General Theta results retain their mathematical dependencies and research role. | Independent A1/A2, B4/C2, process-limit, nonlinear-generator, filtering/posterior and other pipeline assertions require their own proofs. |

These questions retain the original ambition. They are not declared impossible merely because the present theorem does not solve them, and a positive result in one model does not complete the larger programme. The specific obstructions in the paper are proved boundaries of specific realization problems, accompanied by positive constructions and exact laws where established.

## Verification, attribution, and independent assessment

The source contains complete English proofs, a paired current supplement, explicit dependencies, preserved historical bodies, primary-literature comparisons, and exact diagnostic programs. A separately assigned author-team AI challenge reconstructed the principal proofs, checked the new quotient witnesses independently, and detected the inherited R68 duplication. That role is not an independent human referee or a formal proof system.

The actual strict build receipt controls the final source SHA, source tree, manifest, native PDFs, theorem-index comparison, diagnostic source hashes, and ordinary/optimized execution totals. A draft compilation, source seal, historical CI success, proof challenge, or ref scan is not substituted for a fresh source-bound run. Hosted CI and remote publication have their own observed matching identities. The general LP or algebraic procedures are proved available; finite example diagnostics do not constitute execution of every general optimization or quantifier-elimination problem.

The complete source and evidence are presented for the next independent referee. Mathematical priority, the strength of the central contribution, and journal suitability remain subjects for that actual assessment. No human expert approval, editorial decision, or acceptance is created by this author revision.
