# A2 v16 — intrinsic marked boundary laws

**Qian Qi, 28 September 2026.** Primary manuscript: `main.tex`, *Intrinsic marked boundary laws and rigidity of periodic dispersing billiards*. This is the A2 revision responding to the v15 report frozen at `3de6ab93a81e76f35ccf507f8815852ea4c981f6`, not a replacement topic or a change of journal target.

## Mathematical revision

The main theorem is an intrinsic arclength-marked inverse and a registered periodic-table rigidity theorem. It calibrates gap, separate curvatures and free area from onset and low moments, then recovers every asymmetric contact jet with the retained nonsingular even and odd blocks. No numerical Cartesian contact frame or leading geometry is supplied. Analytic continuation recovers a participating pair up to isometry. A connected network visiting every obstacle, with coherent intrinsic arclength registration and rank-two integer lattice-cycle marking, determines the whole labelled periodic table and its marked lattice.

The information contract is explicit: endpoint-arclength laws are observed modulo ONE common sign reversal; they are not averaged with their reflections. The network registration is additional finite data, not inferred from one local law. The theorem uses only onsets, masses, first-moment germs and two leading quadratic moments per channel, rather than the full distributions.

A standalone residual-flux filtration lemma proves that arbitrary lower asymmetric jets do not alter the highest blocks and that the nonlinear arclength mark enters two weights later. A separate analytic-submanifold identity lemma supplies continuation without parametrization ambiguity. Finite-dimensional and formal count-only fibers are proved and physically realized; they are explicitly distinguished from equality of exact analytic count germs modulo reflection, which this revision does not assert it has settled.

## Submission package and preservation

`main.tex` is the theorem-led primary article. The executed local build has **21 pages**. `complete/main.tex` is **Supplement S**, formally included in this submission package. `complete/two_collision.tex` is its retained auxiliary document. The earlier reported 133 and 7 pages belong to the v15 build record, not to a new v16 execution. The current primary rigidity proof is self-contained and does not depend on an unproved assertion in Supplement S.

The entire `complete` directory is the exact preserved Git tree `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`. Its historical front matter still names the preceding article; `SUPPLEMENT_STATUS.md` gives its present submission status. No mathematical input or historical acknowledgment is removed. `history/v15-reviewed` preserves the complete qualified v15 paper tree `db84120af7be42acd785a9bc8d87dc6c652ee8d9`, including its own earlier historical snapshots. Four full primary core files are reused byte-for-byte and included in the new article, not merely archived. Previous repository directories and review branches remain unchanged.

The focused bibliography now contains six external primary research works plus the formally identified supplementary manuscript. Comparisons distinguish local probability laws, intrinsic marks, marked-length spectra, formal normal forms, and their different hypotheses. No exhaustive priority clearance or editorial acceptance is claimed. The Annals/Acta/Inventiones/JAMS writing and submission target is retained.

## Reproduction and evidence scope

Run `python3 tools/run_validation.py` for the primary article. In a full Git checkout run `python3 tools/run_validation.py --all-volumes` to build the primary article and both supplementary documents and verify the pinned complete tree. Requirements: Python 3.10+, `latexmk`, TeX with `amsart`, `lmodern`, `microtype`, `mathtools`, `xr-hyper`, `hyperref`, and Poppler `pdfinfo`. On Ubuntu use `texlive-latex-extra texlive-fonts-recommended latexmk python3 poppler-utils`.

The local **source-content** qualification passed: 5,844 exact finite diagnostics, identical normal and optimized Python output, a 21-page primary build with no final TeX warnings, undefined references, overfull or underfull boxes, and unchanged mathematical/tool source hashes. It was run in a container directory, not an authenticated Git checkout; the receipt therefore truthfully has null source commit/tree and is bound by its source manifest. Supplement S was preserved, not rebuilt in that local execution. A delivery record may bind that manifest to subsequently verified remote blobs without changing this execution scope.

The new GitHub workflow is read-only and records its actual triggering SHA, tree, commands, output hashes, toolchain and PDF hashes. Hosted status is separate from local qualification; existence of a workflow or a queued run is not a pass. Finite diagnostics and compilation do not certify the all-order proofs, analytic continuation or global geometric argument. Those arguments are written out for the next independent referee review.
