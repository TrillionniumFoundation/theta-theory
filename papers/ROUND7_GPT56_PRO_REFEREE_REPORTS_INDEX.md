# Round-Seven GPT-5.6 Pro Referee Review — Eleven-Paper Index

**Repository:** `TrillionniumFoundation/theta-theory`  
**Review date:** 2026-08-31  
**Reviewed revision branch:** `revision/round7-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `b1e3d17f59ca9bb1a04d4ac9157f10dc333f9607`  
**Reviewed tree:** `7af7cb0b5a182eec2dc221a838bfbf0ce65ffcb1`  
**Review branch:** `review/round7-gpt56-pro-harsh-11paper-2026-08-31`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, and *Journal of the AMS*  
**Overall recommendation:** **Reject all eleven manuscripts in their present form.**  
**D1 recommendation:** **Remove as a standalone submission.**

## Evidence boundary

Round seven is a genuine materialized revision. Each `main.tex` loads its paper-level `ROUND7_POSITIVE_CLOSURE.tex`, and `main` and the round-seven revision branch pointed to the same exact paper commit at the start of this review. The reports below therefore address the actual controlling theorem text, not detached candidate packets.

Compilation, PDF production, source hashes, theorem/proof counts, internal hostile checks, certificates, and publication metadata are acknowledged as repository integrity evidence only. They do not establish the truth of estimates, the existence of functional-analytic objects, or the validity of a large-deviation lower bound.

No manuscript source, PDF, bibliography, workflow, author response, certificate, or prior report is modified by this review. The only additions are the eleven reports listed below and this index.

## Paper-level report paths

```text
papers/A1-exact-benchmarks/REFEREE_REPORT_ROUND7_GPT56_PRO.md
papers/A2-sinai-homological-pressure/REFEREE_REPORT_ROUND7_GPT56_PRO.md
papers/A3-full-empirical-path-ldp/REFEREE_REPORT_ROUND7_GPT56_PRO.md
papers/A4-history-memory-universal-pressure/REFEREE_REPORT_ROUND7_GPT56_PRO.md
papers/B1-microcanonical-preparation/REFEREE_REPORT_ROUND7_GPT56_PRO.md
papers/B2-collision-clusters-dynamic-ldp/REFEREE_REPORT_ROUND7_GPT56_PRO.md
papers/B3-hamilton-boltzmann-cotangents/REFEREE_REPORT_ROUND7_GPT56_PRO.md
papers/B4-nonlinear-kinetic-semigroups/REFEREE_REPORT_ROUND7_GPT56_PRO.md
papers/C1-information-risk-sensitive-saddles/REFEREE_REPORT_ROUND7_GPT56_PRO.md
papers/C2-cotangent-rigidity-tangent-representations/REFEREE_REPORT_ROUND7_GPT56_PRO.md
papers/D1-deterministic-theta-contractions/REFEREE_REPORT_ROUND7_GPT56_PRO.md
```

## Editorial verdicts

| Paper | Recommendation | Decisive round-seven finding | Genuine repair recognized |
|---|---|---|---|
| **A1 — Exact Benchmarks** | Reject | The 16-cell biseam complex omits the internal preimages `q=s_{i-1}+p_i s_j` of target seams. At those source points the target has two germs but the source carries no selecting germ, so the return map is not single valued/stratum preserving. The spectral and suspension theorems are built on that incomplete partition. | Full-port work and conditional calibration are correctly repaired. |
| **A2 — Sinai Homological Pressure** | Reject | A uniformly bounded right inverse cannot persist when a newborn physical current vanishes at a birth. The five-word determinant is not explicitly or uniformly constructed; periodic aperiodicity is incorrectly promoted to a high-frequency UNI derivative. The roof-window formula is short by a factor `n` under the scaling declared in the paper. | Zero/nonzero trace spaces are no longer directly identified; near-opposition and three window regimes are the correct ideas. |
| **A3 — Full Empirical-Path LDP** | Reject | The mark `(1/r(a),K_a)` does not identify the inducing branch and therefore cannot determine transition entropy or the recurrent rate. A local Gamma limit is declared rather than proved, and branch-averaged profiles are substituted for actual excursion profiles without exponential equivalence. | An explicit recession coordinate and admissible-edge recovery are structurally appropriate. |
| **A4 — History, Memory, Universal Pressure** | Reject | Quotienting by stable leaves retains the future-determining unstable/symbolic coordinate, so averaging over a stable fiber does not create a nondegenerate future quotient law. The proposed Riesz–Schur operator omits the unresolved space, and the memory transform has the wrong sign. | The Doob transform, forcing correction, transmission-zero awareness, and area anomaly should be retained. |
| **B1 — Microcanonical Preparation** | Reject | A full-rank coarea patch gives only an absolutely continuous component, not a globally smooth convolution law. The nonsmooth complement has non-negligible mass, so the high-frequency estimate fails. Constraint-rank assumptions are absent and the covariance proof uses an exponentially rare fixed-particle sector. | Exact finite saddle, extensive shell scaling, paraboloid recognition, and explicit low Poisson sectors are correct repairs. |
| **B2 — Collision Clusters and Dynamic LDP** | Reject | The interior/boundary measure pair is not a compatible kinetic trace domain. QR frame resets cannot remove accumulated physical singular values while preserving the integration measure; the depth-independent Gramian is unproved. The regularization and full lower bound are only asserted. | Trace control and retention of the true post-collision future correctly replace the old boundary-layer and deletion arguments. |
| **B3 — Hamilton–Boltzmann Cotangents** | Reject | The exact action Hessian contains `(1-q)D^2A_f`, which is indefinite for `q>1`; the claimed coercivity does not follow and can fail in residual-free directions. Closed range/observability and process cumulant estimates are not proved. | Separating analytic/global source domains and exact finite centering are correct. |
| **B4 — Nonlinear Kinetic Semigroups** | Reject | A nonconstant entire cutoff cannot equal one on an open box. The proposed penalty tends to the fixed distance `d_B` and does not force the doubled variables to the diagonal. Including `I_0(f_0)` in every transition action double counts preparation and destroys the semigroup law. | The augmented law state, terminal-value sign, and weak-energy topology are genuine improvements. |
| **C1 — Information and Saddles** | Reject | Coarea transversality does not bound the posterior normalization away from zero; regular rare observations can produce arbitrarily large posterior-current norms. B2 does not act on arbitrary observation currents, and beliefs with the same one-particle mean can retain order-one collision correlations. | The new observation is included, singular posteriors are acknowledged, and KL/Chernoff plus finite LAN centering are corrected. |
| **C2 — Cotangent Rigidity and Representations** | Reject | `N_int` is not defined as a closed linear span and may not be a subspace. The Følner moment bound is not uniform in time. Nearby infinite-volume Gibbs path measures are generally mutually singular, so the Radon–Nikodym Hilbert connection is undefined. The memory sign is again wrong. | Integral and pressure null spaces, exact history martingales, and covariant data requirements are useful distinctions. |
| **D1 — Deterministic Theta Contractions** | Reject; remove standalone paper | A fixed zero-free complex tube cannot cover a genuine coexistence point because finite-volume zeros pinch the real axis. The conjugate of `max_j Q_j` is not generally `min_j Q_j^*`; phase-wise lower recovery is inserted as an external assumption. Local charts do not prove boundary-face LDPs. | Exact local likelihood centering and rejection of entire/steep bounded-cylinder hypotheses are correct. |

## Root-level mathematical findings

### 1. A2's local-limit theorem has a direct scaling inconsistency

The manuscript classifies

```text
G_n = O(n^{-1/2}),
n^{-1/2} << G_n << 1,
G_n >= G_0
```

as local, central, and saturated regimes. These are regimes for a window in the average `T_n/n`. The corresponding interval in the sum `T_n` has width `n G_n`. A two-lattice/one-continuous joint density is order `n^{-3/2}`, so the integrated probability is order

```text
n G_n * n^{-3/2} = G_n n^{-1/2},
```

not `G_n n^{-3/2}` as displayed. If `G_n` instead denotes a sum-scale width, the three stated regimes are wrong. This error is independent of every spectral estimate.

### 2. A4's coarse quotient still keeps the future itinerary

For a hyperbolic map, points on one local stable leaf have the same future symbolic itinerary. Quotienting by stable leaves retains the unstable/future coordinate. Hence integrating over a stable fiber cannot generate a nondegenerate future quotient path. At most it averages transient stable-coordinate differences, which decay rather than accumulate into Brownian randomness.

A genuine quenched diffusion kernel requires a sigma-field that forgets the future-determining coordinate, or an observation-noise model. C2's optional-projection theorem remains blocked until this is redesigned.

### 3. B1 mistakes a smooth component for a smooth law

A nonzero coarea minor on one product patch shows only that the restricted pushforward has an absolutely continuous component. The complement can retain singular mass of order one. Grouping the first `n_*` marks and integrating by parts is therefore invalid for the complete compound sector. This destroys the large-frequency estimate and the mixed shell coefficient.

### 4. Coordinate resets do not eliminate B2's physical Jacobi losses

An orthonormal frame can be reset after every collision, but the physical derivative from original integration variables to the later contact remains the product of the scattering/free-flight cocycle. Rescaling a small singular direction to unit length transfers the inverse factor to complementary coordinates or to the Jacobian. Symplectic determinant one is not a condition-number bound. The claimed depth-independent Gramian consequently has no proof.

### 5. B3's proposed covariance metric is not positive in general

The exact second variation contains

\[
(1-q)D^2A_f[\dot f,\dot f].
\]

For `q>1` this is negative in suitable residual-free directions. In the scalar model `A_f=f^2`, choosing `dotGamma=q DA_f[dotf]` leaves `2(1-q)dotf^2`. A short-block slogan does not make the total fixed-horizon Hessian positive. Lax–Milgram and covariance inversion therefore require additional hypotheses or a different construction.

### 6. B4's comparison penalty solves boundedness by removing coercivity

Because `omega(r)=r` near zero,

\[
\eta^{-1}\omega(\eta d_B)=d_B
\]

for small `eta`. The penalty does not grow off the diagonal and cannot force `f-g -> 0`. Its derivatives remain bounded precisely because the doubling argument has lost the singular penalization needed for comparison.

### 7. C1's exact-observation denominator is the central missing estimate

A submersion lower bound on `J_O` does not bound the level-set marginal density

\[
Z(y)=\int_{O^{-1}(y)}g/J_O.
\]

Regular values can have arbitrarily small `Z(y)`. Uniform posterior-current bounds and a quenched ratio theorem therefore require observation-density lower bounds or a separate local-limit theorem. They do not follow from coarea alone.

### 8. C2's Doob Hilbert connection is generally undefined

Distinct ergodic Gibbs measures on infinite path space are often mutually singular; Bernoulli product measures with different parameters are the elementary example. Thus `d nu_eta^D / d nu_0^D` need not exist, and neither does its logarithmic derivative. Source response must be formulated on a common transfer Banach space or finite-time likelihood space, not by density-square-root identification of mutually singular `L2` spaces.

### 9. D1's coexistence atlas contradicts the finite-volume zeros it must control

At coexistence,

\[
Z_\mu\approx e^{\mu Q_1}+e^{\mu Q_2}
\]

has complex zeros at distance `O(1/mu)` from the real crossing. Hence no fixed-width zero-free tube can cover that point while the limit is a nondifferentiable maximum. Phase-specific pressures require separately defined restricted microscopic partition functions; they are not logarithm branches of one nonvanishing MGF.

## Dependency audit

The declared Sinai chain is

```text
A2 -> A3 -> A4 -> C2/D1
```

with A1 independent. This review finds:

- A1 independently fails at the return-section partition and spectral/suspension construction;
- A2 fails its quotient, UNI, and LLT interfaces;
- A3 additionally lacks a well-defined recurrent rate and excursion Gamma recovery;
- A4 independently uses the wrong coarse quotient and wrong memory transform;
- C2 and D1 therefore cannot treat the Sinai path/Doob interfaces as closed.

The hard-sphere chain is

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

This review finds:

- B2-GC remains open at the trace semigroup and depth-uniform recollision estimate;
- B1 independently fails its compound smoothing/local-limit theorem;
- B3 lacks a positive tangent metric and closed-range/cumulant theorem;
- B4 lacks analytic approximation, comparison, and a correctly additive transition action;
- C1's exact posterior state is not closed under the asserted B2 dynamics and does not reduce uniformly to its mean;
- C2 and D1 inherit all of those failures.

No downstream theorem label can repair an upstream gap.

## Genuine improvements to retain

Round seven is not a null revision. The following ideas should be preserved in a reconstruction:

- A1 full-port work and conditional calibration;
- A2 separation of physical quotient, aperiodicity, UNI, and window regimes;
- A3 explicit recession profiles and admissible-edge recovery;
- A4 genuine Doob normalization, transmission-zero retention, and rough-area correction;
- B1 exact finite saddle, extensive shell, and explicit low Poisson sectors;
- B2 trace-aware stopping states and preservation of the true future;
- B3 separate analytic/global source domains and exact finite centering;
- B4 complete augmented law state and weak-energy topology;
- C1 observed Bayes update, singular-posterior awareness, and KL/Chernoff distinction;
- C2 separate integral/pressure null spaces and exact history likelihoods;
- D1 exact local likelihoods and phase-aware projective intent.

The reports reject the theorem packages, not every local construction.

## Recommended reconstruction order

1. Correct A1's one-step preimage seam completion before developing response or suspension.
2. Build A2's actual physical anisotropic quotient and a separate explicit UNI theorem; then correct the LLT scaling.
3. Redefine A3's compactification so it retains transition/entropy data and prove genuine excursion Gamma convergence.
4. Replace A4's stable quotient by a filtration that genuinely leaves future uncertainty; formulate memory on an actual operator extension and correct its sign.
5. Prove B2-GC on a compatible kinetic trace domain with a depth/epsilon summable physical transversality estimate.
6. Prove B1's mixed coefficient using a globally controlled convolution decomposition.
7. Transfer B2-MC only after B1 is valid.
8. Rebuild B3 covariance from a demonstrably positive quadratic form or directly from finite-volume cumulants.
9. Separate B4 static preparation from dynamic action, construct a real graph core, and solve the comparison coercivity/core tradeoff.
10. Add observation noise or a complete stratified-current theory in C1; prove quenched ratio and chaos/sufficiency theorems on a restricted belief class.
11. Recast C2 response on common transfer spaces and fold D1's valid local identities into the principal platform papers.

## Final recommendation

**Reject all eleven manuscripts in their present form.**  
**D1 should be removed as a standalone submission.**

The internal round-seven certificate verifies repository bytes and builds. It does not close the direct mathematical contradictions identified above. The external top-four publication gate should remain closed.
