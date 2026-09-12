# A2 v25 active source and preservation manifest

Date: September 12, 2026.  
Branch: `revision/a2-v25-observable-calibration-signature-top4-2026-09-12`.

## Provenance

The branch was created from the latest located v24 review tip, `8129defd970bbc1e011bb480b70603d39a31324d`, on `review/a2-v24-external-harsh-top4-2026-09-12`. The reviewed v24 manuscript head was `c35b31b1924a1621374eab72ee60e4cb5ab37df5` on `revision/a2-v24-uniform-physical-global-top4-2026-09-11`.

The full native manuscript remains in the historical directory `papers/A2-v17-boundary-information-coarsening`. That directory name is a stable filesystem identifier, not the current article version. The active entry point is `main.tex`; the source-pinned companion entry point is `two_collision.tex`. The v25 article's main entry-point blob at completion of mathematical integration is `43f0acac5e8858df81e6c5c389f0c5adde05ac96`, committed at `358311409b44d052f428497bacbf347cdb2a1465`.

## Active replacements

| Previous active input | v25 active input | Purpose |
|---|---|---|
| `article/01_introduction_v24.tex` | `article/01_introduction_v25.tex` | Theorem hierarchy, explicit acquisition assumptions, long-even restriction and primary-literature comparison |
| `article/01a_protocol_scope.tex` | `article/01a_protocol_scope_v25.tex` | Correct old v20 references; distinguish same-table transfer, anchored scalar records and global position-sensor calibration |
| `article/23e_quantitative_gluing_stability_v24.tex` | `article/23e_signature_stability_v25.tex` | Finite analytic signature immersion and embedding, noisy unique matching, graph propagation and independent compact inverse modulus |
| `article/18c1_endpoint_time_deficiency_v24.tex` | `article/18c1_endpoint_time_deficiency_v25.tex` | Explicit bulk relative-density hypothesis, correct density token, corner-safe reverse kernel and two-sided deficiency |
| `article/25a_uniform_physical_global_v24.tex` | `article/25a_common_observables_v25.tex`, `article/25b_augmented_global_reconstruction_v25.tex`, `article/25c_analytic_variation_bundles_v25.tex` | Common physical record, charged contact/onset calibration, mixed separator estimator, growing-order reconstruction and separately specified local variation bundle |
| `v5/references_v18.tex` | `v5/references_v25.tex` | Retain all previous bibliography keys and add Meister--Reiss |

All previous files in the left column remain in the branch as historical sources. Their superseded claims are not also compiled into the active article. The new one-flight comparison `article/29a_signed_one_flight_benchmark_v25.tex` is added after, rather than substituted for, `article/29_two_flight_benchmark.tex`.

## Principal active theorem dependencies

The relative law continues to use `01c_geometric_setup_v18`, `02_finite_results`, the v3 geometry/integration modules, the v4 boundary-layer module, the v5 differentiated operators and the operator/hyperbolic-coordinate/strict-margin modules. None of these proof sources is rewritten to obtain the new global conclusion.

The signed contact inverse remains `article/23a_signed_endpoint_rigidity_v22.tex`, supported by the two-contact and compatibility sections. Analytic continuation remains `article/23c_analytic_continuation_v23.tex`. Intrinsic gluing classification remains `article/23b_intrinsic_multichannel_rigidity_v23.tex`, and metric-free rank-two lattice recovery remains `article/23d_rank_two_lattice_recovery_v24.tex`.

The physical comparison remains `v6/10_experiment_transfer.tex` and `article/17_adaptive_experiments.tex`. The new global contact-frame pilot invokes those estimates with a declared parameter-independent acquisition map, rather than treating their parameterwise analytical coordinates as observations.

The local information chain retains the scalar boundary information, vector non-dominated/common-collar argument, anchored realization, fixed-window physical multirate theorem, full endpoint--time information, count--endpoint limit, intrinsic count geometry and compatible-rate modules. The complete endpoint critical, Abel stability, deautoconvolution and regularized-observation results remain active. The v25 Poisson deficiency section strengthens the stated dependencies and preserves the reverse-sampling argument.

The earlier conditional compactness bridge `article/25_analytic_global_bridge_v23.tex` remains active as a separate general principle with its own stated calibration assumptions. The new metric-free global theorem is proved using `thm:v24-global-modulus` in the v25 stability section and the actual capped policy in the v25 physical sections. It does not silently use the older metrized-lattice setup as an assumption for the new lattice-recovery result.

## Full auxiliary material retained

`article/99_auxiliary_compendium_v19.tex` remains an active appendix input, byte-for-byte unchanged. Its full input list remains active, including nonlinear information; contact rigidity; finite-jet stability; profile and Abel acquisition; profile calibration; critical, adaptive-critical, random-hazard and supercritical experiments; inverse and pairwise inverse calculations; three-amplitude, fixed-offset and minimax analyses; smooth remainder/envelope bounds; observable comparisons; self-calibration; coalescence and measurable reconstruction; count-only acquisition and lower bounds; fixed-bracket acquisition; marked and record-response results; circular calculations; and the original flux, geometry, threshold, record and consequence proofs.

`two_collision.tex` and its source graph are retained. No abbreviated smoke-test manuscript replaces either complete native entry point.

## New proof landmarks

`thm:v25-observable-calibration` gives the capped physical pilot. `prop:v25-test-implementation` gives the finite-test implementation bias. `lem:v25-augmented-separators` includes onset coordinates. `thm:v25-fixed-order-physical` gives a measurable finite-template estimator with a deterministic total preparation cap. `thm:v25-global-physical-reconstruction` proves uniform reconstruction while all flight numbers are even and their minimum diverges.

`thm:v25-finite-signature-embedding` proves the finite local/global embedding bounds, and `lem:v25-noisy-signature-match` proves genuine unique matching. `lem:v24-gluing-persistence` and `thm:v24-global-modulus` retain their interfaces but now have distinct justified proof routes.

`lem:v25-hermite-right-inverse` and `prop:v25-analytic-jet-bundle` construct the finite-rank compatible analytic variation model. `lem:v24-uniform-positive-design` is explicitly a theorem about that model, not the whole infinite-dimensional compact analytic class.

`prop:v25-one-flight-inverse` states the signed-support benchmark without asserting an unproved statistical ordering. `thm:v24-two-sided-deficiency` has the explicit bulk relative-density assumption and valid kernels on exceptional configurations.

## Verification artifacts and their scope

`tools/check_revision_v25.py` contains finite mathematical diagnostics, active-input/reference/citation checks, retained-bibliography checks and pinned-byte comparisons for central historical files. It uses explicit exceptions, not Python `assert` statements, for required checks. Its optional `--math-only` mode is deliberately different from a source-graph audit.

`diagnostics/v25-finite-checks.json` records the locally executed finite checks. The full native build utility `tools/build_submission.py` is retained. `.github/workflows/a2-v25-native-build.yml` requests both native entry points, ordinary/optimized diagnostics, source archives, LaTeX logs, page metadata and hashes at the workflow's exact source commit. Only an actually executed successful report can certify those products. See `VERIFICATION_V25.md` for what has and has not run.

This branch is an author revision for further review. It has not been merged into `main`, and it does not alter repository membership or branch-protection settings.
