# Actual C2 CI verification

The dedicated push workflow completed successfully at exact author commit **8fbc6bd56bd9325600018f1aeb0cb2c2d0d8a4f2**. Its actual downloaded artifact, every archived file, command receipt and frozen-source identity have now been independently checked. This receipt belongs to C2 even if the publication refs later advance to a metadata-only successor.

## Actual GitHub execution

| Item | Verified value |
| --- | --- |
| Workflow | .github/workflows/a2-dyn-physical-tube-source-height-20261019.yml |
| Run | [39187286448](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/39187286448), push event, completed/success |
| Exact checkout | 8fbc6bd56bd9325600018f1aeb0cb2c2d0d8a4f2 |
| Article tree | c1ddfd34dd2b79900c747c3a16e941835bc94025 |
| Job | 117852268064, all eleven actual steps completed successfully |
| GitHub final update | 19 October 2026, 01:55:25 UTC |
| Native source/math/typeset phase | 01:53:51.746712–01:54:52.729395 UTC |
| Actual current historical rebuild | 01:54:52.772954–01:55:18.231728 UTC |
| Artifact | 12158866926, 10,763,491 bytes, 200 actual files |
| Artifact SHA-256 | 4b5c090e1a2ef608b48b08b4d0ffa648ffc34813243e597d4b85135464406406 |

The ZIP was actually downloaded through the purpose-built GitHub artifact tool's file reference. Its byte count and digest agree with GitHub's advertised values. All 200 files were read and individually hashed; ordinary ZIP CRC checking occurs during those complete reads. No program from the archive was executed by the independent verifier.

## Frozen source and actual commands

All **1,408 frozen inputs**, totaling **105,914,630 bytes**, match the C2 file identities by byte count, SHA-256 and Git blob SHA. The frozen manifest's SHA-256 is **a891751e40fd6bb41fec5bd099883f78a66e616aeb4a95496694f991d95cc069**.

The archive's complete list of **98 mathematical source/tool inputs** agrees exactly with C2. Its fingerprint was reconstructed independently from the canonical sorted JSON list and is **fdfeab7b2dbb2febcf0b5a06ab47f2088e7b46a6a31b8e326fbaf2a7c76dca9d**. The actual entrypoint hashes for build.sh, requirements.txt and the dedicated article workflow recipe also agree with C2.

The actual mathematical phase contains **44 distinct commands**, all with exit code zero. Each command's individual receipt agrees with the phase summary; every actual output byte count and SHA-256 matches its archived log. All **35 normal/optimized comparisons**, including standard output and applicable detail files, were checked by reading both files and comparing the actual bytes.

The source gate verifies all **54 active core proof bodies**, **64 reachable native TeX files**, and **90 original reports**, with no unresolved native reference. The actual runner used Python 3.11.17, mpmath 1.3.0, numpy 2.3.5, scipy 1.17.0, sympy 1.14.0 and TeX Live 2023/pdfTeX 1.40.25.

## Native and historical documents

The native build contains **three actual pdflatex passes** and one PDF inspection, with command-level output identities verified. The actual CI PDF has **164 pages**, 1,466,753 bytes, and SHA-256 **098f8222b00d63113b589981c7c6c42ab0b711d1c5b40c5c7dc520f75282c0d9**. Its auxiliary-file hash is **1e222d7e2946715796deafceec4ca742f855033b644a4eb86cd93566aef84bea**. No layout/reference problem is reported; the two retained AMS foreign-command advisories remain recorded.

The verifier explicitly selects the fresh historical receipt at **evidence/current-execution/historical-recovery/20261019T015452772763Z/REBUILD_RECEIPT.json**. It checks that this execution began after the current native phase and completed during this actual CI run. It verifies the receipt's **390 historical sources** and **nine actual successful commands**, then independently reads the generated PDFs:

- Historical main: **26 pages**, SHA-256 **f4834441635283fcbbdaa1c85b71a3a1076715fb34c6f5c0ce667b121c1bee6e**.
- Historical supplement: **883 pages**, SHA-256 **779d21e8673dde800a004959240e1d407cd028e34fdb47b713fc01ca7da2c92f**.

The archive retains four earlier historical receipts, including an earlier failure, in addition to the current one. They are listed separately and are not borrowed as evidence of the new execution. Actual post-run changes are confined to generated build PDFs/logs and current execution records inside the new article.

## Exact evidence and reproduction

The principal machine-readable result is **CURRENT_CI_ARTIFACT_VERIFICATION.json**. Its status is passed, and its actual_current_ci_success_verified field is true. The mathematical certification and independent-human-specialist fields remain false.

Other evidence retained in this directory includes the original ZIP, all actual observations, **FINAL_OBSERVATION.json**, **CURRENT_CI_ARTIFACT_FILE_MANIFEST.json**, **EXPECTED_C2_FILE_IDENTITIES.json**, the verification program, and **VERIFIER_EXECUTION_RECEIPT.json** with its actual captured output. The job log is saved as the exact UTF-8 text returned by the GitHub job-log tool: **56,425 bytes**, SHA-256 **f7a2992ddc1579a9345b983099b252ddc1e8a8897bb01a7133ed397813e5f4b1**. No final newline was added.

The verifier uses Python's standard library and the pdfinfo executable. It accepts explicit article, C2 identity, manifest, archive, observation and output paths. Keep CI_JOB_LOG_IDENTITY.json and its named job log beside the verifier, or preserve this entire evidence directory. For example, after setting the two paths to the actual checked-out article and copied evidence:

~~~bash
A2DYN_ARTICLE=/path/to/theta-theory/papers/A2-DYN-physical-tube-source-height-author-revision
A2DYN_CI_DIR=/path/to/copied/current-ci
python3 "$A2DYN_CI_DIR/verify_current_ci_artifact.py" \
  --article "$A2DYN_ARTICLE" \
  --expected-identities "$A2DYN_CI_DIR/EXPECTED_C2_FILE_IDENTITIES.json" \
  --manifest "$A2DYN_ARTICLE/SOURCE_MANIFEST.json" \
  --archive "$A2DYN_CI_DIR/CI_ARTIFACT_12158866926.zip" \
  --observation "$A2DYN_CI_DIR/FINAL_OBSERVATION.json" \
  --output-dir /tmp/a2dyn-ci-verification
~~~

The actual final verification execution completed at **02:02:20 UTC on 19 October 2026**, with exit code zero and empty standard error. The exact script and output hashes are in VERIFIER_EXECUTION_RECEIPT.json. The ZIP contents need not be flattened into duplicate article files: the verifier reads them in place.

These checks establish actual execution, artifact integrity, source identity and rebuild completeness. They do not prove the remaining continuous dynamical, singular-pairing, spectral, arithmetic, conditioned microscopic or inverse inputs, and do not constitute a referee endorsement.
