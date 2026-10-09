# Build and verification protocol

1. Publish ordinary native TeX, scripts, audit Markdown and a source manifest. Any publication transport is an immutable bootstrap only; the build consumes ordinary files and does not reconstruct or rewrite mathematical source.
2. Bind the full native source directory tree and ordinary source commit. Preserve every non-R18 inherited path and all four canonical control blobs.
3. Run source input/label/reference/citation/manifest checks and the native finite regression in ordinary and optimized Python modes. Assertions are not the test oracle. Preserve old regression results without summing nested counts into fictitious independent tests.
4. Build the native article twice in isolated directories, three TeX passes each. Require no undefined references/citations or overfull boxes, and within-environment byte agreement under deterministic PDF metadata.
5. Run the unchanged R15 complete build, which includes R15 and complete U/T/S plus its preserved regression chain. The R18 full delivery therefore has sixteen isolated PDF builds when the R15 fourteen-build chain succeeds. Its outputs are not a fresh mathematical certification of all old theorems.
6. Publish generated PDFs/logs and hosted build receipts in a distinct child commit. A failed run must not be described as successful. The artifact commit is not the mathematical source commit.
7. Download the actual remote source-bound artifact packet and rebuild it in a separate environment. Hash the input tree before and after; do not intentionally regenerate source. Compare source/regression results and each PDF's page count and normalized extracted text. Byte differences across TeX versions are reported rather than hidden. Pixel equality, when claimed, is measured with a specified renderer and scale; it is not inferred from text equality.
8. Render all final pages and inspect the layouts, with enlarged review of proof equations and crowded pages. Record actual checks and limitations.
9. Add only final read-only evidence and referee entry files in a final evidence commit. Create revision/referee-ready refs at that exact head, non-forced, then read back all three new refs and unchanged canonical/review anchors.

Tests and CI validate deliverable integrity, selected finite identities and reproducibility. They do not prove continuum theorems, validate mathematical novelty or predict a journal decision. Any unavailable or failed acceptance step must remain visible in the final receipt.
