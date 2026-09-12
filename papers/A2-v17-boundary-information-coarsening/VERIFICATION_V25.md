# A2 v25 verification record

Date: September 12, 2026.  
Revision branch: `revision/a2-v25-observable-calibration-signature-top4-2026-09-12`.

## Executed finite diagnostics

The following commands were executed in the local working environment on the complete v25 diagnostic script:

```sh
python check_revision_v25.py --math-only > diagnostics-normal.json
python -O check_revision_v25.py --math-only > diagnostics-optimized.json
cmp diagnostics-normal.json diagnostics-optimized.json
```

All three commands succeeded. The two JSON outputs were byte-identical. Their committed output is `diagnostics/v25-finite-checks.json`.

The 337 counted finite cases consist of 96 exact determinant-one jet-block inverses, six exact rank-two lattice/Gram cases, four exact rational Hermite right inverses, 144 exact pilot timing brackets, two distinct-gap quadratic witnesses, six scalar/enriched oval-signature pairs, nine strictly convex noisy-matching Hessian cases, 40 exact one-flight slice identities, 20 layer/bulk finite bounds and ten sensor-frame equivariance checks. Exact algebraic cases use rational arithmetic. The explicitly numerical signature, Hellinger and rigid-motion checks use stated finite tolerances. These tests are diagnostics, not proofs of uniform infinite-dimensional theorems.

The locally executed script was 11,921 bytes. Its SHA-256 was

`259df162c2ab90734994dc991bf619dc84838a4f5c31cab7159188fa9007cd0c`.

Its Git blob SHA-1 was

`70642238fa71284bfdff562bf40c6528290e4216`.

The GitHub connector independently returned that same blob SHA for the committed `tools/check_revision_v25.py`. Thus the executed finite diagnostics were not run on an uncommitted alternate implementation.

## Not certified by those finite tests

The `--math-only` flag was used deliberately because the connected private repository was readable through the GitHub connector but was not available as a complete local native checkout. Therefore the local run did **not** execute the script's full recursive input/reference/citation scan, its byte comparison against the pinned v24 checkout, or the semantic source-token assertion on the entire checkout.

Those additional checks are implemented for a complete checkout and requested by the native workflow. Their presence in a script is not evidence that they have run. Source files and entry-point changes were inspected through the connector, and the Poisson intensity was written with the literal `\rho` control sequence; the whole-tree automated semantic audit remains part of the native execution requirement.

## Native build attempts

The first exact-head hosted workflow was:

- workflow: `A2 v25 complete native build`;
- run: `34661518521`;
- source commit: `d76e58871bdd1f74f36cc1a64be5abc201357f24`;
- job: `103464825643`;
- recorded status: completed/failure;
- recorded steps: empty;
- recorded runner identifier: zero, with no runner name;
- job-log download: `BlobNotFound`.

No LaTeX, source-audit or diagnostic step ran in that attempt. The API metadata does not establish a specific billing or runner-allocation cause, so none is asserted here.

The workflow was subsequently routed to the repository's existing `self-hosted`, `linux`, `x64` labels. Pushes on the revision branch request exact-head executions; concurrency cancels superseded runs. A queued execution is not a successful build. No successful whole-paper v25 native build report, compiled v25 PDF, PDF page count or PDF hash is asserted in this record.

The workflow, once executed, checks both **complete** native entry points, `two_collision.tex` and `main.tex`, including every active appendix and bibliography. It archives the exact source commit, source tarball, active source hashes, normal/optimized diagnostics, build logs, native build report, PDF metadata and PDF hashes. It rejects unresolved references, duplicate labels and missing glyphs through the retained build utility. It does not substitute an isolated revised-section smoke test.

## Reproduction from a complete checkout

From the repository root:

```sh
python3 papers/A2-v17-boundary-information-coarsening/tools/check_revision_v25.py
python3 -O papers/A2-v17-boundary-information-coarsening/tools/check_revision_v25.py
python3 papers/A2-v17-boundary-information-coarsening/tools/build_submission.py \
  --output-dir /absolute/path/outside/the/manuscript/tree
python3 papers/A2-v17-boundary-information-coarsening/tools/check_boundary_information.py
python3 -O papers/A2-v17-boundary-information-coarsening/tools/check_boundary_information.py
```

`latexmk`, `pdflatex`, the required TeX packages, `pdfinfo`, NumPy and SciPy are needed for the complete route. The output directory must be outside the source tree. Pin the checked-out commit and preserve the generated `build-report.json`, source manifest, logs and hashes when evaluating the result.

## Mathematical review status

The new sections contain author proofs responding to M1--M3 and the further technical requests. The manuscript distinguishes exact rigidity, finite noisy matching, a non-effective compact inverse modulus, a specified finite-rank variation model, local information experiments and a common-observable global acquisition protocol. Finite diagnostics and a future clean typesetting build do not independently certify those proofs or establish acceptance at any journal. The new branch is submitted for another referee reading, not merged into `main`.
