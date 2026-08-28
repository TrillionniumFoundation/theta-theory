# Round306 B1AF4 K2R231 — Round231 engineering authority receipt

## Verdict

`GO_R231_ENGINEERING_AUTHORITY_ONLY` / `NO-GO_FOR_CLAIM`.

The frozen Round231 producer and certificate are now independently receipt-backed at the byte, table, order, row, and bounded traversal levels.  This package closes **95,640 / 95,640** selected canonical-row SHA-256 commitments with **0 missing**:

- resolved descendants: 22,348;
- guard descendants: 0;
- depth-6 retained frontier: 67,924;
- root summaries: 5,368.

The independent replay reproduces the frozen census: 5,368 outgoing-seam roots, 22,348 resolved descendants, 67,924 depth-6 frontier rows, 2,220 roots fully released, and 44 distinct released exact-key ordinals.

## Frozen old artifact

- producer: `cm2_round231_source_g_outgoing_seam_depth6_materialization.py`, 12,984 bytes, SHA-256 `5afa1bc6fc6faec4c9b13be707c93714acdf5dbd09f2fafeefff07c445c517ad`;
- certificate: `cm2_round231_source_g_outgoing_seam_depth6_materialization_certificate.json`, 91,909,341 bytes, SHA-256 `7bc861ef4f2c2962dcf7c8e38839af2ec12477f9fc42d808be1b48d858745374`;
- certificate result SHA-256: `83381b3ba9bd22e1616f3b77006113b88486e13ad81e3c9745cb89fd7798f06a`.

The old producer was not changed.  Its own `lstat()` then path-read pattern is not a held-FD security proof, its JSON loader does not independently reject duplicate keys/nonintegral numbers, and it had no independent verifier/receipt/manifest.  The new verifier compensates for the frozen artifact by opening every selected authority input through a directory FD, enforcing regular single-link files, comparing pre-open/path/held-FD identity, hashing every FD twice, loading the frozen engine modules from those held bytes, and revalidating every final FD against its path and SHA.

## Independent replay boundary

The Round231 producer is never imported or executed.  The Round231 root selection and depth-6 traversal are independently implemented here.  The frozen Round174/Round179 arithmetic and classification engines are, however, shared upstream authorities and are loaded from held FDs.  Therefore this is an engineering/row-authority replay, **not** an independent proof of the upstream mathematical semantics.

The package binds 26 input pins totaling 699,167,195 bytes.  Each result is bound to the complete canonical input-pin commitment, the old certificate result, all four ordered table commitments, and every full canonical output row.

## Security and determinism

- two-pass held-FD pins: 26 / 26;
- final FD/path/SHA revalidations: 26 / 26;
- duplicate JSON keys, floats, NaN, bool/int aliases, symlinks, hardlinks, TOCTOU replacement, and coherent final-canonical-row >8 MiB mutations: rejected;
- main replay spills: 0; main replay does not consult `TMPDIR`;
- explicit attack temporary directory remains outside `deliverables` even under adversarial `TMPDIR`;
- seed 17 and seed 93 no-write replays produced the same result SHA-256 `672bd85e4313b5cbfea0173eeb2676bfbb2011e39a8833cbd8b539a1c8717d00`;
- all package bytes plus dev/inode/size/mtime/ctime/SHA snapshots were unchanged across both no-write replays.

## Credit that may and may not move

May move from blocked to ready:

- R231 frozen byte authority;
- R231 four-table row/order authority;
- R231 per-row SHA closure (95,640 closed, 0 missing);
- R231 bounded depth-6 engineering replay authority.

Must remain zero:

- full-support equality and normalized full support;
- physical incidence/equivalence and known-block attachment;
- representation pullback;
- B1A candidate/certificate credit;
- B2 transition/pair-routing credit;
- maximality, D02/D03/D04, Gate5 global block, and CM2 credit.

In particular, a local positive-volume occurrence row and an exact-key ordinal do not by themselves prove physical-component incidence, global exact-key disposition, or normalized support.
