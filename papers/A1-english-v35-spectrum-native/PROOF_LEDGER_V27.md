# A1 v27 proof ledger

This ledger supplements, rather than replaces, the reviewed ledger at `../A1-english-v26/PROOF_LEDGER.md` (blob `eafd84a35f01209c23adafc62c5b1fbb3ce6a2d3`). The complete v26 proof source remains unchanged at its original path. The principal entry point includes every formerly active proof module.

## Inherited proof chain retained in the principal manuscript

| Input | Retained role |
|---|---|
| `core/02_experiments`, `text/operational_model`, `risk_criteria` | Actual report evidence, loss definitions, finite retained label, and charged persistent history |
| `text/exact_information`, `core/03_transversality` | Exact predictive sufficiency and attained local coordinates |
| `text/analytic_inputs`, `text/collision_flags` | Positive pairings, bounded-format global covers and collision-uniform confluent coordinates |
| `text/collision_direct` | All-budget checkpoint estimates and the common causal realization |
| `text/collision_consequences` | Collision phases and persistent-bit inversion |
| `v25/graph_model`, `v25/adaptive_proof` | Independently capped graph profiles, fixed-order causal filters, product-coordinate density input and adaptive converse |
| `v26/selection`, `v26/capacity` | First-block subprobability bounds, unrestricted completion reports and visited-set separator capacities |
| `v25/graph_consequences`, `v26/phases` | Actual star experiment, analytic contact orders and finite phase envelopes |
| Native `companions.tex` and its closure | Historical/supporting proofs; retained as a full companion, not summarized away |

The cited regular-box, recovery and covering inputs are the reviewed source statements. This ledger does not describe the referee's acceptance of their technical core as an independent formal verification.

## New proof obligations and their discharge

| Label | Statement and assumptions | Main proof step | Source |
|---|---|---|---|
| `lem:v27-heavy` | One positive-mass complete trace for a fixed acquisition law | Select mass at least beta/v! before specifying M or a codebook; apply the unconditioned subprobability bound before trace restriction; use one boundary expectation | `v27/uniform_policy.tex` |
| `thm:v27-curve` | One deterministic order dominates a resolution-blind rule at every integer budget | The same selected trace supports every allocation/boundary lower bound; compare attained Leja products with volumes; take a uniform minimum over the finite allocation family | `v27/uniform_policy.tex` |
| `cor:v27-bits` | Simultaneous bounded-additive-bit domination | Invert the quantitative trace bound with separate edge caps; retain beta, recovery/density constants and factorial costs explicitly | `v27/uniform_policy.tex` |
| `thm:v27-menu` | Deterministic completeness for a fixed finite menu, including randomized pre-tape selection | Select one order for each fixed conditional acquisition law; a mixture has a component of probability at least 1/K; invert the resulting profile lower bound; use causal deterministic filters for the upper bound | `v27/policy_menus.tex` |
| `cor:v27-menu-regret` | Finite minimax characterization over any nonempty accuracy set | Uniform pointwise bit comparisons survive the supremum over accuracies and the finite order-set minimization | `v27/policy_menus.tex` |
| `cor:v27-contact-menu` | Leading analytic-contact-order law for reusable menus | Finite determinant contact expansions give a bounded remainder uniformly over a compact positive resolution interval; finite envelopes preserve that remainder | `v27/policy_menus.tex` |
| `cor:v27-two-configurations` | One-rule interval/endpoints coefficients and bounded excess for two configurations in the actual star | Evaluate all partition types; combine the finite-menu theorem with the existing positive 24-trial experiment | `v27/policy_menus.tex` |
| `prop:v27-density` | Full acquired posterior-mean law for the actual two-trial detector | Bayes formulas for both nonfailure atoms; invert the failure map; include command density and report evidence in the Jacobian calculation | `v27/evaluated_model.tex` |
| `prop:v27-exact-reduction` | Exact finite-M average-risk reduction to scalar quantization | Orthogonally project arbitrary query centres, clip to the support hull, use nearest-centre assignment, and condition on independent initial-order seeds | `v27/evaluated_model.tex` |
| `lem:v27-quantization` | Classical sharp scalar coefficient with finitely many atoms | Lower piecewise-constant densities, Voronoi/partition interval counts and Holder's inequality; upper midpoint allocations; assign finitely many atoms exact centres | `v27/evaluated_model.tex` |
| `thm:v27-sharp-constant` | Exact integral expression for the example's sharp average coefficient | Combine the actual density, exact metric factor 1/128 and classical factor 1/12; supply rational numerical-enclosure construction | `v27/evaluated_model.tex` |
| `prop:v27-certificate` | Complete same-model separator comparison | Compute beta and the weighted density H; use the actual recovery norm; include both internal visited sets; integrate capacities; show a completion failure halves the entire submeasure | `v27/evaluated_model.tex` |

## Information-model boundaries

The oracle superscript means that only the acquisition rule is granted full-history access and the decoder is granted a finite prefix. It is a lower-bound relaxation, never a free-memory upper implementation. The decoder has at most M centres once independent seeds and the finite prefix are fixed.

A resolution-blind acquisition law cannot read a budget-dependent predictive state or output. Merely giving one budget-dependent program a fixed name does not establish this hypothesis. Encoders may still change across budgets. The chosen deterministic order is common across the curve; a common codebook is not claimed.

A finite menu may choose its index using the calibration, accuracy and budget before observing any tape. Conditional member transition functions and seed laws remain fixed. Making that finite configuration persistent costs at most ceil(log2 K) bits; it supplies no continuous history channel.

The numerical separator comparison uses the original visited-set decoder on both sides. A prefix-decoder constant is not substituted into it. The average sharp-constant result is not identified with a maximum-tape sharp constant.

## Constants and degeneracies

All general comparison constants are for a fixed graph experiment, fixed priors and the admitted compact calibration family. They are uniform in calibration, predictive budget, fixed acquisition rule and accuracy; menu constants may also depend on fixed K. No bound uniform over an increasing number of vertices is asserted.

Zero determinant products contribute zero and are never inverted. Positive allocations have dimensions between 1 and the finite total attained cap. The bit inversion includes the zero allocation and each individual edge cap. The event mass has a uniform positive lower bound under the inherited first-block construction.

For the evaluated model, the exact inputs are beta=35/1024, H=177957/20480 and L^2=128. The complete separator coefficient is 1071875/12452637120528384. Its complete-word comparison is exactly half. The sharp coefficient is the integral expression in `thm:v27-sharp-constant`, not this separator coefficient.

## Executable checks and nonclaims

`diagnostics_v27.py` contains explicit rational checks and finite-envelope enumeration. The sharp coefficient is enclosed using monotonicity and integer cube-root intervals, not a floating-point quadrature certificate. The script is intended to produce byte-identical result JSON under ordinary and optimized Python. A result file records what was actually executed; source publication alone is not a test pass.

The general heavy-trace and menu theorems are proved in text, not verified by enumerating a finite collection of policies. The classical quantization lemma is not claimed as a new generic quantization theorem. The fully evaluated acquisition law and its application are the example-specific content.

`build_v27.py` records native two-volume TeX execution separately from arithmetic. Unresolved or unstable references prevent a compilation pass from being certified. PDF visual inspection is a further, separately recorded task. Historical author/referee test counts and earlier build records do not certify this revision.

## Editorial assessment

This ledger records proof obligations and their dependencies. It does not assign a journal acceptance decision or claim that adding a theorem or an evaluated constant automatically settles the referee's concern about significance.
