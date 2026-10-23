# Actual PDF visual inspection — R79

This is an internal author production check of the exact PDFs built from source commit `90cae2f5aca243b39d3a2194a4d6e0696671a101`. The three signed-off scope notes below record images actually opened and viewed; successful raster generation alone was not treated as inspection. No blocking layout defect was observed within the stated coverage.

| Document | All pages inspected at thumbnail scale | Pages additionally inspected as readable individual rasters |
|---|---:|---|
| Main article | 1–59 | 1, 3, 7, 9–20, 40, 54, 59 |
| Technical supplement | 1–190 | 1, 89, 124, 138, 170, 190 |
| Retained R58 companion | 1–37 | 1, 12, 25, 37 |

All **286 pages** were therefore checked at contact-sheet scale; **28 pages** received individual readable-page inspection. The main article's new support, regularization, perturbation, uniform frontier, positive-success and exact-model proof sequence, pages 9–20, was inspected in its entirety at detail scale. Manuscript page 24 was also rendered, but it was not among the images recorded as actually inspected; no additional inspection claim is made for that render.

- [Main opening and inherited-content visual record](visual-qa/R79_ROOT_VISUAL_QA.md).
- [All twelve current core-proof pages](visual-qa/R79_CORE_VISUAL_QA.md).
- [Retained supplement and companion](visual-qa/R79_RETAINED_VISUAL_QA.md).
- [Exact render receipt](visual-qa/RENDER_RECEIPT.json), including input PDF identities, render page sets and all 42 contact/detail PNG hashes.
- [Original rendering script](visual-qa/render_r79_original.py), preserved exactly as executed. Its `B` and `O` paths are the original local build and output locations. For reproduction, set `B` to this publication directory and `O` to a fresh output directory; `BUILD_RECEIPT.json`, `THEOREM_INDEX.json` and the PDFs are all provided. It requires Poppler `pdftoppm` and Pillow. Rendering at the same DPI and with the same versions reproduces the layout; byte-identical PNG output on a different software stack is not promised.

The PNG working files are reproducible from the deposited PDFs and script and are not separately deposited. Their recorded hashes identify the actual local renders viewed during this check. The PDFs, every scope note, the script and the complete render receipt are deposited. Native compilation and warning checks are separately recorded in the build receipt and raw logs.

This inspection does not claim that every glyph on every page was read at detail scale. It does not test all clickable links, accessibility tags, print output, mathematical correctness, priority, human expert approval or editorial acceptance. The checks are author-side AI-assisted production work, not a new independent referee report.
