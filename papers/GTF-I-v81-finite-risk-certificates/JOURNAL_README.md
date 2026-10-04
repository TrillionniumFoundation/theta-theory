# Standalone journal submission — Revision 81

`paper.pdf` is the focused mathematical article. `STRUCTURAL_PAPER.pdf` is its independent structural companion. The package includes both complete active LaTeX source graphs, the response to the controlling R51 reports, the current literature audit and independent review brief, and a standalone verifier. The complete historical research edition is available in the research package.

With pdfLaTeX, its standard article and mathematical packages, and PyMuPDF 1.26.6 installed, run:

```sh
python journal_verify.py
```

The verifier checks the manifest's exact native-source identity and all included file hashes. It then copies the two articles' active sources into an empty temporary directory, compiles each article three times with `SOURCE_DATE_EPOCH=1791158400` (5 October 2026, 00:00 UTC), and compares every rebuilt page's text and raster with the submitted PDFs. It rejects unresolved references, citations and typesetting boxes, and verifies that the submitted files were not changed. Raw font-engine warnings may remain in the compiler output.

Neither article needs another repository file or a historical PDF. The archive intentionally contains no complete historical main manuscript, predecessor audit tree, or finite-regression dependency. `JOURNAL_MANIFEST.json` identifies the native source commit, the two submitted documents and the full file inventory.

Reconstruction establishes source and page identity. It does not independently certify mathematical correctness, novelty, human authorship or an editorial decision. The effective learners are mathematical finite-procedure results. Section 64 gives a rational readout with a finite uniform-risk certificate; the separately distributed research replay exercises have their stated finite scope. This package does not claim execution of a general optimal synthesis or physical learner.
