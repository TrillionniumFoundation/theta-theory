# A2 v44 — execution ledger at the source checkpoint

This source-checkpoint ledger records work actually executed before publication. It does not claim that a configured workflow has completed. A later delivery ledger must name the exact compiled source, actual run, published products and fetched-object verification.

## Local checks actually executed

The complete v43 source was obtained through authenticated Actions artifact `10335751435` from run `34813913830`; the native products were obtained through artifact `10336196390`. Direct local GitHub cloning was not used as evidence. The active baseline manifest contains 95 main/companion entries. The new source preserves them as specified in `PRESERVATION_AND_DEPENDENCIES_V44.md`.

`check_revision_v44.py` and `check_realization_v44.py` passed under both ordinary and optimized Python with byte-identical JSON. There are no unresolved static references or citations and no duplicate labels. The geometric check covers 108 parameter cases and 436 contact solves. The maximum contact residual is approximately `3.09e-15`, maximum recovered Gram error `1.01e-11`, and maximum redundant-cycle error `1.59e-12` in this finite test. None is an all-order proof certificate.

`check_retention_v44.py`, using the actual replacement retention helper and downloaded v43 native artifact, reproduced all 13 ignored-file omissions under ordinary staging, verified all 37 artifact files after force-staging, and verified committed objects even after deleting the working-tree main PDF. Normal and optimized outputs agree. This is a temporary local-repository diagnostic, not yet a statement about a newly published remote delivery.

## Complete local native build

Both native entries were compiled in a separate complete-source directory, with companion first:

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' two_collision.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' main.tex
```

Both returned zero. The main has 228 pages, the companion seven. The final main log has no unresolved references, undefined citations, missing-character messages or overfull boxes. It contains four underfull vertical-box notices and the shell-escape-disabled epstopdf warning. This local source directory is not represented as an authenticated Git checkout or a source-SHA build. The hosted build procedure separately freezes actual committed Git objects and records all native inputs.

All 228 main pages have been rendered to overview sheets. Rendering is not the same as visual inspection. The initial readable-resolution examination covers the newly added geometric proof pages; the final delivery ledger will give the precise inspected page list. No all-page visual or mathematical certificate is issued.

## Publication procedure awaiting recorded execution at this checkpoint

`.github/workflows/a2-v44-native-submission.yml` is configured to compile the exact new author commit, retain full native products on a new products branch, repair the original v43 archive in a distinct subtree, fetch published commits and verify every advertised Git blob. `REPOSITORY_RETENTION.json` is explicitly only a verified artifact-copy receipt; `COMMITTED_OBJECTS_VERIFIED.json` is written only after verification of a resolved commit, never from an index check.

The v43 PDFs genuinely existed. Its historical error was omission of 13 promised files from the products commit. The original incorrect receipt remains unmodified. Durable retention and current navigation will be judged from actual fetched published objects and the updated delivery ledger, not inferred from this source checkpoint.
