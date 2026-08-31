# Round-Twelve GPT-5.6 Pro Referee Review — Eleven-Paper Index

**Repository:** `TrillionniumFoundation/theta-theory`  
**Review date:** 2026-09-01  
**Reviewed revision branch:** `revision/round12-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch/main head:** `10b553a750b3ba3f82c751e699446ed40db80d62`  
**Reviewed tree:** `4167b9abfb4e6e5ba5f12123f4bb73fd0f2139f6`  
**Controlling mathematical commit:** `1d9c66382df48ecc143638ad05785e2e4cb9b65b`  
**Review branch:** `review/round12-gpt56-pro-harsh-11paper-2026-08-31`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, and *Journal of the AMS*  
**Overall recommendation:** **Reject all eleven manuscripts in their present form.**  
**D1 recommendation:** **Remove as a standalone submission.**

## Evidence boundary

Round 12 is a genuine materialized revision. At review lock, `main` and the revision branch pointed to the same commit, every paper-level `main.tex` loaded `ROUND12_POSITIVE_CLOSURE.tex`, and the repository recorded 11/11 builds, 77/77 theorem/proof environments, active-module hashes, a dependency ledger, and an internal hostile rereview.

These are source-integrity and reproducibility facts. They are not mathematical certification. The internal hostile JSON largely checks for the presence of phrases such as “speed-dependent power,” “dominated convergence,” or “positive evidence.” It does not test the mathematical implications. Several Round 12 headline statements admit elementary counterexamples despite an internal `PASS`.

This review changes no manuscript source, proof module, PDF, workflow, certificate, bibliography, author response, or previous referee report. It adds only the eleven reports below and this index.

## Paper-level report paths

```text
papers/A1-exact-benchmarks/REFEREE_REPORT_ROUND12_GPT56_PRO.md
papers/A2-sinai-homological-pressure/REFEREE_REPORT_ROUND12_GPT56_PRO.md
papers/A3-full-empirical-path-ldp/REFEREE_REPORT_ROUND12_GPT56_PRO.md
papers/A4-history-memory-universal-pressure/REFEREE_REPORT_ROUND12_GPT56_PRO.md
papers/B1-microcanonical-preparation/REFEREE_REPORT_ROUND12_GPT56_PRO.md
papers/B2-collision-clusters-dynamic-ldp/REFEREE_REPORT_ROUND12_GPT56_PRO.md
papers/B3-hamilton-boltzmann-cotangents/REFEREE_REPORT_ROUND12_GPT56_PRO.md
papers/B4-nonlinear-kinetic-semigroups/REFEREE_REPORT_ROUND12_GPT56_PRO.md
papers/C1-information-risk-sensitive-saddles/REFEREE_REPORT_ROUND12_GPT56_PRO.md
papers/C2-cotangent-rigidity-tangent-representations/REFEREE_REPORT_ROUND12_GPT56_PRO.md
papers/D1-deterministic-theta-contractions/REFEREE_REPORT_ROUND12_GPT56_PRO.md
```

## Editorial verdicts

| Paper | Recommendation | Decisive Round 12 finding | Genuine repair recognized |
|---|---|---|---|
| **A1 — Exact Benchmarks** | Reject | Forward/backward bi-cylinders shrink in both physical directions, so the all-depth refinement is zero-dimensional symbolic data, not a section with two-dimensional symplectic leaves. | Correct coupled natural extension, target refinement, flag currents, and conditional risk calibration. |
| **A2 — Sinai Homological Pressure** | Reject | The “compact gap” includes frequencies tending to zero, and the very-high-frequency bound contains a constant `Ce^{-cn}` on an infinite interval, whose Fourier integral diverges. | Parent-fold viewpoint, removal of period-one winding orbits, separate UNI/arithmetic, exact window masses. |
| **A3 — Full Empirical-Path LDP** | Reject | An order-`n` entropy budget can promote an exponentially rare shield-failure event to constant probability, directly contradicting the uniform `e^{-Mn}` controlled shield. | Deterministic clocks, actual terminal excursion, original renewal kernel, explicit recession state. |
| **A4 — History, Memory, Universal Pressure** | Reject | Finite-step transition laws from different complete pasts retain disjoint deterministic remote tails, so the stated common Doeblin minorization is impossible. | Correct Poisson martingale, eigenfunction Doob normalization, causal memory sign, instantaneous terms. |
| **B1 — Microcanonical Preparation** | Reject without invitation in current architecture | The compound-Poisson empty configuration leaves a nonzero `e^{-c mu}` high-frequency characteristic tail; it cannot satisfy `(1+|u|)^{-s mu}` decay. | Exact source-dependent saddles, relative-interior targets, regular shell mass conditions. |
| **B2 — Collision Clusters and Dynamic LDP** | Reject | Fixed-horizon dominated convergence gives at most `o(1)` total cyclic weight; it does not give the `h omega(epsilon)` uniform block modulus needed to sew `T/h` blocks. | Correct normal trace, true reflected future, fixed-genealogy rather than false uniform exponents. |
| **B3 — Hamilton–Boltzmann Cotangents** | Reject | The advertised joint density/contact Gaussian bracket omits the independent contact test. Pure contact observables are assigned zero variance. | Perturbative chart, covariance first, diagonal fourth-moment term, correct Cameron–Martin domain. |
| **B4 — Nonlinear Kinetic Semigroups** | Reject | The displayed subsolution inequality bounds by `Phi + I`, not the value `sup(Phi - I)`, so the claimed comparison sandwich does not follow. | Correct microscopic typing, one-time preparation charge, observable resolvent, primal action focus. |
| **C1 — Information and Saddles** | Reject | Fixed finitely many cumulants do not determine a law up to `o(1)` Wasserstein error, even for compactly supported laws with entire MGFs. | Positive disintegration separated from currents, explicit zero-evidence direction, exact full-belief state. |
| **C2 — Cotangent Rigidity and Representations** | Reject | `F=0`, `G=1` disproves the claim that equality of all invariant integrals is equivalent to a difference in `R1 + N_inv`. | Signed dual, full perturbation functional, finite spectral frame, typed source/state derivatives. |
| **D1 — Deterministic Theta Contractions** | Reject; remove standalone paper | Positivity of an operator does not make every Riesz band projection positive; the proposed spectral labels can be signed and are not probabilities. | Correct normalized component pressure convention and explicit remainder principle. |

## Root-level mathematical findings

### 1. A1's inverse-limit dimension is wrong

If `p_*<1` is the largest branch width, a depth `(-m,n)` bi-cylinder has horizontal diameter at most `p_*^{n+1}` and vertical diameter at most `p_*^m`. The completed cylinder components form arbitrarily fine clopen neighborhoods. Their inverse limit is the two-sided symbolic completion, locally zero-dimensional; finite-stage area forms do not create a nondegenerate limiting two-form. The Hamiltonian solenoid theorem therefore has no section on which to act.

### 2. A2's Fourier theorem fails in two elementary regimes

At `b=n^{-2/5}`, the leading eigenvalue tends to one, so no uniform compact-frequency gap exists. At very high frequency,

```text
||L_{ib}^n|| <= C e^{-cn} + C(C/|b|)^{eta n}
```

cannot be integrated over `|b|>L_n`, because the first term is constant in `b`. The density LLT and every inserted clock coefficient remain unavailable.

### 3. A3's entropy shield has a universal counterexample

If `P(A_n)=e^{-Ln+o(n)}`, the controlled mixture

```text
Q_n = q P(.|A_n) + (1-q) P(.|A_n^c)
```

has `D(Q_n||P_n)=qLn+O(1)` but `Q_n(A_n)=q`. Choosing `q<M/L` gives entropy cost below `Mn` and constant shield failure probability. Finite-cost controls cannot inherit exponential approximation from the reference law.

### 4. A4 cannot be Doeblin on the complete past

After `m` updates, all coordinates older than `m` remain a shifted copy of the initial past. Two distinct remote tails yield disjoint supports of `P^m(H,.)`. A common nonzero minorizing measure cannot exist. A weighted Wasserstein/Hölder coupling may be possible, but it is not the theorem proved in the manuscript.

### 5. B1 contradicts its singleton compound-Poisson model

For activity `a` and mark characteristic `nu_hat(u)`,

```text
phi_mu(u) = exp{mu a(nu_hat(u)-1)} -> e^{-mu a}
```

as `|u|->infinity`. The zero-particle atom prevents the characteristic function from decaying to zero. The claimed speed-dependent power tail and the logarithmically diverging pressure gap are false, so the shell coefficient proof cannot use absolute Fourier inversion as written.

### 6. B2 has not proved the blockwise recollision modulus

An `L1` time majorant gives absolute continuity, not a uniform linear modulus. An integrable density such as `t^{-1/2}` has mass `O(sqrt h)` on a block of length `h`. The factor `h` required to sum `T/h` block errors needs an `L-infinity` or equivalent nonconcentration theorem absent from the fixed-genealogy argument.

### 7. B3's covariance misses half of the joint source

For a density/contact dual pair `(p,psi)`, one collision has coefficient `Delta p + psi`. The bracket must be

```text
integral q (Delta p + psi)(Delta p' + psi') dA_f dt.
```

The displayed bracket contains only density increments, so it makes pure contact noise vanish. This invalidates the covariance kernel and all inverse-form conclusions.

### 8. B4's comparison proof has the wrong value inequality

From the manuscript's subsolution estimate one obtains `u(s)<=Phi(path)+I(path)`. This is unrelated to `S Phi=sup(Phi-I)`. The supersolution half alone cannot yield comparison. A consistent HJ sign convention and a valid viscosity-to-control verification theorem are still required.

### 9. C1's finite-correlation reduction is false

Distinct probability laws can have the same first `K` moments for any fixed `K`, entire moment-generating functions, and positive Wasserstein separation. A fixed analytic radius only bounds the omitted cumulants; it does not make their tail vanish with the Boltzmann–Grad parameter. The reduced game is therefore not derived from the full belief state.

### 10. C2's constant direction disproves the quotient statement

A nonzero constant belongs to `R1+N_inv` but changes the integral under every invariant probability. Equality of all invariant integrals corresponds to `N_inv`; equality up to one common constant corresponds to `R1+N_inv`. The theorem states the latter space for the former property.

### 11. D1's spectral labels are not positive

For the positive matrix

```text
A = [[2,1],[1,2]],
```

the Riesz projection onto eigenvalue `1` is

```text
(1/2) [[1,-1],[-1,1]],
```

which is signed. Perron–Frobenius positivity of the leading eigenvector does not make every peripheral/subleading band projection positive. The proposed `chi_{n,j}` are not established probabilities, and no exact phase disintegration follows.

## Internal-verification audit

The Round 12 internal certificate correctly records:

- 11/11 active source modules;
- 11/11 nonempty PDFs;
- 77/77 theorem/proof environments;
- no unresolved TeX references; and
- an acyclic declared dependency graph.

The hostile JSON, however, checks tokens and a few scalar regressions. Examples:

- B1 passes because the phrase “speed-dependent power” is present, even though that bound contradicts the empty-sector atom.
- B2 passes because “dominated convergence” and `h omega_T(epsilon)` are present, although the former does not imply the latter.
- D1 passes because “complementary band” appears, without testing positivity of the Riesz projections.

These gates are useful source regressions, not theorem validation.

## Dependency audit

The Sinai chain remains

```text
A2 -> A3 -> A4 -> C2 -> D1
```

with A1 independent.

- A2 has no valid integrable Fourier theorem.
- A3 has a false controlled shield and no completed physical path LDP.
- A4 has an impossible complete-past Doeblin theorem.
- C2 and D1 cannot use their spectral, history, or phase interfaces as closed.

The hard-sphere chain remains

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

- B2-GC lacks a blockwise recollision modulus and full lower-recovery theorem.
- B1's primitive coefficient is false.
- B3's joint covariance is incorrectly typed.
- B4 lacks comparison.
- C1's reduction and coefficient inherit those failures.
- C2 and D1 remain downstream syntheses.

No downstream theorem label, internal certificate, or finite build can close an upstream mathematical gap.

## Genuine Round 12 improvements to retain

Round 12 is not a null revision. The following ideas should be preserved:

- **A1:** target refinement, coupled natural extension, graded flags, global work cocycle.
- **A2:** parent-fold viewpoint, no period-one winding orbit, separated UNI/arithmetic/window regimes.
- **A3:** deterministic clocks, terminal residual, actual recession profiles.
- **A4:** correct Poisson martingale, Doob normalization, causal memory sign, instantaneous terms.
- **B1:** source-dependent exact saddle and a declared regular shell class.
- **B2:** one flux trace, true future, fixed-genealogy rather than fictitious uniform exponent.
- **B3:** perturbative chart, covariance first, microscopic diagonal, square-root covariance domain.
- **B4:** correct finite-volume typing and one-time preparation.
- **C1:** positive posterior measures separated from oriented currents and an explicit zero-evidence direction.
- **C2:** signed invariant duals and full-pressure rather than scalar-pressure rigidity.
- **D1:** normalized component pressures and explicit remainder accounting.

The reports reject the theorem packages, not every local design choice.

## Recommended reconstruction order

1. Replace A1's shrinking refinement by either the ordinary physical symplectic section or a genuine covering-map solenoid.
2. Prove an actually integrable A2 vector–roof spectral/LLT theorem.
3. Rebuild A3's controlled LDP with singularity exposure retained at finite cost.
4. Prove A4 via weighted coupling/transfer methods rather than impossible full-past minorization.
5. Establish B2-GC with a uniform block-time cyclic modulus and complete lower recovery.
6. Rebuild B1's exact-number coefficient after isolating low-particle atoms.
7. Transfer B2-MC only after B1 is valid.
8. Type B3 on the joint collision noise coefficient `Delta p + psi`.
9. Prove B4 comparison with a consistent HJ/value convention.
10. Restrict C1 to a proved Feller observation model and a quantitative, scaling-dependent chaos class.
11. Correct C2's quotients and common-domain form construction.
12. Remove D1 as a standalone paper until a platform constructs a genuine positive phase decomposition.

## Final recommendation

**Reject all eleven manuscripts in their present form.**  
**D1 should be removed as a standalone submission.**

The external top-four publication gate should remain closed.