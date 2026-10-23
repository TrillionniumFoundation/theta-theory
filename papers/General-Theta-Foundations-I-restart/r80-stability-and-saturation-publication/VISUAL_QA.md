# Actual visual inspection of the R80 publication

The three PDFs are the exact outputs of the completed strict build at source commit `c0ac246181c2f4214e3e830952386adffb7d82df`. All image inspections below were actually performed. Rendering by itself was not counted as inspection.

| Document | All pages viewed at contact-sheet scale | Pages additionally viewed as readable 110-dpi individual images |
|---|---|---|
| Main article | 1–73 | 1, 3, 9, 19–33, 68, 73 |
| Technical supplement | 1–196 | 1–7, 94, 130, 144, 176, 196 |
| Independent R58 companion | 1–37 | 1, 12, 25, 37 |

Thus all **306 pages** were viewed at thumbnail scale and **36 pages** at readable detail scale. The full new main proof span (20–32) and full two-location supplement refinement (1–7) received individual-page inspection. No blocking production defect was observed within this coverage. A nonblocking cosmetic wrap remains on main page 26: the word “row” occupies a short line before equation (6.2). It is fully legible and changes no formula or argument.

- [Root main-article coverage](visual-qa/R80_ROOT_VISUAL_QA.md).
- [Complete new main proof sequence](visual-qa/R80_CORE_VISUAL_QA.md).
- [Complete two-location supplement refinement](visual-qa/R80_SEARCH_SUPPLEMENT_VISUAL_QA.md).
- [Retained supplement and companion coverage](visual-qa/R80_RETAINED_VISUAL_QA.md).
- [Actual render receipt and image hashes](visual-qa/RENDER_RECEIPT.json).
- [Exact rendering script](visual-qa/render_r80.py).

The render receipt binds all 51 contact/detail images to exact input-PDF hashes. PNG working files are reproducible and are not separately deposited. To render the deposited files into a fresh directory, run `python3 -B visual-qa/render_r80.py --build . --out /tmp/theta-r80-render-reproduction` from this publication directory, with Poppler and Pillow installed. Image bytes on a different rendering stack are not promised identical.

The notes distinguish each inspector's actual coverage. They are internal AI-assisted author production checks, not human referee reports. Thumbnail inspection does not mean every glyph was read at full scale. This process does not verify all hyperlinks, accessibility tags or physical print output, and does not establish mathematical correctness, novelty, human expert approval or editorial acceptance. Native compiler checks are recorded separately.
