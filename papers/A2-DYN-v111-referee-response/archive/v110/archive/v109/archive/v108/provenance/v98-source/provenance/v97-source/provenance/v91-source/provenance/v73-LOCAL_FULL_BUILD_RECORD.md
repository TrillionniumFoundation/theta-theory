# Local complete-manuscript qualification — v73

This is a **source-blob-bound local build record**, not a successful GitHub Actions run or an exact checkout of the entire remote repository. The inherited source was recovered from the v72 artifact `11677741711`, run `38073663320`, at author commit `295800b658aa2ff3aada1707d5785ff757d60724`. Reconstructing its Git directory tree locally gave exactly `bd761b97e603b666ed97b27241f9ab83c7f2550b`, the reviewed v72 paper tree.

The local complete manuscript used every inherited TeX module and appendix unchanged, the four new core blobs below, and the corrected master blob `e63486d9d41976ffdb29162bdcb6ddd04228cff0`. It used the same deterministic archival-body/opening extraction as verify_v73.py. The top-level local metadata was not treated as a substitute for the remote exact-SHA source gate.

| New compiled input | Git blob |
|---|---|
| `core/160_common_source_versions_and_interfaces.tex` | `9ce6294d78689d2153f4842396fa32ec80011720` |
| `core/161_full_source_bv_by_threshold_mixtures.tex` | `7fd5e359ddf45c5713a02af2c50a175a7c7baff9` |
| `core/162_paired_flux_capacity_bound.tex` | `403ac23fe35c7c44610c854f8275f7639918682c` |
| `core/163_scalar_path_error_equivalence.tex` | `b83fbea8d6b5b5d0a90f86dca0b3ab89c5104951` |

## Observed results

The complete native pdfLaTeX build produced **496 pages**. The new opening and four proof sections end on page **9**. The recorder confirms all **163** core modules were actually loaded. All **159** inherited cores, **212** inherited Python files, **12** inherited appendices and the bibliography were preserved byte-for-byte. The auxiliary file stabilized on successive passes with SHA-256 `884c31f41453e8909e221c6b32678f608feaa498455157ea552a10014044f4b3`. The final log contains no LaTeX/package warnings, unresolved references, overfull boxes or missing-character messages.

The local PDF SHA-256 is `794f2cd477de059ff8d4e60a7b6ca00bac197de68a7a0a876eeb30036a2058ff`. A later build may differ in PDF metadata; this hash identifies this local rendered artifact, not every future rendering. All **304,825** extracted word boxes lie within the physical bounds of their **496** pages. Rendered pages were sampled visually; this is not a claim of independent human proofreading of every page.

The exact-rational v73 fixtures pass in ordinary and optimized Python with identical results: 680 threshold mixtures, 47,628 paired-flux inequalities, 15,876 compact-primitive identities, 225 capacity allocations, 561 positive path-error comparisons, and four negative controls. All six retained scripts (`certify_winding`, `certify_excursion`, `verify`, `verify_v2`, `check_v5`, `check_v6`) also passed with their expected certificate paths.

## Corrections found by the full build

The three new leading theorems now use an independent `revisiontheorem` counter. Sharing the inherited `maintheorem` alphabet counter had exhausted that counter in the historical appendix; no historical theorem was removed or renumbered internally to hide the problem.

Poppler's bbox HTML includes control characters representing some mathematical glyph text, which are invalid XML 1.0 despite a correct native rendering. The geometry checker now uses an HTML parser to check every page and word rectangle without interpreting the glyph payload. It retains the raw bbox output, verifies page coverage and does not modify the PDF or drop geometric boxes. The revised renderer blob is `4e064b7d74821d637f75cb748dda53376fc6160d`.

## Scope

These observations establish a local full-source typesetting and finite-fixture result for the stated source blobs. The remote read-only workflow remains authoritative for its own exact checkout SHA and run conclusion. Neither this local record nor a successful CI run proves the missing collision-uniform paired-flux estimate, records an independent human mathematical review, or certifies journal acceptance.
