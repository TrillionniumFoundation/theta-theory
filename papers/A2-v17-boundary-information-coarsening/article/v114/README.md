# A2 revision 114 — global residual singularities

Principal manuscript: [paper.tex](paper.tex). Compiled manuscript: [paper.pdf](paper.pdf), produced by the branch-scoped source-bound build.

Branch: `revision/a2-v114-global-residual-singularities-2026-09-22`.
Controlling review/base: `63daaeee1da5a1ee3ac569584e06f55081073da0`, the independent v113 report of 2026-09-22. The base contains reviewed mathematical source `c604b9d444db281ea8d662cd15e9bc7822ad55df` and evidence commit `f352be19dd524a6c5ff640289cd00b4bf87049e1`.

## Reading order

The article starts with the multiplication scheme. Section 2 proves the general polar residual tangent theorem, the global expected-codimension singularity theorem, all corank-one residual cotangent-Fitting identities, and the excess local criterion. Sections 5 and 7 supply the formal orientation descent and the relative divisor/normal-derivative/nonemptiness package. Section 8 gives algebraic phase descent; Section 9 contains the prior-result comparison. Section 10 is the short information-recovery application. All longer contact/native/statistical arguments remain in the appendices.

[RESPONSE_TO_R113.md](RESPONSE_TO_R113.md) is the point-by-point response. [PRESERVATION_AND_DEPENDENCIES.md](PRESERVATION_AND_DEPENDENCIES.md) records preserved sources and proof dependencies. [LITERATURE_AUDIT.md](LITERATURE_AUDIT.md) identifies exactly which primary texts were checked. The Ballico 1993 theorem-level comparison is not marked complete.

## Reproduction

From this directory in a checkout of this branch:

```sh
python3 verify_revision.py --source-only
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error paper.tex
python3 verify_revision.py --with-pdf
```

Requirements: Python 3, SymPy, latexmk, a TeX installation with the packages used in `paper.tex`, and `pdfinfo`. The verifier checks additions-only changes relative to the controlling review, all old labels and bibliography keys, six byte-exact inherited parts, inherited finite diagnostics, new exact modular polar calculations, small polynomial fibre calculations, references, and the PDF log. Finite calculations are consistency checks, not universal proofs.

The source-bound receipts in `evidence/` identify the **mathematical source commit**. The PDF/evidence-only commit comes afterwards and is not a different mathematical source. The workflow refuses to push over a branch that has advanced concurrently and never force-pushes.

## Source materialization provenance

The connector transport uses a checksummed, compressed source pack under `.sourcepack/` and a one-shot `materialize_revision.py`. The branch-scoped workflow expands it into the actual readable `.tex`, `.md` and `.py` files, commits those sources, and only then verifies and compiles them. The pack is bootstrap provenance, not a substitute for the expanded manuscript. `SOURCE_MATERIALIZATION.json` records the bootstrap commit, frozen baseline and file hashes. Once the marker exists, the materializer does not overwrite later source revisions. A workflow run can therefore have a bootstrap `head_sha` while its receipts correctly identify a subsequent materialized mathematical-source commit in the same run.

This branch is for independent mathematical review. No merge, journal submission, human author approval or referee endorsement is implied.
