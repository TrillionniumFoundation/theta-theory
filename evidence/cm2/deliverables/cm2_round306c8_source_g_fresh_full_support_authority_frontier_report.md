# Round306C8 Fresh Full-Support Authority Frontier Report

## Verdict

- Status: `PASS_INDEPENDENT_FRESH_C6_C7_AUTHORITY_FRONTIER_REPLAY__ZERO_SUPPORT_CREDIT`.
- C6 and C7 are the exclusive fresh identity/component/routing authorities.
- The sealed C2 frontier and C3 relational census are pinned as historical objects and explicitly non-authoritative after C6.
- Formal normalized-support, B1A, B2, maximality, and CM2 credit remains `0`.

## Frozen Frontier

- Legacy transitive closure: `143` files / `3,201,364,049` bytes.
- Construction authorities: `45`; table/path/order commitments: `82`.
- Fresh partition: `497,772` members / `334,604` roots / `61,928` components.
- Fresh cross-component denominator: `123,410,984,634`.
- Families: PRESERVED `126,468`; NON_GRAPH `51,172`; R2 `295,336`; R292 `9,404`; G2A `5,264`; G2B `10,128`.
- Fresh representations: `545,184`; physical relations and open physical gaps: `15,392` each.
- The `33,344` surviving sides of empty graphs are reclassified into NON_GRAPH.

## Authority Boundary

- Authority order is C6 fresh DSU/component rows, then C7 identity/representation/routing rows, then surviving legacy construction geometry.
- C2 and C3 component-bound products cannot be reused as current authority.
- Historical theorem-obligation counts `824,864`, `824,800`, and `824,832` are not current denominators.
- The exact current theorem-obligation census must be rebuilt from fresh six-family support and is not a feature-ledger row count.
- All `15,392` physical-incidence, pullback, and one-sided-trace obligations remain open.

## Determinism And Verification

- Producer SHA256: `432b4e847c3d417938c8676d53bbd1b1a6f564d1977bfaab84844dabeb665535`.
- Hash seed `308011`: `1m03.57s`, peak RSS `22,032 KiB`.
- Hash seed `308099`: `1m03.81s`, peak RSS `21,508 KiB`.
- Both candidates are byte-identical; candidate SHA256 `1ec052ba9a6c26929d3a8242f3d12f405640f6399c331977acf51a315e201792`.
- Independent verifier SHA256: `dc78545cc1bd7e68717abba6b185cd4b7537f2b57d32aa1b4616fcfbb6cd931e`; it does not import or execute the producer.
- Verification-last: `1m00.72s`, peak RSS `23,296 KiB`.
- Coherent attacks: `20/20` rejected in `2m02.06s`, peak RSS `23,352 KiB`; attack object self-SHA256 `56e9ee91e7b75106c7d7addb1a7be586d4d920acc8fbca7b7480cd090d6d01ff`.
- Cold replay: `1m01.74s`, peak RSS `23,300 KiB`, deliverables writes `0`.
- Verification object self-SHA256: `b2d38b63cd614815f52f27f69b25885c1b5099573431628f970e50e7e86662e1`.

## Next Gate

- Prove all `15,392` physical incidences relation-by-relation and construct their pullback and one-sided-trace certificates.
- Rebuild preserved/NON_GRAPH kernels at the new `51,172` NON_GRAPH denominator, then close the R2/R292 semantic kernels.
- Only after those closures may a `497,772`-member typed full-support ledger and a new B1A/B2 be issued.
