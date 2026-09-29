# Submission and preservation map

## Current primary

`main.tex`: full revised A2 v21 article. Read Theorems 1.1–1.2 and Section 7 for the new finite-aperture and persistence results. All six v20 mathematical core files remain active, in addition to the new introductory and proof chapters. The primary is self-contained at its stated assumptions.

## Unchanged submission volumes

`retained/v18/main.tex`: Supplement R, the complete v18 article. Native tree: `3c558d7799e9e49812e7bab98320d3a98e7f7418`. It retains all moment inverses, count-fiber arguments, physical finite-jet experiments, registered symmetric-table theorems and both earlier regularizations. Its historical validation wrapper is preserved as history, not invoked as the current v21 validator.

`complete/main.tex`: Supplement S, complete smooth relative boundary, Volterra and Abel theory. `complete/two_collision.tex`: its auxiliary document. Their exact shared tree is `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`, also retained inside Supplement R. These are included submission materials, not independently published papers.

## Frozen reviewed source

`history/v20-reviewed`: exact whole reviewed v20 paper tree `3b34e4156b3ff621df9c1a3fb8aece4c66f1f07b`, including previous archives and evidence. This is not a competing current primary. The hosted full qualification verifies its tree, reruns its finite diagnostics and additionally rebuilds its primary for preservation checking.

## Execution route

`python3 tools/validate_v21.py` validates source pins and runs the current primary diagnostics and build. A local content-only run reports null commit/run fields.

`python3 tools/validate_v21.py --all-volumes --require-checkout` requires a real checkout, checks all three retained tree identities, reruns retained diagnostics, builds the current primary, Supplement R, both Supplement S documents, and the archived v20 primary. Output and any failures are recorded under `verification/current`; no historical source is edited. The workflow uploads PDFs and logs bound to its exact triggering commit.
