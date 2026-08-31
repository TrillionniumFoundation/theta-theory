# Independent Referee Report — Round Ten (GPT-5.6 Pro)

**Manuscript:** B4 — Nonlinear Kinetic Semigroups  
**Reviewed revision:** `revision/round10-referee-positive-closure-11paper-2026-08-31@b45406b03ab45e70461d36da5d3ee64892a92c8f`  
**Controlling mathematical commit:** `101dc123e4bafbb8e140e658ac1390f7735dc67e`  
**Registered module SHA-256:** `a39a7888312e5af60f16b0c70dc787ad1859b3e4c7faaa1ab4ba0da1e2728f5e`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject.**

## Executive assessment

Round ten improves the typing of the microscopic flow, its Koopman action, the push-forward on laws, and the limiting action semigroup. The dynamic action no longer charges preparation at every subinterval, and the terminal corrector has the proper backward sign.

The main convergence theorem remains unproved. The finite-horizon tower leaves the domain originally assigned to macro-observables, the observable core theorem assumes the very graph-core density it claims to establish, and the comparison proof contains a direct derivative error: the gradient of the quadratic Tataru penalty is not bounded by the truncation slope \(\lambda\). Thus the Hamiltonian is evaluated on uncontrolled jets, exactly the defect the construction was meant to avoid. The paper also inherits the unproved B1–B3 interfaces.

## Major mathematical objections

### 1. The displayed finite-horizon tower leaves the declared observable class

The value is defined for a terminal macro-observable \(G\) through

\[
G(X_t^\varepsilon(x)).
\]

The inner value

\[
x\longmapsto\mathcal V_{s,t}^\varepsilon(G;\delta_x)
\]

depends on the complete microscopic state \(x\), not generally only on the macrostate \(X_s^\varepsilon(x)\). The outer \(\mathcal V_{r,s}\) was not defined on arbitrary microscopic observables. One can extend the definition and recover the elementary deterministic tower, but the theorem as written is still ill-typed relative to its own domain.

This also confirms that no exact finite-volume Markov closure on the kinetic macrostate has been obtained.

### 2. The resolvent-core proof is circular

For a closed generator \(A\), \(R_\lambda\) maps the whole underlying Banach space onto \(D(A)\), and the graph norm is equivalent to the norm of \((\lambda-A)u\). To conclude that \(R_\lambda\mathcal D_0\) is a graph core, one must prove that \(\mathcal D_0\) is dense in the underlying observable space.

The manuscript instead says that “the range of \(\lambda-A\) on the dense cylinder class is dense,” which is precisely the nontrivial core statement for a singular reflected hard-sphere generator. Smooth cylinders satisfying specular matching need not approximate observables with grazing/contact singularities in the chosen weighted norm. Hille–Yosida does not prove this density.

The additional claim that smooth functional calculus preserves the graph domain requires a product/chain rule for the closed collision generator, including boundary traces. It is not supplied by ordinary finite-dimensional calculus.

### 3. The full-hierarchy corrector is not shown to be normally summable

The proof quotes connected coefficients of size

\[
j!C^jT^{j-1}
\]

and says that multiplication by \(\mu_\varepsilon^{1-j}\) and a smaller label weight makes the series summable. A factorially growing sequence has zero ordinary radius of convergence. Cancellation by the factorial in the product norm must be written explicitly and tracked through the generator image, time derivative, source derivatives, and loss of label radius.

No product-space norm or uniform estimate appears in the theorem. The statement that the equation itself proves graph-domain interchange is not a closed-operator argument.

### 4. The cylinder Hamiltonian convergence is only a restatement of B2's missing theorem

The corrector is said to cancel “every correlation defect,” creation trees are said to converge, and cycles are removed by B2. No formula identifies the finite nonlinear generator, no error is estimated in a separating cylinder core, and no compact-containment theorem is proved here. The result is conditional on the entire unproved B2 source expansion.

### 5. The comparison penalty does not have slope bounded by \(\lambda\)

The manuscript uses

\[
\Phi_{\epsilon,\lambda}(f,g)
=\frac{d_\lambda(f,g)^2}{2\epsilon}.
\]

Suppose \(d_\lambda\) is differentiable in a test direction and
\(\|D_fd_\lambda\|\le\lambda\). Then

\[
\|D_f\Phi_{\epsilon,\lambda}\|
=\frac{d_\lambda(f,g)}{\epsilon}
  \|D_fd_\lambda\|.
\]

At a doubled maximum the proof obtains only

\[
d_\lambda(f,g)=O(\sqrt\epsilon),
\]

so the jet is of size

\[
O(\lambda/\sqrt\epsilon),
\]

not bounded by \(\lambda\). The sentence asserting a bounded slope is false.

Therefore the first limit \(\epsilon\downarrow0\) evaluates the Hamiltonian on unbounded cotangents. Continuity on a fixed radius-\(\lambda\) source ball is irrelevant, and the advertised order of limits does not close the viscosity comparison.

### 6. Truncating the collision ratio does not automatically yield comparison for the full Hamiltonian

Restricting \(q\) to \([e^{-M},e^M]\) changes the convex Hamiltonian to the conjugate of a truncated entropy. To pass \(M\to\infty\), one needs local uniform convergence on the actual viscosity jets and a balance-preserving approximation of minimizing paths. The former is unavailable because the jets above diverge; the latter is delegated to B2's unproved repair lemma.

Entropy bounds provide uniform integrability of large \(q\), but they do not by themselves prove that clipping \(q\), repairing the kinetic balance, and preserving endpoints changes the value uniformly on compact action sublevels.

### 7. Compact action sublevels and relaxed maximizers are imported, not established

The Lax–Oleinik semigroup theorem assumes the B2 rate is good in a topology strong enough for endpoint evaluation and concatenation. B2 has not proved that compactness. Unbounded velocity, contact traces, and weak kinetic balance make endpoint closure nontrivial.

The semigroup law is formal once such a good dynamic action exists, but it cannot supply the missing LDP or compactness.

## Dependency and editorial assessment

B4 is downstream of B1, B2, and B3. Each of those papers retains a load-bearing failure, and B4 additionally fails independently at the comparison step. C1, C2, and D1 cannot cite its nonlinear semigroup as a completed limit.

A viable paper would define one observable Banach space and core, prove generator convergence there, and establish a comparison theorem with a penalty whose jets are controlled in the Hamiltonian domain. The current paper is not a proof of those results.

## Recommendation

**Reject.** The revision fixes several labels and signs, but its key viscosity argument contains a direct gradient miscalculation, while graph-core and generator convergence are assumed. The nonlinear semigroup theorem is not established.
