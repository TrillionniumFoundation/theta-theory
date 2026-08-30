# Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B3 — Hamilton–Boltzmann Cotangents  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**  
**Review object:** SHA-256-pinned eleven-paper source archive `566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2`

## Executive assessment

The paper organizes the formal calculus of an exponential Boltzmann collision Hamiltonian: first and second derivatives, pointwise entropy conjugacy, conservation gauges, adjoint variables, and a Gaussian tangent. The elementary differentiations are correct as formal algebra.

The advertised deterministic cotangent theorem is not. The path-space duality lacks a functional-analytic setting, the uniqueness claim is false because the representation has a larger gauge than the manuscript quotients, and the Gaussian statement is not derived from the microscopic hard-sphere system. The only nonformal origin claimed for the Hamiltonian is B2's unproved actual-collision LDP.

## Major mathematical objections

### 1. Pointwise scalar conjugacy is not a path-space duality theorem

The manuscript does not specify the spaces or topologies for

\[
f,\quad \dot f,\quad p,\quad \psi,\quad \gamma,
\]

the velocity weights, boundary conditions, or the dual pairing. It then passes from the scalar conjugate of \(e^z-1\) to a global action without proving the required closure and interchange results.

A rigorous theorem must address at least:

- the transport term and time integration by parts;
- positivity and exchange/pre-post symmetry of \(\gamma\);
- singular components of the collision measure;
- closure of the weak balance constraint;
- coercivity and equi-integrability in unbounded velocity;
- interchange of supremum and space-time integration;
- boundary and terminal terms; and
- the prepared initial cost.

The local formula is only one algebraic ingredient.

### 2. The claimed unique cotangent pair is false because the full gauge is not quotiented

The collision exponential depends on the combination

\[
\Delta p+\psi.
\]

For any admissible function \(r\), the transformation

\[
p\mapsto p+r,
\qquad
\psi\mapsto\psi-\Delta r
\]

leaves this combination unchanged. Depending on the precise balance and boundary convention, the transport contribution is adjusted by the corresponding adjoint/boundary term. This is a representation gauge far larger than the span of collision invariants \(1,v,|v|^2\).

More simply, if \(\psi\) is an independent arbitrary collision source, the relation

\[
\frac{d\gamma}{dA_f}=e^{\Delta p+\psi}
\]

can determine only the sum \(\Delta p+\psi\), not both variables separately. The uniqueness theorem is therefore untenable on its face. The authors must define a constraint adjoint map and quotient by its full kernel or impose a gauge-fixing condition.

### 3. Strict convexity in the collision flow does not imply uniqueness of the full multiplier

The entropy is strictly convex in \(\gamma\) on an appropriate absolutely continuous class. It need not be strictly convex in the density path \(f\), and it says nothing by itself about uniqueness of \(p\). Infinite-dimensional multiplier uniqueness requires a constraint qualification, interiority, closed-range/adjoint properties, and a carefully chosen topology.

The paper's “full-rank derivative” language is finite-dimensional shorthand and does not establish these conditions. The assertion that the multiplier set is compact in the nonunique case is likewise meaningless until a dual topology and coercive bound are fixed.

### 4. The Gaussian tangent is formal differentiation, not a limit theorem

Differentiating a candidate Hamiltonian twice yields a quadratic form. It does not prove convergence of the centered deterministic hard-sphere fluctuation field, convergence of finite-volume pressure Hessians, or well-posedness of the limiting stochastic evolution.

A genuine theorem needs:

- differentiability of the limiting nonlinear semigroup;
- uniform convergence of finite-volume derivatives;
- a weighted distribution space for the fluctuation field;
- initial fluctuation convergence;
- conservation-law projections; and
- identification of the noise covariance and propagator.

The manuscript omits the initial Gaussian field. Under microcanonical/moment preparation, the initial covariance is constrained and generally nonzero. The instantaneous collision quadratic form is a noise source, not by itself the full finite-horizon pressure Hessian.

### 5. B2 is the indispensable missing microscopic input

The paper repeatedly presents the Hamiltonian and action as deterministic hard-sphere consequences. That interpretation requires B2's joint density/actual-collision LDP. Since B2 does not prove that theorem, B3 has only a formal kinetic Hamiltonian.

A Legendre transform cannot manufacture the microscopic LDP from which it is supposed to arise.

### 6. Conservation invariants and representation gauges are conflated

Collision invariants describe the kernel of the collision increment \(\Delta p\). The freedom to redistribute a potential between \(p\) and an independent source \(\psi\) is a different gauge. Quotienting only the former does not cure the latter. The paper's geometric language obscures this elementary identifiability failure.

### 7. Standalone novelty is insufficient after correction

Once the deterministic interpretation, false uniqueness, and unproved Gaussian convergence are removed, the paper consists mainly of differentiating an exponential Hamiltonian and writing its scalar entropy conjugate. Such material belongs in the analytic section of a future paper that proves B2, not as a separate top-journal submission.

## Dependency assessment

B3 cannot serve as a certified cotangent-selection or Gaussian-tangent input for B4/D1. Downstream arguments must carry the full gauge, initial covariance, and conditional status of the collision Hamiltonian.

## Minimum viable reconstruction

The correct order is:

1. prove the B2 joint LDP;
2. define the primal and dual function spaces;
3. formulate the adjoint constraint operator;
4. identify and quotient its complete kernel;
5. prove multiplier existence/uniqueness under explicit constraint qualifications; and
6. separately prove a fluctuation limit.

## Recommendation

**Reject.** The central uniqueness theorem is false as stated, the path-space duality is not constructed, and the Gaussian tangent is formal. The paper should be merged into a future rigorous collision-LDP paper after the full gauge is fixed.
