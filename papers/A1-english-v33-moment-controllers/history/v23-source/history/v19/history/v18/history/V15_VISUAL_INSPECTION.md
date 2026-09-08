# Typesetting inspection — A1 v15

The complete 80-page manuscript was built locally with `pdflatex` in three passes. The build checks all source references and rejects undefined references or overfull boxes; the successful build has neither. A first-pass missing complex-number macro and one long inline phase formula were corrected before this inspected build. No mathematical content was removed for layout.

All 80 pages were rendered and inspected in five 16-page contact sheets for missing pages, abnormal blank areas, overlapping blocks and margin overflow. Pages 1, 8, 9, 23, 25, 26, 27 and 80 were additionally inspected as full-page raster images at approximately 119 dpi. This includes the title/abstract, both positive-history statements, the circular theorem and query metric, the complete weighted update and phase formulas, the general bounded-dual statement and the final references. The final minor hypothesis clarifications on pages 8–9 were rebuilt and re-rendered. No clipping, broken equation, overlapping theorem block or missing-glyph box was observed in these checks.

The main text uses the AMS article structure, numbered theorems and complete proofs, with technical implementation material in appendices. This inspection checks presentation, not mathematical correctness or compliance with every submission rule of a specific journal. It is not a line-by-line visual audit of all inherited appendix formulas.

The repository workflow rebuilds the same hash-verified source and deposits its own PDF and execution receipt. PDF byte hashes can differ between machines because of metadata and TeX versions; source identity and the actual PDF receipt must be checked separately.
