# CM2 Round235 — single-endpoint graph word/key partition

## Verdict

`PASS_PARTIAL_FORMAL_ROUND235`.

All `38,328` Round234 endpoint boxes with exactly one active source/target wall
factor have a strict `t` derivative.  The endpoint zero is therefore a
two-dimensional graph where present.  On every box, the candidate wall-event
time is strictly earlier than all existing events for a source graph or
strictly later for a target graph.  This certifies exact first/last insertion.

Each box is partitioned into event-absent and event-present open sides with
fully reconstructed signed wall words and official exact keys.  The rows use
`92` candidate exact keys.  Active factors are `552` source and `37,776`
target; `X+`, `X-`, `Y+`, and `Y-` each occur `9,582` times.

The remaining endpoint frontier consists of only `16` double-factor boxes.
The separate Round234 crossing-time frontier contains `32` boxes.

## Verification and boundary

The independent verifier does not import or execute the producer and returns
`PASS_INDEPENDENT_ROUND235` after recomputing all `38,328` graph, order, word,
and key rows.  Hash seeds `235071` and `235929` reproduce the frozen hashes.

Round235 issues local finite exact-key partition credit, not whole-root,
known-block, component, maximality, or global-fibre credit.  CM2 remains
`NO-GO_FOR_CLAIM`.

## Frozen hashes

- producer: `8e5f807dfc43632d59cc9c994fd58907080a52bedc7789f8bb507b002ce8641a`;
- certificate: `e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787`;
- result: `5bbcf6780338c9a40fa9c131b0270e4fb934de022cf597d2f82d6b85af68dca2`;
- verifier: `4ce8c9d516dd95f27bea0f951ea2644705af9b50b63362004e3d3e5d7221dc4d`;
- verification: `8009f857b45aa05848b84258f2081bd6de54ff04643387ea3e8fd9c74bdb0e2a`;
- verification result: `60cd47a28980c82744e4838f22842275c59f65245873a663636cb6ea111d7d9a`.
