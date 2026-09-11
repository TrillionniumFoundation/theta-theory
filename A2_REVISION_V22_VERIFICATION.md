# A2 v22 verification record

**Canonical manuscript-source commit:** `82a19b18f35fee63819bcc99d530f52adf56c384`  
**Workflow:** `A2 v22 complete native build`  
**Workflow file:** `.github/workflows/a2-v22-native-build.yml`  
**Workflow run:** `34595965653`

## Exact-head workflow evidence

The workflow was triggered by the canonical manuscript-source push.

### Attempt 1

- Job: `103251658435`
- Name: `native-build`
- Conclusion: `failure`
- Returned step list: `null`
- No checkout, dependency installation, LaTeX build, diagnostic check or artifact upload step executed.

### Explicit rerun

The failed job was explicitly rerun through the GitHub Actions API.

- Rerun job: `103251787513`
- Name: `native-build`
- Conclusion: `failure`
- Returned step list: `null`
- Again no workflow step executed.

## Interpretation

This is a zero-step runner/infrastructure failure.  It is **not** a successful native-build certificate, and it is **not** evidence of a LaTeX compilation failure.  The repository therefore still lacks the successful exact-head native build requested by R21-7.

The workflow itself is configured to perform, if a runner executes it:

1. exact-head checkout and source-commit recording;
2. source archive capture;
3. native TeX/Python dependency installation;
4. the repository `build_submission.py` build;
5. boundary-information diagnostics under normal and optimized Python;
6. rejection of unresolved references/citations and fatal LaTeX diagnostics;
7. source and PDF hash recording;
8. artifact upload.

No claim of successful submission verification is made until those steps actually execute and pass.
