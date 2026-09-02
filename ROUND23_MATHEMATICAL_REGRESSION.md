# Round-Twenty-Three mathematical regression specification

This document turns the Round-Twenty-Two counterexamples into reproducible algebraic or finite-dimensional tests.  The executable implementation is `tools/verify_round23.py`; this file records the mathematical meaning of each test.  Passing these tests rules out recurrence of the exact refuted mechanisms.  It does not prove all infinite-dimensional estimates in the manuscripts.

## R1 — A1: Hilbert membership does not imply exponential cylinder approximation

Take coefficients

```text
c_n = 1/(n+1)
```

in `l2` after an additional logarithmic or polynomial normalization chosen by the executable test.  The tail tends to zero but `exp(eta N) tail_N` diverges for every fixed positive `eta`.  Therefore an exponential approximation rate must be part of the response-domain norm, not a consequence of Hilbert membership.

**Required source response:** `def:r23-a1-domain` contains the explicit conditional-expectation tail and `thm:r23-a1-response` uses it in the score series.

## R2 — A1: trace-class covariance identity

For a finite Hilbert approximation with martingale increment vector `D`, define

```text
Q = E[D tensor D].
```

Then

```text
trace(Q) = E ||D||^2.
```

The executable test checks this identity exactly on a finite distribution.  The active infinite-dimensional proof applies Tonelli and Parseval to the same formula.

## R3 — A2: closed-subgroup character elimination

The certificate has:

- exact lattice differences `e_1,e_2,e_3`;
- roof differences `beta_1=1` and `beta_2=sqrt(2)`;
- two coprime periods.

If a character satisfies both roof equations `b beta_i in 2 pi Z`, then `b=0`, because a nonzero pair of integers would make `sqrt(2)` rational.  Exact lattice generators then force each torus coordinate to zero, and coprime periods force the constant phase to zero.

The executable finite search confirms there is no nontrivial small integer relation and separately checks the Bezout period step.  This is only a regression for the logical structure; the manuscript proves the full annihilator theorem.

## R4 — A3: order is observable

For marks `A` and `B`, define chronological measures

```text
O_AB = {(0,A),(1/2,B)}
O_BA = {(0,B),(1/2,A)}.
```

They have the same unordered mark counts but different ordered measures and different concatenated paths.  The executable test asserts both facts.  This prevents replacement of the active state by an unordered transition occupation.

## R5 — A3: conditional-reference recovery has finite and reduced KL

Let a nondegenerate reference mass vector be `K=(0.1,0.2,0.3,0.4)` and a controlled mass vector `q`.  For the partition `{0,1}|{2,3}`, define

```text
q^P_i = q(C) K_i/K(C),  i in C.
```

Then

```text
KL(q^P || K) = KL(q cells || K cells) <= KL(q || K).
```

The executable test evaluates all three quantities.  The equality is the finite version of `lem:r23-a3-recovery`; it would fail or become infinite for representative atoms against a non-atomic reference.

## R6 — A4: a large remote mark can have order-one Lyapunov mass but small influence

Put a mark of size `rho^(-n)` at depth `n`.  Its contribution to

```text
sum rho^j chi(m_-j)
```

is one, while its stable influence is

```text
theta^n rho^(-n) = (theta/rho)^n -> 0
```

when `theta<rho`.  The executable test checks these two different limits.  This prevents a return to the false claim that the Lyapunov tail itself is uniformly small.

## R7 — A4: exact Schur--Feshbach identity and high-frequency coefficient

For the block matrix

```text
L = [[a,b],[c,d]],   P = first coordinate,
```

the memory transform is

```text
Khat(z) = b c /(z-d).
```

The compressed full resolvent satisfies

```text
P(z-L)^(-1)P = [z-a-bc/(z-d)]^(-1),
```

and

```text
z Khat(z) -> bc.
```

The executable test checks the exact identity at several complex `z` and the convergence of the leading coefficient.  It deliberately rejects an unconditional `O(z^-2)` claim.

## R8 — B1: factorial pressure versus normalized canonical pressure

For the empty-source ideal integral with a `1/N!` factor,

```text
-(1/N) log(N!) ~ -log N + 1,
```

which is not a finite pressure limit.  Under a normalized canonical probability, the zero-source moment generating function is exactly one and its pressure is zero.  The executable test compares both sequences.

## R9 — B1: conditional Gaussian mean and Schur covariance

For a positive block covariance

```text
Sigma = [[Sigma_ZZ,Sigma_ZR],[Sigma_RZ,Sigma_RR]],
```

conditioning on lattice deviation `z` gives

```text
mean_R|Z = Sigma_RZ Sigma_ZZ^-1 z,
Sigma_R|Z = Sigma_RR - Sigma_RZ Sigma_ZZ^-1 Sigma_ZR.
```

The executable scalar-block example checks positivity of the Schur complement and nonzero conditional shift.  This guards against replacing the mixed local theorem by an unshifted marginal Gaussian.

## R10 — B2: surplus loop produces an optimized positive power

The regular/singular split has schematic bound

```text
epsilon eta^-m + eta^kappa.
```

Choosing `eta=epsilon^(1/(m+kappa))` gives

```text
O(epsilon^(kappa/(m+kappa))).
```

The executable test verifies the exponent is positive and that the optimized expression decays with `epsilon`.  The manuscript includes the additional grazing exponent and opens independent loops successively.

## R11 — B2: factorial normalization is retained

The connected coefficient is defined with `1/k!`.  Cayley's tree count gives

```text
k^(k-2)/k! <= C e^k k^(-5/2).
```

The executable test checks this scaled ratio for a range of `k`.  It prevents a proof from defining a factorially normalized coefficient and then estimating an unnormalized graph count.

## R12 — B3: zero-cost manifold and normal defect Hessian

Let

```text
A_eta = exp(a eta) A,
Gamma_eta = A_eta.
```

Then `q_eta=Gamma_eta/A_eta=1` and `A_eta ell(q_eta)=0` identically, so the second derivative is zero for arbitrary `a`.

For a normal perturbation

```text
Gamma_eta = A_eta (1 + eta h/A),
```

the second-order coefficient is `h^2/(2A)`.  The executable test evaluates symmetric finite differences for both paths.  This is the decisive regression for `thm:r23-b3-mosco`.

## R13 — B4: escaping energy is excluded by a superquadratic moment

For

```text
f_n = (1-n^-2) phi + n^-2 phi(v-ne_1),
```

the remote component contributes order one to the second moment but order `n^delta` to the `(2+delta)` moment.  The executable test checks this divergence.  A fixed superquadratic shell therefore restores uniform integrability of energy.

## R14 — C1: no probability can dominate every uncountable Dirac transition

If a probability dominates `N` distinct Dirac masses, it must give positive mass to all `N` points, and at least one atom has mass at most `1/N`.  Taking arbitrarily large finite subsets rules out any uniform positive atom bound; an uncountable family would require uncountably many positive atoms and cannot be dominated in the required absolute-continuity sense.

The executable finite test checks the `1/N` obstruction.  The active theorem avoids the premise entirely and dominates only observations.

## R15 — C1: integrated posterior ratio remains stable at small evidence

For evidence/numerator pairs `(r_n,N_n)` and `(r,N)`, with bounded test value `M`,

```text
r_n |N_n/r_n - N/r| <= |N_n-N| + M |r_n-r|,
```

using zero conventions where a denominator vanishes.  The executable test samples small positive and zero evidences.  This is the finite algebra behind `thm:r23-c1-filter`.

## R16 — C1: compactness of actions does not imply information

An action whose observation law is parameter-independent has score zero and Fisher information zero.  The executable test computes this Bernoulli example.  The active LAN/BvM theorem therefore restricts to the explicit persistent-excitation class.

## R17 — C2: weighted strict dual transformation

For a finite model, multiplication of a signed measure `mu` by `W` produces the finite measure `nu=W mu`, and

```text
sum f mu = sum (f/W) nu,
sum W |mu| = sum |nu|.
```

The executable test verifies the exact isometry.  The infinite-dimensional theorem is obtained by the same linear homeomorphism from the standard strict topology.

## R18 — C2: a finite continuous Brownian exponential cannot hit zero

For finite real `x`, `exp(x)>0`.  A Doléans exponential of a continuous Brownian integral with finite quadratic variation is therefore strictly positive.  The executable test samples finite exponents and checks positivity.  The active likelihood theorem assumes finite-horizon equivalence and reciprocal moments; a nonnegative martingale that hits zero is outside its scope.

## R19 — D1: polynomial phase weights are independent data

When two phases have equal exponential cost but exponents `kappa_1<kappa_2`,

```text
w_2/w_1 = (c_2/c_1) N^(-(kappa_2-kappa_1)) -> 0.
```

The executable test verifies this limit.  An LDP sees only the equal exponential costs and cannot decide the winner.

## R20 — D1: one common policy is not a sum of phasewise optima

For two phases with action payoffs arranged in the matrix

```text
          action 0  action 1
phase 0      1         0
phase 1      0         1
```

an unobserved shared action has mixture value `1/2`, whereas separately optimizing each phase yields `1`.  The executable test checks the strict inequality.  The active Bellman recursion fixes one common action before phase aggregation.

## Source-structure regressions

In addition to the numerical tests, the verifier requires:

- each wrapper to import exactly `ROUND23_POSITIVE_CLOSURE.tex`;
- every paper to identify `ROUND23-REFEREE-POSITIVE-CLOSURE`;
- every required theorem label from the dependency ledger;
- balanced theorem/proof and display environments;
- no placeholder tokens;
- no unresolved citation keys across `references.bib` and optional `ROUND23_REFERENCES.bib`;
- absence of known superseded formula patterns;
- an acyclic dependency graph;
- preservation of the inherited Round-Twenty-Two report.

## Interpretation

A PASS means that the active sources are internally coherent at the level tested, compile against closed bibliographies, respect the declared dependency order, and do not reproduce the referee's finite counterexamples.  It is deliberately weaker than a new external referee verdict and is labelled as such in every build record.
