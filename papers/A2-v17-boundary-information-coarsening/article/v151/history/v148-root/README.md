# A2 revision 148 — intrinsic coefficient symmetries and moving pencils

**Principal article:** `geometry.pdf` (native LaTeX source: `geometry.tex`). The article is *Finite failure schemes and the reconstruction of quadratic pencils*, by Qian Qi.

The separate application manuscript is `applications.pdf`. `archive-v144.pdf` is a non-submitted historical archive. Neither is bundled into the principal submission.

## Review provenance

New branch: `revision/a2-v148-coefficient-symmetries-moving-pencils-2026-09-24`.

The controlling v147 report is pinned at `17fb7ba7cab6545f5da6d4fcde5283318bd26725`, path `reviews/a2-v147-independent-harsh-top4-2026-09-24/REFEREE_REPORT.md`. Read `RESPONSE_TO_V147_REPORT.md` for the point-by-point response and `ISSUE_MATRIX_V148.json` for status distinctions.

## New mathematical reading path

`parts/35-coefficient-symmetries-v148.tex` proves intrinsic recognition of one-sided Cauchy coefficient relations, the exact proper/full orientation dichotomy, the complete affine linear stabilizer, the global zero/full ambiguity criterion with actual line-twist recovery, and a geometric orbit-set classification.

`parts/36-covering-moduli-v148.tex` proves that degree-m maps of P¹, modulo independent projective changes in source and target, are faithfully realized by unmarked failure thickenings of moving quadratic pencils in a single singular fibre orbit. The fibre algebra, all graded vector bundles, and the abstract pencil, quotient and first-relation bundles are fixed. The explicit degree-three pair has rank 167945 for n=3.

All v147 principal mathematical blocks and labels, including singular-pencil reconstruction, the local inverse and actual source-bundle descent, remain. The introduction and abstract integrate the new consequences. The group quotient now cites the inspected Milne homomorphism theorem precisely.

## Reproduction

With Python, SymPy 1.14.0, NumPy 2.3.5, pdflatex and pdfinfo installed:

```sh
bash build.sh
```

A fresh overlay-only checkout is completed by `python revision_v148.py assemble` first. The sibling v147 directory is the immutable predecessor. The isolated GitHub Actions workflow performs this assembly, publishes the complete native source, runs all 25 regression scripts, builds the three PDFs, and publishes the source-bound receipt. It may only write this revision directory and the A2 root review entry, on the designated revision branch.

Read `evidence/BUILD_RECEIPT_V148.json` for actual executed results and page counts. `NONDELETION_V148.json` records preservation of 194 predecessor source files and every old principal mathematical block. `PROVENANCE_MANIFEST_V148.json` supplies SHA256 values. The tests are finite consistency checks, not universal proof certificates.

## Documentary item still open

Ballico 1993 complete theorem/proof text was not obtained. The publisher metadata and failed full-text accesses are recorded in `LITERATURE_AUDIT_V148.md`. No theorem-level nonanticipation or journal acceptance is asserted. This documentary requirement remains distinct from the new mathematical results submitted for renewed scrutiny.
