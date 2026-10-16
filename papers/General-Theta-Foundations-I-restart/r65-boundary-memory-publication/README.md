# R65 — source-bound author revision and independent review entry

The complete current source is in `../r65-boundary-memory/`. Start with its `main.tex`, the paired `supplement.tex`, and `RESPONSE_TO_REFEREE.md`. The full R64 report is copied unchanged here as `R64_REFEREE_REPORT.md`, Git blob `370ad771cf2e2482beefac866445bd384a161911`, from report commit `0a66ca2ede7835ede2a62fe2363ba5dd3ccd2ed8`. It reviews R64, not this revision; it is not represented as commissioned human or editorial approval.

## Exact source identity

Mathematical source commit: `0469eb4f852eeea953cb3725d4b34dfdd2bf9d36`.
Repository source tree: `a3a633e156cdbfddc8aafa4a03c8245689e56a9e`.
Complete current paper tree: `3a0ea744d1e4721f2c47b5e038023becd4da2ce0`.
Parent R64 delivery: `6ec637d01349ff4525fdc064ab00489442798aaf`.

The enclosing delivery commit adds only this publication directory; it does not change the verified paper subtree. This separation avoids a receipt referring to its own future commit SHA. The complete R64 source remains byte-preserved as `retained/r64-native/`, tree `2fb9a4d5c12c65bab080e3a5b29b397d34823098`. No previous author folder, review branch or other paper is overwritten.

## Current mathematical packet

The native main article is 34 pages and contains the performed-law/optimality core, the new exact boundary-memory criterion and quantum control results, the delayed-release theorem, and the actual-history geometric transfer proof. The current technical supplement is 67 pages and contains all displaced technical proofs plus the complete previous supplement body. The separate retained R58 companion is 37 pages. The main and current supplement use resolved cross-document theorem references; keep their generated PDFs together.

The original title remains **General Theta Foundations I: Acquired Geometry and Causal Resource Transfer**, with the Annals / Acta / Inventiones / JAMS research objective. The new contributions concern exact stochastic boundary memory, the residual decision quotient, positive finite realizations and obstructions, an all-angle noisy-qubit two-label optimum, and rational precision synthesis. Their scopes and unresolved wider questions are stated in the article and response.

## Actually executed verification

After creating the source commit, the complete paper directory was rehashed using Git blob/tree encoding and rebuilt against that source identity. All five diagnostic generations were run normally and with `python -O`, with byte-identical outputs. The run passed 10,190 finite checks: 7,956 exact and 2,234 floating. It verified 1,748 source files and 111 labelled statement entries. All three documents passed three native LaTeX passes. A repeated full build reproduced all three PDFs byte-for-byte. Exact output hashes and the full execution-receipt hash are in `LOCAL_BUILD_RECEIPT.json`.

The local source directory was an export, not a Git checkout; the recorded source identity is its complete recomputed Git tree, matched to the remote commit's paper subtree. The build validates the immutable R64 review reference, not a local review-body copy. This remote publication directory separately retains the original full report by Git object identity.

For an independent rebuild in a checkout, install the pinned requirements and native LaTeX dependencies, then run from the paper directory:

```sh
python3 verify.py --out /tmp/theta-r65-independent --source-commit "$(git rev-parse HEAD)"
```

The isolated read-only GitHub workflow verifies its actual checkout SHA and uploads the source, PDFs, diagnostic data, native logs and publication files. A queued, absent or failed run is not a passed hosted verification. No R59/R64 success is attributed to R65. The downloadable review package additionally includes the historical exported text corpus and its scan records. Finite diagnostics and compilation do not constitute formal proof, exhaustive priority certification, independent human endorsement or a journal decision.
