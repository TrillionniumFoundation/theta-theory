# Main manuscript draft03: completed rendered layout QA

## Identity and scope

This receipt records author-team AI **layout QA**. It is not a mathematical
proof audit, proof-assistant verification, human expert assessment, independent
referee report, or editorial decision. The reviewer did not edit manuscript
source or the PDF.

- Input: `/workspace/scratch/f856e3d63ac5/r76-build/draft03/General_Theta_Foundations_I_R76.pdf`
- SHA256: `32f0f7c69c99c789305430ee888b80ed455e41dab7a1e6d4fe25e497dcb64925`
- Size: 615,028 bytes; 34 unrotated US Letter pages, 612 by 792 points.
- Reviewer task: `/root/r76_structural_math`.
- Date: 2026-10-21 UTC.

## Actual inspection and comparison coverage

All 34 pages were rendered by Poppler at 144 dpi to 1224 by 1584 PNGs.
Decoded RGB pixels of every page were compared with the corresponding page
of the previously inspected 35-page draft02. The comparison is recorded in
`DRAFT02_COMPARISON.json` and gives:

- **Pixel-identical pages:** 1–10 and 12–31, 30 pages in total.
- **Changed pages:** 11, 32, 33 and 34.
- Draft02 page 35 has no separate page in draft03; its final reference was
  retained and moved onto page 34.

Every changed draft03 page was individually opened and visually examined at
the original 144-dpi render size. Page 31 was also directly viewed, so the
new direct inspection set is **11, 31, 32, 33, 34**.

The 30 pixel-identical pages inherit the actual rendered inspection described
in `../visual-main-draft02/VISUAL_QA.md`: all 35 old pages were opened on nine
contact sheets, and old pages 10–18, 20–27 and 32–35 were additionally opened
individually at 144 dpi. This supplies rendered visual coverage of every
draft03 page, with direct enlarged inspection of all new proof and formula
pages. It does not pretend that unchanged pages were reopened unnecessarily.

The effective individual-page coverage of this final draft is 10–18, 20–27,
31–34, totaling 21 pages. Of those, 16 use the pixel-identical prior view and
five were directly viewed in draft03. The remaining pages have the prior
contact-sheet visual inspection and demonstrated pixel equality.

Nine new contact sheets were generated for reproducibility and convenient
review; this receipt does **not** claim they were separately opened, because
the actual new visual review used the individual page images and exact
comparison with the already viewed draft02 images.

## Findings and their disposition

| Previous finding | Draft03 disposition | Visual evidence |
| --- | --- | --- |
| MAIN-D02-01: missing space in the page-11 infimum subscript | **Resolved.** The phrase now visibly reads `pure-start controllers on at most M labels`. | Direct inspection of draft03 page 11. The mathematical display is contained within the margins and remains readable. |
| MAIN-D02-02: a two-line reference alone on page 35 | **Resolved.** Reference [80] is now fully present at the bottom of page 34. | Direct inspection of draft03 pages 32–34. The slightly reduced reference leading leaves every line distinct and legible; the final entry and lower margin are intact. |

The earlier findings and receipt remain preserved, rather than rewritten to
pretend the first draft was defect-free.

**Final visual result:** no unresolved layout defect was observed within the
inspection above. No clipping, overlapping displays, missing-glyph boxes,
illegible equation numbers, broken running headers, or corrupted reference
glyphs was seen. The corrected display and all references are readable. The
unchanged new theorem/proof displays preserve their previously inspected
layout, including the wide equations (4.8), (5.1), (5.8)–(5.12) and the
stopped-experiment formulas (7.1)–(7.17).

## Supporting records

- `RENDER_MANIFEST.json`: PDF hash and SHA256 of all page renders and contact sheets.
- `DRAFT02_COMPARISON.json`: exact decoded-pixel comparisons, including changed
  bounding boxes and both versions' page-image hashes.
- `VISUAL_QA_RECEIPT.json`: machine-readable inspection coverage and issue disposition.
- `pdfinfo.txt`, `pdffonts.txt`, `pdftoppm-version.txt`: actual metadata/tool outputs.
- `TEXT_AND_METADATA_CHECKS.json`: 34 pages, no empty extracted page and no
  literal `??` unresolved-reference marker; all listed fonts embedded.
- `OBSERVED_TEX_SOURCE_HASHES.json`: hashes of the 13 local TeX inputs named by
  the draft03 recorder file, observed at QA time, together with hashes of the
  draft build receipt and recorder file.

Selected observed source identities are:

| File | SHA256 |
| --- | --- |
| `main.tex` | `896fddcc893223ddfa1fa890c12d7e31090b24eb105ad73e549e62f692276ed4` |
| `preamble.tex` | `8b1c66a794432872cc04d411eea9024084c2bbb3bd848e99f77f1008cc3dd890` |
| `references.tex` | `ce00ad200039927c51db5bfd759d1088b62b0447645010333b6e2d3c2ce6387c` |
| `sections/45-convex-specifications.tex` | `2ddf7eda8686a7bc3b9d2c22b9ee4a1f25353f7d341fb0316ae42de0924018ad` |
| `sections/46-mean-contrast.tex` | `5099e707cb0f7b04d59b2411127138abb14da8070b6b304e780da5aaef877e1a` |
| `sections/47-rare-branch-approximation.tex` | `8559ff7c0b6b85c390a49b7591f86a0294e2620be727546f98a3ee81bc3f6374` |
| `sections/48-physical-approximation-lower.tex` | `5a8ad91ae3e177bbe6d8587bec1ed8be7705358e050a8bccd51b058057d96fa5` |

These are observed content hashes, not an assertion that a draft build
authenticated a committed source. The manuscript's strict source/build
identity is checked by its separate verification process. Bibliographic
correctness and mathematical priority were not re-audited by this layout task.

## Applicability to final publication

If the final strict main PDF has SHA256
`32f0f7c69c99c789305430ee888b80ed455e41dab7a1e6d4fe25e497dcb64925`, it is
byte-identical to this inspected PDF and the visual result applies directly.
No such later equality is assumed by this receipt. If the final bytes differ,
compare the renders and inspect the changed pages before reusing the result.
