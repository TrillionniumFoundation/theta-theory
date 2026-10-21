# Actual new CI readback — pending runner

This report records the actual GitHub Actions state retrieved at **2026-10-21T01:32:37.823Z**. It does not claim a completed CI test, remote compilation, successful workflow, or verified artifact. No workflow was started or restarted during this readback.

## Exact published source

- Source commit: `6708e30d1e8511e6ed2f4e3a6247c09628bd3ea9`.
- Branch: `revision/a2-dyn-physical-roof-variation-2026-10-21`.
- Parent: `4d83de89d16bae7f9e9439dcc80e099b8f8f5c4e`.
- Repository root tree: `ad34fd91ad2f1c6e594d3bbe437417aba524bf87`.
- Article tree: `4f41b3a98487a1ae0507d40390aca030c5520e19`.
- Frozen manifest SHA256: `6a8672fb626e605fe9a93f64187421d953d5259cca3ecca5253cd8f11e42ba86`.
- Driver mathematical-source SHA256: `52e7443237ebdcc1b2feb6a845c56ab0d87fb61312a781e13572371992bdb5c9`.

The GitHub commit API returned the stated root tree and parent. The published root workflow and source manifest were fetched at the immutable source SHA. All **130** frozen file paths, modes, blob identities, byte counts and SHA256 values were independently matched against that committed article tree. The **129** inputs used by the mathematical driver reproduce the exact digest above; the remaining frozen input is the article-local workflow copy. That copy equals the actual published root workflow byte for byte. The declared native TeX closure contains **78** files. These are source-identity checks, not remote CI executions.

Exact retrieved sources and the detailed identity result are retained in `tested-source/` and `PUBLISHED_SOURCE_READBACK.json`. The publication status continues to mark the full raw pointwise LLT and full four-coordinate inversion as incomplete.

## Actual remote run and job

- [Run 39526895726, attempt 1](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/39526895726).
- Run created: `2026-10-21T01:22:05Z`.
- Event: `push`; the API head SHA equals the exact published source commit.
- Workflow: `.github/workflows/a2-dyn-physical-roof-variation-20261021.yml`.
- Job: `118983561729`.

| Item observed through the API | Actual state |
|---|---|
| Run status / conclusion | `queued` / `null` |
| Job status / conclusion | `queued` / `null` |
| Assigned runner | `runner_id=0`, empty runner name |
| Returned job steps | **0** |
| Returned artifacts | **0** |
| Actual checkout receipt | Not yet produced or verified |
| Remote mathematical command results | Not executed/verified in this readback |
| Remote native or historical compilation | Not executed/verified in this readback |
| Downloaded/verified artifact | None |
| Downloaded job log | None; no executed step has been reported |

The job metadata contains a `started_at` field even while the authoritative status is queued and no runner or steps are assigned. That field is retained verbatim in the API record and is **not** interpreted as an executed checkout or test. The reason for runner nonassignment has not been inferred. No source/workflow failure has been observed, and a successful conclusion has not been manufactured.

## Planned driver versus completed execution

The committed driver registers **34** programs, **68 planned normal/optimized invocations**, and **59 planned stdout/details comparisons**. These are plans visible in the source. They are not counted as completed remote CI tests here. Local build and verification receipts, where separately provided by the author, retain their local scope and do not change this pending remote status.

The prepared `verify_current_ci_artifact.py` has **not been executed** against this run because no artifact exists yet. This packet does not contain an `ARTIFACT_VERIFICATION.json` success report or an artifact ZIP. When an artifact is actually available, the verifier is designed to check its GitHub digest, exact checkout and source identity, all command-log hashes, actual normal/optimized outputs, compiler recorder closure, PDF identity, and the actual isolated historical reconstruction. It does not rerun source tests or certify continuous mathematics.

## Preserved evidence and handling

The actual API run, job and artifact responses are retained in `run-39526895726.json`, `jobs-39526895726.json` and `artifacts-39526895726.json`. Timestamped earlier responses remain in `snapshots/`; `PENDING_CI_READBACK.json` makes the pending flags explicit. Published source retrieval and verification use the actual command records identified by chunks `76ab8f`, `e122f2`, and `55d4db`.

No temporary signed download URL, authorization header or credential is saved. Public repository/action URLs, IDs, source hashes and local filenames suffice for this record. This status can be updated only after fresh actual API results and, for artifact verification, downloaded bytes are obtained. Any later evidence-only carrier commit is distinct from the source SHA scheduled by this run.
