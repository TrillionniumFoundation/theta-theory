# Actual CI and publication evidence

## Decisive source candidates

The branch census covers all 1,283 repository refs returned by fourteen paginated reads, including 420 A2-DYN refs. Author source identity was checked across 242 author/revision refs and 127 commits, with 115 distinct article trees. The 178 A2-DYN review refs represent 90 canonical reports plus copy/alias refs. Complete identity mappings are in PIPELINE_REF_CENSUS.json and the source-history indices.

The following are fresh exact-head GitHub Actions readbacks. A successful workflow title is insufficient: the actual job steps determine the scope.

| Exact source commit | Run | Actual state | What actually ran |
|---|---|---|---|
| fb99e4d67ef74912f6c69b05c9abff3207572e7a | [39096822675](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/39096822675) | completed / failure; updated 2026-10-18T04:46:12Z | Native source execution failed in job 117584906141. Dependencies and artifact retention passed. The parent job log does not expand the nested source-normal.log; the exact failure cannot be promoted to success. |
| 796e70b65ec17bccb165e047534ed07dd4b148e0 | [39018029024](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/39018029024) | completed / failure; updated 2026-10-17T08:53:30Z | The native continuation validation/build step failed in job 117354038088. |
| ac6a9b5314f5253bea6ff3d4f7bef2103f7fe2a3 | [39007520600](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/39007520600) | completed / success; updated 2026-10-17T07:08:56Z | In job 117322914237, Install native build dependencies and Qualify exact native article when delivered were both skipped. Only source/ref freeze and archive preparation passed. This is not a complete native manuscript qualification pass. |
| 31792379408c5ace2c09284c2eb22d2331023433 | [38832286710](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/38832286710) | completed / success; updated 2026-10-16T04:31:21Z | Job 116753530513 installed dependencies, checked actual retained source identities, ran the stated original/v115 checks and built v112/v115 articles, then uploaded evidence. This later completion does not rewrite the controlling report's earlier queued observation. |
| 3d91709d12db4a292f212d07304ff036f594d892 | [38721146248](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/38721146248) | completed / success; updated 2026-10-15T16:21Z | Job 116375726189 exported and uploaded frozen source. It did not qualify or build a complete new native manuscript. The higher version number remains an export state, not a replacement proof chain. |

The full fresh run-list responses are in history/HISTORICAL_CI_ACTUAL_READBACK.json. Individual raw job/step objects are retained under audit/recovery and history/SUMMABLE_FAILED_CI_JOBS.json. The summable job's 42,699-byte log, including its original UTF-8 BOM and final newline, is recovered exactly in history/SUMMABLE_FAILED_CI_JOB.log with SHA-256 9cee0ebef2da278ec2eb836f1829cf74e60d30b3e36909981d26c1191cf9103f. Fresh metadata serializations are explicitly distinguished from lost pre-maintenance JSON bytes.

These readbacks cover the five decisive candidate heads. Other historical CI observations remain in their frozen original reports, indexed by exact report source. This audit does not claim to have rerun or freshly reread every Actions job in the repository history.

## Dedicated current workflow

The new workflow is restricted to pushes on revision/a2-dyn-global-minimizer-localization-2026-10-18 affecting the new article or its own dedicated workflow, plus workflow_dispatch. It requests contents: read, Ubuntu 24.04 and Python 3.11. Its pinned checkout, Python setup and artifact-upload actions were checked against their actual action metadata. Dependencies include the required native TeX/AMS fonts, lmodern and Poppler; Python requirements are pinned.

It executes the actual new article build.sh with pipefail and captured output. The build invokes source validation, all 38 mathematical commands, three current LaTeX passes, the unchanged historical assembler and six historical LaTeX passes. An always-run artifact step retains the actual build/current and historical-v108/build logs and PDFs, environment record and captured build status. The final preparation also includes evidence/current-execution/historical-recovery, where the historical helper writes its individual command receipts and REBUILD_RECEIPT.json.

The dedicated workflow and its article-local copy have identical SHA-256:

607decd2715cde18209e43ececd68af176fb4b4481aee4e2d6649fb62ebe4781.

Their final prepared Git blob identity is e2bddac6d9c790731b709997adad3df0f245f2ce, 3,762 bytes. The earlier 3,642-byte workflow (SHA-256 574e33889e66bb6fbdb8b1613f5b72811ae6226fbb7580682112a6b59b94d4cf; uploaded blob 1aa6981a0bb3966d9ef49b7b5733a6056807fafd) is preserved verbatim at history/pre-maintenance-author-documents/DEDICATED_WORKFLOW_BEFORE_RECEIPT_PATH_ADDITION.yml. The only change adds retention of the actual historical command receipts. No old workflow is changed by this audit. The immutable baseline workflow has also been freshly read into history/BASELINE_WORKFLOW_READBACK.json.

## Maintenance recovery and publication boundary

The workspace was pruned during the first remote blob transfer. At that instant the dedicated workflow blob existed remotely, but the new manuscript had not been committed or pushed. The interruption is recorded explicitly; an isolated uploaded blob is not a branch commit or a published manuscript.

All 1,178 placements of 699 previously remote source blobs were recovered and verified against the pre-maintenance SHA-256/Git-blob inventory. Original reports, native mathematics and the preserved historical closure retain exact bytes. New generated proof serializations that could not be recovered exactly were reconstructed, identified as such and rechecked on their current hashes. Old execution logs are not invented from later successful runs.

Actual local rebuild evidence and any subsequent source commit, branch update and exact-head CI are recorded by the root publication files. This audit establishes the historical CI and local workflow facts above. It neither predicts a pending run's conclusion nor represents local finite checks or PDF compilation as proof of the continuous Lorentz-gas local-limit theorem.
