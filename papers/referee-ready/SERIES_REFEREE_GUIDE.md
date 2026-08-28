# Series-wide referee guide

## Purpose

The five manuscripts form a directed companion-paper series.  Each paper is
written as a standalone article, but a later paper may assume one explicitly
restated theorem package from an earlier companion.  No paper uses a later
stochastic representation to prove an earlier deterministic or PDE limit.

## Dependency order

```text
Paper I: bilateral graph-current response and U3
    -> Paper II: pressure, suspension, diffusion, high-frequency flow bounds
        -> Paper III: Doob-selected rough homogenization and theta-HJB
            -> Paper IV: filtering and sequential/mixed/pure games
                -> Paper V: FBSDE/BSDE/2BSDE/PPDE/path representations
```

Paper III's one-player HJB does not depend on Paper IV.  Paper V also imports
the one-player theta-semigroup directly from Paper III.

## Recommended allocation of external referees

- **Paper I:** singular hyperbolic dynamics, anisotropic transfer operators,
  billiards, and higher response.
- **Paper II:** spectral perturbation, suspension flows, Dolgopyat/BDL theory,
  and deterministic diffusion.
- **Paper III:** rough paths, martingale functional limits, deterministic
  homogenization, and viscosity HJB limits.
- **Paper IV:** nonlinear filtering, stochastic differential games, minimax,
  and viscosity Isaacs equations.
- **Paper V:** BSDEs, functional Itô calculus, PPDEs, stochastic games, and
  second-order BSDEs.

A single referee is unlikely to cover every paper at the required depth.

## Cross-paper constants and conventions

```yaml
centered_collision_operator: Q = L - Pi
collision_covariance: pressure Hessian in q
physical_covariance: collision covariance divided by mean roof
physical_diffusion: physical covariance divided by 2
slow_diffusion_convention: sigma sigma^T = physical covariance
HJB_orientation: partial_t u + F = 0, with F_X positive semidefinite
BSDE_orientation: Y_t = terminal + integral(driver) - integral(Z dW)
BSDE_gradient_relation: Z = sigma^T Du
maximizing_player: u
minimizing_player: v
```

## Claims intentionally not made

1. Local finite-horizon geometry alone does not imply arbitrary
   noncoboundary moving-singularity U3.
2. Uniform high-frequency bounds on a compact family do not automatically
   imply table-parameter resolvent differentiability on one graph domain.
3. A qualitative enhanced WIP does not imply a full-scale nonautonomous limit
   without a modulus or direct characteristics.
4. Mixed relaxed minimax does not imply a pure saddle.
5. One payoff-independent classical Markov law does not represent a genuinely
   nonlinear theta-semigroup.
6. A generic nonconvex second-order Isaacs equation is not automatically a
   2BSDE.

## Formal-review deliverables

Each paper folder contains:

- `main.tex`;
- `references.bib`;
- `README.md`;
- `REFEREE_GUIDE.md`.

The human authors should send each manuscript with its paper-specific referee
guide.  The internal repository blocker files are provenance and should not be
used as substitutes for proofs in the circulated manuscripts.

## Human-author checks before circulation

- confirm authorship, affiliation, email, acknowledgements, and disclosure;
- verify every bibliography record against the published source;
- compile from a clean TeX environment;
- check every theorem label, equation reference, and companion citation;
- ensure that each imported companion theorem has a stable public preprint;
- run independent line-by-line proof review before claiming correctness;
- adapt disclosure language to the policy of the eventual journal.

The manuscripts are prepared for external formal review, but no external
review or correctness certification has yet occurred.
