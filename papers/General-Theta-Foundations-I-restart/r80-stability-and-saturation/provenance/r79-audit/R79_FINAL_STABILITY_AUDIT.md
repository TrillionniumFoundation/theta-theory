# R79 final focused author-side stability audit

## Identity, scope, and conclusion

This is an internal author-side mathematical challenge and source-reference check performed by an AI collaborator. It is not an independent external referee report, a human specialist endorsement, a formally verified proof, or an editorial judgment. It does not replace the written proofs. No claim about native compilation or hosted CI follows from this record.

The focused read covered the complete integrated `sections/55-memory-regularization.tex`, including the final conditional-label-path argument in `cor:r79-history-limit` and the appended `cor:r79-positive-success`. The primitive/interface definitions in Section 54 were checked where they are needed by those arguments. The current response's item headings and native labels were also checked mechanically.

**Conclusion:** no blocking mathematical defect was found in this focused read at the exact source identities below. In particular, the positive-success comparison is valid with the same controller labels and uniformly over the label budget; its two local scalar coefficient-sharpness statements are supported by the displayed examples. The conditional label-path cancellation supplies a model-independent visible-history realization under the declared observation and initialization conventions. The limitations recorded below remain part of the conclusions.

Source identities were read at **2026-10-23 07:20:40 UTC**. These are hashes of the actual working-tree files inspected; this audit does not invent a future commit identity. The final publication manifest must bind these contents to the actual source/publication commits. A later modification to any controlling mathematical file requires checking whether this audit still applies.

| Inspected file | Bytes | Lines | SHA-256 |
|---|---:|---:|---|
| `sections/55-memory-regularization.tex` | 22,664 | 506 | `cd48963092cbda6958a852249327644c023a0db7835a729e87634ecfb2117dc1` |
| `sections/54-robust-instrument-frontier.tex` | 23,770 | 501 | `5dd6e614497946e4407908e905daf555efca8fba39e26dfc163ff2f2fae08df6` |
| `RESPONSE_TO_REFEREE.md` | 66,833 | 392 | `bbda010fa99c7ef19bc01c1c100eeeedd0494dda84bb9ccbc3dea3e5561f0dd5` |

## 1. Same-label restart: finiteness before rearrangement

Location: `thm:r79-label-restart`, equations `eq:r79-label-restart` through `eq:r79-global-witness`.

The restart modifies only the existing post-failure update row. A fresh coin writes the already counted initial label with probability epsilon. The primitive CP map, physical posterior, fixed hidden model, command rows, terminal rule, and number of live labels are unchanged.

Starting from label 1, the first segment follows the original controller until success or the first restart coin. Its expected cost is at most b. The positive conditional mean-cost floor implies an expected number of calls at most b/c_*, hence a probability of restart before success at most epsilon b/c_*. After a restart, the physical state may be arbitrary. The original bound can be reused precisely because it holds for every initial density matrix and every fixed model.

The proof establishes finiteness by the geometric bound on the probability of reaching successive restart generations, followed by monotone convergence. It does not infer finiteness by rearranging an inequality involving a possibly infinite unknown cost. This distinction is necessary.

From any other label, the probability of avoiding both success and restart for n calls is at most (1-epsilon)^n. The first segment therefore costs at most c^*/epsilon in expectation. Any remaining cost starts from label 1 and is at most U_epsilon. This proves the stated global K_epsilon bound. Positivity and the positive cost floor then justify full-product transience and the exact global cost series. No inaccessible unregularized block is assumed proper.

**Scope retained:** the all-initial-state quantifier is essential to this proof. A restricted set of preparations cannot be substituted unless a separate argument shows that every conditional post-restart state lies in a set with the same bound. The operation is a classical label restart, not a quantum reset.

## 2. Centered primitive comparison and fixed-model quantifiers

Locations: `lem:r79-centered-perturbation`, `thm:r79-frontier-stability`.

The normalized output map includes all failure blocks and the scalar success outcome. A continuation observable has failure blocks between zero and K I and a zero success block. Subtracting K I/2 is permitted because the complete output difference has trace zero. The resulting estimate is K eta, rather than 2 K eta. Omitting the success output would invalidate that trace-zero justification.

The estimate applies to every physical density matrix, so its scalar form gives the claimed Hermitian operator-order inequalities. No auxiliary entangled register is included in the metric or silently made available to the controller.

For the scaling step, the target cost floor gives

`alpha (K_target - delta I) >= K_target`

when `alpha=(1-delta/c_*)^{-1}` and `delta<c_*`. This is the correct use of the target floor. A bounded positive supersolution then bounds the target cost by iteration of the positive continuing map; the argument does not need to assume target properness in advance.

In the family comparison, one source model may be paired with each target model only as an offline witness. The same command and update rows are used in every model, and a model stays fixed throughout a run. Both instrument and cost discrepancies must hold for the same pair. The proof respects these requirements.

For the explicit modulus, epsilon=sqrt(eta), b<=B, and the two stated smallness conditions yield U_epsilon<=2B and delta<=c_*/2. The displayed arithmetic gives the stated coefficients. The eta=0 case is handled by the separate epsilon-to-zero limit, avoiding an invalid choice epsilon=0 in the restart construction. The compact-neighborhood argument uses the common one-row resolvent and preserves a local properness/cost cap; it does not assert continuity of the optimizer or its support.

**Scope retained:** the square-root exponent is a proved upper bound, not a proved optimal exponent. Constants are uniform in M but depend on the physical cost bounds and common fallback cap.

## 3. Conditional label-path cancellation in the history comparison

Location: the final part of the proof of `cor:r79-history-limit`.

The paragraph asserting that finite controllers induce model-independent visible-history command kernels is valid under the Section 54 interface. A direct factorization makes the reason explicit. Fix a nonterminal visible history

`h=(a_0,y_1,a_1,y_2,...,a_{t-1},y_t)`

and a compatible private label path `lambda=(k_0,...,k_t)` with the prescribed pure initial label `k_0=1`. Define the controller weight

`q_lambda(h)=product_{i=0}^{t-1} p^{k_i}_{a_i} u^{k_i,a_i,y_{i+1}}_{k_{i+1}}`.

This nonnegative weight depends on the fixed controller and visible history only. The unnormalized physical branch is the same for every compatible label path:

`Phi_h^theta(rho)=Phi^theta_{a_{t-1},y_t} ... Phi^theta_{a_0,y_1}(rho)`.

Thus the joint probability of h and lambda is

`q_lambda(h) trace(Phi_h^theta(rho))`.

Whenever the visible history has positive probability, its physical branch factor cancels from the conditional distribution of private label paths. The next-command kernel is consequently

`sum_lambda q_lambda(h) p^{k_t}_a / sum_lambda q_lambda(h)`.

This expression depends on neither theta nor rho. If the denominator is zero, the history is impossible under the controller for every model and preparation, and one common arbitrary kernel can be assigned. If only the physical branch factor is zero for a particular model, the same algebraic kernel remains defined by the controller weights and causes no change to that model's performed law. No model-dependent choice on null histories is needed.

The cancellation depends on the declared observation port: actual sampled commands and declared reports are visible, hidden physical suboutcomes and realized costs are not additional observations, and the private label path cannot change the physical map once that visible command/report history is fixed. It also uses the common pure initialization. Those conventions are stated in the primitive interface.

This supplies the reverse comparison V_hist<=V_M without granting an unknown-model oracle or replacing a controller with a history kernel that depends on the model. Conversely, storing the finite visible prefix and then using the common fallback produces a counted finite controller. The count `1+sum_{t=0}^{T-1} (|A||Y|)^t` includes the initial root, all retained nonterminal prefixes, and the fallback label. The depth is stored in those labels; no free clock is used.

The duration bound supplies a survival probability at most b/(c_* T). It is multiplied by the cost of the actual all-state fallback. This is a valid bound on the constructed policy, not an inference that the original infinite-horizon cost tail vanishes uniformly. Taking the infimum over history policies does not require an attained history optimum.

## 4. Positive-success corollary: same-memory Lipschitz comparison

Location: `cor:r79-positive-success`, equations `eq:r79-success-floor` and `eq:r79-lipschitz-frontier`.

The success hypothesis is imposed on every command, every model in both families, and every physical state: `B_a^theta>=kappa I`. Normalization of the controller rows gives

`(T_gamma^theta)^*(I)<= (1-kappa) I`.

For a Hermitian block tuple X with norm at most one, `-I<=X<=I`. Positivity then gives `-(1-kappa)I <= (T_gamma^theta)^*X <= (1-kappa)I`. Thus the Hermitian block operator norm contracts by at most 1-kappa, uniformly over all controller rows and all M. The Neumann inverse has norm at most 1/kappa, and the exact potential satisfies `0<=W^theta<=(c^*/kappa)I` from every label.

For one fixed controller, subtracting the two exact cost equations gives

`W_target-W_source = (I-T_target^*)^{-1} [K_target-K_source + (T_target^*-T_source^*) W_source]`.

The source global potential is positive and bounded by c^*/kappa, so the centered perturbation lemma bounds the bracket's Hermitian norm by `zeta+eta c^*/kappa`. Applying the target resolvent gives

`||W_target-W_source|| <= zeta/kappa+c^* eta/kappa^2`.

The maximum eigenvalue of the initial block, equivalently its worst initial-state expectation, changes by at most the same quantity. For each fixed controller, pairing target models with source models bounds its robust target cost by its robust source cost plus that quantity. Taking the infimum over the same M-label controller class preserves the inequality. Reversing the family pairing gives the absolute-value estimate. This argument does not mix controllers, add memory, assume convexity of the fixed-memory objective, or require continuity of an optimizer.

No small-error condition is needed: both source and target already have the uniform success margin, so both resolvents have their own 1/kappa bound. The argument also applies at kappa=1; then the failure maps vanish and the instrument-error term is unnecessary but harmless. The local sharpness assertion is properly restricted to 0<kappa<1.

## 5. Local coefficient sharpness and the stronger history rate

Locations: `eq:r79-lipschitz-local-sharpness`, `eq:r79-geometric-history`.

For the scalar one-command example, the normalized output is the two-outcome Bernoulli law, so half its trace-norm difference is exactly eta. The deterministic call-cost difference is exactly zeta. Mandatory success stopping gives the two geometric costs `C/(kappa+eta)` and `(C+zeta)/kappa`, and their difference is exactly

`zeta/kappa + C eta/[kappa(kappa+eta)]`.

With eta=0, the coefficient 1/kappa for cost error is attained exactly. This can be realized with a fixed common ceiling c^* by choosing `C=c^*-zeta` and sufficiently small positive zeta within the allowed positive-cost interval. With zeta=0 and C=c^*, the ratio of the cost change to eta tends to `c^*/kappa^2` as eta decreases to zero. Hence neither universal local coefficient can be reduced in the stated class. With one command, no controller can affect the physical waiting law, so the comparison holds at every M.

These are two separate local coefficient statements. They do not assert that the sum of the two upper bounds is attained for every finite pair of errors, and they do not give sharpness of the general square-root modulus at a success/support degeneracy. The source makes these distinctions.

Under the success floor, every visible-history policy has conditional success probability at least kappa on every call. Survival through T calls is at most `(1-kappa)^T`, irrespective of its private randomness, physical posterior, or fixed model. Truncating a competing history policy after T calls and using the actual fallback adds at most `C_0(1-kappa)^T`. Taking the infimum proves the stated geometric approximation inequality with the same counted history tree. Passing the uniform-in-M Lipschitz estimate to the history limit is justified by `cor:r79-history-limit`.

The rate is exponential in T. When `|A||Y|>1`, the displayed memory construction is itself exponential in T; the manuscript correctly does not claim exponential convergence in M. At kappa=1 the tail is zero for T>=1, consistent with success at the first call.

## 6. Response completeness and source-label resolution

The integrated `RESPONSE_TO_REFEREE.md` was scanned against its actual contents, and referenced theorem/equation/example/section labels were checked against the current `sections/*.tex`, `main.tex`, and `supplement.tex` bodies.

| Check | Actual result |
|---|---:|
| R65 section 17 individually numbered response headings | 10 |
| R65 section 18 individually numbered response headings | 40 |
| Total individually numbered current-report responses | 50 |
| Missing expected item numbers | 0 |
| Unexpected item numbers | 0 |
| Duplicate numbered item headings | 0 |
| Distinct inline native labels referenced in the response | 63 |
| Referenced labels absent from the current native source | 0 |

In particular, `cor:r79-positive-success` now resolves. These are content/reference checks, not a statement that all textual responses have received independent referee acceptance or that the paired LaTeX cross-references have compiled. Native compilation belongs to the separate actual build receipt.

## 7. Attribution and remaining limitations

The source explicitly preserves its internal antecedents. Arbitrary-CP reachable supports, supported cost/score certificates, finite-model exact fixed-memory synthesis, dark-subspace fallback, the centered effect estimate, and finite-prefix completion were already present in the inherited paper. The current positive-success estimate uses the standard positive-resolvent argument and is not presented as a newly invented perturbation method. The main new mechanism being checked here is regularization within the same live-label budget and its uniform-in-memory stability consequence across support changes.

The focused check establishes no external priority clearance. It does not resolve optional commitment, the original general-M squared-sign qubit risk, the sharp unrestricted qubit approximation rate, the intermediate phase-type timing curve, intrinsic necessity for the general causal-transfer certificates, a common predictive quotient for arbitrary unknown models, or finite saturation/decidability of the unrestricted-memory optimum. It does not identify classical live labels with program-table storage, exact-sampling resources, or protected physical quantum degrees of freedom. No claim of a four-journal editorial decision is made.

Only this audit record was written during this focused check; the inspected mathematical sources and response were read without modification.
