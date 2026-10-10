# Rebuild protocol

1. Source-only manifest covers every ordinary native file except itself; excludes artifacts/evidence/cache. It records SHA-256 and Git blob SHA, and verify.py reconstructs the native Git tree.
2. Native normal and python -O regressions must have identical output. Uses explicit checks, not assert.
3. Two clean native directories each receive three no-shell-escape pdflatex passes. Actual recorder TeX inputs must equal the source manifest. Undefined citations/references, multiply defined labels and overfull boxes fail the build.
4. Complete R26 and its recursively retained packet are rebuilt against pinned source trees. The source projection must not mutate. Nested check counts are not summed as independent tests.
5. Ordinary source is non-force pushed before build. Artifact PDFs/receipts form a direct child commit. Terminal independent/re-read evidence forms a later evidence-only child.
6. Independent reconstruction starts from the downloaded remote artifact packet, compares input hashes before/after, repeats ordinary/optimized and full builds, and reports PDF byte equality only where actually achieved. Cross-engine normalized text, page count and render comparison are separate claims.
7. All final pages are rendered; visual review of the new native pages and hash/render identity of retained outputs are recorded honestly. Failure attempts are preserved in receipts rather than described as never having occurred.

Dependencies: Python 3, pdflatex with amsart/lmodern/microtype/geometry/hyperref, poppler tools, pypdf and numpy for the inherited pipeline. Tests and builds are not proofs of continuum theorems or mathematical priority.

## Actual local preflight attempts

The first native preflight was rejected for an overfull first-page box and one long scope compound. The abstract was shortened without deleting mathematical statements, and the compound was rewritten as ordinary spaced prose. The next full native preflight passed (31 pages, no overfull boxes, no unresolved citations or references). This local preflight was uncommitted and is not a remote build receipt. All 31 resulting pages were rendered and visually inspected before source publication. The remote source and the independently downloaded source will be built again; only their actual results count as delivery verification.
