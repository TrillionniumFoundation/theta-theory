# R71 author revision — controlled proof clarification

This is an author-side revision on a fresh branch, not an independent referee assessment or a journal decision. The publication identity remains **General Theta Foundations I: Acquired Geometry and Causal Resource Transfer**, with the Annals / Acta / Inventiones / JAMS research goal unchanged.

## Fixed scientific baseline

- Complete parent author submission: `referee-ready/general-theta-restart-r70-leakage-memory-2026-10-16`, branch head `8e64bc7ac7af8f6e66989da331f2ba3b3340ce53`.
- Parent `main.tex` Git blob: `e01e1658077b1588f14b4beeb30ae80d12846dbc`.
- Parent current mathematical section `sections/29-leakage-memory.tex` Git blob: `3c6243247591a359dd0d024642b33134894a54fb`.
- Parent native manifest Git blob: `31a5951554efcb2191f9449fdfe0c6e2039a1983`; this manifest seals the *R70* source, and is not claimed to seal this changed R71 overlay.
- Last identified applicable deposited report is R65, review commit `358481b21ceeeedb1205ebd30f86982e32a2cb04`, report blob `d1ff9c5662390156ee212c82b173e86a21180e84`. The report examines R65 SHA `ee79ca9114f8009d62c056d07381b766645e3fc4`, not R70 or R71.
- Parent R69 is preserved as `retained/r69-native/`, with the older archive beneath it. No historical paper or review was deleted.

## Exactly what changed

The mathematical body has been **continued, not replaced**. Two narrowly scoped proof clarifications were made in the inherited R70 section:

1. In `lem:r70-core` the assertion that the initial label is active is now explicitly proved from the existential quantifier `u_n>0` for some `n`, even if `u_0=0`.
2. In `thm:r70-leakage` the nonzero complex exponential coefficients are justified from the named strict parameter assumptions; the phase factor cannot vanish, including with an initial-output zero.

Neither clarification is a new theorem, generalization beyond the proven hypotheses or solution of the controlling referee's broad contribution concerns. The proofs and claims of the predecessor remain inherited and retain their original hypotheses. The other paper folders and review objects are untouched.

## Verification boundary

The remote GitHub file update and read-back identify the changed section. No native LaTeX compilation, whole-source manifest reseal, independent proof formalization, or R71-matching hosted CI success has been established by this commit. A new R71 source manifest and publication receipt would require reconstructing and verifying the entire source tree; the original R70 manifest must not be relabeled as an R71 certificate.

Remaining mathematical blockers include unrestricted multi-command boundary optimality, a matched general-M squared-sign risk law, sharp background-dependent memory lower rates, and matching algorithmic resource bounds. The R70 response to sections 17–18 of R65 is preserved in `RESPONSE_TO_REFEREE.md` and is not represented as a new external report.

## Referee reading path

Read `main.tex`, `supplement.tex`, the revised `sections/29-leakage-memory.tex`, `RESPONSE_TO_REFEREE.md`, `PROOF_AUDIT.md`, `THEOREM_MAP.md`, `PRESERVATION_MAP.md`, `SOURCE_MANIFEST.json` (R70 predecessor only), and this explicit R71 status. The changed proof remains in the main manuscript's existing input graph.
