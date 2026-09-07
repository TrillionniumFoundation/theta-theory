# Proof hierarchy for A1 v21

This ledger separates mathematical dependence from source preservation.
All page numbers below refer to the 114-page local three-pass build; stable
source labels are controlling if pagination changes in another TeX setup.

## Principal theorem and its minimal route

Theorem `thm:resolution-main` is the single main statement. Its printed
statement is unchanged. The proof in
`sections/collision_transfer_application.tex` verifies the hypotheses of
`thm:causal-transfer`; it does **not** invoke
`thm:intrinsic-checkpoint` or `thm:intrinsic-streaming`. Those two direct
proofs remain in Appendix D as complete alternative routes.

1. `core/02_experiments.tex` and `build/operational_model.tex` fix the actual
   detector, commands, report probabilities, delayed physical queries and
   persistent-label resource. `core/03_transversality.tex` supplies the
   mixed-moment positivity and actual binomial product tangent.
2. `sections/classical.tex` and `build/analytic_inputs.tex` establish complete
   Hermite-prefix independence, confluent positivity and the whole-image
   thin-rectangle cover. The entropy inequality and bounded-format component
   inputs are explicitly attributed to their classical/primary sources.
3. `sections/causal_transfer.tex` proves `thm:causal-transfer` from global
   geometry (G), actual acquired mass (A), and causal compatibility (C).
   It includes arbitrary integer stage budgets and the complete propagated
   error sum. `lem:positive-remaining-update` proves (C) from positive
   finite remaining-test closure, including dependent tests.
4. The first part of `core/06b_collision_geometry.tex`, generated as
   `build/collision_flags.tex`, proves `lem:leja-scales` and
   `lem:newton-attainment` without assuming a nonzero collision gap.
5. `sections/collision_transfer_application.tex` constructs the full
   invertible ambient change T from the active Newton block, checks (G)
   for the complete rational image, obtains every prefix mass in (A) from
   the actual all-failure subprobability, and checks raw updates in (C).
   This directly proves the main theorem. The inherited bit law, tree
   formula and intersecting-collision calculation follow immediately.

## Additional proved results and their scope

| Source label | Role | Proof mechanism | What is not inferred |
| --- | --- | --- | --- |
| `thm:causal-transfer` | Reusable checkpoint-to-causal implication | Global reachable covers, unconditional rectangle lower bound, representative update and quantization recurrence | Does not assume all positive experiments satisfy the geometry hypotheses; no unbounded-horizon constant |
| `lem:positive-remaining-update` | Gap-free causal hypothesis | Bayes quotient on posterior-mixture segments with positive evidence | No geometric lower bound is supplied by positivity alone |
| `lem:dimension-free-feasibility` | E20.1 repair | Separation of a finite moment body, full-support mixture and atomic representation | Feasibility is annihilation, not an exact-kernel claim |
| `prop:finite-matroid-rank` | E20.2 classical specialization | Cauchy–Binet, distinct monomials and positive-orthant nonvanishing | Not new linear matroid intersection; not the constrained compact-space case |
| `prop:square-moving-kernel` | Referee's explanatory stress example | Exact pairing, varying kernel and physical covariance | Not a counterexample to the correct exact-kernel criterion |

The exact-kernel theorem `thm:exact-kernel` keeps every substantive
hypothesis and conclusion. Only the named feasibility citation and the
corresponding proof paragraph change, exactly as listed in
`REVISION_EDITS.json`. The local chart, generic-minor nonvanishing,
bounded-density witnesses, forced-kernel closure and balanced-block
classification remain intact.

## Complete appendices

A: structural rank classification, moment strata and one-step covariance.
B: dimension-free feasibility, universal square and rectangular pairing
criteria, exact kernels, finite comparison, moving kernels, positive-history
mass and covariance degenerations. C: circular contrast, operational inverse,
directional and common-moment ambiguity. D: direct collision checkpoint and
causal proofs, confluence, finite-state streaming and affine attainable
filtration. E: observation algebra, uniform resolution, sequential value and
common-risk arguments. F: numerical construction, certified resource,
stability and request-conformance results. G: precise classical-input and
neighboring-problem comparisons.

## Executed preservation standard

The published sibling's manifest is pinned independently of the new manifest.
All 729 prior source files are verified before any historical preparation
script is run. Of 114 old proofs and 117 old statements, 113 proofs and
116 statements are byte-identical in the complete compilation. The remaining
proof and statement match the exact registered E20.1 correction, not a
whitelist of arbitrary changes. All 347 old labels are present, and source
references and bibliography keys resolve. An actual mutation of the original
operational inverse must be rejected by `build.py --prepare-only` without
relying on `validate.py` or merely regenerating the current manifest.

These checks establish identity, inclusion and reference integrity. They do
not verify analytic proofs or determine editorial importance.
