# A2 revision 115 — renewed independent review

**Controlling review:** R114 at `09869129e16fd43bd2420fa3573a09cd5cbbdff9`.  
**Reviewed mathematical source:** `d58d4ad0546487f4313cf8ed2f05ad9321b54e63`.  
**Intended new branch:** `revision/a2-v115-intrinsic-residual-germs-2026-09-22`.  
**Publication state:** local revision and applicable patch; **not pushed to GitHub**.

## Reading order

[Geometry article](geometry.pdf) is the journal-facing mathematical article. [Complete manuscript](paper.pdf) includes every retained appendix. [Information-recovery and statistical appendices](applications.pdf) is the companion reading copy, with the same appendix numbering as the complete manuscript. Both reading copies are compiled from the same section sources, not separately rewritten manuscripts.

Start with [the response to R114](RESPONSE_TO_R114.md). The main new global result is Theorem `thm:higher-hyperplane-global`: all higher-product hyperplanes, all failure coranks, saturation away from the evaluation curve, the complete associated-point set for degree at least three, and a growing nilpotency lower bound. The exact nonlinear residual-germ section precedes the retained binary quadratic classification.

The PDFs and build receipts are included in the generated-evidence commit of this package. The earlier source-only commit is intentionally not a PDF delivery. The authoritative final file list and source/PDF hashes are in [BUILD_RECEIPT.json](evidence/BUILD_RECEIPT.json), together with [SOURCE_RECEIPT.json](evidence/SOURCE_RECEIPT.json). A local commit identifier is not represented as an upstream commit identifier.

## Reproduce

With Python 3, SymPy, Git, pdfLaTeX, AMS packages, lmodern, microtype, mathtools, booktabs, xr-hyper, geometry, hyperref and Poppler installed, run:

```sh
bash build.sh
```

The build runs the preservation and finite algebra checks, compiles the full manuscript, derives the two nonduplicating external-reference files, then compiles both reading copies and writes receipts. It does not access the network or modify GitHub. For a check against an actual full repository containing the controlling review object, use `python3 verify_revision.py --source-only --git-baseline`.

The included `history/v114_source/` is a byte-exact archive of all 19 reviewed TeX files. Its hashes are independently tied to the retrieved v114 source artifact in `evidence/V114_SOURCE_MANIFEST.json`. This avoids the former nested-directory Git pathspec bug and makes standalone verification possible. A regression test also checks repository-root and nested-directory invocation against the same fixture, including trailing newlines.

## Scope and status

This is a mathematical revision for independent review, not an assertion of journal acceptance. The new higher-product theorem gives a full support/corank/associated-point classification in the natural hyperplane family. It does not classify the full embedded primary ideal, every higher-product contact configuration, or every smaller component of the general quadratic excess scheme. The Ballico 1993 theorem-level priority comparison remains incomplete because the relevant full text was not obtained. The classical determinantal inputs are explicitly identified in the article and literature audit rather than presented as new discoveries.

No old branch or old manuscript file is overwritten by the supplied patch. See [preservation and proof dependencies](PRESERVATION_AND_DEPENDENCIES.md) and [provenance](AI_ASSISTANCE_AND_PROVENANCE.md).
