# General Theta Foundations I — restart R9

**Acquired Geometry and Causal Resource Transfer** — Qian Qi.

This is a new foundations revision responding to the R7 external report. The canonical start remains `18000b21e4bfd89180ccb069e46ac0f21621f34d`. The pre-existing unreviewed R8 source at `3c9b212f8673c95e3a28fd83811b8a4f3bacc431` is credited and preserved, not relabeled as newly discovered work.

## Manuscript and submitted supplement
`main.tex` is the complete native article. Its principal theorem is `thm:serial`: the online resource exponent is the largest acquired continuation exponent across all cuts under explicit raw-verifiable recursion, global covering and positive-mass observability certificates. Checkpoint and online excess match exactly when that largest exponent equals the terminal exponent. The finite horizon, fixed physical exploration and candidate-domain assumptions are part of the theorem.

`thm:ranknoisy` derives all-cut certificates and a rank-sensitive noisy law; `thm:singularserial` proves a singular-acquisition law with a potentially geometry-expanding terminal query. All R8 substantive sections remain active, including two-sided/conditional cuts, a sequential-chart construction, the full-rank noisy model, acquisition, Gaussian filtering, stopping and morphisms.

Supplement S is part of this same submission, not an external publication. `build.py` supplies its complete retained technical text with a cover explaining its status. No theorem is justified by an unpublished, unavailable self-citation.

## Reproduction
Run `python3 refresh_manifest.py` only while authoring. It is not a build step.
Run `python3 verify.py` and then:
```
python3 build.py --source-sha <immutable-source-commit> --expected-tree <native-source-tree> --output <outside-source-output-dir> --receipt <outside-source-receipt.json>
```
The builder never regenerates the source manifest. It runs ordinary and optimized regressions, checks active inputs, builds the native article twice in isolated copies, rebuilds the complete pinned supplement twice, and verifies unchanged source bytes. The mathematical proofs, not the test counts, establish continuum claims.

The final source, artifact and read-only verification SHAs are recorded under `evidence/` after the corresponding operations actually succeed. This document does not predeclare success or journal acceptance.
