# A2 v7 delivery and verification status

Recorded September 9, 2026.

## Materialized source revision

The complete integrated manuscript source, all inherited mathematical body files and historical sources, the unchanged complete two-collision companion, the point-by-point response, proof ledger, source pins, and reproducibility scripts are committed on:

`revision/a2-v7-sharp-physical-experiments-2026-09-09`

The mathematical source commit is `781b91da1b7af41c7c1528ccb44cd0681d564e0d`. The subsequent delivery-record commit does not alter the mathematical source. [Draft PR #49](https://github.com/TrillionniumFoundation/theta-theory/pull/49) provides the independent referee handoff. Its base is the source-pinned latest review branch, not `main`.

Read [main.tex](main.tex), [RESPONSE_TO_REFEREE_V7.md](RESPONSE_TO_REFEREE_V7.md), and [PROOF_LEDGER_V7.md](PROOF_LEDGER_V7.md). The first revision commit adds a complete new paper directory; it does not delete or change any file present at the review baseline. The old main file, preamble, and README are also archived exactly within the new directory. All previously active mathematical body inputs remain in the new main source.

## Actually executed local checks

The standard-library finite suite was executed in normal Python and with `python -O`, then executed again after source submission. All 136 checks passed and the two JSON outputs were byte-identical. The locally executed `checks.py` bytes have the same Git blob SHA as the file retrieved from the committed revision. Both Python scripts passed syntax compilation. Exact hashes and the diagnostic categories are recorded in [verification-v7/LOCAL_DIAGNOSTICS_V7.json](verification-v7/LOCAL_DIAGNOSTICS_V7.json).

These are finite diagnostics, not an independent certification of the nonlinear theorems. The build script's preservation and full-TeX checks are implemented but were not run to completion; they must not be reported as already passing merely because the script exists.

## PDF build did not execute

GitHub Actions run `34342662140`, job `102436836901`, ended with failure before any runner was assigned: `runner_id=0`, an empty runner name, and no job steps. The available response does not establish its underlying cause. See [verification-v7/BUILD_ATTEMPT_V7.json](verification-v7/BUILD_ATTEMPT_V7.json).

Accordingly, this delivery does **not** contain a newly compiled `build/main.pdf` or `build/two_collision.pdf`. Full TeX cross-reference validation, page-count verification, and rendered-page visual inspection have not been completed. No successful `verification-v7/BUILD_V7.json` has been fabricated. PDF paths elsewhere in the reproduction instructions denote intended build outputs, not currently delivered artifacts. Inherited V5/V6 verification files remain historical evidence for their named versions only.

The source revision and the substantive mathematical response are delivered for independent review. The manuscript's correctness, the finite diagnostics, compilation, visual inspection, and journal acceptance are distinct questions. This branch does not merge or approve its own claims, modify the reviewed source or review branch, or substitute a no-go note for the complete paper.
