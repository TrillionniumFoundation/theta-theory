# Final main-manuscript PDF inspection

**Status: PASS for the stated author-side layout and selected-statement check.** No source files were edited during this inspection.

## Controlling artifact

- Source commit: `bc2952aa9a9695fe9985d491a4156b8975024285`.
- Paper tree: `497886b8961cf12001bbea66909757f93bb8d1ee`.
- Main PDF SHA-256: `05adc1704fec098ca74632c4d4e714a5b4a1d9f50f7de7077ff6b5c20bd78c53`.
- Actual page count: 42.
- Strict build receipt: `r75-build/final/BUILD_RECEIPT.json`, SHA-256 `c98123ee4d03768d8e8335971448288e240d5a57feec54059ab3e3739cfffdf9`; its declared commit, manuscript hash and page count match the inspected artifact.

## Rendered inspection

All 42 pages were inspected through seven six-page contact sheets. Pages 17-25 were also read at 125 dpi, covering the entire new nonabelian theorem chain, including the final equality and implementation paragraphs. The corrected first four pages were read at 125 dpi. No clipping, overlap, missing mathematical glyphs, equation-number collisions, or broken theorem/table layout was found in that scope.

The included contact sheets are generated from `draft-final-scope/paired/main.pdf`; this file is byte-identical to the final strict PDF. The comparison with the earlier inspected draft found changed pixels and text only on pages 1, 3 and 4. All other overview pages are identical at 65 dpi. Mathematical detail pages 17-25 were re-rendered from the final-scope file and are pixel-identical at 125 dpi to the pages already read. This transfer is recorded explicitly rather than claiming that unchanged rasters were independently read twice.

## Scope corrections checked in the final rendering

1. The abstract now states memory one at zero contrast and qualifies unchanged group/dimension by positive contrast.
2. The abstract's one-label stationary initialization charge explicitly assumes a finite classical realization.
3. The introduction defines the integer polygon bound through `K(alpha)>=3` and confines exact simultaneous optimality to the minimum `K=K(alpha)` with a maximizing phase.

The rendered sharp matrix lemma has `n>=5` and `t>0`, includes the complete null-vector case split and equality argument, and does not impose matrix symmetry. The exact memory theorem includes the zero-contrast exception, the attained closed threshold, and the necessary and sufficient nonuniform-weight factorization conditions. The statement explicitly classifies minimum permutation cores rather than all unreduced stochastic realizations. The unrestricted orbit-absorption and column-swap reduction, the S6 qualification, and the transpose convention in the prepared quantum realization are present and legible.

## Evidence and limits

`contacts/` contains seven compact sheets covering all pages. `detail/` contains full-page images for pages 1-4 and 17-25. `MAIN_PDF_QA.json` records hashes for every image; `PAGE_COMPARISON.json` records the rendering comparison.

This is an AI author-team visual check and selected mathematical reading. It is not an independent human referee report, proof-assistant certificate, exhaustive mathematical-priority review, or editorial decision. Contact-sheet coverage does not claim line-by-line verification of all inherited theorems. The evidence is valid only for the PDF hash and source commit above.
