# Actual prior-source CI readback for the next A2-DYN author revision

## Outcome and exact applicability

GitHub Actions run **39424256218**, attempt **1**, completed successfully. Its single job **118632668769**, `native-source-checks-and-build`, and all eleven returned setup, substantive and post-job steps completed successfully. This is an actual finished remote run, not a queued status, local qualification, simulated gate, or proposed workflow.

- Actual tested source commit: `86c947eccea6029258d9a362624866a475118a66`.
- Head repository tree recorded by the run: `4624f0eef13e655c39d6313f6779e6c72a86870e`.
- Head branch: `revision/a2-dyn-critical-source-transport-2026-10-20`.
- Article: `papers/A2-DYN-critical-source-transport-author-revision`.
- Workflow: `.github/workflows/a2-dyn-critical-source-transport-20261020.yml`.
- Event: `push`; created `2026-10-20T12:41:42Z`; job started `2026-10-20T13:46:09Z`, completed `2026-10-20T13:49:33Z`; run updated `2026-10-20T13:49:35Z`.
- Later evidence-carrier commit `4d83de89d16bae7f9e9439dcc80e099b8f8f5c4e` is **not** the tested commit of this run. This receipt makes no test claim for that later commit or the next revision.

Authoritative links:

- [Actual run](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/39424256218)
- [Actual job](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/39424256218/job/118632668769)
- [Tested workflow source](https://github.com/TrillionniumFoundation/theta-theory/blob/86c947eccea6029258d9a362624866a475118a66/.github/workflows/a2-dyn-critical-source-transport-20261020.yml)
- [Retained artifact](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/39424256218/artifacts/12268508880)

## Downloaded evidence and verification

The GitHub plugin returned full run metadata, the exhaustive jobs and artifacts pages (`per_page=100`, both `total_count=1`), the full decoded job log, the exact workflow at the tested SHA, and the actual artifact bytes. `RETRIEVAL_RECEIPT.json` records tools, URLs, IDs, scope and retrieval time. Temporary signed artifact URL is intentionally omitted; the artifact ID and durable GitHub URL identify the evidence.

Artifact **12268508880** is named `a2-dyn-critical-source-transport-86c947eccea6029258d9a362624866a475118a66-39424256218-1`. It was unexpired at retrieval, with recorded expiry `2027-01-18T12:41:42Z`. Downloaded ZIP size **10,660,075 bytes**, SHA-256 **`3d94cf762526903ef6de15e6ee37282b15da0fc6f8ace78c760982b85290cd44`**, exactly matches the GitHub artifact metadata and upload log. All **207** archived files passed CRC checks and their extracted bytes equal the ZIP members. `artifact-inventory.json` records every member's size and SHA-256.

`python3 new-round-ci/verify_downloaded_receipts.py` performs readback checks only. It completed **586** consistency checks and wrote `ARTIFACT_VERIFICATION.json`. It does not rerun source, mathematics, TeX, GitHub Actions, or any historical repository gate.

The actual artifact states:

| Evidence | Verified result |
| --- | --- |
| `current/CI_CHECKOUT_SHA.txt` | Exact tested SHA `86c947eccea6029258d9a362624866a475118a66` |
| `current/CI_BUILD_OUTCOME.txt` | `success` |
| `current/CI_POST_RUN_STATUS.txt` | Only untracked article `build/`; no tracked source modifications reported |
| `current/PHASE_all.json` | `math`, `source`, `typeset` completed; `status: passed` |
| Mathematical source identity | `cbe6dac9cab2bf80dd73119aaeda4d9f3122b42898807a4d0b6ac869eaecbc82` across all phase receipts |
| `current/mathematical-checks.json` | **62 / 62** finite-check commands completed, every exit code zero, no recorded failure |
| Normal / optimized comparisons | **53** comparisons independently reconstructed from the downloaded stdout/detail bytes; all match |
| Native compilation | Three actual `pdflatex` passes, each exit zero; **211 pages**, **74** recorded native TeX inputs matching declared closure |
| Native reference/layout gate | Empty reported problems list; actual `main.aux` and PDF digests agree with receipt |
| Historical rebuild | Original assembler and six TeX passes succeeded on isolated **390-file** historical source copy; PDFs **26** and **883** pages |
| Historical gate scope | `historical_repository_wide_gate_executed: false`; no broader historical gate claim |

For `check_all_offset_boundary` and `check_positive_critical_fans`, normal and optimized JSON differ only by `executed_utc` and `optimized`. Those two runtime fields are excluded in the corresponding comparisons. All other declared comparisons are literal byte comparisons; the verifier independently confirms each declared mode. These checks corroborate the finite script outputs, not their continuum applicability.

Every mathematical and native command-log byte count and SHA-256 was independently recomputed. Every historical command-log identity and both historical final-log/PDF identities was likewise recomputed.

| Actual remote PDF | SHA-256 |
| --- | --- |
| `artifact/current/native/main.pdf` | `c7ffa3571c2ff449033d6df56accd4ac8bc747961d054975862452a213759f32` |
| `artifact/current-history/historical-main.pdf` | `f3c527c6ef20b99c1bd5ff2e9dab583e47540f4c7546cf44f4aa41dc09550f8b` |
| `artifact/current-history/historical-supplement.pdf` | `5706cc97463d6069f11cdcb55c509f14a67f987b45cef15cacd328792d97f43c` |

The exact tested workflow SHA-256 is `cb403706f07e84150d634585400c7f8c77c2d5ef454f574d084f19a6e425fd0c`, equal to the in-article workflow digest in the actual CI entrypoint receipt. Recorded runtime: Python 3.12.15; numpy 2.3.5; scipy 1.17.0; sympy 1.14.0; mpmath 1.3.0; pdfTeX 1.40.25 / TeX Live 2023; Poppler 24.02.0; Ubuntu 24.04 job runner.

## Repair decision and limits

**No CI blocker was found, and no source or workflow repair is justified by this run.** The native compiler reports nonblocking `amsmath` advisories for foreign `atopwithdelims` and `over` commands; the historical main reports `over`. These are not failed steps or missing proof bodies. The next revision should preserve these actual receipts and obtain its own source-specific completed run after its source changes, without moving or rewriting the earlier refs.

All retrieved phase receipts explicitly deny a continuum or mathematical proof certificate. Neither CI success nor these byte-integrity checks establishes uniform billiard estimates, singular-trace closure, the original ordered limits, the full raw pointwise local limit theorem, or the four-coordinate inversion theorem. No visual inspection of the downloaded remote PDFs or independent reconstruction of the mathematical proofs was performed as part of this CI-only readback.

No remote mutation, Actions rerun, source edit, old-ref move, or publication was made by this readback task.
