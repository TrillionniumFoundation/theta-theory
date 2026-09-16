# Revision 65 validation protocol and first execution

The delivered script `tools/check_revision_v65.py` uses explicit exceptions, not optimization-sensitive assertions. Its normal and `python -O` executions produced identical JSON in the local preflight environment. The output is a finite diagnostic, not a rigorous enclosure or a proof of any infinite-dimensional statement.

New controls actually executed:

| Control | Count / result |
|---|---|
| Exact rational cyclic blocks, physical cycle lengths 2 through 7, degrees 2 through 9 | 144; direct visit sums, determinant, inverse and row-norm bounds agree |
| Odd-degree orientation negative controls | 48; replacing signed factors by absolute values changes the response |
| Incorrect endpoint multiplicity controls | 144; initial visit cannot be counted twice |
| Curvature Jacobian entries, independently differenced action Hessians of 120-flight Jacobi chains | 180; maximum local difference `2.5008e-10` |
| Curvature blocks versus direct boundary-visit sums | maximum local difference `2.2204e-16` |
| Actual nonlinear Euclidean chord envelope, equilateral and scalene projection-chart graphs, quadratic and cubic shape variations | 72; maximum local difference `3.9661e-12`, 60 flights |
| Actual scaled chord Hessian and stationary equations | maximum local residuals `8.8818e-16` and `4.4409e-16` |
| Exact rational two-offset extraction with independently integrated normalizers | 50 points, 40 amplitude-axis identities, 40 oblique-gauge negative controls |

The retained v64 mathematical functions are rerun unchanged: 360 exact transfer/cofactor cases and the actual equilateral/scalene geometric, relative-factorization and physical-gauge controls. The old v64 preservation routine is not reused against a different revision; the new routine verifies the full frozen v64 baseline and its exact archives.

The first local native preflight compiled all three entries from a clean local Git source with fresh auxiliaries and shell escape disabled: principal 143 pages, full 319 pages and companion seven pages. It detected a 1.454-point title-page vertical overflow in the principal article. A four-point increase to the existing title-page allowance was then made; final remote logs, not this preliminary result, determine the final warning status. No content was shortened to resolve that layout issue. Preliminary mathematical pages were visually inspected; final source-matched product inspection is recorded separately after native publication.

The local preflight commit is not a remote revision identity. The native workflow freezes and records the actual committed remote source, reruns normal/optimized diagnostics, rebuilds the three complete entries and publishes the exact-source artifact and Git-retained products on a new revision branch. A source-matched PDF is a build result, not a mathematical or editorial certificate.
