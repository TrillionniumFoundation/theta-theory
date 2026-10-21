# R75 supplement and retained companion: author-side visual inspection

## Actual inspection scope

The assistant inspected all supplement PDF pages 1–157 through fourteen contact sheets, and all retained companion PDF pages 1–37 through four contact sheets. The overview rasters were rendered with Poppler pdftoppm at 60 dpi and arranged as twelve thumbnails per sheet. This is an overview of every page, not a claim that every page was read at full size.

At 150 dpi the assistant additionally inspected:

- Supplement page 1: current-supplement identity, inherited-content statement, Theorem S1.1, target expected-call hypothesis, nontermination block, and equations (S1.1)–(S1.2).
- Supplement page 2: the one-call trace bound, target-prefix telescoping bound, stopped-law limit, and initializer/product-policy accounting.
- Supplement page 3: approximate-cost qualification, zero-call endpoint, inherited arithmetic consequences, and transition to the retained exact-synthesis material.
- Supplement page 125: retained Figure 1, algebraic transition labels, axes, caption, and surrounding text.
- Companion page 1: title, abstract, introduction, date, classification, and keywords.

## Observations

No visible clipping, overlapping text or equations, missing pages, large unexplained blank regions, or broken-glyph blocks were detected within this scope. The short final supplement page contains the concluding bibliography entries; it is not an unexplained missing-content page. The stopped-law theorem continues normally across pages 1–2, and its proof and scope clarification continue across pages 2–3. Display equations and labels on the detailed pages are legible and inside the text area. The retained figure's tick labels, transition labels, and caption remain legible.

## Identity and limits

The overview PNGs and first-page detail PNGs were rendered from draft03. The hashes below were independently recomputed and match the corresponding strict-release PDFs byte-for-byte, so these exact rasters describe the same documents. Figure page 125 was rendered directly from strict-release. Final publication binding is recorded separately in FINAL_PDF_BINDING.json after recomputing the final build's PDF hashes and checking its actual build receipt.

- Supplement PDF SHA-256: 19a2aa4e9db4bd13feaa7339cf13a0425d34c750882ccbecc41244368e24d52d; 157 pages.
- Retained companion PDF SHA-256: 5bdbe05bcb4955fc4dca36265457675fb94ef86c0ae5c54fd711548f5758c3a3; 37 pages.

The evidence archive contains lossless WebP copies of the inspected rasters; every decoded RGB image was verified byte-for-byte against its PNG. RASTER_MANIFEST.json fixes their file and pixel hashes. No manuscript source was edited during this inspection.

This is author-side model-assisted layout inspection. It is not independent human referee review, proof-assistant verification, a mathematical completeness certification, or a hosted CI run. Native-build results belong to the separately identified build receipt; they are not inferred from these images. The mathematical proof audit is a separate record.

## Verified final source binding

The actual final build receipt reports PASS for source commit bc2952aa9a9695fe9985d491a4156b8975024285 and paper tree 497886b8961cf12001bbea66909757f93bb8d1ee. Both final PDFs were reopened, page-counted, hashed, and compared byte-for-byte with draft03 before marking the binding complete. Their hashes are the two listed above. This statement cites the actual local native-build receipt; it is not a hosted CI claim.
