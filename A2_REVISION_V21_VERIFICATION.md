# A2 revision v21 verification record

## Canonical manuscript source

`672b159ef204ba75a63ab92a4d52ae3960304337`

This commit contains the final v21 theorem-source changes selected by
`papers/A2-v17-boundary-information-coarsening/main.tex`.  The root-level
manifest and this verification file were added afterwards and do not modify
that manuscript source.

## GitHub Actions verification

Workflow:

`.github/workflows/a2-v21-native-build.yml`

Workflow run for the canonical source:

- run id: `34592462690`
- first job id: `103240651306`
- first conclusion: `failure`
- first job steps: empty (`steps=[]`)
- decoded job logs: unavailable because no job log blob was created

A single explicit rerun was made to distinguish a transient queue failure from
persistent infrastructure unavailability:

- rerun job id: `103240788823`
- rerun conclusion: `failure`
- rerun steps: null / no executed steps
- rerun logs URL: null

The original attempt completed approximately two seconds after entering the
queue.  Neither attempt executed checkout, dependency installation, the native
build driver, Python diagnostics, LaTeX, reference checking, or artifact
upload.  Therefore these failures are **not evidence of a TeX or manuscript
failure**, but they are equally **not a successful native-build certificate**.

The same zero-step failure mode is present on the preceding v19 exact head
`837d785dc92c22253aa8809e32d97dd6579aef3c`, whose native-build check also
completed in roughly two seconds before any job step.  This cross-version
observation is consistent with a current repository/account GitHub-hosted
runner infrastructure problem rather than a v21 source regression.

## Local execution availability in this session

The working container has `pdflatex`, `latexmk`, and `chktex`, but outbound DNS
to `github.com` is unavailable.  A direct clone of the private/current branch
therefore could not be materialized into the container for a faithful full
native build.  No local full-PDF success is claimed.

## What has been verified directly

- The v21 branch forks from the exact latest review head
  `a0dfdc85ba8fa6a0908a5b167deb563a085042e4`.
- The controlling review branch differs from the reviewed v20 revision only by
  the new referee report.
- `main.tex` selects the v21 introduction, signed inverse, non-dominated vector
  theorem, anchored physical realization and fixed-window physical experiment.
- The earlier v19/v20 theorem modules remain present as historical provenance
  and have not been deleted.
- The v21 workflow YAML is accepted by GitHub sufficiently to create the
  workflow run and `native-build` job; the failure occurs before a runner
  begins executing its steps.
- The point-by-point response and revision manifest identify every required
  referee repair and its controlling source statement.

## Verification status for the next referee

### Mathematical/source repair status

`implemented in revision source`

for R20-1 through R20-6 and all associated smaller comments addressed in
`RESPONSE_TO_REFEREE_V21.md`.

### Native CI certificate status

`BLOCKED — GitHub-hosted job never started; no runner execution`

This status should be changed to `passed` only after the exact canonical
manuscript source is executed by a real runner through the complete native
build workflow.  No weaker smoke test or zero-step check should be used as a
substitute.
