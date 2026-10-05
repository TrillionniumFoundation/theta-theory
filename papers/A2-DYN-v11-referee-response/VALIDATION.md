# Revision 11 validation and verification limits

## Frozen source and current result

The reviewed mathematical source is revision 10 at `3e45e41b5be6ef636944f67dce529fdc9fd4fcc9`. The controlling report is the revision-10 report at `a42dc1401007f9f8025c916106884e09d7d864f0`, blob `e6732df7a22bc7e161ac4650e74e9fdce80d52b3`. The revision-10 source archive was extracted from its previously successful exact-source artifact. The current report was read directly through the GitHub connection.

The new revision is prepared locally, without an authenticated write-capable GitHub operation in this execution. No remote author commit or Actions result is invented. `PUBLICATION_STATUS.json` records the observed target response branch at the review baseline, which does not contain this revision's additions.

## Native build and preservation

`bash build.sh` completed. It runs the active v11 preservation and finite checks in normal and optimized Python modes, compares their outputs, runs the inherited geometric and clock diagnostics, and compiles the full article with native `pdflatex -no-shell-escape` until the auxiliary references stabilize.

The result is **75 pages, 29 unique core inclusions, 98 proof environments and 289 labels**. All **27** inherited mathematical core files and **14** inherited Python scripts are byte-identical. Every core file is included once. The active source test checks citation/reference resolution, duplicate labels and balanced formal environments. The final native log has no unresolved references, LaTeX/package warnings, overfull boxes or underfull boxes.

`evidence/build-receipt.json` records the actual source and PDF hashes. Because this is an extracted local working archive rather than an authenticated repository commit, local Git and event identifiers are null. A future CI run enforces a clean scoped source and equality of the checked-out commit with its event SHA; this local build is not represented as that run.

## Finite tests

The new exact finite-cycle checks cover **26,880** marked-return compensation identities, including initial marks, terminal marks, varying return gaps and backward intervals. The operator checks cover **243** finite chronological pairings with complex marks. **165** negative controls distinguish the incorrect insertion time, so the test is not merely verifying an unweighted equality.

All norm-growth and frequency error margins are checked in rational arithmetic. The slow supremum margin is `3/280`; the isolated variation margin is `9/175`. The remaining polynomial margins, analytic-radius conditions and logarithmic complementary cutoff are checked separately. The earlier compensation, return-count, interpolation and exponent diagnostics remain included. The ordinary and optimized Python outputs are byte-identical.

These are algebraic and source tests. Finite cyclic systems are not used as billiard models establishing the collision spectral input or the continuum theorem.

## Layout inspection

The PDF was rendered with MuPDF and with Poppler (`pdftoppm`). Selected pages were inspected at the introductory theorems, marked-return identities and spectral proof, the main marked estimate and its exponent table, the same-event conditional corollary, the source-map appendix and the bibliography. Appendix C was moved to a page boundary so that its heading and norm table remain together. No clipping or equation-number collision was observed on the inspected pages. This is a selected-page inspection, not a claim that a human specialist reviewed the entire article.

## Prepared remote qualification

The added workflow `.github/workflows/a2-dyn-v11-qualification.yml` is scoped to the two intended revision branches and the new paper paths. It uses read-only repository permissions, an exact event checkout, native TeX, the same diagnostics and source-bound artifact upload. Its YAML and read-only permission settings have been checked locally. The workflow has **not** executed for this revision.

The accompanying publication patch is add-only and the shell script uses the frozen review parent, checks both target refs for divergent work, builds before committing and makes a non-forcing atomic push. Local patch application and shell syntax checks are recorded in the package-level `PATCH_VALIDATION.json`; no network success is inferred from those checks.

## Mathematical verification boundary

The new marked central theorem is proved in the manuscript from its existing collision input. Neither compilation nor the finite checks certify that input independently. Uniform positive definiteness, periodic-evaluable rigidity, the entire complementary-frequency integral, the global critical/singular coarea residual sum and exact-record weighted local limits have not been proved here. No independent human specialist endorsement or journal acceptance is claimed.
