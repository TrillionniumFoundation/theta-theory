# Final observed native-build status — A2 v28

This supplements [VERIFICATION_V28.md](VERIFICATION_V28.md) after publication of the response and diagnostic fixture. It does not change any mathematical source or close C2.

The response/evidence commit `c6827750cc595d058a1786aa818a57d52266cfdc` triggered a second native workflow run because the separately labelled fixture is a new TeX file. The live job response was inspected. As in the first attempt, no step executed.

| Attempt | Source commit | Run | Job | Completion (UTC) |
|---|---|---|---|---|
| Mathematical revision | `6d8f158c60f3636c572daa64779f57c9c9ec757b` | `34677164341` | `103508962672` | `2026-09-12T06:03:58Z` |
| Response and evidence | `c6827750cc595d058a1786aa818a57d52266cfdc` | `34677568860` | `103510063039` | `2026-09-12T06:13:29Z` |

Both returned `status=completed`, `conclusion=failure`, `steps=[]`, `runner_id=0`, and an empty runner name. Neither ran checkout, source audit, diagnostics, or TeX. Neither supplies native PDFs or a full reference certificate. No underlying account or scheduling cause has been established.

The actual Git comparison from review head `e5a153b1bbb663c4a5e3153c6a7bdedb7fcd5864` to `c6827750cc595d058a1786aa818a57d52266cfdc` reported two commits ahead, zero behind, 21 changed paths and no removed files. Only the two current README pages and the current main entry modify existing paths; new mathematical modules, archives, response records, diagnostics and the workflow are additions. The read-back changed-source audit script blob is `38be6604feec3ad3ef4c4876f4351ed82970a5e8`, matching the executed local bytes.

The complete mathematical source remains the immutable revision listed in [ACTIVE_SOURCE_MANIFEST_V28.md](ACTIVE_SOURCE_MANIFEST_V28.md). C1 has a supplied definition and proof for re-review. C2 remains an unfulfilled complete-native execution requirement, not a failed mathematical theorem and not a successful build inferred from a fixture. This final status update contains no TeX or workflow change.
