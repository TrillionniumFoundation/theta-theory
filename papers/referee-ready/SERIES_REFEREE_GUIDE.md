# Series-wide referee guide — revision v4

## Purpose

The five manuscripts form a directed companion-paper series revised after the
2026-08-29 reports.  A single nonconjugate moving collision model carries the
actual chain from response to tangent-law representation.  An independent
analytic no-eclipse open-billiard class supplies a genuine moving specular
strengthening.

## Dependency order

```text
Paper I: all-order response, arbitrary source, exact innovations
    -> Paper II: pressure, symmetric diffusion, full-frequency suspension
        -> Paper III: same-system rough homogenization and microscopic theta-DPP
            -> Paper IV: noncompact filtering and pure Isaacs game
            -> Paper V: tangent characterization and stochastic representations

Paper IV -> Paper V only for the pure path-game branch.
```

Paper III's one-player and controlled HJB results do not depend on Paper IV.
Paper V is strictly downstream and is never used to prove homogenization.

## Recommended specialist allocation

- **Paper I:** hyperbolic dynamics, transfer operators, billiards, symbolic
  coding, and higher response.
- **Paper II:** pressure, suspension renewal, Green--Kubo theory,
  Dolgopyat/BDL estimates, and Lorentz geometry.
- **Paper III:** martingale rough paths, deterministic homogenization,
  monotone schemes, and nonlinear expectations.
- **Paper IV:** nonlinear filtering, monotone variational inequalities,
  stochastic games, and viscosity Isaacs equations.
- **Paper V:** nonlinear semigroup differentiation, Girsanov theory, BSDEs,
  functional Itô calculus, PPDEs, and 2BSDEs.

No single referee should be represented as having certified all five technical
areas unless the report actually covers them.

## Common constants and conventions

```yaml
centered_collision_operator: Q = L - Pi
collision_covariance: symmetrized Green--Kubo = pressure Hessian = bracket
physical_covariance: collision covariance divided by mean roof
physical_diffusion: physical covariance divided by 2
slow_diffusion_convention: sigma sigma^T = physical covariance
terminal_PDE_orientation: -u_t - generator - Hamiltonian = 0
geometric_rough_second_level: sum_i<j + one_half_diagonal
BSDE_orientation: Y_t = terminal + integral(driver) - integral(Z dW)
BSDE_gradient_relation: Z = sigma^T Du in the state-dependent actual branch
maximizing_player: u
minimizing_player: v
pure_saddle_source: curvature_compensation_variational_inequality
```

## Common actual platform

Read `COMMON_ACTUAL_PLATFORM_V4.md` before the individual papers.  The points
most important for cross-paper consistency are:

1. Paper I's branch labels are Paper III's martingale innovations.
2. Paper II's pressure Hessian is Paper III's predictable covariance.
3. Paper III's finite collision recursion is the path law tilted in Paper V.
4. Paper IV's slow game uses the same collision covariance and innovation
   process.
5. The hidden filter is a deterministic product extension, not a replacement
   for the collision dynamics.

## Recommended cross-paper audit

1. Match the width functions `w_i(a)` in Papers I--III.
2. Match covariance normalization in Papers II--III.
3. Match the terminal PDE sign in Papers III--V.
4. Verify that Paper IV's lower/upper limiting Hamiltonians are the ones used
   in its verification theorem and Paper V's pure path game.
5. Verify that Paper V's discrete tangent laws are exponential tilts of Paper
   III's exact finite recursions.
6. Check that all companion citations refer to an actual theorem stated in the
   upstream controlling `main.tex`.

## New high-risk theorems requiring independent review

- analytic symbolic desingularization for moving no-eclipse billiards;
- uniform moving-family Dolgopyat response from temporal shear;
- high-frequency parameter derivative word bounds;
- curvature-compensated pure-saddle variational inequality and viscosity
  approximation;
- static and dynamic tangent-curvature characterization;
- convergence of microscopic deterministic tangent laws.

## Formal-review deliverables

Each paper folder contains:

- `main.tex`;
- `references.bib`;
- `README.md`;
- `REFEREE_GUIDE.md`;
- frozen round-four source and bibliography copies.

At series level include:

- `REVISION_V4_RESPONSE_TO_REFEREES.md`;
- `COMMON_ACTUAL_PLATFORM_V4.md`;
- `REVISION_V4_THEOREM_MANIFEST.yaml`;
- `REVISION_V4_HOSTILE_PROOF_AUDIT.md`;
- the formal report template.

## Verification boundary

The manuscripts are prepared for a second external formal review.  Structural
or formula verification does not certify analytical correctness, novelty, or
journal-level significance.  No acceptance claim should be made before the
new controlling files, rather than the old monograph snapshot, have actually
been reviewed.
