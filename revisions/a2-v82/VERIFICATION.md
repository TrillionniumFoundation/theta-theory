# A2 v82 verification record

## Exact source

Mathematical commit: `80133d376cc28cc8f2555f58324a3285f9dcfb67`.
Principal source blob: `f8b2126e6faa582ad64e4c9f80d87a8c12d29ac1`.
The remote blob returned by GitHub matches the locally computed Git blob SHA.
The core PDF was built from these same TeX bytes and the unchanged inherited preamble.

## Checks actually executed locally

`python scripts/check_a2_v82.py`: **15 tests passed**. The transcript is `algebra-tests.txt`.

`python scripts/audit_a2_v82.py --core-only`: **passed for the core only**. The active core paths and both SHA-256 and Git blob hashes are recorded in `core-source-graph.json`.

`latexmk -pdf -interaction=nonstopmode -halt-on-error rigidity_v82_core.tex`: **passed**, producing a **10-page** core reading edition. The final log has no undefined references, undefined citations, LaTeX errors or overfull boxes. It reports one underfull bibliography paragraph. All ten pages were rendered with Poppler and inspected for layout; no clipping or overlapping equations was observed.

Local PDF SHA-256:

```text
ce2eae0f787aaf249f617c2150d96a1c8bf5fdae9ae2eadbb3c63201f50b77dc
```

The PDF is supplied in the delivery session. It is not represented as a checked-in binary or as an Actions artifact. The repository contains its complete reproducible core sources.

## Full manuscript and remote execution

The complete integrated entry is `rigidity_v82.tex`, not the core entry. Its inherited companion sources were not all materialized in the local build environment. **A full integrated native build was not executed locally and is not claimed successful.** The complete entry retains the 23 substantive top-level inputs of the inherited v81 entry, including its bibliography through the wrapper; source-graph and retention checks run on the full checkout in the native workflow.

The committed `scripts/build_a2_v82.sh` runs the algebra checks, checks the entire input graph, compiles both entries, rejects unresolved references/citations, and records source commit plus PDF hashes. The workflow has read-only repository permissions. A configured, queued or failed workflow is not a successful build. Its actual run status must be read from GitHub for the exact delivery head.

## Scope of the tests

The tests check observable component reconstruction, scalar example inversion, common detector gauges, projective rescaling, equal-action cancellation, a single-operator spectral collision resolved jointly, the exact Jacobian determinant, the four-pole numerator and root sum, a three-clock action-changing family, finite-degree local Jacobians, unrestricted interpolation compensation, exact shear/roof identities, independent physical channels and survival margins, simultaneous deadlines and rank thresholding.

The example optimizer uses bounded deterministic multistart; convergence in those examples is not the global uniqueness proof. The tests do not formally verify the manuscript, certify all inherited proofs or establish a journal's editorial standard.

## Authorship and review

This revision was prepared with AI assistance at the repository user's request. The existing author name is preserved as manuscript metadata. Human author approval, journal submission and independent referee endorsement are not presumed. No review branch, default branch or historical manuscript is overwritten.
