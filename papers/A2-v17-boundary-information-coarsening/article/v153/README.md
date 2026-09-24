# A2 revision 153

**Article:** *Finite failure schemes and the reconstruction of quadratic pencils*, Qian Qi.

**Branch:** `revision/a2-v153-global-incidence-fibre-structure-2026-09-25`.

The controlling report is the independent report on revision 152 at commit `60f1a3c5f8078c31019dfab249d334d0e717e225`. See [the response](RESPONSE_TO_V152_REPORT.md) for all twenty technical comments and the request for a global structural theorem.

## Referee reading order

Begin with the revised [introduction](introduction-v153.tex), then the new [structural results and full proofs](new-core.tex). The full native article is `geometry.tex` and its compiled review copy is `geometry.pdf`, produced by the branch-specific build. A successful `BUILD_RECEIPT_V153.json` identifies the exact source commit and PDF hash. A source-only state is not a successful full build.

The additions are a global conductor and multiple-branch theorem on the binary squarefree locus; all binary normalization fibres and their finite flat strata; a simultaneous formal collision atlas; the evaluated singular Fitting ideal in every double-root rank; and the complete minimal relation representation and complete-intersection classification for arbitrary-dimensional pure-power fibres.

## Build

From this directory in a checkout containing the controlling reviewed commit:

```sh
python3 check_v153.py
python3 assemble_v153.py --build
```

Requirements: Python 3.10 or later, SymPy, a LaTeX installation with the inherited AMS packages, and Poppler. The assembler verifies all inherited files against the reviewed Git tree, changes no v152 input, and writes a self-contained principal source. All original principal parts, labels and mathematical blocks are retained. Detailed families, recognition and spectral proofs are in the article appendices. The separate applications and non-submitted archive remain at their original v152 paths.

The receipts distinguish exact finite checks, source preservation and actual compilation from proof validity. The Ballico 1993 full-text comparison remains documentary-open in the submitted introduction; no priority or acceptance conclusion is manufactured.
