# Historical derivations and dependency audit

## Fixed material used in the revision

| Edition | Immutable commit | Use |
|---|---|---|
| Latest GTF I v1 review | `01d3e78bd40985651f5b4ff24364e1dba5d481f0` | Complete report and review manifest; base of the new revision branch. |
| Reviewed v1 source edition | Review base's complete `papers/GTF-I-v1` tree `3657060e29726178c0fd26deeda3c36f9a9f86ee` | Original definitions, physical checkpoint loss, causal emulation, refreshing posterior Jacobian, all proofs and boundary examples. Copied exactly to `legacy/`. |
| A1 v37 | `90465076589f5e5c69227d624f278c47744f1c1d` | Anisotropic G/A/C transfer, bounded-format covering, reachable updates, prior causal and resource comparisons. Complete tree copied to `source-editions/A1-v37`. |
| A2 v112 | `0c696736e6ec22259c730672f61ebd8ef0d95460` | Physical contact-ray statistics, nuisance profiling, Poisson comparison, score compression, and finite precision. Complete tree copied to `source-editions/A2-v112`. |
| Historical eleven-paper pipeline | `c04845b6613208406703695c9c184ae461f95805` | `ROUND13_PROOF_DEPENDENCY_LEDGER.md`, earlier paper interfaces, and the historical main baseline. Preserved in branch ancestry and existing paths. |

The preserved master outline is `foundations/general-theta/General_Theta_Foundations_v0.1.md`, together with `GTF_I_IMPLEMENTATION_2026-09-22.md`. The original outline's SHA-256 is `172fac13578c2900870b5bebe115cfb2b774709920b0b69970db511d5c29191a`. It fixes the T01--T12 foundation and G1--G4 program distinction. The revision supplies new quantitative G1/G2/G3 results with their own hypotheses instead of treating the outline as proof evidence.

## Load-bearing source comparisons

The direct source comparison concentrated on the following mathematical chains, not on build badges or a count of historical revisions.

A1's `sections/causal_transfer.tex` already has the anisotropic profile, acquired rectangular subprobability, global bounded-format geometry, and a reachable-state causal recurrence. Its `text/analytic_inputs.tex` supplies the geometric covering estimate. The main/companion architecture and `v36/comparison.tex` distinguish acquisition geometry from classical interpolation and quantization inputs. The `v30/predictable_networks.tex` development concerns predictable finite layered acquisition networks; it is not silently identified with an infinite-time random-filter contraction theorem. The new paper recovers A1's transfer as Corollary 2.2 and states the additional infinite-horizon hypotheses separately.

A2's `parts/04-statistical-experiments.tex` contains the physical local experiment, quadratic-contact amplitude scale, nuisance projection, quantitative Poisson-to-Gaussian comparison, and the finite-precision score reduction. Its noise meanings matter: an independently noisy measurement of a feature is not the same statistical experiment as a feature of raw observations. The new paired Gaussian theorem is proved directly, with an unrestricted nuisance, and is compared with A2 at the level of the stated rate rather than asserted equivalent to the entire A2 experiment.

For GTF I v1 the central chain is physical terminal loss -> acquired posterior law -> actual Jacobian -> small-ball obstruction, and admissible domain -> same-input stability -> one finite-label machine. The revision keeps that chain but replaces the strong-refresh stability argument for its new application by an explicit projective one. The original theorem and proof remain unchanged in the appendices.

## Original acyclic pipeline

```text
A1 independent
A2 -> A3 -> A4 -> C2 -> D1
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1
```

| Edge | Mathematical content retained from the historical ledger | Relation of this revision |
|---|---|---|
| A2 -> A3 | Parent-bundle vector/count/roof pressure and deterministic-clock coefficients | No substitution of finite-label error for the required spectral/coefficient theorem. |
| A3 -> A4 | Actual Markov-renewal kernel, exponential moments, terminal residual | No renewal or random-time LDP inferred from a filter norm bound. |
| B2-GC -> B1 | Complex particle/contact pressure and canonical polymer derivatives | No microcanonical conclusion imported backward. |
| B1 -> B2-MC | Exact-number source-dependent shell coefficient | The source dependence remains a separate requirement. |
| B2-MC -> B3 | Joint density/contact LDP, balance graph, microscopic marked cumulants | Covariance is not defined through an assumed inverse action. |
| B3 -> B4/C1/C2 | Joint covariance and process tangent on the collision-space dual | The finite-state theorem does not identify that dual or prove its process limit. |
| B4 -> C1 | Kinetic Nisio semigroup and compact dynamic-action sublevels | Predictive-state sufficiency is not assumed to prove its own reduction. |
| A4/B4/C1/C2 -> D1 | Already established component laws and typed contractions | Spectral projection does not create labelled phases. |

The new usable conclusions are the acquired-law/suffix theorem, conditional block stability, positive/intermittent HMM applications, a matched measured-calibration contact experiment, and an unrestricted control comparison. An application to a legacy model must establish that model's state domain, actual acquired measure, physical readout, and required stability. Nothing in the revision removes those obligations or marks them proved because an interface is well typed.

## Scope of the historical audit

The full fixed source editions and the original repository history are preserved for further review. The load-bearing comparisons above were read to guide and check this revision. Preservation of a complete historical edition is not a claim to have independently re-proved every theorem in every one of its historical files. The source tree identities and source hashes establish which mathematical editions were used; they do not establish mathematical correctness.
