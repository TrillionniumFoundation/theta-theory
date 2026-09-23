# A2 revision 137 — intrinsic coefficient reconstruction

**Intrinsic reconstruction from nonreduced failure schemes** — Qian Qi.

Branch: `revision/a2-v137-intrinsic-coefficient-torelli-2026-09-23`.
Controlling report: `reviews/a2-v136-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`, commit `d15c9bcabdfc31070b773e2c8014601e75d4e641`.
Reviewed manuscript head: `731729b9e391b507d27994f6db8d71d61cfca577`.

## Manuscript and referee materials

All new native sources and PDFs are in `papers/A2-v17-boundary-information-coarsening/article/v137/` after the branch-specific build.

- [Principal article](papers/A2-v17-boundary-information-coarsening/article/v137/geometry.pdf) and [editable LaTeX driver](papers/A2-v17-boundary-information-coarsening/article/v137/geometry.tex).
- [Point-by-point response](papers/A2-v17-boundary-information-coarsening/article/v137/RESPONSE_TO_REFEREES_V136.md), [literature audit](papers/A2-v17-boundary-information-coarsening/article/v137/LITERATURE_AUDIT_V137.md), and [issue matrix](papers/A2-v17-boundary-information-coarsening/article/v137/ISSUE_MATRIX.json).
- [Technical supplement](papers/A2-v17-boundary-information-coarsening/article/v137/supplement.pdf), [complete mathematical manuscript](papers/A2-v17-boundary-information-coarsening/article/v137/complete.pdf), [provenance manifest](papers/A2-v17-boundary-information-coarsening/article/v137/PROVENANCE_MANIFEST.json), and [executed build receipt](papers/A2-v17-boundary-information-coarsening/article/v137/evidence/BUILD_RECEIPT.json).

The principal article is the primary referee reading object. The complete manuscript preserves the full mathematical content, not merely the current proof spine. The predecessor v136 directory and all review records are unchanged. All 274 inherited mathematical labels are retained; altered predecessor sources are also archived verbatim.

## Substantive changes

The relative rank-one Fano scheme now has a complete scheme proof, including nilpotent/embedded structure and arbitrary complex base change. A self-contained full-orthogonal harmonic lemma covers every n >= 2. One diagram gives the whole abstract-scheme-to-common-coordinate chain, including the degree-one conormal, ruling orientation, determinant colon, right Cauchy factor and common exterior-duality twist.

A structural intrinsic coefficient criterion is proved and verified both for the original smooth (1,4,6) web theorem and for a different family: polar-restriction Fitting failure schemes of **every nonzero homogeneous linear system**, in any n >= 2 and d >= 1. These schemes have identical reduced determinant support but recover the original system from their abstract nonreduced structure. The source includes an explicit nilpotency-three chart and non-diagonal higher-dimensional component-pair examples.

The original full smooth-web theorem is not weakened. The arbitrary-dimensional component-pair theorem is not presented as the original cube-zero failure-scheme theorem in every dimension.

## Literature and evidence boundary

The closer plethysm, harmonic and Piola statements are compared at specified theorem/equation locations and attributed as classical. **The complete Ballico 1993 paper was not obtained; its requested six-axis theorem comparison remains documentary-open.** No exhaustive historical priority clearance, formal proof certificate or journal acceptance is claimed.

Reproduce from the repository root with `python revisions/a2-v137/unpack.py`, `python revisions/a2-v137/assemble.py`, and `bash papers/A2-v17-boundary-information-coarsening/article/v137/build.sh`. The checksummed transport expands into readable sources; the workflow runs twelve exact scripts, compiles all three PDFs and publishes only on this branch. Local mathematical-source preflight: 37-page article, 66-page supplement and 99-page complete manuscript; all checks passed. The completed remote run is recorded separately below.

<!-- REMOTE_BUILD_START -->
Remote source-bound build has not yet been recorded.
<!-- REMOTE_BUILD_END -->
