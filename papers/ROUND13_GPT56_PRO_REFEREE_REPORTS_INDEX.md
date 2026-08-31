# Round-Thirteen GPT-5.6 Pro Referee Review — Eleven-Paper Index

**Repository:** `TrillionniumFoundation/theta-theory`  
**Review date:** 2026-09-01  
**Reviewed revision branch:** `revision/round13-referee-positive-closure-11paper-2026-09-01`  
**Reviewed branch/main head:** `5c8b71e67d62d4a63c53a5a59e7a10f1ccc0f688`  
**Reviewed tree:** `586de2e3cf8c547ca3cbfbc0cb0daba2fd05af59`  
**Controlling mathematical commit:** `87c9068e4a62fb3ab0abfbe7b152259e0aab4321`  
**Review branch:** `review/round13-gpt56-pro-harsh-11paper-2026-09-01`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, and *Journal of the AMS*  
**Overall recommendation:** **Reject all eleven manuscripts in their present form.**  
**D1 recommendation:** **Remove as a standalone submission.**

## Evidence boundary

Round 13 is a genuine materialized revision. At the review lock, `main` and the revision branch pointed to the same commit, every paper-level `main.tex` loaded `ROUND13_POSITIVE_CLOSURE.tex`, and the repository recorded 11/11 builds, 75/75 theorem/proof environments, active-module hashes, a dependency ledger, and an internal hostile rereview.

Those facts establish source identity, compilation, and document structure. They are not mathematical certification. The internal hostile JSON mostly verifies the presence of phrases such as “Dominated convergence,” “Nisio,” “growing finite coordinate,” or `Delta p+psi`; it does not test the implications. Several Round 13 headline statements admit explicit counterexamples despite the internal `PASS`.

This review changes no manuscript source, proof module, PDF, workflow, certificate, bibliography, author response, or previous referee report. It adds only the eleven reports below and this index.

## Paper-level report paths

```text
papers/A1-exact-benchmarks/REFEREE_REPORT_ROUND13_GPT56_PRO.md
papers/A2-sinai-homological-pressure/REFEREE_REPORT_ROUND13_GPT56_PRO.md
papers/A3-full-empirical-path-ldp/REFEREE_REPORT_ROUND13_GPT56_PRO.md
papers/A4-history-memory-universal-pressure/REFEREE_REPORT_ROUND13_GPT56_PRO.md
papers/B1-microcanonical-preparation/REFEREE_REPORT_ROUND13_GPT56_PRO.md
papers/B2-collision-clusters-dynamic-ldp/REFEREE_REPORT_ROUND13_GPT56_PRO.md
papers/B3-hamilton-boltzmann-cotangents/REFEREE_REPORT_ROUND13_GPT56_PRO.md
papers/B4-nonlinear-kinetic-semigroups/REFEREE_REPORT_ROUND13_GPT56_PRO.md
papers/C1-information-risk-sensitive-saddles/REFEREE_REPORT_ROUND13_GPT56_PRO.md
papers/C2-cotangent-rigidity-tangent-representations/REFEREE_REPORT_ROUND13_GPT56_PRO.md
papers/D1-deterministic-theta-contractions/REFEREE_REPORT_ROUND13_GPT56_PRO.md
```

## Editorial verdicts

| Paper | Recommendation | Decisive Round 13 finding | Genuine repair recognized |
|---|---|---|---|
| **A1 — Exact Benchmarks** | Reject | The current norm is an infimum over refinements weighted by `4 rho_- < 1`, `4 rho_+ < 1`; the nonzero constant density therefore has norm zero. | Physical/symbolic separation, coupled natural extension, target impact category, explicit exponential work family. |
| **A2 — Sinai Homological Pressure** | Reject | The joint variable has four scalar coordinates `(kappa_1,kappa_2,r,tau)`, but the LLT uses the three-dimensional prefactor `n^{-3/2}` instead of `n^{-2}`. | Integrable-looking high-frequency bound, covariance damping near zero, removal of period-one winding orbits. |
| **A3 — Full Empirical-Path LDP** | Reject | The displayed rate contains the terminal residual law `rho` in the reconstruction map but no terminal residual cost; the recession state and Γ-limit are partly undefined. | Deterministic clocks, one likelihood for the terminal branch, retained singularity exposure and macroscopic excursions. |
| **A4 — History, Memory, Universal Pressure** | Reject | A neighborhood in the weighted Lipschitz space contains potentials for which `P(e^V)` is infinite; poles of `C(z)` are also incorrectly treated as memory poles despite pole-zero cancellation. | Wasserstein rather than TV coupling, correct Poisson martingale, eigenfunction Doob normalization, instantaneous memory terms. |
| **B1 — Microcanonical Preparation** | Reject | The stated high-frequency bound contains a fixed power `(1+|u|)^{-s-cN_0}` whose integral is constant in `N`, contradicting the claimed `o(N^{-1/2})` tail. | Exact-number extraction before continuous Fourier inversion and separate source-dependent saddles. |
| **B2 — Collision Clusters and Dynamic LDP** | Reject | The trace norm multiplies an already normal-flux measure by `v·n` again; symplectic invertibility does not imply a nondegenerate transverse position minor. | Fixed-horizon global genealogy sum, true reflected future, genealogy-dependent rather than fictitious uniform exponents. |
| **B3 — Hamilton–Boltzmann Cotangents** | Reject | Conditioning on the complete microscopic state reveals the next deterministic collision, directly contradicting the asserted Poisson-type stopping-time fourth-moment bound. | Correct joint noise coefficient `Delta p+psi`, pure-contact variance, microscopic diagonal term, square-root covariance domain. |
| **B4 — Nonlinear Kinetic Semigroups** | Reject | A deterministic Koopman generator is a derivation, so `mu^{-1}e^{-mu F}A e^{mu F}=AF`; it cannot produce the exponential collision Hamiltonian. | Correct five-way typing, dynamic-only action, backward sign, attempt to use a Nisio value rather than an uncontrolled doubled jet. |
| **C1 — Information and Saddles** | Reject | The cone quotient collapses all zero-evidence directions while the text says they are retained; flat positive families can have zero evidence with oscillating normalized directions. | Positive posterior/current separation, joint Rokhlin kernel, growing rather than fixed moments, informative-strategy restriction. |
| **C2 — Cotangent Rigidity and Representations** | Reject | The dual of a Hölder/graph algebra is not merely Radon measures; the common “norm” also inserts a generally complex sectorial form value `a(F,F)`. | Correct invariant-integral distinction, full-pressure rather than scalar rigidity, separated source/state derivatives. |
| **D1 — Deterministic Theta Contractions** | Reject; remove standalone paper | Conditional rates on basin boundaries are not `I-alpha` without basin-internal recovery; nonlinear log-Laplace values do not commute with finite phase mixing. | Positive measurable basins, explicit boundary label, normalized component pressure convention. |

## Root-level mathematical findings

### 1. A1's refinement norm collapses every fixed bulk current

For the constant bulk density `U=1`, the representation on an `(m,n)` refinement has at most `C 4^{m+n}` cells and unit cell norms. Hence

```text
||[U]|| <= C (4 rho_-)^m (4 rho_+)^n -> 0.
```

Because the norm is the infimum over equivalent refinements, `U` has zero norm although it is not the zero current. The asserted Hausdorff Banach complex and all response operators built on it fail.

### 2. A2 uses the wrong Gaussian dimension

Fourier inversion is over

```text
T^2 (homology) x T (return count) x R (roof),
```

so the local density coefficient is of order

```text
(2 pi n)^(-4/2) = (2 pi n)^(-2).
```

The theorem writes `(2 pi n)^(-3/2)`. It therefore overstates the joint local probability by `sqrt(n)`. Its saddle notation also centers at the target and simultaneously inserts a second nonzero Gaussian deviation.

### 3. A3's rate does not contain the cost it says it charges

The rate is

```text
(1-alpha) R_c(eta) + alpha integral J_c d zeta
```

subject to a reconstruction depending on `(eta,alpha,zeta,rho)`. There is no term involving the pointed terminal residual `rho`, although the proof says a macroscopic terminal prefix is paid through that coordinate. The recession probability is additionally written using an unspecified entrance distribution and an undefined scalar normalization of a path.

### 4. A4's descriptor rule has a one-dimensional counterexample

With `L=-1` and `R=I`,

```text
C(z)=1/(z+1)
```

has a pole at `-1`, but

```text
Khat(z)=z+1-C(z)^(-1)=0.
```

There is no descriptor or memory mode. Poles of `C` can cancel in `C^{-1}`; descriptors must be extracted from the final Schur complement, not from every pole and zero of the compressed resolvent.

### 5. B1's displayed Fourier majorant cannot prove the shell coefficient

For fixed `N_0`,

```text
integral_{|u|>R} (1+|u|)^(-s-cN_0) du
```

is a positive constant independent of `N`. It is not `o(N^{-1/2})`. The proof's stronger `s+cN` exponent is assigned only to an unproved “good-label sector,” not to the global bound.

### 6. B2's symplectic argument confuses full phase-space rank with position rank

An invertible symplectic map can send a position plane into momentum directions; `(q,p)->(p,-q)` is the elementary example. Therefore independence of two Jacobi fields in full phase space does not imply that their two transverse position components at the surplus time have nonzero determinant. The fixed-genealogy sublevel estimate has no proved nonzero analytic minor.

### 7. B3's conditional increment estimate contradicts deterministic future knowledge

Choose a full-state stopping time just `h/2` before a known regular collision. Conditional on the microscopic state, one contact occurs with probability one. Its scaled fourth moment is `mu^{-2}`. Taking `h=mu^{-3}`, the claimed bound

```text
C(h^2+h/mu)
```

is only `O(mu^{-4})`. The Aldous input is false on the stated filtration.

### 8. B4 applies a stochastic nonlinear-generator identity to a Koopman derivation

For the deterministic Koopman generator,

```text
A exp(mu F) = mu exp(mu F) A F.
```

Thus exponential conjugation remains linear. The proof silently replaces `A` by a factorial hierarchy generator without an intertwining theorem. The advertised Hamilton–Boltzmann generator is ill-typed.

### 9. C1's zero-evidence direction has a flat oscillatory counterexample

The positive family

```text
Lambda_t = exp(-1/t^2)[(1+0.5 sin(1/t)) delta_0
                       +(1-0.5 sin(1/t)) delta_1]
```

has mass smaller than every power and no first nonzero Taylor coefficient, while its normalized direction oscillates. Neither the proposed leading-coefficient rule nor a collapsed cone gives a unique continuous zero-evidence lift.

### 10. C2 combines incompatible topologies

Radon duality belongs to a weighted strict continuous-function topology. Spectral response and Hölder coboundary closure use a stronger Hölder/graph topology whose dual includes distributions. The manuscript invokes both as though they were the same space. Its common form norm is also not real/positive for a sectorial form.

### 11. D1's nonlinear “commutation” is false

For two deterministic phases with payoffs `0` and `1` and equal weights,

```text
(1/n) log[(1+e^n)/2] -> 1,
```

whereas the weighted mixture of component log values is `1/2`. Linear evolution of component measures before taking a logarithm produces log-sum-exp, not a positive mixture of nonlinear semigroups.

## Internal-verification audit

The Round 13 certificate correctly records:

- 11/11 active source modules;
- 11/11 nonempty PDFs;
- 75/75 theorem/proof environments;
- zero unresolved TeX references; and
- an acyclic declared dependency graph.

The hostile JSON is primarily a source-regression script. Examples:

- A1 passes because the phrases “Complete graded flag complex” and “codimension at most q” are present, but it does not test whether the norm annihilates constants.
- A2 records one small-frequency numerical value but does not count the four Fourier coordinates in the LLT prefactor.
- B1 passes because “linear number of” and “compact annulus” occur, without integrating the displayed fixed-power tail.
- B2 passes because “Dominated convergence” is present, without validating the transverse minor.
- B4 passes because “Nisio” appears, without checking the Koopman chain rule.

These gates are useful for exact-source identity and regression, not theorem validation.

## Dependency audit

The Sinai chain remains

```text
A2 -> A3 -> A4 -> C2 -> D1
```

with A1 independent.

- A2's joint LLT is misnormalized and its bundle/UNI proof is incomplete.
- A3 has no complete recurrent–recession rate or recovery theorem.
- A4's source chart and descriptor memory are invalid.
- C2 and D1 cannot use the path, filtration, memory, or phase interfaces as closed.

The hard-sphere chain remains

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

- B2-GC lacks a valid trace topology, Jacobi theorem, and lower recovery.
- B1 lacks the canonical high-frequency coefficient.
- B3 lacks a valid tightness theorem on its chosen filtration.
- B4 confuses Koopman and hierarchy generators and has no proved nonlinear resolvent.
- C1's filtering reduction and C2's form bundle inherit these failures.
- D1 is a downstream conditional mixture note.

No downstream theorem label, internal certificate, or successful build closes an upstream mathematical gap.

## Genuine Round 13 improvements to retain

Round 13 is not a null revision. The following ideas should be preserved:

- **A1:** ordinary physical symplectic section, coupled natural extension, explicit impact category, engineered exponential work family, full flag intent.
- **A2:** parent-branch viewpoint, covariance damping, integrable high-frequency form, no period-one winding orbit.
- **A3:** deterministic stopped control, terminal branch counted once, retained singularity/recession data, separate physical clock.
- **A4:** weighted Wasserstein rather than impossible TV coupling, correct Poisson martingale, eigenfunction Doob normalization, instantaneous memory terms.
- **B1:** number-first extraction, separate source saddles, regular shell mass condition.
- **B2:** fixed-horizon global summation, true future, genealogy-dependent analytic exponents.
- **B3:** joint coefficient `Delta p+psi`, pure-contact diagonal, microscopic fourth-moment term, correct Cameron–Martin domain.
- **B4:** five distinct finite-volume objects, dynamic-only action, one-time preparation, consistent backward sign.
- **C1:** joint Rokhlin posterior kernel, current/probability separation, growing coordinate order, informative-strategy restriction.
- **C2:** exact invariant-integral distinction, full perturbation functional, separated source/state derivatives.
- **D1:** positive measurable basins, explicit boundary label, normalized conditional pressures.

The reports reject the theorem packages, not every local design choice.

## Recommended reconstruction order

1. Replace A1's refinement-infimum seminorm and honestly type the impact/work extension.
2. Correct A2's four-dimensional LLT and prove the common anisotropic/UNI theorem in full.
3. Define A3's stopped state and terminal/recession cost precisely, then prove the controlled Γ-limit including mesoscopic excursions.
4. Put A4 on an integrable multiplier algebra and factor memory only after pole-zero cancellation.
5. Prove B2-GC's trace and physical Jacobi theorems, then a genuine dense exposed lower bound.
6. Prove B1's canonical exact-number cluster theorem with a global `N`-dependent integrable Fourier tail.
7. Transfer B2-MC only after B1 is valid.
8. Rebuild B3 tightness on a correctly chosen filtration.
9. Separate B4's ensemble/hierarchy nonlinear generator from the deterministic Koopman derivation and prove a genuine Nisio verification theorem.
10. Give C1 one consistent zero-evidence topology and a dimension-controlled finite-coordinate approximation with kernel Lipschitz estimates.
11. Separate C2's strict Radon dual topology from its stronger spectral/form spaces and construct one positive common form domain.
12. Remove D1 as a standalone paper until a platform proves genuine component LDPs; combine nonlinear phase values by log-sum-exp.

## Final recommendation

**Reject all eleven manuscripts in their present form.**  
**D1 should be removed as a standalone submission.**
