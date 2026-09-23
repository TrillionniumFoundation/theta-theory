# A2 revision 143 — finite failure schemes and quadratic pencils

**Finite failure schemes and the reconstruction of quadratic pencils** — Qian Qi — 24 September 2026.

The principal article is `geometry.tex` / `geometry.pdf`. The technical supplement is `supplement.tex` / `supplement.pdf`. `complete.tex` / `complete.pdf` contains both proof networks. All are native LaTeX, not wrappers around an unavailable manuscript.

## The exact review object

The controlling report is **the second v141 report**, `reviews/a2-v141-independent-harsh-top4-r2-2026-09-24/REFEREE_REPORT.md`, at commit `3afecca5e65d7fe9c6784020ea6e813122938140`. It reviews the substantive v141 manuscript at `8cd389f4048a1047be9aa8e8e4f642595175a555`, not the earlier restoration-only state. Revision 143 also preserves the later mathematical development in v142 at `4deb7a35f4488a0c8b686261569ce4ef324ca750`.

The authoritative source SHA and PDF hashes are in **SOURCE_LOCK_V143.json** and **evidence/BUILD_RECEIPT_V143.json**. The root CURRENT_REVIEW_ENTRY.md points to this directory. A future mathematical change requires a new revision branch: the exact source commit, not a moving branch label, defines the referee object. Old issue matrices and receipts describe their own versions only; the active ISSUE_MATRIX.json is revision 143 and names the second v141 report.

## Mathematical revision

The main theorem is uniform intrinsic reconstruction from the unmarked order-d failure neighbourhood, d=n^2+2n-4. The article follows its proof through oriented rank-one geometry, coefficient extraction, natural pencil reconstruction, the sharp finite-order result, universal relative neighbourhoods, and spectral readout. The classical Segre closure order is credited as classical.

The new section `parts/26-critical-correspondence-v143.tex` identifies the reciprocal score zero scheme reconstructed by the finite invariant. It then constructs data by spectral projectors, without choosing an eigenbasis, and identifies a relative critical algebra as B[t]/(F/a). It proves finite etaleness of rank 2r-3 on a specified algebraic spectral open, with a completely real semialgebraic chamber and globally labelled analytic critical sections. It checks the omitted x=0 chart scheme-theoretically and allows arbitrary base change on that open. The real definite realization is explicitly an additional input.

The complete web/contraction, Casimir/singular-value, K3, polar and boundary developments are retained in the supplement, with their statements and proofs unchanged. The new operator dictionary compares the precise restricted map with classical angular differentiation and the Casimir operator. It does not claim exhaustive historical priority. The pencil proof does not depend on the web contraction theorem.

## Preservation and verification

All inherited part files and check files remain byte-identical. The complete predecessor source is archived in history/v142. The active complete compilation must retain every inherited labelled result, every theorem/lemma/proposition/corollary/proof block, and every numbered equation/align/gather block. The verification script checks these requirements rather than treating an inactive archive as sufficient preservation.

Run `bash build.sh` with Python, SymPy, NumPy, PyMuPDF and TeX Live. Nineteen scripts run, followed by native principal/supplement/complete builds and source/layout checks. An isolated local copy must set A2_PREDECESSOR_DIR to the pinned v142 directory. The source-bound remote receipt records the actual source SHA, run ID, output hashes, page counts, all check results and remaining documentary items. A local-preflight receipt is not a remote success.

Read RESPONSE_TO_REFEREES_V141_R2_V143.md, LITERATURE_AUDIT_V143.md and REFEREE_GUIDE_V143.md before re-review. **The complete Ballico 1993 article has not been obtained; its six-axis theorem-level comparison remains open. Exhaustive historical priority is not certified.** No theorem has been weakened because of that documentary limitation, and computational checks are not formal proof or editorial acceptance.
