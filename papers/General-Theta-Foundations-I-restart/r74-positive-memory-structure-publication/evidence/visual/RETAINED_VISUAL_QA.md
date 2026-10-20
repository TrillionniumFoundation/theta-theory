# R74 visual QA: supplement second half and retained companion

## Identity and scope

- Source commit supplied by the verified build handoff: `29b999abf11c43709e64be58765aa1984d13ac91`.
- Inspection completed (UTC): `2026-10-20T18:53:15.528391+00:00`.
- Inspector: author-team AI agent `/root/final_layout_retained`.
- Method: actual `view_image` inspection of the existing 96 dpi contact sheets, followed by actual full-page PNG inspection of selected dense or distinctive layouts.
- Result: **no visible layout defect identified within the coverage stated below**.

This record covers supplement pages 73–144 and the retained companion pages 1–37. Main-manuscript pages and supplement pages 1–72 are covered by other records. No mathematical correctness, priority, independent expert approval, or journal decision is inferred from visual appearance.

## PDF identities, recomputed from the actual files

| PDF | Total pages | Bytes | SHA256 |
|---|---:|---:|---|
| `General_Theta_Foundations_I_R74_Supplement.pdf` | 144 | 1293469 | `8dfa6a1d2edb1c7378259fe42e6b9f397fb11a9c3e0988ff1f0c1c47be28c0fc` |
| `General_Theta_Foundations_I_R74_Retained_Companion_R58.pdf` | 37 | 578400 | `5bdbe05bcb4955fc4dca36265457675fb94ef86c0ae5c54fd711548f5758c3a3` |

Both hashes were recomputed from the files in `r74-build-verified` and matched the build handoff.

## Actual visual coverage

| Document | Overview coverage through contact sheets | Full-page PNG details actually viewed |
|---|---|---|
| Current technical supplement | Pages 73–144 inclusive: six sheets, 72 page thumbnails | 90, 103, 112, 113, 132, 143 |
| Retained R58 companion | Pages 1–37 inclusive: four sheets, 37 page thumbnails | 1, 14, 26, 36, 37 |

The contact sheets actually opened were:

- `supplement/contact-073-084.jpg`
- `supplement/contact-085-096.jpg`
- `supplement/contact-097-108.jpg`
- `supplement/contact-109-120.jpg`
- `supplement/contact-121-132.jpg`
- `supplement/contact-133-144.jpg`
- `companion/contact-001-012.jpg`
- `companion/contact-013-024.jpg`
- `companion/contact-025-036.jpg`
- `companion/contact-037-037.jpg`

## Findings

- No visible page-edge clipping, overlapping text or formula blocks, malformed page geometry, missing-glyph boxes, or unintended blank PDF pages was identified within the stated visual coverage.
- Supplement page 103: compact three-column optimum table, equations, and equation numbers remain inside the text area with separated rows and columns.
- Supplement page 112: the six-branch displayed formula and its conditions are legible and separated; page 113: plot axes, tick labels, transition markers, and caption are visible with no overlap.
- Supplement pages 90 and 132: dense multiline operators and recursion displays have visible separation and stay inside the page margins.
- Supplement page 143 and companion page 37: dense bibliography entries, DOI/arXiv identifiers, and the long URL wrap within the text region in the inspected renders.
- Companion title page and pages 14, 26, and 36: title/abstract/footnotes, theorem displays, asymptotic formulas, and dependency arrows remain legible and separated.
- The unused grey cells in companion/contact-037-037.jpg are contact-sheet padding, not blank document pages.

## Limits and evidence classification

- This is author-team AI visual layout inspection, not independent human referee review, a mathematical proof check, formal verification, or an editorial decision.
- The overview covers every requested page through contact-sheet thumbnails. It does not claim a full-size, line-by-line reading of every page. Full-page detail inspection is limited to the explicitly listed pages.
- The reviewed images are the existing 96 dpi renders. Fine print defects below this render resolution and subtle textual or mathematical errors are outside the assurance provided.
- No sealed paper source was edited. No LaTeX compile or mathematical diagnostic was rerun in this task.
- The source commit association is the parent build handoff; this task independently recomputed both PDF hashes, but did not regenerate the PDFs from source.

No source correction is requested by this layout inspection. This is a bounded visual QA finding; it is not a claim that every word or symbol in all 109 covered page thumbnails was read at full size.
