# C65s18 depth-18 shard 00 independent cold-audit report v2

Status: `PASS_EXACT_SHARD00_COLD_REPLAY_AND_30_OF_30_ATTACKS__ONE_OF_64_ONLY__ZERO_CREDIT`

## Frozen execution result

The exact v3 executor source is frozen at
`170df261ed9451fc3ecc1fca5e686c6f6d8eeb3d643126da09f30c634cda22ef`.
It consumed the preexecution chain frozen by manifest
`8882eb9b9eda1b1bb4c1e065c4c1d25b45de15b42af79804594c9e0887511423`.
Shard 00 completed without replacement and emitted:

- leaf ledger: file SHA-256
  `c9da80d725d6b11f1e8a7e181dff6b02aa7b604b0aedbf35522e4fd3629de7af`;
- receipt: file SHA-256
  `8a932d0abc64761db4eda758122dca4665afea42cf5e6d97fcc303fb1b46018a`,
  object SHA-256
  `3f61e37aa9cf11e1c564f2585fdfea0c3ba0f1d8baa30828cf831dd19f72a4cc`.

The receipt is complete for exactly 330 assigned inputs.  It records 10,870
route evaluations and 5,600 output leaves:

- 2,979 `STRICT_TERMINAL` leaves;
- 0 `COLLISION3_READY` leaves;
- 2,621 `COLLISION2_HANDOFF` leaves;
- 52 of the 330 input partitions are wholly strict-terminal.

The raw classification census is 779 collision-1 word mismatches, 564
collision-2 owner mismatches, 1,437 outgoing-chart mismatches, 199 unique
first-owner mismatches, 425 collision-1 outgoing-state residuals, 1,484 H1
graph-or-boundary residuals, and 712 regular multi-graph arrangement
residuals.  These sum exactly to the disposition census above.

## Independent cold reconstruction

The final v2 cold verifier source was frozen before either final v2 result at
SHA-256
`0468e3533d02366c4241249b3d87d99801c2c31a094d77ec3b566ab6166a45b5`.
It captures the executor only as pinned inert bytes and AST; it never imports
or executes the executor.  It independently rebuilds the 330 assignment
bindings and all 10,870 numeric routes using the frozen C41 independent-audit
kernel, then reconstructs every exact box, reflected box, witness, method,
disposition, continuation object, row hash, row order, and receipt field.

The cold verification passed with:

- file SHA-256
  `f8a15ed8d19b9148f3083e5356ada9834017562e687e04b103ff7fd4a842be45`;
- object SHA-256
  `9ace9e66c227d882e78b32c94193392feeeb6cbca1fc198bf30a3f0c8e107fe7`;
- 330/330 independently reconstructed source partitions prefix-free;
- 330/330 exact per-source Kraft conservation checks;
- exact equality of all 5,600 independently reconstructed output rows and
  the complete receipt census and line-sequence commitments;
- cold-run elapsed time 3 minutes 56.87 seconds and peak RSS 1,518,112 KiB.

The final coherent hostile suite passed 30/30.  Its file SHA-256 is
`aedcfa3000aea1f152fd9b2d918eef75d35a76a3845f0f09908090a199851afc`
and its object SHA-256 is
`1bbdadb73eaf2cce85ba495eefe10e3bf35cefb0af61e33899bf7f321a8aba11`.
It covers all material shard/census/credit and binding mutations, duplicate
keys, non-finite JSON, BOM/trailing-data inputs, truncated gzip, symlink and
hardlink substitution, descriptor/path replacement TOCTOU, and executor
non-import/non-execution.

## Authority and rejection boundary

The C50d/C53/canonical authority snapshot is byte-identical before and after,
with object SHA-256
`c9a8b97be4bed2008fa132f49e0d4ac0b384e973707ecdf48b27028b7d7e93cf`.
Every leaf, continuation, receipt, verification, and self-test credit field is
zero.  No runtime authority, canonical pointer, or seal was written.

The v1 verification and self-test are explicitly excluded from the final
chain because they straddled a self-test-only malformed-JSON exception-class
correction.  Their immutable rejection/supersession marker has SHA-256
`7080150eded1b69bcfd5fa8d6854f2fec84faeed8b342aea4fa4759ecde2d852`.
Only the v2 source and v2 results are admissible for this audit package.

This is exactly one completed and independently audited shard out of 64.  It
is not an aggregate, does not authorize or predict any other shard, does not
close the 20,879-input C61 residual set, and cannot be promoted to D02 gate
credit.  The remaining 63 shards must each complete under the same frozen
assignment/executor chain and then pass an independent all-shard aggregate
audit before any aggregate claim is available.
