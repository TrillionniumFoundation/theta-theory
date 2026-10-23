# R79 author proof audit: regularization at an unchanged memory budget

## Scope and evidence status

This is an internal author-side audit of the written arguments, not an external referee report, an independent human expert endorsement, or formal verification. The audit compares the new Section 55 with the retained Sections 12, 17, 19, and 26. It does not certify worldwide novelty or a journal's editorial judgment.

The principal audited source is `55-label-restart-stability.tex`, SHA-256 `9c185b61316334bd8d2971fceca3657285b2958fa6f152b576b74b713d46f2d2`. The integrated `sections/55-memory-regularization.tex`, SHA-256 `b66250b30fc8142169050dbf3c4cb720d0416c4238a10dde086a662b5fcee6a0`, differs only by its explicit paragraph crediting the inherited centered estimate and completion theory and the surrounding external literature. Its mathematical statements and proofs agree with the audited source.

**Conclusion:** no proof error was found in the new same-memory restart, global-witness, directed perturbation, or uniform-in-memory modulus arguments under their stated hypotheses. Several supporting results are inherited and must not be advertised as new discoveries. The main distinction is preservation of the exact finite live-label budget while obtaining full-space bounded witnesses and transferring an infinite-horizon cost bound across changing reachable supports.

## Inherited results and the precise additional result

| Ingredient | Retained antecedent | Appropriate R79 treatment |
|---|---|---|
| Product CP evolution of a finite stochastic controller | Section 12, equations `memory-T`–`memory-g` | Inherited framework |
| Reachable-support stabilization within the total physical-label dimension | Section 12, Lemma `reachable-support` | Inherited theorem; the new Section 54 recapitulates it |
| Necessary and sufficient supported cost potentials and spectral transience | Section 12, Theorem `memory-certificate` | Inherited theorem, including inaccessible recurrent blocks |
| Compact-controller attainment and finite algebraic synthesis | Section 12, Corollary `memory-algebraic`; Section 26, Theorem `r67-algebraic-memory` | Inherited mechanisms, specialized and assembled for the current cost frontier |
| No-dark-subspace criterion and a common one-row fallback | Section 17, Theorem `primitive-fallback`; Section 19, Lemma `compact-fallback` | Inherited, including compact model families |
| The normalized-output centered effect bound with the factor one half | Section 19, equation `effect-distance` | Inherited estimate; the new use is on regularized full-space cost potentials |
| Finite-history completion, modelwise offline comparison, and square-root primitive bounds with memory allowed to expand | Section 19, Theorem `compact-risk` and Corollary `optimal-robustness` | Inherited construction and rate mechanism |
| Finite-history convergence to unrestricted control | Sections 17 and 19, constructive feasibility/completion results | A current cost-only corollary, not a new completion principle |
| Restarting the already counted initial label to obtain bounded all-label cost at the **same** live-label budget | Section 55, Theorem `r79-label-restart` | The substantive additional structural step identified in this audit |
| Infinite-horizon witness transfer and a modulus simultaneous for every fixed memory, without enlarging it | Section 55, Theorem `r79-frontier-stability` | The resulting additional fixed-memory conclusion |

The older compact-risk theorem changes memory through a depth-dependent history tree and may use an initial mixture role. Its existence of an `O(sqrt(error))` modulus is therefore not, by itself, the new fixed-memory result. Conversely the exponent, trace-distance centering, and compactness machinery are not new priority claims.

## 1. Restart generations and the initial cost bound

The segment argument is valid because a segment starts at the existing initial label with an arbitrary physical density matrix in one fixed model. Up to the first marked restart coin it follows the original controller. Nonnegative paid costs make its expected segment cost at most `b`; the lower cost floor gives original expected duration at most `b/c_*`.

The probability of a marked restart before success is at most `epsilon*b/c_*`. One exact coupling expression is `E[1-(1-epsilon)^(tau-1)]`, bounded by `epsilon*E[tau-1]` and then by the displayed estimate. The proof uses a slightly looser bound, correctly.

Conditioning on an earlier segment's complete history leaves a physical density matrix and the same fixed model. The original uniform bound applies to both. Thus reaching segment `j+1` has probability at most `(epsilon*b/c_*)^j`. Summing finite generations and then applying monotone convergence establishes `U_epsilon=b/(1-epsilon*b/c_*)`. This avoids the invalid circular inference from an inequality involving an a priori possibly infinite total cost.

No restart flag needs to persist: the independent within-call coin only writes one of the existing labels. Segment boundaries are proof variables. The physical state is never reset.

## 2. Full-space witnesses without another label

From an arbitrary label, continuing for `n` calls without success or a marked restart has probability at most `(1-epsilon)^n`. Expected first-segment duration is therefore at most `1/epsilon`, and its expected cost is at most `c^*/epsilon`. The continuation after a marked restart costs at most `U_epsilon`. Hence every model and every physical state at every label has cost at most `K_epsilon=c^*/epsilon+U_epsilon`.

The positive floor and finite-dimensional positivity then imply transience of the full product map and convergence of its cost series. The exact witnesses satisfy `0 <= W_k <= K_epsilon I` globally, with `W_1 <= U_epsilon I`. This step validly repairs the lack of any common bound for the *unregularized* reachable potentials. It does not assert that those original potentials are bounded or continuous.

## 3. Primitive perturbation and its constants

Including the scalar success outcome gives a normalized output state. Its difference between two models has trace zero. For any block continuation observable `0 <= Z <= K I`, centering at `K I/2` gives absolute pairing at most `K*eta`, where `eta` is one half of the complete output trace norm discrepancy. Averaging the unchanged command row and stochastic label updates preserves this bound. It is an induced-state estimate for classical feedback on the specified physical system, not an unproved diamond-norm statement with external entanglement.

The cost error contributes at most `zeta I`. Consequently the source witness has target drift at least `K_target-(zeta+eta*K)I`. With `delta=zeta+eta*K<c_*` and `alpha=(1-delta/c_*)^(-1)`, the identity `(alpha-1)c_*=alpha*delta` proves that `alpha W` is a target supersolution. No spectral gap of the unregularized controller is used.

For `epsilon=sqrt(eta)`, the stated smallness conditions imply `U_epsilon<=2B`, `U_epsilon-b<=2B^2*sqrt(eta)/c_*`, and `delta<=c_*/2`. Expanding the denominator gives the intermediate bound

`(2B^2+4B*c^*)*sqrt(eta)/c_* + 8B^2*eta/c_* + 4B*zeta/c_*`.

Since `eta<=sqrt(eta)` on `[0,1]`, the published constant `10B^2+4B*c^*` is correct. It is conservative. No sharpness of this constant or of the square-root exponent has been proved.

When `eta=0`, the proof correctly takes a limit through positive `epsilon`; it never substitutes zero into `c^*/epsilon`. The resulting directional difference is at most `b*zeta/(c_*-zeta)`, which is bounded by `2B*zeta/c_*` under the given hypothesis and hence by the stated `4B*zeta/c_*`.

## 4. Quantifier audit and support changes

The same regularized controller is used throughout the source family and target family. For each target model, a nearby source model and its witness are selected only in the proof. Both the instrument and cost discrepancies must hold for that same pair. The model remains fixed during the run. The comparison does not reveal a parameter or permit an adaptive switching adversary.

The constants depend on a common positive cost floor, cost ceiling, and one-row cost cap, but not on `M`. A fixed full-support fallback has a continuous invertible resolvent on the compact feasible source family; the same property and a common cap persist in a neighborhood. This justifies the local statement for nearby compact model families. The new theorem controls **optimal values**, not continuity of optimizing labels, supports, or unregularized witnesses.

The result is a cost frontier with mandatory success stopping. It does not contradict Section 19's discontinuity example for a *terminal-risk optimization constrained at a fixed boundary cost*. It must not be used to remove that older theorem's positive budget-slack condition.

## 5. Completion corollary

A cost-`b` history policy has expected duration at most `b/c_*`, so survival after `T` calls is at most `b/(c_*T)`. Its paid prefix costs at most `b`. The common fallback can start from the actual posterior physical state, giving additional cost at most `C_0*b/(c_*T)`.

The prefix controller stores each action/report history of length below `T` and one fallback label. This gives exactly the stated upper count `1+sum_(t=0)^(T-1)(|A||Y|)^t`, including the initial empty history. For an empty nonterminal alphabet the empty-history term is one and all later counts are zero; the claim is then immediate because every call terminates.

Passing to the infimum over history policies does not require an attaining history policy. Finite stochastic controllers belong to the common behavioral class by the retained causal realization argument: conditioning their private label path on a complete command/report history cancels the common physical path factor, so the induced causal command kernel is independent of the hidden model. The reverse value inequality and the monotone limit follow. Uniformity in `M` permits passage of the new perturbation bound to this limit.

## Remaining qualifications

No additional mathematical blocker was identified in Section 55. The all-initial-state guarantee, nonnegative costs with a strictly positive floor, globally legal commands, unchanged observation port, fixed latent model, and mandatory success stopping are used in the proof and must remain explicit. The audit establishes no general finite-memory saturation, optional-commitment theorem, sharp modulus, polynomial-time synthesis, formal proof verification, or resolution of the separate squared-sign minimax-risk frontier.
