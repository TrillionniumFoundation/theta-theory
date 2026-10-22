# New revision CI: prepublication static inspection

This is a read-only inspection before the new source was published. It is not a workflow run, qualification execution, build result or success receipt. No workflow was started or restarted.

## Inspected paths

- `.github/workflows/a2-dyn-physical-roof-variation-20261021.yml`
- `papers/A2-DYN-physical-roof-variation-author-revision/ci/a2-dyn-physical-roof-variation-20261021.yml`
- The new article's `main.tex`, `build.sh`, `requirements.txt`, `tools/validate_revision.py`, `tools/check_source_preservation.py`, `tools/freeze_source_manifest.py`, and `tools/rebuild_preserved_history.py`.

The inspection occurred while the author was still integrating the final new modules and diagnostics. Therefore the integration item below is a snapshot observation, not a defect attributed to a subsequently frozen source.

## Findings relevant to actual CI execution

1. The push branch filter exactly matches the current branch, `revision/a2-dyn-physical-roof-variation-2026-10-21`. Path filters include the new article and its actual root workflow. The preceding article and prior workflow are not build targets of this new job.
2. The root workflow and its article-local `ci/` copy were compared and were byte-identical at inspection. The run records the actual checked-out HEAD and entrypoint hashes. The eventual readback must still bind the actual run's head SHA, not infer it from a later carrier commit.
3. The pinned checkout performs a sparse checkout including the complete new article tree. The build uses the article as its working directory. Python 3.12 is selected and checked; the native TeX packages, fonts, Poppler and pinned Python dependencies are installed before execution.
4. `build.sh` uses `set -euo pipefail` and runs the complete native `all` phase followed by a separate historical reconstruction. The workflow's `tee` pipeline also has pipefail, so a failed build command cannot be hidden by a successful log write.
5. The native driver runs source identity checks, both normal and optimized mathematical invocations, and three actual native TeX passes. It compares the compiler recorder's native TeX closure with the declared closure and rejects undefined references, missing characters and overfull boxes. Those checks identify execution and compilation only; they are not a continuum mathematical certificate.
6. The source verifier checks every one of the 4,393 pinned predecessor files and its reconstructed article tree, preserves the native 260–322 model/proof bytes, and recursively verifies the predecessor package. The new source manifest must be frozen after the final native modules, checker programs and driver arguments are installed.
7. The historical builder copies the preserved historical assembly to an isolated output tree before invoking its original rebuild script. It refuses to overwrite an existing isolated copy. A fresh hosted CI job has a fresh working tree; this preserves separate attempts rather than silently reusing generated historical PDFs.
8. The workflow records the build outcome and uploads actual logs/artifacts under `if: always()`. The artifact name includes source SHA, run ID and attempt. The upload covers native output, current and historical logs, historical PDFs and the historical summary. A completed upload alone is not a successful build: the later audit must read the job/step conclusions and the retained phase summaries.
9. The manuscript wrapper includes all new native modules 323–326 and preserves the complete inherited chain. It expressly leaves the full raw pointwise theorem and four-coordinate inverse conclusion incomplete; it does not identify old favorable A2 geometry assessments as A2-DYN review evidence.

## Integration item observed before freeze

At the inspection snapshot, `validate_revision.py` still had the preceding 31-program list through the 322 diagnostics. The new 323, 324/325 and 326 diagnostics had not yet appeared in `tools/`. This was promptly reported to the author, who was still integrating final proofs and checkers. Before a source can be called fully validated, the actual final driver must include the new diagnostics with their real CLI options and explicit final source paths. Its source manifest must then be frozen on those bytes. No test was run to conceal or work around this pending integration.

## Read evidence

Relevant tool command chunks: `7fa3af`, `1e265c`, `1b7332`, `fd4dac`, `7851aa`, `632975`, `ebc1b2`, `a701ea`, `78fef7`, `634f2a`, `3df8b1`, `89bd23`, `84a8d0`. The byte comparison of workflow copies exited zero (`3df8b1`). These are static read/check receipts, not GitHub Actions executions.

## Pending actual readback

After the author supplies the published source SHA and branch, retrieve the actual workflow run, attempt, jobs, steps, logs and artifacts. Verify the downloaded artifact digest, exact checkout, mathematical source identity, command receipts, normal/optimized comparisons, native compiler closure and PDF identity, and actual historical reconstruction. Preserve all attempts and failures. Do not start or restart a workflow as part of this readback.

## Integration follow-up before publication

A later read of the same current working source resolves the concrete pending integration item above. The driver now includes `check_complete_roof_variation`, `check_canonical_collision_boundaries`, and `check_326_boundary_pressure`, and all three programs are present in `tools/`. Their actual parsers accept the driver's `--details` argument. Their installed defaults resolve the new article's `core/323`, `core/324–326`, and `core/326` sources respectively. The inherited two programs with runtime metadata differences retain their explicit comparison policy; the three new deterministic diagnostics use ordinary byte comparison in normal and optimized modes.

This gives 34 registered programs and therefore 68 planned mathematical invocations, with 59 planned stdout/details comparisons. These are static counts of the driver, not executed results. No additional local diagnostic or workflow was run during this follow-up. Read command chunks: `670889`, `44190f`, `7b95fb`, `670cd2`. The source freeze and actual execution remain the author's subsequent steps, to be verified from real receipts.
