# Referee Report

**Manuscript:** B3 — Hamilton–Boltzmann Cotangents  
**Recommendation:** **Reject**  
**Standard applied:** Annals / Acta / Inventiones / JAMS  
**Review target:** pinned eleven-paper clean-main tree, SHA-256 `566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2`.

## Overall assessment

The paper organizes familiar formal relations around the Boltzmann collision Hamiltonian: first and second derivatives, convex duality with a collision-flow entropy, conservation gauges, and a Gaussian tangent. The elementary derivative formulas are correct. The claimed cotangent-selection and fluctuation theorems are not.

The manuscript is largely formal algebra built on B2’s unproved joint collision-flow LDP. In addition, the asserted uniqueness of the pair \((p,\psi)\) is false because the Hamiltonian has a larger gauge than the paper quotients.

## Major objections

### 1. The “exact density–collision duality” lacks a functional-analytic theorem

The paper does not specify the spaces for \(f,\dot f,p,\psi,\gamma\), the topology of the dual pairing, boundary conditions, velocity weights, or the definition of the reference measure \(A_f\) within the manuscript. It then invokes Fenchel duality as if pointwise conjugation of the exponential automatically yielded the full path-space lower-semicontinuous dual.

A rigorous theorem must address:

- the transport term and time integration by parts;
- positivity and symmetry of collision measures;
- singular parts of \(\gamma\);
- closure of the weak balance constraint;
- coercivity/equi-integrability in unbounded velocity;
- interchange of supremum and integration;
- the initial cost.

The displayed scalar conjugacy is only the local algebraic ingredient.

### 2. The claimed unique cotangent class is false

Only collision invariants are quotiented. But the combination entering the collision exponential is
\[
\Delta p+\psi.
\]
For any admissible function \(r\),
\[
p\mapsto p+r,\qquad
\psi\mapsto\psi-\Delta r
\]
leaves this combination unchanged. Depending on the balance/boundary convention, the transport contribution changes only by the corresponding adjoint/boundary term. At a minimum this produces a much larger representation gauge than
\(\operatorname{span}\{1,v,|v|^2\}\).

Moreover, because \(\psi\) is introduced as an independent arbitrary collision source, the equation
\[
\frac{d\gamma}{dA_f}=e^{\Delta p+\psi}
\]
cannot uniquely determine both \(p\) and \(\psi\). The theorem needs a specified macro-constraint adjoint map and a quotient by its full kernel. As written, uniqueness is plainly untenable.

### 3. Unique primal minimizer plus full-rank constraint derivative is insufficient

In infinite-dimensional convex optimization, existence and uniqueness of Lagrange multipliers require a constraint qualification, appropriate interiority, closed range of the derivative/adjoint, and differentiability or essential smoothness of the value function. Strict convexity of \(\ell\) in \(\gamma\) does not give strict convexity in the density path \(f\), nor uniqueness of \(p\).

The assertion that multiple minimizers produce a compact subdifferential set is also unsupported; compactness depends on the selected dual topology and coercivity.

### 4. The Gaussian tangent is only formal differentiation

Differentiating a formal Hamilton–Jacobi equation twice does not prove convergence of the deterministic hard-sphere fluctuation field or identify the Hessian of the path pressure. One needs differentiability of the limiting semigroup, convergence of finite-volume derivatives, and a well-posed Gaussian evolution in a specified weighted distribution space.

The displayed stochastic equation omits the initial Gaussian field and its covariance. Under microcanonical preparation, the initial fluctuations are constrained/projection-modified and are not generally zero. The instantaneous quadratic form \(\mathcal Q_f\) is the noise covariance source, not by itself the full Hessian of a finite-horizon pressure.

### 5. The paper’s principal nonformal input is B2

The joint Hamiltonian and action are asserted to arise from the collision-marked deterministic LDP. Since B2 has not proved that LDP, B3 cannot present the formal Legendre transform as a deterministic hard-sphere theorem.

### 6. Originality is insufficient after correction

Once the unsupported kinetic claims are removed, the paper consists of differentiating an exponential Hamiltonian and applying the scalar entropy conjugate. This may belong as a section in a paper that actually proves the underlying LDP, but it is not a standalone top-journal contribution.

## Editorial recommendation

**Reject.** The unique-cotangent theorem is false as stated, the duality lacks its functional setting, and the Gaussian theorem is formal. The paper should be merged into a future rigorous B2 after the full gauge and multiplier theory are correctly formulated.
