# A2 v135 — structural support proof and reconstruction article

Branch: `revision/a2-v135-structural-support-proof-2026-09-23`.

Controlling review: `reviews/a2-v134-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md` at `a08b157800c27c0f73f0c5c9a52155265ef4f395`.
Reviewed published v134: `74b1aa9ffb95557f63e993e428a22e491a1edd0f`.

## Referee reading objects

All manuscript files are in `papers/A2-v17-boundary-information-coarsening/article/v135/`:

- [Focused reconstruction article](papers/A2-v17-boundary-information-coarsening/article/v135/geometry.pdf), with the complete load-bearing smooth-locus proof.
- [Technical supplement](papers/A2-v17-boundary-information-coarsening/article/v135/supplement.pdf), retaining the full boundary, primary-specialization, ambient-pencil and exact-certificate material.
- [Complete combined manuscript](papers/A2-v17-boundary-information-coarsening/article/v135/complete.pdf), without deleting inherited mathematical results.
- [Response to the v134 report](papers/A2-v17-boundary-information-coarsening/article/v135/RESPONSE_TO_REFEREE_V134.md).
- [Literature audit](papers/A2-v17-boundary-information-coarsening/article/v135/LITERATURE_AUDIT_V135.md) and [issue matrix](papers/A2-v17-boundary-information-coarsening/article/v135/ISSUE_MATRIX.json).
- [Source provenance](papers/A2-v17-boundary-information-coarsening/article/v135/PROVENANCE_MANIFEST.json) and [executed build receipt](papers/A2-v17-boundary-information-coarsening/article/v135/evidence/BUILD_RECEIPT.json).

Each PDF has its complete editable LaTeX driver and inputs in the same directory.

## Mathematical changes

Standalone arbitrary-degree shear descent handles noncancellation, weight projection, multiple radical directions and determinant twists. A full SO4 decomposition proves the absence of the determinant character in the contraction target. The exact all-ranks kernel theorem is retained. A new reduced-support-pullback proposition identifies the support 4, 7/8 and 9 inverse images and excludes all quartics with at least three essential variables from the closed second Grassmannian secant variety. The residual involution is proved over the actual determinantal rank-one scheme, including nonreduced bases. Fitting ramification is explicitly restricted to the quasi-finite part when that terminology is used.

The conclusion remains reconstruction on **every** basepoint-free smooth-Jacobian web, with no additional genericity open. All 241 inherited mathematical labels remain compiled. Accepted readout and common-g proof files remain byte-identical.

## Documentary status and reproduction

The complete Ballico 1993 theorem-level comparison remains **open**; neither anticipation nor nonanticipation is inferred from metadata. No exhaustive novelty clearance, formal machine proof, complete ambient boundary classification, or journal acceptance is claimed.

Run `python revisions/a2-v135/unpack.py`, `python revisions/a2-v135/assemble.py`, and `bash papers/A2-v17-boundary-information-coarsening/article/v135/build.sh` from the repository root. The branch-specific workflow verifies transport, assembles immutable source, executes all ten exact scripts, compiles three PDFs, verifies preservation, and publishes the expanded sources and evidence **only on this branch**. Its receipt records actual executed status and page counts; this index alone does not assert a successful run.
