# A2 v122 — Ramification and intrinsic primary boundaries in multiplication failure

Branch: `revision/a2-v122-intrinsic-primary-k3-boundaries-2026-09-23`.
Base: v121 product commit `44f6b0bf3bb4f1f8c2a87d84beb61d82194fd5e7`.
Controlling report: Referee II on v120, commit `489009deff528b896d2daee3fcf18a2ebdc2ab39`.

## Referee reading order

Read **geometry.pdf** as the principal article. Sections 1–4 contain the relation–ramification correspondence, the nonempty `(1,3,3)` / `(1,4,6)` class, the fixed-tensor global primary and all-power formulas, flat relative thickenings, and intrinsic recovery of the ramification curve or K3 surface. The v121 universal primary flag, explicit elliptic family, complete `(1,2,2)` theorem and conductor/relative framework then remain in full.

Read `RESPONSE_TO_REFEREE_II_R120.md` for the seven-item reply and crosswalk to the first v120 report; `DEPENDENCY_MAP.md` for the precise theorem chain. `paper.pdf` is the complete preserved companion and `applications.pdf` contains the cross-referenced application edition. All old mathematical parts remain byte-identical; no previous branch is overwritten.

The intrinsic recovery is a theorem about abstract full failure schemes, not just about their ambient embeddings. It recovers the abstract ramification variety, not the polarization, finite map, or entire input algebra. The fixed-tensor primary theorem is on the entire projection-corank-at-most-one open for a proved nonempty admissible class; it does not silently classify the omitted higher-corank locus.

## Reproduce

From a checkout including this directory and its unchanged sibling directories `v120` and `v121`, install Python with SymPy 1.14.0, pdflatex with the amsart/lmodern/geometry/microtype packages, and poppler's pdfinfo. Then run:

```sh
SOURCE_COMMIT_SHA="$(git rev-parse HEAD)" bash papers/A2-v17-boundary-information-coarsening/article/v122/build.sh
```

The script does not author or rewrite mathematical sources. It runs retained and new exact tests, compiles all three editions, checks unresolved references/citations and overfull boxes, and writes source/product hashes and theorem numbers/pages in `evidence/`. `SOURCE_COMMIT_SHA` must be the actual source commit; a local build without it is labelled a local snapshot, not an invented Git commit.

The independent new regression checks use rational arithmetic. They check power intersections for n=1,...,8, symbolic restriction/contraction/Jacobian equalities for cubic and quartic examples, and the unit Groebner bases of basepoint and singularity ideals on every projective chart over QQ. The manuscript proves the general class results separately.

## Evidence boundary

The source-bound build receipt and diagnostics are reproducibility evidence, not mathematical or priority certification. `LITERATURE_AUDIT.md` records the still-uncompleted full-text comparison with Ballico 1993 (RII-120.1). No claims about its unseen theorem statements, exhaustive novelty, or a journal decision are made.
