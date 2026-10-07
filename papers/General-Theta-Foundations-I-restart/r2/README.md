# General Theta Foundations I — restart r2

**Acquired Geometry and Causal Resource Transfer**. New native revision responding to the 7 October 2026 r1 external mathematical assessment. This directory is a revision of restart r1, not a copy or renumbering of v96.

## Entry points

- `main.tex` and `sections/`: complete mathematical manuscript, definitions, proofs, three raw-kernel realizations and algorithm appendix.
- `paper.pdf`: rendered artifact after successful publication.
- `REFEREE_RESPONSE.md`: point-by-point response with theorem labels and residual responsibilities.
- `PROOF_LEDGER.md`, `THEOREM_MAP.md`, `ASSUMPTION_MATRIX.md`, `COUNTEREXAMPLE_LEDGER.md`, `RESOURCE_ACCOUNTING.md`, `PIPELINE_DERIVATION.md`: proof and resource audit.
- `NOTATION_AUDIT.md`, `LITERATURE_COMPARISON.md`, `SCOPE_AUDIT.md`, `HISTORY_COVERAGE.md`, `PAGE_INSPECTION.md`: interpretive, provenance and visual audits.
- `SOURCE_MANIFEST.json`, `PUBLICATION_POLICY.json`, `build.py`, `verify.py`: reproducible source/build contract.
- `evidence/BUILD_RECEIPT.json` and `evidence/REGRESSION.json`: exact native-source binding and artifact hashes. The final read-only receipt is a separate Actions artifact bound to the artifact commit; it is intentionally not committed back into the head it verifies.

## Mathematical additions

The central acquired-geometry theorem now has a structural marked-kernel alternative: a one-step positive-operator Lyapunov condition produces the forced first and second moments through two resolvents. Recurrent active expansion is allowed. Independent exact suspension leaves the forced profiles unchanged. A mandatory-continuation cut proves a growing total-state lower bound; one explicit robust experiment simultaneously realizes acquisition, anisotropic memory resolution, calibration ambiguity, compulsory numerical information loss and optimal erasure deficiency.

These are theorem statements with proofs, not claims of independent validation or journal acceptance. The full ledger is kept in risk notation, but the minimax program/time/workspace conclusion is on a proved feasible region, not a universal complexity lower bound. The open responsibilities are recorded in `SCOPE_AUDIT.md`.

## Immutable inputs

Canonical restart: `18000b21e4bfd89180ccb069e46ac0f21621f34d`. Reviewed r1 paper: `589372183966bef1b40ae223b0ab468cb6419182`. Referee branch snapshot: `4454ad669ebdbccb93d10d828484600dce58845d`. Historical references remain independent. This release changes only the new r2 directory and its uniquely named workflows; it does not move the canonical, review, realization or archive references.

## Local reconstruction

```sh
python3 build.py --audit-only
python3 build.py --out /tmp/gtf-r2-build
```

In an exact Git checkout supply `--source-sha <40-character-native-source-SHA>`. To verify the artifact-only child, use `--verify-published` with the same source SHA and no retained Git HTTP credential. Ordinary and optimized regressions must agree. Finite tests are regression evidence, never proofs of continuum assertions.
