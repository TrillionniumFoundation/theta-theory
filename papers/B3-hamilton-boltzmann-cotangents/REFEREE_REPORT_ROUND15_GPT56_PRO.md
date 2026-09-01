# Independent Referee Report — Round 15

**Manuscript:** B3 — *Hamilton–Boltzmann Cotangents*  
**Submitted revision branch:** `revision/round15-referee-positive-closure-11paper-2026-09-01`  
**Locked branch commit:** `e25e565cc15ae65693c87eda37fd3a1f29357ecd`  
**Locked tree:** `d3c54fc19f0881ce3d38253f62ca3215fbf5000c`  
**Actual controlling module at review lock:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**

## Evidence and submission integrity

No Round-Fifteen B3 source is present or recoverable from the submitted branch; the paper still loads Round Fourteen. The report therefore addresses the controlling manuscript.

## Executive assessment

The manuscript now uses the correct joint collision coefficient \(\Delta p+\psi\), includes pure-contact variance, retains the microscopic diagonal term in deterministic-interval moments, and places the Cameron–Martin form on \(\operatorname{Ran}\Sigma^{1/2}\). These are genuine repairs. The Gaussian random-measure normalization is nevertheless internally inconsistent, and the process tightness and second epi-derivative do not follow from the inputs cited.

## Decisive objections

### 1. The biased intensity is counted twice

The manuscript declares an isonormal Gaussian random measure on

\[
L^2(qA_f)
\]

and then writes the collision noise as

\[
\int(\Delta p+\psi)\sqrt q\,d\mathbb W.
\]

By the Gaussian isometry its covariance is

\[
\int q^2
(\Delta p+\psi)(\Delta\widetilde p+\widetilde\psi)\,dA_f,
\]

not the displayed

\[
\int q
(\Delta p+\psi)(\Delta\widetilde p+\widetilde\psi)\,dA_f.
\]

One must either use \(\mathbb W\) with control \(A_f\) and integrand \(\sqrt q(\Delta p+\psi)\), or control \(qA_f\) and integrand \(\Delta p+\psi\). The text combines both conventions.

This changes the covariance operator, its null space, the inverse form, and every later Gaussian/risk-sensitive formula.

### 2. The finite-time observability/closed-range theorem is not proved

The manuscript claims an estimate controlling the quotient norm of \(r\) by a collision Dirichlet form plus a negative transport norm, then invokes the closed-range theorem to identify all balance coboundaries. This is a substantial hypoelliptic observability result with endpoint and trace terms. It does not follow from the Maxwellian collision gap alone.

Spatially dependent hydrodynamic modes, transport resonances, boundary traces, and the finite time horizon require a precise Gelfand triple and a proof of the claimed coercivity. The text provides only a sketch.

### 3. Deterministic-interval moments do not yet give the announced \(C\)-tightness

The multiscale-grid argument assumes uniform moment estimates for every dyadic interval and test in a determining nuclear family, plus a maximal-jump estimate. The connected-cumulant expansion is stated only on fixed smooth test families and fixed short horizon. Uniformity as the interval support shrinks to scales below \(\mu^{-1}\) is not demonstrated.

The claim that “multiple jumps in one finest cell” is controlled by a contact-count exponential moment does not bound the location-dependent supremum over all grid cells without quantitative constants.

### 4. First-order LDP recovery does not prove a second epi-derivative

A good LDP and analytic finite-dimensional pressure identify first-order convex duality. The statement

\[
d_e^2I(z)=\|\Sigma^{-1/2}z\|^2
\]

requires second-order Mosco/epi convergence: recovery sequences must have action expansion correct to quadratic order around the exposed path. B2's rate-dense first-order recovery allows errors \(o(1)\), which can be much larger than the \(O(\varepsilon^2)\) scale of the second derivative.

The proof simply says the full LDP supplies the required Mosco limsup. It does not.

### 5. Initial and dynamic Gaussian fields are not fully assembled

The prepared initial Schur complement and the collision martingale are placed side by side, but the covariance transmitted through the nonautonomous linearized equation, endpoint terms, density–contact cross covariance, and direct contact drift must be written as one continuous operator on the chosen path space. The paper supplies finite-test formulas, not a constructed process-valued covariance operator.

### 6. The biased kinetic energy estimate is a major theorem, not a perturbative paragraph

The proof invokes Maxwellian comparison, a symmetrized collision gap, hypocoercive commutators, spatially dependent moments, coefficient regularity, trace continuity, and nonautonomous well-posedness. Each requires a defined weighted space and quantitative bounds. The claimed small-source stability does not follow from formal closeness of coefficients, especially with unbounded velocities and an actual-contact trace.

### 7. All microscopic inputs depend on unresolved B1/B2 theorems

The cumulant estimates, compact containment, exact contact source, and initial conditioning are imported from B2 and B1. Both remain unproved in their controlling manuscripts. B3 cannot convert them into certified Gaussian data by differentiation.

## Required reconstruction

Correct the control-measure normalization, prove a standalone finite-time kinetic observability/closed-range theorem, and establish process tightness with explicit uniform interval estimates. Treat second epi-differentiability as a separate theorem with quadratic recovery—not as an automatic corollary of the LDP.

## Recommendation

**Reject.** The submitted revision is absent, and the controlling Gaussian driver has the wrong covariance normalization while its two hardest analytic steps are assumed.
