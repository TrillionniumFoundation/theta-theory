# A1 v34 — proof and scope ledger

Baseline manuscript: `e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c`. Controlling review: `7643c3532ea9f70eaa3010cd13abcb58c1c31a8f`. This ledger is a reading map, not a proof certificate.

| Statement | Source and dependencies | Scope / disposition |
|---|---|---|
| `thm:resolution-main` | `text/main_classification.tex`; checkpoint and streaming theorems | Unchanged: all integer budgets and all calibrations in the fixed compact chamber; fixed full-support prior, detector and horizon |
| `lem:binomial-tangent`, `thm:rank`, `thm:causal` | `core/03_transversality.tex`; explicit product tangent, mixed positivity, normalization, local section and causal changeover | Unchanged exact acquired rank and minimal continuous state; not an arbitrary nonmonomial dimension formula |
| `lem:newton-attainment` | `text/collision_flags.tex`; full confluent pairing, compact derivative bounds, actual failure evidence | Unchanged acquisition-mass theorem; singular latent priors allowed; not supplied-box quantization |
| `lem:tame-rectangle`, `thm:intrinsic-checkpoint` | `text/analytic_inputs.tex`, `text/collision_direct.tex`; classical real entropy plus bounded format | Unchanged whole-image bound, acquired-dimensional truncation and matched unconditional converse |
| `thm:intrinsic-streaming` | `text/collision_direct.tex`; reachable raw moment updates and finite-horizon error recurrence | Unchanged one common per-report transducer; no past history or persistent public seed supplied |
| `cor:intrinsic-bits`, `thm:collision-tree`, `cor:two-parameter` | `text/collision_consequences.tex`; determinant law, collision orders and cluster allocation | Unchanged consequences, made more prominent; not new v34 discoveries |
| `prop:v34-blackwell` | `v34/moment_controllers.tex`; direct channel integration and common submeasure | New explicit identification and proof in the article; classical Blackwell framework is credited |
| `thm:v33-moment-program` | `v34/moment_controllers.tex`; realizable one-step matrices, conditional independence, centroid identity, compactness | Extended to arbitrary standard Borel latent spaces, nonnegative Borel cells, prescribed independent commands; zero evidence included |
| `prop:v34-evaluation` | `v34/moment_controllers.tex`; sum-to-one padding and multiplication | New explicit generality boundary: cell-product algebra evaluates to `W_(mA)` in the monomial case, but does not imply attainment |
| `prop:v34-two-cell` | `v34/moment_controllers.tex`; two-valued cells and nonzero posterior derivative | New positive nonmonomial illustration; one-dimensional image for menus with a distinguishing future query |
| `lem:v33-purification`, `thm:v33-pure` | `v34/moment_controllers.tex`; classical finite-action finite-moment purification | Complete proofs retained at finite-cell scope; atomless command laws; mean-risk vector only |
| `thm:v33-polyhedral` | `v34/moment_controllers.tex`; affine single-time-state replacement | Complete proof retained; scalarized risks only; explicit atomic tie partition `eq:v34-ties` |
| `thm:v33-collision` | `v34/moment_controllers.tex`; positive compact monomial family and compact minimization | Retained fixed-M limit theorem; all-budget scale is separately imported from `thm:resolution-main` |
| Finite compatibility, arbitrary precision, exact continuous-command example | `v33/finite_compatibility.tex`, `v33/precision.tex`, `v33/exact_instance.tex` | Unchanged proofs, retained in main; the N=2 example does not settle multi-checkpoint allocation |
| Complete companion development | `companions.tex` and its inherited inputs | Unchanged, not independently re-audited in full during this revision |

## Classical results versus current contribution

The main comparison now explicitly attributes the interpolation and positivity framework, real entropy estimates, quantization/filtering error recurrence, Blackwell postprocessing interpretation and DWW purification. The main theorem's experiment-level content is the combination of attained tangent, simultaneous acquired mass in confluent flags, whole-image cover and common causal realization with collision-uniform constants. The general finite-cell formula is realization algebra, not an alternative proof of that geometry.

## Historical sources actually consulted

The preparation read the controlling v33 referee report; the complete current main entry, introduction, main classification, transversality, analytic inputs, collision flags, direct collision proof, collision consequences and controller module; the current comparison and bibliography; the companion entry; and the inherited `sections/filter_quantization_comparison.tex` and `sections/comparison.tex`. It also inspected the native build wrapper and builder and the review audit record. This is a targeted revision audit, not a claim that every proof on every historical branch was reread or independently certified.

## Verification boundary

`v34/verify_revision.py` checks finite exact arithmetic with explicit exceptions and exercises three acquisition stages; those are consistency tests of specified controllers, not optimization. `v34/smoke_test.py` validates changed-module TeX with explicit external stubs. The complete native two-volume build and a formal proof-assistant verification were not executed in this session. See `VALIDATION_V34.json`.
