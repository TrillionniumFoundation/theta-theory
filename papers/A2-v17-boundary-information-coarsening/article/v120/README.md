# A2 revision 120

## Conductor boundaries and primary structures in multiplication failure

**Author:** Qian Qi. **Date:** September 22, 2026.

New isolated branch: `revision/a2-v120-loewy-boundary-primary-2026-09-22`.
Controlling referee: R119 Round 3, commit `b409ec5eb4dfbb75850d90bff69a78604d3a512b`.
Frozen prior mathematical source: `59437d7eb88b4791769eaf856bb6dd0f9c6c3a2b`.
The earlier v119-labelled reports on the unmaterialized alternate branch are historical, not the controlling review of this revision.

## Reading editions

[Primary geometry article](geometry.pdf) · [Complete manuscript](paper.pdf) · [Application appendices](applications.pdf).

[Point-by-point response to R119](RESPONSE_TO_R119.md) · [Literature audit](LITERATURE_AUDIT.md) · [Logical dependency map](DEPENDENCY_MAP.md).

The complete TeX sources are committed, not instructions to generate a future paper. `geometry.tex`, `paper.tex` and `applications.tex` share `preamble.tex`; `core.tex` fixes the mathematical input graph. The complete edition retains every inherited mathematical part and all complementary proofs and statistical appendices.

## New results

The new main section `parts/03c-loewy-boundary-primary.tex` proves a quadratic-layer factorization for cube-zero augmentation ideals and classifies the **entire** multiplication failure scheme for every complex local algebra of Hilbert function `(1,2,2)`. It gives all associated strata and explicit primary representatives, including the extreme-corank boundary, a conductor-kernel formula, and an exact family in which the quadratic factors collide. It also gives a global projective realization.

`parts/01e-length-sharpness.tex` proves sharpness of `r+1` in every codimension and every prescribed generating rank at least two, and separates the elementary field-level length argument from the relative theorem. `parts/02l-relative-incidence.tex` and `parts/01f-relative-cohomology.tex` give full arbitrary-base-change proofs. The new roadmap and literature section distinguish general presentation, structural factorization, and complete classification in the specified class.

## Reproduce and verify

Run `bash build.sh` here, with Python 3, SymPy, TeX Live, and `pdfinfo` installed. The script has no network dependency and does not run an authoring or materialization script. The exact frozen v119 source is vendored under `inherited-v119/source`; the previously missing v118 diagnostic is actually vendored under `inherited-v118/verify_revision.py`.

The runner executes every mathematical diagnostic function from v119, the three v118 regression groups, and the new exact primary/deformation/sharpness checks. Its preservation check compares all inherited mathematical part files byte-for-byte and verifies every old label against the frozen source. The resulting diagnostics, preservation manifest and PDF hashes are under `evidence/`.

`evidence/BUILD_RECEIPT.json` binds compilation to the mathematical-source commit. `evidence/PUBLISHED.json`, written in a separate publication-receipt commit, identifies the PDF/product commit without a self-referential commit hash. A successful build is not proof certification, priority certification, an independent referee endorsement, or journal acceptance. Consult the actual workflow conclusion and receipts rather than inferring success from this guide.

The workflow changes only this revision directory and its new index/workflow; it refuses a non-fast-forward publication or a concurrent branch-head mismatch. No existing manuscript, review branch, default branch or earlier revision is overwritten.

## Remaining scholarly item

E119.1 is **partly addressed, not closed**. The generator-scheme comparison and algebra-length context have been strengthened and the published ABHS citation updated. Complete Ballico 1993 theorem text was not obtained. The missing comparison is recorded explicitly in the audit; no non-anticipation claim is inferred from inaccessible text. All mathematical statements are retained at their proved scope, and the new results add boundary geometry rather than reducing the research objective.
