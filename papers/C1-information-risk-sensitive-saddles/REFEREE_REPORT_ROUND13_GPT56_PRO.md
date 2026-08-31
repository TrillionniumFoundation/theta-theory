# Independent Referee Report — Round 13

**Manuscript:** C1 — *Information and Risk-Sensitive Saddles*  
**Reviewed branch:** `revision/round13-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `5c8b71e67d62d4a63c53a5a59e7a10f1ccc0f688`  
**Reviewed tree:** `586de2e3cf8c547ca3cbfbc0cb0daba2fd05af59`  
**Controlling module:** `ROUND13_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `3e1ca3f3abba735f84b9c84d1a3a2b40cb0cb1af2e92c643854a9b503bf71c04`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 13 correctly separates positive posterior measures from oriented currents, formulates observations through a joint Rokhlin kernel rather than a pointwise version of the conditional law, and abandons the claim that a fixed finite moment list is sufficient. These are substantial conceptual repairs.

The replacement zero-evidence state is internally contradictory and the proposed continuous lift is false without a strong analytic asymptotic hypothesis. The displayed quotient represents a positive measure `r pi`, which identifies all pairs `(0,pi)`, while the text simultaneously says that the direction `pi` is retained. Even if one uses the real blow-up instead of the quotient, positive unnormalized measures can approach zero faster than every power while their normalized directions oscillate. There is then no first nonzero coefficient and no continuous boundary direction. The growing-moment theorem is also not typed for the infinite-dimensional microscopic state, and the reduced DPP uses a Lipschitz property that the Feller theorem does not provide.

## Decisive objections

### 1. The zero-evidence state identifies and retains the same direction simultaneously

The manuscript defines

\[
 \widehat{\mathfrak B}_M
 =\{(r,\pi):0\le r\le1,\ \pi\in\mathcal K_M\}/\sim,
\]

and says that `(r,pi)` represents the positive measure `r pi`. Under that representation,

\[
 0\cdot\pi=0\cdot\widetilde\pi
\]

for every pair of directions, so all points with `r=0` belong to one equivalence class. The next sentence says that the direction `pi` is retained at `r=0`.

These are different spaces:

- the cone quotient collapses the zero fiber; and
- the real oriented blow-up keeps the entire zero fiber.

The equivalence relation is not defined, and no topology can both identify all zero measures and distinguish their directions. The Feller kernel therefore has no stated state space.

### 2. A continuous zero-evidence direction need not exist

The proof assumes an expansion

\[
 \Lambda_r=r^kG+o(r^k)
\]

and normalizes the first nonzero positive coefficient. The hypotheses provide only `C^2` observation maps and Sobolev density bounds; they do not give a polyhomogeneous or analytic expansion in the evidence radius.

A direct counterexample is a family of positive finite measures

\[
 \Lambda_t=e^{-1/t^2}
 \left[
 \left(1+\tfrac12\sin(1/t)\right)\delta_0+
 \left(1-\tfrac12\sin(1/t)\right)\delta_1
 \right],\qquad t>0.
\]

Its total mass tends to zero faster than every power, so every Taylor coefficient at zero vanishes. Yet the normalized direction

\[
 {\Lambda_t\over\Lambda_t(X)}
\]

oscillates and has no unique limit. The family can be embedded into a smooth flat density family if atomic measures are excluded.

Thus neither “normalize the first nonzero coefficient” nor “if all coefficients vanish, use the predicted direction” gives a boundary value independent of the approximating positive-evidence sequence.

### 3. Joint weak continuity of observation/posterior laws is not proved by weak convergence of priors

Disintegration is generally unstable under weak convergence. Uniform submersion and Sobolev assumptions can yield stability, but one must state a common reference chart, trace regularity, compact embedding, and convergence of the densities strong enough to pass conditional laws.

The proof says that weak convergence plus uniform Sobolev bounds gives convergence of a determining algebra. Uniform bounds alone give subsequential compactness, not identification of the limit with the disintegration of the weak limit. Boundary strata and moving observation maps make this more delicate.

The theorem is therefore a significant analytic assertion, not a consequence of coarea in one paragraph.

### 4. The quantitative moment lemma is not typed for the declared state space

`M_K(pi)` is said to contain all mixed moments of a fixed **countable** separating observable family. The proof then invokes multivariate Bernstein polynomials with an error `C R/K` and a fixed dimension `d`.

There is no finite-dimensional cube on which this Bernstein estimate is being applied. If the first `d_K` observables are retained, the approximation constants and the number of coefficients depend strongly on `d_K`; no dimension-free `CR/K` bound holds. If all countably many observables are used, the collection of mixed monomials of degree at most `K` is infinite and is not a finite reduced coordinate.

The phrase “normalized coordinates differing by `o(K^{-d})`” is likewise undefined until the dimension, coefficient norm, and growth in the number of monomials are specified.

### 5. Moment closeness does not automatically produce a Markov reduced state

Even if a growing list of moments determines each belief asymptotically, the reduced coordinate must carry a well-defined approximate transition kernel. Two beliefs with nearby moment vectors can have conditional observation kernels that differ greatly near low-evidence fibers unless the full prediction–observation map is quantitatively Lipschitz in the chosen metric.

The proof couples a step through a “common microscopic law” without constructing a common coupling of two different posterior beliefs or controls. Moment approximation of static measures is not a transition-kernel stability theorem.

### 6. Feller continuity does not imply the Bellman Lipschitz estimate used in the reduction

The exact DPP theorem claims only that the controlled kernel is Feller. The reduction proof then says that the Feller kernel makes the Bellman operator Lipschitz in weighted Wasserstein distance. A Feller kernel maps continuous functions to continuous functions; it need not have any Lipschitz modulus.

To sum one-step errors over `J_epsilon` stages, the authors need a uniform Wasserstein contraction or Lipschitz bound for every admissible control and observation update. None is stated or proved.

### 7. The inserted coefficient theorem inherits the unresolved B1 theorem

The ratio theorem relies on B1's exact-number high-frequency estimate. That estimate has a nonvanishing fixed-exponent tail and does not prove an `o(N^{-1/2})` Fourier remainder. Consequently the denominator coefficient and uniform posterior ratio are not available.

Separate numerator and denominator saddles may also move under a posterior insertion; the statement that the insertion changes only the analytic amplitude requires a precise central-insertion condition.

### 8. The controlled Bernstein–von Mises theorem is largely assumed

A predictable information lower bound is not sufficient for adaptive BvM. One also needs uniform local asymptotic normality under the random strategy, contiguity, posterior tightness, control of nuisance/phase coordinates, and a theorem excluding adaptive selection bias. These are asserted through references to B1/B3, neither of which proves the required conditional likelihood result.

## Genuine improvements recognized

The full-belief state, joint observation/posterior kernel, positive measure/current separation, growing rather than fixed moments, separate shell saddles, and informative-strategy restriction are the correct directions.

## Dependency assessment

C1 is downstream of B1–B4. The exact-number coefficient, actual-contact LDP, Gaussian process, and kinetic semigroup are all unproved. C1 cannot serve as a closed filtering/control interface for D1.

## Required reconstruction

A viable paper should first choose one honest zero-evidence topology—either a collapsed cone or an oriented blow-up—and impose hypotheses that guarantee a unique boundary direction. It should then prove quantitative Lipschitz stability of the complete observation kernel. Any finite-coordinate reduction must specify a finite-dimensional approximation scheme whose dimension-dependent constants are controlled as the scale grows.

## Recommendation

**Reject.** The revision identifies the right information-state issues, but the zero-evidence compactification is self-contradictory, the continuous boundary direction has a flat-family counterexample, and the moment/DPP reduction is not mathematically typed or proved.
