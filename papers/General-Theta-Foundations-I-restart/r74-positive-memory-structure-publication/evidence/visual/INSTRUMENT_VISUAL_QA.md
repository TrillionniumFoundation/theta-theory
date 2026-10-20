# R74 instrument and contraction pages: visual QA

## Identity and scope

This is a read-only visual inspection by a separate author-team AI agent.
It is not an independent human referee report, proof certification, a new
diagnostic run, or an editorial assessment. No sealed source file was changed.

- PDF inspected: `General_Theta_Foundations_I_R74.pdf` in
  `/workspace/scratch/f856e3d63ac5/r74-build-verified/`.
- PDF SHA-256, independently computed before inspection:
  `e689bc09a30ddceb7bd45b127986797820003ce15543fe3f732a1181b5def76e`.
- Source commit declared and verified in the matching `BUILD_RECEIPT.json`:
  `29b999abf11c43709e64be58765aa1984d13ac91`.
- `pdfinfo` reports 39 pages. This inspection covers **printed/PDF pages
  20, 21, 22, 23, 24 and 25 only**.

The six pages were freshly rendered from that PDF with Poppler:

```text
pdftoppm -f 20 -l 25 -r 150 -png General_Theta_Foundations_I_R74.pdf instrument-review/page
```

Each resulting page image was opened separately at original image resolution
and visually inspected. Text extraction or the successful LaTeX build was
not substituted for viewing the rendered pages.

## Actual pages inspected

| Page | Material visually checked | Finding |
|---|---|---|
| 20 | Section 7 bridge to retained R68 instrument theory; posterior inequality, dictionary bound, sparse-row statement and supplementary references; transition into Section 8 | No observed clipping, overlap, unresolved reference, missing glyph or isolated section heading. |
| 21 | Response and contraction assumptions; Theorem 8.1, live-label bound, explicit entry time, invariant-polytope construction and prefix-state count | Displayed sums, ceilings, subscripts and norm inequalities are legible and contained within the page. No observed layout defect. |
| 22 | Supremum-norm certificate; Section 9 heading; explicit Fanizza/FRDN priority paragraph; `sin(theta) != 0` condition; instrument matrices and complete Theorem 9.1 statement | Citation and boundary condition display correctly. The full theorem statement fits on the page; outcome intervals and the `q`, `q+1`, infinite alternatives are legible. |
| 23 | Choi bounds, stationarity, one-dependence, oscillatory word probability (9.2), rank-three argument, active-core path inequality and peripheral-cycle lower | Mathematical glyphs and equation numbers display correctly. No clipping, overlap or missing proof text was observed. |
| 24 | Polygon upper, stationary mixed initialization, counted initializer, pure-start rigidity contradiction, algebraic irrational-phase example and Holroyd--Liggett attribution | Fractions, matrices, cycle counts and proof-ending symbol render clearly. The proof continuation from page 23 is readable; no observed layout defect. |
| 25 | Completion of the conditional-memory scope paragraph and transition into retained algebraic synthesis | Continuation and section transition are clear, with normal page margins and no observed formatting defect. |

**Concerns found on the six inspected pages: none.** This statement has only
the visual and page-limited scope just described. It does not certify the
remaining pages, the supplement, mathematical novelty, or proof correctness.

## Rendered image identities

The inspected images are in `instrument-review/` beside this record.

| Image | SHA-256 |
|---|---|
| `page-20.png` | `0f467a421ecdae94db4a9ffd2ec13187fd08627df71ce35914ffe7cdae491a34` |
| `page-21.png` | `495274a52e1dde3e4e0388fe468821063aec2fa726bc575cd6bffb394d2e2068` |
| `page-22.png` | `6e9d99052b845be7a0c596816bc369528ff406fbdeac3c71dd1ed786eadfa18f` |
| `page-23.png` | `73ab7c5a3c96123e848c6d347a650074aef4e674868ed8fa428f61e144e59020` |
| `page-24.png` | `9ea9a3a7e362bac10d5298a01a524933129652e6f59da2b2bf63ee06d936e6fb` |
| `page-25.png` | `03c6ac0f0ee271b92373f2eb24eb2b2eaa77c140b379cc5c0119b14b1d50a1b1` |
