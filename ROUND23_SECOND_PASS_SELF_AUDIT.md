# Round-Twenty-Three second-pass mathematical self-audit

**Branch:** `revision/round23-referee-positive-closure-11paper-2026-09-02`  
**Reviewed report:** `REFEREE_REPORT_ROUND22_GPT56_PRO_HARSH.md`  
**Purpose:** record the additional defects found after the first positive reconstruction, the exact replacements committed before the next referee round, and the downstream interfaces that were rechecked.

This document is a provenance ledger, not an external validation certificate.  The mathematical claims remain those in the eleven `ROUND23_POSITIVE_CLOSURE.tex` sources.

## A2 — exact arithmetic versus finite-precision validation

### Defect found

A finite interval excluding rationals only up to a bounded denominator cannot certify irrationality or closed-subgroup aperiodicity.  Mere character exclusion also does not by itself provide a uniform high-frequency loss on a parameter family.

### Replacement

A2 now requires the exact quantitative certificate `A2-QUANTITATIVE-DIOPHANTINE`.  After using two periodic differences as a basis, three further differences obey a simultaneous Diophantine lower bound for every nonzero integer character.  Symbolic, algebraic, or analytic proof objects establish the exact inequality; interval arithmetic is restricted to periodic-orbit enclosure, homology, regularity, determinant signs, and geometric margins.

A “uniform certified family” is defined by common exact arithmetic constants and common geometric margins.  The source expressly does not infer openness of exact non-arithmeticity.

### Propagation checked

The certificate now supplies the closed-subgroup theorem, the quantitative annulus/high-frequency estimate, covariance nondegeneracy, and the uniform raw four-coordinate LLT imported by A3 and A4.

## A3 — path scaling and measurable macroscopic excursions

### Defects found

The earlier notation `N^{-1} Cat(W_N)` was undefined for a path taking values in a general state space.  The phrase “every subsequence of macroscopic marks” also failed to define one measurable random state and risked threshold double counting.

### Replacement

A3 now uses the time reparametrization

```text
Gamma_N(t) = Cat(W_N)(N t),  0 <= t <= 1,
```

recorded by `A3-TIME-REPARAMETRIZED-PATH`.  No state-space scalar multiplication occurs.

Macroscopic excursions are represented by the measurable projective state `A3-PROJECTIVE-RECESSION`: for every positive rational threshold, the state stores the ordered finite list of normalized marks above threshold and the ordered point measure below threshold.  Deterministic truncation maps enforce compatibility between thresholds.

### Propagation checked

Polishness, concatenation continuity, entropy recovery, goodness, the ordered path LDP, and the conditional path LDP are now stated on that projective state.  A4, C1, C2, and D1 import only this ordered measurable interface.

## A4 — two-rate history geometry and unbounded Feshbach domains

### Defects found

The first weighted history formula algebraically cancelled its own mark-size factor.  The high-frequency resolvent expansion also needed domain assumptions: an unbounded generator cannot be expanded by a formal Neumann series on the whole Hilbert space.

### Replacement

The noncancelling distance-like cost `A4-TWO-RATE-COST` uses sensitivity rate `sigma` strictly below the Lyapunov size rate `rho`, yielding a genuine `(sigma/rho)^m` remote-past bound.

The Feshbach section now defines an admissible finite-rank projection, types the coupling maps `B = QLP` and `C = PLQ`, and derives the expansion from an exact resolvent identity under `A4-SECTORIAL-COUPLING-DOMAIN`.  The generic `z^{-1} PLQLP` term remains.  Time-domain memory decay is proved directly from the orthogonal semigroup gap and does not depend on any inverse-frequency cancellation.

### Propagation checked

C2 treats transmission zeros as zeros, not modes; D1 imports only the typed closed form and genuine covariance compression.

## B3 — detailed balance, hydrodynamic modes, and the normal Hessian

### Defects found

A Maxwellian detailed-balance Dirichlet identity had been written as though it held for a general non-equilibrium path.  More importantly, collision dissipation alone does not control spatially varying hydrodynamic modes: those modes lie in the local collision kernel and are controlled only through transport–collision coupling.

### Replacement

B3 now separates:

1. the true Maxwellian microscopic collision gap;
2. the torus transport–collision hypocoercive gap `B3-HYPOCOERCIVE-GRAPH` on the global conservation quotient; and
3. a small non-autonomous perturbation along a near-Maxwellian trajectory.

The resulting space-time graph operator has the bounded right inverse used by the positive balance chart.  The dynamic action is still expanded in the normal defect

```text
h = delta Gamma - D A_f[u],
```

so its Hessian is `int h^2/A_f` and vanishes identically on every balanced tangent.

### Propagation checked

B4 uses the non-autonomous hypocoercive right inverse in its regular recovery compiler.  C2 uses `L_t^*` rather than unsupported non-equilibrium self-adjointness.  D1 compresses the closed tangent form rather than a Fredholm inverse.

## B4 — containment topology and nonlinear collision products

### Defects found

Putting the numerical value of the superquadratic moment directly into the metric would demand moment-value convergence rather than using it as compact containment.  The prior use of Mazur convex blocks was invalid for nonlinear collision dynamics: an average of solutions is generally not a solution because `Q((f+g)/2,(f+g)/2)` contains cross terms.

### Replacement

B4 separates the weak quadratic-growth metric from the lower-semicontinuous containment function, recorded by `B4-CONTAINMENT-NOT-METRIC`.

The nonlinear passage now uses three distinct gates:

1. weak compactness of action sublevels;
2. a positive regular strong core with Aubin–Lions/velocity-tail compactness, giving strong convergence of collision products; and
3. the balance-preserving recovery compiler `B4-STRONG-CORE-RECOVERY`, which mollifies and then corrects the balance defect with the B3 graph right inverse.

No convex average of nonlinear solutions is used.

### Propagation checked

The Nisio semigroup, Hamiltonian comparison, and microscopic nonlinear semigroup limit use collision products only on the strong core and extend by cost-preserving recovery.  C1 and D1 use the corrected compact containment topology.

## C1 — finite observation envelope and evidence-stable Bayes continuity

### Defect found

With a merely sigma-finite geometric reference, the bound on the set where the predictive evidence is below `delta` was not automatic.  Likelihood differentiation also needed fixed support and positivity only on the diagnostic actions used for inference, not as a global hidden-kernel domination hypothesis.

### Replacement

C1 introduces the finite probability envelope `C1-FINITE-OBSERVATION-ENVELOPE` for the atomic, surface, and volume observation strata.  Hidden deterministic transitions remain undominated.  The evidence density integrates to one against the finite envelope, so the low-evidence contribution is at most `delta` exactly.

Diagnostic actions carry differentiability in quadratic mean, fixed support modulo null sets, score envelopes, persistent excitation, and a uniform Hellinger identifiability condition.

### Propagation checked

The integrated Bayes transition is Feller without hidden-state domination.  Adaptive LAN, testing, posterior contraction, and Bernstein–von Mises use the predictive densities under the finite envelope.  C2 differentiates the joint kernel before Bayes normalization.

## C2 — the actual hypothesis needed for periodic probes

### Defect found

A pressure identity only in a bounded neighborhood of one base potential does not justify sending an exposing potential to zero temperature along `t psi_p`, `t -> infinity`.

### Replacement

C2 now assumes the identity on every complete exposing ray, recorded by `C2-EXPOSING-RAYS`, with a local perturbation in the cocycle direction at every point of the ray.  Differentiation gives zero cocycle expectation under the finite-temperature equilibrium state, and the zero-temperature limit yields every periodic orbit sum before Livšic is invoked.

### Propagation checked

The rigidity theorem now has a valid periodic-data gate.  The weighted strict dual, kinetic adjoint, prediction-process stability, and strictly positive likelihood theorem were rechecked against the corrected A4/B3/C1 interfaces.

## D1 — finite-scale shared policy versus scalar max-plus leading order

### Defect found

For finitely many scalar phase payoffs,

```text
sup_u max_j G_j(u) = max_j sup_u G_j(u).
```

Therefore the leading scalar max-plus value cannot by itself distinguish a common action from phasewise optimization.  Claiming otherwise was algebraically false.

### Replacement

D1 keeps the exact common-control finite-scale operator `D1-FINITE-SCALE-LOGSUMEXP`.  Optimizing each phase before summation is generally a strict upper bound at finite scale.  The leading scalar limit is correctly recorded as `D1-MAX-PLUS-LEADING-ORDER` and is explicitly acknowledged to forget the sharing constraint.

The constraint survives in `D1-SHARED-POLICY-SUBLEADING`: the `A^{-1} log A` and `A^{-1}` corrections, the near-optimal common-control set, and phase-resolved outputs are computed before any phasewise optimization.

### Propagation checked

Morse–Bott coefficients select coexistence weights only after exponential and polynomial orders tie.  The boundary phase remains exponentially negligible, and B4 comparison identifies the leading Nisio semigroup.

## Permanent regression additions

`tools/verify_round23.py` now includes source tokens and explicit tests for:

- normalized pressure and the raw factorial drift;
- Schur conditional covariance;
- the generic Feshbach `z^{-1}` coefficient;
- the balanced collision Hessian;
- a spatial hydrodynamic mode with zero collision dissipation but nonzero transport;
- ordered words and projective recession-list finiteness;
- escaping kinetic energy;
- failure of nonlinear dynamics under convex averaging;
- the finite-envelope low-evidence bound; and
- strict finite-scale separation between one shared control inside phase log-sum-exp and phasewise pre-optimization, together with equality of their scalar max-plus leading values.

## Resulting review scope

The Round-Twenty-Three branch contains a positive reconstruction rather than a no-go revision.  The first-pass referee contradictions and the second-pass type/domain/uniformity defects listed here have been replaced in the active sources and propagated through their downstream interfaces.  Clean source verification and TeX builds establish reproducibility; the next referee remains responsible for independent scrutiny of the long analytic arguments, especially the A2 submersion/Diophantine construction, the B2 loop-opening determinant, the B4 balance-preserving strong-core recovery, and the C1 adaptive testing theorem.
