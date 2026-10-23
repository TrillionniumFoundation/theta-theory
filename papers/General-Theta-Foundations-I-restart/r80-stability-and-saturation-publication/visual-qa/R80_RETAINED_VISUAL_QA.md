# R80 retained supplement and companion: rendered-page visual QA

Inspection completed on 23 October 2026, at approximately 14:08 UTC.

**Disposition:** no blocking layout defect was observed in the assigned coverage. This is an author-side AI production inspection of rendered pages. It is not an external referee report, human expert assessment, formal verification of the mathematics, or an editorial decision.

## 1. Exact build identity

The inspected renders were supplied from the strict native build in `r80_verified_build/`. The build receipt records source commit `c0ac246181c2f4214e3e830952386adffb7d82df`, status `PASS`, verified source identity, and unchanged source during compilation. The actual PDF files were independently hashed during this visual inspection and their hashes matched the receipt.

| Item | Recorded identity |
|---|---|
| Source commit | `c0ac246181c2f4214e3e830952386adffb7d82df` |
| Paper source Git tree | `d9d760358cc951be5dff54c4495810d4bd342185` |
| Source manifest SHA-256 | `e7693ca75ad1db8d45340762572cbff0992d8af6891d1f4192a8aaae120cd0f7` |
| `BUILD_RECEIPT.json` SHA-256 | `07c664d82fcb4700caf68c619e40883c21f505ab652b7ff87af5d47e2094bfd4` |
| Native build completed | `2026-10-23T14:03:48.745351+00:00` |

| Inspected PDF | Pages | Bytes | SHA-256 |
|---|---:|---:|---|
| `General_Theta_Foundations_I_R80_Supplement.pdf` | 196 | 1,643,287 | `14553246ed4f807a1382a9a78419008dbc658fad1bff714c11628c9815c5354b` |
| `General_Theta_Foundations_I_R80_Retained_Companion_R58.pdf` | 37 | 578,400 | `5bdbe05bcb4955fc4dca36265457675fb94ef86c0ae5c54fd711548f5758c3a3` |

The native receipt's compile and diagnostic results are distinct evidence from the visual inspection documented here. This note does not establish a GitHub Actions result.

## 2. Actual visual coverage

All eleven contact-sheet images below were opened and visually inspected at their original 1650 by 1540 pixel resolution. Each full sheet contains six columns and four rows of page thumbnails. Labels identify physical PDF page numbers, not section numbers. Unused gray cells on the final sheets are contact-sheet background, not blank PDF pages.

| Image in `r80_visual_qa/` | Physical PDF pages actually viewed | Overview result |
|---|---:|---|
| `supplement-contact-01.png` | 1–24 | Consistent title, section, theorem and proof layout; transition from the new two-location refinement to the retained body is visible. |
| `supplement-contact-02.png` | 25–48 | Text and displayed mathematics remain within the page body. |
| `supplement-contact-03.png` | 49–72 | No visible page-level break, overlap or clipping. |
| `supplement-contact-04.png` | 73–96 | Headers, equations and text blocks remain separated and inside margins. |
| `supplement-contact-05.png` | 97–120 | Dense proofs and displayed formulae show consistent page geometry. |
| `supplement-contact-06.png` | 121–144 | No visible overlap or page-edge overflow; selected dense pages received the individual inspection below. |
| `supplement-contact-07.png` | 145–168 | Figure on page 164 is present with its caption; no visible displacement or overlap at overview scale. |
| `supplement-contact-08.png` | 169–192 | Retained later sections are present with consistent headers and margins. |
| `supplement-contact-09.png` | 193–196 | Four bibliography pages are present; final page ends normally. |
| `companion-contact-01.png` | 1–24 | Title, abstract, theorem/proof text and equations have a consistent retained article layout. |
| `companion-contact-02.png` | 25–37 | Final body, appendices and bibliography are present; no unexpected blank page or overflow is visible. |

Thus all **196 supplement pages and all 37 retained companion pages** received page-level visual overview. The contact-sheet scale is not sufficient to verify every mathematical symbol, line break, citation or word. The following nine separately rendered pages were additionally opened and inspected at their original 935 by 1210 pixel resolution, where the body text and mathematical displays are readable.

| Individual image | Content visible in the inspected page | Readable-page observations |
|---|---|---|
| `supplement-page-094.png` | Section S26.1, primitive interface and universal termination; Theorem S26.1 | The theorem, support notation, fallback operators and proof opening are legible; multiline mathematics and the bottom proof display stay inside the margins. |
| `supplement-page-130.png` | Section S32.3; Theorem S32.3 and equations (S32.7)–(S32.10) | Equation numbers are separated from the formulae; the finite-label bound and qualification at the bottom are fully visible. |
| `supplement-page-144.png` | Lemma S36.1; Section S36.2; Theorem S36.2 | Reachable-support equations, aligned inequalities and theorem text are legible and do not collide with one another or the running header. |
| `supplement-page-176.png` | Section S46, preparation faces and reachable supports; Theorem S46.1 | The section transition, aligned certificate conditions and continued proof are well separated; all visible lines remain within the page. |
| `supplement-page-196.png` | Final bibliography entries [80]–[98] | Bibliography text and DOI/URL wraps are legible and contained; the added search/control references at the end are visible without truncation. This is a layout observation, not an independent verification of every bibliography item. |
| `companion-page-001.png` | Retained companion title, author, abstract, introduction and title-page footnotes | The original research identity is displayed clearly; title, abstract, introduction, date, classification and keywords do not overlap. |
| `companion-page-012.png` | Equation (7.1), its proof, and Proposition 7.2 | Formulae, proof-ending square, proposition heading and continuing proof are readable with no visible clipping. |
| `companion-page-025.png` | Corollary 14.4 and Section 15, nonintervening Gaussian sensing | The norm display and equations (15.1)–(15.3) fit within the text width; the section transition is clear. |
| `companion-page-037.png` | Final references [1]–[17] | Complete visible entries fit within the text block; the final reference and normal trailing white space are present. |

## 3. Findings and limits

No visible missing page, unintended empty PDF page, page-edge clipping, grossly overfull formula, displaced running header, overlapping text, or black replacement-glyph block was found in the inspected coverage. The nine individual pages show readable prose and mathematical typography. The bibliography has a smaller type size than the main body but remains readable in the inspected individual renders. The consistent dense mathematical layout is appropriate to these technical retained materials; no source or PDF edit was made during this inspection.

This record does not claim a line-by-line visual proofread of all 233 pages, verification of every glyph at native print resolution, checking of all hyperlinks, or validation of figure data and mathematical assertions. It does not cover the 73-page current main manuscript. Readable inspection of the new supplement opening pages was assigned separately and is not claimed as work performed in this note. Rendering, successful LaTeX compilation, finite numerical diagnostics and source-level proof review are different activities; none is substituted for another here.

## 4. Inspected image identities

These hashes pin the actual images that were opened, so later regenerations cannot silently be treated as the same inspected artifacts.

| Image | SHA-256 |
|---|---|
| `supplement-contact-01.png` | `8621cbedea70b206bd3dd05d7b99391430df6ea661b8f0244e4abb5bcca324a3` |
| `supplement-contact-02.png` | `f72f126bab4057b77f15e0d4074257bf1467679ba3e3c9739f065923e1dd93d5` |
| `supplement-contact-03.png` | `a3a60981d886fca29284f9685437669b116bac3826a05ab49cd70a6d349ed209` |
| `supplement-contact-04.png` | `603b6e8f10ecfb94757147c897af6d858dac74e80b3df6e1b5a016c747184904` |
| `supplement-contact-05.png` | `2314e92df5e423ddc8a3201df39308a06bee7b19a6e50d65790cd9fe39897669` |
| `supplement-contact-06.png` | `0973bd0eca9fb6397f6987c89667dc448b8803512e4f017b329b98ea8b23de98` |
| `supplement-contact-07.png` | `87b4311a727fb8c99414aeb9e78355107cd3e377892d93415e6b56ba0b0c469c` |
| `supplement-contact-08.png` | `933be2ad2dd3b046c7c96eaf9ce59f64169e2057005284c23f7a3e176fc7e970` |
| `supplement-contact-09.png` | `2eb9892d22da0156342229c3cd9cee174528b01c6c6c99b705b84ba01e4d9927` |
| `companion-contact-01.png` | `24ed72af1f27a2c30db8ee0df42a1a4976fb2e7a2079d1c3377a8e0b897b2cbc` |
| `companion-contact-02.png` | `9de27034faf215d9e5cfb45d8f4e85f1d0ea21ae695b0a439a8ab786eea9f7bc` |
| `supplement-page-094.png` | `8814cde08b4061ff5fffc645678ac51396f7f6fe2e13f658ef48423c296c0e7a` |
| `supplement-page-130.png` | `730ccd39e5f7705ca92fb1dd5434fdeede3f87cd45e56d57f35f6db0c02533bb` |
| `supplement-page-144.png` | `dfe5d587c73140d96a70564286197412ecb4902883895815f350aa7aff4c81ca` |
| `supplement-page-176.png` | `2def732f3309e51dd538fe2f66427b473bf232fe8d5cb9324027e644ecfc68fe` |
| `supplement-page-196.png` | `7f59f446c96c2b6d12d0258ce340f91c0c4b8e59217e51c89b6ed459f5d4609c` |
| `companion-page-001.png` | `1048da21e6be7253927877b0ea4841b898f209a2c48ef636b1d1f7d02c4fadf5` |
| `companion-page-012.png` | `c32a420d35c06c87b11b2ede61956513a9d18220740f388adbb0166f3f15a133` |
| `companion-page-025.png` | `de12bdb9d094874df4a99591d7acaa4a4e371014d00cb43fa5d364f9e26637e7` |
| `companion-page-037.png` | `43aa2506c09fc65b376a94c541adfb18663a83ee7edb715ab9edccb119908ea7` |
