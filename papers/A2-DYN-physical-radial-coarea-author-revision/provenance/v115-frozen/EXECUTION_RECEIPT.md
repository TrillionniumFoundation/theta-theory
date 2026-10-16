# A2-DYN v115 local native build and evidence receipt

This receipt records *completed local operations* only. It is not an external mathematical proof certificate or a completed remote GitHub Actions result.

- Parent scientific author source: v114 full-delivery commit `8a5a7c2be5630bf5919e9f74ee79de01af0dbb85`, article Git tree `c2e9e83f39985a34690300433f4b40de4f1f88ac`.
- Latest controlling substantive mathematical report: A2-DYN v112, commit `d7fd0b24314d7341f9a611130bb650371d2d5ef2`. The v113 submission-state report is scoped to its workflow-only branch.
- Proof-bearing new module: `core/276_exact_two_mark_clearance_flux.tex` (exact physical double-mark coarea and quadratic bound); unchanged inherited numbered modules 260–275 preserved in both active paper and frozen v114 snapshot.
- Actual script execution: `bash build.sh checks1`, `bash build.sh checks2`, `bash build.sh typeset`, and `bash build.sh finalize` all succeeded, in that dependency order. The monolithic `bash build.sh all` had previously been interrupted by the calling environment's process-time limit and is **not** reported as a completed monolithic invocation. The split phases run the identical fail-closed checks and final receipt gate, not a reduced test suite.
- Source checks: 43 active Git blob identities, 205 frozen v114 files, 48 v112 preserved files, 16 inherited active proof module blobs, 3 original model/interface files and 19 prior clearance-flux files verified.
- New finite checks: 1,296 exact/angular root-Jacobian cases, 18 coarea comparisons (131072 angular sample points each), and 3,000 actual next-collision Lorentz rays (76 clearance witnesses and 1 two-mark ray in the finite sample). Seven other original check scripts also passed. All 8 programs produced byte-identical normal and optimized output.
- TeX engine: pdfTeX TeX Live 2025/dev. Frozen v112 paper compiled three passes to **31 pages**; v115 compiled three passes to **51 pages**. In both finalized logs, unresolved references = 0, multiply-defined labels = 0, overfull boxes = 0.
- Actual final manuscript: `manuscript/A2-DYN-v115-double-clearance.pdf`, SHA256 `5a3754443e1f79574614da52abcad19175a17cd1c8cdbf8839a17ca1402ef923`.
- All exact local pass logs/check summaries and final JSON: `evidence/v115-local-execution-record.zip`, SHA256 `b7ae132f12bce602cc5a8c02ed1a6df6f310d10c64cf48a0ecb46d2f1b6da9c6`.
- Remote CI for v115: **not yet completed** at local freeze. Independent reconstruction of historical uniform pressure/pairing remains outstanding. The full m²-normalized raw pointwise theorem and inversion still **unproved**.
