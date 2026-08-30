# Revision-Round Referee Report — GPT-5.6 Pro

**Manuscript:** B3 — *Hamilton–Boltzmann Cotangent Geometry from Deterministic Hard-Sphere Collisions*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed source:** `main@ae2fdc16bf1ad4a6b58cca6020a7b8b61236e2ad`, manuscript blob `af445408a02f9676de819da91b1bcf4f3510e96d`  
**Revision provenance:** no revised B3 source is present on the repository's discoverable eleven-paper revision ref; the controlling `main` source is reviewed.

## Overall assessment

The paper collects the formal calculus of an exponential Boltzmann collision Hamiltonian: first and second derivatives, scalar entropy conjugacy, conservation invariants, macro-constraint multipliers, and a Gaussian quadratic tangent. The elementary derivative formulas are correct as formal identities.

The central cotangent-selection theorem is not correct. The manuscript quotients only collision invariants, while the pair \((p,\psi)\) has a much larger representation gauge. The functional-analytic setting for the path-space Legendre dual is also absent, and the Gaussian theorem is obtained by formally differentiating an HJ equation rather than proving a microscopic fluctuation limit. Finally, the claimed deterministic origin depends entirely on B2's unproved collision-marked LDP.

## Major objections

### 1. The claimed unique cotangent class is false

The collision exponential depends on

\[
\Delta_\omega p+\psi.
\]

For any admissible field \(r\), the transformation

\[
p\mapsto p+r,
\qquad
\psi\mapsto\psi-\Delta_\omega r
\]

leaves this combination unchanged. Subject to the precise transport and boundary convention, the associated change in the transport term is accounted for by the adjoint balance or boundary contribution. This is a representation gauge much larger than

\[
\operatorname{span}\{1,v_1,v_2,v_3,|v|^2\}.
\]

More fundamentally, because \(\psi\) is introduced as an independent arbitrary collision source, the relation

\[
\frac{d\gamma}{dA_f}=e^{\Delta p+\psi}
\]

can identify only the sum \(\Delta p+\psi\), not the two fields separately. Quotienting collision invariants removes null directions of \(\Delta p\); it does not resolve non-identifiability between \(p\) and \(\psi\).

The theorem needs a specified constraint-adjoint operator and quotient by its full kernel, or an explicit gauge-fixing condition. As stated, uniqueness is impossible.

### 2. The path-space duality has no defined functional setting

The manuscript does not specify the spaces or topologies for

\[
f,\quad \dot f,\quad p,\quad \psi,\quad \gamma,
\]

the velocity weights, trace/boundary conditions, or the dual pairing. It then turns a pointwise scalar conjugate into a global path action.

A rigorous theorem must address:

- time integration by parts and the transport adjoint;
- positivity, exchange symmetry, and pre/post-collisional involution of \(\gamma\);
- singular components of the collision measure;
- closure of the weak kinetic balance;
- coercivity and equi-integrability in unbounded velocity;
- interchange of supremum and space-time integration;
- endpoint terms; and
- the initial rate.

The sentence that the formula is “lower-semicontinuously extended to singular measures” is not a proof of these points.

### 3. Strict convexity of the collision entropy does not imply uniqueness of the full multiplier

The integrand \(\ell\) is strictly convex in the collision density \(d\gamma/dA_f\). It is not thereby strictly convex in the density path \(f\), and it gives no uniqueness of the transport multiplier \(p\). Infinite-dimensional Lagrange multipliers require a constraint qualification, appropriate interiority, closed-range properties of the constraint derivative, and a specified dual topology.

The manuscript's assumptions of a unique primal minimizer and “full-rank” constraint derivative are finite-dimensional shorthand and do not establish the required functional analysis. The compactness of the subdifferential phase set is also unsupported without a topology and coercive bound.

### 4. The Gaussian tangent theorem is formal differentiation

Differentiating a formal Hamilton–Jacobi equation twice yields a quadratic Lyapunov equation. It does not prove convergence of the deterministic hard-sphere fluctuation field, convergence of finite-volume pressure Hessians, or identification of the limiting covariance.

A genuine theorem requires:

- a weighted distribution or test-function space;
- convergence of the initial fluctuation field;
- conservation-law projections;
- uniform differentiability of microscopic cumulants;
- passage of first and second derivatives through the Boltzmann–Grad limit; and
- well-posedness of the resulting Gaussian evolution.

The manuscript omits the initial Gaussian covariance. Under microcanonical and macro conditioning, initial fluctuations are constrained and generally nonzero. The instantaneous quadratic form \(\mathcal Q_f\) is a noise covariance source, not by itself the full finite-horizon pressure Hessian.

### 5. Citing a deterministic fluctuation theorem does not prove the extended collision-source statement

Even if the cited hard-sphere work proves density fluctuations, the present paper adds an independent collision-flow source and uses B2's extended Hamiltonian. The derivative and Gaussian results for that enlarged observable require the source-decorated convergence claimed in B2. They do not follow merely from the density-only fluctuation theorem.

### 6. The exact duality is conditional on B2's unproved LDP

The paper presents the Hamiltonian and action as consequences of deterministic microscopic collisions. That interpretation requires the actual-collision marked cumulant and local LDP. Since B2 has not established them, B3 is a formal kinetic calculus rather than a deterministic theorem.

### 7. The standalone novelty threshold is not met after correction

Once the false uniqueness, unproved microscopic origin, and formal Gaussian limit are removed, the paper consists mainly of differentiating an exponential Hamiltonian and writing the pointwise entropy conjugate. This material could be an analytic section of a future rigorous B2 paper; it is not an independent Annals/Acta/Inventiones/JAMS contribution.

## Status of prior objections

The current source still quotients only the collision-invariant subspace and still allows an independent \(\psi\). The larger gauge identified in the prior review has not been addressed. The Gaussian proof remains a formal HJ differentiation. No material closure is visible.

## Required reconstruction

The correct order is to prove B2, define primal and dual function spaces, formulate the complete constraint-adjoint operator, identify its full kernel, impose or quotient an exact gauge, and prove multiplier existence under explicit constraint qualifications. A microscopic fluctuation theorem with prepared initial covariance must be separate.

## Editorial recommendation

**Reject.** The central uniqueness theorem is false, the path-space duality lacks its functional setting, and the Gaussian tangent is not derived from the microscopic system.
