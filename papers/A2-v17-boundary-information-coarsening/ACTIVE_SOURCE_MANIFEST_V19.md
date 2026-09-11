# A2 v19 active-source manifest

**Revision branch:** `revision/a2-v19-signed-endpoint-rigidity-2026-09-11`  
**Review base:** `review/a2-v18-independent-harsh-top4-2026-09-11`  
**Article entry point:** `main.tex`

This manifest is authoritative for v19. The containing directory retains the historical name `A2-v17-boundary-information-coarsening` to preserve the established source graph and Git history; the active version is determined by the revision branch, `main.tex`, and this manifest.

## Main theorem chain

1. `article/01_introduction_v19.tex` — v19 introduction and theorem hierarchy.
2. `article/01c_geometric_setup_v18.tex` — formal geometric setup, relative boundary theorem, v19 notation and centered-derivative clarification.
3. `article/01a_protocol_scope.tex`, `article/01b_observation_hierarchy.tex` — physical protocol and distinction between fixed-table coarsening and unknown-geometry inference.
4. Part I retained forward chain: `article/02_finite_results.tex`, `v3/10_geometry_action.tex`, `v3/20_integration.tex`, `v4/10_boundary_layers.tex`, `v5/15_differentiated_operators.tex`, `article/15_operator_comparison.tex`, `article/16_hyperbolic_coordinates.tex`, `article/16c_strict_margin.tex`, `v6/10_experiment_transfer.tex`, `article/17_adaptive_experiments.tex`.
5. `article/20_boundary_compatibility.tex` — general smooth scalar/profile inverse.
6. `article/23_two_contact_rigidity.tex` — retained even-contact coarsened inverse.
7. **`article/23a_signed_endpoint_rigidity_v19.tex` — new general signed-endpoint contact rigidity.**
8. `article/24_physical_image.tex`, `article/29_two_flight_benchmark.tex` — physical realization and finite two-flight benchmark.
9. **`article/18_boundary_information_v18.tex` — scalar logarithmic boundary information.**
10. **`article/18a_vector_boundary_information_v19.tex` — new vector LAN, efficient information/minimax theorem and unknown-geometry billiard application.**
11. `article/19_endpoint_critical.tex` — fixed-table endpoint critical experiment.
12. `article/21_abel_stability.tex`, `article/22_deautoconvolution.tex`, `article/28_regularized_observation.tex` — stable function-valued inverse and acquisition.

## Auxiliary compendium

`article/99_auxiliary_compendium_v19.tex` is the single appendix entry point. It inputs every retained auxiliary module that v18 previously listed directly in `main.tex`: historical nonlinear information, contact-rigidity checks, finite-jet stability, acquisition/calibration theorems, critical/adaptive/supercritical experiments, finite-dimensional and envelope minimax results, collision records and the original geometric/flux consequences.

This refactor reduces the visible entry-point complexity without deleting mathematical content.

## Bibliography

`v5/references_v18.tex` remains the compiled bibliography. The v19 literature verification is recorded separately in `LITERATURE_VERIFICATION_V19.md`; the active article claims are deliberately limited to results proved in the manuscript.

## Revision evidence

- `HISTORICAL_DERIVATION_AUDIT_V19.md`
- `PROOF_LEDGER_V19.md`
- `LITERATURE_VERIFICATION_V19.md`
- `RESPONSE_TO_REFEREE_V19.md`
- `VERIFICATION_V19.json` once execution/build evidence is recorded

Older files such as `README.md`, `PROOF_LEDGER.md`, `VERIFICATION.json`, `SOURCE_PINS.json`, `HISTORICAL_DERIVATION_AUDIT_V18.md` and `LITERATURE_VERIFICATION_V18.md` are preserved as historical revision records. They are not the authoritative v19 status documents unless explicitly incorporated above.

## Preservation rule

No reviewed v18 mathematical source is deleted. Files overridden by v19 are limited to the active entry point and referee-identified notation/narrative files; the predecessor versions remain recoverable exactly from the review-base commit and Git history.
