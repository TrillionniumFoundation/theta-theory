# Round-Nine Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B3 — *Hamilton–Boltzmann Cotangent Geometry from Deterministic Hard-Sphere Collisions*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round9-referee-positive-closure-11paper-2026-08-31`  
**Payload-host branch head at review lock:** `a8c0c551f5f8614856a9d433e78b2eb92a5dcfa1`  
**Registered round-nine payload SHA-256:** `cf230322211332af59a7883af1b669eeb9b4f7e9f4220fc24712c634bda17716`  
**Reviewed registered source:** `revision/round9-referee-final/B3_KKT_COVARIANCE_OBSERVABILITY.tex`  
**Reviewed source SHA-256:** `8ff852ab0a2ca9522626ba5e034505305936bf92930f0e43a4ef62ac2a80d8d1`  

## Evidence boundary

At the review lock, the branch stored the checksum-pinned round-nine payload while the paper-level `main.tex` files still loaded the round-eight modules; the repository publication workflow was queued. I independently verified the payload hash, unpacked it, and ran the repository materializer successfully, producing byte-identical paper-level `ROUND9_POSITIVE_CLOSURE.tex` files. This report therefore reviews the exact registered round-nine theorem text. It does not treat a queued workflow, a clean build, theorem/proof counts, or an internal hostile-regression script as evidence that the mathematical claims are true.

## Executive assessment

The revision honestly records that the raw perspective Hessian may be indefinite, starts the covariance from finite-volume cumulants, and avoids defining covariance as the inverse of an unproved positive action. Those are sound corrections.

The proposed cure is nevertheless invalid. The weak density–contact balance constraint is linear, so its Lagrange-multiplier term has zero second variation. The manuscript invents a “multiplier curvature” that is not present in the displayed Lagrangian. Consequently the coercive KKT form, Mosco identification, covariance inverse, and Gaussian Cameron–Martin theorem are not established.

## Decisive objections

### 1. The balance multiplier produces no second-order curvature

The displayed constraint is
\[
 \mathcal B(f,\Gamma)
 =\partial_tf+v\cdot\nabla_xf-\Delta^*\Gamma,
\]
which is linear in \((f,\Gamma)\). Therefore, with \(p^*\) fixed,
\[
 D^2_{(f,\Gamma)}
 \langle p^*,\mathcal B(f,\Gamma)\rangle=0.
\]

The manuscript instead adds
\[
 \mathfrak c_{p^*}(u)
 =\int qA_f\,D_f^2(\Delta p^*)[u,u]\,dt+\cdots .
\]
But \(\Delta p^*\) is a collision increment of the fixed multiplier; it does not depend on \(f\), so \(D_f^2(\Delta p^*)=0\). If the intended expression is \(D^2A_f[u,u]\,\Delta p^*\), that term does not come from the linear balance constraint as written.

Thus the KKT-completed form is not the second variation of the displayed Lagrangian.

### 2. Positive constrained curvature is not proved

After removing the nonexistent multiplier curvature, the form still contains
\[
 \int(1-q)D^2A_f[u,u]\,dt,
\]
which has no sign. It may be absorbable on a sufficiently short horizon under a rigorous linearized energy estimate, but the paper has not supplied such an estimate. The proof invokes a backward weighted kinetic equation, a collision spectral gap, endpoint control, and B2 traces without defining the operators or domains.

The numerical condition
\[
 CT_*\|q-1\|<1/2
\]
does not by itself prove coercivity.

### 3. The weighted tangent space is not shown to be preserved by the linearized dynamics

The norm includes a high polynomial velocity weight, a supremum-in-time \(L^2(f^{-1})\) term, and a negative Sobolev term. The paper does not prove existence, uniqueness, trace regularity, or an energy inequality for the linearized biased Boltzmann equation in this space. The “linearized kinetic energy estimate” is itself a major theorem.

### 4. The observability/closed-range theorem is asserted, not proved

Finite-horizon transport plus collision has hydrodynamic modes, spatial high frequencies, endpoint traces, and a nonselfadjoint biased collision operator. Saying that the symmetric collision part has a spectral gap and that macroscopic modes form a finite hyperbolic system does not establish
\[
 \|(p,\psi)\|\le C\bigl(\|\mathcal B^*(p,\psi)\|+\|\Delta p+\psi\|\bigr).
\]
Without a complete adjoint calculation and boundary estimate, closed range and the exact gauge annihilator do not follow.

The identity
\[
 \ker\mathfrak D=\{(r,-\Delta r)\}
\]
is largely tautological for \(\mathfrak D(p,\psi)=\Delta p+\psi\); it is not the same as identifying the null space of the pressure covariance.

### 5. Covariance convergence does not determine the full null space

Normal convergence of finite-dimensional pressures can give finite-dimensional Gaussian limits. A zero limiting variance need not be detected by varying one free-flight cell and one contact. It can arise from global endpoint coboundaries, closed communicating components, or degeneracies of the prepared phase. The exact converse requires the observability theorem that remains unproved.

### 6. The Mosco theorem is circular at the infinite-dimensional step

Finite-dimensional Legendre transforms have local quadratic limits under strict smooth convexity. Passing through increasing projections does not automatically identify the limit with the pathwise second variation of a constrained action.

The proof says that the “explicit second variation” is exactly \(\mathfrak q_{f,q}\), but that form contains the nonexistent multiplier curvature. It then invokes uniqueness of a Mosco limit without proving equicoercivity, domain density, or convergence of the balance constraints. This does not identify the covariance inverse.

### 7. The fourth-moment estimate is not derived from B2

A connected four-time cumulant with one anchor generally integrates over a short interval with order \(|t-s|/\mu_\varepsilon\), while pairings produce \(|t-s|^2\). The final bound may be plausible, but the B2 pressure theorem does not provide the asserted time-density decay or endpoint-atom control. The proof is only a diagrammatic description.

Aldous/Mitoma tightness also requires uniform control of jumps and of the nuclear test embeddings, which are not specified.

## Dependency assessment

B3 remains downstream of the unproved B2 source-sewing theorem and B1 conditioning. It cannot certify a Gaussian process or cotangent rigidity for B4, C1, C2, or D1.

## Required reconstruction

The authors should first derive the second variation of the *actual constrained variational problem* correctly. If short-time positivity is intended, prove it directly from a well-posed linearized equation. Separately prove finite-dimensional cumulant convergence and process tightness. Only then compare the covariance form with a rigorously established action tangent.

## Recommendation

**Reject.** The KKT curvature used to restore positivity is not present in the displayed linear constraint, and the subsequent covariance/action identification is unsupported.
