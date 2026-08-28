# Paper V theorem interface

## Imports

From Paper III:

- `P3-HJB`
- `P3-THETA`

From Paper IV:

- `P4-SEQ`
- `P4-MIXED`
- `P4-PURE-GATE`
- `P4-BELIEF`
- `P4-PATH`

## Exports

- `P5-SINGLE-LAW-NOGO`: payoff-independent linear-law obstruction.
- `P5-CALIBRATED`: exact payoff-calibrated linear PDE and Feynman--Kac
  formula.
- `P5-FBSDE`: semilinear Markov FBSDE branch.
- `P5-CONTROL-BSDE`: controlled or randomized BSDE branch.
- `P5-SECOND-ORDER`: convex 2BSDE versus nonconvex game/nonlinear-MP typing.
- `P5-PPDE`: path-dependent PPDE and path-evaluation branch.
- `P5-GIRSANOV`: post-calibration Girsanov formula.

## Forbidden reverse uses

- FBSDE or Girsanov may not prove the HJB homogenization.
- A calibrated payoff law may not be promoted to one law for the nonlinear
  semigroup.
- A generic nonconvex Isaacs equation may not be routed to a convex 2BSDE.
