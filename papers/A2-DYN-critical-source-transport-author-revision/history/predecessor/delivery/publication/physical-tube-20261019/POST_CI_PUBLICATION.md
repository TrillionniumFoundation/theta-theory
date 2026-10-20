# Post-CI author publication receipt — 19 October 2026

This receipt accompanies the complete physical-tube source-height author revision. The manuscript and all frozen inputs are the ones actually tested below. The containing post-CI commit adds publication and execution evidence and uses the commit directive **[skip ci]**. It is not represented as the checkout of an additional CI run.

## Exact identities

| Role | Commit or tree |
| --- | --- |
| Preserved complete predecessor | 15ad3962de63f50911b765fe6608e722fe9b8c82 |
| Complete new source publication C1 | 706aa8d1bca33b0d6268806cca873d57511ad8d9 |
| C1 complete article tree | b0c173ad4f974576d0f639e18b77fe16fbab6ff6 |
| Actual tested publication carrier C2 | 8fbc6bd56bd9325600018f1aeb0cb2c2d0d8a4f2 |
| C2 root tree | f2c256f46be33875506ba45953dd7c037e7d5930 |
| C2 article tree | c1ddfd34dd2b79900c747c3a16e941835bc94025 |

The source manifest SHA-256 remains **a891751e40fd6bb41fec5bd099883f78a66e616aeb4a95496694f991d95cc069**, covering 1,408 inputs and 105,914,630 bytes. The mathematical source/tool fingerprint remains **fdfeab7b2dbb2febcf0b5a06ab47f2088e7b46a6a31b8e326fbaf2a7c76dca9d**. The dedicated workflow is unchanged.

## What was actually executed and downloaded

[Actions run 39187286448](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/39187286448) completed successfully at exactly C2. Job 117852268064 completed all eleven actual steps. Its current native source/math/typeset phase ran from 01:53:51 to 01:54:52 UTC, followed by the current historical rebuild from 01:54:52 to 01:55:18 UTC.

The actual downloaded artifact is [CI_ARTIFACT_12158866926.zip](current-ci/CI_ARTIFACT_12158866926.zip): 10,763,491 bytes, 200 files, SHA-256 **4b5c090e1a2ef608b48b08b4d0ffa648ffc34813243e597d4b85135464406406**. All archive files were read and hashed; the digest agrees with the GitHub artifact record.

The [independent artifact check](current-ci/CURRENT_CI_ARTIFACT_VERIFICATION.json) verifies all 98 native/tool inputs and all 1,408 frozen inputs against the actual C2 identities. It reads the 44 successful mathematical command receipts and their logs, all 35 actual normal/optimized output pairs, three actual native TeX passes, and the 164-page PDF. It separately selects the newly executed historical receipt at 20261019T015452772763Z: 390 historical source files, nine successful commands, and the 26/883-page PDFs. Four earlier historical execution receipts remain in the archive with their original success/failure status.

The exact job log contains 56,425 bytes, without an added terminal newline; its SHA-256 is **f7a2992ddc1579a9345b983099b252ddc1e8a8897bb01a7133ed397813e5f4b1**.

The local displayed PDF and the CI-built PDF retain distinct actual byte identities. Both contain 164 pages and arise from the same frozen source; their auxiliary-file SHA-256 agrees. The local PDF is not overwritten with the CI PDF or described as byte-identical to it.

## Complete remote source and isolation

The [C1 remote verification](remote-verification/C1_REMOTE_VERIFICATION.json) compares all 1,964 source-publication paths, modes, byte sizes and Git blob IDs with the exact transport inventory. It fetches all 60 distinct article subtrees nonrecursively and recomputes 68 canonical tree hashes, including the baseline and current control trees. There are no missing, extra or mismatched file identities.

Only the new article was added to the 211 existing paper subtrees; only its new dedicated workflow was added to the 173 existing workflows. All old sibling entries are unchanged. The complete earlier author source, reports, companion and unrelated papers remain preserved.

The saved before/after census confirms that all 423 pre-existing A2-DYN refs are unchanged. Exactly the three authorized new author, response and referee-copy refs were added. One unrelated General Theta ref moved during the observations; the receipt preserves that fact and makes no attribution for it. This author publication did not update that ref.

C2 changes only PUBLICATION_STATUS.json and eight new publication receipts relative to C1. The containing post-CI successor changes only publication/evidence receipts and status; all frozen mathematical inputs and the tested workflow retain their C2 identity.

## Reproduce the artifact checks

From the new article directory, with Python and Poppler pdfinfo installed:

~~~bash
a2dyn_packet=delivery/publication/physical-tube-20261019
a2dyn_check=$(mktemp -d)
python3 "$a2dyn_packet/current-ci/verify_current_ci_artifact.py" \
  --article . \
  --manifest SOURCE_MANIFEST.json \
  --expected-identities "$a2dyn_packet/current-ci/EXPECTED_C2_FILE_IDENTITIES.json" \
  --archive "$a2dyn_packet/current-ci/CI_ARTIFACT_12158866926.zip" \
  --observation "$a2dyn_packet/current-ci/FINAL_OBSERVATION.json" \
  --output-dir "$a2dyn_check/ci"
~~~

To repeat the saved-response tree and ref verification without replacing its historical execution receipt, copy this publication packet into a temporary directory and give that copy to the verifier:

~~~bash
cp -a "$a2dyn_packet" "$a2dyn_check/publication"
python3 "$a2dyn_check/publication/remote-verification/verify_c1_remote_publication.py" \
  --work-dir "$a2dyn_check/publication"
~~~

The packet includes the exact C1 transport inventory, baseline/control tree responses and initial branch census needed by that program. These checks verify source identities and execution records. They are not continuous mathematical proofs and do not represent independent human specialist certification.

## Scientific scope remains unchanged by publication

The full new native bodies 310–313 prove the fixed-guard physical source-height theorem, complete collision-normalized exceptional-source payment on that source, exact marked central comparison, the stated inverse-gradient volume estimate, explicit optical comparison, and guarded physical-word pressure. All inherited bodies remain intact.

The unrestricted raw pointwise local limit theorem and four-coordinate inversion are **not declared complete**. The original guard complement, shallow positive source and full comparison capacity, singular/paired charges, unrestricted pressure and uniform spectral/arithmetic/conditioning/inverse interfaces retain their precise stated obligations. Publication and CI do not alter that mathematical status.
