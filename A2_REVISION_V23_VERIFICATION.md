# A2 v23 verification record

**Revision branch:** `revision/a2-v23-intrinsic-multiscale-top4-2026-09-11`  
**Canonical manuscript-source commit:** `bea3be54dd00cce89a06c65bb9121e078e3f22f1`  
**Canonical source tree:** `b8262ef2962a5f8b290658c1737224c76e3ea814`  
**Revision base / referee-report head:** `7057ec51b341264fa3752a0e5eb466650579bab1`  
**Workflow:** `A2 v23 complete native build`  
**Workflow file:** `.github/workflows/a2-v23-native-build.yml`  
**Workflow run:** `34600520807`

## Source-integrity check

The canonical source commit is a single fast-forward commit from the latest A2 v22 referee-report head.  GitHub compare reports:

- status: `ahead`;
- ahead by: `1`;
- behind by: `0`.

Thus the revision contains the latest referee report in its history and adds the v23 manuscript/response package on top of that immutable review base.

## Exact-head workflow evidence

The workflow was triggered by the push of the canonical manuscript-source commit and targeted exactly

`bea3be54dd00cce89a06c65bb9121e078e3f22f1`.

### Attempt 1

- Run: `34600520807`
- Job: `103266400806`
- Name: `native-build`
- Conclusion: `failure`
- Returned step list: `null`
- No checkout, source archive, dependency installation, LaTeX build, diagnostic check, hash step or artifact upload step executed.

### Explicit rerun

The failed workflow was explicitly rerun through the GitHub Actions API.

- Rerun job: `103266527413`
- Name: `native-build`
- Conclusion: `failure`
- Returned step list: `null`
- Again no workflow step executed.
- The job-log endpoint had no job log to return, consistent with the absence of an executed runner step.

## Interpretation

This is the same zero-step runner/infrastructure failure mode recorded for v22.  It is **not** a successful native-build certificate.  It is also **not** evidence of a TeX compilation failure, unresolved citation, failed mathematical diagnostic, or test failure, because none of those commands executed.

The revision is therefore mathematically/source complete for referee circulation but is **not marked native-build verified**.  A successful runner execution remains the outstanding mechanical verification item.

## Workflow checks configured for the next executing runner

If a runner starts, the exact-branch workflow will:

1. check out and record the exact revision head;
2. archive the exact manuscript source;
3. install the native TeX and numerical dependencies;
4. run `papers/A2-v17-boundary-information-coarsening/tools/build_submission.py`;
5. run `check_boundary_information.py` under normal and optimized Python and require identical output;
6. reject unresolved references/citations and fatal LaTeX diagnostics;
7. record source and PDF SHA-256 hashes;
8. upload exact-source and build artifacts.

No stronger verification claim is made until those steps actually execute and pass.
