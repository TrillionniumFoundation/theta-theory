# A2 v58 — independent audit and reproduction ledger

Date: September 15, 2026. This ledger accompanies `REFEREE_REPORT.md`. It records performed checks, not a formal verification of the manuscript's mathematics.

## 1. Objects and provenance

Repository: `TrillionniumFoundation/theta-theory`.

- Review-ready head: `76535b285378923bacc7eaf17809dd3ab7a3bf6d`.
- Actual compiled source: `92a6d946c98e19c33ebff15997c0116ac158b89d`.
- Manuscript path: `papers/A2-v17-boundary-information-coarsening/`.
- Reconstructed manuscript Git subtree: `39d14581fd018149f2dcce7c306d04ad8e286c0f`.
- Native workflow: `34969789751`, attempt 1; artifact: `10397425264`.
- Downloaded artifact size: 6,063,342 bytes.
- Artifact SHA-256: `4a3d7c6eaed1f4b927b0a05efe94b675a03c4463c4809da81238100dcfc2a868`.
- Previous report: `reviews/a2-v57-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md` at `e14138660e716daf60471f3b98e8f1d30cb61a34`.
- New review branch: `review/a2-v58-independent-harsh-top4-2026-09-15`, created from the review-ready head above.

The GitHub connector supplied the branch identity, repository comparison, manuscript records and native workflow artifact. The actual compiled source, rather than the preparation commit or later delivery-attestation commit, is the mathematical object of review. The compiled-to-review-ready comparison adds delivery records and entry documentation; it does not alter active compiled inputs. No v59 branch was returned when checked before depositing this report.

The review branch adds only the new review directory. It does not replace manuscript inputs, previous reports, the repository README, the default branch, protections, or permissions. No merge or PR approval is part of this review.

## 2. Independent source and product checks

`verify_artifact.py` imports no author checker. It compares the two frozen manifests; checks byte lengths, SHA-256 values and Git blob identities for every declared source file; reconstructs the Git tree using the declared Git modes and directory-aware byte ordering; compares that tree with the pinned source-tree identity; checks every active-manifest entry against the frozen manifest; and verifies every build-report evidence hash.

Observed results:

| Check | Result |
|---|---|
| Frozen source files | 699 verified |
| Active main / principal / companion paths | 111 / 42 / 1 |
| Distinct active paths in their union | 121 |
| Native build-report evidence entries | 45 verified |
| Reconstructed source tree | Matches pinned identity |
| Fresh companion / full / principal page counts | 7 / 285 / 109 |
| Extracted-text mismatch pages | None, across all 401 pages |
| Same-renderer 72-dpi RGB mismatch pages | None, across all 401 pages |
| Rebuilt PDF byte identity | Not identical; not claimed |

The resulting hashes, page counts and log matches are in `ARTIFACT_VERIFICATION.json`. This includes hashes of this session's rebuilt PDFs; another rebuild can have different PDF bytes while reproducing the rendered pages.

The log scan found two principal underfull-box notices (badness 2600 and 1057), three full-manuscript underfull-box notices (1057 once and 10000 twice), and no companion matches. It found no undefined-reference, undefined-citation, missing-glyph, overfull-box or LaTeX-error matches. This is a stated pattern scan of the logs, not a universal TeX diagnostic theorem.

Actual visual inspection was limited to principal pages **3, 19, 48 and 49**, rendered at 108 dpi. The formulas were readable and no clipping was observed there. Other pages were computationally compared but are not claimed to have received individual visual inspection.

## 3. Reproduction procedure

The artifact ZIP contains the native products and `native-source.zip`. The latter contains `SOURCE_MANIFEST.json` and the `source/` tree. Starting with the downloaded native artifact and the review scripts, create the following layout:

```text
audit/
  native/                    # extracted workflow artifact
  source/
    SOURCE_MANIFEST.json
    source/                  # extracted frozen manuscript source
  rebuild/                   # fresh copy of source/source
```

Example commands, run in a writable scratch directory:

```sh
mkdir -p audit/native audit/source
unzip a2-v58-native-delivery.zip -d audit/native
unzip audit/native/native-source.zip -d audit/source
cp -a audit/source/source audit/rebuild
(
  cd audit/rebuild
  for entry in two_collision main rigidity; do
    latexmk -norc -pdf -interaction=nonstopmode -halt-on-error \
      -file-line-error -recorder \
      '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' \
      "$entry.tex" > "$entry-review-build.txt" 2>&1 || exit 1
  done
)
python verify_artifact.py audit > verification.local.json
python independent_checks.py > independent.normal.json
python -O independent_checks.py > independent.optimized.json
cmp independent.normal.json independent.optimized.json
cmp independent.normal.json INDEPENDENT_CHECKS.json
```

Inspect `verification.local.json` for the expected tree, source counts, page counts, empty mismatch lists and log notices. Do not require equality of its rebuilt-PDF hashes with this session's hashes. Page rendering comparison uses the same renderer for the native and rebuilt files within a run. It is not a claim that every different font or rendering environment must produce byte-identical rasters.

Observed local toolchain: Python 3.13.5, PyMuPDF 1.26.7, latexmk 4.86, and pdfTeX 3.141592653-2.6-1.40.26 from TeX Live 2025/dev/Debian. Shell escape was disabled. PyMuPDF is optional for source verification but required for the PDF comparison section of the verifier. The exact mathematical controls use only the Python standard library.

## 4. Independent mathematical controls

`independent_checks.py` uses exact rational arithmetic and explicit runtime checks, not removable `assert` statements. Ordinary and optimized runs produced identical output. `INDEPENDENT_CHECKS.json` records:

- 2,790 geometrically admissible highest-degree blocks at orders 3–64; explicit inverses, determinant one, row-norm bounds, exponential corrections, and endpoint/interior multiplicities.
- 8,370 two-sided vector comparisons on fixed-lower-jet slices; finite factorial-weighted coefficient sums at orders 3–16.
- 117 finite alternating Jacobi systems at flight lengths 2–14; exact Green inverses, normalized cofactors and mixed Schur coefficients.
- 25 rational density-pair controls with separate recording factors and a nonzero cubic action coefficient; four-density cancellation, anchored signed recovery and mixed log derivatives.
- An inadmissible determinant-one negative control, an abstract identity-diagonal lower-triangular example, and a nonunimodular gain matrix of determinant six.

The density polynomial is an algebraic control, not asserted to be a realized billiard action. The lower-triangular example is not a billiard counterexample. The finite checks do not prove infinite-dimensional or arbitrary-order results. The report supplies independent mathematical reasoning for the scope and correctness judgments it makes.

SHA-256 identities of the four independently generated script/result files:

| File | SHA-256 |
|---|---|
| `independent_checks.py` | `2fb0914eebbf37f064d2980aa8dea0c605192026d2037585f0b91920803eedbb` |
| `INDEPENDENT_CHECKS.json` | `e1ef686370ec2be75dfbdae04568f37ff62b4330ad41b0ae1d0430f42519098b` |
| `verify_artifact.py` | `5fcb51e975658ccba847ea715d69d7048fe905d834a2a04c16187f20f7563bb2` |
| `ARTIFACT_VERIFICATION.json` | `a920353e4a254deddfe8a4d02c5f150a0c487a3b3403e8dcd4f1e3e7ae2d2e22` |

The author's `tools/check_revision_v58.py` was also run under ordinary and optimized Python with identical successful output. Its preservation and other inherited controls are author diagnostics. They were not substituted for the independent scripts above, and their statement/proof-block counts are not an independent semantic proof census.

## 5. Mathematical reading boundary

The source keys in the report locate the newly examined central proof interfaces. The principal conclusions are not judged from the response letter alone. In particular the relative normalization, terminal envelope, smooth finite-jet factorization, new coefficient-space estimate, density/window extraction, finite fiber's two inclusions, moving-reference derivative, local angular branch and finite-coordinate argument were examined at source level.

The direct full-manuscript estimation proof was examined with its declared calibration and test-implementation inputs. The complete calibration proof, every earlier finite-action/full-phase prerequisite, the full stopped/adaptive statistical catalogue and the companion's mathematics were not freshly certified. The entire source corpus was preserved and mechanically checked; preservation does not erase this mathematical coverage boundary.

The targeted primary-literature check covers the observation classes and version qualifications stated in the report. Finamore–Leguil's enriched datum and Theorem A were inspected on PDF pp. 4–5; the other cited primary records were checked at abstract/version-notice level. It is not an exhaustive priority search or a proof audit of all cited literature.

## 6. Review outcome and allowed inferences

The report accepts the scoped v58 block refinement within the examination performed, keeps the corrected acquisition dependency closed, and finds no new fatal core error within its stated coverage. It nevertheless recommends declining at the requested highest general-journal level on the present exceptional-significance case. Neither that placement judgment nor the successful diagnostics should be mistaken for a theorem about the correctness or incorrectness of every statement in the corpus.

No arbitrary deletion, new probability appendix, or unrelated stronger inverse theorem is requested as a repair. The report does not ask for an endless repair-only revision cycle. Its adverse placement judgment concerns the actual relative/smooth mechanism and the information regime in which its consequences are established.
