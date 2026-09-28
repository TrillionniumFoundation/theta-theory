# Independent A2 v60 audit ledger

September 16, 2026. This accompanies `REFEREE_REPORT.md`; neither this ledger nor a successful check is a proof certificate.

## Frozen identities

The review branch begins at review-ready head `80ad74228001e8d2c3228ff57aff6f9fb8fc0c39`. The actual compiled source is `1a55bfb1102c3eab9cdcd6a292c5ef9070ea14a5`, under `papers/A2-v17-boundary-information-coarsening/`. Its manuscript subtree reconstructed from the frozen source is `f8e130592a601e000be4ed7be76c9843c8603318`. The native workflow is run `35039952221`, attempt 1, artifact `10424981887`.

Native artifact SHA-256: `cc1d87a5454d2dd2637a8f3f741ee00cdb7e379f1b2138a02fb20649ecdcafc8`.

Native source ZIP SHA-256: `377d60c394440f5a33da62f68145d4d9dc39be30c0270d6664e9fcbc737ca914`.

The new module was fetched directly through GitHub at the compiled commit. Its Git blob, `6e313047140dc9a8033124a1482fe28d282be935`, matches the archive bytes. The source-to-review-ready GitHub comparison lists three later delivery commits and no compiled mathematical input changes. The full repository tree was not independently reconstructed. The manuscript subtree was reconstructed and matched to the pinned native build record; this is not authorship authentication or a hostile-compiler attestation.

## Mathematical coverage and exclusions

The complete new 319-line module was examined: the abstract criterion, necessity and sufficiency, contracted Taylor approximation, Chebyshev interpolation and integer rounding, two-disc compatibility, leading Hessian extraction, real density cancellation, smoothing, total variation and the grid bias.

The new argument was followed into the retained full analytic inverse and density inverse. The current half-line/relative determinant proof, headline observation statements, older quantified-law interpolation, and explicit acquisition application were also examined. The current response, historical audit, dependency ledger and literature note were read as provenance rather than proof substitutes. The full v59 analytic module is byte-identical to its reviewed baseline.

This is not a fresh line-by-line certificate for all 418 pages. Exclusions include the entire earlier finite-action/full-phase construction, every global matching and differential proof, all graph/support prerequisites, the complete calibration/acquisition and stopped-record catalogue, and the companion mathematics. Previously scoped reviews remain scoped; mechanical reproduction does not fill these proof-review exclusions.

## Independent source and delivery checks

The verifier from the preceding review was inspected and reused without changes: `reviews/a2-v59-independent-harsh-top4-2026-09-16/verify_delivery.py`, frozen at `f480cf1d099128c0c84df1ed149cff9b75e6ba2d`. It imports no author checker. The current audit actually reran it, rather than copying the author's current verification ledger.

It checked 739 frozen files by size, SHA-256 and Git blob; 113 full-entry, 44 principal-entry and one companion active paths; 123 distinct active paths; 45 build-report evidence entries; and native PDF hashes. An independent comparison with the downloaded v59 source found 114 inherited active files unchanged and eight amended, plus the new active module. These are byte identities, not counts of semantically distinct theorems.

All three entries were rebuilt in a copy of the frozen manuscript tree, in companion/full/principal order, with regenerated auxiliary files and `pdflatex -no-shell-escape`. All 418 pages match the native PDFs in extracted text and same-renderer 72-dpi RGB arrays. The PDF bytes are not identical. The final main log has three underfull notices; principal and companion have none. No critical-pattern match for undefined references/citations, missing characters, overfull boxes or LaTeX errors was found.

Principal pages 54, 55, 56, 57 and 58 were directly viewed as 108-dpi images. No clipping or unreadable formula was observed on those pages. All-page computational parity is not all-page visual inspection. Exact hashes, software versions and result fields are in `AUDIT_RESULTS.json`.

The author's v60 preservation/finite checker was not rerun. Its native output files were hash-checked as delivery evidence, which is a different operation.

## Independent mathematical diagnostics

`independent_checks.py` is new for this round. It uses SymPy exact algebra and mpmath scalar controls, imports no author checker, and does not use removable Python assertions. It checks a 12-dimensional nonlinear weighted-composition quotient, an explicit resonant kernel with small high tail, 246 interpolation-rounding choices, 2,460 Chebyshev nodal inequalities, 300 monomial norms, 729 exact four-density identities and 81 action recoveries. Nonanalytic positive separate factors are included in the algebraic tests.

The weak-norm examples check exact tent integrals and five sinusoidal grid-bias constructions. They are generic functions/densities, not realized billiard-law counterexamples or a proof of optimality within that subclass. The algebraic density tests are also not claimed to realize periodic billiards. These limitations matter more than the number of checks.

The normal and optimized runs emitted identical full JSON, SHA-256 `ec5e8f7ea182118cc498407be47a33dee71de9aca1cba3cc8ab55215efafa5b6` in this environment. The first local diagnostic draft mixed a floating zero into an intended rational density evaluation; that implementation issue was corrected before the successful runs and committed version. It was not a manuscript counterexample. Cross-environment last digits in high-precision outputs can change without invalidating the mathematical identities.

## Reproduction

Extract native artifact `10424981887` into `WORK/artifact/`; extract its `native-source.zip` into `WORK/source/`. The source root is then `WORK/source/source/`, with `WORK/source/SOURCE_MANIFEST.json` alongside it. Use a clean work directory without a pre-existing `rebuild/`. Obtain the verifier at the pinned preceding-review path above, then run:

```sh
python verify_delivery.py WORK
python verify_delivery.py WORK --build two_collision
python verify_delivery.py WORK --build main
python verify_delivery.py WORK --build rigidity
python verify_delivery.py WORK --compare
python independent_checks.py > independent-normal.json
python -O independent_checks.py > independent-optimized.json
cmp independent-normal.json independent-optimized.json
```

The native build needs the TeX packages used by the manuscript. The verifier needs PyMuPDF for page comparison; the new diagnostics need SymPy and mpmath. The current execution used Python 3.13.5, SymPy 1.14.0, mpmath 1.3.0 and PyMuPDF 1.26.7. Logs and full outputs were retained locally; committed JSON summarizes the completed run, not a proposed future run.

## Review-only writes

Only this new review directory is added on the new branch. Manuscript inputs, previous reports, native products, the default branch and repository permissions are not modified. No PR approval, merge or commissioned journal recommendation is implied. The report's negative placement judgment is separate from its acceptance of the three new statements within the declared audit scope.
