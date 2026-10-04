# A2 v42: scalar collision laws

**Scalar collision laws and recognition of periodic dispersing billiards — Qian Qi**

This is a complete revision, not an erratum or a replacement topic. Compile
`main.tex` for the primary article and `companion.tex` for the retained technical
supplement. Both documents and their literal source dependencies are included.

The controlling referee report is the v40 report at
`24baf07cf2952668d61881c727cc6417e952c76e`, under
`reviews/a2-v40-external-harsh-top4-rereview-2026-10-04/`.
The immediately preceding author revision is v41 at
`d81e4053bfba1703c4086ea8f9c69ed32c3537b6`.
Version 41 had already answered the seven-point report; this revision preserves
that work and adds a direct signed-record acquisition theorem. It does not
invent a later referee report or claim that a human review has occurred.

## Current submission

- [Consolidated response to the controlling referee](V42_RESPONSE_TO_REFEREES.md).
- [Current source, proof and literature audit](V42_AUDIT.md).
- `core/30_linear_moment_acquisition.tex`: the new theorem chain.
- `core/24_measure_support.tex`, `core/25_nonsmooth_curvature.tex`,
  `core/26_finite_geometry_details.tex`, `core/27_moment_factor_details.tex`,
  `core/28_theorem_comparison.tex`, `core/29_supplement_interface.tex`:
  the complete retained responses on supports, curvature, finite geometry,
  positive factorization, literature, and supplement dependencies.

The exact inverse still uses two whole-plane mean fields for the fixed opposite
commands, one unknown stationary probability, and the same strict-convexity and
separation hypotheses. No angular sweep, shrinking command, second launch law,
or sensor has been added. Finite geometry, transportation recovery, prediction,
period recognition, finite-configuration recovery and the complete earlier A2
programme remain present.

The new linear prefix stops at the first exit from a certified outer polygon
of a complete expanded component. One bounded signed record uses two independent
fresh collision bits. All moments through degree n share the records. Conditional
moment acquisition with tolerance tau costs
`C tau^(-2) log(C(n+1)/delta)` attempted bits rather than visiting every fine-grid
node. The resulting joint bound retains `N_geom(c a_m,delta/2)` and the exponentially
small moment tolerance `a_m`; this is not a parametric-rate or minimax claim for
the joint inverse. A finite positive law still has at most `binom(4m+2,2)` atoms.

## Reproduction and evidence

The native entry point is `tools/qualify_v42.py`:

```sh
python3 tools/qualify_v42.py --expected-head "$(git rev-parse HEAD)"
```

It checks the committed source inventory, the frozen source manifest, preserved
historical trees, all v40 and v41 active labels and proof bodies, both finite
diagnostic suites in ordinary and optimized Python, the actual TeX input
closures, stable cross-document auxiliaries and clean final TeX logs. The
workflow is `.github/workflows/a2-v42-verify.yml`.

Successful execution produces `A2-v42-primary.pdf`, `A2-v42-companion.pdf`,
complete journal/repository source archives, source hashes, diagnostic logs,
build logs and a receipt bound to the exact commit. The evidence is available
in the GitHub Actions artifact for that commit, not inferred from an earlier
revision's successful run. `--development` explicitly does not qualify a remote
commit. `--freeze` only updates `V42_SOURCE_PINS.json` after editing.

The unprefixed historical audit/response documents, `SOURCE_PINS.json`, and
v41 tool names are retained as provenance from the preceding package.
`V42_SOURCE_PINS.json` and the v42 qualification receipt govern this revision.
The v41 validator's unchanged source-inspection helpers are imported explicitly;
its old publication entry point is not the v42 entry point.

## Independent review status

The specialist brief in `SPECIALIST_REVIEW_BRIEF.md` remains active. Add the
first-exit isolation, signed-record expectation, uniform quadrature for singular
laws and conditional failure-budget arguments in the new section to that brief.
Independent human proof review has not been performed or certified by this
revision. Finite diagnostics and successful compilation are source and finite
model evidence, not continuum proof certificates or physical sensor validation.
