# General Theta Foundations I — restart r1

**Acquired Geometry and Causal Resource Transfer**

Native manuscript: `main.tex`, with six native sections and `references.tex`.
This package was written anew from the canonical restart; it does not load, copy,
generate, or retitle the v96 manuscript. Its central theorem is `thm:main`.

Canonical branch: `foundation/general-theta-foundations-i-restart-2026-10-06`.
Canonical commit: `18000b21e4bfd89180ccb069e46ac0f21621f34d`.
Canonical root tree: `c52606e659e8b2dc89be671adc02c26224ddc4d0`.
The four controlling files at that commit remain controlling and unchanged.
This directory's status is an **author research submission for external review**,
not an independent referee endorsement or a journal-level novelty certification.

## Central contribution

An actual-mass/innovation-transport theorem derives a finite-label curve from
raw acquired chart weights and widths, rather than assuming optimal distortion.
The upper uses the same acquisition weights as the lower. Holds inject no new
rounding. Intersecting strata, mixed dimensions, atoms, and vanishing widths are
proved cases, not undeveloped interfaces. The filter and absorbing geometric
sensor are downstream raw-kernel verifications, not premises of the theorem.

The complete target has not been silently equated with this certified class:
unknown-kernel learning, unrestricted optimal exploration, expanding active
updates, and optimal total growing simulator/controller/clock resources remain
separate proof obligations. `SCOPE_AUDIT.md` records them. Historical-corpus
inspection in this pass was focused, not exhaustive; see `HISTORY_COVERAGE.md`.

## Build

Requirements: Python 3.10+, pdfLaTeX with amsart, Latin Modern, microtype,
geometry and hyperref, and Poppler `pdfinfo`.

```
python verify.py
python -O verify.py
python build.py --source-sha <exact-source-commit> --out /tmp/gtf-r1-build
```

`build.py` verifies the committed source manifest, references, labels, all native
TeX inputs, normal/optimized diagnostics, three compiler passes and a clean
independent rebuild. It writes only outside the source tree. The resulting
receipt binds the source inventory, source SHA, compiler, regression output,
PDF hash, page count and independent-rebuild hash. Tests are finite regression
checks and do not prove the continuum statements.

The publication workflow has an allowlisted new research branch and new revision
branch. It commits only `paper.pdf` and two evidence files, without force-push.
A distinct read-only job reconstructs the exact artifact commit and checks its
PDF and artifact-only diff. Its final-head receipt is a workflow artifact and
is not committed back into the head it verifies.
