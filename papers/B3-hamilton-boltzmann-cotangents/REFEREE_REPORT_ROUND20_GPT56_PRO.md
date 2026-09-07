# Referee Report — Round 20 (No-Revision Reconsideration)

**Paper:** B3 — *Hamilton–Boltzmann Cotangent Geometry from Deterministic Hard-Sphere Collisions*  
**Branch inspected:** `revision/round19-referee-positive-closure-11paper-2026-09-02`  
**Branch head inspected:** `4eb32f8ff66dbb93edaabcf96d8c62bf06f13bc2`  
**Active mathematical source:** `ROUND17_POSITIVE_CLOSURE.tex`  
**Active source blob:** `b528af2b8483584387181503844ec7f7d98c0d55`  
**Prior detailed report:** `REFEREE_REPORT_ROUND18_GPT56_PRO.md`  
**Date:** 2 September 2026  
**Editorial recommendation:** **REJECT WITHOUT RECONSIDERATION**

## 1. Reconsideration status

The declared revision branch contains no new B3 manuscript. The active source is identical to the file previously reviewed. In particular, the cutoff-collision observability estimate, the cumulant input from B2, the process-tightness argument, and the Mosco recovery are unchanged. The prior detailed report remains fully operative.

## 2. Unresolved fatal defects

### 2.1. The observability estimate still has impossible velocity regularity

For an angular-cutoff hard-sphere collision kernel, the linearized collision Dirichlet form supplies weighted `L^2_v` coercivity on the microscopic component. It does not control a full velocity derivative. The manuscript nevertheless claims an `H^1_v` estimate and writes a hypocoercive energy containing `\|p_\perp\|_{H^1_v}`. Transport commutators can transfer damping between microscopic and spatial hydrodynamic modes, but they cannot manufacture missing velocity Sobolev regularization for a cutoff operator.

A sequence of microscopic functions with bounded weighted `L^2_v` norm and increasing velocity oscillation directly contradicts the displayed estimate: the cutoff Dirichlet form remains of `L^2` size while the `H^1_v` norm diverges. Hence the asserted closed range and bounded right inverse do not follow.

### 2.2. The nonautonomous and nuclear-space constructions remain slogans

Even after replacing `H^1_v` by a legitimate cutoff coercive norm, one would need fixed domains, uniform bounds for time-dependent `f` and `q`, commutator estimates, control of invariant modes, and a precise adjoint closed-range theorem. “Freeze coefficients and use Gronwall” does not supply these.

The projective intersection of weighted Sobolev spaces is also merely called nuclear. Nuclearity requires Hilbert–Schmidt embeddings between specified levels, with all boundary traces and collision symmetries included. Neither `\mathscr S` nor `\mathscr S_c` is constructed sufficiently for Mitoma's theorem.

### 2.3. The cumulant and process CLT still lack a valid microscopic basis

The localized cumulant estimate relies on B2's “factorial majorant,” whose active proof drops a factorial and therefore does not converge. Exact microcanonical conditioning is not shown to preserve interval-local cumulant estimates. The increment bound containing `(|t-s|+\mu_\varepsilon^{-1})^2` does not by itself yield uniform Kolmogorov tightness; Aldous estimates at stopping times, compact containment, and jump-size/bracket control are absent. Differentiating a formal limiting Hamiltonian identifies at most a candidate covariance, not a Gaussian martingale problem for the deterministic contact process.

### 2.4. The action is still treated as convex without justification

The entropy perspective is convex in `(A,\Gamma)`, whereas `A_f\propto ff_*B` is quadratic in `f`. The resulting action need not be convex in `(f,\Gamma)`. The source nevertheless invokes convex Mosco convergence and Legendre duality. No local convexity, twice epi-differentiability, or nonconvex second-order theorem is provided.

### 2.5. Positive exactly balanced recovery remains missing

The proposed second-order correction assumes the invalid right inverse, does not compute the nonlinear balance defect or prove it lies in the range, and does not preserve positivity on unbounded velocity space. Sobolev-small perturbations need not be pointwise dominated by a background that can approach zero. The connection between the balance quotient and `\operatorname{Ran}\Sigma^{1/2}` is also asserted rather than proved.

## 3. Editorial consequence

A new manuscript must adopt a correct cutoff coercive space, prove a nonautonomous closed-range theorem, build the nuclear test scale, derive microscopic cumulants and stopping-time tightness independently of the flawed B2 expansion, and use an appropriate second-order variational framework. No revision addressing these points is present.

## 4. Recommendation

**Reject without reconsideration.** The central observability theorem remains false in its stated norm, and the manuscript is unchanged.