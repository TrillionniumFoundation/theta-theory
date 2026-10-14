# A2-DYN revision 109 — endpoint traces and physical grazing payment

Current packet: `papers/A2-DYN-v109-referee-response`.

Read `main.tex`, `RESPONSE_TO_REFEREE.md`, `PROOF_LEDGER.md` and `VALIDATION.md` in that order. The current article is a standalone, 12-page native-LaTeX exposition. The entire prior packet, all 259 old modules and the old article and supplement are preserved exactly under `archive/v108`; two new modules contain the optical trace derivation and quantitative grazing-capacity payment.

## Frozen sources

- Controlling review: `review/a2-dyn-v108-canonical-capacity-external-top4-review-2026-10-14`, commit `e863e8c110ffee472b3d10163a129a2bcfe9c0e1`.
- Report: `reviews/a2-dyn-v108-canonical-capacity-external-top4-review-2026-10-14/REFEREE_REPORT.md`, blob `5080564a78a192984acc272bc31c7ef8165bda4e`.
- Reviewed author commit: `2144665f89362ca80116f1999d99c80875833dcf`.
- Original and archived author packet tree: `e66a1dec484f419d88c05f12a7e2ec5310430448`.
- Revision-109 manuscript tree: `99e677d4a40f087fc21a2c050e1cc4f43e3ef155`.

## Revision branches

`revision/a2-dyn-v109-capacity-abundance-referee-response-2026-10-14`

`revision/a2-dyn-v109-capacity-abundance-referee-copy-2026-10-14`

Both are intended to carry the same manuscript commit. The branch name identifies the referee task; it does not claim that complete capacity abundance has already been proved.

## Mathematical advance

The new article proves actual optical denominator and marked-incidence bounds, a continuous Schur-complement extension, integrability of the inverse gradient along original Gauss-coordinate segments, and finite endpoint traces. An actually visited grazing collision gives zero original paired minimum; an unvisited disk tangency need not. The full comparison capacity of the visited-grazing class is paid by the original uncut volume. At explicit outer scales,

`0 <= R_B^ng - R_B^full <= K_B P_rB^gr`,

`H_M(R_B^ng - R_B^full) <= C_M B^(-95/384)`.

The original raw pointwise target, labels, weights, section and limit order remain unchanged. The nongrazing microscopic shortage must still be controlled; no finite-count exhaustion or finite diagnostic is represented as a proof of its collision-uniform decay.

## Qualification

Workflow: `.github/workflows/a2-dyn-v109-source-and-manuscript.yml`. It verifies exact source preservation, runs normal/optimized checks, compiles current and historical documents, and checks recorder coverage of all 261 modules. Local current-article checks are in `provenance/local-validation.json`; exact-SHA remote success is recorded only by an actual completed workflow, never inferred from its definition. The initial source-freeze commit `2fa6dbc6e5a7d6677996a3e557975800245617db` is not the theorem-bearing manuscript commit.
