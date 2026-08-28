# Round221 endpoint-edge root census cold record

This read-only outcome-blind probe pins Round219 and the Round186 factor
evaluator.  For each of Round219's `7,236` unresolved terminal subfaces it
identifies the sole non-strict graph endpoint and restricts the active factor
to the corresponding transverse endpoint edge.

The run exited `0`:

- elapsed: `0:54.31`;
- endpoint-edge loop: `6.054343s`;
- user CPU: `53.25s`;
- system CPU: `1.03s`;
- maximum RSS: `954,392 KiB`;
- effective Arb precision: `256` bits.

The graph-axis census first established that every unresolved row has exactly
one non-strict graph endpoint, while the other graph endpoint and full graph
derivative are strict:

- ambiguous lower graph endpoint: `3,618`;
- ambiguous upper graph endpoint: `3,618`;
- fixed `p`: `5,424`;
- fixed `s`: `1,812`.

The transverse endpoint-edge census then found:

| edge class | rows |
|---|---:|
| strict full transverse derivative and opposite strict endpoint signs (`UNIQUE_INTERIOR_ROOT`) | 6,980 |
| strict full transverse derivative and equal strict endpoint signs (`STRICT_MONOTONE_ZERO_ABSENT`) | 4 |
| transverse derivative unavailable (`UNRESOLVED`) | 252 |

The `7,016` incomplete contacts have edge-class multisets:

| edge-class multiset | contacts |
|---|---:|
| one unique interior root | 6,544 |
| two unique interior roots | 216 |
| one unique root plus one strict absence | 4 |
| unresolved | 252 |

Thus a symbolic monotone-root stratification can potentially close `6,764`
additional exact contacts, taking the cumulative exact prefix from `916` to
`7,680 / 7,932`, while the `252` derivative-unavailable contacts remain
fail-closed.

This probe grants no formal, component, whole-origin, global-fibre, or
exact-key-disposition credit.  A formal producer must still assign stable
analytic-root identities, prove the two open 2D sides, materialize the root
stratum and endpoint-to-curve join, and prove that all strata form the exact
contact partition.

