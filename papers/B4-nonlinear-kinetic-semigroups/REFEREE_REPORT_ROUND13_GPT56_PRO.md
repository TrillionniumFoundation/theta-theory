# Independent Referee Report — Round 13

**Manuscript:** B4 — *Nonlinear Kinetic Semigroups*  
**Reviewed branch:** `revision/round13-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `5c8b71e67d62d4a63c53a5a59e7a10f1ccc0f688`  
**Reviewed tree:** `586de2e3cf8c547ca3cbfbc0cb0daba2fd05af59`  
**Controlling module:** `ROUND13_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `03defccc4e6034c8895f8ab340618a4c55676e68841b7d1c410ba1291edea3b4`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 13 correctly distinguishes microscopic states, Koopman observables, pushed-forward laws, ensemble log-Laplace values, and the limiting action semigroup. It also abandons the failed doubled-variable exponential-jet comparison and uses a consistent backward value convention. These are important repairs.

The central generator theorem nevertheless mixes the objects again. The generator `A_epsilon` was defined as the Koopman generator of a deterministic flow. Such a generator is a derivation. Therefore its exponential conjugate is exactly linear:

\[
 {1\over\mu}e^{-\mu F}A(e^{\mu F})=AF.
\]

It cannot produce the jump Hamiltonian `integral (e^{Delta p+psi}-1)dA_f`. The proof silently replaces the Koopman generator by a BBGKY/correlation-hierarchy generator, which is a different operator on a different space. The proposed Nisio “resolvent” is also not shown to solve the nonlinear resolvent equation, so the asserted m-dissipativity and viscosity uniqueness are circular.

## Decisive objections

### 1. A deterministic Koopman generator cannot yield the exponential collision Hamiltonian

For a deterministic flow `Phi_t`, the Koopman generator satisfies the Leibniz and chain rules on its algebraic domain. If `F` and `e^{mu F}` belong to that domain, then

\[
 A_\varepsilon(e^{\mu_\varepsilon F})
 =\mu_\varepsilon e^{\mu_\varepsilon F}
   A_\varepsilon F.
\]

Consequently

\[
 {1\over\mu_\varepsilon}
 e^{-\mu_\varepsilon F}
 A_\varepsilon e^{\mu_\varepsilon F}
 =A_\varepsilon F
\]

exactly, at every finite volume. There is no term

\[
 \int(e^{\Delta p+\psi}-1)dA_f.
\]

A deterministic impact does not change this conclusion. If observables satisfy the impact matching condition and lie in the Koopman generator domain, the chain rule holds through the deterministic trajectory. If they jump across the impact, they are not in that generator domain.

The exponential Boltzmann Hamiltonian arises from an ensemble cumulant or a stochastic/branching hierarchy generator, not from pointwise exponential conjugation of the physical Koopman derivation.

### 2. The proof switches to a different generator without defining an intertwining map

The theorem uses `A_epsilon`, previously defined on microscopic observables. Its proof then speaks of the “full BBGKY/contact ledger generator” acting on factorial correlation sequences. That hierarchy generator is not the Koopman generator on `mathcal X_epsilon`; it acts on a different sequence space and is not a derivation.

To transfer a hierarchy corrector back to one microscopic observable, the authors need an explicit generating-functional map, domain theorem, and intertwining identity. None is given. The displayed convergence is therefore ill-typed even before the upstream B2 estimates are considered.

### 3. The normally summable corrector estimate omits the Boltzmann–Grad scaling of each level

Cancelling `j!` by the sequence weight leaves a geometric factor only if the order-`j` term also carries the correct power of `mu_epsilon` and the loss of label radius is uniform in the generator graph norm. The proof writes

\[
 j!C^jT^{j-1}
\]

and invokes `1/j!`, but it does not specify the finite-volume coefficient multiplying level `j`, the norm of the reconstruction into a microscopic observable, or the generator-domain compatibility of the infinite sum.

Normal convergence in an abstract hierarchy norm does not imply that the sum is an element of the physical Koopman graph domain.

### 4. The proposed `J_lambda` is not shown to be the nonlinear resolvent

The manuscript defines

\[
 (J_\lambda G)(f)=
 \sup_{(\rho,\Gamma)}
 \left\{G(\rho_\lambda)-I_{0,\lambda}^{\rm dyn}
 -{1\over\lambda}d(f,\rho_0)^2\right\}.
\]

This is a finite-horizon sup-convolution with a penalty on the **initial** point. It is not automatically the implicit resolvent solving

\[
 u-\lambda\overline H u=G.
\]

Concatenation of the dynamic action gives a semigroup property for `S_{s,t}`; it does not give the Crandall–Liggett resolvent identity for the displayed `J_lambda`. The proof never verifies the resolvent equation, the range condition, or dissipativity of `overline H`.

The sentence “the range is all bounded uniformly continuous data by the resolvent construction” assumes exactly what must be proved.

### 5. Metric-viscosity uniqueness is not a consequence of semigroup existence alone

A Nisio semigroup defined by a good control action can exist without every metric-viscosity solution of a formally associated Hamilton–Jacobi equation being unique. One must specify the test-function class, tangent/cotangent pairing, relaxed Hamiltonians, and comparison theorem.

The manuscript says that resolvent tests yield one-step domination, but no test theorem connecting the variational `J_lambda` to the viscosity definition is supplied. Thus the equivalence between mild, semigroup, and viscosity solutions remains unproved.

### 6. The action compactness theorem is inherited from an unproved B2 LDP

The proof cites B2 for velocity moments, contact entropy, temporal moduli, closed endpoints, and compact action sublevels. B2 has not proved its trace graph, recollision transversality, or full lower bound. These properties cannot be imported as established facts.

### 7. The finite-volume endpoint value does not itself form the claimed kinetic tower

The exact finite-volume statement is only the Koopman composition inside one initial-law integral. There is no autonomous value map on empirical densities before the limit. Passing from that identity to local uniform convergence of an infinite-dimensional kinetic semigroup requires the full Laplace principle and comparison theorem; the generator corrector cannot substitute for them.

### 8. The Gaussian risk-sensitive tangent remains conditional

The last theorem assumes B3 process convergence and a uniform complex moment neighborhood. B3's stopping-time tightness estimate is false on the microscopic filtration. Even with a valid Gaussian limit, the numerical risk coefficient remains an external exponential-transform parameter unless a separate preference/calibration axiom is imposed.

## Genuine improvements recognized

The five-way typing, dynamic-only action, one-time preparation charge, consistent backward sign, and attempt to use a Nisio action rather than an uncontrolled doubled jet are all correct directions.

## Dependency assessment

B4 cannot close B2 or B3: its action and covariance are downstream of those papers. C1, C2, and D1 may not cite B4 as an established kinetic semigroup or comparison theorem while the generator and resolvent interfaces remain invalid.

## Required reconstruction

The authors must choose one finite-volume object. A viable route is to formulate the nonlinear generator directly for ensemble log-Laplace functionals or the factorial hierarchy, prove an explicit intertwining with empirical observables, and keep it separate from the Koopman derivation. The Nisio value can then be studied through a genuine control verification/comparison theorem without calling an unverified sup-convolution a nonlinear resolvent.

## Recommendation

**Reject.** Round 13 fixes the vocabulary but not the main operator identity. The physical Koopman generator is a derivation and cannot produce the advertised exponential collision Hamiltonian; the hierarchy substitution and m-dissipative resolvent argument are unproved.
