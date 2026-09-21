# A2 revision 107 — referee entry point

**Title:** Hankel information and nonlinear contact of synchronized roots  
**Author:** Qian Qi  
**Date:** 2026-09-21

Principal manuscript: `paper.tex` (compile from `papers/A2-v17-boundary-information-coarsening`).

Source baseline: `5cbbe96cd2ac590bfa2e17bcef97b0630cd91c4a` (v106).  
Review baseline: `bcd8052659a783632de3873af49f05f600a8f764`, report at `reviews/a2-v106-independent-harsh-top4-2026-09-21/REFEREE_REPORT.md`.

Revision branch: `revision/a2-v107-synchronized-root-contact-budget-geometry-2026-09-21`.

## Reading order

Read the introduction and theorem-level literature comparison, the native binary information theorem, the fixed-budget theorem, and the synchronized-root contact theorem. The weighted critical theorem and endpoint completion sections supply the requested extensions. Appendix “Theorem dependencies and source provenance” separates inherited statements from new ones.

The retained v104 and v106 mathematical parts are imported in full; historical articles and review reports are unchanged. A new main article reorganizes the proofs around a nonlinear contact theorem, rather than treating root-label multiplicity as multiple observed affine sheets.

`RESPONSE_TO_R106.md` maps every numbered request to a precise source and theorem label. `checks.py` tests finite algebra and examples, not general proofs. `build_review.py` compiles both the pinned v106 source and this revision, emits input/output SHA-256 manifests, and reports unresolved references or compilation errors. The branch-specific GitHub Actions workflow runs the same script and retains PDFs, logs, and the source-bound receipt as an artifact.

## Local replay

From the repository root, with Python 3, SymPy, latexmk, and a standard TeX Live installation:

```sh
python papers/A2-v17-boundary-information-coarsening/article/v107/build_review.py
```

Outputs are written to `build/a2-v107-review/`. A generated receipt is evidence only after the command actually succeeds; the presence of a workflow or script is not a successful-build claim. No automated step merges this branch or edits any other paper branch.
