# A2 v7 — complete referee revision

**Relative Boundary Laws and Statistical Reconstruction in Periodic Dispersing Billiards**  
Qian Qi — September 9, 2026

This is a complete new revision of the actual A2 v6 submission, responding to the latest source-pinned independent referee memorandum. It is not a marker-only branch or a shortened substitute. Every inherited source file remains in this directory; the replaced main file, preamble, and README are also archived byte-for-byte in `history/v6-reviewed-*`.

## Read the revision

- [`main.tex`](main.tex): complete integrated manuscript. All previously active mathematical body inputs remain active. The bibliography is retained and reformatted in author–year style.
- [`build/main.pdf`](build/main.pdf): compiled full referee manuscript, once materialized by the branch-scoped build.
- [`two_collision.tex`](two_collision.tex) and [`build/two_collision.pdf`](build/two_collision.pdf): unchanged complete companion and its build.
- [`RESPONSE_TO_REFEREE_V7.md`](RESPONSE_TO_REFEREE_V7.md): point-by-point response to V6-R1–V6-R4.
- [`PROOF_LEDGER_V7.md`](PROOF_LEDGER_V7.md): statements, dependencies, exact scope, and provenance of the new results.
- [`SOURCE_PINS_V7.json`](SOURCE_PINS_V7.json): reviewed version, report, and historical sources.

## Substantive additions

The exact moving-support tangent comparison is proved with attribution to the referee memorandum. A uniform nonlinear tangent lemma then yields a sharp **positive-offset** joint experiment transition when `d_j / exp(-j gamma) -> 0`, including the infinite-sample-side limit by subexperiment projection. The general nonsymmetric relative theory is not restricted by this additional benchmark.

The new Bernoulli-design lower bound uses actual finite-offset physical probabilities, permits adaptive stopped queries, and includes `log(1/eta)`. Together with the retained fixed-order calibrated upper bound, it gives matching expected preparation order within the precisely stated bounded-flight, shrinking-offset, indicator-only design. It is not a global minimax claim over richer observations.

An exact nested-cube Borel selection specifies all compact minimum-discrepancy estimators without altering the inherited `2 delta` fitting bound. The experiment table distinguishes the long-bridge approximation, fixed contact jets, unlabelled Bernoulli acquisition, and selected-position acquisition.

## Reproduce

From a checkout containing both the preserved v6 directory and this v7 directory:

```sh
python papers/A2-v7-sharp-physical-experiments/tools-v7/checks.py
python -O papers/A2-v7-sharp-physical-experiments/tools-v7/checks.py
python papers/A2-v7-sharp-physical-experiments/tools-v7/build.py --repo-root .
```

The checks use the Python standard library. The PDF build needs `pdflatex` with standard AMS, Latin Modern, natbib, longtable, microtype, xr-hyper, geometry, and setspace packages. Shell escape is disabled. The companion is built before the main article. The build verifies source preservation, bibliography-key retention, the abstract length, normal/optimized diagnostic agreement, and resolution of TeX references.

`verification-v7/BUILD_V7.json` is generated only after a successful build. It separates compilation, finite diagnostics, inherited verification, and mathematical review. It records page counts and overfull-box warnings rather than silently hiding them. Rendering and visual inspection must be recorded separately.

## Manuscript form and handoff

The new main manuscript uses a 12-point article layout, 1.5 line spacing, 1.25-inch margins, an abstract of at most 150 words, author–year references, and an observation–identification–risk–cost exposition. This is the **complete referee version**, not a representation that a formal journal's submission page cap or author-disclosure requirements have already been satisfied. No author affiliation, disclosure, or journal acceptance has been invented. No material was removed merely to achieve a page count.

The revision is for another independent referee round. The original main branch, earlier revisions, historical manuscripts, and latest referee report are unchanged. Build success and numerical diagnostics are not mathematical certification or editorial acceptance.
