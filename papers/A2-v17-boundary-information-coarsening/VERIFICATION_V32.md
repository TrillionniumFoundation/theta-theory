# A2 v32 execution record

Date: September 12, 2026. Mathematical-source commit: `35fd4ccef1b5785692de512635f7240a4df0d641`. Review parent: `9edd5f48d91b74d09718149de6e2c3550c375f20`.

## Current disposition

**C2 is not claimed closed by this source-and-tooling revision.** A complete native-main and companion success must be established from an executed full-source build and inspection of its PDFs. The workflow is an intended procedure until an actual run and artifacts are recorded below. The mathematical-source SHA is not silently substituted for a later build-attempt SHA.

## Executed local diagnostics

`tools/check_revision_v32.py` was executed under Python 3.13.5 in ordinary and optimized modes. The outputs were byte-identical and passed. The recorded output is `verification/v32/diagnostics.json` (SHA-256 `afccaa2f48f87842142089d1de863105332162d8fad2d24c29c08ef5545e6876`).

The checks cover six exact rational score/information identities, the exact geometric affinity `15/17` and corresponding squared Hellinger distance `4/17`, a closed-form normalized triangular moving-boundary diagnostic, one finite-space triangle inequality and illustrative compatible rate sequences. They do not certify billiard realization, all asymptotic hypotheses or the full theorem chain.

Commands actually used were `python3 check_revision_v32.py`, `python3 -O check_revision_v32.py`, and `cmp` on their outputs.

## Executed isolated changed-section syntax check

The actual unchanged native preamble and the two new sections were compiled together with `latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error`, using `pdflatex -no-shell-escape`. No theorem or reference stubs were introduced. The native preamble and both new mathematical files have the exact Git blob identities recorded in `PRESERVATION_V32.md`.

Compiler: pdfTeX 1.40.26, TeX Live 2025/dev/Debian. The result was **five pages**, rendered with Poppler and inspected as a five-page montage. The log has no overfull/underfull boxes or missing glyphs. **Sixteen external labels are unresolved**, and the companion auxiliary file is not supplied in this fixture. The complete list is in `verification/v32/syntax-audit.json`. The isolated PDF SHA-256 is `2a21b20a059dfc9614bfbdd5f22c3e740516fe3ab3a77eb555aed0f7b353a26d`.

This is only a syntax/layout check of changed sections. It is neither the native main nor the companion, is not published as a submission PDF, and does not satisfy C2.

## Executed build-utility regression

The revised builder passed `py_compile` and a synthetic two-file regression using real LaTeX: one deliberately successful file and one deliberately failing file. The successful PDF and failing log both survived. The record is `verification/v32/build-utility-regression.json`. This tests failure-path evidence retention, not the A2 manuscript.

## Complete native procedure

From a checkout of this branch, run:

```sh
P=papers/A2-v17-boundary-information-coarsening
python3 "$P/tools/audit_native_sources_v27.py" --output /tmp/a2-v32-native-graph.json
python3 "$P/tools/build_submission.py" --output-dir /tmp/a2-v32-native-build
```

The output directory must be outside the manuscript tree. Both `two_collision.tex` and `main.tex` are always the native targets. The complete workflow `.github/workflows/a2-v32-native-build.yml` archives immutable source before installing TeX and uploads source, logs, manifests, statuses and product hashes even after later failure. The builder rejects unresolved references/citations, duplicate labels and missing glyphs. Layout warnings are recorded, not converted into a claim that every page has been inspected.

A new complete native workflow attempt is to be observed after the integration commit. No successful full-main PDF, page count or native build hash is asserted in this initial record. Its actual SHA, run/job identifiers, steps and artifacts will be appended after inspection of the authenticated run.
