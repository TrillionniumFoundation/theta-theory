# Reproducing the A2 v169 review package

The authoritative publication is the complete plaintext LaTeX/Python/Markdown files and compiled PDFs committed on `revision/a2-v169-content-free-higher-contact-2026-09-26`. Compressed source-transfer pieces, when present, are transport only and are not the manuscript.

## Inputs

Complete predecessor tip: `27101d0c3c45703e1a4fa96001d11f6b059cfc5e`.
Controlling report: `f50f6a7b194adbb42813988d3e68a43d71ccc520`, blob `f84656b9a3b0a6be81b844b21b73efafe08c6d8a`.
First report: `be1987dd1a37064c0bea291d7ad38ccd12cc5951`, blob `b0523d8e6b294379de5a2679c116528063efc014`.

The v168 partial-transfer branch is not an input and is not overwritten. The build fetches the first report at its explicit commit because it is not an ancestor of the controlling report. The assembler validates both Git blob hashes, all three predecessor TeX SHA-256 hashes, every inherited mathematical block, and the complete old label set.

## Commands from the repository root

```sh
python3 papers/A2-v17-boundary-information-coarsening/article/v169/check_v169.py
python3 papers/A2-v17-boundary-information-coarsening/article/v169/assemble_v169.py --build
```

Use Python 3 with SymPy 1.14.0, pdfLaTeX with the standard LaTeX recommended/extra and font packages, and Poppler (`pdfinfo`, `pdftotext`, `pdftoppm`). The GitHub workflow records the actual versions and run/source identifiers. The first command reruns the entire v167 verification chain before the new finite exact checks. The second assembles three complete standalone sources, stabilizes companion cross-references, compiles all PDFs, tests the final logs, renders new theorem pages, and writes the receipts and review entries.

`--skip-inherited` and `--local-audit` exist only for explicitly marked local prepublication checks. The remote publication gate rejects an unrerun inherited chain or unvalidated report bytes. All checks are finite regression evidence, not certificates of the general proofs or originality.

The workflow stages only v169 outputs, its own workflow, and the new root review pointers. It checks the branch tip before a non-forced push. No historical manuscript, review branch, or other revision branch is modified. The complete previous root entries and manuscript front matters are preserved inside v169.
