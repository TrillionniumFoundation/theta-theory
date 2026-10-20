# Actual C2 artifact evidence and unresolved workflow completion

This packet preserves actual observations and downloaded execution records for
the marked-boundary A2-DYN author revision. The artifact data audit passed.
**The complete CI verifier did not pass: structured workflow completion remains
unverified.** These are different results, both retained without changing any
observed status, conclusion, timestamp, job step, source file, or validation gate.

## Exact tested source and observed identities

| Item | Actual identity |
| --- | --- |
| Author branch | `revision/a2-dyn-marked-boundary-source-2026-10-19` |
| Dedicated workflow | `.github/workflows/a2-dyn-marked-boundary-source-20261019.yml` |
| Tested C2 commit | `efde9fa6c45e7835989b653622a9870e59027530` |
| Repository root tree | `b5d618b8a4b356f8ca07f1c9f1238e35d879ede8` |
| Article tree | `b4add0580cc8211223dfa57e6e618e2bf9546d09` |
| Complete expected article inventory | 3,596 files; 427,208,639 bytes |
| Expected inventory SHA-256 | `e2009b63912d698f7eaf4a8875e332d3ff5bf23b53059f243f7236272cb3dc38` |
| Actual run | [39281615689](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/39281615689) |
| Actual job | `118156848926` |
| Actual artifact | `12201151164` |
| ZIP | `a2-dyn-marked-boundary-source-39281615689.zip` |
| Actual ZIP size | 11,125,810 bytes |
| Actual ZIP SHA-256 | `3dd55cb52656fea0ec950367067a4a27a6ad08ebed77fd5ee0b4400d7f7ae604` |
| Exact returned job-log UTF-8 bytes | 56,469 bytes |
| Exact returned job-log SHA-256 | `b2af50f6c31763c3cfbf458f1f3e5c20ca477da3e2f754280ba3d616f33534a6` |

The exact observed C2 source is used throughout. A later publication commit that
archives this evidence is a distinct Git identity; it is not silently substituted
for the archived checkout. The actual commit/root/ref transport and complete
remote preservation verification are recorded separately by the publisher.

## What the final structured observations actually say

The latest readbacks in this packet were obtained on **2026-10-19 at
16:21:22 UTC**. The run and job returned `in_progress`, with `conclusion: null`;
the job also retained `completed_at: null`. Eleven actual job steps were present,
and every step returned `completed` / `success`, including `Complete job` with an
observed completion time of 15:59:35 UTC. The artifact identity was unchanged.
The aggregate workflow and job conclusion is therefore still unverified.

Earlier connected-tool and independent public-API observations returned
`queued` / `null`, despite the actual uploaded artifact and completed command
records. The latest observations show a real transition to `in_progress`.
This packet does not assign an unverified cause to the difference between those
structured records and the execution log. It preserves all actual responses.

`FINAL_OBSERVATION.json` contains the unchanged 16:19:46 objects. The later and
controlling final readback is
`LATER_RUN_JOB_ARTIFACT_RAW_OBSERVATIONS_20261019T162122Z.json`, which contains
the exact response strings and parsed objects for all three endpoints.
`CURRENT_CI_SCOPE_SUMMARY.json` indexes the final state and the separately scoped
verification results. A later readback must be saved in a new packet.

## Original full verifier: actual failure retained

`verify_actual_ci_artifact.py` is the byte-identical sealed recovery verifier:
46,440 bytes, SHA-256
`e44db871d6afaea2aaac23ec836ceb1e57993ecb464afcf884475530b1e7b42f`.
It was actually executed at 16:12:56.510876–16:13:05.552780 UTC against the
unchanged independent public-API observation acquired at 16:10:07 UTC.
The original source, anchor and reference checks completed before execution
stopped at the original condition requiring `completed` / `success`.

The process returned **exit code 1**, with empty stdout and 635 bytes of stderr.
The final exception was `RuntimeError: Actual run completed successfully`.
That sentence is the assertion's diagnostic label, not a statement that the
workflow succeeded. The actual argv, executable, byte identities, start/end
times, stdout, stderr and exit code are retained in
`strict-verification-queued-161007/`.

The original completion condition was neither removed nor overridden. There is
no successful `CURRENT_CI_ARTIFACT_VERIFICATION.json` in this packet. The queued
observation used in that execution remains unchanged; it was not replaced with
invented successful job steps or timestamps.

## Separate artifact data audit: actual pass with explicit limits

The current data report is
`artifact-data-only-verification-v2/ARTIFACT_DATA_ONLY_VERIFICATION.json`.
Its principal fields are `data_checks_status: "passed"` and
`workflow_completion_verified: false`. The program does not call or alter the
full verifier's `main()` or `require()`. It imports only the fixed-hash helper
module for canonical trees, source parsing, identity checks and command/PDF
inspection. It executes no archive code and extracts no archive member.

Version 2, `verify_actual_artifact_data_only_v2.py`, has SHA-256
`333214be9f891b8dab1518ad2311899d94f25fe457708e6025678efe8a5a52cd`.
Its actual run at 16:21:01.612636–16:21:07.241909 UTC returned **exit code 0**
with empty stderr. The invocation, exact outputs and exit receipt are retained
in `data-only-execution-2/`.

The report verifies the following data directly.

| Check | Verified scope |
| --- | --- |
| ZIP bytes | Advertised byte count and SHA-256; every one of 249 members actually read; clean CRCs; unique safe names; no symlinks |
| Source identity | Archived checkout equals the actual C2; all three dedicated entrypoint hashes match the tested tree |
| Frozen inputs | Schema 5; all 1,837 source rows and 139,367,900 source bytes; every actual row's byte count, SHA-256, Git blob and file mode |
| Preserved history | Four complete source anchors; original predecessor trees and proof numbering; all 90 original indexed reports plus the distinct original v73 copy |
| Native source | All 59 complete bodies 260–318, each included once; 69 reachable TeX files; 897 unique labels; 86 labels in the new bodies |
| Mathematical fingerprint | All 107 current native/tool inputs; `ee0bd027bf5b4263ea5c6eebfb8ffe2d24c8fa0b21d1187f0967bfcaf0a221a5` |
| Mathematical commands | All 52 actual commands, each with expected argv, correct article, exit 0, exact individual receipt, actual output hash, source fingerprint and phase interval |
| Paired output bytes | All 43 actual comparisons: 26 stdout pairs and 17 details pairs; both files read and compared byte for byte |
| Native build | Three actual TeX passes and actual PDF inspection; each command receipt/log checked; 195 pages independently read from actual PDF bytes |
| Native references | Actual PDF identity checked; actual auxiliary bytes equal the final local auxiliary bytes; main-source identity checked |
| Current historical rebuild | Exactly one rebuild beginning after this native phase: `20261019T155902472797Z`; all nine commands, 390 source inputs, complete 26-page main and 883-page supplement |
| Earlier history | Six older historical receipts retained and listed separately; no old receipt substituted for the current rebuild |
| Environment and outputs | Actual Python 3.11 environment and every frozen package pin; post-run changes confined to generated outputs |

The complete expected inventory reconstructs 156 article Git subtrees. The
source/anchor/reference audit actually reads 2,935 unique local input files; this
is recorded separately from reconstruction of all 3,596 inventory rows.
`ARTIFACT_MEMBER_IDENTITIES.json` records every downloaded member.
`ACTUAL_LOCAL_INPUT_IDENTITIES.json` records each unique local file actually read.

The archived complete phase ran at 15:57:49.505755–15:59:02.429940 UTC.
The actual current historical rebuild ran at
15:59:02.472998–15:59:27.781466 UTC. All checked command intervals lie within the
appropriate phase or historical interval, and both lie within the exact job-log
interval. The data audit does not replace the original structured-run time gate
with an invented `updated_at` value.

The actual CI native PDF contains 1,659,306 bytes and has SHA-256
`b54be63ba6088a96f957e8736227cf61a18a5bbf7b28613254e263207a87ead2`.
Its page count and auxiliary bytes match the final local reference. The data
report does not claim that the local and CI PDF binary files are identical.
The frozen manifest SHA-256 is
`0d4439dc86fab1f1226b41506c67a0069edbe21ea9bfd741a099d725fd94f143`.

### Retained correction to the first data-only audit

The exact returned log starts with a UTF-8 BOM. Version 1's timestamp expression
missed that first line and reported the next timestamp,
15:55:55.6941975 UTC, as the first match. A separate author-side assistant
reconstruction identified the problem. Version 2 accepts the existing BOM and
correctly reads the true first timestamp, **15:55:55.6914264 UTC**. No log bytes,
phase boundaries, source checks or workflow completion conditions changed.

The original program, `data-only-execution-1/` and
`artifact-data-only-verification/` remain as superseded evidence. The correction
is explicitly recorded in `DATA_ONLY_V2_BOM_CORRECTION.json`. The version-2 report
is the current data-only result. This author-side reconstruction is not a new
referee report or independent human specialist certification.

## Download and exact-log provenance

The ZIP was obtained using the purpose-built GitHub artifact download tool.
The initial sandbox network attempt failed with zero bytes received; its actual
failure receipt and exit are retained. The authorized read-only network attempt
then downloaded all 11,125,810 bytes and matched the advertised digest. Its
receipt contains actual HTTP status, byte count, hash and time interval.
The ephemeral signed download URL was neither printed nor persisted in this
packet; only unsigned metadata and artifact identity are retained.

`CI_JOB_LOG_RAW_RESPONSE.json` retains the exact returned Unicode text and the
tool-observation times. `CI_JOB_LOG_EXACT.log` contains its exact UTF-8 encoding,
including the initial BOM and its existing final newline. No newline was added
or removed. `CI_JOB_LOG_IDENTITY.json` records that byte identity.

An unsupported generic single-job URL produced an actual connector error. The
error is retained with its query; subsequent supported connected views and the
publisher's direct public-API readbacks are separate observations. The public
API's initial rate-limit failure and later HTTP-200 readbacks are preserved in
the publisher's adjacent `independent-public-api` evidence directories. Those
failures are transport/metadata observations, not mathematical failures.

## Reproducing the original failure and data-only pass in another workspace

Use a fresh workspace with the actual C2 checkout at
`$WORKSPACE/theta-theory`. Place this complete packet at any `$PACKET` path.
Copy the publisher's exact C2 expected inventory, after checking its SHA-256
above, to
`$WORKSPACE/iteration-20261019c-recovery/current-transport/c2-staged-b5d618b/EXPECTED_FILE_IDENTITIES.json`.
Python 3.11 or later and `pdfinfo` must be available. The verifier itself uses
the standard library and does not execute the archived mathematical programs.

First execute the unchanged full verifier against the retained actual queued
observation, recording a real new failure at the original gate in the new
filesystem layout:

```bash
python "$PACKET/execute_artifact_verifier.py" \
  --workspace "$WORKSPACE" \
  --observation "$PACKET/ACTUAL_STRUCTURED_OBSERVATION_QUEUED_161007.json" \
  --output-dir "$WORKSPACE/reproduced-strict-observation"
```

The expected process exit for this unchanged historical observation is **1**.
Next audit the real archive data using that newly recorded real execution:

```bash
PYTHONDONTWRITEBYTECODE=1 python "$PACKET/verify_actual_artifact_data_only_v2.py" \
  --strict-execution "$WORKSPACE/reproduced-strict-observation/ACTUAL_VERIFIER_EXECUTION.json" \
  --output-dir "$WORKSPACE/reproduced-artifact-data"
```

This avoids editing or translating the original execution receipt. The new
strict invocation has its own actual filesystem paths, output bytes and exit;
the archived API objects are unchanged. Output directories must be new.
To verify a later truly completed observation, invoke the original full
verifier with explicit fresh actual metadata and a new output directory; preserve
the earlier observations and results separately.

These finite execution and identity checks support reproducibility. They do not
prove the complete continuous triangular Lorentz-gas local limit theorem, close
an unresolved boundary or spectral estimate, or certify journal-level peer review.

## Separate author-side reconstruction of the data audit

`independent-author-side-data-reconstruction/` is an exact copy of a separately
sealed assistant reconstruction. Its actual version-2 rerun at
16:22:46.452903–16:22:54.757838 UTC returned exit 0; every report field other than
the execution clocks agreed with this packet's version-2 report. A second
independently written check actually performed 366 checks on the original API,
ZIP, exact log, command/pair outputs and PDF data at
16:25:49.986234–16:25:50.498051 UTC and returned exit 0. It again explicitly
records `workflow_completion_verified: false`.

The independent report is `INDEPENDENT_ARTIFACT_DATA_CONSISTENCY.md`, SHA-256
`529701629fe8c75529a0de922f228021f3eaac7f40ba8544e12388edf817d598`.
Its original 19-file payload seal is retained along with the seal file itself:
SHA-256 `a0a3861c50b8f7a8835f22e21dc47597f9a9847ce9f7349ef822bf43e46611ab`.
An initial failure of its local path adapter and the exact path-only correction
are both retained. No API status or archive data was changed to obtain a pass.
`INDEPENDENT_SUBPACKET_COPY_RECEIPT.json` verifies every copied byte. This is an
author-side reproducibility check, not a new external referee endorsement.
