# A2 revision 94: intrinsic Newton geometry of the stochastic germ

**Branch:** `revision/a2-v94-germ-newton-stochastic-intersection-2026-09-19`.

**Controlling review:** v93 report at `7d5e9d80a6033399afe633da21b44e4d6f435a2f`, reviewing source head `2832f7a7060217f6c8110688b66b73b9b946d13a`. The new branch is based on that review commit, preserving the report and all inherited sources.

## Manuscript and response

The complete manuscript entrypoint is
`papers/A2-v17-boundary-information-coarsening/rigidity_v94.tex`.
Its main source is `article/v94/paper.tex`, relative to that paper directory.
The detailed response is `revisions/a2-v94/RESPONSE_TO_REFEREE.md`.

The main theorem is an intrinsic Newton law on the full admissible observation germ. Finite cluster-coefficient envelopes determine the exponent; a joint rescaled coefficient fibre determines the exact leading root-multiset diameter. An analytic-chart theorem composes the determinant with all relevant model jets. A cubic stochastic example has channel-rank loss, double and triple roots, a singleton exact spectral fibre, and a square-root intrinsic modulus despite a noninjective ambient coefficient Jacobian. The metric-transport theorem explicitly transports Hellinger/Fisher geometry under left-right changes. The new modulus is linked to the corresponding shrinking-observation-ball minimax exponent.

The new proofs are in `article/v94/germ_newton.tex`, `stochastic_intersection.tex`, and `metric_transport.tex`. All twenty-two inherited proof and bibliography modules remain active and unchanged in the appendices. The complete new input graph has twenty-seven TeX files; no earlier manuscript, report, or verifier is overwritten.

## Build and audit

```sh
python3 revisions/a2-v94/verify_a2_v94.py --receipt /tmp/a2-v94-exact-head.json
cd papers/A2-v17-boundary-information-coarsening
latexmk -pdf -interaction=nonstopmode -halt-on-error rigidity_v94.tex
```

The build requires NumPy, SymPy, latexmk, AMS/Latin Modern/microtype/mathtools/hyperref and the inherited TeX dependencies. The branch-scoped workflow `.github/workflows/a2-v94-native.yml` installs them and runs on every push, without a path filter. It checks the runtime HEAD, all source identities, inherited preservation, the complete native build log, and packages `a2-v94-exact-head-<actual SHA>`.

`SOURCE_MANIFEST.json` separates the controlling review and reviewed manuscript from runtime revision HEAD. Its own hash is excluded to avoid self-reference. The audit rejects changes or deletions to inherited paths and requires the exact active input graph.

## Verification status

Six finite symbolic/numerical diagnostic groups passed locally; the recorded output is `revisions/a2-v94/LOCAL_DIAGNOSTICS.json`. An eleven-page local typesetting check of the new core had no overfull boxes. That check omitted inherited appendices and consequently had unresolved inherited references; it is not the complete manuscript PDF or a full-source audit. See `revisions/a2-v94/LOCAL_TYPESETTING.md`.

The complete native result must be obtained from a successfully completed workflow for the delivered HEAD. Queued, incomplete, or failed runs must not be reported as a successful full build. Artifacts retained after failure may contain only diagnostics or logs. Finite tests are not formal proof verification, and the manuscript remains subject to independent mathematical review.
