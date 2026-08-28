# C65s18 depth-18 64-shard preexecution report v2

Status: `PASS_PREEXECUTION_ONLY__AWAITING_SECOND_INDEPENDENT_REVIEW__ZERO_OF_64_SHARDS_EXECUTED`

## Frozen input and assignment

- C61 v4 residual input: exactly 20,879 closed `COLLISION2_HANDOFF`
  rows; every continuation has `next_collision_index=2`.
- Assignment domain:
  `cm2.round306c65s18.depth18-64shard.v2.assignment`.
- The canonical UTF-8 JSON preimage binds the exact C61 aggregate leaf row
  SHA-256 and its exact 21-bit path; SHA-256 modulo 64 selects the shard.
- The inventory is a byte-exact bijection with the frozen C61 filtered source
  order.  All 64 shards are nonempty: 295 through 379 inputs per shard; shard 0
  has 330 inputs.
- Assignment result object:
  `c7671985713c8cfd8a496931f1b2686fa545448ce0a434c89e943b178000407f`.

## Authorization and executor

- Independent zero-credit assignment seal object:
  `d1b508a54553b8944b50e926e895b35a589fe6aca3a03440e416571b339ca228`.
- Final executor SHA-256:
  `fdb3e4eea8f0e45f5a332e3d153109663f9e31d1661e16c63fd27d6736d582ba`.
- Every shard invocation hard-pins the contract, builder, assignment result,
  inventory, sealer, and authorization seal; it replays the full 20,879-row
  source/inventory bijection before selecting its local assignment rows.
- Shard ledgers and receipts use explicit v2 filenames and dirfd-relative
  `O_CREAT|O_EXCL|O_NOFOLLOW`, followed by file fsync, fd/path identity checks,
  byte or gzip replay, and directory fsync.
- No partial shard is an aggregate.  Partial statistics, assignment credit,
  formal credit, whole-parent credit, and D02 gate credit are all zero.

## Independent preexecution audit

- The builder, sealer, and executor were consumed as pinned inert bytes and AST
  only; they were neither imported nor executed by the verifier.
- Independent verification object:
  `93ebc2e2c30ccb06cae5f300c904e9ddcd37316ff5a0ede90dfbeb966c4413bf`.
- Atomic/race/symlink/hardlink/schema/invariant self-test: 53/53 PASS; object:
  `14f7c7bebe3653cf50da9686355a0e04ed9c55c7775d6cdb4676932834054b23`.
- The final execution count remains 0/64.  Shard 0 is not authorized until a
  second independent reviewer returns PASS on this exact manifest.

## Superseded evidence

The v1 execution package, intermediate v2 package, and pre-final v2 verifier
output are each explicitly rejected by companion markers.  They were never
used to execute a shard and are excluded from this manifest except for their
rejection markers.
