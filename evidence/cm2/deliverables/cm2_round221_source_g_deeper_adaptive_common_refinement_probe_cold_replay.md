# Round221 depth 7--10 outcome-blind probe cold record

The read-only probe pins the frozen Round219 source, certificate, and result,
then imports the Round219 interval predicate and continues only the `7,236`
terminal subfaces that were still `UNRESOLVED` at depth six.

It ran once with the workspace Python environment and exited `0`:

- elapsed: `2:54.36`;
- user CPU: `173.37s`;
- system CPU: `0.95s`;
- maximum RSS: `954,660 KiB`;
- effective Arb precision: `256` bits.

The exact observed cost/outcome curve was:

| depth | evaluations | TRACE | ABSENT | UNRESOLVED | new complete contacts | elapsed |
|---:|---:|---:|---:|---:|---:|---:|
| 7 | 14,472 | 3,488 | 3,660 | 7,324 | 0 | `30.275139s` |
| 8 | 14,648 | 3,588 | 3,712 | 7,348 | 0 | `30.892737s` |
| 9 | 14,696 | 3,760 | 3,612 | 7,324 | 0 | `30.847661s` |
| 10 | 14,648 | 3,732 | 3,644 | 7,272 | 0 | `30.387846s` |

All `7,016` incomplete exact contacts retain at least one unresolved child at
every tested depth.  The cumulative complete-contact count therefore remains
Round219's `916`; this probe grants no formal, component, or global credit.

The result rules out further blind dyadic depth as a useful next formal gate:
it narrows the root-containing child but cannot represent the exact boundary
root coordinate needed to close the contact partition.  The next justified
route is a fail-closed symbolic unique-root certificate, backed by strict
monotonicity/interval Newton or Arb root isolation.  Non-simple, endpoint, or
otherwise non-isolated roots must remain unresolved.

