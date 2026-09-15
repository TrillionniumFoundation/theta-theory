# Audit ledger: independent A2 v59 review

Review date: September 16, 2026. This ledger accompanies `REFEREE_REPORT.md`; it is not a proof certificate.

## 1. Frozen provenance

Repository: `TrillionniumFoundation/theta-theory`.

- Actual compiled source: `b56282439324435668ae80be90207fe7f5eebbf2`.
- Repository tree of that commit, obtained through GitHub: `2eaf1196e3d65a0b995472bdef12f320a9ddc250`.
- Manuscript subtree reconstructed from the downloaded frozen source: `d9417e5fafc9ee2ad7f9cf70f98809d4c31a2ff8`.
- Review-ready head and parent of the first review commit: `c75b58f58e34cf56d6d4bf674a907b4b979a3940`.
- Review-ready repository tree: `b8dadcf28e293633ab2286a72f2527a77fec975c`.
- Native workflow run: `34985144445`, attempt 1; artifact `10403013663`.
- Native artifact SHA-256: `c62fd4e19677b48f6fd866a772ba4aa98a32d497c1b0e1d74f57b08496fb6f3a`.
- Native source ZIP SHA-256: `83c4f05ad729b0abba05625ea6e41b86a67a5338a05cd123decbb829890c18dc`.
- Previous report: `464209b66aad6ff48b63f054711396fbfd759b64`, reviewing source `92a6d946c98e19c33ebff15997c0116ac158b89d`.

The GitHub source-to-review-ready comparison showed three later delivery commits and no change to a compiled mathematical input. It changed README/delivery records and added `REVIEW_READY_V59.md`. The new analytic module and the main entry/response were also obtained directly at the compiled commit, rather than relying only on the README.

The independently reconstructed subtree is compared against the native build record. The verifier does not independently reconstruct the entire repository tree, authenticate authorship, or regard an unsigned Git commit as a signature. Hash verification establishes the identities being compared, not the mathematical truth of their contents.

## 2. Mathematical coverage

The complete new file `article/23a2_analytic_contact_inverse_v59.tex`, lines 1–354, was read and analyzed. The main obligations were protected Cauchy domains in a fixed-disc Banach space, bounded weighted Green inversion, holomorphic dependence, terminal cancellation in the full envelope, compactness through contracted evaluations, finite-low-jet/high-tail inversion, nonlinear inversion and induced quotient norms. The report gives a separate qualitative Fredholm cross-check and an elementary topology comparison.

The other fresh reading is specified in source keys S1–S9 of the report. It includes the inherited relative determinant interface, actual-smooth jet factorization, density and interior-window inverses, clear-skeleton descent, finite global matching with both inclusions, and the principal moving-family/differential arguments. The prior report and current response/derivation/dependency documents were used for continuity, not as proof substitutes.

Excluded from a fresh complete proof certification: all earlier finite-action/full-phase prerequisites; every graph-to-support conversion prerequisite; all calibration and physical-acquisition premises; the entire stopped/adaptive statistical catalogue; the companion's mathematical argument. No claim of a line-by-line proof audit of all 410 pages is made. No claim of independently counting distinct mathematical theorems is made.

## 3. Source and native-evidence verification

`verify_delivery.py` imports no author checker. It checks file lengths, SHA-256 values and Git blob identities, reconstructs a Git subtree using the recorded modes, verifies active-input manifests, and verifies build-report evidence and native PDF hashes.

Actual results: 718 frozen files; 112 full-entry paths, 43 principal-entry paths and one companion path; 122 distinct active paths; 45 build-report evidence files. The reconstructed manuscript subtree matches the source-tree value in the build record.

All three entries were rebuilt in a clean copy of the frozen manuscript tree, without reusing the artifact's generated auxiliary files. The companion was built first, then the full manuscript, then the principal article, so external references were regenerated in order. Shell escape was disabled. The full set of native build-report evidence hashes was checked, but the author's preservation/finite-check programs were not rerun as part of this review.

All 410 pages agree in extracted text and same-renderer 72-dpi RGB arrays. PDF bytes differ. The final full-manuscript log has two underfull notices; principal and companion have none. No critical-pattern match was found for undefined references/citations, missing characters, overfull boxes or LaTeX errors. Exact results and hashes are in `AUDIT_RESULTS.json`.

Visual inspection was of principal pages 3, 51, 52, 53 and 54 at approximately 101 dpi. These pages were directly viewed as images; no clipping or unreadable mathematical expression was observed. All-page image-array comparison is not all-page human-style visual inspection.

## 4. Independent finite mathematical controls

`independent_checks.py` imports no manuscript checker and does not use removable Python assertions. It performs:

1. Exact rational checks of 180 finite weighted-Green row sums against the infinite geometric majorant, and tail choices/compactness-majorant decay for four contraction parameters.
2. Sixty-four finite stationary chains, with two unequal-curvature pairs, both starting types, 5 or 12 flights, four signed endpoints, and cubic/quartic graph variations. The action is evaluated in a cancellation-resistant form. Stationarity residuals are tested before comparing the shape derivative with the envelope. The maximum relative discrepancy is `1.5809725027812394e-09`. Deliberately doubling the first contact is detected in every configuration.
3. A fixed-disc versus smaller-real-interval topology control using high-degree monomials.

These are finite local chains, not global periodic tables. They do not verify the complex Banach-space contraction, an infinite orbit limit, arbitrary jet order, trace-class determinant convergence, analytic continuation, or any statistical risk theorem. The proofs rather than the diagnostic samples carry those conclusions.

Normal and optimized Python runs emitted identical full JSON. SHA-256 of the complete emitted JSON for this run: `e403787ab223ee6fe4867bca458af5a7ad87322fffadeefa4adb9df9df0ef976`. The committed results file summarizes it; rerunning the script emits all 64 detailed records. Floating-point last digits and therefore the output hash can vary across numerical-library environments without constituting a mathematical discrepancy.

## 5. Reproduction commands

Use Python 3 with NumPy, SciPy and PyMuPDF, plus a working TeX installation with `latexmk` and the packages required by the manuscript. Extract native workflow artifact `10403013663` into a work directory named `artifact/`, and its `native-source.zip` into `source/`. The resulting structure is `source/SOURCE_MANIFEST.json` and `source/source/` containing the manuscript files. Set `WORK` to their common parent, then run from this review directory:

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

The verifier writes `REPRODUCTION_RESULTS.json`, regenerated manuscripts under `rebuild/`, and retained build outputs in the work directory. Start with no existing `rebuild/` directory for a fresh-build audit. This script assumes the explicitly named artifact/source directories have already been extracted; it does not download a moving branch or make network requests.

## 6. Review-only changes

This review branch starts from the pinned review-ready head. Its additions belong solely under `reviews/a2-v59-independent-harsh-top4-2026-09-16/`. Manuscript source, prior reports, native deliveries, the default branch, branch protections and repository permissions are not edited by this review. No merge or pull-request approval is implied by the mathematical assessment.
