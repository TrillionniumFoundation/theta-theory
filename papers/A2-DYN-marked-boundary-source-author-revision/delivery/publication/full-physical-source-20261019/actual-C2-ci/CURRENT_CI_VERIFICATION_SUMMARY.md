# Actual C2 CI artifact and frozen-source verification

**Verified successfully on 19 October 2026.** This packet records an actual completed GitHub Actions run, actual downloaded ZIP bytes, the exact returned job log and an independently executed offline artifact verifier. It is not a simulated workflow qualification or a reused earlier run.

## Exact tested identity

| Object | Verified identity |
| --- | --- |
| Author article | papers/A2-DYN-full-physical-source-author-revision |
| Dedicated workflow | .github/workflows/a2-dyn-full-physical-source-20261019.yml |
| Tested commit | 228ec6a639d4d195a1a8b869a04dae6f49fece0e |
| Repository root tree | 431dfd86fcd60e50a1469af38343afc470527752 |
| Article tree | 826219579509e91c87c8dfb0c6348e2c42dba178 |
| Actual run | 39229329979, completed/success |
| Actual job | 117983194322, all eleven actual steps completed successfully |
| GitHub completion update | 2026-10-19T09:24:04Z |
| Actual artifact | 12176597487 |

Run URL: https://github.com/TrillionniumFoundation/theta-theory/actions/runs/39229329979

The observation files preserve the transition from dependency installation, through the actual complete rebuild, to completed/success. FINAL_OBSERVATION.json contains the run, job and artifact payloads read at 09:24:57–09:24:58 UTC. C2_INITIAL_REMOTE_READBACKS.json and C2_FILE_IDENTITIES.json preserve the separately obtained exact remote source identity. The latter contains 2,710 expected files totaling 292,904,889 bytes; the verifier independently reconstructs its 114 canonical Git subtrees and exact article tree. Its byte-level source verification concerns every frozen input, every native/tool input and every selected final local reference, as enumerated below.

## Actual downloaded bytes and exact job log

The purpose-built GitHub artifact tool returned a signed file reference. The signed URL was used only for transport and was neither printed nor saved in this packet. The actual ZIP is retained as **CI_ARTIFACT_12176597487.zip**:

- Size: **10,908,310 bytes**.
- SHA-256: **ea2d3207346ed78239dc439971105537f408d5743ff827aef178d9b852ae32a4**.
- All **218** file members were read, hashed and checked for valid ZIP CRC.
- Duplicate, absolute, traversing and symbolic-link member paths were rejected by the verifier.

The first default-sandbox transfer failed before receiving any bytes. Its unsigned receipt is retained as ARTIFACT_DOWNLOAD_DEFAULT_SANDBOX_FAILURE.json. The authorized network-enabled transfer then returned HTTP 200 and completed at 09:26:28.121245 UTC; ARTIFACT_DOWNLOAD_RECEIPT.json records the successful exact size/digest comparison. This was a transfer-environment retry, not a failed CI source or mathematical gate.

The purpose-built job-log tool returned decoded UTF-8 text, saved without an added newline as **CI_JOB_117983194322.log**. It has **56,330 bytes** and SHA-256 **ebd1c2874eb33a8b55a11da71661593ffa28241a00a5613a7029f62b2092952d**. CI_JOB_LOG_IDENTITY.json records that exact identity.

## Frozen input and execution checks

The generic verifier was run under ordinary Python from 09:26:57.194707 to 09:26:58.657926 UTC. It exited zero with empty stderr. Its exact command, program hash, stdout/stderr byte counts and digests are retained in VERIFIER_EXECUTION_RECEIPT.json. The verifier executes no code from the ZIP.

| Check | Actual verified result |
| --- | --- |
| Frozen SOURCE_MANIFEST | SHA-256 13182b20479bcafcd8a3d53804b9cc610739e5a8ad0fb94f32eed65b4768f997 |
| Frozen source/evidence inputs | All 1,668 inputs, totaling 122,736,124 bytes, matched exact tested expected bytes, SHA-256 and Git blob identity |
| Native/tool inputs | All 101 current mathematical source and Python-tool inputs matched exact tested identities |
| Mathematical fingerprint | ebe48d08b94fc0dceecce96ecef8e0bc81d91918521ee1ba24558d549d558b26 |
| Entrypoints | Actual build.sh, requirements.txt and dedicated article workflow-copy hashes matched the tested source |
| Complete CI phase | Source, mathematics and typeset passed from 09:22:25.679660 to 09:23:30.209763 UTC |
| Mathematical commands | All 46 actual commands matched the final local program/option contract, returned zero, and had matching individual receipts and log bytes/hashes |
| Ordinary/optimized comparisons | All 37 required stdout/details pairs were present and byte-identical |
| Retained reports | All 90 original reports verified by the complete source gate |
| Active native source | 56 complete core bodies and 66 reachable TeX files |
| Native document | Three actual TeX passes and one PDF inspection, all successful; independently inspected 174 pages |

The actual native CI PDF has **1,538,407 bytes** and SHA-256 **b34e945a993f59a753ab5018484146bf26ef68fd68f68c0bdbbcff871ba55188**. Its auxiliary-file SHA-256 is **08953321181571d1b4f2f2a08e7d82dbec449ab19fff54bc22bdcb9d3c7c2b67**, equal to both the actual CI receipt and the final local auxiliary file. Every selected local reference receipt and local PDF/aux was itself checked against the exact tested article tree.

The only native advisories are the preserved amsmath foreign-command notices for the historical over and atopwithdelims commands. The current native receipt reports no layout or unresolved-reference problems.

## The newly produced historical rebuild

The verifier did not select a historical receipt merely because it was present in the ZIP. It selected the unique execution whose actual start was after this CI's native phase:

**evidence/current-execution/historical-recovery/20261019T092330252503Z/REBUILD_RECEIPT.json**.

That actual historical execution ran from **09:23:30.252690 to 09:23:56.541059 UTC**, checked **390 original source files**, and completed all **nine** required historical commands. Every recorded command output was read and its byte count, SHA-256 and Git blob identity checked. The complete resulting documents were independently inspected:

| Historical document | Actual pages | Actual PDF SHA-256 |
| --- | ---: | --- |
| Main | 26 | db6fd0d912c13d0fe336244c9a117bd745695cd5b8da4ebe1871dfa959fa4d8c |
| Supplement | 883 | b352619e2f4e053acf5471be4fc7f9828a8253b1ee396910c55bb997fdec76bd |

The final historical PDF/log identities were checked against this fresh receipt. The original main retains its amsmath foreign-command advisory; the supplement has no recorded diagnostic. The receipt explicitly retains its historical source/build scope and does not claim to execute the whole historical repository gate or certify a mathematical proof.

Five earlier historical execution receipts, including the genuine earlier failed attempt, remain in the archive and are individually listed in CURRENT_CI_ARTIFACT_VERIFICATION.json. They are not counted as this CI's new historical reconstruction.

All actual post-run changed paths are generated native or historical build products and the newly generated historical execution evidence. No frozen source input is reported modified. The actual environment contains Python 3.11.17 and all frozen numerical pins: mpmath 1.3.0, NumPy 2.3.5, SciPy 1.17.0 and SymPy 1.14.0.

## Files and reproducibility

- **CURRENT_CI_ARTIFACT_VERIFICATION.json** is the complete structured result, including exact tested identities, timestamps, counts, PDF/aux identities, newly produced historical receipt and separately preserved older receipts.
- **CURRENT_CI_ARTIFACT_FILE_MANIFEST.json** records every actual ZIP member's size, SHA-256 and Git blob identity.
- **ACTUAL_LOCAL_INPUT_IDENTITIES.json** records the local bytes checked against the tested expected tree.
- **verify_actual_ci_artifact.py** is the exact independently executed verifier; its SHA-256 is e4bbbe2adcba3fc81fc8cd91f2fb2d80144e946c16ea537b7596dbb0b07d01e1.
- **VERIFIER_EXECUTION_RECEIPT.json** contains the exact invocation and process result; **verify_actual_ci_artifact.stdout.json** and **verify_actual_ci_artifact.stderr.txt** preserve the exact outputs.
- **download_ci_artifact_bytes.py** and the unsigned download receipts preserve the byte-transfer method without retaining temporary signed credentials.

To reproduce the verification after moving this packet, use the explicit CLI arguments recorded in VERIFIER_EXECUTION_RECEIPT.json and replace their local path prefixes. The article argument must locate the complete frozen source and the preserved final local receipts. The reference-build and reference-source arguments identify evidence/current-execution/full-physical-source-release; the reference-history argument identifies the actual local 20261019T081533713628Z receipt. The latter supplies the required command/document contract; the verifier independently requires the ZIP's newly produced 20261019T092330252503Z execution and does not substitute the local receipt for it.

The standalone program's earlier regression and integrity-negative checks remain in the preceding verifier-preparation packet. They are separate from this new actual CI success.

This evidence establishes exact-source execution and artifact integrity. It does not close unrestricted whole-word pressure, the original collision-normalized shortage limit or the complete raw pointwise local limit/inverse theorem, and it does not represent an independent human specialist proof audit. Any later metadata-only publication commit must identify this tested C2 head separately and preserve the mathematical/source fingerprints unchanged.
