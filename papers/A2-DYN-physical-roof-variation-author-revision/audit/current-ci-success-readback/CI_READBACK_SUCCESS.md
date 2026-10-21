# Actual source CI readback — completed and artifact verified

This is an author-side evidence readback of the actual GitHub Actions run for immutable source commit `6708e30d1e8511e6ed2f4e3a6247c09628bd3ea9`. The run and artifact were retrieved after the earlier pending observation. No workflow was triggered or restarted, and no mathematical program or compiler was rerun during this readback.

## Exact source and chronology

| Identity or event | Actual value |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Source branch | `revision/a2-dyn-physical-roof-variation-2026-10-21` |
| Tested source commit | `6708e30d1e8511e6ed2f4e3a6247c09628bd3ea9` |
| Source parent | `4d83de89d16bae7f9e9439dcc80e099b8f8f5c4e` |
| Source repository tree | `ad34fd91ad2f1c6e594d3bbe437417aba524bf87` |
| Source article tree | `4f41b3a98487a1ae0507d40390aca030c5520e19` |
| Actual run / attempt | [39526895726](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/39526895726) / 1 |
| Event | `push` |
| Workflow | `.github/workflows/a2-dyn-physical-roof-variation-20261021.yml` |
| Run created | `2026-10-21T01:22:05Z` |
| Earlier complete pending observation | `2026-10-21T01:37:28.119Z` |
| Job / runner | `118983561729` / `1000186257` |
| Actual job started | `2026-10-21T01:39:52Z` |
| Actual job completed | `2026-10-21T01:44:23Z` |
| Completed run last updated | `2026-10-21T01:44:24Z` |
| Artifact downloaded | `2026-10-21T01:50:12.503566+00:00` through `2026-10-21T01:50:13.142025+00:00` |
| Successful independent readback verification | `2026-10-21T01:52:17.788591+00:00` through `2026-10-21T01:52:18.086950+00:00` |

The run, the sole job, and all **11** reported steps completed successfully. The exact checkout receipt inside the downloaded artifact names the source commit above; the retained build outcome is `success`, and the recorded post-run Git status is empty. Actual API metadata are retained in `SUCCESS_API_READBACK.json` and the separate run/jobs/artifacts JSON files.

The earlier pending packet remains unchanged and records what the APIs actually returned at its stated observation time. The pending evidence carrier `d46ba004ff1ac8d44dab04549daff7e3c0e5f205`, and any later success evidence carrier, are distinct from the source commit tested by this run.

## Downloaded artifact and source closure

| Result | Verified identity |
|---|---|
| Artifact ID | `12314306857` |
| Artifact name | `a2-dyn-physical-roof-variation-6708e30d1e8511e6ed2f4e3a6247c09628bd3ea9-39526895726-1` |
| ZIP size | **10,808,391 bytes** |
| ZIP SHA256 | `e83672d52e5e90b9f256d31c316a8a1f7ec17dd0da0b9f7ddf5e5d605278c475` |
| Actual extracted file members | **225**, totaling **24,845,567 bytes** |
| Frozen source manifest SHA256 | `6a8672fb626e605fe9a93f64187421d953d5259cca3ecca5253cd8f11e42ba86` |
| Mathematical-source SHA256 | `52e7443237ebdcc1b2feb6a845c56ab0d87fb61312a781e13572371992bdb5c9` |

The ZIP byte count and SHA256 equal the actual GitHub artifact metadata. All ZIP member CRCs passed; member names are unique, relative, nontraversing paths without symlinks. Every extracted file was compared with its exact ZIP bytes.

The prior independent source readback is copied unchanged: all **130** frozen input paths, Git modes, blob identities, sizes and SHA256 values match the immutable published source. The **129** driver inputs reproduce the mathematical-source digest; the additional frozen file is the article-local workflow copy. That copy equals the published root workflow. The actual CI entrypoint hashes for `build.sh`, `requirements.txt`, and the workflow match these published bytes.

Every actual source/math/typeset/all-phase receipt reports the same 129 input identities and digest. The actual predecessor preservation gate checks **4,393 files**, **544,226,975 bytes**, and reconstructs predecessor article tree `7bcaba2bc1ef7ab393c81a7df84f3e45983c4dfa`.

## Actual mathematics and compilation results

| Execution result | Independently checked from downloaded bytes |
|---|---|
| Finite mathematical programs | **34 distinct programs** |
| Actual normal/optimized commands | **68**, all expected tags present exactly once and all exits zero |
| Actual normal/optimized comparisons | **59**, with exact coverage and successful independent output comparison |
| New native manuscript | **3 actual pdflatex passes** and **1 actual pdfinfo command** |
| Native page count / TeX closure | **233 pages / 78 files** |
| Native PDF size | **1,870,738 bytes** |
| Native PDF SHA256 | `6b8714ff679ade78593da4b63244a5c6ca906d81b38bf40334c8e9a30e1d4239` |
| Native auxiliary-file SHA256 | `b4f3341f78aef0e06b8f2866f8fb58bea7e621386d247e35f8bc7d062e8ec016` |
| Actual isolated historical assembly | **390 source files**, **9 retained command records**, all exits zero |
| Historical main PDF | **26 pages**, **529,079 bytes**, SHA256 `aeb66d2f9b8cc633dcf22903be1b7ece269c7e983749e32b421b4bbcb14c8f35` |
| Historical supplement PDF | **883 pages**, **5,714,956 bytes**, SHA256 `203931a2351f95c53b45bbd6816c5d054e9f27087eefc80e0eabd75a1a9594d3` |

The mathematical command log sizes/hashes, zero exits, current-source bindings, and comparison digests were checked individually. For the inherited `check_all_offset_boundary` and `check_positive_critical_fans` programs, only the already-declared `executed_utc` and `optimized` runtime fields are removed from JSON comparison. Other comparisons require byte identity. The new 323 and 326 diagnostic detail files bind to their exact frozen native proof-source hashes.

The native compiler recorder was parsed independently and matches every one of the 78 declared reachable TeX files. The final native log has no undefined references/citations, multiply defined labels, overfull boxes, missing characters, or fatal-error markers under the retained diagnostic scan. The retained native advisories are the inherited amsmath foreign-command warnings for `\\over` and `\\atopwithdelims`. Historical main retains the foreign-command `\\over` advisory; the supplement reports no such advisory. These warnings are disclosed rather than silently discarded.

Historical stdout, each command-output hash, both final-log hashes and both PDF hashes were checked against the actual isolated rebuild receipt. The historical **repository-wide gate was not executed**; isolated source assembly and compilation do not change that explicit scope.

## Independent readback execution and one predicate correction

The final verifier completed **1,333 receipt, source, path and byte consistency checks**, exit code 0. Its exact result is `ARTIFACT_VERIFICATION.json`; invocation, timestamps, stdout/stderr identities and script hash are retained under `readback-execution/`.

The prepared verifier's first attempt rejected an empty post-run Git status because it expected exactly one untracked generated build directory. Actual empty status is a clean checkout. The only script change allows either empty status or that sole generated build path. The original script, failed attempt stdout/stderr and receipt, and the exact one-predicate diff remain in `readback-execution/attempt1.verifier.py`, `attempt1.*`, and `VERIFIER_REPAIR.diff`. This was a readback assumption correction, not a source failure, CI failure, workflow repair, or rerun. The second attempt uses script SHA256 `f0e92803d5586976548393837f794e0c9420a46e34fec2ebdbb6302976d7ce24`.

## Logs, preservation and mathematical scope

The decoded actual job log has **53,729 UTF-8 bytes**, raw decoded-content SHA256 `49e36a3501f32dc8b4a87dcf1cacfb080e1bad599afb1b1dca7bf4d6db76937b`. Nine auth-header-related log lines were removed before filesystem retention. The saved sanitized log has **52,682 bytes**, SHA256 `7ef9965279d2de1347bedd19b3bed5253df93664bf078310482235792c8abc06`; its exact line-number redaction ledger is `JOB_LOG_RETRIEVAL.json`. No temporary signed download URL, authorization header, or credential is retained.

This evidence certifies the stated source identities, actual CI execution receipts, downloaded bytes, and compile outputs. It is not an external referee report, independent expert certification, or proof of continuous billiard estimates. No visual inspection of the downloaded remote PDFs was performed in this CI-only readback. All actual receipts retain their explicit no-continuum-proof-certificate flags. The full raw pointwise local limit theorem, normalized positive-source/clearance remainder closure and full four-coordinate raw inversion are not established by CI success and remain governed by the manuscript's explicit mathematical dependency ledger.

