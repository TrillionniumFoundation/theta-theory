# Theorem Inventory: Paper 3 representation calculus

- Created: 2026-07-07
- Master source: `../../main.tex`
- Extraction target: `main.tex`

## Core body allocation

| Paper 3 item | Current label | Master source |
| --- | --- | --- |
| theta-expectation semigroup input | `ass:theta_semigroup_input` | `main.tex:7634-7666` |
| Linearity obstruction | `thm:linearity_obstruction` | `main.tex:7667-7694` |
| Payoff-dependent linearization | `def:calibrated_linear_generator`, `thm:linearized_representation` | `main.tex:7695-7739` |
| Degenerate calibrated representation | `thm:regularized_diffusion_representation` | `main.tex:7740-7795` |
| Downstream representation character | `thm:representation_package` | `main.tex:7796-7817` and local synthesis |
| Decoupled FBSDE | `thm:fbsde_representation` | `main.tex:7818-7844` |
| Hamiltonian shift/Girsanov | `def:hamiltonian_shift`, `thm:nonlinear_cm_formula` | `main.tex:7845-7888` |
| Representation hierarchy | final positioning section | `main.tex:7889-7899` |
| Sign convention and orientation | `prop:parabolic_orientation_ledger` | `main.tex:13636-13685` |
| Robust-pricing illustration | `def:calibrated_stress_family`, `prop:robust_pricing_stress_test` | local synthesis |

## Appendix Allocation

| Appendix item | Role | Master source |
| --- | --- | --- |
| Calibrated nonlinear semigroup details | supports regularized diffusion representation | `main.tex:11703-12052` |
| Detailed calibrated generator | supports freezing after decoupling field is known | `main.tex:13321-13451` |
| Gradient variable vs BSDE integrand | prevents confusing `p` and `Z` | `main.tex:13452-13635` |
| Sign convention and parabolic orientation | fixes terminal-value convention | `main.tex:13636-13685` |
| Post-derivation calibration | acyclicity and representation guardrail | `main.tex:15756-15890` |

## Submission-facing main theorem

The paper's main theorem should be the representation package theorem:

> Given the theta-expectation semigroup derived in Paper 2, each sufficiently
> regular payoff determines a payoff-calibrated linearized generator,
> carre-du-champ, calibrated diffusion representation, decoupled BSDE, and
> semigroup-level Cameron-Martin--Girsanov formula.

## Local Labels Added or Promoted

| Local label | Purpose |
| --- | --- |
| `ass:representation_window` | Smoothness, nondegeneracy, and localization window for representation theorems. |
| `lem:gradient_z_conversion` | Prevents confusing HJB gradient \(p\) with BSDE integrand \(Z\). |
| `prop:parabolic_orientation_ledger` | Checks terminal-value HJB, forward parabolic time, and backward BSDE sign conventions. |
| `def:calibrated_stress_family` | Defines compact deterministic stress families for the calibrated robust-pricing illustration. |
| `prop:robust_pricing_stress_test` | Records the robust-pricing/model-uncertainty stress-test interpretation after calibration. |
| `prop:post_derivation_calibration` | Explicitly records that calibrated laws are downstream of Paper 2 and payoff-dependent. |

## Bibliography/Provenance Pass

- `main.tex` now cites the standard stochastic-analysis and PDE references used
  by the representation calculus: `stroock2007multidimensional`,
  `CrandallIshiiLions1992`, `FlemingSoner2006`, `PardouxPeng1992`,
  `protter2012stochastic`, and `Peng2019`.
- The visible theorem map has been converted from source-line provenance to a
  journal-facing proof-role map.  Exact source lines remain in this inventory.

## Keep out

- Singular billiard response proofs.
- Deterministic homogenization proof.
- Any wording suggesting that BSDE or Girsanov formulae prove the HJB limit.
