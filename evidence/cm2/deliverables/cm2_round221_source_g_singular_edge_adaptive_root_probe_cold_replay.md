# Round221 singular-edge adaptive-root probe cold record

This read-only probe takes the `252` fixed-`s`, free-`p` endpoint edges for
which the full transverse derivative was unavailable.  It splits only
unresolved rational edge intervals and re-evaluates the full value interval,
endpoint signs, and transverse derivative on each child.

The run exited `0`:

- elapsed: `0:50.70`;
- adaptive edge loop: `1.251905s`;
- user CPU: `49.72s`;
- system CPU: `0.97s`;
- maximum RSS: `955,184 KiB`;
- maximum configured adaptive depth: `8`.

All 252 original edges were resolved by depth five:

| depth | evaluations | unresolved children | complete original edges |
|---:|---:|---:|---:|
| 1 | 504 | 252 | 0 |
| 2 | 504 | 164 | 88 |
| 3 | 328 | 80 | 172 |
| 4 | 160 | 16 | 236 |
| 5 | 32 | 0 | 252 |

Every original edge has exactly one `UNIQUE_INTERIOR_ROOT` terminal child.
All its other terminal children are certified zero-absent either by a strict
full value interval or by strict monotonicity with equal strict endpoint
signs.  The root-containing child is separated from the chart-singular
endpoint by a finite rational partition.

Together with the endpoint-edge census, this makes the Round223 formal target
`7,232` symbolic unique-root rows plus four strict whole-edge absences.  It
can potentially close all `7,016` Round219 incomplete exact contacts and
reach the full local exact `p/s` contact prefix `7,932 / 7,932`.

This outcome-blind probe grants no formal, component, whole-origin,
global-fibre, or exact-key-disposition credit.

