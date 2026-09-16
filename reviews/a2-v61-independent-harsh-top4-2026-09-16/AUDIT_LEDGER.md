# Audit ledger: independent review of A2 v61

Date: September 16, 2026. This accompanies `REFEREE_REPORT.md`; it is not a proof certificate or commissioned journal evaluation.

## 1. Frozen provenance

Repository: `TrillionniumFoundation/theta-theory`.

- Compiled mathematical source: `71e0bd6306f54466728c2e6e781bb0f422c5cfb0`.
- Review-ready head, from which this review branch starts: `774aa34b43f5013dd3a41c8bc6ca5a529466d788`.
- Reconstructed manuscript subtree: `ee2d39dbce4dce4d972ec1a281af1df9aaf44d4a`.
- Manuscript path: `papers/A2-v17-boundary-information-coarsening/`.
- Native workflow / attempt / artifact: `35043311589` / `1` / `10426471183`.
- Artifact SHA-256: `8a08c96bbaaae1a9fc15c4f292bb899c0b7cfab25ac286b6e696eafd699e8b56`.
- Native source ZIP SHA-256: `81a733a228b6815e78a175e41ce1a108570f140e6356756744ff286087658b21`.
- Previous v60 mathematical source: `1a55bfb1102c3eab9cdcd6a292c5ef9070ea14a5`.
- Previous v60 report: `396bb28e17ba9944af5ff89a2db601412eeb95ee`.

The GitHub comparison from compiled source to review-ready head shows three delivery commits, with no intervening compiled mathematical-input change. The new introduction was also fetched directly at the compiled commit; its Git blob is `2d41a5d723b932252283f79b44c53f90f1177575`, matching the frozen archive.

The verifier reconstructs the manuscript subtree and compares it with the native build record. It does not independently reconstruct the entire repository tree, authenticate authorship, or turn an unsigned commit into a cryptographic signature. Hash agreement identifies the material compared; it does not establish mathematical truth.

## 2. Fresh mathematical examination

The precise files and coverage are in source keys S1–S7 of the report. Fresh reading concentrated on the revised principal introduction and the mechanisms now emphasized: near-onset channel localization, finite Jacobi and relative-flux formulas, the physical first-impact phase measure, the two-ended trace-class normalization, actual-smooth stationary factorization, the single-offset and finite-flight inverses, and the complete quartic-response/area-preserving-family argument. The structural headlines and acquisition dependency were checked for consistency. The response and cover letter were treated as claims and arguments, not proof substitutes.

The v59/v60 analytic modules are unchanged. Their earlier scoped assessments are retained for continuity, not described as fresh complete re-verification in this round. The complete global finite-fiber, moving-family, graph-to-support, acquisition/calibration and stopped-experiment catalogues, and the companion's mathematical argument are not freshly certified. There is no claim of a line-by-line proof audit of all 420 pages.

The report finds no new mandatory core repair in this coverage, but remains adverse on the requested highest-level significance case. The fact that v61 adds no theorem is not the reason for that recommendation. The requested mechanism-centered exposition is acknowledged as addressed.

## 3. Source comparison and native reproduction

Independent comparison of the v60 and v61 frozen archives found all 739 inherited files present, 736 byte-identical. Only inherited `README.md`, `main.tex` and `rigidity.tex` changed. The old introduction remains unchanged in place; the new introduction replaces it in the active input graph. Its two inherited mathematical environment blocks occur verbatim in the replacement. These are source-identity checks, not counts of distinct mathematical theorems.

The independent verifier checked all 753 frozen file lengths, SHA-256 values and Git blob identities; reconstructed the manuscript subtree; checked 123 distinct active inputs; and checked 45 build-report evidence entries. Per-entry active counts are 113 full, 44 principal and one companion. Shared inputs explain the difference between their sum and union.

Fresh builds began from the frozen source without native generated auxiliary files, in companion/full/principal order. Shell escape was disabled. All entries built successfully. All 420 pages agree with the native PDFs in extracted text and same-renderer 72-dpi RGB arrays under PyMuPDF 1.26.7. PDF bytes differ. Exact native/fresh hashes are in `AUDIT_RESULTS.json`.

Final logs have one principal and three full-manuscript underfull-box notices, none in the companion. There are no matches for undefined references/citations, missing characters, overfull boxes or LaTeX errors. This log-pattern check is not a proof or exhaustive typographic assessment.

Actual visual inspection covered principal pages 4, 8, 116 and 117 at 108 dpi. No clipping or unreadable mathematical expression was observed there. Other pages were compared mechanically, not claimed as visually inspected. The inspected images and fresh build outputs are included in the accompanying audit package.

## 4. Independent exact and symbolic controls

`independent_checks.py` imports no author checker and uses no removable Python assertions. It requires SymPy and performs the following finite controls:

- Derives the exact support-area polynomial, the area-constraint tangent, and the fourth graph derivative by expanding the actual support parametrization. It checks the response `sqrt(3)/2` and distinguishes the erroneous `7*sqrt(3)/18` obtained by omitting the determinant amplitude.
- Checks 48 positive rational tridiagonal Schur/cofactor configurations, including the empty-interior case. These are finite algebraic matrices, not asserted global billiard realizations.
- Evaluates 21 finite quadratic-chain/quartic coefficient configurations, independently checking the effective Hessian and endpoint recurrence against their hyperbolic formulas. The finite-to-limit comparison is a diagnostic, not a proof of trace-class convergence.

Normal and optimized Python runs produced identical full JSON. Its SHA-256 in this run is `fa460f675279ad0661ecf35dc44d7699ca742459b05202734f4fd837c20b1120`. The complete output is in the audit package; the branch retains the executable script and a summary. The author's own preservation/checker program was not rerun. The retained delivery verifier comes from the previous independent audit, not the author's checking code.

No finite control establishes arbitrary-order smooth factorization, a Banach-space inverse, infinite trace-class convergence, global analytic continuation or a statistical risk theorem. Those assertions depend on their proofs, within the coverage stated above.

## 5. Reproduction

Use Python 3, SymPy and PyMuPDF, and a TeX installation with `latexmk`, `pdflatex` and the manuscript's required packages. Extract native artifact 10426471183 into `$WORK/artifact/`, then extract its `native-source.zip` into `$WORK/source/`. The latter contains `SOURCE_MANIFEST.json` and a nested `source/` directory with the manuscript. Start without `$WORK/rebuild/` for a fresh build. From this review directory run:

```sh
python verify_delivery.py "$WORK"
python verify_delivery.py "$WORK" --build two_collision
python verify_delivery.py "$WORK" --build main
python verify_delivery.py "$WORK" --build rigidity
python verify_delivery.py "$WORK" --compare
python independent_checks.py > independent-normal.json
python -O independent_checks.py > independent-optimized.json
cmp independent-normal.json independent-optimized.json
```

The verifier writes `REPRODUCTION_RESULTS.json`, fresh build outputs and regenerated manuscripts under the work directory. It assumes the specified archives are already extracted; it does not fetch a moving branch. The complete source-difference record and introduction diff used in this audit are also in the accompanying package.

## 6. Review-only changes

The new branch is `review/a2-v61-independent-harsh-top4-2026-09-16`. Its changes are restricted to this review directory. No manuscript, earlier report, default branch, repository permission or branch protection is changed by the review. No pull-request approval or merge is implied.
