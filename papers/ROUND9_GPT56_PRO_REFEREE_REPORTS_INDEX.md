# Round-Nine GPT-5.6 Pro Referee Review — Eleven-Paper Index

**Repository:** `TrillionniumFoundation/theta-theory`  
**Review date:** 2026-08-31  
**Reviewed revision branch:** `revision/round9-referee-positive-closure-11paper-2026-08-31`  
**Payload-host branch head at review lock:** `a8c0c551f5f8614856a9d433e78b2eb92a5dcfa1`  
**Registered payload SHA-256:** `cf230322211332af59a7883af1b669eeb9b4f7e9f4220fc24712c634bda17716`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, and *Journal of the AMS*  
**Overall recommendation:** **Reject all eleven manuscripts in their present form.**  
**D1 recommendation:** **Remove as a standalone submission.**

## Evidence boundary and source-control status

At the review lock, the round-nine branch contained the checksum-pinned source payload while its paper-level `main.tex` files still loaded the round-eight controlling modules. The repository publication workflow was queued. I independently:

1. downloaded the repository's successful round-nine source-snapshot artifact;
2. verified the snapshot SHA-256;
3. concatenated and decoded the seven `.round9/payload.part-*` files;
4. verified the registered payload SHA-256 `cf230322211332af59a7883af1b669eeb9b4f7e9f4220fc24712c634bda17716`;
5. unpacked the registered source;
6. ran `tools/materialize_round9_referee.py`, which returned `ROUND9_MATERIALIZATION_PASS papers=11`; and
7. reviewed the eleven resulting byte-identical `ROUND9_POSITIVE_CLOSURE.tex` modules.

Thus the mathematical review concerns the exact registered round-nine theorem bytes. It does not pretend that a queued workflow had completed at the review lock. Compilation, source hashes, theorem/proof counts, internal hostile scripts, and publication receipts receive repository-integrity credit only, not theorem credit.

The reports add no manuscript source, proof module, workflow, certificate, PDF, bibliography, or author-response changes.

## Paper-level report paths

```text
papers/A1-exact-benchmarks/REFEREE_REPORT_ROUND9_GPT56_PRO.md
papers/A2-sinai-homological-pressure/REFEREE_REPORT_ROUND9_GPT56_PRO.md
papers/A3-full-empirical-path-ldp/REFEREE_REPORT_ROUND9_GPT56_PRO.md
papers/A4-history-memory-universal-pressure/REFEREE_REPORT_ROUND9_GPT56_PRO.md
papers/B1-microcanonical-preparation/REFEREE_REPORT_ROUND9_GPT56_PRO.md
papers/B2-collision-clusters-dynamic-ldp/REFEREE_REPORT_ROUND9_GPT56_PRO.md
papers/B3-hamilton-boltzmann-cotangents/REFEREE_REPORT_ROUND9_GPT56_PRO.md
papers/B4-nonlinear-kinetic-semigroups/REFEREE_REPORT_ROUND9_GPT56_PRO.md
papers/C1-information-risk-sensitive-saddles/REFEREE_REPORT_ROUND9_GPT56_PRO.md
papers/C2-cotangent-rigidity-tangent-representations/REFEREE_REPORT_ROUND9_GPT56_PRO.md
papers/D1-deterministic-theta-contractions/REFEREE_REPORT_ROUND9_GPT56_PRO.md
```

## Editorial verdicts

| Paper | Recommendation | Decisive round-nine finding | Genuine repair recognized |
|---|---|---|---|
| **A1 — Exact Benchmarks** | Reject | For the centered one-coordinate cylinder \(f(\omega_0)\), \(\|\mathcal L^nf\|_+\ge\alpha^{-n}\|f\|_1\), contradicting the claimed bounded Lasota–Yorke estimate. The “autonomous Hamiltonian” still uses an external impact reset. | Physical and symbolic states are separated; full-port work and conditional calibration are correctly scoped. |
| **A2 — Sinai Homological Pressure** | Reject | The birth connection and physical spectral bundle are not constructed; the orbit determinant and UNI packet are asserted. The high-frequency bound is not Fourier-integrable, and the sharp-window corollary exceeds the central density theorem. | Arithmetic, UNI, and density-level LLT are treated as distinct interfaces. |
| **A3 — Full Empirical-Path LDP** | Reject | The theorem uses the random clock \(R_N\) as an LDP speed. Return-length truncation is not exponentially good at collision speed, and the SPR/recession dichotomy is false for positive-recurrent non-SPR shifts. | Actual edges, profiles, return intensity, and a pointed terminal coordinate are retained. |
| **A4 — History, Memory, Universal Pressure** | Reject | The proposed martingale difference has conditional mean \(A(H_n)\), not zero. The normalized Feynman–Kac log transform is not a semigroup. | A genuine past filtration, causal memory sign, and instantaneous/residual distinction are adopted. |
| **B1 — Microcanonical Preparation** | Reject | Dynamical path tilts do not yield the asserted conditionally independent good cells. The admitted shell class includes exponentially tiny sets, contradicting the claim that shell factors are subexponential. | The full source-dependent saddle and weighted shell likelihood are retained. |
| **B2 — Collision Clusters and Dynamic LDP** | Reject | The normal trace is double-weighted in the Green identity. The flux-weighted inverse-Jacobi estimate and depth-uniform surplus gain are unproved for semi-dispersing hard spheres; the finite-cell repair has no quantitative right inverse. | The true reflected future is retained and block errors are scaled linearly in block length. |
| **B3 — Hamilton–Boltzmann Cotangents** | Reject | The balance constraint is linear, so its multiplier has zero second variation; the claimed KKT curvature is not present in the displayed Lagrangian. | Raw indefinite curvature is acknowledged and finite covariance is used as the starting point. |
| **B4 — Nonlinear Kinetic Semigroups** | Reject | State and observable semigroups are mixed: the log-Laplace and resolvent formulas are ill-typed. The fixed-truncation doubling penalty still produces unbounded cotangents. | Static preparation is charged once and the terminal-value corrector sign is repaired. |
| **C1 — Information and Saddles** | Reject | An unnormalized current does not make normalized posteriors Feller at zero evidence. B1's additive good-block Fourier method does not apply to an arbitrary global observation map; the finite correlation skeleton is circularly defined. | Evidence, singular coarea currents, and separate numerator/denominator saddles are retained. |
| **C2 — Cotangent Rigidity and Representations** | Reject | Kato's ODE loses one Banach level at every iteration and cannot define an invertible evolution on the stated scale. The resolved Hilbert projection is assumed, not transported by the phase eigenline. | Null spaces, phase projection, resolved projection, and nonlinear contraction are distinguished. |
| **D1 — Deterministic Theta Contractions** | Reject; remove standalone paper | The exact phase-labelled mixture is not constructed by A3 or B1/B2; exposed/tilted laws are not latent components of the original physical law. The theorem assumes every difficult platform lower bound. | It no longer discards exponential remainders or infers a rate minimum from a pressure maximum. |

## Root-level mathematical findings

### 1. A1 has a one-line functional-analytic counterexample

For
\[
 f(\omega)=1_{\{\omega_0=i\}}-p_i
\]
and \(\mathcal Lf=f\circ\sigma^{-1}\),
\[
 \mathcal L^nf=1_{\{\omega_{-n}=i\}}-p_i.
\]
The strong norm assigns the past-depth weight \(\alpha^{-n}\), so it grows exponentially. The proposed right side is bounded. This directly invalidates the spectral gap and every reduced-resolvent response formula.

### 2. A4 contains two independent algebraic contradictions

First,
\[
 D_{n+1}=A(H_n)+\chi(H_{n+1})-\mathsf P\chi(H_n)
\]
satisfies
\[
 E(D_{n+1}\mid\mathcal F_n^-)=A(H_n),
\]
not zero.

Second,
\[
 \mathcal E_t^VF=\log P_t^V(e^F)-\log P_t^V1
\]
does not obey a semigroup law when \(P_t^V1\) depends on the state. These are not missing estimates; the displayed identities are false.

### 3. A3's finite truncation discards the phenomenon its boundary is meant to describe

At collision speed, one excursion with length proportional to the total clock has probability \(e^{-cR}\), a finite large-deviation cost. It changes the empirical profile by order one. Such events are not exponentially good truncation errors. The recession coordinate must be present in the finite projected theorem rather than added after a finite-state LDP.

### 4. B1's shell hypotheses include exponentially costly shells

A shell of continuous width \(e^{-2\mu}\) satisfies the manuscript's diameter condition but contributes an order-\(\mu\) logarithmic cost. Therefore the final pressure proof cannot say that every admitted shell integral is subexponential. Relative local coefficients also need a lower bound on the Gaussian shell mass.

### 5. B2's root estimate is still the missing theorem

The paper needs an inverse-moment/coarea estimate for the physical hard-sphere Jacobi map that is summable jointly in genealogical depth and \(\varepsilon\). Semi-dispersing collision cylinders have neutral directions, and incoming flux does not automatically compensate products of all inverse incidence factors. No quantitative proof is supplied.

### 6. B3's “KKT completion” does not exist for the displayed constraint

The weak balance is linear in \((f,\Gamma)\). Therefore its multiplier term has zero Hessian. The manuscript's additional curvature cannot arise from the written Lagrangian. The subsequent coercivity and Mosco identification are built on a nonexistent term.

### 7. B4's exact state construction confuses four different levels

The text alternates among microscopic states, probability laws, observables on microscopic states, and observables on law space. A state pushforward resolvent cannot be applied to an observable without passing to the dual semigroup. The nonlinear empirical generator cannot be obtained by exponentiating a deterministic law generator.

### 8. C1's zero-evidence problem is projective, not solved by retaining mass

If unnormalized posteriors converge to zero, their normalized directions can converge to different singular beliefs. Recording \(\log Z\to-\infty\) preserves evidence but does not make the projective posterior continuous. A compactification of directions or a finite-evidence restriction is required.

### 9. C2's scale connection loses regularity at every Picard step

A coefficient mapping \(\mathbb B^{m+1}\to\mathbb B^m\) does not generate an invertible Kato evolution on one Banach space. Repeated integration consumes arbitrarily many derivatives. The paper needs a fixed-space projector theorem or a tame smoothing evolution.

### 10. D1 labels a new mixture rather than decomposing the physical law

Phase-specific tilted laws can be useful changes of measure, but they are not automatically components of one latent mixture. Defining a prior over them creates a different physical law. Without an exact platform phase decomposition, the final “commutation principle” is conditional bookkeeping.

## Dependency audit

The Sinai chain remains:

```text
A2 -> A3 -> A4 -> C2/D1
```

with A1 independent.

- A1 independently fails its directional spectral estimate.
- A2 has no proved moving-billiard spectral/UNI/density packet.
- A3 has an ill-typed speed and no valid recession-inclusive finite LDP.
- A4 has direct martingale and nonlinear-semigroup errors.
- C2 and D1 cannot use these interfaces as closed.

The hard-sphere chain remains:

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

- B2-GC is open at the transport trace and surplus-contact theorem.
- B1 independently lacks its full Fourier coefficient and valid shell class.
- B3 has no valid constrained quadratic form.
- B4 has no typed microscopic nonlinear semigroup or comparison theorem.
- C1 has an independent filtering-state and observation-coefficient gap.
- C2 and D1 inherit the entire chain.

No downstream theorem label can close an upstream mathematical gap.

## Genuine improvements to retain

Round nine is not a null revision. The following ideas should be retained:

- **A1:** separate physical section and symbolic completion; full-port work; conditional calibration.
- **A2:** distinguish birth geometry, arithmetic, UNI, and density LLT.
- **A3:** retain actual edges, profiles, block intensity, and pointed terminal data.
- **A4:** use a genuine past filtration; separate instantaneous distributions; use causal memory sign.
- **B1:** reoptimize the exact source saddle and keep the likelihood inside the shell integral.
- **B2:** keep compatible traces and the true future; scale block errors with block length.
- **B3:** acknowledge raw indefinite curvature and construct covariance from finite cumulants first.
- **B4:** charge preparation once and use terminal-value correctors.
- **C1:** retain evidence, singular currents, and separate saddles.
- **C2:** separate spectral, resolved, and contraction objects; avoid infinite-path RN densities.
- **D1:** retain exact exponential remainders and label coexistence before contraction.

The reports reject the theorem packages, not every local design choice.

## Recommended reconstruction order

1. Correct A1's anisotropic norm and prove a real operator theorem; scope the impact realization honestly.
2. Prove A2 as a standalone parameter-uniform billiard spectral/UNI/density theorem.
3. Reindex A3 by deterministic clock and include recession in every finite projection.
4. Correct A4's martingale algebra and replace the normalized Feynman–Kac family by a genuine semigroup.
5. Prove B2-GC on a rigorously typed trace space with the complete Jacobi/coarea estimate.
6. Prove B1's full tilted Fourier theorem and impose a valid shell regime.
7. Transfer B2-MC only after B1 is valid.
8. Derive B3's true constrained second variation and prove a separate process CLT.
9. Rebuild B4 on the dual observable semigroup and solve the comparison/core problem.
10. Construct C1 on a restricted observation model with a projective zero-evidence state.
11. Recast C2 on a fixed transfer space and fold D1's generic mixture identities into platform papers.

## Final recommendation

**Reject all eleven manuscripts in their present form.**  
**D1 should be removed as a standalone submission.**

The external top-four publication gate should remain closed.
