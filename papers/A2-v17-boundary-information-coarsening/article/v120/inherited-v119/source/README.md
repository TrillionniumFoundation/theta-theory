# A2 revision 119

## Codimension bounds and primary structures in multiplication failure

Author: **Qian Qi**. Date: September 22, 2026.

**Origin of this delivery: generated locally; this authoring session did not push to GitHub.**
A later authorized application and push are separate actions.

Intended new branch: `revision/a2-v119-codimension-primary-conductor-2026-09-22`.
Controlling R118 review commit: `d4254d9b01405ad02c64d2ff591503d4cc7a6aa7`.
Reviewed mathematical source: `c87bfdad8d97e68637d269e656b46c4cce85551e`.
Reviewed v118 product: `44bfc648ead008896a6981a7302a6d5ab8b21bb8`.

## Reading editions

- [Primary geometry article](geometry.pdf), with [self-contained LaTeX source](geometry.tex).
- [Complete manuscript](paper.pdf), retaining all complementary geometry and statistical appendices.
- [Separate application appendices](applications.pdf).
- [Point-by-point response to R118](RESPONSE_TO_R118.md).
- [Literature audit and explicitly open comparison](LITERATURE_AUDIT.md).

## New mathematical content

`parts/01c-codimension-stabilization.tex` proves the universal codimension bound over the coefficient ring.
`parts/02k-full-codimension-two.tex` gives the entire degree-three Fitting scheme, the exact corank-one incidence and the conductor-stratum fibres of its proper extension.
`parts/03b-embedded-multigenerator.tex` proves a connected arbitrary-order embedded primary family and a supplementary three-generator case.
`parts/01d-general-conductor.tex` proves the regularity-controlled global transport for arbitrary finite projective schemes and finite flat families, and applies it to the new primary geometry.

The quotient-flag statement, relative cyclic-vector argument, Schubert divisor identification, moving-fat-point bundle and low-degree interpretation are also made explicit. The original determinant-power theorem, sharp curve and fat-point bounds, contact classifications and all complementary developments remain present.

## Reproduction

Run `bash build.sh` in this directory. It requires Python 3, SymPy, PyMuPDF and a LaTeX distribution providing the packages named in the sources. The build uses no network access and does not regenerate the edited TeX files from an authoring script.

`evidence/PRESERVATION.json` contains the pinned old-source hashes and all 293 inherited labels. `make_preservation.py` can regenerate it when the pinned v118 sibling is available; the retained manifest makes an isolated v119 build portable. The old authoring scripts and evidence are clearly separated under `inherited-v118/` and are not new build receipts.

`evidence/DIAGNOSTICS.json` records exact finite regression tests, not mathematical proof certification. `evidence/BUILD_RECEIPT.json` and `evidence/SOURCE_MANIFEST.json` describe only the actual local build and its content hashes. They do not claim a remote publication, an independent proof audit, priority certification, or journal acceptance.

## Outstanding scholarly item

E118.1 remains open: complete theorem text of Ballico (1993), DOI `10.1002/mana.19931630102`, was not obtained. The manuscript does not infer non-anticipation from this access failure. All other item dispositions and the exact scope of the new results are recorded in the response.

## Repository application

The top-level delivery package supplies an application script and a Git patch. The script starts from the pinned R118 review commit, creates only the named new revision branch and adds the v119 directory plus its new root index. It requires a clean checkout and refuses to overwrite an existing branch or revision directory. Its optional `--push` flag uses the user's own configured GitHub credentials. No existing branch is merged, force-pushed or rewritten by this package.
