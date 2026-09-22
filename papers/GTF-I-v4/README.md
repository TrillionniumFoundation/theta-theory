# General Theta Foundations I — fourth revision

The complete article is `paper.pdf`; the native entry point is `main.tex`.

This edition responds to the v3 report at `d084e3cf505f3978ddaab9b954aac94b97fe7bd3`. It adds a general posterior-orbit realization theorem, a sharp noisy expanding-renewal law with a uniform critical window, and calibrated collision-moment minimax laws. It retains the preceding mathematical development and proofs. It does not modify main, any preceding revision, or the review branch.

Start with `RESPONSE_TO_REFEREE.md` for point-by-point answers and `PROOF_LEDGER.md` for exact dependencies. `HISTORY_AUDIT.md` and `HISTORY_INPUT_MANIFEST.json` identify the historical sources. `LITERATURE_AUDIT.md` specifies theorem-level comparisons. Compiled theorem/page locators, source identity, and executed checks are in `evidence/BUILD_RECEIPT.json`.

## Rebuild

From a repository checkout:

```sh
python3 papers/GTF-I-v4/build.py
```

Requirements: Python 3 standard library, pdfLaTeX with the packages used by the preserved preamble (TeX Live recommended), and Poppler `pdfinfo`. The build uses no network. It validates `SOURCE_MANIFEST.json`, runs new and inherited diagnostics, rejects four negative controls under both ordinary and optimized Python, compiles until references stabilize, rejects unresolved references and overfull boxes, checks all retained mathematical labels, and writes the PDF and evidence.

The independently rebuildable archive `evidence/COMPILED_SOURCES.zip` contains repository-relative native source paths. Extract it into an empty directory and run the same command. `GTF_SOURCE_SHA` is supplied only for an actual Git checkout at that immutable commit; an archive-only rebuild leaves the commit field null rather than inventing an identity. In CI, source commit and later generated-product publication commit are distinct.

`SOURCE_MANIFEST.json` binds input bytes and records preserved Git trees; it deliberately does not hash itself. Generated PDFs, logs, receipts, and archives are not mathematical inputs. Prior editions are imported by their original relative paths and are not duplicated or rewritten.

The manuscript is supplied for another referee round. A successful build is not a formal proof certificate or a representation of acceptance by any journal.
