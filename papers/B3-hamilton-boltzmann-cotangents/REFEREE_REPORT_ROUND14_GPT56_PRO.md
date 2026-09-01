# Independent Referee Report — Round 14

**Manuscript:** B3 — *Hamilton–Boltzmann Cotangents*  
**Reviewed branch:** `revision/round14-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `dd9dbcb891076b7dbfe388bd8543d8342ba103c0`  
**Reviewed tree:** `c4492f8891e065201af70e68e6764ff5975f2137`  
**Controlling module:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `8e650ebe798321e276d6a73f0b40ba6de197066ca1f132384559f7ad51adeb41`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 14 correctly recognizes that the primitive collision coefficient is `Delta p + psi`, retains pure-contact noise, keeps the microscopic diagonal term in interval moments, and avoids conditioning a Poisson estimate on the complete deterministic microstate. These are real improvements.

The new Gaussian theorem is nevertheless internally inconsistent. The isonormal random measure is assigned control measure `q A_f` and the integrand is then multiplied by `sqrt(q)`, producing covariance `q^2 A_f` rather than the displayed `q A_f`. The closed-gauge theorem is assumed through an unproved observability inequality, the deterministic-grid argument does not establish the declared infinite-dimensional `C`-tightness, and first-order LDP recovery does not imply a second epi-derivative.

## Decisive objections

### 1. The isonormal representation has the wrong covariance

The paper says that `W` is an isonormal Gaussian random measure on

\[
L^2(qA_f)
\]

and then defines

\[
M_t(p,\psi)
=
\int (\Delta p+\psi)\sqrt q\,d\mathbb W.
\]

If the control measure of `W` is `q A_f`, the Gaussian isometry gives

\[
\operatorname{Cov}(M(p,\psi),M(\tilde p,\tilde\psi))
=
\int q^2(\Delta p+\psi)(\Delta\tilde p+\tilde\psi)\,dA_f,
\]

not the theorem's

\[
\int q(\Delta p+\psi)(\Delta\tilde p+\tilde\psi)\,dA_f.
\]

There are two correct conventions:

- take `W` isonormal on `L2(A_f)` and integrate `sqrt(q)(Delta p+psi)`; or
- take `W` isonormal on `L2(qA_f)` and integrate `Delta p+psi`.

The manuscript combines both and double-counts `q`. This affects the driving martingale, the density/contact cross-covariance, the kernel, and the Cameron–Martin form.

### 2. The closed-range/observability theorem is not proved

The claimed estimate

\[
\int|\Delta r|^2dA_f
+\|(\partial_t+v\cdot\nabla_x)r\|_{-1,w}^2
\ge c\|r\|_{\mathcal Y_p/\mathcal I}^2
\]

is precisely a finite-time kinetic observability theorem. It does not follow merely by “solving the backward transport equation” and invoking the Maxwellian collision gap.

Spatially varying hydrodynamic modes, endpoint traces, transport resonances, and the choice of negative norm all matter. The paper does not define the quotient norm, prove a Poincaré/observability inequality for the macroscopic fields, or show uniform closed range under the nonautonomous biased coefficients.

Consequently the asserted equality between the covariance kernel and the complete balance-coboundary space is unsupported.

### 3. The perturbative energy theorem is a program, not an estimate

The proof names a hypocoercive multiplier and says the five local moments satisfy an exact hyperbolic balance. It does not display the energy, commutator bounds, boundary terms, coefficient regularity, or closure of the normal trace. In particular, the source chart is claimed to imply two-sided Maxwellian bounds for `f` and bounded pre/post ratios `q,q*`; B2 has not proved this for every exposed path.

A top-journal theorem requires the full nonautonomous estimate, not a list of standard ingredients.

### 4. Cumulant convergence is not established by the cited B2 result

The proof uses normal convergence of all joint source derivatives to claim that every centered cumulant of order at least three is

\[
O(\mu^{1-k/2}).
\]

B2's Round 14 theorem has not established a uniform complex source expansion after recollision removal. Even if local derivatives converge at deterministic times, a process-level cumulant estimate uniform over time-supported sources and shrinking intervals is a stronger result.

### 5. The deterministic interval estimate does not by itself prove `C`-tightness

The dyadic argument controls increments on selected grid cells. To obtain a modulus over all times one needs a chaining argument controlling arbitrary subintervals and the oscillation inside each finest cell. The proof replaces the latter by “the maximal jump is `O(mu^{-1/2})`” and an exponential contact-count bound, but density transport also has continuous variation and multiple contact increments can accumulate inside a cell.

No quantitative bound is given for the supremum over all subintervals below the grid scale. The claim of `C`-tightness in a weighted distribution path space additionally requires a specified nuclear test space and compact-containment estimate for Mitoma's theorem.

### 6. The interval cumulant density assertion is not proved for deterministic hard spheres

The statement that a connected cumulant with `j` distinct collision times has an `L1` density on `I^j` is a nontrivial consequence of the real-trajectory expansion, including singular collision times and recollisions. It is not established by merely inserting a time-supported source. This density and its uniform norm are exactly what produces the powers `h^j`.

### 7. Finite-dimensional Gaussianity does not identify the claimed stochastic evolution

The pressure Hessian determines covariance of tested path observables. To identify a unique nonautonomous linearized Boltzmann martingale problem one must prove that the covariance satisfies the evolution equation, that the stochastic convolution is well posed in the selected distribution space, and that the contact field has the stated drift response. These steps are asserted after the covariance calculation.

### 8. First-order LDP recovery does not imply a second epi-derivative

The theorem claims

\[
d_e^2 I(z)=\|\Sigma^{-1/2}z\|^2.
\]

An analytic Hessian for every finite projection gives finite-dimensional quadratic tangents. Passing to an infinite-dimensional second epi-derivative requires a second-order recovery theorem at scale `t^2`, equicoercivity of the rescaled actions, and Mosco convergence. B2's ordinary LDP lower recovery controls only the leading action, not its quadratic remainder.

The sentence “B2's full LDP supplies the finite-rate recovery needed for Mosco limsup” is false as a matter of order: first-order rate recovery is not second-order epi-recovery.

### 9. The dual and primal quotient identifications remain incomplete

The manuscript defines the dual source quotient by `ker Sigma` and the primal form on `Ran Sigma^(1/2)`, which is the correct abstract distinction. But the asserted concrete characterization of `ker Sigma` depends on the unproved closed-range theorem, and the covariance operator itself is not constructed on a specified Hilbert/Gelfand pairing. Thus the abstract spectral-theorem formula has no completed model-specific domain.

## Dependency assessment

B3 depends on B2's unproved marked pressure/LDP and B1's unproved coefficient theorem. B4 cannot use its Gaussian process or inverse form, and C1/C2 cannot use its score, likelihood, or cotangent kernel as certified inputs.

## Required reconstruction

A viable paper should:

1. correct the Gaussian control-measure convention;
2. prove a complete nonautonomous kinetic energy/observability theorem;
3. derive time-local cumulant density bounds from the microscopic expansion;
4. establish process tightness on a precise test-function space; and
5. prove second-order Mosco convergence separately from the first-order LDP.

## Recommendation

**Reject.** The joint contact coefficient is finally typed correctly, but the Gaussian driver is normalized incorrectly and every infinite-dimensional identification rests on unproved analytic interfaces.