# Audit ledger — independent A2 v62 review

September 16, 2026. This ledger accompanies `REFEREE_REPORT.md`; neither document is a commissioned journal decision or proof certificate.

## Frozen provenance

Repository: `TrillionniumFoundation/theta-theory`.

| Object | Identity |
|---|---|
| Actual compiled source | `037c80dc44d8191e6f808591ea0651e813234d06` |
| Review-ready head / review-branch base | `fa322c27f9aea6ce1f21b46f41e7e2ce02dcc631` |
| Manuscript subtree reconstructed from frozen files | `160735632f3977d47dcf708fb2292699ab79fafd` |
| New proof-module Git blob | `e3ead4bc73e52556490977ad17b4c6868384d03e` |
| Native workflow / attempt / artifact | `35047150051` / `1` / `10427846002` |
| Native artifact SHA-256 | `e02c1f9bb6cb60ad1cbd08dfd1923f2e92672d52ab97ec7f2e6d10b6da2710bc` |
| Native source ZIP SHA-256 | `3d320058366746fb3b4d9d8dc5e71f01a710737ea8c3e686bfe6687ddcea138f` |
| Prior v61 report | `9ec2004a18cccc69ed473685bdf94c91f0b25d4d` |
| Prior v61 source / artifact | `71e0bd6306f54466728c2e6e781bb0f422c5cfb0` / `10426471183` |

Branch searches identified v62 as the latest delivered revision during this review. The source-to-review-ready GitHub comparison showed only three delivery commits and no compiled mathematical input changes. The new module was fetched directly at the compiled SHA, independently of the downloaded archive. Hash checking establishes identities relative to the checked manifests; it does not authenticate authorship, reconstruct the complete repository tree, or prove mathematics.

## Mathematical coverage and result

The complete new file `article/23f2_finite_experiment_analytic_inverse_v62.tex` (463 lines) was read. The central checks concern relative density normalization, actual success mass, comparison through realizable limiting laws, fixed-attempt conditional sampling, cell concentration, measurable approximate selection, even-flight schedules, Borel calibration displacement, gap-to-time amplification, and the exact position-pilot cap.

The current conditional real-observation inverse, four-density identity, physical phase-integration proof, relative determinant/density interface, and complete printed position-pilot file (266 lines) were read as dependencies. Principal structural statements, the additive overview, response, cover letter, historical audit, dependency declaration and the complete v61 report were also examined. Source keys S1–S7 in the report specify these locations.

The scope excludes a fresh complete audit of the earlier nonlinear finite-chain construction, the whole v59 Banach-space construction, all global matching/lattice and moving-family proofs, the quartic comparison, the remaining statistical catalogue and the companion. The previous scoped assessments are not silently treated as full certifications.

The five new statements withstand this scoped examination. R62-m1 corrects the all-history last pilot-grid time: the retained ceiling permits a value strictly below `j*g_+ + 3*epsilon`, not always at most `j*g_+ + 2*epsilon`. The latter does hold as a good-history stopping-time bound. The correction has no effect on the preparation cap or either claimed statistical exponent. The adverse placement assessment is independent of this minor correction.

## Independent source comparison

The native v61 and v62 artifacts were both downloaded through the authorized connector. `compare_baseline.py` independently checks every frozen file's length, SHA-256 and Git blob against its manifest before comparing the bytes.

Actual result: all 753 inherited files remain; 750 are byte-identical; only manuscript `README.md`, `main.tex`, and `rigidity.tex` differ among inherited files. The v62 source has 767 files. Comparing the two active manifests separately gives 123 inherited active paths, none removed, and three additions: the finite-experiment proof, its overview, and the new explicit reference-route file. The resulting union is 126 paths. These are file and active-input findings, not a count of distinct mathematical results or an independent semantic preservation proof.

## Fresh native reproduction

`verify_delivery.py` is the independent v59 review verifier, retained without modification and applied to v62. Its SHA-256 is `5c9a5cfca2246e7a8b3b9428bc4157645d86d71c042c1d600a82269e6052765d`. It imports no author checker. Its provenance is reviewer tooling, not a manuscript program claimed as independent.

Actual checks: 767 frozen files; 115 full-entry, 47 principal-entry and one companion input, with 126 distinct paths; 45 build-report evidence entries; all three native PDF product hashes; the reconstructed manuscript subtree. The source-to-review-ready GitHub comparison was additionally checked.

Fresh builds used an initially absent `rebuild/` directory, copied from the frozen source, with generated auxiliary files produced in companion/full/principal order. Shell escape was disabled. All builds succeeded. The final logs have four full-manuscript and one principal underfull notices and no critical-pattern match for undefined references/citations, missing characters, overfull boxes or LaTeX errors. The companion has no underfull notice.

All 432 pages match the native delivery in extracted text and same-renderer 72-dpi RGB arrays, using PyMuPDF 1.26.7. PDF bytes differ. Native/fresh SHA-256 values and per-entry results are in `AUDIT_RESULTS.json`. This is mechanical parity, not an assertion of all-page visual reading. Pages 63–69 of the principal PDF were rendered for inspection; pages **65, 68 and 69** were actually opened and inspected at 108 dpi. No clipping or unreadable formula was observed on those three pages.

The browser could not fetch the raw manuscript PDF; inspection used the actual connector-downloaded native artifact and local rendering. No OCR was used. Literature checking used the primary online records listed in the report, with the stated record-level rather than proof-audit scope.

## Independent finite mathematical controls

`independent_checks.py` imports no author checker and does not use removable Python assertions. It checks 1,458 exact conditional count configurations; 16 binomial lower tails and 80 Bernstein tails at 70-digit precision; 12 exact square-tube identities; four symbolic exponent balances; 27 calibrated and 21 complete-budget even schedules; and three exact ceiling counterexamples. The outside-category control distinguishes the original cell probability from an inconsistently recropped one; it is not a claim that no alternative consistently cropped experiment can work.

The finite probability parameters and schedule examples are not certified realizations of periodic billiards. They do not prove infinite-dimensional inversion, trace-class limits, the complete statistical theorem or minimax optimality. The printed arguments carry those conclusions.

Normal and optimized Python output is identical. SHA-256 of the full emitted JSON in this environment: `6b9003cbf22c7c671b5862fae78454d03f4095604521c60038be989b1271cd39`. `AUDIT_RESULTS.json` includes the complete emitted mathematical result object. The author's own finite/preservation checker was not rerun.

## Reproduction

Use Python 3 with PyMuPDF, SymPy and mpmath, and a working TeX environment with `latexmk` and the manuscript packages. Extract native artifact 10427846002 into `WORK/artifact/`; extract its `native-source.zip` into `WORK/source/`, producing `WORK/source/SOURCE_MANIFEST.json` and `WORK/source/source/`.

```sh
python verify_delivery.py WORK
python verify_delivery.py WORK --build two_collision
python verify_delivery.py WORK --build main
python verify_delivery.py WORK --build rigidity
python verify_delivery.py WORK --compare
python independent_checks.py > independent-normal.json
python -O independent_checks.py > independent-optimized.json
cmp independent-normal.json independent-optimized.json
python compare_baseline.py a2-v61-native-products.zip a2-v62-native-products.zip
```

Start with no `WORK/rebuild/` directory for a fresh build. The verifier writes a reproduction JSON and retained build transcripts under `WORK/`. It records mismatch lists; examine them rather than treating process success alone as PDF parity. The results committed here have empty mismatch lists for every entry. The baseline script takes the two original workflow artifact ZIPs and does not fetch a moving branch.

The downloadable audit archive retains full mathematical outputs, fresh-build transcripts, reproduction results, baseline comparison and the three inspected page images. The full report is authoritative at this review branch. Only files below `reviews/a2-v62-independent-harsh-top4-2026-09-16/` are added. Manuscripts, past reports, default branch, permissions and branch protections are not edited, and no PR approval or merge is implied.
