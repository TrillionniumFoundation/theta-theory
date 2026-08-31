# Round-Eight GPT-5.6 Pro Referee Review — Eleven-Paper Index

**Repository:** `TrillionniumFoundation/theta-theory`  
**Review date:** 2026-08-31  
**Reviewed revision branch:** `revision/round8-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `ad2b5106678b29b7d9ffb3824f61ddbd141ac4b8`  
**Reviewed tree:** `00d7ef9edcddda26fc88962e206677f9b399bebe`  
**Review branch:** `review/round8-gpt56-pro-harsh-11paper-2026-08-31`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, and *Journal of the AMS*  
**Overall recommendation:** **Reject all eleven manuscripts in their present form.**  
**D1 recommendation:** **Remove as a standalone submission.**

## Evidence boundary

Round eight is a genuine materialized revision. Each paper's `main.tex` loads its paper-level `ROUND8_POSITIVE_CLOSURE.tex`, and at the start of this review both `main` and the round-eight revision branch pointed to the same exact commit above. The source-control failure of an earlier round is therefore not repeated.

The repository's build, source-hash, theorem/proof-count, dependency, internal hostile-check, and publication certificates are acknowledged as integrity evidence only. They do not validate a functional-analytic domain, a sharp coefficient estimate, a large-deviation lower bound, or an operator realization.

This review modifies no manuscript, proof module, PDF, workflow, certificate, bibliography, author response, or earlier report. It adds only the eleven reports listed below and this index.

## Paper-level report paths

```text
papers/A1-exact-benchmarks/REFEREE_REPORT_ROUND8_GPT56_PRO.md
papers/A2-sinai-homological-pressure/REFEREE_REPORT_ROUND8_GPT56_PRO.md
papers/A3-full-empirical-path-ldp/REFEREE_REPORT_ROUND8_GPT56_PRO.md
papers/A4-history-memory-universal-pressure/REFEREE_REPORT_ROUND8_GPT56_PRO.md
papers/B1-microcanonical-preparation/REFEREE_REPORT_ROUND8_GPT56_PRO.md
papers/B2-collision-clusters-dynamic-ldp/REFEREE_REPORT_ROUND8_GPT56_PRO.md
papers/B3-hamilton-boltzmann-cotangents/REFEREE_REPORT_ROUND8_GPT56_PRO.md
papers/B4-nonlinear-kinetic-semigroups/REFEREE_REPORT_ROUND8_GPT56_PRO.md
papers/C1-information-risk-sensitive-saddles/REFEREE_REPORT_ROUND8_GPT56_PRO.md
papers/C2-cotangent-rigidity-tangent-representations/REFEREE_REPORT_ROUND8_GPT56_PRO.md
papers/D1-deterministic-theta-contractions/REFEREE_REPORT_ROUND8_GPT56_PRO.md
```

## Editorial verdicts

| Paper | Recommendation | Decisive round-eight finding | Genuine repair recognized |
|---|---|---|---|
| **A1 — Exact Benchmarks** | Reject | The complete germ surface is homeomorphic to a Cantor shift, not a symplectic Liouville section. The router returns its auxiliary coordinate to one physical point and cannot remember distinct germs. The bilateral total-depth norm does not contract under shift. | All iterated seams and full-port work are acknowledged; calibration is conditional. |
| **A2 — Sinai Homological Pressure** | Reject | The birth bundle is conditional on an unproved transverse closed-range theorem; UNI is not geometrically verified; the Dolgopyat estimate is unquantified. The `o(n^{-1})` LLT error cannot yield the smaller local-window main term `G_n n^{-1/2}`. | Arithmetic and UNI are separated, and the missing roof-window factor is corrected. |
| **A3 — Full Empirical-Path LDP** | Reject | Finite edge/profile rates are assumed. Projective recovery produces blocks of many excursions, but the recession theorem falsely upgrades this to recovery by a single long first-return excursion. The terminal cut profile has no constructed rate. | Edge labels, actual profiles, and bounded escaped-clock coordinates are retained. |
| **A4 — History, Memory, Universal Pressure** | Reject | Analyticity plus polynomial growth of a Laplace transform does not imply an exponentially decaying ordinary kernel; the constant transform gives a Dirac mass. The Riesz–Potapov unitary unresolved-space decomposition is not constructed for the billiard generator. | Genuine past filtration, Doob normalization, area anomaly, and causal sign are repaired. |
| **B1 — Microcanonical Preparation** | Reject | The regenerative theorem treats an ideal independent compound-Poisson mark law and drops the hard-sphere connected remainder. The sharp shell formula omits the undo-tilt factor across widths allowed to grow as `o(sqrt(mu))`. | Singular singleton geometry, rank assumptions, exact saddle intent, and low Poisson sectors are handled honestly. |
| **B2 — Collision Clusters and Dynamic LDP** | Reject | The `L1` transport graph closure cannot contain the claimed boundary Dirac states. The projected Jacobi determinant is not proved, source sewing is only an iterated limit, and the purported compact flow-conjugating smoothing group does not exist. | Independent trace pairs and QR resets are abandoned; the true future is retained. |
| **B3 — Hamilton–Boltzmann Cotangents** | Reject | The KKT multiplier reproduces rather than removes `(1-q)D^2A_f`; the reduced Hessian can remain negative. Defining `Sigma^{-1}` and declaring it equal to the KKT Schur complement is circular. | Raw curvature is computed and finite centering is maintained. |
| **B4 — Nonlinear Kinetic Semigroups** | Reject | Stone–Weierstrass does not give generator graph-core density. In comparison, the state gap is `O(1/R)` while the Boltzmann Hamiltonian continuity constant grows like `e^{cR}`; continuity on each source ball is insufficient. | Dynamic-only action and terminal-value corrector sign are fixed. |
| **C1 — Information and Saddles** | Reject | Numerator and denominator of an observed conditional exponential generally have different source-dependent saddles, contrary to the “one common saddle” theorem. Uniform posterior chaos is claimed beyond the finite-evidence slices used in its proof. | Evidence is lifted explicitly, singular observations are retained, and state reduction is restricted to reachable beliefs. |
| **C2 — Cotangent Rigidity and Representations** | Reject | The Kato ODE is not typed on the regularity-losing strong/weak scale. More fundamentally, the leading spectral projector is used as the Mori–Zwanzig resolved projector; on a spectral subspace the memory kernel is identically zero. | Linear null spaces, common transfer spaces, causal sign, and exact likelihoods are improved. |
| **D1 — Deterministic Theta Contractions** | Reject; remove standalone paper | A remainder of size `e^{-c mu}` is not negligible for a full LDP and can alter rates above `c`; it can also change exponential pressures. Positive phase laws and face recoveries are assumed rather than constructed. | Coexistence is treated through phase laws rather than a false common zero-free atlas. |

## Root-level mathematical findings

### 1. A1's complete symbolic germ is not the mechanical section

The graph over the two-sided full shift is a Cantor space. A smooth Hamiltonian return section is a finite-dimensional symplectic object. Returning the router coordinate to `(0,0)` collapses endpoint germs with identical physical coordinates, so the deterministic flow cannot implement the symbol-dependent return map.

The proposed transfer norm has an independent contradiction: the bilateral shift preserves total past-plus-future depth. A translated cylinder martingale difference can have vanishing weak norm before an iterate moves it to the present with order-one strong norm, contradicting the claimed Lasota–Yorke estimate.

### 2. A2 still has an invalid local regime

The corrected Gaussian formula has an absolute remainder `o(n^{-1})`. In the local regime `G_n << n^{-1/2}`, the main term is

\[
G_n n^{-1/2}=o(n^{-1}).
\]

The error can dominate the main term. A local-density theorem with an error tied to `G_n` is still required. The high-frequency theorem also lacks a quantified block length and iteration estimate sufficient for Fourier inversion.

### 3. A3 confuses block recovery with one-excursion recovery

A projective finite-dimensional lower bound can build a long word containing many first-return excursions. It cannot imply that an arbitrary convex boundary profile is realized by one first-return branch. A mixture of two excursion profiles can be recovered by alternating two long excursions even when no single excursion approaches the mixture.

The deterministic terminal prefix similarly needs a pointed partial-excursion state and rate; a full excursion occupation profile does not determine its prefix.

### 4. A4's memory-decay hypothesis is insufficient

A function analytic and polynomially bounded in a half-strip is the Laplace transform of a distribution of finite order, not necessarily an exponentially decaying function. `Khat(z)=1` gives `delta_0`. Vertical decay or integrable derivatives, after subtracting instantaneous terms, are indispensable.

The finite zero-mode realization also assumes passivity and an additive/unitary decomposition not proved for the non-self-adjoint compressed billiard generator.

### 5. B1 has not returned from the Poisson proxy to hard spheres

The good-block mechanism can smooth an independent compound-Poisson sum. The actual source-decorated hard-sphere pressure contains connected static and dynamical clusters. Those terms must be retained with complex-frequency and source-derivative bounds.

Even in the proxy, undoing a nonzero saddle over a shell of width `w_mu` introduces `exp(-lambda z)`. The displayed unweighted Gaussian coefficient is not a relative asymptotic when `w_mu` may grow while remaining `o(sqrt(mu))`.

### 6. B2's new state and regularizer are not physical

The completion of `L1` densities with `L1` transport derivative remains an interior `L1` graph; it does not acquire a tangential boundary Dirac by thin-layer approximation. The first-surplus theorem also needs a lower bound for the projection of actual chronological Jacobi variables, not only full unstable-cone growth.

The claimed compact group that smooths arbitrary velocity/path laws while conjugating hard-sphere dynamics and preserving all collision geometry has no construction and is incompatible with the limited symmetry group of the mechanical system.

### 7. B3 cannot create positivity through a KKT rewrite

At `Gamma=qA_f`, stationarity gives multiplier `lambda=q-1`. The constrained bordered Hessian restricted to `dot a=DA_f dot f` is exactly the original reduced Hessian, including

\[
(1-q)D^2A_f[\dot f,\dot f].
\]

For `A_f=f^2`, `q>1`, and residual-free directions it is negative. A positive covariance inverse can coincide with this Hessian only after a separate stability/second-epi-derivative theorem, not by definition.

### 8. B4's comparison tradeoff is unresolved

The slope cap `R` localizes states only to distance `C/R`. The collision Hamiltonian's local Lipschitz constant in the state grows exponentially with `R` because of `e^{Delta p}`. Thus the mismatch estimate behaves like `e^{cR}/R`, not something tending to zero. The theorem assumes no joint modulus capable of passing the two limits.

### 9. C1's common-saddle ratio is false

For

\[
E[e^{\mu H};Y=y]/P(Y=y),
\]

the source `H` changes the saddle. The numerator uses `lambda_H`, the denominator uses `lambda_0`. Their determinants and shell coefficients do not generally cancel. Evidence lifting is useful, but it does not remove source dependence.

### 10. C2's memory projector is the wrong projector

A Riesz spectral projector commutes with its generator. Compressing to that invariant eigenspace gives zero Mori–Zwanzig memory. A physically selected resolved-observable projection need not commute, but then it is not transported by the Kato equation for the leading Riesz projector. These objects must be separated.

### 11. D1's exponential remainder changes the rate

If every phase assigns a closed set cost above `2c` but the remainder places mass `e^{-c mu}` there, the physical cost is at most `c`. Therefore a remainder bounded by `e^{-c mu}` cannot be discarded from a full LDP. It must be superexponentially small or treated as another phase/rate component.

## Dependency audit

The declared Sinai chain is

```text
A2 -> A3 -> A4 -> C2/D1
```

with A1 independent. The review finds:

- A1 fails independently at the symbolic/mechanical identification and transfer norm;
- A2 fails its birth derivative, UNI/Dolgopyat, and local-error interfaces;
- A3 assumes finite projection rates and lacks recession/terminal recovery;
- A4 has an independent false memory-decay theorem;
- C2 and D1 cannot treat the Sinai interfaces as closed.

The hard-sphere chain is

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

The review finds:

- B2-GC remains open at the kinetic trace domain, projected Jacobi estimate, sewing, and regularization;
- B1 independently analyzes the wrong proxy pressure and has an invalid sharp shell coefficient;
- B3 lacks a positive identified tangent form and process cumulant theorem;
- B4 lacks a graph core and comparison theorem;
- C1's observed ratio and posterior-chaos interfaces are open;
- C2 and D1 inherit all upstream failures.

No downstream theorem label can close an upstream proof.

## Genuine improvements to retain

Round eight is not a null revision. A future reconstruction should preserve:

- A1's complete seam awareness, full-port work, and conditional calibration;
- A2's separation of aperiodicity, UNI, and roof-window scaling;
- A3's edge-flow marks and bounded escaped-clock ledger;
- A4's genuine past filtration, Doob transform, rough area, and causal sign;
- B1's regenerative compound smoothing, rank assumptions, and explicit low sectors;
- B2's compatibility-first trace philosophy and true-future preservation;
- B3's exact raw curvature and finite cumulant starting point;
- B4's dynamic-only action and correct terminal-value sign;
- C1's evidence lifting and reachable-belief restriction;
- C2's common transfer-space approach and two null spaces;
- D1's phase-restricted coexistence philosophy.

The reports reject the theorem packages, not every local idea.

## Recommended reconstruction order

1. Separate A1's symbolic germ extension from a genuine finite-dimensional symplectic section; build a directional transfer space.
2. Prove A2's physical birth connection, explicit UNI, all-iterate Dolgopyat bound, and window-matched LLT error.
3. Prove A3's finite edge/profile LDPs and distinguish one-excursion from mixture recession recovery.
4. State A4's memory theorem with sufficient vertical resolvent decay and construct any zero-mode realization on actual operator domains.
5. Build B2-GC on a measure-valued kinetic trace space with a physical depth-summable transversality theorem and a real balance-preserving regularizer.
6. Add B1's regenerative singleton factor to the full connected hard-sphere characteristic function and correct the shell integral.
7. Transfer B2-MC only after B1 is valid.
8. Rebuild B3 from a demonstrably positive reduced second variation or directly from finite-dimensional covariance limits without circular inversion.
9. Construct B4's observable graph core and a comparison penalty compatible with exponential source growth.
10. Prove C1's two-saddle observed coefficient and quenched chaos on evidence-controlled reachable states.
11. Separate C2's spectral normalization projector from its physical memory projection; fold D1's valid mixture/contraction lemmas into platform papers.

## Final recommendation

**Reject all eleven manuscripts in their present form.**  
**D1 should be removed as a standalone submission.**

The internal round-eight certificate verifies repository bytes and builds. It does not close the direct mathematical contradictions and missing model theorems identified above. The external top-four publication gate should remain closed.