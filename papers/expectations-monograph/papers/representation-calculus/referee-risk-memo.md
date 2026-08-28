# Paper 3 Referee-Risk Memo

This memo records the current submission posture for
`Representation Calculus for theta-Expectations`.

## Current Verdict

Paper 3 is now a coherent downstream representation draft.  It imports the
theta-expectation semigroup from Paper 2, then develops fixed-payoff
linearization, calibrated diffusion, BSDE, and semigroup-level Girsanov
representations.  The current package has a clean PDF build, bibliography, and
retained submission PDF.  It now also contains a terminal-value
sign-convention ledger and a short robust-pricing/model-uncertainty stress
illustration.

## Main Referee Risks

### R1. Representation could be mistaken for derivation

Status: materially addressed.

Mitigation already in the draft:

- The abstract and introduction say the representations are downstream of the
  already-derived HJB/theta-expectation semigroup.
- `ass:theta_semigroup_input` isolates the only input from Paper 2.
- `prop:post_derivation_calibration` explicitly states that calibrated laws and
  BSDEs do not prove the HJB theorem.

Remaining action:

- Once Paper 2 has an external preprint/submission identifier, cite it directly
  in the introduction and bibliography.

### R2. One-law martingale problem ambiguity

Status: addressed.

Mitigation already in the draft:

- `thm:linearity_obstruction` appears before the representation theorems.
- The calibrated law depends on the fixed payoff through the decoupling field
  \(u\).
- The package theorem describes the laws as payoff-calibrated rather than
  universal.

Remaining action:

- Avoid adding any prose that calls the nonlinear generator a classical
  martingale-problem generator without the fixed-payoff qualifier.

### R3. Smoothness and nondegeneracy assumptions

Status: improved, but still venue-sensitive.

Mitigation already in the draft:

- `ass:representation_window` separates the smooth/nondegenerate window from
  the viscosity-regularized degenerate representation.
- The BSDE theorem is stated only on nondegenerate jet regions.

Remaining action:

- For a probability journal, expand the stochastic-equation well-posedness
  assumptions by one paragraph.
- For a PDE/control journal, keep the assumptions compact and emphasize
  viscosity regularization.

### R4. Gradient variable versus BSDE integrand

Status: addressed.

Mitigation already in the draft:

- `lem:gradient_z_conversion` states explicitly that \(Z\neq p\), and that
  \(Z=\sigma^\top\nabla u\).
- The FBSDE theorem uses the conversion \(p=(\sigma^\top)^{-1}Z\) only after
  nondegeneracy and fixed payoff are in place.
- `prop:parabolic_orientation_ledger` checks the terminal-value HJB,
  forward parabolic time, and backward BSDE sign conventions.

Remaining action:

- None at the current level; expand only if a referee asks for a longer BSDE
  convention appendix.

### R5. Paper could feel formal without an example

Status: addressed at illustration level.

Possible example:

- `def:calibrated_stress_family` and `prop:robust_pricing_stress_test` give a
  compact robust-pricing/model-uncertainty stress test using calibrated
  Girsanov shifts.
- Keep it short unless a finance-facing venue is selected.

### R6. Target venue framing

Status: open.

Likely framing choices:

- Probability/stochastic analysis: emphasize payoff-calibrated martingale
  problems, BSDEs, and why no single law exists.
- Control/PDE: emphasize linearization of a nonconvex HJB semigroup and the
  calibrated generator calculus.
- Finance: expand the robust-pricing example only after target selection.

## Current QA Facts

- `representation-calculus.pdf` is 6 pages and 286530 bytes.
- Both PDFs have SHA256
  `4cfa46f73edfce134c037b0e2963ca091d55a1ed89961638b4b9ddc03be6ade5`.
- Final build command: two
  `pdflatex -interaction=nonstopmode -halt-on-error main.tex` runs after
  BibTeX was already current.
- Log scan is clean for fatal errors, LaTeX errors, undefined citations,
  undefined references, undefined control sequences, overfull boxes, and
  BibTeX warnings.
- Source scan is clean for internal source-line tags, workspace paths,
  extraction macros, and placeholder/process markers.

## Recommended Next Step

Move to a top-level three-paper package checklist that records the current
status of Papers 1, 2, and 3 together, or choose a target venue and polish the
Paper 3 introduction accordingly.
