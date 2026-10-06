# Proof ledger

Every formal result has a full proof in the native manuscript. “Proved” denotes the supplied mathematical argument, not external certification. Finite tests do not establish these results.

## `lem:factor` — Measurable factorization with completed histories

Source: `sections/01_experiments.tex`. Dyadic Borel versions under completion, countable coordinate combination and Borel target correction; standard tool with explicit proof.

## `prop:quotient` — Predictive realization and pointwise update descent

Source: `sections/01_experiments.tex`. Event instruments -> equal measures -> continuous densities -> pointwise normalized fibres; compact quotient maps; lem:factor.

## `thm:main` — Causal acquired geometry and kernel-derived resource transfer

Source: `sections/02_theorem.tex`. lem:projection + lem:geometry + lem:transport; thm:kernel supplies T under K; report maximal coupling. No realization dependency.

## `lem:projection` — Checkpoint projection

Source: `sections/03_proofs.tex`. Conditional square-loss decomposition; eliminate decoder/encoder randomization by convexity and nearest centers.

## `lem:geometry` — Actual anisotropic mass and allocation

Source: `sections/03_proofs.tex`. Width-adapted finite grid; actual conditional small-ball union bound; separated-center allocation including discarded components.

## `lem:transport` — Innovation transport

Source: `sections/03_proofs.tex`. Pathwise nonnegative recurrence unrolling and Minkowski; no independence assumption.

## `prop:mechanisms` — Three kernel-level mechanisms

Source: `sections/03_proofs.tex`. Uniform contraction, event-indexed contractive holds, and disjoint absorbing-overwrite indicators, all re-proved.

## `cor:crossing` — Intersecting strata

Source: `sections/03_proofs.tex`. Use all centers in each conditional small-ball lower; compare equal allocation to Psi; no inverse separation.

## `thm:kernel` — Forced moment resolvent from a raw-kernel factor

Source: `sections/04_kernel_transport.tex`. Exact reverse-edge conditional moment recursions, two positive Neumann resolvents, PSD limiting Gram matrix; dominated preparation; weight-normalized cone bound.

## `cor:finite-kernel` — Finite-state check and recurrent expansion

Source: `sections/04_kernel_transport.tex`. Weighted sup norm and Neumann vector; explicit reversible two-state expanding calculation.

## `prop:suspension` — Exact suspension preserves the forced profiles

Source: `sections/04_kernel_transport.tex`. Held stationary edge mixture; cancel theta in first and second forced fixed-point equations; theta=0 seed separately.

## `thm:morphism` — Typed resource and common-risk composition

Source: `sections/05_resources.tex`. Legal lift inclusions, causal microsteps/stopping, complete-law TV contraction/triangle, all-coordinate cost map and common bounded loss.

## `thm:tag` — Mandatory-state separation and total-memory resolution

Source: `sections/06_minimax.tex`. Condition on independent seed; disjoint positive-probability state supports under exact challenges; allocation lower and product upper.

## `thm:robust` — Joint acquisition--resolution--precision minimax law

Source: `sections/06_minimax.tex`. One eight-member family; uniform-prior projection; actual failure and acquired geometry; compulsory cells; direct bit-erasure floor; finite-bit grid upper and explicit feasible costs.

## `prop:floors` — Exact erasure deficiency and the two elementary floors

Source: `sections/06_minimax.tex`. TV source distance 1-theta and triangle prove deficiency>=theta/2; fair imputation matches; posterior variance proves score floors.

## `thm:hmm` — Filtering realization

Source: `sections/07_realizations.tex`. Raw Bayesian update, compact logit contraction, actual report Jacobian density, TV continuity; exact/finite-bit distinction.

## `thm:sensor` — Stratified acquisition law through rank collapse

Source: `sections/07_realizations.tex`. Raw acquisition mass and variance, glued mixture quotient with continuous density versions, disjoint overwrite indicators, crossing-chart bound.

## `thm:recurrent` — Acquired geometry under recurrent expanding updates

Source: `sections/07_realizations.tex`. Paid initialization, actual density through fold/refresh, report continuity, independent gains and explicit resolvent; width collapse.

## `lem:initialization` — Paid initialization and continuation

Source: `sections/A_algorithms.tex`. Concatenate a paid legal initializer and continuation; apply all bounds to their joint actual law; include terminal call in full ledger.

## Cross-cutting audit

General proofs do not invoke any realization theorem. The kernel theorem is proved from one-step operators before application, despite its forward reference in the central theorem. Zero weights, rank zero, paid initial observations and the terminal call are explicitly handled. The robust lower uses the exact same baseline in every member. The erasure simulator cannot read a terminal answer early. The full-complexity gaps remain in SCOPE_AUDIT.md.
