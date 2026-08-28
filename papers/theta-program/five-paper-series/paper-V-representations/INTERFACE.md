# Paper V theorem interface

## Imports

From Paper III:

- `P3-HJB`
- `P3-THETA`

From Paper IV:

- `P4-SEQ`
- `P4-MIXED`
- `P4-PURE-GATE`
- `P4-PURE-ISAACS-MAXIMAL`
- `P4-BELIEF`
- `P4-PATH`
- `P4-WEIGHTED-NONCOMPACT-ACTUAL`

## Exports

- `P5-SINGLE-LAW-NOGO`: payoff-independent linear-law obstruction.
- `P5-CALIBRATED`: exact payoff-calibrated linear PDE and Feynman--Kac
  formula.
- `P5-FBSDE`: semilinear Markov FBSDE branch.
- `P5-CONTROL-BSDE`: controlled or randomized BSDE branch.
- `P5-SECOND-ORDER`: convex 2BSDE versus nonconvex game/nonlinear-MP typing.
- `P5-PPDE`: path-dependent PPDE and path-evaluation branch.
- `P5-PATH-ACTUAL`: actual noncompact delay-state value, segment DPP,
  generator-oriented path equation with horizontal shift, and BSDE path
  evaluation, coupled to the actual weighted filter through its stationary
  averaged coefficient; normative proof:
  `../../maximal-strengthening/WEIGHTED_NONCOMPACT_PATH_ACTUALIZATION.md`.
- `P5-GIRSANOV`: post-calibration Girsanov formula.

## Actual path scope

The limiting state is the delay segment `C([-delta,0])`. The fast noncompact
filter is averaged before the limit; its stationary observable enters the
delay drift and its centered contribution is `O_{L2}(epsilon)`. Therefore the
PPDE contains the segment shift generator and present-endpoint vertical
derivatives, but no untyped leftover belief derivative.

## Forbidden reverse uses

- FBSDE or Girsanov may not prove the HJB homogenization.
- A calibrated payoff law may not be promoted to one law for the nonlinear
  semigroup.
- A generic nonconvex Isaacs equation may not be routed to a convex 2BSDE.
- A Markov current-state payoff may not be relabelled as an actual path payoff.
