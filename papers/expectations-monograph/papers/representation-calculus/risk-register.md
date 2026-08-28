# Risk Register: Paper 3 representation calculus

- Created: 2026-07-07

## R1: Representation reverses the dependency order

- Severity: high
- Risk: A referee may think the paper uses BSDE/Girsanov arguments to justify
  the HJB equation.
- Mitigation: Keep the input theorem from Paper 2 explicit.  Use "post-
  derivation" language in the abstract, introduction, assumptions, and main
  theorem.
- Current status: materially addressed in `main.tex` by the provenance and
  dependency guardrail paragraph, the isolated `ass:theta_semigroup_input`, and
  `prop:post_derivation_calibration`.

## R2: Single martingale problem ambiguity

- Severity: high
- Risk: Nonlinear generator language can be misread as a classical martingale
  problem under one law.
- Mitigation: Keep the linearity obstruction theorem near the beginning.
  Emphasize payoff-dependent calibrated laws.
- Current status: addressed by `thm:linearity_obstruction` and the new
  post-derivation calibration proposition, which explicitly rules out a single
  payoff-independent martingale problem.

## R3: Smoothness and nondegeneracy assumptions

- Severity: medium-high
- Risk: BSDE and Girsanov formulae require more regularity than the viscosity
  HJB theorem.
- Mitigation: State smooth/nondegenerate versions separately from degenerate
  viscosity-regularized representations.
- Current status: improved by `ass:representation_window`, which separates the
  smooth/nondegenerate window from the viscosity-regularized degenerate
  representation.

## R4: Gradient `p` versus BSDE integrand `Z`

- Severity: medium
- Risk: Confusing `Z` with the gradient rather than `sigma^T grad u`.
- Mitigation: Keep the `Z = sigma^T grad u` convention in the main theorem and
  reserve appendix space for the detailed variable conversion.
- Current status: addressed in the main text by `lem:gradient_z_conversion`.
  The terminal-value sign convention is now also checked by
  `prop:parabolic_orientation_ledger`.

## R5: Journal positioning

- Severity: medium
- Risk: A pure probability journal may not want billiard context, while a
  control journal may want sharper PDE assumptions.
- Mitigation: Prepare two framing variants:
  - probability/stochastic-analysis framing for SPA/AAP/EJP;
  - control/PDE framing for SICON.
- Current status: still open.  The draft now has standard
  stochastic-analysis citations, making a probability-facing posture more
  plausible.  `submission-package-checklist.md` and `referee-risk-memo.md`
  record the probability/stochastic-analysis, control/PDE, and finance-facing
  options; target-specific introduction remains.

## R6: Application example

- Severity: medium
- Risk: Without an example, Paper 3 may feel like formal calculus.
- Mitigation: Add a short robust-pricing/model-uncertainty example only after
  the core theorem chain is stable.
- Current status: addressed at illustration level.  The core representation
  chain now includes a short robust-pricing/model-uncertainty stress-test
  example.  Further application expansion should wait for a target venue.
