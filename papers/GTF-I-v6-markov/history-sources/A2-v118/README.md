# A2 revision 118 — Conductor strata and nonreduced multiplication failure schemes

**Author:** Qian Qi  
**Revision branch:** `revision/a2-v118-higher-defect-nonreduced-generators-2026-09-22`  
**Controlling review:** `review/a2-v117-independent-harsh-top4-2026-09-22`, frozen at `2c6f180fa0baf23386e0a46a64abe7503ea65b00`.  
**Reviewed v117 product:** `fb999b3a43fe4331becb42646bc2faeadfa5492a`.

## Reading editions

- **Primary article:** [geometry.pdf](geometry.pdf), with [LaTeX source](geometry.tex).
- **Complete manuscript:** [paper.pdf](paper.pdf), retaining every previous complementary proof and statistical appendix.
- **Separate application appendices:** [applications.pdf](applications.pdf).
- **Response to the controlling report:** [RESPONSE_TO_R117.md](RESPONSE_TO_R117.md).
- **Literature/priority audit:** [LITERATURE_AUDIT.md](LITERATURE_AUDIT.md).

The new mathematics is in `parts/02a-higher-defect.tex` and `parts/03a-nonreduced-generators.tex`. The first gives the stable generated algebra, conductor exact-rank flags, the extreme-corank Fitting scheme, and the two codimension-two quotient mechanisms. The second gives the full primary law for truncated local algebras and transports it to section multiplication on projective spaces of arbitrary dimension. The inherited hyperplane, contact, pencil, and reduced three-plane results remain in the main article; unrelated complements remain in the complete edition.

## Reproduction and provenance

Run `bash build.sh` from this directory. The published source tree is self-contained. An initial, unexpanded authoring checkout additionally needs the reviewed `v117` sibling. Requirements: Python 3 with SymPy and a LaTeX distribution providing the packages named in the sources. No network access is needed by the build itself. For initial materialization, `prepare_revision.py` writes only `v118`; it copies reviewed sources, makes explicit targeted revisions, and retains every inherited theorem label. The build does not regenerate an already materialized manuscript, so subsequent direct LaTeX edits are respected. Explicitly rerunning the preparation script regenerates its targeted files. `evidence/PRESERVATION.json` gives hashes and the list of unchanged active sources.

On the initial run, the branch workflow materializes the complete source graph and commits the **actual LaTeX sources**, then builds and commits the PDFs and receipts. The mathematical-source commit is recorded in `evidence/SOURCE_RECEIPT.json` and `evidence/BUILD_RECEIPT.json`. The later product commit adds PDFs; it is not confused with the source commit. The reviewable manuscript is the complete `.tex` tree and the PDFs beside it.

`verify_revision.py` contains exact finite regression checks of substitution determinants, the nonreduced action-rank jump, and the global triangular conductor construction. The complete proofs are in the article, not inferred from these tests. A successful build is neither proof certification nor a novelty or journal-acceptance certificate.

## Remaining source-access item

**E117.1 remains open:** the complete theorem pages of Ballico (1993), DOI `10.1002/mana.19931630102`, were not obtained. The manuscript and response do not infer disjointness or originality from this access failure. The broadened comparison with maximal-subalgebra, subalgebra-variety, polynomial-subalgebra, and generator-scheme results is recorded separately; it does not erase this open item.
