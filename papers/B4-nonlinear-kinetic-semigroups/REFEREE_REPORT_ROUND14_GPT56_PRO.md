# Independent Referee Report — Round 14

**Manuscript:** B4 — *Nonlinear Kinetic Semigroups*  
**Reviewed branch:** `revision/round14-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `dd9dbcb891076b7dbfe388bd8543d8342ba103c0`  
**Reviewed tree:** `c4492f8891e065201af70e68e6764ff5975f2137`  
**Controlling module:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `ff0fbd4ae633e2ba7d76c9520d316692d59e43eed4307becb3e3684199a7b20f`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 14 correctly distinguishes the deterministic Koopman derivation from the ensemble boundary jump that can produce an exponential collision term. It also keeps the initial preparation cost outside the transition action and abandons the earlier uncontrolled doubled-variable jet.

The replacement Nisio/resolvent theorem is still not correct. The discounted control formula omits the initial-state constraint, so as written it is independent of its argument. The comparison proof uses a map with Lipschitz constant exactly one after multiplication by `lambda`; subtracting a constant shifts both sides equally and creates no strict inequality. The hierarchy corrector and ensemble-to-kinetic convergence are also stated without a defined intertwining map on the nonlinear exponential observables.

## Decisive objections

### 1. The discounted resolvent omits its initial condition

The manuscript defines

\[
(J_\lambda h)(f)
=
\sup_{(f_\cdot,\Gamma)}
\int_0^\infty e^{-\lambda t}
[h(f_t)-\ell(d\Gamma/dA_f)]dt.
\]

No condition `f_0=f` appears in the formula. Consequently the supremum is the same for every input `f`, so `J_lambda h` is a constant function and cannot be a resolvent of a state-dependent Hamiltonian.

The missing constraint may have been intended, but it is indispensable and must be included in the theorem, topology, admissible-control class, and dynamic-programming proof.

### 2. The comparison argument has no strict contraction

The theorem gives

\[
\|J_\lambda h-J_\lambda k\|_\infty
\le\lambda^{-1}\|h-k\|_\infty.
\]

Applied to `h+lambda u` and `h+lambda v`, this yields Lipschitz constant exactly one:

\[
\|J_\lambda(h+\lambda u)-J_\lambda(h+\lambda v)\|_\infty
\le\|u-v\|_\infty.
\]

Hence the displayed comparison chain only proves

\[
\|(u-v)^+\|\le\|(u-v)^+\|,
\]

which contains no information.

The proposed strict perturbation does not help. Discounted control has the cash rule

\[
J_\lambda(g+c)=J_\lambda(g)+{c\over\lambda}.
\]

Therefore, for `u_eta=u-eta`,

\[
J_\lambda(h+\lambda u_\eta)
=J_\lambda(h+\lambda u)-\eta.
\]

Both sides of the subsolution inequality shift by exactly `eta`; no `eta/lambda` improvement is created. The proof's claimed strict margin is false.

### 3. The Nisio resolvent is not shown to satisfy an `m`-dissipative range theorem

Even after adding `f_0=f`, a discounted infinite-horizon value is not automatically the nonlinear resolvent needed for Crandall–Liggett theory. The paper must specify the Banach space, prove the resolvent identity, show the range condition for every datum, identify the closed generator, and establish consistency between the discount parameter and the semigroup time step.

The proof cites dynamic programming and Fenchel duality but gives no range/surjectivity or closedness theorem.

### 4. The finite-volume boundary identity does not yet include the full contact source

The Green identity is written for a functional `F(pi)` of the empirical density only. It produces the factor `e^{Delta p}-1`. The later Hamiltonian contains an independent actual-contact source `psi`.

To obtain `e^{Delta p+psi}-1`, one must augment the microscopic state by the accumulated contact measure and include its jump in the exponential observable. That extension, its boundary trace, and its domain are not stated in the theorem.

### 5. The law–hierarchy intertwiner is only formal

The paper writes

\[
\mathcal I_\varepsilon F(g)
=
\sum_j{1\over j!}\langle f_j[F],g_j\rangle
\]

for a “polynomial law cylinder,” but does not define the coefficients, the domain of the map, or its inverse/reconstruction on exponential observables. Absolute convergence does not follow from `1/j!` alone; it requires compatible factorial-moment growth and a label radius.

The later corrector is added to a kinetic functional as a sum of `j`-particle hierarchy terms. Without a precise generating-functional intertwiner, these objects do not live in one microscopic observable space.

### 6. The corrector estimate does not prove convergence of the nonlinear generator

The defects are bounded by

\[
\|D_j^\varepsilon[F]\|\le j!C^jT^{j-1},
\]

and multiplied by `mu^(1-j)`. The proof asserts normal convergence of correctors, generator images, and time derivatives, but does not construct the triangular operator domains or establish uniform resolvent estimates at every hierarchy level.

More importantly, a convergent series of linear correctors does not by itself justify exponentiating `F_epsilon`, applying the ensemble boundary generator, and passing the exponential collision nonlinearity through the infinite sum.

### 7. The action compactness and infinite-horizon finiteness are imported from B2

The Nisio theorem assumes compact action sublevels, temporal moduli, endpoint closure, and entropy coercivity. Round 14 B2 has not proved the good LDP or positive recovery from which these properties are taken. The infinite-horizon discounted supremum may also be infinite unless the state/reward growth and Lyapunov conditions are specified; bounded `h` alone controls reward but not existence of admissible paths from every state.

### 8. The PDE sign and fixed-point inequalities are not reconciled

The equation is written

\[
\lambda u-h=\mathbb H(f,Du,0).
\]

The subsolution is then defined by `u <= J_lambda(h+lambda u)`. A rigorous viscosity/resolvent theory must derive this equivalence with the exact sign convention. The manuscript defines it rather than proving it and then uses the invalid contraction argument above.

### 9. Ensemble-to-kinetic convergence is not established

Upper and lower nonlinear-generator limits on a separating core, exponential compact containment, and comparison would be a viable convergence route. Here:

- the corrector/core theorem is formal;
- B2 compact containment is unproved;
- comparison fails; and
- the initial B1 interface is unproved.

The final convergence theorem is therefore a dependency summary, not a proof.

### 10. The Gaussian risk-sensitive limit requires exponential uniform integrability

Weak process convergence to a Gaussian field does not imply convergence of exponential transforms. The paper cites a “uniform complex moment neighborhood” from B3, but B3 does not prove such a process-level bound. The contact/density exponential functional and its time horizon must be controlled uniformly before the logarithmic transform can pass to the limit.

## Dependency assessment

B4 remains downstream of the unresolved B2/B1/B3 interfaces. It cannot certify the kinetic semigroup used by C1, C2, or D1, and its own comparison theorem fails independently.

## Required reconstruction

A viable revision must:

1. define the discounted value with `f_0=f` and a precise admissible state/control space;
2. prove a genuine nonlinear resolvent range/comparison theorem, not a non-strict Lipschitz tautology;
3. construct the contact-augmented ensemble Green identity;
4. define the law–hierarchy generating-functional intertwiner and corrector domains; and
5. prove exponential uniform integrability for the Gaussian transform.

## Recommendation

**Reject.** The boundary origin of the exponential Hamiltonian is now conceptually correct, but the constructed resolvent and comparison are mathematically invalid and the microscopic convergence theorem remains formal.