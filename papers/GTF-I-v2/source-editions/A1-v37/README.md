# A1 v37 — publication revision

**Attainable information and causal compression at exponent collisions**  
Qian Qi — 9 September 2026.

Branch: `revision/a1-english-v37-publication-2026-09-09`.  
Controlling v36 report: `1e7af61f0812638d00ee0efad8fc9a68e2776c3c`.  
Reviewed manuscript: `8f074b8027627a71a81a362b9d15f47975e1f3ae`.  
Compiled publication source: `616904c0f151b51e75b8a09fb98c25b65209975a`.

## Reading entry points

`main.tex` is the complete English article; `companions.tex` is the complete companion. The current native PDFs have **42 and 159 pages**, respectively. The v36 report recommends acceptance of the main article and requests no further mandatory mathematical revision. This is an independent referee-style recommendation, not a named journal's publication decision.

Read `RESPONSE_TO_REFEREE_V37.md` for the disposition of the report, and `PROOF_LEDGER_V37.md` for preservation and proof provenance. The exact controlling report is copied to `review-basis-v36/REFEREE_REPORT.md` in the repository. `REVIEW_SOURCE.json` pins its original commit, path and blob.

The mathematical text is unchanged: all **222 theorem-like blocks and 210 proof blocks** are verbatim. Among the 80 active TeX files, only the edition date in `main.tex` changes. `CHANGES_FROM_V36.diff` displays that entire TeX change. The new directory inherits the entire v36 Git subtree, including inactive historical derivations. Stable module and theorem labels containing earlier version numbers are intentional.

## Reproduce

With Python, a complete TeX Live installation, SymPy and mpmath:

```sh
python build.py --source-commit 616904c0f151b51e75b8a09fb98c25b65209975a
python v37/verify_publication.py > /tmp/a1-v37-checks.json
python -O v37/verify_publication.py > /tmp/a1-v37-checks-O.json
cmp /tmp/a1-v37-checks.json /tmp/a1-v37-checks-O.json
```

The source-commit argument identifies the fixed compiled mathematical source. The later publication-evidence commit does not change those inputs. The recorded execution environment is in `verification-v37/ENVIRONMENT.json`.

The builder cleans generated entrypoint products, compiles both full volumes, exports actual labels, checks convergence and source-recorder agreement, and rejects unresolved final references or overfull boxes. The verification script reconstructs the pinned v36 source manifest, permits only the recorded date change, compares all mathematical blocks, and replays the four unchanged mathematical diagnostics in both Python modes.

With PyMuPDF and the v36 PDFs in a separate directory, the all-page comparison is reproducible:

```sh
python v37/compare_pdfs.py --baseline /path/to/v36-pdfs
```

The baseline directory must contain `main.pdf` and `companions.pdf`. At 72 dpi, all pages except the changed main title-page date are text- and pixel-identical. Manual inspection is recorded separately and is not represented as an enlarged inspection of every page.

## Verification and artifacts

`verification-v37/NATIVE_BUILD_V37.json` identifies the actual current native build and its source manifest. `PRESERVATION_AND_REPLAY.json`, `PDF_EQUIVALENCE.json` and `VISUAL_INSPECTION.json` record distinct checks. Historical receipts retain their historical scope and are not substituted for this execution.

The downloadable native package includes all current compilation inputs, both PDFs, the complete current execution receipt and compiler logs. The repository preserves the larger inactive historical source tree as well. PDF binaries need not be committed to reconstruct this publication object.

The proofs remain in the manuscript. Compilation, finite diagnostics, source preservation and a favorable referee report are not formal proof-assistant verification or a guarantee of publication.
