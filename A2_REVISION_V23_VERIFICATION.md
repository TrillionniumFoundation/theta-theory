# A2 v23 exact-head verification record

**Revision branch:** `revision/a2-v23-intrinsic-multiscale-top4-2026-09-11`  
**Canonical manuscript-source commit:** `8840bf01ee8a7752504d2913bf00af54656afbb5`  
**Canonical source tree:** `0c8046e22b6a3109ae6e8ceb222f49e6a7219052`  
**Revision base / referee-report head:** `7057ec51b341264fa3752a0e5eb466650579bab1`  
**Workflow:** `A2 v23 complete native build`  
**Workflow file:** `.github/workflows/a2-v23-native-build.yml`  
**Exact-source workflow run:** `34602335326`

## Canonical source

The canonical v23 manuscript source is commit

`8840bf01ee8a7752504d2913bf00af54656afbb5`.

It contains the final theorem-interface corrections made during the referee-response audit: lifted-channel deck labels, admissible periodic gluing, cycle holonomy, the root-calibration distinction, the strengthened analytic-continuation lemma, the endpoint--time corner/coarea estimate, and the simultaneous growing-order diagonal theorem.

Subsequent commits on the revision branch may update this verification record only; they are not new manuscript-source commits unless explicitly declared otherwise.

## Exact-head workflow evidence

Pushing the canonical source commit triggered workflow run `34602335326` with

`head_sha = 8840bf01ee8a7752504d2913bf00af54656afbb5`.

### Attempt 1

- job id: `103272423524`
- job name: `native-build`
- conclusion: `failure`
- returned step list: `null`
- no checkout, source archive, dependency installation, TeX build, numerical diagnostic, reference check, hash step or artifact upload step executed.

### Explicit rerun

The failed exact-head workflow was explicitly rerun through the GitHub Actions API.

- rerun job id: `103272500215`
- job name: `native-build`
- conclusion: `failure`
- returned step list: `null`
- again no workflow step executed.

The GitHub combined-status endpoint for the canonical source commit returns no individual commit status entries.  The Actions evidence above is therefore the operative verification evidence for this revision.

## Interpretation

Both exact-head attempts failed before a runner executed any workflow step.  This is a zero-step runner/infrastructure failure mode.

Accordingly:

- this record is **not** a successful native-build certificate;
- it is **not** evidence of a TeX compilation failure;
- it is **not** evidence of an unresolved citation/reference;
- it is **not** evidence of a failed numerical boundary diagnostic;
- no PDF hash or build artifact can honestly be certified from these runs, because the commands that would produce them never executed.

The mathematical/source revision is therefore ready for referee circulation at the repository-source level, but it is marked **native-build verification pending** until GitHub allocates an executing runner and the configured checks pass.

## Checks configured for the next executing runner

The exact-branch workflow will, once a runner starts:

1. check out and record the exact source head;
2. archive the exact manuscript source;
3. install the native TeX and numerical dependencies;
4. run `papers/A2-v17-boundary-information-coarsening/tools/build_submission.py`;
5. run `check_boundary_information.py` under normal and optimized Python and require identical output;
6. reject unresolved references/citations and fatal LaTeX diagnostics;
7. record source and PDF SHA-256 hashes;
8. upload exact-source and build artifacts.

No stronger verification statement is made until those steps actually execute and pass.
