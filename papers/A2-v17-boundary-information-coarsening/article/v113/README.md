# A2 revision 113 — residual geometry of multiplication failure schemes

Principal manuscript: `paper.tex`; compiled manuscript: `paper.pdf` when the source-bound build succeeds.

This is an actual mathematical revision, not a report-only branch. It starts from the second independent v112 review, commit `66220b85960a5a50db15342ccfacfbf1395bca88`, dated 2026-09-22. The reviewed mathematical source was `0c696736e6ec22259c730672f61ebd8ef0d95460`, and the reviewed revision head was `e8eb87d4b22e341295175e2c3223fd21c68f41df`.

Revision branch: `revision/a2-v113-residual-conormal-wall-crossings-2026-09-22`.

## Reading order

The abstract and `parts/01b-structural-overview.tex` identify the new structure. The central arguments are in `02c-residual-calculus.tex`, `02d-all-dimension-components.tex`, `02e-wall-geometry.tex`, and `02f-higher-products.tex`. The earlier full-range codimension proof, contact/native derivations, native realization theorem, stable component theorem, statistics and complements are all retained. The stable component proof and statistical protocols are now in the appendices.

`RESPONSE_TO_R112_R2.md` maps the referee's objections to theorem labels and states the remaining scope boundaries. `PRESERVATION_AND_DEPENDENCIES.md` separates inherited arguments from new ones. `LITERATURE_AUDIT.md` distinguishes primary-text checks from bibliographic-only confirmation. `AI_ASSISTANCE_AND_PROVENANCE.md` records assistance and the need for human author approval before journal submission.

## Reproduction

From this directory run:

```sh
python3 verify_revision.py --source-only
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error paper.tex
python3 verify_revision.py --with-pdf
```

The verifier checks baseline ancestry, additions-only changes relative to the controlling review, exact preservation of six inherited source files, inherited label and bibliography-key retention, finite rank-equality diagnostics, exceptional corank-one examples, phase orbit counts, finite rank-two fibre algebra, and a finite-field residual-wall Jacobian. These diagnostics are not substitutes for the proofs.

The branch-scoped workflow builds and records a source-bound receipt, and commits only the resulting PDF and evidence on this revision branch. A receipt's `source_commit` identifies the mathematical input; an evidence-only commit is not a different mathematical source. Independent mathematical review remains required. No merge or publication approval is implied.
