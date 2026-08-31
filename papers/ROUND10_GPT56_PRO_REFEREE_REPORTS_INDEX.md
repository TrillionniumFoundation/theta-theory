# Round-Ten GPT-5.6 Pro Referee Review — Eleven-Paper Index

**Repository:** `TrillionniumFoundation/theta-theory`  
**Review date:** 2026-08-31  
**Reviewed revision branch:** `revision/round10-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `b45406b03ab45e70461d36da5d3ee64892a92c8f`  
**Reviewed tree:** `f9b93d1a0b06628cb01ba4f6f67b7c3348579b46`  
**Controlling mathematical commit:** `101dc123e4bafbb8e140e658ac1390f7735dc67e`  
**Review branch:** `review/round10-gpt56-pro-harsh-11paper-2026-08-31`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, and *Journal of the AMS*  
**Overall recommendation:** **Reject all eleven manuscripts in their present form.**  
**D1 recommendation:** **Remove as a standalone submission.**

## Evidence boundary

Round ten is a genuine materialized revision. At the review lock, `main` and the revision branch pointed to the same exact commit, and every paper-level `main.tex` loaded its `ROUND10_POSITIVE_CLOSURE.tex`. The registered module hashes, 11/11 builds, theorem/proof counts, dependency ledger, and internal hostile scripts are acknowledged as source-integrity evidence.

They are not mathematical certification. In particular, the internal hostile JSON often checks that a phrase or formula is present, not that the formula is true. A4's gate, for example, marks as passed the exact false identity used in its martingale proof.

This review changes no manuscript source, proof module, PDF, workflow, certificate, bibliography, author response, or previous report. It adds only the eleven reports below and this index.

## Paper-level report paths

```text
papers/A1-exact-benchmarks/REFEREE_REPORT_ROUND10_GPT56_PRO.md
papers/A2-sinai-homological-pressure/REFEREE_REPORT_ROUND10_GPT56_PRO.md
papers/A3-full-empirical-path-ldp/REFEREE_REPORT_ROUND10_GPT56_PRO.md
papers/A4-history-memory-universal-pressure/REFEREE_REPORT_ROUND10_GPT56_PRO.md
papers/B1-microcanonical-preparation/REFEREE_REPORT_ROUND10_GPT56_PRO.md
papers/B2-collision-clusters-dynamic-ldp/REFEREE_REPORT_ROUND10_GPT56_PRO.md
papers/B3-hamilton-boltzmann-cotangents/REFEREE_REPORT_ROUND10_GPT56_PRO.md
papers/B4-nonlinear-kinetic-semigroups/REFEREE_REPORT_ROUND10_GPT56_PRO.md
papers/C1-information-risk-sensitive-saddles/REFEREE_REPORT_ROUND10_GPT56_PRO.md
papers/C2-cotangent-rigidity-tangent-representations/REFEREE_REPORT_ROUND10_GPT56_PRO.md
papers/D1-deterministic-theta-contractions/REFEREE_REPORT_ROUND10_GPT56_PRO.md
```

## Editorial verdicts

| Paper | Recommendation | Decisive round-ten finding | Genuine repair recognized |
|---|---|---|---|
| **A1 — Exact Benchmarks** | Reject | The factor theorem uses a nonexistent independent inverse of a one-sided past shift; the correct natural extension is coupled by the current future symbol. The branched quotient is not shown to be a smooth Hamiltonian manifold. | Physical and symbolic spaces are separated; the false bilateral spectral gap and unconditional risk identification are removed. |
| **A2 — Sinai Homological Pressure** | Reject | The arithmetic certificate uses regular one-collision winding orbits that cannot exist except at grazing. The moderate-frequency bound grows exponentially at its upper endpoint, and the birth construction is smooth only in a square-root coordinate. | Arithmetic, UNI, Fourier ranges, and window scaling are separated. |
| **A3 — Full Empirical-Path LDP** | Reject | Collapsing all omitted branches to a cemetery state does not give a finite Markov factor; the recession functional has no specified common speed; the final rate adds incompatible count- and clock-speed costs without a joint LDP. | Deterministic excursion speed, actual edges/profiles, and multi-excursion recession recovery are adopted. |
| **A4 — History, Memory, Universal Pressure** | Reject | With `h_g=sum_{n>=1}P^n g`, the proposed increment has conditional mean `Pg`, not zero, and its coboundary formula does not telescope. The memory strip theorem is also unsupported. | Genuine past filtration, eigenfunction Doob normalization, and causal Volterra sign are used. |
| **B1 — Microcanonical Preparation** | Reject | The characteristic estimate leaves the compact region `t≈0, delta<|u|<=R` uncontrolled, and its speed-independent polynomial tail cannot yield the claimed `mu^{-1/2}` sharp coefficient. | Source-dependent exact saddle, relative-interior targets, and a CLT-wide shell are retained. |
| **B2 — Collision Clusters and Dynamic LDP** | Reject | A nonzero analytic Jacobi minor does not give a Łojasiewicz exponent uniform in genealogy depth; `x^m` is the elementary counterexample. The mesh-independent recollision error also prevents uniform sewing. | Compatible trace graph, true reflected future, and integrated rather than QR-reset geometry are adopted. |
| **B3 — Hamilton–Boltzmann Cotangents** | Reject | A uniform biased non-equilibrium collision gap is assumed, and the inverse covariance is written on `closure Ran Sigma` instead of the Cameron–Martin form domain `Ran Sigma^{1/2}`. | Raw indefinite curvature is acknowledged; covariance and exact centering come first. |
| **B4 — Nonlinear Kinetic Semigroups** | Reject | The gradient of `d_lambda^2/(2 epsilon)` is `O(lambda/sqrt(epsilon))`, not bounded by `lambda`; hence the comparison theorem again evaluates the Hamiltonian on uncontrolled jets. Graph-core density is circular. | State/observable/law objects are separated, preparation is charged once, and the corrector sign is fixed. |
| **C1 — Information and Saddles** | Reject | Coarea slicing is not defined on the declared arbitrary measure tower, and the Feller state omits the `z=-infinity` boundary while claiming continuity as evidence vanishes. | Unnormalized evidence, singular strata, full belief control, and reachable-only reduction are recognized. |
| **C2 — Cotangent Rigidity and Representations** | Reject | Equal scalar pressure does not imply cohomology modulo constants; a two-symbol full shift is an explicit counterexample. Kato transport is also ill-typed on A2's regularity-losing scale. | Closed linear nullspaces, common transfer spaces, and separation of spectral/resolved projections are improvements. |
| **D1 — Deterministic Theta Contractions** | Reject; remove standalone paper | `Q_{n,j}=n^{-1}log E[e^{n theta X};B_j]` already contains the phase cost, yet the physical pressure subtracts `alpha_j` again. Phase basins and projective labels are assumed, not constructed. | Fixed exponential remainders and genuine microscopic labels are now required in principle. |

## Root-level mathematical findings

### 1. A2's periodic certificate contains nonexistent regular orbits

A period-one collision orbit with nonzero lattice homology must return to the same boundary point and outgoing direction modulo translation. The flight connects corresponding points of two translated circular scatterers, so its direction is the lattice displacement and the endpoint normal equals the initial normal. Specular reflection preserves that direction only if the incidence is tangent. Thus the asserted regular one-collision winding orbits `w1,w2` are grazing, not admissible periodic collision states.

Without them, the advertised four-coordinate determinant does not certify joint arithmetic aperiodicity.

### 2. A4's corrected martingale is still algebraically wrong

For

\[
h_g=\sum_{n\ge1}P^ng,
\qquad (I-P)h_g=Pg,
\]

one has

\[
P(g+h_g)=Pg+Ph_g=h_g,
\]

not `Ph_g`. Therefore the manuscript's increment has conditional mean `Pg`. The internal hostile script checks the false equality as a required token and consequently reports a false positive.

### 3. B2's uniform analytic sublevel inference is invalid

Nonzero analyticity does not control vanishing order uniformly in a growing genealogy. The family `f_m(x)=x^m` has

\[
|\{|f_m|<\rho\}|\asymp\rho^{1/m}.
\]

No depth-independent exponent exists. The whole `epsilon^{alpha_0}` first-surplus gain depends on exactly such an exponent.

### 4. C2's scalar-pressure rigidity has a full-shift counterexample

On the two-symbol full shift, let `F=0` and let `G` take values `log(3/2)` and `log(1/2)` on the two symbols. Then

\[
P(G)=\log(3/2+1/2)=\log2=P(F),
\]

but `G` is not cohomologous to a constant because its sums on the two fixed points have different slopes. Equality of one pressure value is not a cohomology criterion.

### 5. D1 double counts the phase weight

Since

\[
Q_{n,j}(0)=n^{-1}\log w_{n,j}\to-\alpha_j,
\]

the limit of the unnormalized restricted partition function already contains `-alpha_j`. Summing the restricted partition functions gives `max_j Q_j`, not `max_j(Q_j-alpha_j)`.

## Further series-level defects

### Internal verification is syntactic at several decisive points

The round-ten hostile audit confirms tokens such as the A4 false Poisson identity, the existence of a named Jacobi estimate, and numerical output from a formal A2 determinant. It does not prove the geometric existence of the periodic orbits, the operator-domain statements, or the probability estimates.

### Local source control is repeatedly promoted to a global LDP

B2 and its downstream papers use a bounded analytic source ball, then claim the full Poisson entropy action, singular-current exclusion, and recovery of every finite-action state. A separate real-source exhaustion and lower-bound theorem is required.

### Operator scales are called fixed spaces after derivatives lose regularity

A2 explicitly loses one strong level per parameter derivative; C2 then solves a Kato ODE as though the projector derivative were bounded on one space. Similar scale losses occur in B2/B4 hierarchy semigroups.

### Several downstream papers remain conditional summaries

B4, C1, C2, and D1 mainly state standard consequences of a good rate, a comparison theorem, a Gaussian tangent, or a phase decomposition. Their nontrivial inputs are exactly the upstream theorems that remain open.

## Dependency audit

```text
A1  (independent benchmark; presently fails its factor and suspension statements)

A2  --> A3 --> A4 --> C2 --> D1
                  \------------> D1

B2-GC --> B1 --> B2-MC --> B3 --> B4 --> C1 --> D1
   |                         |       \-----> C2 --> D1
   +-------------------------+-----------------------> D1
```

- **A2** is open at geometry, birth regularity, arithmetic, and Fourier control.
- **A3** has no valid finite-core/projective or mixed-clock theorem.
- **A4** fails independently at its martingale algebra.
- **B2-GC** is open at the uniform Jacobi/coarea estimate and global source lower bound.
- **B1** lacks its full mixed local coefficient.
- **B3** lacks its driven spectral/closed-form theorem and process CLT.
- **B4** lacks graph-core convergence and comparison.
- **C1** lacks a filtering state and observation coefficient.
- **C2** contains independent false rigidity and derivative statements.
- **D1** assumes the whole dependency chain and has its own normalization error.

No downstream interface, certificate, or theorem label can close an upstream mathematical gap.

## Genuine improvements to retain

Round ten is not a null revision. The following ideas should be preserved in a future reconstruction:

- **A1:** physical/symbolic separation, one-sided transfer operators, full-port work, and conditional calibration.
- **A2:** separate moving geometry, arithmetic, UNI, high-frequency control, and window regimes.
- **A3:** deterministic indexing, actual edge/profile marks, and a pointed terminal state.
- **A4:** genuine past filtration, eigenfunction Doob transform, causal memory sign, and full unresolved-space retention.
- **B1:** exact source-dependent saddle, intrinsic affine-span conditions, and a central-limit-wide shell.
- **B2:** closed compatible traces, true reflected futures, and integrated physical transversality.
- **B3:** covariance-first construction, explicit acknowledgment of raw negative curvature, and exact finite centering.
- **B4:** separation of Koopman/push-forward/value/action objects, dynamic-only transition cost, and terminal correctors.
- **C1:** evidence-bearing belief states, explicit critical strata, and reduction only on reachable beliefs.
- **C2:** closed linear nullspaces, avoidance of infinite-path RN densities, and typed nonlinear contraction notation.
- **D1:** insistence on genuine microscopic phase components and preservation of exponential remainders.

The reports reject the theorem packages, not every local design choice.

## Recommended reconstruction order

1. Correct A1's coupled natural-extension map and scope the mapping torus as a stratified measurable suspension unless a genuine smooth desingularization is built.
2. Rebuild A2 around actual regular periodic orbits and prove a quantitative moving-billiard spectral/UNI/Fourier theorem with usable frequency ranges.
3. Replace A3's cemetery Markovization by genuine finite observables of the countable process and prove one deterministic-clock recession-inclusive joint LDP.
4. Correct A4's Poisson algebra before any rough or memory theorem; then construct the Hilbert/operator setting and vertical resolvent bounds.
5. Prove B2-GC's uniform inverse-Jacobi/coarea theorem on a rigorously generated trace scale.
6. Prove B1's complete compact/high-frequency coefficient with source-uniform dynamic decoupling.
7. Transfer B2 microcanonically only after B1 is valid and prove a global real-source lower bound.
8. Derive B3's driven linear theory and correct Cameron–Martin form domain; prove process tightness separately.
9. Rebuild B4's observable core and comparison with a penalty compatible with the Hamiltonian source domain.
10. Construct C1 on a precise sliced-current/projective-evidence state and state a complete statistical model before claiming BvM.
11. Separate C2's invariant-integral quotient, full pressure-functional equivalence, fixed-space Kato response, and source/state chain rules.
12. Remove D1 as a standalone paper; retain only a correctly normalized finite-mixture lemma in future platform papers.

## Final recommendation

**Reject all eleven manuscripts in their present form.**  
**D1 should be removed as a standalone submission.**

The external top-four publication gate should remain closed.
