# A2 revision 108 — Contact tomography in Hankel information geometry

This revision responds to the latest independent report on A2 v107. Its principal result is a conormal rigidity theorem, not the mere coexistence of a synchronized cone and a native information metric.

## Provenance and isolation

- Review branch: `review/a2-v107-independent-harsh-top4-2026-09-21`.
- Review commit: `b3d0c5ce18a5f6e4491ed70f50a6991ea846dcd8`.
- Reviewed manuscript: `a17d3cad6aeebe75f29102ecb2d1ef6784927f4e`.
- New branch: `revision/a2-v108-hankel-contact-tomography-intrinsic-fibres-2026-09-21`.

The branch descends from the review commit. No earlier manuscript, review, or other paper branch is overwritten. All v104/v106/v107 mathematical source parts remain in the article, in the main argument or the appendices. The preparation script copies four parts into `prepared/`, exposes hypotheses and scope, and checks that no proof/theorem environments have been removed.

## Reading order

`paper.tex` is the manuscript entry point. The new principal proof is `parts/00-general.tex`; the explicit three-root reconstruction is `parts/01-tomography.tex`. `parts/02-intrinsic.tex` supplies the exact labelled-function inverse problem. `parts/03-precision.tex` separates reciprocal-fibre geometry and states the uniform classes. The introduction and `parts/04-positioning.tex` compare inverse parametric programming and direct design equivalence. `RESPONSE_TO_R107.md` maps every numbered request to the revision.

The central theorem covers any number of endpoint-free root pairs under injective quadratic measurements. With two shared parameters its sole second-jet ambiguity is the determinant form; explicit native three-site relations remove it exactly under transversality. With at least three shared parameters the quadratic ambiguity vanishes. Finite dual-jet recovery transports the fixed-budget design fibres to observable data. In the three-root/two-parameter case, five ordinary directional contact curvatures suffice, with an exact exceptional family.

## Native replay

Requirements: Python 3.10 or newer, SymPy, a TeX distribution with AMS/Latin Modern/`mathrsfs`, `latexmk`, and `pdfinfo`. From the repository root:

```sh
python papers/A2-v17-boundary-information-coarsening/article/v108/prepare.py
# Prepared inputs must be committed before the source-bound build.
git add papers/A2-v17-boundary-information-coarsening/article/v108/prepared
# Commit on this revision branch only, then:
python papers/A2-v17-boundary-information-coarsening/article/v108/build_review.py
```

The branch-scoped workflow performs this preparation, records the exact source commit, builds the PDF, replays the nine new check groups and eight preserved v107 groups, then commits only this revision's delivery files. It does not merge into another branch. Normal non-force pushing prevents overwriting concurrent work.

The delivery is under `evidence/`: `A2-v108.pdf`, final TeX log, `verification.json`, `source-manifest.json`, both finite-check receipts, and `source-bundle.zip`. Check the actual receipt: a source commit and a successful final log, not a first-pass log, are required for a source-bound success claim. The evidence-only commit may follow the exact compiled source commit; the receipt identifies the latter, and the source manifest permits byte comparison.

The original v107 failure stopped at undefined `\mathscr`; v108 loads `mathrsfs`. The build rejects undefined references/citations, duplicate labels, unresolved rerun requests, and overfull boxes. Finite checks and successful compilation are not independent mathematical verification. The proofs remain subject to author and referee examination.
