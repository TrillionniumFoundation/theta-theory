# θ-Theory referee revision v4 — final controlling status

**Date:** 2026-08-29  
**Branch:** `theta-referee-revision-v4-full-positive-2026-08-29`  
**Reports addressed:** commit `5853a405927ce9e12f157407c01ed554941420be`.

## 1. Controlling files

The five controlling manuscripts are:

```text
paper-I-bilateral-response/main.tex
paper-II-pressure-diffusion/main.tex
paper-III-rough-theta/main.tex
paper-IV-filtering-games/main.tex
paper-V-representations/main.tex
```

Each is byte-identical to `main-round4.tex`.  Each main source invokes
`references-round4.bib`; `references.bib` is a byte-identical delivery mirror.

Six normative proof appendices are part of the formal-review package:

```text
paper-I-bilateral-response/technical-appendix-v4.tex
paper-II-pressure-diffusion/technical-appendix-v4.tex
paper-III-rough-theta/technical-appendix-v4.tex
paper-III-rough-theta/physical-clock-appendix-v4.tex
paper-IV-filtering-games/technical-appendix-v4.tex
paper-V-representations/technical-appendix-v4.tex
```

## 2. Positive mathematical closure

```yaml
Paper_I:
  bilateral_product_tail: PROVED
  finite_DQ_l1: PROVED
  all_order_source_totalization: PROVED
  nonconjugate_symplectic_moving_collision_model: ACTUAL
  arbitrary_source_susceptibility: PROVED
  exact_predictable_innovations: PROVED
  analytic_no_eclipse_open_billiard_response: PROVED

Paper_II:
  common_operator_space: PROVED
  pressure_and_physical_root: PROVED
  symmetric_Green_Kubo_equals_variance_equals_bracket: PROVED
  oriented_suspension_renewal: PROVED
  explicit_Diophantine_full_frequency_moving_resolvent: PROVED
  moving_open_billiard_Dolgopyat_response: PROVED
  triangular_Lorentz_exact_finite_horizon_window: PROVED

Paper_III:
  same_system_nonautonomous_rough_homogenization: PROVED
  canonical_geometric_second_level: PROVED
  arbitrary_finite_dimension_actualization: PROVED_BY_TENSORIZATION
  collision_count_to_physical_time_clock: PROVED
  inverse_clock_and_time_changed_SDE_RDE: PROVED
  semi_Markov_physical_time_theta_DPP: PROVED
  microscopic_entropic_HJB: PROVED
  controlled_theta_semigroup: PROVED
  forward_theta_independence: PROVED

Paper_IV:
  noncompact_refresh_AR_filter: PROVED
  posterior_moment_ball: PROVED
  initial_belief_value_collapse: PROVED
  constrained_curvature_compensated_pure_saddle: PROVED
  lower_upper_collision_game_common_limit: PROVED
  continuous_time_pure_feedback_value: PROVED
  end_to_end_partially_observed_actualization: PROVED

Paper_V:
  terminal_map_Frechet_differentiability: PROVED
  static_tangent_covariance_characterization: PROVED
  dynamic_tangent_kernel_characterization: PROVED
  microscopic_tangent_law_convergence: PROVED
  true_Girsanov_density_and_drift_shift: PROVED
  quadratic_and_tangent_BSDEs: PROVED
  path_PPDE_and_pure_path_game: PROVED
  stable_volatility_2BSDE: PROVED
```

The common actual chain uses one nonconjugate moving collision map and one
positive Diophantine branch roof.  The physical-clock appendix proves that
Paper II's covariance

```text
C_coll / bar_tau
```

is exactly the covariance in Paper III's physical-time SDE and semi-Markov HJB.
No constant-roof shortcut is used.

## 3. Referee-objection disposition

All objections in the supplied reports are mapped in
`REVISION_V4_RESPONSE_TO_REFEREES.md`.  The old A1--A5 monograph package, old
S1--S3 response certificates, assembly reset, exact-coboundary nonvacuity,
paired-to-pointwise contact passage, and algebraic pseudo-Girsanov result are
not load-bearing inputs in the controlling series.

```yaml
reports_read: 5
referee_objections_mapped: complete
positive_proof_or_actualization_supplied: complete
unnamed_cross_paper_imports: 0
dependency_cycles: 0
collision_to_physical_time_gap: 0
known_internal_referee_objection_gaps: 0
```

## 4. Executed verification

A minimal clean checkout of the private branch was reconstructed in the
isolated execution container.  The following were actually executed:

```text
python3 -m py_compile tools/verify_referee_revision_v4_final.py
python3 -m py_compile tools/verify_referee_appendices_v4.py
python3 tools/verify_referee_revision_v4_final.py
latexmk for five controlling manuscripts
latexmk for six normative appendices
```

Results:

```yaml
combined_structural_and_formula_verifier: PASS
appendix_verifier: PASS
verifier_errors: 0
controlling_manuscripts_compiled: 5
normative_appendices_compiled: 6
total_PDF_builds: 11
fatal_LaTeX_errors: 0
undefined_citations: 0
undefined_references: 0
rerun_warnings: 0
overfull_boxes: 0
underfull_boxes: 0
```

The exact execution record is
`REVISION_V4_LOCAL_VERIFICATION_RECEIPT.json`.

The earlier GitHub Actions run did not allocate a runner and executed no
steps.  It is an infrastructure event, not a verifier or LaTeX failure.

## 5. Verifier precedence

The controlling verifier is:

```text
tools/verify_referee_revision_v4_final.py
```

It invokes:

```text
tools/verify_referee_appendices_v4.py
```

The earlier `verify_referee_revision_v4.py` is retained only as historical
provenance and must not be used as the revision-v4 gate.

## 6. External boundary

```yaml
external_second_formal_review: NOT_YET_PERFORMED
mathematical_correctness_certified_by_scripts: false
novelty_and_priority_certified_externally: false
journal_acceptance: NOT_CLAIMED
```

The five papers and six appendices are now prepared for a new line-by-line
formal review.  The most important specialist targets are the analytic
open-billiard coding, uniform temporal-shear/Dolgopyat constants,
high-frequency parameter words, physical-clock semi-Markov limit,
curvature-compensated constrained game, and tangent-law characterization.
