# R79 retained supplement and companion: actual raster visual QA

Status: **PASS for the explicitly scoped visual inspection; no blocking layout defect observed.**

This is an author-side AI-assisted visual check of actual rendered pages, not an independent human referee assessment, a mathematical proof audit, or a guarantee that every character on every page has been checked. No source or PDF was changed during this inspection.

## Fixed source and artifact identities

- Source commit: `90cae2f5aca243b39d3a2194a4d6e0696671a101`.
- The strict local `BUILD_RECEIPT.json` was read and reports `PASS`, `source_commit_verified: true`, and the same declared source commit. This is separate evidence from the visual check.
- Supplement: `General_Theta_Foundations_I_R79_Supplement.pdf`, 190 pages, SHA-256 `83b54ebd0b28364709e4bed160b5972efbb6361c425ac8b04f2b238b5c4f01ce`.
- Retained companion: `General_Theta_Foundations_I_R79_Retained_Companion_R58.pdf`, 37 pages, SHA-256 `5bdbe05bcb4955fc4dca36265457675fb94ef86c0ae5c54fd711548f5758c3a3`.
- The two actual strict-build PDFs were independently hashed for this record and matched the render receipt and the identities above. All 20 inspected PNGs were hashed and matched their entries in `RENDER_RECEIPT.json`.

## Images actually opened and inspected

The following files were opened with the image-viewing tool; conclusions were not inferred from successful rendering, LaTeX logs or text extraction alone.

| Document | Contact sheets actually viewed | Page coverage at thumbnail scale | Full-page raster images actually viewed |
|---|---|---|---|
| Supplement | `supplement-contact-01.png` through `supplement-contact-08.png` | 1–24, 25–48, 49–72, 73–96, 97–120, 121–144, 145–168, 169–190 | 1, 89, 124, 138, 170, 190 |
| Retained companion | `companion-contact-01.png`, `companion-contact-02.png` | 1–24 and 25–37 | 1, 12, 25, 37 |

The contact sheets therefore cover all 227 retained-document pages for gross layout inspection. Ten selected full-page rasters provide readable checks of opening material, dense proofs, displayed equations, theorem transitions, and the final bibliographies. The manuscript itself was assigned to separate visual checks and is not covered by this record.

## Specific findings

### Supplement

The eight contact sheets show continuous page sequencing, consistent single-column text blocks and alternating running heads, with no unexpected blank page, gross right/bottom-edge clipping or overprinted text block visible at the displayed scale. The bibliography begins near the end and the final reference page has ordinary remaining white space rather than a missing-content indication. The figure on page 158 is visible in its contact-sheet panel; it was not separately inspected at detail scale.

- **Page 1:** The two-line supplement title, author, abstract, scope paragraph, first section heading and first displayed equation are clear and separated. The title and abstract do not collide with body text. The date footnote and page number remain inside the page area. The abstract identifies the general nonreset result as belonging to the main article and the inherited technical material as the supplement's role.
- **Page 89:** Theorem S25.1 and its proof show readable inline and display mathematics, visible proof-end symbol, and a separated S25.2 heading. The long fallback/resolvent displays remain within the column. Equation S25.1 near the bottom has its number separated from the formula.
- **Page 124:** The backward-cost proof, S31.3 heading, three numbered display groups and Theorem S31.3 are legible. Display fractions and superscripts remain distinct. The page ends during a theorem passage with normal continuation, not visible cropping. The equation numbers remain in their separate right margin.
- **Page 138:** Lemma S35.1, its proof and Theorem S35.2 are clearly differentiated. The block projection identities, supported potential inequalities and resolvent formulas have sufficient spacing and remain inside the text block. The dense numbered equations S35.5–S35.11 do not visibly overlap one another or the prose.
- **Page 170:** The scope paragraph, S45 section title, construction displays and Theorem S45.1 are separated. The wide paired certificate formulas fit; the proof continues at the bottom with normal page flow. No lost mathematical glyph or collision was observed at detail scale.
- **Page 190:** References [80]–[94], including the new fixed-controller, quantum verification and hidden-model sources, are readable. Long titles and DOI strings wrap within the text block with visible continuation indentation. Reference numbers align and no final entry is cut off. This is a visual formatting observation, not a new bibliographic verification of every cited item.

### Retained companion

The two contact sheets show consistent running heads, text margins and page numbering through page 37. The last sheet's unfilled cells are contact-sheet layout space, not blank pages in the PDF. No unexpected blank page, gross clipping, overlapping text or apparent missing page was observed.

- **Page 1:** The long two-line title fits, followed by the author, a dense but readable abstract and a clearly separated introduction. The classification/keywords footnote stays below the body with its rule and page number clear. The independent companion identity is preserved.
- **Page 12:** Equation (7.1), the end of its proof, Proposition 7.2 and the subsequent proof remain legible and correctly separated. Displayed errors and norm notation fit the text column. The final proof continues to the next page without visible truncation of the final line.
- **Page 25:** Corollary 14.4, its trace-norm display and proof-end symbol are clear. The transition to Section 15 is separated and the Gaussian-sensing equations (15.1)–(15.3) fit with their numbers. No observed collision occurs at the section transition or among the multi-part formulas.
- **Page 37:** The final References heading and all 17 entries are legible and aligned. Wrapped titles/DOIs stay within the page. The white space after the last entry is an ordinary short final bibliography page.

## Limits and disposition

No source change is indicated by these observations. The check uses full-document thumbnails and the ten enumerated readable representative pages; it does not inspect every glyph of all 227 pages at full scale. It does not test clickable cross-document links, accessibility tags, text extraction, all reference targets, color-managed printing or a different PDF renderer. It does not certify mathematical correctness, novelty, priority, outside expert approval, hosted CI or editorial acceptance. The strict native build, finite diagnostics, preservation checks and source authentication have their own receipts and retain their stated scopes.

## Exact viewed-image identities

| Image | SHA-256 |
|---|---|
| `supplement-contact-01.png` | `b9a88529621971c7377e2e916e75a3127a73b6bb9becaf8f5b2575a85f1c12ab` |
| `supplement-contact-02.png` | `6dfb981047005c11d1427ea36f393e3d32e1f78e224513657dec74b26b9cbcbc` |
| `supplement-contact-03.png` | `a9cbb34bcaa6789fc2c55c88ad75360117f77cfc6dff8458e96ba0996fdab2ab` |
| `supplement-contact-04.png` | `3b887f307dbfb2f87d95fbe2b1bc8bd1d3e382bf84fcb4d0e6df558a202226f4` |
| `supplement-contact-05.png` | `f2a6b83eff7a3594816ed859c29ec7c7bee4c46cc2b2e845981204a76cd437ea` |
| `supplement-contact-06.png` | `54047eae160ba2927b385957d80d38c41e26f8b0a177afdc40de869d3b0dad1e` |
| `supplement-contact-07.png` | `18e88a1d8688d0f63e719ba7a5ca00180a3164ba60cfc2eea8a963ab067b18f7` |
| `supplement-contact-08.png` | `533b214a9c49c2add1231e6ffc474b5aa25b0eb7b68a7bee345a197ee6e8487c` |
| `companion-contact-01.png` | `24ed72af1f27a2c30db8ee0df42a1a4976fb2e7a2079d1c3377a8e0b897b2cbc` |
| `companion-contact-02.png` | `9de27034faf215d9e5cfb45d8f4e85f1d0ea21ae695b0a439a8ab786eea9f7bc` |
| `supplement-page-001.png` | `465d782dfce34ff9b5ea0de3342c4e018d618631e87efe5f33598e5b22643260` |
| `supplement-page-089.png` | `2bd6c226d71ebb4f6dcb67c3941a443aecf841d784149c3449f4ecd8ce0054e3` |
| `supplement-page-124.png` | `a86194fb9c3901bad5015fddd55b8942cde55ba10e9cc509b4a35b233237f7be` |
| `supplement-page-138.png` | `519bc865317019a0bc711f63b63f93e480f15ee9f1d149ba9ee5d47582701efe` |
| `supplement-page-170.png` | `3a45880044d6f26c5d1658ca952adac1b041e6286cba87e1d698ff1379e88ee4` |
| `supplement-page-190.png` | `9ae1f3aa31538bcc5bf6870fc8e372bdb052d2a8c0b3f6dace9ea9ad922444bf` |
| `companion-page-001.png` | `1048da21e6be7253927877b0ea4841b898f209a2c48ef636b1d1f7d02c4fadf5` |
| `companion-page-012.png` | `c32a420d35c06c87b11b2ede61956513a9d18220740f388adbb0166f3f15a133` |
| `companion-page-025.png` | `de12bdb9d094874df4a99591d7acaa4a4e371014d00cb43fa5d364f9e26637e7` |
| `companion-page-037.png` | `43aa2506c09fc65b376a94c541adfb18663a83ee7edb715ab9edccb119908ea7` |

Completed UTC: `2026-10-23T07:41:00.702856+00:00`.
