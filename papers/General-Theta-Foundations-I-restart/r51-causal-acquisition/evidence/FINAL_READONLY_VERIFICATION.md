# Final read-only validation — General Theta restart R51

## Immutable binding

- Canonical: `18000b21e4bfd89180ccb069e46ac0f21621f34d`.
- Latest external review: `65bd07d89b04274c587d2ae4100511d99c39b0f2` (R32).
- Ordinary mathematical source: `289a1189c45b7f5921c82f43e33abd740545b7d2`.
- Artifact commit: `a0378a01239c46995844f0cd09c31129cdc18b81`; its sole parent is the ordinary source above.
- Ordinary source projection: `ccbbc355d722a71ed970cef92a825bf3e2a06e49`.
- Hosted execution: GitHub Actions run `38352013426`, publication job `115146304180`, successful.

The final audit is this evidence-only commit together with the subsequent Git-object and ref readback. Its SHA is identified by the containing Git commit, rather than self-embedded in a file. No mathematical source or PDF is changed in this final step. The separate delivered `FINAL_REMOTE_READBACK.json` records the resulting final SHA.

## Reconstruction actually performed

Four actual hosted artifact archives were downloaded through the GitHub connection. Their bytes were checked against the archive digests, all publication-receipt hashes, prepared-source binding and remote Git blob identities. All **10,599 prior Git tree entries** remain identical. All **41 native inputs** (38 ordinary files, manifest and two immutable review inputs) match the remote Git blobs; four canonical controls match their pins.

The independent rebuild used a new directory and the ordinary source SHA above. All **1,147 input files** were hashed before and after the full operation and remain identical. Each environment ran **58 isolated PDF builds**, three compilation passes each, including the complete retained chain. Delivery comprises **24 PDFs / 616 pages**, including the new 20-page article. This is the R51 plus complete retained R49 chain, not every paper in the repository.

Native source audit: **38 ordinary files plus manifest; 14 active TeX inputs; 61 labels; 71 cross-references; 13 bibliography entries; 17 formal statements**. Native regression: **20,746 finite checks** plus the rational Gaussian arithmetic certificate, with byte-identical normal and `python -O` output. The complete inherited regression chain also passed; nested historical counts are not summed as independent tests.

No undefined references or overfull boxes were found. Within each environment, repeated builds are byte-identical. Hosted TeX Live 2023 and independent TeX Live 2025/dev PDF bytes differ, while every page count and every normalized text under the same extraction engine agrees. One historical `Companion_B` cross-environment text-extraction receipt hash initially differed. That failure is preserved as `FIRST_COMPARISON.json`; both actual PDF files were then re-extracted with common Poppler 25.06.0 and independently with common MuPDF, and all 24 pairs agree under both engines. Original hosted and independent receipts remain unmodified; the unrecorded hosted Poppler version is not guessed. **All 616 pages are pixel-identical at 97.2 dpi in MuPDF 1.26.7**. No text word bounding box escapes its page. The final native article was visually inspected on all 20 pages; rendering retained pages does not mean every historical proof was reread.

## Failure evidence and scope

The first local layout preflight found a 167-point overfull introduction chain. Its stdout/log is retained in the delivered failure-evidence directory. The chain was reflowed without deleting mathematics; final native and complete builds pass. A preflight artifact-name collision was prevented by separate `Companion_AcquiredRisk` and `Companion_ExactBudget` names and explicit collision checks. Neither issue is presented as mathematical progress.

Full independent input hashes, page render hashes and both build receipts accompany the delivered bundle; their hashes are recorded in `INDEPENDENT_REBUILD.json`. Arithmetic certificates, source audits, builds, retention and render agreement do **not** prove continuous-parameter theorems, establish priority, or decide top-four significance. See `../PROOF_AUDIT.md`, `../LITERATURE_COMPARISON.md`, `../SCOPE_AUDIT.md` and `../HISTORY_COVERAGE.md` for the mathematical and coverage boundaries.
