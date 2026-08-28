# CM2 Round234 — source-G wall endpoint/order depth-6 materialization

Date: 2026-07-27

## Verdict

`PASS_PARTIAL_FORMAL_ROUND234`.

Round234 applies six exact `t` bisection levels to all `2,640` frozen pure
`wall_endpoint_or_count_transition` roots.  It materializes `12,200` strict
positive-volume resolved descendants across `92` exact keys, with zero guard
descendants.  Exactly `408` roots have no depth-6 frontier.

The released coordinate-volume fraction is approximately `87.2752%`.  The
remaining frontier has `38,376` boxes.  Of these, `38,344` retain an endpoint
or count-transition reason and only `32` expose a secondary
`wall_crossing_time_not_strict` reason.  Thus uniform `t` refinement releases
most volume but multiplies endpoint projection boxes; it is not the closure
route for the residual frontier.

## Independent verification

The independent verifier does not import or execute the Round234 producer.  It
reconstructs the `2,640`-root universe from frozen Rounds 179, 220, and 230,
reruns every depth-6 classification, verifies exact volume conservation per
root, and matches every resolved, frontier, and summary row.

Result: `PASS_INDEPENDENT_ROUND234`.

Five semantic mutation classes are rejected.  Cold replays under
`PYTHONHASHSEED=234071` and `234929` reproduce the certificate and verification
result hashes.

## Frozen hashes

- producer: `4bc6867e660cfe1ec936f03fd5543a12a8d69d3dab480366e4a9c3fbd3768d89`;
- certificate: `6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac`;
- certificate result: `d05d6bbc590157e855a577f411668d0f3b7486ccdbea8e47ed30299194b5ba08`;
- verifier: `ccc7711d3e682089344632e6321d6c05402343d937ae967dfd756ea60eef6ae0`;
- verification: `bb4ddd26cffc691d26eaa020dcaab9cba2f581bf5042bcbb247a7462a60eaedb`;
- verification result: `417a8d97fcbba4dd48b99c488b8bb908355f35af014c283b70faf325df307598`.

## Strict boundary and next route

Round234 issues only local positive-3D occurrence rows.  It issues no
whole-root exact-key, known-block, component, maximality, or global-fibre
credit.  CM2 remains `NO-GO_FOR_CLAIM`.

The next route is a parametric endpoint-factor arrangement.  For each residual
box, use the already certified strict `t` derivative of the active source or
target wall factor to represent its zero set as a graph over the `p/s` base.
The graph sides determine wall-event absence/presence.  The `32` secondary
crossing-time boxes require an additional event-time difference graph.  This
must be composed with exact first/last event insertion only after the order
graph is certified.
