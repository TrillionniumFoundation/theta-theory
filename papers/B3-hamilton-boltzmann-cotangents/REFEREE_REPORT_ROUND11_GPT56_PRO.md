# Independent Referee Report — Round Eleven

**Manuscript:** B3 — Hamilton–Boltzmann Cotangents  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**  
**Reviewed branch:** `revision/round11-referee-positive-closure-11paper-2026-08-31@e81cbf57624d21be23ee9d982a1255c076363761`  
**Reviewed source:** `revision/round11-referee-final/B3_DYNAMIC_COHOMOLOGY_CAMERON_MARTIN.tex` (Git blob `53795a7c69901e56fa12a452e2a123f101e824ce`)

## Executive assessment

Round eleven correctly places the inverse covariance on \(\operatorname{Ran}\Sigma^{1/2}\) and no longer invents curvature from a linear KKT multiplier. The paper nevertheless assumes an unproved non-equilibrium collision gap, invokes a nonexistent hard-sphere Livšic theorem, and states a fourth-moment estimate that is false even for a Poisson collision counter. It also confuses the cotangent nullspace of covariance with the primal nullspace of the Cameron–Martin inverse form.

## Major mathematical objections

### 1. The biased collision spectral gap is assumed

Comparability of \(f\) to a local Maxwellian and bounds \(q_-\le q\le q_+\) do not by themselves give a symmetric Dirichlet form comparable to the equilibrium linearized Boltzmann operator. A driven collision ratio generally breaks detailed balance. The manuscript must identify the symmetric part, its measure, its nullspace, and prove a uniform coercivity estimate.

The statement that these conditions are “verified on compact source charts” refers back to B2, which proves no such theorem.

### 2. Fourier hypocoercivity is not valid for variable coefficients by declaration

The exposed path \(f(t,x,v)\) and collision ratio \(q(t,x,v,v_*,\omega)\) are spatially and temporally dependent. Fourier transform in \(x\) does not diagonalize a variable-coefficient collision operator. Mode-by-mode equilibrium hypocoercivity cannot simply be quoted. Commutators, coefficient derivatives, endpoint terms, and the weighted trace graph require a genuine nonautonomous estimate.

### 3. The claimed “five local conservation fields” are not a kernel

The collision invariants span five velocity modes, but spatially dependent coefficients of those modes are transported and coupled. Only the global conserved quantities are null directions after the full transport equation and boundary/initial conditions are imposed. The theorem's quotient and energy estimate do not specify the actual macroscopic system or its constraints.

### 4. There is no Livšic theorem supplied by the B2 pressure

After solving an adjoint balance equation, the proof claims that every remaining zero-variance additive source is a temporal coboundary by a “regular-phase Livšic theorem obtained from the B2 local source pressure.” B2 concerns a short-time hard-sphere/Boltzmann–Grad pressure, not a compact hyperbolic map with periodic-orbit Livšic theory.

For a Markov or kinetic process, zero asymptotic variance may correspond to an \(L^2\) Poisson coboundary under additional closed-range assumptions; it does not imply membership in the source-norm closure of pathwise temporal coboundaries without a separate theorem.

### 5. The fourth-moment estimate is false at microscopic time scales

For a rate-\(\mu\) Poisson contact counter,

\[
Z_h=\frac{N_h-\mu h}{\sqrt\mu}
\]

satisfies

\[
\mathbb E Z_h^4=3h^2+\frac{h}{\mu}.
\]

Thus no constant independent of \(\mu\) can give

\[
\mathbb E|Z_t-Z_s|^4\le C|t-s|^2
\]

for all deterministic intervals: take \(h\ll1/\mu\). Actual contact fields have the same diagonal jump contribution. The previous revision included such a term; round eleven incorrectly deletes it.

Consequently Kolmogorov's criterion cannot be applied as written. One needs Aldous tightness plus control of vanishing jump sizes, or a bound containing \(\mu^{-1}|t-s|\).

### 6. The covariance and inverse-form nullspaces are conflated

The dynamic cohomology/gauge lies in the *dual source* kernel of covariance. The Cameron–Martin form

\[
\mathfrak q(z)=\|\Sigma^{-1/2}z\|^2,
\qquad z\in\operatorname{Ran}\Sigma^{1/2},
\]

is a primal form and has no nonzero zero vector on its domain after quotienting the covariance kernel. Saying that its nullspace “is exactly the dynamic cohomology quotient” is ill-typed: a quotient space is not a subspace of the primal tangent domain.

### 7. Projective finite-dimensional conjugacy does not give infinite-dimensional Mosco equicoercivity

Finite covariance matrices may develop arbitrarily small eigenvalues as the projection grows. The energy estimate for smooth balanced paths does not provide a uniform lower bound on all new test directions. The claimed equicoercivity and diagonal recovery therefore require proof.

### 8. The process CLT remains downstream of B2

The time-localized cumulant density, cross-contact diagonals, compact containment, and closed balance passage all depend on the unproved B2 marked expansion. Finite-dimensional derivative convergence alone does not establish a process limit.

## Status of earlier objections

The correct square-root covariance domain and the rejection of fictitious KKT curvature are important repairs. The hypocoercive, cohomological, and process-tightness theorems remain invalid or unproved.

## Minimum reconstruction

The paper must first prove a nonautonomous biased collision energy theorem and state the exact macroscopic constraints. It then needs a properly typed dual kernel theorem, a tightness estimate retaining the microscopic diagonal term, and a separate Mosco theorem on a specified Hilbert/Gelfand triple.

## Recommendation

**Reject.** The corrected formal covariance geometry is not supported by the required kinetic analysis, and one headline tightness estimate has an explicit elementary counterexample.