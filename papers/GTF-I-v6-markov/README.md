# General Theta Foundations I — sixth Markov revision

**Author:** Qian Qi. **Date:** 22 September 2026.

Working branch: `revision/general-theta-foundations-i-v6-markov-2026-09-22`.
Frozen referee branch: `revision/general-theta-foundations-i-v6-markov-referee-ready-2026-09-22` (created after publication verification).

The controlling report is the v5-intrinsic report at `ee210f3cfe3b4923ef51310e20cd8b20a6a367e1`, not the earlier v4 report.

## Reading editions

`principal-paper.pdf`, compiled from `principal.tex`, contains the new Markov-renewal, critical, nonregenerative posterior and operational theorems, together with the complete retained posterior-orbit converse they invoke.

`paper.pdf`, compiled from `main.tex`, contains the same chain plus the current A2 finite-register application and every preceding quantitative/foundational proof body. Old sources are included without modification; the full and principal views use the same core TeX and have identical core theorem/equation numbering. The old editions and original introductions remain in their original directories.

Start with `RESPONSE_TO_REFEREE.md`, then the proofs in `markov-model.tex`, `renewal-suffix.tex`, `markov-pressure.tex`, `critical-renewal.tex`, and `nonregenerative-filter.tex`. `operational.tex` proves the finite-interface simulations. `a2-finite-budget.tex` proves the new sample/alphabet bound in the full edition. `PROOF_LEDGER.md` gives the dependency and constant audit.

`HISTORY_AUDIT.md` distinguishes the eleven-paper historical snapshot from the active A1-v37 and A2-v118 snapshots. Selected A2-v118 files are preserved under `history-sources/` for consultation only, not compiled into the new proof. `LITERATURE_AUDIT.md` records the primary literature comparison, including published 2026 theorem pages.

## Rebuild

From a repository checkout or a standalone source archive preserving repository-relative paths:

```sh
python3 papers/GTF-I-v6-markov/build.py
```

Python 3, `pdflatex`, `pdfinfo`, the standard AMS/LaTeX packages and Latin Modern fonts are required. No network or third-party Python dependency is required by the build. The hash-bound manifest intentionally rejects edited inputs: after intentional source edits, regenerate `SOURCE_MANIFEST.json` with `refresh_manifest.py` before rebuilding. This does not certify those edits mathematically.

The build checks every input digest, prior-source preservation, both complete reference graphs, core numbering, normal/optimized finite diagnostics, eight negative controls and inherited diagnostic suites. It writes PDFs, `evidence/BUILD_RECEIPT.json` and `evidence/COMPILED_SOURCES.zip`. When running in Git, it additionally checks the exact mathematical-source HEAD, controlling report blob and allowed new-only diff. It does not mutate any old paper source.

Native mathematical source and generated publication artifacts are committed separately. The root `GTF_I_V6_MARKOV_INDEX.md` records their exact identities, pages and hashes after the build. Rendering and independently downloaded archive checks are recorded separately. Build results are not formal proof certificates, independent refereeing, priority determinations or journal acceptance.
