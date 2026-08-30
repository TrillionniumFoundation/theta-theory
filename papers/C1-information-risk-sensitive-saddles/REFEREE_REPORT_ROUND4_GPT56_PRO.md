# Round-Four Independent Referee Report — GPT-5.6 Pro

**Manuscript:** C1 — *Typed Control, Information, and Saddle Envelopes for Kinetic Cotangent Phases*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round4-referee-positive-closure-11paper-2026-08-30@cbee394d6ee33db471b63420131314bd05909a0f`  
**Controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `a811922180e67e29581d1806fadb4ca80c0b73e5`

## Overall assessment

The revision has made a genuine structural improvement: one-time preparation, reward-only feedback, and adaptive canonical reweighting are now formulated as three distinct games. The adaptive finite-volume change of law is normalized block by block through an exact conditional log-partition, replacing the previous false Poisson-compensator formula.

The conditional state and source chart needed for that construction are not defined rigorously, and the information-theoretic part contains an elementary measure-theoretic error: posterior odds between infinitesimal parameter elements are written as a ratio to `rho_T(dz_0)`, which is zero for a continuous prior. The LAN/Bernstein--von Mises theorem also silently assumes a linear exponential-source parametrization, whereas the paper's phase variable includes objects which do not have that likelihood form. The principal control and filtering claims therefore remain unproved.

## Major objections

### 1. The “complete correlation state” used for conditional normalization is ambiguous

The manuscript conditions on `G_{t_j}^epsilon`, called the complete correlation state. Correlation functions usually describe the unconditional or conditional ensemble law and evolve deterministically once that law is fixed. They are not an observed random variable of one hard-sphere trajectory unless a nonlinear filter on measures has first been constructed.

There are two possible interpretations:

- If `G_t^epsilon` is the unconditional BBGKY hierarchy, then it is deterministic and conditioning on it does not produce a strategy-dependent block normalization.
- If it is the conditional hierarchy given the resolved observations and prior controls, then the paper must define this random measure-valued state, prove its measurability, and derive its update equation.

Neither construction is supplied. Consequently the exact block density and discrete dynamic programming state are not well typed.

### 2. The strategy does not observe the state on which the normalizer is conditioned

Controls are predictable with respect to the resolved filtration `F_{t_j}^{res}`, while the normalizer is a function of the complete correlation state. The paper does not show that this state is measurable with respect to the resolved filtration. If it is not, the controller cannot evaluate the displayed likelihood increment; if the normalizer is instead computed under the hidden conditional law, that law must be included in the information state.

The distinction is essential in a partially observed game and cannot be bypassed by notation.

### 3. Uniform conditional source charts do not follow from the unconditional B2 expansion

The proof says that, conditional on any regular correlation state reached under any strategy, the next block is “the same local hierarchy problem” as B2, with uniform constants. This requires a controlled invariant class of conditional correlation hierarchies satisfying uniform positivity, Gaussian tails, cluster bounds, and analytic radii.

An unconditional grand-canonical cluster expansion does not imply such a theorem for all posterior/controlled conditional laws. Canonical reweighting can amplify correlations and push the hierarchy to the boundary of the analytic ball. No induction proving preservation of the compact regular set is given.

Thus the consistency estimate for the adaptive Isaacs Hamiltonian is unproved.

### 4. The continuous-parameter posterior-odds formula is undefined

For a continuous phase parameter and a prior with a density,

\[
\rho_T^\varepsilon(\{z_0\})=0.
\]

The expression

\[
\frac{\rho_T^\varepsilon(dz)}{\rho_T^\varepsilon(dz_0)}
\]

is not a ratio of numbers and has no intrinsic meaning. One must specify posterior densities with respect to a dominating reference/prior measure and compare those densities, or compare masses of shrinking neighborhoods.

The first assertion of the posterior-selection theorem is therefore ill defined as written.

### 5. The expected posterior bound needs a prior-density and metric entropy analysis

The proof controls pointwise likelihood ratios and then invokes a finite cover of `O^c`. For an uncountable compact parameter family, passing from pointwise Chernoff bounds to the posterior integral requires uniform continuity of the likelihood exponent, lower and upper bounds on the prior density, and control of the covering entropy at the large-deviation scale.

None of these assumptions is stated. A fixed finite cover is not justified unless the Chernoff rate and finite-volume moments are uniformly stable on its neighborhoods.

### 6. The LAN theorem applies only to an exponential-source chart, not the declared phase manifold

The proof says “use the exact finite-volume exponential likelihood and Taylor-expand `Q_epsilon(z)`.” This is valid when `z` is a linear canonical source parameter and the law has density

\[
\exp\{\mu z\cdot X-\mu Q_\varepsilon(z)\}.
\]

Earlier in the paper, however, `z` may contain:

- a source-dependent preparation multiplier;
- a B3 cotangent equivalence class;
- a phase label; or
- a general smooth parameter in the kinetic semigroup.

A generic smooth family of path laws is not an exponential family with score `X-DQ`. The LAN expansion and information matrix `D^2Q` do not follow for such a parameter without differentiability in quadratic mean and an explicit score map.

The theorem therefore overstates its scope.

### 7. The Bernstein--von Mises conclusion is not established

LAN alone gives local likelihood approximation. Total-variation Bernstein--von Mises requires posterior concentration at the `mu^{-1/2}` scale, identifiability, prior thickness, control of likelihoods outside local neighborhoods, and usually finite-dimensional regularity conditions. The proof cites “exponential tail control from identifiability” but provides no theorem establishing it uniformly.

The statement “in total variation on compact sets” is also ambiguous: total variation is a global norm on probability measures, not a topology restricted to compact test sets unless a truncation/renormalization is defined.

### 8. The one-time preparation game is correctly typed but mathematically elementary

The theorem that a time-zero choice must be retained across the fixed-phase semigroup is correct. It is a modeling clarification, not a new mathematical theorem of top-journal depth. The reward-only equation is similarly immediate once B4 is available.

### 9. The adaptive game depends on the invalid B2/B4 interfaces

The action, compact containment, and comparison theorem are imported from B2/B4. Those papers do not presently establish them. Even a corrected information state would not close the adaptive game without those upstream results.

### 10. The smooth saddle theorem is a standard envelope formula under assumed curvature

The Schur-complement Hessian is correct once differentiability, a unique interior saddle, and invertibility are known. The new curvature-dominance lemma simply assumes a cost `k` strong enough to force those properties. This is a sufficient modeling condition, not a new kinetic theorem.

## Status of previous objections

The timing/category error from the previous version has been substantially corrected. The paper no longer treats an initial preparation game as automatically satisfying a pointwise Isaacs equation, and the adaptive law is no longer normalized by a fictitious collision compensator.

The present rejection rests on the absence of a constructed conditional hierarchy state and on false/overbroad filtering and LAN statements.

## Minimum viable reconstruction

The paper should be split into a precise modeling/control note and a separate statistical theorem. It must:

1. define the random posterior correlation/history state under resolved observations;
2. prove a uniform conditional cluster/source theorem on an invariant controlled class;
3. write posterior densities relative to a specified reference measure;
4. restrict LAN/BvM to a concrete finite-dimensional canonical exponential family; and
5. state all prior, identifiability, domination, and concentration assumptions.

## Recommendation

**Reject.** The revision separates the games correctly, but the adaptive information state is not constructed and the posterior/LAN theorems are ill typed or substantially underproved.